---
name: agent-memory-ops
description: Audit and maintain OpenClaw-style long-term memory. Use for MEMORY.md cleanup, daily-note digestion, duplicate detection, stale-memory review, and promoting durable facts from memory/YYYY-MM-DD.md into curated memory.
---

# Agent Memory Ops

Use this skill when you need to keep an agent's memory layer healthy instead of letting `MEMORY.md` rot.

## What it does

- scans `MEMORY.md` + `memory/*.md`
- detects duplicate / near-duplicate bullets
- extracts memory candidates from recent daily notes
- surfaces active follow-ups / TODOs
- filters obvious secrets from suggested memory output
- produces a concise maintenance report you can act on

## Good use cases

- "帮我整理 MEMORY.md"
- "检查记忆层有没有重复和过期信息"
- "把最近几天的重要内容沉淀到长期记忆"
- "做一次 agent memory audit"
- "维护长期记忆 / daily memory / notebook memory"

## Commands

Run from the workspace root that contains `MEMORY.md` and `memory/`.

```bash
python3 {baseDir}/scripts/memory_ops.py report --root .
python3 {baseDir}/scripts/memory_ops.py dedupe --root .
python3 {baseDir}/scripts/memory_ops.py digest --root . --days 7
python3 {baseDir}/scripts/memory_ops.py digest --root . --files 5 --format json
```

## Recommended workflow

1. Run `report` to see gaps, duplicates, and follow-ups.
2. Run `digest` on the last 5-7 daily notes.
3. Promote only durable facts into `MEMORY.md`.
4. Keep volatile chatter in daily notes.
5. Never copy secrets into curated memory unless the user explicitly asks.

## Output policy

- Prefer `--format markdown` for human review.
- Prefer `--format json` when another tool or script will consume the result.
- The script intentionally redacts / skips likely secrets from digest suggestions.

## References

- `references/playbook.md`
