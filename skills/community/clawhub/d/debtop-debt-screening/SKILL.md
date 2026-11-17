---
name: debtop-debt-screening
display_name: 债权标的筛选
display_name_en: Debt Target Screening
description: "债权标的筛选：按行业或标的类型、地区与金额区间，批量检索公开的债权转让 / 处置 / 招商公告，定位「这类债权在哪些人手上」——按出让方（债权人）聚合命中标的数、本金合计与涉及债务人，并输出标的清单与分布。金额区间为「已扫描窗口内」筛选（检索接口不支持金额参数），输出会标注扫描覆盖率与时间窗。当用户说「找煤矿不良，金额 3000 万到 3 亿的债权都在哪些人手上」「某地区某行业的债权有哪些出让方在处置」「按金额区间筛一批债权标的」时使用。免注册免登录，只做公开公告的只读检索与汇总。英文触发词：debt screening, debt target screening, NPL screening by industry, debt sourcing by amount range。若用户只是按关键词列公告清单，改用 debtop-notice-search；若要某家出让方的处置清单，改用 debtop-creditor-disposal；若要按抵押物线索反查债权，改用 debtop-collateral-check。"
description_zh: "债权标的筛选：按行业或标的类型、地区与金额区间，批量检索公开的债权转让 / 处置 / 招商公告，定位「这类债权在哪些人手上」——按出让方（债权人）聚合命中标的数、本金合计与涉及债务人，并输出标的清单与分布。金额区间为「已扫描窗口内」筛选（检索接口不支持金额参数），输出会标注扫描覆盖率与时间窗。当用户说「找煤矿不良，金额 3000 万到 3 亿的债权都在哪些人手上」「某地区某行业的债权有哪些出让方在处置」「按金额区间筛一批债权标的」时使用。免注册免登录，只做公开公告的只读检索与汇总。英文触发词：debt screening, debt target screening, NPL screening by industry, debt sourcing by amount range。若用户只是按关键词列公告清单，改用 debtop-notice-search；若要某家出让方的处置清单，改用 debtop-creditor-disposal；若要按抵押物线索反查债权，改用 debtop-collateral-check。"
description_en: "Screen public debt transfer / disposal / investment-invitation notices by industry or asset type, region and amount range, and answer 'who holds this kind of debt' by aggregating hits per seller (creditor): number of targets, principal total and debtors involved. The amount range is applied within the scanned window only (the search API takes no amount filter), and the result always states scan coverage. Use when the user asks to find coal-mine NPLs between 30 million and 300 million, or which sellers are disposing debts of a given industry in a given region. No sign-up and no configuration needed; read-only search and aggregation of publicly published notices only. For a plain keyword notice list, use debtop-notice-search; for one seller's disposal list, use debtop-creditor-disposal; for reverse lookup by collateral clue, use debtop-collateral-check."
version: 1.0.2
author: 智收云
disable-model-invocation: false
user-invocable: true
---

# 债权标的筛选（游客免登录）

给定**行业 / 标的类型**、**地区**与**金额区间**（三者都可选），批量检索公开公告口径的债权转让 / 处置 / 招商公告，按**出让方（债权人）**聚合，回答「这类债权在谁手上」：命中标的数、本金合计、涉及债务人，并输出标的清单；**每条引用都原样附详情页链接**。

> 产出可能被用户用于寻找资产标的或对外材料，请遵守 §七 的合规与限流要求（**声明非征信、不构成投资建议、出让方不等于当前持有人**）。
> 本 Skill 的端点与令牌**仅授权用于 `agent.debtop.com`**；调用前请确认端点与此一致。

本 Skill 的检索入口是**公告全文检索**——关键词会被同时匹配到标题、主体名与公告披露的抵押物文本，因此**行业词与抵押物词都能搜**；这是它能做「标的筛选」的原因。

## 何时使用

- 用户说「找 XX 行业的不良 / 债权，金额 X 到 Y，都在谁手上」
- 用户说「某地区某类债权有哪些出让方在处置 / 有哪些标的」
- 用户要给一批债权标的做**初筛**（按金额区间、地区、类型收窄），再逐条看详情
- 用户想核实「某类标的在公开公告里的分布」（出让方分布、金额分布、地区分布）

