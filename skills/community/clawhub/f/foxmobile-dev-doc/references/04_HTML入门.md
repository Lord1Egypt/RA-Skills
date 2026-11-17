# HTML入门


## Hello World

Hello Word


**Hello Word**

我们先用一个经典的例子，来说明如何使用Foxtable实现http服务。

首先是一个重要提示：要启动http服务，必须以管理员身份运行Foxtable。

你可以在Windows的桌面上右击Foxtable的快捷方式，在快捷菜单中的单击属性命令，然后在兼容性页面中勾选“以管理员身份运行此程序”：

启动Foxtable后，将下面的代码复制到命令窗口执行：

HttpServer.Prefixes.Add("http://127.0.0.1/")
HttpServer.Start()

然后在菜单的“管理项目”功能区，单击“网络监视器”，将“HttpRequest”事件的代码设置为：

e.WriteString("Hello
World")

现在打开你的浏览器，输入地址：http://127.0.0.1，会显示如下内容：

是的，我们只用了3行代码，就建立了一个简单的http服务系统。

通过下面的代码，可以关闭http服务：

HttpServer.Close()

现在为了接下来的测试方便，我们可以设计一个窗口，窗口有两个按钮，分别用于开启和关闭http服务：

按钮的代码就是前面介绍的，就不重复了。

注意每次开启新的服务之前，都必须关闭之前的服务，否则会无效或出现错误提示。

## 服务器IP

服务器IP


**服务器IP**

上一节我们搭建了一个简单的http服务，你只能在本机访问这个http服务，因为127.0.0.1表示的是本机IP。

我们可以设置多个IP，假定服务器的局域网IP是：192.168.0.100，我们可以将开启服务按钮的代码改为：

HttpServer.Prefixes.Add("http://127.0.0.1/")
HttpServer.Prefixes.Add("http://192.168.0.100/")
HttpServer.Start()

这样局域网中的其他电脑，就能通过局域网IP来访问我们的http服务了：

如果服务器有公网IP，一样可以加入，这样外网用户就能通过公网IP来访问我们的http服务。

如果服务器有多个IP，可以用下面的代码来开启http服务：

HttpServer.Prefixes.Add("http://\*/")
HttpServer.Start()

这样用户就可以通过指向服务器的任何一个IP来访问http服务，包括本机IP、局域网IP和公网IP。

建议今后都采用以上代码来开启http服务，这样就无需因IP的变动而修改代码了。

如果是公网，可以设置域名指向你的服务器，让用户通过域名来访问你的http服务。

提示：为了测试方便，接下来所有例子，都将通过127.0.0.1来访问。

## 服务器端口

服务器端口


**服务器端口**

如果我们不指定端口，那么http服务使用的就是默认的端口80。

下面的代码：

HttpServer.Prefixes.Add("http://\*/")
HttpServer.Start()

等同于：

HttpServer.Prefixes.Add("http://\*:80/")
HttpServer.Start()

有时，我们需要给自己的http服务更换端口。
例如你公司已经有了一台web服务器，现在你需要利用这台服务器运行Foxtable的http服务，那么就不能使用80端口了，因为这样会和原来的web服务发生冲突。

换个端口开启http服务很简单，例如：

HttpServer.Prefixes.Add("http://\*:32177/")
HttpServer.Start()

现在你要访问这个http服务，地址必须加上端口号才行：

为了方便，就下来的例子还是使用默认的端口80。

## 增加入站规则

入站规则


**入站规则**

如果你在另一台电脑访问我们新建立的http服务，很可能无法访问。

通常这是防火墙造成的，我们可以新建一个入站规则，让防火墙允许客户端访问我们的http服务。

以windows 10自带的防火墙为例，新建一个入站规则的步骤为：

1、在Windows的控制面板，打开“Windows 防火墙”。

2、在“Windows 防火墙”窗口，单击“高级设置”。

3、在“高级设置”窗口，单击“入站规则”，然后在右侧单击“新建规则”。

4、选择规则类型为“端口”：

5、协议类型选择TCP，并输入你的http服务所采用的端口号：

5、接下来选择允许接入：

6、应用规则勾选所有：

7、最后输入规则名称即可，名称可以随便取，最好方便识别。

## 开启多个服务

开启多个服务


**开启多个服务**

你可以一次开启多个http服务，例如：

HttpServer.Prefixes.Add("http://\*/")
HttpServer.Prefixes.Add("http://\*:32177/")
HttpServer.Prefixes.Add("http://192.168.0.100:32188/")
HttpServer.Start()

上面的代码开启了三个http服务，头两个服务可以通过指向服务器的任何ip来访问，例如：

http://127.0.0.1/
http://192.168.0.100/

http://127.0.0.1:32177/
http://192.168.0.100:32177/

第三个服务则只能根据固定的IP地址访问：

http://192.168.0.100:32188/

重要提示：当你通过多个IP开启服务时，只要有一个IP错误，所有服务都是不能启动的。

## 显示不同的内容

显示不同的内容


**显示不同的内容**

在上一节中，我们开启了三个http服务，当我们分别访问这三个服务时，显示的内容都是“Hello Word”。
显然，这不符合实际需要，真正的http服务应该能根据用户输入的不同地址，显示不同的内容。

HttpRequest事件的e参数有很多，其中有三个e参数，用于获取用户访问路径的各部分。

Host: 返回IP地址(或域名)
Port：返回端口号
Path：返回路径，含文件名。

假定用户输入的访问路径是"http://192.168.0.100:32188/fox/",这三个e参数的返回值分别是：

Host: 192.168.0.100
Port: 32188
Path: fox

假定用户输入访问路径是"http://192.168.0.100:32188/fox/china.htm"，这三个e参数的返回值分别是：

Host: 192.168.0.100
Port: 32188
Path: fox\china.htm

注意：

1、e参数path中的路径分割符号是"\"，不是"/"。
2、尽量通过路径和文件名来区分用户的访问请求，不要占用太多端口，因为端口是有限的。

现在就可以根据用户访问的不同端口、路径和和文件，甚至是不同的IP，来显示不同的内容，例如将HttpRequest的代码设置为：

If
e.host =
"127.0.0.1" Then
    e.WriteString("你是本地用户")
Else
    Select Case
e.Port
        Case 80
            e.WriteString("Hello
World")

Case
32177
            e.WriteString("你好,世界")
        Case 32188
            If
e.path = "fox"
Then
                e.WriteString("你好,狐表用户")
            ElseIf e.path
= "fox\china.htm" Then
'注意这里的路径分隔符是"\"
                e.WriteString("你好,中国狐表用户")

Else
                e.WriteString("你好,未找到网页")
            End If
        Case
Else
            e.WriteString("你好,端口错误")
    End
Select
End
If

如果你通过地址“http://192.168.0.100:32188/fox”访问http服务，将显示:

如果你通过地址"http://192.168.0.100:32188/fox/china.htm"访问http服务，将显示：

## 关于WriteString

关于WriteString


**关于WriteString**

在前面的例子中，在HttpReuest用下面的代码：

e.WriteString("Hello
World")

在浏览器中显示了下面的内容：

需要注意的是，每次只能执行一次WriteString或WriteFile(后面会介绍)，例如下面的代码是无法正常运行的：

e.WriteString("Hello
World")
e.WriteString("Hello
China")
'这一行会出错

需要将两个字符串合并为一个，再用WriteString写入浏览器，例如：

Dim
rs As String = "Hello World"
rs = rs
& vbcrlf
& "Hello China"
e.WriteString(rs)

在浏览器中显示的内容是：

你肯定会奇怪，vbcrlf是回车换行，按理应该分两行显示，怎么上面的内容只显示了一行呢？
这就是涉及到HTML标签的知识，在HTML中，连续的多个空格或换行，都会被显示为1个空格，而换行用<br/>表示。

所以要分开两行显示，正确的HttpReuest事件代码是：

Dim
rs As
String =
"Hello World"
rs =
rs &
"<br/>Hello China"
e.WriteString(rs)

在浏览器显示的内容是：

如果要分段显示文字，可以将段落放在<p>和</p>之间，例如将HttpReuest事件代码设置为：

Dim
rs As
String =
"<p>Foxtable首先是一个优秀的应用软件,你不需要编写任何代码,即可高效完成日常数据管理工作.</p>"
rs = rs
&
"<p>同时Foxtable又是一个高效的.net平台开发工具,专门针对数据管理软件的开发作了大量的优化</p>"
e.WriteString(rs)

在浏览器显示的结果为：

用a标签可以插入超链接，例如将HttpReuest事件代码设置为：

Dim
rs As
String =
"<a href='http://www.foxtable.com/'>单击此处</a>访问Foxtable主页"
e.WriteString(rs)

<a>标签的href属性指定链接地址，属性用单引号括起来，<a>和</a>之间为要显示的文本，上述代码在浏览器显示的结果为：

HTML的标签有很多，我们并不打算一一介绍，教会大家HTML不是我们的任务，有人比我们做得更好，有兴趣的话，可以访问：

<http://www.w3school.com.cn/html/index.asp>

通常不超过半天时间就可以掌握了。

## 关于网页设计

关于网页设计


**关于网页设计**

上一节我们接触了一些常用的HTML标签，但我们不会有专门的章节来介绍HTML标签。
因为我们并不打算教会大家网页设计，这不是我们的长处，已经有很多比我们更擅长的人在做这项工作。
我只想告诉大家，如果你掌握了网页设计，你之前所有的知识，包括HTML、CSS、JavaScript和JQuery等等，在Foxtable都能继续派上用场。

**可以不会网页设计**

如果你完全不会网页设计，也没有关系，Foxtable内置了网页自动生成功能，不需要有任何的网页设计知识，一样可以设计出具备专业效果的网页来。

例如你只需寥寥十来行代码，就可以设计出下面的网页来：

如果你想提前了解一下，可以参考：[使用框架生成网页](0011.htm)

**会网页设计更好**

自动生成，意味着轻松，也意味着约束，如果你懂一些网页设计，你就可以突破这种约束，甚至可以完全放弃Foxtable的自动网页生成功能。

如果你打算学习网页设计，我给你推荐一个网站：<http://www.w3school.com.cn/h.asp>

对于一般用户来说，花一两天的时间掌握[HTML](http://www.w3school.com.cn/html/index.asp)、[HTML5](http://www.w3school.com.cn/html5/index.asp)和[CSS](http://www.w3school.com.cn/css/index.asp)，就足够使用了，如果想做一些动态的效果，可以再掌握一下[JavaScript](http://www.w3school.com.cn/js/index.asp)和[CSS3](http://www.w3school.com.cn/css3/index.asp)。

## 使用StringBuilder

使用StringBuilder


**使用StringBuilder**

前面的例子，我们是直接将字符串组合起来，然后写入客户端的浏览器：

Dim
rs As
String =
"Hello World"
rs =
rs &
"<br/>Hello China"
e.WriteString(rs)

如果要写入的内容比较多，这种方法是比较低效的，因为.net合并字符串的效率并不好。

我们建议用[StringBuilder](2097.htm)来合并字符串，例如：

Dim
sb As
New
StringBuilder
sb.AppendLine("Hello
World")
sb.AppendLine("<br/>Hello
China")
e.WriteString(sb.ToString)

生成的网页内容越多，使用[StringBuilder](2097.htm)的效率优势就越明显，今后例子都将采用这种方式。

## 用HTML生成网页

用HTML生成网页


**用HTML生成网页**

本节内容适合已经掌握HTML的用户，其实不管你是否已经掌握HTML，建议都学习一下，因为：真的很简单！

现在我们将HttpRequest事件代码改为：

Dim
sb As
New
StringBuilder
sb.AppendLine("<form
enctype='multipart/form-data' method='post'
id='form1'
name='form1'>")
sb.AppendLine("产品:
<input name='cp' id='cp'><br/><br/>")
sb.AppendLine("客户:
<input name='kh' id='kh'><br/><br/>")
sb.AppendLine("雇员:
<input name='gy' id='gy'><br/><br/>")
sb.AppendLine("单价:
<input type='number' name='dj' id='dj'><br/><br/>")
sb.AppendLine("折扣:
<input type='number' name='zk' id='zk' min='0' max='0.15' step='0.01'><br/><br/>")
sb.AppendLine("数量:
<input type='number' name='sl' id='sl'><br/><br/>")
sb.AppendLine("日期:
<input type='date' name='rq' id='rq'><br/><br/>")
sb.AppendLine("<input
Type='submit' name='Sumbit' id='Sumbit' value='确定'>")
sb.AppendLine("</form>")
e.WriteString(sb.ToString)

我们用上面的代码生成了一个表单，在Chorme浏览器中的显示效果为：

即使你完全不懂HTML，看懂上面的代码也没有问题，以下面这一行代码为例：

sb.AppendLine("折扣:
<input type='number' name='zk' id='zk' min='0' max='0.15' step='0.01'><br/><br/>")

表示增加一个输入框，输入类型为数字(type='number')，允许最小值为0(min='0')，允许最大值为0.15(max='0.15'),允许输入精度为0.01(step='0.01')，id为zk(id='zk')，name为zk(name='zk')。

在不同的浏览器，上述代码生成的页面会有不同的显示效果，例如对于日期输入框，Chorme可以显示一个下拉
日历供选择，而且你只能输入日期，对于IE来说，这个日期输入框和普通的文本输入框没有任何差别。

教会你HTML不是我的任务，有人干这个我们擅长很多，如果你有兴趣，可以访问：<http://www.w3school.com.cn/html/index.asp>，通常不会超过半天时间就能基本掌握。

## 不用StringBuilder

不用StringBuilder


**不用StringBuilder**

本文档的网页绝大多数都是用StringBuilder的AppendLine组合合成，这是因为网页要和Foxtable的数据结合，用StringBuilder适合运行过程中动态合成。

我们也可以直接发送，例如：

Dim
html
As

String
=
<![CDATA[
<form enctype='multipart/form-data' method='post' id='form1' name='form1'>
产品:
<input name='cp' id='cp'><br/><br/>
客户:
<input name='kh' id='kh'><br/><br/>
雇员:
<input name='gy' id='gy'><br/><br/>
单价:
<input type='number' name='dj' id='dj'><br/><br/>
折扣:
<input type='number' name='zk' id='zk' min='0' max='0.15' step='0.01'><br/><br/>
数量:
<input type='number' name='sl' id='sl'><br/><br/>
日期:
<input type='date' name='rq' id='rq'><br/><br/>
<input Type='submit' name='Sumbit' id='Sumbit' value='确定'>
</form>
]]>.Value
e.WriteString(html)

结果和上一节完全相同。

请注意，第一行的<![CDATA[和最后一行的]]>.Value是语法要求，并不包括在网页内容中，切记。

对于少量需要动态改变的内容，可以先用字符串的Replace方法查找替换，然后再发送。

## 生成结构完整的网页

生成结构完整的网页


**生成结构完整的网页**

在浏览器打开我们上一节生成的网页，右击，查看源代码，可以看到其代码为：

没有head？ 没有body？ 如果你接触过HTML网页设计，你会知道这不是一个结构完整的网页。

你也不要担心，正如我们所演示的，目前所有的浏览器，都能正确解释上面的代码。

不过遵循规范总是没有错，我们来改进一下HttpRequst事件的代码：

|  |
| --- |
| Dim html  As  String =  <![CDATA[  <!doctype html>  <html>  <head>  <meta charset='utf-8'>  <title>表单</title>  </head>  <body>  <form enctype='multipart/form-data' method='post' id='form1' name='form1'>  产品: <input name='cp' id='cp'><br/><br/>  客户: <input name='kh' id='kh'><br/><br/>  雇员: <input name='gy' id='gy'><br/><br/>  单价: <input Type='number' name='dj' id='dj'><br/><br/>  折扣: <input Type='number' name='zk' id='zk' min='0' max='0.15' step='0.01'><br/><br/>  数量: <input Type='number' name='sl' id='sl'><br/><br/>  日期: <input Type='date' name='rq' id='rq'><br/><br/>  <input Type='submit' name='Sumbit' id='Sumbit' value='确定'>  </form>  </body>  </html>  ]]>.Value  e.WriteString(html) |

现在生成的就是一个结构完整的网页，在浏览器看到的代码是：

## 我想显示一个图片

我想显示一个图片


**我想显示一个图片**本节内容适合已经掌握HTML的用户，其实不管你是否已经掌握HTML，建议你学习一下，因为：真的很简单！

在D盘建立一个名为web的目录，复制一个图片文件到这个目录，假定图片文件的名称是abc.jpg。

我们将HttpRequest事件的代码改为：

Dim
sb As
New
StringBuilder
sb.Appendline("我想显示一个图片<br/>")
sb.AppendLine("<img
src='abc.jpg'>")
e.WriteString(sb.ToString())

在浏览器显示的结果为：

img标签用于显示图片，其src属性为要显示的图片文件名称。

不过图片并没有显示，这是意料之中的，因为服务端并没有发送图片文件到浏览器。

浏览器其实是分两步来显示这个网页的：

1、首先获取网页内容：

我想显示一个图片<br/>
<img src='abc.jpg'>

2、然后浏览器解析网页内容，发现要显示一个图片"abc.jpg"，如是又向服务器发送访问请求：

http://127.0.0.1/abc.jpg

要显示图片，服务器必须对这个访问请求对出响应，将后台的图片"abc.jpg"发送给客户端的浏览器，浏览器则显示收到的图片。

实际上不单单是图片，网页中引用的任何文件，包括js、css等等，都会单独向服务器发出下载这个文件的请求，服务器必须对此做出响应。

据此，我们修改HttpRequest事件代码为：

Dim
fl As
String =
"d:\web\" &
e.path '合成含路径的文件名
If
filesys.FileExists(fl) '如果是请求一个已经存在的文件
    e.WriteFile(fl) '则发送此文件
Else
    Dim sb
As New
StringBuilder
    sb.Appendline("我想显示一个图片<br/><br/>")
    sb.AppendLine("<img
src='abc.jpg'>")
    e.WriteString(sb.ToString())
End
If

现在浏览器可以正常显示图片了：

提示：HttpRequest事件的WriteFile方法用于向客户端发送本地文件。

**安全问题**

上面的代码是不严谨的，因为用户可以下载"d:\web"目录下的所有文件，包括非图片文件。

我们需要进行一些判断，限制用户只能下载图片文件，为此可以将HttpRequest事件代码改为：

Dim
fl As
String =
"d:\web\" &
e.path
If
filesys.FileExists(fl) '如果是请求一个已经存在的文件
    Dim idx
As Integer
= fl.LastIndexOf(".")
    Dim ext
As String
= fl.SubString(idx)
    Select Case
ext
        Case
".jpg",".gif",".png",".bmp",".wmf"
 '只允许请求图片文件
            e.WriteFile(fl)
    End
Select
Else
    Dim sb
As New
StringBuilder
    sb.Appendline("我想显示一个图片<br/><br/>")
    sb.AppendLine("<img
src='abc.jpg'>")
    e.WriteString(sb.ToString())
End
If

## 文件引用的路径问题

文件引用的路径问题


**文件引用的路径问题**

对于稍具规模的系统，为便于维护，我们很少会将所有文件放在同一个文件夹中。

那么某一文件夹中的网页，如何引用其他文件夹中的文件呢。

**使用绝对路径**

如果被引用文件的路径是固定的，那么使用绝对路径即可。

假定"d:\web"为网页根目录，图片文件"abc.jpg"位于该目录的"images"子目录下。
那么在任何路径的网页，都可以通过路径"/images/abc.jpg"引用此图片，"/"表示根目录"d:\web"，所以"/images/abc.jpg"就表示"d:\web\images\abc.jpg"。

**示例**

现在将文件"abc.jpg"复制到目录"d:\web\images"下，然后将HttpRequest事件代码改为：

Dim
fl As
String = "d:\web\"
& e.path
If
filesys.FileExists(fl)
    Dim idx
As Integer =
fl.LastIndexOf(".")
    Dim ext
As String  =
fl.SubString(idx)
    Select Case
ext
        Case
".jpg",".gif",".png",".bmp",".wmf"
            e.WriteFile(fl)
    End
Select
Else
    Dim sb
As New
StringBuilder
    sb.Appendline("我想显示一个图片<br/><br/>")
    Select Case
e.path
        Case "a.htm"
            sb.AppendLine("<img
src='/images/abc.jpg'>")
        Case "sub1\a.htm"
            sb.AppendLine("<img
src='/images/abc.jpg'>")
         Case
"sub1\sub2\a.htm"
            sb.AppendLine("<img
src='/images/abc.jpg'>")
    End Select
    e.WriteString(sb.ToString())
End
If

现在你通过下面三个网页访问HttpServer：

http://127.0.0.1/a.htm
http://127.0.0.1/sub1/a.htm
http://127.0.0.1/sub1/sub2/a.htm

可以看到，三个不同路径的网页，使用相同的引用路径""\images\abc.jpg""，都可以正常显示图片"d:\web\images\abc.jpg"。

**使用相对路径**

如果要使用相对路径，需要用到两个重要的符号，一个是表示网页所在的目录的"."，一个是表示父目录的".."

假定网页所在目录为"d:\web"目录，图片文件位于该目录的images子目录下，也就是"d:\web\images"目录下，那么使用相对路径的代码为：

<img src='./images/abc.jpg'>

"."表示网页所在目录"d:\web"，所以"./images"表示"d:\web\images"

假定网页所在目录为"d:\web\sale"目录，图片文件位于"d:\web\images"目录下，
那么使用相对路径的代码为：

<img src='../images/abc.jpg'>

".."表示"d:\web\sale"的父目录，也就是"d:\web"，
所以"../images"表示"d:\web\images"。

**示例**

现在将文件"abc.jpg"复制到目录"d:\web\images"下，然后将HttpRequest事件代码改为：

Dim
fl As
String =
"d:\web\" &
e.path
If
filesys.FileExists(fl)
    Dim idx
As Integer
= fl.LastIndexOf(".")
    Dim ext
As String
= fl.SubString(idx)
    Select Case
ext
        Case
".jpg",".gif",".png",".bmp",".wmf"
            e.WriteFile(fl)
    End
Select
Else
    Dim sb
As New
StringBuilder
    sb.Appendline("我想显示一个图片<br/><br/>")
    Select
Case e.path
        Case
"a.htm"
            sb.AppendLine("<img
src='.\images\abc.jpg'>")
        Case "sub1\a.htm"
            sb.AppendLine("<img
src='..\images\abc.jpg'>")
         Case
"sub1\sub2\a.htm"
            sb.AppendLine("<img
src='..\..\images\abc.jpg'>")
    End Select
    e.WriteString(sb.ToString())
End
If

现在你通过下面三个网页访问HttpServer：

http://127.0.0.1/a.htm
http://127.0.0.1/sub1/a.htm
http://127.0.0.1/sub1/sub2/a.htm

都可以正常显示"d:\web\images"的图片"abc.jpg".

## 使用JavaScript文件

使用JavaScript文件


**使用JavaScript文件**

本节内容要使用到JavaScript。

即使您没有掌握JavaScript，也没有关系，因为真的很简单。

假定在以下网页中，希望输入单价、折扣和数量后，能即时计算出金额：

要完成这个任务，就需要使用Javascript来编写脚本了。

**知识准备**

下面会对本节要使用的JavaScript知识做一个简单的介绍。

教会你JavaScript，并不是我们的任务，
如果你有兴趣进行进一步的了解，可以访问：<http://www.w3school.com.cn/b.asp>

我个人建议你花上一两天时间，通过上述网页，掌握一下JavaScript的基础知识。

首先是一个重要的提示：JavaScript是区分大小写的，例如calc和Calc是两个不同的变量或函数，逻辑值是true和false，写成True和False，也是不行的。

**1、如何引用表单元素**

我们在设计表单的时候，需要给输入框指定id属性和name属性，例如：

sb.appendLine("单价:
<input Type='number' name='dj' id='dj'>")

表示定义了一个输入框用于输入单价，这个输入框的id和name都是"dj"，id和name属性可以设置为不同的值，除非有特殊需要，一般设置为相同的值即可。

我们可以在js代码中直接通过id属性引用这个输入框，例如：

dj.value

表示单价输入框的值，这是一种简写方式，使用起来很方便。

还有一种更为标准的写法，例如下面的代码，同样是表示单价输入框的值：

document.getElementById('dj').value

前一种方法更为简洁，但后一种方法更为标准，多数编程书籍使用的都是后一种方法，本帮助文件两种都用。

**2、网页事件**

网页中所有元素都是有事件的，例如单击按钮，会触发按钮的onclick事件，修改输入框的内容，会触发输入框的onchange事件。

我们可以在设计网页的时候，指定事件触发后要执行的代码，例如：

sb.appendLine("单价:
<input Type='number' name='dj' id='dj' onchange='calc()'>")


表示修改单价输入框的内容后，执行calc函数，注意函数名是区分大小写的，括号也是不能省略的。

**3、在哪里写代码**

JavaScript代码一般放在单独的文本文件中，后缀名为js，你可以直接用记事本编写js代码，我个人喜欢结合nodepad++和Dreamweaver编写，前者可以让我更方便地分析代码结构，后者可以帮我检查出语法错误。

编写好的js代码一般放在某个子目录下，例如本帮助文件所有的js代码，都放在"d:\web\lib"目录下。

编写好的js代码，并不会自动自动生效，我们在设计网页的时候，还需要将编写好的js代码文件，引入到网页中，例如：

sb.appendline("<script src='./lib/calc.js'></script>")

表示将lib子目录下的calc.js文件引入到网页中。

有了上面的知识，我们就能很轻松地完成自动计算金额的任务了。

**设计步骤**

1、在"d:\web"目录下，建立一个子目录lib，在这个子目录中新建一个文本文件，文件名为"calc.js"，文件内容为：

function calc(){
    je.value = dj.value \* sl.value \* (1 - zk.value);
}

上述的代码定义了一个名为calc的函数，用于根据单价(dj)、数量(sl)和折扣(zk)的值，计算出金额。

2、然后修改HttpRequest事件的代码，在有变动的地方，我加上了注释：

Dim
fl As
String = "d:\web\"
& e.path
If
filesys.FileExists(fl)

Dim idx
As Integer =
fl.LastIndexOf(".")

Dim ext
As String  =
fl.SubString(idx)

Select Case
ext

Case ".jpg",".gif",".png",".bmp",".wmf",".js"
'这里加上了js扩展名

e.WriteFile(fl)

End
Select
Else

Dim
html
As

String
=
<![CDATA[
    <!doctype html>
    <html>
    <head>
    <meta charset='utf-8'>
    <title>表单</title>
    </head>
    <body>
    <form enctype='multipart/form-data' method='post' id='form1'
name='form1'>
    产品:
<input name='cp' id='cp'><br/><br/>
    客户:
<input name='kh' id='kh'><br/><br/>
    雇员:
<input name='gy' id='gy'><br/><br/>
    单价:
<input Type='number' name='dj' id='dj' onchange='calc()'><br/><br/>
    折扣:
<input Type='number' name='zk' id='zk' step='0.01' onchange='calc()'><br/><br/>
    数量:
<input Type='number' name='sl' id='sl' onchange='calc()'><br/><br/>
    金额:
<input Type='number' name='je' id='je' readonly><br/><br/>
    日期:
<input Type='date' name='rq' id='rq'><br/><br/>
    <input Type='submit' name='Sumbit' id='Sumbit' value='确定'>
    </form>
    <script src='./lib/calc.js'></script>
    </body>
    </html>
    ]]>.Value
    e.WriteString(html)
End If

现在输入数量、单价和折扣，金额就会自动计算得出了：

## 使用CSS文件

使用CSS文件


**使用CSS文件**

本节内容适合已经掌握CSS的用户。

同样，教会你CSS不是我们的任务，有人干这个我们擅长很多，如果有兴趣，可以访问：<http://www.w3school.com.cn/css/index.asp>，通常不会超过半天时间就能基本掌握。

使用CSS文件和使用js文件的方法一样，只是CSS文件通常在head块引入，js通常在body块的结束位置引入。

**一个例子**

1、在"d:\web"目录下，建立一个子目录css，在这个子目录中新建一个文本文件，文件名为文件名为“test.css”，文件内容为：

.rd{color:red;}
.gr{color:green;}

2、然后修改HttpRequest事件的代码，在有变化的地方，我加上了注释：

Dim
fl As
String =
"d:\web\" &
e.path
If
filesys.FileExists(fl)
    Dim idx
As Integer
= fl.LastIndexOf(".")
    Dim ext
As String
= fl.SubString(idx)
    Select Case
ext
        Case
".jpg",".gif",".png",".bmp",".wmf",".js",".css"
'这里加上了css扩展名
            e.WriteFile(fl)
    End
Select
Else

Dim
html
As

String
=
<![CDATA[
    <!doctype html>
    <html>
    <head>
    <meta charset='utf-8'>
    <title>CSS测试</title>
    <link rel='stylesheet' href='./css/test.css'/>
    </head>
    <body>
    <p class='rd'>This Is some text. This Is some text.</p>
    <p class='gr'>This Is some text. This Is some text.</p>
    </body>
    </html>
    ]]>.Value
    e.WriteString(html)
End
If

在浏览器的显示结果为：

## 使用第三方库

使用第三方库


**使用第三方库**

一般用户可忽略本节内容。

本节内容适合已经掌握JavaScript和CSS，希望使用第三方JavaScript库的用户。

使用第三方的Javascript库和使用本地库并没有差别，下面是一个使用jQuery库的例子。

1、在"d:\web"目录下，建立一个子目录lib，在这个子目录中新建一个文本文件，文件名为"test.js"，文件内容为：

$(document).ready(function(){
    $('button').click(function(){
        $('div').animate({left:'250px'});
    });
});

2、HttpRequest事件代码设置为，在有变化的地方，我加上了注释：

Dim
fl As
String =
"d:\web\" &
e.path
If filesys.FileExists(fl)
    Dim idx
As Integer
= fl.LastIndexOf(".")
    Dim ext
As String
= fl.SubString(idx)
    Select Case
ext
        Case
".jpg",".gif",".png",".bmp",".wmf",".js",".css"

            e.WriteFile(fl)
    End
Select
Else

Dim
html
As

String
=
<![CDATA[
    <!doctype html>
    <html>
    <head>
    <meta charset='utf-8'>
    <title>jQuery测试</title>
    <script src='https://libs.baidu.com/jquery/1.10.2/jquery.min.js'></script>
    <script src='./lib/test.js'></script>
    </head>
    <body>
    <button>开始动画</button><br/><br/>
    <div style='background:#98bf21;height:100px;width:100px;position:absolute;'>
    </body>
    </html>
    ]]>.Value

e.WriteString(html)
End
If

在浏览器显示的结果如下，单击“开始动画”按钮，绿色方框会移动：

## 使用设计好的网页

使用设计好的网页


**使用设计好的网页**

前面的例子，我们都是用Foxtable动态合成网页。

动态合成的好处是：网页是“活”的，同样的页面，根据不同的用户、数据和业务逻辑，显示内容和结构可以完全不同。

我们也可以用第三方网页设计工具事先设计好网页，由Foxtable负责将网页发送给用户浏览器，代码很简单。

例如你将设计好的网页，放在"d:\web"目录及其子目录下，包括图片、js文件、css文件等等。

然后将HttpRequest事件代码设置为：

Dim
fl As
String =
"d:\web\" &
e.path
If
filesys.FileExists(fl)
    Dim idx
As Integer
= fl.LastIndexOf(".")
    Dim ext
As String
= fl.SubString(idx)
    Select Case
ext
        Case
".jpg",".gif",".png",".bmp",".wmf",".js",".css"
,".html",".htm"
            e.WriteFile(fl)
    End
Select
End
If

不到10行代码，这可能是史上最简单的架设http服务的方法。
不，这不是最简单的，很快你会看到真正简单的http服务架设方法，只需三行代码。

**静态与动态**

如果网页需要和动态的数据以及业务逻辑相结合，就用代码动态生成；如果网页基本不变化，就事先设计好网页，也就是静态网页，以提高效率。

同一个系统，可以同时有静态网页和动态网页，除非你明确告诉客户，否则客户并不会感受到这些页面什么不同。

例如：

Select
Case e.Path
    Case ""
        e.WriteString("这是根目录下的默认页面,是动态生成的")
    Case "order.htm"
        e.WriteString("这是根目录下的Order.htm,这个文件并不存在,是自动生成的")
    Case "sale"
        e.WriteString("这是根目录的sale子目录下的默认页面,是动态生成的")
    Case "sale\add.htm"
        e.WriteString("这是根目录的sale子目录下的add.htm,这个文件并不存在,是自动生成的")
    Case Else
        Dim
fl As
String = "d:\web\"
& e.Path
        If
filesys.FileExists(fl)
            Dim idx
As Integer
= fl.LastIndexOf(".")
            Dim ext
As String
= fl.SubString(idx)
            Select
Case ext
                Case
".jpg",".gif",".png",".bmp",".wmf",".js",".css"
,".html",".htm"
                    e.WriteFile(fl)
            End
Select
        Else

e.WriteString("好奇怪,你访问的页面不存在!")
        End
If
End
Select

有个小问题需要注意一下，e.path的路径分割符是\"，不是"/"。

实际上，很难严格区分动态网页和动态网页，因为就是动态生成的网页，也需要使用不少静态的文件，例如图片、js、css等等。

## 再谈WriteString

再谈WriteString


**再谈WriteString**

**指定内容类型**

前面讲到了通过WriteFile发送设计好的JS、CSS和HTML文件。

如果文件内容很小，那么可以直接通过WriteString发送，通过第二个参数指定内容类型。

例如：

e.WriteString("function
abc(){alert('你好！');}",

"text/javascript")

**发送长文本**

本文档有很多网页使用StringBuilder的AppendLine方法拼接，这是因为网页要和Foxtable的数据结合，用StringBuilder适合运行过程中动态合成。

如果不需要拼接，就可以直接发送整个网页，例如：

Dim
html

As


String
=

<![CDATA[
<form enctype='multipart/form-data' method='post' id='form1' name='form1'>
产品:
<input name='cp' id='cp'><br/><br/>
客户:
<input name='kh' id='kh'><br/><br/>
雇员:
<input name='gy' id='gy'><br/><br/>
单价:
<input type='number' name='dj' id='dj'><br/><br/>
折扣:
<input type='number' name='zk' id='zk' min='0' max='0.15' step='0.01'><br/><br/>
数量:
<input type='number' name='sl' id='sl'><br/><br/>
日期:
<input type='date' name='rq' id='rq'><br/><br/>
<input Type='submit' name='Sumbit' id='Sumbit' value='确定'>
</form>
]]>.Value
e.WriteString(html)

请注意：

1、第一行的<![CDATA[和最后一行的]]>.Value是语法要求，并不包括在网页内容中，切记。

2、对于少量需要动态改变的内容，可以先用字符串的Replace方法查找替换，然后再发送，对于需要大量替换的，还是用StringBuilder替换会更高效一些。

3、默认的内容类型就是"text/html"，所以这里可以省略WriteString的第二个参数。

## 网页出现乱码啦

网页出现乱码啦


**网页出现乱码啦**

我用古老的FrontPage中文版设计了一个网页，这个网页很简单，就一行文字：

我喜欢用Foxtable开发管理软件

我将这个网页复制到"d:\web"目录下，通过HttpRequest将这个网页发送到客户端的浏览器上，意外出现了，中文全部变成了乱码：

如果我们在本机双击这个文件，浏览器是能正常显示中文的，说明网页本身是没有问题的：

为了查明原因，我用Nodepad++（也可以用记事本）打开这个网页，看到的源代码是：

现在出现中文乱码的原因清楚了，因为HttpRequest并不会检查要发送网页的编码格式，默认一律采用utf-8编码格式读取网页内容，然后发送到用户浏览器。

为解决这个问题，我们可以修改HttpRequest事件代码：

Dim
fl As
String = "d:\web\"
& e.Path
If
filesys.FileExists(fl)
    Dim idx
As Integer =
fl.LastIndexOf(".")
    Dim ext
As String  =
fl.SubString(idx)
    Select Case
ext
        Case
".jpg",".gif",".png",".bmp",".wmf",".js",".css"
,".html",".htm",".doc",".docx",".xls",".xlsx",".pdf"
            e.ResponseEncoding
= "gb2312"
'设置网页编码为gb2312
            e.WriteFile(fl)
    End
Select
Else
    e.WriteString("好奇怪,你访问的页面不存在!")
End
If

现在浏览器能正常显示中文了：

HttpRequest的e参数ResponseEncoding，用于设置向客户端发送文本性质的内容时，所采用的编码格式。

修改网页编码为utf-8格式

你也可以不修改HttpRequest事件代码，使用utf-8编码保存网页即可，包括js和css文件，
我们都建议采用utf-8编码。
新的网页设计工具，多数默认编码就是utf-8格式。
如果已经有其他编码格式的网页，需要改为utf-8编码，以上面的文件为例，步骤为：

1、用记事本打开这个网页，找到charset=gb2312，改为charset=utf-8
2、不要直接保存，在文件菜单单击"另存为"，在另存窗口选择编码格式为"utf-8"，然后单击"确定"按钮保存即可。

## 接收表单数据

接收表单数据


**接收表单数据**

多数时候，用户是通过表单输入数据的，表单类似于Foxtable的窗口。

**定义表单**

表单用<form>标签开始，用</form>标签结束，中间是各种输入元素。
下面是一个表单的定义，表单名为form1，数据提交方式为post，数据接收页面是accept.htm:

<form action='accept.htm' enctype='multipart/form-data' method='post' id='form1' name='form1'>

</form>

提示：表单的action属性是一个网页地址，用户输入完成后单击提交按钮，会将表单数据提交到这个网页。

**Values属性**

HttpRequest事件e参数有个Values属性，这是一个字典，包括所有用户提交的数据，键为输入元素的name属性，值就是输入元素的值。

**一个例子**

我们下面用一个例子看看Foxtable是如何定义表单和接收表单数据的，将HttpRequest事件代码设置为：

Select
Case e.Path
    Case "input.htm"

Dim
html
As

String
=
<![CDATA[
        <form action='accept.htm' enctype='multipart/form-data' method='post'
id='form1' name='form1'>
        产品:
<input name='cp' id='cp'><br/><br/>
        客户:
<input name='kh' id='kh'><br/><br/>
        单价:
<input type='number' name='dj' id='dj'><br/><br/>
        数量:
<input type='number' name='sl' id='sl'><br/><br/>
        日期:
<input type='date' name='rq' id='rq'><br/><br/>
        密码:
<input type='password' name='mm' id='mm'><br/><br/>
        支付方式:
<br/>
        <input type='radio' name='fs' id='fs1' value = '支付宝'
checked>支付宝
        <input type='radio' name='fs' id='fs2' value = '微信'>微信
        <input type='radio' name='fs' id='fs3' value = '微信'>网银<br/><br/>
        会员:
<input type='checkbox' name='hy' id='hy'><br/><br/>
        <input type='submit' name='sumbit' id='sumbit' value='提交'>
        <input type='reset' name='reset' id='reset' value='重置'>
        <input type='button' name='foxtble' id='foxtable' value='Foxtable主页'
onclick='location="http://www.foxtable.com"'>
        </form>
        ]]>.Value
        e.WriteString(html)
    Case "accept.htm"
        Dim
sb As New
StringBuilder
        sb.AppendLine("接收到的数据有:<br/><br/>")
        For Each
key As
String In
e.Values.Keys
            sb.AppendLine(key
& ":"
& e.Values(key)
& "<br/>")
        Next
        e.WriteString(sb.ToString)
End
Select

这个代码生成了两个页面，第一个页面input.htm是一个表单，用于输入数据，这个表单展示了最常用的输入类型：

用户单击提交按钮后，会将输入的数据提交到第二个页面accept.htm，该页面将收到的数据回写到客户端浏览器：

建议你以后开发系统的时候，都先用上面的方法，实际测试一下表单所提交的数据内容和格式。

需要注意的是，只有已经输入数据的输入框，以及已经勾选的radio和checbox，才会被提交到服务器，也就是说：

1、没有数据的空白输入框，不会提交到服务器。
2、没有勾选的radio和checkbox，也不会提交到服务器。

## 在表单存储标记数据

在表单插入标记数据


**在表单插入标记数据**

我们在生成表单的时候，可能需要在表单插入一些标记数据。

例如你需要根据一个现有订单，来生成一个表单，那么就需要在生成的表单中存储主键值，这样用户编辑完成，将编辑结果提交到后台时，Foxtable才能知道用户编辑的是哪一个订单。

我们可以增加一个隐藏的文本框，将这个文本框的值设置为主键，例如：

<input name='identify' id='identify' value='1' **hidden**>

value属性指定了这个文本框的默认值为1，加上hidden属性使得这个文本框在表单中处于隐藏状态，当用户提交表单数据到后台时，这个文本框的值会和其他输入框的值一起提交到后台
，Foxtable就知道用户编辑的是主键为1的订单。

我们通常不会专门介绍HTML的知识，但是这个方法对于我们今后设计应用系统很重要，所以用专门的一小节介绍一下。

## 另一种数据提交方式

另一种数据提交方式


**另一种数据提交方式**

除了前面介绍的通过表单提交数据，我们还可以通过URL地址提交数据，格式为：

http://网页地址/?键1=值1&键2=值2&键3=值3

**示例**

将HttpRequest事件代码设置为：

Select
Case e.Path
     Case "test.htm"
        Dim
sb As New
StringBuilder
        sb.AppendLine("接收到的数据有:<br/><br/>")
        For Each
key As
String In
e.Values.Keys
            sb.AppendLine(key
& ":"
& e.Values(key)
& "<br/>")
        Next
        e.WriteString(sb.ToString)
End
Select

然后在浏览器中输入地址：

http://127.0.0.01/test.htm?product=foxtable&price=4688&count=2

可以看到Foxtable已经正确提取出URL网址中包括的数据：

这种数据提交方式，通常称为get方式，通过表单提交的方式，通常称为post方式。

当然你可以将表单的method属性设置为get,这样表单也可以采用get方式提交数据，但是没有必要，因为post方式更安全、更方便，一次可以提交更多的数据。

但是get方式也有自己的优势，就是轻量级，通常用于提交一些事先约定好的、不需要用户输入的数据。

**混合Get和Post方式**

其实Get和Post两种方式是可以混合使用的，例如我们将HttpRequest事件代码设置为：

Select
Case e.Path
    Case "input.htm"
        Dim sb
As New
StringBuilder

sb.AppendLine("<form
enctype='multipart/form-data' action='accept.htm?id=1&page=10' method='post'
id='form1'
name='form1'>")
        sb.AppendLine("产品:
<input name='cp' id='cp'><br/><br/>")
        sb.AppendLine("客户:
<input name='kh' id='kh'><br/><br/>")
        sb.AppendLine("数量:
<input type='number' name='sl' id='sl'><br/><br/>")
        sb.AppendLine("日期:
<input type='date' name='rq' id='rq'><br/><br/>")
        sb.AppendLine("<input
type='submit' name='sumbit' id='sumbit' value='提交'>")
        sb.AppendLine("<input
type='reset' name='reset' id='reset' value='重置'>")
         sb.AppendLine("</form>")
        e.WriteString(sb.ToString)
    Case "accept.htm"
        Dim sb
As New
StringBuilder
        sb.AppendLine("接收到的数据有:<br/><br/>")
        For Each
key As
String In
e.Values.Keys
            sb.AppendLine(key
& ":"
& e.Values(key)
& "<br/>")
        Next
        e.WriteString(sb.ToString)
End
Select

上述代码中，我们定义的表单的代码为：

<form action='accept.htm?id=1&page=10' method='post'
name='form1'>

用户输入完成单击提交按钮后，会将输入结果提交到地址"accept.htm?id=1&page=10"，这个地址包括id和page两个值。

所以当用户按下图所示输入数据：

然后单击提交按钮，提交到后台后，显示的内容会包括url地址中的内容，以及用户输入的内容：

## Values、GetValues和PostValues

Values、GetValues和PostValues


**Values、GetValues和PostValues**

前面已经说过，不管是通过GET方式提交，还是通过POST方式提交，客户端提交的所有数据都包括在Values字典中。

HttpReqquest事件还有两个字典属性，他们是Values的子集：

GetValues： 字典，仅包括通过GET方式提交的数据。
PostValues：字典，仅包括通过POST方式提交的数据。

例如我们将HttpRequest事件代码设置为：

Select
Case e.Path
    Case "input.htm"

Dim
html
As

String
=
<![CDATA[
        <form enctype='multipart/form-data' action='accept.htm?id=1&page=10'
method='post' id='form1' name='form1'>
        产品:
<input name='cp' id='cp'><br/><br/>
        客户:
<input name='kh' id='kh'><br/><br/>
        数量:
<input type='number' name='sl' id='sl'><br/><br/>
        日期:
<input type='date' name='rq' id='rq'><br/><br/>
        <input type='submit' name='sumbit' id='sumbit' value='提交'>
        <input type='reset' name='reset' id='reset' value='重置'>
        </form>
        ]]>.Value
        e.WriteString(html)
    Case "accept.htm"
        Dim
sb As New
StringBuilder
        sb.AppendLine("通过GET方式提交的数据:<br/><br/>")
        For Each
key As
String In
e.GetValues.Keys
            sb.AppendLine(key
& ":"
& e.GetValues(key)
& "<br/>")
        Next
        sb.AppendLine("<br/><br/>通过POST方式提交的数据:<br/><br/>")
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
Select

上述代码中，我们定义的表单的代码为：

<form enctype='multipart/form-data' action='accept.htm?id=1&page=10'
method='post' id='form1' name='form1'>

用户输入完成单击提交按钮后，会将输入结果提交到地址"accept.htm?id=1&page=10"，这个地址包括id和page两个值。

当用户按下图所示输入数据：

然后单击提交按钮，提交到后台后，可以看到分别显示GET和POST方式提交的数据：

## 简单的数据统计

简单的数据统计


**简单的数据统计**

**本节任务**

我们希望让用户通过下面的网页输入年月：

单击“开始统计”，由Foxtable统计出该月各产品的销售数量，并显示在用户的浏览器上：

**知识准备**

用户是通过表单(form)输入数据的，这是我们本节要用到的一个表单：

第1行代码为：

<form action='showtj.htm' enctype='multipart/form-data'
method='post' id='form1' name='form1'>

表示用户单击确定按钮后，将结果提交到后台的showtj.htm网页处理，这个表单的名称为form1，数据提交方式为post

再看第3行代码：

年: <input type='number' name='year' id='year' min='2000' max='2018'><br/><br/>

表示这是一个数值输入框，输入值的范围在2000到2018之间，这个输入框的名称（name）为"year"，我们必须给输入框指定name属性，因为后台的Foxtable要通过name属性取得输入值。

服务端的HttpRequest事件通过e参数PostValues获取用户输入的值，这是一个字典，键为输入框的name属性，值就是用户所输入的值，例如在HttpRequest事件
获取用户通过上述表单输入的年份的代码为：

Dim
y As Integer
= 0
'将输入的年转换为整数，因为有的浏览器数值输入框也能输入字符!
Integer.TryParse(e.PostValues("year"),
y)
If y = 0
Then
     e.WriteString("请输入年!")
End
If

**完整代码**

下面是HttpRequest事件的完整代码，代码不长，却完成了生成输入页面、获取用户输入
内容、统计数据，以及呈现统计结果等四大任务：

Select
Case e.Path
    Case "saletj.htm"
        Dim sb
As New
StringBuilder

sb.AppendLine("<form
enctype='multipart/form-data' action='showtj.htm' method='post'
id='form1'
name='form1'>")
        sb.AppendLine("请输入要统计的年月:</br></br>")
        sb.AppendLine("年:
<input type='number' name='year' id='year' min='1999' max='2018'><br/><br/>")
        sb.AppendLine("月:
<input type='number' name='month' id='month' min='1' max='12'><br/><br/>")
        sb.AppendLine("<input
Type='submit' name='Sumbit' id='Sumbit' value='开始统计'>")
        sb.AppendLine("</form>")
        e.WriteString(sb.ToString)
    Case "showtj.htm"

Dim y
As Integer =
0
        Dim m
As Integer =
0

Integer.TryParse(e.PostValues("year"),
y)
'获取用户输入的
年
        Integer.TryParse(e.PostValues("month"),
m)
'获取用户输入的月
        If y
= 0 OrElse
m = 0
Then
            e.WriteString("请输入正确的年月!")
        Else
            '根据输入的年月,统计各产品的销售数量
            Dim g
As New
SQLGroupTableBuilder("统计表1",
"订单")
'这里使用后台统计,如果数据已经全部加载可以直接用GroupTableBuilder

'g.ConnectionName
= "数据源" '外部数据表的话要指定数据源名称
            g.Groups.AddDef("产品")
            g.Totals.AddDef("数量")
            g.VerticalTotal
= True
            g.Filter
= "Year(日期)
= "
& y
&
" And Month(日期)
= "
& m
'后台统计才可以使用这种表达式的哦
            Dim dt
As DataTable
= g.Build(False)


'将统计结果输出到用户浏览器
            Dim sb
As New
StringBuilder
            sb.AppendLine(y
& "年"
& m
& "月各产品销售数量: <br/><br/>")
            For Each
dr As
DataRow In
dt.DataRows
                sb.AppendLine(dr("产品")
& ":"
& dr("数量")
& "<br/>")
            Next
            e.WriteString(sb.ToString)
        End
If
End
Select

## 可能会出现性能问题

可能会出现性能问题


**可能会出现性能问题**

一般用户可以忽略本节内容。

上一节我们完成了一个简单的数据交互任务：
让用户通过网页输入年月，后台根据用户输入的年月，统计出该月各产品的销售数量，并显示在用户浏览器上。

不管是输入页面"saletj.htm"，还是显示统计结果的页面"showtj.htm"，其实都是不存在的，是后台动态生成的，是虚的。

动态生成网页的优势是灵活，但是也有一个劣势，就是性能。

以上一节的例子为例，每次统计的耗时和数据量是成正比的，如果用户每次访问都重新进行一次统计，且用户量和数据量都比较大，那么就必须考虑服务器的负担问题了。

要减轻服务器的负担，我们可以这样考虑：

1、本月的销售数据在不断变化中，适合每次访问都重新统计，而之前月份的销售数据已经固定，没有必要重复统计。

2、所以我们可以将之前月份的统计结果保存为一个网页，这样以后访问时，无需再次进行统计
，直接发送已经生成的网页即可。

3、至于本月销售数据，当然每次都重新统计是最好的，但实际上用户统计本月数据的概率是最大的，每次重新统计，也可能导致服务器负担过重。

4、所以对于本月统计，我们一样可以将统计结果保存为一个网页，用户每次访问时，判断这个网页的生成时间，如果没有超过1小时，就直接发送这个网页，否则重新进行统计。

5、为方便管理，可以在"d:\web"目录下，建立一个子目录"temp"，用于存放这些临时生成的网页。

这是修改后的HttpRequest事件的代码，要正常运行这段代码，请在"d:\web"目录下，建立一个子目录"temp"：

Select
Case e.Path
    Case "saletj.htm"
        Dim sb
As New
StringBuilder

sb.AppendLine("<form
enctype='multipart/form-data' action='showtj.htm' method='post'
id='form1'
name='form1'>")
        sb.AppendLine("请输入要统计的年月:</br></br>")
        sb.AppendLine("年:
<input type='number' name='year' id='year' min='1999' max='2018'><br/><br/>")
        sb.AppendLine("月:
<input type='number' name='month' id='month' min='1' max='12'><br/><br/>")
        sb.AppendLine("<input
Type='submit' name='Sumbit' id='Sumbit' value='开始统计'>")
        sb.AppendLine("</form>")
        e.WriteString(sb.ToString)
    Case "showtj.htm"
        Dim y
As Integer =
0
        Dim m
As Integer =
0

Integer.TryParse(e.PostValues("year"),
y)'获取用户输入的年
        Integer.TryParse(e.PostValues("month"),
m)
'获取用户输入的月
        If y
= 0 OrElse
m = 0
Then
            e.WriteString("请输入正确的年月!")
        Else
            Dim
fl As String
= "d:\web\temp\" &
y &
m &
".htm"
'合成文件名
            If FileSys.FileExists(fl)
Then
'如果文件存在
                Dim
ifo As new
FileInfo(fl)

'如果不是本月,或者文件最近一次修改时间在1个小时内,则发送文件后返回

If
y <> Date.Today.Year
OrElse m <>
Date.Today.Month
OrElse (Date.Now
- Ifo.LastWriteTime).TotalHours
< 1
                    e.WriteFile(fl)
                    Return
                End
If
            End
If
            '根据输入的年月,统计各产品的销售数量
            Dim g
As New
SQLGroupTableBuilder("统计表1",
"订单")
'这里使用后台统计,如果数据已经全部加载可以直接用GroupTableBuilder


'g.ConnectionName = "数据源"
'外部数据表的话要指定数据源名称
            g.Groups.AddDef("产品")
            g.Totals.AddDef("数量")
            g.VerticalTotal
= True
            g.Filter
= "Year(日期)
= "
& y
&
" And Month(日期)
= "
& m
'后台统计才可以使用这种表达式的哦
            Dim dt
As DataTable
= g.Build(False)

'统计数据,将结果保存为网页,然后发送这个网页
            Dim sb
As New
StringBuilder
            sb.AppendLine(y
& "年"
& m
& "月各产品销售数量: <br/><br/>")
            For Each
dr As
DataRow In
dt.DataRows
                sb.AppendLine(dr("产品")
& ":"
& dr("数量")
& "<br/>")
            Next
            sb.AppendLine("<br/>")
            sb.AppendLine("统计时间:"
& Date.Now)
'在网页显示统计时间,提醒用户这可能不是最新的结果
            FileSys.WriteAllText(fl,
sb.ToString,
False, Encoding.UTF8)
'记得用UTF8格式保存网页
            e.WriteFile(fl)
'发送保存的网页
        End
If
End
Select

如果之前月份的销售数据也有调整的可能，导致之前月份的统计结果也会变化，只是变化的概率和频率不高，那么你可以调整代码，检测之前月份统计文件的创建时间，如果超过1天
（具体时长根据需要调整），就重新统计。

## 一个页面完成一个任务

一个页面完成一个任务


**一个页面完成一个任务**

上一节的统计任务，我们使用了两个页面，页面"saletj.htm"用于输入统计年月，页面"showtj.htm"用于显示统计结果。

如果你愿意的话，也可以只用一个页面"saletj.htm"来完成这个统计任务，从代码维护角度而言，我更愿意用一个页面处理一个任务。

**知识准备**

我们已经知道，HttpRequest事件有个e参数PostValues，用于获取用户通过表单提交的数据。
我们可以用一个隐藏的输入框，在这个输入框填入约定的数据，HttpRequest根据这个输入框的值，来执行相应的操作。

例如：

<input name='tj' id='tj' value='按年月统计' hidden>"

这里创建了一个名为"tj"的输入框，默认值是"按年月统计"，这个输入框加上了hidden属性，所以在页面中并不会显示，用户不会感觉有什么变化。

在HttpRequest通过下面的代码，判断如果提交的页面名为tj的输入框，且他的值是"按年月统计"，那么就进行统计并显示统计结果，否则生成年月输入页面：

Select
Case e.Path
    Case "saletj.htm"
        If
e.PostValues.ContainsKey("tj") AndAlso
e.PostValues("tj") = "按年月统计"
Then
              '统计数据，并显示统计结果

        Else
              '生成年月录入界面
        End
If
End
Select

我们也可以用更简单的方式来区分两个页面：

Select
Case e.Path
    Case "saletj.htm"
        If
e.PostValues.Count
> 0
Then

'统计数据，并显示统计结果

        Else
              '生成年月录入界面
        End
If
End
Select

原理很简单，如果是直接访问saletj.htm，那么PostValues为空，其Count属性等于0，如果是通过表单的“开始统计”按钮访问saletj.htm，那么PostValues就会包括用户输入的值，其Count属性就会大于0。

最后别忘记修改表单定义语句，该语句之前是：

<form action='showtj.htm' enctype='multipart/form-data'
method='post' id='form1' name='form1'>

我们需要改为：

<form action='saletj.htm' enctype='multipart/form-data' method='post' id='form1'
name='form1'>

**完整的代码**

下面是HttpRequest事件的完整代码，只使用一个页面完成和上一节完全相同的任务：

Select
Case e.Path
    Case "saletj.htm"
        If

e.PostValues.ContainsKey("tj") AndAlso e.PostValues("tj") = "按年月统计"
Then
            Dim
y As
Integer = 0
            Dim
m As
Integer = 0

Integer.TryParse(e.PostValues("year"),
y)
'获取用户输入的年

Integer.TryParse(e.PostValues("month"),
m)
'获取用户输入的月
            If
y = 0
OrElse m = 0
Then
                e.WriteString("请输入正确的年月!")
            Else
                Dim
fl As
String =
"d:\web\temp\" &
y &
m &
".htm"
'合成文件名
                If
FileSys.FileExists(fl)
Then
'如果文件存在
                    Dim
ifo As
new FileInfo(fl)



'如果不是本月,或者文件创建时间在1个小时内,则发送文件后返回

If
y <> Date.Today.Year
OrElse m <>
Date.Today.Month
OrElse (Date.Now
- Ifo.LastWriteTime).TotalHours
< 1
                        e.WriteFile(fl)
                        Return
                    End
If
                End
If

 '根据输入的年月,统计各产品的销售数量
                Dim
g As New
SQLGroupTableBuilder("统计表1",
"订单")
'这里使用后台统计,如果数据已经全部加载可以直接用GroupTableBuilder

'g.ConnectionName = "数据源"
'外部数据表的话要指定数据源名称
                g.Groups.AddDef("产品")
                g.Totals.AddDef("数量")
                g.VerticalTotal
= True
                g.Filter
=  "Year(日期)
= "
& y
&
" And Month(日期)
= "
& m
'后台统计才可以使用这种表达式的哦
                Dim
dt As
DataTable = g.Build(False)



'统计数据,将结果保存为网页,然后发送这个网页
                Dim
sb As New
StringBuilder
                sb.AppendLine(y
& "年"
& m
& "月各产品销售数量: <br/><br/>")
                For
Each dr As
DataRow In
dt.DataRows
                    sb.AppendLine(dr("产品")
& ":"
& dr("数量")
& "<br/>")
                Next
                sb.AppendLine("<br/>")
                sb.AppendLine("统计时间:"
& Date.Now)
'在网页显示统计时间,提醒用户这可能不是最新的结果
                FileSys.WriteAllText(fl,
sb.ToString,
False, Encoding.UTF8)
'记得用UTF8格式保存网页
                e.WriteFile(fl)
'发送保存的网页

End
If
        Else
            Dim
sb As
New StringBuilder

sb.AppendLine("<form
enctype='multipart/form-data' action='saletj.htm' method='post'
id='form1'
name='form1'>")
            sb.AppendLine("请输入要统计的年月:</br></br>")
            sb.AppendLine("<input
name='tj' id='tj' value='按年月统计'
hidden>")
'这个输入框不会显示，仅用于标记
            sb.AppendLine("年:
<input type='number' name='year' id='year' min='1999' max='2018'><br/><br/>")
            sb.AppendLine("月:
<input type='number' name='month' id='month' min='1' max='12'><br/><br/>")
            sb.AppendLine("<input
Type='submit' name='Sumbit' id='Sumbit' value='开始统计'>")
            sb.AppendLine("</form>")
            e.WriteString(sb.ToString)
        End
 If
End
Select

## 简化HttpRequest事件代码

简化HttpRequest事件代码


简化HttpRequest事件代码

到上一节位置，我们的代码已经有点长了，这只是一个页面而已哦。
随着页面的增加，代码会十倍甚至百倍成长，而Foxtable的代码编辑器并不适合编辑超长的代码，所以最好使用自定义函数，一个页面做成一个函数，方便管理。
关于自定义函数，大家可以参考：[自定义函数](http://www.foxtable.com/webhelp/scr/1486.htm)

用上一节的任务作为例子，我们采用自定义函数来实现：

**1、定义函数**

首先定义一个名为saletj的自定义函数，代码为：

Dim
e As
RequestEventArgs
= args(0)
If
e.PostValues.ContainsKey("tj")
AndAlso e.PostValues("tj")
= "按年月统计"
Then


Dim y
As Integer
= 0
    Dim
m As
Integer = 0
    Integer.TryParse(e.PostValues("year"),
y)
'获取用户输入的年
    Integer.TryParse(e.PostValues("month"),
m)
'获取用户输入的月
    If
y = 0 OrElse
m = 0 Then
        e.WriteString("请输入正确的年月!")
    Else
        Dim fl
As String =
"d:\web\temp\" &
y &
m &
".htm"
'合成文件名
        If FileSys.FileExists(fl)
Then
'如果文件存在
            Dim ifo
As new
FileInfo(fl)

'如果不是本月,或者文件创建时间在1个小时内,则发送文件后返回

If
y <> Date.Today.Year
OrElse m <>
Date.Today.Month
OrElse (Date.Now
- Ifo.LastWriteTime).TotalHours
< 1
                e.WriteFile(fl)
                Return
""
            End
If
        End
If
        '根据输入的年月,统计各产品的销售数量
        Dim g
As New
SQLGroupTableBuilder("统计表1",
"订单")
'这里使用后台统计,如果数据已经全部加载可以直接用GroupTableBuilder

'g.ConnectionName = "数据源"
'外部数据表的话要指定数据源名称
        g.Groups.AddDef("产品")
        g.Totals.AddDef("数量")
        g.VerticalTotal
= True
        g.Filter
= "Year(日期)
= "
& y
&
" And Month(日期)
= "
& m
'后台统计才可以使用这种表达式的哦
        Dim dt
As DataTable
= g.Build(False)

'统计数据,将结果保存为网页,然后发送这个网页
        Dim sb
As New
StringBuilder
        sb.AppendLine(y
& "年"
& m
& "月各产品销售数量: <br/><br/>")
        For Each
dr As
DataRow In
dt.DataRows
            sb.AppendLine(dr("产品")
& ":"
& dr("数量")
& "<br/>")
        Next
        sb.AppendLine("<br/>")
        sb.AppendLine("统计时间:"
& Date.Now)
'在网页显示统计时间,提醒用户这可能不是最新的结果
        FileSys.WriteAllText(fl,
sb.ToString,
False, Encoding.UTF8)
'记得用UTF8格式保存网页
        e.WriteFile(fl)
'发送保存的网页

End
If
Else
    Dim sb
As New
StringBuilder

sb.AppendLine("<form
enctype='multipart/form-data' action='saletj.htm' method='post'
id='form1'
name='form1'>")
    sb.AppendLine("请输入要统计的年月:</br></br>")
    sb.AppendLine("<input
name='tj' id='tj' value='按年月统计'
hidden>")
    sb.AppendLine("年:
<input type='number' name='year' id='year' min='1999' max='2018'><br/><br/>")
    sb.AppendLine("月:
<input type='number' name='month' id='month' min='1' max='12'><br/><br/>")
    sb.AppendLine("<input
Type='submit' name='Sumbit' id='Sumbit' value='开始统计'>")
    sb.AppendLine("</form>")
    e.WriteString(sb.ToString)
End
If

上面的代码和上一节相比，
变化非常小，只有两处，首先在第一行位置插入了一行代码：

Dim
e As
RequestEventArgs
= args(0)

RequestEventArgs是HttpRequest事件的e参数类型。

其次是将代码中的

Return

改为了

Return
""

2、修改HttpRequest事件代码

接下来将HttpRequest事件的代码改为：

Select
Case e.Path
    Case "saletj.htm"

Functions.Execute("saletj",e)
End
Select

由于主要的工作已经转移到自定义函数中，所以HttpRequest变得很简洁。

为便于讲述，接下来的例子并不会采用自定义函数，但是实际开发的时候，建议大一点的系统，都应该采用自定义函数，如果所有代码都写在HttpRequest事件中，你将痛苦不堪。

## 通用HttpRqeust事件头

通用HttpRqeust事件头


**通用HttpRqeust事件头**

建议实际开发的时候，建议在HttpRqeust事件的开始位置都加上一段代码，用于发送已经存在的常见文件：

'通用事件头,用于发送已经存在的常见文件
Dim
fl As
String =
"d:\web\" &
e.path
If
filesys.FileExists(fl)
    Dim idx
As Integer
= fl.LastIndexOf(".")
    Dim ext
As String
= fl.SubString(idx)
    Select Case
ext
        Case
".jpg",".gif",".png",".bmp",".wmf",".js",".css"
,".html",".htm",".zip",".rar"

            e.WriteFile(fl)
            Return
'这里必须返回
    End
Select
End
If
'以下是动态生成网页的代码
Select
Case e.Path

    Case "addnew.htm"
         '生成新增页面
    Case "tongji.htm"
         '生成统计页面
    Case "order.htm"
         '生成订购页面
    Case
Else
       e.WriteString("糟糕,文件未找到！")
End
Select

为了让大家专注与每一节要讲述的问题，帮助文件中很多例子是不会加上事件头的。

有的时候，文件即使已经存在，也可能需要重新生成，参考：[可能出现的性能问题](0023.htm)

对于这种情况，我们可以进行一些判断即可，排除这些特殊页面：

'通用事件头,用于发送已经存在的常见文件
Select
Case e.Path
    Case "saletj.htm","showtj.htm"
'排除两个页面,由后面的代码负责处理
    Case Else
'其他页面或文件如果已经存在,直接发送

Dim
fl As
String =
"d:\web\" &
e.path
        If
filesys.FileExists(fl)
            Dim idx
As Integer
= fl.LastIndexOf(".")
            Dim ext
As String
= fl.SubString(idx)
            Select
Case ext
                Case
".jpg",".gif",".png",".bmp",".wmf",".js",".css"
,".html",".htm",".zip",".rar"
                    e.WriteFile(fl)
                    Return
'这里必须返回
            End
Select
        End
If
End
Select
'以下是动态生成网页的代码
Select
Case e.Path
    Case "addnew.htm"
        '生成新增页面
    Case "saletj.htm"
        '生成统计页面
    Case "showtj.htm"
        '生成统计结果显示页面
    Case "order.htm"

'生成订购页面
    Case
Else
       e.WriteString("糟糕,文件未找到！")
End
Select

有一个问题需要特别留意：

以上面的代码为例，如果你在"d:\web"目录下保存了一个"addnew.htm"网页文件，那么系统将直接发送这个文件，而不会执行后面动态生成"addnew.htm"的代码。
如果某次你修改代码后，生成的网页始终没有变化，一般都是这个原因造成的。

## 一个简单的录入界面

一个简单的录入界面


**一个简单的录入界面**

后台有一个订单表，结构如下：

现在希望设计一个网页用于输入新的订单：

用户输入数据，单击确定后，能在后台的表新增订单，并显示如下页面，让用户选择是否继续增加订单：

看似复杂，实际上HttpRequet事件的代码很简单，望大家仔细体会：

Select
Case e.Path
    Case
"AddNew.htm"
        If e.PostValues.Count
= 0 Then
            Dim
sb As New
StringBuilder

sb.AppendLine("<form
action='AddNew.htm' enctype='multipart/form-data' method='post'
id='form1'
name='form1'>")
            sb.AppendLine("产品:
<input name='cp' id='cp'><br/><br/>")
            sb.AppendLine("客户:
<input name='kh' id='kh'><br/><br/>")
            sb.AppendLine("雇员:
<input name='gy' id='gy'><br/><br/>")
            sb.AppendLine("单价:
<input type='number' name='dj' id='dj'><br/><br/>")
            sb.AppendLine("折扣:
<input type='number' name='zk' id='zk' min='0' max='0.15' step='0.01'><br/><br/>")
            sb.AppendLine("数量:
<input type='number' name='sl' id='sl'><br/><br/>")
            sb.AppendLine("日期:
<input type='date' name='rq' id='rq'><br/><br/>")
            sb.AppendLine("<input
Type='submit' name='Sumbit' id='Sumbit' value='确定'>")
            sb.AppendLine("</form>")
            e.WriteString(sb.ToString)
        Else
            Dim
dr As DataRow
= DataTables("订单").SQLAddNew()
            Dim inms()
As String =
{"cp","kh","gy","dj","zk","sl","rq"} '输入框名称数组


            Dim
cnms() As
String = {"产品","客户","雇员","单价","折扣","数量","日期"}
'列名数组,注意列名和输入框必须一一对应,位置不能错乱

For
i As
Integer = 0
To inms.Length
-1
                dr(cnms(i))
= e.PostValues(Inms(i))

            Next
            dr.Save()
'用SQLAddNew增加的行,必须保存一下,否则会被丢弃.



            Dim sb
As New
StringBuilder
            sb.AppendLine("增加订单成功!
<br/><br/>")

            sb.AppendLine("<a
href='AddNew.htm'>继续增加</a>")

            e.WriteString(sb.ToString)

End
If
End
Select

提示：

1、这里用SQLAddNew直接在后台增加行，SQLAddNew是Foxtable
2017新增加的一个方法，适合加载结构但不加载数据的表，如果希望服务端能即时显示用户通过网页增加的行，请改用AddNew，二者效率差不多。
2、如果用户量很大，需要更高的效率，建议采用SQL语句插入行，需要注意的是，只有外部数据源才支持用SQL语句插入行。

## 文件的上传与接收

文件的上传与接收


**文件的上传与接收**

用户可以通过表单上传文件。

**表单准备**

如果表单要包括文件上传组件，在定义表单的时候，要将enctype设置为"multipart/form-data"，例如：

<form enctype='multipart/form-data' action='accept.htm'
method='post' id='form1' name='form1'>
</form>

否则，HttpServer将无法收到用户上传的文件。

在表单插入一个type为file的input元素，即可实现文件上传，例如：

<input type='file' name='up1' id='up1'>

如果要允许用户选择多个文件上传，加上multiple属性即可，例如

<input type='file' name='up2' id='up2' multiple>

下面是一个完整的文件上传表单：

<form enctype='multipart/form-data' action='accept.htm' method='post' id='form1'
name='form1'>
单文件上传: <input type='file' name='up1' id='up1'><br/><br/>
多文件上传: <input type='file' name='up2' id='up2' multiple><br/><br/>
<input Type='submit' name='Sumbit' id='Sumbit' value='确定'>
</form>

接收文件

HttpRequest的e参数有个Files属性，这是一个字典，键为文件上传组件的name属性，值是一个字符串集合，包括用户通过这个上传组件上传的所有文件名。

HttpRequest的e参数有个SaveFile方法，用于保存接收到的文件，其语法为：

SaveFile(Key,UploadFile,LocalFile)

|  |  |
| --- | --- |
| Key | 文件上传组件的name属性 |
| UploadFile | 用户上传的文件名称，不含路径。 |
| LocalFile | 要保存到本地的文件名称，含路径 |

**完整示例**

将HttpRequest设置为以下代码：

Select
Case e.Path
    Case "upload.htm"
        Dim sb
As New
StringBuilder
        sb.appendLine("<form
enctype='multipart/form-data' action='accept.htm' method='post'
id='form1' name='form1'>")
        sb.appendLine("单文件上传:
<input type='file' name='up1' id='up1'><br/><br/>")
        sb.appendLine("多文件上传:
<input type='file' name='up2' id='up2' multiple><br/><br/>")
        sb.appendLine("<input
Type='submit' name='Sumbit' id='Sumbit' value='确定'>")
        sb.appendLine("</form>")
        e.WriteString(sb.ToString)
    Case "accept.htm"
        Dim sb
As New
StringBuilder
        For Each
key As
String In
e.Files.Keys
            sb.AppendLine(key
&
"
上传"
& e.Files(key).Count
&
"个文件,分别是:</br>")
            For Each
fl As
String In
e.Files(key)
                sb.AppendLine(fl
& "<br>")
                e.SaveFile(key,fl,"d:\web\uploadfiles\"
& fl)
'保存接收到的文件


Next
            sb.AppendLine("</br>")
        Next
        sb.AppendLine("以上文件服务器已正确接收并保存!")
        e.WriteString(sb.ToString)
End
Select

上面的代码生成了两个页面，upload页面用于上传文件：

accept.htm页面用于显示并保存用户上传的文件：

## 避免覆盖同名文件

避免覆盖同名文件


**避免覆盖同名文件**

我们在上一节设计的文件上传和接收示例中，如果多个用户上传了同名的文件，会出现覆盖的情况。

为避免同名文件被覆盖，我们可以将HttpRequest事件代码改为：

Select
Case e.Path
    Case "upload.htm"
        Dim
sb As New
StringBuilder
        sb.appendLine("<form
enctype='multipart/form-data' action='accept.htm' method='post'
id='form1'

name='form1'>")
        sb.appendLine("单文件上传:
<input type='file' name='up1' id='up1'><br/><br/>")
        sb.appendLine("多文件上传:
<input type='file' name='up2' id='up2' multiple><br/><br/>")
        sb.appendLine("<input
Type='submit' name='Sumbit' id='Sumbit' value='确定'>")
        sb.appendLine("</form>")
        e.WriteString(sb.ToString)
    Case "accept.htm"
        Dim
sb As New
StringBuilder
        For
Each key As
String In
e.Files.Keys
            sb.AppendLine(key
&
"
上传"
& e.Files(key).Count
&
"个文件,分别是:</br>")
            For Each
fl As
String In
e.Files(key)
                Dim
NewName As
String = fl
                Dim
idx As
Integer = fl.LastIndexOf(".")
                Dim
cnt As
Integer = 1
                Do
While FileSys.FileExists("d:\web\uploadfiles\"
& NewName)
'判断文件夹是否存在同名文件
                    NewName =
fl.Insert(idx,"("
& cnt
& ")")
'如果存在同名文件,在原文件名加上序号
                    cnt =
cnt + 1
'递增序号
                Loop
                sb.AppendLine(fl
&
"
→
"
& NewName
& "<br>")
'
                e.SaveFile(key,fl,"d:\web\uploadfiles\"
& NewName)
'保存接收到的文件

Next
            sb.AppendLine("</br>")
        Next
        sb.AppendLine("以上文件服务器已正确接收并保存!")
        e.WriteString(sb.ToString)
End
Select

这样HttpServer接收到同名文件后，会自动给同名文件加上编号，而不是直接覆盖：

## 手机拍照与上传

手机拍照与上传


**手机拍照与上传**

如果在手机上访问上一节生成的网页，效果和pc上是不太一样的。

例如在iPhone上访问上面的网页，可以直接拍照并上传：



实际上你通过iPhone访问上述页面时，字体是很小的，上面是放大后截图的，后面的章节会告诉大家解决办法，现在暂时放过这个问题。

## 带上传功能的录入页面

带文件上传功能的录入页面


**带文件上传功能的录入页面**

假定有一个员工表，结构如下：

希望生成一个下图所示的页面，让用户此页面增加员工：

HttpRequest事件代码很简单：

Select
Case e.Path
    Case "AddNew.htm"
        If e.PostValues.Count
= 0 AndAlso
e.Files.Count
= 0 Then
            Dim
sb As
New StringBuilder
            sb.AppendLine("<form
enctype='multipart/form-data' action='AddNew.htm' method='post'
id='form1' name='form1'>")
            sb.AppendLine("姓名:
<input name='xm' id='xm'><br/><br/>")
            sb.AppendLine("部门:
<input name='bm' id='bm'><br/><br/>")
            sb.AppendLine("职务:
<input name='zw' id='zw'><br/><br/>")
            sb.AppendLine("学历:
<input name='xl' id='xl'><br/><br/>")
            sb.AppendLine("照片:
<input type='file' name='zp' id='zp' multiple><br/><br/>")
            sb.AppendLine("<input
Type='submit' name='Sumbit' id='Sumbit' value='确定'>")
            sb.AppendLine("</form>")
            e.WriteString(sb.ToString)
        Else
            Dim
dr As
DataRow =
DataTables("员工").AddNew()
            Dim inms()
As String =
{"xm","bm","zw","xl"}
'输入框名称数组
            Dim cnms()
As String =
{"姓名","部门","职务","学历"}
'列名数组,注意列名和输入框必须一一对应,位置不能错乱

            For i
As Integer
= 0 To
inms.Length
-1
                dr(cnms(i))
= e.PostValues(Inms(i))

            Next
            If  e.Files.ContainsKey("zp")
Then
                dr("照片")
= e.Files("zp")(0)
                e.SaveFile("zp",
e.Files("zp")(0),
ProjectPath &
"Attachments\" &
e.Files("zp")(0))
            End If

dr.Save()
            Dim
sb As
New StringBuilder
            sb.AppendLine("增加记录成功!
<br/><br/>")
            sb.AppendLine("<a
href='AddNew.htm'>继续增加</a>")
            e.WriteString(sb.ToString)

End
If
End
Select

上面的代码，用一个页面"AddNew.htm"完成了录入网页的生成，数据和文件的接收与
保存，以及记录增加成功后反馈页面的生成。

## 生成表格

生成表格


**生成表格**

HTML中的表、行、单元格的开始标签分别为<table>、<tr>、<td>，对应的结束标签分别为</table>、</tr>、</td>。

我们将HttpRequest事件代码代码设置为：

Select
Case e.Path
    Case "table.htm"
        Dim sb
As New
StringBuilder
        sb.AppendLine("<table
border='1'>")
        sb.AppendLine("<caption>标题</caption>")
        sb.AppendLine("<tr><td>1行1列</td><td>1行2列</td><td>1行3列</td></tr>")
        sb.AppendLine("<tr><td>2行1列</td><td>2行2列</td><td>2行3列</td></tr>")
        sb.AppendLine("<tr><td>3行1列</td><td>3行2列</td><td>3行3列</td></tr>")
        sb.AppendLine("</table>")
        e.WriteString(sb.ToString)
End
Select

在浏览器中显示的结果为：

有关HTML表格的更多知识，请访问：

<http://www.w3school.com.cn/html/html_tables.asp>

<http://www.w3school.com.cn/css/css_table.asp>

## 分页显示数据

分页显示数据


**分页显示数据**

本机希望设计一个分页显示订单表的页面，用户可以通过单击“上一页”、“下一页”来切换页面：



HttpRequst事件的代码并不复杂，其中一些技巧请仔细体会：

Select
Case e.Path
    Case "list.htm"
        Dim
page As
Integer = 0

'默认page为0，显示第一页
        Dim
pageRows As
Integer = 10
'每页10行
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
pageRows
'此页第一行
        Dim EndRow
As Integer
= (page + 1)
\* pageRows - 1
'此页最后一行
        Dim lst
As List(of
DataRow) =
DataTables("订单").Select("","日期
Desc")
'按日期顺序显示
        If StartRow
> lst.Count
-1 Then
            e.WriteString("已经是最后一页!")
            Return
        End If
        EndRow =
Math.Min(EndRow,
lst.Count -
1)
'这是必须的
        Dim sb
As New
StringBuilder
        Dim
nms() As
String = {"产品","客户","数量","单价","折扣","金额","日期"}
        sb.AppendLine("<Table
border='1'>")
        sb.AppendLine("<caption>订单浏览<caption></br>")
        sb.Append("<tr>")
        For Each
nm As
String In
nms
            sb.Append("<td>"
& nm
& "</td>")
        Next
        sb.AppendLine("</tr>")
        For r
As Integer
= StartRow To
EndRow
            sb.Append("<tr>")
            For Each
nm As
String In
nms
                sb.Append("<td>"
& lst(r)(nm)
& "</td>")
            Next
            sb.AppendLine("</tr>")
        Next
        sb.AppendLine("</Table></br></br>")
        If page
> 0 Then
            sb.Append("<a
href='list.htm?page=" &
page - 1
&
"'>上一页</a>
")
        End If
        If
EndRow < lst.Count
-1 Then
            sb.Append("<a
href='list.htm?page=" &
page + 1
&
"'>下一页
</a>" )
        End If
        e.WriteString(sb.ToString)
End
Select

上述代码合成的上一页、下一页链接地址包括了要显示的页面参数，例如：

http://127.0.0.1/list.htm?page=1

表示请求显示第二页（0表示第一页），HttpRequst事件提取出这个页面参数后，以表格形式将对应页面数据显示在用户浏览器上。

这种数据传递方式，之前我们已经介绍过，请参考：[另一种数据提交方式](0029.htm)，只是本节是通过GetValues属性获取page参数的。

## 必须掌握的Row_Number

必须掌握的Row\_Number


必须掌握的Row\_Number

接下来我们将给大家介绍如何分页显示后台数据，但是在这之前我需要先给大家介绍一下SQL Server的Row\_Number函数。

Row\_Number函数让我们分页显示后台变得非常方便。

一般用户对于Row\_Number函数的使用会比较迷糊，不过通过本节的学习，你会发现Row\_Number其实很简单。

一个例子

假定我们需要按照日期降序加载订单表数据，每页10行，加载第8页，我们可以在Foxtable的SQL窗口测试以下各步骤的Select语句。

1、按照常规写出最简单的Select语句：

Select \* From {订单}

这是显示的结果是：

2、RowNumber函数用于按指定的列排序，来生成一个序号列，语法为：

Row\_Number() Over(Order by 排序列) As 序号列

可变的只有排序列和序号列名，默认是升序，如果需要降序，在排序列后面加上DESC参数即可。

现在将我们的Select语句改写为：

Select Row\_Number()
Over(Order by 日期 Desc) As 序号, \* From {订单}

显示的结果如下图，可以看到增加了一个序号列，序号是根据日期按照降序编排的。

3、现在我们可以将上面的Select语句当作一个表来看待，我们从这个表提取数据:

Select \* From
(Select Row\_Number() Over(Order by 日期 Desc)
As 序号, \* From {订单}) As tmp

上述语句分三部分，中间括起来的蓝色部分可以理解为一个临时表，我们需要给这个临时表取个名字，后面这段红色部分将这个临时表取名为"tmp"

现在的显示结果没有变化：

4、现在是最后一步，每页10行，第8页的数据的序号列范围为70到80，我们将Select语句改为：

Select \* From
(Select Row\_Number() Over(Order by 日期 Desc)
As 序号, \* From {订单}) As tmp
Where 序号 >=71 And 序号 <= 80

显示结果为：

上图就是按照日期降序加载订单表，每页10行，加载第8页的结果。

最终的Select语句看起来有点复杂：

Select \* From (Select Row\_Number()
Over(Order by 日期 Desc) As 序号, \* From {订单}) As tmp
Where 序号 >=71 And 序号 <= 80

但是你可以理解为：

Select \* From tmp
Where 序号 >=71 And 序号 <= 80

而tmp是个临时表，是通过以下语句生成的：

(Select Row\_Number() Over(Order by 日期 Desc) As 序号, \* From
{订单}) As tmp

注意临时表的Select语句必须用圆括号括起来。

## 分页显示后台数据

分页显示后台数据


**分页显示后台数据**

上一节我们实现分页显示已经加载到DataTable中的数据。

这一节介绍如何分页显示未加载的数据，在给出具体代码之前，我先给大家一些建议：

1、如果服务端的数据量比较小，将数据加载进来，可以提高处理速度。

2、如果服务端数据量比较大，加载全部数据，可能会耗尽内存，甚至导致系统崩溃。

3、怎样才算小，怎样才算大，这没有标准，请以实际运行效果为准，一般不建议服务端加载超过5万行的数据。

4、如果某个表虽然不加载数据，但是需要对这个表进行增加、删除和修改等操作，那么建议加载这个表的结构，这样就可以利用[后台数据处理函数](http://www.foxtable.com/webhelp/scr/2902.htm)简化代码。

5、建议使用SQL Server作为数据源，容量更大，性能更好，而且SQL Server有[Row\_Number](http://www.foxtable.com/webhelp/scr/2721.htm)函数，分页加载方便很多。

**完整示例**

下面的HttpRequest事件，用于分页显示后台数据，这里假定你使用的是SQL
Server作为数据源：

Select
Case e.Path
    Case "list.htm"
        Dim
page As
Integer = 0

'默认page为0，显示第一页
        Dim
pageRows As
Integer = 10
'每页10行
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
pageRows
'此页第一行
        Dim EndRow
As Integer =
(page + 1) \*
pageRows - 1
'此页最后一行
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
= "Select \*, [数量]\*[单价]\*(1-[折扣])
As 金额
From (Select Row\_Number() Over(Order by [日期])
As RowNum, \* From
订单)
As a "
        cmd.CommandText
= cmd.CommandText
& "  Where RowNum >=
" & StartRow
& " And RowNum <= "
& EndRow
        Dim dt
As DataTable
= cmd.ExecuteReader
'获取该页数据
        Dim sb
As New
StringBuilder
        Dim nms()
As String =
{"产品","客户","数量","单价","折扣","金额","日期"}
        sb.AppendLine("<Table
border='1'>")
        sb.AppendLine("<caption>订单浏览<caption></br>")
        sb.Append("<tr>")
        For Each
nm As
String In
nms
            sb.Append("<td>"
& nm
& "</td>")
        Next
        sb.AppendLine("</tr>")
        For Each
r As
DataRow In
dt.DataRows
            sb.Append("<tr>")
            For Each
nm As
String In
nms
                sb.Append("<td>"
& r(nm)
& "</td>")
            Next
            sb.AppendLine("</tr>")
        Next
        sb.AppendLine("</Table></br></br>")
        If page
> 0 Then
            sb.Append("<a
href='list.htm?page=" &
page - 1
&
"'>上一页</a>
")
        End If
        If
EndRow < Count -1
Then
            sb.Append("<a
href='list.htm?page=" &
page + 1
&
"'>下一页
</a>" )
        End If
        e.WriteString(sb.ToString)
End
Select

## 一个综合性的例子

一个综合性的例子


**一个综合性的例子**

本节的任务是在上一节分页显示后台数据的基础上，加上编辑和删除订单的功能：

单击删除链接，可以删除对应的订单，单击编辑链接，可以编辑对应的订单：

编辑或删除订单后，可以返回原来的分页：

**知识准备**

用户单击“编辑”链接，后台如何知道要编辑哪一个订单呢？ 编辑完成后，又怎么知道返回哪一个页面呢？

我们可以在表单中插入隐藏字段，来传递主键和页码，参考：

[在表单中插入标记数据](0028.htm)

不过本节我们不采用这个方法，我们采用get方式来传递主键和页码，参考：

[另一种数据提交方式](0029.htm)

[Values、PostValues和GetValues](0113.htm)

**完整代码**

这是HttpRequest事件的完整代码，由于包括分页、编辑、删除三部分的代码，所以代码有点长，后面会对关键代码进行解释：

Dim
sb As
New
StringBuilder
Select
Case e.Path
    Case
"list.htm"
'分页显示
        Dim page
As Integer
= 0

'默认page为0，显示第一页
        Dim
pageRows As
Integer = 10
'每页10行
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
pageRows
'此页第一行
        Dim EndRow
As Integer
= (page + 1)
\* pageRows - 1
'此页最后一行
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
= "Select \*, [数量]\*[单价]\*(1-[折扣])
As 金额
From (Select Row\_Number() Over(Order by [日期]
desc) As RowNum, \* From
订单)
As a "
        cmd.CommandText
= cmd.CommandText
& "  Where RowNum
>= " &
StartRow & "
And RowNum <= " &
EndRow
        Dim
dt As
DataTable = cmd.ExecuteReader
'获取该页数据
        Dim nms()
As String =
{"产品","客户","数量","单价","折扣","金额","日期"}
        sb.AppendLine("<Table
border='1'>")
        sb.AppendLine("<caption>订单浏览<caption></br>")
        sb.Append("<tr>")
        For Each
nm As
String In
nms
            sb.Append("<td>"
& nm
& "</td>")
        Next
        sb.Append("<td></td>")
        sb.Append("<td></td>")
        sb.AppendLine("</tr>")
        For Each
r As
DataRow In
dt.DataRows
            sb.Append("<tr>")
            For Each
nm As
String In
nms
                sb.Append("<td>"
& r(nm)
& "</td>")
            Next
            sb.Append("<td><a
href='edit.htm?id=" &
r("\_Identify")
& "&page="
& page
&
"'>编辑</a></td>")
            sb.Append("<td><a
href='delete.htm?id=" &
r("\_Identify")
& "&page="
& page
&
"'>删除</a></td>")
            sb.AppendLine("</tr>")
        Next
        sb.AppendLine("</Table></br></br>")
        If page
> 0 Then
            sb.Append("<a
href='list.htm?page=" &
page - 1
&
"'>上一页</a>
")
        End If
        If
EndRow < Count -1
Then
            sb.Append("<a
href='list.htm?page=" &
page + 1
&
"'>下一页
</a>" )
        End If
        e.WriteString(sb.ToString)
    Case
"delete.htm"
'删除订单
        If
e.GetValues.ContainsKey("id")
AndAlso e.GetValues.ContainsKey("page")
Then
            Dim
cnt As
Integer
            cnt =
DataTables("订单").SQLDeleteFor("[\_Identify]
= " & e.GetValues("id"))
            If cnt
> 0 Then
                sb.AppendLine("删除成功!</br></br>")
            Else
                sb.AppendLine("删除失败!</br></br>")
            End If

sb.Append("<a
href='list.htm?page=" &
e.GetValues("page")
&
"'>返回列表</a>"
)
            e.WriteString(sb.ToString)
        Else
            e.WriteString("糟糕,可能出错了")
        End If
    Case
"edit.htm"
'编辑订单
        If
e.GetValues.ContainsKey("id")
AndAlso e.GetValues.ContainsKey("page")
Then
            Dim
dr As
DataRow =
DataTables("订单").SQLFind("[\_Identify]
= " & e.GetValues("id"))
            If dr
Is Nothing
Then
                e.WriteString("此订单不存在,可能已经被其他用户删除!")

Return
            End If
            If
e.PostValues.Count
= 0 Then
'生成编辑页面
                sb.appendLine("<form
action='edit.htm?id=" &
e.GetValues("id")
& "&page="
& e.GetValues("page")
& "' method='post'
id='form1'

name='form1'>")
                sb.appendLine("产品:
<input name='cp' id='cp' value='"
& dr("产品")
& "'><br/><br/>")
                sb.appendLine("客户:
<input name='kh' id='kh' value='"
& dr("客户")
& "'><br/><br/>")
                sb.appendLine("雇员:
<input name='gy' id='gy' value='"
& dr("雇员")
& "'><br/><br/>")
                sb.appendLine("单价:
<input type='number' name='dj' id='dj' step='0.1' value='"
& dr("单价")
& "'><br/><br/>")
                sb.appendLine("折扣:
<input type='number' name='zk' id='zk' step='0.01' value='"
& dr("折扣")
& "'><br/><br/>")
                sb.appendLine("数量:
<input type='number' name='sl' id='sl' value='"
& dr("数量")
& "'><br/><br/>")
                sb.appendLine("日期:
<input type='date' name='rq' id='rq' value='"
& dr("日期")
& "'><br/><br/>")
                sb.appendLine("<input
Type='submit' name='Sumbit' id='Sumbit' value='确定'>")
                sb.appendLine("</form>")
                e.WriteString(sb.ToString)
            Else
'获取用户提交的数据
                Dim
inms() As
String = {"cp","kh","gy","dj","zk","sl","rq"}
'输入框名称数组

Dim cnms()
As
String
= {"产品","客户","雇员","单价","折扣","数量","日期"}
'列名数组,注意列名和输入框必须一一对应,位置不能错乱
                For i As Integer = 0 To inms.Length -1
                    If
e.PostValues.ContainsKey(inms(i))
Then
'必须判断,因为PostValues集合只包括已经输入的值
                        dr(cnms(i))
= e.PostValues(Inms(i))
                    End
If
                Next
                dr.Save()
'用SQLAddNew增加的行,必须保存一下,否则会被丢弃.
                sb.AppendLine("编辑订单成功!
<br/><br/>")
                sb.AppendLine("<a
href='list.htm?page=" &
e.GetValues("page")
&
"'>返回列表</a>")
                e.WriteString(sb.ToString)
            End If
        Else
            e.WriteString("糟糕,可能出错了")


End
If
End
Select

分页显示的代码和上一节基本一样，只是为每一行增加了编辑和删除链接，合成这两个链接的代码为：

sb.Append("<td><a
href='edit.htm?id=" &
r("\_Identify")
& "&page="
& page
&
"'>编辑</a></td>")
sb.Append("<td><a
href='delete.htm?id=" &
r("\_Identify")
& "&page="
& page
&
"'>删除</a></td>")

下面是第5页(页面编号4)中主键为176的行对应的链接：

<a href='edit.htm?id=176&page=4'>编辑</a>
<a href='delete.htm?id=176&page=4'>删除</a>

表示要编辑或删除的订单的主键是176，当前页面编号是4。

例如HttpRequset事件收到访问请求“delete.htm?id=176&page=4”，从中提取出主键176和页面编号4，删除主键为176的订单后，再合成一个链接：

sb.Append("<a
href='list.htm?page=" &
e.GetValues("page")
&
"'>返回列表</a>"
)

这样用户单击这个连接，即可返回原来的分页。

再例如HttpRequset事件收到访问请求“edit.htm?id=176&page=4”后，从中提取出主键176和页面编号4，然后从后台找出主键为176的行，根据
该行的内容生成编辑表单，注意我们定义表单的代码：

sb.appendLine("<form
action='edit.htm?id=" &
e.GetValues("id")
& "&page="
& e.GetValues("page")
& "' method='post'
id='form1'
name='form1'>")

这段代码合成的内容类似：

<form action='edit.htm?id=176&page=4'
method='post' id='form1' name='form1'>

当用户编辑完成，单击确定按钮时，将输入的值发送到到"edit.htm?id=176&page=4"。
HttpRequset收到这个请求后，e.PostValues.Count属性会大于0，系统知道用户本次访问
目的是提交编辑结果。
HttpRequset事件找出主键为176的行，将接收到的值存储到对应的列，并生成一个链接，让用户可以返回原来的页面：

sb.AppendLine("<a
href='list.htm?page=" &
e.GetValues("page")
&
"'>返回列表</a>")

重要提示：所有的浏览器都可以查看网页源码，通过查看网页源码，有助于我们学习理解和排查错误。

**增加订单功能**

为了让代码不至于太长，上面的例子，只有编辑和删除订单的功能，没有增加订单的功能。
实际上，增加订单功能实现起来更简单，而且我们之前已经讲述过了，大家自己将这部分的代码整合进来即可，参考：

[一个简单的录入功能](0026.htm)

**简化HttpRequest事件代码**

这是到目前为止，我们写的最长的一段HttpRequest事件代码，用了三个页面，实现了分页显示、增加订单、删除订单的功能。
建议大家一个页面做成一个函数，在HttpRequest不要涉及具体功能，只负责调用相关函数，参考：[简化HttpRequest事件代码](0025.htm)

## 使用Cookie

使用Cookie


**使用Cookie**

通过Cookie可以在本机临时存储数据，每次访问服务器网页时，都会自动将Cookie中的值，传递给服务器。

HttpRequest事件有个AppendCookie方法，用于添加Cookie，语法为：

AppendCookie(Name, Value)

Name：Cookie名称
Value：Cookie值

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

**示例**

将HttpRequest事件代码设置为：

Dim
sb As
New
StringBuilder
Dim
cnt As
Integer =
1
Integer.TryParse(e.Cookies("count"),cnt)
'提取cookie的值,
并转换为整数
cnt
= cnt +
1
e.AppendCookie("count",cnt)
'在客户端存储Cookie
e.WriteString("您这是第"
& cnt
& "次访问!")

现在每次刷新页面，访问次数都会递增1：

需要注意的是：Cookie名是区分大小写的。

## 用户身份验证

用户身份验证


用户身份验证

本节的任务是利用上节介绍的Cookie知识，设计一个身份验证功能。

这个系统有五个页面，分别是登录页面logon.htm，退出登录页面exit.htm，以及首页default.htm，还有两个普通页面order.htm和product.htm.


这是登录页面logon.htm：

这是登录成功后的首页default.htm：

如果用户身份验证失败，会重新进入登录页面，并有错误提示：

**设计要求:**

1、当用户第一次访问时，不管访问任何页面，都会自动跳转到登录页面logon.htm，要求输入账户名和密码
。

2、等用户身份验证通过后，自动跳转到首页default.htm，并可访问任何其他页面。
3、如果用户身份验证失败，会重新进入登录页面logon.htm，并有错误提示。
4、在首页单击"退出登录"，可以清除当前的登录状态，重新进入登录页面。

**HttpRequest事件代码：**

Dim
sb As
New
StringBuilder
Dim
Verified As
Boolean
Dim
UserName As
String
= e.Cookies("username")
'从cookie中获取用户名
Dim
Password As
String
= e.Cookies("password")
'从cookie中获取用户密码
'如果在登录页面输入了用户名和密码后单击确定按钮
If e.Path
= "logon.htm"
AndAlso e.PostValues.ContainsKey("username")
AndAlso e.PostValues.ContainsKey("password")
Then
    UserName = e.PostValues("username")
    Password = e.PostValues("password")
End
If
'验证用户身份
If
UserName = "张三"
AndAlso Password
= "888"
Then
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
    e.Appendcookie("username",UserName)
'将用户名和密码写入cookie
    e.Appendcookie("password",Password)
    e.WriteString("<meta
http-equiv='Refresh' content='0; url=/default.htm'>")
'直接跳转到首页
    Return
'必须的
ElseIf
Verified = False
AndAlso e.Path
<> "logon.htm" Then
'如果用户身份验证失败,且访问的不是登录页面
    e.WriteString("<meta
http-equiv='Refresh' content='0; url=/logon.htm'>")
'那么直接跳转到登录页面
    Return
'必须的
End
If
Select
Case e.path
    Case
"logon.htm"
        sb.AppendLine("<form
action='logon.htm' enctype='multipart/form-data' method='post'
id='form1'
name='form1'>")
        If e.PostValues.ContainsKey("username")
AndAlso e.PostValues.ContainsKey("password")
Then
'判断是否是验证失败后的重新登录
            sb.AppendLine("用户名或密码错误!</br></br>")
            sb.AppendLine("户名:
<input name='username' id='username' value='"
& UserName
& "''><br/><br/>")
            sb.AppendLine("密码:
<input type='password' name='password' id='password' value ='"
& Password
& "'><br/><br/>")
        Else
            sb.AppendLine("户名:
<input name='username' id='username'><br/><br/>")
            sb.AppendLine("密码:
<input type='password' name='password' id='password'><br/><br/>")
        End
If
        sb.AppendLine("<input
type='submit' name='sumbit' id='sumbit' value='登录'>")
        sb.AppendLine("<input
type='reset' name='reset' id='reset' value='重置'>")
        sb.AppendLine("</form>")
        e.WriteString(sb.ToString)
    Case
"exit.htm"
        e.Appendcookie("username",
"") '清除cookie中原来的用户名和密码
        e.Appendcookie("password",
"")
        e.WriteString("<meta
http-equiv='refresh' content='0; url=/logon.htm'>")
'跳转到登录页
    Case "",
"default.htm"
        sb.AppendLine("这是首页<br/><br/>")
        sb.AppendLine("<a
href='order.htm'>订购产品<a><br/>")
        sb.AppendLine("<a
href='product.htm'>产品列表<a><br/>")
        sb.AppendLine("<a
href='exit.htm'>退出登录<a><br/>")
        e.WriteString(sb.Tostring)
    Case
"order.htm"
        e.WriteString("这是订购页")
    Case
"product.htm"
        e.WriteString("这是产品页")
End
Select

代码逻辑并不复杂，所有知识之前都已经讲述过，唯一没有接触过的是自动跳转网页的代码：

<meta http-equiv='refresh'
content='2; url=/logon.htm'>

表示2秒后跳转到"/logon.htm"页面，如果你要立即跳转，将2改为0即可。

## 特殊内容的显示

特殊内容的显示


**特殊内容的显示**

**显示HTML标签**

如果我们在HttpRequest设置以下代码：

Dim
sb As
new
StringBuilder
sb.AppendLine("</br>表示换行,
段落以<p>开始,以</p>结束!")
e.WriteString(sb.Tostring)

意料之中，浏览器没有按照我们预期的方式显示：

如果要正常显示</br>等HTML标签，可以将代码改为：

Dim
sb As
new
StringBuilder
sb.AppendLine(HTMLEncode("</br>表示换行,
段落以<p>开始,以</p>结束!"))
e.WriteString(sb.Tostring)

现在浏览器就能正常显示了：

**保持格式显示**

假定有下图所示的一个表：

如果我们在HttpRequest设置以下代码：

Dim
sb As
new
StringBuilder
For
Each dr
As DataRow
In DataTables("唐诗").DataRows
    sb.Appendline(dr("内容"))
    sb.AppendLine("</br></br>")
Next
e.WriteString(sb.Tostring)

不出意料，浏览器的没有按照我们希望的格式显示：

这是因为浏览器在解析内容时，会将多个连续的空格或换行，转换为一个空格。

如果希望按照原来的格式显示，可以将代码改为：

Dim
sb As
new
StringBuilder
For
Each dr
As DataRow
In DataTables("唐诗").DataRows
    sb.Appendline("<pre>"
& dr("内容")
& "</pre>")
    sb.AppendLine("</br>")
Next
e.WriteString(sb.Tostring)

现在就可以按照原格式显示了：

提示：<pre>和</pre>之间的内容，会按照原格式显示。

## 适合在手机显示的网页

适合在手机显示的网页


**适合在手机显示的网页**

如果将HttpRequest事件的代码设置为：

Dim
sb As
New
StringBuilder
sb.appendLine("<form
action='showtj.htm' enctype='multipart/form-data' method='post' id='form1' name='form1'>")
sb.appendLine("请输入要统计的年月:</br></br>")
sb.appendLine("年:
<input type='number' name='year' id='year' min='1999' max='2018'><br/><br/>")
sb.appendLine("月:
<input type='number' name='month' id='month' min='1' max='12'><br/><br/>")
sb.appendLine("<input
Type='submit' name='Sumbit' id='Sumbit' value='开始统计'>")
sb.appendLine("</form>")
e.WriteString(sb.ToString)

在iPhone上用QQ浏览器访问，显示效果为：

文字很小，你要放大才能看清楚内容。

为解决这个问题，可以将代码改为：

Dim
sb As
New
StringBuilder
sb.AppendLine("<meta
name='viewport' content='width=device-width,initial-scale=1,user-scalable=0'>")
sb.appendLine("<form
action='showtj.htm' method='post' name='form1'>")
sb.appendLine("请输入要统计的年月:</br></br>")
sb.appendLine("年:
<input type='number' name='year' id='year' min='1999' max='2018'><br/><br/>")
sb.appendLine("月:
<input type='number' name='month' id='month' min='1' max='12'><br/><br/>")
sb.appendLine("<input
Type='submit' name='Sumbit' id='Sumbit' value='开始统计'>")
sb.appendLine("</form>")
e.WriteString(sb.ToString)

现在在iPhone上用QQ浏览器访问，可以正常显示了：

这里给网页加上了一行代码：

<meta name='viewport' content='width=device-width,initial-scale=1,user-scalable=0'>

viewport的content属性中可设置的值有：

initial-scal:  默认缩放比例。
maximum-scale: 允许用户缩放到的最大比例。
minimum-scale: 允许用户缩放到的最小比例。
user-scalable: 用户是否可以手动缩放，0禁止，1允许。
width:
视区宽度,以像素为单位的数字，设置为device-width表示整个设备的宽度。
height:         视区高度,以像雾为单位的数字，设置为device-height表示整个设备的高度。

这里要说明一下，我为什么要在手机上用QQ浏览器进行测试，这是因为微信已经是很多网页的入口，而QQ浏览其和微信内置的浏览器出自同门，显示效果是一样的。

**规范结构**

上述的代码虽然能在浏览器中正常显示，但实际上是不规范的，因为meta标签应该放在网页的head标签中：

<head>
<meta name='viewport' content='width=device-width,initial-scale=1,user-scalable=1'>
</head

而网页内容应该放在<body>标签中，所以我们修改一下代码：

Dim
sb As
New
StringBuilder
sb.appendLine("<!doctype
html>")
sb.appendLine("<html>")
sb.appendLine("<head>")
sb.AppendLine("<meta
name='viewport' content='width=device-width,initial-scale=1,user-scalable=1'>")
sb.appendLine("</head>")
sb.appendLine("<body>")
sb.appendLine("<form
action='showtj.htm' method='post' name='form1'>")
sb.appendLine("请输入要统计的年月:</br></br>")
sb.appendLine("年:
<input type='number' name='year' id='year' min='1999' max='2018'><br/><br/>")
sb.appendLine("月:
<input type='number' name='month' id='month' min='1' max='12'><br/><br/>")
sb.appendLine("<input
Type='submit' name='Sumbit' id='Sumbit' value='开始统计'>")
sb.appendLine("</form>")
sb.appendLine("</body>")
sb.appendLine("</html>")
e.WriteString(sb.ToString)

**用Chorme模拟手机浏览**

建议在开发电脑上，安装谷歌的Chorme浏览器。
在新版的Chorme中，按“Ctrl+Shift+I”，会进入开发者工具界面，在这个界面中，可以模拟网页在各种移动设备下的显示效果：

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

## 去掉通用事件头

去掉通用事件头


**去掉通用事件头**

我们知道，很难严格区分静态网页和动态网页，因为动态生成的网页，也需要使用不少静态的文件，例如图片、js、css等等。

所以我们总是在HtttpRequest事件的开始位置加上代码：

'通用事件头,用于发送已经存在的常见文件
Dim
fl As
String =
"d:\web\" &
e.path
If
filesys.FileExists(fl)
    Dim idx
As Integer
= fl.LastIndexOf(".")
    Dim ext
As String
= fl.SubString(idx)
    Select Case
ext
        Case
".jpg",".gif",".png",".bmp",".wmf",".js",".css"
,".html",".htm",".zip",".rar"
            e.WriteFile(fl)
            Return
'这里必须返回
    End
Select
End
If
'以下是动态生成网页的代码
'...

这有点繁琐，实际上这个事件头可以去掉的，只需将启动服务的代码改为：

HttpServer.Prefixes.Add("http://\*/")
HttpServer.WebPath
= "d:\web"
'指定静态文件存储位置
HttpServer.Start()

现在HtttpRequest不需要任何代码，
当用户访问某个文件时，系统会自动判断"d:\web"目录是否存在此文件，如果存在，则自动发送此文件，否则触发HttpRequet事件。

我们只用了3行代码，这应该是史上最简单的web服务搭建方法了。

从现在开始，我们的HttpRequest事件代码将不再包括通用事件头了，我们假定你已经使用上述代码启动了Web服务。

**关于后缀名**

如果给HttpServer设置了WebPath属性，在默认情况下，系统会发送该目录下以下类型的文件：
.jpg
.gif
.png
.bmp
.wmf
.js
.css
.html
.htm
.zip
.rar
.txt
.json
.svg
.ttf
.woff
.woff2
.eot
.ico
.map
.doc
.docx
.xls
.xlsx

HttpServer还有一个Extensions属性，这是一个集合，用于管理可发送文件的后缀名，我们可以根据需要添加删除后缀名，例如：

HttpServer.Prefixes.Add("http://\*/")
HttpServer.WebPath
= "d:\web"
HttpServer.Extensions.Remove(".doc")
HttpServer.Extensions.Remove(".docx")
HttpServer.Extensions.add(".table")
HttpServer.Start()

**提示：代码中的后缀名必须是小写，且必须以符号"."开头。**

## 提高编码效率

提高编码效率


**提高编码效率**

在开发B/S系统时，需要频繁通过菜单打开网络监视器，编写HttpRequest事件代码。

因为架构问题，打开网络监视器会有几秒的延时，对于开发效率会有一些影响，为解决这个问题，我们特意在网络监视器窗口加上了应用按钮：

单击此按钮，相关事件代码即时生效，无需关闭网络监视器，这样再次修改代码，就节省了打开网络监视器的时间。

大多数时候，移动端的关键代码都在自定义函数中，HttpRequest事件负责调用这些函数。为提高效率，我们也在自定义函数窗口也加上了应用按钮
，编辑函数代码后，单击应用按钮，函数代码即时生效：