# 字段决策与本地检查范围

脚本围绕交付可用性定义一个保守的本地规则集。Schema.org 本身不是一份所有类型共用的必填表；Google 的资格要求另行核验。脚本不下载上下文、展开别名、读取网页或调用 Google。

## Agent 如何整理输入

| 资料中出现的事实 | 草稿属性 | 缺失时的处理 |
| --- | --- | --- |
| 公司/品牌名称和已确认官网 | Organization 的 name、url | 缺 name 暂不完成该实体；未知 url 不推断 |
| 正文里的完整问题与对应答案 | FAQPage → mainEntity → Question → acceptedAnswer → Answer.text | 缺答案的条目单列为未完成；不编答案 |
| 文章标题、真实作者、实际发布日期 | Article/BlogPosting 的 headline、author、datePublished | headline 必需；作者/日期未知省略并提示 |
| 实际可购买价格与币种 | Product.offers 的 Offer.price、priceCurrency | 无价格不创建 Offer；免费 0 需要明确事实 |
| 真实评分、量表和评价/评分数量 | AggregateRating 的 ratingValue、bestRating/worstRating、reviewCount/ratingCount | 缺评分或数量不创建 AggregateRating |
| 已知图片文件的公开 URL | ImageObject 的 url/contentUrl，或适用属性的 URL | 不推断 Logo 路径、图片尺寸或版权归属 |

保持数值含义：`99/月` 不能直接当数字价格；需确认币种及计费周期如何表达，不能隐去周期而改变事实。仅知道年份时不要为凑 `YYYY-MM-DD` 添加月份和日期。本地规则不接受仅年格式，可省略日期并在交接中保留已知年份事实。

普通用户资料未必已用 Schema 属性命名。由 Agent 映射并说明取舍，脚本的 build 输入是整理后的草稿，不是任意公司 JSON 的自动理解器。多个页面分别整理；本地批量转换保留上游逐页交付的用途，不自动猜页面类型。

## 实际规则

| 类型 | 本地必需字段/条件 | 补充检查 |
| --- | --- | --- |
| Organization | name | url 若提供需为绝对 HTTP(S) URL；logo 可省略 |
| WebSite | name、url | 不默认创建搜索动作 |
| Article / BlogPosting | headline | 缺 author/datePublished 仅警告；提供 author 时需 Person/Organization 或引用 |
| FAQPage | 非空 mainEntity 数组 | 每项 Question 或可解析的引用 |
| Question | name、acceptedAnswer | acceptedAnswer 为单个 Answer 或引用，本地规则不接受答案数组 |
| Answer | 去除 HTML 后仍有文字的非空 text | 纯标签、空白实体、图片或 script/style/template 内容不构成答案文字；无正文快照也执行此检查，保留原始 JSON 字符串 |
| Product | name | 不强制 Offer 或评分；存在 offers 时仅覆盖 Offer 对象/数组或引用 |
| Offer | price、priceCurrency | 有限非负数字/数字字符串；币种为三个大写字母，未核实币种代码成员资格 |
| AggregateRating | ratingValue，且有 ratingCount/reviewCount 至少一个 | 数量为正整数；评分在量表内，未给量表时按 Schema.org 1–5 默认范围检查，不写回默认值 |
| LocalBusiness | name、address | address 为非空字符串或 PostalAddress/引用 |
| HowTo | name、step | step 为 HowToStep 或其数组/引用 |
| HowToStep | text | 不强制捏造步骤名称 |
| BreadcrumbList | 非空 itemListElement 数组 | ListItem 或文档内引用，解析后按数组顺序检查 position 为从 1 起连续的 JSON 整数；定义可在引用之后 |
| ListItem | position、name | position 为正 JSON 整数 |
| VideoObject | name | 上传日期若提供需可解析；不宣称满足视频富结果资格 |
| ImageObject | url 或 contentUrl 至少一个 | 地址格式检查，不查询尺寸或可访问性 |
| Person / Brand | name | 用真实身份，不由站点名称猜作者 |
| PostalAddress / ContactPoint / WebPage | 无额外本地必填 | 仍执行通用空值、已知日期和 URL 格式检查 |

其他类型保留输入并警告 `type_not_covered`。例如 AggregateOffer 有独立语义，当前 offers 关系规则不覆盖它；不要改成 Offer 来绕过检查。可以保留原始标记交给完整 Schema.org 工具核验，并明确本地未通过的原因。

