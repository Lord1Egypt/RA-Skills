---
name: tiered-memory
version: 1.0.1
description: Two-tier memory system for OpenClaw agents. Tier 0 = QMD semantic search for recent memories (7-14 days). Tier 1 = SQLite archive for long-term storage. Auto-archives old sessions with LLM summarization. Use when building agents that need efficient, scalable memory management.
metadata:
  openclaw:
    requires:
      bins:
        - ollama
        - python3
    install:
      - id: ollama
        kind: manual
        label: "Install Ollama (https://ollama.com/download) — used for LLM summarization during archiving. Optional: use --skip-llm flag to archive without it."
---

# Tiered Memory Skill

Two-tier memory system combining OpenClaw's QMD semantic search with SQLite archival. Keeps recent memories fast and searchable while compressing old sessions for long-term storage.

## Architecture

```
┌─────────────────────────────────────────┐
│  TIER 0: QMD Semantic Search            │
│  ├── Hot memory (7-14 days)             │
│  ├── GPU-accelerated vector search      │
│  └── Searches: MEMORY.md, memory/*.md   │
├─────────────────────────────────────────┤
│  TIER 1: SQLite Archive                 │
│  ├── Cold storage (14+ days)            │
│  ├── Compressed summaries + key facts   │
│  └── Structured queries via SQL         │
└─────────────────────────────────────────┘
```

## Quick Start

### 1. Ensure QMD is Enabled

QMD comes with OpenClaw. Check status:

```bash
openclaw doctor
```

Should show QMD as available. If not, check `~/.openclaw/openclaw.json`:

```json
{
  "memory": {
    "qmd": {
      "enabled": true,
      "device": "cuda"
    }
  }
}
```

### 2. Set Up Archive Directory

```bash
mkdir -p ~/.openclaw/workspace/memory/archive
```

### 3. Install Cron Job (Auto-archive)

```bash
# Add to crontab
crontab -e

# Add this line for daily 2 AM archive
0 2 * * * /usr/bin/python3 ~/.openclaw/skills/tiered-memory/scripts/memory_archiver.py --days 14 >> ~/.openclaw/workspace/memory/archive.log 2>&1
```

### 4. Use in Your Agent

```python
import sys
sys.path.insert(0, '~/.openclaw/skills/tiered-memory/scripts')
from tiered_memory import TieredMemory

mem = TieredMemory()

# Query across both tiers
results = mem.search("AgentBear project")
```

## Manual Archive

```bash
# See what would be archived
python3 ~/.openclaw/skills/tiered-memory/scripts/memory_archiver.py --dry-run

# Archive files older than 14 days
python3 ~/.openclaw/skills/tiered-memory/scripts/memory_archiver.py

# Archive with custom threshold
python3 ~/.openclaw/skills/tiered-memory/scripts/memory_archiver.py --days 7

# Skip LLM (faster, basic summaries)
python3 ~/.openclaw/skills/tiered-memory/scripts/memory_archiver.py --skip-llm
```

## Query Archives

```bash
# List all archived sessions
python3 ~/.openclaw/skills/tiered-memory/scripts/memory_archiver.py --list

# Search archived summaries
python3 ~/.openclaw/skills/tiered-memory/scripts/memory_archiver.py --search "AgentBear"
```

## How It Works

### Daily Flow

1. **During Day**: Agent writes to `memory/YYYY-MM-DD.md`
2. **QMD Indexes**: Real-time semantic indexing
3. **At 2 AM**: Cron runs archiver
4. **Old Files**: Summarized → SQLite → moved to `archive/`

### Search Priority

When an agent searches memory:

1. **QMD search** (Tier 0) - semantic, fuzzy, fast
2. **If not found** or **need history**: Query SQLite (Tier 1)

### Archive Format

| Field | Type | Description |
|-------|------|-------------|
| session_date | DATE | Original file date |
| summary | TEXT | LLM-generated summary |
| key_facts | JSON | Important facts extracted |
| topics | JSON | Tags/categories |
| message_count | INT | Lines in original file |

## Database Schema

```sql
CREATE TABLE archived_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file TEXT NOT NULL,
    session_date DATE NOT NULL,
    summary TEXT NOT NULL,
    key_facts TEXT,  -- JSON array
    topics TEXT,     -- JSON array
    message_count INTEGER,
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_date ON archived_sessions(session_date);
CREATE INDEX idx_topics ON archived_sessions(topics);
```

## Scripts

- `scripts/memory_archiver.py` - Archive old files to SQLite
- `scripts/tiered_memory.py` - Unified search across both tiers

## Files

- `references/qmd-setup.md` - QMD configuration details
- `references/archiver-api.md` - Archiver script API reference

## Notes

- QMD requires CUDA GPU for best performance (falls back to CPU)
- Archive uses Ollama for summarization (qwen2.5-coder:14b default)
- Original files are preserved in `archive/` folder
- SQLite DB at `~/.openclaw/memory_archive.db`

## Troubleshooting

**QMD not working?**
See `references/qmd-setup.md`

**Archive failing?**
Check Ollama is running: `ollama list`

**Want to restore archived file?**
Just move it back from `memory/archive/` to `memory/`
