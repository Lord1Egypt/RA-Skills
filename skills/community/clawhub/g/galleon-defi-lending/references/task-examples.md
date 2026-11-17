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

**Request:** Compare a 30-day supply of 10,000 USDC. Use my existing providers and exclude rewards.

**Available evidence:** Fresh supplied observations: market A base APR 5%, total entry/exit cost 8 USDC; B base APR 4.5%, cost 2 USDC. Both meet the supplied liquidity and risk constraints. Simple interest, ACT/365; rates may change.

**Read sequence:** Read market identity, base rate methodology, liquidity and total costs at aligned observation times. Apply the requested horizon before ranking headline rates.

**Completed answer:** A: 10,000 × 0.05 × 30/365 - 8 = 33.10 USDC. B: 10,000 × 0.045 × 30/365 - 2 = 34.99 USDC. B leads by 1.89 USDC at unchanged rates. Recommend B for this comparison; this is an estimate, with no transaction prepared.

## Recovery and continuation

**Changed evidence:** B now lacks a fresh liquidity read; A is unchanged.

**Useful response:** Keep both rate calculations, mark B liquidity unverified, and request that one read through an available compatible tool before recommending executable allocation.

If an existing compatible provider can supply the missing observation within the user's scope, perform that read and resume this same task. Otherwise deliver the supported partial result and name the exact missing observation. Do not end at generic setup advice or install another stack by default. An uncertain write requires reconciliation through its existing identity before retry decisions.
