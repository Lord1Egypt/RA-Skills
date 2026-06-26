"""Background migration of legacy QMD reports to include vector embeddings."""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import aiosqlite

logger = logging.getLogger("ghostclaw.qmd.migration")


class EmbeddingBackfillManager:
    """
    Manages background migration of legacy QMD reports to include embeddings.

    Detects reports that lack embeddings in the vector store and generates
    chunks + embeddings for them in batches, with progress tracking and
    throttling to avoid overwhelming the system.
    """

    def __init__(self, store: 'QMDMemoryStore', batch_size: int = 50, throttle_ms: int = 100):
        """
        Initialize backfill manager.

        Args:
            store: QMDMemoryStore instance
            batch_size: Number of reports to process per batch
            throttle_ms: Milliseconds to wait between batches (rate limiting)
        """
        self.store = store
        self.batch_size = batch_size
        self.throttle_ms = throttle_ms / 1000.0  # convert to seconds
        self._running = False
        self._stop_flag = asyncio.Event()
        self._migration_task: Optional[asyncio.Task] = None
        self._pending: Set[int] = set()
        self._stats = {
            "total_runs": 0,
            "processed_runs": 0,
            "errors": 0,
            "started_at": None,
            "completed_at": None,
            "last_error": None,
        }

    async def needs_migration(self) -> bool:
        """
        Check if there are reports that lack embeddings.
        Returns True if SQLite has reports not present in vector store.
        """
        if not self.store.use_enhanced or not self.store.vector_store:
            return False

        # Get total count from SQLite
        async with aiosqlite.connect(self.store.db_path) as db:
            async with db.execute("SELECT COUNT(*) FROM reports") as cursor:
                total = (await cursor.fetchone())[0]

        # Get count of distinct report_ids already indexed in LanceDB
        try:
            existing_ids = await self.store.vector_store.get_indexed_run_ids()
            indexed_count = len(existing_ids)
        except Exception as e:
            logger.warning("Failed to get indexed run IDs: %s", e)
            return False

        return total > indexed_count

    async def start_background(self) -> Optional[asyncio.Task]:
        """
        Start migration in a background task if needed.
        Returns the task object or None if migration not required.
        """
        if self._migration_task and not self._migration_task.done():
            logger.info("Migration already running")
            return self._migration_task

        if not await self.needs_migration():
            logger.info("No migration needed")
            return None

        self._running = True
        self._stop_flag.clear()
        self._migration_task = asyncio.create_task(self._run_migration())
        return self._migration_task

    async def stop(self):
        """Request migration to stop (graceful shutdown)."""
        self._stop_flag.set()
        if self._migration_task and not self._migration_task.done():
            try:
                await asyncio.wait_for(self._migration_task, timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning("Migration did not finish within timeout")
                self._migration_task.cancel()
                try:
                    await self._migration_task
                except asyncio.CancelledError:
                    pass
        self._running = False

    async def _run_migration(self) -> None:
        """Main migration loop: process batches until done or stopped."""
        logger.info("Starting QMD migration")
        self._stats["started_at"] = datetime.utcnow().isoformat() + "Z"

        try:
            while not self._stop_flag.is_set():
                # Fetch next batch of reports needing embeddings
                batch = await self._fetch_next_batch()
                if not batch:
                    logger.info("Migration complete: no more reports to process")
                    break

                # Process batch
                for run in batch:
                    if self._stop_flag.is_set():
                        logger.info("Migration interrupted")
                        break
                    try:
                        await self._process_report(run)
                    except Exception as e:
                        logger.error("Failed to migrate run %d: %s", run["id"], e)
                        # Errors already counted in _process_report

                # Throttle between batches
                if self.throttle_ms > 0 and not self._stop_flag.is_set():
                    await asyncio.sleep(self.throttle_ms)

        except Exception as e:
            logger.error("Migration task crashed: %s", e)
            self._stats["last_error"] = str(e)
        finally:
            self._running = False
            self._stats["completed_at"] = datetime.utcnow().isoformat() + "Z"
            await self._persist_migration_state()
            logger.info("Migration finished: processed=%d, errors=%d",
                       self._stats["processed_runs"], self._stats["errors"])

    async def _fetch_next_batch(self) -> List[Dict]:
        """
        Fetch next batch of reports that need embedding.
        Returns list of report dicts with at least 'id' and 'report_json'.
        """
        # Get last processed run_id from migration_state
        last_id = await self._get_last_processed_id()

        async with aiosqlite.connect(self.store.db_path) as db:
            db.row_factory = aiosqlite.Row

            # Find runs with id > last_id, order by id asc, limit batch_size
            # Note: We don't try to be clever about checking LanceDB existence here;
            # just get next batch by ID and attempt to add; LanceDB add can be idempotent.
            async with db.execute(
                "SELECT id, report_json, repo_path, timestamp, vibe_score, stack, files_analyzed, total_lines "
                "FROM reports "
                "WHERE id > ? "
                "ORDER BY id ASC "
                "LIMIT ?",
                (last_id or 0, self.batch_size)
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def _process_report(self, run: Dict) -> None:
        """Generate embeddings for a single report and store in vector store."""
        run_id = run["id"]
        report = run["report_json"]
        if isinstance(report, str):
            try:
                report = json.loads(report)
            except json.JSONDecodeError:
                logger.warning("Skipping run %d: invalid report JSON", run_id)
                return

        # Build metadata for vector store
        metadata = {
            "repo_path": run.get("repo_path", ""),
            "timestamp": run.get("timestamp", ""),
            "vibe_score": run.get("vibe_score", 0),
            "stack": run.get("stack", ""),
            "files_analyzed": run.get("files_analyzed", 0),
            "total_lines": run.get("total_lines", 0),
        }

        # Mark as pending
        self._pending.add(run_id)
        try:
            # Delegate to embedding manager (same path as normal save_run)
            await self.store.embedding_mgr.vector_store.add_chunks_for_report(
                run_id, report, metadata
            )
            # Update state on success
            self._stats["processed_runs"] += 1
            await self._update_progress(run_id)
        except Exception as e:
            self._stats["errors"] += 1
            self._stats["last_error"] = str(e)
            raise
        finally:
            self._pending.discard(run_id)

    async def _get_last_processed_id(self) -> Optional[int]:
        """Read last_completed_run_id from migration_state table."""
        try:
            async with aiosqlite.connect(self.store.db_path) as db:
                async with db.execute(
                    "SELECT last_completed_run_id FROM migration_state WHERE id = 1"
                ) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        return row[0]
        except aiosqlite.OperationalError:
            # Table doesn't exist yet; create it
            await self._create_migration_state_table()
        return None

    async def _persist_migration_state(self) -> None:
        """Write final migration state (completed timestamp)."""
        async with aiosqlite.connect(self.store.db_path) as db:
            await db.execute(
                """
                UPDATE migration_state
                SET completed_at = ?, is_migrating = 0
                WHERE id = 1
                """,
                (self._stats["completed_at"],)
            )
            await db.commit()

    async def _update_progress(self, run_id: int) -> None:
        """Update migration_state with latest completed run_id and counts."""
        async with aiosqlite.connect(self.store.db_path) as db:
            # Ensure table exists
            await self._create_migration_state_table()
            await db.execute(
                """
                INSERT OR REPLACE INTO migration_state
                (id, last_completed_run_id, total_runs, processed_runs, is_migrating, started_at)
                VALUES (
                    1,
                    ?,
                    (SELECT COUNT(*) FROM reports),
                    ?,
                    1,
                    COALESCE((SELECT started_at FROM migration_state WHERE id = 1), datetime('now'))
                )
                """,
                (run_id, self._stats["processed_runs"])
            )
            await db.commit()

    async def _create_migration_state_table(self) -> None:
        """Create migration_state table if it doesn't exist."""
        async with aiosqlite.connect(self.store.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS migration_state (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    last_completed_run_id INTEGER,
                    total_runs INTEGER,
                    processed_runs INTEGER DEFAULT 0,
                    is_migrating BOOLEAN DEFAULT 0,
                    last_error TEXT,
                    started_at TEXT,
                    completed_at TEXT
                )
            """
            )
            await db.commit()

    def get_stats(self) -> Dict:
        """Return migration statistics."""
        stats = self._stats.copy()
        stats["running"] = self._running
        stats["pending"] = len(self._pending)
        return stats


# Backward compatibility: legacy storage layout migration (old .ghostclaw/reports -> .ghostclaw/storage)
def migrate_legacy_storage(repo_path: Path) -> bool:
    """
    Check for legacy storage layout and migrate to new .ghostclaw/storage/ structure.
    Returns True if migration was performed, False otherwise.
    """
    # Placeholder: not yet implemented; return False to skip
    return False

