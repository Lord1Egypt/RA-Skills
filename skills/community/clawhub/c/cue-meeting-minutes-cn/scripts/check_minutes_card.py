#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_minutes_card.py — 校验一张「会议纪要卡」是否合 `SKILL.md` §1 实证边界、§3 五段契约与 §4 红线。

用法：
    python3 check_minutes_card.py <卡.md>       校验一张卡（默认零网络，不发任何请求）
    python3 check_minutes_card.py --selftest    跑包内守护样：好样、坏样与单点反例各档，档名与枚数由末行自报红并点名
    python3 check_minutes_card.py --help        本说明

出口形制（与套件姊妹件同族）：
    失败 = 一行 "FAIL: <文件>（N 条）"，其下每条详行**先打错误码前缀**（四枚 `E-*` 之一），
           道名后是行号与该道规格；末行 "码表:" 只列本次真正用到的码与含义。
    全过 = 一行 "PASS: <文件>（…）"，并印「扫过行数」与「发条数」两类计数。

四道是什么（判定全集在本脚本，本文只指路，不复述细节）：
    道一 形制与边界申报：头部自标两件套＋录音来源已填＋素材形制三选一已勾＋时间轴基准已勾＋五段齐且有序
    道二 锚：基本信息逐项有依据；逐字每行带 [mm:ss]；话题段带起止双锚；决策与待办带原话锚，负责人须是「录音自报＋锚」或「未自报·待核」
    道三 红线：实时转写·边录边转类越界话术、"已清洗/已校对"类冒充、润色改写类话术、一致通过类外推（无锚即拦）、任何价格数字
    道四 计数与申报：勾选「整场直投·已停用」却仍有逐字行＝自相矛盾；归段未自标「此归类非原文所有」；待核段缺 [待人工]

实证面（内部音视频回测账）：音频腿成立的工作流是**本地小段/切片（≤256 MiB）**；
整场长录音的 URL 路与本地全长路当时均未臻，切片间连续性与跨片时间轴**未建立实证**——
所以本脚本对跨片锚只要求标待核，不校验"时间轴是否连续"：未在证的面上不建闸。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# 与姊妹件逐字同源的四枚码（第五枚 E-LEDGER 属账本状态机面，本件无账本，故不启用）
E_LEGEND = {
    "E-FORMAT":   "形制/输入/表序不合式→按该行括号内规格改形制后复跑",
    "E-ANCHOR":   "锚/证据链缺失或断链→补合式锚或删除该条,禁虚构",
    "E-BANWORD":  "禁词/评级/幻觉/待人工域命中→改中性陈述或删除,零豁免区",
    "E-COVERAGE": "计数/覆盖/申报对不上→逐类补账或如实标未检索到",
}

SECTIONS = ['基本信息', '逐字带锚', '话题分段', '决策与待办', '待核清单']
CN_NUM = ['一', '二', '三', '四', '五']
HEAD_MARKS = ('AI 整理纪要', '决策请对回原话确认')
TIME = re.compile(r'\[\d{1,2}:\d{2}(?::\d{2})?\]')
TIMESPAN = re.compile(r'\[\d{1,2}:\d{2}[^\n]{0,3}~[^\n]{0,4}\d{1,2}:\d{2}\]')
MISSING = re.compile(r'^(缺|未提供|不适用|文内未见)')
SELF_ID = re.compile(r'自报[^\n]{0,4}\[\d{1,2}:\d{2}')
UNANNOUNCED = re.compile(r'^(未自报|待核|不适用)')
AGREE = re.compile(r'一致通过|大家都同意|全票通过|无异议通过')
REALTIME = re.compile(r'实时转写|边录边转|同步转写')
CLEANED = re.compile(r'已清洗|已校对|已修正|已校正|已纠正')
POLISH = re.compile(r'润色|改得更漂亮|漂亮版|美化改写')
PRICE = re.compile(r'\d+(?:\.\d+)?\s*(?:元|块|分钱|credits?)|每\s*(?:分钟|小时)\s*[\d¥$]')
NEG = ('不', '非', '未', '勿', '无', '拒')


