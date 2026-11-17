# Acceptance

Walk every line. A checked template without an evidence-backed consumer
adaptation is incomplete.

## Rubric

- The ICP was read from the workspace context. With none, the agent stopped
  and sent the operator to tam-building's first phase instead of tiering.
- An existing rubric was shown and confirmed, not rewritten. A new one was
  proposed from the ICP's own language, corrected by the operator, and written
  to the project's context repo, not into the agent prompt.
- Every tier names the evidence that counts for it, and is decidable from the
  sourced row plus at most one search.

## Project

- The agent installed and read `cargo-project` before adapting.
- With tam-building installed, the four tier columns were moved onto its
  `tam_companies`, and this skill's model copy and AI Ark connector were
  deleted. The plan shows `tam_companies` as an update that adds the columns,
  and nothing else about it changes.
- The workflow input's column names match the live model's
  (`cargo-ai storage column list`).
- The agent carries the read-only `context` capability and `webSearch`, no
  `memory`, and no model in `uses`.
- The play writes the four columns with bare slugs, filters on `tiered_at`
  (null or stale) and never on the tier, uses `changeKinds: ["added"]` and
  `noConcurrency`, and ships disabled.
- One segment exists per tier the agent can emit.
- `rescoreAfter` in `infra/settings.ts` is the window the operator chose
  (`"6 months"` unless asked; `"7 days"` for weekly), and the play's stale
  condition reads it.
- `crmWriteback` is `none` unless the operator named a CRM. When set, the CRM
  is connected, the three named properties exist on the company object, the
  match property holds the row's domain (or record id on a CRM model), and the
  play's one connector node is `updateRecords` after the row write.
- This skill declares no `defineContext`.
- `node --import tsx evals/contract.mjs`, `cargo-ai project types`,
  `cargo-ai project check` and `cargo-ai project plan` pass.

## Guided handoff

- Every substantive message names the current phase and ends with a
  `Next step` containing one concrete decision, what it unlocks, and what stays
  blocked.
- Phase one ends on approving the rubric; phase two on deploying with the play
  disabled; phase three on approving the backfill at the measured cost and
  enabling the play.
- Nothing was deployed, batched or enabled before its approval.

## Results

- The pilot tiered ten rows. One A, one C and one disqualified were checked
  against the rubric by hand, and the evaluator results were quoted.
- With `crmWriteback` set, one piloted company was read back from the CRM and
  carried the row's tier, reason and scored-at date.
- The backfill estimate came from the pilot's actual credits, not from a
  written price.
- Every row carries a tier, a rationale and a stamp, and the four segments'
  counts sum to the tiered row count.
- The report gives the distribution, the disqualified share read as a verdict
  on the filter, the evaluator pass rate, actual credits against the estimate,
  and one recommended next step.

## Repository isolation

- This is one root skill. Supporting Markdown lives under `references/`, and no
  nested `SKILL.md` exists.
- No relative import leaves the skill folder.
- The template contains no credential, deployment command, customer data, or
  hard-coded price.
