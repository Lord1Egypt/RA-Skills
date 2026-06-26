# Portfolio Risk Manager

Comprehensive portfolio-level risk analysis including VaR, stress testing, correlation analysis, and circuit breakers.

## Description

Portfolio Risk Manager provides institutional-grade risk analytics for individual investors. It calculates Value at Risk using three methods (parametric, historical, Monte Carlo), runs stress tests against historical crises (2008 GFC, 2020 COVID, 2022 rate hikes), analyzes correlation and diversification quality, monitors maximum drawdown with automated circuit breakers, and performs risk budgeting across positions. No paid APIs required—all data from Yahoo Finance.

## Key Features

- **Value at Risk (VaR)** - Parametric, historical, and Monte Carlo methods at 95%/99% confidence
- **Conditional VaR (CVaR)** - Expected shortfall / tail risk measurement
- **Historical stress tests** - Portfolio behavior during 2008 GFC, 2020 COVID, 2022 rate hikes
- **Correlation matrix** - Identify concentration and diversification quality
- **Maximum drawdown** - Peak-to-trough loss tracking with circuit breaker alerts
- **Risk budgeting** - Allocate risk across positions, identify concentration
- **Portfolio beta** - Market sensitivity vs SPY/QQQ
- **Sector/factor exposure** - Concentration risk by sector or style factor

## Quick Start

```bash
# Install dependencies
pip install yfinance numpy pandas scipy

# Create positions.csv:
# ticker,shares,cost_basis
# AAPL,100,145.00
# MSFT,50,310.00
# NVDA,30,420.00

# Run risk analysis
python3 scripts/portfolio_risk.py \
  --positions positions.csv \
  --lookback 252 \
  --benchmark SPY \
  --output risk_report.md
```

**Output includes:**
```
Portfolio Risk Report

Value at Risk (95% confidence, 1-day):
- Parametric: -$3,450 (-2.1%)
- Historical: -$3,890 (-2.4%)
- Monte Carlo: -$3,720 (-2.3%)

Conditional VaR (99%): -$6,200 (-3.8%)
Maximum Drawdown (1Y): -18.5%

Historical Stress Tests:
- 2008 GFC: -42.3%
- 2020 COVID: -28.7%
- 2022 Rate Hikes: -15.2%

Diversification Score: 72/100 (Moderate)
Portfolio Beta vs SPY: 1.15
```

## What It Does NOT Do

- Does NOT provide trade recommendations or signals
- Does NOT predict future portfolio performance
- Does NOT replace comprehensive financial planning
- Does NOT account for leverage or derivatives (equity-only)
- Does NOT include transaction costs or taxes

## Requirements

- Python 3.9+
- yfinance, numpy, pandas, scipy
- No API keys required (Yahoo Finance is free)
- Positions file in CSV format

## License

MIT
