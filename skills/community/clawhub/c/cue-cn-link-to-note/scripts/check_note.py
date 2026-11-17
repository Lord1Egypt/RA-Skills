#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_note.py — 校一条「链接→笔记」是否合 `SKILL.md` §3 四节契约，并把原话引用逐字比回原文。

用法：
    python3 -B scripts/check_note.py <笔记.md> [--source 原文.md]     校一条笔记（纯标准库、零网络、不发任何请求）
    python3 -B scripts/check_note.py --selftest [--source 原文.md]    跑包内夹具：好样必须过，四枚坏样必须各发它该发的那一道
    python3 -B scripts/check_note.py --help                            本说明

出口形制（与套件姊妹件同族）：
    失败 = 一行 "FAIL: <文件>（N 条）"，其下每条详行先打错误码前缀，道名后是行号与该道规格；末行「码表:」只列本次真正用到的码。
    全过 = 一行 "PASS: <文件>（…）"，并印「扫过 N 行」与逐道计数——计数说看到多少，不说猜多少。

四道（判定全集在本脚本，本文只指路）：
    道一 形制 E-FORMAT  ：首行是标题；头部四件自标逐字在位；四节齐且按序；要点枚数 3–7（少于 3＝这条链接没读透，多于 7＝已经不是一条笔记）
    道二 锚   E-ANCHOR  ：每条要点行末带 [S#]；该编号在第四节有对应行；来源行必须同时带 定位（URL／文件:行号／第 N 页）与检索日 YYYY-MM-DD（本件只核这一枚字段在不在、形制对不对；那天是否真是取回当天，机检核不了）
    道三 引用 E-QUOTE   ：原话引用至多一枚、且必须带定位；给了 --source 就把引号里那段逐字比回该定位——比不回去就是冒称原文，发红
                          没给 --source 时这一道**不可判**，明写不并入通过（不可判不等于没违例）
    道四 缺口 E-COVERAGE：正文写了「未取到／取不到／读不到／截断／没取全」的必须第三节逐条点名；第三节一行没有、或第四节零来源行，都发红

退码：0 全过（不可判的道在输出里明写，不改退码）；1 有发条；2 用法错；3 取值域故障（笔记或原文读不到，不读成「零违例」）。
"""

from __future__ import annotations

import argparse
import contextlib
import io
import re
import sys
from pathlib import Path

SECTIONS = ('要点', '原话引用', '口径与未取到', '来源')
MARKS = ('AI 整理笔记', '请回原文核对', '不构成结论或建议', '判断位 [待人工]')
ANCHOR_RE = re.compile(r'\[S(\d+)\]\s*$')
URL_RE = re.compile(r'https?://\S+|www\.\S+')
LOC_RE = re.compile(r'[A-Za-z0-9_./-]+:\d+|https?://\S+|www\.\S+|第\s*\d+\s*页')
PAGE_RE = re.compile(r'第\s*(\d+)\s*页')
LINE_RE = re.compile(r'[:：](\d+)')
DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')
QUOTE_RE = re.compile(r'[「『](.+)[」』]', re.S)
GAP_RE = re.compile(r'未取到|取不到|读不到|没取全|截断')
PLACE_RE = re.compile(r'\[待人工\]')
MIN_POINTS, MAX_POINTS = 3, 7


def norm(text: str) -> str:
    return re.sub(r'\s+', '', text).strip()


def page_block(lines, page):
    start = next((i for i, l in enumerate(lines) if PAGE_RE.search(l) and PAGE_RE.search(l).group(1) == str(page)), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if PAGE_RE.search(lines[i])), len(lines))
    return '\n'.join(lines[start:end])


def resolve_cited_file(path_str, source, source_lines):
    """引用行里那个 文件:行号 指向谁：与 --source 同一枚就用已读的原文；否则按盘上现读；都读不到返回 None。"""
    if source is not None and (path_str == str(source) or Path(path_str).name == source.name):
        return source_lines
    p = Path(path_str)
    if p.is_file():
        return p.read_text(encoding='utf-8', errors='replace').split('\n')
    return None


def check_quote(lines, quote_line_no, quote_text, source, source_lines):
    """引用行的**每一个**定位都各自比一遍——同一行给了页码又给了行号时，只读一个就是把假定位放过。
    → (判定, 逐条说明)。判定 ∈ {合, 不合, 不可判}。"""
    where = lines[quote_line_no - 1]
    if source_lines is None:
        return '不可判', ['未给 --source，没有可比的那份原文']
    want = norm(quote_text)
    results = []
    for page in sorted(set(PAGE_RE.findall(where))):
        block = page_block(source_lines, int(page))
        if block is None:
            results.append(('不合', '「第 %s 页」在原文里找不到页标' % page))
        else:
            results.append(('合' if want in norm(block) else '不合', '第 %s 页' % page))
    for path_str, ln in re.findall(r'([A-Za-z0-9_.\-/]+):(\d+)', where):
        lines_of = resolve_cited_file(path_str, source, source_lines)
        n = int(ln)
        if lines_of is None:
            results.append(('不合', '%s 这枚定位指向的文件读不到（除 --source 外没有第二份可比原文）' % path_str))
        elif n < 1 or n > len(lines_of):
            results.append(('不合', '%s:%d 超出该原文行数（现读行数=%d）' % (path_str, n, len(lines_of))))
        else:
            results.append(('合' if want in norm(lines_of[n - 1]) else '不合', '%s:%d' % (path_str, n)))
    if not results:
        return '不合', ['引用行没有可比对的定位（既无「第 N 页」也无 文件:行号）']
    bad = [d for v, d in results if v == '不合']
    if bad:
        return '不合', bad
    return '合', [d for _, d in results]


def scan(path: Path, source: Path = None, source_lines=None):
    issues = []
    seen = set()
    unverifiable = []

    def add(code, lane, no, msg):
        key = (code, no, msg)
        if key in seen:
            return
        seen.add(key)
        issues.append((code, lane, no, msg))

    lines = path.read_text(encoding='utf-8', errors='replace').split('\n')
    if not lines or not lines[0].startswith('# '):
        add('E-FORMAT', '标题', 1, '首行不是「# 标题」这一形（规格：笔记进库按标题命名，首行就得是标题）')

    head_end = next((i for i, l in enumerate(lines) if l.startswith('## ')), len(lines))
    head = '\n'.join(lines[:head_end])
    for need in MARKS:
        if need not in head:
            add('E-FORMAT', '头部', 1, '头部自标缺『%s』（规格：四件逐字写在第一个「## 」之前）' % need)

    idxs = []
    for n, name in enumerate(SECTIONS, 1):
        hit = [i for i, l in enumerate(lines) if re.match(r'^##\s*%d、%s' % (n, re.escape(name)), l)]
        if not hit:
            add('E-FORMAT', '四节', 1, '缺「## %d、%s」节（规格：四节齐且按一二三四有序）' % (n, name))
        else:
            idxs.append((n, hit[0]))
    bounds = {}
    for pos in range(len(idxs)):
        n, i0 = idxs[pos]
        i1 = idxs[pos + 1][1] if pos + 1 < len(idxs) else len(lines)
        bounds[n] = (i0, i1)

    bullets = []
    if 1 in bounds:
        i0, i1 = bounds[1]
        bullets = [(i + 1, lines[i].strip()) for i in range(i0 + 1, i1) if lines[i].strip().startswith(('- ', '* '))]
        if not MIN_POINTS <= len(bullets) <= MAX_POINTS:
            add('E-FORMAT', '要点枚数', i0 + 1,
                '要点 %d 条，不在 %d–%d 这一档（规格：少于 %d＝这条链接没读透；多于 %d＝已经不是一条能直接进库的笔记）'
                % (len(bullets), MIN_POINTS, MAX_POINTS, MIN_POINTS, MAX_POINTS))
    listed = {}
    if 4 in bounds:
        i0, i1 = bounds[4]
        rows = [(i + 1, lines[i].strip()) for i in range(i0 + 1, i1) if lines[i].strip().startswith(('- ', '* '))]
        if not rows:
            add('E-COVERAGE', '来源', i0 + 1, '第四节一行来源都没有（规格：笔记的价值就在这条能回到哪一处原文，空节等于没出处）')
        for no, ln in rows:
            m = re.match(r'^[-*]\s*\[S(\d+)\]', ln)
            if not m:
                add('E-ANCHOR', '来源', no, '来源行不以 [S#] 开头（规格：编号与要点行的锚一一对应）')
            else:
                listed[int(m.group(1))] = no
            if not DATE_RE.search(ln):
                add('E-ANCHOR', '来源', no, '来源行缺检索日 YYYY-MM-DD（规格：链接那一侧当天就会变，所以这一行要写你是哪天读到的；机检只核这一枚字段在不在、形制对不对，核不了那天是否真是取回当天——那一层由你记录并对得上）')
            if not LOC_RE.search(ln):
                add('E-ANCHOR', '来源', no, '来源行既无 URL／文件:行号 也无「第 N 页」（规格：要回到一处原文，得有个位置）')

    for no, s in bullets:
        m = ANCHOR_RE.search(s)
        if not m:
            add('E-ANCHOR', '锚', no, '要点行行末没有 [S#] 锚（规格：没挂锚的要点不要写进这一节）')
        elif int(m.group(1)) not in listed:
            add('E-ANCHOR', '锚', no, '锚 [S%s] 在第四节没有对应行（规格：正文用的每个编号都要回得到来源行）' % m.group(1))

    quote_lines = [(i + 1, lines[i].strip()) for i in range(len(lines)) if lines[i].strip().startswith('> ')]
    if len(quote_lines) > 1:
        add('E-QUOTE', '引用枚数', quote_lines[1][0],
            '原话引用 %d 枚（规格：至多一枚——一条笔记靠一句原话撑住，抄满篇就成了转述）' % len(quote_lines))
    for no, s in quote_lines[:1]:
        qm = QUOTE_RE.search(s)
        if not qm:
            add('E-QUOTE', '引用形制', no, '引用行里没有「」（规格：逐字那一段用引号括起来，机检才比得了）')
        elif not (PAGE_RE.search(s) or LINE_RE.search(s.split('（')[-1] if '（' in s else s) or URL_RE.search(s)):
            add('E-QUOTE', '引用定位', no, '引用没有定位（规格：带「第 N 页」或 文件:行号，读者才翻得到那一处）')
        else:
            if source_lines is None:
                unverifiable.append('道三 不可判：第 %d 行有引用，但未给 --source，没有可比的那份原文（不可判不并入通过）' % no)
            else:
                verdict, detail = check_quote(lines, no, qm.group(1), source, source_lines)
                if verdict == '不合':
                    add('E-QUOTE', '逐字回原文', no,
                        '引号里那段不是原文逐字（%s）——规格：要么照抄那一处，要么改写成要点并挂锚，不能加引号冒称原文'
                        % '／'.join(detail))
    if source_lines is not None and not quote_lines:
        unverifiable.append('道三 未跑：这条笔记没有原话引用（不是违例，但这一道这一次没量到东西）')

    if 3 in bounds:
        i0, i1 = bounds[3]
        sec3 = '\n'.join(lines[i0 + 1:i1])
        sec3_bullets = [l for l in lines[i0 + 1:i1] if l.strip().startswith(('- ', '* '))]
        if not sec3_bullets:
            add('E-COVERAGE', '口径', i0 + 1, '第三节一行都没有（规格：口径与未取到都得写在这一节，空白不等于没缺口）')
        gap_words = []
        for i, ln in enumerate(lines, 1):
            if bounds[3][0] < i - 1 < bounds[3][1]:
                continue
            if ln.lstrip().startswith('#'):
                continue          # 节题里那个「未取到」是节名，不是缺口申报——把它当缺口会在好样上发假红
            if GAP_RE.search(ln) and not PLACE_RE.search(ln):
                gap_words.append((i, ln.strip()[:24]))
        for no, frag in gap_words:
            named = any(GAP_RE.search(l) or norm(frag) in norm(l) for l in lines[i0 + 1:i1] if l.strip().startswith(('- ', '* ')))
            if not named:
                add('E-COVERAGE', '缺口点名', no,
                    '第 %d 行写了缺口（%s）而第三节没点名（规格：没取到的要么在这节逐条列出，要么别写）' % (no, frag))
    elif 3 not in bounds:
        pass  # 缺节已在道一发过
    return issues, lines, unverifiable


def run_one(path: Path, source: Path = None, quiet=False):
    source_lines = None
    if source is not None:
        if not source.is_file():
            print('取值域故障：原文读不到 %s（道三不因此算通过，也不算违例）' % source)
            return 3, 0, 0
        source_lines = source.read_text(encoding='utf-8', errors='replace').split('\n')
    issues, lines, unverifiable = scan(path, source, source_lines)
    codes = sorted({c for c, _, _, _ in issues})
    counts = {}
    for c, _, _, _ in issues:
        counts[c] = counts.get(c, 0) + 1
    if not quiet:
        for code, lane, no, msg in issues:
            print('  [%s] [%s] 第 %d 行：%s' % (code, lane, no, msg))
        for u in unverifiable:
            print('  [不可判] %s' % u)
    if issues:
        print('FAIL: %s（%d 条）' % (path.name, len(issues)))
        print('       ' + '；'.join('%s %d 条' % (c, n) for c, n in sorted(counts.items())))
        print('       码表: ' + '；'.join('%s=%s' % (c, codes_doc[c]) for c in codes))
        return 1, len(issues), len(unverifiable)
    print('PASS: %s（首行标题、四件自标在位、四节齐、要点 %d–%d 条、每条挂锚回得到来源、引用逐字与定位齐、缺口都点名）'
          % (path.name, MIN_POINTS, MAX_POINTS))
    print('       扫过 %d 行，发条 0 条，不可判 %d 项；判定与阈值全集以本脚本现值为准（--help 看四道说明）'
          % (len(lines), len(unverifiable)))
    return 0, 0, len(unverifiable)


codes_doc = {'E-FORMAT': '道一 形制与要点枚数', 'E-ANCHOR': '道二 锚与来源定位',
             'E-QUOTE': '道三 原话引用逐字与定位', 'E-COVERAGE': '道四 口径与缺口点名'}


def selftest(source: Path):
    fx = Path(__file__).resolve().parent / 'fixtures'
    cases = [('good-note.md', 0, None),
             ('bad-format.md', 1, 'E-FORMAT'),
             ('bad-no-anchor.md', 1, 'E-ANCHOR'),
             ('bad-quote.md', 1, 'E-QUOTE'),
             ('bad-unnamed-gap.md', 1, 'E-COVERAGE')]
    bad = 0
    for name, want_rc, want_code in cases:
        p = fx / name
        if not p.is_file():
            print('  取值域故障：夹具不在场 %s（不读成「零违例」）' % name)
            return 3
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc, _, _ = run_one(p, source)
        detail = buf.getvalue()
        codes = sorted(set(re.findall(r'E-[A-Z]+', detail)))
        if rc != want_rc:
            print('  不合 %s：期望退码 %d，实发 %d' % (name, want_rc, rc))
            bad += 1
            continue
        if want_code and codes != [want_code]:
            print('  不合 %s：期望只发 %s，实发码集=%s（多发＝这枚坏样不单一，少发＝这一道量不到了）'
                  % (name, want_code, '、'.join(codes) or '无'))
            bad += 1
            continue
        print('  ok   %s（退码 %d·期望 %s·实发码 %s）' % (name, rc, want_code or '全过', '、'.join(codes) or '无'))
    print('selftest: ' + ('ALL GREEN（好样 1 枚·坏样四枚各只发它该发的那一道 4/4·原文比对真跑）'
                          if bad == 0 else '%d 条不合预期' % bad))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(prog='check_note.py', add_help=False)
    ap.add_argument('note', nargs='?', help='要校的笔记文件')
    ap.add_argument('--source', help='那份原文（解析件或本地文件）：给了才逐字比引用，不给就明写不可判')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--quiet', action='store_true', help='只报末行与计数')
    ap.add_argument('-h', '--help', action='store_true')
    a = ap.parse_args()
    if a.help or (not a.note and not a.selftest):
        print(__doc__)
        return 0 if a.help else 2
    source = Path(a.source) if a.source else None
    if a.selftest:
        default = source or (Path(__file__).resolve().parent / 'fixtures' / 'source-article.md')
        if not default.is_file():
            print('取值域故障：自测要的原文不在场 %s（没有原文，道三无从跑）' % default)
            return 3
        return selftest(default)
    p = Path(a.note)
    if not p.is_file():
        print('取值域故障：读不到笔记文件 %s（不当「零违例」读）' % p)
        return 3
    rc, _, _ = run_one(p, source, quiet=a.quiet)
    return rc


if __name__ == '__main__':
    sys.exit(main())
