---
name: galleon-morpho-market
description: "Use when evaluating a specific Morpho Blue market or Morpho vault allocation, oracle, LLTV, borrow liquidity or exit risk."
license: MIT
compatibility: "Read-only EVM RPC or official provider tools; Bun is optional for offline examples. No signer required."
metadata:
  version: "0.3.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Morpho market diligence

Resolve the **chain plus market ID or vault address** before evaluating yield. Morpho Blue markets are permissionless. A listed market or curator brand is discovery evidence, not a risk endorsement.

## Identify the object

For a Blue market, read `idToMarketParams(id)` and record all five fields: loanToken, collateralToken, oracle, IRM and LLTV. Recompute the ID with the maintained SDK or the deployed market-ID library. Similar collateral tickers with different oracle, IRM or LLTV are different markets. Read code presence and token decimals on that chain.

For a vault, identify the implementation/version first. A legacy MetaMorpho V1 withdrawal queue is not the interface for Vault V2 adapters. Record asset, share decimals, curator/owner/guardian authority, fees, timelocks, caps and each allocation's downstream market identity. If version or adapter semantics are unknown, stop at a diligence report; do not fabricate a queue call.

## Market observations

Read `market(id)` and `position(id, account)` at a common block. Raw market totals can lag interest accrual; use the official accrual/share-conversion implementation for a current debt estimate. In particular, borrow shares are not loan-token units. Do not replace rounding and virtual-share offsets with a floating-point ratio.

Read the configured oracle's `price()` and its composition. Verify both token decimal conventions and the feed's freshness, fallback and manipulation assumptions. The Blue oracle price uses 1e36 scaling for raw collateral-to-loan conversion; token decimals are already embodied in that price. Applying token decimals twice can make the loan appear many orders of magnitude safer.

Calculate LTV against accrued debt and compare with the market's LLTV, then stress collateral price, loan price and interest. Read supply/borrow totals and identify immediately available liquidity. Liquidation eligibility and profitable liquidation are different: oracle delay, liquidation incentive and collateral market depth matter.

## Vault decision

Return reward-free yield, incentive yield separately, top allocations, concentration, oracle dependencies, governance delay and an exit estimate. For legacy V1, inspect supply and withdrawal queues and downstream utilization; deposits and exits use different constraints. For V2, follow each adapter's documented withdrawal route and loss accounting. A vault's high total assets or unfilled deposit cap does not prove redeemability.

For an account exit, pair share balance and `maxWithdraw`/`maxRedeem` with the appropriate previews and same-state simulation. Shared collateral across markets creates correlated exposure even when market IDs differ. Refuse to rank by headline APY when withdrawal liquidity or the relevant oracle cannot be read.

## Evidence and completion

Return the requested decision, exact deployment and chain, block/time, raw-unit observations, calculation assumptions, and the next missing read. Distinguish an indexed estimate, an onchain read, a simulated call and a confirmed transaction. Research ends with an actionable decision record; it does not require connecting a wallet.

For a requested write, prepare the complete unsigned sequence and simulate with the actual sender, amount, recipient and allowance state. Preserve authorization already supplied; research does not grant debt, spending or signing authority. Never request keys. After an authorized transaction, verify its receipt and the relevant balance or position change. On an ambiguous timeout, reconcile its hash and nonce before retrying.

Read [protocol references and worked record](references/recipe.md) only for the selected operation. Documentation checked 2026-09-27; refresh deployments and current parameters at use time. This directory is independently installable.
