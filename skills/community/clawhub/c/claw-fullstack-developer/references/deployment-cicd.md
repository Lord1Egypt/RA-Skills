# Deployment & CI/CD

How to get the app from "works on my machine" to "running in production, auto-deployed, observable."

## Choosing a deployment target

| Target | Best for | Watch out for |
|---|---|---|
| **Vercel** | Next.js, static sites, small APIs | Serverless cold starts; cost at scale; vendor-specific features |
| **Netlify** | Static sites, JAMstack | Similar to Vercel, lighter on backend features |
| **Cloudflare Pages/Workers** | Edge-first, global low latency | Workers runtime is not Node — subset of APIs |
| **Fly.io** | Dockerized apps, global regions, persistent volumes | Regional failure requires planning |
| **Railway** | Simplest "just run my Dockerfile" | Limited regions; pricing at scale |
| **Render** | Heroku replacement; background workers, cron, DB | Similar to Railway |
| **AWS** (ECS/EKS/Lambda/App Runner) | Serious scale, AWS-integrated stacks | Highest complexity; IAM is a full-time job |
| **GCP / Azure** | Similar scope to AWS | Similar tradeoffs |
| **Kubernetes** (self-managed or EKS/GKE) | Large teams, multi-service, complex infra | Massive operational burden; don't reach for it for an MVP |
| **VPS** (Hetzner, DigitalOcean) + Docker | Cost-sensitive, full control | You own everything — backups, monitoring, security patches |

**Default recommendation**: Vercel for Next.js monolith. Fly.io or Railway for Docker-based Node/Python/Go. AWS when the user is already there or needs specific services. Avoid Kubernetes for v1 unless the team already runs it.

## Docker — when and how

### When to Dockerize
- Deploying to anything container-based (Fly, Railway, Render, ECS, K8s).
- You want the dev environment to match prod.
- The app has non-trivial system dependencies (binary libs, native modules).

### When to skip Docker
- Deploying to Vercel / Netlify (they handle runtime).
- Tiny scripts or cron jobs where a container is overkill.

### Dockerfile patterns

**Node.js (multi-stage, slim):**
```dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY package.json ./
EXPOSE 3000
USER node
CMD ["npm", "start"]
```

**Python (FastAPI):**
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY . .
EXPOSE 8000
USER 1000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Go (distroless, smallest):**
```dockerfile
FROM golang:1.23 AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /bin/server ./cmd/server

FROM gcr.io/distroless/static-debian12
COPY --from=builder /bin/server /server
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/server"]
```

### Docker rules
- **Multi-stage builds**: keep the final image small and free of build tools.
- **Run as non-root**: create a user, switch to it with `USER`.
- **Don't bake secrets** into images. Use runtime env vars or a secrets manager.
- **Pin base image versions** — `node:22-alpine`, not `node:latest`. Rebuild periodically for security patches.
- **`.dockerignore`**: mirror `.gitignore` + add `node_modules`, `.git`, test fixtures, local env files. Smaller context = faster builds.
- **Healthcheck** endpoint: `/health` that returns 200 when the app is ready to serve. Your orchestrator needs this.

## CI: GitHub Actions (default)

Most apps should have a single workflow that runs on every push and PR, plus a deploy workflow on merge to `main`.

### Minimal CI workflow
```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready --health-interval 10s
          --health-timeout 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/postgres
      - run: npm run build
```

### What every CI pipeline should do
1. Install dependencies (with a lockfile, deterministic).
2. Lint.
3. Typecheck.
4. Run tests (unit + integration).
5. Build the production artifact.
6. (Optional) Build and push Docker image to a registry.
7. (Optional) Deploy — usually a separate workflow, gated on passing CI.

### Speeding up CI
- Cache dependencies (`cache: 'npm'`, `actions/cache` for Python/Go).
- Run independent jobs in parallel (lint + typecheck + test as separate jobs).
- Only run E2E on main + nightly, not every push.
- Use matrix sparingly — test on one Node version in CI, not all of them, unless you ship a library.

## CD: deployment strategies

### Continuous deployment to staging
Every merge to `main` → auto-deploy to staging. No approval. Fast feedback, confidence from seeing it run.

### Production deployment
Pick one:
- **Auto-deploy `main` to prod** — fine for small teams and mature test coverage.
- **Tag to deploy** — merge to `main` goes to staging; creating a git tag triggers prod. Forces a human to "press the button."
- **Manual approval** — GitHub Actions environments support required reviewers.

### Preview deployments
Every PR gets its own URL (Vercel, Netlify, Fly.io all do this natively). Reviewers and designers can click around before approving. For anything user-visible, this is essential.

### Migrations during deploy
Run migrations **before** the new app version starts serving traffic, and make them backward-compatible (see `database-design.md`). Options:
- A pre-deploy CI step that runs `prisma migrate deploy` / `alembic upgrade head` / etc.
- A separate "migrate" job in your platform (Render job, Vercel build command, Fly "release command").

