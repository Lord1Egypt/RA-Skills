---
name: galleon-vault-exit
description: "Use when checking how much can leave an ERC4626 vault now, choosing withdraw versus redeem, or diagnosing preview, liquidity, fees and asynchronous exit constraints."
license: MIT
compatibility: "Read-only EVM RPC or official provider tools; Bun is optional for offline examples. No signer required."
metadata:
  version: "0.2.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# ERC4626 vault exit

Produce an **exit feasibility record**, not an APY ranking. Resolve chain, vault, implementation, asset, owner, receiver and requested amount. Explicitly distinguish assets from shares and preserve each token's decimals.

## Read at one block

Collect `asset()`, vault and asset `decimals()`, `balanceOf(owner)`, `totalAssets()`, `totalSupply()`, `maxWithdraw(owner)` and `maxRedeem(owner)`. Determine whether the contract really implements synchronous ERC4626 exits, or an asynchronous extension such as ERC7540. A familiar vault brand does not establish interface semantics.

For an exact-asset request, call `previewWithdraw(assets)` to estimate shares burned, then compare assets with `maxWithdraw(owner)` and required shares with ownership. For an exact-share request, call `previewRedeem(shares)` to estimate assets received, then compare shares with `maxRedeem(owner)`. Previews describe conversion including exit fees but deliberately ignore withdrawal limits. `convertToAssets` is an idealized conversion, not an executable quote.

Read implementation-specific pause, cooldown, queue, withdrawal fee and strategy-liquidity state. For asynchronous redemption, identify request/controller/owner roles and the request-to-claim transition from that vault's interface; do not force a synchronous preview or pretend a request receipt is liquid assets. Unknown interface means report the missing method/source, not invent `claim()`.

## Build a bounded exit

Choose `withdraw(assets, receiver, owner)` when the user needs a specific underlying amount, or `redeem(shares, receiver, owner)` when disposing a specific share amount. A third-party caller may need share allowance. A direct owner redemption does not generally require approving the underlying asset. Verify actual implementation rules and do not approve a random router to repair an unexplained revert.

Standard ERC4626 methods do not include maxShares/minAssets slippage arguments. If the user requires a bound, use a documented router with that bound or another explicitly supported mechanism; never invent extra arguments. Simulation uses actual sender/receiver and current allowance. Slippage bounds, preview freshness and short submission windows all matter; a past preview is not a promise.

If the request exceeds liquidity, return the available portion and remaining amount, plus the specific documented queue/wait route. Do not split or submit a partial exit without authorization for that outcome. A token balance held by the vault is not the full strategy-withdrawable liquidity.

After authorized execution, reconcile burned shares, received underlying, receipt events and fees. Reread remaining shares. Preserve losses in the record; a higher share price can coexist with withdrawal fees or insufficient liquidity.

## Evidence and completion

Return the requested decision, exact deployment and chain, block/time, raw-unit observations, calculation assumptions, and the next missing read. Distinguish an indexed estimate, an onchain read, a simulated call and a confirmed transaction. Research ends with an actionable decision record; it does not require connecting a wallet.

For a requested write, prepare the complete unsigned sequence and simulate with the actual sender, amount, recipient and allowance state. Preserve authorization already supplied; research does not grant debt, spending or signing authority. Never request keys. After an authorized transaction, verify its receipt and the relevant balance or position change. On an ambiguous timeout, reconcile its hash and nonce before retrying.

Read [protocol references and worked record](references/recipe.md) only for the selected operation. Documentation checked 2026-09-27; refresh deployments and current parameters at use time. This directory is independently installable.
