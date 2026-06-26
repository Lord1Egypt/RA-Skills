# Amber-Hunter RAG 升级协议 v1.2.41

## G2: 接口协议定义

---

## 1. config.json 新增配置项

### 路径
`~/.openclaw/skills/amber-hunter/config.json`

### 新增字段

```json
{
  "llm": {
    "provider": "minimax",
    "model": "gpt-4o"
  },
  "embed_model": "BAAI/bge-m3",
  "embed_dimension": 1024,
  "rerank_model": "BAAI/bge-reranker-v2-m3",
  "bm25_enabled": true,
  "chunk_size": 256,
  "chunk_overlap": 32,
  "hyde_enabled": false,
  "multi_hop_enabled": false
}
```

### 字段说明

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `embed_model` | string | `"BAAI/bge-m3"` | embedding 模型名称，支持多语言 |
| `embed_dimension` | int | `1024` | embedding 向量维度（BGE-M3 为 1024） |
| `rerank_model` | string | `"BAAI/bge-reranker-v2-m3"` | reranker 模型名称 |
| `bm25_enabled` | bool | `true` | 是否启用 BM25 关键词检索 |
| `chunk_size` | int | `256` | 长文本分块大小（字符数） |
| `chunk_overlap` | int | `32` | 相邻块重叠字符数 |
| `hyde_enabled` | bool | `false` | 是否启用 HyDE（假设性答案增强检索） |
| `multi_hop_enabled` | bool | `false` | 是否启用多跳检索 |

---

## 2. /recall API 变更

### 端点
`GET /recall`

### 新增参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `rerank_engine` | string | `"auto"` | 重排序引擎：`auto` \| `model` \| `llm` \| `none` |
| `hyde` | bool | `False` | 是否启用 HyDE（假设性答案增强检索） |
| `multi_hop` | bool | `False` | 是否启用多跳检索（multi-hop reasoning） |

### 原有参数（向后兼容）

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `q` | string | 必填 | 查询文本 |
| `limit` | int | `3` | 返回记忆数量 |
| `mode` | string | `"auto"` | 搜索模式：`keyword` \| `semantic` \| `auto/hybrid` |
| `rerank` | bool | `False` | (deprecated) 等价于 `rerank_engine="llm"` |
| `category_path` | string | `""` | MFS 路径过滤 |
| `use_insights` | bool | `True` | 是否优先返回 insight 缓存 |
| `citation` | int | `0` | 1=返回 embedding 裁剪的片段 |

### 响应新增字段

```json
{
  "memories": [...],
  "query": "...",
  "mode": "hybrid",
  "count": 3,
  "semantic_available": true,
  "citation": false,
  "half_life_days": 30.0,
  "rerank_time_ms": 45.2,
  "hyde_time_ms": 0,
  "retrieval_hops": 1
}
```

| 响应字段 | 类型 | 说明 |
|----------|------|------|
| `rerank_time_ms` | float | reranker 耗时（毫秒），未启用时为 0 |
| `hyde_time_ms` | float | HyDE 生成耗时（毫秒），未启用时为 0 |
| `retrieval_hops` | int | 检索跳数（multi_hop 启用时 > 1） |

---

## 3. /recall/evaluate 新评测端点

### 端点
`POST /recall/evaluate`

### 认证
Bearer Token

### 请求体

