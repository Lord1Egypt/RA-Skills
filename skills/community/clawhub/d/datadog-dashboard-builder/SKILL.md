---
name: datadog-dashboard-builder
description: Design Datadog dashboards and monitors — recommend metrics, widget layouts, alerting thresholds, and SLO definitions. Analyze existing dashboards for blind spots and noise. Use when asked to build monitoring, set up alerts, or improve observability in Datadog.
metadata:
  tags: ["datadog", "monitoring", "dashboards", "alerting", "slo", "observability"]
---

# Datadog Dashboard Builder

Design production-grade Datadog dashboards, monitors, and SLOs from scratch or audit existing ones. Recommends the right metrics, widget types, alert thresholds, and layout patterns so on-call engineers can diagnose incidents in under 60 seconds.

Use when: "build a Datadog dashboard", "set up monitoring for this service", "review our alerting", "we need SLOs", "our dashboard is too noisy", "what should we monitor", or when designing observability for a new service.

## Core Principles

1. **Dashboards answer questions, not display data.** Every widget must answer a specific question an on-call engineer would ask.
2. **The top row is the health signal.** Green/red at a glance, no scrolling required.
3. **Alerts fire when humans need to act.** If nobody needs to wake up, it's not an alert.
4. **SLOs align engineering with business.** They translate uptime promises into error budgets.

## Analysis Steps

### 1. Identify the Service Profile

Before building anything, classify the service:

```
Service Name: ____
Type: [API | Worker | Queue Consumer | Batch Job | Frontend | Database | Cache]
Traffic Pattern: [Steady | Diurnal | Spiky | Event-Driven | Cron-Based]
Criticality: [Tier 1 (revenue) | Tier 2 (core feature) | Tier 3 (internal) | Tier 4 (best-effort)]
Dependencies: [list upstream and downstream services]
Current Pain Points: [what incidents happened, what was hard to debug]
```

### 2. Select the Golden Signals

Every service dashboard starts with the four golden signals (Google SRE book):

| Signal | What to Measure | Datadog Metric Pattern |
|--------|----------------|----------------------|
| **Latency** | Request duration (p50, p95, p99) | `trace.{service}.request.duration` or `{service}.request.latency` |
| **Traffic** | Requests per second | `trace.{service}.request.hits` or `{service}.request.count` |
| **Errors** | Error rate as percentage | `trace.{service}.request.errors / trace.{service}.request.hits * 100` |
| **Saturation** | Resource utilization (CPU, memory, connections, queue depth) | `system.cpu.user`, `system.mem.used`, `{service}.pool.active` |

For each service type, add specific metrics:

**API Services:**
```
- Endpoint-level latency breakdown (which endpoint is slow?)
- HTTP status code distribution (2xx, 4xx, 5xx)
- Request payload size (are large payloads causing timeouts?)
- Rate limiting triggers
- Authentication failures
```

**Queue/Worker:** Queue depth, processing rate, consumer lag, dead letter queue size, job duration by type, retry count.

**Database:** Query duration by operation, connection pool utilization, lock wait time, replication lag, cache hit ratio, slow query count.

**Frontend/SPA:** Core Web Vitals (LCP, FID, CLS) via RUM, JS error rate by page, client-side API latency, page load time, session crash rate.

### 3. Design the Dashboard Layout

Follow this proven layout pattern (top to bottom):

```
Row 1: Health Overview — 4x Query Value widgets (SLO burndown, Error Rate %, p99 Latency, RPS)
Row 2: Request Flow   — Request Rate timeseries (stacked by endpoint) + Error Rate timeseries
Row 3: Latency        — p50/p95/p99 overlay + Latency heatmap or top-list by endpoint
Row 4: Infrastructure — CPU %, Memory %, Disk I/O, Network (4 widgets)
Row 5: Dependencies   — Downstream latency + Downstream error rate (DB, cache, APIs)
Row 6: Changes        — Event overlay: deploys, config changes, incidents
```

### 4. Configure Widget Details

**Query Value Widgets (Row 1):**
```json
{
  "type": "query_value",
  "requests": [{
    "q": "sum:trace.express.request.errors{service:my-api}.as_count() / sum:trace.express.request.hits{service:my-api}.as_count() * 100",
    "aggregator": "avg"
  }],
  "precision": 2,
  "custom_unit": "%",
  "conditional_formats": [
    {"comparator": "<", "value": 1, "palette": "white_on_green"},
    {"comparator": ">=", "value": 1, "palette": "white_on_yellow"},
    {"comparator": ">=", "value": 5, "palette": "white_on_red"}
  ]
}
```

**Timeseries Widgets:**
- Use `avg` aggregation for latency, `sum` for counts
- Always include a dotted line for the alerting threshold
- Use `week_before()` function to overlay last week for trend comparison
- Set y-axis minimum to 0 (prevents misleading scales)

**Heatmaps:**
- Best for latency distribution — shows bimodal distributions that p99 hides
- Use for request duration, query time, queue wait time

