# Deterministic snippet ID assignment (Context Pipeline v1)

Goal: keep snippet IDs (`S1..Sn`) stable across runs for easier debugging/testing.

Recommended procedure:

1) Collect candidate snippets with scores.
2) Apply deterministic caps in order:
   - per-file cap
   - daily-log cap
   - global top-K cap
3) Dedupe:
   - exact dedupe key: `path:start_line-end_line`
   - if semantic/overlap dedupe is used, resolve ties deterministically (higher score → path → start_line).
4) Sort final snippets by stable comparator:
   - source group priority (topics → dashboards → daily logs)
   - score (desc)
   - path (asc)
   - start_line (asc)
5) Assign IDs in that final order: `S1..Sn`.

Optional: add `stable_id` (hash) per snippet for resilience to ordering shifts.
