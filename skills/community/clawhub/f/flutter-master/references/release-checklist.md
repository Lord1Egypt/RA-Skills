# Release Checklist

## Versioning

`pubspec.yaml`'s `version: 1.2.3+45` — the part before `+` is the user-facing semantic version, the part after is the build number, which must strictly increase on every store submission (both platforms). Check this is actually bumped per release, not left stale — a common CI-less-project mistake.

## Build flags

Production builds should include:
```bash
flutter build appbundle --release --obfuscate --split-debug-info=build/symbols
flutter build ipa --release --obfuscate --split-debug-info=build/symbols
```
Verify the build is actually `--release`, not `--debug`/`--profile` accidentally shipped (debug builds are much larger and slower, and profile builds include tracing overhead). Confirm `--obfuscate` is used and the symbol files from `--split-debug-info` are archived somewhere retrievable per version, for future crash symbolication.

## App signing

- Android: a proper upload keystore, not a debug key, referenced via `key.properties` (gitignored, never committed) in `android/app/build.gradle`. Losing the upload key is recoverable via Play App Signing (Google keeps the real signing key) but only if that was set up — check.
- iOS: valid provisioning profile + certificates managed via Xcode/Fastlane match, not manually juggled per machine.

## Store metadata & compliance

- Privacy policy URL present and accurate — required by both stores, and must actually reflect what the app collects (mismatches are a common rejection reason and, more importantly, a real user-trust issue).
- Play Store's Data Safety section / App Store's Privacy Nutrition Label filled out accurately — cross-check against what the app's dependencies actually collect (analytics SDKs, crash reporters, ad SDKs all count).
- Permission usage descriptions (`NSCameraUsageDescription`, etc. on iOS; Android permission rationale) are specific and honest, not generic boilerplate — vague descriptions are a rejection risk.
- Target SDK version meets the current store minimum (Play Store enforces a rolling `targetSdkVersion` floor roughly annually) — check this isn't stale enough to block submission.

## CI/CD

A reasonable baseline pipeline (GitHub Actions, Codemagic, Bitrise, or similar):
1. On every PR: `flutter analyze`, `dart format --set-exit-if-changed`, `flutter test`.
2. On merge to main / tag: build release artifacts, run `flutter build appbundle`/`flutter build ipa`.
3. Optional but valuable: automated deployment to internal testing tracks (Play Console internal track, TestFlight) via `fastlane` so every merge is testable by QA/stakeholders without a manual build step.

Flag a total absence of CI as a high-priority finding for any project beyond a solo prototype — it's relatively cheap to set up and prevents an entire category of "it worked on my machine" and regression problems.

## Crash & analytics monitoring

Confirm a crash reporter (Firebase Crashlytics, Sentry) is actually wired up and tested (not just added as a dependency but never verified to report). Without this, post-release issues are invisible until users complain. Confirm it's configured to symbolicate using the obfuscation debug-info files from the build step above, or crash traces will be useless.

## Final pre-submission pass

- Test the actual release build (not debug) on a real device — some issues (obfuscation-related reflection failures, release-only performance characteristics, signing issues) only appear in release mode.
- Check app icon, splash screen, and store screenshots are current and match the actual current UI — stale marketing assets are a common oversight.
- Double-check any feature flags/debug flags default to production-safe values in the release build.
