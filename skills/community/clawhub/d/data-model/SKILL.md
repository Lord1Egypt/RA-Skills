---
name: data-model
description: Deep data modeling workflow—grain, facts and dimensions, keys, slowly changing dimensions, normalization trade-offs, and analytics query patterns. Use when designing warehouse/analytics models or reviewing star/snowflake schemas.
---

# Data Model

Analytics models succeed when **grain** is explicit, **keys** are stable, and **slowly changing dimensions** are chosen deliberately—not “star schema by default.”

## When to Offer This Workflow

**Trigger conditions:**

- Designing a warehouse, lakehouse, or BI layer
- Confusion on **one row per what**; duplicate counts in reports
- Refactoring dimensional models for performance or clarity

**Initial offer:**

Use **six stages**: (1) business questions & grain, (2) conformed dimensions, (3) facts & measures, (4) dimensions & SCD types, (5) keys & integrity, (6) performance & evolution). Confirm **tooling** (dbt, dimensional DW, BigQuery, etc.).

---

## Stage 1: Business Questions & Grain

**Goal:** **Grain** = the atomic row: e.g., “one line item per order per day” not “sort of per order.”

### Practices

- List **questions** the model must answer; **derive** grain from **smallest** needed detail

**Exit condition:** One sentence grain per fact table.

---

## Stage 2: Conformed Dimensions

**Goal:** **Same** customer/product definitions across facts—**shared** dimension tables or **SCD** policy aligned.

---

## Stage 3: Facts & Measures

**Goal:** **Additive** vs **semi-additive** vs **non-additive** measures documented (balances, distinct counts).

### Practices

- **Degenerate** dimensions vs junk dimensions—**avoid** **wide** **fact** **sprawl** **without** **reason**

---

## Stage 4: Dimensions & SCD Types

**Goal:** **SCD1** overwrite vs **SCD2** history with `valid_from`/`valid_to` vs **SCD3** limited history—**match** **compliance** **and** **reporting** **needs**.

---

## Stage 5: Keys & Integrity

**Goal:** **Surrogate** keys in facts; **natural** keys preserved as attributes; **referential** integrity strategy in the warehouse layer.

---

## Stage 6: Performance & Evolution

**Goal:** **Partition** and **cluster** keys for large facts; **late-arriving** facts policy; **version** **dims** when schema evolves.

---

## Final Review Checklist

- [ ] Grain explicit per fact table
- [ ] Conformed dimensions planned
- [ ] Measure additivity documented
- [ ] SCD strategy per critical dimension
- [ ] Keys and late-arriving data handled

## Tips for Effective Guidance

- **Fan traps** and **chasm traps** in BI—flag when joining across facts incorrectly.
- **Snapshot** fact tables for **point-in-time** balances vs **transaction** facts.

## Handling Deviations

- **Event**-only pipelines: still model **curated** **dimensions** **for** **analysis**, not only raw JSON.
