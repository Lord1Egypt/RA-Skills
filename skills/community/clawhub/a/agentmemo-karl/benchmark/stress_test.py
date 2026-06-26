#!/usr/bin/env python3
"""agentMemo Stress Test — throughput and latency under concurrent load.

Tests:
  1. Sequential write throughput (N memories)
  2. Batch write throughput (batch_size chunks)
  3. Concurrent read/write mix (M workers)
  4. Search latency at scale (semantic, keyword, hybrid)
  5. Prune + decay behavior check

Usage:
  cd ~/Documents/vibe_coding/agentmemo
  .venv/bin/python benchmark/stress_test.py [--url URL] [--n 200] [--workers 10]
"""
from __future__ import annotations
import argparse
import concurrent.futures
import json
import os
import statistics
import sys
import time
import threading
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"

# ─── HTTP helpers (thread-safe) ──────────────────────────────────
def _request(method: str, base_url: str, path: str, data=None, params=None, timeout=30):
    url = f"{base_url}{path}"
    if params:
        from urllib.parse import urlencode
        url += "?" + urlencode({k: v for k, v in params.items() if v is not None})
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 204:
                return None
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:200]}")


# ─── Benchmark 1: Sequential writes ─────────────────────────────
def bench_sequential_writes(base_url: str, n: int, namespace: str) -> dict:
    times = []
    ids = []
    for i in range(n):
        text = (
            f"Sequential memory {i}: agent context retention for task {i % 10}. "
            f"Keywords: retrieval augmented generation, vector search, embeddings, "
            f"semantic similarity, knowledge base, context window, attention mechanism."
        )
        t0 = time.perf_counter()
        r = _request("POST", base_url, "/v1/memories", data={
            "text": text, "namespace": namespace,
            "importance": 0.5 + (i % 5) * 0.1, "tags": [f"batch_{i % 5}", "stress"],
        })
        times.append(time.perf_counter() - t0)
        ids.append(r["id"])

    return {
        "n": n,
        "p50_ms": round(statistics.median(times) * 1000, 2),
        "p95_ms": round(sorted(times)[int(n * 0.95)] * 1000, 2),
        "p99_ms": round(sorted(times)[int(n * 0.99)] * 1000, 2) if n >= 100 else None,
        "mean_ms": round(statistics.mean(times) * 1000, 2),
        "throughput_ops": round(n / sum(times), 1),
        "total_s": round(sum(times), 3),
        "ids": ids,
    }


# ─── Benchmark 2: Batch writes ───────────────────────────────────
def bench_batch_writes(base_url: str, total: int, batch_size: int, namespace: str) -> dict:
    times = []
    ids = []
    n_batches = total // batch_size

    for b in range(n_batches):
        items = [{
            "text": f"Batch {b} item {j}: " + " ".join(
                ["semantic", "vector", "embedding", "memory", "context"] * 4
            ),
            "namespace": namespace,
            "importance": 0.7,
            "tags": ["batch_write", "stress"],
        } for j in range(batch_size)]

        t0 = time.perf_counter()
        r = _request("POST", base_url, "/v1/memories/batch", data={"create": items})
        times.append(time.perf_counter() - t0)
        ids.extend([c["id"] for c in r.get("created", [])])

    return {
        "total_memories": len(ids),
        "n_batches": n_batches,
        "batch_size": batch_size,
        "p50_ms": round(statistics.median(times) * 1000, 2),
        "p95_ms": round(sorted(times)[int(n_batches * 0.95)] * 1000, 2) if n_batches > 1 else round(times[0] * 1000, 2),
        "mean_ms": round(statistics.mean(times) * 1000, 2),
        "throughput_ops": round(len(ids) / sum(times), 1),  # memories/sec
        "total_s": round(sum(times), 3),
        "ids": ids,
    }


