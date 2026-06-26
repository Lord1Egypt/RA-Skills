# get-judicial-notice - 法院公告信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| publishDate | string | 刊登日期 |
| noticeOrgName | string | 公告人/公告机构名称 |
| caseReason | string | 案由 |
| caseNo | string | 案号 |
| memberList | list | 法院公告相关方信息集合 |
| dataCourtNoticeId | string | 法院公告ID |

### memberList - 法院公告相关方信息集合

| 字段 | 类型 | 说明 |
|------|------|------|
| list | list | 相关方实体列表 |
| code | string | 身份编码 |
| name | string | 身份名称 |

### list - 相关方实体列表

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 相关方名称 |
| id | string | 主键ID |
| type | int | 类型（1-企业，2-人员，0-其他） |