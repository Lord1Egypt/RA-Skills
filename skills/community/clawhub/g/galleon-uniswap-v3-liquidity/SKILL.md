---
name: uniswap-v3-liquidity
description: "Use when managing a Uniswap v3 NFT position: choose usable ticks, mint or increase liquidity, collect fees, remove liquidity, or move a range. Resolves position inventory and fee accounting with exact manager calls; excludes v4 and gauge custody."
license: MIT
compatibility: "Read-only EVM RPC and official protocol APIs or UI. Optional Node.js 20 for offline helpers. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.6.1"
---

# Uniswap v3 Liquidity

Produce a position decision: keep, collect, increase, reduce, or replace the range. Include exact pool identity, inventory, usable ticks, costs, and an unsigned action sequence. Start with the user's token ID or pair and chain; do not require a wallet for public range analysis.

## Read the position before choosing a range

1. Resolve the chain's v3 factory and NonfungiblePositionManager from official deployments. Read their bytecode, `factory()` and pool identity at one block. A token ID without a manager and chain is ambiguous.
2. Existing NFT: read `ownerOf(tokenId)` and `positions(tokenId)`. Resolve the pool with `getPool(token0,token1,fee)`. Read pool `slot0()`, `tickSpacing()`, `liquidity()` and both token decimals. Preserve raw amounts as integer strings. A vault owning the NFT changes the withdrawal path; stop the direct-owner recipe and identify its share/redemption interface.
3. New position: establish address-sorted token0/token1 before expressing a price. Human token1 per token0 is `1.0001^tick * 10^(decimals0-decimals1)`. Inverting the display pair reverses the price bounds; it does not reverse protocol token order.
4. Pick the horizon and inventory constraints before ticks. Snap the lower tick down and upper tick up to spacing, remaining within usable TickMath bounds. The active interval is `tickLower <= currentTick < tickUpper`. Below range inventory is token0; at/above upper it is token1. Pool-wide liquidity is not the NFT's liquidity.
5. Use the official v3 SDK `Pool` and `Position.fromAmounts` for exact token composition and mint amounts, with the observed sqrt price and raw budgets. Do not price the required ratio from USD weights or floating-point token arithmetic.

## Choose the smallest operation

| User objective | Manager sequence | Completion evidence |
| --- | --- | --- |
| Claim fees | Simulate `collect` from owner, then prepare bounded collect | Recipient deltas and Collect event |
| Add capital to same range | Approvals as needed, `increaseLiquidity` | Same NFT, larger liquidity, actual debits |
| Reduce exposure | `decreaseLiquidity`, then `collect` | Smaller liquidity and received principal plus fees |
| Move range | Decrease, collect, optionally swap inventory, mint new NFT | Old and new IDs reconciled, residual assets reported |
| Close NFT | Full decrease, collect, then optional `burn` | Zero liquidity and owed tokens before burn |

`tokensOwed0/1` is checkpointed accounting, not necessarily current claimable fees. Simulate collection or calculate current inside fee growth with the matching SDK and block. A prior decrease adds principal to owed tokens: never label all collected tokens as income. Decreasing liquidity alone does not deliver tokens to the wallet. Increasing liquidity never changes ticks.

## Prepare and reconcile

Read [recipes](references/recipes.md) only for the selected operation. Bind recipient, max spends, minimum outputs, deadline, manager, allowance amounts and gas budget. Prefer official SDK calldata or the official UI; no new signing runtime. Simulate from the actual owner with the final calldata and value. Multi-step output-dependent swaps and remints stay deferred until inputs are known or the entire atomic call is simulated.

Changing range can crystallize inventory loss and pay swaps, gas and price impact. Compare modeled incremental fees over the user's horizon with those costs, and show the HOLD baseline. No headline APR implies a profitable rebalance.

This skill returns an unsigned plan unless an existing authorized wallet tool has explicit authority for the exact action. Never infer trade authority from installation or research. Reconcile a previously submitted hash before any resend. Completion requires a successful receipt, the manager's post-state, and recipient balance/event evidence at an identified block.

## Offline range probe

From this installed skill directory, run `node scripts/ticks.mjs '{"lower":-121,"upper":119,"spacing":60,"current":120}'`. It snaps integer tick bounds outward and identifies inventory side. It rejects invalid bounds and does not discover token order, choose a profitable range, or calculate mint amounts.

## Worked output

Synthetic equal-decimal pair, spacing 60, current tick 0, requested ticks -121..119: usable enclosing range is -180..120. An existing range -120..0 is out of range at tick 0 and holds token1 principal. Decision: do not increase it to recenter; price a replacement range first. If simulated collect is 25 token1 after a decrease credited 20 principal, at most 5 is fee income before rounding and previous owed balances. Return `plan-only`, old token ID, proposed ticks, cost estimate and missing simulation; do not fabricate a mint ID.

## Sources and maintenance

Primary sources checked 2026-09-27. [Protocol recipes and sources](references/recipes.md) contain the concrete calls. Recheck deployments and API schemas before preparing financial actions; documentation access alone proves no live position or transaction.
