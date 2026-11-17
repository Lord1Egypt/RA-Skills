# Background Work — WorkManager, Services, Alarms, and Doze

Android has spent a decade making background work harder on purpose. Every API here is a negotiation with the battery, and the OEM gets the last word.

**Contents:** [Pick by the Promise You Need](#pick-by-the-promise-you-need) · [WorkManager](#workmanager) · [Foreground Services](#foreground-services) · [Alarms](#alarms) · [Doze and App Standby](#doze-and-app-standby) · [OEM Battery Managers](#oem-battery-managers) · [Push as a Trigger](#push-as-a-trigger) · [Testing Background Work](#testing-background-work) · [Background Traps](#background-traps)

**Before diagnosing "it does not run"**, read `## Pain Points` in `~/Clawic/data/android/memory.md` and the device rows in `~/Clawic/data/devices/devices.md` — the OEM of the device that reported the bug is usually the whole explanation.

## Pick by the Promise You Need

| Promise | Mechanism | Cost |
|---|---|---|
| Must eventually happen, even after reboot or app death | WorkManager | You do not choose when |
| Must happen now and the user knows about it | Foreground service with a declared type | A permanent notification, a declared type, and Play justification |
| Must happen at a wall-clock moment | Exact alarm | A restricted permission; eligibility limited to alarm and calendar apps |
| Should happen soon, small and user-initiated | Expedited WorkManager work | A per-app quota; degrades to normal work when exhausted |
| Only matters while the user is looking | A coroutine in `viewModelScope` | Dies with the screen |
| Only matters while the app is foreground and must survive navigation | Application-scoped coroutine | Dies with the process |

Choosing wrong is the root cause of nearly every "it works on my phone" background bug: a coroutine survives navigation but not process death, and a plain background service does not start at all from the background since targetSdk 26.

## WorkManager

- The durability layer: work is persisted to a database, survives process death and reboot (with the right constraint), and is executed under the system's scheduler.
- **Periodic work has a hard 15-minute minimum interval.** Anything shorter is not a configuration question; the design has to change. The flex window controls where in the interval the work may run, and the system still decides the exact moment — a "every 15 minutes" job that lands every 25 in a low standby bucket is working correctly.
- Constraints (network type, charging, battery not low, storage not low, device idle) are the honest way to express requirements. A job with no constraints that then checks connectivity itself wastes wakeups.
- Unique work with a policy is what stops duplicate jobs: `KEEP` (the existing one wins), `REPLACE`/`UPDATE` (the new one wins), `APPEND_OR_REPLACE` (chained). A sync scheduled on every app launch without a unique name schedules a new job every launch.
- Backoff: exponential or linear, with a floor of about 10 seconds and a ceiling around 5 hours. A worker that returns `retry` on a permanent failure (a 400, a deleted resource) retries until the ceiling forever — distinguish `failure` from `retry` deliberately.
- Workers get a limited execution window; long work is a foreground-service worker (`setForeground`) with the notification and, on modern targets, the declared type.
- Input and output are `Data` objects with a size cap in the low tens of kilobytes. Pass ids and read from the database, exactly as with saved state (SKILL.md Rule 4).
- Workers are constructed by the framework; injecting into them requires the DI framework's worker support plus a custom factory (`architecture.md`).

## Foreground Services

- `startForegroundService()` obliges you to call `startForeground()` within roughly 5 seconds, or the system kills the app with `ForegroundServiceDidNotStartInTimeException`. Build and post the notification as the first statement in `onCreate`, before any initialization — a dependency graph resolving on first access has eaten that window in real apps.
- From targetSdk 34, every foreground service declares a **type** in the manifest and holds the permission for that type, and the type must match reality. Play asks for a justification per type at submission, and a mismatch between the declared type and observable behavior is a rejection (`play-console.md`).
- Starting a foreground service *from the background* is blocked with a narrow exemption list. The supported alternative is expedited work, or a high-priority push that wakes the app into a legal state.
- Long-running `dataSync` services acquired a per-day time budget from targetSdk 35: a design that used one as a permanent worker now stops partway through the day. Move periodic sync to WorkManager and keep the foreground service for the user-initiated case.
- The notification is not optional and users see it. A service whose notification cannot be honestly described to the user is the wrong mechanism.

## Alarms

- Inexact alarms are batched by the system and are the right default for anything that is "around" a time.
- Exact alarms need `SCHEDULE_EXACT_ALARM` (revocable by the user, and the app must handle being refused) or `USE_EXACT_ALARM` (granted at install, restricted by Play policy to apps whose core function is alarms, timers or calendars). Requesting the wrong one is both a policy problem and a runtime failure when the user revokes it.
- Check the permission before every schedule, not once at startup: it can be revoked while the app runs, and scheduling without it throws.
- Alarms do not survive reboot. Reschedule from a `BOOT_COMPLETED` receiver, which itself requires a permission and does not fire for an app the user force-stopped until they open it again.
- `setAndAllowWhileIdle` and `setExactAndAllowWhileIdle` punch through Doze, but the system rate-limits how often — on the order of once every several minutes per app. A design that needs finer granularity while the screen is off does not exist on Android.
- A user-visible countdown or timer is a foreground service, not a chain of alarms.

## Doze and App Standby

Two independent systems, and both are invisible from inside the app:

- **Doze** engages when the device is stationary, unplugged and screen-off. Network access and wakelocks are suspended, alarms deferred, and jobs held until a maintenance window; the windows become less frequent the longer the device stays idle. High-priority push still gets through, briefly.
- **App Standby buckets** classify each app by how recently and often the user interacts with it — from active, through working-set and frequent, to rare and restricted. Job scheduling frequency, alarm allowance and network access tighten with each step down. Your test device, which you open constantly, is in the top bucket; the user who opens the app monthly is not, and their experience is a different app.
- Consequence: never verify a background feature on a plugged-in device you are actively using. Force the bucket down and force Doze on before believing anything (→ Testing).
- `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` exists and Play restricts which app categories may prompt for it. Asking a general-purpose app's users to exempt it is both a policy risk and an admission that the design fights the platform.

## OEM Battery Managers

- Several large manufacturers add their own, undocumented process killers on top of the platform's. Symptoms: WorkManager jobs that never run after the app has been closed for hours, alarms that never fire, push that arrives only when the app is opened, and a sync that works perfectly on a Pixel.
- These behaviors differ by manufacturer, by regional firmware, and by whether the user has toggled a per-app battery setting buried in the OEM's settings app.
- What actually works: design so that delayed execution is acceptable; make the app's state converge on next launch rather than depending on background delivery; and for the user-visible case, use a foreground service the OEM will not kill silently.
- When a bug report only comes from one manufacturer, the OEM row in `~/Clawic/data/devices/devices.md` is the first thing to check, and the finding belongs in `## Pain Points` because it will be reported again.

## Push as a Trigger

- Treat push as a *hint* to sync, not as data transport. Messages can be dropped, delayed, collapsed or delivered out of order, and Doze holds normal-priority messages until a maintenance window.
- High-priority messages wake the device, and platforms rate-limit apps that use them for work the user cannot see. Reserve them for genuinely user-visible events.
- The payload carries an id; the app fetches the truth from its own backend into the database, and the UI updates because it observes the database (`architecture.md`). This removes every ordering and duplication problem at once.
- A notification shown from a push needs `POST_NOTIFICATIONS` on targetSdk 33+, requested in context (`permissions.md`) — an app that never asked simply produces nothing when it pushes.

## Testing Background Work

- Force Doze: put the device on battery, then use the device-idle shell commands to force an idle state and step through maintenance windows. Undo it afterwards or subsequent testing is nonsense.
- Force a standby bucket for the package with the app-standby shell command and verify the feature still works from `rare`.
- Inspect what the system actually has scheduled with the jobscheduler and alarm dumps for your package — that is how you find out whether the job was never scheduled or scheduled and deferred, which are opposite bugs.
- WorkManager ships a test harness that drives constraints, delays and periodic intervals synchronously; use it for worker logic and the device for scheduling behavior.
- The real test is the boring one: install, use the app once, leave the device untouched and unplugged overnight, and check in the morning.

## Background Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| A plain background `Service` for work | Cannot be started from the background since targetSdk 26 | WorkManager, or a foreground service with a type |
| Periodic work "every 5 minutes" | The floor is 15 minutes; the request is silently adjusted | Redesign, or a foreground service if it is genuinely continuous |
| Initialization before `startForeground()` | The 5-second window expires and the app is killed | Notification first, work second |
| Returning `retry` for permanent failures | Retries to the backoff ceiling forever, burning battery | `failure` for anything a retry cannot fix |
| Scheduling sync on every launch without a unique name | Duplicate jobs multiply | Unique work with an explicit policy |
| Testing background work plugged in, on a Pixel, with the app open | Every restriction is suppressed | Unplugged, forced bucket, forced Doze, OEM device |
| Passing a payload through `Data` | Size cap; and the payload is stale by the time it runs | Pass an id, read from the database |
| Prompting for battery-optimization exemption to fix reliability | Policy risk, and it treats the symptom | Design for eventual execution |
| Alarms without a reboot receiver | Everything scheduled is lost at reboot | Reschedule on `BOOT_COMPLETED`, and accept it never fires after a force-stop |
| Exact alarms for non-alarm features | The permission is restricted and can be revoked at any time | Inexact alarms or WorkManager |

## Write Down What It Was

- **An OEM-specific killer and the workaround that held** goes to `## Pain Points` in `~/Clawic/data/android/memory.md`, naming the manufacturer and the OS version — the same report arrives again from another user on the same skin (`memory-template.md`).
- **The device it was reproduced on** gets its row in the shared `~/Clawic/data/devices/devices.md` with a note about its battery manager, so the next investigation starts on the right hardware.
- **A scheduling design decision** — what runs as WorkManager, what runs as a foreground service and why, with the declared types — is `artifacts/adr-<name>.md`; it is also the source text for the Play justification (`play-console.md`).
