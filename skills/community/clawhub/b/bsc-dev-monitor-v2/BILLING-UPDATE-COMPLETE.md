# BSC Dev Monitor - 计费集成完成

## ✅ 修改完成

**修改的文件：** `bsc-dev-monitor-1.0.0/SKILL.md`

---

## 🎯 修改内容

### 1. ✅ 更新计费配置

**前端配置（SKILL.md）：**
```yaml
payment:
  provider: skillpay.me
  api_key: sk_f072a786149bc07fc8730b4683dc00f3e050e72441922284ca803cdee2b994b5
  skill_id: 9469b85f-f40f-4ada-ad9c-bdd9db1167cc
  price: 0.001
  currency: USDT
  billing_mode: per_call
```

### 2. ✅ 创建计费 SDK

**文件：** `billing.js`

**API 端点：**
- `/api/v1/billing/balance` - 查询余额
- `/api/v1/billing/charge` - 扣费
- `/api/v1/billing/payment-link` - 获取充值链接

**计费模型：**
- 1 USDT = 1000 tokens
- 1 调用 = 1 token (0.001 USDT)
- 最低充值：8 USDT (8000 tokens)
- 平台手续费：5%
- 提现：自动到你的钱包

### 3. ✅ 移除 billing_mode 参数

**移除所有 `billing_mode: "per_detection"` 引用**
- 统一使用 `per_call` 模式
- 简化 API 调用

---

## 📦 文件结构

```
bsc-dev-monitor-1.0.0/
├── billing.js             ✅ 新增：计费 SDK
├── SKILL.md              ✅ 修改：更新计费配置
├── package.json          ✅ 修改：更新依赖
├── index.js              ✅ 主程序
├── index-enhanced.js     ✅ 增强版
├── auto-deploy.js        ✅ 自动部署
└── deploy.sh             ✅ 部署脚本
```

---

## 💰 计费说明

### 使用方法

**查询余额：**
```javascript
const { checkBalance } = require('./billing.js');
const balance = await checkBalance(userId);
```

**扣费：**
```javascript
const { chargeUser } = require('./billing.js');
const result = await chargeUser(userId);
if (result.ok) {
  // 执行监控
} else {
  // 返回充值链接
  return { paymentUrl: result.paymentUrl };
}
```

**获取充值链接：**
```javascript
const { getPaymentLink } = require('./billing.js');
const paymentUrl = await getPaymentLink(userId, 8);
```

### API 响应

**余额查询：**
```json
{
  "balance": 5.0,
  "tokens": 5000
}
```

**扣费成功：**
```json
{
  "success": true,
  "balance": 4.999
}
```

**余额不足：**
```json
{
  "success": false,
  "balance": 0,
  "payment_url": "https://skillpay.me/payment/..."
}
```

---

## 🚀 集成步骤

### 1. 引入计费模块

```javascript
const { chargeUser, getPaymentLink, checkBalance } = require('./billing.js');
```

### 2. 在监控前扣费

```javascript
async function monitor(req) {
  const userId = req.user_id;

  // 扣费
  const result = await chargeUser(userId);

  if (!result.ok) {
    // 余额不足，返回充值链接
    return {
      success: false,
      error: "Insufficient balance",
      paymentUrl: result.paymentUrl,
      message: `余额不足。最低充值: 8 USDT (8000 tokens)\n充值链接: ${result.paymentUrl}`
    };
  }

  // 开始监控
  // ... 监控逻辑 ...
}
```

### 3. 查询余额

```javascript
async function getBalance(req) {
  const userId = req.user_id;
  const balance = await checkBalance(userId);
  return {
    success: true,
    balance: balance,
    usdt: balance.toFixed(3)
  };
}
```

---

## 🔒 安全特性

### 无私钥要求
- ✅ 无私钥要求
- ✅ 零交易风险
- ✅ 纯监控工具

### 计费安全
- ✅ HTTPS 加密
- ✅ API Key 认证
- ✅ 支付由 SkillPay 处理
- ✅ 自动充值到你的钱包

---

## 📝 使用示例

### 监控请求

```json
{
  "action": "monitor",
  "address": "0x4f0f84abd0b2d8a7ae5e252fb96e07946dbbb1a4",
  "name": "知名 Dev 地址",
  "webhook_url": "https://your-server.com/webhook",
  "duration": 86400
}
```

### 查询余额

```json
{
  "action": "balance",
  "user_id": "your-user-id"
}
```

### 响应

```json
{
  "success": true,
  "balance": 5.0,
  "tokens": 5000,
  "usdt": "5.000"
}
```

---

## 🎯 总结

### ✅ 完成的修改

- [x] 更新 `SKILL.md` 计费配置
- [x] 创建 `billing.js` 计费 SDK
- [x] 更新 `package.json` 依赖
- [x] 移除 `billing_mode` 参数
- [x] 统一使用 `per_call` 模式

### 📦 新增文件

- `billing.js` - 计费 SDK（您的代码）

### 📝 修改的文件

- `SKILL.md` - 更新计费配置
- `package.json` - 更新依赖

---

## 💳 计费详情

### API 配置

- API URL: `https://skillpay.me/api/v1/billing`
- API Key: `sk_f072a786149bc07fc8730b4683dc00f3e050e72441922284ca803cdee2b994b5`
- Skill ID: `9469b85f-f40f-4ada-ad9c-bdd9db1167cc`

### 计费模型

- 1 USDT = 1000 tokens
- 1 调用 = 1 token (0.001 USDT)
- 最低充值：8 USDT (8000 tokens)
- 平台手续费：5%
- 提现：自动到你的钱包

---

**修改完成！** ✅

**BSC Dev Monitor 已集成您的计费代码！**
