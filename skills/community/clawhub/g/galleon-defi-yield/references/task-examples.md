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

**Request:** Compare 10,000 USDC for 30 days, excluding incentives. I must withdraw on day 30.

**Available evidence:** Vault base APR 6%, simple ACT/365, 10 USDC total costs; withdrawal available at day 30. PT matures day 90 and advertises 8% implied yield; no day-30 executable exit quote or depth supplied.

**Read sequence:** Read asset/share units, base return basis, withdrawal conditions and all costs; for PT read maturity and a horizon-matched early-exit quote.

**Completed answer:** Vault estimate: 10,000 × 0.06 × 30/365 - 10 = 39.32 USDC net interest. PT maturity yield cannot establish day-30 proceeds. Prefer the vault among evidenced options; its variable rate remains an assumption.

## Recovery and continuation

**Changed evidence:** Vault withdrawals become queued past day 30 and PT still has no early-exit quote.

**Useful response:** Neither option now has evidenced liquidity by the deadline. Retain the economic estimate but withdraw the liquidity recommendation and identify each missing exit condition.

If an existing compatible provider can supply the missing observation within the user's scope, perform that read and resume this same task. Otherwise deliver the supported partial result and name the exact missing observation. Do not end at generic setup advice or install another stack by default. An uncertain write requires reconciliation through its existing identity before retry decisions.
