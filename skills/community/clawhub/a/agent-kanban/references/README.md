# Agent Kanban

OpenClaw Agent Dashboard - Real-time monitoring of all Agent status and session history.

![Bloomberg Terminal Style](https://img.shields.io/badge/style-Bloomberg%20Terminal-orange)

## Features

- **Real-time Monitoring** - View all Agent online status and last active time
- **Auto Grouping** - Group by project prefix (main, pmo, alpha, beta)
- **Session History** - Click cards to view recent conversation history
- **File Viewer** - View Agent's OKR.md, SOUL.md, HEARTBEAT.md
- **Session Size Monitor** - Display .jsonl file size with threshold warnings
- **Font Size Control** - 10px-24px with reset button (R)
- **Bloomberg Style** - Bloomberg Terminal style interface

## Tech Stack

- **Backend**: Node.js + Express
- **Frontend**: React 18 (CDN)
- **Avatar**: DiceBear Pixel Art API
- **API**: OpenClaw Gateway HTTP API

---

## Agent Naming Convention

OpenClaw uses a unified Agent naming convention for easy management and extension.

### Naming Format

```
{project}-{role}-{number}
```

| Part | Description | Example |
|------|-------------|---------|
| `{project}` | Project/department prefix | `alpha`, `beta`, `pmo` |
| `{role}` | Role type | `pm`, `algo`, `sre` |
| `{number}` | Instance number (optional) | `1`, `2`, `3` |

### Project Prefixes

| Prefix | Meaning | Description |
|--------|---------|-------------|
| `main` | Main Agent | Entry Agent that talks directly to user |
| `pmo` | Project Management Office | Coordination, monitoring, auditing |
| `alpha` | Project Alpha | Example project Alpha |
| `beta` | Project Beta | Example project Beta |

### Role Types

| Role | Full Name | Responsibility |
|------|-----------|----------------|
| `pm` | Project Manager | Project manager, coordinate team |
| `sre` | Site Reliability Engineer | Operations engineer, monitor services |
| `researcher` | Researcher | Researcher, explore new directions |
| `algo` | Algorithm Engineer | Algorithm engineer, implement algorithms |
| `qa` | Quality Assurance | QA, audit and verify |
| `submitter` | Submitter | Submitter, submit tasks |
| `tracker` | Tracker | Tracker, monitor progress |
| `director` | Director | Director, manage overall |
| `auditor` | Auditor | Auditor, supervise and inspect |
| `clocksmith` | Clocksmith | Clocksmith, automation mechanisms |

---

## Quick Start

### Prerequisites

1. **Install OpenClaw**

```bash
npm install -g openclaw
```

2. **Initialize OpenClaw**

```bash
openclaw wizard
# or
openclaw gateway start
```

3. **Confirm Gateway is Running**

```bash
openclaw gateway status
```

### 1. Install Dependencies

```bash
cd agent-kanban/
npm install
```

### 2. Get Gateway Token

```bash
cat ~/.openclaw/openclaw.json | jq '.gateway.auth.token'
```

### 3. Configure

```bash
cp config.js config.local.js
# Edit config.local.js, fill in token
```

### 4. Start

```bash
npm start
# Access http://localhost:3100
```

---

## Gateway API Configuration

### Get Gateway Token

```bash
# Method 1: From config file
cat ~/.openclaw/openclaw.json | jq '.gateway.auth.token'

# Method 2: From CLI
openclaw gateway status

# Method 3: From Web UI
# http://localhost:18790 → Settings → API Tokens
```

### API Usage

```bash
curl -X POST http://127.0.0.1:18789/tools/invoke \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "sessions_list", "args": {}}'
```

---

## License

MIT

---

# Agent Kanban（中文）

OpenClaw Agent 状态监控面板 - 实时查看所有 Agent 的运行状态和会话历史。

## 功能

- **实时监控** - 显示所有 Agent 的在线状态、最后活跃时间
- **自动分组** - 按项目前缀自动分组（main、pmo、alpha、beta）
- **会话历史** - 点击卡片查看最近的对话记录
- **文件查看** - 查看 Agent 的 OKR.md、SOUL.md、HEARTBEAT.md 文件
- **Session 大小监控** - 显示每个 Agent 的 Session 文件大小
- **字号调节** - 支持调节所有文字的字号大小（10px-24px）
- **彭博风格** - Bloomberg Terminal 风格界面

## 快速开始

### 1. 安装依赖

```bash
cd agent-kanban/
npm install
```

### 2. 获取 Gateway Token

```bash
cat ~/.openclaw/openclaw.json | jq '.gateway.auth.token'
```

### 3. 配置

```bash
cp config.js config.local.js
# 编辑 config.local.js，填入 token
```

### 4. 启动

```bash
openclaw gateway start
npm start
# 访问 http://localhost:3100
```

## License

MIT