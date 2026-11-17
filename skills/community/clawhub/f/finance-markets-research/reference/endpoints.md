# finance-markets-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**77 endpoints across 5 platform group(s).**

## Yahoo Finance (39)

### `yahoo_finance_calendar_results`

- **HTTP:** `GET /yahoo-finance/calendars/{type}`
- **What:** Yahoo Finance calendar results. Returns Yahoo Finance calendar rows for the path `type`: `earnings`, `ipo`, `economic-events` or `splits`. Narrow with `start` and `end` (YYYY-MM-DD, RFC3339 or Unix seconds) and page with `limit` (max 100) and `offset`. For `earnings` only, `market_cap` sets a minimum and `filter_most_active` (default true) filters. The response echoes the window and paging with the `rows`.
- **Params:** `end` (string, optional) — End date as YYYY-MM-DD, RFC3339, or Unix seconds; `filter_most_active` (boolean, optional) — Earnings-only most-active filter, default true; `limit` (integer, optional) — Result count, max 100; `market_cap` (number, optional) — Earnings-only market cap minimum; `offset` (integer, optional) — Result offset; `start` (string, optional) — Start date as YYYY-MM-DD, RFC3339, or Unix seconds; `type` (string, **required**) — Calendar type: earnings, ipo, economic-events, or splits

### `yahoo_finance_calendars`

- **HTTP:** `GET /yahoo-finance/calendars`
- **What:** Yahoo Finance calendar types. Lists the Yahoo Finance calendar types available through the API: `earnings`, `ipo`, `economic-events` and `splits`. The list is static. Takes no parameters.
- **Params:** _none_

### `yahoo_finance_download`

- **HTTP:** `POST /yahoo-finance/download`
- **What:** Yahoo Finance batch historical prices. Returns historical prices for up to 25 symbols in one POST. The body requires `symbols`; `period`, `start`, `end`, `interval`, `include_prepost` and `include_actions` are optional. Each result is one symbol, with price points (open, high, low, close, adjusted close, volume) and dividend, split and capital-gain events, or an `error` for that symbol.
- **Params:** `request` (object, **required**) — Batch download request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `yahoo_finance_industries`

- **HTTP:** `GET /yahoo-finance/industries`
- **What:** Yahoo Finance industries. Lists the Yahoo Finance industries, each with a `key` and a `name`. It takes no parameters. Pass a returned `key` to `/yahoo-finance/industries/{key}` for that industry's detail.
- **Params:** _none_

### `yahoo_finance_industry`

- **HTTP:** `GET /yahoo-finance/industries/{key}`
- **What:** Yahoo Finance industry detail. Returns Yahoo Finance detail for one industry `key` such as `semiconductors`: name, overview, its parent sector (`sector_key`, `sector_name`), top companies, top performing companies, top growth companies and research reports. Valid keys come from `/yahoo-finance/industries`.
- **Params:** `key` (string, **required**) — Industry key such as semiconductors

### `yahoo_finance_lookup`

- **HTTP:** `GET /yahoo-finance/lookup`
- **What:** Yahoo Finance lookup. Looks up instruments on Yahoo Finance by ticker symbol or company name, optionally filtered to one type: equity, ETF, mutual fund, index, future, currency or cryptocurrency. Page with `count` and `start`. Returns the matching instruments, each with its symbol, short name, quote type and exchange, and the total.
- **Params:** `count` (integer, optional) — Result count; `query` (string, **required**) — Ticker symbol or company name; `start` (integer, optional) — Result offset; `type` (string, optional) — Instrument type filter

### `yahoo_finance_market_status`

- **HTTP:** `GET /yahoo-finance/market/{market}/status`
- **What:** Yahoo Finance market status. Returns whether a Yahoo Finance market is open or closed, for the path `market` such as `US`. The response has `market` and a `status` object with the market id, name and its current open or closed state.
- **Params:** `market` (string, **required**) — Market such as US

### `yahoo_finance_market_summary`

- **HTTP:** `GET /yahoo-finance/market/{market}/summary`
- **What:** Yahoo Finance market summary. Returns the market summary rows for a Yahoo Finance `market` such as `US`, as a `summary` list of instruments, each with fields such as `symbol` and `shortName`.
- **Params:** `market` (string, **required**) — Market such as US

### `yahoo_finance_screener`

- **HTTP:** `GET /yahoo-finance/screener/{id}`
- **What:** Yahoo Finance predefined screener results. Runs a predefined Yahoo Finance screener by `id`, such as `day_gainers` or `most_actives`. `count` and `offset` page the results; `sort_field` and `sort_asc` change the order. The response has the screener `title`, `description`, `total`, `meta` and the matching `quotes`. Valid ids come from `/yahoo-finance/screeners`.
- **Params:** `count` (integer, optional) — Result count; `id` (string, **required**) — Predefined screener id; `offset` (integer, optional) — Result offset; `sort_asc` (boolean, optional) — Sort ascending; `sort_field` (string, optional) — Sort field for offset/customized runs

