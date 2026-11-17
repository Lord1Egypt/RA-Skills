---
name: anychunker-skills
description: 使用 `anychunker` Python 库为 LLM / RAG / Agent 管线切分任意文本。触发场景：用户要求切分（chunk / split / segment）文本、Markdown、代码或长文档；提到 "chunk_size / chunk_overlap"；需要搭建 RAG 入库管线；需要在切分时保留 Markdown 结构（代码块 / 表格 / 标题）；需要基于语义 / 句子 / token / 标题的切分；或直接提到 `anychunker`、`AnyMarkdownBlockChunker`、`AnyTextChunker`、`AnyMarkdownChunker`、`AnySemanticsChunker`、`AnySentenceChunker`、`AnyCodeChunker` 中的任何一个。
version: 1.0.0
author: AnyForge
---

# AnyChunker 技能

> **Language**: [English](SKILL.md) · [简体中文](SKILL_zh.md)

使用 `anychunker` 为 LLM / RAG / Agent 管线切分任意文本。

**核心卖点**：**结构感知的块级 Markdown 切分**——代码块、表格、HTML 块保持完整，每个 chunk 还带上父/子索引树，后续检索时可重建层级上下文，是高质量 RAG 检索层的首选。

## 工作流

1. **验证安装** —— 跑 `python scripts/verify_install.py`，确认 `anychunker` 可导入并列出可选依赖（见 [环境自检](#环境自检)）。
2. **选对 Chunker** —— 对照 [Chunker 选型矩阵](#chunker-选型矩阵) 匹配用户意图。拿不准就问一句"要不要保留 Markdown 代码块 / 表格结构？"——这一问通常足以定案。
3. **只加载需要的 API 段落** —— `references/api-reference.md` 内容很长，grep 到类名后只读那一节。
4. **写最小可用示例** —— 不要把所有参数堆出来。从 `chunk_size` + `chunk_overlap` + 默认值起步，只在用户明确要求时才加 tokenizer / language / embedding。
5. **真实运行验证** —— 实际执行脚本，打印 `len(doc.chunks)`、首尾 chunk 的 `content` 预览以及用户关心的 metadata。**绝不编造输出**。
6. **干净交接** —— RAG 入库场景用 `document.batchIterator(batch_size=N)` 喂下游（embedding API、向量库），见 [批量迭代](#批量迭代)。

## 安装

`anychunker` 在 PyPI 上，需要 Python ≥ 3.7。

```bash
pip install anychunker
```

可选扩展（**只有真需要才装**）：

| 用途 | 安装命令 |
|---|---|
| `AnyTextChunker.from_tokenizer("...")` —— 用 HuggingFace tokenizer 做 token 精确切分 | `pip install transformers`（已是硬依赖，但 tokenizer 模型本身首次使用时下载） |
| `AnySemanticsChunker` —— 需要一个 embedding 函数 | `pip install sentence-transformers`（或任何 embedding 后端） |
| 用 jieba 做中文分词长度统计 | `pip install jieba` |

macOS / Linux / Windows 命令完全一致。Windows 上用 PowerShell 或 cmd 都行，`pip install` 命令不变。

### 环境自检

自带的验证脚本，纯 Python，macOS / Linux / Windows 三平台不改一行代码即可运行：

```bash
python scripts/verify_install.py
```

它会打印：
- `anychunker` 版本 + 安装路径
- 可选依赖（`transformers` / `sentence-transformers` / `jieba`）是否可导入
- 一个端到端的最小烟测（切一段 3 行 Markdown）

如果 `anychunker` 没装，脚本以 exit code `1` 退出并打印精确的安装命令——**不要替用户运行 `pip install`**，把命令展示给他，等他确认。

## Chunker 选型矩阵

先按下表选类，然后**只读** `references/api-reference.md` 中对应的那一节。

| 用户意图 | 类 | 选它的原因 |
|---|---|---|
| 切分 Markdown 且保留代码块 / 表格 / HTML；RAG 需要父/子层级关系 | **`AnyMarkdownBlockChunker`** ⭐ | 块级切分，结构感知，chunk 带 `block_parent_id` / `block_child_id` / `chunk_parent_id` / `chunk_child_id` |
| 通用递归文本切分（段落 → 行 → 句 → 字符） | `AnyTextChunker` | 递归分隔符回退，`length_function` 可插拔 |
| Token 精确切分（GPT-4 / Claude / Qwen 等的成本控制） | `AnyTextChunker.from_tokenizer("<HF model>")` | 用真实 HF tokenizer 计数 |
| 中文分词长度 | `AnyTextChunker(..., length_function=jieba_length)` | 用户自定义长度函数，见 recipes |
| 代码切分（Python / JS / Go / Rust / Java / C++ / …） | `AnyTextChunker.from_language(Language.PYTHON, ...)` 或 `AnyCodeChunker.from_python(...)` | 用语言专属分隔符（`class`, `def`, `func`, `fn`, `\nfunction ` …） |
| 简单按 Markdown 标题扁平切（类似 LangChain 的 `MarkdownHeaderTextSplitter`） | `AnyMarkdownChunker` | 只按标题切，扁平 chunk 带 header metadata |
| 按句子边界切分 | `AnySentenceChunker` | 感知 CJK + Latin 标点 |
| 按语义相似度切分（嵌入相邻句子，相似度骤降处切） | `AnySemanticsChunker` | 嵌入无关——接受任意 callable |

## 核心导入

一切从顶层包导入。`__init__.py` 用了懒加载——单独 `import anychunker` **不会**触发 `transformers` / `torch`，重量级依赖只在你真调用相关类时才加载。

```python
from anychunker import (
    AnyTextChunker,             # 递归文本切分
    AnyMarkdownChunker,         # 按标题切 Markdown
    AnyMarkdownBlockChunker,    # 块级 Markdown 切分（★ RAG 首选）
    AnyCodeChunker,             # 按语言切代码
    AnySentenceChunker,         # 按句子切分
    AnySemanticsChunker,        # 语义切分
    Language,                   # 枚举：PYTHON / JS / GO / RUST / MARKDOWN / HTML / ...
    Chunker,                    # schema：单个 chunk
    DocumentMetadata,           # schema：文档级 metadata
    ChunkBatcher,               # schema：一批 chunk
)
```

## 最小用例 —— 四种最常见路径

### 1. 结构感知 Markdown 切分（RAG 推荐默认值）

```python
from anychunker import AnyMarkdownBlockChunker

chunker = AnyMarkdownBlockChunker(chunk_size=500, chunk_overlap=50)
doc = chunker.invoke(markdown_text)

for c in doc.chunks:
    print(c.chunk_id, c.metadata.get("title"), c.content[:60])
```

每个 chunk 的 `metadata` 里挂着 `block_id`、`title`、`headings`、完整的 `block_parent_id` / `block_child_id` 数组——存入向量库后可用于重建层级检索上下文。

### 2. 递归文本切分（速度快，零外部依赖）

```python
from anychunker import AnyTextChunker

chunker = AnyTextChunker(chunk_size=500, chunk_overlap=50)
doc = chunker.invoke(long_text)
```

默认分隔符针对中英混排调过（`\n\n`, `\n`, `。`, ` `, `""`）。需要时传 `separators=[...]` 覆盖。

### 3. 特定 LLM 的 token 精确切分

```python
chunker = AnyTextChunker.from_tokenizer(
    "Qwen/Qwen3-8B",   # 任意 HuggingFace tokenizer id 或本地路径
    chunk_size=1024,
    chunk_overlap=100,
)
doc = chunker.invoke(text)
```

此时 `chunk_size` 的**单位是 token**（不是字符）。

### 4. 语义切分

```python
from anychunker import AnySemanticsChunker
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")
def emb(sentences): return model.encode(sentences).tolist()

chunker = AnySemanticsChunker(embedding_model=emb)
doc = chunker.invoke(text)
```

任何返回 `List[List[float]]` 的 callable 都行——不绑定 `sentence-transformers`。

## 批量迭代

每次 `invoke()` 返回一个 `Document`。要按批次喂下游（embedding API 限速、向量库批量插入）：

```python
for batch in doc.batchIterator(batch_size=16):
    # batch 是 ChunkBatcher，包含：
    #   batch.chunks               → List[Chunker]
    #   batch.get_content_text()   → 拼接后的内容
    #   batch.get_chunk_ids()      → [chunk_id, ...]
    #   batch.total_content_length → int
    embeddings = my_embed_api([c.content for c in batch.chunks])
    my_vector_db.upsert(batch.get_chunk_ids(), embeddings)
```

## 快速演示

跑自带的 demo，端到端看 `AnyMarkdownBlockChunker` 的效果（macOS / Linux / Windows 通用）：

```bash
python scripts/quick_demo.py
```

它会切一段混合 Markdown（标题 + 代码块 + HTML 表格），打印每个 chunk 的 `chunk_id`、`title`、`content` 预览以及父/子块 id，让你亲眼看到层级树。

## 参数速查

除非另注明，所有 chunker 通用：

| 参数 | 默认值 | 说明 |
|---|---|---|
| `chunk_size` | `2048` | 目标大小——单位取决于 `length_function`（默认字符数，`from_tokenizer` 后是 token 数） |
| `chunk_overlap` | `200` | 必须 `<` `chunk_size`；相邻 chunk 的重叠 |
| `separators` | CJK 友好列表 | 递归回退切分顺序 |
| `length_function` | `len` | 任意 `Callable[[str], int]`——可换成 jieba、HF tokenizer、tiktoken 等 |
| `keep_separator` | `True` | `True` / `False` / `"start"` / `"end"` |
| `is_separator_regex` | `False` | 分隔符含正则时设 `True` |
| `strip_whitespace` | `True` | 剥离每个 chunk 首尾空白 |

**`AnyMarkdownBlockChunker` 专属参数**见 `references/api-reference.md#anymarkdownblockchunker`。

## 常见坑

| 症状 | 原因 | 处理 |
|---|---|---|
| `ValueError: Chunk size cannot be less than chunk overlap.` | `chunk_overlap >= chunk_size` | 保证 `chunk_overlap < chunk_size` |
| `AnyTextChunker` 把代码块从中间切开 | Markdown 用错了 chunker | 换 `AnyMarkdownBlockChunker` |
| Markdown 的标题从 chunk 的 `content` 里"消失" | **设计如此**——`AnyMarkdown{,Block}Chunker` 会把标题剥离到 `metadata.title` / `metadata.headings`，只切正文 | 从 `chunk.metadata` 读标题（它们是结构化保存的，没丢失）；要保留原始标题就换 `AnyTextChunker.from_language(Language.MARKDOWN, ...)` |
| 短 Markdown 例如 `# h1\n## h2\nsss` 只切出 1 个 chunk | Markdown chunker 只计正文——`sss` 是唯一正文节点 | 符合预期，两个标题在那唯一 chunk 的 `metadata.title` / `metadata.headings` 里 |
| `chunk_size=500` 结果 chunk 非常小 | 用了 `from_tokenizer`，单位是 token 不是字符 | 增大 `chunk_size` 或去掉 `from_tokenizer` |
| macOS 首次导入很慢 / 拉 torch | 触发了 `AnyTextChunker.from_tokenizer` 或 `AnySemanticsChunker` | 懒加载只在你不调用这些时生效，属于预期行为 |
| `doc.chunks` 为空 | 输入为空或被完全 strip 掉了 | 检查 `strip_whitespace` 和输入 |
| 中文文本切分边界怪异 | 用了英文默认分隔符 | 保持默认 CJK 列表，或传 `separators=["\n\n","\n","。","！","？"," ",""]` |
| Windows 上 `sentence-transformers` 首次运行报错 | 模型下载路径含空格 | 用 `HF_HOME` 环境变量指到短路径（如 `C:\hf` 或 `/tmp/hf`） |

## Recipes（实战配方）

更多端到端配方（RAG 入库、jieba 长度、代码切分、语义调参）在 `references/recipes.md`。按用户问题 grep 到那一节，只读那一节。

## 链接

- PyPI：<https://pypi.org/project/anychunker/>
- GitHub：<https://github.com/anyforge/anychunker>
- DeepWiki：<https://deepwiki.com/anyforge/anychunker/>
