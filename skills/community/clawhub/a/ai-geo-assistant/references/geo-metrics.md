# GEO 各维度判定标准（geo-metrics）

本文件供 `scripts/geo_audit.py` 与 Agent 在落地优化时逐项核对。GEO（Generative Engine Optimization，生成式引擎优化）的目标是让内容在 ChatGPT / Perplexity / Claude / Gemini / 各搜索引擎 AI 摘要中被**准确识别、引用与复述**。

判定信号分两类：**脚本自动可检测**（在 `geo_report.json` 的 `analysis` 中）与**需人工确认**（脚本给出提示，Agent 落地前核实）。

> **评分口径说明**：最终 **GEO Score（0–100）由十维度扣分制**产出（详见 `geo-scoring.md`）：`crawlability(12) / metadata(12) / readability(12) / trust(8) / freshness(8) / entity(10) / discoverability(8) / answerability(12) / citation(8) / content(10)`。下方 1–13 项是**分析诊断层**的细节维度（供定位缺口与生成建议），其结论最终映射到上述十维度扣分。例如 `products`/`services`/`structured_data` 的缺失主要映射到 `metadata`；`credibility`/`faq`/`citations` 映射到 `trust`/`answerability`/`citation`；`enterprise`/`brand` 映射到 `entity`。

---

## 1. 企业实体识别（enterprise）
判定依据：
- 版权行 `© 年份 + 公司名` 是否出现全称（含「有限公司/集团/股份」等后缀）。
- 中文公司名正则（`X+公司/集团/股份`）、英文（`Inc./Ltd./LLC/...`）命中。
- Organization / Corporation / LocalBusiness schema 的 `name`。
- ICP 备案号（`京ICP备…号`）是否出现。
- 是否提供注册地址/成立日期/法定代表人/统一社会信用代码等工商信息。
- 是否有「关于我们 / 公司简介」页面或区块。

清晰度分级：`clear`（名称明确且有关于页） / `partial`（仅识别到名称） / `missing`。

## 2. 品牌识别（brand）
判定依据：
- `og:site_name` / `og:title` 是否给出明确品牌名。
- `<title>` 是否含品牌前缀。
- 是否提供带 `alt`/`title` 的 Logo（img src 含 logo 关键词）。
- 是否使用 ® / ™ 商标符号强化品牌信号。

清晰度分级同企业实体。

## 3. 产品实体识别（products）
判定依据：
- Product / Offer / ItemList schema 是否出现。
- 标题/正文中是否含产品关键词（产品/型号/规格/SKU/系列）。
- 是否出现价格信号（`¥ / ￥ / RMB / $ / 元 / USD`）。
- 是否给出产品名、图片、参数、描述。

## 4. 服务实体识别（services）
判定依据：
- Service schema 是否出现。
- 正文是否含服务关键词（服务/咨询/解决方案/维护/运维/培训/托管/定制）。
- 是否以「服务」为小标题组织内容。

## 5. 行业识别（industry）
判定依据：对 12 个中文行业词库（制造/软件IT/电商零售/教育培训/医疗健康/金融保险/法律咨询/建筑地产/餐饮食品/旅游酒店/能源环保/文创传媒）做词频统计，取 Top 行业作为站点行业归属。用于后续知识覆盖与查询生成的语境。

## 6. 目标市场识别（target_market）
判定依据：
- `<html lang>` 与 `content-language` 元信息。
- 区域词命中（中国/全球/北美/欧洲/东南亚）。
- 币种符号（¥/￥/$/€）与币种词（人民币/美元/欧元）。
- 是否提供配送/物流/海外仓等跨境信息。

## 7. 竞争对手分析（competitors）
判定依据：
- 外链域名统计（Top 10 外部域名）。
- 正文中是否出现竞品提及（「竞争对手/竞品/对比/vs/versus」后接名称）。
- 友链 / 合作伙伴域名。
> 注：本技能默认只做「被动发现」，不主动爬取竞站；如需竞站对比，须用户提供竞站 URL 并单独 `analyze`。

## 8. 问题 / 搜索意图分析（intent）
判定依据：
- 从正文抽取问句式内容（中/英问号 + 疑问词），去重后得到 `questions`。
- 对全文做意图分类（transactional / commercial / navigational / informational）并统计分布。
- 由 H1/H2 生成候选查询（candidate_queries），供内容优化与 FAQ 构建参考。

## 9. 知识覆盖度分析（knowledge_coverage）
对照 GEO 话题清单（11 项）逐条核对站点是否覆盖：
公司简介/关于我们、产品、服务、价格/报价、联系方式、案例/客户、资质认证、常见问题FAQ、博客/资讯、团队/招聘、政策/隐私。
输出 `covered` / `missing` 与 `coverage_ratio`。缺失项即内容建设重点。

