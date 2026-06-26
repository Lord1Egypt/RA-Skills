# AI Stock Master for OpenClaw

> A professional AI analysis system powered by 5 legendary investment master models, deeply integrated with [OpenClaw](https://github.com/hengruiyun/ai-stock-master-openclaw) AI Agent.

---

## Overview

**AI Stock Master for OpenClaw** is the official English driver module of [ai-stock-master-openclaw](https://github.com/hengruiyun/ai-stock-master-openclaw).

It injects professional-grade AI analysis capabilities into the OpenClaw AI Agent, enabling it to function like a real financial analyst — providing deep investment insights based on real, live market data.

All conclusions are derived exclusively from the backend intelligence engine. No hallucination. No guesswork.

---

## Core Capabilities

| Module | Description | Function |
|:---|:---|:---|
| **Market Sentiment Radar** | Greed/Fear/Neutral detection via bull-bear ratio analysis | `get_market_sentiment()` |
| **Sector Momentum Ranking** | Track top-performing industries by TMA quantitative score | `get_industry_momentum()` |
| **Sector Leader Tracker** | Identify the strongest blue-chip leaders in any given industry | `get_industry_top_stocks()` |
| **Master Stock Screener** | Full-market scan for stocks with elite rating (level 7+) | `get_quant_picks()` |
| **Capital Flow Monitor** | Real-time detection of hot money inflows via live sector scoring | `get_hot_money_alerts()` |
| **5-Master Stock Diagnosis** | Deep analysis from 5 investment legend models with risk assessment | `get_stock_analysis()` |

---

## The 5 Investment Master Strategy Matrix

This system incorporates the core philosophies of the world's greatest investors:

- **Warren Buffett** — Value investing, long-term trend analysis
- **Peter Lynch** — Growth investing, price momentum confirmation
- **Benjamin Graham** — Margin of safety, undervaluation detection
- And more master strategies...

---

## Quick Start

### Installation

```bash
pip install requests
```

### Basic Usage

```python
from scripts.ttfox_master_driver_en import TTFoxMasterAgentEn

agent = TTFoxMasterAgentEn()

# Get market sentiment
sentiment = agent.get_market_sentiment()
print(sentiment['summary'])

# Analyze a specific stock
result = agent.get_stock_analysis("000548")
print(result['broadcast'])
```

### Integration with OpenClaw

Place this directory into OpenClaw's skills folder. OpenClaw will automatically load `SKILL.md` and register the following scenarios:

- User says **"How is the market?"** → triggers Market Sentiment analysis
- User says **"What are the hot sectors?"** → triggers Capital Flow monitoring
- User says **"Analyze AAPL"** or **"Analyze 000548"** → triggers 11-Master deep diagnosis

---

## File Structure

```
ai-stock-master-en/
├── README.md                        # This documentation file
├── SKILL.md                         # OpenClaw skill registration & trigger config
└── scripts/
    └── ttfox_master_driver_en.py    # Core driver engine
```

---

## Data Sources & Latency

This system retrieves analysis results via the **TTFox Intelligence Server** (`https://master.ttfox.com`).

** MANDATORY NOTICE:**
- **Non-real-time**: All data used by this system are **Non-real-time / Post-market / Static Analysis Packages**. Due to the high computational load required for A-share analysis, there is inherently a significant delay compared to live exchanges.
- **Academic Use Only**: This tool is designed for **Mid-to-Long term trend research** and **Strategic verification**. It is NOT suitable for high-frequency or real-time intraday trading.

---

## Open Source & Support

- **GitHub**: [https://github.com/hengruiyun/ai-stock-master-openclaw](https://github.com/hengruiyun/ai-stock-master-openclaw)
- **Support Email**: [ttfox@ttfox.com](mailto:ttfox@ttfox.com)

---

## Legal Disclaimer

1. **NOT Investment Advice**: This project and all its content (including but not limited to analysis reports, master scores, and suggestions) are provided for **Educational and Academic** purposes only.
2. **No Liability for Latency**: The system generates conclusions from **Delayed Data**. The conclusions may differ significantly from current market conditions. The authors and contributors shall NOT be held liable for any financial losses caused by data lag, analysis errors, or system failure.
3. **Risk Assumption**: Investing in stock markets involves extreme risk. Users assume full responsibility for any investment outcomes based on the information provided by this tool.
