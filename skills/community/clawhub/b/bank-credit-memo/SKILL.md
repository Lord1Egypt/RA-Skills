---
name: Bank Credit Memo Writer
slug: bank-credit-memo
description: AI-powered bank credit memo and credit analysis report writer - generate structured credit analysis reports, credit ratings, and facility recommendations. Updated for 2024-2026 Basel III risk weight framework, ESG/green credit assessment, real estate "whitelist" policy, and digital supply chain finance. Keywords: credit memo, credit analysis, credit rating, loan approval, Basel III, ESG credit, China banking, 信用备忘录, 授信报告, 信用分析报告, 评级报告, 信贷审批, 贷款评估, 额度测算, 担保评估.
version: "4.0.1"
triggers:
  - 信用备忘录
  - 授信报告
  - 信用分析报告
  - 评级报告
  - 授信建议
  - 贷款审批报告
  - 信用审查报告
  - 额度审批
  - 贷款评审报告
---

# Bank Credit Memo Writer
# 银行信用备忘录撰写助手


### 银行监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 银行监管 | 2026年Q1：信贷资产质量关注点增加，关注类贷款迁徙率需监控 | 授信备忘录模板需增加ESG和供应链金融评估模块 |
| 银行监管 | ESG信息披露扩大至非上市企业，授信备忘录需增加ESG评估 | 授信备忘录模板需增加ESG和供应链金融评估模块 |
| 银行监管 | 供应链金融监管规范更新，应收账款融资尽调逻辑调整 | 授信备忘录模板需增加ESG和供应链金融评估模块 |

> **数据截止**: 2026-05-25 | 来源：国家金融监督管理总局、安永Q1分析、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Skill Overview

| Attribute | Value |
|-----------|-------|
| **Skill Type** | Pure Conversation / Report Generation |
| **Target Users** | Bank credit officers, credit committee members, relationship managers |
| **Core Capability** | Data analysis → Credit rating → Facility recommendation → Full memo generation |
| **Industry** | Commercial bank credit approval, corporate lending |

---

## How to Use

Just tell me the borrower details and I will generate a complete credit memo.

**Example prompts:**
- "帮我写一份信用备忘录，对象是一家制造业企业"
- "生成一份AAA级客户的年度授信复核报告"
- "写一份信用评级下调分析报告"
- "起草一份新的授信申请报告"
- "帮我写一份绿色信贷项目的信用备忘录"

---

## Phase 1: Information Collection

### I will ask for:

**1. Basic Information**
- Company name, industry, main products/services
- Revenue scale (近3年收入)
- Borrowing history with your bank
- Purpose of this credit facility

**2. Financial Data (if available)**
- Latest balance sheet, income statement, cash flow statement
- Key ratios (I can calculate from raw data)

**3. Qualitative Information**
- Industry outlook
- Competitive position
- Management quality
- Recent developments

---

## Phase 2: Credit Analysis

### Financial Ratio Analysis:

| Category | Metrics Analyzed |
|----------|-----------------|
| Profitability | Net margin, ROE, ROA, Cost-to-income ratio |
| Capital Adequacy | D/E ratio, Debt service coverage |
| Liquidity | Current ratio, Quick ratio, CFO quality |
| Asset Quality | NPL ratio, Provision coverage, Write-off rate |
| Growth | Revenue CAGR, Asset growth, Market share trend |

### Industry Context:

- Industry cyclicality assessment
- Peer comparison (vs. sector average)
- Macro environment impact analysis
- Regulatory tailwinds/headwinds

### Business Risk Profile:

- Revenue concentration (top customer %)
- Margin sustainability (gross margin trend)
- Operating leverage (fixed vs. variable costs)
- Cash conversion cycle analysis

---

## Phase 3: Credit Rating (Internal 5-Tier + External Mapping)

### Internal Rating Scale:

| Rating | Grade | PD Estimate | Description |
|--------|-------|------------|-------------|
| AAA | Investment Grade | <0.1% | Market leader, excellent financials |
| AA | Investment Grade | 0.1-0.5% | Strong, low risk |
| A | Investment Grade | 0.5-2% | Good, stable |
| BBB | Investment Grade | 2-5% | Acceptable, moderate risk |
| BB | Speculative | 5-15% | Special mention, watch list |
| B | Speculative | 15-30% | Substandard |
| C/D | Loss/Default | >30% | Non-performing |

### Rating Drivers Analysis:

**Strengths (支持评级因素):**
1. [Key strength 1]
2. [Key strength 2]
3. [Key strength 3]

**Concerns (评级限制因素):**
1. [Key concern 1]
2. [Key concern 2]
3. [Key concern 3]

**Rating Outlook:** Stable / Positive / Negative / Developing

---

## Phase 4: Credit Memo Generation

### Standard Credit Memo Structure:

