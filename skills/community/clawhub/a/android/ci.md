# CI — Building, Signing, and Uploading Automatically

A CI Android build fails for reasons a local build never does: no SDK, no keystore, no KVM, no cache, and a memory limit the JVM cannot see.

**Contents:** [The Minimum Pipeline](#the-minimum-pipeline) · [Caching](#caching) · [Memory in Containers](#memory-in-containers) · [Signing in CI](#signing-in-ci) · [Emulators in CI](#emulators-in-ci) · [Uploading to the Store](#uploading-to-the-store) · [What to Run on What](#what-to-run-on-what) · [Build Times](#build-times) · [CI Traps](#ci-traps)

Written in the dialect of `ci_platform`; the mechanics below are the same on every runner. Pipeline architecture beyond the Android specifics belongs to `ci-cd`.

**Before changing the pipeline**, read `## Toolchain` and `## Build Health` in `~/Clawic/data/android/memory.md`: the JDK and AGP versions CI must match, and the last recorded CI build time.

## The Minimum Pipeline

On every pull request, in one job unless build time forces a split:

1. Check out with enough history for the version scheme to work (a shallow clone breaks any tag-derived version).
2. Set up the JDK that matches AGP (SKILL.md Rule 2) — the runner's default JDK is not it.
3. Restore the Gradle cache.
4. Assemble the debug variant, run lint, run local unit tests.
5. **Assemble the release variant.** This is the step teams skip and the reason R8 breakage reaches production (`release.md`).
6. Publish test results and the lint report as artifacts, so a failure is readable without re-running.

On the release branch or tag, additionally: build the signed bundle, run the instrumented smoke test, upload to the internal track, and write the release row.

## Caching

- Cache the Gradle **user home** dependency cache and the Gradle build cache; do not cache the project's build output directory, which is large, invalid across commits, and a frequent cause of "impossible" build failures.
- Key the cache on the dependency lock inputs — the version catalog, wrapper properties and build files — and restore with a fallback key so a small change does not discard everything.
- The remote build cache is the largest available win for a multi-module project: one machine's task output serves everyone. It needs a shared backend and reliably-cacheable tasks (`gradle.md`).
- A cache is not free: restoring a large cache can cost more than the work it saves on a small project. Measure both ways before assuming.
- Never cache signing material or a decoded keystore. Caches are artifacts and artifacts get downloaded.

## Memory in Containers

- The Gradle JVM, the Kotlin daemon and any test JVM each have their own heap, and their **sum plus overhead must fit inside the container's memory limit**. When it does not, the container kills the process and the build fails with no error message at all — the single most confusing CI failure in Android.
- Symptoms of the container OOM: the job dies mid-compile, the log stops abruptly, or the runner reports a non-zero exit with nothing above it. Symptoms of a JVM OOM: an actual `OutOfMemoryError` with a heap or metaspace name.
- Set the Gradle heap and the Kotlin daemon heap explicitly in CI rather than inheriting a local `gradle.properties` written for a 32 GB laptop.
- Parallel execution multiplies memory use by the number of workers. On a small runner, fewer workers with more memory each finishes faster than many workers thrashing.

## Signing in CI

- The keystore reaches the runner as an encoded secret, is decoded to a temporary file at the start of the job, and the file is deleted at the end. The passwords arrive as separate secrets and are passed to Gradle as properties or environment variables, never on a command line, which is visible in process lists and sometimes in logs.
- The store service account credential is the second secret, needed only by the upload step (`play-console.md`).
- In this skill's memory files, all four are pointers: `env:ANDROID_KEYSTORE_BASE64`, `env:ANDROID_KEYSTORE_PASSWORD`, `env:ANDROID_KEY_PASSWORD`, `env:PLAY_SERVICE_ACCOUNT_JSON`. The values live in the CI platform's secret store and nowhere else (`memory-template.md`).
- Guard against leakage: never echo the decoded values, never run the build with a flag that dumps all properties, and remember that a build scan can publish environment details. Rotate anything that appears in a log, immediately.
- Pull requests from forks must not have access to signing secrets. Restrict the signed build to trusted branches, and let fork builds produce an unsigned debug artifact.

## Emulators in CI

- Instrumented tests need hardware acceleration. Without nested virtualization available on the runner, an emulator either refuses to start or runs so slowly that the suite times out.
- Use an x86_64 system image with acceleration, headless, with animations disabled and the boot completion actually awaited — most emulator flakiness in CI is a test suite starting before the device finished booting (`testing.md`).
- Gradle managed devices let the build own the emulator definition, so CI and developers run the same image with the same settings.
- Prefer a small, fixed API-level matrix over the full range: the oldest supported level, one middle level, and the newest. A matrix of eight levels quadruples cost and finds almost nothing the three do not.
- Cache the emulator snapshot when the runner supports it — boot time dominates a short suite.
- When acceleration is unavailable, a hosted device farm is the honest alternative; a slow software-emulated device produces timeouts that get mistaken for product bugs.

## Uploading to the Store

- The upload uses a service account with the narrowest role that can publish, authenticated by a JSON key held only as a CI secret.
- Automate the boring parts — upload the bundle, upload the mapping file and native symbols, set the track and the rollout percentage, attach release notes. Keep the *decision* to widen a rollout human (`play-console.md`).
- The mapping upload is the step new pipelines forget, and its absence is invisible until the first crash report arrives unreadable (`crashes.md`).
- Upload to internal testing automatically on the release branch; promote to production manually. An automated production push removes the only natural pause in the process.
- After a successful upload, write the release row — version, code, track, rollout, tag, mapping location — before anyone widens anything (SKILL.md Rule 9).

## What to Run on What

| Trigger | Run |
|---|---|
| Every pull request | Assemble debug + release, lint, unit tests, screenshot tests |
| Every merge to the main branch | The above, plus a signed internal-track build and instrumented smoke tests |
| Release tag | Signed bundle, full instrumented suite, mapping and symbol upload, internal track, release row written |
| Nightly | Full instrumented matrix, dependency-update check, benchmark run if the runner is consistent enough |
| Manual | Promote a track, widen a rollout, halt a rollout |

Nightly is where the expensive, slow and flaky-prone jobs go, so that pull-request feedback stays fast enough that people wait for it.

## Build Times

- Measure the CI clean build with a warm cache and record it in `## Build Health` with the date and the runner size (`memory-template.md`). Without a baseline, "CI got slower" is unfalsifiable.
- The usual causes of a slow CI build, in order: no dependency cache, no build cache, an undersized runner, annotation processing that should be KSP, and running instrumented tests on every pull request.
- A build scan on a slow build names the task that cost the time in one look — far faster than reading a log.
- Set a budget and treat crossing it as a defect. Pipeline time is paid by every engineer on every change, and it degrades one commit at a time.

## CI Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Only building debug in CI | R8 and resource shrinking breakage ships to users | Assemble release on every pull request |
| Inheriting a laptop's `gradle.properties` memory settings | Container OOM with no error message | Set heaps explicitly for CI |
| Caching the project build directory | Stale outputs across commits produce impossible failures | Cache the Gradle caches only |
| A keystore committed "temporarily" | Irreversible; the key must be rotated | Encoded secret, decoded at job start, deleted at the end |
| Signing secrets available to fork pull requests | Anyone can exfiltrate them with a one-line change | Restrict signed builds to trusted branches |
| Passing passwords on the command line | Visible in process lists and sometimes in logs | Environment variables or Gradle properties |
| Forgetting the mapping upload | Crash reports are unreadable and nobody notices until an incident | Automate it in the same job as the bundle upload |
| An emulator job without hardware acceleration | Timeouts that look like product bugs | Accelerated x86_64 images, or a device farm |
| A full API-level matrix on every pull request | Cost and time for almost no additional signal | Three levels; the full matrix nightly |
| Fully automated production rollout | Removes the last human check before every user gets it | Automate to internal; promote manually |

## Write Down What It Was

- **The CI toolchain** — runner image, JDK, heap settings, cache strategy — belongs in `## Toolchain` of `~/Clawic/data/android/memory.md`, because it must stay aligned with the local set and is re-derived painfully after a runner upgrade (`memory-template.md`).
- **CI build times** go to `## Build Health` with the date and runner size, and to `benchmarks/<year>.md` when tracked as a series.
- **Secrets are pointers only**: `env:ANDROID_KEYSTORE_BASE64` and its siblings, never the values, in any file under `~/Clawic/data/`.
- **A pipeline failure whose cause was environmental** (a container OOM, a missing accelerator, an expired service account) is a line in `## Pain Points`; it recurs on the next runner upgrade.