### Rollback plan
- Know how to revert the deploy in under 5 minutes.
- Don't assume "just redeploy the previous commit." If that commit has schema migrations, rollback is harder.
- Document the rollback procedure in the runbook.

## Platform-specific notes

### Vercel (Next.js)
- Connect GitHub repo → automatic deploys for `main` (production) and PRs (preview).
- Environment variables configured per environment (dev, preview, production).
- Database migrations: add to `"build"` script or use a dedicated CI job; Vercel build can run `prisma migrate deploy`.
- Serverless function limits: check timeout (10s default, up to 300s on paid plans), bundle size (~50 MB), cold starts.

### Fly.io
- `fly launch` generates a `fly.toml`. Commit it.
- `fly deploy` ships a new version. Can be called from CI with `flyctl` and `FLY_API_TOKEN`.
- Persistent storage via volumes (for DBs or file uploads).
- Global: deploy to multiple regions with `fly regions add`.
- Secrets: `fly secrets set KEY=value`. Not visible in logs.
- Release commands for migrations: `deploy.release_command = "npm run migrate"` in `fly.toml`.

### Railway
- Connect repo → auto-build via nixpacks or Dockerfile.
- Managed Postgres, Redis, etc. available as services with shared env vars.
- Release commands for migrations in `railway.json` or via UI.

### AWS (ECS / App Runner / Lambda)
- **App Runner** is the simplest — point at a container registry, it runs it. Fine for small apps.
- **ECS Fargate** is the workhorse for serious container deployments. Infrastructure as code (Terraform, CDK) is practically required.
- **Lambda** for event-driven or low-traffic APIs. Watch for cold starts; use SnapStart (Java/Python) or lean Node/Go runtimes.
- **Secrets**: AWS Secrets Manager or Parameter Store. Reference by ARN, don't paste values.
- **IAM**: least privilege. The role your app runs as should only have the permissions it needs. Auditing IAM is a real activity — budget time for it.

### Kubernetes
- Don't start here. Start with something simpler.
- If you do need it: use a managed K8s service (EKS, GKE, AKS). Don't self-host the control plane.
- Use Helm for app packaging; ArgoCD or Flux for GitOps.
- Set resource requests and limits on every pod. Pod disruption budgets. Liveness/readiness probes.

### VPS + Docker + nginx
Cost-effective, full control. Roughly:
- Hetzner/DO VPS with Ubuntu LTS.
- Docker + docker-compose or a simple orchestrator (Dokku, Coolify, Caprover).
- nginx (or Caddy — Caddy auto-provisions Let's Encrypt certs, very nice).
- Deploys via SSH + `docker pull && docker compose up -d`, or via a GitHub Actions runner.
- You own: backups, security updates, monitoring, log rotation, firewall, SSH hardening.

## Zero-downtime deploys

For anything past "hobby project" status:
- **Health checks**: app exposes `/health`; platform doesn't route traffic until it's healthy.
- **Graceful shutdown**: on SIGTERM, stop accepting new requests but finish in-flight ones. Platforms usually give you ~30s.
- **Rolling deploys** (or blue-green): new version runs alongside old until healthy, then old is torn down.
- **Database migrations first, app deploys after** — and migrations are backward-compatible.
- **Session handling**: if sessions are in memory, they die on every deploy. Use Redis or your DB.

## Environment management

Typical environments:
- **local** — each dev's machine. Their own `.env`.
- **staging / preview** — prod-like, wired to a staging DB. Every PR or every `main` push deploys here.
- **production** — the real one.

Rules:
- Each env has its own database. Never share.
- Each env has its own secrets. Rotating a staging key must not affect prod.
- Prod data must not flow back to staging (privacy, compliance). If you need realistic test data, anonymize.

## Feature flags

For any app past MVP, consider feature flags (LaunchDarkly, Unleash, ConfigCat, or a simple in-house `flags` table). Benefits:
- Deploy code without exposing it to users.
- Gradual rollouts (1%, 10%, 100%).
- Instant disable of a broken feature — faster than a rollback deploy.
- A/B testing.

Downsides: proliferation of flags that never get cleaned up. Add a "flag retirement" task to each release.

## Blue-green vs. canary

- **Blue-green**: run two identical envs. Cut traffic from blue to green. Rollback = cut back. Simple, not partial.
- **Canary**: route a small % of traffic to the new version; watch error rate; ramp up. Best for detecting regressions before wide blast.

Most platforms do rolling deploys (a kind of canary). Canary-by-header or canary-by-user is a manual setup worth building for revenue-critical apps.

## Disaster recovery

Define and test:
- **RTO** (Recovery Time Objective): how long can the app be down?
- **RPO** (Recovery Point Objective): how much data can we lose?

Then:
- Ensure backups meet RPO (hourly PITR for low RPO; daily for higher).
- Practice restores at least quarterly. Write a runbook.
- Have a secondary region plan if the RTO demands it. Most startups can tolerate an outage while the primary region recovers — don't build multi-region until you need it.
