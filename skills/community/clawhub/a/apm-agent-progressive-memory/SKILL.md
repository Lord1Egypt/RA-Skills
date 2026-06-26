---
name: APM-agent-progressive-memory
description: "APM Protocol (Agent Progressive Memory): Progressive disclosure protocol for group chat AND DM (main session) memory."
---

# APM — Progressive Disclosure Protocol

APM supports **both group chat and private (main session DM)** memory management. The two structures are completely independent and do not interfere with each other.

## Group vs DM: Strategy Comparison

| Aspect | Group Chat | DM (Main Session) |
|-------|-----------|-------------------|
| **Memory path** | `memory/groups/{group_name}/` | `memory/main/` |
| **Loading** | 5-step progressive (index → P0 → P1 → P2 → P3) | 3-layer progressive (index → attention → longterm) |
| **Index file** | `memory/groups/{group_name}.md` | `memory/main/index.md` |
| **Priority files** | attention.md, project.md, experience.md, people.md | attention.md, longterm.md |
| **Entry rule** | Must read index first, no subdirectory bypass | Must read index first |
| **Flush trigger** | Per-group flush on `/remem` | Full-session flush on `/remem` |

**Key differences**:
- Group uses **5-step loading** with budget controls; DM uses simpler **3-layer**
- Group has **conventions/** sub-directory; DM does not
- DM reuses existing **MEMORY.md**; Group uses dedicated files
- Uninstaller: Group loses memory access; DM retains MEMORY.md

Agent must follow the **layered disclosure protocol** when accessing memory in group chats: read the index first, then load layers on demand.

## Core Rules

### 1. Entry Gate

- The **only legal entry point** for group chat memory is `memory/groups/{group_name}.md` (index file)
- **Forbidden**: directly reading any sub-files under `memory/groups/{group_name}/`
- **Forbidden**: bypassing the index to directly `memory_search` subdirectories
- **Group name mapping rule**: group chat room IDs must first be resolved via `memory/groups/group_names.json` to a friendly name `{group_name}` before use

### 2. Five-Step Loading Flow

| Step | Action | Output |
|------|--------|--------|
| 0. Group name mapping | Check `memory/groups/group_names.json`, convert room ID to `{group_name}` | Friendly name |
| 1. Route to index | `memory_get("memory/groups/{group_name}.md")` | Hard Rules + routing table |
| 2. Intent matching | Match current message to trigger scenario | File to load |
| 3. Explicit load | `memory_get("memory/groups/{group_name}/{file}.md")` | Actual memory content |
| 4. Sub-layer control | Load only if Step 3 file references `conventions/` | 1 sub-file max |
| 5. Budget circuit-breaker | Stop when cumulative tokens exceed `memory_budget` | Stop loading |

Only **one** best-matching file is loaded per session (highest priority wins).

### 3. Loading Discipline

- **Per group chat (5-step flow)**:
  - Step 3 loads **1 P-file** (highest-priority match) per session
  - Step 4 may load **1 sub-file** under `conventions/` (only if Step 3 referenced it)
  - **Total ceiling**: 2 P0–P2 files + 1 P3 file (per AGENTS.md layering)
- **Per DM session (3-layer flow)**:
  - Layer 0: `memory/main/index.md` (always)
  - Layer 1: up to **2 P-files** from attention/longterm/daily-synced/projects
- When switching group chats, clear old context first, then restart from Step 1

### 4. Write-Back on Updates

- New decision → append to `experience.md`
- Task status change → update `attention.md`
- Index files: append-only (mark deleted entries `[DEPRECATED]` instead of removing)

### 5. Memory Flush

| Trigger | Condition | Action |
|---------|-----------|--------|
| `/remem` | User manual trigger | Full flush |
| Pre-compact | Context near limit | Auto-flush before loss |
| Idle timeout | 30min inactive, no flush | One-time auto-flush |

### 6. Auto-Initialization on Missing Memory

> When a flush is triggered for a session whose memory system has **not yet been initialized**, the Agent must initialize it based on available information.

| Scenario | Action | Who does it |
|----------|--------|-------------|
| Group index missing (`memory/groups/{name}.md`) | Create from `memory/groups/group_names.json` + context; ask group "purpose" if first-join | `apm_session_start` hook skips injection; **agent** handles per AGENTS.md "First-Join Flow" |
| DM index missing (`memory/main/index.md`) | Create from `MEMORY.md` content | `apm_session_start` hook skips injection; **agent** handles per AGENTS.md "Every Session" |
| `memory/groups/group_names.json` missing | Create from existing room id list (if any) | Operator (out of band) |

**Initialization is not overwriting**: existing files are never overwritten — only created when completely absent.

> ⚠️ The `apm_session_start` hook handles the **read** side (skip injection if index missing → defer to agent). The **write** side (create the index) is always the agent's responsibility. The hook never writes to memory files.

## File Structure

```
memory/groups/
├── {group_name}.md          # L0: Entry gate (mandatory read)
└── {group_name}/             # Group memory (direct access forbidden)
    ├── attention.md          # P0: Current focus
    ├── project.md            # P1: Project static info
    ├── experience.md         # P2: Experience / decision log
    ├── people.md             # P3: People profiles
    └── conventions/          # L3: Detailed specifications
        ├── api.md
        └── ...

memory/main/                    # DM progressive disclosure
├── index.md                # L0: DM entry index
├── attention.md            # P0: Current tasks, blockers
├── longterm.md             # P1: MEMORY.md distilled summary
├── daily-synced.md         # P2: Daily notes summary
└── projects/               # P3: Project context
    └── {name}.md
```

## Priority Definitions

### Group Chat (P0–P3)

| Priority | File | Content | When to Load |
|----------|------|---------|--------------|
| P0 | `attention.md` | Active tasks, blockers | Any work conversation |
| P1 | `project.md` | Tech stack, architecture | Technical decisions |
| P2 | `experience.md` | Lessons learned | Search hit + append |
| P3 | `people.md` | Team roles, contacts | Need to find someone |

### DM (Main Session)

| Priority | File | Content | When to Load |
|----------|------|---------|--------------|
| P0 | `memory/main/attention.md` | Active tasks, blockers | Always (cold start) |
| P1 | `memory/main/longterm.md` | MEMORY.md distilled summary | When project context needed |
| P2 | `memory/main/daily-synced.md` | Daily notes summary | Recent activity context |
| P3 | `memory/main/projects/{name}.md` | Project-specific deep context | Project-specific questions |

> DM uses **3-layer progressive loading** (not 4-P like group): the
> index → attention → longterm, with daily-synced and projects/ loaded
> on-demand per the routing table in `memory/main/index.md`.

## MEMORY.md Discipline (v1.6.0)

> ⚠️ `MEMORY.md` is the **authoritative long-term memory** but must remain **lean and stable**.
> All project-level, event-level, and temporary information MUST go elsewhere.

### ✅ Allowed in MEMORY.md

| Category | Example | Reason |
|----------|---------|--------|
| Identity | Agent self-reference (role, style, principles) | Self-reference, stable |
| User basics | Name, timezone, tech stack | Rarely changes |
| Environment | Server host, key DB paths | Constants |
| Project index | One-liner per project → file | Pointer, not content |
| Other memory entry pointers | `memory/main/...`, `memory/groups/...` | Routing only |

### ❌ Forbidden in MEMORY.md

| Category | Where it goes instead |
|----------|----------------------|
| Project progress | `memory/main/projects/{name}.md` |
| Event logs (incident, fix) | `memory/YYYY-MM-DD.md` |
| Decisions & lessons | `memory/main/longterm.md` |
| Tool lists (iqtree, bcftools...) | Runtime `which` / `command -v` |
| Group chat metadata | `memory/groups/{name}.md` |
| Temporary fix instructions | Daily notes (auto-rotate) |
| Cross-snapshot result narratives | Project report files |

### Rule of Thumb

> - If a new agent could figure it out from `ls` or `which`, **don't write it to MEMORY.md**.
> - If it's about a specific project, **write to `projects/{name}.md`**.
> - If it changes more than once a month, **don't put it in MEMORY.md**.
> - If `MEMORY.md` exceeds 50 lines, **it's bloated** — extract project details.

### MEMORY.md Anti-Pattern

```
❌ 95 lines of "long-term memory" with project details
❌ Tool lists that `which` can answer
❌ Temporary fix notes lingering in MEMORY.md a month later
❌ Group names listed directly
❌ Event outcomes with specific samples or measurements

✅ 30-line identity + index
✅ Project index table → projects/{name}.md
✅ Key events → daily notes + longterm index
✅ Group chats → memory/groups/{name}.md
```

## File Templates

All file templates (MEMORY.md, projects/{name}.md, longterm.md, group index, attention) live in **ADDENDUM.md** → "File Templates" section. Use them as starting points.

## DM Entry Loading (to add in AGENTS.md)

```markdown
## Every Session

1. Read `SOUL.md` → USER.md → MEMORY.md
2. **If in MAIN SESSION** (DM):
   - Read `memory/main/index.md` — DM progressive index
   - Based on routing, load up to 2 files
   - Report `last flush: YYYY-MM-DD HH:mm` (from `memory/flush-state.json` — DM-only)
3. Read `memory/YYYY-MM-DD.md` (today + yesterday)
```

> ⚠️ The `flush-state.json` referenced here is the **DM** flush state
> (`memory/flush-state.json`), NOT the group one. See "Flush State Files"
> above for the two-file split.

## Flush State Files

APM uses **two separate flush-state files** to keep DM and group memory
isolated:

| File | Scope | Owner |
|------|-------|-------|
| `memory/flush-state.json` | DM (main session) | `remem-flush`, `precompact-remem`, `apm_session_start` (DM path) |
| `memory/groups/flush-state.json` | Group chat | `remem-flush`, `precompact-remem`, `apm_session_start` (group path) |

This separation is a **privacy boundary** — group sessions must never
read or write the DM flush-state (and vice versa).

### `memory/flush-state.json` (DM)

```json
{
  "last_flush_time": "2026-06-20T17:20:23+08:00",
  "flush_number": 6,
  "context_usage_at_flush": null,
  "pending_items": [],
  "<file>_mtime": "ISO-8601"  
}
```

### `memory/groups/flush-state.json` (group)

Same shape, scoped to one group. Multiple groups each have their own
flush-state under `memory/groups/{name}/flush-state.json` (when groups
are nested under a parent group name); the top-level
`memory/groups/flush-state.json` aggregates across all groups.

> The `mtime` keys are written by `remem-flush` and `precompact-remem` to
> enable delta-only flushes. See HOOKS.md → "Shared Conventions".

## Anti-Pattern

```
❌ Load all at once        → ✅ Load only one at a time
❌ Skip index           → ✅ Read index first
❌ Load two groups      → ✅ Clear old, reload from Step 1
```

## Complete Protocol Checklist

1. **Entry gate** — index is the only entry
2. **Five-step loading** — name mapping → index → intent → load → sub-layer → budget
3. **Loading discipline** — 2+1 file limit, clear on switch
4. **Write-back** — immediately update on decisions
5. **Memory Flush** — `/remem` + Pre-compact + Idle
6. **Auto-Flush** — precompact hook before compaction
7. **DM Progressive** — independent layout, survives uninstall
8. **Auto-Initialization** — init missing memory from known info
9. **MEMORY.md Discipline (v1.6.0)** — keep MEMORY.md ≤ 50 lines, project details go to `projects/{name}.md`

## MEMORY.md Audit Checklist (v1.6.0)

Run this mental check whenever you touch MEMORY.md:

- [ ] Total lines ≤ 50?
- [ ] No project-specific progress or paths (just index pointers)?
- [ ] No event logs or "X happened on YYYY-MM-DD" narratives?
- [ ] No tool lists (iqtree, bcftools, etc.)?
- [ ] No group names (those live in `memory/groups/`)?
- [ ] No specific project result narratives (sample IDs, measurements)?
- [ ] All project details have a `projects/{name}.md` file behind them?

If any answer is **no** → extract to proper layer.