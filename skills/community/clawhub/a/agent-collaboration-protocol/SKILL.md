---
name: agent-collaboration-protocol
description: Structured multi-agent collaboration for backend + frontend builds. Use when an orchestrator needs to coordinate a backend engineer and frontend engineer on the same feature. Triggered by multi-role build requests like "build a dashboard with an API and UI" or "create a full-stack feature" or any task requiring both backend (API, data, infra) and frontend (UI, templates, design) work.
---

# Agent Collaboration Protocol

## How It Works

Three roles collaborate through a shared workspace:

| Role | Responsibility |
|------|---------------|
| **Orchestrator** | Defines the contract, spawns both builders, verifies integration, merges |
| **Backend Engineer** | Writes API code, data models, infrastructure |
| **Frontend Engineer** | Writes UI components, templates, styles |

The contract lives in a `shared/build-{YYYYMMDD}/` directory on the filesystem. **The orchestrator MUST provide the full absolute path** (e.g. `/home/user/project/shared/build-{YYYYMMDD}/`) in all handoff messages — isolated subagent sessions do not resolve relative paths reliably. Both builders write to the same directory. The orchestrator inspects and merges when both are done.

## Workflow

### Step 1: Orchestrator Creates the Build Directory and Contract

```
shared/build-{YYYYMMDD}/
  SPEC.md           ← Integration contract (orchestrator writes)
  backend/          ← Backend Engineer writes here
  frontend/         ← Frontend Engineer writes here
  backend-log.md    ← Backend Engineer updates (own file, no conflicts)
  frontend-log.md   ← Frontend Engineer updates (own file, no conflicts)
  integration.md    ← Orchestrator merges findings here
```

Write `SPEC.md` with these sections:

```markdown
# SPEC: {Feature Name}

## Contract
- API base path, auth scheme, content type
- Data models (all entities, fields, types, relationships)
- Endpoints (method, path, request/response shapes)
- Shared constants (status enums, error codes, feature flags)
- Error format

## Routes
Backend Engineer implements these. Frontend Engineer consumes them.

## UI Components
Frontend Engineer builds these. Backend Engineer doesn't touch them.

## Shared Constants
Both agents use these. Status enums, error codes, UI state labels.

## Success Criteria
Observable behavior. Not "tests pass" — "user can log in and see calendar."
```

For the full spec template with examples, see `references/spec-template.md`.

### Step 2: Orchestrator Spawns Agents

Spawn two subagents with `sessions_spawn`:

**Backend Engineer:**
```
task: >
  Implement the API spec at {ABSOLUTE_BUILD_DIR}/SPEC.md.
  Write all backend code to {ABSOLUTE_BUILD_DIR}/backend/.
  Log your progress to {ABSOLUTE_BUILD_DIR}/backend-log.md.
  FIRST: Reply "ACK — confirmed build directory: {ABSOLUTE_BUILD_DIR}" before starting any work.
  IMPORTANT: Use the full absolute path for ALL file writes. Verify files exist after writing.
  Use {backend framework} (FastAPI, Express, etc.).
```

**Frontend Engineer:**
```
task: >
  Implement the UI for the spec at {ABSOLUTE_BUILD_DIR}/SPEC.md.
  Write all frontend code to {ABSOLUTE_BUILD_DIR}/frontend/.
  Use the API contract in SPEC.md for your fetch calls.
  Log your progress to {ABSOLUTE_BUILD_DIR}/frontend-log.md.
  FIRST: Reply "ACK — confirmed build directory: {ABSOLUTE_BUILD_DIR}" before starting any work.
  IMPORTANT: Use the full absolute path for ALL file writes. Verify files exist after writing.
  Use {frontend stack} (HTMX+Tailwind, React, etc.).
```

Set `mode: "run"` for one-shot completion.

**Handoff acknowledgment is mandatory.** Each agent must confirm receipt and verify the build directory path exists before beginning work. If an agent does not ACK within a reasonable window (< 2 minutes), re-spawn it. See `references/handoff-format.md` for the full handoff template.

> **Important: Identity comes from context, not the label.** The `label` parameter passed to `sessions_spawn` is a runtime tag for orchestrator tracking — it does NOT determine the agent's role. The subagent's role (Backend Engineer vs Frontend Engineer) is determined entirely by the orchestrator's context injection: the `task` message you provide tells the subagent what role to play, what files to write, and what contract to follow. Two subagents spawned with the same `label` can have completely different tasks and roles.

