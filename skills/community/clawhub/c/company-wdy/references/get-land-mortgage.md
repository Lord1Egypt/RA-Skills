# get-land-mortgage - 土地抵押

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| mortgageAmount | integer | 抵押金额（单位：分） |
| mortgageBeginTime | string | 抵押开始日期 |
| mortgageEndTime | string | 抵押结束日期 |
| mortgageArea | string | 抵押面积 |
| address | string | 地址 |

## 特殊说明

- `mortgageAmount` 单位为分，展示时需 ÷100 换算为元