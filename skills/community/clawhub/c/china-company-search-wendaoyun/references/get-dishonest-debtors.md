# get-dishonest-debtors - 失信被执行信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| caseNo | string | 案号 |
| executeCourtName | string | 执行法院名称 |
| performStatus | string | 被执行人履行情况 |
| releaseTime | string | 发布日期 |
| executeAccordNo | string | 执行依据文号 |
| dishonestySituation | string | 失信被执行人行为具体情形 |
| caseAmount | integer | 涉案金额（单位：分，换算需÷100才是元）|

## 特殊说明

- `caseAmount` 单位为分，展示时需 ÷100 换算为元