# get-customer - 客户查询信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 搜索关键词（统一社会信用代码、企业全称） |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 50 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| source | string | 来源 |
| salesPercent | string | 销售占比 |
| salesAmount | string | 销售金额（万元） |
| logoUrl | string | Logo地址 |
| year | integer | 年份 |
| name | string | 客户名称 |