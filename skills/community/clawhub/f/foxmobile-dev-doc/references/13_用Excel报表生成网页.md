# 用Excel报表生成网页


## Excel报表与后台数据

Excel报表与后台数据


**Excel报表与后台数据**

如果你是一个网页设计高手，那么网页的数据展示能力是非常优秀的。

但绝大多数用户，包括我自己，都无法设计出高水准的网页，所以需要一个简单的替代工具，实现复杂数据的展示，特别是手机端的复杂数据展示。

我们选可以利用Excel报表来完成这项任务，但是在Foxtable
2017之前，Excel报表只能根据已经加载的数据生成，而作为服务端程序，通常是没有办法将所有数据加载的。

所以，我们对Excel报表进行了改进，使得其可以直接基于后台数据生成报表。

**一个例子**

如果你设计了一个下图所示的Excel报表模板：

假定系统并没有加载员工表，或者员工表只加载了部分数据，我们用下面的代码，一样可以从后台提取未加载的数据来生成报表，而且非常简单：

Dim
Book As
New XLS.Book(ProjectPath
& "Attachments\资料卡.xls")
Dim
fl As
String =
ProjectPath &
"Reports\资料卡.xls"
book.AddDataTable("员工","数据源名称","Select
\* from {员工} where 姓名 = '王伟'")

Book.Build()

Book.Save(fl)
Dim
Proc As
New
Process
Proc.File
= fl
Proc.Start()

这是生成的报表：

提示：

AddDataTable方法用于从后台提取数据生成一个临时表，由Excel报表模板根据此临时表生成报表。
例如上面的代码中，AddDataTable利用Select语句生成了一个临时表，表名为"员工"。
系统在生成Excel报表的过程中，优先调用AddDataTable生成的临时表，无需担心和现有同名表产生冲突。

AddDataTable的语法为：

AddDataTable(Name,DataSouce,SelectString)
AddDataTable(Name,DataTable)

|  |  |
| --- | --- |
| Name | 字符型，临时表的名称，必须和报表模板中的表名保持一致。 |
| DataSouce | 字符型，用于指定数据源名称。 |
| SelectString | 字符型，用于指定Select语句 |
| DataTable | DataTable型，用于直接指定一个临时DataTable作为报表的数据来源，此DataTable不能是DataTables中的一员。  GroupTableBuilder、CrossTableBuilder、SQLGroupTableBuilder、SQLCrossTableBuilder、SQLJoinTableBuilder和DataTableBuilder的Build方法，都有一个逻辑参数，将此参数设置为True，将生成一个DataTable，此DataTable将不会包括在DataTables中。 例如：    Dim Book As New XLS.Book(ProjectPath &  "Attachments\test.xls")  Dim fl As String =  ProjectPath &  "Reports\test.xls"  Dim g As New  SQLGroupTableBuilder("统计表1", "订单")  g.ConnectionName = "数据源名称"  g.Groups.AddDef("产品")  g.Totals.AddDef("数量")  book.AddDataTable("统计表1", g.Build(True)) '添加临时表  Book.Build()   Book.Save(fl)  Dim Proc As New  Process  Proc.File = fl  Proc.Start() |

**多个数据表和关联**

我们可以添加多个临时表，而且可以在临时表之间建立关联。

假定设计了下图所示的报表模版，用于生成出库单。

此模版涉及到出库和出库明细两个表，这两个表通过出库单号建立关联。

不管系统是否已经加载了这两个表，我们都可以通过下面的代码生成一个出库单：

Dim
Book As
New XLS.Book(ProjectPath
& "Attachments\出库单.xls")
Dim
fl As
String =
ProjectPath &
"Reports\出库单.xls"
book.AddDataTable("出库","数据源名称","Select
\* from {出库} where 出库单编号= 'CK-20030726001'")
'添加父表
book.AddDataTable("出库明细","数据源名称","Select
\* from {出库明细} where 出库单编号= 'CK-20030726001'")
'添加子表
book.AddRelation("出库","出库单编号","出库明细","出库单编号")
'建立关联
Book.Build()
'生成细节区
Book.Save(fl)
'保存工作簿
Dim
Proc As
New Process
'打开工作簿
Proc.File =
fl
Proc.Start()

这是生成的报表：

提示： AddRelation方法用于在临时表之间建立关联。

**AddRelation的语法为：**

AddRelation(ParentTable,ParentCol,ChildTable,ChildCol)

|  |  |
| --- | --- |
| ParentTable | 字符型，父表名称。 |
| ParentCol | 字符型，父表关联列名称，如果有多个关联列，可以用一个字符型数组表示。 |
| ChildTable | 字符型，子表名称。 |
| ChildCol | 字符型，子表关联类名称，如果有多个关联列，可以用一个字符型数组表示。 |

## 后台报表与远程图片

后台报表与远程图片


**后台报表与远程图片**

上一节讲述了基于后台数据生成报表。

在基于后台数据生成报表的过程中，会根据指定的Select语句生成一些临时的数据表(DataTable)，这些临时表和现有的DataTable没有任何关系，在代码执行完毕之后，会被自动销毁。

你也许担心一个问题，既然这些临时表是独立存在的，如果我们使用了FTP进行远程图片管理，
那么之前所有的相关设置和这些临时表应该是没有关系的，这是否会导致[图片引用](../chmhelp/1387.htm)失败呢？

实际上我们无需担心这个问题，假定我们通过下面的代码添加了一个临时表：

book.AddDataTable("员工","","Select
\* from {员工} where 姓名 = '王伟'")

此临时表的名称为"员工"，在生成报表前，系统会自动从现有的数据表中找到员工表，并从中提取有关远程文件的设置应用到临时表中。
系统是根据表名匹配的，所以添加临时表的时候，必须和对应的数据表同名。

显然如果员工表没有加载，那么系统将无法从现有表中提取相关设置应用到临时表中，此时可以通过Book的DataTables属性引用这些临时表，用代码设置列的扩展类型、FTP地址和密码等，参考代码：

Dim
Book As
New XLS.Book(ProjectPath
&
"Attachments\资料卡.xls")
Dim
fl As
String =
ProjectPath &
"Reports\资料卡.xls"
book.AddDataTable("员工","","Select
\* from {员工} where 姓名 = '王伟'")
**book****.DataTables("员工").DataCols("照片").ExtendType
= ExtendTypeEnum.Images
'扩展类型为图片
book.DataTables("员工").DataCols("照片").Remote
= True '使用FTP管理
With
book.DataTables("员工").DataCols("照片").FTpClient
'设置FTP属性

.Host
= "168.218.199.25"
    .Account =
"ftpuser"
    .Password =
"13613800"
End

With**
Book.Build()
Book.Save(fl)
Dim
Proc As
New
Process
Proc.File
=  fl
Proc.Start()

## 发送Excel报表

发送Excel报表


**发送Excel报表**

我们通常会采用下面的HttpRequest事件代码来响应用户访问Excel报表的请求：

Select
Case e.path
    Case "ckd.xls"
        Dim
Book As New
XLS.Book(ProjectPath
&
"Attachments\出库单.xls")
        Dim fl
As String =
ProjectPath &
"Reports\出库单.xls"
        book.AddDataTable("出库","数据源名称","Select
\* from {出库}
where
出库单编号=
'CK-20030726001'")
'添加父表
        book.AddDataTable("出库明细","数据源名称","Select
\* from {出库明细}
where
出库单编号=
'CK-20030726001'")
'添加子表

book.AddRelation("出库","出库单编号","出库明细","出库单编号")
'建立关联

Book.Build()

        Book.Save(fl)


e.WriteFile(fl)
End
Select

过程很简单：基于模版生成Excel报表，将生成的报表保存为一个文件，然后用WriteFile方法将文件发送到客户端的浏览器。

这样的设计有以下不足：

1、虽然WriteFile是异步执行的，但是Excel报表的生成和保存却是和主线程同步的，且Excel报表的生成并非很高效，所以用户量比较大的时候，会影响效率。
2、整个过程要分别保存和读取一次文件，我们知道计算机性能的瓶颈就是硬盘的读写，所以这同样会影响效率。
3、由于要保存为实际的文件，所以容易出现文件名冲突，假定有多个用户同时访问，上面的代码肯定会出错，虽然可以采用一些手段避免同名冲突，但毕竟增加了工作量。

**WriteBook**

为彻底解决上述问题，我们为HttpRequest事件增加了一个WriteBook方法，此方法专门用于发送Excel报表，其语法为：

WriteBook(Book,FileName，InLine)

|  |  |
| --- | --- |
| Book | 要发送的Excel报表 |
| FileName | 客户端浏览器下载此报表时使用的文件名 |
| InLine | 可选参数，逻辑型，是否直接在浏览器显示报表，默认为True，设为False将下载报表。  实际上除了iOS设备，其他设备不管如何设置，都会下载报表。 |

WriteBook是异步执行的，而且在发送报表之前，还是会异步执行Build方法生成报表，所以如果不是Excel报表模板，请将Book的PreBuild属性设置为False，避免WriteBook执行Build方法。

**一个例子**

HttpRequest事件代码：

Select
Case e.path
    Case
"ckd.xls"
'直接在浏览器显示
        Dim
Book As New
XLS.Book(ProjectPath
& "Attachments\出库单.xls")
        book.AddDataTable("出库","数据源名称","Select
\* from {出库} where 出库单编号= 'CK-20030726001'")
'添加父表
        book.AddDataTable("出库明细","数据源名称","Select
\* from {出库明细} where 出库单编号= 'CK-20030726001'")
'添加子表
        book.AddRelation("出库","出库单编号","出库明细","出库单编号")
'建立关联
        e.WriteBook(book,"出库单.xls",True)
    Case "emp.xls"
'下载为文件
        Dim
Book As New
XLS.Book(ProjectPath
& "Attachments\资料卡.xls")
        book.AddDataTable("员工","数据源名称","Select
\* from {员工} where 姓名 = '王伟'")

e.WriteBook(book,"emp.xls",False)
    Case "orders.htm"
'请求的是网页，返回的是Excel文件
        Dim nms()
As String =
{"产品","客户","数量","单价","金额","日期"}
        Dim cmd
As New
SQLCommand
        cmd.ConnectionName
= "数据源名称"

        cmd.CommandText
= "Select
产品,
客户,
数量,
单价,
数量
\* 单价
As 金额,
日期
From {订单}
Where 日期 = #" &
Date.Today &
"#"
        Dim dt
As DataTable
= cmd.ExecuteReader
        Dim
Book As New
XLS.Book
        Dim
Sheet As XLS.Sheet
= Book.Sheets(0)
        For c
As Integer =
0 To
nms.Length -
1
            Sheet(0,
c).Value =
nms(c)
        Next
        For r
As Integer =
0 To
dt.DataRows.Count
- 1
            For
c As Integer
= 0 To
nms.Length -
1
                Sheet(r
+ 1, c).Value
= dt.Datarows(r)(nms(c))
            Next
        Next
        book.PreBuild
= False
'非报表模请将PreBuild
属性设置为False
        e.WriteBook(book,"订单.xls",True)
End
Select

提示：

1、InLine参数仅对iOS设备有效。
2、非报表模板请将Book的PreBuild参数设置为False。
3、FileName参数可以和客户请求的文件名不同，甚至可以在客户请求一个网页时，返回一个excel文件。

尽管iOS设备可以在浏览器直接查看Office文档，但是兼容性却不好，例如上面的第二个报表，分别在iOS上的浏览器和iOS上的WPS显示，存在很大的差异：

iOS上的浏览器显示为：

iOS上的WPS显示为：

## 用Excel报表生成网页

用Excel报表生成网页


**用Excel报表生成网页**

我们可以直接用Excel报表生成网页后发送给客户端。

用Excel报表生成网页需要事先约定一个目录，每次用户访问这个目录，服务端会进行一些特殊的处理，用于将Excel报表转换成网页并发送到客户端，代码一般类似：

If
e.Path.StartsWith("报表目录\")
    e.ResponseEncoding
= "gb2312"
'这里要正确设置编码格式, 否则会乱码
    Select Case
e.Path
        Case
"报表目录\网页文件.htm"
            Dim
Book As New
XLS.Book(ProjectPath
&
"Attachments\报表模板.xls")
            e.WriteBookAsHTML(Book)
        Case Else
            e.AsReportServer("报表目录\")

    End
Select
Else
    '用于生成常规网页的代码
End
If

WriteBookAsHTML方法会自动生成Excel报表，并将生成结果转换成网页后发送给客户端浏览器。

AsReportServer看起来没有意义，实际上你删除这行代码的话，客户端不会显示任何内容，这是因为Excel报表转换成网页之后，并非只有一个单一的网页文件，还会生成一系列的辅助文件，需要通过AsReportServer方法将这些辅助文件发送给客户端。

我们也无需考虑多线程以及临时文件的处理，Foxtable会自动完成这些工作。

需要注意的是：
AsReportServer的参数就是约定的报表目录，必须和第一行指定的报表目录相同，报表目录也必须是专用的，不能再用于访问其他网页。

**示例一**

1、首先打开CaseStudy目录下的示例文件"Excel报表.foxdb"文件。

2、将HttpRequest事件代码设置为：

If
e.Path.StartsWith("Reports\")
    e.ResponseEncoding
= "gb2312"
    Select Case
e.Path
        Case
"Reports\ckd.htm"
            Dim
Book As
New XLS.Book(ProjectPath
&
"Attachments\出库单.xls")
            e.WriteBookAsHTML(Book)
       Case
"Reports\jianli.htm"
            Dim
Book As
New XLS.Book(ProjectPath
&
"Attachments\资料卡.xls")
            e.WriteBookAsHTML(Book)
        Case Else
            e.AsReportServer("Reports\")
    End
Select
End
If

3、在命令窗口执行：

HttpServer.Prefixes.Add("http://127.0.0.1/")
HttpServer.Start()

现在在浏览器输入网址：

http://127.0.0.1/Reports/ckd.htm

即可得到网页：

输入地址：

http://127.0.0.1/Reports/jianli.htm

即可得到网页：

**示例二**

更多的时候，我们需要根据客户端提交的访问请求，从后台提起对应的数据生成Excel报表并转成网页，例如我们将HttpRequest事件代码改为：

If
e.Path.StartsWith("Reports\")
    e.ResponseEncoding
= "gb2312"
    Select Case
e.Path
        Case
"Reports\jianli.htm"
            Dim
Book As New
XLS.Book(ProjectPath
&
"Attachments\资料卡.xls")
            book.AddDataTable("员工","","Select
\* from {员工}
where
姓名
= '"
& e.GetValues("nm")
& "'")
            e.WriteBookAsHTML(Book)
        Case Else
            e.AsReportServer("Reports\")
    End
Select
End
If

现在输入网址：

http://127.0.0.1/Reports/jianli.htm?nm=张颖

可得到网页：

**示例三**

我们也可以将Excel报表转换成PDF格式发送给客户端浏览器，例如我们将HttpRequest事件代码改为：

If
e.Path.StartsWith("Reports\")
    e.ResponseEncoding
= "gb2312"
    Select Case
e.Path
        Case
"Reports\jianli.htm"
            Dim
Book As New
XLS.Book(ProjectPath
&
"Attachments\资料卡.xls")
            book.AddDataTable("员工","","Select
\* from {员工}
where
姓名
= '"
& e.GetValues("nm")
& "'")
            e.WriteBookAsPDF(Book)
        Case Else
            e.AsReportServer("Reports\")
    End
Select
End
If

代码和示例二基本是相同的，只是将WriteBookAsHTML换成了WriteBookAsPDF，现在输入网址：

http://127.0.0.1/Reports/jianli.htm?nm=张颖

浏览器会显示一个PDF文件：

**示例四**

常规的Excel文件，一样可以转换为网页发送，不过在使用WriteBookAsHTML或WriteBookAsPDF方法是，要将第二个参数设置为False，通知系统这不是一个模板文件，无需生成报表，直接发送即可，例如：

If
e.Path.StartsWith("Reports\")


e.ResponseEncoding
= "gb2312"
    Select Case
e.Path
        Case
"Reports\jianli.htm"
            Dim
Book As New
XLS.Book(ProjectPath
&
"Attachments\资料卡.xls")
            e.WriteBookAsHTML(Book,False)
'第二个参数设置为False,表示这不是模板,直接发送即可
        Case Else
            e.AsReportServer("Reports\")
    End
Select
End
If

示例五

如果一个Excel文件有部分表是模板，有部分表是常规表格，那么怎么处理呢？一样的简单，WriteBookAsHTML和WriteBookAsPDF都可以指定在生成报表的时候，将部分表作为常规表处理，例如：

If
e.Path.StartsWith("Reports\")
    e.ResponseEncoding
= "gb2312"
    Select Case
e.Path
        Case
"Reports\jianli.htm"
            Dim
Book As New
XLS.Book(ProjectPath
& "Attachments\资料卡.xls")
            e.WriteBookAsHTML(Book,1,2)
'第二个表和第三个表作为常规表直接发送.
        Case Else
            e.AsReportServer("Reports\")
    End
Select
End
If

## VBA(Excel)和网页

VBA


**VBA(Excel)和网页**

如果你是Excel的资深用户，一定会留恋VBA，实际上你的VBA知识在Foxtable一样有用，原来的VBA代码只需稍作修改，就可以在Foxtable中使用。

关于如何在Foxtable使用VBA操作Excel文件，参考：[Excel与VBA](http://www.foxtable.com/webhelp/topics/2121.htm)

本节介绍如何将VBA处理后的Excel文件转换为网页或PDF文件发送到客户端，考虑Foxtable的Excel报表功能并不支持图表，本节的内容对于需要实现图文并茂网页的用户很有意义。

HttpRequest有两个方法，WriteExcelAsHTML和WriteExcelAsPDF，分别用于将Workbook对象转换为网页或PDF文件发送到客户端。

**一个简单的例子**

1、打开CaseStudy目录下的文件"Excel报表.foxtdb"

2、将HttpRequest事件代码设置为：

If
e.Path.StartsWith("Reports\")
    e.ResponseEncoding
= "gb2312"
    Select Case
e.Path
        Case
"Reports\table1.htm"
            Dim
app As New
MSExcel.Application
            Dim
wb As MSExcel.Workbook
= app.WorkBooks.Open(ProjectPath
&
"Attachments\table.xlsx")
            'VBA代码
            e.WriteExcelAsHTML(wb)
        Case
"Reports\table2.htm"
            Dim
app As New
MSExcel.Application
            Dim
wb As MSExcel.Workbook
= app.WorkBooks.Open(ProjectPath
&
"Attachments\table.xlsx")

'VBA代码
            e.WriteExcelAsPDF(wb)
        Case Else
            e.AsReportServer("Reports\")
    End
Select
End
If

3、在命令窗口执行：

HttpServer.Prefixes.Add("http://127.0.0.1/")
HttpServer.Start()

现在在浏览器输入网址：

http://127.0.0.1/Reports/table1.htm

即可得到网页：

如果在浏览器输入网址：

http://127.0.0.1/Reports/table2.htm

会以PDF格式显示上图中的内容。

**一定要多线程**

以上代码并不会自动多线程执行，所以效率很低，实际应用的时候，一定要多线程执行，否则多个用户同时访问的时候，排队等候的时间会很长，甚至会出现超时错误。

我们可以用异步函数实现多线程，异步函数后面会有专门的章节介绍，目前我们只需大概了解其用法即可。

我们看看如何通过异步函数将上述代码改为多线程执行。

1、新建一个内部函数，函数名"ExcelWeb"(名称可以随意)，代码为：

Dim
e As
RequestEventArgs =
args(0)
e.ResponseEncoding
= "gb2312"
Select
Case e.Path
    Case
"Reports\table1.htm"
        Dim app
As New
MSExcel.Application
        Dim wb
As MSExcel.Workbook
= app.WorkBooks.Open(ProjectPath
&
"Attachments\table.xlsx")
        'VBA代码
        e.WriteExcelAsHTML(wb)
    Case
"Reports\table2.htm"
        Dim app
As New
MSExcel.Application
        Dim wb
As MSExcel.Workbook
= app.WorkBooks.Open(ProjectPath
&
"Attachments\table.xlsx")
        'VBA代码
        e.WriteExcelAsPDF(wb)
    Case Else
        e.AsReportServer("Reports\")
End
Select
e.Handled
= True '通知系统异步函数执行完毕,可以关闭信道

2、将HttpRequest事件代码改为：

If
e.Path.StartsWith("Reports\")
    e.AsyncExecute
= True
'通知系统异步执行,不要关闭信道
    Functions.AsyncExecute("ExcelWeb",e)
End
If

## 在服务端使用专业报表

在服务端使用专业报表


**在服务端使用专业报表**

上一节我们学习了使用Excel报表生成网页或PDF文件发送到客户端浏览器，这种方式需要在服务端安装Office，而且效率也较低。

我们可以使用专业报表(个人建议你作为开发者，应该学一下专业报表，真的不难)代替Excel报表，效率可以提高6倍左右，且更加灵活，能实现更为复杂的报表功能。

但是专业报表目前只能完美生成PDF文件，不过既然都是静态的，PDF的效果更好，如果要在客户端打印，PDF会更有优势，因为它可以进行页面设置。

HttpRquest事件有个WriteReportAsPDF方法，用于将专业报表生成一个PDF文件并发送到客户端，而且生成过程和发送过程都是异步的，使用起来很方便。

**一个例子**

接下来我们用一个例子，来看看如何在服务端使用专业报表，并和Excel报表比较一下效率，示例中使用的专业报表可以参考：

<http://www.foxtable.com/webhelp/topics/1238.htm>

1、首先打开CaseStudy目录下的示例文件"Excel报表.foxdb"文件。

2、将HttpRequest事件代码设置为：

If
e.Path.StartsWith("Reports\")
    e.ResponseEncoding
= "gb2312"
    Select
Case e.Path
        Case
"Reports\jianli1.htm"
'Excel报表
            Dim
Book As
New XLS.Book(ProjectPath
&
"Attachments\资料卡.xls")
            e.WriteBookAsHTML(Book)
        Case
"Reports\jianli2.htm"
'专业报表
            Dim
doc As
New PrintDoc
'定义一个报表
            Dim rt
As New
prt.RenderTable()
'定义一个表格对象
            Dim rx
As New
prt.RenderText
'定义一个文本对象
            Dim
CurRow As
Row = Tables("员工").Current
            '加入标题
            rx.text
= "员工资料卡"
            rx.Style.FontBold
= True
'字体加粗
            rx.Style.FontSize
= 16
'大体大小为16磅
            rx.Style.TextAlignHorz
= prt.AlignHorzEnum.Center
'水平居中排列
            rx.Style.Spacing.Bottom
= 3
'和下面的对象(表格)距离3毫米
            doc.Body.Children.Add(rx)
'加入到报表中
            '指定行数?列数?列宽?行高
            rt.Rows.Count
= 7
'设置总行数
            rt.Cols.Count
= 5
'设置总列数
            rt.Height
= 80
'设置表格的高度为80毫米
            rt.Rows(6).Height
= 40
'设置第7行(显示备注的行)的高度为40毫米,剩余高度被平均分排到其他行
            rt.Cols(0).Width
= 24
'设置前四列的宽度,剩余的宽度被分配给5列(显示图片的那列)
            rt.Cols(1).Width
= 35
            rt.Cols(2).Width
= 24
            rt.Cols(3).Width
= 40
            '设置合并单元格
            rt.Cells(0,4).SpanRows
= 6
'第1行第5个单元格向下合并6行(用于显示照片)
            rt.Cells(4,1).SpanCols
= 3
'第5行第2个单元格向右合并3列(用于显示地址)
            rt.Cells(6,0).SpanCols
= 5
'第7行第1个单元格向右合并5列(用于显示备注)
            '设置表格样式
            rt.CellStyle.Spacing.All
= 1
'单元格内容缩进1毫米
            rt.Style.GridLines.All
= New prt.Linedef
'设置网格线
            rt.Style.TextAlignVert
= prt.AlignVertEnum.Center
'内容垂直居中
            rt.Rows(6).Style.TextAlignVert
= prt.AlignVertEnum.Top
'唯独第7行是备注,内容靠上对齐

'下面很简单,指定每一个单元格的内容

rt.Cells(0,0).Text=
"姓名"
            rt.Cells(0,1).Text
= CurRow("姓名")
            rt.Cells(0,2).Text=
"出生日期"
            rt.Cells(0,3).Text
= CurRow("出生日期")
            rt.Cells(1,0).Text=
"部门"
            rt.Cells(1,1).Text
= CurRow("部门")
            rt.Cells(1,2).Text=
"雇佣日期"
            rt.Cells(1,3).Text
= CurRow("雇佣日期")
            rt.Cells(2,0).Text=
"性别"
            rt.Cells(2,1).Text
= CurRow("性别")
            rt.Cells(2,2).Text=
"职务"
            rt.Cells(2,3).Text
= CurRow("职务")
            rt.Cells(3,0).Text=
"城市"
            rt.Cells(3,1).Text
= CurRow("城市")
            rt.Cells(3,2).Text=
"邮政编码"
            rt.Cells(3,3).Text
= CurRow("邮政编码")
            rt.Cells(4,0).Text=
"地址"
            rt.Cells(4,1).Text
= CurRow("地址")
            rt.Cells(5,0).Text=
"家庭电话"
            rt.Cells(5,1).Text
= CurRow("家庭电话")
            rt.Cells(5,2).Text=
"办公电话"
            rt.Cells(5,3).Text
= CurRow("办公电话")
            rt.Cells(6,0).Text
= CurRow("备注")
            rt.Cells(0,4).Image
= GetImage(CurRow("照片"))
            doc.Body.Children.Add(rt)
'将表格对象加入到报表中
            e.WriteReportAsPDF(doc)
'以PDF格式将专业报表发送到客户端.
        Case Else
            e.AsReportServer("Reports\")
    End
Select
End
If

3、在命令窗口执行：

HttpServer.Prefixes.Add("http://127.0.0.1/")
HttpServer.Start()

现在在浏览器输入网址：

http://127.0.0.1/Reports/jianli1.htm

得到的是通过Excel报表生成的PDF文件。

如果输入网址：

http://127.0.0.1/Reports/jianli2.htm

得到的是通过专业报表生成的PDF文件。反复刷新页面，可以看到专业报表的反应速度远远超过Excel报表。

4、如果你要使用后台数据生成专业报表，可以参考：

[SQLCommand](http://www.foxtable.com/webhelp/topics/0696.htm)

[SQLFind](http://www.foxtable.com/webhelp/topics/2911.htm)

[SQLSelect](http://www.foxtable.com/webhelp/topics/2900.htm)