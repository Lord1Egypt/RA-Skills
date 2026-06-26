# get-open-court - 开庭公告（司法）

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| memberList | list | 相关方信息 |
| courtOpenTime | string | 开庭时间 |
| courtName | string | 法院名称 |
| caseReason | string | 案由 |
| caseNo | string | 案号 |
| dataOpenCourtId | string | 开庭信息表ID |

### memberList - 相关方信息

| 字段 | 类型 | 说明 |
|------|------|------|
| list | list | 相关方信息列表 |
| name | string | 相关方身份名称 |
| code | string | 相关方身份编码 |

### list - 相关方信息列表

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 相关方名称 |
| type | int | 相关方类型（1-企业，2-人员） |
| id | string | 相关方主键 |