# Capability: Evidence Verify

> **Note / 说明**: This capability is NOT called in the standard orchestration flow.
> Judge-audit already performs independent verification during each round.
> This capability is available for:
> (1) Standalone evidence verification outside a debate context
> (2) Optional pre-round deep verification when `depth=deep`
> (3) Manual invocation via "verify evidence" user intent

## Purpose

Cross-source verification of evidence items. Determine corroboration status, especially for social media sources.

## Inputs

| Parameter | Required | Default | Description |
|---|---|---|---|
| workspace_dir | Yes | - | Path to debate workspace |
| evidence_ids | No | all | Specific evidence IDs to verify, or "all" |

## Execution Steps

### 1. Read Evidence Store

Load `evidence/evidence_store.json`.

### 2. Prioritize Verification

Sort items by `verification_priority`:
1. `high` — likely_unreliable social sources, critical claims
2. `medium` — needs_verification social sources
3. `low` — already from reputable sources

### 3. Cross-Source Verification

For each item to verify:
1. `search` for the core claim using different keywords than original
2. Look for independent sources (different publisher, different URL)
3. Use LLM to assess:
   - **corroborated**: 2+ independent sources confirm the same claim
   - **uncorroborated**: No independent confirmation found
   - **contradicted**: Independent source(s) directly contradict the claim

### 4. Twitter/X Special Rules

- Twitter-only claims can NEVER become `verified` status
- Must find at least one independent non-social source for corroboration
- Set `corroboration_status` based on independent source findings
- Non-Twitter sources: `corroboration_status` = null (not applicable)

### 5. Update Evidence Store

Write updated corroboration statuses back to `evidence/evidence_store.json`.

### 6. Conflict Documentation

When sources conflict, document in the evidence item or related claim:
- `source_a`: What one source says
- `source_b`: What another source says
- `divergence_point`: The specific disagreement
- Let the Judge resolve conflicts during audit

## Completion Marker

Output `DONE:evidence_verify` when complete.
