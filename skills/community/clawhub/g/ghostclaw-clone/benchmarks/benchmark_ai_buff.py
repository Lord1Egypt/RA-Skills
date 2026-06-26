"""
AI-Buff Performance Benchmark

Compares latency and cache effectiveness with AI-Buff enabled vs disabled.
Simulates an agent workflow: multiple searches and run retrievals on a populated QMD store.
"""

import argparse
import asyncio
import json
import time
from pathlib import Path

from ghostclaw.core.qmd_store import QMDMemoryStore
from ghostclaw.core.config import GhostclawConfig
from ghostclaw.core.vector_store.cache import EmbeddingCache
from ghostclaw.core.search_cache import SearchCache

def human_size(num: float, suffix: str = "B") -> str:
    for unit in ["", "K", "M", "G", "T"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}PB{suffix}"

def human_ms(ms: float) -> str:
    return f"{ms:6.3f}ms"

def print_header(text: str):
    print(f"\n{'='*60}\n{text}\n{'='*60}")

def print_row(label: str, baseline: str, buffed: str, improvement: str = ""):
    print(f"{label:30} {baseline:>12} {buffed:>12} {improvement:>12}")

async def run_benchmark(repo_path: Path, iterations: int = 100):
    """Run benchmark simulation."""
    print_header(f"AI-Buff Benchmark: {repo_path} | iterations={iterations}")

    # Load config from repo
    try:
        cfg = GhostclawConfig.load(repo_path)
    except Exception:
        print("⚠️  No repo config found, using defaults")
        cfg = None

    db_path = repo_path / ".ghostclaw" / "storage" / "qmd" / "ghostclaw.db"
    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        print("   Run: ghostclaw analyze . --use-qmd first")
        return

    # Queries to simulate (common agent search patterns)
    test_queries = [
        "security issues",
        "authentication bypass",
        "memory leak",
        "performance optimization",
        "sql injection",
        "xss vulnerability",
        "race condition",
        "buffer overflow",
        "configuration error",
        "dependency vulnerability",
    ]

    # --- Run 1: Baseline (AI-Buff disabled) ---
    print_header("Baseline (AI-Buff DISABLED)")
    baseline_store = QMDMemoryStore(
        db_path=db_path,
        use_enhanced=True,
        embedding_backend=getattr(cfg, 'embedding_backend', 'fastembed') if cfg else 'fastembed',
        ai_buff_enabled=False
    )
    # Initialize vector store if enhanced
    if baseline_store.use_enhanced and baseline_store.vector_store:
        await baseline_store.vector_store.initialize()

    baseline_search_times = []
    baseline_getrun_times = []

    print("Running warm-up...")
    for query in test_queries[:3]:
        await baseline_store.search(query, limit=5)

    print(f"Executing {iterations} search + get_run cycles...")
    for i in range(iterations):
        query = test_queries[i % len(test_queries)]
        start = time.perf_counter()
        results = await baseline_store.search(query, limit=5)
        search_time = (time.perf_counter() - start) * 1000
        baseline_search_times.append(search_time)

        if results:
            # Use first match's 'id' or 'report_id' (store returns 'id' field from DB)
            run_identifier = results[0].get('report_id') or results[0].get('id')
            if run_identifier:
                start = time.perf_counter()
                await baseline_store.get_run(run_identifier)
                getrun_time = (time.perf_counter() - start) * 1000
                baseline_getrun_times.append(getrun_time)

    baseline_stats = baseline_store.get_stats()
    print("\nBaseline results:")
    print(f"  Search avg: {human_ms(sum(baseline_search_times)/len(baseline_search_times))}")
    print(f"  GetRun avg: {human_ms(sum(baseline_getrun_times)/len(baseline_getrun_times)) if baseline_getrun_times else 'N/A'}")
    emb_cache = baseline_stats.get('embedding_cache') or {}
    search_cache = baseline_stats.get('search_cache') or {}
    print(f"  Embedding cache: {emb_cache.get('size',0)} entries")
    print(f"  Search cache: {search_cache.get('size',0)} entries")

    # --- Run 2: AI-Buff enabled ---
    print_header("AI-Buff ENABLED (caching + query planning)")
    buffed_store = QMDMemoryStore(
        db_path=db_path,
        use_enhanced=True,
        embedding_backend=getattr(cfg, 'embedding_backend', 'fastembed') if cfg else 'fastembed',
        ai_buff_enabled=True
    )
    # Vector store will initialize on first use

    # Reset cache state (should be warm from baseline but separate store)
    buffed_search_times = []
    buffed_getrun_times = []

    print("Running warm-up...")
    for query in test_queries[:3]:
        await buffed_store.search(query, limit=5)

    print(f"Executing {iterations} search + get_run cycles...")
    for i in range(iterations):
        query = test_queries[i % len(test_queries)]
        start = time.perf_counter()
        results = await buffed_store.search(query, limit=5)
        search_time = (time.perf_counter() - start) * 1000
        buffed_search_times.append(search_time)

        if results:
            run_identifier = results[0].get('report_id') or results[0].get('id')
            if run_identifier:
                start = time.perf_counter()
                await buffed_store.get_run(run_identifier)
                getrun_time = (time.perf_counter() - start) * 1000
                buffed_getrun_times.append(getrun_time)

    buffed_stats = buffed_store.get_stats()
    print("\nAI-Buff results:")
    print(f"  Search avg: {human_ms(sum(buffed_search_times)/len(buffed_search_times))}")
    print(f"  GetRun avg: {human_ms(sum(buffed_getrun_times)/len(buffed_getrun_times)) if buffed_getrun_times else 'N/A'}")
    emb_cache_b = buffed_stats.get('embedding_cache') or {}
    search_cache_b = buffed_stats.get('search_cache') or {}
    print(f"  Embedding cache: {emb_cache_b.get('size',0)} entries, hits={emb_cache_b.get('hits',0)}, misses={emb_cache_b.get('misses',0)}")
    print(f"  Search cache: {search_cache_b.get('size',0)} entries, hits={search_cache_b.get('hits',0)}, misses={search_cache_b.get('misses',0)}")
    print(f"  Query plan: {buffed_stats.get('last_plan', {})}")

    # --- Summary ---
    print_header("SUMMARY")
    base_search_avg = sum(baseline_search_times)/len(baseline_search_times)
    buffed_search_avg = sum(buffed_search_times)/len(buffed_search_times)
    search_improvement = ((base_search_avg - buffed_search_avg) / base_search_avg) * 100

    print_row("Metric", "Baseline", "AI-Buff", "Δ (%)")
    print_row("-"*60, "-"*12, "-"*12, "-"*12)
    print_row("Search Avg", human_ms(base_search_avg), human_ms(buffed_search_avg), f"{search_improvement:+.1f}%")

    if baseline_getrun_times and buffed_getrun_times:
        base_getrun_avg = sum(baseline_getrun_times)/len(baseline_getrun_times)
        buffed_getrun_avg = sum(buffed_getrun_times)/len(buffed_getrun_times)
        getrun_improvement = ((base_getrun_avg - buffed_getrun_avg) / base_getrun_avg) * 100
        print_row("GetRun Avg", human_ms(base_getrun_avg), human_ms(buffed_getrun_avg), f"{getrun_improvement:+.1f}%")

    # Cache hit rates
    emb_hit_rate = (emb_cache_b.get('hits',0) / max(1, (emb_cache_b.get('hits',0) + emb_cache_b.get('misses',0)))) * 100
    search_hit_rate = (search_cache_b.get('hits',0) / max(1, (search_cache_b.get('hits',0) + search_cache_b.get('misses',0)))) * 100
    print_row("Emb Hit Rate", "n/a", f"{emb_hit_rate:.1f}%", "")
    print_row("Search Hit Rate", "n/a", f"{search_hit_rate:.1f}%", "")

async def main():
    parser = argparse.ArgumentParser(description="AI-Buff Benchmark")
    parser.add_argument("repo", type=Path, help="Path to repository with QMD database")
    parser.add_argument("--iterations", type=int, default=100, help="Number of search cycles (default: 100)")
    args = parser.parse_args()

    await run_benchmark(args.repo, args.iterations)

if __name__ == "__main__":
    asyncio.run(main())
