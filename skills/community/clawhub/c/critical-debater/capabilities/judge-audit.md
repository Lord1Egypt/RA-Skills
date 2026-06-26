# Capability: Judge Audit

## Purpose

Impartial evaluation of a debate round. The Judge independently verifies claims, audits causal chains, evaluates analogies, and produces a structured ruling.

## Inputs

| Parameter | Required | Default | Description |
|---|---|---|---|
| workspace_dir | Yes | - | Path to debate workspace |
| round | Yes | - | Current round number |

## Context Files to Read

1. `rounds/round_{N}/pro_turn.json` — Pro's arguments this round
2. `rounds/round_{N}/con_turn.json` — Con's arguments this round
3. `evidence/evidence_store.json` — all evidence
4. `claims/claim_ledger.json` — all claims and statuses

## IMPARTIALITY RULES (NON-NEGOTIABLE)

- NEVER express preference for either side
- Evaluate REASONING QUALITY, not which conclusion you favor
- Apply IDENTICAL standards to both sides
- If one side is clearly stronger, state it neutrally with evidence

## Execution Steps

### 1. Independent Source Verification (CRITICAL)

For EACH factual claim made by both sides:
1. Use `search` to independently verify the claim
2. Do NOT rely on debaters' citations alone
3. Check if the evidence actually supports what the debater claims it supports
4. Assign status: `verified`, `contested`, `unverified`, or `stale`
5. Document reasoning for each verification result

### 2. Causal Chain Audit

For each argument's reasoning chain, check for:
- **Correlation != Causation**: Is a causal mechanism actually established?
- **Reverse Causality**: Could the effect actually cause the supposed cause?
- **Confounding Variables**: Are there unstated variables that better explain the relationship?
- **Unstated Assumptions**: What assumptions are silently required for the chain to hold?

Flag issues with severity: `critical`, `moderate`, `minor`

### 3. Analogy Audit

For each historical analogy used:
- Verify >= 2 similarities cited
- Verify >= 1 structural difference acknowledged
- Check content share < ~15% of total argument
- Grade relevance: `strong_parallel`, `moderate_parallel`, `weak_parallel`
- Grade honesty: `honest`, `partially_honest`, `misleading`

### 4. Mandatory Response Points

Generate 2-5 points that MUST be addressed next round:
- Each point targets `pro`, `con`, or `both`
- Include clear `reason` for why this needs response
- Focus on: unaddressed weaknesses, unresolved contradictions, evidence gaps

### 5. Round Summary

Write a neutral summary of key developments:
- What new arguments were introduced
- What claims were successfully rebutted
- What evidence gaps remain
- NO scoring, NO preference expression

### 6. Write Output

Write to `rounds/round_{N}/judge_ruling.json` following JudgeRuling schema:

```json
{
  "round": N,
  "verification_results": [...],
  "causal_validity_flags": [...],
  "mandatory_response_points": [...],
  "historical_wisdom_assessment": [...],
  "round_summary": "..."
}
```

### 7. Validate

Run `scripts/validate-json.sh` on the output file with schema type `judge_ruling`.

## Model Tier

This capability MUST use `deep` tier model for best reasoning quality.

## Completion Marker

Output `DONE:judge_audit` when complete.
