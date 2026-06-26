# Analysis Patterns & Known Issue Cross-Reference

## Known Patterns to Check

Cross-reference telemetry results against `memory/amg-check-key-vault/report.md` before presenting findings.

### Throttling (429 Too Many Requests)

Azure Key Vault enforces transaction rate limits per vault. Standard vaults allow up to 4,000 transactions per 10 seconds. Exceeding this results in 429 responses.

**Signals in telemetry:**
- ServiceApiResult with StatusCode 429 in multiple time windows
- ServiceApiLatency increases as requests queue and retry
- ServiceApiHit volume is high (clients retrying increase total hits)
- Availability may dip if throttling is severe

**Investigation technique:**
1. Check if throttling targets specific operation types (SecretGet, KeySign, etc.)
2. Compare total API hits vs error results to compute throttle rate
3. Check if throttling is bursty (single window) or sustained (multiple windows)
4. Identify calling applications from resource logs (identity_claim_appid_g)

**Resolution paths:**
- Distribute secrets across multiple vaults
- Implement exponential backoff in client code
- Cache secret values client-side (with appropriate TTL)
- Request higher throughput limits from Azure support (premium SKU)

### Authentication Failures (401/403)

Repeated 401 (Unauthorized) or 403 (Forbidden) errors indicate expired credentials, misconfigured access policies, or unauthorized access attempts.

**Signals:**
- ServiceApiResult with StatusCode 401 or 403
- Often from specific CallerIPAddress or application IDs
- May spike after key rotation, deployment, or access policy changes

**Impact:** Depends on volume — low-volume 401/403 may be scanners or misconfigured non-critical clients. High-volume indicates broken client authentication that affects application functionality.

**Investigation:** Check resource logs for CallerIPAddress and identity_claim_appid_g patterns. Determine if errors are from known infrastructure or external sources. Correlate with deployment or access policy change timelines.

### Secret/Key Not Found (404)

Repeated 404 errors indicate references to deleted or non-existent secrets, keys, or certificates.

**Signals:**
- ServiceApiResult with StatusCode 404
- Often from SecretGet, KeyGet, or CertificateGet operations
- May spike after secret rotation where old secret names were not updated in consuming applications

**Impact:** Applications that depend on the missing secrets will fail. May cascade to service outages.

**Investigation:** Identify which secret/key names are being requested. Check if they were recently deleted or renamed. Cross-reference with deployment logs.

### Availability Degradation

Sustained availability below 99.9% indicates a vault-level or regional issue.

**Signals:**
- Availability metric drops below 99.9% for multiple consecutive windows
- Often correlated with high error counts or throttling
- May affect multiple vaults in the same region (platform issue)

**Investigation:**
1. Check if availability drop correlates with specific error types (429, 503)
2. Check if other vaults in the same region show the same pattern
3. Check Azure status for regional Key Vault incidents

### Saturation Warning

SaturationShoebox tracks the overall vault transaction saturation as a percentage. Values approaching 100% indicate the vault is near its transaction limits.

**Signals:**
- SaturationShoebox avg > 50% (elevated)
- SaturationShoebox avg > 75% (critical — approaching throttle threshold)
- Correlated with high ServiceApiHit and 429 responses

**Impact:** Vault will start throttling requests once saturation reaches 100%.

**Resolution:** Distribute workload across multiple vaults, reduce unnecessary API calls, implement client-side caching.

### Dormant Vault Detection

Vaults with zero traffic over the scan period may be orphaned resources.

**Signals:**
- All metrics return empty timeSeries
- No API hits, no latency data, no availability data
- Vault exists in Resource Graph but has no activity

**Impact:** Orphaned vaults incur costs and increase the security attack surface. Stored secrets may have expired without rotation.

**Investigation:** Check if the vault contains any secrets/keys. Cross-reference with deployment records and application configurations to determine if the vault is still needed.

## Analysis Techniques

### Cross-Vault Comparison

When a vault is flagged, compare it against similar vaults:

1. **Same region** — if multiple vaults show the same issue, it's likely a regional or platform problem
2. **Different regions** — if only one region is affected, it's region-specific
3. **Same application** — if vaults used by the same application are all affected, the issue is likely client-driven

### Error Rate Calculation

Always compute error rate rather than just error count:
- Error rate = (error results / total API hits) x 100
- Low error count with high total API hits = acceptable
- Low error count with low total API hits = potentially significant

### Latency Attribution

When latency is high, determine the source:
1. Check ServiceApiLatency avg vs max — high max with low avg indicates tail latency (usually normal)
2. Check if latency correlates with high ServiceApiHit — load-induced latency
3. Check if latency correlates with 429 throttling — retry storms inflate perceived latency
4. Compare across regions — if all regions are slow, it may be a platform-wide issue
