---
id: 'einstein-research-portfolio-risk'
name: 'Einstein Research — Portfolio Risk Analyzer'
description: 'Performs a comprehensive, portfolio-level risk analysis. Calculates VaR (Value at Risk), max drawdown, correlation matrix, stress tests against historical crises, and identifies concentration risks. Use when asked about portfolio risk, drawdown, hedging, or stress testing.'
version: '1.0.0'
author: 'DaVinci'
last_amended_at: null
trigger_patterns: []
pre_conditions:
  git_repo_required: false
  tools_available: []
expected_output_format: 'natural_language'
---

# Portfolio Risk Analyzer

## Overview

This skill performs a comprehensive, portfolio-level risk analysis. It goes beyond individual position risk to quantify systemic and correlated risks across the entire portfolio.

**Core Features:**
-   **Value at Risk (VaR)**: Calculates 95% and 99% VaR using Parametric, Historical, and Monte Carlo methods.
-   **Max Drawdown Analysis**: Identifies historical and potential future maximum drawdowns.
-   **Correlation Matrix**: Visualizes how positions move in relation to each other, highlighting diversification benefits or weaknesses.
-   **Stress Testing**: Simulates portfolio performance during historical market crises (e.g., 2008 GFC, 2020 COVID crash, 2022 rate hikes).
-   **Concentration Risk**: Identifies over-concentration in specific sectors, factors, or individual positions.
-   **Beta Calculation**: Measures portfolio volatility relative to benchmarks (SPY, QQQ).

---

## When to Use This Skill

**Explicit Triggers:**
-   "Analyze the risk of my portfolio."
-   "What is my portfolio's Value at Risk?"
-   "How would my portfolio perform in another 2008-style crash?"
-   "Am I too concentrated in the tech sector?"
-   "Calculate the max drawdown of my holdings."
-   User asks about "portfolio risk," "drawdown," "VaR," "correlation," "stress test," or "concentration."

**Implicit Triggers:**
-   User is concerned about a market downturn.
-   User is adding a new large position and wants to understand its impact on overall portfolio risk.
-   User is reviewing their overall asset allocation.

---

## Workflow

### Step 1: Ingest Portfolio Data

The analysis requires the current portfolio holdings, typically from a CSV or JSON file.

**Input Format (`portfolio.json`):**
```json
{
  "positions": [
    { "ticker": "AAPL", "quantity": 100, "avg_price": 150.00 },
    { "ticker": "TSLA", "quantity": 50, "avg_price": 200.00 },
    { "ticker": "SPY", "quantity": 200, "avg_price": 400.00 }
  ],
  "cash": 25000
}
```

### Step 2: Execute the Risk Analysis Script

The `portfolio-risk-analyzer` CLI tool runs the full analysis suite.

```bash
portfolio-risk-analyzer run \
  --portfolio path/to/portfolio.json \
  --benchmark SPY
```

The script performs the following calculations:
1.  Fetches historical price data for all positions.
2.  Calculates daily returns for each position and the total portfolio.
3.  **VaR**:
    -   *Parametric*: Assumes normal distribution of returns.
    -   *Historical*: Uses the actual distribution of historical returns.
    -   *Monte Carlo*: Simulates thousands of possible future return paths.
4.  **Max Drawdown**: Finds the largest peak-to-trough decline in the portfolio's history.
5.  **Correlation**: Computes the correlation matrix for all positions.
6.  **Stress Tests**: Re-prices the portfolio based on the returns of historical crisis periods.
7.  **Concentration**: Calculates weights by position, sector, and factor.

### Step 3: Analyze the Output

The script generates a detailed report in both JSON and Markdown formats.

**JSON Output (`risk_report_YYYY-MM-DD.json`):**
-   Contains all the raw data, calculations, and simulation results for programmatic use.

**Markdown Report (`risk_report_YYYY-MM-DD.md`):**
-   **Risk Summary**:
    -   **Portfolio Beta**: e.g., 1.15 vs. SPY
    -   **99% VaR (1-day)**: e.g., "$5,200 (Your portfolio has a 1% chance of losing at least $5,200 on any given day)."
    -   **Historical Max Drawdown**: e.g., "-28.5%"
-   **Concentration Analysis**:
    -   Top 5 Positions by Weight
    -   Sector Allocation Chart
-   **Stress Test Results**:
    -   A table showing simulated P&L for 2008, 2020, and 2022 scenarios.
-   **Correlation Hotspots**:
    -   Lists the most highly correlated pairs of assets in the portfolio.
-   **Actionable Insights**:
    -   e.g., "Your portfolio is heavily concentrated in Technology (65%). Consider adding exposure to other sectors like Healthcare or Consumer Staples to improve diversification."
    -   e.g., "The high correlation between AAPL and MSFT reduces diversification benefits. Consider trimming one or adding an uncorrelated asset."

### Step 4: Present Findings to User

Synthesize the key findings from the Markdown report into a clear, actionable summary. Start with the most critical information (like high concentration or poor stress test results) and provide concrete suggestions for risk mitigation.
