---
id: 'einstein-research-backtest-engine'
name: 'Einstein Research — Backtest Engine'
description: 'Programmatic backtesting framework for trading strategies. Runs backtests with historical price data (yfinance or CSV), supports momentum/mean-reversion/factor/signal-based strategies, walk-forward optimization, out-of-sample testing, transaction cost modeling, regime-aware splits, and full performance metrics (Sharpe, Sortino, Calmar, max drawdown, CAGR, win rate, profit factor). Distinct from einstein-research-backtest (which provides methodology guidance). Use when a user wants to actually run a backtest, test a specific strategy on historical data, or generate performance metrics.'
version: '1.0.0'
author: 'DaVinci'
last_amended_at: null
trigger_patterns: []
pre_conditions:
  git_repo_required: false
  tools_available: []
expected_output_format: 'natural_language'
---

# Backtest Engine

This skill is the programmatic engine for running quantitative trading strategy backtests. It takes a machine-readable strategy definition (e.g., from the `einstein-research-edge` skill) and executes it against historical data, producing detailed performance metrics.

## When to Use This Skill

-   User wants to run a backtest on a specific strategy.
-   User has a `strategy.yaml` file from the `edge-generator` skill.
-   User wants to generate performance metrics for a trading idea.
-   Triggers: "run a backtest," "test this strategy," "generate performance metrics."

This skill is for *execution*. For guidance on *how* to design a robust backtest, see the `einstein-research-backtest` methodology skill.

## Workflow

### Step 1: Provide Strategy Definition

The backtest engine requires a `strategy.yaml` file that defines the rules of the strategy.

**`strategy.yaml` Format:**
```yaml
version: backtest-engine/v1
name: 52-Week High Momentum
universe: "sp500"
data:
  source: yfinance
  start_date: "2018-01-01"
  end_date: "2023-12-31"
entry_signal:
  - "price > high_52w"
  - "volume > 2 * avg_volume_50d"
exit_signal:
  - "hold_days == 5"
  - "pct_change >= 0.10"
  - "pct_change <= -0.05"
parameters:
  hold_days: 5
  profit_target: 0.10
  stop_loss: -0.05
```

### Step 2: Execute the Backtest

The `backtest-engine` CLI runs the simulation.

```bash
backtest-engine run --strategy-file path/to/strategy.yaml
```

**Optional Flags:**
-   `--costs 0.0005`: Apply a 0.05% transaction cost per trade.
-   `--out-of-sample-split 2022-01-01`: Split data for out-of-sample testing.
-   `--walk-forward`: Enable walk-forward optimization mode.

The script performs the following actions:
1.  **Loads Data**: Fetches historical price data via yfinance or from a local CSV.
2.  **Generates Signals**: Iterates through the historical data day-by-day, applying the `entry_signal` and `exit_signal` logic.
3.  **Simulates Trades**: Creates a trade log based on the generated signals.
4.  **Calculates Equity Curve**: Builds the portfolio's equity curve over time.
5.  **Computes Metrics**: Calculates a full suite of performance metrics.

### Step 3: Analyze the Performance Report

The engine generates a detailed report in JSON and Markdown.

**Key Performance Metrics (KPIs):**
-   **CAGR**: Compound Annual Growth Rate.
-   **Max Drawdown**: The largest peak-to-trough drop.
-   **Sharpe Ratio**: Risk-adjusted return (vs. risk-free rate).
-   **Sortino Ratio**: Risk-adjusted return (vs. downside deviation only).
-   **Calmar Ratio**: Return relative to max drawdown.
-   **Win Rate %**: Percentage of trades that were profitable.
-   **Profit Factor**: Gross profits / gross losses.
-   **Trades per Year**: Frequency of the strategy.

**Report Structure (`backtest_report_YYYY-MM-DD.md`):**
1.  **Strategy Summary**: The input `strategy.yaml` definition.
2.  **Overall Performance**: A table with the key performance metrics.
3.  **Equity Curve**: An ASCII or image chart of the portfolio's growth.
4.  **Drawdown Periods**: Highlights the worst drawdown periods.
5.  **Trade Log**: A sample of the individual trades made.
6.  **Annual Returns**: A bar chart of returns by year.

### Step 4: Present Findings

Synthesize the report for the user, focusing on the most important metrics that answer their original question. Always contextualize the results by referencing the methodology from the `einstein-research-backtest` skill (e.g., "This is an initial backtest. The next step is to test for parameter robustness.").
