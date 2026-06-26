# Anti-Patterns

Concrete before/after examples of the 10 failure modes this pipeline prevents. Each example shows the broken behavior and the disciplined alternative.

## 1. Symptom Patching

**Broken:**

> *User:* "The login redirects in a loop."
> *Agent:* [edits middleware] "I hardcoded the redirect to `/dashboard` when the URL contains `/login`. Should work now."

The symptom is gone, but the cause (session not being read correctly) remains. The bug will resurface the moment anyone changes the middleware order.

**Disciplined:**

> *Phase 1:* "Hypothesis: login redirect loops because middleware reads `session` before next-auth has written the cookie on the callback response. Evidence: network tab shows no cookie on `/api/auth/callback` response."
> *Phase 2:* Edit `middleware.ts` to skip `/api/auth/*` paths.
> *Phase 3:* Verify the callback now sets the cookie, and subsequent requests have a valid session.

## 2. Multi-Fix Chaos

**Broken:**

> *Agent:* "I fixed the auth bug. I also cleaned up the session helper, upgraded `next-auth` to v5, and added logging. 14 files changed."

Now you can't tell which change fixed the bug. If it regresses later, there are 4 candidate causes.

**Disciplined:**

One fix per cycle. The cleanup, upgrade, and logging are three separate tasks. Each gets its own Planner → Coder → Validator pass.

## 3. Retry Loops

**Broken:**

> *Attempt 1:* "Let me add a `try/catch` around the API call."
> *Attempt 2:* "Hmm, that didn't work. Let me add a `try/catch` with a `setTimeout`."
> *Attempt 3:* "Let me wrap it in a `Promise.all` too."
> *Attempt 4:* "Let me also add a retry…"

No hypothesis change, no documentation, no learning.

**Disciplined:**

Each attempt has a new hypothesis backed by evidence from the previous failure. Attempt 3's hypothesis must be substantively different from attempts 1 and 2. After attempt 3, escalate.

## 4. Premature Coding

**Broken:**

> *User:* "Fix the date calculation bug."
> *Agent:* [opens `src/utils/date.ts` and starts editing immediately]

No hypothesis. No scope. No success criteria. Just vibes.

**Disciplined:**

> *Phase 1:* "What date calculation? Show me the failing test. Hypothesis: ISO week function uses `getDay()` returning 0 for Sunday instead of 6 for Sunday. Evidence: failing test case uses a date that is a Sunday."
> *Phase 2:* Narrow edit to the specific line.
> *Phase 3:* Run the failing test; verify it passes; run adjacent date tests to check for regressions.

## 5. Validation Skipping

**Broken:**

> *Agent:* "I fixed it. `pnpm build` succeeded. Done."

Build passing ≠ root cause fixed. The symptom could be hidden by a new bug you just introduced.

**Disciplined:**

Build ✓ is step 1 of Phase 3. Steps 2-6 (types, focused test, root-cause verification, scope check, regression check) are equally required. "It compiles" is never a completion signal.

## 6. Unbounded Debugging

**Broken:**

> *Agent:* [attempt 8] "Still not working. Let me try one more thing…"

No attempt log. No escalation. Context is burned. The human has no idea what's been tried.

**Disciplined:**

Max 3 attempts. Every attempt logged with hypothesis / change / result / why it failed / next direction. At attempt 3 failure, STOP and escalate with the full log.

## 7. Speculative Refactoring

**Broken:**

> *User:* "Fix the failing login test."
> *Agent:* "I fixed the test. I also noticed the auth module had a lot of duplication so I refactored it into a factory pattern. And I renamed some variables for clarity. And I extracted a helper. 600 lines changed."

Now the diff is unreviewable. You can't tell which change fixed the test and which was cosmetic.

**Disciplined:**

Scope in Phase 1 was "fix the failing login test". The refactor wasn't in scope. Log it as a `FEATURE_REQUEST` or TODO for a future separate task. Deliver the narrow fix.

## 8. Hypothesis Drift

**Broken:**

> *Phase 1 hypothesis:* "Redirect loops because the cookie isn't being set."
> *Phase 2:* [edits middleware, not cookie logic]
> *Phase 3:* "Works now. I think the real issue was middleware order, actually."

The hypothesis was retroactively changed to match the fix. This means Phase 1 was skipped in practice.

**Disciplined:**

If the fix didn't test the hypothesis, that's a signal: return to Phase 1, write the *new* hypothesis, start a fresh cycle. Don't rewrite history.

## 9. Type-Ignore Laziness

**Broken:**

```typescript
// @ts-ignore
const user = req.user;
```

No comment. No explanation. The type system was right, and you chose not to listen.

**Disciplined:**

```typescript
// @ts-expect-error — req.user is added by auth middleware at runtime; the Express type definition doesn't include it, but this handler is only reachable after the middleware runs.
const user = req.user;
```

One sentence explaining *why* the type system is wrong here. If you can't write the sentence, fix the types instead of suppressing them.

## 10. Scope Creep

**Broken:**

> *Task:* "Fix login redirect."
> *PR:* 14 files changed. Touches auth, middleware, layout, header component, README, package.json, and three unrelated tests.

Nobody can review this. Nobody knows what the actual fix was.

**Disciplined:**

Phase 1 scope: "in-bounds = `src/middleware.ts`, `src/auth/session.ts`. Out-of-bounds = everything else." Anything outside that list triggers either a hard stop (expand scope with an explicit reason + new Phase 1) or a separate task.

---

## Meta-Pattern

All 10 anti-patterns share a common thread: **the agent skipped or underdid a phase.** The pipeline is designed to be rigid so that the path of least resistance is the correct behavior:

- Phase 1 skipped → symptom patching, premature coding, hypothesis drift
- Phase 2 undisciplined → multi-fix chaos, speculative refactor, scope creep
- Phase 3 skipped → validation skipping, type-ignore laziness
- Phase 4 unbounded → retry loops, unbounded debugging

When in doubt: which phase were you in when the trouble started? Return to it.
