---
name: fix-plan
description: |
  fix_plan.md / checklist.md schema and lifecycle management. Topics — format ([ ]/[x]/[BLOCKED] markers, Progress/Completed sections), priority (P0-P3 GitHub-aligned BLOCKED suffix + external/selfable reason classification), add (Action/Why/How authoring), draft (record a deferred plan stub when full planning is postponed → promote via code-workflow), move ([x] → Completed summary, subtree partial completion), sync (gh pr/issue state polling → auto-check), issue-drafts (write → publish → archive → delete lifecycle). Default (no args): dispatch to configured archive-receiver `<skill>:<topic>` (e.g., weekly report, RAG store) to harvest Completed section + remove from source; falls back to move topic when no receiver registered. Use when: "fix_plan", "checklist", "BLOCKED priority", "triage blocked", "fix-plan sync", "issue draft cleanup", "plan draft", "defer plan", "fix-plan draft", "fix-plan default", "fix-plan archive".
metadata:
  author: es6kr
  version: "0.1.0"
depends-on:
  - code-workflow
  - github-flow
allowed-tools:
  - Read
  - Edit
  - Write
  - Grep
  - Bash(gh:*)
  - Bash(mv:*)
  - Bash(mkdir:*)
---

# Fix Plan

Schema and lifecycle management for `fix_plan.md` (Ralph convention) and `checklist.md` (non-Ralph workspaces). Vendor-agnostic — extracted from Ralph integration to be reusable across environments.

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| format | Schema: `[ ]` / `[x]` / `[BLOCKED]` markers, Progress/Completed sections, item state changes, section-consistency check | [format.md](./format.md) |
| priority | `[BLOCKED:P0-P3:reason]` GitHub-aligned priority suffix + `external` / `selfable` reason classification + triage workflow | [priority.md](./priority.md) |
| add | New item authoring schema (Action / Why / How), length budget, deliverable separation (research / plan / checklist split) | [add.md](./add.md) |
| draft | Record a deferred plan **stub** (purpose + defer reason + resume trigger + expected deliverable) in `## Plan Drafts` when full planning is postponed; promote to `code-workflow` research→plan when the trigger fires. Invoked `/fix-plan draft` | [draft.md](./draft.md) |
| move | `[x]` → Completed summary rules, subtree-move partial completion under unfinished parent, optional abstract RAG dispatch | [move.md](./move.md) |
| sync | GitHub PR/Issue state polling (`gh pr view` / `gh issue view`) → auto-check `[ ]` → `[x]` on MERGED PR or CLOSED issue; PR CLOSED-without-merge → `[BLOCKED:P2:external]` | [sync.md](./sync.md) |
| issue-drafts | Issue Drafts lifecycle: write → publish → archive (`.bak/`) → delete from fix_plan | [issue-drafts.md](./issue-drafts.md) |

## Topic Dependencies

```text
fix-plan (schema + lifecycle)
  ├─→ (default, no args) → archive-receiver dispatch (caller-supplied) — falls back to move
  ├─→ format (entry — section structure + markers)
  ├─→ priority (new convention — BLOCKED P0-P3 + reason)
  │     └─→ depends on sync (Step 0: refresh external state before classifying)
  ├─→ add (authoring act-now items)
  ├─→ draft (deferred plan stub → `## Plan Drafts`)
  │     └─→ code-workflow/steps dispatch on promote (research → plan)
  ├─→ move (completion → Completed)
  │     └─→ optional --rag=<skill>:<topic> dispatch for semantic indexing (caller-supplied)
  ├─→ sync (GitHub state polling) — depends on github-flow gh CLI conventions
  └─→ issue-drafts (lifecycle of draft files)
```

- All topics are independently invocable, **except `priority` which invokes `sync` as Step 0 (HARD STOP)** — triage on stale state is the failure mode the dependency prevents (see [priority.md](./priority.md) Triage workflow Step 0)
- **Default invocation (no args)** dispatches Completed section to a caller-supplied archive-receiver (`--archive=<skill>:<topic>`); if no receiver is registered, falls back to in-tracker `move` (Completed cleanup only). See "Default invocation" section
- `move` topic optionally dispatches to a RAG receiver if the caller supplies `--rag=<skill>:<topic>` — generic skill stays vendor-agnostic; receiver implementation lives in the caller (e.g., ralph wrapper)
- `sync` topic uses `gh` CLI per `github-flow` skill's conventions
- `draft` topic dispatches to `code-workflow` (`steps`) on promote — turns a deferred stub into a real research → plan

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `archive-receiver` | (unset) | Optional `<skill>:<topic>` dispatch for **default invocation** (no args). When set, the caller routes the source's `## Completed` section to this receiver for external archiving (weekly report, postmortem log, RAG store, etc.). Receiver harvests + appends to its own report + removes harvested lines from source. Set via `--archive=<skill>:<topic>` CLI flag. See "Default invocation" below |
| `rag-receiver` | (unset) | Optional `<skill>:<topic>` dispatch for `move` topic semantic indexing — set via the `--rag=<skill>:<topic>` CLI flag on the `move` topic (see [move.md](./move.md)). No env var or config file is consumed by this skill; the caller routes |
| `task-tracker` | `fix_plan.md` | Tracker filename. Use `checklist.md` for non-Ralph workspaces |

## Default invocation (no args)

