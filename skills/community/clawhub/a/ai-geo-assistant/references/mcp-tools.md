# CMS MCP 写回映射（mcp-tools）

本技能在「目标站为支持 MCP 的 CMS 且需执行修改」时，经 MCP 回写 GEO 优化内容。MCP 地址与 Bearer Token 由用户提供（写入用户级 `~/.workbuddy/mcp.json` 的 `mcpServers.<name>.url` 与 `mcpServers.<name>.headers.Authorization`，或由会话提供的 MCP 服务注入）。

## 向用户索取 MCP 地址与访问 Token（必读，写操作前必做）

> 只有当用户**预期执行修改**（JSON-LD/FAQ/E-E-A-T/引用区块回写）时才需要。若用户只需「只读体检 + 出方案」，不必索取 Token，直接走离线 `analyze` 即可。

### 何时询问
- 用户明确要求「帮我改页面」「把 FAQ 落地」「写回 schema」「推送线上」等写操作时；
- 体检报告已出、进入「生成优化方案 → 自动优化 → 验证」阶段且涉及 CMS 回写时。

### 必须收集的两项信息
1. **MCP 完整地址（endpoint URL）**：形如 `https://xxx.com/mcp/<站点ID>` 或托管方提供的完整 MCP 后端地址。用于 JSON-RPC 调用的 `POST` 目标。
2. **访问 Token（Bearer Token）**：形如 `mcp_010477b03f...` 的鉴权令牌，放在请求头 `Authorization: Bearer <token>`。

### 可直接套用的询问话术（复制给用户）
```
请提供目标站的 MCP 配置，我再执行写回：
1. MCP 完整地址（endpoint URL）：https://xxxx/mcp/站点ID
2. 访问 Token（Bearer Token）：mcp_xxxxxxxx...
仅用于本次 GEO 回写，Token 不会回显、不会写入报告文件，仅由 MCP 客户端放入 Authorization 头。
拿到后我会先调用 test 工具验证连通性，确认服务可达、鉴权通过后再操作。
```

### 拿到后如何处理
1. **写入配置（单一数据源）**：把地址写入 `mcp.json` 的 `mcpServers.<name>.url`，Token 写入 `mcpServers.<name>.headers.Authorization`（`Authorization: Bearer <token>`）。若宿主已托管该 MCP 服务，则直接复用会话内已连接的同名服务，无需重复索取。
2. **验证连通性（必须，写前第一动作）**：调用 `test` 工具进行连通性检测——
   - **通过**：服务可达、鉴权通过，继续用 `tools/list` 确认 `list_page`、`save_ai_page`、FAQ 工具等可用。
   - **失败**：立即停下，向用户反馈「地址或 Token 无效 / 无权限」，**不得猜测重试或降级到伪造数据**。
3. **确认目标页**：用 `list_page` 拉取页面清单，核对目标页 `pageId`（必要时 `get_page_info` 取源码）。
4. **离线分析优先**：取 `SourceCode` 存为本地 `页面.html`，先跑 `analyze --file` 得到基线报告，再决定写回内容。

### 安全红线
- Token 仅由 MCP 客户端放入 `Authorization: Bearer`，**不回显、不落文件（除 `mcp.json` 受信位置外）、不出现在任何报告/日志/截图**。
- 未拿到 Token 前，**只做只读分析，不调用任何写工具**（`save_ai_page` / FAQ 写入工具等）。
- 直连后端脚本（见文末）从 `mcp.json` 读 Token，保持单一数据源；仅可信本地环境使用。

## 前置要求（写操作前必做）
1. 已按上文「向用户索取 MCP 地址与访问 Token」完成索取、写入与连通性验证。
2. 用 `list_page` 拉取页面清单，确认目标页 `pageId`。
3. 用 `get_page_info`（或 `get_page_code` 类工具）取目标页 `SourceCode` 存为本地 `页面.html`，先离线 `analyze --file`。
4. 未拿到 Token 前，**只做只读分析，不调用任何写工具**。Token 仅由 MCP 客户端放入 `Authorization: Bearer`，不回显、不落文件。

