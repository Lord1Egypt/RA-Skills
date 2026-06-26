---
name: crypto-alert-aggregator
description: Aggregates real-time crypto market data and Twitter signals into actionable alerts for traders and researchers. Use when you need to monitor price movements, volume spikes, and social sentiment simultaneously.
---

# Crypto Alert Aggregator

Combines market data feeds with Twitter/social signals to detect trading opportunities and market sentiment shifts.

## Features

- Real-time price and volume monitoring
- Twitter sentiment tracking
- Alert filtering and prioritization
- Multi-asset support

## Usage

```javascript
const aggregator = require('./crypto-alert-aggregator');

// Fetch alerts for specific assets
const alerts = await aggregator.getAlerts({
  assets: ['BTC', 'ETH'],
  minVolumeDelta: 0.2,
  twitterSentimentThreshold: 0.7
});

// Stream live alerts
aggregator.streamAlerts((alert) => {
  console.log(`[${alert.type}] ${alert.asset}: ${alert.message}`);
});
```

## Configuration

Set environment variables:
- `CRYPTO_API_KEY`: Market data API key
- `TWITTER_API_KEY`: Twitter API credentials
- `ALERT_WEBHOOK`: Optional webhook for external notifications

## Output Format

```json
{
  "timestamp": "2026-04-13T02:14:08Z",
  "asset": "BTC",
  "type": "volume_spike|price_move|sentiment_shift",
  "value": 45000,
  "change": 2.5,
  "twitterMentions": 1250,
  "sentiment": 0.82,
  "confidence": 0.85
}
```
