#!/usr/bin/env python3
"""agentMemo Evaluation Benchmark — Baseline (stateless) vs agentMemo (with memory).

Runs 30+ sample tasks across 5 categories, comparing task completion, correctness,
response time, token cost, and memory hit rate.

Requires: agentMemo server running at localhost:8790
Usage: cd ~/Documents/vibe_coding/agentvault && .venv/bin/python benchmark/agentvault_eval.py
"""
from __future__ import annotations
import json
import os
import sys
import time
import statistics
import random
import urllib.request
import urllib.error
import traceback
from datetime import datetime, timezone
from typing import Optional

BASE_URL = os.environ.get("AGENTMEMO_URL", "http://localhost:8790")
EVAL_NAMESPACE = "eval_benchmark"
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")


# ─── HTTP helpers ───────────────────────────────────────────────
def _request(method: str, path: str, data=None, params=None):
    url = f"{BASE_URL}{path}"
    if params:
        from urllib.parse import urlencode
        url += "?" + urlencode({k: v for k, v in params.items() if v is not None})
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        if resp.status == 204:
            return None
        return json.loads(resp.read())


# ─── Task definitions (30 samples across 5 categories) ─────────
def _build_task_set():
    """Build 30+ evaluation tasks grouped by category."""
    tasks = []

    # Category 1: Multi-turn context retention (6 tasks)
    context_pairs = [
        {"seed": "My favorite color is deep navy blue", "query": "What color do I prefer?", "expected_contains": "navy blue"},
        {"seed": "I'm allergic to shellfish and peanuts", "query": "What are my food allergies?", "expected_contains": "shellfish"},
        {"seed": "I use VSCode with Vim keybindings on macOS", "query": "What IDE setup do I use?", "expected_contains": "vscode"},
        {"seed": "My project deadline is March 28th 2026", "query": "When is my project deadline?", "expected_contains": "march 28"},
        {"seed": "The API rate limit was set to 100 req/min after the outage", "query": "What is the current API rate limit?", "expected_contains": "100"},
        {"seed": "We decided to use PostgreSQL instead of MongoDB for the user service", "query": "Which database did we choose for the user service?", "expected_contains": "postgresql"},
    ]
    for i, cp in enumerate(context_pairs):
        tasks.append({"id": f"ctx_{i+1}", "category": "context_retention", **cp})

    # Category 2: Preference recall (6 tasks)
    prefs = [
        {"seed": "I prefer Python type hints with strict mypy checking", "query": "How do I like my Python typed?", "expected_contains": "strict"},
        {"seed": "For deployment I always want blue-green with automatic rollback", "query": "What deployment strategy do I prefer?", "expected_contains": "blue-green"},
        {"seed": "I like my commit messages in conventional commit format", "query": "What commit message format do I use?", "expected_contains": "conventional"},
        {"seed": "My preferred LLM temperature is 0.3 for coding tasks", "query": "What temperature should I use for coding LLM calls?", "expected_contains": "0.3"},
        {"seed": "I want all API responses to use snake_case keys", "query": "What casing convention for API responses?", "expected_contains": "snake_case"},
        {"seed": "I use 2-space indentation for TypeScript and 4-space for Python", "query": "What indentation do I use for TypeScript?", "expected_contains": "2"},
    ]
    for i, p in enumerate(prefs):
        tasks.append({"id": f"pref_{i+1}", "category": "preference_recall", **p})

    # Category 3: Project state tracking (6 tasks)
    states = [
        {"seed": "Sprint 12: completed auth service migration, payment service still pending", "query": "What was completed in sprint 12?", "expected_contains": "auth service"},
        {"seed": "Backend PR #247 is blocked by the CI pipeline fix from DevOps", "query": "What is blocking PR #247?", "expected_contains": "ci pipeline"},
        {"seed": "The recommendation model v3 achieved 0.82 NDCG on test set", "query": "What was the NDCG score of recommendation model v3?", "expected_contains": "0.82"},
        {"seed": "Database migration to v5 schema was rolled back due to index corruption", "query": "What happened with the v5 schema migration?", "expected_contains": "rolled back"},
        {"seed": "The new caching layer reduced P99 latency from 450ms to 120ms", "query": "What latency improvement did the caching layer achieve?", "expected_contains": "120"},
        {"seed": "Feature flag dark-mode-v2 is enabled for 30% of users", "query": "What percentage of users have dark-mode-v2?", "expected_contains": "30%"},
    ]
    for i, s in enumerate(states):
        tasks.append({"id": f"state_{i+1}", "category": "project_state", **s})

    # Category 4: Cross-session decision consistency (6 tasks)
    decisions = [
        {"seed": "Architecture decision: microservices with gRPC for internal, REST for external", "query": "What protocol for internal service communication?", "expected_contains": "grpc"},
        {"seed": "Logging standard: structured JSON logs, sent to Datadog via fluentd", "query": "Where do we send logs?", "expected_contains": "datadog"},
        {"seed": "Error handling: all services must return RFC 7807 problem details", "query": "What error format standard do we follow?", "expected_contains": "7807"},
        {"seed": "Testing policy: minimum 80% unit test coverage, integration tests for all API endpoints", "query": "What is our minimum test coverage requirement?", "expected_contains": "80%"},
        {"seed": "Secret management: all secrets in Vault, rotated every 90 days", "query": "How often do we rotate secrets?", "expected_contains": "90"},
        {"seed": "Branch strategy: trunk-based development with short-lived feature branches", "query": "What branching strategy do we use?", "expected_contains": "trunk"},
    ]
    for i, d in enumerate(decisions):
        tasks.append({"id": f"decision_{i+1}", "category": "decision_consistency", **d})

    # Category 5: Error correction memory (6 tasks)
    corrections = [
        {"seed": "CORRECTION: The /users endpoint returns 200 not 201 for list operations. Previous response was wrong.", "query": "What status code does GET /users return?", "expected_contains": "200"},
        {"seed": "CORRECTION: Redis TTL should be 3600s not 7200s. The 7200 value caused stale cache issues.", "query": "What Redis TTL should we use?", "expected_contains": "3600"},
        {"seed": "CORRECTION: The ML pipeline uses PyTorch 2.1 not TensorFlow. I misstated earlier.", "query": "What ML framework do we use?", "expected_contains": "pytorch"},
        {"seed": "CORRECTION: Max file upload size is 10MB not 50MB. 50MB caused OOM in Lambda.", "query": "What is the max file upload size?", "expected_contains": "10mb"},
        {"seed": "CORRECTION: Use UTC timestamps everywhere, not local time. Local time caused timezone bugs.", "query": "What timezone format should we use in the system?", "expected_contains": "utc"},
        {"seed": "CORRECTION: Connection pool size should be 20 not 50. 50 caused connection exhaustion under load.", "query": "What should the connection pool size be?", "expected_contains": "20"},
    ]
    for i, c in enumerate(corrections):
        tasks.append({"id": f"correction_{i+1}", "category": "error_correction", **c})

    return tasks


