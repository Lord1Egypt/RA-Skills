"""
vector_retriever.py — 从 LanceDB 向量库检索记忆

功能：
- 根据用户 query 语义检索已导入的 markdown 记忆
- 与 MemoryManager 记忆层融合
- 支持自定义召回数量和相似度阈值
- 支持本地 embedding（sentence-transformers）和 OpenAI 两种模式
"""

import os
from dataclasses import dataclass
from typing import Optional, List

# sentence-transformers 本地 embedding（可选）
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


@dataclass
class RetrievedChunk:
    """检索到的记忆块"""
    chunk_id: str
    source_file: str
    title: str
    heading: str
    content: str
    score: float  # 相似度分数 0-1


class VectorRetriever:
    """
    从 LanceDB 向量库检索 markdown 记忆
    与 MemoryManager 共享同一个 LanceDB 实例
    """

    # 默认本地 embedding 模型（sentence-transformers）
    DEFAULT_LOCAL_MODEL = "all-MiniLM-L6-v2"

    def __init__(
        self,
        table_name: str = "memory_chunks",
        db_path: str = "~/.hawk/lancedb",
        top_k: int = 5,
        min_score: float = 0.6,
        base_url: str = None,
        api_key: str = None,
        proxy: str = None,
    ):
        self.table_name = table_name
        self.db_path = os.path.expanduser(db_path)
        self.top_k = top_k
        self.min_score = min_score
        self._base_url = base_url or os.environ.get("OPENAI_BASE_URL")
        self._api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self._proxy = proxy or os.environ.get("OPENAI_PROXY") or os.environ.get("HTTPS_PROXY")
        self._embedding_model = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        self._table = None
        self._openai_client = None
        self._local_model = None

    def _get_table(self):
        """延迟初始化 LanceDB 表"""
        if self._table is not None:
            return self._table
        try:
            import lancedb
        except ImportError:
            raise RuntimeError(
                "LanceDB not installed. Install with: pip install lancedb"
            )
        db = lancedb.connect(self.db_path)
        if self.table_name not in db.table_names():
            return None
        self._table = db.open_table(self.table_name)
        return self._table

    def _get_openai_client(self):
        """延迟初始化 OpenAI 客户端"""
        if self._openai_client is not None:
            return self._openai_client
        if not self._api_key:
            raise RuntimeError("请设置 OPENAI_API_KEY 环境变量或传入 api_key 参数")

        import httpx
        http_client = httpx.Client(proxy=self._proxy) if self._proxy else None
        from openai import OpenAI
        self._openai_client = OpenAI(
            api_key=self._api_key,
            base_url=self._base_url,
            http_client=http_client,
        )
        return self._openai_client

    def _get_local_model(self):
        """延迟初始化 sentence-transformers 本地模型"""
        if self._local_model is not None:
            return self._local_model
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise RuntimeError(
                "sentence-transformers 未安装。运行: pip install sentence-transformers"
            )
        model_name = os.environ.get("SENTENCE_TRANSFORMERS_MODEL", self.DEFAULT_LOCAL_MODEL)
        self._local_model = SentenceTransformer(model_name)
        return self._local_model

    def _get_embedding(self, texts: List[str]) -> List[List[float]]:
        """
        统一 embedding 接口：优先用本地 sentence-transformers，fallback 到 OpenAI
        """
        if SENTENCE_TRANSFORMERS_AVAILABLE and os.environ.get("USE_LOCAL_EMBEDDING") == "1":
            model = self._get_local_model()
            embeddings = model.encode(texts, normalize_embeddings=True)
            # 转为 list 格式
            return embeddings.tolist()

        # Fallback to OpenAI
        client = self._get_openai_client()
        resp = client.embeddings.create(
            model=self._embedding_model,
            input=texts,
        )
        return [item.embedding for item in resp.data]

    def recall(self, query: str) -> list[RetrievedChunk]:
        """
        根据 query 语义检索记忆
        返回 top_k 条最相关的记忆块（按相似度排序）
        """
        table = self._get_table()
        if table is None:
            return []

        # 1. query → embedding
        vectors = self._get_embedding([query])
        vector = vectors[0]

        # 2. LanceDB ANN 检索 (wrap in try/except for dimension mismatch)
        try:
            results = table.search(vector).limit(self.top_k).to_list()
        except RuntimeError as e:
            if 'dim' in str(e).lower():
                raise RuntimeError(
                    f"Embedding dimension mismatch: your embedding model output ({len(vector)} dims) "
                    f"does not match the LanceDB column dimension. "
                    f"Set the correct HAWK_EMBEDDING_DIMENSIONS or EMBEDDING_DIMENSIONS in ~/.hawk/config.json. "
                    f"Original error: {e}"
                )
            raise

        # 3. 过滤低分结果
        chunks = []
        for item in results:
            score = item.get("_score", 0)
            if score < self.min_score:
                continue
            chunks.append(RetrievedChunk(
                chunk_id=item["chunk_id"],
                source_file=item["source_file"],
                title=item.get("title", ""),
                heading=item.get("heading", ""),
                content=item["content"],
                score=score,
            ))

        return chunks

    def format_for_context(self, chunks: list[RetrievedChunk]) -> str:
        """
        将检索结果格式化为可注入上下文的文本
        """
        if not chunks:
            return ""
        lines = ["[记忆检索结果]"]
        for c in chunks:
            tag = f"[{c.source_file}]"
            if c.heading:
                tag += f" {c.heading}"
            lines.append(f"{tag} (相似度 {c.score:.0%}):")
            lines.append(c.content)
            lines.append("")
        return "\n".join(lines)


# 便捷函数
def recall_memory(query: str, top_k: int = 5) -> list[RetrievedChunk]:
    """一行调用：recall_memory('之前做过什么')"""
    retriever = VectorRetriever(top_k=top_k)
    return retriever.recall(query)


# ---- 本地 embedding 接口（供 hawk-bridge TypeScript 调用的便捷函数）----
def embed_texts_local(texts: List[str], model: str = None) -> List[List[float]]:
    """
    使用 sentence-transformers 生成文本向量（纯本地，无需 API）
    供 hawk-bridge 在 TypeScript 侧无 Ollama/API Key 时调用。

    用法（Python subprocess）：
        python3 -c "from hawk.vector_retriever import embed_texts_local; print(embed_texts_local(['hello world']))"

    环境变量：
        USE_LOCAL_EMBEDDING=1  强制使用本地模型
        SENTENCE_TRANSFORMERS_MODEL=all-MiniLM-L6-v2  指定模型
    """
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        raise RuntimeError(
            "sentence-transformers 未安装。运行: pip install sentence-transformers"
        )

    model_name = model or os.environ.get("SENTENCE_TRANSFORMERS_MODEL", "all-MiniLM-L6-v2")
    st_model = SentenceTransformer(model_name)
    embeddings = st_model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()
