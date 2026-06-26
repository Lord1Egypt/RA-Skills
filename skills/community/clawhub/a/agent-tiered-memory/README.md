# 🧠 Tiered Memory Skill for OpenClaw

> Two-tier memory system combining **QMD semantic search** (hot) with **SQLite archival** (cold). Keep recent memories fast and searchable while compressing old sessions for long-term storage.

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 What This Skill Does

OpenClaw agents need memory that scales. This skill provides a **two-tier architecture**:

| Tier | System | Retention | Use Case |
|------|--------|-----------|----------|
| **Tier 0** | QMD Semantic Search | 7-14 days | Hot memory, fuzzy search, daily work |
| **Tier 1** | SQLite Archive | Permanent | Cold storage, summaries, key facts |

### Why Tiered Memory?

- ⚡ **Fast recent recall** — QMD vectors for last 2 weeks
- 💾 **Efficient long-term** — SQLite compressed summaries  
- 🧹 **No context bloat** — Old stuff auto-archived
- 🔍 **Best of both worlds** — Semantic + structured search

---

## 📦 Installation

### Option 1: ClawHub (Recommended)

```bash
clawhub install tiered-memory
```

### Option 2: Manual

```bash
# Clone to your OpenClaw skills directory
git clone https://github.com/jpmoregain-eth/tiered-memory-skill.git ~/.openclaw/skills/tiered-memory
```

### Option 3: Skill File

