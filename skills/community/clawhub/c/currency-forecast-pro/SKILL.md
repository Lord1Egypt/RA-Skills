---
name: currency-forecast-pro
description: Professional currency exchange rate analysis and forecasting for any currency pair. Provides technical analysis, trend prediction, and market insights using real-time data.
metadata:
  openclaw:
    emoji: "💹"
    requires:
      env: []
---

# Currency Forecast Pro

A professional-grade currency analysis tool that provides comprehensive exchange rate forecasting for any currency pair.

## Features

- **Universal Currency Support**: Works with any currency pair (USD/EUR, GBP/JPY, AUD/CNY, etc.)
- **Technical Analysis**: Moving averages (7/14/30-day), trend lines, support/resistance levels
- **Predictive Modeling**: Short-term (7-day) and medium-term (30-day) forecasts
- **Market Context**: Real-time market research and economic factors
- **Risk Assessment**: Volatility analysis and confidence intervals

## Usage

### Basic Forecast

```
Forecast USD/EUR exchange rate
```

### Specific Timeframe

```
Analyze GBP/JPY with 60 days of historical data
```

### Compare Multiple Pairs

```
Compare USD/CNY and EUR/USD forecasts
```

## Supported Currencies

All major currencies supported by Frankfurter API:
- **Major**: USD, EUR, GBP, JPY, CHF, CAD, AUD, NZD
- **Asian**: CNY, HKD, SGD, KRW, INR, THB, MYR, IDR
- **European**: SEK, NOK, DKK, PLN, CZK, HUF, RON
- **Others**: MXN, BRL, ZAR, TRY, RUB, AED, SAR

## Output Format

```
💹 Currency Forecast: USD/EUR

📊 Technical Analysis
Current: 0.9234
MA7: 0.9210 | MA14: 0.9185 | MA30: 0.9150
Trend: Upward 📈 (slope: +0.00012)
Support: 0.9100 | Resistance: 0.9350
Volatility: 0.45% daily

📰 Market Context
• Fed Policy: Hawkish stance
• ECB: Dovish outlook
• US Data: Strong employment

🔮 Forecasts
7-day: 0.9250 ~ 0.9300 (+0.2% ~ +0.7%)
30-day: 0.9300 ~ 0.9450 (+0.7% ~ +2.3%)
Confidence: High

⚠️ Risk Factors
- Upcoming Fed meeting
- EU inflation data
- Geopolitical tensions
```

## Data Sources

- **Frankfurter API**: ECB reference rates, historical data
- **Web Search**: Current market conditions and news
- **Technical Indicators**: Calculated locally using statistical methods

## Technical Details

### Indicators Calculated

1. **Moving Averages**: Simple MA for 7, 14, and 30-day periods
2. **Trend Analysis**: Linear regression slope over 30 days
3. **Support/Resistance**: Min/Max of recent 20-day range
4. **Volatility**: Average absolute daily change percentage
5. **Forecast**: Linear projection with volatility bands

### Forecast Methodology

- Short-term (7-day): Linear trend projection
- Medium-term (30-day): Trend + seasonal adjustment
- Confidence levels based on recent volatility

## Installation

No additional dependencies required. Uses:
- `exec` for API calls
- `web_search` for market research

## Examples

### Example 1: Major Pair
```
User: Forecast EUR/USD
Agent: [Comprehensive analysis with 75-day data]
```

### Example 2: Asian Currencies
```
User: Analyze USD/CNY and USD/JPY
Agent: [Comparative analysis of both pairs]
```

### Example 3: Commodity Currencies
```
User: What's the outlook for AUD and CAD against USD?
Agent: [Analysis considering commodity price factors]
```

## Version History

- **1.0.0**: Initial release with full technical analysis

## License

MIT-0 - Free to use, modify, and redistribute

## Author

Created by clawclaw for OpenClaw
