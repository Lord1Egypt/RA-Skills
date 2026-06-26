# finance-monitor TODO

> Prioritized feature and improvement list for finance-monitor.

## 🔴 High Priority

- [x] Add 8 US stocks (AAPL, MSFT, NVDA, AMZN, META, UNH, KO, BRK.B) from CNBC (2026-03-28)
- [ ] Support more financial data sources (Yahoo Finance, Alpha Vantage) to avoid single-source dependency
- [ ] Add support for international markets (HK, JP, EU)
- [ ] Schedule-based automatic fetching (cron / Windows Task Scheduler)
- [ ] Add data export (CSV, Excel)

## 🟡 Medium Priority

- [ ] Add email/Telegram notification when data fetch fails after all retries
- [ ] Support proxy configuration via environment variables
- [ ] Add `--verbose` / `--quiet` CLI flags
- [ ] Cache last-known good data and serve it when fetch fails
- [ ] Add `weekly` and `monthly` summary aggregation views

## 🟢 Low Priority / Nice to Have

- [ ] Web dashboard to visualize fetched data
- [ ] Add unit tests for `parse_html_content()` with mocked HTML samples
- [ ] Add integration tests against live CNBC pages
- [ ] Dockerfile for containerized deployment
- [ ] Historical data import (backfill from archived pages)

## ✅ Completed

- [x] Fetch 18 financial indicators from CNBC (2026-03-24)
- [x] SQLite database storage with `indicators` and `fetch_log` tables (2026-03-24)
- [x] Error handling: FetchError, RateLimitError, DatabaseError (2026-03-24)
- [x] Retry logic: 3 retries with exponential backoff for network failures (2026-03-24)
- [x] HTTP 429 rate limit handling with Retry-After header support (2026-03-24)
- [x] DB write error handling with graceful exit (2026-03-24)
- [x] 52-week high/low distance calculation (2026-03-24)
- [x] Unit tests (test_fetch_data.py, 474 lines) (2026-03-25)
- [x] requirements.txt (stdlib only, documented) (2026-03-25)
