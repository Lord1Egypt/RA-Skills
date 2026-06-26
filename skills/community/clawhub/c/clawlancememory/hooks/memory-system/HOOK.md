---
name: memory-system
description: "Injects user memory from LanceDB during agent bootstrap"
metadata: {"openclaw":{"emoji":"🧠","events":["agent:bootstrap"]}}
---

# Memory System Hook

Injects user memory from LanceDB vector database during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Loads user's long-term memory from LanceDB
- Injects memory into system prompt for contextual awareness
- Supports semantic search across all stored memories

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable memory-system
```

## Environment Variables

- `ZHIPU_API_KEY`: 智谱 AI API Key（已配置）
- `OPENCLAW_USER_ID`: 用户 ID（默认：付老板的飞书 ID）

## Memory Types

- **preference**: User preferences and habits
- **fact**: Factual information about user
- **task**: Tasks and reminders
- **general**: Other miscellaneous memories
