# Phase 3 — Validator Checklist

Run through this every time, even when the change feels obviously correct. Skipping steps here is how symptomatic fixes ship.

---

## Build Check

- [ ] Build / compile succeeds without new errors
- [ ] No new warnings that weren't there before

Stack-specific commands:

| Stack | Command |
|-------|---------|
| TypeScript (NestJS, Next.js) | `pnpm build` or `npm run build` |
| TypeScript strict check | `tsc --noEmit` |
| Rust | `cargo build` |
| Go | `go build ./...` |
| Python | `python -m py_compile <file>` |
| PHP | `php -l <file>` |

## Type Check

- [ ] No new type errors
- [ ] Any `@ts-ignore` / `@ts-expect-error` / `type: ignore` has a **written justification comment** explaining why the type system is wrong here

If you can't write the one-sentence justification, fix the types instead of suppressing.

## Focused Test

- [ ] The specific test that proves the Phase 1 hypothesis is run and passes
- [ ] If no test existed yet, a new failing test was written first and now passes

NOT the full test suite — the targeted test that matches Phase 1's success criteria.

## Root-Cause Verification

**The symptom-vs-cause test.** Ask:

> "If I rolled back this change, would the symptom return **because of the same cause** I hypothesized — or because of something else?"

- [ ] You can answer this confidently
- [ ] The answer is "because of the same cause"
- [ ] The fix addresses the hypothesis, not a side effect

If you can't answer confidently → the fix is symptomatic. Return to Phase 1.

## Scope Verification

- [ ] Run `git diff --stat`
- [ ] The changed files match Phase 1's in-bounds list
- [ ] No unexpected files in the diff
- [ ] No files from the out-of-bounds list

If there are unexpected files: either justify each (and update Phase 1 retroactively with a reason) or revert them.

## Regression Check

- [ ] Adjacent tests in the same module still pass
- [ ] Happy path of the affected feature smoke-tested manually
- [ ] No new errors in logs during the smoke test

You don't need to run the full suite (CI does that). You do need to check the immediate neighborhood.

## Completeness Gate

- [ ] Build ✓
- [ ] Types ✓
- [ ] Focused test ✓
- [ ] Root cause verified ✓
- [ ] Scope matches plan ✓
- [ ] No regressions ✓

All six? → **Done.**

Any unchecked? → **Phase 4 Debugger.**

## Common Shortcuts That Fail

- ❌ "Build is green, that's enough" — skipping root-cause verification
- ❌ "Running tests would take forever" — you run the focused test, not the suite
- ❌ "The diff looks fine" — actually run `git diff --stat` and compare against Phase 1
- ❌ "It smoke tests okay" — without also checking root cause
- ❌ "I'll add the type justification later" — no, write it now or fix the types
