#!/usr/bin/env python3
"""Benchmark search latency with and without IVF-PQ."""

import asyncio
import random
import time
from pathlib import Path
from datetime import datetime, timedelta

from ghostclaw.core.qmd_store import QMDMemoryStore
from ghostclaw.core.config import GhostclawConfig


async def populate_db(db_path: Path, num_reports: int = 1500):
    """Populate DB with reports and embeddings (via save_run)."""
    store = QMDMemoryStore(
        db_path=db_path,
        use_enhanced=True,
        ai_buff_enabled=False,  # no caching/prefetch
        auto_migrate=False,
    )
    base_time = datetime(2026, 1, 1)
    stacks = ["python", "node", "go", "java", "rust"]
    print(f"Populating DB with {num_reports} reports...")
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
            "metadata": {"timestamp": ts, "repo_path": "/tmp/bench_repo"}
        }
        await store.save_run(report, repo_path=str(db_path.parent / "repo"))
        if (i+1) % 100 == 0:
            print(f"   ... saved {i+1}/{num_reports}")
    print("✅ Population complete")
    # No close needed for QMDMemoryStore
    return store


async def run_benchmark(db_path: Path, use_ivf_pq: bool = False):
    """Run benchmark and print latency statistics."""
    store = QMDMemoryStore(
        db_path=db_path,
        use_enhanced=True,
        ai_buff_enabled=False,
        auto_migrate=False,
        # Phase 6 config
        max_chunks_per_report=None,
        vector_index_config={
            "enabled": use_ivf_pq,
            "type": "ivf_pq",
            "partitions": 256,
            "sub_vectors": 64,
            "training_sample_size": 10000
        } if use_ivf_pq else {"enabled": False},
    )

    # Ensure index is created if IVF-PQ enabled
    if use_ivf_pq and store.vector_store:
        print("Creating IVF-PQ index (may take a moment)...")
        await store.vector_store.ensure_index()
        # Wait a bit for background task? ensure_index is immediate.

    # Warm up with a few queries
    warmup_queries = ["security", "performance", "architecture", "testing", "deployment"]
    for q in warmup_queries:
        await store.search(q, limit=5)
    print("✅ Warmup complete")

    # Benchmark queries
    num_queries = 100
    queries = [
        "memory leak",
        "authentication",
        "scalability",
        "error handling",
        "logging",
        "configuration",
        "dependency",
        "coupling",
        "cohesion",
        "technical debt",
    ]
    latencies = []
    print(f"⏳ Running {num_queries} benchmark queries...")
    for i in range(num_queries):
        query = random.choice(queries)
        start = time.perf_counter()
        results = await store.search(query, limit=10)
        elapsed = (time.perf_counter() - start) * 1000  # ms
        latencies.append(elapsed)
        if (i+1) % 20 == 0:
            print(f"   ... completed {i+1}/{num_queries}")

    latencies.sort()
    p50 = latencies[num_queries // 2]
    p99 = latencies[int(num_queries * 0.99)]
    mean = sum(latencies) / num_queries

    mode = "IVF-PQ" if use_ivf_pq else "Brute-force"
    print(f"\n📊 Benchmark results ({mode}):")
    print(f"   Queries: {num_queries}")
    print(f"   P50: {p50:.2f}ms")
    print(f"   P99: {p99:.2f}ms")
    print(f"   Mean: {mean:.2f}ms")

    # No close needed for QMDMemoryStore
    return {
        "mode": mode,
        "queries": num_queries,
        "p50": p50,
        "p99": p99,
        "mean": mean,
    }


async def main():
    import shutil
    tmp_dir = Path("/tmp") / f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    db_path = tmp_dir / ".ghostclaw" / "storage" / "qmd" / "ghostclaw.db"

    # Cleanup any existing
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)

    # Populate with 1500 reports
    store_pop = await populate_db(db_path, num_reports=1500)
    # Note: populate_db already closed store, but we can just create new ones for benchmark

    # Run benchmark without IVF-PQ
    bf_stats = await run_benchmark(db_path, use_ivf_pq=False)

    # Run benchmark with IVF-PQ
    ivf_stats = await run_benchmark(db_path, use_ivf_pq=True)

    # Summary
    print("\n✅ Benchmark complete!")
    print(f"Brute-force P50: {bf_stats['p50']:.2f}ms")
    print(f"IVF-PQ P50: {ivf_stats['p50']:.2f}ms")
    speedup = bf_stats['p50'] / ivf_stats['p50'] if ivf_stats['p50'] > 0 else 0
    print(f"Speedup: {speedup:.2f}x")

    # Cleanup
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
        print(f"🗑 Cleaned up {tmp_dir}")


if __name__ == "__main__":
    asyncio.run(main())
