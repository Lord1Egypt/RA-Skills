# Security

## Secrets

- **Never commit API keys/secrets to the repo**, even "just for dev." Check `pubspec.yaml`, `.env` files, and Dart source for hardcoded keys — this is one of the most common findings in real audits. Use `--dart-define` / `--dart-define-from-file` at build time, or a gitignored `.env` loaded via `flutter_dotenv`, and confirm `.env`/secret files are actually in `.gitignore` (not just present but untracked — check `git status` and `git log` for prior accidental commits too).
- Secrets baked into a Dart app are still extractable from the compiled binary by a motivated attacker (Dart isn't a secure secret vault) — for anything truly sensitive (payment processing keys, admin credentials), the right fix is moving that logic to a backend, not just hiding the key better client-side. Say this plainly if you see business-critical secrets client-side.

## Local storage

- `SharedPreferences` (and its equivalents) is **not encrypted** — fine for non-sensitive UI prefs (theme, onboarding-seen flag), wrong for tokens, PII, or anything sensitive.
- Use `flutter_secure_storage` (backed by Keychain on iOS, Keystore/EncryptedSharedPreferences on Android) for auth tokens, refresh tokens, and sensitive user data.

## Network

- Enforce HTTPS everywhere; flag any hardcoded `http://` endpoint.
- For apps handling sensitive data (banking, health, enterprise), consider certificate pinning (`http` package + custom `HttpClient` config, or a package like `dio` with pinning support) to defend against MITM via compromised CA trust stores. This is a judgment call based on the app's risk profile, not a default requirement for every app.
- Don't log full request/response bodies (especially auth headers, tokens, PII) even in debug builds if that logging could accidentally ship to production or end up in crash reports.

## Permissions

- Request only the permissions actually needed, and request them contextually (at the point of use) rather than all upfront — this is both better UX and reduces the "why does this app want X" red flag that gets apps flagged in store review.
- Check `AndroidManifest.xml` and `Info.plist` for permissions that are declared but no longer used by any code path (common after feature removal).

## Obfuscation

Release builds should be obfuscated to raise the bar against reverse engineering: `flutter build apk --obfuscate --split-debug-info=<dir>` (same flag pattern for `appbundle`/`ios`). Keep the generated debug symbol files (`--split-debug-info` output) somewhere safe and versioned per-release — you need them to symbolicate crash reports later; without them, crash stack traces from obfuscated builds are unreadable.

## Platform-specific

- Android: check `minSdkVersion`/`targetSdkVersion` are reasonably current (Play Store enforces a rolling minimum `targetSdkVersion`); check for `android:allowBackup="true"` left default on an app handling sensitive data (allows the app's data to be extracted via ADB backup on non-rooted devices in some configurations).
- iOS: check App Transport Security exceptions in `Info.plist` aren't blanket-disabling HTTPS enforcement (`NSAllowsArbitraryLoads: true` without justification is a store-review and security flag).

## Dependency hygiene

Run `flutter pub outdated` and separately check for known-vulnerable versions. Old, unmaintained packages (especially ones wrapping native code / platform channels) are a real supply-chain risk, not just a staleness nitpick — flag packages with no updates in 1+ years, especially ones handling networking, auth, or storage.
