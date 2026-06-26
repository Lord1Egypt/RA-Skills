---
name: deepseek-chat
description: DeepSeek 官方 API 对话（免费/超便宜，支持中文）
homepage: https://platform.deepseek.com
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["curl"]}}}
---

# DeepSeek 聊天

DeepSeek 官方 API，支持中文对话、文件处理、联网搜索。

## 环境变量

```bash
DEEPSEEK_API_KEY=sk-xxx
```

## 使用方法

```bash
node scripts/chat.js "你好"
```

## 模型

- `deepseek-chat` - 通用对话
- `deepseek-coder` - 代码
- `deepseek-reasoner` - R1 深度思考

## 价格

超级便宜：
- 输入：¥0.27 / 百万 tokens
- 输出：¥1.10 / 百万 tokens
