#!/usr/bin/env python3
"""
Semantic Cache Engine for OpenClaw Agent Factory.
Caches task inputs and outputs using high-similarity cosine threshold (>0.98),
allowing instantaneous 0-token deduplication.
"""

import json
import os
import time
import math
from typing import Dict, Any, Optional, List, Tuple

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CACHE_FILE = os.path.join(DATA_DIR, "semantic_cache.json")


def _init_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def _cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if len(v1) != len(v2) or not v1:
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def get_embedding(text: str) -> List[float]:
    """
    Deterministic normalized vector representation for local fast execution.
    Can be replaced seamlessly with fastembed / OpenAI embedding API.
    """
    words = text.lower().split()
    vector = [0.0] * 16
    for idx, w in enumerate(words):
        h = sum(ord(c) for c in w)
        vector[h % 16] += 1.0 / (idx + 1.0)
    norm = math.sqrt(sum(x * x for x in vector))
    if norm > 0:
        vector = [x / norm for x in vector]
    return vector


def lookup(prompt: str, threshold: float = 0.98) -> Optional[Dict[str, Any]]:
    """Checks semantic cache for near-identical queries."""
    _init_storage()
    prompt_vec = get_embedding(prompt)
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache_entries = json.load(f)

    best_match = None
    best_sim = -1.0

    for entry in cache_entries:
        sim = _cosine_similarity(prompt_vec, entry["embedding"])
        if sim > best_sim:
            best_sim = sim
            if sim >= threshold:
                best_match = entry

    if best_match:
        best_match["hit_similarity"] = round(best_sim, 4)
        return best_match
    return None


def store(prompt: str, response: Dict[str, Any], agent_id: str, ttl_seconds: int = 86400):
    """Stores a prompt-response pair in the semantic cache."""
    _init_storage()
    prompt_vec = get_embedding(prompt)
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache_entries = json.load(f)

    entry = {
        "id": f"cache_{int(time.time()*1000)}",
        "created_at": time.time(),
        "expires_at": time.time() + ttl_seconds,
        "prompt": prompt,
        "embedding": prompt_vec,
        "response": response,
        "served_by_agent": agent_id,
        "tokens_saved": response.get("tokens_used", 450)
    }

    # Prune expired entries
    now = time.time()
    cache_entries = [e for e in cache_entries if e["expires_at"] > now]
    cache_entries.append(entry)

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache_entries, f, indent=2)


def stats() -> Dict[str, Any]:
    """Returns semantic cache statistics."""
    _init_storage()
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        entries = json.load(f)
    total_tokens_saved = sum(e.get("tokens_saved", 0) for e in entries)
    return {
        "total_cached_entries": len(entries),
        "total_tokens_saved": total_tokens_saved
    }


if __name__ == "__main__":
    _init_storage()
    # Test caching
    sample_prompt = "Extract VAT and total from invoice 402"
    store(
        sample_prompt,
        {"status": "success", "data": {"vat": 20.0, "total": 120.0}, "tokens_used": 500},
        "subagent_invoice_extraction"
    )
    hit = lookup("Extract VAT and total from invoice 402")
    print("🎯 Cache Hit Test:", hit is not None, "Similarity:", hit.get("hit_similarity") if hit else None)
