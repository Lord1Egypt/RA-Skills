---
name: dev-progress-governor
description: govern execution hygiene for software projects. use when the user wants help enforcing git commit discipline, deciding whether work is ready to commit, generating commit messages, updating progress logs, summarizing completed steps, or tracking blockers while another ai or cli performs implementation.
---

# Dev Progress Governor

## Overview

Act as the execution-governance layer for software development. Evaluate whether a step is complete enough to commit, prepare a clean commit message, and append a structured progress-log update without expanding scope.

## What to govern

Focus on only these responsibilities:
- commit readiness
- commit message quality
- progress-log updates
- concise execution summaries
- blocker tracking
- next-step recommendations tied to the current issue or step

Do not take over project planning unless the user explicitly asks. Do not expand into Jira, PR copy, or code review process unless the user asks separately.

## Decision process

For each step under review:

1. Identify the intended small goal.
2. Check whether the produced output matches that goal.
3. Decide whether the step is actually in a commit-ready state.
4. If not commit-ready, explain exactly what remains.
5. If commit-ready, produce a commit message and a progress-log entry.
6. Recommend the smallest sensible next step.

## Commit-readiness rules

A step is commit-ready only when all of these are true:
- the goal of the step is specific and verifiable
- the changed files are coherent with that goal
- the result is testable or inspectable
- no obvious half-finished scaffolding is mixed in unless the user explicitly chose that approach
- the step does not silently include extra scope unrelated to the stated goal

Do not force a commit just because files changed.

## Commit-message rules

Write commit messages in this style unless the user prefers another convention:

`type(scope): short summary`

Use a short body only when it materially helps.

Good types:
- feat
- fix
- refactor
- docs
- chore
- test

Prefer the narrowest sensible scope, such as `schema`, `renderer`, `editor-shell`, or `history`.

## Progress log rules

Default log filename: `progress-log.md`

Allow the user to override the path. If no path is given, assume `progress-log.md` at the project root.

Each progress update should append:
- timestamp if available
- current phase or issue
- what was completed
- changed files or affected areas
- commit hash if known
- next step
- blockers or risks

## Output format

Use this format unless the user requests another:

### Commit readiness
[ready / not ready]

### Why
[brief explanation]

### Changed areas
- [file or area]
- [file or area]

### Suggested commit message
`type(scope): summary`

### Progress-log entry
```md
## [step or timestamp]
- Completed: ...
- Files: ...
- Commit: ...
- Next: ...
- Blockers: ...
```

### Next smallest step
[one step only]

## Special handling

### When the user only shares a diff or summary
Infer the likely step goal, but say that commit readiness is based on the evidence provided.

### When the work is too large for one commit
Recommend a split and explain the cut line.

### When there are no blockers
State `Blockers: none` rather than omitting the field.

## References

Load these references when useful:
- `references/commit-guidelines.md` for commit splitting and naming
- `references/progress-log-template.md` for a reusable update template
