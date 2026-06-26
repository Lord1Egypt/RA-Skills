# Built-in Trading Strategies

## DCA (Dollar-Cost Averaging)
**Risk Level:** Low
**Description:** Buy a fixed dollar amount at regular intervals regardless of price. Reduces impact of volatility.

### Parameters
- `amount`: USD amount per buy (default: $100)
- `interval_hours`: Time between buys (default: 24)
- `pair`: Trading pair (default: BTC/USDT)

### When to Use
- Long-term accumulation (weeks to months)
- High-conviction assets (BTC, ETH)
- When you can't/don't want to time the market

### Risk Profile
- Max drawdown: Market-dependent (no stop-loss — accumulation strategy)
- Best for: Bear markets, range-bound markets
- Worst for: Sharp crashes (still buys on the way down)

---

## Momentum (Trend Following)
**Risk Level:** Medium
**Description:** Uses SMA crossover + RSI to identify trends. Buys when short-term momentum exceeds long-term, sells when overbought or trend reverses.

### Indicators
- SMA(20) vs SMA(50) crossover
- RSI(14) overbought/oversold filter

### Signals
- **BUY:** SMA20 > SMA50 AND RSI < 70
- **SELL:** SMA20 < SMA50 OR RSI > 80
- **HOLD:** No clear signal

### When to Use
- Trending markets (strong up or down moves)
- Medium timeframes (4h to daily candles)
- Assets with clear trend patterns

### Risk Profile
- Stop-loss: 5% below entry (configurable)
- Win rate: Typically 40-50% (profits come from big winners)
- Best for: Trending markets
- Worst for: Choppy/sideways markets (many false signals)

---

## Mean Reversion (RSI-Based)
**Risk Level:** High
**Description:** Buys when RSI indicates oversold, sells when overbought. Assumes prices revert to mean.

### Indicators
- RSI(14)

### Signals
- **BUY:** RSI < 30 (oversold)
- **SELL:** RSI > 70 (overbought)
- **HOLD:** RSI between 30-70

### When to Use
- Range-bound markets
- High-liquidity pairs
- Short timeframes (1h to 4h)

### Risk Profile
- Stop-loss: 3% below entry (tight)
- Win rate: 55-65% (small, frequent profits)
- Best for: Sideways/range-bound markets
- Worst for: Strong trends (catches falling knives)

---

## Grid Trading
**Risk Level:** Medium
**Description:** Places buy and sell orders at regular price intervals within a range. Profits from price oscillation.

### Parameters
- `lower_price`: Bottom of grid range
- `upper_price`: Top of grid range
- `grid_count`: Number of grid levels (default: 10)
- `amount_per_grid`: USD per grid order

### When to Use
- Sideways markets with clear support/resistance
- High-volume pairs with tight spreads
- When you expect oscillation within a range

### Risk Profile
- Max loss: Price breaks below grid (all buys filled, no sells)
- Best for: Ranging markets
- Worst for: Breakout moves

---

## Funding Rate Arbitrage
**Risk Level:** Medium
**Description:** Exploits funding rate differences between perpetual futures and spot. When funding is negative, long perp + short spot. When positive, short perp + long spot.

### When to Use
- When funding rates are significantly positive or negative (>0.05%)
- Pairs with good futures liquidity
- Requires futures account

### Risk Profile
- Market-neutral (hedged position)
- Risk comes from funding rate changing direction
- Best for: High-funding periods
- Worst for: Sudden funding rate reversals
