# Integration Patterns for Codebase Search

## Pattern 1: Pre-research before delegating to a coding agent

Use `search_codebase` to find relevant files *before* spawning a sub-agent. This avoids the "read entire codebase" anti-pattern.

```python
# Manager agent — before spawning prsm-coder
results = await search_codebase("rate limiting middleware", top_k=5)
relevant_files = [r.filepath for r in results if r.score > 0.6]

task = f"""
Fix the rate limiting bug. Relevant files (pre-identified):
{chr(10).join(f'- {f}' for f in relevant_files)}

Error: [paste error here]
"""
# Now spawn coder with focused context
```

## Pattern 2: Scoped search by symbol type

```python
# Find only classes (not functions) related to authentication
classes = await search_codebase("authentication session token", top_k=5, symbol_type="class")

# Find only functions related to webhook handling
fns = await search_codebase("webhook event processing", top_k=5, symbol_type="function")
```

## Pattern 3: Multi-query for complex tasks

```python
# Build a fuller picture before delegating
queries = [
    "circuit breaker state machine",
    "error handling retry logic",
    "network timeout configuration",
]
all_results = []
for q in queries:
    results = await search_codebase(q, top_k=3)
    all_results.extend(results)

# Deduplicate by filepath
seen = set()
unique = [r for r in all_results if r.filepath not in seen and not seen.add(r.filepath)]
```

## Pattern 4: Standalone script usage (no project integration)

Copy `scripts/code_chunker.py` and `scripts/code_index.py` to any directory, then:

```python
import asyncio, sys
sys.path.insert(0, "/path/to/skill/scripts")
from code_index import CodebaseIndex

index = CodebaseIndex("/path/to/any/python/repo")
asyncio.run(index.build())
results = asyncio.run(index.search("your query"))
for r in results:
    print(f"[{r.score:.2f}] {r.symbol_name} — {r.filepath}:{r.start_line}")
```

## Rebuilding a stale index

The index doesn't auto-detect file changes. Rebuild when:
- New files were added
- Significant refactoring occurred
- Search results seem outdated

```python
count = await index.build(force_rebuild=True)
print(f"Rebuilt: {count} symbols indexed")
```

## Score interpretation

| Score | Meaning |
|---|---|
| > 0.75 | Strong semantic match |
| 0.60–0.75 | Relevant, worth inspecting |
| < 0.60 | Weak match, may be noise |

## ChromaDB dependency

```bash
pip install chromadb
# or in a venv:
.venv/bin/pip install chromadb
```

ChromaDB's default embedding function uses `onnxruntime` + `tokenizers` — no OpenAI API key required.
