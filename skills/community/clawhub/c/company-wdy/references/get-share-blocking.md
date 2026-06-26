# get-share-blocking - 股权冻结信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| executedPersonName | string | 被执行人名称 |
| stockOrgName | string | 冻结股权标的企业名称 |
| executeAmount | integer | 股权数额（单位：分，换算需÷100才是元）|
| executeCourtName | string | 执行法院名称 |
| executeNoticeNo | string | 执行通知文书号 |
| freezeState | string | 状态 |
| freezeBeginTime | string | 冻结开始日期 |
| freezeEndTime | string | 冻结结束日期 |
| dataFreezeId | long | 冻结信息ID |

## 特殊说明

- `executeAmount` 单位为分，展示时需 ÷100 换算为元