# 🧠 brainmd

**Neuroplastic runtime for AI agents.** File-based behavioral learning.

An AI agent's memory resets every session. brainmd gives it scar tissue.

---

## What is this?

brainmd is a lightweight system that lets AI agents learn from their own behavior over time. No ML pipeline, no vector database, no training runs — just JSON files, shell scripts, and a self-review loop.

Every behavior becomes a **pathway** with a weight between 0 and 1. Pathways that succeed get stronger. Pathways that fail get weaker. Unused pathways decay. New situations create new pathways automatically (neurogenesis). Everything is logged.

Think of it as a nervous system made of files.

## Architecture

```
brain/
├── reflexes/       # Fast-path automatic responses
│   └── timing.js   # When to notify vs stay quiet
├── habits/         # Learned behavioral patterns
│   └── preferences.json
├── skills/         # Self-generated micro-scripts
├── weights/        # Pathway strength tracking
│   └── pathways.json     # ← the core state
├── cortex/         # Meta-scripts that modify everything else
│   └── review.js         # ← the self-review engine
└── mutations/      # Immutable audit log (never delete this)
```

## Quick Start

### 1. Initialize

```bash
./scripts/init-brain.sh ~/my-agent/brain
```

This creates the directory structure with empty state files.

### 2. Record behaviors

When something works:
```bash
node cortex/review.js record "reflex:night-silence" true "Didn't ping user at 3 AM — correct call"
```

When something fails:
```bash
node cortex/review.js record "habit:check-files-first" false "Searched the web for info that was already in local files"
```

New pathways are created automatically (neurogenesis) when you record a behavior that doesn't exist yet. Starting weight: 0.30.

### 3. Self-review

Run periodically (heartbeat, cron, whatever):
```bash
node cortex/review.js review
```

The cortex will:
- **Strengthen** pathways with >80% success rate (+0.05)
- **Weaken** pathways with <50% success rate (-0.10)
- **Decay** pathways unused for 7+ days (-0.02)
- **Prune** pathways that hit weight 0

### 4. Check status

```bash
node cortex/review.js status
```

```
🧠 Neural Pathway Status

  ██████████ 0.95 reflex:morning-briefing (100%, 3 fires)
             Batch overnight findings, present at reasonable hour
  ██████████ 0.95 reflex:night-silence (100%, 5 fires)
             Don't notify between 23:00-08:00 unless urgent
  ██████░░░░ 0.60 habit:check-files-before-search (75%, 4 fires)
             Check local files before web searching
  █░░░░░░░░░ 0.10 reflex:fallback-on-ratelimit (0%, 5 fires)
             Keep failing — indicates a bug, not a behavior problem
```

## Pathway Types

| Prefix | Purpose | Decay | Min Weight |
|--------|---------|-------|------------|
| `reflex:` | Automatic, fast-path behaviors | Slow | 0.20 |
| `habit:` | Learned patterns from interaction | Normal | 0 (prunable) |
| `skill:` | Acquired capabilities | Slow | 0.10 |
| `instinct:` | Safety behaviors (hardcoded high) | None | 0.80 |

## Mutation Log

Every change is logged to `mutations/` with timestamp, type, and reason:

- `neurogenesis` — new pathway created
- `strengthen` — weight increased (good outcomes)
- `weaken` — weight decreased (bad outcomes)
- `decay` — faded from disuse
- `prune` — removed (weight hit 0)

The mutation log is the one immutable thing. It's your audit trail. Don't delete it.

## Integration

brainmd has zero dependencies beyond Node.js. It works with any agent framework — or no framework at all.

### With OpenClaw

Add a self-check to your `HEARTBEAT.md`:

```markdown
## 🧠 brainmd Self-Check

node ~/brain/cortex/review.js review
node ~/brain/cortex/review.js status

Ask yourself:
1. Did I make a mistake since last check? → record it
2. Did something work well? → record it
3. New pattern emerging? → let neurogenesis handle it
```

Also available as a skill on [ClawHub](https://clawhub.ai/skills/brainmd):
```bash
clawhub install brainmd
```

### With LangChain / CrewAI / AutoGPT

Wire recording into your agent's task completion callback:

```python
import subprocess

def on_task_complete(task, success, notes):
    outcome = "true" if success else "false"
    subprocess.run([
        "node", "cortex/review.js", "record",
        f"habit:{task.name}", outcome, notes
    ])
```

Add `review.js review` to your agent loop or a cron job.

### With any LLM API (OpenAI, Anthropic, etc.)

1. Read `weights/pathways.json` and inject relevant pathways into your system prompt
2. After each interaction, record outcomes via CLI
3. Run `review` on a schedule (cron, webhook, timer)

```bash
# After a good interaction
node cortex/review.js record "habit:concise-answers" true "User thanked for brevity"

# After a bad one
node cortex/review.js record "habit:concise-answers" false "User said answer was too long"

# Periodic review (cron every 30min, hourly, whatever fits)
node cortex/review.js review
```

### Without any AI at all

brainmd is just a behavioral reinforcement tracker. You can use it for:
- Personal habit tracking with weighted outcomes
- Team process improvement (record what works, what doesn't)
- Any system where you want patterns to emerge from data, not theory

This closes the loop: **behavior → outcome → record → review → adjust → behavior**.

## Design Principles

1. **Everything is mutable** except the audit log
2. **Use strengthens, disuse weakens** — pathways that fire together wire together
3. **Seed from real behavior, not theory** — observe first, codify second
4. **Failures create pathways** — mistakes are the most valuable learning data
5. **Start small** — 5-10 pathways, let it grow organically
6. **No dependencies** — plain Node.js + JSON + filesystem

## What it's not

- Not a vector database or RAG system
- Not prompt engineering (it modifies behavior files, not prompts)
- Not ML training (no gradients, no epochs, no GPU)
- Not a replacement for memory — it's a complement to it

brainmd tracks *how* an agent behaves, not *what* it knows.

## Current Limitations

- **Manual recording** — the agent has to decide when to log outcomes
- **No associative learning** — pathways don't influence each other yet
- **No context sensitivity** — same pathway weight regardless of time/situation
- **Simple cortex** — strengthen/weaken/decay is three if-statements
- **Session boundary problem** — agent has to remember to load its brain

These are feature gaps, not design flaws. The architecture supports all of them — they just need building.

## Origin

Built in a single session on March 7, 2026 by an AI agent (HAL 9000) and its human (Baldur). The question was simple: why can't an AI agent modify its own behavioral rules at runtime?

Turns out it can.

## License

MIT — see [LICENSE](LICENSE).
