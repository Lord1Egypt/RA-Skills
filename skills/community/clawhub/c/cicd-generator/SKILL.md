---
name: ci-gen
description: "Generate GitHub Actions CI/CD pipelines tailored to the current project. Use when the user says 'set up CI', 'create pipeline', 'github actions', 'CI/CD', 'deploy pipeline', 'add CI', 'set up continuous integration', 'create workflow', 'automate deploys', or 'add GitHub Actions'."
---

# CI/CD Generator

Generate production-grade GitHub Actions workflows by analyzing the current project structure. Supports any stack, any deploy target.

## Step 1: Detect Project Stack

Read the project root and identify what exists. Run these checks in parallel:

```
Glob: package.json, pnpm-workspace.yaml, turbo.json, lerna.json
Glob: requirements.txt, pyproject.toml, setup.py, Pipfile, poetry.lock
Glob: Dockerfile, docker-compose.yml, docker-compose.yaml
Glob: go.mod, Cargo.toml, Gemfile, build.gradle, pom.xml
Glob: vercel.json, next.config.*, nuxt.config.*, svelte.config.*
Glob: .github/workflows/*.yml, .github/workflows/*.yaml
```

Build a detection summary:

| Signal | Stack |
|--------|-------|
| `package.json` + `next.config.*` | Next.js |
| `package.json` + `nuxt.config.*` | Nuxt |
| `package.json` + `svelte.config.*` | SvelteKit |
| `package.json` (no framework config) | Generic Node.js |
| `requirements.txt` or `pyproject.toml` | Python |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `Dockerfile` | Docker build |
| `pnpm-workspace.yaml` or `turbo.json` | Monorepo |
| `vercel.json` | Vercel deploy target |

Read `package.json` to extract:
- Package manager (`packageManager` field, or check for `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`, `package-lock.json`)
- Scripts available (`lint`, `test`, `build`, `typecheck`, `format`)
- Node version requirements (`engines.node`)
- Framework and key dependencies

For Python, read `pyproject.toml` or `requirements.txt` to determine Python version and test framework (pytest, unittest).

## Step 2: Ask the User

Present the detection results and ask:

1. **Deploy target** (if not obvious from vercel.json/railway.toml):
   - Vercel (auto-deploy via git push, or CLI-based)
   - Railway (auto-deploy or CLI)
   - VPS via SSH (rsync + restart)
   - Docker registry (GHCR, Docker Hub, ECR)
   - None (CI only, no deploy)

2. **Environments**: Preview on PR + Production on main? Or just main?

3. **Matrix testing**: Test across multiple runtime versions? (e.g., Node 20 + 22, Python 3.11 + 3.12)

4. **Additional checks**: Security scanning? Dependency audit? Coverage reporting?

## Step 3: Generate Workflows

Create `.github/workflows/` directory and generate the appropriate workflow files.

### Action Versions Reference (current as of 2026)

Always use these versions:

```yaml
actions/checkout@v6
actions/setup-node@v6
actions/setup-python@v6
actions/cache@v5
docker/setup-buildx-action@v3
docker/login-action@v3
docker/build-push-action@v6
docker/metadata-action@v5
```

### 3A: Node.js / Next.js / Frontend Projects

File: `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with:
          node-version: NODE_VERSION
          cache: PACKAGE_MANAGER
      - run: INSTALL_COMMAND
      - run: LINT_COMMAND

  typecheck:
    name: Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with:
          node-version: NODE_VERSION
          cache: PACKAGE_MANAGER
      - run: INSTALL_COMMAND
      - run: TYPECHECK_COMMAND

  test:
    name: Test
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        node-version: [NODE_VERSIONS]
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with:
          node-version: ${{ matrix.node-version }}
          cache: PACKAGE_MANAGER
      - run: INSTALL_COMMAND
      - run: TEST_COMMAND

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [lint, typecheck, test]
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with:
          node-version: NODE_VERSION
          cache: PACKAGE_MANAGER
      - run: INSTALL_COMMAND
      - run: BUILD_COMMAND
```

**Package manager install commands:**
- npm: `npm ci`
- pnpm: `corepack enable && pnpm install --frozen-lockfile`
- yarn: `corepack enable && yarn install --immutable`
- bun: `bun install --frozen-lockfile`

**Cache key for setup-node:**
- npm: `cache: npm`
- pnpm: `cache: pnpm`
- yarn: `cache: yarn`

