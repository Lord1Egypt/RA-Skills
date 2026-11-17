---
name: Flutter
slug: flutter
version: 1.0.3
description: >-
  Builds, debugs, and ships Flutter apps: widgets, layout constraints, state management, navigation,
  performance, and store releases. Use when writing Dart widgets or screens; when a RenderFlex overflows,
  a viewport is given unbounded height, or a RenderBox was not laid out; when setState is called during
  build or after dispose, or BuildContext is used across an async gap; when the UI janks, scrolling
  stutters, or images exhaust memory; when hot reload stops applying changes; when Provider, Riverpod, or
  Bloc rebuild too much or too little; when routing with Navigator or go_router, deep links, or back-button
  handling; when the keyboard covers a form field or validation misfires; when a platform channel throws
  MissingPluginException; when localizing strings or mirroring a layout for right-to-left; when widget,
  golden, or integration tests hang or fail in CI; or when a build works in debug but the release APK,
  IPA, or web bundle breaks. Not for React Native or native-only Swift and Kotlin work.
homepage: https://clawic.com/skills/flutter
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🐦
    requires:
      bins:
      - flutter
    os:
    - linux
    - darwin
    - win32
    displayName: Flutter
    configPaths:
    - ~/Clawic/data/flutter/
---

User preferences live in `~/Clawic/data/flutter/config.yaml` (see Configuration); nothing else is stored on the user's machine. If you have data at an old location (`~/flutter/` or `~/clawic/flutter/`), move it to `~/Clawic/data/flutter/`.

## When To Use

- Writing or reviewing Flutter UI: widgets, layouts, screens, lists, forms, animations, theming, custom painting
- Decoding a framework exception: overflow, unbounded constraints, setState during build or after dispose, deactivated ancestor
- Structuring an app: state management choice, routing, repositories, dependency injection, folder layout
- Performance work: jank, dropped frames, slow scrolling, memory growth, oversized images, startup time
- Reaching more users: translations, plurals, right-to-left layout, text scaling, semantics, tablet and desktop windows
- Shipping: build modes, flavors, signing, obfuscation, size analysis, store artifacts, release-only failures
- Reaching native: platform channels, FFI, plugins, permissions, background execution, per-platform behavior
- Not for React Native (`react-native`), native-only Swift (`swift`) or Kotlin (`kotlin`) work, or cross-framework motion systems (`animate`) — this is Flutter and Dart

## Quick Reference

