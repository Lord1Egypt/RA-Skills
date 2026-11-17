# JSON解析


## 解析JSON

解析JSON


**解析JSON**

JSON的解析，Foxtable采用的是第三方库Newtonsoft.JSON。

Foxtable已经引入了以下两个命名空间：

Newtonsoft.Json
Newtonsoft.Json.Linq

你可以直接在代码中使用Newtonsoft.JSON进行JSON的系列化和反系列化。

如果已经熟悉了Newtonsoft.JSON，可以跳过本节内容。

示例一

简单JSON对象的解析和注意事项。

在命令窗口执行：

Dim
json As
String =
"{'name':'李云龙','age':'36'}"
Dim
jo As
JObject = JObject.Parse(json)
Output.Show(jo("name"))
Output.Show(jo("age"))

显示的结果是：

李云龙
36

JSON对象成员可以直接转换为相应的数据类型，例如：

Dim
json As
String =
"{'name':'李云龙','age':'36'}"
Dim
jo As
JObject = JObject.Parse(json)
Dim
Name As
String  = jo("name")
Dim
Age As
Integer = jo("age")

但是有一个很奇怪的现象，直接将JSON成员和字符串组合会出错，例如以下代码是无法执行的的：

Dim
json As
String =
"{'name':'李云龙','age':'36'}"
Dim
jo As
JObject = JObject.Parse(json)
Output.Show("姓名:"
& jo("name")
& " 年龄:"
& jo("age"))

必须改为:

Dim
json As
String =
"{'name':'李云龙','age':'36'}"
Dim
jo As
JObject = JObject.Parse(json)
Output.Show("姓名:"
& jo("name").ToString()
& " 年龄:"
& jo("age").ToString())

此外JSON对象是区分大小写的，所以上述代码中，如果你改用JO("Name")是取不到值的，只能是jo("name")。

实际上你用JO("Name")取值，并不会出错，而是返回一个空值(Nothing)，我们可以用这个特性判断JSON对象是否包括指定名称的成员，例如：

Dim
json As
String =
"{'name':'李云龙','age':'36'}"
Dim
jo As
JObject = JObject.Parse(json)
Output.show(
jo("Name")
Is Nothing )
Output.show(
jo("Test")
Is Nothing )

显示的结果是：

True
True

**示例二**

解析嵌套对象。

在命令窗口执行：

Dim
json As
String =

"{'name':'李云龙','age':'36','card':{'bank':'工行','account':'123456'}}"
Dim
jo As
JObject = JObject.Parse(json)
Output.Show(jo("name"))
Output.Show(jo("age"))
Output.Show(jo("card")("bank"))
Output.Show(jo("card")("account"))

上面的JSON对象嵌套了一个子对象card，这个子对象有自己的属性(bank和account)。

显示的结果为：

李云龙
36
工行
123456

**示例三**

JSON值数组的解析。

在命令窗口执行：

Dim
json As
String =
"['张三','李四','王五']"
Dim
ja As
JArray = JArray.Parse(json)
For
i As
Integer = 0
To ja.Count
- 1
    output.show(ja(i))
Next

显示的结果是：

张三
李四
王五

JSON数组
的对象为JArray，数组成员的类型为JToken，所以也可以用下面的代码遍历JSON数组:

Dim
json As
String =
"['张三','李四','王五']"
For
Each v
As JToken
In JArray.Parse(json)
    Output.show(v)
Next

**示例四**JSON对象中的值数组的解析。

在命令窗口执行：

Dim
json As
String  =
"{'touser':['zhansan',
'lisi'],'msgtype':'text'}"
Dim
jo As
JObject = JObject.Parse(json)
Dim
ja As
JArray = jo("touser")
For
i As
Integer = 0
To ja.Count
- 1
   Output.Show(ja(i).ToString)
Next
Output.Show(jo("msgtype").Tostring)

上面的JSON对象中，touser属性是一个值数组，这个数组包括两个成员(zhansan和lisi)。

执行后显示的结果为：

zhansan
lisi
text

同样也可以通过JToken来遍历，得到的结果是一样的：

