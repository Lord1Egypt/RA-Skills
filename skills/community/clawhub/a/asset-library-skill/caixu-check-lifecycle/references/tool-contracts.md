# Tool Contracts

## Required objects

- `CheckLifecycleData`
- `RuleProfileBundle`
- `AgentDecisionAudit`

## CheckLifecycleData must include

- `library_id`
- `as_of_date`
- `window_days`
- `lifecycle_events`
- `rule_matches`
- `missing_items`
- `readiness`

## readiness constraints

- `readiness` 是唯一正式“是否可提交”来源
- `blocking_items` 与 `ready_for_submission` 必须一致
- 不能用自由文本代替结构化 readiness

## Audit rules

- 成功与失败都应生成结构化 audit
- 只有校验通过的结果能成为正式 lifecycle run
