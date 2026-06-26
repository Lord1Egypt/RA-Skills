---
name: environment-promoter
description: Manage environment promotions (dev → staging → prod) — compare configs between environments, detect drift, generate promotion plans, validate prerequisites, and execute safe promotions with rollback support.
---

# Environment Promoter

Safely promote deployments and configurations across environments. Detects config drift, validates promotion prerequisites, generates diff reports, and provides rollback plans.

Use when: "promote to staging", "compare environments", "check config drift", "is staging in sync with dev", "deploy to production checklist", "environment diff", or managing multi-environment deployments.

## Commands

### 1. `compare` — Compare Two Environments

Diff configuration, environment variables, and deployment state between environments.

#### Environment Variable Comparison

```bash
# Compare .env files across environments
ENV_SOURCE="${1:-.env.development}"
ENV_TARGET="${2:-.env.staging}"

if [ ! -f "$ENV_SOURCE" ] || [ ! -f "$ENV_TARGET" ]; then
  echo "Looking for environment files..."
  find . -maxdepth 3 -name ".env*" -not -path '*/node_modules/*' 2>/dev/null | sort
fi

python3 -c "
import sys

def parse_env(path):
    vars = {}
    try:
        for line in open(path):
            line = line.strip()
            if not line or line.startswith('#'): continue
            if '=' in line:
                key, val = line.split('=', 1)
                vars[key.strip()] = val.strip().strip('\"').strip(\"'\")
    except FileNotFoundError:
        print(f'File not found: {path}')
    return vars

source = parse_env('$ENV_SOURCE')
target = parse_env('$ENV_TARGET')

all_keys = sorted(set(source.keys()) | set(target.keys()))

added = [k for k in all_keys if k in source and k not in target]
removed = [k for k in all_keys if k not in source and k in target]
changed = [k for k in all_keys if k in source and k in target and source[k] != target[k]]
same = [k for k in all_keys if k in source and k in target and source[k] == target[k]]

# Mask sensitive values
def mask(val):
    sensitive = ['KEY', 'SECRET', 'TOKEN', 'PASSWORD', 'PASS', 'AUTH', 'CREDENTIAL']
    if any(s in val.upper() for s in sensitive) and len(val) > 4:
        return val[:2] + '***' + val[-2:]
    return val

print(f'Comparing: $ENV_SOURCE → $ENV_TARGET')
print(f'Total keys: {len(all_keys)} | Same: {len(same)} | Changed: {len(changed)} | Added: {len(added)} | Missing in target: {len(removed)}')
print()

if added:
    print('🟢 In source, missing in target (need to add):')
    for k in added:
        print(f'  + {k}={mask(source[k])}')
    print()

if removed:
    print('🔴 In target, missing in source (may need removal):')
    for k in removed:
        print(f'  - {k}={mask(target[k])}')
    print()

if changed:
    print('🟡 Different values:')
    for k in changed:
        print(f'  ~ {k}:')
        print(f'    source: {mask(source[k])}')
        print(f'    target: {mask(target[k])}')
" 2>/dev/null
```

#### Deployment Config Comparison

```bash
# Compare Kubernetes manifests
if [ -d "k8s" ] || [ -d "kubernetes" ] || [ -d "deploy" ]; then
  DEPLOY_DIR=$(ls -d k8s kubernetes deploy 2>/dev/null | head -1)
  echo "=== Kubernetes Config Diff ==="

  for env in dev staging prod production; do
    if [ -d "$DEPLOY_DIR/$env" ] || [ -d "$DEPLOY_DIR/overlays/$env" ]; then
      echo "Found environment: $env"
    fi
  done

  # Compare image versions
  rg -n "image:" "$DEPLOY_DIR/" 2>/dev/null | sort
fi

# Compare docker-compose files
for env in development staging production; do
  if [ -f "docker-compose.$env.yml" ] || [ -f "docker-compose.$env.yaml" ]; then
    echo "Found: docker-compose.$env.yml"
  fi
done

# Compare Terraform workspaces
if [ -d "terraform" ] || [ -f "main.tf" ]; then
  echo "=== Terraform Environments ==="
  find . -name "*.tfvars" -not -path '*/\.terraform/*' 2>/dev/null | sort
fi
```

### 2. `drift` — Detect Configuration Drift

Check if environments have diverged from their expected state.

```bash
echo "=== Drift Detection ==="

# Compare container image versions across environments
echo "--- Image Versions ---"
for env_file in $(find . -name "*.yml" -o -name "*.yaml" | grep -E "(dev|stag|prod|deploy)" | grep -v node_modules); do
  IMAGES=$(grep -oP 'image:\s*\K\S+' "$env_file" 2>/dev/null)
  if [ -n "$IMAGES" ]; then
    echo "$env_file:"
    echo "$IMAGES" | while read img; do echo "  $img"; done
  fi
done

# Compare replicas/resources across environments
echo "--- Resource Drift ---"
for env_file in $(find . -name "*.yml" -o -name "*.yaml" | grep -E "(dev|stag|prod|deploy)" | grep -v node_modules); do
  REPLICAS=$(grep -oP 'replicas:\s*\K\d+' "$env_file" 2>/dev/null)
  if [ -n "$REPLICAS" ]; then
    echo "$env_file: replicas=$REPLICAS"
  fi
done

# Check git tags — what version is deployed where
echo "--- Deployed Versions ---"
git tag -l "staging-*" 2>/dev/null | sort -V | tail -3
git tag -l "production-*" 2>/dev/null | sort -V | tail -3
```

