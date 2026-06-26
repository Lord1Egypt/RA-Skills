---
name: dark-launch-controller
description: Plan and execute dark launches with feature flags, performance monitoring, and gradual exposure rollouts
---

# Dark Launch Controller

Plan and manage dark launches -- deploying new features into production fully hidden from users. Unlike shadow traffic (which mirrors requests), dark launches deploy the actual code path but gate visibility behind feature flags, percentage rollouts, or user-segment targeting. This skill covers launch planning, silent performance monitoring, and controlled promotion to user-facing traffic.

Use when: "dark launch", "feature flag deploy", "hidden feature", "dark deploy", "gradual rollout", "feature gate", "launch plan", "promote feature"

## Commands

### 1. `plan` --- Design a dark launch strategy

Analyze the feature to be launched and produce a dark launch plan with flag configuration, monitoring criteria, and promotion gates.

**Step 1 -- Inventory the feature scope**

```bash
# Identify what changed in the feature branch vs main
FEATURE_BRANCH="${1:-feature/new-feature}"
BASE_BRANCH="${2:-main}"

echo "=== Files changed ==="
git diff --stat "$BASE_BRANCH"..."$FEATURE_BRANCH"

echo ""
echo "=== Diff summary ==="
git diff --shortstat "$BASE_BRANCH"..."$FEATURE_BRANCH"

echo ""
echo "=== Changed services/packages ==="
git diff --name-only "$BASE_BRANCH"..."$FEATURE_BRANCH" | \
  awk -F/ '{print $1"/"$2}' | sort -u
```

**Step 2 -- Detect feature flag integration points**

```bash
# Scan for existing feature flag patterns in the codebase
echo "=== Existing feature flag patterns ==="
rg -n 'feature[_-]?flag|isEnabled|isFeatureOn|toggle|LaunchDarkly|Unleash|flipper|split\.io' \
  --type-add 'code:*.{py,go,js,ts,java,rb}' --type code -l 2>/dev/null | head -20

echo ""
echo "=== Feature flag config files ==="
find . -name '*feature*flag*' -o -name '*toggle*' -o -name '*feature*config*' 2>/dev/null | \
  grep -v node_modules | grep -v .git | head -20

echo ""
echo "=== Environment-based feature switches ==="
rg 'FEATURE_|ENABLE_|FF_|DARK_LAUNCH' --type-add 'config:*.{env,yaml,yml,json,toml}' --type config -l 2>/dev/null | head -20
```

**Step 3 -- Design the flag configuration**

```bash
# Generate feature flag specification
FEATURE_NAME="${3:-new-checkout-flow}"

python3 << PYEOF
import json

flag_spec = {
    "flag_key": "${FEATURE_NAME}".replace(" ", "-").lower(),
    "description": "Dark launch gate for ${FEATURE_NAME}",
    "type": "boolean",
    "default_value": False,
    "environments": {
        "development": {
            "enabled": True,
            "rules": [{"variation": True, "rollout_percentage": 100}]
        },
        "staging": {
            "enabled": True,
            "rules": [{"variation": True, "rollout_percentage": 100}]
        },
        "production": {
            "enabled": True,
            "rules": [
                {
                    "description": "Internal team only (dark launch phase)",
                    "variation": True,
                    "clauses": [
                        {"attribute": "email", "op": "endsWith", "values": ["@yourcompany.com"]}
                    ]
                },
                {
                    "description": "Default: feature hidden",
                    "variation": False,
                    "rollout_percentage": 0
                }
            ]
        }
    },
    "promotion_gates": {
        "phase_1_internal": {
            "audience": "internal employees only",
            "duration": "3 days minimum",
            "success_criteria": {
                "error_rate_delta": "< 0.1%",
                "p99_latency_delta": "< 15%",
                "no_new_error_types": True
            }
        },
        "phase_2_beta": {
            "audience": "5% of production traffic",
            "duration": "3 days minimum",
            "success_criteria": {
                "error_rate_delta": "< 0.5%",
                "p99_latency_delta": "< 10%",
                "user_feedback_score": "> 4.0"
            }
        },
        "phase_3_rollout": {
            "audience": "25% -> 50% -> 100%",
            "duration": "1 week per step",
            "success_criteria": {
                "error_rate_delta": "< 0.1%",
                "p99_latency_delta": "< 5%",
                "business_metric_impact": "neutral or positive"
            }
        }
    }
}

print(json.dumps(flag_spec, indent=2))
PYEOF
```

