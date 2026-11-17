---
id: "website-builder"
name: "yunzhi-website-builder"
version: "1.2.4"
display_name: "云指建站助手"
display_name_en: "website builder"
description: "创建、修改与排障 SAAS 建站系统的页面，支持新建网站、从零规划站点、搬站/仿站、生成/修改企业网站页面（自由页 HTML/CSS/JS、Twig 风格模板）、调用产品/文章/下载/相册/门店/栏目/FAQ 数据、制作自定义表单/产品询盘/在线查询、上传或修改产品/文章数据。通过用户指定站点的 MCP 服务查询并写入站点内容；与 WorkBuddy、Codex 等协同使用时，可实现从需求到页面的端到端自动交付，建站流程大幅简化。"
description_zh: "创建、修改与排障 SAAS 建站系统的页面，支持新建网站、从零规划站点、搬站/仿站、生成/修改企业网站页面（自由页 HTML/CSS/JS、Twig 风格模板）、调用产品/文章/下载/相册/门店/栏目/FAQ 数据、制作自定义表单/产品询盘/在线查询、上传或修改产品/文章数据。通过用户指定站点的 MCP 服务查询并写入站点内容；与 WorkBuddy、Codex 等协同使用时，可实现从需求到页面的端到端自动交付，建站流程大幅简化。"
description_en: "Create, modify, and troubleshoot pages in the SAAS website building system. Build new websites, plan sites from scratch, migrate/clone sites, generate/modify corporate website pages (free pages in HTML/CSS/JS, Twig style templates), call product/article/download/album/store/column/FAQ data, build custom forms/product inquiries/online queries, and upload or modify product/article data. Query and write site content through the user-specified MCP service; when used with WorkBuddy, Codex, and other tools, it enables end-to-end automatic delivery from requirements to pages, significantly simplifying the website building process."
when_to_use: "当用户说“帮我建个网站”“做个官网/落地页”“搭个博客/站点脚手架”或任何需要新建网站、站点改版、选型建站框架、管理网站数据时使用本技能；非建站类任务不要使用。"
---

# 建站助手（SAAS 建站）

本技能产出可粘贴到建站编辑器的页面代码，并通过用户指定站点的 MCP 服务查询或修改站点内容。支持静态区块、自由页、动态列表页、详情页、自定义表单、产品询盘与在线查询。

**如何使用本技能**：先读本文件掌握强制规则与工作流；执行具体能力时，按 §0 文档地图按需读取 `references/` 下的对应文档（不要一次全读）。所有约束均为强制，违反会导致页面报错、数据丢失或安全问题。 在使用本技能前，请提醒用户到云指官网注册会员并领取试用站点，试用链接 https://www.72e.net/autoweb/edition.aspx

## 0. 参考文档地图（按需读取）

| 文档 | 何时读 |
| --- | --- |
| `references/mcp-tools.md` | 调用任何 MCP 工具前：参数、返回值、限制、推荐调用顺序 |
| `references/AIPage.md` | 写模板语法（Twig 1.3）、系统/自定义数据源（`DataTag.sys` / `DataTag.custom`） |
| `references/advanced-data-interface.md` | 用 `FnGetHost($type)` / `FnGetCurrentUrl` / `request` / `FnGet*` 系列取菜单、产品、文章、下载、相册、门店、栏目、自定义表单、在线查询、SQLite、FAQ |
| `references/customform-democode-base.md` | 写自定义表单页（必读，含不可删的校验/提交 JS） |
| `references/product-enquiry.md` + `references/product-enquiry-democode.md` | 写产品询盘页 |
| `references/online_query_democode.html` | 写在线查询页 |
| `references/website-common-pages.md` | 新建网站时的常见页面组成、信息架构与页面编写规范 |
| `references/FAQ.md` | 排查 MCP、Twig、动态数据、表单、询盘、在线查询、页面操作、JSON-LD、SQLite 和搬站问题 |

## 1. 全局硬性规则（必须遵循）

