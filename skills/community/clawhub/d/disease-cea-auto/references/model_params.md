# Model Parameter Reference Guide
# 模型参数参考手册

> 本文档供 disease-cea-auto Skill 在执行阶段三（参数搜索）时参考。
> This document guides Phase 3 (parameter search) of the disease-cea-auto Skill.

---

## 1. 常用健康状态效用值参考 / Utility Value Reference

| 疾病类型 / Disease | 健康状态 / State | EQ-5D 效用值 / Utility | 来源参考 / Source Hint |
|-------------------|-----------------|----------------------|----------------------|
| 慢性阻塞性肺疾病 COPD | 轻度 Mild | 0.78–0.85 | Rutten-van Mölken 2000 |
| COPD | 中度 Moderate | 0.65–0.75 | — |
| COPD | 重度/极重度 Severe | 0.40–0.58 | — |
| 类风湿关节炎 RA | 缓解 Remission | 0.80–0.88 | Anis 2009 |
| RA | 低疾病活动 LDA | 0.70–0.78 | — |
| RA | 中度活动 Moderate | 0.55–0.67 | — |
| RA | 高度活动 High | 0.38–0.50 | — |
| 肺癌 NSCLC | 缓解/PFS | 0.74–0.82 | Nafees 2008 |
| 肺癌 NSCLC | 进展 PD | 0.55–0.65 | — |
| IPF | 轻度 Mild | 0.75–0.80 | Loveman 2014 |
| IPF | 中度 Moderate | 0.55–0.65 | — |
| IPF | 重度 Severe | 0.30–0.42 | — |
| 2型糖尿病 T2DM | 控制良好 | 0.82–0.87 | Clarke 2002 |
| T2DM | 控制不佳 | 0.68–0.76 | — |
| T2DM | 并发症 Complications | 0.40–0.65 | — |
| 死亡 Death | — | 0.00 | — |

---

## 2. 中国人均 GDP 趋势 / China GDP per Capita Trend

| 年份 Year | 人均 GDP (元) / GDP per capita (CNY) | 同比增速 YoY |
|----------|--------------------------------------|------------|
| 2020 | 72,447 | +2.3% |
| 2021 | 80,976 | +11.8% |
| 2022 | 85,698 | +5.8% |
| 2023 | 89,358 | +4.3% |
| 2024 | ~94,000（估算，需联网核实）| ~+5.2% |

> **注意 / Note**: AI 在执行时**必须联网搜索最新值**，不得直接使用上表估算数字。
> **AI MUST web-search the latest official value from NBS at execution time.**

常用 1倍 GDP 作为 WTP 阈值（中国药物经济学评价指南 2020 推荐）。
1× GDP per capita is the standard WTP threshold (Chinese Guidelines 2020).

---

## 3. 模型结构选择指南 / Model Type Selection Guide

| 疾病特征 / Disease Feature | 推荐模型 / Recommended Model |
|---------------------------|------------------------------|
| 慢性、渐进性恶化（如 COPD、IPF、RA、糖尿病） | Markov 模型（年循环） |
| 急性感染、单次手术、疫苗预防 | 决策树 Decision Tree |
| 肿瘤（有 PFS / OS 数据） | Markov（PFS/PD/Death）或分区生存 |
| 急性发作 + 长期管理（哮喘、心血管） | 混合模型（决策树嵌套 Markov） |
| 事件驱动、个体异质性大 | 离散事件模拟 DES（高级选项） |

---

## 4. 中国药物费用参考来源 / Drug Cost Data Sources in China

| 来源 / Source | 说明 / Description | 网址 / URL |
|--------------|-------------------|-----------|
| 药智网 | 药品价格、中标价 | yaozhi.com |
| 国家医保局 | 医保谈判目录价格 | nhsa.gov.cn |
| 阳光采购平台 | 各省集采中标价 | （各省卫健委网站） |
| 中国知网/万方 | 国内成本测算研究 | cnki.net |
| PubMed | 英文成本研究 | pubmed.ncbi.nlm.nih.gov |

---

## 5. 常用转换概率估算方法 / Estimating Transition Probabilities

1. **直接来源** / Direct: 从 RCT 或 observational study 直接提取年度转移率。
2. **风险转换公式** / Rate-to-probability conversion:
   ```
   p = 1 - exp(-r × t)
   ```
   其中 r = 风险率（rate），t = 周期长度（years）。
3. **文献外推** / Extrapolation: 若无直接数据，使用同类疾病、相似人群的历史数据，并标注"外推"。

---

## 6. 敏感性分析变动范围推荐 / SA Variation Ranges

| 参数类型 / Parameter | 推荐范围 / Range | 说明 / Note |
|---------------------|----------------|-------------|
| 药物费用 Drug cost | ±20% | 价格波动、谈判降价 |
| 效用值 Utility | ±20% | EQ-5D 测量不确定性 |
| 转换概率 Trans. prob. | ±20% | 自然史不确定性 |
| 贴现率 Discount rate | 0%–8% | 指南推荐范围 |
| 时间范围 Time horizon | ±5年 | 模型结构不确定性 |
| WTP 阈值 WTP | 1×–3× GDP | 阈值敏感性 |

---

## 7. 报告引用格式 / Reference Format

**中文期刊格式：**
作者. 文题 [J]. 期刊名称, 年份, 卷(期): 页码. DOI.

**英文 AMA 格式：**
Author A, Author B. Title. *Journal*. Year;Vol(No):pages. doi:xxx.

---

*文档版本 / Doc version: 1.0 | 创建 / Created: 2026-04-27*
