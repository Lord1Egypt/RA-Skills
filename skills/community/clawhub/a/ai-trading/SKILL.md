---
name: ai-trading
description: Research US stocks and ETFs like a buy-side analyst: live quotes, technicals, fundamentals, sector context, backtests and a written trade plan with position sizing and hard risk rules. Human approval is required before any order - analysis and education, never financial advice or auto-trading.
version: 1.0.5
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    envVars:
      - name: FINNHUB_API_KEY
        required: false
        description: Optional. US market quotes, company profiles and financials.
      - name: POLYGON_API_KEY
        required: false
        description: Optional. US equities quotes, aggregates and OHLC bars.
      - name: TWELVE_DATA_API_KEY
        required: false
        description: Optional. Alternative quote and technical-indicator provider.
      - name: ALPHA_VANTAGE_API_KEY
        required: false
        description: Optional. Fundamentals, earnings and FX reference data.
    emoji: "\u1F4C8"
    homepage: https://github.com/rapidworker1
---

# AI Trading

**A research desk for US equities and ETFs.** Pull the data, run the numbers,
write the memo, size the position, and stop at the approval gate.

Use this skill when someone asks for:

- a stock pick, thesis, or "what should I look at" on a US ticker
- technical analysis: SMA/EMA, RSI, ATR, support/resistance, volume
- fundamentals: revenue, margins, EPS, valuation multiples, sector context
- a backtest of a simple strategy on US historical data
- position sizing, risk per trade, portfolio exposure, R-multiple math
- a written research memo or a pre-trade plan for a US symbol
- market-hours, earnings-date, or US market holiday questions

---

## What this skill does (and does not) do

**Does:** research, analysis, education, planning, documentation.

**Does not:** place orders, connect to a brokerage account, guarantee returns,
give personalized investment advice, or trade on someone else's behalf.

**Hard rule: this skill never submits an order and never pretends to.** Every
plan ends at an approval gate. If a user asks for automatic execution, this
skill produces the plan and a checklist for the human to execute in their own
broker.

---

## Workflow

1. **Frame the question.** Ticker + exchange (US), time horizon, and the thesis
   in one sentence. If the ticker is ambiguous, confirm the company first.
2. **Pull the data.** Use the runtime's market data tools, or
   `scripts/market_snapshot.py` when a provider key is available.
3. **Run the numbers.** Technicals, key fundamentals, sector context.
4. **Build the plan.** `scripts/portfolio_risk.py` produces a position size from
   the user's own risk rules.
5. **Write the memo.** `templates/equity-research-report.md`.
6. **Stop at the approval gate.** Present the plan, list what would invalidate
   it, and ask for explicit approval.

## Quickstart

**Snapshot a US ticker:**

```bash
python3 scripts/market_snapshot.py --symbol AAPL --provider finnhub
python3 scripts/market_snapshot.py --symbol AAPL --bars /path/to/aapl.csv --out snapshot.json
```

`--bars` reads a local CSV (`date,open,high,low,close,volume`) so the skill works
with no API key at all.

**Size a position (risk-first):**

```bash
python3 scripts/portfolio_risk.py \
  --equity 25000 --risk-pct 0.5 \
  --entry 182.40 --stop 178.10 \
  --open-positions positions.csv --out plan.json
```

Output: shares to buy, dollar risk, R multiple, portfolio heat after the trade,
and the rules it checked against.

**Research memo:** copy `templates/equity-research-report.md` and fill it with
real numbers. Never ship a memo with unfilled numbers - say "not available"
instead of estimating.

---

## US market facts this skill assumes

| Item | Value |
| --- | --- |
| Regular session | 9:30 AM - 4:00 PM ET (NYSE / Nasdaq) |
| Pre-market | 4:00 AM - 9:30 AM ET |
| After-hours | 4:00 PM - 8:00 PM ET |
| Settlement | T+1 (since May 2024) |
| Timezone | America/New_York - always convert with an ET-aware timestamp |
| Holidays | See `references/us-market-calendar.md` |
| Earnings | Typically before open or after close; verify the date with the source |
| Splits/dividends | Split-adjusted prices - verify before comparing across dates |
| Options | 4:00 PM ET expiry for standard listed options |

Never assume a market is open. Check the ET clock and the holiday list first.

## Analysis standards

- **Every number has a source and a timestamp.** "Price $182.40 (Finnhub, 2026-10-21 15:42 ET)".
- **Separate fact from inference.** Facts in one section, your read in another.
- **State the base rate.** If a setup historically works 52% of the time, say so.
- **Give the invalidation level before the target.** If you cannot say what would prove you wrong, you do not have a thesis.
- **Position size comes from risk, not conviction.** A bigger conviction is not a bigger size by default.

## Risk rules (defaults - users may override in writing)

```
Risk per trade      0.5% of equity (hard ceiling 1%)
Max sector exposure 25% of equity
Max single position 10% of equity
Max portfolio heat  6% of equity (total open risk)
Daily loss limit    2% of equity -> stop trading for the day
Stop loss           always defined before entry
Overnight risk      positions that gap risk: halve the size
```

`scripts/portfolio_risk.py` enforces these and reports violations.

## Guardrails (hard rules)

- **No guaranteed returns.** No "guaranteed", "risk-free", "can't lose", "100%".
- **No fabricated data.** If a quote, metric, or earnings date is unavailable, say so plainly. Never invent a price or a filing.
- **No order execution.** This skill does not trade, does not request brokerage credentials, and does not ask for API keys that can move money.
- **No pump-and-dump content.** Never write content designed to move a low-float stock.
- **No insider information.** Only public sources. If asked about non-public information, decline.
- **No signal-selling funnels.** Do not frame analysis as a paid trading signal service.
- **Disclose conflicts.** If the publisher has a position in the name, say so.
- **Education disclaimer.** Every deliverable ends with a short risk note, and the report states it is not personalized investment advice.

## Files in this bundle

```
references/
  us-market-calendar.md   Sessions, ET, 2026 NYSE/Nasdaq holidays, half days
  data-sources.md          Providers, free tiers, env vars, SEC EDGAR
  risk-playbook.md         Position sizing, R multiples, journal template
templates/
  equity-research-report.md
  trade-plan.md
scripts/
  market_snapshot.py       Quotes + technicals (API or local CSV)
  portfolio_risk.py        Position sizing + portfolio heat + rule checks
```

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `401` from provider | Key missing or wrong - use `--bars` with a CSV instead |
| Empty snapshot | Check the ticker is a valid US symbol, not an option contract |
| Stale price | Provider returns delayed quotes outside regular hours - check the timestamp |
| CSV parse error | Header must be `date,open,high,low,close,volume` |

## Related

- [`ai-creative-studio`](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) — turn a research memo into social posts, ad copy and email for your audience.
- [`b2b-lead-research-agent`](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) — find the companies (and their investor-relations pages) worth researching.
- **[Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite)** — one Windows kit that sets up research, content and lead workflows side by side. The desktop app is a separate download from the publisher's GitHub release, with a published SHA-256 so you can check the file before you unpack it; no skill bundle carries an installer.

---

*This skill produces research and educational analysis. It is not investment
advice, not a recommendation to buy or sell any security, and not a substitute
for a licensed adviser. Markets can lose you money. Verify every number against
the primary source before acting.*
