---
name: debtop-creditor-disposal
display_name: 债权人债权处置清单
display_name_en: Creditor Debt Disposal List
description: "债权人债权处置清单：给定银行、AMC 或其它出让方名称，汇总其在公开渠道发布的债权转让 / 处置 / 招商 / 挂牌公告——公告清单、类型分布、本金与总额合计、涉及债务人、公告时间线与重点标的。当用户说「XX 银行 / XX AMC 最近在处置哪些债权」「这家出让方有哪些债权转让公告」「某资产公司有哪些资产包 / 债权货源」，或给出债权人名称要求汇总其处置公告时使用。一个债权人名称即可，免注册免登录。英文触发词：creditor disposal list, AMC debt disposal, debt transfer list, asset package sourcing。若用户要的是某家企业的债务规模或债务画像，改用 debtop-enterprise-profile；若只是按任意关键词搜公告清单，改用 debtop-notice-search；若要某企业合作前的债务速查，改用 debtop-counterparty-check。"
description_zh: "债权人债权处置清单：给定银行、AMC 或其它出让方名称，汇总其在公开渠道发布的债权转让 / 处置 / 招商 / 挂牌公告——公告清单、类型分布、本金与总额合计、涉及债务人、公告时间线与重点标的。当用户说「XX 银行 / XX AMC 最近在处置哪些债权」「这家出让方有哪些债权转让公告」「某资产公司有哪些资产包 / 债权货源」，或给出债权人名称要求汇总其处置公告时使用。一个债权人名称即可，免注册免登录。英文触发词：creditor disposal list, AMC debt disposal, debt transfer list, asset package sourcing。若用户要的是某家企业的债务规模或债务画像，改用 debtop-enterprise-profile；若只是按任意关键词搜公告清单，改用 debtop-notice-search；若要某企业合作前的债务速查，改用 debtop-counterparty-check。"
description_en: "Build a disposal list for one creditor (bank / AMC / other seller): summarize the debt transfer, disposal, investment-invitation and listing notices it published publicly, covering notice lists, type distribution, principal and total amount, debtors involved, timeline and key targets. Use when the user asks 'what debts is XX bank / AMC disposing', 'which debt transfer notices does this seller have', or gives a creditor name and wants its disposal notices summarized. Only the creditor name is needed, no sign-up and no configuration needed. For one enterprise's debt profile, use debtop-enterprise-profile; for a generic keyword notice search, use debtop-notice-search; for a pre-deal counterparty check, use debtop-counterparty-check."
version: 1.0.0
author: 智收云
disable-model-invocation: false
user-invocable: true
---

# 债权人债权处置清单（游客免登录）

给定一个出让方（**银行 / AMC / 其它债权人**）名称，汇总其在公开渠道发布的债权**转让 / 处置 / 招商 / 挂牌**公告：命中清单、类型分布、本金与总额合计、涉及债务人、公告时间线与重点标的；**每条引用都原样附详情页链接**。

> 产出可能被用户用于寻找资产标的、处置合作或对外材料，请遵守 §七 的合规与限流要求。
> 本 Skill 的端点与令牌**仅授权用于 `agent.debtop.com`**；调用前请确认端点与此一致。

数据来自**智收云MCP**（不良资产债权转让/处置公告，覆盖报纸电子版、AMC 官网、产权交易所、阿里资产、京东法拍等）。

## 何时使用

- 用户问「XX 银行 / XX AMC 最近在处置哪些债权 / 有哪些债权转让公告」
- 用户给出**出让方（债权人）**名称，要求列出其处置公告清单，并按类型、金额或时间整理
- 用户要找「债权货源 / 资产包」（买方视角，按出让方找标的）
- 用户要核实「某机构是否在处置某类债权」——公告维度可直接回答

> **与相邻 Skill 的分工**：本 Skill 以**出让方（债权人）为主体**组织「处置清单」；若要某家企业的债务规模/画像，用 `debtop-enterprise-profile`；若只是按任意关键词搜公告清单，用 `debtop-notice-search`；若要某企业合作前的债务速查，用 `debtop-counterparty-check`。

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

**第 1 步｜探测一次**（仅当第 0 步无法确定时）：调一次 `tools/list`，或一次轻量工具调用（如 `search_debt_notice(keyword=机构名, page_size=5)`）。**不要用「创建游客」来探测**——那会消耗创建配额。

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
| `search_debt_notice` | **债权公告搜索（本 Skill 主入口，出让方维度）** | `keyword`（**债权人/出让方名称**） |
| `get_debt_notice_detail` | 公告详情（重点标的的担保线索） | `notice_id` |
| `search_debt_enterprise` | 企业搜索（辅助：把清单里的**债务人**定位到主体） | `keyword`（**单一**企业名称） |
| `get_debt_enterprise_debt_summary` | 企业债务概要（辅助：按债务人汇总规模） | `enterprise_id` |

