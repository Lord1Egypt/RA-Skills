# get-gua-info - 担保信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| assureAmount | integer | 担保金额（单位：分，换算需÷100才是元）|
| assureBeginTime | string | 担保起始日 |
| assureEndTime | string | 担保终止日 |
| assureTerm | string | 担保期限（年） |
| assureName | string | 担保方式 |
| currency | string | 币种 |
| performState | string | 履行状态 |
| isRpt | string | 是否关联交易 |
| assuredEntityName | string | 被担保方名称 |
| assureEntityName | string | 担保方名称 |
| reportDate | string | 报告期 |
| transactionDate | string | 交易日期 |
| assureDealTime | string | 处理日期 |

## 特殊说明

- `assureAmount` 单位为分，展示时需 ÷100 换算为元