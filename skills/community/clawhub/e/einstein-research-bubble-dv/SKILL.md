---
id: 'einstein-research-bubble'
name: 'Einstein Research — Market Bubble Risk Detector'
description: 'Evaluates market bubble risk through quantitative, data-driven analysis using a revised Minsky/Kindleberger framework. Prioritizes objective metrics over subjective impressions to prevent confirmation bias and support practical investment decisions.'
version: '1.0.0'
author: 'DaVinci'
last_amended_at: null
trigger_patterns: []
pre_conditions:
  git_repo_required: false
  tools_available: []
expected_output_format: 'natural_language'
---

# Market Bubble Risk Detector

## Overview

This skill evaluates market bubble risk through a quantitative, data-driven analysis based on a revised Minsky/Kindleberger framework. It prioritizes objective metrics over subjective impressions to prevent confirmation bias and support practical investment decisions.

**Core Principles:**
-   **Data over Narrative**: Relies on measurable data, not just "it feels frothy."
-   **Composite Score**: Generates a score from 0-100 to quantify bubble risk.
-   **Multi-Factor Model**: Incorporates sentiment, valuation, leverage, market structure, and new issuance data.
-   **Action-Oriented**: Provides clear thresholds for tactical adjustments (e.g., raising cash, hedging).

---

## When to Use This Skill

**Explicit Triggers:**
-   "Are we in a stock market bubble?"
-   "Analyze the risk of a market crash."
-   "Is the market overvalued?"
-   "Should I be taking profits?"
-   User asks about "bubble risk," "market froth," "irrational exuberance," or "Minsky moment."

**Implicit Triggers:**
-   User expresses anxiety about high valuations or a rapid market run-up.
-   User is considering de-risking their portfolio.

---

## Workflow

### Step 1: Execute the Data Collection and Analysis Script

The `bubble-detector` CLI tool automates the entire process.

```bash
bubble-detector run
```

The script performs the following actions:
1.  **Fetches Data**: Collects data for each of the 7 quantitative indicators.
    -   Put/Call Ratio (CBOE)
    -   VIX Index (CBOE)
    -   Margin Debt (FINRA)
    -   Market Breadth (% Stocks > 200d MA)
    -   IPO Issuance (e.g., from a public data source)
    -   Retail Volume as % of Total
    -   Forward P/E Ratio vs. Historical Average
2.  **Normalizes Indicators**: For each indicator, it calculates a percentile rank over the last 5 years. A rank of 100 means the indicator is at its most "bubbly" level in 5 years.
3.  **Calculates Composite Score**: A weighted average of the normalized indicator scores.
    -   Sentiment (Put/Call, VIX, Retail Volume): 40%
    -   Leverage (Margin Debt): 20%
    -   Market Structure (Breadth): 20%
    -   Valuation & Issuance (P/E, IPOs): 20%
4.  **Generates Report**: Outputs a JSON file and a Markdown summary.

### Step 2: Analyze the Report

**JSON Output (`bubble_report_YYYY-MM-DD.json`):**
-   Contains the raw data, normalized scores for each indicator, and the final composite score.

**Markdown Report (`bubble_report_YYYY-MM-DD.md`):**
-   **Overall Bubble Score**: e.g., "78 / 100 (High Risk)"
-   **Indicator Dashboard**: A table showing the current value and normalized score for each of the 7 indicators.
-   **Key Drivers**: Highlights which indicators are contributing most to the high score.
-   **Historical Context**: Compares the current score to levels seen before previous market corrections.
-   **Recommended Posture**: Translates the score into a tactical recommendation.

## Interpretation & Recommended Actions

The composite score maps to specific risk postures:

-   **0-40 (Low Risk - "Accumulate")**:
    -   *Characteristics*: Fear is high, valuations are reasonable, leverage is low.
    -   *Action*: A good time to be deploying capital and taking on risk.

-   **41-60 (Moderate Risk - "Cautious Accumulation")**:
    -   *Characteristics*: Market is healthy but not cheap. Some signs of optimism are emerging.
    -   *Action*: Continue to invest, but perhaps with a greater focus on quality.

-   **61-80 (High Risk - "Hold & Hedge")**:
    -   *Characteristics*: Greed is prevalent, valuations are stretched, breadth may be narrowing.
    -   *Action*: Hold existing positions, but stop new aggressive buying. Consider adding hedges (e.g., puts) or raising a small amount of cash.

-   **81-100 (Very High Risk - "Distribute & Protect")**:
    -   *Characteristics*: Euphoria, extreme valuations, high leverage, widespread speculation.
    -   *Action*: Systematically take profits from high-beta positions. Raise significant cash (e.g., 20-40%). Actively hedge the remaining portfolio. This is the time to be selling to the optimists.

## Important Considerations

-   **Not a Timing Tool**: This skill indicates *when risk is high*, not the exact top of the market. Bubbly conditions can persist for months.
-   **Context is Key**: Always present the score in the context of the underlying indicators. A high score driven by stretched valuations is different from one driven by extreme sentiment.
-   **No Panicking**: The goal is to make small, rational adjustments to risk exposure, not to sell everything in a panic.