# ─── Baseline agent (stateless) ─────────────────────────────────
class BaselineAgent:
    """Stateless agent — no memory, answers based only on the current query."""

    def answer(self, query: str, seed_text: str = None) -> dict:
        """Without memory, the agent can only say 'I don't know' or guess."""
        t0 = time.perf_counter()
        # Simulate a stateless agent that has no access to prior context
        # In a real system this would be an LLM call without memory augmentation
        response = f"I don't have information about that. Could you provide more context?"
        elapsed = time.perf_counter() - t0
        return {
            "response": response,
            "latency_s": elapsed,
            "tokens_used": len(query.split()) + len(response.split()),
            "memory_hits": 0,
        }


# ─── agentMemo agent (with memory) ─────────────────────────────
class VaultAgent:
    """Agent with agentMemo memory — stores and retrieves context."""

    def __init__(self):
        self.stored_ids = []

    def store_memory(self, text: str, tags: list[str] = None, importance: float = 0.8) -> dict:
        t0 = time.perf_counter()
        result = _request("POST", "/v1/memories", data={
            "text": text, "namespace": EVAL_NAMESPACE,
            "importance": importance, "tags": tags or ["eval"],
        })
        elapsed = time.perf_counter() - t0
        self.stored_ids.append(result["id"])
        return {"id": result["id"], "write_latency_s": elapsed}

    def answer(self, query: str) -> dict:
        """Search memory, then compose answer from retrieved context."""
        t0_search = time.perf_counter()
        search_result = _request("GET", "/v1/memories/search", params={
            "q": query, "namespace": EVAL_NAMESPACE, "limit": 5,
            "mode": "hybrid", "min_score": "0.15",
        })
        search_latency = time.perf_counter() - t0_search
        results = search_result.get("results", [])
        hits = len(results)

        # Compose answer from top memory
        if results:
            top = results[0]
            response = f"Based on stored context: {top['text']} (score: {top['score']})"
        else:
            response = "No relevant memories found."

        total_latency = time.perf_counter() - t0_search
        token_estimate = (
            len(query.split()) +
            sum(len(r["text"].split()) for r in results) +
            len(response.split())
        )

        return {
            "response": response,
            "latency_s": total_latency,
            "search_latency_s": search_latency,
            "tokens_used": token_estimate,
            "memory_hits": hits,
            "top_score": results[0]["score"] if results else 0.0,
            "scores": [r["score"] for r in results],
        }

    def cleanup(self):
        for mid in self.stored_ids:
            try:
                _request("DELETE", f"/v1/memories/{mid}")
            except Exception:
                pass
        self.stored_ids = []