Dim
json As
String  =
"{'touser':['zhansan',
'lisi'],'msgtype':'text'}"
Dim
jo As
JObject = JObject.Parse(json)
For
Each jt
As JToken
In jo("touser")

Output.Show(jt)
Next
Output.Show(jo("msgtype").Tostring)

**示例五**

JSON对象数组的解析。

在命令窗口执行：

Dim
json As
String =
"[{'name':'李云龙','age':'36'},{'name':'黄晓明','age':'28'}]"
Dim
ja As
JArray = Jarray.Parse(json)
For
i As
Integer = 0
To ja.Count
- 1

OutPut.Show("姓名:"
& ja(i)("name").ToString()
&  "  年龄:"
& ja(i)("age").ToString())
Next

或者：

Dim
json As
String =
"[{'name':'李云龙','age':'36'},{'name':'黄晓明','age':'28'}]"
For
Each ep
As JToken
In JArray.Parse(json)

Output.Show("姓名:"
& ep("name").ToString()
&  "  年龄:"
& ep("age").ToString())
Next

显示的结果为：

姓名:李云龙 年龄:36
姓名:黄晓明 年龄:28

**示例六**

嵌套的对象数组解析。

在命令窗口执行：

Dim
json As
String =

"{'name':'李云龙','card':[{'bank':'工行','account':'123'},{'bank':'建行','account':'678'}]}"
Dim
jo As
JObject = JObject.Parse(json)
Output.Show(jo("name"))
For
Each jt
As JToken
In jo("card")
    Output.Show(jt("bank").ToString
& "|"
& jt("account").ToString)
Next

上面的JSON对象，其card属性是一个对象数组，包括两个银行卡信息。

显示的结果为：

李云龙
工行|123
建行|678

## 解析实例

解析实例


**JSON解析实例**

下面是[阿里云全国快递查询](0246.htm)接口返回的数据格式，顶层对象包括的属性非常多，其属性showapi\_res\_body是一个嵌套对象，这个嵌套对象本身也有很多属性，
其中的data属性是一个对象数组，这个数组的每个成员包括time和context属性：

{
  "showapi\_res\_code": 0,
  "showapi\_res\_error": "",
  "showapi\_res\_body": {
    "mailNo": "929601675231",
    "update": 1488784549365,
    "updateStr": "2017-03-06 15:15:49",
    "ret\_code": 0,
    "flag": true,
    "status": 4,
    "tel": "95338",
    "expSpellName": "shunfeng",
    "data": [
      {
        "time": "2017-03-03 08:42:59",
        "context": "已签收,感谢使用顺丰,期待再次为您服务"
      },
      {
        "time": "2017-03-03 07:40:22",
        "context": "正在派送途中,请您准备签收(派件人:李正国,电话:18907153726)"
      },
      {
        "time": "2017-03-03 06:08:45",
        "context": "快件到达
【武汉�~口区复兴村营业点】"
      },
      {
        "time": "2017-03-03 04:48:26",
        "context": "快件在【武汉吴家山集散中心】已装车，准备发往
【武汉�~口区复兴村营业点】"
      },
      {
        "time": "2017-03-03 00:07:27",
        "context": "快件到达
【武汉吴家山集散中心】"
      },
      {
        "time": "2017-03-02 22:54:14",
        "context": "快件在【武汉总集散中心】已装车，准备发往
【武汉吴家山集散中心】"
      },
      {
        "time": "2017-03-02 22:54:02",
        "context": "快件到达
【武汉总集散中心】"
      },
      {
        "time": "2017-03-02 15:00:33",
        "context": "快件在【深圳总集散中心】已装车，准备发往
【武汉总集散中心】"
      },
      {
        "time": "2017-03-02 14:47:39",
        "context": "快件到达
【深圳总集散中心】"
      },
      {
        "time": "2017-03-02 10:24:37",
        "context": "快件在【江门江海集散中心】已装车，准备发往下一站"
      },
      {
        "time": "2017-03-02 05:41:54",
        "context": "快件到达
【江门江海集散中心】"
      },
      {
        "time": "2017-03-01 22:31:24",
        "context": "快件在【湛江麻章集散中心】已装车，准备发往
【江门江海集散中心】"
      },
      {
        "time": "2017-03-01 22:24:37",
        "context": "快件到达
【湛江麻章集散中心】"
      },
      {
        "time": "2017-03-01 20:02:01",
        "context": "快件在【湛江市赤坎文保北村营业点】已装车，准备发往
【湛江麻章集散中心】"
      },
      {
        "time": "2017-03-01 19:49:28",
        "context": "顺丰速运
已收取快件"
      }
    ],
    "expTextName": "顺丰速运"
  }
}

