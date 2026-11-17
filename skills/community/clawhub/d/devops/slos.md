# SLOs, Error Budgets, And Alerts That Deserve To Wake Someone

Scope: turning signals into a definition of "healthy", a budget, and a small number of pages. Instrumentation is `observability.md`; who carries the pager is `incidents.md`. `slo_target_pct` in `config.yaml` is the default target (99.9%).

**Before setting or changing an objective**, read `## SLOs` in `~/Clawic/data/devops/memory.md` — the current targets, their measured baselines, and the budget consumed this window — and `incidents/<year>.md` for what actually broke.

**Contents:** [Choose The SLI First](#choose-the-sli-first) · [Set The Target From Reality](#set-the-target-from-reality) · [Error Budget Arithmetic](#error-budget-arithmetic) · [Burn-Rate Alerting](#burn-rate-alerting) · [The Error Budget Policy](#the-error-budget-policy) · [Alert Hygiene](#alert-hygiene) · [Dependencies And Composite Availability](#dependencies-and-composite-availability)

## Choose The SLI First

An SLI is a ratio of good events to valid events, measured where the user is.

| Journey | Good event | Valid event | Measured at |
|---|---|---|---|
| Request/response API | Status < 500 and latency under threshold | All requests excluding client-caused 4xx | Load balancer or gateway, not inside the app |
| Async job | Completed within the freshness deadline | All enqueued jobs | Queue consumer |
| Data pipeline | Output produced, complete, on time | Each scheduled run | Output store |
| Batch/report | Delivered before its deadline | Each expected delivery | Delivery point |

- Measure as close to the user as you can afford. An in-process metric shows 100% availability while the load balancer serves 502s to everyone.
- Latency belongs *inside* the SLI, not beside it: "fast enough" is part of "working". A single threshold ("<300 ms") is usually enough; two-tier thresholds are worth it only when a slow-but-served response has real value.
- Exclude what the user caused (authentication failures, malformed requests) and be explicit about it — an SLI nobody agrees on gets argued about during the incident.
- One to three SLIs per service. Every extra one dilutes the meaning of "the service is meeting its objective".

## Set The Target From Reality

1. Measure the SLI for two to four weeks. That baseline is what you are actually delivering.
2. Set the target at or slightly above the baseline, never at an aspirational number. An SLO you breach every week trains everyone to ignore it.
3. Sanity-check against the users' actual need and the dependencies' own reliability (see composite availability below).
4. Revisit on a cadence (a row in `## Due`): raise it when you are comfortably beating it, and only when someone would pay for the difference.

Each additional nine costs roughly an order of magnitude more engineering. 99.9% is a well-run service with a normal team; 99.99% requires eliminating single points of failure, automated recovery faster than human response, and rehearsed failover. Do not set the target where the humans could not react in time even if perfect (see the 99.99% row below).

## Error Budget Arithmetic

Budget = `(1 − SLO) × window`. For a 30-day window (43,200 minutes):

| SLO | Budget / 30 days | Budget / week |
|---|---|---|
| 99% | 7 h 12 min | ~1 h 41 min |
| 99.5% | 3 h 36 min | ~50 min |
| 99.9% | 43.2 min | ~10 min |
| 99.95% | 21.6 min | ~5 min |
| 99.99% | 4.32 min | ~1 min |

For a request-ratio SLI the same arithmetic applies to requests: at 99.9% and 10M requests per month, the budget is 10,000 failed requests.

Rolling windows (trailing 30 days) beat calendar months: a calendar budget resets on the 1st and encourages risky deploys on the 2nd. State which you use — the two disagree constantly and the disagreement gets litigated during an incident.

## Burn-Rate Alerting

Burn rate = fraction of budget consumed per unit time, normalized so 1× exactly exhausts the budget over the window: `burn = (observed bad ratio) ÷ (1 − SLO)`.

| Budget consumed | Long window | Burn rate | Short window (confirm) | Action |
|---|---|---|---|---|
| 2% | 1 hour | 14.4× | 5 min | Page |
| 5% | 6 hours | 6× | 30 min | Page |
| 10% | 3 days | 1× | 6 hours | Ticket |

- Both windows must be breaching to fire. The short window stops an alert from remaining active for the rest of the long window after a blip has resolved.
- Worked example at 99.9%: `1 − SLO = 0.001`, so a 14.4× burn means 1.44% of requests failing for an hour. That is the number to state when someone asks what will page them.
- Fast-burn pages, slow-burn tickets. A slow burn is real degradation with hours of runway — waking someone for it costs more than it saves.
- Alert on the SLI you publish. An alert on a proxy metric drifts from the objective and eventually fires when the objective is fine, which is how teams learn to ignore pages.

## The Error Budget Policy

The objective is only real if exhausting it changes behavior. Write the policy, get it agreed by whoever owns the roadmap, and store it as an artifact:

| Budget state | Consequence |
|---|---|
| Healthy (> 50% remaining) | Normal delivery; risky changes allowed with a canary |
| Depleted (< 25% remaining) | Reliability work takes priority in the next planning cycle; risky changes need explicit sign-off |
| Exhausted | Feature deploys pause until the trailing window recovers; fixes and reliability work only |
| Consistently unused (near 100% every window) | The target is too low, or too much is being spent on reliability nobody needs — raise it or ship faster |

The last row is the one everyone forgets: a permanently unspent budget is a sign of over-investment, not of excellence.

## Alert Hygiene

- **Every page has a runbook link, an owner, and an action a human can take at 3am.** If the action is "look at it", it is a ticket, not a page.
- Cause-based alerts (CPU, memory, disk, restart count, queue depth) go to dashboards and tickets. The exception is a cause with a hard deadline and no symptom until it is too late — disk filling at a known rate, a certificate expiring — which pages *early*, with days of runway (`recovery.md`, `## Due`).
- Two numbers per rotation decide whether the alerting is working: pages per shift, and the fraction that led to action — the `Pages / shift` and `Actioned` columns of that objective's row in `## SLOs` of `memory.md`. A rotation above ~2 pages per 12-hour shift is not sustainable, and an action rate below half means the rules are wrong.
- Delete alerts. Every alert deleted must say what now covers that failure — usually the SLI burn rate, which is the point of having it.
- Test alerts by breaking things deliberately (`recovery.md`, game days). An alert that has never fired in anger is a hypothesis, and the most common failure is the alert depending on the very system that is down.
- Inhibition and grouping: when an upstream dependency pages, suppress the downstream pages it causes. Ten pages for one root cause is how a responder loses the first fifteen minutes.

## Dependencies And Composite Availability

Serial dependencies multiply: a service at 99.9% calling two dependencies each at 99.9% has a theoretical ceiling of `0.999³ ≈ 99.7%` — below its own target, before its own code fails at all.

- You cannot exceed the availability of a hard dependency. Either lower the target, make the dependency soft (cache, degrade, queue), or add redundancy.
- Independent redundancy adds nines: two paths each at 99% give `1 − 0.01² = 99.99%`, but only if the failures are genuinely independent — shared control planes, shared credentials, and shared regions destroy the assumption, which is why correlated failure is what actually takes systems down.
- Publish the dependency chain with each SLO. "We promise 99.95% while our payment provider promises 99.9%" is a conversation to have before the incident, not after.

**Write in the same turn**: every objective (SLI definition with its agreed exclusions, target, window, measurement point, current budget, pages per shift, actioned fraction) goes in `## SLOs` of `~/Clawic/data/devops/memory.md` — the single home of an SLI, never restated in `## Services`; the error-budget policy and any SLO agreement with a stakeholder becomes `artifacts/<kebab-name>.md` with its `## Boxes` line; the SLO review and alert-hygiene review go in `## Due` with their last run; budget-exhausting incidents get their row in `incidents/<year>.md` (`memory-template.md`).
