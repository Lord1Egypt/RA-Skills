# Testing — Unit, Instrumented, Screenshot, and Flakiness

Android tests fail for two reasons: the code is wrong, or the test is. The second is more common, and it is fixable in a small number of known ways.

**Contents:** [The Three Tiers](#the-three-tiers) · [Unit Tests That Stay Fast](#unit-tests-that-stay-fast) · [Coroutines and Flows in Tests](#coroutines-and-flows-in-tests) · [Instrumented Tests](#instrumented-tests) · [Device Setup That Removes Flakiness](#device-setup-that-removes-flakiness) · [The Flakiness Checklist](#the-flakiness-checklist) · [Screenshot Tests](#screenshot-tests) · [What to Test on Android Specifically](#what-to-test-on-android-specifically) · [Testing Traps](#testing-traps)

**Before adding a test layer**, read `## Toolchain` and `## Pain Points` in `~/Clawic/data/android/memory.md`: a flaky test that was already diagnosed once should not be re-diagnosed, and the test-runner configuration that finally worked is part of the toolchain.

## The Three Tiers

| Tier | Runs on | Speed | Good for | Bad for |
|---|---|---|---|---|
| Local unit test | JVM | Milliseconds | Logic, ViewModels, repositories, mappers, serialization | Anything touching the framework for real |
| Local test with an Android simulation layer | JVM, framework simulated | Fast, seconds | Code that needs a `Context`, resources, or simple framework classes | Real rendering, real system behavior, OEM differences |
| Instrumented test | Device or emulator | Slow, tens of seconds up | UI flows, navigation, database migrations, permissions, real integration | Being the bulk of the suite |

The default distribution: most tests local, a thin instrumented layer over the critical user journeys, and screenshot tests for the visual regressions neither of the others catch. An instrumented-heavy suite is slow enough that people stop running it, which converts it into decoration.

## Unit Tests That Stay Fast

- A ViewModel is testable on the JVM only if it takes no `Context` and no framework types (`architecture.md`). If a test needs a simulation layer to construct the class under test, that is a design signal.
- Fakes over mocks for anything with behavior: a fake repository backed by an in-memory list produces readable tests and survives refactoring; a mock with five stubbed calls asserts the implementation, not the behavior.
- Inject the clock and the dispatchers. A test that waits for real time is slow now and flaky later.
- One assertion subject per test, named after the behavior. `loadFails_showsRetry` tells you what broke from the CI output alone; `test3` requires opening the file.
- Test the state object, not the interactions: given this input, the exposed state becomes that. That contract survives a UI rewrite.

## Coroutines and Flows in Tests

- Run suspending tests inside the coroutine test builder, which uses a virtual clock: delays are skipped, and a one-hour timeout takes microseconds.
- Replace the main dispatcher for the test's duration with a test dispatcher — the standard rule-based setup — or every ViewModel test fails with "no main looper".
- Two schedulers behave differently: a standard test dispatcher queues coroutines until you advance the clock (deterministic, and forces you to think about ordering); an unconfined one runs them eagerly (convenient, and hides ordering bugs). Default to the deterministic one.
- Flow assertions need a collector: a testing library that turns a flow into an awaitable sequence makes "emits loading, then content" a two-line test. Collecting into a list in a background job and sleeping is the flaky version of the same test.
- A test that passes alone and fails in the suite is nearly always shared state: a singleton, a real dispatcher, a static cache, or a database not reset between tests.

## Instrumented Tests

- Compose: the compose test rule with semantics-based finders; Views: the espresso-style framework with view matchers. Both auto-synchronize with the UI toolkit, and both fail when work happens outside their awareness.
- Find nodes by user-visible semantics — text, content description — or by an explicit test tag. Structural or index-based finders break on every layout change and produce the "someone changed the padding and forty tests failed" experience.
- Asynchronous work the framework cannot see (a real network call, a custom animator, a background thread) needs an idling mechanism or a `waitUntil` with a condition. A sleep is a guess that gets slower and flakier as the suite grows.
- Use the test orchestrator with per-test package clearing when tests interfere: each test runs in its own process invocation with fresh app data. It costs runtime and buys determinism, and it is the standard answer to "only fails when run after that other test".
- Gradle managed devices let the build declare the emulator specification, so CI and every developer run the same image instead of whatever was installed (`ci.md`).

## Device Setup That Removes Flakiness

Before any instrumented run, on every device and emulator:

- **Turn all three animation scales off.** Animations are the single largest source of instrumented-test flakiness; the frameworks wait for the UI to be idle and a running animation is never idle.
- **Disable the lock screen and keep the screen awake**, or half the suite fails on a device that locked mid-run.
- **Pin the locale, timezone and font scale** for the run. A test that formats a date passes in one locale and fails in another, and CI's locale is not your laptop's.
- **Grant the permissions the test needs** through the test rule rather than by tapping the dialog: the dialog is a different app's UI and interacting with it is fragile.
- **Reset app data between test classes** when state leaks, via the orchestrator rather than by hand.

Encode this in the test setup or the managed-device configuration, not in a wiki page — anything a human has to remember is a flaky test with a delay fuse.

## The Flakiness Checklist

When a test fails intermittently, in this order:

1. **Animations on?** Fix first; it explains most of them.
2. **Real time?** A `delay`, a `Thread.sleep`, a real dispatcher, a real clock.
3. **Shared state?** A singleton, a static, a database, a DataStore file, a mocked static not reset.
4. **Test order dependence?** Run the suite in a shuffled order; if that reproduces it, tests are leaking into each other.
5. **A real network or a real file system?** Any external dependency is a flake source; fake it.
6. **A race in the code under test?** Only after ruling out the five above — but if the same test flakes on slow devices only, this becomes the leading hypothesis, and the bug is real.
7. **Device conditions?** Low storage, thermal throttling, or an emulator without hardware acceleration.

A flaky test that is retried rather than fixed is a test that no longer reports anything. Quarantine it explicitly, with a date, rather than adding a blanket retry to the runner.

## Screenshot Tests

- JVM-side screenshot testing renders composables or views without a device, which makes visual regression cheap enough to run on every pull request.
- Golden images are checked in and reviewed like code; a diff in the review is the point. Regenerating goldens without reading the diff removes all value.
- Rendering differs subtly across environments (fonts, graphics libraries), so goldens must be generated in the same environment CI uses — usually a container. "Works on my machine" screenshot tests are worse than none.
- Cover the states that layout breaks in: longest translation, 200% font scale, dark theme, right-to-left, smallest supported width, and the empty and error states. Those six catch nearly every visual regression that reaches users.

## What to Test on Android Specifically

Beyond ordinary logic tests, the platform-specific things worth explicit tests:

| Area | Test |
|---|---|
| Room migrations | The migration helper: old schema, representative rows, run migration, assert data survived (`data.md`) |
| Process death | An instrumented test that saves and restores state, or the manual `am kill` check on the release checklist (`lifecycle.md`) |
| Deep links | Launch the activity with the real VIEW intent and assert the destination and arguments |
| Permission denial | The denied and permanently-denied paths, not only the granted one (`permissions.md`) |
| Workers | The WorkManager test harness with constraints and periodic intervals driven synchronously (`background.md`) |
| Serialization | Round-trip real payloads, including a response with missing and null fields (`networking.md`) |
| R8 output | At minimum, a smoke test running against the minified release variant — reflection breakage appears nowhere else (`release.md`) |
| Accessibility | The framework's accessibility checks enabled in instrumented tests: touch target size, contrast, missing labels |

## Testing Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Animations left on | Non-deterministic idling; the dominant flake cause | All three scales off, enforced in setup |
| `Thread.sleep` to wait | Slower every year and still flaky | `waitUntil` with a condition, or virtual time |
| Real dispatchers in ViewModel tests | Ordering becomes timing | Injected test dispatchers, main dispatcher replaced |
| Mocking everything | Tests assert the implementation and break on every refactor | Fakes for behavior, mocks for boundaries only |
| Structural or index-based UI finders | Break on every layout change | Semantics: text, content description, test tag |
| Instrumented tests as the bulk of the suite | Too slow to run, so nobody runs them | Thin instrumented layer over critical journeys |
| A blanket retry on the CI runner | Converts a real intermittent bug into a green build | Quarantine with a date and an owner |
| Golden screenshots regenerated without review | The regression is committed as the new truth | Read the diff; generate in the CI environment |
| Testing only the granted permission path | The denied path is what most users see | Test denial and permanent denial |
| No test on the minified release variant | R8 breakage is invisible until launch day | A smoke test against release |

## Write Down What It Was

- **A flaky test's real cause and the fix** goes to `## Pain Points` in `~/Clawic/data/android/memory.md`, with the test name — the same class of flake reappears in the next test someone writes (`memory-template.md`).
- **The test-runner and managed-device configuration that finally worked** belongs in `## Toolchain`, because it is part of the version set and it is re-derived painfully otherwise.
- **A quarantined test** needs a date and an owner somewhere durable: a line in `## Pain Points` at minimum, so the quarantine does not become permanent by silence.
