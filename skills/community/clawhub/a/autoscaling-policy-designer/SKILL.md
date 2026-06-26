---
name: autoscaling-policy-designer
description: Design autoscaling policies based on traffic patterns, cost constraints, and performance SLOs
---

# Autoscaling Policy Designer

Design autoscaling policies that balance performance, cost, and reliability. This skill teaches an AI agent to analyze historical traffic patterns, recommend scaling thresholds, configure Kubernetes HPA/KEDA or cloud-native autoscalers, simulate behavior under load, and model the cost impact of different scaling strategies.

Use when: "design autoscaling", "scaling policy", "HPA configuration", "KEDA setup", "scale to zero", "autoscaling thresholds", "scaling costs", "traffic spike handling", "over-provisioned", "under-provisioned"

## Commands

### 1. `analyze` -- Study traffic patterns

Before designing a policy, understand the workload. Collect metrics, identify patterns, and classify the traffic shape.

#### Step 1: Collect historical utilization data

```bash
# Kubernetes: Get CPU/memory utilization over 7 days from Prometheus
curl -s "$PROMETHEUS_URL/api/v1/query_range" \
  --data-urlencode 'query=avg(rate(container_cpu_usage_seconds_total{namespace="production",pod=~"api-.*"}[5m])) by (pod)' \
  --data-urlencode "start=$(date -d '7 days ago' +%s)" \
  --data-urlencode "end=$(date +%s)" \
  --data-urlencode 'step=1h' | python3 -c "
import json, sys
from datetime import datetime

data = json.load(sys.stdin)
for series in data['data']['result']:
    pod = series['metric'].get('pod', 'aggregate')
    values = [float(v[1]) for v in series['values']]
    print(f'{pod}:')
    print(f'  min:  {min(values):.3f} cores')
    print(f'  avg:  {sum(values)/len(values):.3f} cores')
    print(f'  max:  {max(values):.3f} cores')
    print(f'  p95:  {sorted(values)[int(len(values)*0.95)]:.3f} cores')
    print(f'  p99:  {sorted(values)[int(len(values)*0.99)]:.3f} cores')
"

# AWS: Get CloudWatch CPU utilization for an ASG
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=AutoScalingGroupName,Value="$ASG_NAME" \
  --start-time "$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S)" \
  --end-time "$(date -u +%Y-%m-%dT%H:%M:%S)" \
  --period 3600 \
  --statistics Average Maximum \
  --output json | python3 -c "
import json, sys
data = json.load(sys.stdin)
points = sorted(data['Datapoints'], key=lambda x: x['Timestamp'])
for p in points:
    print(f'{p[\"Timestamp\"]:>25}  avg={p[\"Average\"]:5.1f}%  max={p[\"Maximum\"]:5.1f}%')
"
```

#### Step 2: Identify the traffic pattern class

Classify the workload into one of these patterns, because each requires a different scaling strategy:

```python
import json, sys
from collections import defaultdict
from datetime import datetime

def classify_traffic(timestamps_values):
    """Classify traffic into a pattern type based on 7 days of hourly data."""
    by_hour = defaultdict(list)
    by_weekday = defaultdict(list)

    for ts, val in timestamps_values:
        dt = datetime.fromtimestamp(float(ts))
        by_hour[dt.hour].append(float(val))
        by_weekday[dt.weekday()].append(float(val))

    hourly_avgs = {h: sum(v)/len(v) for h, v in by_hour.items()}
    weekday_avgs = {d: sum(v)/len(v) for d, v in by_weekday.items()}

    peak_hour = max(hourly_avgs, key=hourly_avgs.get)
    trough_hour = min(hourly_avgs, key=hourly_avgs.get)
    peak_to_trough = hourly_avgs[peak_hour] / max(hourly_avgs[trough_hour], 0.001)

    weekday_avg = sum(weekday_avgs.get(d, 0) for d in range(5)) / 5
    weekend_avg = sum(weekday_avgs.get(d, 0) for d in range(5, 7)) / 2

    all_values = [v for _, v in timestamps_values]
    max_val = max(float(v) for v in all_values)
    avg_val = sum(float(v) for v in all_values) / len(all_values)
    spike_ratio = max_val / max(avg_val, 0.001)

    pattern = {
        "peak_hour": f"{peak_hour}:00",
        "trough_hour": f"{trough_hour}:00",
        "peak_to_trough_ratio": round(peak_to_trough, 1),
        "weekday_vs_weekend_ratio": round(weekday_avg / max(weekend_avg, 0.001), 1),
        "spike_ratio": round(spike_ratio, 1),
    }

    if peak_to_trough > 3:
        pattern["type"] = "DAILY_CYCLE"
        pattern["strategy"] = "Predictive scaling + reactive HPA. Pre-warm before peak hours."
    elif spike_ratio > 5:
        pattern["type"] = "SPIKE"
        pattern["strategy"] = "Aggressive scale-up (short stabilization window), conservative scale-down."
    elif weekday_avg / max(weekend_avg, 0.001) > 2:
        pattern["type"] = "WEEKLY_CYCLE"
        pattern["strategy"] = "Scheduled scaling for weekday/weekend transitions + HPA for within-day variation."
    else:
        pattern["type"] = "STEADY_STATE"
        pattern["strategy"] = "Simple target-tracking policy. Right-size the baseline."

    return pattern

# Example: parse Prometheus query_range output
# result = classify_traffic(data['data']['result'][0]['values'])
# print(json.dumps(result, indent=2))
```

