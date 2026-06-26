# Report Templates

Pre-built structures for common report types. Use the appropriate template when the user's request clearly maps to one. Default to the standard output structure in SKILL.md when it doesn't.

## 1. Executive Summary Report

**Use when:** The audience is leadership, time is short, decision needs to be made.
**Length:** 1 page equivalent (~400-600 words)

```
# [Report Title] — Executive Summary

**Period:** [date range]
**Prepared for:** [audience]
**Data source:** [description]

## Bottom Line

[2-3 sentences: the single most important takeaway and what it means for the business]

## Key Numbers

| Metric | Current | Prior Period | Change |
|--------|---------|-------------|--------|
| [metric 1] | [value] | [value] | [+/-X%] |
| [metric 2] | [value] | [value] | [+/-X%] |
| [metric 3] | [value] | [value] | [+/-X%] |

## What's Working
- [1-2 bullets on positive trends]

## What Needs Attention
- [1-2 bullets on concerning trends or risks]

## Recommended Actions
1. [Action with clear owner and timeline]
2. [Action with clear owner and timeline]
3. [Action with clear owner and timeline]

## Data Notes
[One line on data quality, completeness, and any caveats]
```

## 2. Detailed Analysis Report

**Use when:** The user needs full findings with methodology for review or sharing.
**Length:** 2-4 page equivalent

```
# [Report Title] — Detailed Analysis

**Period:** [date range]
**Prepared for:** [audience]
**Data source:** [description]
**Analysis date:** [date]

## Executive Summary
[3-5 bullet points — the findings that matter most]

## Data Quality Notes
[Completeness, cleaning steps, caveats — see data-quality-checks.md]

## Finding 1: [Title]
**What the data shows:** [fact with numbers]
**Why it matters:** [business implication]
**Confidence:** [High/Moderate/Low]
**Detail:** [supporting analysis, breakdowns, context]

## Finding 2: [Title]
[Same structure]

## Finding 3: [Title]
[Same structure]

## Trend Analysis
[Time-series observations with comparison baselines]
- Direction and magnitude
- Acceleration/deceleration
- Seasonal patterns if present

## Watch Items
- [Emerging concern 1 — what to monitor and when to act]
- [Emerging concern 2]

## Recommended Actions
1. **Now:** [Action justified by current data]
2. **Monitor:** [What to track and what threshold triggers action]
3. **Improve:** [Data or process improvement for better future analysis]

## Methodology
- Metrics calculated: [list with formulas]
- Time periods compared: [description]
- Exclusions: [what was excluded and why]
- Assumptions: [any assumptions made]
```

## 3. Comparison Report

**Use when:** The user wants to compare two or more things (periods, segments, products, options).
**Length:** 1-3 pages depending on number of comparisons

```
# [A] vs. [B] — Comparison Analysis

**Period:** [date range]
**Comparison basis:** [what's being compared and why]

## Summary Verdict
[Which option/segment/period performs better overall, and the key reason why]

## Side-by-Side Comparison

| Dimension | [A] | [B] | Delta | Winner |
|-----------|-----|-----|-------|--------|
| [metric 1] | [value] | [value] | [diff] | [A/B/Tie] |
| [metric 2] | [value] | [value] | [diff] | [A/B/Tie] |
| [metric 3] | [value] | [value] | [diff] | [A/B/Tie] |

## Where [A] Outperforms
- [Specific area with numbers and context]

## Where [B] Outperforms
- [Specific area with numbers and context]

## Context and Caveats
- [Factors that explain differences — seasonality, sample size, external events]
- [Evidence quality differences between options]

## Recommendation
[What to do based on the comparison, with confidence level]
```

## 4. Trend Report

**Use when:** The user wants to understand how something is changing over time.
**Length:** 1-2 pages

```
# [Metric/Area] Trend Analysis

**Period:** [full date range analyzed]
**Granularity:** [daily/weekly/monthly]
**Baseline:** [comparison reference point]

## Trend Summary
[2-3 sentences: what's the overall direction, how fast, and is it accelerating or decelerating?]

## Period-by-Period Breakdown

| Period | Value | Change | Growth Rate | Notes |
|--------|-------|--------|-------------|-------|
| [period 1] | [value] | — | — | Baseline |
| [period 2] | [value] | [+/-] | [%] | |
| [period 3] | [value] | [+/-] | [%] | [notable event] |

## Key Observations
1. **[Observation]** — [what the trend shows and confidence level]
2. **[Observation]** — [what the trend shows and confidence level]

## Seasonal/Cyclical Patterns
[If detectable with available data; if not, state minimum data needed to detect]

## Inflection Points
[Periods where the trend changed direction or rate, with possible explanations]

## Projection Context
[If the user asks "where is this going": state assumptions, range, and confidence. Never present as fact.]

## What Would Change This Trend
- Upside scenario: [what would accelerate positive trend]
- Downside scenario: [what would reverse or worsen the trend]
```

## 5. Health Check Report

**Use when:** The user wants a regular KPI review or business health snapshot.
**Length:** 1-2 pages

```
# Business Health Check — [Period]

**Status:** [Green/Yellow/Red overall assessment]

## Scorecard

| Category | Metric | Value | Target | Status |
|----------|--------|-------|--------|--------|
| Revenue | MRR | [value] | [target] | [G/Y/R] |
| Revenue | MoM Growth | [value] | [target] | [G/Y/R] |
| Customers | Total Active | [value] | [target] | [G/Y/R] |
| Customers | Churn Rate | [value] | [target] | [G/Y/R] |
| Efficiency | CAC | [value] | [target] | [G/Y/R] |
| Efficiency | LTV:CAC | [value] | [target] | [G/Y/R] |

## What's Healthy
- [1-3 bullets on metrics at or above target]

## What Needs Attention
- [1-3 bullets on metrics below target or trending negatively]

## Changes Since Last Period
- [What improved]
- [What declined]
- [What's new or noteworthy]

## Recommended Focus Areas
1. [Highest priority action]
2. [Second priority]
3. [Third priority]
```

## Template Selection Guide

| User request contains... | Use template |
|--------------------------|-------------|
| "executive summary", "for leadership", "quick overview" | Executive Summary |
| "full analysis", "detailed report", "deep dive" | Detailed Analysis |
| "compare", "vs.", "which is better", "A or B" | Comparison |
| "trend", "over time", "how is X changing" | Trend |
| "health check", "KPI review", "how are we doing" | Health Check |
| Unclear or mixed | Default structure from SKILL.md |
