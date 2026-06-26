#!/usr/bin/env python3
"""
amber_bench.py — LongMemEval benchmark adapter for amber-hunter.

Usage:
    python3 amber_bench.py [--limit N] [--top-k K]

Downloads LongMemEval dataset (if not present), ingests each session as a capsule,
then runs recall queries and computes Recall@K.
"""

import json
import os
import sys
import time
import math
import argparse
from pathlib import Path

# Config
AMBER_URL = "http://localhost:18998"
AMBER_TOKEN = None  # fetched dynamically
DATA_PATH = Path("/tmp/longmemeval-data/longmemeval_s_cleaned.json")


def get_token():
    global AMBER_TOKEN
    import urllib.request
    req = urllib.request.urlopen(f"{AMBER_URL}/token", timeout=5)
    AMBER_TOKEN = json.loads(req.read())["api_key"]


def ingest_capsule(memo: str, content: str, tags: str) -> str:
    """Ingest one capsule, return its ID."""
    import urllib.request, urllib.parse

    data = json.dumps({
        "memo": memo,
        "content": content,
        "tags": tags
    }).encode()

    req = urllib.request.Request(
        f"{AMBER_URL}/capsules",
        data=data,
        headers={
            "Authorization": f"Bearer {AMBER_TOKEN}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    return result["id"]


def clear_all_capsules():
    """Delete all existing capsules (fresh start)."""
    import urllib.request

    req = urllib.request.Request(
        f"{AMBER_URL}/capsules",
        headers={"Authorization": f"Bearer {AMBER_TOKEN}"},
        method="GET"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            capsules = data.get("capsules", [])
            for c in capsules:
                del_req = urllib.request.Request(
                    f"{AMBER_URL}/capsules/{c['id']}",
                    headers={"Authorization": f"Bearer {AMBER_TOKEN}"},
                    method="DELETE"
                )
                try:
                    urllib.request.urlopen(del_req, timeout=5)
                except Exception:
                    pass
    except Exception:
        pass


def recall(query: str, limit: int = 50) -> list[str]:
    """Query recall, return list of capsule IDs (most relevant first)."""
    import urllib.request, urllib.parse

    url = f"{AMBER_URL}/recall?q={urllib.parse.quote(query)}&limit={limit}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {AMBER_TOKEN}"},
        method="GET"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return [m["id"] for m in data.get("memories", [])]


def id_to_capsule_id(session_id: str, capsule_map: dict) -> str:
    """Map session_id (stored in tags) back to capsule ID."""
    return capsule_map.get(session_id, "")


def download_dataset():
    """Download LongMemEval dataset if not present. Uses curl for reliability."""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    if DATA_PATH.exists():
        print(f"Dataset already at {DATA_PATH}")
        return

    print("Downloading LongMemEval dataset (~300MB via curl)...")
    import subprocess

    url = "https://hf-mirror.com/datasets/xiaowu0162/longmemeval-cleaned/resolve/main/longmemeval_s_cleaned.json"
    result = subprocess.run(
        ["curl", "-fsSL", "-o", str(DATA_PATH), url],
        timeout=300, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Download failed: {result.stderr}")
        raise RuntimeError(f"curl download failed: {result.stderr}")
    print(f"Downloaded to {DATA_PATH}")


def load_dataset(limit=None):
    """Load LongMemEval JSON, return list of entries."""
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        entries = data
    elif isinstance(data, dict) and "data" in data:
        entries = data["data"]
    else:
        raise ValueError(f"Unknown dataset format: {type(data)}")

    if limit:
        entries = entries[:limit]
    return entries


def extract_correct_session_ids(entry):
    """Extract ground truth session IDs from a LongMemEval entry.
    
    The correct sessions are listed in 'answer_session_ids'.
    These are the session IDs that contain the answer to the question.
    """
    return entry.get("answer_session_ids", [])


def build_corpus_map(entry, capsule_map: dict):
    """Build mapping from session_id to capsule_id for this entry's haystack."""
    # Each session gets encoded with its session_id as a tag
    return capsule_map


def recall_at_k(ranked_ids, correct_ids, k):
    """Compute Recall@K — whether any correct ID appears in top-k."""
    top_k = set(ranked_ids[:k])
    return float(any(cid in top_k for cid in correct_ids))


def ndcg_at_k(ranked_ids, correct_ids, k):
    """Compute NDCG@K."""
    relevances = [1.0 if cid in correct_ids else 0.0 for cid in ranked_ids[:k]]
    ideal = sorted(relevances, reverse=True)
    dcg = sum(rel / math.log2(i + 2) for i, rel in enumerate(relevances))
    idcg = sum(1.0 / math.log2(i + 2) for i in range(min(len(correct_ids), k)))
    if idcg == 0:
        return 0.0
    return dcg / idcg


def run_benchmark(limit=None, top_k=10):
    """Main benchmark loop."""
    print(f"\n{'='*60}")
    print(f"Amber-Hunter × LongMemEval Benchmark")
    print(f"  limit={limit or 'all'}, top_k={top_k}")
    print(f"{'='*60}\n")

    # Setup
    get_token()
    download_dataset()
    entries = load_dataset(limit=limit)
    print(f"Loaded {len(entries)} benchmark entries\n")

    # Clear existing capsules for clean slate
    print("Clearing existing capsules...")
    clear_all_capsules()
    print("Done.\n")

    # Phase 1: Ingest all haystack sessions as capsules
    print("Phase 1: Ingesting haystack sessions as capsules...")
    capsule_map = {}  # session_id -> capsule_id
    session_texts = {}  # session_id -> user_turns_text

    total_sessions = 0
    for entry in entries:
        for sess_id, session in zip(
            entry["haystack_session_ids"],
            entry["haystack_sessions"]
        ):
            user_turns = [t["content"] for t in session if t.get("role") == "user"]
            if not user_turns:
                continue
            text = "\n".join(user_turns)
            session_texts[sess_id] = text

            try:
                cid = ingest_capsule(
                    memo=f"[benchmark:{sess_id}]",
                    content=text,
                    tags=f"benchmark,session_id:{sess_id}"
                )
                capsule_map[sess_id] = cid
                total_sessions += 1
            except Exception as e:
                print(f"  Warning: failed to ingest {sess_id}: {e}")

        # Progress indicator
        entry_idx = entries.index(entry) + 1
        if entry_idx % 20 == 0:
            print(f"  Ingested {total_sessions} sessions so far...")

    print(f"  Total: {total_sessions} sessions ingested as capsules.\n")

    # Phase 2: Query each entry and score
    print("Phase 2: Running recall queries...")
    recall_scores = []
    ndcg_scores = []

    for i, entry in enumerate(entries):
        question = entry["question"]
        correct_sids = entry.get("correct_session_ids", entry.get("haystack_session_ids", []))

        # Get capsule IDs for correct sessions
        correct_capsule_ids = [
            capsule_map[sid] for sid in correct_sids
            if sid in capsule_map
        ]

        # Recall query
        try:
            recalled_ids = recall(question, limit=top_k)
        except Exception as e:
            print(f"  Warning: recall failed for entry {i}: {e}")
            recalled_ids = []

        # Score
        r_at_k = recall_at_k(recalled_ids, correct_capsule_ids, top_k)
        ndcg = ndcg_at_k(recalled_ids, correct_capsule_ids, top_k)
        recall_scores.append(r_at_k)
        ndcg_scores.append(ndcg)

        if (i + 1) % 50 == 0:
            print(f"  Queried {i+1}/{len(entries)} entries...")

    # Results
    avg_recall = sum(recall_scores) / len(recall_scores)
    avg_ndcg = sum(ndcg_scores) / len(ndcg_scores)

    print(f"\n{'='*60}")
    print(f"RESULTS (Recall@{top_k})")
    print(f"{'='*60}")
    print(f"  Entries:        {len(entries)}")
    print(f"  Recall@{top_k}: {avg_recall:.3f} ({avg_recall*100:.1f}%)")
    print(f"  NDCG@{top_k}:   {avg_ndcg:.3f}")
    print(f"  Sessions:       {total_sessions}")
    print(f"\nComparison (MemPalace baseline):")
    print(f"  MemPalace raw:   Recall@5 = 0.966")
    print(f"  MemPalace raw:   Recall@10 = 0.982")
    print(f"  Amber-Hunter:    Recall@{top_k} = {avg_recall:.3f}")

    return {
        "recall": avg_recall,
        "ndcg": avg_ndcg,
        "entries": len(entries),
        "sessions": total_sessions
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Amber-Hunter LongMemEval Benchmark")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of entries")
    parser.add_argument("--top-k", type=int, default=10, help="Top-K for Recall@K")
    args = parser.parse_args()

    run_benchmark(limit=args.limit, top_k=args.top_k)
