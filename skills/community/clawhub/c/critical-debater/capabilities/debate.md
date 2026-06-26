# Capability: Full Debate Orchestration

## Purpose

Run a complete multi-round adversarial debate from topic to final report. This is the top-level entry point that chains all other capabilities.

## Inputs

| Parameter | Required | Default | Description |
|---|---|---|---|
| topic | Yes | - | The debate topic / motion |
| rounds | No | 3 | Number of debate rounds (1-5) |
| depth | No | standard | quick / standard / deep |
| mode | No | balanced | balanced / red_team |
| domain | No | general | geopolitics / tech / health / finance / philosophy / culture / general |
| output_format | No | full_report | full_report / executive_summary / decision_matrix |
| language | No | bilingual | en / zh / bilingual |
| speculation_level | No | moderate | conservative / moderate / exploratory |
| evidence_refresh | No | hybrid | upfront_only / per_round / hybrid |
| focus_areas | No | [] | User-defined dimensions to focus on |

## Execution Flow

### Phase 1: Initialization

1. Run `scripts/init-workspace.sh <workspace_dir> <topic> <rounds>` to create directory structure
2. Write complete `config.json` with all parameters (DebateConfig schema)
3. Execute `source-ingest.md` — broad initial evidence gathering (round=0)
4. Execute `freshness-check.md` — classify evidence tracks and apply freshness rules
5. Verify minimum evidence count (based on depth: quick=5, standard=10, deep=15)
6. Update `config.json`: status = "evidence_gathered"

### Phase 2: Debate Rounds (for each round N = 1..R)

**Step 2a: Per-Round Evidence Refresh** (if evidence_refresh == "per_round" OR ("hybrid" AND N > 1))
1. Read `judge_ruling.json` from round N-1 (if exists)
2. Extract search focus from: mandatory_response_points, causal_validity_flags, contested claims
3. Execute `source-ingest.md` with focused queries driven by judge feedback
4. Execute `freshness-check.md` to re-evaluate ALL evidence
5. Log: `per_round_evidence_ingest`

**Optional Step**: For `depth=deep`, execute `evidence-verify.md` after freshness check for thorough cross-source verification before debaters begin their turns.

**Step 2b: Parallel Pro + Con**
1. Launch Pro-Debater and Con-Debater in parallel using `spawn_role`
2. Both execute `debate-turn.md` with their respective side
3. Both read: evidence_store, claim_ledger, round N-1 data (if N>1)
4. Neither sees the other's CURRENT round arguments

**Step 2c: Validate Outputs**
1. Run `scripts/validate-json.sh` on both pro_turn.json and con_turn.json
2. For N>1: Check that mandatory response points from judge are addressed
3. If validation fails: re-prompt agent (max 2 retries)

**Step 2d: Judge Audit**
1. Execute `judge-audit.md` — Judge reads BOTH turns + evidence_store + claim_ledger
2. Judge writes `judge_ruling.json`
3. Validate with `scripts/validate-json.sh`

**Step 2e: Post-Round Processing**
1. Execute `claim-ledger-update.md` — extract new claims, apply judge verdicts
2. Merge `new_evidence` from BOTH turns into evidence_store (tag discovered_by, dedupe by url+hash)
3. Log: `evidence_merged_from_turn`, round summary
4. Update config.json: current_round=N, status="round_N_complete"

### Phase 3: Final Output

1. Execute `final-synthesis.md` — read all data, generate report
2. Write `reports/final_report.json` and `reports/debate_report.md`
3. Validate with `scripts/validate-json.sh`
4. Update config.json: status = "complete"

### Phase 4: Scheduled Refresh (Optional)

If user agrees, create a 6-hour cron to re-run SourceIngest + FreshnessCheck. If evidence states changed, regenerate report.

## Completion Marker

Output `DONE:debate` when the full debate is complete.

## Error Handling

- Search returns no results → broaden keywords, try alternatives; if still empty, note "insufficient evidence"
- Agent produces invalid JSON → re-prompt with explicit structure (max 2 retries)
- Agent skips mandatory response point → re-prompt with missed point (max 2 retries), then log "unaddressed"
- WebFetch fails → retry once, skip source, never block debate for one source
