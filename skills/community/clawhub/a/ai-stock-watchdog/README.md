# AI stock watchdog

A daily watchdog for your Indian equity holdings (NSE/BSE). Optional scheduled run; you can also trigger scans manually. Stays silent unless a **Sev-1** rule in `severity-rubric.md` fires.

> The rubric weights governance, promoter/pledge and insider activity, cash flow quality, earnings vs consensus, surveillance, and sector regulation. It is **not** investment advice — always verify from primary sources.

## What makes v2 different

v1 focused on news and filings. v2 adds structured checks (see table):

| Capability | v1 | v2 |
|---|---|---|
| Promoter holding & pledge tracking | Basic pledge check | Full QoQ comparison, encumbrance tracking, insider selling detection, pledge liquidation alerts |
| Cash flow quality analysis | Not present | CFO/PAT ratio tracking, working capital cycle, receivable/inventory divergence — catches window dressing |
| Segment-level analysis | Not present | Conglomerate drill-down with per-segment peers and key metrics |
| Management credibility | Not tracked | Guidance vs delivery scoring over quarters |
| Portfolio health | Not present | Concentration risk, sector correlation, STCG/LTCG awareness, anchor bias detection |
| India market calendar | Not present | RBI MPC, Budget, F&O expiry, result season awareness |
| Positive signals | Not present | Promoter buying, buybacks, credit upgrades, contract wins |
| Banking-specific metrics | Basic | NIM, CASA, GNPA/NNPA, slippage ratio, credit cost, CD ratio, PCR |
| Severity context | Static | Peer-relative, horizon-adjusted, position-size-weighted, market-regime-aware |

## What it watches for

The skill classifies every signal against a severity rubric and only surfaces **Sev-1 critical** events:

| Category | Examples |
|---|---|
| **Promoter signals** | Holding decline >2pp QoQ, pledge >50%, open market sale by promoter, KMP insider selling pre-results |
| **Governance shocks** | Auditor resignation/qualification, SEBI/ED/CBI action, forensic audit, CEO/CFO exit, related party transaction spike |
| **Cash flow manipulation** | CFO negative while PAT positive, CFO/PAT <0.5x for 2+ quarters, receivables growing 2x revenue |
| **Capital structure stress** | Credit downgrade ≥2 notches, interest coverage <1.5x, debt maturity wall, pledge invocation |
| **Earnings shock** | Revenue/PAT >20–25% below consensus, EBITDA margin compression >300bps, guidance cut >15% |
| **Concall red flags** | Demand weakness, capex cut, declining order book, tone shift + missed guidance |
| **Surveillance flags** | GSM Stage 2+, ASM Long-term, T2T, trading suspension |
| **Sector regulation** | RBI PCA, USFDA Warning Letter, govt ban/duty change, TRAI tariff order |
| **Short-term triggers** | Promoter block deal ≥1% equity, 7%+ single-day fall on 3x volume, 52W low on heavy volume |
| **Conglomerate segment** | Segment EBIT turned negative, cross-subsidization pattern, subsidiary IPO cancelled |

Full rubric: see `severity-rubric.md`.

## How you use it

Everything is conversational. You never edit any JSON.

### First time
Say *"set up stock monitor"* and the skill walks you through:
1. Share your holdings (screenshot or text)
2. Investment horizon (short / medium / long term)
3. Alert sensitivity (critical-only recommended)
4. Optional daily scheduled scan

### Ongoing
- **Update holdings**: *"I bought 10 shares of XYZ at 1265"*, *"sold all my ABC"*, *"trimmed 20 of PQR"*, or drop a broker screenshot
- **Manual scan**: *"check my stocks"*, *"morning brief"*, *"anything I should know?"*
- **Portfolio health**: *"portfolio health check"*, *"how's my portfolio"*

### Alert format
On a Sev-1 hit:

```
🔴 STOCK ALERT — {date}

{TICKER} — {one-line headline}
Severity: Sev-1 | Category: {category} | Sector: {sector}

What happened: [factual, with specific numbers]

Why it matters for YOU ({horizon} holder, avg ₹{price}, {N} shares — {X}% of portfolio):
- [portfolio-specific impact]
- [historical pattern context]

Suggested action: WATCH CLOSELY
Confidence: Medium-High
Management credibility: MEDIUM (missed guidance)

Sources:
- [Title](URL)

Counter-view: [what could make this NOT critical]

Portfolio impact: {X}% of your capital.
```

On quiet days: **nothing**. Silence is the feature.

## Supported brokers (screenshot extraction)
Zerodha Kite, Groww, Upstox, Angel One, ICICI Direct, Kotak Neo, and most others with a clear holdings table.

## Out of scope
- F&O / derivatives (cash equities only)
- Mutual funds / ETFs
- US/global stocks
- Direct trade execution

## Install

### Via ClawHub (recommended)
```bash
openclaw skills install ai-stock-watchdog
```
Then say *"set up stock monitor"* in any supported agent.

### Manual
Copy this folder into your agent's skills directory and say *"set up stock monitor"*.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Full workflow and methodology |
| `portfolio.json` | Your holdings (managed by skill) |
| `competitors.json` | Sector peers + conglomerate segments + regulator mapping |
| `severity-rubric.md` | Sev-1/2/3 rules with context modifiers |
| `sources.md` | Data sources with search query templates |
| `manifest.json` | Skill metadata |
| `state/last-run.json` | Alert history, guidance tracker, suppression log |
| `alerts/` | Archived alerts |
| `examples/` | Worked example scenarios |

## Disclaimer
**This skill is informational only and is NOT investment advice.** It surfaces signals against a transparent rubric you can read and customise. All buy/sell decisions are yours. The author is not a SEBI-registered investment advisor. Stock investments are subject to market risk. Past performance is not indicative of future returns.

## License
MIT-0 — see `LICENSE`.
