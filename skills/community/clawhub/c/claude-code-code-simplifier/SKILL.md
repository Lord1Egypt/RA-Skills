---
name: "code_simplifier"
description: "Use when changed code should be reviewed for reuse, code quality, and efficiency, then cleaned up before finalizing."
---


# Code Simplifier

Use this skill after making changes and before wrapping up.

## Workflow
1. Inspect the relevant diff or latest modified files.
2. Review for existing utilities that should be reused.
3. Review for code smell: parameter sprawl, copy-paste, leaky abstractions, or unnecessary comments.
4. Review for efficiency problems: repeated work, unnecessary reads, event churn, and hot-path bloat.
5. Fix confirmed issues and summarize what changed.

## Guardrails
- Prefer concrete fixes over broad stylistic churn.
- Keep attention on changed code, not the whole codebase.
- If no issue exists, say so explicitly.

## Example Requests
- Review my diff for duplicate logic and unnecessary complexity.
- Clean up this changed code before I ship it.

## Inputs
- Relevant diff or changed files
- Optional focus area

## Outputs
- Concrete cleanup changes
- Short summary of improvements

## Success Criteria
- Duplication or awkward abstractions were reduced.
- Performance regressions were checked.
- No unnecessary churn was introduced.

## Non-Goals
- Massive style-only rewrites
- Review of untouched code with no link to the change

## Source Provenance
Derived from `src/skills/bundled/simplify.ts`.
