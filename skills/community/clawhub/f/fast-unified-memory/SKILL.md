# Skill: Fast Unified Memory

A high-performance unified memory system that integrates OpenClaw memory with semantic memory storage using Ollama's nomic-embed-text model for ultra-fast embeddings.

## Overview

This skill provides a unified memory layer that combines:
- **OpenClaw Memory**: Standard file-based memory storage
- **Semantic Memory**: Vector-based memory using Ollama embeddings

## Features

- ⚡ **Ultra-fast**: ~130ms for combined search (embedding ~40ms + search ~90ms)
- 🔒 **Private**: All processing done locally via Ollama
- 💰 **Free**: No API costs - uses local Ollama instance
- 🧠 **Semantic**: Uses nomic-embed-text for intelligent similarity matching

## Requirements

- [Ollama](https://ollama.ai) installed and running
- `nomic-embed-text` model pulled: `ollama pull nomic-embed-text`

## Installation

```bash
# Install Ollama first
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the embedding model
ollama pull nomic-embed-text

# Start Ollama
ollama serve
```

## Usage

### Commands

```bash
# Search both memory systems
node fast-unified-memory.js search "your query"

# Add a memory
node fast-unified-memory.js add "User prefers concise responses"

# List all memories
node fast-unified-memory.js list

# Show system stats
node fast-unified-memory.js stats
```

## Architecture

```
┌─────────────────────────────────────────────┐
│           FAST UNIFIED MEMORY                │
│                                             │
│  ┌─────────────┐    ┌─────────────┐        │
│  │   OpenClaw  │    │   Semantic  │        │
│  │   Memory    │    │   Memory    │        │
│  │ (files)     │    │  (vectors) │        │
│  └─────────────┘    └─────────────┘        │
│           ↓                  ↓              │
│    [Keyword Match]   [Cosine Similarity]   │
│                                             │
│        Unified Results (ranked)             │
└─────────────────────────────────────────────┘
```

## Performance

| Metric | Value |
|--------|-------|
| Embedding generation | ~40ms |
| Vector search | ~50ms |
| File search | ~40ms |
| **Total search** | **~130ms** |

## Configuration

The skill uses these defaults:
- Ollama URL: `http://localhost:11434`
- Embedding model: `nomic-embed-text`
- Memory storage: `~/.mem0/fast-store.json`
- OpenClaw memory: `~/.openclaw/workspace/memory/`

## Files

- `fast-unified-memory.js` - Main CLI tool
- `SKILL.md` - This documentation

## Troubleshooting

**Ollama not running:**
```bash
ollama serve
```

**Model not found:**
```bash
ollama pull nomic-embed-text
```

**Port conflict:**
The skill assumes Ollama is on port 11434. Update the `OLLAMA_URL` constant if using a different port.

## License

MIT
