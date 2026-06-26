# BMA Installation and Integration

BMA is installed as one integrated memory-evolution skill. It is intended to replace separate OpenCortex and Lesson-Imprint skill folders after verification.

---

## Installation Flow (Agent-Side)

The installation is engineered to run with zero human intervention. Follow these steps:

### 1. Run the installer

```bash
bash skills/biomimetic-memory-architecture/scripts/install.sh
```

### 2. Read the system compatibility check output

`install.sh` automatically runs `check_system_config()`, which inspects 10 OpenClaw plugin parameters:

| Parameter | Path | Required |
|-----------|------|----------|
| memory-wiki plugin | `plugins.entries.memory-wiki.enabled` | `true` |
| bridge.indexDailyNotes | `plugins.entries.memory-wiki.config.bridge.indexDailyNotes` | `true` |
| bridge.indexDreamReports | `plugins.entries.memory-wiki.config.bridge.indexDreamReports` | `false` |
| active-memory plugin | `plugins.entries.active-memory.enabled` | `true` |
| persistTranscripts | `plugins.entries.active-memory.config.persistTranscripts` | `false` |
| memory-core plugin | `plugins.entries.memory-core.enabled` | `true` |
| dreaming.deep.enabled | `plugins.entries.memory-core.config.dreaming.phases.deep.enabled` | `false` |
| dreaming.enabled | `plugins.entries.memory-core.config.dreaming.enabled` | `true` (recommended) |
| bridge.indexMemoryRoot | `plugins.entries.memory-wiki.config.bridge.indexMemoryRoot` | `true` (recommended) |
| bridge.followMemoryEvents | `plugins.entries.memory-wiki.config.bridge.followMemoryEvents` | `false` (recommended) |

### 3. Fix any critical mismatches

If the check finds critical issues, the output includes ready-to-run `gateway config.patch` commands:

```
   ❌ critical: bridge.indexDailyNotes=true

   To auto-fix critical issues:
   gateway config.patch {"plugins.entries.memory-wiki.config.bridge.indexDailyNotes": true}
```

**Execute every `gateway config.patch` command shown under "To auto-fix critical issues".** These are safe partial updates — they only set the specified keys, leaving all other config untouched.

After executing the patches, re-run verify:

```bash
bash skills/biomimetic-memory-architecture/scripts/verify.sh
```

### 4. Verify system health

```bash
bash skills/biomimetic-memory-architecture/scripts/verify.sh
```

`verify.sh` re-runs the same 10-parameter check plus:
- Core bootstrap files (MEMORY.md, SOUL.md, USER.md, TOOLS.md, AGENTS.md)
- BMA directories
- Lesson-Imprint state
- Retention audit script
- Cron job presence and prompt validity
- OpenClaw doctor plugin error status (when available)

Repeat steps 3-4 until all critical checks pass.

---

## What the Installer Creates

```text
memory/projects/
memory/runbooks/
memory/workflows/
memory/contacts/
memory/archive/
memory-archive/reports/
memory-archive/
memory/lesson-imprint/
```

The installer also injects the P9 daily log format principle into MEMORY.md if missing.

---

## System Compatibility Detail

BMA depends on three OpenClaw base plugins. Each requires specific settings:

### memory-wiki

| Setting | Value | Why |
|---------|-------|-----|
| `bridge.indexDailyNotes` | `true` | BMA's daily logs and structured files need to be searchable |
| `bridge.indexDreamReports` | `false` | BMA's distillation handles dreaming output; avoid duplicate indexing |
| `bridge.indexMemoryRoot` | `true` | Index MEMORY.md, TOOLS.md for cross-file search |
| `bridge.followMemoryEvents` | `false` | BMA doesn't use event-based triggers |

### active-memory

| Setting | Value | Why |
|---------|-------|-----|
| `persistTranscripts` | `false` | Runtime-only recall; BMA manages persistence via memory-wiki |

### memory-core (dreaming)

| Setting | Value | Why |
|---------|-------|-----|
| `dreaming.enabled` | `true` | Keep light/REM phases for memory candidate generation |
| `dreaming.phases.deep.enabled` | `false` | BMA's daily distillation handles promotion; OpenClaw's deep phase writes to MEMORY.md directly → conflicts |

---

## Daily Distillation Cron

Use `references/daily-distillation.md` as the cron instruction body, or set the cron message to read that BMA reference file.

Daily distillation handles:

- OpenCortex-style promotion into structured memory files
- Lesson-Imprint extraction from failures/corrections
- raw daily log archive into `memory/archive/`

## Weekly Synthesis Cron

Use `references/weekly-synthesis.md` as the weekly instruction body, or set the cron message to read that BMA reference file.

Weekly synthesis handles:

- recent archive review
- structural integrity
- retrieval health
- runbook candidates
- Lesson-Imprint health
- BMA retention report review + automatic Phase 2 execution

## Lesson-Imprint Component

BMA includes Lesson-Imprint as procedural memory. It stores compact safeguards in:

```text
memory/lesson-imprint/lessons.json
memory/lesson-imprint/config.json
memory/lesson-imprint/BOOTSTRAP.md
```

CLI:

```bash
python3 skills/biomimetic-memory-architecture/scripts/lesson_imprint.py init
python3 skills/biomimetic-memory-architecture/scripts/lesson_imprint.py validate
python3 skills/biomimetic-memory-architecture/scripts/lesson_imprint.py promote
```

Raw failures and corrections remain in daily/archive logs until BMA retention metabolizes those source files.

## Retention Pipeline

```bash
# Phase 1: Audit
python3 skills/biomimetic-memory-architecture/scripts/bma_retention_audit.py --workspace . --older-than-days 30

# Phase 2: Metabolize (runs automatically in Weekly Synthesis)
python3 skills/biomimetic-memory-architecture/scripts/bma_phase2_migrate.py --workspace . --audit-report <report> --execute
```

## Replacing Separate Skills

After BMA verify passes and cron messages have been updated to BMA references, the separate folders can be removed:

```text
skills/opencortex/
skills/lesson-imprint/
```

Do not remove them until:

1. `scripts/verify.sh` passes (all critical checks green).
2. Daily and weekly cron messages point to BMA reference files.
3. Any prior Lesson-Imprint references point to BMA's `scripts/lesson_imprint.py`.
4. You have a git checkpoint.

## Safety Rules

- Do not cold-archive active Lesson-Imprint state files.
- Do not rewrite `MEMORY.md` or `AGENTS.md` for procedural lessons; use `memory/lesson-imprint/BOOTSTRAP.md`.
- Do not scan the full history by default; start with aged candidates only.
- BMA never deletes source files — only moves them to `memory-archive/` (fully reversible).
