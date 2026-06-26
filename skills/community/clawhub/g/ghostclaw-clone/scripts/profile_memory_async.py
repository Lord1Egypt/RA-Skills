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
    """Generate mock analysis runs by inserting directly into the DB."""
    print(f"Generating {count} mock analysis runs...")
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

    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                vibe_score INTEGER,
                stack TEXT,
                files_analyzed INTEGER,
                total_lines INTEGER,
                repo_path TEXT,
                report_json TEXT
            )
        """)
        await db.commit()

        for i in range(count):
            run_id = f"run_{i+1:04d}"
            repo_path = "/mock/repo"
            timestamp = (base_time - timedelta(days=count - i)).isoformat() + "Z"
            vibe_score = random.randint(50, 95)
            num_ghosts = random.randint(0, 10)
            num_flags = random.randint(5, 30)
            files_analyzed = random.randint(50, 200)
            total_lines = random.randint(5000, 50000)
            stack = random.choice(["python", "typescript", "java", "go"])

            issues = []
            for _ in range(num_ghosts + num_flags):
                issues.append({
                    "type": random.choice(["ghost", "flag"]),
                    "file": random.choice(sample_files),
                    "line": random.randint(1, 500),
                    "message": random.choice(sample_issues),
                    "severity": random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])
                })

            # Split issues into ghosts and flags for compatibility
            ghosts = [iss for iss in issues if iss["type"] == "ghost"]
            flags = [iss for iss in issues if iss["type"] == "flag"]

            report = {
                "run_id": run_id,
                "repo_path": repo_path,
                "timestamp": timestamp,
                "vibe_score": vibe_score,
                "files_analyzed": files_analyzed,
                "total_lines": total_lines,
                "stack": stack,
                "issues": issues,
                "architectural_ghosts": ghosts,
                "red_flags": flags,
                "summary": f"Analysis run {i+1}"
            }
            report_json = json.dumps(report)

            await db.execute(
                "INSERT INTO reports (timestamp, vibe_score, stack, files_analyzed, total_lines, repo_path, report_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (timestamp, vibe_score, stack, files_analyzed, total_lines, repo_path, report_json)
            )
        await db.commit()

    # Verify count
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT COUNT(*) FROM reports") as cursor:
            row = await cursor.fetchone()
            total = row[0]
    print(f"Generated {count} runs; DB now has {total} records.")


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
    recurring = len(graph.get('recurring_issues', []))
    print(f"  Knowledge graph: {avg*1000:.2f}ms avg (n={iterations}), recurring_issues={recurring}")
    return avg


async def profile_get_run(store: MemoryStore, iterations: int = 100):
    """Profile get_run lookups."""
    print("\n=== Profiling Get Run ===")
    runs = await store.list_runs()
    if not runs:
        print("  No runs to test")
        return 0.0
    # Use integer DB IDs from summaries
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
    issues_count = len(report.get('issues', [])) if report else 0
    print(f"  Get run: {avg*1000:.2f}ms avg (n={iterations}), issues={issues_count}")
    return avg


async def main():
    parser = argparse.ArgumentParser(description="Profile memory search and knowledge graph")
    parser.add_argument("--runs", type=int, default=50, help="Number of mock runs to generate")
    parser.add_argument("--iterations", type=int, default=100, help="Iterations per benchmark")
    args = parser.parse_args()

    # Initialize MemoryStore with a temporary DB
    tmpdir = Path("/tmp")
    db_path = tmpdir / "ghostclaw_profile_memory.db"
    if db_path.exists():
        db_path.unlink()
    store = MemoryStore(db_path=db_path)

    # Generate mock data
    await generate_mock_runs(db_path, count=args.runs)

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

    print("\nProfiling complete.")

    # Cleanup
    if db_path.exists():
        db_path.unlink()


if __name__ == "__main__":
    asyncio.run(main())
