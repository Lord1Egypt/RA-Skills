# get-execute-info - 被执行信息（强制执行）

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| dataExecuteId | string | 被执行人ID |
| registerDate | string | 立案日期 |
| caseNo | string | 案号 |
| executeOrgName | string | 执行法院名称 |
| executeAmount | integer | 执行标的（单位：分，换算需÷100才是元） |
| possibleExecutorName | string | 疑似申请执行人名称 |

## 特殊说明

- `executeAmount` 单位为分，展示时需 ÷100 换算为元