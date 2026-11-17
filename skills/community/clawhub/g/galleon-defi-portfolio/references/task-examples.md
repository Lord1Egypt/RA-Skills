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

**Request:** Give me a compact USD portfolio report and flow-adjusted change.

**Available evidence:** Consistent synthetic snapshot: wallet USDC 2,000; ETH 3,000 USD; vault receipt worth 5,000 USD includes 4,000 underlying and 1,000 accrued value already in receipt valuation; debt 1,500 USD. Prior NAV 7,500 USD; external deposit 500 USD; no withdrawals.

**Read sequence:** Read scoped accounts and valuation times; map receipt claims to underlying, remove overlaps, subtract debt and external flows.

**Completed answer:** Gross assets 10,000 USD; liabilities 1,500 USD; NAV 8,500 USD. Economic change = 8,500 - 7,500 - 500 = +500 USD. Receipt underlying is not added again. This is dollar change, not a time-weighted return or claim about realized profit.

## Recovery and continuation

**Changed evidence:** The vault price is stale and no compatible fresh valuation tool is available.

**Useful response:** Report known gross assets 5,000 USD less known debt 1,500 = 3,500 USD plus unvalued vault exposure. Do not report complete NAV or complete period change; identify the missing receipt valuation.

If an existing compatible provider can supply the missing observation within the user's scope, perform that read and resume this same task. Otherwise deliver the supported partial result and name the exact missing observation. Do not end at generic setup advice or install another stack by default. An uncertain write requires reconciliation through its existing identity before retry decisions.
