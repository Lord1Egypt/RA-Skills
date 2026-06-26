# Biomimetic Memory Architecture (BMA)

🧬 A biomimetic memory-evolution skill for OpenClaw agents.

BMA models agent memory after human cognition: **consolidation** (daily → structured knowledge), **procedural learning** (repeated mistakes → automatic safeguards), and **metabolization** (aged memory → compressed residue → cold archive). It prevents unbounded context bloat while preserving what matters.

---

## Why BMA Exists

### The Problem

Human memory has forgetting. Agent memory does not.

Without BMA, an OpenClaw agent's `MEMORY.md` grows unbounded. Context windows fill up. Compaction loses information. The agent forgets what it learned, repeats mistakes, and can't distinguish what actually matters from yesterday's tool dump.

### The Solution

BMA introduces **three evolutionary cycles** modeled on human cognition:

| Biological Process | BMA Equivalent | What It Does |
|---|---|---|
| **Sleep consolidation** | Daily distillation + weekly synthesis | Raw daily activity → structured knowledge → patterns |
| **Procedural memory** | Lesson-Imprint | Repeated failures → compact behavioral safeguards |
| **Forgetting & metabolization** | Retention audit → compressed summaries → cold archive | Aged memory shrinks; essential residue persists; full detail remain retrievable |

The result: an agent that **gets better over time** instead of drowning. Week 1 it asks questions. Week 12 it has deep institutional knowledge.

### Design Intent

BMA is not a "memory search engine." It is a **memory metabolism system**.

It treats `memory/` as **active working memory** — indexed, fast, bounded. It treats `memory-archive/` as **cold long-term storage** — full detail, retrievable, but kept outside the indexing surface. Between them sits a **two-phase retention pipeline**:

```
Phase 1 (audit)      Phase 2 (metabolize)
Read-only scan  →    Compress summaries, move sources to cold archive, rewrite references
```

BMA does not optimize for recall speed. It optimizes for **signal retention** — keeping the current state, decisions, failures, and reusable configuration lessons that shape future behavior, while letting transient command logs fade naturally.

---

## System Compatibility

BMA builds on OpenClaw's built-in memory subsystems. For BMA to function correctly, these baseline settings are required:

### memory-wiki

BMA's structured memory files live in `memory/`. memory-wiki indexes them for search and recall.

| Setting | Value | Why |
|---------|-------|-----|
| `bridge.indexDailyNotes` | `true` | **Required.** BMA's daily logs and structured files must be indexed for search. |
| `bridge.indexDreamReports` | `false` | **Required.** BMA handles dreaming output via its own distillation pipeline. memory-wiki should not independently index dream reports. |
| `bridge.indexMemoryRoot` | `true` | Recommends indexing MEMORY.md, TOOLS.md, INFRA.md at the root level. |
| `bridge.followMemoryEvents` | `false` | BMA does not use event-triggered memory updates. |

### memory-core (dreaming)

OpenClaw's default dreaming system generates memory promotion candidates. BMA's daily distillation handles the actual writes.

| Setting | Value | Why |
|---------|-------|-----|
| `dreaming.phases.deep.enabled` | `false` | **Required.** OpenClaw's deep promotion writes directly to MEMORY.md — this conflicts with BMA's own distillation pipeline. |
| `dreaming.phases.light.enabled` | `true` | Keep. Light sleep generates useful short-term candidate memories. |
| `dreaming.phases.rem.enabled` | `true` | Keep. REM sleep identifies cross-day patterns BMA's weekly synthesis can build on. |

### active-memory

Runtime transcript recall. BMA handles its own structured persistence via memory-wiki.

| Setting | Value | Why |
|---------|-------|-----|
| `persistTranscripts` | `false` | BMA persists memory through structured files (memory-wiki bridge), not raw transcripts. Duplicating both paths wastes storage and pollutes indexes. |

### lossless-claw

Optional but recommended. Provides lossless conversation recall that BMA's daily distillation can draw from.

### How They Fit Together

```
active-memory (persistTranscripts=false)
  → Runtime session recall only
  → BMA handles structured persistence via memory-wiki

memory-wiki (indexDailyNotes=true, indexDreamReports=false)
  → Indexes BMA's daily logs and structured memory files
  → Powers memory_search across the active memory surface
  → Excludes dream reports (BMA's distillation pipeline owns that)

memory-core dreaming (light/rem ON, deep OFF)
  → light + rem: generate promotion candidates
  → deep DISABLED: BMA's daily distillation writes the structured output
    (OpenClaw's deep phase writes to MEMORY.md directly → conflicts)

BMA (daily distillation + weekly synthesis + retention)
  → Consolidates: raw logs → structured knowledge
  → Metabolizes: aged files → compressed summaries → cold archive
  → Learns: repeated failures → procedural safeguards (Lesson-Imprint)
```

### Checking Your System

`install.sh` checks your OpenClaw configuration and reports any settings that need adjustment. Run it first:

```bash
bash skills/biomimetic-memory-architecture/scripts/install.sh

```

---


## Provenance

