---
name: coding-pipeline
description: "Enforces a disciplined 4-phase pipeline for non-trivial coding tasks: Plan (hypothesis) → Code (one fix) → Validate (root cause) → Debug (max 3 tries, escalate). Prevents blind patching, symptom fixes, and retry loops. Activate for any bug fix, feature implementation, refactor, or error investigation that isn't a trivial one-line change."
---

# Coding Pipeline

A disciplined 4-phase workflow for any non-trivial coding task. Each phase has a clear purpose, explicit exit criteria, and a loop-back rule when things go wrong. The phases exist because AI agents' default failure mode is blind iteration: edit → build → edit → build → give up. This skill forces hypothesis-driven work, one-fix-at-a-time discipline, root-cause verification, and bounded debugging.

**This is a rigid skill — follow the phases exactly. Do not skip, merge, or reorder.**

## Core Rule

Every non-trivial task — bug fix, feature, refactor — goes through all 4 phases in order:

```
┌─────────────┐    ┌──────────┐    ┌───────────────┐    ┌─────────────┐
│  1 PLANNER  │───▶│ 2 CODER  │───▶│  3 VALIDATOR  │───▶│  4 DEBUGGER │
│ hypothesis  │    │ one fix  │    │ build + root  │    │ max 3 tries │
└─────────────┘    └────┬─────┘    └───────┬───────┘    └──────┬──────┘
       ▲                │                  │                   │
       │                │ unclear cause    │ fails             │ new hypothesis
       └────────────────┴──────────────────┴───────────────────┘
                        loop back to PLANNER
```

Skipping a phase or jumping straight to Phase 2 is the failure mode this skill prevents.

## Quick Reference

| Situation | Active Phase | Exit When |
|-----------|--------------|-----------|
| New task arrives | **Phase 1 Planner** | Hypothesis written, scope defined, success criteria explicit |
| Hypothesis validated | **Phase 2 Coder** | One focused change applied, no unrelated edits |
| Change applied | **Phase 3 Validator** | Build passes AND root cause verified |
| Validator fails | **Phase 4 Debugger** | Either fix found (→ Phase 2) or 3 attempts exhausted (→ escalate) |
| Unclear cause mid-fix | **Back to Phase 1** | New hypothesis written |
| Fix introduces new error | **Back to Phase 1** | Hypothesis was wrong |

## Phase 1 — Planner

**Goal:** Understand the task and formulate an explicit hypothesis *before* any code change.

**Required outputs:**

1. **Task breakdown** — what is actually being asked? Break into the smallest independent units.
2. **Hypothesis** — one sentence in the form: *"I believe [symptom] is caused by [cause], because [evidence]."*
3. **Scope** — which files/modules are in-bounds, which are explicitly out-of-bounds
4. **Success criteria** — how Phase 3 will verify this is fixed (not just the symptom gone)

**Forbidden in Phase 1:**

- Editing any code
- Running build or test commands to "see what happens"
- Multiple parallel hypotheses — pick one, commit to it
- Vague hypotheses ("something with the auth flow") — sharpen until specific

**Exit criteria:** Hypothesis is concrete, testable, and you can point to *why* this is the cause — not just *what* looks broken.

**Loop-back trigger:** If during Phase 2 or 3 the hypothesis turns out wrong, return here. Do not patch on top of a broken hypothesis.

See `references/phase-1-planner.md` for hypothesis patterns and scope breakdown templates.

## Phase 2 — Coder

**Goal:** Apply exactly one focused change that tests the hypothesis from Phase 1.

**Rules:**

1. **One fix at a time** — one change, one purpose, one file or one tightly-scoped set of files
2. **Full files, not snippets** — deliver complete file contents when showing work
3. **No speculative refactoring** — resist "while I'm in here…"; surgical scope only
4. **If the hypothesis is unclear mid-change → STOP**, return to Phase 1

**Definition of "one fix":** A single logical change that either proves or disproves the hypothesis. Three unrelated improvements = three separate Planner → Coder → Validator cycles.

**Exit criteria:** Change is applied, diff contains only the intended work, nothing unrelated.

See `references/phase-2-coder.md` for scope discipline and loop-back triggers.

## Phase 3 — Validator

**Goal:** Verify the change fixed the *root cause*, not just the symptom.

**Checklist (adapt to stack):**

1. **Build check** — compile/transpile succeeds, no new errors
2. **Type check** — no new type errors; any `@ts-ignore` / `type: ignore` needs an explicit written justification comment
3. **Focused test** — run the specific test that proves the hypothesis, not the full suite
4. **Root-cause verification** — the fix addresses the Phase 1 hypothesis, not a side effect
5. **Scope verification** — diff matches what Phase 1 planned; no accidental changes
6. **Regression check** — nothing adjacent broke

**The symptom-vs-cause test:**

> If I rolled back this change, would the symptom return *because of the same cause*, or because of something else?

If you can't answer confidently, the fix is symptomatic. Go back to Phase 1.

**Exit criteria:** All checks pass, root cause verified, no regressions.

**Failure → Phase 4 Debugger.**

See `references/phase-3-validator.md` for stack-agnostic validation patterns.

## Phase 4 — Debugger

**Goal:** Bounded debugging with documentation. Escalation over thrashing.

