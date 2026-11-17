# Pipelines — Making CI Fast, Trustworthy, and Cheap

`ci_platform` in `config.yaml` decides the dialect of every example; while it is unset, say which platform you are assuming before writing a pipeline file. A pipeline is judged on three numbers: PR feedback time, false-failure rate, and cost per merge.

**Before changing a pipeline**, read `## Pipeline Health` and `## Services` in `~/Clawic/data/devops/memory.md` (or `services.md` if `## Boxes` points there) — the platform in use, the measured durations, the cache backend, and which suites are quarantined are recorded there.

**Contents:** [Stage Order](#stage-order) · [Where The Time Goes](#where-the-time-goes) · [Caching That Actually Hits](#caching-that-actually-hits) · [Flaky Tests](#flaky-tests) · [Green Locally, Red In CI](#green-locally-red-in-ci) · [Monorepo Selection](#monorepo-selection) · [Runners And Cost](#runners-and-cost) · [Pipeline Security Basics](#pipeline-security-basics)

## Stage Order

Order by catch rate per second of runtime — the cheapest signal that can fail the build runs first (SKILL.md Rule 4).

| Stage | Typical runtime | Catches | Screening rate |
|---|---|---|---|
| Format + lint | 15-60s | Style, obvious type errors, ~10-20% of failures | Highest — always first |
| Unit tests | 1-4 min | Logic regressions, most real failures | High |
| Build / package | 1-5 min | Compile and dependency-resolution breaks | Medium; produces the artifact everything downstream reuses |
| Integration / e2e | 5-30 min | Wiring, contracts, migrations | Low per second — parallelize or move off the PR path |
| Security + license scan | 1-5 min | Known CVEs, forbidden licenses | Runs in parallel with tests, gates the merge |

- **Fail fast, but only on deterministic stages.** An early stage that flakes blocks every PR; a flaky lint rule costs more than the bugs it finds.
- **Build the artifact once per pipeline** and pass it downstream by identity (SKILL.md Rule 1). Two builds in one pipeline means the tested and the shipped artifact can differ.
- Anything above `pipeline_time_budget_min` on the PR path gets parallelized, cached, sharded, or demoted to a merge-queue/nightly run with a named owner watching the results.

## Where The Time Goes

Measure before optimizing: total duration is the wrong number, the critical path is the right one.

| Symptom | Usual cause | Fix |
|---|---|---|
| Every job spends minutes before the first useful line | Dependency install with no cache, or a fat checkout | Cache keyed on the lockfile hash; shallow clone; sparse checkout for monorepos |
| Duration grew slowly over months | Test suite growth with no sharding | Shard by historical timing, not alphabetically — equal-count shards drift to 3× imbalance |
| One job dominates the wall clock | Serial dependency graph | Split independent work into parallel jobs; only the artifact build must precede deploy |
| Fast locally, slow in CI | Smaller runner, cold cache, no reuse of the daemon or the compiler cache | Compare CPU count and memory first; a 2-vCPU runner running a 16-way test suite queues |
| Queue time exceeds run time | Not enough concurrency, or one shared self-hosted runner | Concurrency limits and runner count are the fix; a faster build changes nothing |

Sharding math: with `n` tests of similar duration across `k` shards, wall clock ≈ total/k plus the fixed setup cost paid `k` times. Setup of 90s across 10 shards spends 15 minutes of billed compute to save wall-clock time — worth it on the PR path, wasteful nightly.

## Caching That Actually Hits

- **Key on the lockfile, restore on a prefix.** `deps-${os}-${hash(lockfile)}` with a fallback to `deps-${os}-` gives a warm-but-stale cache instead of a cold one.
- **Never key a cache on the branch alone** for anything a PR can write: a poisoned cache from an untrusted PR is a supply-chain compromise. Caches written by fork PRs must be isolated from the default-branch cache (`supply-chain.md`).
- A cache that is restored but never used costs upload and download time twice. Verify hit rates before adding a second cache layer.
- Build-tool caches (compiler, bundler, test-result) usually beat dependency caches on repeat time — measure both.
- Cache size limits evict silently; a matrix of 12 jobs each writing 2 GB thrashes a 10 GB budget and every run is a miss.

## Flaky Tests

Suite-level math is the argument that wins: with `n` independent tests each failing spuriously with probability `p`, the chance a clean run goes green is `(1−p)^n`. 500 tests at p=0.001 → 60.6% green, so **39% of honest runs fail**. Two flaky tests in a big suite destroy trust in the whole pipeline.

Quarantine protocol:

1. A test that fails ≥1 in 50 runs on unchanged code is flaky, not unlucky. Track re-runs to know this — an auto-retry that hides the count converts flakiness into slow, invisible rot.
2. Quarantine it out of the blocking set the same day, with an owner and an expiry date (a common shape: 14 days) recorded in `## Pipeline Health`.
3. At expiry it is fixed or deleted. A quarantine list that only grows is a test suite that no longer means anything.
4. Blanket `retry: 3` on the whole suite is not a policy — it multiplies runtime and lets genuine 1-in-4 race conditions ship.

Most common real causes, in order: shared mutable fixtures or a shared database between parallel tests; test-order dependence; wall-clock and timezone assumptions; fixed ports or temp paths colliding on a shared runner; async waits tuned to a fast laptop.

## Green Locally, Red In CI

Rank the causes; do not debug randomly.

1. **Architecture** — arm64 laptop, amd64 runner (`docker` for the image side).
2. **Different artifact** — the runner resolved a different dependency version or base image than the lockfile pinned locally.
3. **Environment variables** — present in the shell, absent in CI; or a CI-only variable changing behavior.
4. **Filesystem** — case-insensitive macOS vs case-sensitive Linux; symlinks; file mode bits.
5. **Concurrency and ordering** — CI runs tests in parallel or in a different order.
6. **Network** — the runner has no access to a host the laptop reaches through a VPN, or hits a rate limit behind a shared NAT.

The reverse (red locally, green in CI) is almost always a stale local artifact or a dirty working directory.

## Monorepo Selection

- Change detection is the entire game: build only the projects whose inputs changed, plus their dependents. Without it, every PR pays for every project and the pipeline time budget is unreachable.
- Compute affected sets from the dependency graph, not from directory globs — a shared library edit must trigger its consumers.
- Merge queues matter more here: independently green PRs can break the trunk together. A queue that tests the merged result serially costs wall-clock time and buys a green trunk; batch its testing to keep throughput.
- Keep a periodic full build (nightly is common) so a stale-selection bug surfaces within a day rather than at release.

## Runners And Cost

- Hosted runners cost per minute; self-hosted cost per hour of a machine you already pay for, plus maintenance and a security boundary. Break-even: `hosted_minutes_per_month × price_per_minute` vs `machine_monthly_cost`. Run the arithmetic with real numbers before migrating; include the maintenance hours.
- Self-hosted runners must be ephemeral for untrusted code. A persistent runner executing fork PRs leaks caches, credentials, and state between jobs.
- Bigger runners are the cheapest optimization when the build parallelizes: 4× cores at ~4× the per-minute price is cost-neutral when it cuts wall clock 4×, and it buys back developer wait time for free.
- Cost per merge is a real metric; track it if the CI bill is a line item worth arguing about, and record the monthly figure in the shared `~/Clawic/data/finances/subscriptions.md` (protocol in `memory-template.md`).

## Pipeline Security Basics

- Default token permissions read-only; elevate per job, never per workflow (`secrets.md`).
- Pin third-party actions/plugins by commit SHA, not by a movable tag — a tag can be repointed at new code by whoever owns it.
- Untrusted PR code never runs in a job that holds deploy credentials or writes the shared cache.
- Anything printed is retained: mask secrets, and remember that `set -x`, environment dumps, and test fixtures print them anyway.

**When the pipeline's shape changes** — platform, stages, cache backend, measured PR duration, runner type, or the quarantine list — update `## Pipeline Health` in `~/Clawic/data/devops/memory.md` in the same turn. **When a pipeline file finally works**, save it to `~/Clawic/data/devops/artifacts/<kebab-name>.md` with the reasoning behind each non-obvious step, and add its `## Boxes` line (`memory-template.md`). Every credential in it is a pointer (`env:DEPLOY_TOKEN`), never a value.
