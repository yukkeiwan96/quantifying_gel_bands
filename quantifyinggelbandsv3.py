################################ALERT####################################
#If you try to run the program for the first time after opening imageJ, #
#a error console will pop up. Just close the the console window, and the#
#program will run perfectly fine.                                       #
#########################################################################

#MIT License

#Copyright (c) 2019 Yuk Kei Wan

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import os
from ij import IJ, ImagePlus, Macro, ImagePlus, WindowManager
from ij.measure import ResultsTable, Measurements
from ij.plugin.frame import RoiManager
from ij.plugin import ImageCalculator
from ij.process import ImageProcessor
from ij.gui import NonBlockingGenericDialog
from ij.gui import Roi
from loci.plugins import BF
from loci.plugins.in import ImporterOptions

gd = NonBlockingGenericDialog("Image Info")
gd.addStringField("1st lane upper left x coordinate", "")
gd.addStringField("1st lane upper left y coordinate", "")
gd.addStringField("last lane upper right x coordinate", "")
gd.addStringField("last lane lower right y coordinate", "")
gd.addStringField("number of lanes to compare", "")
gd.addStringField("number of bands", "")
gd.showDialog()
x= int(gd.getNextString())
y= int(gd.getNextString())
rx= int(gd.getNextString())
ly= int(gd.getNextString())
h=ly-y
n= int(gd.getNextString())
lane=n
b= int(gd.getNextString())
lw= int((rx-x)/n)
imp = IJ.getImage()
#IJ.run("Invert")
IJ.makeRectangle(x, y, lw, h)
IJ.run("Select First Lane")
for i in range(1,n-1):
 x+=lw
 IJ.makeRectangle(x, y, lw, h)
 IJ.run("Select Next Lane")
x+=lw
IJ.makeRectangle(x, y, lw, h)
IJ.run("Plot Lanes")
IJ.run("Scale to Fit")
image = WindowManager.getCurrentImage()
ip = image.getProcessor()
px = ip.getWidth()-5
py = ip.getHeight()-19
IJ.makeRectangle(5, 15, px, py)
IJ.run("Crop")
ia = WindowManager.getCurrentImage()
ipa = ia.getProcessor()
nx = ipa.getWidth()
ny = ipa.getHeight()
IJ.newImage("vertical","8-bit White",nx,ny,1)
ib = WindowManager.getCurrentImage()
ipb = ib.getProcessor()

bd = NonBlockingGenericDialog("Band Size")
for i in range(0,b):
 bd.addStringField("lines set "+str(i+1), "")
bd.showDialog()
li=[]
for i in range(0,b):
 s= bd.getNextString()
 s= s.split(",")
 a=int(s[0])
 b=int(s[1])
 lo=[a,b]
 li.append(lo)

for a in li:
 IJ.makeLine(a[0], 0, a[0], 1318)
 IJ.setForegroundColor(0, 0, 0)
 IJ.run("Draw")
 IJ.makeLine(a[1], 0, a[1], 1318)
 IJ.setForegroundColor(0, 0, 0)
 IJ.run("Draw")
ical= ImageCalculator()
ic= ical.run("Max create", ia,ib)
ipc= ic.getProcessor()
dic={}
ib.changes= False
ib.close()
for x in range(0,nx):
 for y in range(0,ny):
  if ipc.getPixel(x,y) == 0:
   if x not in dic:
     dic[x]=[y]
   else:
     dic[x].append(y)
kl=[]
for k in dic:
 kl.append(k)
nok=len(kl)
nl=[]
rm=[]
for n in dic[kl[0]]:
 nl.append(n)
for n in nl:
 cou=0
 for k in dic:
  if n in dic[k]:
   cou+=1
 if cou== nok:
  rm.append(n)
for n in rm:
 for i in dic:
  dic[i].remove(n)
for key in dic:
 length= len(dic[key])
 if length > lane:
  col=[]
  av=[]
  for l in range(0,length):
   if l < length-1:
    cur=dic[key][l]+1
    nex=dic[key][l+1]
   else:
    nex=dic[key][l]
    cur=nex-1
   if cur == nex:
    rcur=cur-1
    col.append(rcur)
   elif cur != nex:
    if len(col) >0:
      colav=sum(col)/len(col)
      av.append(colav)
      col=[]
    else:
     av.append(cur)
  dic[key]=av
la=[]
for e in li:
 for o in range(0,lane):
  lp=[e[0],dic[e[0]][o], e[1], dic[e[1]][o]]
  la.append(lp)
#print la
ia = WindowManager.getCurrentImage()
ipa = ia.getProcessor()
for a in li:
 IJ.makeLine(a[0], 0, a[0], 1318)
 IJ.setForegroundColor(0, 0, 0)
 IJ.run("Draw")
 IJ.makeLine(a[1], 0, a[1], 1318)
 IJ.setForegroundColor(0, 0, 0)
 IJ.run("Draw")
for c in la:
 IJ.makeLine(c[0], c[1], c[2], c[3])
 IJ.setForegroundColor(0, 0, 0)
 IJ.run("Draw")
 xl=(c[0]+c[2])/2
 if c[3]>c[1]:
  yl=(c[1]+c[3])/2
 else:
  yl=c[1]-5
 IJ.doWand(xl,yl)
 IJ.run("Measure")
fd = NonBlockingGenericDialog("Save Output File")
fd.addStringField("Name ", "")
fd.showDialog()
name= fd.getNextString()
rt= ResultsTable.getResultsTable()
outDir = IJ.getDirectory("Output Directory")
rt.saveAs(outDir+name+".csv")
