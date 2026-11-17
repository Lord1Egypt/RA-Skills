# 生成并发送PDF文件


# 生成并发送PDF文件

生成并发送PDF文件


**生成并发送PDF文件**

在Foxtable
2025之前，要生成PDF文档发送给客户端，需要向通过Excel报表、Word报表或专业报表生成报表，然后另存或转换为PDF格式，效率很低，而且兼容性极差。

从Foxtable
2025开始，我们可以通过PDFCreator快速生成PDF文档。

而且PDFCreator生成的PDF文档，无需保存为文件，可以直接发送到客户端，效率是原来的千百倍，而且不再有任何兼容性问题。

HttpRequest事件为此专门增加了一个WritePDFCreator方法，其语法为：

WritePDFCreator(Creator, FileName, Inline)

|  |  |
| --- | --- |
| Creator | 要发送的PDFCreator |
| FileName | 客户端浏览器下载此文件时使用的文件名 |
| InLine | 可选参数，逻辑型，是否直接在浏览器显示PDF文件，默认为True，设为False将直接下载。 |

**示例**

将HttpRequest事件代码设置为：

Dim
pdc
As

New
PDFCreator()
Dim
rect
As
RectangleF = pdc.PageRectangle()
rect.Inflate( - 72, - 72)
'
Dim
fnt
As

New
Font("微软雅黑",
12)
pdc.DrawString("Hello
Foxtable!",
fnt, Brushes.Black, rect)
e.WritePDFCreator(pdc,

"test.pdf")

现在客户端访问网页，可以瞬间得到一个名为"test.pdf"的PDF文件。

你也可以转换成网页格式再发送给客户端，参考代码：

Dim
pdc
As

New
PDFCreator()
Dim
rect
As
RectangleF = pdc.PageRectangle()
rect.Inflate( - 72, - 72)
'
Dim
fnt
As

New
Font("微软雅黑",
12)
pdc.DrawString("Hello
Foxtable!",
fnt, Brushes.Black, rect)
Dim
tmpPath
As

String
= ProjectPath &

"HttpTempFiles\"
If
FileSys.FileExists(tmpPath) =
False

Then
    FileSys.CreateDirectory(tmpPath)
End

If


Dim
tempFile
As

String
= tmpPath & Rand.NextString(10) &
".html"
pdc.SaveToHtmL(tempFile)
e.WriteFile(tempFile)

提示;

1、所有浏览器都支持直接显示PDF文件，所以一般没有必要转成HTML再发送。

2、临时文件建议放在HttpTempFiles子目录中，方便系统自动清理。