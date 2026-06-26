# get-case-filing - 立案信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| memberList | list | 当事人信息 |
| caseReason | string | 案由 |
| registerDate | string | 立案日期 |
| courtName | string | 法院名称 |
| caseNo | string | 案号 |
| dataRegisterId | string | 立案信息ID |

### memberList - 当事人信息

| 字段 | 类型 | 说明 |
|------|------|------|
| code | string | 身份编码 |
| name | string | 身份名称 |
| list | list | 当事人信息列表 |

### list - 当事人信息列表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 实体主键 |
| type | int | 实体类型（1-企业，2-人员，0-其他） |
| name | string | 实体名称 |