def blank(s: str) -> bool:
    s = s.strip()
    return (not s) or set(s) <= {'-', ' ', '—'} or '__' in s or s in {'☐', '－'}


def cells(line: str):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def neg_protect(line: str, pat: re.Pattern) -> bool:
    """命中检测词，但紧前方有否定字（如「不清洗」「非实时」）不算违例——逐位判断，不做整卡豁免。"""
    for m in pat.finditer(line):
        before = line[max(0, m.start() - 2):m.start()]
        if not any(n in before for n in NEG):
            return True
    return False


def row_items(lines, i0, i1):
    out = []
    for j in range(i0, i1):
        ln = lines[j]
        if not ln.strip().startswith('|'):
            continue
        cs = cells(ln)
        if not cs or set(cs[0]) <= {'-'} or cs[0] in {'#', '项'}:
            continue
        out.append((j, cs))
    return out


def checked_items(cell: str):
    """勾选项文字清单：兼容「☑ 甲　☐ 乙」与「甲 ☑」两形（与姊妹件的 ticks／chosen 同族）。"""
    return [w.strip() for mk, w in re.findall(r'([☑☐])\s*([^☐☑]+)', cell) if mk == '☑']


CONT_PAT = re.compile(r'^[ \t　]+')


def field_span(lines, i1, start):
    """字段行的判定域＝该行＋其后续物理行（行首缩进或直接以 ☑／☐ 起头的续写）。

    勾被写到下一物理行仍是同一字段的申报，只取第一行会把「三选一勾成两项」看成合规；
    返回 (合并文本, 含勾的行号表)。"""
    parts = [lines[start]]
    rows = [start]
    k = start + 1
    while k < i1:
        ln = lines[k]
        if not ln.strip():
            break
        if CONT_PAT.match(ln) or ln.lstrip().startswith(('☑', '☐')):
            parts.append(ln)
            rows.append(k)
            k += 1
        else:
            break
    return '\n'.join(parts), rows


def tick_rows(rows, lines):
    """判定域里真正带着 ☑ 的物理行号（1 基）。"""
    return [r + 1 for r in rows if '☑' in lines[r]]


def section_ranges(lines):
    heads = {}
    for i, ln in enumerate(lines):
        m = re.match(r'^##\s+([一二三四五六七八九])、(.+?)\s*$', ln)
        if m:
            heads.setdefault(m.group(2).strip(), i)
    order = sorted(heads.values())
    return {n: (i, min([o for o in order if o > i], default=len(lines))) for n, i in heads.items()}


