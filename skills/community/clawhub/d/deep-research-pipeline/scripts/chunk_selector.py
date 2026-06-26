"""Chunk Selector — LLM scores each chunk for relevance, filters by threshold.

This is the "hallucination killer": instead of feeding raw search results to the
synthesis LLM, we first have an LLM review each chunk and keep only relevant ones.

Usage:
    python chunk_selector.py --question "..." --content <json_file_or_stdin> --min-score 0.7

Input content format (JSON):
    [
        {"content": "...", "url": "...", "title": "..."},
        ...
    ]

Output: JSON array of scored chunks above threshold.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from typing import Optional

from llm_client import call_llm as _call_glm

# Max tokens per batch — avoid context overflow
MAX_BATCH_TOKENS = 8000


def _estimate_tokens(text: str) -> int:
    """Rough token estimate (1 token ≈ 4 chars)."""
    return len(text) // 4


def select_relevant_chunks(
    question: str,
    content: list[dict],
    min_score: float = 0.7,
    max_context_tokens: int = 8000,
    api_key: Optional[str] = None,
) -> list[dict]:
    """Score each chunk for relevance, return filtered list.

    Batches chunks to avoid context overflow. Each chunk gets scored 0.0-1.0.
    Only chunks >= min_score are returned, sorted by score descending.
    """

    if not content:
        return []

    # Batch chunks to fit in context
    batches = _batch_chunks(content, max_context_tokens)
    all_scored = []

    for batch in batches:
        scored = _score_batch(question, batch, api_key=api_key)
        all_scored.extend(scored)

    # Filter and sort
    filtered = [c for c in all_scored if c.get("score", 0) >= min_score]
    filtered.sort(key=lambda x: x.get("score", 0), reverse=True)

    return filtered


def _batch_chunks(chunks: list[dict], max_tokens: int) -> list[list[dict]]:
    """Split chunks into batches that fit within token limit."""
    batches = []
    current_batch = []
    current_tokens = 0

    for chunk in chunks:
        text = chunk.get("content", "")
        tokens = _estimate_tokens(text)
        if tokens > max_tokens:
            # Truncate oversized chunks
            chunk = {**chunk, "content": text[: max_tokens * 4]}
            tokens = max_tokens

        if current_tokens + tokens > max_tokens and current_batch:
            batches.append(current_batch)
            current_batch = []
            current_tokens = 0

        current_batch.append(chunk)
        current_tokens += tokens

    if current_batch:
        batches.append(current_batch)

    return batches


def _score_batch(question: str, batch: list[dict], api_key: Optional[str] = None) -> list[dict]:
    """Score a batch of chunks using LLM."""
    system = (
        "You are a research relevance scorer. Score each chunk's relevance "
        "to the research question on a scale of 0.0 to 1.0.\n\n"
        "Scoring criteria:\n"
        "- 1.0: Directly answers or is essential context for the question\n"
        "- 0.8: Highly relevant supporting information\n"
        "- 0.6: Somewhat relevant but tangential\n"
        "- 0.4: Loosely related, minor utility\n"
        "- 0.2: Barely related\n"
        "- 0.0: Completely irrelevant\n\n"
        'Output ONLY a JSON array. Each element: {"index": N, "score": 0.X, '
        '"reason": "one sentence"}. Use the same index numbers as input.'
    )

    # Build numbered list
    numbered = []
    for i, chunk in enumerate(batch):
        numbered.append(
            f"[{i}] {chunk.get('title', 'Untitled')} ({chunk.get('url', 'unknown')})\n"
            f"{chunk.get('content', '')[:2000]}"  # Truncate long chunks for prompt
        )

    prompt = (
        f"Research question: {question}\n\n"
        f"Chunks to score:\n{chr(10).join(numbered)}\n\n"
        "Score each chunk. Output JSON array only."
    )

    try:
        response = _call_glm(prompt, system, max_tokens=4096, temperature=0.1, api_key=api_key)
        response = response.strip()
        if response.startswith("```"):
            response = response.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        scores = json.loads(response)
        if not isinstance(scores, list):
            scores = [scores]

        # Merge scores back into chunks
        result = []
        for score_entry in scores:
            idx = score_entry.get("index", 0)
            if 0 <= idx < len(batch):
                merged = {**batch[idx]}
                merged["score"] = float(score_entry.get("score", 0))
                merged["relevance_reason"] = score_entry.get("reason", "")
                result.append(merged)

        # Add unscored chunks with score 0
        scored_indices = {s.get("index", 0) for s in scores}
        for i, chunk in enumerate(batch):
            if i not in scored_indices:
                merged = {**chunk, "score": 0.0, "relevance_reason": "Not scored"}
                result.append(merged)

        return result

    except Exception as e:
        # On error, return all chunks with neutral score
        print(
            f"Warning: scoring failed ({e}), returning all chunks unscored",
            file=sys.stderr,
        )
        return [
            {**c, "score": 0.5, "relevance_reason": "Scoring failed"} for c in batch
        ]


def main():
    parser = argparse.ArgumentParser(description="Score and filter chunks by relevance")
    parser.add_argument("--question", "-q", required=True, help="Research question")
    parser.add_argument("--content", "-c", help="JSON file with chunks (or stdin)")
    parser.add_argument("--min-score", "-m", type=float, default=0.7)
    parser.add_argument("--max-tokens", type=int, default=MAX_BATCH_TOKENS)
    parser.add_argument("--stdin", action="store_true", help="Read content from stdin")
    args = parser.parse_args()

    # Load content
    if args.stdin or not args.content:
        content = json.load(sys.stdin)
    else:
        with open(args.content) as f:
            content = json.load(f)

    if not isinstance(content, list):
        content = [content]

    selected = select_relevant_chunks(
        args.question, content, args.min_score, args.max_tokens
    )

    print(json.dumps(selected, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
