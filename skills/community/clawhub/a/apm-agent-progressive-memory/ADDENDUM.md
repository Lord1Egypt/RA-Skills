# APM — ADDENDUM (Technical Details)

## File Templates (v1.6.0)

### MEMORY.md Template (lean, ≤ 50 lines)

```markdown
# MEMORY.md — Long-term Memory (Authoritative Source)

> ⚠️ This file only stores **high-level identity + index**.
> Project details go to `memory/main/projects/`.
> Event logs go to `memory/YYYY-MM-DD.md`.

## Identity
- **Me**: {agent name}, {role}, {style}
- **Principles**: {3-5 max}

## User
- **Name**: {user name} / {aliases}
- **Timezone**: {tz}
- **Stack**: {languages/tools}

## Servers
- **Host**: {hostname}
- **Access**: {ssh/sftp url}

## Key Databases
- **{db name}**: {path}

## Project Index (see `memory/main/projects/`)

| Project | Path | Detail File |
|---------|------|-------------|
| {name} | {path} | `projects/{name}.md` |
| ... | ... | ... |

## Other Memory Entries
- Current tasks: `memory/main/attention.md`
- Experience index: `memory/main/longterm.md`
- Daily logs: `memory/YYYY-MM-DD.md`
- Group chats: `memory/groups/` (APM 5-step)
- DVC / data: {path}
```

### projects/{name}.md Template

```markdown
# {Project Name}

**Status**: {one-line state, e.g. "Stage3 analysis, batch1 138/140 done"}

## Project Info
- **Path**: {absolute path}
- **Description**: {one-liner}
- **Group**: {group chat name, if any}

## Progress / Milestones
- ✅ {milestone 1}
- ✅ {milestone 2}
- ⏳ {current}

## Key Findings / Notes
- {decision, gotcha, or constraint}

## References
- Source repo: {path}
- Data storage: {path}
- Project report: {path}

## See Also
- `memory/main/attention.md` (current task tracking)
```

### longterm.md Template (DM experience index)

```markdown
# Long-term Memory (APM DM Summary)

> Experience index layer for MEMORY.md.
> Project details → `memory/main/projects/{name}.md`.
> Current tasks → `memory/main/attention.md`.

## Project Status Index

| Project | Detail File | Current Stage |
|---------|-------------|---------------|
| {name} | `projects/{name}.md` | {stage} |

## Key Events Index

| Event | Date | Location |
|-------|------|----------|
| {event} | YYYY-MM-DD | {file path} |

## Server Resources
- Host: {hostname}
- DVC: {path}
- Key DBs: {path list}
```

## Group Index File Template

```markdown
---
group_name: {group_name}
last_updated: YYYY-MM-DD
status: active
memory_budget: 6000
---

# {Group Name} — Progressive Disclosure Index

> ⚠️ This file is the **only legal entry point** for accessing this group's memory.

## Hard Rules

- rule 1
- rule 2

## Routing Index

| Trigger Scenario | Load File | Priority |
|-----------------|-----------|----------|
| Current tasks, Sprint, blockers | `attention.md` | P0 |
| Tech stack, architecture constraints | `project.md` | P1 |
| Historical decisions, lessons learned | `experience.md` | P2 |
| Team roles, contacts | `people.md` | P3 |
| API development details | `conventions/api.md` | P2-L3 |
```

## DM Index File Template

```markdown
---
type: main-session-index
last_updated: YYYY-MM-DD
status: active
memory_budget: 8000
---

# Main Session Memory Index

> This file is the **only entry point** for DM progressive disclosure.

## Reference Declarations

- **Authoritative long-term memory**: `MEMORY.md` (workspace root)
- **Raw daily logs**: `memory/YYYY-MM-DD.md`

## Routing Index

| Trigger Scenario | Load File | Priority |
|-----------------|-----------|----------|
| Current tasks, blockers | `attention.md` | P0 |
| MEMORY.md summary | `longterm.md` | P1 |
| Daily notes summary | `daily-synced.md` | P2 |
| Project context | `projects/{name}.md` | P3 |

## Relationship with MEMORY.md

> ⚠️ **MEMORY.md is the authoritative original. It stays completely unchanged.**
> APM's `longterm.md` serves as MEMORY.md's **experience summary + detail supplement layer**.

## attention.md (Group)

```markdown
# {Group} — Current Focus

## Active Tasks

| Task | Status | Notes |
|------|--------|-------|
| ... | ... | ... |

## Blockers

- ...

## Environment Snapshot

- Last session: YYYY-MM-DD
```

## attention.md (DM)

```markdown
# Main Session — Current Focus

## Active Tasks

| Task | Status | Notes |
|------|--------|-------|
| ... | ... | ... |

## Blockers

- ...

## Environment Snapshot

- Last session: YYYY-MM-DD
- Pending items: N
```

## experience.md (Group)

```markdown
# Experience Log

## Decisions

- [YYYY-MM-DD] Decision: ... → Context: ... | Action: ...
- [YYYY-MM-DD] Decision: ... → Context: ... | Action: ...

