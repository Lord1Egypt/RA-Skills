# Output Patterns

## Lifecycle decision response

返回值应收敛为完整 `CheckLifecycleData`，至少包含：

```json
{
  "lifecycle_run": {
    "run_id": "run_xxx",
    "library_id": "lib_xxx",
    "goal": "summer_internship_application",
    "as_of_date": "2026-03-31",
    "window_days": 60,
    "readiness": {
      "ready_for_submission": false,
      "blocking_items": [],
      "warning_items": [],
      "rationale": "..."
    }
  }
}
```

- `readiness` 只能来自 agent 主判后的结构化结果
- `blocking_items` 和 `warning_items` 要与 `ready_for_submission` 自洽
- 引用的 `asset_id` 必须存在于当前库
