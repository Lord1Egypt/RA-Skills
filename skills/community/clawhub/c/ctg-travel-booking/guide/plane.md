# 机票订购操作指南

**触发条件**：购买/查询/预订机票、航班、飞机票

---

## 交互规范

> **核心原则**：
> 1. 列表结果必须以**表格形式完整展示**
> 2. 展示后给出**推荐选项**并说明理由
> 3. 每步等待用户确认后再推进
> 4. 舱位选择后需要和用户选择乘机人

### 步骤1：查询航班 (flightListV2)

**入参**：`fromCityName`、`toCityName`、`fromDate`（格式：yyyyMMdd，如 20260315）

**执行后**：表格展示 → 给出推荐 → 询问用户选择

**表格列**：序号、航班号、起飞时间、到达时间、出发机场、到达机场

**用户选择后**：记录 `extData`、`flightNo`

---

### 步骤2：查询舱位 (cabinList)

**入参**：`goExtData` ← 步骤1的 `flights[].extData`

**执行后**：表格展示 → 给出推荐 → 询问用户选择

**表格列**：序号、舱位类型、票价、机建费、燃油费、总价、剩余座位

**用户选择后**：记录 `resourceItemId`

---

### 步骤3：选择乘客 (getPassengerList)

**执行后**：
- 有乘客：表格展示 → 询问选择（可多选）→ 允许新增
- 无乘客：引导新增（姓名、身份证号、手机号）

**表格列**：序号、姓名、证件类型、证件号、手机号

**用户选择/新增后**：记录 `passengerIds`，询问联系人手机号

---

### 步骤4：创建订单 (flight.createOrder)

**入参**：`resourceItemId`、`goExtData`、`passengerIds`、`contactPhone`

**执行**：收集联系人手机号后**直接下单**，无需二次确认

**执行后**：下单成功 → 自动进入轮询

---

### 步骤5：状态轮询 (getOrderStatus)

**规范**：每3秒查询一次，最多10次，下单后**自动轮询**

| 状态码 | 处理 |
|--------|------|
| `1` 处理中 | 继续轮询，提示「正在为您占位，请稍候…」 |
| `10` 占位完成 | 轮询结束，展示订单，引导支付 |
| `9` 占位失败 | 轮询结束，引导重新预订 |

**成功展示**：订单号、航班、日期、舱位、乘客、金额、提示「请前往中旅旅行App完成支付」

---

## 核心流程

```
flightListV2(表格+推荐) → 用户选航班
    → cabinList(表格+推荐) → 用户选舱位
    → getPassengerList → 用户选/新增乘客 → 询问联系手机号
    → flight.createOrder(直接下单) → getOrderStatus(自动轮询)
    → 占位成功 → 引导支付
```

---

## 参数传递

| 接口 | 关键入参来源 |
|------|-------------|
| cabinList | `goExtData` ← flightListV2 的 `flights[].extData` |
| flight.createOrder | `resourceItemId` ← cabinList<br>`goExtData` ← flightListV2<br>`passengerIds` ← getPassengerList |

**注意**：`passengerIds` 为ID数组如 `[11,21]`，后端自动查询乘客详情。

---

## 异常处理

- **后台异常**：保留已选内容，提示稍后重试
- **航班/舱位为空**：建议换日期或航线
- **网络超时**：提示稍后重试或前往中旅旅行App

**重要**：异常时不清除已收集信息。

---

## 退票流程

用户表达退票意图时，加载 [guide/plane-refund.md](plane-refund.md)
