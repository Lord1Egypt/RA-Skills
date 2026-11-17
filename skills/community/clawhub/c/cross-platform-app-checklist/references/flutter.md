# Flutter notes

Platform facts are in the other references; this file maps their checklist
IDs to Flutter APIs and plugin traps. Check the Flutter SDK and locked
plugin versions actually shipped: package support badges do not promise
that every method works on every listed platform.

## Layout (L1–L8) — P0

- Use `LayoutBuilder` constraints for a component's available space or
  `MediaQuery.sizeOf(context)` for its containing view. Never choose layout
  from `Platform.isX`, `defaultTargetPlatform` or raw `View.physicalSize`.
  Size-specific `MediaQuery.*Of` accessors narrow rebuild dependencies.
  Pass embedded-pane / navigation context explicitly to third-party kits
  instead of letting each invent its own mobile / desktop breakpoint.
- Keep controllers and session state above a layout switch. Stable keys /
  `PageStorage` can help retain element or scroll state; they do not replace
  process-death restoration. A `GlobalKey` is not a general-purpose state
  store and reparenting has lifecycle / performance costs.
- Insets: `MediaQuery.paddingOf` reflects safe-area padding;
  `viewPaddingOf` is independent of the keyboard; `viewInsetsOf` represents
  fully obscured areas such as a docked keyboard. `SafeArea` adjusts the
  descendant `MediaQuery`, so nested consumers must not add the original
  inset again. `Scaffold(resizeToAvoidBottomInset: true)` normally resizes
  its body above the keyboard; do not also pad that body by the same inset.
