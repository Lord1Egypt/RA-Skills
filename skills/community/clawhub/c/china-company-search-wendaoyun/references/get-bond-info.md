# get-bond-info - 债券信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| issueScale | string | 发行规模（亿元） |
| remainTerm | string | 剩余期限（年） |
| bondTerm | string | 债券期限（年） |
| expireDate | string | 到期日期（如 "2022-01-01"） |
| issueDate | string | 发行日期（如 "2022-01-01"） |
| bondType | string | 债券类型 |
| bondName | string | 债券简称 |
| bondNo | string | 债券编号 |