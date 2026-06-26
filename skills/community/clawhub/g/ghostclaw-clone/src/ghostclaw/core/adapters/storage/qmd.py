"""Storage adapter using QMD (Quantum Memory Database) backend."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import aiosqlite
    HAS_AIOSQLITE = True
except ImportError:
    HAS_AIOSQLITE = False

from ghostclaw.core.adapters.base import StorageAdapter, AdapterMetadata
from ghostclaw.core.adapters.hooks import hookimpl
from ghostclaw.core.config import GhostclawConfig
from ghostclaw.core.qmd_store import QMDMemoryStore

logger = logging.getLogger("ghostclaw.qmd")


class QMDStorageAdapter(StorageAdapter):
    """
    Persists ArchitectureReports to a QMD backend with vector embeddings.

    Uses QMDMemoryStore for unified write path (ensures FTS and embeddings).
    Implements StorageAdapter interface for plugin compatibility.
    """

    def __init__(self):
        # QMD uses its own directory under .ghostclaw/storage/qmd/
        self.db_path = Path.cwd() / ".ghostclaw" / "storage" / "qmd" / "ghostclaw.db"
        self._initialized = False
        self._memory_store = None
        # Determine embedding_backend from project config
        try:
            cfg = GhostclawConfig.load(".")
            self.embedding_backend = getattr(cfg, 'embedding_backend', 'fastembed')
        except Exception:
            self.embedding_backend = 'fastembed'

    async def _ensure_db_schema(self):
        """Ensure the base reports table exists (for backward compatibility)."""
        if not HAS_AIOSQLITE:
            raise ImportError("aiosqlite is required for QMDStorageAdapter")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    vibe_score INTEGER,
                    stack TEXT,
                    files_analyzed INTEGER,
                    total_lines INTEGER,
                    report_json TEXT,
                    repo_path TEXT,
                    vcs_commit TEXT,
                    vcs_branch TEXT,
                    vcs_dirty BOOLEAN
                )
            """)
            await db.commit()

    async def _get_memory_store(self) -> QMDMemoryStore:
        """Lazy-initialize the QMDMemoryStore with enhanced mode."""
        if self._memory_store is None:
            # Determine ai_buff_enabled and prefetch settings from project config
            try:
                from ghostclaw.core.config import GhostclawConfig
                repo_path = self.db_path.parent.parent.parent.parent  # .ghostclaw/storage/qmd/ghostclaw.db -> repo root
                cfg = GhostclawConfig.load(repo_path)
                ai_buff = getattr(cfg, 'ai_buff_enabled', False)
                prefetch_enabled = getattr(cfg, 'prefetch_enabled', True)
                prefetch_workers = getattr(cfg, 'prefetch_workers', 2)
                prefetch_window = getattr(cfg, 'prefetch_window', 2)
                prefetch_hours = getattr(cfg, 'prefetch_hours', 24)
                prefetch_vibe_delta = getattr(cfg, 'prefetch_vibe_delta', 10)
                prefetch_stack_count = getattr(cfg, 'prefetch_stack_count', 5)
                auto_migrate = getattr(cfg, 'auto_migrate', True)
                migration_batch_size = getattr(cfg, 'migration_batch_size', 50)
                migration_throttle_ms = getattr(cfg, 'migration_throttle_ms', 100)
                # Phase 6: vector optimization & diversity
                max_chunks_per_report = getattr(cfg, 'max_chunks_per_report', None)
                vector_index_config = {}
                if hasattr(cfg, 'vector_index'):
                    vector_index_config = getattr(cfg, 'vector_index', {})
                # Optionally also get classifier config but not used directly here
            except Exception:
                ai_buff = False
                prefetch_enabled = True
                prefetch_workers = 2
                prefetch_window = 2
                prefetch_hours = 24
                prefetch_vibe_delta = 10
                prefetch_stack_count = 5
                auto_migrate = True
                migration_batch_size = 50
                migration_throttle_ms = 100
                max_chunks_per_report = None
                vector_index_config = {}

            self._memory_store = QMDMemoryStore(
                db_path=self.db_path,
                use_enhanced=True,
                embedding_backend=self.embedding_backend,
                ai_buff_enabled=ai_buff,
                prefetch_enabled=prefetch_enabled,
                prefetch_workers=prefetch_workers,
                prefetch_window=prefetch_window,
                prefetch_hours=prefetch_hours,
                prefetch_vibe_delta=prefetch_vibe_delta,
                prefetch_stack_count=prefetch_stack_count,
                auto_migrate=auto_migrate,
                migration_batch_size=migration_batch_size,
                migration_throttle_ms=migration_throttle_ms,
                max_chunks_per_report=max_chunks_per_report,
                vector_index_config=vector_index_config,
            )
        return self._memory_store

    def get_metadata(self) -> AdapterMetadata:
        return AdapterMetadata(
            name="qmd",
            version="0.2.0-alpha",
            description="QMD (Quantum Memory Database) backend with hybrid BM25+vector search (enhanced).",
            dependencies=["aiosqlite", "lancedb", "sentence-transformers"],
        )

    async def is_available(self) -> bool:
        """QMD is available if aiosqlite is installed."""
        return HAS_AIOSQLITE

    # ------------------------------------------------------------------
    # StorageAdapter required methods
    # ------------------------------------------------------------------

    async def save_report(self, report: Any) -> str:
        """Save report to QMD store and return its ID."""
        mem = await self._get_memory_store()
        # Convert report to dict if needed
        if hasattr(report, "model_dump"):
            data = report.model_dump()
        else:
            data = report
        repo_path = str(Path.cwd())
        # Delegate to memory_store, which handles FTS + embeddings
        run_id = await mem.save_run(data, repo_path=repo_path)
        return str(run_id)

    async def get_history(self, limit: int = 10) -> List[Any]:
        """Retrieve recent reports from QMD store."""
        mem = await self._get_memory_store()
        # Use memory_store.list_runs and then fetch each full report
        summaries = await mem.list_runs(limit=limit)
        results = []
        for summary in summaries:
            full = await mem.get_run(summary["id"])
            if full:
                # The get_run returns a dict with "report" key containing the full report
                # Merge metadata
                full_data = full["report"].copy()
                full_data["_db_id"] = full["id"]
                full_data["_db_timestamp"] = full["timestamp"]
                results.append(full_data)
        return results

    # ------------------------------------------------------------------
    # Hook implementations
    # ------------------------------------------------------------------

    @hookimpl
    async def ghost_save_report(self, report: Any) -> Optional[str]:
        """Hook implementation for saving report."""
        return await self.save_report(report)

    @hookimpl
    def ghost_get_metadata(self) -> Dict[str, Any]:
        """Expose metadata to the plugin manager."""
        meta = self.get_metadata()
        return {
            "name": meta.name,
            "version": meta.version,
            "description": meta.description,
            "available": True,
        }
