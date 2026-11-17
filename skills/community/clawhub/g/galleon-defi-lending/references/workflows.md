# Lending workflows and evaluation cases

## Comparative research

For each candidate record `chain_id`, deployment/version, market ID, loan/collateral addresses and decimals, indexed observation time and fresh block, rate type and observation window, fees/rewards, caps, oracle unit, liquidity source, borrow limits, liquidation conditions and governance/access constraints. Discover official builders before choosing transaction code. An empty API result is not a zero balance unless the correct account, chain, pagination and coverage are established.

Use the same asset denomination and holding horizon for cost comparison. Keep realized APY, spot borrow APR, fixed-term quote and incentive estimate separate. Show reward-free cost first and scenario assumptions separately. For each debt position, assess collateral drawdown, debt appreciation, accrued interest and correlated-asset depeg. A health factor is a protocol-specific summary; do not compare two protocols without their actual liquidation definitions.

## Prepare and reconcile

A plan records operation, account/subaccount, chain, target, input/output tokens, exact or maximum amount semantics, recipient, spender/permit, expiry, pre/post debt and collateral, rate/cost assumptions, loss/slippage limits and simulation block. For a multi-leg refinance, each approval/flash-loan/swap/repay/withdraw step must be visible; an external quote cannot prove all legs remain possible.

Obtain missing authorization for this concrete plan before signatures or value movement. Preserve standing authorization only within its amounts, assets, protocols and time limits. An approval signature is a financial permission even when no token moves immediately. Inspect the chosen signer configuration without exporting secrets.

After broadcast, track the known transaction hash and nonce. Confirm receipt success, expected events and fresh debt/supply balances. Handle approval-only success, cancelled/replaced transactions, partial multi-transaction completion and indexer lag explicitly. On ambiguous delivery, query rather than blindly resubmitting. If a fixed-term loan expires or a refinance quote lapses, re-evaluate the terms instead of reusing a stale plan.

## Monitoring

Save the user's chosen markets/account and thresholds, not credentials. A meaningful alert gives observation time, changed debt/health/liquidity/rate/collateral parameter, its implication and a scoped proposed action. A monitoring request does not authorize an automatic repayment, new loan or asset sale. Do not assume an alert arrived or a transaction succeeded from a scheduler's status alone.

## Offline evaluation scenarios

These cases exercise expected reasoning; they are not claims of live protocol execution tests.

| Scenario | Required outcome |
| --- | --- |
| Compound III user supplies WBTC and asks why interest is zero | Explain collateral versus base supply; do not claim WBTC accrues the base supply rate |
| Compound III account has positive base balance and requests a larger `withdraw` | Show that the excess creates debt, check collateral and minimum borrow, and seek missing borrow authority |
| Morpho query succeeds on a REST-only chain; prepare fails | Check supported-chain RPC flag; do not invent a slug or claim execution support |
| Morpho preparation includes an approval plus an error warning | Stop presentation for signing; do not strip warnings or add a duplicate approval |
| Midnight fixed-term quote compared to Blue 24-hour average | Identify different products/time bases; include expiry, refinancing and fresh quote requirements |
| Aave V4 input contains a Pool address copied from V3 | Resolve correct V4 spoke/reserve deployment before preparing; do not reuse V3 calldata |
| Euler liquidation appears profitable but receiver lacks a controller | Explain receiving-account health/controller requirements and simulate the full EVC outcome |
| API reports health 1.03 from an old block; new oracle data unavailable | Mark risk unverified and defer execution planning rather than presenting the old number as safe |
| Approval confirmed, borrow transaction timed out, indexer shows no debt | Inspect borrow hash/nonce and chain receipt before retry; report partial/unknown state |
| Spark frontend shows a Morpho isolated market | Use the Morpho market identity and mechanics, not SparkLend Pool assumptions |
