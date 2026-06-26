# get-tax-notice - 欠税公告

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| taxDepartment | string | 发布单位 |
| publishDate | string | 发布日期 |
| taxCategory | string | 欠税税种 |
| newOwnTaxBalance | integer | 当前发生新欠税余额（单位：分） |
| ownTaxBalance | integer | 欠税余额（单位：分） |

## 特殊说明

- 金额字段单位为分，展示时需 ÷100 换算为元