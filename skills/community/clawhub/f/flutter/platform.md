# Platform — Channels, FFI, Plugins, and Permissions

Reaching native code means crossing an async boundary with a codec on it. Everything below follows from that: calls are asynchronous, arguments are serialized, and either side can be missing.

## Choosing the Mechanism

| Need | Mechanism | Cost |
|---|---|---|
| Call a native API a few times (share sheet, biometrics, a vendor SDK) | `MethodChannel` | Async, serialized, hand-written on both sides |
| The same, with generated type-safe bindings | `pigeon` | A codegen step; removes the whole class of string-key and codec bugs |
| A continuous native feed (sensors, location, connectivity) | `EventChannel` | A stream you must cancel (SKILL.md rule 3) |
| Call a C or Rust library synchronously | `dart:ffi` (+ `ffigen`) | No channel overhead, no async — but a crash there kills the process |
| Existing solved problem (camera, files, purchases) | A published plugin | Someone else's maintenance; audit it (`dependencies.md`) |
| Render a native view inside Flutter | Platform views (`AndroidView`, `UiKitView`) | Real cost: composition per frame; use only when nothing else works |

## MethodChannel Discipline

- Name the channel with a reverse-domain prefix (`com.acme.app/battery`). A bare name like `battery` collides with whatever plugin picked the same word, and the collision presents as one plugin receiving another's calls.
- Every call can throw. Handle three distinct failures, because they mean different things:
  - `MissingPluginException` — no handler is registered on this platform. Either the plugin was added without a full app restart (see below), or this platform genuinely has no implementation.
  - `PlatformException` — native code answered with an error. Branch on `code`, show the `message` only if it is user-appropriate.
  - A codec error — the argument or return type is not in the standard codec's set.
- The standard codec handles null, bool, num, String, `Uint8List`/`Int32List`/`Int64List`/`Float64List`, `List`, and `Map`. Anything else — a custom class, a `DateTime`, an enum — must be converted at the boundary. A silently-null field on the native side is the usual symptom of skipping this.
- Return types arrive as `dynamic` and often as `Map<Object?, Object?>`; cast defensively (`Map<String, dynamic>.from(result)`), because a direct cast throws on the platform's actual map type.
- **Never assume symmetry.** Implement both platforms or make the Dart side degrade explicitly; an unimplemented iOS path found by a user is the standard way this bug ships.
- Calls from a background isolate need `BackgroundIsolateBinaryMessenger.ensureInitialized(token)` (`flutter >=3.7`), with a `RootIsolateToken` captured on the root isolate and passed in (`async.md`).

## The Native Side

- Handlers run on the platform's main/UI thread. Heavy work there freezes the native UI and, through it, your Flutter frames — dispatch to a background queue and reply when done.
- The reply must be delivered on the platform's main thread on Android; replying from a background thread is undefined behavior that works until it does not.
- Reply exactly once per call. Two replies, or none, is a hang or a crash with no Dart-side stack.
- `setMethodCallHandler` registered twice (a hot reload plus a re-registration) means the older handler is silently replaced — a source of "it works after a restart" confusion.

## Plugins

- **`MissingPluginException` immediately after adding a plugin**: hot restart does not register new plugins. Stop the app fully and re-run. After adding an iOS plugin, `cd ios && pod install` as well (`commands.md`).
- Federated plugins split into `*_platform_interface` and per-platform packages. A version conflict between them is the usual cause of "the plugin compiles but does nothing on Android" (`dependencies.md`).
- Check platform support before adopting: a plugin listing only Android and iOS will fail to compile — or throw `UnimplementedError` — the moment the app adds web or desktop to `target_platforms`.
- Wrap third-party plugins behind your own interface in the data layer. Plugins are the most churn-prone dependency in a Flutter app, and a wrapper turns a migration into one file (`architecture.md`).
- Audit before adding: last publish date, whether it maintains its own native code, and whether it requests permissions you would have to justify in a store review.

## Permissions

- Every permission has three states worth distinguishing: not yet asked, denied (can ask again), permanently denied (must send the user to Settings). Code that only checks granted-or-not leaves users stuck with no path forward.
- Ask in context, right before the feature needs it, with a preceding explanation screen when the reason is not obvious. A permission requested at launch is the most-denied permission.
- iOS requires a purpose string in `Info.plist` for every permission; a missing one is an immediate crash on first use, not a denial — and App Review rejects vague strings.
- Android splits permissions by API level (notifications became a runtime permission on Android 13, storage access was reworked into scoped storage). Test on both an old and a current OS version.
- Permissions can be revoked while the app is backgrounded: re-check on resume, do not cache the granted state across sessions (`state.md`).

## Platform Differences That Reach Dart

- `Platform.isAndroid`/`isIOS` from `dart:io` throws on web — `defaultTargetPlatform` guarded by `kIsWeb` is the portable form (`adaptive.md`).
- Back navigation: Android has a system back; iOS has an edge-swipe. Interception differs (`navigation.md`).
- Background execution: iOS suspends aggressively; Android has foreground services and Doze. Neither platform runs your Dart code indefinitely — anything periodic goes through the platform's own scheduler (WorkManager, BGTaskScheduler) via a plugin, and its minimum interval is the platform's, not yours.
- Push notification taps are a cold-start entry point: the payload arrives before the first frame in one path and as a stream in another. Handle both, exactly like deep links (`navigation.md`).
- File paths, keyboard behavior, haptics, and text selection controls all differ; verify on both platforms before calling a feature done.

## FFI

- `dart:ffi` calls are synchronous and run on the calling isolate: a long native call blocks the frame exactly like a long Dart loop (SKILL.md rule 6).
- Memory allocated with `malloc` must be freed explicitly (`calloc.free`); Dart's GC knows nothing about it.
- `ffigen` generates bindings from headers — write the binding by hand only for a one-function library.
- A segfault in native code takes the whole process down with no Dart stack. Isolate risky native work in a separate isolate so at least the failure is contained and observable.
- The native library must be bundled per platform and per architecture. This is a build-system problem, not a Dart problem, and it is where most FFI time goes (`release.md`).
