# Troubleshooting Patterns

Common troubleshooting workflows using Datadog MCP tools.

## Pattern 1: Error Spike Investigation

**Symptom:** Sudden increase in errors for a service.

1. `get_logs` — Search `status:error service:{name}` in the last 30 min
2. Group by `@http.status_code` or `@error.kind` to find the dominant error
3. `list_spans` — Find errored spans to identify the failing endpoint
4. `get_trace` — Get a sample trace to see the full request path
5. `get_metrics` — Check `trace.{service}.errors` rate to confirm the spike

## Pattern 2: Latency Degradation

**Symptom:** P99 latency increasing for a service.

1. `get_metrics` — Query `trace.{service}.duration.by.resource_name` (p99)
2. Identify which resource/endpoint is slow
3. `list_spans` — Find spans with `@duration:>5s` for that resource
4. `get_trace` — Examine a slow trace to find the bottleneck span
5. `list_hosts` — Check if host CPU/memory is saturated

## Pattern 3: Infrastructure Issue

**Symptom:** Host or container alerts firing.

1. `list_hosts` — Get host list, check for `agent_unreachable` or high load
2. `get_monitors` — Find triggered infra monitors
3. `get_logs` — Search `source:system` or `source:docker` for host-level errors
4. `get_metrics` — Check `system.cpu.user`, `system.mem.used`, `system.disk.in_use`

## Pattern 4: Deployment Verification

**Symptom:** New deploy, need to verify health.

1. `get_logs` — Search for errors after deploy timestamp
2. `get_metrics` — Compare error rate before/after deploy
3. `get_monitors` — Confirm no new monitors triggered
4. `list_spans` — Check for new error types in traces

## Pattern 5: Cross-Service Dependency Issue

**Symptom:** Service A errors, root cause may be in Service B.

1. `get_logs` — Search errors in Service A
2. `list_spans` — Find spans showing calls to Service B with errors
3. `get_trace` — Follow a trace across services
4. `get_logs` — Search errors in Service B at the same timestamps
5. `get_metrics` — Compare error rates for both services

## Log Query Syntax Quick Reference

| Query | Description |
|---|---|
| `service:web-app status:error` | Errors from web-app |
| `@http.status_code:500` | HTTP 500 errors |
| `@duration:>5000000000` | Spans over 5 seconds (nanoseconds) |
| `host:i-abc123` | Logs from specific host |
| `source:nginx @http.url:"/api/*"` | Nginx logs for API paths |
| `status:(error OR critical)` | Error or critical logs |
| `@error.kind:TimeoutError` | Specific error types |
