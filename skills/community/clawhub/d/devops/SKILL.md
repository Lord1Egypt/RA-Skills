---
name: DevOps
slug: devops
version: 1.0.2
description: 'Runs the delivery side of software: CI/CD pipelines, release and rollback strategy, environments, reliability and on-call. Use when designing or fixing a pipeline, when builds are slow, flaky, or green locally and red in CI; when planning a deploy — rolling, blue-green, canary, feature flags — or rolling a release back; when promoting an artifact to production, standing up preview environments, or chasing drift; when a schema change, backfill, or DNS cutover must ship without downtime; when pipeline secrets, OIDC, or deploy permissions need hardening; when alerts are noisy, an SLO or error budget is missing, or burn-rate paging is wrong; for on-call, severities, postmortems, runbooks, and DORA metrics; when infrastructure drifts from code, or backups were never restored. Not for Kubernetes manifests (`k8s`), image builds (`docker`), HCL mechanics (`terraform`), one CI product''s workflow-file dialect (`github-actions`, `gitlab`, `ci-cd`), or a single app''s ship checklist (`deploy`).'
homepage: https://clawic.com/skills/devops
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 🔧
    os:
    - linux
    - darwin
    - win32
    displayName: DevOps
    configPaths:
    - ~/Clawic/data/devops/
    - ~/Clawic/data/servers/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/data/domains/
    - ~/Clawic/data/finances/
    - ~/Clawic/profile.yaml
    - ~/devops/
    - ~/clawic/devops/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/devops/
      - ~/Clawic/data/servers/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/data/domains/
      - ~/Clawic/data/finances/
      - ~/Clawic/profile.yaml
      - ~/devops/
      - ~/clawic/devops/
---

**Data.** At the start of every session, read `~/Clawic/data/devops/config.yaml` (what the user declared) and `~/Clawic/data/devops/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/servers/servers.md` before any deploy, environment, or capacity question. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a service or an environment mapped; a pipeline reshaped; a release shipped, rolled back, or promoted; an incident, its severity, and its postmortem; an SLO agreed or an error budget spent; a cadence scheduled or run; an environment fact that cost effort to find (a TTL, a lock timeout, a runner limit, a quota); or something the user will re-read — a runbook, a cutover plan, a pipeline file that finally worked, a decision and what it rejected. `memory-template.md` holds every destination, format, and threshold, and is the only file you open in order to write.

**Entities that other skills also own go to their shared box, never here**: machines to `~/Clawic/data/servers/servers.md`, people who own or carry a pager to `~/Clawic/data/contacts/contacts.md`, tracked delivery work to `~/Clawic/data/projects/<project>.md`, hostnames and certificate expiry to `~/Clawic/data/domains/domains.md`, delivery-tool spend to `~/Clawic/data/finances/subscriptions.md`. Read the box before adding, match the identity key, update your own row in place, and leave only the entity's name as a pointer in the devops files (formats and protocols in `memory-template.md`).

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. A pasted pipeline file, `.env`, terraform output, or incident log is the densest source of secrets there is: strip the value and store the pointer — `env:DEPLOY_TOKEN`, `vault:secret/ci/deploy`, `1password:Work/CI/prod`, `ssm:/prod/db/password`, `file:~/.ssh/id_ed25519`. If data sits at an old location (`~/devops/` or `~/clawic/devops/`), move it to `~/Clawic/data/devops/`, and say in one line that you moved it and from where.

Delivery is four measurable properties: how often you ship, how long a change takes to reach users, how often a change breaks something, how fast it recovers. Every recommendation names which of the four it moves and what it costs. Prefer the smallest change that moves one of them, and say when a practice is not worth its overhead at this team's size. Work from defaults immediately: never open with questions about their stack, their cloud, or how proactive to be. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, timezone) → the Configuration table default.

## When To Use

