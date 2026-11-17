# Performance, size and energy (F1–F3)

Measured budgets for smoothness, delivered size, startup time and power use.
Memory peaks and decode sizes are in [media-devices.md M5](media-devices.md);
what may run while hidden is in [lifecycle.md B4](lifecycle.md). Store
thresholds below change; re-check the linked source before quoting one.

## F1 Frame pacing, jank and changing refresh rates — P1

**Rule.** Set frame-time and missed-frame budgets for representative
scrolling, navigation, animation and embedded platform / video views, and
measure them against the refresh period that is active at that moment, not a
fixed 60 Hz: about 16.7 ms at 60 Hz, 11.1 ms at 90 Hz, 8.3 ms at 120 Hz.
Drive animation and physics from frame timestamps or elapsed time, never
from a frame count or an unsynchronised timer. Request only the frame rate
the content needs; a high rate everywhere costs power (F3).

**iOS / iPadOS**
- ProMotion switches between rates up to 120 Hz; the lowest rate depends
  on the model, and Apple's own pages disagree on it for iPad Pro. Low
  Power Mode and thermal limits can remove faster rates, so an app cannot
  presume a rate at any time; use actual display-link timing.
- On iPhone, Core Animation does not exceed 60 Hz unless Info.plist sets
  `CADisableMinimumFrameDurationOnPhone` to `true`; iPad Pro needs no key.
- With `CADisplayLink`, set `preferredFrameRateRange` per content and drive
  updates from `targetTimestamp`; a callback that overruns it loses the
  next interval.

**Android**
- Devices may run 60 / 90 / 120 Hz and the scheduler may change the rate at
  runtime or decline a `Surface.setFrameRate()` request (API 30+), for
  example in battery saver. Do not call it every frame; listen for display
  changes instead of polling `getRefreshRate()`, which can cost a binder call.
- Android defines slow frames as over 16 ms and frozen frames as over
  700 ms; Play vitals reports both for View-based UI (not for apps that
  bypass `Choreographer`, such as Vulkan / OpenGL renderers). They have no
  core-vital bad-behaviour threshold, but no frame should ever exceed
  700 ms. Games get a separate slow-session metric (20 / 30 fps targets).

**macOS / Windows / Linux**
- A window can move between monitors with different and variable refresh
  rates (60 Hz external display, 120 Hz ProMotion laptop panel, Windows 11
  dynamic refresh rate on supported panels). Read the rate from the display
  the window is on now; on macOS 14+ `NSView.displayLink(target:selector:)`
  follows the view's display and `NSScreen.maximumFramesPerSecond` gives the
  per-screen maximum (macOS 12+).
- Hidden or occluded windows may stop receiving frame callbacks; animation
  driven by elapsed time resumes correctly, animation driven by frame count
  jumps or stalls.

**Traps.** Measuring in a debug / JIT build or on a simulator / emulator;
averages that hide tail frames; one 60 fps overlay or spinner keeping the
whole screen at a high rate; a frame-rate request issued on every frame;
first-use shader or image work causing a one-time hitch that a warm rerun
does not show.

**Verify.** Profile release or profile builds on the slowest supported
physical phone and on a high-refresh device. Record p90 / p99 frame time and
the count of frames over budget and over 700 ms for each scripted flow, on a
fresh install and on a warm run. Repeat with Low Power Mode / battery saver
on, while dragging a desktop window between monitors with different refresh
rates, and while the device is warm. Use the platform profiler (Instruments,
Android Studio / Perfetto with `dumpsys gfxinfo`, or the framework's
timeline).

Flutter profiling and size-analysis commands are in
[the framework reference](flutter.md).

