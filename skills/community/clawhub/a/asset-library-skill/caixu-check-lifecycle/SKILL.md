---
name: caixu-check-lifecycle
description: "Check Document Renewal Requirements. Use when the user wants a lifecycle diagnosis for an existing asset library at the lifecycle stage, including “看未来 60 天续办”“查缺件”“判断能不能提交某个目标场景”. Prefer caixu-skill when the user asks for the full end-to-end mainline or is unsure which stage to run. This skill loads assets and a versioned RuleProfileBundle, asks an agent to produce a complete CheckLifecycleData decision, validates readiness and asset references with shared rules helpers, records an audit sidecar, and persists the lifecycle run only when the decision is structurally valid."
---

# Check Document Renewal Requirements

在用户要“看未来 60 天续办”“查缺件”“判断能不能提交某个目标场景”时使用这个 skill。

## Quick flow

1. 读取资产库和 `RuleProfileBundle`
2. 让 agent 产出完整 `CheckLifecycleData`
3. 校验、审计、持久化

## Read next only when needed

- 要确认 goals、默认值和 agent 主判顺序时，读 [references/workflow.md](references/workflow.md)
- 要确认 `CheckLifecycleData`、`readiness`、audit 字段时，读 [references/tool-contracts.md](references/tool-contracts.md)
- 要对齐 `CheckLifecycleData` 输出形状时，读 [references/output-patterns.md](references/output-patterns.md)
- 遇到 schema 冲突、未知 goal、readiness 不一致时，读 [references/failure-modes.md](references/failure-modes.md)

## Required tools

- `caixu-data-mcp.query_assets`
- `caixu-data-mcp.get_rule_profile`
- `caixu-data-mcp.write_lifecycle_run`

## Required input

- `library_id`
- `goal`
- `as_of_date`
- `window_days`
- `run_id`

## Workflow

1. 用 `goal` 读取 `get_rule_profile`，拿到 versioned `RuleProfileBundle`。
2. 调用 `query_assets` 读取当前库资产。
3. 把相对日期先解成绝对 `YYYY-MM-DD`。
4. 让 agent 直接产出完整 `CheckLifecycleData`。
5. 在持久化前运行 `scripts/validate-lifecycle-payload.mjs` 预检，并结合共享规则校验器确认：
   - schema 完整
   - `asset_id` 都存在
   - `readiness` 与 blocking/warning items 自洽
6. 只有通过校验的结果才调用 `write_lifecycle_run`，并附带 audit sidecar。
7. 成功后推荐下一步 `build-package`。

## Guardrails

- 不回退到旧 deterministic rule engine 作为主判来源。
- 未知 `goal` 必须结构化失败。
- 不得把 free text 建议当成 `readiness`。
- 校验失败时不得把结果写成正式 lifecycle run。
