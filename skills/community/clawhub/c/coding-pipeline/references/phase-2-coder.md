# Phase 2 — Coder

Deep-dive on the Coder phase. Read this when applying a change from a Phase 1 hypothesis.

## Purpose

Phase 2 is where the hypothesis from Phase 1 gets tested in code. The rule is **one fix, one purpose, one cycle**. The failure mode Phase 2 prevents is the "while I'm here" trap: you open the file to make the intended change, and you see three other things that bother you, and suddenly your diff touches 11 files and nobody can tell which change fixed the bug.

## Rules

### 1. One Fix at a Time

Exactly one logical change per cycle. A "logical change" is a single modification that either **proves or disproves the Phase 1 hypothesis**.

**Counts as one fix:**

- Edit one function in one file
- Add one guard clause where the hypothesis predicts null input
- Rename one variable if the hypothesis says a typo is the cause
- Edit multiple files if they're part of the same logical change (e.g. a type definition + its single consumer)

**Does NOT count as one fix:**

- "Fix the auth bug + clean up the tests + update the README"
- "Fix the calculation + refactor the helper + add logging"
- "Fix the type error + upgrade the dependency + remove the workaround"

Each of those is a separate Plan → Code → Validate cycle.

### 2. Full Files, Not Snippets

When showing your work, deliver complete file contents. Reasons:

- **Reviewability** — snippets hide context, full files don't
- **Confidence** — the reviewer knows nothing unrelated changed
- **Reversibility** — a full file is easy to revert; a snippet requires reconstructing the surrounding context

Exception: file is >500 lines and you only touched a small region — in that case, show the diff *plus* a note about what the surrounding code looks like.

### 3. No Speculative Refactoring

The temptation: *"This function is a bit messy, let me clean it up while I'm in here."*

**Do not.** That is a separate task. Log it as a feature request (`FEATURE_REQUESTS.md` if using `self-improving-agent`) or a TODO, but do not bundle it into the current fix.

Why it matters: speculative refactors change the behavior you're trying to observe in Phase 3. If the bug is fixed but you also moved 40 lines around, you have no way to know if the bug was fixed by your intended change or by the refactor.

### 4. Loop-Back on Uncertainty

If mid-change you realize **any** of:

- The hypothesis doesn't match what you see in the code
- You need to edit a file that wasn't in the Phase 1 scope
- The fix requires a deeper architectural change
- You don't actually understand why the current code looks the way it does

→ **STOP editing**. Return to Phase 1. Write a new hypothesis. Start a new cycle.

Continuing through uncertainty is how retry loops begin.

## Scope Discipline

If you find yourself:

- Opening files not in the Phase 1 scope
- Running `grep` or `find` to "explore" — that was Phase 1's job
- Adding imports for libraries you didn't touch
- Modifying tests to make the build pass rather than asserting the fix works

…you have drifted. Stop, return to Phase 1, expand scope explicitly with a reason, and start over.

## One-Fix Examples

### Example: Bug Fix

**Hypothesis from Phase 1:** *"Login redirect loops because middleware runs before next-auth sets its cookie."*

**Phase 2 (correct):**
- Edit `src/middleware.ts` — add skip condition for `/api/auth/*` routes
- Nothing else

**Phase 2 (wrong):**
- Edit `src/middleware.ts` + clean up unused imports in `src/auth/session.ts` + add missing types in `src/auth/callback.ts` + update the README auth section

### Example: Feature Addition

**Hypothesis from Phase 1:** *"Rate limiting on `/api/chat` will be enforced by sliding window counter in Redis."*

**Phase 2 (correct):**
- Edit `src/api/chat.ts` — wrap handler with rate limit middleware
- Add `src/lib/rate-limit.ts` — the sliding window implementation
- Nothing else

**Phase 2 (wrong):**
- All of the above + refactor the rest of the API routes to "be consistent" + add logging + update dependencies

## Exit Gate to Phase 3

Proceed to Phase 3 **only when**:

1. ✅ Exactly one logical change is applied
2. ✅ Diff is clean — no unrelated edits, no "while I was here"
3. ✅ Full files are available for review
4. ✅ You can point at the diff and say which line tests the Phase 1 hypothesis

Otherwise: revert speculative changes, narrow the diff, try again.

## Common Failures

- **Scope drift** — edit 7 files when Phase 1 planned 2
- **Bundled fixes** — two unrelated changes in one commit
- **Snippet delivery** — showing only the changed lines, hiding context
- **Refactor temptation** — cleaning up while "passing through"
- **Partial edits** — changing a function signature but forgetting one caller
- **Test amendments** — modifying the test to pass instead of making the code pass the test

Each of these invalidates Phase 3 because you can no longer tell what the fix was.
