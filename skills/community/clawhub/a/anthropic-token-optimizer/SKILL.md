---
name: anthropic-token-optimizer
description: Reduce Anthropic API costs (cache read, compaction, context bloat) for OpenClaw agents. Use when users ask about token optimization, reducing API costs, cache read expenses, context management, workspace file trimming, codebase navigation caching, or cost-effective Anthropic model usage. Covers config tuning, behavioral patterns, workspace hygiene, cache TTL alignment, bootstrap size limits, context budgeting, compaction survival, and codebase map caching (Atris pattern) for Claude Opus/Sonnet/Haiku.
---

# Anthropic Token Optimizer

Minimize Anthropic API costs without sacrificing quality. Focus on **cache read reduction** — the #1 cost driver for long sessions with Opus.

## Anthropic Pricing Reference

| Model | Input | Cache Write | Cache Read | Output |
|-------|-------|-------------|-----------|--------|
| Haiku | $0.80 | $1.00 | $0.08 | $4 |
| Sonnet | $3 | $3.75 | $0.30 | $15 |
| Opus | $15 | $18.75 | $1.50 | $75 |

*(per MTok — multiply by millions of tokens)*

**Key insight:** Cache read = `context_size × num_turns`. 200k context × 50 turns on Opus = **~$15 just cache reads**.

---

## Part 1: Config Optimizations (openclaw.json)

### 1. Compaction model — use cheaper model (highest ROI ✅)

```jsonc
"compaction": {
  "mode": "safeguard",
  "model": "anthropic/claude-sonnet-4-20250514"
}
```

Sonnet summarizes at **5x less cost** than Opus. Quality comparable for summaries.

### 2. Context pruning — trim old tool results

```jsonc
"contextPruning": { "mode": "cache-ttl", "ttl": "1h" }
```

| TTL | Behavior | Verdict |
|-----|----------|---------|
| `1h` | Trims after 1 hour | ✅ Best balance |
| `30m` | Moderate | OK for active sessions |
| `5m` | Aggressive | ⚠️ Loses tool results |

### 3. Cache retention — keep "long"

```jsonc
"params": { "cacheRetention": "long", "context1m": true }
```

`"long"` = fewer cache writes ($18.75/MTok on Opus!). Don't switch to `"default"`.

### 4. Cache TTL heartbeat alignment

Anthropic cache expires after ~1h idle. Heartbeat at 55min keeps it warm:

```jsonc
"heartbeat": { "every": "55m" }
```

Prevents expensive cache re-writes when agent resumes after idle.

### 5. Bootstrap size limits — cap workspace injection

```jsonc
"bootstrapMaxChars": 8000,
"bootstrapTotalMaxChars": 30000
```

Check current injection: `/context list`. Prevents oversized files from inflating every turn.

---

## Part 2: Workspace Hygiene (biggest long-term win)

### File budgets

| File | Target | Review cycle |
|------|--------|-------------|
| AGENTS.md | <500 tokens (~2KB) | Monthly |
| SOUL.md | <250 tokens (~1KB) | Rarely |
| TOOLS.md | <500 tokens (~2KB) | When tools change |
| MEMORY.md | <400 tokens (~1.5KB) | Weekly prune |
| HEARTBEAT.md | <400 tokens (~1.5KB) | When done |
| memory/YYYY-MM-DD.md | <30 lines | Collapse at EOD |
| **Total injected** | **<2,800 tokens** | |

### Reduction tactics

- **Merge** redundant files (IDENTITY.md + USER.md → SOUL.md)
- **Move** non-essential docs to subfolders (`docs/`, `notes/`) — not auto-injected
- **Collapse** exploration into decisions: keep "what we decided", delete "how we got here"
- **Prune** ghost context: references to old paths, removed tools, fixed bugs
- **Deduplicate**: info in SOUL.md shouldn't repeat in MEMORY.md or AGENTS.md

### Daily memory rules

**Write:** decisions + why (1 line), new tools/config, lessons, user preferences.
**Skip:** exploration steps, command outputs, things already in MEMORY.md, delivered content.
**Format:** Bullets, not paragraphs. One fact per line.

---

## Part 3: Behavioral Patterns

### 6. `/compact` after each topic (most effective manual action)

```
/compact Focus on [topic summary]
```

### 7. `/new` when switching topics entirely

Context resets to 0. Don't carry 200k into unrelated work.

### 8. Subagents for tool-heavy work

Spawn subagents (cheaper model) for: codebase grep, reading 5+ files, research/web fetch. Tool results stay isolated.

### 9. Tool output discipline

- Truncate: `| head -20`, `| jq '.key'`
- Request only needed fields from APIs
- Never paste full JSON when you need one value
- Output >50 lines → summarize, don't quote

### 10. File loading discipline