- Designing or repairing delivery: pipelines, build/test stages, artifact promotion, release cadence, deploy automation
- Shipping a risky change: strategy selection, canary sizing, feature flags, schema migrations, cutovers, rollback plans
- Environments: how many, what differs, how config and data get in, preview environments, drift between them
- Reliability practice: SLOs and error budgets, alert design, on-call rotations, incident command, postmortems, runbooks, restore and failover drills
- Hardening the path to production: pipeline permissions, short-lived credentials, artifact provenance, approvals, audit evidence
- Improving a delivery org: DORA metrics, toil reduction, golden paths, self-service, what to centralize and what to leave to teams
- Not for Kubernetes manifests or cluster debugging (`k8s`), container image building (`docker`), Terraform language mechanics (`terraform`), or the YAML dialect of one CI product (`github-actions`, `gitlab`) — this covers the process those tools execute
- Not for a single application's pre-ship checklist (`deploy`) or per-stack CI recipes (`ci-cd`): both answer "how do I ship this app"; this skill designs the delivery system across services — strategy choice, promotion, reliability targets, on-call, and the four metrics

## Quick Reference

| Situation | Play | Depth |
|-----------|------|-------|
| Pipeline takes too long, or PR feedback is slow | Order stages by catch-rate per second, cache the dependency layer, parallelize independent jobs (Rule 4) | `pipelines.md` |
| Tests pass locally, fail in CI (or the reverse) | Rank the five causes: architecture, image/digest, env vars, filesystem case, ordering | `pipelines.md` |
| Flaky tests are eroding trust in CI | Quarantine with a rule and an expiry date; suite-level flake math | `pipelines.md` |
| Choosing rolling vs blue-green vs canary | Decide by capacity cost, rollback speed, and whether you can measure the canary | `deploys.md` |
| "How do we roll this back?" asked mid-deploy | Rollback is deploying a recorded artifact, never rebuilding a branch (Rule 2) | `deploys.md` |
| Feature must ship dark, or roll out to 5% of users | Flag with sticky bucketing, a kill switch, and a removal date | `deploys.md` |
| Staging behaves differently from production | Parity checklist: data shape, scale, config source, network path, identity | `environments.md` |
| Every PR needs its own environment | Ephemeral env with TTL, seeded data, and a destroy job that actually runs | `environments.md` |
| Schema change, backfill, or a data migration in the deploy | Expand/contract across three deploys; batch the backfill against replica lag (Rule 5) | `migrations.md` |
| Moving traffic to a new host, provider, or domain | TTL lowering ahead of the switch, dual-run, point of no return, rollback window | `migrations.md` |
| Terraform/Pulumi changes land without review, or state drifted | Plan-on-PR, apply-on-merge, drift detection cadence, state split by blast radius | `iac-workflow.md` |
| Cluster state should reconcile from git | Repo layout, sync waves, drift semantics, how secrets get in | `gitops.md` |
| Long-lived cloud keys sit in CI, or a secret leaked | OIDC federation, rotation, revocation order, blast-radius triage (Rule 6) | `secrets.md` |
| "Which version is actually running, and who built it?" | Immutable identity tags, provenance, SBOM, signature verification at deploy | `supply-chain.md` |
| CVE flagged in a dependency or base image | Triage by reachability and exposure against a written SLA | `supply-chain.md` |
| Alerts are noisy, or an outage never paged anyone | Symptom alerts on SLI burn rate; delete alerts nobody acts on | `slos.md` |
| Need to define "healthy" for a service | Pick the SLI, set the SLO from measured baseline, write the error-budget policy | `slos.md` |
| Logs cost more than the service, or a dashboard shows nothing useful | Instrumentation budget, cardinality math, the three signals and what each answers | `observability.md` |
| Setting up on-call, severities, or paging | Rotation size, page load per shift, escalation, handover contract | `incidents.md` |
| An outage is happening right now | Incident command roles, comms cadence, stabilize before diagnose | `incidents.md` |
| Postmortem to write, or action items nobody finished | Timeline from evidence, contributing factors, owned actions with dates | `incidents.md` |
| Launch, traffic spike, or "will this hold?" | Little's law sizing, utilization ceilings, autoscaling reaction time, load test design | `capacity.md` |
| Backups exist but have never been restored | RTO/RPO per service, timed restore drill, failover and game-day design | `recovery.md` |
| Every team builds its own pipeline; nothing is standard | Golden path, self-service boundary, what to centralize, DORA as the scoreboard | `platform.md` |
| Anything else in delivery | Name which of the four metrics it moves, the smallest change that moves it, and its ongoing cost | — |