### `yahoo_finance_screener_custom`

- **HTTP:** `POST /yahoo-finance/screener`
- **What:** Yahoo Finance custom screener. Runs a custom Yahoo Finance screen from a JSON body. `query` is a tree of `operator` and `operands`: combine conditions with `AND` or `OR`, and compare a field to a value with operators such as `EQ` or `GT`. Screen equities (default), ETFs or mutual funds with `quote_type`, and page and sort with `count`, `offset`, `sort_field` and `sort_asc`. Returns the matching quotes and the total.
- **Params:** `request` (object, **required**) — JSON body for a custom screen. The query field is required; quote_type, count, offset, sort_field, and sort_asc are optional.
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `yahoo_finance_screeners`

- **HTTP:** `GET /yahoo-finance/screeners`
- **What:** Yahoo Finance predefined screeners. Lists the predefined Yahoo Finance screeners that can be run, such as `day_gainers`, `day_losers` and `most_actives`, as a `screeners` list of ids. It takes no parameters. Pass an id to `/yahoo-finance/screener/{id}`.
- **Params:** _none_

### `yahoo_finance_search`

- **HTTP:** `GET /yahoo-finance/search`
- **What:** Yahoo Finance search. Searches Yahoo Finance for the required `q`, a ticker symbol or company name, and returns matching `quotes`, `news` and `lists`, plus `research` reports when `include_research` is set and Yahoo returns them. `quotes_count`, `news_count` and `lists_count` set how many of each; `enable_fuzzy_query` turns on fuzzy matching.
- **Params:** `enable_fuzzy_query` (boolean, optional) — Enable fuzzy matching; `include_research` (boolean, optional) — Include research reports when Yahoo returns them; `lists_count` (integer, optional) — List result count; `news_count` (integer, optional) — News result count; `q` (string, **required**) — Ticker symbol or company name; `quotes_count` (integer, optional) — Quote result count

### `yahoo_finance_sector`

- **HTTP:** `GET /yahoo-finance/sectors/{key}`
- **What:** Yahoo Finance sector detail. Returns Yahoo Finance detail for one sector `key` such as `technology`: name, overview, top companies, top ETFs, top mutual funds, the sector's industries and research reports. Valid keys come from `/yahoo-finance/sectors`.
- **Params:** `key` (string, **required**) — Sector key such as technology

### `yahoo_finance_sectors`

- **HTTP:** `GET /yahoo-finance/sectors`
- **What:** Yahoo Finance sectors. Lists the Yahoo Finance sectors, each with a `key` and a `name`. It takes no parameters. Use a returned `key` with `/yahoo-finance/sectors/{key}` to get that sector's companies, funds and industries.
- **Params:** _none_

### `yahoo_finance_ticker_actions`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/actions`
- **What:** Yahoo Finance corporate actions. Returns the corporate actions for a Yahoo Finance `symbol` such as `AAPL`: `dividends`, `splits` and `capital_gains`. Dividend and capital-gain entries carry a Unix timestamp and an amount; split entries carry a ratio such as `4:1`.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_analysts`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/analysts`
- **What:** Yahoo Finance analyst data. Returns analyst data for a Yahoo Finance `symbol` such as `AAPL`, as `modules` keyed by Yahoo module name: recommendation trend, upgrade and downgrade history, price targets and estimates, where Yahoo provides them.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_calendar`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/calendar`
- **What:** Yahoo Finance calendar. Returns the calendar events Yahoo Finance holds for a `symbol` such as `AAPL`, under `modules.calendarEvents`. The response echoes the `symbol`, and the symbol is the only input.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_capital_gains`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/capital-gains`
- **What:** Yahoo Finance capital gains. Returns capital gain events for a Yahoo Finance `symbol`, mainly ETFs and mutual funds such as `SPY`, each with a Unix timestamp and an amount, when Yahoo provides them. The response object also has `dividends` and `splits` fields.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as SPY

### `yahoo_finance_ticker_dividends`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/dividends`
- **What:** Yahoo Finance dividends. Returns the dividend events for a Yahoo Finance `symbol` such as `AAPL`, each with a Unix timestamp and an amount. The response object also has `splits` and `capital_gains` fields.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_earnings`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/earnings`
- **What:** Yahoo Finance earnings. Returns the Yahoo Finance earnings modules for a `symbol` such as `AAPL`, including `earnings` and `earningsTrend`, under `modules`. The response echoes the `symbol`, and the symbol is the only input.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_earnings_dates`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/earnings-dates`
- **What:** Yahoo Finance earnings dates. Returns earnings-date rows for a Yahoo Finance `symbol`, taken from Yahoo's earnings calendar table. `limit` (max 100) and `offset` page the rows. Each row is keyed by the table's column names, such as `Earnings Date`. Returns an upstream error when Yahoo does not serve the table.
- **Params:** `limit` (integer, optional) — Result count, max 100; `offset` (integer, optional) — Result offset; `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_financials`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/financials`
- **What:** Yahoo Finance financial statements. Returns financial statement data for a Yahoo Finance `symbol`. `statement` picks `income`, `balance-sheet` or `cash-flow` (aliases `income-statement`, `balance` and `cashflow` also work) and `period` picks `annual`, `quarterly` or `trailing`; trailing is supported for income and cash flow only. The response echoes `statement` and `period`, with the data under `modules`.
- **Params:** `period` (string, optional) — annual, quarterly, or trailing; `statement` (string, optional) — Statement type. Allowed values: income (alias income-statement), balance-sheet (alias balance), cash-flow (alias cashflow); `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_funds`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/funds`
- **What:** Yahoo Finance fund data. Returns fund data for an ETF or mutual fund `symbol` such as `SPY`, under `modules`: the fund profile, top holdings, equity holdings, bond holdings and sector weightings.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as SPY

