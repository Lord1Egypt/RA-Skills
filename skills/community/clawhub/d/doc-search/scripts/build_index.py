#!/usr/bin/env python3
"""
Build BM25 inverted index for document library (增量构建文档倒排索引)

Index is stored at <docs_dir>/.cache/index.json by default.

Usage:
    build_index.py <docs_dir> [--index <index_file>] [--ext md,txt,rst]

Examples:
    build_index.py ~/obsidian
    build_index.py ~/docs --ext md,txt
    build_index.py ~/docs --index /custom/path/index.json
"""

import sys
import os
import json
import math
import re
import hashlib
import time
from pathlib import Path
from collections import defaultdict

DEFAULT_EXTS = {"md", "txt", "rst", "org"}

# BM25 params
K1 = 1.5
B = 0.75


def bigrams(text):
    """Extract CJK bigrams + latin words (提取中文bigram和英文词)"""
    tokens = set()
    # Latin words (case-insensitive)
    for w in re.findall(r'[a-zA-Z0-9_\-\.]+', text):
        tokens.add(w.lower())
    # CJK bigrams
    cjk = re.findall(r'[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]', text)
    for i in range(len(cjk) - 1):
        tokens.add(cjk[i] + cjk[i+1])
    # CJK trigrams for better recall
    for i in range(len(cjk) - 2):
        tokens.add(cjk[i] + cjk[i+1] + cjk[i+2])
    return tokens


def file_hash(path):
    """Quick hash using mtime+size (快速文件指纹)"""
    st = os.stat(path)
    return f"{st.st_mtime:.0f}:{st.st_size}"


def extract_title(content, path):
    """Extract first heading or filename as title (提取标题)"""
    for line in content.splitlines()[:10]:
        line = line.strip()
        if line.startswith('#'):
            return line.lstrip('#').strip()
        if line:
            return line[:80]
    return Path(path).stem


def extract_summary(content, max_chars=200):
    """Extract first meaningful paragraph (提取摘要)"""
    lines = [l.strip() for l in content.splitlines() if l.strip() and not l.startswith('#')]
    return ' '.join(lines)[:max_chars]


def tokenize_file(path, content):
    """Tokenize file content, return (tokens_set, tf_dict) (分词)"""
    tokens = bigrams(content)
    # TF: count occurrences
    tf = defaultdict(int)
    # Latin
    for w in re.findall(r'[a-zA-Z0-9_\-\.]+', content):
        tf[w.lower()] += 1
    # CJK bigrams
    cjk = re.findall(r'[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]', content)
    for i in range(len(cjk) - 1):
        tf[cjk[i] + cjk[i+1]] += 1
    for i in range(len(cjk) - 2):
        tf[cjk[i] + cjk[i+1] + cjk[i+2]] += 1
    return tokens, dict(tf)


def build_index(docs_dir, index_file, exts):
    docs_dir = Path(docs_dir).expanduser().resolve()
    index_file = Path(index_file).expanduser()
    index_file.parent.mkdir(parents=True, exist_ok=True)

    # Load existing index (加载已有索引)
    existing = {}
    if index_file.exists():
        try:
            with open(index_file) as f:
                existing = json.load(f)
        except Exception:
            existing = {}

    meta = existing.get("meta", {})       # path -> {hash, title, summary, length}
    inv = existing.get("inv", {})         # token -> {path: tf}
    doc_lengths = existing.get("doc_lengths", {})  # path -> token count

    # Scan files (扫描文件)
    all_files = []
    for ext in exts:
        all_files.extend(docs_dir.rglob(f"*.{ext}"))

    current_paths = set()
    changed = 0
    skipped = 0

    for fpath in all_files:
        rel = str(fpath.relative_to(docs_dir))
        current_paths.add(rel)
        fhash = file_hash(fpath)

        if rel in meta and meta[rel].get("hash") == fhash:
            skipped += 1
            continue

        # Read and index (读取并索引)
        try:
            content = fpath.read_text(errors='ignore')
        except Exception as e:
            print(f"  skip {rel}: {e}", file=sys.stderr)
            continue

        tokens, tf = tokenize_file(rel, content)
        title = extract_title(content, fpath)
        summary = extract_summary(content)

        # Remove old entries for this file (删除旧索引条目)
        if rel in meta:
            for token in list(inv.keys()):
                if rel in inv[token]:
                    del inv[token][rel]
                    if not inv[token]:
                        del inv[token]

        # Add new entries (添加新索引条目)
        for token, count in tf.items():
            if token not in inv:
                inv[token] = {}
            inv[token][rel] = count

        doc_lengths[rel] = sum(tf.values())
        meta[rel] = {
            "hash": fhash,
            "title": title,
            "summary": summary,
            "path": str(fpath),
        }
        changed += 1

    # Remove deleted files (删除已删除文件的索引)
    removed = set(meta.keys()) - current_paths
    for rel in removed:
        del meta[rel]
        if rel in doc_lengths:
            del doc_lengths[rel]
        for token in list(inv.keys()):
            if rel in inv[token]:
                del inv[token][rel]
                if not inv[token]:
                    del inv[token]

    # Save index (保存索引)
    index_data = {
        "meta": meta,
        "inv": inv,
        "doc_lengths": doc_lengths,
        "total_docs": len(meta),
        "avg_length": sum(doc_lengths.values()) / max(len(doc_lengths), 1),
        "built_at": time.time(),
    }
    with open(index_file, 'w') as f:
        json.dump(index_data, f, ensure_ascii=False, separators=(',', ':'))

    print(f"Index built: {len(meta)} docs, {changed} updated, {len(removed)} removed, {skipped} unchanged")
    print(f"Index: {index_file} ({index_file.stat().st_size // 1024}KB)")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    docs_dir = sys.argv[1]
    index_file = None  # derived from docs_dir below
    exts = DEFAULT_EXTS

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--index' and i + 1 < len(sys.argv):
            index_file = sys.argv[i+1]; i += 2
        elif sys.argv[i] == '--ext' and i + 1 < len(sys.argv):
            exts = set(sys.argv[i+1].split(',')); i += 2
        else:
            i += 1

    if index_file is None:
        index_file = str(Path(docs_dir).expanduser().resolve() / ".cache" / "index.json")

    build_index(docs_dir, index_file, exts)


if __name__ == "__main__":
    main()
