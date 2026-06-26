#!/usr/bin/env python3
"""
Benchmark BM25 search performance in QMDMemoryStore.

Generates synthetic reports and measures query latency.
"""

import asyncio
import random
import time
from pathlib import Path
from ghostclaw.core.qmd_store import QMDMemoryStore

# Sample words for synthetic issue/ghost generation
ISSUE_WORDS = [
    "security", "performance", "memory", "leak", "race", "condition",
    "authentication", "bypass", "injection", "xss", "csrf", "sql",
    "null", "pointer", "exception", "timeout", "deadlock", "lock",
    "callback", "hell", "god", "object", "spaghetti", "code"
]

def generate_synthetic_report(index: int) -> dict:
    """Generate a random report for benchmarking."""
    # Pick 1-3 random issue words
    num_issues = random.randint(1, 3)
    issue_words = random.sample(ISSUE_WORDS, num_issues)
    issues = [{"message": f"Issue: {w}"} for w in issue_words]

    # Maybe add a ghost
    ghost_words = random.sample(ISSUE_WORDS, random.randint(0, 2))
    ghosts = [{"message": f"Ghost: {w}"} for w in ghost_words]

    # AI synthesis with some of the words
    synth_words = random.sample(ISSUE_WORDS, random.randint(2, 5))
    synthesis = " ".join(f"Discussion about {w}." for w in synth_words)

    return {
        "vibe_score": random.randint(40, 95),
        "stack": random.choice(["python", "node", "java", "go", "rust"]),
        "files_analyzed": random.randint(5, 50),
        "total_lines": random.randint(100, 5000),
        "issues": issues,
        "architectural_ghosts": ghosts,
        "ai_synthesis": synthesis,
        "metadata": {"timestamp": f"2026-03-14T12:{index:02d}:00Z"}
    }

async def main():
    import argparse
    parser = argparse.ArgumentParser(description="Benchmark QMD BM25 search")
    parser.add_argument("--reports", type=int, default=1000, help="Number of synthetic reports to generate")
    parser.add_argument("--queries", type=int, default=50, help="Number of search queries to run")
    parser.add_argument("--db-dir", type=Path, default=Path("./benchmark_qmd_db"), help="Directory for benchmark DB")
    args = parser.parse_args()

    db_path = args.db_dir / "qmd.db"
    if db_path.exists():
        print(f"Using existing DB at {db_path}")
    else:
        print(f"Creating new DB at {db_path} and generating {args.reports} reports...")
        store = QMDMemoryStore(db_path=db_path, use_enhanced=False)
        await store.fts.ensure_initialized()
        # Generate reports
        for i in range(args.reports):
            report = generate_synthetic_report(i)
            await store.save_run(report, repo_path=str(db_path.parent))
            if (i+1) % 100 == 0:
                print(f"  Generated {i+1} reports...")
        print(f"✓ Generated {args.reports} reports")

    # Initialize store for searching
    store = QMDMemoryStore(db_path=db_path, use_enhanced=False)
    await store.fts.ensure_initialized()

    # Benchmark queries
    print(f"\nRunning {args.queries} search queries...")
    timings = []
    for i in range(args.queries):
        # Pick a random word from ISSUE_WORDS as query
        query = random.choice(ISSUE_WORDS)
        start = time.perf_counter()
        results = await store.search(query, limit=10)
        elapsed = time.perf_counter() - start
        timings.append(elapsed)
        if (i+1) % 10 == 0:
            avg = sum(timings[-10:]) / 10
            print(f"  Query {i+1}/{args.queries}: {elapsed*1000:.2f}ms (avg last 10: {avg*1000:.2f}ms, results={len(results)})")

    # Statistics
    timings_ms = [t*1000 for t in timings]
    p50 = sorted(timings_ms)[len(timings_ms)//2]
    p99 = sorted(timings_ms)[int(0.99*len(timings_ms))] if len(timings_ms) >= 100 else max(timings_ms)
    avg = sum(timings_ms)/len(timings_ms)

    print("\n=== Benchmark Results ===")
    print(f"Total reports: {args.reports}")
    print(f"Total queries: {args.queries}")
    print(f"Average latency: {avg:.2f}ms")
    print(f"P50 latency: {p50:.2f}ms")
    print(f"P99 latency: {p99:.2f}ms")
    print(f"Min: {min(timings_ms):.2f}ms")
    print(f"Max: {max(timings_ms):.2f}ms")

    # Success threshold: <50ms p50
    if p50 < 50:
        print("\n✅ PASS: P50 latency < 50ms")
    else:
        print(f"\n❌ FAIL: P50 latency {p50:.2f}ms exceeds 50ms threshold")

if __name__ == "__main__":
    asyncio.run(main())
