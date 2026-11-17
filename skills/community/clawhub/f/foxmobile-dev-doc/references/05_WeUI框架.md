# WeUI框架


## 使用框架生成网页

使用框架生成网页


**使用框架生成网页**

其实即使是网页设计高手，想要好的设计效果，多数也是要使用框架的，至于菜鸟，更是离不开框架。
你可以使用第三方的框架，目前用得比较多的是[jQuery](http://www.w3school.com.cn/jquery/index.asp),
在这个基础上还有两个官方维护的界面框架，分别是[jQueryUI](http://www.runoob.com/jqueryui/jqueryui-tutorial.html)和[jQuery
Mobile](http://www.w3school.com.cn/jquerymobile/index.asp)，前者适合常规网页设计，后者适合手机端网页设计。
第三方框架的一般都是有js和css文件组成，如何使用，我们之前已经介绍，这里就不重复了，参考：[使用JavaScript文件](0016.htm)
[使用CSS文件](0017.htm)

FoxTable内置了一个框架，这个框架基于腾讯的微信网页开发样式库(WeUI)，选择这个框架，不是因为这个框架有多么的优秀，是为了让你开发的网页未来能更好地和微信整合，毕竟都是腾讯的产品。
我们用一个简单的例子来说明使用这个框架的步骤：

1、准备WeUI框架文件

你可以在以下地址下载到WeUI框架文件：

<http://www.foxtable.com/download/mobile/weui.zip>

解压会得到三个文件，分别是：

weui.me.js
weui.me.css
weui.min.css

解压后将上述三个文件复制到"d:\web\weui"目录下

2、用以下代码开启http服务网：

HttpServer.Prefixes.Add("http://\*/")
HttpServer.WebPath
= "d:\web"
'指定静态文件存储位置
HttpServer.Start()

重要提示，必须将HttpServer的WebPath设置为正确的路径，否则框架将不会生效。

3、将HttpRequest事件代码设置为：
Select
Case e.Path
    Case "addnew.htm"


Dim wb
As New WeUI

'定义一个基于weui框架的网页生成器
        wb.AddForm("","form1","addnew.htm")
        With wb.AddInputGroup("form1","ipg1","新增订单")
            .AddSelect("cp","产品","PD01|PD02|PD03|PD04|PD05")
            .AddInput("gy","雇员","text")
            .AddInput("kh","客户","text")
            .AddInput("dj","单价","number")
            .AddInput("zk","折扣","number")
            .AddInput("sl","数量","number")
            .AddInput("rq","日期","date")
        End With
        With wb.AddButtonGroup("form1","btg1",True)
            .Add("btnok","确定")
        End With
        e.WriteString(wb.Build) '生成网页
End Select

3、现在通过手机访问，可以得到下图所示的网页：

你可以通过网页浏览器查看上述网页的源代码，合计有73行，而Foxtable的Httprequest事件只用了14行代码就生成了这个网页。

节省的代码量超过了80%，更重要的是，上述代码简洁易懂，不涉及任何网页设计知识，完全是傻瓜式的，而且网页效果很专业，一般用户完全靠自己编码，可能很难做出这样的效果。

## 请输入正确网址

请输入正确网址


**请输入正确网址**

在很大程度上而言，本节内容真的是多余，输入正确网址难道也需要专门提醒吗？

可就是有用户犯这样的错误，而且还不少，^\_^

以我们上一节的例子而言，HttpRequest事件代码为：

Select
Case e.Path
    Case "addnew.htm"

Dim wb
As New WeUI
'定义一个基于weui框架的网页生成器
        wb.AddForm("","form1","addnew.htm")
        With wb.AddInputGroup("form1","ipg1","新增订单")
            .AddSelect("cp","产品","PD01|PD02|PD03|PD04|PD05")
            .AddInput("gy","雇员","text")
            .AddInput("kh","客户","text")
            .AddInput("dj","单价","number")
            .AddInput("zk","折扣","number")
            .AddInput("sl","数量","number")
            .AddInput("rq","日期","date")
        End With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btnok","确定")
        End With
        e.WriteString(wb.Build) '生成网页
End Select

那么测试的时候，应该输入：

http://ip地址/addnew.htm

如果是本机测试，就是：

http://127.0.0.1/addnew.htm

相当多的用户只是简单的输入ip地址，不输入后面的网页名称，导致网页内容不能显示，然后很肯定地认为框架有问题。

如果你想直接输入ip或者域名就能访问某个页面，请参考下一节[设置默认页面](0245.htm)

## 设置默认网页

设置默认网页


**设置默认网页**

一个网页管理系统会有多个网页，其中一个只需输入IP或者域名就能访问的网页，称为默认网页。

设置默认网页很简单，e.path为空的时候，表示要访问默认网页。

例如HttpRequest事件代码：

Dim
wb As
New WeUI
'定义一个基于weui框架的网页生成器
Select
Case e.Path
    Case "addnew.htm",""
        wb.InsertHTML("这是默认页面addnew.htm")

    Case "order.htm"

wb.InsertHTML("这是普通页面order.htm")

End
Select
e.WriteString(wb.Build)
'生成网页

上面的代码生成了两个网页，其中addnew.htm是默认页面，可以直接通过ip访问，也可以输入完整路径：

http://127.0.0.1/
http://127.0.0.1/addnew.htm

另一个页面order.htm，是普通页面，必须输入完整路径才能访问：

http://127.0.0.1/order.htm

## 用Chorme模拟手机

用Chorme模拟手机


**用Chorme模拟手机**

WeUI框架主要是针对手机的，如果每次修改HttpRequest代码后，都要通过手机访问来预览效果，可能会影响开发效率。

建议在开发电脑上，安装谷歌的Chorme浏览器。

在新版的Chorme中，按“Ctrl+Shift+I”，会进入开发者工具界面，在这个界面中，可以模拟网页在各种移动设备下的显示效果：

当然电脑上模拟的和手机上实际显示的效果，还是会有一些细节差异的。

## 定义表单

定义表单


**定义表单**

使用WeUI定义表单的语法很简单：

AddForm(ParentID, ID, Action)
AddForm(ParentID, ID, Action, Method)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可 |
| ID | 表单ID |
| Action | 接收表单数据的网页。 |
| Method | 可选参数，指定表单提交方式，默认为"post" |

示例

将HttpRequest事件代码设置为：

Select
Case e.Path
    Case "test.htm"
        Dim wb
As New
weui
'定义一个基于weui框架的网页生成器
        wb.AddForm("","form1","accept.htm")
        e.WriteString(wb.Build) '生成网页
End Select

表示新增一个表单，表单的名称为form1，接收数据的网页为"accpet.htm"

## 定义按钮

定义按钮


**定义按钮**

在WeUI定义按钮之前，首先要定义一个按钮分组，定义按钮分组的语法为：

AddButtonGroup(ParentID, ID)
AddButtonGroup(ParentID, ID, Vertical)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可 |
| ID | 按钮分组ID |
| Vertical | 可选参数，逻辑型，按钮是否垂直排列，默认为True。 |

添加按钮的语法为：

Add(ID, Text)
Add(ID, Text, Type)
Add(ID, Text, Type, Href)

|  |  |
| --- | --- |
| ID | 按钮ID |
| Text | 按钮标题 |
| Type | 可选参数，字符型，用于指定按钮类型，可用值有"submit"、"reset"、"button" |
| Href | 可选参数，字符型，指定单击按钮之后跳转的目标网页的URL |

按钮有两个属性，分别为：

|  |  |
| --- | --- |
| Kind | 用于设置按钮的颜色，默认为0，表示绿色，1表示灰色，2表示红色 |
| Value | 用于设置按钮的值， |

**示例**

将HttpRequest事件代码设置为：
Select
Case e.Path
    Case "test.htm"
        Dim wb
As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddButtonGroup("form1","btg1",True)
'垂直排列
            .Add("btn1",
"按钮")
            .Add("btn4",
"按钮",
"reset")
            .Add("btn5",
"按钮",
"", "http://www.foxtable.com")
'单击这个按钮可以打开foxtable主页
        End With
        With wb.AddButtonGroup("form1","btg2",
False)
'水平排列
            .Add("btn6",
"按钮")
            .Add("btn7",
"按钮").Kind
= 2
        End With
        With wb.AddButtonGroup("form1","btg3",
False)
            .Add("btn8",
"按钮").Kind
= 0
            .Add("btn9",
"按钮").Kind
= 1

End
With
        e.WriteString(wb.Build)
'生成网页
End
Select

现在通过手机访问，可以看到下图所示的网页：

## 文本输入框

文本输入框


**文本输入框**

在定义输入框之前，首先你得定义一个输入框组(InputGroup)，定义输入框组的语法为：

AddInputGroup(ParentID, ID)
AddInputGroup(ParentID, ID, Text)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | 分组ID。 |
| Text | 可选参数，用于指定分组标题。 |

增加文本输入框的语法为：

AddInput(ID, Label, type)

|  |  |
| --- | --- |
| ID | 输入框ID,注意生成网页时，WeUI会自动将所有ID转换为小写，例如"Table1"或转换为"table1"，今后不再重复提示，大家请自行留意。 |
| Label | 在输入框左侧显示的标签内容 |
| Type | 输入框类型，普通文本输入框设置为"text"，密码输入框设置为"password" |

通过AddInput，还可以增加[日期输入框](0046.htm)和[数值输入框](0046.htm)。

**示例**

将HttpRequest事件代码设置为：

Select
Case e.Path
    Case "test.htm"
        Dim wb
As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","登录")
            .AddInput("xm","户名","text")
            .AddInput("pw","密码","password")
        End With
        With wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定", "submit")
        End With
        e.WriteString(wb.Build)
'生成网页
End
Select

现在通过手机访问，可以看到下图所示的网页：

**属性**

Foxtable为输入框提供了以下属性：

|  |  |
| --- | --- |
| Value | 字符型，输入框的初始值 |
| Readonly | 逻辑型，输入框是否只读 |
| Post | 逻辑型，提示表单数据时是否包括此输入框的值，默认为True。 |
| Required | 逻辑型，是否必须输入内容，目前基于iOS的多数浏览器暂不支持这个属性。 |
| Placeholder | 字符型，对输入框预期值的提示 |

将HttpRequest事件代码设置为：

Select
Case e.Path
    Case "test.htm"
        Dim wb
As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","登录")
            With .AddInput("xm","户名","text")
                .Value =
"张三"
                .Readonly=
True
            End With
            .AddInput("xm","密码","password").Placeholder
=  "请输入6位数密码"
        End With
        With wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With

e.WriteString(wb.Build)
'生成网页
End
Select

现在通过手机访问，可以看到下图所示的网页
，其中户名输入框是只读的：

## 日期输入框

日期输入框


**日期输入框**

和文本输入框一样，日期输入框也必须添加在输入框组中。

在输入框组增加一个日期输入框的语法为：

AddInput(ID, Label, type)

|  |  |
| --- | --- |
| ID | 输入框ID。 |
| Label | 在输入框左侧显示的标签内容 |
| Type | 输入框类型，普通日期设置为"date"， 只有时间设置为"time"，同时有日期时间设置为"datetime-local" |

**示例**

将HttpRequest事件代码设置为：

Select
Case e.Path
    Case "test.htm"
        Dim wb
As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","日期输入")
            .AddInput("rq","日期","date")
            .AddInput("sh","时间","time")
            .AddInput("rs","日期时间","datetime-local")
        End With
        With wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With

e.WriteString(wb.Build)
'生成网页
End
Select

下图是通过iPhone访问的截屏：

**属性**

日期输入框有以下属性：

|  |  |
| --- | --- |
| Value | 字符型，输入框的初始值。 |
| Readonly | 逻辑型，输入框是否只读。 |
| Required | 逻辑型，是否必须输入内容，目前基于iOS的多数浏览器暂不支持这个属性。 |
| Post | 逻辑型，提示表单数据时是否包括此输入框的值，默认为True。 |
| Min | 字符型，设置允许输入的最小值，目前基于iOS的多数浏览器暂不支持这个属性。 |
| Max | 字符型，设置允许输入的最大值，目前基于iOS的多数浏览器暂不支持这个属性。 |

例如下面的HttpRequest事件代码设置了日期输入框的一些属性：

Select
Case e.Path
    Case "test.htm"
        Dim wb
As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","时间输入")
            .AddInput("xm","日期","date").Value
= Format(Date.Today,"yyyy-MM-dd")
            With .AddInput("xm","时间","time")
                .value =
Format(Date.Now,"HH:mm")
                .Min
= "08:00"
'输入的事件必须在8:00到12:00之间
                .Max =
"12:00"
            End With
            With .AddInput("xm","日期时间","datetime-local")
                .Value =
Format(Date.Now,"yyyy-MM-ddTHH:mm")
'留意一下这个格式,日期和时间之间用字母T隔开

.Readonly =
True
            End
With
        End With
        With wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With

e.WriteString(wb.Build)
'生成网页
End
Select

Max和Min属性在iPhone上无效，在安卓和Windows系统下有效，这是我在Windows中用Chorme模拟手机访问的效果：

## 数值输入框

数值输入框


**数值输入框**

和文本输入框一样，数值输入框也必须添加在输入框组中。

在输入框组增加一个数值输入框的语法为：

AddInput(ID, Label, type)

|  |  |
| --- | --- |
| ID | 输入框ID。 |
| Label | 在输入框左侧显示的标签内容 |
| Type | 输入框类型，对于数值输入框，这个参数必须设置为"number" |

数值输入框有以下属性：

|  |  |
| --- | --- |
| Value | 字符型，输入框的初始值。 |
| Step | 字符型，指定输入精度，数值输入框默认只能输入整数，Step属性设置为"0.1"，可以输入一位小数，设置为"0.01"可以输入两位小数，依次类推。 |
| Post | 逻辑型，提示表单数据时是否包括此输入框的值，默认为True。 |
| Min | 字符型，设置允许输入的最小值，目前基于iOS的多数浏览器暂不支持这个属性。 |
| Max | 字符型，设置允许输入的最大值，目前基于iOS的多数浏览器暂不支持这个属性。 |
| Required | 逻辑型，是否必须输入内容，目前基于iOS的多数浏览器暂不支持这个属性。 |
| Readonly | 逻辑型，输入框是否只读。 |
| Placeholder | 字符型，对输入框预期值的提示。 |

**示例**

将HttpRequest事件代码设置为：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","数值输入")
            .AddInput("xm","姓名","text")
            With .AddInput("sl","年龄","number")
                .Min =
"18"
                .Max =
"60"
                .Placeholder =
"年龄范围为18到60"
            End With
            .AddInput("dj","工资","number").Step
= "0.01"
        End With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With

e.WriteString(wb.Build)
'生成网页
End
Select

现在通过手机访问，可以看到下图所示的网页
，其中年龄只能输入整数，工资可以输入两位小数：

## 列表输入框

列表输入框


**列表输入框**

和文本输入框一样，列表输入框也必须添加在输入框组中。

在输入框组增加一个列表输入框的语法为：

AddSelect(ID, Label, Values)

|  |  |
| --- | --- |
| ID | 输入框ID。 |
| Label | 在输入框左侧显示的标签内容 |
| Values | 列表项目，用符号"|"隔开，例如"大专|本科|硕士|博士"。  打开网页后，默认会选择第一个值，如果要将其他位置的值作为默认值，可以将其用方括号括起来，例如"大专|[本科]|硕士|博士"，打开网页后，会自动选择本科。 |

列表输入框有以下属性：

|  |  |
| --- | --- |
| Post | 逻辑型，提示表单数据时是否包括此输入框的值，默认为True。 |
| Required | 逻辑型，是否必须输入内容，目前基于iOS的多数浏览器暂不支持这个属性。 |

**示例**

将HttpRequest事件代码设置为：

Select Case
e.Path
    Case "test.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","列表项目")
            .AddSelect("os","操作系统","iOS|Windows|Andriod")
            .AddSelect("bw","浏览器","Chorme|[Edge]|Firefox|Internet
Explorer")
        End With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定", "submit")
        End With
        e.WriteString(wb.Build)
'生成网页
End
Select

下图是通过iPhone访问时的截屏:

## 使用InputCell

使用InputCell


**使用InputCell**

我们之前定义的各种输入框，其实都是放在输入格中的，每个输入格被分成两部分，左边显示标签，右边显示输入框。
通过InputCell，我们可以对格子进行更多的控制。

**一个例子**

我们先用一个例子说明如何使用InputCell。
在运行这个例子之前，先下载下面的图片到"d:\web\images"目录中，名称为"vcode.jpg"：

HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim wb
As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","基本资料")
            .AddInput("xm","姓名","text")
'常规语法增加输入框
            With .AddInputCell("ic1")
'通过InputCell增加输入框
                .AddLabel("lnl","年龄",0)
'增加标签,0显示在左边
                .AddInput("nl","number",1)
'增加输入框,1表示显示在中间
            End With
            With .AddInputCell("ic2",1)
'通过InputCell增加输入框,1表示突出显示
                .AddLabel("lkh","卡号",0)
'增加标签,0显示在左边
                .AddInput("kh","number",1).PlaceHolder=
"请输入卡号"
'增加输入框,1表示显示在中间
            End With
            With .AddInputCell("ic3",2)
'通过InputCell增加输入框,
2表示突出显示(含图标)
                .AddLabel("lmm","密码",0)
'增加标签,0显示在左边
                .AddInput("mm","text",1).PlaceHolder=
"请输入密码"
'增加输入框,1表示显示在中间
            End With
            With .AddInputCell("ic4")
'通过InputCell增加输入框
                .AddLabel("lsj","手机",0)
'增加标签,0显示在左边
                .AddInput("sj","text",1)
'增加输入框,1表示显示在中间
                .AddVcodeButton("hym","获取验证码",2)
'增加获取验证码按钮,2表示显示在右边
            End
With
            With .AddInputCell("ic5")
'通过InputCell增加输入框
                .AddLabel("lyzm","验证码",0)
'增加标签,0显示在左边
                .AddInput("yzm","text",1)
'增加输入框,1表示显示在中间
                .AddImage("pim",".\images\vcode.jpg",2)
'增加一个图片,2比表示显示在右边
            End
With
            With .AddInputCell("ic6")
'通过InputCell增加输入框
                .AddSelect("zn","+86|+87|+88|+89",0)
'增加下拉列表,0表示显示在左边
                .AddInput("dh","text",1).PlaceHolder
= "请输入联系电话"
'增加输入框,1表示显示在中间
            End
With
        End With
        e.WriteString(wb.Build)
'生成网页
End
Select

下图是是通过手机访问的显示效果：

上面的例子基本涵盖了InputCell的全部用法。

增加InputCell的语法很简单：

AddInputCell(ID)
AddInputCell(ID，Warn)

|  |  |
| --- | --- |
| ID | InputCell的ID |
| Warn | 可选参数，设为1左边标签会套红显示，设为2右边还会显示一个红色警示图标。 |

**AddLabel**

InputCell中通过AddLabel方法增加标签，语法为：

AddLabel(ID, Text,
Position)

|  |  |
| --- | --- |
| ID | 标签ID |
| Text | 标签内容 |
| Position | 标签位置，0靠左显示，1居中显示，2靠右显示 |

AddInput

InputCell通过AddInput方法增加输入框，语法：

AddInput(ID, Type,
Position)

|  |  |
| --- | --- |
| ID | 输入框ID |
| Type | 输入框类型，可选值有：  |  |  | | --- | --- | | text | 文本输入框，参考：[文本输入框](0045.htm) | | password | 密码输入框，参考：[文本输入框](0045.htm) | | date | 日期输入框，参考：[日期时间输入框](0046.htm) | | time | 时间输入框，参考：[日期时间输入框](0046.htm) | | datetime-local | 日期时间输入框，参考：[日期时间输入框](0046.htm) | | number | 数值输入框，参考：[数值输入框](0047.htm) | |
| Position | 输入框位置，0靠左显示，1居中显示，2靠右显示 |

**AddSelect**

InputCell通过AddSelect方法增加[列表输入框](0048.htm)，语法：

AddSelect(ID,
Values, Position)

|  |  |
| --- | --- |
| ID | 列表输入框ID。 |
| Values | 列表项目，用符号"|"隔开，例如"大专|本科|硕士|博士"。 |
| Position | 标签位置，0靠左显示，1居中显示，2靠右显示 |

AddVcodeButton

InputCell通过AddVcodeButton方法增加类似"获取验证码"的按钮，语法：

AddVcodeButton(ID,
Text, Position)

|  |  |
| --- | --- |
| ID | 按钮ID |
| Text | 按钮标题。 |
| Position | 按钮位置，0靠左显示，1居中显示，2靠右显示 |

AddImage

InputCell通过AddImage方法增加图片，语法：

AddImage(ID, File,
Postion)

|  |  |
| --- | --- |
| ID | 图片ID |
| File | 图片文件，包括路径。 |
| Position | 图片位置，0靠左显示，1居中显示，2靠右显示 |

## 逻辑开关

逻辑开关


**逻辑开关**

逻辑开关（Switch）类似复选框(CheckBox)，但视觉效果更好。
逻辑开关必须添加在输入框组中。

在输入框组中添加逻辑开关的语法是：

AddSwtich(ID, Label)
AddSwtich(ID, Label, Checked)

|  |  |
| --- | --- |
| ID | 开关ID。 |
| Label | 在开关左侧显示的标签内容 |
| Checked | 逻辑型，可选参数，开关默认是否处于开启状态。 |

开关的属性有：

|  |  |
| --- | --- |
| Value | 字符型，开关开启后提交端到服务端的值，如果不设置，将传递"on"值给服务端。 |
| Post | 逻辑型，提示表单数据时是否包括此开发的值，默认为True。 |
| Enabled | 逻辑型，设置为False，将无法改变开关状态。 |

**示例**

将HttpRequest事件代码设置为：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","增加客户")
            .AddInput("xm","姓名","text")
            .AddInput("nl","年龄","number")
            .AddSwitch("hy","会员",True)
            .AddSwitch("vip","VIP客户")
        End With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
        e.WriteString(wb.Build)
'生成网页
End
Select

现在通过手机访问，可以看到下图所示的网页：

## 多行文本框

多行文本框


**多行文本框**

和文本输入框一样，多行文本框也必须添加在输入框组中。

在输入框组增加一个多行文本框的语法为：

AddTextArea(ID)
AddTextArea(ID，Rows)

|  |  |
| --- | --- |
| ID | 输入框ID。 |
| Rows | 整数型，可选参数，用于设置行数，默认为3行。 |

Foxtable为多行输入框提供了以下属性：

|  |  |
| --- | --- |
| Value | 字符型，输入框的初始值。 |
| Readonly | 逻辑型，输入框是否只读。 |
| Required | 逻辑型，是否必须输入内容，目前基于iOS的多数浏览器暂不支持这个属性。 |
| Post | 逻辑型，提示表单数据时是否包括此输入框的值，默认为True。 |
| Placeholder | 字符型，对输入框预期值的提示。 |

**示例**

将HttpRequest事件代码设置为：

Select
Case e.Path
    Case "test.htm"
        Dim wb
As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","基本资料")
            .AddInput("xm","姓名","text")
            .AddInput("nl","年龄","number")
            .AddInput("rq","日期","date")
            .AddSwitch("vip","VIP客户")
        End With
        With wb.AddInputGroup("form1","ipg2","备注")
            .AddTextArea("bz",5).Placeholder
= "请输入200字以内的备注"
        End With
        With wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")

End
With
        e.WriteString(wb.Build)
'生成网页
End
Select

下图是在手机上的显示效果：

## 单选列表项

单选列表项


**单选列表项**

要使用单选列表项，首先得定义一个单选列表组，定义单选列表组的语法是：

AddRadioGroup(ParentID, ID)
AddRadioGroup(ParentID, ID, Text)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | 分组ID。 |
| Text | 可选参数，用于指定分组标题。 |

增加单选列表项的语法是：

Add(ID, Text)
Add(ID, Text, Checked)

|  |  |
| --- | --- |
| ID | 列表项ID。 |
| Text | 单选列表项的文本内容 |
| Checked | 逻辑型，可选参数，单选列表项默认是否勾选。 |

单选列表项的属性有：

|  |  |
| --- | --- |
| Value | 字符型，勾选后传递给服务端的值，如果不设置，将传递ID值给服务端。 |
| Enabld | 逻辑型，设置为False，将无法勾选此列表项。 |

**示例**

HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim wb
As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddRadioGroup("form1","rdg1","浏览器")
            .Add("bw1","Intenet
Explorer")

            .Add("bw2","Google
Chorme", True)
'默认勾选
            .Add("bm3","FireFox")
            .Add("bm4","Safari").Enabled
= False '此项不可选
        End With
        With wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定", "submit")
        End With
        e.WriteString(wb.Build)
'生成网页
End
Select

下图是在手机上的显示效果：

## 复选列表项

复选列表项


**复选列表项**

要使用复选列表项，首先得定义一个复选列表组，定义复选列表组的语法是：

AddCheckGroup(ParentID, ID)
AddCheckGroup(ParentID, ID, Text)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | 分组ID。 |
| Text | 可选参数，用于指定分组标题。 |

增加复选列表项的语法是：

Add(ID, Text)
Add(ID, Text, Checked)

|  |  |
| --- | --- |
| ID | 列表项ID。 |
| Text | 复选列表项的文本内容。 |
| Checked | 逻辑型，可选参数，复选列表项默认是否勾选。 |

复选列表项的属性有：

|  |  |
| --- | --- |
| Value | 字符型，勾选后传递给服务端的值，如果不设置，将传递"on"值给服务端。 |
| Enabld | 逻辑型，设置为False，将无法勾选此列表项。 |

**示例**

HttpRequest事件代码：

Select
Case e.Path
    Case
"test.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddCheckGroup("form1","rdg1","浏览器")
            .Add("bw1","Intenet
Explorer", True)
'默认勾选
            .Add("bw2","Google
Chorme")
            .Add("bm3","FireFox")
            .Add("bm4","Safari").Enabled
= False '此项不可选
        End With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
        e.WriteString(wb.Build)
'生成网页
End
Select

下图是在手机上的显示效果：

## 接收表单数据

接收表单数据


**接收表单数据**

我们已经介绍完毕WeUI框架中基本的表单输入元素。

现在我们用一个例子来演示如何在服务端接收用户通过表单输入的数据。

以下是HttpRequest事件代码，为了方便，我们首次采用中文作为输入元素的ID:

Select
Case e.Path
    Case "test.htm"
        If e.PostValues.count
= 0 Then
            Dim
wb As
New weui
            wb.AddForm("","form1","test.htm")
            With wb.AddInputGroup("form1","ipg1","客户资料")
                .AddInput("姓名","姓名","Text")
'前一个"姓名"是ID,后一个"姓名"是标题
                .AddInput("年龄","年龄","number")
                .AddInput("日期","日期","date")
                .AddSelect("级别","级别","普通会员|高级会员|VIP会员")
                .AddSwitch("停权","停权")
            End With
            With
wb.AddRadioGroup("form1","学历","学历")
                .Add("本科","本科")
                .Add("硕士","硕士")
                .Add("博士","博士")
            End With
            With
wb.AddCheckGroup("form1","偏好","品牌偏好")
                .Add("苹果","苹果")
                .Add("华为","华为")

.Add("三星","三星")
            End With
            With
wb.AddButtonGroup("form1","btg1",True)
                .Add("btn1",
"确定",
"submit")
            End With
            e.WriteString(wb.Build)
'生成网页
        Else
            Dim
sb As
New StringBuilder
            sb.AppendLine("<meta
name='viewport' content='width=device-width,initial-scale=1,user-scalable=0'>")
            sb.AppendLine("接收到的数据有:<br/><br/>")
            For Each
key As
String In
e.PostValues.Keys
                sb.AppendLine(key
& ":"
& e.PostValues(key)
& "<br/>")
            Next
            e.WriteString(sb.ToString)

End
If
End
Select

在浏览器中按下图所示输入数据：

单击确定按钮，浏览器会显示服务端接收到的数据：

框架表单和我们在快速入门中介绍的常规表单，基本上是一样的，只需留意一下：

1、单选列表项在勾选状态下，传递到服务器的值是其ID，你可以通过Value属性设置你希望传递给服务器的值。

2、每个单选列表项组只能勾选一项，服务端收到的键是**组**的ID值，值为**勾选项**的ID值或其Value属性值。

3、复选列表项组中的每一项，只要被勾选了，都会独立向服务端传递值，键为勾选项的ID值，值为"on"。

3、开关组件本质上就是复选列表项，所以开关在开启后，提交给服务端的值也是"on"。

4、开关组件和复选列表项都有Value属性，用于设置在勾选(开启)后，提交给服务器的值。

5、没有输入内容的输入框，没有勾选项目的单选或复选列表项组，都不会向服务端传递值。

## Class和Attribute

Class和Attribute


**Class和Attribute**

所谓通过WeUI自动生成的网页，其实就是自动生成各种HTML元素。

各种HTML元素可定义的属性是很多的，但是Foxtable通过WeUI组件提供的可直接设置的属性却不多。

不过Foxtable为所有WeUI组件都提供了Class和Attribute属性，前者用于设置HTML元素的Class属性，后者用于设置HTML元素除Class之外的所有属性。

**示例**

将HttpRequest事件代码设置为：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddButtonGroup("form1","btngrp1")
            With .Add("btn1","单击我","button")
                .Class =
"btnClass"

.Attribute
= "style='font-style:italic;font-weight:900;' onclick='location=""http://www.foxtable.com""'"
            End
With
        End
With
        e.WriteString(wb.Build)
End
Select

上面的代码通过Class属性给按钮添加了一个新类"btnClass"。

并通过Attribute属性完成了两项设置：

1、按钮的字体为斜体加粗：

2、单击按钮跳转到Foxtable主页。

如果通过浏览器查看生成的HTML源代码，可以看到生成的按钮的代码是:

<button id='btn1' name='btn1' type='button' class='weui\_btn weui\_btn\_primary
btnClass' style='font-style:italic;font-weight:900;' onclick='location="http://www.foxtable.com"'>单击我</button>

## 再谈按钮类型

再谈按钮类型


再谈按钮类型

现在我们有必要回头看看按钮的类型(Type)，我们知道添加按钮的语法是：

Add(ID, Text)
Add(ID, Text, Type)
Add(ID, Text, Type, Href)

|  |  |
| --- | --- |
| ID | 按钮ID |
| Text | 按钮标题 |
| Type | 可选参数，字符型，用于指定按钮类型，可用值有"submit"、"reset"、"button" |
| Href | 可选参数，字符型，指定单击按钮之后跳转的目标网页的URL |

按钮的类型由第三个参数决定，默认就是"submit"。

一般来说提交按钮的type参数设置为"submit"或者不设置；重置按钮的type参数设置为"reset"；超链接按钮不要设置type参数，设置href参数即可；自定义按钮(单击执行代码)的type参数设置为"button"。

例如：

Select
Case e.Path
    Case "test.htm"
        If e.PostValues.Count
= 0 Then
            Dim
wb As
New weui
            wb.AddForm("","form1","test.htm")
            With wb.AddInputGroup("form1","ipg1","登录")
                .AddInput("姓名","户名","text")
                .AddInput("密码","密码","password")
            End With
            With
wb.AddButtonGroup("form1","btngrp1",False)
                .Add("btn1",
"确定",
"submit")
'提交
                .Add("btn2",
"重置",
"reset")
'重置
                With .Add("btn3",
"自定义",
"button")
'自定义按钮
                    .Attribute =
"onclick=""confirm('你喜欢foxtable吗?')"""
                End
With
                .Add("btn4",
"主页",
"", "http://www.foxtable.com")
'超链接
            End With
            e.WriteString(wb.Build)
        Else
            Dim
sb As
New StringBuilder
            sb.AppendLine("<meta
name='viewport' content='width=device-width,initial-scale=1,user-scalable=0'>")
            sb.AppendLine("接收到的数据有:<br/><br/>")
            For Each
key As
String In
e.PostValues.Keys
                sb.AppendLine(key
& ":"
& e.PostValues(key)
& "<br/>")
            Next
            e.WriteString(sb.ToString)

End
If
End
Select

这是在手机上的访问效果，您可以分别单击这些按钮，看看有什么不同：

## 使用MsgPage

使用MsgPage


**使用MsgPage**

结果页(MsgPage)通常在一系列操作后显示，用于告知用户操作结果以及一些必要的细节。

添加MsgPage的语法是：

AddMsgPage(ParentID, ID, Title, Content)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | MsgPage的ID。 |
| Title | 内容标题 |
| Content | 内容详情 |

MsgPage的方法有：

**AddButton**

用于添加按钮，语法：

AddButton(ID, Text)
AddButton(ID, Text, Href)

|  |  |
| --- | --- |
| ID | 按钮ID |
| Text | 按钮标题 |
| Href | 可选参数，字符型，指定单击按钮之后跳转的目标网页的URL |

**AddExtra**

用于添加要在页面底部显示的内容，语法：

AddExtra(text)
AddExtra(text, href)

|  |  |
| --- | --- |
| Text | 内容 |
| href | 可选参数，指定单击底部内容后跳转的目标网页地址。 |

MsgPage的属性有：

|  |  |
| --- | --- |
| Icon | 字符型：指定显示的图标，可选值有"success","info","warn",对应的图标分别是：   默认为"success" |

**示例**

HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim wb
As new
WeUI
        With wb.AddMsgPage("","msgpage","操作完成","内容详情,可根据实际需要安排")
            .AddButton("btn1","确定")
            .AddButton("btn2","取消").kind
= 1
            .AddExtra("详细信息","http://www.foxtable.com/")

End
With
        e.WriteString(wb.Build)
'生成网页
End
Select

下图是通过iPhone访问该页面的显示效果：

## 一个录入界面

一个简单录入界面


**一个简单录入界面**

假定有下图所示的一个表：

希望设计一个手机录入界面：

在输入数据，单击确定按钮，能提示下图所示的页面：

如果有些关键列内容没有输入，则提示下图所示页面：

下面是HttpRequest事件代码，这段代码完成了HTTP服务的建立，3个页面的生成，以及数据接收等任务：

Dim
wb As
New
weui
Select
Case e.Path
    Case "addnew.htm"
        If e.PostValues.Count
= 0 Then
            wb.AddForm("","form1","addnew.htm")
            With wb.AddInputGroup("form1","ipg1","客户资料")
                .AddInput("姓名","姓名","Text")
'前一个"姓名"是ID,后一个"姓名"是标题
                .AddInput("年龄","年龄","number")
                .AddInput("日期","日期","date")
                .AddSelect("级别","级别","普通会员|高级会员|VIP会员")
                .AddSwitch("停权","停权").Value
= "True"
            End
With
            With
wb.AddRadioGroup("form1","学历","最高学历")
                .Add("本科","本科")
                .Add("硕士","硕士")
                .Add("博士","博士")
            End With
            With
wb.AddCheckGroup("form1","偏好","品牌偏好")

 .Add("苹果","苹果")
                .Add("华为","华为")

.Add("三星","三星")
            End With
            With
wb.AddButtonGroup("form1","btg1",True)
                .Add("btn1",
"确定",
"submit")
            End With
            e.WriteString(wb.Build)
        Else
            Dim
nms() As
String =  {"姓名","年龄","日期","级别"}
'不能为空的列名数组



            For Each nm As String In nms


If
e.PostValues.ContainsKey(nm)
= False Then
'生成错误提示页
                    With
wb.AddMsgPage("","msgpage","增加失败",
nm &
"列不能为空!")
                        .icon =
"Warn" '改变图标
                        .AddButton("btn1","返回").Attribute
= "onclick='history.back()'"
                    End
With
                    e.WriteString(wb.Build)
                    Return
'必须返回
                End
If
            Next
            nms =
New String()
{"姓名","年龄","日期","级别","停权","学历"}
'重新定义了nms数组,增加了两列.

            Dim
dr
As
DataRow =
DataTables("员工").AddNew()
            For Each
nm As
String In
nms
                If
e.PostValues.ContainsKey(nm)
Then
                    dr(nm)
= e.PostValues(nm)
                End If
            Next
            '以下代码处理品牌复选列表项
            Dim
pp As String
            nms =
New String()
{"苹果","华为","三星"}
'将nms重新定义为品牌数组



For Each

nm

As
String

In

nms
                If e.PostValues.ContainsKey(nm)
AndAlso e.PostValues(nm).Trim()
= "on" Then
'不能省略Trim

                    pp =
pp &
nm  &
","
                End
If
            Next
            If
pp > "" Then
                dr("偏好")
= pp.Trim(",")
            End If

'保存并生成增加成功提示页面
            dr.save()
            With wb.AddMsgPage("","msgpage","增加成功",
"好好学习,天天向上")
'生成成功提示页



 .AddButton("btn1","继续增加","addnew.htm")

            End With
            e.WriteString(wb.Build)
        End
 If
End
Select

代码很好理解，以下几点注意一下：

1、输入组件的ID尽量用列名，方便简化编码。
2、对于开关组件，默认返回值是"on"，可以将其Value属性设置为"True"，方便统一编码。
3、开关组件和复选列表项的返回值可能有空格，例如"on  "，所以比较值的时候要用Trim方法去掉空格。

## 引用外部文件

引用外部文件


**引用外部文件**

Foxtable为WeUI提供了一个AppendHTML方法，用于添加原生的HTML代码。

语法：

AppendHTML(HTML，Head)

|  |  |
| --- | --- |
| HTML | 字符型，HTML代码。 |
| Head | 字符型，设置为True，代码添加在网页的Head区，否则添加在网页的Body区，默认为False。 |

很少用这个方法生成可视的HTML元素，通常用来添加第三方库文件，如CSS或JavaScript文件，或动态合成JavaScript代码。

**引用外部文件**

假定有下图所示的一个手机录入界面，希望录入单价、折扣和数量后，能自动计算出金额
，而且当金额超过30000时，字体颜色自动变为红色：

**设计步骤**

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"mark.css"，文件内容为：

input.mark{color:red;}

再另外建立一个文本文件，文件名为"calc.js"，文件内容为：

function markCalc(){
    je.value=dj.value \* sl.value \* (1 - zk.value);
    if(je.value >= 30000){
        if(!je.classList.contains('mark')){

je.classList.add('mark');
        }
    }
    else{
        if(je.classList.contains('mark')){

je.classList.remove('mark');
        }
    }
}

提示：

dj.value表示id为"dj"的输入框框的值，需要注意的时候，WeUI在生成网页时，会自动将所有id转换为小写，所以即使你在HttpRequest事件中设置的id是大写的"DJ"，在js代码中依然应用用小写的"dj"。

2、将HttpRequest事件代码设置为：

Select
Case e.Path
    Case "addnew.htm"
        Dim wb
As New
weui
        wb.AppendHTML("<link
rel='stylesheet' href='./lib/mark.css'/>",True)
'引入样式文件,参数True表示添加到head区
        wb.AddForm("","form1","addnew.htm")
        With wb.AddInputGroup("form1","ipg1","新增订单")
            .AddInput("cp","产品","text")
            .AddInput("gy","雇员","text")
            .AddInput("kh","客户","text")
            .AddInput("dj","单价","number").Attribute
= "step='0.1' onchange='markCalc()'"
'事件调用
            .AddInput("zk","折扣","number").Attribute
= "step='0.01' onchange='markCalc()'"
            .AddInput("sl","数量","number").Attribute
= "onchange='markCalc()'"
            .AddInput("je","金额","number")
            .AddInput("rq","日期","date")
        End With
        With wb.AddButtonGroup("form1","btg1",True)
            .Add("btnok","确定")
        End With
        wb.AppendHTML("<script
src='./lib/calc.js'></script>")
'引入脚本文件
        e.WriteString(wb.Build)
End
Select

**再谈Attribute属性**

这里特意通过Attribute来设置step属性。

Attribute可以用一行代码集中设置各种属性，例如下面的代码设置折扣的输入精度为0.01，最小值为0，最大值为0.15，值发生变化后调用calc函数。

.AddInput("zk","折扣","number").Attribute
= "step='0.01' min='0' max='0.15' onchange='calc()'"

遗憾的是，精度、最大值和最小值属性在iOS平台的设备上是无效的。

## InsertHTML

InsertHTML


**InsertHTML**

之前介绍的AppendHTML，用于在Head区或Body区的结束位置追加代HTML代码。

如果需要在当前位置插入HTML代码，请使用InsertHTML，语法：

InsertHTML(Content)
InsertHTML(ParentId,Content)

Content:  要插入的内容。
ParentId: 父容器ID，如果是顶层对象，可以不设置。

**一个例子**

HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
WeUI
        wb.InsertHTML("<h3
align='center' style='margin-top:5px'>用户登录</h3>")
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1")
            .Attribute =
"style='margin-top:5px'"
            .AddInput("xm","户名","text")
            .AddInput("pw","密码","password")
        End With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
        e.WriteString(wb.Build)
End
Select

下图是通过手机访问的效果，标题“用户登录”四个字是通过InsertHTML方法插入的：

## 插入标记数据

插入标记数据


**插入标记数据**

我们在生成表单的时候，可能需要在表单插入一些标记数据。

例如你需要根据现有订单来生成一个表单，那么就需要在生成的表单中存储主键值，这样用户编辑完成，将编辑结果提交到后台时，Foxtable才能知道用户编辑的是哪一个订单。

我们可使用AddHiddenValue方法，在输入框组插入隐藏的标记数据，语法为：

AddHiddenValue(ID,Value)

ID：    ID值
Value： 值

用户提交表单时，隐藏数据将随表单数据一起被提交到服务器。

**一个例子**

HttpRequest事件代码：

Dim
wb As
New
weui
Select
Case e.Path
    Case "test.htm"
        If e.PostValues.count
= 0 Then
            wb.AddForm("","form1","test.htm")
            With wb.AddInputGroup("form1","ipg1","订单编辑")
                .AddHiddenValue("订单编号","123")
                .AddInput("客户","客户","text")
                .AddInput("产品","产品","text")
                .AddInput("数量","数量","number")
                .AddInput("单价","单价","number").Step=
"0.01"
            End
With
            With
wb.AddButtonGroup("form1","btg1",True)
                .Add("btn1",
"确定",
"submit")
            End With
        Else
            wb.InsertHTML("接收到的数据有:<br/>")
            For Each
key As
String In
e.PostValues.Keys
                wb.InsertHTML(key
& ":"
& e.PostValues(key)
& "<br/>")

Next
        End
If
End
Select
e.WriteString(wb.Build)
'生成网页

用户在表单中输入数据：

单击提交按钮，可以看到，提交的数据包括隐藏的订单编号：

## 动态列表项目之一

动态列表项目之一


**动态列表项目之一**

掌握了JavaScript，可以给网页增加很多动态效果，例如最常见的动态列表项目。

**一个例子**

如下图所示的录入界面，希望选择不同国家后，能自动列出该国家的汽车品牌供选择：

**设计步骤：**

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"brands.js"，文件内容为：

function setBrands(){
var gj=document.getElementById("国家").value;
if(gj=="中国")setOptions("品牌","比亚迪|奇瑞|长城|荣威|吉利");
else
if(gj=="德国")setOptions("品牌","奔驰|宝马|奥迪|大众|欧宝");
else
if(gj=="日本")setOptions("品牌","丰田|本田|日产|讴歌|雷克萨斯");
}

需要特别提醒的是:

a、因为有中文，请将这个文件保存为utf-8格式，如果你是用Windows自带的记事本编辑，第一次请不要直接保存，请单击文件菜单中的另存为命令，在对话框中将编码格式选择为"UTF-8"
b、setOptions不是原生的JavaScript函数，是为了方便大家，我们在weui.me.js中扩展的一个函数，用于设置列表项目，第一个参数为列表输入框的ID，第二个参数为列表项目。

2、HttpRequet事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim wb
As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","动态列表")
            .AddSelect("国家","国家","中国|德国|日本").Attribute
= "onchange='setBrands()'"
            .AddSelect("品牌","品牌","比亚迪|奇瑞|长城|荣威|吉利")
        End With
        With wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
        wb.AppendHTML("<script
src='./lib/brands.js'></script>")
'引入脚本文件
        e.WriteString(wb.Build)
'生成网页
End
Select

## 动态列表项目之二

动态列表项目之二


**动态列表项目之二**

上一节介绍的动态列表项目，其实是不够动态的，因为列表内容是固化在js代码文件中的，如果列表项目要根据后台数据库内容动态生成，显然这种方式是行不通的。

假定后台有个名为"汽车"的数据表：

前台的录入界面如下图，希望选择不同的国家后，能自动根据后台数据表的内容，列出该国的汽车品牌供选择：

**设计步骤**

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"brands.js"，文件内容为：

function getBrands(){
    var gj=document.getElementById("国家").value;
    setOptions("品牌",document.getElementById(gj).innerHTML);
}

2、HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim wb
As New
weui
        wb.AddForm("","form1","test.htm")
        Dim gjs
As List(of
String) = DataTables("汽车").GetValues("国家")
        With wb.AddInputGroup("form1","ipg1","动态列表")
            .AddSelect("国家","国家","|"
& String.Join("|",gjs.ToArray)).Attribute
= "onchange='getBrands()'"
 '调用js函数。
            .AddSelect("品牌","品牌","")
        End With
        With wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
        For Each
gj As
String In
gjs

'插入一些隐藏段落,用于存储各个国家的汽车品牌
            wb.InsertHTML("<p
hidden id='" &
gj & "'>"
& DataTables("汽车").GetComboListString("品牌","国家='"
& gj
& "'")
& "</p>")
        Next
        wb.AppendHTML("<script
src='./lib/brands.js'></script>") '引入脚本文件
        e.WriteString(wb.Build) '生成网页
End Select

设计的思路很简单，就是生成的网页中，插入一些隐藏的段落，段落id为国家名称，内容为该国家的汽车品牌：

<p hidden id='德国'>奥迪|宝马|奔驰|大众|欧宝</p>
<p hidden id='日本'>本田|丰田|雷克萨斯|讴歌|日产</p>
<p hidden id='中国'>比亚迪|长城|吉利|奇瑞|荣威</p>

当用户选择不同国家后，触发onchange事件，执行getBrand函数，自动找出对应的段落，从中提取出列表项目。

## 动态列表项目之三

动态列表项目之三


**动态列表项目之三**

前面介绍的动态列表项目方法，优势是响应快，因为运行过程不需要连接服务器。

但是如果数据量比较大，用这种方法是不合适的，所以我们还提供了在运行过程中连接服务器来动态生成列表项目的方法。

参考：[setAjaxOptions](0096.htm)

三种方法各有优势，根据需要选用即可。

## 区分多个提交按钮

区分多个提交按钮


**区分多个提交按钮**

同一个表单，可能需要多个提交按钮，服务端在接收表达数据后，根据用户单击不同的提交按钮，进行不同的后续操作。

服务端是如何区分不同的提交按钮呢？

方法一

最简单的方式是设置提交按钮的value属性，单击某个提交按钮，此按钮的Value属性值将作为表单数据的一部分提交到服务器。

方法二

另一中方法是设置提交按钮的FormAction属性，单击提交按钮后，数据将被提交到FormAction所制定的网页链接，这种方法的优势是可以通过get方式附加更多的数据。

**一个例子**

HttpRequest事件代码：

Dim
wb As
New weui
Select
Case e.Path
    Case
"input.htm"
        If e.PostValues.Count
= 0 Then
            wb.AddForm("","form1","input.htm")
            With wb.AddInputGroup("form1","ipg1","数据输入")
                .AddInput("客户","客户","text")
                .AddInput("日期","日期","date")
                .Addinput("产品","产品","text")
                .Addinput("数量","数量","number")
            End With
            With
wb.AddButtonGroup("form1","btngrp1",False)
                .Add("btn1",
"按钮1",
"submit").Value
= "btn1"
                .Add("btn2",
"按钮2",
"submit").Value
= "btn2"
                .Add("btn3",
"按钮3",
"submit").FormAction
= "accept.htm"
                .Add("btn4",
"按钮4",
"submit").FormAction
= "accept.htm?type=1&model=ha"
            End
With
        Else
            wb.InsertHTML("接收到的数据有:<br/>")
            For Each
key As
String In
e.PostValues.Keys
                wb.InsertHTML(key
& ":"
& e.PostValues(key)
& "<br/>")
            Next
        End If
    Case "accept.htm"
        wb.InsertHTML("通过accept.htm接收到的数据有:<br/>")
        For Each
key As
String In
e.PostValues.Keys
            wb.InsertHTML(key
& ":"
& e.PostValues(key)
& "<br/>")
        Next
End
Select
e.WriteString(wb.Build)

通过浏览器访问，可以看到四个提交按钮：

定义表单的代码为：

wb.AddForm("","form1","input.htm")

表示默认接收表单的目标网页为input.htm，单击按钮1和按钮2会将数据提交到这个页面。

由于我们给按钮1和按钮2设置了Value属性，服务端通过接收到的值，可以判断出用于单击的是那个按钮。

按钮3和按钮4通过FormAction属性，将数据接收页面改为accept.htm，不同的是按钮4还会通过get方式
附加了两个数据，这两个数据会随表单数据一并提交到服务器。。

下表分别单击四个按钮后的显示结果：

|  |  |
| --- | --- |
| 按钮1 | 接收到的数据有:   客户:CS01   日期:2016-11-30   产品:PD01   数量:100   btn1:btn1 |
| 按钮2 | 接收到的数据有:   客户:CS01   日期:2016-11-30   产品:PD01   数量:100   btn2:btn2 |
| 按钮3 | 通过accept.htm接收到的数据有:   客户:CS01   日期:2016-11-30   产品:PD01   数量:100 |
| 按钮4 | 通过accept.htm接收到的数据有:   type:1   model:ha   客户:CS01   日期:2016-11-30   产品:PD01   数量:100 提示：type和model两个值是通过get方式传递的。 |

## 使用Uploader


### 使用Uploader

使用Uploader


**使用Uploader**

Uploader用于上传文件，和其他数据输入组件一样，Uploader需要放在输入框分组中。

定义一个Uploader的语法是：

AddUploader(ID, Label, Multiple)

|  |  |
| --- | --- |
| ID | 组件ID |
| Text | 组件标题 |
| Multiple | 逻辑型，可选参数，手否允许选择多个文件上传。 |

上传组件可以浏览图片，通过AddImage添加要浏览的图片，语法：

AddImage(Image)
AddImage(Thumbnail, Image)

|  |  |
| --- | --- |
| Thumbnail | 缩略图文件。 |
| Image | 图片文件。 |

**示例**

在运行这个例子之前，请先复制几个图片到"d:\web\images目录"，文件名分别是"001.jpg"、"002.jpg"和"003.jpg"。

HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","文件上传")
'文件上传
            .AddUploader("up1","")
        End With
        With
wb.AddInputGroup("form1","ipg22","文件上传")
'带图片浏览的文件上传
            With .AddUploader("up2","图片",True)
'True表示允许一次上传多个文件
                .AddImage("./images/001.jpg")
                .AddImage("./images/002.jpg")
                .AddImage("./images/003.jpg")
            End With
        End
With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With


e.WriteString(wb.Build)
'生成网页
End Select

下图是在iPhone上的显示效果：

单击上图中的“+”按钮，可以拍照上传，或选择现有的照片上传：

### 改变标题位置

改变标题位置


**改变标题位置**

Uploader组件有个TextPosition属性，用于设置标题位置，0表示标题靠左，1表示标题靠上，默认为1。

HttpRequet事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","客户资料")
            .AddInput("姓名","姓名","Text").value
= "舒淇"
            .AddInput("年龄","年龄","number").Value
= "28"
            .AddInput("日期","日期","date").value
= #10/12/2012#
            With .AddUploader("up1","照片",True)
                .TextPosition =
0
'标题靠左
                .AddImage("./images/shuqi1.jpg")
                .AddImage("./images/shuqi2.jpg")
            End With
        End
With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With

e.WriteString(wb.Build)
'生成网页
End
Select

下图是通过手机访问的效果：

### 在微信浏览器中使用相机

在微信浏览器中使用相机


**在微信浏览器中使用相机**

如果你的手机是安卓系统，并且使用的是微信内置的浏览器浏览WeUI生成的网页，你会发现Uploader只能从相册中选择图片上传，无法使用相机拍照上传。

要解决这个问题很简单， 只需将Uploader的Accept属性设置为"image/\*"，例如：

Select
Case e.Path


Case "test.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg22","文件上传")
            With .AddUploader("up2","图片",True) **.Accept =
"image/\*"
'允许使用相册和相机**
            End With
        End
With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
        e.WriteString(wb.Build)

End
Select

如果希望不能从相册选择，而是直接拍照上传，可以再将Capture属性设置为"camera"，例如：

Select
Case e.Path
    Case
"test.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg22","文件上传")
            With .AddUploader("up2","图片",True)
**.Accept =
"image/\*"
                .Capture =
"camera"** **'****只能拍照上传**
            End With
        End
With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
        e.WriteString(wb.Build)

End
Select

### 接收上传的文件

接收上传的文件


**接收上传的文件**

假定有下图所示的一个表：

希望设计一个下图所示的录入界面，能拍照并上传照片：

HttpRequest事件代码：

Dim
wb As
New weui
Select
Case e.Path
    Case "addnew.htm"
        If e.PostValues.Count
= 0 Then
            wb.AddForm("","form1","addnew.htm")
            With wb.AddInputGroup("form1","ipg1","增加员工")
                .AddInput("姓名","姓名","Text")
'前一个"姓名"是ID,后一个"姓名"是标题
                .AddInput("年龄","年龄","number")
                .AddSelect("学历","学历","大专|本科|硕士|博士")
                .AddUploader("up1","照片",True)
'True表示允许上传多个文件
            End With
            With
wb.AddButtonGroup("form1","btg1",True)
                .Add("btn1",
"确定",
"submit")
            End With
            e.WriteString(wb.Build)
        Else
            Dim
nms() As
String = {"姓名","年龄","学历"}

Dim
dr

As

DataRow
=
DataTables("员工").AddNew()
            For Each
nm As
String In
nms
                dr(nm)
= e.PostValues(nm)
            Next
            For
Each key As
String In
e.Files.Keys
                If
key = "up1"
Then
                    For
Each fln
As String
In e.Files(key)
                        e.SaveFile(key,
fln, ProjectPath
& "Attachments\"
& fln)
                    Next
                    dr.Lines("照片")
= e.Files(key)
                End If
            Next
            '保存并生成增加成功提示页面
            dr.save()
            With wb.AddMsgPage("","msgpage","增加成功",
"好好学习,天天向上")
'生成成功提示页
                .AddButton("btn1","继续增加","addnew.htm")
            End With
            e.WriteString(wb.Build)
        End If
End
Select

关于Foxtable是如何接收用户上传的文件，我们在快速入门这一章已经讲述，参考：[文件的上传与接收](0030.htm)

关于如何处理包括多行内容的单元格，参考：[单元格多行内容的处理](http://www.foxtable.com/webhelp/scr/2717.htm)

### 图片浏览窗口

图片浏览窗口


**图片浏览窗口**

在Uploader中，单击图片，会出现一个图片浏览窗口，在这个窗口中，你可以：

1、点击窗口左侧显示上一副图片。

2、点击窗口右侧显示下一幅图片。

3、点击窗口中央位置关闭图片浏览窗口。

### 我只想浏览图片

我只想浏览图片


**我只想浏览图片**

如果将Uploader的AllowAdd属性设置为False，Uploader的文件上传功能将被关闭，成为一个单纯的图片浏览器。

HttpRequest事件代码：

Select
Case e.Path
    Case
"test.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","客户资料")
            .AddInput("姓名","姓名","text").value
= "舒淇"
            .AddInput("地点","地点","text").Value
= "蒙古草原"
            .AddInput("日期","日期","date").value
= #10/12/2012#
            With .AddUploader("up1","",True)
                .AllowAdd =
False
'关闭文件上传功能
                .AddImage("./images/001.jpg")
                .AddImage("./images/002.jpg")
                .AddImage("./images/003.jpg")
                .AddImage("./images/004.jpg")
                .AddImage("./images/005.jpg")
                .AddImage("./images/006.jpg")
                .AddImage("./images/007.jpg")
                .AddImage("./images/008.jpg")
                .AddImage("./images/009.jpg")
                .AddImage("./images/010.jpg")
                .AddImage("./images/011.jpg")
                .AddImage("./images/012.jpg")
            End With
        End
With
        e.WriteString(wb.Build)
'生成网页
End
Select

下图是通过手机访问的效果：

### 使用缩略图

使用缩略图


**使用缩略图**

为了提高网页打开速度，我们可以在Uploader中显示低分辨率的缩略图，在图片浏览器中显示高分辨率的原图。

**一个例子**

HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","客户资料")
            .AddInput("姓名","姓名","text").value
= "舒淇"
            .AddInput("地点","地点","text").Value
= "蒙古草原"
            .AddInput("日期","日期","date").value
= #10/12/2012#
            With .AddUploader("up1","",True)
                .AllowAdd =
False
'关闭文件上传功能

 'AddImage的第一个参数为缩略图，第二个参数为原图
                .AddImage("./images/001s.jpg","./images/001.jpg")
                .AddImage("./images/002s.jpg","./images/002.jpg")
                .AddImage("./images/003s.jpg","./images/003.jpg")
                .AddImage("./images/004s.jpg","./images/004.jpg")
                .AddImage("./images/005s.jpg","./images/005.jpg")
                .AddImage("./images/006s.jpg","./images/006.jpg")
                .AddImage("./images/007s.jpg","./images/007.jpg")
                .AddImage("./images/008s.jpg","./images/008.jpg")
                .AddImage("./images/009s.jpg","./images/009.jpg")
                .AddImage("./images/010s.jpg","./images/010.jpg")
                .AddImage("./images/011s.jpg","./images/011.jpg")
                .AddImage("./images/012s.jpg","./images/012.jpg")
            End
With
        End
With
        e.WriteString(wb.Build)
'生成网页
End
Select

这是通过手机访问的显示效果：

### 开启图片删除功能

开启图片删除功能


**开启图片删除功能**

如果将Uploader的AllowDelete属性设置为True,在图片浏览窗口的底部会出现一个删除按钮，单击这个按钮，可以删除正在浏览的图片。

HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","客户资料")
            .AddInput("姓名","姓名","Text").value
= "舒淇"
            .AddInput("年龄","年龄","number").Value
= "28"
            .AddInput("日期","日期","date").value
= #10/12/2012#
            With .AddUploader("up1","照片",True)
                .AllowDelete =
True
'允许用户删除图片
                .AddImage("./images/shuqi1.jpg")
                .AddImage("./images/shuqi2.jpg")
                .AddImage("./images/shuqi3.jpg")
            End With
        End
With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
        e.WriteString(wb.Build)
'生成网页
End
Select

这是通过手机访问的效果，当所有图片都被删除完毕时，图片浏览窗口会被自动关闭：

### 删除后台文件

删除后台文件


**删除后台文件**

在默认情况下，用户删除Uploader中显示的图片，并不会影响服务器中对应的的图片文件。

如果要同步删除服务器中的图片文件，我们还需要做响应的处理。

**原理：**

将Uploader的AllowEdit属性设置为True之后，系统会自动生成一个隐藏的输入框，这个输入框的ID是Uploader的ID加上“\_deleted”。
该隐藏输入框会自动记录用户删除的图片文件，如果删除了多个图片文件，会用符号"|"分割文件名。
用户向服务端提交数据时，这个隐藏输入框的值会一并提交，服务端可以从这个值中提取出用户已经删除的文件，然后删除后台对应的文件。

**一个例子：**

HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        If e.PostValues.Count
= 0 Then
            Dim
wb As New
weui
            wb.AddForm("","form1","test.htm")
            With wb.AddInputGroup("form1","ipg1","客户资料")
                .AddInput("姓名","姓名","Text").value
= "舒淇"
                .AddInput("年龄","年龄","number").Value
= "28"
                .AddInput("日期","日期","date").value
= #10/12/2012#
                With .AddUploader("up1","照片",True)
                    .AllowDelete =
True '允许用户删除图片
                    .AddImage("./images/shuqi1.jpg")
                    .AddImage("./images/shuqi2.jpg")
                    .AddImage("./images/shuqi3.jpg")
                End
With
            End
With
            With
wb.AddButtonGroup("form1","btg1",True)
                .Add("btn1",
"确定",
"submit")
            End With
            e.WriteString(wb.Build)
'生成网页
        Else
            Dim
sb As New
StringBuilder
            sb.AppendLine("<meta
name='viewport' content='width=device-width,initial-scale=1,user-scalable=0'>")
            sb.AppendLine("已经删除了以下文件:<br/>")
            If e.PostValues.ContainsKey("up1\_deleted")
Then
                Dim
Files = e.PostValues("up1\_deleted").Split("|")
                For
Each File As
String In
Files
                    sb.AppendLine(file
& "<br/>")
                    file =
"d:\web\" &
File.Trim(".")
                    If
Filesys.FileExists(file)
Then
                        Filesys.DeleteFile(file)
                    End
If
                Next
            End
If
            e.WriteString(sb.ToString)
        End
If
End
Select

## 使用PageTitle

PageTitle


**使用PageTitle**

PageTile用于给页面加上标题。

添加PageTitle的语法是：

AddPageTitle(ParentID, ID, Title, SubTitle)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | PageTitle的ID。 |
| Title | 标题。 |
| SubTitle | 副标题。 |

**一个例子**

HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"


Dim wb
As New WeUI
        wb.AddPageTitle("","ph1","FoxUI","为Foxtable用户量身设计")
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1")
            .AddInput("xm","户名","text")
            .AddInput("pw","密码","password")
        End With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
        e.WriteString(wb.Build)
End
Select

下图是通过手机浏览显示的效果：

## 使用PageFooter

使用PageFooter


**使用PageFooter**

PageFooter用于在页面底部显示文字信息和链接，例如版权信息。

**一个例子**

HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
WeUI
        wb.AddPageTitle("","ph1","FoxUI","为Foxtable用户量身设计")
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1")
            .AddInput("xm","户名","text")
            .AddInput("pw","密码","password")
        End With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
        With
wb.AddPageFooter("","pf1","Copyright
&copy; 2008-2016 foxtable.com")
            .AddLink("底部链接","http://www.foxtable.com")
        End With
        e.WriteString(wb.Build)
End
Select

下图是通过手机访问的效果，可以看到页面底部有版权说明和链接：

**AddPageFooter**

AddPageFooter用于增加PageFooter，语法：

AddPageFooter(ParentId,
ID, Text)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | PageFooter的ID。 |
| Text | PageFooter的文本内容。 |

**AddLink**

AddLink用于给PageFooter增加链接，语法：

AddLink(Text, Href, Attribute)

|  |  |
| --- | --- |
| Text | 链接的文本内容。 |
| Href | 目标URL。 |
| Attribute | 可选参数，用于设置链接属性。 |

## 使用List

List


**使用List**

List(列表)用于列表内容，列表项可以附带说明、超链接和图标。

**一个例子**

HttpRequest事件代码

Select
Case e.Path
    Case "test.htm"

Dim wb
As New WeUI
        With
wb.AddListGroup("",
"lsg1","简单列表")
            .Add("ls1",
"新浪主页")
            .Add("ls2",
"网易主页")
        End With
        With
wb.AddListGroup("",
"lsg2",
"增加说明的列表")
            .Add("ls3","新浪主页",
"sina.com")
            .Add("ls4","网易主页",
"163.com")
        End With
        With
wb.AddListGroup("",
"lsg3",
"增加跳转的列表")
            .Add("ls5","新浪主页",
"sina.com",
"http://www.sina.com.cn")
            .Add("ls6","网易主页",
"163.com",
"http://www.163.com")
        End With
        With
wb.AddListGroup("",
"lsg4","增加图标的列表")
            .Add("ls7","新浪主页",
"sina.com",
"http://www.sina.com.cn", "./images/sina.png")
            .Add("ls8","网易主页",
"163.com",
"http://www.163.com", "./images/163.png")
        End With
        e.WriteString(wb.Build)
End
Select

图标大小建议为16\*16像素，下图是通过手机访问的效果：

AddListGroup

Add用于增加列表项组，其语法为：

AddListGroup(ParentID,
ID, Text)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | 分组ID。 |
| Text | 可选参数，用于指定分组标题。 |

**Add**

Add用于增加列表项，其语法为：

Add(ID, Text)
Add(ID, Text, Description)
Add(ID, Text, Description, Href)
Add(ID, Text, Description, Href, Image)

|  |  |
| --- | --- |
| ID | ID。 |
| Text | 列表内容。 |
| Description | 列表说明 |
| Href | 超链接。 |
| Image | 图标。 |

## 给List加上徽章

给List加上徽章


**给List加上徽章**

List的列表项有个字符型属性Badge，可以用来给列表项设置徽章。

**一个例子**

HtppRequest事件代码

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
WeUI
        With
wb.AddListGroup("",
"lsg1","简单列表")
            .Add("ls1",
"新浪主页").Badge
= "8"
            .Add("ls2",
"网易主页").Badge=
" "
        End
With
        With
wb.AddListGroup("",
"lsg2",
"增加说明的列表")
            .Add("ls3","新浪主页",
"sina.com").Badge
= "New"
            .Add("ls4","网易主页",
"163.com")
        End With
        With
wb.AddListGroup("",
"lsg3",
"增加跳转的列表")
            .Add("ls5","新浪主页",
"sina.com",
"http://www.sina.com.cn").Badge =
" "
            .Add("ls6","网易主页",
"163.com",
"http://www.163.com")
        End With
        With
wb.AddListGroup("",
"lsg4","增加图标的列表")
            .Add("ls7","新浪主页",
"sina.com",
"http://www.sina.com.cn", "./images/sina.png")
            .Add("ls8","网易主页",
"163.com",
"http://www.163.com", "./images/163.png").Badge="新"
        End
With
        e.WriteString(wb.Build)
End
Select

这是通过手机访问的显示效果：

提示：如果Badge被设置为空格，徽章会显示为一个红色小圆。

## 使用Grid

Grid


**Grid**

Grid(网格)通常用于设计首页的功能导航。

**一个例子**

HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"


Dim wb
As New WeUI
        wb.AddPageTitle("","pageheader","WeUI","微信网页设计样式库")
        With wb.AddGrid("","g1")
            .Add("c1","Button",
"./images/button.png").Attribute
= "onclick='javascript:alert(""你单击了我!"")'"
            .Add("c2","Cell",
"./images/cell.png",
"http://www.foxtable.com")
            .Add("c3","Toast",
"./images/toast.png",
"http://www.foxtable.com")
            .Add("c4","Dialog",
"./images/dialog.png",
"http://www.foxtable.com")
            .Add("c5","Progress",
"./images/progress.png",
"http://www.foxtable.com")
            .Add("c6","Msg",
"./images/msg.png",
"http://www.foxtable.com")
            .Add("c7","Article",
"./images/article.png",
"http://www.foxtable.com")
            .Add("c8","ActionSheet",
"./images/actionSheet.png",
"http://www.foxtable.com")
            .Add("c9","Icons",
"./images/icons.png",
"http://www.foxtable.com")
            .Add("c10","Panel",
"./images/panel.png",
"http://www.foxtable.com")
            .Add("c11","Tab",
"./images/tab.png",
"http://www.foxtable.com")
            .Add("c12","SearchBar",
"./images/search.png",
"http://www.foxtable.com")
        End With
        e.WriteString(wb.Build)
End
Select

这是通过手机访问的显示效果：

**A****ddGrid**

AddGrid方法用于增加网格，语法：

AddGrid(ParentID,ID)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | 网格ID。 |

**Add**

Add方法用于在网格中添加单元格，语法：

Add(ID, Text, Image)
Add(ID, Text, Image, Href)

|  |  |
| --- | --- |
| ID | 单元格ID。 |
| Text | 单元格文本 |
| Image | 单元格图片 |
| Href | 可选参数，页面链接地址。 |

## 使用Panel

使用Panel


**使用Panel**

Panel主要用于图文组合列表显示。

**一个例子**

Select
Case e.Path
    Case "test.htm"


Dim wb
As New WeUI
        Dim txt
As String =
"由各种物质组成的巨型球状天体,叫做星球.星球有一定的形状,有自己的运行轨道."
        With wb.AddPanelGroup("","pg1","图文组合列表")
            .Add("pn1","标题一",txt,"./images/button.png","http://www.foxtable.com")
'超链接
            With .Add("pn2","标题二",txt,"./images/search.png")
'带子链接
                .AddFoot("文字来源")
                .AddFoot("时间")
                .AddFoot("|其他信息","http://www.foxtable.com")
            End With
        End With
        With wb.AddPanelGroup("","pg2","文字组合列表")
            .Add("pn1","标题一",txt)
'普通列表
            .Add("pn1","标题
二",txt,"","http://www.foxtable.com")
'超链接
            With .Add("pn2","标题三",txt)
'带有子链接
                .AddFoot("文字来源")
                .AddFoot("时间")
                .AddFoot("|其他信息","http://www.foxtable.com")
            End With
            .GroupFoot =
"查看更多"

'底部链接
            .GroupHref =
"http://www.foxtable.com/"
        End With
        e.WriteString(wb.Build)
'生成网页
End
Select

这是在手机上的显示效果：

AddPanelGroup

AddPanelGroup用于增加组合列表组，语法：

AddPanelGroup(ParentID,ID,Text)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | 分组ID。 |
| Text | 可选参数，用于指定分组标题。 |

GroupFoot和GroupHref

GroupFoot和GroupHref属性用于在列表组的结束位置显示一个超链接，上图中的"查看更多"链接就是通过这两个属性实现的。

Add

Add方法用于增加组合列表项，语法：

Add(ID, Text,
Content)
Add(ID, Text,
Content, Image)
Add(ID, Text, Content,
Image, Href)

|  |  |
| --- | --- |
| ID | 列表ID。 |
| Text | 列表标题。 |
| Content | 列表内容 |
| Image | 可选参数，列表图片。 |
| Href | 可选参数，单击列表要跳转到的目标URL。 |

**AddFoot**

AddFoot方法用于在列表项的下方添加脚注，语法：

AddFoot(Text)
AddFoot(Text，Href)

|  |  |
| --- | --- |
| Text | 脚注内容。 |
| Href | 可选参数，单击脚注要跳转到的目标URL。 |

## 给Panel加上徽章

给Panel加上徽章


**给Panel加上徽章**

Panel有个字符型属性Badge，可以用来设置徽章。

**一个例子**

HtppRequest事件代码:

Select
Case e.Path
    Case
"test.htm"
        Dim
wb As New
WeUI
        Dim
txt As
String = "由各种物质组成的巨型球状天体,叫做星球.星球有一定的形状,有自己的运行轨道."
        With wb.AddPanelGroup("","pg1","图文组合列表")
            .Add("pn1","标题一",txt,"./images/button.png","http://www.foxtable.com").Badge
= "8"
            With .Add("pn2","标题二",txt,"./images/search.png")

                .Badge=
" "
                .AddFoot("文字来源")
                .AddFoot("时间")
                .AddFoot("|其他信息","http://www.foxtable.com")
            End With
        End
With
        With
wb.AddPanelGroup("","pg2","文字组合列表")
            .Add("pn1","标题一",txt)

            .Add("pn1","标题二",txt,"","http://www.foxtable.com").Badge="新"
            With .Add("pn2","标题三",txt)

                .Badge =
"New"
                .AddFoot("文字来源")
                .AddFoot("时间")
                .AddFoot("|其他信息","http://www.foxtable.com")

End
With
        End
With
        e.WriteString(wb.Build)
'生成网页
End
Select

下图是通过手机访问的显示效果：

提示：如果Badge被设置为空格，徽章会显示为一个红色小圆。

## 使用Article

使用Article


**使用Article**

Article用于显示大段的文字，支持分段、多层标题、引用和内嵌图片。

一个例子

HttpRequest事件代码

'''
Select
Case e.Path
    Case "test.htm"


Dim wb
As New WeUI
        With
wb.AddArticle("","ar1")
            .AddTitle("h1","大标题")
            .AddTitle("h2","章标题")
            .AddTitle("h3","1.1节标题")
            .AddContent("Lorem
ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute")
            .AddImage("./images/001.jpg")
            .AddTitle("h3","1.2节标题")
            .AddContent("Foxtable将Excel、Access、Foxpro、VB以及易表的优势融合在一起，无论是数据录入、查询、统计，还是报表生成，都前所未有的强大和易用，普通用户无需编写任何代码，即可轻松完成复杂的数据管理工作，真正做到拿来即用。")
            .AddImage("./images/002.jpg")
        End With
        e.WriteString(wb.Build)
'生成网页
End
Select

这是通过手机访问的显示效果：

**AddArticle**AddArticle用于增加Article，语法为：

AddArticle(ParentID,
ID)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | 组件ID。 |

**AddTitle**

AddTitle用于增加标题，语法为：

AddTitle(Level, Text)
AddTitle(Level, Text, Attribute)

|  |  |
| --- | --- |
| Level | 标题层级，有6个可选值，分别为：h1、h2、h3、h4、h5、h6。 |
| Text | 标题内容。 |
| Attribute | 可选值，标题属性。 |

**A****ddContent**

AddContent用于增加文本段落，语法为：

AddContent(Text)
AddContent(Text, Attribute)

|  |  |
| --- | --- |
| Text | 段落内容。 |
| Attribute | 可选值，段落属性。 |

**AddImage**

AddImage用于增加图片，语法为：

AddImage(Image, Attribute)

|  |  |
| --- | --- |
| Image | 图片文件。 |
| Attribute | 可选值，图片属性。 |

## 使用Dialog

使用Dialog


**使用Dialog**

Dialog用于显示一个对话框。

**一个例子**

HttpRequest事件代码：

'''
Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
WeUI
        With
wb.AddButtonGroup("","bng2",True)
            .Add("btn1","Dialog1").Attribute
= "onclick=""show('dlg1')"""
            .Add("btn2","Dialog2").Attribute
= "onclick=""show('dlg2')"""
        End
With
        With
wb.AddDialog("","dlg1",
"提示","您的订单正在派送,请注意查收!")
            .AddButton("btnOK","确定").Attribute
= "onclick=""alert('谢谢支持!')"""
        End
With
        With
wb.AddDialog("","dlg2",
"删除确认","您确定要删除当前记录吗?")
            .AddButton("btnCancel","取消").Kind =
1
            .AddButton("btnOK","确定","./delete.htm?id=12")
        End With
        e.WriteString(wb.Build)
'生成网页
    Case "delete.htm"
        Dim
sb As New
StringBuilder
        sb.AppendLine("<meta
name='viewport' content='width=device-width,initial-scale=1,user-scalable=0'>")


sb.AppendLine("呜呜，我被删除了！")
        e.WriteString(sb.ToString)
End
Select

提示：

1、上述代码中的show，是我们在文件"weui.me.js"定义的一个函数，分别用于显示和隐藏指定ID的对象
，对应地还有一个hide函数，用于隐藏指定ID的对象。
2、注意所有js函数都是区分大小写的，例如你用Show或者Hide，是不会执行的，今后不会再重复提示，请大家注意了。

通过手机访问，会显示两个按钮，分别单击两个按钮，会显示两个对话框：



AddDialog

AddDialog用于添加对话框,语法：

AddDialog(ParentId, ID, Title, Content)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | 对话框ID。 |
| Title | 对话框标题。 |
| Content | 对话框内容。 |

**AddButton**
AddButton用于添加对话框按钮，语法：

AddButton(ID, Text)
AddButton(ID, Text, Href)

|  |  |
| --- | --- |
| ID | 按钮ID |
| Text | 按钮标题 |
| Href | 可选参数，字符型，指定单击按钮之后跳转的目标网页的URL |

**Dialog的属性有：**

Visible：逻辑型，打开网页后是否显示Dialog，默认为False。

## showDialog函数

showDialog函数


**showDialog函数**

showDialog是是我们在文件"weui.me.js"定义的一个函数，专门用于显示对话框，而且可以修改显示的标题和内容，语法：

showDialog(id,Title,Content)

|  |  |
| --- | --- |
| ID | 对话框ID。 |
| Title | 对话框标题。 |
| Content | 对话框内容。 |

有了showDialog，我们可以用同一个对话框，显示不同的内容。

**一个例子**

HttpRequet事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
WeUI
        With
wb.AddButtonGroup("","bng2",True)
            .Add("btn1","内容1").Attribute
= "onclick=""showDialog('dlg1','恭喜','恭喜您抽中大奖,记得及时领奖哦!')"""
            .Add("btn2","内容2").Attribute
= "onclick=""showDialog('dlg1','成功','增加记录成功,单击确定继续增加!')"""
        End With
        With
wb.AddDialog("","dlg1",
"","")
            .AddButton("btnOK","确定")

End
With
        e.WriteString(wb.Build)
'生成网页
End
Select

下图是通过手机访问的效果，我们只定义了一个对话框，分别单击两个按钮，会在这个对话框显示不同的内容：

## 使用TabBar

使用TabBar


**使用TabBar**

TabBar可以包括多个页面，可以在顶端或底端显示页面切换按钮：

**一个例子**

上图的效果是通过下面的HttpRequest事件代码生成的，因为包括三个页面的内容，所以代码比较长：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
WeUI
        Dim
txt As
String = "由各种物质组成的巨型球状天体,叫做星球.星球有一定的形状,有自己的运行轨道."

'增加三个页面,一个按钮

With
wb.AddTabBar("",
"tb1", 1)
            .AddPage("page1","微信","./images/button.png")
            .AddPage("page2","通讯录","./images/msg.png")
            .AddPage("page3","发现","./images/article.png")
            .AddButton("bt1","我","./images/cell.png","http://www.foxtable.com")
        End
With
        '为第一个页面增加内容
        wb.AddForm("page1","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1")
            .AddInput("xm","户名","text")
            .AddInput("mm","密码","password")
        End With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定", "submit")
        End With
        '为第二个页面增加内容
        With
wb.AddPanelGroup("page2","pg1","图文组合列表")
            .Add("pn1","标题一",txt,"./images/button.png","http://www.foxtable.com")
            With .Add("pn2","标题二",txt,"./images/search.png")
                .AddFoot("文字来源")
                .AddFoot("时间")
                .AddFoot("|其他信息","http://www.foxtable.com")

End
With
            .GroupFoot =
"查看更多"
            .GroupHref =
"http://www.foxtable.com/"
        End
With
        '为第三个页面增加内容
        With wb.AddArticle("page3","ar1")
            .AddTitle("h1","发现")
            .AddTitle("h2","章标题")
            .AddTitle("h3","1.1节标题")
            .AddContent(txt)
            .AddImage("./images/001.jpg")
            .AddTitle("h3","1.2节标题")
            .AddContent(txt)
            .AddImage("./images/002.jpg")
        End With
        e.WriteString(wb.Build)
End
Select

**AddTabBar**

AddTabBar用于增加TabBar，语法：

AddTabBar(ParentID, ID, Positon)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | TabBar的ID |
| Position | 按钮位置，0显示在底端，1显示在顶端。 |

**AddPage**

AddPage用于增加页面，语法：

AddPage(ID, Text)
AddPage(ID, Text, Image)

|  |  |
| --- | --- |
| ID | 页面ID |
| Text | 页面按钮标题 |
| Image | 可选参数，页面按钮图片 |

**AddButton**

AddButton用于添加按钮，语法：

AddButton(ID, Text)
AddButton(ID, Text, Image)
AddButton(ID, Text, Image, Href)

|  |  |
| --- | --- |
| ID | 按钮ID |
| Text | 按钮标题 |
| Image | 可选参数，设置按钮图片 |
| Href | 可选参数，字符型，指定单击按钮之后跳转的目标网页的URL |

## 使用Page

使用Page


**使用Page**

Page表示一个页面，一个网页可以有多个Page，用于显示不同的内容。
Page需要自行编写代码切换，如果需要自带切换按钮，可以使用TabBar。

添加Page的语法为：

AddPage(ParentID,ID,Visible)

|  |  |
| --- | --- |
| ParentID | 父容器ID，如果是顶层对象，设为""即可。 |
| ID | 页面ID。 |
| Visible | 可选参数，逻辑型，用于设置页面默认是否显示。默认为True。 |

**一个例子**

假定要生成一个网页，这个网页包括两个Page，可以相互切换：



HttpRequest事件代码：

'''
Select
Case e.Path
    Case "test.htm"
        Dim wb
As New
weui
        wb.AddPage("","page1")
'增加两个page
        wb.AddPage("","page2",False)
'第二个
        With wb.AddArticle("page1","ar1")
            .AddTitle("h1","关于Foxtable")
            .AddContent("Foxtable将Excel、Access、Foxpro、VB以及易表的优势融合在一起,无论是数据录入、查询、统计,还是报表生成,都前所未有的强大和易用,普通用户无需编写任何代码,即可轻松完成复杂的数据管理工作,真正做到拿来即用.")
            .AddImage("./images/001.jpg")
        End With
        With wb.AddButtonGroup("page1","btg1")
            .Add("btn1",
"下一页",
"button").Attribute="onclick=""hide('page1');show('page2')"""
        End With
        With wb.AddArticle("page2","ar2")
            .AddTitle("h1","关于易表")
            .AddContent("易表.net介于电子表格和数据库软件之间，它有类似电子表格的界面，同时又有很多数据库软件特有的功能和灵活性，它能将复杂的操作简单化，让普通用户轻松完成复杂的数据管理和统计分析工作.")

.AddImage("./images/002.jpg")
        End With
        With wb.AddButtonGroup("page2","btg2")
            .Add("btn2",
"上一页",
"button").Attribute="onclick=""hide('page2');show('page1')"""
        End With
        e.WriteString(wb.Build)
'生成网页
End
Select

## 使用Toast

使用Toast


**使用Toast**

Toast用于临时显示某些信息，并且会在数秒后自动消失。

**一个例子**

HttpRequest事件代码:

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
WeUI
        With
wb.AddButtonGroup("","bng2",True)
            .Add("btn1","Toast1").Attribute
= "onclick=""show('t1',2000)"""
'参数2000表示2秒后隐藏
            .Add("btn2","Toast2").Attribute
= "onclick=""show('t2',2000)"""
            .Add("btn3","Toast3").Attribute
= "onclick=""show('t3',2000)"""
        End
With
        wb.AddToast("","t1",
"操作完成",0)
        wb.AddToast("","t2",
"正在加载",1)
        wb.AddToast("","t3",
"操作完成",0).Icon=
"success"
        e.WriteString(wb.Build)
End
Select

下图是在手机中访问的效果，单击三个按钮，会分别显示三个Toast，在2秒后会自动消失：

AddToast

AddToast方法用于增加Toast，语法：

AddToast(ParentId, ID, Text, Type)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | ToastID。 |
| Text | Toast文本内容。 |
| Type | Toast类型，默认为0，如果设置为1，图标将显示为一个表示正在运行的动画。 |

**Toast的属性有：**

|  |  |
| --- | --- |
| Visible | 逻辑型，打开网页后是否显示Toast，默认为False。 |
| msec | 整数型，默认为0，用于设置Toast初始显示的毫秒数。 |
| Icon | 字符型，指定Toast显示的图标，默认为"default"。    其他可选值有"success","info","warn",对应的图标分别是： |

## 给用户一个提示

给用户一个提示


**给用户一个提示**

如果表单包括文件上传组件Uploader，那么有必要在提交表单的过程中，给用户一个提示，避免用户失去耐心：

**知识准备**

用户单击确定按钮提交表单的时候，会触发表单的onsubmit事件，我们可以在这个事件中显示一个toast，提示用户正在上传文件，例如：

wb.AddForm("","form1","test.htm").attribute= "onsubmit=""show('t1')"""

表示定义了一个表单，提交这个表单的时候，会显示名为t1的toast，不仅可以给用户一个提示，还可以避免用户再次单击确定按钮，重复提交数据。

**HttpRequest事件代码:**

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
weui
        wb.AddToast("","t1",
"正在上传",1)
'定义提示
        wb.AddForm("","form1","test.htm").attribute=
"onsubmit=""show('t1')"""
        With
wb.AddInputGroup("form1","ipg1","客户资料")
            .AddInput("姓名","姓名","Text").value
= "舒淇"
            .AddInput("年龄","年龄","number").Value
= "28"
            .AddInput("日期","日期","date").value
= #10/12/2012#
            With .AddUploader("up1","照片",True)
                .AddImage("./images/shuqi1.jpg")
                .AddImage("./images/shuqi2.jpg")
            End With
        End
With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
        e.WriteString(wb.Build)
'生成网页
End Select

## 使用TopTips

使用TopTips


**使用TopTips**

TopTips用于在页面顶端临时显示信息，并且会在数秒后自动消失。

**一个例子**

假定你设计了一个用户登录页面，如果用户单击确定按钮之前，没有输入用户名和密码，就在顶部显示一个提示信息，2秒后自动消失：

这个例子对于iOS用户比较有意义，因为required属性对于iOS设备无效。

**知识准备**

用户单击确定按钮提交表单的时候，会触发表单的onsubmit事件，这个事件如果返回false，将终止提交表单。
例如下面的定义表单的代码，表示提交表单前，先执行valid函数:

wb.AddForm("","form1","logon.htm").Attribute
= "onsubmit='return valid()'"

如果valid函数返回false，将终止提交表单。

**设计步骤：**

1、在"d:\web\lib"新建一个文本文件，文件名为"valid.js"，文件内容为：

function valid(){
   var v1 = document.getElementById("xm").value;
   var v2 = document.getElementById("pw").value;
   if (v1 && v2){return true}
   show("toptip1",2000);
   return false;
}

2、HttpRequest事件代码：

Select
Case e.Path
    Case "logon.htm"
        If e.PostValues.Count
= 0 Then
            Dim
wb As
New WeUI
            wb.AddTopTips("","toptip1","请输入姓名和密码!")
            wb.AddForm("","form1","logon.htm").Attribute
= "onsubmit='return valid()'"
'调用函数
            With
wb.AddInputGroup("form1","ipg1","用户登录")
                .AddInput("xm","户名","text")
                .AddInput("pw","密码","password")
            End With
            With
wb.AddButtonGroup("form1","btg1",True)
                .Add("btn1",
"确定",
"submit")
            End With
            wb.AppendHTML("<script
src='./lib/valid.js'></script>")
'引入脚本文件
            e.WriteString(wb.Build)
        Else
            Dim
sb As
New StringBuilder
            sb.AppendLine("<meta
name='viewport' content='width=device-width,initial-scale=1,user-scalable=0'>")
            For Each
key As
String In
e.PostValues.Keys
                sb.AppendLine(key
& ":"
& e.PostValues(key)
& "</br>")
            Next
            e.WriteString(sb.ToString)

End
If
End
Select

AddTopTips

AddTopTips用于增加TopTips，语法：

AddTopTips(ParentId, ID, Text)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | TopTips的ID。 |
| Text | TopTips文本内容。 |

**showTopTips**

前面的例子，我们用show方法显示TopTips，如果显示内容是变化的，可以改用showTopTips方法。
showTopTips是是我们在文件"weui.me.js"定义的一个函数，专门用于显示Toptips，而且可以动态指定显示内容，语法：

showTopTips(id,text,msec)

|  |  |
| --- | --- |
| id | Toptips的ID |
| text | 指定要显示的内容 |
| msec | 指定显示时长，整数型，范围为毫秒 |

**TopTips的属性有：**

|  |  |
| --- | --- |
| msec | 整数型，默认为0，用于设置TopTips初始显示的毫秒数。 |

## 使用ActionSheet

使用ActionSheet


**使用ActionSheet**

ActionSheet用于显示一个从底部弹出的菜单，一般用于响应用户单击页面的动作。

**一个例子**

Select
Case e.Path
    Case "test.htm"
            Dim
wb As
New WeUI
            With
wb.AddButtonGroup("","btg",True)
                .Add("btn1","单击显示上拉菜单").Attribute
= "onclick=""show('s1')"""
            End
With
            With
wb.AddActionSheet("","s1")
                .Add("menu1",
"菜单项目1",
"http://www.foxtable.com/")
                .Add("menu2",
"菜单项目2")
                .Add("menu3",
"菜单项目3").Attribute
= "onclick='alert(""你单击了我"")'"
                .Add("menu4","取消","",True)
            End
With
            e.WriteString(wb.Build)
End
Select

通过手机访问，会显示一个按钮，点击这个按钮，底部会弹出一个菜单：

**AddActionSheet**

AddActionSheet用于增加ActionSheet，语法：

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | ActionSheet的ID。 |

**Add**

Add用于在ActionSheet中增加菜单项，语法：

Add(ID, Text)
Add(ID, Text, Href)
Add(ID, Text, Href, Separator)

|  |  |
| --- | --- |
| ID | 菜单项的ID。 |
| Text | 菜单项的文本内容。 |
| Href | 可选参数，单击菜单项后要跳转到的目标URL。 |
| Separator | 可选参数，逻辑型，是否在此菜单项之前显示一个分割条。 |

## 使用Preview

使用Preview


**使用Preview**

Preview通常用于表单内容预览。

**一个例子**

HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
weui
        With
wb.AddPreview("","pv1","付款金额","￥2400")
            .AddItem("项目1","内容1")
            .AddItem("项目2","内容2")
            .AddItem("项目3",
"电动打蛋机")
            .Addbutton("操作",
"", 1,
"onclick='alert(""你单击了我"")'")
       End
With
        wb.AppendHTML("<br/>")
        With wb.AddPreview("","pv2","付款金额","￥3400")
            .AddItem("项目1","内容1")
            .AddItem("项目2","内容2")
            .AddItem("项目3",
"电动打蛋机")
            .Addbutton("辅助操作",
"http://www.foxtable.com",
0)
            .Addbutton("操作",
"", 1,
"onclick='alert(""你单击了我"")'")
       End
With
        e.WriteString(wb.Build)
'生成网页
End
Select

下面是通过手机访问的显示效果：

**AddPreview**

AddPreview用于增加Preview，语法：

AddPreview(ParentID, ID, HeadText, HeadValue)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | Preview的ID。 |
| HeadText | 标题文本 |
| HeadValue | 标题的值 |

**AddItem**

AddItem用于在Preview中增加项目，语法：

AddItem(Text, Value)
AddItem(Text, Value, Attribute)

|  |  |
| --- | --- |
| Text | 项目标题 |
| Value | 项目值 |
| Attribute | 可选参数，项目属性。 |

**Addbutton**

Addbutton用于在Preview底部增加操作按钮，语法：

Addbutton(Text, Href)
Addbutton(Text, Href, Type)
Addbutton(Text, Href, Type, Attribute)

|  |  |
| --- | --- |
| Text | 按钮标题 |
| Href | 单击按钮后要跳转到的目标URL。 |
| Type | 可选参数，设置为0按钮文字为灰色，设为1按钮文字为绿色 |
| Attribute | 可选参数，按钮属性。 |

## 使用Gallery

使用Gallery


**使用Gallery**

`Gallery`用于实现图片的展示或幻灯片播放。
我们之前介绍的Uploader，其图片浏览窗口就是一个Gallery。
Gallery也可以单独创建和使用。

一个例子

HttpRequest事件代码：

Select Case
e.Path
    Case "test.htm"
        Dim
wb As new
WeUI
        With
wb.AddGallery("","gla1")
            .AddImage("./images/001.jpg","./images/002.jpg","./images/003.jpg","./images/004.jpg")
        End
With
        e.WriteString(wb.Build)
'生成网页
End Select

下图是通过手机访问的效果，点击图片的右侧切换到下一副图片，单击图片左侧切换到上一副图片：

**AddGallery**

AddGallery用于添加AddGallery，语法：

AddGallery(ParentID,
ID)
AddGallery(ParentID, ID, Visible)
AddGallery(ParentID, ID, Visible, AutoHide)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | Gallery的ID。 |
| Visible | 逻辑型，可选参数，Gallery初始是否可见，默认为True |
| AutoHide | 逻辑型，可选参数，默认为False，当需要和其他组件配合使用时，可将此属性设置为True，这样点击图片中央位置，会自动隐藏Gallery。 |

**AddImage**

AddImage用于向Gallery添加图片，语法：

AddImage(Images)
AddImage(Image1, Image2, Image3...)

|  |  |
| --- | --- |
| Images | 图片文件的集合或数组。 |
| Image1, Image2, Image3 | 要添加的多个图片文件。 |

## 结合Article和Gallery

结合Article和Gallery


结合Article和Gallery

Article可能包括很多图片，有的时候，可能希望点击Article中的某个图片，能自动显示一个Gallery，集中显示所有图片：

**自动实现**

实现这个功能很简单，只需将Article的UserGallery属性设置为True即可，参考下面的HttpRequest事件代码:

Select
Case e.Path

Case
"test.htm"

Dim wb
As new
WeUI

With wb.AddArticle("","ar1")
            .UseGallery
= True
'启用Gallery,必须放在第一行
            .AddTitle("h1","大标题")
            .AddTitle("h2","章标题")
            .AddTitle("h3","1.1节标题")
            .AddContent("Write
your Sad Times in Sand, Write your Good Times in Stone.-- George Bernard Shaw")
            .AddImage("./images/001.jpg")
            .AddTitle("h3","1.2节标题")
            .AddContent("Write
your Sad Times in Sand, Write your Good Times in Stone.-- George Bernard Shaw")
            .AddImage("./images/002.jpg")
            .AddTitle("h2","章标题")
            .AddTitle("h3","2.1节标题")
            .AddContent("Write
your Sad Times in Sand, Write your Good Times in Stone.-- George Bernard Shaw")
            .AddImage("./images/003.jpg")
            .AddTitle("h3","2.2节标题")
            .AddContent("Write
your Sad Times in Sand, Write your Good Times in Stone.-- George Bernard Shaw")
            .AddImage("./images/004.jpg")

End
With

e.WriteString(wb.Build)

End
Select

**手工实现**

你也可以自己编码完成同样的任务，自己编码的好处是可以进行更多的控制，例如排除部分图片，或为提高网页打开速度，在Article显示低分辨率的图，在Gallery中显示高分辨率的原图。
你还可以用这个方法，将Gallery和其他元素组合使用。

HttpRequest事件代码：


Select
Case e.Path

Case
"test.htm"

Dim wb
As new
WeUI

With wb.AddArticle("","ar1")
            .AddTitle("h1","大标题")
            .AddTitle("h2","章标题")
            .AddTitle("h3","1.1节标题")
            .AddContent("Write
your Sad Times in Sand, Write your Good Times in Stone.-- George Bernard Shaw")
            .AddImage("./images/001.jpg","onclick=""showGallery('gla1','./images/001.jpg')""")
            .AddTitle("h3","1.2节标题")
            .AddContent("Write
your Sad Times in Sand, Write your Good Times in Stone.-- George Bernard Shaw")
            .AddImage("./images/002.jpg","onclick=""showGallery('gla1','./images/002.jpg')""")
            .AddTitle("h2","章标题")
            .AddTitle("h3","2.1节标题")
            .AddContent("Write
your Sad Times in Sand, Write your Good Times in Stone.-- George Bernard Shaw")
            .AddImage("./images/003.jpg","onclick=""showGallery('gla1','./images/003.jpg')""")
            .AddTitle("h3","2.2节标题")
            .AddContent("Write
your Sad Times in Sand, Write your Good Times in Stone.-- George Bernard Shaw")
            .AddImage("./images/004.jpg","onclick=""showGallery('gla1','./images/004.jpg')""")

End
With

'增加Gallery,第三个参数False表示初始隐藏,第四个参数True表示点击图片自动隐藏

With wb.AddGallery("","gla1",False,True)
            .AddImage("./images/001.jpg","./images/002.jpg","./images/003.jpg","./images/004.jpg")

End
With

e.WriteString(wb.Build)
'生成网页
End
Select

**showGallery**

showGallery是在框架文件"weui.me.js"中定义的一个函数(注意JavaScript是区分大小写的)，用于显示Gallery，语法为：

showGallery(ID, Image)

|  |  |
| --- | --- |
| ID | Gallery的ID |
| Image | 要在Gallery中显示的图片，必须事先添加到Gallery中。 |

## 使用Progress

使用Progress


使用Progress

Progress表示进度条。

**一个例子**

HttpRequest事件代码

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
WeUI
        wb.AddPageTitle("","ph1","Progress")
        wb.AddProgress("","pgb1",True,20).CancelCommand
= "onclick=""alert('你取消了')"""
        With wb.AddButtonGroup("","btg1",)
            .Add("btn1",
"设置进度").Attribute=
"onclick=""setProgressValue('pgb1',80)"""
        End
With
        e.WriteString(wb.Build)
End
Select

这是在手机上的显示效果。

**AddProgress**

AddProgress用于增加Progress，语法：

AddProgress(ParentID, ID)
AddProgress(ParentID, ID, Visible)
AddProgress(ParentID, ID, Visible, Value)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可。 |
| ID | Progress的ID。 |
| Visible | 逻辑型，可选参数，Progress初始是否可见，默认为True |
| Value | 整数型，可选参数，设置Progress初始值，范围为0-100。 |

**setProgressValue**

setProgressValue是我们在文件weui.me.js中扩展的一个函数，用于设置Progress的值，语法：

setProgressValue(ID,Value)

|  |  |
| --- | --- |
| ID | Progress的ID。 |
| Value | 要设置的值，范围为0-100。 |

**getProgressValue**

我们在为你教案weui.me.js还扩展了一个getProgressValue函数，用于获取Progress的进度值，语法：

getProgressValue(ID)

|  |  |
| --- | --- |
| ID | Progress的ID。 |

## 动态生成图表

动态生成图表


**动态生成图表**

关于Foxtable是如何动态生成图表的，请参考：[ChartBuilder](http://www.foxtable.com/webhelp/scr/1242.htm)

我们可以利用Foxtable的ChartBuilder动态生成图表，然后保存为图片文件，发送给客户端。

但是这样会产生大量的临时文件，为此WeUI提供了一个ImageToBase64方法，可以将ChartBuilder生成的图片直接转换为base64字符串发送给客户端，无需先保存为文件。

**一个例子**

HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
WeUI
        Dim
Chart As New
ChartBuilder
        Dim Series
As WinForm.ChartSeries

        Chart.PrintWidth
= 140
        Chart.PrintHeight
= 100
        Chart.VisualEffect
= True
        For n
As Integer
= 0 To
1
            Series =
Chart.SeriesList.Add()

            Series.Length
= 10
            For i
As Integer
= 0 To
9
                Series.X(i)
= i
                Series.Y(i)
= i + n \*
2 + Rand.Next(5)

            Next
        Next
        wb.AddPageTitle("","ph1","FoxUI")
        wb.InsertHTML("<img
width='100%' src='" &
wb.ImageToBase64(Chart.Image)
&  "'/>")

e.WriteString(wb.Build)
End
Select

这是显示效果：

## 使用Cookie

使用Cookie


**使用Cookie**

通过Cookie可以在本机临时存储数据，每次访问服务器网页时，都会自动将Cookie中的值，传递给服务器。

HttpRequest事件有个Cookies字典，包括所有的Cookie，例如要列出所有Cookie的名称和值：

Dim
sb As
New StringBuilder
For Each key
As String
In e.Cookies.Keys
    sb.AppendLine(key
& ":"
& e.Cookies(key))
Next
e.WriteString(sb.Tostring)

HttpRequest只有一个AppendCookie方法，用于增加Cookie，使用起来不是很方便，参考使用[Cookie](0156.htm)。

WeUI扩展了三个和Cookie相关的方法，分别是：

* **AppendCookie**

  用于添加Cookie，语法为：

  AppendCookie(Name, Value, Expires)

  Name：   Cookie名称
  Value：  Cookie值
  Expires：可选参数，整数型，用于设置Cookie的有效时间，单位是分钟，如果不设置，关闭浏览器后Cookie将失效。
* **DeleteCookie**

  用于删除指定名称的Cookie，语法：

  DeleteCookie(Name)

  Name：Cookie名称
* **ClearCookie**

  清除全部Cookie。

我的建议是：

尽量用WeUI处理Cookie，但是也有一些特殊情况无法使用WeUI，例如HttpClient，此时只能使用HttpRequest内置的AppendCookie方法。

**一个例子**

将HttpRequest事件代码设置为：

Dim
wb As
New WeUI
Dim
cnt As
Integer = 1
If
e.Cookies.ContainsKey("count")
'如果存在名为count的Cookie
    Integer.TryParse(e.Cookies("count"),cnt)
'提取cookie的值,
并转换为整数
    cnt = cnt
+ 1
End
If
wb.AppendCookie("count",cnt)
'在客户端存储Cookie
wb.InsertHTML("您这是第"
& cnt
& "次访问!")
e.WriteString(wb.Build)

现在每次刷新页面，访问次数都会递增1：

## 设计首页和登录页面

设计首页和登录页面


**设计首页和登录页面**

本节的任务是设计一个登录页面：

如果用户名和密码错误，会显示2秒的错误提示：

如果用户名和密码正确，进入首页：

如果在首页点击退出，会回到登录页面。

HttpRequest事件代码：

Dim
wb As
New
weui
'身份验证
Dim
Verified As
Boolean
'用于标记用户是否通过了身份验证
Dim
UserName As
String = e.Cookies("username")
'从cookie中获取用户名
Dim
Password As
String = e.Cookies("password")
'从cookie中获取用户密码
If
e.Path =
"logon.htm"
'如果是通过登录页面访问,从PostValues即可中提取用户名和密码
    If e.PostValues.ContainsKey("username")
AndAlso e.PostValues.ContainsKey("password")
Then
        UserName =
e.PostValues("username")
        Password =
e.PostValues("password")
    End
If
End
If
If
UserName =
"张三"
AndAlso Password
= "888" Then
'实际使用的时候,请改为从数据库读取用户名和密码进行比较
    Verified  =
True
ElseIf
Username =
"李四"
AndAlso Password="999"
Then
    Verified  =
True
End
If
If
Verified AndAlso
e.Path =
"logon.htm"  Then
'如果用户访问的是登录页,且身份验证成功
    wb.AppendCookie("username",UserName)
'将用户名和密码写入cookie
    wb.AppendCookie("password",Password)
    wb.InsertHTML("<meta
http-equiv='Refresh' content='0; url=/default.htm'>")
'直接跳转到首页
    e.WriteString(wb.Build)
'生成网页
    Return
'必须的
ElseIf
Verified = False
AndAlso e.Path
<> "logon.htm" Then
'如果用户身份验证失败,且访问的不是登录页面
    wb.InsertHTML("<meta
http-equiv='Refresh' content='0; url=/logon.htm'>")
'那么直接跳转到登录页面
    e.WriteString(wb.Build)
'生成网页
    Return
'必须的
End
If
'开始生成网页
Select
Case e.path

Case
"logon.htm"
'登录页面
        wb.AddPageTitle("","pageheader","销售系统","由湛江辉迅基于Foxtable开发")
        If e.PostValues.ContainsKey("username")
AndAlso e.PostValues.ContainsKey("password")
Then
'判断是否是验证失败后的重新登录
            wb.AddTopTips("","toptip1","用户名或密码错误!").msec
= 2000
'如果用户通过登录按钮访问,则给用户一个2秒的提示.

End
If
        wb.AddForm("","form1","logon.htm")
        With wb.AddInputGroup("form1","ipg1")
            .AddInput("username","户名","text")
            .AddInput("password","密码","password")
        End With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"登录",
"submit")
        End With
    Case "exit.htm"
'退出登录
        wb.DeleteCookie("username")
'清除cookie中原来的用户名和密码
        wb.DeleteCookie("password")
        wb.InsertHTML("<meta
http-equiv='Refresh' content='0; url=/logon.htm'>")
'那么直接跳转到登录页面
    Case "",
"default.htm"
'首页
        wb.AddPageTitle("","pageheader","销售系统","由湛江辉迅基于Foxtable开发")
        With wb.AddGrid("","g1")
            .Add("c1","增加订单",
"./images/button.png").Attribute
= "onclick='javascript:alert(""你单击了我!"")'"
            .Add("c2","客户管理",
"./images/cell.png",
"http://www.foxtable.com")
            .Add("c3","销售统计",
"./images/toast.png",
"http://www.foxtable.com")
            .Add("c4","Dialog",
"./images/dialog.png",
"http://www.foxtable.com")
            .Add("c5","Progress",
"./images/progress.png",
"http://www.foxtable.com")
            .Add("c6","Msg",
"./images/msg.png",
"http://www.foxtable.com")
            .Add("c7","Article",
"./images/article.png",
"http://www.foxtable.com")
            .Add("c8","ActionSheet",
"./images/actionSheet.png",
"http://www.foxtable.com")
            .Add("c9","Icons",
"./images/icons.png",
"http://www.foxtable.com")
            .Add("c10","Panel",
"./images/panel.png",
"http://www.foxtable.com")
            .Add("c11","Tab",
"./images/tab.png",
"http://www.foxtable.com")
            .Add("c12","退出",
"./images/exit.png",
"exit.htm")
'退出登录
        End
With
End
Select
e.WriteString(wb.Build)
'生成网页

代码逻辑并不复杂，所有知识之前都已经讲述过，唯一没有接触过的是自动跳转网页的代码：

<meta
http-equiv='refresh' content='2; url=/logon.htm'>

表示2秒后跳转到"/logon.htm"页面，如果你要立即跳转，将2改为0即可。

## 让登录变得更安全

让登录变得更安全


**让登录变得更安全**

我们上一节介绍的用户登录，无法避免同名用户重复登录，而且直接通过Cookie存储用户密码
在安全方面也是有欠缺的。

在安全方面，我的建议是：

1、Cookie名称不要用UserName和PassWord等指示性很强的名称。
2、内容加密存储，关于字符的加密和机密，参考：[加密和解密函数](http://www.foxtable.com/webhelp/scr/1346.htm)。
3、不要设置Cookie的有效时间，这样Cookie会随浏览器的关闭而消失。

如果你觉得以上措施还不足以让你在安全方面放心，而且需要禁止重复登录，可以考虑下面的方法。

**设计任务**

1、不能在Cookie存储密码，即使时加密后的密码，也不能出现在Cookie中。
2、同名用户在其他电脑登录后(实际开发时，可以用不同的浏览器来模拟不同电脑)，前一次的登录自动失效。
3、如果用户30分钟内没有操作，或关闭浏览器，登录失效。

**设计思路**

1、服务端新建一个临时表，包括三列，分别是：UserName，UserID和ActiveTime。

2、服务端在验证用户身份后，在临时表中新增一行，生成一个16位的随机字符串存储在UserID列，用户名和当前时间则分别存储在UserName和ActiveTime列。

3、完成上述操作后，再将UserName和UserID保存在Cookie中，其中UserName存储在Cookie中的是加密后的字符串。

4、为方便理解，本节的示例代码直接使用username和userid作为Cookie名称，实际开发的时候，请采用没有任何指示性的名称，注意Cookie名是区分大小写的，这里用的是小写。

5、用户在登录成功，继续访问其他页面时，Cookie中会包括username和userid，服务端根据username和userid从临时表中查找对应的行，此时会有三种可能：

* 如果找到，且ActiveTime和当前时间相比，相差不超过30分钟，允许访问，并将ActiveTime列更新为当前时间。
* 如果找到，但ActiveTime和当前时间相比，相差已超过30分钟，拒绝访问，并删除此行，然后跳转到登录页面。
* 如果没有找到，则拒绝访问，直接跳转到登录页面。

6、如果用户在其他位置登录成功，服务端根据加密后的UserName在临时表中查找对应的行，如果找到，说明是重复登录，删除此行，使得前一次的登录无效
；然后重复2、3操作，在临时表和Cookie中存储加密后的UserName和随机生成的UserID，并在ActiveTime列记录当前时间。

7、显然临时表的记录会越来越多，我们可以定期清除ActiveTime列和当前时间相比超过30分钟的行，也可以在表在超过约定行数后执行一次清理动作，本示例选择的是前者，每30分钟清理一次。

**HttpRequest事件代码**

以下是根据上述设计思路整理出来的HttpRequest事件代码，由于Cookie中的用户名是加密存储的，而且Cookie不会出现密码，出现的是随机生成UserID，
且每次登录UserID都不同，所以安全性会大大提高。

看起来代码有点长，这是因为完成的任务比较多，如果你分开任务看，每一个任务的代码都很精简，也很好理解：

第1到14行代码用于生成临时表和清除过期登录信息；
第21到47行代码用于根据用户输入的用户名和密码进行身份验证，并在在临时表和Cookie中保存登录信息；
第49到第58行代码用于从Cookie中提取登录信息进行身份验证，并更新最后一次活动时间；
第63到第74行代码用于生成登录页面；
第76到第78行代码用于退出登录；
第80到第94行代码用于生成首页。

|  |  |
| --- | --- |
| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96 | Static UserTable As DataTable   '定义一个变量,用于存储用户随机身份ID,以及最后一次活动时间.  Static ClearTime As Date  If UserTable Is Nothing Then '创建用于记录登录信息的临时表      ClearTime = Date.Now()        Dim dtb As New  DataTableBuilder("UserInfos")      dtb.AddDef("UserName", Gettype(String), 16)      dtb.AddDef("UserID",Gettype(String),16)      dtb.AddDef("ActiveTime",Gettype(Date))      UserTable = dtb.Build(True)  End If  If (Date.Now - ClearTime).TotalMinutes >= 30 Then '清除超过30分钟没有操作的登录信息      UserTable.DeleteFor("ActiveTime < #" & Date.Now.AddMinutes(-30) & "#")      ClearTime = Date.Now()  End If  Dim wb As New  weui  '身份验证  Dim UserName As String  Dim Password As String  Dim UserID As String  If e.Path = "logon.htm"  '验证用户名和密码      If e.PostValues.ContainsKey("username") AndAlso e.PostValues.ContainsKey("password")  Then          Dim Verified As Boolean  '用于标记用户是否通过了身份验证          UserName = e.PostValues("username")          Password = e.PostValues("password")          If  UserName = "张三" AndAlso  Password = "888" Then   '实际使用的时候,请改为从数据库读取用户名和密码进行比较              Verified  = True          ElseIf Username =  "李四" AndAlso  Password="999" Then              Verified  = True          End If          If Verified Then              UserID = Rand.NextString(16) '生成随机用户ID              UserName = EncryptText(UserName,"123","123") '将用户名加密.              Dim dr As DataRow =  UserTable.Find("UserName = '" & UserName & "'")              If  dr IsNot Nothing Then '如果是重复登录,删除以前的登录信息                  dr.Delete()              End  If              dr = UserTable.AddNew()              dr("UserName") = UserName              dr("UserID") = UserId              dr("ActiveTime") = Date.Now '记录登录时间              wb.AppendCookie("username",UserName) '将用户名和UserID写入cookie              wb.AppendCookie("userid",UserID)              wb.InsertHTML("<meta http-equiv='Refresh' content='0; url=/default.htm'>")  '直接跳转到首页              e.WriteString(wb.Build) '生成网页              Return  '必须的          End If      End  If  Else '其它页面从Cookie提取登录信息进行验证      UserName = e.Cookies("username")   '从cookie中获取用户名      UserID = e.Cookies("userid")   '从cookie中获取 随机ID      Dim  dr As  DataRow = UserTable.Find("UserName = '" & UserName & "'")      If dr IsNot Nothing AndAlso dr("UserID") = UserID Then  '如果通过验证,更新活动时候,继续访问其它页面.          dr("ActiveTime") = Date.Now '更新活动时间      Else  '如果验证失败          wb.InsertHTML("<meta http-equiv='Refresh' content='0; url=/logon.htm'>")  '那么直接跳转到登录页面          e.WriteString(wb.Build) '生成网页          Return  '必须的      End  If  End If  '开始生成网页  Select Case e.path       Case "logon.htm" '登录页面          wb.AddPageTitle("","pageheader","销售系统","由湛江辉迅基于Foxtable开发")          If e.PostValues.ContainsKey("username") AndAlso e.PostValues.ContainsKey("password")  Then  '判断是否是验证失败后的重新登录              wb.AddTopTips("","toptip1","用户名或密码错误!").msec = 2000  '如果用户通过登录按钮访问,则给用户一个2秒的提示.            End If          wb.AddForm("","form1","logon.htm")          With  wb.AddInputGroup("form1","ipg1")              .AddInput("username","户名","text")              .AddInput("password","密码","password")          End  With          With wb.AddButtonGroup("form1","btg1",True)              .Add("btn1", "登录", "submit")          End  With      Case "exit.htm"  '退出登录          wb.DeleteCookie("username") '清除cookie中原来的用户名和UserID          wb.DeleteCookie("UserID")          wb.InsertHTML("<meta http-equiv='Refresh' content='0; url=/logon.htm'>")  '然后直接跳转到登录页面      Case "", "default.htm"  '首页          wb.AddPageTitle("","pageheader","销售系统","由湛江辉迅基于Foxtable开发")          With  wb.AddGrid("","g1")              .Add("c1","增加订单", "./images/button.png").Attribute = "onclick='javascript:alert(""你单击了我!"")'"              .Add("c2","客户管理", "./images/cell.png", "http://www.foxtable.com")              .Add("c3","销售统计", "./images/toast.png", "http://www.foxtable.com")              .Add("c4","Dialog", "./images/dialog.png", "http://www.foxtable.com")              .Add("c5","Progress", "./images/progress.png", "http://www.foxtable.com")              .Add("c6","Msg", "./images/msg.png", "http://www.foxtable.com")              .Add("c7","Article", "./images/article.png", "http://www.foxtable.com")              .Add("c8","ActionSheet", "./images/actionSheet.png", "http://www.foxtable.com")              .Add("c9","Icons", "./images/icons.png", "http://www.foxtable.com")              .Add("c10","Panel", "./images/panel.png", "http://www.foxtable.com")              .Add("c11","Tab", "./images/tab.png", "http://www.foxtable.com")              .Add("c12","退出", "./images/exit.png", "exit.htm")  '退出登录          End  With  End Select  e.WriteString(wb.Build) '生成网页 |

提示：用户表以及最近一次清理过期信息的时间，用静态变量保存，关于静态变量，参考：[使用静态变量](http://www.foxtable.com/webhelp/scr/1061.htm)

## 使用AJAX


### 使用AJAX函数

使用AJAX函数


**使用AJAX函数**

AJAX可以实现网页和后台服务器的即时交互。

一般用户使用AJAX可能会有一些困难，所以我们提供了一些简单的AJAX函数，使得大家可以快速上手。

例如通过setAjaxOptions函数，我们只需一行代码，就
能实现动态列表项目的功能。

当然，如果你熟悉JavaScript和AJAX，完全可以自行编码实现相关函数，以获得更好的灵活性。

### setAjaxOptions

setAjaxOptions


**setAjaxOptions**

setAjaxOptions是我们在weui.me.js中扩展的一个函数，用于根据后台数据动态生成列表项目，语法：

setAjaxOptions(SelectID, URL, ID1, ID2, ..., asyn)

|  |  |
| --- | --- |
| SelectID | 列表输入框的ID。 |
| URL | 后台用于生成列表项目的网页。 |
| ID1, ID2, ... | 输入框ID，个数不限，这些输入框的内容将以POST方式传递给后台，后台据此生成列表项目。 |
| asyn | 逻辑型，可选参数，是否异步执行，默认为true，如果要同步执行，请设置为false。  注意是true和false，不是True和False。 |

例如：

setAjaxOptions('品牌','getBrands.htm','国家',false)

表示将"国家"输入框的值，传递给后台的网页getBrands.htm，为"品牌"输入框生成列表项目
，注意这里的"国家"和"品牌"，都是输入框的ID。

后台的处理代码可以非常的简单，例如根据收到的国家名称，从数据表提取品牌，回传给客户端即可：

Dim
pps As
String =
DataTables("汽车").GetComboListString("品牌","国家='"
& e.PostValues("国家")
& "'")
e.WriteString(pps)

**示例一**

假定后台有个名为"汽车"的数据表：

前台的录入界面如下图，希望选择不同的国家后，能自动根据后台数据表的内容，列出该国的汽车品牌供选择：

看起来比较复杂，其实非常简单，HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","动态列表")
            With .AddSelect("国家","国家","|中国|德国|日本")
                .Attribute =
"onchange=""setAjaxOptions('品牌','getBrands.htm','国家',false)"""
            End With
            .AddSelect("品牌","品牌","")
        End With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
        e.WriteString(wb.Build)
'生成网页
    Case  "getBrands.htm"
        Dim
pps As
String = DataTables("汽车").GetComboListString("品牌","国家='"
& e.PostValues("国家")
& "'")
        e.WriteString(pps)
End
Select

**示例二**

根据setAjaxOptions可以做出级联列表的效果，假定后台有个表A：

希望前台的输入页面，选择不同的型号，能自动列出对应的规格供选择，选择某个规格后，还能自动列出对应的颜色供选择：

HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim wb
As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","动态列表")
            With .AddSelect("xh","型号","|"
& DataTables("表A").GetComboListString("型号"))
                .Attribute =
"onchange=""setAjaxOptions('gg','getProducts.htm','xh',false)"""
            End
With
            With .AddSelect("gg","规格","")
                .Attribute =
"onchange=""setAjaxOptions('ys','getProducts.htm','xh','gg',false)"""
            End
With
            .AddSelect("ys","颜色","")
        End With
        With wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
        e.WriteString(wb.Build)
'生成网页
    Case  "getProducts.htm"
        Dim
vals As
String
        If
e.PostValues.Count
= 1 Then
            vals  =
"|" &
DataTables("表A").GetComboListString("规格","型号='"
& e.PostValues("xh")
& "'")
        ElseIf
e.PostValues.Count
= 2 Then
            Dim
Filter As
String =  "型号='"
& e.PostValues("xh")
&
"' And
规格='"
& e.PostValues("gg")
& "'"
            vals =
"|" &
DataTables("表A").GetComboListString("颜色",
Filter)
        End If
        e.WriteString(vals)
End
Select

注意这里型号输入框的ID是"xh"，规格输入框的id是"gg"，setAjaxOptions通过ID来提交输入框的值，例如：

setAjaxOptions('ys','getProducts.htm','xh','gg',false)

服务端也是通过ID来获取对应输入框的值：e.PostValues("xh")

### submitAjaxForm

submitAjaxForm


**submitAjaxForm**

submitAjaxForm用于不刷新当前页面的情况下提交表单数据。

submitAjaxForm(id,func,asyn)

|  |  |
| --- | --- |
| ID | 表单ID。 |
| func | 回调函数名，收到服务器返回信息后，会调用此函数进行处理。 |
| asyn | 逻辑型，可选参数，是否异步执行，默认为true，如果要同步执行，请设置为false。  注意是true和false，不是True和False。 |
| toast | 可选参数，一个toast的ID，此toast用于显示表单数据和文件的上传进度。 |

例如：

submitAjaxForm('form1','myfunction');

表示异步提交表单form1，由myfunction函数负责接收处理服务器返回的数据。

当asyn参数为False，也可以不指定func参数，此时submitAjaxForm函数将返回一个值，此值就是服务器返回的数据，例如：

var result=submitAjaxForm('form1','',false);

表示同步提交表单form1，并将服务器返回的数据保存在变量result中。
注意，这里的func参数设置为""，并不能直接省略。


**一个例子**

这次我们要设计一个录入页面：

录入完成后，单击确定按钮，在服务器成功添加订单后，会提示：

如果单击按钮“否”，可以跳转到其他页面(通常是首页)，如果单击按钮"是"，会自动清除之前已经输入的内容，开始输入下一个订单：

如果输入数据录入不完整，就单击确定按钮，会提示错误：

在错误窗口单击"确定"后，可以继续输入内容再提交：

看起来有点复杂，不过设计起来却一点不复杂。

**设计步骤**

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"ajaxform.js"，文件内容为：

function myfunction(){
    var result = submitAjaxForm('form1','',false);
    if (result =='OK') {show('dlg1')}
    else {showDialog('dlg2','错误',result)}
}

这个文件定义了一个JS函数，用于接收服务器返回的值，如果值为"OK"，显示对话框"dlg1"，否则显示对话框"dlg2",通过"dlg2"显示服务器返回的错误信息。

注意

a、JavaScript(JS)中的函数名、变量名、字符比较等等，都是区分大小写的，所以"ok"不等于"OK"，"returnval"不等于"returnVal"。
b、记得用utf-8格式存盘，否则中文乱码。

2、现在编写HttpRequest事件代码， 用页面"addnew.htm"用于输入数据，用页面"handle.htm"用于接收用户提交的数据：

Select
Case e.Path
    Case "addnew.htm"
        Dim wb
As New
weui
        wb.AddForm("","form1","handle.htm") '指定接收表单数据的的页面为handle.htm
        With wb.AddInputGroup("form1","ipg1","新增订单")
            .AddInput("客户","客户","text")
            .AddInput("日期","日期","date")
            .AddInput("产品","产品","text")
            .AddInput("数量","数量","number")
            .AddInput("单价","单价","number").Step
= 0.1
        End With
        With wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"button").Attribute=
"onclick='myfunction()'"
        End With
        With wb.AddDialog("","dlg1",
"提示","增加订单成功,是否继续增加?")
'增加订单成功提示框
            .AddButton("btnYes","是").Attribute
= "onclick='form1.reset()'"
            .AddButton("btnNo","否","http://www.foxtable.com").Kind
= 1
        End With
        With wb.AddDialog("","dlg2",
"错误","")
'增加订单失败提示框
            .AddButton("btnOK","确定")
        End With
        wb.AppendHTML("<script
src='./lib/ajaxform.js'></script>")
'引入脚本文件
        e.WriteString(wb.Build)
    Case "handle.htm"
        Dim nms()
As String =
{"客户","日期","产品","数量","单价"}
        For Each
nm
As String In
nms
            If
e.PostValues.ContainsKey(nm) =
False
Then
                e.WriteString("请输入"
& nm
& "!")
'返回错误消息
                Return
'必须返回
            End If
        Next
        Dim dr
As DataRow =
DataTables("订单").AddNew()
        For Each
nm As
String In
nms

dr(nm)
= e.PostValues(nm)
        Next
        dr.Save()
        e.WriteString("OK")
'返回增加成功消息
End
Select

### submitAjaxFileds

submitAjaxFileds


**submitAjaxFileds**

submitAjaxFiled用于发送表单中部分输入框的值，语法：

submitAjaxFileds(url,func,id1,id2...,asyn)

|  |  |
| --- | --- |
| url | 接收数据的目标网页 |
| func | 回调函数名，收到服务器返回信息后，会调用此函数进行处理。 |
| id1,id2... | 输入框ID，个数不限。 |
| asyn | 逻辑型，可选参数，是否异步执行，默认为true，如果要同步执行，请设置为false。  注意是true和false，不是True和False。 |

例如：

submitAjaxFileds('getCodes.htm','setCodes','province','county');

表示将ID为"province"和"county"两个输入框的值
，异步提交到后台的"getCodes.htm"页面处理，
服务器返回的数据由函数setCodes函数负责接收和处理。

当asyn参数为False，也可以不指定func参数，此时submitAjaxFileds函数将返回一个值，此值就是服务器返回的数据，例如：

var result=submitAjaxFileds("valid.htm","","产品","数量","折扣",false);

表示将产品、数量和折扣三个输入框的值提交到后台的"valid.htm"页面处理，并将服务器返回的结果存储在变量result中。
注意，这里的func参数设置为""，并不能直接省略。

**一个例子**

假定要求设计一个下图所示的输入页面，选择省市后，自动列出所有该省所有的县供选择，选择县之后，自动输入该县的区号和邮编：

当然，要完成这个设计，首先得在后台准备一个"行政区域"数据表：

设计步骤

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"ajaxform.js"，文件内容为：

function setCodes(){
    var result= submitAjaxFileds('getCodes.htm','','province','county',false);
    if(result){
        var vals=result.split("|");
        if(vals.length==2){

document.getElementById("areacode").value=vals[0];

document.getElementById("postcode").value=vals[1];
        }
    }
}

这个文件定义了一个JS函数，将province(省)和county(县)输入框的值同步发送到服务器，服务区返回的数据的格式为"区号|邮编"，将收到的
数据拆分之后，分别写入区号(areacode)和邮编(postcode)输入框。

2、HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddInputGroup("form1","ipg1","自动输入")
            With .AddSelect("province","省市","|"+DataTables("行政区域").GetComboListString("省市"))
                .Attribute =
"onchange=""setAjaxOptions('county','getCounties.htm','province',false)"""
            End
With
            With .AddSelect("county","县","")
                .Attribute =
"onchange='setCodes()'"
 '调用js函数
            End
With
            .AddInput("areacode","区号","text")
            .AddInput("postcode","邮编","text")
        End With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
        wb.AppendHTML("<script
src='./lib/ajaxform.js'></script>") '引入脚本文件
        e.WriteString(wb.Build)
'生成网页
    Case  "getCounties.htm"
'根据输入的省,获取县市列表
        Dim pps
As String =
DataTables("行政区域").GetComboListString("县市","省市='"
& e.Values("province")
& "'")
        e.WriteString("|"
& pps)
    Case "getCodes.htm"
'根据输入的省和县,获取区号有邮编
        Dim dr
As DataRow
= DataTables("行政区域").Find("省市='"
& e.Values("province")
& "' and
县市='"
& e.values("county")
& "'")
        If
dr IsNot
Nothing Then
           e.WriteString(dr("区号")
& "|"
& dr("邮编"))
        End If
End Select

### sendAjaxJSON

sendAjaxJSON


**sendAjaxJSON**

一般用户可以忽略本节内容。

Foxtable为WeUI扩展了一个名为"sendAjaxJSON"的函数，用于向服务器发送JSON数据，语法：

sendAjaxJSON(data,url,func,asyn)

|  |  |
| --- | --- |
| data | 要发送的数据，可以是一个对象，也可以是一个JSON格式的字符串。 |
| url | 接收数据的目标网页。 |
| func | 回调函数名，收到服务器返回信息后，会调用此函数进行处理。 |
| asyn | 逻辑型，可选参数，是否异步执行，默认为true，如果要同步执行，请设置为false。  注意是true和false，不是True和False。 |

例如：

sendAjaxJSON(val,"json.htm","afterSendJson")

表示将val(JSON数据或对象)异步发送到页面json.htm，由afterSendJson函数负责处理接收到的数据。

当asyn参数为False，也可以不指定func参数，此时sendAjaxJSON函数将返回一个值，此值就是服务器返回的数据，例如：

var result = sendAjaxJSON(val,"json.htm","",false)

表示将将val(JSON数据或对象）同步发送到页面json.htm，将返回值保存在变量result中。

**一个例子**

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"ajaxform.js"，文件内容为：

//发送JSON对象
function sendJsonObject(){
    var obj=new Object();
    obj.name = "舒淇";
    obj.age=39;
    var result = sendAjaxJSON(obj,"json.htm","",false);
    document.getElementById("p1").innerHTML=result;
}

//发送JSON字符串
function sendJsonString(){
    var val= '{"name":"李云龙","age":"36"}'
    var result = sendAjaxJSON(val,"json.htm","",false);
    document.getElementById("p1").innerHTML=result;
}

2、HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim wb
As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddButtonGroup("form1","btg1",True)
'垂直排列
            .Add("btn1",
"发送jason对象","button").Attribute="onclick='sendJsonObject()'"
            .Add("btn2",
"发送jason字符串","button").Attribute="onclick='sendJsonString()'"
        End With
        wb.AppendHTML("<div
id='p1' style='margin:0.5em'></div>") '插入一个div,用于显示服务器返回的数据
        wb.AppendHTML("<script
src='./lib/ajaxform.js'></script>") '引入脚本文件
        e.WriteString(wb.Build)
    Case "json.htm"
        Dim sb
As New
StringBuilder
        Dim jo
As JObject =
JObject.Parse(e.PlainText)
'解析JSON数据
        sb.AppendLine("服务器收到的数据有:<br/>")
        sb.AppendLine("name:"
& jo("name").ToString()
& "<br/>")
        sb.AppendLine("age:"
& jo("age").ToString())
        e.WriteString(sb.ToString())
End
Select

HttpRequest将收到JSON数据以纯文本形式保存在e参数PlainText中，我们需要对其进行解析，参考：[解析JSON](0140.htm)。

此外我们这个例子，直接将服务器返回的数据显示在当前页面中，这个技巧是很实用的，望大家掌握：

### sendAjaxText

sendAjaxText


**sendAjaxText**

Foxtable为WeUI扩展了一个名为"sendAjaxText"的函数，用于向服务器发送纯文本数据，语法：

sendAjaxText(data,url,func,asyn)

|  |  |
| --- | --- |
| data | 要发送的文本数据， |
| url | 接收数据的目标网页。 |
| func | 回调函数名，收到服务器返回信息后，会调用此函数进行处理。 |
| asyn | 逻辑型，可选参数，是否异步执行，默认为true，如果要同步执行，请设置为false。  注意是true和false，不是True和False。 |

例如：

sendAjaxText("getUser","accept.htm","afterGetUser")

表示将字符串"getUser"异步发送到页面accept.htm，由afterGetUser函数负责处理接收到的数据。

当asyn参数为False，也可以不指定func参数，此时sendAjaxText函数将返回一个值，此值就是服务器返回的数据，例如：

var result = sendAjaxText("getUser","accept.htm","",false)

表示将字符串"getUser"同步发送到页面accept.htm，将返回值保存在变量result中。

提示：

HttpRequest的e参数PlainText，用于返回接收到的文本数据。

**一个例子**

这个例子用于演示了如何向服务器发送文本命令，服务器根据收到的文本命令，返回相应的JSON数据或文本数据：

**设计步骤**

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"ajaxform.js"，文件内容为：

function getDate(){
    var result = sendAjaxText("getDate","accept.htm","",false);
    document.getElementById("p1").innerHTML="今天日期:<br/>"
+ result;
}

function getUser(){
    var result = sendAjaxText("getUser","accept.htm","",false);
    var user=JSON.parse(result);
    result="姓名:"
+ user.name + "<br/>" + "年龄:" +
user.age
    document.getElementById("p1").innerHTML=result;
}

2、HttpRequest事件代码：

Select Case
e.Path
    Case
"test.htm"
        Dim wb
As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddButtonGroup("form1","btg1",True)
'垂直排列
            .Add("btn1",
"getUser","button").Attribute="onclick='getUser()'"
            .Add("btn2",
"getDate","button").Attribute="onclick='getDate()'"
        End With
        wb.AppendHTML("<div
id='p1' style='margin:0.5em'></div>")
'插入一个div,用于显示服务器返回的数据
        wb.AppendHTML("<script
src='./lib/ajaxform.js'></script>") '引入脚本文件
        e.WriteString(wb.Build)
'生成网页
    Case "accept.htm"
        Select
e.PlainText
            Case
"getUser" '发送jason数据
                Dim
v As
String =
"{""name"":""李云龙"" , ""age"":""38""}"
                e.WriteString(v)
            Case "getDate"
'发送纯文本
                e.Writestring(CUDate(Date.Today))
        End
Select
End
Select

### 再谈表单验证

再谈表单验证


**再谈表单验证**

多数时候，我们可以用submitAjaxForm将表单数据发送给服务器，由服务器对输入结果进行验证处理，参考:[submitAjaxForm](0101.htm)

不过如果表单中包括文件上传组件，那么需要比较长的时间，才能将所有数据和文件上传到服务器，验证通过也罢，如果验证失败，时间的浪费是很可惜的。

其实验证通常只是针对数据，而不是针对文件，我们可以用submitAjaxFileds将需要验证的数据发送到服务器，验证成功，才提交整个表单数据。

**一个例子**

希望设计一个下图所示的输入界面，当用户单击提交按钮的时候，可以先将产品、数量和折扣三列的数据提交到服务器，由服务器进行验证，验证通过后，再提交整个表单的数据和文件：

**知识准备**

用户单击确定按钮提交表单的时候，会触发表单的onsubmit事件，这个事件如果返回false，将终止提交表单。
例如下面的定义表单的代码，表示提交表单前，先执行validit函数:

wb.AddForm("","form1","addnew.htm").Attribute="onsubmit='return validit()'"

我们在validit函数中将需要验证的数据，用submitAjaxFileds将要验证的数据提交给服务器，根据服务器返回的结果，决定是否正常提交表单。

**设计步骤**

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"ajaxform.js"，文件内容为：

function
validit(){
    var result=submitAjaxFileds("valid.htm","","产品","数量","折扣",false);
    if(result=="OK"){
        return true;
    }
    else{
        showTopTips("toptip1",result,2500);
        return false;
    }
}

这段js代码在提交表单之前执行，将产品、数量和折扣提交到服务器的valid.htm页面进行验证，如果服务器返回OK，则允许提交表单，否则显示一个错误提示，并禁止提交表单。

2、HttpRequest事件代码：

Select
Case e.Path
    Case
"addnew.htm"
        If e.PostValues.Count
= 0
Then
            Dim wb
As New
weui
            wb.AddTopTips("","toptip1","")
'用于显示动态错误提示
            wb.AddForm("","form1","addnew.htm").Attribute="onsubmit='return
validit()'"
            With wb.AddInputGroup("form1","ipg1","新增订单")
                .AddSelect("产品","产品","|PD01|PD02|PD03")
                .AddInput("数量","数量","number")
                .AddInput("单价","单价","number").Step
= 0.1
                .AddInput("折扣","折扣","number").Step
= 0.01
                With .AddUploader("up1","图片",True)
                    .TextPosition =
0
'标题靠左
                    .AddImage("./images/shuqi2.jpg")
                End
With
            End
With
            With wb.AddButtonGroup("form1","btg1",True)
                .Add("btn1",
"确定","submit")
            End
With
            wb.AppendHTML("<script
src='./lib/ajaxform.js'></script>")
'引入脚本文件
            e.WriteString(wb.Build)
        Else
            Dim sb
As New
StringBuilder

sb.AppendLine("<meta
name='viewport' content='width=device-width,initial-scale=1,user-scalable=1'>")
            sb.AppendLine("我已经收到您提交的数据和文件")
             e.WriteString(sb.Tostring)
        End
If
    Case
"valid.htm"
        If e.PostValues.ContainsKey("产品")
AndAlso e.PostValues.ContainsKey("数量")
AndAlso e.PostValues.ContainsKey("折扣")
Then
            If e.PostValues("产品")
= "PD01" AndAlso
e.PostValues("数量")
> 1000
Then
                e.WriteString("PD01库存只剩1000啦!")
            ElseIf e.PostValues("产品")
= "PD01" AndAlso
e.PostValues("折扣")
> 0.1
Then
                e.WriteString("PD01的最大允许折扣为0.1哦")
            Else
                e.WriteString("OK")
            End
If
        Else
            e.WriteString("请完整输入订单内容!")

End
If
End
Select

### 接收完整的页面

接收完整的页面


**接收完整的页面**

使用Ajax可以从服务器接收完整的页面，并将接收到的页面显示在当前页面中。

例如我们希望设计一个下图所示的统计页面，用户单击统计按钮后，能直接在当前页面显示统计结果：

**设计步骤：**

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"ajaxform.js"，文件内容为：

function tongji(){
    var result = submitAjaxForm('form1','',false);
    document.getElementById("p1").innerHTML=result;
}

2、HttpReqquest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","tongji.htm")
        With wb.AddInputGroup("form1","ipg1","销售统计")
            .AddSelect("水平分组","水
平分组","产品|客户|雇员")
            .AddSelect("垂直分组","垂直分组","产品|[客户]|雇员")
            .AddSelect("统计列","统计列","数量|金额")
        End
With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"统计",
"button").Attribute=
"onclick= 'tongji()'"
        End
With
        wb.AppendHTML("<div
id='p1' style='margin:0.5em'></div>")
'插入一个div,用于显示服务器返回的
页面
        wb.AppendHTML("<script
src='./lib/ajaxform.js'></script>")
'引入脚本文件
        e.WriteString(wb.Build)
    Case "tongji.htm"
        Dim
wb As New
weui
        If e.PostValues.ContainsKey("垂直分组")
AndAlso e.PostValues.ContainsKey("水平分组")
AndAlso e.PostValues.ContainsKey("统计列")
Then
            Dim
b As
New
CrossTableBuilder("统计表1",DataTables("订单"))
            b.HGroups.AddDef(e.PostValues("水平分组"))
            b.VGroups.AddDef(e.PostValues("垂直分组"))
            b.Totals.AddDef(e.PostValues("统计列"))
            wb.AddTable("","Table1").CreateFromDataTable(b.Build(True))
        Else
            wb.InsertHTML("请按输入分组列和统计列!")
        End If
        e.WriteString(wb.Build)
End
Select

分页显示

我们也可以分开两个Page，一个Page用于统计设置，一个Page用于显示统计结果，两个Page可以来切换：

设计起来也很简单：

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"ajaxform.js"，文件内容为：

function tongji2(){
    var result = submitAjaxForm('form1','',false);
    document.getElementById("page2").innerHTML=result;
    hide('page1');
    show('page2');
}

2、HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim
wb As New
weui
        wb.AddPage("","page1")
'增加两个page
        wb.AddPage("","page2")
        wb.AddForm("page1","form1","tongji.htm")
'表单显示在第一个页面
        With wb.AddInputGroup("form1","ipg1","销售统计")
            .AddSelect("水平分组","水品分组","产品|客户|雇员")
            .AddSelect("垂直分组","垂直分组","产品|[客户]|雇员")
            .AddSelect("统计列","统计列","数量|金额")
        End With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"统计",
"button").Attribute=
"onclick= 'tongji2()'"
        End
With
        wb.AppendHTML("<script
src='./lib/ajaxform.js'></script>")
'引入脚本文件
        e.WriteString(wb.Build)
    Case
"tongji.htm"
        Dim
wb As New
weui
        If e.PostValues.ContainsKey("垂直分组")
AndAlso e.PostValues.ContainsKey("水平分组")
AndAlso e.PostValues.ContainsKey("统计列")
Then
            Dim
b As
New
CrossTableBuilder("统计表1",DataTables("订单"))
            b.HGroups.AddDef(e.PostValues("水平分组"))
            b.VGroups.AddDef(e.PostValues("垂直分组"))
            b.Totals.AddDef(e.PostValues("统计列"))
            wb.AddTable("","Table1").CreateFromDataTable(b.Build(True))
        Else
            wb.InsertHTML("请按输入分组列和统计列!")
        End If
        With
wb.AddButtonGroup("","btg1",True)
            .Add("btn2",
"重新统计",
"button").Attribute=
"onclick =""hide('page2');show('page1')"""
        End
With
        e.WriteString(wb.Build)
End
Select

### 使用回调函数

使用回调函数


**使用回调函数**

一般用户可以忽略本节的内容。

我们前面关于AJAX函数的示例，采用的都是同步执行方式，只有获得服务器返回的数据，才能进行其他操作。

所有的AJAX函数都可以异步执行，异步执行的好处是在等待服务器响应的过程中，可以进行其他操作，坏处是在操作过程中，你看到的数据，可能并不是最新的。

要异步执行AJAX函数，省略asyn参数即可。

除了setAjaxOptions参数，其他AJAX函数在异步执行的时候，都必须定义一个回调函数，客户端在收到服务器返回的数据后，将调用此函数。

所有的回掉函数都必须定义一个参数，这个参数表示服务器返回的值，例如：

function afterSendJson(result){
    document.getElementById("p1").innerHTML=result;
}

唯一的参数result表示服务器返回的数据，上面代码的意思就是：将服务器返回的数据显示在id为"p1"的元素中。

我们以sendAjaxJSON为例，介绍一下如何使用回掉函数，该函数的语法为：

sendAjaxJSON(data,url,func,asyn)

|  |  |
| --- | --- |
| data | 要发送的数据，可以是一个对象，也可以是一个JSON格式的字符串。 |
| url | 接收数据的目标网页。 |
| func | 回调函数名，收到服务器返回信息后，会调用此函数进行处理。 |
| asyn | 逻辑型，可选参数，是否异步执行，默认为true，如果要同步执行，请设置为false。  注意是true和false，不是True和False。 |

例如：

sendAjaxJSON(val,"json.htm","afterSendJson")

表示将val(JSON数据或对象)异步发送到页面json.htm，由afterSendJson函数负责处理接收到的数据。

**一个例子**

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"ajaxform.js"，文件内容为：

//异步发送对象
function sendJsonObjectAsyn(){
    var obj=new Object();
    obj.name = "hehui";
    obj.age=39;
    sendAjaxJSON(obj,"json.htm","afterSendJson"); //afterSendJson为发送完成后要执行的对象
}

//异步发送JSON字符串
function sendJsonStringAsyn(){
    var val= '{"name":"李云龙","age":"36"}';
    sendAjaxJSON(val,"json.htm","afterSendJson");//afterSendJson为发送完成后要执行的对象
}

//显示服务器返回的数据
function afterSendJson(result){
    document.getElementById("p1").innerHTML=result;
}

2、HttpRequest事件代码：

Select
Case e.Path
    Case "test.htm"
        Dim wb
As New
weui
        wb.AddForm("","form1","test.htm")
        With wb.AddButtonGroup("form1","btg1",True)
'垂直排列
            .Add("btn1",
"发送jason对象","button").Attribute="onclick='sendJsonObjectAsyn()'"
            .Add("btn2",
"发送jason字符串","button").Attribute="onclick='sendJsonStringAsyn()'"
        End With
        wb.AppendHTML("<div
id='p1' style='margin:0.5em'></div>") '插入一个div,用于显示服务器返回的数据
        wb.AppendHTML("<script
src='./lib/ajaxform.js'></script>") '引入脚本文件
        e.WriteString(wb.Build)
'生成网页
    Case "json.htm"
        Dim sb
As New
StringBuilder
        Dim jo
As JObject =
JObject.Parse(e.PlainText)
        sb.AppendLine("服务器收到的数据有:<br/>")
        sb.AppendLine("name:"
& jo("name").ToString
& "<br/>")
        sb.AppendLine("age:"
& jo("age").ToString)
        e.WriteString(sb.ToString)
End
Select

## 再探Uploader


### 增强Uploader

增强Uploader


**增强Uploader**

从本节开始，我们利用前面介绍的AJAX函数，来扩展一下Uploader组件的功能。

Uploader在默认情况下：

1、再次选择上传文件，会覆盖上次选择好的文件。
2、如果开启了图片删除功能，删除其中一个选择好的图片，那么所有已经选择好的图片都会被删除，需要全部重选。

多数时候，这关系不大，但是如果你需要连续拍摄多张照片上传，是没有办法的，因为每拍摄一张照片，就会覆盖之前拍摄好的照片，当然你也可以事先用手机自带的相机拍摄好多张照片，然后用Uploader选择上传，
不过多少有点不方便。

如果我们将Uploader的Incremental属性设置为True，可以实现：

1、再次选择上传文件，不会覆盖之前上传的文件。
2、如果开启了图片删除功能，可以逐个删除选择好的图片。

但是，在这种情况下，表单默认的提交功能，将不会上传选择好的文件，我们只能用submitAjaxForm函数提交表单，不过代码依旧很简单。

**一个例子**

设计一个下图所示的图片上传窗口，要求:

1、可以如前所述，能重复选择文件，或连续拍摄照片。
2、能删除单个的图片，而不影响其他图片。
3、能在上传过程中，显示"正在上传"。

设计过程：

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"ajaxform.js"，文件内容为：

function submitForm(){
    show("tst1",2000);
    var result = submitAjaxForm('form1','afterSubmit');
}

function afterSubmit(result){
    hide("tst1");
    if (result=='OK') {
        show("tst2");
        location="upload.htm";
    }
    else{
        show("tst3",2000);
    }
}

提示: 这里的submitAjaxForm是通过异步方式运行的，用回调函数接收服务器返回的结果，因为如果用同步方式运行，将无法显示“正在上传”的提示。

2、HttpRequest事件代码：

Select
Case e.Path
    Case "upload.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","receive.htm")
        With wb.AddInputGroup("form1","ipg1","文件上传")
            With .AddUploader("up128","照片",True)
                .AllowDelete =
True '允许删除
                .Incremental =
True '允许
重复选择文件或连续拍照
            End With
        End
With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"button").Attribute=
"onclick='submitForm()'"
 '调用js函数上传
        End
With
        wb.AddToast("","tst1",
"正在上传",1)
        wb.AddToast("","tst2",
"上传成功",0)
        wb.AddToast("","tst3",
"上传失败",0).Icon=
"warn"
        wb.AppendHTML("<script
src='./lib/ajaxform.js'></script>") '引入脚本文件
        e.WriteString(wb.Build)
'生成网页
    Case "receive.htm"
        For
Each key As
String In
e.Files.Keys
            For
Each fln
As String
In e.Files(key)
                e.SaveFile(key,fln,"d:\web\uploadfiles\"
& fln)
'保存接收到的文件
            Next
        Next
        e.WriteString("OK")
End
Select

### 微信内置浏览器问题

微信内置浏览器问题


**微信内置浏览器问题**

微信内置浏览器在页面跳转的时候，似乎存在一些问题。

以上一节的例子为例，在所有独立的浏览器测试都没有问题，但是在微信内置浏览器测试时，发现上传结束后一直显示"上传成功"，并不会重新打开"upload.htm"。

要解决这个问题，可以将代码改为：

function submitForm(){
    show("tst1",2000);
    var result = submitAjaxForm('form1','afterSubmit');
}

function afterSubmit(result){
    hide("tst1");
    if (result=='OK') {
        show("tst2");
        **location="upload.htm?v="+Math.random();**
    }
    else{
        show("tst3",2000);
    }
}

通过在网址后面附加一个随机的get参数，确保浏览器重新加载页面，而不会使用缓存。

### 图片压缩上传

图片压缩上传


**图片压缩上传**

如今手机拍照的分辨率非常高，多数都是千万级别的像素，照片文件动辄好几M。

有时我们并不需要这么高的分辨率，这种高分辨率的照片不仅耽误了上传时间，也增加了服务器的处理负担。

UpLoader提供了两个属性，用于对要上传的照片进行自动压缩处理，这两个属性分别为：

* ScaleWidth
  整数型，用于设置图片压缩后的宽度，单位为像素。
* ScaleHeight
  整数型，用于设置图片压缩后的高度，单位为像素。

如果压缩后图片的长宽比例要厚原图保持一致，那么ScaleWidth和ScaleHeight只能设置一个，另一个由系统按原图长宽比例自动计算得出。

要实现图片的压缩上传，单单设置ScaleWidth或ScaleHeight是不够的，我们还需要将Uploader的Incremental属性设置为True，所以和上一节一样，我们只能用submitAjaxForm函数提交表单，不过代码依旧很简单。

**一个例子**

设计一个下图所示的图片上传窗口，和上一节相比，新增第4点的要求：

1、能重复选择文件，或连续拍摄照片。
2、能删除单个的图片，而不影响其他图片。
3、能在上传过程中，显示"正在上传"。
4、所有图片在上传前，宽度统一压缩到400个像素，高度则按比例压缩。

**设计过程：**

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"ajaxform.js"，文件内容和上一节完全相同：

function submitForm(){
    show("tst1",2000);
    var result = submitAjaxForm('form1','afterSubmit');
}

function afterSubmit(result){
    hide("tst1");
    if (result=='OK') {
        show("tst2");
        location="upload.htm";
    }
    else{
        show("tst3",2000);
    }
}

提示: 这里的submitAjaxForm是通过异步方式运行的，用回调函数接收服务器返回的结果，因为如果用同步方式运行，将无法显示“正在上传”的提示。

2、的HttpRequest事件代码如下，和上一节相比，只是增加了一行代码（加粗显示的这行）而已：

Select
Case e.Path
    Case "upload.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","receive.htm")
        With wb.AddInputGroup("form1","ipg1","文件上传")
            With .AddUploader("up128","照片",True)
                .AllowDelete =
True
'允许删除
                .Incremental =
True
'允许重复选择文件或连续拍照
**.ScaleWidth =
400** **'自动压缩图片宽度为400个像素,高度等比例压缩**

End
With
        End
With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"button").Attribute=
"onclick='submitForm()'"
'调用js函数上传
        End With
        wb.AddToast("","tst1",
"正在上传",1)
        wb.AddToast("","tst2",
"上传成功",0)
        wb.AddToast("","tst3",
"上传失败",0).Icon=
"warn"
        wb.AppendHTML("<script
src='./lib/ajaxform.js'></script>")
'引入脚本文件
        e.WriteString(wb.Build)
'生成网页
    Case "receive.htm"
        For
Each key As
String In
e.Files.Keys
            For
Each fln
As String
In e.Files(key)
                e.SaveFile(key,fln,"d:\web\uploadfiles\"
& fln)
'保存接收到的文件
            Next
        Next
        e.WriteString("OK")
End
Select

### 图片旋转上传

图片旋转上传


**图片旋转上传**

手机可以横着拍照，也可以竖着拍照，但通过手机拍照上传的时候，Uploader并不知道这个照片的拍摄方向。

典型的问题是，在iPhone中竖着拍照上传，Uploader会横过来显示照片，服务端接收到的照片也是横过来的。

为解决这个问题，我们为Uploader增加了一个整数型属性Rotate，用于设置图片的旋转角度，可选值有：

|  |  |
| --- | --- |
| 1 | 顺时钟旋转90° |
| 2 | 顺时钟旋转180° |
| 3 | 顺时钟旋转270° |

通常在iPhone上竖方向拍照上传的时候，需要将Rotate属性设置为1。

要实现图片的旋转上传，单单设置Rotate属性是不够的，我们还需要将Uploader的Incremental属性设置为True，所以和上一节一样，我们只能用submitAjaxForm函数提交表单，不过代码依旧很简单。

**一个例子**

希望图片顺时钟旋转90°上传，并将宽度压缩为400个像素，高度则等比例压缩，设计步骤：

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"ajaxform.js"，文件内容和上一节完全相同：

function submitForm(){
    show("tst1",2000);
    var result = submitAjaxForm('form1','afterSubmit');
}

function afterSubmit(result){
    hide("tst1");
    if (result=='OK') {
        show("tst2");
        location="upload.htm";
    }
    else{
        show("tst3",2000);
    }
}

2、的HttpRequest事件代码如下，和上一节相比，只是增加了一行代码（加粗显示的这行）而已：

Select
Case e.Path
    Case "addnew.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","receive.htm")
        With wb.AddInputGroup("form1","ipg1","文件上传")
            With .AddUploader("up128","照片",True)
                .AllowDelete =
True
'允许删除
                .Incremental =
True
'允许重复选择文件或连续拍照
                .ScaleWidth
= 400
'自动压缩图片宽度为400个像素,高度等比例压缩

**.Rotate =
1** **'顺时钟旋转90°**
            End
With
        End
With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定", "button").Attribute=
"onclick='submitForm()'"
'调用js函数上传
        End
With
        wb.AddToast("","tst1",
"正在上传",1)
        wb.AddToast("","tst2",
"上传成功",0)
        wb.AddToast("","tst3",
"上传失败",0).Icon=
"warn"
        wb.AppendHTML("<script
src='./lib/ajaxform.js'></script>") '引入脚本文件
        e.WriteString(wb.Build)
'生成网页

Case
"receive.htm"
        For
Each key As
String In
e.Files.Keys
            For
Each fln
As String
In e.Files(key)
                e.SaveFile(key,fln,"d:\web\uploadfiles\"
& fln)
'保存接收到的文件
            Next
        Next
        e.WriteString("OK")
End
Select

### 显示上传进度

显示上传进度


**显示上传进度**

本节的任务是在上一节的基础上，加上上传进度显示：

实现起来非常简单：

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"ajaxform.js"，文件内容为：

function submitWithProgress(){
    var result = submitAjaxForm('form1','afterSubmit',true,'tst1');
}


function afterSubmit(result){
    hide("tst1");
    if (result=='OK') {
        show("tst2");
        location="upload.htm";
    }
    else{
        show("tst3",2000);
    }
}

提示：

a、submitAjaxForm函数的第4个参数，用于指定一个Toast的ID，系统将通过这个Toast显示上传进度。
b、这里同样是采用异步上传，所以第三个参数要设置为true(不是True)。

2、HttpRequest事件代码则完全不变(注意JS函数名改了)：

Select
Case e.Path
    Case "upload.htm"
        Dim
wb As New
weui
        wb.AddForm("","form1","receive.htm")
        With wb.AddInputGroup("form1","ipg1","文件上传")
            With .AddUploader("up128","照片",True)
                .AllowDelete =
True
'允许删除
                .Incremental =
True
'允许重复选择文件或连续拍照
            End With
        End
With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"button").Attribute=
"onclick='submitWithProgress()'"
'调用js函数上传
        End With
        wb.AddToast("","tst1",
"正在上传",1)
        wb.AddToast("","tst2",
"上传成功",0)
        wb.AddToast("","tst3",
"上传失败",0).Icon=
"warn"
        wb.AppendHTML("<script
src='./lib/ajaxform.js'></script>")
'引入脚本文件
        e.WriteString(wb.Build)
'生成网页
    Case "receive.htm"
        For
Each key As
String In
e.Files.Keys
            For
Each fln
As String
In e.Files(key)

e.SaveFile(key,fln,"d:\web\uploadfiles\"
& fln)
'保存接收到的文件
            Next
        Next
        e.WriteString("OK")
End
Select

## 使用表格


### 生成表格

生成表格


**生成表格**

腾讯的WeUI样式库并不包括表格，为方便普通用户，Foxtable对此进行了扩展。

**一个例子**

我们先用一个简单的例子，看看如何增加表格，HttpRequest事件代码：

Select Case
e.Path
    Case "table.htm"


Dim wb
As New WeUI
        With
wb.AddTable("","Table1")
            .head.AddRow("部门","姓名","年龄","电话","地址")
'表头
            .body.AddRow("技术部","张三","36","110","中国北京")
'数据
            .body.AddRow("技术部","李四","38","110","中国上海")
            .body.AddRow("技术部","王五","39","110","中国深圳")
            .body.AddRow("生产部","赵六","39","110","中国深圳")
            .body.AddRow("生产部","刘七","39","110","中国深圳")
        End With
        e.WriteString(wb.Build)
End Select

下图是通过手机访问的效果：

**AddTable**

增加表格的语法是：

AddTable(ParentID, ID)

|  |  |
| --- | --- |
| ParentID | 父容器的ID,如果是顶层对象，设置为""即可 |
| ID | 表ID |

**AddRow**

表格有三个对象，分别为Head(表头)、Body（表体）、Foot（表尾），这三个对象都有AddRow方法，用于增加行。
AddRow方法的参数就是新增行各列的值。
AddRow还可以直接用数组或集合作为参数，非常方便：

Dim
vals() As
String = {"生产部","刘七","39","110","中国深圳"}
.body.AddRow(vals)

**Class和Attribute**

表有Class和Attribute属性。
行只有Attribute属性，可通过Attribute属性设置其Class。

例如将HttpRequet事件代码设置为：

Select
Case e.Path
    Case "table.htm"


Dim wb
As New WeUI
        wb.AppendHTML("<style>.mark{background-color:red;
color:white;}</style>", True)
'添加样式
        With wb.AddTable("","Table1")
            .Attribute=
"border='2'"
            .head.AddRow("部门","姓名","年龄","电话","地址")

            .body.AddRow("技术部","张三","36","110","中国北京")
            .body.AddRow("技术部","李四","38","110","中国上海")
            .body.AddRow("技术部","王五","39","110","中国深圳").Attribute
= "class='mark'"
            .body.AddRow("生产部","赵六","39","110","中国深圳")
            .body.AddRow("生产部","刘七","39","110","中国深圳")
        End With
        e.WriteString(wb.Build)
End
Select

下图是通过手机访问的效果，表的边框加厚了，第三行变成了红底白字：

### 多层表头

多层表头


**多层表头**

使用WeUI框架，不需要任何技巧，即可实现多层表头。

**一个例子**

HttpRequest事件代码：

Select
Case e.Path
    Case "table.htm"


Dim wb
As New WeUI
        With
wb.AddTable("","Table1")
            .head.Addrow("部门","姓名","信息","信息","信息")
            .head.AddRow("部门","姓名","年龄","电话","地址")
            .body.AddRow("技术部","张三","36","110","中国北京")
            .body.AddRow("技术部","李四","38","110","中国上海")
            .body.AddRow("技术部","王五","39","110","中国深圳")
            .body.AddRow("生产部","赵六","39","110","中国深圳")
            .body.AddRow("生产部","刘七","39","110","中国深圳")
        End With
        e.WriteString(wb.Build)
End
Select

这是在手机上的显示效果：

原理很简单，正常填入表头各单元格的值，Foxtable会自动合并表头中内容相同的单元格。

### 合并模式

合并模式


**合并模式**

使用WeUI框架，实现合并模式是很简单的。

**一个例子**

HttpRequest事件代码：

Select Case
e.Path
    Case "table.htm"


Dim wb
As New WeUI
        With
wb.AddTable("","Table1")
            .MergeCols =
2 '合并左边2列
            .head.Addrow("国家","金属","类型","数量")
            .body.AddRow("美国","白银","出口","70")
            .body.AddRow("美国","白银","进口","321")
            .body.AddRow("美国","黄金","出口","78")
            .body.AddRow("美国","黄金","进口","789")
            .body.AddRow("中国","白银","出口","380")
            .body.AddRow("中国","白银","进口","809")
            .body.AddRow("中国","黄金","出口","289")
            .body.AddRow("中国","黄金","进口","668")
        End With
        e.WriteString(wb.Build)
End
Select

这是通过手机访问的效果：

提示：MergeCols用于指定要合并的列数，从左边第一列开始计算。

### 显示行号

显示行号


**显示行号**

通过表格的RowHead属性，可以左边多少列作为行头，行头通常用于显示行号。

一个例子：

Select
Case e.Path
    Case "table.htm"


Dim wb
As New WeUI
        With
wb.AddTable("","Table1")
            .RowHead =
1
'左边第一列作为行头
            .head.AddRow("","部门","姓名","年龄","电话","地址")
'表头,行号列标题为空
            .body.AddRow("1","技术部","张三","36","110","中国北京")
'数据
            .body.AddRow("2","技术部","李四","38","110","中国上海")
            .body.AddRow("3","技术部","王五","39","110","中国深圳")
            .body.AddRow("4","生产部","赵六","39","110","中国深圳")
            .body.AddRow("5","生产部","刘七","39","110","中国深圳")
        End With
        e.WriteString(wb.Build)
End
Select

下图是再手机上显示的效果：

### 设置列宽

设置列宽


**设置列宽**

默认情况下，系统会自动分配列宽。

通过ColWidth属性，可以指定列宽，这是一个字符型的属性，可以一次设置多列的宽度。

**一个例子**

下面的HttpRequest事件代码，将第一列(行号)的宽度设置为12px，第三列（姓名）的宽度设置为120px：

Select Case
e.Path
    Case "table.htm"


Dim wb
As New WeUI
        With
wb.AddTable("","Table1")
            .RowHead =
1
            .ColWidth =
"12px,,120px"
'设置列宽
            .head.AddRow("","部门","姓名","年龄","电话","地址")

            .body.AddRow("1","技术部","张三","36","110","中国北京")

            .body.AddRow("2","技术部","李四","38","110","中国上海")
            .body.AddRow("3","技术部","王五","39","110","中国深圳")
            .body.AddRow("4","生产部","赵六","39","110","中国深圳")
            .body.AddRow("5","生产部","刘七","39","110","中国深圳")
        End With
        e.WriteString(wb.Build)
End
Select

这是在手机上的显示效果：

### 高亮显示行列

高亮显示行列


**高亮显示行列**

在手机中显示查阅一个大表格是很痛苦的，为解决这个问题，Foxtable提供了高亮显示行列的功能。

点击行号，会高亮显示对应的行：

点击列标题，会高亮显示对应的列：

点击某单元格，会高两显示对应的行列：

Foxtable为表提供了一个整数型的Highlight属性，可以用来关闭高亮显示功能：

|  |  |
| --- | --- |
| 值 | 说明 |
| 0 | 高亮显示行列 |
| 1 | 仅高亮显示行 |
| 2 | 仅高亮显示列 |
| -1 | 关闭高亮显显示 |

**一个例子**

下面的HttpRequest事件代码关闭了表格的高亮显示功能：

Select
Case e.Path
    Case
"table.htm"


Dim wb
As New WeUI
        With wb.AddTable("","Table1")
            .Highlight = -1
 '关闭高亮显示功能
            .RowHead =
1
            .head.AddRow("","部门","姓名","年龄","电话","地址")
            .body.AddRow("1","技术部","张三","36","110","中国北京")
            .body.AddRow("2","技术部","李四","38","110","中国上海")
            .body.AddRow("3","技术部","王五","39","110","中国深圳")
            .body.AddRow("4","生产部","赵六","39","110","中国深圳")
            .body.AddRow("5","生产部","刘七","39","110","中国深圳")
        End
With
        e.WriteString(wb.Build)
End
Select

### 交替行背景颜色

交替行背景颜色


**交替行背景颜色**

除了上一节介绍的高亮显示行列功能，我们还可以设置交替行背景颜色，只是此功能默认是关闭的。

表有一个整数型的Alternate属性，用于设置每多少行显示一个不同背景颜色的行。

一个例子

Select
Case e.Path
    Case "table.htm"


Dim wb
As New WeUI
        With
wb.AddTable("","Table1")
            .Highlight = -1
'关闭高亮显示
            .Alternate =
2
'每两行显示一个不同背景颜色的行
            .RowHead =
1
            .head.AddRow("","部门","姓名","年龄","电话","地址")

            .body.AddRow("1","技术部","张三","36","110","中国北京")

            .body.AddRow("2","技术部","李四","38","110","中国上海")
            .body.AddRow("3","技术部","王五","39","110","中国深圳")
            .body.AddRow("4","生产部","赵六","39","110","中国深圳")
            .body.AddRow("5","生产部","刘七","39","110","中国深圳")
        End With
        e.WriteString(wb.Build)
End
Select

这是在手机上显示的效果：

### 逐个单元格添加

逐个单元格添加


**逐个单元格添加**

前面的例子，都是整行整行地向表中增加行，简单方便。

如果需要更多的控制，可以逐个单元格添加。

**一个例子**

HttpRequest事件代码设置为：

Select
Case e.Path
    Case "table.htm"


Dim wb
As New WeUI
        wb.AppendHTML("<style>.mark{background-color:red;
color:white;}</style>", True)
'添加样式
        With wb.AddTable("","Table1")
            .head.AddRow("部门","姓名","年龄","电话","地址")
            .body.AddRow("技术部","张三","36","110","中国北京")
'整行增加
            With .body.AddRow()

                .AddCell("技术部")
'逐个单元格增加
                .AddCell("李四","class='mark'")
'第二个参数用于设置单元格的Attribute属性
                .AddCells("38","110")
'用AddCells可以一次添加多个单元格
                .AddCell("中国上海")
            End With
            .body.AddRow("技术部","王五","39","110","中国深圳")
'整行增加
        End With
        e.WriteString(wb.Build)
End
Select

下图是通过手机访问的显示效果，一个单元格变成了红底白字：

**AddCell**

AddCell用于向行中添加单元格，语法：

AddCell(Value)
AddCell(Value, Attribute)

|  |  |
| --- | --- |
| Value | 要在单元格显示的内容。 |
| Attribute | 可选参数，用于设置单元格元素的属性 |

提示：表有Class和Attribute属性；行只有Attribute属性；单元格没有任何属性，但是通过AddCell的Attribute参数可以设置Attribute属性。
 **AddCells**

AddCells用于向行中一次添加多个单元格，语法：

AddCells(Values)
AddCells(Value1,Value2,Value3...)

|  |  |
| --- | --- |
| Values | 一个包括各单元格值的集合或数组。 |
| Value1,Value2,Value3 | 各单元格的值。 |

### 由Table自动生成

由Table自动生成


**由Table自动生成**

WeUI可以根据Foxtable中的Table自动生成网页。

**一个例子**

Select
Case e.Path
    Case "table.htm"


Dim wb
As New WeUI

With
wb.AddTable("","Table1")
            .CreateFromTable(Tables("表名"),True)
        End With
        e.WriteString(wb.Build)
End
Select

我用一个有多层表头的Table测试，用上面的代码生成了下图所示的网页：

生成上面的表其实只用了一行代码，这就是使用框架的优势：

.CreateFromTable(Tables("表名"),True)

提示：

自动生成的网页，逻辑列中的True倍符号●代替，False被符号○代替，你可以自定义符号，你可以用BooleanSymbol属性自定义符号，例如：

With
wb.AddTable("","Table1")
     .BooleanSymbol= "√×"
    .CreateFromTable(Tables("订单"))
End With

CreateFromTable

CreateFromTable用于根据Foxtable中的Table自动生成网页，语法：

CreateFromTable(Table)
CreateFromTable(Table,RowNum)
CreateFromTable(Table,RowNum,OnlyVisible)
CreateFromTable(Table,RowNum,Cols)
CreateFromTable(Table,RowNum,Col1,Col2,Col3...)

|  |  |
| --- | --- |
| 参数 | 说明 |
| Table | Foxtable中的Table。 |
| RowNum | 逻辑型，是否显示行号。 |
| OnlyVisible | 逻辑型，是否只包括可见列。 |
| Cols | 一个包括所有要显示列的列名的集合或数组，例如：    Dim Cols() As String  =  "产品,客户,日期,数量".Split(",")  .CreateFromTable(Tables("订单"),True,Cols) |
| Col1, Col2, Col3 | 字符型，用于指定要显示的列，例如：    .CreateFromTable(Tables("订单"),True,"产品","客户","日期","数量") |

### 由DataTable自动生成

由DataTable自动生成


**由DataTable自动生成**

WeUI可以根据Foxtable中的DataTable自动生成网页。

**一个例子**

Select
Case e.Path
    Case "table.htm"

Dim wb
As New WeUI
        With
wb.AddTable("","Table1")
            '按日期顺序列出客户CS01的订单,仅显示产品/数量/单价/日期/审核等五列
            .CreateFromDataTable(DataTables("订单"),False,"客户='CS01'","日期
desc","产品","单价","数量","日期","审核")
        End With
        e.WriteString(wb.Build)
End
Select

这是通过手机访问的效果：

我们只用了一行代码，就完成了一看起来有点复杂的任务:

 .CreateFromDataTable(DataTables("订单"),False,"客户='CS01'","日期
desc","产品","单价","数量","日期","审核")

这就是使用框架的好处。

提示：

自动生成的网页，逻辑列中的True被符号●代替，False被符号○代替，你可以自定义符号，你可以用BooleanSymbol属性自定义符号，例如：

With
wb.AddTable("","Table1")
     .BooleanSymbol= "√×"
    .CreateFromDataTable(DataTables("订单"))
End With

CreateFromDataTable

CreateFromDataTable用于根据Foxtable的DataTable自动生成网页，语法：

CreateFromDataTable(DataTable)
CreateFromDataTable(DataTable, RowNum)
CreateFromDataTable(DataTable, RowNum, Filter)
CreateFromDataTable(DataTable, RowNum, Filter)
CreateFromDataTable(DataTable, RowNum, Filter, Sort)
CreateFromDataTable(DataTable, RowNum, Filter, Sort, DataCols)
CreateFromDataTable(DataTable, RowNum, Filter, Sort, DataCol1, DataCol2,
DataCol3...)

|  |  |
| --- | --- |
| 参数 | 说明 |
| DataTable | Foxtable中的DataTable。 |
| RowNum | 逻辑型，是否显示行号。 |
| Filter | 筛选条件 |
| Sort | 排序列 |
| DataCols | 一个包括所有要显示列的列名的集合或数组，例如：    Dim nms() As String  =  "产品,客户,日期,数量".Split(",")  .CreateFromDataTable(DataTables("订单"),True,"","",nms) |
| DataCol1, DataCol2, DataCol3 | 字符型，用于指定要显示的列，例如：    .CreateFromDataTable(DataTables("订单"),False,"","","产品","单价","数量","日期","审核") |

### 手工编码生成

手工编码生成


**手工编码生成**

前面我们介绍了根据DataTable和Table自动生成网页的方法，简单到只需一行代码。


如果需要对细节做更多的控制，则需要手工编码，不过也不要担心，代码依然简单，因为这是Foxtable嘛。

**一个例子**

下面的HttpRequest事件代码，从订单表中提取数量超过100的订单，按日期顺序生成网页表：

Select
Case e.Path


Case "table.htm"


Dim wb
As New WeUI


With wb.AddTable("","Table1")

            .Alternate
= 3


Dim nms()
As String =
{"产品","客户","数量","单价","日期"}

            .Head.AddRow(nms)


For Each
r As
DataRow In
DataTables("订单").Select("数量
> 100",
"日期
Desc")


With .Body.AddRow(r("产品"),r("客户"),r("数量"))

                    .AddCell(Format(r("单价"),"#0.00"))

                    .AddCell(Format(r("日期"),"MM月dd日"))


End
With


Next


End
With

        e.WriteString(wb.Build)

End
Select

这是在手机上访问的效果：

**加上行号**

如果希望显示行号，可以参考下面的HttpRequest事件代码：

Select
Case e.Path


Case
"table.htm"



Dim wb
As New WeUI


With wb.AddTable("","Table1")

            .Alternate
= 3

            .RowHead
= 1

            .ColWidth
= "12px"


Dim nms()
As String =
{"","产品","客户","数量","单价","日期"}

            .Head.AddRow(nms)


Dim cnt
As
Integer


For Each
r As
DataRow In
DataTables("订单").Select("数量
> 100",
"日期
Desc")


cnt = cnt +
1


With .Body.AddRow(cnt,
r("产品"),
r("客户"),
r("数量"))

                    .AddCell(Format(r("单价"),
"#0.00"))

                    .AddCell(Format(r("日期"),
"MM月dd日"))


End
With


Next


End
With


e.WriteString(wb.Build)

End
Select

**多层表头**

假定有下图所示的一个已知结构的有多层表头的数据表：

如果要根据这个表生成网页，可以参考下面的HttpRequest事件代码：

Select
Case e.Path


Case
"table.htm"


Dim wb
As New WeUI


With wb.AddTable("","Table1")


'下面这个数组,用实际的列名.


Dim nms()
As String =
{"产品","东部\_一季度","东部\_二季度","东部\_三季度","东部\_四季度","南部\_一季度","南部\_二季度","南部\_三季度","南部\_四季度"}



.Head.AddRow("产品","东部","东部","东部","东部","西部","西部","西部","西部")
'第一层标题

            .Head.AddRow("产品","一季度","二季度","三季度","四季度","一季度","二季度","三季度","四季度")
'第二层标题


For Each
r As
DataRow In
DataTables("表名").DataRows


With
.Body.AddRow()


For Each
nm As
String In
nms

                        .AddCell(r(nm))


Next


End
With


Next


End
With


e.WriteString(wb.Build)

End
Select

### 编码合并单元格

编码合并单元格


**编码合并单元格**

通过AddCell方法的第二个参数，可以给单元格设置属性。
单元格有两个属性用于实现单元格合并，分别为：

* rowspan
  指定单元格在纵向跨越的行数。
* colspan
  指定单元格在横向跨越的列数。

**一个例子**

HttpRequest事件代码:

Select
Case e.Path
    Case "list.htm"
        Dim
wb As New
WeUI
        wb.InsertHTML("合并单元格<br/><br/>")
        With wb.AddTable("","Table1")
            With .body.AddRow
                .AddCell("1")
                .AddCell("2","rowspan=3")
                .Addcell("3")
                .Addcell("4")
            End With
            .body.AddRow("5","7","8")
            .body.AddRow("9","11","12")
            With .body.AddRow("a")
                .AddCell("b","colspan='2'")
                .Addcell("d")
            End With
        End
With
        e.WriteString(wb.Build)
End
Select

显示效果：

在添加单元格的时候，如果遇到合并单元格，必须省略此单元格的值，按顺序添加其他单元格的值。
例如第二行，我们只添加了三个值，分别为5、7、8，由于第二个单元格被合并，所以7、8顺被移到第三个和第四个单元格显示。

这些都属于HTML的知识，有兴趣的话，可以访问以下网址学习：
<http://www.w3school.com.cn/html/index.asp>

### 分页显示数据

分页显示数据


**分页显示数据**

本节以SQL
Server为例，介绍一下如何分页显示后台数据，原理和我们在快速入门这一章介绍的相同，在合成的链接地址中包括要现实的页码：

http://127.0.0.1/list.htm?page=1

下面是HttpRequest事件代码：

Select
Case e.Path
    Case "list.htm"
        '获取要显示的页
        Dim page
As Integer
= 0
'默认page为0,显示第一页
        Dim pageRows
As Integer
= 15
'每页15行
        If e.GetValues.ContainsKey("page")
Then
'如果地址中有page参数
            Integer.TryParse(e.GetValues("page"),
page)
'提取page参数
        End If
        Dim
StartRow As
Integer = page \*
pageRows + 1
'此页第一行
        Dim EndRow
As Integer
= (page + 1)
\* pageRows
'此页最后一行


'获取该页数据
        Dim cmd
As New
SQLCommand
        cmd.ConnectionName
= "orders"
'记得设置数据源名称
        cmd.CommandText
= "Select Count(\*) From {订单}"
        Dim Count
As Integer
= cmd.ExecuteScalar()
'获取总的行数
        cmd.CommandText
= "Select \* From (Select
Row\_Number() Over(Order by 日期)
As [NO.],
产品,客户,数量,单价,日期
From 订单)
As a "
        cmd.CommandText
= cmd.CommandText
& "  Where [NO.]>=
" & StartRow
& " And [NO.] <= "
& EndRow
        Dim
dt As
DataTable = cmd.ExecuteReader


'根据此页数据生成网页

Dim
wb As
New WeUI
        With
wb.AddTable("","Table1")
            .CreateFromDataTable(dt)
        End With
        With
wb.AddButtonGroup("","btg2",
False)
            If page
> 0 Then
                .Add("btnPrev",
"上一页","","List.htm?page="
& page -
1)
            End If
            If
Endrow < count
Then
                .Add("btnNext",
"下一页","","List.htm?page="
& page +
1)
            End If
        End
With
        e.WriteString(wb.Build)
End
Select

这是通过手机访问显示的效果：

### 生成汇总模式

生成汇总模式


**生成汇总模式**

有了前面的知识，生成汇总模式是很轻松的。

下面是按产品和客户分组，对数量和金额进行统计的HttpRequest事件代码：

Select
Case e.Path
    Case
"list.htm"
        '获取要显示的页
        Dim page
As Integer
= 0
'默认page为0,显示第一页
        Dim pageRows
As Integer
= 13
'每页13行
        If e.GetValues.ContainsKey("page")
Then
'如果地址中有page参数
            Integer.TryParse(e.GetValues("page"),
page)
'提取page参数
        End If
        Dim
StartRow As
Integer = page \*
pageRows + 1
'此页第一行
        Dim EndRow
As Integer
= (page + 1)
\* pageRows
'此页最后一行
        '获取该页数据
        Dim cmd
As New
SQLCommand
        cmd.ConnectionName
= "orders"
'记得设置数据源名称
        cmd.CommandText
= "Select Count(\*) From {订单}"
        Dim Count
As Integer
= cmd.ExecuteScalar()
'获取总的行数
        cmd.CommandText
= "Select \* From (Select
Row\_Number() Over(Order by
产品,客户,日期)
As [NO.],
产品,
客户,
数量,
单价,
数量
\* 单价
as 金额,日期
From 订单)
As a "
        cmd.CommandText
= cmd.CommandText
& "  Where [NO.]>=
" & StartRow
& " And [NO.] <= "
& EndRow
        Dim
dt As
DataTable = cmd.ExecuteReader

'根据此页数据生成网页

Dim
wb As
New WeUI
        With
wb.AddTable("","Table1")
            Dim nms()
As String
            Dim
qty As
Integer
            Dim
amt As
Double
            .Head.AddRow("No.","产品","客户","数量","单价","金额","日期")
            For i
As Integer
= 0 To dt.DataRows.count
- 1
                Dim
r As
DataRow = dt.DataRows(i)
                If i
> 0 Then
                    Dim
lr As
DataRow = dt.DataRows(i-1)
                    If
r("客户")
<> lr("客户")
Then
                        qty =
dt.compute("sum(数量)","产品='"
& lr("产品")
&
"' And
客户=
'"
& lr("客户")
& "'")

amt
= dt.compute("sum(金额)","产品='"
& lr("产品")
& "' And 客户= '"
& lr("客户")
& "'")
                        With .Body.AddRow()
                            .Attribute =
"style='background-color:#F0FFFF'"
                            .AddCell("小计
" & lr("客户"),"colspan='3'")
                            .AddCells(qty,"",amt,"")
                        End
With
                    End
If
                    If
r("产品") <>
lr("产品")
Then
                        qty =
dt.compute("sum(数量)","产品='"
& lr("产品")
&  "'")
                        amt =
dt.compute("sum(金额)","产品='"
& lr("产品")
& "'")
                        With .Body.AddRow()
                            .Attribute =
"style='background-color:#FFFFE0'"
                            .AddCell("小计
" & lr("产品"),"colspan='3'")

.AddCells(qty,"",amt,"")
                        End
With
                    End
If
                End
If
                .Body.AddRow(r("NO."),r("产品"),r("客户"),r("数量"),r("单价"),r("金额"),r("日期"))
            Next
            qty =
dt.compute("sum(数量)")
            amt =
dt.compute("sum(金额)")
            If
EndRow >= Count
Then
                .Body.AddRow("总计","","",qty,"",amt,"").Attribute
= "style='background-color:#98FB98'"
            End
If
        End
With
        With
wb.AddButtonGroup("","btg2",
False)
            If page
> 0 Then
                .Add("btnPrev",
"上一页","","List.htm?page="
& page -
1)
            End If
            If Endrow < count  Then
                .Add("btnNext", "下一页","","List.htm?page="
& page + 1)
            End If
        End With
        e.WriteString(wb.Build)
End Select

代码逻辑很简单，按产品和客户顺序，分页显示数据，每当产品或客户发生变化时，就插入一个分组行显示该产品或客户的累计数量和金额。
需要注意的是，分组行的背景没有采用外部CSS文件设置，直接使用了内嵌样式。

这是在手机上的显示效果：

### 数据筛选

数据筛选显示


**数据筛选显示**

本节的任务使设计一个筛选页面，输入输入条件，单击确定后，能从后台筛选出符合条件的行显示：

HttpRequest事件代码：

Dim
wb As New
WeUI
Select
Case e.Path
    Case "filter.htm"
        wb.AddForm("","form1","list.htm")
        With wb.AddInputGroup("form1","ipg1","数据筛选")
            .AddSelect("product","产品","PD01|PD02|PD03|PD04|PD05")
            .AddInput("startdate","开始日期","date")
            .AddInput("enddate","结束时间","date")
        End With
        With
wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
    Case "list.htm"
        Dim
flt As
String
        If e.PostValues.ContainsKey("product")
Then
            flt =
"产品
= '"
& e.PostValues("product")
& "'"
        End If
        If e.PostValues.ContainsKey("startdate")
Then
            If
flt > ""
Then
                flt =
flt &
" and "
            End
If

flt =
flt &
"日期
>= '"
& e.PostValues("startdate")
& "'"
        End If
        If e.PostValues.ContainsKey("enddate")
Then
            If
flt > ""
Then
                flt =
flt &
" and "
            End
If

flt =
flt &
"日期
<= '"
& e.PostValues("enddate")
& "'"
        End If
        Dim
cmd As new
SQLCommand
        cmd.ConnectionName
= "orders"
        cmd.CommandText=
"select
产品,客户,数量,单价,[日期]
From 订单"
        If flt
> "" Then
            cmd.CommandText
= cmd.CommandText
& " where "
& flt
        End If
        With
wb.AddTable("","Table1")
            .CreateFromDataTable(cmd.ExecuteReader)
        End With
        With
wb.AddButtonGroup("","btg1",True)
            .Add("btn1",
"重新筛选", "","filter.htm")
        End With
End Select
e.WriteString(wb.Build)

### 数据筛选与分页

数据筛选与分页


**数据筛选与分页**

筛选后的数据，可能还是太多，依然需要分页处理：



如何筛选，如何分页，前面都有讲述，并不复杂。

将二者组合起来，首先必须解决的问题是如何保存和传递筛选条件，当然我们可以像页码一样，将条件写在url地址中，用get方式传递。

但是这样的设计，会增加编码难度，我们改用cookie来保存和传递筛选条件，会方便很多，关于cookie，参考：[使用cookie](0042.htm)

下面是一小段示例代码，清晰地说明了如何通过cookie来保存和传递筛选条件：

Dim
flt As
String

If e.GetValues.ContainsKey("unfilter")
Then
    wb.ClearCookie()
ElseIf e.PostValues.ContainsKey("product")
Then
    flt =
"产品
= '"
& e.PostValues("product")
& "'"
    wb.AppendCookie("product",
e.PostValues("product"))
ElseIf e.Cookies.ContainsKey("product")
Then
    flt =
"产品
= '"
& e.Cookies("product")
&
"'"
End
If

代码流程如下：

1、首先判断访问请求中是否包括get参数"unfilter"，如果包括，则清除所有Cookie。
2、然后判断PostValues中是否包括product，如果有则从PostValues中提起此值合成筛选条件，然后将product的值保存在cookie中。
3、如果PostValues中是不包括product，就判断cookie中是否包括product，如果有，则提取此值合成筛选条件。

使用流程如下：

1、用户通过筛选页面输入筛选条件，单击确定按钮提交到服务器，此时product的值是保存在PostValues中的，服务端从PostValues中提取出product合成筛选条件，然后将product的值存入客户端的cookie中。
2、当用户单击上一页、下一页按钮时，保存在cookie中的product值，会自动发送到服务器，服务端从cookie中提取出product值合成筛选条件。
3、如果用户单击"取消筛选"按钮，向服务器发出访问请求"list.htm?unfilter=true"，服务段收到请求后，判断请求中包括get参数"unfilter"，如是清除cookie，系统回到非筛选状态。

完整的HttpRequest事件代码：

Dim
wb As
New WeUI
Select
Case e.Path
    Case
"filter.htm"
        wb.AddForm("","form1","list.htm")
        With wb.AddInputGroup("form1","ipg1","数据筛选")
            .AddSelect("product","产品","|PD01|PD02|PD03|PD04|PD05")
            .AddInput("startdate","开始日期","date")
            .AddInput("enddate","结束时间","date")
        End With
        With wb.AddButtonGroup("form1","btg1",True)
            .Add("btn1",
"确定",
"submit")
        End With
    Case "list.htm"
        '合成条件
        Dim flt
As String
        If e.GetValues.ContainsKey("unfilter")
Then '如果有unfilter参数,则清除cookie
            wb.ClearCookie()
        ElseIf e.PostValues.Count
> 0 Then
'如果是filter.htm访问,则根据用户输入合成条件表达式
            If e.PostValues.ContainsKey("product")
Then
                flt =
"产品
= '"
& e.PostValues("product")
& "'"
'合成条件
                wb.AppendCookie("product",
e.PostValues("product"))
'将值写入cookie中
            Else
                wb.DeleteCookie("product")
'删除cookie
            End If
            If
e.PostValues.ContainsKey("startdate")
Then
                If
flt > ""
Then
                    flt =
flt &
" and "
                End
If
                flt =
flt &
"日期
>= '"
& e.PostValues("startdate")
& "'"
                wb.AppendCookie("startdate",
e.PostValues("startdate"))
            Else
                wb.DeleteCookie("startdate")
            End If
            If
e.PostValues.ContainsKey("enddate")
Then
                If
flt > ""
Then
                    flt =
flt &
" and "
                End
If
                flt =
flt &
"日期
<= '"
& e.PostValues("enddate")
& "'"
                wb.AppendCookie("enddate",
e.PostValues("enddate"))
            Else
                wb.DeleteCookie("enddate")
            End If
        Else
'否则根据Cookie合成条件表达式
            If e.Cookies.ContainsKey("product")
Then
                flt =
"产品
= '"
& e.Cookies("product")
& "'"
            End
If
            If
e.Cookies.ContainsKey("startdate")
Then
                If
flt > ""
Then
                    flt =
flt &
" and "
                End
If
                flt =
flt &
"日期
>= '"
& e.Cookies("startdate")
& "'"
            End
If
            If
e.Cookies.ContainsKey("enddate")
Then
                If
flt > ""
Then
                    flt =
flt &
" and "
                End
If
                flt =
flt &
"日期
<= '"
& e.Cookies("enddate")
& "'"
            End
If
        End If
        '获取要显示的页码
        Dim page
As Integer =
0 '默认page为0,显示第一页
        Dim pageRows
As Integer =
10 '每页10行
        If e.GetValues.ContainsKey("page")
Then  '如果地址中有page参数

Integer.TryParse(e.GetValues("page"),
page) '提取page参数
        End If
        Dim
StartRow As
Integer = page \*
pageRows + 1
'此页第一行
        Dim
EndRow As
Integer = (page +
1) \* pageRows
'此页最后一行
        '提取此页数据
        Dim cmd
As New
SQLCommand
        cmd.ConnectionName
= "orders"
'记得设置数据源名称
        cmd.CommandText
= "Select Count(\*) From {订单}"

If
flt > ""
Then
            cmd.CommandText
= cmd.CommandText
& " where "
& flt
        End If
        Dim
Count As
Integer = cmd.ExecuteScalar()
'获取总的行数
        cmd.CommandText
= "Select \* From (Select Row\_Number() Over(Order by
日期)
As [NO.],
产品,客户,数量,单价,日期
From 订单
"
        If flt
> "" Then
            cmd.CommandText
= cmd.CommandText
& " where "
& flt
        End If
        cmd.CommandText
= cmd.CommandText
& ") As a "
        cmd.CommandText
= cmd.CommandText
& "  Where [NO.]>= "
& StartRow
& " And [NO.] <= "
& EndRow
        '合成网页
        With wb.AddTable("","Table1")
            .CreateFromDataTable(cmd.ExecuteReader)
        End With
        With wb.AddButtonGroup("","btg2",
False)
            If page
> 0 Then
                .Add("btnPrev",
"上一页","","List.htm?page="
& page -
1)
            End If
            If
Endrow < count
Then
                .Add("btnNext",
"下一页","","List.htm?page="
& page +
1)
            End If
            If
flt  = "" Then
                .Add("btn1",
"筛选",
"","filter.htm").kind
= 1
            Else
                .Add("btn1",
"取消筛选",
"","list.htm?unfilter=true").kind
= 1
            End
If
        End With
End
Select
e.WriteString(wb.Build)

### 给表格加上菜单

给表格加上菜单


**给表格加上菜单**

给表加上菜单的代码很简单，我们首先要设计一个ActionSheet，然后将此ActionSheet的ID设置为表的ActiveSheet属性即可。

例如HttpRequest事件代码：

Select
Case e.Path
    Case "table.htm"
        Dim
wb As New
WeUI
        With
wb.AddTable("","Table1")
            .head.AddRow("部门","姓名","年龄","电话","地址")
'表头
            .body.AddRow("技术部","张三","36","110","中国北京")
'数据
            .body.AddRow("技术部","李四","38","110","中国上海")
            .body.AddRow("技术部","王五","39","110","中国深圳")
            .body.AddRow("生产部","赵六","39","110","中国深圳")
            .body.AddRow("生产部","刘七","39","110","中国深圳")
            .ActiveSheet =
"menu"
'指定菜单
        End With
        With
wb.AddActionSheet("","menu")
'设计菜单
            .Add("mnudAdd",
"增加订单")
            .Add("mnuEdit",
"编辑订单")
            .Add("mnuDelete",
"删除订单")
            .Add("mnuCancel","取消","",True)
        End With
        e.WriteString(wb.Build)
End
Select

打开网页后，先点击选择某个单元格，然后再次点击此单元格，即可出现菜单。

也就是说，第一次点击是选择，第二次点击是显示菜单：

单单显示菜单是没有意义的，目的是通过菜单增加行，或编辑和删除选定的行，新增行好办，但是要实现编辑和删除行，就必须给服务器传递当前行的主键，这样服务器才能知道客户端需要编辑和删除的是哪一行，最好也将当前的页码一并传递给服务器，这样编辑和删除行之后，还能回到当前页，这是我们下一节要解决的问题。

### 传递主键和页码

传递主键和页码


**传递主键和页码**

上一节说到，要实现通过菜单编辑和删除行，必须给客户端传递行的主键和页码。

传递页码很简单，生成表格的时候，直接将其PageNumber属性设置为当前页码即可。

传递主键要分两种情况，如果是CreateFromDataTable和CreateFromTable自动生成表格，那么设置表格的Primarykey为主键列的列名即可；如果是手工编码生成，则需要逐行设置主键值。

本节先介绍第一种情况，第二种情况留待下一节讲述。

在编写JavaScript代码的时候，表格同样有pagenumber和primarykey(注意是小写)，分别用于返回当前页码和选定行的主键值。

**一个例子**

HttpRequest事件代码：

Select
Case e.Path
    Case "list.htm"
        '获取要显示的页
        Dim page
As Integer =
0
'默认page为0,显示第一页
        Dim pageRows
As Integer =
15
'每页15行
        If e.GetValues.ContainsKey("page")
Then
'如果地址中有page参数
            Integer.TryParse(e.GetValues("page"),
page)
'提取page参数
        End If
        Dim
StartRow As
Integer = page \*
pageRows + 1
'此页第一行
        Dim EndRow
As Integer =
(page + 1) \*
pageRows
'此页最后一行
        '获取该页数据
        Dim cmd
As New
SQLCommand
        cmd.ConnectionName
= "orders"
'记得设置数据源名称
        cmd.CommandText
= "Select Count(\*) From {订单}"
        Dim Count
As Integer =
cmd.ExecuteScalar()
'获取总的行数
        cmd.CommandText
= "Select \* From (Select
Row\_Number() Over(Order by
日期)
As [NO.],[\_Identify],产品,客户,数量,单价,日期
From 订单)
As a "
        cmd.CommandText
= cmd.CommandText
& "  Where [NO.]>= "
& StartRow
& " And [NO.] <= "
& EndRow
        Dim dt
As DataTable
= cmd.ExecuteReader
        '生成菜单
        Dim wb
As New
WeUI
        With wb.AddActionSheet("","menu")
'设计菜单
            .Add("mnudAdd",
"增加订单").Attribute="onclick=""alert('增加订单')"""
            .Add("mnuEdit",
"编辑订单").Attribute
="onclick=""alert('编辑订单
页码:'+table1.pagenumber+
'主键:'+
table1.primarykey)"""
            .Add("mnuDelete",
"删除订单").Attribute
="onclick=""alert('删除订单
页码:'+table1.pagenumber+
'主键:'+
table1.primarykey)"""
            .Add("mnuCancel","取消","",True)
        End With

'根据此页数据生成网页
        With wb.AddTable("","Table1")
            .PageNumber =
page '设置页码
            .Primarykey =
"\_Identify" '设置主键
            .ActiveSheet =
"menu" '设置菜单
            .CreateFromDataTable(dt)
        End With

With
wb.AddButtonGroup("","btg2",
False)
            If page
> 0 Then
                .Add("btnPrev",
"上一页","","List.htm?page="
& page -
1)
            End
If
            If
Endrow < count
Then
                .Add("btnNext",
"下一页","","List.htm?page="
& page +
1)
            End If
        End With
        e.WriteString(wb.Build)
End
Select

因为要传递主键给客户端，所以select语句必须将主键列包括进来，接下来你要做的知识指定页码和主键：

With
wb.AddTable("","Table1")
    .PageNumber =
page '设置页码
    .Primarykey =
"\_Identify" '设置主键
    .ActiveSheet =
"menu" '设置菜单
    .CreateFromDataTable(dt)
End
With

需要注意的是：页码、主键和菜单名，都需要在执行CreateFromDataTable之前设置好，否则无效。

现在你在客户端浏览器连续点击某行，会出现菜单，在点击菜单中的命令，会显示当前页码和当前行的主键。

下图是我在iPhone按着上述操作后截图：

### 手工编码传递主键

手工编码传递主键


**手工编码传递主键**

如果因为特殊原因，不能采用CreateFromDataTable或CreateFromTable自动生成表格，那就需要逐行设置Primarykey属性了
，例如：

Dim
wb As
New WeUI
With
wb.AddTable("","Table1")
    Dim nms()
As String =
{"产品","客户","数量","单价","日期"}
    .Head.AddRow(nms)
    For Each
r As
DataRow In
DataTables("订单").DataRows

        With .Body.AddRow(r("产品"),r("客户"),r("数量"))
            .Primarykey =
r("\_Identify")
'设置主键
            .AddCell(Format(r("单价"),"#0.00"))
            .AddCell(Format(r("日期"),"MM月dd日"))
        End
With
    Next
End
With

上述代码假定订单表的主键列是"\_Identity"，表格每增加一行，就将其Primarykey属性设置为对应DataRow的"\_Identify"列的值。

完整示例

HttpRequest事件代码：

Select
Case e.Path
    Case "list.htm"
        '获取要显示的页
        Dim
page As
Integer = 0
'默认page为0,显示第一页
        Dim
pageRows As
Integer = 15
'每页15行
        If e.GetValues.ContainsKey("page")
Then
'如果地址中有page参数
            Integer.TryParse(e.GetValues("page"),
page) '提取page参数
        End If
        Dim
StartRow As
Integer = page \*
pageRows + 1
'此页第一行
        Dim
EndRow As
Integer = (page +
1) \* pageRows
'此页最后一行
        '获取该页数据
        Dim
cmd As New
SQLCommand
        cmd.ConnectionName
= "orders"
'记得设置数据源名称
        cmd.CommandText
= "Select Count(\*) From {订单}"
        Dim
Count As
Integer = cmd.ExecuteScalar()
'获取总的行数
        cmd.CommandText
= "Select \* From (Select Row\_Number() Over(Order by
日期) As [NO.],[\_Identify],产品,客户,数量,单价,日期 From 订单) As a "
        cmd.CommandText
= cmd.CommandText
& "  Where [NO.]>=
" & StartRow
& " And [NO.] <= "
& EndRow
        Dim
dt As
DataTable = cmd.ExecuteReader
        '生成菜单
        Dim
wb As New
WeUI
        With
wb.AddActionSheet("","menu")
'设计菜单
            .Add("mnudAdd",
"增加订单").Attribute="onclick=""alert('增加订单')"""
            .Add("mnuEdit",
"编辑订单").Attribute
="onclick=""alert('编辑订单页码:'+table1.pagenumber+ '主键:'+
table1.primarykey)"""
            .Add("mnuDelete",
"删除订单").Attribute
="onclick=""alert('删除订单页码:'+table1.pagenumber+ '主键:'+
table1.primarykey)"""
            .Add("mnuCancel","取消","",True)
        End With
        '根据此页数据生成网页
        With
wb.AddTable("","Table1")
            .PageNumber =
page '设置页码
            .ActiveSheet =
"menu"
             Dim
nms() As
String = {"NO.","产品","客户","数量","单价","日期"}
            .Head.AddRow(nms)
             For
Each r As
DataRow In
dt.DataRows


With .Body.AddRow(r("NO."),r("产品"),r("客户"),r("数量"))
                    .Primarykey =
r("\_Identify")
'设置主键
                    .AddCell(Format(r("单价"),"#0.00"))
                    .AddCell(Format(r("日期"),"MM月dd日"))
                End
With
            Next
        End
With
        With
wb.AddButtonGroup("","btg2",
False)
            If page
> 0 Then
                .Add("btnPrev",
"上一页","","List.htm?page="
& page -
1)
            End If
            If
Endrow < count
Then
                .Add("btnNext",
"下一页","","List.htm?page="
& page +
1)
            End If
        End
With
        e.WriteString(wb.Build)
End
Select

同样Select语句必须将主键列包括进来。

现在你在客户端浏览器连续点击某行，会出现菜单，在点击菜单中的命令，会显示当前页码和当前行的主键。

下图是我在iPhone按着上述操作后截图：

### 菜单综合示例

菜单综合示例


**菜单综合示例**

本节的任务是分页浏览后台数据，连续点击某个单元格，能弹出一个菜单，通过这个菜单实现订单的编辑、增加和删除：

增加、编辑或删除订单后，都能出现一个提示，例如下图是增加订单成功后的提示：

设计步骤：

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"table.js"，文件内容为：

function edit(){
    location="edit.htm?page=" + table1.pagenumber + "&key=" +
table1.primarykey;
}
function del(){
    location="delete.htm?page=" + table1.pagenumber + "&key=" +
table1.primarykey;
}
function addnew(){
    location="addnew.htm?page=" + table1.pagenumber;
}

上述js代码定义了三个函数，代码都很简单，将表格的pagenumber(当前页码)和primarykey(选定行主键)用get方式传递给服务器

假定当前页码是3，主键为176，那么执行edit函数，传递给服务器的链接地址就是：

http://127.0.0.1/edit.htm?page=3&key=176

服务器就知道：用户要编辑的订单的主键值是176，编辑结束后，返回第4页。

提示：delete是JavaScript的关键词，不能用作函数名。

2、为例避免HttpRequest事件代码过长，也为了更便于维护，我们将主要功能用自定义函数实现。

本示例包括四个自定义函数，其中List函数用于数据的分页显示，以及菜单的生成和显示，另外三个函数为AddNew、Delete和Edit，分别用于增加、删除和编辑订单。

函数的代码为：

|  |  |
| --- | --- |
| 函数名 | 代码 |
| List | Dim e As RequestEventArgs = args(0)  '获取要显示的页  Dim page As Integer = 0 '默认page为0,显示第一页  Dim pageRows As Integer =  10 '每页10行  If e.GetValues.ContainsKey("page") Then   '如果地址中有page参数      Integer.TryParse(e.GetValues("page"), page)  '提取page参数  End  If  Dim StartRow As Integer =  page \* pageRows + 1  '此页第一行  Dim EndRow As Integer = (page + 1) \*  pageRows '此页最后一行  '获取该页数据  Dim cmd As New  SQLCommand  cmd.ConnectionName = "orders"  '记得设置数据源名称  cmd.CommandText = "Select Count(\*) From {订单}"  Dim Count As Integer =  cmd.ExecuteScalar()  '获取总的行数  cmd.CommandText = "Select \* From (Select Row\_Number() Over(Order by  日期 desc) As [NO.],[\_Identify],产品,客户,数量,单价,日期 From 订单) As a "  cmd.CommandText = cmd.CommandText & "  Where [NO.]>= " & StartRow & " And [NO.] <= " &  EndRow  Dim dt As DataTable =  cmd.ExecuteReader  '生成菜单  Dim wb As New  WeUI  With wb.AddActionSheet("","menu") '设计菜单      .Add("mnudAdd", "增加订单").Attribute="onclick='addnew()'" '调用js函数      .Add("mnuEdit", "编辑订单").Attribute ="onclick='edit()'"      .Add("mnuDelete", "删除订单").Attribute ="onclick='del()'"      .Add("mnuCancel","取消","",True)  End  With  '根据此页数据生成网页  With wb.AddTable("","Table1")      .PageNumber = page  '设置页码      .Primarykey = "\_Identify"  '设置主键      .ActiveSheet = "menu"  '设置菜单      .CreateFromDataTable(dt)  End  With  With wb.AddButtonGroup("","btg2", False)  '生成上一页和下一页按钮      If page > 0 Then          .Add("btnPrev", "上一页","","List.htm?page=" & page - 1)      End If      If  Endrow < count Then          .Add("btnNext", "下一页","","List.htm?page=" & page + 1)      End If  End  With  wb.AppendHTML("<script src='./lib/table.js'></script>")  '引入脚本文件  e.WriteString(wb.Build) |
| AddNew | Dim e As RequestEventArgs = args(0)  Dim wb As New  weui  If e.PostValues.Count = 0 Then '生成增加订单网页      wb.AddForm("","form1","addnew.htm")      With wb.AddInputGroup("form1","ipg1","增加订单")          .AddInput("产品","产品","text")          .AddInput("客户","客户","text")          .AddInput("数量","数量","number")          .AddInput("单价","单价","number").Step="0.01"          .AddInput("日期","日期","date")      End With      With wb.AddButtonGroup("form1","btg1",True)          .Add("btn1", "确定", "submit")      End  With  Else  '保存新增的订单      Dim dr As DataRow = DataTables("订单").AddNew()      Dim nms() As String = {"产品","客户","数量","单价","日期"}      For Each nm As String In nms          dr(nm) = e.PostValues(nm)      Next      dr.Save()      With wb.AddMsgPage("","msgpage","增加成功", "好好学习,天天向上") '增加订单成功提示信息          .AddButton("btn1","继续增加","addnew.htm")          .AddButton("btn1","返回列表","list.htm")       End With  End  If  e.WriteString(wb.Build) '生成网页 |
| Edit | Dim e As RequestEventArgs = args(0)  Dim wb As New  weui  Dim PageNumber As Integer = e.GetValues("page")  Dim PrimaryKey As Integer = e.GetValues("key")  Dim PageURL = "List.htm?page=" &  PageNumber  If e.PostValues.Count = 0 Then '生成编辑页面      Dim dr As DataRow = DataTables("订单").SQLFind("[\_Identify]=" & PrimaryKey)      If dr IsNot Nothing Then          wb.AddForm("","form1","edit.htm?key=" & PrimaryKey &  "&page=" & PageNumber)          With  wb.AddInputGroup("form1","ipg1","编辑订单")              .AddInput("产品","产品","text").Value = dr("产品")              .AddInput("客户","客户","text").Value = dr("客户")              .AddInput("数量","数量","number").Value = dr("数量")              With .AddInput("单价","单价","number")                  .Step="0.01"                  .Value = dr("单价")              End  With              .AddInput("日期","日期","date").Value = dr("日期")          End  With          With wb.AddButtonGroup("form1","btg1",True)              .Add("btn1", "确定", "submit")          End  With      Else          With wb.AddMsgPage("","msgpage","编辑失败", "此订单可能已经被删除!") '提示用户此订单不存在.              .icon= "Warn"              .AddButton("btn1","返回",PageURL) '生成返回原来页面的按钮          End  With      End  If  Else  '保存编辑结果      Dim dr As DataRow = DataTables("订单").SQLFind("[\_Identify]=" & PrimaryKey)      If dr IsNot Nothing Then          Dim nms() As String =  {"产品","客户","数量","单价","日期"}          For  Each nm  As String In nms               dr(nm) = e.PostValues(nm)           Next           dr.Save()            '显示完成提示,2妙手自动返回原来的页面            wb.AppendHtml("<meta http-equiv='refresh' content='2; url=/" & PageURL  & "'>",True)          wb.AddToast("","t1", "编辑完成",0).Visible = True      Else          With wb.AddMsgPage("","msgpage","保存失败", "此订单可能已经被删除!") '提示用户此订单不存在.              .icon= "Warn"              .AddButton("btn1","返回",PageURL) '生成返回原来页面的按钮          End With      End  If  End  If  e.WriteString(wb.Build) '生成网页 |
| Delete | Dim e As RequestEventArgs = args(0)  Dim wb As New  weui  Dim PageURL = "List.htm?page=" & e.GetValues("page") '合成当前页面链接  DataTables("订单").SQLDeleteFor("[\_Identify] =" & e.GetValues("key")) '根据主键删除行  '显示删除完成提示,2秒后返回原来的页面  wb.AppendHtml("<meta http-equiv='refresh' content='2; url=/"  & PageURL  & "'>",True)  wb.AddToast("","t1", "订单已删除",0).Visible= True  e.WriteString(wb.Build) |

3、将HttpRequest事件代码设置为：

Select
Case e.Path
    Case "list.htm"
        Functions.Execute("List",e)
    Case "addnew.htm"
        Functions.Execute("AddNew",e)
    Case "edit.htm"
        Functions.Execute("Edit",e)
    Case "delete.htm"
        Functions.Execute("Delete",e)
End
Select

### 改用按钮操作

改用按钮操作


**改用按钮操作**

本节任务和上一节相同，但全部改用按钮操作，并加上首页和末页按钮。

此外根据页面的位置，按钮颜色会改变，例如到了最后一页，下一页和末页按钮颜色变灰：

需要改动的地方有两处。

1、首先如果用户没有选择任何行，应该禁止编辑和删除订单，以免出错，所以将table.js的代码改为：

function edit(){
    if (table1.primarykey){
        location="edit.htm?page=" +
table1.pagenumber + "&key=" + table1.primarykey;
    }
}
function del(){
    if(table1.primarykey){
        location="delete.htm?page=" +
table1.pagenumber + "&key=" + table1.primarykey;
    }
}
function addnew(){
    location="addnew.htm?page=" + table1.pagenumber;
}

2、自定义函数list的代码改为：

Dim
e As
RequestEventArgs =
args(0)
'获取要显示的页
Dim
page As
Integer = 0
'默认page为0,显示第一页
Dim
pageRows As
Integer = 10
'每页10行
If
e.GetValues.ContainsKey("page")
Then  '如果地址中有page参数
    Integer.TryParse(e.GetValues("page"),
page) '提取page参数
End
If
Dim
StartRow As
Integer = page
\* pageRows + 1
'此页第一行
Dim
EndRow As
Integer = (page
+ 1) \* pageRows
'此页最后一行
'获取该页数据
Dim
cmd As
New SQLCommand
cmd.ConnectionName
= "orders" '记得设置数据源名称
cmd.CommandText
= "Select Count(\*) From {订单}"
Dim
Count As
Integer = cmd.ExecuteScalar()
'获取总的行数
Dim
Pages As
Integer = Math.Ceiling(Count/PageRows)
'计算出总页数
cmd.CommandText
= "Select \* From (Select Row\_Number() Over(Order by
日期
desc) As [NO.],[\_Identify],产品,客户,数量,单价,日期
From 订单)
As a "
cmd.CommandText
= cmd.CommandText
& "  Where [NO.]>=
" & StartRow
& " And [NO.] <= "
& EndRow
Dim
dt As
DataTable = cmd.ExecuteReader
Dim
wb As
New WeUI
'根据此页数据生成网页
With
wb.AddTable("","Table1")
    .PageNumber =
page '设置页码
    .Primarykey =
"\_Identify" '设置主键
    .CreateFromDataTable(dt)
End
With
With
wb.AddButtonGroup("","btg1",
False) '生成换页按钮
    If page >
0 Then
        .Add("btnFirst",
"首页","","List.htm?page=0")
        .Add("btnPrev",
"上一页","","List.htm?page="
& page -
1)
    Else
        .Add("btnFirst",
"首页").Kind
= 1
        .Add("btnPrev",
"上一页").Kind
= 1
    End If
    If Endrow
< count Then
        .Add("btnNext",
"下一页","","List.htm?page="
& page +
1)
        .Add("btnLast",
"末页","","List.htm?page="
& pages -
1)
    Else
       .Add("btnNext",
"下一页").Kind
= 1
        .Add("btnNext",
"末页").Kind
= 1
    End If
End
With
With
wb.AddButtonGroup("","btg2",
False) '生成操作按钮
    .Add("btnAdd",
"增加订单").Attribute
= "onclick='addnew()'"
    .Add("btnEdit",
"编辑订单").Attribute
= "onclick='edit()'"
    .Add("btnDelete",
"删除订单").Attribute
= "onclick='del()'"
End
With
wb.AppendHTML("<script
src='./lib/table.js'></script>") '引入脚本文件
e.WriteString(wb.Build)

### 显示动态菜单

显示动态菜单


**显示动态菜单**

一般用户可以忽略本节内容。

本节的任务是设计一个动态菜单，如果当前行部门列的内容为"技术部"时，隐藏“菜单项目1”：



设计步骤：

1、在"d:\web"目录下，建立一个子目录lib，在这个目录建立一个文本文件，文件名为"activesheet.js"，文件内容为：

function dynaActiveSheet(){
   if(table1.rows[table1.rowSel].cells[0].innerHTML=="技术部"){
      hide("menu1");
   }

else{
      show("menu1");
   }
}

提示: rowSel(注意区分大小写)属性是Foxtable为WeUI扩展的一个表格属性，用于返回选定行的位置，对应还有一个colSel属性，用于返回选定列的位置。

2、HttpRequest事件代码：

Select
Case e.Path
    Case "table.htm"
        Dim
wb As New
WeUI
        With
wb.AddTable("","table1")
            .AfterSelChange =
"dynaActiveSheet()"
'置顶选择不同单元格后要执行的js行数,注意区分大小写
            .head.AddRow("部门","姓名","年龄","电话","地址")
'表头
            .body.AddRow("技术部","张三","36","110","中国北京")
'数据
            .body.AddRow("技术部","李四","38","110","中国上海")
            .body.AddRow("技术部","王五","39","110","中国深圳")
            .body.AddRow("生产部","赵六","39","110","中国深圳")
            .body.AddRow("生产部","刘七","39","110","中国深圳")
            .ActiveSheet =
"menu" '指定菜单
        End
With
        With
wb.AddActionSheet("","menu")
'设计菜单
            .Add("menu1",
"菜单项目1")
            .Add("menu2",
"菜单项目2")
            .Add("menu3",
"菜单项目3")
            .Add("menu4","取消","",True)
        End With
        wb.AppendHTML("<script
src='./lib/activesheet.js'></script>")
'引入脚本文件
        e.WriteString(wb.Build)
End
Select

提示：

AfterSelChange属性用于指定在表格中选择不同单元格后，要执行的js事件代码，这里是要执行我们在第一步定义好的js函数，注意js函数是区分大小写的，而且括号不能省略。

### 又一个综合示例

又一个综合示例


**又一个综合示例**

本节是一个综合性比较强的例子，包括三个页面。

list.htm用于分页显示数据，有四个页面切换按钮：

连续两次点击同一单元格，会出现一个菜单，且在筛选和非筛选的状态下，显示的菜单是不同的：



filter.htm用于输入筛选条件：

tongji.htm用于统计数据（包括统计结果的显示），如果已经进行了筛选，则仅统计筛选后的数据：



为避免HttpRequest事件代码过程，本节全部采用自定义函数实现。

1、HttpRequest事件代码：

Select
Case e.Path
    Case "filter.htm"
        Functions.Execute("Filter",e)
    Case "list.htm"
        Functions.Execute("List",e)

    Case "tongji.htm"
        Functions.Execute("Statistics",e)
End
Select

2、自定义函数Filter用于生成筛选页面filter.htm：

Dim
e As
RequestEventArgs =
args(0)
Dim
wb As
New WeUI
wb.AddForm("","form1","list.htm")
With
wb.AddInputGroup("form1","ipg1","数据筛选")
    .AddSelect("product","产品","|PD01|PD02|PD03|PD04|PD05")
    .AddSelect("customer","客户","|CS01|CS02|CS03|CS04|CS05")
    .AddInput("startdate","开始日期","date")
    .AddInput("enddate","结束时间","date")
End
With
With
wb.AddButtonGroup("form1","btg1",True)
    .Add("btn1",
"确定",
"submit")
End
With
e.WriteString(wb.Build)

3、自定义函数GetFilter用于根据生成filter.htm提交的内容合成条件表达式：

Dim
e As
RequestEventArgs =
args(0)
Dim
wb As
WeUI = Args(1)
Dim
flt As
String
If
e.PostValues.ContainsKey("product")
Then
    flt = "产品
= '"
& e.PostValues("product")
& "'"
'合成条件
    wb.AppendCookie("product",
e.PostValues("product"),30)
'将值写入cookie中
Else
    wb.DeleteCookie("product")
'删除cookie
End
If
If
e.PostValues.ContainsKey("customer")
Then
    If flt
> "" Then
        flt =
flt &
" and "
    End If
    flt =
flt & "客户
= '"
& e.PostValues("customer")
& "'"
'合成条件
    wb.AppendCookie("customer",
e.PostValues("customer"))
'将值写入cookie中
Else
    wb.DeleteCookie("customer")
'删除cookie
End
If
If
e.PostValues.ContainsKey("startdate")
Then
    If flt
> "" Then
        flt =
flt &
" and "
    End If
    flt =
flt & "日期
>= '"
& e.PostValues("startdate")
& "'"
    wb.AppendCookie("startdate",
e.PostValues("startdate"))
Else
    wb.DeleteCookie("startdate")
End
If
If
e.PostValues.ContainsKey("enddate")
Then
    If flt
> "" Then
        flt =
flt &
" and "
    End If
    flt =
flt & "日期
<= '"
& e.PostValues("enddate")
& "'"
    wb.AppendCookie("enddate",
e.PostValues("enddate"))
Else
    wb.DeleteCookie("enddate")
End
If
Return
flt

提示：GetFilter函数需要输入的条件保存到Cookie中，而Coolie的保存和删除是通过WeUI完成的，所以在调用GetFilter的时候，需要将WeUI作为第二个参数传递过去。

4、自定义函数GetCookieFilter用于根据Cookie合成条件表达式：

Dim
flt As
String
Dim
e As
RequestEventArgs =
args(0)
If
e.Cookies.ContainsKey("product")
Then
    flt = "产品
= '"
& e.Cookies("product")
& "'"
End
If
If
e.Cookies.ContainsKey("customer")
Then
    If flt
> "" Then
        flt =
flt &
" and "
    End If
    flt =
flt & "客户
= '"
& e.Cookies("customer")
& "'"
End
If
If
e.Cookies.ContainsKey("startdate")
Then
    If flt
> "" Then
        flt =
flt &
" and "
    End If
    flt =
flt & "日期
>= '"
& e.Cookies("startdate")
& "'"
End
If
If
e.Cookies.ContainsKey("enddate")
Then
    If flt
> "" Then
        flt =
flt &
" and "
    End If
    flt =
flt & "日期
<= '"
& e.Cookies("enddate")
& "'"
End If
Return flt

5、List函数用于生成list.htm：

Dim
e As
RequestEventArgs =
args(0)
Dim
wb As
New WeUI
Dim
flt As
String
If
e.GetValues.ContainsKey("unfilter")
Then '如果是取消筛选
    wb.ClearCookie()
'清除Cookie
ElseIf
e.PostValues.Count
> 0
    flt =
Functions.Execute("GetFilter",e,
wb) '根据输入内容合成条件，注意WeUI也需要传递过去
Else
    flt = Functions.Execute("GetCookieFilter",e)
'根据Cookie合成条件
End
If
'获取要显示的页码
Dim
page As
Integer = 0
'默认page为0,显示第一页
Dim
pageRows As
Integer = 10
'每页10行
If
e.GetValues.ContainsKey("page")
Then  '如果地址中有page参数
    Integer.TryParse(e.GetValues("page"),
page) '提取page参数
End
If
Dim
StartRow As
Integer = page
\* pageRows + 1
'此页第一行
Dim
EndRow As
Integer = (page
+ 1) \* pageRows
'此页最后一行
'提取此页数据
Dim
cmd As
New SQLCommand
cmd.ConnectionName
= "orders" '记得设置数据源名称
cmd.CommandText
= "Select Count(\*) From {订单}"
If
flt > ""
Then
    cmd.CommandText
= cmd.CommandText
& " where "
& flt
End
If
Dim
Count As
Integer = cmd.ExecuteScalar()
'获取总的行数
Dim
Pages As
Integer = Math.Ceiling(Count/PageRows)
'计算出总页数
cmd.CommandText
= "Select \* From (Select Row\_Number() Over(Order by
日期) As [NO.], 产品,客户,数量,单价,日期 From 订单 "
If
flt > ""
Then
    cmd.CommandText
= cmd.CommandText
& " where "
& flt
End
If
cmd.CommandText
= cmd.CommandText
& ") As a "
cmd.CommandText
= cmd.CommandText
& "  Where [NO.]>=
" & StartRow
& " And [NO.] <= "
& EndRow
'合成网页
With
wb.AddTable("","Table1")
    .ActiveSheet =
"menu" '指定菜单
    .CreateFromDataTable(cmd.ExecuteReader)
End
With
With
wb.AddButtonGroup("","btg2",
False)
    If page >
0 Then
        .Add("btnFirst",
"第一页","","List.htm?page=0")
        .Add("btnPrev",
"上一页","","List.htm?page="
& page -
1)
    Else
        .Add("btnFirst",
"第一页","button").Kind
= 1
        .Add("btnPrev",
"上一页","button").Kind
= 1
    End If
    If Endrow
< count Then
        .Add("btnNext",
"下一页","","List.htm?page="
& page +
1)
        .Add("btnLast",
"最末页","","List.htm?page="
& pages -
1)
    Else
        .Add("btnNext",
"下一页","button").Kind
= 1
        .Add("btnLast",
"最末页","button").Kind
= 1
    End If
End
With
With
wb.AddActionSheet("","menu")
'设计菜单
    If flt =
"" Then
        .Add("mnuFilter",
"数据筛选","filter.htm")
    Else
        .Add("mnuUnFilter",
"取消筛选","list.htm?unfilter=true")
    End
If
    .Add("mnuStatistics",
"数据统计","tongji.htm")
    .Add("mnuCancel","取消","",True)
End
With
e.WriteString(wb.Build)

6、自定函数Statistics用于生成页面tongji.htm:

Dim
e As
RequestEventArgs =
args(0)
Dim
wb As
New WeUI
If
e.PostValues.Count
= 0 Then
'分组统计设置
    wb.AddForm("","form1","tongji.htm")
    With wb.AddCheckGroup("form1","rdg1","选择分组列")
        .Add("fz1","产品",)
        .Add("fz2","客户")
        .Add("fz3","年")
        .Add("fz4","月")
    End With
    With wb.AddCheckGroup("form1","rdg2","选择统计列")
        .Add("tj1","数量")
        .Add("tj2","金额")
    End With
    With wb.AddButtonGroup("form1","btg1",True)
        .Add("btn1",
"统计",
"submit")
    End With
Else
'显示统计结果
    Dim gp
As new
SQLGroupTableBuilder("统计表1","订单")
    gp.ConnectionName
= "orders"
    gp.Filter
= Functions.Execute("GetCookieFilter",e)
'根据Cookie合成条件
    If e.PostValues.ContainsKey("fz1")
Then
        gp.Groups.AddDef("产品")
    End If
    If e.PostValues.ContainsKey("fz2")
Then
        gp.Groups.AddDef("客户")
    End If
    If e.PostValues.ContainsKey("fz3")
Then
        gp.Groups.AddDef("日期",DateGroupEnum.Year,"年")
    End If
    If e.PostValues.ContainsKey("fz4")
Then
        gp.Groups.AddDef("日期",DateGroupEnum.Month,"月")
    End If
    If e.PostValues.ContainsKey("tj1")
Then
        gp.Totals.AddDef("数量")
    End If
    If e.PostValues.ContainsKey("tj2")
Then
        gp.Totals.AddExp("金额","数量
\* 单价")
    End If

If gp.Groups.Count
= 0 OrElse
gp.Totals.Count
= 0 Then
        wb.InsertHTML("请选择分组列和统计列!")
    Else
        With wb.AddTable("","Table1")
            .CreateFromDataTable(gp.Build(True))
        End With
        With wb.AddButtonGroup("","btg1",
False)  '水平排列
            .Add("btn6",
"重新统计","button","tongji.htm")
            .Add("btn7",
"返回列表","button","list.htm?page=0")
        End With
    End If
End
If
e.WriteString(wb.Build)

## 使用关联表


### 后台表结构

后台表结构


**后台表结构**

通过网页显示和编辑关联表，对于专业程序员也是一个不小的挑战，当然由于这是Foxtable，技术实现上是不会有多少难度的，只是在设计逻辑的理解上，一些用户可能会有困惑。

我们会提供一个完整的示例，不仅是为了方便大家理解，更重要的是，即使你暂时理解不了，直接在这个例子的基础上改改表名和列名，就能套用在自己的系统中。

接下来你会看到，整个任务的完成，基本不要求你懂网页设计，因为绝大多数任务都是直接通过Foxtable完成的。
而且代码数量很少，从客户端到服务端，从分页浏览后台数据，到从订单的增加、删除和修改，再到订单明细的增加、删除和修改，以及多个菜单和按钮的生成，完成所有这些任务，不过200行左右的代码而已。

我们首先介绍一下后台的表结构。

后台数据库有订单和订单明细两个表，二者通过订单编号建立关联，结构如下图所示：

订单明细表的金额，以及订单表的总数量和总金额，都是表达式列，后台数据库不存在这三列。

希望设计一个手机网页管理系统，该系统有要完成三个任务：

1、分页浏览订单
2、订单的增加、修改和删除
3、订单明细的增加、修改和删除。

**软件开发没有定式**

关联表的显示和编辑是一个综合性的例子，我会按照比较容易理解，且相对比较高效合理的方式来给大家编写这个例子。
大家掌握好这个例子之后，基本上就可以开发一些比较复杂的手机管理系统了。
但是软件开发是没有定式的，完成同样的任务，会有很多种方法，我的例子是针对初学者而言的，希望大家不要被例子局限了思路。

### 如何传递命令

如何传递命令


**如何传递命令**

网页是无法直接操作后台数据的，我们需要利用get方式，按照事先约定的方式，将各种参数传递给服务器，服务器根据收到的参数，来执行相应的操作。

例如要编辑一个订单，客户端肯定要将订单编号（或主键）传递给服务器，服务器才知道用户要编辑的是那一个订单，还需要将当前页码传递给服务器，这样编程完成之后，客户端才能正确返回原来的页面。

所以要编辑一个订单，客户端通常需要给服务器发送以下访问请求：

edit.htm?page=2&oid=161130078

page为页码，oid为订单编号，完整的意思是：

我目前位于第3页(页码从0开始)，我要编辑订单编号为161130078的订单，编辑完成之后，请让我返回第3页吧。

事先约定好每个页面的get参数的名称和含义，以便于通过get方式正确传递数据给服务器，是能否完成设计的关键，否则很容易将自己绕晕，最后难以为继。

在Foxtable开发网页管理系统，基本上就是两部分：

1、客户端发送包含get参数的访问请求给服务器。
2、服务端收到访问请求，从中提取get参数，执行相应的操作后，生成新的页面，发回给客户端。

所以接下来我要先理清楚每个页面要完成的任务，以及对应的get参数要求。

### list.htm的设计思路

list.htm的设计思路


**list.htm的设计思路**

首先我们需要一个页面来分页浏览订单，这个网页我们命名为list.htm。

为节省显示空间，list.htm只显示三个常用的按钮，分别是增加订单、上一页和下一页：

连续点击某个单元格，可以显示一个上拉菜单，通过这个菜单可以进行跟多的操作，例如编辑或删除当前订单：

list.htm的get参数说明：

* **page参数**

  page参数用于指定要显示的页面，例如：

  list.htm?page=2

  表示要显示第3页(页码从0开始编号)，如果省略page参数，则显示第一页。
* **deloid参数**

  deloid参数用于指定要删除订单的订单编号，例如：

  list.htm?page=2&deloid=161130078

  表示要先删除订单编号为161130078的订单，然后显示第3页。

### edit.htm的设计思路

edit.htm的设计思路


**edit.htm的设计思路**

通常我们还需要两个页面，分别用于增加订单和编辑订单。
我们可以按照之前的示例一样，用两个页面（addnew.htm和edit.htm）来完成这两项任务，简单也容易理解。

但实际上，不管是增加订单，还是编辑订单，其实都是一回事，前者是先增加一个订单再编辑这个订单，后者是直接编辑现有的订单
所以我们可以将二者合并为一个页面，用不同的get参数，来完成不同的任务，我们将这个页面命名为：edit.htm。

将新增和编辑合并在一个页面处理，编码会变得复杂一点，但是需要维护的页面和函数会减少一半，总的代码数量也会减少很多，还是值得的。
为便于大家理解，我们会对有关函数逐行讲述，但是对于代码逻辑能力不强的用户，我还是建议分开处理。

由于手机屏幕显示面积不大，而且WeUI的表格暂时没有数据编辑功能，所以订单明细的录入我们也采用输入框完成，例如：

为节省空间，edit.htm默认只显示三个按钮，连续点击订单明细表格中同一单元格，会出现一个上拉菜单：

**edit.htm的get参数说明**

通过edit.htm，我们可以：

1、编辑订单
2、新增订单
3、编辑订单明细
4、新增订单明细
5、删除订单明细

不同的任务用户不同的get参数来表示，我们首先约定所有get参数的名称和含义：

* **page参数**

  page参数表示用户在新增或编辑订单之前，在list.htm中正在浏览第几页数据。
* **oid**

  oid参数用于指定要编辑的订单的订单编号。
* **addnext参数**

  addnext是一个逻辑参数，用于表明是否需要新增一个订单明细。
* **did**

  did参数用于指定要编辑的订单明细的主键。
* **deldid**

  deldid参数用于指定要删除的订单明细的主键

下面我们分5种情况来介绍edit.htm的get参数的使用：

**编辑订单**

如果要编辑一个订单，需要向服务器发送访问请求：

edit.htm?page=2&oid=161203005

意思是我目前正在浏览第3页数据，现在要编辑订单编号为161203005的订单。

收到这个访问请求后，服务器返回的页面如下：

**新增订单**

如果要新增订单，需要向服务器发送访问请求：

edit.htm?page=2

服务器收到这个访问请求之后，知道用户正在浏览第3页，由于没有发现oid参数，所以知道用户要新增一个订单。
如是服务器新增一个订单，并自动生成订单编号。
另外，既然是新增订单，肯定也需要新增订单明细，所以服务器最后发送给用户的页面为：

**新增订单明细**

在edit.htm中，单击"增加明细"按钮，发送给服务器的访问请求为：

edit.htm?page=2&oid=161203005&addnext=true

服务器收到这个访问请求后，从get参数分析：

用户正在编辑编号为161203005的订单，之前正在list.htm浏览第3页数据，现在要新增一个订单明细。

如是服务器发送以下页面给用户：

**编辑订单明细**

在edit.htm中的订单明细表格中，连续点击同一单元格，从弹出的菜单中执行"编辑明细"，发送给服务器的访问请求为：

edit.htm?page=2&oid=161203005&did=567

服务器收到这个访问请求后，从get参数分析：

用户正在编辑编号为161203005的订单，之前正在list.htm浏览第3页数据，现在要编辑主键为567的订单明细。

如是服务器发送以下页面给用户：

**删除订单明细**在edit.htm中的订单明细表格中，连续点击同一单元格，从弹出的菜单中执行"删除明细"，发送给服务器的访问请求为：

edit.htm?page=2&oid=161203005&deldid=568

服务器收到这个访问请求后，从get参数分析：

用户正在编辑编号为161203005的订单，之前正在list.htm浏览第3页数据，现在要删除主键为568的订单明细。

如果服务器先删除主键为568的订单明细，然后将以下页面发送给用户，新的页面不再包括被删除的订单明细：

现在设计思路已经清晰，我们可以开始客户端和服务端的编码工作了。

### 准备JS文件

准备JS文件


**准备JS文件**

我们的代码分客户端和服务端两部分。
服务端就是Foxtable的HttpRequest事件。
客户端就是简单的JavaScript代码，用于按照我们之前约定的get参数规则，向服务器发送反问请求，非常简单。

在目录"d:\web\lib"新建一个文本文件"order.js"，内容为：

function edit(){
   location="edit.htm?page=" + table1.pagenumber + "&oid=" +
table1.primarykey;
}

function del(){
   location="list.htm?page=" + table1.pagenumber + "&deloid=" +
table1.primarykey;
}

function addnew(){
   location="edit.htm?page=" + table1.pagenumber;
}

function addDetail(){
   location=form1.action + "&addnext=true";
}

function editDetail(){
   location = form1.action + "&did=" + detailtable.primarykey;
}

function delDetail() {
   location = form1.action + "&deldid=" + detailtable.primarykey;
}

function calc(){
   document.getElementById("金额").value = document.getElementById("数量").value
\* document.getElementById("单价").value;
}

上代码中的table1为list.htm中的订单表格，form1为edit.htm中的输入表单，detailtable为edit.htm中的订单明细表格。

除了最后一个calc函数用于输入过程自动计算金额外，其他函数都是根据我们上一节
理顺
的get参数规则，根据要完成的任务向服务器发送访问请求，只是简单的字符串合并而已，都很好理解。

**一个例子**

以编辑订单为例，当我们在list.htm的菜单中执行“编辑订单”，会执行edit函数，该函数的代码为：

function edit(){
   location="edit.htm?page=" + table1.pagenumber + "&oid=" +
table1.primarykey;
}

假定我们正在访问第3页，选定订单的订单编号为161130078，此时table1.pagenumber等于2，table1.primarykey等于161130078，以上代码合成的链接为：

edit.htm?page=2&oid=161130078

等于告诉服务器：我正在浏览第3页，我现在要编辑订单编号为161130078的订单。

后面在介绍Foxtable端的代码时，还会对以上js函数逐个讲述。

**你有疑问？**

我估计少数用户会发出这样的疑问，JS代码文件明明存放在服务端，怎么就是客户端代码呢？
其实在运行的时候，JS代码文件会先被下载到客户端，然后再执行，用户可以通过浏览器查看JS文件的内容，这一点和普通的网页或图片没有不同，都是由客户端浏览器负责显示或执行的。
HttpRequest才是真正的服务端代码，直接在服务端运行，用户是看不到代码的。
所以千万不要在JS代码中出现敏感信息哦。

### HttpRequest事件代码

HttpRequest事件代码


**HttpRequest事件代码**

我计划所有任务都用自定义函数来完成，所以HttpRequest事件代码很简单：

Select
Case e.Path
    Case "list.htm"
        Functions.Execute("List",e)
'分页显示
    Case "edit.htm"
        If e.PostValues.Count
> 0 Then

Functions.Execute("Save",e)
'保存表单数据
        End If
        Functions.Execute("Edit",e)
'生成订单编辑页面
End
Select

由于edit.htm承担了太多的任务，为避免单个函数代码过长，我们用两个函数处理edit.htm，Save函数负责保存表单数据，Eidt函数负责生成网页。

接下来我们分别介绍这3个自定义函数，实际上有4个自定义函数，因为还有一个用于生成订单编号的函数。

### List函数

List函数


List函数

当用户访问list.htm时，服务器会将访问请求转给自定义函数list处理。

list函数用于分页显示数据，这里假定使用的是SQL
Server数据源，其代码为：

|  |  |
| --- | --- |
| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59  60  61 | Dim e As RequestEventArgs = args(0)  '订单删除代码  If e.GetValues.ContainsKey("deloid") Then  '如果提交了deloid参数,则删除对应的订单.      DataTables("订单").SQLDeleteFor("订单编号='" & e.GetValues("deloid") & "'")      DataTables("订单明细").SQLDeleteFor("订单编号='" & e.GetValues("deloid") & "'")  End If  '获取要显示的页  Dim page As Integer = 0 '默认page为0,显示第一页  Dim pageRows As Integer =  10 '每页10行  If e.GetValues.ContainsKey("page") Then   '如果地址中有page参数      Integer.TryParse(e.GetValues("page"), page)  '提取page参数  End If  Dim StartRow As Integer =  page \* pageRows + 1  '此页第一行  Dim EndRow As Integer = (page + 1) \*  pageRows '此页最后一行  '获取该页数据  Dim cmd As New  SQLCommand  cmd.ConnectionName = "orders"  '记得设置数据源名称  cmd.CommandText = "Select Count(\*) From {订单}"  Dim Count As Integer =  cmd.ExecuteScalar()  '获取总的行数  Dim Pages As Integer =  Math.Ceiling(Count/PageRows) '计算出总页数  cmd.CommandText = "Select \* From (Select  Row\_Number() Over(Order by  订单.订单编号 desc ) As RowNum,订单.订单编号,日期,客户,Sum(数量) As  数量,sum(数量\*单价) As  金额"  cmd.CommandText = cmd.CommandText &  " From  订单 Left JOIN  订单明细 ON  订单明细.订单编号 =  订单.订单编号 Group By {订单}.订单编号,日期,客户) As a "  cmd.CommandText = cmd.CommandText & "  Where RowNum >= " & StartRow & " And RowNum <= " &  EndRow  Dim dt As DataTable =  cmd.ExecuteReader  '根据此页数据生成表格  Dim wb As New  WeUI  With wb.AddTable("","Table1")      .PageNumber = page  '设置页码      .ActiveSheet = "menu"  '指定菜单      .Primarykey = "订单编号" '指定主键,只要是能唯一区分行的列即可,并非一定要表的实际主键.      .CreateFromDataTable(dt, False,"","","订单编号","客户","日期","数量","金额")  End With  '设计菜单  With wb.AddActionSheet("","menu")      .Add("mnudAdd", "增加订单").Attribute="onclick='addnew()'" '调用js函数      .Add("mnuEdit", "编辑订单").Attribute ="onclick='edit()'"      .Add("mnuDelete", "删除订单").Attribute ="onclick=""show('dlg1')"""      .Add("mnuFirst","第一页","List.htm?page=0",True)      .Add("mnuLast","最末页","List.htm?page=" & pages - 1)      .Add("mnuCancel","取消","",True)  End With  With wb.AddDialog("","dlg1", "删除确认","您确定要删除当前订单吗?")      .AddButton("btnCancel","取消").Kind = 1      .AddButton("btnOK","确定").Attribute = "onclick='del()'"  End With  '生成换页按钮  With wb.AddButtonGroup("","btg1", False)      .Add("btnAdd", "增加订单").Attribute = "onclick='addnew()'"      If page > 0  Then          .Add("btnPrev", "上一页","","List.htm?page=" & page - 1)       Else          .Add("btnPrev", "上一页").Kind = 1      End  If      If Endrow < count  Then          .Add("btnNext", "下一页","","List.htm?page=" & page + 1)       Else          .Add("btnNext", "下一页").Kind = 1      End  If  End With  wb.AppendHTML("<script src='./lib/order.js'></script>")  '引入脚本文件  e.WriteString(wb.Build) |

代码解析

list.htm一般带有一个page参数，例如：
list.htm?page=2
表示要显示第3页数据。

如果要删除订单，还需要带有deloid参数，例如：
list.htm?page=2&deloid=161130078
表示要删除编号为161130078的订单，然后显示第3页数据。

第3行代码判断GetValues是否由deloid参数。
如果有，则在第4行代码删除对应的订单，在第5行代码删除对应的订单明细。

第8行代码定义了一个变量page，这个变量表示要显示的页面，默认为0.，也就是显示第1页。
第10行到第12行代码，判断GetValues集合是否包括page参数，如果有的话， 将其转换为整数保存在变量page中。

第13行和第14行代码，分别计算出此页第一行数据的顺序号，和最后一行数据的顺序号。
第19行代码统计出订单表的总行数，第20行代码据此算出总页数。

第21行到第24行代码，利用SQL语句提取出这一页数据，保存在DataTable型变量dt中。
需要注意几点：
1、顺序号根据订单编号降序生成，保证新增订单显示在第一页。
2、后台的订单表其实没有数量和金额两列，所以要在select语句中用聚合函数计算出每个订单的数量和金额。
3、订单和订单明细表用的是Left Join方式联结，确保没有录入订单明细的订单，也能出现在查询结果中。

第27行到第32行代码根据这页数据生成表格。
第28行代码设置了表的页码。
第29行代码设置了表格的上拉菜单名称。
第30行代码指定了主键列名称，这个名称不一定是订单表真正的主键，只要是能唯一区分每个订单的列即可。

第34行到第41行生成了上拉菜单，菜单名称必须和第29行代码使用的名称保持一致。
第42行到第45行代码生成了一个对话框，用于删除订单。
第47到第59行代码生成了操作按钮。
除了上一页和下一页命令，其他命令都是调用js函数。
这些js函数定义在“d:\web\lib\order.js”文件中，我们之前已经对此进行了介绍。
第60行代码引用了这个js函数文件。

综上所述，list.htm默认只显示三个常用的按钮，分别是增加订单、上一页和下一页：

连续点击某个单元格，可以显示一个上拉菜单，通过这个菜单可以进行跟多的操作，例如编辑或删除当前订单：

现在我们结合具体代码，分别看看list.htm是如何实现新增订单、编辑订单和删除订单的：

**删除订单**

当我们在菜单中点击"删除订单"时，会显示一个对话框（第37行代码）：

如果在对话框中单击确定按钮，会执行js函数del(第44行代码)。


del函数的代码为：

function del(){
   location="list.htm?page=" + table1.pagenumber + "&deloid=" +
table1.primarykey;
}

假定我们正在访问第3页，选定订单的订单编号为161130078，此时table1.pagenumber等于2，table1.primarykey等于161130078，以上代码合成的链接为：

list.htm?page=2&deloid=161130078

服务器收到这个访问请求之后，触发HttpRequest事件，转给List函数负责处理，List函数执行第3行到第6行代码，删除编号为161130078的订单及其订单明细。

**编辑订单**

当我们在菜单中点击"编辑订单“时，会执行js函数edit，这个函数的代码为：

function edit(){
   location="edit.htm?page=" + table1.pagenumber + "&oid=" +
table1.primarykey;
}

假定我们正在访问第3页，选定订单的订单编号为161130078，此时table1.pagenumber等于2，table1.primarykey等于161130078，以上代码合成的链接为：

edit.htm?page=2&oid=161130078

服务器收到这个访问请求之后，触发HttpRequest事件，转给Edit函数负责处理，Edit函数是如何处理以上访问请求的，在介绍Edit函数的时候会详细讲述。

**增加订单**

当我们单击"增加订单"按钮时，会调用js函数addnew，这个函数的代码为：

function addnew(){
   location="edit.htm?page=" + table1.pagenumber;
}


假定我们正在访问第3页，此时table1.pagenumber等于2，以上代码合成的链接为：

edit.htm?page=2

服务器收到这个访问请求之后，触发HttpRequest事件，转给Edit函数负责处理，Edit函数是如何处理以上访问请求的，在介绍Edit函数的时候会详细讲述。

### Edit函数

Edit函数


**Edit函数**

Edit函数用于生成订单编辑页面edit.htm。

按照我们之前的设计思路，订单的增加与编辑，以及订单明细的增加、编辑和删除，都在这个页面完成，所以Edit函数的代码比较长，超过100行。

该函数的代码为：

|  |  |
| --- | --- |
| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99  100  101  102  103  104  105  106  107  108  109  110  111  112  113  114  115 | Dim e As RequestEventArgs = args(0)  Dim wb As New  weui  '删除订单明细  If e.GetValues.ContainsKey("deldid") Then      DataTables("订单明细").SQLDeleteFor("[\_Identify] = " &  e.GetValues("deldid"))  End If  '订单编辑  Dim pr As DataRow  '订单  Dim srs As List(of DataRow)  '订单明细集合  Dim Page As Integer  '页码变量  If e.GetValues.ContainsKey("page") Then   '如果地址中有page参数      Integer.TryParse(e.GetValues("page"), page)  '提取page参数  End If  If e.GetValues.ContainsKey("oid") = False Then '如果没有传递订单编号,则新增与一个订单      pr =  DataTables("订单").SQLAddNew() '      pr("订单编号") = Functions.Execute("GetOrderID") '利用自定义函数GetOrderID为新增订单生成编号.      pr("日期") = Date.Today()  Else '如果传递了订单编号,则找出此订单进行编辑      pr = DataTables("订单").SQLFind("订单编号='" & e.GetValues("oid") & "'")      If  pr Is  Nothing Then '多用户情况下,必须考虑其他用户删除订单的可能.          wb.InSertHtml("此订单已被其他用户删除!")          e.WriteString(wb.Build)          Return  ""  '必须返回      End  If      srs =   DataTables("订单明细").SQLSelect("订单编号='" & pr("订单编号")  & "'") '获取订单明细    End  If  Dim url As String = "edit.htm?page=" & page &  "&oid=" & pr("订单编号")  '传递页码和订单编号  wb.AddForm("","form1",url)  With wb.AddInputGroup("form1","ipg1",iif(e.GetValues.ContainsKey("oid"),"编辑订单","新增订单"))      With .AddInput("订单编号","编号","text")          .Value = pr("订单编号")          .Readonly = True      End  With      .AddInput("客户","客户","text").Value = pr("客户")      .AddInput("日期","日期","date").Value = pr("日期")      If e.GetValues.ContainsKey("oid")  Then  '如果是旧订单,则汇总显示数量和金额            Dim qty As Integer          Dim amt As Integer          For Each sr As DataRow In srs              qty = qty + sr("数量")              amt = amt + sr("数量") \* sr("单价")          Next          .AddInput("总数量","总数量","number").value = qty          .AddInput("总金额","总金额","number").value = amt      End  If  End With  '订单明细编辑  Dim mr As DataRow  '要编辑的订单明细  Dim IsNew As Boolean  '此变量用于标记是否要新增明细  If e.GetValues.ContainsKey("oid") = False OrElse e.GetValues.ContainsKey("addnext") '如果是新增订单,或这包括addnext参数      IsNew =  True '将IsNew参数设置为True,表明需要新增订单明细  ElseIf e.GetValues.ContainsKey("did") Then  '如果传递了订单明细主键      mr =  DataTables("订单明细").SQLFind("[\_Identify]=" & e.GetValues("did")) '找出此订单明细进行编辑  End If  If IsNew OrElse mr IsNot Nothing  Then      With wb.AddInputGroup("form1","ipg2",iif(IsNew,"新增明细","编辑明细"))          .Attribute = "onchange='calc()'"  '调用js函数,自动计算金额          If  IsNew Then  '如果是新增订单明细              .AddInput("产品","产品","text")              .AddInput("数量","数量","number")              .AddInput("单价","单价","number").Step= "0.01"              .AddInput("金额","金额","number")          Else              .AddHiddenValue("DetailID",mr("\_Identify")) '插入一个隐藏的订单明细主键,此值将随表单数据一并提交到服务器.              .AddInput("产品","产品","text").Value = mr("产品")              .AddInput("数量","数量","number").value = mr("数量")              With .AddInput("单价","单价","number")                  .Step= "0.01"                  .value = mr("单价")              End  With              .AddInput("金额","金额","number").value = mr("数量") \* mr("单价") '后台没有金额列,要通过数量和单价计算得出          End If      End  With  End If  '生成订单明细表格  If e.GetValues.ContainsKey("oid") AndAlso  srs.count > 0 Then '如果不是新增订单,且订单明细行数大于0,则生成订单明细表格.      With wb.AddTable("form1","detailTable") '为了区分,明细表的名字设为detailTable          .head.AddRow("产品","数量","单价","金额")          .ActiveSheet = "menu"  '指定菜单          For  Each sr  As DataRow In srs              With .Body.AddRow(sr("产品"),sr("数量"),sr("单价"))                  .AddCell(sr("数量") \* sr("单价"))                  .Primarykey = sr("\_Identify") '为此行指定主键值              End  With          Next      End  With      '设计菜单      With wb.AddActionSheet("","menu")          .Add("mnudAdd", "增加明细").Attribute="onclick='addDetail()'" '调用js函数          .Add("mnuEdit", "编辑明细").Attribute ="onclick='editDetail()'"          .Add("mnuDelete", "删除明细").Attribute ="onclick=""show('dlg1')"""          .Add("mnuCancel","取消","",True)      End  With  End If  With wb.AddDialog("","dlg1", "删除确认","您确定要删除当前明细吗?")      .AddButton("btnCancel","取消").Kind = 1      .AddButton("btnOK","确定").Attribute = "onclick='delDetail()'"  End With  With wb.AddButtonGroup("form1","btg1",False)      .Add("btn1", "增加明细", "submit").FormAction = url & "&addnext=true"  '加上addnext参数,表示保存后进入增加明细状态      .Add("btn2", "保存", "submit")  '正常提交,保存后进入编辑状态      If  e.GetValues.ContainsKey("oid") = False Then '如过是新增订单          .Add("btn3", "取消", "button","list.htm?page=" & page & "&deloid=" & pr("订单编号")) '删除新增订单后返回列表      ElseIf  IsNew OrElse mr IsNot Nothing  Then '如果在给旧订单新增或修改明细,则直接返回编辑状态          .Add("btn3", "取消", "button",url) '返回编辑状态      Else          .Add("btn3", "返回", "button","list.htm?page=" & page) '返回列表      End  If  End With  pr.Save() '必须保存,而且必须在最后保存,因为SQLAddNew增加的行,保存之后就会销毁,无法再调用  If e.PostValues.Count > 0 Then '如果是通过提交按钮访问,则给一个已经保存的提示给用户,时长500毫秒      wb.AddToast("","t1", "已经保存",0).Msec= 500  End If  wb.AppendHTML("<script src='./lib/order.js'></script>")  '引入脚本文件  e.WriteString(wb.Build) '生成网页 |

我们前面已经提到，上面的函数完成了5项任务，所以我们要分5种情况来解析代码。
我强烈建议你直接看上面的代码，自行分析，代码的逻辑很清晰，而且我加上了注释，理解起来不困难，实在看不懂的时候，再来看下面的解析不迟。
只要你明白了之前已经理顺的设计思路，看懂上述代码应该不会有问题的。

**增加订单**

我们已经知道，当用户在list.htm中，单击"增加订单"按钮，会向服务器发送访问请求：
edit.htm?page=2
服务端收到这个访问请求后，触发HttpRequest事件，将请求转给Edit函数处理。

以下是edit函数的处理流程：

第11行到第13行代码，从GetValues集合中提取page参数，保存在变量page中，page变量的值等于2。
由于没有传递oid参数，第14行代码的条件成立，执行第15行到第17行代码。
第15行代码新增一个订单。
第16行代码利用自定义函数GetOrderID为新订单生成订单编号。
第17行代码将订单日期设置为当天日期。

假定新增订单编号为161203006，第27行代码合成了一个链接，保存在url中，内容为：
edit.htm?page=2&oid=161203006
第28行代码新增一个表单，数据接收链接为url，即：edit.htm?page=2&oid=161203006。
第29到第46行代码，生成了订单输入框。
由于第36行代码的条件不成立，不会生成总数量和总金额输入框。

第50行代码的条件成立，IsNew参数设置为True，表明需要新增一个订单明细。
第59到第62行代码，为订单明细生成输入框。

第57行代码调用了js函数calc，这个函数的代码为：
function calc(){
    document.getElementById("金额").value = document.getElementById("数量").value \*
document.getElementById("单价").value;
}
这样用户输入订单明细的数量和单价后，能自动计算出金额。
注意这里没有单独给数量和单价输入框定义onchange事件，而是给他们的父容器定义onchange事件，在父容器定义的事件，对于子元素有效，JavaScript这个特性真不错。

第76行行代码的条件不成立，所以不会生成明细表格及相关菜单。
第101行代码定义了一个提交按钮，标题为"保存"。
第100行代码定义了一个提交按钮，标题为"增加明细",数据接收链接为:edit.htm?page=2&oid=161203006&addnext=true
这样用户单击"保存明细"后,服务器通过分许get参数，就知道用户要保存本次输入结果，然后开始下一个明细的输入。
第103行代码定义了一个取消按钮，链接为:list.htm?page=2&deloid=161203006
这样用户单击取消按钮，会返回list.htm，并显示第3页数据，在显示数据之前会先删除新增加的订单。

第111行代码判断本次访问是否含有有表单数据。
如果本次访问包括有表单数据，则在第112行代码创建一个Toast，显示0.5秒，内容为"已经保存".
需要注意的时候，表单数据的保存是通过Save函数完成的，Edit函数只负责生成网页内容。

综上所示，edit.htm在新增订单状态下的显示内容为：

编辑订单

假定客户端正在访问list.htm，浏览到第3页，选择该页中订单编号为161203005的订单，然后执行菜单命令“编辑订单”。
服务端会收到以下访问请求：
edit.htm?page=2&oid=161203005
服务端收到这个访问请求后，触发HttpRequest事件，将请求转给Edit函数处理。

下面是Edit函数的处理流程，和增加订单相同的部分就不重复讲述了：

第19行代码根据传递过来的订单编号找出订单，保存在变量pr中。
第25行代码提取出这个订单所有的订单明细，保存在集合srs中。
第29行到第46行代码，为这个订单生成了输入框。
由于后台的订单表并不存在总数量和总金额两列，所以第37到第44行代码，累加了订单明细的数量和金额，赋值给对应输入框的value属性。

由于没有传递addnext和did参数，所以第50行代码和第52行代码的条件都不成立。
因此第55行代码的条件也不成立，本次请求不会生成订单明细输入框。

第76到第94行代码，生成订单明细表格，以及操作明细的菜单。
由于订单明细表的金额是表达式列，无法用CreateDataTable自动生成，所以只能逐行生成表格，逐行设置主键。

第107行代码定义了一个返回按钮，链接为:list.htm?page=2
这样用户单击返回按钮，会返回list.htm，并显示第3页数据。

综上所述，在编辑订单状态下，edit.htm显示内容为：

**新增明细**

假定用户正在编辑编号为161203005，单击了"新增明细"按钮。
服务器会收到以下访问请求：
edit.htm?page=2&oid=161203005&addnext=true
服务端收到这个访问请求后，触发HttpRequest事件，由于PostValue集合包括有表单数据，所以HttpRequest事件先执行Save函数保存数据，然后将请求转给Edit函数处理。

Edit函数的处理流程和编辑订单基本相同，下面只讲述不同的地方：

由于访问请求中包括addnext参数，第50行代码的条件成立。
第51行代码将变量IsNew设置为True，表明需要新增明细。
第55行和第58行代码的条件成立，执行第59到第62行代码，为新增明细定义输入框。

第104行代码的条件成立，第105代码生成一个取消按钮，这个取消按钮的链接地址为：
edit.htm?page=2&oid=161203005
返回按钮的类型不是submit，所以单击这个按钮，不会提交数据，而是直接返回到订单编辑状态，等于取消了本次新增明细操作。

综上所述，在新增明细状态下，edit.htm的显示内容为：

小提示：如果想直接增加订单明细，不想保存当前输入结果，可以点击菜单中的"增加明细"命令。

**编辑明细**

假定用户正在编辑编号为161203005的订单，连续点击订单明细表格的同一单元格，在弹出的菜单中执行"编辑明细"命令，会调用js函数editDetail。
editDetail函数的代码为：
function editDetail(){
   location = form1.action + "&did=" + detailtable.primarykey;
}
form1.action获取表单的action属性(数据接收链接)，值为:edit.htm?page=2&oid=161203005
假定用户点击的订单明细的主键为567，那么执行js函数editDetail，会向服务器发出访问请求：
edit.htm?page=2&oid=161203005&did=567
服务端收到这个访问请求后，触发HttpRequest事件，将请求转给Edit函数处理。

edit函数的处理流程和新增明细基本相同，不同的部分只有：

由于访问请求中包括did参数(订单明细主键)，第52行代码的条件成立。
第53行代码根据did参数，找出对应的订单明细，保存再变量mr中。
第64到第71行代码，为此订单明细生成输入框。
第64行代码，插入了一个隐藏的输入框，名为DetailID，值为此明细的主键。
这样服务器收到用户提交的表单数据后，通过判断PostValues集合是否包括DetailID参数，就能知道是用户新增明细还是编辑明细。
第71行代码，由于订单明细表的金额列是表达式列，并不存在于后台数据表，所以需要用代码计算出金额，并赋值给金额输入框的value属性

综上所述，在编辑明细状态下，edit.htm的显示内容为：

**删除明细**

假定用户正在编辑编号为161203005，连续点击订单明细表格的同一单元格，在弹出的菜单中执行"删除明细"命令，
会显示一个对话框(第91行代码)：

如果用户单击确定，会调用js函数delDetail（第97行代码），该函数的代码为：
function delDetail() {
   location = form1.action + "&deldid=" + detailtable.primarykey;
}
假定用户在订单明细表格中点击的是主键为568的明细，那么执行js函数delDetail，会向服务器发出访问请求：
edit.htm?page=2&oid=161203005&deldid=568
服务端收到这个访问请求后，触发HttpRequest事件，将请求转给Edit函数处理。

Edit函数的处理流程如下：

第4行代码判断GetValues集合是否包括deldid参数。
如果包括过deldid参数，则执行第5行代码，删除主键等于deldid参数的订单明细。
接下来处理流程，和编辑订单请求完全相同，就不重复了。

综上所述，删除订单明细后，edit.htm重新进入订单编辑状态，显示内容为：

### Save函数

Save函数


**Save函数**

Save函数负责保存表单内容，包括订单和订单明细，其代码为：

|  |  |
| --- | --- |
| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36 | Dim e As RequestEventArgs = args(0)  '保存订单  Dim dr As DataRow =  DataTables("订单").SQLFind("订单编号='" & e.PostValues("订单编号") & "'")  Dim nms() As String =  {"客户","日期"}  '""  If dr IsNot Nothing Then      For Each nm As String In nms          If e.PostValues.ContainsKey(nm) Then              dr(nm)= e.PostValues(nm)          End  If      Next  End If  dr.Save()  '保存明细  Dim valid As Boolean  '用于判断用户是否 输入了订单明细数据  nms = New  String() {"产品","数量","单价" }  For Each nm As String In nms      If e.PostValues.ContainsKey(nm) Then          valid = True  '如果 输入了订单明细数据,将valid变量设置为True      End  If  Next  If valid Then '如果提交了订单明细数据      Dim sr As DataRow      If e.PostValues.ContainsKey("DetailID") Then  '如果传递了订单明细主键          sr =  DataTables("订单明细").SQLFind("[\_Identify]=" & e.PostValues("DetailID"))          If  sr Is  Nothing  Then   '多用户环境,必须考虑其他用户删除此明细的可能,避免程序报错              Return ""          End If      Else          sr = DataTables("订单明细").SQLAddNew() '增加一个订单明细          sr("订单编号") = dr("订单编号")      End If      For Each nm As String  In nms          sr(nm) = e.PostValues(nm)      Next      sr.Save()  '必须保存,而且必须在最后保存,因为用SQLAddNew增加的行,一旦保存,就不能再引用此行  End If |

上述代码很好理解，只是需要注意第23行代码，通过判断PostValues集合中是是否包括DetailID，来判断出用户是编辑明细，还是新增明细。
你要是不记得DetailID是怎么来的，请回头看一下Edit函数的代码。
另外代码还采取了措施，避免保存空的订单明细，用户必须给订单明细至少输入一列的内容，此明细才会被保存。

SQLAddNew和主键

用SQLAddNew增加行的时候，并没有真正在后台数据库增加行，直到用代码保存此行，此行才会写入后台数据库，保存之后，此行不能再访问。
这带来一个问题，如果表使用的是自动增量型主键，那么行的主键只能在保存后生成，但是SQLAddNew增加的行在保存后又无法再访问，所以我们是无法获取新增行的主键
值。
如果你需要获取行的主键，请使用DataTable的AddNew方法增加行，保存之后，会自动生成行的主键，还可以继续访问此行，获取包括主键在内的所有列的数据。

### GetOrderID函数

GetOrderID函数


**GetOrderID函数**

GetOrderID函数用于生成订单编号

一开始我是直接在Edit函数中编写代码生成订单编号的，后来之所以将生成编号的代码单独提出来做成一个函数，是考虑到用户可能需要直接在Foxtable输入订单。

编号格式为两位年两位月和两位日，后接三位顺序号。

GetOrderID函数代码为：

Static
Lastbh As
String
'通过这个Static变量可以访问上一次生成的编号,避免重复Compute
Dim prefix
As String =
Format(Date.now,"yyMMdd")
'本次编号前缀
If Lastbh >""
AndAlso Lastbh.SubString(0,6)
= prefix Then
'如果上一次生成编号的前缀和本次相同
    Lastbh =
prefix &
Format(Cint(Lastbh.SubString(6,3))
+ 1,"000")
'在上次编号的基础上递增1
Else
    '取数据表中同前缀的最大编号
    Dim max
As String=DataTables("订单").SQLCompute("Max(订单编号)","订单编号
like '" &
prefix &
"%'")
    If max =
"" Then
'如果不存在同前缀的编号
        Lastbh  =
prefix &
"001"
'同前缀的第一个编号
    Else
        Lastbh =
prefix &
Format(CInt(max.SubString(6,3))
+ 1,"000")
'在同前缀最大编号的基础上递增1
    End
If
End
If
Return
Lastbh

注意上述代码中，Lastbh是一个静态变量，每次执行都可以通过此变量获取上一次生成的编号，这样处理的好处是，不用次次执行SQLCompute生成新的编号，提高了效率。

关于静态变量，参考：[使用静态变量](http://www.foxtable.com/webhelp/scr/1061.htm)

### 继续扩展功能


#### 加上数据筛选功能

加上数据筛选功能


**加上数据筛选功能**

**知识准备**

为了方便大家理解掌握，不要被枝节问题干扰，所以前面的例子并没有设计数据筛选功能。

当然设计一个普通的数据筛选并不复杂，可以参考：

[数据筛选](0115.htm)

[数据筛选和分页](0116.htm)

不过本节的筛选涉及到父表(订单)和子表(订单明细)，所以处理起来有点特别。

我们知道，一个订单可以订单多个产品，假定我们要筛选出订购过产品"PD01"的订单，由于订单表并不包括产品列，需要用如下的语句查询：

Select \* From {订单} Where 订单编号 in (Select Distinct
订单编号 From 订单明细 Where 产品 = 'PD01')

上面的查询有两个Select语句，执行步骤为：

1、从订单明细表中找出产品为PD01的不重复的订单编号，执行红色部分的Select语句：

Select Distinct 订单编号 From 订单明细 Where
产品 = 'PD01'

2、然后从订单表中找出订单编号包括在以上查询结果中的订单：

Select \* From {订单} Where 订单编号
in (第一次查询的结果)

**设计要求**

1、菜单中增加一个"筛选数据"命令：

2、执行“数据筛选”命令，显示数据筛选页(filter.htm)：

3、在数据筛选页输入条件后，单击筛选按钮，显示符合条件的数据，且此时菜单会显示一个“撤销筛选”命令：

**设计思路**

筛选部分设计的思路非常简单，在list函数中增加代码，根据用户输入的条件合成条件表达式，为避免list函数的代码过程，我们可以另外增加一个函数(GetFilter)用于合成条件表达式。

至于撤销筛选，我们可以传递一个约定的get参数给list.htm，例如：

List.htm?page=0&unfilter=true

list函数判断存在unfilter参数后，清除筛选条件后，显示第一个数据。

**相关代码**

1、在order.js中增加一个函数，代码为：

function filter() {
    location="filter.htm?page=" + table1.pagenumber
}

在菜单中点击"筛选数据"命令，将执行此函数。

2、增加一个自定义函数Filter，用于生成筛选页面(Filter.htm)：

Dim
e As
RequestEventArgs =
args(0)
Dim
wb As
New
weui
Dim
Page As
Integer
If
e.GetValues.ContainsKey("page")
Then
    Integer.TryParse(e.GetValues("page"),
page)
End
If
wb.AddForm("","form1","list.htm?page=0")
With
wb.AddInputGroup("form1","ipg1","数据筛选")
    .AddInput("订单编号","订单编号","text")
    .AddInput("客户","客户","text")
    .AddInput("产品","产品","text")
    .AddInput("开始日期","开始日期","date")
    .AddInput("结束日期","结束日期","date")
End
With
With
wb.AddButtonGroup("form1","btg1",False)
    .Add("btn1",
"筛选", "submit")
    .Add("btn1",
"返回", "button","list.htm?page="
& Page)
'返回原页面
End
With
e.WriteString(wb.Build())

注意表单的数据接收页为：

list.htm?page=0

将输入的条件传递给List函数，有List函数负责筛选出数据，并显示第一页符合条件的数据。

3、增加一个GetFilter函数，供List函数调用，用于根据Filter.htm的输入结果合成条件表达式，这段代码有点长，不过很好理解：

Dim
bh As
String
'订单编号
Dim
cp As
String
'产品
Dim
kh As
String
'客户
Dim
rq1 As
String
'开始日期
Dim
rq2 As
String
'结束日期
Dim
Filter As
String
'条件表达式
Dim
e As
RequestEventArgs =
args(0)
Dim
wb As
WeUI = args(1)
If
e.PostValues.Count
> 0 Then
'如果是通过表单输入了筛选条件
    If e.PostValues.ContainsKey("订单编号")
Then
        bh =
e.PostValues("订单编号")
        wb.Appendcookie("bh",
bh)
    Else
        wb.DeleteCookie("bh")
    End If
    If e.PostValues.ContainsKey("产品")
Then
        cp =
e.PostValues("产品")
        wb.Appendcookie("cp",
cp)
    Else
        wb.DeleteCookie("cp")
    End If
    If e.PostValues.ContainsKey("客户")
Then
        kh =
e.PostValues("客户")
        wb.Appendcookie("kh",
kh)
    Else
        wb.DeleteCookie("kh")
    End If
    If e.PostValues.ContainsKey("开始日期")
Then
        rq1=
e.PostValues("开始日期")
        wb.Appendcookie("rq1",
rq1)
    Else
        wb.DeleteCookie("rq1")
    End If
    If e.PostValues.ContainsKey("结束日期")
Then
        rq2 =
e.PostValues("结束日期")
        wb.Appendcookie("rq2",rq2)
    Else
        wb.DeleteCookie("rq2")
    End
If
Else
'否则从Cookie中提取筛选条件
    If e.Cookies.ContainsKey("bh")
Then
        bh =
e.Cookies("bh")

End
If
    If e.Cookies.ContainsKey("cp")
Then

cp =
e.Cookies("cp")
    End If
    If e.Cookies.ContainsKey("kh")
Then
        kh =
e.Cookies("kh")
    End If
    If e.Cookies.ContainsKey("rq1")
Then
        rq1 =
e.Cookies("rq1")
    End If
    If e.Cookies.ContainsKey("rq2")
Then
        rq2 =
e.Cookies("rq2")
    End
If
End
If
If
bh > ""
Then
'如果输入了订单编号,其他条件可以忽略
    Return
"产品编号
= '"
& bh
&
"'"
End
If
If
cp > ""
Then
'如果输入产品
    '产品列在子表订单明细,不是在父表订单,注意这种根据子表列合成父表条件的技巧
    Filter =
"订单.订单编号
in (Select Distinct
订单编号
From {订单明细}
Where
产品=
'"
& cp
&
"')"
End
If
If
kh > ""
Then
    If Filter
> "" Then
        Filter =
Filter &
" And "
    End If
    Filter =
Filter &
"客户
= '"
& kh
&
"'"
End
If
If
rq1 > ""
Then
    If Filter
> "" Then
        Filter =
Filter &
" And "
    End If
    Filter =
Filter &
"日期
>= '"
& rq1
&
"'"
End
If
If
rq2 > ""
Then
    If Filter
> "" Then
        Filter =
Filter &
" And "
    End If
    Filter =
Filter &
"日期
<= '"
& rq2
&
"'"
End
If
Return
Filter

4、修改HttpRequest事件代码，粗体部分是新加上的：

Select
Case e.Path
    Case "list.htm"
        Functions.Execute("List",e)
'分页显示
    Case "edit.htm"
        If e.PostValues.Count
> 0 Then
            Functions.Execute("Save",e)
'保存表单数据
        End If
        Functions.Execute("Edit",e)
'生成订单编辑页面
**Case "filter.htm"
        Functions.Execute("Filter",e)**
    Case "order.xls"

Functions.Execute("CreateXLS",e)
End
Select

5、最后我们需要对List函数稍作修改，增加一些内容，新增加的内容我用粗体显示，可以看到增加内容很少：

Dim
e As
RequestEventArgs =
args(0)
Dim
wb As
New
WeUI
'订单删除代码
If
e.GetValues.ContainsKey("deloid")
Then
'如果提交了deloid参数,则删除对应的订单.
    DataTables("订单").SQLDeleteFor("订单编号='"
& e.GetValues("deloid")
& "'")
    DataTables("订单明细").SQLDeleteFor("订单编号='"
& e.GetValues("deloid")
& "'")
End
If
'获取要显示的页
Dim
page As
Integer = 0
'默认page为0,显示第一页
Dim
pageRows As
Integer = 10
'每页10行
If
e.GetValues.ContainsKey("page")
Then
'如果地址中有page参数
    Integer.TryParse(e.GetValues("page"),
page)
'提取page参数
End
If
Dim
StartRow As
Integer = page
\* pageRows + 1
'此页第一行
Dim
EndRow As
Integer = (page
+ 1) \* pageRows
'此页最后一行
**Dim****Filter As
String
'条件表达式
If
e.GetValues.ContainsKey("unfilter")
Then
    wb.ClearCookie()
'清除Cookie
Else
    Filter =
Functions.Execute("GetFilter",e，wb)'合成条件表达式
End
If**
'获取该页数据
Dim
cmd As
New
SQLCommand
cmd.ConnectionName
= "orders"
'记得设置数据源名称
cmd.CommandText
= "Select Count(\*) From {订单}"
& iif(Filter
> "", " Where "
& Filter,
"")
Dim
Count As
Integer = cmd.ExecuteScalar()
'获取总的行数
Dim
Pages As
Integer = Math.Ceiling(Count/PageRows)
'计算出总页数
cmd.CommandText
= "Select \* From (Select
Row\_Number() Over(Order by
订单.订单编号
desc ) As RowNum,订单.订单编号,日期,客户,Sum(数量)
As 数量,sum(数量\*单价)
As 金额"
&
\_
" From
订单
Left JOIN
订单明细
ON 订单明细.订单编号
= 订单.订单编号
"**& iif(Filter
> "", " Where "
& Filter ,"")**
& \_

" Group By {订单}.订单编号,日期,客户)
As a  Where RowNum >= "
& StartRow
& " And RowNum <= "
&
EndRow
Dim
dt As
DataTable = cmd.ExecuteReader
'根据此页数据生成表格
With
wb.AddTable("","Table1")
    .PageNumber
= page '设置页码
    .ActiveSheet =
"menu" '指定菜单
    .Primarykey =
"订单编号"
'指定主键,只要是能唯一区分行的列即可,并非一定要表的实际主键.
    .CreateFromDataTable(dt,
False,"","","订单编号","客户","日期","数量","金额")
End
With
'设计菜单
With
wb.AddActionSheet("","menu")
    .Add("mnudAdd",
"增加订单").Attribute="onclick='addnew()'"
'调用js函数
    .Add("mnuEdit",
"编辑订单").Attribute
="onclick='edit()'"
    .Add("mnuDelete",
"删除订单").Attribute
="onclick=""show('dlg1')"""
    .Add("mnuFirst","第一页","List.htm?page=0",True)
    .Add("mnuLast","最末页","List.htm?page="
& pages -
1)
**If Filter
= "" Then
        .Add("mnuFilter","筛选数据").Attribute
= "onclick='filter()'"
    Else
        .Add("mnuUnFilter","撤销筛选","List.htm?page=0&unfilter=true")
    End** **If**
    .Add("mnuCancel","取消","",True)
End
With
With
wb.AddDialog("","dlg1",
"删除确认","您确定要删除当前订单吗?")
    .AddButton("btnCancel","取消").Kind
= 1
    .AddButton("btnOK","确定").Attribute
= "onclick='del()'"
End
With
'生成换页按钮
With
wb.AddButtonGroup("","btg1",
False)
    .Add("btnAdd",
"增加订单").Attribute
= "onclick='addnew()'"
    If page
> 0 Then
        .Add("btnPrev",
"上一页","","List.htm?page="
& page -
1)
    Else
        .Add("btnPrev",
"上一页").Kind
= 1
    End If
    If Endrow
< count Then
        .Add("btnNext",
"下一页","","List.htm?page="
& page +
1)
    Else
        .Add("btnNext",
"下一页").Kind
= 1
    End
If
End
With
wb.AppendHTML("<script
src='./lib/order.js'></script>")
'引入脚本文件
e.WriteString(wb.Build)

#### 生成Excel格式的订单

生成Excel格式的订单


**生成Excel格式的订单**

本节的任务是在订单编辑页面，加上一个按钮，用于生成Excel格式的订单：

整个设计逻辑很简单，假定当前订单编号为“161203001”，用户单击“生成Excel格式订单”按钮后，会向服务器发送访问请求：

order.xls?oid=161203001

HttpRequest事件收到这个访问请求后，将请求转给自定义函数(CreateXLS)处理，此函数提取出编号为161203001的订单和订单明细，据此生成Excel报表，并将生成的报表发送给用户。

所有的代码加起来只有18行：

**设计步骤**

1、首先要设计好一个Excel报表模板：

2、增加一个自定义函数CreateXls，用于生成Excel报表：

Dim
e As
RequestEventArgs =
args(0)
Dim
oid As
String
If
e.GetValues.ContainsKey("oid")
Then
    oid = e.GetValues("oid")
Else
    Return
""
End
If
Dim
Book As
New XLS.Book(ProjectPath
&
"Attachments\订单.xls")
Dim
fl As
String =
ProjectPath &
"Reports\订单.xls"
book.AddDataTable("订单","orders","Select
\* from {订单}
where
订单编号=
'"
& oid
& "'")
'添加父表
book.AddDataTable("订单明细","orders","Select
\*,数量
\* 单价
As 金额
from {订单明细}
where
订单编号=
'"
& oid
& "'")
'添加子表
book.AddRelation("订单","订单编号","订单明细","订单编号")
'建立关联
e.WriteBook(book,"订单"
& oid
& ".xls",False)

代码逻辑很简单，根据传递过来的订单编号，找出对应的订单和订单明细，生成Excel报表。

参考：

[根据后台数据生成Excel报表](0149.htm)

[提升Excel报表效率](0148.htm)

3、修改HttpRequst事件代码，粗体部分是我们新增加的代码：

Select
Case e.Path
    Case "list.htm"
        Functions.Execute("List",e)
'分页显示
    Case "edit.htm"
        If e.PostValues.Count
> 0 Then
            Functions.Execute("Save",e)
'保存表单数据
        End If
        Functions.Execute("Edit",e)
'生成订单编辑页面
    Case "filter.htm"
        Functions.Execute("Filter",e)
**Case "order.xls"** **Functions.Execute("CreateXLS",e)**
End
Select

3、最后在Edit函数增3行代码（最后面的粗体部分），用于添加生成Excel报表的按钮：

Dim
e As
RequestEventArgs =
args(0)
Dim
wb As
New
weui
'删除订单明细
If
e.GetValues.ContainsKey("deldid")
Then
    DataTables("订单明细").SQLDeleteFor("[\_Identify]
= " & e.GetValues("deldid"))
End
If
'订单编辑
Dim
pr As
DataRow
'订单
Dim
srs As
List(of
DataRow)
'订单明细集合
Dim
Page As
Integer
'页码变量
If
e.GetValues.ContainsKey("page")
Then
'如果地址中有page参数
    Integer.TryParse(e.GetValues("page"),
page)
'提取page参数
End
If
If
e.GetValues.ContainsKey("oid")
= False Then
'如果没有传递订单编号,则新增与一个订单
    pr = DataTables("订单").SQLAddNew()
'
    pr("订单编号")
= Functions.Execute("GetOrderID")
'利用自定义函数GetOrderID为新增订单生成编号.
    pr("日期")
= Date.Today()
Else
'如果传递了订单编号,则找出此订单进行编辑
    pr =
DataTables("订单").SQLFind("订单编号='"
& e.GetValues("oid")
& "'")
    If pr
Is Nothing
Then
'多用户情况下,必须考虑其他用户删除订单的可能.
        wb.InSertHtml("此订单已被其他用户删除!")
        e.WriteString(wb.Build)
        Return ""
'必须返回
    End If
    srs =
DataTables("订单明细").SQLSelect("订单编号='"
& pr("订单编号")
& "'")
'获取订单明细
End
If
Dim
url As
String = "edit.htm?page="
& page
&  "&oid="
& pr("订单编号")
'传递页码和订单编号
wb.AddForm("","form1",url)
With
wb.AddInputGroup("form1","ipg1",iif(e.GetValues.ContainsKey("oid"),"编辑订单","新增订单"))
    With .AddInput("订单编号","编号","text")
        .Value = pr("订单编号")
        .Readonly =
True
    End With
    .AddInput("客户","客户","text").Value
= pr("客户")
    .AddInput("日期","日期","date").Value
= pr("日期")
    If e.GetValues.ContainsKey("oid")
Then
'如果是旧订单,则汇总显示数量和金额
        Dim qty
As Integer

Dim
amt As
Integer
        For Each
sr As
DataRow In
srs
            qty =
qty + sr("数量")
            amt = amt
+ sr("数量")
\* sr("单价")
        Next
        .AddInput("总数量","总数量","number").value
= qty
        .AddInput("总金额","总金额","number").value
= amt
    End
If
End
With
'订单明细编辑
Dim
mr As
DataRow
'要编辑的订单明细
Dim
IsNew As
Boolean
'此变量用于标记是否要新增明细
If
e.GetValues.ContainsKey("oid")
= False OrElse
e.GetValues.ContainsKey("addnext")
'如果是新增订单,或这包括addnext参数
    IsNew = True
'将IsNew参数设置为True,表明需要新增订单明细
ElseIf
e.GetValues.ContainsKey("did")
Then
'如果传递了订单明细主键
    mr = DataTables("订单明细").SQLFind("[\_Identify]="
& e.GetValues("did"))
'找出此订单明细进行编辑
End
If
If
IsNew OrElse
mr IsNot
Nothing  Then
    With wb.AddInputGroup("form1","ipg2",iif(IsNew,"新增明细","编辑明细"))
        .Attribute =
"onchange='calc()'" '调用js函数,自动计算金额
        If IsNew
Then
'如果是新增订单明细
            .AddInput("产品","产品","text")
            .AddInput("数量","数量","number")
            .AddInput("单价","单价","number").Step=
"0.01"
            .AddInput("金额","金额","number")
        Else
            .AddHiddenValue("DetailID",mr("\_Identify"))
'插入一个隐藏的订单明细主键,此值将随表单数据一并提交到服务器.
            .AddInput("产品","产品","text").Value
= mr("产品")
            .AddInput("数量","数量","number").value
= mr("数量")
            With .AddInput("单价","单价","number")
                .Step=
"0.01"
                .value =
mr("单价")
            End With
            .AddInput("金额","金额","number").value
= mr("数量")
\* mr("单价")
'后台没有金额列,要通过数量和单价计算得出
        End If
    End
With
End
If
'生成订单明细表格
If
e.GetValues.ContainsKey("oid")
AndAlso  srs.count
> 0 Then
'如果不是新增订单,且订单明细行数大于0,则生成订单明细表格.
    With wb.AddTable("form1","detailTable")
'为了区分,明细表的名字设为detailTable
        .head.AddRow("产品","数量","单价","金额")
        .ActiveSheet =
"menu"
'指定菜单
        For Each
sr As
DataRow In
srs
            With .Body.AddRow(sr("产品"),sr("数量"),sr("单价"))
                .AddCell(sr("数量")
\* sr("单价"))
                .Primarykey =
sr("\_Identify")
'为此行指定主键值
            End
With
        Next
    End With
    '设计菜单
    With wb.AddActionSheet("","menu")
        .Add("mnudAdd",
"增加明细").Attribute="onclick='addDetail()'"
'调用js函数
        .Add("mnuEdit",
"编辑明细").Attribute
="onclick='editDetail()'"
        .Add("mnuDelete",
"删除明细").Attribute
="onclick=""show('dlg1')"""
        .Add("mnuCancel","取消","",True)
    End
With
End
If
With
wb.AddDialog("","dlg1",
"删除确认","您确定要删除当前明细吗?")
    .AddButton("btnCancel","取消").Kind
= 1

.AddButton("btnOK","确定").Attribute
= "onclick='delDetail()'"
End
With
With
wb.AddButtonGroup("form1","btg1",False)
    .Add("btn1",
"增加明细",
"submit").FormAction
= url &
"&addnext=true"
'加上addnext参数,表示保存后进入增加明细状态
    .Add("btn2",
"保存",
"submit")
'正常提交,保存后进入编辑状态
    If  e.GetValues.ContainsKey("oid")
= False Then
'如过是新增订单
        .Add("btn3",
"取消",
"button","list.htm?page="
& page
& "&deloid="
& pr("订单编号"))
'删除新增订单后返回列表
    ElseIf IsNew
OrElse mr
IsNot Nothing
Then
'如果在给旧订单新增或修改明细,则直接返回编辑状态
        .Add("btn3",
"取消",
"button",url)
'返回编辑状态
    Else
        .Add("btn3",
"返回",
"button","list.htm?page="
& page)
'返回列表
    End
If
End
With
**With****wb.AddButtonGroup("form1","btg2",False)
       .Add("btn4",
"生成Excel格式订单",
"button","order.xls?oid="
& pr("订单编号"))

End
With**
pr.Save()
'必须保存,而且必须在最后保存,因为SQLAddNew增加的行,保存之后就会销毁,无法再调用
If
e.PostValues.Count
> 0 Then
'如果是通过提交按钮访问,则给一个已经保存的提示给用户,时长500毫秒
    wb.AddToast("","t1",
"已经保存",0).Msec=
500
End
If
wb.AppendHTML("<script
src='./lib/order.js'></script>")
'引入脚本文件
e.WriteString(wb.Build)
'生成网页