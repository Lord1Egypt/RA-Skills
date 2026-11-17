# Step 2 — build, install, provision

## 2.1 The JDK (this is the step that stops people)

The build needs **JDK 17–20**.

- AGP 8.3.1 requires 17 or newer.
- **The Gradle 8.4 wrapper cannot run on 21 or newer.** Android Studio's bundled JBR 25 is rejected
  outright with `Unsupported class file major version 69`.

`gradle.properties` intentionally does **not** hardcode `org.gradle.java.home`, because a
machine-specific path in there is exactly what made the first build fail on every other machine.
Point *your* machine at a JDK in one of two ways — neither belongs in the repository:

```bash
export JAVA_HOME=/path/to/jdk-17                                              # 1. environment
printf 'org.gradle.java.home=/path/to/jdk-17\n' >> ~/.gradle/gradle.properties  # 2. user-level
```

Android Studio users: **Settings → Build, Execution, Deployment → Build Tools → Gradle → Gradle
JDK**, pick a 17–20 JDK. (The IDE setting overrides the file.)

## 2.2 The Android SDK

Gradle finds the SDK through `sdk.dir=` in `local.properties`. Android Studio writes that file for
you; it is **not in the repository** (gitignored), so every machine configures it once.

### Path A — Android Studio (recommended)

