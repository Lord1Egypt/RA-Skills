---
name: expo-app-store-screenshots
description: Capture and prepare App Store / Google Play screenshots for any React Native / Expo app. Drives iOS Simulator and Android device/emulator via deep links, locks the status bar to a clean marketing state, captures the standard set of screens per locale, and resizes to store-target dimensions. Use when the user asks to (re)generate or refresh store screenshots, add a new locale, add a new screen, or upload screenshots to App Store Connect or Google Play. Also trigger for adjacent phrasing like "marketing screenshots", "store listing screenshots", "screen capture for the app stores", or when the user mentions `xcrun simctl`, `adb screencap`, or paths like `screenshots/<locale>/<device>/`.
license: MIT
compatibility: Designed for Claude Code and compatible agents. Requires macOS for iOS capture (Xcode CLI / `xcrun simctl`). Android capture needs Android Platform Tools (`adb`) and an attached device or running emulator. Resize step needs ImageMagick 7+ (`magick`). Detection helper uses `jq` and optionally `npx expo` for `app.config.{ts,js}` projects. Upload helpers need Python 3.9+ with `requests`, `pyjwt[crypto]` (App Store Connect) and `google-auth` (Google Play).
metadata:
  author: "北京腾秀创智技术有限公司 (Tenshow Innovation)"
  organization: tenshowinnovation.com
  version: "0.2.0"
---

# App Store / Google Play Screenshots

End-to-end runbook for marketing screenshots that ship to the iOS App Store and Google Play. The skill does **not** hard-code app identity — it discovers the deep-link scheme + iOS bundle ID + Android package from the project's Expo config, and takes everything else as parameters.

## Required tooling

| Platform | Needed                                          |
| -------- | ----------------------------------------------- |
| iOS      | Xcode CLI (`xcrun simctl`)                      |
| Android  | Android Platform Tools (`adb`)                  |
| Resize   | ImageMagick 7+ (`magick`)                       |
| Detect   | `jq` and (optional) `npx expo` for `app.config.{ts,js}` projects |
| Upload   | Python 3.9+ with `requests`, `pyjwt[crypto]` (App Store) and `google-auth` (Play) |

## Output layout (convention)

```text
screenshots/<locale>/<device>/NN-<device>-<screen>.png
```

- `<locale>`: BCP-47 tag — `en-US`, `zh-CN`, `ja-JP`, …
- `<device>`: `iphone`, `ipad`, `android-phone`, `android-tablet`
- `NN`: zero-padded ordinal so files sort the same in Finder and the store back-office
- `<screen>`: kebab-case slug for the page (`sign-in`, `home`, `settings`, …)

## Store target dimensions

| Device          | Required size | Notes                                                                                    |
| --------------- | ------------- | ---------------------------------------------------------------------------------------- |
| `iphone`        | 1284×2778     | App Store 6.5" display. Capture on iPhone 16 Pro Max sim (1320×2868) and resize.         |
| `ipad`          | 2064×2752     | App Store 13" display. iPad Pro 13" M4 captures natively at this size.                   |
| `android-phone` | 1440×3120     | Google Play phone (9:19.5). Pixel 7+/8+/9 Pro class captures natively.                   |

For other targets, look up the current Apple / Google specs and pass the size through to `assets/resize.sh`.

## Scripts (all live under `assets/`)

| Script                                                                                       | Purpose                                                                                                  |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [`assets/detect-app-config.sh`](assets/detect-app-config.sh)                 | Discover `APP_SCHEME`, `IOS_BUNDLE_ID`, `ANDROID_PACKAGE` from the Expo config.                          |
| [`assets/detect-routes.sh`](assets/detect-routes.sh)                         | Walk an Expo Router `app/` (or `src/app/`) tree and print every route as `<url>\t<group>\t<source-file>`. |
| [`assets/ios-status-bar.sh`](assets/ios-status-bar.sh)                       | Lock / clear the iOS Simulator status bar (9:41, charged, full bars).                                    |
| [`assets/ios-capture.sh`](assets/ios-capture.sh)                             | One screenshot: `openurl` → settle → `simctl io screenshot`.                                             |
| [`assets/android-status-bar.sh`](assets/android-status-bar.sh)               | Enter / exit Android system UI demo mode (clean clock, battery, signal).                                 |
| [`assets/android-capture.sh`](assets/android-capture.sh)                     | One screenshot: `am start` deep link → settle → `screencap` + `adb pull`.                                |
| [`assets/resize.sh`](assets/resize.sh)                                       | Batch resize a directory of PNGs to a target `WxH`, idempotent.                                          |
| [`assets/write-summary.sh`](assets/write-summary.sh)                         | Write `summary.md` into a device folder (model, OS, resolution, screen list).                            |
| [`assets/upload-app-store.py`](assets/upload-app-store.py)                   | Upload one (locale, device) folder to App Store Connect via the API.                                     |
| [`assets/upload-play-store.py`](assets/upload-play-store.py)                 | Upload one (locale, image-type) folder to Google Play via the Publisher API.                             |

