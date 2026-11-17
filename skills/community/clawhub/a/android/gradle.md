# Gradle — Build System, Dependencies, and Build Speed

The Android build is a Gradle build with one very opinionated plugin on top. Most build pain is configuration pain, and it is measurable before it is fixable.

**Contents:** [The Version Catalog Is the Single Source](#the-version-catalog-is-the-single-source) · [Build Speed: Measure, Then Fix](#build-speed-measure-then-fix) · [Configuration Cache](#configuration-cache) · [Dependency Resolution](#dependency-resolution) · [Variants, Flavors and Build Types](#variants-flavors-and-build-types) · [Modularization](#modularization) · [Convention Plugins Over Copy-Paste](#convention-plugins-over-copy-paste) · [JVM Memory and Daemons](#jvm-memory-and-daemons) · [Build Logic Traps](#build-logic-traps)

**Before changing build configuration**, read `## Toolchain`, `## Modules` and `## Build Health` in `~/Clawic/data/android/memory.md`: the aligned version set, the module graph, and the last measured clean and incremental times. Optimizing a build without the previous numbers produces an opinion, not an improvement.

## The Version Catalog Is the Single Source

- `gradle/libs.versions.toml` holds every version, library and plugin alias. A version that appears in a `build.gradle` file is a version that will be forgotten during the next upgrade.
- Group versions that must move together under one key: `kotlin` drives the Kotlin plugin, KSP's prefix, and (from Kotlin 2.0) the Compose compiler. `composeBom` drives every Compose artifact — declare Compose libraries without versions and let the BOM decide.
- Bundles (`libs.bundles.compose`) keep module files short; plugin aliases keep the plugins block declarative and let a single upgrade touch one line.
- `build_language` decides the dialect. Kotlin DSL gets type-safe catalog accessors and IDE completion at the cost of slower first configuration; Groovy configures marginally faster and offers no help when a property name is wrong.

## Build Speed: Measure, Then Fix

Two numbers matter, and they are different problems:

- **Clean build time** — CI's cost. Dominated by the number of modules, annotation processing, and R8 in release.
- **Incremental (edit-one-file) time** — the developer's cost. Dominated by how much the module graph forces to recompile.

Measure with `./gradlew --profile` or a build scan, and take the median of three runs. Then fix in this order, because the earlier items are free and the later ones are work:

| Fix | Typical effect | Cost |
|---|---|---|
| Configuration cache on | Removes configuration time (often 1-5 s) from every invocation | Build-logic changes may be required |
| Build cache on (`org.gradle.caching=true`) | Unchanged tasks restored instead of re-run; largest effect in CI with a remote cache | Needs cacheable tasks |
| Parallel execution (`org.gradle.parallel=true`) | Scales with independent modules; nothing on a single module | None |
| Adequate JVM heap | Removes GC thrash and OOM retries | Memory on the machine |
| kapt → KSP | Removes Java stub generation for annotated files; the single largest win in heavily annotated codebases | Migration per processor |
| `implementation` instead of `api` | Cuts recompilation cascade: an `api` dependency change recompiles every consumer, transitively | Discipline |
| Module split by feature | Parallelism plus a smaller recompile blast radius | Real plumbing (see below) |
| Non-transitive R classes | Smaller R classes, faster resource processing | Fully-qualified resource references |

Rule of thumb for whether a split is worth it: if editing one file in the largest module rebuilds more than about half the codebase, the module boundary is missing. If it does not, the module count is not your problem.

## Configuration Cache

- It caches the *configuration phase* result, keyed by build inputs. The first run pays; every later run with the same inputs skips straight to execution.
- It fails loudly on build logic that reads project state at execution time — `project.` references inside task actions, `System.getenv` at the wrong phase, un-serializable task fields. That failure is the feature: the same patterns break parallelism and incrementality silently.
- Fix by injecting values at configuration time into task inputs (`Provider`, `@Input`, `ValueSource`), not by disabling the cache. A build that opts out is a build that opted out of every future improvement in this area too.
- `--configuration-cache-problems=warn` is for the migration, not for the steady state.

## Dependency Resolution

- Default resolution is **highest version wins** across the graph, per configuration. That means the version you declared is a floor, not a fact.
- `./gradlew :app:dependencyInsight --configuration releaseRuntimeClasspath --dependency <group:artifact>` answers "why this version" and "who pulled it in". `./gradlew :app:dependencies` gives the whole tree, which is only readable when you already know what you are looking for.
- To force a version, prefer a constraint with `strictly` over `resolutionStrategy.force`: the constraint fails the build when something requires an incompatible version, instead of silently downgrading it.
- Configurations, precisely: `implementation` (not exposed to consumers), `api` (exposed, and therefore recompiles consumers), `compileOnly` (compile classpath only, absent at runtime — the correct choice for annotations), `runtimeOnly`, `testImplementation`, `androidTestImplementation`, `debugImplementation` (the right home for a leak detector or a debug database inspector).
- Lock or at least pin anything that must be reproducible in CI. A dynamic version (`1.+`, `latest.release`) makes a green build unreproducible tomorrow, which is the same class of problem as an unpinned container tag.

## Variants, Flavors and Build Types

- Build types answer "how is it built" (debug, release, benchmark); product flavors answer "which product is it" (free/paid, staging/prod, per-client white labels). Variants are the cross product, and the count grows multiplicatively — three flavors × three build types is nine variants of every task.
- A `benchmark` build type is the standard third one: release-like (minified, shrunk) but signed with the debug key and debuggable-adjacent settings off, so macrobenchmarks measure something close to what users run (`performance.md`).
- Applications of `applicationIdSuffix` and `versionNameSuffix` on debug builds let a debug and a release build coexist on one device — worth having from day one, because comparing them side by side is a routine debugging move.
- Flavor-specific source sets (`src/free/java`, `src/free/res`) beat runtime `if (BuildConfig.FLAVOR == …)` branching: the unused code is not in the artifact at all.
- Signing configuration for release never lives in a checked-in file. Read it from properties supplied by the environment, with the values themselves stored outside the repository (`release.md`, `ci.md`).

## Modularization

Governed by `module_layout`.

- **single** — one `:app`. Correct for a small app; every change rebuilds everything, and that is cheap while everything is small.
- **by-layer** — `:data`, `:domain`, `:ui`. Enforces direction of dependency, but every feature touches every module, so the incremental win is small.
- **by-feature** — `:feature:jobs`, `:feature:sync`, over shared `:core:*` modules. The layout that actually shortens incremental builds, because a feature change recompiles one feature.
- Direction rule: features depend on core, never on each other; core never depends on a feature. A feature-to-feature dependency is the moment the graph stops being a graph and starts being a knot — route through a shared abstraction in core instead.
- Every module boundary costs a build file, a namespace, dependency plumbing and a slower clean build. Add them against a measured incremental time, and write the resulting module list to `## Modules` in `memory.md` so the next session does not have to re-derive the graph.

## Convention Plugins Over Copy-Paste

- Once there are more than about three modules, identical blocks in every `build.gradle` are the problem. A convention plugin in `build-logic` (an included build) applies compile options, the JVM toolchain, common test setup and shared plugins in one line per module.
- `buildSrc` versus an included `build-logic` build: a change in `buildSrc` invalidates the entire build's configuration, so on a large project `includeBuild("build-logic")` is the better shape. On a small one, `buildSrc` is fine and simpler.
- `subprojects { }` and `allprojects { }` blocks in the root file are the anti-pattern they replace: they defeat configuration-on-demand and make every module's configuration depend on the root.

## JVM Memory and Daemons

- `org.gradle.jvmargs=-Xmx4g` in `gradle.properties` is the common starting point; too small produces GC thrash and `OutOfMemoryError: Metaspace`, too large starves the rest of the machine and, in CI containers, gets the JVM killed by the container limit rather than by Gradle.
- CI memory rule: the Gradle JVM heap plus the Kotlin daemon heap must fit inside the container's memory limit with room to spare — a container OOM presents as a build that dies with no error message at all (`ci.md`).
- The Kotlin compile daemon has its own heap (`kotlin.daemon.jvmargs`). A Gradle heap increase that changed nothing usually means the Kotlin daemon was the one starving.
- Keeping the Gradle daemon alive is the right default locally and, with a warm cache, in most modern CI too. `--no-daemon` is cargo-culted from an era of leak bugs; measure before adopting it, because it forfeits JIT warm-up on every run.

## Build Logic Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Version numbers inline in module files | An upgrade misses one module and two versions ship in one app | Version catalog, always |
| `api` used by default | One library change recompiles the whole graph | `implementation` unless a consumer genuinely needs the type |
| Reading `System.getenv` at execution time | Breaks the configuration cache and makes the task's inputs invisible | Wire it in as a task input at configuration time |
| Dynamic versions (`1.+`) | Yesterday's green build cannot be reproduced today | Pin in the catalog; upgrade deliberately on the `## Due` cadence |
| Disabling the configuration cache to make an error go away | The error is a real ordering bug that will resurface as a flaky CI build | Fix the task's inputs |
| A custom task with no declared inputs and outputs | Never up-to-date, never cacheable, runs on every build forever | Declare `@Input`/`@OutputFile` and mark it cacheable |
| `./gradlew clean` in the normal loop | Discards every incremental and cached result to work around a bug that has a cause | Find the stale-state cause once and write it down |

## Write Down What It Was

- **An aligned version set** — AGP, Gradle, JDK, Kotlin, KSP, Compose BOM — goes to `## Toolchain` in `~/Clawic/data/android/memory.md` the moment it builds green, with the one-line reason any obvious upgrade is blocked (`memory-template.md`).
- **A measured clean or incremental build time** goes to `## Build Health`, with its date and machine, and to `benchmarks/<year>.md` when it is part of a series being tracked. A time without a machine cannot be compared.
- **A module added, removed or renamed** updates `## Modules` in the same turn.
- **A dependency-update cadence** the user accepts becomes a row in `## Due`.