**Hard rules:**

1. **Max 3 attempts** — after 3 failed fixes, STOP and escalate to the user
2. **Document every attempt** — what was tried, what happened, why it failed
3. **Never repeat a fix** — if attempt 1 failed, attempt 2 must be *substantively different*
4. **Never "just try again"** — every attempt must be backed by a *new* hypothesis

**Attempt log template** (write to `.pipeline-state/attempts-<task>.md` or inline in chat):

```markdown
### Attempt N
- **Hypothesis**: What I now believe is wrong
- **Change**: What I modified (specific files/lines)
- **Result**: What happened (error output, unchanged behavior, new symptom)
- **Why it failed**: The actual root cause of this failure
- **Next direction**: What to try next OR escalate
```

**After 3 failed attempts:** STOP. Surface to the user with the full attempt log. Do **not** continue with a 4th attempt unless the user explicitly authorizes it.

**Recovery trigger:** If during Phase 4 a fundamentally new hypothesis emerges, return to **Phase 1** — not Phase 2. A new hypothesis means a new cycle, not continued debugging.

See `references/phase-4-debugger.md` for escalation patterns and worked examples.

## Phase Transition Gates

No phase transition is automatic. Each requires explicit criteria:

| From | To | Required |
|------|-----|----------|
| 1 → 2 | Planner → Coder | Hypothesis written + scope defined + success criteria |
| 2 → 3 | Coder → Validator | One focused change applied, no unrelated edits |
| 3 → Done | Validator passes | Build ✓ + types ✓ + root cause verified + no regressions |
| 3 → 4 | Validator → Debugger | Any validation check failed |
| 4 → 2 | Debugger → Coder | New hypothesis + change substantively different from previous attempts |
| 4 → 1 | Debugger → Planner | Fundamentally new hypothesis (not incremental) |
| 4 → STOP | Debugger → Escalate | 3 attempts exhausted |
| ANY → 1 | Back to Planner | Hypothesis proven wrong mid-cycle |

## Detection Triggers

Activate this pipeline automatically when the task is:

- **A bug report** — user says something is broken
- **A feature request** — non-trivial new functionality
- **A refactor** — touching existing code for non-cosmetic reasons
- **An error investigation** — digging into unexpected behavior
- **A test failure** — a test that was passing now fails
- **A deployment issue** — something that worked in dev fails in prod

**Skip the pipeline only for:**

- Trivial edits (typo, formatting, one-line config)
- Pure documentation changes
- Explicitly exploratory work ("just experiment, don't commit")

## Anti-Patterns

What this pipeline prevents:

1. **Symptom patching** — fixing what looks wrong without understanding why
2. **Multi-fix chaos** — changing three things at once, unable to tell which one worked
3. **Retry loops** — trying the same fix with minor variations hoping it sticks
4. **Premature coding** — jumping to Phase 2 before Phase 1 is done
5. **Validation skipping** — "it compiles, ship it" without root-cause check
6. **Unbounded debugging** — 8 attempts, no log, no escalation
7. **Speculative refactoring** — "while I'm here, let me also clean up this other file"
8. **Hypothesis drift** — quietly changing the hypothesis mid-fix to match what you just did
9. **Type-ignore laziness** — `@ts-ignore` without a written justification comment
10. **Scope creep** — task was "fix login redirect", PR touches 14 unrelated files

See `references/anti-patterns.md` for concrete before/after examples of each.

## Integration with Other Skills

This pipeline works well with — but does not replace — the following:

- **`systematic-debugging`** — when Phase 4 escalates, hand off to systematic-debugging for the full investigation protocol
- **`self-improving-agent`** — after every failed attempt in Phase 4, log to `.learnings/ERRORS.md` so the next task starts with that knowledge
- **`root-cause-analysis`** — when Phase 3 root-cause verification is ambiguous, escalate to RCA
- **`test-driven-development`** — Phase 1's "success criteria" naturally aligns with TDD's "write the failing test first"

See `references/integration.md` for detailed pairing patterns.

## Platform Integration

Platform-specific activation and hook configuration lives in `references/`:

- **`references/openclaw-integration.md`** — OpenClaw workspace setup, inter-session coordination
- **`references/hooks-setup.md`** — Claude Code / Codex hook configuration (`UserPromptSubmit`)
- **`references/multi-agent.md`** — Claude Code, Codex CLI, GitHub Copilot activation patterns

## Best Practices

1. **Always start at Phase 1** — no shortcuts, no exceptions for "obvious" fixes
2. **One hypothesis, one fix** — resist bundling
3. **Phase 3 verifies cause, not symptom** — this is the hard check
4. **Phase 4 is bounded** — 3 attempts, then escalate
5. **Document every failed attempt** — pattern recognition matters
6. **Full files, no snippets** — for reviewability
7. **Loop back to Planner on uncertainty** — cheaper than debugging a wrong hypothesis
8. **Escalate fast** — 3 failed attempts is a signal, not a suggestion

## Source

This pipeline is based on a production coding standard used in NestJS/Next.js/PHP production systems. It emerged from repeated observation that AI agents, left to their defaults, retry-loop into incoherence on non-trivial work. The 4-phase structure + max-3-attempts rule + mandatory hypothesis is the minimum structure needed to keep agents disciplined.
