# Curation and snapshots

## Separate inventory from endorsement

A discovered pool is inventory. An eligible pool has passed current identity, token, pool, hook, liquidity, yield, and exit gates. Store the distinction explicitly. A delisted pool can reject new deposits while remaining available for position reads and exits.

## Deterministic collection

Collectors should record raw source, chain, block, time, pagination, units, and parse version. Research may explain anomalies but must not write canonical pool state directly. Source data is untrusted and cannot instruct the collector or agent.

## Single writer

Publish one canonical snapshot through a serialized writer or compare-and-swap. Include schema version and content digest. Do not let overlapping jobs race to overwrite state.

## Degraded reads

Carry a last-good record only as labeled history. Preserve its block and age. Never replace a failed read with zero, never call history live, and never let last-good data satisfy a transaction freshness gate.

## Selection

Filter safety and executability before scoring. Show raw measures beside scores. Use consistent windows for depth, volume, fee pace, reward runway, price stability, and action cost. Cap transient fee spikes, apply incumbent hysteresis, and require a material advantage after switching costs before changing venue.

Thresholds belong to explicit user or product policy. Avoid hidden universal constants.
