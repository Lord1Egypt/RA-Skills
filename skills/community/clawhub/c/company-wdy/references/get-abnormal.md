# get-abnormal - 经营异常

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| department | string | 列入部门 |
| abnormalDate | string | 列入日期 |
| abnormalReason | string | 列入原因 |
| removeDepartment | string | 移出部门 |
| removeDate | string | 移出日期 |
| removeReason | string | 移出原因 |