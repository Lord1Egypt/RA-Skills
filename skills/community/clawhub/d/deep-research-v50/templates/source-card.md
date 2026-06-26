# 来源卡片模板 (Card Template)

> 版本：2.1 - 强制数据提取版

---

## 卡片格式（必须按此格式填写）

```markdown
---
source_id: card-{{001}}
type: academic|industry|market|policy
title: {{完整标题，禁止缩写}}
authors: {{所有作者}}
publication: {{期刊/机构/公司}}
year: {{具体年份}}
url: {{可点击链接}}
doi: {{DOI号（学术必须）}}
retrieved_at: {{YYYY-MM-DD}}
quality_score: {{0-10}}
---

## 1. 核心数据提取 (必须填具体数值)

| 指标 | 数值 | 单位/上下文 |
|------|------|-------------|
| 样本量 | | 如：n=1,298 |
| 主要结果 | | 如：AUC=0.85, p<0.01 |
| 成本影响 | | 如：节省$200/人 |
| 时间范围 | | 如：2020-2023 |
| 置信区间 | | 如：95% CI [0.78-0.92] |

## 2. 原文直接引用 (必须填)

> "{{此处复制原文至少 50 字，证明你真的读了}}"
> —— 来源：{{期刊名}}, {{年份}}, {{页码}}

## 3. 方法论简述

- **研究设计**：{{RCT/前瞻性队列/回顾性分析/横断面研究/系统综述}}
- **数据来源**：{{数据来源描述}}
- **关键变量**：{{自变量X, 因变量Y, 控制变量Z}}
- **统计方法**：{{回归/ML/Cox等}}
- **局限性**：{{作者自述的局限}}

## 4. 与本课题关联

- **支持观点**：{{具体观点}}
- **冲突观点**：{{如有}}
- **证据等级**：{{A/B/C/D}}

## 5. 检索信息

- **检索式**：{{当时用的搜索词}}
- **检索时间**：{{YYYY-MM-DD}}
- **检索工具**：{{OpenAlex/网页浏览/手动}}
- **质量评分明细**：
  - 时效性：/2.5
  - 权威性：/3
  - 方法论：/3
  - 可复现：/1
  - 透明度：/0.5

---

## 填写示例

```markdown
---
source_id: card-001
type: academic
title: Telemedicine Cost Savings in Outpatient Care: A Systematic Review
authors: Smith J., Johnson M., Williams R.
publication: JAMA Network Open
year: 2024
url: https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2812345
doi: 10.1001/jamanetworkopen.2024.12345
retrieved_at: 2026-03-19
quality_score: 8.5
---

## 1. 核心数据提取

| 指标 | 数值 | 单位/上下文 |
|------|------|-------------|
| 样本量 | n=15,420 | 3年回顾性研究 |
| 主要结果 | 节省23.5% | 门诊费用降低 |
| 成本影响 | $185/人 | 平均节省 |
| 时间范围 | 2020-2023 | 研究周期 |
| 置信区间 | 95% CI [18.2%-28.8%] | p<0.001 |

## 2. 原文直接引用

> "Our analysis of 15,420 outpatient visits found that telemedicine interventions 
> reduced overall healthcare costs by 23.5% (95% CI, 18.2%-28.8%; p<0.001) 
> compared with traditional in-person visits, with the largest savings in 
> primary care follow-ups and chronic disease management."
> —— 来源：JAMA Network Open, 2024, Vol.7(3), P.234

## 3. 方法论简述

- **研究设计**：回顾性队列研究
- **数据来源**：美国商业保险理赔数据库 2020-2023
- **关键变量**：远程医疗vs线下就诊、成本差异
- **统计方法**：多元回归分析 + 倾向得分匹配
- **局限性**：仅涵盖商业保险，结论可能不适用其他人群

## 4. 与本课题关联

- **支持观点**：远程医疗可有效降低门诊费用23.5%
- **冲突观点**：无明显冲突
- **证据等级**：A（高质量队列研究）

## 5. 检索信息

- **检索式**：("telemedicine" OR "virtual care") AND ("cost savings" OR "healthcare spending")
- **检索时间**：2026-03-19
- **检索工具**：OpenAlex API
- **质量评分明细**：
  - 时效性：2.0 (2年内)
  - 权威性：3.0 (JAMA)
  - 方法论：2.5 (大样本+统计方法)
  - 可复现：0.5 (数据部分公开)
  - 透明度：0.5 (利益冲突已声明)
```

---

*模板版本：2.1 | 最后更新：2026-03-19*
