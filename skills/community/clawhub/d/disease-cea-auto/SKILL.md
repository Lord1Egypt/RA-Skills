---
name: disease-cea-auto
description: >
  疾病药物经济学自动评价 Skill — 对任意指定疾病，自动设计适合的 Markov / 决策树模型框架，
  联网遴选当前最常用治疗药物，搜索模型参数（有效率、AE率、效用值、费用等），
  以中国最新人均 GDP（1倍）为 QALY 支付阈值，计算每种药物的增量成本效果比（ICER）与
  货币化净收益（NMB），从大到小排序，最终输出完整 Python 代码 + 科学论文格式报告。

  Disease Pharmacoeconomics Auto-Evaluation Skill — For any specified disease, automatically designs
  an appropriate Markov or decision tree model framework, identifies the most commonly used treatment
  drugs through web-based search, retrieves model parameters (response rate, adverse event rate,
  utility values, costs, etc.), uses China's latest per capita GDP (1×) as the WTP threshold per QALY,
  calculates ICER and NMB for each drug, ranks from highest to lowest, and outputs complete Python
  code plus a scientific paper–style report.

  触发词：药物经济学评价、CEA、成本效果分析、ICER、NMB、多药对比、治疗方案比较、
  cost-effectiveness analysis, economic evaluation, multiple drugs, QALY, NMB ranking。
---

<!-- ============================================================
     SKILL: disease-cea-auto  ·  v1.0  ·  2026-04-27
     Disease-Specific Pharmacoeconomic Auto-Evaluation
     中文 / English Bilingual Skill
     ============================================================ -->

# Disease-Specific Pharmacoeconomic Auto-Evaluation Skill
# 疾病药物经济学自动评价 Skill

---

## 概述 / Overview

本 Skill 帮助你对**任意指定疾病**完成一次端到端的药物经济学评价：
自动确定模型框架 → 遴选主流药物 → 联网搜索参数 → 运行成本效果分析 →
以我国最新人均 GDP（1倍）为支付阈值计算货币化净收益（NMB）→ 排序输出报告与 Python 代码。

This Skill performs an end-to-end pharmacoeconomic evaluation for **any specified disease**:
auto-design model → select key drugs → web-search parameters → run CEA →
compute NMB using China's latest GDP per capita (1×) as WTP threshold → rank and report.

---

## 执行流程 / Execution Workflow

### 阶段一：模型框架设计 / Phase 1 — Model Design

**中文指令：**
1. 根据用户输入的疾病名称，判断疾病是**慢性进展性（chronic/progressive）** 还是
   **急性/治愈性（acute/curative）**：
   - 慢性进展性疾病 → 使用 **Markov 模型**（状态：通常含疾病缓解期、进展期、重度/终末期、死亡）
   - 急性/治愈性疾病 → 使用 **决策树模型**（分支：治疗成功、治疗失败、不良反应）
   - 如同时存在急性发作和长期管理（如哮喘、心血管病） → 混合模型
2. 明确说明模型的**健康状态定义、循环周期（cycle length）、时间范围（time horizon）、
   贴现率（discount rate）**，并解释设定依据。
3. 以中英文表格列出模型参数清单（见阶段二）。

**English Instructions:**
1. Based on the disease provided, classify as **chronic/progressive** or **acute/curative**:
   - Chronic/progressive → **Markov model** (states: typically remission, mild, moderate, severe, death)
   - Acute/curative → **Decision tree** (branches: success, failure, AE)
   - Mixed (acute exacerbations + long-term, e.g., asthma, CVD) → Hybrid model
2. State the model's **health states, cycle length, time horizon, discount rate**, with justification.
3. List all required parameters in a bilingual table (see Phase 2).

---

### 阶段二：药物遴选 / Phase 2 — Drug Selection

**中文指令：**
1. 使用 `web_search` 联网搜索该疾病**当前国内外最常用/一线/二线治疗药物**，
   参考来源：中国临床指南、国家医保目录、UpToDate、PubMed、药智网等。
2. 遴选标准：优先纳入①中国医保目录内药物；②国内外指南推荐的一线/二线药物；
   ③近5年上市或获批的代表性新药（如有）。
3. 遴选数量：**不超过20种**代表性药物/方案，确保覆盖不同作用机制和费用区间。
4. 以表格输出：药物名称（中英文）、适应症、作用机制、是否医保、上市年份。