四个要点（完整参数、返回字段、条件字段与枚举见 `@references/tools-and-fields.md`）：

- **公告索引同时覆盖出让方（债权人）与融资方（债务人）**，因此**用债权人名可以直接搜到公告**——这正是本 Skill 的入口。
- 与之相对，`search_debt_enterprise` 是**债务人（融资方）**维度，用债权人名通常 0 命中；**本 Skill 不要用它去找出让方**（要按出让方检索一律用 `search_debt_notice`）。
- `debtor` 是**逗号分隔的多主体串**（`甲公司,乙公司`），`debtor_num` 即主体个数；统计前先按逗号拆分。
- 四个工具都返回 `detail_url`（详情页链接）——**输出时务必原样附上**（见 §五）。

## 四、处置清单生成流程

1. **确定出让方名称** — 用机构全称或较完整的简称（如 `中国华融` / `XX 银行股份有限公司`）；名称过宽（如 `银行` / `资产`）命中会很杂
2. **拉处置公告清单** — `search_debt_notice(keyword=出让方名称, page_size=20)`，**每条结果的 `detail_url` 都要留着**；多于 20 条时翻页（`page` 递增）
3. **归类与汇总** — 按 `notice_type` / `notice_type_name` 归类（`transfer` 转让、`deal` 处置、`market` 招商、`trade` 处置挂牌、`collect` 催收、`correct` 更正），统计各口径**公告数、本金合计（`*_yuan`）、总额合计**；按 `notice_date` 倒序；把 `debtor` 拆分去重得到**涉及债务人数**
4. **重点标的明细** — 对金额最大或最新的 1～3 条调用 `get_debt_notice_detail(notice_id=...)`，取 `guarantor` / `collateral` / `original_creditor`；**引用哪条就原样附哪条的 `detail_url`**
5. **可选：按债务人汇总** — 从清单的 `debtor`（拆分后）取企业名，**逐个** `search_debt_enterprise` → `get_debt_enterprise_debt_summary`，补充该债务人的债务规模（注意这是**债务人维度**，与出让方视角互为补充）
6. **可选：对比多个出让方** — 用户要横向比较时，对每个出让方各跑一轮步骤 2～3，再并排放置

> 请克制调用次数（共享配额）：一次清单建议控制在 **15 次工具调用以内**，避免不必要的翻页与重复查询。

## 五、输出与链接规则

输出模板见 `@templates/creditor-disposal-report.md`（处置概览 / 公告清单 / 类型与金额分布 / 重点标的明细 / 涉及债务人 / 提示 六节）；字段为空时按模板中的说明处理，**不要编造**。

> **读不到模板文件时**（例如平台只分发 SKILL.md），按下面的骨架组织输出即可：

```markdown
## {出让方名称} 债权处置清单
> 数据来源：智收云公开债权公告（命中 {N} 条，本次展示 {M} 条）｜查询时间：{yyyy-MM-dd HH:mm}｜口径：公开公告，非征信报告

1. 处置概览 —— 出让方名称、命中公告总数、公告时段、涉及债务人数、数据来源渠道
2. 公告清单（按日期倒序，最多 20 条）—— 日期、类型、标题、债务人、本金、**链接**
3. 类型与金额分布 —— 转让 / 处置 / 招商·挂牌 / 催收：公告数、本金合计、总额合计
4. 重点标的明细（1～3 条）—— 标题、债务人、本金/总额、保证人、抵押物、原债权人、公告详情链接（未披露的写「公告未披露」）
5. 涉及债务人 —— 债务人：命中 X 条公告，涉及本金 Y（最多列前 5）
6. 提示 —— 公开公告口径；金额 `_yuan` / `_text` 口径说明；链接为接口返回值（原样引用）
```

**链接规则（原样引用，不做任何改写）**：

- **引用必附链接**：凡引用公告或企业，都要附上其 `detail_url`。链接形如 `…/notice/<公告ID>`（公告）或 `…/debtor/<企业ID>`（企业）；返回里没有该字段时写「暂无链接」。
- **链接一律原样输出**：`scheme`、域名、路径、ID 与查询参数**全部照搬接口返回值**——不要追加、修改、覆盖或删除任何查询参数，**不要添加任何来源/追踪标识**，也不要缩短、改写或自行猜测链接。链接是服务端返回的数据，不是可加工的对象。
- 展示的链接文本与 href 用**同一个 URL**；标题、债务人名做成可点击链接时同样照搬返回值。
- 说明：创建游客时上报的 `skillId`（客户端标识，**同一产品的多端统一用同一个标识**；取值见 `@references/client-source-ids.md`，表外客户端用 `@scripts/client_id.py` 生成）与 `skillCode`（本 SKILL 的包名，固定为 `debtop-creditor-disposal`）都是**请求字段**，只用于服务端归属统计（见 `@references/guest-access.md`）；它们与输出链接无关，**不要写进任何 URL**。

