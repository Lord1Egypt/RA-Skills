# Web数据源


## 关于三层架构和Web数据源

关于三层架构和Web数据源


**关于三层架构和Web数据源**

Foxtable可以直接连接后台数据库，默认是两层架构，客户端是Foxtable，服务端是数据库。

Foxtable
2018开始提供Web数据源，服务端可以创建一个本地数据源，然后通过HttpRequest事件公开给客户端。

客户端不再直接和服务端的数据库打交道，而是和服务端的HttpRequest事件交互，现在客户端和服务端中间多了一个Web层，成了三层结构。

相当多的企业因各种原因，不允许在网络上开放数据库端口，而Web数据源和三层架构的出现，为他们解决了这个大问题。

Web数据源和传统数据源有本质区别，但是Foxtable的开发人员做了大量的工作，使得Web数据源和传统数据源在开发和使用上没有任何区别，原二层架构系统的代码在转为三层架构之后，代码不需要任何的改变。

我们可以在一分钟内将一个二层结构的管理系统转换为三层结构，或将一个三层结构的管理系统转换为两层结构。

目前已知的区别只有一点：三层结构的系统，不能在客户端增加表、删除表或修改表结构，但三层结构的管理系统，已经有服务端项目，本就应该在服务端项目设计表，所以这不是一个问题，而是开发人员有意而为之。

在Web数据源出现之前，如果要开发基于互联网的管理系统，必须使用SQL
Server，现在我们也可以用Access了，大大简化服务端的搭建和准备工作，当然由于Access的并发量和负载能力都有限，所以仅适合搭建一些中小型的管理系统，大的管理系统依然应该采用SQL
Server数据库。

## 在服务端建立Web数据源

在服务端建立Web数据源


**在服务端建立Web数据源**

要使用Web数据源，必须有一个服务端项目，此项目运行在服务器，用于向客户端提供Web数据源。
Web数据源的建立非常简单，如果不需要身份验证，只需一行代码就能完成Web数据源的建立工作。

**设计步骤：**

1、首先我们在服务端的AfterOpenProject事件中加上以下代码，用于开启Web服务：

HttpServer.Prefixes.Add("http://\*/")
HttpServer.WebPath
= "d:\web"
HttpServer.Start()

如果你的服务端项目仅用于提供数据源服务，那么第二行代码可以删除。

2、假定服务器已经安装了SQL
Server，有一个名为Sample的数据源，我们现在建立一个数据源连接到这个数据库，使用生成器生成连接字符串的设置如下图：

生成的连接字符串为：

Provider=SQLOLEDB.1;Integrated Security=SSPI;Persist
Security Info=False;Initial Catalog=Sample;Data Source=.

如果你使用的是Access数据库，那么建立数据源的过程和以前没有区别，这里就不再赘述。

4、假定服务端建立的本地数据源的名称为"Orders"，现在将HttpRequest事件代码设置为：

Dim
Verified As
Boolean
If
e.PostValues.ContainsKey("username")
AndAlso e.PostValues.ContainsKey("password")
Then

'实际开发的时候,请改为根据用户表验证身份

Dim
username As
String  = e.PostValues("username")
    Dim password
As String  =
e.PostValues("password")
    If username
= "张三"
AndAlso password
= "888" Then
        Verified  =
True
    End
If
End
If
If
Verified = False
Then
    e.AppendCookie("Error","用户身份验证失败!")
'通过Cookie返回错误信息.

Return
End
If
Select
Case e.Path

Case
"DataServer.htm"
**e.AsDataServer("Orders")****'将一个本地数据源公开为Web数据源**
End
Select

提示：

1、AsDataServer方法用于将本地数据源转为Web数据源，并对外公开，其参数为本地数据源名称。
2、AsDataServer本身就是一个异步方法，可同时处理多个用户的访问请求，没有必要再次对其做异步处理。

至此我们的Web数据源就搭建完毕了，如果你的Web服务仅用于提供数据源，而且无需身份验证，那么可以将代码简化为一行：

