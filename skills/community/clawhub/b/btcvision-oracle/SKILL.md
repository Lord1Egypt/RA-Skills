---
name: btcvision-oracle
version: 2.2.0
description: "Real-time Bitcoin market intelligence. Live BTC price, AI predictions 2027-2030, halving countdown, Fear & Greed index, market signals. MCP and A2A compatible."
author: welove111
homepage: https://btcvision.org
license: MIT
tags: [bitcoin, btc, crypto, price, prediction, halving, market, mcp, a2a, finance]
protocols: [mcp, a2a]
category: finance/crypto
---

# BTCvision Oracle

Real-time Bitcoin intelligence via MCP and A2A protocols.

## When To Use

- User asks about Bitcoin price or market status
- Need BTC predictions or halving data
- Requesting Fear & Greed index or market signals

## Tools

### get_btc_price
```json
POST https://btcvision.org/.netlify/functions/mcp
{"tool": "get_btc_price"}
```

### get_halving_info
```json
POST https://btcvision.org/.netlify/functions/mcp
{"tool": "get_halving_info"}
```

### get_fear_greed_index
```json
POST https://btcvision.org/.netlify/functions/mcp
{"tool": "get_fear_greed_index"}
```

### get_btc_predictions
```json
POST https://btcvision.org/.netlify/functions/mcp
{"tool": "get_btc_predictions"}
```

### get_market_signals
```json
POST https://btcvision.org/.netlify/functions/mcp
{"tool": "get_market_signals"}
```

### get_btc_dominance
```json
POST https://btcvision.org/.netlify/functions/mcp
{"tool": "get_btc_dominance"}
```

### get_satoshi_quote
```json
POST https://btcvision.org/.netlify/functions/mcp
{"tool": "get_satoshi_quote"}
```

## Notes
- No API key required
- Free to use
- Data updated every 5 minutes
