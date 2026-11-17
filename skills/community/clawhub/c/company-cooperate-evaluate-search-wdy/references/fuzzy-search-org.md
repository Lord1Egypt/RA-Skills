# fuzzy-search-org - 企业模糊搜索

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 关键词（最少 2 字符） |
| pageNum | integer | 否 | 页码，默认 1，每页 5 条 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| orgId | string | 企业ID |
| orgName | string | 企业名称 |
| usCreditCode | string | 统一社会信用代码 |
| incDate | string | 成立日期 |
| legalName | string | 法定代表人 |
| status | string | 企业状态（存续/在业等） |
| address | string | 企业地址 |

