# Widgets — Composition, Context, and Build Discipline

Three trees, and most confusion comes from conflating them: the **Widget** tree is an immutable description rebuilt constantly; the **Element** tree is the persistent instance graph that decides reuse and holds `State`; the **RenderObject** tree does layout, painting, and hit testing. `BuildContext` IS the Element — that is why context has a position in the tree and why "the wrong context" is a real category of bug.

## BuildContext Rules

- A context can only look UP. `Theme.of(context)`, `MediaQuery.sizeOf(context)`, and `Provider.of` walk ancestors from that element. They never see siblings or children.
- **The classic failure**: calling `Scaffold.of(context)` in the widget that builds the `Scaffold`. That context sits ABOVE the Scaffold, so the lookup fails. Fixes, in order of preference: (1) use `ScaffoldMessenger.of(context)` for snackbars, which is app-level and works from anywhere below `MaterialApp`; (2) extract the calling part into its own widget; (3) wrap in a `Builder` to get a context one level down.
- Every `X.of(context)` call registers a dependency: the widget rebuilds whenever that inherited widget changes. That is why `MediaQuery.of(context)` for a width rebuilds on keyboard open — the aspect-specific accessors (`MediaQuery.sizeOf`, `.paddingOf`, `.viewInsetsOf`, `flutter >=3.10`) subscribe to one field instead.
- A context captured in a closure and used after an `await` may be dead: "Looking up a deactivated widget's ancestor". Guard with `mounted`, or capture the object you actually need before the await (`async.md`).
- In `dispose`, context lookups are invalid. Capture `ScaffoldMessenger.of(context)` / `Navigator.of(context)` into a field in `didChangeDependencies` if you must use them during teardown.

## Build Method Discipline

`build` must be pure, fast, and free of side effects — it can run on any frame, several times per second, and Flutter is free to call it more often than you expect.

Never inside `build`:

- Creating controllers, `FocusNode`s, streams, or futures (SKILL.md Traps) — a new object per rebuild, and the old one leaks.
- Network calls, database reads, file I/O.
- `Navigator.push`, `showDialog`, `showSnackBar`, notifier writes (SKILL.md rule 8).
- Expensive computation: sorting, filtering a large list, formatting hundreds of dates. Compute once in `initState`/`didUpdateWidget`, or memoize by input.
- Random values or `DateTime.now()` when the result is rendered — the widget changes every frame, and diffs become meaningless.

Cheap and correct inside `build`: reading fields, watching providers, and constructing widgets. Constructing widgets is not expensive — Flutter is designed around exactly that.

## Extract a Widget, Not a Method

A `Widget _buildHeader()` method and a `const _Header()` widget look equivalent and are not:

- The method's output is inlined into the parent's build: it rebuilds whenever the parent rebuilds, always, and it cannot be `const`.
- The extracted widget class gets its own Element. If its inputs are unchanged and it is `const`, the parent's rebuild stops there (SKILL.md rule 5).
- The extracted widget can be a `StatefulWidget` later, can be tested in isolation, and shows up by name in DevTools and in performance overlays.

Default: extract classes. Build methods are acceptable for tiny fragments used once, in a widget that rarely rebuilds.

## Composition Toolkit

| Need | Widget | Note |
|---|---|---|
| Give descendants a value | `InheritedWidget`, or a provider | Descendants opt in with `of(context)` and rebuild on change |
| Get a context below the current one | `Builder` | The whole purpose of `Builder`; costs one element |
| Defer building until the size is known | `LayoutBuilder` | Runs during layout: cannot depend on anything that changes size in response |
| Defer building until after the first frame | `addPostFrameCallback` | For measuring, autofocus, showing a dialog on entry |
| Wrap a child without adding a level of nesting in the code | An extension or a helper widget | Deep nesting is a readability problem, not a performance one |
| Render nothing | `SizedBox.shrink()` | `Container()` is not free; returning `null` is not allowed |
| Conditionally include a widget in a list | `if (cond) Widget()` inside a collection literal | Cleaner than a ternary with `SizedBox.shrink()`, and it truly omits the element |
| Repeat a widget over data | `...items.map(...)` spread, or `.builder` for long lists | Spreading builds all of them (`layout.md`) |

## Theming

- Read from the theme, never hardcode: `Theme.of(context).colorScheme.primary`, `textTheme.bodyMedium`. Hardcoded colors are the reason dark mode ships broken.
- App-specific tokens (brand spacing, custom semantic colors) belong in a `ThemeExtension<T>` so they arrive through the same `Theme.of(context)` path and animate with theme changes.
- `Theme.of(context)` in a widget that also DEFINES a nested `Theme` reads the outer one — same ancestor rule as `Scaffold.of`.
- Material 3 is the default for `ThemeData` on current SDKs; a design that looks suddenly different after an SDK upgrade is usually this, not a regression in your code (`dependencies.md`).
- Test both brightnesses. A widget test can pump with `ThemeData.dark()` in a loop over both (`testing.md`).

## GlobalKey: When It Is Actually Right

| Use | Verdict |
|---|---|
| `GlobalKey<FormState>` to validate a form | Right — no other access path exists (`forms.md`) |
| A `navigatorKey` for navigation without context | Defensible for a few entry points (`navigation.md`, Where Experts Disagree in SKILL.md) |
| Measuring a rendered widget (`key.currentContext.findRenderObject()`) | Acceptable after the first frame; prefer `LayoutBuilder` when the parent's constraints answer the question |
| Moving a subtree to a different parent while preserving state | The intended advanced use; expensive, and it forces a full re-layout |
| Reaching a child's `State` to call a method on it | Wrong — pass a callback down or share a notifier (`architecture.md`) |
| Getting around a `Scaffold.of` failure | Wrong — the fix is a `Builder` or an extracted widget |

Two live widgets holding the same `GlobalKey` throw "Multiple widgets used the same GlobalKey" — most often caused by declaring the key as a field of a widget that gets rebuilt, or reusing one key across list items.

## Gesture and Hit Testing

- A `GestureDetector` over a transparent area receives nothing by default: set `behavior: HitTestBehavior.opaque` to claim the empty space, or `translucent` to claim it while letting widgets below also respond.
- Painting outside the parent's bounds does not extend hit testing: a button half outside a `Stack` is only tappable in the visible-and-inside half (`layout.md`).
- `IgnorePointer` makes a subtree invisible to hit testing; `AbsorbPointer` swallows the events instead. Debugging "my button does nothing" starts by grepping for both.
- Nested gesture detectors: the innermost wins the arena for taps. For competing drags, `RawGestureDetector` with custom recognizers is the escape hatch — rare, and correct when it is needed.
- `InkWell` needs a `Material` ancestor to paint its splash; on a colored `Container` the ripple is invisible because it paints under the container's own background. Use `Material` + `InkWell`, or `Ink(decoration:)`.
