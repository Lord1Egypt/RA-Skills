# Review Workflow

Use this reference when the user wants to track whether past calls were useful.

## Snapshot logging

After a meaningful analysis, save a snapshot with:
- symbol
- action
- price at time of call
- confidence
- short thesis
- planned entries, stop, and targets when available

## Review logic

Later, compare the logged price with current price.

### For BUY or SCALE IN calls
- Positive if price is now above the logged price
- Negative if price is now below the logged price

### For REDUCE, SELL, or EXIT calls
- Positive if price is now below the logged price
- Negative if price is now above the logged price

## Important note

This is a simple review loop, not a full backtest engine.
Use it to spot patterns in decision quality and improve future rules.
