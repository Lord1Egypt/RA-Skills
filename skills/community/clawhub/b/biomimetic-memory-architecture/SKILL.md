---
name: Biomimetic Memory Architecture
slug: biomimetic-memory-architecture
version: 0.1.7
homepage: https://github.com/Suidge/biomimetic-memory-architecture
Replace OpenCortex and Lesson-Imprint with integrated OpenClaw memory structure, procedural learning, retention, and forgetting.
metadata: {"openclaw":{"emoji":"🧬","requires":{"bins":["python3"]},"os":["linux","darwin"]}}
---

# Biomimetic Memory Architecture (BMA)

A biomimetic memory architecture for OpenClaw agents.

## When to Use

Use this skill when the user wants to:
- install or verify a complete OpenClaw memory architecture
- replace separate OpenCortex and Lesson-Imprint skill folders
- run daily distillation / weekly synthesis memory governance
- reduce long-term memory bloat
- audit old `memory/archive/` records
- design or run retention / forgetting workflows
- move metabolized source files out of active memory
- keep `memory/` clean for memory-wiki `indexDailyNotes=true`
- convert repeated failures into compact behavioral safeguards

## Core Rules

1. **Provide the full stack** — BMA includes OpenCortex-style structure, daily distillation, weekly synthesis, Lesson-Imprint procedural learning, and retention/forgetting.
2. **Keep promotion and forgetting separate** — daily distillation promotes useful current memory; BMA retention metabolizes aged archives later.
3. **Integrate Lesson-Imprint as procedural learning** — repeated failures become compact safeguards, not bulky narrative memory.
4. **Default to read-only audit** — produce a candidate report before moving, deleting, or rewriting files.
5. **Scan aged candidates only** — avoid full-history sweeps; default threshold is records older than 30 days.
6. **Cold archive, not blind deletion** — move metabolized source files to `memory-archive/` unless the user explicitly approves deletion.
7. **Keep citations** — compressed summaries must cite the moved source file path.
8. **Protect active memory** — never move `projects/`, `runbooks/`, `workflows/`, `contacts/`, `preferences.md`, `lesson-imprint/`, or today’s daily log.
9. **Verify after action** — check file counts, wiki status, and git status after any write phase.

## Quick Reference

| Task | File |
|------|------|
| Architecture and lifecycle | `references/architecture.md` |
| Installation and integration | `references/installation.md` |
| OpenCortex foundation | `references/opencortex-foundation.md` |
| Lesson-Imprint component | `references/lesson-imprint.md` |
| Daily distillation prompt | `references/daily-distillation.md` |
| Weekly synthesis prompt | `references/weekly-synthesis.md` |
| Retention scoring rubric | `references/retention-rubric.md` |
| Read-only audit script | `scripts/bma_retention_audit.py` |
| Lesson-Imprint CLI | `scripts/lesson_imprint.py` |
| Install / update / verify | `scripts/install.sh`, `scripts/update.sh`, `scripts/verify.sh` |
| Vault / metrics / git backup | `scripts/vault.sh`, `scripts/metrics.sh`, `scripts/git-backup.sh` |

## MVP Workflow

**For installation, read `references/installation.md` first.**

```bash
# 1. Install (runs system compatibility check + auto-fix guidance)
bash skills/biomimetic-memory-architecture/scripts/install.sh

# 2. If system check shows critical issues:
#    Execute the gateway config.patch commands shown in the output

# 3. Verify
bash skills/biomimetic-memory-architecture/scripts/verify.sh

# 4. Phase 1 retention audit (read-only)
python3 skills/biomimetic-memory-architecture/scripts/bma_retention_audit.py --workspace . --older-than-days 30
```

See `references/installation.md` for the complete agent-side installation flow including system config auto-fix.
