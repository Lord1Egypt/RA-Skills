# 门票退票操作指南

**触发条件**：退票、我要退票、申请退款、把刚刚预定的门票退了、取消这张门票（已支付）

---

## 退票流程

```
1. orderHistory → 获取订单列表（用户未提供订单号时）
2. orderDetail → 获取订单详情，供用户确认
3. ticket.refund.info → 获取退款信息（退票前必调）
4. ticket.refund → 提交退票申请
```

---

## 参数传递依赖

| 接口 | 入参来源 |
|------|----------|
| orderDetail | `orderBaseId` ← orderHistory 或用户提供 |
| ticket.refund.info | `orderBaseId` ← 同上 |
| ticket.refund | `orderBaseId` ← 同上<br>`orderItemNo` ← ticket.refund.info 返回的 `orderItemNo`<br>`refundQuantity` ← ticket.refund.info 返回的 `refundQuantity`<br>`amount` ← `cashRefundAmount` + `quotaRefundAmount` |

---

## 接口参数

### ticket.refund.info（获取退款信息）
**必填**：`orderBaseId`（订单号）

**返参关键字段**：
- `refundQuantity`：可退数量
- `quantity`：下单数量
- `orderItemNo`：订单明细编号（申请退票时使用）
- `originAmount`：原金额
- `cashRefundAmount`：现金退款金额
- `quotaRefundAmount`：额度退款金额

### ticket.refund（申请退票）
**必填**：
- `orderBaseId`：订单号
- `orderType`：传 3（门票）
- `applyType`：默认 1
- `refundType`：1=全额退票
- `amount`：退款金额，取 cashRefundAmount + quotaRefundAmount
- `refundItemList`：退票明细列表，**仅一个元素**

**refundItemList 结构（必填）**：
- `orderItemNo`：取退款信息接口返回的 orderItemNo
- `refundQuantity`：取退款信息返回的 refundQuantity
- `refundAmount`：取退款信息返回的退款金额

---

## 调用命令

```bash
# 订单历史
python scripts/apiexe.py call --method orderHistory --arg "{\"current\": 1, \"size\": 15}"

# 订单详情（必填：orderBaseId）
python scripts/apiexe.py call --method orderDetail --arg "{\"orderBaseId\": \"TRO202603151234567890\"}"

# 获取退款信息（必填：orderBaseId）
python scripts/apiexe.py call --method ticket.refund.info --arg "{\"orderBaseId\": \"TRO202603151234567890\"}"

# 申请退票（必填：orderBaseId, orderType, applyType, refundType, amount, refundItemList）
python scripts/apiexe.py call --method ticket.refund --arg "{\"orderBaseId\": \"TRO202603151234567890\", \"orderType\": 3, \"applyType\": 1, \"refundType\": 1, \"amount\": 55, \"refundReason\": \"行程变更\", \"refundItemList\": [{\"orderItemNo\": \"OI202603151234567890\", \"refundQuantity\": 1, \"refundAmount\": 55}]}"
```

---

## 展示格式

**订单列表**：「① 景点名  门票×数量  日期  状态  金额」

**退款信息**：订单号、景点、门票、可退数量、原金额、退款金额

**退票成功**：订单号、退款金额、预计到账时间(3-7个工作日)

---

## 异常处理

- **订单不可退**：提示可能原因（未支付/超时限/已使用）
- **获取退款信息失败**：提示稍后重试或前往中旅旅行App
- **退票申请失败**：展示后台友好提示，引导重试或前往App
