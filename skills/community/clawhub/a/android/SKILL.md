---
name: Android
slug: android
version: 1.0.3
description: 'Builds, debugs, ships, and hardens Android apps: Gradle, Jetpack Compose, XML Views, ADB, and the Play release path. Use when a Gradle build fails or a dependency resolves to the wrong version, an APK will not install, or `adb` cannot see the device; when the app crashes, ANRs, leaks, or works on the emulator but not on a real phone; when Compose recomposes too much, state resets on rotation, or a list janks; when WorkManager never runs, an alarm is throttled, or a foreground service crashes at start; when a runtime permission is denied silently, scoped storage blocks a file, or Play rejects a declaration; when raising targetSdk changes behavior; when signing, R8 keep rules, bundle size, staged rollout, or Android vitals are the problem; also Room migrations, deep links, emulators, foldables, and CI builds. Not for Kotlin language mechanics (`kotlin`), store-listing ASO (`google-play-store`), or cross-platform frameworks (`flutter`, `react-native`).'
homepage: https://clawic.com/skills/android
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 🤖
    requires:
      anyBins:
      - adb
      - gradle
    os:
    - linux
    - darwin
    - win32
    displayName: Android
    configPaths:
    - ~/Clawic/data/android/
    - ~/Clawic/data/devices/
    - ~/Clawic/data/projects/
    - ~/Clawic/data/contacts/
    - ~/Clawic/profile.yaml
    - ~/android/
    - ~/clawic/android/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/android/
      - ~/Clawic/data/devices/
      - ~/Clawic/data/projects/
      - ~/Clawic/data/contacts/
      - ~/Clawic/profile.yaml
      - ~/android/
      - ~/clawic/android/
---

**Data.** At the start of every session, read `~/Clawic/data/android/config.yaml` (what the user declared) and `~/Clawic/data/android/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/devices/devices.md` before proposing a device test, an emulator image, or a minSdk change. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a release and its rollout; a toolchain version set that finally aligned (AGP, Gradle, JDK, Kotlin, Compose BOM); a build or runtime failure whose cause was not obvious; a test device or emulator profile; a module added or removed; a measured number (cold start, bundle size, crash-free rate, build time); a permission or policy declaration submitted to Play; or something the user will re-read — a keep-rule set, a runbook, an architecture decision, a targetSdk migration plan. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**Test devices and emulators go to the shared inventory `~/Clawic/data/devices/devices.md`**, not here: one file holds every machine the user owns, so "which of my phones is on API 30" answers itself whichever skill wrote the row. The app itself, when the user treats it as a piece of work with a goal and a status, goes to `~/Clawic/data/projects/<project>.md`; a client who owns an app is a row in `~/Clawic/data/contacts/contacts.md` and only a name here. Formats and protocols travel with this skill, in `memory-template.md`.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved, and logcat output, `gradle.properties` and `local.properties` are exactly the pastes that carry one. Store the pointer and strip the value: `keychain:android-upload-key`, `env:PLAY_SERVICE_ACCOUNT_JSON`, `1password:Work/Android/keystore`, `file:~/keystores/upload.jks`. If data sits at an old location (`~/android/` or `~/clawic/android/`), move it to `~/Clawic/data/android/`, and say in one line that you moved it and from where.

Every Android problem belongs to exactly one of four layers: the **build** (Gradle produced the wrong artifact or none), the **install** (the device rejected the artifact), the **runtime** (the app misbehaves on a device), or the **store** (Play rejected, throttled, or flagged it). Name the layer before proposing a fix — the same symptom means different things in each, and the file to open is decided by the layer, not by the feature. Work from defaults immediately: never open with questions about their toolkit, their modules, or how proactive to be. The one exception to silence is `target_sdk` — while it is unset, state which API level you are assuming before generating manifest or Gradle code (Rule 3). That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals) → the Configuration table default.

## When To Use

