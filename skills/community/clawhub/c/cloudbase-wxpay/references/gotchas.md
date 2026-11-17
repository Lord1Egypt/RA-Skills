# CloudBase 微信支付踩坑全记录

本文档记录一次完整的 CloudBase 微信支付 + 退款集成过程中遇到的所有坑点、
根因分析和修复方案。每个坑点都经过生产环境验证。

---

## 坑点 1: DevTools 上传不带环境变量，支付走了模拟路径

### 症状

支付流程"成功"了但没有实际扣款，微信支付后台看不到任何交易记录。
`WX_MCH_ID` 在云函数中为空字符串。

### 根因

微信开发者工具的"上传并部署"功能**不会携带云函数的环境变量**。
`process.env.WX_MCH_ID` 等关键变量为空 → `cloud.cloudPay.unifiedOrder()`
在没有商户号的情况下静默降级到模拟模式。

### 修复

使用 CloudBase CLI 部署：

```bash
tcb fn deploy payment --envId <your-env-id>
tcb fn deploy order --envId <your-env-id>
```

### 防御措施

在 payment 云函数入口加环境变量检查：

```js
exports.main = async (event, context) => {
  const required = ['WX_MCH_ID', 'WX_APPID', 'WX_MCH_KEY'];
  const missing = required.filter(k => !process.env[k]);
  if (missing.length > 0) {
    console.error('Missing env vars:', missing);
    return { code: -1, errMsg: `配置缺失: ${missing.join(', ')}。请使用 CLI 部署。` };
  }
  // ... continue
};
```

---

## 坑点 2: `envId` 用了 `cloud.DYNAMIC_CURRENT_ENV`

### 症状

`cloud.cloudPay.unifiedOrder()` 返回异常数据，支付预处理阶段就失败。

### 根因

`cloud.DYNAMIC_CURRENT_ENV` 在云调用的上下文中无法正确解析为当前环境 ID，
导致微信支付 API 收到无效的环境标识。

### 修复

直接硬编码环境 ID 字符串：

```js
// ❌ 错误
envId: cloud.DYNAMIC_CURRENT_ENV

// ✅ 正确
envId: 'prod-xxxxx'
```

使用环境变量管理不同环境的值：

```js
envId: process.env.CLOUDBASE_ENV_ID || 'prod-xxxxx'
```

---

## 坑点 3: `subAppId` 大小写 / 多余字段

### 症状

`unifiedOrder` 返回 `resultCode: FAIL`，错误信息含糊。

### 根因

非子商户模式下不需要 `subAppId` 字段。如果代码中携带了这个字段，
微信支付 API 会因为字段名大小写敏感或字段不存在而拒绝请求。

### 修复

删除 `unifiedOrder` 调用中的 `subAppId` 字段（除非确实在使用子商户模式）：

```js
// ❌ 包含 subAppId
const result = await cloud.cloudPay.unifiedOrder({
  body: '...',
  subAppId: 'wx...',  // 不必要
  // ...
});

// ✅ 删除 subAppId
const result = await cloud.cloudPay.unifiedOrder({
  body: '...',
  // subAppId: removed
  // ...
});
```

---

## 坑点 4: 退款返回值只检查了外层 `code`，没检查 `returnCode`/`resultCode`

### 症状（最严重的坑）

用户取消订单后，订单状态变成了 `user_cancelled`，`refundedAt` 也设置了时间戳，
但 `refundTransactionId` 为空字符串，微信钱包根本没有收到退款。
**钱没有退回用户。**

数据库查询结果示例：

```json
{
  "_id": "717c23bf6a60e76c1146068100688a4d",
  "status": "user_cancelled",
  "transactionId": "4500000275202607221598101055",
  "refundTransactionId": "",
  "totalAmount": 1,
  "refundedAt": "2026-07-22T15:53:37.230Z"
}
```

### 根因

