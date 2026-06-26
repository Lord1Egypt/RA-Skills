# Setup checklist

## Inputs to collect

- RapidAPI key
- dYdX address
- dYdX mnemonic path
- dYdX subaccount (default 0)
- max leverage
- order margin in USD
- max open positions
- close-after-hours
- Telegram bot token and chat IDs (comma-separated)

## Runtime behavior

- Retry order create up to 3 attempts total.
- Place TP/SL as reduce-only conditional orders after open.
- Validate TP/SL exists in active orders; retry once if chain accepted but indexer delayed.
- On position close, cancel only matching signal-bound reduce-only orders.

## Notification templates

### Open

NEW SIGNAL!
{MARKET} {Side}
Entry: {entry}
TakeProfit: {tp}
StopLoss: {sl}

### Close

POSITION CLOSED
{MARKET} ({reason})
PnL: {pnl}
