---
name: feature-toggle-manager
description: Audit, manage, and clean up feature flags across codebases to reduce toggle debt
---

# Feature Toggle Manager

Manage the full lifecycle of feature flags and toggles across a codebase. This skill teaches an AI agent to discover all toggle usage, detect stale or orphaned flags that should be removed, plan safe cleanup operations, and evaluate overall toggle debt. Supports LaunchDarkly, Unleash, environment-variable-based, and custom in-code implementations.

Use when: "audit feature flags", "find stale toggles", "clean up feature flags", "toggle debt", "feature flag lifecycle", "orphaned flags", "flag rollout plan"

## Commands

### 1. `audit` -- Find all toggles in code and check staleness

Discover every feature flag reference in the codebase, classify each by type and status, and produce a staleness report.

#### Step 1: Identify the toggle implementation pattern

Determine which toggle system is in use by scanning for known SDK imports and common patterns.

```bash
# Check for LaunchDarkly SDK
rg -l "launchdarkly|ldclient|LDClient|useFlags|withLDConsumer" --type-add 'code:*.{js,ts,tsx,py,go,java,rb,cs}' -t code .

# Check for Unleash SDK
rg -l "unleash-client|Unleash|isEnabled|unleash_client" --type-add 'code:*.{js,ts,tsx,py,go,java,rb}' -t code .

# Check for environment-variable-based flags
rg "FEATURE_|ENABLE_|FF_|TOGGLE_|FLAG_" --type-add 'code:*.{js,ts,py,go,java,env,yaml,yml,toml}' -t code .

# Check for custom toggle files (JSON/YAML config)
rg -l "featureFlags|feature_flags|toggles|feature.toggles" . -g '*.{json,yaml,yml,toml}'
```

#### Step 2: Extract a complete flag inventory

Build a structured list of every distinct flag name and where it appears.

```bash
# Extract flag names from LaunchDarkly variation calls
rg -o "variation\(['\"]([^'\"]+)['\"]" -r '$1' --no-filename . | sort -u

# Extract flag names from Unleash isEnabled calls
rg -o "isEnabled\(['\"]([^'\"]+)['\"]" -r '$1' --no-filename . | sort -u

# Extract environment-variable flags
rg -o "(FEATURE_[A-Z_]+|ENABLE_[A-Z_]+|FF_[A-Z_]+)" --no-filename . | sort -u

# For each flag, count references to gauge how embedded it is
for flag in $(rg -o "variation\(['\"]([^'\"]+)['\"]" -r '$1' --no-filename . | sort -u); do
  count=$(rg -c "$flag" -l . 2>/dev/null | wc -l)
  echo "$count files -- $flag"
done | sort -rn
```

#### Step 3: Assess staleness using git history

A flag is potentially stale if its last meaningful change was long ago and it has been consistently returning one value.

```bash
# For each flag, find the date it was last modified in any file
flag="my-feature-flag"
git log -1 --format="%ai" -S "$flag" -- '*.ts' '*.js' '*.py' '*.go'

# Bulk staleness check: flags not touched in 90+ days
threshold=$(date -d '90 days ago' +%s)
for flag in $(rg -o "variation\(['\"]([^'\"]+)['\"]" -r '$1' --no-filename . | sort -u); do
  last_date=$(git log -1 --format="%at" -S "$flag" 2>/dev/null)
  if [ -n "$last_date" ] && [ "$last_date" -lt "$threshold" ]; then
    human_date=$(date -d "@$last_date" +%Y-%m-%d)
    echo "STALE ($human_date) -- $flag"
  fi
done
```

#### Step 4: Cross-reference with the toggle service (if accessible)