# ─── Evaluation engine ──────────────────────────────────────────
def evaluate_task(task: dict, baseline: BaselineAgent, vault: VaultAgent) -> dict:
    """Run one task through both agents and compare."""
    # Phase 1: Store the seed memory in agentMemo
    store_result = vault.store_memory(
        task["seed"],
        tags=[task["category"], "eval"],
        importance=0.85,
    )

    # Small delay for indexing
    time.sleep(0.05)

    # Phase 2: Query both agents
    baseline_result = baseline.answer(task["query"], seed_text=task["seed"])
    vault_result = vault.answer(task["query"])

    # Phase 3: Check correctness
    expected = task["expected_contains"].lower()
    baseline_correct = expected in baseline_result["response"].lower()
    vault_correct = expected in vault_result["response"].lower()

    return {
        "task_id": task["id"],
        "category": task["category"],
        "query": task["query"],
        "expected_contains": task["expected_contains"],
        "baseline": {
            "response": baseline_result["response"][:200],
            "correct": baseline_correct,
            "latency_s": baseline_result["latency_s"],
            "tokens_used": baseline_result["tokens_used"],
            "memory_hits": 0,
        },
        "vault": {
            "response": vault_result["response"][:200],
            "correct": vault_correct,
            "latency_s": vault_result["latency_s"],
            "search_latency_s": vault_result.get("search_latency_s", 0),
            "tokens_used": vault_result["tokens_used"],
            "memory_hits": vault_result["memory_hits"],
            "top_score": vault_result.get("top_score", 0),
        },
        "write_latency_s": store_result["write_latency_s"],
    }


