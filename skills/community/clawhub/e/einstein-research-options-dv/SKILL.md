---
id: 'einstein-research-options'
name: 'einstein-research-options'
description: 'Options trading strategy analysis and simulation tool. Provides theoretical
  pricing using Black-Scholes model, Greeks calculation, strategy P/L simulation,
  and risk management guidance. Use when user requests options strategy analysis,
  covered calls, protective puts, spreads, iron condors, earnings plays, or options
  risk management. Includes volatility analysis, position sizing, and earnings-based
  strategy recommendations. Educational focus with practical trade simulation.'
version: '1.0.0'
author: 'DaVinci'
last_amended_at: null
trigger_patterns: []
pre_conditions:
  git_repo_required: false
  tools_available: []
expected_output_format: 'natural_language'
---

# Options Strategy Analyzer

## Overview

This skill provides comprehensive analysis, simulation, and risk management for options trading strategies. It combines theoretical pricing with practical P/L simulation to help users understand the risk/reward profile of various options positions.

**Core Features:**
- **Black-Scholes Pricing**: Theoretical option value calculation
- **Greeks Calculation**: Delta, Gamma, Theta, Vega, Rho
- **Strategy Simulation**: P/L charts for common strategies (covered calls, spreads, etc.)
- **Volatility Analysis**: Implied vs. historical volatility, IV Rank/Percentile
- **Risk Management**: Position sizing, max loss calculation, earnings event awareness
- **Educational Focus**: Provides clear explanations of concepts and trade-offs

---

## When to Use This Skill

**Explicit Triggers:**
- "Analyze a covered call on AAPL"
- "Show me the P/L for a protective put on TSLA"
- "What's a good options strategy for a high-volatility stock?"
- "Calculate the Greeks for this SPY call option"
- "Simulate an iron condor on QQQ for next month"
- "Help me with an options play for the upcoming earnings report"
- "What are the risks of a cash-secured put?"
- User mentions specific options strategies: covered call, protective put, cash-secured put, credit/debit spread, iron condor, straddle, strangle

**Implicit Triggers:**
- User wants to hedge a stock position
- User is looking for income-generating strategies
- User is speculating on a large price move (up or down)
- User asks about managing risk for an options trade

**When NOT to Use:**
- Simple stock analysis (use `us-stock-analysis`)
- Portfolio-level risk management (use `portfolio-risk-analyzer`)
- Macroeconomic analysis (use `macro-regime-detector`)

---

## Workflow

### Step 1: Gather Inputs

The user must provide the following parameters for analysis:

```bash
options-analyzer analyze \
  --ticker AAPL \
  --strategy covered-call \
  --stock-price 175.00 \
  --strike-price 180.00 \
  --expiry-date 2026-04-17 \
  --option-type call \
  --risk-free-rate 0.05 \
  --dividend-yield 0.005 \
  # Optional:
  --volatility 0.35 # (If not provided, script fetches historical volatility)
  --num-shares 100
  --num-contracts 1
```

**Required Parameters:**
- `--ticker`: Underlying stock symbol
- `--strategy`: One of `covered-call`, `protective-put`, `cash-secured-put`, `credit-spread`, `debit-spread`, `iron-condor`, `straddle`, `strangle`
- `--stock-price`: Current price of the underlying stock
- `--strike-price`: Strike price of the option(s)
- `--expiry-date`: Expiration date of the option(s) (YYYY-MM-DD)
- `--option-type`: `call` or `put`
- `--risk-free-rate`: Current risk-free rate (e.g., 10-year Treasury yield)

**Optional Parameters:**
- `--volatility`: Implied volatility (if known, otherwise calculated from historical data)
- `--dividend-yield`: Annual dividend yield of the stock
- `--num-shares`: Number of shares held (for covered calls/puts)
- `--num-contracts`: Number of options contracts

### Step 2: Execute Analysis Script

Run the main analysis script with the gathered parameters:

```bash
python3 skills/options-analyzer/scripts/options_analyzer.py --ticker AAPL ...
```

The script performs the following actions:
1. Fetches historical data via yfinance to calculate historical volatility (if not provided).
2. Uses the Black-Scholes model to calculate the theoretical price of the option(s).
3. Calculates all relevant Greeks (Delta, Gamma, Theta, Vega, Rho).
4. Simulates the P/L of the strategy across a range of potential stock prices at expiration.
5. Identifies key metrics: max profit, max loss, break-even point(s).
6. Generates a P/L chart (ASCII or image) and a summary report.

### Step 3: Analyze Results and Provide Recommendations

The script generates a JSON output and a human-readable Markdown report.

**JSON Output (`options_analysis_YYYY-MM-DD_HHMMSS.json`):**
```json
{
  "strategy": "Covered Call",
  "ticker": "AAPL",
  "theoretical_premium": 2.50,
  "greeks": {
    "delta": 0.45,
    "gamma": 0.05,
    "theta": -0.02,
    "vega": 0.12,
    "rho": 0.01
  },
  "simulation": {
    "max_profit": 750.00,
    "max_loss": -17250.00,
    "break_even": 172.50,
    "pnl_data": [...]
  },
  "recommendations": [
    "This strategy profits if AAPL stays below $182.50 by expiration.",
    "Time decay (theta) is beneficial, generating daily income.",
    "High volatility (vega) increases the premium received but also risk."
  ]
}
```

**Markdown Report (`options_analysis_YYYY-MM-DD_HHMMSS.md`):**
- **Strategy Overview**: Explanation of the covered call strategy.
- **Trade Setup**: Summary of the user's inputs.
- **Theoretical Premium**: Calculated value of the option.
- **The Greeks Explained**: What each Greek means for this specific trade.
- **P/L Simulation**: Max profit, max loss, break-even points.
- **P/L Chart**: Visual representation of profit/loss at expiration.
- **Risk Analysis**: Key risks associated with the strategy.
- **Earnings Alert**: Checks if an earnings report falls within the trade duration.

### Step 4: Present Findings to User

Synthesize the Markdown report into a clear, educational response.
- Start with a high-level summary of the strategy's goal.
- Explain the key metrics (max profit/loss, break-even).
- Use the "Greeks Explained" section to educate the user on the trade's dynamics.
- Highlight any warnings, such as an upcoming earnings report.
- Attach the P/L chart image if generated.

---

## Supported Strategies

- **Covered Call**: Long stock, short call (income, limited upside)
- **Protective Put**: Long stock, long put (hedging, downside protection)
- **Cash-Secured Put**: Short put, cash collateral (income, willing to buy stock)
- **Credit Spread**: Short option, long further OTM option (income, defined risk)
- **Debit Spread**: Long option, short further OTM option (directional bet, defined risk)
- **Iron Condor**: Short call spread + short put spread (range-bound, income)
- **Straddle**: Long call + long put at same strike (speculating on large move)
- **Strangle**: Long OTM call + long OTM put (cheaper straddle, needs larger move)

---

## Important Considerations

- **American vs. European Options**: The Black-Scholes model is for European options (exercised only at expiration). While most US stock options are American, this provides a standard theoretical benchmark. Always mention this limitation.
- **Liquidity**: Remind users to check the bid-ask spread and open interest for the specific option contract. Illiquid options can have high transaction costs.
- **Earnings**: Always check for earnings dates within the option's life. Volatility crush after earnings can significantly impact the value of options. The script should automatically flag this.
- **Not Financial Advice**: Include a disclaimer that all analysis is for educational purposes only and not financial advice.
