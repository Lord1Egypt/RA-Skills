"""Classic IR engine: FTS5 BM25 index/search/RM3/RRF (stdlib)."""
import argparse
import glob
import json
import math
import os
import re
import sqlite3

TOK = re.compile(r'[a-z0-9]+')


def tok(text):
    return TOK.findall(text.lower())


def cmd_index(a):
    if os.path.exists(a.db):
        os.remove(a.db)
    c = sqlite3.connect(a.db)
    c.execute('CREATE VIRTUAL TABLE docs USING fts5(path, body)')
    n = 0
    for pat in ('*.md', '*.txt'):
        for fp in glob.glob(os.path.join(a.dir, '**', pat), recursive=True):
            try:
                with open(fp, encoding='utf-8', errors='ignore') as f:
                    body = f.read()
            except OSError:
                continue
            c.execute('INSERT INTO docs(path, body) VALUES(?,?)', (fp, body))
            n += 1
    c.commit()
    c.close()
    print('indexed %d files -> %s' % (n, a.db))


def cmd_search(a):
    c = sqlite3.connect(a.db)
    q = ' '.join(tok(a.query))
    rows = c.execute('SELECT path, rank FROM docs WHERE docs MATCH ? '
                     'ORDER BY rank LIMIT ?', (q, a.k)).fetchall()
    c.close()
    out = [{'path': p, 'bm25_rank': r, 'rank': i + 1}
           for i, (p, r) in enumerate(rows)]
    if a.out:
        json.dump(out, open(a.out, 'w'), indent=2)
    print(json.dumps(out[:20], indent=2))


def cmd_expand(a):
    c = sqlite3.connect(a.db)
    q = ' '.join(tok(a.query))
    rows = c.execute('SELECT body FROM docs WHERE docs MATCH ? LIMIT ?',
                     (q, a.k)).fetchall()
    c.close()
    qterms = set(tok(a.query))
    freq = {}
    for (body,) in rows:
        for t in tok(body):
            if t not in qterms and len(t) > 2:
                freq[t] = freq.get(t, 0) + 1
    cands = sorted(freq.items(), key=lambda kv: -kv[1])[:10]
    print(json.dumps([{'term': t, 'df_topk': f} for t, f in cands],
                     indent=2))


def cmd_fuse(a):
    ra = {r['path']: r.get('rank', i + 1)
          for i, r in enumerate(json.load(open(a.a)))}
    rb = {r['path']: r.get('rank', i + 1)
          for i, r in enumerate(json.load(open(a.b)))}
    fused = {}
    for p, r in ra.items():
        fused[p] = fused.get(p, 0.0) + 1.0 / (a.k + r)
    for p, r in rb.items():
        fused[p] = fused.get(p, 0.0) + 1.0 / (a.k + r)
    out = [{'path': p, 'rrf': round(s, 6)}
           for p, s in sorted(fused.items(), key=lambda kv: -kv[1])]
    print(json.dumps(out[:20], indent=2))


def main():
    ap = argparse.ArgumentParser(prog='ir.py')
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('index')
    s.add_argument('dir')
    s.add_argument('--db', required=True)
    s.set_defaults(f='index')
    s = sub.add_parser('search')
    s.add_argument('db')
    s.add_argument('query')
    s.add_argument('--k', type=int, default=100)
    s.add_argument('--out', default='')
    s.set_defaults(f='search')
    s = sub.add_parser('expand')
    s.add_argument('db')
    s.add_argument('query')
    s.add_argument('--k', type=int, default=5)
    s.set_defaults(f='expand')
    s = sub.add_parser('fuse')
    s.add_argument('a')
    s.add_argument('b')
    s.add_argument('--k', type=int, default=60)
    s.set_defaults(f='fuse')
    a = ap.parse_args()
    {'index': cmd_index, 'search': cmd_search, 'expand': cmd_expand,
     'fuse': cmd_fuse}[a.f](a)


if __name__ == '__main__':
    main()
