---
name: code-memory
description: Use when doing coding work in a Git repository and semantic code search, AST-aware symbol lookup, documentation search, Git-history search, or dead-code discovery would help.
metadata: {"openclaw":{"emoji":"🧠","os":["linux","darwin","win32"],"requires":{"bins":["uvx"],"python":">=3.13"},"install":[{"id":"uvx-code-memory","kind":"command","command":"uvx code-memory","label":"Run code-memory MCP server"}]}}
---

# code-memory

`code-memory` is a local MCP server for code intelligence. It indexes a project into a local SQLite database, extracts AST symbols where supported, embeds code/docs with `sentence-transformers`, and exposes MCP tools for code search, docs search, Git history, index stats, and dead-code candidates.

Upstream: https://github.com/kapillamba4/code-memory
Reviewed version: `v1.0.32` / commit `563788a2a7d015699f20251d404aeb293346f40c`.

## When To Use

Use this skill anytime coding a GitHub project or any local Git repository, especially when:

- Starting work in an unfamiliar or large codebase.
- Looking for definitions, references, file structure, or concept-related code.
- Understanding architecture, README/doc conventions, or docstrings.
- Debugging regressions where Git history, file history, blame, or commit details matter.
- Looking for candidate dead code before a cleanup.

Do not use it as the only evidence for risky edits. It is retrieval assistance, not a replacement for `rg`, direct file reads, tests, typechecks, or human review.

## Install

Prerequisites:

- Python `>=3.13`.
- `uv`/`uvx` recommended. Install `uv` with the official Astral installer or package manager.
- First run downloads the default embedding model, currently `jinaai/jina-code-embeddings-0.5b`, to the HuggingFace cache. Expect roughly 600 MB download and about 1 GB+ RAM when loaded.
- On GPU machines, it may auto-use CUDA or MPS. Use CPU mode when GPU memory is tight.

Recommended MCP command:

```bash
uvx code-memory
```

Pip install:

```bash
python3.13 -m pip install code-memory
code-memory
```

From source:

```bash
git clone https://github.com/kapillamba4/code-memory.git
cd code-memory
uv sync
uv run mcp run code_memory/server.py
```

Standalone binaries are published on GitHub Releases. Treat binaries as a supply-chain trust decision: prefer package/source installs unless there is a specific reason to use a binary.

## MCP Configuration

Use stdio for normal per-project MCP hosting:

```json
{
  "mcpServers": {
    "code-memory": {
      "command": "uvx",
      "args": ["code-memory"]
    }
  }
}
```

For a shared server, run:

```bash
uvx code-memory --transport sse --host 127.0.0.1 --port 8765
```

Then configure the MCP host to use:

```json
{
  "mcpServers": {
    "code-memory": {
      "url": "http://127.0.0.1:8765/sse"
    }
  }
}
```

Do not bind SSE to `0.0.0.0` or a public interface without an authenticated reverse proxy. The SSE endpoint is unauthenticated.

## Use Workflow

Before searching a project:

1. Check status if available: `check_index_status(directory="/path/to/repo")`.
2. Index first: `index_codebase(directory="/path/to/repo")`.
3. Re-index after meaningful file changes or if results look stale.
4. Use direct reads/tests after retrieval before making edits.

Core tools:

- `index_codebase(directory, cpu=false)`: builds/refreshes the local index. Use `cpu=true` if CUDA/MPS memory is constrained.
- `check_index_status(directory)`: quick readiness check.
- `get_index_stats(directory)`: index size, coverage, model, and database health.
- `search_code(query, search_type, directory)`: semantic/structural code lookup. `search_type` is `topic_discovery`, `definition`, `references`, or `file_structure`.
- `search_docs(query, directory, top_k=10)`: README/docs/docstring search.
- `search_history(query, directory, search_type, target_file, line_start, line_end)`: Git history, file history, blame, and commit details.
- `find_dead_code(directory, min_confidence=0.5, kinds=null, include_tests=false, top_k=50)`: candidate unused functions/classes/methods. Verify manually before deleting anything.

Useful examples:

```text
index_codebase(directory="/home/jim/project")
search_code(query="authentication middleware", search_type="topic_discovery", directory="/home/jim/project")
search_code(query="UserService", search_type="definition", directory="/home/jim/project")
search_code(query="send_email", search_type="references", directory="/home/jim/project")
search_docs(query="deployment architecture", directory="/home/jim/project", top_k=5)
search_history(query="timeout", search_type="commits", directory="/home/jim/project")
search_history(query="", search_type="file_history", target_file="src/auth.py", directory="/home/jim/project")
find_dead_code(directory="/home/jim/project", min_confidence=0.75)
```

