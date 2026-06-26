# Easy Mining Skill 🦐

**一句话管理 BTC 矿场** | **Manage BTC Mining Farms via Natural Language**

通过自然语言与 AI 对话，完成矿场日常运维，无需打开 App。  
Chat with AI in natural language to manage your BTC mining farm — no app required.

---

## 功能概览 | Features

| 功能 | Feature |
|------|---------|
| 矿场实时概况（在线数/总算力） | Real-time farm overview (online count / total hashrate) |
| 矿机实时状态（算力/温度/功耗） | Miner real-time status (hashrate / temp / power) |
| 异常矿机识别（离线/高温/故障） | Abnormal miner detection (offline / overheat / error) |
| 收益历史查询（日级 BTC 数据） | Revenue history (daily BTC earnings) |
| 批量运维操作（重启/调频/升级） | Batch operations (reboot / power mode / firmware) |
| 任务进度追踪 | Task progress tracking |

---

## 快速上手 | Quick Start

### 中文版

#### 第一步：获取 Nonce API Key

1. 访问 [https://app.nonce.app](https://app.nonce.app) 注册账号
2. 登录后进入 **Settings → API Keys → Generate New Key**
3. 复制生成的 Key（格式：`ak_XXXXXXXXXXXXXXXXXXXXXXXX`）

> ⚠️ Key 只显示一次，请立即保存！

#### 第二步：告诉 AI 你的 Key

```
"我的 Nonce API Key 是 ak_XXXXXXXXXX，帮我验证一下连接"
```

#### 第三步：用自然语言管理矿场

```
"帮我看一下矿场概况"
"现在有多少台矿机在线？"
"过去7天挖了多少 BTC？"
"有没有高温或离线的矿机？"
"重启那3台异常矿机"
```

---

### English Version

#### Step 1: Get Your Nonce API Key

1. Visit [https://app.nonce.app](https://app.nonce.app) and create an account
2. After login, go to **Settings → API Keys → Generate New Key**
3. Copy your API Key (format: `ak_XXXXXXXXXXXXXXXXXXXXXXXX`)

> ⚠️ The key is only shown once — save it immediately!

#### Step 2: Provide the Key to AI

```
"My Nonce API Key is ak_XXXXXXXXXX, please verify the connection"
```

#### Step 3: Manage Your Farm with Natural Language

```
"Show me my farm overview"
"How many miners are online right now?"
"What's my BTC earnings for the past 7 days?"
"Which miners are offline or overheating?"
"Reboot the 3 abnormal miners"
```

---

## 架构 | Architecture

```
用户 (User)
    ↓ 自然语言 / Natural Language
OpenClaw (AI Agent)
    ↓ MCP tool calls
Antalpha MCP Server
    ↓ MCP protocol (with Bearer auth)
Nonce MCP Server (mcp.nonce.app)
    ↓ Nonce API
矿机 / BTC Miners
```

- **API Key 不落库**：每次调用即用即弃，服务端不持久化  
  **Key never stored**: used per-request only, never persisted server-side
- **写操作二次确认**：重启/调频等操作必须用户确认后执行  
  **Write ops require confirmation**: reboot/power mode changes need explicit user approval

---

## 支持的任务类型 | Supported Task Types

| 任务 | `task_name` | 说明 |
|------|------------|------|
| 重启矿机 | `miner.system.reboot` | Reboot miners |
| 调整功耗 | `miner.power_mode.update` | Change power mode: `low_power` / `normal` / `high_power` |
| 固件升级 | `miner.firmware.update` | Firmware upgrade |
| 网络扫描 | `miner.network.scan` | Network scan |
| 矿池配置 | `miner.pool.config` | Update pool URL |
| 指示灯定位 | `miner.light.flash` | Flash LED to locate miner |

---

## 工具列表 | MCP Tools

| Tool Name | 说明 | Description |
|-----------|------|-------------|
| `easy-mining-get-workspace` | 验证 API Key，获取 Workspace 信息 | Verify API key and get workspace info |
| `easy-mining-list-farms` | 列出所有矿场 | List all mining farms |
| `easy-mining-list-agents` | 列出所有 Agent | List all Nonce agents |
| `easy-mining-list-miners` | 矿机实时状态 | Real-time miner status |
| `easy-mining-list-metrics-history` | 矿场历史收益（日级） | Farm metrics history (daily) |
| `easy-mining-list-pool-diffs` | 矿池变更记录 | Pool change records |
| `easy-mining-list-history` | 单台矿机历史数据 | Single miner historical data |
| `easy-mining-list-miner-tasks` | 矿机任务历史 | Miner task history |
| `easy-mining-list-task-batches` | 任务批次列表 | Task batch list |
| `easy-mining-create-task-batch` | ⚠️ 创建任务批次（写操作） | ⚠️ Create task batch (write op) |
| `easy-mining-get-task-batch` | 查询任务批次状态 | Get task batch status |

---

## 安装 | Installation

从 GitHub 直接安装 | Install directly from GitHub:

```bash
openclaw skill install https://github.com/AntalphaAI/easy-mining
```

或通过 OpenClaw 对话安装 | Or install via OpenClaw chat:

```
"安装 Easy Mining Skill"
```

---

## 数据来源 | Data Source

矿场数据由 [Nonce](https://app.nonce.app) 提供，通过其官方 MCP API 接入。  
Mining data is provided by [Nonce](https://app.nonce.app) via their official MCP API.

---

## 许可 | License

MIT © [Antalpha AI Team](https://www.antalpha.com/)
