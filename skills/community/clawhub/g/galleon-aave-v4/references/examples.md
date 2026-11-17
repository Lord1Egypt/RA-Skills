# V4 worked records

Synthetic observations only; no API access or financial actions are implied.

## Exact amount and reserve

Request: prepare a borrow of 0.1 USDC in an observed V4 position. Current tool discovery returns opaque reserve R; the token has 6 decimals. MCP amount is `"0.1"`; a raw contract input would be `100000`. Calling MCP with `"100000"` would request 100,000 USDC, so reject a unit mismatch before preparation. Keep R exactly as returned; a different reserve for the same ticker can belong to another Spoke.

Read account/position/reserve, then preview unchanged parameters. If an error warning reports no collateral borrowing power, return the prerequisite. Do not silently enable collateral or choose another position. A warning-only successful preview reaches the user with the unsigned plan and post-action health factor.

## Approval/indexing delay

Approval receipt is successful, but indexer still reports pending and provider emits an approval branch again. Read actual allowance and preserve the approval hash. Wait/retry current read within bounds rather than submitting approval repeatedly. If the action has a V4 operations-aware processed check, carry its original `operations`; do not invent them from a hash.

After a borrow, compare actual principal/balance and health with preview. A successful transaction receipt with unindexed activity is chain-confirmed/index-pending. Indexing alone with no receipt is a separate weaker observation.

## Repay then withdraw

Displayed debt is rounded to four USD decimals, while fresh position items show nonzero accrued interest. Exact old principal cannot prove full repayment. Use documented current full-debt preparation within the user's approved maximum, then reconcile receipt and position. Withdraw only after reading the resulting collateral constraint. Liquidity-only `withdrawableIgnoringDebt` is not an authorized healthy maximum.
