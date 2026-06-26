### get-risk - 企业风险信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orgId | string | 是 | 企业ID |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| operationRisk | object | 经营风险 |
| lawRisk | object | 法律风险 |
| financeRisk | object | 财务风险 |
| opinionRisk | object | 舆情风险 |
| riskDynamic | object | 风险动态 |

### operationRisk / lawRisk / financeRisk / opinionRisk - 风险结构

| 字段 | 类型 | 说明 |
|------|------|------|
| totalRiskCnt | long | 风险条数 |
| riskInfo | string | 最近一次风险简述 |
| riskDetail | string | 最近一次风险明细 |
| riskTime | string | 最近一次风险记录时间 |

### riskDynamic - 风险动态

| 字段 | 类型 | 说明 |
|------|------|------|
| riskInfo | string | 最近一次风险动态简述 |
| riskTime | string | 最近一次风险动态记录时间 |