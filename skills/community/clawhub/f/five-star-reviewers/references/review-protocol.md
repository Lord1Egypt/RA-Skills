# Review protocol

## 1. Acquire the review target

Default to the current repository state.

Suggested command sequence when operating in a repository:
- inspect state with `git status --short`
- collect unstaged diff with `git diff`
- collect staged diff with `git diff --cached`
- if the user specifies revisions, use `git diff <base>..<head>`
- if the user specifies a single commit for review, compare it to its parent or inspect with `git show`

If a raw patch or pr diff is already provided, use that directly.

## 2. Pre-scan before review

Identify:
- changed files and directories
- added, removed, or renamed files
- risky interfaces
- stateful logic, persistence, networking, concurrency, authorization, or parsing changes
- corresponding tests and whether they changed

## 3. Pull context deliberately

Read adjacent code only when needed to judge:
- behavior
- module boundaries
- test coverage
- reuse claims
- integration impact

Avoid broad repository tours.

## 4. Launch five dedicated sub-agents

This step is mandatory.

- Launch one and only one sub-agent for each reviewer role.
- Do not merge roles inside a shared agent.
- Give each sub-agent the same diff plus any deliberately selected extra context.
- Keep each sub-agent narrowly scoped to its own rubric.

Required assignments:
- `star_correctness` -> correctness-only review
- `star_architecture` -> architecture-only review
- `star_testability` -> testability-only review
- `star_readability` -> readability-only review
- `star_simplicity` -> simplicity-only review

## 5. Persist the five sub-agent reports

Each sub-agent report should be written to the repository under:

`docs/five-star-reviewers/YYYY-MM-DD-XX-agent-<role>.md`

Recommended default ordering:
- `01-agent-correctness.md`
- `02-agent-architecture.md`
- `03-agent-testability.md`
- `04-agent-readability.md`
- `05-agent-simplicity.md`

## 6. Consolidate

The lead agent should:
- read the five sub-agent reports
- merge duplicates
- resolve disagreements explicitly
- rebuild priorities into global p0 / global p1 / global p2
- highlight simplification opportunities
- preserve good decisions under a “things to keep” section

## 7. Persist the consolidated review

Write the merged report beside the five agent reports, for example:

`docs/five-star-reviewers/YYYY-MM-DD-06-consolidated-review.md`

If file writes are unavailable, produce the same structure in chat and explicitly note the missing on-disk outputs.

## 8. Hand off cleanly

The final report should help a follow-up AI implement the next pass without needing extra restructuring.
Prefer direct, actionable language over broad principles.
