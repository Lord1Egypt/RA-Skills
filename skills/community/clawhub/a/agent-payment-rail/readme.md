# Agent Payment Rail

[English](#english) | [中文](#chinese)

---

<a name="english"></a>

## English

### What is Agent Payment Rail?

**Agent Payment Rail** is a universal payment infrastructure for AI Agents. It provides a unified, type-safe API to integrate multiple payment providers into your agent applications, enabling seamless payment processing, transaction management, and refund handling.

### Why Use Agent Payment Rail?

#### 🌐 Multi-Provider Support
Integrate Stripe, PayPal, Alipay, and more through a single, consistent API. Switch providers or use multiple providers simultaneously without changing your code.

#### 💡 Agent-First Design
Built specifically for AI agents with:
- Natural language-friendly tool definitions
- Clear error messages for agent understanding
- Metadata support for context tracking
- Async-first architecture

#### 🔒 Type-Safe & Reliable
- Full TypeScript support
- Comprehensive input validation
- Detailed error handling
- Production-ready code

#### 🚀 Quick Integration
Get started in minutes with simple setup and clear documentation. No complex configuration required.

### Quick Start

#### 1. Install

```bash
npm install openclaw-agent-payment-rail
```

#### 2. Set API Keys

```bash
export STRIPE_API_KEY="sk_test_..."
```

#### 3. Use in Your Agent

```typescript
import { PaymentRail } from 'openclaw-agent-payment-rail';

const rail = new PaymentRail();

// Initialize
await rail.initialize({
  provider: 'stripe',
  apiKey: process.env.STRIPE_API_KEY,
});

// Create payment
const payment = await rail.createPayment({
  amount: 99.99,
  currency: 'USD',
  description: 'Premium subscription',
});

console.log(`Payment created: ${payment.transactionId}`);
```

### Key Features

#### Payment Operations

- **Create Payment** - Process one-time or recurring payments
- **Query Transaction** - Get real-time payment status
- **Refund Payment** - Full or partial refunds
- **Cancel Payment** - Cancel pending payments

#### Transaction Management

- Automatic transaction tracking
- Metadata support for custom data
- Multi-currency support (USD, EUR, GBP, CNY, JPY)
- Sandbox mode for testing

#### Agent Integration

- 4 ready-to-use tools for agent conversations
- Natural language-friendly responses
- Structured error handling
- Context preservation across interactions

### CLI Tool

Global command-line interface for quick operations:

```bash
# Install globally
npm install -g openclaw-agent-payment-rail

# Create payment
agent-payment-rail pay 99.99 USD --desc "Test payment"

# Check status
agent-payment-rail status pi_123456

# Refund
agent-payment-rail refund pi_123456
```

### Use Cases

#### E-commerce Agent
```typescript
// Agent processes customer purchases
const payment = await rail.createPayment({
  amount: orderTotal,
  currency: 'USD',
  description: `Order #${orderId}`,
  metadata: { orderId, customerId, items }
});
```

#### Subscription Service
```typescript
// Agent manages recurring subscriptions
const payment = await rail.createPayment({
  amount: 29.99,
  currency: 'USD',
  description: 'Monthly Pro subscription',
  metadata: { plan: 'pro', userId }
});
```

#### Refund Automation
```typescript
// Agent handles refund requests
const refund = await rail.refund({
  transactionId: payment.transactionId,
  reason: 'Product quality issue',
});
```

### Supported Payment Providers

| Provider | Status | Features |
|----------|--------|----------|
| **Stripe** | ✅ Production Ready | All features supported |
| **PayPal** | 🚧 In Development | Coming soon |
| **Alipay** | 📋 Planned | Q2 2026 |
| **WeChat Pay** | 📋 Planned | Q2 2026 |

### Documentation & Resources

- **GitHub Repository**: https://github.com/ZhenRobotics/openclaw-agent-payment-rail
- **npm Package**: https://www.npmjs.com/package/openclaw-agent-payment-rail
- **API Documentation**: See GitHub README
- **Examples**: Check `examples/` directory

### Requirements

- Node.js >= 18.0.0
- Payment provider API keys (Stripe, etc.)
- TypeScript 5.x (for development)

### License

MIT License - Free to use for commercial and personal projects.

### Support

- **Issues**: https://github.com/ZhenRobotics/openclaw-agent-payment-rail/issues
- **Discussions**: https://github.com/ZhenRobotics/openclaw-agent-payment-rail/discussions

---

<a name="chinese"></a>

## 中文

### 什么是 Agent Payment Rail？

**Agent Payment Rail** 是一个为 AI Agent 设计的通用支付基础设施。它提供统一的、类型安全的 API，让你的 Agent 应用能够集成多个支付提供商，实现无缝的支付处理、交易管理和退款处理。

### 为什么使用 Agent Payment Rail？

#### 🌐 多提供商支持
通过单一、统一的 API 集成 Stripe、PayPal、支付宝等。无需更改代码即可切换提供商或同时使用多个提供商。

#### 💡 Agent 优先设计
专为 AI Agent 构建：
- 自然语言友好的工具定义
- Agent 易于理解的清晰错误消息
- 支持元数据以跟踪上下文
- 异步优先架构

#### 🔒 类型安全且可靠
- 完整的 TypeScript 支持
- 全面的输入验证
- 详细的错误处理
- 生产就绪代码

#### 🚀 快速集成
几分钟内即可开始使用，设置简单，文档清晰。无需复杂配置。

### 快速开始

#### 1. 安装

```bash
npm install openclaw-agent-payment-rail
```

#### 2. 设置 API 密钥

```bash
export STRIPE_API_KEY="sk_test_..."
```

#### 3. 在 Agent 中使用

```typescript
import { PaymentRail } from 'openclaw-agent-payment-rail';

