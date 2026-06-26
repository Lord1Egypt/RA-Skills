---
name: financial-services-commercial-banking
description: >
  Use when building credit memos, loan underwriting analyses, covenant compliance tests, spread sheets, or cash flow analyses for lending decisions. Covers the full commercial banking credit analysis workflow.
metadata:
  openclaw:
    emoji: "🏦"
---

# Commercial Banking

构建商业银行级别的信用分析材料：credit memo、贷款承销、合约合规测试、财务展期、现金流分析。

**Announce at start:** "I'm using the commercial-banking skill to structure this credit analysis."

## Core Principle

信用分析的核心是还款能力评估。每一项财务数据必须映射到合约条款，每一个风险判断必须有数据支撑。

**REQUIRED:** Use financial-services:source-attribution before finalizing any deliverable.
**REQUIRED:** Use financial-services:excel-powerpoint-output for all output formatting.

## Checklist

You MUST create a task for each applicable item and complete them in order:

1. **Parse the request** — Identify deliverable type (credit memo / covenant test / spread sheet / cash flow)
2. **Gather source materials** — Borrower package, financial statements, covenant terms, industry data
3. **Spread financials** — Map historical financials to standardized format
4. **Run credit ratios** — Calculate key credit metrics
5. **Covenant compliance test** — Test against covenant terms
6. **Risk assessment** — Identify and quantify risks
7. **Source attribution** — Verify every number traces to source
8. **Format output** — Apply standardized Excel formatting

## Workflow: Financial Spreading

When spreading financials from a borrower package:

**Standard Layout (Excel):**
```
Row | Category           | FY2023 | FY2024 | FY2025 | FY2026E | YoY Chg
----|--------------------|--------|--------|--------|---------|--------
    | INCOME STATEMENT   |        |        |        |         |
    | Revenue            |        |        |        |         |  X%
    | COGS               |        |        |        |         |  X%
    | Gross Profit       |        |        |        |         |  X%
    | Gross Margin       |        |        |        |         |  X bps
    | SG&A               |        |        |        |         |  X%
    | EBITDA             |        |        |        |         |  X%
    | EBITDA Margin      |        |        |        |         |  X bps
    | D&A                |        |        |        |         |  X%
    | EBIT               |        |        |        |         |  X%
    | Interest Expense   |        |        |        |         |  X%
    | Pre-tax Income     |        |        |        |         |  X%
    | Taxes              |        |        |        |         |  X%
    | Net Income         |        |        |        |         |  X%
    |                    |        |        |        |         |
    | BALANCE SHEET      |        |        |        |         |
    | Cash               |        |        |        |         |  X%
    | Accounts Receivable|        |        |        |         |  X%
    | Inventory          |        |        |        |         |  X%
    | Total Current Assets|       |        |        |         |  X%
    | PP&E (net)         |        |        |        |         |  X%
    | Total Assets       |        |        |        |         |  X%
    |                    |        |        |        |         |
    | Current Liabilities|        |        |        |         |  X%
    | Long-term Debt     |        |        |        |         |  X%
    | Total Liabilities  |        |        |        |         |  X%
    | Shareholders' Equity|       |        |        |         |  X%
    | Total L&E          |        |        |        |         |  X%
    |                    |        |        |        |         |
    | CASH FLOW          |        |        |        |         |
    | Operating CF       |        |        |        |         |  X%
    | Capex              |        |        |        |         |  X%
    | Free Cash Flow     |        |        |        |         |  X%
    | Debt Repayment     |        |        |        |         |  X%
    | Dividends          |        |        |        |         |  X%
    | Net Change in Cash |        |        |        |         |  X%
```

**Rules:**
- Use consistent units (millions with 1 decimal, or thousands)
- All percentages calculated YoY
- Margin changes in basis points (bps)
- Negative values in parentheses: (123)
- Highlight any covenant breach or near-miss in red/yellow

## Workflow: Credit Ratio Analysis

**Leverage Ratios:**
```
Total Debt / EBITDA        → Target: < 3.0x (investment grade: < 2.0x)
Net Debt / EBITDA          → Target: < 2.5x
Debt / Total Capital       → Target: < 50%
Debt / Equity              → Target: < 1.0x
```

**Coverage Ratios:**
```
Interest Coverage (EBIT / Interest)     → Target: > 3.0x
Fixed Charge Coverage                    → Target: > 1.5x
Debt Service Coverage (EBITDA / Debt Service) → Target: > 1.25x
```

