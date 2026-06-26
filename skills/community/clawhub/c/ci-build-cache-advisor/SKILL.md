---
name: ci-build-cache-advisor
description: Optimize CI/CD build caching across GitHub Actions, GitLab CI, CircleCI, and Jenkins — analyze cache hit rates, recommend cache keys, and reduce build times.
metadata:
  tags: ["ci-cd", "caching", "build", "performance", "devops"]
---

# CI Build Cache Advisor

Optimize CI/CD build caching strategies across GitHub Actions, GitLab CI, CircleCI, and Jenkins. Analyze cache configurations, recommend cache keys, identify cache misses, and reduce build times by maximizing cache hit rates.

## Usage

```
"Optimize caching in my CI pipeline"
"Why are my builds not using cache?"
"Design cache keys for my monorepo CI"
"Reduce my CI build time"
```

## How It Works

### 1. CI Platform Detection

```bash
ls .github/workflows/ 2>/dev/null && echo "GitHub Actions"
ls .gitlab-ci.yml 2>/dev/null && echo "GitLab CI"
ls .circleci/config.yml 2>/dev/null && echo "CircleCI"
ls Jenkinsfile 2>/dev/null && echo "Jenkins"
```

### 2. Cache Analysis

**What should be cached:**
- Package manager dependencies (node_modules, .pip, .cargo, .gradle)
- Build artifacts (compiled code, generated assets)
- Docker layers
- Test fixtures and snapshots
- Linter and type checker caches

**Cache key strategy:**
- Primary key: hash of lockfile (package-lock.json, Cargo.lock)
- Restore key: platform + branch fallback
- Matrix-aware: different caches per OS/Node version/Python version
- Monorepo: workspace-specific caches

### 3. Common Issues

- **Cache too broad**: Single cache for entire node_modules invalidated by any dep change
- **Cache too narrow**: Cache key includes commit SHA (never hits)
- **Missing restore keys**: No fallback when primary key misses
- **Cache pollution**: Dev dependencies cached for production builds
- **Stale cache**: Cache never expires, using outdated artifacts
- **Cache size limit**: Exceeding platform limits (GitHub: 10GB, GitLab: varies)

### 4. Recommendations by Platform

**GitHub Actions:**
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-
```

**GitLab CI:**
```yaml
cache:
  key:
    files: [package-lock.json]
    prefix: $CI_JOB_NAME
  paths: [node_modules/]
  policy: pull-push
```

### 5. Advanced Strategies

- **Turbo/Nx remote caching**: Share build cache across CI and developers
- **Docker layer caching**: BuildKit cache mounts, registry-backed cache
- **Gradle build cache**: Remote cache server for team-wide sharing
- **ccache/sccache**: C/C++/Rust compilation caching

## Output

```
## CI Cache Optimization

**Platform:** GitHub Actions | **Workflows:** 3

### Current Cache Usage
| Workflow | Cache Configured | Hit Rate | Build Time |
|----------|-----------------|----------|------------|
| CI | Yes (npm) | 67% | 8m 30s |
| Deploy | No | 0% | 12m 15s |
| Release | Partial | 45% | 15m |

### Recommendations
1. **Add npm cache to Deploy workflow** — saves ~3 min/run
2. **Fix CI cache key** — includes branch name (low hit rate on PRs)
   → Remove branch, use lockfile hash only
3. **Add Docker layer caching to Release** — saves ~5 min
4. **Add TypeScript build cache** — `tsBuildInfoFile` not cached

### Projected Improvement
- CI: 8m 30s → 3m 45s (56% faster)
- Deploy: 12m 15s → 7m (43% faster)
- Release: 15m → 8m (47% faster)
- Monthly minutes saved: ~2,400 (~$19)
```
