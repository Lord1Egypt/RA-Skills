# Options Strategy Advisor

Educational options analysis and simulation tool using Black-Scholes pricing and Greeks calculation.

## Description

Options Strategy Advisor provides comprehensive analysis of options trading strategies without requiring real-time market data subscriptions. It uses the Black-Scholes model for theoretical pricing, calculates Greeks (delta, gamma, theta, vega), simulates P/L across price ranges, and provides risk management guidance. Ideal for learning options strategies, evaluating trade setups, and understanding risk exposure before execution.

## Key Features

- **Black-Scholes pricing** - Theoretical option values and Greeks calculation
- **Strategy simulation** - P/L analysis for 15+ common options strategies
- **Earnings plays** - Pre-earnings volatility strategies with calendar integration
- **Risk metrics** - Max profit, max loss, breakeven points, Greeks exposure
- **Position sizing** - Calculate appropriate contract quantities based on risk tolerance
- **Strategy comparison** - Side-by-side analysis of multiple approaches
- **Educational focus** - Detailed explanations of each strategy

## Supported Strategies

**Income**: Covered Call, Cash-Secured Put, Poor Man's Covered Call  
**Protection**: Protective Put, Collar  
**Directional**: Bull/Bear Call/Put Spreads  
**Volatility**: Long/Short Straddle, Long/Short Strangle, Iron Condor, Iron Butterfly  
**Calendar**: Calendar Spread, Diagonal Spread

## Quick Start

```bash
# Install dependencies
pip install scipy pandas requests

# Analyze a covered call
python3 scripts/options_analyzer.py \
  --ticker AAPL \
  --strategy covered_call \
  --stock-price 175 \
  --strike 180 \
  --dte 30 \
  --iv 0.25

# Simulate bull call spread
python3 scripts/options_analyzer.py \
  --ticker MSFT \
  --strategy bull_call_spread \
  --long-strike 350 \
  --short-strike 360 \
  --dte 45 \
  --iv 0.30

# Earnings straddle analysis
python3 scripts/options_analyzer.py \
  --ticker NVDA \
  --strategy straddle \
  --earnings-mode \
  --dte 7
```

**Output includes:**
- Theoretical option prices
- Greeks (Delta, Gamma, Theta, Vega, Rho)
- P/L across price range
- Max profit/loss and breakeven points
- Position sizing recommendations

## What It Does NOT Do

- Does NOT execute trades or connect to brokers
- Does NOT provide real-time option chain data (uses theoretical pricing)
- Does NOT guarantee accuracy of implied volatility estimates
- Does NOT account for early assignment risk on American options
- Does NOT replace professional options education or risk management

## Requirements

- Python 3.8+
- scipy, pandas, requests
- FMP API key (for stock prices and historical volatility)
- Basic understanding of options mechanics

## License

MIT