旧代码在 order 云函数的 cancel 流程中这样处理退款结果：

```js
// ❌ 错误：只检查了云函数返回值，没检查退款 API 的 returnCode/resultCode
const refundResult = await callPaymentCloud('refund', { ... });
if (refundResult.code === 0) {
  // 以为退款成功了 → 设置 refundedAt → 订单标记为"已退款"
  await updateOrder(orderId, {
    status: 'user_cancelled',
    refundedAt: new Date(),
  });
}
```

问题在于 `callPaymentCloud` 返回的 `code` 只是云函数调用成功的标识，
不等于微信支付退款 API 真的执行了退款。必须检查 `cloud.cloudPay.refund()`
返回对象中的 `returnCode` 和 `resultCode`。

### 修复

退款结果必须做双层检查：

```js
const refundResult = await callPaymentCloud('refund', { ... });

// 第一层：云函数调用是否成功
if (refundResult.code !== 0) {
  return { code: -1, errMsg: '调用支付云函数失败' };
}

// 第二层：退款 API 的 returnCode（CloudBase 封装层）
if (refundResult.returnCode !== 'SUCCESS') {
  return { code: -1, errMsg: refundResult.returnMsg || '退款请求失败' };
}

// 第三层：退款 API 的 resultCode（微信支付层）
if (refundResult.resultCode !== 'SUCCESS') {
  return { code: -1, errCode: refundResult.errCode, errMsg: refundResult.errCodeDes };
}

// 现在才是真正退款成功
await updateOrder(orderId, {
  status: 'user_cancelled',
  refundedAt: new Date(),
  refundTransactionId: refundResult.refundId,
});
```

### 防御措施

在 payment 云函数的 refund action 中直接返回原始 API 结果的关键字段，
不在云函数层做乐观的成功假设：

```js
const result = await cloud.cloudPay.refund({...});
return {
  code: 0,
  returnCode: result.returnCode,       // 必须透传
  returnMsg: result.returnMsg,
  resultCode: result.resultCode,       // 必须透传
  errCode: result.errCode,
  errCodeDes: result.errCodeDes,
  refundId: result.refundId || '',
};
```

---

## 坑点 5: CLI (`tcb fn invoke`) 调用退款报 `-501001 invalid wx openapi access_token`

### 症状

用 CLI 手动触发退款云函数时：

```bash
tcb fn invoke payment --envId <env-id> --params '{"action":"refund","orderId":"..."}'
```

返回：`-501001 invalid wx openapi access_token`

### 根因

`cloud.cloudPay.refund()` 属于**云调用**。云调用需要微信侧的鉴权上下文
（access_token），这个上下文只在以下场景中由平台自动注入：

| 调用方式 | 是否有云调用上下文 |
|---------|------------------|
| 小程序端 `wx.cloud.callFunction` | ✅ 有 |
| 定时触发器 | ✅ 有 |
| HTTP API 触发器 | ✅ 有 |
| `tcb fn invoke` (CLI) | ❌ 无 |
| CloudBase 控制台测试 | ❌ 无 |

CLI 调用不携带微信用户会话，无法获取有效的 access_token → 微信支付 API 拒绝请求。

### 修复

**永远不要**用 CLI 测试云调用。改为：
- 在小程序端通过 `wx.cloud.callFunction` 触发
- 或通过 HTTP API 触发器触发

对于历史订单补退款，需要在小程序订单列表页添加触发按钮：

**WXML (list.wxml):**
```html
<view wx:if="{{item.status === 'user_cancelled' && !item.refundTransactionId}}"
      class="refund-info-warn">
  已取消，退款尚未到账
  <button class="btn-refund-retry" bindtap="onForceRefund" data-order-id="{{item._id}}">
    重试退款
  </button>
</view>
```