Each script accepts `-h`-style usage on bad input. Read the file headers for full arg lists.

## How to drive the skill

Capture runs in **three phases**: phase 1 takes the unauth screens (`sign-in`, `sign-up`, etc.) while the demo account is signed *out*, then you manually sign in across all devices, then phase 2 takes the auth-required screens. This avoids round-tripping through the sign-in flow during automation and keeps both states clean.

Script paths in the bash blocks below are written relative to the skill root (`assets/...`). Resolve them to wherever your agent installed the skill before running.

1. **Pre-flight**
   - Build & install the app on the target sim/device (a release-style build looks best).
   - **Verify the installed build is up to date.** A stale dev client or a cached `.app`/`.apk` from weeks ago will either crash on missing native modules (`NativeModule.X is null`) or — worse — quietly render an *old UI*, and you won't notice until the screenshots ship. Cold-launch the app and visually confirm it matches today's source before capturing. If it doesn't, rebuild and reinstall (for Expo: `pnpm --filter <app> prebuild --clean && pnpm --filter <app> ios && pnpm --filter <app> android`, or whatever your pipeline is).
   - **Start in a signed-out state on every device.** If the demo account is already signed in, sign out first — phase 1 needs the unauth screens.
   - **Have demo account credentials ready.** You'll be asked to sign in manually between phase 1 and phase 2.
   - Set the in-app language to match the `<locale>` you're capturing (or rely on system locale if the app inherits it).
   - **If the simulator can't run the app, fall back to a real device.** Apps that depend on native modules Expo Go doesn't ship (BLE, custom Stripe SDK, push, certain camera/payments pipelines) often won't run in Expo Go and may not run on a freshly built sim either. Plan:
     - **Android** — `adb` targets emulators and physical phones identically; every script here works against a plugged-in Pixel/Galaxy/etc. just by running `adb devices` first. If multiple devices are attached, pass `-s <serial>` to the capture/status-bar scripts.
     - **iOS** — `xcrun simctl` is simulator-only. For a real iPhone, the path is Xcode-driven (`xcrun devicectl device install`, Xcode for deep-link launch, `xcrun devicectl device screenshot` on Xcode 16+) and not wired into these scripts. Prefer rebuilding the dev client or installing a release `.app` to the simulator instead.

2. **Discover app identity**
   ```bash
   eval "$(bash assets/detect-app-config.sh path/to/app)"
   echo "$APP_SCHEME $ANDROID_PACKAGE"
   ```
   If detection fails (custom config plugin, monorepo quirks), set the three env vars by hand.

