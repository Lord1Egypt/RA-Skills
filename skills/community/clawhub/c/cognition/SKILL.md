---
name: cognition
description: Practical memory architecture for OpenClaw agents. Use when an agent needs to remember commitments across sessions, retrieve prior context, prevent repeat mistakes, stage durable-memory updates safely, compile reusable procedures, or improve memory hygiene over time. Supports a 3-tier adoption path: Core, Recommended, and Advanced.
---

# Cognition

Cognition gives an OpenClaw agent a practical memory architecture: raw logs, durable knowledge, commitments, and reusable procedures.

Use it to make memory operational, not decorative.

## Start Here

Install the scaffolding:

```bash
bash {baseDir}/scripts/install.sh
```

Then adopt it in 3 tiers.

## Tier 1 — Core

Adopt this first. It is the smallest useful subset.

### Core behavior
1. Log important work to `memory/YYYY-MM-DD.md`
2. Keep durable facts in `MEMORY.md` and deeper detail in `memory/bank/*.md`
3. Track commitments in `memory/FUTURE_INTENTS.md`
4. Add the protocol blocks from `{baseDir}/references/protocols.md` to your AGENTS.md

### What Core gives you
- recent-session continuity
- a compact durable memory index
- fewer dropped promises
- a default place to put important facts instead of hoping the model remembers

## Tier 2 — Recommended

Adopt this once Core is part of normal use.

### Add these pieces
- nightly staged consolidation via `{baseDir}/references/consolidation-prompt.md`
- reusable procedures in `memory/procedures/`
- procedure registry in `memory/procedures/index.yaml`
- importance tagging from `{baseDir}/references/protocols.md`

### Safety model
- consolidation stages proposals before durable mutation
- daily logs stay append-only
- uncertain items stay tagged `[NEEDS_REVIEW]`
- new procedures start as `draft`
- promote procedures cautiously: `draft` → `reviewed` → `trusted`

## Tier 3 — Advanced

Only adopt this if Core and Recommended are already working.

### Optional overlays
- `memory/bank/cross-references.md` for linked retrieval
- `memory/KNOWLEDGE_MAP.md` for coarse confidence tracking
- `memory/meta/gap_tracker.json` for repeated retrieval misses
- `memory/meta/retrieval_log.json` for retrieval analytics
- weekly reflection via `{baseDir}/references/weekly-reflection-prompt.md`
- hybrid retrieval tuning via `{baseDir}/references/config.md`

Advanced is for sharper retrieval and maintenance, not for replacing the Core system.

## Core File Map

### Always-on files
- `memory/YYYY-MM-DD.md` — daily session log
- `MEMORY.md` — durable fact index
- `memory/bank/*.md` — deeper topic files
- `memory/FUTURE_INTENTS.md` — commitments and deferred actions

### Recommended files
- `memory/consolidation/YYYY-MM-DD-staged.md` — staged memory proposals
- `memory/procedures/index.yaml` — procedure registry
- `memory/procedures/*.md` — reusable procedures

### Advanced files
- `memory/KNOWLEDGE_MAP.md`
- `memory/bank/cross-references.md`
- `memory/meta/gap_tracker.json`
- `memory/meta/retrieval_log.json`
- `memory/summaries/YYYY-WNN.md`

## Reference Map

Read only what you need:

- `{baseDir}/references/protocols.md` — protocol blocks to copy into AGENTS.md
- `{baseDir}/references/consolidation-prompt.md` — nightly staged consolidation
- `{baseDir}/references/weekly-reflection-prompt.md` — weekly reflection without direct mutation
- `{baseDir}/references/architecture.md` — core systems, overlays, retrieval tiers, safety notes, file structure
- `{baseDir}/references/config.md` — advanced hybrid retrieval tuning
- `{baseDir}/references/cognitive-science.md` — theory appendix

## Guardrails

- Prefer staged proposals over silent durable-memory edits
- Keep raw logs append-only
- Keep `MEMORY.md` compact; move detail into `memory/bank/`
- Treat procedure promotion as earned, not automatic
- If retrieval fails, log the gap instead of inventing certainty