## Lessons Learned

- [YYYY-MM-DD] ... → Problem: ... | Solution: ...
```

## longterm.md (DM)

```markdown
# Long-Term Memory — Experience Summary

## MEMORY.md Experience Index

| Topic | MEMORY.md Location | Summary |
|-------|-------------------|---------|
| ... | §... | ... |

## Detail Supplements

| Entry | Detail | Source Date |
|-------|--------|-------------|
| ... | ... | YYYY-MM-DD |

## Decision Log

- [YYYY-MM-DD] Decision: ... → MEMORY.md §...
```

## Flush Content Decisions

### ✅ Write This

| Category | Target File | Decision Criteria |
|----------|------------|-------------------|
| Confirmed decision | `experience.md` | User explicitly agreed/confirmed |
| Task status change | `attention.md` | in-progress → completed/blocked |
| New project agreement | `project.md` | Cross-confirmed by two messages |
| Personnel role change | `people.md` | Explicit role assignment |
| Environment change | `attention.md` | Server migration, port change |
| Lessons learned | `experience.md` | Complete problem + solution |

### ❌ Don't Write

| Category | Reason |
|----------|--------|
| Small talk, greetings | No informational value |
| Opinion only, not landed | No decision formed |
| Repeating existing content | Already recorded |
| Temporary exploration | Direction undecided |

## Write-Back Rules

### Group Chat (`memory/groups/{group}/`)

- **`experience.md`**: append-only, reverse chronological, each entry `YYYY-MM-DD` + context + decision + action
- **`attention.md`**: overwrite (task progress is factual)
- **`project.md`, `people.md`**: primarily append; deletions require confirmation

### DM (`memory/main/`)

- **`longterm.md`**: each flush, distill MEMORY.md updates with original references
- **`attention.md`**: overwrite-update tasks/blockers
- **`daily-synced.md`**: flush-merged summary (append-only)
- **`MEMORY.md`**: **do not touch**

## MEMORY.md Size Audit (v1.6.0)

| Lines | Verdict | Action |
|-------|---------|--------|
| ≤ 30 | ✅ Lean | Maintain |
| 31–50 | ⚠️ Watch | Trim if growth continues |
| 51–80 | ❌ Bloated | Extract project details → `projects/{name}.md` |
| > 80 | 🚨 Violates design | Immediate extraction, treat as bug |

**Symptoms of bloat**:
- Tool lists (which/command -v)
- Temporary fix notes (e.g. post-upgrade instructions) lingering in MEMORY.md
- Project progress with versioned counts (e.g. "batch_1 138/140")
- Result narratives with specific samples or measurements
- Group names listed inline

**Quick extract script** (run from `memory/main/`):

```bash
# Find candidate extraction targets
grep -nE '^- (Stage|batch|complete|finished|installed|fixed)' MEMORY.md
# Find tool lists
grep -nE '(iqtree|vcftools|bcftools|GATK|FastQC|BWA|spades|busco|quast|braker|augustus|metaphlan|bowtie|star|hisat|salmon|kallisto|trinity|canu|flye|raven|miniasm|wtdbg|smartdenovo)' MEMORY.md
# Find event markers
grep -nE '20[0-9]{2}-[0-9]{2}-[0-9]{2}' MEMORY.md
```

If any match → move to `projects/{name}.md` or `longterm.md`.

## Flush State Tracking (v1.6.0)

APM uses **two separate flush-state files** (privacy boundary between DM
and group memory). See `SKILL.md` → "Flush State Files" for the rationale.

### `memory/flush-state.json` (DM)

```json
{
  "last_flush_time": "YYYY-MM-DDTHH:MM:SS+08:00",
  "flush_number": 6,
  "context_usage_at_flush": 45,
  "session_id": "agent:<id>:matrix:direct:room:...",
  "pending_items": [],
  "memory/main/attention.md_mtime": "YYYY-MM-DDTHH:MM:SS+08:00",
  "memory/main/longterm.md_mtime":  "YYYY-MM-DDTHH:MM:SS+08:00"
}
```

### `memory/groups/flush-state.json` (group)

Same shape, scoped to one or more groups:

```json
{
  "last_flush_time": "YYYY-MM-DDTHH:MM:SS+08:00",
  "flush_number": 2,
  "context_usage_at_flush": null,
  "session_id": "agent:<id>:matrix:channel:room:...",
  "pending_items": [],
  "memory/groups/{group_name}/attention.md_mtime": "YYYY-MM-DDTHH:MM:SS+08:00"
}
```

### Rules

- **DM flush writes only** to `memory/flush-state.json`
- **Group flush writes only** to `memory/groups/flush-state.json`
- `pending_items` is **NOT** shared — each file is independent
- `mtime` keys are written by `remem-flush` and `precompact-remem` to
  enable delta-only flushes; old timestamps are preserved across flushes
  for unchanged files
- `context_usage_at_flush` records the context-usage percentage at
  flush time (useful for tuning `precompact-remem` thresholds)