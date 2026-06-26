# Emergency Circuit - SKILL Documentation

**The Kill Switch for Rogue Agents** | **失控 AI 代理的紧急断路器**

---

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## 🇬🇧 English

### SKILL Name

**emergency-circuit** - AI Agent Safety Monitor

### Category

AI Safety / Agent Monitoring / DevOps

### Tagline

The Kill Switch for Rogue Agents

### Description

Emergency Circuit is a production-ready safety system that monitors AI agents in real-time and provides emergency shutdown capabilities. It implements the circuit breaker pattern to automatically detect and halt runaway agents before they cause damage.

### When to Use This SKILL

Use Emergency Circuit when you need to:

- ✅ **Monitor AI agents** - Track resource usage, API calls, and costs
- ✅ **Enforce safety policies** - Set hard limits on agent behavior
- ✅ **Prevent runaway costs** - Auto-kill when budget exceeded
- ✅ **Detect anomalies** - Identify suspicious behavioral patterns
- ✅ **Test safely** - Sandbox mode for development
- ✅ **Production monitoring** - Enterprise-grade agent oversight

### Core Capabilities

#### 1. Real-time Monitoring
- Track API calls, token consumption, and execution time
- Monitor costs across providers (OpenAI, Anthropic, etc.)
- Session-based statistics and health scores

#### 2. Circuit Breaker
- Three states: CLOSED (normal), OPEN (halted), HALF_OPEN (testing)
- Automatic failure detection and recovery
- Configurable trip thresholds

#### 3. Policy Engine
- Resource limit enforcement (API calls, tokens, cost)
- Action whitelisting and blacklisting
- Anomaly detection with configurable sensitivity

#### 4. Emergency Controls
- Instant kill switch
- Pause/resume capabilities
- Manual override controls

### Command Reference

```bash
# Monitor an agent
emergency-circuit monitor --agent-id <id> [--policy <path>]

# Emergency kill
emergency-circuit kill --agent-id <id> [--reason <text>]

# Check status
emergency-circuit status [agent-id]

# View logs
emergency-circuit logs --agent-id <id> [--last <duration>]

# List all agents
emergency-circuit list

# Validate policy
emergency-circuit policy validate --policy <path>

# View incidents
emergency-circuit incidents [--last <duration>]
```

### Safety Policies

Create custom policies or use pre-configured templates:

```json
{
  "limits": {
    "max_api_calls_per_minute": 100,
    "max_tokens_per_hour": 1000000,
    "max_cost_per_day": 100.0
  },
  "allowed_actions": ["read_file", "api_call"],
  "blocked_actions": ["execute_shell", "delete_database"],
  "anomaly_detection": {
    "enabled": true,
    "sensitivity": "medium",
    "alert_threshold": 0.8
  },
  "circuit_breaker": {
    "enabled": true,
    "trip_threshold": 5,
    "reset_timeout": 300
  }
}
```

### Integration Example

```typescript
import { AgentMonitor } from 'emergency-circuit';

// Create monitor
const monitor = new AgentMonitor(agent, policy);

// Start monitoring
await monitor.start();

// Track actions
await monitor.trackAction({
  action_type: 'api_call',
  resource_usage: { tokens: 1000 },
  cost: 0.03
});

// Emergency stop
await monitor.kill('Budget exceeded');
```

### Use Cases

#### Development & Testing
```bash
# Test with strict sandbox limits
emergency-circuit monitor --agent-id test-agent --sandbox
```

#### Production Monitoring
```bash
# Monitor with production policy
emergency-circuit monitor \
  --agent-id prod-agent \
  --policy ./policies/production.json
```

#### Cost Control
```bash
# Auto-kill on budget exceeded
emergency-circuit monitor \
  --agent-id expensive-agent \
  --policy ./policies/low-cost.json
```

### Troubleshooting

**Q: Agent keeps getting killed**
- Check policy limits in your policy file
- Review logs: `emergency-circuit logs --agent-id <id>`
- Try sandbox mode for testing

**Q: How to reset circuit breaker**
- Circuit auto-resets after timeout
- Or restart monitoring session

**Q: Policy validation failed**
- Use: `emergency-circuit policy validate --policy <path>`
- Check JSON syntax and required fields

### Requirements

- Node.js ≥18.0.0
- TypeScript 5.7+ (for development)
- Git (for installation from source)

### Installation

```bash
# From ClawHub
clawhub install emergency-circuit

# From npm
npm install -g openclaw-emergency-circuit

# From GitHub
git clone https://github.com/ZhenRobotics/openclaw-emergency-circuit.git
```

### Support

- **GitHub Issues**: https://github.com/ZhenRobotics/openclaw-emergency-circuit/issues
- **Documentation**: See README.md and QUICKSTART.md
- **Examples**: Check `examples/` directory

### License

MIT License - Free for commercial and personal use

---

