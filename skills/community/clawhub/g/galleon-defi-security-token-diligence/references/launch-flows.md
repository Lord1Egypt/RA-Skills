# Launch allocations and asset flows

## Define the population before measuring it

Bind launch history to the exact factory/version and creation receipt. Decode the initial allocation, pool/curve initialization, exempt recipients and first purchases. A deterministic address or factory deployment is not evidence of common human ownership. Distinguish launcher, transaction sender, actual buyer/beneficiary, fee recipient and inferred controller.

Write the cohort rule before calculating its concentration: included events/addresses, start/end blocks, exclusions and missing pages. Separate current holders from launch recipients. Group custody addresses only when their beneficial ownership is supported; disclose pool, exchange, locker and treasury exclusions and the denominator used. Never equate total supply with freely tradable float.

[ERC-20](https://eips.ethereum.org/EIPS/eip-20) defines Transfer events and optional metadata, but extensions can change balances through rebases or other accounting. Use full event replay only for a historical question or a supply discrepancy that needs it; reconcile terminal balances with the token's actual accounting rules. A current holder list cannot establish the launch distribution.

## Trace quantities before inferring motives

Track opening inventory, acquisitions, transfers, confirmed sales, rebuys, retained inventory and proceeds for the defined cohort. A zero token balance can mean a transfer or custody change. Prove a sale from successful execution, decoded venue mechanics and asset deltas; a router transfer alone is insufficient. Shared funding or timing is an observation, not proof of coordination or identity. Cost basis and outstanding inventory are needed before calling proceeds profit.

For each asset, reconcile opening balance plus inflows and explained adjustments against outflows and closing balance; state any residual and its cause or bound. Treat wraps and bridge legs as transformations, not new income. Exclude reverted value transfers while accounting for gas actually spent. Stop exact beneficiary attribution when commingling prevents it. An exchange deposit does not prove a sale or fiat cash-out.

For fee-origin questions, connect collection receipts, decoded fee/principal components and forwarding transactions to the destination. Distinguish gross turnover from fee revenue, the percentage charged from the percentage allocated, and historical realized payments from present settings. Fee balances and rewards can also contain donations, prefunding or purchased assets. Do not infer provenance from a current balance alone.

## Conditional launch-platform review

For Pons, resolve the launch's factory generation and deployed curve/locker/hook from current official [contracts](https://github.com/ponsdotdev/ponsfamily) and [V2 documentation](https://docs.ponsfamily.com/v2). V1 and V2 use different launch paths. For V2, distinguish curve trading from post-graduation pool trading; read the actual token recipient when checking early-buy exemptions and tax. Inspect quote denomination, fee escrow, buyback custody and unlock terms. Do not copy a factory address, fee rate or lock claim from an older deployment into the target report.

For Robinhood Chain, verify the requested mainnet or testnet against [official connection documentation](https://docs.robinhood.com/chain/connecting/) and observed RPC chain ID. Do not describe test assets as economic backing or assume a familiar symbol has identical issuer rights on another network. Platform-specific source review does not establish deployment correspondence or scanner coverage.

Reviewed 2026-09-06. Use these branches only when the target's provenance supports them; unrelated EVM tokens do not require Pons tooling.