```json
{
  "queries": [
    {
      "q": "用户在项目中遇到了什么技术问题？",
      "expected_capsule_ids": ["capsule_id_1", "capsule_id_2"]
    },
    {
      "q": "关于 Python 异步编程的记忆有哪些？",
      "expected_capsule_ids": ["capsule_id_3"]
    }
  ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `queries` | list[QueryItem] | 是 | 查询列表 |
| `QueryItem.q` | string | 是 | 查询文本 |
| `QueryItem.expected_capsule_ids` | list[string] | 是 | 期望召回的胶囊 ID 列表 |

### 响应体

```json
{
  "ragas_scores": {
    "faithfulness": 0.847,
    "answer_relevancy": 0.762,
    "context_precision": 0.891
  },
  "ndcg_at_5": 0.823,
  "evaluated_at": "2026-04-09T01:00:00Z",
  "total_queries": 2
}
```

| 响应字段 | 类型 | 说明 |
|----------|------|------|
| `ragas_scores` | dict | RAGAS 评估指标 |
| `ragas_scores.faithfulness` | float | 答案忠实度（0-1） |
| `ragas_scores.answer_relevancy` | float | 答案相关性（0-1） |
| `ragas_scores.context_precision` | float | 上下文精确度（0-1） |
| `ndcg_at_5` | float | NDCG@5 分数（0-1） |
| `evaluated_at` | string | 评测时间（ISO 8601） |
| `total_queries` | int | 评测查询总数 |

### 错误响应

```json
{
  "error": "RAGAS not installed",
  "code": "RAGAS_UNAVAILABLE",
  "detail": "Please install ragas: pip install ragas"
}
```

---

## 4. 新增 core 模块接口

### 4.1 core/embedding.py — BGE-M3 Embedding Provider

```python
class BGEProvider(EmbedProvider):
    """BAAI/bge-m3 本地模型 via sentence-transformers."""
    
    def encode(self, texts: Union[str, list[str]]) -> np.ndarray:
        """Encode text(s) into 1024-dim embedding vectors."""
        
    def encode_chunks(self, text: str) -> list[list[float]]:
        """Chunk long text and return embeddings for each chunk.
        
        Algorithm: split by sentence boundaries, respect chunk_size.
        Returns list of chunk embeddings.
        """
```

### 4.2 core/bm25.py — BM25 Searcher

```python
class BM25Searcher:
    def __init__(self, corpus: list[str] = None):
        """Initialize with optional corpus."""
        
    def add_documents(self, documents: list[str]) -> None:
        """Add documents to the BM25 index."""
        
    def search(self, query: str, top_k: int = 10) -> list[tuple[int, float]]:
        """Search for top_k documents.
        
        Returns: list of (doc_index, score) tuples, sorted by score desc.
        """
```

### 4.3 core/reranker.py — Cross-Encoder Reranker

```python
class Reranker:
    """BAAI/bge-reranker-v2-m3 本地模型 reranker."""
    
    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3"):
        """Load reranker model. Auto-downgrade on failure."""
        
    def rerank(self, query: str, documents: list[str], top_k: int = 10) -> list[tuple[int, float]]:
        """Rerank documents by relevance to query.
        
        Returns: list of (doc_index, score) tuples, sorted by score desc.
        Falls back to original order on model failure.
        """
```

### 4.4 core/hyde.py — HyDE Generator

```python
class HyDEGenerator:
    """Hypothetical Document Embeddings — generate hypothetical answer, then retrieve."""
    
    def __init__(self):
        """Initialize HyDE with LLM for hypothetical answer generation."""
        
    def generate(self, query: str) -> str:
        """Generate a hypothetical answer to the query.
        
        Uses LLM to produce a plausible (but potentially incorrect) answer.
        """
        
    def retrieve(self, query: str, hyde_answer: str) -> list[str]:
        """Dual retrieval: query + hyde_answer, merge results.
        
        Returns merged list of retrieved document texts.
        """
```

---

## 5. 多跳检索协议（Multi-Hop）

当 `multi_hop=true` 时：

1. **第一跳**：用 query 直接检索，获取 top-K 候选胶囊
2. **扩展**：从候选胶囊提取实体/概念，构造扩展查询
3. **第二跳**：用扩展查询再次检索
4. **合并**：两跳结果按 score 合并去重

### 响应格式
```json
{
  "retrieval_hops": 2,
  "memories": [...],
  "hops": [
    {"hop": 1, "query": "原始查询", "retrieved_ids": ["id1", "id2"]},
    {"hop": 2, "query": "扩展查询", "retrieved_ids": ["id3"]}
  ]
}
```

---

## 6. 向后兼容性保证

- 所有新增参数均有默认值，不影响现有调用
- `rerank_engine="auto"` 行为与原有 `rerank=false` 一致
- BM25/Reranker/HyDE 功能默认关闭（feature flags）
- 响应中新增字段不影响现有解析逻辑
