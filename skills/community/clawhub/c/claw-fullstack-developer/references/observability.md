# Observability

How to know what the app is doing in production — before, during, and after an incident.

## The three pillars (and why they matter)

1. **Logs** — discrete events with context. Answer: "what happened in this specific request?"
2. **Metrics** — aggregated numeric data over time. Answer: "is the system healthy right now?"
3. **Traces** — the path of a request across services. Answer: "where was the 3 seconds spent?"

You don't need all three on day one. Get logs and basic metrics first; add traces when the system spans multiple services or background jobs.

## Logging

### Structured JSON, always
Plain-text logs that look like `2026-04-01 user "Foo Bar" did a thing with id 123` are nearly impossible to query in aggregate. Emit JSON:

```json
{
  "timestamp": "2026-04-01T12:34:56.789Z",
  "level": "info",
  "message": "payment.completed",
  "request_id": "req_abc123",
  "user_id": "usr_xyz",
  "amount_cents": 2500,
  "currency": "USD",
  "duration_ms": 142
}
```

### Fields every log line should have
- `timestamp` (ISO 8601, UTC)
- `level` (debug, info, warn, error)
- `message` (short, semantic, like an event name — not "the thing happened for user 123")
- `request_id` / `trace_id` — correlate across services
- `user_id` / `tenant_id` when available
- service-specific context (order_id, job_id, etc.)

### What to log
- Every inbound HTTP request at info level: method, path, status, duration, user, request ID.
- Every outbound call to external services: endpoint, status, duration, outcome.
- Every auth event: login (success/fail), logout, password change, MFA.
- Every background job: start, end, duration, outcome, attempts.
- Every error with full stack.

### What NOT to log
- Passwords, tokens, session IDs, card numbers, SSNs, health records. Even hashed.
- Full request bodies on endpoints that accept sensitive data.
- Full response bodies (usually unnecessary, often sensitive).

