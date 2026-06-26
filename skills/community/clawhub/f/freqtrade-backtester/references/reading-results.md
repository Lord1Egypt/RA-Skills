# Reading Backtest Results

When your backtest completes, you'll see a summary table and a JSON file. Here's what to look for.

## Console Output

The summary table shows:

| Metric | What It Means | Good Threshold |
|--------|---------------|-----------------|
| Total trades | Number of trades executed | More data = more confidence, but avoid tiny sample sizes (<20 trades) |
| Avg profit | Average return per trade (%) | Positive = good. Compare wins/losses, not just the average. |
| Total profit | Total % return over the period | Depends on your risk tolerance; compare across strategies |
| Win rate | % of winning trades | >55% is decent. Watch for inflated rates on short timeframes. |
| Max drawdown | Biggest peak-to-trough loss (%) | <20% is acceptable; >25% indicates excessive risk |
| Sharpe ratio | Risk-adjusted return | >1.0 = good; >2.0 = excellent |
| Sortino ratio | Return vs downside risk | Similar to Sharpe but ignores upside volatility |
| Profit factor | Gross profit / Gross loss | >1.5 is solid |

## JSON Export Deep Dive

The exported `my_backtest.json` contains detailed trade logs. Key fields per trade:

- **profit_ratio** — Gain/loss as a decimal (0.05 = 5% gain, -0.03 = 3% loss)
- **exit_reason** — Why it closed (roi, stop_loss, sell_signal, trailing_stop, etc.)
- **trade_duration** — How long the trade lasted
- **close_date** — When it exited

## Red Flags

1. **High win rate, low profit factor** — You're winning often but losses are huge. Tighten stops.
2. **Exit reason: >30% stop-loss** — Too many losses hit the stop. Either the stop is too tight for your market, or your entry signal is weak.
3. **Profit clusters** — If 90% of profit comes from a few lucky trades, the strategy isn't robust. Look for consistent, repeatable wins.
4. **Max drawdown rising over time** — The strategy broke in later periods. It may have been overfit to earlier data.

## Comparing Two Backtests

When you change a parameter and re-run:

1. **Same timeframe?** Always test the same period to isolate the parameter change.
2. **Trade count stable?** If one version has 5 trades and another has 50, the smaller sample is less reliable.
3. **Metrics improvement?** Win rate alone doesn't count. Look at profit factor, max drawdown, and average loss size.
4. **Sharpe ratio trend** — Higher is better, but compare across your recent backtests, not absolute values.

## Example Decision Tree

- Strategy A: 55% win rate, 1.2 profit factor, -18% max drawdown
- Strategy B: 45% win rate, 1.8 profit factor, -12% max drawdown

**Choose B.** Lower win rate, but bigger wins, smaller losses, and you survive drawdowns better. Strategy B is more resilient.
