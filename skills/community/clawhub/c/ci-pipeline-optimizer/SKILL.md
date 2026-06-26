---
name: ci-pipeline-optimizer
description: Analyze CI/CD pipelines (GitHub Actions, GitLab CI, CircleCI) and suggest optimizations — caching strategies, parallelization, step elimination, Docker layer optimization, matrix builds, and conditional execution to reduce build times.
---

# CI Pipeline Optimizer

Make CI/CD pipelines faster and cheaper. Analyzes workflow files to find bottlenecks, missing caches, serial steps that can run in parallel, unnecessary work, and oversized Docker builds.

Use when: "CI is too slow", "optimize our pipeline", "reduce build time", "CI costs too much", "speed up GitHub Actions", "pipeline taking 20 minutes", or doing CI/CD maintenance.

## Commands

### 1. `analyze` — Full Pipeline Analysis

Scan all CI configuration files and identify optimization opportunities.

#### Step 1: Discover Pipeline Config

```bash
echo "=== CI Pipeline Discovery ==="

# GitHub Actions
if [ -d ".github/workflows" ]; then
  echo "Platform: GitHub Actions"
  ls -la .github/workflows/*.yml .github/workflows/*.yaml 2>/dev/null
fi

# GitLab CI
[ -f ".gitlab-ci.yml" ] && echo "Platform: GitLab CI"

# CircleCI
[ -f ".circleci/config.yml" ] && echo "Platform: CircleCI"

# Jenkins
[ -f "Jenkinsfile" ] && echo "Platform: Jenkins"

# Bitbucket
[ -f "bitbucket-pipelines.yml" ] && echo "Platform: Bitbucket Pipelines"

# Azure DevOps
[ -f "azure-pipelines.yml" ] && echo "Platform: Azure DevOps"
```

#### Step 2: Caching Analysis

```bash
echo ""
echo "=== Caching Analysis ==="

# GitHub Actions: check for cache steps
if [ -d ".github/workflows" ]; then
  echo "--- Cache Usage ---"
  rg -n "actions/cache|cache:" .github/workflows/ 2>/dev/null

  # Check if node_modules is cached
  HAS_NODE_CACHE=$(rg -c "node_modules|npm-cache|yarn-cache|pnpm-store" .github/workflows/ 2>/dev/null | awk -F: '{s+=$2} END {print s+0}')
  [ -f "package.json" ] && [ "$HAS_NODE_CACHE" -eq 0 ] && echo "⚠️  MISSING: Node.js dependency cache"

  # Check if pip cache exists
  HAS_PIP_CACHE=$(rg -c "pip-cache\|pip.*cache\|~/.cache/pip" .github/workflows/ 2>/dev/null | awk -F: '{s+=$2} END {print s+0}')
  [ -f "requirements.txt" ] && [ "$HAS_PIP_CACHE" -eq 0 ] && echo "⚠️  MISSING: Python pip cache"

  # Check for Docker layer caching
  HAS_DOCKER_CACHE=$(rg -c "docker/build-push-action.*cache|buildx.*cache|docker-layer-caching" .github/workflows/ 2>/dev/null | awk -F: '{s+=$2} END {print s+0}')
  HAS_DOCKER=$(rg -c "docker build\|docker-compose\|docker/build-push" .github/workflows/ 2>/dev/null | awk -F: '{s+=$2} END {print s+0}')
  [ "$HAS_DOCKER" -gt 0 ] && [ "$HAS_DOCKER_CACHE" -eq 0 ] && echo "⚠️  MISSING: Docker layer cache"

  # Check for build output caching (turbo, nx)
  [ -f "turbo.json" ] && ! rg -q "turborepo-cache\|turbo.*cache" .github/workflows/ 2>/dev/null && echo "⚠️  MISSING: Turborepo remote cache"
fi

# GitLab CI
if [ -f ".gitlab-ci.yml" ]; then
  rg -n "cache:" .gitlab-ci.yml 2>/dev/null
  HAS_CACHE=$(rg -c "cache:" .gitlab-ci.yml 2>/dev/null || echo "0")
  [ "$HAS_CACHE" -eq 0 ] && echo "⚠️  No cache configuration in .gitlab-ci.yml"
fi
```

#### Step 3: Parallelization Analysis

```bash
echo ""
echo "=== Parallelization Opportunities ==="

if [ -d ".github/workflows" ]; then
  # Find workflows with sequential jobs that could be parallel
  for wf in .github/workflows/*.yml .github/workflows/*.yaml; do
    [ -f "$wf" ] || continue
    echo "--- $(basename $wf) ---"

    # Check for needs: (job dependencies)
    JOBS=$(rg -c "^\s{2}\w+:" "$wf" 2>/dev/null || echo "0")
    NEEDS=$(rg -c "needs:" "$wf" 2>/dev/null || echo "0")

    echo "  Jobs: $JOBS, Dependencies (needs): $NEEDS"

    if [ "$JOBS" -gt 1 ] && [ "$NEEDS" -eq 0 ]; then
      echo "  ✅ Jobs run in parallel (no dependencies)"
    elif [ "$NEEDS" -gt 0 ]; then
      echo "  Check if some 'needs' can be removed for parallel execution:"
      rg -n "needs:" "$wf" 2>/dev/null | head -5
    fi

    # Check for matrix strategy
    HAS_MATRIX=$(rg -c "matrix:" "$wf" 2>/dev/null || echo "0")
    [ "$HAS_MATRIX" -gt 0 ] && echo "  ✅ Uses matrix strategy"

    # Check for steps that could be split into parallel jobs
    STEPS=$(rg -c "^\s*- (name|run|uses):" "$wf" 2>/dev/null || echo "0")
    [ "$STEPS" -gt 15 ] && echo "  ⚠️  $STEPS steps in a single job — consider splitting into parallel jobs"
  done
fi
```

