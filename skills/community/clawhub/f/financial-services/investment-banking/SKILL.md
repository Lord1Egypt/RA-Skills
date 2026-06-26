---
name: financial-services-investment-banking
description: >
  Use when building pitch books, CIMs, comps tables, DCF models, precedent transaction analyses, or any M&A valuation work. Covers the full investment banking analysis workflow from data gathering to formatted deliverables.
metadata:
  openclaw:
    emoji: "📊"
---

# Investment Banking

构建投行级别的分析材料：pitch book、CIM、可比公司分析、DCF 估值、先例交易。

**Announce at start:** "I'm using the investment-banking skill to structure this analysis."

## Core Principle

每个数字必须可追溯到源文档。估值结论必须交叉验证（可比公司、DCF、先例交易三角验证）。

**REQUIRED:** Use financial-services:source-attribution before finalizing any deliverable.
**REQUIRED:** Use financial-services:excel-powerpoint-output for all output formatting.

## Checklist

You MUST create a task for each applicable item and complete them in order:

1. **Parse the request** — Identify deliverable type (pitch book / CIM / comps / DCF / precedent transactions)
2. **Gather source materials** — Collect CIM, financial statements, peer data, market data
3. **Build the analysis** — Follow the applicable workflow below
4. **Cross-validate** — Triangulate valuation across methods
5. **Source attribution** — Verify every number traces to source
6. **Format output** — Apply standardized Excel/PowerPoint formatting
7. **Self-review** — Run the review checklist before delivery

## Workflow: Pitch Book / Valuation Summary

When building a pitch book or valuation summary slide:

**Step 1: Peer Selection**
- Select 5-10 comparable companies based on: sector, size (revenue/EBITDA range), geography, business model
- Justify each inclusion/exclusion in a brief note

**Step 2: Comps Table**
Build a comps table with these columns:
```
Company | EV | Revenue | EBITDA | EV/Revenue | EV/EBITDA | P/E | EV/EBITDA Growth
```
- Include: median, mean, min, max, target company position
- Source each multiple to the specific filing or data provider

**Step 3: DCF Model**
Build a DCF with:
- Free Cash Flow projections (5-10 year explicit period)
- Terminal value (exit multiple or perpetuity growth method)
- WACC calculation (show components: risk-free rate, equity risk premium, beta, cost of debt, capital structure)
- Sensitivity table: WACC vs terminal growth/exit multiple
- Clearly label: enterprise value, equity value, per-share value

**Step 4: Precedent Transactions**
- Collect 5-10 relevant M&A transactions in the same sector
- Include: date, acquirer, target, deal value, EV/Revenue, EV/EBITDA
- Adjust for market conditions if transactions are from different periods

**Step 5: Valuation Triangle**
Present implied valuation range from all three methods:
```
Method          | Low    | Midpoint | High
----------------|--------|----------|-------
Comps           | $X.Xb  | $X.Xb    | $X.Xb
DCF             | $X.Xb  | $X.Xb    | $X.Xb
Precedent Txns  | $X.Xb  | $X.Xb    | $X.Xb
Implied Range   | $X.Xb  | $X.Xb    | $X.Xb
```

**Step 6: Position in Range**
- Where does the target sit in its 52-week trading range?
- Flag any outlier explanations (one-time events, market dislocations)

## Workflow: CIM (Confidential Information Memorandum)

When building or analyzing a CIM:

**Structure:**
1. Executive Summary
2. Company Overview (history, products, market position)
3. Industry Overview (market size, growth, dynamics, competitive landscape)
4. Financial Analysis (3-5 year historical, projections, key metrics)
5. Investment Thesis (growth drivers, competitive advantages, opportunities)
6. Risk Factors
7. Appendments (detailed financials, organizational chart, material contracts)

**Financial Analysis Section Must Include:**
- Revenue bridge (organic vs. inorganic growth)
- EBITDA bridge (revenue growth, margin expansion/contraction, one-time items)
- Cash flow analysis (FCF conversion, capex trends)
- Key metrics by segment (if applicable)
- Quality of earnings adjustments

## Workflow: Comparable Company Analysis

**Selection Criteria:**
- Same GICS sub-industry (preferred) or adjacent industry
- Revenue within 0.5x-2.0x of target
- Similar geographic exposure
- Similar growth profile

**Standard Multiples:**
- Enterprise Value: EV/Revenue, EV/EBITDA, EV/EBIT
- Equity Value: P/E, P/B, P/FCF
- Growth-adjusted: EV/EBITDA/Growth (PEG equivalent)

**Statistical Treatment:**
- Report median AND mean (outlier-sensitive)
- Exclude outliers with clear justification
- Show where target ranks within the distribution

## Workflow: DCF Model

**WACC Components:**
```
WACC = (E/(D+E)) × Ke + (D/(D+E)) × Kd × (1-T)

Where:
- Ke = Rf + β × ERP + Size premium (if applicable)
- Rf = 10-year government bond yield
- β = Raw beta adjusted for leverage (Hamada formula)
- ERP = Equity risk premium (Damodaran or consensus)
- Kd = Risk-free rate + credit spread
- T = Marginal tax rate
```

**Terminal Value:**
- Exit Multiple Method: Apply peer median EV/EBITDA to terminal year EBITDA
- Perpetuity Growth Method: g = long-term GDP growth + inflation (typically 2-3%)
- Present both; reconcile if materially different

**Sensitivity Table:**
```
              | Terminal Growth / Exit Multiple
WACC          |  Low  | Base |  High
----------------------------------
Low (-1%)     |       |      |
Base          |       |      |
High (+1%)    |       |      |
```

## Workflow: Precedent Transactions

**Data Points to Collect:**
- Announcement date, completion date
- Acquirer, target, deal structure (cash/stock/mixed)
- Enterprise value, equity value
- Multiples: EV/Revenue, EV/EBITDA, P/E
- Premium to unaffected price
- Strategic vs. financial buyer

**Adjustments:**
- Control premium (typically 20-40%)
- Market condition adjustment if comparing across time periods
- Synergy expectations (strategic buyers often pay more)

## Common Mistakes to Avoid

| Mistake | Correct Approach |
|---------|------------------|
| Using trailing multiples without noting period | Specify LTM, NTM, or calendar year |
| Mixing equity and enterprise value | Be explicit: EV for operating metrics, equity for per-share |
| Ignoring non-recurring items | Normalize EBITDA: add back restructuring, impairments, one-time gains/losses |
| DCF with inconsistent FCF definition | FCF = EBITDA - Capex - Change in NWC - Cash Taxes |
| Circular reference in WACC/valuation | Use goal-seek or iterate: lever beta → unlever → relever → WACC |
| Presenting single point estimate | Always show range with sensitivity |

## Self-Review Checklist

Before delivery:

- [ ] Every number has a source citation
- [ ] Valuation triangulated across 2+ methods
- [ ] Comps median and mean both reported
- [ ] DCF sensitivity table included
- [ ] Key assumptions explicitly stated
- [ ] Non-recurring items normalized
- [ ] Source attribution skill applied
- [ ] Output formatted per excel-powerpoint-output standard
