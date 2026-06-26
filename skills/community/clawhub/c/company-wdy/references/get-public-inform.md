# get-public-inform - 公示催告

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| publishAuthority | string | 发布机关名称 |
| billType | string | 票据类型 |
| faceValue | integer | 票面金额 |
| publishDate | string | 公告日期 |
| orgName | string | 企业名称 |
| billNumber | string | 票据号 |