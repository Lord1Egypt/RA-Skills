# Emergency Circuit ⚡

**The Kill Switch for Rogue Agents** | **失控 AI 代理的紧急断路器**

---

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## 🇬🇧 English

### Overview

Emergency Circuit is a comprehensive safety system for monitoring and emergency shutdown of AI agents. It provides real-time monitoring, anomaly detection, and instant kill switch capabilities to prevent runaway autonomous systems.

### Key Features

- **🚨 Emergency Kill Switch** - Instantly halt any rogue agent
- **📊 Real-time Monitoring** - Track API calls, tokens, costs, and behavior
- **⚡ Circuit Breaker** - Auto-disconnect on policy violations
- **🛡️ Policy Engine** - Enforce resource limits and safety rules
- **🔍 Anomaly Detection** - Identify suspicious patterns
- **💰 Cost Control** - Budget enforcement and spending alerts

### Quick Start

#### Installation

```bash
# From ClawHub
clawhub install emergency-circuit

# From npm
npm install -g openclaw-emergency-circuit
```

#### Basic Usage

```bash
# Start monitoring an agent
emergency-circuit monitor --agent-id my-agent

# Emergency stop
emergency-circuit kill --agent-id my-agent

# Check status
emergency-circuit status my-agent
```

### Safety Policies

Three pre-configured templates included:

**Default Policy**
- 100 API calls/minute
- 1M tokens/day
- $100/day budget

**Sandbox Policy**
- 10 API calls/minute
- 10K tokens/hour
- $5/day budget

**Production Policy**
- 200 API calls/minute
- 50M tokens/day
- $500/day budget

### Use Cases

- ✅ Prevent runaway AI agents
- ✅ Enforce resource and cost limits
- ✅ Monitor autonomous systems
- ✅ Detect anomalous behavior
- ✅ Protect against unintended actions

### Technical Details

- **Language**: TypeScript 5.7+
- **Runtime**: Node.js ≥18.0.0
- **Architecture**: Circuit breaker pattern with policy engine
- **License**: MIT

### Links

- **GitHub**: https://github.com/ZhenRobotics/openclaw-emergency-circuit
- **npm**: https://www.npmjs.com/package/openclaw-emergency-circuit
- **Documentation**: See README.md

---

<a name="chinese"></a>
## 🇨🇳 中文

### 概述

Emergency Circuit 是一个全面的 AI 代理安全系统，提供实时监控、异常检测和紧急停止功能，防止自主系统失控。

### 核心功能

- **🚨 紧急停止开关** - 立即终止任何失控代理
- **📊 实时监控** - 追踪 API 调用、Token、成本和行为
- **⚡ 断路器** - 违反策略时自动断开
- **🛡️ 策略引擎** - 强制执行资源限制和安全规则
- **🔍 异常检测** - 识别可疑模式
- **💰 成本控制** - 预算执行和支出警报

### 快速开始

#### 安装

```bash
# 从 ClawHub 安装
clawhub install emergency-circuit

# 从 npm 安装
npm install -g openclaw-emergency-circuit
```

#### 基本用法

```bash
# 开始监控代理
emergency-circuit monitor --agent-id my-agent

# 紧急停止
emergency-circuit kill --agent-id my-agent

# 检查状态
emergency-circuit status my-agent
```

### 安全策略

包含三个预配置模板：

**默认策略**
- 每分钟 100 次 API 调用
- 每天 100 万 Token
- 每天 $100 预算

**沙箱策略**
- 每分钟 10 次 API 调用
- 每小时 1 万 Token
- 每天 $5 预算

**生产策略**
- 每分钟 200 次 API 调用
- 每天 5000 万 Token
- 每天 $500 预算

### 使用场景

- ✅ 防止 AI 代理失控
- ✅ 执行资源和成本限制
- ✅ 监控自主系统
- ✅ 检测异常行为
- ✅ 防止意外操作

### 技术详情

- **语言**: TypeScript 5.7+
- **运行时**: Node.js ≥18.0.0
- **架构**: 断路器模式 + 策略引擎
- **许可**: MIT

### 相关链接

- **GitHub**: https://github.com/ZhenRobotics/openclaw-emergency-circuit
- **npm**: https://www.npmjs.com/package/openclaw-emergency-circuit
- **文档**: 查看 README.md

---

**Stay Safe. Stay in Control.** ⚡🛡️

**保持安全，保持控制。** ⚡🛡️