#### Step 3: Analyze request-level metrics (for RPS-based scaling)

```bash
# Get requests per second over 7 days
curl -s "$PROMETHEUS_URL/api/v1/query_range" \
  --data-urlencode 'query=sum(rate(http_requests_total{namespace="production",service="api"}[5m]))' \
  --data-urlencode "start=$(date -d '7 days ago' +%s)" \
  --data-urlencode "end=$(date +%s)" \
  --data-urlencode 'step=1h' | python3 -c "
import json, sys
data = json.load(sys.stdin)
values = [(float(v[0]), float(v[1])) for v in data['data']['result'][0]['values']]
rps_values = [v for _, v in values]
print(f'RPS over 7 days:')
print(f'  min:  {min(rps_values):.0f} rps')
print(f'  avg:  {sum(rps_values)/len(rps_values):.0f} rps')
print(f'  max:  {max(rps_values):.0f} rps')
print(f'  p99:  {sorted(rps_values)[int(len(rps_values)*0.99)]:.0f} rps')
print(f'  Capacity per pod (from load tests): ~200 rps')
print(f'  Min pods needed at peak: {int(max(rps_values)/200) + 1}')
print(f'  Min pods needed at trough: {max(1, int(min(rps_values)/200))}')
"

# Get response latency percentiles to determine SLO baseline
curl -s "$PROMETHEUS_URL/api/v1/query" \
  --data-urlencode 'query=histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service="api"}[5m])) by (le))' | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
p99 = float(data['data']['result'][0]['value'][1])
print(f'Current p99 latency: {p99*1000:.0f}ms')
if p99 < 0.2:
    print('SLO headroom: GOOD (p99 < 200ms)')
elif p99 < 0.5:
    print('SLO headroom: TIGHT (p99 200-500ms)')
else:
    print('SLO headroom: CRITICAL (p99 > 500ms, scaling may be needed now)')
"
```

#### Report template

```
## Traffic Pattern Analysis

**Service:** api-service
**Period:** YYYY-MM-DD to YYYY-MM-DD (7 days)
**Data source:** Prometheus

### Utilization Summary
- CPU: avg 0.35 cores, p95 1.2 cores, max 2.1 cores
- Memory: avg 512MB, p95 780MB, max 1.1GB
- RPS: avg 450, p95 1,200, max 2,800

### Pattern Classification
- **Type:** DAILY_CYCLE
- **Peak hours:** 09:00-17:00 UTC
- **Trough hours:** 02:00-06:00 UTC
- **Peak-to-trough ratio:** 4.2x
- **Weekend reduction:** 60% lower than weekday

### Scaling Implications
- Minimum pods needed at trough: 3
- Minimum pods needed at peak: 14
- Currently running: 10 (fixed) -- overprovisioned at night, tight at peak
- Recommended strategy: Predictive scaling + reactive HPA
```

---

### 2. `design` -- Create a scaling policy

Based on the traffic analysis, generate a concrete autoscaler configuration.

#### Step 1: Kubernetes HPA (resource-based)

