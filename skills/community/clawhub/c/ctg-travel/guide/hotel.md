# 酒店预订操作指南

**触发条件**：预订/查询酒店

> **接口文档**：调用接口前请查阅 [api/hotel.json](../api/hotel.json)，获取完整的 method、category、subCategory、action 及参数定义。

---

## 核心流程

```
1. hotel.search → 查询酒店列表，入参：cityName、arrivalDate、departureDate、page、pageSize
2. hotel.detail → 获取房型列表，入参：hotelId、arrivalDate、departureDate
3. hotel.validatePrice → 验价（可选），入参：resourceItemId、checkInDate、checkOutDate、roomCount
4. getPassengerList(orderType=1) → 入住人列表；无入住人则调用 savePassenger 新增
5. hotel.createOrder → 创建订单，入参：resourceItemId、travelerList、price、checkInDate、checkOutDate、roomNum 等
6. getOrderStatus → 轮询订单状态（间隔10秒，最多6次）
7. orderDetail → 查询订单详情
8. hotel.cancelOrder → 取消未支付订单
9. orderHistory → 获取历史订单
```

---

## ⚠️ 下单规则（必须遵守）

1. **先确认入住人**：展示入住人列表 → 用户确认 → 再下单，禁止直接下单
2. **禁止重复下单**：同一需求只下单一次；失败最多重试1次；成功后绝不再下单

---

## 参数传递依赖

| 接口 | 入参来源 |
|------|----------|
| hotel.search | `cityName` ← 用户输入<br>`arrivalDate`、`departureDate` ← 用户输入 |
| hotel.detail | `hotelId` ← hotel.search 返回的 `hotelId` |
| hotel.validatePrice | `resourceItemId` ← hotel.detail 返回的房型 `resourceItemId` |
| hotel.createOrder | `resourceItemId` ← hotel.detail 返回<br>`travelerList` ← getPassengerList 返回<br>`price` ← 房型价格 |
| getOrderStatus | `orderBaseId` ← hotel.createOrder 返回 |

---

## 关键参数说明

### 订单状态码（getOrderStatus）
- `10`：处理中 → 继续轮询
- `12`：预订完成 → 引导支付
- `11`：预订失败 → 引导重试

### 取消订单参数（cancelOrder）
- `orderType`：1（酒店）
- `subOrderType`：1（必填，子订单类型）

### 日期格式
- arrivalDate/departureDate：`yyyy-MM-dd`（如 2026-03-15）

### travelerList 结构（createOrder 必填）
```json
[{
  "passengerId": 399,
  "name": "张三",
  "identityNo": "420102199007015297",
  "phoneNumber": "15000000000"
}]
```

---

## 调用命令示例

```bash
# 酒店列表
python scripts/apiexe.py call --method hotel.search --arg "{\"cityName\": \"武汉\", \"arrivalDate\": \"2026-03-15\", \"departureDate\": \"2026-03-17\", \"page\": 1, \"pageSize\": 10}"

# 酒店详情（房型列表）
python scripts/apiexe.py call --method hotel.detail --arg "{\"hotelId\": \"H123456\", \"arrivalDate\": \"2026-03-15\", \"departureDate\": \"2026-03-17\"}"

# 验价
python scripts/apiexe.py call --method hotel.validatePrice --arg "{\"resourceItemId\": \"RES_123\", \"checkInDate\": \"2026-03-15\", \"checkOutDate\": \"2026-03-17\", \"roomCount\": 1}"

# 入住人列表
python scripts/apiexe.py call --method getPassengerList --arg "{\"orderType\": 1}"

# 新增入住人
python scripts/apiexe.py call --method savePassenger --arg "{\"passengerName\": \"张三\", \"identityNo\": \"420102199007015297\", \"phoneNumber\": \"13800138000\"}"

# 创建订单
python scripts/apiexe.py call --method hotel.createOrder --arg "{\"memberId\": \"xxx\", \"phoneNumber\": \"15000000000\", \"orderSource\": 0, \"checkInDate\": \"2026-03-15\", \"checkOutDate\": \"2026-03-17\", \"roomNum\": 1, \"resourceItemId\": \"RES_123\", \"price\": 398, \"travelerList\": [{\"passengerId\": 399, \"name\": \"张三\", \"identityNo\": \"420102199007015297\", \"phoneNumber\": \"15000000000\"}]}"

# 订单状态轮询
python scripts/apiexe.py call --method getOrderStatus --arg "{\"orderBaseId\": \"HRO202603101234567890\"}"

# 订单详情
python scripts/apiexe.py call --method orderDetail --arg "{\"orderBaseId\": \"HRO202603101234567890\"}"

# 取消订单
python scripts/apiexe.py call --method hotel.cancelOrder --arg "{\"orderBaseId\": \"HRO202603101234567890\", \"orderType\": 1, \"subOrderType\": 1}"

# 订单历史
python scripts/apiexe.py call --method orderHistory --arg "{\"current\": 1, \"size\": 15}"
```

---

## 展示格式参考

**酒店列表**：一行一行展示，格式「① 酒店名  ⭐星级  ¥价格/晚  地址/标签」

**房型列表**：
- 每个房型最多展示5个报价政策
- 格式「① 房型名  床型 | 面积 | 设施」
- 政策格式「  - ¥价格/晚  政策说明(如:无早/含早)  剩余X间」
- 按价格从低到高排序

**展示示例**：
```
🛏️ 武汉汉口喜来登大酒店 可选房型

① 豪华双床房  双床 1.37米 50㎡ | 有窗 9-21层
  - ¥806/晚  无早  剩余5间
  - ¥860/晚  含1份早餐  剩余5间

② 豪华大床房  大床 2.03米 50㎡ | 有窗 9-21层
  - ¥851/晚  无早  剩余5间
  - ¥905/晚  含1份早餐  剩余5间
```

**订单详情**：订单号、酒店、房型、入住日期、入住人、状态、金额

**订单创建成功**：展示订单信息后，提示「请前往「中旅旅行」App 完成支付」

---

## 异常处理

- **后台异常**：保留用户已选内容，提示稍后重试
- **房型售罄**：建议选择其他房型或酒店
- **网络超时**：提示稍后重试或前往中旅旅行App

**重要**：异常时不要让用户重复提供信息，已选择的内容必须记住。

---

## 退订流程

- 当用户明确表达退订、申请退款、取消订单（已支付）意图时，加载 [guide/hotel-refund.md](hotel-refund.md)