首先将上面的JSON数据复制到剪贴版，然后在命令窗口执行下面的代码：

Dim
jo As
JObject = Jobject.Parse(ClipBoard.GetText)
If
jo("showapi\_res\_body")("data")
IsNot Nothing
Then
    For Each
jt As
JToken In
jo("showapi\_res\_body")("data")
        Output.Show(jt("time").ToString
& " | "
& jt("context").ToString)
    Next
End
If

可以得到解析结果：

2017-03-03
08:42:59 | 已签收,感谢使用顺丰,期待再次为您服务
2017-03-03 07:40:22 | 正在派送途中,请您准备签收(派件人:李正国,电话:18907153726)
2017-03-03 06:08:45 | 快件到达 【武汉�~口区复兴村营业点】
2017-03-03 04:48:26 | 快件在【武汉吴家山集散中心】已装车，准备发往 【武汉�~口区复兴村营业点】
2017-03-03 00:07:27 | 快件到达 【武汉吴家山集散中心】
2017-03-02 22:54:14 | 快件在【武汉总集散中心】已装车，准备发往 【武汉吴家山集散中心】
2017-03-02 22:54:02 | 快件到达 【武汉总集散中心】
2017-03-02 15:00:33 | 快件在【深圳总集散中心】已装车，准备发往 【武汉总集散中心】
2017-03-02 14:47:39 | 快件到达 【深圳总集散中心】
2017-03-02 10:24:37 | 快件在【江门江海集散中心】已装车，准备发往下一站
2017-03-02 05:41:54 | 快件到达 【江门江海集散中心】
2017-03-01 22:31:24 | 快件在【湛江麻章集散中心】已装车，准备发往 【江门江海集散中心】
2017-03-01 22:24:37 | 快件到达 【湛江麻章集散中心】
2017-03-01 20:02:01 | 快件在【湛江市赤坎文保北村营业点】已装车，准备发往 【湛江麻章集散中心】
2017-03-01 19:49:28 | 顺丰速运 已收取快件

可以看到，用JObject解析JSON数据是异常方便的。

## 生成JSON

生成JSON


**生成JSON**

我们当然可以手工编码生成JSON，但是比较繁琐，容易出错。

如果采用Newtonsoft.JSON生成，会变得简单可靠。

Foxtable已经引入了以下两个命名空间：

Newtonsoft.Json
Newtonsoft.Json.Linq

你可以直接在代码中使用Newtonsoft.JSON进行JSON的系列化和反系列化。

如果已经熟悉了Newtonsoft.JSON，可以跳过本节内容。

示例一

根据现有对象生成JSON。

例如根据当前登录用户生成JSON，可在命令窗口执行：

Dim
jo As
JObject = JObject.FromObject(User)
Dim
js As
String = jo.ToString()
Output.Show(js)

显示的结果为：

{
"Name": "张三",
"Group": null,
"Type": 2,
"Tag": null,
"Roles": "经理",
"Default": false,
"ExtendedValues": {}
}

示例二

动态生成JSON。

在命令窗口执行：

Dim
jo As
New
JObject
jo("Name")
= "张三"
jo("Group")
= "VIP"
jo("Type")
= 2
jo("Default")
= False
Output.Show(jo.ToString)

显示的结果为：

{
"Name": "张三",
"Group": "VIP",
"Type": 2,
"Default": false
}

**示例三**

生成包括嵌套对象的JSON。

在命令窗口执行：

