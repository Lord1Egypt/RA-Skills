# 公司贸易基础统计 API 参考

> 根据公司ID获取公司的贸易基础统计数据（交易次数、总重量、总数量、总金额、合作伙伴数量等）。
> 接口路径：`POST /agent/customs/company/stats`

## python脚本参数

- `--companyId`：公司ID（必填），如 `100001`
- `--companyType`：公司类型（必填），1=供应商，2=采购商

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| companyId | string | 是 | 公司ID |
| companyType | integer | 是 | 公司类型（1：供应商，2：采购商） |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：公司贸易基础统计数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| companyId | integer | 公司ID |
| companyType | integer | 公司类型（1：供应商，2：采购商） |
| countTrade | integer | 交易次数 |
| countWeight | integer | 总重量 |
| countQuantity | integer | 总数量 |
| countAmount | integer | 总金额 |
| countPartner | integer | 合作伙伴数量 |
| earliestTradeDate | string | 最早交易日期，如 "2020-01-15" |
| latestTradeDate | integer | 最后交易日期（毫秒级时间戳） |
