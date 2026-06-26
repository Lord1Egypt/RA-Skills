# 火车票订购操作指南

**触发条件**：购买/查询/预订火车票、车次

> **接口文档**：调用接口前请查阅 [api/train.json](../api/train.json)，获取完整的 method、category、subCategory、action 及参数定义。

---

## 核心流程

```
1. train.search → 查询车次列表，入参：fromStation、fromCityType、toStation、toCityType、ticketDate
2. train.detail → 查询车次详情，入参：fromStation、toStation、ticketDate、trainNo
3. getPassengerList(orderType=2) → 乘客列表；无乘客则调用 savePassenger 新增
4. train.createOrder → 创建订单，入参：orderItem(resourceItemId、fromDate、seatTypeName、 adultSalePrice、childSalePrice、hasSeat、passengers 等)
5. train.orderStatus → 轮询订单状态（占位中 → 成功/失败）
6. orderDetail → 查询订单详情
7. train.createOrder → 取消未支付订单（仅取消未支付订单，已支付需走退票流程）
8. orderHistory → 获取历史订单
```

---

## 参数传递依赖

| 接口                | 入参来源                                                                                                                                                                                       |
|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| train.detail      | `fromStation`、`toStation` 、`ticketDate`、`trainNo` ← train.search返回的 `trainInfos`中的`fromStation`、`toStation`、`fromDate`、`trainNo`, fromStation、toStation需要传站点名称，不是城市名称                                                         |
| train.createOrder | `resourceItemId` ← train.detail 返回的 `resourceItemId` 、`passengers` ← getPassengerList 返回的乘客信息 `adultSalePrice`和 `childSalePrice` ←  train.detail 返回的 `seatDetails`对象中的`price`和`childPrice` |

---
## 订单状态

订单详情->订单状态 展示 响应数据status 对应的'状态说明'，不要展示数字

| 状态(statusModule.status) |  状态说明 |
|------|----------|
| 10 |  占座中 |
| 11 |  占座失败 |
| 12 |  待支付 |
| 20 |  已取消 |
| 21 |  取消中 |
| 30 |  出票中 |
| 31 |  已出票 |
| 32 |  出票失败 |
| 33 |  出票失败 |
| 40 |  退票失败 |
| 41 |  退票中 |
| 42 |  已退票 |
| 43 |  已退票 |
| 44 |  已退票 |
| 50 |  部分退票失败 |
| 51 |  部分退票中 |
| 52 |  部分退票成功 |
| 53 |  部分退票成功 |
| 54 |  部分退票成功 |


## 调用命令示例


```bash

# 车次列表（必填：fromStation、fromCityType、toStation、toCityType、ticketDate）
python scripts/apiexe.py call --method train.search --arg '{"fromStation": "上海", "fromCityType": 2, "toStation": "北京", "toCityType": 2, "ticketDate": "2026-03-18"}'

# 车次详情（必填：fromStation、toStation、ticketDate、trainNo, fromStation、toStation需要传站点名称，不是城市名称）
python scripts/apiexe.py call --method train.detail --arg '{"fromStation": "上海", "toStation": "北京南", "ticketDate": "2026-03-18", "trainNo": "G101", "entranceSource": 0}'

# 乘客列表
python scripts/apiexe.py call --method getPassengerList --arg '{"orderType": 2}'

# 新增乘客（必填：passengerName, identityType，identityNo, phoneNumber）
python scripts/apiexe.py call --method savePassenger --arg '{"passengerName": "张三", "identityType": "ID", "identityNo": "420102199007015297", "phoneNumber": "15629199695"}'

# 创建订单
python scripts/apiexe.py call --method train.createOrder --arg '{"orderItem":{"hasSeat":false,"resourceItemId":"RW12ff1d2df9da42567f1b939bbfefe481","fromDate":"2026-02-12","seatTypeName":"无座","adultSalePrice":298,"childSalePrice":149,"passengers":[{"passengerId":316,"passengerType":0,"seatTypeName":"无座","parentId":null,"idType":"ID",idNumber":"420115199001010101","phoneNumber":"18872233316","name":"张飞"}]}}'

# 订单状态轮询
python scripts/apiexe.py call --method getOrderStatus --arg '{"orderBaseId": "SRO202603091138018328863"}'

# 订单详情
python scripts/apiexe.py call --method orderDetail --arg '{"orderBaseId": "FRO202603101234567890"}'

# 取消订单
python scripts/apiexe.py call --method train.cancelOrder --arg '{"orderBaseId": "SRO202603091138018328863", "orderType": 2, "subOrderType": "DOMESTIC_TRAIN", cancelReason": "不需要了", "terminalCode": "APP"}'

# 订单历史
python scripts/apiexe.py call --method orderHistory --arg '{"memberId": "15d6676f6be54d5099b106abeeecfcd6"}'
```

### passengers 结构（train.createOrder 必填）

```json
[{
  "passengerId": 1,
  "name": "张三",
  "idNumber": "420102...",
  "idType": "ID",
  "phoneNumber": "138...",
  "customerType": "0",
  "birthday": "1990-07-01"
}]
```

---

## 展示格式参考

**车次列表**：一行一行展示，格式「G458 武汉 07:55 → 上海虹桥 11:31  3小时36分 」

**车次详情**：格式「💺 二等座 ¥354 剩余99张 一等座 ¥575 剩余1张 商务座 ¥1132 剩余0张」，显示在每行车次列表下方，即换行显示

**订单详情**：订单号、车次、日期、乘客、舱位、状态、金额

**订单创建成功**：展示订单信息后，提示「请前往「中旅旅行」App 完成支付」

备注：车次列表、车次详情必须向用户展示，不可省略

---

## 异常处理

- **后台异常**：保留用户已选内容，提示稍后重试
- **车次列表、车次详情为空**：建议换日期/换车次
- **座位售罄**：建议选择其他车次或座位
- **网络超时**：提示稍后重试或前往中旅旅行App

**重要**：异常时不要让用户重复提供信息，已选择的内容必须记住。

---

## 退票流程

- 当用户明确表达退票、我要退票、申请退款、取消这张火车票（已支付、已出票）意图时，加载 [guide/train-refund.md](train-refund.md)