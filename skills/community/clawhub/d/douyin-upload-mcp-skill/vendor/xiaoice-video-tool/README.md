# XiaoIce Video Tool

Standalone self-hosted XiaoIce video task toolchain with:

- `video-task-service` (HTTP API + SQLite task state + provider callback)
- `mcp-server` (single MCP tool: `xiaoice_video_produce`)

Current stage: **Phase 4 (shared client + OpenClaw plugin + `vhBizId` hard cut, in progress)**.

## Phase 1 Goals

- Bootstrap repository structure
- Initialize version control workflow
- Add base docs and package metadata
- Prepare parallel feature development with `git worktree`

## Phase 2 Service Run (WIP)

Phase 2 focuses on `video-task-service` extraction and standalone runtime.

```bash
npm install
cp .env.example .env
npm run service
```

Key environment variables:

- `VIDEO_TASK_SERVICE_HOST`: bind host for task service (default `127.0.0.1`)
- `VIDEO_TASK_SERVICE_PORT`: HTTP listen port for task service
- `VIDEO_SERVICE_INTERNAL_TOKEN`: internal auth token for service callers
- `VIDEO_SERVICE_ADMIN_TOKEN`: reserved admin/debug auth token
- `VIDEO_SERVICE_CALLBACK_TOKEN`: provider callback auth token
- `VIDEO_CALLBACK_PUBLIC_BASE_URL`: public callback base URL returned to provider
- `XIAOICE_VIDEO_STATE_DIR`: local task/state persistence directory
- `VIDEO_PROVIDER_API_BASE_URL`: XiaoIce provider API base URL
- `VIDEO_PROVIDER_API_KEY`: XiaoIce provider API key
- `VIDEO_PROVIDER_VH_BIZ_ID`: default `vhBizId` mapped to provider `vhBizId`
- `VIDEO_PROVIDER_AUTH_HEADER`: provider auth header name (default `X-API-Key`, some XiaoIce environments require `subscription-key`)

`npm run service` starts only the service process. MCP stdio is available separately via `npm run mcp` and uses `XIAOICE_VIDEO_SERVICE_BASE_URL`.

## Required Credentials (Where They Come From)

Before you can create real video tasks, you must configure two credential groups in `.env`.

### 1) Local service auth tokens (you generate these yourself)

These are not issued by XiaoIce or ngrok. They are internal secrets for this tool:

- `VIDEO_SERVICE_INTERNAL_TOKEN`
- `VIDEO_SERVICE_ADMIN_TOKEN`
- `VIDEO_SERVICE_CALLBACK_TOKEN`

Generate strong random values locally, then paste into `.env`:

```bash
node -e "const c=require('crypto');const r=()=>c.randomBytes(24).toString('hex');console.log('VIDEO_SERVICE_INTERNAL_TOKEN='+r());console.log('VIDEO_SERVICE_ADMIN_TOKEN='+r());console.log('VIDEO_SERVICE_CALLBACK_TOKEN='+r());"
```

### 2) XiaoIce provider credentials (from XiaoIce platform/business config)

- `VIDEO_PROVIDER_API_BASE_URL`: provider endpoint base URL assigned for your environment
- `VIDEO_PROVIDER_API_KEY`: API key issued by XiaoIce platform
- `VIDEO_PROVIDER_VH_BIZ_ID`: business id (`vhBizId`) issued by XiaoIce business side
- `VIDEO_PROVIDER_AUTH_HEADER`: header name required by your provider environment for the API key

In the currently verified environment, this must be:

```env
VIDEO_PROVIDER_AUTH_HEADER=subscription-key
```

That means the service sends:

```http
subscription-key: <VIDEO_PROVIDER_API_KEY>
```

`vhBizId` is required in each `POST /v1/tasks` create request body.  
Service-side `VIDEO_PROVIDER_VH_BIZ_ID` remains a runtime config field for operational management, but create calls should always pass request-level `vhBizId`.

## Local ngrok Bootstrap (Fresh Clone)

Use this path when provider callbacks must reach your local service without manually editing callback URLs each time.

```bash
npm install
cp .env.example .env
ngrok config add-authtoken <your-token>
# set VIDEO_USE_NGROK=true and fill required service/admin/callback tokens in .env
npm run dev:up
```

Prerequisites:

- Node.js `>=22`
- ngrok CLI available in `PATH` (or set `NGROK_BIN` in `.env`)
- non-empty `VIDEO_SERVICE_INTERNAL_TOKEN`, `VIDEO_SERVICE_ADMIN_TOKEN`, and `VIDEO_SERVICE_CALLBACK_TOKEN`
- valid `VIDEO_PROVIDER_API_BASE_URL` and `VIDEO_PROVIDER_API_KEY`
- valid `VIDEO_PROVIDER_VH_BIZ_ID` in service config, and provide `vhBizId` in each task request
- correct `VIDEO_PROVIDER_AUTH_HEADER` for your environment (`subscription-key` in the verified environment)
- `VIDEO_USE_NGROK=true` when using bootstrap mode

Bootstrap command set:

