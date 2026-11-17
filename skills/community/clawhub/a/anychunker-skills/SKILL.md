---
name: anychunker-skills
description: Use the `anychunker` Python library to split any text for LLM / RAG / Agent pipelines. Trigger this skill whenever the user asks to chunk, split, or segment text, Markdown, code, or long documents; when they mention "chunk_size / chunk_overlap"; when they need to build a RAG ingestion pipeline; when they ask to preserve Markdown structure (code blocks, tables, headings) during splitting; when they want semantic / sentence / token / header-based splitting; or when they mention `anychunker`, `AnyMarkdownBlockChunker`, `AnyTextChunker`, `AnyMarkdownChunker`, `AnySemanticsChunker`, `AnySentenceChunker`, or `AnyCodeChunker`.
version: 1.0.0
author: AnyForge
---

# AnyChunker Skill

> **Language**: [English](SKILL.md) · [简体中文](SKILL_zh.md)

Split any text for LLM / RAG / Agent pipelines using the `anychunker` library.

The killer feature is **structure-preserving block-level Markdown splitting**: code fences, tables, and HTML blocks stay intact, and every chunk carries parent/child index trees so you can reconstruct hierarchical context later — ideal for high-quality RAG retrieval layers.

## Workflow

1. **Verify install** — run `python scripts/verify_install.py` to confirm `anychunker` is importable and print installed extras (see [Environment check](#environment-check)).
2. **Pick the right chunker** — cross-check the user's intent against the [Chunker selection matrix](#chunker-selection-matrix). If unsure, ask the user one clarifying question ("Do you need to preserve Markdown code blocks / tables?" is usually the deciding factor).
3. **Load only the needed API section** — `references/api-reference.md` is long; grep for the class name and read only that section.
4. **Write the smallest working example** — do NOT dump every parameter. Start with `chunk_size` + `chunk_overlap` and defaults; add tokenizer / language / embedding only when the user asks.
5. **Verify with a real run** — actually execute the script and print `len(doc.chunks)`, first/last chunk `content` preview, and any metadata the user cares about. Never fabricate output.
6. **Hand off cleanly** — for RAG ingestion, use `document.batchIterator(batch_size=N)` to feed downstream (embedding API, vector DB); see [Batch iteration](#batch-iteration).

## Installation

`anychunker` is on PyPI. Requires Python ≥ 3.7.

```bash
pip install anychunker
```

Optional extras (install only when the user's use case requires them):

| Extra need | Install command |
|---|---|
| `AnyTextChunker.from_tokenizer("...")` — HuggingFace tokenizer for token-accurate splits | `pip install transformers` (already a hard dep, but the tokenizer model itself is downloaded on first use) |
| `AnySemanticsChunker` — needs an embedding function | `pip install sentence-transformers` (or any embedding backend of your choice) |
| Chinese word-count length via jieba | `pip install jieba` |

Same command works on macOS / Linux / Windows. On Windows use PowerShell or cmd; the `pip install` line is identical.

### Environment check

Run the bundled verification script — it's pure Python and works on macOS / Linux / Windows without modification:

```bash
python scripts/verify_install.py
```

It prints:
- `anychunker` version + install path
- Whether optional deps (`transformers`, `sentence-transformers`, `jieba`) are importable
- A tiny end-to-end smoke test that splits a 3-line Markdown snippet

If `anychunker` is missing, the script exits with code `1` and prints the exact install command — **do not `pip install` on the user's behalf**; show them the command and wait.

## Chunker selection matrix

Use this table to pick a class, then read only that section of `references/api-reference.md`.

| User intent | Class | Why this one |
|---|---|---|
| Split Markdown while keeping code blocks / tables / HTML intact; need parent/child chunk relationships for RAG | **`AnyMarkdownBlockChunker`** ⭐ | Block-level split, structure-preserving, returns chunks with `block_parent_id` / `block_child_id` / `chunk_parent_id` / `chunk_child_id` |
| Generic recursive text split (paragraphs → lines → sentences → chars) | `AnyTextChunker` | Recursive separator fallback, pluggable `length_function` |
| Token-accurate splits (control cost for GPT-4 / Claude / Qwen etc.) | `AnyTextChunker.from_tokenizer("<HF model>")` | Uses a real HF tokenizer to count tokens |
| Chinese-word-count length | `AnyTextChunker(..., length_function=jieba_length)` | User-supplied length function; see recipe |
| Language-aware code split (Python / JS / Go / Rust / Java / C++ / …) | `AnyTextChunker.from_language(Language.PYTHON, ...)` or `AnyCodeChunker.from_python(...)` | Uses language-specific separators (`class`, `def`, `func`, `fn`, `\nfunction `, …) |
| Simple flat split by Markdown headers (like LangChain's `MarkdownHeaderTextSplitter`) | `AnyMarkdownChunker` | Header-only split, flat chunks with header metadata |
| Split by sentence boundaries | `AnySentenceChunker` | Sentence-aware, respects CJK + Latin punctuation |
| Split by semantic similarity (embed adjacent sentences, cut on similarity drop) | `AnySemanticsChunker` | Embedding-agnostic — pass any callable |

## Core imports

Import everything from the top-level package. `__init__.py` uses lazy loading, so importing `anychunker` alone does **not** pull `transformers` / `torch`; the heavy deps only load when you touch a class that needs them.

```python
from anychunker import (
    AnyTextChunker,             # recursive text split
    AnyMarkdownChunker,         # header-based Markdown split
    AnyMarkdownBlockChunker,    # block-level Markdown split (★ RAG go-to)
    AnyCodeChunker,             # code split by language
    AnySentenceChunker,         # sentence split
    AnySemanticsChunker,        # semantic split
    Language,                   # enum: PYTHON / JS / GO / RUST / MARKDOWN / HTML / ...
    Chunker,                    # schema: one chunk
    DocumentMetadata,           # schema: doc-level metadata
    ChunkBatcher,               # schema: a batch of chunks
)
```

## Minimal usage — the four most common paths

### 1. Structure-preserving Markdown split (recommended default for RAG)

```python
from anychunker import AnyMarkdownBlockChunker

chunker = AnyMarkdownBlockChunker(chunk_size=500, chunk_overlap=50)
doc = chunker.invoke(markdown_text)

for c in doc.chunks:
    print(c.chunk_id, c.metadata.get("title"), c.content[:60])
```

Each chunk's `metadata` carries `block_id`, `title`, `headings`, and full `block_parent_id` / `block_child_id` arrays — use these to rebuild hierarchical context in your vector store.

### 2. Recursive text split (fast, no external deps)

```python
from anychunker import AnyTextChunker

chunker = AnyTextChunker(chunk_size=500, chunk_overlap=50)
doc = chunker.invoke(long_text)
```

Default separators are tuned for mixed CJK + Latin text (`\n\n`, `\n`, `。`, ` `, `""`). Override with `separators=[...]` if needed.

### 3. Token-accurate split for a specific LLM

```python
chunker = AnyTextChunker.from_tokenizer(
    "Qwen/Qwen3-8B",   # any HuggingFace tokenizer id or local path
    chunk_size=1024,
    chunk_overlap=100,
)
doc = chunker.invoke(text)
```

`chunk_size` is now measured in tokens (not characters).

### 4. Semantic split

```python
from anychunker import AnySemanticsChunker
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")
def emb(sentences): return model.encode(sentences).tolist()

chunker = AnySemanticsChunker(embedding_model=emb)
doc = chunker.invoke(text)
```

Any callable that returns `List[List[float]]` works — you're not locked into `sentence-transformers`.

## Batch iteration

Every `invoke()` returns a `Document`. To feed downstream in batches (embedding API rate limits, DB bulk inserts):

```python
for batch in doc.batchIterator(batch_size=16):
    # batch is a ChunkBatcher with:
    #   batch.chunks               → List[Chunker]
    #   batch.get_content_text()   → joined content
    #   batch.get_chunk_ids()      → [chunk_id, ...]
    #   batch.total_content_length → int
    embeddings = my_embed_api([c.content for c in batch.chunks])
    my_vector_db.upsert(batch.get_chunk_ids(), embeddings)
```

## Quick demo

Run the bundled demo to see `AnyMarkdownBlockChunker` in action end-to-end (works on macOS / Linux / Windows):

```bash
python scripts/quick_demo.py
```

It splits a mixed Markdown sample (headings + code fence + HTML table) and prints each chunk's `chunk_id`, `title`, `content` preview, and parent/child block ids so you can see the hierarchy tree.

## Parameter cheat sheet

Common to every chunker unless noted otherwise:

| Param | Default | Notes |
|---|---|---|
| `chunk_size` | `2048` | Target size — units depend on `length_function` (chars by default, tokens with `from_tokenizer`) |
| `chunk_overlap` | `200` | Must be `<` `chunk_size`; overlap between adjacent chunks |
| `separators` | CJK-friendly list | Recursive split fallback order |
| `length_function` | `len` | Any `Callable[[str], int]` — swap in `jieba`, HF tokenizer, tiktoken, etc. |
| `keep_separator` | `True` | `True` / `False` / `"start"` / `"end"` |
| `is_separator_regex` | `False` | Set `True` if your separators contain regex |
| `strip_whitespace` | `True` | Strip leading/trailing whitespace on each chunk |

For **`AnyMarkdownBlockChunker`** specific params, see `references/api-reference.md#anymarkdownblockchunker`.

## Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `ValueError: Chunk size cannot be less than chunk overlap.` | `chunk_overlap >= chunk_size` | Ensure `chunk_overlap < chunk_size` |
| Code fence gets split mid-block by `AnyTextChunker` | Wrong chunker for Markdown | Switch to `AnyMarkdownBlockChunker` |
| Markdown headers "disappear" from chunk `content` | **By design** — `AnyMarkdown{,Block}Chunker` strip headers into `metadata.title` / `metadata.headings`; only body text is chunked | Read headers from `chunk.metadata` (they're structured, not lost); use `AnyTextChunker.from_language(Language.MARKDOWN, ...)` if you need raw headers in content |
| A short Markdown doc like `# h1\n## h2\nsss` returns just 1 chunk | Markdown chunkers count body-only; `sss` is the sole body node | Expected behavior — the two headers are in `metadata.title` / `metadata.headings` of that single chunk |
| `chunk_size=500` produces tiny chunks | Using `from_tokenizer` — size is in tokens, not chars | Increase `chunk_size` or drop `from_tokenizer` |
| First import is slow / pulls torch on macOS | User touched `AnyTextChunker.from_tokenizer` or `AnySemanticsChunker` | Lazy loading only helps if you don't call those; expected behavior |
| Empty `doc.chunks` | Input was empty or entirely stripped | Check `strip_whitespace` and input |
| Weird chunk boundaries for Chinese text | Using default English-only separators | Keep the default CJK-aware list, or pass `separators=["\n\n","\n","。","！","？"," ",""]` |
| Semantic chunker crashes on Windows with `sentence-transformers` | First run downloads model → path with spaces | Use `HF_HOME` env var to point to a short path (e.g. `C:\hf` or `/tmp/hf`) |

## Recipes

More end-to-end recipes (RAG ingestion, jieba length, code splitting, semantic tuning) live in `references/recipes.md`. Grep for the section that matches the user's ask and read only that section.

## Links

- PyPI: <https://pypi.org/project/anychunker/>
- GitHub: <https://github.com/anyforge/anychunker>
- DeepWiki: <https://deepwiki.com/anyforge/anychunker/>
