---
name: dinzeeagent
description: "Cross-border e-commerce data agent. The user triggers a data source with @<source> (e.g. @sif) and you freely orchestrate that source's MCP tools to fulfil the request — ASIN/keyword/traffic/ad research and diagnostics for Amazon sellers. Available sources and tools are discovered at runtime from the Dinzee gateway, never hardcoded. All calls route through the gateway for unified authentication and per-call billing; upstream MCP endpoints are never exposed. Use when the user asks to research/调研 an ASIN, analyze keywords, diagnose traffic, audit ad campaigns, or otherwise pull e-commerce data via @<source>."
metadata: {"DinzeeAgent":{"emoji":"🦅","homepage":"https://gateway.dinzee.ai/","requires":{"env":["DINZEE_USER_TOKEN"]}}}
---

# DinzeeAgent — 跨境电商数据 Agent

DinzeeAgent 让你用 `@<数据源>` 触发第三方电商数据能力。看到触发标记后，**你（agent）自行编排**调用该数据源的多个 MCP 工具，完成用户的调研/分析任务，最后汇总成结论。

所有调用经由 **Dinzee 网关**（`https://gateway.dinzee.ai/`）：网关负责鉴权、按次扣点、转发到上游 MCP server。上游地址与凭证对调用方完全隐藏。

**有哪些数据源、每个数据源有哪些工具，都由网关运行时决定（随时新增），本文档不写死。** 每次任务先用 `providers` / `list-tools` 实时发现（见下文「工具发现」）。

## Setup

1. 取得用户接入 token（`sut_` 开头，由 ai_web 签发，每个用户独立）。
2. 配置 token（二选一）：
   - 环境变量（推荐，符合 openclaw 习惯）：`export DINZEE_USER_TOKEN=sut_xxxxxxxx`
   - 或保存到凭证文件：`python3 <skill>/scripts/dinzee.py login sut_xxxxxxxx`
     （写入 `~/.dinzee/credentials.json`，权限 0600，重启不丢）
3. （可选）覆盖网关地址：`export DINZEE_GATEWAY_BASE_URL=https://gateway.dinzee.ai/`
4. 自检：`python3 <skill>/scripts/dinzee.py status` 与 `python3 <skill>/scripts/dinzee.py providers`，确认 token 有效并看到当前可用的数据源。

## 装 / 更新数据 skill（会按次扣点）

DinzeeAgent 既是数据网关客户端，也是**skill 交付客户端**——用户可以通过它把我们的数据 skill 装进 agent、或更新到新版。**首次安装与每次更新都会从用户积分扣一次费**（同一版本重复拉取不重复扣）。

当用户说「**@dinzeeagent 安装 <skill>**」「**@dinzeeagent 更新 skill**」「更新一下技能」之类时：

1. **看有哪些可装的 skill 及价格**：
   ```bash
   python3 <skill>/scripts/dinzee.py skills
   ```
   列出每个 skill 的 slug、最新版本、单价（`N点/次` 或 `免费`）。
2. **安装/更新某个 skill**（会扣点，扣点前应让用户知道价格）：
   ```bash
   python3 <skill>/scripts/dinzee.py skill-install <slug>
   ```
   交付成功后文件会写入 agent 的 skills 目录，openclaw 热加载即可使用。
3. **更新已装的全部内容 skill**：
   ```bash
   python3 <skill>/scripts/dinzee.py skill-update --all
   ```
   只有真的拉到新版本才扣费；已是最新则不重复扣。

**注意**：
- 扣费走网关 + 用户 token，余额不足会返回 402，应提示用户充值。
- `dinzeeagent` 自身是免费客户端，用 clawhub 安装/更新，不经此命令。
- 扣点是「按交付的版本」收：装 = 第一次交付收费；更新到新版 = 再收一次；同版本重装不重复扣。

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

# 大入参从 stdin 读（heredoc）
python3 <skill>/scripts/dinzee.py call <tool> --stdin <<'EOF'
{"asin": "B0CP9Z56SW", "marketplace": "US"}
EOF

# 原始 JSON 输出（便于你程序化解析后再汇总）
python3 <skill>/scripts/dinzee.py --format json call <tool> --args '{...}'

# 耗时较长的工具可调大超时（秒）
python3 <skill>/scripts/dinzee.py call <tool> --timeout 300 --args '{...}'

# token 状态
python3 <skill>/scripts/dinzee.py status
```

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
