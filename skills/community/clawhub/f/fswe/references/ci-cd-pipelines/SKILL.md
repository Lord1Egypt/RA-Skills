# CI/CD Pipelines

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| language | string | en | en, id |
| depth | string | standard | quick, standard, deep |
| platform | string | github | github, gitlab |

## Checklist

### Pipeline Design
- [ ] Fast feedback — lint + typecheck + unit tests first
- [ ] Parallelize independent jobs
- [ ] Cache dependencies between runs
- [ ] Use matrix builds for multi-version testing
- [ ] Separate build → test → deploy stages
- [ ] Block deploy on test failure

### GitHub Actions
```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
      - run: bun run lint
      - run: bun run typecheck

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
      - run: bun test --coverage

  deploy:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/deploy.sh
    environment: production
```

### Deployment Strategies
| Strategy | Risk | Downtime | Rollback Speed |
|----------|------|----------|----------------|
| Rolling | Low | None | Medium |
| Blue-Green | Low | None | Fast |
| Canary | Medium | None | Fast |
| Big Bang | High | Yes | Slow |

### Secrets Management
- [ ] Never hardcode secrets in workflow files
- [ ] Use platform secrets (GitHub Secrets, GitLab CI Variables)
- [ ] Rotate secrets regularly
- [ ] Use environment protection rules for production deploys
- [ ] Audit secret access

### Pipeline Security
- [ ] Pin action versions (`actions/checkout@v4`, not `@main`)
- [ ] Use `--frozen-lockfile` for dependency installs
- [ ] Run SAST scans (Semgrep, CodeQL)
- [ ] Scan container images before push
- [ ] Use OIDC for cloud provider auth (no static keys)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No caching | Use `actions/cache` or built-in cache |
| Sequential jobs | Parallelize independent steps |
| Secrets in logs | Use `::add-mask::` for sensitive output |
| No deploy protection | Use environment protection rules |
| `npm install` in CI | Use `npm ci` or `bun install --frozen-lockfile` |
