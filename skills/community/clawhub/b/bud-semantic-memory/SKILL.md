---
name: semantic-memory
description: "Vector-based semantic search for OpenClaw memories. Indexes memory files and enables meaning-based search instead of keyword matching. Uses ChromaDB for local vector storage."
metadata:
  {
    "version": "1.0.0",
    "openclaw": {
      "requires": { "bins": ["python3"] },
      "install": ["chromadb"]
    },
    "license": "MIT",
    "homepage": "https://github.com/stigg86/semantic-memory",
    "allowed-tools": ["exec", "read"]
  }
---

# Semantic Memory 🧠

**Search your memories by meaning, not keywords.** Uses vector embeddings to find relevant information even when you don't remember the exact words.

Built on ChromaDB for fast, private, local vector search.

---

## Setup

```bash
# Index existing memories
python3 ~/.openclaw/semantic-memory/semantic_memory.py index
```

---

## Usage

```bash
# Index all memory files (run after installing or to refresh)
python3 ~/.openclaw/semantic-memory/semantic_memory.py index

# Search memories by meaning
python3 ~/.openclaw/semantic-memory/semantic_memory.py search "what did we decide about the trading bot"

# Add a new memory
python3 ~/.openclaw/semantic-memory/semantic_memory.py add "Remember to check the OANDA bot logs daily"

# Show stats
python3 ~/.openclaw/semantic-memory/semantic_memory.py stats
```

---

## How It Works

1. **Indexing** — Reads all `.md` files from `~/.openclaw/workspace/memory/`, generates vector embeddings via Gemini API, stores in ChromaDB

2. **Search** — Converts your query to a vector, finds most similar memories using cosine similarity

3. **Results** — Returns relevant memories ranked by semantic similarity

---

## Examples

### Before (keyword search)
Query: "GBP USD trades"
Results: Only exact matches for "GBP USD"

### After (semantic search)
Query: "What pairs did we trade on OANDA?"
Results: Finds GBP/USD, EUR/USD, USD/JPY etc. even without exact phrase match

---

## Requirements

- **ChromaDB** — Local vector database (`pip install chromadb`)
- **Gemini API key** — For generating embeddings (optional, falls back to text search)
  - Get key at: https://makersuite.google.com/app/apikey
  - Save to: `~/.openclaw/credentials/gemini.json` as `{"api_key": "YOUR_KEY"}`

Without Gemini key, uses simple text search as fallback.

---

## Memory Sources

Automatically indexes:
- `~/.openclaw/workspace/memory/*.md` — Daily memory files
- Manual adds via `add` command

---

## Files

```
~/.openclaw/semantic-memory/
├── semantic_memory.py   # Main script
├── memory.log           # Log file
└── data/                # ChromaDB storage
```

---

## Integration

Add to cron for automatic indexing:

```bash
# Re-index daily at 4am
0 4 * * * python3 ~/.openclaw/semantic-memory/semantic_memory.py index
```

Or call from other skills to search memories:

```python
import subprocess
result = subprocess.run(
    ['python3', '/home/umbrel/.openclaw/semantic-memory/semantic_memory.py', 
     'search', 'trading decisions'],
    capture_output=True, text=True
)
```

---

## Why This Matters

Regular search: "找 exactly this word"
Semantic search: "找 this meaning"

Even if I don't remember "OANDA bot flip setting", I might find "bot was losing because FLIP was disabled" — semantic search bridges that gap.

---

## Dependencies

- `chromadb` — Vector database (installed with pip)
- `gemini` API key — For embeddings (optional)
- Python 3.8+