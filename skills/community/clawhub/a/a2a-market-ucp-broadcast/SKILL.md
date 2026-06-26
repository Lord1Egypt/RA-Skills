---
name: a2a-market-ucp-broadcast
description: Implement UCP broadcast of buyer intents to eligible nodes, including message signing, routing, and ack handling. Use when building universal commerce protocol publish/subscribe behavior for matching and quote intake.
---

# a2a-Market UCP Broadcast

Define the transport and protocol shell for intent broadcast in UCP.

Current status: framework release for registration. Prioritize interoperability contracts over optimization.

## Scope
- Build intent payload schema and canonical signing routine.
- Broadcast to eligible nodes and track delivery acknowledgements.
- Feed response stream into quote intake service.

## Suggested Project Layout
- `app/protocol/ucp/intent_message.py`
- `app/protocol/ucp/signer.py`
- `app/application/services/broadcast_service.py`
- `app/infrastructure/ws/ucp_gateway.py`

## Minimum Contracts (MVP P0)
1. `build_intent(payload)` normalizes and version-tags message.
2. `sign_intent(intent, private_key)` returns detached signature object.
3. `broadcast(intent_id, target_nodes)` returns dispatch receipt ids.
4. `collect_acks(intent_id, timeout_ms)` returns per-node ack status.

## Event Mapping
- Emit `INTENT_CREATED` before dispatch.
- Emit `INTENT_BROADCASTED` after fan-out completes.
- Emit `NODE_RESPONDED` when quote/ack arrives.

## Guardrails
- Keep canonical JSON serialization deterministic for signing.
- Record per-node retry counters and stop after configured threshold.
- Attach protocol version in every envelope.

## Implementation Backlog
- Add adaptive node selection based on reputation percentile.
- Add dead-letter handling for nodes with repeated timeouts.

## Runtime Implementation
- Status: implemented in local runtime package.
- Primary code paths:
- `runtime/src/protocol/ucp-client.js`
- `runtime/src/application/market-agent.js`
- Validation: covered by `runtime/tests` and `npm test` in `runtime/`.