**Step 4 -- Generate Kubernetes deployment strategy**

```bash
cat << 'DEPLOYEOF'
# Dark launch deployment: code ships but feature is gated
# No separate deployment needed -- the flag controls visibility

# Option A: ConfigMap-based flag (simple, no external dependency)
apiVersion: v1
kind: ConfigMap
metadata:
  name: feature-flags
data:
  flags.json: |
    {
      "{FEATURE_KEY}": {
        "enabled": false,
        "internal_only": true,
        "rollout_percentage": 0
      }
    }

---
# Option B: Environment variable flag
# Add to deployment spec:
# env:
# - name: FF_{FEATURE_KEY_UPPER}
#   value: "false"
# - name: FF_{FEATURE_KEY_UPPER}_INTERNAL
#   value: "true"
DEPLOYEOF
```

**Report template:**

```
## Dark Launch Plan: {FEATURE_NAME}

### Feature Scope
- Files changed: {N}
- Services affected: {list}
- Flag key: {flag_key}
- Flag type: {boolean/percentage/segment}

### Launch Phases
| Phase | Audience | Duration | Success Criteria |
|-------|---------|----------|-----------------|
| 1. Internal | Employees | 3 days | Error rate < 0.1%, p99 < +15% |
| 2. Beta | 5% users | 3 days | Error rate < 0.5%, p99 < +10% |
| 3. Ramp | 25/50/100% | 1wk/step | Metrics stable, business KPIs neutral+ |

### Rollback
- Instant: set flag to `false` (no deploy needed)
- Estimated rollback time: < 30 seconds

### Monitoring Setup Required
{list of dashboards and alerts to configure}
```

---

### 2. `monitor` --- Track dark feature performance in production

Monitor the hidden feature's impact on system performance even while it is gated.

**Step 1 -- Check feature flag state**

```bash
# Verify current flag configuration
NAMESPACE="${1:-default}"
FEATURE_KEY="${2:-new-checkout-flow}"

echo "=== ConfigMap-based flags ==="
kubectl get configmap feature-flags -n "$NAMESPACE" -o jsonpath='{.data.flags\.json}' 2>/dev/null | python3 -m json.tool || echo "No feature-flags ConfigMap found"

echo ""
echo "=== Environment variable flags ==="
kubectl get deployments -n "$NAMESPACE" -o json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for deploy in data['items']:
    name = deploy['metadata']['name']
    for c in deploy['spec']['template']['spec']['containers']:
        for env in c.get('env', []):
            if 'FF_' in env.get('name', '') or 'FEATURE_' in env.get('name', ''):
                val = env.get('value', env.get('valueFrom', 'ref'))
                print(f\"  {name}/{c['name']}: {env['name']}={val}\")
"
```

**Step 2 -- Measure code-path performance**

```bash
# Query application metrics for the feature code path
# Prometheus queries (adapt to your metrics naming)
PROM_URL="${PROMETHEUS_URL:-http://prometheus.monitoring.svc:9090}"

echo "=== Feature code path latency ==="
curl -s "$PROM_URL/api/v1/query" \
  --data-urlencode "query=histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{feature=\"${FEATURE_KEY}\"}[5m]))" \
  2>/dev/null | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for result in data.get('data', {}).get('result', []):
        labels = result['metric']
        value = result['value'][1]
        print(f\"  p99 latency: {float(value)*1000:.1f}ms  labels: {labels}\")
except Exception as e:
    print(f'  Could not query Prometheus: {e}')
"

echo ""
echo "=== Feature error rate ==="
curl -s "$PROM_URL/api/v1/query" \
  --data-urlencode "query=rate(http_requests_total{feature=\"${FEATURE_KEY}\",status=~\"5..\"}[5m]) / rate(http_requests_total{feature=\"${FEATURE_KEY}\"}[5m])" \
  2>/dev/null | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for result in data.get('data', {}).get('result', []):
        rate = float(result['value'][1]) * 100
        print(f\"  Error rate: {rate:.3f}%\")
except Exception as e:
    print(f'  Could not query Prometheus: {e}')
"
```

