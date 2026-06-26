# ⚙️ Coding Pipeline

**Make AI coding agents work like disciplined engineers: plan, change one thing, validate, then debug with a limit.**

Coding Pipeline is a phase-gated workflow for non-trivial coding work. It stops agents from blind-patching, bundling unrelated fixes, and declaring success without proof.

## The 4 Phases

| Phase | Purpose | Required Exit |
|---|---|---|
| 1. Plan | Understand task, risk, hypothesis, success criteria | Written plan + smallest safe scope |
| 2. Code | Apply one focused change | One coherent diff, no surprise scope creep |
| 3. Validate | Prove the change works and root cause is addressed | Test/build/lint/log evidence |
| 4. Debug | If validation fails, investigate with a max of 3 attempts | Fixed or escalated with attempt log |

## Use It For

- Feature implementation
- Non-trivial bug fixes
- Refactors
- Test failures
- Deployment/CI failures
- Any task where “just edit it” is likely to create mess

Skip it only for trivial edits: typo, copy change, one-line config with obvious verification.

## Core Rules

1. **Hypothesis before code** — what should this change prove?
2. **One fix at a time** — unrelated improvements become separate cycles
3. **Validate cause, not vibes** — “it compiles” is not always enough
4. **Max 3 debug attempts** — then escalate with what was tried and what remains unknown
5. **No DONE without evidence** — test, build, lint, logs, screenshot, or named blocker

## Example Agent Output

```text
Phase 1 — Plan
Hypothesis: The checkout 500 is caused by missing null handling in discount lookup.
Smallest change: guard null discount before price calculation.
Validation: unit test for no-discount checkout + npm test checkout.
Risk: low; only checkout pricing path affected.
```

Then code. Then validation. No wandering.

## Pair It With

- **safe-change** before touching shared/high-risk files
- **deep-debugging** when root cause is unclear
- **self-improving-agent** when a failed attempt should become durable learning

---

*by brasco05 · phase-gated coding discipline for OpenClaw, Claude Code, Codex, and similar agents*
