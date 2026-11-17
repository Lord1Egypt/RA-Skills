---
name: "drt-trading"
description: "Dealing Range Theory (DRT) — complete ICT structure: Type 1 (continuation), Type 2 (reversal), Type 3 (consolidation), quadrant levels (25/50/75), entry models, SMT confirmation and news filter. For market analysis and trade setups."
metadata: {"clawbot": {"requires": {"python3": true}, "notes": "100% lokal analyse og backtest — ingen netværkskald, ingen API-nøgle."}}
---

# DRT — Dealing Range Theory 📐

## Foundation
- Price is delivered by the IPDA algorithm: it seeks **liquidity above old highs / below old lows**, and rebalances Fair Value Gaps.
- A **Dealing Range** forms after a **liquidity raid** (sweep of a swing high/low).
- Range boundaries: **DRH** (Dealing Range High) and **DRL** (Dealing Range Low).
- Price rotates between **internal range liquidity** and **external range liquidity** (raids).
- The range is divided into **4 equal quadrants** → levels: **25DRT, 50DRT, 75DRT**.
  - **25DRT** = extreme discount (buy zone)
  - **50DRT** = equilibrium (balance)
  - **75DRT** = extreme premium (sell zone)
- Buy in discount → sell in premium.

## The 3 Types of Dealing Ranges

### Type 1 — Continuation ⬆️⬇️
- **Situation:** After the raid, price continues in the **same direction** as the raid → trend/continuation toward DRH or DRL.
- **What the algorithm does:** Delivers price toward the opposite range boundary without a deep retracement.
- **Detection:** Raid of swing high/low → price breaks **through** the relative equal levels with **displacement** (strong candle) → continues.
- **Entry:** Retest of the broken level or **50DRT** after displacement.
- **Target:** DRH (for longs) / DRL (for shorts) — often 3R+.
- **SL:** Behind the raid level (sweep extreme + buffer).

### Type 2 — Reversal 🔄
- **Situation:** Raid → reversal back toward the opposite side of the range.
- **What the algorithm does:** Collects liquidity (raid), reverses, and delivers price toward the opposite quadrant.
- **Detection:** Sweep of swing high/low → **relative equal levels** on the opposite side → bias:
  - Equal **highs** formed first → **long** bias (toward equal highs)
  - Equal **lows** formed first → **short** bias (toward equal lows)
- **Entry Model 1:** At **25DRT** (long) / **75DRT** (short) after **closure** (candle closes above/below the level).
  - Target: opposite side of the range = **3R**
  - SL: behind the sweep extreme + buffer (0.5 × ATR)
- **Entry Model 2:** At **50DRT** after **displacement** (body > 1.5 × ATR).
  - Target: **2R** (tighter stop)
  - SL: closer (behind the 50DRT reaction)

### Type 3 — Consolidation 📦
- **Situation:** Range compression — price rotates internally between the quadrants without raiding either side.
- **What the algorithm does:** Builds liquidity, waits for a trigger.
- **Rule:** **Avoid trades** in a Type 3 environment — it wastes trades and lowers win rate.
- **Detection:** Low ATR relative to the range; price between 25-75 without a raid on either side; low equal highs/lows without a sweep.
- **If trading:** Only on **breakouts** with displacement + retest (breakout model).

## SMT — Smart Money Technique (confirmation) 🤝
- **Divergence** between correlated instruments confirms reversal:
  - **EUR/USD ↔ GBP/USD** — when EU makes a new low but GU does not = bullish SMT → confirms long.
  - **DXY ↔ indices/gold** — DXY weakness = risk-on.
- Use SMT as a **filter**: if SMT contradicts the DRT signal → skip the trade.

## News filter ⛔
- Avoid trades **15 min before/after high-impact events**: FOMC, NFP, CPI, PCE, interest rates.
- Red folder news = flat or out.

## Execution windows (CET/Danish time)
- Intraday/scalp: only in killzones (London 09-11, NY AM 14:30-17:00, SB PM 19:30-21:00, ⛔ 15:30-16:00).
- Swing: entry can happen at any time.
- Max 3 trades/day, SL always, journal in TradeVault.

## Checklist — BEFORE trade
1. ✅ Is there an established dealing range (DRH/DRL defined after a raid)?
2. ✅ **Range ≥ 5×ATR?** (backtested: ≥5×ATR = 89.7% WR, ≥7×ATR = 92%)
3. ✅ **Is it NY session (15:00-20:00 CET)?** (backtested: 15-20 = 80.8% WR)
4. ✅ Which type: Type 1 (continuation) / Type 2 (reversal) / Type 3 (avoid)?
5. ✅ Is price in discount (25DRT) for longs / premium (75DRT) for shorts?
6. ✅ Entry model: 25/75DRT closure (3R) or 50DRT displacement (2R)?
7. ✅ SMT confirmation (EU/GU/DXY)?
8. ✅ No high-impact news in the window?
9. ✅ R:R at least 2:1 — otherwise skip.

## Final filters (backtested 31/7, 1h DRT, 2 years, 2,531 trades)
- **Only ranges ≥ 5×ATR** → 89.7% WR (+NY hours → 92.5%)
- **Only NY hours 15:00-20:00 CET** → 80.8% WR
- **≥6×ATR + NY** → 93.8% WR (144 trades)
- **≥5×ATR + NY** → 92.5% WR (226 trades = ~2-3/week) ⭐ RECOMMENDED

## Backtest references (1h DRT, 2 years)
- Baseline: 2,531 trades, 71.8% WR, +4741R
- ≥5×ATR: 474 trades, 89.7% WR, +1226R
- ≥5×ATR + NY hours: 226 trades, **92.5% WR**, +610R
- Primary instruments: GBP/USD (71.8%), XAU/USD (72.6%), US30 (70.3%), XAG/USD (70.4%)
- Scripts: `tradevault/scripts/backtest_drt.py`, `backtest_drt_v2.py`, `backtest_combo.py`
