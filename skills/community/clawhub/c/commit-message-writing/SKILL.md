---
name: commit-message-writing
description: Strict Conventional Commits v1.0.0, atomic commit discipline, and Trunk-Based Development guardrails for git work. Use when preparing a commit, staging changes, writing or revising a commit message, deciding whether to split changes, planning branch strategy for a feature/bug/fix, opening or reviewing pull requests, or after finishing any meaningful implementation unit.
---

# Commit Message Writing

Every commit: valid Conventional Commit, atomic, on the right short-lived branch.

## Required workflow

1. `git status --short` and `git diff --stat`.
2. Verify you're on a short-lived branch dedicated to one feature, bug, fix, or coding area. If not, create/switch first.
3. Confirm the changes are one logical unit. If mixed, split before committing.
4. Confirm automated tests appropriate to the scope will run.
5. Pick the most specific commit type.
6. Write the message:

```text
<type>[optional scope][!]: <imperative lowercase description>

[optional body]

[optional footer(s)]
```

7. Validate with `scripts/validate_commit_message.py` before committing.

## Hard rules

- One short-lived branch per feature, bug, fix, or distinct coding area.
- Keep branches narrow, merge back quickly, avoid long-lived divergence.
- Every PR must have robust automated tests so bugs are caught early.
- Always include a lowercase type followed by `: `.
- Imperative, lowercase description, no trailing period, ≤72 chars.
- Body: one blank line after description. Footers: one blank line after body.
- Footer format: `Token: value`. Hyphens in tokens except `BREAKING CHANGE`.
- Use `!` and/or `BREAKING CHANGE:` footer for breaking changes.
- Never use `WIP`, `misc`, `update`, or vague summaries.

## Types

| Type | When | SemVer |
|---|---|---|
| `feat` | new feature | minor |
| `fix` | bug fix | patch |
| `refactor` | restructure, no behavior change | none |
| `perf` | performance improvement | none (patch if fixes bug) |
| `docs` | documentation only | none |
| `test` | tests only | none |
| `build` | build system / deps | none |
| `ci` | CI/CD changes | none |
| `chore` | maintenance / tooling | none |
| `style` | formatting only | none |
| `revert` | revert prior commit | depends |

## Scope

Use a consistent noun for the dominant area. Omit only when truly cross-cutting. Never multiple scopes in one commit line.

## Splitting rules

Split when:
- feature + bug fix
- code + formatting-only cleanup
- deps/build + application logic
- refactor + standalone behavior change
- generated files + loosely coupled source

One type, one intent per commit. If you can't describe it that way, split.

## Validation

```bash
python3 scripts/validate_commit_message.py --message "feat(auth): add otp fallback"
```
