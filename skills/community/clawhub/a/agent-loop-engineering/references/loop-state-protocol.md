# Loop State Protocol

Use project-local `Docs/` as the durable state source. Do not use global memory as the primary project state.

## Files

Canonical files are written in the names below. Legacy aliases may be read for migration only.

| Canonical file | Legacy aliases to read |
| --- | --- |
| `Docs/TARGET.md` | `Docs/PROJECT_TARGET.md` |
| `Docs/STATUS.md` | `Docs/PROJECT_STATUS.md` |
| `Docs/COMPLETED.md` | `Docs/COMPLETED_JOBS.md` |
| `Docs/PENDING.md` | `Docs/PENDING_JOBS.md` |
| `Docs/NEXT_ACTIONS.md` | `Docs/NEXT_STEPS.md`, `Docs/SCHEDULE.md` |
| `Docs/HANDOFF.md` | none |

If aliases are found, migrate once, record the mapping in `Docs/EVALUATION.md`, then write only canonical files.

If a later agent writes a legacy alias again after migration, treat it as a compatibility warning: read it once, merge any new information into the canonical file, record the warning in `Docs/EVALUATION.md`, and keep writing only canonical files. Do not delete the legacy file without user approval.

### `Docs/TARGET.md`

Store the stable goal contract. `TARGET.md` is the source of truth for what the project is trying to do and what is out of scope. Keep success criteria high-level here; put executable checks in `ACCEPTANCE.md`.

```markdown
Status: Confirmed

# Project Target

## User Goal

## Success Criteria
- [High-level outcome, not a test command]

## Non-Goals
- [ ]

## Acceptance Evidence
- Automatic verification:
- Functional verification:
- Review/documentation evidence:

## Failure Examples
- [What would prove this is not complete]

## Last Confirmed
YYYY-MM-DD
```

Terminology aliases: `Non-Goals`, `Out of scope`, and `Scope / Out of scope` mean the same boundary field. Preserve the canonical `Non-Goals` heading when rewriting `TARGET.md`.

### `Docs/ACCEPTANCE.md`

Store the executable completion contract. `ACCEPTANCE.md` is the source of truth for the completion gate and must be derived from `TARGET.md`.

```markdown
# Acceptance Contract

## Must Pass
- [ ] Requirement:
  Evidence required:
  Current evidence:

## Should Pass
- [ ] Requirement:
  Evidence required:
  Current evidence:

## Manual Confirmation Needed
- [ ] Item:
  Reason:

## Known Exclusions
- Item:
  Reason:
```

Use this evidence format when possible:

```text
Current evidence: [type] command/scenario -> result; evidence path or short snippet; timestamp
```

Examples:

- `Current evidence: [automatic] npm test -> passed; .agent/logs/test-2026-06-09.log; 2026-06-09T10:20:00Z`
- `Current evidence: [functional] POST /api/login invalid password -> 401 with error code AUTH_INVALID; .agent/logs/api-login.json; 2026-06-09T10:25:00Z`
- `Current evidence: [review] SKILL.md frontmatter has only name + description; manual structural review; 2026-06-09T10:30:00Z`

### `Docs/STATUS.md`

Keep only the latest working state and recent update history. This schema is compatible with daily workflow checkpoints as long as the compressed context remains present:

```markdown
# Project Status

## Current State

## Latest Verification
- Command/result:
- Functional check:
- Evidence path:

## Risks

## Compressed Context
- Target: 1-2 lines
- Decisions: up to 5 bullets
- Completed: up to 5 bullets
- Pending: up to 5 bullets
- Blockers: up to 5 bullets
- Files touched: paths only
- Commands/tests: command + result + short error summary
- Evidence paths: log, screenshot, fixture, or report path
- Immediate next action: exactly one action
```

### `Docs/COMPLETED.md`

Append user-visible or verification-backed completed units. Keep entries concise; archive by month if the file becomes too large. `COMPLETED.md` is for acceptance items, user-visible deliverables, or durable milestones. `STATUS.md` -> `Completed` is only the latest compressed summary, capped to about 5 bullets.

```markdown
# Completed Work

## YYYY-MM-DD
- Completed:
  Evidence:
  Related acceptance item:
  Files:
```

### `Docs/PENDING.md`

Keep the active queue:

```markdown
# Pending Work

## Immediate
- [ ]

## Later
- [ ]

## Blockers and Decisions
- [ ]
```

### `Docs/NEXT_ACTIONS.md`

Keep one continuation path:

```markdown
# Next Actions

## Immediate Next Action
1.

## Stop/Resume Notes
- Stop state:
- Resume command or entry point:
- Needed human input:
```

### `Docs/LOOP_CONFIG.md`

Store loop policy:

