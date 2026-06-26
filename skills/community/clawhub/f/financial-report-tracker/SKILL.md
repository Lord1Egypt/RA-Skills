---
name: financial-report-tracker
description: Automatically track tech company financial reports and generate investment summaries. Supports retrieving earnings calendars, market expectation comparisons, key metric interpretation, and more.
---

# Financial Report Tracker

Automatically track tech company financial reports and generate investment summaries. Suitable for investors tracking portfolio companies' earnings calendars and automatically summarizing earnings highlights and risks.

## Use Cases

When users mention earnings reports, financial reports, EPS, revenue expectations, earnings interpretation, tracking a company's financials, and similar scenarios.

## Prerequisites

Install Python dependencies before first use:
```bash
pip install yfinance requests pandas
```

## Core Capabilities

1. **Earnings Calendar Tracking** — Automatically retrieve target company earnings release dates
2. **Market Expectation Comparison** — EPS/Revenue expectations vs. actual data
3. **Earnings Interpretation** — Key metric changes and management guidance summary

## Command List

| Command | Description | Usage |
|---------|-------------|-------|
| `track` | Track earnings release dates | `python scripts/earnings_tracker.py track <ticker>` |
| `preview` | Earnings preview analysis | `python scripts/earnings_tracker.py preview <ticker>` |
| `review` | Earnings interpretation | `python scripts/earnings_tracker.py review <ticker> --quarter <Q1/Q2/Q3/Q4>` |

## Usage Workflow

### Scenario 1: Track Earnings Date

```
Track Apple's next earnings release date and market expectations
```

```bash
python scripts/earnings_tracker.py track AAPL
```

### Scenario 2: Earnings Preview Analysis

```
Pre-earnings expectation analysis
```

```bash
python scripts/earnings_tracker.py preview AAPL
```

### Scenario 3: Earnings Review

```
Interpret key data from the latest earnings report
```

```bash
python scripts/earnings_tracker.py review AAPL --quarter Q1
```

## Output Format

All commands output a standard Markdown format report:

```markdown
# 📊 Financial Report Tracker Report

**Generated on**: YYYY-MM-DD HH:MM

## Key Findings
1. [Key finding 1]
2. [Key finding 2]
3. [Key finding 3]

## Data Overview
| Metric | Value | Trend | Rating |
|--------|-------|-------|--------|
| Metric A | XXX | ↑ | ⭐⭐⭐⭐ |
| Metric B | YYY | → | ⭐⭐⭐ |

## Detailed Analysis
[Multi-dimensional analysis based on actual data]

## Actionable Recommendations
| Priority | Recommendation | Expected Outcome |
|----------|----------------|------------------|
| 🔴 High | [Specific recommendation] | [Quantified expectation] |
| 🟡 Medium | [Specific recommendation] | [Quantified expectation] |
| 🟢 Low | [Specific recommendation] | [Quantified expectation] |
```

## References

- [yfinance Library](https://pypi.org/project/yfinance/) — Earnings calendar and earnings data
- [Financial Modeling Prep API](https://site.financialmodelingprep.com/developer/docs) — Financial report data

## Notes

- All analysis is based on data retrieved by the script; data is not fabricated
- Missing data fields are marked "Data Unavailable" rather than guessed
- It is recommended to combine with human judgment; AI analysis is for reference only