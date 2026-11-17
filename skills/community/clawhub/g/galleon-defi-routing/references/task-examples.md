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

**Request:** Compare these bridge routes for the same input. Max cost 10 USDC. Use my available tools.

**Available evidence:** Both quotes spend 1,000 USDC and have sufficient destination gas. A minimum net received 994 USDC, including a 4 USDC bridge fee and 2 USDC gas paid from input. B minimum net received 992 USDC, including all costs. Both meet deadline and freshness constraints.

**Read sequence:** Compare exact input, minimum net output, separately paid fees, destination gas and deadlines; normalize included versus additional costs.

**Completed answer:** A has 6 USDC total loss from input, B 8 USDC. Choose A with minimum 994 USDC received; both meet the 10 USDC budget. The nested fee breakdown is already included and is not deducted again. This comparison does not submit a route.

## Recovery and continuation

**Changed evidence:** A source receipt succeeds but destination receipt is absent; status is pending and user asks whether to retry.

**Useful response:** Report source confirmed, destination pending, route not reconciled. Track the same bridge message/route identifier and destination balance; do not submit a duplicate route.

If an existing compatible provider can supply the missing observation within the user's scope, perform that read and resume this same task. Otherwise deliver the supported partial result and name the exact missing observation. Do not end at generic setup advice or install another stack by default. An uncertain write requires reconciliation through its existing identity before retry decisions.
