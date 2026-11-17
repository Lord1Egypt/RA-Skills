# 分析报告-概览 API 参考

> 按国家维度统计概览数据，返回各国供应商/采购商数量等信息。
> 接口路径：`POST /agent/customs/analysis/overview`

## python脚本参数

- `--params`：JSON格式的查询参数（必填）

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cursor | string | 否 | 分页游标（base64 编码） |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：概览数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| cursor | string | 下一页游标（base64 编码） |
| list | array | 概览数据列表 |

### list 条目字段

| 字段 | 类型 | 说明 |
|------|------|------|
| countryCode | string | 国家代码（ISO 3166-1 alpha-2） |
| countSeller | integer | 供应商数量 |
| countBuyer | integer | 采购商数量 |
| latestTradeDate | integer | 最近交易时间戳（毫秒） |
| latestTradeDateText | string | 最近交易日期文本，如"2024-06" |
