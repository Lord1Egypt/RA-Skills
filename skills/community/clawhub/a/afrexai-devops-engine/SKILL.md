---
name: afrexai-devops-engine
description: Complete DevOps & Platform Engineering system. CI/CD pipelines, infrastructure as code, container orchestration, observability, incident response, and SRE practices — all platforms, all clouds.
metadata: {"clawdbot":{"emoji":"🔧","os":["linux","darwin","win32"]}}
---

# DevOps & Platform Engineering Engine

Complete system for building, deploying, operating, and observing production software. Covers the entire DevOps lifecycle — not just CI/CD, not just one cloud.

## Phase 1: Repository & Branch Strategy

### Git Flow Decision Matrix

| Team Size | Release Cadence | Strategy | Branches |
|-----------|----------------|----------|----------|
| 1-3 | Continuous | Trunk-based | main + short-lived feature/ |
| 4-15 | Weekly/biweekly | GitHub Flow | main + feature/ + PR |
| 15+ | Scheduled releases | Git Flow | main + develop + feature/ + release/ + hotfix/ |
| Regulated | Audited releases | Git Flow + tags | Above + signed tags + audit trail |

### Branch Protection Rules (Apply These)

```yaml
# branch-protection.yml — document your rules
main:
  required_reviews: 2
  dismiss_stale_reviews: true
  require_codeowners: true
  require_status_checks:
    - ci/test
    - ci/lint
    - ci/security
  require_linear_history: true  # No merge commits
  restrict_pushes: true         # Only via PR
  require_signed_commits: false # Enable for regulated

develop:
  required_reviews: 1
  require_status_checks:
    - ci/test
```

### Commit Convention

Format: `<type>(<scope>): <description>`

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`

Breaking changes: `feat!: remove legacy API` or footer `BREAKING CHANGE: description`

Enforce with commitlint + husky (Node) or pre-commit hooks.

## Phase 2: CI/CD Pipeline Architecture

### Pipeline Design Principles

1. **Build once, deploy everywhere** — same artifact through dev→staging→prod
2. **Fail fast** — cheapest checks first (lint→unit→integration→e2e)
3. **Hermetic builds** — no external state, reproducible from commit SHA
4. **Immutable artifacts** — never modify after build; tag with git SHA
5. **Parallelise independent stages** — test/lint/security scan simultaneously

### Universal Pipeline Template

```yaml
# pipeline-stages.yml — adapt to your CI system
stages:
  # Stage 1: Quality Gate (parallel, <2 min)
  lint:
    run: lint
    parallel: true
    timeout: 2m
  typecheck:
    run: tsc --noEmit
    parallel: true
    timeout: 2m
  security_scan:
    run: trivy, snyk, or semgrep
    parallel: true
    timeout: 3m

  # Stage 2: Test (parallel by type, <10 min)
  unit_tests:
    run: test --unit
    parallel: true
    coverage_threshold: 80%
    timeout: 5m
  integration_tests:
    run: test --integration
    parallel: true
    needs: [database_service]
    timeout: 10m

  # Stage 3: Build (<5 min)
  build:
    needs: [lint, typecheck, unit_tests]
    outputs: [docker_image, release_artifact]
    tag: "${GIT_SHA}"
    cache: [node_modules, .next/cache, target/]

  # Stage 4: Deploy Staging (auto)
  deploy_staging:
    needs: [build]
    environment: staging
    strategy: rolling
    smoke_test: true
    auto: true

  # Stage 5: E2E on Staging (<15 min)
  e2e_tests:
    needs: [deploy_staging]
    timeout: 15m
    retry: 1
    artifacts: [screenshots, videos]

  # Stage 6: Deploy Production (manual gate or auto)
  deploy_prod:
    needs: [e2e_tests]
    environment: production
    strategy: canary  # or blue-green
    approval: required  # manual gate
    rollback_on_failure: true
    monitoring_window: 15m
