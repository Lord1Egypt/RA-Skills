---
name: financial-services-asset-management
description: >
  Use when building portfolio reports, performance attribution analyses, IC memos, fund performance decks, or any asset management deliverable. Covers Brinson attribution, risk metrics, and institutional investor reporting.
metadata:
  openclaw:
    emoji: "📈"
---

# Asset Management

构建资管级别的分析材料：组合报告、Brinson 归因分析、IC memo、业绩 Deck、风险指标。

**Announce at start:** "I'm using the asset-management skill to structure this portfolio analysis."

## Core Principle

资管报告的核心是回答：业绩从哪来（归因）、风险在哪（风控）、下一步怎么做（展望）。每个绩效数字必须与基准和持仓数据交叉验证。

**REQUIRED:** Use financial-services:source-attribution before finalizing any deliverable.
**REQUIRED:** Use financial-services:excel-powerpoint-output for all output formatting.

## Checklist

You MUST create a task for each applicable item and complete them in order:

1. **Parse the request** — Identify deliverable type (attribution / IC memo / performance deck / risk report)
2. **Gather source materials** — Holdings data, benchmark returns, market data
3. **Calculate returns** — Time-weighted and money-weighted returns
4. **Run attribution** — Brinson-Fachler or other attribution method
5. **Calculate risk metrics** — Sharpe, beta, max drawdown, tracking error, active share
6. **Source attribution** — Verify every number traces to source
7. **Format output** — Apply standardized Excel/PowerPoint formatting

## Workflow: Portfolio Performance Attribution

**Brinson-Fachler Attribution Model:**

The Brinson-Fachler model decomposes active return into allocation and selection effects:

```
Total Active Return = Allocation Effect + Selection Effect + Interaction Effect

Where:
- Allocation Effect = (wp - wb) × (Rb - Rb_total)
  (overweight sector × sector benchmark return vs total benchmark)

- Selection Effect = wb × (Rp - Rb)
  (sector benchmark weight × portfolio vs benchmark return within sector)

- Interaction Effect = (wp - wb) × (Rp - Rb)
  (combined effect of both weight and return differences)
```

**Standard Attribution Table:**
```
Sector       | Port Wt | Bmk Wt | Active | Port Ret | Bmk Ret | Alloc  | Select | Interact | Total
-------------|---------|--------|--------|----------|---------|--------|--------|----------|------
Technology   | 32.5%   | 28.0%  | +4.5%  | 12.3%    | 10.1%   | +0.45% | +0.70% | +0.10%   | +1.25%
Healthcare   | 18.2%   | 20.0%  | -1.8%  | 8.5%     | 9.2%    | -0.17% | -0.13% | +0.01%   | -0.29%
Financials   | 15.0%   | 16.0%  | -1.0%  | 6.8%     | 7.5%    | -0.08% | -0.11% | +0.01%   | -0.18%
...          | ...     | ...    | ...    | ...      | ...     | ...    | ...    | ...      | ...
TOTAL        | 100.0%  | 100.0% | 0.0%   | X.X%     | X.X%    | +X.X%  | +X.X%  | +X.X%    | +X.X%
```

**Interpretation Guide:**
- Positive allocation: overweight in outperforming sectors (or underweight in underperforming)
- Positive selection: picked better securities within sector
- Interaction: combined effect (usually small, but can be meaningful in concentrated portfolios)

## Workflow: Risk Metrics Calculation

**Core Risk Metrics:**

```
Sharpe Ratio = (Rp - Rf) / σp
  - Rp = portfolio return, Rf = risk-free rate, σp = portfolio standard deviation
  - Interpretation: > 1.0 good, > 2.0 excellent

Sortino Ratio = (Rp - Rf) / σd
  - σd = downside deviation only
  - Better for asymmetric return distributions

Information Ratio = (Rp - Rb) / TE
  - TE = tracking error = σ(Rp - Rb)
  - Interpretation: > 0.5 good, > 1.0 excellent

Beta = Cov(Rp, Rb) / Var(Rb)
  - Sensitivity to benchmark movements
  - β > 1 = more volatile than benchmark

Max Drawdown = max(Peak - Trough) / Peak
  - Worst peak-to-trough decline
  - Report: date of peak, date of trough, recovery time

Active Share = (1/2) × Σ|wp_i - wb_i|
  - Percentage of portfolio that differs from benchmark
  - < 60% = closet indexer, > 80% = truly active

Tracking Error = σ(Rp - Rb) × √12 (if monthly data)
  - Annualized standard deviation of active returns

VaR (95%) = μ - 1.645 × σ
  - Maximum expected loss at 95% confidence over 1 day
  - Report: parametric, historical, and Monte Carlo if available
```

