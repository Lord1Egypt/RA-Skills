#!/usr/bin/env python3
"""
fragments_search.py — Client-side semantic reranker for Memos search results.

Usage:
  python3 fragments_search.py --query "intent" --candidates '<json_array>'
  echo '<json_array>' | python3 fragments_search.py --query "intent" --stdin

Requires: numpy
"""

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from typing import Any, Dict, List, Tuple

try:
    import numpy as np
except ImportError:
    print(json.dumps({"ok": False, "error": "numpy is required. Install: pip install numpy"}))
    sys.exit(1)


def tokenize_text(text: str) -> List[str]:
    """Multilingual tokenizer: Latin words + CJK bigrams."""
    if not text:
        return []
    lowered = text.lower()
    tokens = re.findall(r"[a-z0-9]+", lowered)
    for chunk in re.findall(r"[\u4e00-\u9fff]+", lowered):
        if len(chunk) == 1:
            tokens.append(chunk)
            continue
        tokens.extend(chunk[i : i + 2] for i in range(len(chunk) - 1))
    return tokens


def memo_text_for_ranking(memo: Dict[str, Any]) -> str:
    parts = [memo.get("content") or "", memo.get("snippet") or "", " ".join(memo.get("tags") or [])]
    return "\n".join([p for p in parts if p])


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(np.dot(a, b) / (na * nb)) if na and nb else 0.0


def build_tfidf_space(
    doc_tokens: List[List[str]], query_tokens: List[str], max_terms: int = 5000
) -> Tuple[np.ndarray, np.ndarray]:
    doc_count = len(doc_tokens)
    if doc_count == 0:
        return np.zeros((0, 0)), np.zeros((0,))

    df: Dict[str, int] = defaultdict(int)
    tf_total: Dict[str, int] = defaultdict(int)
    for tokens in doc_tokens:
        counts = Counter(tokens)
        for term, cnt in counts.items():
            tf_total[term] += cnt
        for term in counts:
            df[term] += 1

    seen = set()
    vocab_terms = []
    for t in query_tokens:
        if t not in seen and t in df:
            seen.add(t)
            vocab_terms.append(t)
    for t in sorted(df, key=lambda x: (df[x], tf_total[x]), reverse=True):
        if t not in seen:
            seen.add(t)
            vocab_terms.append(t)
        if len(vocab_terms) >= max_terms:
            break

    vocab = {t: i for i, t in enumerate(vocab_terms)}
    n = len(vocab)
    idf = np.array([math.log((doc_count + 1) / (df.get(t, 0) + 1)) + 1.0 for t in vocab_terms])

    matrix = np.zeros((doc_count, n))
    for r, tokens in enumerate(doc_tokens):
        for term, cnt in Counter(tokens).items():
            c = vocab.get(term)
            if c is not None:
                matrix[r, c] = (1.0 + math.log(cnt)) * idf[c]

    qv = np.zeros(n)
    for term, cnt in Counter(query_tokens).items():
        c = vocab.get(term)
        if c is not None:
            qv[c] = (1.0 + math.log(cnt)) * idf[c]

    return matrix, qv


def build_excerpt(content: str, query_tokens: List[str], max_chars: int = 420) -> str:
    if not content:
        return ""
    cl = content.lower()
    positions = [cl.find(t) for t in query_tokens if len(t) >= 2 and cl.find(t) >= 0]
    start = max(0, min(positions) - 120) if positions else 0
    end = min(len(content), start + max_chars)
    excerpt = content[start:end].strip()
    return ("..." if start else "") + excerpt + ("..." if end < len(content) else "")


def memo_title(content: str, fallback: str) -> str:
    for line in content.splitlines():
        s = line.strip()
        if s:
            return s[:120]
    return fallback


def rank(query: str, memos: List[Dict], top_k: int = 8, min_score: float = 0.15, dims: int = 24) -> List[Dict]:
    qt = tokenize_text(query)
    if not qt or not memos:
        return []

    texts = [memo_text_for_ranking(m) for m in memos]
    doc_tokens = [tokenize_text(t) for t in texts]
    matrix, qv = build_tfidf_space(doc_tokens, qt)
    if matrix.size == 0:
        return []

    lex = [cosine_similarity(qv, matrix[i]) for i in range(matrix.shape[0])]
    sem = list(lex)

    n_d, n_t = matrix.shape
    k = min(dims, n_d - 1, n_t - 1)
    if k >= 1:
        try:
            _, _, vt = np.linalg.svd(matrix, full_matrices=False)
            basis = vt[:k].T
            sem = [cosine_similarity(qv @ basis, (matrix @ basis)[i]) for i in range(n_d)]
        except np.linalg.LinAlgError:
            pass

    qset = set(qt)
    results = []
    for i, m in enumerate(memos):
        dset = set(doc_tokens[i])
        cov = len(qset & dset) / max(len(qset), 1)
        pin = 0.02 if m.get("pinned") else 0.0
        score = sem[i] * 0.70 + lex[i] * 0.25 + cov * 0.05 + pin
        if score < min_score:
            continue
        c = m.get("content") or ""
        results.append({
            "name": m.get("name"),
            "title": memo_title(c, m.get("name", "")),
            "excerpt": build_excerpt(c, qt),
            "relevance": {"score": round(score, 4), "semantic": round(sem[i], 4), "lexical": round(lex[i], 4), "coverage": round(cov, 4)},
        })
    results.sort(key=lambda x: x["relevance"]["score"], reverse=True)
    return results[:top_k]


def main():
    parser = argparse.ArgumentParser(description="Semantic reranker for Memos search results")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--candidates", help="JSON array of memo objects")
    parser.add_argument("--stdin", action="store_true", help="Read candidates from stdin")
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--min-score", type=float, default=0.15)
    args = parser.parse_args()

    if args.stdin:
        raw = sys.stdin.read()
    elif args.candidates:
        raw = args.candidates
    else:
        print(json.dumps({"ok": False, "error": "Provide --candidates or --stdin"}))
        sys.exit(1)

    memos = json.loads(raw)
    results = rank(args.query, memos, top_k=args.top_k, min_score=args.min_score)
    print(json.dumps({"ok": True, "results": results, "total": len(results)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
