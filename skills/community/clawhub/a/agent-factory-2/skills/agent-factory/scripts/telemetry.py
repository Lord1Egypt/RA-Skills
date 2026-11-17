#!/usr/bin/env python3
"""
Telemetry Engine for OpenClaw Agent Factory.
Logs tasks, tracks token cost, latency, errors, and identifies specialization candidates.
"""

import json
import os
import time
import math
from typing import List, Dict, Any, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LOGS_FILE = os.path.join(DATA_DIR, "task_telemetry.jsonl")


def init_storage():
    os.makedirs(DATA_DIR, exist_ok=True)


from semantic_cache import get_embedding


def log_task(
    task_id: str,
    prompt: str,
    domain_tag: str,
    tokens_in: int,
    tokens_out: int,
    latency_ms: float,
    error_occurred: bool,
    human_corrected: bool,
    tools_used: List[str]
):
    """Logs a real executed task with accurate performance metrics."""
    init_storage()
    entry = {
        "timestamp": time.time(),
        "task_id": task_id,
        "prompt": prompt,
        "domain_tag": domain_tag,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "total_tokens": tokens_in + tokens_out,
        "latency_ms": latency_ms,
        "error_occurred": error_occurred,
        "human_corrected": human_corrected,
        "tools_used": tools_used,
        "embedding": get_embedding(prompt)
    }
    with open(LOGS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def analyze_clusters(
    min_occurrences: int = 5,
    cost_weight: float = 0.4,
    latency_weight: float = 0.3,
    error_weight: float = 0.3,
    threshold: float = 50.0
) -> List[Dict[str, Any]]:
    """
    Analyzes telemetry logs from real tasks, groups by domain tag/cluster,
    and returns clusters meeting the specialization score threshold.
    """
    if not os.path.exists(LOGS_FILE):
        return []

    clusters: Dict[str, List[Dict[str, Any]]] = {}
    with open(LOGS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                tag = item.get("domain_tag", "general")
                clusters.setdefault(tag, []).append(item)

    candidates = []
    for tag, tasks in clusters.items():
        count = len(tasks)
        if count < min_occurrences:
            continue

        avg_tokens = sum(t["total_tokens"] for t in tasks) / count
        avg_latency = sum(t["latency_ms"] for t in tasks) / count
        error_rate = sum(1 for t in tasks if t["error_occurred"] or t["human_corrected"]) / count

        # Normalized score
        token_cost_score = min(avg_tokens / 100.0, 100.0)
        latency_score = min(avg_latency / 50.0, 100.0)
        error_score = error_rate * 100.0

        composite_score = count * (
            cost_weight * token_cost_score +
            latency_weight * latency_score +
            error_weight * error_score
        )

        all_tools = set()
        for t in tasks:
            all_tools.update(t.get("tools_used", []))

        candidates.append({
            "domain_tag": tag,
            "occurrences": count,
            "avg_tokens": round(avg_tokens, 1),
            "avg_latency_ms": round(avg_latency, 1),
            "error_rate": round(error_rate, 2),
            "composite_score": round(composite_score, 2),
            "eligible": composite_score >= threshold,
            "recommended_tools": list(all_tools),
            "recent_tasks": tasks[-min_occurrences:]
        })

    return sorted(candidates, key=lambda x: x["composite_score"], reverse=True)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Telemetry Engine")
    parser.add_argument("--analyze", action="store_true", help="Analyze clusters for specialization")
    args = parser.parse_args()

    init_storage()
    results = analyze_clusters()
    if not results:
        print("ℹ️ No clusters found in real telemetry logs. Process real tasks to generate telemetry.")
    else:
        print("\n📊 --- Telemetry Workload Cluster Report ---")
        for res in results:
            status = "🚨 ELIGIBLE FOR SPECIALIZATION" if res["eligible"] else "⏳ Monitoring"
            print(f"- Domain: {res['domain_tag']} | Occurrences: {res['occurrences']} | Score: {res['composite_score']} -> {status}")
            print(f"  Recommended Tools: {res['recommended_tools']} | Error Rate: {res['error_rate']*100}% | Avg Latency: {res['avg_latency_ms']}ms")
