#!/usr/bin/env python3
"""Integration test: Migrate a legacy QMD DB with >1000 reports."""

import asyncio
import json
import random
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

from ghostclaw.core.qmd_store import QMDMemoryStore
from ghostclaw.core.config import GhostclawConfig


async def create_legacy_qmd_db(db_path: Path, num_reports: int = 1200):
    """Create a legacy QMD SQLite database with reports but no embeddings."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Create empty LanceDB directory to simulate "no embeddings"
    lancedb_path = db_path.parent / "lancedb"
    if lancedb_path.exists():
        import shutil
        shutil.rmtree(lancedb_path)

    # Create SQLite reports table
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                vibe_score INTEGER NOT NULL,
                stack TEXT NOT NULL,
                files_analyzed INTEGER,
                total_lines INTEGER,
                report_json TEXT NOT NULL,
                repo_path TEXT
            )
            """
        )
        # Insert reports
        base_time = datetime(2026, 1, 1)
        stacks = ["python", "node", "go", "java", "rust"]
        for i in range(num_reports):
            vibe = random.randint(30, 100)
            stack = random.choice(stacks)
            files = random.randint(1, 20)
            lines = random.randint(100, 2000)
            ts = (base_time + timedelta(hours=i)).isoformat() + "Z"

            report = {
                "vibe_score": vibe,
                "stack": stack,
                "files_analyzed": files,
                "total_lines": lines,
                "issues": [f"Issue {i}-{j}" for j in range(random.randint(0, 3))],
                "architectural_ghosts": [f"Ghost {i}-{j}" for j in range(random.randint(0, 2))],
                "metadata": {"timestamp": ts, "repo_path": "/tmp/legacy_repo"}
            }

            await db.execute(
                "INSERT INTO reports (timestamp, vibe_score, stack, files_analyzed, total_lines, report_json, repo_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (ts, vibe, stack, files, lines, json.dumps(report), "/tmp/legacy_repo")
            )
        await db.commit()
        print(f"✅ Created legacy DB with {num_reports} reports at {db_path}")


async def run_migration_test():
    import aiosqlite

    tmp_dir = Path("/tmp") / f"migration_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    db_path = tmp_dir / ".ghostclaw" / "storage" / "qmd" / "ghostclaw.db"

    # Create legacy DB with >1000 reports
    num_reports = 1200
    await create_legacy_qmd_db(db_path, num_reports=num_reports)

    # Verify no LanceDB directory
    lancedb_path = db_path.parent / "lancedb"
    assert not lancedb_path.exists(), "LanceDB should not exist yet"

    # Initialize store (auto_migrate=False)
    store = QMDMemoryStore(
        db_path=db_path,
        use_enhanced=True,
        ai_buff_enabled=True,
        auto_migrate=False,
        migration_batch_size=100,
        migration_throttle_ms=10,
    )

    # Manually create and start backfill manager
    from ghostclaw.core.migration import EmbeddingBackfillManager
    store.backfill_manager = EmbeddingBackfillManager(store, batch_size=100, throttle_ms=10)

    # Confirm need migration
    needs = await store.backfill_manager.needs_migration()
    print(f"✅ needs_migration: {needs}")
    assert needs, f"Should need migration ({num_reports} reports, 0 embeddings)"

    # Start migration background task
    task = await store.backfill_manager.start_background()
    assert task is not None, "Migration task should start"
    print("🚀 Migration started")

    # Wait for completion
    print("⏳ Waiting for migration to complete...")
    max_wait = 600  # seconds (10 min)
    start = asyncio.get_event_loop().time()
    while store.backfill_manager._running:
        await asyncio.sleep(3)
        stats = store.get_stats()
        mig = stats.get("migration", {})
        completed = mig.get('completed', 0)
        total = mig.get('total_runs', num_reports)
        pending = mig.get('pending', 0)
        print(f"   Progress: {completed}/{total} completed, pending={pending}, errors={mig.get('errors',0)}")
        if asyncio.get_event_loop().time() - start > max_wait:
            print("❌ Migration timed out")
            return False

    # Final stats
    final_stats = store.get_stats()
    mig_stats = final_stats.get("migration", {})
    total = mig_stats.get("total_runs", 0)
    completed = mig_stats.get("completed", 0)
    errors = mig_stats.get("errors", 0)

    print(f"✅ Migration finished: {completed}/{total} processed, {errors} errors")

    # Check LanceDB exists
    assert lancedb_path.exists(), "LanceDB directory should exist after migration"

    # Check vector store indexed runs
    if store.vector_store:
        indexed_ids = await store.vector_store.get_indexed_run_ids()
        print(f"✅ Vector store indexed {len(indexed_ids)} run IDs")

    # Verify random sample has embeddings
    sample_id = random.randint(1, total)
    if store.vector_store:
        chunks = await store.vector_store.search_by_run_id(sample_id, limit=5)
        print(f"   Sample run {sample_id} has {len(chunks)} chunks")
        assert len(chunks) > 0, f"Expected chunks for run {sample_id}"

    print("✅✅ Migration integration test PASSED (legacy DB with >1000 reports)")
    return True


if __name__ == "__main__":
    import aiosqlite
    result = asyncio.run(run_migration_test())
    exit(0 if result else 1)