- Writing or reviewing Android code: Compose or XML screens, ViewModels, Room, WorkManager, Gradle build logic, manifest entries
- Diagnosing an Android failure: build errors, install rejections, crashes, ANRs, leaks, jank, background work that never fires, a permission that returns denied without a dialog
- Shipping: signing, R8, app bundles, versioning, staged rollout, Play policy declarations, CI builds and automated uploads
- Raising `compileSdk`/`targetSdk`, or making the app work on a device generation, an OEM skin, or a form factor it was never tested on
- Hardening: exported components, WebView, backup rules, deep-link verification, what an attacker reads out of the APK
- Not for Kotlin language mechanics (`kotlin`), store-listing copy and ASO (`google-play-store`), or cross-platform toolkits (`flutter`, `react-native`) — this is the Android-platform side of all of them

## Quick Reference

| Situation | Play | Depth |
|-----------|------|-------|
| Build fails with an error string you can quote | Match the string first; most Android build errors are one of a dozen | `build-failures.md` |
| Build is slow, cache never hits, or a dependency resolves to the wrong version | Configuration cache, layer the modules, then `dependencyInsight` on the winner | `gradle.md` |
| Raising `targetSdk` or `compileSdk` | Behavior changes apply the moment targetSdk crosses the level (→ Target SDK Breakage) | `sdk-upgrades.md` |
| `adb` cannot see the device, or install fails | Decode the `INSTALL_FAILED_*` string; it names the cause exactly | `devices.md` |
| Compose recomposes too much, loses state, or a list janks | Deferred reads, stable parameters, `key` on list items | `compose.md` |
| XML layouts, Fragments, RecyclerView, or interop with Compose | ViewBinding, `viewLifecycleOwner`, ListAdapter + DiffUtil | `views.md` |
| State lost on rotation, or after the app sat in the background | Three tiers: recomposition, config change, process death (Rule 4) | `lifecycle.md` |
| "Where does this code go", DI wiring, or a Flow that emits wrong | Layering, Hilt/Koin, `stateIn` + `repeatOnLifecycle` | `architecture.md` |
| Room migration, DataStore, files, or a query on the main thread | Migration test first, then `fallbackToDestructiveMigration` never | `data.md` |
| Background work never runs, is late, or the service crashes at start | Guaranteed-eventually vs user-visible-now vs exact (Rule 6) | `background.md` |
| Permission denied with no dialog, or scoped storage blocks a file | Rationale state machine, then the policy-restricted list | `permissions.md` |
| Requests fail on device but succeed from the terminal | Cleartext policy, then DNS/proxy, then pinning, then timeouts | `networking.md` |
| Reproducing a bug on a device, or instrumenting one | `logcat --pid`, `dumpsys`, StrictMode, forced Doze, deep-link intents | `debug.md` |
| A crash or ANR reported from the field | Deobfuscate, cluster by signature, then match the ANR timeout | `crashes.md` |
| Slow cold start, jank, oversized bundle, or memory growth | Measure with the macrobenchmark before changing anything | `performance.md` |
| Tests flake, or instrumented tests need a device | Animations off, dispatcher injected, orchestrator with `clearPackageData` | `testing.md` |
| Signing, keystore, R8 keep rules, versionCode, building the AAB | Upload key vs app signing key; mapping file per versionCode | `release.md` |
| Play rejection, staged rollout, tracks, declarations, vitals | The declaration forms are the rejection surface, not the code | `play-console.md` |
| Build, sign, or upload from CI | Keystore as a decoded secret, Gradle cache, emulator with KVM | `ci.md` |
| Foldables, tablets, Wear, TV, Auto, or an OEM-only bug | Window size classes, and the OEM battery ladder for background bugs | `devices.md` |
| Exported components, WebView, backup, deep-link hijack, secrets in the APK | Nothing in the APK is a secret (Rule 7); everything else is attack surface | `security.md` |
| Anything else Android | Name the layer — build, install, runtime, store — then reproduce on one device with one variable changed at a time | — |