Download `tiered-memory.skill` from [releases](https://github.com/jpmoregain-eth/tiered-memory-skill/releases) and extract to `~/.openclaw/skills/`.

---

## 🚀 Quick Start

### 1. Set Up Auto-Archive (Cron)

```bash
# Add to crontab - runs daily at 2 AM
crontab -e

# Add this line:
0 2 * * * /usr/bin/python3 ~/.openclaw/skills/tiered-memory/scripts/memory_archiver.py --days 14 >> ~/.openclaw/workspace/memory/archive.log 2>&1
```

### 2. Use in Your Agent

```python
import sys
sys.path.insert(0, '~/.openclaw/skills/tiered-memory/scripts')
from tiered_memory import TieredMemory

mem = TieredMemory()

# Search across both tiers
results = mem.search("AgentBear project")

# Results include:
# - Tier 0: Recent files (semantic match)
# - Tier 1: Archived summaries (keyword match)
```

---

## 📚 Architecture

```
┌─────────────────────────────────────────────────────────┐
│  TIER 0: QMD Semantic Search (GPU Accelerated)          │
│  ├── Hot memory (7-14 days)                             │
│  ├── Searches: MEMORY.md, memory/*.md                   │
│  └── Vector embeddings for fuzzy semantic match         │
├─────────────────────────────────────────────────────────┤
│  TIER 1: SQLite Archive                                 │
│  ├── Cold storage (14+ days)                            │
│  ├── Compressed summaries + key facts                   │
│  └── Structured SQL queries                             │
└─────────────────────────────────────────────────────────┘
```

### Daily Flow

1. **During Day** → Agent writes to `memory/YYYY-MM-DD.md`
2. **QMD Indexes** → Real-time semantic indexing (GPU accelerated)
3. **At 2 AM** → Cron runs archiver
4. **Old Files** → LLM summarizes → SQLite → moved to `archive/`

---

## 🛠️ CLI Usage

### Archive Management

```bash
# See what would be archived (dry run)
python3 ~/.openclaw/skills/tiered-memory/scripts/memory_archiver.py --dry-run

# Archive files older than 14 days
python3 ~/.openclaw/skills/tiered-memory/scripts/memory_archiver.py

# Archive with custom threshold (7 days)
python3 ~/.openclaw/skills/tiered-memory/scripts/memory_archiver.py --days 7

# Skip LLM (faster, basic summaries)
python3 ~/.openclaw/skills/tiered-memory/scripts/memory_archiver.py --skip-llm
```

### Query Archives

```bash
# List all archived sessions
python3 ~/.openclaw/skills/tiered-memory/scripts/memory_archiver.py --list

# Search archived summaries
python3 ~/.openclaw/skills/tiered-memory/scripts/memory_archiver.py --search "AgentBear"
```

### Unified Memory Interface

```bash
# Check memory stats
python3 ~/.openclaw/skills/tiered-memory/scripts/tiered_memory.py stats

# Search across both tiers
python3 ~/.openclaw/skills/tiered-memory/scripts/tiered_memory.py search -q "project"

# List recent sessions
python3 ~/.openclaw/skills/tiered-memory/scripts/tiered_memory.py recent --days 7

# List archived sessions
python3 ~/.openclaw/skills/tiered-memory/scripts/tiered_memory.py archived
```

---

## 📖 Python API

### Basic Usage

```python
from tiered_memory import TieredMemory

mem = TieredMemory()

# Search both tiers
results = mem.search("crypto analysis", days_back=14, limit=10)

# results['tier0'] - Recent file matches
# results['tier1'] - Archived summary matches
```

### Get Session by Date

```python
# Get specific session (checks Tier 0 first, then Tier 1)
session = mem.get_session("2026-03-14")

if session['tier'] == 0:
    print(f"Full content: {session['content']}")
elif session['tier'] == 1:
    print(f"Summary: {session['summary']}")
    print(f"Key facts: {session['key_facts']}")
```

### Memory Statistics

```python
stats = mem.stats()
print(f"Tier 0: {stats['tier0_count']} sessions")
print(f"Tier 1: {stats['tier1_count']} sessions")
print(f"Total size: {stats['total_size_mb']} MB")
```

---

## 🗄️ Database Schema

### SQLite Archive Tables

```sql
-- Archived sessions with summaries
CREATE TABLE archived_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file TEXT NOT NULL,
    session_date DATE NOT NULL,
    summary TEXT NOT NULL,
    key_facts TEXT,      -- JSON array
    topics TEXT,         -- JSON array
    message_count INTEGER,
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for fast queries
CREATE INDEX idx_date ON archived_sessions(session_date);
CREATE INDEX idx_topics ON archived_sessions(topics);
```

---

## ⚙️ Configuration

### QMD Setup (Tier 0)

Ensure QMD is enabled in `~/.openclaw/openclaw.json`:

```json
{
  "memory": {
    "qmd": {
      "enabled": true,
      "device": "cuda",
      "model": "sentence-transformers/all-MiniLM-L6-v2"
    }
  }
}
```

See [references/qmd-setup.md](references/qmd-setup.md) for full configuration.

### Archive Settings (Tier 1)

| Setting | Default | Description |
|---------|---------|-------------|
| `days` | 14 | Archive files older than N days |
| `db_path` | `~/.agentbear/memory_archive.db` | SQLite database location |
| `model` | `qwen2.5-coder:14b` | LLM for summarization |

---

## 🔧 Requirements

- **OpenClaw** with QMD enabled
- **Python 3.8+**
- **Ollama** (for LLM summarization, optional)
- **CUDA GPU** (recommended for QMD, can use CPU)

### Install Ollama (Optional)

```bash
# For LLM-powered summarization
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5-coder:14b
```

---

## 📝 Example Workflow

```bash
# Day 1-14: Agent works, writes to memory/*.md
# QMD indexes everything for semantic search

# Day 15: Cron runs at 2 AM
$ python3 memory_archiver.py --days 14
🔍 Scanning for files older than 14 days...
📋 Found 1 file(s) to archive
📄 2026-03-01.md
   Summary: Session Log — 2026-03-01...
   Facts: 1
   Topics: general
   ✅ Archived

# Now memory/ only has recent files (< 14 days)
# Archive has 2026-03-01.md + SQLite entry
```

---

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built for [OpenClaw](https://openclaw.ai) — the open AI agent platform
- QMD powered by sentence-transformers + CUDA
- Archiver uses [Ollama](https://ollama.com) for local LLM inference

---

<div align="center">

**Made with ❤️ for the OpenClaw community**

[⭐ Star this repo](https://github.com/jpmoregain-eth/tiered-memory-skill) • [🐛 Report Bug](https://github.com/jpmoregain-eth/tiered-memory-skill/issues) • [💡 Request Feature](https://github.com/jpmoregain-eth/tiered-memory-skill/issues)

</div>
