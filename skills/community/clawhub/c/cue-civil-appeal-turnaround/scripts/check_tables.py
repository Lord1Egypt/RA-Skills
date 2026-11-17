#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_tables.py — 校验案件工作目录里的两张核心表是否合 `SKILL.md` 八条硬约束与「交付前自检」（零网络）。

用法：
    python3 check_tables.py <事实台账.md> [败诉三面表.md ...]   校验一个案件目录里的表（可多份）
    python3 check_tables.py --selftest                          跑包内八件守护样（好样 4＋坏样 4）
    python3 check_tables.py --help                              本说明

出口形制（与套件姊妹件同族）：
    失败 = 一行 "FAIL: <文件>（N 条）"，其下每条详行先打错误码前缀（四枚 `E-*` 之一），
           道名后是行号与该道规格；末行 "码表:" 只列本次真正用到的码与含义。
    全过 = 一行 "PASS: <文件>（…）"，并印「扫过行数」与「实测计数」——计数说看到多少，不说猜多少。

四道是什么（判定全集在本脚本，本文只指路，不复述细节）：
    道一 形制：表头与 `assets/` 模板列头逐字同（现值见 TEMPLATES）；每数据行字段数与表头同数
    道二 锚与等级：台账每行「来源」非空；「等级」在 A/B/C 枚举内（硬约束 2——禁止把 C 当 A 用）
    道三 禁预断：码内禁词族零命中（硬约束 3）；C 级行须带「待核实」标注；判语已定式与等级冲突即发
    道四 计数与申报：文内「共 N 条」申报与表内实测对账（交付前自检第 1 条）；法条/条号行须标「递交前核对」（第 2 条）
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = HERE.parent

# 与姊妹件逐字同源的四枚码（第五枚 E-LEDGER 属账本状态机面，本件台账非状态机账本，故不启用）
E_LEGEND = {
    "E-FORMAT":   "形制/输入/表序不合式→按该行括号内规格改形制后复跑",
    "E-ANCHOR":   "锚/证据链缺失或断链→补合式锚或删除该条,禁虚构",
    "E-BANWORD":  "禁词/评级/幻觉/待人工域命中→改中性陈述或删除,零豁免区",
    "E-COVERAGE": "计数/覆盖/申报对不上→逐类补账或如实标未检索到",
}

# 表头逐字取自本包模板现值（assets/），不另立第二份事实源
TEMPLATES = {
    '事实台账': ['来源（文件 + 页码/时点）', '等级', '已用于哪些文书', '纪律备注'],
    '败诉三面表': ['事实', '为何天然不利', '出处等级（A/B/C）', '处置'],
}
GRADE_COL = re.compile(r'^(A|B|C)$')
GRADES = ('A', 'B', 'C')
# 硬约束 3「不预断、不虚构、不推断」——禁词族全集在本现值，成品面只指路不复述
PREJUDGE = ('保证改判', '必然胜诉', '一定赢', '稳赢', '肯定能赢', '百分百', '绝对赢', '包赢')
C_NEEDED = ('待核实', '待核', '未取得', '未调取')
ARTICLE_RE = re.compile(r'(第[零〇一二三四五六七八九十百千0-9]+条|《[^》]{2,20}》)')
DECLARE_RE = re.compile(r'共\s*(\d+)\s*条')
CHECK_MARK = '递交前核对'


def which_kind(path: Path, lines: list[str]) -> str | None:
    for k, cols in TEMPLATES.items():
        if any(all(c in line for c in cols) and line.strip().startswith('|') for line in lines):
            return k
    return None


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip('|').split('|')]


def data_rows(lines: list[str], need: list[str]) -> tuple[int | None, list[str], list[tuple[int, list[str]]]]:
    hdr_at = None
    cols: list[str] = []
    rows: list[tuple[int, list[str]]] = []
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if hdr_at is None:
            if s.startswith('|') and all(c in s for c in need):
                hdr_at, cols = i, split_row(s)
            continue
        if not s.startswith('|'):
            if rows:
                break          # 表块以第一处非表格行收尾（模板里的说明段与例示行不计入本表）
            continue
        cells = split_row(s)
        if cells and all(re.fullmatch(r':?-{2,}:?', c) for c in cells if c):
            continue
        rows.append((i, cells))
    return hdr_at, cols, rows