```

### CI Platform Cheat Sheet

| Feature | GitHub Actions | GitLab CI | CircleCI | Jenkins |
|---------|---------------|-----------|----------|---------|
| Config file | `.github/workflows/*.yml` | `.gitlab-ci.yml` | `.circleci/config.yml` | `Jenkinsfile` |
| Parallelism | `jobs.<id>` (automatic) | `stages` + `parallel` | `workflows` | `parallel` step |
| Caching | `actions/cache` | `cache:` key | `save_cache/restore_cache` | Stash/unstash |
| Secrets | Settings → Secrets | Settings → CI/CD → Variables | Project Settings → Env | Credentials plugin |
| Matrix builds | `strategy.matrix` | `parallel:matrix` | `matrix` in workflows | `matrix` in pipeline |
| Self-hosted | `runs-on: self-hosted` | GitLab Runner | `resource_class` | Default |
| OIDC/Keyless | `permissions: id-token: write` | `id_tokens:` | OIDC context | Plugin |

### Caching Strategy

```yaml
# Cache key patterns (ordered by specificity)
cache_keys:
  # Exact match first
  - "deps-{{ runner.os }}-{{ hashFiles('**/lockfile') }}"
  # Partial match fallback
  - "deps-{{ runner.os }}-"

# What to cache by stack
node: [node_modules, .next/cache, .turbo]
python: [.venv, .mypy_cache, .pytest_cache]
rust: [target/, ~/.cargo/registry]
go: [~/go/pkg/mod, ~/.cache/go-build]
docker: [/tmp/.buildx-cache]  # BuildKit layer cache
```

### GitHub Actions Specific Patterns

```yaml
# Reusable workflow (DRY across repos)
# .github/workflows/reusable-deploy.yml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      DEPLOY_KEY:
        required: true

# Caller workflow
jobs:
  deploy:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: production
    secrets: inherit
```

```yaml
# Path-based triggers (monorepo)
on:
  push:
    paths:
      - 'packages/api/**'
      - 'shared/**'
  # Skip CI for docs-only changes
  pull_request:
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

```yaml
# Concurrency (cancel in-progress on new push)
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## Phase 3: Container Strategy

### Dockerfile Best Practices

```dockerfile
# Multi-stage build template
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --production=false    # Install all deps for build
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS production
RUN addgroup -g 1001 app && adduser -u 1001 -G app -s /bin/sh -D app
WORKDIR /app
COPY --from=builder --chown=app:app /app/dist ./dist
COPY --from=builder --chown=app:app /app/node_modules ./node_modules
COPY --from=builder --chown=app:app /app/package.json ./

USER app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

### Image Size Reduction Checklist

- [ ] Use alpine or distroless base images
- [ ] Multi-stage builds (build deps not in final image)
- [ ] `.dockerignore` excludes: `.git`, `node_modules`, `*.md`, tests, docs
- [ ] Combine RUN commands (fewer layers)
- [ ] Clean package manager cache in same RUN (`rm -rf /var/cache/apk/*`)
- [ ] No dev dependencies in production stage
- [ ] Pin base image SHA: `FROM node:20-alpine@sha256:abc123...`

### Container Security Scan

```bash
# Trivy (recommended — free, fast)
trivy image myapp:latest --severity HIGH,CRITICAL
trivy fs . --security-checks vuln,secret,config

# Scan in CI before push
# Fail pipeline if CRITICAL vulnerabilities found
trivy image --exit-code 1 --severity CRITICAL myapp:${GIT_SHA}
```

### Docker Compose for Local Dev

