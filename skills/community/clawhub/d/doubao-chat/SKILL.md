---
name: doubao-chat
description: 豆包大模型对话（免费 API，支持联网搜索）
homepage: https://www.doubao.com
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["curl","node"]}}}
---

# 豆包聊天

使用豆包免费 API 进行对话，支持联网搜索。

## 环境变量

```bash
DOUBAO_SESSIONID=your_sessionid
```

## 使用方法

```bash
node scripts/chat.js "你好"
```

## API 端点

对话补全：POST https://doubao-free-api.vercel.app/v1/chat/completions
