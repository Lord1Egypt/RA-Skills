---
name: eodhd
description: >
  Provides access to EODHD financial data APIs covering company information, market prices,
  fundamentals, economic data, exchange info, and alternative datasets. Use this skill
  when the user asks for company information or profile data (company name, description,
  address, website, officers, sector, industry, exchange, ISIN, logo), stock prices,
  financial fundamentals, earnings, dividends, forex, crypto, macro indicators, news
  sentiment, options data, insider transactions, ESG scores, or any financial market data.
  For company information requests, prefer the Fundamentals API first, then Search API,
  Exchange Symbol List, ID Mapping, and News API as needed. All requests are made via curl
  using the EODHD REST API.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - EODHD_API_TOKEN
      bins:
        - curl
    primaryEnv: EODHD_API_TOKEN
    emoji: "📈"
---

# EODHD Financial APIs

## Routing for company information

When the user asks for **company information**, **company profile**, **tell me about a company**,
**what company is this ticker**, or similar, use these endpoints in this order:

1. **Fundamentals API** — primary source for full company profile and fundamentals
2. **Search API** — find the correct symbol when the user gives only a name
3. **Exchange Symbol List API** — validate symbol, company name, exchange, type, ISIN
4. **ID Mapping API** — resolve ISIN / CUSIP / FIGI / LEI / CIK to ticker
5. **News API** — add recent company-specific news when requested
6. **Insider Transactions API** — add insider activity when requested
7. **Calendar API** — add earnings, dividends, IPO, or split events when requested

### Minimum company-info response

For a company-info request, try to return:
- Company name
- Ticker and exchange
- Sector and industry
- Business description
- Website
- Country / address when available
- Market cap / valuation highlights when available
- Recent earnings / dividend / insider context when the user asks for it

### Primary company-profile curl examples
```bash
# Full company profile + fundamentals
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=${EODHD_API_TOKEN}"

# Only general company profile fields
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=${EODHD_API_TOKEN}&filter=General"

# Company highlights / valuation
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=${EODHD_API_TOKEN}&filter=Highlights,Valuation"

# Find company by name first
curl "https://eodhd.com/api/search/apple?api_token=${EODHD_API_TOKEN}&limit=10&fmt=json"

# Validate company on exchange and get company name / ISIN
curl "https://eodhd.com/api/exchange-symbol-list/US?api_token=${EODHD_API_TOKEN}&fmt=json"

# Resolve ISIN to ticker
curl "https://eodhd.com/api/isin?api_token=${EODHD_API_TOKEN}&isin=US0378331005&fmt=json"
```

## Authentication

- Base URL: `https://eodhd.com/api/`
- API key: **ALWAYS** read from env first: `echo $EODHD_API_TOKEN`. NEVER hardcode or guess the token. NEVER use the demo key.
- Always append `&fmt=json` for JSON output

## Ticker Format

| Asset Class  | Format           | Example        |
|-------------|------------------|----------------|
| AU Stocks   | `TICKER.AU`      | `CBA.AU`       |
| US Stocks   | `TICKER.US`      | `AAPL.US`      |
| UK Stocks   | `TICKER.LSE`     | `BARC.LSE`     |
| ETFs        | `TICKER.US`      | `VTI.US`       |
| Crypto      | `SYMBOL-USD.CC`  | `BTC-USD.CC`   |
| Forex       | `PAIR.FOREX`     | `AUDUSD.FOREX` |
| Indices     | `SYMBOL.INDX`    | `GSPC.INDX`    |

## Common Parameters

| Parameter   | Values              | Description                    |
|------------|---------------------|--------------------------------|
| `api_token`| string              | Required — your API key        |
| `fmt`      | `json` / `csv`      | Response format (default: csv) |
| `from`     | `YYYY-MM-DD`        | Start date                     |
| `to`       | `YYYY-MM-DD`        | End date                       |
| `order`    | `a` / `d`           | Ascending or descending        |
| `period`   | `d` / `w` / `m`     | Daily, weekly, or monthly      |
| `limit`    | integer             | Max results                    |
| `offset`   | integer             | Pagination offset              |

---

## 1. Market Data

### End-of-Day Historical Prices

