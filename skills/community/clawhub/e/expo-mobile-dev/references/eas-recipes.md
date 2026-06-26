# EAS Build & Submit Recipes

Common workflows for shipping with EAS. Assumes `eas-cli` installed and `eas login` done.

## First-time project setup

```bash
eas build:configure
# Creates eas.json with development/preview/production profiles
# Adds projectId to app.config.ts (or app.json) extra.eas
```

## Standard `eas.json`

```json
{
  "cli": { "version": ">= 13.0.0", "appVersionSource": "remote" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": { "simulator": true },
      "channel": "development"
    },
    "preview": {
      "distribution": "internal",
      "channel": "preview"
    },
    "production": {
      "autoIncrement": true,
      "channel": "production"
    }
  },
  "submit": {
    "production": {
      "ios": { "ascAppId": "1234567890" },
      "android": { "serviceAccountKeyPath": "./google-service-account.json", "track": "internal" }
    }
  }
}
```

Key fields:
- `developmentClient: true` — build includes Expo Dev Client, can connect to local Metro
- `distribution: "internal"` — produces an installable file (.ipa / .apk), not store-ready
- `ios.simulator: true` — produces a build runnable in the iOS simulator (separate from device builds)
- `appVersionSource: "remote"` — EAS manages buildNumber/versionCode for you
- `channel` — pairs the build with `eas update` branches

## Build commands

```bash
# Development build (used with `expo start --dev-client`)
eas build --profile development --platform ios
eas build --profile development --platform android

# Internal QA build for testers
eas build --profile preview --platform all

# Production
eas build --profile production --platform all
```

`--platform all` runs iOS and Android in parallel.

## Environment variables and secrets

Three layers:

1. **Plain env vars** in `eas.json` per profile — visible in version control:
   ```json
   "production": { "env": { "API_URL": "https://api.example.com" } }
   ```
2. **EAS secrets** — encrypted, set via CLI, never committed:
   ```bash
   eas secret:create --scope project --name SENTRY_AUTH_TOKEN --value <token>
   eas secret:list
   ```
3. **`EXPO_PUBLIC_*` env vars** — inlined into the JS bundle at build time. Safe for non-secrets that the client needs.

Rule of thumb: anything sensitive → EAS secret. Anything the client legitimately needs → `EXPO_PUBLIC_*`. Anything that changes per build profile but isn't sensitive → env block in `eas.json`.

## OTA updates with `eas update`

For JS-only changes (no native code, no native deps changed), you can ship instantly without a new binary.

```bash
# One-time per profile: build with the matching channel set in eas.json
eas build --profile production --platform all   # build understands "channel": "production"

# Then ship updates
eas update --branch production --message "fix login button"
```

Builds subscribe to a channel; updates publish to a branch; you link them with `eas channel:edit` if needed. Default is: channel name === branch name.

What works OTA:
- JS code changes
- Asset changes (images, fonts already in `assets/`)
- New screens, new routes

What requires a new build:
- Installing/updating any native module
- Changing `app.config.ts` plugins or permissions
- Bumping Expo SDK
- Editing `eas.json` profile config

## Submit to stores

```bash
# Submit the last finished production build
eas submit --profile production --platform ios
eas submit --profile production --platform android
```

Or pass `--id <build-id>` to submit a specific one.

### iOS submit prerequisites

- Apple Developer account ($99/year)
- App Store Connect app record created (manually, first time)
- `ascAppId` (10-digit number) in `eas.json` submit config
- EAS can auto-handle credentials (recommended) — answer "yes" when first prompted

### Android submit prerequisites

- Google Play Console account ($25 one-time)
- App created in Play Console with first manual submission to internal track
- Service account JSON key downloaded and path set in `eas.json`
- After the first manual submission, EAS submit works for all subsequent uploads

## Build hooks

Run scripts during the EAS build process. Add to `package.json`:

```json
"scripts": {
  "eas-build-pre-install": "echo Running before install",
  "eas-build-post-install": "echo Running after install, before native build",
  "eas-build-on-success": "echo Build succeeded",
  "eas-build-on-error": "echo Build failed"
}
```

Common use: code generation, fetching env-specific config, Sentry sourcemap uploads.

## Credentials

EAS manages signing credentials for you by default. Check what's set:

```bash
eas credentials
```

If migrating from another build system, you can import existing keys via the interactive prompts.

## Common issues

- **"No development build is installed"** when running `expo start --dev-client` — you haven't installed the dev build on your device/simulator yet. Run `eas build --profile development` and install the result.
- **iOS build fails with provisioning error** — let EAS regenerate credentials: `eas credentials` → manage → reset.
- **Android build fails after adding a library** — likely a `compileSdkVersion` or `minSdkVersion` mismatch. Add `expo-build-properties` plugin to pin versions.
- **OTA update doesn't appear in the app** — check `runtimeVersion`. Build's `runtimeVersion` must match the update's. If you've added native code, you need a new build, not an update.