- `npm run dev:service`
- `npm run dev:ngrok`
- `npm run dev:ngrok:status`
- `npm run dev:callback:sync`
- `npm run dev:up`
- `npm run dev:doctor`

Troubleshooting entry points:

- run `npm run dev:doctor` for health, ngrok, and callback sync diagnostics
- run `npm run dev:ngrok:status` to inspect the current public callback URL
- see `docs/09-ngrok-local-dev.md` for full local runbook
- see `docs/04-deployment.md` for manual callback URL fallback mode

## Phase 3 MCP Run (WIP)

After the service is running, start MCP stdio server:

```bash
XIAOICE_VIDEO_SERVICE_BASE_URL=http://127.0.0.1:3105 \
VIDEO_SERVICE_INTERNAL_TOKEN=dev-internal-token-change-me \
npm run mcp
```

MCP server currently supports:

- `initialize`
- `tools/list`
- `tools/call` with one tool: `xiaoice_video_produce`

OpenClaw native plugin planning is tracked in:

- `docs/07-openclaw-thin-plugin-plan.md` (Phase 4 milestones for native thin plugin adapter)

## Phase 4 Execution (In Progress)

Phase 4 has entered execution with three coordinated tracks:

- extract and reuse a shared service client across MCP and OpenClaw adapters
- add OpenClaw native thin plugin support under plugin identity `one-click-video`
- hard cut public field naming to `vhBizId` across docs, examples, and configuration

## Current Contract Freeze

The current Phase 2 contract is frozen by integration tests around the HTTP service boundary.

Verified behavior:

- `POST /v1/tasks` returns `202` with `status=submitted` and queues provider submission asynchronously.
- `GET /v1/tasks/:taskId` returns the current normalized task record, including timeout materialization on stale in-flight tasks.
- `POST /v1/callbacks/provider` accepts callback auth by `X-Callback-Token` header or `?token=` query parameter.
- provider payload mapping is stable for top-level `topic` / `vhBizId` and optional official fields, plus callback URL and `modelId` service-side injection.
- `PUT /v1/admin/config` updates runtime provider settings used by later task submissions.

Not frozen yet:

- live-provider callback payload variants beyond the normalized samples covered in tests
- exact oversized-request connection behavior under low-level socket termination
- end-to-end OpenClaw runtime loading/registration verification against production OpenClaw environment

## Version Control Workflow (Subagents + Worktree)

This repo uses one integration branch per phase, then one feature branch per subagent.

Recommended branch model:

- `main`: stable baseline
- `phase1/bootstrap`: Phase 1 integration branch
- `phase2/service-extraction`: Phase 2 integration branch
- `feat/p1-<scope>-<owner>`: subagent feature branches
- `feat/p2-<scope>-<owner>`: subagent feature branches

Example:

- `feat/p1-docs-agent-a`
- `feat/p1-package-agent-b`
- `feat/p1-scripts-agent-c`
- `feat/p2-service-agent-a`
- `feat/p2-tests-agent-b`

### 1) Initialize Git (once)

```bash
git init
git add .
git commit -m "chore: initialize xiaoice-video-tool baseline"
git checkout -b phase1/bootstrap
```

### 2) Create isolated worktrees for subagents

From repository root:

```bash
git worktree add ../xvt-agent-a -b feat/p1-docs-agent-a phase1/bootstrap
git worktree add ../xvt-agent-b -b feat/p1-package-agent-b phase1/bootstrap
git worktree add ../xvt-agent-c -b feat/p1-scripts-agent-c phase1/bootstrap
```

Each subagent works only in its own worktree and branch.

Helper scripts are available:

```bash
./scripts/worktree-add.sh --branch feat/p1-docs-agent-a
./scripts/worktree-list.sh
./scripts/worktree-remove.sh --branch feat/p1-docs-agent-a --delete-branch
```

### 3) Ownership rules

Assign non-overlapping file scopes:

- Agent A: `docs/**`
- Agent B: `package.json`, `.env.example`, `tests/**`
- Agent C: `scripts/**`, root helper scripts

Rules:

- Do not revert other branches' work.
- Keep commits small and focused.
- Open merge back to `phase1/bootstrap` only after local checks pass.

### 4) Merge back to phase branch

```bash
git checkout phase1/bootstrap
git merge --no-ff feat/p1-docs-agent-a -m "merge: phase1 docs bootstrap"
git merge --no-ff feat/p1-package-agent-b -m "merge: phase1 package bootstrap"
git merge --no-ff feat/p1-scripts-agent-c -m "merge: phase1 scripts bootstrap"
```

### 5) Cleanup worktrees

```bash
git worktree remove ../xvt-agent-a
git worktree remove ../xvt-agent-b
git worktree remove ../xvt-agent-c
git branch -d feat/p1-docs-agent-a feat/p1-package-agent-b feat/p1-scripts-agent-c
```

## Planned Layout

```text
xiaoice-video-tool/
  README.md
  CHANGELOG.md
  .env.example
  package.json
  docs/
  src/
    service/
    mcp/
    shared/
  scripts/
  tests/
```

## Development Method

- Architecture and API structure follow `backend-patterns`.
- Feature development follows `tdd-workflow` (tests first, then implementation).
