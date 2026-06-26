# order-query 输出模板

拿到 JSON 后**直接按模板填充输出**。返回结构：`summary`（汇总）+ `orders`（订单列表）。

## 输出模板

```
### 📋 近 {days} 天返利订单

**汇总**：共 {summary.totalOrders} 笔订单，预估返利 **{summary.totalCommission}**

| 商家 | 订单金额 | 预估返利 | 状态 | 下单时间 |
|------|---------|---------|------|---------|
| {storeName} | {orderAmount} | {commission} | {status} | {orderTime} |
```

## 状态映射

渲染时把 API 状态值转成中文：

| API 状态值 | 用户可见 |
|-----------|---------|
| `pending` | 待确认 |
| `confirmed` | 已确认 |
| `paid` | 已到账 |
| `rejected` | 已拒绝 |

## 空订单处理

`orders` 为空或不存在时输出：

```
近 {days} 天暂无返利订单。

💡 通过返利链接购物后，订单通常需要 1-3 天才会出现在这里。
```

## 完整示例

<example>
用户：我的返利订单

助手：

正在查询返利订单...

[调用 node {baseDir}/scripts/run.mjs orders]

### 📋 近 30 天返利订单

**汇总**：共 3 笔订单，预估返利 **¥82.50**

| 商家 | 订单金额 | 预估返利 | 状态 | 下单时间 |
|------|---------|---------|------|---------|
| Adidas | ¥899.00 | ¥53.94 | 已确认 | 2026-03-25 |
| Space NK NL | €65.00 | €5.20 | 待确认 | 2026-04-01 |
| designwebstore DE | €120.00 | €8.40 | 待确认 | 2026-04-05 |
</example>

<example>
用户：最近有返利到账吗

助手：

正在查询返利订单...

[调用 node {baseDir}/scripts/run.mjs orders]

近 30 天暂无返利订单。

💡 通过返利链接购物后，订单通常需要 1-3 天才会出现在这里。
</example>
