# 公司贸易区域维度统计 API 参考

> 根据公司ID获取公司贸易的区域维度统计数据（交易次数、总金额、总数量、总重量、月度贸易趋势、国家分布等）。
> 接口路径：`POST /agent/customs/company/area/stats`

## python脚本参数

- `--params`：JSON格式的查询参数（必填）

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| companyId | integer | 是 | 公司ID |
| companyType | integer | 是 | 公司类型（1：供应商，2：采购商） |
| dateStart | integer | 否 | 开始时间（毫秒级时间戳） |
| dateEnd | integer | 否 | 结束时间（毫秒级时间戳） |
| port | string | 否 | 港口名称 |
| products | array[string] | 否 | 产品名称列表 |
| hscodes | array[string] | 否 | HS编码列表 |
| countryCodes | array[string] | 否 | 国家代码列表 |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：区域维度统计数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| countTrade | integer | 交易次数 |
| countAmount | integer | 总金额 |
| countQuantity | integer | 总数量 |
| countWeight | integer | 总重量 |
| totalDates | integer | 贸易月份总数 |
| tradeDates | array | 月度贸易趋势列表 |
| totalCountries | integer | 国家总数 |
| tradeCountries | array | 国家分布列表 |

### tradeDates 条目字段

| 字段 | 类型 | 说明 |
|------|------|------|
| month | integer | 月份时间戳（毫秒） |
| monthText | string | 月份文本，如 "2024-01" |
| tradeCount | integer | 交易次数 |

### tradeCountries 条目字段

| 字段 | 类型 | 说明 |
|------|------|------|
| countryCode | string | 国家代码 |
| tradeCount | integer | 交易次数 |
| percentTrade | number | 贸易占比（%） |
