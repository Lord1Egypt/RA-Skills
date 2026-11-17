#!/usr/bin/env python3
"""
Streaming Clustering Engine for OpenClaw Agent Factory.
Clusters unstructured tasks dynamically based on vector distances
to discover candidates for sub-agent specialization without predefined tags.
"""

import json
import os
import math
from typing import List, Dict, Any, Tuple
from semantic_cache import get_embedding, _cosine_similarity

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LOGS_FILE = os.path.join(DATA_DIR, "task_telemetry.jsonl")
CLUSTERS_FILE = os.path.join(DATA_DIR, "discovered_clusters.json")


def discover_clusters(similarity_threshold: float = 0.82, min_cluster_size: int = 4) -> List[Dict[str, Any]]:
    """
    Performs leader-follower single-pass streaming clustering over telemetry logs.
    Groups semantically similar tasks into emerging cluster centroids.
    """
    if not os.path.exists(LOGS_FILE):
        return []

    tasks = []
    with open(LOGS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                item["embedding"] = get_embedding(item["prompt"])
                tasks.append(item)

    clusters: List[Dict[str, Any]] = []

    for task in tasks:
        vec = task["embedding"]
        assigned = False

        for c in clusters:
            sim = _cosine_similarity(vec, c["centroid"])
            if sim >= similarity_threshold:
                c["tasks"].append(task)
                # Update moving centroid
                n = len(c["tasks"])
                c["centroid"] = [(c["centroid"][i] * (n - 1) + vec[i]) / n for i in range(len(vec))]
                assigned = True
                break

        if not assigned:
            clusters.append({
                "cluster_id": f"cluster_{len(clusters)+1:03d}",
                "centroid": vec,
                "tasks": [task]
            })

    # Filter and enrich valid clusters
    discovered = []
    for c in clusters:
        size = len(c["tasks"])
        if size >= min_cluster_size:
            total_tokens = sum(t.get("total_tokens", 0) for t in c["tasks"])
            avg_latency = sum(t.get("latency_ms", 0) for t in c["tasks"]) / size
            errors = sum(1 for t in c["tasks"] if t.get("error_occurred") or t.get("human_corrected"))

            # Derive domain name from top keyword
            words = {}
            for t in c["tasks"]:
                for w in t["prompt"].lower().split():
                    if len(w) > 3 and w not in ["this", "from", "with", "please", "extract", "summarize"]:
                        words[w] = words.get(w, 0) + 1
            top_keyword = max(words, key=words.get) if words else f"domain_{c['cluster_id']}"

            discovered.append({
                "cluster_id": c["cluster_id"],
                "inferred_domain": top_keyword,
                "task_count": size,
                "centroid": [round(x, 4) for x in c["centroid"]],
                "avg_tokens": round(total_tokens / size, 1),
                "avg_latency_ms": round(avg_latency, 1),
                "error_rate": round(errors / size, 2),
                "sample_prompts": [t["prompt"] for t in c["tasks"][:3]]
            })

    with open(CLUSTERS_FILE, "w", encoding="utf-8") as f:
        json.dump(discovered, f, indent=2)

    return discovered


if __name__ == "__main__":
    discovered = discover_clusters(min_cluster_size=2)
    print("\n🔍 --- Automated Unsupervised Cluster Discovery ---")
    for d in discovered:
        print(f"📦 [{d['cluster_id']}] Inferred Domain: '{d['inferred_domain']}' (Tasks: {d['task_count']}, Errors: {d['error_rate']*100}%)")
        print(f"   Samples: {d['sample_prompts']}")
