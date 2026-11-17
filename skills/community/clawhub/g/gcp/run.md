# Cloud Run — Services, Jobs, and Functions

Cloud Run is GCP's default compute answer and the platform's best product. Cloud Run functions (formerly Cloud Functions gen2) are the same runtime with a different deployment surface, so almost everything here applies to both.

**Contents:** [The Container Contract](#the-container-contract) · [Concurrency Is the Dial That Matters](#concurrency-is-the-dial-that-matters) · [CPU Allocation and Cold Starts](#cpu-allocation-and-cold-starts) · [Revisions and Traffic](#revisions-and-traffic) · [Reaching a VPC](#reaching-a-vpc) · [Jobs](#jobs) · [Functions: Gen1 vs Gen2](#functions-gen1-vs-gen2) · [Eventarc and Pub/Sub Triggers](#eventarc-and-pubsub-triggers) · [Cost Model](#cost-model) · [Production Checklist](#production-checklist)

## The Container Contract

Four requirements. Violating any one produces the same unhelpful deploy failure.

1. **Listen on `$PORT`** (8080 unless overridden) **on `0.0.0.0`**. Binding to `127.0.0.1` is the number-one Cloud Run deploy failure: the container runs perfectly on a laptop and never becomes ready in Cloud Run.
2. **Start within the startup window.** A framework that loads a large model or warms a connection pool before binding the port will fail the check. Bind the port first, warm afterwards, and configure a startup probe with a realistic failure threshold rather than raising the request timeout.
3. **Be stateless between requests.** The instance filesystem is in-memory — writing to it consumes the memory limit and counts toward the container's allocation. Temporary files of any size go to Cloud Storage.
4. **Handle `SIGTERM`.** Instances are shut down when scaling in or when a revision is replaced. Draining in-flight requests and closing pool connections cleanly is the difference between a silent deploy and a burst of 502s.

## Concurrency Is the Dial That Matters

Cloud Run sends up to `concurrency` simultaneous requests to one instance — the default is 80, the maximum is 1000, and a value of 1 makes it behave like a classic function-per-request platform.

- **Cost scales with instance-time, not request count.** Doubling concurrency roughly halves the instance count and therefore the bill, for a workload whose bottleneck is waiting on I/O.
- **The right value comes from the bottleneck.** I/O-bound service (calling a database or an API) → high concurrency is free throughput. CPU-bound service (image processing, inference) → concurrency above the core count just adds latency; drop it toward 1-4.
- **Concurrency multiplies every downstream limit.** Instances × concurrency is the peak number of database connections, of API calls, of file handles. A service scaling to 100 instances at concurrency 80 can open 8,000 connections to a database whose ceiling is 400 (`databases.md`).
- **Set `max-instances` deliberately.** The default cap exists to stop a runaway from bankrupting you, and it is also what limits downstream damage. Compute it from the downstream ceiling, then verify against the concurrency math above.
- **Memory is per instance, shared by all concurrent requests on it.** A service that needs 200 MB per request at concurrency 80 needs an instance far larger than the per-request figure suggests, and OOM shows up as sporadic 503s under load.

## CPU Allocation and Cold Starts

- **CPU allocated during requests only** (default): you pay for CPU while a request is in flight, and background work between requests is throttled to near zero. Async work started in a handler and not awaited will be paused mid-flight and may never finish — a classic source of "logs stop halfway".
- **CPU always allocated**: the instance keeps CPU between requests. Required for background processing, streaming responses that compute between chunks, and long-lived connections. Costs more per instance-second but is billed at a lower CPU rate — worth comparing rather than assuming.
- **CPU boost at startup** gives the instance extra CPU during initialization. The cheapest real fix for a slow-starting runtime.
- **`min-instances`** eliminates cold starts by keeping instances warm, and bills for them continuously at an idle rate. Set it only after measuring that cold start is a user-visible problem, and remember it forfeits the free tier and the scale-to-zero economics that made Cloud Run the default.
- Cold start reduction that costs nothing: smaller image, fewer layers, lazy-load anything not needed to serve the first request, avoid a runtime that reads a large dependency tree at boot, and keep the container's entrypoint from doing network calls.

## Revisions and Traffic

Every deploy creates an immutable revision. Traffic is a separate, instant assignment — and this is the rollback story.

- Deploy without serving: create the revision with no traffic, then send a tagged share of traffic to it. Each revision gets a stable tag URL for testing without affecting the main URL.
- Canary: shift a small percentage, watch error rate and latency, then move the rest. Rollback is a traffic reassignment, which takes effect in seconds and needs no rebuild.
- **The rollback artifact is the previous revision name.** Record it in `deploys/<year>.md` with the deploy row. A deploy row without the previous revision is a deploy with no written rollback plan (`memory-template.md`).
- Revisions retain their configuration, including environment variables and secrets bindings, so rolling back rolls back configuration too — which is usually what you want and occasionally a surprise when a secret's *value* changed underneath.
- Pin the image by **digest**, not by a mutable tag, in anything that claims to be reproducible.

## Reaching a VPC

Cloud Run runs outside your VPC by default. Two ways in:

| Mechanism | Use | Note |
|---|---|---|
| **Direct VPC egress** | The current default choice: the service gets addresses from a subnet, no connector to size or pay for | Consumes IPs from the subnet range — size it for peak instance count |
| **Serverless VPC Access connector** | Older path, still required in some configurations | A managed instance group you pay for and must size; throughput is bounded by its machine type and count |

- `vpc-egress` setting decides whether *all* traffic goes through the VPC or only private ranges. Sending all egress through the VPC routes internet traffic via Cloud NAT, which gives a stable outbound IP for third-party allowlists — and adds NAT data-processing charges (`costs.md`).
- Cloud SQL from Cloud Run: prefer the built-in connection over private IP, or the Cloud SQL Auth Proxy pattern. Either way, connection count is the constraint, not bandwidth (`databases.md`).

## Jobs

Cloud Run **jobs** run to completion instead of serving requests. Right for batch, migrations, scheduled reports and anything with no HTTP surface.

- Task-parallel: a job runs N tasks, each with an index available in the environment, so a shard-by-index pattern needs no coordinator.
- Task timeout reaches 24 hours, far past the service request ceiling — the correct escape hatch when a request-shaped design hits the limit.
- Retries are per task, with a configurable maximum. A task that is not idempotent will corrupt data on retry; make it idempotent or set retries to zero and handle failure explicitly.
- Trigger with Cloud Scheduler for cron, or from Workflows as a step (`pipelines.md`).
- Jobs are the answer to "my Cloud Run request times out": move the work, return immediately, and let the caller poll or receive a notification.

## Functions: Gen1 vs Gen2

| | Gen1 | Gen2 (Cloud Run functions) |
|---|---|---|
| Runtime | Legacy function infrastructure | Cloud Run underneath |
| Max duration | 9 minutes, hard | Up to 60 minutes for HTTP |
| Concurrency | One request per instance | Configurable, like any Cloud Run service |
| Traffic splitting | No | Yes, via revisions |
| Event sources | Direct triggers | Eventarc, which covers far more sources |

Gen1's 9-minute ceiling and single-request concurrency are the two reasons to migrate. Once on gen2 the mental model is simply Cloud Run, and everything above applies. New work should not start on gen1.

## Eventarc and Pub/Sub Triggers

- Eventarc delivers events from Cloud Audit Logs, Pub/Sub, Cloud Storage and other sources to a Cloud Run target as CloudEvents. Under the hood most paths are a Pub/Sub subscription, which is why the delivery semantics are Pub/Sub's.
- **At-least-once delivery means duplicates.** Handlers must be idempotent — key on the event id, not on a timestamp.
- **The ack deadline is the request timeout.** A push subscription that does not get a 2xx within the deadline redelivers; a slow handler therefore multiplies its own load. Match the subscription's ack deadline to the handler's real p99, and use a dead-letter topic so a poison message stops after N attempts instead of retrying forever (`pipelines.md`).
- **A retry storm is a cost event as well as an outage.** A handler failing on every message retries at full rate until the retention window expires; the bill and the log volume both spike.
- Audit-log-triggered functions fire on the control plane, not the data plane — "when a bucket object is created" is a Cloud Storage event, "when a bucket is created" is an audit log event. Choosing the wrong one produces a trigger that never fires.

## Cost Model

Billed on vCPU-seconds, memory GiB-seconds, and requests, with a monthly free allowance that covers a real side project — provided the service scales to zero.

- The three ways to lose the free tier and the scale-to-zero economics: `min-instances` above zero, always-allocated CPU on a low-traffic service, and a health check pinging the public URL frequently enough to keep an instance alive.
- Raising concurrency is usually the largest single cost lever, because instance-seconds fall proportionally for I/O-bound work.
- Over-provisioned memory costs continuously and buys nothing; measure the actual peak rather than rounding up "to be safe".
- Compare against GKE honestly: a Cloud Run service at steady high utilization can cost more than the equivalent nodes, and the crossover is a real number worth computing before a migration in either direction (`services.md`).

## Production Checklist

Before calling a Cloud Run service production:

- Listens on `$PORT` on `0.0.0.0`; startup probe tuned to real startup time; `SIGTERM` drains in-flight requests
- Concurrency set from the measured bottleneck, and instances × concurrency verified against every downstream ceiling
- `max-instances` computed from the downstream limit, not left at the default by accident
- Runs as a dedicated service account with only the roles it uses — never the default compute service account (`iam.md`)
- Image pinned by digest; the previous revision name recorded as the rollback target
- Secrets mounted from Secret Manager, never baked into the image or the revision's plain environment variables (`security.md`)
- Ingress restricted to internal or to the load balancer when the service is not meant to be public; unauthenticated invocation off unless it is genuinely a public endpoint
- Structured JSON logging to stdout, so Log Explorer filters work on fields rather than substrings (`debug.md`)
- Alerts on error rate and p99 latency, with the metric's absence treated as a condition (`production.md`)

Write every deploy into `~/Clawic/data/gcp/deploys/<year>.md`: date, service, image digest and commit, the new revision, and the previous revision as the rollback target. Anything the session had to figure out — a concurrency value derived from load testing, a startup fix that took hours — belongs in `~/Clawic/data/gcp/artifacts/` with its `## Boxes` line (`memory-template.md`).