Coverage map: `pipelines.md` CI speed, flakiness, runners · `deploys.md` release strategies and rollback · `environments.md` env topology and promotion · `migrations.md` schema, data, and cutovers · `iac-workflow.md` infrastructure as a delivery process · `gitops.md` reconciliation-based deploys · `secrets.md` credentials in the pipeline · `supply-chain.md` artifacts, provenance, CVEs · `observability.md` signals and instrumentation cost · `slos.md` SLOs, error budgets, alerting · `incidents.md` on-call, response, postmortems · `capacity.md` load, scaling, launch readiness · `recovery.md` backups, restore, failover · `platform.md` golden paths and delivery metrics.

## Core Rules

1. **Build once, promote the artifact.** One build produces one immutable artifact (digest or version) that moves dev → staging → prod unchanged; only configuration is injected per environment. Verification: the identity running in prod is byte-identical to the one staging validated. A pipeline that rebuilds per environment has never tested what it ships — and the rebuild is also where "works in staging" quietly dies.
2. **A rollback is deploying a recorded artifact, not rebuilding a branch.** At deploy time, record the artifact identity and the previous one in `releases/<year>.md` (`memory-template.md`). Decision rule during an incident: if one attempt at a fix has not restored service within 15 minutes, or within 25% of the remaining error budget — whichever is smaller — roll back and diagnose afterward. Roll forward only when the change is not reversible (a migration past its contract step, an irreversible data write).
3. **Deploy small, deploy often — batch size is the risk dial.** A release carrying 30 changes and one carrying 3 fail at similar rates per *change*, but the 30-change release costs 10× the bisection to localize and cannot be reverted without reverting 29 innocent changes. Freezes do not reduce risk, they batch it: the post-freeze release is the largest and most dangerous of the quarter (`platform.md`).
4. **Feedback under `pipeline_time_budget_min`.** Order stages by catch rate per second, cheapest signal first: a lint stage catching ~15% of failures in 30s screens at 0.5 %/s, an integration suite catching 60% in 12 min at 0.08 %/s — so lint, unit, build, integration, deploy, in that order. Anything above the budget (default 10 min) gets parallelized, cached, or moved off the PR path to a nightly (`pipelines.md`).
5. **Schema changes are expand/contract, never one deploy.** Three deploys: expand (add the new column/table, nullable, dual-write), migrate (backfill in batches, both code paths valid), contract (drop the old, after the old code is gone everywhere). At every point, the previous release must run correctly against the current schema — otherwise a rollback (Rule 2) corrupts data instead of restoring service (`migrations.md`).
6. **Pipeline credentials are short-lived and scoped, or they are an incident waiting.** Prefer OIDC federation to the cloud (tokens minted per job, typically ~1h, nothing at rest) over stored keys. Where a static credential is unavoidable: one per pipeline, scoped to one environment, rotated on a written cadence, and revocable in a single action. Default job permissions read-only; deploy privileges live in a separate protected job (`secrets.md`).
7. **Alert on symptoms, page on burn rate.** A page must correspond to a user-visible SLI breaking fast enough to matter: burn rate = (observed bad-event ratio) ÷ (1 − SLO). Page at 14.4× over 1h (2% of a 30-day budget), ticket at 1× over 3 days. Cause-based alerts (CPU high, disk 80%, pod restarted) go to dashboards and tickets, never to a pager (`slos.md`).
8. **Every recurring obligation has a last-run date.** Restore drills, secret rotation, access review, dependency and base-image refresh, SLO review, alert hygiene, postmortem action sweeps — each is a row in the `## Due` table of `memory.md` with its cadence and last run. A cadence with no recorded last run is skipped for two quarters and nobody notices until the day it mattered.
9. **Manual production access is an exception with a record, not a workflow.** Anything that survives the session goes through the pipeline. When an emergency requires a human at the console, it ends with the change reproduced in code and a line in `## Pain Points` — otherwise the next apply silently reverts the fix, usually mid-incident (`iac-workflow.md`).

