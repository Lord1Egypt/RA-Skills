---
name: render
description: Deploy and operate apps on Render from OpenClaw (Blueprint + Dashboard deeplink, native MCP, or REST). Use when the user wants to deploy, host, or publish an app; create or edit render.yaml; add web, static, worker, cron, private, Workflow, Postgres, or Key Value services; get a Blueprint deeplink; connect Render MCP with openclaw mcp add; or configure env vars, health checks, scaling, and previews.
version: 4.0.0
metadata:
  openclaw:
    emoji: "☁️"
    homepage: "https://render.com/docs"
    primaryEnv: RENDER_API_KEY
    requires:
      bins:
        - git
        - curl
    envVars:
      - name: RENDER_API_KEY
        required: false
        description: Optional Render API key for MCP, REST, and deploy verification. Create one at https://dashboard.render.com/u/*/settings#api-keys. Not required for Blueprint plus Dashboard deeplink.
      - name: RENDER_DEPLOY_HOOK_URL
        required: false
        description: Optional per-service deploy hook. POST only after the user confirms this redeploy. Do not log the URL.
---

# Render Skill

Deploy apps to Render from OpenClaw. Prefer a Blueprint when the app is more than one service. Prefer native Render MCP for a single web or static site once MCP is connected. Workflows are a separate service type and do not belong in `render.yaml` yet.

