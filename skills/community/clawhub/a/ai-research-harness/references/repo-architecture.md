# Repo Architecture & Governance

> Distilled from real-world AI-native research execution practice

## Three-Layer Repo Positioning

Research work naturally splits into three layers with different ownership and lifecycles:

| Layer | Role | Source of Truth | Should NOT Contain |
|-------|------|-----------------|-------------------|
| `thinking-space/` | Research direction | claims, decisions, hypotheses | raw logs, routine code |
| `execution-layer/` | Experiment execution | briefs, logs, results, drafts | claim reframing, unverified claims as facts |
| `code-workshop/` | Runnable artifacts | code, packages, reproducible tools | research governance, long prose |

**Information flow**: thinking-space defines direction → execution-layer generates evidence → code-workshop provides tools → insights flow back as proposals.

## Phase + Module Contract Dual Governance

Phase controls **time progress** (Phase 0→4). Module controls **asset quality**.

```text
Phase       controls progress over time
Module      controls asset correctness
Manifest    controls experiment facts
Validator   controls local correctness
Checkpoint  controls phase summary
```

### Seven Stable Modules

These modules appear in most research execution repos, regardless of domain:

| Module | Typical Assets | Local Checks |
|--------|---------------|-------------|
| Literature | survey, paper notes, research intake | citation status, source verification |
| Assets | schema, taxonomy, knowledge artifacts | schema compliance, ID validity, evidence status |
| Tasks | test tasks, gold checklist, rubric | task schema, coverage, checklist completeness |
| Runner | prompts, LLM client, run config | output schema, group settings, prompt version |
| Scoring | scorer, metrics, exports | metric definitions, score range, version metadata |
| Results | raw outputs, scores, manifest | run coverage, status, retry records |
| Writing | method, experiment, results drafts | claim evidence, missing refs, critical checks |

## Module CONTRACT.md Template

Every core module gets a contract with 9 fixed sections:

```markdown
# Module Contract: <Name>

## Purpose
## Inputs
## Outputs
## Canonical Files
## Allowed Changes
## Forbidden Changes
## Invariants
## Local Validator
## Downstream Consumers
```

Example invariants for the Assets module:
- Every artifact passes schema validation
- Every taxonomy ID exists in the canonical taxonomy file
- Every artifact has an evidence_registry entry
- Artifacts marked "verified" must have a source citation
- **Derived representations** (vector indexes, graph relations, ontology projections) are projections from canonical artifacts, not replacements. Each derived representation must preserve: source artifact IDs, evidence IDs, projection rules, projection version, and retrieval/traversal logs

## Experiment Manifest

`experiments/results/manifest.csv` is the canonical run ledger.

Key columns: run_id, wave, task_id, group, model, prompt_version, runner_version, scorer_version, schema_version, raw_output_path, score_path, status, retry_of, git_commit

**Rules**:
- Raw outputs only append, never overwrite
- Retries get new run_id + retry_of pointer
- Successful rows must have both raw_output_path and score_path
- wave/task_id/group combo must not repeat unless retry

## Local Validators

```text
scripts/validate_assets.py
scripts/validate_tasks.py
scripts/validate_runner.py
scripts/validate_scoring.py
scripts/validate_results_manifest.py
scripts/validate_repo_state.py  ← aggregator
```

Phase gate rule: `python scripts/validate_repo_state.py` must report 0 FAIL before any formal execution.

## Artifact Creation QA

Artifact quality is governed at two levels:

1. **Card-level evidence**: The card JSON has `evidence_type`, `confidence_level`, `review_status`. A card may appear structurally correct but have no traceable evidence for any individual claim.
2. **Claim-level evidence**: Each critical factual claim in a card has its own row in a claims registry (e.g., `config/card_claims.csv`) with `source_ref`, `evidence_span`, and `verification_action`.

Card-level evidence is necessary but not sufficient. Claim-level evidence is the audit trail.

### Claim-First Workflow

Never write the card text before establishing the claims. The correct order:

```text
coverage need
→ claim draft (3-5 critical claims per card)
→ source packet (find and document sources per claim)
→ claim-level evidence rows (config/card_claims.csv)
→ card JSON (projection of the claim table)
→ domain red-team review (construct validity)
→ validate_cards --strict
→ human approval for batch pattern
```

### Scaffold → Validate → Commit Micro-Cycle

1. **Scaffold**: Create the artifact from a template or taxonomy definition. Apply web search for domain-specific facts (formulas, thresholds, data specifications). Mark all claims as `candidate` evidence.
2. **Validate**: Run local validators. Common failures to watch for:
   - Unescaped special characters in JSON/YAML string values (especially Chinese quotation marks)
   - Enum values that don't match the canonical schema (check `belonging_task`, `spatial_composition`, etc.)
   - Registry sync: `literature_source`, `evidence_type`, `confidence_level`, `review_status` must match between the artifact and its registry entry
   - `related_assets` pointing to non-existent artifacts
3. **Fix**: Resolve all FAIL-level issues. WARN-level issues can remain as known gaps.
4. **Commit**: Only commit when validators pass 0 FAIL.

This pattern is especially important when creating artifacts in bulk. The temptation to create "perfect" artifacts in one pass leads to analysis paralysis. Create skeleton artifacts first (passing validators), then enrich with content in subsequent passes.

## Protected Surfaces

These require version bump + proposal, never silent change:
- **claims** — writing claims must point to evidence
- **rubric** — versioned; old scores never rescored silently
- **raw results** — append-only
- **scoring config** — metric definitions
- **schema/taxonomy** — canonical data structures

## Four Checkpoint Levels

1. **Run checkpoint** — per-run, in manifest.csv
2. **Module checkpoint** — after major module change
3. **Wave checkpoint** — after each experiment wave
4. **Phase checkpoint** — after phase gate (summarizes module checkpoints)

## Agent Onboarding

New agent reads short alignment doc, not long chat history:

```text
AGENTS.md → PLAN.md current phase → target module CONTRACT.md → target module manifest → local validator
```

Minimum file set for external AI review:
1. AGENTS.md — workspace map
2. PLAN.md — current status
3. WORKFLOW.md — execution procedure
4. config/schema.json — core data types
5. config/schema.yaml — canonical taxonomy and classification
6. experiments/briefs/*.md — experiment design
