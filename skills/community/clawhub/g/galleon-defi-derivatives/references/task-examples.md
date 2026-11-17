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

**Request:** Calculate an incremental ETH hedge using my existing venue; target zero delta. Analysis only.

**Available evidence:** Spot +10 ETH, filled linear ETH perp -3 ETH, live unfilled sell order -2 ETH. Contract multiplier 1 ETH, no other exposure. Assume the resting order fills for target planning and separately report current filled exposure.

**Read sequence:** Read exact contract multiplier, filled positions, open orders and spot units; calculate current and contingent delta separately.

**Completed answer:** Filled exposure is +7 ETH. If the resting sell fills, projected exposure is +5 ETH; an additional 5 ETH short targets zero projected delta. If that order does not fill, the additional hedge leaves +2 ETH. Recheck/cancel-or-account-for the resting order before preparing an executable order.

## Recovery and continuation

**Changed evidence:** The open-order read times out after a prior submission.

**Useful response:** Report +7 ETH filled exposure only, mark contingent exposure unknown and reconcile the existing order before computing a new executable size.

If an existing compatible provider can supply the missing observation within the user's scope, perform that read and resume this same task. Otherwise deliver the supported partial result and name the exact missing observation. Do not end at generic setup advice or install another stack by default. An uncertain write requires reconciliation through its existing identity before retry decisions.