**Liquidity Ratios:**
```
Current Ratio    → Target: > 1.5x
Quick Ratio      → Target: > 1.0x
Cash / Current Liabilities → Target: > 0.2x
```

**Profitability Ratios:**
```
Gross Margin     → Track trend, compare to industry
EBITDA Margin    → Track trend, compare to industry
ROA              → Target: > 5%
ROE              → Target: > 10%
```

**Efficiency Ratios:**
```
Days Sales Outstanding (DSO)  → Track trend
Days Inventory Outstanding    → Track trend
Days Payable Outstanding      → Track trend
Cash Conversion Cycle         → Track trend
```

## Workflow: Covenant Compliance Testing

**Standard Covenant Test Layout:**
```
Covenant Type          | Covenant Term    | Actual  | Cushion  | Status
-----------------------|------------------|---------|----------|--------
Max Debt / EBITDA      | ≤ 3.50x         | 2.80x   | 0.70x    | PASS
Min Interest Coverage   | ≥ 3.00x         | 4.20x   | 1.20x    | PASS
Max Capex               | ≤ $50M          | $42M    | $8M      | PASS
Min Tangible Net Worth  | ≥ $200M         | $185M   | ($15M)   | BREACH
Max Debt / Total Capital| ≤ 55%           | 58%     | (3%)     | BREACH
```

**Status Definitions:**
- **PASS**: Actual meets or exceeds covenant with positive cushion
- **NEAR-MISS**: Cushion < 10% of covenant value (yellow highlight)
- **BREACH**: Actual violates covenant term (red highlight)
- **WAIVED**: Covenant waived by lender (note waiver date and terms)

**When a breach is found:**
1. Identify the specific covenant and the breach amount
2. Assess if it's a technical breach (calculation timing) or fundamental (deteriorating performance)
3. Check for any cure provisions or grace periods
4. Flag cross-default implications
5. Recommend action: waiver request, amendment, or remediation plan

## Workflow: Credit Memo Structure

**Standard Credit Memo Sections:**

1. **Executive Summary**
   - Borrower name, facility type, amount requested
   - Purpose of credit
   - Recommendation (approve / approve with conditions / decline)
   - Key risk factors and mitigants

2. **Borrower Overview**
   - Business description, history, ownership
   - Management quality assessment
   - Industry position and competitive landscape

3. **Financial Analysis**
   - Historical financial spread (3-5 years)
   - Key ratio trends with commentary
   - Quality of earnings assessment
   - Working capital analysis

4. **Cash Flow Analysis**
   - Sources and uses of cash
   - Debt service capacity
   - Free cash flow after debt service
   - Stress scenarios (base / downside / severe)

5. **Covenant Compliance**
   - Current compliance status
   - Projected compliance (12-24 months)
   - Recommended covenant set for new facility

6. **Risk Assessment**
   - Credit risks (quantified where possible)
   - Mitigants for each risk
   - Industry/macro risks
   - Concentration risks

7. **Recommendation**
   - Approval amount and terms
   - Covenants and conditions
   - Monitoring requirements
   - Early warning indicators

## Stress Testing

Always include at least two stress scenarios:

**Base Case:**
- Management projections or consensus
- No material changes to business model

**Downside Case:**
- Revenue decline 10-15%
- Margin compression 100-200 bps
- Working capital deterioration
- Test: Can borrower still service debt?

**Severe Case:**
- Revenue decline 20-30%
- Margin compression 300-500 bps
- Credit facility draw-up
- Test: What is the loss given default?

## Common Mistakes to Avoid

| Mistake | Correct Approach |
|---------|------------------|
| Using GAAP EBITDA without adjustments | Normalize for non-recurring items, stock comp, operating leases |
| Ignoring off-balance sheet liabilities | Include operating leases, guarantees, pension obligations |
| Not testing projected covenants | Always project 12-24 months forward |
| Single scenario analysis | Minimum: base + downside. Better: + severe |
| Ignoring industry cyclicality | Compare to industry-adjusted norms |
| Mixing fiscal and calendar year | Normalize to same period for comparisons |

## Self-Review Checklist

Before delivery:

- [ ] All financials spread with consistent format
- [ ] Key credit ratios calculated and trended
- [ ] Every covenant tested with status and cushion
- [ ] Near-misses and breaches highlighted
- [ ] Stress scenarios included (base + downside minimum)
- [ ] Every number has a source citation
- [ ] Source attribution skill applied
- [ ] Output formatted per excel-powerpoint-output standard
