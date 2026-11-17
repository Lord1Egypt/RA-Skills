## 高级数据接口完整文档
### 注意事项1：因为前端的HTML编辑器会用 new DOMParser().parseFromString() 处理最终的代码，注意 html tag 的属性要规范，避免在html标签内部使用{%if%} {%for%}等逻辑控制代码(就是<和>之间不能有twig逻辑标签{%if%} {%for%})
### 注意事项2：为避免在手工编辑页面时大量 {%%} 逻辑标签影响编辑体验，应该在{%%}外围包裹<!---->
### 注意事项3：twig的标签不能写在页面开头("<html>"标签的前面)，否则可能会被可视化编辑器过滤掉
### 注意事项4：<title>标签内不要使用使用{%%}逻辑标签
### 注意事项5：当页面需要拼接当前网站的完整URL时，URL中的域名部分不要写死，而是要用 {{FnGetHost($type)}} 来动态获取，参数 $type 的值为 0或1,0表示只返回域名，不包括访问协议，如 abc.com，1表示返回访问协议和域名，如 http://abc.com
### 注意事项6：如果要获取当前访问的完整URL，不需要或不希望手工拼接时，请使用  {{FnGetCurrentUrl()}} 来动态获取
### 注意事项7：如果一个页面中有多个系统表单(包括询盘表单和自定义表单)，要注意不同表单的样式/验证逻辑/JS逻辑这些要隔离，避免不同表单冲突或混淆

> 适用范围：本文件是 Twig 高级数据接口的完整参考，涵盖 `FnGetHost`/`FnGetCurrentUrl`、请求参数、菜单、产品、文章、下载、相册、门店、栏目、自定义表单、在线查询、SQLite、FAQ 系列函数。执行具体能力时按需查阅对应章节，无需通读。所有 `FnGet*` 返回字段以本文件为准；MCP 工具的 `get_*` 返回字段以 `references/mcp-tools.md` 为准，二者独立。

### 目录

- 一、基础工具函数（`FnGetHost`、`FnGetCurrentUrl`、`request`）
- 二、菜单（`FnGetMenu`）
- 三、产品（分类/列表/详情/上一下一篇）
- 四、文章/新闻（分类/列表/详情/上一下一篇）
- 五、下载（`FnGetDown*`）
- 六、相册（`FnGetGallery` / `FnGetOneGallery`）
- 七、门店（`FnGetStore`）
- 八、栏目（`FnGetColumn`）
- 九、自定义表单（`FnGetCustomForm`：字段类型/验证/上传/短信/地区/图形验证码）
- 十、产品询盘（见 `references/product-enquiry.md`）
- 十一、在线查询（`FnGetOnlineQuery` / `FnGetOnlineQueryResult`）
- 十二、SQLite（`FnSqliteQuery` / `FnSqliteExecute`）
- 十三、FAQ（`FnGetFaqClassList` / `FnGetFaqList`）

### 一、基础工具函数

#### 1. request - 获取当前请求参数
**功能**: 获取当前请求参数
**限制**: 不能在request中使用|default兜底表达式

**示例**:
{{ request.get.参数名 }} -- 获取当前网址问号后的参数值, 比如 {{ request.get.name }} 可以获取 ?name=xxx 的值
{{ request.post.参数名 }} -- 获取POST参数值, 比如 {{ request.post.name }} 可以获取post参数name的值
{{ request.param.参数名 }} -- 获取POST或网址问号后的参数值, 比如 {{ request.param.name }} 可以获取post参数name的值或?name=xxx的值，如果POST和问号都有传相同名称的值，以问号后的值优先
---

### 二、菜单相关函数

#### 1. FnGetMenu - 获取菜单树
**功能**: 获取指定父级ID的菜单树形结构
**参数**:
- `$ParentID` (int): 父级菜单ID,-1表示获取所有一级菜单

**返回**: 菜单数组,包含子菜单(sublist)

