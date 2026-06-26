# get-judge-doc - 裁判文书信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| dataCaseId | string | 关联案件ID |
| caseNo | string | 案号 |
| caseReason | string | 案由 |
| caseAmount | integer | 案件金额（单位：分，换算需÷100才是元）|
| judgeResult | string | 裁判结果 |
| judgeTime | string | 裁判日期 |
| publishTime | string | 公布日期 |
| memberList | list | 案件关联方信息 |
| caseType | string | 案件类型 |

### memberList - 案件关联方信息

| 字段 | 类型 | 说明 |
|------|------|------|
| list | list | 关联信息 [{name, type, judgeResult}] |
| name | string | 人员身份名称 |

### list - 关联信息

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 名称 |
| type | int | 关联类型（1-企业，2-人员） |
| judgeResult | string | 裁判结果 |

## 特殊说明

- `caseAmount` 单位为分，展示时需 ÷100 换算为元