```yaml
# Standard HPA for daily-cycle workloads
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3           # Floor: handles trough traffic + one pod failure
  maxReplicas: 25          # Ceiling: cost cap
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60    # React to traffic in 1 min
      policies:
        - type: Percent
          value: 100                    # Can double capacity per minute
          periodSeconds: 60
        - type: Pods
          value: 4                      # But add at least 4 pods at a time
          periodSeconds: 60
      selectPolicy: Max                 # Use whichever adds more pods
    scaleDown:
      stabilizationWindowSeconds: 300   # Wait 5 min before scaling down
      policies:
        - type: Percent
          value: 25                     # Remove at most 25% per 2 min
          periodSeconds: 120
      selectPolicy: Min                 # Use whichever removes fewer pods
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 65        # Target 65% -- headroom for spikes
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 75
```

#### Step 2: KEDA (event-driven scaling)

For workloads that should scale based on queue depth, RPS, or custom metrics.

```yaml
# KEDA ScaledObject for a queue-processing worker
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: worker-scaler
  namespace: production
spec:
  scaleTargetRef:
    name: worker
  pollingInterval: 15
  cooldownPeriod: 120
  minReplicaCount: 0        # Scale to zero when queue is empty
  maxReplicaCount: 50
  triggers:
    - type: rabbitmq
      metadata:
        host: amqp://user:pass@rabbitmq.production:5672/
        queueName: jobs
        queueLength: "10"    # 1 pod per 10 queued messages
    - type: prometheus
      metadata:
        serverAddress: http://prometheus.monitoring:9090
        query: sum(rate(http_requests_total{service="api"}[2m]))
        threshold: "100"     # 1 pod per 100 rps
        activationThreshold: "5"  # Don't scale from zero until 5 rps
```

#### Step 3: AWS Auto Scaling Group policy

```bash
# Create a target-tracking scaling policy for an ASG
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name "$ASG_NAME" \
  --policy-name "cpu-target-tracking" \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ASGAverageCPUUtilization"
    },
    "TargetValue": 65.0,
    "ScaleInCooldown": 300,
    "ScaleOutCooldown": 60
  }'

# Add a scheduled scaling action for known daily pattern
aws autoscaling put-scheduled-update-group-action \
  --auto-scaling-group-name "$ASG_NAME" \
  --scheduled-action-name "morning-scaleup" \
  --recurrence "0 8 * * MON-FRI" \
  --min-size 6 \
  --desired-capacity 8

aws autoscaling put-scheduled-update-group-action \
  --auto-scaling-group-name "$ASG_NAME" \
  --scheduled-action-name "evening-scaledown" \
  --recurrence "0 20 * * *" \
  --min-size 2 \
  --desired-capacity 3
```

#### Step 4: Validate the design

```bash
# Check current HPA status
kubectl get hpa -n production -o wide

# Verify HPA can read the metrics it needs
kubectl get --raw "/apis/metrics.k8s.io/v1beta1/namespaces/production/pods" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for pod in data['items']:
    name = pod['metadata']['name']
    for c in pod['containers']:
        cpu = c['usage']['cpu']
        mem = c['usage']['memory']
        print(f'{name}: cpu={cpu}, mem={mem}')
"

# Check if custom metrics API is available (needed for RPS-based scaling)
kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta1" 2>/dev/null && echo "Custom metrics API available" || echo "Custom metrics API NOT available -- install prometheus-adapter"
```

---

### 3. `simulate` -- Model behavior under load

Before deploying a scaling policy, simulate how it would react to different traffic scenarios.

#### Step 1: Replay historical traffic against the proposed policy

