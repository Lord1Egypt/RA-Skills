---
name: contradiction-detector
description: "Detects and eliminates contradictions between agent instruction files that cause hallucinations and silent misbehavior. Use when: (1) any agent behaves inconsistently despite correct-looking instructions, (2) a sub-agent format/behavior was fixed in one file but the behavior didn't change, (3) a new agent, cron job, or instruction file was added, (4) running a periodic consistency sweep. Scans AGENTS.md, SOUL.md, HEARTBEAT.md, MEMORY.md, cron job payloads, and skill files for any agent — then cross-references them for contradictions."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["openclaw", "python3", "find", "cat"] },
        "configPaths": ["openclaw.json"],
        "readAccess": ["workspace", "workspace/skills", "workspace/hooks"]
      }
  }
---

# Contradiction Detector

Contradictions between agent instruction files are the #1 cause of silent misbehavior in multi-agent OpenClaw setups. Files are loaded non-deterministically across sessions — the only fix is making all files agree.

## Prerequisites

- **`openclaw` CLI** — listing agents and cron jobs
- **`python3`** — parsing JSON config
- **`find`, `cat`** — standard POSIX utilities
- **Filesystem access** to the OpenClaw workspace directory

## Audit Procedure

### Step 1 — Discovery

Enumerate every instruction source: all agents, their workspace files (AGENTS.md, SOUL.md, HEARTBEAT.md, MEMORY.md, IDENTITY.md, USER.md), all cron jobs with inline prompts, all installed skills, and any hook scripts.

**→ Detailed procedure: [references/discovery.md](references/discovery.md)**

Build a complete inventory per agent before proceeding. Missing even one source means contradictions slip through.

### Step 2 — Cross-reference for contradictions

Systematically check every pair of instruction sources per agent against 12 known contradiction patterns:

| # | Pattern | Risk | Most common trigger |
|---|---------|------|---------------------|
| 1 | Format duplication | HIGH | Same output format defined in 2+ files independently |
| 2 | Cron prompt override | HIGH | Cron contains stale instructions; HEARTBEAT.md fix is invisible |
| 3 | Routing mismatch | HIGH | Different session/channel targets for same output |
| 4 | Persona/tone conflict | MED | SOUL.md vs AGENTS.md communication style |
| 5 | Trigger/schedule mismatch | MED | Cron frequency vs HEARTBEAT.md timing |
| 6 | Memory routing conflict | MED | Same data type sent to different memory locations |
| 7 | Dead/orphaned rules | MED | Old rule not removed after newer rule added elsewhere |
| 8 | Cross-agent assumption mismatch | MED | Sender expects X, receiver does Y |
| 9 | Implicit vs explicit behavior | LOW-MED | Gap filled differently by different files |
| 10 | Skill-agent conflict | LOW-MED | Skill instructions override agent rules when triggered |
| 11 | Stale MEMORY.md directives | LOW | "From now on" in MEMORY.md contradicts current AGENTS.md |
| 12 | Environment/config drift | LOW | Hardcoded paths, model names, or URLs that changed |

**→ Full detection procedures and examples: [references/contradiction-patterns.md](references/contradiction-patterns.md)**

### Step 3 — Report and fix

Produce a structured finding for each contradiction (agent, severity, pattern, evidence with exact quotes, impact, proposed fix). Present all fixes as diffs and wait for user confirmation before applying.

**→ Report format, severity guidelines, and fix protocol: [references/reporting-and-fixes.md](references/reporting-and-fixes.md)**

### Post-fix verification

After every fix: re-read both files, verify agreement, and confirm no new contradictions were introduced.

## Scheduling (optional)

This skill works as a manual on-demand invocation. Optionally add to HEARTBEAT.md or a cron job for periodic runs.