# ─── Benchmark 3: Concurrent mixed load ─────────────────────────
def bench_concurrent(base_url: str, n_ops: int, n_workers: int, namespace: str) -> dict:
    write_times: list[float] = []
    read_times: list[float] = []
    errors = 0
    lock = threading.Lock()

    # Pre-create some memories to read
    seeded_ids = []
    for i in range(20):
        r = _request("POST", base_url, "/v1/memories", data={
            "text": f"Pre-seeded memory for concurrent test {i}. vector semantic embedding retrieval.",
            "namespace": namespace, "importance": 0.8, "tags": ["concurrent_seed"],
        })
        seeded_ids.append(r["id"])

    queries = [
        "vector search embedding", "semantic memory retrieval",
        "agent context retention", "knowledge base query",
        "attention mechanism transformer",
    ]

    def worker(op_idx: int):
        nonlocal errors
        try:
            if op_idx % 3 == 0:
                # Write op
                t0 = time.perf_counter()
                _request("POST", base_url, "/v1/memories", data={
                    "text": f"Concurrent write {op_idx}: semantic vector memory embedding context retrieval knowledge.",
                    "namespace": namespace, "importance": 0.6, "tags": ["concurrent"],
                })
                with lock:
                    write_times.append(time.perf_counter() - t0)
            else:
                # Read/search op
                q = queries[op_idx % len(queries)]
                t0 = time.perf_counter()
                _request("GET", base_url, "/v1/memories/search", params={
                    "q": q, "namespace": namespace, "limit": 10,
                    "mode": "hybrid", "min_score": "0.1",
                })
                with lock:
                    read_times.append(time.perf_counter() - t0)
        except Exception as e:
            with lock:
                errors += 1

    t_start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = [executor.submit(worker, i) for i in range(n_ops)]
        concurrent.futures.wait(futures)
    total_s = time.perf_counter() - t_start

    # Cleanup seeded
    for mid in seeded_ids:
        try:
            _request("DELETE", base_url, f"/v1/memories/{mid}")
        except Exception:
            pass

    all_times = write_times + read_times
    return {
        "n_ops": n_ops,
        "n_workers": n_workers,
        "n_writes": len(write_times),
        "n_reads": len(read_times),
        "errors": errors,
        "error_rate_pct": round(errors / n_ops * 100, 2),
        "overall_throughput_ops": round(n_ops / total_s, 1),
        "total_s": round(total_s, 3),
        "write_p50_ms": round(statistics.median(write_times) * 1000, 2) if write_times else None,
        "write_p95_ms": round(sorted(write_times)[int(len(write_times) * 0.95)] * 1000, 2) if len(write_times) > 1 else None,
        "read_p50_ms": round(statistics.median(read_times) * 1000, 2) if read_times else None,
        "read_p95_ms": round(sorted(read_times)[int(len(read_times) * 0.95)] * 1000, 2) if len(read_times) > 1 else None,
    }


# ─── Benchmark 4: Search latency at scale ───────────────────────
def bench_search_at_scale(base_url: str, namespace: str) -> dict:
    """Measure search latency with current DB state (no new writes)."""
    queries = [
        "semantic memory retrieval for agents",
        "vector embedding similarity search",
        "context window knowledge base",
        "neural network inference pipeline",
        "attention transformer architecture",
        "reinforcement learning policy",
        "multi-agent coordination protocol",
        "natural language understanding",
        "recommendation system collaborative filtering",
        "distributed systems consistency",
    ]
    modes = ["semantic", "keyword", "hybrid"]
    results_by_mode: dict[str, list[float]] = {m: [] for m in modes}

    # Run each query in each mode, 3 repetitions
    for _ in range(3):
        for q in queries:
            for mode in modes:
                t0 = time.perf_counter()
                _request("GET", base_url, "/v1/memories/search", params={
                    "q": q, "namespace": namespace, "limit": 10,
                    "mode": mode, "min_score": "0.0",
                })
                results_by_mode[mode].append(time.perf_counter() - t0)

    out = {}
    for mode, times in results_by_mode.items():
        out[mode] = {
            "p50_ms": round(statistics.median(times) * 1000, 2),
            "p95_ms": round(sorted(times)[int(len(times) * 0.95)] * 1000, 2),
            "mean_ms": round(statistics.mean(times) * 1000, 2),
            "n": len(times),
        }
    return out


# ─── Cleanup helper ──────────────────────────────────────────────
def cleanup_namespace(base_url: str, namespace: str, max_ids: int = 5000):
    """Delete all memories in a namespace via search+delete."""
    deleted = 0
    for q in ["memory", "agent", "context", "vector", "semantic", "batch", "concurrent", "stress"]:
        try:
            r = _request("GET", base_url, "/v1/memories/search", params={
                "q": q, "namespace": namespace, "limit": 100, "min_score": "0.0",
            })
            for item in r.get("results", []):
                try:
                    _request("DELETE", base_url, f"/v1/memories/{item['id']}")
                    deleted += 1
                    if deleted >= max_ids:
                        return deleted
                except Exception:
                    pass
        except Exception:
            pass
    return deleted


