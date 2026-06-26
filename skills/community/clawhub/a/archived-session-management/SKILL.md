---
name: archived-session-management
description: Implement, extend, or repair archived-session browsing in OpenClaw Control UI. Use when adding or fixing Archived Sessions / Recent Archived Sessions UI, archived search, resume / restore flows, session-history DB filters, live-session rebind logic, archive-state reconciliation, or session lifecycle cleanup for OpenClaw chat sessions.
---

# Archived Session Management

Implement archived-session UX as an end-to-end feature, not a single-button patch. Archived session work spans the Control UI, gateway RPC handlers, transcript file moves, the `session_history` SQLite index, and the live `sessions.json` store.

## Core workflow

1. **Inspect the whole chain first**
   - UI list/search rendering
   - gateway methods for `sessions.archived`, `sessions.resume`, `sessions.deleteArchived`
   - archive/restore helpers in `src/gateway/session-archive.ts`
   - history DB filters in `src/config/sessions/history-db.ts`
   - live session store behavior in `sessions.json`

2. **Treat these as separate failure classes**
   - archived list cannot find a real session
   - archived list finds the session but resume fails
   - resume works but opens the wrong live session
   - session vanishes from both Live and Archived due to DB/store drift

3. **Fix backend truth before UI polish**
   - Make archived search and restore semantics correct.
   - Then wire or refine UI buttons, copy, filters, and pagination.

4. **Reconcile legacy/inconsistent rows when needed**
   - Archived session features often fail because the DB, transcript path, and live store disagree.
   - Be tolerant in reads, then repair writes so future rows stay consistent.

## Required implementation areas

### 1. Archived-session search

Archived search must match more than just friendly labels. Include at least:
- `sessionId`
- `sessionKey`
- `displayName`
- `firstMessage`
- `agentId`
- `channel`
- `chatType`
- `status`
- `filePath`

When filtering archived sessions, do not rely on `status = 'archived'` alone. Legacy rows can still be archived-discoverable when:
- `archivedAt IS NOT NULL`, or
- `filePath` points into `/sessions/archive/`

Read `references/implementation-map.md` before editing the query layer.

### 2. Restore / resume behavior

Restoring an archived session must be **idempotent**.

Handle all three cases:
- transcript exists only in archive → move it back to active sessions dir
- transcript already exists in active sessions dir → do not fail; repair metadata and continue
- transcript exists nowhere → return not found

When restore succeeds, update the history row so it reflects the active transcript path and active status.

### 3. Rebind restored sessions into a unique live key

Do **not** resume old archived main sessions into `agent:main:main`.

Older rows often store that key, which causes the UI to jump back into the current main thread instead of the restored transcript.

Bind restored transcripts to a distinct live key such as:
- `agent:<agentId>:archive-<sessionId>`

Then write that binding into the live session store so the session actually appears in Live and can be opened by URL.

### 4. UI expectations

Archived-session UI should include:
- Archived tab / section
- search box
- Resume button
- Delete action for archived transcripts when supported
- loading / empty states that are specific enough to debug

If the repo already has the UI shell, wire it to the corrected backend instead of rebuilding it.

## Debugging checklist

When a user says an archived session is broken, verify all four:

1. **History row exists** in `session_history`
2. **Transcript file exists** at the path the row expects, or at the active fallback path
3. **History row status/path fields are coherent**
4. **Live store contains a session binding** after resume

If a session is in neither Live nor Archived, suspect DB/store drift immediately.

## File map

Read `references/implementation-map.md` for the concrete OpenClaw file map, bug patterns, and example fixes.

## Delivery standard

When work is complete, report:
- what failed
- which layer was wrong (UI, restore logic, DB filter, store binding, or mixed state)
- what changed
- whether a rebuild / gateway restart is needed
