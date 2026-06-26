---
name: finance-data
description: "Fetch professional stock market data from Yahoo Finance (yfinance) and SEC EDGAR. Use when: user asks about stock prices, market data, company financials, earnings, analyst recommendations, SEC filings (10-K, 10-Q, 8-K), insider transactions, options chains, dividend history, company profiles, XBRL financial concepts, or any equity research task. Supports US stocks, Chinese A-shares (e.g. 600519.SS), and international markets."
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": ["python3"] } } }
---

# Finance Data Skill

Fetch professional stock and financial data from **Yahoo Finance** (via yfinance) and **SEC EDGAR** (free public API).

## Setup

Install the Python dependency (one-time):

```bash
pip install -r skills/finance-data/scripts/requirements.txt
```

SEC EDGAR requires a User-Agent header identifying the requester. Set the env var (optional — a default is provided):

```bash
export SEC_EDGAR_USER_AGENT="YourName your@email.com"
```

## Ticker Formats

| Market            | Format  | Example                       |
| ----------------- | ------- | ----------------------------- |
| US stocks         | Symbol  | `AAPL`, `MSFT`, `GOOGL`       |
| Shanghai A-shares | Code.SS | `600519.SS` (Moutai)          |
| Shenzhen A-shares | Code.SZ | `000858.SZ` (Wuliangye)       |
| Hong Kong         | Code.HK | `0700.HK` (Tencent)           |
| Tokyo             | Code.T  | `7203.T` (Toyota)             |
| London            | Code.L  | `HSBA.L` (HSBC)               |
| ETFs / Indices    | Symbol  | `SPY`, `QQQ`, `^GSPC`, `^HSI` |

## Yahoo Finance Commands

All commands output JSON to stdout.

### Current Quote

```bash
python3 scripts/yfinance_query.py quote AAPL
```

Returns: price, volume, market cap, P/E, EPS, 52-week range, moving averages, dividend yield, beta, profit margins, etc.

### Historical Prices (OHLCV)

```bash
# Last month, daily
python3 scripts/yfinance_query.py history AAPL

# Last year, weekly
python3 scripts/yfinance_query.py history AAPL --period 1y --interval 1wk

# Last 5 days, 5-minute bars
python3 scripts/yfinance_query.py history AAPL --period 5d --interval 5m
```

Period options: `1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max`
Interval options: `1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo`

### Financial Statements

```bash
# All statements (income, balance sheet, cash flow) — annual
python3 scripts/yfinance_query.py financials AAPL

# Quarterly income statement only
python3 scripts/yfinance_query.py financials AAPL --statement income --quarterly

# Balance sheet only
python3 scripts/yfinance_query.py financials AAPL --statement balance

# Cash flow only
python3 scripts/yfinance_query.py financials AAPL --statement cashflow
```

### Full Company Profile

```bash
python3 scripts/yfinance_query.py info AAPL
```

Returns all available metadata: sector, industry, description, officers, full-year financials, etc.

### Shareholders

```bash
python3 scripts/yfinance_query.py holders AAPL
```

Returns institutional holders, major holders breakdown, and insider transactions.

### Analyst Recommendations & Price Targets

```bash
python3 scripts/yfinance_query.py analysts AAPL
```

Returns recent analyst recommendations (buy/hold/sell) and consensus price targets.

### Dividend History

```bash
python3 scripts/yfinance_query.py dividends AAPL
```

### Options Chain

```bash
# Nearest expiry (default)
python3 scripts/yfinance_query.py options AAPL

# Specific expiry date
python3 scripts/yfinance_query.py options AAPL --expiry 2025-06-20
```

Returns calls and puts with strike, bid, ask, volume, open interest, implied volatility.

### Earnings

```bash
python3 scripts/yfinance_query.py earnings AAPL
```

Returns quarterly and annual earnings (revenue, earnings, surprise).

### News

```bash
python3 scripts/yfinance_query.py news AAPL
```

Returns recent news headlines with links.

## SEC EDGAR Commands

Free public API — no API key required. All US public company filings.

### Full-Text Search

```bash
# Search across all filings
python3 scripts/sec_edgar.py search --query "artificial intelligence" --limit 10

# Filter by form type and date
python3 scripts/sec_edgar.py search --query "revenue growth" --form-type 10-K --date-from 2024-01-01
```

### Company Filings

```bash
# Recent filings by ticker
python3 scripts/sec_edgar.py filings AAPL --limit 20

# Filter by form type
python3 scripts/sec_edgar.py filings AAPL --form-type 10-K
python3 scripts/sec_edgar.py filings AAPL --form-type 10-Q
python3 scripts/sec_edgar.py filings AAPL --form-type 8-K

# By CIK number
python3 scripts/sec_edgar.py filings 320193 --form-type 10-K
```

