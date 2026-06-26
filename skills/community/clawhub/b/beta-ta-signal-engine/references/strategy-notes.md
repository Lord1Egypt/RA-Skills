# Strategy Notes

- `trend`: best in persistent directional markets; avoid chop.
- `mean-reversion`: best in range-bound markets; avoid strong trends.
- `breakout`: best when volatility expands after consolidation.

Risk defaults used by script:
- Stop distance: `1.5 * ATR(14)`
- Target distance: `3.0 * ATR(14)`
- Position size: fixed-fractional (`account_size * risk_per_trade / stop_distance`)
