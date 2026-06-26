---
name: context-optimizer
description: Slash OpenClaw token costs and prevent context overflow. Use whenever the user mentions high API costs, expensive tokens, context truncation, context overflow, slow responses in long sessions, noisy memory recall, bloated bootstrap, or wants to tune openclaw.json for efficiency. Also trigger when the user says their agent "uses too many tokens" or tasks feel "wasteful." This skill is aggressive and opinionated — it gives concrete configs to paste, not menus of knobs.
---
# Context Optimizer

Goal: cut input tokens to the minimum that preserves task quality.

Principle: diagnose → apply the single highest-impact fix → re-measure → repeat.

## Fast path — use the script

Use the bundled script to audit and apply defaults quickly:

```bash
python scripts/context_optimizer.py
python scripts/context_optimizer.py --apply
python scripts/context_optimizer.py --apply --aggressive
```

The script auto-detects config path, validates after writing, and rolls back on failure. Use `--config <path>` for a specific file.

After running, verify with `/status` and `/usage tokens`.

## Step 1 — Diagnose (manual path)

If script use is not enough or unavailable, run:

```
/status
/context detail
/usage tokens
```

Identify the dominant sink: bootstrap, tool output, memory retrieval, or long-session buildup.

## Step 2 — Apply fixes in impact order
Work top-down and stop when usage is acceptable.

### Fix 1: Shrink bootstrap files

Trim `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `USER.md`, `MEMORY.md`, and heavy skill files. Remove filler and move rarely-needed detail into references read on demand.

Set smaller bootstrap/image limits and related defaults. See `references/configs.md` for full config examples.

### Fix 2: Throttle tool output

Reduce web search/fetch payloads and prefer targeted reads (line ranges/excerpts) over full dumps.

See `references/configs.md` for full config examples.

### Fix 3: Prune stale tool results

Enable context pruning so older, large tool payloads expire automatically while recent turns stay intact.

See `references/configs.md` for full config examples.

### Fix 4: Tighten memory retrieval

Lower recall volume and raise relevance thresholds; keep deduplication and recency bias enabled. Narrow `memorySearch.extraPaths` if too broad.

See `references/configs.md` for full config examples.

### Fix 5: Session hygiene

Use `/compact` mid-session, `/new` for topic shifts, `/reset` when recovery is unlikely. Enable automatic compaction for sessions that routinely run long.

See `references/configs.md` for full config examples.

## Step 3 — Validate

After each change:
1. Run `openclaw config validate`.
2. Restart gateway if prompted.
3. Re-check `/status` and `/usage tokens`.
4. Spot-check recall on a representative task.
5. If quality drops, loosen the most recent change one notch.

## Quick-reference: symptom → fix
| Symptom | Go to |
|---|---|
| Every turn is expensive, even simple ones | Fix 1 (bootstrap) |
| Cost spikes after searches or file reads | Fix 2 (tool output) |
| Long sessions get slow/truncated | Fix 3 (pruning) + Fix 5 (session hygiene) |
| Memory results feel noisy or irrelevant | Fix 4 (memory retrieval) |
| Screenshots are costly | Fix 1, set `imageMaxDimensionPx: 512` |
| "Context too large" / truncation errors | Fix 5 (`/compact` or `/new`), then Fix 3 |

See `references/aggressive-config.md` for the full aggressive all-in-one config.
See `references/commands.md` for the full commands cheat sheet.