Analyze drift with AI reasoning: which differences are intentional (environment-specific settings) vs accidental (forgot to promote a config change).

### 3. `plan` — Generate Promotion Plan

Create a step-by-step plan to promote from source to target environment.

```markdown
# Promotion Plan: staging → production
Generated: [date]

## Prerequisites
- [ ] All tests pass on staging
- [ ] QA sign-off received
- [ ] No open P0/P1 bugs
- [ ] Database migrations compatible
- [ ] Feature flags configured
- [ ] Rollback plan documented

## Changes to Promote
1. **Config changes** (3 vars):
   - Add: NEW_FEATURE_ENABLED=true
   - Update: API_RATE_LIMIT 100→200
   - Update: LOG_LEVEL debug→info

2. **Image version**: v1.4.2 → v1.5.0

3. **Infrastructure changes**:
   - Replicas: 2 → 3
   - Memory limit: 512Mi → 1Gi

## Promotion Steps
1. Create database backup
2. Run database migrations (if any)
3. Update environment variables
4. Deploy new image version
5. Verify health check endpoints
6. Monitor error rates for 15 minutes
7. If OK → mark promotion complete
8. If errors → execute rollback plan

## Rollback Plan
1. Revert image to v1.4.2
2. Revert environment variables
3. Verify rollback health
```

### 4. `validate` — Pre-Promotion Validation

Check if the target environment is ready to receive a promotion.

```bash
echo "=== Pre-Promotion Validation ==="

# Check if source environment is healthy
echo "--- Source Health ---"
# Ping health endpoints from env config
rg -o "https?://[a-zA-Z0-9._:/-]+" .env.staging 2>/dev/null | while read url; do
  if echo "$url" | grep -qE "(health|status|ready)"; then
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$url" 2>/dev/null)
    echo "$url → $STATUS"
  fi
done

# Check for pending migrations
echo "--- Migrations ---"
find . -path "*/migrations/*" -name "*.sql" -newer .last-promotion 2>/dev/null | head -10
find . -path "*/migrations/*" -name "*.py" -newer .last-promotion 2>/dev/null | head -10

# Check for feature flag dependencies
echo "--- Feature Flags ---"
rg -n "feature_flag\|featureFlag\|FEATURE_\|isEnabled\|isFeatureOn" \
  -g '!node_modules' -g '!vendor' -g '!dist' -g '!*.test.*' \
  --type-not binary 2>/dev/null | head -15

# Check git state
echo "--- Git State ---"
BRANCH=$(git branch --show-current 2>/dev/null)
echo "Current branch: $BRANCH"
UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l)
echo "Uncommitted changes: $UNCOMMITTED"
```

### 5. `history` — Promotion History

Track promotions over time:

```bash
# Git tags as promotion markers
echo "=== Promotion History ==="
for env in staging production; do
  echo "--- $env ---"
  git tag -l "${env}-*" --sort=-version:refname 2>/dev/null | head -10 | while read tag; do
    DATE=$(git log -1 --format="%ai" "$tag" 2>/dev/null)
    MSG=$(git log -1 --format="%s" "$tag" 2>/dev/null)
    echo "  $tag ($DATE) — $MSG"
  done
done

# Recent deploys from CI
if command -v gh &>/dev/null; then
  echo "--- GitHub Deployments ---"
  gh api repos/:owner/:repo/deployments --jq '.[0:5] | .[] | "\(.environment) — \(.created_at) — \(.description // "no description")"' 2>/dev/null
fi
```

### 6. `matrix` — Environment Matrix

Show all environments and their current state:

```markdown
| Environment | Version | Last Deploy | Status | Config Vars |
|------------|---------|-------------|--------|-------------|
| development | v1.5.1-dev | 2h ago | ✅ healthy | 42 vars |
| staging | v1.5.0 | 2d ago | ✅ healthy | 38 vars |
| production | v1.4.2 | 5d ago | ✅ healthy | 35 vars |
```

Detect environments from:
- `.env.*` files
- `docker-compose.*.yml` files
- `k8s/overlays/*/` or `deploy/*/` directories
- Terraform workspace/tfvars files
- Git tags with environment prefixes
- CI/CD environment configurations

## Output Formats

- **text** (default): Human-readable diff with color indicators
- **json**: `{source, target, added: [], removed: [], changed: [], drift: [], plan: {}}`
- **markdown**: Report suitable for PR comments or wiki

## Notes

- Masks sensitive values (passwords, tokens, keys) in all output
- Does not execute deployments — generates plans for human review
- Works with any deployment tool (K8s, Docker, Terraform, Heroku, etc.)
- Environment detection is convention-based — adapts to common patterns
- For automated promotions, use the `plan` output as input to your deployment tool
- Promotion history relies on git tags — tag your deployments for best results
