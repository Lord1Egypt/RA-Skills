# ETF Day-Trading Strategies (做T策略)

## Grid Trading (网格交易)

### Principle
Divide price range into N grids. Buy one unit when price drops to a grid line, sell when it rises to the next.

### Parameters
- `grid_num`: Number of grids (default 10)
- `grid_range`: (low, high) price range — auto-detected from 30-day range if not set
- `position_per_grid`: Capital allocated per grid buy (capital / grid_num)

### Entry/Exit Rules
```
Buy:  price <= current_grid_price AND no position at this grid
Sell: price >= next_upper_grid AND has position from lower grid
```

### Best For
- Sideways markets (震荡市)
- ETFs with moderate volatility (日波动 1-3%)
- Avoid in strong trends

### Optimization
- Reduce grid_num in high-volatility periods
- Use ATR to set dynamic grid spacing
- Add time filter: no new positions after 14:30 (close to market close)

---

## MA Crossover (均线交叉)

### Principle
Buy when short MA crosses above long MA (golden cross), sell on death cross.

### Parameters
- `ma_short`: Short moving average period (default 5)
- `ma_long`: Long moving average period (default 20)
- MA type: SMA or EMA

### Entry/Exit Rules
```
Buy:  MA_short[t] > MA_long[t] AND MA_short[t-1] <= MA_long[t-1]
Sell: MA_short[t] < MA_long[t] AND MA_short[t-1] >= MA_long[t-1]
```

### Best For
- Trending markets (趋势市)
- Works better on daily timeframe for swing trades
- Use 5/20 for intraday, 10/30 for swing

### Optimization
- Add volume confirmation: buy signal requires volume > 20-day avg
- Add RSI filter: avoid buy when RSI > 70 (overbought)

---

## Bollinger Band Mean Reversion (布林带回归)

### Principle
Price tends to revert to mean. Buy near lower band, sell near upper band.

### Parameters
- `period`: Bollinger band period (default 20)
- `std_dev`: Standard deviations (default 2)

### Entry/Exit Rules
```
Buy:  price <= lower_band AND RSI < 30
Sell: price >= upper_band OR RSI > 70
Stop: price < lower_band * 0.97
```

### Best For
- Mean-reverting markets
- ETFs with stable historical range
- Avoid in breakout scenarios

### Optimization
- Use %B (percent B) for finer entry timing
- Combine with volume spike at lower band for higher probability

---

## Volatility Breakout (波动率突破)

### Principle
Enter when price breaks out of recent range with expanding volatility.

### Parameters
- `atr_period`: ATR calculation period (default 14)
- `atr_multiplier`: Breakout threshold (default 1.5)
- `lookback`: Range calculation window (default 20)

### Entry/Exit Rules
```
Breakout Up:   close > high[lookback] AND ATR > ATR_avg * atr_multiplier → Buy
Breakout Down: close < low[lookback] AND ATR > ATR_avg * atr_multiplier → Sell (short)
Exit:          ATR contracts below ATR_avg, or fixed time exit (2 days)
```

### Best For
- Markets entering new trends
- Earnings releases, policy announcements
- Use sparingly — 20-30% of trades max

---

## Strategy Selection Guide

| Market Condition | Primary Strategy | Secondary |
|-----------------|-----------------|-----------|
| 震荡 (ADX < 20) | Grid | Bollinger |
| 上升趋势 (ADX > 25, +DI > -DI) | MA Crossover | Volatility Breakout |
| 下降趋势 (ADX > 25, -DI > +DI) | Bollinger (rebound) | Cash |
| 高波动 (ATR > 2x avg) | Grid (wider) | Volatility Breakout |
| 低波动 (ATR < 0.5x avg) | MA Crossover | Skip |

## Position Sizing

```python
def position_size(capital, risk_pct, entry_price, stop_price):
    """Kelly-lite position sizing"""
    risk_amount = capital * risk_pct
    price_risk = abs(entry_price - stop_price) / entry_price
    if price_risk == 0:
        return 0
    shares = int(risk_amount / (entry_price * price_risk) / 100) * 100
    return shares
```