**English Instructions:**
1. Use `web_search` to find current **first-line/second-line drugs** for the disease,
   referencing Chinese clinical guidelines, NRDL, UpToDate, PubMed, etc.
2. Selection criteria: ① NRDL-listed drugs; ② guideline-recommended drugs;
   ③ representative new drugs approved in the last 5 years (if any).
3. Target **no more than 20 representative drugs/regimens** covering different mechanisms and cost ranges.
4. Output as a bilingual table: drug name (CN/EN), indication, mechanism, NRDL status, approval year.

---

### 阶段三：参数搜索 / Phase 3 — Parameter Search

**中文指令：**
对每种遴选药物，使用 `web_search` 搜索以下参数（**每个参数均需注明文献来源**）：

| 参数类型 | 说明 | 优先来源 |
|----------|------|----------|
| 临床疗效 | 有效率、ORR、PFS、OS（适用时）| RCT、Meta分析 |
| 效用值（utility）| 各健康状态下的 QoL 权重（0-1）| EQ-5D 研究 |
| 药物费用 | 年均药品费用（元）| 国家医保谈判价、药智网、公立医院价格 |
| 疾病管理费用 | 门诊/住院/辅助检查费用（元/年）| 国内成本测算研究 |
| 不良反应率及处理费用 | 3/4级 AE 发生率及对应费用 | RCT、安全性数据 |
| 转换概率（Markov） | 各状态间年转换概率 | RCT、自然史研究 |

若某参数无直接文献支撑，优先参考同类药物或同类疾病研究，并标注"外推"。

**English Instructions:**
For each selected drug, use `web_search` to retrieve (**cite every source**):

| Parameter | Description | Priority Source |
|-----------|-------------|-----------------|
| Clinical efficacy | Response rate, ORR, PFS, OS | RCT, meta-analysis |
| Utility values | QoL weights per health state (0–1) | EQ-5D studies |
| Drug cost | Annual drug cost (CNY) | NRDL negotiated price |
| Disease management cost | Outpatient/inpatient/diagnostic (CNY/yr) | Chinese cost studies |
| AE rate & cost | Grade 3/4 AE rate and management cost | RCT safety data |
| Transition probabilities | Annual transition probs between states | RCT, natural history |

If a parameter lacks direct evidence, extrapolate from analogous drugs/diseases and label as "extrapolated."

---

### 阶段四：人均 GDP 获取 / Phase 4 — WTP Threshold (GDP per Capita)

**中文指令：**
1. 使用 `web_search` 搜索"中国最新人均 GDP"（优先查国家统计局最新年度数据，通常在每年1月公布）。
2. 搜索词示例：`中国 2024 人均GDP 国家统计局`
3. 以 **1倍人均 GDP** 作为 QALY 的货币化支付阈值（WTP）。
4. 在报告中明确注明：数据来源、统计年份、具体数值（元/人/年）。

**English Instructions:**
1. Use `web_search` to find "China latest GDP per capita" (prefer NBS official annual data).
2. Sample query: `China 2024 GDP per capita National Bureau of Statistics`
3. Use **1× GDP per capita** as the WTP threshold for QALY valuation.
4. Report: data source, year, exact value (CNY/person/year).

---

### 阶段五：成本效果分析与 NMB 计算 / Phase 5 — CEA & NMB Calculation

**中文指令：**
1. 以**标准治疗或安慰剂**作为参照方案（比较组）。
2. 对每种药物计算：
   - **增量成本（ΔC）** = 干预组总成本 - 对照组总成本
   - **增量效益（ΔE）** = 干预组总 QALY - 对照组总 QALY
   - **ICER** = ΔC / ΔE（元/QALY）
   - **货币化净收益（NMB）** = ΔE × WTP - ΔC（元）
3. 按 NMB **从大到小**排列所有药物（NMB>0 表示具有成本效果，<0 则不具有）。
4. 同时进行**单因素敏感性分析**（至少对效用值、药物费用、转换概率各做±20%变动）。

**English Instructions:**
1. Use **standard of care or placebo** as the comparator.
2. For each drug, compute:
   - **Incremental cost (ΔC)** = Total cost (intervention) − Total cost (comparator)
   - **Incremental effectiveness (ΔE)** = Total QALY (intervention) − Total QALY (comparator)
   - **ICER** = ΔC / ΔE (CNY/QALY)
   - **Net Monetary Benefit (NMB)** = ΔE × WTP − ΔC (CNY)
