---
name: currency-forecast
description: Professional currency exchange rate analysis and forecasting tool. Provides technical analysis, market research, and predictive insights for currency pairs like AUD/CNY, USD/CNY, etc.
metadata:
  openclaw:
    emoji: "💱"
    requires:
      env: []
---

# Currency Forecast Skill

Professional currency exchange rate analysis and forecasting using technical indicators, market research, and predictive modeling.

## Features

- **Technical Analysis**: Moving averages, trend lines, support/resistance levels
- **Market Research**: Real-time market factors and news analysis
- **Predictive Modeling**: Short, medium, and long-term forecasts
- **Multi-Currency Support**: Works with any currency pair supported by Frankfurter API

## Usage

### Basic Analysis

```
Analyze AUD/CNY exchange rate
```

### With Specific Parameters

```
Forecast USD/EUR with 30-day historical data
```

### Custom Threshold Alert

```
Check if AUD/CNY is below 4.82 and provide analysis
```

## Supported Currency Pairs

Any pair supported by Frankfurter API:
- AUD/CNY, AUD/USD, AUD/EUR
- USD/CNY, USD/EUR, USD/JPY
- EUR/CNY, EUR/USD
- And more...

## Data Sources

- **Frankfurter API**: Historical exchange rate data
- **Web Search**: Current market conditions and news
- **Technical Indicators**: Calculated locally

## Output Format

The skill generates a comprehensive report including:
1. Technical Analysis (MA, trends, volatility)
2. Fundamental Analysis (market factors)
3. Professional Forecasts (short/medium/long-term)
4. Trading Recommendations

## Example Output

```
## 📊 AUD/CNY Technical Analysis

Current Rate: 4.8583
7-day MA: 4.8826 (below)
Trend: Downward slope -0.000175
Support: 4.8376 | Resistance: 4.9100

## Market Factors
- RBA Rate: 4.10% (hawkish)
- PBOC Policy: Loose (3.0%)
- Iron Ore: $95/ton (rebounding)

## Forecast
Short-term: 4.82 ~ 4.92
Medium-term: 4.80 ~ 4.95
Long-term: Target 5.36 by end 2026
```

## Installation

No additional setup required. Uses built-in tools:
- `exec` for API calls
- `web_search` for market research

## Version

1.0.0
