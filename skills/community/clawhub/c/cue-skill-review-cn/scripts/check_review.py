#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_review.py — 校一份「skill 体检报告」是否合 `SKILL.md` §3 五节契约与 §5 红线。

用法：
    python3 check_review.py <报告.md>            校一份报告（纯标准库、零网络、不发任何请求）
    python3 check_review.py --selftest           跑包内夹具：好样必须过，五枚坏样必须各发它该发的那一道
    python3 check_review.py --help               本说明

出口形制（与套件姊妹件同族）：
    失败 = 一行 "FAIL: <文件>（N 条）"，其下每条详行先打错误码前缀，道名后是行号与该道规格；末行「码表:」只列本次真正用到的码。
    全过 = 一行 "PASS: <文件>（…）"，并印「扫过 N 行」与五道计数——计数说看到多少，不说猜多少。

五道（判定全集在本脚本，本文只指路）：
    道一 形制 E-FORMAT   ：头部四件自标逐字在位；五节齐且有序；结论位不得写成装／不装的断言（要写只能挂 [待人工]）
    道二 锚   E-ANCHOR   ：每条发现行行末带 [S#]；该编号在第五节有对应行；来源行必须同时带 定位（文件:行号 或 URL）与检索日 YYYY-MM-DD
    道三 判决词 E-BANWORD：安全／无风险／可放心装／建议安装／一定可用 一类断言零命中，同行挂 [待人工] 才放行
    道四 覆盖 E-COVERAGE ：五个检查面（声明层／前置层／面文承诺／样例是否真跑通／许可与出处行）各须至少一条挂锚发现，或在第四节逐条点名未取到；第三节是方法自述，不算覆盖证据
    道五 真跑申报 E-VERIFY：报告里写「真跑通／跑过」的那条必须附那条命令与它这次的退码（形如 cmd=… rc=N），没有命令与退码就是没跑

退码：0 全过；1 有发条；2 用法错；3 取值域故障（文件读不到，不读成「零违例」）。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SECTIONS = ('被检对象', '逐条发现', '五个检查面', '未取到与口径', '来源')
MARKS = ('AI 整理初稿', '请回原文核对', '不构成上架或安装建议', '判断位 [待人工]')
FACES = ('声明层', '前置层', '面文承诺', '样例真跑', '许可与出处')
ANCHOR_RE = re.compile(r'\[S(\d+)\]\s*$')
URL_RE = re.compile(r'https?://|www\.[A-Za-z0-9.-]+')
LOC_RE = re.compile(r'[A-Za-z0-9_./-]+:\d+|https?://\S+|www\.\S+')
DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')
RUNWORD_RE = re.compile(r'真跑通|跑过|实跑过|真跑了一遍')
RC_RE = re.compile(r'cmd=.+?rc=\d+')
VERDICT_RE = re.compile(r'可放心装|建议安装|建议上架|一定可用|肯定没问题|安全无害|无风险可装|不会有问题')
PLACE_RE = re.compile(r'\[待人工\]')


def scan(path: Path):
    issues = []
    seen = set()

    def add(code, lane, no, msg):
        key = (code, no, msg)
        if key in seen:
            return
        seen.add(key)
        issues.append((code, lane, no, msg))

    lines = path.read_text(encoding='utf-8', errors='replace').split('\n')
    head_end = next((i for i, l in enumerate(lines) if l.startswith('## ')), len(lines))
    head = '\n'.join(lines[:head_end])
    for need in MARKS:
        if need not in head:
            add('E-FORMAT', '头部', 1, f"头部自标缺『{need}』（规格：四件逐字齐，写在第一个「## 」之前）")

    idxs = []
    for n, name in enumerate(SECTIONS, 1):
        hit = [i for i, l in enumerate(lines) if re.match(r'^##\s*%d、%s' % (n, re.escape(name)), l)]
        if not hit:
            add('E-FORMAT', '五节', 1, f"缺「## {n}、{name}」节（规格：五节齐且按一二三四五有序）")
        else:
            idxs.append((n, hit[0]))
    bounds = {}
    for pos in range(len(idxs)):
        n, i0 = idxs[pos]
        i1 = idxs[pos + 1][1] if pos + 1 < len(idxs) else len(lines)
        bounds[n] = (i0, i1)

    listed = {}
    if 5 in bounds:
        i0, i1 = bounds[5]
        rows = [(i + 1, lines[i].strip()) for i in range(i0 + 1, i1) if lines[i].strip().startswith(('-', '*'))]
        if not rows:
            add('E-COVERAGE', '来源', i0 + 1, '第五节一行来源都没有（规格：体检报告的价值就在这一节，空节等于每条都回不去）')
        for no, ln in rows:
            m = re.match(r'^[-*]\s*\[S(\d+)\]', ln)
            if not m:
                add('E-ANCHOR', '来源', no, '来源行不以 [S#] 开头（规格：编号与正文锚一一对应）')
            else:
                listed[int(m.group(1))] = no
            if not DATE_RE.search(ln):
                add('E-ANCHOR', '来源', no, '来源行缺检索日 YYYY-MM-DD（规格：体检读的是那一刻的面文，隔一天可能就不同）')
            if not LOC_RE.search(ln):
                add('E-ANCHOR', '来源', no, '来源行既无 URL 也无 文件:行号 定位（规格：每条都要能回到一处原文）')

    covered = {f: False for f in FACES}
    if 2 in bounds:
        i0, i1 = bounds[2]
        for i in range(i0 + 1, i1):
            s = lines[i].strip()
            if not s.startswith('- '):
                continue
            m = ANCHOR_RE.search(s)
            if not m:
                add('E-ANCHOR', '锚', i + 1, '发现行行末没有 [S#] 锚（规格：没有锚的发现不要写进这一节）')
            elif int(m.group(1)) not in listed:
                add('E-ANCHOR', '锚', i + 1, f"锚 [S{m.group(1)}] 在第五节没有对应行（规格：正文用的每个编号都要能回到来源行）")
            for f in FACES:
                if f in s:
                    covered[f] = True
            if RUNWORD_RE.search(s) and not RC_RE.search(s):
                add('E-VERIFY', '真跑申报', i + 1, '写了真跑通却没附那条命令与它这次的退码（规格：cmd=… rc=N 同一行给出；跑过就印得出，跑不了就别写）')
    if 4 in bounds:
        i0, i1 = bounds[4]
        for i in range(i0 + 1, i1):
            s = lines[i].strip()
            if not s.startswith('- '):
                continue
            for f in FACES:
                if f in s:
                    covered[f] = True
    for f, hit in covered.items():
        if not hit:
            add('E-COVERAGE', '检查面', 1, f"检查面「{f}」既无挂锚发现也无未取到点名（规格：五个面各自要么在第二节有一条带 [S#] 的发现，要么在第四节写明未取到；第三节自述不算证据）")

    for i, ln in enumerate(lines, 1):
        m = VERDICT_RE.search(ln)
        if m and not PLACE_RE.search(ln):
            add('E-BANWORD', '判决词', i, f"命中「{m.group(0)}」（规格：本件只交付能回到原文的事实，装或不装是人的判断；要写就同行挂 [待人工]）")
    if 1 in bounds:
        i0, i1 = bounds[1]
        for i in range(i0 + 1, i1):
            if '装' in lines[i] and not PLACE_RE.search(lines[i]) and not lines[i].startswith(('#', '本页', '|')):
                add('E-BANWORD', '结论位', i + 1, '被检对象节里出现对「装不装」的表态且没挂 [待人工]（规格：这一节只登记对象与版本，判断走第五节前先归人）')
    return issues, lines


def run_one(path: Path, quiet=False):
    issues, lines = scan(path)
    codes = sorted({c for c, _, _, _ in issues})
    counts = {}
    for c, _, _, _ in issues:
        counts[c] = counts.get(c, 0) + 1
    if not quiet:
        for code, lane, no, msg in issues:
            print(f"  [{code}] [{lane}] 第 {no} 行：{msg}")
    if issues:
        print(f'FAIL: {path.name}（{len(issues)} 条）')
        print('       ' + '；'.join(f'{c} {n} 条' for c, n in sorted(counts.items())))
        print('       码表: ' + '；'.join(f'{c}={codes_doc[c]}' for c in codes))
        return 1, len(issues)
    print(f'PASS: {path.name}（五节齐、自标在位、每条发现可回到一处原文、五个检查面全覆盖、真跑申报带命令与退码、判决词零命中）')
    print(f'       扫过 {len(lines)} 行，发条 0 条；判定与阈值全集以本脚本现值为准（--help 看五道说明）')
    return 0, 0


codes_doc = {'E-FORMAT': '道一 形制', 'E-ANCHOR': '道二 锚与定位', 'E-BANWORD': '道三 判决词',
             'E-COVERAGE': '道四 检查面与来源覆盖', 'E-VERIFY': '道五 真跑申报'}


def selftest():
    fx = Path(__file__).resolve().parent / 'fixtures'
    cases = [('good-review.md', 0, None),
             ('bad-format.md', 1, 'E-FORMAT'),
             ('bad-no-anchor.md', 1, 'E-ANCHOR'),
             ('bad-unverified-claim.md', 1, 'E-VERIFY'),
             ('bad-safety-verdict.md', 1, 'E-BANWORD'),
             ('bad-missing-face.md', 1, 'E-COVERAGE')]
    bad = 0
    import contextlib
    import io
    for name, want_rc, want_code in cases:
        p = fx / name
        if not p.is_file():
            print(f'  取值域故障：夹具不在场 {name}（不读成「零违例」）')
            return 3
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc, _ = run_one(p, quiet=True)
        detail = buf.getvalue()
        if rc != want_rc:
            print(f'  不合 {name}：期望退码 {want_rc}，实发 {rc}')
            bad += 1
            continue
        if want_code and want_code not in detail:
            print(f'  不合 {name}：期望发码 {want_code}，实发详行不含它')
            bad += 1
            continue
        codes = sorted(set(re.findall(r'E-[A-Z]+', detail)))
        if want_code and codes != [want_code]:
            print('  不合 %s：期望只发 %s，实发码集=%s（多发的道说明这枚坏样不单一，少发说明这一道量不到了）'
                  % (name, want_code, '、'.join(codes) or '无'))
            bad += 1
            continue
        print('  ok   %s（退码 %d·期望 %s·实发码 %s）'
              % (name, rc, want_code or '全过', '、'.join(codes) or '无'))
    print('selftest: ' + ('ALL GREEN（好样 1 枚·坏样五枚各只发它该发的那一道 5/5·逐枚发码见上）'
                          if bad == 0 else '%d 条不合预期' % bad))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(prog='check_review.py', add_help=False)
    ap.add_argument('target', nargs='?')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--quiet', action='store_true')
    ap.add_argument('-h', '--help', action='store_true')
    a = ap.parse_args()
    if a.help or (not a.target and not a.selftest):
        print(__doc__)
        return 0 if a.help else 2
    if a.selftest:
        return selftest()
    p = Path(a.target)
    if not p.is_file():
        print(f'取值域故障：读不到报告文件 {p}（不当「零违例」读）')
        return 3
    rc, _ = run_one(p, quiet=a.quiet)
    return rc


if __name__ == '__main__':
    sys.exit(main())
