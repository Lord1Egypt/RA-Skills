---
name: a2a-market-stripe-payment
description: Integrate Stripe payment intents, capture flow, and webhook reconciliation for A2A orders. Use when implementing payment authorization/capture, refund path, and payment status propagation into the order lifecycle.
---

# a2a-Market Stripe Payment

Create the Stripe payment integration skeleton for order settlement.

Current status: registration scaffold with stable payment contracts and webhook map.

## Scope
- Create payment intent from negotiated order terms.
- Capture or cancel payments based on order transitions.
- Reconcile webhook events with internal order state.

## Suggested Project Layout
- `app/integrations/stripe/stripe_client.py`
- `app/application/services/payment_service.py`
- `app/interfaces/api/payment_routes.py`
- `app/infrastructure/tasks/stripe_webhook_worker.py`

## Minimum Contracts (MVP P0)
1. `create_payment_intent(order_id, amount, currency)` returns provider intent id + client secret.
2. `capture_payment(provider_intent_id)` captures authorized funds.
3. `cancel_payment(provider_intent_id)` voids uncaptured authorization.
4. `handle_webhook(event)` verifies signature and upserts payment status.

## Event Mapping
- Emit `ORDER_CREATED` when payment intent is created.
- Emit `PAYMENT_SUCCEEDED` when capture confirms.
- Emit payment-failed incident event when authorization/capture fails.

## Guardrails
- Verify webhook signature before parsing payload.
- Enforce idempotency key for create/capture endpoints.
- Keep provider status mapping table explicit and versioned.

## Implementation Backlog
- Add partial refund and dispute webhook handling.
- Add multi-currency routing and fee optimization.

## Runtime Implementation
- Status: implemented in local runtime package.
- Primary code paths:
- `runtime/src/integrations/stripe/stripe-payment-service.js`
- Validation: covered by `runtime/tests` and `npm test` in `runtime/`.
