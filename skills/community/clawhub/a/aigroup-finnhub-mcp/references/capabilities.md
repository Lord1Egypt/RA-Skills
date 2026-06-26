# Finnhub MCP Capabilities

## Tool groups

- `finnhub_stock_market_data`: quote, candles, profile, basic financials, earnings surprises
- `finnhub_news_sentiment`: company news, market news, news sentiment, insider sentiment
- `finnhub_stock_fundamentals`: financials as reported, dividends, splits, revenue breakdown
- `finnhub_stock_estimates`: earnings estimates, revenue estimates, EBITDA estimates, price target, recommendation trends
- `finnhub_stock_ownership`: insider transactions, institutional ownership, institutional portfolio, congress transactions
- `finnhub_sec_filings`: SEC filings, filing sentiment, similarity index
- `finnhub_technical_analysis`: indicators, aggregate signals, pattern recognition, support/resistance
- `finnhub_calendar_data`: IPO, earnings, economic, FDA calendars
- `finnhub_market_events`: market holidays, analyst ratings, merger and acquisition activity
- `finnhub_crypto_data`: exchanges, symbols, quote, candles
- `finnhub_forex_data`: exchanges, symbols, rate, candles
- `finnhub_alternative_data`: ESG, social sentiment, supply chain, patents
- `finnhub_project_create`, `finnhub_project_list`, `finnhub_job_status`: project and export helpers

## Task mapping

- “What changed this week for a stock?”:
  - Start with `finnhub_news_sentiment`, then add `finnhub_market_events` or `finnhub_stock_estimates`.
- “Show me recent filings and what they imply”:
  - Use `finnhub_sec_filings`.
- “Who is buying or selling?”:
  - Use `finnhub_stock_ownership`.
- “Is this move supported by technicals?”:
  - Use `finnhub_technical_analysis`.
- “Check BTC or FX spot and short history”:
  - Use `finnhub_crypto_data` or `finnhub_forex_data`.

## Dependency

- MCP server name: `aigroup-finnhub-mcp`
- Local launch pattern in this workspace: `npx aigroup-finnhub-mcp`