def compute_summary(results: list[dict]) -> dict:
    """Compute aggregate metrics from evaluation results."""
    categories = set(r["category"] for r in results)

    def _agg(group):
        bl_correct = sum(1 for r in group if r["baseline"]["correct"])
        vt_correct = sum(1 for r in group if r["vault"]["correct"])
        n = len(group)
        bl_latencies = [r["baseline"]["latency_s"] for r in group]
        vt_latencies = [r["vault"]["latency_s"] for r in group]
        vt_search_latencies = [r["vault"]["search_latency_s"] for r in group]
        write_latencies = [r["write_latency_s"] for r in group]
        bl_tokens = [r["baseline"]["tokens_used"] for r in group]
        vt_tokens = [r["vault"]["tokens_used"] for r in group]
        hits = [r["vault"]["memory_hits"] for r in group]
        top_scores = [r["vault"]["top_score"] for r in group if r["vault"]["top_score"] > 0]

        return {
            "n": n,
            "baseline_accuracy": round(bl_correct / n * 100, 1),
            "vault_accuracy": round(vt_correct / n * 100, 1),
            "accuracy_lift": round((vt_correct - bl_correct) / n * 100, 1),
            "baseline_latency_p50_ms": round(statistics.median(bl_latencies) * 1000, 2),
            "baseline_latency_p95_ms": round(sorted(bl_latencies)[int(n * 0.95)] * 1000, 2) if n > 1 else round(bl_latencies[0] * 1000, 2),
            "vault_latency_p50_ms": round(statistics.median(vt_latencies) * 1000, 2),
            "vault_latency_p95_ms": round(sorted(vt_latencies)[int(n * 0.95)] * 1000, 2) if n > 1 else round(vt_latencies[0] * 1000, 2),
            "vault_search_latency_p50_ms": round(statistics.median(vt_search_latencies) * 1000, 2),
            "vault_search_latency_p95_ms": round(sorted(vt_search_latencies)[int(n * 0.95)] * 1000, 2) if n > 1 else round(vt_search_latencies[0] * 1000, 2),
            "write_latency_p50_ms": round(statistics.median(write_latencies) * 1000, 2),
            "write_latency_p95_ms": round(sorted(write_latencies)[int(n * 0.95)] * 1000, 2) if n > 1 else round(write_latencies[0] * 1000, 2),
            "baseline_avg_tokens": round(statistics.mean(bl_tokens), 1),
            "vault_avg_tokens": round(statistics.mean(vt_tokens), 1),
            "token_overhead_pct": round((statistics.mean(vt_tokens) - statistics.mean(bl_tokens)) / max(statistics.mean(bl_tokens), 1) * 100, 1),
            "avg_memory_hits": round(statistics.mean(hits), 2),
            "hit_at_1": round(sum(1 for h in hits if h >= 1) / n * 100, 1),
            "hit_at_3": round(sum(1 for h in hits if h >= 3) / n * 100, 1),
            "hit_at_5": round(sum(1 for h in hits if h >= 5) / n * 100, 1),
            "avg_top_score": round(statistics.mean(top_scores), 4) if top_scores else 0,
        }

    summary = {"overall": _agg(results), "by_category": {}}
    for cat in sorted(categories):
        group = [r for r in results if r["category"] == cat]
        summary["by_category"][cat] = _agg(group)

    return summary


def run_storage_benchmark(vault: VaultAgent, n=50) -> dict:
    """Measure storage growth and memory overhead."""
    # Get initial state
    initial_metrics = _request("GET", "/metrics")
    initial_stats = _request("GET", "/v1/stats")

    # Store n memories of varying sizes
    write_times = []
    for i in range(n):
        text = f"Benchmark memory entry {i}: " + " ".join(
            random.choices(["agent", "memory", "context", "retrieval", "embedding",
                           "knowledge", "inference", "pipeline", "vector", "search",
                           "transformer", "attention", "neural", "semantic", "graph"], k=random.randint(10, 40))
        )
        t0 = time.perf_counter()
        result = _request("POST", "/v1/memories", data={
            "text": text, "namespace": "eval_storage_bench",
            "importance": random.uniform(0.3, 1.0), "tags": ["storage_bench"],
        })
        write_times.append(time.perf_counter() - t0)
        vault.stored_ids.append(result["id"])

    # Get final state
    final_metrics = _request("GET", "/metrics")
    final_stats = _request("GET", "/v1/stats")

    # Search benchmark at current scale
    search_times = []
    queries = ["agent memory retrieval", "neural network pipeline", "semantic search vector",
               "knowledge graph context", "transformer embedding inference"]
    for q in queries * 3:  # 15 searches
        t0 = time.perf_counter()
        _request("GET", "/v1/memories/search", params={
            "q": q, "namespace": "eval_storage_bench", "limit": 10, "mode": "semantic", "min_score": "0.1",
        })
        search_times.append(time.perf_counter() - t0)

    return {
        "memories_added": n,
        "storage_growth_bytes": final_stats["storage_size_bytes"] - initial_stats["storage_size_bytes"],
        "storage_per_memory_bytes": round((final_stats["storage_size_bytes"] - initial_stats["storage_size_bytes"]) / n, 1),
        "hnsw_index_growth": final_metrics["hnsw_index_size"] - initial_metrics["hnsw_index_size"],
        "embedding_cache_growth": final_metrics["embedding_cache_size"] - initial_metrics["embedding_cache_size"],
        "write_latency_p50_ms": round(statistics.median(write_times) * 1000, 2),
        "write_latency_p95_ms": round(sorted(write_times)[int(len(write_times) * 0.95)] * 1000, 2),
        "write_latency_mean_ms": round(statistics.mean(write_times) * 1000, 2),
        "search_latency_p50_ms": round(statistics.median(search_times) * 1000, 2),
        "search_latency_p95_ms": round(sorted(search_times)[int(len(search_times) * 0.95)] * 1000, 2),
        "search_latency_mean_ms": round(statistics.mean(search_times) * 1000, 2),
        "total_storage_bytes": final_stats["storage_size_bytes"],
        "total_storage_human": final_stats["storage_size_human"],
        "total_hnsw_vectors": final_metrics["hnsw_index_size"],
        "total_cache_entries": final_metrics["embedding_cache_size"],
        "cache_hit_rate_pct": round(
            final_metrics["embedding_cache_hits"] /
            max(final_metrics["embedding_cache_hits"] + final_metrics["embedding_cache_misses"], 1) * 100, 1),
    }


