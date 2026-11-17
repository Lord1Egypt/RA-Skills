# 国家贸易概览-进出口趋势 API 参考

> 按月份维度返回指定时间范围内的进出口贸易总量趋势数据，支持游标分页。
> 接口路径：`POST /agent/customs/overview/trend`

## python脚本参数

- `--params`：JSON格式的查询参数（必填）

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| originCountryCode | string | 否 | 起运国二字码 |
| arrivalCountryCode | string | 否 | 抵运国二字码 |
| startDate | integer | 是 | 起始月份，如 202501 |
| endDate | integer | 是 | 结束月份，如 202512 |
| cursor | string | 否 | 游标（base64 编码的 {"start":N}） |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：趋势数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| cursor | string | 下一页游标（base64 编码） |
| list | array | 趋势数据列表 |

### list 条目字段

| 字段 | 类型 | 说明 |
|------|------|------|
| tradeDate | integer | 贸易日期，如 202501 |
| tradeTotal | integer | 贸易总量 |
