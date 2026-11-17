# US market data sources

## Providers, free tiers, and env vars

| Provider | Env var | Free tier | Best for |
| --- | --- | --- | --- |
| Finnhub | `FINNHUB_API_KEY` | 60 calls/min, US quotes free | Quotes, company profile, financials, candles |
| Polygon.io | `POLYGON_API_KEY` | 5 calls/min, 2 years history | Aggregates, splits/dividends adjusted bars |
| Twelve Data | `TWELVE_DATA_API_KEY` | 8 calls/min, 800/day | Quotes, time series, indicators |
| Alpha Vantage | `ALPHA_VANTAGE_API_KEY` | 25 calls/day | Fundamentals, earnings, FX, ETF profiles |
| SEC EDGAR | none (User-Agent required) | Free, no key | Filings, company facts, insider forms |

All four are optional. Every script in this bundle works offline against a CSV.

## SEC EDGAR (free, authoritative)

```bash
curl -H "User-Agent: your-email@example.com" \
  "https://data.sec.gov/api/xbrl/companyconcept/CIK0000320193/us-gaap/Revenues.json"
```

- `company_tickers.json` maps a ticker to a CIK.
- `companyfacts/CIK##########.json` gives every XBRL fact the company has filed.
- `submissions/CIK##########.json` gives filing history, including 8-Ks and
  Form 4s.
- The SEC requires a descriptive `User-Agent` with a contact email. Rate limit:
  10 requests per second maximum.

## Quote hygiene rules

1. **Timestamp everything.** A quote without an ET timestamp is useless.
2. **Check the feed type.** Delayed (15 min) and real-time quotes must be
   labeled as such.
3. **Split-adjust history.** Use adjusted close for any multi-year comparison.
4. **Cross-check one number.** Compare the provider close against the exchange
   close before publishing the memo.
5. **Do not mix sources in one series.** Pick one provider per series.

## Fundamentals to pull for a US large cap

- Revenue and revenue growth (YoY, 3-year CAGR)
- Gross margin, operating margin, net margin
- Free cash flow and FCF margin
- Net cash or net debt
- Diluted EPS, share count trend (buybacks vs dilution)
- ROIC versus the cost of capital
- Segment revenue mix
- Insider ownership and recent Form 4 activity

## Market sentiment / positioning (optional, needs a paid feed)

- CFTC Commitment of Traders (free, weekly, https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm)
- Short interest (FINRA bi-monthly, https://www.finra.org/finra-data/equity-short-interest)
- Put/call ratio (CBOE publishes daily)

## Macro context (free)

- BLS releases: CPI, PPI, employment situation (BLS schedule)
- FOMC calendar and statements (federalreserve.gov)
- Treasury yields: US Treasury daily yield curve (home.treasury.gov)
- Consumer sentiment: University of Michigan (S&P Global)

## What to do when a source is unavailable

State the gap in the memo: "Sector revenue mix: not available from the sources
used for this memo." Never substitute a remembered number, and never present an
estimate as a fact.
