# Process and parity (X1–X9)

Use this reference to choose test profiles and evidence. Platform behaviour
belongs in [layout](layout.md), [display](display.md), [input](input.md),
[lifecycle](lifecycle.md), [permissions](permissions.md),
[media and devices](media-devices.md), and [desktop](desktop.md).
Version-sensitive claims below were checked against the linked official
sources on 2026-10-22; recheck them when SDKs or release requirements change.

## X1 Device matrix — P0

**Rule.** Exercise a change on every relevant shipped platform and profile.
Record device / emulator, OS build, app build / revision, build SDK and
Android `minSdk` / `targetSdk`, window size in logical units, pixel ratio,
display / text settings, and distribution channel. The installed Android
API level is independent of `targetSdk`; cover the oldest supported OS,
current stable OS, and boundaries of affected APIs. Label preview runs
separately. Android distinguishes [changes for all apps from target-gated
changes](https://developer.android.com/guide/app-compatibility/test-debug).

Minimum applicable profiles; one device can cover several rows:

| Profile | Failure it catches |
|---|---|
| Smallest supported phone in portrait; additional narrow stress widths such as 320 / 375 pt or dp | Unreachable actions; these sample widths are not OS minimums |
| Cutout / notched phone, both landscape directions and portrait; a non-cutout profile | Asymmetric insets and assumptions that every phone has a bottom safe-area inset |
| Android phone, gesture navigation and 3-button navigation, with / without a cutout | System bars or back handling covering / bypassing controls; inspect actual side and bottom insets |
| Phone with soft keyboard open in portrait and landscape | Short usable height, hidden validation and submit buttons |
| iPad full screen and resizable windows on supported OS modes; legacy Split View / Stage Manager where available | A fixed set of pane ratios misses freely resized windows and breakpoint transitions |
| Android tablet and foldable: folded, unfolded, available tabletop / book postures, multi-window / desktop windowing where supported | Stale sizes, hinge occlusion, assumed portrait locks and activity recreation |
| Each desktop OS at its minimum supported window, maximised and full screen; 100 %, fractional and high scale where offered | Layout / physical-pixel confusion, clipped native chrome and oversized minimums |
| macOS window on Retina and non-Retina displays where supported; Windows at e.g. 125 % / 150 % / 175 % and 200 %; mixed-scale monitor transitions | Blurry assets, misplaced popup anchors and pointer coordinates after scale changes |
| Linux sessions and packaging actually supported: Wayland / X11 or XWayland as applicable, relevant compositor and scale | One display backend passing does not verify another or its portal integration |
| Tablet / touch-capable desktop with keyboard and pointer; keyboard-only desktop | Touch-only navigation, hover-only actions, wrong shortcuts and lost focus |
| A lower-memory physical device within the support policy; constrained storage | Memory pressure, interrupted persistence and storage errors; RAM alone does not prove process-death handling |
| Optional camera, microphone, location or biometric hardware absent / disabled; external devices disconnected | Permission granted being mistaken for hardware availability |

**Additional surfaces — applicable when the app can reach them.** Store
availability decides applicability, not the build list: record each
surface as tested, deliberately excluded (with the setting or declaration
that excludes it), or `to do`. A surface left at its default availability
is shipped. Behaviour rules live in L3, M7 and W4; this table only adds
profiles.

| Surface | Why it can be reached | Profile and failure it catches |
|---|---|---|
| Android phone / foldable on a connected display; tablet desktop session across two displays | [Connected displays](https://developer.android.com/blog/posts/android-devices-extend-seamlessly-to-connected-displays) reached general availability in Android 16 QPR3 on supported devices | Move an active editor and popup between displays of different density, resize / maximise, unplug. Catches density / display data read from the application context and state lost when the activity is [moved back and recreated](https://developer.android.com/develop/adaptive-apps/guides/support-connected-displays) (L3) |
| Android app on ChromeOS | Play on Chromebooks; apps not requiring `android.hardware.touchscreen` can run there | Keyboard / mouse only, free resizing, minimise and restore. ChromeOS runs Android in a container: [inbound connections are generally blocked and multicast is not forwarded, except mDNS](https://developer.android.com/develop/devices/chromeos/learn) — test local discovery separately (X8, M7) |
| Android TV | Only if the app ships TV manifest entries | Five-way D-pad navigation, Back to the TV home screen, launcher banner, no required touchscreen; see [TV app quality](https://developer.android.com/docs/quality-guidelines/tv-app-quality) (M7) |
| Android XR headset | [Compatible mobile apps are automatically opted in on Play](https://developer.android.com/docs/quality-guidelines/android-xr) unless unsupported feature requirements make them uninstallable | Core flows with the headset's indirect input; missing telephony / sensors produce a fallback, not a dead control (M7) |
| iPhone / iPad app on Apple silicon Mac ("Designed for iPad") | [Available on the Mac App Store by default](https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/manage-availability-of-iphone-and-ipad-apps-on-macs-with-apple-silicon/) unless opted out; releasing a macOS platform for the same app record later replaces it and updates existing users | Pointer / keyboard and Touch Alternatives, file access, absent iOS hardware, window resizing; data continuity when a native macOS build replaces it ([iOS apps on Mac](https://developer.apple.com/documentation/apple-silicon/running-your-ios-apps-in-macos); W4) |
| Mac Catalyst build | Only when a Catalyst target ships; it is a separate build, not the "Designed for iPad" runtime. Flutter's [supported platforms](https://docs.flutter.dev/reference/supported-platforms) list neither Catalyst nor visionOS, so check every plugin | The desktop and macOS profiles in the main table, plus plugin availability (W4) |
| Compatible iPhone / iPad app on visionOS | [Offered automatically once the updated developer agreement is accepted](https://developer.apple.com/documentation/visionos/making-your-app-compatible-with-visionos), unless availability is turned off. Core Motion and most location services are unavailable; camera capture is limited to Apple's documented exceptions (persona photo, Continuity Camera) | Run the "Designed for iPad" destination in Simulator for core flows; verify supported capture paths and other device-only features on hardware, marking them **needs device** until then (X4, M7) |
| Web build, **only if one ships** | A hosted web release is its own target | Each declared browser and compile target / renderer; Flutter's supported-platforms page lists browser versions per release. Framework specifics are in [framework notes](flutter.md); release checks are in X6 and X8 |

Apply largest text settings, increased display size / zoom where supported,
RTL and the longest shipped strings, light / dark, screen reader and
reduced motion. Combine high-risk settings, such as large text + narrow
landscape + keyboard, rather than changing each setting only in isolation.
See [display](display.md) and [input](input.md) for the acceptance rules.

**Version traps.**

- On Android 16, apps targeting API 36 have orientation, aspect-ratio and
  resizability restrictions ignored by default on displays with smallest
  width ≥ 600 dp, subject to documented exceptions and a temporary opt-out.
  API 37 targeting removes that developer opt-out on Android 17 large
  screens, subject to documented game and user-setting exceptions. Test
  below, at and above 600 dp as well as app breakpoints; Android's current
  documentation is inconsistent about inclusivity at exactly 600 dp for
  API 37. Do not assume an activity's current pane width determines whether
  the rule applies. Official sources:
  [Android 16](https://developer.android.com/about/versions/16/behavior-changes-16)
  and [Android 17](https://developer.android.com/about/versions/17/changes/ff-restrictions-ignored).
- iPadOS 26 introduced expanded windowing and deprecated
  `UIRequiresFullScreen`. With the iOS / iPadOS 27 SDK, that key no longer
  opts an app out of resizing on iOS / iPadOS 27; it can instead select
  discrete scene resizing. Test the shipped SDK / OS combination rather
  than treating the key as a permanent full-screen guarantee. See
  [Apple TN3192](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key).
- A synthetic 320-wide viewport does not establish support for an old
  phone's OS, and a logical 800-wide window at 200 % is not a 1600-wide
  layout. Record logical and captured pixel dimensions separately.

**Verify.** Publish the selected matrix with results and explicit gaps.
If a profile is unavailable, record `to do` or `needs device` with an owner
and test plan; another OS's screenshot cannot close that gap.

## X2 Automated layout sweep — P0 for UI-heavy apps

**Rule.** Render every affected screen **and overlay** (dialogs, sheets,
menus, dropdowns, snackbars, loading / error / empty states, validation and
results) across:

- logical window sizes from X1, including minimum height and widths just
  below / at / above each app breakpoint;
- default, intermediate and maximum platform text settings. Numeric
  multipliers such as 1.0 / 1.3 / 2.0 are supplemental stress cases, not a
  substitute for Android 14+ [non-linear scaling up to
  200 %](https://developer.android.com/about/versions/14/features#non-linear-font-scaling)
  or iOS [Dynamic Type accessibility
  categories](https://developer.apple.com/documentation/swiftui/dynamictypesize);
- every shipped locale, including plural / formatted values, long user
  content, RTL and mixed-direction text;
- safe-area profiles: notch portrait / landscape, gesture / button
  navigation, tablet taskbar / caption bar, keyboard open / closed, and
  desktop native chrome. Zero mobile safe-area insets do not mean a custom
  title bar has no occlusion;
- supported pixel ratios, including fractional ones, independently of
  logical window size; both themes and relevant accessibility settings;
- live size and setting changes without rebuilding the app from scratch.

**Trap.** A golden image can faithfully capture a broken layout. A 2×
linear text multiplier does not reproduce a non-linear scaler, and mocked
insets do not verify the OS's actual delivery of them.

Detectors that fail the test:

- framework overflow errors;
- essential text ellipsised, line-limited, silently clipped or faded; allow
  intentional truncation only with a documented way to obtain the content;
- laid-out text / line bounds outside their available box, labels outside
  buttons, or app-bar titles outside the toolbar;
- controls obscured by system UI, a keyboard, or an overlay at the end of a
  scroll; scroll to and activate the last action;
- text reduced below the project's documented minimum in logical units,
  or scaling disabled to hide overflow; there is no universal 12 physical
  pixel accessibility floor;
- focus order / hit bounds that no longer match the visible controls;
- lost state, duplicate requests or recreated sessions after relayout.

**Verify.**

- Load the app's actual fonts and required script / emoji fallbacks before
  capture; check for missing glyphs. Placeholder test fonts hide shaping
  and wrapping defects. In Flutter, explicitly load fonts for goldens;
  the rendering notes describe the default test font's [replacement by
  FlutterTest](https://docs.flutter.dev/release/breaking-changes/rendering-changes).
  Do not assume a test runner has the production font fallback chain.
- Pin framework / renderer and fonts, and record the host OS for goldens;
  keep baselines per renderer where necessary. Review visual diffs and do
  not let CI update its expected images automatically. See Flutter's
  [golden matcher](https://api.flutter.dev/flutter/flutter_test/matchesGoldenFile.html).
- Run intentionally broken fixtures to prove each detector fires. Include
  a silent clip, missing font and obscured final button, not just an obvious
  framework overflow.
- Use semantics and interaction assertions alongside screenshots; exercise
  native pickers / platform views and actual screen readers on the app.
  Widget-only rendering cannot establish those integrations.
- Assert that required destinations actually build and display their expected
  state. A tap, visited-control count or zero overflow records does not prove
  the destination rendered. Capture build / async / platform-host errors and
  visible error placeholders too: fail the affected case or explicitly leave
  it unverified, rather than counting it as a layout pass. Prove this gate
  with a broken destination and a non-layout failure. Test-host substitutes
  must implement the exercised contracts, restore global state and retain
  lifecycle assertions; they do not qualify real camera, picker or audio UI.
- Keep a representative sweep in PR CI and the larger matrix on a scheduled
  run; record any combinations omitted. See [framework notes](flutter.md)
  for framework-specific test APIs.

## X3 Rotation / resize test — P1

**Rule.** At least one integration test runs the app on every affected
mobile platform and changes orientation through the OS, where supported;
also resize tablet and desktop windows across a breakpoint in both
directions. Changing a mock viewport alone does not cover native lifecycle
or window events. If the OS refuses rotation, verify that result and test
the available resize path instead.

**Trap.** A screenshot before and after a full relaunch misses state loss,
duplicated network work and stale popup anchors during a live transition.

**Verify.** Start with a selected tab / item, draft with selection, scroll
position, keyboard and an open dialog or media session. Rotate both ways,
resize rapidly through the breakpoint and return. Assert the logical edit
state and selected content survive; editing can resume if the OS dismisses
the keyboard. Check overlay placement, scroll reachability, session
continuity and that callbacks / submissions occur once. Repeat relevant
transitions while a permission prompt or picker is open (X7).

Move desktop windows and open popups between different-scale monitors;
change scale while running, then disconnect / reconnect a display. Check
sharpness, hit testing and dialog coordinates, not just outer window size.
Exercise supported docking / remote-session paths. Microsoft lists these
as distinct [DPI-change
scenarios](https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows).
See D4 in [display](display.md) and [window management](desktop.md) for
expected behaviour.

## X4 Label what needs a real device — P0

**Rule.** Separate a simulated code path from hardware, OS integration and
distribution-channel evidence. Record what the test environment actually
supports instead of treating every simulator or emulator as identical.

Hardware checks include:

- headset / Bluetooth routing, acoustic output, proximity sensing and the
  device's available silent / ringer controls;
- physical camera orientation, mirroring, autofocus, capture quality and
  supported multitasking camera features;
- actual cellular / Wi-Fi handover, carrier behaviour and external devices;
- real memory pressure, thermal throttling and vendor battery policies;
- genuine multi-monitor / docking behaviour on desktop, beyond injected
  scale factors or virtual screens in headless CI.

**Traps: simulation can cover part of the flow.**

| Test | What it establishes and what remains |
|---|---|
| iOS Simulator push injection | Payload parsing / UI routing, not server-to-APNs delivery |
| Sandbox APNs on supported Simulator / Mac configurations | Supported configurations can register and receive remote notifications; record host / runtime. Still test the chosen release channel and physical-device presentation / background behaviour |
| Emulator camera / location / sensor input | Injected-state handling, not physical sensor quality or device routing |
| Android forced Doze or simulated low memory | Specific forced behaviour, not vendor battery policy or natural timing |
| Controlled IPv6-only / DNS64-NAT64 network or captive portal | Real transport / recovery behaviour if the app actually uses that network; these are network-environment tests, not inherently hardware-only |

Apple documents [Simulator sandbox APNs support in Xcode 14 release
notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-14-release-notes);
payload injection and remote delivery are different tests. For networking,
use X8 rather than inferring coverage from the simulator's network icon.
Apple also distinguishes [simulated-device behaviour from physical-device
verification](https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices).

**Verify.** Mark remaining hardware cases **needs device**, with an owner,
device, steps and expected result. A passing simulator test may close its
specific case; it cannot close the remaining device cases. "Implemented"
does not mean "verified".

## X5 Parity — P0

**Rule.** Shared-code changes can affect every caller; verify the platforms
and features they reach. For platform-specific fixes, reproduce the
equivalent scenario on other shipped platforms, then fix or record why it
does not apply. A shared patch alone does not prove identical behaviour.

**Trap.** Marking a feature "implemented" on all platforms hides a release
whose Windows permission denial and Android cold start were never tested.

**Verify.** Keep a feature × platform table with support status
(`implemented` / `partial` / `missing`) separate from verification status
(`verified` / `to do` / `needs device` / `not applicable` with reason).
Link the regression scenario, build and evidence. Split rows when one ID
has mixed results; do not convert an untested platform into `not applicable`.

## X6 Packaged release verification — P0 for release

**Rule.** Inspect and install artifacts from the actual release pipeline,
including every shipped architecture and relevant package / sandbox model.
Source declarations and a debug launch do not establish release behaviour.
Use [permissions](permissions.md) for the required declarations and
[packaging](desktop.md) for distribution rules.

**Traps and verification.**

| Artifact / environment | Check and failure prevented |
|---|---|
| Native payload architecture | Inventory the final app, engine and loaded plugin / FFI binaries against the declared target ABI: PE `Machine` (`dumpbin /headers`), Mach-O slices (`lipo -archs` on each executable), ELF class / machine / ABI flags (`readelf -h -A`). Every in-process module needs a compatible target ABI / slice; document intentional universal / hybrid binaries and out-of-process helpers separately. Package labels and CI job names are not binary evidence. Sources: [PE headers](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format#machine-types), [Mach-O inspection](https://developer.apple.com/documentation/apple-silicon/building-a-universal-macos-binary), [ELF inspection](https://sourceware.org/binutils/docs/binutils/readelf.html). |
| Android release APKs generated from the shipped bundle | Inspect final permissions, SDK levels, components and hardware requirements; run release shrinking / obfuscation and invoke plugins / native libraries. The [manifest merger](https://developer.android.com/build/manage-manifests) includes variants and dependencies, so the main source manifest is insufficient |
| Android device availability | Check Play device filtering as well as sideload installation. Optional hardware permissions can imply required features; inspect camera and autofocus separately, then test without the hardware. See [`uses-feature`](https://developer.android.com/guide/topics/manifest/uses-feature-element) |
| Android native libraries, including framework / SDK binaries | Check packaged ELF and ZIP alignment and run on a 16 KB page-size system with compatibility fallback disabled where available; a passing 4 KB emulator is insufficient. Follow the current [16 KB testing procedure](https://developer.android.com/guide/practices/page-sizes) and record the measured page size |
| Apple exported app and embedded extensions / frameworks | Inspect built usage strings and localisations, privacy manifests, deployment minima and signed entitlements / provisioning where applicable. Install the distribution build and invoke protected features; debug signing can hide release access failures |
| Windows shipped package or unpackaged installer | Verify the actual manifest / identity and capabilities where used, then exercise system privacy settings. [Capability requirements depend on the app model](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/app-capability-declarations); an unpackaged build does not validate an MSIX build |
| Linux shipped package and supported desktop session | Install on a clean supported system; exercise file / device portals with the shipped sandbox permissions. Developer-machine libraries and permission overrides can hide failures. See [Flatpak sandbox and portal guidance](https://docs.flatpak.org/en/latest/sandbox-permissions.html) when applicable |
| Hosted web release, **only if one ships** | Test the deployed site on the real host, not a local dev server: open nested URLs directly and reload them, use Back / Forward, and deploy a new version while an old tab stays open. Catches 404s on deep links, and a cached entry file loading assets from a different deploy. See [framework notes](flutter.md) |

**Native CI gates.** Analysis and unit tests in shared code do not compile
native plugins, link libraries or exercise deployment minima. For changes
to shared code, plugins, native code or dependencies:

- Require a release-mode build of every shipped target on the host its
  toolchain needs (for example macOS with Xcode for Apple targets) and
  publish the artifacts that X6 inspects.
- Run the documented packaging entry point from a clean checkout, with
  only declared tools / generated inputs. A local `chmod` or an ignored
  helper can hide a broken CI path. On POSIX runners, helpers executed
  directly need a committed executable bit (`git ls-files --stage`);
  alternatively invoke the documented interpreter explicitly. See
  [Git index mode handling](https://git-scm.com/docs/git-update-index).
- Install that build and run a smoke test: launch, open the local
  database / storage, and invoke each changed plugin or native method.
  Retain the payload architecture inventory with the artifact hash; prove
  the gate rejects a mismatched native-module fixture. Header checks do not
  replace target-machine loading / smoke tests or establish native execution.
  Compare actual package metadata (for example MSI
  [Template Summary](https://learn.microsoft.com/en-us/windows/win32/msi/template-summary)
  or MSIX [Identity architecture](https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/uapmanifestschema/element-f-identity))
  with the payload and store target too; changing a filename does not set
  the installer's target architecture.
- Release credentials being present is only an input check. Verify the
  final artifact's actual signing identity against the channel's expected
  identity, reject unintended debug / ad-hoc fallback for distribution,
  and inspect after the last packaging mutation (W4). For Android, check
  the produced APK / AAB certificates; distinguish the upload key from
  Play App Signing's distribution key. See
  [Android app signing](https://developer.android.com/studio/publish/app-signing).
  Test a missing-credential path and a wrongly signed fixture so the gate
  proves it rejects an unsafe release; development artifacts may use an
  explicitly separate policy.
- Keep minimum-OS and API-boundary cases explicit: run the oldest supported
  OS (X1) as well as the current one, and guard newer native APIs at
  runtime, as with Android's [`SDK_INT`
  checks](https://developer.android.com/training/basics/supporting-devices/platforms);
  a minimum-SDK lint does not exercise the fallback branch.
- Treat a dependency that raises a deployment minimum or drops an
  architecture as a support-policy change, not a routine bump.

Traps: an OS job skipped by a path filter, missing runner or
`continue-on-error` while the pipeline shows green; a test step that
reports success with zero tests executed. Record the required jobs per
platform, their artifacts and actual executed-test counts; cases CI cannot
run go to a scheduled device-lab run or **needs device** with an owner.

Bind evidence to the final reviewed commit, workflow attempt and artifact
hash, including after a conflict resolution or dependency fix. Inspect
individual jobs, steps and raw failure / exit records; an allowed failure
is still a failure of that case. Explain conditional skips separately from
executed passes. A failed-job rerun may retain successful jobs from an older
attempt: retain their original execution records rather than claiming the
whole matrix rebuilt. Cancelled runs and green checks on an earlier head
do not qualify the final head. Record test totals and reasons for skips;
a dedicated layout run covers only the cases it actually executes.

**Verify.** Record artifact identifiers / hashes and installation channel.
Test both clean install with fresh consent and upgrade from the previous
released version with existing data and consent. Reinstall, OS update,
backup restore and account change are separate cases when affected; do not
assume reinstall resets permissions or credentials. Exercise launch, a
protected feature, links / associations and any changed update / migration
path as a standard user without developer permission overrides.

Store validation and privacy declarations need their own evidence; an
accepted upload or local permission prompt is not approval of all policies.
See P4 in [permissions](permissions.md).
For submission readiness, use the channel × territory evidence matrix in
[stores.md](stores.md#report-record) ([简体中文](stores.zh-CN.md#报告记录));
keep local artifact tests, account-owner console checks and actual store
review disposition separate.

## X7 Interrupted flows and access changes — P0 for stateful / permissioned flows

**Rule.** Verify each interruption separately, using the real app and OS
where possible. Follow [lifecycle](lifecycle.md) and
[permission-flow](permissions.md) rules; assert recoverable state and
exactly-once handling of results, rather than only "no crash".

| Scenario | Verification |
|---|---|
| Activity / view recreation | Rotate or recreate while editing. Android's "Don't keep activities" destroys activities when left; it is not a process-death test. See [developer options](https://developer.android.com/studio/debug/dev-options) |
| Background process death | Save a draft, background the app, detach the debugger and terminate only its background process with a supported test method; verify it actually exited. Resume via the existing task and separately test a notification / link cold start |
| System picker / camera / permission UI open | Cancel, rotate / resize where permitted, background / lock, and return; on supported platforms also recreate or terminate the host process while external UI is active. Assert pending actions recover or offer a safe retry, with no duplicate upload / route |
| Denial and access change | On fresh consent, test grant, deny, restricted / permanently denied where applicable, limited / approximate / one-time access where offered, and revocation in Settings. Return with a draft; verify a fresh access check, state recovery if the OS restarts the process, and a usable fallback |
| Visible but unfocused / multiple windows | Focus another app or scene while a session runs; apply resource-specific policy. Close one scene without corrupting another; see B1 / B5 |
| Lock / unlock and desktop sleep / wake | Verify saved data, allowed background work, credential / file access and reconnection; unavailable resources produce a recoverable state |

**Trap.** Force-stop, task dismissal, activity destruction and OS process
reclamation have different effects. Do not label a force-stop / relaunch
as a complete low-memory restoration or background-delivery test.
Android's [`am kill`](https://developer.android.com/tools/adb#am) targets
processes safe to kill; it may not kill one retained by a foreground
service, so check process exit. Android also does [not guarantee
`onDestroy()` on process
death](https://developer.android.com/guide/components/activities/state-changes).

**Verify.** Capture the initial state, interruption method, observed process
/ scene transition, restored state and delivered result count. Reset
developer options afterwards. Test consent under the release identity (X6)
and label emulator-only evidence accurately (X4).

## X8 Network environments — P1 for networked apps

**Rule.** Exercise network-dependent flows under controlled failures and
address-family changes. A Wi-Fi indicator or a connectivity callback is
not evidence that DNS, TLS, the API or a long-lived connection works.

**Traps.** A developer host's network path can mask a device's failure;
automatic retries can duplicate non-idempotent submissions; a DNS64-NAT64
test network can translate to IPv4 without proving the server's native
IPv6 endpoint works. Apple's [IPv6 testing
guide](https://developer.apple.com/library/archive/documentation/NetworkingInternetWeb/Conceptual/NetworkingOverview/UnderstandingandPreparingfortheIPv6Transition/UnderstandingandPreparingfortheIPv6Transition.html)
documents that last limitation; [IPv6-only support](https://developer.apple.com/support/ipv6/)
also remains a release check for applicable App Store apps.

**Verify.**

- Run launch / sign-in, download, upload and reconnect offline, with failed
  DNS, a timeout, and service errors. Assert bounded retries, cancellation,
  preserved drafts and safe retry of uncertain submissions.
- Test IPv4, a controlled IPv6-only / DNS64-NAT64 path, and native IPv6
  service reachability where applicable. Record DNS / route setup and
  evidence that the app used it; disable alternate cellular or other
  fallback routes on the test device.
- Where relevant, test captive-portal entry / exit, metered / restricted
  data, VPN / proxy and Wi-Fi ↔ cellular transitions; use hardware for
  actual carrier handover (X4). Repeat an active operation after sleep /
  wake or airplane mode, without creating duplicate sessions.
- For local discovery, test peer isolation and absent peers separately
  from permission denial. Cross-link [permissions](permissions.md) and
  [media / device](media-devices.md) results instead of reporting all
  failures as "no internet".
- **If a web build ships**, also test from the deployed origin: CORS and
  credentialed requests against the production API, and storage failure.
  Browser storage is best-effort by default and can be evicted, and
  IndexedDB / Cache API writes can throw `QuotaExceededError`; see
  [storage for the web](https://web.dev/articles/storage-for-the-web).
  Reopen offline only if offline support is promised and configured.

## X9 Production diagnostics — P1 for released apps

**Rule.** Every shipped platform reports crashes and errors from the
release build with readable stacks, and logs stay bounded and free of
private data.

- **Capture.** Initialise framework / runtime error hooks before
  application startup, including unhandled asynchronous and native-bridge
  (platform-channel) errors, and forward errors from spawned workers /
  isolates. Native crashes (signals, uncaught Objective-C / Kotlin / C++
  exceptions) need a native reporter on each native target, desktop
  included. Flutter hooks are in [framework notes](flutter.md).
- **Symbols per build, archived with the artifact (X6).**

  | Code | Keep | Note |
  |---|---|---|
  | Dart AOT with `--obfuscate --split-debug-info` | The per-platform / architecture symbols output | [`flutter symbolize`](https://docs.flutter.dev/deployment/obfuscate) needs the file from the crashing build; Windows x64 emits a PDB that `flutter symbolize` does not read — use a debugger such as WinDbg. Web is minified, not obfuscated |
  | Apple binaries, frameworks, extensions | One dSYM per binary, matched by build UUID; retain the Xcode archive | Set Debug Information Format to DWARF with dSYM File for release; include symbols in App Store Connect uploads ([Apple](https://developer.apple.com/documentation/xcode/building-your-app-to-include-debugging-information)) |
  | Android Kotlin / Java with R8 | `mapping.txt` of each release | It is overwritten on every build; AABs bundle it ([retrace](https://developer.android.com/topic/performance/app-optimization/test-and-troubleshoot-the-optimization)) |
  | Android native libraries | Native debug symbols (`debugSymbolLevel`) | Bundled in AABs, manual upload for APKs; prebuilt dependencies may already be stripped ([native symbols](https://developer.android.com/build/include-native-symbols)) |
  | Windows native code | PDBs matching the shipped binaries | A debugger needs the [symbols for the exact build](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/symbols-and-symbol-files); archive them with each release |
  | Linux native code | Separate debug files (`objcopy --only-keep-debug`) linked by build ID or debuglink | GDB checks the [build match](https://www.sourceware.org/gdb/current/onlinedocs/gdb.html/Separate-Debug-Files.html) |
  | Web JavaScript / Wasm, **only if one ships** | Source maps matching the shipped output | Generate with the toolchain's source-map option, archive per release, keep them off public hosting and verify symbolication; Flutter commands are in [framework notes](flutter.md) |

  Match against binaries extracted from the final package or installed app,
  not only an intermediate build directory. For native formats, check the
  matching identifier (Mach-O architecture / UUID, PE CodeView GUID / age,
  ELF build ID or GNU debuglink name / CRC as applicable), usable debug
  content and file hashes. Reject mismatched or empty-symbol fixtures. A
  cache hit must restore and verify the binary / symbol pair. Preserve
  release optimisation and runtime configuration when adding debug info;
  a separately compiled debug helper is not the shipped release binary.
  Retain symbols separately from user payloads where appropriate, with an
  owner and retention period that outlasts temporary CI artifact expiry.
  List engine, vendor and OS symbol coverage separately from app-owned code.

- **Logs.** Route logging through one sanitiser; never log credentials,
  tokens, full URLs with query secrets, message / document contents or
  personal data, and prefer compile-time constant messages. Restrict
  verbose / system-log output to developer builds
  ([Android log disclosure](https://developer.android.com/privacy-and-security/risks/log-info-disclosure)).
  Write detailed logs to app-private storage with size-based rotation, a
  retention limit and deletion on sign-out where the policy requires it.
  Upload support bundles only after user action or a documented policy, and
  disclose the data in store privacy declarations (P4).

  Inventory every output, including framework defaults, stderr, native
  writers and a missing-sink fallback. One bounded file does not bound a
  second writer. Avoid rendering arbitrary exception objects, caller stacks
  or context before sanitisation; use closed event / category values when
  detailed content is unnecessary. A failing diagnostic sink must not
  escape an error hook or recursively print the original private value.
  For file sinks, check symlink / hard-link destinations and replacement
  semantics: an app-private path alone must not permit truncating unrelated
  application data. Exercise rotation, retention and write failures.

  Where writers or processes share a retained file family, verify ownership
  across every active-name / history-name alias. Different locks for
  overlapping families can allow retention to remove another live writer's
  file. Exercise concurrent owners and ensure failed ownership or uncertain
  closure cannot authorise deletion or replay of a possibly committed record.
  A failed directory enumeration is not an empty, complete retention ledger.
  The app's documented budget must cover all writers it claims to bound;
  record any memory-only fallback and the data lost on process termination.

  Verify which records survive retention, not only file count and byte limits.
  Exercise equal or coarse timestamps, clock rollback, numeric suffix reuse
  and process restarts: lexical filenames or modification times alone may
  discard a just-archived segment while retaining older records. Keep the
  active file safe, establish ordering for newly retained segments, and
  document any legacy chronology that cannot be recovered.

**Traps.** A mobile-only crash SDK leaves desktop failures invisible;
symbols from "the same commit" are insufficient evidence — verify that
they match the shipped binaries (a rebuild can change UUIDs / mappings); a reporter initialised after the first frame misses
startup crashes; breadcrumbs, screenshots and HTTP traces in reports carry
tokens or user content.

**Verify.** On each native target, trigger a controlled application
error, an unhandled async / native-bridge error and a native crash in a
release-configured build installed like the shipped one. For web, trigger
framework and unhandled async errors in every shipped JavaScript / Wasm
output. Confirm each report arrives and resolves to file / function using
only the archived symbols or source maps. Run sign-in, sharing and
a failure recovery with a known marker secret, then search logs, rotated
files, support bundles and uploaded payloads for it: zero hits.
Use release / profile policy tests as well as debug tests, and exercise
hostile error rendering and a throwing sink. A sanitised fixed event proves
privacy at that entry point, not readable original stacks or native crash
capture. Label a newly captured reporter stack as a capture point; do not
present it as the original failure location.

## Report template

Evidence is scoped to a case. Include app build / artifact, OS build,
device or simulator, logical size, pixel ratio, text / locale settings,
steps, expected / observed result, and test / log / screenshot link as
relevant. Do not put credentials or private user data in artifacts.

Use the entrypoint's current output contract: scope and selected/excluded IDs,
then priority, ID, platform, status, evidence and next step, followed by separate
device plans and release blockers. The compact rows below illustrate evidence
wording only; add the target, priority and next action in a real report.

```markdown
| ID | Status | Evidence |
|----|--------|----------|
| L1 | verified | build A, iPadOS 27 simulator: resizable window crosses the documented breakpoint; size / text settings and screenshots attached |
| L3 | to do | build A, Android 17 emulator: rotation loses the edit-dialog draft; regression case attached |
| M2 | not applicable | this app ships no audio feature |
| P1 | verified | release artifact A: final Android manifest, built Apple purpose strings and signed entitlements inspected; capability inventory and artifact hashes attached |
| P2 | to do | declaration inspection complete; fresh-consent denial and Settings revocation not exercised |
| X4 | needs device | Bluetooth route switch; owner: release QA; plan: paired physical phone / headset, disconnect during playback, verify fallback and continued session |
| X6 | to do | release APK starts on 4 KB image; 16 KB native-library test pending |
| X9 | to do | release build A: Android and iOS Dart / native test crashes symbolised from archived mapping, native symbols and dSYMs; Windows / Linux reporter not yet integrated; log marker search clean |
```
