---
name: a2a-supermarket
description: Unified entry skill for RealMarket A2A commerce workflows. Supports seller product publish and buyer product discovery through UCP market connectivity, plus end-to-end order orchestration modules.
---

# a2a-supermarket

Act as the integrated entrypoint for the A2A market runtime.

Current status: orchestrator scaffold for early launch. This skill routes tasks to the right module-level skills and keeps contracts consistent.

## Direct Marketplace Actions (Implemented)

This skill now supports two direct role-based actions:

1. Seller publishes products to market (`role=seller`).
2. Buyer discovers products from market (`role=buyer`).

## Executable Entrypoint

Run from skill directory:

```bash
node src/cli/index.js --role seller --domain 127.0.0.1:3456 --name "Skill Chair" --price-minor-units 12999 --category Furniture
```

```bash
node src/cli/index.js --role buyer --domain 127.0.0.1:3456 --query chair --limit 10
```

```bash
node src/cli/index.js --role buyer --domain 127.0.0.1:3456 --all true
```

The CLI also accepts stdin JSON with the same fields.
Output is JSON only:
- seller: publish result (`mode=seller_publish`)
- buyer: discovery result (`mode=buyer_discover`, supports `all/listAll` for full listing)

## Routing Map
- Identity and login: route to `a2a-market-google-oauth`.
- Intent broadcast and node response: route to `a2a-market-ucp-broadcast`.
- Stake lock and penalty policy: route to `a2a-market-stake-freeze`.
- Multi-round negotiation: route to `a2a-market-acp-lite-negotiation`.
- Compute accounting and debit/freeze: route to `a2a-market-compute-ledger`.
- Payment authorization and capture: route to `a2a-market-stripe-payment`.
- Order lifecycle and transitions: route to `a2a-market-order-state-machine`.
- Realtime event fanout: route to `a2a-market-websocket-realtime`.

## End-to-End Flow (MVP)
1. Authenticate actor and create session.
2. Build buyer intent and broadcast via UCP.
3. Collect quotes and start ACP-lite negotiation.
4. Freeze stake and reserve compute budget before commit.
5. Create order and payment intent.
6. Capture payment after final acceptance.
7. Transition order through fulfillment to completion.
8. Emit events to websocket, billing, reputation, and logs.

## Canonical Event Backbone
- `INTENT_CREATED`
- `INTENT_BROADCASTED`
- `NODE_RESPONDED`
- `QUOTE_RECEIVED`
- `NEGOTIATION_STARTED`
- `RISK_FLAGGED`
- `ORDER_CREATED`
- `PAYMENT_SUCCEEDED`
- `ORDER_COMPLETED`
- `REPUTATION_UPDATED`

## Interface Contracts
- Keep request and event payloads versioned.
- Enforce idempotency keys on write operations.
- Use deterministic timestamps and correlation ids.
- Propagate a single `trace_id` across all modules.

## Coordination Rules
- Prefer module skill execution for domain-specific logic.
- Keep this entry skill focused on orchestration and contract governance.
- If submodule behavior conflicts, prioritize order state machine safety and financial correctness.

## Implementation Backlog
- Add global policy engine for cross-module risk checks.
- Add replay/debug mode for full transaction traces.
- Add SLA dashboard hooks for timeouts and retries.

## Runtime Implementation
- Status: implemented in local runtime package.
- Primary code paths:
- `runtime/src/application/market-agent.js`
- `runtime/src/cli/index.js`
- `runtime/tests/market-agent.e2e.test.js`
- `a2a-supermarket/src/cli/index.js`
- Validation: covered by `runtime/tests` and `npm test` in `runtime/`.
