---
name: Bank Credit Investigation Assistant
slug: bank-credit-due-diligence
description: AI-powered bank credit due diligence assistant - analyze borrowers, financials, industry risk, and generate complete investigation reports. Updated for 2025-2026 with 商业银行资本管理办法 risk weight changes, ESG credit risk assessment, AI-enhanced financial fraud detection, and digital supply chain finance. Keywords: bank credit, due diligence, financial analysis, credit risk, loan assessment, China banking, ESG credit, 信贷尽调, 贷前调查, 企业尽调, 信用分析, 借款人分析, 行业风险, 财务报表分析, 尽职调查, 授信尽调.
version: "5.0.0"
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
---

# Bank Credit Investigation Assistant
# 银行信贷尽调助手


### 银行监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 银行监管 | 2026年Q1：净息差管理压力持续，低成本负债竞争加剧 | 信贷尽调需关注净息差压力对借款人还款能力的影响 |
| 银行监管 | 理财产品信息披露'三清'（估值清晰、责任清晰、信息清晰）推进 | 信贷尽调需关注净息差压力对借款人还款能力的影响 |
| 银行监管 | 资本新规计量规则在特定上市银行实践参考已发布 | 信贷尽调需关注净息差压力对借款人还款能力的影响 |

> **数据截止**: 2026-05-25 | 来源：国家金融监督管理总局、安永Q1分析、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准

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


---

## 核心工作流程（Dianjin融合版）

### 第一步：借款人画像与信息收集

| 输入项 | 说明 | 默认值 |
|--------|------|--------|
| 借款人名称 | 企业全称或统一社会信用代码 | — |
| 所属行业 | 国标行业分类或用户指定 | — |
| 授信金额 | 拟申请授信额度（万元） | — |
| 授信品种 | 流贷/固贷/贸融/保函/银承 | 流贷 |
| 调查深度 | 快速筛查/标准尽调/深度尽调 | 标准尽调 |

**触发规则**：用户提及以下场景时触发
- 分析[企业名称]贷前尽调
- 生成[企业名称]尽职调查报告
- [企业名称]是否值得授信
- 审查[企业名称]财务风险

---

### 第二步：财务健康度深度分析（Dianjin精髓：财报分析）

#### 2.1 财务报表三维分析框架
| 分析维度 | 核心指标 | 风险信号 |
|---------|---------|---------|
| **盈利能力** | 营收CAGR、毛利率、净利率、ROE | 营收下滑、毛利率低于行业、ROE<8% |
| **资本结构** | 资产负债率、有息负债率、利息保障倍数 | 负债率>70%、利息保障<1.5x |
| **现金流** | 经营现金流/净利润、自由现金流 | 经营现金流持续为负 |
| **资产质量** | 应收账款周转、存货周转、其他应收款占比 | 应收账款账龄>1年占比高 |

#### 2.2 财务造假风险识别（Dianjin精髓：AI增强财务欺诈检测）
| 风险类型 | 识别方法 | 风险信号 |
|---------|---------|---------|
| 收入虚增 | 营收 vs 现金流、应收账款增速 vs 营收增速 | 营收增但现金流不增 |
| 成本虚减 | 毛利率异常高于同行、存货周转异常 | 毛利率超同行5pct以上 |
| 现金流操纵 | 经营现金流 vs 净利润、应收/应付异常 | 经营现金流持续低于净利润 |
| 表外负债 | 担保余额、未决诉讼、融资租赁 | 担保余额超净资产50% |

#### 2.3 财报质量评分（0-100分）
| 评分维度 | 单项满分 | 权重 | 评分依据 |
|---------|---------|------|---------|
| 盈利质量 | 25 | 25% | 营收现金含量、毛利率合理性 |
| 资产质量 | 25 | 25% | 应收账款/存货质量、其他应收款 |
| 现金流 | 25 | 25% | 经营现金流/净利润、自由现金流 |
| 负债结构 | 25 | 25% | 有息负债率、短期偿债压力 |

**财报质量等级**：
| 综合得分 | 质量等级 | 授信建议 |
|---------|---------|---------|
| 80-100 | 优质 | 可积极介入 |
| 60-79 | 良好 | 正常介入 |
| 40-59 | 一般 | 审慎介入 |
| 20-39 | 较差 | 限制介入 |
| 0-19 | 很差 | 禁止介入 |

---

### 第三步：股权穿透与关联方分析（Dianjin精髓：股权穿透与关联方分析）

#### 3.1 股权结构穿透分析
| 分析层级 | 关注重点 | 风险信号 |
|---------|---------|---------|
| 实际控制人 | 穿透至自然人/国资/集体 | 无法穿透、代持嫌疑 |
| 直接股东 | 股东性质（国资/民营/外资/混合） | 股东信用瑕疵 |
| 一致行动人 | 一致行动协议、表决权委托 | 控制权不稳定 |
| 员工持股/期权 | ESOP、股权激励 | 股权稀释风险 |

#### 3.2 关联方交易风险识别
| 关联方类型 | 交易类型 | 风险信号 |
|------------|---------|---------|
| 母公司/子公司 | 资金拆借、担保、购销 | 定价不公允、资金占用 |
| 兄弟公司 | 同业竞争、资产转让 | 掏空上市公司 |
| 关键管理人关联 | 薪酬、借款 | 利益输送 |
| 隐性关联方 | 前股东、前高管关联企业 | 隐蔽的利益输送 |