const rail = new PaymentRail();

// 初始化
await rail.initialize({
  provider: 'stripe',
  apiKey: process.env.STRIPE_API_KEY,
});

// 创建支付
const payment = await rail.createPayment({
  amount: 99.99,
  currency: 'USD',
  description: '高级订阅',
});

console.log(`支付已创建：${payment.transactionId}`);
```

### 核心功能

#### 支付操作

- **创建支付** - 处理一次性或定期付款
- **查询交易** - 获取实时支付状态
- **退款** - 全额或部分退款
- **取消支付** - 取消待处理的支付

#### 交易管理

- 自动交易跟踪
- 支持自定义数据的元数据
- 多币种支持（USD、EUR、GBP、CNY、JPY）
- 沙盒模式用于测试

#### Agent 集成

- 4 个即用型工具供 Agent 对话使用
- 自然语言友好的响应
- 结构化错误处理
- 跨交互保持上下文

### CLI 工具

全局命令行界面用于快速操作：

```bash
# 全局安装
npm install -g openclaw-agent-payment-rail

# 创建支付
agent-payment-rail pay 99.99 USD --desc "测试支付"

# 查看状态
agent-payment-rail status pi_123456

# 退款
agent-payment-rail refund pi_123456
```

### 使用场景

#### 电商 Agent
```typescript
// Agent 处理客户购买
const payment = await rail.createPayment({
  amount: orderTotal,
  currency: 'USD',
  description: `订单 #${orderId}`,
  metadata: { orderId, customerId, items }
});
```

#### 订阅服务
```typescript
// Agent 管理定期订阅
const payment = await rail.createPayment({
  amount: 29.99,
  currency: 'USD',
  description: '月度专业版订阅',
  metadata: { plan: 'pro', userId }
});
```

#### 退款自动化
```typescript
// Agent 处理退款请求
const refund = await rail.refund({
  transactionId: payment.transactionId,
  reason: '产品质量问题',
});
```

### 支持的支付提供商

| 提供商 | 状态 | 功能 |
|--------|------|------|
| **Stripe** | ✅ 生产就绪 | 支持所有功能 |
| **PayPal** | 🚧 开发中 | 即将推出 |
| **支付宝** | 📋 计划中 | 2026年Q2 |
| **微信支付** | 📋 计划中 | 2026年Q2 |

### 文档与资源

- **GitHub 仓库**: https://github.com/ZhenRobotics/openclaw-agent-payment-rail
- **npm 包**: https://www.npmjs.com/package/openclaw-agent-payment-rail
- **API 文档**: 见 GitHub README
- **示例**: 查看 `examples/` 目录

### 系统要求

- Node.js >= 18.0.0
- 支付提供商 API 密钥（Stripe 等）
- TypeScript 5.x（用于开发）

### 许可证

MIT 许可证 - 可免费用于商业和个人项目。

### 支持

- **问题反馈**: https://github.com/ZhenRobotics/openclaw-agent-payment-rail/issues
- **讨论**: https://github.com/ZhenRobotics/openclaw-agent-payment-rail/discussions
