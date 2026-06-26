---
name: bsc-dev-monitor
description: |
  BSC Dev Wallet Monitor - 专为跟投 Dev 的用户设计。
  监控指定 BSC 地址的代币转出（发币）行为，第一时间发现新币发布。
  支持 Webhook 通知、安全检测、历史记录等功能。
version: 1.0.0
author: "Your Name"
tags: [bsc, monitor, trading, crypto, defi, follow-trader]
payment:
  provider: skillpay.me
  api_key: sk_f072a786149bc07fc8730b4683dc00f3e050e72441922284ca803cdee2b994b5
  skill_id: 9469b85f-f40f-4ada-ad9c-bdd9db1167cc
  price: 0.001
  currency: USDT
  billing_mode: per_call  # 按次收费：每次监控请求 0.001 USDT
---

# BSC Dev Monitor Skill

## 🎯 适用人群

- **跟投 Dev 的用户** - 追踪项目方地址，第一时间发现新币
- **Alpha 猎人** - 寻找早期机会代币
- **套利交易者** - 检测大额转账，捕捉套利机会
- **风险管理者** - 追踪可疑地址行为

## 💰 收费模式

### 按次收费
- **每次监控请求**: 0.001 USDT (1 token)
- **无论是否有检测**
- **简单明了**

**当前价格**: 0.001 USDT / 次
**充值比例**: 1 USDT = 1000 tokens
**最低充值**: 8 USDT (8000 tokens)
**平台手续费**: 5%
**提现**: 自动到你的钱包

## 🔧 使用方法

### 1. 设置监控

```javascript
{
  "action": "monitor",
  "address": "0x4f0f84abd0b2d8a7ae5e252fb96e07946dbbb1a4",
  "name": "知名 Dev 地址",
  "webhook_url": "https://your-server.com/webhook",  // 可选：Webhook 通知
  "duration": 86400  // 监控 24 小时，0 表示持续监控
}
```

### 2. 查询监控历史

```javascript
{
  "action": "history",
  "address": "0x4f0f84abd0b2d8a7ae5e252fb96e07946dbbb1a4",
  "limit": 20
}
```

### 3. 取消监控

```javascript
{
  "action": "stop",
  "monitor_id": "monitor_xxxx"
}
```

## 📊 检测通知

### 检测到新币时的返回

```json
{
  "status": "detected",
  "timestamp": "2026-03-05T08:00:00Z",
  "block": 84768918,
  "monitor_id": "monitor_abc123",
  "token": {
    "name": "New Token",
    "symbol": "NEW",
    "decimals": 18,
    "contract": "0x..."
  },
  "amount": "1000000000000000000",
  "txHash": "0x...",
  "from": "0x4f0f84abd0d...1a4",
  "billing": {
    "mode": "per_call",
    "charged": true,
    "amount": "0.001",
    "currency": "USDT"
  }
}
```

### Webhook 通知格式

如果配置了 webhook_url，系统会自动推送：

```json
{
  "event": "token_detected",
  "timestamp": "2026-03-05T08:00:00Z",
  "monitor_id": "monitor_abc123",
  "data": {
    "token": {
      "name": "New Token",
      "symbol": "NEW",
      "contract": "0x..."
    },
    "txHash": "0x...",
    "block": 84768918
  },
  "billing": {
    "charged": true,
    "amount": "0.001 USDT"
  }
}
```

## 🔍 高级功能

### 1. 批量监控

```javascript
{
  "action": "batch_monitor",
  "addresses": [
    {
      "address": "0x4f0f84abd0d...1a4",
      "name": "Dev A"
    },
    {
      "address": "0x742d35Cc663...bEb",
      "name": "Dev B"
    }
  ],
  "webhook_url": "https://your-server.com/webhook"
}
```

### 2. 安全过滤

```javascript
{
  "action": "monitor",
  "address": "0x...",
  "safety_checks": {
    "honeypot_check": true,      // 蜜罐检测
    "liquidity_check": true,      // 流动性检查
    "min_liquidity": "1000"      // 最小流动性（USDT）
  },
  "only_safe_tokens": true  // 只通知通过安全检查的代币
}
}
```

### 3. 智能过滤

```javascript
{
  "action": "monitor",
  "address": "0x...",
  "filters": {
    "min_amount": "1000000000000000000000",  // 最小金额
    "exclude_contracts": ["0x..."],           // 排除的合约
    "include_symbols": ["PEPE", "DOGE"]       // 只关注指定符号
  }
}
```

## 💡 使用场景

### 场景 1：跟投知名 Dev

```javascript
// 设置监控
{
  "action": "monitor",
  "address": "0x4f0f84abd0d...1a4",  // 知名 Dev 地址
  "name": "知名 Dev A",
  "webhook_url": "https://your-bot.com/webhook"
}

// 收到通知后，你可以：
// 1. 查看代币信息
// 2. 检查流动性
// 3. 决定是否买入
```

### 场景 2：监控多个地址

```javascript
// 批量设置监控
{
  "action": "batch_monitor",
  "addresses": [
    {"address": "0x...", "name": "Dev A"},
    {"address": "0x...", "name": "Dev B"},
    {"address": "0x...", "name": "Dev C"}
  ]
}

// 任何地址发币都会通知你
```

### 场景 3：安全跟投

```javascript
// 只投资安全的代币
{
  "action": "monitor",
  "address": "0x...",
  "safety_checks": {
    "honeypot_check": true,
    "liquidity_check": true,
    "min_liquidity": "10000"
  },
  "only_safe_tokens": true
}

// 只有通过安全检查的代币才会通知
```

## ⚠️ 重要提示

1. **本 Skill 仅监控，不保证代币质量**
   - 检测到的代币可能存在风险
   - 建议自行评估项目基本面
   - 配合安全检测功能使用

2. **收费模式说明**
   - 按次收费：每次监控请求都收费 (0.001 USDT/次)
   - 无论是否有检测都会收费
   - 最低充值：8 USDT (8000 tokens)
   - 平台手续费：5%
   - 提现自动到你的钱包

3. **建议操作**
   - 检测到代币后，先查看合约
   - 检查流动性池状态
   - 验证代币安全
   - 小仓位试水

## 📞 支持

- 查看 README.md 了解详细文档
- 访问 https://clawhub.com/skill/bsc-dev-monitor
- 提交 Issue 或联系作者

---

**让跟投更简单！** 🚀
