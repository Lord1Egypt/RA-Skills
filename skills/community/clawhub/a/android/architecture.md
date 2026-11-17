# Architecture — Layering, Dependency Injection, and Coroutines

Architecture on Android is mostly about two things: which object survives which death (`lifecycle.md`), and who is allowed to know about whom.

**Contents:** [Layers, and When to Add Them](#layers-and-when-to-add-them) · [UI State as One Object](#ui-state-as-one-object) · [Flows: Cold, Hot, and Lifecycle](#flows-cold-hot-and-lifecycle) · [One-Off Events](#one-off-events) · [Coroutine Scopes and Dispatchers](#coroutine-scopes-and-dispatchers) · [Error Handling](#error-handling) · [Dependency Injection](#dependency-injection) · [Offline-First](#offline-first) · [Architecture Traps](#architecture-traps)

Governed by `di_framework` and `module_layout`. Kotlin-language mechanics (coroutine internals, flow operators, null safety) belong to `kotlin`; this file is about the Android-shaped decisions.

**Before proposing a structure**, read `## Modules` in `~/Clawic/data/android/memory.md` and any `artifacts/adr-*.md` its `## Boxes` index names: the module graph and the layering decisions already made are the constraints, and re-deriving them produces a second, contradictory architecture.

## Layers, and When to Add Them

- **UI** (composables or views + a ViewModel) → **domain** (optional: use cases) → **data** (repositories, then data sources). Dependencies point one way only: UI knows domain, domain knows data interfaces, data knows nothing above it.
- The ViewModel exposes state and receives events. It never holds a `Context`, a `View`, a navigation controller or an Android framework type it did not need — that is what makes it testable on the JVM and what stops it leaking.
- Repositories own the decision of *where* data comes from (cache, network, database) and expose a single answer. A ViewModel that calls two data sources and merges them has absorbed the repository's job.
- **When to add the domain layer**: when a second consumer needs the same operation, or when a piece of logic combines two repositories. A use case per screen method, added on day one, is ceremony — a file that forwards one call.
- **When to add modules**: against measured build time (`gradle.md`), not against the layer diagram. Layers are a rule about direction; modules are a mechanism to enforce it and speed up builds.

## UI State as One Object

- One state class per screen, exposed as one `StateFlow`. Three separate flows for `isLoading`, `data` and `error` can express impossible combinations (loading and error at once) and produce two recompositions per update.
- Model exclusive states as a sealed hierarchy when they truly exclude each other (`Loading`, `Content`, `Empty`, `Error`); model independent flags as fields. A screen that can show content *and* a refresh spinner needs a field, not a sealed variant.
- Everything the screen renders comes from that object, including formatted strings' inputs — but not the strings themselves. Formatting with a `Context` in a ViewModel breaks configuration changes like locale and font scale; pass the id and the arguments and let the UI resolve them.
- The state object is the contract for tests: assert on states, not on view interactions.

## Flows: Cold, Hot, and Lifecycle

- Cold flows (`flow { }`, Room queries, Retrofit suspend wrappers) do nothing until collected, and each collector gets its own execution — two collectors of a network flow means two requests.
- `stateIn(scope, SharingStarted.WhileSubscribed(5_000), initial)` converts cold to hot, shares one upstream across collectors, and keeps it alive for five seconds after the last collector leaves. That timeout exists precisely so a configuration change (which unsubscribes and resubscribes within milliseconds) does not tear down and restart the upstream; a value of zero re-runs the query on every rotation, and `Eagerly` keeps it running forever.
- `StateFlow` always has a value, conflates (intermediate values can be skipped) and drops duplicates by equality — correct for state, wrong for events. If your data class does not implement `equals` sensibly, updates silently vanish.
- `SharedFlow` has no initial value and configurable replay — correct for events (below).
- Collect in the UI with `collectAsStateWithLifecycle()` (Compose) or `repeatOnLifecycle(STARTED)` (views). Both cancel collection when the UI stops; `collectAsState()` and the deprecated `launchWhenStarted` do not, which keeps the upstream working for a screen nobody is looking at.

## One-Off Events

Navigation, snackbars, toasts and "purchase succeeded" are events, not state: replaying them on recreation shows them twice.

- Preferred: keep them out of the ViewModel entirely by expressing them as state the UI consumes and acknowledges (`state.navigateTo != null` → navigate → `onNavigated()` clears it). Verbose, correct under every death.
- Common: a `Channel` consumed as a flow — a single consumer, buffered, so an event emitted while the UI is stopped is delivered when it returns. `SharedFlow` with `replay = 0` drops those events instead.
- Never `SharedFlow(replay = 1)` for events: the last one replays on every configuration change, and the user gets the snackbar again after every rotation.

## Coroutine Scopes and Dispatchers

| Scope | Cancelled when | For |
|---|---|---|
| `viewModelScope` | The ViewModel clears | Screen work; the default |
| `lifecycleScope` + `repeatOnLifecycle` | The lifecycle stops | Collection tied to visible UI |
| An application-scoped scope, injected | Never (process lifetime) | Work that must finish even if the user leaves — a write that was already accepted |
| `GlobalScope` | Never, and untestable | Nothing |

- Work that must survive the screen does **not** belong in `viewModelScope` — the classic bug is a save that is cancelled because the user navigated back the instant they pressed the button. Either an injected application scope or, if it must survive process death, WorkManager (`background.md`).
- Dispatchers: `Main` for UI, `IO` for blocking I/O (a large elastic pool sized well above the core count), `Default` for CPU work (sized to the cores). Suspend functions are main-safe by contract — the function switches internally with `withContext`, the caller does not have to know.
- Never hardcode a dispatcher in a class you want to test. Inject it, and substitute a test dispatcher (`testing.md`).
- Sequential `withContext(IO)` calls in a loop are still sequential; parallelism needs `async`/`awaitAll` or a flow operator that concurrently maps.

## Error Handling

- `launch` throws into the scope's handler and, without one, crashes; `async` holds the exception until `await`. An `async` whose result is never awaited swallows the failure entirely.
- A `CancellationException` is normal control flow. A `catch (e: Exception)` that logs and continues will swallow cancellation and keep a cancelled coroutine running — rethrow it, or catch the specific exception you expect.
- Map failures to state at the repository boundary: a domain `Result` type or a sealed error, never a raw `IOException` reaching the UI. The UI needs to know "retryable" versus "not", not the exception class.
- Retry with exponential backoff and a cap, only for transient failures, and never for a 4xx that will fail identically (`networking.md`).

## Dependency Injection

Governed by `di_framework`.

- **hilt** — annotation-processed, compile-time verified, with Android-aware components (application, activity, viewmodel, and their scopes). The build cost is real; the payoff is that a missing binding is a build error, not a crash.
- **koin** — a service locator with a DSL; no processor, faster builds, failures at first resolution rather than at compile time. Its verification test closes most of that gap and belongs in the test suite.
- **manual** — constructor injection with a hand-written container. Entirely viable for a small app, and the honest starting point: DI frameworks solve a graph-size problem you may not have.
- Whatever the choice: constructor injection everywhere, field injection only where the framework constructs the object (Activity, Fragment, Worker, Service). Scope things to the narrowest component that works — an application-scoped object holding screen state is a memory leak with extra steps.
- Interfaces at the boundaries you actually swap (data sources, dispatchers, clock). An interface with exactly one implementation and no test double is indirection with no payer.

## Offline-First

- The database is the single source of truth: the UI reads from Room, the network writes into Room, and the UI never reads a network response directly. Every screen then works offline for free, and there is one cache-invalidation story instead of one per screen.
- Writes queue as pending operations with an idempotency key so a retry after a crash cannot double-submit; the sync worker drains the queue (`background.md`, `data.md`).
- Conflict policy is a product decision made once and written down: last-write-wins, server-wins, or a merge. Undocumented, it becomes three different behaviors in three features.
- Show sync state explicitly. An app that silently discards a change the user made offline is worse than one that refuses to accept it.

## Architecture Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| `Context` in a ViewModel | Ties it to a lifecycle it outlives and breaks JVM tests | Pass what is needed, or use an application-scoped provider |
| Three flows for loading/data/error | Impossible combinations, extra recompositions | One state object |
| `SharedFlow(replay = 1)` for navigation | The event replays after every rotation | Channel, or state the UI acknowledges |
| `stateIn(..., WhileSubscribed(0), ...)` | Upstream restarts on every configuration change | `WhileSubscribed(5_000)` |
| Long-running work in `viewModelScope` | Cancelled when the user navigates away mid-save | Application scope, or WorkManager for durability |
| Hardcoded `Dispatchers.IO` inside a class | Untestable; tests become slow and flaky | Inject the dispatcher |
| `GlobalScope.launch` | Never cancelled, never tested, leaks | Any scope with an owner |
| A use case per ViewModel method on day one | Files that forward calls | Add the domain layer at the second consumer |
| Repository returning `LiveData` or a UI type | Couples data to a framework and to one consumer | Return a flow of domain types |
| Business logic in a composable or a Fragment | Untestable and re-executed unpredictably | ViewModel or plain functions |

## Write Down What It Was

- **A layering, DI or state-holder decision that took an argument to settle** is an `artifacts/adr-<name>.md` with its `## Boxes` line: this is the class of decision re-opened by every new contributor (`memory-template.md`).
- **The module graph** — which modules exist and which direction they depend — lives in `## Modules` of `~/Clawic/data/android/memory.md`, updated in the same turn a module is added, removed or renamed.
- **A concurrency bug whose cause was subtle** (a cancelled save, a swallowed exception, a flow that never restarted) is a line in `## Pain Points`; the same shape recurs in the next feature.
