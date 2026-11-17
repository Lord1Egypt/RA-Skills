#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_brief.py — 校验一份「证据表＋简报」是否合 `SKILL.md` 的硬约束（零网络，不发任何请求）。

用法：
    python3 check_brief.py <evidence-table.md> [--brief <brief.md>]   校验一对产物
    python3 check_brief.py --selftest                                  跑包内守护样：好样、坏样与真样例各档，档名与枚数由末行自报
    python3 check_brief.py --help                                      本说明

出口形制（与套件姊妹件同族）：
    失败 = 一行 "FAIL: <文件>（N 条）"，其下每条详行先打错误码前缀（四枚 `E-*` 之一），
           道名后是行号与该道规格；末行 "码表:" 只列本次真正用到的码与含义。
    全过 = 一行 "PASS: <文件>（…）"，并印「扫过行数」与「实测计数」——计数说看到多少，不说猜多少。

四道是什么（判定全集在本脚本，本文只指路，不复述细节）：
    道一 形制：表头七列齐且有序；数据行字段数与表头同数；证据级别在枚举内
    道二 锚：来源列非空非占位；日期列走全格式（YYYY-MM-DD 或 YYYY-MM）
    道三 禁词与混标：来源／主张列禁词族零命中；带自识标记的行不得标 fact；opinion 行不得标「高」
    道四 计数与申报：覆盖度段申报的总行数与三级计数＝表内实测；置信度分布＝表内实测；未覆盖清单必须在场
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = HERE.parent

# 与姊妹件逐字同源的四枚码（第五枚 E-LEDGER 属账本状态机面，本件无账本，故不启用）
E_LEGEND = {
    "E-FORMAT":   "形制/输入/表序不合式→按该行括号内规格改形制后复跑",
    "E-ANCHOR":   "锚/证据链缺失或断链→补合式锚或删除该条,禁虚构",
    "E-BANWORD":  "禁词/评级/幻觉/待人工域命中→改中性陈述或删除,零豁免区",
    "E-COVERAGE": "计数/覆盖/申报对不上→逐类补账或如实标未检索到",
}

HEADER = ['竞品', '维度', '主张', '证据级别', '来源', '日期', '置信度']
LEVELS = ('fact', 'inference', 'opinion')
PRIOR_MARKS = ('prior knowledge', 'inference from training data', '自识', '既有知识')
BANNED_SRC = ('推测', '大概', '应该', '听说', '我觉得', '网传', '据说', '猜', '估计')
PLACEHOLDER_SRC = ('', '-', '—', '待补', 'TBD', 'tbd', 'N/A', 'n/a')
CONF_VALUES = ('高', '中', '低')
DATE_RE = re.compile(r'^\d{4}-(\d{2}-(\d{2}|[0-9A-Za-z?]{2})|\d{2})$')
COV_TOTAL = re.compile(r'证据表总行数|总行数')
COV_LEVEL = re.compile(r'(fact|inference|opinion)[：:\s]*(\d+)')
COV_CONF = re.compile(r'置信度\s*高\s*(\d+)\s*·?\s*中\s*(\d+)\s*·?\s*低\s*(\d+)')
COV_UNCOV = re.compile(r'未覆盖')


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip('|').split('|')]


def table_rows(lines: list[str]) -> tuple[int, list[tuple[int, list[str]]], list[str]]:
    """返回 (表头行号, [(行号, 字段)], 数据行数)。表以首行含「证据级别」为锚定位。"""
    hdr_at, cols = None, []
    rows = []
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s.startswith('|'):
            continue
        cells = split_row(s)
        if hdr_at is None:
            if '证据级别' in cells:
                hdr_at, cols = i, cells
            continue
        if all(re.fullmatch(r':?-{2,}:?', c) for c in cells if c):
            continue
        rows.append((i, cells))
    return hdr_at, rows, cols


def counts(rows: list[list[str]], lvl_i: int, conf_i: int) -> dict:
    c = {k: 0 for k in ('total', 'fact', 'inference', 'opinion', '高', '中', '低', '空')}
    for r in rows:
        c['total'] += 1
        lv = r[lvl_i].strip().lower() if len(r) > lvl_i else ''
        if lv in LEVELS:
            c[lv] += 1
        cf = r[conf_i].strip() if len(r) > conf_i else ''
        if cf in CONF_VALUES:
            c[cf] += 1
        else:
            c['空'] += 1
    return c