3. Rank all drugs by NMB **descending** (NMB > 0 = cost-effective; < 0 = not cost-effective).
4. Perform **one-way sensitivity analysis** (±20% on utility values, drug costs, transition probabilities).

---

### 阶段六：Python 代码输出 / Phase 6 — Python Code Output

**中文指令：**
根据前述参数，生成完整可运行的 Python 代码，要求：
- 使用 `pandas`、`numpy`、`matplotlib` 标准库
- 代码结构：① 参数定义模块；② Markov/决策树计算模块；③ ICER/NMB 计算模块；④ 排序与可视化模块
- 生成两张图：① 成本效果平面散点图（CE plane）；② NMB 条形图（按大到小排序）
- 代码中所有变量名和注释使用**中英文双语**（变量名英文，注释中英文并行）
- 代码末尾调用 `print` 输出汇总结果表格

**English Instructions:**
Generate complete, runnable Python code based on the parameters collected, with:
- Libraries: `pandas`, `numpy`, `matplotlib`
- Structure: ① Parameter definition; ② Markov/decision-tree computation; ③ ICER/NMB calculation; ④ Ranking & visualization
- Two figures: ① CE plane scatter plot; ② NMB bar chart (descending order)
- All variable names in English; comments bilingual (CN+EN parallel)
- Final `print` output of summary table

---

### 阶段七：报告输出 / Phase 7 — Scientific Report Output

**中文指令：**
按以下科学论文格式输出简明结果报告（**每段内容均中英文并行**）：

```
# [疾病名称] 多药成本效果分析报告
# Cost-Effectiveness Analysis Report for [Disease Name] — Multiple Drugs

## 1. 研究背景 / Background
## 2. 研究方法 / Methods
   2.1 模型结构 / Model Structure
   2.2 研究视角与时间范围 / Perspective & Time Horizon
   2.3 数据来源 / Data Sources
   2.4 支付阈值 / WTP Threshold
## 3. 参数汇总表 / Parameter Summary Table（中英文表头）
## 4. 结果 / Results
   4.1 基础分析 / Base-Case Results（NMB排序表 + ICER表）
   4.2 敏感性分析 / Sensitivity Analysis
## 5. 结论与政策建议 / Conclusions & Policy Implications
## 6. 参考文献 / References
```

**English Instructions:**
Output a concise scientific report in the above structure,
with **every section bilingual (CN+EN parallel paragraphs)**.

---

## 参数默认值 / Default Settings

| 参数 / Parameter | 默认值 / Default | 说明 / Note |
|------------------|-----------------|-------------|
| 贴现率 Discount rate | 5% per year | 中国药物经济学指南推荐 / Chinese guideline |
| 循环周期 Cycle length | 1 year (chronic) / per episode (acute) | 依疾病类型调整 |
| 时间范围 Time horizon | 10–20 years (chronic) / 1–5 years (acute) | 依疾病类型调整 |
| 研究视角 Perspective | 卫生体系视角 / Healthcare system | 含直接医疗费用 |
| WTP 阈值 WTP threshold | 1× China GDP per capita (最新值，联网获取) | 依 Phase 4 实时获取 |
| 敏感性分析范围 SA range | ±20% on key parameters | 单因素 one-way |

---

## 质量控制要求 / Quality Control

**中文：**
- 每个参数来源必须注明（作者、年份、期刊/数据库）
- 若参数为外推或假设，必须标注并在敏感性分析中重点测试
- NMB 排序表必须包含置信区间或不确定性说明
- Python 代码必须可直接运行，不依赖外部私有数据文件

**English:**
- Every parameter must be cited (author, year, journal/database)
- Extrapolated/assumed parameters must be labeled and prioritized in SA
- NMB ranking table must include confidence intervals or uncertainty notes
- Python code must run standalone without private external data files

---

## 示例触发 / Example Triggers

- "帮我做2型糖尿病的药物经济学评价"
- "对比IPF常用药物的成本效果"
- "肺癌靶向药的ICER和NMB计算"
- "哪种NSCLC一线治疗方案净收益最高"
- "Do a multi-drug CEA for COPD"
- "Rank asthma biologics by NMB"
- "Compare cost-effectiveness of HER2+ breast cancer therapies"

---

*Skill version: 1.0 | 创建日期 / Created: 2026-04-27 | 作者 / Author: TLB*
