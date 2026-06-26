# Phase 1 — Planner

Deep-dive on the Planner phase. Read this when starting any non-trivial task.

## Purpose

Phase 1 exists because **premature coding is the single biggest failure mode of AI agents**. When an agent jumps to Phase 2 without a hypothesis, it ends up:

- Patching symptoms (the bug returns next week)
- Flailing between plausible fixes
- Missing the actual root cause
- Producing unreviewable diffs

The Planner's job is to make you **commit to a hypothesis in writing** before you touch code.

## Required Outputs

### 1. Task Breakdown

Decompose the task into the smallest independent units. Ask:

- What is *actually* being asked — not what you assume
- What is the **one sentence** version of the goal?
- Are there hidden sub-tasks? (auth changes usually drag in token handling, CORS, session state)
- What is explicitly **not** in scope?

### 2. Hypothesis

A hypothesis is a falsifiable claim about the cause. Use this form:

> *"I believe [symptom] is caused by [cause], because [evidence]."*

**Good hypotheses:**

- *"I believe the login redirect loops because the middleware runs before `next-auth` sets its cookie, because the network tab shows no cookie on the `/api/auth/callback` response."*
- *"I believe the vital signs calculation is off by one day because the ISO week function is using `getDay()` (Sunday=0) instead of `getDay()+6 % 7` (Monday=0), because the test fails exactly when the date is a Sunday."*

**Bad hypotheses:**

- *"I think there's something wrong with the auth flow."* → too vague
- *"It's probably a race condition."* → no evidence
- *"Let me just try fixing X and see if it works."* → not a hypothesis, that's Phase 2 without Phase 1

### 3. Scope

Explicitly list:

- **In bounds**: `src/auth/middleware.ts`, `src/auth/session.ts`
- **Out of bounds**: anything in `src/features/`, any test file unrelated to auth, any dependency upgrade

If you find yourself wanting to edit an out-of-bounds file mid-Phase 2, **STOP** — that's scope creep. Either return to Phase 1 to expand scope with a reason, or leave it alone.

### 4. Success Criteria

How will Phase 3 verify this is fixed? Be concrete:

- ✅ "The integration test `auth.e2e.spec.ts → login redirect` passes"
- ✅ "Login from a cold browser session reaches `/dashboard` in ≤1 redirect"
- ❌ "It works" — not verifiable
- ❌ "Users can log in" — not specific enough

## Hypothesis Patterns

Common patterns that produce sharp hypotheses:

| Pattern | Template |
|---------|----------|
| **Timing/ordering** | "X happens before Y, but X depends on Y being complete" |
| **State leakage** | "X is read before it is set in the request lifecycle" |
| **Environment diff** | "Works in dev because X is set via `.env.local`, fails in prod because Railway env vars lack X" |
| **Off-by-one** | "The calculation uses Z index but iterates from Z+1" |
| **Missing invariant** | "The function assumes input is not null, but caller Y passes null" |
| **Contract mismatch** | "API returns snake_case, client expects camelCase" |

## Quality Check

Before exiting Phase 1, your hypothesis must pass:

- [ ] **Specific** — names exact files, functions, conditions
- [ ] **Falsifiable** — can be proven wrong by a concrete observation
- [ ] **Evidence-backed** — references something you actually observed (logs, test output, code reading)
- [ ] **Narrow** — one cause, not "maybe X or Y or Z"
- [ ] **Written down** — not just in your head

If any checkbox is unchecked, the hypothesis isn't ready. Sharpen it.

## Forbidden in Phase 1

- Editing code
- Running `npm install` / `pnpm install` / any setup command
- Running the build "to see"
- Running tests "to see what breaks"
- Multiple parallel hypotheses ("maybe it's A, or B, or C…") — pick one
- Skipping straight to Phase 2 because "it's obvious"

If the fix feels obvious, that's when discipline matters most. *Write the hypothesis anyway*. The 30 seconds of explicit thinking prevents the 30 minutes of retry-loop later.

## Exit Gate to Phase 2

You may proceed to Phase 2 **only when**:

1. ✅ Task is decomposed into independent units
2. ✅ Hypothesis is written, specific, falsifiable, evidence-backed
3. ✅ Scope is explicit (in-bounds + out-of-bounds)
4. ✅ Success criteria is concrete and verifiable

Otherwise: stay in Phase 1.

## Loop-back Triggers

Return to Phase 1 from any later phase when:

- Phase 2: you realize your hypothesis was wrong as soon as you start editing
- Phase 3: validation fails in a way that invalidates the hypothesis
- Phase 4: a fundamentally new hypothesis emerges — don't continue debugging the old one, start a new cycle

Looping back is cheaper than pushing through a wrong hypothesis.
