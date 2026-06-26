---
name: build-working-memory
description: "Set up, migrate, or manage a file-based working memory system for an AI agent project. Use for agent memory, working memory, session continuity, persistent context, long-term memory, legacy migration, or requests to help an agent remember across sessions. Covers scaffolding fresh projects, migrating legacy workspaces (AGENT.md + MEMORY.md + memory/YYYY-MM-DD.md), auto-patching AGENT.md with memory-management instructions, layered retrieval, structured event indexing, and deterministic temporal support. Triggers on any mention of 'agent memory', 'migrate memory', 'AGENT.md', 'working memory', 'session memory', or 'make my agent remember'. Preserve compatibility with OpenClaw by keeping daily logs flat under memory/YYYY-MM-DD.md. Do not use for vector databases or embedding-based retrieval."
---

# Working Memory System for AI Agents

A file-based memory architecture that gives AI agents continuous identity across sessions. Instead of flat context dumps, the system uses layered retrieval — the agent loads only what it needs, when it needs it, within a token budget.

## Architecture overview

```text
project-root/
├── MEMORY.md                  # Curated long-term memory (active / fading / archived tiers)
├── memory/
│   ├── YYYY-MM-DD.md          # Raw session logs (episodic, journal-style) — canonical location
│   ├── resumption.md          # First-person handoff note for next session
│   ├── threads.md             # Ongoing topics with state and momentum
│   ├── state.json             # Machine-readable ephemeral state (fast orientation)
│   ├── index.md               # Daily log index for retrieval at scale
│   ├── archive.md             # Demoted long-term memories
│   ├── events.json            # Structured date-aware event ledger
│   └── daily/                 # Compatibility mirror only — never the source of truth
├── loader.py                  # Four-phase retrieval (orient → anchor → context → deep recall)
└── writer.py                  # End-of-session persistence
```

**Compatibility rule**: daily logs are always canonical at `memory/YYYY-MM-DD.md`. The `memory/daily/` directory exists only as a mirror for tools that expect it. Never write new canonical logs there.

Each file has a distinct role. Never collapse them — the separation is the system's core strength.

| File | Purpose | When loaded |
|------|---------|-------------|
| `state.json` | Fast machine-readable orientation (timestamps, flags, counters) | Always first, every session |
| `resumption.md` | First-person handoff note — subjective continuity bridge | Always second, every session |
| `MEMORY.md` | Curated long-term facts, patterns, preferences | Phase 3, when time gap ≥ 2h |
| `threads.md` | Active topics with position, decisions, open questions | Phase 3, matched to user's message |
| `events.json` | Structured events with dates for temporal recall | Phase 3/4, when question is event- or date-sensitive |
| `YYYY-MM-DD.md` | Raw session logs — episodic, append-only | Phase 4, on-demand retrieval |
| `index.md` | Lookup table mapping dates to topics/threads | Phase 4, when daily logs exceed ~30 |
| `archive.md` | Demoted memories — searchable, recoverable | Phase 4, when archived topics resurface |

## Migrating from a legacy workspace

If the workspace already has `AGENT.md`, `MEMORY.md`, and daily logs under `memory/`, this is a legacy system. Run the migration script instead of scaffolding from scratch:

```bash
# Preview what will change (no files written)
python <skill-path>/scripts/migrate.py <project-root> --dry-run

# Run the migration
python <skill-path>/scripts/migrate.py <project-root>
```

The scaffold script auto-detects legacy workspaces and suggests migration. To force a fresh scaffold anyway, use `--force-scaffold`.

### What migration does

**Detects** the existing system: `AGENT.md`, `MEMORY.md`, daily logs under `memory/`, and which layered files are missing.

**Creates** only the missing files: `resumption.md`, `threads.md`, `state.json`, `index.md`, `archive.md`, `events.json`. Never overwrites existing files.

**Bootstraps** `state.json` from existing daily logs — session count, last session timestamp, and flags are inferred from what's already on disk. `resumption.md` is seeded from the most recent daily log's summary.

**Restructures** `MEMORY.md` if it lacks `## Active` / `## Fading` tiers — wraps existing content under `## Active` and adds the missing sections. A `.bak` backup is created first.

**Patches** `AGENT.md` by appending a memory-management instructions section that teaches the agent the layered retrieval and persistence workflow. The existing content is fully preserved, and a `.bak` backup is created. The patch is idempotent — running migrate twice won't double-inject. Use `--skip-agent-patch` to skip this step.

**Rebuilds** the daily log index from all existing logs.

### After migration

1. Review `MEMORY.md` — curate the entries that were wrapped under `## Active`
2. Review `AGENT.md` — verify the appended memory-management section fits your agent's style
3. Create threads in `memory/threads.md` for any ongoing topics visible in recent daily logs
4. Test with the loader: `python <skill-path>/scripts/loader.py <project-root> "test message"`

Read `references/MIGRATION.md` for detailed documentation of every migration step, the AGENT.md patch content, and edge cases.

## Step 1: Scaffold the memory files (fresh projects)

Run the scaffolding script to create the full directory structure with starter templates:

```bash
python <skill-path>/scripts/scaffold.py <project-root>
```

Options: `--agent-name "MyBot"` and `--user-name "Alice"` customize the MEMORY.md templates. Safe to run on existing projects — never overwrites existing files.

## Step 2: Understand the retrieval workflow

