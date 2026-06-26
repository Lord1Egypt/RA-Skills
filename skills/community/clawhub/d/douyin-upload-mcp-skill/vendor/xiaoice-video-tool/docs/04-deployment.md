# Deployment Guide (v1 Draft)

## 1. Deployment Modes

v1 supports three runtime modes:

| Mode | Callback URL source | Recommended commands |
| --- | --- | --- |
| Local manual mode | `VIDEO_CALLBACK_PUBLIC_BASE_URL` from `.env` | `npm run service` (+ optional `npm run mcp`) |
| Local ngrok bootstrap mode | ngrok public URL synced through `PUT /v1/admin/config` | `npm run dev:up` |
| Self-hosted Docker mode | deployment-specific public URL | `docker compose up -d --build` |

No managed SaaS deployment is included in v1.

## 2. Environment Variables

Base service variables:

| Variable | Required | Purpose |
| --- | --- | --- |
| `VIDEO_TASK_SERVICE_PORT` | Yes | HTTP service listen port |
| `VIDEO_SERVICE_INTERNAL_TOKEN` | Yes | MCP -> service internal auth |
| `VIDEO_SERVICE_ADMIN_TOKEN` | Yes | Admin auth for runtime config sync |
| `VIDEO_SERVICE_CALLBACK_TOKEN` | Yes | Provider callback auth |
| `VIDEO_CALLBACK_PUBLIC_BASE_URL` | Yes | Callback base URL (manual mode default) |
| `XIAOICE_VIDEO_STATE_DIR` | Yes | Local state/storage path |
| `XIAOICE_VIDEO_SERVICE_BASE_URL` | Yes | MCP target service URL |
| `VIDEO_PROVIDER_VH_BIZ_ID` | Yes (unless request provides `vhBizId`) | Default provider business id |

Ngrok bootstrap variables (when `VIDEO_USE_NGROK=true`):

- `VIDEO_USE_NGROK`
- `NGROK_BIN`
- `NGROK_API_URL`
- `NGROK_AUTHTOKEN`
- `NGROK_DOMAIN`
- `NGROK_REGION`

## 3. Local Mode Selection

### A) Local Manual Callback Mode

Use when you already have a stable callback domain or want full manual control.

```bash
npm install
cp .env.example .env
# set VIDEO_USE_NGROK=false
# set VIDEO_CALLBACK_PUBLIC_BASE_URL=<public-base-url>
npm run service
```

### B) Local ngrok Bootstrap Mode

Use for fresh clone and fast callback exposure without manual callback URL editing.

```bash
npm install
cp .env.example .env
ngrok config add-authtoken <your-token>
# set VIDEO_USE_NGROK=true
npm run dev:up
```

`dev:up` flow: `dev:service -> dev:ngrok -> dev:callback:sync`.

## 4. Roll Back to Manual Callback URL

If ngrok bootstrap is unavailable or unstable, switch back immediately:

1. Stop local helper processes (`video-task-service`, `ngrok`).
2. Set `VIDEO_USE_NGROK=false` in `.env`.
3. Set `VIDEO_CALLBACK_PUBLIC_BASE_URL=<manual-public-url>` in `.env`.
4. Start service with `npm run service` (and `npm run mcp` if needed).
5. Verify callback endpoint: `POST ${VIDEO_CALLBACK_PUBLIC_BASE_URL}/v1/callbacks/provider?token=<VIDEO_SERVICE_CALLBACK_TOKEN>`.

## 5. Docker Run (Target Contract)

Single-host target:

```bash
docker compose up -d --build
docker compose ps
```

Minimum expectations:

- persistent volume for `XIAOICE_VIDEO_STATE_DIR`
- environment variables injected via `.env`
- health endpoint exposed for readiness checks

## 6. Smoke Check

After deployment, verify:

1. `GET /health` returns success.
2. `POST /v1/tasks` returns `submitted`.
3. provider callback can update terminal status and `videoUrl`.
4. MCP `create` and `get` both work.

## 7. Troubleshooting Entry Points

- run `npm run dev:doctor` in ngrok bootstrap mode
- run `npm run dev:ngrok:status` to inspect the active public callback URL
- verify callback URL is reachable from provider network
- verify callback token/header/query configuration matches runtime values
- verify `XIAOICE_VIDEO_STATE_DIR` is writable
