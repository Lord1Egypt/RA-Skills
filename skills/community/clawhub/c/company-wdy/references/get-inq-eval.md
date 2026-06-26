# get-inq-eval - 询价评估信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| partyList | list | 当事人信息 |
| ownerList | list | 标的物所有人信息 |
| inqResult | string | 询价结果（元） |
| subjectMatter | string | 标的物 |
| caseNo | string | 案号 |

### partyList - 当事人信息

| 字段 | 类型 | 说明 |
|------|------|------|
| entityName | string | 当事人名称 |
| entityCategory | int | 当事人类型（1-企业，2-人员） |
| entityId | string | 当事人主键 |

### ownerList - 标的物所有人信息

| 字段 | 类型 | 说明 |
|------|------|------|
| entityCategory | int | 所有人类型（1-企业，2-人员） |
| entityId | string | 所有人主键 |
| entityName | string | 所有人名称