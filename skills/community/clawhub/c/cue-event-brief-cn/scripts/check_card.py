#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_card.py — 校验一张「公告事件速读卡」是否合 `SKILL.md` §3 五段契约与 §5 红线。

用法：
    python3 check_card.py <卡.md>          校验一张卡（默认零网络，不发任何请求）
    python3 check_card.py --selftest       跑包内两件夹具：好样必须过，坏样四道必须全发
    python3 check_card.py --help           本说明

出口形制（与套件姊妹件同族）：
    失败 = 一行 "FAIL: <文件>（N 条）"，其下每条详行**先打错误码前缀**（四枚 `E-*` 之一），
           道名后是行号与该道规格；末行 "码表:" 只列本次真正用到的码与含义。
    全过 = 一行 "PASS: <文件>（…）"，并印「扫过行数」与「各道计数」——计数说看到多少，不说猜多少。

四道是什么（判定全集在本脚本，本文只指路，不复述细节）：
    道一 形制：头部自标三件套＋披露日/数据日/来源三要素＋五段齐且有序＋类型单选与判定句已填
    道二 锚与依据：关键数每行带出处锚；影响链每条带「← 依据：」且依据非占位
    道三 红线：禁词表零命中；关键数不得写「约/左右」这类改数；评级·目标价·走势只能挂 [待人工]
    道四 计数与申报：影响链至多三条；同类对照要么列行要么声明；待核清单必须有 [待人工] 汇总位
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

SECTIONS = ['事件类型判定', '关键数快表', '影响链候选', '同类对照', '待核清单']
CN_NUM = ['一', '二', '三', '四', '五']
BANWORDS = ('必涨', '稳赚', '零风险', '保证收益', '强烈推荐', '稳赢', '无风险')
HEDGE = ('约', '左右', '近似', '大概')
JUDGE_WORDS = ('评级', '目标价', '走势')
ANCHOR_PAT = re.compile(r'(?:[页段行]|P|§|¶)\s*\d+|\d+\s*(?:页|段|行)')
PLACEHOLDER = re.compile(r'_{2,}|\ {\d}|\t{2,}')


def is_blank_cell(s: str) -> bool:
    s = s.strip()
    return (not s) or set(s) <= {'-', ' ', '-'} or '__' in s or bool(PLACEHOLDER.search(s)) or s in {'☐', '－', '—'}


def split_row(line: str):
    core = line.strip().strip('|')
    return [c.strip() for c in core.split('|')]


def section_ranges(lines):
    """返回 {段名: (起, 止)}；止为该段末行（下一 H2 前）。找不到即缺段。"""
    heads = {}
    for i, ln in enumerate(lines):
        m = re.match(r'^##\s+([一二三四五六七八九])、(.+?)\s*$', ln)
        if m:
            heads.setdefault(m.group(2).strip(), i)
    out = {}
    order = sorted(heads.values())
    for name, idx in heads.items():
        nxt = min([o for o in order if o > idx], default=len(lines))
        out[name] = (idx, nxt)
    return out


