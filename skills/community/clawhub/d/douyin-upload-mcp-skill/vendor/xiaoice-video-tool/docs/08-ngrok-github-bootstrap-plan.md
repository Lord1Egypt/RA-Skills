# GitHub-Ready Ngrok Bootstrap Plan

## Summary

This plan migrates the useful ngrok workflow from `claw-xiaoice` into `xiaoice-video-tool` in a way that is safe for a public GitHub repository and usable by fresh users after clone.

The goal is not to copy the old machine-specific setup literally. The goal is to copy the workflow:

- start `video-task-service`
- expose `3105` through ngrok
- discover the public URL
- sync `callbackPublicBaseUrl` through the existing admin API
- give the operator one-command local bootstrap and one-command status/diagnostics

The resulting public-repo experience must be:

```bash
npm install
cp .env.example .env
ngrok config add-authtoken <your-token>
npm run dev:up
```

After that, the user should be able to create a task and receive provider callbacks without manually editing callback URLs.

## Gap Review (Closed by This Revision)

The previous draft was directionally correct but under-specified in four places that block reliable execution:

- no preflight checklist (ngrok binary/version, Node runtime, required tokens) before running scripts
- no explicit command failure contract (what exits non-zero and what remediation is printed)
- no idempotency/re-entry rules for repeated `dev:up` execution on the same machine
- no phase-gated delivery plan mapping concrete file ownership to implementation tasks

This revision closes those gaps and defines an execution-ready runbook.

## Locked Decisions

- Do not copy `claw-xiaoice`'s dual-tunnel default.
- Default topology is one ngrok tunnel only: `video-callback -> VIDEO_TASK_SERVICE_PORT` and the default port remains `3105`.
- Do not depend on `/home/.../.openclaw`, `~/.openclaw`, or any repo-external cache directory.
- Do not commit ngrok credentials, fixed public URLs, or developer-specific filesystem paths.
- Keep `package.json` as `private: true`; public GitHub distribution does not require npm publish.
- Reuse the existing service admin endpoint `PUT /v1/admin/config` to update `callbackPublicBaseUrl`; do not add a second callback-sync mechanism.
- Prefer Node-based utility scripts as the main implementation so the workflow is usable on macOS, Linux, and Windows/WSL. Shell wrappers are optional, not primary.
- Continue treating `VIDEO_CALLBACK_PUBLIC_BASE_URL` as a supported manual mode variable. When ngrok bootstrap is enabled, runtime scripts overwrite the active callback URL through the admin API.

## Runtime Contract

The implementation must add the following user-facing environment variables to `.env.example`:

- `VIDEO_USE_NGROK=false`
- `NGROK_BIN=ngrok`
- `NGROK_API_URL=http://127.0.0.1:4040`
- `NGROK_AUTHTOKEN=`
- `NGROK_DOMAIN=`
- `NGROK_REGION=`

Preflight assumptions for local bootstrap:

- Node.js `>=22`
- ngrok CLI installed and available in `PATH` (or explicitly set via `NGROK_BIN`)
- first-time user runs `ngrok config add-authtoken <token>` unless `NGROK_AUTHTOKEN` is provided in `.env`
- `.env` contains non-empty and non-weak values for `VIDEO_SERVICE_INTERNAL_TOKEN`, `VIDEO_SERVICE_ADMIN_TOKEN`, and `VIDEO_SERVICE_CALLBACK_TOKEN`

The implementation must keep these existing variables as the main service contract:

- `VIDEO_TASK_SERVICE_HOST`
- `VIDEO_TASK_SERVICE_PORT`
- `VIDEO_SERVICE_INTERNAL_TOKEN`
- `VIDEO_SERVICE_ADMIN_TOKEN`
- `VIDEO_SERVICE_CALLBACK_TOKEN`
- `VIDEO_CALLBACK_PUBLIC_BASE_URL`
- `XIAOICE_VIDEO_STATE_DIR`

The implementation must store runtime artifacts under `XIAOICE_VIDEO_STATE_DIR`, not the repo root:

