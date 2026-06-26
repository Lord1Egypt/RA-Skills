---
name: andrew-memory
description: >-
  Product-grade semantic memory layer for AI agents using LanceDB. Provides long-term memory with semantic search, Core Identity management, and conversation distillation. Use when: (1) Learning new facts about the user, (2) Searching for past context, (3) Maintaining consistent persona across sessions, (4) Extracting key memories from conversations.
---

# Andrew Memory Layer

A product-grade semantic memory layer for AI agents, powered by LanceDB.

## Overview

This skill provides long-term memory capabilities for AI agents using a local LanceDB vector database. It enables semantic search, Core Identity management, and conversation distillation.

## Features

- **Semantic Memory Search** - Find relevant memories using natural language queries
- **Core Identity Injection** - Maintain consistent persona across sessions
- **Conversation Distillation** - Automatically extract memory atoms from conversations
- **Dual LLM Support** - Works with MiniMax API (cloud) or Ollama (local)
- **Rich Metadata** - Tracks importance, confidence, and reuse count for each memory

## Tools

| Tool | Description |
|------|-------------|
| `andrew_memory_add` | Store a new memory with type, importance, and confidence |
| `andrew_memory_search` | Search memories semantically using natural language |
| `andrew_memory_set_identity` | Set the agent's Core Identity |
| `andrew_memory_get_identity` | Retrieve the current Core Identity |
| `andrew_memory_distill` | Extract key memories from a conversation |
| `andrew_memory_regenerate_vectors` | Rebuild all vectors (after changing embedding model) |

## Configuration

```json
{
  "plugins": {
    "entries": {
      "andrew-memory": {
        "enabled": true,
        "config": {
          "dataDir": "~/.andrew-memory/data",
          "llmMode": "api",
          "localLlmUrl": "http://localhost:11434"
        }
      }
    }
  }
}
```

### Config Options

| Option | Default | Description |
|--------|---------|-------------|
| `dataDir` | `~/.andrew-memory/data` | LanceDB data directory |
| `llmMode` | `api` | `api` (MiniMax) or `local` (Ollama) |
| `localLlmUrl` | `http://localhost:11434` | Ollama URL when using local mode |

## Requirements

- OpenClaw
- Node.js >= 22
- LanceDB (auto-installed)
- MiniMax API key (if using cloud mode): set `MINIMAX_API_KEY` env var

## Memory Types

- `preference` - User preferences and habits
- `fact` - Factual information about the user or world
- `rule` - Executable rules and guidelines
- `experience` - Past experiences with success/failure outcomes
- `thought` - Thoughts, observations, insights
- `distilled` - Auto-extracted from conversations
- `general` - Default general-purpose memory

## Usage Example

```
User: Remember that I prefer short responses in the morning.
→ andrew_memory_add: { text: "User prefers short responses in the morning", memoryType: "preference" }

User: What did I say about my communication preferences?
→ andrew_memory_search: { query: "communication preferences morning responses" }
```
