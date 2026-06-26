# Bayesian Analysis Result Schema

## Overview

技能保存的 JSON 文件记录一次完整的贝叶斯推理会话，包含假设、证据链和所有计算结果。文件可用于二次加载继续分析，也可被第三方工具读取。

## JSON Structure

```json
{
  "hypothesis": "string - 要评估的假设",
  "created_at": "ISO 8601 UTC timestamp",
  "evidence_chain": [
    {
      "name": "string - 证据名称",
      "prior": 0.3,
      "likelihood": 0.7,
      "false_positive": 0.2,
      "posterior": 0.6,
      "bayes_factor": 3.5,
      "bayes_factor_label": "moderate"
    }
  ],
  "sensitivity": {
    "prior": 0.3,
    "likelihood_range": [0.6, 0.9],
    "false_positive_range": [0.1, 0.3],
    "posterior_range": [0.4615, 0.7941],
    "bayes_factor_range": [2.0, 9.0]
  },
  "final_posterior": 0.6,
  "cumulative_bayes_factor": 3.5
}
```

## Fields

| Field | Type | Description |
|-------|------|-------------|
| hypothesis | string | 用户定义的假设文本 |
| created_at | string | 会话创建时间（ISO 8601） |
| evidence_chain | array | 按顺序记录的每条证据及其计算结果 |
| evidence_chain[].name | string | 证据描述 |
| evidence_chain[].prior | float | 本次更新的先验概率 (0, 1) |
| evidence_chain[].likelihood | float | P(E\|H), [0, 1] |
| evidence_chain[].false_positive | float | P(E\|¬H), [0, 1] |
| evidence_chain[].posterior | float | 计算得到的后验概率 |
| evidence_chain[].bayes_factor | float | 贝叶斯因子 = likelihood / false_positive |
| evidence_chain[].bayes_factor_label | string | 证据强度标签 |
| sensitivity | object\|null | 敏感性分析结果（如有） |
| sensitivity.prior | float | 敏感性分析使用的先验 |
| sensitivity.posterior_range | [float, float] | 后验概率的最小值和最大值 |
| final_posterior | float | 最终后验概率（最后一条证据的 posterior） |
| cumulative_bayes_factor | float | 累积贝叶斯因子（各证据因子之积） |

## Multi-Evidence Example

```json
{
  "hypothesis": "明天下雨",
  "created_at": "2026-05-02T10:00:00Z",
  "evidence_chain": [
    {
      "name": "乌云密布",
      "prior": 0.3,
      "likelihood": 0.7,
      "false_positive": 0.2,
      "posterior": 0.6,
      "bayes_factor": 3.5,
      "bayes_factor_label": "moderate"
    },
    {
      "name": "湿度很大",
      "prior": 0.6,
      "likelihood": 0.8,
      "false_positive": 0.3,
      "posterior": 0.8,
      "bayes_factor": 2.6667,
      "bayes_factor_label": "moderate"
    }
  ],
  "sensitivity": null,
  "final_posterior": 0.8,
  "cumulative_bayes_factor": 9.3333
}
```

## Secondary Loading

技能通过 Read 工具读取此 JSON 文件，提取 `final_posterior` 作为新先验，`evidence_chain` 中的证据名用于避免重复，继续添加新证据进行迭代分析。
