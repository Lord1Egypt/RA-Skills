# get-risk-index - 企业风险指数

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orgId | long | 是 | 企业ID |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| entityId | string | 企业ID |
| region | string | 地区 |
| industry | string | 行业 |
| riskScore | bigdecimal | 综合风险指数（10-90分） |
| riskLevel | string | 风险等级（高风险/中风险/低风险/提示风险） |
| riskRank | integer | 风险排名 |
| calcDt | string | 计算日期 |
| sentimentWeight | string | 舆情风险权重 |
| legalWeight | string | 法律风险权重 |
| operationalWeight | string | 运营风险权重 |
| financialWeight | string | 财务风险权重 |
| debtVsIndustry | string | 负债率与行业均值差 |
| roeVsIndustry | string | ROE与行业均值差 |
| profitQualityRatio | string | 盈利质量比率 |
| debtToEquityRatio | string | 产权比率 |
| returnVolatility | string | 收益波动性 |
| operationalStabilityBase | integer | 运营稳定性基础分（0-100分） |
| financialHealthBase | integer | 财务健康度基础分（0-100分） |
| highRiskCombination | string | 高风险组合类型 |
| changeAnomalyFlag | string | 变更异常标志 |
| growthAnomalyFlag | string | 增长异常标志 |
| financialAnomalyFlag | string | 财务异常标志 |
| riskSignalCount | integer | 风险信号计数（0-8+） |
| changeFrequencyRisk | integer | 变更频率风险（0-100分） |
| efficiencyRisk | integer | 运营效率风险（0-100分） |
| growthRisk | integer | 成长性风险（0-100分） |
| profitabilityRisk | integer | 盈利能力风险（0-100分） |
| liquidityRisk | integer | 流动性风险（0-100分） |
| solvencyRisk | integer | 偿债能力风险（0-100分） |
| sentimentRiskScore | bigdecimal | 舆情风险分数 |
| legalRiskScore | bigdecimal | 法律风险分数 |
| operationalRiskScore | bigdecimal | 运营风险分数 |
| financialRiskScore | bigdecimal | 财务风险分数 |
| tipContribution | bigdecimal | 提示风险贡献分数 |
| lowContribution | bigdecimal | 低风险贡献分数 |
| mediumContribution | bigdecimal | 中风险贡献分数 |
| highContribution | bigdecimal | 高风险贡献分数 |
| riskCreditRating | integer | 信用评价 |

## 使用说明

- `orgId` 需从 `fuzzy-search-org` 接口的搜索结果中获取
- `riskScore` 范围 10-90 分，分数越高风险越大
- 各风险维度分数（如 `changeFrequencyRisk`）范围 0-100 分，越高风险越大
- 基础分（`operationalStabilityBase`、`financialHealthBase`）范围 0-100 分，越高越健康