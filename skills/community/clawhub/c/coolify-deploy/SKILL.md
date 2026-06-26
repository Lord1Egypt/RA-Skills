---
name: coolify-deploy
description: Create, deploy, update, and troubleshoot Coolify applications with the official Coolify CLI. Use when user wants deploy via Coolify, app creation from GitHub, redeploy on push, env vars, logs, or fallback Docker/Traefik routing.
---

# Coolify Deploy

Use the **official `coolify` CLI first**. Use direct Docker + Traefik only as fallback.

## Core Rules

1. **Prefer CLI-managed apps** so deployments appear in Coolify UI and support push-to-deploy.
2. **Use `app create github` for private GitHub repos** and the correct GitHub App UUID.
3. **Verify both app status and HTTP 200** before calling a deploy finished.
4. **Use direct Docker only if Coolify creation is blocked**.

## When to Use

- Creating a new Coolify app
- Redeploying after code changes
- Debugging unhealthy deployments
- Adding env vars or checking deployment logs

## Required Info

- `server_uuid`
- `project_uuid`
- `environment_name` (usually `production`)
- `github_app_uuid` for private repos
- repo, branch, domain, exposed port

## Preferred Workflow

### 1. Verify CLI + context

```bash
coolify context verify
coolify github list --format=json
coolify app list --format=json
```

### 2. Create app from private GitHub repo

```bash
coolify app create github \
  --server-uuid <server_uuid> \
  --project-uuid <project_uuid> \
  --environment-name production \
  --github-app-uuid <github_app_uuid> \
  --git-repository owner/repo \
  --git-branch main \
  --build-pack dockerfile \
  --ports-exposes 80 \
  --name <app-name> \
  --domains http://<app>.<ip>.sslip.io \
  --instant-deploy \
  --format=json
```

### 3. Add env vars when needed

```bash
coolify app env create <app-uuid> --key PORT --value 80 --format=json
```

### 4. Force redeploy

```bash
coolify deploy uuid <app-uuid> --force --format=json
```

### 5. Verify success

```bash
coolify app get <app-uuid> --format=json
coolify app deployments list <app-uuid> --format=json
curl -I http://<domain>
```

## GitHub App Integration

List configured GitHub apps:

```bash
coolify github list --format=json
```

Use the **UUID** from this output in `coolify app create github --github-app-uuid ...`.

If a repo is private and `public` creation fails, switch to `github` creation.

## Common Issues

### App is `exited:unhealthy`

Check deployment logs first:

```bash
coolify app deployments list <app-uuid> --format=json
coolify app deployments logs <app-uuid>
```

Then verify:
- wrong GitHub App UUID
- wrong Dockerfile path
- missing env vars like `PORT`
- build/runtime errors

### Vite/Rollup native module error

Use Debian-based Node image:

```dockerfile
FROM node:20-slim AS builder
```

Avoid Alpine for builds that need native Rollup modules.

### nginx template expects `${PORT}`

Set env var in Coolify:

```bash
coolify app env create <app-uuid> --key PORT --value 80 --format=json
```

### Domain responds but UI still says `running:unknown`

Treat `HTTP 200 + finished deployment` as success. Coolify may still show `running:unknown`.

## Fallback: Direct Docker Deploy

Only use when CLI-managed app creation is blocked.
See `references/coolify-api.md` for direct Docker/Traefik fallback patterns.

## Quick Reference

```bash
coolify github list --format=json
coolify app create github --server-uuid <server> --project-uuid <project> --environment-name production --github-app-uuid <ghapp> --git-repository owner/repo --git-branch main --build-pack dockerfile --ports-exposes 80 --name myapp --domains http://myapp.<ip>.sslip.io --instant-deploy --format=json
coolify app env create <uuid> --key PORT --value 80 --format=json
coolify deploy uuid <uuid> --force --format=json
coolify app deployments list <uuid> --format=json
curl -I http://myapp.<ip>.sslip.io
```
