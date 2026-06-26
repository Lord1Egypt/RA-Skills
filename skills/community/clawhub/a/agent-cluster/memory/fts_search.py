"""
fts_search.py - FTS5 全文检索增强层

在现有 persistent_store（FTS5 触发器同步）基础上，提供增强检索能力：

1. FTS5Searcher：独立的全文检索封装，支持：
   - 纯关键词搜索（利用已有 FTS5 虚拟表）
   - BM25 排序（SQLite 内置，无需外部依赖）
   - snippet 高亮（maxhermes 风格【】包裹）
   - 搜索结果去重（content_hash）
   - 混合召回（semantic boost，不依赖外部 embedding 服务）

2. HybridSearcher：混合搜索，在 FTS5 基础上：
   - 可注入语义相似度函数（自定义 LLM/embedding）
   - 融合 BM25 关键词分 + 语义分
   - 零外部依赖模式（仅用 FTS5，也完全可用）

不修改 persistent_store.py，作为独立检索层叠加。

依赖：Python 3.10+, sqlite3（标准库）
"""

from __future__ import annotations

import json
import logging
import math
import re
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)

# =============================================================================
# 路径配置
# =============================================================================

DEFAULT_DB_DIR = Path(__file__).parent.parent / "data" / "memory"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "memory.db"


# =============================================================================
# 数据模型
# =============================================================================

@dataclass
class SearchHit:
    """一次检索命中结果"""
    entry_id: str
    content: str
    summary: str
    tags: list[str]
    memory_type: str
    scope: str
    importance: int
    created_at: str

    # FTS 专属
    rank: float = 0.0                 # BM25 排序分（越低越相关）
    snippet: str = ""                 # 高亮片段（【】包裹关键词）
    bm25_score: float = 0.0          # BM25 原始分
    semantic_score: float = 0.0       # 语义相似度（可选）
    combined_score: float = 0.0       # 融合分（可选）

    # 来源信息
    source_agent_id: str = ""
    is_skill_candidate: bool = False   # 是否来自 Skill 候选

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "content": self.content,
            "summary": self.summary,
            "tags": self.tags,
            "memory_type": self.memory_type,
            "scope": self.scope,
            "importance": self.importance,
            "created_at": self.created_at,
            "rank": self.rank,
            "snippet": self.snippet,
            "bm25_score": self.bm25_score,
            "semantic_score": self.semantic_score,
            "combined_score": self.combined_score,
            "source_agent_id": self.source_agent_id,
            "is_skill_candidate": self.is_skill_candidate,
        }


@dataclass
class SearchOptions:
    """检索选项"""
    limit: int = 10                   # 最大返回数量
    offset: int = 0                   # 分页偏移
    min_importance: int = 2          # 最低重要性过滤
    scopes: list[str] = field(default_factory=list)   # 作用域过滤
    memory_types: list[str] = field(default_factory=list)  # 类型过滤
    agent_id: str = ""               # 指定 Agent 过滤
    include_deleted: bool = False    # 是否包含已删除（默认否）

    # FTS5 选项
    use_bm25: bool = True            # 使用 BM25 排序
    snippet_size: int = 5            # snippet 上下文词数
    highlight_open: str = "【"        # 高亮开始标记
    highlight_close: str = "】"       # 高亮结束标记
    prefix_match: bool = True        # 前缀匹配（支持 incomplete 词）

    # 混合搜索
    semantic_weight: float = 0.0      # 语义权重（0=纯关键词）
    semantic_func: Optional[Callable[[str, list[str]], float]] = None


@dataclass
class SearchResult:
    """检索结果集"""
    hits: list[SearchHit]
    total: int                       # 符合条件总数（未分页）
    query: str
    options: SearchOptions
    elapsed_ms: float = 0.0          # 检索耗时
    search_type: str = "fts5"        # fts5 | hybrid

    def to_dict(self) -> dict[str, Any]:
        return {
            "hits": [h.to_dict() for h in self.hits],
            "total": self.total,
            "query": self.query,
            "limit": self.options.limit,
            "offset": self.options.offset,
            "elapsed_ms": self.elapsed_ms,
            "search_type": self.search_type,
        }


