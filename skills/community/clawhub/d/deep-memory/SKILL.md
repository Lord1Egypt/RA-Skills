---
name: deep-memory
version: 1.0.0
description: "One-click clone of a production-grade semantic memory system: HOT/WARM/COLD tiered storage + Qdrant vector DB + Neo4j graph DB + qwen3-embedding. Enables cross-session semantic retrieval and entity relationship memory for AI agents."
author: DeepEye
tags: [memory, vector-db, neo4j, qdrant, embedding, semantic-search, agent-memory]
requires: [docker, ollama]
---

# Deep Memory Skill 🧠

A production-grade semantic memory system for AI agents. Combines tiered file storage with vector search and graph relationships.

## Architecture

```
┌─────────────────────────────────────┐
│        File Layer (always-on)        │
│  HOT / WARM / COLD Markdown files   │
│  semantic_memory.json               │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│        Vector Layer (Docker)         │
│  Qdrant: semantic similarity search │
│  Collection: semantic_memories       │
│  Dimensions: 4096 (qwen3-embedding)  │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│        Graph Layer (Docker)          │
│  Neo4j: entity relationship memory  │
│  Constraints: Memory.key + Entity.id │
└─────────────────────────────────────┘
               ↓
┌─────────────────────────────────────┐
│     Embedding Model (Ollama)         │
│  qwen3-embedding:8b (4096 dims)      │
│  Local, free, no API calls          │
└─────────────────────────────────────┘
```

## Prerequisites

- Docker Desktop (running)
- Ollama installed (`brew install ollama` on macOS)

## Usage

### Setup (first time)
```bash
python3 ~/.openclaw/workspace/skills/deep-memory/scripts/setup.py
```

### Write a memory
```python
from deep_memory import MemorySystem
mem = MemorySystem()
mem.store("user_sir", "Sir prefers direct communication, no pleasantries", tags=["preference", "communication"])
```

### Search memories
```python
results = mem.search("how does Sir like to communicate?", top_k=5)
for r in results:
    print(r['content'], r['score'])
```

### Joint query (vector + graph)
```python
results = mem.joint_query("investment strategy", entity="Sir", top_k=3)
```

## Setup Flow

When triggered, the setup script will:
1. Check Docker is running
2. Check Ollama is installed and pull qwen3-embedding:8b if needed
3. Start Qdrant container (port 6333/6334)
4. Start Neo4j container (port 7474/7687)
5. Create Qdrant collection (semantic_memories, 4096 dims, Cosine)
6. Create Neo4j constraints (Memory.key, Entity.id)
7. Create HOT/WARM/COLD directory structure
8. Copy Python toolkit to workspace
9. Run end-to-end verification test

## Agent Integration

In your SOUL.md or AGENTS.md, add:
```
## Memory Retrieval
Before answering questions about prior work, decisions, or preferences:
1. Run: python3 ~/.openclaw/workspace/.lib/qdrant_memory.py search "<query>"
2. Combine with memory_search tool results
3. Use top results as context
```