| Situation | Play |
|---|---|
| "A RenderFlex overflowed by N pixels" | A child asked for more than the parent allows — `Expanded`/`Flexible` for a flex child, or make the axis scrollable → `layout.md` |
| "Vertical viewport was given unbounded height" | A scrollable inside a `Column` or another scrollable — `Expanded`, a fixed height, or slivers; `shrinkWrap: true` is the slow escape → `layout.md` |
| "RenderBox was not laid out" | Almost always a knock-on: scroll UP to the FIRST exception in the console and fix that one → `debug.md` |
| "setState() or markNeedsBuild() called during build" | A notifier fired, or navigation/snackbar ran, inside `build` — move it to a callback or a post-frame callback → `debug.md` |
| "setState() called after dispose()" | An `await` outlived the widget — `if (!mounted) return;` after every await (rule 2) → `async.md` |
| "Looking up a deactivated widget's ancestor" | A captured `BuildContext` used after its widget left the tree — capture the `NavigatorState` or `ScaffoldMessengerState` BEFORE the await → `async.md` |
| "Incorrect use of ParentDataWidget" | `Expanded`/`Flexible`/`Positioned` is not a direct child of `Row`/`Column`/`Flex`/`Stack` → `layout.md` |
| List items keep the wrong state after reorder or delete | Missing or unstable keys — `ValueKey(item.id)`, never `UniqueKey()` in a builder (rule 4) → `state.md` |
| A widget rebuilds far more than it should | Climb the Rebuild Scope Ladder below, then confirm in DevTools' rebuild counter → `performance.md` |
| Scrolling stutters, frames dropped | Profile mode on a real device first, then image decode size, `saveLayer`, and per-item work → `performance.md` |
| Memory climbs while scrolling images | Decoded bytes = width × height × 4, independent of file size — set `cacheWidth`/`cacheHeight` → `performance.md` |
| Choosing or migrating a state management library | Match the repo (`state_management: auto`); greenfield defaults and migration cost → `architecture.md` |
| Route needs an argument, a result, or a deep link | Typed routes and result handling with Navigator or go_router → `navigation.md` |
| Keyboard covers the field, focus jumps, validation fires too early | Controller lifetime, `AutovalidateMode.onUserInteraction`, scroll-on-focus → `forms.md` |
| Parsing, caching, or persisting data | Isolate for large payloads, local DB as the source of truth for offline → `data.md` |
| An animation stutters, leaks, or never restarts | Controller lifetime, `child:` hoisting, implicit vs explicit choice → `animations.md` |
| `MissingPluginException` right after adding a plugin | Hot restart does not register plugins — full stop and re-run → `platform.md` |
| Right on the phone, broken on tablet, web, or desktop | Window size classes, `LayoutBuilder` vs `MediaQuery`, platform-adaptive widgets → `adaptive.md` |
| Text overflows once the user enlarges the system font | Text scaling is a layout input, not a cosmetic setting → `accessibility.md` |
| A chart, gauge, signature pad, or anything no widget can express | `CustomPaint`, and the `shouldRepaint` contract that keeps it cheap → `custom-painting.md` |
| Translated text overflows, dates look wrong, or the layout must mirror for Arabic | ARB workflow, ICU plurals, and the directional widgets → `localization.md` |
| A test hangs, or passes locally and fails in CI | `pumpAndSettle` against an endless animation; goldens are platform-specific → `testing.md` |
| Works in debug, broken in the release build | AOT, tree-shaken icons, stripped asserts, obfuscation, undeclared assets → `release.md` |
| `pub get` cannot resolve, or a plugin breaks after an upgrade | Version solving, overrides, transitive plugin constraints → `dependencies.md` |
| A Dart language question (records, patterns, `late`, `==`) | → `dart.md` |
| Anything else | Read the FIRST exception in full including "The relevant error-causing widget", reproduce it in a widget test, then open the file the message names → `debug.md` |

Depth on demand: `layout.md` constraints, flex, overflow, slivers · `state.md` lifecycle, keys, state preservation · `architecture.md` state management, DI, layering · `widgets.md` composition, context, build discipline · `async.md` futures, streams, isolates, cancellation · `navigation.md` Navigator, go_router, deep links · `forms.md` text input, focus, validation · `data.md` JSON, HTTP, persistence, offline · `performance.md` jank triage, rebuilds, images · `animations.md` implicit, explicit, transitions · `custom-painting.md` canvas, painters, custom render objects · `platform.md` channels, FFI, plugins, permissions · `adaptive.md` phone, tablet, web, desktop · `accessibility.md` semantics, text scaling, tap targets · `localization.md` translations, plurals, RTL, formats · `testing.md` widget, golden, integration · `release.md` modes, flavors, signing, size · `debug.md` symptom to cause · `dependencies.md` pub, versions, codegen · `dart.md` the language · `commands.md` CLI toolkit.

## Core Rules