Dim
jo As
New
JObject
jo("name")
= "李云龙"
jo("age")
= "36"
jo("card")
= New
JObject
jo("card")("bank")
= "工行"
jo("card")("account")
= "12345678"
Output.Show(jo.ToString)

显示的结果为：

{
  "name": "李云龙",
  "age": "36",
  "card": {
    "bank": "工行",
    "account": "12345678"
  }
}

**示例四**

生成包括数组的JSON。

在命令窗口执行：

Dim
jo As
New
JObject
jo("Name")
= "张三"
jo("Group")
= "VIP"
Dim
ja As
New Jarray
'定义数组
ja.Add("manager")
ja.Add("developer")
jo("Roles")
= ja
'将Roles设置为前面定义的数组
Output.Show(jo.ToString)

显示的结果为：


{
  "Name": "张三",
  "Group": "VIP",
  "Roles": [
    "manager",
    "developer"
  ]
}

下面是一段完全等效的代码，希望大家体会，在实际开发过程中灵活运用：

Dim
jo As
New
JObject
Dim
values() As
String = {"manager","developer"}
jo("Name")
= "张三"
jo("Group")
= "VIP"
jo("Roles")
= New Jarray(values)
Output.Show(jo.ToString)

**示例五**生成包括对象数组的JSON。

在命令窗口执行：

Dim
jo As
New
JObject
Dim
ja As
New
JArray
jo("dept")
= "销售部"
jo("mpr")
= "赵刚"
jo("staff")
=  ja
'
ja.Add(New
JObject)
'给数组添加两个对象成员
ja.Add(New
JObject)

ja(0)("name")
= "李云龙"
ja(0)("age")
= 36
ja(1)("name")
= "黄晓明"
ja(1)("age")
= 26
Output.Show(jo.ToString)

显示的结果为：

{
  "dept": "销售部",
  "mpr": "赵刚",
  "staff": [
    {
      "name": "李云龙",
      "age": 36
    },
    {
      "name": "黄晓明",
      "age": 26
    }
  ]
}

对象数组也是一个数组，只不过这个数组的成员也是JObject，JObject的成员可以是数组，数组的成员可以是JObject，二者可以层层嵌套，生成任意复杂的JSON。

## 生成实例

生成实例


**JSON生成实例**

在后面学习微信接口的时候，你会发现很多数据都需要用JSON格式提交到微信服务器。

例如下面是一个JSON格式的微信菜单数据，我们将这段数据提交到微信相关接口后，可以生成一个微信菜单。
这个菜单包括两个顶层按钮，第一个顶层按钮"今日歌曲"是一个普通按钮，第二个顶层按钮"功能"是一个菜单，这个菜单包括三个子菜单按钮，分别是"搜索"、"视频"和"赞一下我们"：

{
  "button": [
    {
      "type": "click",
      "name": "今日歌曲",
      "key": "V1001\_TODAY\_MUSIC"
    },
    {
      "name": "功能",
      "sub\_button": [
        {
          "type": "view",
          "name": "搜索",
          "url": "http://www.soso.com/"
        },
        {
          "type": "view",
          "name": "视频",
          "url": "http://v.qq.com/"
        },
        {
          "type": "click",
          "name": "赞一下我们",
          "url": "V1001\_GOOD"
        }
      ]
    }
  ]
}

我们可以用代码生成以上格式的数据，请务必仔细体会：

