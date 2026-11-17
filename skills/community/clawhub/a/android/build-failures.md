# Build Failures — Error String to Cause

Android build errors are a small, repeating set wearing different stack traces. Match the string, not the stack.

**Contents:** [Read the Failure Correctly](#read-the-failure-correctly) · [Dependency Conflicts](#dependency-conflicts) · [Manifest Merger](#manifest-merger) · [Resource and Linking Errors](#resource-and-linking-errors) · [Dex and Method Count](#dex-and-method-count) · [Kotlin, KSP and kapt](#kotlin-ksp-and-kapt) · [JDK and AGP Mismatch](#jdk-and-agp-mismatch) · [Works in the IDE, Fails on the Command Line](#works-in-the-ide-fails-on-the-command-line) · [Release-Only Build Failures](#release-only-build-failures) · [When Nothing Matches](#when-nothing-matches)

**Before the first fix**, read `## Toolchain` and `## Pain Points` in `~/Clawic/data/android/memory.md`, and open any `artifacts/runbook-*.md` its `## Boxes` index names for this failure. A version matrix that took an afternoon to align is recorded there, and half of all build failures are the same failure.

## Read the Failure Correctly

- The last line of a Gradle failure is almost never the cause. Read upward to the first `> Task :… FAILED` and the first `Caused by:` — everything below is Gradle explaining that a task failed.
- `--stacktrace` shows where Gradle failed; `--info` shows what it was doing; `--scan` shows which task, how long and with what inputs. Reach for `--info` before `--stacktrace`: the cause is usually a missing input, not a Gradle bug.
- Failures in `:app:process<Variant>Manifest`, `:app:merge<Variant>Resources`, `:app:compile<Variant>Kotlin`, `:app:dexBuilder…` and `:app:minify<Variant>WithR8` are five different subsystems. The task name in the failure tells you which section below to read.
- Non-reproducible failure? Run once with `--rerun-tasks` to rule out stale up-to-date state before touching code.

## Dependency Conflicts

| Symptom | Cause | Fix |
|---|---|---|
| `Duplicate class a.b.C found in modules x and y` | The same library arrives under two coordinates (a rename, or a bundled fat jar) | `./gradlew :app:dependencyInsight --configuration releaseRuntimeClasspath --dependency a.b` finds both paths; exclude the loser at the module that pulls it |
| `NoSuchMethodError` at runtime, build green | Version conflict silently resolved upward or downward, so compile-time and runtime differ | Resolution is "highest wins" by default — pin the version in the catalog and add a `strictly` constraint if a transitive keeps overriding |
| `Failed to resolve: <coordinate>` | Repository order, a missing repository, or an artifact that only exists for another variant | Check `dependencyResolutionManagement` repositories; for a snapshot or private artifact, the repository is missing, not the artifact |
| Two versions of the same AndroidX artifact | Different BOM versions across modules | One BOM version, declared once in the version catalog and imported in every module (Compose BOM does the same job for Compose) |
| Build fine locally, resolution failure in CI | Local `~/.gradle` cache holds an artifact the CI machine cannot fetch | Reproduce with `--refresh-dependencies` and no network shortcuts (`ci.md`) |

Rule: never fix a conflict with a blanket `exclude group:` at the top level. Exclude at the dependency that introduces the loser, so the next person can see which pairing was the problem.

## Manifest Merger

- `Manifest merger failed : Attribute X@Y value=(A) … is also present at [lib] … value=(B)` means two manifests disagree. The merged result and its provenance are written to the merger report under the module's build outputs — read it before editing anything.
- `tools:replace="android:X"` overrides one attribute; `tools:node="remove"` drops an element a library injects. Use the narrowest of the two. A `tools:replace` on `android:label` because a library set one is normal; a `tools:node="replace"` on `<application>` is a decision to own everything the library declared, including permissions.
- Libraries inject permissions, providers and receivers silently. After adding an SDK, diff the merged manifest — an unexpected `QUERY_ALL_PACKAGES` or a background-location permission arriving from a dependency is both a Play rejection and a privacy problem (`play-console.md`).
- `minSdkVersion X cannot be smaller than version Y declared in library` is not negotiable by manifest edits: either raise `min_sdk` or drop the library. `tools:overrideLibrary` compiles and then crashes on the devices the library excluded.

## Resource and Linking Errors

- `Android resource linking failed` always names a file and a line. The two common causes: an attribute or style parent that does not exist at this `compileSdk` (raise compileSdk, which is safe — behavior follows `targetSdk`, not compileSdk), or a typo'd resource reference in a merged library resource.
- `resource android:attr/lStar not found` and its relatives are the classic "compileSdk too low for the AndroidX version you just upgraded" signature.
- Duplicate resources across modules resolve by module priority, silently. A library's `colors.xml` overriding yours is a resource-naming problem: prefix module resources (`core_ui_`, `feature_jobs_`) and the collision cannot happen.
- Vector drawable attributes added in later platform versions fail to link against an older compileSdk; the fix is compileSdk, never removing the attribute.

## Dex and Method Count

- `Cannot fit requested classes in a single dex file (# methods: 70000 > 65536)` — the 64K limit is per dex file, not per app. Multidex is automatic when `minSdk >= 21`; if this error appears with a modern minSdk, the build is in a configuration where multidex is off, or a legacy multidex path is in use.
- The durable fix is fewer methods: run R8 on the variant that fails, and check what a single dependency costs before adding it. A method count that grew 20% in one commit names the dependency that arrived in that commit.
- Legacy multidex (`minSdk < 21`) has a real cost: a slower cold start and `MultiDexApplication` initialization before anything else runs. It is one of the reasons `min_sdk` below 21 is a tax, not a preference (SKILL.md Rule 3).

## Kotlin, KSP and kapt

- `Inconsistent JVM-target compatibility` — Java and Kotlin compile tasks disagree on the JVM target. Set both from one place (the JVM toolchain), never one in `compileOptions` and the other in `kotlinOptions`.
- KSP version is bound to the Kotlin version by an explicit suffix: a Kotlin upgrade with a stale KSP fails immediately with a version-mismatch message. Move Kotlin and KSP together, always.
- kapt is slower than KSP and generates Java stubs for every annotated file; a library with a KSP processor should be migrated. A kapt failure that mentions a stub is usually a Kotlin compilation error hidden by stub generation — fix the underlying compile error first.
- `Unresolved reference` for generated code (Hilt components, Room DAOs, view bindings) is almost never the reference: the annotation processor failed earlier in the log. Scroll up.
- A Compose compiler mismatch reports itself as an incompatible-version error at configuration time. From Kotlin 2.0 the Compose compiler moves with the Kotlin plugin, which removes the pairing but makes Kotlin upgrades gate Compose upgrades.

## JDK and AGP Mismatch

| Error | Meaning |
|---|---|
| `Unsupported class file major version 6x` | Gradle or a plugin is running on a JDK newer than it supports |
| `Unable to make field private final java.lang.String java.io.File.path accessible` | A Gradle version older than the JDK's module restrictions, running on JDK 16+ |
| `Android Gradle plugin requires Java 17 to run. You are currently using Java 11.` | Exactly what it says: `AGP >=8` needs JDK 17 |
| `invalid source release: 17` | The toolchain compiles at a level the running JDK does not support |

The JDK that matters is the one Gradle runs on, which is not necessarily the IDE's setting or the shell's `java -version`. Pin it with a Gradle JVM toolchain so the CLI, the IDE and CI agree — a build that only works in Android Studio is this, nine times out of ten.

## Works in the IDE, Fails on the Command Line

Check in this order; each is a one-minute test:

| Difference | Check |
|---|---|
| Different JDK | The IDE's Gradle JDK setting versus the JDK on `PATH` |
| Different Gradle | The IDE may use its bundled distribution instead of the wrapper — always build with `./gradlew` |
| Stale IDE state | The IDE holds generated sources the CLI regenerates; `./gradlew clean` on the CLI side only |
| Environment variables | Signing properties or SDK paths exported in a shell profile the IDE never loaded |
| Different variant | The IDE builds the selected variant; the CLI task you typed may be another one |
| Case-sensitive filesystem | A package or resource name whose case differs only matters on Linux CI |

## Release-Only Build Failures

- R8 failures name a missing class or a rule file. `-printusage` and the R8 configuration dump under the build outputs show what was removed and which rule kept what. Add the narrowest keep rule, then rebuild the release variant — verifying on debug proves nothing (`release.md`).
- A `Missing classes detected while running R8` message lists classes referenced but absent, usually optional dependencies of a library. The generated `missing_rules.txt` is a starting point, not an answer: adding all of it silences the diagnostic and keeps the bloat.
- Resource shrinking removes resources reached only by name. `Resources$NotFoundException` in release is the signature; keep them with a resource-keep rule rather than disabling shrinking.
- A signing failure in release (`Keystore was tampered with, or password was incorrect`) is a wrong password or a wrong keystore, not a corrupted file — verify against the pointer in `## Release Setup` of `memory.md`, never by pasting a password into a build file.

## When Nothing Matches

1. `./gradlew clean` then rebuild once. If that fixes it, the cause was stale state, and that is worth one line in `## Pain Points` because it will happen again.
2. Bisect the change, not the code: `git stash` the working tree, confirm green, then reapply in halves.
3. Bisect the toolchain: revert the single version that moved most recently (Rule 2 says one axis at a time precisely so this bisect is possible).
4. Delete the Gradle caches for the failing artifact only, never the whole `~/.gradle` — a full cache wipe turns a five-minute problem into a thirty-minute download and destroys the evidence.
5. Reproduce on a clean checkout in a new directory. A failure that does not reproduce there is local state, and the fix is to find which file, not to keep building.

## Write Down What It Was

A build failure that took more than a couple of minutes to explain is worth more than its fix (`memory-template.md`):

- **One line in `## Pain Points`** of `~/Clawic/data/android/memory.md`: date, the error string, the actual cause, what changed.
- **A version set that finally built green** goes to `## Toolchain` instead, with the one-line reason any obvious upgrade is blocked — that is the section that stops the next session re-deriving the matrix.
- **The second time the same failure appears**, it becomes `artifacts/runbook-<symptom>.md`: the ordered checks and the fix, with its `## Boxes` line naming the error string as the read condition.
