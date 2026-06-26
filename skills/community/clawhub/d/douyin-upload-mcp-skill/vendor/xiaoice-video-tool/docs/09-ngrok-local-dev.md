# Ngrok Local Dev Runbook

This runbook describes the local ngrok bootstrap workflow defined in `docs/08-ngrok-github-bootstrap-plan.md`.

## 1. Scope and Warning

- This workflow manages **one tunnel only** by default: callback tunnel for `VIDEO_TASK_SERVICE_PORT` (default `3105`).
- Dual-tunnel XiaoIce webhook bootstrap is out of scope in this repository.
- Use this runbook for fresh clone local development and callback verification.

## 2. First-Time Setup (Fresh Clone)

```bash
npm install
cp .env.example .env
ngrok config add-authtoken <your-token>
```

Then update `.env`:

- `VIDEO_USE_NGROK=true`
- non-empty `VIDEO_SERVICE_INTERNAL_TOKEN`
- non-empty `VIDEO_SERVICE_ADMIN_TOKEN`
- non-empty `VIDEO_SERVICE_CALLBACK_TOKEN`
- optional ngrok overrides: `NGROK_BIN`, `NGROK_API_URL`, `NGROK_AUTHTOKEN`, `NGROK_DOMAIN`, `NGROK_REGION`

Notes:

- If `NGROK_AUTHTOKEN` is empty, the command above (`ngrok config add-authtoken`) is required once per machine.
- Node.js runtime must be `>=22`.

## 3. Command Reference

| Command | Purpose | Main Output |
| --- | --- | --- |
| `npm run dev:service` | Start `video-task-service` in background helper mode | service health becomes reachable; runtime PID/log files |
| `npm run dev:ngrok` | Start/reuse one ngrok tunnel for `VIDEO_TASK_SERVICE_PORT` | HTTPS public URL written to runtime file |
| `npm run dev:ngrok:status` | Query `NGROK_API_URL/api/tunnels` and print active tunnel info | current public URL, bound local addr, callback endpoint |
| `npm run dev:callback:sync` | Sync ngrok HTTPS URL into service runtime config (`callbackPublicBaseUrl`) | admin config updated via `PUT /v1/admin/config` |
| `npm run dev:up` | One-command bootstrap (`dev:service -> dev:ngrok -> dev:callback:sync`) | final health URL + callback URL summary |
| `npm run dev:doctor` | Diagnostics for service health, ngrok reachability, callback sync consistency | pass/fail checks with remediation hints |

## 4. Daily Start

```bash
npm run dev:up
npm run dev:ngrok:status
npm run dev:doctor
```

Expected result:

- service `/health` is healthy
- ngrok exposes an `https://` URL for the service port
- callback base URL is synced to the same ngrok URL

## 5. Runtime Files

Runtime artifacts are written under `${XIAOICE_VIDEO_STATE_DIR}/runtime`.

Required files:

- `${XIAOICE_VIDEO_STATE_DIR}/runtime/video-service.pid`
- `${XIAOICE_VIDEO_STATE_DIR}/runtime/video-service.log`
- `${XIAOICE_VIDEO_STATE_DIR}/runtime/ngrok.pid`
- `${XIAOICE_VIDEO_STATE_DIR}/runtime/ngrok-url.txt`
- `${XIAOICE_VIDEO_STATE_DIR}/runtime/ngrok.log`
- `${XIAOICE_VIDEO_STATE_DIR}/runtime/bootstrap.last.json`

If `XIAOICE_VIDEO_STATE_DIR` is relative (default `./data`), it resolves against repository root.

## 6. Recovery After ngrok URL Changes

When ngrok rotates to a new public URL:

1. Run `npm run dev:ngrok` (or `npm run dev:up` when `VIDEO_USE_NGROK=true`).
2. Run `npm run dev:callback:sync`.
3. Run `npm run dev:doctor`.
4. Re-check tunnel output with `npm run dev:ngrok:status`.

This ensures `callbackPublicBaseUrl` matches the current tunnel URL before new tasks are submitted.

## 7. Troubleshooting

- `dev:ngrok` fails on first machine setup:
  Run `ngrok config add-authtoken <your-token>` and retry.
- `dev:ngrok:status` cannot find a valid HTTPS tunnel:
  Ensure ngrok is running for `VIDEO_TASK_SERVICE_PORT` and retry `npm run dev:ngrok`.
- `dev:doctor` reports callback URL mismatch:
  Run `npm run dev:callback:sync`, then run `npm run dev:doctor` again.
- Need immediate fallback without ngrok:
  Switch to manual mode in `docs/04-deployment.md` (`VIDEO_USE_NGROK=false` + manual `VIDEO_CALLBACK_PUBLIC_BASE_URL`).
