# Payments, funding and recovery

Use the connected tools' current schemas and owned next actions. Preserve
amount, currency, asset, network, recipient, merchant, total debit and expiry.
Do not infer account readiness or spend authority from available balance.

## Balance and history

`get_payment_balance` returns wallet availability; activity is different.
`list_recent_transactions` is paginated agent-scoped workflow activity. Follow
the returned page/cursor unchanged with consistent limits. Even fully paginated
workflow activity can never establish settled spending or remaining allowance.
Purchases, compute, reserves, confirmed fees, refunds and other agents need
their owning operation/accounting reads. State period, timezone and scope;
without those records, report only the visible agent-scoped activity subtotal.
Use the provided money representation and formatter without floating-point
reconstruction. Unknown amounts or currencies remain unknown.

## Start the requested rail

- Crypto transfer: resolve exact recipient/address, network, asset and amount.
  For a named recipient, discover Memory before asking for an address; use a
  purpose-matched session or `begin_request_session`, then materialize the
  address, network and asset together. Memory release is not payment approval.
  Use `run_crypto_transfer` with the user's authorized debit and current schema.
- x402: a price-only request uses `quote_x402_payment`, presents the
  fee-inclusive debit/maximum and expiry, and stops. For an authorized purchase,
  obtain the exact request from current official provider documentation and
  use `run_x402_payment`. Do not pay as a probe or treat a registry description
  or historical token-label error as authority to change the request.
  After explicit acceptance of a quote, preserve its `acceptedQuoteRef`,
  original clientRequestId and exact request. The execution maximum debit may
  be tightened to the accepted fee-inclusive debit, but must remain at least
  the quoted debit and no greater than the preview maximum. Expired or changed
  terms require a fresh preview and acceptance before execution.
- Browser: `create_checkout_session` binds the exact intended checkout; it
  neither opens nor controls the merchant page. Discover saved billing roles
  through `get_memory_footprint`, supply those as ordinary fields to
  `run_browser_payment`, and collect only what remains missing. Follow
  [browser execution](browser.md) for the authorized page interaction.

Continue each run with `wait_payment` using its exact returned run identity,
cursor and next action. Approval and policy checks are owned by that run.
Do not ask for a redundant chat confirmation before or after Aftercard's
approval, repeat an approval, or replace it with a generic action request.
The host's own permissions and required confirmations still apply.

## Funding

Read current balance and `list_funding_methods` before a funding action.
Generic “top up” uses `show_topup` and its returned view/link. Use
`create_topup_link` when the user explicitly requests a link or the widget
cannot render; otherwise reuse the returned generic funding link. Use
`request_topup_addresses` or `request_funding_address` only for the requested
supported funding route. A displayed address, opened link or changed balance
does not prove a particular payment or deposit settled.

When the owning run reports required funding, retain its existing funding
gate and approval, state the shortfall/deadline and reuse the returned link.
Without such a gate, use `show_topup` once as directed. After timeout or
expiry, read that same run/request; elapsed time never permits replacement.

## Observe and recover the same operation

Use `get_payment_operation` for the exact payment and
`reconcile_payment_operation` only as directed for that operation. Do not
repeat a possibly dispatched transfer, purchase or merchant submission after
a timeout, missing output or unclear result. Preserve all operation, session,
request, approval, run and idempotency identities and unchanged retry input.

For browser results, inspect the live page and use
`record_browser_payment_result` on the original attempt as its current schema
requires. `list_card_transactions` can provide evidence for that exact card;
one incomplete page cannot establish that a charge is absent. Merchant paid
confirmation, provider processing and durable settlement must be reported as
separate observations. Verified purchased output belongs to the user; deliver
it privately, preserving provenance and any seller continuation capability.

Follow current financial and cleanup state. The legacy `freshStartAllowed`
summary alone is not task-wide permission. A separately requested additional
purchase must explicitly authorize possible duplicate charges, use fresh
identities and satisfy normal balance/approval limits. A service result that
disallows fallback cannot be bypassed by another route or client.

User cancellation preempts further payment actions. Use
`cancel_checkout_session` for the exact workflow and follow cleanup and
same-operation reconciliation. Cancellation is not proof of refund, release
or settlement. Report preserved recovery state honestly and continue normal
browsing or independently authorized work when available. Use
`fail_checkout_session` only for an open workflow when its native terminal
failure/cleanup contract directs it; preserve existing terminal outcomes.
