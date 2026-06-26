---
name: crypto-sentiment-monitor
description: >
  Real-time crypto market sentiment analysis. Aggregates Twitter/X, Reddit,
  Google Trends, and exchange data. Detects FOMO/FUD cycles and whale movements.
  Triggers: "crypto", "比特币", "sentiment", "情绪", "FOMO", "FUD".
version: 1.0.0
tags:
  - latest
  - crypto
  - trading
  - sentiment
---

# Crypto Sentiment Monitor

Real-time cryptocurrency market sentiment analysis combining social media, search trends, and exchange data.

## Features

- **Social Sentiment**: Twitter/X, Reddit, Telegram channel analysis
- **Search Trends**: Google Trends, Baidu Index for crypto keywords
- **Exchange Data**: Funding rates, open interest, whale transactions
- **FOMO/FUD Detection**: Fear & Greed index calculation

## Usage

### Twitter Sentiment

```bash
xreach search "$BTC OR #Bitcoin OR $ETH" -n 50 --json | \
  python3 analyze_sentiment.py
```

### Fear & Greed Index

```python
def calculate_fear_greed():
    """Calculate Crypto Fear & Greed Index (0-100)"""
    components = {
        "volatility": get_volatility(),      # 25%
        "market_momentum": get_momentum(),  # 25%
        "social_volume": get_social_vol(),  # 15%
        "dominant": get_btc_dominance(),    # 10%
        "trends": get_google_trends(),      # 10%
        "whale_ratio": get_whale_ratio(),   # 15%
    }
    score = sum(c["weight"] * c["value"] 
                for c in components.values())
    
    if score < 25: return "Extreme Fear 😱"
    elif score < 45: return "Fear 😰"
    elif score < 55: return "Neutral 😐"
    elif score < 75: return "Greed 😊"
    else: return "Extreme Greed 🤑"
```

### Whale Alert Detection

```python
def detect_whale_movements():
    """Detect large wallet transactions"""
    alerts = get_whale_alerts(min_usd=1000000)
    for alert in alerts:
        if alert["amount_usd"] > 10000000:
            print(f"🐋 ${alert['amount_usd']/1e6:.1f}M moved: "
                  f"{alert['from']} → {alert['to']}")
```

## Sources

- Twitter/X: xreach tool
- Reddit: `r/CryptoCurrency` and `r/Bitcoin` hot posts
- Google Trends: `crypto`, `bitcoin`, `ethereum`
- Whale Alert: whale-alert.io (free API)

## Tags

`crypto` `bitcoin` `sentiment` `trading` `fear-greed` `whale-alert` `twitter`
