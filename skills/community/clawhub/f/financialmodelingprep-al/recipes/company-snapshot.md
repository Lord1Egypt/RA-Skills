# Recipe: Company Snapshot

## Goal
Produce a concise, cited one-page snapshot of a company: who they are, current price, size, and a few key metrics — grounded entirely in FMP data.

## When to use
The user asks "give me an overview of <company>", "what's the snapshot on <ticker>", or wants a quick grounded profile before deeper analysis.

## Inputs
- Company name or ticker (from the user).
- `FMP_API_KEY` in the environment.

## Steps
1. **Resolve the symbol.** If a name was given, call `/search-name?query=<company>` (or `fmp_search`). Pick the primary listing; note `symbol`, `exchange`, `currency`.
2. **Confirm identity.** Call `/profile?symbol=<TICKER>` (`fmp_company_profile`). Read `companyName`, `sector`, `industry`, `country`, `ceo`, `marketCap`, `currency`, `description`, `isActivelyTrading`. Verify it's the company the user meant.
3. **Get the quote.** Call `/quote?symbol=<TICKER>` (`fmp_quote`). Read `price`, `changePercentage`, `marketCap`, `volume`, `timestamp`.
4. **Get key metrics.** Call `/key-metrics?symbol=<TICKER>&period=annual&limit=1` (`fmp_key_metrics`). Read `peRatio`, `enterpriseValue`, per-share figures.
5. **Assemble** the snapshot with every figure cited (symbol, endpoint, period, currency, as-of).

## Output
A short structured block:
- Identity: name, ticker, exchange, sector/industry, country.
- Price: last (delayed) price + % change + as-of timestamp + currency.
- Size: market cap, enterprise value.
- A few metrics: P/E and one or two others, with period.
- Source + disclaimer.

## Example
> **Apple Inc. (AAPL — NASDAQ, USD)**
> Sector: Technology / Consumer Electronics. CEO: Tim Cook.
> Price: 192.34 USD, +0.8% (delayed quote, as of 2026-05-30 16:00 ET; FMP `/quote`).
> Market cap: 2.98T USD (FMP `/quote`). Enterprise value: 3.01T USD (FMP `/key-metrics`, FY2024).
> P/E: 31.2x (FMP `/key-metrics`, FY2024, filing-based).
> Source: Financial Modeling Prep. Data as-of latest available; newer data may exist. *Informational only, not investment advice.*

(Numbers above are illustrative of format — report only what the live API returns.)

## Edge cases
- **Empty array** on quote/profile → symbol wrong or not covered; re-resolve or explain coverage.
- **Non-USD currency** → label clearly; do not assume USD.
- **Multiple listings** (ADR vs local) → state which you used.
- **`isActivelyTrading=false`** → flag the company may be delisted/inactive.

## Production notes
- Cache the profile and quote; reuse if the same company is asked again in-session.
- This is 3–4 calls; on the free tier, don't repeat them needlessly.
- Keep the as-of timestamp visible so the snapshot is auditable.
