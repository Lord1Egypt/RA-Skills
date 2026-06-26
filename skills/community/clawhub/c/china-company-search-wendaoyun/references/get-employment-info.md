# get-employment-info - 企业招聘信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 搜索关键词（统一社会信用代码、企业全称） |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 50 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| education | string | 学历 |
| experience | string | 经验 |
| city | string | 城市 |
| provinceDesc | string | 省份描述 |
| provinceCode | integer | 省份Code |
| salary | string | 月薪 |
| releaseDate | string | 发布日期 |
| title | string | 职位标题 |
| orgName | string | 企业名称 |
| orgId | long | 企业ID |
| id | long | 企业招聘信息ID |

## 使用说明

- 此接口返回招聘信息**列表**，每条记录包含 `id` 字段
- 用户选中某条招聘信息后，可使用该条记录的 `id` 值调用 `get-employment-detail` 查询详细信息