Dim
mnu As
New JObject
'菜单对象
Dim
button As
New
JArray
mnu("button")
= button
'菜单对象只有一个属性button,这个是一个数组,包括所有顶层菜单按钮.
'增加第一个顶层按钮.
button.Add(New
Jobject)
button(0)("type")
= "click"
button(0)("name")
= "今日歌曲"
button(0)("key")
= "V1001\_TODAY\_MUSIC"
'增加第二个顶层按钮,这个按钮其实是一个菜单.
button.Add(New
Jobject)
button(1)("name")
= "功能"
button(1)("sub\_button")
= New Jarray
'第二个顶层按钮的sub\_button属性是一个数组,包括所有的子菜单按钮
Dim
SubButton
As
JArray
=
button(1)("sub\_button")
'为方便后面的编码，将子菜单数组保存在变量SubButton中
'增加第一个子菜单按钮
SubButton.Add(New
Jobject)
SubButton(0)("type")
= "view"
SubButton(0)("name")
= "搜索"
SubButton(0)("url")
= "http://www.soso.com/"
'增加第二个子菜单按钮
SubButton.Add(New
Jobject)
SubButton(1)("type")
= "view"
SubButton(1)("name")
= "视频"
SubButton(1)("url")
= "http://v.qq.com/"
'增加第三个子菜单按钮
SubButton.Add(New
Jobject)
SubButton(2)("type")
= "click"
SubButton(2)("name")
= "赞一下我们"
SubButton(2)("url")
= "V1001\_GOOD"
Output.Show(mnu.ToString)
'生成JSON字符串

你也许觉得代码有点长，因为这是"硬"生成，但是自行用工具编写JSON数据非常繁琐，也很容易出错，多数时候我们会通过数据表输入菜单设置，然后用代码遍历数据表中的行自动生成JSON数据。

实际上我在编写上面这段实例代码时，已经考虑到你未来的需要，你可以很轻松地将上面这段代码改为根据数据表中的行遍历生成，这在《微信接口》这一章会有介绍。

## 压缩JSON

压缩JSON


**压缩JSON**

CompressJson是Foxtable提供的一个用于压缩JSON字符串的函数，该函数的参数可以是一个JObject或JArray，也可以是一个JSON字符串。

我们知道JObject等的ToString方法，输出的JSON字符串是经过格式化的，存在空格缩进和换行，以方便阅读。

例如：

Dim
json As
String =
"{'touser':['zhansan', 'lisi'],'msgtype':'text'}"
Dim
jo As
JObject = JObject.Parse(json)
Output.Show(jo.ToSTring)

输出结果为：

{
  "touser": [
    "zhansan",
    "lisi"
  ],
  "msgtype": "text"
}

如果用CompressJson函数输出，则会压缩掉多余的空格和换行，例如：

Dim
json As
String =
"{'touser':['zhansan', 'lisi'],'msgtype':'text'}"
Dim
jo As
JObject = JObject.Parse(json)
Output.Show(CompressJson(jo))

输出结果为：

{"touser":["zhansan","lisi"],"msgtype":"text"}

如果你需要在数据库中存储JSON字符串，先用CompressJson压缩一下比较合适。

## 关于引号

单引号还是双引号


**单引号还是双引号**

JSON可以用单引号，也可以用双引号，例如：

Dim
json As
String =
"{'name':'李云龙','age':'36'}"

也可以写为：

Dim
json As
String =
"{""name"":""李云龙"",""age"":""36""}"

为方便阅读，本文档很多地方采用了单引号编写JSON。

但实际上双引号才是标准的写法，兼容性最好，例如微信使用的JSON，就必须是双引号的。

所以自行编写JSON字符串的时候，最好全部使用双引号。

好消息是，Newtonsoft.JSON生成的JSON都是双引号的，所以基本上我们无需为这个问题分心。

## 解析XML

解析XML


**解析XML**

现在互联网的数据传递，JSON的使用率已经远远超过XML，我也推荐大家使用JSON。

但是微信有点奇葩，有的接口是XML，有的是JSON，开发者需要处理两种类型的数据，而且有时还需要转换。

为了提高大家的学习和开发效率，我们增加了一个新的类型XObject，让大家可以将XML数据直接作为JSON数据进行解析。

XObject和JObject在数据解析方面是完全相同的，可以说唯一差别就是类名不同，几乎不需要额外的学习就能掌握。

如果你熟悉.net，可以直接用.net的相关类库进行XML的解析和生成，也一样的简单，效率会更高一些。

至于普通用户，还是用XObject来得快捷方便。

由于Foxtable和System.XML.Linq命名空间都有名为XObject的类，实际使用时为避免冲突，必须加上命名空间Foxtable，例如：

Dim
xo As **Foxtable**.XObject


**示例一**

解析简单的XML。

