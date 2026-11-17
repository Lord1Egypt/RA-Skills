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

**Request:** Check my existing Base RPC tool so I can read a balance. Do not install anything.

**Available evidence:** Synthetic discovered read-only tool supports chain identity and balance. Chain identity reports 8453, matching requested Base. Balance read for supplied account at block 123 returns 2 ETH. Observation time is 2026-09-09T12:00:00Z, observed head block time is 2026-09-09T11:59:55Z, age 5 seconds within the supplied 60-second freshness limit. No signer or paid service is configured.

**Read sequence:** Discover the existing capability schema, verify chain identity, then perform the requested balance read and retain its block/time; finish the original task after readiness succeeds.

**Completed answer:** Existing tool is ready for the requested Base balance read: chain 8453, block 123, balance 2 ETH, observed at 2026-09-09T12:00:00Z and fresh within the supplied 60-second limit. Report successful read and read-only scope; signer readiness is untested and unnecessary for this task.

## Recovery and continuation

**Changed evidence:** Endpoint instead returns chain ID 1 before the balance read.

**Useful response:** Report chain mismatch, do not label an Ethereum balance as Base. Select another already configured compatible Base tool if available, otherwise identify the exact endpoint correction needed.

If an existing compatible provider can supply the missing observation within the user's scope, perform that read and resume this same task. Otherwise deliver the supported partial result and name the exact missing observation. Do not end at generic setup advice or install another stack by default. An uncertain write requires reconciliation through its existing identity before retry decisions.
