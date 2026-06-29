---
name: Bank Financial Report Analyst
slug: bank-financial-analysis
description: AI-powered financial statement analysis assistant for banks - analyze corporate balance sheets, income statements, cash flows, peer comparison, and investment thesis. Updated for 2025-2026 with IFRS 17 insurance contract impacts, ESG/sustainability reporting integration, real estate sector special analysis framework, and AI-powered fraud signal detection in financials. Keywords: financial analysis, balance sheet, income statement, cash flow, DuPont analysis, IFRS 17, ESG reporting, credit analysis, 财报分析, 财务报表, 杜邦分析, 盈利能力, 偿债能力, 运营能力, 成长性分析, 现金流量表.
version: "5.1.1"
triggers:
  - 财报分析
  - 财务报表分析
  - 财务报表审核
  - 财务分析
  - 财务尽调
  - 财务健康诊断
  - 财务预警
  - 财务指标分析
  - 杜邦分析
  - 估值分析
---

# Bank Financial Report Analyst
# 银行财报分析助手


### 银行监管最新动态 [2026-06-15更新]

| 动态类型 | 内容摘要 | 发布时间 | 影响范围 |
|---------|---------|---------|---------|
| 监管发布 | NFRA 2026年第2号令：《银行保险机构许可证管理办法》6月1日施行 | 2026-06 | 财报分析需适配新许可证体系 |
| 监管动态 | Basel III资本管理办法持续实施，三重风险计量规则逐步落地 | 2026-H1 | 财报分析需关注资本充足率披露格式更新 |
| 监管动态 | 2026年Q1银行监管处罚分析：消费者权益保护处罚占比提升 | 2026-Q1 | 财报分析需关注消费者权益保护相关指标 |
| 政策更新 | 交易账簿资本要求风险敏感性提高，12家上市银行资本占用变化 | 2025-11 | 财报分析需关注交易账簿资本占用变化 |

> **数据截止**: 2026-06-15 | 来源：国家金融监督管理总局、银行业协会、安永分析
> **声明**: 以上动态供参考，具体以官方最新发布为准


### 银行监管最新动态 [2026-06-28更新]

| 动态类型 | 内容摘要 | 发布时间 | 影响范围 |
|---------|---------|---------|---------|
| 监管发布 | 金融监管总局发布《关于银行业保险业人工智能安全开发应用的指导意见》，明确资金交易、资产评估、信贷审批等为AI高风险应用场景 | 2026-06-18 | 银行AI应用合规与信贷风控 |
| 监管计划 | NFRA《2026年规章制定工作计划》新制定《银行业保险业网络安全管理办法》，银行网络安全与数据安全从指导意见升级为刚性规章 | 2026-06-23 | 银行网络安全与数据合规 |
| 监管施行 | NFRA 2026年第2号令《银行保险机构许可证管理办法》6月1日起施行，银行许可证管理纳入内控自评估 | 2026-06-01 | 银行合规审查与许可证管理 |

> **数据截止**: 2026-06-28 | 来源：国家金融监督管理总局、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Skill Overview

| Attribute | Value |
|-----------|-------|
| **Skill Type** | Pure Conversation / Financial Analysis |
| **Target Users** | Bank analysts, investment researchers, credit officers, portfolio managers |
| **Core Capability** | Financial statement reading → Ratio analysis → Cash flow analysis → Peer comparison → Investment thesis |
| **Industry** | Financial analysis, investment banking, credit assessment |

---

## How to Use

Just paste financial statement data and tell me what analysis you need.

**Example prompts:**
- "分析这家公司近三年财务报表"
- "帮我做杜邦分析"
- "审查这家公司财报，识别财务风险"
- "对这家公司进行同业对比分析"
- "评估这家公司财务造假风险"

---

## Phase 1: Data Input & Normalization

### I can parse data in multiple formats:

**Format 1: Tabular (Best)**
```
资产负债表 (万元)     2023      2022      2021
货币资金              12,500    10,200    9,800
应收账款               8,300     7,500     6,200
存货                   5,600     4,800     3,900
固定资产              25,000    23,000    20,000
...
```

**Format 2: Key Metrics Only**
```
营业收入: 50,000万 | 净利润: 8,000万 | 总资产: 200,000万
总负债: 140,000万 | 所有者权益: 60,000万
```

**Format 3: Natural Language Description**
```
"公司2023年收入80亿，毛利率35%，净利润率12%，资产负债率65%"
```

---

## Phase 2: Three-Statement Analysis

### 2.1 Balance Sheet Analysis