def check(path: Path) -> tuple[list[str], int]:
    text = path.read_text(encoding='utf-8', errors='replace')
    lines = text.split('\n')
    nlines = len(lines)
    finds: list[str] = []

    hdr_at, rows, cols = table_rows(lines)
    # 道一 形制
    if hdr_at is None:
        finds.append(f'[E-FORMAT] [道一·形制] 第 1 行：全文找不到含「证据级别」列的表（规格：证据表是本件唯一强制产物，表头须为 {HEADER} 现值）')
        return finds, nlines
    if cols != HEADER:
        finds.append(f'[E-FORMAT] [道一·形制] 第 {hdr_at} 行：表头与现值不合（实得 {cols}，规格 {HEADER}）')
    lvl_i = cols.index('证据级别') if '证据级别' in cols else 3
    src_i = cols.index('来源') if '来源' in cols else 4
    date_i = cols.index('日期') if '日期' in cols else 5
    conf_i = cols.index('置信度') if '置信度' in cols else 6
    if not rows:
        finds.append(f'[E-FORMAT] [道一·形制] 第 {hdr_at} 行：表头在场但零数据行（规格：至少一行主张才可称证据表）')
    for ln, cells in rows:
        if len(cells) != len(cols):
            finds.append(f'[E-FORMAT] [道一·形制] 第 {ln} 行：字段数 {len(cells)} 与表头 {len(cols)} 不等（规格：每行须补齐七列，空值留空而非缺列）')
        lv = cells[lvl_i].strip().lower() if len(cells) > lvl_i else ''
        if lv and lv not in LEVELS:
            finds.append(f'[E-FORMAT] [道一·形制] 第 {ln} 行：证据级别「{cells[lvl_i]}」不在枚举内（规格：判定={list(LEVELS)} 现值）')

    # 道二 锚
    for ln, cells in rows:
        src = cells[src_i].strip() if len(cells) > src_i else ''
        date = cells[date_i].strip() if len(cells) > date_i else ''
        if src in PLACEHOLDER_SRC:
            finds.append(f'[E-ANCHOR] [道二·锚] 第 {ln} 行：来源列为空或占位「{src}」（规格：每行主张须指得回一个出处，禁虚构）')
        if date and not DATE_RE.match(date):
            finds.append(f'[E-ANCHOR] [道二·锚] 第 {ln} 行：日期「{date}」非全格式（规格：YYYY-MM-DD 或 YYYY-MM）')

    # 道三 禁词与混标
    for ln, cells in rows:
        src = cells[src_i] if len(cells) > src_i else ''
        claim = cells[2] if len(cells) > 2 else ''
        lv = cells[lvl_i].strip().lower() if len(cells) > lvl_i else ''
        cf = cells[conf_i].strip() if len(cells) > conf_i else ''
        for w in BANNED_SRC:
            if w in src:
                finds.append(f'[E-BANWORD] [道三·禁词] 第 {ln} 行：来源列含禁词「{w}」（规格：「推测」不是来源；判定={list(BANNED_SRC)} 现值）')
                break
        else:
            for w in BANNED_SRC:
                if w in claim and lv == 'fact':
                    finds.append(f'[E-BANWORD] [道三·禁词] 第 {ln} 行：fact 行主张含禁词「{w}」（规格：直接可证的行不用改数与推测词）')
                    break
        low_src = src.lower()
        if lv == 'fact' and any(m.lower() in low_src for m in PRIOR_MARKS):
            finds.append(f'[E-BANWORD] [道三·混标] 第 {ln} 行：来源带自识标记却标 fact（规格：不得混在 fact 里不标注，此类行应标 inference 或 opinion）')
        if lv == 'opinion' and cf == '高':
            finds.append(f'[E-BANWORD] [道三·混标] 第 {ln} 行：opinion 行置信度标「高」（规格：无可引用来源即不得标「高」，宁可空着）')

    # 道四 计数与申报
    cov_ln = [i for i, l in enumerate(lines, 1) if COV_TOTAL.search(l)]
    if not cov_ln:
        finds.append('[E-COVERAGE] [道四·计数] 第 1 行：找不到覆盖度申报（规格：SKILL §约束4——交付附覆盖度：行数／三级计数／未覆盖维度）')
    else:
        ln0 = cov_ln[0]
        body = '\n'.join(lines[max(0, ln0 - 3):])
        m = re.search(r'(?:证据表总行数|总行数)[：:\s]*(\d+)', body)
        real = counts([c for _, c in rows], lvl_i, conf_i)
        if not m:
            finds.append(f'[E-COVERAGE] [道四·计数] 第 {ln0} 行：覆盖度段没写出总行数数字（规格：行数＝表内数据行实测 {real["total"]}）')
        elif int(m.group(1)) != real['total']:
            finds.append(f'[E-COVERAGE] [道四·计数] 第 {ln0} 行：申报总行数 {m.group(1)} 与表内实测 {real["total"]} 不符（规格：计数对不上即未覆盖事项也可能失真）')
        for lv, n in COV_LEVEL.findall(body):
            if real[lv] != int(n):
                finds.append(f'[E-COVERAGE] [道四·计数] 申报 {lv}={n} 与表内实测 {real[lv]} 不符（规格：三级计数逐类对账，缺类补账）')
        mc = COV_CONF.search(body)
        if mc:
            got = (int(mc.group(1)), int(mc.group(2)), int(mc.group(3)))
            exp = (real['高'], real['中'], real['低'])
            if got != exp:
                finds.append(f'[E-COVERAGE] [道四·计数] 置信度分布申报 {got} 与实测 {exp} 不符（规格：高／中／低三档实测对账；未填者计入不申报位）')
        if not COV_UNCOV.search(body):
            finds.append('[E-COVERAGE] [道四·申报] 覆盖度段缺「未覆盖」清单（规格：什么维度完全没覆盖必须列出，填不满的维度不写进简报）')

    return finds, nlines


