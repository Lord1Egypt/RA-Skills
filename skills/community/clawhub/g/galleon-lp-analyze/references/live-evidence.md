# Live evidence

## Source order

1. Current official protocol documentation, deployment registry, contract repository, and audits
2. Direct RPC reads and verified explorer data at a named chain and block
3. Protocol-native subgraphs, APIs, and indexers with known lag
4. Independent analytics for discovery and cross-checks
5. Social posts only as leads to verify

Search snippets, model memory, pool names, and dashboard cards are not evidence of current state.

DexScreener can discover candidate pools and current market labels. DefiLlama can cross-check reported TVL, fee yield, and incentives. Treat both as independent analytics: bind their returned addresses to verified pools, inspect metric definitions and windows, and confirm execution-critical state through RPC or a protocol-native source.

## Minimum live record

For each changing claim, retain:

- UTC observation time
- chain ID and block number where applicable
- endpoint or contract and method
- raw unit and decimal conversion
- source window, pagination, and known lag
- whether a second source agreed

Use exact integers for balances, liquidity, fees, token units, bitmap words, and calldata. Convert to decimal only for presentation.

## Freshness

Derive a freshness limit from the decision. A submission plan usually needs same-block or near-block state. A seven-day fee comparison can use a trailing window but still needs a current endpoint check. State the chosen limit; do not hide stale values inside a score.

If a read fails, distinguish absence, lag, rate limiting, unsupported protocol, and RPC disagreement. Keep the last good observation only as labeled history. It cannot authorize a new transaction.

## Read-only rule

Research may call read methods, estimate gas, and simulate without broadcasting. It must not request a wallet signature, modify an allowance, call a transaction-building endpoint, or submit a write.