# =============================================================================
# BM25 计算工具（SQLite 内置，无需外部库）
# =============================================================================

class BM25Config:
    """BM25 参数（SQLite FTS5 内置 k1/b）"""
    K1 = 1.5
    B = 0.75


def _sqlite_bm25_score(conn: sqlite3.Connection, table: str, query: str) -> dict[str, float]:
    """
    调用 SQLite FTS5 BM25 函数获取排序分。

    SQLite FTS5 内置 BM25 实现：
        bm25(memory_fts, ?, ?)  → (score, rank)
    其中 k1 和 b 为可选参数。
    """
    cursor = conn.execute("""
        SELECT entry_id,
               bm25(memory_fts, ?, ?, ?) AS bm25_score
        FROM memory_fts
        WHERE memory_fts MATCH ?
        ORDER BY bm25_score
        LIMIT 500
    """, (BM25Config.K1, BM25Config.B, query, query))
    return {row[0]: row[1] for row in cursor.fetchall()}


def _build_fts_query(query_text: str, prefix_match: bool = True) -> str:
    """
    构建 FTS5 查询字符串。

    - 多词自动加 OR
    - 前缀匹配：word* 形式
    - 布尔支持：AND / OR / NOT
    """
    terms = query_text.strip().split()
    if not terms:
        return '""'

    parts = []
    for term in terms:
        term = term.strip()
        if not term:
            continue
        # 处理已有布尔操作符
        if term.upper() in ("AND", "OR", "NOT"):
            parts.append(term.upper())
        elif prefix_match:
            parts.append(f'"{term}"*')
        else:
            parts.append(f'"{term}"')
    return " ".join(parts)


def _render_snippet(
    content: str,
    query_terms: list[str],
    size: int = 5,
    open_tag: str = "【",
    close_tag: str = "】",
) -> str:
    """
    在内容中定位查询词附近窗口，渲染 snippet。

    不依赖外部库，纯 Python 实现。
    """
    if not content:
        return ""

    # 找到每个查询词的第一次出现位置
    content_lower = content.lower()
    positions: list[tuple[int, str]] = []
    for term in query_terms:
        pos = content_lower.find(term.lower())
        if pos >= 0:
            positions.append((pos, term))

    if not positions:
        # 未找到精确匹配，取开头
        snippet = content[:200]
    else:
        # 以第一个匹配词为中心
        first_pos = min(p[0] for p in positions)
        start = max(0, first_pos - size * 30)
        end = min(len(content), first_pos + size * 30)
        snippet = content[start:end]
        if start > 0:
            snippet = "…" + snippet
        if end < len(content):
            snippet = snippet + "…"

    # 高亮所有查询词
    for term in query_terms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        snippet = pattern.sub(f"{open_tag}{term}{close_tag}", snippet)

    return snippet


# =============================================================================
# FTS5 检索器
# =============================================================================

