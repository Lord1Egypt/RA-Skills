"""
QMD (Quantum Memory Database) backend for Ghostclaw.

Provides high-performance hybrid search (BM25 + vector) as an alternative
to the default SQLite MemoryStore.

This is a minimal implementation that uses SQLite with FTS5 for now,
providing the same interface as MemoryStore. Future versions may
integrate a true vector database or specialized QMD engine.
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("ghostclaw.qmd")


class QMDMemoryStore:
    """
    QMD-backed memory store with hybrid search capabilities.

    Storage location: .ghostclaw/storage/qmd/ghostclaw.db (separate from SQLite).
    Schema: Same as MemoryStore initially, but extensible for vectors.
    """

    def __init__(
        self,
        db_path: Optional[Path] = None,
        use_enhanced: bool = False,
        embedding_backend: str = "fastembed",
        ai_buff_enabled: bool = False,
        prefetch_enabled: bool = True,
        prefetch_workers: int = 2,
        prefetch_window: int = 2,
        prefetch_hours: int = 24,
        prefetch_vibe_delta: int = 10,
        prefetch_stack_count: int = 5,
        auto_migrate: bool = True,
        migration_batch_size: int = 50,
        migration_throttle_ms: int = 100,
        max_chunks_per_report: Optional[int] = None,
        vector_index_config: Optional[Dict] = None,
    ):
        # Use .ghostclaw/storage/qmd/ instead of .ghostclaw/storage/
        self.db_path = db_path or Path.cwd() / ".ghostclaw" / "storage" / "qmd" / "ghostclaw.db"
        self.use_enhanced = use_enhanced
        self.embedding_backend = embedding_backend
        self.ai_buff_enabled = ai_buff_enabled
        # Prefetch configuration
        self.prefetch_enabled = prefetch_enabled and ai_buff_enabled
        self.prefetch_window = prefetch_window
        self.prefetch_hours = prefetch_hours
        self.prefetch_vibe_delta = prefetch_vibe_delta
        self.prefetch_stack_count = prefetch_stack_count
        # Migration configuration
        self.auto_migrate = auto_migrate and use_enhanced and ai_buff_enabled
        self.migration_batch_size = migration_batch_size
        self.migration_throttle_ms = migration_throttle_ms

        # Phase 6: Vector optimization & diversity
        self.max_chunks_per_report = max_chunks_per_report
        self.vector_index_config = vector_index_config or {}

        # Subsystems
        # Using late imports to avoid circular dependencies
        from .qmd.fts import BM25Search
        from .qmd.indexer import ReportIndexer
        from .qmd.query_engine import QueryEngine
        from .vector_store import VectorStore
        from .qmd.embeddings import EmbeddingManager
        from .search_cache import SearchCache  # relative import from same package (core)
        from .prefetch import PrefetchManager
        from .migration import EmbeddingBackfillManager

        self.fts = BM25Search(self.db_path)

        # Initialize SearchCache if AI-Buff is enabled
        self.search_cache = None
        if ai_buff_enabled:
            # Defaults: maxsize=500, ttl=300 (5min)
            self.search_cache = SearchCache(maxsize=500, ttl=300)

        if self.use_enhanced:
            # VectorStore defaults its db_path to .ghostclaw/storage/qmd/lancedb
            # We explicitly set it to be adjacent to the sqlite db for consistency
            lancedb_path = self.db_path.parent / "lancedb"
            self.vector_store = VectorStore(
                db_path=lancedb_path,
                embedding_backend=self.embedding_backend,
                index_config=self.vector_index_config
            )
            self.embedding_mgr = EmbeddingManager(self.vector_store, self.embedding_backend)
        else:
            self.vector_store = None
            self.embedding_mgr = None

        self.indexer = ReportIndexer(self.db_path, self.fts, self.embedding_mgr)
        self.query_engine = QueryEngine(
            self.db_path,
            self.fts,
            self.vector_store,
            self.search_cache,
            max_chunks_per_report=self.max_chunks_per_report
        )

        # Prefetch manager (requires AI-Buff enabled)
        self.prefetch_manager = None
        if self.prefetch_enabled:
            self.prefetch_manager = PrefetchManager(self)

        # Migration manager (backfill embeddings for legacy reports)
        self.backfill_manager = None
        if self.auto_migrate and self.use_enhanced and self.vector_store and self.embedding_mgr:
            self.backfill_manager = EmbeddingBackfillManager(
                self,
                batch_size=self.migration_batch_size,
                throttle_ms=self.migration_throttle_ms
            )
            # Start migration in background (fire-and-forget)
            asyncio.create_task(self.backfill_manager.start_background())

        # Schedule vector index creation in background if configured
        if self.vector_store and self.vector_index_config.get("enabled", True):
            asyncio.create_task(self._maybe_create_index())

    async def _maybe_create_index(self):
        """Background task to create IVF-PQ index once data is available."""
        try:
            await self.vector_store.ensure_index()
        except Exception as e:
            logger.warning("Failed to create vector index: %s", e)

    def get_stats(self) -> Dict[str, Any]:
        """Return statistics for the memory store."""
        stats = {
            "db_path": str(self.db_path),
            "use_enhanced": self.use_enhanced,
            "embedding_backend": self.embedding_backend,
            "ai_buff_enabled": self.ai_buff_enabled,
        }
        if self.vector_store:
            # Access underlying cache stats from VectorStore
            if hasattr(self.vector_store, "_embedding_cache"):
                stats["embedding_cache"] = self.vector_store._embedding_cache.stats()
            else:
                stats["embedding_cache"] = None
        else:
            stats["embedding_cache"] = None

        if self.search_cache:
            stats["search_cache"] = self.search_cache.stats()
        else:
            stats["search_cache"] = None

        if self.prefetch_manager:
            stats["prefetch"] = self.prefetch_manager.get_stats()
        else:
            stats["prefetch"] = None

        if self.backfill_manager:
            stats["migration"] = self.backfill_manager.get_stats()
        else:
            stats["migration"] = None

        return stats

    async def list_runs(
        self,
        limit: int = 20,
        repo_path: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List recent runs."""
        if not self._db_exists():
            return []
        return await self.query_engine.list_runs(limit=limit, repo_path=repo_path)

    async def get_run(self, run_id: int) -> Optional[Dict[str, Any]]:
        """Get a single report by run_id."""
        if not self._db_exists():
            return None
        run = await self.query_engine.get_run(run_id)

        # Trigger prefetch if enabled
        if self.prefetch_manager and run:
            context = {
                "action": "get_run",
                "run_id": run_id,
                "run_data": run,
                "filters": {"repo_path": run.get("repo_path")},
                "prefetch_window": self.prefetch_window,
                "prefetch_hours": self.prefetch_hours,
                "prefetch_vibe_delta": self.prefetch_vibe_delta,
                "prefetch_stack_count": self.prefetch_stack_count,
            }
            self.prefetch_manager.trigger(context)

        return run

    async def get_previous_run(
        self, repo_path: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get the most recent analysis run, optionally filtered by repo path."""
        if not self._db_exists():
            return None
        runs = await self.query_engine.list_runs(limit=1, repo_path=repo_path)
        if not runs:
            return None
        return await self.query_engine.get_run(runs[0]["id"])

    async def search(
        self,
        query: str,
        limit: int = 10,
        repo_path: Optional[str] = None,
        stack: Optional[str] = None,
        min_score: Optional[int] = None,
        max_score: Optional[int] = None,
        alpha: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """Search across saved reports using hybrid BM25 + vector search."""
        if not self._db_exists():
            return []

        # Determine alpha using query planning if not explicitly provided
        if alpha is None:
            if self.ai_buff_enabled:
                # Build filters dict for planning
                filters = {
                    "repo_path": repo_path,
                    "stack": stack,
                    "min_score": min_score,
                    "max_score": max_score,
                }
                plan = self.query_engine._plan_query(query, limit, filters)
                alpha = plan.alpha
            else:
                alpha = 0.6

        results = await self.query_engine.search(
            query=query,
            limit=limit,
            repo_path=repo_path,
            stack=stack,
            min_score=min_score,
            max_score=max_score,
            alpha=alpha
        )

        # Trigger prefetch based on search results (if repo_path filter used)
        if self.prefetch_manager and repo_path:
            context = {
                "action": "search",
                "query": query,
                "filters": {"repo_path": repo_path, "stack": stack},
                "prefetch_window": self.prefetch_window,
                "prefetch_hours": self.prefetch_hours,
                "prefetch_vibe_delta": self.prefetch_vibe_delta,
                "prefetch_stack_count": self.prefetch_stack_count,
            }
            self.prefetch_manager.trigger(context)

        return results

    async def diff_runs(self, run_id_a: int, run_id_b: int) -> Optional[Dict[str, Any]]:
        """Compare two analysis runs."""
        if not self._db_exists():
            return None
        try:
            return await self.query_engine.diff_runs(run_id_a, run_id_b)
        except (ValueError, Exception) as e:
            logger.error("Error diffing runs %d and %d: %s", run_id_a, run_id_b, e)
            return None

    async def get_knowledge_graph(
        self,
        repo_path: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Build a knowledge graph from accumulated analysis history."""
        if not self._db_exists():
            return {
                "total_runs": 0,
                "stacks_seen": [],
                "score_trend": [],
                "recurring_issues": [],
                "recurring_ghosts": [],
                "recurring_flags": [],
                "coupling_hotspots": [],
                "nodes": [],
                "edges": []
            }
        # QueryEngine.knowledge_graph accepts limit
        return await self.query_engine.knowledge_graph(limit=limit)

    async def save_run(
        self,
        report: Dict[str, Any],
        repo_path: str,
        timestamp: Optional[str] = None,
    ) -> int:
        """Save an analysis run and handle FTS/embeddings indexing."""
        return await self.indexer.save(report, repo_path, timestamp)

    def _db_exists(self) -> bool:
        """Internal check for database existence."""
        return self.db_path.exists()
