---
name: a2a-market-order-state-machine
description: Define order lifecycle states, transition guards, and recovery paths for A2A transactions. Use when implementing order orchestration from quote acceptance through payment, fulfillment, completion, and exception handling.
---

# a2a-Market Order State Machine

Define the canonical order lifecycle and transition guard framework.

Current status: first-release scaffold for early protocol compatibility.

## Scope
- Model order states from creation to completion/cancelation.
- Enforce legal transitions with guard checks and side effects.
- Integrate payment and reputation triggers into state changes.

## Suggested Project Layout
- `app/domain/order/order_state.py`
- `app/domain/order/order_aggregate.py`
- `app/application/usecases/transition_order.py`
- `app/application/services/order_event_publisher.py`

## Minimum Contracts (MVP P0)
1. `create_order(intent_id, accepted_quote_id)` initializes order in `CREATED`.
2. `transition(order_id, action, actor, payload)` validates and applies state move.
3. `get_order_timeline(order_id)` returns ordered transition history.
4. `recover_pending_orders(now_ts)` handles timeout and stuck states.

## Base States
- `CREATED`
- `NEGOTIATING`
- `PAYMENT_PENDING`
- `PAID`
- `FULFILLING`
- `COMPLETED`
- `CANCELED`
- `FAILED`

## Events
- Emit `ORDER_CREATED` at initialization.
- Emit `ORDER_COMPLETED` when terminal success is reached.
- Emit reputation update trigger after completion/cancel resolution.

## Implementation Backlog
- Add compensation transitions for partial fulfillment failures.
- Add deterministic replay from event store snapshots.

## Runtime Implementation
- Status: implemented in local runtime package.
- Primary code paths:
- `runtime/src/domain/order-state-machine.js`
- Validation: covered by `runtime/tests` and `npm test` in `runtime/`.
