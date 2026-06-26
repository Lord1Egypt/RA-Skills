# Detail File Template

Use this structure for `.learnings/details/YYYY-MM-DD-slug.md` when a one-line entry isn't enough.

All sections are optional — include what's useful, skip what isn't.

```markdown
# ERR-YYYYMMDD-NNN: Brief Title

## Trigger
What happened that surfaced this issue.

## Environment
OS, tool versions, config state — anything relevant to reproduction.

## Root Cause
Why it actually failed (not just what failed).

## Failed Alternatives
What was tried first and why it didn't work.

## Fix
The working solution, with enough detail to reproduce.

## Scope Conditions
When does this apply? When does it NOT apply?
(e.g., "Only on macOS 14+", "Only when running in Docker", "Only with API v2")
```

## When to Create a Detail File

- The fix is non-obvious or has preconditions
- Multiple approaches were tried before finding the solution
- The failure is environment-specific
- Someone else might hit this and need the full story

## When NOT to Create One

- Simple gotcha with a one-line fix
- Well-documented tool behavior
- Entry is already clear from the one-liner
