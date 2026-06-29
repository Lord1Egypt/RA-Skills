# Report Contract

This markdown contract is authoritative for BigDeal Supplier Finder reports. Use it when writing or reviewing report fields, runtime profiles, or evidence admissibility.

Every report must include the fields below. Preserve these field names exactly.

## Required Fields

- `execution_metadata` — profile, runtime capabilities, started_at, finished_at, elapsed_seconds, rounds_completed, stage_records, stop_reason, limits_hit, and all counters.
- `execution_limit_audit` — hard limits, skipped external actions, rate or fetch caps, timeout status, and any budget constraints that shaped the run.
- `summary` — high-level outcome: candidate count, source categories covered, top gaps, and whether expansion was needed.
- `source_map` — URL-backed discovery surfaces that list, index, or aggregate multiple potential suppliers.
- `supplier_candidates` — evidence-bound supplier entities with required candidate fields and at least one admissible evidence link.
- `search_result_signals` — raw search results used as query fuel, not evidence.
- `source_attempts` — fetch or inspection attempts with status, reason, and provenance.
- `queries_tried` — executed query combinations, source category targets, and runtime search context.
- `query_suggestions` — next-search fuel for uncovered regions, source categories, or product terms.
- `gaps` — missing evidence, restricted sources, failed attempts, uncovered surfaces, or runtime capability limits.
- `next_steps` — bounded follow-up search or review steps, including deferred provider, browser, credential, session, or live boundaries when relevant.
- `risk_notice` — evidence and sourcing boundary notice; the report is discovery support, not a procurement recommendation, trust score, due-diligence result, or production readiness proof.