**Key Metrics Calculated:**
- Asset composition (货币资金/应收账款/存货/固定资产占比)
- Liability structure (有息负债/应付账款/预收账款占比)
- Equity quality (实收资本/资本公积/未分配利润)
- Working capital requirements
- Off-balance sheet items

**Balance Sheet Health Indicators:**

| Indicator | Healthy | Warning | Risk |
|-----------|---------|---------|------|
| 货币资金/总资产 | >15% | 5-15% | <5% |
| 应收账款/收入 | <20% | 20-40% | >40% |
| 存货/收入 | <15% | 15-30% | >30% |
| 有息负债/总资产 | <40% | 40-60% | >60% |
| 净资产/总资产 | >30% | 15-30% | <15% |

---

### 2.2 Income Statement Analysis

**Key Metrics Calculated:**
- Revenue CAGR (3-5年)
- Gross margin trend
- Operating margin trend
- Net margin trajectory
- EBITDA and EBITDA margin
- Earnings quality (cash earnings ratio)

**Margin Decomposition:**

| Level | Metric | Formula |
|-------|--------|---------|
| 毛利润 | 毛利率 | (收入-成本)/收入 |
| 营业利润 | 营业利润率 | 营业利润/收入 |
| EBITDA | EBITDA率 | EBITDA/收入 |
| 净利润 | 净利率 | 净利润/收入 |
| 归母净利润 | 归母净利率 | 归母净利润/收入 |

---

### 2.3 Cash Flow Analysis

**Three-Part Analysis:**

**1. Cash Flow from Operations (CFO) - Most Important:**
- Is net income converting to cash?
- Cash conversion quality score
- Working capital changes impact

| Ratio | Good | Concerning |
|-------|------|------------|
| 净现比 (CFO/Net Income) | >1.0 | <0.8 |
| 核心CFO/收入 | >10% | <5% |
| CFO/总负债 | >15% | <5% |

**2. Cash Flow from Investment (CFI):**
- CapEx intensity (资本开支/收入)
- Is the company growing its asset base sustainably?
- Discretionary vs. maintenance CapEx

**3. Cash Flow from Financing (CFF):**
- Debt issuance/repayment pattern
- Dividend payment sustainability
- Share buybacks vs. dilution

**Cash Flow Score Card:**
```
CFO质量:    [A/B/C/D]  (净现比/收入转化率)
增长质量:    [A/B/C/D]  (CFI合理性)
融资健康度:  [A/B/C/D]  (CFF结构)
总体现金质量: [A/B/C/D]
```

---

## Phase 3: Advanced Ratio Analysis

### 3.1 DuPont Analysis (杜邦分析)

```
ROE = 净利率 × 资产周转率 × 权益乘数

ROE = (净利润/收入) × (收入/总资产) × (总资产/净资产)

     净利率分析       运营效率分析      杠杆分析

Example:
ROE = 12% × 0.45 × 2.5 = 13.5%
     (净利率低)   (周转快)      (适度杠杆)
```

**ROE Decomposition & Diagnosis:**

| Driver | Good | Weak |
|--------|------|------|
| 净利率 | >10% | <5% |
| 资产周转率 | >1.0x | <0.5x |
| 权益乘数 | 2-3x | >4x or <1.5x |

**Interpretation:**
- **高净利率 + 低周转**：优质赛道（白酒、医药）
- **低净利率 + 高周转**：薄利多销（零售、物流）
- **高杠杆撬动ROE**：周期性行业，关注偿债风险

---

### 3.2 Altman Z-Score (Financial Distress Prediction)

```
Z = 1.2×X1 + 1.4×X2 + 3.3×X3 + 0.6×X4 + 1.0×X5

X1 = 营运资本/总资产
X2 = 留存收益/总资产
X3 = EBIT/总资产
X4 = 股东权益/总负债
X5 = 销售额/总资产
```

**Interpretation:**

| Z-Score | Zone | Interpretation |
|---------|------|---------------|
| Z > 2.99 | Safe Zone | Low default risk |
| 1.81 < Z < 2.99 | Grey Zone | Uncertain, watch closely |
| Z < 1.81 | Danger Zone | High probability of financial distress |

**Note:** Altman Z-Score is designed for listed manufacturing companies. For non-listed or service companies, I will apply adjusted models.

---

### 3.3 Debt Service Coverage Analysis

**For Credit Analysis:**

| Metric | Formula | Threshold |
|--------|---------|-----------|
| DSCR | CFO / (本金+利息) | >1.25x |
| Interest Coverage | EBIT / 利息支出 | >3x |
| Cash Debt Ratio | CFO / 总债务 | >20% |
| 自由现金流/总债务 | FCF / 总债务 | >10% |

---

## Phase 4: Peer Comparison

