# Capacity — Will It Hold, And What Breaks First

Scope: sizing, load testing, autoscaling, and launch readiness. Reliability targets are `slos.md`; recovery from failure is `recovery.md`.

**Before sizing or planning a launch**, read `~/Clawic/data/servers/servers.md` (what exists and what it costs), `## Services` in `~/Clawic/data/devops/memory.md` (limits already discovered), and `## Pain Points` — the ceiling that bit last time is usually the one about to bite again.

**Contents:** [Size From Arithmetic](#size-from-arithmetic) · [Utilization Ceilings](#utilization-ceilings) · [Find The First Ceiling](#find-the-first-ceiling) · [Load Testing](#load-testing) · [Autoscaling](#autoscaling) · [Timeouts, Retries, And Backpressure](#timeouts-retries-and-backpressure) · [Launch Readiness](#launch-readiness)

## Size From Arithmetic

Little's law is the whole first pass: **concurrency = arrival rate × service time**.

- 200 req/s at 150 ms average → 30 requests in flight. A pool of 20 workers is already the bottleneck; 40 leaves headroom.
- Connection pools follow the same law and are the most common invisible ceiling: total pool size across all instances must stay under the database's connection limit — `instances × pool_size ≤ max_connections − reserved`. Autoscaling from 4 to 20 instances multiplies pool demand by 5 and exhausts the database while every instance looks healthy.
- Convert traffic to resources per unit: memory per in-flight request, CPU-seconds per request, bytes per request. Peak = average × peak-to-mean ratio, measured from real traffic, not assumed (a consumer product's daily peak is commonly 2-4× its mean; a business tool's can exceed 10× against a nightly-idle baseline).
- Always size against the *peak minute*, not the hourly average. Aggregation hides exactly the spike that breaks things.

## Utilization Ceilings

Queueing theory sets the ceiling, and it is lower than intuition. For a simple queue, waiting time scales with `ρ/(1−ρ)` where ρ is utilization: at 50% utilization the queue wait equals one service time, at 80% it is 4×, at 90% it is 9×.

| Utilization | Queue wait (× service time) | Verdict |
|---|---|---|
| 50% | 1× | Comfortable |
| 70% | ~2.3× | Normal steady-state target |
| 80% | 4× | Latency already visibly degraded |
| 90% | 9× | One traffic bump from a queue collapse |

- Target 60-70% steady-state utilization for latency-sensitive services; batch systems can run hotter because queueing costs them nothing user-visible.
- The knee is sharp and non-linear: the difference between 80% and 90% is not "a bit slower", it is a doubling of wait time. This is why "we still have 15% CPU headroom" is not a safe statement.
- Headroom must cover the failure case: with N instances, losing one moves the rest to `N/(N−1)` of their previous load. Three instances at 70% become 105% when one dies.

## Find The First Ceiling

Every design hits one limit before all others. Name it and its current value, or the design is not finished (this is the sizing twin of SKILL.md Rule 8's cadence discipline).

| Candidate ceiling | How it announces itself |
|---|---|
| Database connections | Connection-refused errors while CPU is idle |
| Thread/worker pool | Latency rises with queueing, throughput flat |
| Single-writer database | Write latency climbs, read replicas are bored |
| Provider quota (API rate, IP count, instance count) | Throttling errors, or capacity requests denied at the worst time |
| File descriptors / sockets | Errors under load only, often after a deploy |
| Payload or message size caps | Works for small inputs, fails for the important customer |
| Lock contention on a hot row | Throughput plateaus and then falls as load increases |
| Egress bandwidth | Everything slow, nothing saturated on the dashboard |

Quota increases are not instant — request headroom before the launch, not during it.

## Load Testing

- **Model the journey, not the endpoint.** Hammering `/health` proves nothing. Replay a realistic mix with realistic think time and realistic payload sizes.
- **Data volume matters as much as request rate**: run against production-shaped cardinality, or the query plans are fiction (`environments.md`).
- Three tests answer different questions: *load* (does it meet the SLO at expected peak), *stress* (where does it break, and how — gracefully or catastrophically), *soak* (does it survive 8-24 hours: leaks, log disks, connection churn, token expiry).
- Ramp gradually, and watch the derivative: the interesting moment is where latency's slope changes, not where errors start.
- Test the whole path including the CDN, proxy, and authentication. Load tests that bypass the front door miss the component that actually saturates.
- Warn everyone and mark the traffic, or you will page the on-call and pollute the SLI. Excluding synthetic traffic from the SLI is a deliberate decision, written into that objective's `SLI` cell in `## SLOs` of `~/Clawic/data/devops/memory.md` (`slos.md`).

## Autoscaling

- **Scale-out must be faster than the traffic can double.** If instances take 3 minutes to become healthy and traffic doubles in 5, the target utilization must leave a full doubling of headroom — roughly 50%, not 80%. Measure boot-to-healthy including image pull, warm-up, and cache fill.
- Scale on the signal that saturates: request concurrency or queue depth usually beats CPU. CPU-based scaling is blind to I/O-bound saturation, which is most web services.
- Asymmetric thresholds: scale out fast, scale in slowly (a cooldown of several minutes) — flapping costs more than a few extra instances.
- Set the maximum deliberately, and make it a cost decision reviewed by a human. An unbounded maximum turns a retry storm or a bot into a five-figure surprise.
- Minimum replicas above one for anything user-facing: scale-from-zero adds cold-start latency exactly when demand arrives.
- Everything downstream must survive the scaled-out fleet: connection pools, third-party rate limits, and license counts (see the pool arithmetic above).

## Timeouts, Retries, And Backpressure

The mechanism by which a small failure becomes an outage.

- **Timeout budgets shrink per hop.** If the user-facing timeout is 3s and the chain is A→B→C, then C's must be well under B's, which is under A's. Equal timeouts everywhere mean the whole chain waits for the slowest and the user gets nothing.
- **Retries multiply load precisely when the system is weakest.** Total attempts = `1 + retries` per hop, and they compound across hops: two retries at three levels is up to 27 requests from one user action.
- Cap retries as a fraction of traffic (a retry budget of ~10% of requests is a common ceiling), use exponential backoff **with jitter** (synchronized retries re-create the spike), and never retry non-idempotent operations without an idempotency key.
- Circuit breakers stop a dead dependency from consuming every worker: trip on an error-rate threshold, half-open with a trickle of probes, and make the tripped state a visible metric.
- Load shedding beats collapse: reject the excess early with a fast error rather than queue everything and time out. A service that serves 70% of traffic correctly during a spike beats one that serves 0% slowly.
- Bound every queue. An unbounded queue converts a throughput problem into a memory outage and a latency problem nobody can see the end of.

## Launch Readiness

The checklist for anything with an announced date:

| Check | Evidence needed |
|---|---|
| Expected peak, from a stated assumption | The number and where it came from |
| Load test at 2× that peak passed | Test results, with the SLI measured |
| First ceiling named with its current value | The quota or limit, plus the headroom request if needed |
| Autoscaling limits set, boot-to-healthy measured | The measured seconds, not an estimate |
| Rollback rehearsed, artifact identity recorded | The release row (`deploys.md`) |
| SLI, alerts, and dashboard live before launch, not after | Alert fired at least once in a test |
| On-call informed, runbook written, escalation known | The runbook artifact (`incidents.md`) |
| Cost at expected and at 2× peak | Two monthly figures with their currency |
| Third-party limits raised and confirmed in writing | The confirmation, with the date |

**Write in the same turn**: measured limits, boot-to-healthy times, peak-to-mean ratios, and the first ceiling per service go in `## Services` of `~/Clawic/data/devops/memory.md` — these are exactly the numbers re-derived from scratch every six months otherwise. Load-test results and a launch-readiness review become `artifacts/<kebab-name>.md` with their `## Boxes` line; machines and their monthly cost with currency go in `~/Clawic/data/servers/servers.md`; a saturation surprise goes in `## Pain Points` (`memory-template.md`).
