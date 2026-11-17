# ClawAPI Manager

> 🔧 Professional API management and cost optimization for OpenClaw deployments

[English](#english) | [中文](#中文)

---

## English

Professional API management and cost optimization for OpenClaw deployments.

### What It Does

Manages API keys, monitors costs, and routes tasks to the most cost-effective models automatically. Saves 30-90% on API costs through intelligent routing and free model integration.

Professional API management and cost optimization for OpenClaw deployments.

## What It Does

Manages API keys, monitors costs, and routes tasks to the most cost-effective models automatically. Saves 30-90% on API costs through intelligent routing and free model integration.

## Key Features

- **Smart Routing**: Automatically routes simple tasks to free models (Qwen, Llama) via OpenRouter
- **Cost Tracking**: Real-time monitoring of API usage and spending
- **Multi-Provider**: Supports OpenAI, Anthropic, Google, and 40+ providers
- **Budget Alerts**: Get notified before you exceed spending limits
- **Key Health**: Automatic detection of expired or rate-limited keys
- **Multi-Channel Alerts**: Telegram, Discord, Slack, Feishu, QQ, DingTalk

## Quick Start

```bash
# Install
cd ~/.openclaw/workspace/skills
git clone https://github.com/2233admin/clawapi-manager.git
cd clawapi-manager
pip install -r requirements.txt

# Configure notifications (optional)
cp config/notify.json.example config/notify.json
# Edit with your webhook URLs

# Test
python3 lib/cost_monitor.py health
```

## How It Saves Money

The system analyzes each task and routes it intelligently:

- **Simple tasks** (search, weather, translate) → Free models (100% savings)
- **Medium tasks** (summaries, basic code) → Cost-effective models (50-70% savings)
- **Complex tasks** (architecture, analysis) → Premium models (Opus, GPT-4)

### Example Savings

| Task Type | Before | After | Savings |
|-----------|--------|-------|---------|
| Weather check | $0.015 | $0.00 | 100% |
| Code review | $0.30 | $0.10 | 67% |
| Architecture design | $1.50 | $1.50 | 0% |

**Average savings: 30-90%** depending on your task mix.

## Configuration

### OpenRouter (Optional, for free models)

Add your OpenRouter key to `config/openrouter.json`:

```json
{
  "api_key": "sk-or-v1-YOUR_KEY_HERE"
}
```

Get a free key at [openrouter.ai](https://openrouter.ai)

### Notifications

Edit `config/notify.json`:

```json
{
  "telegram": {
    "enabled": true,
    "bot_token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
  }
}
```

## Usage

```bash
# Check system health
python3 lib/cost_monitor.py health

# Generate cost report
python3 lib/daily_report.py

# Route a task (returns recommended model)
python3 lib/task_delegation.py route "search weather in Tokyo"

# Check key health
python3 lib/key_health.py status

# Test notifications
python3 lib/notifier.py test
```

## Automation

Add to cron for automated monitoring:

```cron
# Daily cost report at 1 AM
0 1 * * * cd /path/to/clawapi-manager && python3 lib/daily_report.py

# Health check every 15 minutes
*/15 * * * * cd /path/to/clawapi-manager && python3 lib/cost_monitor.py health
```

## Architecture

```
ClawAPI Manager
├── lib/                    # Core modules
│   ├── cost_monitor.py     # Cost tracking
│   ├── task_delegation.py  # Smart routing
│   ├── notifier.py         # Alerts
│   ├── budget_alert.py     # Budget monitoring
│   └── key_health.py       # Key health checks
├── config/                 # Configuration
└── data/                   # Runtime data
```

## Requirements

- Python 3.8+
- OpenClaw (any recent version)
- Optional: OpenRouter API key (for free model routing)

## Security

- API keys are encrypted at rest (AES-256)
- Never commit keys to version control
- Use environment variables for production
- Review config examples before deployment

## License

MIT License - Free for personal and commercial use.

## Links

- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenRouter](https://openrouter.ai)
- [ClawHub](https://clawhub.com)

---

**Version**: 1.0.1  
**Last Updated**: 2026-03-02

## 模型切换（新功能）

集成自 openclaw-switch，提供安全的模型切换功能。

### 查看当前模型

```bash
python3 lib/model_switcher.py status
```

### 列出所有模型

```bash
python3 lib/model_switcher.py list
```

### 切换模型

```bash
# 通过编号切换
python3 lib/model_switcher.py switch 6

# 或通过模型 ID
python3 lib/model_switcher.py switch minimax/MiniMax-M2.5
```

### 特性

- ✅ 安全的 JSON 修改（防止格式错误）
- ✅ 显示 Fallback 链
- ✅ 自动重启 daemon
- ✅ 支持编号和 ID 两种方式


## 使用场景

### 场景 1：SSH/终端（推荐）
完整的 Textual TUI，支持鼠标和键盘交互。

```bash
ssh user@server
cd ~/.openclaw/workspace/skills/clawapi-manager
python3 clawapi-tui.py
```

### 场景 2：受限终端
Rich 交互式菜单，只支持键盘。

```bash
python3 clawapi-rich.py
```

### 场景 3：QQ/飞书等纯文字
使用 CLI 命令。

```bash
./clawapi status
./clawapi providers
./clawapi add-provider openai https://api.openai.com/v1 sk-xxx
```

### 场景 4：智能自动选择
自动检测环境并选择合适的界面。

```bash
python3 clawapi-ui.py
```

---

## 环境检测

| 环境 | 检测方式 | 使用界面 |
|------|---------|---------|
| SSH/终端 | `termios.tcgetattr()` | Textual TUI |
| 受限终端 | `sys.stdin.isatty()` | Rich 菜单 |
| QQ/飞书 | 非 TTY | CLI |

# ClawAPI Manager - 核心亮点

## 与 OpenClaw Switch 的对比

### OpenClaw Switch
> "The missing remote control for your AI Agents."

**定位**：模型切换工具

**核心功能**：
- 🚫 拒绝崩溃：Python 原生解析 JSON
- 📊 可视化 Failover：展示备份链
- 🚀 丝滑切换：数字编号快速切换
- 💓 路由透明：显示心跳和子智能体路由
- 🛡️ 极致安全：本地运行，Key 脱敏

---

### ClawAPI Manager
> "From Cost Optimization to Intelligent Orchestration"

**定位**：完整配置管理平台

## 独特亮点

### 1. 🎯 三合一管理
**OpenClaw Switch**：只管理模型切换  
**ClawAPI Manager**：Models + Channels + Skills 统一管理

### 2. 🌐 多界面适配
**OpenClaw Switch**：只有命令行  
**ClawAPI Manager**：
- Textual TUI（SSH/终端）
- Rich 菜单（受限终端）
- CLI（脚本）
- 对话式接口（QQ/飞书）

### 3. 🤖 AI 驱动
**OpenClaw Switch**：手动输入命令  
**ClawAPI Manager**：
- AI 复杂度预测（Qwen 0.5B）
- 自然语言操作
- 智能路由（自动选免费模型）

### 4. 🔗 通道管理（独有）
**OpenClaw Switch**：无  
**ClawAPI Manager**：
- QQ、企业微信、飞书、钉钉等通道配置
- 一键启用/禁用
- 批量管理

### 5. 📦 任务调度（独有）
**OpenClaw Switch**：无  
**ClawAPI Manager**：
- 多节点负载均衡
- 任务队列
- 失败重试
- 性能追踪

### 6. 💰 成本优化（独有）
**OpenClaw Switch**：无  
**ClawAPI Manager**：
- 智能路由（省钱 30-90%）
- 成本监控
- 预算预警

---

## 功能对比表

| 特性 | OpenClaw Switch | ClawAPI Manager |
|------|----------------|-----------------|
| 定位 | 模型切换工具 | 完整配置管理平台 |
| 功能范围 | 单一（模型） | 三合一（Models + Channels + Skills） |
| 界面 | CLI | TUI + Rich + CLI + 对话式 |
| 智能化 | 无 | AI 预测 + 自动路由 |
| 成本优化 | 无 | 监控 + 优化 |
| 多节点协作 | 无 | 任务调度 + 负载均衡 |
| 通道管理 | 无 | QQ/飞书/企业微信等 |
| 环境适配 | 终端 | SSH/QQ/飞书/脚本 |

---

## 核心差异

**OpenClaw Switch 是螺丝刀，ClawAPI Manager 是瑞士军刀。**

- **OpenClaw Switch**：专注于模型切换，简单高效
- **ClawAPI Manager**：全方位配置管理，智能协作

---

## 适用场景

### 选择 OpenClaw Switch
- 只需要切换模型
- 喜欢简单的命令行工具
- 不需要成本优化和多节点协作

### 选择 ClawAPI Manager
- 需要管理 Models、Channels、Skills
- 需要多种界面（TUI/CLI/对话式）
- 需要成本优化（省钱 30-90%）
- 需要多节点协作和任务调度
- 需要在 QQ/飞书等环境中使用

---

## 总结

ClawAPI Manager 不只是模型切换工具，而是：
- ✅ 完整的配置管理平台
- ✅ 智能的成本优化系统
- ✅ 强大的多节点协作框架
- ✅ 灵活的多界面适配方案

**从成本优化到智能编排，一站式解决方案。**

---

## 故障排查

遇到问题？查看 [故障排查指南](TROUBLESHOOTING.md)

常见问题：
- [错误码对照表](TROUBLESHOOTING.md#常见错误码)
- [协议不匹配](TROUBLESHOOTING.md#1-协议不匹配)
- [配置文件损坏](TROUBLESHOOTING.md#2-配置文件损坏)
- [API Key 失效](TROUBLESHOOTING.md#3-api-key-失效)

