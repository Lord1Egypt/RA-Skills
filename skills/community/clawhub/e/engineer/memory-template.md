# Memory Template - Engineer

Create `~/engineer/memory.md` with this structure only if the user wants persistence:

```markdown
# Engineer Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | paused | never_ask

## Context
- Default activation moments for engineering judgment
- Preferred output style: checklist, matrix, decision record, or execution plan
- Default posture: safety-first, speed-first, cost-first, or reliability-first
- Stable constraints that often matter in this user's work

## Notes
- Repeated assumptions that should be surfaced automatically
- Reusable verification habits and evidence thresholds
- Domain-specific failure patterns worth checking early

---
Updated: YYYY-MM-DD
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning | Capture reusable patterns gradually |
| `complete` | Enough context exists | Use stored defaults without extra setup |
| `paused` | User wants minimal persistence | Avoid asking for more memory unless needed |
| `never_ask` | User does not want persistence | Keep all future work session-only |

## Key Principles

- Store reusable engineering preferences, not confidential project payloads.
- Keep local notes focused on activation, risk posture, and preferred output shape.
- Do not store credentials, proprietary files, or regulated data.
- If the user declines persistence, do not create or update `~/engineer/`.
