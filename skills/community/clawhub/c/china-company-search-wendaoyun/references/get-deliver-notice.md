# get-deliver-notice - 送达公告信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| memberList | list | 相关方信息列表 |
| releaseTime | string | 发布日期 |
| courtName | string | 法院名称 |
| caseReason | string | 案由 |
| caseNo | string | 案号 |
| noticeName | string | 公告名称 |
| dataDeliverNoticeId | string | 送达公告ID |

### memberList - 相关方信息列表

| 字段 | 类型 | 说明 |
|------|------|------|
| list | list | 相关方实体信息 |
| name | string | 相关方身份名称 |
| code | string | 相关方身份编码 |

### list - 相关方实体信息

| 字段 | 类型 | 说明 |
|------|------|------|
| type | int | 类型（1-企业，2-人员） |
| id | string | 主键 |
| name | string | 名称 |
