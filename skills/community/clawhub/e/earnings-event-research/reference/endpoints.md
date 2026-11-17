# earnings-event-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**10 endpoints across 2 platform group(s).**

## Yahoo Finance (6)

### `yahoo_finance_calendar_results`

- **HTTP:** `GET /yahoo-finance/calendars/{type}`
- **What:** Yahoo Finance calendar results. Returns Yahoo Finance calendar rows for the path `type`: `earnings`, `ipo`, `economic-events` or `splits`. Narrow with `start` and `end` (YYYY-MM-DD, RFC3339 or Unix seconds) and page with `limit` (max 100) and `offset`. For `earnings` only, `market_cap` sets a minimum and `filter_most_active` (default true) filters. The response echoes the window and paging with the `rows`.
- **Params:** `end` (string, optional) — End date as YYYY-MM-DD, RFC3339, or Unix seconds; `filter_most_active` (boolean, optional) — Earnings-only most-active filter, default true; `limit` (integer, optional) — Result count, max 100; `market_cap` (number, optional) — Earnings-only market cap minimum; `offset` (integer, optional) — Result offset; `start` (string, optional) — Start date as YYYY-MM-DD, RFC3339, or Unix seconds; `type` (string, **required**) — Calendar type: earnings, ipo, economic-events, or splits

### `yahoo_finance_search`

- **HTTP:** `GET /yahoo-finance/search`
- **What:** Yahoo Finance search. Searches Yahoo Finance for the required `q`, a ticker symbol or company name, and returns matching `quotes`, `news` and `lists`, plus `research` reports when `include_research` is set and Yahoo returns them. `quotes_count`, `news_count` and `lists_count` set how many of each; `enable_fuzzy_query` turns on fuzzy matching.
- **Params:** `enable_fuzzy_query` (boolean, optional) — Enable fuzzy matching; `include_research` (boolean, optional) — Include research reports when Yahoo returns them; `lists_count` (integer, optional) — List result count; `news_count` (integer, optional) — News result count; `q` (string, **required**) — Ticker symbol or company name; `quotes_count` (integer, optional) — Quote result count

### `yahoo_finance_ticker_calendar`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/calendar`
- **What:** Yahoo Finance calendar. Returns the calendar events Yahoo Finance holds for a `symbol` such as `AAPL`, under `modules.calendarEvents`. The response echoes the `symbol`, and the symbol is the only input.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_earnings`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/earnings`
- **What:** Yahoo Finance earnings. Returns the Yahoo Finance earnings modules for a `symbol` such as `AAPL`, including `earnings` and `earningsTrend`, under `modules`. The response echoes the `symbol`, and the symbol is the only input.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_earnings_dates`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/earnings-dates`
- **What:** Yahoo Finance earnings dates. Returns earnings-date rows for a Yahoo Finance `symbol`, taken from Yahoo's earnings calendar table. `limit` (max 100) and `offset` page the rows. Each row is keyed by the table's column names, such as `Earnings Date`. Returns an upstream error when Yahoo does not serve the table.
- **Params:** `limit` (integer, optional) — Result count, max 100; `offset` (integer, optional) — Result offset; `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_history`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/history`
- **What:** Yahoo Finance historical prices. Returns price points for a Yahoo Finance `symbol`: open, high, low, close, adjusted close and volume with timestamps. Use `period` (default `1mo`, up to `max`) or `start` and `end`, which override it. `interval` sets the candle size (default `1d`; intraday covers recent ranges only). `include_actions` adds dividend, split and capital-gain `events`.
- **Params:** `auto_adjust` (boolean, optional) — Adjust OHLC prices with adjusted close; `back_adjust` (boolean, optional) — Back-adjust OHLC prices while keeping close; `end` (string, optional) — Unix seconds, RFC3339, or YYYY-MM-DD; `include_actions` (boolean, optional) — Include dividends, splits, and capital gains; `include_prepost` (boolean, optional) — Include pre/post market data; `interval` (string, optional) — Interval such as 1d, 1h, 5m; `keepna` (boolean, optional) — Keep fully empty chart rows; `period` (string, optional) — Range such as 1d, 1mo, 1y, max; `rounding` (boolean, optional) — Round prices to two decimals; `start` (string, optional) — Unix seconds, RFC3339, or YYYY-MM-DD; `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

## SEC EDGAR (4)

### `sec_company_search`

- **HTTP:** `GET /sec/company/search`
- **What:** Resolve a ticker or company name to EDGAR companies. Resolves a ticker symbol or company-name query to SEC EDGAR companies (CIK, ticker, name).
- **Params:** `limit` (integer, optional) — Max matches, default 10, max 100; `q` (string, **required**) — Ticker symbol or company name

### `sec_company_submissions`

- **HTTP:** `GET /sec/company/submissions`
- **What:** List a company's EDGAR filings. Returns a company's recent SEC filings (form, dates, primary document URL) filtered by form type and date range, plus company profile fields as reported by EDGAR: entity_type, former_names, exchanges, category, fiscal_year_end, state_of_incorporation. Provide cik or ticker.
- **Params:** `cik` (string, optional) — SEC CIK (numeric or zero-padded); `form` (string, optional) — Filter by form type, e.g. 10-K, 10-Q, 8-K; `from` (string, optional) — Earliest filing date (YYYY-MM-DD); `limit` (integer, optional) — Max filings, default 50, max 500; `ticker` (string, optional) — Ticker symbol (alternative to cik); `to` (string, optional) — Latest filing date (YYYY-MM-DD)

### `sec_filing_sections`

- **HTTP:** `GET /sec/filing/sections`
- **What:** Extract 10-K/10-Q/8-K item sections. Extracts item sections (e.g. 1A Risk Factors, 7 MD&A) from a 10-K/10-Q/8-K primary document as clean text. Provide accession plus cik or ticker.
- **Params:** `accession` (string, **required**) — Accession number; `cik` (string, optional) — SEC CIK (numeric or zero-padded); `items` (string, optional) — Comma-separated item numbers to return, e.g. 1A,7; `max_chars` (integer, optional) — Max characters per section, default 20000, max 200000; `ticker` (string, optional) — Ticker symbol (alternative to cik)

### `sec_financials`

- **HTTP:** `GET /sec/financials`
- **What:** Normalized income statement, balance sheet, or cash flow. Returns a company's financial statements across recent periods, resolving EDGAR's inconsistent XBRL tags to a stable schema. Provide cik or ticker.
- **Params:** `cik` (string, optional) — SEC CIK (numeric or zero-padded); `limit` (integer, optional) — Number of periods, default 5, max 20; `period` (string, optional) — Period basis, default annual; `statement` (string, optional) — Statement, default income; `ticker` (string, optional) — Ticker symbol (alternative to cik)
