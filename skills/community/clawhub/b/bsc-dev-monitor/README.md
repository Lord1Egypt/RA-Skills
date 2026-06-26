# BSC Dev Monitor Skill

## 🎯 简介

这是一个用于监控 BSC 链上指定地址代币转出行为的 OpenClaw Skill。

当目标地址发送代币时，系统会立即检测并通知用户。

## 💰 定价

- **每次调用**: 0.001 USDT
- **支付方式**: SkillPay.me
- **计费模式**: 按次收费

## 🚀 快速开始

### 安装

```bash
npm install
```

### 测试运行

```bash
# 监控指定地址 60 秒
npm test

# 监控自定义地址 120 秒
node index.js <ADDRESS> 120
```

### 使用方法

#### 监控单个地址

```javascript
{
  "action": "monitor",
  "address": "0x4f0f84abd0b2d8a7ae5e252fb96e07946dbbb1a4",
  "duration": 3600
}
```

#### 返回结果

检测到代币转账时返回：

```json
{
  "status": "detected",
  "timestamp": "2026-03-05T08:00:00Z",
  "block": 84768918,
  "token": {
    "name": "Unknown",
    "symbol": "UNK",
    "decimals": 18,
    "contract": "0x..."
  },
  "amount": "Unknown",
  "txHash": "0x...",
  "from": "0x..."
}
```

## ⚙️ 配置

### SkillPay 配置

```javascript
{
  apiKey: 'sk_f072a786149bc07fc8730b4683dc00f3e050e72441922284ca803cdee2b994b5',
  price: '0.001',
  currency: 'USDT',
  perCall: true
}
```

### BSC 配置

```javascript
{
  rpc: 'https://bsc-dataseed.binance.org/',
  chainId: 56
}
```

## 🔧 API 接口

### generatePaymentLink(userId, callbackUrl)

生成支付链接

**参数:**
- `userId`: 用户 ID
- `callbackUrl`: 回调 URL

**返回:** 支付链接字符串

### verifyPayment(userId, paymentId)

验证支付状态

**参数:**
- `userId`: 用户 ID
- `paymentId`: 支付 ID

**返回:** 验证结果

### monitorAddress(address, options)

监控指定地址

**参数:**
- `address`: 监控地址
- `options.duration`: 监控时长（秒），默认 3600
- `options.chain`: 网络，默认 'BSC'

**返回:** 检测结果数组

## 📊 支付流程

1. 用户发起监控请求
2. 系统返回支付链接
3. 用户完成支付
4. 系统验证支付
5. 开始监控
6. 检测到代币转账时通知用户

## ⚠️ 注意事项

1. 本 Skill 仅监控代币转出，不保证代币质量
2. 使用前请自行评估风险
3. 建议配合安全检测工具使用
4. 监控服务为异步模式

## 📝 更新日志

### v1.0.0 (2026-03-05)

- ✅ 初始版本发布
- ✅ 实现基础监控功能
- ✅ 接入 SkillPay.me 支付
- ✅ 支持多地址监控
- ✅ 实时代币转账检测

## 📞 支持

如有问题或建议，请提交 Issue。

---

**Skill 版本**: v1.0.0
**最后更新**: 2026-03-05
