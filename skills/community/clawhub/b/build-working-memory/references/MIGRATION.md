# Migration Reference

Detailed documentation for migrating legacy workspaces to the layered working-memory architecture.

## Legacy system layout

The migration script expects this structure:

```text
/workspace/
├── AGENT.md            # Agent configuration / system prompt / behavior spec
├── MEMORY.md           # Long-term memory (flat or unstructured)
└── memory/
    ├── 2026-03-18.md   # Daily session logs
    ├── 2026-03-19.md
    └── ...
```

Detection criteria: `AGENT.md` exists AND `MEMORY.md` exists AND `memory/state.json` does NOT exist. If `state.json` already exists, the system has already been migrated.

## Migration steps in order

### 1. MEMORY.md restructuring

If `MEMORY.md` already contains `## Active` and `## Fading` headings, it's left untouched.

If not, the existing content is wrapped under a new `## Active` section, and `## Fading` plus `## Maintenance Log` sections are appended:

```markdown
# Long-Term Memory

> Last reviewed: YYYY-MM-DD
> Next review due: after 5 sessions or 7 days, whichever comes first
> Migrated from legacy MEMORY.md — review and curate entries below.

---

## Active

[... original MEMORY.md content here ...]

---

## Fading

(Nothing here yet — entries not referenced in 7+ sessions will move here)

---

## Maintenance Log

| Date       | Action                                |
|------------|---------------------------------------|
| YYYY-MM-DD | Migrated from legacy flat MEMORY.md   |
```

A backup is saved as `MEMORY.md.bak` before any modification.

### 2. New layered files

Created only if missing:

**resumption.md** — seeded from the most recent daily log's Session Summary section. If no daily logs exist, a generic migration note is written.

**threads.md** — empty template with a commented-out thread format example. The user or agent should populate this from recent daily logs after migration.

**state.json** — bootstrapped from existing daily logs:
- `session_counter.total` = number of existing daily log files
- `last_session.timestamp` = last log date + T23:59:00Z (approximation)
- `last_session.daily_log` = path to the most recent log
- `flags.memory_review_due` = true if 5+ logs exist (curation is overdue)
- `context_hints.last_topic_position` = migration note with log count

**index.md** — rebuilt from all existing daily logs via `rebuild_index.py`.

**archive.md** — empty starter template.

**events.json** — empty `{"events": []}`. Historical events must be manually extracted from daily logs if needed.

### 3. Compatibility mirror

`memory/daily/` is created as an empty directory. This exists only for tools that expect the legacy `memory/daily/YYYY-MM-DD.md` path. No files are copied there — canonical logs remain flat under `memory/`.

### 4. AGENT.md patching

The migration appends a `## Working Memory System` section to `AGENT.md` that teaches the agent the full session lifecycle:

**Session start**: what files to load in what order (state.json → resumption.md → MEMORY.md + threads.md → events.json).

**During session**: what to capture (decisions, open questions, structured events, thread updates).

**Session end**: what to persist (daily log, threads, state.json, resumption.md, events.json).

**File locations table**: maps every memory file to its purpose.

**Rules**: canonical flat paths, resumption as handoff not summary, curation cadence, cross-referencing format.

The section is wrapped in HTML comments with a marker (`WORKING MEMORY MANAGEMENT (auto-injected by build-working-memory skill)`) so the migration can detect if AGENT.md has already been patched. Running migrate twice is safe — the second run skips the patch.

A backup is saved as `AGENT.md.bak` before any modification.

Use `--skip-agent-patch` to skip this step entirely if you prefer to manually update AGENT.md.

## CLI usage

```bash
# Full migration
python migrate.py /workspace

# Preview only (no files written)
python migrate.py /workspace --dry-run

# Migrate without touching AGENT.md
python migrate.py /workspace --skip-agent-patch
```

## Edge cases

**Workspace has no daily logs**: state.json is created with `total: 0` and a current timestamp. resumption.md gets a generic "fresh start" note.

**MEMORY.md is empty**: wrapped in Active tier as-is. The empty content under Active signals that curation is needed.

**AGENT.md already patched**: detected by the marker comment. Skipped silently.

**Workspace already fully migrated** (state.json exists): the detection reports `is_legacy: false` and no migration is attempted.

**Daily logs in memory/daily/ instead of memory/**: the migration script recognizes both locations. state.json is bootstrapped from whichever directory has logs, preferring flat `memory/` if both exist.

## Post-migration checklist

1. Review `MEMORY.md` — the content under `## Active` was migrated verbatim. Curate it: add `[session count] [confidence]` metadata, split into subsections, remove stale entries.

2. Review `AGENT.md` — verify the appended section matches your agent's communication style. Edit the wording if needed, but keep the structural instructions intact.

3. Create threads — read the 3-5 most recent daily logs and create a thread in `threads.md` for each ongoing topic. This is the highest-value post-migration task.

4. Rebuild the index — `python rebuild_index.py /workspace` if it wasn't auto-run during migration.

5. Test the loader — `python loader.py /workspace "continue where we left off"` and verify the loaded sources make sense.

6. Run a session — the first post-migration session will populate `resumption.md` with a real handoff note, replacing the bootstrapped one.