For **pnpm**, add the corepack enable step before install:
```yaml
- run: corepack enable
- uses: actions/setup-node@v6
  with:
    node-version: NODE_VERSION
    cache: pnpm
```

If the project has no `test` script, omit the test job. If no `lint` script, omit lint. Same for typecheck. Always keep build.

### 3B: Python Projects

File: `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: PYTHON_VERSION
          cache: pip
      - run: pip install ruff
      - run: ruff check .

  test:
    name: Test
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: [PYTHON_VERSIONS]
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - run: pip install -r requirements.txt
      - run: pytest

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: PYTHON_VERSION
          cache: pip
      - run: pip install -r requirements.txt
      - run: python3 -m build
```

For **pyproject.toml** projects, replace `pip install -r requirements.txt` with `pip install -e ".[dev]"` or the appropriate extras.

For **poetry** projects:
```yaml
- run: pip install poetry
- run: poetry install
- run: poetry run pytest
```

### 3C: Docker Projects

File: `.github/workflows/docker.yml`

```yaml
name: Docker

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    name: Build & Push
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v6

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        if: github.event_name != 'pull_request'
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - uses: docker/build-push-action@v6
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

For **Docker Hub** instead of GHCR:
```yaml
env:
  REGISTRY: docker.io
  IMAGE_NAME: DOCKER_HUB_USERNAME/IMAGE_NAME

# Login step:
- uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

For **ECR**:
```yaml
- uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: AWS_REGION
- uses: aws-actions/amazon-ecr-login@v2
```

### 3D: Monorepo Projects

For monorepos (Turborepo, pnpm workspaces, Nx), add **path filters** to avoid running everything on every change:

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  changes:
    name: Detect Changes
    runs-on: ubuntu-latest
    outputs:
      app: ${{ steps.filter.outputs.app }}
      api: ${{ steps.filter.outputs.api }}
      packages: ${{ steps.filter.outputs.packages }}
    steps:
      - uses: actions/checkout@v6
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            app:
              - 'apps/web/**'
              - 'packages/**'
            api:
              - 'apps/api/**'
              - 'packages/**'
            packages:
              - 'packages/**'

  ci-app:
    name: CI (Web)
    needs: changes
    if: needs.changes.outputs.app == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - run: corepack enable
      - uses: actions/setup-node@v6
        with:
          node-version: NODE_VERSION
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm --filter web lint
      - run: pnpm --filter web test
      - run: pnpm --filter web build

  ci-api:
    name: CI (API)
    needs: changes
    if: needs.changes.outputs.api == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - run: corepack enable
      - uses: actions/setup-node@v6
        with:
          node-version: NODE_VERSION
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm --filter api lint
      - run: pnpm --filter api test
      - run: pnpm --filter api build
```

Adapt the app names and filter paths based on the actual monorepo structure. Read `pnpm-workspace.yaml` or `turbo.json` to discover workspace packages.

For **Turborepo** specifically, leverage `turbo run`:
```yaml
- run: pnpm turbo run lint test build --filter=...[origin/main]
```

## Step 4: Generate Deploy Workflows

### Vercel Deploy

If deploying via Vercel CLI (not git-push auto-deploy):

File: `.github/workflows/deploy.yml`

```yaml
name: Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: true

env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

jobs:
  deploy-preview:
    name: Deploy Preview
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    needs: [ci]  # reference CI job
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with:
          node-version: NODE_VERSION
          cache: PACKAGE_MANAGER
      - run: npm i -g vercel
      - run: vercel pull --yes --environment=preview --token=${{ secrets.VERCEL_TOKEN }}
      - run: vercel build --token=${{ secrets.VERCEL_TOKEN }}
      - run: vercel deploy --prebuilt --token=${{ secrets.VERCEL_TOKEN }}

  deploy-production:
    name: Deploy Production
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    needs: [ci]
    environment: production
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with:
          node-version: NODE_VERSION
          cache: PACKAGE_MANAGER
      - run: npm i -g vercel
      - run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}
      - run: vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}
      - run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}
