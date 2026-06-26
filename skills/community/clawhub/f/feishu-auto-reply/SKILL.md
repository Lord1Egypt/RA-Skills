---
name: feishu-auto-reply
description: Feishu Auto Reply Bot - Automatic reply to Feishu messages based on rules
metadata:
  openclaw:
    requires:
      bins: []
---

# Feishu Auto Reply Bot

Automatic reply to Feishu messages based on custom rules, features:
- Keyword matching support
- Regular expression matching
- Multiple reply strategies
- Support for @mention only reply
- Working hours configuration
- Custom reply templates
- Support for rich text messages

## Usage

```bash
# Start auto reply service
openclaw feishu-auto-reply start --config ./config.yaml

# Test rule matching
openclaw feishu-auto-reply test --message "你好" --config ./config.yaml
```

## Configuration Example (config.yaml)
```yaml
rules:
  - keyword: "你好"
    reply: "你好！我是自动回复机器人，有什么可以帮你的？"
    match: contains
  - regex: "^(请假|休假)"
    reply: "请假请直接联系人事部门，谢谢！"
    only_mention: true
working_hours:
  - "9:00-18:00"
  - exclude_weekends: true
```

## Required Permissions
- `im:message:read`
- `im:message:send`
- `im:chat:read`
