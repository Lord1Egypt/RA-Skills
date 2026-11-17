# AnyChunker API Reference

Full API for every chunker class, schema, and enum in `anychunker`. Grep for the class name and read only the section you need.

## Table of contents

- [`AnyTextChunker`](#anytextchunker) — recursive text split
- [`AnyMarkdownChunker`](#anymarkdownchunker) — header-based Markdown split
- [`AnyMarkdownBlockChunker`](#anymarkdownblockchunker) — block-level Markdown split (structure-preserving)
- [`AnyCodeChunker`](#anycodechunker) — code split by language
- [`AnySentenceChunker`](#anysentencechunker) — sentence split
- [`AnySemanticsChunker`](#anysemanticschunker) — semantic split
- [`Language`](#language) — supported code / markup languages
- [Schemas](#schemas) — `Chunker` / `DocumentMetadata` / `ChunkBatcher` / `Document`

---

## `AnyTextChunker`

Recursive character text splitter with pluggable length function. This is the general-purpose splitter — reach for it when the input is not clearly Markdown / code / RAG-hierarchical.

### Constructor

```python
AnyTextChunker(
    chunk_size: int = 2048,
    chunk_overlap: int = 200,
    separators: Optional[List[str]] = None,
    length_function: Callable[[str], int] = len,
    keep_separator: Union[bool, Literal["start", "end"]] = True,
    is_separator_regex: bool = False,
    strip_whitespace: bool = True,
)
```

**Default `separators` (CJK-friendly):**
```python
["\n\n", "\n", "。", " ", ""]
```

### Classmethods

```python
# Token-accurate splits using a HuggingFace tokenizer
AnyTextChunker.from_tokenizer(
    "Qwen/Qwen3-8B",         # any HF model id or local path
    chunk_size=1024,
    chunk_overlap=100,
    # any other AnyTextChunker kwarg
)

# Language-aware splits (Python, JS, Go, Rust, Markdown, HTML, ...)
AnyTextChunker.from_language(
    Language.PYTHON,
    chunk_size=1000,
    chunk_overlap=100,
)
```

### Methods

```python
doc = chunker.invoke(text: str, **kwargs) -> Document
await chunker.ainvoke(text: str, **kwargs) -> Document   # async
```

### Example

```python
from anychunker import AnyTextChunker

# 1. Default (character-based, CJK-friendly separators)
chunker = AnyTextChunker(chunk_size=500, chunk_overlap=50)
doc = chunker.invoke(text)

# 2. Token-based
chunker = AnyTextChunker.from_tokenizer(
    "Qwen/Qwen3-8B", chunk_size=1024, chunk_overlap=100
)

# 3. Language-based (Markdown)
from anychunker import Language
chunker = AnyTextChunker.from_language(
    Language.MARKDOWN, chunk_size=500, chunk_overlap=50
)

# 4. Custom length function (jieba word count for Chinese)
import jieba
chunker = AnyTextChunker(
    chunk_size=200,
    chunk_overlap=20,
    length_function=lambda s: len(jieba.lcut(s)),
)
```

---

## `AnyMarkdownChunker`

Simple header-based Markdown splitter. Analogous to LangChain's `MarkdownHeaderTextSplitter`. Chunks are **flat** — no parent/child tree. Use `AnyMarkdownBlockChunker` when you need hierarchy.

### Constructor

```python
AnyMarkdownChunker(
    headers_to_split_on: List[Tuple[str, str]],
    strip_headers: bool = True,
    return_each_line: bool = False,
)
```

`headers_to_split_on` is a list of `(marker, metadata_key)` tuples:

```python
[("#", "header1"), ("##", "header2"), ("###", "header3")]
```

### Example

```python
from anychunker import AnyMarkdownChunker

chunker = AnyMarkdownChunker([("#", "h1"), ("##", "h2")])
doc = chunker.invoke(markdown_text)
for c in doc.chunks:
    print(c.metadata)  # e.g. {"h1": "Intro", "h2": "Overview"}
    print(c.content)
```

---

## `AnyMarkdownBlockChunker` ⭐

**The RAG go-to.** Block-level Markdown splitter that keeps code fences, tables, and HTML blocks intact **and** returns chunks with full parent/child index trees. Use this whenever you're building a RAG ingestion pipeline over Markdown docs.

### Constructor

```python
AnyMarkdownBlockChunker(
    chunk_size: int = 2048,
    chunk_overlap: int = 200,
    length_function: Callable[[str], int] = len,
    # ...same set of params as AnyTextChunker
)
```

### Methods

```python
doc = chunker.invoke(text: str, **kwargs)           # full pipeline
doc = chunker.invoke_markdown(text: str, **kwargs)  # markdown-only mode
```

### Chunk metadata schema

Every returned `Chunker` object has this `metadata` shape:

```python
{
    "block_id":          int,          # unique id of the source block
    "chunk_id":          int,          # sub-chunk id within the block
    "title":             dict,         # {"name": "...", "value": [...]} or {}
    "headings":          dict,         # nearest heading context
    "chunk_parent_id":   List[int],    # chunks this chunk depends on
    "chunk_child_id":    List[int],
    "block_parent_id":   List[int],    # block-level hierarchy ↑
    "block_child_id":    List[int],    # block-level hierarchy ↓
    "chunk_size":        int,
    "chunk_overlap":     int,
    "start_pos":         int,
    "end_pos":           int,
}
```

### Example

```python
from anychunker import AnyMarkdownBlockChunker

chunker = AnyMarkdownBlockChunker(chunk_size=500, chunk_overlap=50)
doc = chunker.invoke(markdown_text)

for c in doc.chunks:
    print(
        f"block={c.metadata['block_id']} chunk={c.metadata['chunk_id']} "
        f"title={c.metadata['title']} parents={c.metadata['block_parent_id']}"
    )
    print(c.content[:80])
```

### Why the parent/child ids matter for RAG

Store each chunk as a vector with `block_id` + parent/child arrays. At query time:
1. Retrieve top-K by vector similarity.
2. Expand each hit by fetching its `block_parent_id` chunks — you now have the enclosing section for LLM context.
3. Optionally pull `block_child_id` chunks for wider recall.

This gives you **hierarchical retrieval without a separate graph store**.

---

## `AnyCodeChunker`

Convenience subclass of `AnyTextChunker` with per-language factory methods.

```python
from anychunker import AnyCodeChunker

# Language-specific factories
AnyCodeChunker.from_python(chunk_size=1000, chunk_overlap=100)
AnyCodeChunker.from_c(chunk_size=1000, chunk_overlap=100)
AnyCodeChunker.from_html(chunk_size=1000, chunk_overlap=100)
AnyCodeChunker.from_markdown(chunk_size=1000, chunk_overlap=100)
```

For languages without a dedicated factory, use `AnyTextChunker.from_language(Language.XXX, ...)` — the underlying separator table (`AnySeparators`) covers 25+ languages.

---

## `AnySentenceChunker`

Sentence-boundary splitter. Handles CJK punctuation (`。！？`) and Latin punctuation (`. ! ?`) out of the box.

```python
from anychunker import AnySentenceChunker

chunker = AnySentenceChunker(chunk_size=500, chunk_overlap=50)
doc = chunker.invoke(text)
```

Use this when you want sentence-atomic chunks (e.g. for reranking or dense passage retrieval where you want small, tight units).

---

## `AnySemanticsChunker`

Splits text by semantic similarity: embeds adjacent sentences and cuts on similarity drop. **Embedding-agnostic** — pass any callable.

### Constructor

```python
AnySemanticsChunker(
    embedding_model: Callable[[List[str]], List[List[float]]],
    breakpoint_threshold: float = 0.5,   # tune per corpus
    # + standard chunk params
)
```

### Example

```python
from anychunker import AnySemanticsChunker
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

def emb(sentences: list[str]) -> list[list[float]]:
    return model.encode(sentences).tolist()

chunker = AnySemanticsChunker(embedding_model=emb)
doc = chunker.invoke(text)
```

Any embedding backend works — OpenAI API, Cohere, local ONNX, custom REST endpoint — as long as the callable returns `List[List[float]]`.

---

## `Language`

Enum of supported languages. Used by `AnyTextChunker.from_language(...)` and `AnyCodeChunker`.

```python
from anychunker import Language

Language.CPP         Language.GO          Language.JAVA        Language.KOTLIN
Language.JS          Language.TS          Language.PHP         Language.PROTO
Language.PYTHON      Language.RST         Language.RUBY        Language.RUST
Language.SCALA       Language.SWIFT       Language.MARKDOWN    Language.LATEX
Language.HTML        Language.SOL         Language.CSHARP      Language.COBOL
Language.C           Language.LUA         Language.PERL        Language.HASKELL
Language.ELIXIR      Language.POWERSHELL
```

---

## Schemas

All schemas inherit from `AnyDataModel` (a Pydantic v2 `BaseModel` with dict-like access, `in`, `len()`, `iter()`, and `created`-aware `__eq__`).

### `Chunker`

One chunk of text.

```python
class Chunker:
    metadata:   Dict[str, Any]   # chunker-specific metadata
    chunk_id:   int
    chunk_size: int
    start_pos:  int              # start offset in original text
    end_pos:    int              # end offset in original text
    content:    str              # the chunk text
```

Dict-like access is supported: `chunk["chunk_id"]`, `"content" in chunk`, `len(chunk)`.

### `DocumentMetadata`

```python
class DocumentMetadata:
    created: datetime.datetime   # auto: creation time
    name:    str = "default"
    topic:   str = "default"
    tag:     str = "default"
    length:  int = 0             # auto-updated with each add_chunk
```

### `Document` (returned by every `invoke`)

```python
class Document:
    metadata: DocumentMetadata
    chunks:   List[Chunker]

    def batchIterator(self, batch_size: int = 10) -> Generator[ChunkBatcher, None, None]: ...
    def add_chunk(self, chunk: Chunker) -> None: ...
    def add_chunks(self, chunks: List[Chunker]) -> None: ...
```

### `ChunkBatcher`

Batch view over `Document.chunks`.

```python
class ChunkBatcher:
    batch_index:          int
    batch_size:           int
    chunks:               List[Chunker]
    metadata:             DocumentMetadata
    actual_size:          int
    total_content_length: int
    start_chunk_id:       int
    end_chunk_id:         int

    def __len__(self) -> int: ...
    def get_content_text(self) -> str: ...
    def get_chunk_ids(self) -> List[int]: ...
    def get_total_size(self) -> int: ...
```