```python
import json

def simulate_hpa(traffic_rps, capacity_per_pod, target_utilization,
                 min_replicas, max_replicas, scaleup_window_s, scaledown_window_s,
                 interval_s=60):
    """Simulate HPA behavior over a traffic timeline."""
    current_replicas = min_replicas
    history = []
    scaleup_cooldown = 0
    scaledown_cooldown = 0

    for i, rps in enumerate(traffic_rps):
        timestamp_min = i * interval_s // 60
        total_capacity = current_replicas * capacity_per_pod
        utilization = rps / max(total_capacity, 1)

        desired = max(min_replicas, min(max_replicas,
                      int(rps / (capacity_per_pod * target_utilization)) + 1))

        if desired > current_replicas and scaleup_cooldown <= 0:
            # Scale up: can double at most
            scale_to = min(desired, current_replicas * 2, max_replicas)
            current_replicas = scale_to
            scaleup_cooldown = scaleup_window_s // interval_s
            event = "SCALE UP"
        elif desired < current_replicas and scaledown_cooldown <= 0:
            # Scale down: remove at most 25%
            scale_to = max(desired, int(current_replicas * 0.75), min_replicas)
            current_replicas = scale_to
            scaledown_cooldown = scaledown_window_s // interval_s
            event = "SCALE DOWN"
        else:
            event = ""

        scaleup_cooldown = max(0, scaleup_cooldown - 1)
        scaledown_cooldown = max(0, scaledown_cooldown - 1)

        slo_ok = utilization < 0.85  # SLO: stay under 85% utilization
        history.append({
            "minute": timestamp_min,
            "rps": rps,
            "replicas": current_replicas,
            "utilization": round(utilization * 100, 1),
            "slo_ok": slo_ok,
            "event": event
        })

    return history

# Scenario 1: Normal daily cycle (24 hours, 1-min intervals)
import math
daily_traffic = [int(200 + 800 * max(0, math.sin((h - 6) * math.pi / 12)))
                 for h in range(24) for _ in range(60)]

result = simulate_hpa(
    traffic_rps=daily_traffic,
    capacity_per_pod=200,
    target_utilization=0.65,
    min_replicas=3,
    max_replicas=25,
    scaleup_window_s=60,
    scaledown_window_s=300
)

slo_violations = sum(1 for r in result if not r['slo_ok'])
max_replicas_used = max(r['replicas'] for r in result)
print(f"Daily cycle simulation:")
print(f"  SLO violations: {slo_violations} / {len(result)} minutes ({slo_violations/len(result)*100:.1f}%)")
print(f"  Max replicas used: {max_replicas_used}")
print(f"  Scale events: {sum(1 for r in result if r['event'])}")
```

#### Step 2: Simulate a traffic spike

```python
# Scenario 2: 10x traffic spike lasting 15 minutes
spike_traffic = [300] * 60 + [3000] * 15 + [300] * 60  # ramp, spike, recovery

result = simulate_hpa(
    traffic_rps=spike_traffic,
    capacity_per_pod=200,
    target_utilization=0.65,
    min_replicas=3,
    max_replicas=25,
    scaleup_window_s=60,
    scaledown_window_s=300
)

# Find how long until capacity catches up
spike_start = 60
for r in result[spike_start:]:
    if r['utilization'] < 85:
        catch_up_min = r['minute'] - spike_start
        print(f"Capacity caught up in {catch_up_min} minutes after spike start")
        break
else:
    print("WARNING: Capacity never caught up during spike")

slo_violations_during_spike = sum(1 for r in result[60:75] if not r['slo_ok'])
print(f"SLO violations during spike: {slo_violations_during_spike} / 15 minutes")
```

#### Step 3: Check for flapping

```python
# Scenario 3: Oscillating traffic (tests stabilization windows)
import random
oscillating = [500 + 300 * (1 if i % 6 < 3 else -1) + random.randint(-50, 50)
               for i in range(120)]

result = simulate_hpa(
    traffic_rps=oscillating,
    capacity_per_pod=200,
    target_utilization=0.65,
    min_replicas=3,
    max_replicas=25,
    scaleup_window_s=60,
    scaledown_window_s=300
)

scale_events = [r for r in result if r['event']]
print(f"Oscillation test: {len(scale_events)} scale events in {len(result)} minutes")
if len(scale_events) > 20:
    print("WARNING: Possible flapping. Increase stabilization windows.")
else:
    print("OK: Scaling is stable under oscillating load.")
```

---

### 4. `cost` -- Project scaling costs

Model the monthly cost of the autoscaling policy versus alternatives.

#### Step 1: Calculate cost for different strategies

