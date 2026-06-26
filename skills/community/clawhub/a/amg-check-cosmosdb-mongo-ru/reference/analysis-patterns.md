# Analysis Patterns & Known Issue Cross-Reference

## Known Patterns to Check

Cross-reference telemetry results against `memory/amg-check-cosmosdb-mongo-ru/report.md` before presenting findings.

### RU Throttling (429 Errors)

The most common Cosmos DB issue. Occurs when request rate exceeds provisioned or autoscale throughput.

**Signals in telemetry:**
- NormalizedRUConsumption sustained at or near 100%
- MongoRequests count stays high but TotalRequestUnits flattens (requests being rejected)
- Resource logs show ErrorCode 429 or 16500
- ServerSideLatency may increase as the system queues requests

**Investigation technique:**
1. Check if the account uses manual or autoscale throughput (AutoscaleMaxThroughput empty = manual)
2. Check which databases/collections are consuming the most RUs via resource logs
3. Determine if throttling is sustained or burst (periodic job vs steady workload)
4. Compare ProvisionedThroughput against TotalRequestUnits to see utilization ratio

**Resolution paths:**
- Manual throughput: Increase provisioned RU/s or switch to autoscale
- Autoscale: Increase max autoscale RU/s
- Query optimization: Reduce per-operation RU cost via indexing

### Hot Partition

Uneven distribution of requests across logical partitions causes one physical partition to hit its RU limit while others are underutilized.

**Signals:**
- NormalizedRUConsumption at 100% but TotalRequestUnits well below ProvisionedThroughput
- Throttling concentrated on specific collections
- Individual partition consumption reports (if available in logs) show skew

**Impact:** The account reports throttling even though overall provisioned throughput should be sufficient. Increasing throughput may not resolve the issue.

**Investigation:** Check resource logs for which collections are throttled. Look for operations targeting a single partition key value.

### Autoscale Thrashing

Rapid scale-up/scale-down cycles when workload oscillates around autoscale thresholds.

**Signals:**
- NormalizedRUConsumption oscillating between low (<30%) and high (>70%) within short intervals
- AutoscaleMaxThroughput is non-empty (autoscale enabled)
- ProvisionedThroughput shows step changes

**Impact:** Medium — autoscale handles this automatically, but rapid changes may cause brief latency spikes during scale transitions.

### Replication Lag

Multi-region write scenarios where secondary regions fall behind the primary.

**Signals:**
- ReplicationLatency > 100ms (warning) or > 1000ms (critical)
- ServiceAvailability may dip in secondary regions
- Often correlates with high write volume (MongoRequests + high RU)

**Impact:** Read-your-own-writes consistency violations. Applications reading from secondary regions may see stale data.

**Investigation:** Check if the lag is transient (network blip) or sustained (write volume exceeds replication capacity). Check which regions are affected.

### Workload Burst Pattern

Periodic jobs or batch operations causing regular RU spikes.

**Signals:**
- NormalizedRUConsumption shows regular spike pattern (e.g., daily at same time)
- MongoRequests and MongoRequestCharge spike together
- Pattern repeats across multiple days in 7-day scan

**Impact:** Usually manageable with autoscale. With manual throughput, bursts may cause throttling during the spike window.

**Investigation:** Correlate spike timing with known batch jobs or ETL schedules. Check resource logs for the specific operations running during spikes.

### Latency Degradation Without RU Pressure

High latency with normal RU consumption indicates backend or network issues rather than throughput problems.

**Signals:**
- ServerSideLatency avg > 10ms but NormalizedRUConsumption < 50%
- No throttling (no 429 errors in logs)
- May be region-specific

**Impact:** Application performance degrades despite adequate throughput provisioning.

**Investigation:** Check if latency is region-specific. Compare against other accounts in the same region. Check Azure status for regional issues.

## Analysis Techniques

### Identifying Throttling Root Cause

When throttling (429) is detected:

1. **Check autoscale status** — is the account on manual or autoscale throughput?
2. **Compare total RU consumed vs provisioned** — are we using most of the budget?
3. **Check per-collection breakdown in logs** — is one collection dominating?
4. **Check operation types** — are expensive operations (aggregations, cross-partition queries) driving costs?
5. **Check for hot partitions** — is NormalizedRU at 100% while TotalRU is well below provisioned?

### RU Efficiency Analysis

Compare request count to RU consumption to find expensive operations:

1. **High RU per request** (MongoRequestCharge / MongoRequests > 10 RU) suggests missing indexes or large document scans
2. **Normal RU per request** with high request count suggests the workload needs more throughput
3. **Sporadic high RU** suggests occasional expensive queries (aggregation pipelines, large sorts)

### Capacity Planning

Use 7-day trends to project future needs:

1. Check if NormalizedRUConsumption is trending upward over the 7-day window
2. Compare DataUsage growth rate — is storage growing faster than expected?
3. If autoscale is hitting its max frequently, recommend increasing the autoscale ceiling
4. If manual throughput has consistent headroom, it may be over-provisioned (cost optimization)
