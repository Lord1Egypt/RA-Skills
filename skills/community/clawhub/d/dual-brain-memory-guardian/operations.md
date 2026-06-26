# Memory Operations (Dual-Brain)

This project now runs on a dual-brain model:

- Left Brain (Markdown): explicit rules and scoped overrides.
- Right Brain (Pinecone): semantic recall for corrections, reflections, and historical episodes.

## Source of Truth Ownership

This file is the canonical runtime spec.

1. Trigger sequencing and command execution are defined here only.
2. `SKILL.md` should reference this file and avoid duplicating runtime steps.
3. `learning.md` should focus on learning criteria and promotion signals, not command choreography.

## Runtime Commands (npm)

| Intent | Command |
|------|---------|
| Initialize index for model | `npm run memory:init` |
| Enforced pre-task recall at session start | `npm run memory:session-start -- --task "..." --top-k 3 --max-content-chars 1000` |
| Auto pre-task recall (idempotent) | `npm run memory:auto-session-start -- --task "..." --top-k 3 --max-content-chars 1000` |
| Enforced correction capture | `npm run memory:on-correction -- --content "..." --content-file ./correction.txt --project my-app` |
| Enforced post-task reflection | `npm run memory:on-task-complete -- --summary "..." --summary-file ./summary.txt --outcome success` |
| Auto post-task reflection (idempotent) | `npm run memory:auto-task-complete -- --summary "..." --summary-file ./summary.txt --outcome success` |
| Mark event as promoted to Markdown | `npm run memory:mark-promoted -- --id <event-id> --promoted true` |
| Save correction/reflection to DEEP memory | `npm run memory:save -- --type correction --content "..."` |
| Semantic recall (Top-K) | `npm run memory:search -- --query "..." --query-file ./query.txt --top-k 3 --max-content-chars 1000` |
| Start bulk import | `npm run memory:import:start -- --uri s3://bucket/path --error-mode continue` |
| Check import progress | `npm run memory:import:status -- --id <import-id>` |
| List imports | `npm run memory:import:list -- --limit 20` |
| Cancel import | `npm run memory:import:cancel -- --id <import-id>` |
| Freshness snapshot | `npm run memory:freshness` |
| Forget specific records/filters | `npm run memory:forget -- --id <id>` or `npm run memory:forget -- --type reflection --project qclaw` |
| Forget tenant memory in Pinecone | `npm run memory:forget-all -- --tenant default` |
| Syntax verify scripts | `npm run verify` |

### CLI parser note

- Values that start with `--` are supported via `--key=value` form.
- Example: `npm run memory:save -- --content=--prefixed-value --type correction`
- For long or quote-heavy text, prefer file-backed flags: `--content-file`, `--summary-file`, `--query-file`, `--metadata-file`.

## Enforced Trigger Contract

The following triggers are mandatory and non-skippable for dual-brain continuity:

1. Session start must run `memory:session-start` before substantive task execution.
2. User correction/rewrite request must run `memory:on-correction` immediately.
3. Non-trivial task completion must run `memory:on-task-complete` before ending the workflow.
4. If a trigger command fails, report the failure and retry once after fixing input/env.
5. Runtime guard blocks `on-correction` and `on-task-complete` when `session-start` is missing or stale (>12h).

Preferred agent integration for autonomous triggering:

1. At conversation start, call `memory:auto-session-start` (auto-skip if fresh for same tenant).
2. At final response stage, call `memory:auto-task-complete` (auto-skip if completion already recorded for current session).
3. Use `--force` only when you intentionally want to re-run either trigger.

## Runtime Guard State

- Trigger guard state file: `.memory-trigger-state.json` (workspace root).
- Write/update points:
  - `memory:session-start` updates `sessionStartedAt`.
  - `memory:on-correction` updates correction marker.
  - `memory:on-task-complete` updates completion marker.
- For one-off maintenance/migration only, bypass guard with `--allow-without-session-start`.

## Automatic Operations

### On Session Start

1. Load `~/dual-brain-memory-guardian/memory.md` (HOT).
2. Load smallest matching WARM files from `~/dual-brain-memory-guardian/projects/*` and `~/dual-brain-memory-guardian/domains/*`.
3. Run `npm run memory:session-start -- --task "..." --project "..." --domain "..."`.
4. Use `top_k=3` by default unless the task explicitly needs broader recall.
5. Merge retrieved experience with Markdown rules and expose loaded files in the command output (`leftBrain`).
6. Truncate each recalled right-brain `content` in stdout (default 1000 chars via `--max-content-chars`) to avoid context blowout.