#### Step 4: Unnecessary Work Detection

```bash
echo ""
echo "=== Unnecessary Work ==="

if [ -d ".github/workflows" ]; then
  for wf in .github/workflows/*.yml .github/workflows/*.yaml; do
    [ -f "$wf" ] || continue

    # Check for path filters (run only on relevant changes)
    HAS_PATHS=$(rg -c "paths:" "$wf" 2>/dev/null || echo "0")
    [ "$HAS_PATHS" -eq 0 ] && echo "⚠️  $(basename $wf): No path filters — runs on ALL file changes"

    # Check for conditional execution
    HAS_IF=$(rg -c "if:" "$wf" 2>/dev/null || echo "0")
    echo "  $(basename $wf): $HAS_IF conditional steps"

    # Full checkout vs shallow
    FULL_CHECKOUT=$(rg -c "fetch-depth: 0" "$wf" 2>/dev/null || echo "0")
    [ "$FULL_CHECKOUT" -gt 0 ] && echo "  ⚠️  Full git history checkout (fetch-depth: 0) — needed?"

    # Multiple npm install steps
    NPM_INSTALLS=$(rg -c "npm install\|npm ci\|yarn install\|pnpm install" "$wf" 2>/dev/null || echo "0")
    [ "$NPM_INSTALLS" -gt 1 ] && echo "  ⚠️  $NPM_INSTALLS separate install steps — consolidate or cache"
  done
fi
```

#### Step 5: Docker Optimization

```bash
echo ""
echo "=== Docker Build Optimization ==="

find . -name "Dockerfile" -not -path '*/node_modules/*' 2>/dev/null | while read df; do
  echo "--- $df ---"
  LINES=$(wc -l < "$df")
  echo "  Lines: $LINES"

  # Multi-stage build?
  STAGES=$(grep -c "^FROM " "$df")
  [ "$STAGES" -gt 1 ] && echo "  ✅ Multi-stage build ($STAGES stages)" || echo "  ⚠️  Single-stage build — add multi-stage to reduce image size"

  # COPY before package install (cache-busting)
  COPY_ALL=$(grep -n "COPY \. \.\|COPY \.\/ " "$df" | head -1 | cut -d: -f1)
  RUN_INSTALL=$(grep -n "npm install\|npm ci\|pip install\|go build" "$df" | head -1 | cut -d: -f1)
  if [ -n "$COPY_ALL" ] && [ -n "$RUN_INSTALL" ] && [ "$COPY_ALL" -lt "$RUN_INSTALL" ]; then
    echo "  ⚠️  COPY . before install — busts Docker cache on every file change"
    echo "     Fix: COPY package*.json first, then install, then COPY rest"
  fi

  # .dockerignore exists?
  DIR=$(dirname "$df")
  [ -f "$DIR/.dockerignore" ] || [ -f ".dockerignore" ] || echo "  ⚠️  No .dockerignore — sending unnecessary files to Docker daemon"

  # Large base image
  BASE=$(grep "^FROM " "$df" | tail -1 | awk '{print $2}')
  echo "$BASE" | grep -qE "^(ubuntu|debian|centos|node:|python:)" && \
    ! echo "$BASE" | grep -qE "(slim|alpine|distroless)" && \
    echo "  ⚠️  Large base image ($BASE) — consider slim/alpine/distroless variant"
done
```

### 2. `cache` — Caching Recommendations

Generate specific caching configuration for the project:

```yaml
# For GitHub Actions + Node.js
- uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      node_modules
    key: node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: node-
```

Recommendations per ecosystem:
- **Node.js**: Cache `node_modules` or `~/.npm` keyed on lockfile hash
- **Python**: Cache `~/.cache/pip` keyed on `requirements.txt` hash
- **Go**: Cache `~/go/pkg/mod` keyed on `go.sum` hash
- **Rust**: Cache `~/.cargo` and `target/` keyed on `Cargo.lock`
- **Docker**: Use BuildKit cache mount or `docker/build-push-action` cache

### 3. `timeline` — Build Timeline Visualization

Parse CI logs or config to estimate job duration:

```
Pipeline: build-and-test.yml
Total estimated time: ~12 min (serial) → ~6 min (optimized)

[lint]        ████░░░░░░░░  2 min
[test]        ██████████░░  5 min  (needs: lint)
[build]       ████████░░░░  4 min  (needs: lint)
[deploy]      ██░░░░░░░░░░  1 min  (needs: test, build)

Optimization: run [test] and [build] in parallel → save 4 min
```

### 4. `suggest` — Generate Optimized Pipeline

Produce a rewritten pipeline with all optimizations applied:
- Added caches
- Parallelized independent jobs
- Path filters added
- Docker build optimized
- Conditional execution for skip-on-docs-only changes

## Output Formats

- **text** (default): Human-readable analysis with suggestions
- **json**: `{platform, workflows: [{name, jobs, steps, caches, issues: []}], optimizations: [], estimated_savings: ""}`
- **markdown**: Report for PRs or wiki documentation
- **yaml**: Ready-to-use optimized workflow configuration

## Notes

- Supports GitHub Actions, GitLab CI, CircleCI, and Jenkinsfile analysis
- Does not access CI logs or run history — analyzes config files statically
- Time estimates are heuristic (based on common operation durations)
- Caching recommendations are framework-aware and use current best practices
- Docker optimization checks apply to all Dockerfiles in the project
- For monorepos, suggests path-filtered triggers and affected-only testing
