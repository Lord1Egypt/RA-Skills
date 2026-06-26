---
name: five-star-reviewers
description: orchestrate a five-reviewer code review over a git diff, pull request diff, patch, or commit range by launching one dedicated sub-agent per reviewer role, then produce one consolidated report for a follow-up ai coding pass. use when reviewing a code repository, comparing working tree changes, checking a pr, or evaluating changes between two git revisions. optimized for pragmatic, language-agnostic review that prioritizes correctness, architecture, testability, readability, and simplicity while actively discouraging code bloat, unnecessary abstraction, and maintenance-heavy designs.
---

# Five Star Reviewers

Run a coordinated, language-agnostic review across five focused reviewer sub-agents, then merge them into one pragmatic report that a human or a follow-up AI can act on immediately.

## Core principles

Apply these principles globally, especially when reviewers disagree:

1. Preserve correctness before optimizing elegance.
2. Prefer fewer concepts over fewer lines.
3. Favor high cohesion, low coupling, and a small maintenance surface.
4. Allow small amounts of repetition when the alternative is a weak abstraction.
5. Do not add complexity for speculative future requirements.
6. Every finding should help the next iteration produce smaller, clearer, safer code.

## Mandatory multi-agent rule

You must launch exactly five dedicated sub-agents for every full review run.

- Use one sub-agent per reviewer role.
- Do not collapse multiple reviewer roles into one agent.
- Do not emulate reviewer separation inside a single mixed-context analysis.
- The lead agent may pre-scan the diff and gather context, but the role-specific review must still be produced by separate sub-agents.

Required reviewer identities:

- `star_correctness`
- `star_architecture`
- `star_testability`
- `star_readability`
- `star_simplicity`

## Review workflow

1. **Acquire the review target.** Follow [references/diff-acquisition.md](references/diff-acquisition.md).
2. **Pre-scan the change.** Identify changed files, risky areas, missing tests, and places where surrounding context is needed.
3. **Launch the five reviewer sub-agents.** Follow the rubric in [references/reviewer-rubric.md](references/reviewer-rubric.md).
4. **Write each sub-agent report to disk.** Follow [references/report-template.md](references/report-template.md).
5. **Merge and arbitrate.** Deduplicate overlapping findings, resolve conflicts, and rebuild priorities globally.
6. **Write one consolidated report.** Use [references/report-template.md](references/report-template.md).

## Default operating mode

Start from the repository diff rather than from static style rules.

- Prefer the current working tree diff by default.
- Support commit-range comparison, pr diff input, or raw patch input when provided.
- Expand beyond the diff when necessary to understand behavior, module boundaries, calling context, or tests.
- Stay language-agnostic. Judge the change using durable engineering principles, not language-specific taste.

## Diff-first acquisition rules

When the user does not specify an input form, assume the current repository is the target.

- First inspect repository state and collect the active diff.
- If the diff is empty, check staged vs unstaged changes and verify the current directory and revision context.
- If the user specified a revision range, review that range.
- If the user supplied a pr diff or patch directly, review that artifact instead of trying to reconstruct it.
- If the change is very large, prioritize the highest-risk areas first and clearly state any scope reduction.

## Report file locations

Each reviewer sub-agent must write its own report into the current project under:

`docs/five-star-reviewers/YYYY-MM-DD-XX-agent-<role>.md`

Rules:

- Create the `docs/five-star-reviewers/` directory if it does not exist.
- Use the current local date in `YYYY-MM-DD` format.
- Use a stable two-digit sequence for `XX` so the five files are easy to scan in order.
- Use these default filenames:
  - `docs/five-star-reviewers/YYYY-MM-DD-01-agent-correctness.md`
  - `docs/five-star-reviewers/YYYY-MM-DD-02-agent-architecture.md`
  - `docs/five-star-reviewers/YYYY-MM-DD-03-agent-testability.md`
  - `docs/five-star-reviewers/YYYY-MM-DD-04-agent-readability.md`
  - `docs/five-star-reviewers/YYYY-MM-DD-05-agent-simplicity.md`
- The lead agent should then write the merged report beside them, for example:
  - `docs/five-star-reviewers/YYYY-MM-DD-06-consolidated-review.md`

If the environment prevents writing files, still produce the reports in chat, but explicitly state that the expected disk outputs could not be created.

## The five reviewers

Use these reviewer prefixes so their outputs are easy to recognize as part of the same skill:

- `star_correctness`
- `star_architecture`
- `star_testability`
- `star_readability`
- `star_simplicity`

Reviewers should stay inside their own lane. They may look at adjacent code for context, but they should not duplicate one another's focus. Detailed scopes, severity guidance, and anti-noise rules are in [references/reviewer-rubric.md](references/reviewer-rubric.md).

## Consolidation rules for the lead agent

The lead agent is the final arbiter.

- Merge duplicate findings from different reviewers into one stronger issue.
- Resolve conflicts explicitly. For example, if one reviewer wants more abstraction and another argues the abstraction is unnecessary, choose the option that best preserves correctness with the smallest concept count and maintenance burden.
- Re-rank findings into **global p0**, **global p1**, and **global p2**. Do not simply concatenate reviewer lists.
- Keep strong ideas worth preserving under a dedicated “things to keep” section so the next AI does not over-correct.
- Prefer actionable guidance over abstract commentary.

## Severity discipline

Only raise a finding when it is grounded in the actual change.

- **p0**: likely correctness break, severe boundary violation, or a critical validation gap that could ship a defect.
- **p1**: meaningful maintainability, architecture, readability, or testability issue that should be addressed in the next iteration.
- **p2**: optional improvement, cleanup, or simplification opportunity that is real but not urgent.

Avoid turning vague best-practice opinions into high-priority findings.

## Evidence requirements

Every issue should include:

- a concrete location such as file, function, module, or diff hunk
- why the issue matters
- a practical suggested fix

Do not emit generic advice such as “improve structure” or “add more tests” without naming where and why.

## Budget and focus control

Keep review output dense and useful.

- Per reviewer, prefer at most 3 p0 findings, 5 p1 findings, and 5 p2 findings.
- Skip low-value style nits unless they materially affect comprehension or maintenance.
- When the diff is large, spend attention on risky logic, boundaries, error handling, integration points, and test gaps before commenting on polish.

## Simplicity is a first-class concern

Treat unnecessary code growth as a real engineering problem.

Specifically look for:

- one-off abstractions with little reuse value
- wrappers, managers, helpers, or adapters that only forward behavior
- configuration layers that are more complex than the logic they configure
- speculative flexibility that increases present-day maintenance cost
- opportunities to reduce files, indirection, or branching while keeping correctness intact

Shorter code is not automatically better. Lower cognitive load and lower maintenance cost are the actual goals.

## Output expectations

Produce one human-readable report that is also suitable as direct input to a follow-up AI implementation pass.

Use the consolidated report structure in [references/report-template.md](references/report-template.md). The report should make it obvious:

- what must change now
- what should change next
- what can wait
- what should not be “improved” further

## When to inspect more context

Broaden context when the diff alone is insufficient to judge behavior or design quality.

Common triggers:

- a modified function depends heavily on surrounding helpers
- a changed interface affects callers or implementers elsewhere
- tests appear thin and related tests may exist outside the diff
- a new abstraction claims broader reuse than the diff demonstrates
- a bug risk depends on lifecycle, state, or integration behavior not visible in the patch alone

Be deliberate. Read more context to improve judgment, not to wander.