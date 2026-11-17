# Task examples and user configuration

These observations and identifiers are synthetic teaching fixtures, not live quotes or receipts. Select actual operations from the available tool schema and the relevant provider documentation; descriptive reads below are not invented API names.

## Route the request

| Intent | Minimum inputs | Completion |
| --- | --- | --- |
| Explain or compare | Target, question and relevant supplied observations | Useful answer with calculation, evidence scope and material unknowns |
| Inspect an account | Explicit account/chain scope and appropriate read capability | Observed state with source and block/time |
| Prepare an action | Exact financial terms and current state needed by the action | Decoded unsigned plan and applicable simulation |
| Execute or reconcile | Matching authorization and action/receipt identity | Verified effects or precise pending/unknown state |

Use the current explicit request first, then supplied saved preferences for provider, account scope, denomination, horizon, freshness, cost and output detail. For reversible analysis, state a material provisional assumption when useful; ask only when a missing input changes the requested answer. Public research does not require a wallet. Preferences never supply missing financial authority. Keep compatible user tools even when their provider is absent from the examples. Discover their schemas and evidence quality before use.

## Worked successful task

**Request:** Prepare the already authorized stream: 86.4 USDC over 24 hours to the supplied recipient.

**Available evidence:** Synthetic exact chain, 6-decimal USDC address and recipient are supplied to the mock builder. Duration 86,400 seconds. Builder enforces total cap and end time, simulation matches terms. Existing authorization covers this exact stream. No submission receipt supplied.

**Read sequence:** Resolve asset decimals, recipient and clock; calculate integer rate and remainder, inspect enforceable cap/end time and simulated funding before signing.

**Completed answer:** Rate = 86,400,000 atomic units / 86,400 seconds = 1,000 atomic units per second, or 0.001 USDC/s. Total cap 86.4 USDC; duration 24 hours. Return the calculated stream terms and the supplied simulation result. No encoded unsigned payload or absolute start time was supplied, so an actual signable artifact still needs retrieval and review. Terms are calculated; no stream is confirmed. Do not describe terms alone as a constructed transaction or request the same valid authorization again.

## Recovery and continuation

**Changed evidence:** A submission later returns a timeout with known transaction hash and no receipt.

**Useful response:** Preserve submitted/unknown status and reconcile that hash plus stream creation/funding events before another submission. Do not re-request permission for unchanged valid terms merely because a transport timed out.

If an existing compatible provider can supply the missing observation within the user's scope, perform that read and resume this same task. Otherwise deliver the supported partial result and name the exact missing observation. Do not end at generic setup advice or install another stack by default. An uncertain write requires reconciliation through its existing identity before retry decisions.