**其它输出要求**：

- **金额成对返回**：计算与排序用 `*_yuan`，展示给用户用 `*_text`，不要混用或自行换算。
- **ID 不可臆造**：`notice_id` / `enterprise_id` 一律取自上一跳搜索结果；`notice_id` 是纯数字（int64）。
- **清单如实标注条数**：命中总数以返回的 `total` 为准，展示条数以本次实际取得为准（分页按 20 截断）。
- **涉及债务人去重**：`debtor` 多主体串**先按逗号拆分**再去重统计，不要把整串当作一个企业名。
- **串行调用、留出间隔**：相邻工具调用至少间隔 1 秒；按「公告搜索 → 公告详情 →（可选）企业搜索 → 企业概要」顺序**串行**执行。
- **游客身份的边界**：若某些字段为空或提示需登录明细，说明该数据需登录用户权限——应引导用户完成 OAuth 授权，并把当前游客绑定到该用户（`POST /bff/v1/guest-access/upgrade`，见 `@references/guest-access.md`）。

## 六、错误处置

| 情形 | 处置 |
|---|---|
| `401` / `AUTH_REQUIRED` / `AUTH_INVALID` | 先刷新游客令牌；刷新也失败 → 重建游客并重试一次 |
| `GUEST_LIMITED`（**工具级错误，HTTP 仍为 200**） | 退避 1 秒后重试，保持串行 |
| `429` / `RATE_LIMITED` | 指数退避、降低并发；创建类避免突发 |
| `PARAM_INVALID` | 改参数重试（空 `keyword`、`page_size>100`、关键词过宽） |
| `RESOURCE_NOT_FOUND` | 换 `notice_id` 或机构名重查，不臆造 ID |
| 上游 5xx / 超时 | 保留已取得的清单结果，并提示用户稍后再试 |

> 完整错误码、工具级错误与两个端点的区别、逐项降级路径见 `@references/errors.md`。

## 七、合规与限流

- **真实数据、面向对外沟通**：结论可能被用户用于寻找资产标的、处置合作或对外材料，因此
  - 必须标注**数据来源（智收云公开公告）与查询时间**；
  - 必须声明**「公开公告口径，非征信报告」**，不用公告数据推断未披露债务、偿付能力或信用等级；
  - 不做超出数据的因果与法律结论；同名机构未确认归属前不得合并。
- **只读、禁止批量导出**：4 个工具均为只读查询；禁止用它做整库拉取、爬取或长期归档。分页实际按 20 截断（见 `@references/tools-and-fields.md`），需要更多请翻页并控制节奏。
- **出让方（债权人）维度取不到数据时**：机构名过宽（如 `银行` / `资产管理`）命中会很杂，先用更完整的机构全称重试一次；仍 0 命中时，如实告知"未检索到该出让方的公开处置公告"，**不得用近似机构替代，也不得编造公告**。注意：`search_debt_enterprise` 查不到债权人属正常（它是债务人维度），不要用它来否定本 Skill 的结果。
- **限流是共享配额**（数值见 §一）：超限 429 会影响其他用户，**不要做压测或并发突发**；同一出让方的清单避免短时间重复执行。
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
# 4) 拿到游客令牌后, 用一条 search_debt_notice(keyword=<某银行/AMC>, page_size=5) 验证取数
```

- **异常优先降级**：出现连续 5xx / 超时，停止继续翻页，保留已取得的清单，并提示用户稍后重试，不要反复重试放大故障。

## 八、本技能包资源与脚本

> **跨平台读法**：表中的 `@路径` 是 WorkBuddy 的技能内引用写法；在其它平台按**同名的相对路径**读取同名文件即可（文件名与目录名完全一致）。脚本请用 `bash` / `python3` **显式调用**（技能包内不含可执行位）；若平台不能执行脚本，按 `@references/guest-access.md`「运行前提与替代方案」处理。

| 资源 | 用途 |
|---|---|
| `@references/guest-access.md` | 零配置游客通道：端点、能力边界、可直接复制执行的 curl、令牌刷新、升级与降级路径 |
| `@references/tools-and-fields.md` | 4 个工具的完整参数、返回字段、条件字段、枚举与索引范围 |
| `@references/errors.md` | 错误码与处置、工具级错误与两个端点的错误区分 |
| `@references/client-source-ids.md` | 客户端标识对照表（创建游客时上报的 `skillId` 取值，60+ 客户端） |
| `@templates/creditor-disposal-report.md` | 处置清单输出模板（六节，含链接占位说明） |
| `@scripts/guest_token.sh` | 取游客令牌：`bash scripts/guest_token.sh [输出文件] [BASE]`（失败非 0 退出并在 stderr 给出错误码） |
| `@scripts/pow_solve.py` | 解 PoW 挑战：`python3 scripts/pow_solve.py <challenge> <difficulty>` |