源XML数据结构：

<XML>
<to>George</to>
<from>John</from>
<content>Don't forget the meeting!</content>
</XML>

在命令窗口执行下面的代码：

Dim
xml As
String =
"<xml><to>George</to><from>John</from><content>Don't forget the
meeting!</content></xml>"
Dim
xo As
Foxtable.XObject = Foxtable.XObject.Parse(xml)
Output.Show(xo("to"))
Output.Show(xo("from"))
Output.Show(xo("content"))

显示的结果为：

George
John
Don't forget the meeting!

可以看到解析XML和解析JSON的方法几乎是一样的。

**示例二**

嵌套XML的解析，源XML数据结构：

<XML>
<公司>宏兴贸易</公司>
<部门>
<名称>销售部</名称>
<员工>张三</员工>
<员工>李四</员工>
</部门>
<部门>
<名称>行政部</名称>
<员工>王五</员工>
<员工>赵六</员工>
</部门>
</XML>

在命令窗口执行以下代码：

Dim
xml As
String =
"<xml><公司>宏兴贸易</公司><部门><名称>销售部</名称><员工>张三</员工><员工>李四</员工></部门>"

xml
= xmL &

"<部门><名称>行政部</名称><员工>王五</员工><员工>赵六</员工></部门></xml>"
Dim
xo As
Foxtable.XObject = Foxtable.XObject.Parse(xml)
Output.Show(xo("公司"))
For
Each bm
As JToken
In  xo("部门")
    Output.show(bm("名称"))
    For Each
yg As
JToken In
bm("员工")

Output.Show(yg)
    Next
Next

显示的结果为：

宏兴贸易
销售部
张三
李四
行政部
王五
赵六

在解析XML的过程中，同一父节点之下的同名结点，会被解析为一个数组，为了验证这一点，可以在命令窗口执行：

Dim
xml As
String =
"<xml><公司>宏兴贸易</公司><部门><名称>销售部</名称><员工>张三</员工><员工>李四</员工></部门>"

xml =
xmL &

"<部门><名称>行政部</名称><员工>王五</员工><员工>赵六</员工></部门></xml>"
Dim
xo As
Foxtable.XObject = Foxtable.XObject.Parse(xml)
Output.Show(xo.ToString())

显示的结果为：

{
  "公司":
"宏兴贸易",
  "部门":
[
    {
      "名称":
"销售部",
      "员工":
[
        "张三",
        "李四"
      ]
    },
    {
      "名称":
"行政部",
      "员工":
[
        "王五",
        "赵六"
      ]
    }
  ]
}

可以看到，部门和员工，都是以JSON数组的形式存在，其中部门是对象数组，员工是值数组。

通过上面的代码，大家也可以看到将XML数据转为JSON数据是多么的简单。

既然是数组，就可以用JArray进行解析：

Dim
xml As
String =
"<xml><公司>宏兴贸易</公司><部门><名称>销售部</名称><员工>张三</员工><员工>李四</员工></部门>"

xml =
xmL &

"<部门><名称>行政部</名称><员工>王五</员工><员工>赵六</员工></部门></xml>"
Dim
xo As
Foxtable.XObject = Foxtable.XObject.Parse(xml)
Output.Show(xo("公司"))
Dim
bms As
JArray = xo("部门")
For
i As
Integer = 0
To bms.Count
- 1
    Output.show(bms(i)("名称"))
    Dim
ygs As
JArray = bms(i)("员工")
    For n
As Integer =
0 To
ygs.Count -
1
          Output.Show(ygs(n))
    Next
Next

当然用For Each语句处理起来更加简洁一些。

我们可以直接用索引提取数据，例如第一个部门的第二个员工，可以表示为：

Dim
nm As
String = xo("部门")(0)("员工")(1)

## 生成XML

生成XML


**生成XML**

我们也可以用XObject生成XML，和用JObject生成JSON的方法是一回事，只是前者用ToXML方法，后者用ToString方法。

示例一

在命令窗口执行：

