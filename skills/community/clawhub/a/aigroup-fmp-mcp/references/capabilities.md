# FMP MCP Capabilities

## Core coverage

- Quotes: `get_quote`
- Symbol discovery: `search_symbol`
- Market movers: `get_market_gainers`, `get_market_losers`, `get_most_active`
- Sectors and universe context: `get_sector_performance`, `get_sp500_constituents`
- Company overview: `get_company_profile`
- Financial statements: `get_income_statement`, `get_balance_sheet`, `get_cash_flow`
- Metrics and ratios: `get_key_metrics`, `get_financial_ratios`
- News and estimates: `get_stock_news`, `get_analyst_estimates`, `get_price_target`, `get_analyst_ratings`
- Ownership and insider activity: `get_insider_trading`, `get_institutional_holders`
- Technicals and charts: `get_technical_indicator_rsi`, `get_technical_indicator_sma`, `get_technical_indicator_ema`, `get_historical_chart`
- Calendars and macro: `get_earnings_calendar`, `get_economic_calendar`, `get_economic_indicator`

## Task mapping

- Unknown ticker or fuzzy company name:
  - Start with `search_symbol`.
- Quick company snapshot:
  - Use `get_quote` and `get_company_profile`.
- Financial health check:
  - Use the three statements plus `get_key_metrics` and `get_financial_ratios`.
- Market breadth recap:
  - Use `get_market_gainers`, `get_market_losers`, `get_most_active`, and `get_sector_performance`.
- Light technical context:
  - Use one or two indicators only.

## Dependency

- MCP server name: `aigroup-fmp-mcp`
