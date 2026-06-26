#!/usr/bin/env python3
"""Semantic deduplication against existing long-term memories."""
import argparse
import json
import math
import logging
from pathlib import Path
from typing import Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from config_loader import load_config
from blayer_client import get_client
from log_utils import get_logger

logger = get_logger("dreaming-optimizer.deduplicate")

# ─────────────────────────────────────────────────────────────────────────────
# Stop Words (minimal, for Chinese + English)
# ─────────────────────────────────────────────────────────────────────────────

STOP_WORDS = {
    # Chinese
    "的", "了", "是", "在", "我", "有", "和", "就", "不", "人", "都", "一",
    "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有",
    "看", "好", "自己", "这", "那", "它", "他", "她", "们", "这个", "那个",
    # English
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "need", "to", "of",
    "in", "for", "on", "with", "at", "by", "from", "as", "into", "through",
}

# ─────────────────────────────────────────────────────────────────────────────
# Similarity Functions
# ─────────────────────────────────────────────────────────────────────────────

def normalize_text(text: str) -> list[str]:
    """Normalize text for similarity comparison.
    
    - Lowercase
    - Strip punctuation
    - Split on whitespace
    - Remove stop words
    
    Args:
        text: Input text
        
    Returns:
        List of normalized tokens
    """
    # Lowercase and strip
    text = text.lower()
    
    # Remove punctuation (keep Chinese characters and alphanumerics)
    import re
    text = re.sub(r"[^\w\s\u4e00-\u9fff]", " ", text)
    
    # Split on whitespace
    tokens = text.split()
    
    # Remove stop words and very short tokens
    tokens = [t for t in tokens if t not in STOP_WORDS and len(t) >= 2]
    
    return tokens


def token_similarity(a: str, b: str) -> float:
    """Compute token-overlap similarity between two texts.
    
    Uses Jaccard similarity combined with overlap coefficient.
    
    Args:
        a: First text string
        b: Second text string
        
    Returns:
        float: Similarity score 0.0-1.0
    """
    if not a or not b:
        return 0.0
    
    tokens_a = set(normalize_text(a))
    tokens_b = set(normalize_text(b))
    
    if not tokens_a or not tokens_b:
        return 0.0
    
    # Jaccard similarity
    intersection = len(tokens_a & tokens_b)
    union = len(tokens_a | tokens_b)
    jaccard = intersection / union if union > 0 else 0.0
    
    # Overlap coefficient (Szymkiewicz–Simpson)
    overlap = intersection / min(len(tokens_a), len(tokens_b)) if min(len(tokens_a), len(tokens_b)) > 0 else 0.0
    
    # Weighted combination: favor higher overlap
    similarity = 0.4 * jaccard + 0.6 * overlap
    
    return round(similarity, 4)


def embedding_similarity(a: str, b: str, model_name: str = None) -> float:
    """Compute semantic similarity via embeddings (Pro feature, v1.1).
    
    Requires: sentence-transformers
    
    Args:
        a: First text string
        b: Second text string
        model_name: HuggingFace model name
        
    Returns:
        float: Cosine similarity -1.0 to 1.0 (0.0 if model unavailable)
    """
    # TODO (Pro v1.1): Implement with sentence-transformers
    # from sentence_transformers import SentenceTransformer
    # model = SentenceTransformer(model_name or "paraphrase-multilingual-MiniLM-L12-v2")
    # embeddings = model.encode([a, b])
    # return float(cosine_similarity(embeddings[0], embeddings[1]))
    logger.debug("Embedding similarity not yet implemented (Pro v1.1)")
    return 0.0


def batch_similarities(
    candidate: str,
    existing: list[str],
    use_embeddings: bool = False,
) -> list[float]:
    """Compute similarities between a candidate and multiple existing texts.
    
    Args:
        candidate: Text to check
        existing: List of existing texts to compare against
        use_embeddings: Use embedding similarity (Pro)
        
    Returns:
        List of similarity scores (same order as existing)
    """
    if use_embeddings:
        # TODO (Pro v1.1): Batch embedding comparison
        return [embedding_similarity(candidate, e) for e in existing]
    
    return [token_similarity(candidate, e) for e in existing]


# ─────────────────────────────────────────────────────────────────────────────
# Deduplication Logic
# ─────────────────────────────────────────────────────────────────────────────

def get_blayer_memories(
    db_path: Path = None,
    limit: int = 1000,
    min_score: int = 0,
) -> list[dict]:
    """Read existing B-layer memories.
    
    Args:
        db_path: Path to SQLite DB (default: from blayer_client)
        limit: Maximum number of memories to retrieve (default: 1000)
        min_score: Only return memories with score >= min_score
        
    Returns:
        List of dicts: [{"id": int, "content": str, "score": int, "tag": str}, ...]
    """
    client = get_client()
    memories = client.get_memories(limit=limit, min_score=min_score)
    
    # Return only the fields we need for dedup
    return [
        {"id": m["id"], "content": m["content"], "score": m["score"], "tag": m["tag"]}
        for m in memories
    ]


