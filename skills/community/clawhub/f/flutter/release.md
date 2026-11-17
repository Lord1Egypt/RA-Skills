# Release — Build Modes, Flavors, Signing, Size, and Store Artifacts

Release builds differ from debug in ways that only appear in release (SKILL.md rule 9). This file is the list of those differences and the process around them.

## Build Modes

| Mode | Compilation | Assertions | Use |
|---|---|---|---|
| debug | JIT, hot reload, service extensions, inspector | On | Development only. Performance numbers here are meaningless (SKILL.md rule 7) |
| profile | AOT, tracing kept, inspector partly available | Off | Every performance measurement. Not available on simulators |
| release | AOT, tracing stripped, asserts removed, tree shaking | Off | What users run. Verify here before shipping |

- Release mode is not available on the iOS Simulator; profile and release require a physical iOS device.
- `kDebugMode`, `kProfileMode`, `kReleaseMode` are compile-time constants: code inside `if (kDebugMode)` is tree-shaken out of release entirely — the correct home for verbose logging.
- `assert(() { ...; return true; }())` is the idiom for debug-only side effects; the whole block disappears in release.

## What Breaks Only in Release

| Symptom | Cause | Fix |
|---|---|---|
| Icons render as blank boxes | Icon tree-shaking removed glyphs it could not prove were used (non-const `IconData`) | Make the `IconData` const, or build with `--no-tree-shake-icons` |
| An asset is missing | Not declared in `pubspec.yaml`, or a directory entry without a trailing slash | Declare it; assets are matched literally |
| Code that "always worked" no longer runs | It lived inside an `assert`, or depended on an assert's side effect | Move real logic out of asserts |
| Type or reflection lookups fail | Obfuscation renamed the symbols; `Type.toString()` and runtime type-name switches break | Do not switch on type names; use explicit tags |
| Crash reports are unreadable | AOT symbols were split out of the binary | Upload the symbol files, and symbolize (below) |
| Works on your device, crashes on others | A native library missing for that ABI, or a platform-specific permission | Test a real store-track build on a second device |
| White screen at launch | An exception before the first frame | Read native logs — the Dart console is not attached to a store build |

## Flavors and Environments

- Flavors are a native build concept (Android product flavors, iOS schemes/configurations) plus `--flavor` on the Flutter command. Dart-only "environments" cannot change the bundle id, the app name, or the icon — which is what actually keeps two builds installable side by side.
- The minimum useful set: dev, staging, production, each with its own application id suffix, display name, and icon. Anything less and testers install over their production app.
- Configuration values enter with `--dart-define` (or `--dart-define-from-file`). They are compiled in and readable in the artifact: they select an environment, they are not a secret store (`data.md`).
- Firebase and other services need per-flavor config files wired into the native build, not chosen at runtime.

## Signing

- **Android**: a release key in a keystore, referenced from `key.properties`, which is gitignored. A build without it silently signs with the debug key and Play rejects the upload. Play App Signing holds the distribution key; the upload key is yours to keep and back up — losing it without App Signing enrolled means a new listing.
- **iOS**: a distribution certificate plus a provisioning profile matching the bundle id and capabilities. Automatic signing works for a single developer; a team wants explicit profiles in version control via a credentials-management tool.
- Store both platforms' credentials in CI secrets, never in the repo. A committed keystore is a compromised app.
- Bumping the version: `version: 1.4.0+42` in `pubspec.yaml` is name + build number. Both stores reject a build number that is not higher than the last upload — automating it from the CI run number removes the most common failed-upload cause.

## Artifacts

| Target | Command shape | Note |
|---|---|---|
| Android, for Play | `flutter build appbundle --release` | Play requires an app bundle for new apps; it generates per-device APKs |
| Android, sideload or another store | `flutter build apk --split-per-abi` | A universal APK carries every ABI and is much larger |
| iOS, for App Store or TestFlight | `flutter build ipa` | Then upload from Xcode or the command-line tool (`testflight`) |
| Web | `flutter build web --release` | Ships the engine plus your app; measure the initial download |
| Desktop | `flutter build macos` / `windows` / `linux` | Packaging, notarization, and installers are per-platform work |

## Obfuscation and Symbols

```
flutter build appbundle --release --obfuscate --split-debug-info=build/symbols/<version>
```

- `--obfuscate` requires `--split-debug-info`. It renames Dart symbols; it does not encrypt strings, and an API key in the source is still extractable.
- Keep the symbol directory per released version, forever. Without it, `flutter symbolize -i stack.txt -d build/symbols/<version>/app.android-arm64.symbols` cannot decode a crash from that build, and crash reporting is useless for exactly the releases that matter.
- Upload the platform symbol files (dSYMs on iOS, native symbols on Android) to the crash reporter in the same CI step that produces the artifact, so it can never be skipped.

## Size

- Measure, do not estimate: `flutter build apk --analyze-size` (and the equivalents for other targets) emits a breakdown that DevTools can open. The usual top entries are the engine, uncompressed images, and fonts.
- Highest-yield reductions, in order: ship an app bundle (per-device delivery), compress and right-size images, subset fonts to the glyphs you use, and remove packages that pull in large native dependencies (`dependencies.md`).
- Deferred components (Android) and deferred imports (web) move rarely used code out of the initial download. On mobile the complexity rarely pays unless the app is large; on web it usually does.
- Adding a locale, an ABI, or a large plugin all move the number — check size in CI on a schedule so a regression is attributable to one merge.

## Release Gate

Before submitting:

- The `--release` artifact was installed and launched on a physical device for every entry in `target_platforms`
- Version name and build number are higher than the last submission on every store
- Signing uses release credentials, verified by the store's own upload check
- Symbol files for this exact build are archived and uploaded to the crash reporter
- Crash reporting and analytics initialize in release (they are frequently wired only in debug)
- Debug-only paths are gone: verbose logs, test endpoints, seeded accounts, and any dev banner
- Permissions in the manifest and `Info.plist` match what the app actually uses, each with a purpose string a reviewer will accept
- Deep links resolve from a cold start on a real device (`navigation.md`)
- The store listing's minimum OS versions match what the build actually supports