def main():
    print("=" * 70)
    print("  agentMemo Evaluation Benchmark")
    print(f"  Server: {BASE_URL}")
    print(f"  Time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    # Check server health
    try:
        health = _request("GET", "/health")
        print(f"\n✅ Server: {health['status']} (v{health['version']})")
    except Exception as e:
        print(f"\n❌ Cannot connect to {BASE_URL}: {e}")
        sys.exit(1)

    os.makedirs(RESULTS_DIR, exist_ok=True)

    baseline = BaselineAgent()
    vault = VaultAgent()

    # ── Part A: Task-based evaluation (30 samples) ──────────
    print("\n" + "─" * 50)
    print("Part A: Task Evaluation (30 samples)")
    print("─" * 50)

    tasks = _build_task_set()
    print(f"  Tasks: {len(tasks)} across {len(set(t['category'] for t in tasks))} categories")

    results = []
    for i, task in enumerate(tasks):
        result = evaluate_task(task, baseline, vault)
        results.append(result)
        status = "✅" if result["vault"]["correct"] else "❌"
        print(f"  [{i+1:2d}/{len(tasks)}] {status} {task['id']:20s} | vault_hit@1={result['vault']['memory_hits']>=1} score={result['vault']['top_score']:.3f} | {result['vault']['latency_s']*1000:.1f}ms")

    summary = compute_summary(results)

    print(f"\n  ── Overall Results ──")
    print(f"  Baseline accuracy:  {summary['overall']['baseline_accuracy']}%")
    print(f"  Vault accuracy:     {summary['overall']['vault_accuracy']}%")
    print(f"  Accuracy lift:     +{summary['overall']['accuracy_lift']}%")
    print(f"  Hit@1:              {summary['overall']['hit_at_1']}%")
    print(f"  Hit@3:              {summary['overall']['hit_at_3']}%")
    print(f"  Hit@5:              {summary['overall']['hit_at_5']}%")
    print(f"  Avg top score:      {summary['overall']['avg_top_score']:.4f}")
    print(f"  Vault search P50:   {summary['overall']['vault_search_latency_p50_ms']:.2f}ms")
    print(f"  Vault search P95:   {summary['overall']['vault_search_latency_p95_ms']:.2f}ms")
    print(f"  Token overhead:     {summary['overall']['token_overhead_pct']}%")

    # ── Part B: Storage & cost benchmark ─────────────────────
    print("\n" + "─" * 50)
    print("Part B: Storage & Cost Benchmark")
    print("─" * 50)

    storage_results = run_storage_benchmark(vault, n=50)
    print(f"  Write P50:          {storage_results['write_latency_p50_ms']:.2f}ms")
    print(f"  Write P95:          {storage_results['write_latency_p95_ms']:.2f}ms")
    print(f"  Search P50:         {storage_results['search_latency_p50_ms']:.2f}ms")
    print(f"  Search P95:         {storage_results['search_latency_p95_ms']:.2f}ms")
    print(f"  Storage/memory:     {storage_results['storage_per_memory_bytes']:.0f} bytes")
    print(f"  HNSW vectors:       {storage_results['total_hnsw_vectors']}")
    print(f"  Cache hit rate:     {storage_results['cache_hit_rate_pct']}%")
    print(f"  Total storage:      {storage_results['total_storage_human']}")

    # ── Cleanup ──────────────────────────────────────────────
    print("\n  Cleaning up evaluation data...")
    vault.cleanup()
    # Also clean storage bench namespace
    try:
        mems, _ = [], None
        search = _request("GET", "/v1/memories/search", params={
            "q": "benchmark", "namespace": "eval_storage_bench", "limit": 100, "min_score": "0.0",
        })
        for r in search.get("results", []):
            try:
                _request("DELETE", f"/v1/memories/{r['id']}")
            except Exception:
                pass
    except Exception:
        pass

    # ── Save results ─────────────────────────────────────────
    full_report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "server_version": health["version"],
        "task_count": len(tasks),
        "summary": summary,
        "storage_benchmark": storage_results,
        "detailed_results": results,
    }

    report_path = os.path.join(RESULTS_DIR, "eval_report.json")
    with open(report_path, "w") as f:
        json.dump(full_report, f, indent=2)
    print(f"\n  📊 Full report saved to {report_path}")

    # ── Generate markdown summary ────────────────────────────
    md_path = os.path.join(RESULTS_DIR, "eval_summary.md")
    with open(md_path, "w") as f:
        f.write("# agentMemo Evaluation Report\n\n")
        f.write(f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n")
        f.write(f"**Server:** v{health['version']} | **Tasks:** {len(tasks)} | **Categories:** {len(set(t['category'] for t in tasks))}\n\n")

        f.write("## 1. Performance Summary (Baseline vs agentMemo)\n\n")
        f.write("| Metric | Baseline | agentMemo | Delta |\n")
        f.write("|--------|----------|------------|-------|\n")
        o = summary["overall"]
        f.write(f"| Accuracy | {o['baseline_accuracy']}% | {o['vault_accuracy']}% | **+{o['accuracy_lift']}%** |\n")
        f.write(f"| Latency P50 | {o['baseline_latency_p50_ms']:.2f}ms | {o['vault_latency_p50_ms']:.2f}ms | +{o['vault_latency_p50_ms'] - o['baseline_latency_p50_ms']:.2f}ms |\n")
        f.write(f"| Latency P95 | {o['baseline_latency_p95_ms']:.2f}ms | {o['vault_latency_p95_ms']:.2f}ms | +{o['vault_latency_p95_ms'] - o['baseline_latency_p95_ms']:.2f}ms |\n")
        f.write(f"| Avg Tokens | {o['baseline_avg_tokens']} | {o['vault_avg_tokens']} | +{o['token_overhead_pct']}% |\n")
        f.write(f"| Memory Hit@1 | N/A | {o['hit_at_1']}% | — |\n")
        f.write(f"| Memory Hit@5 | N/A | {o['hit_at_5']}% | — |\n")
        f.write(f"| Avg Top Score | N/A | {o['avg_top_score']:.4f} | — |\n\n")

        f.write("## 2. By Category\n\n")
        f.write("| Category | Baseline | Vault | Hit@1 | Search P50 |\n")
        f.write("|----------|----------|-------|-------|------------|\n")
        for cat, m in summary["by_category"].items():
            f.write(f"| {cat} | {m['baseline_accuracy']}% | {m['vault_accuracy']}% | {m['hit_at_1']}% | {m['vault_search_latency_p50_ms']:.1f}ms |\n")

        f.write("\n## 3. Cost Metrics\n\n")
        s = storage_results
        f.write(f"- **Write latency (P50/P95):** {s['write_latency_p50_ms']:.1f}ms / {s['write_latency_p95_ms']:.1f}ms\n")
        f.write(f"- **Search latency (P50/P95):** {s['search_latency_p50_ms']:.1f}ms / {s['search_latency_p95_ms']:.1f}ms\n")
        f.write(f"- **Storage per memory:** ~{s['storage_per_memory_bytes']:.0f} bytes\n")
        f.write(f"- **HNSW index vectors:** {s['total_hnsw_vectors']}\n")
        f.write(f"- **Embedding cache hit rate:** {s['cache_hit_rate_pct']}%\n")
        f.write(f"- **Token overhead:** +{o['token_overhead_pct']}% (memory retrieval augments context)\n")

    print(f"  📝 Markdown summary saved to {md_path}")
    print("\n✅ Evaluation complete.")
    return full_report


if __name__ == "__main__":
    main()