> **与相邻 Skill 的分工**：本 Skill 是**筛选视角**（多关键词 × 多条件 → 聚合分布）；若只是按任意关键词列公告清单，用 `debtop-notice-search`；若以某家出让方为主体列处置清单，用 `debtop-creditor-disposal`；若按抵押物线索（小区 / 地块 / 资产类型）反查债权，用 `debtop-collateral-check`。

## 一、零配置与能力边界

本 Skill **不需要注册、不需要登录、不需要填任何 key、不需要任何配置项**：

| 情形 | 做法 |
|---|---|
| 该 MCP 已连接过（OAuth 授权，或客户端已配置 PAT） | **直接调用工具**，不做任何认证动作 |
| 尚未连接 | 本 Skill 自行以「游客（Guest）」身份取只读令牌（见 §二），用户**直接提问即可** |

游客是**只读**身份、短时效、可限流、可审计：scope 为 `notice:read` + `enterprise:read` + `guest:access`（4 个工具全部可用）；access 30 分钟、refresh 1 天、单游客最长 7 天；调用限流 **1 QPS（相邻调用间隔 ≥1 秒）**、30 次/分、1000 次/天（共享配额）；创建游客另有配额（单 IP 3 次/小时、全局 500 次/天）。完整端点、能力边界与可直接复制执行的 curl 见 `@references/guest-access.md`。

**运行前提**：若该 MCP 已配成客户端连接器（见 §二），用户侧无任何要求；若需要走游客兜底，则要求**运行侧能访问 HTTPS**且可执行 `curl` 与 `bash` / `python3`（无脚本能力时按 `@references/guest-access.md`「运行前提与替代方案」处理）。

## 二、先判断「能不能直接用」（认证判定）

**一句话结论**：**有工具就直接用**（已配置）；**只有 `401` 且客户端不能自动 OAuth 才创建游客**；其余情况（工具级报错 / `429` / 连不上）**一律不要创建游客**。

**第 0 步｜先看手里有没有工具（零成本，先做这一步）**：当前会话能看到这 4 个工具（`search_debt_notice` / `get_debt_notice_detail` / `search_debt_enterprise` / `get_debt_enterprise_debt_summary`）→ **该 MCP 已在客户端配置好**，直接调用（凭据由平台注入）；一个都看不到 → 未配置为连接器，只能自行走 HTTP + 游客通道（见 `@references/guest-access.md`），或引导用户先到平台配置该连接器。

> 客户端是否已配置，**只能**由「工具是否可见」与「探测响应」推断；SKILL 读不到平台的连接器配置，因此不要问用户"你配了吗"，直接按下述步骤探测。

**第 1 步｜探测一次**（仅当第 0 步无法确定时）：调一次 `tools/list`，或一次轻量工具调用（如 `search_debt_notice(keyword=行业词, page_size=5)`）。**不要用「创建游客」来探测**——那会消耗创建配额。

**第 2 步｜按返回判定**：

| 返回 | 判定 | 动作 |
|---|---|---|
| `200` | 已配置且已授权 | 直接干活，**不要再创建游客**；后续沿用同一会话 |
| `401` + `WWW-Authenticate: Bearer resource_metadata=…` | 链路通，但**无凭据或凭据已过期**（两者响应相同，无法区分） | 客户端能自动 OAuth → 交给客户端（用户点一次）；否则走游客。若本机此前已取过游客令牌（缓存仍在），先**刷新**而不是重建——跨会话复用同一份缓存，不要每次对话都重建游客 |
| `200` 但结果里 `isError=true` | **工具级错误（HTTP 仍是 200）**：`INSUFFICIENT_SCOPE` / `GUEST_LIMITED` / `PARAM_INVALID` | scope 不足**不要降级为游客**（游客只读、权限更低）；限流退避 1 秒重试；参数问题改参数重试 |
| `429` | 已触达限流 → 说明链路本来就通 | 退避后重试，**不要**创建游客 |
| 连接失败 / DNS 失败 / 超时 / `404`、`405` 等非 401 的 4xx | 服务不可达或路径不对（属"未接入"） | **不要创建游客**、不要反复重建；如实告知用户该 MCP 未接入或地址有误 |

> 上表只适用**探测 MCP 端点**（`/mcp/debt/stream`）。创建游客与挑战端点的返回另有一套判定（`404 FEATURE_DISABLED`、`401 AUTH_REQUIRED`、`POW_REQUIRED` / `POW_INVALID`），详见 `@references/errors.md`。

