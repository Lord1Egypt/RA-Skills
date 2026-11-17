#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_outline.py — 零通道降级：把手上已有的公告清单排成「跨期跟踪稿」的骨架。

用法：
    python3 make_outline.py <公告清单.jsonl> [--out 骨架.md]
    python3 make_outline.py --help

输入每行一个 JSON 对象，至少三格：
    {"date": "2026-01-15", "node": "草案", "title": "重组报告书（草案）", "url": "https://…"}
    date  YYYY-MM-DD（公告披露日）
    node  在册节点之一：停牌／预案／草案／问询／过会／核准／实施／终止
    title 公告标题（原样，不改写）
    url   公告链接（原样，不改写）

它做什么：按 date 升序排成第三节时间轴，把每行 title+url 落成第七节来源行，编号 [S1]…[Sn]；
          第四节每步变化留空槽（变化要读原文才知道，本脚本不猜），第五节未决事项留空槽。
它不做什么：不读公告正文、不判断节点、不填变化、不下结论——**没有通道时它只排形状，不产出内容**。
          所以骨架跑过 check_tracker.py 必然红（结论与变化是占位），这是设计：红在占位行上，
          提醒你补完再交，而不是让一份空壳冒充成品。

退码：0 骨架已写出；1 清单里没有一行可用（逐行点名为什么不可用）；2 用法错；3 读不到输入文件。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NODES = ('停牌', '预案', '草案', '问询', '过会', '核准', '实施', '终止')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
REQUIRED = ('date', 'node', 'title', 'url')

HEAD = """AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]

跟踪口径：跨期（同一笔交易的多份公告按时间轴串起来，标进度节点与每步变化）

## 一、一句话结论

（待填：本件不代你下结论）

## 二、交易概况

- （待填：上市公司、交易对方、标的资产各一行，逐条挂源）

## 三、进度时间轴

"""

MID = """
## 四、每步变化

- （待填：`- 变化项：前值 → 后值 [S#][S#]`，每行至少两枚不同号的锚）

## 五、未决事项

- （待填：交易还没走到实施或终止，就一定有未决事项）

## 六、未取到与口径

- （待填：正文写了未取到的，这里逐条点名；口径写清取的是哪一版公告）

## 七、来源

"""


def main() -> int:
    ap = argparse.ArgumentParser(prog='make_outline.py', add_help=False,
                                 description='把公告清单排成跨期跟踪稿骨架（零通道降级，只排形状不产内容）')
    ap.add_argument('manifest', nargs='?')
    ap.add_argument('--out')
    ap.add_argument('-h', '--help', action='store_true')
    a = ap.parse_args()
    if a.help or not a.manifest:
        print(__doc__)
        return 0 if a.help else 2

    src = Path(a.manifest)
    if not src.is_file():
        print(f'取值域故障：读不到公告清单 {src}（不当「零行」读）')
        return 3

    rows, rejected = [], []
    for no, raw in enumerate(src.read_text(encoding='utf-8', errors='replace').split('\n'), 1):
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            rejected.append((no, f'不是合法 JSON（{e.msg}）'))
            continue
        if not isinstance(obj, dict):
            rejected.append((no, '不是 JSON 对象'))
            continue
        miss = [k for k in REQUIRED if not str(obj.get(k) or '').strip()]
        if miss:
            rejected.append((no, '缺格 ' + '／'.join(miss)))
            continue
        d, node = str(obj['date']).strip(), str(obj['node']).strip()
        if not DATE_RE.match(d):
            rejected.append((no, f'date「{d}」不是 YYYY-MM-DD'))
            continue
        if node not in NODES:
            rejected.append((no, f'node「{node}」不在册（在册＝{"／".join(NODES)}）'))
            continue
        rows.append((d, node, str(obj['title']).strip(), str(obj['url']).strip()))

    for no, why in rejected:
        print(f'  跳过第 {no} 行：{why}')
    if not rows:
        print(f'清单 {src.name} 里没有一行可用（跳过 {len(rejected)} 行，逐行原因见上）——不写空骨架冒充成品')
        return 1

    rows.sort(key=lambda r: r[0])
    tl = ''.join(f'- {d}｜{node}｜{title} [S{i}]\n' for i, (d, node, title, _u) in enumerate(rows, 1))
    srcs = ''.join(f'- [S{i}] {title} {u} 检索日 {rows[0][0]}\n'
                   for i, (_d, _n, title, u) in enumerate(rows, 1))
    text = HEAD + tl + MID + srcs

    out = Path(a.out) if a.out else src.with_suffix('.skeleton.md')
    out.write_text(text, encoding='utf-8')
    print(f'骨架已写出：{out}（时间轴 {len(rows)} 行·来源 {len(rows)} 行·跳过 {len(rejected)} 行）')
    print('注意：结论与每步变化是占位，跑 check_tracker.py 会红在占位行上——这是设计，补完再交。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