BMA is derived from **OpenCortex** ([MIT License](https://github.com/Suidge/openclaw-skills/blob/main/skills/opencortex/LICENSE)).

### What was changed

| Component | Change |
|-----------|--------|
| **Namespace** | `OPENCORTEX_*` env vars → `BMA_*` (`BMA_VAULT_PASS`, `BMA_ALLOW_FILE_PASSPHRASE`, etc.) |
| **Keyring label** | `opencortex-vault` → `bma-vault` |
| **Service name** | `opencortex` → `bma` (secret-tool / macOS Keychain) |
| **Script headers / help** | All references to "OpenCortex" replaced with "BMA" |
| **`update.sh`** | Rewritten as a BMA maintenance script (removed old upgrade logic, dead code, and OpenCortex-only directories) |
| **`install.sh`** | No longer deletes user's `memory/reports/` directory |
| **Principles** | Added P9: Daily Log Structure (required `##` H2 headers for structured daily entries) |

### Bug fixes applied

| Script | Issue | Fix |
|--------|-------|-----|
| **vault.sh** | `rotate` silently lost the new passphrase on `env` backend, rendering vault unrecoverable | `rotate` now rejects `env` backend with a clear error message |
| **vault.sh** | `_store_passphrase` keychain fallback used `|| &&` (incorrect precedence) | Rewritten with `|| { }` block |
| **update.sh** | `set -e` aborted the script when `lesson_imprint.py` was missing | Failure increments SKIPPED counter instead |
| **update.sh** | Dead `say_do()` function and references to old directories | Removed |
| **git-backup.sh** | `sed` scrubbing failed on secrets with regex metacharacters | Rewritten to use `perl` with `\Q...\E` for literal matching |
| **install.sh** | Deleted `memory/reports/` (potentially destroying user data) | Removed; BMA creates its own directories only |

### What was added (beyond OpenCortex)

| Component | Purpose |
|-----------|---------|
| **`bma_retention_audit.py`** | Phase 1: read-only audit of aged archive files with retention scoring |
| **`bma_phase2_migrate.py`** | Phase 2: compress summaries, migrate sources to cold archive, rewrite references |
| **`lesson_imprint.py`** | Procedural learning — repeated failures become compact behavioral safeguards |
| **`memory-archive/`** | Cold long-term storage outside `memory/` indexing surface |
| **`.bma-flags` / `.bma-version`** | Runtime feature flags and version tracking |
| **P9 principle** | Standardized daily log format (`##` H2 headers, `- ` bullets) for predictable compression |

---

## Architecture

```
memory/                     ← active working memory (indexed by memory-wiki)
 ├─ projects/               ← per-project knowledge
 ├─ runbooks/               ← repeatable procedures
 ├─ workflows/              ← automation pipelines
 ├─ contacts/               ← per-person/org context
 ├─ lesson-imprint/         ← procedural memory state
 ├─ archive/                ← aged daily logs (downranked, still indexed)
 │   └─ _compressed/        ← Phase 2 compressed summaries (active residue)
 └─ YYYY-MM-DD.md           ← daily raw log

memory-archive/             ← cold long-term storage (outside memory/ index scope)
 ├─ archive/                ← metabolized source files (Phase 2 migration target)
 └─ reports/                ← Phase 1 audit reports (process artifacts)

skills/biomimetic-memory-architecture/scripts/
 ├─ install.sh              ← new-user setup (crons, dirs, vault init)
 ├─ update.sh               ← incremental maintenance
 ├─ verify.sh               ← health check
 ├─ vault.sh                ← encrypted secrets (GPG AES-256)
 ├─ git-backup.sh           ← safe auto-commit with secret scrubbing
 ├─ bma_retention_audit.py  ← Phase 1: read-only archive audit
 ├─ bma_phase2_migrate.py   ← Phase 2: compress, migrate, rewrite references
 └─ lesson_imprint.py       ← procedural learning CLI
```

---

## Quick Start

> **Read `references/installation.md` for the complete agent-side installation flow.**

```bash
# 1. Install (runs system compatibility check)
bash skills/biomimetic-memory-architecture/scripts/install.sh

# 2. If system check shows critical issues:
#    Execute the gateway config.patch commands shown in the output
#    Then re-run verify.sh

# 3. Verify
bash skills/biomimetic-memory-architecture/scripts/verify.sh

# Phase 1: Audit aged archives (read-only)
python3 skills/biomimetic-memory-architecture/scripts/bma_retention_audit.py \
  --workspace . --older-than-days 30

# Phase 2: Compress, migrate, rewrite references (dry-run first)
python3 skills/biomimetic-memory-architecture/scripts/bma_phase2_migrate.py \
  --workspace . \
  --audit-report memory-archive/reports/bma-retention-audit-YYYY-MM-DD.md \
  --dry-run

# Phase 2: Execute (after reviewing dry-run output)
python3 skills/biomimetic-memory-architecture/scripts/bma_phase2_migrate.py \
  --workspace . \
  --audit-report memory-archive/reports/bma-retention-audit-YYYY-MM-DD.md \
  --execute
```

---

## Changelog

### v0.1.7

- Refined Daily Distillation rules so project files remain current-state knowledge maps instead of append-only changelogs.
- Added explicit guidance for system/config changes: keep durable decisions, current effective state, reusable lessons, unresolved issues, and archive references; leave raw command traces in daily logs.
- Added an `openclaw.md`-specific rule to prevent complete setting-change ledgers from bloating project memory.

---

## License

BMA inherits from OpenCortex under the MIT License. All derived components carry the same license. New components (`bma_retention_audit.py`, `bma_phase2_migrate.py`, retention rubric, BMA-specific documentation) are also MIT.
