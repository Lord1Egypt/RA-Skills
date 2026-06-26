---
name: beastxa-memory-pro
description: >
  Production-grade memory system for OpenClaw agents. Auto-organizes notes into topic files,
  prevents context loss during compaction, and runs daily/weekly maintenance crons.
  Zero external dependencies — pure local Markdown files. Install and forget.
  Use when: agent keeps forgetting context, MEMORY.md is too large, notes are disorganized,
  or you want automatic memory maintenance without manual effort.
license: MIT-0
---

# BeastXA Memory Pro

Stop losing context. Start remembering everything.

## What It Does

1. **Structured Session Notes** — auto-maintained `session-notes.md` captures your current work state
2. **Smart Memory Split** — breaks large MEMORY.md into topic files with an index
3. **Auto Maintenance** — daily cleanup + weekly deep organization via cron
4. **Anti-Amnesia** — enhanced compaction saves critical context before compression

## Quick Start

```bash
# Install
clawhub install beastxa-memory-pro

# Run setup (interactive, takes ~30 seconds)
bash scripts/install.sh
```

That's it. Everything else is automatic.

## What Gets Created

```
your-workspace/
├── memory/
│   ├── session-notes.md          # Live session state (auto-updated)
│   ├── MEMORY-INDEX.md           # Topic file directory
│   ├── YYYY-MM-DD.md             # Daily logs (auto-appended)
│   └── topics/                   # Organized by theme
│       ├── projects.md
│       ├── decisions.md
│       ├── lessons.md
│       └── ...                   # Auto-generated from your content
```

## How It Works

### Three-Layer Memory

| Layer | File | Purpose | Update Frequency |
|-------|------|---------|-----------------|
| Session | `session-notes.md` | Current work state | Every compaction |
| Daily | `YYYY-MM-DD.md` | Raw daily log | Every significant event |
| Topics | `topics/*.md` | Long-term organized memory | Daily cron |

### Anti-Amnesia System

Before each context compaction:
1. Saves current task, recent decisions, errors, and next steps
2. Writes to both `session-notes.md` and daily log
3. After compaction, agent reads session-notes and resumes seamlessly

### Auto Maintenance Crons

- **Daily (23:30)** — extracts key decisions and lessons from today's log into topic files
- **Weekly (Sunday 23:00)** — deduplicates, merges, trims topic files; verifies index

## Manual Commands

**Split an existing MEMORY.md:**
```bash
python3 scripts/split_memory.py --input MEMORY.md --output memory/topics/
```
- Reads your MEMORY.md, detects topic boundaries (## headers)
- Creates one file per topic in `memory/topics/`
- Generates `memory/MEMORY-INDEX.md` with pointers
- Original file untouched — zero risk

**Verify installation:**
```bash
bash scripts/verify.sh
```

## Configuration

The install script adds compaction enhancement to your OpenClaw config:

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "memoryFlush": {
          "enabled": true,
          "prompt": "Pre-compaction memory flush. Store durable memories in memory/YYYY-MM-DD.md..."
        },
        "instructions": "Preserve: user decisions, file paths, errors+fixes, current task, next step..."
      }
    }
  }
}
```

You can customize the compaction instructions to match your workflow.

## FAQ

**Will it overwrite my existing MEMORY.md?**
Never. The split script only reads it. Your original stays intact.

**Does it send data anywhere?**
No. Everything is local Markdown files. No APIs, no cloud, no external services.

**Can I use it with other memory skills?**
Yes. It only creates files and cron jobs — no core modifications.

**What if I don't like the topic categories?**
Edit them freely. They're just Markdown files. The cron will respect your structure.

## Requirements

- OpenClaw 2026.3.x or later
- Python 3.8+ (for split script)
- That's it
