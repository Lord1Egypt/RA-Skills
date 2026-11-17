# AnyChunker Recipes

End-to-end patterns for real workloads. Copy, adjust, run.

## Table of contents

- [RAG ingestion pipeline (Markdown → embeddings → vector DB)](#rag-ingestion-pipeline)
- [Token-accurate chunks for LLM cost control](#token-accurate-chunks)
- [Chinese text with jieba word count](#chinese-text-with-jieba)
- [Splitting a code repository](#splitting-a-code-repository)
- [Semantic split with an OpenAI-compatible embedding API](#semantic-split-with-openai-compatible-embedding)
- [Hierarchical retrieval using block parent/child ids](#hierarchical-retrieval-using-block-parentchild-ids)
- [Saving and loading a Document](#saving-and-loading-a-document)

---

## RAG ingestion pipeline

Markdown docs → block-level chunks → batch embed → upsert to a vector store.

```python
from anychunker import AnyMarkdownBlockChunker
from pathlib import Path

chunker = AnyMarkdownBlockChunker(chunk_size=500, chunk_overlap=50)

def ingest(md_path: Path, doc_id: str):
    text = md_path.read_text(encoding="utf-8")
    doc = chunker.invoke(text)

    for batch in doc.batchIterator(batch_size=16):
        texts = [c.content for c in batch.chunks]
        vectors = embed(texts)  # your embedding backend

        rows = []
        for c, v in zip(batch.chunks, vectors):
            rows.append({
                "id":               f"{doc_id}:{c.metadata['block_id']}:{c.chunk_id}",
                "vector":           v,
                "content":          c.content,
                "doc_id":           doc_id,
                "block_id":         c.metadata["block_id"],
                "block_parent_id":  c.metadata["block_parent_id"],
                "block_child_id":   c.metadata["block_child_id"],
                "title":            c.metadata.get("title", {}),
                "headings":         c.metadata.get("headings", {}),
                "start_pos":        c.start_pos,
                "end_pos":          c.end_pos,
            })
        vector_db.upsert(rows)
```

Storing `block_parent_id` / `block_child_id` alongside each vector lets you do the [hierarchical retrieval trick](#hierarchical-retrieval-using-block-parentchild-ids) at query time.

---

## Token-accurate chunks

When you need `chunk_size` to mean "tokens" (LLM context budgeting):

```python
from anychunker import AnyTextChunker

# HuggingFace tokenizer — matches GPT / Claude / Qwen etc. depending on the model id
chunker = AnyTextChunker.from_tokenizer(
    "Qwen/Qwen3-8B",
    chunk_size=1024,       # tokens, not chars
    chunk_overlap=128,
)
doc = chunker.invoke(text)
```

For `tiktoken` (OpenAI tokenizers), plug the count function in directly:

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

chunker = AnyTextChunker(
    chunk_size=2000,
    chunk_overlap=200,
    length_function=lambda s: len(enc.encode(s)),
)
```

---

## Chinese text with jieba

Word-count-based sizing for Chinese input (more meaningful than character count for some retrieval tasks):

```python
import jieba
from anychunker import AnyTextChunker

def zh_word_len(s: str) -> int:
    return len(jieba.lcut(s))

chunker = AnyTextChunker(
    chunk_size=200,          # jieba words
    chunk_overlap=20,
    length_function=zh_word_len,
    separators=["\n\n", "\n", "。", "！", "？", "；", " ", ""],
)
doc = chunker.invoke(text)
```

---

## Splitting a code repository

Walk a repo, split each file by its language, keep filename in metadata:

```python
from pathlib import Path
from anychunker import AnyTextChunker, Language, DocumentMetadata

LANG_BY_EXT = {
    ".py":   Language.PYTHON,
    ".js":   Language.JS,
    ".ts":   Language.TS,
    ".go":   Language.GO,
    ".rs":   Language.RUST,
    ".java": Language.JAVA,
    ".c":    Language.C,
    ".cpp":  Language.CPP,
    ".md":   Language.MARKDOWN,
    ".html": Language.HTML,
}

def split_repo(root: Path, chunk_size: int = 1200, chunk_overlap: int = 120):
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in LANG_BY_EXT:
            continue
        lang = LANG_BY_EXT[path.suffix]
        chunker = AnyTextChunker.from_language(
            lang, chunk_size=chunk_size, chunk_overlap=chunk_overlap,
        )
        text = path.read_text(encoding="utf-8", errors="ignore")
        doc = chunker.invoke(text)
        doc.metadata = DocumentMetadata(
            name=str(path.relative_to(root)),
            topic=lang.value,
            tag="code",
            length=len(text),
        )
        yield doc
```

`Path.rglob` and `Path.read_text` work identically on macOS / Linux / Windows.

---

## Semantic split with OpenAI-compatible embedding

`AnySemanticsChunker` accepts any callable, so any REST embedding API works — including OpenAI-compatible providers (Together, Anyscale, local vLLM / Ollama, …):

```python
import openai
from anychunker import AnySemanticsChunker

client = openai.OpenAI(base_url="http://localhost:8000/v1", api_key="sk-x")

def embed(sentences: list[str]) -> list[list[float]]:
    resp = client.embeddings.create(
        model="text-embedding-3-large",
        input=sentences,
    )
    return [d.embedding for d in resp.data]

chunker = AnySemanticsChunker(embedding_model=embed)
doc = chunker.invoke(long_text)
```

Tune `breakpoint_threshold` per corpus — lower = more chunks, higher = fewer but larger.

---

## Hierarchical retrieval using block parent/child ids

At query time, expand each hit into its enclosing block(s):

```python
def retrieve(query: str, top_k: int = 5, expand_parents: bool = True):
    query_vec = embed([query])[0]
    hits = vector_db.search(query_vec, top_k=top_k)  # returns rows with metadata

    seen = set()
    passages = []
    for h in hits:
        # 1. Add the hit itself
        key = (h["doc_id"], h["block_id"], h["chunk_id"])
        if key in seen:
            continue
        seen.add(key)
        passages.append(h["content"])

        # 2. Fetch parent blocks for surrounding context
        if expand_parents:
            for parent_block_id in h["block_parent_id"]:
                parent = vector_db.get_by(
                    doc_id=h["doc_id"], block_id=parent_block_id, chunk_id=0,
                )
                if parent:
                    parent_key = (h["doc_id"], parent_block_id, 0)
                    if parent_key not in seen:
                        seen.add(parent_key)
                        passages.append(parent["content"])

    return passages
```

This turns a flat similarity search into a **section-aware** retrieval without any extra store.

---

## Saving and loading a Document

`Document` is a Pydantic model — full serialization for free:

```python
import json

# Save
doc = chunker.invoke(text)
with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(doc.model_dump(mode="json"), f, ensure_ascii=False, indent=2)

# Load
from anychunker import Documents
with open("chunks.json", encoding="utf-8") as f:
    data = json.load(f)
doc2 = Documents.model_validate(data)
```

Cross-platform note: always pass `encoding="utf-8"` when reading/writing on Windows — the default there is `cp1252` and will mangle non-ASCII.

---

## Combining chunkers (block → sentence, header → semantic, etc.)

Chunkers compose freely. Example: first cut by Markdown block, then split large blocks by sentence for finer granularity:

```python
from anychunker import AnyMarkdownBlockChunker, AnySentenceChunker

md = AnyMarkdownBlockChunker(chunk_size=2000, chunk_overlap=0)
sent = AnySentenceChunker(chunk_size=300, chunk_overlap=30)

doc = md.invoke(text)
fine_chunks = []
for c in doc.chunks:
    if c.chunk_size <= 300:
        fine_chunks.append(c)
    else:
        for s in sent.invoke(c.content).chunks:
            s.metadata = {**c.metadata, **s.metadata, "parent_chunk_id": c.chunk_id}
            fine_chunks.append(s)
```

The parent `block_parent_id` / `block_child_id` from the outer split flows through unchanged, so hierarchical retrieval still works.
