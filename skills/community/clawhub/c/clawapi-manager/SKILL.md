---
name: clawapi-manager
slug: clawapi-manager
version: 1.1.2
author: 2233admin
description: OpenClaw API management and cost optimization. Manages multi-provider keys, monitors costs, routes tasks intelligently, and provides automated failover. Use when managing API keys, tracking costs, or optimizing API spending. Triggers: "api key", "cost", "budget", "provider", "validate config", "fix config".
---

# ClawAPI Manager

> 🔧 Professional API management and cost optimization for OpenClaw deployments

[English](#english) | [中文](#中文)

---

## English

### Overview

ClawAPI Manager is an OpenClaw-native tool for managing API keys, monitoring costs, and optimizing API spending through intelligent routing. It saves 30-90% on API costs by automatically routing simple tasks to free models.

### Capabilities

- **Multi-Provider Management**: Manage keys for OpenAI, Anthropic, Google, and 40+ providers
- **Cost Tracking**: Real-time monitoring of API usage and spending
- **Smart Routing**: Automatically route tasks to cost-effective models
- **Key Health Monitoring**: Detect expired, rate-limited, or invalid keys
- **Config Validation**: Detect and auto-fix configuration issues
- **Budget Alerts**: Multi-channel notifications (Telegram, Discord, Slack, Feishu, QQ)
- **Automated Failover**: Round-robin key rotation with health checks

### How to Use

#### 1. Installation

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/2233admin/clawapi-manager.git
cd clawapi-manager
pip install -r requirements.txt
```

#### 2. Basic Commands

```bash
# List all providers
python3 claw_api_manager_central.py list

# Validate configuration
python3 claw_api_manager_central.py validate

# Auto-fix configuration issues
python3 claw_api_manager_central.py fix

# Update API key
python3 claw_api_manager_central.py update provider-name new-key

# Add new provider
python3 claw_api_manager_central.py add provider-name https://api.example.com sk-key anthropic-messages
```

#### 3. Configuration

```bash
# Create example configs
cp config/managed_keys_central.json.example config/managed_keys_central.json
cp config/openrouter_keys.json.example config/openrouter_keys.json

# Edit with your keys
nano config/managed_keys_central.json
```

### Example Usage

**Scenario 1: Validate Configuration**
```
User: "Check if my OpenClaw config is valid"
Assistant: [Runs validate command, reports issues]
```

**Scenario 2: Auto-Fix Issues**
```
User: "Fix my config errors"
Assistant: [Runs fix command, repairs common issues]
```

**Scenario 3: Add OpenRouter Key**
```
User: "Add this OpenRouter key: sk-or-v1-xxx"
Assistant: [Adds key, configures rotation]
```

### Scripts

- `claw_api_manager_central.py`: Main management CLI
- `lib/config_manager.py`: Configuration management core
- `lib/key_rotation.py`: Automated key rotation
- `lib/cost_monitor.py`: Cost tracking and reporting
- `lib/smart_router.py`: Intelligent task routing

### Limitations

- Requires Python 3.8+
- Only supports OpenClaw deployments
- Config validation covers common issues only
- Smart routing requires OpenRouter integration

### Troubleshooting

**Issue: "Unknown model" error**
- Run: `python3 claw_api_manager_central.py validate`
- Run: `python3 claw_api_manager_central.py fix`
- Restart gateway: `openclaw gateway restart`

**Issue: Key rotation not working**
- Check: `config/openrouter_keys.json` exists
- Verify: All keys have `enabled: true`
- Check logs: `~/.openclaw/logs/gateway.log`

---

## 中文

### 概述

ClawAPI Manager 是 OpenClaw 原生的 API 管理和成本优化工具。通过智能路由自动将简单任务分配给免费模型，节省 30-90% 的 API 成本。

### 功能

- **多 Provider 管理**：管理 OpenAI、Anthropic、Google 等 40+ 家 API 密钥
- **成本追踪**：实时监控 API 使用和花费
- **智能路由**：自动将任务路由到性价比最高的模型
- **密钥健康监控**：检测过期、限流或无效的密钥
- **配置验证**：检测并自动修复配置问题
- **预算告警**：多渠道通知（Telegram、Discord、Slack、飞书、QQ）
- **自动故障转移**：Round-robin 密钥轮换 + 健康检查

### 使用方法

#### 1. 安装

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/2233admin/clawapi-manager.git
cd clawapi-manager
pip install -r requirements.txt
```

#### 2. 基本命令

```bash
# 列出所有 providers
python3 claw_api_manager_central.py list

# 验证配置
python3 claw_api_manager_central.py validate

# 自动修复配置问题
python3 claw_api_manager_central.py fix

# 更新 API Key
python3 claw_api_manager_central.py update provider-name new-key

# 添加新 provider
python3 claw_api_manager_central.py add provider-name https://api.example.com sk-key anthropic-messages
```

#### 3. 配置

```bash
# 创建示例配置
cp config/managed_keys_central.json.example config/managed_keys_central.json
cp config/openrouter_keys.json.example config/openrouter_keys.json

# 编辑你的密钥
nano config/managed_keys_central.json
```

### 使用示例

**场景 1：验证配置**
```
用户："检查我的 OpenClaw 配置是否正确"
助手：[运行 validate 命令，报告问题]
```

**场景 2：自动修复**
```
用户："修复我的配置错误"
助手：[运行 fix 命令，修复常见问题]
```

**场景 3：添加 OpenRouter 密钥**
```
用户："添加这个 OpenRouter 密钥：sk-or-v1-xxx"
助手：[添加密钥，配置轮换]
```

### 脚本

- `claw_api_manager_central.py`：主管理 CLI
- `lib/config_manager.py`：配置管理核心
- `lib/key_rotation.py`：自动密钥轮换
- `lib/cost_monitor.py`：成本追踪和报告
- `lib/smart_router.py`：智能任务路由

### 限制

- 需要 Python 3.8+
- 仅支持 OpenClaw 部署
- 配置验证仅覆盖常见问题
- 智能路由需要 OpenRouter 集成

### 故障排除

**问题："Unknown model" 错误**
- 运行：`python3 claw_api_manager_central.py validate`
- 运行：`python3 claw_api_manager_central.py fix`
- 重启 gateway：`openclaw gateway restart`

**问题：密钥轮换不工作**
- 检查：`config/openrouter_keys.json` 是否存在
- 验证：所有密钥都有 `enabled: true`
- 查看日志：`~/.openclaw/logs/gateway.log`

---

**📖 详细文档**: [README.md](./README.md)  
**🐛 问题反馈**: [GitHub Issues](https://github.com/2233admin/clawapi-manager/issues)  
**🚀 快速开始**: 运行 `python3 claw_api_manager_central.py --help`