1. **Constraints go down, sizes go up, the parent sets position.** Every layout exception decodes from this one sentence. A widget may only choose a size inside the constraints its parent passed; given unbounded constraints (a `Column`'s main axis, a scrollable's scroll axis) a child that wants "as much as possible" has nothing to resolve and throws. Worked example: `ListView` inside `Column` → wrap it in `Expanded`, which converts the unbounded height into the leftover bounded height; `SizedBox(height: 240)` also works; `shrinkWrap: true` compiles and then lays out every child on every scroll frame.
2. **`mounted` is the gate on every async gap.** After each `await`, before touching `setState`, `context`, or any controller: `final data = await repo.load(); if (!mounted) return; setState(() => _data = data);`. The `use_build_context_synchronously` lint catches the context case only — controllers, tickers, and `ScaffoldMessenger` calls need the same guard and nothing warns you.
3. **Every disposable you create gets a matching line in `dispose`, in reverse creation order.** Controllers (`TextEditingController`, `ScrollController`, `AnimationController`, `PageController`, `TabController`), `FocusNode`s, `StreamSubscription`s, `Timer`s, `ValueNotifier`s. The leak is invisible in debug and surfaces as a climbing memory graph plus callbacks firing on dead widgets. Cheap check: a widget test that pumps the widget, pumps an empty tree, and asserts no exception (`testing.md`).
4. **Keys decide identity; without a key, position does.** Flutter matches a new widget to an existing `Element` by `runtimeType` + `key` at the same position, so inserting, removing, or reordering stateful children without keys hands state to the wrong item. Use `ValueKey(item.id)`. Never `UniqueKey()` inside a builder: a fresh key every build destroys and recreates the subtree — including its scroll offset and running animations — on every frame.
5. **`const` is the rebuild firewall.** Identical `const` widget expressions are canonicalized to a single instance, so `Element.update` sees `identical(oldWidget, newWidget)` and skips that subtree entirely. This is why extracting a static subtree into a `const` widget beats trying to "scope" a `setState` that still sits above it. A widget cannot be `const` if anything inside it reads `context` or a runtime value — that, not style, is the real constraint.
6. **Frame budget = 1000 / refresh rate ms — 16.7 ms at 60 Hz, 8.3 ms at 120 Hz — shared by the UI thread (build, layout, paint) and the raster thread (GPU).** Any single synchronous unit of work that can exceed it (decoding a large JSON payload, image processing, crypto, sorting tens of thousands of items) belongs in an isolate (`async.md`). Wrapping it in a `Future` changes nothing: the work still runs on the same isolate and still blocks the frame.
7. **Only profile mode produces real numbers.** Debug builds run the JIT with assertions, service extensions, and widget-inspector instrumentation; frame timings there are noise. `flutter run --profile` on a physical device — simulators and emulators have GPU behavior the shipped app never sees.
8. **Side effects never run inside `build`.** Navigation, snackbars, dialogs, notifier writes, network calls: each marks something dirty while the tree is building, which is exactly the "setState() or markNeedsBuild() called during build" exception. Put them in an event callback, a listener (`ref.listen`, `BlocListener`, `addListener`), or `WidgetsBinding.instance.addPostFrameCallback` when no other hook exists.
9. **A feature is not done until its release artifact runs.** AOT compilation, icon tree-shaking, stripped `assert`s, obfuscation, and asset declarations change behavior only in release. Build and launch the `--release` artifact on a device before calling it finished (`release.md`).

## Layout Error Decoder

Flutter's layout exceptions name the mechanism, not the mistake. The first move below is right in most cases; `layout.md` carries the reasoning.

| Message | What it actually means | First move |
|---|---|---|
| `A RenderFlex overflowed by N pixels` | A flex child's chosen size exceeds the space left after its fixed siblings | `Expanded`/`Flexible` on the growing child, or make the axis scrollable |
| `Vertical viewport was given unbounded height` | A scrollable sits inside another scrollable or a `Column`'s main axis | `Expanded`, a fixed height, or convert the parent to `CustomScrollView` + slivers |
| `BoxConstraints forces an infinite width/height` | An unbounded constraint reached a widget that expands (`double.infinity` under a `Row`, `Expanded` inside a scroll axis) | Bound it at the nearest parent that knows the real size |
| `RenderBox was not laid out` | A previous layout exception aborted the pass | Fix the FIRST exception in the console; this one disappears with it |
| `Incorrect use of ParentDataWidget` | `Expanded`/`Flexible` outside a `Flex`, or `Positioned` outside a `Stack` | Make it a DIRECT child of the right parent — a `Padding` in between breaks it |
| `Cannot hit test a render box with no size` | The box was laid out with zero constraints, usually inside a zero-size parent | Give the parent a real size; check for an empty `Container` wrapper |
| `Failed assertion: 'constraints.hasBoundedHeight'` under `IntrinsicHeight` | Intrinsic sizing under unbounded constraints | Remove the intrinsic widget; intrinsics can cost O(N²) over the subtree |
| `No Material widget found` / `No Directionality widget found` | The widget is outside the app's `MaterialApp` scope | Wrap in `Material`/`MaterialApp` — in tests this is the usual cause (`testing.md`) |
| `Scaffold.of() called with a context that does not contain a Scaffold` | The context is the one that CREATED the Scaffold, not one below it | A `Builder`, a child widget, or `ScaffoldMessenger.of(context)` for snackbars |
| Anything else | The console block above the stack names the offending widget and the constraints it received | Read `The relevant error-causing widget was:` and open that line |

