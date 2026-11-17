---
name: lifi-cross-chain
description: "Use when comparing LI.FI bridge quotes, preparing an unsigned cross-chain transfer, or diagnosing source-confirmed destination-pending, partial or refunded transfers. Reconciles actual destination asset and amount rather than declaring success from a source receipt."
license: MIT
compatibility: "Read-only EVM RPC and official protocol APIs or UI. Optional Node.js 20 for offline helpers. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.3.1"
---

# LI.FI Cross-chain

Produce a route comparison with a minimum destination amount and a source-to-destination evidence ledger. For an already submitted route, begin with its source hash and status; do not fetch a new transfer as a recovery action.

## Quote one exact intent

Collect source/destination chain IDs, exact token addresses, raw input amount, sender, recipient, slippage fraction, maximum cost and deadline. Resolve destination gas needs separately from the bridged token. A USDC receipt cannot pay native gas by itself.

Use the official `/v1/quote` recipe in [recipes](references/recipes.md). Quote returns one executable Step with `transactionRequest`; broader `/advanced/routes` comparison yields route steps whose transaction data must be obtained through `/advanced/stepTransaction` when ready. Do not assume a route list already contains executable calldata or precompute later steps from stale balances.

Record quote ID, tool/bridge, included steps, action, `estimate.toAmount`, `toAmountMin`, feeCosts, gasCosts and executionDuration. LI.FI slippage is a fraction: `0.005` means 0.5%. Compare routes for the same assets, recipient, amount and quote window. Compare raw minimum amounts only when destination token and decimals match. Do not subtract fees already reflected in minimum output twice; account separately for extra source/destination native gas.

## Inspect the handoff

Verify `action.fromAddress`, `toAddress`, token/chain identities and returned transaction target/value/data. Check chainId and chain-native gas balance, simulation and quoted allowance. `estimate.approvalAddress` is a spender hint requiring verified protocol/deployment checks, not permission for unlimited approval. `transactionRequest.to` and approval spender need not be the same address.

Use existing official SDK/UI or an authorized wallet tool for requested execution; this skill supplies no signer. Return unsigned terms for research/planning. Exact authority must cover recipient, spend, route, slippage and expiry. If construction or approval changes those terms, re-evaluate before any send. Persist source hash/route ID before waiting for settlement.

## Reconcile until a meaningful terminal outcome

Query `/v1/status` with source hash and chain IDs; bridge/tool can help disambiguate. Observe provider rate limits and retry-after. Do not run an unbounded tight polling loop: report pending with a bounded next-check time when the task cannot wait.

| Provider state | What to report and verify |
| --- | --- |
| NOT_FOUND / INVALID | No indexed transfer yet or bad input; verify source hash/chain/receipt before concluding failure |
| PENDING | Source and destination stages separately; keep same transfer identity |
| DONE + COMPLETED | Verify destination receipt, exact asset, recipient and raw amount against quoted minimum |
| DONE + PARTIAL | Report received asset and amount; destination swap can fail while bridge delivers an intermediate asset |
| DONE + REFUNDED | Identify refund chain, asset, recipient, hash and net amount; original destination obligation is not paid |
| FAILED or unknown | Preserve error/substatus, inspect source/refund evidence; do not create a second transfer automatically |

A provider quote object can appear while pending; it is an estimate, not receiving evidence. A DONE label alone cannot establish intended delivery. Compare `receiving.amount` with the saved `toAmountMin` only after token identity, chain and decimals agree. Reconcile actual destination logs/balances against source debit and both gas costs. A refund is a distinct outcome, not success at the destination.

## Offline outcome classifier

Run `node scripts/settlement.mjs '{"status":"DONE","substatus":"PARTIAL"}'` from this installed skill directory to classify a saved response without network access. For COMPLETED supply positive `expectedChain`, `receivedChain`, EVM `expectedToken`, `receivedToken`, and integer-string `minimumRaw`, `receivedRaw`. The helper compares large amounts exactly and never treats supplied observations as independent chain proof. It intentionally handles EVM token identities only.

## Worked output

Synthetic 1,000 USDC from Base to Arbitrum, minimum 995 USDC. Source receipt succeeds; LI.FI returns DONE/PARTIAL with 0.42 WETH at destination. Report `partial, received 0.42 WETH; 995 USDC objective not satisfied`. Do not compare WETH raw units with a USDC minimum. Show the destination hash and recipient proof; quote a separate WETH-to-USDC remedy only if requested, without repeating the bridge.

For DONE/COMPLETED with actual 997 USDC and quoted estimate 998/minimum 995, report a 1 USDC difference from estimate and 2 USDC above minimum, not slippage failure. Completion remains unverified until the destination evidence agrees.

## Sources and maintenance

Primary sources checked 2026-09-27. [Protocol recipes and sources](references/recipes.md) contain the concrete calls. Recheck deployments and API schemas before preparing financial actions; documentation access alone proves no live position or transaction.
