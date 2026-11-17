# Debugging — Symptom to Cause in Minutes

Work symptom-first. Each chain below is ordered by probability, and every step is a check, not a guess.

## The Universal First Three

1. **Read the FIRST exception, not the last.** One layout failure cascades into a screenful of `RenderBox was not laid out` and `Another exception was thrown`. Scroll to the top of the burst; everything after it is noise.
2. **Read the block above the stack trace.** Flutter prints `The relevant error-causing widget was:` with a file and line, and for layout failures it prints the constraints that arrived. That is usually the whole answer.
3. **Reproduce it in a widget test.** A failing `testWidgets` that pumps the offending widget turns an intermittent app-level bug into a one-second loop, and leaves a regression test behind (`testing.md`).

## Exception Decoder

| Exception | Real cause | First move |
|---|---|---|
| `setState() called after dispose()` | An await outlived the widget | `if (!mounted) return;` after every await (SKILL.md rule 2) |
| `setState() or markNeedsBuild() called during build` | A notifier fired, or navigation/snackbar/dialog ran, inside `build` | Move it to a callback or `addPostFrameCallback` (SKILL.md rule 8) |
| `Looking up a deactivated widget's ancestor` | A `BuildContext` captured before an await, used after | Capture the `NavigatorState`/`ScaffoldMessengerState` BEFORE awaiting (`async.md`) |
| `A RenderFlex overflowed by N pixels` | A child wants more than the axis allows | `Expanded`/`Flexible`, or make the axis scrollable (`layout.md`) |
| `Vertical viewport was given unbounded height` | A scrollable inside a `Column` or another scrollable | `Expanded`, a fixed height, or slivers (`layout.md`) |
| `Incorrect use of ParentDataWidget` | `Expanded`/`Positioned` is not a direct child of its flex/stack | Remove the widget in between (`layout.md`) |
| `Multiple widgets used the same GlobalKey` | One key on two live widgets, or a key recreated on rebuild | Make the key a field of the `State`, or stop using a `GlobalKey` (`widgets.md`) |
| `Bad state: Stream has already been listened to` | A single-subscription stream re-listened after a rebuild | Cache the stream in a field, or make it broadcast (`async.md`) |
| `A Ticker was started and is still running` | An `AnimationController` was never disposed | Dispose it (SKILL.md rule 3) |
| `MissingPluginException` | The plugin was added without a full restart, or this platform has no implementation | Stop and re-run; `pod install` for iOS (`platform.md`) |
| `PlatformException(code, message)` | Native code answered with a failure | Branch on `code`; read the native log for the real reason (`platform.md`) |
| `type 'Null' is not a subtype of type 'String'` | JSON parsed with an unchecked cast | Parse defensively at the boundary (`data.md`) |
| `Scaffold.of() called with a context that does not contain a Scaffold` | The context is above the Scaffold it created | `Builder`, an extracted widget, or `ScaffoldMessenger.of` (`widgets.md`) |
| `Unable to load asset` | Undeclared in `pubspec.yaml`, or a path typo | Declare it; directory entries need a trailing slash (`release.md`) |
| Anything else | The message names a subsystem | Search the exact message text with the widget name from the error block |

## Nothing Happens When I Tap

1. Is the widget hit-testable? Painting outside the parent's bounds is visible but not tappable (`layout.md`).
2. Is something swallowing the gesture? Grep for `IgnorePointer`, `AbsorbPointer`, and an overlaying transparent `Container` in a `Stack`.
3. Transparent area under a `GestureDetector`: needs `behavior: HitTestBehavior.opaque` (`widgets.md`).
4. Is the callback null? A `disabled` button (`onPressed: null`) looks nearly identical to an enabled one in many themes.
5. Is the handler running but the UI not changing? Add a print, then check for a mutation without `setState` (`state.md`) — the silent no-op.
6. Still nothing: `flutter run` then press `p` for the debug paint overlay, which shows the real box you are aiming at.

## Hot Reload Did Nothing

Hot reload re-runs `build` with the new code and keeps state. It does NOT re-run code that already ran.

- Changes inside `main()`, `initState`, a top-level or static field initializer, or a `const` value need a hot RESTART (`R`).
- Enum changes, generic type parameter changes, and changes to a class's supertype require a restart, sometimes a full rebuild.
- Adding or removing a PLUGIN requires a full stop and re-run: the native side registers at startup (`platform.md`).
- Changing native code (Kotlin/Swift/Gradle/Podfile), assets declared in `pubspec.yaml`, or the app icon all require a rebuild.
- If a restart also does nothing, the artifact is stale: `flutter clean` earns its keep exactly here and nowhere else (`commands.md`).