```bash
curl "https://eodhd.com/api/eod/{TICKER}.{EXCHANGE}?api_token=${EODHD_API_TOKEN}&fmt=json"
curl "https://eodhd.com/api/eod/CBA.AU?api_token=${EODHD_API_TOKEN}&from=2024-01-01&to=2024-12-31&order=d&fmt=json"
curl "https://eodhd.com/api/eod/CBA.AU?api_token=${EODHD_API_TOKEN}&period=m&fmt=json"
```

### Live / Real-Time Quotes

```bash
curl "https://eodhd.com/api/real-time/CBA.AU?api_token=${EODHD_API_TOKEN}&fmt=json"
curl "https://eodhd.com/api/real-time/CBA.AU?s=BHP.AU,ANZ.AU&api_token=${EODHD_API_TOKEN}&fmt=json"
```

### Intraday Data

Intervals: `1m`, `5m`, `1h`. Date range uses Unix timestamps.

```bash
curl "https://eodhd.com/api/intraday/CBA.AU?api_token=${EODHD_API_TOKEN}&interval=1h&fmt=json"
curl "https://eodhd.com/api/intraday/CBA.AU?api_token=${EODHD_API_TOKEN}&interval=5m&from=1609459200&to=1609545600&fmt=json"
```

### Tick Data (US Only)

```bash
curl "https://eodhd.com/api/ticks/AAPL.US?api_token=${EODHD_API_TOKEN}&fmt=json&from=2024-01-02&to=2024-01-02"
```

### Technical Indicators

Functions: `sma`, `ema`, `wma`, `macd`, `rsi`, `atr`, `bbands`, `sar`, `stddev`

```bash
curl "https://eodhd.com/api/technical/CBA.AU?api_token=${EODHD_API_TOKEN}&fmt=json&function=sma&period=50"
curl "https://eodhd.com/api/technical/CBA.AU?api_token=${EODHD_API_TOKEN}&fmt=json&function=rsi&period=14"
```

### Bulk EOD (US Exchanges)

```bash
curl "https://eodhd.com/api/eod-bulk-last-day/US?api_token=${EODHD_API_TOKEN}&fmt=json"
curl "https://eodhd.com/api/eod-bulk-last-day/US?api_token=${EODHD_API_TOKEN}&symbols=AAPL,MSFT&fmt=json"
```

---

## 2. Corporate Actions

### Dividends

```bash
curl "https://eodhd.com/api/div/CBA.AU?api_token=${EODHD_API_TOKEN}&fmt=json"
curl "https://eodhd.com/api/div/CBA.AU?api_token=${EODHD_API_TOKEN}&from=2020-01-01&fmt=json"
```

### Splits

```bash
curl "https://eodhd.com/api/splits/CBA.AU?api_token=${EODHD_API_TOKEN}&fmt=json"
```

### Stock Market Screener

```bash
curl "https://eodhd.com/api/screener?api_token=${EODHD_API_TOKEN}&filters=[[\"market_capitalization_mln\",\">\",1000]]&sort=market_capitalization_mln.desc&limit=10&fmt=json"
```

---

## 3. Fundamentals

### Company Fundamentals

Full: financials, balance sheet, cash flow, holders, valuation.

```bash
curl "https://eodhd.com/api/fundamentals/CBA.AU?api_token=${EODHD_API_TOKEN}"
curl "https://eodhd.com/api/fundamentals/CBA.AU?api_token=${EODHD_API_TOKEN}&filter=General,Highlights,Valuation,Financials::Income_Statement"
```

### ESG Scores

```bash
curl "https://eodhd.com/api/fundamentals/CBA.AU?api_token=${EODHD_API_TOKEN}&filter=ESGScores"
```

### Historical Market Capitalisation

```bash
curl "https://eodhd.com/api/historical-market-cap/CBA.AU?api_token=${EODHD_API_TOKEN}&fmt=json&from=2020-01-01"
```

### Insider Transactions

```bash
curl "https://eodhd.com/api/insider-transactions?api_token=${EODHD_API_TOKEN}&code=CBA.AU&fmt=json"
curl "https://eodhd.com/api/insider-transactions?api_token=${EODHD_API_TOKEN}&code=CBA.AU&from=2024-01-01&to=2024-12-31&fmt=json"
```

