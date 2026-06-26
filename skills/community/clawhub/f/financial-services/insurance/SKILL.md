---
name: financial-services-insurance
description: >
  Use when reviewing reserve adequacy, building actuarial analyses, analyzing underwriting results, or preparing insurance regulatory filings. Covers reserve analysis, link ratio triangles, actuarial review, and insurance-specific financial reporting.
metadata:
  openclaw:
    emoji: "🛡️"
---

# Insurance

构建保险级别的分析材料：准备金充足性审查、精算分析、承保结果分析、监管报告。

**Announce at start:** "I'm using the insurance skill to structure this actuarial analysis."

## Core Principle

保险分析的核心是不确定性量化。精算数据必须展示置信区间和敏感性，不能只给点估计。每个假设必须明确标注来源和合理性。

**REQUIRED:** Use financial-services:source-attribution before finalizing any deliverable.
**REQUIRED:** Use financial-services:excel-powerpoint-output for all output formatting.

## Checklist

You MUST create a task for each applicable item and complete them in order:

1. **Parse the request** — Identify deliverable type (reserve review / actuarial analysis / underwriting / regulatory)
2. **Gather source materials** — Actuarial workbook, regulatory filings, loss triangles
3. **Analyze reserve adequacy** — Compare carried vs indicated reserves
4. **Build link ratios** — Development triangles and heatmaps
5. **Flag anomalies** — Accelerated development, tail divergence, elevated initial reporting
6. **Source attribution** — Verify every number traces to source
7. **Format output** — Apply standardized Excel/PowerPoint formatting

## Workflow: Reserve Adequacy Review

**Step 1: Reserve Summary**
```
Line of Business    | Carried Reserves | Indicated Reserves | Redundancy/(Deficiency) | %
--------------------|------------------|--------------------|-----------------------|-----
Workers' Comp       |    $XXX M        |    $XXX M          |    $XX M               | X.X%
General Liability   |    $XXX M        |    $XXX M          |    ($XX M)             | X.X%
Auto Liability      |    $XXX M        |    $XXX M          |    $XX M               | X.X%
Professional Liab   |    $XXX M        |    $XXX M          |    ($XX M)             | X.X%
Property            |    $XX M         |    $XX M           |    $X M                | X.X%
TOTAL               |    $X,XXX M      |    $X,XXX M        |    $XX M               | X.X%
```

**Step 2: Ultimate Loss Analysis**
```
Accident Year | Paid Losses | Case Reserves | IBNR  | Total Incurred | Selected Ultimate | % Developed
--------------|-------------|---------------|-------|----------------|-------------------|-------------
2019          | $XXX M      | $XX M         | $X M  | $XXX M         | $XXX M            | 98%
2020          | $XXX M      | $XX M         | $XX M | $XXX M         | $XXX M            | 95%
2021          | $XXX M      | $XX M         | $XX M | $XXX M         | $XXX M            | 88%
2022          | $XXX M      | $XX M         | $XX M | $XXX M         | $XXX M            | 75%
2023          | $XX M       | $XX M         | $XX M | $XXX M         | $XXX M            | 55%
2024          | $XX M       | $XX M         | $XX M | $XX M          | $XXX M            | 30%
2025          | $X M        | $XX M         | $XX M | $XX M          | $XXX M            | 10%
```

**Key Metrics:**
- Average ultimate trend for accident years 2019-2025
- Year-over-year development patterns
- Paid-to-incurred ratio trends
- Case reserve adequacy (case incurred vs. paid development)

## Workflow: Link Ratio Triangles

**Standard Development Triangle:**
```
              | Development Period
Accident Year |  1    |  2    |  3    |  4    |  5    |  6    |  7    |  Ultimate
--------------|-------|-------|-------|-------|-------|-------|-------|----------
2019          | 1.45  | 1.22  | 1.10  | 1.05  | 1.02  | 1.01  | 1.00  |  $XXX M
2020          | 1.42  | 1.20  | 1.08  | 1.04  | 1.02  | 1.01  |       |  $XXX M
2021          | 1.48  | 1.25  | 1.12  | 1.06  | 1.03  |       |       |  $XXX M
2022          | 1.50  | 1.28  | 1.15  | 1.08  |       |       |       |  $XXX M
2023          | 1.55  | 1.30  | 1.18  |       |       |       |       |  $XXX M
2024          | 1.52  | 1.26  |       |       |       |       |       |  $XXX M
2025          | 1.48  |       |       |       |       |       |       |  $XXX M
```

**Link Ratio Heatmap Rules:**
- Green: Within ±5% of 5-year weighted average for that development period
- Yellow: 5-15% deviation from weighted average
- Red: >15% deviation from weighted average
- Always show the 5-year weighted average row for reference

**Building the Heatmap:**
```
For each cell (accident_year, dev_period):
  deviation = (actual_ratio - weighted_avg_ratio) / weighted_avg_ratio × 100
  color = green if |deviation| ≤ 5%, yellow if ≤ 15%, red otherwise
```

