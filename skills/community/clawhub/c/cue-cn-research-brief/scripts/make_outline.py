#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_outline.py — 零通道那一头的骨架发生器：把一份来源清单（逐行 JSON）落成一张待填速览骨架。

一条命令：python3 -B scripts/make_outline.py --sources <sources.jsonl> --out <outline.md>
  来源行必需三键：title／url／asof（asof 是检索日，YYYY-MM-DD）；id 可省，缺省按行序给 S1／S2…。

它只做什么（写在件首防后人夸大）：
  1) 把来源逐条排进第四节，并按来源行的编号在第二节各挂一行「未取到（骨架）」的发现位；
  2) 第一节的结论位留成占位串「（待填：本件不代你下结论）」——**骨架过不了机检是设计**，
     check_brief.py 会在这一行发 E-FORMAT，正是要它发：没有来源交叉过的结论不该被当成速览交付；
  3) 第三节逐条点名「未取到」，一条不省。
  它不发请求、不取数、不填内容：多源取证那一层是通道腿的活（见 README 的通道正路那一节），
  这里给的是「无通道时你能拿到的最好东西就是一张有形状的骨架」。

退码：0 落成；1 来源清单里一行都没有（空清单不静默出骨架）；3 取值域故障（文件读不到／不是合法 JSON／缺必需键）。
零网络、纯标准库。
"""

import argparse
import json
import re
import sys
from pathlib import Path

DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
REQUIRED = ('title', 'url', 'asof')


def die(msg, code):
    print('make_outline: ' + msg)
    return code


def tag(row):
    """锚编号：来源行自带 S# 就用它的，没有就补 S——正文锚与来源行锚必须逐字同形。"""
    raw = str(row['id'])
    return raw if raw.startswith('S') else 'S' + raw


def main():
    ap = argparse.ArgumentParser(description='来源清单 → 待填速览骨架（零网络，不代填结论）')
    ap.add_argument('--sources', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--subject', default='（待填：主体名与代码）')
    ap.add_argument('--window', default='（待填：检索窗口）')
    a = ap.parse_args()

    p = Path(a.sources)
    if not p.is_file():
        return die(f'读不到来源清单 {p}（取值域故障，不猜内容）', 3)
    rows, bad = [], []
    for i, ln in enumerate(p.read_text(encoding='utf-8', errors='replace').split('\n'), 1):
        ln = ln.strip()
        if not ln or ln.startswith('#'):
            continue
        try:
            obj = json.loads(ln)
        except ValueError:
            return die(f'来源清单第 {i} 行不是合法 JSON（不静默跳行）', 3)
        missing = [k for k in REQUIRED if k not in obj]
        if missing:
            bad.append(f'第 {i} 行缺 {missing}')
            continue
        if not DATE_RE.match(str(obj['asof'])):
            bad.append(f"第 {i} 行 asof 不是 YYYY-MM-DD：{obj['asof']!r}")
            continue
        obj.setdefault('id', len(rows) + 1)
        rows.append(obj)
    if bad:
        for b in bad:
            print('  未采信：' + b)
    if not rows:
        return die('来源清单里一条可用行都没有——空清单不出骨架（那是没有出处，不是待填）', 1)

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ['# 多源研究速览（骨架）', '',
             '本页由 AI 整理，是 **AI 整理初稿**：逐条请回原文核对，不构成投资建议，判断位 [待人工]。',
             f'主体：{a.subject}｜检索窗口：{a.window}', '',
             '## 1、一句话结论',
             '（待填：本件不代你下结论）', '',
             '## 2、逐条发现']
    for r in rows:
        lines.append(f'- 未取到（骨架）：{tag(r)} 所载要点待逐字摘入，本件不代填 [{tag(r)}]')
    lines += ['', '## 3、未取到与口径']
    for r in rows:
        lines.append(f'- 未取到：{tag(r)}（{r["title"]}）的逐字要点与可回查定位尚未摘入')
    lines += ['- 口径：本骨架由来源清单生成，未做过任何跨源互校；互校是通道腿的活',
              '- 待人工：结论位空着比填上更诚实（判断位 [待人工]）', '', '## 4、来源']
    for r in rows:
        lines.append(f'- [{tag(r)}] {r["title"]}（{r["url"]} ｜检索日 {r["asof"]}）')
    lines.append('')
    out.write_text('\n'.join(lines), encoding='utf-8')
    print('make_outline: %s 落成｜来源 %d 枚 → 发现位 %d 行、未取到点名 %d 条、结论位留占位（骨架过不了机检是设计）' % (
        out.name, len(rows), len(rows), len(rows)))
    if bad:
        print('  （另有 %d 行未采信，见上方「未采信」逐行）' % len(bad))
    return 0


if __name__ == '__main__':
    sys.exit(main())
