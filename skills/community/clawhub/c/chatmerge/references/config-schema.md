# Config Schema

这个 skill 只推荐一套 canonical schema。只有当用户要复用配置、做自动化或 API 化调用时，再读取本文件。

## Canonical Config

```yaml
version: 1
objective: general_minutes

channels:
  - platform: telegram
    id: "-1001234567890"
    label: "Project Alpha"

time_window:
  type: full_input
  value: ""
  start: ""
  end: ""

analysis:
  summary_level: detailed
  language: zh-CN
  detect_sentiment: false
  detect_priority: true
  extract_entities: true
  reconstruct_threads: true
  deduplicate_cross_posts: true

filters:
  exclude_bots: true
  min_message_length: 2
  exclude_patterns: []
  include_users: []
  exclude_users: []

output:
  format: markdown
  include_quotes: true
  include_timestamps: true
  include_authors: true
  max_length: 5000
  sections:
    - executive_summary
    - key_discussions
    - decisions
    - action_items
    - risks
    - follow_ups

delivery:
  mode: return_only
  target: ""
  on_failure: return_inline
```

## Field Notes

- `objective`: `general_minutes`、`standup`、`exec_brief`、`customer_feedback` 任选其一
- `time_window.type`:
  - `full_input`：总结用户提供的全部消息
  - `relative`：使用 `value`，例如 `last_24h`、`last_7d`
  - `absolute`：使用 `start` 和 `end`
- `analysis.language` 指输出语言，不是输入语言
- `summary_level`: `brief` 适合日报，`detailed` 适合项目同步，`comprehensive` 适合周报或管理材料
- `delivery.mode` 默认 `return_only`；只有在当前环境明确具备发送能力时，才使用 `chat`、`webhook`、`doc`、`email`

## Safe Defaults

推荐默认值：

- `objective: standup` 用于团队日报和站会纪要
- `objective: exec_brief` 用于老板摘要，优先保留结论、风险和下一步
- `detect_sentiment: false`，除非用户明确要情绪或舆情视角
- `include_quotes: true`，但只引用高信号原句
- `max_length: 5000`，超长时优先保留摘要、决策和行动项

## Example Presets

### Daily Standup

```yaml
objective: standup
time_window:
  type: relative
  value: last_24h
analysis:
  summary_level: brief
output:
  format: markdown
```

### Executive Brief

```yaml
objective: exec_brief
time_window:
  type: relative
  value: last_7d
analysis:
  summary_level: comprehensive
output:
  include_quotes: false
```
