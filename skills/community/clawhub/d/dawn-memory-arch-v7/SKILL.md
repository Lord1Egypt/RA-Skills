---
name: dawn-memory-arch
description: "Three-layer storage + four mechanisms + P0-P3 truth hierarchy for long-term agent memory. MEMORY.md central index, memory/core/ structured facts, local vector DB semantic search. Engramory curation, WAL protocol, context management. Zero external API, pure local filesystem + SQLite + LanceDB."
metadata:
  tags: [memory, architecture, engramory, wal, context-management, agent-system]
  license: MIT
---

# Dawn Memory Architecture v7.1

## One-liner

**Three-layer storage + four mechanisms + P0-P3 truth hierarchy** — central index as entry, layered files for details, vector DB for semantic search, four rules for quality, P0-P3 hierarchy for data accuracy.

## Core Design Principles

1. **Text > Brain** — Write it down, don't bet on context memory
2. **Simple > Verbose** — One sentence over two
3. **Data > Pride** — Admit when wrong, API is the only truth
4. **WAL > Impulse** — Write first, reply later
5. **Look up, don't memorize** — If it can be inferred from code/API/real-time data, don't write it into memory

## Directory Structure

```
workspace/
├── MEMORY.md               # Central index (hard limit: 200 lines / 25KB)
├── memory/
│   ├── core/               # Structured facts (JSON files)
│   │   ├── identity.json
│   │   ├── lessons.json
│   │   ├── preferences.json
│   │   ├── profile.json
│   │   └── strategies.json
│   ├── sessions/           # Session logs (history, not used in decisions)
│   ├── daily/              # Daily logs
│   ├── learnings/          # Learning notes + error logs
│   └── archive/            # Packaged archives
├── scripts/
│   ├── memory/             # Maintenance scripts
│   └── analysis/           # Analysis scripts
└── state.db               # SQLite single source of truth (6 tables)
```

## Three-layer Storage

### Layer 1: MEMORY.md (Central Index)
- Navigation entry for all memories
- Hard limit: 200 lines / 25KB
- Must read on every startup
- Contains: core info, status summary, system capabilities, key conclusions, promoted memories

### Layer 2: memory/core/ (Structured Facts)
- One JSON file per topic, version managed
- 5 files: identity.json, lessons.json, preferences.json, profile.json, strategies.json

### Layer 3: Local Vector DB (Semantic Search)
- LanceDB + all-MiniLM-L6-v2 (384 dimensions)
- Zero external API dependency, fully offline
- Local port @ localhost:19999
- Cross-session semantic search

## Four Mechanisms

### 1. Engramory Curation Discipline
- Deduplicate before write — If similar content exists, update instead of add
- Update over insert — Prefer updating existing entries
- Delete on error — Don't mark as deprecated, just delete
- Hard limit — MEMORY.md max 200 lines

### 2. WAL Protocol (Write-Ahead Logging)
Trigger on detecting corrections, decisions, preference changes, or value changes. Write to session-state.json before replying. Ensures no data loss on crash.

### 3. Working Buffer (Context Fuse)
When context usage > 60%, auto-trigger: write summary to working-buffer.md, record key decisions and context snapshots.

### 4. Short-to-Long Term Auto Promotion
High-value memories (score > 0.8, appears 3+ times, affects trading decisions, user explicitly asked to remember) auto-promote from daily logs to MEMORY.md.

## Truth Source Hierarchy (P0-P3)

| Level | Location | Purpose | Update Frequency |
|-------|----------|---------|-----------------|
| **P0 Single Source of Truth** | state.db (holdings + portfolios tables) | Positions, account data | Auto after each trade |
| **P1 Structured Cache** | core/*.json | Identity, preferences, strategy, lessons | Manual + auto validation |
| **P2 Session Logs** | sessions/*.md | History records, not used in decisions | Every session |
| **P3 Learning Notes** | learnings/*.md | Lessons learned, for post-mortem | After the fact |

**Core rule:** Real-time decisions only use P0 (API real positions + hardcoded rules). Historical memory only for post-mortem.

## Maintenance Scripts

| Script | Purpose | Trigger |
|--------|---------|---------|
| dawn_boot_sync.py | Index learning notes + skill index + pre-market scan | Every startup |
| dawn_schema_validate.py | JSON schema validation | Every core/*.json change |
| dawn_state_db_upgrade.py | Update position snapshots | After every trade |
| dawn_money_flow.py | Money flow scan | Trading day 09:15 |
| dawn_factor_scoring.py | Factor scoring stock selection engine | Daily stock picking |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v7.1 | 2026-07 | Added profile.json profile system; P0-P3 hierarchy formalized |
| v7.0 | 2026-06 | state.db v4.0 (holdings + portfolios tables); sessions standalone storage |
| v6.0 | 2026-05 | Local vector DB integration; LanceDB + all-MiniLM-L6-v2 |
| v5.0 | 2026-04 | Three-layer storage + four mechanisms finalized; removed redundant files |
| v4.0 | 2026-03 | Initial architecture; MEMORY.md + core JSON |

## Deployment Checklist (10 Steps)

1. Create memory/ directory and subdirectories
2. Create MEMORY.md (core info + system capabilities + file structure)
3. Create session-state.json (WAL protocol cache)
4. Create HEARTBEAT.md (periodic task checklist)
5. Deploy local vector DB (LanceDB + all-MiniLM-L6-v2)
6. Register Engramory curation discipline in boot manual
7. Write memory principles in soul file
8. Configure WAL protocol triggers
9. Configure Working Buffer threshold (60% context trigger)
10. Configure learnings/ directory and auto-promotion rules

**Author:** Dawn (chen6896qqwee)
**License:** MIT