```yaml
protocol_version: 1
runner: generic
max_loops: 5
max_consecutive_failures: 2
max_runtime_minutes: 60
max_context_files_per_loop: 8
max_recent_loop_records: 5
require_double_evidence_for_done: true
core_verification: test
max_compressed_context_lines: 40
log_directory: .agent/logs
allow_parallel_tasks: false
progress_signals:
  - new passing verification
  - narrower failing scope
  - changed root cause with evidence
  - implemented accepted next action
verification_commands:
  test: null
  typecheck: null
  build: null
  lint: null
  functional: null
allow_project_dependency_install: true
allow_project_config_changes: true
allow_system_install: false
allow_secret_access: false
allow_production_data_access: false
allow_destructive_changes: false
```

`core_verification` defaults to `test`. If no test command exists, use the first available command in this order: `typecheck`, `build`, `lint`, `functional`, `review`.

`progress_signals` define what counts as measurable progress. If no signal appears and the core verification still fails, increment `max_consecutive_failures`.

Default signal thresholds:

- `new passing verification`: at least one verification command that failed or was unavailable in the previous loop now passes.
- `narrower failing scope`: failing test/check count decreases by at least 1 and no new failure category appears.
- `changed root cause with evidence`: error type, file path, line number, stack frame, or failing scenario changes with a recorded command/log/evidence path.
- `implemented accepted next action`: the exact `Docs/NEXT_ACTIONS.md` immediate action was completed and verified, even if a later core check still fails.

Progress examples:

- Positive `narrower failing scope`: unit tests drop from 10 failing tests in 3 modules to 3 failing tests in 1 module, with no new failure type.
- Negative `narrower failing scope`: failures drop from 10 to 8 but add a new build failure category.
- Positive `changed root cause`: failure changes from `auth token missing` to `session fixture expired`, with a log path or stack trace summary.
- Negative `changed root cause`: the error wording changes but points to the same file, line, and failing assertion.

`allow_*` fields may make defaults stricter, but they must not loosen the hard stop rules in `environment-escalation.md` unless the user explicitly approves that run and the approval is recorded in `Docs/STOP_RULES.md` under `Overrides`.

`max_consecutive_failures` counts consecutive loops where `core_verification` fails and no measurable progress signal is present. Non-core verification failures are recorded in `EVALUATION.md` but do not consume this budget unless the project defines a stricter rule.

### `Docs/STOP_RULES.md`

Store project-specific stop rules and overrides. Project-specific rules may be stricter than the skill defaults, but not looser unless the user explicitly approves.

```markdown
# Stop Rules

## Hard Stops
- Rule:
  Reason:
  Human decision needed:

## Budget Stops
- max_loops:
- max_consecutive_failures:
- max_runtime_minutes:

## Project-Specific Stops
- Rule:
  Severity: hard / soft
  Reason:

## Overrides
- Override:
  Approved by:
  Approval source:
  Expiration:
  Scope:
  Cannot override:
```

`STOP_RULES.md` can only add stricter project rules by default. Overrides must be narrow, time-limited, and cannot allow secret exposure, production data access, destructive Git operations, or irreversible changes without explicit human confirmation for that specific run.

### `Docs/EVALUATION.md`

Append each evaluation:

```markdown
## YYYY-MM-DD HH:mm Loop Evaluation

- State: Continue / Done / Done with Risk / Blocked
- Target alignment:
- Success criteria status:
- Automatic verification:
- Functional verification:
- Risks:
- Stop rule triggered:
- Acceptance evidence updated:
- Next action:
```

Archive older evaluation entries to `Docs/archive/EVALUATION_YYYY-MM.md` when the file grows beyond the latest 10 loop evaluations plus any active investigation entries. Keep a short index entry in `EVALUATION.md` with the archived date range.

### `Docs/LOOP_RUNS.jsonl`

Append one JSON object per loop. Keep it concise:

```json
{"run_id":"2026-06-09T17:30:00+08:00","state":"continue","goal_snapshot":"...","action":"...","verification":["typecheck passed"],"risks":[],"next_action":"..."}
```

Required fields: `run_id`, `state`, `action`.

Optional fields: `timestamp`, `goal_snapshot`, `verification`, `risks`, `files_touched`, `next_action`, `progress_signal`, `progress_signal_evidence`, `core_verification`, `failure_count`.

When `progress_signal` is present, `progress_signal_evidence` must contain a one-line reason or evidence path.

Use ISO 8601 timestamps with timezone. Prefer UTC (`Z`) unless the project config requires a local timezone.

Examples:

```json
{"run_id":"2026-06-09T10:30:00Z","timestamp":"2026-06-09T10:30:00Z","state":"continue","action":"fixed login validation branch","verification":["test failed: 2 auth tests remain"],"progress_signal":"narrower failing scope","progress_signal_evidence":"failed tests decreased from 5 to 2 with no new category","core_verification":"test","failure_count":0,"files_touched":["src/auth/login.ts"],"next_action":"fix remaining expired-session test"}
```

```json
{"run_id":"2026-06-09T11:00:00Z","timestamp":"2026-06-09T11:00:00Z","state":"blocked","action":"attempted API verification","verification":["requires production API key"],"risks":["secret required"],"core_verification":"functional","failure_count":1,"next_action":"human provides approved staging credential flow"}
```