- Startup: only today + yesterday memory files
- Read SKILL.md only when task needs that skill
- Don't re-read files already in context

---

## Part 4: Context Budgeting

### Information partitioning

| Budget | Content |
|--------|---------|
| 10% | Task instructions + constraints |
| 40% | Recent 5-10 turns of dialogue |
| 20% | Decision logs ("tried X, failed because Y") |
| 20% | High-relevance MEMORY.md snippets |
| 10% | Tool schemas + system prompt |

### Compaction survival

Before compaction hits, critical state must be captured:

1. **WAL Protocol**: On corrections, decisions, specific values → write to `SESSION-STATE.md` before responding
2. **Working buffer**: At 60%+ context → append exchange summaries to `memory/working-buffer.md`
3. **Recovery**: After compaction, read buffer + session state first. Never ask "where were we?"

### Session lifespan

After 85% context or 3+ compactions → start fresh with `/new`. Good MEMORY.md means minimal context loss.

---

## Part 5: Codebase Map Caching (Atris Pattern)

**Problem:** Every code review or exploration session re-reads the same files, burning tokens on repeated `grep`/`read` calls. A 500-file project can cost 50k+ tokens just for navigation.

**Solution:** Generate a persistent codebase map (`atris/MAP.md`) once, reuse across sessions.

### Setup (one-time per project)

```bash
# Install atris skill
npx clawhub@latest install atris

# Or manually: create atris/ folder in project root, then scan
rg "^(export|function|class|const|def |async def |router\.|app\.)" \
  --line-number -g "!node_modules" -g "!.git" -g "!dist" -g "!.env*"
```

### MAP.md structure

```markdown
# MAP.md — [Project] Navigation Guide
> Last updated: YYYY-MM-DD

## Quick Reference
- `src/index.ts:1` — App entry point
- `src/routes/auth.ts:15` — POST /login handler
- `src/models/user.ts:8` — User schema

### Feature: Authentication
- **Entry:** `src/auth/login.ts:45-89` (handleLogin)
- **Validation:** `src/auth/validate.ts:12` (validateToken)
- **Routes:** `src/routes/auth.ts:5-28`

### Feature: Billing
- **Controller:** `src/controllers/billing.ts:20`
- **Service:** `src/services/stripe.ts:1-45`
```

### MAP-first rule

Before searching codebase:
1. Read `atris/MAP.md` — found? Go directly to file:line
2. Not found? Search with `rg`, then **add result to MAP.md**

Map gets smarter every session. Never let a discovery go unrecorded.

### Keeping fresh

- New file → add to relevant section
- Deleted file → remove from map
- Major refactor → regenerate affected sections only
- Small updates, not full regeneration

### Token savings

| Codebase | Without map | With map | Savings |
|----------|------------|----------|---------|
| Small (50 files) | ~5k tokens/explore | ~1k | 80% |
| Medium (200 files) | ~20k tokens/explore | ~3k | 85% |
| Large (500+ files) | ~50k tokens/explore | ~5k | 90% |

---

## Diagnostics

```
/context list    → token count per injected file
/context detail  → full breakdown (tools, skills, system)
/usage tokens    → append token count to every reply
/usage cost      → cumulative cost summary
/status          → model, context %, cost estimate
```

## Decision Matrix

| Situation | Action |
|-----------|--------|
| Session >100k context | `/compact` immediately |
| Switching topics | `/new` or `/compact` |
| Reading 5+ files | Spawn subagent |
| Compaction cost high | Set compaction model to Sonnet |
| Daily cost >$10 | Audit session count, compact more |
| Cache writes spiking | Heartbeat ≤55min, keep `cacheRetention: long` |
| Workspace injection >20KB | Merge/move files, set `bootstrapMaxChars` |
| Context >85% | `/new` — start fresh |

## Impact Summary

| Technique | Savings | UX Impact |
|-----------|---------|-----------|
| Compaction model = Sonnet | ~80% compaction cost | None |
| Workspace file budgets | ~30-50% base cost | None |
| `/compact` after topics | ~40-60% cache read | Manual step |
| Cache TTL heartbeat (55m) | ~20-30% cache writes | None |
| Bootstrap size limits | ~20-30% base cost | None |
| Subagent delegation | ~30% cache read | Better (parallel) |
| Tool output discipline | ~10-20% per turn | Requires habit |
| `/new` for new topics | ~100% (reset) | Lose old context |
| Codebase map (Atris) | ~80-90% code exploration | One-time setup |

---

## Credits

Incorporates ideas from: [openclaw-token-optimizer](https://clawhub.ai/asif2bd/openclaw-token-optimizer), [context-slimmer](https://clawhub.ai), [context-budgeting](https://clawhub.ai), [compaction-survival](https://clawhub.ai), [context-hygiene](https://clawhub.ai), [atris](https://clawhub.ai) (codebase map caching).
