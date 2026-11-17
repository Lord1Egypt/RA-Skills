# Engineering Operations

## DORA Metrics

The four that predict engineering health (DORA / Accelerate, Forsgren et al.; bucket boundaries shift slightly by report year — treat as bands, not gospel):

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| Deployment frequency | On demand / multiple per day | Weekly | Monthly | < Monthly |
| Lead time for changes | < 1 day | < 1 week | < 1 month | > 1 month |
| Change failure rate | ~5% | ~10% | ~15% | > 15% |
| Time to restore | < 1 hour | < 1 day | < 1 week | > 1 week |

Move one bucket at a time; the leverage metric for most teams is **lead time** — shrinking it forces smaller changes, which improves failure rate and restore time for free. Gaming check: deploy frequency without failure-rate tracking just measures enthusiasm.

## Error Budgets (Google SRE)

Set an SLO, spend the difference deliberately. Worked example: 99.9% availability over 30 days = 30 × 24 × 60 × 0.001 = **43.2 minutes** of allowed downtime. Budget remaining → ship features freely. Budget exhausted → feature freeze, reliability work only, until the rolling window recovers. The point: it converts "how reliable is reliable enough" from a standoff between product and engineering into arithmetic both sides agreed to in advance.

Don't set 99.99% because it sounds better — each extra nine roughly 10×es the cost, and your users can't tell 99.9 from 99.99 if their own wifi is worse.

## On-Call

- **Sustainability threshold**: more than ~2 incidents per 12-hour shift, sustained, burns the rotation (Google SRE's operating limit). Past it, fix alert noise before anything else — most pages at that volume are non-actionable alerts, not real incidents.
- Every alert must be actionable and have a runbook; an alert with no action is a notification, delete or downgrade it.
- Compensate off-hours on-call explicitly. Unpaid on-call is a resignation letter with a delay.

| Team size | Rotation |
|-----------|----------|
| 1-3 | Informal, shared — and be honest with customers about coverage |
| 4-8 | Weekly rotation, minimum 4 people (below 4, it's permanent on-call with extra steps) |
| 8+ | Multiple rotations split by service |

## Incidents

Severity convention (define yours; this is the common shape):

| Sev | Meaning | Response |
|-----|---------|----------|
| SEV1 | Customers down / data at risk | Page immediately, incident commander, exec notified |
| SEV2 | Degraded, workaround exists | Page on-call, fix in hours |
| SEV3 | Minor, contained | Ticket, fix in normal flow |

Flow: detect → acknowledge → **mitigate first** (stop the bleeding — rollback beats debugging in production) → resolve root cause → review. The classic error is debugging forward while customers are down; the flag/rollback is almost always faster.

**Postmortems:** written within 48 hours, blameless (name systems and gaps, never people — the person who fat-fingered it was allowed to fat-finger it by the system), action items with owner + date and tracked to completion, shared widely. A postmortem whose actions die in the backlog trains the team that incidents have no consequences.

## Development Workflow

- Trunk-based for small teams; feature branches elsewhere, **living < 1 week** — branch age is merge-conflict interest compounding daily.
- CI green required to merge, no exceptions for seniority.
- **Code review: keep PRs under ~400 lines** — defect detection falls off past that (SmartBear/Cisco study); a 2,000-line PR gets a "LGTM", not a review. Review latency target < 24h: a fast decent review beats a slow perfect one, because slow reviews push authors to batch bigger PRs, which makes reviews worse — the doom loop runs on latency.
- Author's side of the contract: small focused PRs, self-review first, description says why not just what.

## Release Process

CI → staging → canary (small % of real traffic) → full rollout → watch dashboards for the first hour. Canary is the cheapest insurance in the pipeline; skipping it to save 20 minutes trades against your worst outage.

**Feature flags:** decouple deploy from release, gradual rollout, instant rollback. And the part everyone skips: **delete flags after full rollout** — stale flags are debt with combinatorial interest (every live flag doubles the config states you claim to have tested).

## Security Baseline

- Dependency scanning automated in CI; secrets never in code (scanner in CI too — the leak you catch pre-push costs nothing, the one on GitHub costs a rotation drill)
- Least privilege, access reviews on a calendar (quarterly beats "when we remember")
- Incident response plan exists and has been walked through once — a plan first read during the incident isn't a plan