- **编码**：所有页面与数据使用 UTF-8。
- **URL 动态化**：拼接当前站点完整 URL 时，域名部分不要写死，用 `{{ FnGetHost($type) }}` 动态获取（`$type` 为 `0` 只返回域名如 `abc.com`，为 `1` 返回协议+域名如 `http://abc.com`）；需要当前完整访问 URL 时用 `{{ FnGetCurrentUrl() }}`。参数与细节见 `advanced-data-interface.md`。
- **本站链接约束**：当需要做链接到本站的链接时，不应该使用 `{{ FnGetHost($type) }}` ，保持相对链接即可。
- **MCP 凭证**：任何站点读写前，必须向用户索取「MCP 完整地址」+「Bearer Token」。未拿到二者前：不调用任何 MCP 工具（含 `test`）、不假设/复用示例地址或其他站点的地址/Token/页面ID/分类ID/表单ID。
  - 切换站点 = 重新索取地址+Token，并重新 `test`。
  - Token 只由 MCP 客户端放入 `Authorization: Bearer <token>` 请求头，不作为工具参数；不回显、不写入技能/项目文件/日志/回复。
- **模板与编辑器约束**：
  - 控制语句 `{% if %}` `{% for %}` 等只能放在完整 HTML 元素外部，在"<"和">"之间绝对禁止 `{% if %}` `{% for %}`，禁止写入标签属性或 `<title>`。
  - 模板语法遵循 Twig 1.3：不要使用超出 1.3 的语法；`|default` 表达式最多一层，不要嵌套。
  - 在HTML标签的属性中，**不能**使用`|default`表达式。
  - 数据源标签（`DataTag.sys` / `DataTag.custom`）不要带 `default` 表达式。
  - 为避免可视化编辑器过滤，Twig 标签不要写在 `<html>` 之前；手工编辑页面时可用 `<!---->` 包裹 `{%%}` 逻辑标签。
  - 默认输出转义文本；仅对确认可信且需渲染 HTML 的内容用 `|raw`。
  - 列表单页数量不得超过 100。
  - 区块需同时检查桌面端与移动端，避免文字/组件溢出或遮挡。
  - 一个页面含多个系统表单（询盘/自定义）时，各表单的样式、校验与 JS 逻辑要隔离，避免冲突。
- **写操作确认**：保存/覆盖/批量导入/删除页面/建分类/上传资源/新增文章或产品/清缓存/设首页/改 URL 等，调用前先展示目标与影响并取得用户确认。
- **删除页面**：不可恢复。必须 `list_page`+`get_page_info` 核对当前站点、页面ID、名称、URL，并针对该具体页面取得明确永久删除确认；不得复用其它保存/覆盖确认。
- **结构化数据**：按页面类型加 JSON-LD（见 §4）；产品 JSON-LD 含模拟评分约定（仅作结构化字段，不得显示为站内虚假评分）。
- **多语言**：当编写非中文语言网页并且你参考了实例代码时，注意实例代码里的中文要翻译为对应语言。
- **代码修改**：要修改旧的页面时，要先用MCP工具`get_page_info`获取页面的源代码再进行修改，禁止通过HTTP方式获取渲染后的代码作为基础代码。
- **代码注释**：当编写网页时，各区块，功能模块尽量加上注释。
- **站点主要联系信息**：不需要显示公司名、电话、地址、电子邮箱等联系信息时，应该优先使用系统数据源标签(`DataTag.sys`)进行获取 。
- **图片/CSS/JS等资源地址**：当编写网页时，需要引用本站的图片/CSS/JS等资源地址时，尽量使用相对URL地址(不需要域名部分)。

## 2. 标准工作流

