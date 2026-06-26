# Worked Examples

Three complete walkthroughs showing all 4 phases on real scenarios: a bug fix, a feature addition, and a refactor.

---

## Example 1: Bug Fix

**Scenario:** User reports that login from a cold browser session redirects in a loop between `/login` and `/api/auth/callback`.

### Phase 1 — Planner

**Task breakdown:**
- Reproduce in a cold browser session
- Understand which redirect is failing
- Identify what state is expected at each hop

**Hypothesis:**
> *I believe the login redirect loops because the `/api/auth/callback` response is not setting a session cookie, because the middleware is reading the request's session before the callback can write it.*

**Evidence:**
- Network tab shows `Set-Cookie: next-auth.session-token=...` missing on `/api/auth/callback` response
- Middleware logs show `session: null` on the request that follows the callback

**Scope:**
- **In**: `src/middleware.ts`, `src/auth/config.ts`
- **Out**: all route handlers, all UI components, test files other than `auth.e2e.spec.ts`

**Success criteria:**
- `auth.e2e.spec.ts → login redirect` passes
- Fresh browser session reaches `/dashboard` in ≤1 redirect after login
- Network tab shows the session cookie on the callback response

### Phase 2 — Coder

Edit `src/middleware.ts`:
- Add early return for `pathname.startsWith('/api/auth/')` before the session read
- Nothing else

Full file delivered, diff is 6 lines.

### Phase 3 — Validator

1. `pnpm build` ✓
2. `tsc --noEmit` ✓
3. `pnpm test auth.e2e.spec.ts → login redirect` ✓
4. **Root-cause verification**: the middleware no longer blocks the callback; the callback sets the cookie; the subsequent request carries the session. Verified via browser devtools.
5. **Scope verification**: `git diff --stat` shows only `src/middleware.ts` modified ✓
6. **Regression check**: adjacent tests (`auth.unit.spec.ts`, `middleware.spec.ts`) still pass ✓

**Done.** Phase 4 not needed.

---

## Example 2: Feature Addition

**Scenario:** Add rate limiting to the `/api/chat` endpoint — max 20 requests per minute per user.

### Phase 1 — Planner

**Task breakdown:**
- Choose a rate limit mechanism (in-memory vs Redis)
- Implement the limiter
- Wire it into the `/api/chat` handler
- Test both "under limit" and "over limit" cases

**Hypothesis:**

Note: for feature work, the hypothesis is about *how* to implement, not *why* something is broken.

> *The simplest correct approach is a sliding window counter in Redis, keyed by `chat:rate:{userId}`, with a 60-second TTL. Evidence: we already use Redis for sessions, so the infrastructure is in place; in-memory would fail on multi-instance Railway deployments.*

**Scope:**
- **In**: `src/api/chat.ts`, new file `src/lib/rate-limit.ts`, `src/api/chat.test.ts`
- **Out**: other API routes (intentional — do one at a time)

**Success criteria:**
- 20 requests in 60s succeed
- 21st request in 60s returns `429 Too Many Requests`
- Counter resets after 60s
- Redis calls add <10ms to p95 latency (measured locally)

### Phase 2 — Coder

One change:
- Create `src/lib/rate-limit.ts` with sliding window implementation
- Wrap `/api/chat` handler with the limiter

Nothing else — do NOT also refactor the existing handler, do NOT also add limits to other routes, do NOT also update logging.

### Phase 3 — Validator

1. `pnpm build` ✓
2. `tsc --noEmit` ✓
3. Tests:
   - `chat.test.ts → under limit` ✓
   - `chat.test.ts → over limit` ✓
   - `chat.test.ts → resets after window` ✓
4. **Root-cause / feature verification**: local load test with 21 requests in 60s — first 20 return 200, 21st returns 429 ✓
5. **Scope verification**: `git diff --stat` shows `src/api/chat.ts`, `src/lib/rate-limit.ts`, `src/api/chat.test.ts` — matches Phase 1 ✓
6. **Regression**: `/api/*` smoke tests pass ✓

**Done.**

---

## Example 3: Refactor

**Scenario:** A `validateUser()` function is duplicated (with minor variations) in 4 different service files. Consolidate.

### Phase 1 — Planner

**Task breakdown:**
- Identify the 4 call sites
- Find the common core and the variations
- Decide on the consolidated signature
- Migrate call sites one at a time

**Hypothesis:**

> *The 4 copies differ only in whether they throw or return null on invalid input. A single function with a `throwOnInvalid: boolean` option can replace all 4 with identical behavior. Evidence: read the 4 copies side-by-side; the core validation logic is byte-identical except for the error path.*

**Scope:**
- **In**: new file `src/shared/validate-user.ts`, `src/services/auth.service.ts`, `src/services/chat.service.ts`, `src/services/profile.service.ts`, `src/services/admin.service.ts`
- **Out**: any other service file, any test file beyond the 4 affected services

**Success criteria:**
- All 4 services import from `src/shared/validate-user.ts`
- Behavior of each service is unchanged (tests for each still pass)
- `git grep 'function validateUser' | wc -l` returns 1 (the shared one)

### Phase 2 — Coder

**Apply in sub-cycles.** A refactor touching 5 files is not "one fix" — it's 5 coordinated fixes.

Cycle 1:
- Create `src/shared/validate-user.ts`
- Migrate `auth.service.ts` to import from it
- Run `auth.service.test.ts` — passes

Cycle 2:
- Migrate `chat.service.ts`
- Run `chat.service.test.ts`

…and so on for each service.

Each cycle goes through Phase 2 → Phase 3 independently. If cycle 3 breaks, you don't have to re-do cycles 1 and 2.

### Phase 3 — Validator (per cycle)

For each cycle:
1. `tsc --noEmit` ✓
2. Service's own tests pass ✓
3. **Root-cause verification**: the service now uses the shared function; behavior matches the previous inline implementation (diff the outputs on a known input)
4. Scope verification: only the intended service file + the shared file changed in this cycle

### Final Validation

After all 4 sub-cycles:
- `git grep 'function validateUser' | wc -l` → 1 ✓
- Full test suite for affected services passes ✓
- No unrelated behavior changes (diff the API responses for a smoke test)

**Done.**

---

## Takeaways

- **Refactors are multi-cycle**, not one big change
- **Features and bug fixes are single-cycle** when scoped correctly
- **Phase 1 rigor scales down for trivial tasks** but never down to zero — even a typo fix should have an explicit scope ("this file, this line")
- **The pipeline is the cheapest path**, not the slowest — skipping phases wastes more time downstream
