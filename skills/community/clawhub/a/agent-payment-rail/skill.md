# Agent Payment Rail Skill

[English](#english) | [中文](#chinese)

---

<a name="english"></a>

## English

### Overview

**Agent Payment Rail** is a universal payment infrastructure skill for AI Agents. It provides a unified API to integrate multiple payment providers (Stripe, PayPal, etc.) into your agent applications.

### Features

- 🌐 **Multi-Provider Support** - Stripe, PayPal, and more
- 🔌 **Unified API** - Single interface for all payment providers
- 💰 **Complete Transaction Management** - Create, query, refund, cancel
- 🔒 **Type-Safe** - Full TypeScript support
- 🌍 **Multi-Currency** - USD, EUR, GBP, CNY, JPY

### Available Tools

#### 1. `create_payment`

Create a new payment transaction.

**Parameters:**
- `amount` (number, required) - Payment amount (e.g., 99.99)
- `currency` (string, required) - Currency code (USD, EUR, GBP, CNY, JPY)
- `description` (string, required) - Payment description
- `provider` (string, optional) - Payment provider (stripe, paypal)
- `metadata` (object, optional) - Additional metadata

**Example:**
```javascript
create_payment({
  amount: 99.99,
  currency: "USD",
  description: "Premium subscription",
  metadata: { userId: "user_123" }
})
```

#### 2. `get_transaction`

Get transaction status and details.

**Parameters:**
- `transaction_id` (string, required) - Transaction ID
- `provider` (string, optional) - Payment provider

**Example:**
```javascript
get_transaction({
  transaction_id: "pi_123456"
})
```

#### 3. `refund_payment`

Refund a payment transaction.

**Parameters:**
- `transaction_id` (string, required) - Transaction ID to refund
- `amount` (number, optional) - Refund amount (full refund if not specified)
- `reason` (string, optional) - Refund reason
- `provider` (string, optional) - Payment provider

**Example:**
```javascript
refund_payment({
  transaction_id: "pi_123456",
  reason: "Customer request"
})
```

#### 4. `cancel_payment`

Cancel a pending payment.

**Parameters:**
- `transaction_id` (string, required) - Transaction ID to cancel
- `provider` (string, optional) - Payment provider

**Example:**
```javascript
cancel_payment({
  transaction_id: "pi_123456"
})
```

### Setup

#### 1. Installation

```bash
npm install openclaw-agent-payment-rail
```

#### 2. Environment Variables

Set up your payment provider API keys:

```bash
# Stripe
export STRIPE_API_KEY="sk_test_..."

# PayPal (coming soon)
export PAYPAL_CLIENT_ID="..."
export PAYPAL_CLIENT_SECRET="..."
```

#### 3. Initialize in Your Agent

```typescript
import { PaymentRail } from 'openclaw-agent-payment-rail';

const rail = new PaymentRail();

await rail.initialize({
  provider: 'stripe',
  apiKey: process.env.STRIPE_API_KEY,
});
```

### Use Cases

1. **E-commerce Agent** - Automated purchase processing
2. **Subscription Service** - Recurring payment management
3. **Refund Automation** - Smart refund handling
4. **Multi-currency Payments** - Global transaction support

### Supported Providers

| Provider | Status | Features |
|----------|--------|----------|
| **Stripe** | ✅ Full Support | Payments, Refunds, Cancellations |
| **PayPal** | 🚧 Coming Soon | In Development |
| **Alipay** | 📋 Planned | Future Release |
| **WeChat Pay** | 📋 Planned | Future Release |

### Documentation

- **GitHub**: https://github.com/ZhenRobotics/openclaw-agent-payment-rail
- **npm**: https://www.npmjs.com/package/openclaw-agent-payment-rail

### License

MIT License

---

<a name="chinese"></a>

## 中文

### 概述

**Agent Payment Rail** 是一个为 AI Agent 设计的通用支付基础设施技能。它提供统一的 API，让你的 Agent 应用能够集成多个支付提供商（Stripe、PayPal 等）。

### 特性

- 🌐 **多提供商支持** - Stripe、PayPal 等
- 🔌 **统一 API** - 所有支付提供商使用单一接口
- 💰 **完整交易管理** - 创建、查询、退款、取消
- 🔒 **类型安全** - 完整 TypeScript 支持
- 🌍 **多币种** - USD、EUR、GBP、CNY、JPY

### 可用工具

#### 1. `create_payment` - 创建支付

创建新的支付交易。

**参数：**
- `amount`（数字，必填）- 支付金额（如 99.99）
- `currency`（字符串，必填）- 货币代码（USD、EUR、GBP、CNY、JPY）
- `description`（字符串，必填）- 支付描述
- `provider`（字符串，可选）- 支付提供商（stripe、paypal）
- `metadata`（对象，可选）- 附加元数据

**示例：**
```javascript
create_payment({
  amount: 99.99,
  currency: "USD",
  description: "高级订阅",
  metadata: { userId: "user_123" }
})
```

#### 2. `get_transaction` - 查询交易

获取交易状态和详情。

**参数：**
- `transaction_id`（字符串，必填）- 交易 ID
- `provider`（字符串，可选）- 支付提供商

**示例：**
```javascript
get_transaction({
  transaction_id: "pi_123456"
})
```

#### 3. `refund_payment` - 退款

退款支付交易。

**参数：**
- `transaction_id`（字符串，必填）- 要退款的交易 ID
- `amount`（数字，可选）- 退款金额（不指定则全额退款）
- `reason`（字符串，可选）- 退款原因
- `provider`（字符串，可选）- 支付提供商

**示例：**
```javascript
refund_payment({
  transaction_id: "pi_123456",
  reason: "客户要求"
})
```

#### 4. `cancel_payment` - 取消支付

取消待处理的支付。

**参数：**
- `transaction_id`（字符串，必填）- 要取消的交易 ID
- `provider`（字符串，可选）- 支付提供商

**示例：**
```javascript
cancel_payment({
  transaction_id: "pi_123456"
})
```

### 设置

#### 1. 安装

```bash
npm install openclaw-agent-payment-rail
```

#### 2. 环境变量

设置你的支付提供商 API 密钥：

```bash
# Stripe
export STRIPE_API_KEY="sk_test_..."

# PayPal（即将推出）
export PAYPAL_CLIENT_ID="..."
export PAYPAL_CLIENT_SECRET="..."
```

#### 3. 在 Agent 中初始化

```typescript
import { PaymentRail } from 'openclaw-agent-payment-rail';

const rail = new PaymentRail();

await rail.initialize({
  provider: 'stripe',
  apiKey: process.env.STRIPE_API_KEY,
});
```

### 使用场景

1. **电商 Agent** - 自动化购买处理
2. **订阅服务** - 定期付款管理
3. **退款自动化** - 智能退款处理
4. **多币种支付** - 全球交易支持

### 支持的提供商

| 提供商 | 状态 | 功能 |
|--------|------|------|
| **Stripe** | ✅ 完全支持 | 支付、退款、取消 |
| **PayPal** | 🚧 即将推出 | 开发中 |
| **支付宝** | 📋 计划中 | 未来发布 |
| **微信支付** | 📋 计划中 | 未来发布 |

### 文档

- **GitHub**: https://github.com/ZhenRobotics/openclaw-agent-payment-rail
- **npm**: https://www.npmjs.com/package/openclaw-agent-payment-rail

### 许可证

MIT 许可证
