# Cost Control

Prices: us-central1, on-demand, recorded early 2026. The **ratios and break-evens are stable**; verify the absolute number on the pricing page before committing money. Every threshold below scales with `monthly_budget_usd`.

**Contents:** [The Export Is the Prerequisite](#the-export-is-the-prerequisite) · [Budgets Notify, They Do Not Cap](#budgets-notify-they-do-not-cap) · [Diagnosing a Surprise Bill](#diagnosing-a-surprise-bill) · [The Ten Biggest Line Items](#the-ten-biggest-line-items) · [Discounts, In the Order They Apply](#discounts-in-the-order-they-apply) · [Let Recommender Do the Right-Sizing](#let-recommender-do-the-right-sizing) · [Free Tier Worth Designing Around](#free-tier-worth-designing-around) · [Monthly Review Checklist](#monthly-review-checklist)

**Before answering any spend question**, read `## Spend` in `~/Clawic/data/gcp/memory.md` — or `spend-log.md` if the `## Boxes` index points there. A current-month number with no prior months is not an answer.

**After any bill review or saving**, write it back in the same turn: the month row with its `As of` date, the top three services, and any optimization (`memory-template.md`).

## The Export Is the Prerequisite

Cloud Billing's console reports are a rounded, lagging summary. The detailed export to BigQuery is the actual data, and it has one property that decides when you enable it: **it reports forward only**. Turn it on in the month you need it and the month you needed it does not exist.

- Enable **detailed usage cost** export (SKU-level, with labels and resource ids), not the standard export — the standard one omits the resource-level breakdown that names which VM or which query did it.
- Put the export dataset in the project that owns the billing account, not in the workload project, so a project deletion never takes the cost history with it.
- The pricing export is a separate toggle and is worth having: it is how you compare what you paid against list price and see whether a discount is actually applying.
- Data lands with a lag measured in hours, and rows are **restated** for up to several days as Google finalizes usage. A number read on the 1st for the previous month is not final; a number read on the 5th is close enough to compare.
- Labels appear in the export from the moment both the label and the export exist. Neither is retroactive (SKILL.md Rule 6).

Record the export dataset and its enablement date in `### Alerts Configured` in `memory.md`. "Is the export on?" should never cost an API call twice.

## Budgets Notify, They Do Not Cap

The single most expensive misunderstanding in GCP billing.

- A budget sends notifications at thresholds. Spend continues past every one of them. There is no built-in stop.
- Thresholds worth setting: **50% actual** (early signal that the month is running hot), **90% actual** (act now), **100% actual**, **100% forecast** (the one that catches a ramp before it lands).
- Scope the budget to the project or the label set, not just the billing account: a billing-account budget on a five-project org tells you the total went up and nothing else.
- Route the budget's Pub/Sub topic somewhere a human reads. Email-only budgets on a shared alias are how a 3× month gets discovered on the 30th.
- **A real cap** requires a Pub/Sub-triggered function that calls the billing API to detach the billing account from the project. Understand what that does before recommending it: every resource in the project stops, VMs terminate, and some resources are deleted rather than paused. It is a circuit breaker for a sandbox, never for production.
- Budget alerts have a lag of their own. For anything with a runaway shape — a recursive Cloud Function, a query loop, a compromised key mining crypto — a **log-based alert on resource creation rate** fires hours earlier than a budget threshold does.

## Diagnosing a Surprise Bill

In order. Stop when the number is explained; do not optimize before you know the cause.

1. **Billing export, grouped by service, this month vs the same span of last month.** Compare like spans — the 1st-to-8th against the 1st-to-8th, never month-to-date against a closed month.
2. **Take the service that moved and group by SKU.** The service name says "Compute Engine"; the SKU says "N2 Instance Core running in Americas" or "Network Internet Egress from Americas to Americas". The SKU is the answer.
3. **Group by resource id or label** to find the specific instance, dataset or bucket.
4. **Map the delta's start date to a change.** Cross-reference `deploys/<year>.md` and the audit log. A cost curve that starts on a Tuesday afternoon has a deploy on that Tuesday afternoon.
5. **If the shape is a step, it is a resource. If it is a ramp, it is data volume. If it is a spike, it is a job.** Steps come from something created; ramps come from storage, logs, or a table that keeps growing; spikes come from a query, a batch, or a retry storm.
6. **If nothing explains it, check for a second billing account or a project outside the folder you are looking at.** Org-wide totals and project totals disagreeing is usually a project nobody remembered.

## The Ten Biggest Line Items

Ordered by how often each one is the answer, not by size.

| Driver | Mechanics | Fix |
|---|---|---|
| BigQuery on-demand scans | ~$6.25/TiB scanned. Cost is bytes read from columns touched, not rows returned; `LIMIT` changes nothing | Column pruning, partition filters, `require_partition_filter`, dry-run before every run (`bigquery.md`) |
| Cloud SQL running 24/7 | An HA instance is two machines plus storage plus backups, and storage never shrinks | Right-size the tier, stop non-prod out of hours, and check whether the read replica is read by anything (`databases.md`) |
| Cloud NAT | Hourly gateway charge plus ~$0.045/GB processed. Package pulls, container images and Google API calls all traverse it by default | Private Google Access (free) for Google APIs; Artifact Registry over PSC; NAT only for genuine third-party egress (`networking.md`) |
| Cloud Logging ingestion | ~$0.50/GiB past the monthly free allowance per project. The `_Required` bucket is free and 400 days; `_Default` is 30 days and billable | Exclusion filters at the sink for health checks and debug levels; enable Data Access audit logs selectively, never org-wide (`security.md`) |
| Persistent disks and snapshots | Disks bill by provisioned size, not used. Deleting a VM leaves disks behind unless auto-delete was set at creation | Sweep disks with no users; snapshot schedules with retention; balanced instead of SSD unless IOPS were measured (`storage.md`) |
| External IPv4 | Billed hourly attached or not; a reserved unused address costs more per hour than an attached one | Release orphans; put VMs behind a load balancer or Cloud NAT with no external IP |
| Idle serving capacity | Vertex AI endpoints, Cloud Run `min-instances`, Memorystore, and a GKE cluster's node pool all bill while nothing is happening | Undeploy endpoints between experiments; `min-instances` only where cold start was measured as a problem (`vertex.md`, `run.md`) |
| Inter-zone and internet egress | Same-zone free; cross-zone billed; internet egress billed by destination and network tier | Co-locate chatty pairs; Cloud CDN for public assets; Standard network tier where global routing is not needed |
| Managed platform floors | Composer, Bigtable, Spanner and Dataproc all bill from a minimum capacity regardless of use | Check the floor before choosing the service, not after the first invoice (`services.md`) |
| Support tier | An Enhanced or Premium support plan is a percentage of spend and appears as a line item people forget they chose | Match the tier to the on-call reality, and re-check it when spend grows |

## Discounts, In the Order They Apply

Getting the order wrong produces recommendations that lose money.

1. **Sustained use discounts (SUD)** — automatic, no commitment, applied to Compute Engine general-purpose and memory-optimized predefined machine types when an instance runs a large fraction of the month. **E2 machines earn none.** This is why an E2 that looks cheaper on the pricing page can be more expensive than an N2D for an always-on workload: compare the *effective* month price, not the hourly list price.
2. **Right-size** (below). Commit to nothing until the fleet is the size it should be.
3. **Committed use discounts (CUD)** — 1-year and 3-year terms. Resource-based CUDs (vCPU and memory in a region and family) discount more but lock the shape; spend-based / flexible CUDs discount less and move across families and regions. Rough guidance: resource-based is the bigger number, flexible is the one that survives a re-platform. Buy flexible when the architecture is still moving.
4. **Spot VMs** — deep discount, 30-second preemption notice, no fixed maximum lifetime. Correct for batch, CI, fault-tolerant queue workers and GKE node pools with a Standard baseline. Wrong for anything that cannot drain in 30 seconds.
5. **BigQuery editions with commitments** — only after the on-demand baseline is known and stable (`bigquery.md`).

Traps in this order: a CUD bought before right-sizing locks the waste in for years; a CUD bought in the wrong region is unusable and non-refundable; and CUD coverage below ~70% of steady-state usage means you are paying on-demand for the rest while still paying the commitment.

Put every commitment's **expiry date** in the `## Due` table. A CUD that lapses unnoticed reprices a whole fleet to on-demand overnight.

## Let Recommender Do the Right-Sizing

GCP computes recommendations from observed usage and they are the best free cost tool on the platform. Use them before guessing.

| Recommender | What it finds | Watch out for |
|---|---|---|
| Idle VM | Instances with negligible CPU and network over the observation window | A cold standby is idle on purpose — check before deleting |
| Idle persistent disk | Disks with no attached instance | A disk kept as a manual backup looks identical; prefer snapshots and delete the disk |
| Idle external IP | Reserved addresses with nothing attached | Releasing an address someone hardcoded in DNS breaks it (`domains.md` in the shared box) |
| Machine type | Right-sizing based on observed CPU and memory | It optimizes for the observed window; a monthly batch peak may fall outside it |
| Idle Cloud SQL | Instances with no connections | A replica used only for a quarterly report looks idle for 89 days |
| Unattended project | Projects with no recent activity | The cheapest saving on the list, and the one nobody looks for |
| Commitment (CUD) | Where a commitment would pay off at current usage | Only trustworthy after right-sizing (step 2 above) |
| IAM role | Over-granted roles, from actual permission use | Security, not cost, but it runs on the same data (`iam.md`) |

Where no recommendation exists: avg CPU <20% over 14 days → step down one size; sustained >70% → step up or scale out. Each size step roughly halves or doubles compute cost. Check memory before downsizing a JVM or a database — CPU alone under-diagnoses memory-bound workloads.

## Free Tier Worth Designing Around

Only the parts big enough to change a decision for a small project:

- **BigQuery**: a monthly on-demand query allowance and a monthly storage allowance. A hobby analytics stack can genuinely cost zero — until one `SELECT *` blows the allowance in a single query.
- **Cloud Run**: a monthly allowance of requests and of vCPU/memory-seconds, which covers a real side project as long as it scales to zero. `min-instances: 1` gives that up entirely.
- **Cloud Logging**: a per-project monthly ingestion allowance. Multi-project layouts get one allowance each, which is a genuine argument for project separation.
- **Compute Engine**: one small always-free VM in specific US regions, plus a small always-free Cloud Storage bucket in the same regions. Region-locked, so a project placed in Europe for latency or residency forfeits it — say so rather than silently losing it.
- **Cloud Scheduler**: a few free jobs per month, which is why Scheduler + Workflows beats Composer for simple orchestration by three orders of magnitude (`pipelines.md`).

## Monthly Review Checklist

Run it, then record it. Each row is a query against the billing export or a Recommender call.

| Check | Action |
|---|---|
| Top 5 services by spend, vs last month same span | Anything that moved >20% gets a SKU-level look |
| Recommender: idle VMs, disks, addresses, Cloud SQL | Delete or downsize; anything kept idle on purpose gets a row in `### Intentionally Idle` in `memory.md` with its reason and a recheck date, so next month's sweep skips it instead of re-proposing the same deletion |
| Disks with no attached instance; snapshots past retention | Delete; put the survivors on a schedule with a retention policy |
| Unattached reserved external IPs | Release, after checking DNS |
| Cloud Logging ingestion by log name | Add exclusion filters to the top talker; check whether Data Access logs got enabled somewhere |
| BigQuery top queries by bytes billed | The top three usually are one dashboard; fix that one (`bigquery.md`) |
| Cloud Run and Vertex AI services with `min-instances` or a deployed endpoint | Confirm each one is still earning its idle cost |
| CUD coverage and utilization; commitment expiry dates | Under ~70% coverage of steady state = under-committed; any expiry inside 90 days goes in `## Due` |
| Non-production running outside business hours | Schedule stop/start |
| Unlabelled spend | Anything unattributable is next month's argument — fix the labels now (SKILL.md Rule 6) |
| Projects with spend and no owner recorded in `~/Clawic/data/gcp/projects.md` | Find the owner or shut it down (`organization.md`) |

Record the date this ran in the `## Due` table of `memory.md`, the month row in `## Spend`, any saving in `### Optimization Log` with its monthly value, and every deliberate keep in `### Intentionally Idle` with its reason and recheck date (`memory-template.md`). A checklist with no last-run date gets skipped for a quarter and nobody notices; a saving with no recorded value gets re-derived next quarter; an idle resource with no recorded reason gets re-flagged every month until someone deletes the one that was load-bearing.
