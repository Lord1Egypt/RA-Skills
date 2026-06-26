# 酒店退订操作指南

**触发条件**：退订/退款酒店

> **接口文档**：调用接口前请查阅 [api/hotel-refund.json](../api/hotel-refund.json)，获取完整的 method、category、subCategory、action 及参数定义。

---

## 核心流程

```
1. hotel.orderHistory → 获取订单列表
2. orderDetail → 获取订单详情（orderItemNo、入住人）
3. orderDeduct → 核算手续费和退款金额
4. hotel.refund → 提交退订申请
```

---

## 参数传递依赖

| 接口 | 入参来源 |
|------|----------|
| hotel.orderHistory | `memberId` ← 认证上下文 |
| orderDetail | `orderBaseId` ← 用户选择或订单列表 |
| orderDeduct | `orderBaseId` ← 上一步<br>`orderItemNo` ← orderDetail 返回的 `data.hotelProductInfo.orderItemNo`<br>`passengerIdList` ← orderDetail 返回的入住人ID列表 |
| hotel.refund | `amount`、`refundAmount` ← orderDeduct 返回<br>`orderItemNo`、`orderPassengerIds` ← orderDeduct 返回的 `deductItemList[]` |

---

## 关键参数说明

### orderDeduct（核损）
- `resourceType`: 1（酒店）
- `refundType`: 1-全额退订，2-部分退订
- `applyType`: 1（默认）
- `deductItemList`: 核损项目列表
  - `orderItemNo`: 订单项编号（从 orderDetail 获取）
  - `passengerIdList`: 入住人ID列表（数组格式）

### hotel.refund（申请退订）
- `orderType`: 1（酒店）
- `applyType`: 1（默认）
- `refundType`: 1-全额退订，2-部分退订
- `amount`: 退款金额（从核损结果获取）
- `originAmount`: 原支付金额（从订单详情获取）
- `refundItemList`:
  - `orderItemNo`: 从核损结果的 `deductItemList[].orderItemNo` 获取
  - `orderPassengerIds`: 从核损结果的 `deductItemList[].passengerIdList` 获取（数组格式）
  - `refundAmount`: 手续费（从核损结果获取）

---

## 调用命令示例

```bash
# 订单历史
python scripts/apiexe.py call --method hotel.orderHistory --arg "{\"memberId\": \"15d6676f6be54d5099b106abeeecfcd6\"}"

# 订单详情
python scripts/apiexe.py call --method orderDetail --arg "{\"orderBaseId\": \"HRO202603101234567890\"}"

# 核损
python scripts/apiexe.py call --method orderDeduct --arg "{\"orderBaseId\": \"HRO202603101234567890\", \"resourceType\": 1, \"refundType\": 1, \"applyType\": 1, \"reason\": \"行程变更\", \"deductItemList\": [{\"orderItemNo\": \"OI202603101234567890\", \"passengerIdList\": [399]}]}"

# 申请退订
python scripts/apiexe.py call --method hotel.refund --arg "{\"orderBaseId\": \"HRO202603101234567890\", \"orderType\": 1, \"applyType\": 1, \"refundType\": 1, \"amount\": 680, \"originAmount\": 796, \"refundReason\": \"行程变更\", \"refundItemList\": [{\"orderItemNo\": \"OI202603101234567890\", \"orderPassengerIds\": [399], \"refundQuantity\": 1, \"refundAmount\": 116}]}"
```

---

## 展示格式参考

**订单列表**：一行一行展示，格式「订单号 | 酒店 | 入住日期 | 状态 | 金额」

**核损结果**：
```
📊 核损结果

订单号：HRO202603101234567890
酒店：如家酒店(北京天安门广场店)
入住日期：2026年3月15日 - 3月17日

退订入住人：
  张三  退款金额：¥680  手续费：¥116

原支付金额：¥796
退款金额：¥680
手续费：¥116

确认核损信息无误后，请回复「确认退订」。
```

**退订成功**：
```
✅ 退订申请已提交

订单号：HRO202603101234567890
退款金额：¥680
手续费：¥116
预计到账时间：3-7 个工作日

您可以通过「查询订单状态」查看退订进度。
```

---

## 异常处理

- **核损失败/退订失败**：保留订单号、退订原因等信息，提示稍后重试或前往中旅旅行App
- **网络超时**：提示稍后重试

**重要**：异常时不要让用户重复提供信息，已收集的内容必须记住。

---

## 用户体验

- **对话风格**：友好自然，如「好的，我来帮您办理退订」
- **润色展示**：使用 📋 ✅ ❌ ⚠️ 等符号增强可读性，一行一行展示，勿用表格
- **禁止技术用语**：对用户说「正在为您核算退款金额」「正在提交退订申请」，不得出现接口名、API、method 等
