# Analysis Patterns & Known Issue Cross-Reference

## Known Patterns to Check

Cross-reference telemetry results against `memory/amg-check-storage-account/report.md` before presenting findings.

### Storage Throttling (503 Server Busy)

Azure Storage returns 503 when the request rate exceeds the account or partition scalability targets.

**Signals in telemetry:**
- Error transactions with StatusCode 503 in multiple time windows
- SuccessE2ELatency increases as requests queue
- Availability drops below 99.9%
- Transaction volume remains high (clients retrying)

**Investigation technique:**
1. Check if throttling is on a specific operation type (GetBlob, PutBlob, ListBlobs)
2. Check if throttling is on a specific container or blob path (hot partition)
3. Compare total transactions vs error transactions to compute error rate
4. Check if ingress/egress volumes are unusually high

**Resolution paths:**
- Distribute workload across more storage accounts or containers
- Implement exponential backoff in client code
- Use CDN for read-heavy workloads
- Request higher scalability targets from Azure support

### Network Latency vs Server Latency Divergence

When E2E latency is high but server latency is normal, the issue is in the network path between client and storage.

**Signals:**
- SuccessE2ELatency avg > 50ms but SuccessServerLatency avg < 10ms
- The gap between E2E and server latency is consistent across time windows
- No error transactions or availability issues

**Impact:** Application performance degrades but storage backend is healthy. Issue is in DNS resolution, TCP connection, or network routing.

**Investigation:** Check if the issue is region-specific. Compare E2E vs server latency across regions. Check if clients are connecting to the nearest storage endpoint.

### Authentication Failures (403)

Repeated 403 errors indicate expired keys, misconfigured SAS tokens, or unauthorized access attempts.

**Signals:**
- Error transactions with StatusCode 403
- Often from specific CallerIpAddress or UserAgentHeader values
- May spike after key rotation or deployment

**Impact:** Depends on volume — low-volume 403s may be scanners. High-volume indicates broken client configuration.

**Investigation:** Check resource logs for CallerIpAddress and UserAgentHeader patterns. Determine if errors are from known infrastructure or external sources.

### Dormant Account Detection

Accounts with zero traffic over the scan period may be orphaned resources.

**Signals:**
- All 3 Tier 1 metrics return empty timeSeries
- No transactions, no latency data, no availability data
- Account exists in Resource Graph but has no activity

**Impact:** Low immediate impact but orphaned resources incur costs and increase attack surface.

**Investigation:** Check UsedCapacity — if non-zero, data exists but isn't being accessed. Cross-reference with deployment records to determine if the account is still needed.

### Regional Latency Baseline Shift

A sustained latency shift across multiple accounts in the same region may indicate a regional storage platform issue.

**Signals:**
- Multiple accounts in a specific region all showing elevated latency
- Other accounts in different regions remain normal
- No error transactions (just slower)

**Impact:** Application performance degrades for all workloads in the affected region.

**Investigation:** Compare latency across accounts in the affected region vs other regions. Check Azure status for regional storage incidents.

### Capacity Growth Anomaly

Unexpected capacity growth may indicate log accumulation, data leak, or runaway writes.

**Signals:**
- UsedCapacity trend shows steady growth over 7 days
- Growth rate is unusual compared to similar accounts
- No corresponding increase in expected workload

**Impact:** May lead to storage quota exhaustion and eventual write failures.

**Investigation:** Compare capacity across similar accounts. Use container-level log queries to identify which containers are growing.

## Analysis Techniques

### Cross-Account Comparison

When an account is flagged, compare it against similar accounts:

1. **Similar accounts, same region** — if multiple accounts show the same issue, it's likely a regional or systemic problem
2. **Similar accounts, different regions** — if only one region is affected, it's region-specific
3. **Different account types, same region** — if all accounts in a region are affected, it's a storage platform issue

### Error Rate Calculation

Always compute error rate rather than just error count:
- Error rate = (error transactions / total transactions) x 100
- Low error count with high total transactions = acceptable
- Low error count with low total transactions = potentially significant

### Latency Attribution

When latency is high, determine the source:
1. Compare SuccessE2ELatency vs SuccessServerLatency
2. If gap is large: network issue (DNS, routing, TCP)
3. If both are high: storage backend issue (throttling, overloaded)
4. If server is high but E2E is similar: backend issue only
5. Check max vs avg — high max with low avg indicates tail latency (usually normal)