Sources: [ProMotion and display-link pacing](https://developer.apple.com/documentation/quartzcore/optimizing-iphone-and-ipad-apps-to-support-promotion-displays),
[Android slow rendering](https://developer.android.com/topic/performance/vitals/render),
[Android frame-rate API](https://developer.android.com/media/optimize/performance/frame-rate),
[`NSView.displayLink`](https://developer.apple.com/documentation/appkit/nsview/displaylink(target:selector:)),
[Windows dynamic refresh rate](https://devblogs.microsoft.com/directx/dynamic-refresh-rate/).

## F2 App size and startup budgets — P1

**Rule.** Keep separate size and startup budgets per shipped artifact,
architecture and representative device class, and track them per release.
Measure what users receive (download and installed size per device variant)
and when the first frame and the usable content appear. Defer optional
initialisation (analytics, SDK warm-up, sync, migrations that are not
blocking) until after usable content; never block the first frame on the
network.

**Size**
- iOS / iPadOS: do not measure the `.app`, `.xcarchive` or uploaded `.ipa` (they
  contain files users never download). Export with "All compatible device
  variants" to get the App Thinning Size Report (compressed ≈ download,
  uncompressed ≈ installed); App Store Connect gives the authoritative
  per-variant sizes and warns when a variant exceeds the cellular download
  limit.
- Android: an App Bundle is split per device; read download size in Play
  Console. Play's compressed download limits are currently 500 MB per base
  or feature module, 4 GB for all modules and install-time asset packs, and
  100 MB for apps still published as APKs.
- Desktop: record installer size and on-disk size after install and after an
  update (old versions, caches and bundled runtimes accumulate).
  Universal / multi-architecture binaries are larger than any one
  architecture's download.

Where a project has an agreed artifact budget, enforce it against the final
bytes after packaging / signing, not an intermediate file or a rounded
display value. Define the metric: compressed installer bytes, logical
regular-file payload bytes and filesystem allocation are different values;
state symlink / hard-link treatment and do not follow links outside the
payload. Retain the measured artifact hash and exact byte count. Build
artifact measurements are useful regression gates but do not substitute for
store-delivered variant or device measurements above. If a budget or usable
startup definition is missing, record that decision separately and still
report available observations; do not invent a universal threshold.

**Startup**
- Android: TTID (first frame, reported by the system) and TTFD (usable
  content, reported by the app with `reportFullyDrawn()` /
  `FullyDrawnReporter`). Play vitals treats cold starts of 5 s or longer,
  warm of 2 s or longer and hot of 1.5 s or longer as excessive (measured by
  TTID). Ship a Baseline Profile so startup and critical paths are
  ahead-of-time compiled from the first launch; Play reports about 30 %
  faster code execution in many apps, and some non-Play stores may not apply
  it at install time.
- Apple: MetricKit delivers daily launch, resume and hang metrics from the
  field on iOS / iPadOS 13+; scroll-hitch metrics need iOS / iPadOS 14+
  and cover `UIScrollView`. On macOS, daily metric reports need macOS 26+
  (diagnostic reports macOS 12+). Check each metric's availability (Apple
  marks `MXMetricManager` deprecated in favour of
  `MetricManager`) and use Instruments for local startup traces.
- Desktop: cold start from a spinning disk, network home directory or a
  freshly updated install (security scanning of new binaries) can be far
  slower than a warm start on the developer's SSD.

**Traps.** Comparing a universal upload with a device-specific download;
measuring debug builds; stopping the clock at splash dismissal while content
is still loading; benchmarking with an empty database or account instead of
realistic data; a first-run or upgrade migration that runs on the main
thread; a launch that waits for a network timeout when offline.

**Verify.** For each release record download and installed size per
platform / architecture and diff them against the previous release (size
analyser output where the toolchain has one). Measure cold and warm start
at least ten times on the low-end supported device with a realistic data
set, on first run after upgrade, offline and with slow dependencies; report
the median and worst (Android: Macrobenchmark `StartupTimingMetric`).

Sources: [Apple app size measurement](https://developer.apple.com/documentation/xcode/reducing-your-app-s-size),
[Play size limits](https://support.google.com/googleplay/android-developer/answer/9859372),
[TTID / TTFD](https://developer.android.com/topic/performance/vitals/launch-time),
[Play startup thresholds](https://developer.android.com/google/play/vitals/launch-time),
[startup analysis](https://developer.android.com/topic/performance/appstartup/analysis-optimization),
[Baseline Profiles](https://developer.android.com/topic/performance/baselineprofiles/overview),
[MetricKit](https://developer.apple.com/documentation/metrickit),
[Flutter app size](https://docs.flutter.dev/perf/app-size).

## F3 Energy consumption and thermal adaptation — P1

**Rule.** Bound idle, active and background resource use: an idle visible
screen does no repeated work, and a hidden app does only the work B4 allows.
Observe the platform's power-saving and thermal signals and shed optional
work (frame rate, effects, video resolution, prefetching, polling, ML)
before the OS throttles it, while preserving the core task and its
progress. Step quality down and back up with hysteresis so it does not
oscillate.

**Signals**
- Apple: `ProcessInfo.thermalState` (`nominal`, `fair`, `serious`,
  `critical`) with `thermalStateDidChangeNotification`;
  `isLowPowerModeEnabled` (iOS 9+, macOS 12+) with
  `NSProcessInfoPowerStateDidChange`. ProMotion already lowers the maximum
  refresh rate in Low Power Mode or when hot (F1).
- Android: `PowerManager.getCurrentThermalStatus()` /
  `addThermalStatusListener()` (API 29+) and `getThermalHeadroom()`
  (API 30+; sample conservatively — the ADPF guide recommends at least
  10 s between calls — and handle `NaN` from unsupported or rate-limited
  implementations; some devices report status `NONE` despite throttling,
  so cross-check headroom);
  `PowerManager.isPowerSaveMode()` for battery saver.
- Windows: Windows App SDK `PowerManager.EnergySaverStatus` /
  `EffectivePowerMode` and their change events; power source and battery
  status for laptops.

**Android vitals.** Excessive partial wake locks is a core vital: a session
is excessive when its non-exempt partial wake locks add up to 2 hours or
more in 24 hours, counted while the app is in the background or running a
foreground service; more than 5 % affected sessions across devices over
28 days can affect Play visibility. Since 1 March 2026 Play may exclude
such apps from discovery surfaces or show a battery warning on the
listing. Bound the work, handle cancellation and release manually acquired
wake locks in `finally` paths. WorkManager workers must finish promptly —
their wake locks can still count — and a foreground service does not by
itself keep the CPU awake (B4).

**Traps.** Animations, spinners or video still running when obscured or
off-screen; reconnect or polling loops with no backoff while offline; a
wake lock, screen-on flag or desktop sleep inhibitor never released after
an error; a secondary animation requesting a higher frame rate than the
main content needs; thermal mitigation that toggles quality every few
seconds; ignoring battery saver on laptops.

Separate UI observation from core service work. Stop optional status polling
when its UI is hidden or disposed, and refresh when visible again; a visible
desktop window that loses focus is not necessarily hidden (B1). Bound slow
reads to the intended concurrency, discard ordinary timer backlog and
coalesce at most the required fresh resume read. Stopping a UI timer must
not stop an active call, transfer or other permitted core task. Test hide,
resume, slow completion and disposal with a controlled scheduler; those
tests prove lifecycle behaviour, not a measured energy saving.

**Verify.** On battery-powered hardware run a scripted idle screen (5–10
minutes) and a sustained workload (for example 15 minutes of video call or
camera capture). Record CPU / GPU time, wakeups, network activity and any
available energy estimate with a local platform profiler (Xcode energy
gauge / Instruments, Android Studio / Perfetto), and log thermal-state
changes during the run; use MetricKit's aggregated reports for field
behaviour, not for this run. Repeat with Low Power Mode / battery saver /
Energy Saver on and confirm optional work drops and recovers when the
setting or thermal state clears. Check Play vitals wake-lock data after
release.

Sources: [Apple energy practices (WWDC22)](https://developer.apple.com/videos/play/wwdc2022/10083/),
[Apple thermal state](https://developer.apple.com/documentation/foundation/processinfo/thermalstate-swift.enum),
[Low Power Mode](https://developer.apple.com/documentation/foundation/processinfo/islowpowermodeenabled),
[Android thermal APIs](https://developer.android.com/games/optimize/adpf/thermal),
[Android vitals thresholds](https://developer.android.com/topic/performance/vitals),
[excessive wake-lock definition](https://developer.android.com/google/play/vitals/excessive-wakelock),
[wake-lock metric](https://developer.android.com/blog/posts/raising-the-bar-on-battery-performance-excessive-partial-wake-locks-metric-is-now-out-of-beta),
[Windows App SDK `PowerManager`](https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.system.power.powermanager).
