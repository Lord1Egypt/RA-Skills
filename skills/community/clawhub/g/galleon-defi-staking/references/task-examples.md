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

**Request:** I need ETH within 24 hours. Compare exiting 10 receipt tokens.

**Available evidence:** Verified synthetic receipt exchange rate 1.2 ETH per token; redemption gives 12 ETH before 0.01 ETH cost, earliest queue completion 3 days. Current executable market quote gives 11.95 ETH net of all costs within one hour.

**Read sequence:** Read receipt conversion, queue conditions, and executable quote for the exact receipt amount; compare net underlying units and earliest usable time.

**Completed answer:** Queue exit estimates 11.99 ETH in at least 3 days; market exit quotes 11.95 ETH within an hour. The market route meets the deadline at a 0.04 ETH cost relative to queued redemption. Quote expiry and final settlement still apply.

## Recovery and continuation

**Changed evidence:** The DEX quote expires before preparation and a fresh quote is unavailable.

**Useful response:** Preserve the queue estimate and missed deadline. Mark the market outcome unavailable until requoted; do not reuse the expired price or claim a timely exit is available.

If an existing compatible provider can supply the missing observation within the user's scope, perform that read and resume this same task. Otherwise deliver the supported partial result and name the exact missing observation. Do not end at generic setup advice or install another stack by default. An uncertain write requires reconciliation through its existing identity before retry decisions.