<a name="chinese"></a>
## 🇨🇳 中文

### 技能名称

**emergency-circuit** - AI 代理安全监控器

### 分类

AI 安全 / 代理监控 / DevOps

### 标语

失控 AI 代理的紧急断路器

### 描述

Emergency Circuit 是一个生产就绪的安全系统，可实时监控 AI 代理并提供紧急关闭功能。它实现了断路器模式，可在失控代理造成损害之前自动检测并终止它们。

### 何时使用此技能

在以下情况下使用 Emergency Circuit：

- ✅ **监控 AI 代理** - 追踪资源使用、API 调用和成本
- ✅ **执行安全策略** - 对代理行为设置硬性限制
- ✅ **防止成本失控** - 超出预算时自动终止
- ✅ **检测异常** - 识别可疑的行为模式
- ✅ **安全测试** - 开发时使用沙箱模式
- ✅ **生产监控** - 企业级代理监督

### 核心能力

#### 1. 实时监控
- 追踪 API 调用、Token 消耗和执行时间
- 监控跨提供商的成本（OpenAI、Anthropic 等）
- 基于会话的统计和健康评分

#### 2. 断路器
- 三种状态：CLOSED（正常）、OPEN（暂停）、HALF_OPEN（测试）
- 自动故障检测和恢复
- 可配置的触发阈值

#### 3. 策略引擎
- 资源限制执行（API 调用、Token、成本）
- 操作白名单和黑名单
- 可配置灵敏度的异常检测

#### 4. 紧急控制
- 即时终止开关
- 暂停/恢复功能
- 手动覆盖控制

### 命令参考

```bash
# 监控代理
emergency-circuit monitor --agent-id <id> [--policy <path>]

# 紧急终止
emergency-circuit kill --agent-id <id> [--reason <text>]

# 检查状态
emergency-circuit status [agent-id]

# 查看日志
emergency-circuit logs --agent-id <id> [--last <duration>]

# 列出所有代理
emergency-circuit list

# 验证策略
emergency-circuit policy validate --policy <path>

# 查看事件
emergency-circuit incidents [--last <duration>]
```

### 安全策略

创建自定义策略或使用预配置模板：

```json
{
  "limits": {
    "max_api_calls_per_minute": 100,
    "max_tokens_per_hour": 1000000,
    "max_cost_per_day": 100.0
  },
  "allowed_actions": ["read_file", "api_call"],
  "blocked_actions": ["execute_shell", "delete_database"],
  "anomaly_detection": {
    "enabled": true,
    "sensitivity": "medium",
    "alert_threshold": 0.8
  },
  "circuit_breaker": {
    "enabled": true,
    "trip_threshold": 5,
    "reset_timeout": 300
  }
}
```

### 集成示例

```typescript
import { AgentMonitor } from 'emergency-circuit';

// 创建监控器
const monitor = new AgentMonitor(agent, policy);

// 开始监控
await monitor.start();

// 追踪操作
await monitor.trackAction({
  action_type: 'api_call',
  resource_usage: { tokens: 1000 },
  cost: 0.03
});

// 紧急停止
await monitor.kill('超出预算');
```

### 使用场景

#### 开发和测试
```bash
# 使用严格的沙箱限制进行测试
emergency-circuit monitor --agent-id test-agent --sandbox
```

#### 生产监控
```bash
# 使用生产策略监控
emergency-circuit monitor \
  --agent-id prod-agent \
  --policy ./policies/production.json
```

#### 成本控制
```bash
# 超出预算时自动终止
emergency-circuit monitor \
  --agent-id expensive-agent \
  --policy ./policies/low-cost.json
```

### 故障排查

**问：代理不断被终止**
- 检查策略文件中的限制设置
- 查看日志：`emergency-circuit logs --agent-id <id>`
- 尝试沙箱模式进行测试

**问：如何重置断路器**
- 断路器会在超时后自动重置
- 或重新启动监控会话

**问：策略验证失败**
- 使用：`emergency-circuit policy validate --policy <path>`
- 检查 JSON 语法和必需字段

### 系统要求

- Node.js ≥18.0.0
- TypeScript 5.7+（用于开发）
- Git（用于从源代码安装）

### 安装

```bash
# 从 ClawHub 安装
clawhub install emergency-circuit

# 从 npm 安装
npm install -g openclaw-emergency-circuit

# 从 GitHub 安装
git clone https://github.com/ZhenRobotics/openclaw-emergency-circuit.git
```

### 技术支持

- **GitHub Issues**: https://github.com/ZhenRobotics/openclaw-emergency-circuit/issues
- **文档**: 查看 README.md 和 QUICKSTART.md
- **示例**: 查看 `examples/` 目录

### 许可证

MIT 许可证 - 可免费用于商业和个人用途

---

**Stay Safe. Stay in Control.** ⚡🛡️

**保持安全，保持控制。** ⚡🛡️