```yaml
# docker-compose.yml — local development stack
services:
  app:
    build:
      context: .
      target: builder  # Use build stage for hot reload
    volumes:
      - .:/app
      - /app/node_modules  # Don't override node_modules
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/app
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
      timeout: 3s
      retries: 5

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

## Phase 4: Infrastructure as Code

### IaC Decision Matrix

| Tool | Best For | State | Language | Learning Curve |
|------|----------|-------|----------|----------------|
| Terraform/OpenTofu | Multi-cloud, cloud-agnostic | Remote (S3, GCS) | HCL | Medium |
| Pulumi | Devs who prefer real code | Remote | TS/Python/Go | Low (if you code) |
| AWS CDK | AWS-only shops | CloudFormation | TS/Python | Medium |
| Ansible | Config management, server setup | Stateless | YAML | Low |
| Helm | Kubernetes deployments | Tiller/OCI | YAML+Go templates | Medium |

### Terraform Project Structure

```
infrastructure/
├── modules/                    # Reusable components
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── ecs-service/
│   └── rds/
├── environments/
│   ├── dev/
│   │   ├── main.tf            # Calls modules with dev params
│   │   ├── terraform.tfvars
│   │   └── backend.tf         # Dev state bucket
│   ├── staging/
│   └── prod/
├── .terraform-version          # Pin terraform version
└── .tflint.hcl
```

### Terraform Safety Rules

1. **Always `plan` before `apply`** — review every change
2. **Remote state with locking** — S3 + DynamoDB or GCS + locking
3. **State never in git** — contains secrets (DB passwords, keys)
4. **Import existing resources** before managing them — don't recreate
5. **Use `prevent_destroy`** on critical resources (databases, S3 buckets)
6. **Tag everything** — `environment`, `team`, `cost-center`, `managed-by: terraform`
7. **`terraform fmt`** in CI — consistent formatting

```hcl
# backend.tf — remote state with locking
terraform {
  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "prod/main.tfstate"
    region         = "eu-west-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# Protect critical resources
resource "aws_rds_instance" "main" {
  # ...
  lifecycle {
    prevent_destroy = true
  }
}
```

### Environment Promotion Pattern

```
                    ┌──────────────────┐
  terraform plan ──►│  Review in PR    │
                    └────────┬─────────┘
                             │ merge
                    ┌────────▼─────────┐
  auto-apply ──────►│  Dev             │──► smoke tests
                    └────────┬─────────┘
                             │ promote
                    ┌────────▼─────────┐
  manual approve ──►│  Staging         │──► integration tests
                    └────────┬─────────┘
                             │ promote (manual gate)
                    ┌────────▼─────────┐
  manual approve ──►│  Production      │──► monitoring window
                    └──────────────────┘
```

## Phase 5: Kubernetes Operations

### K8s Resource Templates

```yaml
# deployment.yml — production-ready template
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
    version: "1.0.0"
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0    # Zero-downtime
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
        - name: myapp
          image: myregistry/myapp:abc123  # Git SHA tag
          ports:
            - containerPort: 3000
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 10
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: database-url
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
```

```yaml
# hpa.yml — autoscaling
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # 5 min cooldown
      policies:
        - type: Pods
          value: 1
          periodSeconds: 60  # Scale down 1 pod per minute max
```

### Helm Chart Checklist

- [ ] `values.yaml` with sensible defaults (works out of the box)
- [ ] Resource requests AND limits set
- [ ] Health/readiness probes defined
- [ ] PodDisruptionBudget (minAvailable: 1 or maxUnavailable: 25%)
- [ ] NetworkPolicy (deny all, allow specific)
- [ ] ServiceAccount (not default)
- [ ] Secrets via external-secrets-operator or sealed-secrets (not plain)
- [ ] `helm lint` and `helm template` in CI
- [ ] NOTES.txt with post-install instructions

### kubectl Cheat Sheet

```bash
# Debugging
kubectl get pods -l app=myapp -o wide          # Pod status + node
kubectl describe pod <pod>                      # Events, conditions
kubectl logs <pod> --tail=100 -f               # Stream logs
kubectl logs <pod> --previous                   # Crashed container logs
kubectl exec -it <pod> -- /bin/sh              # Shell into pod
kubectl top pods -l app=myapp                  # Resource usage

# Rollouts
kubectl rollout status deployment/myapp        # Watch rollout
kubectl rollout history deployment/myapp       # Revision history
kubectl rollout undo deployment/myapp          # Rollback to previous
kubectl rollout undo deployment/myapp --to-revision=3  # Specific

# Scaling
kubectl scale deployment/myapp --replicas=5    # Manual scale
kubectl autoscale deployment/myapp --min=3 --max=10 --cpu-percent=70

# Context management
kubectl config get-contexts                     # List clusters
kubectl config use-context prod-cluster         # Switch
kubectl config set-context --current --namespace=myapp  # Set namespace
```

## Phase 6: Deployment Strategies

### Strategy Decision Matrix

| Strategy | Risk | Speed | Rollback | Cost | Best For |
|----------|------|-------|----------|------|----------|
| Rolling | Low-Med | Fast | Slow (re-roll) | None | Standard deployments |
| Blue-Green | Low | Instant | Instant (switch) | 2x infra | Critical services, zero-downtime |
| Canary | Very Low | Slow | Instant (route 0%) | Minimal | High-traffic, risky changes |
| Feature Flag | Very Low | Instant | Instant (toggle) | None | Gradual rollout, A/B testing |
| Recreate | High | Fast | Slow | None | Dev/staging, stateful apps |

### Canary Deployment Workflow

```
1. Deploy canary (1 pod with new version)
2. Route 5% traffic → canary
3. Monitor for 5 minutes:
   - Error rate < baseline + 0.1%?
   - p99 latency < baseline + 50ms?
   - No new error types?
4. If healthy → 25% → monitor 10 min
5. If healthy → 50% → monitor 10 min
6. If healthy → 100% (full rollout)
7. If ANY check fails → route 0% to canary → rollback → alert

Automation: Argo Rollouts, Flagger, or Istio + custom controller
```

### Rollback Checklist

When a deployment goes wrong:
1. **Immediate**: Route traffic away from new version (canary→0%, blue-green→switch)
2. **If rolling**: `kubectl rollout undo` or redeploy previous SHA
3. **Check**: Are database migrations backward-compatible? (If not, you have a bigger problem)
4. **Verify**: Rollback successful? Check error rates, latency
5. **Communicate**: Post in #incidents, update status page
6. **Investigate**: Don't re-deploy until root cause found

### Database Migration Safety

```
RULE: Migrations must be backward-compatible with the PREVIOUS version.
      (Because during rolling deploy, both versions run simultaneously)

Safe migration pattern:
  v1: Add new column (nullable, with default)
  v2: Backfill data, start writing to new column
  v3: Make new column required, stop writing old column
  v4: Drop old column (after v3 is fully deployed)

NEVER in one deploy:
  ❌ Rename column
  ❌ Change column type
  ❌ Drop column still read by current version
  ❌ Add NOT NULL without default
```

## Phase 7: Observability Stack

### Three Pillars + Bonus

| Pillar | What | Tools | Priority |
|--------|------|-------|----------|
| **Metrics** | Numeric measurements over time | Prometheus, Datadog, CloudWatch | 1 (start here) |
| **Logs** | Event records | ELK, Loki, CloudWatch Logs | 2 |
| **Traces** | Request flow across services | Jaeger, Tempo, X-Ray, Honeycomb | 3 |
| **Profiling** | CPU/memory hot paths | Pyroscope, Parca | 4 (when optimizing) |

### Key Metrics to Track

```yaml
# RED Method (request-driven services)
rate:     # Requests per second
errors:   # Failed requests per second
duration: # Latency distribution (p50, p95, p99)

# USE Method (infrastructure/resources)
utilization:  # % of resource in use (CPU, memory, disk)
saturation:   # Queue depth, pending work
errors:       # Resource errors (OOM, disk full)

# Business Metrics (most important!)
signups_per_hour:
checkout_completion_rate:
api_calls_by_customer:
revenue_per_minute:
```

### Alerting Rules

```yaml
# alerting-rules.yml
alerts:
  # Symptom-based (good — tells you users are impacted)
  - name: HighErrorRate
    condition: "error_rate_5xx > 1% for 5m"
    severity: critical
    runbook: docs/runbooks/high-error-rate.md
    notify: [pagerduty, slack-incidents]

  - name: HighLatency
    condition: "p99_latency > 2s for 5m"
    severity: warning
    runbook: docs/runbooks/high-latency.md
    notify: [slack-incidents]

  # Cause-based (supplementary — helps diagnose)
  - name: PodCrashLooping
    condition: "pod_restart_count increase > 3 in 10m"
    severity: warning
    notify: [slack-platform]

  - name: DiskSpaceWarning
    condition: "disk_usage > 80%"
    severity: warning
    notify: [slack-platform]

  - name: CertificateExpiring
    condition: "cert_expiry_days < 14"
    severity: warning
    notify: [slack-platform]

# Alert rules:
# 1. Every alert must have a runbook link
# 2. Every alert must be actionable (if you can't do anything, remove it)
# 3. Critical = wake someone up. Warning = check next business day.
# 4. Review alerts monthly — archive unused, tune noisy ones
```

### Structured Logging Standard

```json
{
  "timestamp": "2026-02-16T05:00:00.000Z",
  "level": "error",
  "service": "api",
  "trace_id": "abc123",
  "span_id": "def456",
  "method": "POST",
  "path": "/api/orders",
  "status": 500,
  "duration_ms": 342,
  "user_id": "usr_789",
  "error": {
    "type": "DatabaseError",
    "message": "connection timeout",
    "stack": "..."
  },
  "context": {
    "order_id": "ord_123",
    "payment_method": "card"
  }
}
```

**Log level guide:**
- `error`: Something failed, needs attention
- `warn`: Unexpected but handled (retry succeeded, fallback used)
- `info`: Business events (order placed, user signed up, deploy started)
- `debug`: Technical detail (query executed, cache hit/miss) — OFF in prod

### Dashboard Template

Every service dashboard should have:

```
Row 1: Traffic Overview
  - Request rate (per endpoint)
  - Error rate (4xx, 5xx separate)
  - Active users / connections

Row 2: Performance
  - p50, p95, p99 latency
  - Throughput
  - Apdex score

Row 3: Resources
  - CPU utilization (per pod/instance)
  - Memory usage (vs limit)
  - Disk I/O / Network I/O

Row 4: Business
  - Revenue per minute (if applicable)
  - Conversion funnel
  - Queue depth / processing lag

Row 5: Dependencies
  - Database query latency + connection pool
  - External API latency + error rate
  - Cache hit rate
```

## Phase 8: Incident Response

### Severity Levels

| Level | Definition | Response Time | Example |
|-------|-----------|---------------|---------|
| SEV-1 | Complete outage, revenue impact | 15 min | Site down, payments failing |
| SEV-2 | Major feature broken, workaround exists | 30 min | Search broken, checkout slow |
| SEV-3 | Minor feature broken, low impact | 4 hours | Admin panel bug, non-critical API |
| SEV-4 | Cosmetic / no user impact | Next sprint | Typo, minor UI glitch |

### Incident Workflow

```
1. DETECT (automated or reported)
   → Alert fires / user reports issue
   → Create incident channel: #inc-YYYY-MM-DD-description

2. TRIAGE (first 5 minutes)
   → Assign Incident Commander (IC)
   → Determine severity level
   → Post initial assessment in channel
   → Update status page (if customer-facing)

3. MITIGATE (focus on stopping the bleeding)
   → Can we rollback? → Do it
   → Can we scale up? → Do it
   → Can we feature-flag disable? → Do it
   → DON'T debug root cause yet — restore service first

4. RESOLVE
   → Confirm service restored (metrics, customer reports)
   → Communicate resolution to stakeholders
   → Update status page

5. POST-MORTEM (within 48 hours)
   → Blameless — focus on systems, not people
   → Timeline of events
   → Root cause analysis (5 Whys)
   → Action items with owners and deadlines
   → Share with team
```

### Post-Mortem Template

```markdown
# Incident Post-Mortem: [Title]

**Date:** YYYY-MM-DD
**Duration:** Xh Ym
**Severity:** SEV-X
**Incident Commander:** [name]
**Author:** [name]

## Summary
[1-2 sentence summary of what happened and impact]

## Impact
- Users affected: [number/percentage]
- Revenue impact: [if applicable]
- Duration: [start to full resolution]

## Timeline (all times UTC)
| Time | Event |
|------|-------|
| 14:00 | Deploy v2.3.1 begins |
| 14:05 | Error rate spikes to 15% |
| 14:07 | Alert fires, IC paged |
| 14:12 | Rollback initiated |
| 14:15 | Service restored |

## Root Cause
[Technical explanation — what actually broke and why]

## Contributing Factors
- [Factor 1 — e.g., migration not tested with production data volume]
- [Factor 2 — e.g., canary deployment not configured for this service]

## What Went Well
- [Fast detection — alert fired within 2 minutes]
- [Clear runbook — IC knew rollback procedure]

## What Went Wrong
- [No canary — went straight to 100% rollout]
- [Migration was not backward-compatible]

## Action Items
| Action | Owner | Due | Priority |
|--------|-------|-----|----------|
| Add canary to deployment | @engineer | YYYY-MM-DD | P1 |
| Add migration backward-compat check | @engineer | YYYY-MM-DD | P1 |
| Update runbook for this service | @sre | YYYY-MM-DD | P2 |

## Lessons Learned
[Key takeaways for the team]
```

### On-Call Best Practices

```yaml
on_call:
  rotation: weekly
  handoff: Monday 10:00 (overlap 1h with previous)
  escalation:
    - primary: respond within 15 min
    - secondary: auto-page if no ack in 15 min
    - manager: auto-page if no ack in 30 min

  expectations:
    - Laptop + internet within reach
    - Respond to page within 15 minutes
    - Follow runbook first, improvise second
    - Escalate early — "I don't know" is fine
    - Update incident channel every 15 min during active incident

  wellness:
    - No more than 1 week in 4 on-call
    - Comp time after major incidents
    - Toil budget: <30% of on-call time should be toil
    - Quarterly review: are we paging too much?
```

## Phase 9: Security Hardening

### Security Checklist (CI Pipeline)

```yaml
security_gates:
  # Pre-commit
  - tool: gitleaks / trufflehog
    what: Secret detection in code
    block: true

  # Build
  - tool: semgrep / CodeQL
    what: Static analysis (SAST)
    block: critical findings

  - tool: npm audit / pip audit / cargo audit
    what: Dependency vulnerabilities (SCA)
    block: critical/high

  # Container
  - tool: trivy / grype
    what: Image vulnerability scan
    block: critical

  - tool: hadolint
    what: Dockerfile best practices
    block: error level

  # Deploy
  - tool: checkov / tfsec
    what: IaC security scan
    block: high findings

  # Runtime
  - tool: falco / sysdig
    what: Runtime anomaly detection
    alert: true
```

### Secrets Management Decision

| Method | Security | Complexity | Best For |
|--------|----------|------------|----------|
| CI/CD env vars | Basic | Low | Small teams, non-critical |
| AWS Secrets Manager / GCP Secret Manager | High | Medium | Cloud-native apps |
| HashiCorp Vault | Very High | High | Multi-cloud, strict compliance |
| SOPS + git | Good | Low | GitOps workflows |
| External Secrets Operator | High | Medium | Kubernetes + cloud secrets |

**Rules:**
- Rotate secrets every 90 days minimum
- Different secrets per environment (dev ≠ staging ≠ prod)
- Audit all secret access
- Never log secrets — mask in CI output
- Use OIDC/keyless auth where possible (no long-lived tokens)

### Network Security Baseline

```
1. Default deny all — explicitly allow what's needed
2. TLS everywhere — including internal service-to-service
3. No public IPs on internal services — use load balancers / API gateways
4. WAF on public endpoints — OWASP Top 10 rules minimum
5. Rate limiting on all APIs — prevent abuse and DDoS
6. DNS for service discovery — never hardcode IPs
7. VPN or zero-trust for admin access — no SSH from internet
8. Network policies in K8s — pods can't talk to everything
9. Egress control — services should only reach what they need
10. Certificate auto-renewal — cert-manager or ACM
```

## Phase 10: SRE Practices

### SLO Framework

```yaml
# Define SLOs for every user-facing service
service: checkout-api
slos:
  availability:
    target: 99.95%        # 4.38 hours downtime/year
    window: 30d rolling
    measurement: "successful_requests / total_requests"

  latency:
    target: 99%           # 99% of requests under threshold
    threshold: 500ms      # p99 < 500ms
    window: 30d rolling

  freshness:
    target: 99.9%         # Data updated within SLA
    threshold: 5m
    window: 30d rolling

error_budget:
  monthly_budget: 0.05%   # ~21.6 minutes
  burn_rate_alert:
    fast: 14.4x           # Budget consumed in 1 hour → page
    slow: 3x              # Budget consumed in 10 hours → ticket
  policy:
    budget_exhausted:
      - freeze non-critical deploys
      - redirect eng effort to reliability
      - review in weekly SRE sync
```

### Toil Reduction

```
Toil = manual, repetitive, automatable, reactive, no lasting value

Track toil:
  - Log manual interventions for 2 weeks
  - Categorize: deployment, scaling, cert renewal, data fixes, permissions
  - Prioritize: frequency × time × frustration

Target: <30% of engineering time on toil
If toil > 50%: stop feature work, automate the top 3 toil items

Common toil automation:
  Manual deploys         → CI/CD pipeline
  Certificate renewal    → cert-manager / ACM
  Scaling up/down        → HPA / auto-scaling groups
  Permission requests    → Self-service IAM with approval
  Data fixes             → Admin API / scripts
  Dependency updates     → Renovate / Dependabot
  Flaky test management  → Auto-quarantine + ticket
```

### Capacity Planning

```yaml
capacity_review:
  frequency: monthly
  inputs:
    - current_utilization: "CPU, memory, disk, network per service"
    - growth_rate: "request rate trend over 90 days"
    - planned_events: "launches, marketing campaigns, seasonal peaks"
    - headroom_target: 30%  # Don't run above 70% sustained

  formula:
    needed_capacity: "current_usage × (1 + growth_rate) × (1 + headroom)"
    lead_time: "14 days for cloud, 60+ days for hardware"

  actions:
    - "If utilization > 70%: plan scaling within 2 weeks"
    - "If utilization > 85%: emergency scaling NOW"
    - "If utilization < 30%: rightsize down (save money)"
```

## Phase 11: Cost Optimization

### Cloud Cost Rules

```
1. Right-size first — most instances are overprovisioned
   Check: actual CPU/memory usage vs provisioned (CloudWatch, Datadog)
   Action: downsize to next tier that maintains 70% headroom

2. Reserved capacity for baseline — spot/preemptible for burst
   Pattern: 60% reserved + 30% on-demand + 10% spot
   Savings: 40-70% on reserved vs on-demand

3. Auto-scale to zero when possible
   - Dev/staging environments: scale down nights + weekends
   - Serverless for bursty workloads (Lambda, Cloud Functions)

4. Delete zombie resources monthly
   - Unattached EBS volumes
   - Old snapshots (>90 days, not tagged for retention)
   - Unused load balancers
   - Orphaned Elastic IPs

5. Storage tiering
   - Hot: SSD (frequently accessed)
   - Warm: HDD (monthly access)
   - Cold: S3 Glacier / Archive (yearly access)
   - Auto-lifecycle policies on S3 buckets

6. Tag everything — untagged = untracked = wasted
   Required tags: environment, team, service, cost-center
   Weekly report: cost by tag, highlight untagged resources
```

### Monthly Cost Review Template

```markdown
## Cloud Cost Review — [Month YYYY]

### Summary
- Total spend: $X,XXX (vs budget: $X,XXX)
- MoM change: +X% ($XXX)
- Top 3 cost drivers: [service1, service2, service3]

### By Service
| Service | Cost | % of Total | MoM Change | Action |
|---------|------|-----------|------------|--------|
| EKS | $XXX | XX% | +X% | Right-size node group |
| RDS | $XXX | XX% | 0% | Consider reserved |
| S3 | $XXX | XX% | +X% | Add lifecycle rules |

### Optimization Actions Taken
- [Action 1]: Saved $XXX/mo
- [Action 2]: Saved $XXX/mo

### Next Month Actions
- [ ] [Action with estimated savings]
```

## DevOps Maturity Assessment

Score your team (1-5 per dimension):

| Dimension | 1 (Ad-hoc) | 3 (Defined) | 5 (Optimized) |
|-----------|-----------|-------------|----------------|
| **CI/CD** | Manual deploy | Automated pipeline, manual gate | Full auto with canary, <15 min to prod |
| **IaC** | Click-ops console | Some Terraform, manual tweaks | 100% IaC, GitOps, drift detection |
| **Monitoring** | Check when broken | Dashboards + basic alerts | SLOs, error budgets, auto-remediation |
| **Incident** | Panic + SSH | Runbooks, on-call rotation | Blameless postmortems, chaos engineering |
| **Security** | Annual audit | CI scanning, secret manager | Shift-left, runtime detection, zero-trust |
| **Cost** | Surprise bills | Monthly review, some reservations | Real-time tracking, auto-optimization |

**Score interpretation:**
- 6-12: Foundations needed — focus on CI/CD and basic monitoring
- 13-20: Growing — add IaC and incident process
- 21-26: Mature — optimize with SRE practices and cost management
- 27-30: Elite — focus on chaos engineering and developer experience

## Natural Language Commands

Say things like:
- "Set up CI/CD for my Node.js project"
- "Create a Dockerfile for my Python API"
- "Write Terraform for an ECS service with RDS"
- "Design a monitoring dashboard for my service"
- "Help me write a post-mortem for yesterday's outage"
- "Review my Kubernetes deployment for production readiness"
- "What deployment strategy should I use?"
- "Help me set up alerting rules"
- "Create an incident response runbook for database failures"
- "Audit my cloud costs and suggest optimizations"
- "Assess our DevOps maturity"
- "Set up secret management for our CI pipeline"
