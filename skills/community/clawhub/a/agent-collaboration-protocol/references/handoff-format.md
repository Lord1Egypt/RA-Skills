# Handoff Message Format

Use this template when spawning or messaging agents. Include ALL fields.

```
## Handoff: {Title}

**What:** {Specific task or deliverable — one sentence}

**Why:** {Context and priority — why this is needed now}

**Files:**
- `shared/build-{YYYYMMDD}/backend/router.py` — route handler
- `shared/build-{YYYYMMDD}/SPEC.md` — API contract

**Success criteria:** {Observable behavior — how we know it's done}

**ETA:** {YYYY-MM-DD HH:MM UTC}
```

## Monitoring

Adapt monitoring to your setup. Suggested pattern:

1. Check shortly after handoff: Did the agent start? Files modified?
2. Check near ETA: Progress? Blockers?
3. If no progress by ETA: re-spawn or escalate

Adjust frequency and method based on your agent architecture and tooling.