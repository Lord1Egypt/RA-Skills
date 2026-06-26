---
name: flyai-commit-lint
description: Enforce conventional commit messages with semantic validation, scope checking, and automated fix suggestions for git workflows.
version: 1.0.0
author: dingtom336-gif
license: MIT
tags:
  - git
  - commit
  - linting
  - workflow
  - automation
allowedTools:
  - Bash
  - Read
  - Grep
---

# FlyAI Commit Lint

Enforce conventional commit messages across your team with semantic validation, scope verification, and automated fix suggestions.

## When to use

Activate this skill when:
- A user runs git commit and the message does not follow conventional commit format
- A user asks to review or fix commit messages in a branch
- Pre-commit hooks need commit message validation
- CI pipelines require commit format enforcement

## Commit Format

All commits must follow the pattern: type(scope): subject

### Allowed Types

| Type | Description |
|------|-------------|
| feat | A new feature |
| fix | A bug fix |
| docs | Documentation changes |
| style | Formatting, missing semicolons, etc. |
| refactor | Code change that neither fixes a bug nor adds a feature |
| perf | Performance improvement |
| test | Adding or updating tests |
| chore | Maintenance tasks |
| ci | CI/CD configuration changes |
| build | Build system or dependency changes |

### Scope Rules

- Scope is optional but recommended
- Must be lowercase kebab-case
- Should match a module, component, or directory name in the project
- Examples: auth, api, ui, database, ci

### Subject Rules

- Use imperative mood: "add feature" not "added feature"
- No period at the end
- Maximum 72 characters
- Start with lowercase

## Validation Process

1. Parse the commit message into type, scope, subject, body, and footer
2. Validate type against the allowed list
3. Check scope format if present
4. Verify subject follows all rules
5. Check total first line length does not exceed 72 characters
6. If body is present, ensure blank line separator exists

## Auto-Fix Suggestions

When a commit message fails validation, suggest fixes:

- Wrong type: suggest the closest matching type
- Uppercase subject: auto-lowercase the first character
- Period at end: remove trailing period
- Past tense: suggest imperative form (added -> add, fixed -> fix)
- Missing type: infer from changed files (test files -> test, docs -> docs)

## Integration

Works with:
- Git hooks (pre-commit, commit-msg)
- GitHub Actions CI checks
- Local development workflow
- Branch history cleanup before merge

## Examples

Good:
- feat(auth): add OAuth2 login flow
- fix(api): handle null response from upstream
- docs: update API reference for v2 endpoints
- refactor(database): extract connection pooling logic

Bad:
- Added new feature (missing type)
- feat: Add OAuth2. (uppercase, period)
- fix(API): Fixed the bug (uppercase scope, past tense)
