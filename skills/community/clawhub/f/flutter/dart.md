# Dart — The Language Under Flutter

Only what changes Flutter code. Sound null safety and the Dart 3 features below are available on any SDK a current Flutter release ships with (`dart >=3.0`).

## Null Safety in Practice

- `T?` is a different type from `T`; the compiler will not let you use one as the other. That is the point, and fighting it with `!` reintroduces exactly the crashes the system exists to prevent.
- `!` asserts non-null and throws if wrong. Legitimate when you can name the invariant (`_formKey.currentState!` inside a callback the form owns); a smell when it appears in a chain of three.
- Promotion works on LOCAL variables and final fields, not on non-final instance fields or getters — because another isolate-free path could change them between the check and the use. Copy to a local first: `final v = widget.value; if (v != null) { use(v); }`.
- `late` defers initialization and moves the error to runtime: `LateInitializationError` if read first. Right for a field initialized in `initState` that cannot be `final`; wrong as a way to silence the compiler.
- `late final x = expensive();` is lazy: computed on first read, once. Useful for a controller you may never need — and a trap if the computation depends on something not yet available.
- `??`, `??=`, and `?.` cover most of what `!` gets used for. `a?.b ?? c` reads better than `a != null ? a.b : c` and does not risk the assertion.

## Records and Patterns

- Records are lightweight unnamed tuples with value equality: `(int, String)` positional, `({int id, String name})` named. Perfect for returning two values without a class, and for a `Map` key that must compare by content.
- Value equality is the reason they matter in Flutter: a record in a state object compares by content, so a rebuild is skipped when nothing changed (`architecture.md`).
- Destructuring: `final (id, name) = fetchPair();` and `if (json case {'id': int id, 'name': String name})` — the pattern form validates the shape AND binds typed variables in one step, which is a genuinely better JSON guard than a chain of casts (`data.md`).
- Switch expressions return a value and are exhaustive over sealed hierarchies: `final label = switch (status) { Loading() => '…', Error(:final msg) => msg, Data(:final n) => '$n' };`. The compiler flags a missing case — that is what makes sealed state classes worth the ceremony.
- `sealed class` permits subtypes only in the same library, which is what enables that exhaustiveness. `final class` forbids extension; `base` forbids implementation. Use them to make illegal states unrepresentable in view state.

## Equality and Immutability

- The default `==` is identity. Two structurally identical objects are unequal, so every rebuild re-renders and every state emit is treated as a change (`architecture.md`).
- Override `==` and `hashCode` together, always, and only over the fields that define identity. An overridden `==` without `hashCode` breaks `Set` and `Map` in ways that surface far from the mistake.
- Prefer records for small value bundles, generated equality for models, and hand-written only for a handful of classes.
- `const` constructors give compile-time canonicalization: two identical `const` instances ARE the same object, which is what makes `const` widgets skip rebuilds (SKILL.md rule 5). A class whose fields are all final can and should have one.
- `List`, `Map`, and `Set` literals are mutable by default even inside a const-looking class. `const []` is deeply immutable; `List.unmodifiable` wraps at runtime and throws on write.

## Collections

- Collection-if and collection-for build widget lists cleanly: `[ const Header(), if (showBanner) const Banner(), for (final i in items) ItemTile(i) ]` — no `.where().map().toList()` chains inside `build` (`widgets.md`).
- Spread `...` and null-aware spread `...?` merge lists; `...?maybeList` is the clean way to include an optional group.
- `map`, `where`, and `expand` are lazy: nothing runs until iterated. A `map` whose result is iterated twice runs twice — add `.toList()` when the result is reused.
- `firstWhere` throws when nothing matches; pass `orElse: () => null` with a nullable element type, or use `firstWhereOrNull` from `package:collection`.
- Sorting mutates in place and returns void: `final sorted = [...items]..sort(compare);` is the non-destructive form, and it is what a state object needs (`architecture.md`).

## Async Language Semantics

- `async` functions run synchronously up to the first `await`, then return a `Future`. Code after an `await` runs in a later microtask — that is the async gap `mounted` protects (`async.md`).
- `Future.wait([a, b])` runs concurrently and fails as a unit on the first error; `eagerError: false` still waits for all. Sequential awaits run serially — a page loading three independent resources one after another is a common, silent slowness.
- `async*` produces a `Stream`, `sync*` an `Iterable`; `yield*` delegates to another. A `async*` generator pauses when its listener pauses, which is the backpressure most manual controllers forget.
- Unawaited futures swallow their errors into an unhandled-exception log. Mark deliberate ones with `unawaited(...)` and attach error handling.

## Classes and Constructors

- Super parameters remove constructor boilerplate: `const MyWidget({super.key, required this.title});`.
- Named constructors and factory constructors: a factory can return a cached instance or a subtype, which is the standard shape for `fromJson` with variants.
- Extension methods add behavior without inheritance and are resolved statically — an extension on `BuildContext` (`context.colors`, `context.textTheme`) is a common, readable convenience in Flutter code. Extensions do not apply to `dynamic`.
- Callable objects, operator overloads, and mixins are all available; `mixin` with an `on` clause is how framework mixins like `TickerProviderStateMixin` constrain themselves to `State`.
- `typedef` for function types keeps callback-heavy widget APIs readable: `typedef ItemSelected = void Function(Item item);`.

## Errors

- `Error` signals a programming bug (`StateError`, `ArgumentError`, `LateInitializationError`) and should not be caught in production paths. `Exception` signals an expected failure (network, parsing) and should be.
- `catch (e, st)` captures the stack trace; forwarding the trace is what keeps a crash report readable. `Error.throwWithStackTrace(e, st)` preserves the original origin across a boundary, where a bare rethrow of a stored error would not.
- `on SomeType catch (e)` filters by type; a bare `catch` also catches `Error`, which is how a real bug ends up reported as "network unavailable" (`data.md`).
- `finally` runs on both paths — the correct home for the `_busy = false` that re-enables a submit button (`forms.md`).
