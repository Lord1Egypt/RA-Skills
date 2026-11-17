# Code Style & Effective Dart

## Linting

Every project should have `analysis_options.yaml` with a strict lint set, not just the defaults. Recommend:
```yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    prefer_const_constructors: true
    prefer_const_literals_to_create_immutables: true
    avoid_print: true
    always_declare_return_types: true
    prefer_final_locals: true
    unawaited_futures: true
    cancel_subscriptions: true
```
`flutter_lints` is the official baseline; `avoid_print`, `unawaited_futures`, and `cancel_subscriptions` in particular catch real bugs, not just style nits — prioritize flagging their absence.

## Naming

- `UpperCamelCase` for classes, enums, extensions, typedefs.
- `lowerCamelCase` for variables, functions, parameters.
- `lowercase_with_underscores` for file names and package names.
- Boolean names should read as a question/state: `isLoading`, `hasError`, `canSubmit` — not `loading`, `error`, `submit`.
- Widget class names should describe what they render, not implementation detail: `ProfileAvatar`, not `ProfileWidget1`.

## Immutability

Prefer `final` over non-final wherever the value doesn't need to change, and prefer immutable data classes for models. Use `const` constructors everywhere possible — this isn't just style, it directly reduces rebuild cost (see performance.md). A widget class with all-final fields and a `const` constructor is a strong default:
```dart
class UserCard extends StatelessWidget {
  const UserCard({super.key, required this.name, required this.avatarUrl});

  final String name;
  final String avatarUrl;

  @override
  Widget build(BuildContext context) => ...;
}
```

## Null safety

- Avoid `!` unless nullness is genuinely impossible at that point and you can explain why. If you find yourself unsure, that's a sign to handle the null case instead of suppressing it.
- Prefer `?.` and `??` for concise null handling over verbose `if (x != null)` where it doesn't hurt readability.
- Late variables (`late final foo`) are for values guaranteed to be set before use (e.g. in `initState`) — don't use `late` as a lazy way to dodge nullability when the value genuinely might not be set.

## Formatting

Run `dart format .` — don't hand-format. If the project doesn't already enforce this in CI, flag it as an easy win.

## Records, pattern matching, sealed classes (modern Dart)

Current Dart (3.x) has records, patterns, and sealed classes — use them where they reduce boilerplate versus older patterns:
```dart
// Sealed class + switch pattern instead of a manual "type" enum + if-chain
sealed class LoadState<T> {}
class Loading<T> extends LoadState<T> {}
class Loaded<T> extends LoadState<T> { Loaded(this.data); final T data; }
class Failed<T> extends LoadState<T> { Failed(this.error); final Object error; }

String describe(LoadState<int> state) => switch (state) {
  Loading() => 'loading...',
  Loaded(:final data) => 'got $data',
  Failed(:final error) => 'error: $error',
};
```
If a codebase is on an older Dart SDK, don't recommend these — check the SDK constraint in `pubspec.yaml` first.

## Comments and documentation

Doc comments (`///`) on public APIs (exported classes, methods used across features) are worth the effort; inline `//` comments explaining *why*, not *what*, for anything non-obvious. Don't recommend comments that just restate the code.

## Common smells to flag

- `print()` statements left in — should be a proper logger (or removed) so production builds don't leak debug output.
- Deeply nested ternaries or `if` chains — extract to a named function or use pattern matching.
- Magic numbers/strings repeated across files — extract to named constants.
- Catching exceptions and doing nothing (`catch (e) {}`) — silent failure is almost always worse than a visible one.
