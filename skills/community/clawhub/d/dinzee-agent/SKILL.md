---
name: dinzeeagent
description: "Cross-border e-commerce data agent. The user triggers a data source with an at-source marker such as @sif, or triggers a bundled local business skill with @<task-name> plus a natural-language task instruction. The agent syncs official Dinzee skills into the local Hermes/OpenClaw runtime, extracts business parameters, runs the matched local skill, and lets every data/tool call route through the Dinzee gateway for unified authentication and per-call billing. Available sources and tools are discovered at runtime from the gateway; upstream MCP endpoints and credentials are never exposed."
metadata: {"DinzeeAgent":{"emoji":"🦅","homepage":"https://gateway.dinzee.ai/","requires":{"env":["DINZEE_USER_TOKEN"]}}}
---

# DinzeeAgent — 跨境电商数据 Agent

DinzeeAgent 让你用 `@<数据源>` 触发第三方电商数据能力，也让用户用 `@<业务任务>` 触发已同步到本地 Hermes/OpenClaw runtime 的 Dinzee 业务 skill。看到触发标记后，**你（agent）自行编排**调用该数据源的多个 MCP 工具，或运行匹配的本地业务 skill，完成用户的调研/分析任务，最后汇总成结论。

所有调用经由 **Dinzee 网关**（`https://gateway.dinzee.ai/`）：网关负责鉴权、按次扣点、转发到上游 MCP server。上游地址与凭证对调用方完全隐藏。

**有哪些数据源、每个数据源有哪些工具，都由网关运行时决定（随时新增），本文档不写死。** 每次任务先用 `providers` / `list-tools` 实时发现（见下文「工具发现」）。

## 内置业务能力

DinzeeAgent 是总入口。用户只需要安装/更新 `dinzeeagent`，再运行一次 `sync-skills`，不需要知道每个业务 skill 的安装名称。

当前随 DinzeeAgent 推荐同步的业务能力：

### Amazon 商品/市场分析

- `@amazon-product-attribute-market-analysis`：美国站前台搜索、配送邮编模拟、TOP 商品采集、属性打标、销量容量饼图、爆款组合锁定。

### 爆发新品/黑马挖掘

- `@breakout-product-radar`：指定类目近周期新晋上架/新追踪商品，过滤 BSR 阈值，按销量权重排序并输出趋势报告。
- `@momentum-product-scout`：低评价量、高近月销量商品扫描，识别视觉创新、功能差异化、套装组合、强 IP、季节/人群场景等起量路径。

### 数据网关工具

- `@sif` 及其他已开放数据源：通过 `providers` / `list-tools` 实时发现当前可用工具，按用户 token 计费调用。

## Setup

1. 取得用户接入 token（`sut_` 开头，由 ai_web 签发，每个用户独立）。
2. 配置 token（二选一）：
   - 环境变量（推荐，符合 openclaw 习惯）：`export DINZEE_USER_TOKEN=sut_xxxxxxxx`
   - 或保存到凭证文件：`python3 <skill>/scripts/dinzee.py login sut_xxxxxxxx`
     （默认写入 `/opt/data/.dinzee/credentials.json`，权限 0600，重启不丢）
3. （可选）覆盖凭证路径：
   `export DINZEE_CREDENTIALS_PATH=/your/persistent/path/credentials.json`
   - 建议使用绝对路径，并确保运行 Agent 的系统用户可写。
   - 旧路径 `~/.dinzee/credentials.json` 仅作为兼容读取回退；`login` 和 `logout` 不会写入或删除旧路径。
4. MCP 调用结果默认写入 `/opt/data/.dinzee/data`。可覆盖：
   `export DINZEE_DATA_DIR=/your/persistent/data`
   - 建议使用绝对路径，并确保运行 Agent 的系统用户可写。
   - 数据目录及 provider/tool 子目录会显式设置为 `0777`，数据 JSON 会设置为 `0666`。
   - 该开放权限适用于单租户、容器内仅运行可信程序的部署；凭证文件仍严格保持 `0600`。
   - 单次调用可通过 `--no-save` 禁止落盘。
5. （可选）覆盖网关地址：`export DINZEE_GATEWAY_BASE_URL=https://gateway.dinzee.ai/`
6. 自检：`python3 <skill>/scripts/dinzee.py status` 与 `python3 <skill>/scripts/dinzee.py providers`，确认 token 有效并看到当前可用的数据源。

## 装 / 更新数据 skill（安装不扣费）