## Files And State

- Creates `code_memory.db` in the indexed project root.
- SQLite WAL mode may also create `code_memory.db-wal` and `code_memory.db-shm`.
- The index stores file paths, source excerpts/symbol text, doc chunks, embeddings, and Git-derived search data.
- `.gitignore` is respected, including nested `.gitignore` files. Built-in skipped dirs include `.git`, `.venv`, `venv`, `node_modules`, caches, `dist`, `build`, `target`, `bin`, and `obj`.
- If a repo contains secrets that are not ignored, they can be indexed. Add sensitive files to `.gitignore` or exclude/remove the database after accidental indexing.
- Add `code_memory.db*` to `.gitignore` unless there is a deliberate reason to version the index. Usually there is not.

## Python And Dependencies

Current upstream requires Python `>=3.13` and declares these runtime dependencies:

- `mcp[cli]`
- `sentence-transformers`
- `sqlite-vec`
- `tree-sitter`
- language grammars: `tree-sitter-python`, `tree-sitter-javascript`, `tree-sitter-typescript`, `tree-sitter-java`, `tree-sitter-kotlin`, `tree-sitter-go`, `tree-sitter-rust`, `tree-sitter-c`, `tree-sitter-cpp`, `tree-sitter-ruby`
- `gitpython`
- `pathspec`
- `markdown-it-py`
- `einops`
- `xxhash`

Development dependencies include `pytest`, `pytest-asyncio`, `pytest-cov`, `ruff`, and `mypy`.

Supported AST parsing: Python, JavaScript/TypeScript, Java, Go, Rust, C/C++, Ruby, Kotlin.

Fallback whole-file indexing: C#, Swift, Scala, Lua, shell, YAML/TOML/JSON, HTML/CSS, SQL, Markdown, text, and similar source-like files.

Environment variables:

- `CODE_MEMORY_LOG_LEVEL`: `DEBUG`, `INFO`, `WARNING`, or `ERROR`.
- `EMBEDDING_MODEL`: HuggingFace model id. Changing it invalidates/rebuilds indexes.
- `CODE_MEMORY_DEVICE`: `auto`, `cuda`, `mps`, or `cpu`.
- `CODE_MEMORY_BATCH_SIZE`: embedding batch size, default `64`.
- `CODE_MEMORY_MAX_WORKERS`: parser thread pool size, default `4`.
- `CODE_MEMORY_RERANK`: `true`/`1`/`yes` enables cross-encoder reranking.
- `RERANK_MODEL`: HuggingFace model id for reranking.

## Security Review

Observed positives:

- No obvious telemetry, analytics, HTTP client, or external API reporting path in reviewed source.
- Code/docs/Git search runs locally after package/model installation.
- Paths are resolved and directory existence is validated for indexing.
- SQLite queries appear parameterized where user-provided values matter.
- `.gitignore` and common dependency/build/cache folders are skipped during indexing.

Important risks and controls:

- `sentence-transformers` loads the embedding model with `trust_remote_code=True`. The default HuggingFace model therefore becomes executable code. For sensitive environments, pre-vet/pin the model or use a trusted local/bundled model via `EMBEDDING_MODEL`.
- First install/run fetches packages and model artifacts from package/model registries. For high-trust work, pin versions/hashes or pre-cache artifacts from a vetted machine.
- SSE transport is unauthenticated. Keep `--host 127.0.0.1`; never expose it directly to a LAN or internet interface.
- The MCP server can index any directory path the host allows it to access. Do not run it with broader filesystem access than needed.
- `code_memory.db*` contains searchable code snippets and embeddings. Treat it as sensitive project data; do not commit, sync, or share casually.
- Secrets accidentally committed or merely present in non-ignored files can be indexed. Check `.gitignore` before indexing private repos.
- `find_dead_code` is heuristic. Reflection, decorators, framework registration, dynamic dispatch, exports, and tests can make live code appear unused.
- Standalone binaries should be verified before use. Prefer source/PyPI installs if provenance matters.

## Troubleshooting

- Empty code/docs results: run `index_codebase(directory)` first, then search again.
- Git history errors: make sure `directory` is inside a Git repository.
- CUDA out-of-memory: call `index_codebase(..., cpu=true)` or set `CODE_MEMORY_DEVICE=cpu`.
- Slow first run: the model download and warmup are normal. Subsequent runs reuse the HuggingFace cache.
- Stale results after edits: re-run `index_codebase`; indexing is incremental.
- Model changed: re-index. Existing index metadata is invalidated when embedding model/dimension changes.