def report(path: Path, quiet=False) -> int:
    finds, nlines = check(path)
    if finds:
        print(f"FAIL: {path.name}（{len(finds)} 条）")
        for f in finds:
            print('  - ' + f)
        codes = sorted({re.match(r'\[(E-[A-Z]+)\]', f).group(1) for f in finds})
        print('  码表: ' + '; '.join(f'{c}→{E_LEGEND[c]}' for c in codes))
        return 1
    _, rows, cols = table_rows(path.read_text(encoding='utf-8', errors='replace').split('\n'))
    c = counts([x for _, x in rows], cols.index('证据级别'), cols.index('置信度'))
    print(f"PASS: {path.name}（表头七列、每行带来源与全格式日期、级别在枚举内、覆盖度计数与表内实测对平）")
    if not quiet:
        print(f"       扫过 {nlines} 行，发条 0 条；数据行 {c['total']}（fact {c['fact']}／inference {c['inference']}／opinion {c['opinion']}；置信度 高 {c['高']}／中 {c['中']}／低 {c['低']}／未填 {c['空']}）；判定全集以本脚本现值为准（--help 看四道说明）")
    return 0


GOOD = ['good-full.md', 'good-minimal.md', 'good-prior-knowledge.md', 'good-opinion-uncovered.md']
BAD = ['bad-format.md', 'bad-anchor.md', 'bad-banword.md', 'bad-coverage.md']
EXAMPLE_TABLE = PKG / 'examples' / 'competitive-test' / 'evidence-table.md'
EXAMPLE_BRIEF = PKG / 'examples' / 'competitive-test' / 'brief.md'


def example_tier() -> tuple[bool, int]:
    """真样例档：包内那份随包样例必须过道四，且同批 brief 的申报数与表内实测对平。
       这档的存在意义：样例自己再漂号时 selftest 直接发红，而不是留一句文档说明。"""
    if not EXAMPLE_TABLE.is_file():
        print(f"SELFTEST FAIL: 真样例缺失 {EXAMPLE_TABLE}")
        return False, 0
    finds, nlines = check(EXAMPLE_TABLE)[:2]
    hdr_at, rows, cols = table_rows(EXAMPLE_TABLE.read_text(encoding='utf-8', errors='replace').split('\n'))
    real = counts([c for _, c in rows], cols.index('证据级别'), cols.index('置信度')) if cols else {}
    ok = True
    print(f"selftest 真样例：{EXAMPLE_TABLE.relative_to(PKG)} 扫过 {nlines} 行，发条 {len(finds)} 条（规格 0；实测数据行 {real.get('total')}）")
    for x in finds:
        print('   样例自身未过道四 → ' + x)
        ok = False
    if EXAMPLE_BRIEF.is_file():
        bt = EXAMPLE_BRIEF.read_text(encoding='utf-8', errors='replace')
        m1 = re.search(r'证据表总行数[：:\s]*(\d+)', bt)
        m2 = COV_CONF.search(bt)
        exp = (real.get('高'), real.get('中'), real.get('低'))
        got = (int(m2.group(1)), int(m2.group(2)), int(m2.group(3))) if m2 else None
        if not m1 or int(m1.group(1)) != real.get('total'):
            print(f"selftest 真样例：brief 申报总行数「{m1.group(1) if m1 else '缺'}」与表内实测 {real.get('total')} 不符")
            ok = False
        elif got != exp:
            print(f"selftest 真样例：brief 申报置信度 {got} 与表内实测 {exp} 不符")
            ok = False
        else:
            print(f"selftest 真样例：同批 brief.md 申报（{real['total']} 行·高{exp[0]} 中{exp[1]} 低{exp[2]}）与表内实测对平")
    else:
        print(f"selftest 真样例：同批 brief 缺失 {EXAMPLE_BRIEF}——该档按未过处理")
        ok = False
    return ok, real.get('total', 0)


