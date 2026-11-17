#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lint.py — 记忆健康检查：断链 / 重复 / 陈旧。

用法: python lint.py <memory_dir> [--stale-months 3]
"""
import argparse
import os
import sqlite3
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_index import build


def lint(memory_dir, stale_months=3, db=None):
    db = db or os.path.join(memory_dir, 'memory.db')
    build(memory_dir, db)
    conn = sqlite3.connect(db)
    names_lower = {r[0].lower() for r in conn.execute('SELECT name FROM facts')}

    # 断链：[[tgt]] 的 tgt 不在事实名集合里
    broken = []
    for src, tgt in conn.execute('SELECT src, tgt FROM links').fetchall():
        if tgt.lower() not in names_lower:
            broken.append((src, tgt))

    # 重复：description 非空且相同
    dups = []
    for desc, _ in conn.execute(
            'SELECT description, COUNT(*) FROM facts '
            'WHERE description<>"" GROUP BY description HAVING COUNT(*)>1'
    ).fetchall():
        names_d = [r[0] for r in conn.execute(
            'SELECT name FROM facts WHERE description=?', (desc,)).fetchall()]
        dups.append((desc, names_d))

    # 陈旧：type=project 且 updated 早于 cutoff
    cutoff = (date.today() - timedelta(days=30 * stale_months)).isoformat()
    stale = conn.execute(
        "SELECT name, updated, path FROM facts "
        "WHERE type='project' AND updated<>'' AND updated<?", (cutoff,)
    ).fetchall()
    # 无日期的 project 也提醒
    no_date = [r[0] for r in conn.execute(
        "SELECT name FROM facts WHERE type='project' "
        "AND (updated IS NULL OR updated='')").fetchall()]

    conn.close()
    return broken, dups, stale, no_date


def main():
    ap = argparse.ArgumentParser(description='记忆健康检查')
    ap.add_argument('memory_dir', help='memory 目录路径')
    ap.add_argument('--stale-months', type=int, default=3,
                    help='project 类型超多少个月算陈旧')
    args = ap.parse_args()
    broken, dups, stale, no_date = lint(args.memory_dir, args.stale_months)

    print('== 记忆健康检查 ==')
    print(f'\n[断链] {len(broken)} 条')
    for src, tgt in broken:
        print(f'  {src} → [[{tgt}]]  目标不存在')

    print(f'\n[重复] {len(dups)} 组')
    for desc, names_d in dups:
        print(f'  {names_d}  desc="{desc[:40]}"')

    print(f'\n[陈旧 project] {len(stale)} 条（超 {args.stale_months} 个月）')
    for name, updated, path in stale:
        print(f'  {name}  (updated {updated}) → {path}')
        print(f'    ⚠ 使用前请核实此事实是否仍成立')

    if no_date:
        print(f'\n[无日期 project] {len(no_date)} 条：{no_date}')

    if not (broken or dups or stale or no_date):
        print('\n✓ 全部健康')


if __name__ == '__main__':
    main()
