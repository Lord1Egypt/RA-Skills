---
name: data-pipelines
description: Deep data pipeline workflow—ingestion, orchestration, idempotency, data quality, SLAs, observability, and lineage. Use when building batch/stream pipelines, debugging job failures, or hardening ETL/ELT.
---

# Data Pipelines

Pipelines fail on silent schema drift, partial writes, and unclear ownership. Design for at-least-once delivery, idempotent sinks, and observable stages.

## When to Offer This Workflow

**Trigger conditions:**

- Batch or streaming ingestion (Kafka, Fivetran, Airflow, Dagster, Spark, etc.)
- Late data, backfills, or schema changes breaking jobs
- SLA misses on freshness or row counts

**Initial offer:**

Use **six stages**: (1) requirements & SLAs, (2) source contracts, (3) transforms & idempotency, (4) orchestration & dependencies, (5) quality & monitoring, (6) lineage & operations). Confirm batch vs stream and cloud stack.

---

## Stage 1: Requirements & SLAs

**Goal:** Freshness (latency), completeness expectations, cost ceiling, failure tolerance (quarantine vs stop-the-line).

**Exit condition:** SLA table: pipeline → metric → threshold.

---

## Stage 2: Source Contracts

**Goal:** Schema versioning; CDC vs snapshot pulls; API rate limits.

### Practices

- Raw landing zone immutable; curated layers downstream

---

## Stage 3: Transforms & Idempotency

**Goal:** Deterministic transforms; upsert keys; partition strategy for rewinds.

### Practices

- Watermark progress for incremental loads

---

## Stage 4: Orchestration & Dependencies

**Goal:** Clear DAG; retry policy; backfill without double counting; SLA miss alerts.

---

## Stage 5: Quality & Monitoring

**Goal:** Data quality checks (null spikes, row bounds, referential checks); metrics on lag, duration, error rate.

---

## Stage 6: Lineage & Operations

**Goal:** Column-level lineage where valuable; on-call runbook; ownership per pipeline.

---

## Final Review Checklist

- [ ] SLAs and failure policy explicit
- [ ] Source contracts and schema evolution path
- [ ] Idempotent writes and checkpointing
- [ ] Orchestration with retries and safe backfill
- [ ] Data quality checks and alerts
- [ ] Lineage and ownership documented

## Tips for Effective Guidance

- Separate compute from storage cost awareness for large shuffles.
- Pair with **etl-design** for batch patterns and **message-queues** for streaming handoffs.

## Handling Deviations

- Single-script pipelines: still document inputs, outputs, and schedule.