def selftest() -> int:
    want_bad = {'bad-format.md': 'E-FORMAT', 'bad-anchor.md': 'E-ANCHOR',
                'bad-banword.md': 'E-BANWORD', 'bad-coverage.md': 'E-COVERAGE'}
    ok = True
    n_good_pass = 0
    for name in GOOD:
        f = HERE / 'fixtures' / name
        if not f.is_file():
            print(f"SELFTEST FAIL: 守护样缺失 {f}")
            return 1
        finds, nlines = check(f)
        print(f"selftest 好样：{name} 扫过 {nlines} 行，发条 {len(finds)} 条（规格 0）")
        for x in finds:
            print('   意外发条 → ' + x)
            ok = False
        if not finds:
            n_good_pass += 1
    got_codes = set()
    for name, code in want_bad.items():
        f = HERE / 'fixtures' / name
        if not f.is_file():
            print(f"SELFTEST FAIL: 守护样缺失 {f}")
            return 1
        finds, nlines = check(f)
        codes = {re.match(r'\[(E-[A-Z]+)\]', x).group(1) for x in finds} if finds else set()
        got_codes |= codes
        spec = '规格 ≥1 条且必发 ' + code
        if not finds:
            print(f"selftest 坏样：{name} 扫过 {nlines} 行，发条 0 条（{spec}）→ 未发红，鉴别力失效")
            ok = False
        elif code not in codes:
            print(f"selftest 坏样：{name} 扫过 {nlines} 行，发条 {len(finds)} 条（{spec}）→ 实发 {sorted(codes)}")
            ok = False
        else:
            print(f"selftest 坏样：{name} 扫过 {nlines} 行，发条 {len(finds)} 条（{spec}）→ 命中 {code}")
    want = set(E_LEGEND)
    missing = sorted(want - got_codes)
    if missing:
        print('   四道未全发 → ' + ', '.join(missing))
        ok = False
    ex_ok, ex_rows = example_tier()
    ok = ok and ex_ok
    print(f"selftest: {'ALL GREEN' if ok else 'FAIL'}（好样 {n_good_pass}/{len(GOOD)} · 坏样四道 {len(got_codes)}/{len(want)} · 真样例档 {'过' if ex_ok else '未过'}／实测 {ex_rows} 行）")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="校验一份证据表（可带简报）是否合本件硬约束（零网络）。",
        epilog="出口：FAIL 一行计数＋逐条 E-* 详行＋码表；PASS 一行＋扫过与实测计数。判定全集在本脚本现值。")
    ap.add_argument('table', nargs='?', help='待校验的证据表（markdown）')
    ap.add_argument('--brief', help='同批简报（可选；覆盖度申报在读入文件内判）')
    ap.add_argument('--selftest', action='store_true', help='跑包内守护样：好样、坏样与真样例各档，档名与枚数由末行自报')
    ap.add_argument('--quiet', action='store_true', help='PASS 行不带计数附注')
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.table:
        ap.error('缺参数：给一个证据表文件，或用 --selftest')
    p = Path(args.table)
    if not p.is_file():
        print(f"[出错] 文件不存在：{p}")
        return 1
    rc = report(p, quiet=args.quiet)
    if args.brief:
        b = Path(args.brief)
        if not b.is_file():
            print(f"[出错] 文件不存在：{b}")
            return 1
        rc = max(rc, report(b, quiet=args.quiet))
    return rc


if __name__ == '__main__':
    sys.exit(main())
