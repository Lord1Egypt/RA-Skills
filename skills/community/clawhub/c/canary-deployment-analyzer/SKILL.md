---
name: canary-deployment-analyzer
description: Analyze canary deployments by comparing metrics between canary and baseline. Provide data-driven promotion/rollback recommendations based on error rates, latency percentiles, and custom business metrics.
---

# Canary Deployment Analyzer

Analyze canary deployments to decide whether to promote or rollback. Compare error rates, latency distributions, business metrics, and log patterns between canary and baseline populations — then give a data-driven recommendation.

Use when: "analyze canary", "should we promote this canary", "compare canary metrics", "canary vs baseline", "is this deploy safe to promote", "canary health check", or during progressive delivery decisions.

## Commands

### 1. `analyze` — Full Canary Analysis

#### Step 1: Collect Metrics

Identify the metrics source (Prometheus, Datadog, CloudWatch, custom):

```bash
# Prometheus query examples
# Error rate — canary vs stable
curl -s "$PROMETHEUS_URL/api/v1/query" --data-urlencode \
  'query=sum(rate(http_requests_total{status=~"5..",deployment="canary"}[5m])) / sum(rate(http_requests_total{deployment="canary"}[5m]))' | \
  python3 -c "import json,sys;r=json.load(sys.stdin);print(f'Canary error rate: {r[\"data\"][\"result\"][0][\"value\"][1] if r[\"data\"][\"result\"] else \"no data\"}')"

# Same for baseline
curl -s "$PROMETHEUS_URL/api/v1/query" --data-urlencode \
  'query=sum(rate(http_requests_total{status=~"5..",deployment="stable"}[5m])) / sum(rate(http_requests_total{deployment="stable"}[5m]))' | \
  python3 -c "import json,sys;r=json.load(sys.stdin);print(f'Baseline error rate: {r[\"data\"][\"result\"][0][\"value\"][1] if r[\"data\"][\"result\"] else \"no data\"}')"

# Latency p50/p95/p99
for q in 50 95 99; do
  curl -s "$PROMETHEUS_URL/api/v1/query" --data-urlencode \
    "query=histogram_quantile(0.${q}, sum(rate(http_request_duration_seconds_bucket{deployment=\"canary\"}[5m])) by (le))"
done
```

If no Prometheus, check for:
- Datadog: `curl -s "https://api.datadoghq.com/api/v1/query" -H "DD-API-KEY: $DD_API_KEY" --data-urlencode "query=avg:http.request.duration{deployment:canary}"`
- CloudWatch: `aws cloudwatch get-metric-statistics --namespace MyApp --metric-name ErrorRate --dimensions Name=Deployment,Value=canary`
- Application logs: parse error counts from structured logs

#### Step 2: Statistical Comparison

For each metric, calculate:

1. **Absolute difference:** canary_value - baseline_value
2. **Relative change:** (canary - baseline) / baseline × 100%
3. **Statistical significance:** For rates, use a two-proportion z-test; for latencies, use Welch's t-test or Mann-Whitney U if distributions are skewed

Decision thresholds (configurable):
- Error rate increase > 0.1% absolute OR > 10% relative → **FAIL**
- p95 latency increase > 50ms OR > 15% relative → **WARNING**
- p99 latency increase > 200ms OR > 25% relative → **FAIL**
- Business metric (conversion, throughput) decrease > 5% → **WARNING**

#### Step 3: Log Analysis

```bash
# Compare error log patterns
# Canary errors
kubectl logs -l deployment=canary --since=1h 2>/dev/null | grep -i "error\|exception\|panic\|fatal" | \
  sort | uniq -c | sort -rn | head -20

# Baseline errors
kubectl logs -l deployment=stable --since=1h 2>/dev/null | grep -i "error\|exception\|panic\|fatal" | \
  sort | uniq -c | sort -rn | head -20
```

Look for:
- **New error types** in canary that don't appear in baseline (strongest signal)
- **Error rate spike** in existing error types
- **Timeout patterns** or **connection refused** (infrastructure issues vs code issues)

#### Step 4: Generate Verdict

```markdown
# Canary Analysis Report

## Verdict: PROMOTE / ROLLBACK / HOLD

## Metrics Comparison (last 30 min)
| Metric | Baseline | Canary | Delta | Status |
|--------|----------|--------|-------|--------|
| Error rate | 0.12% | 0.14% | +0.02% | ✅ Pass |
| p50 latency | 45ms | 48ms | +3ms | ✅ Pass |
| p95 latency | 180ms | 210ms | +30ms | ✅ Pass |
| p99 latency | 450ms | 620ms | +170ms | ⚠️ Warning |
| Throughput | 1200 rps | 1180 rps | -1.7% | ✅ Pass |

## New Errors in Canary
- `NullPointerException in UserService.getProfile` (23 occurrences)
  → Not present in baseline — likely regression

## Traffic Split
- Canary: 5% (60 rps)
- Baseline: 95% (1140 rps)
- Observation window: 30 min (sufficient for 5% traffic)

## Recommendation
[PROMOTE] Metrics within acceptable thresholds. p99 latency elevated but within warning range.
Monitor p99 closely after full promotion. Investigate NullPointerException — non-blocking but should be tracked.
```

### 2. `thresholds` — Configure Promotion Criteria

Help define canary promotion thresholds based on SLOs:

- If team has SLOs → derive thresholds from error budget remaining
- If no SLOs → suggest industry defaults (99.9% availability = 0.1% error budget)
- Generate a config file for Argo Rollouts, Flagger, or custom canary controller

### 3. `progressive` — Design Progressive Delivery Strategy

Given a service profile (traffic volume, criticality, deployment frequency), recommend:
- Traffic split stages (1% → 5% → 25% → 50% → 100%)
- Observation window per stage
- Automated vs manual promotion gates
- Rollback trigger conditions
