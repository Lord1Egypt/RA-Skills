# Route, swap and recovery workflows

## Quote and approval contract

Capture `network`, `fromChain`, `toChain`, token contracts/mints and decimals, base-unit amount, exact-in/out mode, sender, ultimate recipient, venue/tool version, quote time/expiry, conservative output, all fees, gas reserve and maximum slippage. Include intermediate tokens, approval spender and amount, permit domain/nonce/deadline, transaction target/value and any destination calls. Resolve integer precision before comparing prices.

Use official builders rather than copying router calldata. A quote is not proof of current allowance or sufficient gas. Native currency needs no ERC-20 approval; wrapped currency does. For a fee-on-transfer or rebasing asset, require an explicitly supported route. Review both approval and action, and use finite scope. Separate typed-data permits from token transactions. Requote after delays or confirmed approvals when the provider contract requires it; changing calldata or recipient invalidates the reviewed plan.

Do not hide integrator, RFQ, bridge, priority or destination execution fees inside the displayed exchange rate. An API key, subscription or x402 payment may have a separate cost. No paid fallback is implied by a failed free query.

## Same-chain swaps and signed intents

1. Validate the current quote and exact payload against approved terms.
2. Simulate where the provider supports it; simulation success predicts a specific state, not guaranteed inclusion.
3. Hand off to an existing trusted wallet only under active authorization. A signed off-chain CoW/1inch intent can move assets when a solver fills it; it is not a harmless login signature.
4. Record transaction hash or order UID before reporting progress. Check action-level errors even with HTTP 200.
5. Reconcile fills, recipient balances and terminal order state. A partially filled order may remain open for the remainder. Cancellation can race with a fill; reread before placing a replacement.

For Jupiter managed `/order` transactions, preserve returned bytes until signing and use the matching execution request. Custom instructions belong in the `/build` path. Check Solana signature status, transaction error and actual token deltas; a signature string or blockhash expiry alone is not evidence that nothing landed. Rebuild expired transactions only after resolving prior signature state.

## Cross-chain settlement

Treat route stages independently: quoted → source approved → source submitted → source confirmed → destination pending/submitted → delivered, partial or refunded. Store bridge/request identity, source hash, destination hash, recipient and actual output. Pending or unknown states retain the original identity across restarts. A source receipt cannot establish destination execution, and a destination transfer cannot establish a subsequent vault deposit.

Provider-specific checks:

- **LI.FI:** inspect status plus substatus. `DONE/COMPLETED`, `DONE/PARTIAL` and `DONE/REFUNDED` are different outcomes. For PARTIAL, inspect actual receiving tokens and any split/refund; do not promise full value merely from the label. Refund location depends on bridge and can be the destination. `NOT_FOUND` can mean indexing delay. [LI.FI status recovery](https://docs.li.fi/agents/workflows/status-recovery), [intermediate tokens](https://docs.li.fi/guides/intermediate-tokens), accessed 2026-09-05.
- **Relay:** `submitted` is destination submission, `success` a successful destination fill; `delayed` remains processing. `refund` and `failure` are distinct. Reconcile returned hashes and account state. [Relay status v3](https://docs.relay.link/references/api/get-intents-status-v3), accessed 2026-09-05.
- **Across:** track deposit through destination fill using the current API. For embedded actions, confirm final recipient position/token state, not just relayer delivery to a handler. Read supported chain/token/action combinations live. [Across workflows](https://docs.across.to/ai-agents/agent-examples), accessed 2026-09-05.

Fee accounting: a quote's conservative output already reflects the provider's conversion charges, so do not subtract displayed fee components again. A fee breakdown often lists parts of one total, for example relayer gas and relayer service inside a relayer total, rather than additive charges; only source network gas is additional. Sequence a cross-chain entry as bridge the sized amount plus destination gas reserve, verify destination delivery, then trade. Never trade on the destination before delivery is verified, and never obtain a fresh quote to escape an unresolved deposit.

## CCTP V2

Verify supported source/destination domains and version-specific contracts. The stages are burn → adequate source finality → attestation → destination mint transaction → verified receipt and recipient balance. Threshold 1000 requests fast confirmation; 2000 requests finalized confirmation. Fast capacity and costs must be checked live. Finality varies by chain; an L2 source may depend on L1 batches. Never promise a universal transfer time.

Use current `/v2/messages` and `/v2/burn/USDC/fees`; the older fast-fees endpoint is deprecated. Check `destinationCaller` restriction before mint. A valid attestation can still fail for expired authorization, insufficient destination gas or a missing Solana token account. Inspect used nonce and destination receipt before retry; a completed burn must not be repeated to repair minting. Re-attestation is a separate request, not proof of mint completion. [Circle technical guide](https://developers.circle.com/cctp/references/technical-guide), [mint recovery](https://developers.circle.com/cctp/howtos/retry-failed-mint), [finality](https://developers.circle.com/cctp/concepts/finality-and-block-confirmations), accessed 2026-09-05.

## Unknown results and handoff

Retry bounded read requests using provider limits and Retry-After. Never retry ambiguous writes automatically. Persist original identifiers, last observed state/time, evidence sources and next eligible poll. If the polling budget expires, return pending/unknown and the next read; do not create a scheduler unless requested.

A recovery swap, manual refund claim or destination deposit is a new financial action with current asset identity, quote, costs and authorization. Return usable evidence even if the next action cannot execute. A compact completion record contains route/request ID, both networks, source and destination receipts, expected versus actual token/amount, recipient, finality, fee evidence, unresolved gaps and next action.
