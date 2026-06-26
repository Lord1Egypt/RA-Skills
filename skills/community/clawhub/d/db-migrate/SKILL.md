---
name: db-migrate
description: Deep database migration workflow—expand/contract, backward-compatible deploys, backfills, locking risks, and verification. Use when changing production schemas safely with zero or low downtime.
---

# DB Migrations

Production schema changes fail when old and new code disagree during rollout. Prefer **expand/contract**: add compatible changes first, remove old shapes later.

## When to Offer This Workflow

**Trigger conditions:**

- ALTER TABLE in production; large table rewrites
- Blue/green deploys coupled to schema state
- Need zero-downtime or low-downtime migrations

**Initial offer:**

Use **six stages**: (1) classify change, (2) expand phase, (3) backfill & dual-write, (4) flip reads/writes, (5) contract phase, (6) verify & rollback). Confirm database engine (PostgreSQL, MySQL, etc.).

---

## Stage 1: Classify Change

**Goal:** Additive vs destructive; lock risk (full table rewrite vs instant metadata change).

**Exit condition:** Migration labeled as expand or contract with risk notes.

---

## Stage 2: Expand Phase

**Goal:** Add nullable columns or new tables without breaking currently deployed code.

### Practices

- Avoid DEFAULT clauses that lock large tables badly on some engines (use phased backfill instead)

---

## Stage 3: Backfill & Dual-Write

**Goal:** Throttled batch backfill; dual-write old and new representations during transition when needed.

---

## Stage 4: Flip Reads/Writes

**Goal:** Deploy code that reads new columns only after backfill completes; use feature flags for staged rollout.

---

## Stage 5: Contract Phase

**Goal:** Drop old columns only after no code references them (search repo, logs, feature usage).

---

## Stage 6: Verify & Rollback

**Goal:** Monitor errors, slow queries, replication lag; rollback = redeploy previous app version + avoid destructive steps until stable.

---

## Final Review Checklist

- [ ] Change classified; expand/contract path clear
- [ ] Additive migrations before dependent code
- [ ] Backfill throttled and verified
- [ ] Read/write cutover sequenced with flags
- [ ] Contract only after references gone
- [ ] Monitoring and rollback tested

## Tips for Effective Guidance

- Long transactions on migrations can cause outages—chunk work.
- Use online schema tools (pt-online-schema-change, etc.) when appropriate.

## Handling Deviations

- SQLite/embedded engines have different locking—validate per engine.