Coverage map: `build-failures.md` error string→cause · `gradle.md` build system and dependencies · `sdk-upgrades.md` API-level migration · `compose.md` Compose UI and state · `views.md` XML/Fragments/RecyclerView · `lifecycle.md` state survival and navigation · `architecture.md` layering, DI, coroutines · `data.md` Room, DataStore, storage · `background.md` WorkManager, services, alarms · `permissions.md` runtime and policy permissions · `networking.md` HTTP stack and connectivity · `debug.md` on-device diagnosis toolkit · `crashes.md` field crashes, ANRs, vitals · `performance.md` startup, jank, size, memory · `testing.md` unit, instrumented, screenshot · `release.md` signing, R8, bundles · `play-console.md` tracks, rollout, policy · `ci.md` automated build and upload · `devices.md` devices, emulators, form factors · `security.md` hardening and app surface.

## Core Rules

1. **Name the layer before the fix — build, install, runtime, or store.** "It does not work" means four different investigations, and the wrong one costs the session. The artifact tells you where you are: no APK/AAB produced → build; artifact exists but the device refuses it → install; it runs and misbehaves → runtime; it runs fine and Play says no → store.
2. **The toolchain is one pinned set, upgraded one axis at a time.** AGP, Gradle, the JDK, the Kotlin plugin and the Compose BOM move together; a mismatch surfaces as an error about none of them. Floor rule: `AGP >=8` requires JDK 17, `AGP 7.x` required JDK 11 — `Unsupported class file major version` and `Unable to make field private final java.lang.String java.io.File.path accessible` are both this mismatch, not a code bug. Declare every version in `libs.versions.toml`, never inline, and write the aligned set to `## Toolchain` in `memory.md` the moment it builds green (`gradle.md`).
3. **`targetSdk` is a contract you opt into; `minSdk` is a bill you pay.** Raising targetSdk activates every behavior change up to that level at once (→ Target SDK Breakage) — so raise it deliberately, one level per release, with the compatibility toggles used to test each change before flipping. Raising minSdk deletes compatibility code and deletes users: check the current install-base distribution before moving it, and treat anything below API 24 as a desugaring-and-multidex tax. Play's rule is a moving deadline, not a fixed number — new apps and updates must target within about a year of the latest major release, enforced each 31 August (`play-console.md` carries the current level and its verification date). While `target_sdk` is unset, name the level you are assuming before writing manifest or Gradle code.
4. **Every state holder answers two questions: does it survive rotation, and does it survive process death?** Three tiers, and picking the wrong one is the most common Android bug: `remember`/local field survives recomposition only; `ViewModel` survives configuration change but dies with the process; `SavedStateHandle` and `rememberSaveable` survive both — inside a hard size limit, because saved state crosses a Binder transaction capped at ~1 MB *shared per process*, so keep a screen's saved state in the low tens of KB and store the rest by id. Verify with "Don't keep activities" plus `adb shell am kill <pkg>`, never by rotating alone (`lifecycle.md`).
5. **The main thread has a 16.67 ms frame budget at 60 Hz (8.33 ms at 120 Hz) and a 5 s input-ANR ceiling.** Frames dropped ≈ `work_ms ÷ frame_budget_ms`, so a 100 ms main-thread parse on a 60 Hz device drops 6 frames and reads to the user as a stutter; the same work in a loop reads as a freeze and then an ANR. Disk, network, JSON, image decode, crypto and database access are off-thread by default — StrictMode in debug builds is how you find the ones you forgot (`performance.md`).
6. **Background work is a request the system may refuse.** Choose by the promise you need: guaranteed-eventually → WorkManager (periodic work has a hard 15-minute minimum interval and a flex window; the system decides the moment); user-visible-now → a foreground service, which must call `startForeground()` within ~5 s of being started or the system kills it, and which needs a declared type on API 34+; genuinely time-critical → an exact alarm, which is a permission-gated capability Play restricts to alarm-and-calendar apps. Everything else is best-effort and will not run in Doze or a low App Standby bucket (`background.md`).
7. **Nothing shipped in the APK is a secret.** An APK is a zip: `BuildConfig` constants, `strings.xml`, the manifest, resources and native libraries all come out with public tooling in under a minute, and obfuscation renames symbols without hiding string literals. Any value that authenticates lives behind a backend you control, fetched per session; the client holds at most a short-lived token (`security.md`).
8. **R8 is on in release from the very first release.** Enabling minification later turns every reflection assumption into a launch-day crash in a build nobody can reproduce. `minifyEnabled true` plus resource shrinking from v1, keep rules narrowed to what actually reflects (JSON model classes, anything loaded by name), and the `mapping.txt` for every uploaded versionCode preserved — a stack trace without its mapping file is unreadable forever (`release.md`).
9. **A release writes its row before the rollout starts, not after.** versionCode, versionName, track, rollout percentage, the commit or tag, and where the mapping file went, into `releases/<year>.md` (`memory-template.md`); the crash-free and ANR numbers get appended to the same row after ~48 hours of rollout. Play has no downgrade: rolling back means halting the rollout and shipping a *higher* versionCode built from the previous tag, which is only possible if the tag and its toolchain were written down at the time.

