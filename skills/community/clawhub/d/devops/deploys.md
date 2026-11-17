# Deploys — Getting A Change In Front Of Users, Reversibly

Scope: the act of releasing and the ability to undo it. Reconciliation-based delivery is `gitops.md`; environment topology is `environments.md`; data changes are `migrations.md`.

**Before any deploy or rollback**, read `releases/<year>.md` if `## Boxes` points there — the previous artifact identity you would roll back to lives in that file and nowhere else — plus `## Services` in `~/Clawic/data/devops/memory.md` for the strategy, the target, and the owner of that service. **Check `## Due`** for an overdue drill or rotation that this deploy depends on.

**Contents:** [The Deploy Contract](#the-deploy-contract) · [Choosing The Strategy](#choosing-the-strategy) · [Canary Sizing](#canary-sizing) · [Rollback Decision](#rollback-decision) · [Feature Flags](#feature-flags) · [Deploy Gates Worth Having](#deploy-gates-worth-having) · [Deploy-Time Failure Modes](#deploy-time-failure-modes)

## The Deploy Contract

Every deploy answers these before it starts. Missing answers are the outage.

| Question | Acceptable answer |
|---|---|
| What exactly is being deployed? | An artifact identity — digest or immutable version stamped by `version_scheme` |
| What is running now? | The same kind of identity, read from the target, not from the pipeline's memory |
| How do we undo it? | Deploy the previous identity; the command is written down before the deploy starts |
| What can we not undo? | Migrations past the contract step, irreversible writes, third-party side effects, emails sent |
| What tells us it went wrong? | A named SLI and its threshold, evaluated over a window shorter than the bake time |
| Who is watching? | A person, for a stated duration, not "the team" |

The last two make the difference between a deploy and a bet. Write the release row (date, service, identity, strategy, rollback target, result) in `releases/<year>.md` in the same turn (`memory-template.md`).

## Choosing The Strategy

The table in SKILL.md picks the default; these are the conditions that override it.

- **Rolling** requires the old and new versions to coexist: the API must be backward compatible for the length of the window, and so must the schema (`migrations.md`). Set `maxUnavailable`-style limits so a broken image cannot take the whole fleet, and gate each batch on health, not on start.
- **Blue-green** doubles capacity for the switch window. Its trap is shared state: both colors read and write the same database, so a schema change is still expand/contract, and any in-flight session or long-lived connection must drain or be re-established. Keep the old color warm for the agreed rollback window before reclaiming it.
- **Canary** needs per-cohort metrics. Comparing canary error rate against the overall average is self-defeating: the canary's own traffic is inside the average, and cohort skew (canary gets sticky-routed heavy users) invalidates the comparison. Compare canary against the control slice over the same window.
- **Recreate** is honest when downtime is cheap: for an internal tool a 40-second gap costs less than the machinery to avoid it.
- **Shadow traffic** (mirror requests to the new version, discard responses) tests capacity and correctness with zero user exposure — and doubles downstream load, so mirrored writes must be disabled or routed to a scratch store.

## Canary Sizing

Rule of three: with zero failures observed in `n` requests, the 95% upper bound on the true failure rate is ≈ `3/n`. Inverted: to be reasonably confident a regression above rate `r` would have shown up, the canary must serve at least `3/r` requests.

| Regression you must catch | Requests needed | At 100 req/s, 1% canary | At 10 req/s, 10% canary |
|---|---|---|---|
| 1% of requests | ~300 | ~5 min | ~5 min |
| 0.1% | ~3,000 | ~50 min | ~50 min |
| 0.01% | ~30,000 | ~8 h | ~8 h |

Consequences: a service under ~10 req/s cannot canary a small regression in a reasonable window — use blue-green with a fast flip instead. And bake time must exceed the slowest signal in the decision: a 5-minute alert window means a minimum 5-minute bake, plus the metric pipeline's own lag (often 1-2 min).

Ramp shape: 1% → 10% → 50% → 100%, each step held for at least a full bake window, with an automatic halt if the canary SLI breaches. Latency regressions need percentile comparison (p95/p99), not averages — an average hides a 5% cohort at 10× latency.

## Rollback Decision

SKILL.md Rule 2 gives the trigger; this is the procedure.

1. **Stabilize first.** Roll back, shift traffic, or disable the flag before diagnosing. Diagnosis on a burning system takes longer and costs the budget.
2. **Check the migration state.** If the change's migration is past the contract step, rollback of code alone corrupts data — roll forward with a fix, and say so explicitly in the incident channel.
3. **Deploy the recorded identity**, not "the previous tag" — movable tags have already moved.
4. **Verify by reading the target**, not the deploy tool's success message. Confirm the identity actually serving traffic and the SLI recovering.
5. **Write the row**: what was rolled back, to which identity, why, and how long it took. That duration is your time-to-restore metric (`platform.md`) and it is the number that makes the next investment argument.

Automated rollback earns its place when the canary signal is trustworthy: bind it to the SLI, require two consecutive breaching windows to avoid flapping, and cap it at one automatic rollback per release — a loop that redeploys and reverts repeatedly is worse than either state.

## Feature Flags

Deploy and release become separate events; the cost is a permanent branch in your code and your test matrix.

- **Kill switch first.** Any flag guarding a risky path must be flippable without a deploy, by whoever is on call, and documented in the runbook.
- **Sticky bucketing** by a stable user id — random per-request assignment makes a percentage rollout produce inconsistent experiences and unreproducible bugs.
- **Every flag gets a removal date** at creation, tracked in `## Due`. Flag debt compounds: `n` live flags mean up to `2^n` code paths and no test suite covers them.
- **Default off, fail closed** for anything touching money or data; default on, fail open for cosmetic changes. State the failure behavior when the flag service is unreachable — that unreachability is itself an outage mode.
- Flags are not access control and not secrets: the client can see them.

## Deploy Gates Worth Having

Each gate costs lead time; keep the ones that catch real failures. `approval_gate` sets where a human sits.

| Gate | Catches | Cost |
|---|---|---|
| Health check post-deploy, before traffic | Broken image, bad config, missing dependency | Seconds; mandatory |
| Smoke test against the deployed artifact | "Builds fine, missing runtime dep" | 1-2 min; high value |
| Canary bake with SLI comparison | Regressions that only appear under real traffic | Minutes to hours; needed at scale |
| Human approval | Judgment calls, coordination, compliance evidence | Hours of lead time — worth it only where a person genuinely decides something |
| Change freeze window | Nothing, on its own | Batches risk (SKILL.md Rule 3); use only for genuine external constraints |

A gate that nobody has ever failed is measuring nothing — either the check is wrong or the gate is theater. Review gates whenever change failure rate moves.

**Write in the same turn**: every release, promotion, and rollback gets its row in `~/Clawic/data/devops/releases/<year>.md` with the artifact identity and the rollback target (SKILL.md Rule 2). A strategy change or a new deploy target updates the service's row in `## Services` of `memory.md`. A deploy plan or runbook worth re-reading — a cutover, a first blue-green switch, a flag rollout procedure — becomes `artifacts/<kebab-name>.md` with its `## Boxes` line (`memory-template.md`).
