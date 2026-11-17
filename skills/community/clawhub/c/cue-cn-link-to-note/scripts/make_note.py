#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_note.py — 离线笔记骨架发生器：把「已经取回本地的那份原文」排成一条能直接进笔记库的笔记骨架。

用法：
    python3 -B scripts/make_note.py --source 原文.md [--url https://… ] [--title 标题]
                                    [--quote-line 5 | --quote-page 1] [--asof YYYY-MM-DD] --out 我的笔记.md
    python3 -B scripts/make_note.py --help

它做什么：
    只读那份原文（解析通道取回的本地件，或你手上已有的文件），把定位、检索日、四件头部自标、
    四节形状排好；原话引用那一句是**从原文那一行逐字摘出来的**——不是它替你重写的一句话。
它不做什么：
    不抓链接、不发请求、不替你决定哪条要点重要。要点位留三条占位且不挂锚，
    机检按设计在这一节发 E-ANCHOR——那是「等你把要点摘进来并挂上锚」的记号，不是待补的疏漏。

退码：0 骨架落成；1 原文里没有可用文本（空文件＝没有出处，不是待填）；3 取值域故障（原文读不到、--asof 形制不对、定位取不到）。
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

PAGE_RE = re.compile(r'第\s*(\d+)\s*页')


def pick_line(lines, hint_line=None, hint_page=None):
    """选出引用那一行：给了就用给的，没给就取正文里最长的一行实句（不为省字改写）。"""
    if hint_page is not None:
        starts = [i for i, l in enumerate(lines) if PAGE_RE.search(l) and PAGE_RE.search(l).group(1) == str(hint_page)]
        if not starts:
            return None, None, '第 %s 页这一页标在原文里找不到' % hint_page
        body = [i for i in range(starts[0] + 1, len(lines))
                if not PAGE_RE.search(lines[i]) and lines[i].strip()]
        if not body:
            return None, None, '第 %s 页里没有承载文本的行' % hint_page
        i = max(body, key=lambda k: len(lines[k]))
        return i + 1, lines[i].strip(), None
    if hint_line is not None:
        if hint_line < 1 or hint_line > len(lines) or not lines[hint_line - 1].strip():
            return None, None, '第 %d 行取不到可用文本（现读行数=%d）' % (hint_line, len(lines))
        return hint_line, lines[hint_line - 1].strip(), None
    cand = [(len(l), i) for i, l in enumerate(lines)
            if l.strip() and not l.startswith(('#', '〔')) and len(l.strip()) >= 18
            and not any(ch in l for ch in '「」『』')]   # 自带引号的行不选：套出来就是引号里再嵌引号，比对会读成内层那一段
    if not cand:
        return None, None, None
    _, i = max(cand)
    return i + 1, lines[i].strip(), None


def main():
    ap = argparse.ArgumentParser(prog='make_note.py', description=__doc__, add_help=False)
    ap.add_argument('--source', required=True, help='已经取回本地的那份原文（解析件或已有文件）')
    ap.add_argument('--url', help='这条链接的原始 URL（只登记，本件不发请求）')
    ap.add_argument('--title', help='笔记标题；不给就用原文首行或文件名')
    ap.add_argument('--quote-line', type=int, help='原话引用取原文的第几行')
    ap.add_argument('--quote-page', type=int, help='原话引用取原文的第几页（页标形如〔第 1 页〕）')
    ap.add_argument('--asof', help='检索日 YYYY-MM-DD（缺省＝本次运行的当天）')
    ap.add_argument('--out', help='骨架落盘位置；不给就走标准输出')
    ap.add_argument('-h', '--help', action='store_true')
    a = ap.parse_args()
    if a.help:
        print(__doc__)
        return 0
    src = Path(a.source)
    if not src.is_file():
        print('取值域故障：原文读不到 %s（本件不抓链接——先把正文取回本地，再跑这一支）' % src)
        return 3
    lines = src.read_text(encoding='utf-8', errors='replace').split('\n')
    if not any(l.strip() for l in lines):
        print('没有可用文本：%s 是空的——空原文不出笔记（那是没有出处，不是待填）' % src)
        return 1
    today = dt.date.today().isoformat()
    if a.asof:
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', a.asof):
            print('取值域故障：--asof 要写成 YYYY-MM-DD，现读=%r（笔记进库后靠这一天判时效——这一天由你记录；机检只核它形制对不对、在不在，不证它是否真是取回当天）' % a.asof)
            return 3
        asof = a.asof
    else:
        asof = today
    if a.quote_line is not None and a.quote_page is not None:
        print('用法错：--quote-line 与 --quote-page 二选一（两个都给就无从判引用出处落在哪一个）')
        return 2

    title = a.title
    if not title:
        first_hash = next((l for l in lines if l.startswith('# ')), None)
        title = first_hash[2:].strip() if first_hash else src.stem
    where = a.url or str(src)
    q_no, q_text, q_err = pick_line(lines, a.quote_line, a.quote_page)
    if q_err:
        print('取值域故障：原话引用取不到（%s）' % q_err)
        return 3

    out = ['# %s（一条笔记）' % title, '',
           '本页由 AI 整理，是 **AI 整理笔记**：每条要点都请回原文核对，它不构成结论或建议，判断位 [待人工]。',
           '链接／出处：%s ｜检索日：%s｜读取方式：本件只读盘上那份原文（%s），不抓链接、不发请求'
           % (where, asof, src),
           '这一条的形状：要点各一行、行末挂 [S#]；原话只留一句、带页码或行号；缺的那部分写第三节点名。', '',
           '## 1、要点', '',
           '- （待填：这条链接里对你有用的一句话，摘进来并在行末挂 [S1]）',
           '- （待填：第二要点——要点共 3–7 条，少于 3 条说明这条没读透，多于 7 条已经不是一条笔记了）',
           '- （待填：第三要点——写不出的那条别硬写，落进第三节点名为未取到）', '',
           '## 2、原话引用', '']
    if q_no is None:
        out.append('> （未取到：原文里没有可直接照抄的实句——把这一节删掉，并在第三节点名，不要加引号冒称原文）')
    else:
        page = None
        for i in range(0, q_no - 1):          # 取最近的那一枚页标——取第一枚会把第 2 页的正文标成第 1 页，机检照实发红
            m = PAGE_RE.search(lines[i])
            if m:
                page = m.group(1)
        loc = '%s:%d' % (src, q_no)
        if page:
            loc = '〔第 %s 页〕，%s' % (page, loc)
        out.append('> 「%s」（出处：%s）' % (q_text, loc))
    out += ['', '## 3、口径与未取到', '',
            '- 口径：本条只出自一处（上面那枚来源），单源笔记不做跨源互校——这是设计，不是遗漏；要互校就换多源那一路',
            '- 未取到：作者署名、发布日期、以及原文本身没载的东西，本骨架一律不代填（代填就是编）',
            '- 口径：检索日 %s；链接那一侧隔天就可能换形制，页码与行号只在那一刻成立' % asof,
            '- 判断位：这条笔记要不要进你的库、信不信上面那句结论，一律 [待人工]', '',
            '## 4、来源', '',
            '- [S1] %s（%s ｜检索日 %s）' % (title, (a.url if a.url else '%s:1' % src), asof)]
    body = '\n'.join(out) + '\n'

    if a.out:
        p = Path(a.out)
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding='utf-8')
        except OSError as e:
            print('取值域故障：写不到 %s（%s）' % (p, e.strerror or '原因未取到'))
            return 3
        print('骨架落成：%s｜原文行数=%d｜引用=%s｜要点待填=3 条（机检按设计在 E-ANCHOR 发红）'
              % (p, len(lines), ('第 %d 行逐字摘出' % q_no) if q_no else '未取到'))
    else:
        sys.stdout.write(body)
        print('\n---- 以上为骨架全文；未落盘（没给 --out）。原文行数=%d｜引用=%s'
              % (len(lines), ('第 %d 行' % q_no) if q_no else '未取到'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
