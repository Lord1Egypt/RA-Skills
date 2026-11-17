# Money and entitlements

Fires: when the app sells purchases, subscriptions, credits or plan limits

Leading word: **truth table**. Every entitlement state against what the app actually unlocks.

Artifact: the entitlement truth table. Rows: purchased, trial, trial expired, renewed, grace period, billing retry, cancelled but active, expired, refunded, revoked, family-shared, restored on a new device, reinstalled, offline, signed into another account, sandbox build. Columns: what the user paid for, what the code unlocks, where the code decides.

- **truth-table**: Every row where the unlock and the payment disagree is a finding: paid but locked, or free but unlocked.
- **entitlement-source**: Server-verified receipts or store notifications are the truth; a local flag is a cache. Look for entitlement read from local storage, a plan column the client can write, and checks scattered across screens instead of one place.
- **counter-integrity** (when there are usage counters, credits or quotas): For each scan, credit, usage or pack counter: can it go negative, decrement twice on a retry, reset on reinstall, reset on a time zone or clock change, be raced from two devices, or be farmed with new accounts? Is the limit enforced on the server? Fix family: one atomic server statement such as `update … set n = n - 1 where n > 0 returning n`, keyed by an idempotency key.
- **store-webhooks** (when a store or payment provider sends server notifications): Signature verified; deduplicated by event id; correct when events arrive out of order (cancel before purchase, refund before renewal); every event type handled or explicitly ignored.
- **money-arithmetic**: Floats for money, rounding at each step instead of once, currencies mixed, prices hardcoded instead of read from the store's localized product.
- **paywall-honesty**: Everything the paywall and receipts promise (limits, trial length, what unlocks, how to cancel) matches what the code enforces.

Confirm with sandbox or test-mode purchases only.

Done: every truth-table row has an answer, and every counter has an answer for each failure in counter-integrity.
