# From Bug Report to Verified Fix

Work symptom-first. Every chain below is ordered by probability, and every step is a check, not a guess. Isolation technique in depth — hypothesis discipline, delta debugging, time-travel tooling — is `debugging`; this is the developer's field route.

**Before the first command**, read `## Pain Points` in `~/Clawic/data/developer/memory.md`, the `## Gotchas` section of that repo's profile, and any `artifacts/runbook-*.md` the `## Boxes` index names for this symptom. A large share of repeat incidents are the same incident, and the runbook is faster than any chain here.

## Reproduce First, Always

A fix for a bug you never watched fail is a guess with a diff attached (SKILL.md Rule 1). Reproduce at the smallest scope that still fails, in this order:

1. **In a test.** Best case: the reproduction becomes the regression test and the verification in one artifact.
2. **In a script or a single request.** One command, one wrong output, no UI.
3. **In the running app with the reporter's exact input.** Slowest loop; use only when the input is the mystery.

If it will not reproduce, the difference between your run and theirs *is* the bug: input, data, permissions, time, locale, version, or concurrency. Enumerate those six against the report before touching code.

**Getting a usable report**: what they did, what happened, what they expected, when it started, whether it is every time, and the exact input. "It's broken" plus a timestamp plus a user id gets you the log line, which is usually enough.

## Bisect: the Cheapest Search There Is

Worked-then-broken is a solved problem. `git bisect start` / `bad <now>` / `good <known-good>` gives log₂(n) steps: 1,000 commits in 10 checks, 10,000 in 14. Automate it with `git bisect run <command>` where the command exits non-zero on the bug, and go do something else.

- Every commit must build for this to work — the reason for Rule 4 and for green-at-every-commit (`changes.md`).
- Merge commits muddy the result: `--first-parent` bisects the merge sequence instead of the internals.
- It lands on the commit that *exposed* the bug, not always the one that caused it. A commit that only added a caller is telling you the bug was already there and dormant.
- No git history to bisect? Bisect the surface instead: halve the input, halve the config, halve the enabled features.

## Chains by Symptom

### Wrong value out

1. Find the first place the value is wrong — print or breakpoint at input, midpoint, output; binary-search the pipeline, not the file.
2. At that point, check the three usual suspects: the type (string `"10"` vs number `10`), the unit (cents vs euros, ms vs s), and the boundary (inclusive vs exclusive).
3. Money wrong by cents → binary floating point; integers in minor units or a decimal type, never `float`.
4. Dates wrong by hours or one day → timezone. Store UTC, convert at the edges, and check whether "today" was computed in the server's zone or the user's. Anything that says `DATE(created_at)` in a query is a bug in most of the world.
5. Text wrong for some users → encoding or locale: byte length vs code points vs grapheme clusters, locale-dependent uppercasing (Turkish dotless `i`), collation in the database differing from the application's sort.

### Intermittent

The five sources, in order of frequency: shared mutable state, ordering, time, concurrency, randomness.

1. Does it fail alone? Run the single case 100 times in a loop. Passing alone but failing in a suite means shared state (`tests.md`).
2. Fix the clock and the seed. Anything using `now()` or an unseeded RNG is non-deterministic by construction; inject both.
3. Under load only → resource exhaustion before race: connection pool, file descriptors, thread pool. Little's law sizes the pool: `concurrency = arrival_rate × service_time` — 200 req/s at 50 ms needs 10 in-flight; a pool of 5 queues and then times out.
4. Real race → find the shared mutable thing crossing a boundary: a module-level variable, a cache, a database row read then written without a lock or a conditional update (`concurrency`).
5. Fails at a specific time of day, or once a month → cron overlap, token expiry, DST transition, month-end boundary, or a certificate.

### Cannot reproduce locally

Diff the environment in the fixed order in `environments.md`: runtime version, dependency versions from the lockfile, env vars, filesystem case sensitivity, clock and timezone, parallelism, data volume and shape.

### Regression after an upgrade

The lockfile diff, not the manifest diff — the change is nearly always transitive (`dependencies.md`). Then the changelog between the two exact versions, searching for the behavior you relied on. Semver minors break things in practice; that is a base rate, not an accusation.

### Slow, not wrong

Measure before touching (`performance.md`). The dominant cause in application code is round trips: N+1 queries, a call inside a loop, a synchronous request to another service per item.

### Crash or unhandled error

1. Read the whole stack trace, bottom-up: the deepest frame in *your* code is where to start, not the top of the trace.
2. The error type names the class before the message does: null/undefined access, type mismatch, index bound, timeout, connection refused, permission.
3. Cannot map the line number to your source → stale build, source maps, or a different file loaded. Prove the running code is your code by changing a message and watching it appear.

## Fault Localization Toolkit

| Tool | When it wins | Cost |
|---|---|---|
| Print/log | Loops, hot paths, non-attachable environments; a snapshot over time | Rebuild-run cycle per idea |
| Debugger breakpoint | One-shot inspection of a rich state you cannot serialize | Setup, and it lies under concurrency |
| Conditional breakpoint | The failure happens on iteration 4,000 | Slows execution significantly |
| Bisect | Worked before, broken now | Needs a reliable pass/fail command |
| Delete half the config/input | No history, no debugger, black box | Manual halving |
| Record/replay or time-travel | Non-reproducible and expensive per attempt | Tooling, overhead |
| Rubber duck | Twenty minutes stuck on something you can explain | Free; use before all of the above |

Timebox at ~30 minutes without a new hypothesis: at that point ask (`collaboration.md`), or list what you have eliminated in `## Open Threads` of `memory.md` and change technique. The stuck loop is re-testing an assumption you already tested.

## Verify the Fix

- The test fails without the change and passes with it — run both directions, not just the green one.
- The symptom the reporter described is gone, checked with their input.
- The class is checked, not just the instance: grep for the same pattern elsewhere.
- Nothing else moved: the rest of the suite is green, and you did not "fix" a test to match new behavior without deciding that was correct.

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Fixing what the report names | The report names the visible end, not the origin | Trace to the first wrong value |
| Changing several things at once | The bug goes away and you do not know which change did it — or two changes cancel out | One variable at a time |
| Adding a null check where the null appeared | Hides the fact that something upstream produced nothing | Fix the producer, or make it explicit and fail loudly (`error-handling`) |
| Widening a `try/catch` to make it stop | Converts a crash into silent wrong data | Catch the specific error where you can act on it |
| Trusting the comment or the docs | Both describe intent; the bug is where reality differs from intent | Trust the running code and the test |
| Debugging a build you did not just make | Stale artifacts, cached bytecode, the wrong container | Rebuild and confirm you are running your code |
| Declaring victory on the first green run | Intermittent bugs pass often | Run it 20 times, or fix the determinism first |

## Write Down What It Was

A cause that took more than a couple of minutes to find is worth more than the fix. Three destinations (`memory-template.md`):

- **A cross-repo cause** — a class of bug that will recur anywhere: one row in `## Pain Points` of `~/Clawic/data/developer/memory.md` with date, symptom, actual cause, what changed.
- **A cause specific to this codebase** — the env var that must be set, the stale-cache behavior, the ordering assumption: `## Gotchas` in `repos/<repo>.md`, where the next session will be looking.
- **The second time the same failure appears** it stops being a note and becomes `artifacts/runbook-<symptom>.md`: the ordered checks, the fix, and how to verify. Add its `## Boxes` line with a read condition naming the symptom, so the next session opens it before the chain above rather than after.