**Standard Risk Summary Table:**
```
Metric              | Portfolio | Benchmark | Peer Median
--------------------|-----------|-----------|------------
Return (1Y)         |   X.X%   |   X.X%    |   X.X%
Volatility (1Y)     |   X.X%   |   X.X%    |   X.X%
Sharpe Ratio        |   X.XX   |   X.XX    |   X.XX
Sortino Ratio       |   X.XX   |   —       |   X.XX
Information Ratio   |   X.XX   |   —       |   X.XX
Max Drawdown        |  (X.X%)  |  (X.X%)   |  (X.X%)
Beta                |   X.XX   |   1.00    |   X.XX
Active Share        |   X.X%   |   —       |   X.X%
Tracking Error      |   X.X%   |   —       |   X.X%
VaR (95%, 1-day)    |  (X.X%)  |  (X.X%)   |  (X.X%)
```

## Workflow: IC Memo (Investment Committee Memo)

**Standard IC Memo Structure:**

1. **Executive Summary**
   - Fund/portfolio name, period, AUM
   - Key performance highlights (1-3 bullet points)
   - Top contributors and detractors

2. **Performance Overview**
   - Period return vs benchmark vs peers
   - Cumulative return chart (trailing 1M, 3M, 6M, 1Y, 3Y, 5Y, ITD)
   - Attribution summary (allocation + selection effect)

3. **Sector Attribution**
   - Brinson-Fachler attribution table (per above)
   - Commentary on top 3 attribution drivers

4. **Position-Level Highlights**
   - Top 5 contributors (name, weight, return, contribution)
   - Top 5 detractors (name, weight, return, contribution)
   - Notable new positions and exits

5. **Risk Analysis**
   - Risk metrics table (per above)
   - Factor exposure decomposition (if available)
   - Concentration analysis (top 10 holdings % of portfolio)

6. **Outlook & Positioning**
   - Current positioning vs benchmark
   - Key tilts and rationale
   - Upcoming catalysts or events
   - Proposed changes (if any)

## Workflow: Performance Deck (PowerPoint)

**Slide Structure:**

1. **Title Slide** — Fund name, period, "Confidential"
2. **Performance Snapshot** — Single slide with headline return, attribution pie, risk metrics
3. **Return Attribution** — Brinson table + commentary
4. **Sector Positioning** — Bar chart: portfolio vs benchmark weights
5. **Top Holdings** — Table with top 10 positions
6. **Contributors & Detractors** — Two-column layout
7. **Risk Dashboard** — Metrics table + drawdown chart
8. **Outlook** — Current positioning rationale

**Formatting Rules:**
- One key message per slide
- Charts preferred over tables where possible
- Consistent color coding: green = positive, red = negative, gray = benchmark
- All data labeled with source and date
- Footnotes for any methodology assumptions

## Attribution Edge Cases

**Multi-Period Attribution:**
- Linking single-period attribution effects across multiple periods requires geometric linking
- Arithmetic attribution does not sum to total active return over multiple periods
- Always state whether attribution is arithmetic or geometric

**Cash Drag:**
- If portfolio holds cash, include cash as a "sector" in attribution
- Cash drag in rising markets = negative allocation effect
- Document cash policy (tactical vs. liquidity requirement)

**Currency Effects:**
- For global portfolios, decompose return into: local return + currency effect
- Use Brinson with currency overlay or separate currency attribution

**Derivatives and Leverage:**
- Options/futures: use delta-adjusted notional for weight calculations
- Leveraged positions: weights can exceed 100%
- Document derivative usage in risk section

## Common Mistakes to Avoid

| Mistake | Correct Approach |
|---------|------------------|
| Arithmetic attribution over multiple periods | Use geometric linking for multi-period |
| Ignoring cash in attribution | Include cash as explicit sector |
| Not benchmarking risk metrics | Always show portfolio vs benchmark vs peers |
| Single-period attribution only | Show trailing 1Y, 3Y, 5Y where available |
| Not disclosing benchmark methodology | State benchmark rebalancing frequency and rules |
| Confusing time-weighted and money-weighted | TWR for manager skill, MWR for investor experience |

## Self-Review Checklist

Before delivery:

- [ ] Returns calculated correctly (TWR vs MWR stated)
- [ ] Attribution sums to total active return
- [ ] Risk metrics include benchmark comparison
- [ ] Top contributors and detractors identified
- [ ] Every number has a source citation
- [ ] Source attribution skill applied
- [ ] Output formatted per excel-powerpoint-output standard
