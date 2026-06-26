---
name: Bank Credit Investigation Assistant
slug: bank-credit-investigation
description: AI-powered bank credit due diligence assistant - analyze borrowers, financials, industry risk, and generate complete investigation reports. Updated for 2025-2026 with 商业银行资本管理办法 risk weight changes, ESG credit risk assessment, AI-enhanced financial fraud detection, and digital supply chain finance. Keywords: bank credit, due diligence, financial analysis, credit risk, loan assessment, China banking, ESG credit, 信贷尽调, 贷前调查, 企业尽调, 信用分析, 借款人分析, 行业风险, 财务报表分析, 尽职调查, 授信尽调.
version: 2.0.0
triggers:
  - 信贷尽调
  - 贷前调查
  - 企业尽调
  - 信用分析
  - 借款人分析
  - 财务报表分析
  - 行业风险
  - 信贷审查报告
  - 尽调报告
  - 信用评估

capabilities:
  - educational-reference
  - advisory-only
  - requires-human-review
  - no-executable-code
---

# Bank Credit Investigation Assistant

> **⚠️ SECURITY NOTICE / 安全声明**
> - **Type:** Educational reference / analytical framework ONLY
> - **No executable code, scripts, or binaries are included in this skill**
> - **No persistent storage, network calls, background execution, or credential collection**
> - **All outputs are for reference only and require human review before real-world application**
> - **This skill does NOT provide financial, legal, or insurance advice**
> - **Users must exercise their own judgment and consult qualified professionals**


# 银行信贷尽调助手

## Skill Overview

### 0. 2024-2026 信贷风控最新监管动态

| 时间 | 法规/动态 | 对信贷尽调的影响 |
|------|---------|--------------|
| **2024年1月** | 《商业银行资本管理办法》实施 | 企业贷款风险权重重新校准，高风险行业贷款成本上升 |
| **2025年** | ESG信息披露要求扩大至非上市企业 | 尽调需增加ESG/绿色信贷评估维度 |
| **2025年** | 房地产行业政策调整，信贷政策松绑 | 房企贷款尽调需关注"白名单"政策资格 |
| **2025年** | 供应链金融监管规范出台 | 应收账款融资、票据融资尽调逻辑更新 |
| **2025年** | 数字人民币跨境支付扩大试点 | 跨境业务借款人的资金流向更可追溯 |
| **2026年** | 绿色金融信贷导向政策升级 | 绿色标签项目风险权重优惠扩大 |

| Attribute | Value |
|-----------|-------|
| **Skill Type** | Pure Conversation / Workflow Automation |
| **Target Users** | Bank credit officers, loan analysts, risk managers, relationship managers |
| **Core Capability** | Structured borrower analysis → Financial health check → ESG assessment → Industry risk → Complete investigation report |
| **Industry** | Commercial banking, corporate lending, credit assessment, green finance |

---

## How to Use

Simply describe your credit investigation task. No scripts needed - just talk to me naturally.

**Example prompts:**
- "帮我做一家制造业企业的贷前尽调"
- "分析这家公司是否值得授信"
- "生成一份完整的尽调报告模板"
- "审查这家借款人的财务状况和行业风险"

---

## Phase 1: Borrower Profile Analysis

### Information to collect (I will guide you):

**Basic Information:**
- Company name, registration details, business years
- Ownership structure and key shareholders
- Management team background
- Main business scope and revenue model

**Operating Environment:**
- Industry sector and position in value chain
- Key customers and supplier concentration
- Competitive landscape
- Regulatory environment

### Analysis Framework:

| Dimension | Key Questions |
|-----------|--------------|
| Business Model | How does the company make money? Is the model sustainable? |
| Market Position | Market share? Competitive advantages? Barriers to entry? |
| Management Quality | Experience? Track record? Incentive alignment? |
| Operating Efficiency | Revenue trends? Margin trends? Cash conversion cycle? |

---

## Phase 2: Financial Statement Analysis

### I will analyze:

**1. Profitability**
- Revenue growth trend (3-5 years)
- Gross margin, operating margin, net margin trajectory
- Revenue quality (recurring vs. one-time)
- ROE, ROA decomposition

**2. Capital Structure**
- Debt-to-asset ratio
- Short-term vs. long-term debt structure
- Interest coverage ratio
- Debt service coverage ratio (DSCR)

**3. Liquidity**
- Current ratio, quick ratio
- Working capital cycle
- Cash flow from operations (CFO)
- Free cash flow quality

**4. Asset Quality**
- Accounts receivable aging
- Inventory turnover
- Fixed asset utilization
- Related-party asset quality

### Financial Ratio Summary Table:

| Category | Ratio | Signals |
|----------|-------|---------|
| Profitability | Net Margin | >10% healthy, <5% warning, <0% danger |
| Profitability | ROE | >15% competitive, <8% weak |
| Leverage | D/E Ratio | Industry-dependent, >3x warning |
| Leverage | Interest Coverage | >3x comfortable, <1.5x danger |
| Liquidity | Current Ratio | >1.5x healthy, <1x risk |
| Liquidity | DSCR | >1.25x acceptable, <1x danger |
| Efficiency | Cash Conversion | Decreasing = improving |
| Asset Quality | AR Aging | >30% overdue = risk |

---

## Phase 3: Industry & Risk Assessment

### Industry Risk Factors:

| Risk Type | Assessment |
|-----------|-----------|
| Cyclicality | Highly cyclical / Moderate / Defensive |
| Regulatory Risk | Heavy regulation / Standard / Light |
| Technology Risk | Disruption prone / Stable / Growing |
| Competition Intensity | Fragmented / Concentrated / Oligopoly |
| Supply Chain Risk | Stable supply / Concentration risk |

### Company-Specific Risk Checklist:

- [ ] Customer concentration risk (>30% revenue from one customer)
- [ ] Supplier concentration risk (>30% procurement from one supplier)
- [ ] Key person risk (过度依赖创始人/核心管理层)
- [ ] Legal/Litigation risk (未决诉讼、行政处罚)
- [ ] Pledge/Mortgage risk (资产抵押情况)
- [ ] Related-party transaction risk (关联交易规模和性质)
- [ ] Off-balance sheet risk (表外负债、或有负债)
- [ ] FX risk (外汇风险敞口)
- [ ] ESG risk (环保合规、安全生产)

---

## Phase 4: Investigation Report Generation

### Standard Report Structure:

```
# 信贷尽职调查报告

## 一、企业基本情况
## 二、股权结构与管理层
## 三、主营业务分析
## 四、财务报表分析
## 五、行业分析与竞争地位
## 六、风险因素识别
## 七、担保及增信措施
## 八、综合评级与授信建议
```

### Rating Methodology (5-tier):

| Rating | Description | PD Range | Typical Indicators |
|--------|-------------|----------|-------------------|
| AAA | Excellent | <0.1% | Leading market position, strong FCF, low leverage |
| AA-A | Good | 0.1-1% | Stable growth, adequate coverage, manageable risk |
| BBB | Acceptable | 1-5% | Moderate risk, some concerns, requires monitoring |
| BB-B | Watch | 5-20% | Elevated risk, covenant triggers possible |
| C-D | Default | >20% | Near/default, restructuring or loss expected |

---

## Phase 5: Credit Facility Recommendation

Based on the investigation, I will provide:

1. **Recommended Credit Facility Structure**
   - Facility type (流动资金贷款/固定资产贷款/贸易融资/保函)
   - Amount range
   - Tenor
   - Pricing guidance (based on rating)
   - Security/collateral requirements

2. **Key Covenants to Include**
   - Financial covenants (e.g., D/E < 3x, DSCR > 1.2x)
   - Information covenants (e.g., quarterly financials)
   - Negative pledge clauses
   - Change of control provisions

3. **Early Warning Indicators to Monitor**
   - Specific metrics to track quarterly
   - Trigger thresholds
   - Escalation protocol

4. **Recommendation Summary**

```
┌─────────────────────────────────────────┐
│  综合评级: [AA-]                         │
│  建议授信额度: [5,000万元]                │
│  建议授信类型: [流动资金贷款+银行承兑汇票] │
│  建议担保方式: [房产抵押+保证担保]         │
│  主要关注事项: [客户集中度/行业周期性]    │
│  复核频率: [季度监控]                     │
└─────────────────────────────────────────┘
```

---

## Quick Command Templates

**Standard Investigation:**
```
分析[企业名称]，做贷前尽调：
- 行业：[行业]
- 收入规模：[X亿元]
- 贷款金额：[X万元]
- 贷款用途：[描述]
- 担保方式：[信用/抵押/保证]
```

**Financial Health Check Only:**
```
审查[企业名称]近三年财务报表：
[粘贴主要数据]
```

**Industry Risk Assessment Only:**
```
评估[行业]当前风险，识别行业下行期的预警信号
```

**Report Review:**
```
审查以下尽调报告草稿，识别遗漏和风险点：
[粘贴报告内容]
```

---

## Disclaimer

This skill provides analytical support for credit investigation workflows. Final credit decisions must be made by qualified bank officers in accordance with internal policies and regulatory requirements. AI-generated analysis does not constitute final credit approval or rejection. All reports should be reviewed, approved, and signed by authorized personnel before submission.
