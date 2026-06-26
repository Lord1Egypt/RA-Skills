"""
test_fts_search.py - 单元测试

覆盖：
- _build_fts_query 查询构建
- _render_snippet snippet 渲染
- BM25 计算
- FTS5Searcher 搜索（in-memory DB）
- HybridSearcher 混合搜索
- 过滤、分页、去重

运行：
    pytest agent-cluster/memory/tests/test_fts_search.py -v
"""

from __future__ import annotations

import json
import sqlite3
import tempfile
import time
from pathlib import Path

import pytest

import sys as _sys
_sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from memory.fts_search import (
    BM25Config,
    FTS5Searcher,
    HybridSearcher,
    SearchHit,
    SearchOptions,
    SearchResult,
    _build_fts_query,
    _render_snippet,
    _sqlite_bm25_score,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def temp_db():
    """创建带 FTS5 的临时 in-memory 数据库"""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA journal_mode=WAL")

    # 主表
    conn.execute("""
        CREATE TABLE memory_entries (
            entry_id       TEXT PRIMARY KEY,
            content        TEXT NOT NULL,
            content_hash   TEXT NOT NULL,
            memory_type    TEXT NOT NULL,
            scope          TEXT NOT NULL,
            importance     INTEGER NOT NULL DEFAULT 3,
            agent_id       TEXT NOT NULL DEFAULT '',
            created_at     TEXT NOT NULL,
            updated_at     TEXT NOT NULL,
            accessed_at    TEXT NOT NULL,
            tags           TEXT NOT NULL DEFAULT '[]',
            related_agents TEXT NOT NULL DEFAULT '[]',
            related_entries TEXT NOT NULL DEFAULT '[]',
            ttl_seconds    REAL NOT NULL DEFAULT 3600.0,
            version        INTEGER NOT NULL DEFAULT 1,
            is_deleted     INTEGER NOT NULL DEFAULT 0,
            is_pinned      INTEGER NOT NULL DEFAULT 0,
            summary        TEXT NOT NULL DEFAULT '',
            source         TEXT NOT NULL DEFAULT ''
        )
    """)

    # FTS5 虚拟表
    conn.execute("""
        CREATE VIRTUAL TABLE memory_fts USING fts5(
            entry_id,
            content,
            summary,
            tags,
            content='memory_entries',
            content_rowid='rowid'
        )
    """)

    # 触发器
    conn.execute("""
        CREATE TRIGGER memory_ai AFTER INSERT ON memory_entries BEGIN
            INSERT INTO memory_fts(entry_id, content, summary, tags)
            VALUES (new.entry_id, new.content, new.summary, new.tags);
        END
    """)

    conn.execute("""
        CREATE TRIGGER memory_ad AFTER DELETE ON memory_entries BEGIN
            INSERT INTO memory_fts(memory_fts, entry_id, content, summary, tags)
            VALUES ('delete', old.entry_id, old.content, old.summary, old.tags);
        END
    """)

    conn.commit()

    # 插入测试数据
    fixtures = [
        {
            "entry_id": "entry-001",
            "content_hash": "abc123",
            "content": "Python asyncio error: SSL certificate verify failed. "
                       "Solution: update certifi package and set REQUESTS_CA_BUNDLE.",
            "summary": "Fix Python SSL certificate error",
            "tags": '["python", "ssl", "async"]',
            "memory_type": "procedure",
            "scope": "shared",
            "importance": 4,
            "agent_id": "agent-001",
        },
        {
            "entry_id": "entry-002",
            "content_hash": "def456",
            "content": "Deploy Django app to production using Docker and nginx. "
                       "Steps: 1. Build image 2. Push to registry 3. Pull on server 4. Restart",
            "summary": "Django Docker production deployment",
            "tags": '["django", "docker", "deployment"]',
            "memory_type": "procedure",
            "scope": "shared",
            "importance": 5,
            "agent_id": "agent-002",
        },
        {
            "entry_id": "entry-003",
            "content_hash": "ghi789",
            "content": "SQLite FTS5 full-text search tutorial. "
                       "Supports BM25 ranking, prefix matching, and snippet highlighting.",
            "summary": "SQLite FTS5 tutorial",
            "tags": '["sqlite", "fts5", "search"]',
            "memory_type": "fact",
            "scope": "shared",
            "importance": 3,
            "agent_id": "agent-001",
        },
        {
            "entry_id": "entry-004",
            "content_hash": "jkl012",
            "content": "Skill candidate: Python error handling pattern. "
                       "Actions: 1. Catch specific exceptions 2. Log errors 3. Retry on transient",
            "summary": "Python error handling skill",
            "tags": '["skill-candidate", "python", "error-handling"]',
            "memory_type": "procedure",
            "scope": "shared",
            "importance": 4,
            "agent_id": "agent-001",
        },
    ]

    now = "2026-04-16T00:00:00+00:00"
    for f in fixtures:
        conn.execute("""
            INSERT INTO memory_entries (
                entry_id, content, content_hash, memory_type, scope,
                importance, agent_id, created_at, updated_at, accessed_at,
                tags, related_agents, related_entries, ttl_seconds,
                version, is_deleted, is_pinned, summary, source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '[]', '[]', 3600.0, 1, 0, 0, ?, '')
        """, (
            f["entry_id"],
            f["content"],
            f["content_hash"],
            f["memory_type"],
            f["scope"],
            f["importance"],
            f["agent_id"],
            now, now, now,
            f["tags"],
            f["summary"],
        ))
    conn.commit()

    yield conn

    conn.close()


@pytest.fixture
def temp_db_path(temp_db):
    """将 in-memory DB 写入临时文件，供 FTS5Searcher 使用"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        path = f.name

    # 使用 SQLite backup API 完整复制 in-memory DB 到文件
    dest_conn = sqlite3.connect(path)
    dest_conn.execute("PRAGMA journal_mode=WAL")
    temp_db.backup(dest_conn)
    dest_conn.commit()
    dest_conn.close()

    yield path
    Path(path).unlink(missing_ok=True)


# =============================================================================
# 辅助函数测试
# =============================================================================

class TestBuildFtsQuery:
    def test_single_term(self):
        q = _build_fts_query("python")
        assert '"python"*' == q

    def test_multiple_terms(self):
        q = _build_fts_query("python ssl error")
        parts = q.split()
        assert '"python"*' in parts
        assert '"ssl"*' in parts
        assert '"error"*' in parts

    def test_prefix_match_disabled(self):
        q = _build_fts_query("python", prefix_match=False)
        assert '"python"' == q

    def test_empty_query(self):
        assert '""' == _build_fts_query("")

    def test_boolean_operators_preserved(self):
        q = _build_fts_query("python AND async OR sync")
        assert "AND" in q
        assert "OR" in q


class TestRenderSnippet:
    def test_highlight_single_term(self):
        text = "Python SSL certificate error fix"
        result = _render_snippet(text, ["SSL"], size=5)
        assert "【SSL】" in result

    def test_highlight_multiple_terms(self):
        text = "Python SSL error in asyncio coroutine"
        result = _render_snippet(text, ["Python", "asyncio"], size=5)
        assert "【Python】" in result
        assert "【asyncio】" in result

    def test_context_window(self):
        text = "a" * 100 + "SSL" + "b" * 100
        result = _render_snippet(text, ["SSL"], size=3)
        # 应该截取附近内容，不包含全文
        assert len(result) < 300

    def test_no_match_returns_start(self):
        text = "Some text without the query"
        result = _render_snippet(text, ["xyz123"], size=5)
        assert "…" in result or len(result) <= 200


# =============================================================================
# FTS5Searcher
# =============================================================================

class TestFTS5Searcher:
    def test_search_finds_relevant(self, temp_db_path):
        searcher = FTS5Searcher(temp_db_path)
        result = searcher.search("SSL certificate", limit=5)

        assert result.total >= 1
        assert result.search_type == "fts5"
        assert result.elapsed_ms > 0

        hit_ids = [h.entry_id for h in result.hits]
        assert "entry-001" in hit_ids

    def test_search_snippet_contains_highlight(self, temp_db_path):
        searcher = FTS5Searcher(temp_db_path)
        result = searcher.search("SSL", limit=5)

        assert result.hits[0].snippet
        # 高亮标记存在
        assert "【" in result.hits[0].snippet

    def test_search_skill_candidate_flag(self, temp_db_path):
        searcher = FTS5Searcher(temp_db_path)
        result = searcher.search("skill candidate", limit=5)

        skill_hits = [h for h in result.hits if h.is_skill_candidate]
        assert len(skill_hits) >= 1
        assert skill_hits[0].entry_id == "entry-004"

    def test_search_importance_filter(self, temp_db_path):
        searcher = FTS5Searcher(temp_db_path)
        result = searcher.search(
            "python", limit=10, min_importance=5
        )
        for hit in result.hits:
            assert hit.importance >= 5

    def test_search_scope_filter(self, temp_db_path):
        searcher = FTS5Searcher(temp_db_path)
        result = searcher.search("python", scopes=["shared"], limit=10)
        for hit in result.hits:
            assert hit.scope == "shared"

    def test_search_pagination(self, temp_db_path):
        searcher = FTS5Searcher(temp_db_path)
        page1 = searcher.search("python OR docker OR sqlite", limit=2, offset=0)
        page2 = searcher.search("python OR docker OR sqlite", limit=2, offset=2)

        ids1 = {h.entry_id for h in page1.hits}
        ids2 = {h.entry_id for h in page2.hits}
        assert ids1.isdisjoint(ids2)  # 分页无重复

    def test_search_deduplication(self, temp_db_path):
        # 搜索包含所有 fixture 词的查询
        searcher = FTS5Searcher(temp_db_path)
        result = searcher.search("python", limit=10)

        ids = [h.entry_id for h in result.hits]
        assert len(ids) == len(set(ids))  # 无重复

    def test_get_skill_candidates(self, temp_db_path):
        searcher = FTS5Searcher(temp_db_path)
        hits = searcher.get_skill_candidates(limit=10)
        assert all(h.is_skill_candidate for h in hits)
        assert len(hits) >= 1

    def test_count(self, temp_db_path):
        searcher = FTS5Searcher(temp_db_path)
        total = searcher.count("python")
        assert total >= 1

    def test_bm25_scores_sorted(self, temp_db_path):
        searcher = FTS5Searcher(temp_db_path)
        result = searcher.search("python deployment", limit=5)

        # BM25 分数升序（越负越相关）
        scores = [h.bm25_score for h in result.hits]
        assert scores == sorted(scores)


# =============================================================================
# HybridSearcher
# =============================================================================

class TestHybridSearcher:
    def test_hybrid_with_fake_semantic(self, temp_db_path):
        """注入假的语义评分函数，验证混合排序生效"""
        def fake_semantic(query: str, texts: list[str]) -> list[float]:
            # 语义分：文本长度越短分数越高（模拟性）
            return [1.0 / (len(t) + 1) for t in texts]

        searcher = HybridSearcher(temp_db_path)
        result = searcher.search(
            "python",
            mode="keyword_first",
            semantic_weight=0.5,
            semantic_func=fake_semantic,
            limit=5,
        )

        assert result.search_type == "hybrid_keyword_first"
        assert all(h.semantic_score > 0 for h in result.hits)
        assert all(h.combined_score > 0 for h in result.hits)

    def test_pure_fts_mode(self, temp_db_path):
        """pure_fts 模式等价于纯 FTS5"""
        searcher = HybridSearcher(temp_db_path)
        result = searcher.search("python", mode="pure_fts", limit=5)

        assert result.search_type == "pure_fts"
        assert len(result.hits) >= 1

    def test_semantic_fallback_on_error(self, temp_db_path):
        """语义函数失败时回退到 FTS5"""
        def bad_semantic(query: str, texts: list[str]) -> list[float]:
            raise RuntimeError("simulated failure")

        searcher = HybridSearcher(temp_db_path)
        result = searcher.search(
            "python",
            mode="keyword_first",
            semantic_weight=0.5,
            semantic_func=bad_semantic,
            limit=5,
        )

        assert result.search_type == "hybrid_semantic_fallback"
        assert len(result.hits) >= 1


# =============================================================================
# SearchHit / SearchResult
# =============================================================================

class TestSearchHitResult:
    def test_hit_to_dict(self):
        hit = SearchHit(
            entry_id="e1",
            content="test content",
            summary="summary",
            tags=["tag1"],
            memory_type="fact",
            scope="shared",
            importance=3,
            created_at="2026-04-16",
            rank=1.5,
            snippet="【test】 content",
            bm25_score=-2.5,
            semantic_score=0.7,
            combined_score=0.6,
            is_skill_candidate=True,
        )
        d = hit.to_dict()
        assert d["entry_id"] == "e1"
        assert d["is_skill_candidate"] is True
        assert "【test】" in d["snippet"]

    def test_search_result_to_dict(self, temp_db_path):
        searcher = FTS5Searcher(temp_db_path)
        result = searcher.search("python", limit=5)
        d = result.to_dict()
        assert "hits" in d
        assert "total" in d
        assert "elapsed_ms" in d
        assert d["search_type"] == "fts5"


# =============================================================================
# BM25Config
# =============================================================================

class TestBM25Config:
    def test_default_values(self):
        assert BM25Config.K1 == 1.5
        assert BM25Config.B == 0.75


# =============================================================================
# SearchOptions
# =============================================================================

class TestSearchOptions:
    def test_defaults(self):
        opts = SearchOptions()
        assert opts.limit == 10
        assert opts.use_bm25 is True
        assert opts.snippet_size == 5
        assert opts.highlight_open == "【"
        assert opts.highlight_close == "】"
        assert opts.prefix_match is True

    def test_custom_options(self):
        opts = SearchOptions(
            limit=20,
            scopes=["shared"],
            memory_types=["fact"],
            min_importance=4,
            semantic_weight=0.4,
        )
        assert opts.limit == 20
        assert opts.scopes == ["shared"]
        assert opts.memory_types == ["fact"]
        assert opts.semantic_weight == 0.4