Use a redaction filter in the logger (e.g., [`pino`](https://github.com/pinojs/pino)'s `redact` option) to strip known-sensitive fields automatically.

### Log levels — when to use which
- **debug** — development noise, detailed diagnostic. Off in production.
- **info** — normal operations. Log what happened; future-you will want this.
- **warn** — something unusual but not broken (fallback triggered, rate limit hit).
- **error** — something broke. Page someone if it's unexpected.

Keep production at `info`. Turn on `debug` for a single request via a header, not globally.

### Request IDs
Every incoming request gets a unique ID. It's logged on every line for that request, and propagated to downstream calls (via `X-Request-Id` header or W3C Trace Context). When a user reports a problem, you can find every log line related to their request.

### Where to send logs
- **Managed platforms** (Vercel, Fly, Railway) have built-in log viewers for a short retention.
- **Aggregation**: ship to a log platform — Datadog, New Relic, Grafana Loki, Better Stack, Axiom, Papertrail. Structured JSON makes querying trivial.
- **Self-hosted**: ELK stack (Elasticsearch, Logstash, Kibana) or Grafana Loki. Operationally heavy; don't start here.

## Error tracking

Logs are for "everything that happened." Error tracking is for the subset: exceptions and errors that need human attention.

### Tooling
- **Sentry** — standard for JS/Python/Go/etc. Great frontend + backend coverage.
- **Rollbar**, **Bugsnag** — similar category.
- **Honeybadger** — Ruby-first but fine elsewhere.
- Most error trackers have free tiers sufficient for small apps.

### Setup essentials
- Wire into both frontend and backend.
- Attach user context (ID, email redacted) on every event.
- Attach release/version so you can correlate error spikes with deploys.
- Upload sourcemaps from the frontend build so errors have readable stacks — but don't serve sourcemaps to users.
- Configure data scrubbing: redact passwords, tokens, card numbers from captured payloads.
- Set up alerts: new error types, error volume spikes, errors affecting >N users.

### Frontend errors
- Global `window.onerror` / `unhandledrejection` handler reports to Sentry.
- React/Vue error boundary that reports and shows a fallback UI.
- Core Web Vitals (LCP, CLS, INP) — Sentry can capture these; so can Vercel Analytics.

## Metrics

### What to measure — the RED method
For every request-handling service, track:
- **R**ate — requests per second
- **E**rrors — % of requests failing
- **D**uration — p50, p95, p99 latency

This is the absolute minimum. You can make most performance and reliability decisions from these.

### The USE method (for resources)
For every resource (CPU, memory, disk, DB connections):
- **U**tilization — % busy
- **S**aturation — queue depth / wait time
- **E**rrors — failures

### Product metrics
Beyond system health, measure the business:
- Signups per day
- Active users (DAU/WAU/MAU)
- Conversion rates on key flows
- Revenue

These tell you if the app is doing its job, not just if it's up.

### Tooling
- **Managed platform metrics** — start with what's built in (Vercel Analytics, Fly metrics, AWS CloudWatch).
- **Prometheus + Grafana** — the open source standard. Hosted: Grafana Cloud, AWS Managed Prometheus.
- **Datadog / New Relic** — paid, but bundle logs + metrics + traces + alerts.
- **Cloudflare Analytics** — free, good for edge-level request metrics.

### Dashboards
Have at least one dashboard you look at weekly:
- Request rate, error rate, p95 latency per service
- Database: connections, query duration, slow queries
- Background job queue depth and failure rate
- Top 10 endpoints by p95 latency

A dashboard nobody looks at is dead. Fewer, more meaningful panels beats a wall of 50.

## Tracing

Distributed tracing shows the path of a request across services — useful when you have multiple services or heavy background processing.

- **OpenTelemetry** is the standard. Instrument once, send to any backend (Jaeger, Honeycomb, Datadog, Grafana Tempo, Sentry's tracing).
- Start with auto-instrumentation (HTTP libraries, DB drivers) — gets you 80% for free.
- Add custom spans around critical business operations.
- Sampling: 1–10% of requests in prod for a busy service; 100% of errors.

For a single-service Next.js app, tracing is nice-to-have. For a 5-service system, it's essential.

## Alerting

### Alert on symptoms, not causes
- Good alert: "error rate >1% for 5 minutes." (Symptom.)
- Bad alert: "CPU >80%." (Cause — and possibly benign.)

High CPU is interesting for debugging but doesn't always mean something's wrong. User-facing error rate does.

### Alert fatigue is real
- Every alert should be actionable. If the response is "ignore it," remove the alert.
- Tune thresholds after a week of calibration. A hair-trigger alert gets muted.
- Alert severity: pageable (wake someone) vs. FYI (Slack/email).

### Sensible starting alerts
- 5xx rate >1% over 5 minutes → page
- p95 latency >2x baseline over 10 minutes → page
- Deploy failed → Slack
- Background job queue depth exceeds threshold → Slack
- Error tracker: new error type → Slack; >N users affected in an hour → page
- Uptime monitor (healthcheck failing from external) → page
- Certificate expiring in <7 days → Slack
- Disk >80% → Slack; >95% → page

### On-call
For anything past hobby status, define who's on-call. PagerDuty, Opsgenie, incident.io. Rotation is weekly, not per-person forever.

## Uptime monitoring

External checks (from outside your infrastructure) hitting a `/health` endpoint every 30–60s. If internal monitoring goes down with the app, you'd miss outages. External doesn't.

Tools: UptimeRobot, Better Stack, Pingdom, Checkly. Free tiers are fine for small apps.

### The `/health` endpoint
- Returns 200 when the app can serve traffic.
- Checks what matters: DB connectivity, external services, cache.
- Simple implementation: query a trivial `SELECT 1`, check Redis ping, return success.
- Don't do expensive work in `/health` — it's called constantly.

Separate `/readiness` and `/liveness` if using Kubernetes:
- `/liveness` — "the process is alive." Fails → restart the container.
- `/readiness` — "the process can serve traffic." Fails → remove from load balancer.

## Cost observability

Your observability stack itself will have a bill. Watch it:
- Logs: storage is usually the driver. Aggressive retention (30 days hot, archive longer if needed) controls cost.
- Metrics: cardinality is the killer — high-cardinality tags (user_id, request_id) multiply series counts.
- APM/tracing: per-request. Sampling matters.

Review the monitoring bill quarterly. It's easy for it to become 10% of infra spend.

## Feedback loops — closing the loop

Observability is about closing the loop from "incident" back to "code change." Each incident should ask:
1. What was the signal? Was it fast enough?
2. What was the root cause?
3. How do we prevent recurrence or detect faster?
4. Did the runbook help? If not, update it.

Write a short post-incident note, even for small incidents. They compound into institutional knowledge.

## Minimum viable observability

For an app just launched, you need:
- Structured JSON logs, aggregated somewhere searchable.
- Sentry (or equivalent) on frontend and backend with sourcemaps + scrubbing.
- One external uptime check on `/health`.
- A dashboard: request rate, error rate, p95, DB connections.
- Alerts: 5xx spike, uptime failure, new Sentry error type.

That's a weekend of setup for an app of any size. Everything past that is refinement.
