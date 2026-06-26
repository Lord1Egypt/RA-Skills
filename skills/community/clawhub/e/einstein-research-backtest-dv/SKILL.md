---
id: 'einstein-research-backtest'
name: 'einstein-research-backtest'
description: 'Expert guidance for systematic backtesting of trading strategies. Use
  when developing, testing, stress-testing, or validating quantitative trading strategies.
  Covers "beating ideas to death" methodology, parameter robustness testing, slippage
  modeling, bias prevention, and interpreting backtest results. Applicable when user
  asks about backtesting, strategy validation, robustness testing, avoiding overfitting,
  or systematic trading development.'
version: '1.0.0'
author: 'DaVinci'
last_amended_at: null
trigger_patterns: []
pre_conditions:
  git_repo_required: false
  tools_available: []
expected_output_format: 'natural_language'
---

# Systematic Backtesting Methodology

This skill provides expert guidance for the rigorous, systematic backtesting of quantitative trading strategies. It ensures that strategies are robust, statistically sound, and free from common biases before any consideration of live deployment. This is the *methodology* guide; for the programmatic backtesting engine, see the `einstein-research-backtest-engine` skill.

## Core Principle: "Beat the Idea to Death"

A single backtest with good results is meaningless. The goal is not to find one set of parameters that worked in the past, but to prove that a strategy has a persistent edge across a wide range of market conditions and parameter variations.

## When to Use This Skill

- User asks how to backtest a trading idea.
- User presents a backtest result and asks for interpretation or next steps.
- User wants to know if their strategy is robust or overfit.
- User is developing a systematic or quantitative trading strategy.
- Triggers: "backtest", "strategy validation", "robustness testing", "overfitting", "systematic trading".

## The 7 Stages of Systematic Backtesting

### Stage 1: Hypothesis Definition
- **Action**: Clearly define the strategy's logic, the underlying inefficiency it exploits, and the expected behavior.
- **Example**: "Hypothesis: Stocks that gap down on high volume but close in the upper 50% of their daily range tend to mean-revert over the next 1-3 days."
- **Output**: A clear, one-sentence hypothesis.

### Stage 2: Initial Backtest
- **Action**: Run a single backtest using a baseline set of parameters on in-sample data.
- **Goal**: Sanity check. Does the idea show any promise at all?
- **Tool**: `einstein-research-backtest-engine`
- **Output**: Initial performance metrics (Sharpe, Max Drawdown, CAGR).

### Stage 3: Parameter Robustness Testing
- **Action**: Vary the strategy's key parameters across a logical range.
- **Example**: For a moving average crossover, test 20/50, 25/60, 15/45, etc.
- **Goal**: Check for a "plateau" of profitability. A good strategy works across a range of parameters, not just one magic number. A single peak is a major red flag for overfitting.
- **Output**: A heatmap or table showing performance across parameter variations.

### Stage 4: Out-of-Sample (OOS) Testing
- **Action**: Test the best parameter *plateau* from Stage 3 on a separate, unseen dataset (e.g., a different time period).
- **Goal**: Verify that the strategy's edge is not specific to the in-sample data.
- **Rule**: If performance degrades significantly (>30%) on OOS data, the strategy is likely overfit. **Go back to Stage 1.**
- **Output**: Comparison of In-Sample vs. Out-of-Sample performance metrics.

### Stage 5: Monte Carlo Simulation
- **Action**: Resample the trade history thousands of times to simulate different possible sequences of returns.
- **Goal**: Stress-test the strategy's path dependency and assess the probability of hitting a certain drawdown.
- **Example**: "What is the probability of a >30% drawdown over a 5-year period?"
- **Output**: Distribution of potential outcomes, probability of ruin, expected max drawdown.

### Stage 6: Slippage and Commission Modeling
- **Action**: Re-run the backtest with realistic transaction costs (e.g., 0.05% per trade for slippage + commissions).
- **Goal**: Ensure the strategy's edge is not consumed by trading friction. High-frequency strategies are particularly sensitive to this.
- **Rule**: If the strategy is not profitable after costs, it has no real-world edge.
- **Output**: Net performance metrics after costs.

### Stage 7: Walk-Forward Optimization
- **Action**: A more advanced form of OOS testing. Optimize parameters on a rolling window of data, then test on the subsequent window.
- **Example**: Optimize on 2020-2022 data, test on 2023. Then, optimize on 2021-2023 data, test on 2024.
- **Goal**: Simulate how the strategy would have been adapted and traded in real-time. This is the gold standard for avoiding lookahead bias.
- **Output**: A series of OOS performance reports, stitched together to form an equity curve.

## Common Biases to Avoid

- **Lookahead Bias**: Using information that would not have been available at the time of the trade (e.g., using closing prices to make a decision at the open).
- **Survivorship Bias**: Using a dataset that excludes companies that have gone bankrupt or been delisted. Always use a high-quality, survivorship-bias-free dataset.
- **Overfitting (Curve-Fitting)**: Finding a complex set of rules and parameters that perfectly fits historical data but fails on new data. Parameter robustness testing is the primary defense.
- **Data Snooping**: Repeatedly testing different hypotheses on the same dataset until one looks good by random chance.

## Final Assessment

A strategy is considered potentially viable for live trading **only if** it passes all 7 stages:
1. Clear hypothesis.
2. Shows initial promise.
3. Profitable across a plateau of parameters.
4. Performs well on out-of-sample data.
5. Survives Monte Carlo stress tests.
6. Profitable after costs.
7. Generates a positive walk-forward equity curve.

If a strategy fails at any stage, it is considered invalid, and the process should restart from Stage 1 with a new or revised hypothesis.