def check(path: Path):
    lines = path.read_text(encoding='utf-8').split('\n')
    finds = []

    def add(code, lane, lineno, detail):
        finds.append(f"[{code}] [{lane}] 第 {lineno} 行：{detail}")

    # ---- 道一 形制与边界申报 ----
    hi = [i for i, ln in enumerate(lines) if ln.strip() == '## 头部自标']
    if not hi:
        add('E-FORMAT', '头部', 1, "缺「## 头部自标」段（规格：该段存在，且含『AI 整理纪要』『决策请对回原话确认』两件套）")
        head_rng = (0, min([i for i, l in enumerate(lines) if l.startswith('## ')], default=len(lines)))
    else:
        i0 = hi[0]
        i1 = min([i for i, ln in enumerate(lines) if i > i0 and ln.startswith('## ')], default=len(lines))
        head_rng = (i0, i1)
        blob = '\n'.join(lines[i0:i1])
        for need in HEAD_MARKS:
            if need not in blob:
                add('E-FORMAT', '头部', i0 + 1, f"头部自标缺『{need}』（规格：两件套逐字齐）")
        src = [j for j in range(i0, i1) if '录音来源' in lines[j]]
        if not src:
            add('E-FORMAT', '来源', i0 + 1, "头部缺「录音来源」行（规格：Bridge 授权目录内路径或可解析链接）")
        elif '__' in lines[src[0]]:
            add('E-FORMAT', '来源', src[0] + 1, "「录音来源」仍是占位（规格：同上；来源不填，锚无处可回）")
        form = [j for j in range(i0, i1) if '素材形制' in lines[j]]
        if not form:
            add('E-FORMAT', '边界申报', i0 + 1, "头部缺「素材形制」行（规格：单段／切片／整场直投·已停用 三选一并勾选）")
        else:
            ftxt, frows = field_span(lines, i1, form[0])
            fchk = checked_items(ftxt)
            if not fchk:
                add('E-FORMAT', '边界申报', form[0] + 1, "素材形制未勾选（规格：三选一；未证面直投即停用，停用也要留说明）")
            elif len(fchk) > 1:
                add('E-FORMAT', '边界申报', form[0] + 1,
                    "素材形制勾了 %d 项（%s），勾落在第 %s 行（规格：三选一——单段／切片／整场直投只能中一项，双勾等于本卡同时声称两种取数路径；把第二个勾挪到下一物理行仍是同一字段，照样计）" % (
                        len(fchk), '、'.join(fchk), '、'.join(str(x) for x in tick_rows(frows, lines))))
        axis = [j for j in range(i0, i1) if '时间轴基准' in lines[j]]
        if not axis:
            add('E-FORMAT', '时间轴', i0 + 1, "头部缺「时间轴基准」行（规格：单切片内 mm:ss／多切片拼接·跨片连续性未建立实证，二选一）")
        else:
            atxt, arows = field_span(lines, i1, axis[0])
            achk = checked_items(atxt)
            if not achk:
                add('E-FORMAT', '时间轴', axis[0] + 1, "时间轴基准未勾选（规格：同上；这是「锚能不能横着比」的唯一依据）")
            elif len(achk) > 1:
                add('E-FORMAT', '时间轴', axis[0] + 1,
                    "时间轴基准勾了 %d 项（%s），勾落在第 %s 行（规格：二选一——单切片与多切片拼接只能中一项，双勾会让 mm:ss 锚的可比性无定义；跨物理行续写同样算数）" % (
                        len(achk), '、'.join(achk), '、'.join(str(x) for x in tick_rows(arows, lines))))

    secs = section_ranges(lines)
    for n, name in zip(CN_NUM, SECTIONS):
        if name not in secs:
            add('E-FORMAT', '五段', 1, f"缺「## {n}、{name}」段（规格：五段齐且按一二三四五有序）")
    if all(s in secs for s in SECTIONS):
        idx = [secs[s][0] for s in SECTIONS]
        if idx != sorted(idx):
            add('E-FORMAT', '五段', idx[0] + 1, "五段次序与契约不一致（规格：基本信息→逐字→话题→决策待办→待核）")

    # ---- 道二 锚 ----
    if '基本信息' in secs:
        i0, i1 = secs['基本信息']
        for j, cs in row_items(lines, i0, i1):
            if len(cs) < 3 or blank(cs[1]):
                continue
            if blank(cs[2]) or not (TIME.search(cs[2]) or MISSING.match(cs[2]) or '通道返回' in cs[2]):
                add('E-ANCHOR', '基本信息', j + 1, f"「{cs[0]}」有内容无依据（规格：带 [mm:ss] 锚，或写「缺／未提供／通道返回」；日期无来源即标缺）")
    if '逐字带锚' in secs:
        i0, i1 = secs['逐字带锚']
        for j, cs in row_items(lines, i0, i1):
            if len(cs) < 3 or blank(cs[1]):
                continue
            if not TIME.search(cs[2]):
                add('E-ANCHOR', '逐字', j + 1, "逐字行无 [mm:ss] 锚（规格：每段原文带时间锚；给不出锚就删该行）")
    if '话题分段' in secs:
        i0, i1 = secs['话题分段']
        for j, cs in row_items(lines, i0, i1):
            if len(cs) < 4 or blank(cs[1]):
                continue
            if not TIMESPAN.search(cs[2]) and not (TIME.search(cs[2]) and TIME.search(cs[2].split(']')[-1])):
                add('E-ANCHOR', '段锚', j + 1, "话题段缺起止双锚（规格：[mm:ss]~[mm:ss]；单点锚只能算引用，不能算分段）")
            if '☑' not in cs[3]:
                add('E-COVERAGE', '归段自标', j + 1, "话题归类未自标（规格：勾「此归类非原文所有」——归段是笔记法，不是会议结构）")
    if '决策与待办' in secs:
        i0, i1 = secs['决策与待办']
        for j, cs in row_items(lines, i0, i1):
            if len(cs) < 4 or blank(cs[1]):
                continue
            if not TIME.search(cs[3]):
                add('E-ANCHOR', '决策锚', j + 1, "决策／待办无原话锚（规格：结论句必须回指 [mm:ss]；没有依据的待办不造）")
            if blank(cs[2]) or not (SELF_ID.search(cs[2]) or UNANNOUNCED.match(cs[2])):
                add('E-ANCHOR', '负责人', j + 1, "负责人既非「录音自报＋锚」也未标「未自报·待核」（规格：SKILL §3.4——名单不凭记忆补）")

    # ---- 道三 红线 ----
    for j, ln in enumerate(lines):
        if neg_protect(ln, REALTIME):
            add('E-BANWORD', '越界', j + 1, "出现实时转写·边录边转类话术（规格：本件不做实时面，见 §0「不是什么」）")
        if neg_protect(ln, CLEANED):
            add('E-BANWORD', '清洗冒充', j + 1, "声称已清洗／已校对（规格：ASR 谐音原样入纪要并标待核，不冒充清洗过的转写）")
        if neg_protect(ln, POLISH):
            add('E-BANWORD', '改写', j + 1, "出现润色·美化改写类话术（规格：纪要只忠实原话，不做「更漂亮」版本）")
        if AGREE.search(ln) and not TIME.search(ln):
            add('E-BANWORD', '外推', j + 1, "「一致通过／大家都同意」类表述无原话锚（规格：不外推没说的话，无锚即删）")
        if PRICE.search(ln):
            add('E-BANWORD', '价格', j + 1, "出现价格或计费数字（规格：计费状态以服务端返回为准，本件不给任何价格）")

    # ---- 道四 计数与申报 ----
    stopped = False
    for ln in lines[head_rng[0]:head_rng[1]]:
        if '素材形制' in ln:
            chosen = [w for mk, w in re.findall(r'([☑☐])\s*([^☐☑]+)', ln) if mk == '☑']
            stopped = any('整场直投' in w for w in chosen)
    if '逐字带锚' in secs:
        i0, i1 = secs['逐字带锚']
        n_ver = len([1 for _, cs in row_items(lines, i0, i1) if len(cs) >= 3 and not blank(cs[1])])
        if stopped and n_ver:
            add('E-COVERAGE', '停用矛盾', i0 + 1, f"素材形制勾「整场直投·已停用」但逐字仍有 {n_ver} 行（规格：停用即无逐字产出，二者只能选一）")
        if not stopped and n_ver == 0:
            add('E-COVERAGE', '逐字空', i0 + 1, "未声明停用却没有任何逐字行（规格：有产出就填行，取不到就勾停用并说明理由）")
    if '待核清单' in secs:
        i0, i1 = secs['待核清单']
        if '[待人工]' not in '\n'.join(lines[i0:i1]):
            add('E-COVERAGE', '申报', i0 + 1, "待核清单缺 [待人工] 汇总位（规格：谐音疑点、指代不明、跨片锚全挂此节）")
        # 状态格逐行数勾：模板给的是「☐ 待核 ☐ 已核」两枚互斥框。这是表格行，不靠字段续行合并域——
        # 域合并只治「同一字段写到下一物理行」，表格行的第二勾若写到别的列，这里照样要被抓到。
        for j, cs in row_items(lines, i0, i1):
            for c_i, cell in enumerate(cs):
                if '待核' not in cell or '已核' not in cell:
                    continue
                st = checked_items(cell)
                if len(st) > 1:
                    add('E-FORMAT', '状态互斥', j + 1,
                        "第 %d 列状态格同时勾了 %d 项（%s）（规格：待核／已核互斥二选一，同勾等于本行既未复核又已复核；两枚都空算未复核，不报）" % (
                            c_i + 1, len(st), '、'.join(x.strip() for x in st)))
    return finds, len(lines)


