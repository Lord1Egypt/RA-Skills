# Stream discipline

## State model

Treat a stream as `connecting`, `snapshot`, `live`, `gapped`, `reconciling`, or `stopped`. Only `live` data inside its freshness bound can produce `not-triggered`.

## Start

1. Record network, subscriptions, user address, DEX, and start time.
2. Fetch a REST snapshot for stateful subjects.
3. Subscribe and identify which first messages are snapshots.
4. Deduplicate by stable identifiers such as trade ID, order ID, client order ID, sequence, or timestamp plus payload identity.
5. Declare live only after snapshot and stream positions agree or their ordering is reconciled.

## Heartbeat and freshness

Send the documented ping and require a recent pong or data heartbeat. Enforce connection, subscription, message, and condition-evaluation freshness separately. A running process with an old last message is not healthy.

## Reconnect

On disconnect:

1. Enter `gapped` and stop clean-negative alerts.
2. Record the last confirmed event time and identifiers.
3. Reconnect and resubscribe.
4. Backfill the gap with REST history where available.
5. Deduplicate overlapping events.
6. Fetch current account and order snapshots.
7. Return to `live` only after reconciliation.

If the available history cannot cover the gap, report the interval as unknown.

## Event rules

- Do not treat the initial user-fills snapshot as new fills.
- Open candles update repeatedly; label intrabar evaluation or wait for close.
- Book updates need a fresh snapshot after a gap unless the feed supplies complete sequencing and replay.
- WebSocket acknowledgements prove subscription acceptance, not data freshness.
- Callbacks may alert or persist evidence. They must not invoke an exchange write.

Respect current connection, subscription, message, in-flight, IP, and address limits from the official rate-limit page. Back off on rate limits instead of increasing concurrency.

## User-defined watches

For a requested watch, retain exact account/market, condition and units, evaluation
cadence or event source, freshness limit, end time or stop rule, notification policy,
and last delivered event ID. Reuse an existing suitable scheduler or stream exposed
by the harness; a new daemon, trading provider or LLM call for every tick is optional.
Use deterministic comparisons for simple thresholds and reserve model interpretation
for the resulting evidence or ambiguous conditions.

Create or update a watch only through a real supported scheduling capability. Record
its returned identifier and active state before claiming it is running. If no such
tool exists, complete a one-time observation and return the unscheduled watch spec.
An open conversation or a proposed script is not a running monitor.

Unless the user requests periodic reports, notify on meaningful state changes,
incidents or required input. Deduplicate repeated alerts and record recovery from
unavailable state. Stop or expiry ends notifications, not exchange protection or
positions. No watch condition authorizes a trading action.
