#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""init_watchlist.py — 把一组公司名或 6 位代码落成 watchlist.json（本件第一公民）。

用法：
    python3 init_watchlist.py --run-dir <目录> --subject 600519 --subject 某某股份 \
                              [--from-return <返货转写件.jsonl>] [--quiet]
规则（与 SKILL.md §1 一致）：
    · 6 位数字直接作 sec_code；名称必须在 --from-return 给的候选里**唯一命中**才绑码；
    · 命中 0 条或多条 → 列出候选让用户点，本脚本**不代选**，退码 1；
    · 缺字段即报错不猜；同一组输入重复跑产出逐字节相同（幂等）。
零网络：不取任何数，只读本地返货转写件。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CODE = re.compile(r'^\d{6}$')


def load_return(path: Path | None):
    if not path:
        return []
    rows = []
    for i, ln in enumerate(path.read_text(encoding='utf-8').split('\n'), 1):
        ln = ln.strip()
        if not ln:
            continue
        try:
            obj = json.loads(ln)
        except json.JSONDecodeError:
            raise SystemExit(f'init_watchlist: --from-return 第 {i} 行不是 JSON：{ln[:40]}…')
        if not isinstance(obj, dict):
            raise SystemExit(f'init_watchlist: --from-return 第 {i} 行是 JSON {type(obj).__name__}，'
                             f'本件每行只收对象（一条主体＝一个对象，缺字段即报错，不猜）')
        if 'name' not in obj and 'code' not in obj:
            raise SystemExit(f'init_watchlist: --from-return 第 {i} 行需含 name/code 至少一键（缺字段即报错，不猜）')
        rows.append(obj)
    return rows


def resolve(subject: str, rows):
    if CODE.match(subject):
        hit = [r for r in rows if r.get('code') == subject]
        name = hit[0].get('name') if len(hit) == 1 else ''
        return {'code': subject, 'name': name or subject}, []
    cands = [r for r in rows if subject in (r.get('name') or '')]
    if len(cands) == 1:
        return {'code': cands[0].get('code') or '', 'name': cands[0].get('name')}, []
    return None, [f"{c.get('name','?')} / {c.get('code','?')}" for c in cands]


def main() -> int:
    ap = argparse.ArgumentParser(description='生成/更新 watchlist.json（零网络，不代选主体）')
    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--subject', action='append', default=[], help='公司名或 6 位代码，可重复')
    ap.add_argument('--from-return', help='主体解析返货转写件（jsonl，每行含 name/code）')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    subs = [s.strip() for s in args.subject if s.strip()]
    if not subs:
        print('init_watchlist: 至少给一个 --subject（名或 6 位码）', file=sys.stderr)
        return 1
    rows = load_return(Path(args.from_return) if args.from_return else None)
    out, unresolved = [], []
    for s in subs:
        rec, cands = resolve(s, rows)
        if rec is None:
            unresolved.append((s, cands))
            continue
        if not CODE.match(rec['code']):
            unresolved.append((s, cands or ['（该名称在返货件里没有 6 位码）']))
            continue
        out.append(rec)
    run_dir = Path(args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    wl = run_dir / 'watchlist.json'
    prev = None
    if wl.exists() and not unresolved:
        prev = json.loads(wl.read_text(encoding='utf-8'))
    body = {'subjects': sorted(out, key=lambda r: (r['code'], r['name'])),
            'source': 'from-return' if rows else 'codes-only'}
    text = json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
    if prev is not None and json.dumps(prev, ensure_ascii=False, sort_keys=True) == json.dumps(body, ensure_ascii=False, sort_keys=True):
        if not args.quiet:
            print(f'幂等：{wl} 内容不变（同主体集）')
        return 0
    wl.write_text(text, encoding='utf-8')
    if not args.quiet:
        print(f'写入 {wl}：{len(out)} 个主体')
    for s, cands in unresolved:
        print(f'未绑码：{s} → 候选：{ "、".join(cands) if cands else "无"}（请用户点名，本件不代选）', file=sys.stderr)
    return 1 if unresolved else 0


if __name__ == '__main__':
    sys.exit(main())
