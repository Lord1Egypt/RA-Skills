# 火车票退票操作指南

**触发条件**：退票、我要退票、申请退款、把刚刚预定的火车票退了、取消这张火车票（已支付）

---

## 退票流程

```
1. orderDetail → 获取订单详情，供用户确认
2. orderDeduct → 核损（退票前必调）
3. train.refund → 提交退票申请
```

---

## 退票场景智能识别

**用户表达意图识别**：

| 用户输入                               | refundType    | 说明                 |
| -------------------------------------- | ------------- | -------------------- |
| 「退票」「我要退票」「取消这张火车票」 | 1（全额退票） | 未指定乘客，默认全退 |
| 「全退」「全部退票」「三个人都要退」   | 1（全额退票） | 明确全额退票         |
| 「张三退票」「退张三的票」             | 2（部分退票） | 指定了单个乘客       |
| 「张三和李四退票」「退张三和李四」     | 2（部分退票） | 指定了部分乘客       |
| 「只退王五」「王五一个人退票」         | 2（部分退票） | 指定了单个乘客       |

---

## 接口参数

### orderDetail

- `orderBaseId`: orderHistory 或用户提供

### orderDeduct

- `orderBaseId`: orderHistory 或用户提供
- `resourceType`: 资源类型，默认 2（火车票）
- `refundType`: 1-整单退，2-部分退
- `applyType`: 0-自愿退票，1-非自愿退票，默认 0
- `reason`: 退票原因
- `deductItemList`: 核损项目列表（必填）
  - `orderItemNo`: 订单项编号（从订单详情获取 取值 `data.trainProductInfos.orderItemNo`）
  - `passengerIdList`: 需要退票的乘客ID列表(必填 从订单详情获取 取值 `data.trainProductInfos.trainTicketInfo.passengerId`)

    * 全额退票：包含订单中所有乘客ID
    * 部分退票：只包含用户指定的乘客ID

### train.refund

- `orderBaseId`: orderHistory 或用户提供
- `refundType`: 1-全额退票，2-部分退票（必填）
- `orderItemNo`: 订单项编号（从订单详情获取 取值从核损的 `ddeductItemList[].orderItemNo`获取）
- `amount`: 从核损的 `trainDeductInfo.totalRefundAmount`获取（退款金额）
- `originAmount`: 原金额
- `orderPassengerIds`: 订单使用人

---

## 调用命令

```bash
# 订单历史
python scripts/apiexe.py call --method orderHistory --arg '{"current": 1, "size": 15}'

# 订单详情（必填：orderBaseId）
python scripts/apiexe.py call --method orderDetail --arg '{"orderBaseId": "TRO202603151234567890"}'

# 获取核损信息（必填：orderBaseId）
python scripts/apiexe.py call --method orderDeduct --arg '{"orderBaseId": "SRO202603091138018328863", "resourceType": 2, "refundType": 1, "applyType": 0, "reason": "行程变更", "deductItemList": [{"orderItemNo": "OI202603091441449321207", "passengerIdList": ["399"]}]}'

# 申请退票（必填：orderBaseId, orderType, applyType, refundType, amount, refundItemList）
python scripts/apiexe.py call --method train.refund --arg '{"orderBaseId": "SRO202603091138018328863", "refundType": 1, "amount": 479, "originAmount": 479, "orderPassengerIds": [316]}'
```

---

## 展示格式

**核损信息**：

```
📊 核损结果

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

订单号：TRO202603101234567890
车次：G101 北京 → 上海
日期：2026年3月10日 08:00 → 10:15

退票乘客：
  张三 退票金额：¥580  手续费：¥100
  李四 退票金额：¥580  手续费：¥100
  王五 退票金额：¥580  手续费：¥100

────────────────────────────────────────
总计：
  原支付金额：¥2040
  退款金额：¥1740
  手续费：¥300

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

确认核损信息无误后，请回复「确认退票」。
```

**退票成功**：

```
✅ 退票申请已提交

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

订单号：TRO202603101234567890
退款金额：¥1740
预计到账时间：3-7 个工作日

您可以通过「查询订单状态」查看退票进度。
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 异常处理

- **订单不可退**：提示可能原因（未支付/超时限/已使用）
- **获取核损信息失败**：提示稍后重试或前往中旅旅行App
- **退票申请失败**：展示后台友好提示，引导重试或前往App
