# Incident Response via Datadog MCP

Step-by-step workflow for triaging production incidents using MCP tools.

## Phase 1: Detection & Assessment

1. **Check active incidents**
```text
   "List all active incidents" → list_incidents
   ```
   Review severity, status, commander, and timeline.

2. **Get incident details**
```text
   "Get details for incident INC-{id}" → get_incident
   ```
   Review: timeline, impacted services, postmortem notes.

## Phase 2: Log Investigation

3. **Search error logs around incident start time**
```text
   "Show error logs from service:{name} between {start} and {end}"
   → get_logs with time range and status:error filter
   ```

4. **Broaden search if needed**
```text
   "Show warn and error logs from service:{name} in the last 2 hours"
   ```

## Phase 3: Trace Correlation

5. **Find slow or errored spans**
```text
   "List spans for service:{name} with errors in the last hour"
   → list_spans
   ```

6. **Get full trace for a problematic request**
```text
   "Get trace {trace_id}" → get_trace
   ```
   Review: span waterfall, error tags, latency breakdown.

## Phase 4: Metrics Validation

7. **Check key metrics**
```text
   "Show me error rate for service:{name} over the last 4 hours"
   → list_metrics + get_metrics
   ```

8. **Compare with baseline**
```text
   "Show {metric} for the last 24 hours to see when it started spiking"
   ```

## Phase 5: Infrastructure Check

9. **Verify host health**
```text
   "List hosts tagged with service:{name}" → list_hosts
   ```
   Check: CPU, memory, disk, agent version, uptime.

## Phase 6: Monitor Review

10. **Check triggered monitors**
```text
    "Show triggered monitors for service:{name}" → get_monitors
    ```
    Review: thresholds, evaluation history, notification targets.

## Phase 7: Resolution

11. After identifying root cause, document in incident timeline
12. Verify metrics return to baseline
13. Confirm monitors recover to OK state
