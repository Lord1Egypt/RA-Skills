---
name: along-plan
description: "Read-only exploration and planning skill for safe code analysis. This skill should be used when the user asks to enter plan mode, analyze before changing, create a plan first, or wants a safe exploration phase before making edits. Enforces read-only tool access, produces a numbered plan under a Plan: header, and tracks step completion with [DONE:n] markers during execution."
---

# Along Plan

## Explore

- Only use `read`, `grep`, `glob`, `bash` (bash restricted to safe commands — see `references/safe-commands.md`)
- Do NOT use `edit` or `write`, except to save the plan document (see below)

Output the plan under an exact `Plan:` header:

```
Plan:
1. Step one
2. Step two
3. Step three
```

Then save it to `docs/plan-<topic>.md` or `doc/plan-<topic>.md`(whichever exists) using `write`:

```markdown
# Plan: <topic>

## TODO
- [ ] 1. Step one
- [ ] 2. Step two

## Acceptance Criteria
- Observable outcome that confirms the plan succeeded
- Edge cases or constraints that must hold
```

- `references/safe-commands.md` — bash allowlist/blocklist for plan mode
