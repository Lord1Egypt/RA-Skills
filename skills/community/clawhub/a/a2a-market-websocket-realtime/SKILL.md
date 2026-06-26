---
name: a2a-market-websocket-realtime
description: Deliver real-time websocket updates for intent, quote, negotiation, order, and payment events. Use when implementing push channels, subscription authorization, and connection/session lifecycle for market clients.
---

# a2a-Market WebSocket Realtime

Set up realtime delivery skeleton for buyer and operator clients.

Current status: publishable framework with stable event contracts, not full scale tuning.

## Scope
- Define channel naming and auth guard for buyer, node, and admin roles.
- Push canonical domain events with predictable payload shape.
- Manage reconnect semantics and last-event cursor replay.

## Suggested Project Layout
- `app/interfaces/ws/socket_gateway.py`
- `app/application/services/realtime_service.py`
- `app/infrastructure/ws/connection_registry.py`
- `app/infrastructure/cache/replay_cursor_store.py`

## Minimum Contracts (MVP P0)
1. `subscribe(channel, cursor)` validates permission and registers stream.
2. `publish_event(channel, event)` fans out to online subscribers.
3. `resume(channel, cursor)` replays missed events within retention window.
4. `heartbeat(connection_id)` updates liveness and cleanup scheduling.

## Required Event Coverage
- `INTENT_CREATED`
- `QUOTE_RECEIVED`
- `NEGOTIATION_STARTED`
- `ORDER_CREATED`
- `PAYMENT_SUCCEEDED`

## Guardrails
- Keep payloads versioned and backward compatible.
- Limit per-connection queue to prevent memory blowups.
- Drop unauthorized subscription attempts with structured error codes.

## Implementation Backlog
- Add presence channels and typing/status hints for negotiation UI.
- Add regional relay nodes for cross-region latency reduction.

## Runtime Implementation
- Status: implemented in local runtime package.
- Primary code paths:
- `runtime/src/interfaces/ws/event-bus.js`
- Validation: covered by `runtime/tests` and `npm test` in `runtime/`.