1. Install [Android Studio](https://developer.android.com/studio). The first launch runs a **Setup
   Wizard** — take the defaults and it downloads the SDK, Platform-Tools (`adb`) and a bundled JDK.
2. **Open the repository root** in Android Studio. It writes `local.properties`, notices which SDK
   pieces are missing, and offers "Install missing SDK" in a blue bar. Accept it.
3. In **SDK Manager** (Tools → SDK Manager), confirm:
   - **SDK Platforms:** Android 14 (API 34 — that is compileSdk/targetSdk); Android 11 (API 30 —
     minSdk, handy if you want an emulator)
   - **SDK Tools:** Android SDK Build-Tools (34.x), Android SDK Platform-Tools (latest), Android SDK
     Command-line Tools (latest)
4. Default SDK path: `~/Library/Android/sdk` on macOS, `%LOCALAPPDATA%\Android\Sdk` on Windows.

> Android Studio's own JDK is often too new (JBR 25). Set the **Gradle JDK** as in §2.1 even if the
> IDE itself runs fine.

### Path B — command line only (server, CI, no Studio)

```bash
# 1. JDK 17 (macOS)
brew install --cask temurin@17

# 2. command-line tools: developer.android.com/studio → "Command line tools only"
#    grab commandlinetools-mac-*.zip, then:
mkdir -p ~/Library/Android/sdk/cmdline-tools
unzip commandlinetools-mac-*.zip -d ~/Library/Android/sdk/cmdline-tools
mv ~/Library/Android/sdk/cmdline-tools/cmdline-tools ~/Library/Android/sdk/cmdline-tools/latest

# 3. put it on PATH (~/.zshrc)
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# 4. install the pieces
sdkmanager --licenses        # answer y to all
sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"
```

### `local.properties`

One line at the **repository root**:

```
sdk.dir=/Users/<your-name>/Library/Android/sdk
```

Linux is usually `/home/<user>/Android/Sdk`; on Windows,
`C\:\\Users\\<user>\\AppData\\Local\\Android\\Sdk` (backslashes escaped). You can also skip the file
entirely and export `ANDROID_HOME` / `ANDROID_SDK_ROOT` — Gradle reads either.

**`local.properties` is gitignored for a reason.** Whatever is in it gets baked into your build, and
it is where credentials land. Never commit it, never paste it into an issue, never hand it to
someone else.

### Optional: bake your own defaults in

`app/build.gradle` reads these keys out of `local.properties` at build time. Leave them out and the
app builds with sensible defaults (an on-device brain, no CodeFlying backend):

| Key | Effect |
|---|---|
| `CODEFLYING_ENABLED` / `CODEFLYING_KEY` / `CODEFLYING_DOMAIN` / `CODEFLYING_SSL_ENABLED` | Makes the hosted CodeFlying backend the out-of-box choice instead of a blank On-device tab |
| `DEFAULT_LANG` | `zh` or `en` — first-install UI language (a choice saved on the device always wins) |
| `DEFAULT_THINKING` | `on` or `off` |

| What | Value |
|---|---|
| Android Gradle Plugin | 8.3.1 |
| Kotlin | 1.9.22 |
| compileSdk / targetSdk | 34 |
| minSdk | 30 (Android 11 — `ACTION_IME_ENTER` and `takeScreenshot` are both API 30+) |
| Java / Kotlin JVM target | 1.8 |
| applicationId / namespace | `net.kuafuai.andee` |

### Verify the toolchain

```bash
./gradlew --version    # expect JVM 17.x and Gradle 8.4
./gradlew tasks        # seeing :app:assembleDebug means you are through
```

## 2.3 Build

```bash
./gradlew clean :app:assembleDebug
```

First run downloads dependencies, so it is slow. **Success looks like `BUILD SUCCESSFUL` plus an APK
that exists — check for the file, do not trust the exit code alone:**

```bash
ls -lh app/build/outputs/apk/debug/
```

The APK is **per-ABI** (`splits` is on, `universalApk false`):

```
app/build/outputs/apk/debug/app-arm64-v8a-debug.apk     ← pick this for any recent phone
app/build/outputs/apk/debug/app-armeabi-v7a-debug.apk
app/build/outputs/apk/debug/app-x86_64-debug.apk        ← only for an emulator
```

**Debug vs release, in one line each:** the debug APK is signed with the standard Android debug
certificate and **installs as-is**; the release build is the minified one and is most of what makes
the APK small, but there is no `signingConfig` and no keystore in the repo, so `assembleRelease`
emits `app-<abi>-release-unsigned.apk`, **which will not install until you sign it**.

> Handing an APK to someone else? The per-ABI split means you must pick the right one — `arm64-v8a`
> for anything bought in the last several years. A debug build is fine for showing something to
> someone; it is just bigger.

## 2.4 Install

```bash
./gradlew installDebug                    # build + install to an attached device
# or, from an APK you already have:
adb install -r app/build/outputs/apk/debug/app-arm64-v8a-debug.apk
```

## 2.5 Provisioning order (do it in this order — it is the shortest path)

Each step has a **verify**. Take the verify seriously; a step that "probably worked" is how people
end up debugging the wrong thing.

**1. Install the APK.** Nothing to verify yet.

**2. Grant Overlay.** Settings → Apps → Andee → Permissions → Display over other apps → on. (Or
Settings → Apps & notifications → Special access → Display over other apps → Andee.) The first
launch usually raises a prompt; tapping through to settings from it is the quickest route.
*Verify:* relaunch the app — **the ball is on screen immediately.**
*If refused:* nothing is visible at all. Overlay is the only genuinely all-or-nothing grant here.

**3. Enable the Accessibility service.** Settings → Accessibility → Downloaded services → **Andee**
→ on. Android then shows the large red warning that the service can view everything you do — confirm
it. Some vendor ROMs (Xiaomi / Huawei / HONOR) additionally want "allow background pop-ups" or "show
on lock screen".
*Verify:* `adb logcat -s Body:*` shows `Body: ws server started on 0.0.0.0:9008`. That line is proof
`onServiceConnected` fired. Then tap `☰` (UI tree) or `◉` (screenshot) on the ball's top bar — the
subtitle line should report success and a filename.
*Expect this to be switched off again* after a system update or a force-stop on most vendor ROMs.
That is ROM behaviour, not a bug.

**4. Tap the ball, allow the microphone.** *Verify:* `listening…`, or live ASR text in the subtitle
line.

**5. Fill in the backend.** Open the ⚙ on the ball.

*If you want the brain on this device (default, no hub needed):* **Backend → On-device** and fill in
an OpenAI-compatible endpoint plus `llm_api_key`. The default base URL is `https://api.deepseek.com`.

*If you want the brain elsewhere:* in **Advanced**, turn on **Show cloud option** (the **Cloud** tab
is hidden by default), go back to **Backend**, flip the picker to **Cloud**, set `hub_url` =
`ws://<your computer's IP>:9100` and `device_name` to anything, and save.

*If the package was built with CodeFlying configured:* ⚙ → **Backend** already shows **CodeFlying** as
the active tab and there is nothing to fill in.

**6. Confirm the link.** logcat should show `hub: registered as body-xxx with N tools`, and the brain
side `[body_hub] 'body-xxx' registered (…) with N tools`.

### The two keys, and how their absence looks

**No credentials ship in this repository**, and both missing ones fail in ways that do not look like
missing credentials.

| Key | Where | Required? | If it is missing |
|---|---|---|---|
| Brain key — `llm_api_key` + `llm_base_url` | ⚙ → Backend → **On-device** | **Yes**, for `brain = local` | The local brain **does not run at all**. Nothing behind it falls back. The ball at least says so out loud |
| Volcengine Speech API key | ⚙ → Backend → **On-device** | No | ASR and TTS fail during the WebSocket handshake — which surfaces as a **connect timeout**, so the device looks like it has a network problem when what it has is a blank field. Everything else still works; it is just mute and deaf |

> On a CodeFlying-packaged APK both are already baked in — ⚙ → Backend will show **CodeFlying** as the
> active tab. The two keys above then only apply to the **On-device** tab you configure yourself.

The app re-checks itself on every start; if either key is missing the card it puts up names what is
missing, and its button opens the settings page where both live. The **✓** button in the ball's
control bar reopens that same list whenever you want it.

## 2.6 One optional adb grant

```bash
adb shell pm grant net.kuafuai.andee android.permission.WRITE_SECURE_SETTINGS
```

Why: some apps (measured on WeChat, on a Xiaomi Pad 5 with MIUI) hand **every** accessibility client
a blank UI tree — the system's own `uiautomator dump` gets the same blank page, so it is not Andee's
fault. When a dump comes back blank, Andee adds the ROM's own helper service (on MIUI,
`MiuiEnhanceTBService`) to the enabled list and dumps again. It never removes anything, it does
nothing on devices without that component, and it tries at most once a minute. Writing that list
needs this one grant.

**Without it nothing breaks.** On blank screens Andee falls back to screenshots and coordinates:
slower and less precise, but the task still gets done.

## 2.7 Traps and their fixes

| Message | Cause | Fix |
|---|---|---|
| `SDK location not found` | no `sdk.dir=` in `local.properties`, and no `ANDROID_HOME` | configure one of the two (§2.2) |
| `Failed to find Build Tools revision 34.0.0` | that build-tools version is not installed | `sdkmanager "build-tools;34.0.0"` |
| `You have not accepted the license agreements` | licences not accepted | `sdkmanager --licenses`, answer y |
| `Unsupported class file major version 69` | JDK too new (25); Gradle 8.4 cannot take it | switch to JDK 17–20 (§2.1) |
| `Could not resolve com.android.tools.build:gradle:8.3.1` | network, or no mirror reachable | try a phone hotspot. `settings.gradle` already puts Aliyun mirrors first; `jitpack.io` (the robot-dog USB serial driver) is deliberately direct and last, because Aliyun answers 401 on it |

**If the build does not work, the answer is almost always the JDK.**

## → Next

`debug-loop.md` — only if the person is actually developing. If they just wanted it running, stop here.