def check(path: Path):
    text = path.read_text(encoding='utf-8')
    lines = text.split('\n')
    finds = []

    def add(code, lane, lineno, detail):
        finds.append(f"[{code}] [{lane}] 第 {lineno} 行：{detail}")

    # ---- 道一：形制 ----
    head_i = [i for i, ln in enumerate(lines) if ln.strip() == '## 头部自标']
    if not head_i:
        add('E-FORMAT', '头部', 1, "缺「## 头部自标」段（规格：该段须存在，且含『AI 整理初稿』『不构成投资建议』『回原文核对』三件套）")
    else:
        i0 = head_i[0]
        i1 = min([i for i, ln in enumerate(lines) if i > i0 and ln.startswith('## ')], default=len(lines))
        blob = '\n'.join(lines[i0:i1])
        for need in ('AI 整理初稿', '不构成投资建议', '回原文核对'):
            if need not in blob:
                add('E-FORMAT', '头部', i0 + 1, f"头部自标缺『{need}』（规格：三件套逐字齐）")
        for key, spec in (('披露日', 'YYYY-MM-DD'), ('数据日', 'YYYY-MM-DD'), ('来源', '官方 URL 或文件名＋定位')):
            hit = [j for j in range(i0, i1) if key in lines[j]]
            if not hit:
                add('E-FORMAT', '时点', i0 + 1, f"头部缺「{key}」行（规格：{spec}）")
            else:
                vals = []
                for j in hit:
                    m = re.search(rf'{key}[：:]\s*([^\u3000\n]*)', lines[j])
                    vals.append(m.group(1) if m else '')
                if all(is_blank_cell(v) for v in vals):
                    add('E-FORMAT', '时点', hit[0] + 1, f"「{key}」留空或仍是占位（规格：{spec}；披露日≠用户所指日期时须明说）")

    secs = section_ranges(lines)
    for n, name in zip(CN_NUM, SECTIONS):
        if name not in secs:
            add('E-FORMAT', '五段', 1, f"缺「## {n}、{name}」段（规格：五段齐且按一二三四五有序）")
    if all(s in secs for s in SECTIONS):
        idxs = [secs[s][0] for s in SECTIONS]
        if idxs != sorted(idxs):
            add('E-FORMAT', '五段', idxs[0] + 1, "五段次序与契约不一致（规格：判定→关键数→影响链→同类对照→待核）")
        i0, i1 = secs['事件类型判定']
        blob = '\n'.join(lines[i0:i1])
        if '☑' not in blob:
            add('E-FORMAT', '类型', i0 + 1, "类型单选未勾选（规格：表中恰选一类，勾选写作 ☑）")
        elif blob.count('☑') > 1:
            add('E-FORMAT', '类型', i0 + 1, f"类型勾选 {blob.count('☑')} 处（规格：单选）")
        judge = [j for j in range(i0, i1) if lines[j].startswith('判定句')]
        if not judge:
            add('E-FORMAT', '类型', i0 + 1, "缺判定句行（规格：以「判定句：」起头，照原文标题写）")
        else:
            jline = lines[judge[0]]
            tail = jline.split('：', 1)[-1] if '：' in jline else ''
            if not tail.strip() or is_blank_cell(tail):
                add('E-FORMAT', '类型', judge[0] + 1, "判定句未填（规格：照原文标题，不加工；选「其他」须附归类理由）")

    # ---- 道二：锚与依据 ----
    if '关键数快表' in secs:
        i0, i1 = secs['关键数快表']
        for j in range(i0, i1):
            ln = lines[j]
            if not ln.strip().startswith('|'):
                continue
            cells = split_row(ln)
            if len(cells) < 3 or cells[0] in {'#', '---'} or set(cells[0]) <= {'-'}:
                continue
            val, anchor = cells[1], cells[2] if len(cells) > 2 else ''
            if is_blank_cell(val):
                continue
            if is_blank_cell(anchor) or not ANCHOR_PAT.search(anchor):
                add('E-ANCHOR', '关键数', j + 1, f"该行有关键数无出处锚（锚样：页／段／行＋数字；规格：无锚则删行，不许补猜）")

    if '影响链候选' in secs:
        i0, i1 = secs['影响链候选']
        cand = [(j, lines[j]) for j in range(i0, i1) if '候选' in lines[j] and '←' in lines[j]]
        for j, ln in cand:
            if '依据' not in ln:
                add('E-ANCHOR', '依据', j + 1, "影响链候选未带「← 依据：」（规格：依据＝公告原文逐字段落 或 可核数据通道现值；无依据不写）")
            else:
                tail = ln.split('依据', 1)[-1].lstrip('：:').strip()
                if is_blank_cell(tail) or not tail.strip('-— '):
                    add('E-ANCHOR', '依据', j + 1, "依据段为空或占位（规格：同上；不许留空顶替）")

    # ---- 道三：红线 ----
    for j, ln in enumerate(lines):
        for w in BANWORDS:
            if w in ln:
                add('E-BANWORD', '禁词', j + 1, f"命中禁词「{w}」（规格：必涨/稳赚/零风险/保证收益/强烈推荐/稳赢/无风险 零豁免）")
    if '关键数快表' in secs:
        i0, i1 = secs['关键数快表']
        for j in range(i0, i1):
            ln = lines[j]
            if not ln.strip().startswith('|'):
                continue
            cells = split_row(ln)
            if len(cells) < 2 or is_blank_cell(cells[1]):
                continue
            for h in HEDGE:
                if h in cells[1]:
                    add('E-BANWORD', '改数', j + 1, f"关键数含约数「{h}」（规格：逐字摘录，不四舍五入、不写约／左右）")
                    break
    for j, ln in enumerate(lines):
        if any(w in ln for w in JUDGE_WORDS):
            i5 = secs.get('待核清单')
            in_pending = bool(i5) and i5[0] <= j < i5[1]
            if '[待人工]' not in ln and not in_pending:
                add('E-BANWORD', '待人工域', j + 1, "评级/目标价/走势类语句未挂 [待人工]（规格：本件不产出判断，此类一律挂待核清单）")

    # ---- 道四：计数与申报 ----
    if '影响链候选' in secs:
        i0, i1 = secs['影响链候选']
        n_cand = len([j for j in range(i0, i1) if '候选' in lines[j] and '←' in lines[j]])
        if n_cand > 3:
            add('E-COVERAGE', '条数', i0 + 1, f"影响链候选 {n_cand} 条（规格：至多三条）")
    if '同类对照' in secs:
        i0, i1 = secs['同类对照']
        rows = [j for j in range(i0, i1) if lines[j].strip().startswith('|') and len(split_row(lines[j])) >= 3
                and not is_blank_cell(split_row(lines[j])[0]) and split_row(lines[j])[0] not in {'披露日', '---'}
                and not set(split_row(lines[j])[0]) <= {'-'}]
        declared = any(k in '\n'.join(lines[i0:i1]) for k in ('未检索到同类', '检索未覆盖'))
        marked = '☑' in '\n'.join(lines[i0:i1])
        if not rows and not (declared and marked):
            add('E-COVERAGE', '对照', i0 + 1, "同类对照既无行也未声明（规格：列 24 个月内同类，或勾选「未检索到同类／检索未覆盖，待核」）")
    if '待核清单' in secs:
        i0, i1 = secs['待核清单']
        if '[待人工]' not in '\n'.join(lines[i0:i1]):
            add('E-COVERAGE', '申报', i0 + 1, "待核清单缺 [待人工] 汇总位（规格：评级/目标价/持续影响全挂此节）")
    return finds, len(lines)