## 仅使用的 MCP 工具
- `list_page`：列举站点页面，定位目标页 ID。
- `get_page_info` / 取源码类工具：读取页面源码（离线分析）。
- `save_ai_page`：将 GEO 优化内容（JSON-LD、FAQ 区块、E-E-A-T 区块、meta 标签）写回页面。
- `edit_seo` / `edit_site_seo` / `get_seo_*`：仅用于 TDK 与 SEO 字段微调（GEO 中次要）。
- FAQ 工具组（GEO FAQ 维度站内落地，详见下文「FAQ 工具」）：`list_faq`、`list_faq_class`、`get_faq_info`、`add_faq`、`add_faq_class`、`edit_faq`、`edit_faq_class`、`del_faq`、`del_faq_class`。
> 不调用上列以外的其它 MCP 工具。其中 `save_ai_page` 严禁改动 `{{}}`/`{%%}` 数据标签及其上下文逻辑。

## GEO 写回字段 / 操作映射
| GEO 优化项 | 落地方式 | 工具 | 约束 |
| --- | --- | --- | --- |
| Organization / WebSite / BreadcrumbList / Article JSON-LD | 在页面 `</head>` 前追加 `<script type="application/ld+json">` 块 | `save_ai_page` | 标签为新增 GEO 内容，不触碰既有数据标签；字段须真实 |
| 产品 / 新闻详情页 JSON-LD | **直接输出平台数据返回的 `JsonLD` 字段**（已含 `<script>` 标签），如 `{{ product.JsonLD \| raw }}` / `{{ article.JsonLD \| raw }}`；非详情页或不带该字段时再按类型手写 | `save_ai_page` | 详情页优先复用 `JsonLD` 字段避免重复 schema；资源地址须完整 URL、企业信息走 `DataTag.sys`；产品 `aggregateRating` 仅作结构化占位，严禁展示为站内虚假评分（详见 `geo-metrics.md` §11.1） |
| FAQPage schema + 可见问答区 | 追加 FAQ 区块（含 schema 与可读问答） | `save_ai_page` | 答案须为真实权威内容，禁止占位 |
| E-E-A-T 内容（作者/日期/引用/联系方式） | 追加/补全内容区块 | `save_ai_page` | 作者、日期、引用来源须真实 |
| 引用区块（资料来源/参考文献） | 追加 references 区块 + 权威外链 | `save_ai_page` | 链接真实、锚文本描述性 |
| TDK / og 标签微调 | 改 title/description/keywords/og | `edit_seo` 优先；必要时 `save_ai_page` | 仅改 TDK 不得用 `save_ai_page` 大改 |

## FAQ 工具（GEO 关键维度）

FAQ 是 GEO 最高频的「被直接引用」形态：生成式引擎常把 FAQ 内容原样复述进答案。GEO 流水线在「FAQ 分析」阶段（`analyze` 的 `faq` 维度）会抽取页面问句并判定是否存在 FAQPage schema；`optimize` 会基于抽取问句生成 FAQPage JSON-LD 骨架。**但该骨架仅是页面内 schema，若要真正被站点 FAQ 模块与搜索/生成式结果复用，必须把问答落地为站点真实的 FAQ 数据**——即通过下列 FAQ MCP 工具写入，再让页面/区块引用。

> 工具名称、参数与限制以建站 MCP 服务的权威定义为准（参考 `yun-zhi-jian-zhan/references/mcp-tools.md` 的 FAQ 章节）。以下为 GEO 落地所需的要点摘录。

### 查询工具（只读）
| 工具 | 参数（JSON） | 用途 |
| --- | --- | --- |
| `list_faq_class` | 无参数（输入对象必须为空） | 列出全部 FAQ 分类，每项含 `ClassID`/`Name`/`Icon`/`FaqCount`；用于创建/编辑 FAQ 前核对分类 ID |
| `list_faq` | `{"keyword":"", "classId":-1, "isTop":0, "status":1, "page":1, "pageSize":20}` | 分页列出 FAQ；`-1`=全部分类，正整数=指定分类；`status` 0=草稿/1=发布 |
| `get_faq_info` | `{"id": 123}` | 获取单条 FAQ 完整信息（`Question`/`Answer`/`ClassID`/`IsTop`/`Status`/`ShowOrder`/`CrTime`）；编辑前必读 |

