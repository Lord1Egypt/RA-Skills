# Review evidence

Collect the raw record before calculating performance.

## Required

- immutable ticket revision and action digest
- risk sign-off and the user's exact approval by ticket ID
- request send time, client order IDs, exchange order IDs, and response class
- `orderStatus` and `historicalOrders` for each order
- detailed open orders across the review window where retained
- `userFillsByTime`, paginated and deduplicated by trade ID
- `userFunding` for the holding window
- position and balance state before, during, and after
- non-funding ledger changes that affect account value
- account mode, DEX, market identity, and effective fee schedule

Optional depth snapshots support slippage analysis. A screenshot or chat claim cannot replace missing exchange evidence.

## Reconstruction

Order fills chronologically. Use `startPosition`, direction, side, size, price, fee, maker or taker status, and client order ID to reconstruct position transitions. Separate entries, adds, reductions, reversals, and exits.

Funding is already signed from the account's perspective. Sum it once. Keep fee tokens explicit and convert only with a dated price source when needed.

Portfolio history is sampled. Use it for broad account context, not exact per-trade accounting.

## Gaps

State the bounded API windows and any missing interval. If historical detailed order state cannot prove continuous protection, grade protection as unknown for that interval rather than present.

Fill and funding reads return one bounded page per request across a limited window; a busy account can have later activity omitted, so they are not a complete ledger and cannot support a claim of total historical PnL. Portfolio history is sampled provider history, not cash-flow-adjusted accounting. A leaderboard or profile PnL is a provider claim until fills reconstruct it.