## Release Strategies

Pick by what you can pay and what you can measure — not by fashion. `deploy_strategy_default` sets the standing choice.

| Strategy | Capacity cost | Rollback speed | Requires | Use when |
|---|---|---|---|---|
| Recreate | 1× | Redeploy old (full downtime) | Nothing | Internal tools, batch jobs, a maintenance window is acceptable |
| Rolling | ~1.1-1.3× | Minutes: roll the old version back through | Backward-compatible API *and* schema during the window | The default for stateless services |
| Blue-green | 2× for the switch window | Seconds: flip traffic back | Two full environments, a shared data layer that both versions can read and write | Cutovers that must be instantly reversible |
| Canary | ~1.05× | Seconds: shift the slice back | Traffic splitting plus per-cohort metrics | High-traffic services where a bad release is expensive |
| Feature flag | 1× | Instant: flip the flag | Flag infrastructure, sticky bucketing, cleanup discipline | Decoupling deploy from release; risky behavior changes |

**Canary sizing is a statistics problem, not a percentage habit.** With zero failures in *n* canary requests, the 95% upper bound on the failure rate is ≈ 3/n (rule of three): 300 clean requests only prove the failure rate is below 1%. So a 1% canary on a 100 req/s service needs ~5 minutes to bound a 1% regression, and a low-traffic service cannot canary meaningfully at all — use blue-green there. Bake time must also exceed the slowest signal you rely on: if the latency alert evaluates a 5-minute window, a 2-minute bake proved nothing.

## Error Budgets And Paging

Budget for a 30-day month (43,200 minutes), and the burn-rate table that turns it into alerts:

| SLO | Budget / 30 days | 1-hour page threshold (14.4× burn) |
|---|---|---|
| 99% | 7 h 12 min | 14.4% of requests failing for an hour |
| 99.9% | 43.2 min | 1.44% failing for an hour |
| 99.95% | 21.6 min | 0.72% failing for an hour |
| 99.99% | 4.32 min | 0.144% failing for an hour — usually beyond what a human page can save |

| Budget consumed | Window | Burn rate | Action |
|---|---|---|---|
| 2% | 1 hour | 14.4× | Page |
| 5% | 6 hours | 6× | Page |
| 10% | 3 days | 1× | Ticket |

Each page threshold pairs with a short window (about 1/12 of the long one) that must also be breaching, so a resolved blip does not page for the rest of the hour. The policy is what gives the number teeth: budget exhausted → feature deploys pause and reliability work takes priority until the trailing window recovers. An SLO with no written consequence is a dashboard decoration (`slos.md`).

## Failure Signatures

| Signature | Most likely cause | First move |
|---|---|---|
| Deploy reported success, users still get the old version | CDN or proxy cache, a client bundle pinned by an old index, or a rolling deploy that never finished | Verify the running artifact identity on each instance, not the pipeline's exit code |
| Pipeline green, production broken | The pipeline tested a different artifact or a different config than it shipped (Rule 1) | Compare the deployed identity with the tested one; then compare env var sets |
| Rollback made things worse | The migration already ran; the old code cannot read the new schema (Rule 5) | Contract step is the point of no return — check where the migration sits before rolling back |
| Works in staging, fails in production only under load | Data volume and cardinality, not code — a query plan flips when the table is 1000× bigger | Compare row counts and index usage, not configs (`environments.md`) |
| Intermittent CI failures with no code change | Test order dependence, shared fixtures, wall-clock/timezone assumptions, or a port already bound on the runner | Re-run the failing test alone and in reverse order before blaming infrastructure |
| Alert never fired during a real outage | The alert depends on the failing system (metrics pipeline down), or it evaluates missing data as OK | Test alerts by breaking the thing deliberately; set missing-data behavior explicitly |
| Everything pages at once for one root cause | No dependency-aware inhibition; every downstream service alerts on its upstream | Alert on your own SLI only; inhibit downstream pages while the upstream page is firing |
| Retry storm turns a blip into an outage | Retries without jitter or budget, plus timeouts longer than the caller's | Cap retries at ~10% of request volume, exponential backoff with jitter, timeout budget shrinks per hop (`capacity.md`) |
| First deploy after a quiet period fails | Expired credential, rotated token, drifted infrastructure, or a base image that no longer exists | Check credential expiry and drift before reading application logs (`iac-workflow.md`) |
| Restore fails when it is finally needed | Backups were verified as *existing*, never as *restorable* — missing keys, roles, parameter groups | Timed restore drill into a scratch environment (`recovery.md`) |
| Anything else | Get the artifact identity, the config diff, and the timestamp of the last change to either | The change that immediately precedes the symptom is the suspect until eliminated |

