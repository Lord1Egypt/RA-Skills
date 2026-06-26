# get-labour-arb - 劳动仲裁送达报告

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| publishDate | string | 公告日期 |
| applicantName | string | 原告名称 |
| respondentName | string | 被告名称 |
| caseNo | string | 案号 |