DinzeeAgent 既是数据网关客户端，也是 **skill 交付客户端**——用户可以通过它把我们的数据 skill 装进 agent、或更新到新版。安装/更新只交付包，不扣费；真实扣费发生在本地业务 skill 成功执行后，通过 Gateway 工具调用或 `dinzee_skill_meter` 记录。

当用户说「**@dinzeeagent 安装 <skill>**」「**@dinzeeagent 更新 skill**」「更新一下技能」之类时：

1. **看有哪些可装的 skill 及价格**：
   ```bash
   python3 <skill>/scripts/dinzee.py skills
   ```
   列出每个 skill 的 slug、最新版本、单价（`N点/次` 或 `免费`）。
2. **安装/更新某个 skill**（不扣费，只交付包）：
   ```bash
   python3 <skill>/scripts/dinzee.py skill-install <slug>
   ```
   交付成功后文件会写入 agent 的 skills 目录，openclaw 热加载即可使用。
3. **更新已装的全部内容 skill**：
   ```bash
   python3 <skill>/scripts/dinzee.py skill-update --all
   ```
   只拉取新版本包；安装/更新不扣费。

4. **同步 Dinzee 官方业务 skill 包（推荐）**：
   ```bash
   python3 <skill>/scripts/dinzee.py sync-skills
   ```
   这会自动安装/更新当前随 DinzeeAgent 推荐的业务 skill，用户不需要知道每个子 skill 的 slug。当前包含官方商品/市场分析、爆发新品、低评高销挖掘，以及从 Dinzee skill 仓库导入的 Amazon/1688/SIF/BSC 等业务 skill。

**注意**：
- 安装/更新不扣费；不要把包交付当成业务调用收费。
- `dinzeeagent` 自身是免费客户端，用 clawhub 安装/更新。
- 业务扣费只在本地 skill 成功完成并准备交付时发生，来源应是具体 Gateway 工具或 `dinzee_skill_meter.<skill>_run`。

## 本地运行业务 skill（推荐路径）

当用户要运行一个已经封装好的任务包，走**本地 Hermes/OpenClaw runtime 执行 skill**。Dinzee 服务端只负责网关鉴权、上游工具转发和扣点，不负责替用户执行整个业务 workflow。

对当前内置业务任务，先确认本地已同步这些 skill；如果本地还没有，先执行 `sync-skills`。随后打开对应本地 skill 的 `SKILL.md`，按其中脚本/流程运行；这些脚本会使用 `DINZEE_USER_TOKEN` 调 Dinzee gateway，工具调用或最终 `skill_meter` 会实时计费。

### 统一用户调用方式

用户不需要知道 `skill_slug`、`params`、`idempotencyKey`。面向用户只暴露一种格式：

```text
@任务名 自然语言任务指令
```

例如：

```text
@amazon-product-attribute-market-analysis
模拟美国站点前台搜索，配送邮编设置为90001，搜索关键词为「MagSafe phone tripod」，抓取前50条TOP商品，完成属性打标、销量占比、饼状图和趋势总结。
```

OpenClaw/Hermes/Agent 看到这类指令时必须执行以下规则：

1. **识别任务包**：如果 `@` 后面正好是某个已同步业务 skill 名称，直接使用该本地 skill；如果用户没有写精确名称，则根据任务语义从本地已同步 Dinzee 业务 skill 中选择最匹配的一个。
2. **抽取业务参数**：从自然语言里抽取站点、邮编、关键词、数量、类目、时间窗口、BSR 阈值、评价数阈值、销量阈值等，只保留业务参数。
3. **标准化参数**：把「美国 / 美国站 / US / Amazon.com」统一成 `"US"`；把「前50条 / top 50」统一成 `"limit": 50`；缺失但 manifest 有默认值的参数使用默认值。
4. **执行本地 skill**：打开匹配 skill 的 `SKILL.md`，优先运行其 `scripts/` 下的封装脚本；不要把用户转去填写 `skill_slug`、变量名或 JSON 参数。
5. **返回结果**：最终向用户展示报告文件/链接、结果摘要、关键样本和扣点明细。工具扣点明细来自 gateway 返回或运行日志。

常用操作：

```bash
# 一键同步/更新 Dinzee 官方业务 skill
python3 <skill>/scripts/dinzee.py sync-skills

# 然后根据用户 @ 的任务名，进入对应本地 skill 执行其 SKILL.md 里的流程
```

当前随包注册的业务 skill 以 `scripts/dinzee.py sync-skills` 的清单为准；包括商品属性分析、爆发新品、低评高销挖掘，以及 Amazon/1688/SIF/BSC 等导入业务 skill。

