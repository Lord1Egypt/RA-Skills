# Test matrix

## Unit and property tests

- token ordering and decimal conversion
- exact fee and basis-point arithmetic
- tick snapping, bounds, negative compression, and upper-tick exclusivity
- v2 reserve-share amounts and embedded-fee accounting
- concentrated amount math below, inside, and above range
- duplicate accounting and HOLD-baseline protection
- capability routing by protocol and position type
- stale-plan, cooldown, spend, impact, and economic skip gates
- backtest gaps, candle-path uncertainty, interval-specific fee dilution, and lookahead prevention
- fungible share accounting across multi-currency hook reserves

## Fork tests

Pin chain, block, deployment addresses, and expected code hashes. Cover:

- read and quote for every supported protocol and chain
- mint or add, increase, decrease, collect, stake, claim, unstake, remove, and burn where supported
- native and wrapped value paths
- Permit2 and direct approval paths
- v4 pools with no hook and each supported hook class
- StateView reads, PositionManager event discovery, and onchain position reconciliation
- LP API approval wrappers, permit normalization, field-name variants, KYC warnings, and stale transaction payloads
- Aerodrome stable, volatile, and Slipstream routes
- one-token and third-token atomic funding, per-leg swap minima, leftovers, and refunds
- atomic range moves that replace an NFT and preserve position lineage
- receipt decode and state reconciliation

## Negative tests

- wrong chain, wallet, token order, decimals, pool, hook, gauge, target, or selector
- owner mismatch, approval mismatch, insufficient balance, and stale nonce
- empty or placeholder calldata
- expired deadline, excessive price impact, gas cap, spend cap, and minimum-output failure
- fee-on-transfer, rebasing, paused, blacklisted, honeypot, and high-tax tokens
- indexer lag, RPC disagreement, partial bitmap read, and missing logs
- hook revert, blocked removal, callback reentrancy, malicious delta, forged hook user identity, and unexpected external call
- gauge epoch change, reward exhaustion, and fee-right mismatch
- active automation conflict, beneficial-owner mismatch, unsafe standing NFT approval, and missing disable path
- stale or short-lived quote, unexpected allowance target, one deficient swap leg, and missing refund
- hook reserve drift, stale or malformed rate source, invariant non-convergence, and degraded withdrawal

## Partial-state tests

- approval mined, mint reverted
- decrease mined, collect reverted
- unstake mined, removal reverted
- submission timed out but transaction later mined
- transaction replaced at the same nonce
- receipt succeeds but expected state diff does not match
- old NFT changed but replacement NFT, owner, configuration, or refund is missing

Assert recovery begins from reread chain state and never blind-retries.

## Packaging tests

Validate every `SKILL.md`, plugin manifest, relative link, CLI command, npm tarball, and clean install. Keep routing evals with prompts that should and should not load each skill.