## DORA Scoreboard

Four metrics; each recommendation in this skill should name which one it moves. DORA's research programme places its elite band near: deploy on demand (multiple times per day), change lead time under an hour, change failure rate roughly 0-15%, and service restored in under an hour. Treat them as directional bands, not certification thresholds.

| Metric | How to measure it without new tooling | The lever that moves it |
|---|---|---|
| Deploy frequency | Count rows in `releases/<year>.md` per week | Batch size (Rule 3), approval gates, pipeline duration |
| Change lead time | Merge timestamp → deploy timestamp, median | Pipeline time (Rule 4), manual gates, environment queueing |
| Change failure rate | Releases with a rollback or a hotfix within 24h ÷ all releases | Test signal quality, canary sizing, migration discipline |
| Time to restore | Incident start → service restored, from `incidents/<year>.md` | Rollback readiness (Rule 2), runbooks, alert latency |

Measure for two weeks before proposing an improvement: without the baseline, every intervention "works". A team below one deploy per week should fix batch size and pipeline time before buying any tooling.

## Output Gates

Before delivering a pipeline, a deploy plan, a policy, or an incident artifact:

- Does the plan name which of the four DORA metrics it moves, and what it costs to keep running?
- Is the thing being deployed the artifact that was tested, identified by digest or immutable version (Rule 1)?
- Is the rollback path a recorded artifact identity, and does it survive the migration state this change leaves behind (Rules 2, 5)?
- Are credentials short-lived or scoped, with no secret in a log, an env dump, an artifact, or anywhere under `~/Clawic/data/` (Rule 6)?
- Does every new alert correspond to a user-visible symptom with an owner and an action, and does every removed alert say what now covers it?
- Is any step destructive (drop, prune, force-apply, delete environment, restore over live data)? Then it names exactly what dies and ships with an explicit confirmation step, never inside a copy-paste block of read-only commands.
- Did anything durable come out of this — a service, an environment, a release, an incident, an SLO, a cadence, a runbook, a decision? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/devops/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| ci_platform | github-actions \| gitlab-ci \| jenkins \| buildkite \| circleci \| azure-devops \| none | none | Dialect of every pipeline example and the cache backend recommended in `pipelines.md`; while unset, name the platform being assumed before writing a pipeline file |
| iac_tool | terraform \| opentofu \| pulumi \| cloudformation \| cdk \| ansible \| none | terraform | Language and workflow of `iac-workflow.md`, including the drift-check and policy-gate commands |
| deploy_model | push \| gitops | push | Whether deploys are pipeline-driven (`deploys.md`) or reconciled from a repo (`gitops.md`) |
| environment_chain | list | [dev, staging, prod] | The promotion path in `environments.md`; each added environment adds a gate, a config set, and a cost line |
| deploy_strategy_default | rolling \| blue-green \| canary \| recreate | rolling | Standing choice in Release Strategies and the shape of every generated deploy plan |
| version_scheme | semver \| calver \| git-sha | git-sha | Identity stamped on artifacts and releases, and what `releases/<year>.md` records |
| pipeline_time_budget_min | number (min, 1-120) | 10 | The PR-feedback ceiling Rule 4 enforces and the threshold for calling a pipeline slow |
| slo_target_pct | number (90-99.999) | 99.9 | Default availability target, its error budget, and every burn-rate threshold in `slos.md` |
| secrets_backend | vault \| aws-secrets-manager \| gcp-sm \| azure-kv \| sops \| 1password \| ci-native | ci-native | Where `secrets.md` puts secrets, what the pointer scheme looks like, and how rotation is described |
| observability_stack | prometheus-grafana \| datadog \| cloudwatch \| new-relic \| elastic \| otel-generic \| none | none | Query dialect and cost model in `observability.md` and `slos.md` |
| oncall_model | none \| business-hours \| rotation-24x7 \| follow-the-sun | business-hours | Rotation sizing, escalation, and severity definitions in `incidents.md`; also whether paging advice applies at all |
| approval_gate | none \| prod-only \| all | prod-only | Where a human approval sits in the promotion path, and what evidence the pipeline must capture for it |
| compliance_regime | none \| soc2 \| iso27001 \| pci \| hipaa \| fedramp | none | Forces separation of duties, retention, and audit-evidence capture into the pipeline and the artifact list |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — artifact registry, feature-flag system, paging provider, load-testing tool, policy engine, dependency-update bot — affects which product's shape every example takes
- **Conventions** — branch model (trunk-based vs release branches), tag and release naming, environment naming, service ownership metadata, runbook location — affects generated files and `platform.md`
- **Platform** — where workloads run (single host, VMs, containers, serverless, managed platform), cloud provider, region and data-residency constraints — affects `capacity.md`, `recovery.md`, and every cutover plan
- **Safety posture** — appetite for automated rollback, whether destructive commands are emitted at all, blast-radius limits per change, freeze windows — affects Output Gates and `deploys.md`
- **Work order** — review gates, who approves what, whether migrations ship with or ahead of code, pairing on production changes — affects the promotion path in `environments.md`
- **Compliance and restrictions** — the CVE remediation SLA per severity (`supply-chain.md`), audit-evidence and log retention floors, data-residency limits, separation-of-duties requirements, vetoed technologies or registries — recorded under a `compliance` block in `config.yaml`; `compliance_regime` sets the ones a regime dictates, the rest are the user's own
- **Cadence** — restore drills, game days, secret rotation, access review, dependency refresh, SLO and alert review, postmortem action sweeps — every accepted cadence becomes a row in the `## Due` table of `memory.md`
- **Output register** — plan-first vs command-first, how much reasoning to keep, whether to produce diffs or whole files, incident-comms tone — affects every answer's shape

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Rebuilding the artifact for production | The tested bytes and the shipped bytes differ; every "only in prod" bug starts here | Promote one artifact by identity (Rule 1) |
| "Rollback = revert the commit and redeploy" | That is a roll-forward through the full pipeline, at the worst possible moment | Keep the previous artifact deployable and its identity recorded (Rule 2) |
| Migration and application change in one deploy | The rollback path no longer exists the moment the migration runs | Expand/contract across three deploys (Rule 5) |
| Alerting on CPU, memory, or restart counts | They fire when nothing is wrong and stay quiet when everything is | Symptom SLI plus burn rate (Rule 7); resources belong on dashboards |
| Staging with toy data | Query plans, timeouts, and pagination bugs only appear at production cardinality | Match shape and order of magnitude, anonymized (`environments.md`) |
| Long-lived cloud keys in CI secrets | They outlive the person who created them and grant more than the job needs | OIDC federation, scoped per environment (Rule 6) |
| Canary at 1% for two minutes on a low-traffic service | The sample cannot detect the regression it exists to catch | Size the canary from the rule of three, or use blue-green |
| Deploy freeze as risk management | Batches the quarter's changes into one release nobody can bisect | Smaller, more frequent releases; freeze only what the calendar genuinely forbids (Rule 3) |
| Postmortem action items with no owner or date | Completion rate collapses and the same incident recurs | One owner, one date, tracked in `## Due` until closed (`incidents.md`) |
| Runbook that lives in the system that goes down | The wiki is on the cluster that is on fire | Runbook in `artifacts/`, plus a copy the on-call can open offline |
| Secret "rotated" by adding a new one | The old credential stays valid forever; the leak is still live | Rotation is issue → cut over → **revoke** → verify the old one fails (`secrets.md`) |
| Retry logic added without a budget | Retries multiply load exactly when the system is weakest | Cap retries as a fraction of traffic, jitter the backoff, shrink the timeout per hop |
| Auto-merging dependency updates on a green pipeline | "Green" means your tests passed, not that the change is safe or the package is genuine | Gate on provenance and a CVE policy; batch and review majors (`supply-chain.md`) |
| One giant IaC state or one giant pipeline | Every change waits behind every other change, and one bad apply blocks all of them | Split by blast radius and lifecycle (`iac-workflow.md`) |
| Buying an observability platform before defining an SLI | Cost scales with cardinality and the question stays unanswered | Define the SLI, instrument that, then price the storage (`observability.md`) |
| Measuring the team by deploy count alone | Deploy frequency without change failure rate rewards shipping breakage | Read all four DORA metrics together (`platform.md`) |

