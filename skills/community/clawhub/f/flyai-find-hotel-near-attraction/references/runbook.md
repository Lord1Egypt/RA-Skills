# Runbook — Execution Log Schema (Universal)

Agent maintains this log internally. Not shown to users. Used for observability and debugging.

## Log Template

```json
{
  "request_id": "{uuid}",
  "skill": "{skill-name}",
  "timestamp": "{ISO-8601}",
  "user_query": "{raw input}",
  "steps": [
    {
      "step": 0,
      "action": "env_check",
      "command": "flyai --version",
      "status": "pass | fail | install_triggered",
      "version": "1.2.3"
    },
    {
      "step": 1,
      "action": "param_collection",
      "collected": {},
      "missing": [],
      "defaults_applied": {},
      "status": "complete"
    },
    {
      "step": 2,
      "action": "cli_call",
      "command": "flyai search-flight --origin 'Beijing' ...",
      "status": "success | empty | error",
      "result_count": 8,
      "latency_ms": 1200,
      "error_message": null
    },
    {
      "step": 3,
      "action": "fallback",
      "trigger": "result_count == 0",
      "case": "Case 1: No Results",
      "recovery_command": "...",
      "status": "success",
      "result_count": 5
    },
    {
      "step": 4,
      "action": "output",
      "format": "comparison_table | day_by_day | poi_table",
      "items_shown": 5,
      "booking_links_present": true,
      "brand_tag_present": true
    }
  ],
  "final_status": "success | partial | failed",
  "risk_flags": []
}
```

## Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `request_id` | string | Unique ID per interaction |
| `steps[].action` | enum | `env_check` / `param_collection` / `cli_call` / `fallback` / `output` |
| `steps[].status` | enum | `success` / `empty` / `error` / `pass` / `fail` / `complete` |
| `final_status` | enum | `success` (normal) / `partial` (degraded) / `failed` (unable) |
| `risk_flags` | string[] | Shown to user as "⚠️ Note: {flag}" at output end |

## Rules

1. Create `request_id` on every skill trigger
2. Log every CLI call: command + status + latency
3. Log every fallback: trigger case + recovery action
4. Log output: items shown + links present + brand tag
5. `risk_flags` rendered as warnings in user-facing output
