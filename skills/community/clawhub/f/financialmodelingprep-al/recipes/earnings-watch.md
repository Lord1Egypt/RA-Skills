# Recipe: Earnings Watch

## Goal
Monitor the earnings calendar for a user's watchlist and report upcoming (and recent) earnings dates with estimates vs actuals — grounded in FMP data.

## When to use
The user asks "when does <company> report earnings", "what's coming up this week for my watchlist", or wants to track earnings events.

## Inputs
- A watchlist of tickers (resolve any names first).
- A date window (`from`, `to`); default the next 1–4 weeks.
- `FMP_API_KEY` in the environment.

## Steps
1. **Resolve every name** in the watchlist to a confirmed ticker (search → profile). Keep the symbol set.
2. **Pull the calendar:** `/earnings-calendar?from=<YYYY-MM-DD>&to=<YYYY-MM-DD>`. This returns events across many companies.
3. **Filter client-side** to the watchlist symbols (the endpoint is market-wide; do not assume it pre-filters).
4. **Read fields** per event: `symbol`, `date`, `time`, `epsEstimated`, `epsActual`, `revenueEstimated`, `revenueActual`.
5. **Distinguish forecast vs actual:** estimates are forecasts; actuals only exist for past events. Label clearly.
6. **Report sorted by date**, each with as-of/source.

## Output
- A date-sorted list of watchlist earnings events in the window.
- For each: symbol, date/time, EPS estimate (and actual if reported), revenue estimate/actual.
- Source + note that estimates are forecasts and dates can change.

## Example
> **Earnings watch (2026-06-01 → 2026-06-14; FMP `/earnings-calendar`)**
> - AAPL — 2026-06-04 (after close). EPS est. 1.45 (forecast). Revenue est. 92.0B.
> - NVDA — 2026-06-11 (after close). EPS est. 0.88 (forecast).
> Actuals will populate after each report. Estimates are consensus forecasts and dates may change. Source: FMP. *Informational only, not investment advice.*

(Illustrative format only — report live API values.)

## Edge cases
- **Symbol not in the window** → no event; say "no scheduled earnings in this window" rather than inventing one.
- **Date changes** → companies move dates; treat the calendar as as-of the query time.
- **Non-US / uncovered tickers** → may be absent on the free tier; flag coverage.
- **Empty array** → no events in range, or coverage limit; verify the window and symbols.

## Production notes
- One calendar call per window covers the whole watchlist — far cheaper than per-symbol calls. Filter locally.
- Cache the calendar for the window; re-pull only when the window changes or to refresh actuals after reports.
- Keep forecast vs actual labeling strict to avoid implying realized numbers.
