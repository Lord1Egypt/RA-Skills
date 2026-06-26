# Promotion and extraction

## Promotion rule of thumb

Promote a learning when it is:
- broadly applicable across multiple files or tasks
- likely to save future contributors time
- a stable convention rather than a one-off event
- better expressed as a short prevention rule than a full incident report

## Promotion targets

| Target | Best for |
|---|---|
| `CLAUDE.md` | Project facts, conventions, durable gotchas |
| `AGENTS.md` | Workflow rules, automation sequences, verification steps |
| `.github/copilot-instructions.md` | Shared Copilot context |
| `SOUL.md` | Behavioural rules in OpenClaw workspaces |
| `TOOLS.md` | Tool-specific gotchas in OpenClaw workspaces |

## Extraction criteria

Extract a reusable skill when most of these are true:
- the solution is resolved and tested
- the pattern is not tied to a single file or repo
- the fix is non-obvious enough to deserve specialised guidance
- the pattern has recurred or is likely to recur
- the resulting skill can stand on its own without original chat context

## Before extracting

Check:
- Does the new skill solve a real category of task?
- Can its description say exactly when it should trigger?
- Can you move detailed docs to `references/`?
- Can repeated logic be bundled into `scripts/`?
- Can you add at least a small eval set?
