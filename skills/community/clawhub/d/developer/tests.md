# Tests Worth Keeping

A test earns its place by catching a regression you would otherwise ship, or by making a change safe to attempt. Tests that do neither are cost with a green checkmark.

**Before writing tests here**, read `## Flaky Tests` and `## Conventions` in `~/Clawic/data/developer/repos/<repo>.md`: test style, location and runner are repo decisions, and a known flake in the area you are about to touch will otherwise be blamed on your change.

## What To Test, In Priority Order

1. **The bug you just fixed.** Non-negotiable, and it is already written if you followed Rule 1 (`bugs.md`).
2. **Behavior at the boundary you would hate to break** — the money path, the auth check, the data write. One integration test through the real seam beats ten unit tests of its parts.
3. **The branches a human would get wrong**: empty, one, many, max, negative, null, duplicate, out of order, unicode, concurrent.
4. **The contract with anything you do not control**: the API shape you emit, the schema you consume. A contract test fails at build time instead of at their deploy.
5. **Nothing else by default.** Getters, framework wiring, and constructors do not fail in ways tests catch.

## The Pyramid, Priced

Mike Cohn's shape holds for a reason that is economic, not aesthetic: the higher the test, the more it covers and the more it costs per run and per failure.

| Level | Runs in | Catches | Costs |
|---|---|---|---|
| Unit | milliseconds | Logic errors in one unit | Nothing — but passes while the system is broken |
| Integration (real DB, real HTTP boundary) | ~0.1-2 s | Wiring, SQL, serialization, transactions — where most real bugs live | Setup, and it is where flakes appear |
| End-to-end | seconds to minutes | The path the user actually takes | Slow, brittle, and expensive to diagnose |

Sizing rule: keep the whole suite under the time the team will actually wait — about 10 minutes for CI, under ~1 minute for the loop you run while coding. When it crosses that, split into a fast suite on every push and a slow suite on merge, rather than deleting coverage. Ten end-to-end tests covering the ten paths that produce revenue beat two hundred covering everything.

## Structure of a Test That Helps

- **Name it as the behavior**: `returns_empty_cart_total_as_zero`, not `test_cart_2`. The name is what you read in a CI failure at 6pm.
- **Arrange, act, assert, one act.** Multiple acts in one test means the failure does not name the cause.
- **One reason to fail.** Multiple assertions are fine when they describe one behavior; assertions about unrelated things belong in separate tests.
- **Assert on behavior, not on how it was achieved.** A test that asserts a private method was called breaks on every refactor and catches nothing — this is what "tests slow us down" actually refers to.
- **No logic in the test.** A loop or a conditional in a test means the test needs a test. Table-driven cases are the exception, with the case name in the failure output.
- **Fixtures build the case, not the world.** A shared 300-line fixture makes every test depend on data no one understands; build the minimum in the test and make the difference visible.

## Mocking: the Boundary Rule

Mock what you do not own and cannot run: third-party HTTP, payment providers, email, the clock, randomness. Do not mock your own domain objects, your own database, or the layer under test.

| Situation | Do |
|---|---|
| External HTTP API | Stub at the HTTP layer with a recorded response; a contract test hits the real one on a cadence |
| Database | Use a real one — containerized, migrated, seeded. In-memory substitutes have different SQL and pass while production fails |
| Time | Inject a clock; never `sleep()` in a test |
| Randomness / UUIDs | Seed it, or accept any value and assert the shape |
| A collaborator you own | Use the real one; if that is too slow, the design is telling you something (`changes.md`) |
| Something not written yet | A fake with real behavior, not a mock asserting calls |

The mockist failure mode is a suite that is green while the system is down. The classicist failure mode is a suite too slow to run. Pick the one whose failure mode you can live with, and be consistent within a repo.

## Flaky Tests

A flake is an outage of the test suite: it teaches the team to ignore red, and after that, real failures ship. At Google's scale ~1.5% of test runs flaked and most pass→fail transitions were not caused by the change under test.

Protocol, in order:
1. **Confirm** by running the test alone 50-100 times and the suite twice with different ordering and seeds.
2. **Classify**: shared state, ordering, real clock, real network, concurrency, or unseeded randomness — those five plus one cover nearly all of them.
3. **Quarantine with an owner and a deadline** — out of the blocking suite, still running and reported. A quarantine with no name and no date is a deletion nobody voted for.
4. **Record it** in `## Flaky Tests` of the repo profile with the symptom and suspected cause; a flake seen twice by two people is otherwise diagnosed twice.
5. **Never** wrap it in an automatic retry. Retry-until-green hides a real race about half the time, and the race is in production too.

## Coverage and Its Limits

Coverage tells you a line executed. It never tells you anything was asserted — a suite with no assertions can reach 100%.

- Useful gate: **changed-lines coverage** on the diff (governed by `coverage_policy`). It asks "did you test what you wrote", which is answerable and fair.
- Global percentage targets get met by testing what is easy: getters, generated code, `__str__`. The number goes up and the risk does not move.
- Where correctness is load-bearing — pricing, auth, permissions — mutation testing is the honest measure: it changes the code and checks whether a test notices. Run it on one module, not the repo.
- Uncovered code that handles money, permissions, or data deletion is a finding regardless of the overall number.

## Repairing a Repo With No Tests

1. Do not backfill. Add a test with every change, starting with the bug you are fixing.
2. First get *one* test running end to end in CI — the harness, the database, the fixture. That first hour buys every test after it.
3. Characterize before you refactor: assert current behavior, bugs included, so the refactor is provably behavior-preserving (`legacy-code`).
4. Prioritize by blast radius: the money path and the auth path first, the admin report last.

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Testing the implementation | Every refactor turns the suite red without a single bug | Assert observable behavior at the boundary |
| One giant test that walks the whole flow | When it fails you learn "something broke" | One behavior per test, plus one happy-path E2E |
| `sleep(2)` to wait for something | Flaky and slow at once; the number is wrong on a loaded CI box | Poll with a timeout, or inject the clock |
| Sharing state between tests to go faster | Order dependency, and it fails only in CI where order differs | Fresh state per test; transaction rollback if the DB is the cost |
| Asserting on the whole serialized object | Breaks on every unrelated field addition | Assert the fields the behavior is about |
| Snapshot tests everywhere | Nobody reads a 400-line diff; it gets updated blindly | Snapshots only for output whose shape is the contract |
| Deleting a failing test to unblock the build | Deletes the signal, keeps the bug | Quarantine with owner and deadline, or fix the code |
| Writing tests after the PR is approved | They get written to match the code, not the requirement | Test alongside; `workflow` decides before or during |

## Write Down What Came Out Of It

- A test found flaky, quarantined, or fixed → `## Flaky Tests` in `~/Clawic/data/developer/repos/<repo>.md` with symptom, suspected cause, owner and deadline (`memory-template.md`).
- Suite wall time, or the cost of the slow part → `## Baselines` in the same profile, so "the tests are slow" becomes a number with a date.
- A testing convention this repo enforces (where tests live, which runner flags, what CI blocks on) → `## Conventions` in the profile.