**JS (list.js):**
```js
onForceRefund(e) {
  const orderId = e.currentTarget.dataset.orderId;
  wx.showModal({
    title: '确认退款',
    content: '将为此订单重新发起退款，确认？',
    success: async (res) => {
      if (!res.confirm) return;
      const result = await wx.cloud.callFunction({
        name: 'payment',
        data: { action: 'force_refund', orderId },
      });
      if (result.result?.code === 0) {
        wx.showToast({ title: '退款已发起', icon: 'success' });
        this.loadOrders(); // refresh
      } else {
        wx.showToast({
          title: result.result?.errMsg || '退款失败',
          icon: 'error',
        });
      }
    },
  });
},
```

**payment 云函数 force_refund action:**
```js
case 'force_refund':
  // 绕过 status 检查，直接调用退款
  // 注意：这个 action 不需要用户鉴权 token
  const order = await db.collection('orders').doc(event.orderId).get();
  const refundResult = await cloud.cloudPay.refund({
    transactionId: order.data.transactionId,
    outTradeNo: event.orderId,
    outRefundNo: generateOutRefundNo(event.orderId),
    totalFee: order.data.totalAmount,
    refundFee: order.data.totalAmount,
    envId: 'your-env-id',
    functionName: 'payment',
  });
  return {
    code: 0,
    returnCode: refundResult.returnCode,
    resultCode: refundResult.resultCode,
    errCode: refundResult.errCode,
    errCodeDes: refundResult.errCodeDes,
    refundId: refundResult.refundId || '',
  };
```

### 临时代码清理

`force_refund` 和相关 UI 按钮是**临时修复措施**。历史订单补退完成后必须移除：
- `payment/index.js` 中的 `force_refund` case
- `list.wxml` 中的退款按钮
- `list.js` 中的 `onForceRefund` 方法
- `list.wxss` 中的相关样式

---

## 调试命令速查

### 检查订单状态

```bash
# 按订单号查询
tcb db query --envId <env-id> -c orders --where '{"orderNo":"2026072215004"}'

# 按文档 ID 查询
tcb db query --envId <env-id> -c orders --where '{"_id":"<doc-id>"}'
```

### 检查云函数环境变量

```bash
tcb fn detail payment --envId <env-id>
```

### 查看云函数日志

```bash
tcb fn log payment --envId <env-id> --limit 20
```

### 检查退款关键字段

订单文档中退款相关的关键字段：

| 字段 | 正常值 | 异常值 | 含义 |
|------|--------|--------|------|
| `refundTransactionId` | `"5000..."` | `""` | 退款没执行 |
| `refundedAt` | 有效时间戳 | 存在但 refundTransactionId 为空 | 假退款 |
| `status` | `refunded` | `user_cancelled` + 空 refundTransactionId | 假退款 |
| `transactionId` | `"4500..."` | 空或不存在 | 支付没执行 |

### 退款失败诊断流程

```
订单显示"已退款"但用户没收到钱？
    ↓
查 refundTransactionId
    ↓
├── 非空 → 查微信支付后台，确认退款状态
└── 空字符串 → 确认假退款 bug
        ↓
    检查旧代码是否有双层 returnCode/resultCode 检查
        ↓
    没有 → 这就是根因
        ↓
    修复退款检查逻辑 + 小程序端补退
```

---

## 经验总结

1. **云函数部署必须用 CLI**，DevTools 上传不可靠
2. **环境变量硬编码兜底**，并在云函数入口做防御性检查
3. **`envId` 绝不可以用 `DYNAMIC_CURRENT_ENV`**，云调用上下文不支持动态解析
4. **退款结果检查是三层**：云函数返回码 → CloudBase 封装层 returnCode → 微信支付层 resultCode，缺一不可
5. **云调用只能在有微信上下文的场景使用**：小程序端、定时触发器、HTTP API。CLI 和控制台都不行
6. **历史数据修复需要用小程序端触发**，不能图方便用 CLI
7. **临时修复代码要及时清理**，不要留在生产环境