Field names and CLI verbs change. Before emitting YAML or API bodies, fetch [Blueprint spec](https://render.com/docs/blueprint-spec.md) and [MCP docs](https://render.com/docs/mcp-server.md). Official Cursor/Codex skills: [render-oss/skills](https://github.com/render-oss/skills).

## When to Use This Skill

Activate when the user wants to:

- Deploy, host, or publish an application on Render
- Create or edit a `render.yaml` Blueprint
- Add web, static, private, worker, cron, or Workflow services; Postgres; or Key Value
- Connect Render MCP from OpenClaw, or fall back to mcporter / REST
- Validate a Blueprint or get a Dashboard deeplink

## Method Selection

Use this rule unless the user names a method.

**Direct create (MCP, else REST)** when all of these are true:

- One web service or one static site
- No worker, cron, private service, or Workflow
- No Postgres or Key Value at create time
- Simple env vars only (no env groups)
- MCP is connected, or `RENDER_API_KEY` is set and the user accepts REST

If this path fits and MCP is not connected, set up MCP first (`references/mcp-integration.md`). Do not invent a Blueprint unless the user prefers IaC.

**Blueprint + push + deeplink** when any of these are true:

- Multiple services
- Postgres, Key Value, worker, cron, or private service
- The user wants IaC in the repo
- No MCP and no API key

**Dashboard or Render CLI for Workflows.** Blueprints cannot create or manage them. See `references/workflows.md`.

## Live actions (required)

Creating services, triggering deploys (API, MCP `trigger_deploy`, or a deploy hook), replacing env vars, restarting, or destroying resources changes a live Render workspace and can incur cost. Blueprint Apply in the Dashboard is the user’s click; do not also fire API/MCP/hook deploys unless they asked for that too.

Before any mutating call, state in chat and wait for an explicit yes for **this** action:

- Target workspace (not “whatever is selected”)
- Service or Blueprint name
- Environment: production vs preview vs new
- Plan / that the resource can be billable and persistent
- What will happen (create, redeploy, env replace, destroy)

Do not treat a general “deploy this app” from an earlier turn as consent to redeploy now.

Read-only list/get/logs/metrics are fine once credentials exist.

**Credentials:** never print `RENDER_API_KEY`, deploy-hook URLs with secrets, or `Authorization` headers. Check presence, not value:

```bash
[ -n "$RENDER_API_KEY" ] && echo "RENDER_API_KEY is set" || echo "RENDER_API_KEY is not set"
openclaw mcp doctor render --probe
```

Do not echo headers, curl `-v`, or MCP probe output that might contain the token. Prefer a test workspace for first-time MCP/REST creates.

## Happy Path (New Users)

## Happy Path (New Users)

1. Git repo (GitHub, GitLab, Bitbucket, or Cursor Origin) vs prebuilt Docker image. Image-backed services are Dashboard/API only; MCP cannot create them. A Blueprint with `runtime: image` still needs `render.yaml` in a Git repo.
2. Whether Render should provision the database, workers, cron, or Workflow the app actually needs.

Then follow the matching method below.

## Prerequisites

1. **Git remote** for Blueprint and MCP Git deploys: `git remote -v`. If none, ask the user to create a repo, add `origin`, and push. Cursor Origin is in beta; workspace admins connect it in Render Account Settings.
2. **Render CLI (optional)** for `render blueprints validate` and `render workflows init`. Install: `brew install render` or the [Render CLI](https://github.com/render-oss/cli).
3. **API key (optional)** for MCP, REST, verify, and re-deploy: [API Keys](https://dashboard.render.com/u/*/settings#api-keys). Set `RENDER_API_KEY`. Do not commit it.

## Security Notes

- Never put secret **values** in `render.yaml`, chat, or logs. Record env **names** only; use `sync: false` and have the user fill values in the Dashboard.
- Validate before push: `render blueprints validate render.yaml` or the Validate Blueprint API.
- Do not `git commit` / `git push` unless the user asked to deploy or confirmed the Blueprint file.
- New Key Value instances: `ipAllowList: []` unless the user asked for public access.
- Do not set continuous auto-deploy unless the user wants every push to go live.
- Sanitize user-supplied names before writing YAML.

## References

- `references/codebase-analysis.md`
- `references/blueprint-spec.md`
- `references/workflows.md`
- `references/mcp-integration.md`
- `references/rest-api-deployment.md`
- `references/post-deploy-checks.md`
- `references/troubleshooting-basics.md`
- `assets/` (node-express, python-web, static-site, web-with-postgres)

---

# Method 1: Blueprint + deeplink

## Step 1: Analyze and write render.yaml

Use `references/codebase-analysis.md`. Put `render.yaml` at the repo root. `sync: false` for secrets. Validate before asking for a push.

```bash
render blueprints validate render.yaml
```

## Step 2: Commit and push

Render reads the Blueprint from the Git remote.

```bash
git add render.yaml
git commit -m "Add Render deployment configuration"
git push origin main
```

Stop if there is no remote.

## Step 3: Dashboard deeplink

```bash
git remote get-url origin
```

Convert SSH to HTTPS and drop `.git`:

| SSH | HTTPS |
|-----|--------|
| `git@github.com:user/repo.git` | `https://github.com/user/repo` |
| `git@gitlab.com:user/repo.git` | `https://gitlab.com/user/repo` |
| `git@bitbucket.org:user/repo.git` | `https://bitbucket.org/user/repo` |

Cursor Origin remotes: use the HTTPS URL Render’s Git-provider docs show for that host. Do not guess a hostname.

Deeplink:

```
https://dashboard.render.com/blueprint/new?repo=<REPO_HTTPS_URL>
```

User checklist: confirm `render.yaml` is on the default branch, click the link, finish Git OAuth, fill `sync: false` vars, Apply.

## Step 4: Verify

If MCP is connected, use `list_services` / `list_deploys` / `list_logs` (see `references/mcp-integration.md`). Else REST (`references/post-deploy-checks.md`). Expect latest deploy `status: "live"`.

## Re-deploy

Only after the Live actions checklist. A deploy hook URL is a production trigger: same confirmation as MCP/REST.

- Push to the linked branch when the user already enabled auto-deploy and wants this commit live.
- MCP: `trigger_deploy` (after yes).
- REST: `POST https://api.render.com/v1/services/{serviceId}/deploys` with `Authorization: Bearer $RENDER_API_KEY`. Optional body: `{ "clearCache": "do_not_clear" }` or `"clear"`.
- Deploy hook: `curl -X POST "$RENDER_DEPLOY_HOOK_URL"` only if the user provided the hook and confirmed this redeploy. Do not log the URL.

---

# Method 2: Direct create (MCP or REST)

Single web or static site only. Confirm the repo is pushed. Complete **Live actions** (workspace, plan/cost, explicit yes). Then `references/mcp-integration.md` (preferred) or `references/rest-api-deployment.md`.

MCP cannot create: workers, private services, Workflows, image-backed services. Use Blueprint or Dashboard for those.

Set the workspace first (`list_workspaces` / `get_selected_workspace`, or ask the user to pick one). Do not create in the first workspace returned without confirmation.

---

# Blueprint snippets

**File:** `render.yaml` at repo root (Render can use another path at setup; default is root).

**Root keys:** `services`, `databases`, `envVarGroups`, `projects`, `ungrouped`, `previews`. Not Workflows.

**Service types in YAML:** `web`, `pserv`, `worker`, `cron`, `keyvalue`. Static site: `type: web` + `runtime: static`. Private services: `pserv`, not `private`.

**Runtimes:** `node`, `python`, `elixir`, `go`, `ruby`, `rust`, `docker`, `image`, `static`. Prefer `runtime`; `env` is deprecated.

### Web

```yaml
services:
  - type: web
    name: my-app
    runtime: node
    plan: free
    buildCommand: npm ci
    startCommand: npm start
    healthCheckPath: /health
    envVars:
      - key: NODE_ENV
        value: production
```

Python: `runtime: python`, `buildCommand: pip install -r requirements.txt`, `startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Bind HTTP to `0.0.0.0:$PORT`. Set `PYTHON_VERSION` / `NODE_VERSION` when the repo pins them.

### Static site

No `plan` field.

```yaml
- type: web
  name: my-blog
  runtime: static
  buildCommand: npm ci && npm run build
  staticPublishPath: ./dist
```

Optional: `headers`, `routes`.

### Env vars

- Literal: `key` + `value` (never secrets).
- Postgres: `fromDatabase.name` + `fromDatabase.property` (`connectionString`).
- Key Value / other service: `fromService.type` + `fromService.name` + `fromService.property` (or `fromService.envVarKey`).
- Secret: `sync: false` (service-level only; not inside env groups).
- Generated: `generateValue: true`.
- Shared: `fromGroup: <envVarGroups[].name>`.

Env groups cannot use `fromDatabase`, `fromService`, or `sync: false`.

### Postgres

```yaml
databases:
  - name: my-db
    plan: basic-256mb
    databaseName: my_app
    user: my_user
    region: oregon
    postgresMajorVersion: "18"
```

Plans: `free`, `basic-256mb`, `basic-1gb`, `basic-4gb`, `pro-*`, `accelerated-*`. **Free instances expire after 30 days.** Confirm the default major version on the spec before pinning. Optional: `diskSizeGB`, `ipAllowList`, `readReplicas`, `highAvailability.enabled`, `storageAutoscalingEnabled`, `connectionPool`.

### Key Value

`ipAllowList` is required. Default to private:

```yaml
services:
  - type: keyvalue
    name: my-cache
    ipAllowList: []
    plan: free
    maxmemoryPolicy: allkeys-lru
```

Public access only if requested: `source: 0.0.0.0/0`. Reference with `fromService.type: keyvalue`, `property: connectionString`. Paid instances persist; see spec for `persistenceMode`.

### Cron

```yaml
- type: cron
  name: my-cron
  runtime: python
  schedule: "0 * * * *"
  buildCommand: "true"
  startCommand: python scripts/daily.py
```

`buildCommand` is required. Free plan is not available for cron, worker, or `pserv`.

### Env groups

```yaml
envVarGroups:
  - name: app-env
    envVars:
      - key: CONCURRENCY
        value: "2"
      - key: APP_SECRET
        generateValue: true

services:
  - type: web
    name: api
    envVars:
      - fromGroup: app-env
      - key: DATABASE_URL
        fromDatabase:
          name: my-db
          property: connectionString
```

### Health, region, scaling, disks, Docker

- Web: `healthCheckPath` for zero-downtime deploys.
- `region`: `oregon` (default), `ohio`, `virginia`, `frankfurt`, `singapore`. Set at create.
- `preDeployCommand` after build, before start (migrations).
- Manual scale: `numInstances`. Autoscaling: `scaling.minInstances` / `maxInstances` / CPU or memory targets. Not with persistent disks.
- Disk: `disk.name`, `disk.mountPath`, `disk.sizeGB` on web, pserv, worker.
- Monorepo: `rootDir`, `buildFilter.paths` / `ignoredPaths`.
- Docker: `runtime: docker` or `runtime: image`. `dockerCommand` instead of `startCommand` when needed.

### Previews and projects

- `previews.generation`: `off` | `manual` | `automatic`. Optional `previews.expireAfterDays`.
- `projects` with `environments` for staging/production. `ungrouped` for leftovers.

### Service plans

`free | starter | standard | pro | pro plus` (web/pserv/worker also `pro max`, `pro ultra`). Omit to keep an existing plan. Default for new paid-capable services is `starter` if you skip `plan`. Free is not available for pserv, worker, cron.

Dashboard: https://dashboard.render.com. New Key Value: https://dashboard.render.com/new/redis.

---

## Checklist

1. Choose MCP/REST vs Blueprint vs Workflow CLI using the heuristic above.
2. Write `render.yaml` when using Blueprint: `runtime`, Key Value as `type: keyvalue`, `ipAllowList: []` unless public access was requested.
3. `sync: false` for secrets at service level only.
4. Validate, commit, push, then the Blueprint deeplink. Or create via MCP after workspace selection.
5. Verify deploy `live`. Fix from `references/troubleshooting-basics.md` before a second deploy.

## Rules

- Prefer Blueprint for the full app; MCP for one web or static site; Dashboard/CLI for Workflows.
- Never commit API keys or secrets.
- Use `fromService` with the real type (`keyvalue`, `pserv`).
- Confirm live docs when a field is missing from this file rather than guessing.
