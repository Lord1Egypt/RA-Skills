---
name: uniswap-swap
description: "Use when quoting or preparing a Uniswap token swap, reviewing Permit2 authorization, choosing an AMM versus UniswapX path, or reconciling a submitted swap. Uses the official Trading API with exact raw amounts and route-specific lifecycle handling."
license: MIT
compatibility: "Read-only EVM RPC and official protocol APIs or UI. Optional Node.js 20 for offline helpers. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.3.1"
---

# Uniswap Swap

Return a comparable quote and a bounded unsigned handoff, or resolve an existing transaction/order. Distinguish `CLASSIC` AMM transactions from UniswapX signed orders before constructing anything. Use the official Trading API or verified official interface; a wallet connection is not needed to explain or compare a public quote, but its real swapper address is needed for an executable one.

For application integration work, discover the official `swap-integration` skill from `uniswap/uniswap-ai` if already available. This operational recipe complements that upstream integration surface; it does not require an automatic install or replace upstream transaction builders.

## Gather and quote

Require chain IDs, exact input/output token addresses, raw integer amount, exact-input or exact-output intent, swapper, recipient intent, slippage and expiry/cost bounds. Look up token decimals on the selected chain; symbols do not identify assets. For exact-output intent show maximum input, not a fixed input debit.

Use [API recipes](references/recipes.md). Obtain an API key through the user's existing secret mechanism; never print it. Missing key means use a connected official tool/UI or produce a parameter-complete request marked unqueried, not a fabricated quote. Pin one supported `x-universal-router-version` consistently through the journey. For an AMM-only task request `protocols: ["V2","V3","V4"]` only if the user accepts those protocols; narrow to the approved subset when required.

Interpret the actual `routing` discriminator, `quoteId`, quoted input/output and minimum/maximum amounts. Preserve returned quote JSON rather than reconstructing it. Check `txFailureReason`, gas, recipient, chain, token identities and quote time. A successful quote endpoint does not prove allowance, affordability or a submitted swap.

## Approval and route lifecycle

1. Use `/check_approval` with the actual wallet, token, chain and required amount. Inspect any returned revoke/approval transaction: target, spender, token, raw cap and chain. ERC-20 allowance to Permit2 and a signed Permit2 message are different authorizations.
2. If quote contains `permitData`, inspect its domain chain/verifying contract, token, spender, amount, nonce and deadlines. The wallet must explicitly authorize that exact message in an execution workflow. A signature belonging to an older quote must never be attached to a refreshed one. Do not expose signatures in a report.
3. `CLASSIC`: `/swap` constructs an unsigned transaction from the preserved quote and matching permit data/signature when needed. Inspect and simulate returned from/to/data/value/chain before any authorized wallet sends it. The skill itself includes no signer. Do not request a signature merely to complete a research task.
4. UniswapX routes such as `DUTCH_V2`, `DUTCH_V3` or `PRIORITY`: an order signature can authorize spending. Use the corresponding official `/order` flow and track order identity/fills. Never feed an auction order into the AMM `/swap` recipe or label order acceptance a mined fill. Unsupported routing types require their documented flow, not a guessed fallback.
5. A changed token, recipient, chain, route, quote or limit invalidates the old packet. Refresh and recheck; do not silently relax slippage to make simulation pass. Native input has value/gas requirements, and wrapping is not an ERC-20 transferFrom.

## Reconcile the result

For AMM swaps record submitted hash, receipt status and block, input debit, output received by intended recipient, gas paid, and any unspent input/refund. Token transfer logs must agree with the actual token addresses and account deltas; handle unrelated concurrent transfers rather than blindly subtracting two balances. An RPC timeout after send is `submission-unknown`: inspect the original hash/nonce instead of creating a new send.

For orders query `/orders` using the documented order identifier and reconcile on-chain fills, remaining authorization, expiry and cancellation status. An expired quote is not proof an already signed order is cancelled. Never retry by signing another order while the first may still fill.

## Worked output

Synthetic exact-input 100 USDC (6 decimals): amount `100000000`; slippage `0.5` means 0.5 percent in this API. Returned CLASSIC minimum is `49000000000000000` WETH and permitData is present. Report minimum 0.049 WETH plus separately quoted gas; state `quote-only, signature and simulation absent`. If a second quote replaces the first, discard the earlier permit handoff. Do not use LI.FI's fractional slippage convention here.

## Sources and maintenance

Primary sources checked 2026-09-27. [Protocol recipes and sources](references/recipes.md) contain the concrete calls. Recheck deployments and API schemas before preparing financial actions; documentation access alone proves no live position or transaction.
