# Child Brief Template (delegate_task)

A brief is the task's **interface contract** — like a function signature: inputs → work → outputs, with preconditions, postconditions and an error contract. Fill every field; the child sees only this brief and cannot ask questions.

## Skeleton (copy & fill)

```text
GOAL: <one concrete objective, one sentence>
ROLE: <explorer | researcher | worker | tester | reviewer>
SCOPE / OWNED: <exact files or areas; anything else is forbidden>
INPUTS: <only what this child must read — exact paths/URLs>
CONSTRAINTS: <no scope expansion; role limits (read-only / tests-only); no commits>
ASSUMPTIONS: <state explicitly what you assume where the brief is silent; never hide them>
NEEDS_INPUT: <[] or each open question + default_if_forced + blocking_level (low|high)>
  <!-- a structured RETURN block, not a pause: depth-1 children cannot stop mid-run and wait.
       blocked or ambiguous → fill this instead of guessing; the main agent closes the loop -->
MANIFEST: <N/A, or manifest path for ≥3-slice / relay / expected-cut-off tasks — a resuming child
  reads the manifest first and works only unfinished slices; slices idempotent, artifacts append-only>
DELIVERABLE: <artifact path + format; bulk output → write to a file, not chat>
SAVE-EARLY: <start the deliverable as a skeleton file FIRST (title + section stubs), then fill it in as you go — a cut-off then costs at most the current section>
BUDGET: <attempt / time / call ceiling for THIS task — always state one; when exceeded: STOP and report instead of pushing on>
RETURN: <one-line status + where the artifact is; inline findings ≤ ~1-2k tokens — prompt convention, no hard clamp>
ACCEPTANCE: <what the main agent will check to accept it>
STOP: <stop-and-report conditions; when to return instead of pushing on>
```

## Field → contract element

| Field | Contract element |
|---|---|
| GOAL | 1. one concrete objective |
| SCOPE / OWNED + CONSTRAINTS | 2. scope + 4. constraints / forbidden expansion |
| INPUTS | 3. necessary context only |
| DELIVERABLE + RETURN | 5. required deliverable (+ summary-size convention) |
| ASSUMPTIONS + NEEDS_INPUT | ambiguity contract: declared assumptions + structured needs_input return block |
| MANIFEST | optional checkpoint protocol (durability under replay) — N/A unless triggers fire |
| SAVE-EARLY | durability: survives iteration-cap cut-offs — artifact on disk early, grows incrementally |
| BUDGET | effort & stop discipline: the child knows its ceiling, so it stops instead of thrashing |
| ACCEPTANCE | 6. acceptance evidence |
| STOP | failure & scope handling |

## Per-role quick fills

| ROLE | Scope note | Deliverable | Extra rules |
|---|---|---|---|
| explorer | read-only | findings: paths/symbols/flows/risks/boundary | report uncertainty or conflicts; never redesign |
| researcher | read-only; one question | answer + references | facts vs inference; record version/date assumptions |
| worker | one owned area | changed files + commands + results + risks | smallest defensible change; follow patterns; no unrelated refactors |
| tester | tests only (edit tests only when asked) | exact command + pass/fail + output + gaps | never force a pass by changing production code |
| reviewer | read-only | findings (severity + file/symbol + impact + fix) or "no material findings" + residual uncertainty | review the actual final change, not its intended story; edit nothing; recompute hashes/counts instead of restating them |

## Filled example (worker)

```text
GOAL: Add the invoice-date column to the CSV export.
ROLE: worker
SCOPE / OWNED: src/export/csv.ts and tests/export/csv.test.ts only
INPUTS: src/export/csv.ts; tests/export/csv.test.ts; docs/export-format.md
CONSTRAINTS: no schema or dependency changes; no commits; do not touch other exporters
ASSUMPTIONS: date format follows docs/export-format.md §3 (ISO-8601); header name "invoice_date"
NEEDS_INPUT: [] — if the format doc is silent on timezone, use default_if_forced=UTC, blocking_level=low
MANIFEST: N/A (single slice)
DELIVERABLE: patched src/export/csv.ts + change note (what changed, why, limits)
SAVE-EARLY: change-note file started as stub headings before editing; filled as the edit progresses
BUDGET: ≤3 tool calls and one file edit; if it needs more, stop and report
RETURN: one line — files changed + test command + result
ACCEPTANCE: focused test passes; column present in sample export; main reads the diff
STOP: if the change needs a schema or API change, stop and report instead
```
