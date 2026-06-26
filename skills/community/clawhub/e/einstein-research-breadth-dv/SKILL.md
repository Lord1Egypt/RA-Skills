---
id: 'einstein-research-breadth'
name: 'einstein-research-breadth'
description: "Quantifies market breadth health using TraderMonty's public CSV data.
  Generates a 0-100 composite score across 6 components (100 = healthy). No API
  key required. Use when user asks about market breadth, participation rate, advance-decline
  health, whether the rally is broad-based, or general market health assessment."
version: '1.0.0'
author: 'DaVinci'
last_amended_at: null
trigger_patterns: []
pre_conditions:
  git_repo_required: false
  tools_available: []
expected_output_format: 'natural_language'
---

# Market Breadth Analyzer

## Overview

This skill quantifies the health of market breadth using public data from TraderMonty's GitHub repository. It generates a composite score from 0-100 (100 = healthy) across six key components, providing a quick, data-driven assessment of market participation.

**Key Features:**
- **Composite Score (0-100)**: Single, easy-to-understand metric for breadth health.
- **6-Component Analysis**:
  1. % Stocks > 50-day MA
  2. % Stocks > 200-day MA
  3. 1-Month New Highs - New Lows
  4. Advance-Decline Line (ADL) Momentum
  5. % Bullish (AAII Sentiment)
  6. S&P 500 distance from 200-day MA
- **No API Key Required**: Uses a publicly available CSV, making it free and reliable.
- **Historical Context**: Compares the current score to its 3-month and 6-month moving averages.

---

## When to Use This Skill

**Explicit Triggers:**
- "What's the current market breadth?"
- "Is this rally broad-based?"
- "Analyze market participation."
- "Show me the advance-decline health."
- User asks about "market breadth," "A-D line," "% stocks above moving average."

**Implicit Triggers:**
- User is concerned about a narrow, top-heavy market rally (e.g., led by only a few mega-cap stocks).
- User is assessing the risk of a market downturn, as poor breadth is often a leading indicator.

**When NOT to Use:**
- For real-time, intraday breadth data (this is end-of-day).
- For individual stock analysis.
- For deep technical analysis of a single indicator (this skill provides a composite view).

---

## Workflow

### Step 1: Execute the Analysis Script

The entire process is handled by a single Python script.

```bash
# Run the breadth analysis
python3 skills/market-breadth/scripts/breadth_analyzer.py
```

The script performs the following actions:
1.  **Downloads Data**: Fetches the latest `Market-Breadth-Data.csv` from TraderMonty's public GitHub repo.
2.  **Calculates Components**: For each of the 6 components, it calculates a normalized score (0-100) based on its current value relative to its 1-year range.
3.  **Computes Composite Score**: A weighted average of the 6 component scores.
    -   `% > 50d MA`: 25%
    -   `% > 200d MA`: 25%
    -   `NH-NL`: 20%
    -   `ADL Momentum`: 15%
    -   `AAII Bullish`: 10% (inverse scoring)
    -   `SPX distance from 200d MA`: 5%
4.  **Generates Report**: Outputs a JSON file and a human-readable Markdown summary.

### Step 2: Analyze the Output

The script produces two files:
-   `breadth_report_YYYY-MM-DD.json`
-   `breadth_report_YYYY-MM-DD.md`

**JSON Output:**
```json
{
  "composite_score": 78.5,
  "assessment": "Healthy",
  "trend": "Improving",
  "components": {
    "stocks_above_50d_ma": 85,
    "stocks_above_200d_ma": 90,
    "new_highs_lows": 75,
    "ad_line_momentum": 60,
    "aaii_bullish_inverse": 70,
    "spx_distance_from_200d_ma": 95
  },
  "moving_averages": {
    "3_month": 65.2,
    "6_month": 58.9
  }
}
```

**Markdown Report:**
-   **Overall Score**: 78.5 / 100 (Healthy)
-   **Trend**: Improving (Current > 3-Month MA)
-   **Component Breakdown**: A table showing the score for each of the 6 components.
-   **Key Takeaway**: A short, human-readable summary of the current breadth situation.

### Step 3: Present Findings to User

Synthesize the Markdown report into a concise, clear answer.

**Example Response:**
"Current market breadth is **healthy**, with a composite score of **78.5 out of 100**. This is above the 3-month average of 65.2, indicating an **improving trend**.

-   **Strengths**: A high percentage of stocks are trading above their 50-day (85/100) and 200-day (90/100) moving averages.
-   **Weakness**: Advance-Decline Line momentum is only moderate (60/100).

Overall, this suggests the current market rally is broad-based and well-supported."

## Interpretation Guide

-   **> 70 (Healthy)**: Strong participation. Rally is likely sustainable.
-   **50-70 (Moderate)**: Decent participation, but some signs of narrowing.
-   **30-50 (Weak)**: Narrow, selective market. High risk of reversal.
-   **< 30 (Very Weak)**: Extremely poor participation. Market is vulnerable.

A **divergence** (e.g., S&P 500 making new highs while the breadth score is falling) is a significant warning sign.
