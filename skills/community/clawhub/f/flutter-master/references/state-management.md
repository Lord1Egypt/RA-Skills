# State Management

## Choosing an approach

There is no single "correct" choice — but there is a correct process: pick one, and use it consistently across the app. The most common source of maintainability rot in real Flutter codebases isn't which library was chosen, it's that two or three got mixed together over time.

Rough guidance for greenfield choices:

| Approach | Good fit when | Watch out for |
|---|---|---|
| **Riverpod** | New projects, teams that want compile-time-safe DI + state in one system, apps needing easy testability | Learning curve around providers/families/AsyncValue; overusing `ref.watch` at too broad a scope causes extra rebuilds |
| **BLoC/Cubit** | Teams that want a strict, explicit, highly testable event→state contract; larger teams wanting enforced consistency | Boilerplate-heavy for simple screens; Cubit is the lighter-weight sibling of full BLoC and is fine for most cases — don't force full event-based BLoC everywhere by default |
| **Provider** | Small-to-medium apps, teams wanting something simpler than Riverpod/BLoC, or legacy codebases already using it | Officially in "maintenance" territory relative to Riverpod (same author recommends Riverpod for new code) — fine to keep in an existing app, worth mentioning as a consideration for new projects |
| **GetX** | Rapid prototyping, very small teams wanting minimal boilerplate | Tends to encourage tight coupling and "magic" global state access; testability and maintainability suffer at scale — flag this tradeoff honestly if a project is growing past prototype stage |
| **setState only** | Genuinely local, ephemeral UI state (a text field's focus, an expand/collapse toggle) | Using it for anything shared across widgets/screens is the #1 sign a project needs to graduate to a real state solution |

When auditing an existing project, don't push a rewrite to your preferred library just because it's not what you'd have chosen — evaluate whether the *existing* choice is applied consistently and correctly, and only recommend a switch if there's a concrete, current pain point it's causing.

## Common mistakes across all approaches

**Business logic in the widget tree.** If a `build()` method or an `onPressed` callback contains actual decision-making (validation rules, calculations, API-response transformation), it belongs in a notifier/bloc/controller instead. The test: could this logic be unit-tested without pumping a widget? If not, it's in the wrong place.

**Rebuilding more than necessary.** Watching an entire object when only one field matters causes cascading rebuilds:
```dart
// Rebuilds on ANY change to `user`, even unrelated fields
final user = context.watch<User>();

// Better: select only what this widget needs
final name = context.select<User, String>((u) => u.name);
```
Riverpod equivalent: prefer narrow, derived providers over watching a large state object wholesale when a widget only needs a slice of it.

**Not disposing.** Controllers, `StreamSubscription`s, `AnimationController`s, and BLoC/Cubit instances created manually (not via a DI framework that handles disposal) must be disposed in `dispose()`. This is the single most common Flutter memory leak.

**Calling `setState` after `dispose`.** Async work that completes after a widget is disposed and then calls `setState` throws. Guard with a `mounted` check:
```dart
final result = await someAsyncCall();
if (!mounted) return;
setState(() => _data = result);
```

**Overusing global/singleton state for things that aren't actually global.** Not every piece of state needs to live at the app root. Scope state to where it's actually used — it's easier to reason about and test.

**Mixing paradigms.** Finding `Provider.of` next to `BlocBuilder` next to raw `setState` for logically similar things in the same app is a red flag worth calling out explicitly in an audit, even if each individual usage is "correct" in isolation.