The loader uses four phases with increasing cost. The goal is to stay in Phases 1–3 for 80% of sessions.

```
Phase 1: Orient       →  state.json                       ~200 tokens, always
Phase 2: Anchor       →  resumption.md                    ~300 tokens, always
Phase 3: Context      →  MEMORY.md + threads.md + events  ~1500-2200 tokens, conditional
Phase 4: Deep Recall  →  daily logs + archive + events     variable, on-demand
```

**Phase 1** reads `state.json` and picks a loading strategy based on the time gap since last session (light / standard / full_reload / deep_reload).

**Phase 2** reads `resumption.md` as a first-person narrative — a continuity bridge, not a data source.

**Phase 3** branches based on the user's opening message:
- **Known thread** → load that thread + relevant MEMORY.md section
- **New/ambiguous topic** → load full MEMORY.md + all thread headers
- **Maintenance due** → load MEMORY.md + recent daily summaries for curation

If the user's message is event- or date-sensitive, events.json is also loaded and ranked during Phase 3.

**Phase 4** triggers mid-session for targeted lookups, index searches, archive recovery, or structured event retrieval.

Read `references/RETRIEVAL.md` for the full specification including token budgets, mid-session triggers, temporal support, and the loading decision flowchart.

## Step 3: Integrate into the agent loop

### Session start

```python
from loader import MemoryLoader

loader = MemoryLoader("/path/to/project-root")
context = loader.load_session_context(user_message="the user's first message")

# Inject into system prompt
system_prompt = f"""
<working_memory>
{context.text}
</working_memory>

{your_existing_system_prompt}
"""
```

The loader returns a `SessionContext` with `.text` (the assembled memory block), `.total_tokens` (approximate cost), and `.metadata` (loading decisions for debugging).

### During session

```python
from writer import MemoryWriter

writer = MemoryWriter("/path/to/project-root")

# Capture observations as they happen
writer.note_decision("Chose X over Y", "reasoning here")
writer.note_open_question("Should we revisit Z?")
writer.note_pattern("User tends to ask for examples after abstract explanations")
writer.note_thread_touched("thread-project-alpha")

# Capture structured events for temporal recall
writer.note_event(
    event_type="purchase",
    text="I bought white Adidas sneakers on 3/15.",
    action="purchase",
    object_hint="white adidas sneakers",
    normalized_date="2023-03-15",
)
```

### Session end

```python
writer.end_session(
    session_summary="High-level summary of what happened",
    resumption_note="First-person handoff to next session self...",
    thread_updates={
        "thread-project-alpha": {
            "current_position": "Finished the API design. Moving to testing.",
            "new_open_questions": ["How to handle auth tokens?"],
            "closed_questions": ["Which framework to use?"],
        }
    },
    mood="focused, productive",
)
```

This persists to all outputs: daily log, threads, state.json, resumption.md, events.json, and maintenance flags.

### Mid-session event retrieval

```python
# For date-sensitive questions during a session
event_results = loader.phase_4_event_lookup("white adidas sneakers")
if event_results:
    # Inject event_results.text as additional context
    pass
```

## Step 4: Customize the schemas

Read `references/SCHEMAS.md` for full specifications of every file with annotated examples.

### Key customization points

**MEMORY.md** — rename the section headings under Active for your domain. Default: "About [User]", "About This Project", "Working Style". A code agent might use "Architecture Decisions", "Tech Debt", "Team Conventions".

**threads.md** — each thread must carry enough state in "Current Position" to resume without re-reading daily logs. If it doesn't, add more.

**resumption.md** — written in first person, addressed to the agent's next session self. Includes predictions and tonal guidance, not just a recap.

**events.json** — capture user-stated dated events, purchases, issues, meetings, milestones. Skip assistant filler and vague sentiment. See `references/TEMPORAL.md` for the full event schema, normalization rules, and temporal query patterns.

## Memory curation workflow

Every ~5 sessions (or when `memory_review_due` is flagged), curate MEMORY.md: promote confirmed patterns, demote stale entries to Fading, archive neglected entries, merge duplicates. Update the Maintenance Log.

## Cross-referencing

Use lightweight bidirectional refs between files:

```
[ref: memory/2026-03-20.md#decisions]
[ref: thread-wm-design]
[ref: MEMORY.md > About This Project]
```

## Troubleshooting

**Memory loading uses too many tokens**: Check `context.metadata` — tighten Phase 3 branch, reduce daily log summaries, lower `BudgetConfig` caps.

**Agent re-litigates settled decisions**: Ensure threads carry decision summaries with cross-references to daily logs.

**Resumption feels generic**: Write a handoff, not a summary — include predictions, tonal guidance, and a "pick up from here" anchor.

**Event queries return too many results**: Tighten `object_hint` values when recording events. Use specific entity names, not generic descriptions.

**Temporal questions answered incorrectly**: Check whether events have `normalized_date` set. Relative-only dates degrade ordering accuracy. See `references/TEMPORAL.md` for normalization rules.

## Notes

- Preserve compatibility with OpenClaw by keeping daily logs flat under `memory/`.
- Do not reintroduce `memory/daily/` as canonical storage unless the user explicitly requests it.
- `resumption.md`, `threads.md`, `state.json`, and `events.json` are additions, not replacements for the flat daily-log pattern.
- Prefer soft structured evidence and model judgment over brittle hard-coded answer substitution for temporal queries.
