# 国家贸易概览-采供商TopN API 参考

> 按国家维度返回供应商或采购商的TopN排名列表，支持游标分页。
> 接口路径：`POST /agent/customs/overview/top-n`

## python脚本参数

- `--params`：JSON格式的查询参数（必填）

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| originCountryCode | string | 否 | 起运国二字码 |
| arrivalCountryCode | string | 否 | 抵运国二字码 |
| year | integer | 是 | 年份 |
| companyType | integer | 是 | 公司类型：1=供应商，2=采购商 |
| cursor | string | 否 | 游标（base64 编码的 {"start":N}） |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：采供商TopN数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| cursor | string | 下一页游标（base64 编码） |
| list | array | 采供商TopN列表 |

### list 条目字段

| 字段 | 类型 | 说明 |
|------|------|------|
| year | integer | 年份 |
| companyId | integer | 公司ID |
| companyName | string | 公司名称 |
| tradeTotal | integer | 贸易总量 |
| latestTradeDate | integer | 最新贸易日期（时间戳） |
| quarterTradeTotal | integer | 季度贸易量 |
| monthTradeTotal | integer | 月度贸易量 |
| lastYearQuarterTradeTotal | integer | 去年季度贸易量 |
| lastYearMonthTradeTotal | integer | 去年月度贸易量 |
