# Crashes, ANRs, and Vitals

A crash in the field is a different investigation from a crash on your desk: you get a stack trace, a device distribution and a rate, and you have to work backwards.

**Contents:** [Deobfuscate First](#deobfuscate-first) · [Cluster Before Fixing](#cluster-before-fixing) · [ANRs: Read the Trace, Not the Message](#anrs-read-the-trace-not-the-message) · [The ANR Timeout Table](#the-anr-timeout-table) · [Common ANR Causes](#common-anr-causes) · [Native Crashes](#native-crashes) · [Crashes You Cannot Reproduce](#crashes-you-cannot-reproduce) · [Vitals as a Release Gate](#vitals-as-a-release-gate) · [Crash Traps](#crash-traps)

**Before triaging**, read `## Pain Points` and the current `releases/<year>.md` row in `~/Clawic/data/android/memory.md`'s boxes: a crash that started at a specific version has its cause in that release's diff, and that is usually the whole investigation.

## Deobfuscate First

- A release stack trace obfuscated by R8 is unreadable without the `mapping.txt` for **that exact versionCode**. The mapping file is generated per build and differs between builds of the same source (SKILL.md Rule 8).
- With the Android Gradle plugin, the mapping file is uploaded with the bundle automatically for Play's own crash reporting; third-party crash reporters need their own upload step, usually a Gradle plugin, and it is the step people forget in a new CI pipeline (`ci.md`).
- If the upload was missed, the mapping file can still be applied locally with the retrace tool that ships with the build tools — provided the file was kept. If it was not kept, that build's crashes are permanently unreadable, which is why the release row records where the mapping went (`memory-template.md`).
- Line numbers survive obfuscation only if the keep rules preserve source-file and line-number attributes and the build renames the source file to a constant. Without that, you get method names and no lines.

## Cluster Before Fixing

- Group by **exception type + top frame in your own package**, not by the reporter's default grouping, which splits one bug across several signatures when the framework frames differ by OS version.
- Sort by users affected, not by event count: a crash loop from one device generates thousands of events and affects one person.
- For each cluster, read the distribution before the code: one OS version, one manufacturer, one locale or one app version in the breakdown *is* the hypothesis.
- A crash that starts exactly at a version is in that version's diff. A crash that grows slowly across versions is usually data-dependent — a value that only some users have accumulated.
- The breadcrumb trail (last screens, last actions) matters more than the stack for state-related crashes, because the stack shows where it died, not what put it in that state.

## ANRs: Read the Trace, Not the Message

An ANR report contains the stack of every thread at the moment of the timeout. The message names the trigger; the main thread's stack names the cause.

- **Main thread `RUNNABLE` in your code** — you are doing too much work. Move it off-thread.
- **Main thread blocked on a lock** — find the thread holding it in the same dump; that thread's stack is the real bug. Deadlocks appear as two threads each waiting on the other's lock.
- **Main thread in a binder call** (`BinderProxy.transactNative`) — waiting on another process: a content provider, a system service, or your own remote service. The remote side is slow or dead.
- **Main thread idle in the message loop** — the app was not busy. The system was: heavy I/O elsewhere, a device under memory pressure, or a broadcast queue backed up. These are the ANRs that are not your bug, and they show up disproportionately on low-end devices.
- **Main thread on disk I/O** (`FileInputStream.read`, a SharedPreferences load, a Room query) — the single most common real cause, and the one StrictMode catches in development (`debug.md`).

## The ANR Timeout Table

| Trigger | Approximate limit |
|---|---|
| Input dispatch (touch or key not handled) | 5 s |
| Broadcast receiver, foreground | 10 s |
| Broadcast receiver, background | around a minute |
| Service start or lifecycle callback, foreground | 20 s |
| Service, background | several minutes |
| ContentProvider publish | 10 s |
| `startForeground()` after `startForegroundService()` | ~5 s, and it kills rather than ANRs (`background.md`) |

Design consequence: `onReceive` is not a place to do work. It runs on the main thread, it has ten seconds at most, and the process may be killed as soon as it returns — hand off to WorkManager and return.

## Common ANR Causes

| Cause | Signature | Fix |
|---|---|---|
| Disk or database on the main thread | Main thread in a file or SQLite frame | Off-thread; StrictMode to find the rest |
| A synchronous SharedPreferences load at startup | Main thread in preferences initialization | DataStore, and do not gate the first frame on it (`data.md`) |
| Work in `onReceive` | ANR attributed to a broadcast | Enqueue and return |
| A lock held across an I/O call | Main thread waiting, worker thread in I/O | Never hold a lock across I/O |
| A slow content provider (yours or another app's) | Main thread in a binder transaction | Query off-thread; treat other apps' providers as network calls |
| A huge saved-state or intent payload | Main thread in binder, plus `TransactionTooLargeException` nearby | Pass ids (SKILL.md Rule 4) |
| An unbounded main-thread loop over a growing dataset | Main thread runnable in your own code | Paginate, or move the computation |
| Initialization done eagerly in `Application.onCreate` | Main thread in library initialization, at launch | Lazy initialization; measure startup (`performance.md`) |

## Native Crashes

- A native crash produces a tombstone with a signal (SIGSEGV, SIGABRT), a fault address and native backtraces. It is not a Java exception and does not go through the usual handler.
- `SIGSEGV` at a low address is a null dereference in native code; `SIGABRT` usually means an assertion or an uncaught C++ exception in a library.
- The backtrace needs symbolication with the unstripped native libraries for that exact build — so the debug symbols have to be kept alongside the mapping file, or the trace is a list of addresses.
- Common sources in apps with no native code of their own: an image or video decoding library, a database engine, a crypto library, and the ABI mismatch case where the wrong architecture's library was packaged.
- Native crashes concentrated on one architecture or one OS version usually mean a library packaging problem, not a logic bug (`release.md`).

## Crashes You Cannot Reproduce

1. Match the distribution: one OS version, one OEM, one locale, one app version. That narrows it more than any amount of code reading.
2. Read the breadcrumbs for the state that preceded it, and try to reconstruct that state directly from the shell rather than by playing through the app (`debug.md`).
3. Look for the race: crashes that appear with no pattern and a low rate are usually concurrency or lifecycle races, and they concentrate on slow devices, where the window is wider.
4. Add targeted, non-personal diagnostic context to the reporter for that code path — the state that would have made the trace obvious — and ship it.
5. Defensive code is the last resort, not the first: a null check that hides a state bug converts a crash into a wrong screen, which is harder to detect and worse for the user.

## Vitals as a Release Gate

- Play measures **user-perceived** crash and ANR rates — those that happen while the user is interacting — and publishes bad-behavior thresholds above which an app's store visibility can be affected. The published figures have been around 1.09% for crashes and 0.47% for ANRs; verify the current numbers on Play's own vitals documentation before treating either as a hard line, and read them as a floor of acceptability rather than a target.
- Your own gate should be much tighter and expressed as a delta: a staged rollout is halted when the crash-free rate drops more than a fraction of a point against the previous version at the same rollout stage, not against an absolute number (`play-console.md`).
- Compare like with like: the first hours of a rollout over-represent enthusiastic users on new devices, and the numbers move as the rollout widens. Two data points from the same rollout stage are comparable; the first hour against a full week is not.
- The vitals numbers for each release go into that release's row in `releases/<year>.md`, roughly 48 hours in, so "is this worse than last time" is answerable without opening the console.

## Crash Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Losing the mapping file for a shipped build | Every crash from that build is permanently unreadable | Upload it, keep it, and record where it went in the release row |
| Fixing the top crash by event count | It may affect one device in a loop | Sort by users affected |
| Reading the ANR message instead of the thread dump | The message names the trigger, never the cause | Read the main thread's stack, then whoever holds its lock |
| Doing work in `onReceive` | Ten seconds on the main thread, and the process can die right after | Enqueue and return |
| Catching `Exception` broadly to reduce the crash rate | Converts crashes into silent corruption and swallows coroutine cancellation | Fix the cause; catch what you can handle |
| Comparing early-rollout vitals with a mature release | Different populations entirely | Compare at the same rollout stage |
| Treating Play's bad-behavior threshold as a target | It is the line at which the store acts, not a quality bar | Set your own delta-based gate |
| Ignoring ANRs because "they are not crashes" | Users experience them as worse than crashes, and Play weighs them heavily | Treat the ANR rate as a release gate too |
| Storing a user's full bug report to investigate later | It contains their personal data and possibly tokens | Extract the trace, discard the rest (`debug.md`) |

## Write Down What It Was

- **Every crash signature that reached users, its cause and the version that fixed it** is a line in `## Pain Points` of `~/Clawic/data/android/memory.md`; the same signature returns after a refactor and the line saves the whole investigation (`memory-template.md`).
- **Crash-free and ANR rates** go into the release row in `releases/<year>.md`, about 48 hours into the rollout, next to the rollout percentage that produced them.
- **A keep-rule set that fixed a release-only crash** is `artifacts/keep-rules-<name>.md` with its `## Boxes` line — with the reason for each rule, because an unexplained keep rule gets deleted in the next cleanup and the crash comes back.
