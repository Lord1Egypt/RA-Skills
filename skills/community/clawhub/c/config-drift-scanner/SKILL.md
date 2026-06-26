---
name: config-drift-scanner
description: Detect configuration drift across environments (dev, staging, production). Compare config files, environment variables, feature flags, and secrets across deployments to find dangerous inconsistencies.
---

# Config Drift Scanner

Find configuration differences across your environments before they cause incidents. Compare config files, environment variables, feature flags, database settings, and runtime parameters between dev/staging/production — catching the "works on my machine" problems that slip past code review.

Use when: "compare configs between environments", "find config drift", "why does staging work but prod doesn't", "audit environment parity", "check env vars across deploys", or after an incident caused by config mismatch.

## Commands

### 1. `scan` — Detect Drift Across Environments

#### Step 1: Discover Configuration Sources

```bash
# Find config files in the project
find . -maxdepth 4 \( \
  -name "*.env" -o -name "*.env.*" -o \
  -name "*.config.*" -o -name "config.yaml" -o -name "config.json" -o \
  -name "*.toml" -o -name "settings.*" -o \
  -name "docker-compose*.yml" -o -name "docker-compose*.yaml" -o \
  -name "values*.yaml" -o -name "*.tfvars" \
  \) -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null

# Find environment variable references in code
rg "process\.env\.|os\.environ|os\.getenv|ENV\[|System\.getenv" \
  --type-not binary -g '!node_modules' -g '!vendor' --stats 2>&1 | tail -5
```

#### Step 2: Extract Config from Each Environment

For Kubernetes:
```bash
# ConfigMaps
for env in dev staging prod; do
  kubectl get configmaps -n "$env" -o json | python3 -c "
import json, sys
cms = json.load(sys.stdin)['items']
for cm in cms:
    name = cm['metadata']['name']
    for k, v in cm.get('data', {}).items():
        print(f'{name}.{k}={v}')
" > "/tmp/config-$env.txt"
done
```

For .env files:
```bash
# Compare .env files across environments
for f in .env.development .env.staging .env.production; do
  if [[ -f "$f" ]]; then
    echo "=== $f ==="
    grep -v '^#' "$f" | grep -v '^$' | sort
  fi
done
```

For Terraform:
```bash
# Compare tfvars across environments
for f in terraform/environments/*/terraform.tfvars; do
  echo "=== $f ==="
  cat "$f"
done
```

#### Step 3: Diff and Classify

Compare each key across environments and classify differences:

**🔴 Dangerous Drift (same key, unexpected difference):**
- Database connection strings pointing to wrong environment
- API keys that should be environment-specific but are shared
- Feature flags enabled in prod but disabled in staging (testing gap)
- Timeout values that differ without documented reason
- Memory/CPU limits that are lower in prod than staging

**🟡 Expected Drift (different by design):**
- Database URLs (each env has its own DB)
- API endpoints (staging.api.com vs api.com)
- Log levels (DEBUG in dev, INFO in prod)
- Replica counts (1 in dev, 3 in prod)

**🟢 Missing in Environment (potential problem):**
- Env var exists in prod but not staging → can't test that code path
- Config key exists in staging but not prod → forgot to add on deploy

#### Step 4: Generate Report

```markdown
# Configuration Drift Report

## Environments Compared: dev ↔ staging ↔ production

## 🔴 Dangerous Drift (3 found)
1. `DATABASE_POOL_SIZE`: dev=5, staging=10, **prod=5**
   → Prod should be ≥ staging. Likely copy-paste from dev config.

2. `FEATURE_NEW_CHECKOUT`: dev=true, staging=true, **prod=false**
   → Feature tested in staging but not enabled in prod. Intentional? If so, document.

3. `REDIS_TIMEOUT_MS`: dev=5000, **staging=500**, prod=5000
   → Staging has 10× shorter timeout. Will mask timeout bugs in staging tests.

## 🟡 Expected Drift (8 found)
- DATABASE_URL: different per environment ✅
- LOG_LEVEL: debug/info/warn ✅
- API_BASE_URL: per-environment ✅

## 🟢 Missing Variables (2 found)
- `SENTRY_DSN`: exists in prod, missing in staging → errors not tracked in staging
- `RATE_LIMIT_RPS`: exists in prod (100), missing in dev/staging → no rate limit testing

## Recommendations
1. Add SENTRY_DSN to staging for error visibility
2. Fix DATABASE_POOL_SIZE in prod (should be ≥ staging value)
3. Document why FEATURE_NEW_CHECKOUT differs between staging and prod
```

### 2. `watch` — Continuous Drift Monitoring

Set up a CI check that runs on every config change:

```yaml
# GitHub Actions
name: Config Drift Check
on:
  push:
    paths:
      - '**/*.env*'
      - '**/config.*'
      - '**/values*.yaml'
      - '**/*.tfvars'
jobs:
  drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check for drift
        run: |
          # Compare all env files and flag dangerous differences
          diff <(grep -v '^#' .env.staging | sort) <(grep -v '^#' .env.production | sort) || true
```

### 3. `template` — Generate Config Parity Checklist

For a new environment setup, generate a checklist of all config keys that need to be set, with:
- Required vs optional
- Expected value ranges
- Whether the value should differ or match other environments
- Where to get the value (secrets manager, team lead, auto-generated)

### 4. `secrets-check` — Verify Secret Rotation

Cross-reference config with secrets management:
- Which secrets are hardcoded vs pulled from vault/secrets manager?
- When were secrets last rotated?
- Are any secrets shared across environments (bad practice)?
- Are test/dev credentials accidentally in prod config?