def check(path: Path) -> tuple[list[str], int, dict]:
    lines = path.read_text(encoding='utf-8', errors='replace').split('\n')
    nlines = len(lines)
    finds: list[str] = []
    kind = which_kind(path, lines)
    if kind is None:
        return ([f'[E-FORMAT] [道一·形制] 第 1 行：全文找不到与本包任一模板列头同名的表（规格：可判表种={list(TEMPLATES)} 现值）'],
                nlines, {})

    hdr_at, cols, rows = data_rows(lines, TEMPLATES[kind])
    # 道一 形制
    missing_cols = [c for c in TEMPLATES[kind] if c not in cols]
    if missing_cols:
        finds.append(f'[E-FORMAT] [道一·形制] 第 {hdr_at} 行：表头缺列 {missing_cols}（规格：与 assets/ 模板列头逐字同）')
    if not rows:
        finds.append(f'[E-FORMAT] [道一·形制] 第 {hdr_at} 行：表头在场但零数据行（规格：空模板不作为交付物）')
    for ln, cells in rows:
        if len(cells) != len(cols):
            finds.append(f'[E-FORMAT] [道一·形制] 第 {ln} 行：字段数 {len(cells)} 与表头 {len(cols)} 不等（规格：空值留空而非缺列）')

    def col(sub: str) -> int:
        for i, c in enumerate(cols):
            if sub in c:
                return i
        return -1

    src_i, grade_i = (col('来源'), col('等级')) if kind == '事实台账' else (col('出处等级') * 0 + col('出处等级'), col('出处等级'))
    if kind == '败诉三面表':
        src_i = -1
    # 道二 锚与等级
    for ln, cells in rows:
        g = cells[grade_i].strip() if 0 <= grade_i < len(cells) else ''
        gm = GRADE_COL.match(g)
        if not gm:
            finds.append(f'[E-ANCHOR] [道二·等级] 第 {ln} 行：等级列「{g}」不在枚举内（规格：判定={list(GRADES)} 现值——硬约束 2 三级 A/B/C）')
        if kind == '事实台账' and src_i >= 0:
            src = cells[src_i].strip() if src_i < len(cells) else ''
            if src in ('', '-', '—', '略', '同上'):
                finds.append(f'[E-ANCHOR] [道二·来源] 第 {ln} 行：来源列为空或占位「{src}」（规格：每行须指回文件+页码/时点，禁虚构）')
    # 道三 禁预断
    body = '\n'.join(lines)
    for ln, line in enumerate(lines, 1):
        for w in PREJUDGE:
            if w in line:
                finds.append(f'[E-BANWORD] [道三·禁预断] 第 {ln} 行：命中禁词「{w}」（规格：硬约束 3——不预断、不虚构、不推断；词族全集在码内现值）')
                break
    for ln, cells in rows:
        g = cells[grade_i].strip() if 0 <= grade_i < len(cells) else ''
        joined = ' '.join(cells)
        if g == 'C' and not any(k in joined for k in C_NEEDED):
            finds.append(f'[E-BANWORD] [道三·待核实标注] 第 {ln} 行：C 级行未带「待核实/待核/未取得/未调取」任一句（规格：未核实事项一律标注，禁写入文书）')
        if g == 'C' and '判决已认定' in joined:
            finds.append(f'[E-BANWORD] [道三·混级] 第 {ln} 行：C 级却写「判决已认定」（规格：硬约束 2——禁止把 C 当 A 用）')
    # 道四 计数与申报
    real = len(rows)
    for ln, line in enumerate(lines, 1):
        m = DECLARE_RE.search(line)
        if m and int(m.group(1)) != real:
            finds.append(f'[E-COVERAGE] [道四·计数] 第 {ln} 行：申报「共 {m.group(1)} 条」与表内实测 {real} 不符（规格：交付前自检第 1 条——逐条带等级并核对条数）')
        if ARTICLE_RE.search(line) and line.strip().startswith('|') and CHECK_MARK not in line and '条号' not in line:
            finds.append(f'[E-COVERAGE] [道四·申报] 第 {ln} 行：行内引用条号/法规名却未标「{CHECK_MARK}」（规格：交付前自检第 2 条——每一处条号都要标注）')
    counts = {'kind': kind, 'rows': real,
              'A': sum(1 for _, c in rows if 0 <= grade_i < len(c) and c[grade_i].strip() == 'A'),
              'B': sum(1 for _, c in rows if 0 <= grade_i < len(c) and c[grade_i].strip() == 'B'),
              'C': sum(1 for _, c in rows if 0 <= grade_i < len(c) and c[grade_i].strip() == 'C')}
    return finds, nlines, counts