## 三、可用工具（4 个，只读）

| 工具 | 用途 | 必填参数 |
|---|---|---|
| `search_debt_notice` | **公告全文检索（本 Skill 主入口）** | `keyword` |
| `get_debt_notice_detail` | 公告详情（抵押物 / 保证人线索） | `notice_id` |
| `search_debt_enterprise` | 企业搜索（辅助：把命中的债务人定位到主体） | `keyword`（**单一**企业名称） |
| `get_debt_enterprise_debt_summary` | 企业债务概要（辅助：按债务人汇总规模） | `enterprise_id` |

四个要点（完整参数、返回字段、条件字段与枚举见 `@references/tools-and-fields.md`）：

- 入参统一 **snake_case**（`page_size` / `notice_id` / `enterprise_id`）；ID 参数整数与字符串都可传；`page_size` 默认 10，**工具接受 1–100，但上游按 20 截断**。
- **`search_debt_notice` 的全部入参只有 `keyword` / `page` / `page_size`**——**没有**金额、地区、公告类型参数。金额与地区只能在取回后本地过滤，且**只能覆盖已扫描到的条目**（见 §四）。
- `search_debt_notice` 的 `keyword` 是**全文**匹配（标题、出让方 / 债务人名、公告披露的抵押物文本都会命中）——因此**行业词、标的类型词、抵押物词、地名都可作关键词**。
- 公告项含 **`area`（公告地区，省级，条件字段，可能缺失）**——区域筛选优先用它，缺失时用地区关键词兜底。
- 四个工具都返回 `detail_url`（详情页链接）——**输出时务必原样附上**（见 §五）。

## 四、筛选流程（金额区间 = 「已扫描窗口内」筛选）

**先讲清能力边界（最容易答错的地方）**：`search_debt_notice` 的入参**只有 `keyword` / `page` / `page_size`**——**服务端不支持任何金额、地区、类型条件**（接口与后端查询均无这些参数）。所以「金额 3000 万–3 亿」**不是一次查询就能筛出的条件**，正确姿势是：

> **先用关键词把命中量收窄到可扫描规模 → 按日期倒序逐页扫描 → 在已扫描到的条目里按金额区间过滤 → 并如实披露扫描覆盖率。**

**扫描粒度固定 20 条/次**（`page_size` 服务端硬上限 20，传更大也只回 20 条）。

### 4.1 第一步永远是把 `total` 压到可扫描规模

| 命中总数 `total` | 做法 |
|---|---|
| ≤ 100（≤5 页） | 逐页扫完 → 金额区间即**全量命中内的筛选** |
| 100 – 400（≤20 页） | 按 4.2 的预算扫描，输出**必须**标注覆盖率与时间窗 |
| > 400 | **不要硬扫**：先按 4.3 收窄；收窄不动时只输出「预算窗口内的筛选结果」并显著标注**非全量** |

### 4.2 扫描预算与覆盖率口径

- 每页固定 `page_size=20`，`page` 从 1 递增，**按日期倒序推进**（同一天可能跨页，取回后按 `notice_id` 去重；分页推进即为沿时间轴向前回溯）。
- 换算：`可扫描条数 ≈ 20 × 调用次数`。一次筛选建议**总额 ≤20 次调用**（含翻页与明细），即最多扫 ~400 条。
- **必须输出三个数**：`已扫描条数`、`覆盖率 = 已扫描条数 / total`、`已覆盖日期窗口`（本次扫描到的 `notice_date` 最小～最大）。
- `total` 为 `10000` 时是**上限估算**：覆盖率写成「≥ 已扫描 / 10000」，不得声称全量。

### 4.3 收窄关键词三招（优先于翻页）

1. **换更具体的同义词**：`煤矿` → `煤业` / `煤化工` / `采矿权` / `煤场`；词越具体 `total` 越小。
2. **叠加主体词分轮取交集**：用出让方（AMC / 银行）名或已知债务人名各搜一轮，与行业词结果取交集。
3. **按资产类型拆分**：同一行业内按标的类型分轮搜（`采矿权` / `土地使用权` / `机器设备`），最后取并集。

> **禁止把多个词写进一个 `keyword`**：`keyword` 是**单词（短语）**匹配，实测传 `煤矿 转让`（带空格）返回 **0 条**。要组合条件只能**分轮单词检索 + 本地取交集**。
>
> 关键词过宽（`公司` / `银行` / `资产`）命中会很杂；关键词过短（单字）命中通常更大，不建议。