3. **Split screens by auth state.** Two bash arrays of `NN slug deep-path` rows. The `NN` ordering keeps both arrays disjoint so filenames sort correctly together.

   > **For Expo Router projects only**: rather than guessing deep-link paths from memory, dump every route under `app/` (or `src/app/`) first so you don't miss anything the team added since the last screenshot pass:
   > ```bash
   > bash assets/detect-routes.sh path/to/app
   > # TSV: <url-path>\t<group>\t<source-file>
   > ```
   > Expo Router collapses `(group)` segments out of the user-visible URL — `app/(auth)/sign-in.tsx` deep-links as `/sign-in`. The `(group)` column is a useful auth-state hint (`(auth)`, `(app)`, `(tabs)` usually gate; `(public)`, `(onboarding)` usually don't), but confirm against the matching `_layout.tsx` where redirect logic actually lives. For non-Expo-Router apps, read the project's own router config.

   ```bash
   UNAUTH_SCREENS=(
     "01 sign-in  /sign-in"
     "02 sign-up  /sign-up"
   )

   AUTH_SCREENS=(
     "03 home          /"
     "04 agent-plaza   /agent"
     "05 profile       /user"
     "06 settings      /settings"
     "07 agent-create  /agent/create"
     "08 product       /product"
   )
   ```

4. **Set up — lock status bars on all devices once.** Persists across app launches and across both phases.
   ```bash
   LOCALE=en-US
   IPHONE_UDID=<...>; IPAD_UDID=<...>   # `xcrun simctl list devices` to find them

   bash assets/ios-status-bar.sh     "$IPHONE_UDID"
   bash assets/ios-status-bar.sh     "$IPAD_UDID"
   bash assets/android-status-bar.sh enter

   capture_set() {
     local udid="$1" device="$2" platform="$3"; shift 3
     for row in "$@"; do
       read -r nn slug path <<<"$row"
       local out="screenshots/$LOCALE/$device/$nn-$device-$slug.png"
       if [[ "$platform" == ios ]]; then
         bash assets/ios-capture.sh     "$udid" "$APP_SCHEME://$path" "$out"
       else
         bash assets/android-capture.sh "$APP_SCHEME://$path" "$out" "$ANDROID_PACKAGE"
       fi
     done
   }
   ```

5. **Phase 1 — capture unauth screens.** App must be signed *out* on every device.
   ```bash
   capture_set "$IPHONE_UDID" iphone        ios     "${UNAUTH_SCREENS[@]}"
   capture_set "$IPAD_UDID"   ipad          ios     "${UNAUTH_SCREENS[@]}"
   capture_set ""             android-phone android "${UNAUTH_SCREENS[@]}"
   ```

6. **Manual sign-in.** Open the simulator/emulator windows, complete the sign-in flow with the demo account on **iPhone, iPad, and Android**. Confirm you land on the post-sign-in home page on all three before continuing. (Status bar stays locked — no need to re-run step 4.)

7. **Phase 2 — capture auth screens.**
   ```bash
   capture_set "$IPHONE_UDID" iphone        ios     "${AUTH_SCREENS[@]}"
   capture_set "$IPAD_UDID"   ipad          ios     "${AUTH_SCREENS[@]}"
   capture_set ""             android-phone android "${AUTH_SCREENS[@]}"
   ```

8. **Resize & verify.** iPad is already 2064×2752 native, no resize needed.
   ```bash
   bash assets/resize.sh "screenshots/$LOCALE/iphone"        1284x2778
   bash assets/resize.sh "screenshots/$LOCALE/android-phone" 1440x3120

   identify "screenshots/$LOCALE/iphone"/*.png        # expect 1284x2778
   identify "screenshots/$LOCALE/ipad"/*.png          # expect 2064x2752
   identify "screenshots/$LOCALE/android-phone"/*.png # expect 1440x3120

   bash assets/android-status-bar.sh exit         # release demo mode
   ```

9. **Per-device summary.** Drop a `summary.md` into each device folder so reviewers and future-you can tell at a glance which hardware/OS produced these and which screen each PNG corresponds to. Run after step 8 so the recorded resolution reflects the resized output.
   ```bash
   ALL_SCREENS=( "${UNAUTH_SCREENS[@]}" "${AUTH_SCREENS[@]}" )
   bash assets/write-summary.sh ios     "$IPHONE_UDID" "screenshots/$LOCALE/iphone"        "$LOCALE" "${ALL_SCREENS[@]}"
   bash assets/write-summary.sh ios     "$IPAD_UDID"   "screenshots/$LOCALE/ipad"          "$LOCALE" "${ALL_SCREENS[@]}"
   bash assets/write-summary.sh android -              "screenshots/$LOCALE/android-phone" "$LOCALE" "${ALL_SCREENS[@]}"
   ```
   The script auto-detects model + OS from `simctl`/`adb` and reads the resolution off any PNG already in the folder. Pass `-` for the Android target when only one device/emulator is attached, otherwise pass the serial.

## Uploading to the stores

Both upload scripts upload one (locale, device-or-image-type) directory per invocation. Re-running replaces the contents of that slot — pass `--keep-existing` to append instead. Loop in shell to cover multiple locales/devices.

### App Store Connect — `upload-app-store.py`

Pre-reqs:
- Generate an App Store Connect API key (App Store Connect → Users and Access → Integrations → App Store Connect API). Save the `.p8`, the Key ID, and the Issuer ID.
- The target app must have an *editable* iOS appStoreVersion (PREPARE_FOR_SUBMISSION, METADATA_REJECTED, etc.). The script refuses to touch READY_FOR_SALE or in-review versions.
- App Store Connect locale codes differ from the BCP-47 tags used in the screenshots tree — most notably `zh-CN → zh-Hans`, `zh-TW → zh-Hant`. Map before invoking.

```bash
pip install 'pyjwt[crypto]' requests

export ASC_KEY_ID=ABC1234567
export ASC_ISSUER_ID=11111111-2222-3333-4444-555555555555
export ASC_KEY_PATH=$HOME/.appstoreconnect/AuthKey_ABC1234567.p8

UPLOAD=assets/upload-app-store.py
APP_ID=1234567890

# en-US (BCP-47 == ASC code), iPhone + iPad
python3 "$UPLOAD" --app-id "$APP_ID" --locale en-US   --device iphone --dir screenshots/en-US/iphone
python3 "$UPLOAD" --app-id "$APP_ID" --locale en-US   --device ipad   --dir screenshots/en-US/ipad

# zh-CN folder → zh-Hans on App Store Connect
python3 "$UPLOAD" --app-id "$APP_ID" --locale zh-Hans --device iphone --dir screenshots/zh-CN/iphone
python3 "$UPLOAD" --app-id "$APP_ID" --locale zh-Hans --device ipad   --dir screenshots/zh-CN/ipad
```

Default device → display-type mapping (override with `--device iphone-65|iphone-67|iphone-69|ipad-129`):
- `iphone` → `APP_IPHONE_67` (1284×2778 / 1290×2796)
- `ipad`   → `APP_IPAD_PRO_3GEN_129` (2064×2752 / 2048×2732)

### Google Play — `upload-play-store.py`

Pre-reqs:
- Enable the "Google Play Android Developer API" in Google Cloud, create a service account, download its JSON key.
- Play Console → Setup → API access → link the project, then grant the service account "Manage store presence" on the target app.
- The locale must already exist on the listing (Play Console → Main store listing → Manage translations) before this script can target it.

```bash
pip install google-auth requests

export PLAY_CREDENTIALS=$HOME/.gcloud/play-service-account.json

UPLOAD=assets/upload-play-store.py
PKG=$ANDROID_PACKAGE   # e.g. com.example.myapp (use detect-app-config.sh to populate)

python3 "$UPLOAD" --package "$PKG" --locale en-US --image-type phoneScreenshots --dir screenshots/en-US/android-phone
python3 "$UPLOAD" --package "$PKG" --locale zh-CN --image-type phoneScreenshots --dir screenshots/zh-CN/android-phone
```

Image-type values: `phoneScreenshots`, `sevenInchScreenshots`, `tenInchScreenshots`, `tvScreenshots`, `wearScreenshots`. Each slot caps at 8 images on Play; the script does not enforce that — the commit step will fail if you exceed it.

The script opens an edit, replaces the (locale, image-type) slot, then commits. If the commit fails, the edit is abandoned automatically by Play after a short TTL — re-run.

## Notes & gotchas

- **Deep link form**: `xcrun simctl openurl` and `adb shell am start ... -d` both want a full URL. With Expo Router, paths nest under the scheme as `<scheme>:///<path>` (note the triple slash — empty host).
- **Multiple Android devices attached**: forward `-s <serial>` to `android-status-bar.sh` and `android-capture.sh`; both pass remaining args through to `adb`.
- **`adb exec-out screencap -p > file`** corrupts bytes on shells that translate CRLF. The capture script uses `screencap` to a remote path then `adb pull`, which is byte-safe.
- **`simctl status_bar booted`** targets whichever simulator is currently booted — convenient when only one sim is running.
- **Idempotency**: `resize.sh` skips files already at the target size, so re-running is cheap.

## Adding a new locale

1. Switch the in-app language (Settings → Language) or restart the sim/emulator with that locale.
2. Pre-create the directory: `mkdir -p screenshots/<new>/{iphone,ipad,android-phone}`.
3. Re-run the loops with `LOCALE=<new>`.
4. Sanity-check one screenshot per device before the full sweep.

## Adding a new screen

1. Add an Expo Router path (or whatever your app's deep-link router uses) that renders the new screen cleanly under a deep link.
2. Append `"NN slug /path"` to the `SCREENS` array.
3. Re-run all device loops × all locales.
