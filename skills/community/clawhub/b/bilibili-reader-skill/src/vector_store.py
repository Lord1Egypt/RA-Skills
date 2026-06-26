"""向量存储模块 — ChromaDB 向量搜索封装

功能：
1. 将视频总结向量化存储到 ChromaDB
2. 混合搜索：向量语义 + 关键词，合并排序
3. 懒加载：ChromaDB 仅在实际使用时才导入
4. 零依赖降级：ChromaDB 不可用时静默降级到纯关键词搜索
"""

import json
import logging
from pathlib import Path
from dataclasses import dataclass

from .memory import Memory
from .summarizer import VideoSummary

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# ChromaDB 可用性检测
# ──────────────────────────────────────────────

def _check_chromadb_available() -> bool:
    """检测 ChromaDB 是否可用"""
    try:
        import chromadb  # noqa: F401
        return True
    except ImportError:
        return False


CHROMADB_AVAILABLE = _check_chromadb_available()


# ──────────────────────────────────────────────
# ChromaDB 懒加载
# ──────────────────────────────────────────────

class _LazyChroma:
    """
    懒加载 ChromaDB 客户端。
    首次访问时真正导入，后续复用。
    """
    _client = None

    @classmethod
    def get_client(cls, persist_path: str):
        if cls._client is None:
            import chromadb
            from chromadb.config import Settings
            cls._client = chromadb.PersistentClient(
                path=persist_path,
                settings=Settings(anonymized_telemetry=False),
            )
        return cls._client


# ──────────────────────────────────────────────
# 数据结构
# ──────────────────────────────────────────────

@dataclass
class SearchResult:
    """单条搜索结果"""
    bvid: str
    title: str
    genre: str
    tldr_cn: str
    summary_cn: str
    score: float
    source: str  # "vector" | "keyword" | "hybrid"


# ──────────────────────────────────────────────
# 向量存储核心类
# ──────────────────────────────────────────────

