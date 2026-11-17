# Stream invariants

Model snapshots and deltas explicitly.

## Required fields

Every normalized event carries network, subscription, DEX, market or user, receive time, source time, snapshot flag, stable identifier, and raw payload reference.

## Connection state

Use a state machine: `connecting`, `subscribed`, `snapshotting`, `live`, `gapped`, `backfilling`, `stopped`. Expose it to consumers. No consumer may interpret `gapped` as a quiet market.

## Recovery

- Heartbeat and detect silent connections.
- On reconnect, resubscribe and fetch a fresh REST snapshot.
- Backfill fills, funding, and orders from the last durable cursor where endpoints allow it.
- Deduplicate overlap by trade ID, client order ID, order ID, and event identity.
- Treat book state as invalid after a gap until a complete snapshot arrives.
- Record uncovered intervals as unknown.

## Backpressure

Bound queues and report drops. Coalesce only event types whose semantics permit it, such as replacing a newer full-state snapshot. Never coalesce fills or order transitions without durable deduplication.

## Write isolation

Stream handlers publish facts and alerts. They never call the exchange write client directly. Any action enters the same intent, risk, approval, send-ledger, and reconciliation path as a human request.