### 4.4 逐词扫描、过滤与聚合

1. **逐词扫描** — 对每个关键词调用 `search_debt_notice(keyword=词, page_size=20)`，按 `page` 递增到预算上限；**每条结果的 `detail_url` 都要留着**
2. **去重与去噪** — 多词结果按 `notice_id` 去重；`title` / `debtor` 与线索明显无关的（全文命中的噪声）剔除并计数
3. **地区过滤** — `area` 等于目标省 → 保留；`area` 缺失 → 用地区词是否出现在 `title` / `debtor` 中兜底，并标注「按关键词兜底」
4. **金额过滤**（本地，闭区间）
   - 口径：**本金优先** `principal_amount_yuan`；本金为 `0` 或缺失 → **回落** `total_amount_yuan`，并标注所用口径；两者都为 `0` 或缺失 → 归入「金额未披露」组**单列**
   - 判定：`min_yuan` ≤ 取值 ≤ `max_yuan`；区间换算成元（3000 万 → `30000000`，3 亿 → `300000000`）
5. **按出让方聚合** — 以 `creditor` 分组：标的数、本金合计（`*_yuan` 求和）、涉及债务人（`debtor` **先按逗号拆分**再去重）、最近公告日期；按本金合计倒序
6. **重点标的明细（可选）** — 金额最大或最新的 1～3 条调 `get_debt_notice_detail(notice_id=...)`，取 `collateral` / `guarantor` / `original_creditor`
7. **可选：按债务人汇总** — 从清单的 `debtor`（拆分后）取企业名，**逐个** `search_debt_enterprise` → `get_debt_enterprise_debt_summary`

> 请克制调用次数（共享配额）：相邻调用间隔 ≥1 秒（游客 1 QPS）；一次筛选建议 **≤20 次工具调用**。扫描与过滤的参考实现见 `@references/tools-and-fields.md`「扫描与过滤参考实现」。

## 五、输出与链接规则

输出模板见 `@templates/debt-screening-report.md`（筛选概览 / 持有人分布 / 标的清单 / 分布统计 / 提示 五节）；字段为空时按模板中的说明处理，**不要编造**。

> **读不到模板文件时**（例如平台只分发 SKILL.md），按下面的骨架组织输出即可：

```markdown
## 债权标的筛选：{行业词} × {地区} × {金额区间}
> 数据来源：智收云公开债权公告（命中 {total} 条，已扫描 {scanned} 条，覆盖率 {coverage}）｜查询时间：{yyyy-MM-dd HH:mm}｜口径：公开公告，非征信报告

1. 筛选概览 —— 关键词（枚举了几个）、地区、金额区间与所用金额口径、命中总数 `total`、**已扫描条数 / 覆盖率 / 已覆盖日期窗口**
2. 入筛结果 —— 金额区间内命中 X 条（**限已扫描窗口内**）；是否为全量（覆盖率 100% / 未覆盖说明）
3. 持有人（出让方）分布 —— 出让方：命中 X 个标的，本金合计 Y，涉及债务人数 Z，最近公告日期（按本金合计倒序，最多 15 家）
4. 标的清单（按本金倒序，最多 20 条）—— 日期、类型、地区、标题、出让方、债务人、本金、**链接**
5. 分布统计 —— 类型 / 地区 / 金额档位：条数与本金合计
6. 提示 —— 公开公告口径；**金额区间仅在已扫描窗口内生效，不等于全量结果**；`area` 为公告地区（省级、可能缺失）；出让方≠当前持有人；金额未披露单列；`total` 为 10000 时可能被截断；链接为接口返回值（原样引用）
```

**链接规则（原样引用，不做任何改写）**：