```

**Required secrets:** `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`

If the project uses Vercel's git integration (auto-deploy on push), skip this workflow and tell the user -- CI workflow alone is sufficient since Vercel handles deploys automatically.

### Railway Deploy

File: `.github/workflows/deploy.yml`

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    name: Deploy to Railway
    runs-on: ubuntu-latest
    needs: [ci]
    environment: production
    steps:
      - uses: actions/checkout@v6
      - uses: npm i -g @railway/cli
      - run: railway up --service SERVICE_NAME
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

**Required secrets:** `RAILWAY_TOKEN`

If Railway auto-deploys from GitHub, tell the user to enable "Wait for CI" in Railway service settings so it waits for the CI workflow to pass before deploying.

### VPS via SSH

File: `.github/workflows/deploy.yml`

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    name: Deploy to VPS
    runs-on: ubuntu-latest
    needs: [ci]
    environment: production
    steps:
      - uses: actions/checkout@v6

      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          port: ${{ secrets.VPS_PORT }}
          script: |
            cd /path/to/app
            git pull origin main
            INSTALL_AND_BUILD_COMMANDS
            RESTART_COMMAND
```

For **rsync-based deploys** (push built artifacts):
```yaml
      - name: Build
        run: BUILD_COMMAND

      - name: Deploy via rsync
        uses: burnett01/rsync-deployments@7
        with:
          switches: -avzr --delete
          path: dist/
          remote_path: /var/www/app/
          remote_host: ${{ secrets.VPS_HOST }}
          remote_user: ${{ secrets.VPS_USER }}
          remote_key: ${{ secrets.VPS_SSH_KEY }}
          remote_port: ${{ secrets.VPS_PORT }}

      - name: Restart service
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          port: ${{ secrets.VPS_PORT }}
          script: sudo systemctl restart APP_SERVICE
```

**Required secrets:** `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY`, `VPS_PORT`

### Docker Registry Deploy

Use the Docker workflow from Step 3C. If deploying to a server after push, add a post-push job:

```yaml
  deploy:
    name: Deploy
    needs: build-and-push
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            docker pull ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main
            docker compose up -d
```

## Step 5: Secrets Checklist

After generating workflows, output a checklist of secrets the user needs to configure in GitHub repo settings (Settings > Secrets and variables > Actions):

```
Required GitHub Secrets:
- [ ] VERCEL_TOKEN — from vercel.com/account/tokens
- [ ] VERCEL_ORG_ID — from .vercel/project.json or vercel.com dashboard
- [ ] VERCEL_PROJECT_ID — from .vercel/project.json or vercel.com dashboard
- [ ] RAILWAY_TOKEN — from railway.app dashboard > project > settings
- [ ] VPS_HOST — server IP or hostname
- [ ] VPS_USER — SSH username
- [ ] VPS_SSH_KEY — private SSH key (ed25519 recommended)
- [ ] VPS_PORT — SSH port (default 22)
- [ ] DOCKERHUB_USERNAME — Docker Hub username
- [ ] DOCKERHUB_TOKEN — Docker Hub access token
```

Only list secrets relevant to the chosen deploy target.

## Step 6: Status Badge

Offer to add a CI status badge to the project README:

```markdown
![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)
```

Read the git remote to determine OWNER/REPO automatically:
```bash
git remote get-url origin
```

## Rules

1. **Never hardcode secrets.** Always use `${{ secrets.NAME }}` references.
2. **Always use `concurrency` groups** to cancel redundant runs on the same branch/PR.
3. **Always pin action versions** to major tags (e.g., `@v6`), never `@latest` or `@main`.
4. **Use `fail-fast: false`** in matrix builds so one version failing doesn't cancel others.
5. **Separate CI from deploy.** CI runs on PRs and pushes. Deploy only runs on main (or tags).
6. **Use GitHub Environments** for production deploys to enable approval gates and env-specific secrets.
7. **Cache aggressively.** Use setup-node/setup-python built-in cache for dependencies. Use GHA cache for Docker layers.
8. **Run lint/typecheck/test in parallel** as separate jobs for faster feedback. Build depends on all passing.
9. **For monorepos, always add path filters.** Never run all workspace CI on every file change.
10. **If workflows already exist** (`.github/workflows/` is non-empty), read them first and ask the user whether to replace or extend.
11. **Replace placeholder values** (NODE_VERSION, PACKAGE_MANAGER, etc.) with actual detected values from the project. Never leave placeholders in the generated output.
12. **Only include jobs that the project supports.** If there is no test script, no test job. If there is no lint script, no lint job. Don't generate dead jobs.