**示例**:
{# 获取一级菜单 #}
{% set menus = FnGetMenu(0) %}
<ul>
  {% for menu in menus %}
    <li>
      <a href="{{ menu.Url }}">{{ menu.Name }}</a>
      {# 二级菜单 #}
      {% if menu.sublist %}
        <ul>
          {% for sub in menu.sublist %}
            <li><a href="{{ sub.Url }}">{{ sub.Name }}</a></li>
          {% endfor %}
        </ul>
      {% endif %}
    </li>
  {% endfor %}
</ul>

{# 获取指定父菜单的子菜单 #}
{% set subMenus = FnGetMenu(5) %}

---

### 三、产品分类与列表

#### 1. FnGetProCls - 获取产品分类树
**功能**: 获取产品分类的树形结构
**参数**:
- `$ParentID` (int): 父级分类ID,0表示获取一级分类

**返回**: 分类数组,包含子分类(sublist)

**示例**:
{# 获取一级产品分类 #}
{% set categories = FnGetProCls(0) %}
<div class="category-list">
  {% for cat in categories %}
    <div class="category-item">
      <h3>{{ cat.Name }}</h3>
      {# 子分类 #}
      {% if cat.sublist %}
        <ul>
          {% for sub in cat.sublist %}
            <li>{{ sub.Name }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    </div>
  {% endfor %}
</div>

#### 2. FnGetProList - 获取产品列表
**功能**: 根据条件查询产品列表
**参数**:
- `$ClassID` (int/string): 分类ID,多个用逗号分隔
- `$offset` (int): 偏移量,-99返回分页信息
- `$pagesize` (int): 每页数量(最大100)
- `$keyword` (string, optional): 搜索关键词
- `$sortcol` (string, default='CrTime'): 排序字段
- `$sort` (string, default='desc'): 排序方式 asc/desc
- `$extParams` (array/string, optional): 扩展参数,支持 show_label, show_params, filtervalue

**返回**: 产品数组或分页信息

**分页说明**: 本函数为模板(Twig)侧分页，使用 `$offset`（偏移量，从 0 起；传 -99 返回分页信息）与 `$pagesize`（最大 100）。注意：MCP 工具 `get_product_list` 使用另一套分页参数——`page`（从 1 起）与 `pageSize`（最大 100），二者相互独立，调用 MCP 时请使用后者。

**返回字段说明**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `ProductID` | int | 产品ID（主键） |
| `SerialNum` | string | 产品货号 |
| `Price` | decimal | 产品售价 |
| `CrTime` | datetime | 创建时间 |
| `UpTime` | datetime | 发布时间/更新时间 |
| `BigImages` | array | 大图路径数组（已拼接完整路径：/comdata/{siteID}/product/xxx） |
| `SmallImages` | array | 小图路径数组（已拼接完整路径：/comdata/{siteID}/product/xxx） |
| `ImgBig` | string | 默认大图（BigImages第一个元素） |
| `ImgSmall` | string | 默认小图（SmallImages第一个元素） |
| `Name` | string | 产品名称 |
| `ProKeyword` | string | 产品关键词 |
| `ProDesc` | string | 产品描述 |
| `MarketPrice` | decimal | 市场价格 |
| `FuJianName` | string | 附件名称 |
| `Video` | text | 产品详情视频 |
| `SeoTitle` | string | SEO标题 |
| `SeoDesc` | string | SEO描述 |
| `VRUrl` | string | VR视频地址 |
| `OutsideUrl` | string | 跳转外链地址 |
| `CustomParamsOn` | tinyint | 是否开启自定义参数：0=不开启，1=开启 |
| `CustomParams` | text | 自定义参数JSON |
| `TopSet` | tinyint | 是否置顶：0=不置顶，1=置顶 |
| `ShareImg` | string | 分享头图路径 |
| `OutsideLinkList` | string | 平台导流链接列表 |
| `LabelsList` | array | 标签列表数组（当extParams包含show_label时），每个元素包含：`Name`(标签名称) |
| `PropertyList` | array | 产品参数列表（当extParams包含show_params时），每个元素包含：`id`(参数ID)、`name`(参数名称)、`value`(参数值)、`status`(状态) |
| `Status` | tinyint | 产品状态：0=不生效，1=生效 |
| `SiteID` | int | 站点ID |
| `Content` | text/array | 产品详情内容（HTML字符串或JSON数组，取决于decodeContent参数） |

**限制**:
1. 一般情况下，产品的名称，图片，查看情况的链接/按钮等，要加上链接到产品情况的链接
2. 当产品价格为空或0时，应该隐藏价格显示，或显示为"面议"

**示例**:
{# 获取最新10个产品 #}
{% set products = FnGetProList(0, 0, 10) %}
<div class="product-grid">
  {% for product in products %}
    <div class="product-item">
      <img src="{{ product.ImgBig }}" alt="{{ product.Name }}">
      <h4><a href="product-detail.html?id=XXXX">{{ product.Name }}</a></h4>
      <p class="price">¥{{ product.DefaultPrice }}</p>
      <p>{{ product.ProDesc|slice(0, 100) }}...</p>
      <a href="product-detail.html?id=XXXX">查看详情</a>
      {# 如果有标签 #}
      {% if product.LabelsList %}
        <div class="labels">
          {% for label in product.LabelsList %}
            <span class="label">{{ label.Name }}</span>
          {% endfor %}
        </div>
      {% endif %}
      
      {# 如果有参数 #}
      {% if product.PropertyList %}
        <ul class="params">
          {% for param in product.PropertyList %}
            <li>{{ param.name }}: {{ param.value }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    </div>
  {% endfor %}
</div>

{# 带搜索和排序 #}
{% set searchProducts = FnGetProList(5, 0, 20, '手机', 'Price', 'asc') %}

{# 获取分页信息 #}
{% set pageInfo = FnGetProList(0, -99, 10) %}
<p>总记录: {{ pageInfo.recordcount }}, 总页数: {{ pageInfo.pagecount }}</p>

{# 带标签和参数 #}
{% set extParams = {'show_label': 1, 'show_params': 1} %}
{% set products = FnGetProList(0, 0, 10, '', 'CrTime', 'desc', extParams) %}

#### 3. FnGetOnePro - 获取单个产品详情
**功能**: 根据产品ID获取完整产品信息
**参数**:
- `$ProductID` (int): 产品ID
- `$showjifen` (int, default=0): 是否显示积分信息

**返回**: 产品详细信息数组，包含以下字段：

**基础字段说明**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `ProductID` | int | 产品ID（主键） |
| `SerialNum` | string | 产品货号 |
| `Price` | decimal | 产品售价（根据用户等级计算后的价格） |
| `CrTime` | datetime | 创建时间 |
| `UpTime` | datetime | 发布时间/更新时间 |
| `BigImages` | array | 大图路径数组（已拼接完整路径：/comdata/{siteID}/product/xxx） |
| `SmallImages` | array | 小图路径数组（已拼接完整路径：/comdata/{siteID}/product/xxx） |
| `ImgBig` | string | 默认大图（BigImages第一个元素） |
| `ImgSmall` | string | 默认小图（SmallImages第一个元素） |
| `Name` | string | 产品名称 |
| `ProKeyword` | string | 产品关键词 |
| `ProDesc` | string | 产品描述 |
| `MarketPrice` | decimal | 市场价格 |
| `FuJianName` | string | 附件名称 |
| `Video` | text | 产品详情视频 |
| `SeoTitle` | string | SEO标题 |
| `SeoDesc` | string | SEO描述 |
| `VRUrl` | string | VR视频地址 |
| `OutsideUrl` | string | 跳转外链地址 |
| `CustomParamsOn` | tinyint | 是否开启自定义参数：0=不开启，1=开启 |
| `CustomParams` | text | 自定义参数JSON |
| `TopSet` | tinyint | 是否置顶：0=不置顶，1=置顶 |
| `ShareImg` | string | 分享头图路径 |
| `OutsideLinkList` | string | 平台导流链接列表 |
| `Status` | tinyint | 产品状态：0=不生效，1=生效 |
| `SiteID` | int | 站点ID |
| `Content` | array/text | 产品详情内容（JSON数组或HTML字符串） |
| `WebUserID` | int | 店铺用户ID（如果是店铺产品） |
| `JsonLD` | string | 产品结构化数据JSONLD） |

**产品详情内容字段特别说明**:
产品详情内容字段`Content`通常为JSON数组，极少情况下为原始HTML字符串，可参考下面的实例代码来列出详情内容
{% if product.Content %}
<div class="content">
  {% for section in product.Content %}
    <h3>{{ section.title }}</h3>
    <div>{{ section.content|raw }}</div>
  {% endfor %}
</div>
{% endif %}


**价格相关字段**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `DefaultPrice` | decimal | 默认出售价格（计算了用户等级及关联默认规格后的价格） |
| `OriginalPrice` | decimal | 原始价格（未根据用户等级计算的价格，用于分享） |
| `CostPrice` | decimal | 成本价格 |

**分类相关字段**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `ClassList` | array | 产品分类列表数组，每个元素包含：`ClassID`(分类ID)、`ClassName`(分类名称) |

**参数相关字段**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `ParamList` | array | 产品参数列表数组，每个元素包含：`ID`(参数ID)、`Name`(参数名称)、`Value`(参数值) |

**规格/SKU相关字段**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `Attrs` | array | 产品规格属性数组，每个元素包含：`AttrKeyID`(规格键ID)、`AttrKeyName`(规格键名称，如颜色、尺寸)、`hasImg`(是否有图片)、`AttrVals`(规格值数组) |
| `AttrVals` | array | 规格值数组（Attrs的子元素），每个元素包含：`AttrValID`(规格值ID)、`AttrValName`(规格值名称，如红色、XL)、`AttrKeyID`(所属规格键ID)、`AttrValBigImg`(规格值大图)、`AttrValSmallImg`(规格值小图) |

**标签相关字段**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `LabelList` | array | 产品标签列表数组，每个元素包含：`Name`(标签名称) |
| `Labels` | string | 标签ID字符串（逗号分隔） |

**示例**:
{% set product = FnGetOnePro(123) %}
<div class="product-detail">
  <h1>{{ product.Name }}</h1>
  
  {# 图片 #}
  {% if product.BigImages %}
    <div class="images">
      {% for img in product.BigImages %}
        <img src="{{ img }}" alt="{{ product.Name }}">
      {% endfor %}
    </div>
  {% endif %}
  
  {# 价格 #}
  <p class="price">¥{{ product.DefaultPrice }}</p>
  
  {# 分类 #}
  {% if product.ClassList %}
    <div class="categories">
      {% for cls in product.ClassList %}
        <span>{{ cls.ClassName }}</span>
      {% endfor %}
    </div>
  {% endif %}
  
  {# 参数 #}
  {% if product.ParamList %}
    <table class="params">
      {% for param in product.ParamList %}
        <tr>
          <td>{{ param.Name }}</td>
          <td>{{ param.Value }}</td>
        </tr>
      {% endfor %}
    </table>
  {% endif %}
  
  {# 规格/SKU #}
  {% if product.Attrs %}
    <div class="specs">
      {% for attr in product.Attrs %}
        <div class="attr-group">
          <strong>{{ attr.AttrKeyName }}:</strong>
          {% for val in attr.AttrVals %}
            <span>{{ val.AttrValName }}</span>
          {% endfor %}
        </div>
      {% endfor %}
    </div>
  {% endif %}
  
  {# 详情内容 #}
  {% if product.Content %}
    <div class="content">
      {% for section in product.Content %}
        <h3>{{ section.title }}</h3>
        <div>{{ section.content|raw }}</div>
      {% endfor %}
    </div>
  {% endif %}
  
  {# 标签 #}
  {% if product.LabelList %}
    <div class="tags">
      {% for tag in product.LabelList %}
        <span class="tag">{{ tag.Name }}</span>
      {% endfor %}
    </div>
  {% endif %}
</div>

#### 4. FnGetNextProduct / FnGetPrevProduct - 获取下一个/上一个产品
**功能**: 获取当前产品的下一个或上一个产品链接
**参数**:
- `$id` (int): 当前产品ID

**返回**: 下一篇/上一篇的基本信息数组 ['ID' => int, 'Name' => string, 'Url' => string]

**示例**:

<div class="article-navigation">
  <div class="prev">{% set prev = FnGetPrevProduct(product.ProductID) %} {% if prev is defined %} ID: {{prev.ID}} 标题：{{ prev.Name }} 网址：{{ prev.Url|raw }} {% endif %}</div>
  <div class="next">{% set next = FnGetNextProduct(product.ProductID) %} {% if next is defined %} ID: {{next.ID}} 标题：{{ next.Name }} 网址：{{ next.Url|raw }} {% endif %}</div>
</div>


---

### 四、文章/新闻相关

#### 1. FnGetNewsCls - 获取文章分类树
**功能**: 获取文章分类的树形结构
**参数**:
- `$ParentID` (int): 父级分类ID

**返回**: 分类数组

**示例**:

{% set newsCategories = FnGetNewsCls(0) %}
<nav class="news-nav">
  {% for cat in newsCategories %}
    <div class="nav-item">
      <h3>{{ cat.Name }}</h3>
      {% if cat.sublist %}
        <ul>
          {% for sub in cat.sublist %}
            <li>{{ sub.Name }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    </div>
  {% endfor %}
</nav>


#### 2. FnGetNewsList - 获取文章列表
**功能**: 根据条件查询文章列表
**参数**:
- `$ClassID` (int): 分类ID
- `$offset` (int): 偏移量,-99返回分页信息
- `$pagesize` (int): 每页数量(最大100)
- `$keyword` (string, optional): 搜索关键词
- `$sortcol` (string, default='UpTime'): 排序字段
- `$sort` (string, default='desc'): 排序方式

**返回**: 文章数组或分页信息

**分页说明**: 本函数为模板(Twig)侧分页，使用 `$offset`（偏移量，从 0 起；传 -99 返回分页信息）与 `$pagesize`（最大 100）。注意：MCP 工具 `get_news_list` 使用另一套分页参数——`page`（从 1 起）与 `pageSize`（最大 100），二者相互独立，调用 MCP 时请使用后者。

**返回字段说明**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `ArticleID` | int | 文章ID（主键） |
| `ImgSmall` | string | 文章小图路径 |
| `ImgBig` | string | 文章大图路径 |
| `CrTime` | datetime | 创建时间 |
| `UpTime` | datetime | 更新时间 |
| `Source` | string | 文章来源 |
| `Recommend` | int | 是否推荐：0=不推荐，1=推荐 |
| `TopSet` | int | 是否置顶：0=不置顶，1=置顶 |
| `PublishTime` | datetime | 发布时间 |
| `AuthorImg` | string | 作者头像路径 |
| `Author` | string | 文章作者 |
| `AuthorDesc` | string | 作者描述 |
| `Title` | string | 文章标题 |
| `ArtDesc` | string | 文章描述（SEO用） |
| `ArtKeyword` | string | 文章关键词（SEO用） |
| `Descriptor` | string | 文章摘要 |
| `TagKeyword` | string | 文章标签 |
| `SeoTitle` | string | SEO标题 |
| `Labels` | string | 文章标签，逗号隔开 |
| `OutsiteUrl` | string | 跳转外链地址 |
| `LikeNum` | int | 点赞数 |
| `GoodArticle` | tinyint | 好文推荐：0=否，1=是 |
| `RecIntroduction` | string | 好文引导推荐语 |
| `RecReply` | string | 推荐回复 |
| `RecNum` | int | 好文推荐数 |
| `RecBase` | int | 推荐基数 |
| `ShareImg` | string | 分享头图路径 |
| `Video` | string | 文章视频路径 |

**示例**:

{# 获取最新10篇文章 #}
{% set articles = FnGetNewsList(0, 0, 10) %}
<div class="article-list">
  {% for article in articles %}
    <article class="article-item">
      {% if article.ImgBig %}
        <img src="{{ article.ImgBig }}" alt="{{ article.Title }}">
      {% endif %}
      <h2>{{ article.Title }}</h2>
      <p class="desc">{{ article.Descriptor }}</p>
      <div class="meta">
        <span>作者: {{ article.Author }}</span>
        <span>发布时间: {{ article.PublishTime|date('Y-m-d') }}</span>
        <span>来源: {{ article.Source }}</span>
      </div>
      <a href="news-detail.html?id=XXXX">阅读全文</a>
    </article>
  {% endfor %}
</div>

{# 按分类获取 #}
{% set categoryArticles = FnGetNewsList(5, 0, 20) %}

{# 搜索文章 #}
{% set searchArticles = FnGetNewsList(0, 0, 10, '技术') %}


#### 3. FnGetOneNews - 获取单篇文章
**功能**: 根据文章ID获取完整文章信息
**参数**:
- `$NewsID` (int): 文章ID

**返回**: 文章详细信息，包含以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `ArticleID` | int | 文章ID（主键） |
| `ImgSmall` | string | 文章小图路径 |
| `ImgBig` | string | 文章大图路径 |
| `CrTime` | datetime | 创建时间 |
| `UpTime` | datetime | 更新时间 |
| `Source` | string | 文章来源 |
| `Recommend` | int | 是否推荐：0=不推荐，1=推荐 |
| `TopSet` | int | 是否置顶：0=不置顶，1=置顶 |
| `PublishTime` | datetime | 发布时间 |
| `AuthorImg` | string | 作者头像路径 |
| `Author` | string | 文章作者 |
| `AuthorDesc` | string | 作者描述 |
| `Title` | string | 文章标题 |
| `Content` | text | 文章内容（HTML格式） |
| `ArtDesc` | string | 文章描述（SEO用） |
| `ArtKeyword` | string | 文章关键词（SEO用） |
| `Descriptor` | string | 文章摘要 |
| `TagKeyword` | string | 文章标签 |
| `SeoTitle` | string | SEO标题 |
| `Labels` | string | 文章标签，逗号隔开 |
| `OutsiteUrl` | string | 跳转外链地址 |
| `PublishDelayTime` | datetime | 延时发布时间（定时发布用） |
| `ShowOrder` | int | 文章排序值 |
| `LikeNum` | int | 点赞数 |
| `GoodArticle` | tinyint | 好文推荐：0=否，1=是 |
| `RecIntroduction` | string | 好文引导推荐语 |
| `RecReply` | string | 推荐回复 |
| `RecNum` | int | 好文推荐数 |
| `RecBase` | int | 推荐基数 |
| `ShareImg` | string | 分享头图路径 |
| `Video` | string | 文章视频路径 |
| `ClassList` | array | 文章所属分类列表，每个元素包含：`ClassID`(分类ID)、`Name`(分类名称) |
| `JsonLD` | string | 文章结构化数据JSONLD） |

**示例**:

{% set article = FnGetOneNews(456) %}
<article class="article-detail">
  <h1>{{ article.Title }}</h1>
  
  <div class="article-meta">
    <span>作者: {{ article.Author }}</span>
    {% if article.AuthorImg %}
      <img src="{{ article.AuthorImg }}" alt="{{ article.Author }}">
    {% endif %}
    <span>发布时间: {{ article.PublishTime|date('Y-m-d H:i') }}</span>
    <span>来源: {{ article.Source }}</span>
  </div>
  
  {% if article.ImgBig %}
    <img src="{{ article.ImgBig }}" class="featured-image">
  {% endif %}
  
  <div class="article-content">
    {{ article.Content|raw }}
  </div>
  
  {% if article.Video %}
    <div class="video">
      <video src="{{ article.Video }}" controls></video>
    </div>
  {% endif %}
</article>


#### 4. FnGetNextNews / FnGetPrevNews - 获取下一篇/上一篇
**功能**: 获取当前文章的下一篇或上一篇文章链接
**参数**:
- `$id` (int): 当前文章ID

**返回**: 下一篇/上一篇的基本信息数组 ['ID' => int, 'Title' => string, 'Url' => string]

**示例**:

<div class="article-navigation">
  <div class="prev">{% set prev = FnGetPrevNews(article.ArticleID) %} {% if prev is defined %} ID: {{prev.ID}} 标题：{{ prev.Title }} 网址：{{ prev.Url|raw }} {% endif %}</div>
  <div class="next">{% set next = FnGetNextNews(article.ArticleID) %} {% if next is defined %} ID: {{next.ID}} 标题：{{ next.Title }} 网址：{{ next.Url|raw }} {% endif %}</div>
</div>


---

### 五、下载相关

#### 1. FnGetDownCls - 获取下载分类树
**功能**: 获取下载分类的树形结构
**参数**:
- `$ParentID` (int): 父级分类ID

**返回**: 分类数组

**示例**:

{% set downCategories = FnGetDownCls(0) %}
<ul class="download-categories">
  {% for cat in downCategories %}
    <li>
      <strong>{{ cat.Name }}</strong>
      {% if cat.sublist %}
        <ul>
          {% for sub in cat.sublist %}
            <li>{{ sub.Name }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    </li>
  {% endfor %}
</ul>


#### 2. FnGetDownList - 获取下载列表
**功能**: 根据条件查询下载列表
**参数**:
- `$ClassID` (int): 分类ID
- `$offset` (int): 偏移量,-99返回分页信息
- `$pagesize` (int): 每页数量(最大100)
- `$keyword` (string, optional): 搜索关键词
- `$sortcol` (string, default='CrTime'): 排序字段
- `$sort` (string, default='desc'): 排序方式

**返回**: 下载数组或分页信息

**示例**:

{% set downloads = FnGetDownList(0, 0, 10) %}
<div class="download-list">
  {% for down in downloads %}
    <div class="download-item">
      <h3>{{ down.Title }}</h3>
      <p>{{ down.Descriptor }}</p>
      <div class="file-info">
        <span>文件大小: {{ down.FileSize }}</span>
        <span>下载次数: {{ down.DownloadCount }}</span>
        <span>上传时间: {{ down.CrTime|date('Y-m-d') }}</span>
      </div>
      <a href="/index.php?c=Front/DownDetail&a=download&id={{ down.DownID }}" class="btn-download">
        点击下载
      </a>
    </div>
  {% endfor %}
</div>


#### 3. FnGetOneDown - 获取单个下载
**功能**: 根据下载ID获取完整下载信息
**参数**:
- `$ID` (int): 下载ID

**返回**: 下载详细信息

**示例**:

{% set download = FnGetOneDown(789) %}
<div class="download-detail">
  <h1>标题：{{ download.Title }}</h1>
  <div class="description">封面图：<img src="{{ download.ImgUrl }}"></div>
  
  <div class="file-info">
    <p>文件名: {{ download.Src }}</p>
    <p>文件大小: {{ download.FileSize }}</p>
    <p>下载次数: {{ download.Hits }}</p>
    <p>上传时间: {{ download.CrTime }}</p>
	  <p>内容: {{ download.Content }}</p>
  </div>
  
  <a href="/index.php?c=Front/DownDetail&a=download&id={{ download.DownID }}" class="btn-download">
    立即下载
  </a>
</div>


---

### 六、相册相关

#### 1. FnGetGallery - 获取相册列表
**功能**: 根据条件查询相册列表
**参数**:
- `$offset` (int): 偏移量
- `$num` (int): 每页数量(最大100)
- `$keyword` (string, optional): 搜索关键词(搜索Title字段)
- `$sortcol` (string, default='CrTime'): 排序字段
- `$sort` (string, default='desc'): 排序方式 asc/desc
- `$extParams` (array, optional): 扩展参数(预留)

**返回**: 相册数组，每个相册包含以下字段:
- `RecID`: 主键ID
- `ID`: 相册ID
- `SiteID`: 站点ID
- `Banner`: 相册封面图片路径(已自动添加 `/comdata/{SiteID}/gallery/` 前缀)
- `Title`: 相册名称
- `Intro`: 相册介绍
- `CrTime`: 相册创建时间
- `Status`: 相册状态(0=关闭, 1=展示)
- `ShowOrder`: 显示顺序
- `GalleryType`: 相册类型(sitegallery=PC端相册, wxgallery=手机端相册)

**示例**:
{# 获取最新10个相册 #}
{% set galleries = FnGetGallery(0, 10) %}
<div class="gallery-list">
  {% for gallery in galleries %}
    <div class="gallery-item">
      {% if gallery.Banner %}
        <img src="{{ gallery.Banner }}" alt="{{ gallery.Title }}">
      {% endif %}
      <h3>{{ gallery.Title }}</h3>
      <p>{{ gallery.Intro }}</p>
      <span class="time">{{ gallery.CrTime|date('Y-m-d') }}</span>
    </div>
  {% endfor %}
</div>

{# 带搜索和排序 #}
{% set searchGalleries = FnGetGallery(0, 20, '风景', 'ShowOrder', 'asc') %}

{# 按创建时间倒序 #}
{% set latestGalleries = FnGetGallery(0, 5, '', 'CrTime', 'desc') %}

#### 2. FnGetOneGallery - 获取单个相册详情
**功能**: 根据相册ID获取完整相册信息及相片列表
**参数**:
- `$id` (int): 相册ID

**返回**: 包含 gallery 和 itemList 的数组
- `gallery`: 相册基本信息(同FnGetGallery返回的单个相册结构)
- `itemList`: 相片数组，每个相片包含:
  - `ID`: 相片主键ID
  - `GalleryID`: 所属相册ID
  - `SiteID`: 站点ID
  - `ShowOrder`: 显示顺序
  - `Url`: 链接地址
  - `Image`: 相片路径
  - `Intro`: 相片介绍
  - `Title`: 相片标题

**示例**:
{% set galleryData = FnGetOneGallery(123) %}
{% if galleryData.gallery %}
<div class="gallery-detail">
  <h1>{{ galleryData.gallery.Title }}</h1>
  
  {% if galleryData.gallery.Banner %}
    <img src="{{ galleryData.gallery.Banner }}" class="banner">
  {% endif %}
  
  <p class="intro">{{ galleryData.gallery.Intro }}</p>
  
  {# 相片列表 #}
  {% if galleryData.itemList %}
    <div class="photo-grid">
      {% for item in galleryData.itemList %}
        <div class="photo-item">
          <img src="{{ item.Image }}" alt="{{ item.Title }}">
          {% if item.Title %}
            <h4>{{ item.Title }}</h4>
          {% endif %}
          {% if item.Intro %}
            <p>{{ item.Intro }}</p>
          {% endif %}
          {% if item.Url %}
            <a href="{{ item.Url }}">查看详情</a>
          {% endif %}
        </div>
      {% endfor %}
    </div>
  {% endif %}
</div>
{% endif %}

---

### 七、门店相关

#### 1. FnGetStore - 获取门店列表
**功能**: 根据条件查询门店列表
**参数**:
- `$offset` (int): 偏移量
- `$num` (int): 每页数量(最大100)
- `$keyword` (string, optional): 搜索关键词(搜索Name和Address字段)
- `$sortcol` (string, default='CrTime'): 排序字段
- `$sort` (string, default='desc'): 排序方式 asc/desc
- `$extParams` (array, optional): 扩展参数(预留)

**返回**: 门店数组，每个门店包含以下字段:
- `StoreID`: 门店ID
- `SiteID`: 站点ID
- `Name`: 门店名称
- `TelePhone`: 联系电话
- `Picture`: 封面图路径
- `BusinessHours`: 营业时间
- `Lng`: 经度
- `Lat`: 纬度
- `City`: 市ID
- `Province`: 省ID
- `District`: 区ID
- `Address`: 详细地址
- `CrTime`: 创建时间

**示例**:
{# 获取所有门店 #}
{% set stores = FnGetStore(0, 20) %}
<div class="store-list">
  {% for store in stores %}
    <div class="store-item">
      {% if store.Picture %}
        <img src="{{ store.Picture }}" alt="{{ store.Name }}">
      {% endif %}
      <h3>{{ store.Name }}</h3>
      <p class="phone">电话: {{ store.TelePhone }}</p>
      <p class="address">地址: {{ store.Address }}</p>
      {% if store.BusinessHours %}
        <p class="hours">营业时间: {{ store.BusinessHours }}</p>
      {% endif %}
      {% if store.Lng and store.Lat %}
        <div class="map" data-lng="{{ store.Lng }}" data-lat="{{ store.Lat }}"></div>
      {% endif %}
    </div>
  {% endfor %}
</div>

{# 搜索门店 #}
{% set searchStores = FnGetStore(0, 10, '北京') %}

{# 按创建时间正序 #}
{% set oldestStores = FnGetStore(0, 5, '', 'CrTime', 'asc') %}

---

### 八、栏目相关

#### 1. FnGetColumn - 获取栏目列表
**功能**: 根据栏目类型获取栏目列表
**参数**:
- `$type` (int): 栏目类型(0=文章栏目, 1=产品栏目)
- `$offset` (int): 偏移量
- `$num` (int): 每页数量(最大100)

**返回**: 栏目数组，每个栏目包含以下字段:
- `ID`: 栏目ID
- `SiteID`: 站点ID
- `Name`: 栏目名称
- `Type`: 栏目类型(0=文章, 1=产品)
- `ShowOrder`: 排序值

**示例**:
{# 获取文章栏目 #}
{% set articleColumns = FnGetColumn(0, 0, 10) %}
<nav class="article-columns">
  {% for column in articleColumns %}
    <a href="#" class="column-link">{{ column.Name }}</a>
  {% endfor %}
</nav>

{# 获取产品栏目 #}
{% set productColumns = FnGetColumn(1, 0, 10) %}
<ul class="product-columns">
  {% for column in productColumns %}
    <li>
      <strong>{{ column.Name }}</strong>
      {# 可以根据栏目ID获取对应的产品列表 #}
      {% set products = FnGetProList(column.ID, 0, 5) %}
      {% if products %}
        <ul>
          {% for product in products %}
            <li>{{ product.Name }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    </li>
  {% endfor %}
</ul>

{# 分页获取 #}
{% set moreColumns = FnGetColumn(0, 10, 5) %}

---

### 九、自定义表单

#### 1. FnGetCustomForm - 获取自定义表单
**功能**: 获取自定义表单的结构信息
**参数**:
- `$id` (int): 表单ID

**返回**: 包含 action, form, fields, needValidateCode, submitChecksum 的数组
- `action`: 表单提交地址
- `needValidateCode`: 是否需要图形验证码(0=否,1=是)；为 1 时表单需渲染图形验证码模块
- `submitChecksum`: 表单提交校验码，必须作为隐藏字段原样提交（见基础示例代码中的 submitChecksum 字段）
- `form`: 表单基本信息数组
  - `ID`: 表单ID
  - `Name`: 表单名称
  - `Intro`: 表单介绍
  - `SuccessMsg`: 提交成功提示语
  - `FailMsg`: 提交失败提示语
- `fields`: 表单字段数组,每个字段包含以下属性:
  - `ID`: 字段ID
  - `Name`: 字段显示名称(如:姓名、电话、邮箱等)
  - `Intro`: 字段说明/介绍
  - `FieldType`: 字段类型
    - `1`: 单行文本(input type="text")
    - `2`: 多行文本(textarea)
    - `3`: 单选框(radio)
    - `4`: 下拉选择(select)
    - `5`: 多选框(checkbox)
    - `6`: 图片上传(file type="file" accept="image/*")
    - `7`: 中国国内地区选择(省市区三级联动)
    - `8`: 时间选择(date/datetime picker)
    - `9`: 文件上传(普通文件)
    - `10`: 多图上传(file multiple)
    - `11`: 静态文本(仅显示,不可编辑)
    - `12`: 国际地区选择(国家/一级行政区域/二级行政区域 三级联动)
    - `13`: 公司名（单行文本）
    - `14`: 姓名（单行文本）
    - `15`: 邮箱（单行文本）
  - `FieldValues`: 字段选项值(用于单选、多选、下拉框),多个选项用 `|` 分隔,如: "选项1|选项2|选项3"
  - `FieldValuesRel`: 选项关联JSON数据(用于级联选择等复杂场景)
  - `Placeholder`: 输入框占位提示文字
  - `IsRequire`: 是否必填(0=非必填,1=必填)
  - `ValidateType`: 验证类型
    - `0`: 不验证
    - `1`: 普通文本
    - `2`: 数字
    - `3`: 手机号码
    - `4`: 座机号码
    - `5`: 座机或手机
    - `6`: 邮箱地址
    - `7`: 身份证号
  - `Icon`: 字段图标(CSS类名或图标路径)
  - `IsSmsValidate`: 是否需要短信验证(0=否,1=是)，ValidateType=3 且 FieldType 为 1、13、14 或 15 时有效
  - `IsEmailValidate`: 是否需要邮箱真实性验证(0=否,1=是)，ValidateType=6 且 FieldType 为 1、13、14 或 15 时有效；开启后字段自动设为必填
  - `values`: 解析后的选项数组(由 FieldValues 分割而来,仅在 FieldType 为 3/4/5 时存在)
  - `IsShow`: 字段是否显示(0=隐藏,1=显示)；前端应只渲染 IsShow=1 的字段
  - `IsShowTitle`: 静态文本字段(FieldType=11)是否显示标题(0=不显示标题,1=显示)
  - `ExtendName`: 字段扩展标识(如 Tel、Email、Name 等)，可用于按业务含义快速定位字段（见"使用技巧 1"）

**字段类型详细说明**:

| 类型 | FieldType值 | HTML控件 | 适用场景 | 特殊属性 |
|------|------------|----------|---------|---------|
| 单行文本 | 1 | `<input type="text">` | 通用短文本 | Placeholder, ValidateType, IsSmsValidate, IsEmailValidate |
| 多行文本 | 2 | `<textarea>` | 备注、描述、留言等长文本 | Placeholder, rows |
| 单选框 | 3 | `<input type="radio">` | 性别、满意度等单项选择 | FieldValues(选项用\|分隔) |
| 下拉选择 | 4 | `<select>` | 省份、服务类型等单项选择 | FieldValues, 标准HTML select标签 |
| 多选框 | 5 | `<input type="checkbox">` | 兴趣爱好、技能等多选 | FieldValues, name加[] |
| 图片上传 | 6 | `<input type="file">` | 头像、证件照等图片 | accept="image/*", 需enctype |
| 中国国内地区选择 | 7 | 三个`<select>`联动 | 省市区地址选择 | 需要JS实现三级联动，隐藏字段存储完整值 |
| 时间选择 | 8 | `<input type="text">` | 预约时间、生日等 | 通过JS插件实现日期选择器 |
| 文件上传 | 9 | `<input type="file">` | 文档、压缩包等文件 | 非图片文件上传 |
| 多图上传 | 10 | `<input type="file" multiple>` | 多张图片上传 | accept="image/*", multiple |
| 静态文本 | 11 | 纯文本显示 | 说明文字、提示信息 | IsShowTitle控制是否显示标题 |
| 国际地区选择 | 12 | 三个`<select>`联动 | 国家/一级行政区域/二级行政区域 地址选择 | 需要JS实现三级联动，隐藏字段存储完整值 |
| 公司名 | 13 | `<input type="text">` | 公司名称 | Placeholder, ValidateType, IsSmsValidate, IsEmailValidate |
| 姓名 | 14 | `<input type="text">` | 联系人姓名 | Placeholder, ValidateType, IsSmsValidate, IsEmailValidate |
| 邮箱 | 15 | `<input type="text">` | 邮箱地址 | Placeholder, ValidateType, IsSmsValidate, IsEmailValidate |

**验证类型说明**:

| ValidateType值 | 验证规则 | 正则表达式示例 |
|---------------|---------|--------------|
| 0 | 不验证 | - |
| 1 | 普通文本 | 无特殊限制 |
| 2 | 数字 | `/^[0-9]+$/` |
| 3 | 手机号码 | `/^1[3-9]\d{9}$/` |
| 4 | 座机号码 | `/^\d{3,4}-?\d{7,8}$/` |
| 5 | 座机或手机 | `/^1[3-9]\d{9}$\|^\d{3,4}-?\d{7,8}$/` |
| 6 | 邮箱地址 | `/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/` |
| 7 | 身份证号 | `/^[1-9]\d{5}(18\|19\|([23]\d))\d{2}((0[1-9])\|(10\|11\|12))(([0-2][1-9])\|10\|20\|30\|31)\d{3}[0-9Xx]$/` |

**使用技巧**:

1. **通过 ExtendName 快速定位字段**: 
   
   {% for field in form.fields %}
     {% if field.ExtendName == 'Tel' %}
       {# 专门处理电话字段 #}
     {% endif %}
   {% endfor %}
   

2. **动态设置placeholder**:
   
   placeholder="{{ field.Placeholder ?: '请输入' ~ field.Name }}"
   

3. **必填项标记**:
   
   {% if field.IsRequire == 1 %}
     <span class="required">*</span>
   {% endif %}
   

4. **条件显示**:
   
   {% if field.IsShow == 1 %}
     {# 只渲染显示的字段 #}
   {% endif %}
   

5. **图片/文件上传必须添加enctype**:
   html
   <form enctype="multipart/form-data">
   

6. **多选字段name要加[]**:
   html
   <input type="checkbox" name="col{{ field.ID }}[]">
   

7. **按ShowOrder排序**(后端已排序,前端直接使用即可)

8. **短信验证功能**:
   - **触发条件**: 当字段满足 `FieldType=1/13/14/15`（单行文本类）且 `ValidateType=3`（手机号）且 `IsSmsValidate=1` 时自动显示
   - **验证码输入框**: name格式为 `col{{ field.ID }}_vcode`，必须设置为必填（required）
   - **发送按钮**: 点击后调用短信接口发送验证码到用户输入的手机号
   - **验证流程**: 
     1. 用户输入手机号
     2. 点击"获取验证码"按钮
     3. 前端调用短信接口发送验证码
     4. 用户收到短信并输入验证码
     5. 提交表单时后端验证验证码是否正确
   - **示例代码**:
     {% if field.ValidateType == 3 and field.IsSmsValidate == 1 %}
     <span class="sms-validate-box">
         <input 
             class="sms-code" 
             name="col{{ field.ID }}_vcode" 
             placeholder="请输入验证码" 
             required
         >
         <button class="sms-btn" type="button">获取验证码</button>
     </span>
     {% endif %}

8.1. **邮箱真实性验证功能**:
   - **触发条件**: 当字段满足 `FieldType=1/13/14/15`（单行文本类）、`ValidateType=6`（邮箱）且 `IsEmailValidate=1` 时显示
   - **验证码输入框**: name格式为 `col{{ field.ID }}_vcode`，必须设置为必填（required）
   - **发送按钮**: 点击后调用邮箱验证码接口发送验证码到用户输入的邮箱
   - **验证流程**:
     1. 用户输入邮箱地址
     2. 前端校验邮箱格式
     3. 点击“获取验证码”按钮
     4. 前端调用邮箱验证码接口
     5. 用户收到邮件并输入验证码
     6. 提交表单时后端验证邮箱验证码是否正确
   - **示例代码**:
     {% if field.ValidateType == 6 and field.IsEmailValidate == 1 %}
     <span class="email-validate-box">
         <input
             class="email-code"
             name="col{{ field.ID }}_vcode"
             placeholder="请输入验证码"
             required
         >
         <button class="email-btn" type="button">获取验证码</button>
     </span>
     {% endif %}

9. **字段图标**:
   
   {% if field.Icon %}
     <img class="field-icon" src="{{ field.Icon }}" />
   {% endif %}
   

10. **使用FnGetFieldValuesArray函数解析选项**:
    
    {% for fieldValue in FnGetFieldValuesArray(field.FieldValues) %}
      <option value="{{ fieldValue }}">{{ fieldValue }}</option>
    {% endfor %}
    

11. **隐藏字段的命名规范**:
    - 所有字段的name统一使用 `col{{ field.ID }}` 格式
    - 上传文件的name使用 `file_{{ field.ID }}` 格式
    - 短信和邮箱验证码的name都使用 `col{{ field.ID }}_vcode` 格式
    - 地区选择需要额外的隐藏字段存储完整地区信息
    - 国际地区选择需要额外的隐藏字段存储完整地区信息

12. **中国国内地区选择JS联动**:
    - 省市区三个select需要通过JS实现联动
    - 选择省时自动加载对应城市列表
    - 选择市时自动加载对应区县列表
    - 最终值存储在隐藏的region字段中

13. **国际地区选择JS联动**:
    - 国家/一级行政区域/二级行政区域 三个select需要通过JS实现联动
    - 选择国家时自动加载对应一级行政区域列表
    - 选择一级行政区域时自动加载对应二级行政区域列表
    - 最终值存储在隐藏的global_region字段中

14. **时间选择器初始化**:
    - 时间字段使用文本框，需通过JS插件(如datetimepicker)初始化
    - 可配置日期格式、时间范围等参数

15. **表单自动验证功能**:
    - **内置验证脚本**: 表单已包含完整的JavaScript验证逻辑，无需额外编写
    - **必填验证**: 自动检查所有 `isrequire="1"` 的字段是否有值
    - **格式验证**: 根据 `validatetype` 自动验证手机号、邮箱、数字、身份证等格式
    - **多选验证**: 多选框字段会验证至少选中一个选项
    - **单选验证**: 单选框字段会验证至少选择一个选项
    - **文件验证**: 文件上传字段会验证对应的hidden input是否有值
    - **错误提示**: 验证失败时弹出alert显示所有错误信息
    - **阻止提交**: 验证失败时自动阻止表单提交

16. **表单AJAX提交**:
    - **自动拦截**: 表单submit事件被自动拦截，改为AJAX方式提交
    - **智能数据收集**: 
      - 自动遍历所有表单元素（input、select、textarea）
      - **排除file类型input**: 因为文件已提前上传并存入hidden input，无需重复提交
      - checkbox/radio只添加选中的项
      - 其他元素直接添加到FormData
    - **防重复提交**: 提交时禁用按钮并显示"提交中..."，完成后恢复
    - **响应处理**: 
      - 成功: 显示成功消息，重置表单，清空上传状态
      - 失败: 显示错误消息，恢复按钮状态
    - **JSON响应**: 后端应返回JSON格式: `{"success":true, "message":"提示信息"}`
    - **无需配置**: 自动使用form的action属性作为提交地址
    - **文件提交流程**:
      1. 用户选择文件 → 立即AJAX上传到服务器
      2. 上传成功后将文件路径写入hidden input
      3. 提交表单时只提交hidden input的值，不提交file input
      4. 后端从hidden input获取已上传的文件路径

17. **短信验证码功能**:
    - **自动绑定**: 短信按钮会自动绑定点击事件
    - **手机号验证**: 发送前自动验证手机号格式
    - **倒计时**: 发送后自动60秒倒计时，防止重复发送
    - **TODO提醒**: 代码中标记了需要接入实际短信API的位置
    - **自定义实现**: 可根据实际需求修改短信发送逻辑

18. **中国国内地区三级联动**:
    - **自动初始化**: 自动查找所有地区选择字段并初始化
    - **接口调用**:
      - 获取省份: `/index.php?c=Front/CustomForm&a=getRegion&type=prov`
      - 获取城市: `/index.php?c=Front/CustomForm&a=getRegion&type=city&prov=省ID`
      - 获取区县: `/index.php?c=Front/CustomForm&a=getRegion&type=district&prov=省ID&city=市ID`
    - **响应格式**: `{"success":true, "data":[{"ID":"1520", "Name":"东陵区"}]}`
    - **级联加载**: 
      - 页面加载时自动获取省份列表
      - 选择省份后自动加载对应城市列表，清空区县和隐藏字段
      - 选择城市后自动加载对应区县列表，清空隐藏字段
      - 选择区县后更新隐藏字段
    - **值存储**: 
      - select的value存储ID（用于联动查询）
      - hidden input存储名称（提交时使用）
      - 格式为"省名称/市名称/区名称"，例如: "辽宁省/沈阳市/东陵区"
    - **提交处理**: AJAX提交时，后端收到的是地区名称而非ID
    - **重置支持**: 表单提交成功后会自动重新加载省份列表

19. **国际地区三级联动**:
    - **自动初始化**: 自动查找所有地区选择字段并初始化
    - **接口调用**:
      - 获取国家列表: `/index.php?c=Front/CustomForm&a=getIntlRegion`
      - 获取一级行政区域列表: `/index.php?c=Front/CustomForm&a=getIntlRegion&parent_id=国家ID`
      - 获取二级行政区域列表: `/index.php?c=Front/CustomForm&a=getIntlRegion&parent_id=一级行政区域ID`
    - **响应格式**: `{"success":true, "data":[{"ID":"1520", "Name":"Guangdong"}]}`
    - **级联加载**: 
      - 页面加载时自动获取国家列表
      - 选择国家后自动加载对应一级行政区域列表，清空二级行政和隐藏字段
      - 选择一级行政区域后自动加载对应二级行政区域列表，清空隐藏字段
      - 选择二级行政区域后更新隐藏字段
    - **值存储**: 
      - select的value存储ID（用于联动查询）
      - hidden input存储名称（提交时使用）
      - 格式为"国家名称/一级行政区域名称/二级行政区域名称"，例如: "China/Guangdong/Foshan"
    - **提交处理**: AJAX提交时，后端收到的是地区名称而非ID
    - **重置支持**: 表单提交成功后会自动重新加载国家列表

20. **短信验证码接口**:
    - **接口地址**: `/index.php?c=Front/CustomForm&a=sendsmsvcode&mobile=手机号`
    - **请求方式**: GET
    - **前置验证**: 发送前自动验证手机号格式（/^1[3-9]\d{9}$/）
    - **响应格式**: `{"success":true, "message":"..."}` 或 `{"success":false, "message":"错误信息"}`
    - **防重复发送**: 发送成功后自动60秒倒计时
    - **错误处理**: 网络错误或接口失败时显示友好提示

20.1. **邮箱验证码接口**:
    - **接口地址**: `/index.php?c=validatecode&a=sendEmailCode&email=邮箱地址`
    - **请求方式**: GET
    - **前置验证**: 发送前自动验证邮箱格式
    - **响应格式**: `{"success":true, "msg":"ok"}` 或 `{"success":false, "msg":"错误信息"}`
    - **防重复发送**: 发送成功后自动60秒倒计时
    - **提交校验**: 表单提交时将 `col{{ field.ID }}_vcode` 与邮箱字段一起提交，由后端校验验证码
    - **注意**: 邮箱验证码必须使用邮箱接口，不能调用短信接口；短信和邮箱验证可在同一表单中分别配置

21. **图片验证码接口**:
    - **接口地址**: `/index.php?c=validatecode&useCurve=1&useNoise=1&fontSize=32&imageW=290&imageH=100`
    - **参数说明**:
      - `useCurve`: 是否使用曲线干扰（1=是）
      - `useNoise`: 是否使用噪点干扰（1=是）
      - `fontSize`: 字体大小（默认32，可根据实际需要调整）
      - `imageW`: 图片宽度（默认290，可根据实际需要调整）
      - `imageH`: 图片高度（默认100，可根据实际需要调整）
    - **显示逻辑**: 点击验证码输入框时显示图片，提供刷新按钮
    - **防缓存**: 每次请求添加时间戳参数避免浏览器缓存
    - **获取验证码参考代码，非常重要，请务必参考**: 
    ```html
      <input class="verify-input" type="text" name="vCode" placeholder="点击获取验证码" chname="验证码" isrequire="1" fieldtype="1" validatetype="1">
      <img class="verify-img" style="display:none" src="">
      <span class="refresh-btn" style="display:none">刷新验证码</span>
      <script>
	      // 图片验证码加载和刷新
              var verifyImg = form.querySelector('.verify-img');
              var refreshBtn = form.querySelector('.refresh-btn');
              var verifyInput = form.querySelector('.verify-input');

              if (verifyImg && refreshBtn && verifyInput) {
                  function getVerifyCodeUrl() {
                      return '/index.php?c=validatecode&useCurve=1&useNoise=1&fontSize=32&imageW=290&imageH=100&t=' + new Date().getTime();
                  }
                  verifyInput.addEventListener('click', function() {
                      if (verifyImg.style.display === 'none') {
                          verifyImg.src = getVerifyCodeUrl();
                          verifyImg.style.display = 'block';
                          refreshBtn.style.display = 'inline';
                      }
                  });
                  refreshBtn.addEventListener('click', function() {
                      verifyImg.src = getVerifyCodeUrl();
                  });
              }
      </script>
      ```

22. **文件上传接口**:
    - **单图/单文件上传**（类型6、9）:
      - **接口地址**: `/index.php?c=Front/CustomForm&a=uploadfile`
      - 请求方式: POST (multipart/form-data)
      - 响应格式: `{"success":true, "newfile":"\/comdata\/1001\/customform\/xxx.jpg"}`
      - 使用`<label for="file_{{ field.ID }}">`关联隐藏的file input，点击即选择
      - 选择文件后自动触发上传，无需额外按钮
      - 上传参数名: `file_{{ field.ID }}`
      - 上传成功后将`newfile`值写入对应的隐藏字段`col{{ field.ID }}`
      - 显示"上传成功"状态，清空file input允许重复上传
    - **多图/多文件上传**（类型10）:
      - **接口地址**: `/index.php?c=Front/CustomForm&a=uploadfiles`（注意是uploadfiles，不是uploadfile）
      - 请求方式: POST (multipart/form-data)
      - 响应格式: `{"success":true, "newfile":"\/path\/a.jpg,\/path\/b.jpg"}`（多文件时逗号分隔）
      - 使用`name="file_{{ field.ID }}[]"`作为上传参数名
      - 用户一次选择多个文件后，**一次性将所有文件添加到FormData**
      - 所有文件使用相同的参数名`file_XXX[]`添加到formData中
      - **必须添加`count`参数**: `formData.append('count', this.files.length)`，告知后端文件数量
      - **只调用一次上传接口**，后端PHP接收`$_FILES['file_XXX']`数组和`$_POST['count']`并自动处理
      - 后端返回的`newfile`字段已经是逗号分隔的文件路径字符串
      - 直接将返回的`newfile`值存入hidden input
      - 例如后端返回: `{"success":true, "newfile":"/comdata/1001/customform/a.jpg,/comdata/1001/customform/b.jpg"}`
      - 显示已上传文件数量
    - **必填验证**:
      - 表单提交时检查hidden input的值，而非file input
      - 确保上传成功后才能提交表单
    - **用户体验**:
      - 上传过程中显示"上传中..."或"上传中X个文件..."
      - 上传完成后显示"上传成功"或"已上传X张"
      - 失败时提示错误并清空状态
      - file input设置为display:none，通过label触发

23. **表单提交自定义表单示例代码，请务必参考，特别是示例代码里的JS处理逻辑**:
    - 请参考 customform-democode-base.md

> 注：本技能目前仅提供基础版示例。美化版（customform-democode-beautify.md）暂未包含在技能中，请始终以基础版代码为起点，仅修改样式、真实表单 ID 与字段展示结构，并保留其校验与提交逻辑。

---

### 十、产品询盘
**请参考[产品询盘说明] product-enquiry.md**

### 十一、在线查询

在线查询功能由后台 `tbl_onlinequery` 配置（含 `Condition` 查询条件、`Fields` 结果字段两组 JSON），前台提供两个 Twig 函数：`FnGetOnlineQuery` 负责"读出配置并渲染查询表单"，`FnGetOnlineQueryResult` 负责"执行查询并取回结果"。二者存在两种配合模式：AJAX 模式（推荐）与同步提交模式，见文末说明。

#### 1. FnGetOnlineQuery - 获取在线查询配置（渲染查询表单用）

**功能**：根据在线查询记录 ID，读取 `tbl_onlinequery` 中指定记录，把 `Condition`/`Fields` 两组 JSON 解码成数组，计算可查询状态，返回可直接用于渲染查询表单的数据数组。此函数只返回"表单配置数据"，并不执行查询；真正查询由表单提交到 `FormAction` 触发。

**参数**：
- `$id` (int)：在线查询记录 ID（`tbl_onlinequery.ID`）
- `$type` (string, default=`'json'`)：返回/提交模式。
  - `'json'`：表单通过 AJAX 提交到后端 `queryData&type=json`，后端返回 `{success:true, list:[…]}` JSON（前端自行渲染表格）。
  - 其它值（如 `'list'`）：表单**同步**提交到当前页面（URL 自动追加 `getOnlineQueryResult=1`），由 `FnGetOnlineQueryResult` 在服务端渲染结果。
- `$action` (string, default=`''`)：仅当 `$type!='json'` 时生效，作为表单提交地址；默认取当前页面 URL。

**返回**：关联数组（记录行），字段如下：

| 字段 | 类型 | 说明 |
|------|------|------|
| `ID` / `Name` / `Desc` / `BtnName` | 原表值 | 查询标题、描述、按钮文案等 |
| `StartTime` / `EndTime` | string | 可查询时间窗（来源 tbl_onlinequery） |
| `Status` | int | 0=启用，1=关闭 |
| `SuccessTips` / `FailTips` | string | 查询成功 / 无结果提示语 |
| `IsNullDisplay` | int | 是否隐藏空值字段（1=隐藏） |
| `IsFieldStress` / `FieldStress` | — | 是否高亮某字段及其列名 |
| `Condition` | array | 已解码的查询条件数组，每项含：`value`(列名colX)、`matchtype`(0精确/1模糊)、`filter`(1用AND/0用OR)、`valitype`(1=手机号需短信验证)、`tips`(占位提示)、`field`(字段显示名，取自 Fields.name，找不到时回退为 value) |
| `Fields` | array | 已解码的结果字段数组，每项含：`value`(列名colX)、`name`(显示名)、`_checked`(是否展示) |
| `IsCanQuery` | int | 可查询状态：**1**=可查，**2**=未开始，**0**=已截止，**-1**=已关闭（由 StartTime/EndTime/Status 计算，Status=1 强制覆盖为 -1） |
| `FormAction` | string | 表单提交地址。type=json 时为 `/index.php?c=Front/OnlineQuery&a=queryData&type=json`；否则为当前页 URL + `?getOnlineQueryResult=1` |
| `Type` | string | 传入的 `$type` 原值 |

**示例（AJAX 模式，配合前端 JS 把 `list` 渲染成表格），编写时请务必参考 online_query_democode.html 并注意保留里面的js逻辑**：
{% set oq = FnGetOnlineQuery(123) %}   {# 默认 type=json #}

{% if oq.IsCanQuery == 1 %}
<form method="post" action="{{ oq.FormAction }}" id="OnlineQueryForm{{ oq.ID }}">
  <input type="hidden" name="QueryID" value="{{ oq.ID }}">
  <input type="hidden" name="vCode" value="">
  {% for cond in oq.Condition %}
  <div class="oq-row">
    {% if not loop.first %}
      <span class="oq-link">{% if cond.filter == 1 %}且{% else %}或{% endif %}</span>
    {% endif %}
    <label>{{ cond.field }}</label>
    {% if cond.valitype == 1 %}
      <input type="tel" name="{{ cond.value }}" placeholder="{{ cond.tips|default('请输入手机号') }}" maxlength="11">
      <input type="text" name="{{ cond.value }}_vCode" placeholder="短信验证码" maxlength="6">
    {% else %}
      <input type="text" name="{{ cond.value }}" placeholder="{{ cond.tips|default('') }}">
    {% endif %}
  </div>
  {% endfor %}
  <button type="submit">{{ oq.BtnName|default('查询') }}</button>
</form>
{% elseif oq.IsCanQuery == 2 %}
  <p>查询尚未开始</p>
{% elseif oq.IsCanQuery == 0 %}
  <p>查询已截止</p>
{% elseif oq.IsCanQuery == -1 %}
  <p>查询已关闭</p>
{% endif %}

#### 2. FnGetOnlineQueryResult - 获取在线查询结果（服务端同步渲染用）

**功能**：直接调用后端 `OnlineQueryController::queryData`（内部强制 `type=list`）执行查询，返回结果数组。

**参数**：
- `$id` (int)：在线查询记录 ID

**返回**：结果数组（`list`），每个元素是一条记录，键为 `Fields` 中的显示名（`name`），值为对应列数据，例如：
```json
[
  {"姓名": "张三", "证书编号": "X123"},
  {"姓名": "李四", "证书编号": "X456"}
]
```
无匹配结果时返回 `null`。

**⚠️ 重要注意事项（易踩坑）**：
1. **依赖当前请求的表单 POST 数据**：本函数内部会校验图形验证码 `vCode` 与条件字段值。若当前请求没有有效的 `vCode`（例如页面初次加载就直接调用），函数会返回字符串 `"验证码不正确"`；若是其它异常（记录不存在、未到开始时间、已截止、短信验证码错误），底层会 `echo json_encode(...)` 并 `exit`，**直接中断整个页面渲染**。
2. **必须配合"同步提交"流程使用**：让 `FnGetOnlineQuery(id, 'list')` 渲染的表单（其 `FormAction` 含 `getOnlineQueryResult=1`）提交到当前页，页面重新渲染时再调用 `FnGetOnlineQueryResult(id)`——此时 `$_POST` 中已带 `vCode` 与条件值，才能正常返回结果数组。
3. **不适用于"打开即显示全部结果"**：那种场景请用 AJAX 模式（见 `FnGetOnlineQuery` type=json + 前端渲染 `list`）。
4. **图片字段**：但本函数只返回纯数组，图片需前端自行判断字段值是否为图片 URL 来渲染。

**示例（同步模式：表单提交到当前页，再渲染结果），编写时请务必参考 online_query_democode.html 并注意保留里面的js逻辑**：
{% set oq = FnGetOnlineQuery(123, 'list') %}
{# 上面渲染 oq.Condition 表单，action 指向 oq.FormAction（含 ?getOnlineQueryResult=1） #}

{% set result = FnGetOnlineQueryResult(123) %}
{% if result is iterable and result|length > 0 %}
<table class="oq-result-table">
  <thead>
    <tr>{% for key in result[0]|keys %}<th>{{ key }}</th>{% endfor %}</tr>
  </thead>
  <tbody>
    {% for row in result %}
    <tr>{% for val in row %}<td>{{ val }}</td>{% endfor %}</tr>
    {% endfor %}
  </tbody>
</table>
{% else %}
<p>{{ oq.FailTips|default('未查询到相关结果') }}</p>
{% endif %}

#### 3. 两种模式对照 & 与 JSON 契约的关系

| 模式 | FnGetOnlineQuery 调用 | FormAction | 结果获取 | 后端返回 | 适用场景 |
|------|----------------------|-----------|----------|----------|----------|
| **AJAX（推荐）** | `FnGetOnlineQuery(id)`（默认 `type=json`） | `…queryData&type=json` | 前端 AJAX 取 `list` 自行渲染表格 | `{success:true, list:[{字段名:字段值}]}` | 不刷新页面、前端控制表格样式 |
| **同步提交** | `FnGetOnlineQuery(id, 'list')` | 默认当前页 `?getOnlineQueryResult=1` | 模板内 `FnGetOnlineQueryResult(id)` 直接拿到数组 | 普通数组（无 success 包装） | 表单 POST 到自身或指定的Action目标、服务端整页渲染结果 |

####  4. 示例代码
请参考 online_query_democode.html

---

### 十一、SQLite 数据库查询

提供两个函数，可在模板里直接读写站点私有的 SQLite 数据库文件。典型用途：扩展本建站系统没有的功能，此功能需要简单的数据库支撑。

**数据库文件命名**：
- 命名：`$dbName` 只能是纯文件名（不能含 `/` `\` 或空字节），且必须匹配 `^[A-Za-z0-9_]+\.(db|sqlite)$`（仅字母、数字、下划线 + `.db` 或 `.sqlite` 后缀，后缀自动转小写）。例如 `member.db`、`product.sqlite`。
- 管理：数据库通常由后台上传（`.db`/`.sqlite`）或新建；模板里只需传入文件名（含后缀）引用，无需写路径。
- 若 `$dbName` 对应文件不存在，`FnSqliteQuery` 会直接抛出异常（`SQLite database not found`）并**中断整个页面渲染**，调用前请确认库已存在。

#### 1. FnSqliteQuery - 查询 SQLite 数据（只读）

**功能**：在指定 SQLite 数据库上执行 SELECT 查询，返回结果集（二维数组，每行一个关联数组）。

**参数**：
- `$dbName` (string)：数据库文件名（含 `.db`/`.sqlite` 后缀），如 `member.db`
- `$sql` (string)：SQL 语句，仅允许以 `SELECT` 开头
- `$params` (array, default=`[]`)：命名参数（关联数组），用于防 SQL 注入。键名可带或不带 `:` 前缀，SQL 中用 `:key` 占位

**返回**：二维数组（`list`），每个元素是一条记录（关联数组，键为列名）。例如：
```json
[
  {"id": "1", "name": "张三"},
  {"id": "2", "name": "李四"}
]
```

**⚠️ 重要限制（易踩坑）**：
1. **结果最多 1000 行**：底层会把任意 `SELECT` 自动包成 `SELECT * FROM (你的SQL) _limited_ LIMIT 1000`，超出部分被静默截断且不报错。大数据量请自行用 SQL 的 `LIMIT/OFFSET` 分页。
2. **仅允许查询**：走只读连接，执行 INSERT/UPDATE/DELETE 非 SELECT 语句会失败；写操作请用 `FnSqliteExecute`。
3. **只支持单条 SELECT**：带 `$params` 时内部禁止分号多语句，多语句会被拒绝。
4. **数据库必须存在**：文件不存在直接抛异常中断渲染（见上文）。

**示例**：
{% set result = FnSqliteQuery("test_db.sqlite", "SELECT * from users where status = :status", {"status": "active"}) %}
        {% if result is iterable and result|length > 0 %}
<table>
  <thead>
    <tr>{% for key in result[0]|keys %}<th>{{ key }}</th>{% endfor %}</tr>
  </thead>
  <tbody>
    {% for row in result %}
    <tr>{% for val in row %}<td>{{ val }}</td>{% endfor %}</tr>
    {% endfor %}
  </tbody>
</table>
{% else %}
<p>暂无数据 {{result}}</p>
{% endif %}

#### 2. FnSqliteExecute - 执行 SQLite 写操作

**功能**：在指定 SQLite 数据库上执行 INSERT / UPDATE / DELETE / CREATE 等写操作（或建表），返回受影响行数。

**参数**：
- `$dbName` (string)：数据库文件名（含后缀）
- `$sql` (string)：写操作 SQL（INSERT/UPDATE/DELETE/CREATE 等）
- `$params` (array, default=`[]`)：命名参数（关联数组），用于防注入；键名可带或不带 `:` 前缀，SQL 中用 `:key` 占位

**返回**：受影响行数（int）。无 `$params` 时走 `exec`，有 `$params` 时走 `prepare` + 绑定。

**⚠️ 注意事项**：
1. **仅允许单条语句**：带 `$params` 时，SQL 内部不得出现 `;`（多语句会被拒绝并抛异常）；无 `$params` 时也建议只写单条。
2. **参数必须是关联数组**：`$params` 的键须为非空字符串（自动补 `:`），非关联数组会抛异常。
3. **写库有风险**：前台模板直接写库会改变站点数据，务必确认业务确实需要，并做好权限与校验控制。
4. **表结构应预建**：建议在后台先创建好表结构再调用；`execute` 在读写模式下打开库，但首次凭空写表仍需 SQL 先 `CREATE TABLE`。

**示例**：
{% set affected = FnSqliteExecute('member.db', 'UPDATE member SET last_login = :t WHERE id = :id', {'id': 1, 't': '2026-08-21'}) %}
{# affected 为受影响行数 #}

#### 3. 参数绑定写法对照

| 写法 | 是否允许 | 说明 |
|------|----------|------|
| `FnSqliteQuery('a.db', 'SELECT * FROM t WHERE id = :id', {'id': 5})` | ✓ | 键不带 `:` 前缀，底层自动补 `:` |
| `FnSqliteQuery('a.db', 'SELECT * FROM t WHERE id = :id', {':id': 5})` | ✓ | 键带 `:` 前缀，等价 |
| `FnSqliteQuery('a.db', 'SELECT * FROM t WHERE id = 5')` | ✓ | 无参数，直接执行（仍受 LIMIT 1000 约束） |
| 值用字符串拼接进 SQL（如 `'... id = ' ~ id`） | ✗ | 禁止，存在 SQL 注入风险，务必用 `$params` 占位 |

---

### 十二、常见问题（FAQ）相关

#### 1. FnGetFaqClassList - 获取常见问题分类列表

**功能**: 获取当前站点的常见问题分类列表

**参数**: 无

**返回**: FAQ 分类数组。每个分类记录通常包含以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `ClassID` | int | 分类ID |
| `Name` | string | 分类名称 |
| `Icon` | string | 分类图标 |
| `SiteID` | int | 站点ID |

**示例**:

```twig
{% set faqClasses = FnGetFaqClassList() %}
<nav class="faq-category-list">
  {% for faqClass in faqClasses %}
    <a href="?classid={{ faqClass.ClassID }}">{{ faqClass.Name }}</a>
  {% endfor %}
</nav>
```


#### 2. FnGetFaqList - 获取常见问题列表

**功能**: 根据分类、关键词和分页条件查询当前站点已启用的常见问题

**参数**:

- `$classId` (int, default=0): 分类ID。传 `0` 表示不限制分类；FAQ 支持多个分类，按分类ID匹配

- `$keyword` (string, default=''): 搜索关键词，仅匹配问题内容（`Question`）

- `$page` (int, default=1): 页码，从 1 开始；传 `-99` 返回分页信息

- `$pageSize` (int, default=20): 每页数量

**返回**: FAQ 数组或分页信息。列表按 `IsTop DESC, ShowOrder DESC, ID DESC` 排序，且只返回 `Status=1` 的记录。

**FAQ 字段说明**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `ID` | int | FAQ ID（主键） |
| `SiteID` | int | 站点ID |
| `ClassID` | string | 所属分类ID，多个分类ID以逗号分隔并带首尾逗号，例如 `,1,3,` |
| `Question` | string | 问题内容 |
| `Answer` | text | 问题答案，通常为 HTML 内容 |
| `CrTime` | datetime | 创建时间 |
| `ShowOrder` | int | 显示排序值 |
| `IsTop` | tinyint | 是否置顶：0=否，1=是 |
| `Status` | tinyint | 状态：0=未启用，1=启用 |

**分页说明**: 本函数使用 `$page`（从 1 起）和 `$pageSize` 分页。传入 `$page=-99` 时返回：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `recordcount` | int | 符合条件的 FAQ 总数 |
| `pagecount` | int | 总页数 |
| `pagesize=` | int | 每页数量（底层返回键名包含等号） |

**示例**:

```twig
{# 获取第1页FAQ #}
{% set faqs = FnGetFaqList(0, '', 1, 10) %}
<section class="faq-list">
  {% for faq in faqs %}
    <article class="faq-item">
      <h3>{{ faq.Question }}</h3>
      <div class="faq-answer">{{ faq.Answer|raw }}</div>
    </article>
  {% endfor %}
</section>

{# 按分类和关键词搜索FAQ #}
{% set searchedFaqs = FnGetFaqList(5, '售后', 1, 20) %}

{# 获取分页信息 #}
{% set faqPageInfo = FnGetFaqList(0, '', -99, 20) %}
<p>共 {{ faqPageInfo.recordcount }} 条，{{ faqPageInfo.pagecount }} 页</p>
```
