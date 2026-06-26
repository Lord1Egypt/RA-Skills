# 🧠 Agent Memory Loop

**Lightweight self-improvement loop for AI agents.**

Your agent forgets everything between sessions. This skill gives it a learning system that actually works — one-line entries, structured dedup, severity-aware review queues, injection-safe source labels, and pre-task review. Minimal context burn, maximum learning.

## Quick Start

```bash
bash scripts/install.sh /path/to/workspace
```

Then add to your agent's instructions:

```markdown
## Self-Improvement
Before major tasks: `grep -i "keyword" .learnings/*.md` for relevant past issues.
After errors or corrections: log to `.learnings/` using the agent-memory-loop format.
Never auto-write to SOUL.md/AGENTS.md/TOOLS.md. Stage to .learnings/promotion-queue.md.
```

## How It Works

1. **Log** errors, corrections, and discoveries as one-line entries
2. **Dedup** by stable ID (fallback: keyword grep)
3. **Review queue** when recurring (`count:3+`) or critical (`severity:critical`)
4. **Human approves** promotion to instruction files
5. **Pre-task review** before major work — grep, name the learning, state the adjustment
6. **Track prevention** — increment `prevented:N` when a learning actually changed behavior

## Runtime structure

| File | Purpose |
|------|---------|
| `SKILL.md` | Lean runtime entrypoint |
| `references/logging-format.md` | Canonical line formats, optional fields, examples |
| `references/operating-rules.md` | Dedup, review queue, promotion model, trimming |
| `references/promotion-queue-format.md` | Queue entry structure and status lifecycle |
| `references/detail-template.md` | Optional detail-file template for complex failures |
| `references/design-tradeoffs.md` | Why this stays lean instead of turning into a system |
| `scripts/install.sh` | Set up `.learnings/` in a workspace |
| `scripts/review.sh` | Health check — pending promotions, stale entries, stats |
| `assets/*.md` | Template files copied by install script |

## Key features

- **Review queue** — no auto-promotion to instruction files; human approval required
- **Source labels** — `agent` / `user` / `external`; external content blocked from promotion
- **Severity awareness** — `severity:critical` triggers review even at count:1
- **Loop closure** — `prevented:N` tracks whether learnings actually changed behavior
- **Structured dedup** — stable IDs (`ERR-YYYYMMDD-NNN`) instead of raw grep
- **Optional detail files** — link to `.learnings/details/` for complex failures
- **Staleness / expiry** — optional `expires:` field + periodic trimming

## Requirements

- `grep`, `date` (any POSIX system)
- No frameworks, no dependencies, no configuration

## License

MIT — Don Zurbrick

## Links

- [ClawHub](https://clawhub.ai/zurbrick/agent-memory-loop)
- [GitHub](https://github.com/zurbrick/agent-memory-loop)