### `yahoo_finance_ticker_history`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/history`
- **What:** Yahoo Finance historical prices. Returns price points for a Yahoo Finance `symbol`: open, high, low, close, adjusted close and volume with timestamps. Use `period` (default `1mo`, up to `max`) or `start` and `end`, which override it. `interval` sets the candle size (default `1d`; intraday covers recent ranges only). `include_actions` adds dividend, split and capital-gain `events`.
- **Params:** `auto_adjust` (boolean, optional) — Adjust OHLC prices with adjusted close; `back_adjust` (boolean, optional) — Back-adjust OHLC prices while keeping close; `end` (string, optional) — Unix seconds, RFC3339, or YYYY-MM-DD; `include_actions` (boolean, optional) — Include dividends, splits, and capital gains; `include_prepost` (boolean, optional) — Include pre/post market data; `interval` (string, optional) — Interval such as 1d, 1h, 5m; `keepna` (boolean, optional) — Keep fully empty chart rows; `period` (string, optional) — Range such as 1d, 1mo, 1y, max; `rounding` (boolean, optional) — Round prices to two decimals; `start` (string, optional) — Unix seconds, RFC3339, or YYYY-MM-DD; `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_history_metadata`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/history-metadata`
- **What:** Yahoo Finance history metadata. Returns the chart metadata Yahoo Finance holds for a `symbol` such as `AAPL`, in `meta`, for example `currency` and `exchangeName`. The symbol is the only input.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_holders`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/holders`
- **What:** Yahoo Finance holders. Returns holder data for a Yahoo Finance `symbol` such as `AAPL`, under `modules`: the major holders breakdown (`majorHoldersBreakdown`), institutional ownership, and the fund and insider holder modules.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_info`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/info`
- **What:** Yahoo Finance ticker info. Returns profile and quote information for a Yahoo Finance `symbol` such as `AAPL`, under `modules`: the profile, quote type (`quoteType`), price, statistics and summary modules. The symbol is the only input.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_isin`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/isin`
- **What:** Yahoo Finance ticker ISIN. Returns the ISIN for a Yahoo Finance `symbol`, for example `US0378331005` for `AAPL`. The lookup is experimental, and the `isin` field is `-` when none can be found.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_news`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/news`
- **What:** Yahoo Finance ticker news. Returns the Yahoo Finance news stream for the ticker in the `symbol` path parameter, such as `AAPL`. `count` limits the items (default 8, max 250) and `tab` picks `news` (default), `all` or `press_releases`. Stories have title, provider, dates and URLs. A valid empty stream returns `news: []`.
- **Params:** `count` (integer, optional) — News result count; `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL; `tab` (string, optional) — News tab: news, all, or press_releases