## Target SDK Breakage

What activates the moment `targetSdk` reaches the level — regardless of the device's own version. Compile against the newest SDK freely; this table is about the target. Per-level migration procedure, detection commands and compatibility toggles: `sdk-upgrades.md`.

| targetSdk | What starts applying to your app |
|---|---|
| 23 (6.0) | Runtime permissions: dangerous permissions are requested at use, not granted at install; Doze begins |
| 24 (7.0) | `file://` URIs across app boundaries throw `FileUriExposedException` — a `FileProvider` becomes mandatory for sharing |
| 26 (8.0) | Background execution limits, notification channels required, most implicit broadcasts no longer delivered |
| 28 (9.0) | Cleartext HTTP blocked by default; non-SDK interface restrictions begin; foreground services need their permission |
| 29 (10) | Scoped storage (still opt-out-able); background location becomes a separate prompt; starting activities from the background is restricted |
| 30 (11) | Scoped storage enforced; package visibility requires `<queries>`; unused-permission auto-reset |
| 31 (12) | Every `PendingIntent` must declare mutability; every component with an intent filter must declare `android:exported`; exact alarms become permission-gated; splash screen API applies to all launches |
| 33 (13) | `POST_NOTIFICATIONS` becomes a runtime permission — apps that never asked stop being seen; media permissions split by type |
| 34 (14) | Foreground services require a declared type plus its permission; runtime-registered receivers must declare exported or not; exact-alarm eligibility narrows further |
| 35 (15) | Edge-to-edge display is applied by default (your content draws under the bars); long-running `dataSync` foreground services get a per-day time cap; 16 KB-page native builds become the direction of travel |
| 36+ | Recent levels have continued down the same three roads: display insets, background-work limits, and large-screen behavior. Verify the current level's list against the official behavior-changes page before planning the upgrade — this row exists so nobody assumes the table ends where it was last edited |

## Failure Signatures

Decode rule: the string names the layer. A Gradle stack trace is the build; an `INSTALL_FAILED_*` is the device's package manager; a Java exception class is the runtime; a policy code is Play.

