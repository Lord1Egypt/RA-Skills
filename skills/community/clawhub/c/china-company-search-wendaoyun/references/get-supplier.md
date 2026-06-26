# get-supplier - 供应商查询

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 搜索关键词（统一社会信用代码、企业全称） |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 50 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| detailList | List<Object> | 供应商信息列表（字段见下方 detailList 说明） |
| yearList | List<Integer> | 年份列表信息 |

### detailList - 供应商信息列表

| 字段 | 类型 | 说明 |
|------|------|------|
| source | string | 来源 |
| purchasePercent | string | 采购占比 |
| purchaseAmount | string | 采购金额（万元） |
| logoUrl | string | Logo地址 |
| name | string | 供应商名称 |
| id | long | 主键 |
| year | integer | 年份 |