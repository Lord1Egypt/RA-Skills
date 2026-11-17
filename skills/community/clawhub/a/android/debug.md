# Debugging on Device — Tools, Logs, and Reproduction

Diagnosis is where Android eats hours. The tooling answers most questions in one command; the trick is knowing which command asks your question.

**Contents:** [The Universal First Three](#the-universal-first-three) · [Logcat Properly](#logcat-properly) · [Inspecting App and System State](#inspecting-app-and-system-state) · [Driving the App From the Shell](#driving-the-app-from-the-shell) · [StrictMode](#strictmode) · [Memory Leaks](#memory-leaks) · [Simulating Hostile Conditions](#simulating-hostile-conditions) · [Reproducing "Only on Their Device"](#reproducing-only-on-their-device) · [Debugging Traps](#debugging-traps)

**Before the first command**, read `## Pain Points` and `## App Context` in `~/Clawic/data/android/memory.md` and open any `artifacts/runbook-*.md` its `## Boxes` index names for this symptom. Half of all repeat incidents are the same incident, and the runbook is faster than the chain below.

## The Universal First Three

1. **`adb logcat --pid=$(adb shell pidof -s <package>)`** — everything your app logged, and nothing else. Tag filters (`-s MyTag:*`) miss the framework messages that name the actual cause; the pid filter does not. Add `*:E` on top when the log is too noisy to read.
2. **`adb shell dumpsys activity <package>`** — the system's view of your app: activities, their states, the task stack, and what it thinks is in the foreground. When the app "does nothing", this says whether the component was even started.
3. **`adb shell dumpsys package <package>`** — installed version, signing certificate summary, granted permissions, declared components and their exported state. Half of all permission and deep-link mysteries end here.

## Logcat Properly

- Buffers: the default set hides some system messages. `-b all` widens it when a crash leaves no trace; the crash buffer specifically holds native crash reports.
- `adb logcat -c` clears before a reproduction so the log starts at the moment of interest. Doing this before every attempt is the difference between reading a log and searching one.
- `-v threadtime` gives timestamps, pid and tid, which is the only way to see that two things happened in the wrong order. `-v time` is not enough when concurrency is suspected.
- The log has a fixed ring-buffer size and a high-volume app overwrites its own crash. Raise the buffer size for a debugging session, and remember that a `logcat` full of debug output is itself a production cost (`performance.md`).
- Verbose logging can be enabled per tag at runtime with a system property, so a library's diagnostic output can be turned on without rebuilding.
- **Logcat output is not a safe paste.** Auth headers, tokens, user identifiers and personal data end up there routinely. If a log excerpt has to be kept, strip those values before writing anything (`memory-template.md`).

## Inspecting App and System State

| Question | Where the answer is |
|---|---|
| Is my job actually scheduled, or just requested? | The jobscheduler dump, filtered to the package (`background.md`) |
| Did my alarm get registered, and when does it fire? | The alarm dump |
| Which notification channels exist, with what importance? | The notification dump |
| Why does this intent open the wrong app? | Resolve the intent through the package manager's resolve command |
| Are my App Links verified? | The domain-verification state for the package |
| How much memory is the process using, and where? | The meminfo dump for the package |
| Is the app being frozen or bucketed? | The app-standby and device-idle state for the package |
| What is the frame timing on this screen? | The gfxinfo dump with frame statistics, reset before the interaction |
| What did the app store on disk? | The app's data directory via run-as, on a debuggable build |

A device bug report bundles most of these plus the system logs into one archive, which is the right artifact to ask a user for — and the wrong thing to store, because it contains their data.

## Driving the App From the Shell

- Start an activity with explicit extras to reproduce a state without navigating to it — the fastest way to test a screen that is five taps deep.
- Send a VIEW intent with a URL to test a deep link exactly as the system delivers it, instead of tapping a link in a chat app that rewrites URLs (`lifecycle.md`).
- Broadcast an intent to exercise a receiver, including simulated system events where the receiver is not protected.
- Clear app data (`pm clear`) for a true first-launch test — uninstalling and reinstalling is slower and also resets permissions differently than a real update does. This is destructive: it deletes the user's data on that device, and it needs confirmation before it runs.
- Change device settings (animation scales, locale, font scale, dark mode, display size) from the shell to test configurations without hunting through settings menus.
- Simulate input events and text entry for a deterministic repro of a gesture-triggered bug.

## StrictMode

- Enable it in debug builds only, in `Application.onCreate`, before anything else initializes.
- Thread policy catches disk reads, disk writes and network on the main thread — the exact operations that produce jank and ANRs (SKILL.md Rule 5). VM policy catches leaked closeables, leaked Activity instances, unsafe intent launches and non-SDK API usage.
- Start with logging, fix the violations, then switch the ones you have cleared to `penaltyDeath` so a regression fails loudly in development rather than quietly in production.
- Third-party SDKs will produce violations you cannot fix. Suppress those specific ones deliberately, with a comment naming the SDK — a blanket suppression removes the tool's value entirely.
- StrictMode's violations are early warnings for upcoming platform enforcement: unsafe intent launches and non-SDK API usage both became hard errors after being StrictMode findings (`sdk-upgrades.md`).

## Memory Leaks

- The classic Android leak is an object holding an Activity, Fragment view, or Context past its lifetime: a static field, a singleton listener never unregistered, a long-lived callback, a non-static inner class of an Activity, or a Fragment binding not nulled (`views.md`).
- Symptom without a tool: memory grows with every rotation and never returns. Rotate ten times, force a garbage collection from the memory profiler, and see whether the count of Activity instances is one or eleven.
- A leak detection library in debug builds catches these automatically and points at the reference chain. Add it as a debug-only dependency so it cannot ship.
- A heap dump answers "what is holding it": find the object, walk the shortest strong reference path to a GC root, and the field on that path is the bug.
- Bitmaps dominate real memory: a full-resolution photo decoded at four bytes per pixel is tens of megabytes regardless of the file size on disk (`performance.md`).

## Simulating Hostile Conditions

The conditions your users have and your desk does not:

- **No network, then flaky network**: airplane mode, then a throttled or lossy profile on the emulator. Most retry and offline bugs need the *transition*, not the steady state.
- **Doze and a low standby bucket**: force both from the shell before believing any background feature works (`background.md`).
- **Process death**: `am kill` while the app is backgrounded, then return from Recents (`lifecycle.md`).
- **Low memory**: the "don't keep activities" and background-process limit developer options approximate a device under pressure.
- **A slow device**: developer options can slow animations, but they cannot simulate a slow CPU. Keep one genuinely low-end device (`devices.md`).
- **Large text and display size**: the two settings that break more layouts than any device model.

## Reproducing "Only on Their Device"

Ask for, in this order: the exact OS version and device model, whether it is a fresh install or an update, the app version, the steps, and a bug report if they can produce one. Then:

1. Match the API level on an emulator first — free and fast, and it catches genuine platform differences.
2. Check the OEM. If it is a background, notification or battery report and the device is from a manufacturer with an aggressive battery manager, that is the hypothesis until disproven (`background.md`).
3. Check the locale and the display settings. Right-to-left layouts, long translations, 200% font scale and non-Gregorian calendars break real apps.
4. Check the install path. Sideloaded, from an old backup, restored to a new device, or updated from a very old version each produce state your fresh install never has.
5. If it still does not reproduce, ship a build with more diagnostics to that user rather than guessing — and remove the diagnostics afterwards.

## Debugging Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Filtering logcat by your own tag | Framework messages naming the cause are filtered out | Filter by pid |
| Debugging the debug build for a release-only bug | R8, resource shrinking and different flags mean it is a different app | Build the release variant, temporarily debuggable if needed (`release.md`) |
| Reading only the last line of a stack trace | The last line is usually the framework rethrowing | Read to the first frame in your package, then the `Caused by:` chain |
| Adding logging and rebuilding, repeatedly | Each cycle costs minutes and changes timing | Set a breakpoint, or drive the state from the shell |
| Testing a first launch by reinstalling | Reinstalling resets things a real update does not | `pm clear` on a device you own, with confirmation |
| Believing a fix because the symptom went away once | Timing bugs hide when you look at them | Reproduce reliably first, then fix, then re-run the repro |
| Keeping a user's bug report file | It contains their data and their tokens | Extract the stack trace, discard the archive |
| Long-lived verbose logging in release | Battery, log-buffer pressure, and a privacy leak | Debug-only, and stripped from release |

## Write Down What It Was

- **A cause that took more than a couple of minutes to find** is one line in `## Pain Points` of `~/Clawic/data/android/memory.md`: date, symptom, actual cause, what changed. This is what stops the next session re-walking the chain (`memory-template.md`).
- **An environmental fact that will change future decisions** — a corporate proxy CA, a specific OEM's behavior, a device's OS quirk — goes to `## App Context` or the device's row in `~/Clawic/data/devices/devices.md`, because it applies to everything, not just this incident.
- **The second time the same failure appears**, it becomes `artifacts/runbook-<symptom>.md`: the ordered checks and the fix, with its `## Boxes` line naming the symptom as the read condition.
