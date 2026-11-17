# Pipelines — Pub/Sub, Dataflow, Workflows, Composer, Datastream

Data movement and orchestration. The recurring mistake in this area is not technical: it is reaching for the heavyweight tool for a job that Cloud Scheduler plus Workflows would do for a few dollars a year.

**Contents:** [Pick the Orchestrator by Weight](#pick-the-orchestrator-by-weight) · [Pub/Sub](#pubsub) · [Delivery Semantics and Idempotency](#delivery-semantics-and-idempotency) · [Dataflow](#dataflow) · [Workflows](#workflows) · [Cloud Tasks vs Pub/Sub](#cloud-tasks-vs-pubsub) · [Composer](#composer) · [Datastream and CDC](#datastream-and-cdc) · [Dataproc](#dataproc) · [Pipeline Failure Modes](#pipeline-failure-modes)

## Pick the Orchestrator by Weight

| Need | Tool | Monthly floor |
|---|---|---|
| Run one thing on a schedule | Cloud Scheduler → Cloud Run job | Cents |
| A handful of steps with branching, retries and error handling | Workflows (+ Scheduler for the trigger) | Cents to a few dollars |
| Per-item queue with rate control and per-task retry | Cloud Tasks | Near zero |
| Fan-out of events to many consumers | Pub/Sub | Per GB, no floor |
| Stateful stream or large batch transform | Dataflow | Per worker-hour, scales to zero between jobs |
| Real DAGs: dependencies, backfills, a UI operators live in | Composer | Hundreds, running or idle |
| Existing Spark or Hadoop jobs | Dataproc | Per cluster-hour; ephemeral clusters cost nothing between jobs |

The rule: **start at the top of this table and move down only when a specific requirement forces it.** Composer's floor is charged whether a DAG runs or not, so a nightly job in Airflow can cost a hundred times what the same job costs in Scheduler plus Workflows. Backfills and inter-task dependency graphs are the honest reasons to pay it; "the team knows Airflow" is a real reason too, and worth pricing openly rather than pretending.

## Pub/Sub

- **Topics and subscriptions are independent.** Each subscription gets its own copy of every message and its own backlog. Adding a consumer means adding a subscription, never sharing one — two consumers on one subscription split the messages between them, which is a load-balancing pattern, not a fan-out pattern.
- **Push vs pull.** Push delivers to an HTTPS endpoint and the response code is the ack — simple, and the endpoint's latency becomes the throughput limit. Pull lets the consumer control rate and batch, and is what a high-throughput worker should use. Push into Cloud Run is the common serverless shape (`run.md`).
- **Ack deadline** defaults to 10 seconds and extends to 600. A handler slower than the deadline gets its message redelivered while it is still working, which manifests as duplicate processing under load and nothing at all under test. Client libraries extend the deadline automatically while a message is held — do not rely on that when the handler is an HTTP push endpoint.
- **Retention**: unacked messages are retained up to a configurable maximum; a subscription can also retain acked messages to allow replay by timestamp or by snapshot. Turning on message retention before a risky deploy is a cheap undo button.
- **Dead-letter topics** stop a poison message from retrying forever. Set the maximum delivery attempts, and put a subscription on the dead-letter topic — a dead-letter topic nobody reads is a silent data-loss mechanism.
- **Ordering keys** guarantee order within a key, and serialize that key's throughput. Order and parallelism trade against each other; pick the key so that "in order" applies to the smallest scope that is actually required.
- **Exactly-once delivery** is available per subscription within a region. It reduces duplicates but does not remove the need for idempotent handlers, because your own retries and redeployments still exist.
- Pricing is per GiB of message data, with message overhead counted per message — millions of tiny messages cost more than the payload sizes suggest.

## Delivery Semantics and Idempotency

Everything event-driven on GCP is at-least-once unless it says otherwise, so idempotency is a design requirement, not a defensive extra.

- **Key on the event id**, not on a timestamp or on message content. Pub/Sub's message id is stable across redeliveries of the same publish.
- **Deduplicate at the destination where possible**: an upsert keyed on the event id costs nothing extra; a separate dedupe store is another thing to operate.
- **Make the side effect idempotent, or make it recorded.** Sending an email twice is a user-visible bug; writing a row twice is a data bug; charging a card twice is a company problem. The cost of a duplicate determines how much machinery is justified.
- **Retry storms are a cost event.** A handler that fails on every message retries at full rate until retention expires, multiplying compute, logging and downstream load. Dead-letter after a small number of attempts and alert on the dead-letter backlog.
- Alert on **oldest unacked message age**, not on backlog size. Backlog size is normal during a burst; a message that has been unacked for an hour is always a problem.

## Dataflow

Managed Apache Beam. One programming model for batch and streaming, which is the reason to accept its learning curve.

- **Streaming Engine** moves shuffle and state off the worker VMs. It is the default for new streaming jobs and it decouples worker sizing from state size — without it, a growing state forces bigger workers.
- **Autoscaling** works on backlog and CPU. It cannot scale past the parallelism the source offers: a Pub/Sub subscription scales well, a single unsplittable file does not. A job stuck at one worker is usually a source parallelism problem, not an autoscaler problem.
- **Windows, triggers and watermarks** are the actual difficulty. Late data is dropped by default past the allowed lateness — a correctness decision hiding inside a default. Set allowed lateness deliberately and route late elements somewhere visible.
- **Hot keys** stall a job the way they stall any distributed system: one key does all the work while the rest of the fleet idles. Dataflow logs a hot-key warning; act on it with a salted key or a combiner.
- **Updating a streaming job** in place preserves state only when the transform graph is compatible; incompatible changes require draining (finish in-flight work, then stop) or cancelling (drop it). Drain is what you want in production, and it can take a while.
- **Templates** (Flex Templates, and the Google-provided catalog) let a pipeline be launched without a build step. The provided templates cover the common paths — Pub/Sub to BigQuery, Cloud Storage to BigQuery, Datastream to BigQuery — and are usually better than writing the same pipeline yourself.
- Cost is worker-hours plus Streaming Engine and shuffle. A streaming job bills continuously, so a low-volume stream may be cheaper as a scheduled micro-batch.

## Workflows

A serverless state machine defined in YAML, billed per step, with a free allowance that covers most orchestration.

- Right for: sequencing API calls, calling Cloud Run jobs, waiting on long operations, branching on results, retrying with backoff, and catching errors with a compensating action.
- It has real control flow — conditionals, loops, subworkflows, parallel branches — and native support for polling long-running operations, which is the part people hand-roll badly.
- Connectors for GCP services handle authentication and long-running-operation polling for you; prefer a connector over a raw HTTP call.
- Not right for: high-volume per-item processing (that is Pub/Sub or Cloud Tasks), or dependency graphs with backfill requirements (that is Composer).
- Combined with Cloud Scheduler it replaces most small Airflow installations at a rounding-error cost, which is the single biggest saving available in this file.

## Cloud Tasks vs Pub/Sub

They look similar and solve different problems.

| | Pub/Sub | Cloud Tasks |
|---|---|---|
| Model | Publish/subscribe, fan-out | Named task queue, one target |
| Consumer control | Subscription-level | Per-queue rate limit and concurrency cap |
| Per-item scheduling | No | Yes — schedule a task for a future time |
| Deduplication | No (idempotency is yours) | Task names give a dedupe window |
| Typical use | Events many things care about | Work one service must do, at a controlled rate |

The tell: if you need to say "no more than 50 of these per second, and retry this one in an hour", it is Cloud Tasks. If you need "everyone who cares about this event gets it", it is Pub/Sub.

## Composer

Managed Airflow. Pay for it deliberately.

- The floor is the environment, not the DAGs: a small environment costs hundreds a month idle, because it runs a scheduler, a web server and a database continuously.
- Genuine reasons to pay it: dependency graphs across many systems, backfills over historical dates, a UI that operators use daily, and an existing Airflow codebase.
- **Version upgrades are the operational cost.** Airflow major versions change operator imports and DAG syntax; Composer upgrades are a planned project, not a maintenance window.
- Keep DAG files small and free of top-level work: Airflow parses every DAG file on a schedule, so an expensive import or an API call at module scope is executed constantly and is the usual cause of a slow scheduler.
- Use Composer to *trigger* work that runs elsewhere (Cloud Run jobs, Dataflow, BigQuery) rather than to *do* work on its workers. The workers are the smallest and least scalable part of the environment.

## Datastream and CDC

- Serverless change data capture from operational databases into BigQuery or Cloud Storage, using the source's replication log.
- **The source must be configured for it**: logical replication and a replication slot on Postgres, binary logging on MySQL. A replication slot with no consumer causes the source's write-ahead log to grow until the disk fills — this takes down the production database, and it is the main operational risk of CDC.
- The initial backfill is a full read of the source and is heavy; schedule it, and expect the source to feel it.
- Schema drift is handled for common cases (added columns) and not for others (type changes, dropped columns). Decide the policy before the first `ALTER TABLE`.
- Into BigQuery, Datastream writes a merged, current-state table — which is what most people want, and is not a full history unless you configure it that way.
- The alternative for simple cases is a scheduled export plus a batch load, which is free to ingest and has no replication slot to babysit (`bigquery.md`).

## Pipeline Failure Modes

| Symptom | Cause | Move |
|---|---|---|
| Backlog grows steadily | Consumer throughput below publish rate | Scale the consumer; check for a hot key or a per-message external call |
| Backlog spikes then drains, repeatedly | Bursty source plus a consumer that scales too slowly | Raise minimum instances or workers; batch on the consumer side |
| Duplicate rows downstream | At-least-once delivery, no idempotency | Upsert keyed on event id |
| Messages lost | Acked before the work completed, or dead-lettered with nobody reading | Ack after the side effect; put a subscription on the dead-letter topic |
| Dataflow job stuck at one worker | Source parallelism, not autoscaling | Split the source; check for an unsplittable file or a single-partition read |
| Streaming job's state grows without bound | A window that never closes, or a key space that never stops growing | Bound the state; check allowed lateness and key cardinality |
| Everything downstream fails after a deploy | Schema change with no compatibility path | Schema registry or a versioned payload; expand-then-contract, never in place |
| Costs jumped with no volume change | A retry storm, or streaming inserts where a batch load would do | Dead-letter policy; check the ingest path (`bigquery.md`) |
| The source database's disk is filling | An orphaned replication slot from a CDC job that stopped | Drop the slot or restart the consumer — this is urgent |

Alert on **oldest unacked message age**, **dead-letter topic backlog**, **watermark lag** for streaming jobs, and **replication slot lag** for CDC. Those four cover almost every real pipeline incident (`production.md`).

When a pipeline is created or its shape changes, update `## Current Infrastructure` in `~/Clawic/data/gcp/memory.md`. A design decision with a rejected alternative — Workflows over Composer, Cloud Tasks over Pub/Sub, and why — goes to `~/Clawic/data/gcp/artifacts/decision-<name>.md` with its monthly cost and its `## Boxes` line (`memory-template.md`). That note is what stops the same argument being had again in six months.