| Signature | Most likely cause | First move |
|---|---|---|
| `Duplicate class X found in modules …` | Two dependency paths pull the same library under different coordinates | `dependencyInsight` on the class's group, then exclude or align (`build-failures.md`) |
| `Unsupported class file major version 6x` | Gradle running on a JDK newer than it supports | Match the JDK to AGP (Rule 2), set it in Gradle's JVM, not just in the IDE |
| `Manifest merger failed : Attribute … is also present at …` | Two manifests declare the same attribute differently | Read the merged manifest report, then `tools:replace` only the attribute you own |
| `Android resource linking failed` | A resource, style parent, or attribute that does not exist at this `compileSdk` | The line is in the message — usually a new attribute against an old compileSdk |
| `Cannot fit requested classes in a single dex file` | Over 65,536 methods without multidex | Enable multidex (automatic on `minSdk >= 21`), then shrink with R8 rather than living with it |
| `INSTALL_FAILED_UPDATE_INCOMPATIBLE` | The installed app is signed with a different key | Uninstall first; on a user's device that means the signing identity changed — never ship that |
| `INSTALL_FAILED_TEST_ONLY` | The APK is flagged test-only, as IDE-run debug builds are | Install with `-t`, or build a real debug APK from the assemble task |
| `INSTALL_FAILED_VERSION_DOWNGRADE` | Lower versionCode than what is installed | Uninstall for local work; on Play there is no downgrade at all (Rule 9) |
| `ActivityNotFoundException` on a deep link | No component matches the intent, or the link is not verified | Resolve the intent from the shell, then check App Links verification (`security.md`) |
| `SecurityException: … PendingIntent … must be mutable/immutable` | Missing the mutability flag required from targetSdk 31 | `FLAG_IMMUTABLE` unless the receiver must fill in the intent (`sdk-upgrades.md`) |
| `ForegroundServiceDidNotStartInTimeException` | `startForegroundService()` without `startForeground()` inside the window | Post the notification first thing in `onCreate`, before any work (`background.md`) |
| `NetworkOnMainThreadException` / `IllegalStateException: Cannot access database on the main thread` | I/O on the UI thread (Rule 5) | Move to a background dispatcher; never use the "allow main thread" escape hatches |
| `IllegalStateException: Can not perform this action after onSaveInstanceState` | A fragment transaction after the state was saved | Do the transaction in a lifecycle-aware place; `commitAllowingStateLoss` hides the bug (`views.md`) |
| `ClassNotFoundException` / `NoSuchFieldException` only in release | R8 removed or renamed something reached by reflection | Add the narrowest keep rule and re-test the release build, not the debug one (`release.md`) |
| `TransactionTooLargeException` | More than the ~1 MB Binder budget crossed at once, usually saved state or an intent extra | Pass an id, load the payload on the other side (Rule 4) |
| ANR with `Input dispatching timed out` | The main thread was blocked past 5 s | Read the ANR trace's main-thread stack — the top frame is the block (`crashes.md`) |
| Anything else | Reproduce on one device, change one variable, and match the exact string | `build-failures.md` for build, `debug.md` for runtime |

## Limits That Force Designs

Constraints that have each killed a half-built Android design.

| Limit | Value | What it decides |
|---|---|---|
| Dex methods per file | 65,536 | Multidex is automatic on `minSdk >= 21`; past that the real cost is startup and build time, so shrink dependencies instead of celebrating multidex |
| Binder transaction | ~1 MB, shared across the whole process | Saved state, intent extras and bound-service payloads all draw on it — pass ids, not blobs (Rule 4) |
| Input ANR | 5 s | Every main-thread operation budget derives from this; broadcasts, services and providers have their own shorter or longer ceilings (`crashes.md`) |
| Foreground service start | ~5 s from start to `startForeground()` | Notification construction happens before any initialization work |
| WorkManager periodic work | 15-minute minimum interval | Anything more frequent is either a foreground service or nothing |
| versionCode | Max 2,100,000,000, must strictly increase | Rules out timestamp schemes in milliseconds; a date-plus-counter scheme fits comfortably (`release.md`) |
| Bundle download size | Play caps the compressed download of the delivered app; larger payloads move to asset packs or on-demand delivery | Ship media as an asset pack rather than fighting the cap (`play-console.md`) |
| Notification channel | Immutable after creation, except by the user | Get importance right the first time; changing it means a new channel id and a migration |
| Activity result / permission request | Must be registered before the lifecycle reaches STARTED | Registration happens at field initialization, not inside a click handler (`lifecycle.md`) |

