---
name: "drt-self-improving-agent"
description: "Self-improving DRT/ICT trading agent — journals every trade (setup type, bias, R:R, outcome), analyzes its own win/loss patterns, and builds a personal trading memory that makes the agent smarter over time. 100% lokal — ingen netværkskald."
metadata: {"clawbot": {"requires": {"python3": true}, "notes": "100% lokal analyse — ingen netværkskald, ingen API-nøgle."}}
---

# DRT Self-Improving Trading Agent 🤖📈

A trading agent that **learns from its own trades**. Every trade is journaled → analyzed → patterns are discovered → the agent adjusts its own rules. The more trades, the sharper it gets.

## What the skill does

1. **Journals** every trade (DRT type, bias, entry/SL/TP, R:R, outcome, killzone)
2. **Analyzes patterns** — which setups win, which lose, what time of day
3. **Builds memory** — `trades.json` grows with every trade
4. **Learns and adjusts** — prints changed rules based on data (not gut feeling)
5. **Proactive** — reminds about killzones and A+ setups

## Files

```
drt-self-improving-agent/
├── SKILL.md
├── scripts/
│   ├── journal.py      # Add trade to trades.json (CLI)
│   ├── analyze.py      # Analyze patterns + print learnings
└── data/
    └── trades.json     # Trade memory (auto-created)
```

## Quick start

```bash
# Journal a trade (after every trade!)
python3 scripts/journal.py --symbol SP500 --bias LONG --type 2 \
  --entry 7741 --sl 7681 --tp 7802 --rr 2.5 --result win --killzone NY

# See what the agent has learned
python3 scripts/analyze.py

```

## Journal fields

| Field | Value | Description |
|------|-------|-----------|
| `symbol` | SP500, BTCUSD… | Instrument |
| `bias` | LONG / SHORT | Direction |
| `type` | 1, 2, 3 | DRT type (continuation/reversal/consolidation) |
| `entry` / `sl` / `tp` | price | Trade levels |
| `rr` | 1.5, 2.0, 3.0 | R:R at entry |
| `result` | win / loss / be | Outcome |
| `killzone` | London, NY, SB-AM, SB-PM | Where the trade was taken |
| `notes` | text | Free note (e.g. "sweep 12 bars old") |

## Learning logic (analyze.py)

The agent prints concrete learnings, e.g.:
- "Type 2 LONG wins 92% — keep taking them"
- "Trades in SB-PM lose 60% — avoid or tighten the filter"
- "R:R < 1.5 gives 40% WR — skip, wait for 2R+"
- "When the sweep is older than 12 bars: 0 winners — set an age gate"

## Killzone reminder (proactive)

Use the agent to remind about trading windows (CET/Danish time):
- London 09:00-11:00 · NY 14:30-17:00 · SB AM 09:00-10:00 · SB PM 19:30-21:30
- ⛔ Never NY open 15:30-16:00 · max 3 trades/day · SL ALWAYS

## Rules that never change (even if the data says otherwise)
- Stop loss ALWAYS · Max 3 trades/day · Never revenge trade
- Only A+ setups — a high win rate requires saying no to 80% of setups
---
