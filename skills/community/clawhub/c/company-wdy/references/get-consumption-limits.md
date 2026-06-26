# get-consumption-limits - 限制高消费信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| executeCourtName | string | 执行法院名称 |
| caseAmount | string | 涉案金额（单位：分，换算需÷100才是元）|
| limitHighObjName | string | 限制令对象名称（企业） |
| applicantName | string | 申请人名称 |
| releaseTime | string | 发布日期 |
| registerTime | string | 立案日期 |
| relatePersonName | string | 关联人名称 |
| caseNo | string | 案号 |
| dataLimitHighId | string | 限制高消费ID |

## 特殊说明

- `caseAmount` 单位为分，展示时需 ÷100 换算为元