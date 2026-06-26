#!/usr/bin/env python3
"""Profile memory search and knowledge graph performance with a realistic dataset."""

import argparse
import asyncio
import random
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys
import aiosqlite

# Add workspace src to PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ghostclaw.core.memory import MemoryStore


async def generate_mock_runs(db_path: Path, count: int = 50):
    """Generate mock analysis runs directly in SQLite."""
    print(f"Generating {count} mock analysis runs...")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                vibe_score INTEGER,
                stack TEXT,
                files_analyzed INTEGER,
                total_lines INTEGER,
                report_json TEXT,
                repo_path TEXT
            )
        """)
        base_time = datetime.now()
        sample_issues = [
            "High cyclomatic complexity in module",
            "Tight coupling between classes",
            "Missing type hints in public API",
            "God object detected",
            "Feature envy",
            "Inconsistent naming",
            "Long parameter list",
            "Duplicate code",
            "Unused imports",
            "Dead code"
        ]
        sample_files = [f"src/file_{i}.py" for i in range(100)]

        for i in range(count):
            timestamp = (base_time - timedelta(days=count - i)).isoformat() + "Z"
            vibe_score = random.randint(50, 95)
            num_ghosts = random.randint(0, 10)
            num_flags = random.randint(5, 30)
            issues = []
            for _ in range(num_ghosts + num_flags):
                issues.append({
                    "type": random.choice(["ghost", "flag"]),
                    "file": random.choice(sample_files),
                    "line": random.randint(1, 500),
                    "message": random.choice(sample_issues),
                    "severity": random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])
                })
            # For profiling the current buggy version, use simple strings for aggregation
            simple_issue_messages = [random.choice(sample_issues) for _ in range(num_ghosts + num_flags)]
            report = {
                "run_id": f"run_{i+1:04d}",
                "repo_path": "/mock/repo",
                "timestamp": timestamp,
                "vibe_score": vibe_score,
                "issues": simple_issue_messages,  # simple strings
                "architectural_ghosts": [f"Ghost: {msg}" for msg in simple_issue_messages[:num_ghosts]],
                "red_flags": [f"Flag: {msg}" for msg in simple_issue_messages[num_ghosts:]],
                "summary": f"Analysis run {i+1}",
                "stack": "python",
                "files_analyzed": random.randint(50, 200),
                "total_lines": random.randint(1000, 10000),
                "coupling_metrics": {
                    f"module_{random.randint(1,10)}": {"instability": round(random.random(), 2)}
                    for _ in range(random.randint(3, 8))
                },
            }
            await db.execute(
                "INSERT INTO reports (timestamp, vibe_score, stack, files_analyzed, total_lines, report_json, repo_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    timestamp,
                    vibe_score,
                    "python",
                    report["files_analyzed"],
                    report["total_lines"],
                    json.dumps(report),
                    "/mock/repo"
                ),
            )
        await db.commit()
    print(f"Inserted {count} records.")


async def profile_memory_search(store: MemoryStore, iterations: int = 100):
    """Profile memory search queries."""
    print("\n=== Profiling Memory Search ===")
    queries = [
        ("complexity", 20),
        ("coupling", 15),
        ("type hints", 15),
        ("god object", 10),
        ("naming", 15),
        ("unused", 10)
    ]

    total_time = 0.0
    for query, limit in queries:
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            results = await store.search(query=query, limit=limit)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
        avg = sum(times) / len(times)
        total_time += avg
        print(f"  Query '{query}' (limit={limit}): {avg*1000:.2f}ms avg (n={iterations}), hits={len(results)}")

    print(f"  Total average per query variant: {total_time*1000:.2f}ms")
    return total_time / len(queries)


async def profile_knowledge_graph(store: MemoryStore, iterations: int = 50):
    """Profile knowledge graph generation."""
    print("\n=== Profiling Knowledge Graph ===")
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        graph = await store.get_knowledge_graph()
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    avg = sum(times) / len(times)
    recurring = len(graph.get('recurring_issues', [])) + len(graph.get('recurring_ghosts', []))
    print(f"  Knowledge graph: {avg*1000:.2f}ms avg (n={iterations}), aggregated_entities={recurring}")
    return avg


async def profile_get_run(store: MemoryStore, iterations: int = 100):
    """Profile get_run lookups."""
    print("\n=== Profiling Get Run ===")
    runs = await store.list_runs()
    if not runs:
        print("  No runs to test")
        return 0.0
    run_ids = [r["id"] for r in runs[:10]]
    times = []
    for run_id in run_ids * (iterations // len(run_ids) + 1):
        start = time.perf_counter()
        report = await store.get_run(run_id)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        if len(times) >= iterations:
            break
    avg = sum(times) / len(times)
    issues_count = len(report.get("report", {}).get("issues", [])) if report else 0
    print(f"  Get run: {avg*1000:.2f}ms avg (n={iterations}), issues={issues_count}")
    return avg


async def main():
    parser = argparse.ArgumentParser(description="Profile memory search and knowledge graph")
    parser.add_argument("--runs", type=int, default=200, help="Number of mock runs to generate")
    parser.add_argument("--iterations", type=int, default=100, help="Iterations per benchmark")
    args = parser.parse_args()

    # Initialize MemoryStore with a temporary DB
    db_path = Path("/tmp/ghostclaw_profile_memory.db")
    if db_path.exists():
        db_path.unlink()

    # Seed the database with mock data
    await generate_mock_runs(db_path, count=args.runs)

    # Create store
    store = MemoryStore(db_path=db_path)

    # Run benchmarks
    print("\nStarting benchmarks...")
    search_avg = await profile_memory_search(store, iterations=min(args.iterations, 50))
    kg_avg = await profile_knowledge_graph(store, iterations=min(args.iterations, 30))
    get_run_avg = await profile_get_run(store, iterations=min(args.iterations, 50))

    # Summary
    print("\n=== Summary ===")
    print(f"Memory search avg: {search_avg*1000:.2f}ms")
    print(f"Knowledge graph avg: {kg_avg*1000:.2f}ms")
    print(f"Get run avg: {get_run_avg*1000:.2f}ms")
    print(f"\nDB size: {db_path.stat().st_size / 1024:.1f} KB")

    print("\nProfiling complete.")

    # Cleanup
    if db_path.exists():
        db_path.unlink()


if __name__ == "__main__":
    asyncio.run(main())
