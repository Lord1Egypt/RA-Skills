---
name: agent-memory-persistence
description: Provide long-term memory persistence for AI agents with SQLite-backed storage, structured metadata, vector embeddings, semantic retrieval, lifecycle management, and queries by user, session, and time.
---

# Agent Memory Persistence

Use this skill when an agent needs durable memory storage across sessions.

## What it provides

- SQLite-backed persistence for text, metadata, and embedding vectors
- CRUD operations for memory items
- Semantic retrieval with cosine-similarity vector search
- Memory lifecycle operations including expiration cleanup
- Filters by user, session, type, and time window

## Project structure

- `src/MemoryStore.ts`: low-level SQLite storage engine
- `src/VectorIndex.ts`: vector similarity search over stored embeddings
- `src/MemoryManager.ts`: high-level API used by agents
- `src/types.ts`: shared TypeScript contracts

## Usage pattern

1. Create a `MemoryManager` with a SQLite path.
2. Write memories with `content`, optional `metadata`, and optional `embedding`.
3. Query memories by session/user or use `searchByVector()` for semantic lookup.
4. Periodically call `cleanupExpired()` to delete stale memories.

## Notes

- Embeddings are stored as JSON arrays in SQLite.
- Vector search is implemented in TypeScript using cosine similarity, which keeps deployment simple and avoids SQLite extensions.
- If memory volume grows substantially, replace `VectorIndex` with an ANN index or SQLite vector extension while preserving the `MemoryManager` API.
