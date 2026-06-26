---
name: capacity-planner
description: Forecast infrastructure capacity needs using historical metrics, growth projections, and cost modeling. Identify bottlenecks before they cause outages and right-size resources to avoid over-provisioning.
---

# Capacity Planner

Forecast when your infrastructure will hit limits. Analyze historical metrics (CPU, memory, disk, network, database connections), project growth curves, identify approaching bottlenecks, and recommend right-sizing — so you scale proactively instead of reactively.

Use when: "when will we run out of space", "capacity forecast", "right-size our instances", "are we over-provisioned", "plan for traffic growth", "infrastructure scaling plan", "when do we need to upgrade", or before budget planning.

## Commands

### 1. `forecast` — Project Resource Exhaustion

#### Step 1: Collect Historical Metrics

```bash
# Prometheus — CPU utilization over last 30 days
curl -s "$PROMETHEUS_URL/api/v1/query_range" \
  --data-urlencode 'query=avg(rate(node_cpu_seconds_total{mode!="idle"}[5m])) by (instance)' \
  --data-urlencode "start=$(date -d '30 days ago' +%s)" \
  --data-urlencode "end=$(date +%s)" \
  --data-urlencode 'step=1h' | python3 -c "
import json, sys
data = json.load(sys.stdin)
for result in data['data']['result']:
    instance = result['metric']['instance']
    values = [float(v[1]) for v in result['values']]
    avg = sum(values) / len(values)
    peak = max(values)
    trend = (values[-1] - values[0]) / len(values)  # slope per hour
    print(f'{instance}: avg={avg:.1%} peak={peak:.1%} trend={trend:+.4%}/hr')
"

# Disk usage over time
df -h / /data /var 2>/dev/null
# Historical disk growth (if monitoring available)
curl -s "$PROMETHEUS_URL/api/v1/query_range" \
  --data-urlencode 'query=node_filesystem_avail_bytes{mountpoint="/"}' \
  --data-urlencode "start=$(date -d '30 days ago' +%s)" \
  --data-urlencode "end=$(date +%s)" \
  --data-urlencode 'step=1d'

# Memory usage
free -h
# Database connections
curl -s "$PROMETHEUS_URL/api/v1/query" \
  --data-urlencode 'query=pg_stat_activity_count / pg_settings_max_connections'
```

If Prometheus unavailable, use CloudWatch, Datadog, or system tools:
```bash
# Last 30 days of CloudWatch CPU
aws cloudwatch get-metric-statistics --namespace AWS/EC2 \
  --metric-name CPUUtilization --statistics Average Maximum \
  --dimensions Name=InstanceId,Value=i-0abc123 \
  --start-time $(date -d '30 days ago' -u +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) --period 86400
```

#### Step 2: Fit Growth Model

For each resource, determine growth pattern:
- **Linear:** constant rate of increase (disk filling at 2GB/day)
- **Exponential:** accelerating growth (user base doubling quarterly)
- **Seasonal:** cyclical patterns (weekend dips, end-of-month spikes)
- **Flat:** no growth (stable, well-bounded workload)

Calculate days until exhaustion:
```
days_remaining = (capacity - current_usage) / daily_growth_rate
```

For exponential: use doubling time to project.

#### Step 3: Generate Forecast Report

```markdown
# Capacity Forecast Report — [date]

## Critical (exhaustion < 30 days)
| Resource | Current | Capacity | Growth/day | Exhaustion | Action |
|----------|---------|----------|------------|------------|--------|
| Disk (/) | 45 GB | 50 GB | 180 MB/day | ~28 days | Expand volume or add cleanup cron |
| DB connections | 85/100 | 100 | +2/week | ~5 weeks | Increase max_connections or add pgbouncer |

## Warning (exhaustion 30-90 days)
| Resource | Current | Capacity | Growth/day | Exhaustion |
|----------|---------|----------|------------|------------|
| Memory | 12/16 GB | 16 GB | 50 MB/day | ~82 days |

## Healthy (>90 days or no growth)
- CPU: avg 35%, peak 72%, flat trend — no action needed
- Network: avg 200 Mbps of 1 Gbps — no concern

## Over-Provisioned (wasting money)
| Resource | Used | Provisioned | Utilization | Savings |
|----------|------|-------------|-------------|---------|
| worker-pool-3 | 2 vCPU avg | 8 vCPU | 25% | Downsize to 4 vCPU, save ~$150/mo |
| Redis cluster | 512 MB | 8 GB | 6% | Downsize to 2 GB, save ~$80/mo |
```

### 2. `rightsize` — Recommend Instance Sizes

Given current utilization and growth projections:
- Map workload to optimal instance family (compute, memory, storage-optimized)
- Factor in reserved instance / savings plan pricing
- Account for headroom (recommend 60-70% target utilization, not 95%)
- Compare across cloud providers if multi-cloud

### 3. `cost-model` — Project Infrastructure Costs

Given the capacity forecast:
- Calculate current monthly spend
- Project spend at 3, 6, 12 months based on growth
- Identify the biggest cost drivers
- Suggest cost optimization levers (spot instances, reserved pricing, auto-scaling, compression, archival)

### 4. `bottleneck` — Identify Scaling Bottlenecks

Analyze the system for the component that will fail first under load:
- Database (connections, IOPS, lock contention)
- Application (CPU-bound, memory-bound, thread pool exhaustion)
- Network (bandwidth, DNS resolution, TLS handshake overhead)
- External dependencies (rate limits, API quotas, third-party SLAs)

Rank bottlenecks by "time to impact" and recommend mitigation order.