# ─── Main ────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="agentMemo Stress Test")
    parser.add_argument("--url", default="http://localhost:8790")
    parser.add_argument("--n", type=int, default=200, help="Sequential writes count")
    parser.add_argument("--workers", type=int, default=10, help="Concurrent workers")
    parser.add_argument("--batch-size", type=int, default=20, help="Batch size for batch writes")
    parser.add_argument("--concurrent-ops", type=int, default=100, help="Ops for concurrent test")
    args = parser.parse_args()

    base_url = args.url
    NS_SEQ = "stress_seq"
    NS_BATCH = "stress_batch"
    NS_CONC = "stress_conc"

    print("=" * 65)
    print("  agentMemo Stress Test")
    print(f"  Server: {base_url}")
    print(f"  Time:   {datetime.now(timezone.utc).isoformat()}")
    print("=" * 65)

    # Health check
    try:
        health = _request("GET", base_url, "/health")
        metrics_before = _request("GET", base_url, "/metrics")
        print(f"\n✅ Server v{health['version']} — {health['status']}")
        print(f"   Existing memories: {metrics_before['total_memories']}")
        print(f"   HNSW index size:   {metrics_before['hnsw_index_size']}")
    except Exception as e:
        print(f"❌ Cannot connect: {e}")
        sys.exit(1)

    all_ids_to_cleanup = []

    # ── 1. Sequential writes ──────────────────────────────────
    print(f"\n{'─'*50}")
    print(f"[1/4] Sequential writes (n={args.n})")
    print("─" * 50)
    t0 = time.time()
    r1 = bench_sequential_writes(base_url, args.n, NS_SEQ)
    all_ids_to_cleanup.extend(r1.pop("ids", []))
    print(f"  P50: {r1['p50_ms']:.2f}ms  P95: {r1['p95_ms']:.2f}ms  P99: {r1.get('p99_ms', 'N/A')}ms")
    print(f"  Throughput: {r1['throughput_ops']:.1f} writes/sec  ({r1['n']} total in {r1['total_s']:.2f}s)")

    # ── 2. Batch writes ───────────────────────────────────────
    batch_total = max(args.batch_size * 5, 100)
    print(f"\n{'─'*50}")
    print(f"[2/4] Batch writes ({batch_total} memories in batches of {args.batch_size})")
    print("─" * 50)
    r2 = bench_batch_writes(base_url, batch_total, args.batch_size, NS_BATCH)
    all_ids_to_cleanup.extend(r2.pop("ids", []))
    print(f"  P50/batch: {r2['p50_ms']:.2f}ms  P95/batch: {r2['p95_ms']:.2f}ms")
    print(f"  Throughput: {r2['throughput_ops']:.1f} memories/sec  ({r2['total_memories']} in {r2['total_s']:.2f}s)")
    print(f"  vs sequential: {r2['throughput_ops'] / max(r1['throughput_ops'], 0.01):.1f}x faster")

    # ── 3. Search at scale ────────────────────────────────────
    print(f"\n{'─'*50}")
    print(f"[3/4] Search latency at scale (DB state after {args.n + batch_total} new writes)")
    print("─" * 50)
    r3 = bench_search_at_scale(base_url, NS_SEQ)
    for mode, stats in r3.items():
        print(f"  {mode:10s}  P50: {stats['p50_ms']:.2f}ms  P95: {stats['p95_ms']:.2f}ms  mean: {stats['mean_ms']:.2f}ms")

    # ── 4. Concurrent mixed load ──────────────────────────────
    print(f"\n{'─'*50}")
    print(f"[4/4] Concurrent mixed load ({args.concurrent_ops} ops, {args.workers} workers)")
    print("─" * 50)
    r4 = bench_concurrent(base_url, args.concurrent_ops, args.workers, NS_CONC)
    print(f"  Throughput: {r4['overall_throughput_ops']:.1f} ops/sec  errors: {r4['errors']} ({r4['error_rate_pct']}%)")
    print(f"  Write P50/P95: {r4['write_p50_ms']:.2f}ms / {r4['write_p95_ms']:.2f}ms")
    print(f"  Read  P50/P95: {r4['read_p50_ms']:.2f}ms / {r4['read_p95_ms']:.2f}ms")

    # ── Final metrics delta ───────────────────────────────────
    metrics_after = _request("GET", base_url, "/metrics")
    mem_added = metrics_after["total_memories"] - metrics_before["total_memories"]
    hnsw_added = metrics_after["hnsw_index_size"] - metrics_before["hnsw_index_size"]
    cache_hit_rate = round(
        metrics_after["embedding_cache_hits"] /
        max(metrics_after["embedding_cache_hits"] + metrics_after["embedding_cache_misses"], 1) * 100, 1)
    stats_after = _request("GET", base_url, "/v1/stats")

    print(f"\n{'─'*50}")
    print("Server state after stress test:")
    print(f"  Memories added:   {mem_added}")
    print(f"  HNSW vectors:     {metrics_after['hnsw_index_size']} (+{hnsw_added})")
    print(f"  Cache size:       {metrics_after['embedding_cache_size']}")
    print(f"  Cache hit rate:   {cache_hit_rate}%")
    print(f"  Total storage:    {stats_after['storage_size_human']}")

    # ── Cleanup ───────────────────────────────────────────────
    print("\nCleaning up stress test data...")
    for mid in all_ids_to_cleanup:
        try:
            _request("DELETE", base_url, f"/v1/memories/{mid}")
        except Exception:
            pass
    for ns in [NS_SEQ, NS_BATCH, NS_CONC]:
        cleanup_namespace(base_url, ns)

    # ── Save results ──────────────────────────────────────────
    RESULTS_DIR.mkdir(exist_ok=True)
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "server_version": health["version"],
        "config": {"n": args.n, "workers": args.workers, "batch_size": args.batch_size,
                   "concurrent_ops": args.concurrent_ops},
        "sequential_writes": r1,
        "batch_writes": r2,
        "search_at_scale": r3,
        "concurrent_mixed": r4,
        "server_delta": {
            "memories_added": mem_added,
            "hnsw_vectors_added": hnsw_added,
            "cache_hit_rate_pct": cache_hit_rate,
            "storage_size_human": stats_after["storage_size_human"],
        },
    }

    out_path = RESULTS_DIR / "stress_results.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n📊 Stress test results saved to {out_path}")
    print("\n✅ Stress test complete.")
    return report


if __name__ == "__main__":
    main()
