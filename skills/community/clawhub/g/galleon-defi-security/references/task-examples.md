# Task examples and user configuration

These observations and identifiers are synthetic teaching fixtures, not live quotes or receipts. Select actual operations from the available tool schema and the relevant provider documentation; descriptive reads below are not invented API names.

## Route the request

| Intent | Minimum inputs | Completion |
| --- | --- | --- |
| Explain or compare | Target, question and relevant supplied observations | Useful answer with calculation, evidence scope and material unknowns |
| Inspect an account | Explicit account/chain scope and appropriate read capability | Observed state with source and block/time |
| Handoff an action request | Requested terms and observed gaps | Evidence for the appropriate action-owning skill; this skill stays read-only |
| Inspect a claimed outcome | Explicit action/receipt identity and read capability | Observed effects and coverage; this skill does not sign or submit |

Use the current explicit request first, then supplied saved preferences for provider, account scope, denomination, horizon, freshness, cost and output detail. For reversible analysis, state a material provisional assumption when useful; ask only when a missing input changes the requested answer. Public research does not require a wallet. Preferences never supply missing financial authority. Keep compatible user tools even when their provider is absent from the examples. Discover their schemas and evidence quality before use.

## Worked successful task

**Request:** Review this finite approval and swap against my exact intent.

**Available evidence:** Synthetic complete decoded batch: approve exactly 100 USDC to the supplied router, swap exactly 100 USDC for minimum 0.04 ETH to the supplied account, matching chain and expiry. Complete simulation shows only that allowance and balance change; all targets resolved and no nested calls omitted.

**Read sequence:** Decode the actual payload and nested calls, resolve targets, compare each authority/value change with intent, inspect simulation coverage and return a bounded verdict.

**Completed answer:** Reviewed within the supplied bounds: chain, spender, finite 100 USDC allowance, recipient, minimum 0.04 ETH and expiry match intent; complete simulation matches those effects. No mismatch found in this payload. This is scoped review evidence, not a universal safety guarantee or signature.

## Recovery and continuation

**Changed evidence:** A nested call grants an additional unlimited allowance to a different spender absent from the intent.

**Useful response:** Return intent mismatch and identify the extra spender/unlimited grant. Require a corrected payload and fresh review of that exact payload; do not approve because the main swap matches.

If an existing compatible provider can supply the missing observation within the user's scope, perform that read and resume this same task. Otherwise deliver the supported partial result and name the exact missing observation. Do not end at generic setup advice or install another stack by default. An uncertain write requires reconciliation through its existing identity before retry decisions.
