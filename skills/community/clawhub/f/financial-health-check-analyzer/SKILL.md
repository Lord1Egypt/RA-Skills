---
name: Financial Health Check Analyzer
version: v1.0.0
tags: financial-health, wellness-assessment, personal-finance, financial-diagnosis, money-management
---

# Financial Health Check Analyzer

## Overview

Provides a multi-dimensional assessment of financial health with actionable improvement recommendations. This is a descriptive skill that provides templates, frameworks, and heuristic analysis without executing real code, accessing external APIs, or performing actual financial transactions.

## Trigger

Use this skill when the user wants to:
- get structured guidance on financial health check analyzer
- apply best-practice frameworks to their financial situation
- generate templates and checklists for financial planning

### Example prompts
- "Help me create a personal budget"
- "Analyze my cash flow forecast"
- "Check my expense categorization"
- "Assess my financial health"
- "Review my receivables aging"
- "Check invoice compliance"
- "Develop a pricing strategy"
- "Find cost reduction opportunities"
- "Optimize my tax deductions"
- "Interpret my financial reports"

## Workflow

1. User provides context and goals.
2. Skill applies built-in templates and frameworks.
3. Skill generates structured output with recommendations.
4. User receives actionable insights and next steps.

## Inputs
- User context (financial situation, goals, constraints)
- Optional data inputs (amounts, categories, timeframes)
- Analysis preferences

## Outputs
- Structured analysis report
- Templates and frameworks
- Actionable recommendations
- Next steps checklist


## Usage Scenarios

1. **User input:** "Give my finances a full health check. 32, single, $75K income, $15K debt, $25K savings."
→ **Expected output:** Financial health scorecard — emergency fund (4 months, target 6), debt-to-income (20%, moderate), savings rate (12%, needs improvement), net worth trend, insurance gaps — with prioritized improvement plan and 90-day action items.
2. **User input:** "I feel financially anxious but don't know if it's justified. Assess my situation."
→ **Expected output:** Dual assessment — objective financial metrics (DTI, savings rate, net worth trajectory) + subjective financial wellness survey results — with gap analysis between actual risk and perceived stress, plus calming action plan.
3. **User input:** "Annual financial physical for our household before making major decisions."
→ **Expected output:** Comprehensive household financial report — balance sheet, cash-flow statement, goal-funding progress, risk exposure (insurance, concentration, job-loss scenario), tax efficiency score, and 12-month decision calendar with trigger events.



### Scenario 2: 月光族财务体检
**User input:** "我月薪15000，但每个月月底看银行卡余额都是0，不知道钱花哪了。帮我做个体检看哪里出了问题？"
**Expected output:** 个人财务健康快速检测——第一步：把过去3个月微信/支付宝/银行卡流水导出来分类（餐饮/交通/购物/娱乐/社交/住房/水电/其他）；第二步：算核心指标（储蓄率=月存款/月收入，理想≥20%；负债率=月供/月收入，理想≤40%；应急储备=现金/月支出，理想≥6倍）；第三步：找出最大3个黑洞（大多数人会发现外卖+奶茶+打车占到了总支出30%以上）；第四步：制定止血方案（先把储蓄转进不可随意取的账户如余利宝/理财通，设置自动工资日转账）。关键工具：随手记App或Excel模板。

## Safety
- No real financial transactions or API calls
- No access to real bank accounts or financial systems
- Recommendations are informational only
- Users should consult financial professionals for actual decisions

## Acceptance Criteria
- Must return structured markdown/JSON output
- Must include actionable recommendations
- Must clearly state the descriptive/non-executable nature
- Must provide templates or frameworks for user adaptation