class FTS5Searcher:
    """
    SQLite FTS5 全文检索封装。

    直接操作已有 FTS5 虚拟表（由 persistent_store 初始化），
    提供 BM25 排序、snippet 高亮、过滤等功能。

    与 PersistentStore 完全解耦，拥有独立连接管理。

    使用示例：
        searcher = FTS5Searcher()
        result = searcher.search("python 错误处理", limit=5)
        for hit in result.hits:
            print(hit.snippet)
    """

    def __init__(
        self,
        db_path: str = str(DEFAULT_DB_PATH),
    ):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._ensure_fts_ready()

    def _ensure_fts_ready(self) -> None:
        """确保 FTS5 虚拟表存在（幂等初始化）"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        # 仅检查，不重复创建（IF NOT EXISTS）
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='memory_fts'"
        )
        if not cursor.fetchone():
            logger.warning("FTS5 table 'memory_fts' not found; run persistent_store first")
        conn.close()

    def search(self, query: str, **kwargs) -> SearchResult:
        """
        全文检索主入口。

        Args:
            query: 搜索关键词（支持 FTS5 布尔语法）
            **kwargs: SearchOptions 字段（见 SearchOptions）

        Returns:
            SearchResult（含排序后的 hits、总数、耗时）
        """
        import time
        start = time.perf_counter()

        options = SearchOptions(**kwargs) if kwargs else SearchOptions()
        query_terms = query.strip().split()

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        # ---- 构建 FTS5 MATCH 查询 ----
        fts_query = _build_fts_query(query, options.prefix_match)

        # ---- 过滤条件 ----
        conditions = ["me.is_deleted=0"]
        params: list[Any] = []

        if not options.include_deleted:
            conditions.append("me.is_deleted=0")

        if options.scopes:
            placeholders = ",".join(["?"] * len(options.scopes))
            conditions.append(f"me.scope IN ({placeholders})")
            params.extend(options.scopes)

        if options.memory_types:
            placeholders = ",".join(["?"] * len(options.memory_types))
            conditions.append(f"me.memory_type IN ({placeholders})")
            params.extend(options.memory_types)

        if options.agent_id:
            conditions.append("me.agent_id=?")
            params.append(options.agent_id)

        if options.min_importance > 1:
            conditions.append("me.importance>=?")
            params.append(options.min_importance)

        where_clause = " AND ".join(conditions)

        # ---- FTS5 搜索 + BM25 排序 ----
        sql = f"""
            SELECT me.entry_id,
                   me.content,
                   me.summary,
                   me.tags,
                   me.memory_type,
                   me.scope,
                   me.importance,
                   me.created_at,
                   me.agent_id,
                   bm25(memory_fts, ?, ?, ?) AS bm25_score,
                   snippet(memory_fts,
                           1,        -- 1=content column (entry_id=0, content=1, summary=2, tags=3)
                           ?,
                           ?,
                           '…',
                           {options.snippet_size}) AS snippet_text
            FROM memory_entries me
            JOIN memory_fts fts ON me.entry_id = fts.entry_id
            WHERE {where_clause}
              AND memory_fts MATCH ?
            ORDER BY bm25_score
            LIMIT ?
        """
        params = (
            [BM25Config.K1, BM25Config.B, fts_query] +   # BM25: 3 params
            [options.highlight_open, options.highlight_close] +  # snippet: 2 params
            params +                                        # WHERE values: dynamic
            [fts_query, options.limit + options.offset]     # MATCH + LIMIT: 2 params
        )

        try:
            rows = conn.execute(sql, params).fetchall()
        except sqlite3.OperationalError as exc:
            logger.warning(f"FTS5 query failed, falling back to LIKE: {exc}")
            return self._fallback_like_search(query, options, start)

        conn.close()

        # ---- 解析结果 ----
        seen: set[str] = set()
        hits: list[SearchHit] = []

        for row in rows:
            entry_id = row["entry_id"]
            if entry_id in seen:
                continue
            seen.add(entry_id)

            # snippet fallback（SQLite snippet 失败时用 Python 渲染）
            snippet = row["snippet_text"] or _render_snippet(
                row["content"], query_terms,
                options.snippet_size, options.highlight_open, options.highlight_close
            )

            # 判断是否 Skill 候选（tag 中含 skill-candidate）
            tags = json.loads(row["tags"]) if isinstance(row["tags"], str) else row["tags"]
            is_skill = "skill-candidate" in tags

            hit = SearchHit(
                entry_id=entry_id,
                content=row["content"],
                summary=row["summary"] or "",
                tags=tags,
                memory_type=row["memory_type"],
                scope=row["scope"],
                importance=row["importance"],
                created_at=row["created_at"],
                rank=float(row["bm25_score"]) if row["bm25_score"] else 0.0,
                snippet=snippet,
                bm25_score=float(row["bm25_score"]) if row["bm25_score"] else 0.0,
                semantic_score=0.0,
                combined_score=float(row["bm25_score"]) if row["bm25_score"] else 0.0,
                source_agent_id=row["agent_id"],
                is_skill_candidate=is_skill,
            )
            hits.append(hit)

        # 分页
        total = len(hits)
        hits = hits[options.offset:options.offset + options.limit]

        elapsed_ms = (time.perf_counter() - start) * 1000

        return SearchResult(
            hits=hits,
            total=total,
            query=query,
            options=options,
            elapsed_ms=round(elapsed_ms, 2),
            search_type="fts5",
        )

    def _fallback_like_search(
        self,
        query: str,
        options: SearchOptions,
        start: float,
    ) -> SearchResult:
        """FTS5 查询失败时的 LIKE 回退"""
        import time

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        query_terms = query.strip().split()
        conditions = ["is_deleted=0"]
        params: list[Any] = []

        # 构建 LIKE 子句
        like_clauses = []
        for term in query_terms:
            like_clauses.append("(content LIKE ? OR summary LIKE ? OR tags LIKE ?)")
            like_param = f"%{term}%"
            params.extend([like_param, like_param, like_param])

        where_clause = f"({' OR '.join(like_clauses)})" if like_clauses else "1=1"

        rows = conn.execute(f"""
            SELECT * FROM memory_entries
            WHERE {where_clause}
            ORDER BY importance DESC, accessed_at DESC
            LIMIT ?
        """, params + [options.limit + options.offset]).fetchall()
        conn.close()

        hits = [
            SearchHit(
                entry_id=row["entry_id"],
                content=row["content"],
                summary=row["summary"] if row["summary"] else "",
                tags=json.loads(row["tags"]) if isinstance(row["tags"], str) else [],
                memory_type=row["memory_type"],
                scope=row["scope"],
                importance=row["importance"],
                created_at=row["created_at"],
                rank=idx,
                snippet=_render_snippet(
                    row["content"], query_terms,
                    options.snippet_size, options.highlight_open, options.highlight_close
                ),
            )
            for idx, row in enumerate(rows)
        ]

        total = len(hits)
        hits = hits[options.offset:options.offset + options.limit]
        elapsed_ms = (time.perf_counter() - start) * 1000

        return SearchResult(
            hits=hits, total=total, query=query, options=options,
            elapsed_ms=round(elapsed_ms, 2), search_type="fts5_like_fallback",
        )

    def count(self, query: str = "") -> int:
        """返回符合查询的记忆条目总数（用于分页）"""
        conn = sqlite3.connect(self.db_path)
        if query:
            fts_query = _build_fts_query(query)
            cursor = conn.execute("""
                SELECT COUNT(*) FROM memory_entries me
                JOIN memory_fts fts ON me.entry_id = fts.entry_id
                WHERE me.is_deleted=0 AND memory_fts MATCH ?
            """, (fts_query,))
        else:
            cursor = conn.execute(
                "SELECT COUNT(*) FROM memory_entries WHERE is_deleted=0"
            )
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_skill_candidates(self, limit: int = 20) -> list[SearchHit]:
        """快速获取所有 Skill 候选（用于 Dreaming 引擎）"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT me.* FROM memory_entries me
            WHERE me.is_deleted=0
              AND me.tags LIKE '%skill-candidate%'
            ORDER BY me.importance DESC, me.created_at DESC
            LIMIT ?
        """, (limit,)).fetchall()
        conn.close()

        return [
            SearchHit(
                entry_id=row["entry_id"],
                content=row["content"],
                summary=row["summary"] if row["summary"] else "",
                tags=json.loads(row["tags"]) if isinstance(row["tags"], str) else [],
                memory_type=row["memory_type"],
                scope=row["scope"],
                importance=row["importance"],
                created_at=row["created_at"],
                source_agent_id=row["agent_id"],
                is_skill_candidate=True,
            )
            for row in rows
        ]


# =============================================================================
# 混合搜索器（FTS5 + 语义）
# =============================================================================

class HybridSearcher:
    """
    混合搜索器：在 FTS5 基础上融合语义相似度。

    支持三种模式：
    1. pure_fts  — 纯 FTS5 BM25 搜索（无需任何外部依赖）
    2. keyword_first  — 关键词优先，语义 boost
    3. semantic_first  — 语义优先，关键词兜底

    语义函数接口：
        semantic_func(query: str, candidates: list[str]) -> list[float]
        输入：原始查询 + 待评分内容列表
        输出：与查询等长的相似度分数列表（0-1 越高质量越好）

    使用示例：
        def my_embedding(query, texts):
            # 你的 embedding 服务
            return scores

        searcher = HybridSearcher(semantic_func=my_embedding)
        result = searcher.search("python 异步任务", mode="keyword_first", semantic_weight=0.4)
    """

    def __init__(
        self,
        db_path: str = str(DEFAULT_DB_PATH),
        fts_weight: float = 1.0,
    ):
        self._fts = FTS5Searcher(db_path)
        self._fts_weight = fts_weight

    def search(
        self,
        query: str,
        mode: str = "pure_fts",
        semantic_weight: float = 0.5,
        semantic_func: Optional[Callable[[str, list[str]], list[float]]] = None,
        **kwargs,
    ) -> SearchResult:
        """
        混合检索主入口。

        Args:
            query: 搜索关键词
            mode: 搜索模式
                - "pure_fts"：纯 FTS5 BM25（默认）
                - "keyword_first"：FTS5 为主要排序，语义作 boost
                - "semantic_first"：语义相似度为主，FTS5 结果兜底
            semantic_weight: 语义分在融合分中的权重（0-1）
            semantic_func: 语义评分函数，可选
            **kwargs: SearchOptions 字段

        Returns:
            SearchResult（含融合排序的 hits）
        """
        import time
        start = time.perf_counter()

        options = SearchOptions(**kwargs) if kwargs else SearchOptions()

        if mode == "pure_fts" or not semantic_func:
            result = self._fts.search(query, **kwargs)
            result.search_type = "pure_fts"
            result.elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
            return result

        # ---- 混合模式 ----
        # Step 1: 用 FTS5 快速召回候选（扩大 limit 留出语义重排空间）
        candidates_limit = (options.limit + options.offset) * 4
        fts_result = self._fts.search(query, **{**kwargs, "limit": candidates_limit})
        if not fts_result.hits:
            fts_result.elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
            fts_result.search_type = f"hybrid_{mode}"
            return fts_result

        # Step 2: 语义评分
        try:
            texts_for_semantic = [hit.content for hit in fts_result.hits]
            semantic_scores = semantic_func(query, texts_for_semantic)
        except Exception as exc:
            logger.warning(f"Semantic scoring failed, falling back to FTS5: {exc}")
            fts_result.elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
            fts_result.search_type = "hybrid_semantic_fallback"
            return fts_result

        # Step 3: 归一化 BM25 分（转正数，越高越好）
        bm25_scores = [hit.bm25_score for hit in fts_result.hits]
        min_bm25, max_bm25 = min(bm25_scores), max(bm25_scores)
        range_bm25 = max_bm25 - min_bm25

        if range_bm25 > 0:
            norm_bm25 = [(s - min_bm25) / range_bm25 for s in bm25_scores]
        else:
            norm_bm25 = [0.5] * len(bm25_scores)

        # Step 4: 融合分
        kw = 1.0 - semantic_weight
        combined_scores = [
            kw * nb + semantic_weight * ss
            for nb, ss in zip(norm_bm25, semantic_scores)
        ]

        # Step 5: 重新排序
        scored_hits = list(zip(combined_scores, fts_result.hits, semantic_scores))
        scored_hits.sort(key=lambda x: x[0], reverse=True)

        # 分页
        total = len(scored_hits)
        page = scored_hits[options.offset:options.offset + options.limit]

        hits = []
        for combined, hit, sem_score in page:
            hit.semantic_score = sem_score
            hit.combined_score = round(combined, 4)
            # rank: 融合分（越小 BM25 rank 越接近越好）
            hit.rank = combined
            hits.append(hit)

        elapsed_ms = (time.perf_counter() - start) * 1000

        return SearchResult(
            hits=hits,
            total=total,
            query=query,
            options=options,
            elapsed_ms=round(elapsed_ms, 2),
            search_type=f"hybrid_{mode}",
        )


# =============================================================================
# 便捷工厂函数
# =============================================================================

def create_searcher(
    db_path: str | None = None,
    hybrid: bool = False,
    semantic_func=None,
) -> FTS5Searcher | HybridSearcher:
    """
    快速创建检索器实例。

    Example:
        # 纯 FTS5 搜索（推荐，无外部依赖）
        searcher = create_searcher()

        # 混合搜索（需要提供 semantic_func）
        searcher = create_searcher(hybrid=True, semantic_func=my_embedding)
    """
    path = db_path or str(DEFAULT_DB_PATH)
    if hybrid:
        return HybridSearcher(db_path=path, fts_weight=1.0)
    return FTS5Searcher(db_path=path)
