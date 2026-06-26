---
name: etl-design
description: Deep ETL/ELT design workflow—extract patterns, transforms, loading strategies, idempotency, validation, and reconciliation. Use when designing batch data flows between systems or hardening pipelines for correctness.
---

# ETL Design

ETL is **correctness under change**: schema drift, partial loads, retries, and reconciliation with upstream systems.

## When to Offer This Workflow

**Trigger conditions:**

- Batch loads into warehouse or data lake
- Choosing between CDC, snapshots, and incremental watermarks
- Missing rows, duplicates, or inconsistent aggregates downstream

**Initial offer:**

Use **six stages**: (1) source contract, (2) extract strategy, (3) transform rules, (4) load & dedupe, (5) validation, (6) operations & backfill). Confirm batch window and SLA.

---

## Stage 1: Source Contract

**Goal:** Document schema, primary keys, change indicators (`updated_at`, CDC log position), and access constraints (rate limits, read replicas).

---

## Stage 2: Extract Strategy

**Goal:** Full dump vs incremental watermark vs CDC—trade freshness, source load, and complexity.

### Practices

- CDC for large sources; snapshots for small or infrequent tables

---

## Stage 3: Transform Rules

**Goal:** Deterministic transforms; surrogate keys; business rules versioned; handling of deletes (tombstones vs hard deletes).

---

## Stage 4: Load & Dedupe

**Goal:** Upsert keys; partitions; rerunnable jobs with same batch id producing the same outcome (idempotent load).

---

## Stage 5: Validation

**Goal:** Row counts, checksums, key uniqueness, referential checks; alert on threshold breaches.

---

## Stage 6: Operations & Backfill

**Goal:** Replay by date range; monitor lag; dead-letter or quarantine bad rows with reason codes.

---

## Final Review Checklist

- [ ] Source contract and keys documented
- [ ] Extract mode matches SLA and source constraints
- [ ] Transforms deterministic and versioned
- [ ] Idempotent load strategy
- [ ] Validation and reconciliation defined

## Tips for Effective Guidance

- Plan for late-arriving facts and slowly changing dimensions in analytics paths.
- Pair with **data-pipelines** for orchestration and monitoring.

## Handling Deviations

- Near-real-time: document micro-batch or streaming semantics separately.
