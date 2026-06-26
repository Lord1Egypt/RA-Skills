# Capability: Debate Turn

## Purpose

Construct a structured debate turn (arguments + rebuttals) for either Pro or Con side. Outputs a DebateTurn JSON file.

## Inputs

| Parameter | Required | Default | Description |
|---|---|---|---|
| workspace_dir | Yes | - | Path to debate workspace |
| round | Yes | - | Current round number |
| side | Yes | - | "pro" or "con" |
| topic | Yes | - | Debate topic |
| mode | No | balanced | balanced / red_team |
| speculation_level | No | moderate | conservative / moderate / exploratory |
| depth | No | standard | Controls argument count: quick=2, standard=2-4, deep=3-5 |

## Context Files to Read

1. `evidence/evidence_store.json` — all available evidence
2. `claims/claim_ledger.json` — all claims and their statuses
3. **Round 2+**: `rounds/round_{N-1}/pro_turn.json`, `con_turn.json`, `judge_ruling.json`
4. **NEVER** read current round opponent's turn file

## Execution Steps

### 1. Address Mandatory Response Points (FIRST — Non-negotiable)

For Round 2+:
- Read `judge_ruling.json` from round N-1
- Identify all `mandatory_response_points` targeting this side (or "both")
- Address EVERY mandatory point in `mandatory_responses[]`
- This MUST happen before building new arguments

### 2. Build Arguments

For each argument:
- State the claim clearly (`claim_text`)
- Classify as `fact`, `inference`, or `analogy`
- Reference specific `evidence_ids` from evidence_store
- Construct the MANDATORY 5-element reasoning chain:

```json
{
  "observed_facts": "What concrete data/events support this",
  "mechanism": "WHY does A lead to B (causal explanation)",
  "scenario_implication": "What follows IF the mechanism holds",
  "trigger_conditions": "What would ACTIVATE this scenario",
  "falsification_conditions": "What would PROVE this argument wrong"
}
```

Every factual claim MUST reference evidence_ids. No unsupported assertions.

### 3. Build Rebuttals

For Round 2+:
- Target opponent's STRONGEST arguments from previous round (not strawmen)
- Attack the causal chain — identify: correlation!=causation, reverse causality, confounding variables, unstated assumptions
- Reference evidence_ids that counter opponent's claims

### 4. Search for Supplementary Evidence

If evidence_store is insufficient for the arguments being constructed:
1. Use `search` to find additional sources
2. Normalize to EvidenceItem format
3. Include in `new_evidence[]` array in the turn output
4. Tag: `discovered_by` = side, `search_context` = "{side}_supplement"

### 5. Historical Wisdom (Optional)

Include if relevant historical parallels exist:
- `weight`: always "advisory"
- Each reference MUST include:
  - `historical_event`: Name and description
  - `era_context`: Historical background
  - `parallel_to_current`: How it parallels current topic
  - `key_differences`: Critical structural differences (REQUIRED)
  - `lesson_extracted`: The insight drawn
  - `applicability_caveat`: Limitations (REQUIRED)

### 6. Speculative Scenarios

Controlled by `speculation_level`:
- `conservative`: OMIT this section entirely
- `moderate`: 1-2 evidence-grounded scenarios
- `exploratory`: 2-4 scenarios including black swans
- Every scenario MUST include `what_would_falsify`
- `weight`: always "exploratory"

### 7. Write Output

Write to `rounds/round_{N}/{side}_turn.json` following DebateTurn schema.

### 8. Validate

Run `scripts/validate-json.sh` on the output file with schema type `{side}_turn`.

## Quality Requirements

- Minimum arguments per depth: quick=2, standard=2, deep=3
- Minimum rebuttals (Round 2+): 1
- ALL mandatory response points addressed
- ALL factual claims have evidence_ids
- ALL arguments have complete 5-element reasoning chains

## Completion Marker

Output `DONE:debate_turn_{side}` when complete.
