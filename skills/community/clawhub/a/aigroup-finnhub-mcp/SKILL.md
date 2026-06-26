---
name: aigroup-finnhub-mcp
description: Use Finnhub-backed market intelligence through the `aigroup-finnhub-mcp` server for stock, crypto, forex, calendar, news, sentiment, filing, ownership, analyst, and technical-analysis tasks. Trigger when the user needs market-moving news, sentiment, SEC filings, recommendation trends, insider or institutional activity, crypto or FX quotes, or a ticker-level event-driven research pass.
homepage: https://github.com/jackdark425/aigroup-finnhub-mcp
---

# Finnhub MCP

Route event-driven, news-led, filing, sentiment, crypto, and FX work to `aigroup-finnhub-mcp`.

## Route

1. Identify the asset class first:
   - equities and company events
   - crypto
   - forex
   - market calendars or holidays
2. Choose the narrowest Finnhub capability that fits:
   - `finnhub_stock_market_data` for quote, profile, candles, or earnings surprise context
   - `finnhub_news_sentiment` for news, article sentiment, or insider sentiment
   - `finnhub_sec_filings` for filings and filing sentiment
   - `finnhub_stock_estimates` or `finnhub_market_events` for analyst and event context
   - `finnhub_stock_ownership` for insider, congress, and institutional data
   - `finnhub_technical_analysis` for aggregate signals or indicators
   - `finnhub_crypto_data` and `finnhub_forex_data` for non-equity assets
3. Use date ranges deliberately. Finnhub has many time-bounded endpoints, so specify `from` and `to` when freshness matters.
4. Summarize signal quality, not just raw output. Call out whether a finding is based on news flow, filings, analyst revisions, or technicals.

## Common Jobs

- Build a recent-news and sentiment brief for a ticker.
- Check SEC filings, filing sentiment, or filing similarity.
- Review insider activity, institutional ownership, or congress trading.
- Pull crypto or forex quotes and short candle history.
- Compare technical aggregate signals with the latest fundamental or news backdrop.
- Fetch earnings, economic, IPO, or FDA calendar context.

## References

- Read [capabilities.md](./references/capabilities.md) for the exposed Finnhub tool groups and suggested routing.
