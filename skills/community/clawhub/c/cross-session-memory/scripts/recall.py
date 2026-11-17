#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recall.py — 从派生索引选择性召回 top-k 事实。

用法: python recall.py <memory_dir> "词1 词2" [--k 5]
若索引缺失或 .md 比 db 新，自动重建。标准库，中文子串匹配。
"""
import argparse
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_index import build


def _need_rebuild(memory_dir, db):
    if not os.path.exists(db):
        return True
    db_mtime = os.path.getmtime(db)
    for f in os.listdir(memory_dir):
        if f.lower().endswith('.md') and f != 'MEMORY.md':
            if os.path.getmtime(os.path.join(memory_dir, f)) > db_mtime:
                return True
    return False


def search(memory_dir, query, k=5, db=None):
    db = db or os.path.join(memory_dir, 'memory.db')
    if _need_rebuild(memory_dir, db):
        build(memory_dir, db)
    conn = sqlite3.connect(db)
    terms = [t.lower() for t in query.split() if t.strip()]
    rows = conn.execute(
        'SELECT name, path, type, description, updated, body FROM facts'
    ).fetchall()
    scored = []
    for name, path, typ, desc, updated, body in rows:
        hay = (name + ' ' + desc + ' ' + body).lower()
        score = sum(1 for t in terms if t in hay)
        if terms and score == len(terms):
            scored.append((score, updated or '', name, path, typ, desc))
    # 相关度降序，同分按更新日期降序
    scored.sort(key=lambda x: x[1], reverse=True)
    scored.sort(key=lambda x: x[0], reverse=True)
    conn.close()
    return scored[:k]


def main():
    ap = argparse.ArgumentParser(description='召回相关事实')
    ap.add_argument('memory_dir', help='memory 目录路径')
    ap.add_argument('query', help='查询，多词用空格分隔（AND）')
    ap.add_argument('--k', type=int, default=5, help='返回条数')
    args = ap.parse_args()
    results = search(args.memory_dir, args.query, args.k)
    if not results:
        print('（无匹配）')
        return
    for i, (score, updated, name, path, typ, desc) in enumerate(results, 1):
        print(f'{i}. [{typ or "?"}] {name}  (updated {updated or "?"}, 相关度 {score})')
        print(f'   {desc}')
        print(f'   → {path}')


if __name__ == '__main__':
    main()