## Rebuild Scope Ladder

Ordered cheapest to costliest. Take the first rung that removes the rebuild, and confirm it in DevTools' rebuild counter rather than by feel (`performance.md`).

1. **`const` the parts that never change.** Free at runtime, and it stops the rebuild at that boundary (rule 5).
2. **Hoist the unchanging subtree into the `child:` slot.** `AnimatedBuilder`, `ValueListenableBuilder`, and `Consumer` all take a `child` that is built once and handed back on every rebuild — the highest-yield single edit in animation and list code.
3. **Extract the changing part into its own widget.** `setState` rebuilds the whole `State`'s subtree; a smaller widget is a smaller subtree. This is the fix for "setState rebuilds my entire screen".
4. **Listen to one value, not one object.** `ValueListenableBuilder`, `Selector`, `context.select`, `ref.watch(provider.select(...))` — rebuild on the field you render, not on every notification.
5. **Move state DOWN, not up.** State lifted higher than its only consumer forces every sibling to rebuild. Lift only to the lowest common ancestor of the widgets that actually read it.
6. **Isolate repaints with `RepaintBoundary`.** Only after build cost is gone: it addresses painting, not building, and each boundary is a separate GPU layer with its own memory cost.
7. **Restructure with slivers or a different scroll widget.** When per-item work is genuinely unavoidable, stop rebuilding the items that are off-screen (`layout.md`).

## Widget Choice

Pick the least capable widget that expresses the need — each row costs something the row above does not.

| Need | Use | Cost or trap |
|---|---|---|
| Fixed size, or space between widgets | `SizedBox` | `const`-friendly; a `Container` with only a size drags in the whole decoration pipeline |
| Padding | `Padding` | `Container(padding:)` is the same thing wrapped in more objects |
| Any list longer than one screen | `ListView.builder` / `.separated` | `ListView(children: [...])` builds and retains every item, on-screen or not |
| List with uniform row height | `ListView.builder` + `itemExtent` | Lets the viewport skip measuring items; required for instant jumps in long lists |
| Headers, grids, and lists in one scroll view | `CustomScrollView` + slivers | Nesting scrollables inside a `Column` is the wrong shape (`layout.md`) |
| Rebuild on one value | `ValueListenableBuilder` | No package needed; `setState` rebuilds the whole `State` |
| A future rendered once | `FutureBuilder` with the future held in a FIELD | Creating the future inside `build` re-runs it on every rebuild (`async.md`) |
| A continuously changing value | `StreamBuilder` over a cached stream | Re-listening to a single-subscription stream throws `Bad state: Stream has already been listened to` |
| Show/hide without losing state | `Offstage`, or `Visibility(maintainState: true)` | A conditional `if` in the child list DISPOSES the subtree — often the actual bug |
| Fade, size, or color change on a state change | `AnimatedContainer`, `AnimatedOpacity`, `AnimatedSwitcher` | Implicit animations need a CHANGED value and, for `AnimatedSwitcher`, differing keys (`animations.md`) |
| One animation driving several widgets | `AnimationController` + explicit transitions | Owns a ticker: `TickerProviderStateMixin` plus a `dispose` line (rule 3) |
| Read theme, media, or an inherited value | `Theme.of`, `MediaQuery.sizeOf`, `context.watch` | Creates a dependency: the widget rebuilds whenever that value changes |
| Reach into a child's state | A callback or a shared notifier passed down | `GlobalKey` works, but forces a global registry and blocks subtree reuse (`widgets.md`) |
| Anything else | Compose from existing widgets before writing a `RenderObject` | A custom `RenderObject` is right for genuinely custom layout and a maintenance tax everywhere else |

