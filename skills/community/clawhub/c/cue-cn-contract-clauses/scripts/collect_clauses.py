#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""collect_clauses.py — 离线采集器：读一份合同正文，把条款逐条搬成四节骨架（不代判哪条要盯）。

用法：
    python3 -B scripts/collect_clauses.py --source 合同.md [--out 清单.md] [--asof YYYY-MM-DD] [--max-rows 20]
    python3 -B scripts/collect_clauses.py --help

它做什么：
    只读那份本地文件（解析通道取回的正文或已有文件），按「第 N 条／N.／N、」认出条款行，
    逐条把**整句原文**搬进第二节并自带页码与行号两枚定位（页码取该行的最近前驱）；
    第三节按七类需盯条款各留一个待核位；第四节登记来源与解析日。
它不做什么：
    不判哪一条要盯（那需要读语义，机器按关键词写「未见到」会把「没命中关键词」说成「合同里没有」），
    不代填概览里的标的／期限／价款，不出法律意见、不判效力、不评级排序，不发请求、不执行合同里提到的任何程序。

骨架按设计发红：第三节的七个待核位不是点名，机检在道四发 E-COVERAGE——那是「哪一类要盯还没判」的记号，不是待补的疏漏。
退码：0 骨架落成；1 原文里认不出任何条款行（没有可拆的对象，不出骨架）；3 取值域故障（文件读不到、--asof 形制不对）。
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

CLAUSE_RE = re.compile(r'^\s*((?:第\s*[0-9〇一二三四五六七八九十百]+\s*条|[0-9]+[.、])\s*\S+.*)$')
PAGE_RE = re.compile(r'第\s*(\d+)\s*页')
WATCH_TYPES = ('单方变更', '自动续约', '排他', '违约金', '争议解决地', '数据与保密', '责任上限')


def nearest_page(lines, idx):
    page = None
    for i in range(0, idx):
        m = PAGE_RE.search(lines[i])
        if m:
            page = m.group(1)
    return page


def main():
    ap = argparse.ArgumentParser(prog="collect_clauses.py", description=__doc__, add_help=False)
    ap.add_argument('--source', required=True, help='合同正文（解析件或本地文件）')
    ap.add_argument('--out', help='骨架落盘位置；不给就走标准输出')
    ap.add_argument('--asof', help='解析日 YYYY-MM-DD（缺省＝本次运行的当天）')
    ap.add_argument('--max-rows', type=int, default=20, help='第二节最多搬几条（默认 20，与机检的条数带上限同值）')
    ap.add_argument('-h', '--help', action='store_true')
    a = ap.parse_args()
    if a.help:
        print(__doc__)
        return 0
    src = Path(a.source)
    if not src.is_file():
        print('取值域故障：%s 读不到（本件不抓链接——先把正文取回本地，再跑这一支）' % src)
        return 3
    lines = src.read_text(encoding='utf-8', errors='replace').split('\n')
    if not any(l.strip() for l in lines):
        print('没有可用文本：%s 是空的——空原文不出骨架（那是没有出处，不是待填）' % src)
        return 1
    if a.asof:
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', a.asof):
            print('取值域故障：--asof 要写成 YYYY-MM-DD，现读=%r（来源行的解析日用它）' % a.asof)
            return 3
        try:
            dt.date.fromisoformat(a.asof)
        except ValueError:
            print('取值域故障：--asof 成形但不是日历上存在的一天，现读=%r（来源行的解析日要的是真实存在的一天，2026-13-99 那一形不收）' % a.asof)
            return 3
        asof = a.asof
    else:
        asof = dt.date.today().isoformat()

    clauses = [(i + 1, m.group(1).strip()) for i, l in enumerate(lines) for m in [CLAUSE_RE.match(l)] if m]
    if not clauses:
        print('认不出条款行：%s 里没有匹配「第 N 条／N.／N、」的整行——不出骨架（那是要另定形状，不是待填）' % src)
        return 1
    title = next((l[2:].strip() for l in lines if l.startswith('# ')), src.stem)
    moved = clauses[:a.max_rows]

    out = ['# %s·逐条要点与需盯条款（骨架）' % title, '',
           '本页由 AI 整理，是 **AI 整理初稿**：每条都请回原文核对，它不构成实务级法律意见或效力判断，也不替代律师审查，判断位 [待人工]。',
           '被核对文件：%s｜解析日：%s｜读取方式：本地只读（本件不抓链接、不执行合同里提到的任何程序）' % (src, asof),
           '未读到的部分一律写进第三节，不补常识性推断。', '',
           '## 1、概览', '',
           '标的：（待填，只写文里有的）；期限：（待填）；价款／金额：（待填；文里没有就在这一行写明未见）。', '',
           '## 2、逐条要点', '']
    for no, text in moved:
        page = nearest_page(lines, no - 1)
        loc = '〔第 %s 页〕，' % page if page else ''
        out.append('- 「%s」%s%s:%d [S1]' % (text, loc, src, no))
    out += ['', '## 3、需盯条款', '']
    for name in WATCH_TYPES:
        out.append('- %s：（待核——填原文位置与一句逐字引文，没有这一类就在此写未见到）' % name)
    out += ['', '- 未读到：（待填——扫描缺页、附件未给、正文截断等，都在这行列明）',
            '口径：条款级要点不做跨期比较，也不判效力；本节只登记文里写了什么。',
            '判断位：哪几条要在谈判里盯、怎么盯，一律 [待人工]。', '',
            '## 4、来源与解析日', '',
            '- [S1] %s（%s:1 ｜解析日 %s）' % (title, src, asof),
            '',
            '条款行现读=%d 条｜第二节搬入=%d 条（上限 --max-rows=%d，超出部分本件不代选）｜页码取该行最近前驱'
            % (len(clauses), len(moved), a.max_rows)]
    body = '\n'.join(out) + '\n'

    if a.out:
        p = Path(a.out)
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding='utf-8')
        except OSError as e:
            print('取值域故障：写不到 %s（%s）' % (p, e.strerror or '原因未取到'))
            return 3
        print('骨架落成：%s｜条款行=%d｜搬入要点=%d 条｜待核位=7 类（机检按设计在 E-COVERAGE 发红）'
              % (p, len(clauses), len(moved)))
    else:
        sys.stdout.write(body)
        print('\n---- 以上为骨架全文；未落盘（没给 --out）。条款行=%d' % len(clauses))
    return 0


if __name__ == '__main__':
    sys.exit(main())
