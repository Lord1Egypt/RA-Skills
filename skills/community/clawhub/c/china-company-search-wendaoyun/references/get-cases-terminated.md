# get-cases-terminated - 终本案件信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |


## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| noExecuteAmount | long | 未履行金额（单位：分，换算需÷100才是元） |
| executeAmount | long | 执行标的（单位：分，换算需÷100才是元） |
| finalTime | string | 终本日期 |
| executeCourtName | string | 执行法院名称 |
| caseNo | string | 案号 |
| dataCaseId | string | 案件ID |
| dataCaseFinalId | string | 终本案件ID |