**Step 3 -- Compare with baseline**

```bash
python3 << 'PYEOF'
# Compare feature-on vs feature-off performance
# This requires metrics instrumented with a feature label

import json

# Simulated analysis logic -- replace with real Prometheus query results
def assess_gate(metric_name, current, threshold, unit="%"):
    passed = current <= threshold
    status = "PASS" if passed else "FAIL"
    print(f"  {status}: {metric_name} = {current:.3f}{unit} (threshold: {threshold}{unit})")
    return passed

print("=== Promotion Gate Assessment ===")
print()
all_pass = True
all_pass &= assess_gate("Error rate delta", 0.05, 0.1)
all_pass &= assess_gate("p99 latency delta", 8.2, 15.0, "% increase")
all_pass &= assess_gate("Memory usage delta", 2.1, 20.0, "% increase")
all_pass &= assess_gate("CPU usage delta", 1.5, 15.0, "% increase")

print()
if all_pass:
    print("VERDICT: All gates passed -- ready for next promotion phase")
else:
    print("VERDICT: One or more gates failed -- investigate before promoting")
PYEOF
```

**Step 4 -- Check resource consumption impact**

```bash
# Compare resource usage of pods with feature enabled vs baseline
NAMESPACE="${1:-default}"

echo "=== Current resource usage ==="
kubectl top pods -n "$NAMESPACE" --no-headers 2>/dev/null | sort -k3 -rn | head -20

echo ""
echo "=== Pod restart counts (detect instability) ==="
kubectl get pods -n "$NAMESPACE" -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{range .status.containerStatuses[*]}{.restartCount}{" "}{end}{"\n"}{end}' 2>/dev/null | awk '$2 > 0'
```

**Report template:**

```
## Dark Launch Monitoring Report: {FEATURE_KEY}

### Current State
- Flag status: {enabled/disabled}
- Audience: {internal/beta/N% rollout}
- Duration at current phase: {N days}

### Performance Metrics
| Metric | Baseline | With Feature | Delta | Gate |
|--------|---------|-------------|-------|------|
| Error rate | | | | {PASS/FAIL} |
| p99 latency | | | | {PASS/FAIL} |
| CPU usage | | | | {PASS/FAIL} |
| Memory usage | | | | {PASS/FAIL} |

### Stability
- Pod restarts: {N}
- OOM kills: {N}
- New error types: {list or "none"}

### Gate Verdict: {PASS / FAIL}
```

---

### 3. `promote` --- Plan exposure rollout

Generate the step-by-step promotion plan to move from dark to fully visible.

**Step 1 -- Validate promotion readiness**

```bash
# Check all promotion gates for the current phase
python3 << 'PYEOF'
phases = [
    {"name": "Internal", "pct": 0, "flag": "internal_only=true"},
    {"name": "Beta 5%", "pct": 5, "flag": "rollout_percentage=5"},
    {"name": "Ramp 25%", "pct": 25, "flag": "rollout_percentage=25"},
    {"name": "Ramp 50%", "pct": 50, "flag": "rollout_percentage=50"},
    {"name": "GA 100%", "pct": 100, "flag": "rollout_percentage=100"},
    {"name": "Cleanup", "pct": 100, "flag": "remove flag, hardcode feature"},
]

print("=== Promotion Phases ===")
print()
for i, p in enumerate(phases):
    status = "CURRENT >>>" if i == 1 else "          "  # adjust based on actual state
    print(f"  {status} Phase {i}: {p['name']} ({p['flag']})")
PYEOF
```

**Step 2 -- Generate promotion commands**

