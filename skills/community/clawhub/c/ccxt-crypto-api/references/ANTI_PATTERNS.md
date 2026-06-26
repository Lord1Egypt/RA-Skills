# Anti-Patterns (Cross-Project)

Total: **13**

## ccxt (1)

### `AP-CRYPTO-TRADING-002` — Missing Market Initialization Before Access <sub>(high)</sub>

Attempting to access market data via symbol lookups before load_markets() is called leaves self.markets empty, causing KeyError or BadSymbol exceptions on all trading operations and data retrieval. This breaks the entire trading workflow at the first market interaction.

## cryptofeed (3)

### `AP-CRYPTO-TRADING-009` — Applying Order Book Deltas Before Snapshot <sub>(high)</sub>

Processing order book delta messages before receiving a snapshot for the symbol applies updates to an uninitialized or stale book state. Price levels are incorrectly added/removed, corrupting the local book representation with no way to recover without full reset.

### `AP-CRYPTO-TRADING-010` — Silent HTTP Error Handling <sub>(medium)</sub>

Ignoring non-200 HTTP response status codes without raising exceptions causes silent failures for data requests. Market data is missing or corrupted, failed requests are not retried, and downstream consumers receive incomplete data with no indication of failure.

### `AP-CRYPTO-TRADING-011` — Missing Sequence Number Validation <sub>(medium)</sub>

Not validating that order book sequence numbers increment by exactly 1 allows out-of-order or missing messages to corrupt local book state. Stale or incorrect price levels persist in the book, leading to wrong trading signals and corrupted market depth data.

## hummingbot (5)

### `AP-CRYPTO-TRADING-005` — Unvalidated Collateral for Order Execution <sub>(high)</sub>

Submitting orders without checking collateral requirements including order cost, percent fees, and fixed fees against available balance causes orders to exceed margin. This triggers immediate liquidation or forced position closure at unfavorable prices with partial or total loss of collateral.

### `AP-CRYPTO-TRADING-006` — Close Order Placed Before Open Order Fills <sub>(high)</sub>

Placing a close order before verifying the open order is fully filled causes mismatched position sizes. The executor attempts to close a larger or smaller position than actually exists, leading to unintended directional exposure and potential losses exceeding the configured risk parameters.

### `AP-CRYPTO-TRADING-007` — Arbitrage Across Non-Interchangeable Tokens <sub>(high)</sub>

Executing arbitrage trades between tokens that appear similar but are not interchangeable causes permanent loss of funds. The received tokens cannot be used to close the opposing position, stranding capital and creating one-sided exposure with no recovery path.

### `AP-CRYPTO-TRADING-008` — Skipping Triple Barrier Evaluations <sub>(high)</sub>

Omitting control_stop_loss, control_take_profit, or control_time_limit calls in the control_barriers cycle leaves positions unprotected. Losses exceed configured thresholds as barrier checks never trigger, positions remain open beyond risk tolerance, resulting in amplified losses.

### `AP-CRYPTO-TRADING-012` — Wrong Position Key for Perpetual Modes <sub>(medium)</sub>

Using trading_pair only as the position key in HEDGE mode causes different position sides to collide and overwrite each other. Position tracking becomes incorrect, leading to wrong order matching and potential financial loss when the system misidentifies position direction.

## rotki (3)

### `AP-CRYPTO-TRADING-003` — Bypassing API Facade Layer <sub>(high)</sub>

Directly accessing internal service methods without routing through the RestAPI facade bypasses authentication, task tracking, and error handling mechanisms. Anonymous requests can execute privileged operations, creating critical security vulnerabilities where unauthorized users access sensitive financial data or execute trades.

### `AP-CRYPTO-TRADING-004` — Non-Checksummed EVM Addresses <sub>(high)</sub>

Passing lowercase or mixed-case Ethereum addresses to RPC nodes causes InvalidAddress exceptions since nodes enforce EIP-55 checksum format. This results in RemoteError failures that halt all blockchain data collection for the affected chain, with no graceful degradation or fallback.

### `AP-CRYPTO-TRADING-013` — Overwriting User-Customized Event Classifications <sub>(medium)</sub>

Re-decoding operations silently replace user-modified events marked as CUSTOMIZED without explicit user action. User edits to event classifications are permanently lost, causing incorrect accounting treatment and potential tax reporting errors that may not be detected until audit.

## rotki, hummingbot, cryptofeed, ccxt (1)

### `AP-CRYPTO-TRADING-001` — Float Arithmetic for Monetary Values <sub>(high)</sub>

Using Python float type instead of Decimal for price, amount, balance, PnL, and other financial calculations causes precision errors due to binary floating-point representation. Rounding errors compound across multiple calculations, leading to incorrect order sizing, wrong profit/loss reporting, and potentially incorrect trading decisions or tax calculations.
