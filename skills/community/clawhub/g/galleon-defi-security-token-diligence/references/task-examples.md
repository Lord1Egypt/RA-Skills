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

**Request:** Check only whether this token has a mutable transfer fee.

**Available evidence:** Synthetic pinned verified source at block 500: transfer calls feeBps, owner-only setter accepts 0 through 1000 basis points; current value 100. Ownership is active. No liquidity or holder data supplied.

**Read sequence:** Trace transfer fee usage to its setter and access control, pin source/deployment/block and distinguish current value from owner capability.

**Completed answer:** Finding FEE-001: transfer fee is currently 1% and the active owner can raise it to 10%, based on the pinned setter bound and transfer usage at block 500. Scope covers fee mutability only; liquidity and holder distribution were not evaluated. No broader token safety verdict.

## Recovery and continuation

**Changed evidence:** Only ABI exposes setFee but implementation and setter bounds are unavailable.

**Useful response:** Report fee mutability as unverified from ABI alone; request verified implementation and control state. Do not infer a 10% cap or malicious behavior from the function name.

If an existing compatible provider can supply the missing observation within the user's scope, perform that read and resume this same task. Otherwise deliver the supported partial result and name the exact missing observation. Do not end at generic setup advice or install another stack by default. An uncertain write requires reconciliation through its existing identity before retry decisions.