## The App Is Slow or Janky

1. Rebuild in profile mode on a physical device — a debug-mode observation ranks nothing (SKILL.md rule 7).
2. Which thread missed the frame? UI vs raster changes the entire diagnosis (`performance.md`).
3. Rebuild storm: DevTools' rebuild counter names the widget rebuilding thousands of times. Climb the Rebuild Scope Ladder (SKILL.md).
4. Frozen rather than janky (no frames at all): a synchronous block on the UI isolate — a big `jsonDecode`, a file read, a sort. Move it to an isolate (`async.md`).
5. Jank only while scrolling images: decoded image size (`performance.md`).
6. Jank only the first time an effect plays: shader compilation on the pre-Impeller renderer — confirm which renderer started before treating it as a code problem (`performance.md`).

## Memory Keeps Growing

1. Push and pop the suspect screen ten times, forcing a GC each time in DevTools. A floor that climbs is a leak.
2. Usual causes, in order: an uncancelled `StreamSubscription`, a listener added without `removeListener`, a `Timer.periodic`, an `AnimationController` never disposed, a static reference to a widget's state (SKILL.md rule 3).
3. Rule out intentional retention first: `AutomaticKeepAliveClientMixin`, `IndexedStack`, and a large `cacheExtent` all hold memory by design (`state.md`).
4. Image memory dominates most apps: check the image cache before hunting objects (`performance.md`).

## Works in Debug, Fails in Release

Check in this order; each is a one-minute test.

| Difference | Check |
|---|---|
| Icons blank, assets missing | Tree-shaking and `pubspec.yaml` declarations (`release.md`) |
| Logic inside an `assert` | `assert`s are stripped in release |
| Reflection or `Type.toString()` | Obfuscation renamed it (`release.md`) |
| Timing-dependent code | AOT is faster; races that never lost in debug now lose |
| A native library or permission | Test the store-track artifact on a second physical device |
| Unreadable crash stack | Symbolize with the symbols from THAT build (`release.md`) |

## Works on My Machine, Fails in CI

| Difference | Check |
|---|---|
| SDK version | Pin the Flutter version in CI to the team's (`dependencies.md`) |
| Golden mismatch | Goldens are platform-specific; generate on the CI image (`testing.md`) |
| Generated code | `build_runner` not run, or a stale committed output (`dependencies.md`) |
| Test surface size | CI runs the default 800 × 600; a size-dependent test needs an explicit view size (`testing.md`) |
| Test hangs then times out | `pumpAndSettle` against a repeating animation (`animations.md`) |
| A real network call | A test hitting the network flakes on a runner; block it in `setUpAll` (`testing.md`) |

## Build Won't Compile

- Dart-level errors: `flutter analyze` first — it names the file and line the build tool buries under a hundred lines of Gradle output.
- Version solving failed: `dependencies.md`.
- Gradle failures mentioning a plugin: usually a Kotlin, AGP, or compile-SDK mismatch introduced by a plugin upgrade. Read which module Gradle names.
- CocoaPods failures: `pod repo update`, then `cd ios && pod install`. After changing plugins, delete `Podfile.lock` only when you intend to re-resolve everything (`destructive_confirm`).
- "It compiled yesterday": check what changed in `pubspec.lock` before touching anything else — the SDK, a plugin, or a transitive constraint moved.

## Inspection Toolkit

- DevTools (`flutter run` prints its URL): widget inspector, rebuild counts, performance timeline, memory, network, and the semantics tree.
- `debugDumpApp()`, `debugDumpRenderTree()`, `debugDumpLayerTree()`, `debugDumpSemanticsTree()` — the four trees, printed on demand.
- `debugPaintSizeEnabled = true` draws every box and padding; the `p` key in `flutter run` toggles it live.
- `debugRepaintRainbowEnabled = true` recolors layers on each repaint — the fastest way to see what is repainting per frame.
- `debugPrintBeginFrameBanner` / `debugPrintRebuildDirtyWidgets` for frame-by-frame tracing when the inspector is not enough.
- `flutter logs` (or `adb logcat` / Console.app) for anything the native side reports — a store build's Dart console does not exist.

## When You Are Truly Stuck

Reduce to the smallest widget that reproduces it, in a fresh `main()` with no providers, no theme, and no data layer. Either it reproduces — and you now have the actual cause in twenty lines — or it does not, and the difference between that file and your app is the bug.
