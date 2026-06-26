# Cross-Project Wisdom

Total: **8**

## `CW-CRYPTO-TRADING-001` — Decimal Type for All Monetary Values
**From**: rotki, hummingbot, cryptofeed, ccxt · **Applicable to**: crypto-trading

All four projects mandate Decimal type for price, amount, balance, quantity, and PnL fields. Float arithmetic causes rounding errors that compound across financial calculations, leading to incorrect order sizing and reporting. Always use Decimal for any value representing money in crypto trading systems.

## `CW-CRYPTO-TRADING-002` — Initialize Data Structures Before Access
**From**: ccxt, cryptofeed, rotki · **Applicable to**: crypto-trading

Projects consistently require explicit initialization before data access: load_markets() before symbol lookups, check symbol population before mapping access, establish RPC connections before queries. Skipping initialization causes KeyError, AttributeError, or silent data corruption that breaks downstream operations.

## `CW-CRYPTO-TRADING-003` — Precise String Arithmetic for Financial Calculations
**From**: ccxt · **Applicable to**: crypto-trading

CCXT mandates Precise.string_* static methods (string_mul, string_div, string_add, string_sub) for monetary calculations to avoid floating-point precision errors. This is especially critical for high-precision exchange data where rounding errors cause incorrect order costs, fees, and balances that may result in financial loss.

## `CW-CRYPTO-TRADING-004` — Respect Exchange Rate Limits
**From**: ccxt · **Applicable to**: crypto-trading

Disabling rate limiting via enableRateLimit=False causes HTTP 429 responses and potential temporary or permanent API key suspension by exchanges. CCXT enforces rate limits per IP/API key pair, and bypassing throttle() gates results in compliance violations that disrupt all trading activity until exchanges lift bans.

## `CW-CRYPTO-TRADING-005` — Inverse Contract Price Adjustment
**From**: ccxt, hummingbot · **Applicable to**: crypto-trading

Perpetual swap cost calculations require applying inverse price adjustment (1/price) before multiplying by contractSize for inverse contracts. Incorrect cost calculation causes wrong position sizing, leading to unexpected liquidation or insufficient margin for perpetual trading positions.

## `CW-CRYPTO-TRADING-006` — Strict Connection Lifecycle Ordering
**From**: cryptofeed, ccxt · **Applicable to**: crypto-trading

Both projects enforce strict execution order for connection operations: cryptofeed requires authenticate -> subscribe -> message handler sequence, while ccxt mandates connect -> on_connected_callback -> subscriptions -> on_close_callback. Out-of-order operations cause subscription failures and no data flow through connections.

## `CW-CRYPTO-TRADING-007` — Validate Input Data Structure Before Processing
**From**: rotki, cryptofeed · **Applicable to**: crypto-trading

Rotki validates EVM address checksum format before RPC calls; cryptofeed checks Symbols.populated() before symbol mapping access. Validating data structure before processing prevents downstream crashes (KeyError, InvalidAddress) and data corruption that is harder to debug when symptoms appear in unrelated code paths.

## `CW-CRYPTO-TRADING-008` — Validate Order Sizes Against Exchange Minimums
**From**: hummingbot · **Applicable to**: crypto-trading

DCAExecutor amounts must be validated against min_notional_size and amounts_quote/prices against min_order_size before execution. Orders below exchange minimums are rejected, breaking strategy execution and potentially leaving positions partially unfilled at unfavorable prices.
