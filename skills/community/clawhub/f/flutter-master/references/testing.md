# Testing

## The pyramid, Flutter-flavored

- **Unit tests** — business logic, notifiers/blocs/controllers, repositories (with mocked data sources), pure functions. Should be the bulk of the suite: fast, no widget tree needed.
- **Widget tests** — a single widget/screen rendered via `testWidgets` + `WidgetTester`, verifying it renders correctly and responds to interaction, with dependencies mocked/faked. This is Flutter's sweet spot — fast (no real device/emulator needed) but tests real rendering and interaction.
- **Integration tests** (`integration_test` package) — full app or large flows on a real device/emulator. Slower and fewer in number; reserve for critical user journeys (login, checkout, core flow) rather than trying to cover everything this way.
- **Golden tests** — pixel-level snapshot comparison for widgets where visual regression matters (design-system components, brand-critical screens). Useful but maintenance-heavy (goldens need regenerating on intentional visual changes) — recommend for a design system/component library more than for every screen.

## What's worth testing

Prioritize by risk × frequency of change:
1. Business logic with actual branching (validation, pricing/calculation, state transitions) — high value, cheap to test since it doesn't need a widget tree.
2. Repositories/data layer — especially error handling paths (what happens when the API call fails? Is that tested, or only the happy path?).
3. Critical user flows end-to-end (integration tests) — auth, payment, core value-prop action.
4. Widgets with non-trivial conditional rendering (loading/error/empty/data states) — a widget test per state is cheap and catches real regressions.

Don't chase 100% coverage as a goal in itself — a trivial widget test on a static `Text` widget adds maintenance cost for near-zero regression protection. Coverage number is a signal, not a target.

## Mocking

`mocktail` (no code gen, works with null safety cleanly) or `mockito` (code-gen based, `build_runner`) are the standard choices. Prefer defining a small abstract interface for anything you'll want to mock (repositories, API clients) rather than mocking concrete classes directly — cleaner test doubles and enforces the dependency-inversion boundary from architecture.md.

## Example: widget test structure
```dart
testWidgets('shows error message when load fails', (tester) async {
  await tester.pumpWidget(
    ProviderScope(
      overrides: [repositoryProvider.overrideWithValue(FakeFailingRepository())],
      child: const MaterialApp(home: ProfileScreen()),
    ),
  );
  await tester.pumpAndSettle();
  expect(find.text('Something went wrong'), findsOneWidget);
});
```

## CI gates

At minimum, a Flutter project's CI should run on every PR:
```yaml
- flutter analyze
- dart format --set-exit-if-changed --output=none .
- flutter test --coverage
```
Flag the absence of any CI quality gate as a high-priority audit finding — it's cheap to set up (GitHub Actions has an official `flutter-action`) and prevents regressions from ever reaching main in the first place.

## Common testing mistakes to flag

- Tests that mock so much they only verify the mock was called, not real behavior.
- No tests for error/failure paths — only happy-path coverage.
- Flaky integration tests tolerated/ignored rather than fixed (usually a timing/`pumpAndSettle` issue).
- Business logic untested because it's embedded in a widget instead of extracted (see state-management.md) — this is often the *reason* coverage is low, not just a testing gap on its own.