## Workflow: Anomaly Detection

**Flag these patterns when reviewing actuarial data:**

**Accelerated Development:**
- Link ratios significantly above historical pattern
- Potential causes: litigation surge, regulatory change, large claim emergence
- Impact: may indicate reserve deficiency

**Tail Development:**
- Development continuing beyond expected closure period
- Check: is this line developing faster or slower than historical?
- Impact: IBNR may be inadequate if tail is lengthening

**Elevated Initial Reporting:**
- First development period ratio above historical average
- Potential causes: claims frequency increase, underwriting change, reporting lag change
- Impact: may signal adverse development in recent accident years

**Calendar Year Effects:**
- Consistent acceleration or deceleration across accident years in same calendar period
- Potential causes: economic conditions, legal environment, claims handling changes
- Impact: may need calendar year adjustment to development factors

## Workflow: Underwriting Analysis

**Combined Ratio Decomposition:**
```
Combined Ratio = Loss Ratio + Expense Ratio + Dividend Ratio

Where:
- Loss Ratio = Incurred Losses / Earned Premium
- Expense Ratio = Underwriting Expenses / Written Premium
  - Commissions ratio
  - General expenses ratio
- Dividend Ratio = Policyholder Dividends / Earned Premium
```

**Standard Underwriting Summary:**
```
Metric                | Current Year | Prior Year | 3-Yr Avg | Industry
----------------------|--------------|------------|----------|----------
Earned Premium        | $XXX M       | $XXX M     | $XXX M   | —
Incurred Losses       | $XXX M       | $XXX M     | $XXX M   | —
Loss Ratio            | X.X%         | X.X%       | X.X%     | X.X%
Expense Ratio         | X.X%         | X.X%       | X.X%     | X.X%
Combined Ratio        | X.X%         | X.X%       | X.X%     | X.X%
Underwriting Income   | $XX M        | $XX M      | $XX M    | —
Investment Income     | $XX M        | $XX M      | $XX M    | —
Net Income            | $XX M        | $XX M      | $XX M    | —
```

**Key Ratios to Track:**
- Loss development (prior year reserve releases/ strengthening)
- Current accident year loss ratio (excluding development)
- Frequency (claims per exposure unit)
- Severity (average claim size)
- Expense ratio trend
- Reinsurance impact

## Workflow: Regulatory Filing Analysis

**Common Filing Types:**
- Annual Statement (NAIC)
- Risk-Based Capital (RBC)
- ORSA (Own Risk and Solvency Assessment)
- Statutory Financial Statements

**Key Regulatory Metrics:**
```
RBC Ratio = Total Adjusted Capital / Company Action Level RBC
  - > 200% = Well capitalized
  - 150-200% = Adequately capitalized
  - 100-150% = Company action level (triggers filing)
  - < 100% = Regulatory action required

Premium-to-Surplus Ratio = Net Written Premium / Policyholder Surplus
  - Target: < 3.0x

Reserve-to-Surplus Ratio = Total Reserves / Policyholder Surplus
  - Varies by line; monitor trend
```

## Actuarial Assumptions Documentation

Every actuarial analysis must document:

```
Assumption Category     | Assumption Made           | Source/Basis          | Sensitivity
------------------------|---------------------------|-----------------------|------------
Loss Development Factors| 5-year weighted average   | Company experience    | ±5% = ±$XX M
Tail Factor             | 1.05 for long-tail lines  | Industry benchmark    | ±2% = ±$XX M
Claim Inflation         | 3.5% annual               | CPI + litigation trend| ±1% = ±$XX M
Expense Trend           | 2.5% annual               | Company budget        | ±0.5% = ±$X M
Investment Return       | 4.0% on reserves          | Current portfolio yield| ±1% = ±$XX M
```

## Common Mistakes to Avoid

| Mistake | Correct Approach |
|---------|------------------|
| Point estimates without ranges | Always show sensitivity to key assumptions |
| Ignoring calendar year effects | Check for consistent patterns across accident years |
| Not disclosing development method | State: Bornhuetter-Ferguson, chain ladder, or frequency-severity |
| Using industry benchmarks without adjustment | Calibrate to company-specific experience where data permits |
| Not linking reserves to pricing | Reserve adequacy impacts future pricing adequacy |
| Ignoring reinsurance effects | Show gross and net of reinsurance separately |

## Self-Review Checklist

Before delivery:

- [ ] Carried vs indicated reserves compared with redundancy/deficiency
- [ ] Link ratio heatmap shows deviation from 5-year weighted average
- [ ] Anomalies flagged with explanation and impact quantification
- [ ] Actuarial assumptions documented with source and sensitivity
- [ ] Every number has a source citation
- [ ] Source attribution skill applied
- [ ] Output formatted per excel-powerpoint-output standard
