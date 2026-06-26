---
name: ctx-usage
description: Check current session's context window usage. Shows model name, estimated token usage, and context window utilization percentage. Use when user asks about context window, token usage, context usage rate, context remaining, "how full is the context", or any question about how much of the model's context is being used.
---

# Context Window Usage

## How to Check

1. Call `session_status` to get current session info
2. Extract the `📚 Context:` line for usage data
3. Present a clean summary to the user

## Output Format

```
📊 Context Window
Model: <model_name>
Used: <used> / <total> (<percent>%)
Cache: <cache_hit>% hit · <cached_tokens> cached
Status: 🟢 Comfortable | 🟡 Getting Full | 🔴 Near Limit
```

## Thresholds

| Usage | Status | Action |
|---|---|---|
| <50% | 🟢 Comfortable | No action needed |
| 50-70% | 🟡 Getting Full | Monitor |
| 70-85% | 🟠 Consider compact | Suggest `/compact` |
| >85% | 🔴 Near limit | Recommend `/compact` |

## Notes

- `session_status` provides exact context data via the `📚 Context:` field
- Token counts and cache hit rates are also available
- If usage is high, suggest running `op-helper` skill for `/compact`