- `${XIAOICE_VIDEO_STATE_DIR}/runtime/video-service.pid`
- `${XIAOICE_VIDEO_STATE_DIR}/runtime/video-service.log`
- `${XIAOICE_VIDEO_STATE_DIR}/runtime/ngrok.pid`
- `${XIAOICE_VIDEO_STATE_DIR}/runtime/ngrok-url.txt`
- `${XIAOICE_VIDEO_STATE_DIR}/runtime/ngrok.log`
- `${XIAOICE_VIDEO_STATE_DIR}/runtime/bootstrap.last.json`

If `XIAOICE_VIDEO_STATE_DIR` is relative, resolve it against the repository root before use so behavior matches current service state-path handling.

## Implementation Plan

### 1. Bootstrap Scripts

Add Node-based scripts under `scripts/` and expose them through `package.json`.

Recommended file split:

- `scripts/dev-utils.js` (env parsing, state dir resolution, health polling, process helpers)
- `scripts/dev-service.js`
- `scripts/dev-ngrok.js`
- `scripts/dev-ngrok-status.js`
- `scripts/dev-callback-sync.js`
- `scripts/dev-up.js`
- `scripts/dev-doctor.js`

Required commands:

- `npm run dev:service`
- `npm run dev:ngrok`
- `npm run dev:ngrok:status`
- `npm run dev:callback:sync`
- `npm run dev:up`
- `npm run dev:doctor`

Required behavior:

- `dev:service` starts `src/service/cli.js`, writes PID/log files into `${XIAOICE_VIDEO_STATE_DIR}/runtime`, and fails fast if `/health` does not come up.
- `dev:ngrok` starts a single tunnel for `VIDEO_TASK_SERVICE_PORT`, waits for `NGROK_API_URL/api/tunnels`, extracts the HTTPS public URL, and writes it to `ngrok-url.txt`.
- `dev:ngrok:status` reads `NGROK_API_URL/api/tunnels`, prints the current public URL, the bound local address, and the callback endpoint `${publicUrl}/v1/callbacks/provider`.
- `dev:callback:sync` reads `ngrok-url.txt` and calls `PUT /v1/admin/config` with `X-Admin-Token` to update `callbackPublicBaseUrl`.
- `dev:up` runs `dev:service`, then `dev:ngrok` when `VIDEO_USE_NGROK=true`, then `dev:callback:sync`, then prints the final service health URL and callback URL.
- `dev:doctor` verifies `/health`, ngrok API reachability, callback URL sync state, and callback endpoint reachability.

Command execution contract:

- all commands must print actionable remediation when failing and exit with non-zero status
- `dev:up` must be re-runnable; if service/ngrok is already healthy, scripts should reuse existing runtime instead of spawning duplicate background processes
- every command must log which state directory it resolved to (for deterministic debugging)
- secrets/tokens must never be printed in plain text

### 2. Ngrok Invocation Rules

Default command:

```bash
ngrok http ${VIDEO_TASK_SERVICE_PORT}
```

If `NGROK_DOMAIN` is set, the script must use a domain-aware invocation so reserved domains are supported.

If `NGROK_AUTHTOKEN` is set, the script must pass it into the ngrok process or configure the process environment for that run. If it is empty, the script must assume the user already ran `ngrok config add-authtoken` and must print a concrete remediation message if startup fails.

The script must not generate or write `~/.ngrok2/ngrok.yml` automatically. For public-repo distribution, mutating user-global ngrok config is out of scope.

Tunnel discovery rules:

- prefer the tunnel whose `config.addr` matches `http://127.0.0.1:${VIDEO_TASK_SERVICE_PORT}` or `localhost:${VIDEO_TASK_SERVICE_PORT}`
- only accept `https://` public URLs for callback base URL sync
- if multiple candidate tunnels exist, choose the first exact-port match and emit a warning

### 3. Service and Callback Sync

Do not change the service HTTP contract.

The bootstrap flow must rely on existing endpoints:

- `GET /health`
- `PUT /v1/admin/config`
- `POST /v1/tasks`
- `GET /v1/tasks/:taskId`
- `POST /v1/callbacks/provider`

The callback sync script must only update:

- `callbackPublicBaseUrl`

It must not rewrite provider credentials, `vhBizId`, or other runtime config fields.

Admin sync request contract:

