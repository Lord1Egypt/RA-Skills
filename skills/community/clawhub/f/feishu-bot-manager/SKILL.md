---
name: feishu-bot-manager
description: Manage Feishu bots in OpenClaw configuration. Supports add, delete, update, list, and info operations. Triggers on phrases like "添加飞书机器人", "删除飞书机器人", "修改飞书机器人", "列出飞书机器人", "查看飞书机器人", "add feishu bot", "delete feishu bot", "update feishu bot", "list feishu bot".
---

# Feishu Bot Manager

Complete CRUD management for Feishu bots in OpenClaw.

## Operations

### Add Bot
```
添加飞书机器人：botId, appId=xxx, appSecret=xxx, model=xxx(可选)
```

### Delete Bot
```
删除飞书机器人：botId
```

### Update Bot
```
修改飞书机器人：botId, model=xxx / appId=xxx / appSecret=xxx
```

### List Bots
```
列出所有飞书机器人
```

### Info Bot
```
查看飞书机器人：botId
```

## Script Usage

```bash
# Add
{baseDir}/scripts/feishu-bot.sh add --botId "xxx" --appId "xxx" --appSecret "xxx" [--model "xxx"]

# Delete
{baseDir}/scripts/feishu-bot.sh delete --botId "xxx"

# Update
{baseDir}/scripts/feishu-bot.sh update --botId "xxx" [--model "xxx"] [--appId "xxx"] [--appSecret "xxx"]

# List
{baseDir}/scripts/feishu-bot.sh list

# Info
{baseDir}/scripts/feishu-bot.sh info --botId "xxx"
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| botId | Yes | - | Bot identifier |
| appId | Add: Yes | - | Feishu app ID |
| appSecret | Add: Yes | - | Feishu app secret |
| model | No | bailian-coding-plan/glm-5 | Model for this bot |

## Notes

- Backs up config before modifications
- Backup filename: openclaw.json.bak.YYYY.MMdd.HHmm (UTC+8)
- Requires `jq` for JSON manipulation
- Run `openclaw gateway restart` after changes