**Top Lists:**
- Use for "which endpoint is slowest" or "which error is most frequent"
- Limit to 10 entries — more is noise

### 5. Design Monitors (Alerts)

#### Monitor Template for Each Signal

**Error Rate Monitor:**
```yaml
name: "[{service}] Error rate above {threshold}%"
type: metric alert
query: |
  sum(last_5m):
    sum:trace.{service}.request.errors{env:production}.as_count() /
    sum:trace.{service}.request.hits{env:production}.as_count() * 100
    > {threshold}
thresholds:
  critical: 5        # Page the on-call
  warning: 2         # Slack notification
  recovery: 1        # Auto-resolve
evaluation_delay: 60  # Wait for late-arriving data
require_full_window: false
notify_no_data: true
no_data_timeframe: 10
renotify_interval: 30
escalation_message: "Error rate still elevated after 30 minutes"
tags:
  - "service:{service}"
  - "team:{team}"
  - "tier:1"
```

**Additional monitors to create** (follow same pattern as error rate above):
- **Latency:** `avg(last_5m):trace.{service}.request.duration.by.service.99p{env:production} > 2000` — critical at 2s, warning at 1s
- **Saturation:** `avg(last_10m):avg:system.cpu.user{service:{service}} by {host} > 80` — critical at 90%, warning at 80%
- **Anomaly:** Use `anomalies()` function with `agile` algorithm, sensitivity 3, weekly seasonality for traffic volume

#### Alert Threshold Guidelines

| Service Tier | Error Rate Critical | Latency p99 Critical | CPU Critical |
|-------------|--------------------|--------------------|-------------|
| Tier 1 (revenue) | 1% | 500ms | 80% |
| Tier 2 (core) | 5% | 2s | 85% |
| Tier 3 (internal) | 10% | 5s | 90% |
| Tier 4 (best-effort) | No page | No page | 95% |

### 6. Define SLOs

Create metric-based SLOs with `numerator` (successful requests excluding 5xx) divided by `denominator` (all requests). Set 30-day rolling window.

**Recommended SLO Targets by Tier:**

| Tier | Availability SLO | Latency SLO (p99 < target) | Error Budget (30 days) |
|------|-----------------|---------------------------|----------------------|
| Tier 1 | 99.95% | 99.9% under 500ms | 21.6 min downtime |
| Tier 2 | 99.9% | 99.5% under 2s | 43.2 min downtime |
| Tier 3 | 99.5% | 99% under 5s | 3.6 hr downtime |
| Tier 4 | 99% | N/A | 7.2 hr downtime |

### 7. Dashboard Audit Checklist

When reviewing an existing dashboard, check for:

- [ ] **No health summary at top** — engineers must scroll to assess service health
- [ ] **Missing golden signal** — one of latency/traffic/errors/saturation is absent
- [ ] **No deploy markers** — impossible to correlate changes with metric shifts
- [ ] **Wrong aggregation** — using `avg` for latency instead of percentiles (hides tail)
- [ ] **No dependency visibility** — can't tell if the issue is this service or a downstream one
- [ ] **Too many widgets** — more than 20 widgets causes cognitive overload (split into sub-dashboards)
- [ ] **Vanity metrics** — total request count (cumulative) instead of rate (per second)
- [ ] **No conditional formatting** — all numbers are the same color regardless of health
- [ ] **Hardcoded time window** — should use template variables for environment and time
- [ ] **No template variables** — missing `$env`, `$service`, `$host` dropdowns
- [ ] **Stale widgets** — metrics that no longer emit data (renamed or removed)
- [ ] **Missing units** — numbers without ms, %, req/s labels

## Output Format

```markdown
# Dashboard Design: {Service Name}

## Service Profile
- **Type:** {API/Worker/etc.}
- **Tier:** {1-4}
- **Dependencies:** {list}

## Dashboard Structure
{Layout description with widget specifications}

## Monitors
{List of monitors with thresholds and notification routing}

## SLOs
{SLO definitions with targets and error budgets}

## Audit Findings (if reviewing existing)
- {Finding 1: problem and recommendation}
- {Finding 2: problem and recommendation}

## Implementation Steps
1. {Step-by-step instructions to create in Datadog UI or via API/Terraform}
```

## Tips

- Use Terraform or Datadog's API to version-control dashboards — never build production dashboards only in the UI
- Set default time window to 4 hours — long enough to see trends, short enough to see spikes
- Add a "Notes" widget at the top with runbook links, on-call rotation, and escalation path
- Use template variables for `env` and `service` so one dashboard works across environments
- Group related widgets in collapsible sections to reduce visual noise
- Set monitor notification channels by severity: P1 to PagerDuty, P2 to Slack, P3 to email
- Review alert thresholds quarterly — traffic growth makes static thresholds obsolete
- Add `week_before()` overlays to catch gradual degradation that doesn't trigger alerts