**关联方风险评分**：
- 低风险：关联交易占比<10%，定价公允，披露完整
- 中风险：关联交易占比10-30%，基本公允
- 高风险：关联交易占比>30%，定价不公允，披露不完整

---

### 第四步：行业与区域风险分析（Dianjin精髓：行业深度分析）

#### 4.1 行业风险量化评分
| 评分维度 | 单项满分 | 权重 | 评分依据 |
|---------|---------|------|---------|
| 政策环境 | 20 | 20% | 行业政策友好度、监管强度 |
| 行业景气度 | 20 | 20% | 行业增速、产能利用率、价格走势 |
| 竞争格局 | 15 | 15% | 行业集中度、进入壁垒 |
| 周期位置 | 15 | 15% | 周期阶段、上行/下行风险 |
| 技术变革 | 15 | 15% | 技术迭代风险、被替代风险 |
| 区域风险 | 15 | 15% | 区域财政健康度、产业升级 |

#### 4.2 区域风险分析（针对城投/地产/基建）
| 区域指标 | 计算方法 | 风险阈值 |
|---------|---------|---------|
| 一般预算收入 | 公共财政预算收入 | <50亿为弱区域 |
| 债务率 | 债务余额/一般预算收入 | >150%为高风险 |
| 土地财政依赖度 | 土地出让收入/财政收入 | >60%为高风险 |
| 再融资便利性 | 存量债券估值、新发债利差 | 利差>200bp为高风险 |

---

### 第五步：综合评级与授信建议（Dianjin精髓：风险评分机制）

#### 5.1 借款人综合评级模型
| 评级 | PD区间 | 建议授信策略 |
|--------|----------|------------|
| AAA | <0.1% | 积极介入，可信用授信 |
| AA+ ~ AA- | 0.1%-1% | 正常介入，抵押或强担保 |
| A+ ~ A- | 1%-5% | 审慎介入，强担保+贷后管理 |
| BBB+ ~ BBB- | 5%-20% | 限制介入，只减不增 |
| BB及以下 | >20% | 禁止介入，加快退出 |

#### 5.2 授信建议输出模板
```
┌─────────────────────────────────────────┐
│  借款人：[企业名称]                      │
│  综合评级：[AAA/AA+/...]                 │
│  建议授信额度：[X]万元                   │
│  建议授信品种：[流贷/固贷/贸融/...]      │
│  建议期限：[X]年                        │
│  建议担保方式：[信用/抵押/质押/保证]      │
│  定价建议：[LPR+X bp]                   │
│                                        │
│  主要关注事项：                          │
│  1. [风险点1]                         │
│  2. [风险点2]                         │
│  3. [风险点3]                         │
│                                        │
│  贷后管理要求：                          │
│  - 按[季度/月度]监测[指标1/指标2]       │
│  - 触发阈值为[具体数值]                 │
│  - 触发后执行[具体措施]                 │
└─────────────────────────────────────────┘
```

---

## 合规约束与审计规则（Dianjin精髓）

### 合规约束
1. **不适用边界**：本技能不适用于信贷审批决策、法律意见出具，此类需求需转交信贷审批部门或法律合规部门
2. **禁止承诺**：不使用"一定过审"" guaranteed approval"等承诺性表述，只能说"建议""可参考"
3. **禁止替代决策**：仅输出分析建议，最终授信决策由授信审批专员出具
4. **数据溯源**：财务数据、行业数据必须标注来源和日期，未标注来源的分析结论视为不合规
5. **隐私保护**：借款人未公开财务数据、商业秘密必须保密，不得外泄
6. **客观中立**：分析不得受银行既有授信关系、客户关系影响，须客观呈现风险

### 审计日志规则
每次执行后，生成审计日志至 `audit/` 目录，内容包含：
- 技能名称和版本
- 触发时间和用户标识
- 借款人名称和授信申请信息
- 核心分析步骤和输出结论
- 是否触发高风险预警
- 最终输出摘要

---

## 测试用例（Dianjin精髓）

| 用例ID | 输入场景 | 预期输出 | 验证点 |
|--------|---------|---------|---------|
| 用例1 | 分析某制造业企业，营收10亿，净利润5000万，负债率65% | 综合评级A-，建议授信5000万，关注负债率偏高 | 评级逻辑合理 |
| 用例2 | 分析某城投企业，所属区域债务率200%，土地出让收入占比70% | 综合评级BBB，建议限制介入，提示区域风险 | 区域风险识别准确 |
| 用例3 | 分析某科技企业，营收快速增长但经营现金流为负 | 综合评级BBB+，提示现金流风险，建议强担保 | 现金流风险识别 |

---

## 关联技能（Dianjin精髓）

- **银行市场研究**（`bank-market-research`）：提供行业深度分析、竞争格局、市场机会
- **银行监管报告**（`bank-regulatory-reporting`）：提供最新监管政策解读和合规要求
- **金融全场景风控**（`finance-omni-risk`）：提供行业风险量化模型和预警指标

---

*GitHub: https://github.com/gechengling/bank-credit-investigation*