Dim
jo As
New
Foxtable.XObject
jo("Name")
= "张三"
jo("Group")
= "VIP"
jo("Type")
= 2
jo("Default")
= False
Output.Show(jo.ToXML)

显示的结果为：

<XML><Name>张三</Name><Group>VIP</Group><Type>2</Type><Default>false</Default></XML>

**示例二**生成嵌套的XML。

在命令窗口执行：

Dim
xo As
New Foxtable.XObject
xo("name")
= "李云龙"
xo("age")
= "36"
xo("card")
= New JObject
xo("card")("bank")
= "工行"
xo("card")("account")
= "12345678"
Output.Show(xo.ToXML)

显示的结果为：


<xml><name>李云龙</name><age>36</age><card><bank>工行</bank><account>12345678</account></card></xml>

**示例三**

生成带数组的XML。

在命令窗口执行：

Dim
jo As
New Foxtable.XObject
jo("Name")
= "张三"
jo("Group")
= "VIP"
jo("Roles")
= New Jarray("manager","developer")
'定义数组
jo("Type")
= 2
Output.Show(jo.ToXML)

显示的结果为：


<XML><Name>张三</Name><Group>VIP</Group><Roles>manager</Roles><Roles>Developer</Roles><Type>2</Type></XML>

**示例四**生成包括对象数组的XML。

在命令窗口执行：

Dim
jo As
New Foxtable.XObject
Dim
ja As
New JArray
jo("dept")
= "销售部"
jo("mpr")
= "赵刚"
jo("staff")
=  ja '
For
i As
Integer = 1
To 2
    Dim so
As New
JObject

If
i = 1
Then
        so("name")
= "李云龙"
        so("age")
= 36
    Else
        so("name")
= "黄晓明"
        so("age")
= 26
    End If
    ja.Add(so)
Next
Output.Show(jo.ToXML)

显示的结果为：

<XML><dept>销售部</dept><mpr>赵刚</mpr><staff><name>李云龙</name><age>36</age></staff><staff><name>黄晓明</name><age>26</age></staff></XML>

## CDATA结点

CDATA结点


CDATA结点

XML的CDATA结点可以理解为数据结点，此类结点的内容会被原样不动解析，内容中的所有标记都会被忽略，也就是说CDATA结点可以包括任意特殊字符。

微信接收方的消息都是XML结构，其中很多结点就是CDATA的：

<xml>
<ToUserName><![CDATA[gh\_c78d6e907523]]></ToUserName>
<FromUserName><![CDATA[o\_0W1wG4xCDJTpdqlTfjSdVjlznQ]]></FromUserName>
<CreateTime>1483933403</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[测试文本]]></Content>
<MsgId>6373445435737863016</MsgId>
</xml>

其中有4个结点是CDATA的，CDATA结点内容
以“<![CDATA[”开始，以“]]>”结束。

**解析CDATA结点**

将上面的XML数据复制到剪贴板，在命令窗口执行下面的代码：

Dim
xo As
Foxtable.XObject =
Foxtable.XObject.Parse(ClipBoard.GetText())
Output.Show(xo("ToUserName"))
Output.Show(xo("FromUserName"))
Output.Show(xo("CreateTime"))
Output.Show(xo("MsgType"))
Output.Show(xo("Content"))
Output.Show(xo("MsgId"))

显示的结果为：

gh\_c78d6e907523
o\_0W1wG4xCDJTpdqlTfjSdVjlznQ
1483933403
text
测试文本
6373445435737863016

可以看到CDATA结点的解析和普通结点是一样的。

**增加CDATA结点**

Foxtable.XObject的AddCDATA方法用于新增CDATA结点，此方法的语法为：

AddCDATA(Key, Value)

Key：  结点名称
Value：结点值

例如在命令窗口执行：

Dim
xo As
New Foxtable.XObject
xo("name")
= "李云龙"
xo("age")
= 38
xo.AddCDATA("remark","1+
2 <> 2")

xo("rank")
= "少将"
Output.Show(xo.ToXML)

显示的结果为：

<XML><name>李云龙</name><age>38</age><remark><![CDATA[1+ 2 <>
2]]></remark><rank>少将</rank></XML>