# get-pre-mediate - 诉前调解信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| memberList | list | 诉前调解相关方信息 |
| caseReason | string | 案由 |
| registerDate | string | 立案日期 |
| courtName | string | 法院名称 |
| caseNo | string | 案号 |
| dataPreMediateId | string | 诉前调解ID |

### memberList - 诉前调解相关方信息

| 字段 | 类型 | 说明 |
|------|------|------|
| list | list | 相关方信息 |
| code | string | 相关方身份CODE |
| name | string | 相关方身份名称 |

### list - 相关方信息

| 字段 | 类型 | 说明 |
|------|------|------|
| type | int | 相关方类型（1-企业，2-自然人） |
| id | string | 相关方主键 |
| name | string | 相关方名称 |