---
name: agent-memory-hygiene
version: 1.0.0
description: Maintain an agent's long-term memory files: deduplicate, expire stale facts, and keep a clean index. Use on a schedule or whenever memory starts contradicting itself.
---

# Agent Memory Hygiene

## Overview

Agent memory rots: facts expire, duplicates accumulate, and stale instructions quietly override fresh ones. This workflow audits memory the way you would audit a wiki — every entry needs a source, a date, and a reason to still exist.

## When to use

Monthly, after any big project, or whenever the agent cites something that is no longer true.

## Workflow

1. **Inventory** — list every memory file/entry with its date and source
2. **Deduplicate** — merge entries that say the same thing; keep the newest source
3. **Expire** — flag facts with natural lifetimes (prices, statuses, deadlines) and verify or delete them
4. **Resolve contradictions** — when two entries disagree, the newer verified one wins and the loser is removed, not annotated forever
5. **Check for secrets** — memory must never contain keys, seeds, passwords, or one-time codes; remove and rotate if found
6. **Re-index** — the summary/index should let a fresh reader find anything in two hops

## Guardrails

- Never delete the only record of a commitment or debt without moving it somewhere tracked
- When unsure whether a fact is stale, verify it instead of guessing either way
- Keep the user's corrections verbatim — they outrank any inference

## Output format

A hygiene report: entries merged, expired, corrected, secrets found (count only), and the new index state.

---

Part of the Manteclaw free skill series. These workflow skills are free forever; Manteclaw's paid automation tools (runnable code, not just prompts) live at payhip.com/Manteclaw.
