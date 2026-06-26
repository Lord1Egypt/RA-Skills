---
name: crypto-trading-decision-framework
emoji: 📊
category: Finance & Trading
tags: [trading, crypto, position-sizing, risk-management, entry-exit, decision-framework]
description: >
  Structured decision system for crypto traders — position sizing, entry checklist, exit framework,
  and halt decision tree. Eliminates ad-hoc calls and enforces disciplined risk management on every trade.
  Use when sizing a new position, evaluating an entry, managing a live trade, or deciding when to halt
  a strategy. Prevents the most common trader failure modes: oversizing, moving stops, and holding losers.
author: Kenneth Kim (KK_HoldCo)
version: 1.0.0
---

# Crypto Trading Decision Framework

**Bottom line:** Every trade decision runs through 3 gates — sizing, entry checklist, exit plan. If any gate fails, the trade doesn't happen. No exceptions.

---

## When to invoke

Any trading discussion that involves:
- New position entry recommendation
- Position sizing for any asset
- Stop loss / take profit calibration
- Risk-reward analysis
- Live trade management
- Strategy halt / kill decisions
- Portfolio concentration calls

---

## Gate 1 — Position Sizing

### Step 1: Risk per trade
- **Default:** 1% of total liquid portfolio per single trade
- **Aggressive:** 2% if conviction ≥85% AND backtest sample n≥30 trades
- **Conservative:** 0.5% on first trade in a new strategy or unfamiliar asset

### Step 2: Stop distance
- **Hard stop:** Always at the level that technically invalidates the thesis
- **Time stop:** Default 48 bars on 4H, 24 bars on 1H (strategy isn't playing out on schedule = exit)
- **Trailing stop:** Activate after first 1R achieved; trail at 0.5R below current price

### Step 3: Position size formula
```
Position size (notional) = (Risk % ÷ Stop distance %) × Liquid portfolio
Example: 1% risk, 1.5% stop distance → (1/1.5) × $50,000 = ~$33,333 notional
```

For leveraged accounts: cap leverage at 3× for new strategies, 5× for proven strategies with n≥50 live trades.

---

## Gate 2 — Entry Checklist (must answer all YES)

1. ☐ Backtest sample size n ≥ 20 trades
2. ☐ Profit factor (PF) ≥ 1.3 in out-of-sample test window (not just training)
3. ☐ Max drawdown (MDD) ≤ 20%
4. ☐ Out-of-sample (OOS) returns positive
5. ☐ Strategy has a clear thesis — not just curve-fitting
6. ☐ Current market regime matches strategy's design regime (mean-reversion in choppy, trend-following in trending)
7. ☐ Position size compliant with Gate 1 above
8. ☐ Hard stop level identified pre-entry
9. ☐ Time exit level identified pre-entry
10. ☐ Take profit ladder identified (TP1 / TP2 / TP3 if multi-target)

**Scoring:**
- 10/10 YES → proceed
- 8-9/10 YES → proceed with caution, note the gaps
- < 8/10 YES → DO NOT ENTER
- < 6/10 YES → KILL THE STRATEGY entirely

---

## Gate 3 — Exit Framework

### Priority order for exits
1. **Hard stop hit** — thesis invalidated. Cut without question. No re-evaluation during the close.
2. **Time stop hit** — strategy hasn't played out in expected timeframe. Exit at market.
3. **Take profit hit** — pre-planned TP reached. Exit per ladder (e.g., 50% at TP1, 25% at TP2, 25% trail).
4. **Signal flip** — strategy generates the opposite signal. Exit + flip.
5. **Regime change** — macro backdrop has shifted materially (e.g., dominance flip, Fear & Greed regime change).
6. **Discretionary** — user decision. Done.

### What NOT to do (the most common losses)
- ❌ Moving stops further away mid-trade ("just give it more room")
- ❌ Adding to losing positions ("averaging down" on a broken thesis)
- ❌ Early exit on a winner before TP1 unless thesis explicitly broke
- ❌ Second-guessing a planned exit because of hope or FOMO
- ❌ Holding past time stop because "it might come back"

---

## R:R Minimums by Strategy Type

| Strategy type | Minimum R:R | Win rate floor |
|---|---|---|
| Mean reversion | 1.5:1 | 60% |
| Trend following | 2.5:1 | 40% |
| Breakout | 3:1 | 35% |
| News-driven / event | 4:1 | 30% |
| Funding/yield carry | N/A | N/A |

If a setup doesn't clear BOTH the R:R minimum and the historical win rate floor → **DO NOT RECOMMEND**.

---

## Strategy Halt Decision Tree

When a live strategy is underperforming, work through this tree top to bottom:

```
1. Has the strategy hit its account-level kill-switch loss?
   YES → HALT immediately. Post-mortem before any restart.
   NO → next step.

2. Has the strategy hit -3R drawdown beyond its expected backtest MDD?
   YES → PAUSE for 5 trading days. Re-evaluate regime fit.
   NO → next step.

3. Is the live profit factor ≤ 50% of backtest PF over n≥10 live trades?
   YES → SHRINK position size 50%, run another 10 trades, re-evaluate.
   NO → next step.

4. Has the strategy produced zero signals for N days, where N > 2× expected signal frequency?
   YES → Strategy is dead in current regime. KILL or re-tune thresholds.
   NO → Normal volatility. No action needed.
```

---

## Real-Money Escalation Rules

These always require human approval — never autonomous execution:
- New live capital deployment of any size
- Increasing an existing live capital allocation
- Moving a strategy from paper to live
- Stop loss override or removal
- Adding to a losing position
- Manual close of an open live position
- Any single action that reduces account equity by >5%

---

## 4-Model Consensus Rule (for large capital decisions)

For any deployment of significant capital:
1. **Primary LLM** — full recommendation with confidence tags
2. **Second LLM** — independent macro + asset-specific opinion
3. **Third LLM** — code/execution path audit + edge case check
4. **Fourth LLM** — risk/sizing sanity check

If 2+ models disagree → defer 24h, re-run consensus tomorrow. Disagreement = edge case, not clear enough to act.

---

## Confidence Tags (include on every trading recommendation)

Always attach 3 tags to any trade call:
- **Confidence:** % belief the recommendation is correct (60-95% typical)
- **Research depth:** % of relevant data actually pulled this session (50-90% typical)
- **Reality gap:** % unknowns / black-swan exposure (5-25% typical)

Example: "Confidence 82% / Research Depth 75% / Reality Gap 20%"

This keeps recommendations honest and prevents overconfidence drift.

---

## Output Format

When this framework produces a trade recommendation, structure it as:

```
## Trade Recommendation: [ASSET] [LONG/SHORT]

**Thesis:** [1-2 sentences — why this setup exists]
**Regime fit:** [why current market supports this strategy type]

**Sizing:**
- Portfolio size: $X
- Risk per trade: $X (1%)
- Stop distance: X%
- Position notional: $X

**Entry checklist:** X/10 YES [list any NO items]
**R:R:** X:1 [minimum met: YES/NO]

**Levels:**
- Entry: $X
- Hard stop: $X (thesis invalidated if price reaches here because: [reason])
- TP1: $X (partial exit X%)
- TP2: $X (partial exit X%)
- Time stop: [date/bar count]

**Confidence:** X% / Research Depth X% / Reality Gap X%

**Escalation required:** YES/NO [why]
```
