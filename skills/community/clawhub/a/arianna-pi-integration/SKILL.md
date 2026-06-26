---
name: arianna-pi-integration
description: 'Integrates the Playfilo shared-memory DAG into the pi-mono coding agent. Adds DAG persistence, time-travel tools (tobe, life, recall, trace), and cross-session memory.'
version: 0.1.0
metadata:
  openclaw:
    emoji: 🪡
    homepage: https://arianna.run
---

# Playfilo Integration Skill for Pi-mono

This skill integrates the Playfilo shared-memory DAG into the Pi coding agent. Apply the patches in order (steps 1–5), then run the verification checklist.

**Target codebase:** `pi-mono/packages/coding-agent/src/core/`
**Dependency:** `better-sqlite3` (already in pi-mono's dependencies)
**Shared DB:** `~/.playfilo/playfilo.db` (SQLite, WAL mode)

---

## Layout (post 2026-05-09 reorg)

This skill behaves as a small repo. Each top-level folder has a different role:

| Folder | Purpose | Who can write |
|---|---|---|
| `filo/` | **Frozen reference**. Original Filo-authored implementation. | Nobody (deprecated path) |
| `playtiss/` | **Canonical online implementation**. Backed by `@playtiss/core` instead of raw better-sqlite3. AIs merge collaborative contributions here. | Any graduated AI |
| `<ai-name>/` (e.g. `mirin/`, `pax/`) | **Per-AI worktrees**. Each AI's own data structures + integration approach + per-AI patches. | Only that AI |

**Authorship rules:**
- Each AI commits to their own worktree (`<ai>/**`) and to `playtiss/**` only
- Nobody commits to `filo/` (frozen) or to another AI's worktree
- `playtiss/patches/` filenames are content-describing (NOT AI-named); attribution lives in git history

If you're integrating a NEW graduated AI, create your own worktree (`<your-name>/` with README + patches/ + optional core/) and add patches to `playtiss/patches/` with neutral filenames.

If you're applying the integration for the first time on a clean pi-mono checkout, follow `filo/patches/` (the historical canonical reference) OR wait for `playtiss/core/` to land (the post-Dispatch-1 canonical).

---

## Architecture Overview

Playfilo adds a content-addressable Merkle DAG alongside Pi's native JSONL session files. Both the terminal agent (`playfilo_node.ts`) and Pi share the same SQLite database. Each agent writes nodes to the DAG through its own persistence path and maintains its own HEAD ref (`terminal_head` vs `PI_HEAD`).

**What the integration provides:**
1. **Shared memory** — Every Pi session entry is mirrored to the DAG as a content-addressed node
2. **DAG-based session recovery** — On resume, Pi loads history from the DAG instead of raw JSONL (preserving cross-agent branches)
3. **Temporal tools** — `life` (DAG visualization), `tobe` (time-travel), `recall` (deep inspection), `trace` (navigation log)
4. **System prompt injection** — Identity primer via Pi extension system

**Integration is fully additive** — no native Pi code is removed or fundamentally changed. All Playfilo code hooks into existing Pi patterns (custom tools, `_persist`, `setSessionFile`, extensions).

---

## Patch Steps

Apply in order. Each patch file is self-contained with exact code to add, where to add it, and a build verification command.

| Step | File | Patch doc | What it does |
|------|------|-----------|--------------|
| 1 | `playfilo-db.ts` (new) | [patches/01-playfilo-db.md](filo/patches/01-playfilo-db.md) | Build env setup (pnpm), copy DAG module, add dependency |
| 2 | `sdk.ts` | [patches/02-sdk-tools.md](filo/patches/02-sdk-tools.md) | Register 4 custom tools (tobe, life, recall, trace) |
| 3 | `session-manager.ts` | [patches/03-session-manager.md](filo/patches/03-session-manager.md) | Persistence shim, DAG read hook, PI_HEAD management |
| 4 | `agent-session.ts` | [patches/04-agent-session.md](filo/patches/04-agent-session.md) | Metadata wiring, auto-continue handler, SESSION_SWITCH |
| 5 | Extension file | [patches/05-extension.md](filo/patches/05-extension.md) | System prompt injection via Pi extension |

**Verification:** [filo/patches/verify.md](filo/patches/verify.md)
**Version-specific notes:** [filo/patches/versions/](filo/patches/versions/) — per-version adaptation docs (e.g. [v0.61.1](filo/patches/versions/v0.61.1.md))

---

## Bundled Source

The complete `playfilo-db.ts` is bundled at [`filo/playfilo-db.ts`](filo/playfilo-db.ts). Copy it to `packages/coding-agent/src/core/playfilo-db.ts` as step 1.

---

## Critical Implementation Notes

Read these before starting — they explain design decisions that aren't obvious from the patch code alone.

### playfilo-db.ts Design

- Module-level `db` singleton opened at import time (WAL mode)
- Schema V4 via `CREATE TABLE IF NOT EXISTS` (safe for concurrent access)
- All exports are pure functions operating on the module-level `db`

### Key Exports

| Function | Purpose |
|---|---|
| `hashContent(obj)` | SHA-256 of deterministic JSON (sorted keys) |
| `storeBlob(type, content)` | Content-addressable blob storage; returns hash |
| `getRef` / `setRef` / `clearRef` | Read/write/delete mutable refs (HEAD pointers) |
| `setTobeAbortState(messages, skips=2)` | Unified tobe abort: skip N DAG commits, freeze HEAD, stash context |
| `checkTobeAbortState()` | Called by `_persist()` — returns `true` to skip DAG commit |
| `consumePendingTobeContext()` | Called by auto-continue handler — returns stashed context |
| `loadEntriesFromDAG(startHash)` | Walk DAG backwards, reconstruct Pi `SessionEntry[]` |
| `commitNodeWithExternalId(...)` | Create DAG node with Pi UUID as `external_id` |
| `commitTobeDeparture(assistantHash, targetHash)` | Dead-end tool_result node for INCARNATE `from_node` |
| `setPendingIncarnateLog` / `consumePendingIncarnateLog` | Deferred INCARNATE logging with accurate hashes |
| `handleLife` / `handleRecall` / `handleTrace` | Tool handler implementations |

### loadEntriesFromDAG Shape Requirements

Must reconstruct Pi's exact `SessionEntry` shape:
- `AssistantMessage` needs `api`, `provider`, `model`, `stopReason`, `usage` fields
- `toolResult` blobs → Pi's `ToolResultMessage` shape
- `config_json` parsed for `provider`/`model`
- `external_id` used as entry `id` (falls back to hash prefix)

### Tobe V2: Eager Carryover Commit

The tobe handler commits the carryover node to the DAG and logs INCARNATE **eagerly** (inside the tool handler), then appends the carryover to the stashed context. No follow-up queue is used.

**Design spec and rationale:** [filo/patches/tobe-v2-spec.md](filo/patches/tobe-v2-spec.md)

**Handler flow (sdk.ts):**
1. `commitTobeDeparture(fromHash, targetHash)` — dead-end departure node for trace()
2. Build target context via `loadEntriesFromDAG` + `buildSessionContext`
3. `setRef("PI_HEAD", targetHash)` — point HEAD at target (before abort guard is active)
4. Commit carryover to DAG: `commitNodeWithExternalId(targetHash, "user", [blobHash], carryoverId)`
5. `setRef("PI_HEAD", carryoverHash)` — point HEAD at carryover
6. `logAction("INCARNATE", departureHash, carryoverHash, metadata)` — log immediately
7. `msgs.push(carryover)` — append to target context (no tail popping)
8. `setTobeAbortState(msgs)` — enable skip guard (2 skips for tool_result + aborted assistant)
9. `agent.abort()` — no `followUp()` calls

**Key ordering:** Steps 3–6 (DAG writes + PI_HEAD updates) must happen BEFORE step 8 (`setTobeAbortState`). The `setRef("PI_HEAD")` guard checks `tobeAbortState.skipsRemaining > 0` — setting the abort state first would block the PI_HEAD updates.

### Tobe Abort State

`setTobeAbortState` handles two concerns:
1. **Persist skip** — Skip 2 DAG commits (tool result + aborted assistant). `setRef("PI_HEAD")` also guarded while `skipsRemaining > 0`.
2. **Deferred context replacement** — Stashes `messages[]` for auto-continue handler → `agent.replaceMessages()`

**Why exactly 2 skips:** When tobe fires `agent.abort()` inside `executeToolCalls`, the inner loop iterates once more (`hasMoreToolCalls` still `true`). `streamAssistantResponse()` is called with the aborted signal, returns `stopReason === "aborted"`, and `runLoop` exits via `return` — before `getFollowUpMessages()` is reached. The 2 skipped events are:
1. Tool result (emitted during `executeToolCalls`)
2. Aborted assistant (emitted during the next `streamAssistantResponse` iteration)

**Safety cleanup:** When `skipsRemaining` reaches 0, a `setTimeout(0)` clears `tobeAbortState` if `consumePendingTobeContext` hasn't already nulled it. This prevents dangling state from corrupting the next session when a nested tobe's continuation is lost (e.g., host calls `dispose()` before `agent_end` is processed).

### Auto-Continue Handler (agent-session.ts)

The handler calls `continue()` **synchronously** (not via `setTimeout`). This is critical: after `_runLoop` ends, `agent.runningPrompt` is cleared. If the host calls `waitForIdle()` during cleanup, it resolves immediately. A `setTimeout`-deferred `continue()` would start after the listener is removed. Calling `continue()` synchronously ensures `_runLoop` sets `runningPrompt` before `_processAgentEvent` returns, so `waitForIdle()` blocks until the continuation completes.

```typescript
if (event.type === "agent_end") {
    const tobeCtx = consumePendingTobeContext();
    if (tobeCtx) {
        this.agent.replaceMessages(tobeCtx);
        this.agent.continue().catch(...);
        return; // skip retry/compaction
    }
}
```

### Parent Tracking

Uses `getRef("PI_HEAD")` directly. During tobe, PI_HEAD is set eagerly to the carryover hash (step 5). The abort state guard freezes it there. When the continuation's LLM response is committed via `_persist()`, it reads `PI_HEAD = carryoverHash` as parent → clean topology: `target → carryover → response`.

### Hash Hiding in life()

`nodeHasToolCalls()` replaces hashes with same-width spaces for any assistant node with tool_call blobs. This naturally hides HEAD (always the assistant making the life() call, with unpersisted tool_result). Agents cannot target these nodes via tobe.

### handleTrace Ancestor Walk

- Only shows actions whose `to_node` is in the current lineage
- SQL-level `action_type IN (...)` filtering so `LIMIT` counts visible events
- Filter modes: `default` (BOOT/INCARNATE), `switches` (+SESSION_SWITCH), `all` (+COMMIT)

---

## Schema

```sql
CREATE TABLE IF NOT EXISTS blobs (
  hash TEXT PRIMARY KEY, type TEXT NOT NULL, content TEXT NOT NULL, thought_signature TEXT
);
CREATE TABLE IF NOT EXISTS nodes (
  id TEXT PRIMARY KEY, parent_id TEXT, role TEXT NOT NULL, parts_list TEXT NOT NULL,
  timestamp INTEGER NOT NULL, config_json TEXT, thought_signatures TEXT,
  system_prompt_hash TEXT, external_id TEXT
);
CREATE TABLE IF NOT EXISTS refs (name TEXT PRIMARY KEY, node_id TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS action_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp INTEGER NOT NULL,
  action_type TEXT NOT NULL, from_node TEXT, to_node TEXT, metadata TEXT
);
CREATE INDEX IF NOT EXISTS idx_nodes_parent ON nodes(parent_id);
CREATE INDEX IF NOT EXISTS idx_nodes_external_id ON nodes(external_id);
```

---

## Maintenance Protocol

When making changes to the Playfilo integration:
1. Edit the source files in pi-mono
2. Update the relevant patch file and this index
3. Copy the updated `playfilo-db.ts` into this directory to keep it in sync
4. If a new tool is added, add it to `patches/02-sdk-tools.md` and `patches/verify.md`
5. If a new hook point is added, create a new patch file or extend the relevant one