- **引用必附链接**：凡引用公告或企业，都要附上其 `detail_url`。链接形如 `…/notice/<公告ID>`（公告）或 `…/debtor/<企业ID>`（企业）；返回里没有该字段时写「暂无链接」。
- **链接一律原样输出**：`scheme`、域名、路径、ID 与查询参数**全部照搬接口返回值**——不要追加、修改、覆盖或删除任何查询参数，**不要添加任何来源/追踪标识**，也不要缩短、改写或自行猜测链接。链接是服务端返回的数据，不是可加工的对象。
- 展示的链接文本与 href 用**同一个 URL**；出让方名、标题做成可点击链接时同样照搬返回值。
- 说明：创建游客时上报的 `skillId`（客户端标识，**同一产品的多端统一用同一个标识**；取值见 `@references/client-source-ids.md`，表外客户端用 `@scripts/client_id.py` 生成）与 `skillCode`（本 SKILL 的包名，固定为 `debtop-debt-screening`）都是**请求字段**，只用于服务端归属统计（见 `@references/guest-access.md`）；它们与输出链接无关，**不要写进任何 URL**。

**其它输出要求**：

- **金额成对返回**：计算、求和与排序一律用 `*_yuan`，展示给用户用 `*_text`，不要混用或自行换算；合计金额可同时给出 `_text` 便于阅读。
- **命中缘由要标注**：全文检索可能因**抵押物文本**而非债务人主业命中（如某公告标题或抵押物里出现「煤矿」），输出时不要把"命中"写成"该债务人主业为煤矿"。
- **ID 不可臆造**：`notice_id` / `enterprise_id` 一律取自上一跳搜索结果；`notice_id` 是纯数字（int64）。
- **覆盖率必须披露（本 Skill 的核心口径）**：必须同时给出 `total`、`已扫描条数`、`覆盖率`（已扫描 / total）与**已覆盖日期窗口**；覆盖率 < 100% 时必须写明「金额区间结果仅覆盖已扫描窗口，非全量」，不得用"全部 / 全量"表述。展示条数以本次实际取得为准，不要用数组长度冒充命中总数。
- **禁止多词关键词**：一次 `search_debt_notice` 只传**一个**词（短语）；组合条件靠分轮检索 + 本地取交集（见 §四 4.3）。
- **`debtor` 去重**：多主体串**先按逗号拆分**再统计，不要把整串当作一个企业名。
- **串行调用、留出间隔**：相邻工具调用至少间隔 1 秒；按「公告检索（逐词）→ 本地过滤聚合 →（可选）公告详情 →（可选）企业搜索 → 企业概要」顺序**串行**执行。
- **游客身份的边界**：若某些字段为空或提示需登录明细，说明该数据需登录用户权限——应引导用户完成 OAuth 授权，并把当前游客绑定到该用户（`POST /bff/v1/guest-access/upgrade`，见 `@references/guest-access.md`）。

## 六、错误处置

| 情形 | 处置 |
|---|---|
| `401` / `AUTH_REQUIRED` / `AUTH_INVALID` | 先刷新游客令牌；刷新也失败 → 重建游客并重试一次 |
| `GUEST_LIMITED`（**工具级错误，HTTP 仍为 200**） | 退避 1 秒后重试，保持串行；必要时**减少关键词枚举数** |
| `429` / `RATE_LIMITED` | 指数退避、降低并发；创建类避免突发 |
| `PARAM_INVALID` | 改参数重试（空 `keyword`、`page_size>100`、关键词过宽） |
| `RESOURCE_NOT_FOUND` | 换 `notice_id` 或关键词重查，不臆造 ID |
| 上游 5xx / 超时 | 保留已取得的清单结果，并提示用户稍后再试；不要继续翻页 |

> 完整错误码、工具级错误与两个端点的区别、逐项降级路径见 `@references/errors.md`。

## 七、合规与限流

- **真实数据、面向对外沟通**：结论可能被用户用于寻找资产标的或对外材料，因此
  - 必须标注**数据来源（智收云公开公告）与查询时间**；
  - 必须声明**「公开公告口径，非征信报告」**，不用公告数据推断未披露债务、偿付能力或信用等级，**不构成投资建议**；
  - 必须声明**出让方（`creditor`）是公告中的债权人 / 出让方，不等于当前实际持有人**（债权可能已再次转让）；
  - `area` 是**公告地区（省级、条件字段可能缺失）**，不是抵押物坐落；按关键词兜底时要标注兜底口径；
  - 不做超出数据的因果与法律结论；同名机构未确认归属前不得合并。
