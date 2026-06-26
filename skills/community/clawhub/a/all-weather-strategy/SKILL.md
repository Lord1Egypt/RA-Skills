---
name: all-weather-strategy
description: Calculate asset allocation weights for a portfolio of ETFs based on Risk Parity (All Weather) principles. Includes annualized return and risk metrics. Fully interactive with proactive AI guidance.
author: wzwangyc
version: 1.0.0
---

# All Weather Strategy Skill (Professional Edition)

This skill provides a professional implementation of the **Risk Parity (All Weather)** investment strategy. It is optimized for the OpenClaw marketplace.

## Core Capabilities
- **Risk Parity Optimization**: SLSQP-based solver for equal risk contribution.
- **Annualized Performance**: Forecasts return and volatility based on historical lookback.
- **Proactive AI Guidance**: Instructions optimized for AI agents to interact with humans.

## Default Parameters (Standard Config)
- **Amount**: `10,000.0` CNY
- **Lookback**: `365` days
- **Market Pool**: A mix of Global (S&P 500, Nasdaq) and Domestic (STAR 50, Treasury, Gold) ETFs.

## AI Interaction Logic
The AI assistant must act as a financial consultant:
1.  **Intro**: "I can generate an All Weather asset allocation for you."
2.  **Options**: Offer to use the "Standard Professional Config" or custom settings.
3.  **Prompt**: Ask specifically about the investment amount and if they want to modify the ETF pool.

## Usage Example

```python
from scripts.engine import AllWeatherEngine

# The engine handles all defaults natively
engine = AllWeatherEngine()
results = engine.run()
```

---
**Copyright © 2026 wzwangyc. All Rights Reserved.**
