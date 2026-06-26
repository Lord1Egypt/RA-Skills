# Phase 3 — Validator

Deep-dive on the Validator phase. Read this after applying a Phase 2 change.

## Purpose

Phase 3 is the hard check. Its job is to answer **"did this fix the root cause, or just the symptom?"** The failure mode it prevents is "it compiles, ship it" — where an agent runs the build, sees green, and declares victory without verifying that the original cause is actually addressed.

A fix that makes the symptom go away **without addressing the cause** is worse than no fix. It hides the bug and makes it return in a different form.

## Validation Checklist

Adapt to your stack. This is the minimum.

### 1. Build Check

The build/compile succeeds without new errors or warnings.

| Stack | Command |
|-------|---------|
| TypeScript (NestJS, Next.js) | `pnpm build` or `npm run build` |
| TypeScript strict | `tsc --noEmit` |
| Rust | `cargo build` |
| Go | `go build ./...` |
| Python | `python -m py_compile` + import check |
| PHP | `php -l <file>` + manual load |

If a new warning appeared that wasn't there before: investigate. Do not suppress.

### 2. Type Check

No new type errors. Any `@ts-ignore`, `@ts-expect-error`, `// eslint-disable`, `type: ignore`, or equivalent **requires a written justification comment** — one sentence explaining *why* the type system is wrong here.

Unjustified type ignores are a Phase 1 violation: they mean you don't actually understand what the code is doing.

### 3. Focused Test

Run the **specific test** that proves the Phase 1 hypothesis. Not the full suite. The full suite takes longer and obscures which check matters.

If no test exists yet for this hypothesis, write one now — a failing test that exercises the specific cause you hypothesized, then re-run it to confirm the fix made it pass.

### 4. Root-Cause Verification

This is the phase's core job. Ask:

> **"If I rolled back this change, would the symptom return *because of the same cause* I hypothesized — or because of something else?"**

If you can't answer confidently, the fix is symptomatic. Return to Phase 1.

**Examples:**

| Symptom | Symptomatic fix | Root-cause fix |
|---------|-----------------|----------------|
| Login redirect loops | Hardcode `redirect: '/dashboard'` in middleware | Fix the cookie-setting order so middleware can read the session |
| Off-by-one date | Subtract 1 day everywhere | Fix the ISO-week function to use Monday=0 |
| Type error in API call | `as any` cast | Fix the response type definition to match actual API shape |
| Test fails on CI but passes locally | `.skip()` the test | Fix the timezone assumption that only breaks outside Europe |

### 5. Scope Verification

Run `git diff --stat`. The changed files should match what Phase 1 planned. If there are extra files:

- **Expected extras** (imports, type files the hypothesis implied) → fine, note them
- **Unexpected extras** → scope creep. Revert them or explain why they were necessary.

### 6. Regression Check

Did anything adjacent break? Minimum:

- Run tests in the same module (`src/auth/*.test.ts`)
- Smoke-test the happy path of the affected feature manually
- Check for new errors in log output during the smoke test

You don't need to run the whole test suite — that's CI's job. You *do* need to check that nothing in the immediate neighborhood is broken.

## The Symptom-vs-Cause Test in Practice

The most reliable signal that a fix is symptomatic:

- **You can describe what the code now does, but not why the original code was wrong.**

If that's true, you didn't fix the cause. You fixed a coincidence. The bug will come back.

**Good diagnostic questions:**

- "Why was the original code doing X?" — if you don't know, you're patching blind
- "What assumption was being violated?" — name it
- "Why did this work before?" — if it did, something changed; what?
- "Could this same cause produce a different symptom elsewhere?" — if yes, there are related bugs

## Exit Gate to "Done"

The task is complete **only when**:

1. ✅ Build passes, no new errors/warnings
2. ✅ Types pass, no unjustified suppressions
3. ✅ The focused test proves the hypothesis
4. ✅ Root cause is verified — the fix addresses the Phase 1 hypothesis, not a coincidence
5. ✅ Diff matches Phase 1 scope
6. ✅ No regressions in the adjacent area

Otherwise → **Phase 4 Debugger**.

## Common Failures

- **Build green = done** — skipping root-cause verification
- **Unjustified type suppression** — `@ts-ignore` without a comment
- **Symptom tests** — asserting the symptom is gone instead of asserting the cause is addressed
- **Scope creep accepted** — noticing extra files in the diff and shrugging
- **Regression blindness** — not checking adjacent code at all
- **Full-suite churn** — running 2000 tests to feel confident when 3 targeted tests would prove it

Each of these means Phase 3 was skipped, not completed.
