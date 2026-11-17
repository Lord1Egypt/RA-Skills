# Jetpack Compose — State, Recomposition, and Performance

Compose is a function of state to UI, re-executed when state changes. Almost every Compose bug is a wrong answer to "what exactly changed, and what does the framework think changed".

**Contents:** [The Three Phases](#the-three-phases) · [State: Which Holder for Which Lifetime](#state-which-holder-for-which-lifetime) · [Recomposition Scope](#recomposition-scope) · [Stability and Skipping](#stability-and-skipping) · [Side Effects](#side-effects) · [Lists](#lists) · [Modifier Order](#modifier-order) · [Deferred Reads for Animation and Scroll](#deferred-reads-for-animation-and-scroll) · [Performance Work](#performance-work) · [Testing and Previews](#testing-and-previews) · [Compose Traps](#compose-traps)

Applies when `ui_toolkit` is `compose` or `both`. Interop with the View system and the migration order: `views.md`.

**Before a performance or state fix**, read `## Pain Points` in `~/Clawic/data/android/memory.md` and any `artifacts/adr-*.md` its `## Boxes` index names for a design-system or adoption decision: an unstable type from a specific library, or a rule about how screens are built here, is recorded once and applies to every screen after it.

## The Three Phases

Composition (what to show) → Layout (where and how big) → Drawing (pixels). Each frame runs only the phases that were invalidated.

- Reading a state value inside a composable function body invalidates **composition** when it changes — the most expensive of the three.
- Reading it inside a lambda-based modifier (`Modifier.offset { }`, `Modifier.graphicsLayer { }`, `drawBehind { }`) invalidates only **layout** or **drawing**.
- The optimization that matters more than any other in Compose is moving a frequently-changing read from the first category to the second (→ Deferred Reads).

## State: Which Holder for Which Lifetime

Answer both survival questions for every piece of state (SKILL.md Rule 4).

| Holder | Survives recomposition | Survives config change | Survives process death | Use for |
|---|---|---|---|---|
| Plain local `val`/`var` | No | No | No | Derived values cheap enough to recompute |
| `remember { }` | Yes | No | No | Anything expensive to build, scroll and animation state |
| `rememberSaveable { }` | Yes | Yes | Yes | Small UI state the user would notice losing: text in a field, selected tab, expanded row |
| `ViewModel` | Yes | Yes | No | Screen state, in-flight work, anything scoped to the screen |
| `SavedStateHandle` in a ViewModel | Yes | Yes | Yes | The ids and arguments needed to rebuild screen state |
| Repository / database | Yes | Yes | Yes | The truth |

- `remember(key)` recomputes when the key changes. `remember { mutableStateOf(x) }` with `x` from a parameter does *not* update when the parameter changes — that is the single most common state bug in Compose. Either key the remember, or derive instead of storing.
- `rememberSaveable` needs its value to be `Bundle`-storable, or a custom `Saver`. It rides the same ~1 MB Binder budget as the rest of saved state, so it holds ids and flags, never lists of objects.
- `derivedStateOf` is for the case where a *frequently* changing state produces a *rarely* changing derived value: `val isAtTop by remember { derivedStateOf { listState.firstVisibleItemIndex == 0 } }` recomposes readers when the boolean flips, not on every scroll pixel. Using it for cheap derivations that change as often as their inputs adds overhead and no benefit.

## Recomposition Scope

- The smallest unit that can be re-executed is the enclosing composable function that reads the state. State read high in the tree recomposes everything below that is not skippable.
- Two fixes, in order: **read the state lower** (pass a lambda that reads it, not the value) and **hoist the state up** so the reading composable is a small leaf. Wrapping things in extra composables is not a fix by itself; moving the *read* is.
- State hoisting rule: a composable that owns state cannot be reused or tested with different state. Hoist until the composable takes `value` and `onValueChange` — then it is a function, and functions are testable.
- Passing a lambda that captures changing state defeats skipping unless the lambda is stable. In Kotlin 2.0's compose compiler with strong skipping, lambdas are remembered automatically; on older setups, `remember` the lambda or pass a method reference.

## Stability and Skipping

The compiler skips a composable when all its parameters are stable and unchanged.

- **Stable**: primitives, `String`, function types, `@Immutable`/`@Stable` annotated types, and classes whose public properties are all `val`s of stable types.
- **Unstable, and it surprises people**: any interface type in a parameter position, including `List`, `Set`, `Map` — the compiler cannot know the implementation is immutable. Also any class with a `var`, and any class from a module the Compose compiler did not process.
- Fixes, cheapest first: mark the type `@Immutable` when it truly is; use an immutable collection type from `kotlinx.collections.immutable`; or wrap the list in a stable data class. Never fix it by adding `key(...)` around the call — that changes identity, not stability.
- Strong skipping mode (default from the Kotlin 2.0 compose compiler) skips composables with unstable parameters by comparing instance equality, which removes most of this class of problem — but a new list instance built in the caller on every recomposition still fails the comparison. The upstream fix is to stop rebuilding the list.
- Diagnose with the compiler's stability report or the Layout Inspector's recomposition counts. A composable with a count climbing during idle is the bug; a count that matches user actions is fine.

## Side Effects

| Effect | Runs | Use for |
|---|---|---|
| `LaunchedEffect(key)` | On first composition and whenever `key` changes; cancelled on leaving composition | Starting a coroutine tied to the composable: loading, animating, snackbars |
| `DisposableEffect(key)` | Same lifecycle, with an `onDispose` block | Registering and unregistering listeners, sensors, broadcast receivers |
| `SideEffect` | After every successful composition | Publishing state to non-Compose code |
| `rememberCoroutineScope()` | Gives a scope tied to the composition | Launching from a click handler — never `LaunchedEffect` for user events |
| `rememberUpdatedState(value)` | Keeps a long-lived effect reading the latest value without restarting | A callback captured by a `LaunchedEffect(Unit)` that must not restart |
| `produceState` | Converts non-Compose state into Compose state | Bridging a callback API |

- `LaunchedEffect(Unit)` runs once per composition entry and never restarts — correct for a one-shot, wrong whenever it captures something that changes. That capture bug is why `rememberUpdatedState` exists.
- Never launch work from the body of a composable. The body runs an unknown number of times.
- Collect flows with `collectAsStateWithLifecycle()`, not `collectAsState()`: the plain version keeps collecting while the app is in the background, burning battery and pushing updates at a UI nobody is looking at (`architecture.md`).

## Lists

- Give `LazyColumn`/`LazyRow` items a **stable `key`**. Without it, reordering or removing an item shifts every item's identity: `remember`ed state, animations and scroll position attach to the wrong row. This is the difference between a checkbox staying with its item and jumping to another.
- `contentType` on heterogeneous lists lets the framework reuse compositions of the same shape; without it, a mixed list recomposes more than it needs to.
- Never put a `LazyColumn` inside a vertically scrolling parent — it has infinite height available and the framework throws. Use one lazy container with typed sections instead.
- Paging: load ahead of the viewport, keyed by a stable id, and let the list keep its scroll position across configuration change by keying on ids rather than indices.
- Item animation (`animateItem`) requires the stable key to work at all.

## Modifier Order

Modifiers apply in order, outside in, and the order is semantics, not style:

- `Modifier.padding(8.dp).background(Red)` paints red *inside* the padding; `Modifier.background(Red).padding(8.dp)` paints red including it.
- `Modifier.clickable { }.padding(16.dp)` makes the padding part of the touch target; reversing it shrinks the target to the content — the most common accessibility defect in Compose code. Minimum comfortable touch target is 48 dp; check it on the outermost clickable, not on the icon.
- `Modifier.size()` before `padding` sets the outer size; after, it sets the content size and the composable grows.
- Any modifier that must apply to the whole component, including its click ripple and semantics, goes at the front of the chain the caller passes in — which is why every reusable composable takes `modifier: Modifier = Modifier` as its first optional parameter and applies it first.

## Deferred Reads for Animation and Scroll

The single highest-leverage Compose performance technique:

- Reading a rapidly changing value in the composable body recomposes on every frame of the change. Reading it in a lambda modifier skips composition entirely.
- `Modifier.offset { IntOffset(x.roundToPx(), 0) }` (lambda form) rather than `Modifier.offset(x)`; `Modifier.graphicsLayer { alpha = progress }` rather than `Modifier.alpha(progress)`.
- Scroll-driven effects read `listState.firstVisibleItemScrollOffset` inside `graphicsLayer`/`drawBehind`, or behind a `derivedStateOf` that only flips a boolean.
- Same rule for text that changes per frame: keep it out of the recomposing body when it is decorative, or accept composition and make the subtree tiny.

## Testing and Previews

- `createComposeRule()` for composables with no Activity dependency; `createAndroidComposeRule<T>()` when the composable needs one.
- Find nodes by semantics, not by structure: `onNodeWithText`, `onNodeWithContentDescription`, or `testTag` for things with no user-visible label. A test that navigates the node tree by index breaks on every layout change.
- The rule auto-syncs with the composition; when work happens outside Compose's awareness (a real network call, an external animator), `waitUntil` with a condition beats a sleep. Idling problems in Compose tests are usually an infinite animation keeping the clock busy — `mainClock.autoAdvance = false` gives manual control.
- `@Preview` with `@PreviewParameter` for state variants; multi-preview annotations for font scale, dark theme and device size. Previews are the cheapest place to catch a layout that breaks at 200% font scale, which is a real accessibility requirement and a real crash source when text is constrained.
- Screenshot tests over JVM-side renderers catch visual regressions without a device (`testing.md`).

## Compose Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| `remember { mutableStateOf(param) }` | Ignores every later value of `param` — the state is frozen at first composition | Key the remember, or derive the value instead of storing it |
| `mutableStateOf` without `remember` | Re-created on every recomposition; the state resets constantly | `remember { mutableStateOf(...) }`, or hoist it into a ViewModel |
| `collectAsState()` on a screen flow | Collects while backgrounded | `collectAsStateWithLifecycle()` |
| No `key` on `LazyColumn` items | State and animations attach to positions, not items | Stable `key = { it.id }` |
| `LaunchedEffect(Unit)` capturing a changing lambda | The effect keeps calling the first version forever | `rememberUpdatedState`, or key the effect properly |
| Business logic in the composable body | Runs an unknown number of times, in an undefined order | ViewModel or a plain function called from an effect |
| Wrapping a list parameter in a new `listOf()` at the call site | New instance every recomposition defeats skipping regardless of stability annotations | Hoist the list, or use an immutable collection type |
| Nested scroll containers of the same axis | Infinite constraints, immediate crash | One lazy container with sections |
| Reading a scroll offset in the composable body for a parallax effect | Recomposes the whole subtree every frame | Read it inside `graphicsLayer` (→ Deferred Reads) |
| Benchmarking Compose on a debug build | Debug Compose runs with extra checks and no R8; numbers are meaningless | Release variant, with a baseline profile (`performance.md`) |
| Skipping baseline profiles | Compose code ships as bytecode with no ahead-of-time compilation; first-run screens are visibly slower | Generate and ship a profile, regenerate when the UI changes materially |

## Write Down What It Was

- **A recomposition or stability problem whose cause was not obvious** — an unstable parameter from a specific library, a list rebuilt in a caller — is a line in `## Pain Points` of `~/Clawic/data/android/memory.md`, because the same pattern recurs across screens (`memory-template.md`).
- **A measured jank or frame-timing number** goes to `benchmarks/<year>.md` with the device and build variant, never into prose.
- **A decision about Compose adoption, interop boundaries or a design-system rule** is an `artifacts/adr-<name>.md` with its `## Boxes` line — it is the argument that otherwise gets re-litigated every quarter.