## Where Experts Disagree

- **Trunk-based vs release branches.** Trunk-based with flags is the default when you ship the one version you host. Release branches earn their overhead only when customers run versions you cannot upgrade (on-prem, mobile, embedded) — then the cost is real and unavoidable.
- **GitOps pull vs pipeline push.** Pull-based reconciliation wins on drift correction, audit, and many clusters; push wins on simplicity, on ordering across non-Kubernetes resources, and on being debuggable by whoever is awake. The frontier is cluster count and whether anyone will own the reconciler (`gitops.md`).
- **A staging environment vs testing in production.** Flags, canaries, and shadow traffic catch what staging cannot, at the price of exposure. The frontier is whether you can legally and practically reproduce production data volume elsewhere; regulated data usually forces a real staging environment.
- **Dedicated platform/SRE team vs "you build it, you run it".** Below roughly a dozen engineers, a platform team is overhead and the same people do both. The signal to specialize is duplicated pipelines and a rising share of time spent on delivery plumbing rather than a headcount number (`platform.md`).
- **Automated rollback on SLO breach.** Automating it cuts time-to-restore and occasionally reverts a good release during an unrelated outage. Teams with reliable canary signal automate; teams whose signal is noisy get faster recovery from a rehearsed human decision (Rule 2).
- **How much to standardize.** A golden path raises the floor and lowers the ceiling. The defensible line: standardize what breaks production (deploy, secrets, observability, rollback) and leave language, framework, and test style to the teams.

## Security & Privacy

**Credentials:** this skill designs pipelines and deploys that consume credentials from the platform's own secret store, an OIDC federation, or an OS keychain. It does NOT store, log, copy, or transmit tokens, keys, or passwords, and never writes a credential into `~/Clawic/data/`.

**Local storage:** service and environment inventory, release and incident records, SLOs, cadences, and generated artifacts stay in `~/Clawic/data/devops/` on this machine, plus rows in the shared `servers/`, `contacts/`, `projects/`, `domains/`, and `finances/` boxes. Names, versions, digests, dates, and pointers only — no secret values.

**Guardrails:** commands are read-only by default. Destructive operations (force apply, environment teardown, restore over live data, prune, drop) name exactly what they destroy and require explicit confirmation.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/devops (install if the user confirms):
- `docker` — building and running the images this pipeline ships
- `k8s` — Kubernetes manifests and cluster debugging for the deploy target
- `terraform` — HCL authoring, state surgery, module design
- `github-actions` — workflow syntax, reusable pipelines, runner configuration
- `feature-flags` (planned) — cohort targeting, kill switches, and flag-debt cleanup in depth

## Feedback

- If useful, star it: https://clawic.com/skills/devops
- Latest version: https://clawic.com/skills/devops

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/devops.
