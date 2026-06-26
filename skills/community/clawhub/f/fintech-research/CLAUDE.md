# CC Fintech Research Toolkits — 100% Free, Self-Hosted, Global Equity Markets (US, HK, CN)

## Project Introduction

This project transforms Claude Code into a professional equity research agent for **global markets** — US, Hong Kong, and A-Share Connect. It provides 24 analysis skills, a free data MCP server, and a personalization layer — all 100% self-contained with zero external dependencies on paid services.

**Market coverage:**
- **US equities**: Full support via yfinance + SEC EDGAR + FRED macro
- **Hong Kong equities**: Native .HK support via yfinance + HKEX News scraping
- **A-Share Connect**: AH spread analysis for dual-listed stocks

## Intent Map

| Command | Trigger Keywords | What It Does | Example |
|---------|-----------------|-------------|---------|
| `/probe` | "discover", "thematic", "themes", "screen", "find ideas", "what to buy" | Scans global markets for thematic opportunities, supply-chain plays, and alternative ideas | "Screen US semiconductor stocks" or "Find HK EV supply chain plays" |
| `/dive` | "analyze", "deep dive", "business model", "earnings", "financial forensics" | Deep fundamental analysis on a single ticker (business model, financials, management, reporting quality) | "Dive into AAPL" or "Analyze 0700.HK business model" |
| `/track` | "monitor", "watchlist", "track", "thesis check", "event radar" | Ongoing monitoring: price alerts, thesis validation, event tracking for portfolio holdings | "Track NVDA position" or "Monitor my HK watchlist" |
| `/landscape` | "macro", "yield curve", "trade flows", "labor market", "rates" | Macro landscape analysis across CN-HK-US tri-polar framework | "Show CN-HK-US yield curves" or "Compare US vs HK tech valuations" |

## Data Sources — All Free

| Tier | Source | Cost | Coverage |
|------|--------|------|----------|
| P0 Core | yfinance | Free (MIT) | **Global** equities (US, HK, CN) |
| P0 Core | SEC EDGAR | Free (official API) | **US** filings (10-K, 10-Q, 8-K) |
| P0 Core | HKEX News | Free (public) | **HK** announcements, filings |
| P1 Macro | FRED | Free (official API) | **US** macro, rates, FX |
| P1 Macro | HKMA | Free (public) | **HK** monetary statistics |
| P2 News | NewsAPI | Free tier (100/day) | **Global** news headlines |
| P2 News | RSS Feeds | Free | **Global** financial news feeds |

## Market Support Details

### US Equities (Full Support)
- All US tickers via yfinance (AAPL, MSFT, GOOGL, NVDA, TSLA, META, etc.)
- SEC EDGAR filings: 10-K, 10-Q, 8-K with full-text search
- FRED macro: Treasury yields, Fed Funds, CPI, unemployment, DXY
- US market news via NewsAPI with sentiment scoring

### Hong Kong Equities (Native Support)
- All HKEX-listed stocks via yfinance `.HK` suffix
- Hang Seng Index top 50 constituents pre-configured
- HKEX regulatory announcements and filings scraping
- HK tech leaders: Tencent (0700.HK), Alibaba (9988.HK), Meituan (3690.HK), Xiaomi (1810.HK), BYD (1211.HK), Kuaishou (1024.HK), Li Auto (2015.HK)
- A-share connect flows and AH spread analysis

### A-Share Connect (Cross-Market)
- AH spread analysis for dual-listed stocks (A-share vs H-share premium/discount)
- Limited A-share coverage via yfinance `.SS` / `.SZ` suffixes

## Constraint: No External Projects / Paid Services

- **All code is self-contained** in this repository
- **No calls to external projects** or paid APIs — all functionality is self-contained
- **All data sources are free** with zero subscription requirement
- MCP server runs locally via stdio transport

## Anthropic Skill Path

Skill definitions are loaded from `.claude/commands/` directory:
- `.claude/commands/probe.md`
- `.claude/commands/dive.md`
- `.claude/commands/track.md`
- `.claude/commands/landscape.md`

Mode and style settings are read from `.claude/mode.md` and `.claude/style.md`.

## Routing Examples

**Example 1 — US equity**: "Dive into AAPL"
1. Parse ticker: `AAPL` → recognized as US equity
2. Keyword match: "dive" → maps to `/dive` command
3. Execute: Load `dive` skill → call `get_ticker_info("AAPL")` → call `get_price_history("AAPL")` → call `get_sec_filings("AAPL")` → perform business model + financial + earnings analysis
4. Output: Structured deep-dive report with US context (SEC filings, FRED macro backdrop)

**Example 2 — HK equity**: "analyze 0700.HK"
1. Parse ticker: `0700.HK` → recognized as HKEX-listed stock (Tencent Holdings)
2. Keyword match: "analyze" → maps to `/dive` command
3. Execute: Load `dive` skill → call `get_ticker_info("0700.HK")` → call `get_price_history("0700.HK")` → call `get_hkex_disclosures("0700")` → perform business model + financial analysis
4. Output: Structured deep-dive report with HK context (AH spread, connect flow, HKEX filings)
