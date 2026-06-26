"""agentMemo v3.0.0 Benchmark Script — with concurrent testing + JSON output."""
from __future__ import annotations
import json
import time
import statistics
import urllib.request
import urllib.error
import random
import sys
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://localhost:8790"
RESULTS = {}


def _request(method: str, path: str, data=None, params=None):
    url = f"{BASE_URL}{path}"
    if params:
        from urllib.parse import urlencode
        url += "?" + urlencode({k: v for k, v in params.items() if v is not None})
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        if resp.status == 204:
            return None
        return json.loads(resp.read())


def _random_text(length=100):
    words = ["agent", "memory", "semantic", "search", "vector", "embedding",
             "neural", "context", "retrieve", "store", "knowledge", "graph",
             "attention", "transformer", "model", "inference", "learning",
             "distributed", "cache", "index", "query", "similarity", "cosine",
             "namespace", "vault", "mesh", "pipeline", "data", "token", "batch"]
    return " ".join(random.choices(words, k=length // 5))


def _stats(times, label):
    if not times:
        return {}
    s = {
        "mean_ms": round(statistics.mean(times) * 1000, 1),
        "p50_ms": round(statistics.median(times) * 1000, 1),
        "p95_ms": round(sorted(times)[int(len(times) * 0.95)] * 1000, 1) if len(times) >= 2 else round(times[0] * 1000, 1),
        "rate_ops": round(len(times) / sum(times), 1) if sum(times) > 0 else 0,
        "total_s": round(sum(times), 2),
    }
    print(f"  Mean:  {s['mean_ms']}ms | P50: {s['p50_ms']}ms | P95: {s['p95_ms']}ms | Rate: {s['rate_ops']} ops/s")
    RESULTS[label] = s
    return s


def benchmark_create(n=100):
    print(f"\n--- Create {n} memories ---")
    times, ids = [], []
    for i in range(n):
        t0 = time.perf_counter()
        result = _request("POST", "/v1/memories", data={
            "text": _random_text(), "namespace": "benchmark",
            "importance": random.uniform(0.3, 1.0),
            "tags": random.sample(["test", "bench", "perf", "v2", "demo"], k=random.randint(1, 3)),
        })
        times.append(time.perf_counter() - t0)
        ids.append(result["id"])
    _stats(times, "create")
    return ids


def benchmark_batch_create(n=100, batch_size=20):
    print(f"\n--- Batch create {n} (batch={batch_size}) ---")
    times, ids = [], []
    for i in range(0, n, batch_size):
        batch = [{"text": _random_text(), "namespace": "benchmark_batch",
                   "importance": random.uniform(0.3, 1.0), "tags": ["batch"]}
                 for _ in range(min(batch_size, n - i))]
        t0 = time.perf_counter()
        result = _request("POST", "/v1/memories/batch", data={"create": batch})
        times.append(time.perf_counter() - t0)
        ids.extend([c["id"] for c in result["created"]])
    _stats(times, "batch_create")
    return ids


def benchmark_search(queries=30):
    print(f"\n--- Search ({queries} queries each mode) ---")
    terms = ["agent memory", "vector search", "semantic retrieval", "embedding model",
             "knowledge graph", "neural network", "distributed cache", "batch processing"]
    for mode in ["semantic", "keyword", "hybrid"]:
        times = []
        for _ in range(queries):
            t0 = time.perf_counter()
            _request("GET", "/v1/memories/search", params={"q": random.choice(terms), "limit": 10, "mode": mode, "min_score": "0.1"})
            times.append(time.perf_counter() - t0)
        print(f"  [{mode}]")
        _stats(times, f"search_{mode}")


def benchmark_get(ids, n=50):
    print(f"\n--- Get {n} memories ---")
    sample = random.sample(ids, min(n, len(ids)))
    times = []
    for mid in sample:
        t0 = time.perf_counter()
        _request("GET", f"/v1/memories/{mid}")
        times.append(time.perf_counter() - t0)
    _stats(times, "get")


def benchmark_update(ids, n=20):
    print(f"\n--- Update {n} memories ---")
    sample = random.sample(ids, min(n, len(ids)))
    times = []
    for mid in sample:
        t0 = time.perf_counter()
        _request("PUT", f"/v1/memories/{mid}", data={"text": _random_text(), "tags": ["updated"]})
        times.append(time.perf_counter() - t0)
    _stats(times, "update")


def benchmark_concurrent(ids, threads=10, requests_per_thread=10):
    print(f"\n--- Concurrent ({threads} threads × {requests_per_thread} req) ---")
    times = []
    errors = [0]

    def worker():
        local_times = []
        for _ in range(requests_per_thread):
            try:
                t0 = time.perf_counter()
                _request("GET", "/v1/memories/search", params={"q": "agent memory", "limit": 5, "mode": "semantic", "min_score": "0.1"})
                local_times.append(time.perf_counter() - t0)
            except Exception:
                errors[0] += 1
        return local_times

    with ThreadPoolExecutor(max_workers=threads) as pool:
        futures = [pool.submit(worker) for _ in range(threads)]
        t_start = time.perf_counter()
        for f in as_completed(futures):
            times.extend(f.result())
        total_time = time.perf_counter() - t_start

    total_req = threads * requests_per_thread
    print(f"  Total: {total_req} requests in {total_time:.2f}s")
    print(f"  Throughput: {total_req / total_time:.1f} req/s | Errors: {errors[0]}")
    _stats(times, "concurrent")
    RESULTS["concurrent"]["throughput"] = round(total_req / total_time, 1)
    RESULTS["concurrent"]["errors"] = errors[0]


def cleanup(ids):
    print(f"\n--- Cleanup: {len(ids)} memories ---")
    t0 = time.perf_counter()
    for mid in ids:
        try:
            _request("DELETE", f"/v1/memories/{mid}")
        except Exception:
            pass
    print(f"  {len(ids)/(time.perf_counter()-t0):.1f} ops/s")


def main():
    print("=" * 60)
    print("  agentMemo v3.0.0 Benchmark")
    print("=" * 60)

    try:
        health = _request("GET", "/health")
        print(f"\nServer: {health['status']} (v{health['version']}, uptime {health['uptime_seconds']:.0f}s)")
    except Exception as e:
        print(f"\nERROR: Cannot connect to {BASE_URL}: {e}")
        return

    # Memory usage
    try:
        import resource
        mem_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # KB on macOS
        RESULTS["mem_before_mb"] = round(mem_before / 1024, 1)
    except Exception:
        pass

    ids1 = benchmark_create(100)
    ids2 = benchmark_batch_create(100, batch_size=20)
    all_ids = ids1 + ids2

    benchmark_search(30)
    benchmark_get(all_ids, 50)
    benchmark_update(ids1, 20)
    benchmark_concurrent(all_ids, threads=8, requests_per_thread=10)

    # Metrics
    metrics = _request("GET", "/metrics")
    print(f"\n--- Server Metrics ---")
    print(f"  Requests: {metrics['total_requests']} ({metrics['requests_per_minute']:.1f}/min)")
    print(f"  Cache: {metrics['embedding_cache_size']} entries ({metrics['embedding_cache_hits']} hits)")
    print(f"  HNSW: {metrics['hnsw_index_size']} vectors")
    RESULTS["server"] = {k: metrics[k] for k in ["total_requests", "embedding_cache_size", "embedding_cache_hits", "hnsw_index_size"]}

    cleanup(all_ids)

    # JSON output
    json_path = os.path.join(os.path.dirname(__file__), "benchmark_results.json")
    RESULTS["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    RESULTS["version"] = health["version"]
    with open(json_path, "w") as f:
        json.dump(RESULTS, f, indent=2)
    print(f"\nResults saved to {json_path}")
    print("Done.")


if __name__ == "__main__":
    main()