Common form types: `10-K` (annual), `10-Q` (quarterly), `8-K` (current events), `DEF 14A` (proxy), `S-1` (IPO), `13F-HR` (institutional holdings).

### Read Filing Content

Download and extract readable text from an SEC filing. Use the `url` from the `filings` command output.

```bash
# Read full filing (first 50000 chars by default)
python3 scripts/sec_edgar.py read-filing --url "https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm"

# Read a specific 10-K section (much more focused)
python3 scripts/sec_edgar.py read-filing --url "URL" --section 7    # MD&A
python3 scripts/sec_edgar.py read-filing --url "URL" --section 1    # Business
python3 scripts/sec_edgar.py read-filing --url "URL" --section 1a   # Risk Factors
python3 scripts/sec_edgar.py read-filing --url "URL" --section 8    # Financial Statements

# Control output length
python3 scripts/sec_edgar.py read-filing --url "URL" --max-chars 100000
```

10-K section numbers: `1` (Business), `1a` (Risk Factors), `2` (Properties), `5` (Market), `7` (MD&A), `7a` (Quantitative Disclosures), `8` (Financial Statements), `9a` (Controls), `10` (Directors), `11` (Executive Compensation), `12` (Security Ownership).

**Recommended workflow for reading annual reports:**

```bash
# Step 1: find the latest 10-K filing
python3 scripts/sec_edgar.py filings AAPL --form-type 10-K --limit 1

# Step 2: read a specific section using the url from step 1
python3 scripts/sec_edgar.py read-filing --url "<url_from_step_1>" --section 7
```

### Filing Document Index

List all documents within a filing package (useful for finding exhibits, XBRL files, etc.):

```bash
python3 scripts/sec_edgar.py filing-index AAPL --accession "0000320193-25-000079"
```

### Company Metadata

```bash
python3 scripts/sec_edgar.py submissions AAPL
```

Returns company name, CIK, SIC code, address, phone, fiscal year end, exchanges, and filing count.

### Structured Financial Data (XBRL)

```bash
# List all available XBRL concepts for a company
python3 scripts/sec_edgar.py company AAPL

# Get time-series for a specific concept
python3 scripts/sec_edgar.py concept AAPL --concept Revenue
python3 scripts/sec_edgar.py concept AAPL --concept NetIncomeLoss
python3 scripts/sec_edgar.py concept AAPL --concept EarningsPerShareBasic
python3 scripts/sec_edgar.py concept AAPL --concept Assets
python3 scripts/sec_edgar.py concept AAPL --concept StockholdersEquity
```

Useful XBRL concepts: `Revenue`, `NetIncomeLoss`, `EarningsPerShareBasic`, `EarningsPerShareDiluted`, `Assets`, `Liabilities`, `StockholdersEquity`, `OperatingIncomeLoss`, `CashAndCashEquivalentsAtCarryingValue`, `LongTermDebt`.

### Insider Transactions

```bash
python3 scripts/sec_edgar.py insider AAPL --limit 20
```

Returns Forms 3, 4, 5 filings (insider buys/sells/grants) with links to SEC documents.

## Common Workflows

**Quick stock check:**

```bash
python3 scripts/yfinance_query.py quote TSLA
```

**Fundamental analysis:**

```bash
python3 scripts/yfinance_query.py financials MSFT --statement income
python3 scripts/yfinance_query.py financials MSFT --statement balance
python3 scripts/sec_edgar.py concept MSFT --concept Revenue
python3 scripts/sec_edgar.py concept MSFT --concept NetIncomeLoss
```

**Read the latest annual report (10-K):**

```bash
# 1. Find the latest 10-K
python3 scripts/sec_edgar.py filings AAPL --form-type 10-K --limit 1
# 2. Read the MD&A section (most important for investors)
python3 scripts/sec_edgar.py read-filing --url "<url>" --section 7
# 3. Read the risk factors
python3 scripts/sec_edgar.py read-filing --url "<url>" --section 1a
```

**Due diligence / SEC filings:**

```bash
python3 scripts/sec_edgar.py filings NVDA --form-type 10-K --limit 5
python3 scripts/sec_edgar.py insider NVDA --limit 20
python3 scripts/sec_edgar.py submissions NVDA
```

**Compare multiple stocks:**

Run quote or financials commands for each ticker and compare the JSON output side by side.

## Notes

- yfinance data is sourced from Yahoo Finance — may have a 15-minute delay for real-time prices
- SEC EDGAR is official SEC data — always accurate but filings may lag by a few days
- SEC rate limit: max 10 requests/second per IP; the scripts respect this by default
- Chinese A-share tickers use `.SS` (Shanghai) or `.SZ` (Shenzhen) suffix in yfinance
- XBRL concepts are case-sensitive (e.g. `Revenue` not `revenue`)
