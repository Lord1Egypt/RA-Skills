# Coolify Reference

## Order of Preference

1. **Official Coolify CLI** (`coolify`) — preferred
2. **Coolify API** — useful for deploy/list/get when CLI is unavailable
3. **Direct Docker + Traefik** — fallback only

## Official CLI

### Context setup

```bash
coolify context add default http://217.77.2.59:8000 '<token>' --default
coolify context verify
```

### Discover GitHub Apps

```bash
coolify github list --format=json
```

### Create private GitHub app deployment

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

### App management

```bash
coolify app list --format=json
coolify app get <app-uuid> --format=json
coolify app update <app-uuid> --git-branch main --domains http://app.ip.sslip.io
coolify app delete <app-uuid> --force
```

### Environment variables

```bash
coolify app env list <app-uuid>
coolify app env create <app-uuid> --key PORT --value 80 --format=json
coolify app env update <app-uuid> --key PORT --value 80 --format=json
```

### Deployments and logs

```bash
coolify deploy uuid <app-uuid> --force --format=json
coolify app deployments list <app-uuid> --format=json
coolify app deployments logs <app-uuid>
```

## API

Use API mainly for:
- listing applications
- getting details
- triggering deployment
- deleting broken apps

### Auth

```bash
curl -H "Authorization: Bearer <token>" http://<host>:8000/api/v1/applications
```

### Trigger deploy

```bash
curl -X POST -H "Authorization: Bearer <token>" \
  "http://217.77.2.59:8000/api/v1/deploy?uuid=<app-uuid>"
```

### Delete app

```bash
curl -X DELETE -H "Authorization: Bearer <token>" \
  "http://217.77.2.59:8000/api/v1/applications/<app-uuid>"
```

## Fallback: Direct Docker Deploy

Use only if Coolify-managed app creation is blocked.

```bash
docker build -t myapp .
docker stop myapp 2>/dev/null || true
docker rm myapp 2>/dev/null || true
docker run -d --name myapp \
  --network coolify \
  --label "traefik.enable=true" \
  --label "traefik.http.routers.myapp.entrypoints=http" \
  --label "traefik.http.routers.myapp.rule=Host(\`myapp.<ip>.sslip.io\`)" \
  --label "traefik.http.services.myapp.loadbalancer.server.port=80" \
  myapp:latest
```

## Known Lessons

### `running:unknown`

If:
- deployment status is `finished`
- domain returns `HTTP 200`

Treat the app as healthy enough to proceed.

### Vite/Rollup on Alpine fails

Use:

```dockerfile
FROM node:20-slim AS builder
```

### nginx uses `${PORT}`

Set:

```bash
coolify app env create <app-uuid> --key PORT --value 80 --format=json
```
