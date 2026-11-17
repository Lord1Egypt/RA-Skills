# Observability — Signals That Answer Questions, At A Price You Chose

Scope: what to instrument, what each signal answers, and what it costs. Turning signals into objectives and pages is `slos.md`. `observability_stack` in `config.yaml` sets the query dialect and the cost model.

**Before proposing instrumentation or a dashboard**, read `## Delivery Setup` in `~/Clawic/data/devops/memory.md` (which stack, which paging provider), `## SLOs` (which SLIs already exist and where each is measured), and `## Pain Points` — the questions this team could not answer during past incidents are the instrumentation backlog.

**Contents:** [The Three Signals](#the-three-signals) · [Instrument The Journey, Not The Function](#instrument-the-journey-not-the-function) · [Cardinality Is The Bill](#cardinality-is-the-bill) · [Logs](#logs) · [Traces](#traces) · [Dashboards People Actually Use](#dashboards-people-actually-use) · [Cost Control](#cost-control)

## The Three Signals

| Signal | Answers | Costs scale with | Fails at |
|---|---|---|---|
| Metrics | "Is it broken, how much, since when" | Number of unique series (cardinality × retention) | Explaining *why*; no per-request detail |
| Logs | "What exactly happened to this request" | Volume ingested, then storage | Aggregation at scale; expensive to query broadly |
| Traces | "Where did the time go across services" | Spans × sampling rate | Answering rate questions; sampled data misses rare cases |

Start with metrics for the SLI, logs for the detail, traces when more than two services are on the request path. Each additional signal is a recurring bill and a maintenance burden — adopt one when a question you actually had went unanswered.

Events (deploys, config changes, flag flips, scaling actions) are the fourth, cheapest, most under-used signal: an annotated timeline of changes explains most incidents faster than any dashboard, because the change that precedes the symptom is the suspect (SKILL.md Failure Signatures).

## Instrument The Journey, Not The Function

- Measure at the boundary the user experiences: request rate, error ratio, latency distribution, and saturation of the resource that runs out first — the four golden signals, per service and per critical endpoint.
- One SLI per user journey beats fifty per service. "Checkout completes in under 2s" is actionable; "average CPU" is not.
- Errors must be counted by whether the *user* failed, not whether a function threw. A retried failure that eventually succeeded is not a user-visible error; a 200 with an empty body may be one.
- Latency is a distribution: record percentiles or a histogram, never only an average. An average hides a 5% cohort at 10× latency, which is exactly the cohort that complains.
- Instrument what you will page on first; everything else can wait for a real question.

## Cardinality Is The Bill

A metric's cost is one time series per unique combination of label values: `series = ∏ (distinct values per label)`. Ten endpoints × 5 status classes × 3 regions = 150 series, fine. Add `user_id` at 50,000 users and it is 7.5 million series — a bill and, in most systems, an outage of the metrics backend itself.

- Never label with unbounded values: user id, request id, email, full URL path with parameters, error message text.
- Bound the ones that look small but are not: `status_code` (use classes), `endpoint` (use the route template, never the raw path), `version` (drops old series slowly — check retention).
- High-cardinality questions belong in logs or traces, which are priced per event rather than per series.
- Before adding a label, multiply. The arithmetic takes ten seconds and prevents most metrics-cost incidents.

## Logs

- **Structured (JSON), one event per line, with a request/trace id.** Grep works; queries work better, and the id is what stitches a request across services.
- Log level is the cost dial: ingestion is typically the dominant charge and debug logging can be an order of magnitude above info. A service emitting 1 GB/day of debug logs is a line item on its own.
- Sample high-volume, low-information events (health checks, successful polls) and keep every error. Uniform sampling of errors is how the one occurrence you needed disappears.
- Never log secrets, tokens, or full request bodies; scrubbing is verified with a deliberate test event (`secrets.md`).
- Retention is two decisions, not one: hot searchable window (days to weeks) and cold archive (months, cheap, slow). `compliance_regime` may set a floor for the second.
- Log to stdout and let the platform ship it. Applications that write and rotate their own files lose data during crashes and fill disks.

## Traces

- Adopt when a request crosses three or more services, or when latency is the problem and you cannot say which hop owns it.
- Context propagation is the whole feature: a broken header chain gives you disconnected spans and no answer. Verify propagation across every hop *including* queues and async workers, where it usually breaks.
- Head sampling (decide at the start) is cheap and misses rare errors; tail sampling (decide after seeing the trace) keeps the interesting ones and needs a collector holding spans in memory. Choose deliberately; a 1% head sample cannot debug a 0.1% failure.
- Span attributes are subject to the same cardinality economics as metric labels, but priced per span — high-cardinality context belongs here rather than in metrics.
- Instrument the client-visible boundary and the slow internal hops first; auto-instrumentation everywhere produces noise and a surprising bill.

## Dashboards People Actually Use

- **One overview dashboard per service**, answering in a glance: is it up, is it fast, is it erroring, is it saturated, what changed. If it does not fit one screen, it is a report, not a dashboard.
- Every panel earns its place by answering a question someone asked during an incident. Panels added "for completeness" train people to ignore the screen.
- Annotate deploys and config changes on the time axis. This single feature shortens more incidents than any additional metric.
- Link each alert to the dashboard and the runbook that resolve it (`incidents.md`); a page with no link costs the responder minutes of navigation at the worst time.
- Review dashboards after each incident: whichever panel was missing is the one to add, and whichever nobody looked at can go.

## Cost Control

- Price the question before instrumenting: what is the retention, the cardinality, and the per-GB or per-series rate? Observability bills routinely rival compute bills, and they grow silently with traffic.
- The three levers, in order of effect: log level and sampling, metric cardinality, retention. Retention feels like the obvious cut and is usually the smallest of the three.
- Set a budget per service and review it on a cadence; the review is a row in `## Due` and the monthly figure belongs in the shared `~/Clawic/data/finances/subscriptions.md`.
- Self-hosted is not free: storage, scaling, and the on-call burden of the observability system itself — which, when it fails, fails during the incident you needed it for.

**Write in the same turn**: the stack and the paging provider go in `## Delivery Setup` of `~/Clawic/data/devops/memory.md`; every SLI and the point it is measured at goes in `## SLOs`, which is its only home (`slos.md`) — never restated per service; the monthly observability spend goes in `~/Clawic/data/finances/subscriptions.md` with its currency (protocol in `memory-template.md`); a dashboard or instrumentation decision worth re-reading becomes `artifacts/<kebab-name>.md` with its `## Boxes` line; a question an incident could not answer goes in `## Pain Points`.