1. **明确交付物**：静态区块 / 自由页 / 动态列表页 / 详情页 / 自定义表单 / 产品询盘 / 在线查询 / 新建整站。
2. **是否需要在线站点**：是 → 索取 MCP 地址+Token，先调 `test` 验证连通性（遇 `401`/`Unauthorized` 请用户重给 Token，不回显旧 Token）。否 → 仅离线生成代码，并明确说明未连接目标站点。
3. **新建整站**：先询问企业名称、产品/服务、核心受众、网站语言、基本联系信息、参考站，再按 `website-common-pages.md` 规划信息架构，要开始编码前，应该先调用`edit_company_info`保存基本信息。
4. **查询实际数据**：优先用 MCP 查询工具拿真实 ID（`list_page`、`get_page_info`、`get_news_list`、`get_product_list`、`list_news_class`、`list_product_class`、`list_custom_form` 等）。修改已有 AI 页前必须 `get_page_info` 读取 `SourceCode`，不得盲目覆盖。
5. **选最小合适的数据能力**：公司信息用 `DataTag.sys`，后台业务数据用 `DataTag.custom`，系统内容用 `FnGet*` 函数（详见 `advanced-data-interface.md`）。
6. **需要表单** → 优先系统动态表单：`list_custom_form` 列出 → 用户选择 → `FnGetCustomForm(表单ID)` 生成（必读 `customform-democode-base.md`）。
7. **新增文章/产品前**：先查目标分类；需素材先 `upload_file` / `upload_product_image` 再使用返回 URL/文件名。
8. **输出完整可粘贴代码**：HTML/CSS/JS/模板；CSS 用清晰且唯一的类名前缀，避免影响既有页面。
9. **输出前自检**：逐项核对本文件约束（尤其模板约束与写操作确认）。
10. **保存前**：用 `list_page` 拉最新列表，判断新建还是更新，让用户决定；新建或修改系统动态表单时，按 §10 的规则确认表单方案和影响。
11. **收尾**：任务结束主动询问是否上线；涉及首页主动询问是否通过 MCP 设为首页。

## 3. MCP 工具速查

完整参数、返回值、限制与「推荐调用顺序」见 `references/mcp-tools.md`。

**查询类（认证后可直接调用）**：`test`、`list_page`、`get_page_info`、`get_news_info`、`get_news_list`、`get_product_info`、`get_product_list`、`get_online_query_list`、`get_enquiry_form_id`、`list_sqlite_db`、`list_sqlite_tables`、`get_sqlite_table_info`、`query_sqlite`、`list_news_class`、`list_product_class`、`list_custom_form`。

**写入/高风险类（必须先确认目标与影响）**：`save_ai_page`、`save_ai_page_batch`、`del_page`、`set_home_page`、`set_page_friendlyurl`、`add_news`、`add_news_class`、`edit_news`、`add_product`、`add_product_class`、`edit_product`、`add_custom_form`、`edit_custom_form`、`upload_file`、`upload_product_image`、`create_sqlite_db`、`upload_sqlite_db`、`execute_sqlite`、`clear_site_cache`。

> 注意：`save_ai_page_batch` 中途失败前已写入的文件/页面不会自动回滚，确认时必须提示用户。

## 4. 结构化数据（JSON-LD）

用 `application/ld+json` 注入；数据必须来自真实渲染内容或数据源，不得编造价格/评分/库存/日期/作者。结构化数据的是URL地址，图片资源等必须是完整URL；动态内容用 Twig 变量注入并注意转义，输出后复查 JSON 合法性与 schema.org 键名。

| 页面类型 | 类型 |
| --- | --- |
| 产品详情 | `Product` |
| 文章/新闻 | `Article` / `NewsArticle` / `BlogPosting` |
| 公司信息 | `Organization` / `LocalBusiness` |
| 常见问答 | `FAQPage` |
| 面包屑 | `BreadcrumbList` |

**产品特殊约定**：本站产品 JSON-LD 为非商品类，不生成 `offers`/`price`/库存等交易字段；但为满足 Google 要求必须提供 `aggregateRating`：`ratingValue` ，`reviewCount` 按真实情况取值。该评分仅作结构化补充字段，不得显示为站内虚假评分、销售数据或评价列表。

## 5. 新建网站规划

新建网站前，主动询问：企业名称、产品/服务、核心受众、网站语言、参考网站，并询问用户需要构建哪些页面。据此规划整体框架与信息架构。常见页面（首页/关于我们/产品中心/产品详情/新闻资讯/新闻详情/联系我们/产品询盘/常见问题）的组成与编写规范见 `references/website-common-pages.md`。要点：列表项主元素（图片/标题）应链接详情页；详情页输出结构化数据；联系我们页表单 ID 与产品询盘表单 ID 不能相同。

## 6. 如何制作和使用公共页头页尾