def report(path: Path, quiet=False) -> int:
    finds, nlines, c = check(path)
    if finds:
        print(f"FAIL: {path.name}（{len(finds)} 条）")
        for f in finds:
            print('  - ' + f)
        codes = sorted({re.match(r'\[(E-[A-Z]+)\]', f).group(1) for f in finds})
        print('  码表: ' + '; '.join(f'{x}→{E_LEGEND[x]}' for x in codes))
        return 1
    print(f"PASS: {path.name}（表头同模板、每行带等级{'与来源' if c.get('kind') == '事实台账' else ''}、无预断词、条数与条号申报就位）")
    if not quiet and c:
        print(f"       扫过 {nlines} 行，发条 0 条；表种＝{c['kind']}，数据行 {c['rows']}（A {c['A']}／B {c['B']}／C {c['C']}）；判定全集以本脚本现值为准（--help 看四道说明）")
    return 0


GOOD = ['good-ledger.md', 'good-threefaces.md', 'good-ledger-c-waiting.md', 'good-threefaces-mixed.md']
BAD = ['bad-format.md', 'bad-anchor.md', 'bad-banword.md', 'bad-coverage.md']


def selftest() -> int:
    want_bad = {'bad-format.md': 'E-FORMAT', 'bad-anchor.md': 'E-ANCHOR',
                'bad-banword.md': 'E-BANWORD', 'bad-coverage.md': 'E-COVERAGE'}
    ok, npass = True, 0
    for name in GOOD:
        f = HERE / 'fixtures' / name
        if not f.is_file():
            print(f"SELFTEST FAIL: 守护样缺失 {f}")
            return 1
        finds, nlines, _ = check(f)
        print(f"selftest 好样：{name} 扫过 {nlines} 行，发条 {len(finds)} 条（规格 0）")
        for x in finds:
            print('   意外发条 → ' + x)
            ok = False
        if not finds:
            npass += 1
    got: set[str] = set()
    for name, code in want_bad.items():
        f = HERE / 'fixtures' / name
        if not f.is_file():
            print(f"SELFTEST FAIL: 守护样缺失 {f}")
            return 1
        finds, nlines, _ = check(f)
        codes = {re.match(r'\[(E-[A-Z]+)\]', x).group(1) for x in finds} if finds else set()
        got |= codes
        spec = '规格 ≥1 条且必发 ' + code
        if not finds:
            print(f"selftest 坏样：{name} 扫过 {nlines} 行，发条 0 条（{spec}）→ 未发红，鉴别力失效")
            ok = False
        elif code not in codes:
            print(f"selftest 坏样：{name} 扫过 {nlines} 行，发条 {len(finds)} 条（{spec}）→ 实发 {sorted(codes)}")
            ok = False
        else:
            print(f"selftest 坏样：{name} 扫过 {nlines} 行，发条 {len(finds)} 条（{spec}）→ 命中 {code}")
    missing = sorted(set(E_LEGEND) - got)
    if missing:
        print('   四道未全发 → ' + ', '.join(missing))
        ok = False
    print(f"selftest: {'ALL GREEN' if ok else 'FAIL'}（好样 {npass}/{len(GOOD)} · 坏样四道 {len(got)}/{len(E_LEGEND)}）")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="校验案件工作目录里的核心表是否合本件八条硬约束与交付前自检（零网络）。",
        epilog="出口：FAIL 一行计数＋逐条 E-* 详行＋码表；PASS 一行＋扫过与实测计数。判定全集在本脚本现值。")
    ap.add_argument('tables', nargs='*', help='待校验的表文件（一个或多个）')
    ap.add_argument('--selftest', action='store_true', help='跑包内八件守护样：好样 4 须全过、坏样 4 须各点一道')
    ap.add_argument('--quiet', action='store_true', help='PASS 行不带计数附注')
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.tables:
        ap.error('缺参数：给至少一个表文件，或用 --selftest')
    rc = 0
    for t in args.tables:
        p = Path(t)
        if not p.is_file():
            print(f"[出错] 文件不存在：{p}")
            rc = max(rc, 1)
            continue
        rc = max(rc, report(p, quiet=args.quiet))
    return rc


if __name__ == '__main__':
    sys.exit(main())