- Modal routes need their own inset handling. In
  `showModalBottomSheet(useSafeArea: true, isScrollControlled: true)`,
  `useSafeArea` covers **top / left / right**, not the bottom or keyboard.
  Give sheet content appropriate bottom safe-area / keyboard padding and
  scrolling, using the route's constraints. `isScrollControlled` alone
  neither scrolls arbitrary content nor keeps a text field visible. See
  [bottom-sheet semantics](https://api.flutter.dev/flutter/material/showModalBottomSheet.html).
- Android 15 / target API 35 enables edge-to-edge by default; target API 36
  on Android 16+ removes the old opt-out. Prefer migrating insets over
  relying on `SystemChrome.setEnabledSystemUIMode` / colour calls to undo
  platform enforcement. Check gesture and 3-button navigation on-device.
  See [Flutter's migration](https://docs.flutter.dev/release/breaking-changes/default-systemuimode-edge-to-edge).
- `SystemChrome.setPreferredOrientations` is a request with platform limits.
  Android 16 / target API 36 generally ignores orientation / resizability
  restrictions on displays with smallest width ≥ 600 dp (with documented
  exceptions and a temporary opt-out); target API 37 removes that opt-out.
  Test actual resize / rotation instead of assuming a portrait call locks
  the device. See [Android large-screen changes](https://developer.android.com/blog/posts/prepare-your-app-for-the-resizability-and-orientation-changes-in-android-17).
- On letterboxed Android, `MediaQuery.size` is the letterboxed app size;
  that is right for UI layout. If an orientation policy needs display size,
  use the current view's `View.of(context).display` and convert its units
  with the display's pixel ratio. Do not use the display size for pane
  breakpoints. iPad multitasking can ignore orientation requests too;
  full-screen opt-outs are not a durable adaptation strategy. See
  [orientation API limits](https://api.flutter.dev/flutter/services/SystemChrome/setPreferredOrientations.html)
  and [orientation rules](layout.md).
- Use scrollable / collapsing headers on short windows.
  `AlertDialog(scrollable: true)` scrolls title and content; its actions use
  an `OverflowBar`. Keep action area height reachable and constrain dialog
  width to available space / a product maximum; 560 logical pixels is a
  common Material width, not an OS requirement.
- Foldables: use `MediaQuery.displayFeaturesOf(context)` and supported
  display-feature-aware layouts. Dialog / sheet `anchorPoint` can choose the
  intended sub-screen. Test both vertical and horizontal hinges rather than
  treating all foldables as two equal portrait panes.
- Connected displays / desktop windowing (L3 / L4): read density, insets
  and display data per view (`MediaQuery.*Of(context)`,
  `View.of(context)`), never once at startup or from
  `PlatformDispatcher.instance.views.first`. Native plugin UI (pickers,
  dialogs, share sheets) chooses its own display / context; check it opens
  on the window that requested it. Do not assume the shipped engine reports
  iPadOS window controls or Android caption bars as safe-area padding;
  confirm on device and keep toolbar actions clear of them.

**Verify.** Pump narrow / short and wide constraints, keyboard / safe-area
profiles, hinge profiles and breakpoint transitions; then rotate / resize
an Android tablet and iPad window in a real app. Open sheets, dialogs and
menus with the keyboard visible. See [layout.md](layout.md) for the matrix.

## Text (D1–D2) — P0 for essential content

- Respect `MediaQuery.textScalerOf(context)` and use `TextScaler.scale`
  when manually measuring text. Do not replace a nonlinear scaler with a
  single multiplier. If a specific decorative element must clamp, use the
  scaler instance's `clamp` or `MediaQuery.withClampedTextScaling` locally
  and justify the limit; do not disable accessibility scaling app-wide.
  See [TextScaler](https://api.flutter.dev/flutter/painting/TextScaler-class.html).
- Avoid `FittedBox(fit: BoxFit.scaleDown)` around essential text that should
  wrap. Chips, segmented controls and action rows need tests with long
  labels and large text. `DropdownButton(isExpanded: true, isDense: false)`
  can help sizing but does not prove selected / menu labels remain readable.
- `flutter gen-l10n`: generated getters catch unknown resource IDs, but
  missing locale translations can still fall back. Configure
  `untranslated-messages-file` and have CI fail if it reports missing
  translations (an empty JSON object is not a missing translation).
  `required-resource-attributes` requires ARB metadata, **not translation
  completeness**. Include the intended `supportedLocales` and localisation
  delegates; strings outside widgets must refresh on locale change. See
  [localisation configuration](https://docs.flutter.dev/ui/internationalization).
- Widget tests default to Ahem square glyphs. Load shipped fonts with
  `FontLoader` and control fallback fonts on CI for meaningful wrapping /
  glyph checks; system font availability is not guaranteed by installing
  one font family.

**Verify.** Test long / RTL text with real fonts and a nonlinear `TextScaler`,
then the actual maximum accessibility settings on mobile. Confirm CI fails
for an intentionally missing translation before trusting its coverage.

## Density and assets (D3–D5) — P1

- `Image.asset` resolves density variants such as `2.0x/` and `3.0x/`.
  Provide suitable raster sources or vector rendering; naming one asset a
  high-density variant does not improve its resolution.
- Decode near rendered size, for example
  `Image.asset(name, cacheWidth: (logicalWidth * dpr).ceil())`, or use
  `ResizeImage` with an `ImageProvider`. The plain `Image` constructor has
  no `cacheWidth` parameter. `MediaQuery.devicePixelRatioOf(context)` can
  change at runtime; update derived decode / screenshot sizes without
  rescaling the logical UI twice. Bound caches and repeated decode work.
  See [Image.asset](https://api.flutter.dev/flutter/widgets/Image/Image.asset.html)
  and [M5](media-devices.md).
- `flutter_launcher_icons` supports platform-specific sources and Android
  `adaptive_icon_monochrome`; do not claim that it cannot generate a
  monochrome layer. Inspect generated artifacts for the locked version:
  launcher, notification and tray icons are different assets, and generating
  sizes cannot fix unsuitable artwork / geometry. See the
  [package configuration](https://pub.dev/packages/flutter_launcher_icons)
  and [platform icon rules](display.md).
- Keep the Windows runner's PerMonitorV2 DPI-awareness declaration when
  customising it. Verify the compiled runner and native plugin windows,
  rather than assuming every historical template has the same manifest.

**Verify.** Move a release desktop window across mixed-DPI monitors and
change scaling while an image / popup is visible. Check sharpness, decode
memory, icon artifacts and native plugin UI as well as Flutter widgets.

## Input (I1–I9) — P1 (P0 for navigation / text loss)

- `MaterialTapTargetSize.padded` / `kMinInteractiveDimension` help supported
  Material controls reach 48 logical pixels; they do not enforce the actual
  hit area of arbitrary widgets or overrides. Measure the interactive
  render box and tap edges. Run accessibility guideline matchers.
- Use `MouseRegion`, `Tooltip`, secondary-tap handlers, `Shortcuts` /
  `Actions`, `FocusTraversalGroup` and visible focus as appropriate.
  `SingleActivator(..., meta: true)` versus `control: true` follows the
  shortcut convention; platform detection is appropriate for conventions,
  not layout. Prefer Flutter's text-editing actions over overriding native
  selection / copy / paste shortcuts. See [input.md](input.md).
- Material desktop scroll behaviour adds scrollbars to many scrollables;
  thumbs fade by default. `Scrollbar(thumbVisibility: true)` needs the
  appropriate `ScrollController`; do not attach one controller to multiple
  independently interactive scrollbars. Avoid duplicate automatic / manual
  bars. Mouse drag-to-scroll is not the same as wheel / trackpad scrolling;
  configure `ScrollBehavior.dragDevices` deliberately. See
  [Scrollbar](https://api.flutter.dev/flutter/material/Scrollbar-class.html).
- For a custom Enter-to-send handler, active IME composition requires a
  **valid, non-collapsed** composing range. `isValid` alone also accepts an
  empty range and can suppress sending forever. Prefer `TextField` editing
  / submission actions where they match the flow; test composition commit,
  multiline input, key repeat and Shift+Enter on actual IMEs.
- Back: `PopScope(canPop:, onPopInvokedWithResult:)` must expose whether a
  pop is allowed before the predictive gesture. The callback reports whether
  it already happened; do not pop again when `didPop` is true. Check the
  merged `android:enableOnBackInvokedCallback` configuration and SDK / router
  support instead of assuming adding a manifest flag completes migration.
  See [PopScope](https://api.flutter.dev/flutter/widgets/PopScope-class.html).
- `IconButton.tooltip` normally supplies its accessible description; avoid
  duplicate wrapper labels. For custom controls expose the correct name,
  role, state and action with `Semantics`. Use `tester.ensureSemantics()`,
  `find.bySemanticsLabel` and guideline matchers such as
  `androidTapTargetGuideline`, `labeledTapTargetGuideline` and
  `textContrastGuideline`, then exercise a platform screen reader.
- Use `MediaQuery.alwaysUse24HourFormatOf(context)` for a user-requested
  time convention alongside locale-aware formatting; do not format time by
  concatenating translated fragments.
- Menus (I2): Flutter's built-in `PlatformMenuBar` implementation supports
  **macOS only**; elsewhere it just returns its child. iPadOS menu-bar
  integration needs native `UIMenuBuilder` work or a verified plugin, and
  Windows / Linux need in-window menus (`MenuBar`, `MenuAnchor`). Keep one
  command model behind menus, `Shortcuts` and toolbar buttons so enabled /
  checked state agrees. See [PlatformMenuBar](https://api.flutter.dev/flutter/widgets/PlatformMenuBar-class.html).
- Verified links (I8): since Flutter 3.27 the embedder's deep-link handler
  defaults to **on** (`flutter_deeplinking_enabled` meta-data on Android,
  `FlutterDeepLinkingEnabled` in Info.plist). With Flutter's handler, links
  go to the router (`go_router` / `Router` / `MaterialApp.routes`); with
  a plugin such as `app_links`, set both flags to `false` or links are
  handled twice / not at all. Instantiate the plugin early enough to catch
  the cold-start link. Router or plugin config does not verify the domain:
  `assetlinks.json` (release / Play App Signing SHA-256) and
  `apple-app-site-association` plus the Associated Domains entitlement are
  host / native work. Desktop `app_links` support differs per platform and
  link type; check its matrix. See
  [deep-links flag change](https://docs.flutter.dev/release/breaking-changes/deep-links-flag-change),
  [App Links setup](https://docs.flutter.dev/cookbook/navigation/set-up-app-links)
  and [Universal Links setup](https://docs.flutter.dev/cookbook/navigation/set-up-universal-links).
- Transfers (I9): `Clipboard` in `services` is plain text only. Typed
  clipboard / drag needs a plugin: `super_clipboard` and
  `super_drag_and_drop` (shared native layer; Android NDK and a content
  provider; drag out via `DragItemWidget`; author-labelled experimental),
  `pasteboard` (images / files; Android `FileProvider`), `desktop_drop`
  (drop-in only). `share_plus` shares files on Android / iOS / macOS /
  Windows / web but **not Linux**, shares URIs as text on web / Windows /
  Linux, should receive an accurate `sharePositionOrigin` for the iPad
  popover (check the locked version's fallback), and may return
  `ShareResultStatus.unavailable`. Receiving shares (share extensions,
  Android `ACTION_SEND`) is native host configuration, not Dart code.
  For `super_drag_and_drop`, request data before `onPerformDrop` returns
  and let that callback finish promptly (it blocks the platform thread);
  consume delivered data asynchronously. Copy received / dropped content
  into app storage before its provider-specific access expires, or retain a
  supported grant / bookmark (P6).

**Verify.** Complete core flows by keyboard, pointer, touch and screen
reader on shipping platforms. Test a composing IME, nested back navigation,
cancelled predictive back and long text in menus; see [input.md](input.md).
Open verified links from another app on a clean release install with Flutter's
handler state as shipped, and exchange typed content with real apps.

## Lifecycle and data (B1–B8) — P0 for state / session loss

- `AppLifecycleListener` / `WidgetsBindingObserver`: `inactive` can be
  visible without focus; `hidden` means all views are hidden; `paused` is
  a mobile lifecycle state, not a desktop focus-loss event. Callbacks can
  be skipped during abrupt termination. Persist important edits as they
  happen; do not wait exclusively for `detached` or `onExitRequested`.
  See [AppLifecycleState](https://api.flutter.dev/flutter/dart-ui/AppLifecycleState.html).
- Apply resource-specific policy: a focus change alone should not end a
  call, but camera plugins / OS capture interruptions may require releasing
  and reacquiring capture even on `inactive`. Likewise valid background
  audio must not be stopped merely because the app becomes hidden. See
  [media rules](media-devices.md) and the camera note below.
- `RestorationMixin` / `restorationScopeId` restore participating state;
  controllers, files and app data are not automatically persisted. For
  Android `image_picker`, run `retrieveLostData()` during startup, handle
  errors and reconcile recovered attachments with drafts once (M4).
- Call `getNotificationAppLaunchDetails()` on a
  `FlutterLocalNotificationsPlugin` instance on supported implementations;
  buffer routing until navigation is ready and handle foreground /
  background response callbacks
  separately. Plugin background handlers have platform / isolate limits;
  do not assume a UI navigator is available there.
- Desktop window / single-instance packages need a per-platform capability
  check. `window_manager` / `screen_retriever` do not remove Wayland
  placement restrictions. With `RandomAccessFile.lock`, Linux / macOS
  locks are advisory and process-wide: closing another descriptor for the
  same file can release them, and another isolate can acquire the lock.
  Windows locks belong to a handle and require matching unlock ranges;
  other handles cannot write the locked region. Keep a dedicated handle
  for ownership and separate activation metadata; verify with independent
  processes on each OS (B5), not only isolates. See
  [Dart lock semantics](https://api.dart.dev/dart-io/RandomAccessFile/lock.html).
- `Future.timeout` stops waiting; it does **not** cancel the source future.
  A timed-out save / disconnect / dispose may still mutate state later.
  Share and join the original quit future. Before resuming a session after
  teardown began, confirm the operation supports cancellation and services
  remain usable, or rebuild them explicitly. Catching `TimeoutException`
  and returning `AppExitResponse.cancel` does not undo disposal. Test late
  completion explicitly (W2). See
  [`Future.timeout`](https://api.dart.dev/dart-async/Future/timeout.html).
- An Android foreground-service plugin still needs the host manifest,
  matching service type / permissions and a legally startable service.
  Follow [B4](lifecycle.md); a Dart timer is not background execution policy.
- Migrations (B7): `drift` — bump `schemaVersion`, use
  `MigrationStrategy(onUpgrade: stepByStep(...))` and
  `dart run drift_dev make-migrations` to keep schema snapshots and generate
  migration tests; commit the snapshots. `sqflite` — `openDatabase(version:,
  onUpgrade:, onDowngrade:)` callbacks already run in a transaction; handle
  every `oldVersion` path, not only the previous release. Linux / Windows
  need `sqflite_common_ffi`; macOS is supported directly by `sqflite`.
  Record and test the SQLite build used by each backend. `shared_preferences`: renaming keys loses values;
  moving from legacy `SharedPreferences` to `SharedPreferencesAsync` /
  `WithCache` needs
  `migrateLegacySharedPreferencesToSharedPreferencesAsyncIfNecessary`
  (Android's new backend is DataStore, a different store). The package says
  it must not hold critical data; writes may not be on disk when the call
  returns. For other stores (Isar, Hive, ObjectBox) check the locked
  version's migration support and maintenance status before relying on it.
- Offline sync (B8): Flutter supplies no sync engine. Keep sync status in
  the local store with the record, not only in a provider / bloc, and make
  the repository the single writer; see
  [offline-first patterns](https://docs.flutter.dev/app-architecture/design-patterns/offline-first).
  `connectivity_plus` reports an interface, not service reachability (X8).

**Verify.** Abrupt process loss during editing / a system picker, focus
loss with an active call, hidden / resumed capture and second launch with
activation arguments. Confirm durable state and no duplicated attachments.
Run generated / fixture migration tests from every supported schema on
the real SQLite build per platform, then upgrade an installed old release.

## Permissions and store (P1–P9) — P0

- `permission_handler`: host declarations remain necessary. CocoaPods
  integrations enable the required `PERMISSION_*` macros in the Podfile
  (for example `PERMISSION_CAMERA=1`). Current Swift Package Manager
  integrations derive enabled permissions from usage-description keys in
  the app's Info.plist; they do not use the Podfile setup. Follow the
  **locked version's** instructions and validate flavor / build-specific
  plists and SPM caching behaviour. See
  [permission_handler setup](https://pub.dev/packages/permission_handler).
- Use the returned request result and re-check on return from Settings;
  handle limited / restricted / permanently denied states according to
  the capability. `openAppSettings()` opens settings; it does not grant
  access. macOS / Linux support must come from an actual implementation,
  not an assumed `permission_handler` method.
- Inspect the merged Android **release / flavor** manifest and packaged
  Info.plist / privacy manifests / entitlements, including plugin-added
  declarations. Intermediate paths vary by Gradle / plugin version; use
  the build's manifest-merger report or APK Analyzer instead of hard-coding
  one directory. See [permissions.md](permissions.md).
- In typical macOS runners, check both `DebugProfile.entitlements` and
  `Release.entitlements`, plus any custom configurations. Keep functional
  capabilities aligned while retaining debug-only signing differences (W4).
- `flutter_secure_storage`: Keychain items can survive uninstall; apply an
  explicit reinstall / sign-out policy to entries owned by the app, not an
  unconditional wipe of shared credentials. Linux implementations need the
  documented native Secret Service / keyring dependencies; handle locked /
  missing services without hanging startup. See [P5](permissions.md).
- Purchases (P8): `in_app_purchase` supports **Android, iOS and macOS
  only** — no Windows, Linux or web; those need a separate channel /
  backend or no purchase UI. On Apple it uses StoreKit 2 by default
  (StoreKit 1 is an explicit opt-in). Listen to `purchaseStream` from app
  start, not only on the purchase screen. After verifying and delivering,
  call `completePurchase` when `pendingCompletePurchase` is true: on Android
  this is the acknowledgement (unacknowledged purchases are refunded after
  3 days); on Apple an unfinished transaction is redelivered and blocks a new
  purchase of that product. `PurchaseStatus.pending` grants nothing. Restored
  purchases need the same verification. Verify server-side and derive
  entitlements from the backend so other platforms see them. See
  [in_app_purchase](https://pub.dev/packages/in_app_purchase).
- Store requirements (P9): `flutter gen-l10n` covers the binary, not store
  listing text / screenshots. For Kids / Families audiences, audit every
  plugin's bundled native SDK (ads, analytics, crash reporting) in the
  packaged artifact, not only Dart imports.

**Verify.** Fresh installed release, first request denied, limited access,
Settings change and each flavor's artifact. Check that permission dialogs
actually appear on the relevant device and unsupported hosts degrade.
Exercise purchases with store sandbox / test accounts, including pending
and interrupted cases and a relaunch before completion.

## Media and audio (M1–M8) — P0 if used

- Audio plugins can each configure `AVAudioSession`. Coordinate with
  `audio_session` or the call engine's documented integration and reapply
  the intended configuration after plugin initialization where necessary.
  A common Dart API does not make focus / routing behaviour identical on
  all hosts. See [audio_session](https://pub.dev/packages/audio_session).
- `wakelock_plus` controls display wakefulness, not an Android CPU wakelock
  or background-service permission. One owner should release it when the
  last qualifying visible session ends, including error paths (M1).
- `camera` does not handle lifecycle for the app. Its documented mobile
  example disposes on `inactive` and recreates on `resumed`; do not blindly
  override that with a hidden-only rule. Retaining capture during iPad
  multitasking requires verified OS **and plugin** support. Serialise
  initialization / disposal and ignore stale async completions so resume
  cannot install an already-disposed controller. Handle denied / restricted
  initialization errors. See [camera lifecycle](https://pub.dev/packages/camera).
- The endorsed `camera` package does not imply desktop camera support.
  Likewise desktop `image_picker` file selection does not provide a camera
  UI by default; a supported `cameraDelegate` or separate capture backend
  is needed. Check actual backend support for external cameras (M3).
- Do not assume `image_picker` quality / maximum-size options force HEIC
  into JPEG. Inspect the result and explicitly transcode if required by
  the receiver. Camera results can live only in cache; move / copy durable
  attachments before cleanup. Test HEIC on a physical Apple device and
  cloud-only items offline. See [image_picker](https://pub.dev/packages/image_picker)
  and [format / access rules M4](media-devices.md).
- For ZIP / a protocol defined with POSIX separators use `path.posix`;
  use the local `path` context for real filesystem paths. A content URI is
  not a local path; do not run it through `File(uriString)` (M4 / W3).
- ChromeOS / TV / XR (M7): these receive the Android build; there is no
  separate Flutter target. ChromeOS adds keyboard, mouse and resizable
  windows, so the I2 and L3 notes apply. TV needs host-manifest leanback /
  launcher-banner declarations and D-pad navigation: check that directional
  keys move visible focus through `Focus` / `FocusTraversalGroup` and that
  the remote's select key activates controls. Treat Android XR as a
  compatible 2D Android runtime unless a verified plugin or native
  integration provides the required spatial features.

**Verify.** Use the media reference's real-device route / camera / capture
checks, including permission denied, lock / resume, another plugin taking
over audio, resize during capture and rapid cancel / reopen.

## Performance (F1–F3) — P1

- Frame pacing (F1): measure in **profile mode** (`flutter run --profile`)
  on physical devices, never debug (JIT, asserts) or a simulator. Use the
  DevTools Performance view and performance overlay: UI and raster thread
  each need to fit the active refresh period. Impeller is the only renderer
  on iOS and the default on Android (API 29+ with Vulkan, otherwise OpenGL
  fallback) and, in current releases, on desktop; profile the renderer
  actually shipped on each device class, including the Android fallback.
  Shader / raster jank conclusions from one renderer do not carry over. See
  [UI performance](https://docs.flutter.dev/perf/ui-performance) and
  [Impeller](https://docs.flutter.dev/perf/impeller).
- 120 Hz on iPhone needs `CADisableMinimumFrameDurationOnPhone = true` in
  Info.plist. Current `flutter create` templates include it; older or
  hand-edited runners may not. Drive custom animation from elapsed time
  (`Ticker` / `AnimationController`), not frame counts.
- Size / startup (F2): `flutter build <target> --analyze-size` (apk,
  appbundle, ios, linux, macos, windows; not web) writes a JSON for the
  DevTools app-size tool; diff two builds there. The `.aab` / `.ipa` is an
  upload size: read download / install size from Play Console and App Store
  Connect / an Xcode size report. Deferred components (`loadLibrary()`)
  work only on Android (dynamic feature modules) and web. Keep `main()`
  before `runApp` minimal and await only what the first screen needs. See
  [app size](https://docs.flutter.dev/perf/app-size).
- Energy (F3): hidden `AnimationController`s / tickers outside `TickerMode`,
  `Timer.periodic` polling and reconnect loops keep the engine and radios
  busy. Mute offscreen tickers and stop polling / reconnect loops when their
  work is no longer needed, applying B1's resource-specific lifecycle
  policy and preserving supported background work (B4). Obtain thermal /
  power signals through a verified plugin or platform channel.

**Verify.** Profile-mode traces on the slowest supported device and on a
120 Hz device; `--analyze-size` diff per release; startup timed with
realistic data; idle energy measured with native tools (Xcode / Android
Studio profilers).

## Testing and release integration (X1–X9, W4) — P0 for release

- Build a plugin matrix by method / platform / architecture, including
  native dependencies and minimum OS. For unsupported methods provide a
  fallback before invocation; catching `MissingPluginException` only after
  a user action is not a completed feature. Widget mocks cannot verify
  plugin registration, native signing or hardware support.
- Layout sweeps should vary `tester.view.physicalSize` and
  `devicePixelRatio` consistently with logical size; reset view overrides,
  locale / inset overrides and error handlers in teardown. Use real fonts
  and nonlinear text scaling. Preserve normal `FlutterError.onError`
  reporting while collecting overflow evidence, and check
  `RenderParagraph.didExceedMaxLines` after layout. It detects truncation,
  not every parent clip / occlusion; add visibility / hit tests for essential
  actions. See [truncation API](https://api.flutter.dev/flutter/rendering/RenderParagraph/didExceedMaxLines.html).
- Use `integration_test` for real flows; drive rotation / window resize
  from device / emulator / desktop controls too. Calling
  `SystemChrome.setPreferredOrientations` alone cannot prove a resize
  occurred on a platform that ignores it. Assert size actually changed and
  the open item, draft, selection and navigation state survived.
- Golden tests need controlled fonts, renderer / SDK and host assumptions;
  platform differences require deliberate baselines, not a broad tolerance
  that hides clipped content. Goldens do not prove native overlays or
  screen-reader behaviour; see [testing.md](testing.md).
- Build and install every shipped native architecture. Keep iOS device
  and simulator artifacts separate; an arm64 simulator library is not an
  arm64 device library. Check deployment targets against every bundled
  native framework, and exercise macOS / Windows ARM dependencies where
  supported. Verify desktop releases on a clean machine (W4).
- Windows target selection can follow the **Dart process ABI**, not the
  runner CPU: [Flutter 3.41.9's build command](https://github.com/flutter/flutter/blob/3.41.9/packages/flutter_tools/lib/src/commands/build_windows.dart#L67-L70)
  uses [hostPlatform / Abi.current()](https://github.com/flutter/flutter/blob/3.41.9/packages/flutter_tools/lib/src/base/os.dart#L478-L485),
  and its [SDK bootstrap](https://github.com/flutter/flutter/blob/3.41.9/bin/internal/update_dart_sdk.ps1#L50-L65)
  can fall back to x64. Record framework / engine revisions and the actual
  Dart ABI, verify target SDK / engine availability, then inspect every
  packaged native binary (X6). Changing CMake paths or package labels cannot
  supply a missing engine or supported cross-compilation. Check the pinned
  release's support, not only the current [platform matrix](https://docs.flutter.dev/reference/supported-platforms#previous-flutter-versions);
  [maintainer discussion](https://github.com/flutter/flutter/issues/186730#issuecomment-4511188861)
  documents version-dependent limits. This example is not a permanent
  minimum-version rule or proof that an app's ARM64 build / smoke test passed.
- Android Flutter apps include native engine / plugin libraries. Validate
  **all** bundled `.so` files and APK / bundle packaging for 16 KB page
  compatibility, then run on a 16 KB device / emulator. Updating Dart code
  or the engine does not rebuild an incompatible prebuilt plugin library.
  Check current Play enforcement and any app-specific extension rather
  than copying an old deadline. See
  [Android's 16 KB checks](https://developer.android.com/guide/practices/page-sizes).
- Native CI (X6): `flutter analyze` and ordinary unit / widget tests do
  not compile native plugin implementations (integration tests run on a
  device do). Gate dependency / plugin changes with
  `flutter build` in release mode on each required host — iOS / macOS on
  macOS, Windows on Windows, Linux on Linux — and an installed
  `integration_test` smoke run (launch, database open, changed plugin
  methods). Fail the pipeline when a platform job is skipped. A plugin
  upgrade can raise the iOS / macOS deployment target or Android
  `minSdk`; diff the generated Podfile / Package.swift / Gradle values
  against the support policy. See
  [supported platforms](https://docs.flutter.dev/reference/supported-platforms).
- Production diagnostics (X9): route both `FlutterError.onError`
  (framework errors) and `PlatformDispatcher.instance.onError` (uncaught
  errors outside Flutter callbacks) through the sanitised reporter. Keep
  `FlutterError.presentError` in developer builds only (it writes raw
  errors to the device log); return `true` from the dispatcher handler only
  when the error was handled. Background isolates are
  separate: forward with `Isolate.addErrorListener` or catch inside the
  isolate. `ErrorWidget.builder` controls the release build-failure UI.
  See [handling errors](https://docs.flutter.dev/testing/errors).
- Dart diagnostic inputs are not automatically safe metadata: an object
  can override `runtimeType` / `toString`, and a caller can supply a custom
  `StackTrace`. Do not invoke them to derive a supposedly fixed release
  category or trust a stack merely because it implements that interface.
  Test such objects and a throwing reporter in compiled-product policy
  tests. An internal `StackTrace.current` is the reporter's capture point,
  not the original throw site; X9's readable-stack qualification remains
  separate.
- Reduced motion (D7): read inherited animation preferences at the supported
  widget dependency lifecycle point and respond to later changes, not only
  once at construction.
- `--obfuscate --split-debug-info=<dir>` works for Android, iOS, macOS,
  Windows and Linux release builds (not web, which is minified instead).
  Archive the per-architecture `.symbols` files (Windows x64 emits a PDB)
  with each build; `flutter symbolize` needs the exact match and cannot read
  PDBs. Code that depends on `runtimeType.toString()` / class names breaks
  under obfuscation. Native dSYMs, Android native symbols / R8 mappings and
  desktop PDBs / debug info are separate uploads. See
  [obfuscation](https://docs.flutter.dev/deployment/obfuscate).
- Crash SDK coverage differs per platform: `firebase_crashlytics` lists
  Android, iOS and macOS only; `sentry_flutter` lists all six plus web but
  documents native crash capture only for some. Record which hosts report
  Dart errors and which report native crashes; scrub tokens, URLs and
  content from breadcrumbs / logs before upload.
- Apple compatibility surfaces (W4): Flutter's supported targets are iOS,
  Android, macOS, Windows, Linux and web; Mac Catalyst and native visionOS
  are **not** Flutter targets. "Designed for iPad" on Apple silicon Macs
  and compatible iPad apps on visionOS run the iOS build, with iOS plugins
  meeting a different host; disable those availability options in App Store
  Connect unless the build was exercised there. A native Flutter macOS app
  is a separate bundle with its own plugins, entitlements and data paths.

**Verify.** Record the SDK / locked plugin versions, artifact, host OS /
architecture and device evidence. A widget test / successful build is not
"verified" for permissions, real audio routes, external hardware, native
pickers or store / installed-release behaviour. Trigger a Dart error, an
isolate error and a native crash on each native host, in the shipped
release configuration (obfuscated where used), and confirm a readable, symbolicated report arrives. For web, build
with `--source-maps` (and `--wasm` when shipped), archive the maps, upload
them privately and exclude them from public hosting; verify readable
reports from every shipped output.

## If a web build ships (X1 / X6 / X8) — P1 when web is a target

Skip this section unless the product ships a Flutter web build.

- `dart:io` is unavailable and `Platform.isX` throws `UnsupportedError`;
  use `kIsWeb` and conditional imports keyed on `dart.library.js_interop`
  (`dart.library.html` / `dart.library.js` are not available under Wasm).
  Plugins need a web implementation; check each method.
- `flutter build web` emits JavaScript; `flutter build web --wasm` adds a
  Wasm build with JavaScript fallback for browsers without WasmGC (all iOS
  browsers use the fallback). Multithreaded Wasm rendering needs
  `Cross-Origin-Opener-Policy` / `Cross-Origin-Embedder-Policy` headers,
  which can break third-party embeds. Test each output in each browser in
  the support policy. See [Wasm](https://docs.flutter.dev/platform-integration/web/wasm).
- URL strategy: the default is hash URLs. `usePathUrlStrategy()` requires
  the server to rewrite unknown paths to `index.html` and a correct
  `<base href>` for non-root hosting; otherwise a refreshed nested route
  404s. See [URL strategies](https://docs.flutter.dev/ui/navigation/url-strategies).
- Caching: Flutter no longer generates a caching service worker by
  default; configure one if offline support is promised. Revalidate
  `index.html` / bootstrap files and use versioned deployment paths that
  retain assets an already-open tab may still request, or provide a tested
  reload / recovery path.
- Network / images: cross-origin HTTP fetches and image-pixel access
  require CORS headers from the API / CDN; the app cannot set them. Without
  CORS, Flutter can use an HTML `<img>` element fallback for display only,
  but `Image.network` must opt in (`webHtmlElementStrategy`); test
  the shipped renderer and any image operations you need. Browser storage
  can be evicted; treat it as a cache unless persistence is requested and
  verified.
- DevTools cannot attach to a web app in profile mode; profile with the
  browser's tools. JavaScript deferred imports emit additional `.js` chunks
  that must deploy with their matching release; for Wasm, check the locked
  SDK's deferred-loading support (experimental) and verify the generated
  output. See [web FAQ](https://docs.flutter.dev/platform-integration/web/faq).

**Verify.** On the hosted release in each supported browser: open a
nested URL directly and refresh, Back / Forward, deny a browser
permission, block storage, reopen offline (if promised) and deploy a new
version while an old tab is open.
