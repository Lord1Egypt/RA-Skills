# AI 自由页数据调用说明

> 适用范围：本文件讲自由页的模板语法基础（变量输出、if/for/set/filter、Twig 1.3 限制）与系统/自定义数据源（`DataTag.sys` / `DataTag.custom`）。菜单、产品、文章、下载、相册、门店、栏目、自定义表单、在线查询、SQLite 等高级 `FnGet*` 函数见 `references/advanced-data-interface.md`。

### 注意事项1：因为前端的HTML编辑器会用 new DOMParser().parseFromString() 处理最终的代码，注意 html tag 的属性要规范，避免在标签属性中使用 {%if%} {%for%}等逻辑控制代码
### 注意事项2：本系统数据调用采用twig1.3，请不要使用超出twig1.3版本的语法，注意|default表达式不要嵌套，最多只能使用一层default

## 1. 数据源的获取方式
注意数据源(包括系统数据源和自定义数据源)标签都不要带default表达式

### 系统数据源 (System Data)
系统预置字段，可直接在模板中调用。注意只有以下字段或用，不要猜测下表中没列出的字段，也不要在以下字段中使用|default兜底表达式。

| 调用语法 | 说明 |
| :--- | :--- |
| {{DataTag.sys.getCompanyName}} | 获取公司名 |
| {{DataTag.sys.getAddress}} | 获取地址 |
| {{DataTag.sys.getSiteBah}} | 获取网站备案号 |
| {{DataTag.sys.getPhone}} | 获取固定电话 |
| {{DataTag.sys.getContact}} | 获取联系人 |
| {{DataTag.sys.getMobile}} | 获取业务联系手机 |
| {{DataTag.sys.getFax}} | 获取传真 |
| {{DataTag.sys.getEmail}} | 获取邮箱 |
| {{DataTag.sys.getPostCode}} | 获取邮政编码 |
| {{DataTag.sys.getCompanyUrl}} | 获取网址 |

### 自定义数据源 (Custom Data)
用于获取后台配置的业务数据。

| 调用语法 | 说明 |
| :--- | :--- |
| {{DataTag.custom.数据源名称1}} | 具体数据源名称请登录 **网站后台 -> 功能 -> 数据源** 菜单下获取 |
| {{DataTag.custom.数据源名称2}} | 自定义数据源 |
| {{DataTag.custom.数据源名称...}} | 自定义数据源 |

---

## 2. 高级数据接口
请参考[高级数据接口说明] advanced-data-interface.md

---

## 3. 模板语法

### 基本语法
用于输出变量的值。

{{变量名}} -- 获取变量值


### 控制指令

#### 一、条件控制：if / elseif / else
用于根据条件动态渲染内容。

**示例：**
{% if score >= 90 %}
    A
{% elseif score >= 60 %}
    B
{% else %}
    C
{% endif %}


**支持运算符：**
- 比较：==, !=, >, <, >=, <=
- 包含：in, not in
- 类型判断：is, is not

**特殊用法：**
{% if user is defined %}
{% if status in ['active', 'pending'] %}


#### 二、循环控制：for
用于遍历数组或对象。

**1. 遍历数组 / 对象**
{% for item in items %}
    {{ item.name }}
{% endfor %}


**2. 带索引的循环**
{% for i, item in items %}
    {{ i }} - {{ item }}
{% endfor %}


**3. loop 内置变量**
在循环体内可使用以下变量：

| 变量 | 含义 |
| :--- | :--- |
| loop.index | 当前循环次数（从 1 开始） |
| loop.index0 | 当前循环次数（从 0 开始） |
| loop.first | 是否为第一次循环 |
| loop.last | 是否为最后一次循环 |
| loop.length | 总数量 |

#### 三、中断与控制循环：break / continue
{% for i in 1..10 %}
    {% if i == 5 %}
        {% break %}
    {% endif %}
    {{ i }}
{% endfor %}


#### 四、变量控制：set
定义或修改临时变量。
{% set total = 100 %}
{% set items = [1, 2, 3] %}


#### 五、过滤与控制：filter
对块内容进行过滤处理。
{% filter upper %}
    hello world
{% endfilter %}


---

### 常用过滤器

#### 一、格式化与展示类（最常用）

| 过滤器 | 示例 | 说明 |
| :--- | :--- | :--- |
| date | {{ post.createdAt|date('Y-m-d H:i') }} | 日期格式化 |
| date (时区) | {{ post.createdAt|date('Y-m-d', 'Asia/Shanghai') }} | 带时区的日期格式化 |
| number_format | {{ price|number_format(2, '.', ',') }} | 数字格式化 (输出: 1,234.56) |
| format | {{ 'Hello %s'|format(user.name) }} | 字符串格式化 (类似 sprintf) |

#### 二、字符串处理类

| 过滤器 | 示例 | 说明 |
| :--- | :--- | :--- |
| upper / lower | {{ name|upper }} | 转为大/小写 |
| capitalize | {{ 'hello'|capitalize }} | 首字母大写 |
| trim | {{ text|trim }} | 去除首尾空白 |
| slice | {{ text|slice(0, 100) }}... | 截取字符串/数组 |
| replace | {{ 'Hello World'|replace({'World': 'China'}) }} | 替换字符串 |
| split | {% set parts = str|split(',') %} | 分割字符串为数组 |

#### 三、数组 / 对象处理类

| 过滤器 | 示例 | 说明 |
| :--- | :--- | :--- |
| length | {{ items|length }} | 获取长度 |
| first / last | {{ items|first }} | 获取第一个/最后一个元素 |
| join | {{ tags|join(', ') }} | 将数组拼接为字符串 |
