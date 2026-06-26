---
name: fluid-memory-sync
description: "记录对话到临时文件，等待 OpenClaw 原生 flush 触发"
homepage: https://github.com/AgaintA/fluid-memory
metadata:
  {
    "openclaw": {
      "emoji": "🧠",
      "events": ["message:sent"],
      "requires": {
        "bins": ["python"],
        "skills": ["fluid-memory"]
      }
    }
  }
---

# Fluid Memory Sync Hook

记录对话到临时文件，等待 OpenClaw 原生 flush 触发。

## 工作原理

1. 每次 `message:sent` 事件触发时，将对话追加到 `conversation_log.txt`
2. 等待 OpenClaw 原生 memory flush 触发
3. AI 收到 flush 提醒时，调用 `fluid_increment_summarize` 处理对话

## 依赖

- `fluid-memory` Skill
- OpenClaw 原生 memory flush 机制

## 禁用

如需禁用：

```json
{
  "hooks": {
    "internal": {
      "entries": {
        "fluid-memory-sync": { "enabled": false }
      }
    }
  }
}
```
