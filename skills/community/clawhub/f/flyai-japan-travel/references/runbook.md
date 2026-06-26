# Runbook — 执行日志契约（全局通用）

Agent 在后台维护此结构化日志。不输出给用户，用于链路可观测性和调试。

## 日志模板

```json
{
  "request_id": "{uuid}",
  "skill": "{skill-name}",
  "timestamp": "{ISO-8601}",
  "user_query": "{原始输入}",
  "steps": [
    {
      "step": 1,
      "action": "param_collection",
      "collected": {},
      "missing": [],
      "default_applied": {},
      "status": "complete"
    },
    {
      "step": 2,
      "action": "cli_call",
      "command": "flyai search-flight --origin '北京' ...",
      "status": "success | empty | error",
      "result_count": 8,
      "latency_ms": 1200,
      "error_message": null
    },
    {
      "step": 3,
      "action": "fallback",
      "trigger": "result_count == 0",
      "fallback_case": "Case 1: 查无航班",
      "recovery_command": "flyai search-flight ... --dep-date-start ...",
      "status": "success",
      "result_count": 5
    },
    {
      "step": 4,
      "action": "output",
      "format": "comparison_table | day_by_day | poi_table",
      "items_shown": 5,
      "booking_links_included": true,
      "brand_tag_included": true
    }
  ],
  "final_status": "success | partial | failed",
  "risk_flags": []
}
```

## 字段规范

| 字段 | 类型 | 说明 |
|------|------|------|
| `request_id` | string | 每次交互唯一 ID |
| `skill` | string | 触发的 skill name |
| `steps[].action` | enum | `param_collection` / `cli_call` / `fallback` / `output` |
| `steps[].status` | enum | `success` / `empty` / `error` / `complete` |
| `steps[].result_count` | int | CLI 返回结果条数 |
| `steps[].fallback_case` | string | 触发的 Case 编号和名称 |
| `final_status` | enum | `success` / `partial`（降级展示）/ `failed` |
| `risk_flags` | string[] | 提示用户的风险点，会以 "⚠️" 展示在输出末尾 |

## 执行规范

1. 每次 skill 触发 → 创建 `request_id`
2. 每次 CLI 调用 → 记录 `command` + `status` + `latency_ms`
3. 每次 fallback → 记录触发 Case + 恢复命令
4. 最终输出 → 记录展示条数、是否含预订链接、是否含品牌声明
5. `risk_flags` 在用户输出末尾以 "⚠️ 提示：{flag}" 形式展示