## 结构与内容边界

- check 接受对象、非空对象数组、带非空数组的 `@graph`；嵌套继承上下文，数组每个根对象须有上下文。build 只补缺失的根级上下文。
- 字符串上下文支持 `https://schema.org`（可带结尾斜线），兼容 HTTP 并警告。对象上下文仅接受 `{"@vocab":"https://schema.org/"}`：`@vocab` 的末尾斜线不可省略，否则拼接类型与属性名称会形成错误 IRI。其他上下文、别名及 `@list/@reverse/@value` 等高级关键字明确失败，交给完整 JSON-LD 工具处理。
- `@type` 可为非空字符串或非空字符串数组。嵌套实体按已知类型递归检查；未识别属性不进行 Schema.org 词表或值域的全面校验。
- `@id` 为绝对 HTTP(S) URL 或非空 `#fragment`；文档内按原字符串解析引用，不做基址展开。`#organization` 和完整 URL 是不同标识，不混写。每个 ID 只定义一次，用仅含 `@id` 的对象引用。未定义 fragment 报错；文档外绝对 ID 给出未采集警告。
- 输入不允许重复 JSON 键、NaN/Infinity、null 或空的属性值；数组及任意深度的嵌套数组也逐项检查 null、空串、纯空白、空对象和空数组，错误路径定位到具体元素。数值 `0` 与布尔值 `false` 不作为空值。JSON 根结构错误、FAQ 错形、错误日期、价格/评分错误都会返回结构化错误，不输出“通过”。
- 日期支持真实日历 `YYYY-MM-DD` 或带秒的 ISO 日期时间；URL 只检查绝对 HTTP(S) 格式，不验证可达性、所有权或 canonical。
- 正文参数必须是已提取的 UTF-8 纯文本快照；工具不会替用户判断浏览器可见性。文字匹配规范化 Unicode NFKC 和空白，Answer.text 先去 HTML 标签。缺文字报 `content_not_found`；答案在对应问题之前或跨过下一条已标记问题报 `faq_pair_mismatch`。不同排版或合法改写也可能不匹配，应核对原文与排版后解释原因，不把本地匹配当事实认证。
- FAQ 配对检查仅以本次标记的独立完整问题作为边界，并将每处出现位置绑定到对应题名。同一正文中的全部 FAQPage 共用这些边界，包括分布在 `@graph` 或顶层数组中的节点。短题不能借用长题内部子串；问题首尾若与相邻字母、数字或汉字直接相连，不视为独立题目。完整匹配的答案内部，用成对引号复述的问题不作为新题目，例如 `关于‘如何退款？’，请联系支持。`。带引号的独立题目仍保留边界，未加引号的重复题目仍会切断跨题答案。这是文字规则，无法证明未标记的内容、所有页面区块或其他平台的内容一致。价格、评分、日期、URL、法律名称等仍由 Agent 对照原始资料复核。

## CLI 契约

```text
python3 scripts/schema_tool.py build INPUT --output-dir DIR [--visible-text TEXT]
python3 scripts/schema_tool.py check INPUT [--visible-text TEXT] [--report FILE]
python3 scripts/schema_tool.py batch INPUT_DIR --output-dir DIR
```

build/batch 的输出目录须新建或为空；不同运行使用不同目录，防止旧的成功文件混入失败交付。check 的 `--report` 明确写入所指定文件，不能指向任何输入文件。stdout 始终是报告或批量摘要 JSON（帮助与参数错误除外）。脚本不提供网站抓取、交互问答或任意自定义生成参数。

退出码：`0` 为本地通过（可带警告），`1` 为内容/结构/输入读取检查失败或批量中至少一页失败，`2` 为参数、输出目录或报告写入等操作错误。不存在或不可解析的输入会标记 `input_error`；没有正文时为 `not_run`，有正文但不匹配为 `mismatch`，无待检查文字为 `no_text_fields`，文字和可检查 FAQ 配对通过为 `matched`。

Google 结果固定为未运行，除非另有真实外部测试证据；脚本不会将其改为通过。AI 引用检测不在此 CLI 范围。外部模拟、未运行与查询失败均不能变成“零引用”或“已收录”。
