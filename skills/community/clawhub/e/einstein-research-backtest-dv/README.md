# Backtest Expert

Professional methodology for systematically validating trading strategies with a focus on robustness over optimistic results.

## Description

Backtest Expert provides comprehensive guidance for testing trading strategies using the "beat it to death" philosophy employed by professional quantitative traders. Rather than seeking the best-looking backtest results, this approach prioritizes finding strategies that survive stress testing, parameter variations, and pessimistic assumptions.

## Key Features

- **Systematic methodology** - Step-by-step framework from hypothesis to validation
- **Stress testing protocols** - Parameter sensitivity analysis, slippage modeling, execution friction
- **Robustness evaluation** - Walk-forward analysis, regime testing, out-of-sample validation
- **Bias prevention** - Guidance on avoiding look-ahead bias, survivorship bias, and curve-fitting
- **Quality metrics** - Evaluation criteria beyond just returns (Sharpe, drawdown, win rate, consistency)
- **Reality checks** - Pessimistic assumptions to filter out strategies that won't survive live trading

## Quick Start

```python
# Example: Validating a mean reversion strategy
# 1. State your hypothesis clearly
hypothesis = "Stocks that gap up >3% on earnings and pull back to previous close provide mean-reversion opportunity"

# 2. Define rules with zero discretion
entry_rules = {
    "gap_threshold": 0.03,
    "pullback_target": "previous_close",
    "time_window": "first_hour",
}

# 3. Run initial backtest (5+ years, multiple regimes)
# 4. Stress test parameters (vary by ±50%)
# 5. Apply execution friction (2x typical slippage)
# 6. Walk-forward validation
# 7. Evaluate robustness score
```

Consult the full SKILL.md for detailed testing protocols and evaluation criteria.

## What It Does NOT Do

- Does NOT provide ready-made trading strategies or signals
- Does NOT execute trades or connect to brokers
- Does NOT guarantee profitable results (it's a testing framework)
- Does NOT replace understanding of market structure and execution
- Does NOT work with machine learning models without modification

## Requirements

- Python 3.9+ (for optional evaluation scripts)
- No API keys required
- No external data dependencies
- Historical price data (from your own source)

## License

MIT
