---
name: agent-manager
description: Multi-Agent conversation management platform with Gemini-style UI. Manage all your OpenClaw agents in one place with image upload, chat history, and message isolation.
version: 1.0.0
author: MSK
license: MIT
tags: agent,management,chat,ui,gemini,multi-agent
homepage: https://clawhub.com
category: productivity
---

# Agent Manager - 多 Agent 对话管理平台

统一管理多个 OpenClaw Agent 的对话平台，支持文字 + 图片输入，对话历史自动保存。

## 🎯 功能亮点

- **多 Agent 管理** - 统一管理所有 Agent
- **Gemini 风格界面** - 现代化左右分栏设计
- **图片输入** - 支持拖拽上传、按钮选择
- **对话历史** - 自动保存，切换 Agent 不丢失
- **消息隔离** - 每个 Agent 独立对话历史
- **本地存储** - 数据保存在浏览器

## 🚀 快速开始

### 1. 安装依赖

```bash
cd agent-manager
npm install
```
## 配置

编辑 `config.json`:
```json
{
  "openclawToken": "你的 Operator Token"
}

### 2. 启动服务

```bash
node server-gemini.js
```
** 修复 Shell 执行:**

在 `server-gemini.js` 中，使用参数化命令:
```javascript
// 修复前 ❌
execCmd(`openclaw agent --agent ${agentId} --message "${message}"`)

// 修复后 ✅
const { exec } = require('child_process');
exec(`openclaw agent --agent ${agentId}`, (error, stdout, stderr) => {
  // 处理结果
});

### 3. 访问界面

```
http://localhost:3000
```

## 📋 使用说明
获取 GET Token:
cat ~/.openclaw/devices/paired.json | jq '.[].tokens.operator.token'

### 与 Agent 对话

1. 左侧选择 Agent
2. 右侧输入消息
3. 按 Enter 或点击发送

### 上传图片

1. 点击 📎 按钮
2. 或拖拽图片到输入框
3. 点击发送

## 🔒 安全说明

本技能需要访问:
- `~/.openclaw/agents` - Agent 配置
- `~/.openclaw/workspace-*` - Agent 工作区

请在使用前审查代码。

## 💰 付费说明

**价格:** $10 USD（一次性购买）

**支付:** PayPal (396554498@qq.com)

**包含:**
- ✅ 完整源代码
- ✅ 永久使用授权
- ✅ 基础技术支持

## 📄 许可

- ✅ 个人使用
- ✅ 商业使用
- ❌ 转售技能本身

---

**详细文档请查看 CLAWHUB.md**
