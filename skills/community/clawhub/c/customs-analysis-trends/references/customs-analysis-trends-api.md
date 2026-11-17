# 分析报告-贸易趋势 API 参考

> 查询指定HS编码在最近N个月的进出口贸易趋势数据。
> 接口路径：`POST /agent/customs/analysis/trends`

## python脚本参数

- `--params`：JSON格式的查询参数（必填）

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| hscode | string | 是 | HS编码，如"04021000" |
| countryCode | string | 否 | 国家代码（ISO 3166-1 alpha-2），如"CN" |
| recentMonths | integer | 是 | 最近月数，如12 |
| cursor | string | 否 | 分页游标（base64 编码） |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：贸易趋势数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| exportData | object | 出口数据（见AnalysisTrendsDataVo） |
| importData | object | 进口数据（见AnalysisTrendsDataVo） |

### AnalysisTrendsDataVo 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| countTrade | integer | 贸易次数 |
| countQuantity | integer | 数量 |
| countWeight | number | 重量 |
| countAmount | number | 金额 |
| totalDates | integer | 总月数 |
| tradeDates | array | 月度数据列表（见AnalysisTrendsMonthVo） |

### AnalysisTrendsMonthVo 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| month | string | 月份（YYYYMM格式），如"202406" |
| monthText | string | 月份文本，如"2024-06" |
| countTrade | integer | 贸易次数 |
| percentTrade | number | 贸易占比(%) |
| countQuantity | integer | 数量 |
| countWeight | number | 重量 |
| countAmount | number | 金额 |
| countBuyer | integer | 采购商数量 |
| countSeller | integer | 供应商数量 |