Archive older records when record count exceeds `max_recent_loop_records` plus the number needed for the current investigation. Move older records to `Docs/archive/LOOP_RUNS_YYYY-MM.jsonl`.

### `Docs/HANDOFF.md`

Create `HANDOFF.md` when any of these is true:

- The agent session is ending while state is `Continue`.
- The user requests a checkpoint, wrap-up, or handoff.
- Context is about to reset or cannot be safely kept in the active loop.
- State is `Done`, `Done with Risk`, or `Blocked` and the next reader needs a standalone summary.

```markdown
# Handoff

## Reason

## Current State

## Target and Acceptance Summary

## Key Decisions

## Completed Work

## Pending Work

## Blockers and Risks

## Verification Evidence

## Files Touched

## Next Agent Instructions
```

## Conflict Resolution

Use this priority when files disagree:

```text
TARGET.md -> ACCEPTANCE.md -> STATUS.md -> PENDING.md -> NEXT_ACTIONS.md -> LOOP_RUNS.jsonl
```

If `TARGET.md` and `ACCEPTANCE.md` disagree, stop before coding and reconcile them. If lower-priority files disagree, update them to match the higher-priority file and record the correction in `EVALUATION.md`.

## Write Rules

- Append to `LOOP_RUNS.jsonl` and `EVALUATION.md`.
- Update `STATUS.md` compressed context every loop.
- Update touched `ACCEPTANCE.md` items every loop by filling `Current evidence`, or by noting the missing evidence for blocked criteria.
- Append completed, evidence-backed work to `COMPLETED.md`.
- Preserve unresolved blockers in `PENDING.md`.
- Keep only the current continuation path in `NEXT_ACTIONS.md`.
- Never store secrets, full private documents, large logs, or full chat transcripts.
- Prefer writing state files in this order at loop end: `EVALUATION.md`, `STATUS.md`, `ACCEPTANCE.md`, `COMPLETED.md`, `PENDING.md`, `NEXT_ACTIONS.md`, `LOOP_RUNS.jsonl`.
- If a previous write was interrupted, recover by reading `TARGET.md` and `ACCEPTANCE.md` first, then reconciling lower-priority files.
- If `EVALUATION.md` has a partial final entry, `NEXT_ACTIONS.md` is empty, or `LOOP_RUNS.jsonl` has invalid JSON on the last line, treat the previous write as interrupted. Re-read `TARGET.md` and `ACCEPTANCE.md`, then reconcile `STATUS.md`, `PENDING.md`, `NEXT_ACTIONS.md`, and `LOOP_RUNS.jsonl` from the highest-priority complete evidence. Record the recovery in `EVALUATION.md`.

## Git and Persistence Policy

- Version `Docs/TARGET.md`, `Docs/ACCEPTANCE.md`, `Docs/STATUS.md`, `Docs/PENDING.md`, `Docs/NEXT_ACTIONS.md`, `Docs/STOP_RULES.md`, `Docs/COMPLETED.md`, and `Docs/HANDOFF.md` when they are part of project coordination.
- Version `Docs/EVALUATION.md` and `Docs/LOOP_RUNS.jsonl` only when the project wants loop audit history in Git; otherwise archive or ignore them by project policy.
- Always ignore `.agent/logs/` unless sanitized logs are intentionally published.
- Do not delete legacy alias files automatically after migration. Mark them as migrated or leave them read-only unless the user approves removal.

## Verification Command Discovery

Discover commands in this order:

1. Read project manifests such as `package.json`, `pyproject.toml`, `Makefile`, `Cargo.toml`, `go.mod`, `pom.xml`, or repository docs.
2. Map conventional script names to `verification_commands`: `test`, `typecheck`, `build`, `lint`, `check`, `validate`, `acceptance`.
3. If multiple commands exist for one type, choose the narrowest fast command for `core_verification` first, such as unit tests before e2e tests. Record broader commands as non-core verification.
4. Smoke-check a discovered command once when safe, using `--help`, `--dry-run`, a list mode, or the normal command if no dry-run exists.
5. If the command itself is unavailable or misconfigured, record the reason in `Docs/EVALUATION.md` and fall back to the next verification layer.
6. If a command requires secrets, production data, or privileged environment variables, stop under the hard-stop rules.
7. If no runnable artifact exists, set `core_verification: review` and record the reason in `Docs/EVALUATION.md`.
8. If no command can be discovered, add `Manual Confirmation Needed` to `Docs/ACCEPTANCE.md` and stop before claiming `Done`.

## Protocol Versioning

Use `protocol_version: 1` for this document. Future versions must preserve canonical file names or provide an alias migration table. Unknown fields should be preserved when rewriting state.

## Scope Change Counting

For `scope_expansion` versus `target_revision`, count `Must Pass` changes by acceptance checkbox item. If an agent splits or merges acceptance items during the same decision, freeze the pre-change count until the scope decision is recorded. Changes that alter `Non-Goals`, the user goal, or the verification strategy are always `target_revision`, regardless of item count.
