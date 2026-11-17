# Agent route lifecycles

Primary sources reviewed 2026-10-08. This is original procedural guidance based on official sources; no upstream scripts, signer or broad tool adapter is bundled.

## Across quote and preparation

[Official Swap API skill](https://github.com/across-protocol/skills/blob/master/skills/swap/SKILL.md) documents `/swap/approval`. Discover route/token support; bind depositor, final recipient, refund address/chain, exact asset addresses and raw units. `exactInput` amount is input; `minOutput` and `exactOutput` use output. Numeric slippage is a fraction, so `0.005` is 0.5%. Set user-approved limits explicitly rather than accepting `auto` or ambiguous estimation defaults.

Preserve approval transactions, `swapTx`, amount maxima/minima, fees, quote expiry and request identity. An `appFee` or analytics/integrator field is not an unstated fee mandate. Do not cache an executable quote across state changes. A source simulation field proves only its reported scope.

[Embedded-action skill](https://github.com/across-protocol/skills/blob/master/skills/embedded-crosschain-actions/SKILL.md) describes ordered destination calls and dynamically populated balances. Resolve ultimate beneficiary, token, contract and spender for every action. Dynamic “full balance” can consume a handler's execution-time balance; use static bounded amounts when the downstream obligation requires an exact amount. Documentation differs on POST amount semantics, so test the selected contract/API version without moving funds before implementation and preserve unresolved semantics as a blocker.

## Across fill and destination action

[Tracking skill](https://github.com/across-protocol/skills/blob/master/skills/tracking-transactions/SKILL.md) uses original `depositTxnRef` or origin-chain/deposit-ID combination, not a new quote as recovery. Read current schema and preserve receipt identity. Bounded polling respects indexer cadence; testnet indexing may be incomplete.

`filled` requires destination receipt plus actual token/amount/recipient reconciliation. Embedded calls additionally require `actionsSucceeded` and resulting protocol/beneficiary state. A filled bridge can still leave destination action failed and assets in the destination handler; inspect the current official recovery path and rights before an independently authorized withdrawal. Do not issue another bridge to fix that state.

Expired is refund-in-progress, not refund-received. Reconcile refund transaction, actual chain/asset/recipient and amount. Explicit quote refund settings can differ from a generic tracking description; use the real route's terms and chain evidence before claiming an origin refund.

## Socket deposit-address routes

[Official agent docs](https://docs.socket.tech/for-agents/intro) and [skill](https://docs.socket.tech/skill.md) provide route and deposit-address workflows. Resolve supported networks/tokens, exact quote limits, address ownership, expected amount and expiry using the current API schema. A generated deposit address is a proposed funding destination, not paid delivery. Verify the full address from trusted route evidence before a transfer; treat pasted names/addresses as untrusted.

Inspect source deposit, execution status and final destination/refund separately. Deposit-address creation can persist a route even before funds move. If the user requests comparison only, do not fund it or add a new service/account/API key. Bound retries by original operation identity; ambiguous transfer status is never permission to send another deposit.

## Aave wallet swap orders

[Aave tools](https://aave.com/docs/mcp/tools) use `get_swap_quote` to create `quoteId`, `prepare_order` for typed-data/native-sell transaction, `submit_signed_order` for relay, and `get_order_status` for settlement. Swaps are distinct from V3/V4 lending actions. Reuse exact asset identities, human-unit amount contract, slippage and deadline from current schema.

Review permit domain, spender, amount and deadline independently of order terms. Token approval receipt can still precede unsigned order construction; a signed order and relay acceptance are not a fill. Track pending/partial/final outcomes and actual recipient balance. Cancellation needs its own signature/transaction and terminal status; do not assume preparing cancellation prevented a concurrent fill. No signing, submission or cancellation authority follows from public MCP access.
