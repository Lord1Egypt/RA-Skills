# Vertex AI — Serving, Quota, and Not Paying for Idle GPUs

The AI platform is where GCP's cost surprises are largest per hour, because an endpoint bills for capacity rather than for use and accelerator quota starts at zero.

**Contents:** [Quota Starts at Zero](#quota-starts-at-zero) · [Capacity Is Not Quota](#capacity-is-not-quota) · [Online vs Batch](#online-vs-batch) · [Endpoints Bill While Idle](#endpoints-bill-while-idle) · [Model APIs vs Your Own Model](#model-apis-vs-your-own-model) · [Training Jobs](#training-jobs) · [Pipelines and Artifacts](#pipelines-and-artifacts) · [Data and Grounding](#data-and-grounding) · [Governance](#governance) · [Cost Checklist](#cost-checklist)

**Before requesting accelerators or sizing an endpoint**, read `## Quotas` in `~/Clawic/data/gcp/memory.md` — or `quotas.md` if `## Boxes` points there. It records what was already granted, in which project and region, and the observed peak that made the case.

## Quota Starts at Zero

Unlike CPU quota, accelerator quota in a fresh project is typically **zero**, per accelerator type, per region, and separately for training and for serving.

- Consequences: the first GPU job fails immediately with a quota error, an increase is a request with a human reviewer, and approval takes days rather than minutes. Plan the request before the sprint that needs it (SKILL.md Rule 8).
- Quota is granted per **accelerator type and region**, so an approval for one GPU family in one region does nothing for another. Ask for what will actually be used, in the region the data is in.
- Preemptible/Spot accelerator quota is separate from on-demand. A team can hold Spot quota and none on-demand, which produces confusing intermittent failures.
- A request with an observed usage number attached is approved far more often than one without. That is what the `Observed peak` column in `## Quotas` exists for.
- Record every request and grant — project, region, accelerator, limit, date — in `## Quotas` in the same turn. The alternative is re-requesting a quota you already hold in a project you forgot about.

## Capacity Is Not Quota

A resource-exhausted error at deploy time has two entirely different causes and the fix differs.

| Signal | Meaning | Fix |
|---|---|---|
| Quota exceeded, naming a limit and a value | You hold less quota than you asked for | Request an increase; nothing else works |
| Resources unavailable / zone exhausted, naming no limit | Google has none of that accelerator in that region right now | Different region, different accelerator type, or a reservation |

Scarce accelerator types are regularly capacity-constrained. For anything with a deadline, hold a **reservation** — capacity you pay for and that is there when you ask. A reservation is a commitment, so price it against the alternative of a slower accelerator that is actually available.

## Online vs Batch

The single largest cost decision in this file.

- **Online prediction** deploys a model to an endpoint with a minimum replica count and bills per node-hour for as long as it is deployed, traffic or not. Correct when a user is waiting.
- **Batch prediction** runs a job over a dataset, bills for the job's duration, and leaves nothing running. Correct for everything offline: nightly scoring, backfills, embeddings over a corpus, evaluation runs.
- Teams routinely deploy an endpoint for work that is offline, then pay for it for months. If nothing is waiting on the response, it is a batch job.
- For a low-traffic online use case, a model served from a Cloud Run service with CPU or a small accelerator scales to zero and can be dramatically cheaper than an endpoint with a minimum replica count — at the price of cold starts (`run.md`).

## Endpoints Bill While Idle

- **Minimum replicas below one** is the setting that allows scale to zero where the model and configuration support it. Where it does not, the minimum replica is a floor on the monthly bill.
- Autoscaling on an endpoint reacts to a utilization target. Set the maximum replica count against both cost and quota — an endpoint that cannot get accelerators will not scale regardless of the setting.
- **Undeploy between experiments.** The model stays in the registry; only the serving capacity goes away. Redeploying takes minutes and costs nothing to keep.
- **Traffic splitting** across model versions on one endpoint is how a new model is canaried. Both versions are deployed, so both are billed — plan the overlap window rather than leaving it open.
- Put "review deployed endpoints" in `## Due` alongside the monthly cost review. An idle endpoint is the single most expensive forgotten resource on the platform (`costs.md`).

## Model APIs vs Your Own Model

- **Managed model APIs** (the first-party generative models, and third-party models offered through the platform) bill per token or per request. No infrastructure, no quota request for accelerators, and cost scales exactly with use — the right starting point for almost every generative use case.
- **Provisioned throughput** buys reserved capacity for those APIs at a fixed price. It converts a variable bill into a predictable one and is worth it only above a stable, measured volume — the same commitment logic as everywhere else (`costs.md`).
- **Your own weights on an endpoint** makes sense for a fine-tuned or open model with steady traffic, a latency requirement the API cannot meet, or a residency requirement. It is a per-node-hour bill and an operations burden; be honest about both.
- Rate limits on managed APIs are per project and per region and are their own quota family. A production service should handle 429 with backoff and should have its limit raised before launch, not during it.
- Model versions change. Pin the version in code where reproducibility matters, and put the model's deprecation date in `## Due` if one is published.

## Training Jobs

- **Custom training jobs** run to completion and release their machines, so they are inherently cheaper than a standing cluster. Spot/preemptible accelerators cut the price substantially in exchange for interruption.
- **Checkpoint to Cloud Storage, always.** Without checkpoints, a preempted job loses everything and Spot is a false economy. With them, Spot is usually the correct default for training.
- Data loading is the usual bottleneck, not the accelerator. A GPU at 30% utilization is a data pipeline problem; measure before renting a bigger accelerator.
- **Hyperparameter tuning multiplies the bill by the number of trials.** Bound the trial count and use early stopping.
- Distributed training's inter-node traffic is real network cost and real latency; keep workers in one zone.

## Pipelines and Artifacts

- **Vertex AI Pipelines** runs containerized ML steps with caching: an unchanged step reuses its previous output instead of recomputing. That caching is the main reason to use it over a hand-rolled sequence of jobs.
- The **Model Registry** versions models and is what an endpoint deploys from. Deploying an ad-hoc artifact from a bucket works and leaves no lineage — which becomes the problem the first time someone asks which model produced a prediction.
- **Feature Store** is worth its cost when the same features are served online and used in training, and the training/serving skew is a real risk. Below that, it is infrastructure for its own sake.
- **Experiments and metadata** tracking costs nothing meaningful and answers "what did we try" months later. Turn it on at the start; it cannot be backfilled.

## Data and Grounding

- Keep the model and the data in the same region. Cross-region reads are billed egress and add latency to every call, and some regimes forbid the movement entirely.
- **Vector search** on the platform is a managed index with a per-hour serving cost, so it has a floor. For a modest corpus, pgvector in Cloud SQL or AlloyDB is materially cheaper and adequate; the managed index earns its price at scale and low latency (`databases.md`).
- Grounding against BigQuery or Cloud Storage means the query patterns of that store now apply — including bytes-scanned billing on every grounded call (`bigquery.md`).
- Training and tuning data in a bucket is subject to the same access controls and public-access risk as any other data. Fine-tuning data is often the most sensitive data an organization has (`storage.md`).

## Governance

- Run every AI workload as a dedicated service account with only the roles it uses, never the default compute service account (`iam.md`).
- Prompts, completions and training data may contain personal data. Where a compliance regime is set, that decides logging, retention and CMEK for these services exactly as it does for a database — the fact that it is an AI product changes nothing about the obligation (`security.md`).
- Data Access audit logging on the prediction services is off by default and is what answers "who called the model with what". Enable it where it matters, and price the log volume before enabling it everywhere.
- Where a regime names allowed regions, `constraints/gcp.resourceLocations` applies to these services too — and accelerator availability by region may conflict with it. Discover that conflict during design, not during a launch.

## Cost Checklist

Run with the monthly review (`costs.md`):

| Check | Action |
|---|---|
| Deployed endpoints | Every one justified by live traffic; undeploy the rest |
| Minimum replica counts | Above zero only where cold start was measured as a problem |
| Batch-eligible work running online | Move it to batch prediction |
| Training jobs on on-demand accelerators | Move to Spot with checkpointing, unless the deadline forbids it |
| Accelerator utilization during training | Below ~60% means a data pipeline problem, not a hardware problem |
| Provisioned throughput commitments | Utilization against the commitment; expiry date in `## Due` |
| Notebook and workbench instances | Idle instances left running overnight; enable idle shutdown |
| Vector index serving capacity | Justified by query volume, or replaced by pgvector |
| Quota held but unused | Recorded in `## Quotas` so it is not requested again elsewhere |

Every accelerator quota checked, requested or granted goes into `## Quotas` in `~/Clawic/data/gcp/memory.md` with its project, region, limit and observed peak. A serving architecture decided here — endpoint versus Cloud Run versus batch, with the monthly number and the rejected alternative — goes to `~/Clawic/data/gcp/artifacts/decision-<name>.md` with its `## Boxes` line (`memory-template.md`).