## Defaults That Decide Behavior

Android's defaults are chosen for compatibility, not for your app. Each of these has produced a bug that reads as an application defect.

| Default | Value | Why it bites |
|---|---|---|
| `android:allowBackup` | true | App data leaves the device through backup unless `dataExtractionRules` restrict it (`security.md`) |
| Configuration change | The Activity is destroyed and recreated | Anything held in the Activity is gone; `android:configChanges` suppresses recreation and creates a second, subtler class of bug (`lifecycle.md`) |
| `collectAsState` on a Flow | Keeps collecting while the app is in the background | `collectAsStateWithLifecycle` is the default choice on Android; the plain version burns battery and hits dead views (`architecture.md`) |
| Room queries | Throw on the main thread — unless the escape hatch is enabled | Enabling `allowMainThreadQueries` converts a crash into an ANR (`data.md`) |
| HTTP client timeouts | OkHttp connect/read/write default to 10 s, with **no** overall call timeout | A stalled response can hang a request indefinitely; set `callTimeout` explicitly (`networking.md`) |
| Bitmap config | `ARGB_8888` → 4 bytes per pixel | A 4000×3000 photo is ~48 MB decoded, whatever the JPEG weighed — always decode with a target size (`performance.md`) |
| `WebView` | JavaScript disabled, but file access and mixed content settings are permissive on older targets | Enable exactly what the page needs; a JavaScript interface is a remote-code surface (`security.md`) |
| App Standby bucket | Assigned by usage, invisible to the app | The same code runs on schedule on your desk and hours late on a device the user rarely opens (`background.md`) |
| OEM battery management | Additional, undocumented, and off-spec | Background work verified on a Pixel can be killed outright on several popular skins (`devices.md`) |

## Output Gates

Before emitting a Gradle file, a manifest entry, a screen, or a release command:

