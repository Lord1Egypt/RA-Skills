# get-simple-cancel - 简易注销

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| result | string | 简易注销结果 |
| publicDate | string | 公告日期 |
| regInstitute | string | 登记机关 |
| usCreditCode | string | 统一社会信用代码 |
| orgName | string | 企业名称 |
| objectionList | list | 异议信息 [{objectionDate, content, objectionName}] |
| promiseUrl | string | 全体投资人承诺书Url |