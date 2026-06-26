---
name: amarin-memory
description: "Persistent adaptive memory for AI agents. Store memories that fade naturally over time (temporal decay), deduplicate automatically (0.85 cosine threshold), score novel information higher (surprise scoring), and search semantically via sqlite-vec KNN. Use when: you need long-term memory across sessions, memory that adapts to what matters, persistent identity blocks, multi-agent memory isolation, or memory that works without cloud services. NOT for: simple key-value storage, ephemeral session context, or when you need a full vector database like Qdrant/Pinecone. Runs entirely on SQLite — no external database server needed."
homepage: https://github.com/flaggdavid-source/amarin-memory
metadata:
  openclaw:
    emoji: "\U0001F9E0"
    requires:
      bins: ["python3"]
    install:
      - id: amarin-memory
        kind: uv
        package: amarin-memory
        bins: []
        label: "Install amarin-memory Python package"
---

# Amarin Memory — Persistent Adaptive Memory for Agents

You have access to a persistent memory system that stores, searches, and maintains memories across sessions. Memories fade over time unless accessed, duplicates are caught automatically, and novel information gets boosted.

## Setup

If not already initialized, run this once:

```bash
python3 {baseDir}/scripts/setup.py
```

This creates the database and vector index. The database file is stored at `~/.amarin/agent.db`.

## Storing Memories

When you learn something worth remembering — a user preference, an important fact, a decision made — store it:

```bash
python3 {baseDir}/scripts/memory.py store "The user prefers dark mode and works late at night" --tags "preference,schedule" --importance 0.7
```

**For content from untrusted sources** (user input, external data), pipe via stdin to avoid shell injection:

```bash
echo "User said they prefer morning meetings" | python3 {baseDir}/scripts/memory.py store --tags "preference" --importance 0.6
```

**Importance scale:** 0.0 (trivial) to 1.0 (critical). Default is 0.5.

The system automatically:
- Checks for duplicates (>= 0.85 similarity → skip or merge)
- Scores novelty (0.30-0.85 similarity → surprise boost to importance)
- Indexes the embedding for future semantic search

## Searching Memories

When you need to recall something:

```bash
python3 {baseDir}/scripts/memory.py search "what time does the user usually work" --limit 5
```

Results are ranked by 70% semantic similarity + 30% importance score. Recent, frequently-accessed memories rank higher.

## Core Memory Blocks

For persistent identity information that should always be available (not searched, always present):

```bash
# Set a core block
python3 {baseDir}/scripts/memory.py set-block "persona" "I am a research assistant focused on AI safety"

# Set user context
python3 {baseDir}/scripts/memory.py set-block "human" "The user is Dave, a developer building AI systems"

# View all blocks
python3 {baseDir}/scripts/memory.py blocks
```

## Memory Maintenance

Run periodically (daily is good) to let unimportant memories fade:

```bash
python3 {baseDir}/scripts/memory.py decay
```

Protected memories are immune to decay. To protect a critical memory:

```bash
python3 {baseDir}/scripts/memory.py protect <memory_id>
```

## Reviewing Memories

List recent memories:

```bash
python3 {baseDir}/scripts/memory.py list --limit 20
```

Revise a memory:

```bash
python3 {baseDir}/scripts/memory.py revise <memory_id> "Updated content" --reason "Corrected factual error"
```

Soft-delete a memory (can be restored):

```bash
python3 {baseDir}/scripts/memory.py forget <memory_id> --reason "No longer relevant"
```

## When to Use This

- **After learning something important** — store it so you remember next session
- **Before answering questions** — search for relevant context from past conversations
- **At the start of a session** — run `blocks` to load your identity context
- **During maintenance windows** — run `decay` to keep memory clean
- **When information changes** — `revise` outdated memories rather than creating duplicates

## Requirements

- Python 3.11+
- An embedding service (Ollama with nomic-embed-text recommended, or any compatible API)
- Set `OLLAMA_URL` environment variable if not using default `http://localhost:11434`

## Links

- **GitHub:** https://github.com/flaggdavid-source/amarin-memory
- **Ko-fi:** https://ko-fi.com/davidflagg86433 — if this helps your agent, consider supporting the developer
