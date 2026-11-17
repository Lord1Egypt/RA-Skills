#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_brief.py — 校一份「中文多源研究速览」是否合 `SKILL.md` §3 四节契约与 §5 红线。

用法：
    python3 check_brief.py <速览.md>        校一份速览（纯标准库、零网络、不发任何请求）
    python3 check_brief.py --selftest       跑包内夹具：好样必须过，四枚坏样必须各发它该发的那一道
    python3 check_brief.py --help            本说明

出口形制（与套件姊妹件同族）：
    失败 = 一行 "FAIL: <文件>（N 条）"，其下每条详行先打错误码前缀（四枚 E-* 之一），道名后是行号与该道规格；
           末行 "码表:" 只列本次真正用到的码与含义。
    全过 = 一行 "PASS: <文件>（…）"，并印「扫过 N 行」与四道计数——计数说看到多少，不说猜多少。

四道是什么（判定全集在本脚本，本文只指路，不复述细节）：
    道一 形制：头部四件自标逐字在位＋四节齐且按一二三四有序＋一句话结论非空非占位
    道二 锚：每条发现行行末带 [S#]，且该编号在第四节有对应行；第四节每行必须同时带 URL 与 YYYY-MM-DD 检索日
    道三 红线：评级／目标价／买卖与走势类断言一律零命中，要写只能同行挂 [待人工]；改数词（约／左右／大概）不得替数字打底
    道四 未取到与计数：正文写了「未取到／未检索到」的，第三节必须逐条点名它；第四节一行来源都没有＝没有出处

退码：0 全过；1 有发条（详行逐条给码、道名、行号与规格）；2 用法错；3 取值域故障（文件读不到，不读成「零违例」）。
"""

from __future__ import annotations

import argparse
import atexit
import re
import shutil
import sys
import tempfile
from pathlib import Path

TMP_ROOTS = []


@atexit.register
def _cleanup_tmp() -> None:
    for d in TMP_ROOTS:
        shutil.rmtree(d, ignore_errors=True)


def _probe_copy(text: str) -> Path:
    d = Path(tempfile.mkdtemp(prefix='check-brief-', dir=tempfile.gettempdir()))
    TMP_ROOTS.append(d)
    f = d / 'probe.md'
    f.write_text(text, encoding='utf-8')
    return f

SECTIONS = ('一句话结论', '逐条发现', '未取到与口径', '来源')
MARKS = ('AI 整理初稿', '请回原文核对', '不构成投资建议', '判断位 [待人工]')
URL_RE = re.compile(r'https?://|www\.[A-Za-z0-9.-]+')
DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')
ANCHOR_RE = re.compile(r'\[S(\d+)\]\s*$')
MISS_RE = re.compile(r'未取到|未检索到')
PLACEHOLDER_RE = re.compile(r'^\s*(（[^）]*）)?[—\-–]\s*$|待定|待填|TBD|<[^>]*>$')
BANNED = re.compile(r'买入|卖出|建仓|清仓|加仓|目标价|止盈|止损|必涨|必跌|稳赚|无风险|强烈建议|建议持有|翻倍|跑赢大盘')
HEDGE = re.compile(r'约\s*[\d０-９]|左右|大概|大约')
CODES = {'E-FORMAT': '道一 形制', 'E-ANCHOR': '道二 锚', 'E-BANWORD': '道三 红线', 'E-COVERAGE': '道四 未取到与计数'}


def scan(path: Path):
    issues = []
    seen = set()

    def add(code, lane, line_no, msg):
        key = (code, line_no, msg)
        if key not in seen:
            seen.add(key)
            issues.append((code, lane, line_no, msg))

    lines = path.read_text(encoding='utf-8', errors='replace').split('\n')

    head = '\n'.join(lines[:next((i for i, ln in enumerate(lines) if ln.startswith('## ')), len(lines))])
    for need in MARKS:
        if need not in head:
            add('E-FORMAT', '头部', 1, f"头部自标缺『{need}』（规格：四件逐字齐，写在第一个「## 」之前）")

    idxs = []
    for n, name in enumerate(SECTIONS, 1):
        hit = [i for i, ln in enumerate(lines) if re.match(rf'^##\s*{n}、{re.escape(name)}\s*$', ln)]
        if not hit:
            add('E-FORMAT', '四节', 1, f"缺「## {n}、{name}」段（规格：四节齐且按一二三四有序）")
        else:
            idxs.append((n, hit[0]))
    if len(idxs) > 1 and [n for n, _ in idxs] != sorted(n for n, _ in idxs):
        add('E-FORMAT', '四节', idxs[0][1] + 1, '四节次序与契约不一致（规格：一二三四有序）')
    bounds = {}
    for pos, (n, i0) in enumerate(idxs):
        i1 = idxs[pos + 1][1] if pos + 1 < len(idxs) else len(lines)
        bounds[n] = (i0, i1)

    if 1 in bounds:
        i0, i1 = bounds[1]
        body = [ln for ln in lines[i0 + 1:i1] if ln.strip() and not ln.startswith('#')]
        if not body:
            add('E-FORMAT', '结论', i0 + 1, '一句话结论留空（规格：至少一行实句，不留占位）')
        elif any(PLACEHOLDER_RE.search(ln) for ln in body):
            add('E-FORMAT', '结论', i0 + 1 + body.index(next(ln for ln in body if PLACEHOLDER_RE.search(ln))),
                '一句话结论仍是占位（规格：写成可核的实句；判断走第六位的 [待人工]，不靠占位）')

    anchors_used, rows_without = [], []
    if 2 in bounds:
        i0, i1 = bounds[2]
        for i in range(i0 + 1, i1):
            ln = lines[i]
            if not ln.strip().startswith(('-', '*', '|')):
                continue
            m = ANCHOR_RE.search(ln.strip())
            if not m:
                rows_without.append(i + 1)
                add('E-ANCHOR', '锚', i + 1, '发现行行末没有 [S#] 锚（规格：每条发现一行、行末带一个锚；没有锚就不要写进这一节）')
            else:
                anchors_used.append((int(m.group(1)), i + 1))
        for i in range(i0 + 1, i1):
            if HEDGE.search(lines[i]):
                add('E-BANWORD', '改数', i + 1, f"命中改数词「{HEDGE.search(lines[i]).group(0)}」（规格：数值要么照来源写，要么落第三节写未取到，不用约／左右打底）")

    listed = set()
    if 4 in bounds:
        i0, i1 = bounds[4]
        rows = [ln for ln in lines[i0 + 1:i1] if ln.strip().startswith(('-', '*'))]
        if not rows:
            add('E-COVERAGE', '来源', i0 + 1, '第四节一行来源都没有（规格：速览的价值就在这一节，空节等于没有出处）')
        for k, ln in enumerate(rows, 1):
            m = re.match(r'^[-*]\s*\[S(\d+)\]', ln.strip())
            if not m:
                add('E-ANCHOR', '来源', i0 + 1 + lines[i0 + 1:i1].index(ln) + 1,
                    f'来源第 {k} 行不以 [S#] 开头（规格：编号与正文锚一一对应）')
            else:
                listed.add(int(m.group(1)))
            if not URL_RE.search(ln):
                add('E-ANCHOR', '来源', i0 + 1 + lines[i0 + 1:i1].index(ln) + 1,
                    f'来源 [S{m.group(1) if m else k}] 缺 URL（规格：逐条可回查——域名或链接原样写进同一行）')
            if not DATE_RE.search(ln):
                add('E-ANCHOR', '来源', i0 + 1 + lines[i0 + 1:i1].index(ln) + 1,
                    f'来源 [S{m.group(1) if m else k}] 缺检索日 YYYY-MM-DD（规格：多源速览的时效以检索日为凭）')
    else:
        listed = set()
    for num, ln_no in anchors_used:
        if num not in listed:
            add('E-ANCHOR', '锚', ln_no, f'锚 [S{num}] 在第四节没有对应行（规格：正文用的每个编号都要能回到来源行）')

    for i, ln in enumerate(lines, 1):
        m = BANNED.search(ln)
        if m and '[待人工]' not in ln:
            add('E-BANWORD', '判断词', i, f"命中「{m.group(0)}」（规格：评级／目标价／买卖与走势类断言本件不产出；要写就同行挂 [待人工]，或改中性陈述）")

    MISS_WORD = re.compile(r"未取到|未检索到|没取到|没检索到")
    STOP_TOK = {"它", "这", "该", "其", "本节", "来源", "渠道", "本条", "该项", "本次"}
    # 名目「同指」判（M544 打回那格的处置路①）：先把括号注与标点剥掉，再按核心名词短语判——
    # 字面全等算同指；一方含另一方且短的一方 ≥4 字算同指；否则取汉字集合的 Jaccard ≥ SAME_REF_MIN 算同指。
    # 阈值写在这里、由自测的三形钉死（字面全等同指／同指异词同指／真无关不同指），不按文体特例放宽。
    SAME_REF_MIN = 0.6
    PUNCT_STRIP = re.compile(r"[^\u4e00-\u9fa5A-Za-z0-9]")
    def core(tok):
        return PUNCT_STRIP.sub("", re.sub(r"[（(][^）)]*[）)]", "", tok))
    def same_ref(a, b):
        ca, cb = core(a), core(b)
        if not ca or not cb:
            return False
        if ca == cb:
            return True
        if (ca in cb or cb in ca) and min(len(ca), len(cb)) >= 4:
            return True
        sa, sb = set(ca), set(cb)
        return len(sa & sb) / len(sa | sb) >= SAME_REF_MIN
    def refs(tok, pool):
        return any(same_ref(tok, other) for other in pool)
    def miss_tokens(seg_lines):
        out = []
        for off, ln in seg_lines:
            if ln.strip().startswith("#") or not MISS_WORD.search(ln):
                continue
            for m in re.finditer(r"(?:未取到|未检索到|没取到|没检索到)[：:，,\s]*([^\s，。；、：:｜\[\]（）()「」【】\n]{3,24})", ln):
                tok = m.group(1)
                if tok not in STOP_TOK:
                    out.append((tok, off))
            for m in re.finditer(r"([^\s，。；、：:｜\[\]（）()「」【】\n]{3,24}?)(?:未取到|未检索到|没取到|没检索到)", ln):
                tok = m.group(1)
                if tok not in STOP_TOK:
                    out.append((tok, off))
        return out
    body_seg = [(i, lines[i]) for n, (a, b) in bounds.items() if n in (1, 2, 4) for i in range(a + 1, b)]
    sec3_seg = [(i, lines[i]) for i in range(bounds[3][0] + 1, bounds[3][1])] if 3 in bounds else []
    sec3_text = "\n".join(l for _, l in sec3_seg)
    body_text = "\n".join(l for _, l in body_seg)
    body_toks = [tok for tok, _ in miss_tokens(body_seg)]
    sec3_toks = [tok for tok, _ in miss_tokens(sec3_seg)]
    for tok, no in miss_tokens(body_seg):
        if not refs(tok, sec3_toks):
            add("E-COVERAGE", "未取到点名", no + 1,
                f"第三节的点名缺一项：正文写了「{tok}」未取到，第三节没有同指的名目（规格：没列就是没说——逐条点名按名目同指对，不认整节出现过一个「未取到」）")
    for tok, no in miss_tokens(sec3_seg):
        if not refs(tok, body_toks):
            add("E-COVERAGE", "未取到点名", no + 1,
                f"第三节多列一项：「{tok}」在第三节点名为未取到，正文没有同指的这条表述（规格：反向同判——多列与少列都不许）")
    return issues, lines


def run_one(path: Path, quiet=False):
    issues, lines = scan(path)
    codes = sorted({c for c, _, _, _ in issues})
    if not quiet:
        for code, lane, no, msg in issues:
            print(f"  [{code}] [{lane}] 第 {no} 行：{msg}")
    counts = {}
    for code, _, _, _ in issues:
        counts[code] = counts.get(code, 0) + 1
    if issues:
        print(f'FAIL: {path.name}（{len(issues)} 条）')
        print('       ' + '；'.join(f'{CODES[c]} {n} 条' for c, n in sorted(counts.items())))
        print('       码表: ' + '；'.join(f'{c}={CODES[c]}' for c in codes))
        return 1, len(issues), counts
    print(f'PASS: {path.name}（四节齐、自标在位、每条发现带可回锚、来源行齐 URL 与检索日、判断词零命中、未取到逐条点名）')
    print(f'       扫过 {len(lines)} 行，发条 0 条；判定与阈值全集以本脚本现值为准（--help 看四道说明）')
    return 0, 0, {}


def selftest():
    fx = Path(__file__).resolve().parent / 'fixtures'
    cases = [('good-brief.md', 0, None),
             ('bad-no-anchor.md', 1, 'E-ANCHOR'),
             ('bad-missing-section.md', 1, 'E-FORMAT'),
             ('bad-rating-word.md', 1, 'E-BANWORD'),
             ('bad-unsourced.md', 1, 'E-COVERAGE')]
    bad = 0
    gt = (fx / 'good-brief.md').read_text(encoding='utf-8')
    body_line = '- 2025 年报口径的毛利率与本次渠道检索到的季度口径毛利率未互校，未取到同口径对照数 [S3]'
    sec3_line = '- 未取到：同口径毛利率对照数（渠道只给到季度口径，年报为年度口径）；分客户账期未披露'
    assert gt.count(body_line) == 1 and gt.count(sec3_line) == 1, '夹具形制变了，反证档要跟着改'
    probes = []
    # 阈值三形钉死（M544 打回格·处置路①）：字面全等与同指异词都算点到，真无关才算多列
    p0a = gt.replace(sec3_line, '- 未取到：同口径对照数（渠道只给到季度口径，年报为年度口径）')
    probes.append(('钉阈·字面全等（两侧都写「同口径对照数」）不得报多列', p0a, '第三节多列一项', False))
    p0b = gt.replace(sec3_line, '- 未取到：同口径毛利率对照数（渠道只给到季度口径）')
    probes.append(('钉阈·同指异词（正文「同口径对照数」∥第三节「同口径毛利率对照数」）不得报多列', p0b, '第三节多列一项', False))
    p0c = gt.replace(sec3_line, '- 未取到：质押股份比例未取到')
    probes.append(('钉阈·真无关（第三节只列「质押股份比例」）必须报多列', p0c, '第三节多列一项', True))
    p1 = gt.replace(body_line, body_line + '\n- 境外子公司担保余额这条渠道未取到 [S2]')
    probes.append(('反证·正文多写一条未取到而第三节不列｜独有句「第三节的点名缺一项」', p1, '第三节的点名缺一项', True))
    p2 = gt.replace(sec3_line, sec3_line + '；质押股份比例未取到')
    probes.append(('反证·第三节多列一条而正文无｜独有句「第三节多列一项」', p2, '第三节多列一项', True))
    p3 = gt.replace('\n' + body_line, '').replace(sec3_line, '- 口径：产能数字为公司自述的设计产能，非实际产量')
    probes.append(('反证·两处都无这一项时本支不发｜独有句反向断言', p3, '第三节的点名缺一项', False))
    probes.append(('反证·两处都有时本支不发（好样原样）', gt, '第三节多列一项', False))
    import io as _io
    import contextlib as _cl
    for name, txt, needle, want in probes:
        assert txt != gt or not want, '注入自证：反证档必须真改过文本（除好样档）'
        pf = _probe_copy(txt)
        iss_p, _ls_p = scan(pf)
        detail_p = "\n".join(f'[{c}] 第 {no} 行：{msg}' for c, lane, no, msg in iss_p)
        rc_p = 1 if iss_p else 0
        hit = needle in detail_p
        okp = (hit if want else not hit)
        rows = globals().get('_M544_ROWS')
        print(f"  {'ok  ' if okp else 'FAIL'} {name}｜实发{'含' if hit else '不含'}独有句、退码 {rc_p}")
        if not okp:
            bad += 1
    root = Path(tempfile.gettempdir())
    for d in TMP_ROOTS:
        shutil.rmtree(d, ignore_errors=True)
    leftover = sorted(q.name for q in root.iterdir() if q.name.startswith('check-brief-')) if root.is_dir() else []
    print(f"  {'ok  ' if not leftover else 'FAIL'} 临时根自清（跑后不增）｜本次建 {len(TMP_ROOTS)} 枚·跑后残留 {len(leftover)} 枚")
    if leftover:
        bad += 1
    for name, want_rc, want_code in cases:
        p = fx / name
        if not p.is_file():
            print(f'  selftest 取值域故障：夹具不在场 {name}')
            return 3
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc, n, counts = run_one(p, quiet=True)
        detail = buf.getvalue()
        if rc != want_rc:
            print(f'  不合 {name}：期望退码 {want_rc}，实发 {rc}')
            bad += 1
            continue
        if want_code and want_code not in detail:
            print(f'  不合 {name}：期望发码 {want_code}，实发详行不含它')
            bad += 1
            continue
        if want_code is None and bad == 0 and rc == 0:
            print(f'  ok   {name}（退码 {rc}·发条 {n}）')
        elif want_code:
            print(f'  ok   {name}（退码 {rc}·发条 {n}·实发 {want_code}）')
    print('selftest: ' + ('ALL GREEN（好样 1 枚·坏样四道 4/4）' if bad == 0 else f'{bad} 条不合期望'))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(prog='check_brief.py', add_help=False,
                                 description='校一份中文多源研究速览（四道，见 --help 正文）')
    ap.add_argument('target', nargs='?')
    ap.add_argument('--selftest', action='store_true', help='跑包内夹具（好样须过、四枚坏样须各发红）')
    ap.add_argument('--quiet', action='store_true', help='只报末行')
    ap.add_argument('-h', '--help', action='store_true', help='本说明')
    a = ap.parse_args()
    if a.help or (not a.target and not a.selftest):
        print(__doc__)
        return 0 if a.help else 2
    if a.selftest:
        return selftest()
    p = Path(a.target)
    if not p.is_file():
        print(f'取值域故障：读不到速览文件 {p}（不当「零违例」读）')
        return 3
    rc, _, _ = run_one(p, quiet=a.quiet)
    return rc


if __name__ == '__main__':
    sys.exit(main())