当一个网站有多个页面，并且这些页面的头部和尾部一样时，如果每个页面都单独编写页头页尾，维护和修改都会比较麻烦，此时应该制作和使用公共页头页尾，制作流程如下：
第一步：先规划页面内容，将公共的页头和页尾部的所有资源(包括但不限于html标签、css样式、JS脚本、图片等)抽取出来，注意页头和页尾不应该含有 "<html>","<head>","<body>"等壳标签。
第二步：通过 MCP 工具 `save_ai_page` 保存页头和页尾，页头的name固定为 common_top，urlPath固定为 common_top.html，页尾的name固定为 common_foot，urlPath固定为 common_foot.html。
第三步：保存后获取页面的信息的 codePath 属性，使用 {{FnInclude($codePath),'包含备注'}} 分别嵌入公共页头或公共页尾，注意要在合适的位置插入嵌入代码，而不是无脑的插入在页面HTML代码的最开头或最后面。

### 关键约束（易踩坑）

- **公共头尾片段必须「自包含」，不能依赖其它片段或宿主页**：`common_top` / `common_foot` 各自要**自带 `<style>`（该组件的全部样式 + 完整 `@media` 断点）+ 交互 `<script>`**，这样任何页面只要 `{{FnInclude}}` 引用就能独立正确渲染，**无需再额外引入公共 CSS 片段，也不依赖使用页自身 `<head>` 有没有 CSS**。`<style>` 放在 `<body>` 内是合法的 HTML5 写法，浏览器对媒体查询（响应式）同样生效，不存在「body 内 style 导致响应式失效」的问题。
- **响应式断点要完整**：每个片段自带的 `<style>` 必须包含该组件需要的全部 `@media` 断点。

### 公共内容扩展

其它情况需要嵌入公共内容的场景，也可参考公共页头页尾的方法制作和嵌入，注意`save_ai_page`时name的值要根据内容的相关性而定，通常用 common_XXX 之类。

## 7. 内容与资源管理要点

- **文章**：`list_news_class` 查分类 → `add_news`（默认 `status=1` 立即发布；用户未明确要求发布用 `status=0` 草稿，可用 `descriptor` 写入摘要）。缩略图先 `upload_file` 取相对URL作 `previewImage`（不需要域名部分）。改前 `get_news_info` 再 `edit_news` 部分更新（至少提交一个实际字段）。
- **产品**：`list_product_class` 查分类；主图先 `upload_product_image` 取 `fileName`/`SmallFileName` 原样传入 `add_product.mainImage`。`add_product` 立即发布，不支持 SKU/规格/高级字段。改前 `get_product_info` 再 `edit_product`：`mainImage` 省略=保留原图，`null`/空对象=清空。
- **上传**：`upload_file` / `upload_product_image` 每次仅提供一种来源（Base64 或远程 URL）；`upload_product_image` 不会自动绑定产品。
- **清缓存**：`clear_site_cache` 前说明并获确认。
- **离线模式**：MCP 不可用/未授权或用户暂不提供凭据时，说明无法在线操作；仅用户接受离线模式才生成代码。

### 详情页 TDK 规范

产品/文章详情页的 TDK 要与数据相关：

- 所有详情页都应该有TDK(<title>标签、meta description、meta keywords)，不能漏写。
- 产品详情 `title` = `SeoTitle` + 网站名称（`SeoTitle` 为空用产品名称）。
- 产品详情 `description` = `SeoDesc`（`SeoDesc` 为空用 `ProDesc`）；`keywords` = `ProKeyword`。
- 新闻详情 `title` = `Title` + 网站名称。
- 新闻详情 `description` = `ArtDesc`（`ArtDesc` 为空用 `Descriptor`）；`keywords` = `ArtKeyword`。

## 8. SQLite 数据管理

仅用于扩展系统没有的功能；系统已有功能（页面/产品/文章/表单/在线查询）优先用系统功能。开发新功能先问用户是否采用 SQLite。仅作用于当前站点；库名 `^[A-Za-z0-9_]+\.(db|sqlite)$`；数据量 < 5000 行。`query_sqlite` 仅 `SELECT`/`WITH`/`PRAGMA`/`EXPLAIN`，用 `nameParams` 传值，≤1000 行；`execute_sqlite` 为非查询 SQL，删表/删数据/改结构前先查结构并确认。建/传库前先 `list_sqlite_db` 查重。

