# Strategy Iteration Workflow

Step-by-step process for developing, testing, and optimizing a profitable Freqtrade strategy.

## Phase 1: Baseline Strategy

### Step 1: Define Core Logic

Write a simple, testable strategy with:
- One clear entry condition (e.g., RSI < 30)
- One clear exit condition (e.g., RSI > 70, or ROI target)
- Tight stop-loss (3%)
- Basic position sizing

**Example:**
```python
# Entry: RSI oversold
# Exit: 4% profit target or 3% stop loss
# No filters yet; just raw signal
```

### Step 2: Set Conservative Parameters

- `stoploss = -0.03` (3%)
- `minimal_roi = {"0": 0.04}` (4% immediate target)
- `timeframe = "5m"` (shorter candles = faster feedback)
- `dry_run = True` (always)

### Step 3: Backtest 90–120 Days

```bash
freqtrade backtesting \
  --strategy MyStrategy \
  --datadir user_data/data \
  --timerange 20240101-20240331
```

**Capture these metrics:**
- Total trades
- Win rate
- Avg win / Avg loss ratio
- Sharpe ratio
- Max drawdown
- Profit %

---

## Phase 2: Analysis & Diagnosis

### Step 4: Review Exit Reasons

After backtest, analyze:

**Q: Are you exiting winners too early?**
- Increase minimal_roi targets
- Add trailing_stop to let winners run

**Q: Are you exiting losers too late?**
- Tighten stop-loss (but not below 2%)
- Add early exit condition for weak signals

**Q: Are you taking too many losing trades?**
- Add entry filters (volume, momentum, trend)
- Require multiple indicators to align

**Q: Are you trading in choppy, sideways markets?**
- Filter by trend (price above EMA)
- Require strong momentum (CCI < -100)

---

## Phase 3: Selective Iteration

### Step 5: Tighten ONE Parameter

Pick the single biggest issue from Step 4. Change ONLY that parameter.

**Example iteration path:**

**Version 1 (baseline):**
- RSI < 30 entry
- Result: 150 trades, 52% win rate, losing

**Version 2 (add RSI > 70 exit):**
- RSI < 30 entry, RSI > 70 exit
- Result: 145 trades, 55% win rate, still losing

**Version 3 (add volume filter):**
- RSI < 30 entry, volume > 20-period SMA
- Result: 65 trades, 60% win rate, +2.3% profit ✓

**Version 4 (add CCI confirmation):**
- RSI < 30 AND CCI < -100, volume > SMA
- Result: 42 trades, 64% win rate, +3.8% profit ✓

**Version 5 (tighten stop-loss):**
- Same entry logic
- Stop-loss 2% instead of 3%
- Result: 42 trades, 65% win rate, +4.1% profit ✓

### Step 6: Backtest Same Period, Compare

Run backtest on identical date range. Compare to baseline:

```text
Metric              | v1 Baseline | v3 (Volume) | v4 (CCI) | v5 (2% SL)
Total Trades        | 150         | 65          | 42       | 42
Win Rate            | 52%         | 60%         | 64%      | 65%
Avg Win / Loss      | 1.1x        | 1.4x        | 1.8x     | 1.9x
Total Profit        | -0.8%       | +2.3%       | +3.8%    | +4.1%
Max Drawdown        | -12%        | -8%         | -6%      | -5%
```

**Decision rule:**
- If profit improves & max drawdown stays acceptable → **KEEP**
- If profit improves but drawdown explodes → **REVERT**
- If no improvement → **REVERT & try different approach**

---

## Phase 4: Multi-Market Testing

### Step 7: Test Different Market Conditions

After finding a baseline that works, backtest against:

1. **Bull market** (Jan–Jun 2021)
2. **Bear market** (Jun–Nov 2022)
3. **Sideways/choppy** (Aug–Oct 2023)

**Questions:**
- Does strategy adapt to different regimes?
- Does it lose too much in bear markets?
- Does it miss opportunities in bull markets?

If strategy fails in bear market, add trend filter or reduce position size.

---

## Phase 5: Live Deployment

### Step 8: Dry-Run on Live Data

Before live trading, run dry-run mode for 1–2 weeks:

```bash
freqtrade trade \
  --strategy MyStrategy \
  --dry-run \
  --datadir user_data/data
```

Monitor:
- Are entry signals firing as expected?
- Are exits happening correctly?
- Are there any crashes or errors?

### Step 9: Live Trade (Micro Positions)

Start with minimal stake per trade (e.g., 10 USDT). Monitor for:
- Real slippage vs. backtest expectations
- Exchange latency
- Actual entry/exit prices
- Account stability

Only increase position size after 50+ live trades with positive results.

---

## Version Control & Documentation

For each version, use a naming pattern:

```text
MyStrategy_v1.py  # Baseline
MyStrategy_v2.py  # Added volume filter
MyStrategy_v3.py  # Added CCI confirmation
MyStrategy_v4.py  # Tightened stop-loss
```

In each file, add header comments:

```python
"""
MyStrategy_v3 — CCI Confirmation
=================================
Changes from v2:
- Added CCI < -100 filter for momentum confirmation
- Reduced entry trades from 65 to 42
- Win rate improved 60% → 64%
- Profit improved +2.3% → +3.8%

Key settings:
- stoploss = -0.03
- minimal_roi = {"0": 0.04, "30": 0.02}
- Entry: RSI < 30 AND CCI < -100 AND volume > SMA
- Exit: ROI or stop-loss
"""
```

---

## Quick Troubleshooting

| Problem | Diagnosis | Fix |
|---------|-----------|-----|
| Too many trades, low win rate | Entry filter too loose | Add RSI + CCI + volume requirements |
| Few trades, high win rate | Might be luck or overfitted | Test different timeframes & markets |
| Good backtest, bad live results | Overfitting or slippage | Increase stop-loss by 0.5–1%, reduce position size |
| Strategy loses in bear market | No downside protection | Add stop-loss tightener or trend filter |
| Whipsaws on 5m timeframe | Noise | Switch to 15m or 1h candles |

---

## Final Checklist Before Live

- [ ] Backtested on 90+ days of data
- [ ] Tested on bull, bear, and sideways markets
- [ ] Dry-run on live feeds for 1–2 weeks
- [ ] Win rate ≥ 55% AND avg win ≥ avg loss
- [ ] Sharpe ratio > 1.0
- [ ] Max drawdown ≤ 10%
- [ ] Stop-loss ≤ 3%
- [ ] Position sizing allows 10+ concurrent trades
- [ ] Can explain every entry filter in plain English
- [ ] All strategy versions saved with comments