---

## 4. Calendar & Events

### Earnings

```bash
curl "https://eodhd.com/api/calendar/earnings?api_token=${EODHD_API_TOKEN}&fmt=json&from=2025-01-01&to=2025-01-31"
curl "https://eodhd.com/api/calendar/trends?api_token=${EODHD_API_TOKEN}&symbols=CBA.AU&fmt=json"
```

### Dividends Calendar

```bash
curl "https://eodhd.com/api/calendar/dividends?api_token=${EODHD_API_TOKEN}&fmt=json&from=2025-01-01&to=2025-01-31"
```

### IPOs

```bash
curl "https://eodhd.com/api/calendar/ipos?api_token=${EODHD_API_TOKEN}&fmt=json&from=2025-01-01&to=2025-06-30"
```

### Economic Events

```bash
curl "https://eodhd.com/api/economic-events?api_token=${EODHD_API_TOKEN}&fmt=json&from=2025-01-01&to=2025-01-31"
curl "https://eodhd.com/api/economic-events?api_token=${EODHD_API_TOKEN}&fmt=json&country=AU&from=2025-01-01"
```

---

## 5. News & Sentiment

```bash
curl "https://eodhd.com/api/news?api_token=${EODHD_API_TOKEN}&s=CBA.AU&limit=20&fmt=json"
curl "https://eodhd.com/api/news?api_token=${EODHD_API_TOKEN}&t=stocks&limit=20&fmt=json"
curl "https://eodhd.com/api/news?api_token=${EODHD_API_TOKEN}&s=CBA.AU&from=2024-01-01&to=2024-01-31&fmt=json"
```

---

## 6. Macro & Economic Indicators

Country codes: `AUS` (Australia), `USA`, `GBR`, etc.

```bash
curl "https://eodhd.com/api/macro-indicator/AUS?api_token=${EODHD_API_TOKEN}&fmt=json&indicator=gdp_current_usd"
curl "https://eodhd.com/api/macro-indicator/AUS?api_token=${EODHD_API_TOKEN}&fmt=json&indicator=inflation_consumer_prices_annual"
curl "https://eodhd.com/api/macro-indicator/AUS?api_token=${EODHD_API_TOKEN}&fmt=json"
```

---

## 7. Options (US Only)

```bash
curl "https://eodhd.com/api/options/AAPL.US?api_token=${EODHD_API_TOKEN}&fmt=json"
curl "https://eodhd.com/api/options/AAPL.US?api_token=${EODHD_API_TOKEN}&fmt=json&to=2025-03-21"
```

---

## 8. Exchange & Search

### Search Tickers

```bash
curl "https://eodhd.com/api/search/commonwealth?api_token=${EODHD_API_TOKEN}&limit=10&fmt=json"
curl "https://eodhd.com/api/search/commonwealth?api_token=${EODHD_API_TOKEN}&type=stock&fmt=json"
```

### List Tickers on Exchange

```bash
curl "https://eodhd.com/api/exchange-symbol-list/AU?api_token=${EODHD_API_TOKEN}&fmt=json"
curl "https://eodhd.com/api/exchange-symbol-list/AU?api_token=${EODHD_API_TOKEN}&fmt=json&type=etf"
```

### List Exchanges

```bash
curl "https://eodhd.com/api/exchanges-list?api_token=${EODHD_API_TOKEN}&fmt=json"
```

### Exchange Details (Trading Hours, Holidays)

```bash
curl "https://eodhd.com/api/exchange/AU?api_token=${EODHD_API_TOKEN}&fmt=json"
```

### ID Mapping (ISIN / CIK to Ticker)

```bash
curl "https://eodhd.com/api/isin?api_token=${EODHD_API_TOKEN}&isin=AU000000CBA7&fmt=json"
```

---

## 9. API Usage

```bash
curl "https://eodhd.com/api/user?api_token=${EODHD_API_TOKEN}&fmt=json"
```

---

## Notes

- Always append `&fmt=json` — default response is CSV
- Real-time quotes have 15-20 min delay on free plans
- Always include `from` and `to` date parameters to avoid pulling excessive data
- Rate limits depend on subscription tier — check the usage endpoint
