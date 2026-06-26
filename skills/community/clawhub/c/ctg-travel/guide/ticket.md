# 门票订购操作指南

**触发条件**：购买/查询/预订门票、景区门票

---

## 核心流程

```
1. poi-list → 查询景点列表，入参：destinationCityName、keyword、current=1、size=10
2. poiDetail → 获取景点详情，入参：poiId(sourcePoiId)、ticketDate(可选)
3. poiRule → 门票规则，入参：resourceId(ticketList中选中项)
4. getPassengerList(orderType=3) → 乘客列表；无乘客则调用 savePassenger 新增
5. createTicketOrder → 创建订单，入参：resourceItemId、quantity、price、totalPrice、travelDate、travellerInfoList
6. getOrderStatus → 查询订单状态
7. orderDetail → 查询订单详情
8. ticket.cancelOrder → 取消未支付订单（仅仅取消未支付订单，如果用户已经购买了门票，需要走退票流程）
9. orderHistory → 获取历史订单
```

## 退票流程

- 当用户明确表达退票、我要退票、申请退款、把刚刚预定的门票退了、取消这张门票（已支付）意图时，加载 [guide/ticket-refund.md](ticket-refund.md)

---

## 参数传递依赖

| 接口 | 入参来源                                                                                                                                                |
|------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| poi-list | `destinationCityName` ← 用户 输入的 `城市名称`                                                                                                       |
| poiDetail | `poiId` ← poi-list 返回的 `sourcePoiId`                                                                                                                |
| poiRule | `resourceId` ← poiDetail 返回的 `ticketList[].resourceId`                                                                                              |
| createTicketOrder | `resourceItemId` ← poiDetail 返回的 `ticketList[].resourceItemId`<br>`price` ← `ticketList[].sellPrice`<br>`travellerInfoList` ← getPassengerList 返回的乘客信息 |

---

## 关键参数说明

### poiDetail 返参
- `businessStatus`：0=营业中，1=已关门，2=筹建中，3=暂停营业
- `ticketList`：门票列表，含 sellPrice(售价)、resourceItemId(下单用)、resourceId(规则用)、visitorInfoType、visitorInfoGroupSize

### visitorInfoType 游客数量规则
- 1=不需要游玩人信息
- 2=只需1位游玩人信息
- 3=每位游玩人都需要
- 4=每 visitorInfoGroupSize 个人需要1位
- 5=每张票需要 visitorInfoGroupSize 位

### 调用命令示例

```bash
# 景点列表（必填：destinationCityName）
python scripts/apiexe.py call --method poi-list --arg "{\"destinationCityId\": 1, \"destinationCityName\": \"北京\", \"keyword\": \"故宫\", \"current\": 1, \"size\": 10}"

# 景点详情（必填：poiId）
python scripts/apiexe.py call --method poiDetail --arg "{\"poiId\": 123456}"

# 门票规则（必填：resourceId）
python scripts/apiexe.py call --method poiRule --arg "{\"resourceId\": \"xxx\"}"

# 乘客列表
python scripts/apiexe.py call --method getPassengerList --arg "{\"orderType\": 3}"

# 新增乘客（必填：passengerName、identityNo、phoneNumber）
python scripts/apiexe.py call --method savePassenger --arg "{\"passengerName\": \"张三\", \"identityNo\": \"420102199007015297\", \"phoneNumber\": \"13800138000\"}"

# 创建订单（必填：phoneNumber、orderSource、resourceItemId、quantity、price、totalPrice、travelDate、travellerInfoList、name、mobile）
python scripts/apiexe.py call --method createTicketOrder --arg "{\"resourceItemId\": \"xxx\", \"quantity\": 1, \"price\": 60, \"totalPrice\": 60, \"travelDate\": \"2026-03-15\", \"phoneNumber\": \"13800138000\", \"name\": \"张三\", \"mobile\": \"13800138000\", \"orderSource\": 0, \"travellerInfoList\": [{\"passengerId\": 1, \"name\": \"张三\", \"idNumber\": \"420102199007015297\", \"idType\": \"ID\", \"phoneNumber\": \"13800138000\"}]}"

# 订单状态（必填：orderBaseId）
python scripts/apiexe.py call --method getOrderStatus --arg "{\"orderBaseId\": \"TRO202603151234567890\"}"

# 订单详情（必填：orderBaseId）
python scripts/apiexe.py call --method orderDetail --arg "{\"orderBaseId\": \"TRO202603151234567890\"}"

# 取消订单（必填：orderBaseId）
python scripts/apiexe.py call --method ticket.cancelOrder --arg "{\"orderBaseId\": \"xxx\", \"orderType\": 3, \"subOrderType\" : \"DOMESTIC_TICKET\"}"

# 订单历史
python scripts/apiexe.py call --method orderHistory --arg "{\"current\": 1, \"size\": 15}"
```

### travellerInfoList 结构（createTicketOrder 必填）
```json
[{
  "passengerId": 1,   
  "name": "张三",
  "idNumber": "420102...",
  "idType": "ID",
  "phoneNumber": "138..."
}]
```

---

## ⚠️ 下单规则（必须遵守）
1. **禁止重复下单**：同一需求只下单一次；失败最多重试1次；成功后绝不再下单
2. **订单确认**：创建订单前必须向用户展示订单信息并确认，用户明确同意后再调用 createTicketOrder
---

---

## 展示格式参考

**景点列表**：一行一行展示，格式「① 景点名  标签 · 城市」

**门票列表**：格式「① 门票名  ¥价格/张」

**订单详情**：订单号、景点、门票、游玩日期、游客、状态、金额

**订单创建成功**：展示订单信息后，提示「请前往「中旅旅行」App 完成支付」

---

## 异常处理

- **后台异常**：保留用户已选内容，提示稍后重试
- **景点列表为空**：建议换关键词/换一批/换城市
- **网络超时**：提示稍后重试或前往中旅旅行App

**重要**：异常时不要让用户重复提供信息，已选择的内容必须记住。

---
