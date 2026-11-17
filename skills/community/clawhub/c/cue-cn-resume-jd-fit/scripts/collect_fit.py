#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""collect_fit.py — 离线采集器：读一枚合成 JD，把「要求」逐条排成四节核对骨架（不代人做匹配）。

用法：
    python3 -B scripts/collect_fit.py --jd JD.md --resume 简历.md [--out 报告.md]
                                      [--require-keyword 要求] [--asof YYYY-MM-DD]
    python3 -B scripts/collect_fit.py --help

它做什么：
    只读那两份本地文件（简历与 JD 都可为解析通道取回的正文），从 JD 里按节标题含「要求／资格」的那一段
    逐条抽出要求行，原样带行号写进第二节，每条后面留一个证据待填位；第四节把两侧都登记成带定位与解析日的来源行。
它不做什么：
    不代人判断简历里哪句话对上哪条要求，不数年限，不做匹配率，不排先后——那些要么是人做的判断，要么是造出来的数。
    远端那侧要读得更多层，走解析通道把文件取回本地再跑；本件自己不发请求、不执行任何一侧附带的代码。

骨架按设计发红：证据待填位不是简历原文里的逐字句，机检在道三发 E-QUOTE——那是「匹配这一步还没做」的记号，不是待补的疏漏。
退码：0 骨架落成；1 JD 里抽不出可核对的要求行（没有可对齐的对象，不出骨架）；3 取值域故障（文件读不到、--asof 形制不对）。
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

NUM_RE = re.compile(r'^\s*(?:\d+[.、]|[（(]\d+[)）]|[-*]\s)\s*(.+)$')
REQ_HEAD_RE = re.compile(r'要求|资格|任岗条件|任职')


def read_lines(path, label):
    p = Path(path)
    if not p.is_file():
        print('取值域故障：%s 读不到 %s（读不到不等于「没有要求」，也不当「简历空白」）' % (label, path))
        raise SystemExit(3)
    return p.read_text(encoding='utf-8', errors='replace').split('\n')


def pick_requirements(lines, keyword):
    """从 JD 里取要求段：节标题命中关键词之后、下一个「## 」之前的编号行。"""
    out, in_sec, sec_title = [], False, ''
    for i, ln in enumerate(lines, 1):
        if ln.startswith('## '):
            in_sec = bool(re.search(keyword, ln[3:]))
            sec_title = ln[3:].strip() if in_sec else sec_title
            continue
        if not in_sec:
            continue
        m = NUM_RE.match(ln)
        if m and m.group(1).strip():
            out.append((i, m.group(1).strip()))
    return out, sec_title


def main():
    ap = argparse.ArgumentParser(prog='collect_fit.py', description=__doc__, add_help=False)
    ap.add_argument('--jd', required=True, help='岗位说明（JD）本地文件')
    ap.add_argument('--resume', required=True, help='简历本地文件')
    ap.add_argument('--out', help='骨架落盘位置；不给就走标准输出')
    ap.add_argument('--require-keyword', default='要求|资格', help='要求段的节标题关键词（默认「要求|资格」）')
    ap.add_argument('--asof', help='解析日 YYYY-MM-DD（缺省＝本次运行的当天）')
    ap.add_argument('-h', '--help', action='store_true')
    a = ap.parse_args()
    if a.help:
        print(__doc__)
        return 0
    today = dt.date.today().isoformat()
    if a.asof:
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', a.asof):
            print('取值域故障：--asof 要写成 YYYY-MM-DD，现读=%r（来源行的解析日要的是真实存在的一天）' % a.asof)
            return 3
        asof = a.asof
    else:
        asof = today

    jd_lines = read_lines(a.jd, 'JD 原文')
    rs_lines = read_lines(a.resume, '简历原文')
    reqs, sec_title = pick_requirements(jd_lines, a.require_keyword)
    if not reqs:
        print('没有可核对的要求行：%s 里按节标题含「%s」抽到 0 条——不出骨架（那是对不齐，不是待填）；'
              '要求段若用了别的标题，请带 --require-keyword 指定' % (a.jd, a.require_keyword))
        return 1
    title = next((l[2:].strip() for l in jd_lines if l.startswith('# ')), Path(a.jd).stem)

    out = ['# %s × 简历 双向核对（骨架）' % title, '',
           '本页由 AI 整理，是 **AI 整理初稿**：每条都请回原文核对，它不构成录用或排序建议，判断位 [待人工]。',
           '两侧文件：%s（JD）｜%s（简历）｜解析日：%s｜读取方式：本地只读（本件不抓链接、不执行任何一侧附带的代码）'
           % (a.jd, a.resume, asof), '',
           '## 1、一句话结论', '',
           '（待填：只说匹配到哪一层，一句、80 字符内；不排先后、不下录不录的话）', '',
           '## 2、逐条对齐', '']
    for no, text in reqs:
        out.append('- 要求「%s」[S2] → 证据「（待填：从简历里照抄那一句）」[S1]（要求出处 %s:%d）'
                   % (text, a.jd, no))
    out += ['', '## 3、缺口与未取到', '',
            '- JD 有要求而简历无证据的一条：（待填——逐条对齐里判为对不上的，都要在这一栏留名；一条没有就写「本栏无」）',
            '- 简历有内容而 JD 不关心的两条：（待填——简历里那些没有对应要求的内容，也要点名，别当没看见；没有就写「本栏无」）',
            '- 口径：两侧引号内都必须是原文逐字；行号按解析日那一刻的盘上现值写，文件改了就失效',
            '- 判断位：这一份要不要往下走、怎么走，一律 [待人工]——本件不做人评', '',
            '## 4、来源', '',
            '- [S1] 简历（%s:1 ｜解析日 %s）' % (a.resume, asof),
            '- [S2] JD（%s:1 ｜解析日 %s）' % (a.jd, asof),
            '',
            '要求段现读：%s｜抽出要求行 %d 条（数由上面第二节逐行现算；这行不是来源行，别写成列表项）'
            % (sec_title or '(按关键词命中的节)', len(reqs))]
    body = '\n'.join(out) + '\n'

    if a.out:
        p = Path(a.out)
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding='utf-8')
        except OSError as e:
            print('取值域故障：写不到 %s（%s）' % (p, e.strerror or '原因未取到'))
            return 3
        print('骨架落成：%s｜要求行=%d 条｜简历行数=%d｜JD 行数=%d（计数由本件现算自报）'
              % (p, len(reqs), len(rs_lines), len(jd_lines)))
    else:
        sys.stdout.write(body)
        print('\n---- 以上为骨架全文；未落盘（没给 --out）。要求行=%d 条' % len(reqs))
    return 0


if __name__ == '__main__':
    sys.exit(main())