Hermes 用户任务优先走本地业务 skill + Dinzee gateway。历史调试命令保留在 CLI 中，仅供开发者排查旧链路。

### 三个内置任务的自然语言映射

- 用户提到「美国站前台搜索 / 商品属性打标 / 容量饼状图 / 爆款组合锁定」时，映射到 `amazon-product-attribute-market-analysis`。
  常见参数：`site`、`zipcode`、`keyword`、`limit`。
- 用户提到「近30天新上架 / BSR前10000 / 新品黑马 / 类目趋势」时，映射到 `breakout-product-radar`。
  常见参数：`site`、`category`、`days_new`、`bsr_threshold`、`limit`。
- 用户提到「低评价量 / 高销量 / 评价少但月销高 / 爆发单品」时，映射到 `momentum-product-scout`。
  常见参数：`site`、`max_reviews`、`min_monthly_sales`、`limit`。

## 工具发现：动态，不要硬编码（核心）

**不要假设有哪些数据源、也不要背工具清单**——可用的数据源和工具由网关运行时决定，随时可能新增或下线。每次任务都先发现：

1. **看有哪些数据源**：`python3 <skill>/scripts/dinzee.py providers`
   返回当前网关已开放的 provider 列表。用户 `@xxx` 里的 `xxx` 必须在这个列表里，否则告诉用户该数据源暂未开放。
2. **看某数据源有哪些工具**：`python3 <skill>/scripts/dinzee.py list-tools --provider <source>`
   返回该 provider 全部已开放工具，**每个工具自带 `description`（官方用途说明）、`input_schema`（入参 schema）、`points_cost`（单价，null=免费）、`chargeable`**。
3. **据此自由编排**：读 `description` 理解每个工具能干什么、读 `input_schema` 知道怎么填参数，按任务需要挑工具、定顺序、多次调用，最后汇总。

这样你永远拿到的是网关上**当前真实可用**的工具及其官方说明——新接入的数据源/工具无需更新本文档即可使用。

## 触发与编排

当用户输入含 `@<source>`（例如「使用 @sif 帮我调研 B0CP9Z56SW」），你应当：

1. **理解任务**：用户想要什么结论（广告诊断 / 关键词机会 / 流量异常 / 销量趋势 / 综合调研 …）。
2. **发现工具**：`providers` 确认 `<source>` 可用 → `list-tools --provider <source>` 拿到该源全部工具及说明。
3. **自由编排**：从工具清单里挑合适的，按需多次调用。一般思路——
   - 综合调研一个对象：先用「结构/概览类」工具看全貌 → 再按需下钻「趋势类 / 明细类」工具 → 需要时用「诊断/分析类」工具。
   - 具体用哪些工具、什么顺序，**完全依据 `list-tools` 返回的 `description` 自己判断**，不要套用固定工具名。
4. **每个工具调一次 CLI**（同步、秒级返回单工具结果）：
   ```bash
   python3 <skill>/scripts/dinzee.py call <tool_name> --args '<json>'
   ```
5. **汇总**：把多次调用的 JSON 结果整合成一份给用户的结论（不要把原始 JSON 直接丢给用户）。

每次「可扣点」工具调用都会从用户积分扣除对应点数（单价见 `list-tools` 的 `points_cost`）。

## CLI 速查

```bash
# 列出当前已开放的数据源（不扣点）
python3 <skill>/scripts/dinzee.py providers

# 列出某数据源的全部工具，带 description / input_schema / points_cost（不扣点）
python3 <skill>/scripts/dinzee.py list-tools --provider <source>

# 查看单个工具是否可用 / 是否扣点
python3 <skill>/scripts/dinzee.py describe <tool>

# 调用工具（JSON 入参）
python3 <skill>/scripts/dinzee.py call <tool> --args '<json>'

# 调用结果默认保存到 /opt/data/.dinzee/data/<provider>/<tool>/
# 如本次不需要落盘
python3 <skill>/scripts/dinzee.py call <tool> --no-save --args '<json>'

# 大入参从 stdin 读（heredoc）
python3 <skill>/scripts/dinzee.py call <tool> --stdin <<'EOF'
{"asin": "B0CP9Z56SW", "marketplace": "US"}
EOF

# 原始 JSON 输出（便于你程序化解析后再汇总）
python3 <skill>/scripts/dinzee.py --format json call <tool> --args '{...}'

# 耗时较长的工具可调大超时（秒）
python3 <skill>/scripts/dinzee.py call <tool> --timeout 300 --args '{...}'

# 根据本地落盘文件查询网关中已持久化的原调用记录
python3 <skill>/scripts/dinzee.py trace /opt/data/.dinzee/data/<provider>/<tool>/<record>.json

# token 状态
python3 <skill>/scripts/dinzee.py status

# 一键安装/更新 Dinzee 官方业务 skill 包
python3 <skill>/scripts/dinzee.py sync-skills
```