- method: `PUT`
- path: `/v1/admin/config`
- auth header: `X-Admin-Token`
- body must be exactly `{ "callbackPublicBaseUrl": "<https-ngrok-url>" }`
- reject non-HTTPS callback URL in ngrok mode

### 4. Documentation Changes

Update:

- `README.md`
- `docs/04-deployment.md`

Add:

- `docs/08-ngrok-github-bootstrap-plan.md` (this file)
- `docs/09-ngrok-local-dev.md`

Documentation must include:

- first-time setup with `ngrok config add-authtoken`
- one-command bootstrap
- where runtime logs and cache files live
- how to inspect the current public callback URL
- how to recover when ngrok URL changes
- explicit warning that the current tool uses one tunnel only by default

### 5. Ignore Rules

### 5. Ignore Rules

Update `.gitignore` to exclude runtime state produced by the bootstrap flow:

- `data/`
- `*.pid`
- `*.log`
- any state-dir runtime cache files if a non-default state directory is used locally

The implementation must not rely on gitignored runtime artifacts already existing.

### 6. Delivery Phases (Execution Order)

Phase A: bootstrap utilities and scripts

- add Node scripts + runtime artifact writes
- wire npm commands
- basic happy-path manual check (`dev:service`, `dev:ngrok:status`)

Phase B: callback sync + doctor checks

- add `dev:callback:sync`, `dev:up`, `dev:doctor`
- enforce minimal admin update payload
- add operator-facing diagnostics and remediations

Phase C: docs + cleanup

- update `.env.example`, `.gitignore`, `README.md`, deployment docs
- add `docs/09-ngrok-local-dev.md`
- ensure clone-to-run path is documented end-to-end

Phase D: automated verification

- add/refresh tests listed below
- run `npm test` and keep CI independent from real ngrok/provider

## Test Plan

Add automated coverage for the bootstrap flow without depending on the real ngrok service in CI.

Required tests:

- starting the service helper writes runtime files under the configured state dir
- ngrok status parsing works from mocked `NGROK_API_URL/api/tunnels` JSON
- callback sync sends `PUT /v1/admin/config` with only `callbackPublicBaseUrl`
- `dev:up` stops with actionable errors when admin token, callback token, or ngrok startup is missing
- relative `XIAOICE_VIDEO_STATE_DIR` resolves correctly
- `dev:doctor` fails with actionable output when callback base URL does not match ngrok URL
- ngrok discovery prefers exact-port HTTPS tunnel when multiple tunnel entries are present

Manual acceptance criteria:

1. Fresh clone user runs `npm install`.
2. User copies `.env.example` to `.env`.
3. User runs `ngrok config add-authtoken <token>` once.
4. User runs `npm run dev:up`.
5. `GET /health` returns `ok`.
6. `dev:ngrok:status` prints a public HTTPS URL for port `3105`.
7. `dev:callback:sync` updates the service runtime config successfully.
8. A real task can be created and later reaches terminal state through the public callback URL.

## Rollback and Recovery

If the bootstrap scripts are broken on a local machine, operator can immediately fall back to manual mode:

1. stop local helper processes (`video-task-service`, `ngrok`)
2. set `VIDEO_USE_NGROK=false`
3. set `VIDEO_CALLBACK_PUBLIC_BASE_URL` manually in `.env`
4. run `npm run service` and continue without bootstrap helpers

Recovery from ngrok URL rotation:

1. run `npm run dev:ngrok` (or `npm run dev:up` when `VIDEO_USE_NGROK=true`)
2. run `npm run dev:callback:sync`
3. run `npm run dev:doctor` to verify `/health` + callback sync state

## Done Definition

This plan is complete only when all are true:

- required scripts exist and are exposed in `package.json`
- runtime artifacts are written under resolved `XIAOICE_VIDEO_STATE_DIR/runtime`
- docs match actual commands and env variables
- tests pass with mocked ngrok/provider dependencies
- fresh clone setup succeeds using only documented commands

## Non-Goals

- no dual-tunnel XiaoIce webhook bootstrap in this repository
- no automatic installation of the ngrok binary
- no automatic mutation of global ngrok config files
- no real ngrok or real provider dependency in CI