## Output Gates

Before emitting Flutter code, verify:

- Every `await` inside a `State` is followed by a `mounted` check before `setState`, `context`, or a controller is touched
- Every controller, `FocusNode`, subscription, and timer created has a matching line in `dispose`
- Every list of stateful children carries a stable `ValueKey`, and no `UniqueKey` appears inside a builder
- No future creation, network call, navigation, snackbar, or notifier write happens inside `build`
- Static subtrees are `const`; `AnimatedBuilder`/`ValueListenableBuilder` pass their unchanging subtree through `child:`
- Long lists use `.builder`; images from network or disk set `cacheWidth`/`cacheHeight`
- Text that can grow (labels, buttons, chips) survives a large text scale without overflowing (`accessibility.md`)
- Interactive targets meet the platform minimum, and icon-only controls carry a semantic label
- `flutter analyze` is clean — not merely "it compiles"

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/flutter/config.yaml`. Never interview the user — record a preference the moment it is stated.

| Variable | Type | Default | Effect |
|---|---|---|---|
| state_management | auto \| setstate \| provider \| riverpod \| bloc | auto | `auto` reads `pubspec.yaml` and matches the repo; the resolved value selects the idioms in `architecture.md` and the listener form used in Core Rule 8 examples |
| router | auto \| navigator \| go_router | auto | `auto` reads `pubspec.yaml`; drives every routing example, deep-link setup, and back-button pattern in `navigation.md` |
| target_platforms | list (android, ios, web, macos, windows, linux) | android, ios | Which platform sections surface in `platform.md`, `adaptive.md`, and `release.md`, and which store steps appear in the release checklist |
| target_fps | 60 \| 120 | 60 | Sets the frame budget used everywhere (1000 / target_fps ms, Core Rule 6) and therefore the jank threshold in `performance.md` and `debug.md` |
| project_layout | feature-first \| layer-first | feature-first | Where new files go, and how `architecture.md` names folders and boundaries |
| codegen | allowed \| avoid | allowed | `avoid` bans `build_runner` solutions (freezed, json_serializable, route generators) and emits hand-written equivalents in `data.md` and `architecture.md` |
| destructive_confirm | bool | true | Confirms before `flutter clean`, `--update-goldens`, and deleting `Podfile.lock`/`pubspec.lock` (`commands.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Tooling**: DI (`get_it` vs scoped providers), HTTP client (`http` vs `dio`), local storage (`drift`, `isar`, `sqflite`, `hive`), image caching package, lint set — affects every "add a package" recommendation in `data.md` and `dependencies.md`
- **Conventions**: widget file granularity, naming of state and notifier classes, private-widget vs builder-method style, `const`-everywhere policy — affects the shape of emitted code in `widgets.md`
- **Platform**: min SDK and deployment targets, flavor names, web hosting shape, desktop window behavior — affects `release.md` and `adaptive.md`
- **Design system**: Material vs Cupertino vs custom, theming through `ThemeExtension` vs constants, dark-mode obligation — affects `adaptive.md` and every styling example
- **Testing posture**: golden-test policy, coverage gate, whether integration tests run in CI, mocks vs fakes — affects the gates in `testing.md`
- **Safety posture**: how proactively to raise release-only and accessibility risks vs answering only what was asked — affects Output Gates verbosity
- **Integrations**: backend (Firebase, Supabase, REST, GraphQL), crash reporting, analytics, CI provider and distribution channel — affects `data.md` and `release.md`

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Creating a controller or a future inside `build` | `build` can run many times per second; each run makes a new object, restarts the request, and abandons the old one | Create in `initState` or as a field; dispose in `dispose` (rules 2-3) |
| `Container` everywhere | It composes decoration, constraints, padding, and transform whether or not you use them, and blocks `const` | `SizedBox`, `Padding`, `ColoredBox`, `DecoratedBox` — one job each |
| `UniqueKey()` to "force a refresh" | New identity every build: state, scroll offset, and animations reset every frame | `ValueKey(stableId)`, or change the value the widget renders |
| `GlobalKey` to reach another widget's state | Global lookup, blocks subtree reuse, and throws "multiple widgets used the same GlobalKey" on reparenting | Pass a callback down, or share a notifier (`architecture.md`) |
| `shrinkWrap: true` to silence an unbounded-height error | Lays out every child on every scroll frame; the list gets slower as it grows | `Expanded`, a bounded height, or slivers (`layout.md`) |
| `MediaQuery.of(context)` just for a size | Subscribes to ALL of `MediaQueryData`: the widget rebuilds on keyboard open, rotation, and inset changes | `MediaQuery.sizeOf(context)` (`flutter >=3.10`), or `LayoutBuilder` for the parent's real constraints |
| `Platform.isIOS` in shared code | `dart:io` does not exist on web — the app fails to compile or throws at startup | `defaultTargetPlatform`, guarded by `kIsWeb` (`adaptive.md`) |
| `Opacity` inside an animation | Wrapping a subtree triggers `saveLayer`: an offscreen buffer allocated and composited every frame | `FadeTransition`/`AnimatedOpacity`, or animate the alpha of a leaf's color |
| Network images without `cacheWidth`/`cacheHeight` | Decoded cost is width × height × 4 bytes regardless of the compressed file size; one photo can evict the whole image cache | Decode at display size (`performance.md`) |
| `flutter clean` as the first debugging move | Deletes build outputs and guarantees the slowest possible next build; it only fixes stale-artifact bugs | Read the first exception; reach for `clean` after a plugin, SDK, or native-config change (`commands.md`) |
| Catching channel failures with a bare `catch (e)` | Hides `MissingPluginException` (registration) behind `PlatformException` (the native side said no) — two different bugs | Catch `PlatformException` explicitly and branch on `code` (`platform.md`) |
| Judging performance from a debug build or a simulator | Debug is JIT plus instrumentation; simulators do not model the device GPU | `--profile` on a physical device (rule 7) |
| `if (visible) child` to hide a subtree | Removing the widget disposes its `State` — the "why did my half-filled form clear itself" bug | `Offstage`, or `Visibility(maintainState: true)` when the state must survive |

