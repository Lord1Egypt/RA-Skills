# FDE project-state contract

## Purpose

`fde-project.json` is the current snapshot; `fde-events.jsonl` is its append-only event history. Neither stores complete customer material or replaces stage artifacts. The snapshot answers “where are we?” and the event log answers “how did we get here?”

Create state only for end-to-end work, continuation, multi-person handoffs, audits, or rollback. A one-off specialist task does not require it.

## Top-level fields

| Field | Meaning |
|---|---|
| `schema_version` | Contract version, currently `1.0` |
| `revision` | Monotonically increasing snapshot revision |
| `project` | Project identity, scenario, mode, and status |
| `current_stage` | Current primary stage, 1–8; other stages may still run in parallel |
| `stages` | Status, gates, artifact, version, owner, and blockers for all eight stages |
| `decisions` | Material decisions and their rationale |
| `risks` | Open risks affecting scope, operation, or value |
| `next_action` | The one prioritized next action, owner, and completion condition |

Allowed stage states are `not_started`, `in_progress`, `blocked`, `passed`, `failed`, and `skipped`. `passed` means the evidence, responsibility, executability, and risk gates all passed—not merely that a file exists. A failed run and its artifact remain in history.

Use artifact paths relative to the state file. Record a concrete accountable owner, retain only unresolved blockers, and close blockers through decisions. Stages 4 and 5 may proceed in parallel after their prerequisites are stable; independent external artifacts may also justify a later stage, but the decision or skip rationale must be recorded.

## Commands

```text
node scripts/project-state.js init --file <project-directory/fde-project.json> --project-id <ID> --name <name> --mode end_to_end
node scripts/project-state.js set-stage --file <file> --stage 1 --status passed --artifact golden-outputs/01-problem-discovery.md --version v1.0 --owner FDE --gates pass --actor xukun --reason "Problem discovery passed joint review"
node scripts/project-state.js set-next --file <file> --skill fde-engagement-charter --owner "Business lead" --condition "Confirm success criteria and customer inputs" --actor xukun --reason "Problem discovery passed its quality gates"
node scripts/project-state.js add-decision --file <file> --id DEC-001 --summary "POC remains read-only" --status confirmed --actor xukun
node scripts/project-state.js status --file <file>
node scripts/project-state.js history --file <file>
node scripts/project-state.js validate --file <file>
```

Each mutation appends actor, reason, changes, revision, and snapshot SHA-256 to `fde-events.jsonl`. Scripts validate structure and continuity, not business truth.

## Update discipline

1. Set a stage to `in_progress` when work starts.
2. Set it to `blocked` with blocker and owner when required evidence is missing.
3. Set it to `passed` only after review, with artifact, version, and all gates recorded.
4. Preserve failed POC or adoption attempts and route to the earliest stage needing correction.
5. Update one prioritized `next_action` at the end of each cycle.
6. Never store secrets, complete customer data, personal data, or restricted content.
7. Never edit previous event lines; append a correction referencing the original event.