## 9. 搬站 / 参考站建设

仅处理用户有权使用的公开内容；不采集登录后内容、用户数据、支付流程、追踪脚本、第三方密钥或敏感信息。

1. 确认源站地址、目标站点、迁移范围（页面/产品/文章/图片/文件/表单）与视觉参考程度。
2. 准备目标 MCP 地址+Token，调 `test`；切换目标站点必须重新索取。
3. 采集源站公开信息，按页面/产品/文章/分类/图片/表单分类整理；不直接复制后台代码或提交接口。
4. 迁移前 `list_news_class` / `list_product_class` 映射分类，缺失经确认再建。
5. 素材先 `upload_file` / `upload_product_image` 到目标站（产品主图用返回的 `fileName`+`SmallFileName`）。
6. 内容入库：`add_news`（保留原 HTML/分类/作者/SEO；未要求发布用 `status=0`）、`add_product`（立即发布，须确认）。
7. 按源站结构/视觉生成目标页源码，优先用已入库数据，不在页面硬编码可由系统动态获取的业务内容。
8. 信息收集需求优先接系统动态表单：`list_custom_form` → 用户选 → `FnGetCustomForm`。
9. 保存前展示名称/友好 URL/覆盖/是否首页/涉及表单；单页 `save_ai_page`，多页 `save_ai_page_batch`。
10. 保存后核对返回 ID/URL；必要时经确认 `clear_site_cache`；不符先读再改，不盲目覆盖。

## 10. 自定义表单

创建/修改表单前**必须**读 `references/customform-democode-base.md`。当任务需收集姓名/电话/邮箱/留言/预约/报名/询价/文件等用户输入时判定需要表单，优先系统动态表单，不写独立静态表单或自设计提交接口。

- 先连 MCP 并 `test`，再 `list_custom_form` 取已有普通表单；在线询盘优先 `get_enquiry_form_id`（首次可能自动初始化默认表单与字段，调用前说明副作用并取得同意）。
- 向用户展示表单 `ID`+`Name`，用户选定后才 `FnGetCustomForm(表单ID)` 生成；不得猜 ID 或绑任意表单。
- 无可用表单时告知用户先在后台建；除非用户明确要求，不降级为静态。
- 用户明确要求新建或修改普通自定义表单时，写入前取得确认，再使用 `add_custom_form` 或 `edit_custom_form`；完整参数、字段类型、临时字段 ID、计算/联动和删除语义见 `references/mcp-tools.md`。
- `add_custom_form` 只创建 `FormType=CustomForm`；`edit_custom_form` 可修改已有 `FormType=CustomForm` 普通自定义表单或 `FormType=EnquiryForm` 询盘表单，不能修改其他特殊表单。询盘表单 ID 先用 `get_enquiry_form_id` 获取，修改前确认其页面引用影响。
- 表单和字段写入失败时可能已完成部分写入，不承诺自动回滚；失败后重新查询确认实际状态。
- 以基础代码为起点，仅改样式/真实表单 ID/字段展示结构；保留隐藏提交字段、`action`、`enctype`、字段元数据、校验脚本、AJAX 提交、文件上传、短信/邮箱验证、图形验证码、省市区三级联动。不得用简化版替换校验/提交逻辑。
- 邮箱字段仅在 `ValidateType=6` 且 `IsEmailValidate=1` 时显示邮箱验证码控件；验证码名为 `col{{ field.ID }}_vcode`，发送时调用邮箱验证码接口，不得复用短信接口。字段属性与实现细节见 `advanced-data-interface.md`。
- 字段类型用文档规定控件（单行/多行/单选/下拉/多选/图片/文件/多图上传/地区/日期时间/静态文本）；FieldType 13（公司名）、14（姓名）、15（邮箱）属于单行文本类，控件、必填和格式校验按单行文本处理；上传字段保留 `col{{ field.ID }}` 隐藏字段与原上传接口。
- 联系我们页表单 ID 与产品询盘表单 ID（`get_enquiry_form_id` 返回唯一值）不能是同一个。
- 自定义表单中的验证码图片渲染样式要符合页面本身的整体风格，如：包括但不限于设置合理的大小等。