def report(path: Path):
    finds, n = check(path)
    if finds:
        print(f"FAIL: {path.name}（{len(finds)} 条）")
        for f in finds:
            print('  - ' + f)
        codes = sorted({re.match(r'\[(E-[A-Z]+)\]', f).group(1) for f in finds})
        print('  码表: ' + '; '.join(f'{c}→{E_LEGEND[c]}' for c in codes))
        return 1
    print("PASS: " + path.name + "（五段齐、边界与时间轴已申报、句级锚齐、归段自标、外推与清洗冒充零命中、价格零）")
    print(f"       扫过 {n} 行，发条 0 条；判定与阈值全集以本脚本现值为准（--help 看四道说明）")
    return 0


# 反例档：素材形制双勾（单段与切片同时勾）——三选一勾成两项，其余与好样全同
def selftest():
    good, bad = HERE / 'fixtures' / 'good-minutes-card.md', HERE / 'fixtures' / 'bad-minutes-card.md'
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
    got = {re.match(r'\[(E-[A-Z]+)\]', x).group(1) for x in bf}
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
    probes = [('mut-form-double-tick.md', ('E-FORMAT', '边界申报'), '勾了 2 项'),
              ('mut-form-crossline.md', ('E-FORMAT', '边界申报'), '勾落在第'),
              ('mut-axis-crossline.md', ('E-FORMAT', '时间轴'), '勾落在第'),
              ('mut-status-double-tick.md', ('E-FORMAT', '状态互斥'), '状态格同时勾了 2 项')]
    allred = True
    for fname, expect, needle in probes:
        mu = HERE / 'fixtures' / fname
        if not mu.is_file():
            print(f"SELFTEST FAIL: 反例夹具缺失 {mu}")
            return 1
        mf, mnl = check(mu)
        mcode = [(m.group(1), m.group(2)) for m in (re.match(r'\[(E-[A-Z]+)\] \[([^\]]+)\]', x) for x in mf) if m]
        mhit = expect in mcode
        mnamed = any(needle in x for x in mf)
        print("selftest 反例档：%s 扫过 %d 行，发条 %d 条（规格 ≥1、须发 %s／%s、详行含「%s」）" % (
            mu.name, mnl, len(mf), expect[0], expect[1], needle))
        for x in mf[:2]:
            print('   实发详行 → ' + x[:150])
        if not mf:
            print('   意外：单点反例过了闸（缺陷——本档治的正是「判据只查其一」把门过宽）')
            ok = False
            allred = False
        elif not mhit:
            print('   未命中预期码与道名 → 期望 %s／%s，实发 %s' % (
                expect[0], expect[1], '、'.join(a + '／' + b for a, b in mcode) or '无'))
            ok = False
            allred = False
        elif not mnamed:
            print('   发条未点名病灶 → 详行里找不到「%s」' % needle)
            ok = False
            allred = False
    print(f"selftest: {'ALL GREEN' if ok else 'FAIL'}（好样 {len(goods)} 枚·发条 {len(gf)} 条（规格 0）· 坏样四道 {len(got)}/{len(want)} · 反例档 {len(probes)} 枚{'全发红' if allred else '有未红!'}）")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="校验一张会议纪要卡是否合五段契约、实证边界与红线（零网络）。",
        epilog="出口：FAIL 一行计数＋逐条 E-* 详行＋码表；PASS 一行＋两类计数。判定全集在本脚本现值。")
    ap.add_argument('card', nargs='?', help='待校验的卡（markdown）')
    ap.add_argument('--selftest', action='store_true', help='跑包内守护样（好样、坏样与单点反例各档，档名与枚数由末行自报红）')
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
