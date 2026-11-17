# Performance — Startup, Jank, Size, Memory, Battery

Four separate budgets with four separate tools. Optimizing without measuring on a release build, on a slow device, produces confident nonsense.

**Contents:** [Measure Before Anything](#measure-before-anything) · [Startup](#startup) · [Baseline Profiles](#baseline-profiles) · [Jank](#jank) · [App Size](#app-size) · [Memory](#memory) · [Battery](#battery) · [The Benchmark Discipline](#the-benchmark-discipline) · [Performance Traps](#performance-traps)

**Before claiming anything improved**, read `benchmarks/<year>.md` if the `## Boxes` index in `~/Clawic/data/android/memory.md` names it: a performance claim without the previous number on the same device and build variant is not a claim. Budgets come from `cold_start_budget_ms` and `size_budget_mb`.

## Measure Before Anything

Three rules that decide whether the numbers mean anything:

1. **Release build, minified, with the baseline profile installed.** A debug build has no R8, extra checks, and different Compose behavior; its numbers do not correlate with users'.
2. **A slow device.** A flagship hides everything. A mid-range or low-end device from a couple of generations back is where the users are, and where regressions are visible.
3. **Several iterations, and report the median with the spread.** A single run measures the thermal state of the device as much as the app.

Then measure the right thing: macrobenchmarks for startup and scrolling from outside the app, microbenchmarks for a specific hot function, and a system trace when you need to see *why* rather than *how much*.

## Startup

- Three kinds, and they are different problems: **cold** (process created), **warm** (process alive, activity recreated), **hot** (activity resumed). Cold is the one users judge and the one every measurement should default to.
- Measure with the activity-manager's start command, which reports total time, or with a macrobenchmark, which reports time-to-initial-display and time-to-full-display across iterations. Call `reportFullyDrawn()` when the screen has real content, or the framework only ever knows about the first frame — which is often a spinner.
- The cold-start budget in `config.yaml` is a quality target. Play's own bad-behavior line for a slow cold start sits several seconds higher, and hitting only that means shipping something users experience as sluggish.
- Where the time actually goes, in order of how often it is the answer:

| Cost | Why | Fix |
|---|---|---|
| Eager initialization in `Application.onCreate` | Every SDK's "call this at startup" adds up, on the main thread | Lazy initialization, or the app-startup initializer with explicit ordering; measure each one's cost |
| Content providers from dependencies | Libraries auto-initialize through a provider before your `Application` even runs | Disable the auto-init provider in the manifest and initialize explicitly, where you can measure it |
| No baseline profile | Code is interpreted or JIT-compiled on first run | Ship a profile (below) |
| Disk I/O on the critical path | A preferences load or database open before the first frame | Move off the critical path, render with defaults (`data.md`) |
| A heavy first layout | Deep hierarchies, a large list built synchronously | Simplify the first screen specifically |
| A splash activity plus the system splash | Two screens, and the platform's own splash always shows first | Use the platform splash API; delete the custom one |

## Baseline Profiles

- An app ships as bytecode that the runtime interprets or JIT-compiles on first execution. A baseline profile lists the classes and methods on the critical paths, and they get compiled ahead of time at install — so first-run startup and first-scroll jank improve without changing a line of app code.
- Reported improvements are in the tens of percent for startup on real apps, and Compose benefits more than the View system because so much of the UI is library code executing on first frame.
- Generate the profile from a macrobenchmark that exercises startup and the main scrolling screens; it is a build artifact, not a hand-written file.
- **Regenerate when the UI changes materially.** A profile that describes last year's screens is dead weight. That is a `## Due` cadence, not a memory (`memory-template.md`).
- Verify the profile actually installed — a profile in the artifact that was not compiled at install gives none of the benefit, and the benchmark on a device with the profile installed versus not is the only proof.

## Jank

- A frame must be produced within the display's refresh period: 16.67 ms at 60 Hz, 8.33 ms at 120 Hz. Miss it and the previous frame stays on screen — the visible stutter. Frames dropped ≈ `work_ms ÷ frame_budget_ms` (SKILL.md Rule 5).
- Measure with frame statistics from the graphics dump, or with a macrobenchmark that reports frame durations across a scroll. "It feels smooth" on a flagship is not a measurement.
- The causes, in rough order of frequency: work on the main thread during scroll (parsing, formatting, database access), layout that is too deep or measured twice, oversized bitmaps decoded during scroll, recomposition of a whole subtree per frame (`compose.md`), and allocation churn causing GC pauses (`views.md`).
- A system trace shows which of those it is. Reading a trace: find the long frame, look at what the main thread was doing inside it, and check whether the work was scheduled by your code or by the framework responding to it.
- 120 Hz devices halve the budget, so an app that is marginal at 60 Hz is visibly janky on a high-refresh screen. Test on one.

## App Size

- Ship an app bundle and let the store deliver per-device splits: a user downloads one architecture, one screen density and their languages instead of all of them. This is usually the single largest reduction available and costs nothing but the format.
- Inspect the actual artifact with the APK analyzer: it shows what each part contributes, and the answer is almost always resources and native libraries, not code.
- Reduction ladder, by typical return: per-device splits → R8 with resource shrinking → dropping unused languages and densities → modern image formats and correctly sized assets → removing a heavyweight dependency → on-demand feature or asset delivery for the genuinely large parts.
- Watch the *download* size and the *installed* size separately; users see the first before installing and the second when they run out of storage.
- `size_budget_mb` is the trigger for this work. Record each measured size in `benchmarks/<year>.md` so a regression is visible in the release it arrived in, not a year later.

## Memory

- A bitmap costs width × height × 4 bytes decoded in the default configuration, regardless of the compressed file size: a 4000 × 3000 photo is roughly 48 MB. Always decode to the display size, and let an image library manage the cache.
- The heap limit is per-device and modest; `largeHeap` raises it and is almost always the wrong answer — it delays the OOM and makes the app a bigger target for the low-memory killer.
- Leaks are a different problem from usage: memory that grows and never returns after leaving a screen is a leak (`debug.md`); memory that is genuinely needed is a caching or decoding decision.
- Respond to `onTrimMemory` by dropping caches at the more severe levels. An app that never releases anything gets killed in the background, which the user experiences as the app "restarting" every time they switch back.
- Measure with the profiler or the meminfo dump. The number that matters for being killed is the proportional set size, not the Java heap alone — native allocations from image and video libraries do not appear in the heap.

## Battery

- The expensive operations are radio wakeups, GPS, sustained CPU and keeping the screen on. Everything else rounds to zero next to them.
- Batch and defer: WorkManager with constraints exists so the system can align your work with other apps' wakeups instead of waking the radio separately (`background.md`).
- Wakelocks must be released on every path, including exceptions, and must have a timeout. A leaked wakelock drains a battery overnight and is attributed to your app in the system's battery report, where the user sees it.
- Location: request the coarsest accuracy that works and the longest interval acceptable. Continuous high-accuracy location is the largest battery cost an app can inflict short of the screen.
- Measure with a battery-usage report after a controlled session rather than by intuition — the intuitive answer is usually the CPU, and the real answer is usually the radio.

## The Benchmark Discipline

- One benchmark harness, checked into the repository, run on the same device before and after. A number from a different device, or from a debug build, is not a comparison.
- Record every measurement in `benchmarks/<year>.md` with the date, device name (matching the shared inventory), build variant and whether a baseline profile was installed. A number without those columns cannot be compared to anything (`memory-template.md`).
- Run the benchmark in CI on a consistent device or emulator when the budget allows: performance regressions are found weeks late otherwise, when the cause is no longer obvious (`ci.md`).
- Set the budget once, in `config.yaml`, and treat crossing it as a bug with an owner rather than a topic for discussion.

## Performance Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Benchmarking a debug build | No R8, extra checks, different Compose behavior | Release variant with the profile installed |
| Optimizing on a flagship | Hides every problem the users have | A mid-range or older device |
| A single timing run | Measures thermal state as much as code | Several iterations, median plus spread |
| `largeHeap="true"` | Delays the OOM and makes the process a bigger kill target | Fix the allocation; decode images to size |
| Decoding full-resolution images | Tens of megabytes per photo | Decode to the display size |
| A custom splash activity | The platform splash shows first, so users see two | The splash API |
| Adding a dependency without checking its cost | Startup and size regress silently, one library at a time | Measure startup and size before and after |
| A baseline profile generated once | Describes screens that no longer exist | Regenerate on a `## Due` cadence |
| Chasing GC in the profiler without a jank measurement | Allocation is not automatically a problem | Start from a dropped frame and work back |
| Reporting "it feels faster" | Not falsifiable, and usually wrong | A number, on a device, in `benchmarks/<year>.md` |

## Write Down What It Was

- **Every measurement** — cold start, jank, download size, build time — goes to `benchmarks/<year>.md` with its date, device, build variant and profile state (`memory-template.md`). The series is the only thing that makes the next claim checkable.
- **A number tied to a release** goes into that release's row in `releases/<year>.md` instead, so a regression is attributable to the version that shipped it.
- **A performance decision with a cost** — dropping a dependency, moving to on-demand delivery, accepting a slower cold start for a feature — is an `artifacts/adr-<name>.md` with its `## Boxes` line.
- **The baseline-profile regeneration cadence** is a row in `## Due`.
