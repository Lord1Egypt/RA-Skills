# Archived Session Management Implementation Map

## Scope

This reference captures the OpenClaw implementation points involved in archived-session UX and the concrete fixes needed when archived sessions fail across search, restore, or resume.

## Main files

### Backend / data layer

- `src/config/sessions/history-db.ts`
  - archived listing query
  - search fields
  - active vs archived filtering
  - status update helpers

- `src/gateway/session-archive.ts`
  - archive transcript to history
  - restore transcript from history
  - path reconciliation between active and archive dirs

- `src/gateway/server-methods/sessions.ts`
  - `sessions.archived`
  - `sessions.resume`
  - `sessions.deleteArchived`
  - live store rebind after restore

### UI layer

- `ui/src/ui/controllers/sessions.ts`
  - archived-session list loading
  - delete / rename / resume controller wiring

- `ui/src/ui/views/sessions.ts`
  - Archived tab table
  - search input
  - Resume button
  - empty/loading states

- `ui/src/ui/app-render.ts`
  - session view wiring
  - archived resume callback

## Failure patterns and fixes

### 1. Exact UUID search returns nothing

**Symptom**
- User pastes a real archived `sessionId`
- Archived search shows no results

**Root cause**
- Archived search query only checks friendly fields like `displayName`, `firstMessage`, and `sessionKey`
- It does not search `sessionId`

**Fix**
Expand the archived search query to include:
- `sessionId`
- `sessionKey`
- `displayName`
- `firstMessage`
- `agentId`
- `channel`
- `chatType`
- `status`
- `filePath`

### 2. Archived session exists but is filtered out

**Symptom**
- Session is known to exist in `history.db`
- Archived tab still misses it

**Root cause**
- Query filters only on `status = 'archived'`
- Legacy or inconsistent rows may still be archived because:
  - `archivedAt` is set, or
  - `filePath` still points into `/sessions/archive/`

**Fix**
When filtering archived sessions, treat these rows as archived-discoverable:
- `status = 'archived'`
- `archivedAt IS NOT NULL`
- `filePath LIKE '%/sessions/archive/%'`

### 3. Resume says “Session not found in archive”

**Symptom**
- Archived row is visible
- Clicking Resume returns not found

**Root cause**
- DB row points to archive path
- real transcript has already moved back to active sessions dir
- restore code only checks archive path and fails hard

**Fix**
Make restore idempotent:
- if archive file exists and active file does not → move archive file back to active path
- if active file already exists → treat as already restored and repair metadata
- if neither path exists → return not found

### 4. Resume opens the current main chat instead of the archived chat

**Symptom**
- Resume succeeds
- UI navigates back into current main session

**Root cause**
- older main-session archived rows carry `sessionKey = agent:main:main`
- restore returns that same key
- UI obediently opens current main thread

**Fix**
After restore, bind the transcript to a distinct live session key, for example:
- `agent:<agentId>:archive-<sessionId>`

Write that key into the live store and return it from `sessions.resume`.

### 5. Session disappears from both Live and Archived

**Symptom**
- user cannot find the session anywhere
- transcript file still exists on disk

**Root cause**
- half-restored / half-archived drift:
  - history DB says active
  - live `sessions.json` has no binding
  - transcript file still exists

**Fix**
Rebind the transcript into the live session store with a distinct key and repair the history row.

## Concrete backend behaviors to preserve

### `history-db.ts`

Implement archived discovery with tolerant archived filtering and broad search fields.

Also ensure `updateSessionStatus(..., 'active')` clears `archivedAt` so rows do not remain half-archived after restore.

### `session-archive.ts`

On restore:
- compute active transcript path from basename
- allow fallback when active transcript already exists
- persist repaired row via `indexSession(...)`
  instead of only flipping status

### `server-methods/sessions.ts`

On `sessions.resume`:
- call restore helper
- generate unique live session key for restored transcript
- resolve live session store target
- write a live session-store entry for the restored transcript
- respond with the restored key, not `agent:main:main`

## Operational notes

- Rebuild the repo after source changes.
- Restart the gateway after applying runtime-facing session/archive changes.
- If old rows are already corrupted, run a one-off reconciliation pass against `history.db` and/or `sessions.json`.

## Good user-facing explanation

When reporting fixes, separate the failure into one of these buckets:
- search problem
- archived filter problem
- restore path problem
- live-session binding problem
- mixed-state corruption across multiple layers