```python
import json

def model_monthly_cost(
    strategy,
    min_pods, max_pods,
    cpu_per_pod, mem_gb_per_pod,
    cpu_cost_hr, mem_cost_hr_gb,
    peak_hours_per_day=8,
    avg_pods_at_peak=None,
    avg_pods_off_peak=None
):
    """Model monthly cost of a scaling strategy."""
    hours_per_month = 730  # 24 * 30.4

    if strategy == "fixed_at_peak":
        pods = max_pods
        cost = pods * hours_per_month * (cpu_per_pod * cpu_cost_hr + mem_gb_per_pod * mem_cost_hr_gb)
        return {"strategy": strategy, "monthly_cost": round(cost, 2), "avg_pods": pods}

    elif strategy == "fixed_at_average":
        pods = (min_pods + max_pods) // 2
        cost = pods * hours_per_month * (cpu_per_pod * cpu_cost_hr + mem_gb_per_pod * mem_cost_hr_gb)
        return {"strategy": strategy, "monthly_cost": round(cost, 2), "avg_pods": pods,
                "risk": "Under-provisioned at peak, SLO violations likely"}

    elif strategy == "autoscaled":
        peak_hours = peak_hours_per_day * 30.4
        off_peak_hours = hours_per_month - peak_hours
        peak_pods = avg_pods_at_peak or int(max_pods * 0.7)
        off_peak_pods = avg_pods_off_peak or min_pods
        cost = ((peak_pods * peak_hours + off_peak_pods * off_peak_hours) *
                (cpu_per_pod * cpu_cost_hr + mem_gb_per_pod * mem_cost_hr_gb))
        return {"strategy": strategy, "monthly_cost": round(cost, 2),
                "avg_pods_peak": peak_pods, "avg_pods_off_peak": off_peak_pods}

    elif strategy == "scale_to_zero":
        # For batch/worker: assume active only when queue has items
        active_hours = peak_hours_per_day * 30.4
        avg_pods = avg_pods_at_peak or max_pods // 2
        cost = avg_pods * active_hours * (cpu_per_pod * cpu_cost_hr + mem_gb_per_pod * mem_cost_hr_gb)
        return {"strategy": strategy, "monthly_cost": round(cost, 2),
                "active_hours_per_month": round(active_hours, 0)}

# Compare strategies
params = dict(min_pods=3, max_pods=20, cpu_per_pod=0.5, mem_gb_per_pod=1.0,
              cpu_cost_hr=0.048, mem_cost_hr_gb=0.006, peak_hours_per_day=8,
              avg_pods_at_peak=14, avg_pods_off_peak=3)

strategies = ["fixed_at_peak", "fixed_at_average", "autoscaled", "scale_to_zero"]
results = []
for s in strategies:
    results.append(model_monthly_cost(strategy=s, **params))

baseline = results[0]["monthly_cost"]
print(f"{'Strategy':<20} {'Monthly Cost':>12} {'vs Fixed Peak':>14}")
print("-" * 48)
for r in results:
    savings = (1 - r["monthly_cost"] / baseline) * 100
    print(f"{r['strategy']:<20} ${r['monthly_cost']:>10.2f} {savings:>+12.1f}%")
```

#### Step 2: Factor in spot/preemptible instances

```bash
# AWS: Compare on-demand vs spot pricing for the instance type
aws ec2 describe-spot-price-history \
  --instance-types m5.large \
  --product-descriptions "Linux/UNIX" \
  --start-time "$(date -u -d '1 day ago' +%Y-%m-%dT%H:%M:%S)" \
  --query 'SpotPriceHistory[*].{AZ:AvailabilityZone,Price:SpotPrice,Time:Timestamp}' \
  --output table

# GKE: Check if node pool supports spot VMs
gcloud container node-pools describe "$NODE_POOL" \
  --cluster "$CLUSTER" --zone "$ZONE" \
  --format="value(config.spot)"
```

#### Report template

```
## Autoscaling Cost Projection

**Service:** api-service
**Instance type:** m5.large (2 vCPU, 8GB RAM)
**Region:** us-east-1

### Strategy Comparison (monthly)
| Strategy | Monthly Cost | Savings vs Fixed | Risk |
|----------|-------------|-----------------|------|
| Fixed at peak (20 pods) | $1,576.80 | baseline | None (over-provisioned) |
| Fixed at average (11 pods) | $867.24 | -45.0% | SLO violations at peak |
| Autoscaled (3-20 pods) | $623.88 | -60.4% | 1-2 min lag on spikes |
| Scale-to-zero + autoscale | $412.32 | -73.8% | Cold start latency |

### Recommended: Autoscaled (3-20 pods)
- Estimated savings: $952.92/month ($11,435/year) vs fixed-at-peak
- SLO risk: Minimal (simulation shows 0.3% violation rate)
- Cold start: N/A (min 3 pods always warm)

### Spot instance opportunity
- Current on-demand cost per pod: $0.054/hr
- Current spot price: $0.018/hr (67% discount)
- If 50% of scale-out pods use spot: additional $156/month savings
- Recommendation: Use spot for pods above minReplicas, on-demand for baseline
```
