---
name: galleon-aave-position
description: "Use when checking an Aave V3 health factor, sizing a borrow, or planning a repay and collateral withdrawal; use for eMode and isolation constraints, not Aave V4."
license: MIT
compatibility: "Read-only EVM RPC or official provider tools; Bun is optional for offline examples. No signer required."
metadata:
  version: "0.3.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Aave V3 position risk

Produce a borrow/repay decision for one **EVM Aave V3 pool**. First identify chain, PoolAddressesProvider, Pool, account, requested debt asset and action. V4 hubs/spokes and Aptos require their own interfaces; stop this recipe if the deployment is not V3.

For official MCP use, load [current MCP procedure](references/mcp.md) first. Its human-unit amounts differ from the raw contract calls below.

## Read and reconcile

1. Resolve the pool from the official address book, then call the provider's `getPool()` and `getPriceOracle()`. Pin reads to one block and record its timestamp. Do not reuse another chain's deployment or assume USD base units.
2. Read `getUserAccountData(account)` and `getUserEMode(account)`. Account data includes collateral/debt in the oracle base currency, weighted liquidation threshold/LTV in basis points, and health factor in 1e18 units. Read the oracle base unit and asset prices before converting values.
3. Enumerate supplied and borrowed reserves using the deployment's documented data provider/SDK. For each, collect token decimals, aToken and variable-debt balances, collateral enablement, applicable eMode threshold, current variable rate, caps, available underlying, freeze/pause flags, isolation debt ceiling and borrowable-in-isolation status. An aggregate health factor cannot establish that a particular new borrow is permitted.
4. Reconcile your per-reserve weighted collateral and debt with `getUserAccountData`. Stop sizing if the discrepancy cannot be explained by accrual, rounding, eMode or different blocks. Do not infer available liquidity from supply caps.

## Decide

Build current, requested-post-state and stressed-post-state rows. Health factor is liquidation-threshold-weighted collateral value divided by debt value. Apply collateral and debt price shocks separately; include interest over the requested holding period. Changing eMode or collateral composition invalidates the old weighted threshold. Zero debt means no finite liquidation health factor, not a divide-by-zero error.

Use a user-selected minimum health factor, never a universal safe threshold. Report the protocol's maximum separately from that user's budget. A collateral withdrawal can reduce health faster than its unweighted value suggests. Borrowing at the limit leaves no allowance for debt accrual or oracle moves.

For a requested borrow, prepare `borrow(asset, amount, 2, 0, onBehalfOf)` only after reserve checks. Borrowing for another account requires credit delegation, not ERC20 approval. A repay uses the debt asset, and a subsequent withdrawal must be simulated against the repaid state. Exact full repayment needs an accrual buffer or the documented full-repay mode for the actual caller; never assume a displayed debt amount clears it.

## Evidence and completion

Return the requested decision, exact deployment and chain, block/time, raw-unit observations, calculation assumptions, and the next missing read. Distinguish an indexed estimate, an onchain read, a simulated call and a confirmed transaction. Research ends with an actionable decision record; it does not require connecting a wallet.

For a requested write, prepare the complete unsigned sequence and simulate with the actual sender, amount, recipient and allowance state. Preserve authorization already supplied; research does not grant debt, spending or signing authority. Never request keys. After an authorized transaction, verify its receipt and the relevant balance or position change. On an ambiguous timeout, reconcile its hash and nonce before retrying.

Read [protocol references and worked record](references/recipe.md) only for the selected operation. Documentation checked 2026-10-08; refresh deployments and current parameters at use time. This directory is independently installable.
