# Choosing Services — Thresholds, Floors, and Break-Evens

Decide by hard limit, capacity floor and break-even, never by feature list. Every table here is a decision with a number attached; where the number depends on the user's data, the method for computing it is given instead of a fake constant.

**Contents:** [The Three Questions](#the-three-questions) · [Compute](#compute) · [Machine Families and Discounts](#machine-families-and-discounts) · [Spot](#spot) · [Data Stores](#data-stores) · [Messaging and Orchestration](#messaging-and-orchestration) · [Analytics](#analytics) · [The Floors Table](#the-floors-table) · [Migration Costs Between Choices](#migration-costs-between-choices)

## The Three Questions

Ask them in this order; most choices resolve at the first or second.

1. **Does a hard limit rule anything out?** A 60-minute ceiling, a 400 KB item, a single-writer document, a fixed row key. Limits eliminate options for free (SKILL.md, Limits That Force Designs).
2. **Does anything here have a floor?** Bigtable, Spanner, Composer, Filestore, Dataproc-as-a-standing-cluster and a Vertex AI endpoint all bill from a minimum whether used or not. A floor turns a small workload into a subscription.
3. **Where is the break-even?** For everything that survives, compute the crossover from the user's actual numbers. State the number in the recommendation — "Cloud Run below roughly X requests per second, GKE above it, and here is why" is an answer; "Cloud Run is simpler" is a preference.

## Compute

| Option | Bills for | Choose when | Avoid when |
|---|---|---|---|
| Cloud Run service | Request-time CPU and memory, scales to zero | Request-shaped work, variable traffic, small teams | Steady 24/7 saturation, or Kubernetes APIs are required |
| Cloud Run job | Task duration, up to 24h per task | Batch, migrations, scheduled work with no HTTP surface | Anything needing sub-second startup |
| GKE Autopilot | Pod resource requests | Kubernetes ecosystem needed, mixed workloads, per-pod billing wanted | Privileged pods, node-level tuning, tiny footprints paying a cluster fee |
| GKE Standard | Nodes | Bin-packing at high utilization, GPU packing, custom kernels | Small teams without platform capacity |
| Compute Engine | VM-hours | Lift-and-shift, licensed software, anything needing a real machine | Anything that could scale to zero |
| Batch | Job resources | Large parallel batch with scheduling and dependencies | Interactive work |

**Cloud Run vs GKE, the honest arithmetic.** Cloud Run bills only while requests are in flight (with CPU-during-request), so a service at 5% duty cycle costs roughly 5% of the equivalent always-on node. As duty cycle rises the two converge, and past high sustained utilization a bin-packed node fleet with committed-use discounts wins — plus GKE's cluster fee is amortized across every workload on the cluster while Cloud Run has no fixed fee at all. Compute it as: (Cloud Run vCPU-seconds and GiB-seconds at the measured request volume and concurrency) versus (the node fleet that would serve the same peak, at its discounted price, plus the cluster fee divided by the number of workloads sharing it). The concurrency setting moves the Cloud Run side of that comparison more than anything else (`run.md`).

**Cloud Run vs Compute Engine** is rarely close: unless the workload needs a persistent local disk, a specific kernel, or licensed software tied to a machine, Cloud Run wins on both cost and operations.

## Machine Families and Discounts

| Family | Character | Discount behaviour |
|---|---|---|
| E2 | Cheapest list price, shared or fractional cores at the small end | **Earns no sustained-use discount** |
| N2 / N2D | General purpose, predictable | Sustained-use discount applies automatically |
| C3 / C4 and newer general-purpose | Higher per-core performance, newer platform | Sustained-use discount applies; availability varies by region |
| T2A / C4A (Arm) | Materially cheaper per core for workloads that run on Arm | Requires Arm-compatible images; most modern runtimes qualify |
| Memory-optimized (M-series) | High memory per core | For in-memory databases and analytics |
| Accelerator-attached | GPU or TPU | Quota starts at zero, capacity is scarce (`vertex.md`) |

The reflex that saves money: **an always-on workload should be compared on the discounted price, not the list price.** E2's cheaper hourly rate loses to a discounted N-series over a full month often enough that "E2 is the cheap one" is wrong as a default. For bursty or short-lived workloads, where the discount never accrues, E2 is genuinely the cheap one.

Arm is the other underused lever: for a stateless service on a modern runtime, rebuilding for Arm is usually a Dockerfile change and a substantial per-core saving. Test it rather than assuming compatibility problems that mostly no longer exist.

## Spot

- Deep discount, **30-second preemption notice**, no fixed maximum lifetime. The 30 seconds is the number that decides everything — it is far shorter than AWS's two minutes, and a design ported from there will lose data.
- Correct for: batch, CI runners, rendering, queue workers with idempotent handlers, and GKE node pools behind an on-demand baseline (`gke.md`).
- Wrong for: anything stateful that cannot drain in 30 seconds, and anything whose deadline is measured in a fixed window Google may not have capacity in.
- The requirement to make Spot safe: handle `SIGTERM` and finish or checkpoint within 30 seconds, and never hold the only copy of anything.
- Spot capacity is subject to the same regional scarcity as on-demand — a Spot request can fail for capacity, not just be preempted later.

## Data Stores

| Question | Answer |
|---|---|
| Relational, single-region, normal scale | Cloud SQL for PostgreSQL |
| Relational, analytics against live rows | AlloyDB |
| Relational, multi-region writes, strong consistency | Spanner — and only then, because the floor is real |
| Documents, mobile/web SDKs, scale to zero | Firestore |
| Wide-column, huge scale, one known access pattern | Bigtable — and only then, because of the node floor |
| Cache, sessions, rate limits | Memorystore |
| Analytics over large volumes | BigQuery |
| Objects | Cloud Storage |
| Shared POSIX filesystem | Filestore, reluctantly |

Two break-evens worth computing rather than asserting:

- **Firestore vs Cloud SQL** is a read-volume question, because Firestore bills per document read. Estimate documents read per user action × expected actions per month and price it against the smallest Cloud SQL tier that serves the same load. A read-heavy rendering pattern crosses over faster than people expect (`databases.md`).
- **Vertex AI vector search vs pgvector** is a corpus-size and latency question. The managed index has an hourly serving floor; pgvector in an existing Cloud SQL or AlloyDB instance is marginal cost. For a modest corpus with relaxed latency, pgvector wins by an order of magnitude (`vertex.md`).

## Messaging and Orchestration

| Need | Pick | Tell |
|---|---|---|
| Fan-out of events to independent consumers | Pub/Sub | Every consumer needs its own subscription |
| Controlled-rate work queue, per-item scheduling | Cloud Tasks | "No more than N per second, retry this one later" |
| A few steps with branching and retries | Workflows | Cents per month; replaces most small Airflow installs |
| Stateful stream or big batch transform | Dataflow | Windows, watermarks, autoscaling |
| Dependency DAGs with backfills | Composer | Only when the floor is justified |
| Existing Spark / Hadoop | Dataproc, ephemeral clusters | A standing cluster is a floor; an ephemeral one is not |

Full treatment and the failure modes: `pipelines.md`.

## Analytics

- **BigQuery** for anything warehouse-shaped. The choice inside it is on-demand versus editions, and it is arithmetic on a representative month's bytes billed (`bigquery.md`).
- **AlloyDB** when the analytics run against live operational data and an ETL hop is the thing you are trying to avoid.
- **Dataproc** when Spark or Hadoop code already exists. Ephemeral job-scoped clusters cost nothing between jobs; a standing cluster is a floor nobody chose deliberately.
- **Looker Studio** is free and adequate for internal dashboards, and every refresh is a BigQuery scan. A dashboard on a short auto-refresh against a raw table is the single most common BigQuery cost incident — put a materialized view or a scheduled aggregate between them.

## The Floors Table

Services that bill from a minimum capacity, regardless of use. Check this before choosing, not after the first invoice.

| Service | Floor is | Consequence |
|---|---|---|
| Bigtable | One node minimum | A small workload pays a monthly subscription |
| Spanner | A minimum processing-unit allocation | Same, at a lower but still real level |
| Composer | The environment (scheduler, web server, database) | Hundreds a month whether DAGs run or not |
| Filestore | Provisioned capacity per tier | Bills from creation, continuously |
| Memorystore | Provisioned capacity | Bills while idle |
| Vertex AI endpoint | Minimum replica count | Bills at zero traffic (`vertex.md`) |
| GKE cluster | Per-cluster management fee, with a credit covering roughly one zonal cluster | Ten small clusters pay it ten times |
| Cloud Run `min-instances` | The instances kept warm | Forfeits scale-to-zero and the free allowance |
| Cloud NAT | Hourly gateway charge | Bills with no traffic (`networking.md`) |
| BigQuery editions baseline | Baseline slots | Idle slots are paid slots |

Everything not in this table scales to something close to zero. That property is worth real money for anything that is not continuously busy, and it is the strongest reason to prefer Cloud Run, Firestore, BigQuery on-demand, Pub/Sub, Workflows and Cloud Storage for a young system.

## Migration Costs Between Choices

Reversibility should weigh in the decision, because some of these choices are effectively permanent.

| From → To | Difficulty |
|---|---|
| Cloud Run → GKE | Low. The container is the same; the surrounding configuration is the work |
| GKE → Cloud Run | Low to medium, unless Kubernetes APIs are load-bearing |
| Cloud SQL → AlloyDB | Low. Postgres to Postgres |
| Cloud SQL → Spanner | High. Different SQL dialect, schema model and transaction semantics |
| Firestore → anything | High. No SQL, no joins, and the data model was shaped by the pricing |
| Bigtable → anything | Very high. The row key is the schema |
| BigQuery on-demand → editions | Trivial. A billing setting |
| BigQuery dataset between regions | Medium. A copy, plus egress, plus every reference updated |
| Composer → Workflows | Medium. Rewriting DAGs as state machines, one at a time |
| Single project → organization | High. Every binding re-granted, every policy re-evaluated (`organization.md`) |

The pattern: **compute choices are reversible, data choices mostly are not.** Spend the design time on the data layer, and be willing to change the compute layer later.

Whenever a selection decision is made with real numbers behind it, write it to `~/Clawic/data/gcp/artifacts/decision-<name>.md` — the choice, the rejected alternative, the break-even that decided it, the estimated monthly cost with its region, and the first quota and timeout it will hit — and add its `## Boxes` line in the same turn. It is what stops the same argument being reopened every quarter (`memory-template.md`).