- Is the layer named — build, install, runtime, or store — and does the fix act on that layer (Rule 1)?
- Do the versions in this snippet form one valid set (AGP, Gradle, JDK, Kotlin, Compose BOM), and is the assumed `target_sdk` stated when it is unset (Rules 2, 3)?
- Does every new state holder answer "survives rotation?" and "survives process death?" (Rule 4)?
- Is anything on the main thread that touches disk, network, database, image decode, or crypto (Rule 5)?
- Does any new permission, foreground service type, or exported component carry the manifest declaration *and* the Play declaration it will need (`permissions.md`, `play-console.md`)?
- Would this survive R8 — is anything reached by reflection covered by a keep rule (Rule 8)?
- Is any command destructive (`adb uninstall`, `pm clear`, wiping an emulator, `--rm` on a build directory, halting a rollout)? Then it names exactly what dies and ships with a confirmation step, never inside a copy-paste block of read-only commands.
- Did anything durable come out of this — a release, a toolchain set, a device, a measured number, a non-obvious cause, a declaration text, a decision? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/android/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| ui_toolkit | compose \| views \| both | compose | Which UI idiom every generated screen, test and review uses; `both` means interop guidance in `views.md` applies by default |
| min_sdk | number (21-35) | 24 | The compatibility floor of every snippet: desugaring, multidex, and which platform APIs need a fallback branch |
| target_sdk | number (API level) | none | The behavior-change set assumed by generated manifest and Gradle code; while unset, name the assumed level out loud before acting (Rule 3) |
| build_language | kotlin-dsl \| groovy | kotlin-dsl | The dialect of every generated `build.gradle` snippet and version-catalog accessor |
| di_framework | hilt \| koin \| manual \| none | hilt | Wiring style in `architecture.md` examples and in every generated ViewModel or repository |
| module_layout | single \| by-layer \| by-feature | single | Where new code is placed and whether a change is proposed as a module boundary (`gradle.md`, `architecture.md`) |
| ci_platform | github-actions \| gitlab-ci \| bitrise \| circleci \| jenkins \| none | none | Which CI dialect `ci.md` examples are written in and which cache backend is recommended |
| crash_reporting | play-vitals \| crashlytics \| sentry \| none | play-vitals | Where `crashes.md` says to look first and how deobfuscation mapping is expected to arrive |
| distribution_track | internal \| closed \| open \| production | internal | The default track of a release plan and how conservative the staged-rollout ladder is (`play-console.md`) |
| size_budget_mb | number (5-500) | 100 | The bar for calling a bundle large and the trigger for asset packs, ABI review and resource shrinking (`performance.md`) |
| cold_start_budget_ms | number (200-5000) | 1000 | The pass mark for startup work in `performance.md`; Play's own bad-behavior line for a slow cold start sits far higher, so this is a quality target, not a compliance one |
| destructive_confirm | bool | true | Whether `adb uninstall`, `pm clear`, emulator wipes and rollout halts are emitted behind an explicit confirmation step |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — Gradle version catalogs vs direct coordinates, KSP vs kapt, ViewBinding vs Compose interop, image and JSON library picks, macrobenchmark vs manual timing — affects the shape of every example
- **Conventions** — package and module naming, versionCode scheme, branch and tag names for releases, resource naming, string-resource discipline — affects generated files and `release.md`
- **Platform** — form factors that must pass (phone, tablet, foldable, Wear, TV, Auto), device matrix for testing, JDK, arm64 vs x86_64 emulators, distribution outside Play — affects `devices.md` and `testing.md`
- **Safety posture** — whether destructive `adb` commands are emitted at all, rollout ladder aggressiveness, whether a release requires a green pre-launch report — affects Output Gates and `play-console.md`
- **Constraints** — banned libraries, licence rules, offline-first requirements, privacy regimes (families policy, health data, regional data rules) — affects `permissions.md`, `data.md` and the declarations in `play-console.md`
- **Cadence** — dependency and BOM update sweep, targetSdk deadline check, baseline profile regeneration, keystore backup verification, vitals review — every accepted cadence becomes a row in the `## Due` table of `memory.md`
- **Output register** — diff vs whole file, code-first vs explanation-first, how much of the failing log to quote back — affects every answer's shape

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| `multiDexEnabled true` copied into every project | Native from `minSdk >= 21`; on modern projects it changes nothing and hides that the real problem is dependency bloat | Measure the method count, then remove dependencies or let R8 shrink them |
| Testing rotation and calling state handling done | Rotation keeps the process alive; the state bug appears an hour later when the process was killed | "Don't keep activities" plus `am kill`, on the actual navigation path (Rule 4) |
| `commitAllowingStateLoss` to silence a crash | Converts a visible crash into a screen that silently does not appear | Move the transaction to a lifecycle-safe point (`views.md`) |
| Reading `shouldShowRequestPermissionRationale` as "permanently denied" | It returns false *both* before the first request and after permanent denial — the two states are indistinguishable from it alone | Persist "we have asked" yourself and combine the two facts (`permissions.md`) |
| Enabling R8 for the first time at a major release | Every reflection assumption fails at once, in the one build you cannot iterate on | R8 on from v1 (Rule 8); test the release variant on every release |
| `fallbackToDestructiveMigration()` left in a shipped build | Silently wipes user data on any schema change that lacks a migration | Write and test the migration; the destructive fallback belongs to debug builds only (`data.md`) |
| Debugging a background-work bug on a plugged-in Pixel | Charging suppresses most restrictions and Pixels apply none of the OEM extras | Unplug, force the standby bucket and force Doze, then retest on the OEM device that reported it (`background.md`) |
| Storing an API key in `BuildConfig`, `strings.xml`, or the NDK | All three are readable from the APK; the native library only adds a minute of work (Rule 7) | Proxy the call server-side, or use a short-lived token bound to an attested session (`security.md`) |
| Uploading a build without keeping its `mapping.txt` | The stack traces from that build stay unreadable forever | Keep the mapping per versionCode and note where it lives (`release.md`) |
| Chasing a jank report from a debug build | Debug builds are not R8-processed and run unoptimized; the numbers are not the user's numbers | Benchmark the release variant, with a baseline profile, on a mid-range device (`performance.md`) |
| Pinning certificates without a backup pin and an expiry | The day the certificate rotates, every installed app is bricked until an update ships | Backup pins plus an expiry, or no pinning at all (`networking.md`) |
| Suppressing a lint or policy warning to get the release out | Play's declaration forms are checked by humans and by static analysis; the warning is usually the rejection reason arriving early | Fix or declare, and put the declaration text in `artifacts/` so the next submission matches (`play-console.md`) |
| One `app` module forever | Every change rebuilds everything; incremental build time becomes the team's largest cost | Split by feature when clean-build time or a rebuild loop starts hurting (`gradle.md`) |
| Treating an emulator pass as a device pass | Emulators have no OEM skin, no real thermal limits, x86 native paths and unlimited background allowances | Keep one real low-end device in the loop for anything about performance or background (`devices.md`) |

