# 生成并发送Word文件


# 生成并发送Word文件

生成并发送Word文件


**生成并发送Word文件**

从Foxtable 2025开始，我们可以通过WordCreator快速生成Word文件。

此外，HttpRequest事件增加了一个WriteWordCreator方法，用于将WordCreator的内容发送到客户端，其语法为：

WriteWordCreator(Creator, FileName, Inline)

|  |  |
| --- | --- |
| Creator | 要发送的WordCreator |
| FileName | 客户端浏览器下载此报表时使用的文件名 |
| InLine | 可选参数，逻辑型，是否直接在浏览器显示报表，默认为True，设为False将下载报表。  实际上除了iOS设备，其他设备不管如何设置，都会下载报表。 |

**示例**

将HttpRequest事件代码设置为：

Dim
wdc
As

New
WordCreator()
Dim
txt
As

String
For
i
As

Integer
= 1
To
5
    txt = txt &

"Foxtable不仅是一个优秀的应用软件，同时又是一个高效率的开发工具。"
Next
With
wdc.AddParagraph(txt)
    .ForeColor = Color.Green
    .Font =
New
Font("宋体",
9)
    .FirstLineIndent = 20
    .SpaceBetweenLines = 10
    .Alignment = Word.RtfHorizontalAlignment.Justify

End

With

e.WriteWordCreator(wdc,

"test.docx")
'直接发送，不需要启动word程序，也不需要
先保存为文件，所以效率极高

现在客户端访问网页，可以瞬间得到一个名为"test.docx"的Word文件。