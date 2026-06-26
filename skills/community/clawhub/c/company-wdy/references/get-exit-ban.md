# get-exit-ban - 限制出境信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| caseNo | string | 案号 |
| releaseTime | string | 发布日期 |
| phone | string | 联系电话 |
| executeCourtName | string | 执行法院名称 |
| executeAmount | long | 执行标的（单位：分，换算需÷100才是元） |
| applicationList | list | 申请人信息 |
| executeList | list | 被执行人信息 |
| limitList | list | 限制出境对象信息 |
| dataLimitExitId | string | 限制出境ID |

### applicationList - 申请人信息

| 字段 | 类型 | 说明 |
|------|------|------|
| type | int | 类型（1-企业，2-人员） |
| id | string | 主键 |
| name | string | 名称 |

### executeList - 被执行人信息

| 字段 | 类型 | 说明 |
|------|------|------|
| type | int | 类型（1-企业，2-人员） |
| id | string | 主键 |
| name | string | 名称 |

### limitList - 限制出境对象信息

| 字段 | 类型 | 说明 |
|------|------|------|
| type | int | 类型（1-企业，2-人员） |
| id | string | 主键 |
| name | string | 名称 |