```bash
FEATURE_KEY="${1:-new-checkout-flow}"
NAMESPACE="${2:-default}"
TARGET_PHASE="${3:-beta}"  # internal|beta|ramp25|ramp50|ga|cleanup

echo "=== Promotion Commands for phase: $TARGET_PHASE ==="
echo ""

case "$TARGET_PHASE" in
  beta)
    echo "# Update ConfigMap to enable 5% rollout"
    echo "kubectl get configmap feature-flags -n $NAMESPACE -o json | \\"
    echo "  jq '.data[\"flags.json\"] |= (fromjson | .[\"$FEATURE_KEY\"].rollout_percentage = 5 | .[\"$FEATURE_KEY\"].internal_only = false | tojson)' | \\"
    echo "  kubectl apply -f -"
    echo ""
    echo "# Restart pods to pick up config change (if not using hot-reload)"
    echo "kubectl rollout restart deployment -n $NAMESPACE -l feature-flags=enabled"
    ;;
  ramp25)
    echo "kubectl get configmap feature-flags -n $NAMESPACE -o json | \\"
    echo "  jq '.data[\"flags.json\"] |= (fromjson | .[\"$FEATURE_KEY\"].rollout_percentage = 25 | tojson)' | \\"
    echo "  kubectl apply -f -"
    ;;
  ramp50)
    echo "kubectl get configmap feature-flags -n $NAMESPACE -o json | \\"
    echo "  jq '.data[\"flags.json\"] |= (fromjson | .[\"$FEATURE_KEY\"].rollout_percentage = 50 | tojson)' | \\"
    echo "  kubectl apply -f -"
    ;;
  ga)
    echo "kubectl get configmap feature-flags -n $NAMESPACE -o json | \\"
    echo "  jq '.data[\"flags.json\"] |= (fromjson | .[\"$FEATURE_KEY\"].rollout_percentage = 100 | tojson)' | \\"
    echo "  kubectl apply -f -"
    ;;
  cleanup)
    echo "# Feature is GA -- remove the flag from code and config"
    echo "# 1. Remove flag checks from application code:"
    echo "rg -l '$FEATURE_KEY' --type-add 'code:*.{py,go,js,ts,java,rb}' --type code"
    echo ""
    echo "# 2. Remove from ConfigMap"
    echo "kubectl get configmap feature-flags -n $NAMESPACE -o json | \\"
    echo "  jq '.data[\"flags.json\"] |= (fromjson | del(.[\"$FEATURE_KEY\"]) | tojson)' | \\"
    echo "  kubectl apply -f -"
    echo ""
    echo "# 3. Remove feature flag environment variables from deployments"
    echo "# Edit deployment manifests to remove FF_${FEATURE_KEY^^} env vars"
    ;;
esac
```

**Step 3 -- Generate rollback commands**

```bash
echo "=== Emergency Rollback ==="
echo ""
echo "# Instant kill switch (< 30 seconds if using hot-reload)"
echo "kubectl get configmap feature-flags -n $NAMESPACE -o json | \\"
echo "  jq '.data[\"flags.json\"] |= (fromjson | .[\"$FEATURE_KEY\"].enabled = false | .[\"$FEATURE_KEY\"].rollout_percentage = 0 | tojson)' | \\"
echo "  kubectl apply -f -"
echo ""
echo "# Force pod restart if config not hot-reloaded"
echo "kubectl rollout restart deployment -n $NAMESPACE -l feature-flags=enabled"
echo ""
echo "# Verify rollback"
echo "kubectl get configmap feature-flags -n $NAMESPACE -o jsonpath='{.data.flags\\.json}' | python3 -m json.tool"
```

**Report template:**

```
## Promotion Plan: {FEATURE_KEY}

### Current Phase: {phase_name}
### Target Phase: {next_phase_name}

### Pre-promotion Checklist
- [ ] All monitoring gates passed for current phase
- [ ] No unresolved incidents related to the feature
- [ ] Stakeholder approval obtained
- [ ] Rollback procedure tested

### Promotion Steps
1. {command to update flag}
2. Verify flag update applied
3. Monitor for 15 minutes
4. Check error rates and latency
5. If stable, confirm promotion complete

### Rollback (if needed)
- Command: {single command to disable flag}
- Expected rollback time: < 30 seconds
- Rollback does NOT require a deployment

### Schedule
| Phase | Target Date | Duration | Owner |
|-------|-----------|----------|-------|
```