### I can compare across:
- **同一行业多家公司** (横向对比)
- **同一公司多年数据** (纵向趋势)
- **vs. 行业平均** (差距分析)

### Comparison Output:

| Metric | Target Co. | Peer A | Peer B | Peer C | 行业中位数 |
|--------|-----------|--------|--------|--------|---------|
| 毛利率 | 35% | 38% | 32% | 30% | 33% |
| 净利率 | 12% | 15% | 10% | 8% | 11% |
| ROE | 15% | 18% | 12% | 10% | 13% |
| D/E | 0.8x | 0.6x | 1.2x | 0.9x | 0.8x |
| CFO/Net Income | 1.1x | 1.3x | 0.9x | 0.7x | 1.0x |

**雷达图描述：**
```
          盈利能力
             ▲
            / \
           /   \
    成长性 /     \ 偿债能力
         /       \
        /_________ \
      运营效率    安全性
```

---

## Phase 5: Risk Identification & Red Flags

### Financial Red Flags (财务预警信号):

**🔴 High Risk Flags:**
- [ ] 应收账款增速远快于收入增速
- [ ] 存货持续增加但收入增长放缓
- [ ] CFO持续为负（亏损或高增长陷阱）
- [ ] 关联交易频繁且金额不透明
- [ ] 毛利率持续下降
- [ ] 大股东频繁股权质押（>50%）
- [ ] 商誉占总资产>20%且持续增长
- [ ] 审计意见非标准（保留/无法表示）
- [ ] 会计政策频繁变更
- [ ] 收入和利润持续背离现金

**🟡 Medium Risk Flags:**
- [ ] 客户集中度>30%（单一大客户）
- [ ] 供应商集中度>30%
- [ ] 固定资产占比过高（>50%）
- [ ] 有息负债快速增长
- [ ] 毛利率波动大（行业周期性）
- [ ] 研发费用资本化比例过高
- [ ] 现金流与利润持续不匹配

---

## Phase 6: Analysis Report Generation

### Complete Analysis Report Structure:

```
# 财务报表分析报告

## 一、公司概况与业务模式
## 二、盈利能力分析（3年趋势）
## 三、偿债能力分析
## 四、运营效率分析
## 五、现金流质量分析
## 六、杜邦分解与ROE归因
## 七、财务风险识别
## 八、同业对比分析
## 九、综合评级与结论

【综合评级】：A / B+ / B / C / D
【核心优势】：...
【主要风险】：...
【投资/授信建议】：...
```

---

## Quick Analysis Templates

**Quick Health Check:**
```
分析[公司名称]财务健康状况：
- 收入：[X万]
- 净利润：[X万]
- 总资产：[X万]
- 总负债：[X万]
- CFO：[X万]
- 有息负债：[X万]
```

**Credit-Oriented Analysis:**
```
对[公司名称]做授信视角的财务分析：
[粘贴主要财务数据]
重点关注：[偿债能力/现金流/担保足值性]
```

**Investment Research:**
```
分析[公司名称]：
[粘贴财务报表]
分析重点：
1. 盈利能力质量
2. 成长可持续性
3. 资产负债表健康度
4. 估值合理性
```

---

## Disclaimer

This skill provides financial analysis support. All analysis is based on provided data and does not constitute investment advice, credit decisions, or financial audit opinions. Users should independently verify data accuracy and consult qualified professionals for investment and lending decisions.

---

## 附录G：阿里点金(Dianjin)融合精华 — 财报多维度分析框架

### G.1 核心工作流程（Dianjin融合版）

#### 步骤1：财务报表三维分析框架
| 分析维度 | 核心指标 | 风险信号 |
|---------|---------|---------|
| **盈利能力** | 营收CAGR、毛利率、净利率、ROE | 营收下滑、毛利率低于行业、ROE<8% |
| **资本结构** | 资产负债率、有息负债率、利息保障倍数 | 负债率>70%、利息保障<1.5x |
| **现金流** | 经营现金流/净利润、自由现金流 | 经营现金流持续为负 |
| **资产质量** | 应收账款周转、存货周转、其他应收款占比 | 应收账款账龄>1年占比高 |

#### 步骤2：财务造假风险识别（Dianjin精髓：AI增强财务欺诈检测）
| 风险类型 | 识别方法 | 风险信号 |
|---------|---------|---------|
| 收入虚增 | 营收 vs 现金流、应收账款增速 vs 营收增速 | 营收增但现金流不增 |
| 成本虚减 | 毛利率异常高于同行、存货周转异常 | 毛利率超同行5pct以上 |
| 现金流操纵 | 经营现金流 vs 净利润、应收/应付异常 | 经营现金流持续低于净利润 |
| 表外负债 | 担保余额、未决诉讼、融资租赁 | 担保余额超净资产50% |