### Step 3: Both Build Simultaneously

**Backend Engineer writes to** `{ABSOLUTE_BUILD_DIR}/backend/`:
- Router/handler code
- Data models and schemas
- Config and infrastructure files
- Logs progress to `{ABSOLUTE_BUILD_DIR}/backend-log.md`

**Frontend Engineer writes to** `{ABSOLUTE_BUILD_DIR}/frontend/`:
- UI components / templates
- Styles and layout
- API client code
- Logs progress to `{ABSOLUTE_BUILD_DIR}/frontend-log.md`

Each agent has its own log file — **no simultaneous-write conflicts possible.**

### Step 4: Orchestrator Verifies and Merges

1. Read both `backend-log.md` and `frontend-log.md` for progress
2. Read `integration.md` for orchestrator notes
3. Inspect files in `backend/` and `frontend/`
4. Verify API responses match UI expectations
5. If mismatches found, follow the Recovery Protocol below
6. Verify against the [Verification Guide](#verification-guide)

### Step 5: Deploy & Activate

The build is not done until the server reads from the new build. Follow these steps **in order**:

**5a. Determine: full build or incremental?**

| Build Type | What it means | Action |
|------------|--------------|--------|
| **Full build** | The build directory contains ALL project files (new + existing) | Point server at new build directly |
| **Incremental build** | The build directory contains ONLY new/changed files | Integrate new files into the live tree first |

Most collaborative builds are **incremental** — the backend and frontend agents only write the files they changed.

**5b. Integrate incremental builds into the live tree**

Copy new files from the build directory into the active deployment path. Use your platform's copy tool (cp, rsync, robocopy) with flags that preserve existing files. Only overwrite files that changed.

After integration, verify the deployment is intact:
```bash
# Quick sanity: key endpoints still respond
curl -s -o /dev/null -w "%{http_code}" https://example.com/api/health
```

**5c. Point server at the new build (full builds)**

Update your server's deployment target to the new build directory. On Unix systems this is typically a symlink swap (e.g. `ln -snf build-{YYYYMMDD}/ current`). On other platforms, update the server configuration directly.

**5d. Configure server to use the deployment target**

Any server config that references build paths should point to the deployment target (e.g. `current/`), never to a date-stamped directory. This is a **one-time config change** — set it once, then only the target changes on each deploy.

Example pattern:
```python
# ✅ Correct — never needs updating after initial setup
TEMPLATES = Path("/home/user/project/deploy/current/frontend")

# ❌ Wrong — bakes in a date, breaks after every deploy
TEMPLATES = Path("/home/user/project/deploy/build-20260501/frontend")
```

**5e. Restart the service**

Restart your application server to pick up the new deployment. Use your platform's service manager (systemctl, supervisor, docker restart, etc.).

**5f. Create workspace shortcuts (once per project)**

Set up convenient access paths so the live deployment is easy to find and edit. On Unix: `ln -snf deploy/current/ ~/myproject`. On other platforms, create a shortcut or bookmark.

**5g. Verify deploy**
```bash
# Confirm the deployment target points to the new build
ls -la /path/to/deploy/current
# Check the server responds with the new code
curl -s https://example.com/health
```

## Recovery Protocol

When something goes wrong during a parallel build, follow these steps:

### Agent Crash or Timeout
1. Check if the agent produced any files before crashing
2. Read `integration.md` — did it log progress before failing?
3. Re-spawn the agent with the *same* task + a note: "Previous run crashed. Continue from where you left off. Read integration.md for progress so far."
4. If the agent crashes again on the same task, reduce scope — split the work into smaller pieces

### Build Mismatch (API ≠ UI)
1. Identify the specific mismatch (field names, response shape, auth flow)
2. Determine which side is correct by re-reading `SPEC.md`
3. Send a targeted correction to the *wrong* agent — not a full re-spawn, just: "Fix {specific thing}. The spec says {X} but your code does {Y}."
4. If both sides deviated from spec, update `SPEC.md` with the correct contract, then correct both

### Blocked Agent
1. Read the blocker in `integration.md`
2. If it's a dependency on the other agent's work (e.g., frontend needs an endpoint that backend hasn't built yet):
   - Check if backend's route handler exists even partially
   - If yes, tell frontend to mock the expected response shape from the spec
   - If no, tell frontend to stub the API client and proceed with placeholder data
3. If it's an external blocker (missing credentials, environment issue), alert the orchestrator's human

### integration.md Conflict
If both agents edit `integration.md` simultaneously and create a conflict:
1. Read both versions
2. Merge manually — keep both progress sections
3. Write the merged version back
4. Consider switching to a per-agent log format (see `references/integration-log.md`)

## Verification Guide

Before declaring the build complete, verify:

### Backend Verification
```bash
# Test each endpoint from the spec
curl -s http://localhost:8000/api/v1/{resource} | jq .
curl -X POST http://localhost:8000/api/v1/{resource} -d '{...}' | jq .
```

### Frontend Verification
- [ ] Loading state renders (spinner/skeleton)
- [ ] Empty state renders (no data message)
- [ ] Error state renders (actionable error message)
- [ ] Populated state renders (data from API)
- [ ] All user interactions work (click, submit, navigate)

### Integration Verification
- [ ] Frontend fetch calls match backend endpoint paths
- [ ] Request/response shapes match the spec
- [ ] Error responses display correctly in the UI
- [ ] Auth flow works end-to-end

## Setup Script

Run once per project to initialize the collaboration structure:

```
scripts/init_collab.sh /path/to/project
```

Creates `shared/` with template `SPEC.md` and `.gitignore`.

## Filesystem Conventions

Every deployed project follows a three-tier filesystem pattern:

| Path | Type | Purpose | Edit? |
|------|------|---------|-------|
| `shared/build-{YYYYMMDD}/` | Directory | Historical snapshot / rollback point | Read-only after deploy |
| `shared/current/` | Symlink → active build | The server's source of truth | Set via `ln -snf` during deploy |
| `~/<project>/` | Symlink → `shared/current/` | Your editing workspace | **This is where you edit** |

**Rules:**

1. **`shared/current/` is the heartbeat.** Every build deploy ends with an atomic symlink swap to `shared/current/`. The previous build is preserved as a dated snapshot.

2. **Server config uses `current`, never a date.** Any import, mount, or path reference in server code (e.g., `RTS_BASE`, template directories, static file mounts) points to `shared/current/`. This is set once and never changes.

3. **`~/<project>/` is the intuitive path.** All human-facing workspaces are symlinks to the deployment target. When you edit `~/myproject/frontend/...`, you are writing to the live build. No indirection.

4. **This pattern applies ONLY to projects deployed via `shared/build-*/`.** Server code edited directly in agent workspaces (e.g., `myagent/workspace/`) does not use the `shared/current/` symlink — those directories ARE the live paths already.

5. **⚠️ Symlink swap replaces the entire tree.** `ln -snf` does not merge — it atomically points `current` at a new destination. If the new build only contains the files that changed (incremental build), the server will lose access to all other files. Always integrate incremental builds into the live tree (Step 5b) before changing the deployment target.

**Common pitfall:** You add a login page to `build-20260508/` and swap `current` to it. The login page works, but every other page returns 404 because the new build directory doesn't contain them. This is the #1 deploy-time failure mode.

**Rollback procedure:**

If the new build is broken, point your deployment target back to the last known good build directory, then restart the service. On a Unix system using symlinks:

```bash
ln -snf /path/to/deploy/build-{PREVIOUS_DATE}/ /path/to/deploy/current
# Then restart your service via your platform's service manager
```

The dated build directories are your safety net — each one is a complete, verifiable snapshot you can roll back to instantly.

## Reference Files

For deeper patterns and templates:
- `references/spec-template.md` — Full SPEC.md template with examples
- `references/integration-log.md` — integration.md status format
- `references/handoff-format.md` — Task handoff message template

## When This Pattern Applies

Use the full protocol (build dir → verify → symlink deploy) when:
- A feature requires both backend and frontend code changes
- The project is deployed from `shared/build-*/` directories
- The server reads templates/static files from a separate frontend path

Do NOT use when:
- Single-file changes (just do it directly)
- Bug fixes that are purely backend or purely frontend
- Tasks where one agent can handle both sides (use a single subagent instead)
- Server-side code in `workspace-*/` directories (those are the live paths; no build/deploy step needed)
- Config-only changes (feature flags, environment variables)

## Limitations

- Requires the `sessions_spawn` tool (OpenClaw v1.0+)
- Works best with model pairs that have complementary strengths (e.g., backend-specialized + frontend-specialized)
- Not a replacement for a design system — frontend engineer should have access to design tokens separately