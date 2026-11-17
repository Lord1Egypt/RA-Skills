# 国家贸易概览-交易汇总 API 参考

> 按国家维度统计年度贸易总量、季度贸易量、供应商/采购商数量等汇总数据。
> 接口路径：`POST /agent/customs/overview/summary`

## python脚本参数

- `--params`：JSON格式的查询参数（必填）

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| originCountryCode | string | 否 | 起运国二字码 |
| arrivalCountryCode | string | 否 | 抵运国二字码 |
| year | integer | 是 | 年份 |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：交易汇总数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| tradeTotal | integer | 年度贸易总量 |
| quarterTradeTotal | integer | 季度贸易量 |
| sellerCount | integer | 供应商数量 |
| buyerCount | integer | 采购商数量 |
