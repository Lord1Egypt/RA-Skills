# Workflow

## Supported goals

- `summer_internship_application`
- `renew_contract`
- `expense_reimbursement`
- `scholarship_application`

## Default values

- `goal = summer_internship_application`
- `window_days = 60`
- `as_of_date = today's absolute date in YYYY-MM-DD`

## Sequential flow

1. `get_rule_profile`
2. `query_assets`
3. 规范化日期
4. agent 产出 `CheckLifecycleData`
5. 预检与验证
6. `write_lifecycle_run`

## Agent prompt context should include

- `goal`
- `as_of_date`
- `window_days`
- 资产摘要
- 选中的 `RuleProfileBundle`