When `/fix-plan` is invoked with **no args**, dispatch to the configured **archive receiver** to harvest the `## Completed` section into an external report and remove the harvested items from the source tracker. If no receiver is registered, fall back to the `move` topic (in-tracker Completed cleanup only).

### Receiver contract

The fix-plan skill stays vendor-agnostic — no hardcoded receiver name. The caller (Claude in the user's environment) routes to whichever receiver is registered.

| Field | Value |
|-------|-------|
| Dispatch flag | `--archive=<skill>:<topic>` (CLI) |
| Receiver responsibility | (1) Read source's `## Completed` section, (2) Append items to its own report format, (3) Edit source to remove harvested lines |
| Idempotency | Receiver must be safe to re-invoke — already-harvested items must not double-append |
| Failure handling | If receiver unavailable / errors → log + fall back to `move` topic without touching source |

### Caller auto-dispatch heuristic

The caller decides at invocation time:

1. Check `--archive=<skill>:<topic>` CLI arg → if present, use it
2. Otherwise scan registered skills for a Completed-archive contract (matching topic name or declared `fix-plan-archive` keyword in description)
3. Exactly one match → dispatch automatically
4. Multiple matches → ask the user
5. Zero matches → fall back to `move` topic

### Example receivers (illustrative — not bundled)

The following are environments in which an archive receiver might be registered:

| Environment | Receiver pattern | What it does |
|-------------|-----------------|--------------|
| Weekly-report workflow | a topic that ingests fix_plan Completed into weekly reports | Append by ISO-week + remove from source |
| Postmortem log | a topic that appends to a rolling postmortem document | Append + remove |
| RAG store | a topic that upserts Completed entries into a vector DB | Upsert + remove |

These are **examples**, not dependencies. The fix-plan skill does not import any of them; the caller supplies the receiver.

## Quick Reference

### Default invocation

```bash
/fix-plan                            # dispatch to configured archive-receiver (or fall back to move)
/fix-plan --archive=<skill>:<topic>  # explicit receiver
```

See "Default invocation (no args)" section above.

### Schema (format)

```markdown
# Fix Plan

## Progress

- [ ] {Action}
  - **Why**: {motivation}
  - **How to apply**: {procedure}
- [BLOCKED:P0:external] {Action} (awaiting X)
- [x] {Completed item — pending move}

## Completed

- 2026-06-07 12:00 — {one-line summary} (commit {sha}, PR #{N})
```

See [format.md](./format.md) for full schema.

### BLOCKED priority + reason (priority — NEW convention)

```markdown
- [BLOCKED:P0:external] PR #45 user merge decision
- [BLOCKED:P1:selfable] consolidate Step 2.4 PR create (branch + body ready)
- [BLOCKED:P2:external] CodeRabbit re-review awaiting
```

- **P0**–**P3**: GitHub priority label-aligned (P0 highest)
- **external**: true external dependency
- **selfable**: progressable now (P-rank for immediate action)
- **Triage Step 0 — sync external state first (HARD STOP)**: `/fix-plan priority` invokes `sync` topic before classifying — `gh pr view <N>` + `gh issue view <N>` on every referenced PR/Issue. Auto-resolves merged/closed entries to `[x]` so stale items don't get sorted as live BLOCKERs

See [priority.md](./priority.md) for full convention.

### Add new item

```markdown
- [ ] {one-sentence Action}
  - **Why**: {motivation 1-2 sentences}
  - **How to apply**: {procedure / tools / commands}
```

See [add.md](./add.md) for length budget + deliverable separation.

### Record a deferred plan draft

```markdown
## Plan Drafts

- [BLOCKED:P2:selfable] {Purpose — one line}
  - **Defer reason**: {why postponed}
  - **Resume trigger**: {what promotes it}
  - **Expected deliverable**: research | plan | checklist
```

Invoked `/fix-plan draft`. Stub only (no full plan) → promote to `code-workflow` research→plan when the trigger fires.

Plan Drafts are **always** `[BLOCKED:P*:selfable]`, never `[ ]` — `[ ]` would let autonomous loops (e.g. Ralph wrapper) act on the entry, but promote requires a user decision. The reason is always `:selfable` (body file ready, waiting on a user signal, not on a third party). Priority `P0`-`P3` ranks promote urgency relative to other drafts. See [draft.md](./draft.md) and [priority.md](./priority.md).

### Move to Completed

After `[x]` checked, summarize to one line + move to Completed section. See [move.md](./move.md).

### Sync GitHub state

```bash
gh pr view <N> --json state,mergedAt   # PR
gh issue view <N> --json state,closedAt # Issue
```

MERGED PR or CLOSED issue → auto `[x]`. PR CLOSED-without-merge → `[BLOCKED:P2:external]`. See [sync.md](./sync.md).

### Issue Drafts lifecycle

`issue-drafts/<slug>.md` → `gh issue create` → archive to `.bak/` → delete from fix_plan. See [issue-drafts.md](./issue-drafts.md).

## See Also

- `github-flow` (depends-on) — `gh` CLI conventions for sync + register
- Ralph integration is a separate workstream maintained outside this published skill. A Ralph wrapper, when present, owns Ralph-specific concerns: the `## REPEAT` persistent-item section, autonomous-loop `[BLOCKED]` skip semantics, and the caller-side `--rag=<skill>:<topic>` dispatch (this skill exposes only the abstract flag contract). See the Ralph project's documentation for wrapper details
