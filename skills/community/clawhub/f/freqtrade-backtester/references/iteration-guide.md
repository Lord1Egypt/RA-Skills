# Iteration Guide: Improving Your Strategy

This guide walks you through a repeatable cycle for refining your strategy without overfitting.

## The Core Loop

### 1. Establish a Baseline

Run your strategy on a fixed, representative period (e.g., 6 months of data):

```bash
docker-compose run --rm freqtrade backtesting \
  --strategy MyStrategy \
  --timerange 20240101-20240630 \
  --export trades \
  --export-filename user_data/backtest_results/baseline.json
```

Record the metrics:
- Win rate
- Profit factor
- Max drawdown
- Average profit per trade
- Exit reason distribution

This is your **baseline**. All future changes are measured against it.

### 2. Change One Thing

Pick a single parameter:
- RSI threshold (e.g., 30 → 25)
- Stop-loss percentage (e.g., -5% → -3%)
- Trailing stop activation (e.g., 0.05 → 0.03)
- Timeframe (e.g., 5m → 15m)

Edit your strategy file, then backtest **the same period**:

```bash
docker-compose run --rm freqtrade backtesting \
  --strategy MyStrategy \
  --timerange 20240101-20240630 \
  --export trades \
  --export-filename user_data/backtest_results/iteration_1.json
```

### 3. Compare Results

Use the same period and same strategy class to isolate the parameter change. Compare:

| Metric | Baseline | Iteration 1 | Better? |
|--------|----------|------------|---------|
| Win rate | 55% | 58% | ✓ |
| Max drawdown | -18% | -22% | ✗ |
| Profit factor | 1.2 | 1.15 | ✗ |
| Avg profit | 0.8% | 0.7% | ✗ |

In this example, higher win rate came at a cost: bigger drawdowns and lower profits. **Revert the change.**

### 4. Keep It or Revert

- **Better on all/most metrics?** Keep it, move to step 5.
- **Trade-off (some better, some worse)?** Decide based on your risk tolerance. If max drawdown is your hard limit, revert.
- **Worse overall?** Revert and try a different parameter.

### 5. Test Multiple Market Conditions

Once you have an improved version, backtest across different market regimes to ensure robustness:

**Bull market (strong uptrend):**
```bash
docker-compose run --rm freqtrade backtesting \
  --strategy MyStrategy \
  --timerange 20230101-20230630 \
  --export trades \
  --export-filename user_data/backtest_results/bull_market.json
```

**Bear market (downtrend or stagnation):**
```bash
docker-compose run --rm freqtrade backtesting \
  --strategy MyStrategy \
  --timerange 20220101-20220630 \
  --export trades \
  --export-filename user_data/backtest_results/bear_market.json
```

**Sideways market (low volatility, choppy):**
```bash
docker-compose run --rm freqtrade backtesting \
  --strategy MyStrategy \
  --timerange 20210101-20210630 \
  --export trades \
  --export-filename user_data/backtest_results/sideways_market.json
```

If your strategy crashes in bear or sideways markets, it's not ready. Go back to the drawing board.

## Avoiding Overfitting

**Overfitting = optimizing so hard to one dataset that your strategy fails in real trading.**

Red flags:
- You've done 50+ iterations on the same timeframe.
- Your metrics improved 10% or more after heavy tuning.
- The strategy performs great on 2023 data but terrible on 2024 data.
- You tweaked so many parameters that you can't remember the logic anymore.

**Prevention:**
- Use a fixed, 6-month baseline. Don't jump between periods.
- Change one parameter at a time.
- Always test on 3+ different market conditions before declaring victory.
- Keep the strategy logic simple. Complex rules = overfitting risk.

## When to Go Live

Your strategy is **candidate-ready** when:

1. ✓ Baseline win rate >50% (preferably >55%)
2. ✓ Profit factor >1.2
3. ✓ Max drawdown <25% (ideally <20%)
4. ✓ Consistent performance across bull, bear, and sideways markets
5. ✓ Exit reasons make sense (if >30% of exits are stop-loss, reconsider entry or stop sizing)
6. ✓ You understand why each rule exists (no "magic" parameters)

Even then, **start with small position sizes.** Backtests are historical. Real markets surprise you.

## Checklist

- [ ] Baseline established on fixed 6-month period
- [ ] Metrics recorded (win rate, drawdown, profit factor, avg profit)
- [ ] First parameter change tested on same period
- [ ] Compared baseline vs iteration 1
- [ ] Decision made (keep or revert)
- [ ] Multi-market testing done (bull, bear, sideways)
- [ ] Profit factor check (>1.2?)
- [ ] Max drawdown within tolerance (<25%?)
- [ ] Exit reason distribution reviewed
- [ ] Strategy logic documented
- [ ] Ready for small-size live test
