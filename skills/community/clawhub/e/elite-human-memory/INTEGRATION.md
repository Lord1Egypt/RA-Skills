# Integration Examples

This document provides minimal examples for wiring the Portable Elite Human Memory skill into different agent environments.

## General Pseudocode

```python
# On agent startup or context load
if needs_memory_context(query):
    memories = load_semantic_memories(query)  # or keyword fallback
    memories += apply_metadata_filters(memories, scope="project")
    inject_into_prompt(memories)

# When user says "remember this" or strong signals appear
if should_record_memory(user_input):
    entry = create_memory_entry(user_input, metadata={...})
    write_to_daily_file(entry)
    evaluate_for_promotion(entry)

# Weekly maintenance
run_conflict_detection()
run_auto_promotion_review()
```

## With Embeddings (Recommended)

```python
from sentence_transformers import SentenceTransformer
import chromadb

embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="memory/vectors")

# When writing semantic memory
embedding = embedder.encode(memory_text)
collection.add(documents=[memory_text], embeddings=[embedding], metadatas=[metadata])

# When retrieving
results = collection.query(query_embeddings=[query_embedding], n_results=5)
```

## Without Vector Search (Lightweight Fallback)

Simply scan `MEMORY.md` + recent daily files with keyword matching + metadata filters.

## Clawhub / Marketplace Notes

- This skill expects the host agent to provide file I/O and optional embedding capabilities.
- No external service dependencies.
- Safe to publish as a standalone skill.

## Recommended Agent Hooks

- Context injection before every response when relevant
- Background task for weekly maintenance
- User confirmation step before any auto-promotion

Adapt these patterns to your specific agent runtime.