- **只读、禁止批量导出**：4 个工具均为只读查询；禁止用它做整库拉取、爬取或长期归档。分页实际按 20 截断（见 `@references/tools-and-fields.md`），需要更多请翻页并控制节奏。
- **不要暗示「服务端能按金额筛」**：检索接口没有金额参数，金额区间只有在**已扫描窗口内**才成立。回答时不得表述成「系统里 3000 万–3 亿的煤矿债权共有 N 条」，只能表述为「在已扫描的 X 条（覆盖 Y%）中，符合区间的是 N 条」。
- **命中总数可能被截断**：`total` 达到 `10000` 时表示可能已被上限截断，输出时应说明"命中总数以接口返回为准，达到 10000 表示可能截断"，不要声称"全量"。
- **关键词取不到数据时**：换同义词 / 更完整的名称重试一次；仍 0 命中时如实告知"未检索到符合条件的公开公告"，**不得编造公告**，也不得用近似主体替代。
- **限流是共享配额**（数值见 §一）：超限 429 会影响其他用户，**不要做压测或并发突发**；同一组筛选条件避免短时间重复执行。
- **数据处理范围（对外可明确说明）**：本 Skill 只做三件事——① 用用户给的关键词调用本服务的**只读**查询工具；② 需要走游客通道时上报「客户端/平台标识（`skillId`）」与「本技能包名（`skillCode`）」，**仅用于来源归属统计与配额防滥用**；③ **原样**返回服务端结果。**不读取本地文件、不采集用户个人信息、不向任何第三方转发数据、不改写任何返回链接。**
- **令牌仅限本服务**：游客令牌与 Guest 签名密钥**仅授权用于 `agent.debtop.com`**；不得用于其它部署或域名。
- **接入前自查**（首次接入或升级后各跑一次）：

```bash
BASE=https://agent.debtop.com
# 1) 发现元数据应含 x-guest-access 且 public_create=true
curl -s $BASE/.well-known/oauth-protected-resource | grep -qE '"public_create"[[:space:]]*:[[:space:]]*true' \
  && echo "元数据 OK (公开通道已开启)"     # 注意: 响应是紧凑 JSON, 冒号后可能无空格
# 2) PoW 挑战端点应可达
curl -s -o /dev/null -w "challenge=%{http_code}\n" $BASE/bff/v1/guest-access/challenge
# 期望: 200；若为 404 说明 GUEST_PUBLIC_CREATE_ENABLED=false
# 3) 免凭据创建必须被要求 PoW（准入校验生效）
curl -s -X POST $BASE/bff/v1/guest-access -H 'Content-Type: application/json' -d '{"source":"web"}'
# 期望: {"success":false,"code":"POW_REQUIRED",...}
#       若直接返回 accessToken, 说明 PoW 校验被绕过（严重, 立即熔断: 置 false 并重建容器）
# 4) 拿到游客令牌后, 用一条 search_debt_notice(keyword=<行业词>, page_size=5) 验证取数
```

- **异常优先降级**：出现连续 5xx / 超时，停止继续翻页，保留已取得的清单，并提示用户稍后重试，不要反复重试放大故障。

## 八、本技能包资源与脚本

> **跨平台读法**：表中的 `@路径` 是 WorkBuddy 的技能内引用写法；在其它平台按**同名的相对路径**读取同名文件即可（文件名与目录名完全一致）。脚本请用 `bash` / `python3` **显式调用**（技能包内不含可执行位）；若平台不能执行脚本，按 `@references/guest-access.md`「运行前提与替代方案」处理。

| 资源 | 用途 |
|---|---|
| `@references/guest-access.md` | 零配置游客通道：端点、能力边界、可直接复制执行的 curl、令牌刷新、升级与降级路径 |
| `@references/tools-and-fields.md` | 4 个工具的完整参数、返回字段、条件字段、枚举与索引范围（含 `area`、金额口径、分页与扫描口径、**扫描与过滤参考实现**） |
| `@references/errors.md` | 错误码与处置、工具级错误与两个端点的错误区分 |
| `@references/client-source-ids.md` | 客户端标识对照表（创建游客时上报的 `skillId` 取值，60+ 客户端） |
| `@templates/debt-screening-report.md` | 筛选结果输出模板（五节，含链接占位说明） |
| `@scripts/guest_token.sh` | 取游客令牌：`bash scripts/guest_token.sh [输出文件] [BASE]`（失败非 0 退出并在 stderr 给出错误码） |
| `@scripts/pow_solve.py` | 解 PoW 挑战：`python3 scripts/pow_solve.py <challenge> <difficulty>` |
