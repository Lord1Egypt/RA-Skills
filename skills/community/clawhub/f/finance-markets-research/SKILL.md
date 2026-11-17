---
name: finance-markets-research
description: Research stocks, crypto, SEC filings, insider/congressional trading, and private-market profiles through Crawlora. Use for one-ticker data, filing lookups, or market snapshots; for matched financial-statement comparisons across public-company peers, use company-fundamentals-comparison.
---

# Finance & markets research

Pull equities, crypto, SEC filings, and private-market data as normalized
JSON from the Crawlora API — no scraping finance sites or parsing 10-Ks by hand.

## When to use this skill

- "What's the price / financials / news for <ticker>?" or "chart its history."
- "What are <ticker>'s recent SEC filings / insider trades / institutional holders?"
- "What did <member of Congress> trade recently?"
- "What's <coin>'s market cap / price / trending right now?"
- "Give me a profile of <VC firm / private company / fund / LP>."
- Stock screening, earnings calendars, sector/industry overviews.
- For sampled Reddit discussion around a ticker alongside same-window price
  context, use reddit-stock-sentiment-research when installed.
- For a period-matched financial statement matrix across multiple public
  companies, use company-fundamentals-comparison.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

Pick the data domain, then the job:

1. **Equities (Yahoo Finance)** — `/yahoo-finance/ticker/{symbol}/quote|info|history|financials|analysts|news|options|holders|dividends|splits` for one symbol; `/yahoo-finance/screener/{id}` or `POST /yahoo-finance/screener` to screen; `/yahoo-finance/search` to resolve a name to a symbol; `/yahoo-finance/trending/{region}` for what's hot.
2. **SEC filings** — `/sec/company/search` to resolve ticker→CIK, then
   `/sec/company/submissions`, `/sec/filing`, `/sec/filing/sections` (10-K/10-Q
   item extraction), `/sec/financials` (normalized statements), `/sec/insider`
   (Forms 3/4/5), `/sec/institutional-holdings` (13F-HR). `/sec/full-text-search`
   searches across all EDGAR filings; `/sec/frames` compares one XBRL concept
   across every filer for a period.
3. **Congress** — `/congress/stock-disclosures` to search public
   congressional trade disclosures; `/congress/report` for one filed report's
   parsed detail.
4. **Crypto (CoinGecko)** — `/coingecko/coin/{id}` for a coin profile,
   `/coingecko/markets` for market rows, `/coingecko/trending`/`/gainers-losers`
   for momentum, `/coingecko/global` for the overall market.
5. **Private markets (PitchBook)** — `/pitchbook/company|fund|investor|advisor|limited-partner`
   free/teaser profile pages (query params identify the entity — see reference).

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Equities:
scripts/crawlora.sh /yahoo-finance/ticker/AAPL/quote | jq '.'
scripts/crawlora.sh /yahoo-finance/ticker/AAPL/history period=1y interval=1d | jq '.'

# SEC filings (resolve ticker → CIK first):
scripts/crawlora.sh /sec/company/search q="Apple Inc" | jq '.'
scripts/crawlora.sh /sec/company/submissions cik=0000320193 | jq '.'
scripts/crawlora.sh /sec/insider cik=0000320193 | jq '.'

# Congress:
scripts/crawlora.sh /congress/stock-disclosures ticker=NVDA | jq '.'

# Crypto:
scripts/crawlora.sh /coingecko/coin/bitcoin | jq '.'
scripts/crawlora.sh /coingecko/trending | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Yahoo Finance,
SEC EDGAR, Congress, CoinGecko, and PitchBook endpoint this skill uses.

## Examples

- **Ticker deep-dive:** `/yahoo-finance/ticker/{symbol}/info` +
  `/financials` + `/analysts` + `/ticker-news`, cross-checked against
  `/sec/financials` for the audited numbers.
- **Insider-trading watch:** `/sec/insider` for a company's Form 4 filings,
  and `/congress/stock-disclosures` filtered by the same ticker to see if
  lawmakers traded it too.
- **Crypto momentum scan:** `/coingecko/gainers-losers` then `/coingecko/coin/{id}`
  for the top movers' fundamentals.
- **VC due diligence:** `/pitchbook/company` for the teaser profile, then
  `/pitchbook/investor` for its backers.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public quote/filing/disclosure pages; not investment advice.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **PitchBook profiles are free-tier teasers** (not the paid platform's full data)
  — treat fields as directional, not exhaustive.
- SEC full-text search only covers filings from 2001 onward.