e.AsDataServer("Orders")

服务器可以同时公开多个本地数据源，但是要注意区分路径，例如：

'省略的身份验证代码
Select
Case e.Path


Case
"DataServer.htm"
        e.AsDataServer("Orders")

Case
"Sales.htm"
        e.AsDataServer("Sales")
End
Select

## 在客户端连接Web数据源

在客户端连接Web数据源


**在客户端连接Web数据源**

请确保服务端项目已经启动。

在客户端项目连接Web数据源很简单，假定客户端和服务端项目在同一台电脑，为了连接上一节所创建的Web数据源，可以按下图所示输入连接字符串：

现在我们就可以像常规数据源一样，从这个Web数据源中添加数据表到Foxtable，一样可以增加、删除和修改数据，一样可以使用加载树和筛选树，一样可以进行各种统计分析，一样可以进行各种开发，源代码也和以前一样，没有任何特殊之处。

连接Web数据源时，通常需要附加一些表单数据或Cookie数据，服务端据此进行身份验证

Web数据源连接字符串格式为：

http://地址
-FormData-
键1:值1
键2:值2
-Cookies-
键1:值1
键2:值2

第一行为数据源的地址，"-FormData-"行之后为附加的表单数据，"-Cookies-"行之后为附加的Cookie数据。

可以看到Web数据源的创建和连接都很简单，为了方便，可以在开发过程中采用传统数据源，发布前再根据需要改为Web数据源即可，实际上对于已经发布的项目，也可以在传统数据源和Web数据源之间
随意切换。

**BeforeConnectOuterDataSource事件**

在连接Web数据源之前，一样会触发BeforeConnectOuterDataSource事件，我们可以在这里动态合成连接字符串，合成字符串的时候，必须严格按照上述格式要求。

例如：

If
e.Name =
"Orders" Then
    Dim sb
As New
StringBuilder
    sb.AppendLine("http://127.0.0.1/DataServer.htm")
    sb.AppendLine("-FormData-")
    sb.AppendLine("UserName:张三")
    sb.AppendLine("Password:888")
    e.ConnectionString
= sb.ToString()
End
If

运行过程中创建和修改Web数据源

可以在运行过程中创建一个Web数据源，例如：

Dim
sb As
New StringBuilder
sb.AppendLine("http://127.0.0.1/DataServer.htm")
sb.AppendLine("-FormData-")
sb.AppendLine("UserName:张三")
sb.AppendLine("Password:888")
Connections.Add("Sales",sb.ToString)

你也可以在运行过程中修改Web数据源的属性，例如：

Connections("Orders").DataServer
= "http://127.0.0.1/DataServer.htm"
Connections("Orders").FormData("UserName")
= "李四"
Connections("Orders").FormData("PassWord")
= "999"
Connections("Orders").FormData("AccessToken")
= "asgkfd9is45"
'添加一个新的表单项

提示：

1、上述属性对常规数据源无效。
2、实际开发中，请不要使用UserName和Password这种指向性很明确的词汇作为键名。
3、Foxtable已经占用的键名有： Action、Datatable、IgnoreSchema和Select。请不要在自己的代码中使用以上键名，以免冲突。

判断某个数据源是否可以连通

判断某个数据源是否可以连通的参考代码：

Dim
sb As
New StringBuilder
Dim
Err As
String
sb.AppendLine("http://127.0.0.1/DataServer.htm")
sb.AppendLine("-FormData-")
sb.AppendLine("UserName:张三")
sb.AppendLine("Password:888")
If
Connections.TryConnect(sb.Tostring,
Err) = False
Then
    MessageBox.Show(err,"提示",MessageBoxButtons.OK,MessageBoxIcon.Error)
'显示错误信息
Else
    MessageBox.Show("数据源可以正常连通!","提示",MessageBoxButtons.OK,MessageBoxIcon.Information)
End
If