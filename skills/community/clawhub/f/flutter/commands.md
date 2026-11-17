# Commands — Flutter and Dart CLI

The incident toolkit: the commands that answer a question or unblock a build, not the basics. Confirm before anything that discards state when `destructive_confirm` is true (SKILL.md Configuration).

## Diagnose the Toolchain

```bash
flutter doctor -v                 # every toolchain component, with paths and versions
flutter --version                 # SDK, channel, framework and engine revisions, Dart version
flutter devices                   # what you can actually run on right now
flutter config                    # which platforms are enabled for this install
```

`flutter doctor` is the first command in any "it builds on their machine" conversation — a missing Android licence or a Command Line Tools path shows up here and nowhere else.

## Run and Iterate

```bash
flutter run                                   # debug on the only/attached device
flutter run -d <deviceId> --flavor staging    # pick device and flavor (release.md)
flutter run --profile                         # the ONLY mode for performance work (SKILL.md rule 7)
flutter run --release                         # verify release behavior; not available on the iOS Simulator
flutter run --dart-define=API_URL=https://…   # compile-time configuration, not a secret store
flutter attach                                # reconnect tooling to an already-running app
```

In a running session: `r` hot reload, `R` hot restart, `p` debug paint, `o` toggle platform, `v` open DevTools, `q` quit. What each of hot reload and restart can and cannot pick up: `debug.md`.

## Analyze, Format, Fix

```bash
flutter analyze                   # the fastest path to the real error under a Gradle wall of text
dart format .                     # formatter; --set-exit-if-changed for CI
dart fix --dry-run                # what the automated migrations would change
dart fix --apply                  # apply them — a deprecation sweep after an SDK upgrade
```

## Test

```bash
flutter test                                        # all widget and unit tests
flutter test test/foo_test.dart --name 'submits'    # one file, one test by name
flutter test --coverage                             # writes coverage/lcov.info
flutter test --update-goldens                       # DESTRUCTIVE: rewrites golden files (testing.md)
flutter test integration_test/app_test.dart -d <id> # on a real device
```

## Dependencies

```bash
flutter pub get                        # resolve per the lockfile
flutter pub outdated                   # read the "Resolvable" column first (dependencies.md)
flutter pub upgrade                    # move within constraints, rewrite the lock
flutter pub upgrade --major-versions   # rewrite the CONSTRAINTS; its own commit
flutter pub deps                       # the tree — who is blocking whom
dart run build_runner build --delete-conflicting-outputs   # codegen: allowed only
```

## Build Artifacts

```bash
flutter build appbundle --release                 # Play (release.md)
flutter build apk --split-per-abi --release       # sideload / other stores
flutter build ipa                                 # App Store / TestFlight
flutter build web --release
flutter build apk --analyze-size                  # size breakdown, openable in DevTools
flutter build appbundle --release --obfuscate --split-debug-info=build/symbols/<version>
flutter symbolize -i stack.txt -d build/symbols/<version>/app.android-arm64.symbols
```

Archive the symbol directory per released version, or crashes from that build stay unreadable forever (`release.md`).

## Native Side

```bash
cd ios && pod install              # after ANY plugin change (platform.md)
cd ios && pod repo update          # when CocoaPods cannot find a version that exists
flutter logs                       # device logs, including native output
adb logcat | grep -i flutter       # Android, when the Dart console is not attached
```

Android and Xcode build failures are usually clearer in their own tools: open `android/` in Android Studio or `ios/Runner.xcworkspace` in Xcode and build there once — the message is specific in a way the Flutter wrapper's output is not.

## Cleaning (last resort, not first)

```bash
flutter clean                      # DESTRUCTIVE: deletes build/, forces a full rebuild
rm ios/Podfile.lock                # DESTRUCTIVE: re-resolves every pod
rm pubspec.lock                    # DESTRUCTIVE: re-resolves every package (dependencies.md)
```

`flutter clean` fixes stale-artifact problems and nothing else: after an SDK change, a plugin add or remove, or a native-config edit. Reaching for it before reading the first exception costs a full rebuild and teaches nothing (SKILL.md Traps).

## Project Scaffolding

```bash
flutter create --platforms=android,ios,web my_app     # only the platforms you will ship
flutter create --template=package my_lib              # pure Dart package
flutter create --template=plugin --platforms=android,ios my_plugin
flutter create . --platforms=macos                    # add a platform to an existing project
```

`flutter create .` in an existing project regenerates missing platform folders without touching `lib/` — the standard way to add a target later. Review the diff: it also rewrites platform config files.
