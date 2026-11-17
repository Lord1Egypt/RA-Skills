# Observability — Logs With Context, Probes That Tell The Truth

The goal is answering "what happened to this one request" in under a minute. That needs three things wired at startup: a request id on every line, honest health endpoints, and metrics that survive multiple workers.

## Logging Setup

- Uvicorn configures its own loggers (`uvicorn`, `uvicorn.access`, `uvicorn.error`). Configure logging in your own `dictConfig` at startup with `disable_existing_loggers: False`, or half your libraries go silent and only uvicorn's lines appear.
- Log to stdout as JSON in production (structlog or a JSON formatter). The platform collects stdout; writing files inside a container creates a disk to rotate and a volume to mount for nothing.
- The default access log has no request id, no user, and no duration bucket. Either disable it (`--no-access-log`) and emit your own structured access line from middleware, or accept two log lines per request with different shapes.
- Never log the `Authorization` header, cookies, tokens, or request bodies from auth routes. A redaction filter belongs in the logging config, not in the discipline of every caller (`auth.md`).

## Request Correlation

```python
request_id_var: ContextVar[str] = ContextVar("request_id", default="-")

class RequestContext(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_var.get()
        return True
```

- A pure ASGI middleware sets the contextvar and echoes the id back as a response header (`middleware.md`); `BaseHTTPMiddleware` cannot reliably read a contextvar set downstream.
- Accept an inbound `X-Request-ID` from your proxy when present, generate one when absent; a client-supplied id ties their bug report to your logs.
- Propagate the id on outbound calls (`headers={"X-Request-ID": request_id_var.get()}`) so a request can be followed across services without full tracing.
- Log the id on the error response too: the client sees an opaque message plus an id you can grep (`errors.md`).

## Health, Readiness, Startup

| Probe | Answers | Checks |
|---|---|---|
| Liveness `/health` | "Is this process alive?" | Nothing external — returns 200 unconditionally. A liveness probe that pings the database restarts every pod when the database blips |
| Readiness `/ready` | "Should traffic come here?" | Dependencies this instance cannot serve without: database, required cache; short timeouts, cached for a second or two |
| Startup | "Has boot finished?" | Same as readiness, with a longer grace period for slow imports and model loading |

- Both live on an unauthenticated router; a router-level auth dependency on them makes the orchestrator restart a healthy service in a loop (SKILL.md Traps).
- Readiness must flip to failing *before* shutdown begins, and liveness must keep passing during the drain (`deployment.md`).
- Keep probes off the shared database pool if you can, or a pool exhaustion event also fails every readiness check and the platform kills the instances that were about to recover.

## Metrics

- The four that answer most questions: request rate, error rate, duration percentiles (p50/p95/p99) — all three labelled by *route template*, never by raw path — and in-flight requests.
- Labelling by raw path (`/orders/7f3c...`) makes one time series per id and kills the metrics backend. Use `request.scope["route"].path` for the template.
- Multiple workers behind one port each have their own registry; a Prometheus scrape hits a random worker. Either run one worker per container (the simple answer) or use the client's multiprocess mode with a shared directory.
- Beyond HTTP: connection pool checkouts and waits (`database.md`), threadpool saturation (SKILL.md rule 2), queue depth and task age (`background.md`), WebSocket connection count (`websockets.md`).
- Event-loop lag is the single best early warning for blocked loops: sample `loop.time()` drift from a background task and alert when it exceeds a few tens of milliseconds (`async.md`).

## Tracing

- OpenTelemetry's ASGI/FastAPI instrumentation gives spans per request; adding the httpx, SQLAlchemy, and Redis instrumentations turns those spans into the actual latency breakdown, which is what makes tracing worth its cost.
- Sample: 100% of errors and slow requests, a small percentage of the rest. Full sampling on a busy API costs more than the service.
- Put the trace id in the log line and the response header, so logs, traces, and the client's report share one key.
- Manual spans around business steps (`with tracer.start_as_current_span("charge_card")`) are worth more than instrumenting more libraries.

## Alerting On The Right Signals

- Alert on symptoms users feel: error rate, p99 latency, readiness failures, queue age. CPU and memory are diagnostics, not alerts.
- Ratios, not counts: "5xx over 1% of requests for 5 minutes" survives traffic growth; "50 errors per minute" does not.
- Every alert needs a first move written next to it. The Error Signatures table in SKILL.md is that first move for most of this domain.

## After The Incident

Keep enough to reconstruct: structured access logs with route, status, duration, request id, and user id; a retained trace sample of the failing window; and the deploy timeline. The most common answer to "what changed" is a deploy, and the second is a dependency's rollout — neither is visible in application logs unless you log the version at startup.
