# get-open-court-arb - 开庭公告（劳动仲裁）

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| courtOpenTime | string | 开庭日期 |
| caseReason | string | 案由 |
| plaintiffName | string | 原告名称 |
| defendantName | string | 被告名称 |
| caseNo | string | 案号 |
| undertakeDept | string | 承办部门名称 |
| dataOpenCourtId | long | 开庭公告ID |