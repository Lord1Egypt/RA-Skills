---
name: crypto-market-news
description: Fetch real-time crypto and market news from major sources (CoinDesk, CoinTelegraph, Decrypt, Blockworks). Use when the user asks for market news, latest crypto news, news about a specific token (BTC, ETH, ZEC, etc.), or wants a market overview before trading decisions. Triggers on phrases like "市場消息", "最新消息", "新聞", "market news", "what's happening in crypto", "news about [token]", "any news on [coin]".
---

# Crypto Market News

Fetch live crypto news from public RSS feeds — no API key required.

## Script

`scripts/fetch_news.sh [keyword] [hours]`

- `keyword` — filter by token or topic (e.g. `bitcoin`, `ZEC`, `ETF`, `regulation`). Leave empty for all news.
- `hours` — lookback window, default `24`

```bash
# All news, last 24h
bash skills/crypto-market-news/scripts/fetch_news.sh

# ZEC-specific news, last 48h
bash skills/crypto-market-news/scripts/fetch_news.sh "zcash" 48

# Regulation news
bash skills/crypto-market-news/scripts/fetch_news.sh "regulation" 24
```

## Sources

- CoinDesk (feedburner)
- CoinTelegraph
- Decrypt
- CryptoSlate

## Workflow

1. Run the script with relevant keyword (use token name or topic)
2. Summarize top stories in plain language
3. Flag any that directly affect the user's current holdings or trade decisions
4. Add sentiment signal (bullish / neutral / bearish) based on tone of headlines
