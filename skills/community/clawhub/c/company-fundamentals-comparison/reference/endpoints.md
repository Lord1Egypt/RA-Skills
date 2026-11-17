# company-fundamentals-comparison — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**11 endpoints across 2 platform group(s).**

## SEC EDGAR (6)

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

## Yahoo Finance (5)

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

### `yahoo_finance_ticker_financials`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/financials`
- **What:** Yahoo Finance financial statements. Returns financial statement data for a Yahoo Finance `symbol`. `statement` picks `income`, `balance-sheet` or `cash-flow` (aliases `income-statement`, `balance` and `cashflow` also work) and `period` picks `annual`, `quarterly` or `trailing`; trailing is supported for income and cash flow only. The response echoes `statement` and `period`, with the data under `modules`.
- **Params:** `period` (string, optional) — annual, quarterly, or trailing; `statement` (string, optional) — Statement type. Allowed values: income (alias income-statement), balance-sheet (alias balance), cash-flow (alias cashflow); `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_info`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/info`
- **What:** Yahoo Finance ticker info. Returns profile and quote information for a Yahoo Finance `symbol` such as `AAPL`, under `modules`: the profile, quote type (`quoteType`), price, statistics and summary modules. The symbol is the only input.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL
