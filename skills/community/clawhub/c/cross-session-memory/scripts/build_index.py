#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_index.py — 扫描 memory 目录，构建派生索引 memory.db。

第一层（真理源）是每个事实一个 .md；本脚本构建第二层（派生索引）。
标准库，无需 pip。中文用子串匹配，不做分词。
"""
import argparse
import os
import re
import sqlite3

FRONT_RE = re.compile(r'\A---\s*\n(.*?)\n---\s*\n?(.*)\Z', re.S)
LINK_RE = re.compile(r'\[\[([^\]]+)\]\]')


def parse_front(text):
    m = FRONT_RE.match(text)
    if not m:
        return {}, text
    fm_raw, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_raw.splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip()
    return fm, body


def build(memory_dir, db=None):
    db = db or os.path.join(memory_dir, 'memory.db')
    conn = sqlite3.connect(db)
    conn.executescript('''
DROP TABLE IF EXISTS facts;
DROP TABLE IF EXISTS links;
CREATE TABLE facts(
    name TEXT PRIMARY KEY,
    path TEXT,
    type TEXT,
    description TEXT,
    updated TEXT,
    mtime REAL,
    body TEXT
);
CREATE TABLE links(src TEXT, tgt TEXT);
''')
    files = [f for f in os.listdir(memory_dir)
             if f.lower().endswith('.md') and f != 'MEMORY.md']
    n = 0
    for f in sorted(files):
        path = os.path.join(memory_dir, f)
        with open(path, 'r', encoding='utf-8') as fh:
            text = fh.read()
        fm, body = parse_front(text)
        name = fm.get('name') or os.path.splitext(f)[0]
        desc = fm.get('description', '')
        typ = fm.get('type', '')
        updated = fm.get('updated', '')
        mtime = os.path.getmtime(path)
        conn.execute(
            'INSERT OR REPLACE INTO facts VALUES(?,?,?,?,?,?,?)',
            (name, path, typ, desc, updated, mtime, body))
        for tgt in LINK_RE.findall(body):
            conn.execute('INSERT INTO links VALUES(?,?)',
                         (name, tgt.strip()))
        n += 1
    conn.commit()
    conn.close()
    return n, db


def main():
    ap = argparse.ArgumentParser(description='构建 memory 派生索引')
    ap.add_argument('memory_dir', help='memory 目录路径')
    ap.add_argument('--db', default=None,
                    help='索引 db 路径（默认 memory 目录下 memory.db）')
    args = ap.parse_args()
    n, db = build(args.memory_dir, args.db)
    print(f'索引完成：{n} 条事实，写入 {db}')


if __name__ == '__main__':
    main()