## Left-Right Merge Protocol

When executing a task:

1. Apply Markdown constraints first.
2. Use Pinecone hits to avoid historical pitfalls.
3. If Pinecone experience conflicts with Markdown, keep Markdown behavior and ask whether rules should be updated.

Priority order:

- Project Markdown > Domain Markdown > Global Markdown > Pinecone recall.

### On Correction Received

1. Parse correction type (`correction`, `reflection`, `pitfall`, `rejection`).
2. Run `memory:on-correction` to save full normalized event to Pinecone DEEP memory.
3. Check whether it is a hard contract (explicit "always/never" or project rule).
4. If hard contract, write concise version to Markdown (HOT/WARM) unless `--no-markdown-promotion` is set.
5. Mark the original Pinecone event with `promoted_to_markdown=true` (automatic on successful promotion, or via `memory:mark-promoted`).
6. Track repetition count. Repeated, high-signal rules can be promoted.

### On Error Encountered (Mandatory Capture)

1. Capture what failed, impact, and root cause (including reasoning mistakes).
2. Run `memory:on-correction` immediately (recommended: `--type pitfall`).
3. Use `--resolution` to store root cause and applied fix.
4. For long traces or quote-heavy payloads, use `--content-file` and `--resolution-file`.
5. Add searchable tags such as `error`, `root-cause`, `regression`, and related module/task labels.

### On Task Complete

1. Summarize outcome (`success`, `partial`, `failed`) and key lesson.
2. Run `memory:on-task-complete` to persist reflection/pitfall to Pinecone DEEP memory.
3. Append concise local reflection to `~/dual-brain-memory-guardian/reflections.md` unless `--no-local-reflection` is set.
4. Promote durable hard rules to Markdown only if explicit and stable.

### On Pattern Match During Work

1. Cite source type in reasoning (Markdown rule or Pinecone recall).
2. Never treat Pinecone memory as mandatory contract unless promoted to Markdown.
3. Log usage count for future promotion/demotion decisions.

## Data Model Guidance (Pinecone)

Use structured IDs and metadata for reliable filtering and traceability.

- ID pattern: `tenant#event_type#timestamp#shortid`
- Namespace pattern: `dualbrain-<tenant>`
- Text field (integrated embedding): `content`
- Recommended metadata:
  - `event_type`
  - `domain`
  - `project`
  - `tenant_id`
  - `task_context`
  - `resolution`
  - `created_at`
  - `promoted_to_markdown`
  - `promoted_at`
  - `tags` (string list)

## Search Guidance

For integrated embedding indexes:

- Use `searchRecords` with text query.
- Keep `top_k` small (3-5) for planning, increase when synthesizing digests.
- Keep CLI recall output compact with `--max-content-chars` (default 1000).
- Use metadata filters for `event_type`, `domain`, `project`, and `tags`.

## Ingestion Strategy

- Online events and corrections: `upsertRecords` (text input).
- Large backfills: `startImport` with Parquet vectors from object storage.
- For large datasets, prefer import over frequent upsert loops.

## Freshness and Consistency

Pinecone is eventually consistent.

After writes:

1. Use bounded fetch retry (`waitForWrite`) when strict read-after-write is needed.
2. Use `describeIndexStats` for namespace-level count checks.
3. Avoid assuming immediate visibility after upsert/import completion.

## Forget and Deletion Operations

- `Forget X`: remove from Markdown scopes and delete matching vector records by id or metadata filter (`memory:forget`).
- `Forget everything`: clear `~/dual-brain-memory-guardian/` and run Pinecone tenant clear (`memory:forget-all`).

Before any deletion request (`memory:forget` or `memory:forget-all`):

1. Remind that deletion is permanent for vector memory.
2. State the exact deletion scope (ids/filter/tenant namespace).
3. Confirm explicit user intent before execution.
4. After deletion, report what was deleted and what was not deleted.

## Edge Cases

### Contradiction

- Markdown says TypeScript, Pinecone recalls Python.
- Resolution: obey Markdown, attach optional note to user about historical difference.

### Namespace Ambiguity

- If tenant or project is unclear, default to current active tenant.
- Ask user before promoting ambiguous memory to global rules.

### Import Limits and Caveats

- Import only works for serverless indexes.
- Import into new namespaces only.
- Integrated embedding indexes import vectors, not text.