### 写入工具
| 工具 | 参数（JSON） | 用途 / 约束 |
| --- | --- | --- |
| `add_faq_class` | `{"name":"售后服务", "icon":""}` | 新增 FAQ 分类；`name` 必填，不可仅空白 |
| `add_faq` | `{"question":"如何联系公司？", "answer":"<p>请通过联系我们页面提交信息。</p>", "classIds":[12], "isTop":0, "status":1, "showOrder":0}` | 新增一条 FAQ；`question`/`answer` 必填（answer 可传 HTML）；`classIds` 为当前站点分类 ID 数组（省略/空=未分类）；`isTop` 0/1；`status` 0=草稿/1=发布（默认 1 立即发布）；`showOrder` 非负整数 |
| `edit_faq` | `{"id":123, "question":"更新后的问题", "answer":"<p>更新后的答案。</p>", "classIds":[], "isTop":0, "status":1, "showOrder":0}` | 部分修改一条 FAQ；`id` 必填，至少提交一个更新字段；未提交字段保持原值 |
| `edit_faq_class` | `{"classId":12, "name":"新的分类名称", "icon":""}` | 部分修改 FAQ 分类；至少提交 `name` 或 `icon` 之一 |

### 删除工具（高风险，永久不可恢复）
| 工具 | 参数（JSON） | 约束 |
| --- | --- | --- |
| `del_faq` | `{"id": 123}` | 物理删除一条 FAQ；`id` 须为当前站点正整数 ID，输入对象不接受额外属性 |
| `del_faq_class` | `{"classId": 12}` | 物理删除一个 FAQ 分类；不影响已有 FAQ 中保存的 `ClassID` 字段 |

### GEO 落地流程（FAQ 维度）
1. **抽取问答**：`analyze` 的 `faq` 维度给出页面问句与 FAQPage 缺失项；`optimize` 给出 FAQPage JSON-LD 骨架（含 `【】` 占位答案）。
2. **建分类（按需）**：若尚无合适分类，先 `list_faq_class` 核对，再 `add_faq_class` 创建（如「产品问答」「服务支持」）。
3. **写真实问答**：对每条高价值问句，用 `add_faq` 写入——`question` 用真实问法，`answer` 用真实权威内容（可 HTML），`classIds` 关联上一步分类，`status=1` 前明确告知用户将立即发布（草稿用 `status=0`）。
4. **页面引用（双通道）**：
   - 在目标页 `save_ai_page` 追加 FAQPage JSON-LD，其 `name`/`acceptedAnswer.text` 与站内 FAQ 数据保持一致（不得出现两套答案）。
   - 站点前端 FAQ 模块通过 `FnGet*` 类数据标签渲染（保留平台绑定，不破坏数据流）。
5. **核对与验证**：用 `list_faq` / `get_faq_info` 确认已落地；重跑 `analyze` 确认 `faq` 维度分提升、FAQPage schema 出现；`del_faq`/`del_faq_class` 仅在用户逐条明确确认永久删除时调用。

> 红线：`add_faq`/`edit_faq` 的 `answer` 必须是真实权威内容；`optimize` 产出的占位答案须先补全再写入，禁止把 `【请在此填写该问题的权威答案】` 直接入库。

## 模板函数（CMS 站内绝对地址）
JSON-LD / canonical / og:url 等要求绝对地址时，用动态模板表达式，**禁止写死域名**：
- `{{ FnGetHost(0) }}` → 仅域名（`abc.com`）
- `{{ FnGetHost(1) }}` → 协议+域名（`https://abc.com`）
- `{{ FnGetCurrentUrl() }}` → 当前完整访问 URL

JSON-LD 中的网址、Logo、图片地址必须是完整 URL（优先 `FnGetHost(1)` 拼接或 `FnGetCurrentUrl()`）。

## 直连后端提示
若宿主 `DeferExecuteTool` 的本地 ajv 校验因 `oneOf`/`coerceTypes` 误拦截带 `pageId` 的写工具（如 `save_ai_page`、`del_page`），可改用直连后端脚本（从 `mcp.json` 读 Token，POST JSON-RPC：`initialize` → `notifications/initialized` → `tools/call`）绕过宿主校验。仅在可信本地环境使用，且仍须遵守上述数据标签与真实数据红线。

## 写后验证
回写后：① 在 CMS 预览确认页面正常；② 重新 `analyze`（或 `validate` 对比基线）确认 GEO Score 提升、schema 类型出现、无模板绑定破坏。
