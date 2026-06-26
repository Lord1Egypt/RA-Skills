# 🧠 BeastXA Memory Pro

**Stop losing context. Start remembering everything.**

A production-grade memory system for [OpenClaw](https://github.com/openclaw/openclaw) agents. Zero external dependencies — pure local Markdown files.

## The Problem

AI agents forget. Every time the context window fills up and compacts, your agent loses track of what it was doing, what you decided, and what mistakes it already made. You end up repeating yourself. Again. And again.

## The Solution

BeastXA Memory Pro gives your agent a three-layer memory system that survives compaction:

| Layer | What | How |
|-------|------|-----|
| **Session Notes** | Current work state | Auto-updated before each compaction |
| **Daily Logs** | Raw daily records | Auto-appended, never overwritten |
| **Topic Files** | Organized long-term memory | Auto-maintained by daily/weekly crons |

## Quick Start

```bash
# Install from ClawHub
clawhub install beastxa-memory-pro

# Run setup (~30 seconds)
bash scripts/install.sh

# Done. Everything else is automatic.
```

## What It Does

- ✅ Creates structured memory directory (`memory/topics/`, `session-notes.md`)
- ✅ Splits large MEMORY.md into organized topic files
- ✅ Enhances compaction to preserve critical context
- ✅ Runs daily cleanup cron (23:30) — extracts key info into topics
- ✅ Runs weekly deep clean (Sunday 23:00) — dedup, merge, trim
- ✅ Never overwrites or deletes your existing files

## What It Doesn't Do

- ❌ No external APIs or cloud services
- ❌ No data leaves your machine
- ❌ No modifications to OpenClaw core
- ❌ No complex configuration needed

## Manual Split

Already have a large MEMORY.md? Split it:

```bash
python3 scripts/split_memory.py

# Preview first (no changes):
python3 scripts/split_memory.py --dry-run

# Custom paths:
python3 scripts/split_memory.py --input /path/to/MEMORY.md --output /path/to/topics/
```

## Verify Installation

```bash
bash scripts/verify.sh
```

## Requirements

- OpenClaw 2026.3.x+
- Python 3.8+

## License

MIT-0 — use it however you want, no attribution required.

## Credits

Built by [BeastXA](https://github.com/beastxa6-668) — battle-tested in production with 9 AI agents running 24/7.
