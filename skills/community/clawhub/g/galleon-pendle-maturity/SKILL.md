---
name: galleon-pendle-maturity
description: "Use when evaluating a Pendle PT or YT trade, comparing hold-to-maturity with an early exit, or redeeming a matured position."
license: MIT
compatibility: "Read-only EVM RPC or official provider tools; Bun is optional for offline examples. No signer required."
metadata:
  version: "0.2.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Pendle maturity planner

Produce a maturity decision for an exact **chain, market, SY, PT and YT**. A token ticker plus date is insufficient. PT claims are denominated in the market's accounting asset; they are not universally a dollar or one unit of the receipt token.

## Establish the instruments

Read the market's `readTokens()` and `expiry()`, then verify token addresses and underlying SY integration against official Pendle data. Record the chain block timestamp, not the laptop clock, for expiry decisions. Identify the SY accounting asset, supported redemption token, exchange rate and underlying protocol's withdrawal or cooldown restrictions. Do not treat an advertised PT rate as a dollar guarantee.

Separate PT principal, YT's pre-expiry yield exposure and LP inventory. If the user holds LP, first account for removal outputs; an LP token is not a PT balance. If tokens are posted as collateral elsewhere, an exit also requires that position's health check.

## Compare the three paths

- **Hold PT:** compute implied return in the accounting asset using the actual acquisition quote and remaining time. Deduct gas, fees and redemption costs. Annualization close to expiry can make a tiny absolute gain look attractive. Disclose depeg, underlying protocol and redemption constraints.
- **Sell before expiry:** fetch an exact-size route through the maintained Hosted SDK; retain chain, market, token in/out, amount, min output, price impact, route timestamp and destination. A thin PT pool can make the realized exit materially worse than the display price. No quote means no executable exit estimate.
- **Redeem:** before expiry, paired equal PT and YT amounts are needed for the paired redemption path; holding PT alone is insufficient. After expiry, principal redemption no longer needs matching YT. Follow the deployed router/Hosted SDK flow into SY or supported output and include any underlying cooldown. YT's future yield stream ends at expiry; separately account for already accrued claimable yield/rewards.

For comparison, show units and costs in the same accounting asset. Rewards/points are a separate speculative row, not guaranteed principal return. A rollover is an exit plus a new purchase with new maturity and risk; do not silently roll the position when the user only requested redemption.

Inspect the actual Hosted SDK response schema and transaction fields. Decode target, spender, recipient, value, amount and minimum output, then simulate the full route. Do not synthesize calldata from an old API example or use a price endpoint as a trade builder.

## Evidence and completion

Return the requested decision, exact deployment and chain, block/time, raw-unit observations, calculation assumptions, and the next missing read. Distinguish an indexed estimate, an onchain read, a simulated call and a confirmed transaction. Research ends with an actionable decision record; it does not require connecting a wallet.

For a requested write, prepare the complete unsigned sequence and simulate with the actual sender, amount, recipient and allowance state. Preserve authorization already supplied; research does not grant debt, spending or signing authority. Never request keys. After an authorized transaction, verify its receipt and the relevant balance or position change. On an ambiguous timeout, reconcile its hash and nonce before retrying.

Read [protocol references and worked record](references/recipe.md) only for the selected operation. Documentation checked 2026-09-27; refresh deployments and current parameters at use time. This directory is independently installable.
