# Architecture — State Management, Layering, and Dependency Injection

Everything here follows one question: **who owns this state, and who is allowed to rebuild when it changes?** Library choice matters less than answering that consistently. Read `state_management` and `project_layout` from config before proposing a structure (SKILL.md Configuration); with `auto`, read `pubspec.yaml` and match what the repo already uses.

## Choosing the Scope

| State | Lives in | Signal you chose wrong |
|---|---|---|
| Only this widget cares (a toggle, a text controller, an animation) | `StatefulWidget` + `setState` | You are threading a callback through three widgets to change it |
| Two sibling subtrees read it (a filter and a list) | A notifier above their lowest common ancestor | Parent rebuilds the whole screen on every keystroke |
| Whole app reads it (session, theme, locale, connectivity) | An app-level provider or repository | You pass it into every route's constructor |
| Server data with loading and error states | A repository + an async-aware provider or bloc | Every screen re-implements loading, retry, and caching |
| Only this route cares, and must die with it | A route-scoped provider (`autoDispose`, or a provider inside the route's subtree) | Stale data appears when you reopen the screen |
| Ephemeral form draft | `StatefulWidget` until it must survive navigation | The draft clears when the keyboard opens (`state.md` element reuse) |

Prefer the lowest scope that works. Global state is the default in the codebases that are hardest to change, and lifting state one level too high is the most common cause of "everything rebuilds".

## The Rule That Crosses All Libraries

**Watch in `build`, read in callbacks, listen for side effects.**

- `build` may only WATCH (subscribe): `context.watch`, `ref.watch`, `BlocBuilder`. Watching is what creates the dependency that rebuilds you.
- Callbacks (`onPressed`, `onChanged`) must READ without subscribing: `context.read`, `ref.read`, `context.read<Bloc>().add(...)`. Watching inside a callback either throws or silently adds a dependency you did not want.
- Navigation, snackbars, dialogs, and analytics go through a LISTENER: `ref.listen`, `BlocListener`, `addListener`. Never in `build` (SKILL.md rule 8), because a rebuild would fire them again — the "my dialog opens twice" bug.

## Per-Library Traps

**`ChangeNotifier` / Provider**

- `notifyListeners()` inside the constructor or during a build fires "setState() or markNeedsBuild() called during build". Defer with `Future.microtask` or move the trigger to a callback.
- `notifyListeners()` after `dispose()` throws. A notifier owned by a route outlives an in-flight request unless you guard or cancel.
- `Provider.of<T>(context)` subscribes by default. `listen: false` is the callback form; `context.read<T>()` is the same thing spelled better.
- `context.select<Model, String>((m) => m.name)` rebuilds only when that field's `==` result changes — the cheapest rebuild-narrowing in Provider (Rebuild Scope Ladder rung 4).
- `ProxyProvider` recreates its object whenever a dependency changes; if that object holds a subscription, it leaks unless `dispose:` is supplied.

**Riverpod**

- `ref.watch` in `build` and in provider bodies; `ref.read` only inside callbacks. `ref.read` in a provider body silently freezes the dependency at first read — the "why doesn't it update" report.
- `autoDispose` disposes the provider when the last listener leaves. That is correct for screen-scoped data and wrong for a session; use `ref.keepAlive()` for the exceptions rather than dropping `autoDispose` everywhere.
- `ref.listen` for side effects; `ref.watch` inside a listener callback is a bug.
- Provider identity is the provider object, not its type: creating a provider inside a build method makes a new one every rebuild.

**Bloc / Cubit**

- `emit` after `close()` throws `StateError`. Any async handler must check `isClosed` before emitting.
- Emitting an object that is `==` to the current state is ignored. A mutated list emitted back to itself changes nothing on screen — emit a copy (`List.of(items)`) or use value equality on an immutable model.
- `BlocProvider.of<T>(context)` needs a context BELOW the provider; calling it in the same widget that creates the provider throws. Wrap with a `Builder`.
- `buildWhen`/`listenWhen` are the rebuild filters; without them a status-only change rebuilds the entire screen.
- One bloc per feature, not per widget: a bloc whose only consumer is one widget is a `StatefulWidget` with extra files.

**Plain `InheritedWidget`**

- Still correct for a small, stable dependency (a theme extension, a config object). `updateShouldNotify` decides who rebuilds; returning `true` unconditionally rebuilds every dependent on every parent rebuild.
- `dependOnInheritedWidgetOfExactType` in `initState` does not subscribe — that is what `didChangeDependencies` is for (`state.md`).

## Layering

Three layers earn their keep in any app past a few screens; more layers than this need a specific reason.

```
ui/            widgets, screens — no HTTP, no SQL, no dart:io
  ↓ reads view state, sends intents
application/   notifiers, blocs, view models — orchestration, no framework types
  ↓ calls
data/          repositories → API clients + local stores; owns DTOs and mapping
```

- The rule that makes layering real: **domain models never carry JSON**. Parse a DTO at the data boundary and map it to a model the UI understands; otherwise a field rename in the API reaches into widget code.
- Repositories return domain types and throw domain failures — not `DioException`, not `SocketException`. Translation happens where the client lives (`data.md`).
- `application/` must not import `package:flutter/material.dart`. If it needs `BuildContext`, the side effect belongs in the UI layer.
- `project_layout: feature-first` puts these three folders inside each feature (`features/checkout/{ui,application,data}`) and keeps a `core/` for shared plumbing; `layer-first` puts features inside each layer. Feature-first survives growth better because a feature can be deleted in one move; layer-first reads better in an app with fewer than a handful of features.

## Dependency Injection

- Constructor injection is the baseline: a class that takes its dependencies is testable without any framework.
- A service locator (`get_it`) is the pragmatic top-level wiring: one `setup()` at startup, no `BuildContext` needed in the data layer. Its cost is compile-time invisibility — a missing registration is a runtime error, so register everything in one file and cover it with a startup test.
- Scoped providers give override-per-subtree for free, which is what makes widget tests cheap: pump the widget with a fake repository injected above it (`testing.md`).
- Do not mix both for the same dependency. Pick the one the repo uses and keep the other out of that layer.
- Async initialization (opening a database, reading secure storage) belongs in a single `bootstrap()` awaited before `runApp`, or behind a provider that exposes a loading state — not in `main()` with a fire-and-forget call that later races the first screen.

## Immutability and Equality

- State objects compared by identity re-render on every emit; state objects with value equality skip no-op updates. Implement `==`/`hashCode`, or generate them (`codegen: allowed`), or use records for small value bundles (`dart.md`).
- `copyWith` on a class with nullable fields cannot express "set this to null" — the standard workaround is a sentinel or a wrapper type. Generated `copyWith` from `freezed` handles it; a hand-written one usually does not, and that silently ignores clears.
- Mutating a list or map held inside an immutable state object defeats the whole mechanism: the reference is unchanged, so `==` is true, so nothing rebuilds.
