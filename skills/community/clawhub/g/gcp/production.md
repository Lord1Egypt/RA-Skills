# Production — SLOs, Alerting, Backups, and the Day It Breaks

Scope: taking something that works into something you are on call for. The gate at the bottom is the checklist; everything above it explains why each item is on it.

**Contents:** [Availability Is a Number You Choose and Pay For](#availability-is-a-number-you-choose-and-pay-for) · [SLOs and Error Budgets](#slos-and-error-budgets) · [The Four Signals, and Where They Live](#the-four-signals-and-where-they-live) · [Alerts That Fire When They Should](#alerts-that-fire-when-they-should) · [Uptime Checks](#uptime-checks) · [Backups and Recovery](#backups-and-recovery) · [Deploy and Rollback](#deploy-and-rollback) · [Incident Response](#incident-response) · [Cadences](#cadences) · [The Production Gate](#the-production-gate)

## Availability Is a Number You Choose and Pay For

Pick the target before designing, because each nine changes the architecture and the bill.

| Target | Downtime per month | What it takes |
|---|---|---|
| 99% | ~7.2 hours | Single zone, restore from backup, humans in the loop |
| 99.9% | ~43 minutes | Multi-zone (regional cluster, HA database), health checks, automated restart, a tested restore |
| 99.95% | ~22 minutes | The above plus tested failover, deploy safety, and someone awake |
| 99.99% | ~4.4 minutes | Multi-region with automated failover, and a data layer that supports it |

Two GCP-specific notes. **Regional is the cheap nine**: because a VPC is global and most managed services offer a regional (multi-zone) mode as a toggle, 99.9% is usually a configuration decision rather than an architecture. **Multi-region is the expensive nine**: it needs a data layer that can do it — Spanner, a multi-region bucket, or an application that tolerates asynchronous replication — and the honest cost is roughly double plus the complexity of failover you have actually tested.

Your own availability is bounded by your dependencies' composed availability. Three sequential services at 99.9% give about 99.7%, before your own code has a bug.

## SLOs and Error Budgets

- Define the SLI as a ratio of good events to valid events — successful requests over total requests, or requests faster than a threshold over total. Latency SLOs must name a percentile and a threshold; "fast" is not an SLI.
- The **error budget** is the inverse of the target. At 99.9%, roughly 43 minutes a month of failure is acceptable, and that number is the argument that ends the "can we ship on Friday" discussion with data instead of seniority.
- **Burn-rate alerting is the technique that matters.** Alert on the rate at which the budget is being consumed, not on a raw error-rate threshold: a fast-burn alert (a large multiple of the budget rate over a short window) pages for real outages, and a slow-burn alert (a small multiple over a long window) opens a ticket for chronic degradation. A single static threshold does one of those two jobs badly.
- Cloud Monitoring models services, SLOs and burn-rate alerts natively — use it rather than reimplementing the arithmetic in ad-hoc conditions.
- One or two SLOs per user-facing service. An SLO per endpoint is a dashboard nobody reads.

## The Four Signals, and Where They Live

| Signal | Where | Note |
|---|---|---|
| Traffic | Load balancer request count, Cloud Run request count, Pub/Sub publish rate | The denominator for everything else |
| Errors | Load balancer 5xx by `statusDetails`, application error rate, Error Reporting groups | `statusDetails` distinguishes "backend broke" from "client left" (`debug.md`) |
| Latency | Load balancer and application latency distributions, at p50/p95/p99 | Averages hide the outage; percentiles do not |
| Saturation | CPU, memory, connection counts, queue depth, quota consumption | Quota is a saturation signal in GCP and almost nobody graphs it |

Three additions that are specific to this platform and catch real incidents: **quota consumption** approaching a limit, **oldest unacked message age** on every Pub/Sub subscription (`pipelines.md`), and **certificate expiry** for managed certificates whose DNS may have drifted (`networking.md`).

Custom and Prometheus-compatible metrics are billed per sample ingested. A high-cardinality label — user id, request id, full URL — turns one metric into millions of time series and a monitoring bill that rivals the workload. Label with bounded values only.

## Alerts That Fire When They Should

- **Alert on symptoms, page on user impact.** A CPU alert is a diagnostic; an SLO burn-rate alert is a page. Everything that is not user-impacting is a ticket.
- **Absence of data is a condition.** A metric that stops publishing looks like a healthy zero to a threshold condition, so the alert stays silent through the outage. Configure the absent-data behaviour deliberately on every alert whose metric can stop — this is the single most common reason an alert did not fire during a real incident.
- **Auto-close is not resolution.** An incident closes when its condition stops evaluating as met, which includes the metric disappearing entirely. Set the auto-close duration deliberately and treat a closed incident nobody acted on as a bug in the alert.
- **Notification channels must be tested.** A channel added and never exercised fails the first time it matters. Send a test through every channel when it is created, and again after any change to the receiving system.
- **Every alert names its runbook.** Put the artifact path in the alert's documentation field, so the page and the procedure arrive together (`artifacts/`).
- Group by service, not by resource. Ten instances of one failure is one incident.

## Uptime Checks

- Synthetic checks from multiple global locations catch what internal metrics cannot: DNS failures, certificate expiry, a load balancer misconfiguration, and a region that is fine while the path to it is not.
- Check a URL that exercises a real dependency, not a static health endpoint that returns 200 while the database is down. The endpoint should be cheap enough to call frequently and honest enough to fail when the service is failing.
- Uptime checks arrive from Google's own ranges and must be allowed through Cloud Armor and any IP allowlist, or the check reports an outage that does not exist.
- A private service can be checked from inside the VPC; the check then loses the external-path coverage that was the reason to have it. Do both where it matters.

## Backups and Recovery

- **RPO and RTO are agreements, not aspirations.** Write them to `~/Clawic/data/gcp/artifacts/dr-targets.md` — one row per stateful service, with who agreed them, the configuration that delivers them and the last measured restore — and add its `## Boxes` line. Then verify: PITR window against RPO, measured restore time against RTO (`memory-template.md`).
- **Every stateful service, explicitly**: Cloud SQL automated backups with PITR (`databases.md`), Cloud Storage versioning plus a noncurrent-version lifecycle rule (`storage.md`), disk snapshot schedules with retention, Firestore scheduled exports, BigQuery time travel plus table snapshots for anything beyond the window, GKE cluster state via Backup for GKE.
- **Backups attached to the resource die with it.** Cloud SQL backups are deleted with the instance; an export to a bucket in another project is what survives an accidental deletion or a compromised project.
- **Deletion protection everywhere it exists** — Cloud SQL instances, GKE clusters, project liens (`organization.md`), and `prevent_destroy` in Terraform (`iac.md`).
- **Test the restore, not the backup.** Restores fail on details nobody wrote down: a CMEK grant the new project lacks, a peering range with no space, a database flag set by hand, an extension not installed, a DNS record still pointing at the old endpoint.
- Quarterly, restore into a scratch environment, time it end to end, and record the measured RTO and everything that was missing in `~/Clawic/data/gcp/deploys/<year>.md` under `## Restore Drills` — then update the `Last measured RTO` cell in `artifacts/dr-targets.md`, since a target nobody re-measured is the one that fails on the day (`memory-template.md`).

## Deploy and Rollback

- **The rollback artifact is named before the deploy, not found during the incident.** Cloud Run: the previous revision name. GKE: the previous image digest and manifest revision. Terraform: the previous state version and module ref. Record it in the deploy row.
- **Progressive delivery**: Cloud Run traffic splitting or Cloud Deploy's canary phases, with a bake window long enough for the SLI to move. A canary with a two-minute bake proves the container starts and nothing else.
- **Health-gate the promotion** on the SLI, not on "the deploy command succeeded".
- **Database migrations are expand-contract, always**: add the new column, deploy code that writes both and reads the old, backfill, switch reads, deploy code that only uses the new, then drop. A migration that renames a column in one step makes rollback impossible, which means the deploy is one-way regardless of what the deploy tool offers.
- **Pin images by digest.** A mutable tag means the rollback target may not be the artifact you rolled back from.
- Write every deploy to `deploys/<year>.md`: date, service, image digest and commit, the new revision or template version, the rollback target, and anything unusual.

## Incident Response

1. **Stabilize before diagnosing.** Roll back or shift traffic first; the cause can be found from logs afterwards. An incident spent debugging a bad deploy is downtime chosen voluntarily.
2. **Establish the timeline from the audit log.** What changed, when, and by which principal. Admin Activity logs always exist for exactly this (`debug.md`).
3. **Check the platform.** The service health dashboard rules out the one cause you cannot fix. Rare, and worth thirty seconds.
4. **Communicate on a cadence**, even with nothing new. Silence is interpreted as absence.
5. **Write the runbook while it is fresh** — the symptom in the title, the walk that found the cause, the fix, and every secret replaced by its pointer. Save it to `~/Clawic/data/gcp/artifacts/runbook-<symptom>.md` and add its `## Boxes` line with the read condition in the same turn. The second occurrence should cost minutes (`memory-template.md`).
6. **One action item, owned, with a date.** A postmortem with twelve action items produces zero.

## Cadences

Recurring work has to have a home or it does not happen. Each of these goes in the `## Due` table of `memory.md` with its interval and last-run date, and is checked against today's date at the start of a session.

| Cadence | Every | Why it cannot be skipped |
|---|---|---|
| Cost review from the billing export | Month | Spend drifts silently; the export is the only detail source (`costs.md`) |
| Recommender sweep (idle VMs, disks, addresses) | Month | The cheapest saving on the platform, and it recurs |
| Restore drill with a measured RTO | Quarter | An untested restore is a hope |
| GKE version support check | Quarter | An unattended cluster gets upgraded for you (`gke.md`) |
| Unused service account and key sweep | Quarter | Every stale credential is an unowned access path (`iam.md`) |
| Exposure sweep and Security Command Center triage | Quarter | Drift toward public is one-directional (`security.md`) |
| Quota headroom review against growth | Quarter | Increases take days; incidents do not wait (`organization.md`) |
| Commitment and certificate expiry check | Before each expiry | A lapsed commitment reprices a fleet overnight |

## The Production Gate

Before calling something production:

- Availability target chosen, and the architecture matches it — regional control plane, HA database, multi-zone compute
- SLO defined with a burn-rate alert (fast and slow), routed to a human who is awake
- Every alert has its absent-data behaviour set deliberately, and every notification channel has been tested
- Uptime check against a URL that exercises a real dependency, allowed through Cloud Armor and any IP restriction
- Backups configured for every stateful component, with a retention matching the agreed RPO and a restore that has been timed
- Deletion protection and liens on the resources whose loss is unrecoverable
- Autoscaling configured, and the downstream ceiling verified against instances × concurrency (`run.md`, `databases.md`)
- The first quota the design will hit is named, its current value known, and headroom requested (`## Quotas`)
- Deploy path is health-gated with a named rollback artifact; migrations are expand-contract
- State and configuration in version control; no console-only resources (`iac.md`)
- Runbooks exist for the top three failure modes, saved in `~/Clawic/data/gcp/artifacts/` with their `## Boxes` lines, and the restore drill has been run once with a recorded time
- Every cadence above is in `## Due` with a last-run date

Every item above that produced a fact writes it in the same turn: the agreed RPO and RTO per service to `~/Clawic/data/gcp/artifacts/dr-targets.md` with its `## Boxes` line, measured RTO and what was missing to `~/Clawic/data/gcp/deploys/<year>.md` under `## Restore Drills`, each deploy with its rollback target to the same file, every runbook to `~/Clawic/data/gcp/artifacts/` with its `## Boxes` line and read condition, and every cadence with its last-run date to the `## Due` table of `~/Clawic/data/gcp/memory.md` (`memory-template.md`).