def report(path: Path, quiet=False):
    finds, nlines = check(path)
    if finds:
        print(f"FAIL: {path.name}（{len(finds)} 条）")
        for f in finds:
            print('  - ' + f)
        codes = sorted({re.match(r'\[(E-[A-Z]+)\]', f).group(1) for f in finds})
        print('  码表: ' + '; '.join(f'{c}→{E_LEGEND[c]}' for c in codes))
        return 1
    print(f"PASS: {path.name}（五段齐、头部三件套与三要素就位、关键数带锚、影响链带依据、禁词零命中、申报就位）")
    if not quiet:
        print(f"       扫过 {nlines} 行，发条 0 条；判定与阈值全集以本脚本现值为准（--help 看四道说明）")
    return 0


def selftest():
    good, bad = HERE / 'fixtures' / 'good-card.md', HERE / 'fixtures' / 'bad-card.md'
    for f in (good, bad):
        if not f.is_file():
            print(f"SELFTEST FAIL: 夹具缺失 {f}")
            return 1
    goods = [good]  # 好样夹具集：末行枚数由它现算，不写字面量
    gf, gnl = [], 0
    for g in goods:
        fx, nl = check(g)
        gf += fx
        gnl += nl
    bf, bnl = check(bad)
    got = {c for c in (re.match(r'\[(E-[A-Z]+)\]', x).group(1) for x in bf)}
    want = set(E_LEGEND)
    ok = True
    print(f"selftest 好样：{'、'.join(g.name for g in goods)} 扫过 {gnl} 行，发条 {len(gf)} 条（规格 0）")
    for x in gf:
        print('   意外发条 → ' + x)
        ok = False
    print(f"selftest 坏样：{bad.name} 扫过 {bnl} 行，发条 {len(bf)} 条（规格 ≥1 且四道全发）")
    missing = sorted(want - got)
    if missing:
        print('   未发出的码 → ' + ', '.join(missing))
        ok = False
    print(f"selftest: {'ALL GREEN' if ok else 'FAIL'}（好样 {len(goods)} 枚·发条 {len(gf)} 条（规格 0）· 坏样四道 {len(got)}/{len(want)}）")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="校验一张公告事件速读卡是否合五段契约与红线（零网络）。",
        epilog="出口：FAIL 一行计数＋逐条 E-* 详行＋码表；PASS 一行＋扫过计数。判定全集在本脚本现值。")
    ap.add_argument('card', nargs='?', help='待校验的卡（markdown）')
    ap.add_argument('--selftest', action='store_true', help='跑包内两件夹具（好样须过、坏样四道全发）')
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.card:
        ap.error('缺参数：给一个卡文件，或用 --selftest')
    p = Path(args.card)
    if not p.is_file():
        print(f"[出错] 文件不存在：{p}")
        return 1
    return report(p)


if __name__ == '__main__':
    sys.exit(main())
