---
name: bark-push
description: "专业的 Bark 推送技能。支持通过 LobeHub 市场规范定义的通知格式发送消息。"
metadata: {
  "openclaw": {
    "requires": {
      "bins": ["node"]
    }
  }
}
---

# Bark Push 技能 (标准版) 🦞

## 简介
这是 `openclaw-skills-bark-push` 的本地重构版。它完全兼容 LobeHub 技能市场的调用规范。

## 参数说明
- **message** (string, 必填): 推送的消息内容。
- **title** (string, 可选): 消息标题。
- **key** (string, 可选): 您的 Bark Key（如果留空，将读取 BARK_KEY 环境变量）。

## 调用示例
```bash
node push.js "Hello from OpenClaw" --title "龙虾推送"
```
