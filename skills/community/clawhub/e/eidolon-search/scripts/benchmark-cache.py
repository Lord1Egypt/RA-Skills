#!/usr/bin/env python3
"""
Cache Performance Benchmark for Eidolon Search

Compares warm cache vs cold cache search times.
"""

import sqlite3
import time
import json
from pathlib import Path
import subprocess
import sys

TEST_QUERIES = [
    "Physical AI 로드맵",
    "Triangle 완성",
    "미라클 철학",
    "Qdrant 설정",
    "FTS5 최적화"
]

def drop_cache():
    """Drop OS page cache (Linux only, requires sudo)"""
    try:
        # Drop page cache, dentries, inodes
        subprocess.run(
            ["sudo", "sync"],
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["sudo", "sh", "-c", "echo 3 > /proc/sys/vm/drop_caches"],
            check=True,
            capture_output=True
        )
        return True
    except Exception as e:
        print(f"Warning: Could not drop OS cache ({e})")
        print("Running benchmark without cache drop...")
        return False

def search_fts(db_path: Path, query: str, limit: int = 10):
    """FTS5 검색"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    start = time.time()
    
    cursor.execute("""
        SELECT path, snippet(memory_fts, 1, '<b>', '</b>', '...', 32) as snippet
        FROM memory_fts
        WHERE memory_fts MATCH ?
        ORDER BY rank
        LIMIT ?
    """, (query, limit))
    
    results = cursor.fetchall()
    elapsed = time.time() - start
    
    conn.close()
    
    return len(results), elapsed

def run_benchmark(db_path: Path, can_drop_cache: bool):
    """벤치마크 실행"""
    print("=" * 60)
    print("Cache Performance Benchmark for Eidolon Search")
    print("=" * 60)
    print()
    
    cold_times = []
    warm_times = []
    
    for query in TEST_QUERIES:
        # Cold cache (if available)
        if can_drop_cache:
            drop_cache()
            time.sleep(0.5)  # Let cache settle
        
        count_cold, time_cold = search_fts(db_path, query)
        cold_times.append(time_cold)
        
        # Warm cache (immediate re-run)
        count_warm, time_warm = search_fts(db_path, query)
        warm_times.append(time_warm)
        
        cache_type = "cold" if can_drop_cache else "first"
        print(f'Query: "{query}"')
        print(f"  {cache_type.capitalize()}: {time_cold*1000:.2f}ms ({count_cold} results)")
        print(f"  Warm:  {time_warm*1000:.2f}ms ({count_warm} results)")
        print(f"  Speedup: {time_cold/time_warm:.1f}x")
        print()
    
    # Summary
    avg_cold = sum(cold_times) / len(cold_times)
    avg_warm = sum(warm_times) / len(warm_times)
    
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    cache_type = "Cold" if can_drop_cache else "First"
    print(f"Average {cache_type} Cache: {avg_cold*1000:.2f}ms")
    print(f"Average Warm Cache:  {avg_warm*1000:.2f}ms")
    print(f"Average Speedup:     {avg_cold/avg_warm:.1f}x")
    print()
    
    if not can_drop_cache:
        print("Note: OS cache drop not available (no sudo). Results show")
        print("first-run vs second-run instead of true cold vs warm.")
        print()
    
    # Export
    output = {
        "cache_drop_available": can_drop_cache,
        "queries": TEST_QUERIES,
        "cold_times_ms": [t * 1000 for t in cold_times],
        "warm_times_ms": [t * 1000 for t in warm_times],
        "summary": {
            "avg_cold_ms": avg_cold * 1000,
            "avg_warm_ms": avg_warm * 1000,
            "avg_speedup": avg_cold / avg_warm
        }
    }
    
    return output

if __name__ == "__main__":
    db_path = Path(__file__).parent.parent / "db" / "memory.db"
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        print("Run 'python scripts/build-index.py' first to create the index.")
        sys.exit(1)
    
    can_drop = drop_cache()
    output = run_benchmark(db_path, can_drop)
    
    # Save
    output_path = Path(__file__).parent.parent / "docs" / "benchmark-cache.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Results saved to: {output_path}")