```bash
# LaunchDarkly API: list flags and their current status
curl -s -H "Authorization: $LD_API_KEY" \
  "https://app.launchdarkly.com/api/v2/flags/$LD_PROJECT_KEY" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
for f in data.get('items', []):
    status = 'ON' if f['on'] else 'OFF'
    age_days = (json.loads('{\"now\":0}')['now'])  # placeholder
    print(f\"{status:>3}  {f['key']}  (envs: {len(f.get('environments', {}))})\" )
"

# Unleash API: list all toggles
curl -s -H "Authorization: $UNLEASH_API_TOKEN" \
  "$UNLEASH_URL/api/admin/features" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for f in data.get('features', []):
    stale = 'STALE' if f.get('stale') else 'active'
    print(f\"{stale:>6}  {f['name']}  type={f.get('type','unknown')}\")
"
```

#### Report template

```
## Feature Toggle Audit Report

**Date:** YYYY-MM-DD
**Repository:** repo-name
**Toggle system:** LaunchDarkly / Unleash / env-vars / custom

### Summary
- Total unique flags found: N
- Active (touched in last 90 days): N
- Stale (untouched 90+ days): N
- Orphaned (in code but not in service): N
- Phantom (in service but not in code): N

### Flag Inventory
| Flag Name | Files | Last Modified | Service Status | Recommendation |
|-----------|-------|---------------|----------------|----------------|
| flag-name | 12    | 2025-11-03    | ON (100%)      | REMOVE (fully rolled out) |

### Toggle Debt Score
- Debt score: N/10 (stale_count * 2 + orphan_count * 3, capped at 10)
- Recommended action: [cleanup sprint / urgent removal / acceptable]
```

---

### 2. `cleanup` -- Identify removable flags and generate removal plan

For each stale or fully-rolled-out flag, trace every code path it touches and produce a safe removal plan.

#### Step 1: Map the blast radius of a single flag

```bash
flag="old-feature-flag"

# Find every file referencing this flag
rg -l "$flag" .

# Show the actual usage context (5 lines around each match)
rg -C 5 "$flag" .

# Identify conditional branches that would collapse
rg -n "if.*$flag|$flag.*\?" . --type-add 'code:*.{js,ts,tsx,py,go,java}' -t code
```

#### Step 2: Determine the winning code path

Reason about which branch to keep. If the flag is ON everywhere (fully rolled out), keep the "enabled" branch. If OFF everywhere, keep the "disabled" branch (or delete the feature entirely).

```python
# Analysis helper: parse toggle usage and determine kept branch
import ast, sys

flag_name = sys.argv[1] if len(sys.argv) > 1 else "old-feature-flag"
# For Python codebases, find if/else blocks guarded by the flag
# and output which branch (if-body or else-body) to keep
print(f"Flag: {flag_name}")
print(f"Action: Keep the ENABLED branch (flag was fully rolled out)")
print(f"Files to modify: [list from rg output]")
print(f"Tests to update: [list test files referencing flag]")
```

#### Step 3: Validate no external dependencies

```bash
# Check if the flag is referenced in infrastructure configs
rg "$flag" . -g '*.{yaml,yml,json,tf,hcl,toml}'

# Check CI/CD pipelines
rg "$flag" . -g '{Jenkinsfile,*.groovy,.github/workflows/*,*.gitlab-ci.yml,Dockerfile*}'

# Check documentation
rg "$flag" . -g '*.{md,rst,txt,adoc}'
```

#### Step 4: Generate a removal checklist

For each flag targeted for cleanup, produce this checklist:

```
## Cleanup Plan: [flag-name]

**Current state:** ON in all environments for 120+ days
**Kept branch:** enabled (remove the conditional, keep the if-body)
**Risk:** LOW (no external config dependencies)

### Steps
1. [ ] Remove flag evaluation calls in: [file list]
2. [ ] Collapse conditional branches -- keep enabled path
3. [ ] Remove flag from toggle service configuration
4. [ ] Remove flag from environment variable definitions
5. [ ] Update or remove tests that mock this flag
6. [ ] Remove flag from documentation references
7. [ ] Verify build passes: `npm test` / `pytest` / `go test ./...`
8. [ ] Deploy to staging and verify behavior unchanged
9. [ ] Remove flag from LaunchDarkly/Unleash dashboard

### Files to modify (N total)
- `src/components/Feature.tsx` (lines 23, 45)
- `src/api/handler.py` (lines 112-130)
- `tests/test_feature.py` (lines 8, 34, 67)
```