## Where Experts Disagree

- **Compose vs XML for new work.** Compose is the default for new screens and Google's investment; the frontier is a large existing View codebase with heavy custom drawing and a team without Compose experience, where incremental interop beats a rewrite. Mixed codebases are normal, not a failure state (`views.md`).
- **How much architecture a small app needs.** Layer-and-DI-from-day-one pays off when there will be tests, more than one developer, or a second data source; on a solo two-screen app the same structure is ceremony that slows every change. The trigger to add layers is the second consumer of the same data, not the first screen (`architecture.md`).
- **Single-module vs modularized.** Modules buy parallel and incremental builds and enforce boundaries, and cost dependency plumbing and slower clean builds. Split when the clean-build or edit-rebuild cycle is the bottleneck you can measure — the module count is a symptom of build time, not a design goal.
- **Exact alarms and aggressive background work.** One camp treats OEM restrictions as bugs to work around with wakelocks and battery-optimization prompts; the other designs for eventual delivery. The second is the only one that survives policy review and the next Android release — the first is legitimate only for genuine alarm-clock and calendar apps, which is exactly the eligibility Play enforces (`background.md`).
- **Client-side integrity checks.** Root and tamper detection on the client is defeatable by definition, and shipping it costs support tickets from legitimate rooted users. It is defensible as friction for high-value fraud, worthless as a security control, and never a substitute for server-side verification (`security.md`).

## Security & Privacy

**Credentials:** this skill drives local build and device tooling, which reads signing material from the keystore path and Gradle properties the user configured. It does NOT store, log, copy, or transmit keystores, key passwords, service-account files, or API keys, and never writes a credential into `~/Clawic/data/android/`.

**Local storage:** preferences, memory, release history, benchmarks and generated artifacts stay in `~/Clawic/data/android/` on this machine, plus device rows in the shared `~/Clawic/data/devices/`. Package names, version codes, certificate fingerprints, device models and measured numbers only — no secrets.

**Guardrails:** commands are read-only by default. Destructive operations (`adb uninstall`, `pm clear`, emulator wipes, deleting build output, halting or replacing a rollout) name exactly what they destroy and require explicit confirmation when `destructive_confirm` is true.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/android (install if the user confirms):
- `kotlin` — the language itself: coroutines, null safety, collections, Java interop
- `google-play-store` — store listing, ASO keywords, and the marketing side of publishing
- `android-studio` — the IDE itself: profiler navigation, inspectors, refactoring
- `ios` — the other half of a two-platform product
- `ci-cd` — pipeline design around the build and upload steps

## Feedback

- If useful, star it: https://clawic.com/skills/android
- Latest version: https://clawic.com/skills/android

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/android.