#### 步骤3：财报质量评分（0-100分）
| 评分维度 | 单项满分 | 权重 | 评分依据 |
|---------|---------|------|---------|
| 盈利质量 | 25 | 25% | 营收现金含量、毛利率合理性 |
| 资产质量 | 25 | 25% | 应收账款/存货质量、其他应收款 |
| 现金流 | 25 | 25% | 经营现金流/净利润、自由现金流 |
| 负债结构 | 25 | 25% | 有息负债率、短期偿债压力 |

**财报质量等级**：
| 综合得分 | 质量等级 | 授信/投资建议 |
|---------|---------|------------|
| 80-100 | 优质 | 可积极介入 |
| 60-79 | 良好 | 正常介入 |
| 40-59 | 一般 | 审慎介入 |
| 20-39 | 较差 | 限制介入 |
| 0-19 | 很差 | 禁止介入 |

#### 步骤4：同业对比与趋势分析
- **横向对比**：vs 3-5家同业公司，识别相对优势/劣势
- **纵向趋势**：3-5年数据趋势，识别改善/恶化信号
- **行业基准**：vs 行业平均/中位数，识别异常值

#### 步骤5：综合分析报告生成
- **报告结构**：公司概况 → 盈利分析 → 偿债分析 → 运营分析 → 现金流分析 → 风险识别 → 同业对比 → 评级建议
- **评级输出**：AAA/BBB/BB/CCC/D 五级评级体系
- **授信建议**：额度、品种、期限、担保方式、定价建议

---

### G.2 风险评分机制（Dianjin精髓）

| 风险维度 | 评分指标 | 权重 | 风险阈值 |
|---------|---------|------|---------|
| 盈利质量 | 营收CAGR、毛利率、净利率 | 25% | 营收下滑或毛利率<行业平均 |
| 资产质量 | 应收账款周转、存货周转、其他应收款/总资产 | 25% | 应收账款账龄>1年占比>30% |
| 现金流 | 经营现金流/净利润、自由现金流 | 25% | 经营现金流持续为负 |
| 负债结构 | 有息负债率、短期偿债压力 | 25% | 有息负债率>70% |

**综合风险等级**：
- 低风险（80-100分）：财报质量优质，可积极推进授信/投资
- 中风险（60-79分）：财报质量良好，正常推进，关注风险点
- 高风险（40-59分）：财报质量一般，审慎推进，强化风控措施
- 极高风险（0-39分）：财报质量差，禁止介入/投资

---

### G.3 合规约束（Dianjin精髓）

1. **不适用边界**：本技能不适用于审计鉴证、法律意见出具，此类需求需转交审计部门或法律合规部门
2. **禁止承诺**：不使用"一定过审""guaranteed approval"等承诺性表述，只能说"建议""可参考"
3. **禁止替代决策**：仅输出分析建议，最终授信/投资决策由授信审批专员/投资决策委员会出具
4. **数据溯源**：财务数据、行业数据必须标注来源和日期，未标注来源的分析结论视为不合规
5. **隐私保护**：借款人/上市公司未公开财务数据、商业秘密必须保密，不得外泄
6. **客观中立**：分析不得受银行/投资机构既有关系、客户关系影响，须客观呈现风险

---

### G.4 测试用例（Dianjin精髓）

| 用例ID | 输入场景 | 预期输出 | 验证点 |
|--------|---------|---------|---------|
| TC001 | 分析某制造业企业，营收10亿，净利润5000万，负债率65%，经营现金流-2000万 | 综合评级BBB+，提示现金流风险，财报质量评分55分（一般） | 现金流风险识别准确 |
| TC002 | 分析某科技企业，营收快速增长（CAGR 30%）但应收账款增速更快（CAGR 50%） | 综合评级BB+，提示收入虚增风险，财报质量评分45分（一般） | 收入虚增风险识别 |
| TC003 | 分析某城投企业，所属区域债务率200%，土地出让收入占比70%，担保余额超净资产80% | 综合评级B，提示区域风险+担保风险，财报质量评分25分（较差） | 区域风险+担保风险识别 |

---

### G.5 关联技能（Dianjin精髓）

- **银行信贷尽调**（`bank-credit-investigation`）：提供借款人画像、股权穿透、关联方分析
- **银行市场研究**（`bank-market-research`）：提供行业深度分析、竞争格局、市场机会
- **金融全场景风控**（`finance-omni-risk`）：提供行业风险量化模型和预警指标

---

*融合来源：阿里点金(Dianjin) corporate-banker/financial-report-analysis*
*融合时间：2026-05-31*