def deduplicate_entries(
    entries: list[dict],
    blayer_memories: list[dict] = None,
    threshold: float = 0.85,
    use_embeddings: bool = False,
    check_blayer_limit: int = 1000,
    min_blayer_score: int = 0,
) -> dict:
    """Remove near-duplicate entries based on similarity threshold.
    
    Args:
        entries: List of entry dicts with "content_preview" or "content" key
        blayer_memories: Existing B-layer memories to check against.
                        If None, fetches from B-layer.
        threshold: Similarity threshold 0.0-1.0 (default: 0.85)
        use_embeddings: Use embedding similarity (Pro, v1.1)
        check_blayer_limit: Max existing memories to compare against
        min_blayer_score: Minimum score of B-layer entries to compare
        
    Returns:
        dict: {
            "unique": list[dict],     # Entries to commit
            "merged": list[dict],    # Entries merged into existing
            "merged_into": dict,     # Map of merged_id → existing_id
            "stats": {
                "total_input": int,
                "unique_count": int,
                "merged_count": int,
                "avg_similarity": float,
                "max_similarity_seen": float,
            }
        }
    """
    # Fetch B-layer memories if not provided
    if blayer_memories is None:
        blayer_memories = get_blayer_memories(limit=check_blayer_limit, min_score=min_blayer_score)
    
    if not blayer_memories:
        logger.info("B-layer is empty, all entries are unique")
        return {
            "unique": entries,
            "merged": [],
            "merged_into": {},
            "stats": {
                "total_input": len(entries),
                "unique_count": len(entries),
                "merged_count": 0,
                "avg_similarity": 0.0,
                "max_similarity_seen": 0.0,
            }
        }
    
    # Build existing content list for fast comparison
    existing_contents = [m["content"] for m in blayer_memories]
    existing_ids = [m["id"] for m in blayer_memories]
    
    unique = []
    merged = []
    merged_into = {}
    similarities = []
    
    for entry in entries:
        content = entry.get("content_preview") or entry.get("content", "")
        
        # Compute similarities against all existing memories
        entry_sims = batch_similarities(content, existing_contents, use_embeddings)
        
        max_sim = max(entry_sims) if entry_sims else 0.0
        max_idx = entry_sims.index(max_sim) if entry_sims else -1
        
        similarities.append(max_sim)
        
        if max_sim >= threshold:
            # Merge into existing memory
            target_id = existing_ids[max_idx]
            merged.append(entry)
            merged_into[id(entry)] = target_id
            
            # Update the entry with merge info
            entry["is_merged"] = True
            entry["merged_into_id"] = target_id
            entry["similarity_score"] = max_sim
        else:
            unique.append(entry)
    
    avg_sim = sum(similarities) / len(similarities) if similarities else 0.0
    max_sim_seen = max(similarities) if similarities else 0.0
    
    logger.info(
        f"Dedup: {len(unique)} unique, {len(merged)} merged "
        f"(avg_sim={avg_sim:.3f}, max_sim={max_sim_seen:.3f})"
    )
    
    return {
        "unique": unique,
        "merged": merged,
        "merged_into": merged_into,
        "stats": {
            "total_input": len(entries),
            "unique_count": len(unique),
            "merged_count": len(merged),
            "avg_similarity": round(avg_sim, 4),
            "max_similarity_seen": round(max_sim_seen, 4),
        }
    }


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deduplicate memory entries against B-layer"
    )
    parser.add_argument(
        "--threshold", type=float, default=0.85,
        help="Similarity threshold (default: 0.85)"
    )
    parser.add_argument(
        "--no-embeddings", action="store_true",
        help="Disable embedding-based similarity"
    )
    parser.add_argument(
        "--input-json", type=Path, default=None,
        help="Read entries from JSON file (instead of stdin)"
    )
    parser.add_argument(
        "--output-json", type=Path, default=None,
        help="Write results to JSON file"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable verbose logging"
    )
    args = parser.parse_args()
    
    if args.verbose:
        import logging
        logger.setLevel(logging.DEBUG)
    
    # Load entries from input
    if args.input_json:
        entries = json.loads(args.input_json.read_text(encoding="utf-8"))
    else:
        # Read from stdin
        import sys
        input_data = sys.stdin.read()
        entries = json.loads(input_data) if input_data.strip() else []
    
    result = deduplicate_entries(
        entries,
        threshold=args.threshold,
        use_embeddings=not args.no_embeddings,
    )
    
    print(
        f"[deduplicate] Unique: {result['stats']['unique_count']}, "
        f"Merged: {result['stats']['merged_count']}, "
        f"Avg similarity: {result['stats']['avg_similarity']:.3f}"
    )
    
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"[deduplicate] Written to {args.output_json}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
