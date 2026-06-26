#!/usr/bin/env python3
"""
BM25 search over indexed document library (BM25文档检索)

Index is read from <docs_dir>/.cache/index.json by default.

Usage:
    search.py <query> --docs-dir <dir> [--index <index_file>] [--topk 5]

Examples:
    search.py "TTS音色管理" --docs-dir ~/obsidian
    search.py "voice list API" --docs-dir ~/obsidian --topk 3
    search.py "支付回调" --index /custom/path/index.json
"""

import sys
import os
import json
import math
import re
from pathlib import Path
from collections import defaultdict

K1 = 1.5
B = 0.75


def bigrams(text):
    """Same tokenizer as build_index.py (与索引构建使用相同分词)"""
    tokens = set()
    for w in re.findall(r'[a-zA-Z0-9_\-\.]+', text):
        tokens.add(w.lower())
    cjk = re.findall(r'[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]', text)
    for i in range(len(cjk) - 1):
        tokens.add(cjk[i] + cjk[i+1])
    for i in range(len(cjk) - 2):
        tokens.add(cjk[i] + cjk[i+1] + cjk[i+2])
    return tokens


def bm25_score(tf, df, doc_len, avg_len, total_docs):
    """BM25 scoring formula"""
    idf = math.log((total_docs - df + 0.5) / (df + 0.5) + 1)
    return idf * (tf * (K1 + 1)) / (tf + K1 * (1 - B + B * doc_len / avg_len))


def search(query_terms, index_data, topk=5):
    """Multi-term BM25 search, returns ranked (path, score) list"""
    inv = index_data["inv"]
    doc_lengths = index_data["doc_lengths"]
    total_docs = index_data["total_docs"]
    avg_length = index_data["avg_length"]

    scores = defaultdict(float)
    for term in query_terms:
        if term not in inv:
            continue
        postings = inv[term]
        df = len(postings)
        for doc_path, tf in postings.items():
            doc_len = doc_lengths.get(doc_path, avg_length)
            scores[doc_path] += bm25_score(tf, df, doc_len, avg_length, total_docs)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:topk]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    query = sys.argv[1]
    index_file = None
    topk = 5
    docs_dir = None

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--index' and i + 1 < len(sys.argv):
            index_file = sys.argv[i+1]; i += 2
        elif sys.argv[i] == '--topk' and i + 1 < len(sys.argv):
            topk = int(sys.argv[i+1]); i += 2
        elif sys.argv[i] == '--docs-dir' and i + 1 < len(sys.argv):
            docs_dir = sys.argv[i+1]; i += 2
        else:
            i += 1

    if index_file is None:
        if docs_dir is None:
            print("Error: provide --docs-dir <dir> or --index <file>", file=sys.stderr)
            sys.exit(1)
        index_file = str(Path(docs_dir).expanduser().resolve() / ".cache" / "index.json")

    if not Path(index_file).exists():
        print(f"Index not found: {index_file}", file=sys.stderr)
        print("Run build_index.py first.", file=sys.stderr)
        sys.exit(1)

    with open(index_file) as f:
        index_data = json.load(f)

    query_terms = bigrams(query)
    results = search(query_terms, index_data, topk)

    meta = index_data["meta"]
    output = []
    for rel_path, score in results:
        m = meta.get(rel_path, {})
        abs_path = m.get("path", rel_path)
        output.append({
            "path": abs_path,
            "rel": rel_path,
            "score": round(score, 3),
            "title": m.get("title", ""),
            "summary": m.get("summary", ""),
        })

    # Print as JSON for easy parsing by Claude (输出JSON供Claude解析)
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
