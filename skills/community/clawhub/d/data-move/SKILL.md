---
name: data-move
description: Deep data migration workflow—scope, mapping, validation, batching and ordering, dual-write and cutover, rollback, and reconciliation. Use when moving tenants, bulk backfills, or changing stores without losing trust in data correctness.
---

# Data Move

Data migration fails in **silent corruption**, **ordering bugs**, and **unclear cutover**. Treat it as **ETL with production risk**: explicit mapping, checkpoints, and **reconciliation** against sources of truth.

## When to Offer This Workflow

**Trigger conditions:**

- Moving data between databases, regions, or tenants
- Large backfills after schema changes
- **Zero** or **minimal** downtime requirements

**Initial offer:**

Use **seven stages**: (1) scope & invariants, (2) source/target mapping, (3) batching & idempotency, (4) validation rules, (5) execution strategy (big bang vs phased), (6) cutover & rollback, (7) reconciliation & sign-off). Confirm **volume**, **downtime** budget, and **compliance** (PII, audit).

---

## Stage 1: Scope & Invariants

**Goal:** Define **what** moves, **what** must never diverge, and **ordering** dependencies (foreign keys, references).

### Questions

1. **Cutover** moment: read-only window vs dual-write?
2. **Immutable** identifiers: preserve primary keys or remap with mapping tables?
3. **Deletes**: soft-delete vs hard-delete semantics in target

**Exit condition:** Written invariants (e.g., “every migrated row has `legacy_id` for traceability”).

---

## Stage 2: Source/Target Mapping

**Goal:** Field-level mapping document; **transforms** (timezone, encoding, rounding); **defaults** for nulls.

### Practices

- **Surrogate keys** generated deterministically or via mapping table
- Document **one-way** vs **bi-directional** sync if any

---

## Stage 3: Batching & Idempotency

**Goal:** Jobs **restartable**; **same** input yields **same** output (idempotent writes or upsert keys).

### Practices

- **Checkpoint** by primary key or updated_at watermark
- **Throttle** to protect source and target DB

---

## Stage 4: Validation Rules

**Goal:** Row counts, checksums, **sample** joins, **business** invariants (sums, balances).

### Practices

- **Shadow** compare: run parallel queries on old vs new for critical aggregates

**Exit condition:** Validation checklist signed before cutover.

---

## Stage 5: Execution Strategy

**Goal:** Phased by tenant/region vs single window—**risk** vs **complexity** trade-off.

### Patterns

- **Dual-write** then backfill then flip reads
- **Blue/green** tables with rename swap

---

## Stage 6: Cutover & Rollback

**Goal:** **Runbook**: who flips DNS/config, **order** of steps, **rollback** triggers (error rate, failed checks).

### Practices

- **Feature flags** for read path to new store
- **Keep** rollback script **tested** in staging

---

## Stage 7: Reconciliation & Sign-off

**Goal:** Post-cutover **24–72h** monitoring; **reconciliation** job scheduled; **support** playbook for edge cases.

---

## Final Review Checklist

- [ ] Invariants and mapping documented
- [ ] Idempotent batches with checkpoints
- [ ] Validation and shadow checks passed
- [ ] Cutover/rollback runbook tested
- [ ] Reconciliation after go-live

## Tips for Effective Guidance

- **Never** assume “batch job finished” = correct—**prove** with checks.
- **Clock skew** and **timezone** bugs are classic—call them out in transforms.
- Pair with **db-migrate** for schema timing vs data movement.

## Handling Deviations

- **Small** one-off SQL: still document mapping and run counts before/after.