```markdown
# 信用备忘录
## Credit Memorandum

**报告编号**：[编号]
**客户名称**：[名称]
**报告日期**：[日期]
**报告撰写人**：[姓名]
**信用评级**：[AAA/AA+/AA/...]

---

## 一、授信申请摘要

### 1.1 授信申请人基本情况
[Company overview - 200 words]

### 1.2 本次授信申请要素
| 项目 | 内容 |
|------|------|
| 申请授信额度 | [X]万元 |
| 授信类型 | [流动资金贷款/固定资产贷款/银行承兑汇票/信用证/保函] |
| 授信期限 | [X个月/X年] |
| 利率/费率 | [LPR+X bp / X%] |
| 担保方式 | [信用/抵押/质押/保证] |
| 贷款用途 | [描述] |
| 还款来源 | [描述] |

---

## 二、客户信用分析

### 2.1 股权结构
[Ownership structure - key shareholders and UBO]

### 2.2 经营情况
[Business overview, revenue breakdown, key customers/suppliers]

### 2.3 财务分析
#### 2.3.1 盈利能力
| 指标 | [Year-3] | [Year-2] | [Year-1] | 行业平均 |
|------|---------|---------|---------|---------|
| 营业收入(万元) | | | | |
| 净利润(万元) | | | | |
| 毛利率 | | | | |
| 净利率 | | | | |
| ROE | | | | |
| ROA | | | | |

#### 2.3.2 偿债能力
| 指标 | [Year-3] | [Year-2] | [Year-1] | 指标值 |
|------|---------|---------|---------|---------|
| 资产负债率 | | | | |
| 流动比率 | | | | |
| 速动比率 | | | | |
| 利息保障倍数 | | | | |
| EBITDA(万元) | | | | |

#### 2.3.3 运营能力
| 指标 | [Year-3] | [Year-2] | [Year-1] | 指标值 |
|------|---------|---------|---------|---------|
| 应收账款周转天数 | | | | |
| 存货周转天数 | | | | |
| 应付账款周转天数 | | | | |
| 现金循环周期 | | | | |

### 2.4 外部评级参考
[Mapping from internal rating to external (Moody's/S&P/国内评级)]

---

## 三、行业分析与风险评估

### 3.1 行业概况
[Industry size, growth, regulatory environment]

### 3.2 竞争地位
[Market position, competitive advantages, barriers to entry]

### 3.3 风险因素识别
| 风险类型 | 风险描述 | 影响程度 |
|---------|---------|---------|
| 行业风险 | [描述] | [高/中/低] |
| 经营风险 | [描述] | [高/中/低] |
| 财务风险 | [描述] | [高/中/低] |
| 担保风险 | [描述] | [高/中/低] |
| 合规风险 | [描述] | [高/中/低] |

---

## 四、担保及增信措施

### 4.1 本次担保安排
| 担保方式 | 担保物/担保人 | 评估价值(万元) | 抵押率 |
|---------|-------------|---------------|-------|
| [抵押] | [物产名称/位置] | [X] | [X%] |
| [保证] | [保证人名称] | [X] | - |
| [质押] | [质押物] | [X] | [X%] |

### 4.2 担保覆盖率评估
- 担保敞口：[X]万元
- 担保价值：[X]万元
- 担保覆盖率：[X%] ≥ [基准要求]

---

## 五、综合评级与授信建议

### 5.1 综合评级
| 评级维度 | 权重 | 得分 | 加权得分 |
|---------|------|------|---------|
| 盈利能力 | 20% | | |
| 偿债能力 | 25% | | |
| 运营能力 | 15% | | |
| 资产质量 | 15% | | |
| 行业地位 | 15% | | |
| 管理质量 | 10% | | |
| **综合评分** | 100% | | |

**信用评级：[AAA/AA+/AA/A/BBB/BB/B/C]**

### 5.2 授信方案建议

| 授信要素 | 建议内容 |
|---------|---------|
| 授信额度 | [X]万元（较上期[X]万元变化及原因） |
| 授信类型 | [综合授信/专项授信] |
| 授信期限 | [X]年 |
| 利率定价 | [LPR+X bp / X%]（基于评级） |
| 担保要求 | [信用/满足[X]%抵押率] |
| 额度分配 | 流动资金[X]万 + 银行承兑[X]万 + 保函[X]万 |

### 5.3 关键授信条件（重要约束）
1. [条件1，如：D/E ≤ 3x]
2. [条件2，如：季度报告提交]
3. [条件3，如：资金归行率≥50%]

### 5.4 贷后管理重点
- 监控频率：[季度/半年]
- 关注指标：[DSCR / D/E / 销售回款]
- 预警阈值：[具体数值]
- 处置预案：[触发条件及措施]

---

## 六、审阅与批准

| 角色 | 姓名 | 日期 | 签名 |
|------|------|------|------|
| 客户经理 | | | |
| 风险经理 | | | |
| 分管审批 | | | |
| 审批委员会 | | | |

---

**免责声明**：本信用备忘录由AI辅助生成，仅供内部审贷参考。最终授信决策须经有权审批人审慎评估后作出。
```

---

## Report Variations

### Short Memo (简化版，额度≤500万):
```
适用场景：快速审批、续授信、转授权范围内
结构：摘要 + 核心财务数据 + 风险提示 + 授信建议 + 审批记录
字数：约800-1000字
```

### Green Credit Memo (绿色信贷专用版):
```
额外维度：碳排放/能耗/环保合规/绿色项目认定
政策契合度评估：[符合/部分符合/不符合绿色信贷导向]
ESG评级建议：[A/B/C]
```

### Group Credit Memo (集团客户版):
```
合并范围分析、关联交易风险、连带责任评估、
内部评级统一还是分别评级、集团限额管理
```

---

## Disclaimer

This skill generates credit analysis reports for bank internal use. AI-generated memos require thorough review by qualified credit officers and approval from appropriate credit committee authority. This tool does not replace professional credit judgment. All credit decisions remain the responsibility of authorized bank personnel.