---

### 3. `lifecycle` -- Plan flag rollout stages

Design a phased rollout plan for a new feature flag, including percentage ramps, monitoring checkpoints, and full-rollout criteria.

#### Step 1: Classify the flag type

Feature flags have different lifecycle expectations based on type:

- **Release toggle**: Short-lived (days-weeks). Gates a deployment. Remove after full rollout.
- **Experiment toggle**: Medium-lived (weeks-months). A/B test. Remove after decision.
- **Ops toggle**: Long-lived. Circuit breaker or kill switch. Keep indefinitely but review quarterly.
- **Permission toggle**: Long-lived. Entitlement gating. Part of the product, not debt.

#### Step 2: Define rollout stages

```python
import json

def generate_rollout_plan(flag_name, flag_type, total_users_estimate):
    stages = []
    if flag_type == "release":
        stages = [
            {"stage": "Internal", "percentage": 0, "audience": "employees only", "duration": "2-3 days", "gate": "no P0/P1 errors in logs"},
            {"stage": "Canary", "percentage": 5, "audience": "random 5%", "duration": "3-5 days", "gate": "error rate < baseline + 0.1%"},
            {"stage": "Early adopters", "percentage": 25, "audience": "random 25%", "duration": "3-5 days", "gate": "latency p99 within SLO"},
            {"stage": "Broad", "percentage": 50, "audience": "random 50%", "duration": "2-3 days", "gate": "no support ticket spike"},
            {"stage": "Full", "percentage": 100, "audience": "all users", "duration": "7 days before flag removal", "gate": "stable, schedule cleanup"},
        ]
    elif flag_type == "experiment":
        stages = [
            {"stage": "Control setup", "percentage": 0, "audience": "none", "duration": "1 day", "gate": "metrics pipeline verified"},
            {"stage": "Experiment", "percentage": 50, "audience": "random 50% (treatment vs control)", "duration": "2-4 weeks", "gate": "statistical significance reached"},
            {"stage": "Decision", "percentage": "0 or 100", "audience": "based on results", "duration": "1 day", "gate": "team decision logged"},
        ]
    print(json.dumps({"flag": flag_name, "type": flag_type, "stages": stages}, indent=2))

generate_rollout_plan("new-checkout-flow", "release", 50000)
```

#### Step 3: Set up monitoring checkpoints

```bash
# Verify metrics exist for the flag (Datadog example)
curl -s "https://api.datadoghq.com/api/v1/query?query=avg:app.feature_flag.evaluation{flag_name:new-checkout-flow}" \
  -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY"

# Check error rates segmented by flag state (Prometheus/Grafana)
# PromQL: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])
#   filtered by: feature_flag="new-checkout-flow", flag_state="enabled"
```

#### Step 4: Document the expiry contract

Every flag should have an owner and a kill date.

```
## Lifecycle Plan: [flag-name]

**Type:** Release toggle
**Owner:** @engineer-name
**Created:** YYYY-MM-DD
**Expected full rollout:** YYYY-MM-DD
**Hard expiry (must remove by):** YYYY-MM-DD (created + 60 days)

### Rollout Schedule
| Stage | % | Audience | Duration | Gate Criteria |
|-------|---|----------|----------|---------------|
| Internal | 0% (allowlist) | Employees | 2-3 days | No P0/P1 |
| Canary | 5% | Random | 3-5 days | Error < +0.1% |
| Broad | 50% | Random | 3 days | p99 within SLO |
| Full | 100% | All | 7 days | Schedule removal |

### Rollback trigger
- Error rate exceeds baseline by > 0.5%
- p99 latency exceeds SLO
- Any P0 incident attributed to this change

### Cleanup deadline
Flag must be removed within 14 days of reaching 100%. If not removed by [hard expiry], it enters the stale backlog and accrues toggle debt.
```
