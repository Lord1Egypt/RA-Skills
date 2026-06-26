# Capability: Claim Ledger Update

## Purpose

Extract new claims from debate turns, apply judge verification results, and maintain the claim state machine.

## Inputs

| Parameter | Required | Default | Description |
|---|---|---|---|
| workspace_dir | Yes | - | Path to debate workspace |
| round | Yes | - | Current round number |

## Context Files to Read

1. `rounds/round_{N}/pro_turn.json` — Pro's arguments
2. `rounds/round_{N}/con_turn.json` — Con's arguments
3. `rounds/round_{N}/judge_ruling.json` — Judge's verification results
4. `claims/claim_ledger.json` — existing claims

## Execution Steps

### 1. Extract New Claims

From both pro_turn.json and con_turn.json, extract each argument as a ClaimItem:

```json
{
  "claim_id": "clm_{round}_{side}_{seq}",
  "round": N,
  "speaker": "pro" | "con",
  "claim_type": "fact" | "inference" | "analogy",
  "claim_text": "The claim statement",
  "evidence_ids": ["evi_xxx", ...],
  "status": "unverified",
  "last_verified_at": null,
  "judge_note": null,
  "mandatory_response": false,
  "conflict_details": []
}
```

### 2. Apply Judge Verification Results

For each entry in `judge_ruling.verification_results`:
1. Find the matching claim in the ledger
2. Update `status` according to the state machine transitions:
   - `unverified → verified`: Cross-source confirmed
   - `unverified → contested`: Sources conflict
   - `unverified → stale`: Current-state source expired
   - `verified → contested`: New contradicting evidence
   - `verified → stale`: Fact-track source expired
   - `contested → verified`: Resolution with new evidence
   - `contested → stale`: All sources expired
   - `stale → verified`: Fresh confirming source found
3. Update `judge_note` with judge's reasoning
4. Update `last_verified_at` timestamp

### 3. Apply Critical Rules

- **Reasoning-track claims** (claim_type=analogy OR evidence_track=reasoning): NEVER auto-transition to `stale`
- **Twitter-only claims**: NEVER set to `verified` unless independent non-social source confirms

### 4. Handle Conflict Details

When judge flags a claim as `contested`, populate `conflict_details`:
```json
{
  "source_a": {"evidence_id": "evi_xxx", "position": "Source A claims..."},
  "source_b": {"evidence_id": "evi_yyy", "position": "Source B claims..."},
  "divergence_point": "The specific disagreement",
  "judge_assessment": "Judge's evaluation"
}
```

### 5. Mark Mandatory Response Claims

If judge's `mandatory_response_points` reference specific claims, set `mandatory_response: true` on those claims.

### 6. Write Updated Ledger

Write back to `claims/claim_ledger.json`.

### 7. Audit Log

For each status change, log via `scripts/append-audit.sh`:
```json
{"timestamp":"...","action":"claim_status_changed","details":{"claim_id":"clm_xxx","old_status":"unverified","new_status":"verified","round":N}}
```

## Completion Marker

Output `DONE:claim_ledger_update` when complete.
