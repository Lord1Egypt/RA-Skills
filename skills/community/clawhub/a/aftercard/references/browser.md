# Browser checkout and merchant accounts

The current host owns navigation, live-page understanding, screenshots,
ordinary/protected input, challenges, submission and observation. Aftercard
supplies financial authority and authorized values; it does not operate a
second browser. Use only the host's documented APIs and actual permissions.
If browser access or required payment input is unavailable or prohibited,
report that limitation and preserve the operation. A skill cannot override it.

After a payment-method or form-revealing transition, discard stale targets
and inspect the rendered page again. Hidden DOM/accessibility presence is not
visible availability. Use screenshots and normal visual reasoning throughout,
including after filling. Handle frames, intermediate controls, field errors
and challenges through normal host recovery while keeping the same checkout.
Do not replace a payment to repair a form or install another controller.

Verify merchant, item, amount, currency, total and billing roles against the
current task and approved operation. Only the unchanged approved checkout
and its exact final action are authorized. A material change requires the
owning service's new decision/approval path; never reuse the earlier approval
for a different merchant or amount. Respect explicit user “do not buy”.

Authorized one-time card and Memory values may be visible to the model and
host. Use them only through host-supported targeted input for the approved
tab and task, including documented per-key input or a host REPL wrapper when
required. This does not provide transcript isolation. Do not quote values,
save them in helper scripts/files/logs or exported evidence, inject credentials
with arbitrary page-evaluation code, or send them to another site/message.

## Login, signup and forms

Inspect the page and URL-scoped saved `login.website` fields before asking
whether an account exists. Use [Memory](memory.md) to discover and release
exact fields, or `resolve_browser_form_values` to collect missing values
securely. Reuse the saved account. Signup is a separate user-intended action
when needed, not permission to accept unrelated terms or create identities.

For SSO, OTP, passkey, QR or a challenge requiring a human, use one supported
handoff and keep the same cart/task. Do not expose credentials or claim the
handoff succeeded before observing the result. After interruption, recover
the actual current page and operation; do not reconstruct a checkout from
stale handles or repeat a possibly submitted purchase.

Non-payment form preparation does not authorize submitting it. Resolve saved
details and missing fields through the same Memory workflow. Saved card,
default-card changes, recurring authorization and the purchase are distinct
actions. A one-time checkout card is not a permanent merchant-locked card;
claim merchant restrictions or approval enforcement for later charges only
when verified provider support establishes both. Never make a test charge or
silently delete a saved card or transfer subscriptions.

The agent's ready email is the default checkout receipt address unless the
user chose another or the merchant already fixed/submitted one. Do not
substitute an account's personal identity email without that intent. Report
merchant confirmation promptly while distinguishing unresolved provider
processing/settlement. Follow [payment recovery](payments.md) for uncertainty.