## Where Experts Disagree

- **State management library.** Bloc's camp buys testability and an explicit event log and pays in ceremony per feature; the Riverpod/Provider camp buys terseness and pays with looser conventions. The line both accept: plain `setState` is correct for state owned by one widget, and state read by two sibling subtrees needs something above them. Repo consistency outranks the ranking — a codebase running two of them is worse than either alone.
- **Codegen (`freezed`, `json_serializable`, route generators).** One camp treats generated code as the only defensible way to keep 200 models correct; the other refuses the `build_runner` step, the diff noise, and the CI minutes. Boundary: hand-written parsing scales to a few dozen models and stops scaling once nested optional fields appear. Set `codegen` once and stop re-litigating it.
- **`BuildContext`-free navigation.** A global `navigatorKey` makes navigation callable from anywhere (interceptors, notification handlers) and hides the tree dependency that makes routes testable. Reserve it for the few entry points with genuinely no context; anything triggered by a widget navigates with its own context.
- **Golden tests.** Advocates catch visual regressions no widget test sees; skeptics point at a suite that breaks on every font, platform, and SDK bump. Where the evidence lands: goldens pay off for design-system components on a pinned CI platform, and cost more than they return on full screens (`testing.md`).

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/flutter (install if the user confirms):
- `react-native` — the other cross-platform stack; when comparing or migrating
- `animate` — cross-framework motion systems and reduced-motion policy
- `in-app-purchases` — subscriptions and paywalls on top of a Flutter app
- `testflight` — distributing the iOS build produced in `release.md`
- `app-store` — store listing, metadata, and review process

## Feedback

- If useful, star it: https://clawic.com/skills/flutter
- Latest version: https://clawic.com/skills/flutter

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/flutter.
