# Testing — Unit, Widget, Golden, Integration

Three harnesses with different costs. Push each test to the cheapest one that can catch its failure.

| Kind | Runs on | Catches | Cost |
|---|---|---|---|
| Unit (`test`) | The Dart VM, no framework | Logic, parsing, mapping, view-model behavior | Milliseconds |
| Widget (`flutter test`) | A headless test binding | Tree structure, interaction, state, layout errors | Tens of milliseconds |
| Golden (`matchesGoldenFile`) | The same binding, pixel comparison | Visual regressions | Fragile across platforms |
| Integration (`integration_test`) | A real device or emulator | Wiring, plugins, permissions, real navigation | Seconds to minutes each |

The pyramid holds in Flutter with one adjustment: widget tests are cheap enough that they, not unit tests, are the workhorse for UI code.

## Widget Test Mechanics

```dart
testWidgets('submits when the form is valid', (tester) async {
  await tester.pumpWidget(MaterialApp(home: LoginScreen(auth: FakeAuth())));
  await tester.enterText(find.byKey(const Key('email')), 'a@b.c');
  await tester.tap(find.byType(ElevatedButton));
  await tester.pump();                                  // one frame
  expect(find.text('Welcome'), findsOneWidget);
});
```

- `pump()` advances one frame. `pump(Duration)` advances virtual time by that much. `pumpAndSettle()` pumps until no frames are scheduled — and **hangs on any repeating animation** (`animations.md`), returning only when its timeout expires, which defaults to 10 minutes. A test that "takes forever" is almost always this.
- The default test surface is 800 × 600 logical pixels. A layout that assumes a phone width overflows in tests and nowhere else; set `tester.view.physicalSize` and `devicePixelRatio` (and reset them with `addTearDown(tester.view.reset)`) when the size matters.
- Overflow errors FAIL widget tests. That is a feature: a test that pumps every screen at a couple of sizes catches the whole `RenderFlex overflowed` category (`layout.md`).
- `pumpWidget` with a bare widget throws `No Material widget found` or `No Directionality widget found` — wrap in `MaterialApp` (or `Directionality` for a pure text widget).
- Async work must be pumped: after an `await`-based action, `pump()` once for the state change, or use `tester.runAsync` when the code needs real async I/O (which most test doubles should make unnecessary).
- Finders: prefer `find.byKey` for the things a test drives and `find.text` for what the user sees. `find.byType` couples the test to the widget hierarchy and breaks on refactors.
- `find.byIcon`, `find.bySemanticsLabel`, and `find.descendant` cover the rest; `warnIfMissed: false` on `tap` hides real failures — do not reach for it.

## Fakes over Mocks

- A fake repository (a real class returning canned data) reads better and breaks less than a mock with stubbed methods. Reserve mocks for verifying that a call HAPPENED.
- Inject the dependency; do not reach for a global. Scoped providers and constructor injection both make this one line in the test (`architecture.md`); a service locator needs a per-test registration and a teardown.
- Fake time with `fakeAsync` (or `tester.pump(Duration)`) rather than sleeping. A test containing a real delay is a test that will flake in CI.
- `HttpOverrides` in `setUpAll` stops any forgotten real request; a test suite that silently hits the network is the classic source of CI-only failures.
- Plugins are unavailable in widget tests: any code path touching a `MethodChannel` needs a mock handler (`TestDefaultBinaryMessengerBinding...setMockMethodCallHandler`) or an injected fake at the boundary (`platform.md`).

## What to Test

- Every bug fixed gets a test that fails without the fix. This is the only rule that reliably grows a useful suite.
- State transitions in notifiers and blocs: input event → expected state sequence, including the failure branch.
- Parsing and mapping against a real captured payload, including a null-heavy and a malformed one (`data.md`).
- Screens: renders loading, renders data, renders error, and the primary interaction works.
- Disposal: pump the widget, pump an empty tree, and assert no exception — that catches uncancelled tickers and subscriptions (SKILL.md rule 3).
- Accessibility guidelines as assertions: `meetsGuideline(textContrastGuideline)`, `androidTapTargetGuideline`, `labeledTapTargetGuideline` (`accessibility.md`).
- Not worth testing: that a `Text` renders the string you passed it, or that Flutter's own widgets work.

## Golden Tests

- `expect(find.byType(Card), matchesGoldenFile('goldens/card.png'))`, refreshed with `flutter test --update-goldens`. Treat `--update-goldens` as destructive: review the diff, never regenerate to make a red suite green (`destructive_confirm`).
- Goldens are platform-specific. Font rasterization differs between macOS, Linux, and Windows, so a golden generated on a laptop fails on a Linux runner. Generate and verify them on ONE pinned platform — in practice, the CI image.
- An SDK upgrade can shift antialiasing and invalidate the whole set. Budget for that when adopting them.
- Scope them to design-system components, where the pixels ARE the contract. Full-screen goldens fail on every copy change and teach the team to regenerate without looking (SKILL.md, Where Experts Disagree).
- Load real fonts in the test setup, or every golden renders in the fallback test font and stops resembling the app.

## Integration Tests

- `integration_test` drives a real build on a device: this is where plugins, permissions, deep links, and platform channels actually run.
- Keep the suite to the handful of flows whose breakage would be a business incident — sign-in, checkout, first-run. Each test costs device minutes on every run.
- Flakiness comes from waiting on wall-clock time. Wait for a condition (poll a finder until it matches, with a timeout), never `Future.delayed`.
- Permission dialogs are native UI and are not driven by the Flutter finders; grant them at install time on the test device, or use a driver that can reach native views.
- Screenshots for store listings can be produced from this harness, which pays for part of its cost.

## In CI

- `flutter test --coverage` produces `lcov.info`. Coverage is a conversation starter, not a gate on its own — a suite at 90% that never asserts behavior is worse than one at 50% that does.
- Pin the SDK version in CI to the one the team develops on: analyzer rules, goldens, and generated code all move between versions (`dependencies.md`).
- `flutter analyze` runs before tests; a type error found by the analyzer is cheaper than the same error found by a failed test.
- Run `dart run build_runner build --delete-conflicting-outputs` in CI when `codegen: allowed`, and commit or verify — a stale generated file that compiles locally and not in CI is the classic Monday-morning failure.
