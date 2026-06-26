# Capability: Freshness Check

## Purpose

Classify each evidence item's track (fact vs reasoning) and apply freshness rules. Update evidence_store.json with current freshness status.

## Inputs

| Parameter | Required | Default | Description |
|---|---|---|---|
| workspace_dir | Yes | - | Path to debate workspace |

## Execution Steps

### 1. Read Evidence Store

Load `evidence/evidence_store.json`.

### 2. Classify Evidence Tracks

For each item, use LLM to confirm/update `evidence_track`:
- **Fact track**: Concrete data, current-state claims, prices, statistics, event reports
  - These CAN become `stale` when the underlying fact may have changed
- **Reasoning track**: Mechanisms, causal explanations, historical patterns, theoretical frameworks
  - These are ALWAYS `timeless` — NEVER auto-degraded to `stale`

### 3. Apply Freshness Rules

For each item:

**Fact track items:**
- If `published_at` is within a reasonable window for the claim type → `current`
- If `published_at` is too old for a current-state claim → `stale`
- Use LLM judgment for the threshold — do NOT use mechanical time cutoffs
  - A stock price from yesterday is stale; a GDP figure from last quarter may still be current
  - Context matters: breaking news topics need fresher data than structural analysis

**Reasoning track items:**
- Always set to `timeless`
- NEVER transition to `stale` regardless of age

### 4. Update Evidence Store

Write updated items back to `evidence/evidence_store.json`.

### 5. Audit Log

Log via `scripts/append-audit.sh`:
```json
{"timestamp":"...","action":"freshness_check","details":{"items_checked":N,"current":X,"stale":Y,"timeless":Z}}
```

## Critical Rules

- Reasoning-track evidence is NEVER auto-degraded to `stale`
- Use semantic judgment for freshness, not mechanical time thresholds
- Re-evaluate ALL evidence each time (not just new items)

## Completion Marker

Output `DONE:freshness_check` when complete.