## MCP 调用结果落盘与溯源

- `call` 收到 HTTP 200 响应后，默认将完整请求、响应及溯源 ID 原子写入 JSON 文件。
- 数据根目录、provider/tool 子目录均显式设置为 `0777`；数据 JSON 设置为 `0666`，不受容器 `umask` 影响。
- 凭证文件不使用开放权限，始终保持 `0600`。
- 默认路径为 `/opt/data/.dinzee/data/<provider>/<tool>/`；文件中不保存用户 token。
- 保存提示输出到 stderr，不会污染 `--format json` 的 stdout。
- `trace <path>` 优先使用文件中的 `call_id` 查询
  `GET /v1/mcp/calls/{call_id}`；没有 `call_id` 或该记录返回 404 时，使用
  `GET /v1/mcp/calls/lookup?idempotencyKey=...`。
- `trace` 只读取网关已持久化的调用记录，不会重新调用 Provider，不扣点，也不退款。

## 错误处理

| HTTP | code | 含义 / 处理 |
|---:|---|---|
| 401 | `USER_INTEGRATION_TOKEN_REQUIRED` | 没传 token；CLI 会自动带，通常是 token 没配，跑 `status` 检查 |
| 401 | `USER_INTEGRATION_TOKEN_INVALID` | token 错或过期，让用户重新取一个 |
| 402 | `INSUFFICIENT_POINTS` | 用户积分不足，提示充值 |
| 403 | `MCP_PROVIDER_NOT_ALLOWLISTED` / `MCP_TOOL_NOT_ALLOWLISTED` | provider/tool 名拼错，或该数据源/工具未在网关开放——用 `providers` / `list-tools` 确认当前可用 |
| 409 | `IDEMPOTENCY_CONFLICT` | 同 idempotencyKey 配了不同参数；CLI 默认随机 key，一般不会遇到 |
| 503 | `MCP_PROVIDER_UNAVAILABLE` | 上游不可达/鉴权失败，网关已记熔断 |
| 503 | `MCP_PROVIDER_CIRCUIT_OPEN` | 上游连续失败触发熔断，等几十秒重试 |

调用失败时读 error 详情，按上表调整或重试；不要把原始报错直接丢给用户，转述成可理解的提示。

## Examples

> 下列示例只示范**工作流程**，`<...>` 处的工具名/参数一律以 `list-tools` 的实时返回为准，不要照抄占位名。

### Example 1：综合调研一个 ASIN（典型 @<source> 编排）

用户：「使用 @sif 帮我调研 B0CP9Z56SW」。你应当：

```bash
# 1) 发现该源的工具
python3 <skill>/scripts/dinzee.py list-tools --provider sif
# 2) 读 description 选工具：先调「广告/流量结构概览」类工具看全貌
python3 <skill>/scripts/dinzee.py call <结构概览工具> --args '{"asin":"B0CP9Z56SW","marketplace":"US"}'
# 3) 按需下钻「趋势 / 关键词 / 明细」类工具
python3 <skill>/scripts/dinzee.py call <趋势或关键词工具> --args '{"asin":"B0CP9Z56SW","marketplace":"US"}'
# 4) 如怀疑异常，再调「诊断/分析」类工具
```
然后把多份结果整合成一份「结构 + 流量来源 + 关键词机会」的调研结论给用户。

### Example 2：关键词研究

```bash
python3 <skill>/scripts/dinzee.py list-tools --provider <source>
python3 <skill>/scripts/dinzee.py --format json call <关键词需求工具> --args '{"keyword":"wireless earbuds"}'
python3 <skill>/scripts/dinzee.py --format json call <关键词竞争工具> --args '{"keyword":"wireless earbuds"}'
```
对比需求强度与竞争程度，给出选词建议。

### Example 3：耗时较长的诊断类工具

```bash
python3 <skill>/scripts/dinzee.py call <诊断分析工具> --timeout 300 \
  --args '{"asin":"B0XXXXXXXX","marketplace":"US"}'
```
