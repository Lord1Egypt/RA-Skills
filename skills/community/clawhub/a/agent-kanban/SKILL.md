---
name: agent-kanban
description: OpenClaw Agent Dashboard - A Bloomberg Terminal-style web interface for real-time monitoring of all Agent status, session history, and session file sizes. Use this skill when users need to monitor agents, view agent status, or deploy a kanban dashboard.
---

# Agent Kanban

OpenClaw Agent Dashboard - Bloomberg Terminal Style Interface.

## Features

- **Real-time Monitoring** - View all Agent online status and last active time
- **Auto Grouping** - Group by project prefix (main, pmo, alpha, beta)
- **Heartbeat Display** - Show agent heartbeat interval from openclaw.json
- **Session History** - Click cards to view recent conversation history
- **File Viewer** - View Agent's OKR.md, SOUL.md, HEARTBEAT.md
- **Session Size Monitor** - Display .jsonl file size with threshold warnings
- **Send Message** - Send messages to agents directly from the UI
- **Font Size Control** - 10px-24px with reset button (R)
- **Bloomberg Style** - Bloomberg Terminal style interface
- **Auto Config Reload** - Hot reload when openclaw.json changes
- **Configurable Timeouts** - All timeouts and paths configurable via config.js

## Tech Stack

- **Backend**: Node.js + Express
- **Frontend**: React 18 (CDN)
- **Avatar**: DiceBear Pixel Art API
- **API**: OpenClaw Gateway HTTP API

## Quick Start

### 1. Deploy

```bash
# Copy project to destination
cp -r assets/agent-kanban /path/to/destination/
cd /path/to/destination/agent-kanban

# Install dependencies
npm install
```

### 2. Start (No Manual Config Needed!)

```bash
# Ensure Gateway is running
openclaw gateway start

# Start Kanban
npm start

# Access
# http://localhost:3100
```

**Gateway Token is auto-loaded from `~/.openclaw/openclaw.json`** - no manual configuration required!

### 3. (Optional) Custom Config

```bash
cp config.js config.local.js
# Edit config.local.js if needed
```

Config options:

```javascript
module.exports = {
  server: { port: 3100, host: '0.0.0.0' },
  gateway: {
    url: 'http://127.0.0.1:18789',
    token: ''  // Leave empty to auto-load from openclaw.json
  },
  openclaw: {
    homeDir: '.openclaw',
    configFilename: 'openclaw.json',
    binPath: '/home/dyh/.nvm/versions/node/v22.18.0/bin/openclaw',
    nodePath: '/home/dyh/.nvm/versions/node/v22.18.0/bin'
  },
  timeout: {
    gatewayHealth: 5000,
    gatewayInvoke: 30000,
    sendMessage: 120
  },
  frontend: {
    refreshInterval: 30000,
    highlightThreshold: 60000,
    activeThreshold: 300000
  },
  refreshInterval: 60000,
  sessionSizeThresholds: { warning: 500, danger: 1024 }
};
```

## Prerequisites

1. OpenClaw installed and running
2. Gateway started (`openclaw gateway start`)
3. Node.js 18+ installed

## UI Operations

| Action | Description |
|--------|-------------|
| Click agent card | View details (files + messages) |
| `-` / `+` button | Adjust font size (10-24px) |
| `R` button | Reset font size to 13px |
| `CLOSE` button | Close agent + hide right panel |
| `HIDE` button | Hide right panel |
| Input box + SEND | Send message to selected agent |

## Send Message to Agent

Click on an agent card, then use the input box at the bottom of the right panel to send messages directly to the agent.

- Uses `openclaw agent --agent <id> --message <msg>` CLI command
- Message appears in agent's session history
- Agent responds based on its role and context

## Error Handling

| Error | Code | Solution |
|-------|------|----------|
| Gateway 未启动 | `GATEWAY_NOT_RUNNING` | Run `openclaw gateway start` |
| Gateway 响应超时 | `GATEWAY_TIMEOUT` | Check Gateway health |
| Gateway Token 无效 | `TOKEN_INVALID` | Check token in openclaw.json |
| Gateway Token 未配置 | `TOKEN_MISSING` | Run `openclaw wizard` |
| 网络错误 | `NETWORK_ERROR` | Check network connection |

## Security

- **Local Access Only**: Gateway URL must be localhost or private IP
- **CORS Protected**: Only allows requests from localhost:3100
- **Token Validation**: Validates Gateway token before API calls

## Get Gateway Token

```bash
# Method 1: From config file
cat ~/.openclaw/openclaw.json | jq '.gateway.auth.token'

# Method 2: From CLI
openclaw gateway status
```

---

# Agent Kanban（中文）

OpenClaw Agent 状态监控面板 - Bloomberg Terminal 风格界面。

## 功能特性

- **实时监控** - 显示所有 Agent 的在线状态、最后活跃时间
- **自动分组** - 按项目前缀自动分组（main、pmo、alpha、beta）
- **心跳显示** - 从 openclaw.json 读取并显示 Agent 心跳间隔
- **会话历史** - 点击卡片查看最近的对话记录
- **文件查看** - 查看 Agent 的 OKR.md、SOUL.md、HEARTBEAT.md
- **Session 大小监控** - 显示 .jsonl 文件大小，超过阈值高亮警告
- **发送消息** - 直接从界面给 Agent 发送消息
- **字号调节** - 10px-24px，带重置按钮
- **彭博风格** - Bloomberg Terminal 风格界面
- **配置热更新** - 自动检测 openclaw.json 变化并重新加载
- **可配置超时** - 所有超时和路径可通过 config.js 配置

## 快速开始

### 1. 部署

```bash
cp -r assets/agent-kanban /path/to/destination/
cd /path/to/destination/agent-kanban
npm install
```

### 2. 启动（无需手动配置！）

```bash
openclaw gateway start
npm start
# 访问 http://localhost:3100
```

**Gateway Token 自动从 `~/.openclaw/openclaw.json` 读取，无需手动配置！**

## 获取 Gateway Token

```bash
cat ~/.openclaw/openclaw.json | jq '.gateway.auth.token'
```

## Changelog

### 2026-03-31

- **New Feature**: Send message to agent from UI
- **New Feature**: `/api/config` endpoint for frontend configuration
- **Improvement**: All hardcoded values moved to config.js
- **Fix**: File expand height improved

---

## More Documentation

See `references/README.md` for full documentation.