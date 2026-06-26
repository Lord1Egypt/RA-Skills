# get-equity-pledge - 股权质押

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| pledgeeNameList | list | 质权人列表 [{name, type}] |
| riskState | string | 股权质押状态 |
| publicTime | string | 公告日期 |
| pledgeName | string | 出质人名称 |