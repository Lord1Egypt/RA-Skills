---
name: fintech-research
description: >
  100% free, self-hosted equity research toolkit for Claude Code with global
  market support (US, HK, CN). Provides 24 analysis skills across 4 command
  families (/probe, /dive, /track, /landscape) backed by a local MCP server
  connecting to yfinance (global quotes), SEC EDGAR (US filings), HKEX News
  (HK announcements), FRED (US macro), NewsAPI and RSS (global news) — all
  free, zero subscription required.
version: 2.0.2
license: Apache-2.0
metadata:
  openclaw:
    tags:
      - fintech
      - equity-research
      - us-stocks
      - hong-kong-stocks
      - a-shares
      - yfinance
      - sec-edgar
      - hkex
      - fred
      - free-data
      - claude-code
      - mcp
      - finance
      - investing
    category: Data & APIs
    languages:
      - en
      - zh-CN
      - ja
    requires:
      - description: "Python 3.10+ with pip"
        command: "python3 --version"
      - description: "Claude Code CLI"
        command: "claude --version"
    env:
      - name: FRED_API_KEY
        description: "Optional. Free API key from fred.stlouisfed.org for US macro data"
        required: false
      - name: NEWS_API_KEY
        description: "Optional. Free API key from newsapi.org for global news signals"
        required: false
---

# Fintech Research Toolkit

Transform Claude Code into a professional equity research agent for **global equity markets** — all 100% free and self-hosted.

## What This Skill Provides

### 4 Command Families

| Command | Purpose | Example |
|---------|---------|---------|
| `/probe` | Thematic discovery, supply-chain scanning, alt-plays | "Screen US semiconductor stocks" or "Find HK EV supply chain" |
| `/dive` | Single-company deep analysis | "Dive into AAPL" or "Analyze 0700.HK business model" |
| `/track` | Position tracking, thesis validation, event radar | "Track NVDA position" or "Monitor my HK portfolio" |
| `/landscape` | Macro research across CN-HK-US | "Compare US vs HK tech valuations" |

### 24 Analysis Skills

- **9 Anthropic official skills** (Apache 2.0): initiating-coverage, earnings-preview, earnings-analysis, model-update, morning-note, catalyst-calendar, thesis-tracker, idea-generation, sector-overview
- **14 Community skills**: themes, supply-chain, alt-plays, business-model, financial-forensics, earnings-scorecard, reporting-quality, management, watchlist, thesis-check, event-radar, yield-curve, trade-flows, labor-market

### Free Data MCP Server

A local MCP server (`mcp-server/server.py`) providing 10 tools across three markets:

**US Equities:**
| Tool | Data Source | Free Basis |
|------|-------------|------------|
| `get_ticker_info` | yfinance | Open source |
| `get_price_history` | yfinance | Open source |
| `batch_ticker_info` | yfinance | Open source |
| `get_sec_filings` | SEC EDGAR | Official free API |
| `get_macro_data` | FRED | Official free API |

**Hong Kong Equities:**
| Tool | Data Source | Free Basis |
|------|-------------|------------|
| `get_ticker_info` | yfinance | Open source |
| `get_hkex_disclosures` | HKEX News | Public access |
| `get_ah_spread` | yfinance | Open source |

**Global / All Markets:**
| Tool | Data Source | Free Basis |
|------|-------------|------------|
| `get_news_signals` | NewsAPI + RSS | Free tier |
| `fiscal_calendar` | Local JSON | Self-maintained |
| `run_sql` | SQLite cache | Local |

## Market Coverage

### US Equities
- **yfinance**: Quotes, fundamentals, history for all US tickers (AAPL, MSFT, GOOGL, NVDA, TSLA, META, etc.)
- **SEC EDGAR**: Official filings (10-K, 10-Q, 8-K)
- **FRED**: Treasury yields, Fed Funds, CPI, unemployment, DXY
- **NewsAPI**: US market news with sentiment

### Hong Kong Equities
- **yfinance**: Quotes, fundamentals, history for all `.HK` tickers
- **HKEX News**: Regulatory announcements scraping
- **65 Pre-configured tickers**: Hang Seng Top 50 + tech leaders
- **AH Spread**: A-share vs H-share premium/discount
- **Stock Connect**: Northbound/southbound flow

### A-Share Equities (via Connect)
- **AH Spread**: Cross-market price comparison
- **yfinance**: Limited coverage via `.SS` / `.SZ`

## Setup

```bash
git clone https://github.com/fredtai/Fintech-research.git
cd Fintech-research
pip install -r requirements.txt
claude
# /mcp to verify → then /probe, /dive, /track, /landscape
```

## Optional API Keys (enhanced features, not required)

- `FRED_API_KEY` — fred.stlouisfed.org (free) for US macro data
- `NEWS_API_KEY` — newsapi.org (free, 100 req/day) for global news

## Personalization

- `.claude/mode.md` — `new` or `experienced`
- `.claude/style.md` — depth(quick/balanced/deep), tone(professional/conversational), coverage(global/us-only/hk-only)

## License

Apache 2.0 — Community skills and scaffolding. Anthropic skills bundle is also Apache 2.0 (vendored from `anthropics/financial-services`).
