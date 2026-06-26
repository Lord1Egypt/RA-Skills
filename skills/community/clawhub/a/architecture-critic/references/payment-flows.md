# Payment Flows Checklist — Architecture Critic

Payment logic is where AI-generated code fails silently and catastrophically. These checks are mandatory for any build that touches charges, subscriptions, or billing.

---

## 🔏 Stripe Webhook Validation

- [ ] **Signature verified** — `stripe.webhooks.constructEvent(payload, sig, webhookSecret)` on every webhook; raw body passed (not parsed JSON)
- [ ] **Per-environment webhook secrets** — production and staging have separate webhook secrets; never share
- [ ] **Webhook secret in env vars** — `STRIPE_WEBHOOK_SECRET` set in Vercel/environment; not hardcoded
- [ ] **Early return on signature failure** — webhook handler returns 400 immediately on signature mismatch; no partial processing
- [ ] **Webhook idempotency** — handler checks if event already processed before acting (use event ID as idempotency key)
- [ ] **Relevant events only** — handler ignores event types it doesn't handle; no silent failures on unexpected events

---

## 🔁 Idempotency Key Usage

- [ ] **Idempotency keys on charge creation** — `stripe.paymentIntents.create({ idempotencyKey: ... })` for every charge attempt
- [ ] **Key generation strategy** — keys are deterministic from the business action (e.g., `order-${orderId}-attempt-${attemptNumber}`)
- [ ] **Retry behavior** — client retries use the same idempotency key; never generate a new key on retry
- [ ] **Key expiry awareness** — Stripe idempotency keys expire after 24h; keys not reused across different business actions
- [ ] **Database-level idempotency** — for non-Stripe operations, idempotency enforced via unique constraint or conditional insert

---

## ⚡ Race Conditions in Charge Flows

- [ ] **No double-charge on concurrent requests** — charge creation uses optimistic locking or database-level unique constraint on pending order
- [ ] **Webhook processing serialized per entity** — concurrent webhooks for the same subscription/customer don't create duplicate records
- [ ] **Status check before charge** — verify order/subscription status before initiating charge; don't re-charge a paid order
- [ ] **Webhook vs API response race** — system handles case where webhook arrives before the API call that created the resource returns
- [ ] **Concurrent subscription updates** — upgrade/downgrade concurrent with payment doesn't create inconsistent plan state

---

## 🔄 Subscription Lifecycle Edge Cases

- [ ] **`customer.subscription.updated` handled** — plan changes (upgrade/downgrade) update local DB immediately
- [ ] **`customer.subscription.deleted` handled** — cancellation revokes access; no grace period leakage
- [ ] **`invoice.payment_failed` handled** — access suspended or dunning flow triggered; not silently ignored
- [ ] **`invoice.payment_succeeded` handled** — subscription active state confirmed and renewed in local DB
- [ ] **Reactivation flow** — reactivating a canceled subscription creates new subscription record; old one not reused
- [ ] **Trial end handling** — `customer.subscription.trial_will_end` and post-trial payment failure both handled
- [ ] **Proration clarity** — upgrade/downgrade proration behavior documented and tested; unexpected credit/charge explained
- [ ] **Subscription pause** — if pause is supported, paused state doesn't allow feature access
- [ ] **Portal vs API cancellation** — cancellation via Stripe Customer Portal fires same webhook as API cancellation; single handler covers both

---

## 💸 Refund & Dispute Handling

- [ ] **Refund flow** — `stripe.refunds.create()` used; refund recorded in local DB immediately
- [ ] **Partial refund accounting** — partial refunds update balance correctly; idempotency applied
- [ ] **`charge.dispute.created` webhook** — dispute flagged in system; access suspended pending resolution if policy requires
- [ ] **`charge.refunded` webhook** — refund status synced from webhook, not just optimistic API response
- [ ] **No double-refund vulnerability** — refund endpoint checks if charge already refunded before calling Stripe

---

## 🔒 PCI Scope Considerations

- [ ] **No raw card data touches server** — card numbers, CVVs, expiry never sent to backend; Stripe.js / Elements handles client-side tokenization
- [ ] **PaymentIntent on server** — `PaymentIntent` created server-side with amount; amount not passed from client
- [ ] **Amount validation** — server validates amount against its own calculation; never trusts client-supplied price
- [ ] **PCI SAQ A compliance** — if using Stripe Checkout or Elements exclusively, SAQ A scope applies (minimal)
- [ ] **TLS enforced** — all payment pages and API routes served over HTTPS only; HTTP redirects to HTTPS

---

## 🧪 Test vs Live Key Segregation

- [ ] **Environment-specific keys** — `STRIPE_SECRET_KEY` is test key in dev/staging, live key in production only
- [ ] **No live keys in CI/CD** — CI pipelines use test keys; live keys never in GitHub Actions secrets or test environments
- [ ] **Test mode webhooks** — staging webhook endpoint configured in Stripe test mode dashboard; separate from production
- [ ] **Test card library** — team knows to use `4242 4242 4242 4242` for success, `4000 0000 0000 9995` for decline
- [ ] **Live key access control** — live Stripe secret key access limited to production environment and key holders only
- [ ] **Key prefix validation** — code asserts `sk_live_` prefix in production, `sk_test_` in other environments

---

## ⚠️ Common AI-Generated Payment Anti-Patterns

| Anti-Pattern | Risk | Correct Approach |
|---|---|---|
| Amount passed from client | Client manipulates price to $0.01 | Server calculates amount from product lookup |
| No webhook signature check | Anyone can fake a payment success event | `constructEvent()` always, raw body required |
| Synchronous charge in API handler | Double-charge on retry/timeout | Idempotency key + status check before charge |
| Access granted on PaymentIntent creation | PaymentIntent ≠ successful payment | Grant access only on `payment_intent.succeeded` webhook |
| Single webhook secret for all environments | Test events fire production access grants | Per-environment secrets, always |
| Missing `invoice.payment_failed` handler | Unpaid subscriptions keep access indefinitely | Suspend or queue dunning on first failure |
