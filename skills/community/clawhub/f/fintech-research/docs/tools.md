# MCP Tools Reference

All tools are exposed through the local MCP server (`mcp-server/server.py`) and are consumed by Claude Code via stdio transport. Every tool uses free data sources only.

## Tool Inventory

| Tool | Data Source | Free Basis | HK Support | Rate Limit | Cache |
|------|-------------|------------|------------|------------|-------|
| `run_sql` | yfinance + SQLite | Open source | Yes | N/A | 4h |
| `get_ticker_info` | yfinance | Public data | Yes | Respectful | 24h |
| `get_price_history` | yfinance | Public data | Yes | Respectful | 1h |
| `get_sec_filings` | SEC EDGAR | Free official API | No (US only) | 10 req/s | 24h |
| `get_hkex_disclosures` | HKEX News | Free public access | Yes | 2s delay | 4h |
| `get_macro_data` | FRED | Free official API | N/A | 120 req/min | 24h |
| `get_news_signals` | NewsAPI + RSS | Free tier | Yes | 100/day (NewsAPI) | 30min |
| `fiscal_calendar` | Local JSON | Self-maintained | Yes | N/A | Static |
| `batch_ticker_info` | yfinance | Public data | Yes | Max 10/tick | 24h |
| `get_ah_spread` | yfinance | Public data | Yes | Max 10/tick | 1h |

## Tool Details

### run_sql
Execute arbitrary SQL queries against the local SQLite cache database.
- **Input**: SQL query string
- **Output**: JSON result set
- **Use case**: Complex cross-ticker screening, historical comparisons

### get_ticker_info
Retrieve static ticker information (company profile, sector, market cap, etc.).
- **Input**: Ticker symbol (e.g., `0700.HK`, `AAPL`)
- **Output**: JSON with company metadata
- **HK Support**: Full — all `.HK` suffixes resolve via yfinance

### get_price_history
Retrieve historical OHLCV price data.
- **Input**: Ticker symbol, period (1d to max), interval (1d, 1wk, 1mo)
- **Output**: JSON array of price records
- **HK Support**: Full — HKEX trading days and prices

### get_sec_filings
Query SEC EDGAR for US company filings.
- **Input**: US ticker symbol, filing type (10-K, 10-Q, 8-K), count
- **Output**: JSON array of filing metadata and links
- **HK Support**: No — US securities only

### get_hkex_disclosures
Scrape HKEX News platform for regulatory announcements.
- **Input**: HK stock code (e.g., `0700`), category (announcements, filings), count
- **Output**: JSON array of disclosure titles, dates, and document links
- **HK Support**: Yes — primary HK regulatory data source

### get_macro_data
Fetch macroeconomic time series from FRED.
- **Input**: FRED series ID (e.g., `DGS10` for 10Y Treasury, `DEXCHUS` for USD/CNY)
- **Output**: JSON array of date-value observations
- **HK Support**: N/A — macro data is country-level

### get_news_signals
Aggregate news headlines from NewsAPI and RSS feeds.
- **Input**: Query keywords (ticker or topic), source preference, count
- **Output**: JSON array of headline, source, timestamp, sentiment signal
- **HK Support**: Yes — NewsAPI covers global English-language news

### fiscal_calendar
Look up fiscal year-end dates for major HK-listed companies.
- **Input**: Ticker symbol (e.g., `0700.HK`)
- **Output**: JSON with fiscal year-end month, fiscal quarter mapping
- **HK Support**: Yes — covers 15+ major HK-listed companies

### batch_ticker_info
Efficiently retrieve info for multiple tickers in one call.
- **Input**: Array of ticker symbols (max 10)
- **Output**: JSON object keyed by ticker
- **HK Support**: Yes — mixed US + HK batches supported

### get_ah_spread
Calculate A-share vs H-share premium/discount spread for dual-listed companies.
- **Input**: H-ticker (e.g., `0700.HK`) or A-ticker
- **Output**: JSON with AH prices, premium/discount %, last update
- **HK Support**: Yes — core HK feature for connect-flow analysis