## 10. 内容可信度分析（credibility）
7 项信号，命中数 / 7 × 100 为 `score`：
- 作者署名（meta author / article:author / 「作者/编辑/撰稿」）。
- 发布/更新日期（datePublished/dateModified/发布时间/YYYY-MM-DD）。
- 参考文献/资料来源区块。
- 联系方式（联系我们/电话/邮箱/地址）。
- 隐私政策/条款。
- 版权标识（© / 版权）。
- 外链数量与权威外链（.edu/.gov/wikipedia/doi）计数。

## 11. 结构化数据分析（structured_data）
- 解析页面 JSON-LD，统计已出现的 `@type`。
- 检测 microdata / RDFa 痕迹（`itemscope`/`itemtype`/`vocab="http://schema.org"`/`property="x:y"`）。
- 推荐必备 schema 集合：Organization、WebSite（含 SearchAction）、FAQPage、（有产品时）Product、（有服务时）Service、BreadcrumbList、Article。
- 输出 `present` / `missing` 与 `coverage_ratio`。

### 11.1 产品 / 新闻详情页 JSON-LD 落地约定
详情页的结构化数据是最易被生成式引擎直接引用的部分，落地遵循以下约定：

- **Schema 类型匹配页面类型**：产品详情页 → `Product`；新闻/文章详情页 → `Article` / `NewsArticle` / `BlogPosting`，一一对应，不跨页混用。
- **直接复用平台返回的 `JsonLD` 字段**：云指建站的产品/文章数据已自带 `JsonLD` 结构化字段，**且该字段已包含 `<script>` 标签**。详情页应直接输出该字段，避免手写重复 schema 造成字段不一致。
  - 模板内写法（平台返回的 `JsonLD` 已是合法 `<script>` 块，按平台约定用 `|raw` 输出）：`{{ product.JsonLD | raw }}` / `{{ article.JsonLD | raw }}`。
- **绝对地址**：JSON-LD 中的网址、Logo、图片地址必须是完整 URL（用 `FnGetHost(1)` 拼接或 `FnGetCurrentUrl()`，**禁止写死域名**）；动态内容用模板变量注入并转义，输出后复查 JSON 合法性与 schema.org 键名。
- **企业信息走系统数据源**：JSON-LD 中的公司名、邮箱、电话、地址等用 `DataTag.sys` 获取，不硬编码。
- **产品详情页的评分占位（平台合规项）**：本站产品 JSON-LD 为非商品类，不生成 `offers`/`price`/库存等交易字段；但为满足搜索引擎结构化要求，平台约定提供 `aggregateRating`（`ratingValue` ，`reviewCount` 按真实情况取值）。该评分**仅作结构化补充字段，严禁作为站内可见的虚假评分、销量或评价列表展示**。
- **与 GEO 红线并行**：上述字段中的名称、价格、评分、库存、作者、日期仍须来自真实数据或数据源；模拟评分仅限占位、不向用户展示、不写入正文。本约定与 geo-metrics.md 的全局红线（不得编造）不冲突。

## 12. FAQ 分析（faq）
- 是否存在 FAQPage schema 及问答对数（`schema_pairs`）。
- 页面内问句式内容数量（`onpage_question_count`）。
- 生成式引擎极依赖 FAQ 直接引用，缺 FAQPage 是高频短板。

## 13. Citation / Reference 分析（citations）
- 外链总数、权威外链数及比例（authoritative_ratio）。
- 描述性锚文本占比（避免「点击这里/更多」）。
- 是否存在「参考文献/资料来源」区块。
> GEO 强调「被引用」——内容本身要成为可被引用的信源，同时合理引用权威信源提升自身可信度。

---

## 自动检测 vs 人工确认对照
| 维度 | 自动检测 | 需人工确认 |
| --- | --- | --- |
| enterprise | 名称/ICP/关于页存在 | 工商信息真实性、法律主体一致性 |
| brand | 品牌名/Logo/商标 | 品牌名与工商名是否一致 |
| products | schema/价格/关键词 | 价格/库存/参数真实性 |
| services | schema/关键词 | 服务范围边界 |
| industry | 词频 Top | 行业归类是否贴合业务 |
| target_market | lang/区域/币种 | 实际目标市场策略 |
| competitors | 外链/提及 | 竞品名单准确性 |
| intent | 问句/意图分布 | 真实搜索词与商业意图 |
| knowledge_coverage | 话题命中 | 缺失项优先级 |
| credibility | 信号计数 | 作者资质、引用来源真实性 |
| structured_data | 类型解析 | schema 字段真实性 |
| faq | 问答对数 | 答案准确性 |
| citations | 外链/权威比 | 引用来源是否恰当 |

**红线**：结构化数据中的名称、价格、评分、库存、作者、日期必须来自真实数据或数据源，**不得编造**。