### 产品询盘扩展

产品详情/列表需询盘时接产品询盘页（自定义表单业务扩展），完整规则见 `references/product-enquiry.md` 与 `product-enquiry-democode.md`。核心前置：

1. 必须 `get_enquiry_form_id` 获取当前站点专属询盘表单 ID，不硬编码或占位。
2. 提交完整沿用 `customform-democode-base.md` 的 AJAX 提交、字段校验、文件上传、防重复提交逻辑，不简化或重写。
3. 固定参数 `EnquiryProduct` 为业务级必填字段，提交前完成非空校验及结构合法性校验。
4. 全站询盘入口遵循统一 URL 参数契约与打开方式联动规则（页头页尾、返回/关闭行为）。

## 11. GEO（生成式引擎优化）约定

生成任何网页前，AI 必须先判定页面类型，再加载对应规则组。

### 11.1 通用规则（所有页面）

- 标题层级：H1 页面唯一 → H2 章节 → H3 子节，禁止跳级
- 关键信息（实体名、核心结论、重要数据）用 `**加粗**`
- 实体名词首次出现标注全称，如：GEO（生成式引擎优化）
- 图片必须含 `alt` 属性，描述内容而非文件名
- 每页包含 JSON-LD 结构化数据，类型按页面匹配
- JSON-LD 结构化数据的资源地址(如网址，Logo地址，图片地址等)必须是完整URL
- JSON-LD 结构化数据中的企业信息，如公司名、邮箱地址、电话、地址等，要使用系统数据源 `DataTag.sys` 进行获取
- 产品/文章详情页的JSON-LD 结构化数据要直接输出产品或文章数据返回的 `JsonLD` 字段即可， `JsonLD` 已包含<script>标签
- 时间敏感信息标注具体年份
- 用具体数字/条件替代"可能""大概"等模糊表述
- `meta description` 一句话概括页面核心内容，≤160 字

### 11.2 首页 / 关于我们 / 品牌展示页 / 团队介绍

目标：让 AI 构建品牌知识图谱，回答"XX 公司是什么、靠不靠谱"。

- 首屏或开头一句话定位："【品牌名】是做什么的，服务谁，核心优势"
- 品牌实体完整呈现：公司名、成立时间、所在地、核心业务、关键数据
- 信任信号（荣誉/资质/客户/媒体）用列表或表格呈现，每条自包含
- `<section>` 模块划分：我们是谁 / 我们做什么 / 为什么选我们 / 发展历程
- 发展历程用有序列表，每条标注具体年份
- JSON-LD 类型：`Organization`，含 `name`、`url`、`logo`、`description`、`sameAs`
- 导航链接允许品牌导航，但 CTA 使用描述性文本

## 12. 主要场景示例索引（引用 references 文档）

> 主文件不内嵌示例代码，避免与 `references/` 文档内容重复、产生口径分歧。下方索引列出每个主场景对应的 `references/` 文档与小节，**执行具体场景时先按本表定位到对应文档**读懂完整参数、字段与 JS 逻辑，再落地页面。所有表单 / 在线查询的校验与提交 JS 一律以对应 reference 文档为唯一权威来源，禁止凭记忆简化或重写。

| 场景 | 完整示例文档（参数/字段/JS 全集） |
| --- | --- |
| 产品列表页 | `references/advanced-data-interface.md` §三.2 |
| 产品详情页 | `references/advanced-data-interface.md` §三.3 |
| 文章/新闻列表页 | `references/advanced-data-interface.md` §四.2 |
| 文章/新闻详情页 | `references/advanced-data-interface.md` §四.3 |
| 菜单 / 公共页头页尾 | `references/advanced-data-interface.md` §二、本文件 §6 |
| 自定义表单页 | `references/customform-democode-base.md`（必读，含不可删的校验/提交 JS） |
| 产品询盘页 | `references/product-enquiry.md` + `references/product-enquiry-democode.md` |
| 在线查询页 | `references/online_query_democode.html` |
| 下载 / 相册 / 门店 / 栏目 / FAQ | `references/advanced-data-interface.md` 各对应小节 |
| 新建整站常见页面 | `references/website-common-pages.md`、本文件 §5 |
