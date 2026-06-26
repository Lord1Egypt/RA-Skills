# Technical Signals Reference

## Simple Moving Average (SMA)

The SMA smooths price data over a set period. Common periods:
- **SMA(7)**: Short-term trend. Price above SMA7 = short-term bullish
- **SMA(21)**: Medium-term trend. Price above SMA21 = medium-term bullish
- **SMA(50/200)**: Long-term trend indicators (not computed here, use CoinGecko history for longer periods)

**How to read:**
- Price > SMA →Bullish signal
- Price < SMA → Bearish signal
- SMA crossing above another SMA → Golden cross (bullish)
- SMA crossing below another SMA → Death cross (bearish)

## RSI (Relative Strength Index)

RSI measures momentum on a 0-100 scale:
- **RSI > 70**: Overbought — possible pullback expected
- **RSI < 30**: Oversold — possible bounce expected
- **RSI ~ 50**: Neutral/market in balance

RSI is calculated as: 100 - (100 / (1 + RS)) where RS = average gain / average loss over the period.

## Support & Resistance

Simple estimation based on 30-day high/low:
- **Resistance**: The price ceiling — 30-day high. Breaking above is bullish.
- **Support**: The price floor — 30-day low. Falling below is bearish.

## Price Alerts

User-defined thresholds:
- `--upper`: Alert when price rises above this level
- `--lower`: Alert when price falls below this level

## Trading Signals Summary

| Signal | Bullish | Bearish |
|--------|---------|---------|
| Price vs SMA(7) | Price above | Price below |
| Price vs SMA(21) | Price above | Price below |
| RSI | > 70 overbought | < 30 oversold |
| 24h Change | > +5% | < -5% |

**Disclaimer**: These are simple technical indicators for informational purposes only. Not financial advice.