### `yahoo_finance_ticker_options`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/options`
- **What:** Yahoo Finance options chain. Returns the option expiration dates (`expiration_dates`, as Unix timestamps) and the current option chain for a Yahoo Finance `symbol` such as `AAPL`. Each `options` entry has an `expiration_date` with its `calls` and `puts`; `underlying` describes the underlying security.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_options_expiration`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/options/{expiration}`
- **What:** Yahoo Finance options chain by expiration. Returns the calls and puts for one expiration of a Yahoo Finance `symbol`. `expiration` is a Unix timestamp, and the options endpoint lists the available ones in `expiration_dates`. The result is an `options` entry with `expiration_date`, `calls` and `puts`.
- **Params:** `expiration` (string, **required**) — Unix expiration timestamp; `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_quote`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/quote`
- **What:** Yahoo Finance ticker quote. Returns fast quote fields for one Yahoo Finance `symbol` such as `AAPL`, for example `regularMarketPrice`, in a `quotes` list alongside the requested `symbols`. The symbol is the only input.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_sec_filings`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/sec-filings`
- **What:** Yahoo Finance SEC filings. Returns the SEC filing summaries Yahoo Finance lists for a `symbol` such as `AAPL`, under `modules.secFilings`. The response echoes the `symbol`, and the symbol is the only input.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_shares`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/shares`
- **What:** Yahoo Finance share counts. Returns the current share-count fields for a Yahoo Finance `symbol` such as `AAPL`, for example `sharesOutstanding`, in `shares`. The symbol is the only input, and the response echoes it as `symbol`.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_shares_full`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/shares-full`
- **What:** Yahoo Finance historical share counts. Returns the historical shares-outstanding series for a Yahoo Finance `symbol`. `start` and `end` accept YYYY-MM-DD, RFC3339 or Unix seconds; without them the last 18 months are returned. Each point has `timestamp`, `datetime` and `shares_out`.
- **Params:** `end` (string, optional) — End date as YYYY-MM-DD, RFC3339, or Unix seconds; `start` (string, optional) — Start date as YYYY-MM-DD, RFC3339, or Unix seconds; `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_splits`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/splits`
- **What:** Yahoo Finance splits. Returns the stock split events for a Yahoo Finance `symbol` such as `AAPL`, each with a Unix timestamp and a split ratio such as `4:1`. The response object also has `dividends` and `capital_gains` fields.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_sustainability`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/sustainability`
- **What:** Yahoo Finance sustainability. Returns ESG and sustainability scores for a Yahoo Finance `symbol` such as `AAPL`, under `modules.esgScores`. When Yahoo recognises the ticker but has no ESG data, `esgScores` comes back empty instead of an error.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_valuation`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/valuation`
- **What:** Yahoo Finance valuation measures. Returns the valuation measures table from Yahoo Finance key statistics for a `symbol` such as `AAPL`, as `headers` and `rows` keyed by column, for example Market Cap. Returns an upstream error when Yahoo does not serve the table.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_trending`

- **HTTP:** `GET /yahoo-finance/trending/{region}`
- **What:** Yahoo Finance trending symbols. Returns the symbols Yahoo Finance lists as trending in a `region` such as `US`. `count` sets how many. The response has `region`, `count`, the `symbols`, and the `job_timestamp` and `start_interval` fields.
- **Params:** `count` (integer, optional) — Symbol count; `region` (string, **required**) — Region such as US

## SEC EDGAR (10)

### `sec_company_intelligence`

- **HTTP:** `GET /sec/company/intelligence`
- **What:** Company 360 overview from SEC data. Aggregates a company's profile, a latest-annual financial snapshot, the latest 10-K/10-Q/8-K, and recent material events into one call. Provide cik or ticker. Optionally fuse live cross-source data with enrich (a comma list of market, news, hiring): market and news are keyed on the ticker; hiring needs ats plus that ATS's careers slug (or tenant/datacenter/site for Workday). Enrichment is best-effort — requested-but-unavailable sources are listed under degraded and never fail the SEC-native response.
- **Params:** `ats` (string, optional) — ATS provider for hiring enrichment; `careers_slug` (string, optional) — Careers board slug for hiring (greenhouse/lever/ashby/smartrecruiters); `cik` (string, optional) — SEC CIK (numeric or zero-padded); `datacenter` (string, optional) — Workday datacenter shard (hiring, when ats=workday); `enrich` (string, optional) — Comma list of cross-source enrichments; `site` (string, optional) — Workday career site (hiring, when ats=workday); `tenant` (string, optional) — Workday tenant (hiring, when ats=workday); `ticker` (string, optional) — Ticker symbol (alternative to cik)

### `sec_company_search`

- **HTTP:** `GET /sec/company/search`
- **What:** Resolve a ticker or company name to EDGAR companies. Resolves a ticker symbol or company-name query to SEC EDGAR companies (CIK, ticker, name).
- **Params:** `limit` (integer, optional) — Max matches, default 10, max 100; `q` (string, **required**) — Ticker symbol or company name

### `sec_company_submissions`

- **HTTP:** `GET /sec/company/submissions`
- **What:** List a company's EDGAR filings. Returns a company's recent SEC filings (form, dates, primary document URL) filtered by form type and date range, plus company profile fields as reported by EDGAR: entity_type, former_names, exchanges, category, fiscal_year_end, state_of_incorporation. Provide cik or ticker.
- **Params:** `cik` (string, optional) — SEC CIK (numeric or zero-padded); `form` (string, optional) — Filter by form type, e.g. 10-K, 10-Q, 8-K; `from` (string, optional) — Earliest filing date (YYYY-MM-DD); `limit` (integer, optional) — Max filings, default 50, max 500; `ticker` (string, optional) — Ticker symbol (alternative to cik); `to` (string, optional) — Latest filing date (YYYY-MM-DD)

### `sec_filing`

- **HTTP:** `GET /sec/filing`
- **What:** Get a single filing by accession number. Returns a single SEC filing's metadata and primary document URL. Provide accession plus cik or ticker.
- **Params:** `accession` (string, **required**) — Accession number; `cik` (string, optional) — SEC CIK (numeric or zero-padded); `ticker` (string, optional) — Ticker symbol (alternative to cik)

### `sec_filing_sections`

- **HTTP:** `GET /sec/filing/sections`
- **What:** Extract 10-K/10-Q/8-K item sections. Extracts item sections (e.g. 1A Risk Factors, 7 MD&A) from a 10-K/10-Q/8-K primary document as clean text. Provide accession plus cik or ticker.
- **Params:** `accession` (string, **required**) — Accession number; `cik` (string, optional) — SEC CIK (numeric or zero-padded); `items` (string, optional) — Comma-separated item numbers to return, e.g. 1A,7; `max_chars` (integer, optional) — Max characters per section, default 20000, max 200000; `ticker` (string, optional) — Ticker symbol (alternative to cik)

### `sec_financials`

- **HTTP:** `GET /sec/financials`
- **What:** Normalized income statement, balance sheet, or cash flow. Returns a company's financial statements across recent periods, resolving EDGAR's inconsistent XBRL tags to a stable schema. Provide cik or ticker.
- **Params:** `cik` (string, optional) — SEC CIK (numeric or zero-padded); `limit` (integer, optional) — Number of periods, default 5, max 20; `period` (string, optional) — Period basis, default annual; `statement` (string, optional) — Statement, default income; `ticker` (string, optional) — Ticker symbol (alternative to cik)

### `sec_frames`

- **HTTP:** `GET /sec/frames`
- **What:** Cross-company values for one XBRL concept and period. Returns every filer's reported value for one XBRL concept in one reporting period (an EDGAR "frame").
- **Params:** `concept` (string, **required**) — XBRL concept tag, e.g. Assets, Revenues; `limit` (integer, optional) — Max companies, default 200, max 2000; `period` (string, **required**) — Reporting frame, e.g. CY2024, CY2024Q1, CY2024Q4I; `taxonomy` (string, optional) — XBRL taxonomy, default us-gaap; `unit` (string, optional) — Unit of measure, default USD

### `sec_full_text_search`

- **HTTP:** `GET /sec/full-text-search`
- **What:** Full-text search across EDGAR filings. Searches the full text of SEC EDGAR filings, filtered by form and date, with pagination. Free where incumbents gate full-text search behind paid tiers.
- **Params:** `forms` (string, optional) — Filter by form types, comma-separated; `from` (string, optional) — Earliest filing date (YYYY-MM-DD); `page` (integer, optional) — 1-based page number, default 1; `q` (string, **required**) — Search query (supports quoted phrases); `to` (string, optional) — Latest filing date (YYYY-MM-DD)

### `sec_insider`

- **HTTP:** `GET /sec/insider`
- **What:** Insider transactions (Forms 3/4/5). Returns a company's recent insider transactions from Form 3/4/5 ownership filings (owner, role, security, shares, price). Provide cik or ticker.
- **Params:** `cik` (string, optional) — SEC CIK (numeric or zero-padded); `limit` (integer, optional) — Max transactions, default 10, max 30; `ticker` (string, optional) — Ticker symbol (alternative to cik)

### `sec_institutional_holdings`

- **HTTP:** `GET /sec/institutional-holdings`
- **What:** Institutional holdings (13F-HR). Returns the latest 13F-HR holdings for an institutional manager (by CIK): issuer, value, shares, sorted by value.
- **Params:** `cik` (string, **required**) — Institutional manager CIK; `limit` (integer, optional) — Max holdings, default 50, max 1000

## Congress (2)

### `congress_report`

- **HTTP:** `GET /congress/report`
- **What:** Fetch and parse a congressional disclosure report. Returns one US Senate disclosure report from the `filing_url` found by the stock-disclosures search, passed as `url`. Supports annual reports, periodic transaction reports and due date extension notices. Output has filer, filing date, `parts` with their rows, and a `transactions` list. House PDFs and paper filings return a validation error.
- **Params:** `url` (string, **required**) — Filing URL, as returned by congress-stock-disclosures' filing_url field. Must be an efdsearch.senate.gov /search/view/annual/..., /search/view/ptr/..., or /search/view/extension-notice/regular/... URL.

### `congress_stock_disclosures`

- **HTTP:** `GET /congress/stock-disclosures`
- **What:** Search congressional stock-disclosure filings. Searches congressional stock-disclosure filings for the House (default) or the Senate via `chamber`. House needs `member`; Senate takes `first_name`, `last_name`, `filer_type`, state and `report_type` filters, and `from`/`to` dates. Each result has member, office, filing year, filing type and `filing_url`. Paged by `page` and `limit` (default 50, max 500).
- **Params:** `candidate_state` (string, optional) — Candidate state filter (Senate only, 2-letter code).; `chamber` (string, optional) — Chamber filter. Allowed values: house, senate.; `district` (string, optional) — House district filter (House only).; `election_year` (string, optional) — House candidate-search election year filter (requires filer_type=candidate).; `filer_type` (string, optional) — Filer-type filter, meaning differs by chamber. House: member (default) or candidate. Senate: comma-separated senator, candidate, former_senator, or the standalone all value. Defaults to senator when omitted.; `first_name` (string, optional) — Senate filer first-name prefix (Senate only; cannot be combined with member).; `from` (string, optional) — Minimum filing date. House accepts YYYY. Senate accepts YYYY or MM/DD/YYYY and defaults to 2012 when omitted.; `last_name` (string, optional) — Senate filer last-name prefix (Senate only; cannot be combined with member).; `limit` (integer, optional) — Max results (1-500).; `member` (string, optional) — Member name. Required for House. For Senate, this backward-compatible shorthand maps one word to last_name and maps the first word plus the complete remaining surname to first_name/last_name; it cannot be combined with either exact name field.; `page` (integer, optional) — 1-based result page (1-1000).; `report_type` (string, optional) — Comma-separated Senate report-type filter (Senate only). Allowed values: annual, periodic_transaction, due_date_extension, blind_trust, other. Defaults to all types when omitted.; `senator_state` (string, optional) — Senator state filter (Senate only, 2-letter code).; `sort` (string, optional) — Sort key. Allowed values: name_asc, name_desc, office_asc, office_desc, filing_year_asc, filing_year_desc.; `state` (string, optional) — State or territory filter (2-letter code). For Senate this backward-compatible shorthand applies to both Senator and Candidate states and cannot be combined with senator_state or candidate_state.; `ticker` (string, optional) — Deprecated unsupported parameter; any non-empty value returns a validation error and the parameter is planned for removal.; `to` (string, optional) — Maximum filing date. House accepts YYYY. Senate accepts YYYY or MM/DD/YYYY.

## CoinGecko (21)

### `coingecko_categories`

- **HTTP:** `GET /coingecko/categories`
- **What:** CoinGecko categories. Lists CoinGecko coin categories, up to `limit` rows (default and max 100), priced in the `vs_currency` you choose. Each row has its rank, id, slug, name, URL, 1h, 24h and 7d percentage changes, market cap, 24h volume and coin count, where CoinGecko shows them.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100; `vs_currency` (string, optional) — Quote currency

### `coingecko_category_coins`

- **HTTP:** `GET /coingecko/category/{slug}/coins`
- **What:** CoinGecko category coins. Lists the coins in one CoinGecko category, identified by the required `slug` such as `stablecoins`. Paged with `page` (default 1) and `limit` (default and max 100), priced in `vs_currency`. Each coin has rank, symbol, price, 1h to 30d changes, 24h volume, market cap and fully diluted valuation.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100; `page` (integer, optional) — Page number, default 1; `slug` (string, **required**) — CoinGecko category slug such as stablecoins; `vs_currency` (string, optional) — Quote currency

### `coingecko_chain`

- **HTTP:** `GET /coingecko/chains/{id}`
- **What:** CoinGecko chain detail. Returns sections from a CoinGecko chain detail page. Sections are omitted when not present. This endpoint supports the documented `vs_currency` enum.
- **Params:** `id` (string, **required**) — CoinGecko chain id such as ethereum; `limit` (integer, optional) — Rows per section to return, default 20, max 100; `vs_currency` (string, optional) — Quote currency

### `coingecko_chains`

- **HTTP:** `GET /coingecko/chains`
- **What:** CoinGecko chains. Lists blockchains from CoinGecko's chains table, up to `limit` rows (default and max 100), in the `vs_currency` you pick. Each chain has its rank, id, name, URL, logo, top gainers, 24h, 7d and 30d changes, 24h volume, TVL, dominance percent and coin count, where shown.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100; `vs_currency` (string, optional) — Quote currency

### `coingecko_coin`

- **HTTP:** `GET /coingecko/coin/{id}`
- **What:** CoinGecko coin profile. Returns CoinGecko profile, market stats, links, and categories for one coin id. This endpoint supports the documented `vs_currency` enum and is not intended for real-time trading.
- **Params:** `id` (string, **required**) — CoinGecko coin id such as bitcoin; `vs_currency` (string, optional) — Quote currency

### `coingecko_coin_analysis`

- **HTTP:** `GET /coingecko/coin/{id}/analysis`
- **What:** CoinGecko coin chart analysis. Returns derived price-chart metrics from CoinGecko public chart JSON. This endpoint supports the documented `vs_currency` enum and is not investment advice or real-time trading data.
- **Params:** `id` (string, **required**) — CoinGecko coin id such as bitcoin; `include_annotations` (boolean, optional) — Fetch optional CoinGecko chart annotations; `range` (string, optional) — Chart range; `vs_currency` (string, optional) — Quote currency

### `coingecko_exchange`

- **HTTP:** `GET /coingecko/exchange/{id}`
- **What:** CoinGecko exchange detail. Returns profile stats and market rows from a CoinGecko exchange page. This endpoint supports the documented `vs_currency` enum.
- **Params:** `id` (string, **required**) — CoinGecko exchange id such as binance; `limit` (integer, optional) — Rows to return, default 100, max 100; `vs_currency` (string, optional) — Quote currency

### `coingecko_exchanges`

- **HTTP:** `GET /coingecko/exchanges`
- **What:** CoinGecko exchanges. Lists CoinGecko exchanges from one table chosen by `kind`: `spot` (default), `dex`, `derivatives` or `perp_dex`. Paged with `page` and `limit` (default and max 100). Each exchange has rank, id, name, URL, logo, and, where shown, a trust score and 24h volume in `vs_currency`.
- **Params:** `kind` (string, optional) — Exchange table kind, default spot; `limit` (integer, optional) — Rows to return, default 100, max 100; `page` (integer, optional) — Page number, default 1; `vs_currency` (string, optional) — Quote currency

### `coingecko_gainers_losers`

- **HTTP:** `GET /coingecko/gainers-losers`
- **What:** CoinGecko crypto gainers and losers. Returns CoinGecko's top crypto gainers and top losers as two separate arrays, `gainers` and `losers`, each up to `limit` rows (default 20, max 100). Each coin has its rank, symbol, name, price in `vs_currency`, 24h percentage change and 24h volume.
- **Params:** `limit` (integer, optional) — Rows per section to return, default 20, max 100; `vs_currency` (string, optional) — Quote currency

### `coingecko_global`

- **HTTP:** `GET /coingecko/global`
- **What:** CoinGecko global market snapshot. Returns CoinGecko's global crypto market snapshot: total market cap in USD with its 24-hour and 1-year change, Bitcoin market cap, Bitcoin and Ethereum dominance, stablecoin market cap and share, and the number of coins, exchanges and categories tracked. Takes no parameters.
- **Params:** _none_

### `coingecko_global_charts`

- **HTTP:** `GET /coingecko/global/charts`
- **What:** CoinGecko global chart series. Returns a time series for one global crypto metric from CoinGecko: total market cap (default), Bitcoin dominance, altcoin market cap or DeFi market cap. Choose a `range` from `24h` to `max` (default `90d`) and cap points per series with `limit` (default 120, max 500). Each point has a timestamp, datetime and value.
- **Params:** `kind` (string, optional) — Chart kind, default total_market_cap; `limit` (integer, optional) — Rows per series to return, default 120, max 500; `range` (string, optional) — Chart range, default 90d

### `coingecko_learn_articles`

- **HTTP:** `GET /coingecko/learn/articles`
- **What:** CoinGecko Learn articles. Lists article cards from CoinGecko Learn, optionally narrowed by `category` (`all` by default, `latest`, `guides`, `reviews`, `api` and others), up to `limit` (default 20, max 50). Each card has title, URL, image, category, excerpt, author, published date and, where present, rating score, text and votes.
- **Params:** `category` (string, optional) — Learn category, default all; `limit` (integer, optional) — Rows to return, default 20, max 50

### `coingecko_markets`

- **HTTP:** `GET /coingecko/markets`
- **What:** CoinGecko markets. Returns cryptocurrency market rows from CoinGecko. This endpoint supports the documented `vs_currency` enum and is not intended for real-time trading.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100; `page` (integer, optional) — Page number, default 1; `vs_currency` (string, optional) — Quote currency

### `coingecko_new_coins`

- **HTTP:** `GET /coingecko/new-coins`
- **What:** CoinGecko new cryptocurrencies. Lists newly listed cryptocurrencies from CoinGecko, paged with `page` (default 1) and `limit` (default and max 100), priced in `vs_currency`. Each coin has its rank, symbol, name, chain, price, 1h and 24h changes, 24h volume, fully diluted valuation and when it was last added.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100; `page` (integer, optional) — Page number, default 1; `vs_currency` (string, optional) — Quote currency

### `coingecko_news`

- **HTTP:** `GET /coingecko/news`
- **What:** CoinGecko news cards. Returns recent crypto news cards from CoinGecko, up to `limit` articles (default 20, max 50). Each article has its title, URL, image URL, summary, publisher and `published_text`, plus the coins it mentions with their id, name, symbol, URL and `change_percent` when present.
- **Params:** `limit` (integer, optional) — Rows to return, default 20, max 50

### `coingecko_nft_category`

- **HTTP:** `GET /coingecko/nft/category/{slug}`
- **What:** CoinGecko NFT category. Lists NFT collections in one CoinGecko NFT category, identified by the required `slug` such as `metaverse`. Paged with `page` and `limit` (default and max 100). Each collection has chain, floor price and market cap in native and USD terms, 24h volume, 24h sales, and 24h, 7d and 30d changes.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100; `page` (integer, optional) — Page number, default 1; `slug` (string, **required**) — CoinGecko NFT category slug such as metaverse; `vs_currency` (string, optional) — Quote currency

### `coingecko_nfts`

- **HTTP:** `GET /coingecko/nfts`
- **What:** CoinGecko NFT collections. Lists NFT collections from CoinGecko's main NFT table, paged with `page` (default 1) and `limit` (default and max 100). Each collection has rank, name, chain, floor price, market cap and 24h volume in native and USD terms, 24h sales, and 24h, 7d and 30d percentage changes.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100; `page` (integer, optional) — Page number, default 1; `vs_currency` (string, optional) — Quote currency

### `coingecko_search`

- **HTTP:** `GET /coingecko/search`
- **What:** CoinGecko discovery search. Searches CoinGecko for the required query `q` and returns matches in separate sections: `coins`, `categories`, `markets`, `nft_contracts`, `asset_platforms` and `posts`, each up to `limit` rows (default 10, max 50). Every section is always an array, and a search with no matches returns empty arrays.
- **Params:** `limit` (integer, optional) — Rows per section to return, default 10, max 50; `q` (string, **required**) — Search query

### `coingecko_token_unlocks`

- **HTTP:** `GET /coingecko/token-unlocks`
- **What:** CoinGecko incoming token unlocks. Returns CoinGecko's list of upcoming token unlocks, up to 100 rows. Each row has the coin's name, symbol, rank, price, 1-hour, 24-hour and 7-day change and market cap, the share of supply already released, and the next unlock's amount, percentage, USD value and time remaining.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100

### `coingecko_treasuries`

- **HTTP:** `GET /coingecko/treasuries`
- **What:** CoinGecko crypto treasuries. Lists entities that hold crypto treasuries, filtered by `asset` (`all`, `bitcoin`, `ethereum`, `solana`, `bnb`, `xrp`, `tron`) and `holder_type` (`all`, `companies`, `governments`), up to `limit` (default and max 100). Setting both filters to non-`all` values is rejected. Rows show holdings, cost, current value, mNAV and 30-day activity.
- **Params:** `asset` (string, optional) — Treasury asset filter, default all; `holder_type` (string, optional) — Treasury holder type filter, default all; `limit` (integer, optional) — Rows to return, default 100, max 100; `vs_currency` (string, optional) — Quote currency

### `coingecko_trending`

- **HTTP:** `GET /coingecko/trending`
- **What:** CoinGecko trending highlights. Returns trending coins and trending categories from CoinGecko's highlights, deduplicated by slug, each section up to `limit` rows (default 20, max 50). Items carry name, URL and, where CoinGecko shows them, price in `vs_currency` and 1h, 24h and 7d percentage changes.
- **Params:** `limit` (integer, optional) — Rows per section to return, default 20, max 50; `vs_currency` (string, optional) — Quote currency

## PitchBook (5)

### `pitchbook_advisor`

- **HTTP:** `GET /pitchbook/advisor`
- **What:** PitchBook advisor profile. Returns the free/teaser content of a PitchBook advisor (service provider, e.g. investment bank, lender, or financing advisory firm) profile page: overview, description, contact/HQ, and a preview of serviced companies/deals, co-lenders, and subsidiaries. PitchBook gates most numeric figures and full lists behind a paid subscription; those come through as empty cells rather than being fabricated. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — PitchBook advisor id; `url` (string, optional) — Absolute https://pitchbook.com/profiles/advisor/<id> URL

### `pitchbook_company`

- **HTTP:** `GET /pitchbook/company`
- **What:** PitchBook company profile. Returns the free/teaser content of a PitchBook company profile page (overview, description, contact/HQ, industry, funding-round history without dollar amounts, a preview of investors, acquisitions, and subsidiaries). PitchBook gates most numeric figures (deal amounts, cap tables, full investor/LP lists) behind a paid subscription; those come through as empty cells rather than being fabricated. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — PitchBook company id; `url` (string, optional) — Absolute https://pitchbook.com/profiles/company/<id> URL

### `pitchbook_fund`

- **HTTP:** `GET /pitchbook/fund`
- **What:** PitchBook fund profile. Returns the free/teaser content of a PitchBook fund profile page (strategy, status, manager, size, vintage, and a preview of limited partners and benchmark peer funds). PitchBook gates most numeric figures (returns/IRR, full LP lists) behind a paid subscription; those come through as empty cells rather than being fabricated. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — PitchBook fund id; `url` (string, optional) — Absolute https://pitchbook.com/profiles/fund/<id> URL

### `pitchbook_investor`

- **HTTP:** `GET /pitchbook/investor`
- **What:** PitchBook investor profile. Returns the free/teaser content of a PitchBook investor (fund manager/firm) profile page (overview, description, contact/HQ, and a preview of investments, exits, and co-investors). PitchBook gates most numeric figures and full lists behind a paid subscription; those come through as empty cells rather than being fabricated. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — PitchBook investor id; `url` (string, optional) — Absolute https://pitchbook.com/profiles/investor/<id> URL

### `pitchbook_limited_partner`

- **HTTP:** `GET /pitchbook/limited-partner`
- **What:** PitchBook limited partner profile. Returns the free/teaser content of a PitchBook limited partner (institutional investor, e.g. pension fund, endowment, or insurance company) profile page: overview, description, contact, and a preview of fund commitments. PitchBook gates most numeric figures and full lists behind a paid subscription; those come through as empty cells rather than being fabricated. Some limited partner profiles have no FAQ section (thinner profiles) -- this is normal, not a sign of a blocked or broken response. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — PitchBook limited partner id; `url` (string, optional) — Absolute https://pitchbook.com/profiles/limited-partner/<id> URL