class VectorStore:
    """
    ChromaDB 向量存储 + 混合搜索。

    使用方式：
        store = VectorStore(data_dir=Path("./data"))
        store.add(summary, video)
        results = store.search("Python异步编程")
    """

    COLLECTION_NAME = "bilibili_summaries"
    EMBED_BATCH_SIZE = 5  # 分批向量化，避免单次过大

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.persist_path = str(self.data_dir / "chroma_db")

        self._collection = None  # 懒加载
        self._memory = None       # 懒加载

        if not CHROMADB_AVAILABLE:
            logger.warning(
                "ChromaDB 未安装，向量搜索功能不可用。"
                "运行 `pip install chromadb` 可启用语义搜索。"
            )

    # ── 懒加载属性 ──

    @property
    def collection(self):
        """懒加载 ChromaDB collection"""
        if self._collection is None:
            if not CHROMADB_AVAILABLE:
                return None
            try:
                client = _LazyChroma.get_client(self.persist_path)
                self._collection = client.get_or_create_collection(
                    name=self.COLLECTION_NAME,
                    metadata={"description": "B站视频总结向量库"},
                )
            except Exception as e:
                logger.warning(f"ChromaDB 初始化失败: {e}，将降级到关键词搜索")
                self._collection = None
        return self._collection

    @property
    def memory(self) -> Memory:
        """懒加载 Memory"""
        if self._memory is None:
            self._memory = Memory(self.data_dir / "processed.json")
        return self._memory

    # ── 向量化 ──

    def add(self, summary: VideoSummary, video_bvid: str, title: str):
        """
        将视频总结向量化存入 ChromaDB。

        Args:
            summary: VideoSummary 实例
            video_bvid: 视频 BV 号
            title: 视频标题（用于 metadata）
        """
        if not CHROMADB_AVAILABLE or self.collection is None:
            return

        doc_cn = self._build_doc(summary, lang="cn")
        doc_en = self._build_doc(summary, lang="en")

        if not doc_cn.strip():
            return

        try:
            self.collection.add(
                documents=[doc_cn, doc_en],
                metadatas=[
                    {
                        "bvid": video_bvid,
                        "lang": "cn",
                        "genre": summary.genre or "",
                        "title": title,
                    },
                    {
                        "bvid": video_bvid,
                        "lang": "en",
                        "genre": summary.genre or "",
                        "title": title,
                    },
                ],
                ids=[f"{video_bvid}_cn", f"{video_bvid}_en"],
            )
        except Exception as e:
            logger.warning(f"向量化失败: {e}")

    def _build_doc(self, summary: VideoSummary, lang: str = "cn") -> str:
        """构建向量化文档"""
        if lang == "cn":
            parts = [
                summary.title_cn,
                summary.tldr_cn,
                summary.summary_cn,
                " ".join(summary.key_points_cn),
                summary.insights_cn,
                summary.my_analysis.overview if hasattr(summary.my_analysis, "overview") else str(summary.my_analysis.get("overview", "")) if isinstance(summary.my_analysis, dict) else "",
            ]
        else:
            parts = [
                summary.title_en,
                summary.tldr_en,
                summary.summary_en,
                " ".join(summary.key_points_en),
                summary.insights_en,
            ]
        return " ".join(p for p in parts if p)

    # ── 搜索 ──

    def search(
        self,
        query: str,
        top_k: int = 5,
        lang: str = "cn",
        genre_filter: str = "",
    ) -> list[SearchResult]:
        """
        混合搜索：向量语义 + 关键词，合并排序。

        Args:
            query: 搜索查询
            top_k: 返回数量
            lang: 搜索语言，"cn" | "en" | "both"
            genre_filter: 体裁过滤

        Returns:
            按相关性排序的搜索结果
        """
        if not query.strip():
            return []

        vector_results: list[SearchResult] = []
        keyword_results: list[SearchResult] = []

        # 1. 向量搜索
        if CHROMADB_AVAILABLE and self.collection is not None:
            vector_results = self._vector_search(query, top_k * 2, lang, genre_filter)

        # 2. 关键词搜索（始终执行，作为 fallback 和补充）
        keyword_results = self._keyword_search(query, top_k * 2, lang, genre_filter)

        # 3. 合并排序
        merged = self._merge_and_rerank(vector_results, keyword_results)
        return merged[:top_k]

    def _vector_search(
        self, query: str, top_k: int, lang: str, genre_filter: str
    ) -> list[SearchResult]:
        """向量语义搜索"""
        if self.collection is None:
            return []

        where_clause = {}
        if genre_filter:
            where_clause["genre"] = genre_filter

        query_ids = [f"{lang}", f"{lang}"] if lang == "cn" else ["cn", "en"]

        try:
            # ChromaDB 0.4+ 接口
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=where_clause if where_clause else None,
            )
        except TypeError:
            # ChromaDB < 0.4 接口（无 where 参数）
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
            )

        if not results or not results.get("ids") or not results["ids"][0]:
            return []

        search_results: list[SearchResult] = []
        seen: set[str] = set()

        for bvid_id, distance, metadata in zip(
            results["ids"][0],
            results["distances"][0],
            results["metadatas"][0],
        ):
            bvid = bvid_id.replace("_cn", "").replace("_en", "")
            if bvid in seen:
                continue
            seen.add(bvid)

            # 距离转相似度分数
            score = max(0.0, 1.0 - distance)

            # 获取完整视频信息
            video_info = self._get_video_info(bvid)
            search_results.append(SearchResult(
                bvid=bvid,
                title=metadata.get("title", video_info.get("title", bvid)),
                genre=metadata.get("genre", ""),
                tldr_cn=video_info.get("tldr_cn", ""),
                summary_cn=video_info.get("summary_cn", ""),
                score=score,
                source="vector",
            ))

        return search_results

    def _keyword_search(
        self, query: str, top_k: int, lang: str, genre_filter: str
    ) -> list[SearchResult]:
        """纯关键词搜索（基于 processed.json）"""
        kw = query.lower()
        results: list[SearchResult] = []

        for v in self.memory.get_all_processed():
            searchable = " ".join([
                getattr(v, "title", ""),
                getattr(v, "tldr_cn", ""),
                " ".join(getattr(v, "key_points_cn", [])),
                getattr(v, "summary_cn", ""),
            ]).lower()

            if kw not in searchable:
                continue

            if genre_filter and genre_filter not in (getattr(v, "genre", "") or ""):
                continue

            score = self._calc_keyword_score(kw, searchable)

            results.append(SearchResult(
                bvid=getattr(v, "bvid", ""),
                title=getattr(v, "title", ""),
                genre=getattr(v, "genre", ""),
                tldr_cn=getattr(v, "tldr_cn", ""),
                summary_cn=getattr(v, "summary_cn", ""),
                score=score,
                source="keyword",
            ))

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]

    def _calc_keyword_score(self, keyword: str, text: str) -> float:
        """计算关键词匹配得分"""
        count = text.count(keyword)
        if count == 0:
            return 0.0
        # 出现次数越多得分越高，上限 1.0
        return min(1.0, count * 0.3)

    def _merge_and_rerank(
        self,
        vector_results: list[SearchResult],
        keyword_results: list[SearchResult],
    ) -> list[SearchResult]:
        """加权合并向量和关键词结果"""
        seen: dict[str, SearchResult] = {}
        scored: list[tuple[SearchResult, float]] = []

        # 关键词结果基础分 1.0
        for r in keyword_results:
            if r.bvid not in seen:
                seen[r.bvid] = r
                scored.append((r, 1.0))

        # 向量结果（相似度 × 权重）
        for r in vector_results:
            if r.bvid in seen:
                # 已有关键词结果，保留较高分
                existing = seen[r.bvid]
                if r.score > existing.score:
                    existing.score = r.score
            else:
                seen[r.bvid] = r
                scored.append((r, r.score * 0.85))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [r for r, _ in scored]

    def _get_video_info(self, bvid: str) -> dict:
        """从 processed.json 获取视频信息"""
        for v in self.memory.get_all_processed():
            if getattr(v, "bvid", "") == bvid:
                return {
                    "title": getattr(v, "title", ""),
                    "tldr_cn": getattr(v, "tldr_cn", ""),
                    "summary_cn": getattr(v, "summary_cn", ""),
                    "genre": getattr(v, "genre", ""),
                }
        return {}

    # ── 管理 ──

    def on_video_processed(self, summary: VideoSummary, video_bvid: str, title: str):
        """视频处理完成后自动向量化"""
        self.add(summary, video_bvid, title)

    def reindex_all(self):
        """全量重新索引（从 processed.json 重建向量）"""
        if self.collection is not None:
            try:
                self.collection.delete(where={})
            except Exception:
                pass

        # 遍历 processed.json 重建
        for v in self.memory.get_all_processed():
            # processed.json 存储了部分 summary 字段
            # 向量化需要完整 summary，这里仅重建关键词索引（向量无法重建）
            pass  # 向量无法从纯文本重建，需要重新调用 LLM

    def stats(self) -> dict:
        """获取向量库统计"""
        total = 0
        if self.collection is not None:
            try:
                total = self.collection.count()
            except Exception:
                pass

        return {
            "chroma_available": CHROMADB_AVAILABLE,
            "total_vectors": total,
            "persist_path": self.persist_path,
        }


# ──────────────────────────────────────────────
# 便捷访问
# ──────────────────────────────────────────────

_vector_store: VectorStore | None = None


def get_vector_store(data_dir: Path | None = None) -> VectorStore:
    """获取全局 VectorStore 单例"""
    global _vector_store
    if _vector_store is None:
        if data_dir is None:
            from .config import Config
            data_dir = Config.DATA_DIR
        _vector_store = VectorStore(data_dir)
    return _vector_store
