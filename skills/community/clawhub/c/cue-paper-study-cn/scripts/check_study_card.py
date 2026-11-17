#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_study_card.py — 校验一张「论文研读卡」是否合 `SKILL.md` §3 五段契约与 §4 红线。

用法：
    python3 check_study_card.py <卡.md>        校验一张卡（默认零网络，不发任何请求）
    python3 check_study_card.py --selftest     跑包内四件夹具：好样必须过、坏样四道必须全发、两枚单点反例各自发红，另有一档隔离副本必须响亮失败
    python3 check_study_card.py --help         本说明

出口形制（与套件姊妹件同族）：
    失败 = 一行 "FAIL: <文件>（N 条）"，其下每条详行**先打错误码前缀**（四枚 `E-*` 之一），
           道名后是行号与该道规格；末行 "码表:" 只列本次真正用到的码与含义。
    全过 = 一行 "PASS: <文件>（…）"，并印「扫过行数」与「发条数」两类计数。

四道是什么（判定全集在本脚本，本文只指路，不复述细节）：
    道一 形制：头部自标三件套＋本次读取依据与论文版本与通道页集就位（占位即发）＋五段齐且有序
    道二 锚：论文卡每行、引用网络每条、槽材料句每句都要有页／节锚；取不到写「缺」并注「不适用」；
            头部记了「共 N 页」时，本道另核**锚号 ≤ N**（越界即发 E-ANCHOR）；页集未记则这条比对跳过
    道三 红线：禁"应该能复现"式推断、禁代写·降重·润色交稿类话术、学术评价类语句必须挂 [待人工]
    道四 计数与申报：复现三项逐个交代；引用无条目必须勾选声明；推断槽必须带确认标记；待核段必须有 [待人工] 汇总；
            页集取不到时必须在头部申报「页集比对跳过」（不申报即发，机检不替你猜页集）

计数口径：PASS 行的「扫过 N 行」按 `split('\\n')` 口径计，比 `wc -l` 现值多 1（行尾换行也占一格）；
            报「扫过 N 行」时请连口径一起报，免得与 wc 对不上被误判成计数错。

本件不做学术数据库检索（文献输入只有你给的文件与公开可访问链接），因此本脚本**不校验任何学术域检索结果**——
未立的面上不建闸，免得把没跑过的能力说成已可核对；此判据不因 §2 文案改写而放松。
本脚本是**形制闸，不是事实闸**：它核卡面形制与「锚号 ≤ 卡面页集」，**不**判「那句话是否真在这一页」——
那一层由卡外的逐字复验器（把引句与解析返回文本逐字节比对）承担，交付时须随件说明其存在与结果。
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

REPRO_SOURCE = Path(__file__).resolve().parent.parent / 'assets' / '论文研读卡.md'
REPRO_ERROR = None


def _repro_classes():
    """复现清单三类名：从本包模板现值取（模板改了它跟着变），文档与码内不留第二份。

    模板读不到时**不留空元组**——空元组会让「逐类名点名」退化成恒真放行（无类可缺＝永远通过），
    那是最坏的一种假绿：闸还在、退出码还在、话术还是原话，只是不再判任何东西。
    此处把故障记进 REPRO_ERROR，由 check() 当场发一条 E-FORMAT 并以非 0 退出。"""
    global REPRO_ERROR
    try:
        lines = REPRO_SOURCE.read_text(encoding='utf-8').split('\n')
    except OSError as e:
        REPRO_ERROR = f'复现清单尺子的来源不可读：期望 {REPRO_SOURCE.name}（{e.strerror or e}）'
        return ()
    names = []
    for ln in lines:
        cs = [c.strip() for c in ln.strip().strip('|').split('|')]
        if len(cs) >= 2 and re.match(r'^\d+$', cs[0] or 'x') and cs[1] and '☐' not in cs[1]:
            names.append(cs[1])
    if len(names) < 3:
        REPRO_ERROR = f'复现清单尺子的来源里凑不齐三类名：{REPRO_SOURCE.name} 现取 {len(names)} 类（规格 ≥3）'
        return ()
    return tuple(names[:3])


REPRO_CLASSES = _repro_classes()

SECTIONS = ['论文卡', '复现清单', '引用网络', '综述脚手架', '待核清单']
CN_NUM = ['一', '二', '三', '四', '五']
HEAD_MARKS = ('AI 研读整理', '观点请回原文核对', '不构成学术评价')
ANCHOR_PAT = re.compile(r'[Pp§]\s*\d+|\d+\s*[页节段]|第\s*[一二三四五六七八九十\d]+\s*[节段]|参考文献区')
MISSING_MARK = re.compile(r'^(缺|文内未见|未标注|不适用)')
INFER = re.compile(r'应该能复现|应当能复现|必然能复现|肯定能复现|一定能复现|必然可复现')
GHOST = re.compile(r'代写|降重|润色交稿|已为你改写|已帮你改写|已代写')
JUDGE = re.compile(r'值得推广|结论可靠|证明了?有效性|建议(录用|拒稿)|审稿意见|创新性不足|质量很高')
REPRINT = re.compile(r'被引\s*\d+|\d+\s*次引用|引用量\s*\d+')
NEG = ('不', '非', '拒', '未', '勿', '婉')

# 页集自证：头部记「共 N 页」则道二核锚号 ≤ N；取不到须在头部申报这句话
PAGE_SET_KEY = '通道页集'
PAGE_DECL = '页集比对跳过'
PAGE_N = re.compile(r'共\s*(\d+)\s*页')
PNUM = re.compile(r'[Pp]\s*(\d+)')


def ghost_hit(line):
    for m in GHOST.finditer(line):
        before = line[max(0, m.start() - 2):m.start()]
        if not any(n in before for n in NEG):
            return True
    return False


def blank(s: str) -> bool:
    s = s.strip()
    return (not s) or set(s) <= {'-', ' ', '—'} or '__' in s or s in {'☐', '－'}


def cells(line: str):
    core = line.strip().strip('|')
    return [c.strip() for c in core.split('|')]


def row_items(lines, i0, i1):
    """给出该段内的表格数据行（跳过表头与分隔行），返回 (行号, 单元格列表)。"""
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


def section_ranges(lines):
    heads = {}
    for i, ln in enumerate(lines):
        m = re.match(r'^##\s+([一二三四五六七八九])、(.+?)\s*$', ln)
        if m:
            heads.setdefault(m.group(2).strip(), i)
    order = sorted(heads.values())
    out = {}
    for name, idx in heads.items():
        out[name] = (idx, min([o for o in order if o > idx], default=len(lines)))
    return out


def check(path: Path):
    lines = path.read_text(encoding='utf-8').split('\n')
    finds = []

    def add(code, lane, lineno, detail):
        finds.append(f"[{code}] [{lane}] 第 {lineno} 行：{detail}")

    # ---- 道一 形制 ----
    hi = [i for i, ln in enumerate(lines) if ln.strip() == '## 头部自标']
    if not hi:
        add('E-FORMAT', '头部', 1, "缺「## 头部自标」段（规格：该段存在，且含『AI 研读整理』『观点请回原文核对』『不构成学术评价』三件套）")
    else:
        i0 = hi[0]
        i1 = min([i for i, ln in enumerate(lines) if i > i0 and ln.startswith('## ')], default=len(lines))
        blob = '\n'.join(lines[i0:i1])
        for need in HEAD_MARKS:
            if need not in blob:
                add('E-FORMAT', '头部', i0 + 1, f"头部自标缺『{need}』（规格：三件套逐字齐）")
        for key, spec in (('本次读取所依据', '论文文件路径或 URL'), ('论文版本', '年／卷／期／版次，文内取；取不到写「缺」')):
            hit = [j for j in range(i0, i1) if key in lines[j]]
            if not hit:
                add('E-FORMAT', '来源', i0 + 1, f"头部缺「{key}」行（规格：{spec}）")
            else:
                j = hit[0]
                ln = lines[j]
                if '__' in ln:
                    add('E-FORMAT', '来源', j + 1, f"「{key}」仍是占位（规格：{spec}；论文内容只能来自本次读到的文件）")
                elif key == '论文版本' and not re.search(r'\d{4}|缺|文内未见', ln):
                    add('E-FORMAT', '来源', j + 1, f"「{key}」既无年卷期也未标「缺」（规格：{spec}）")

    # ---- 页集自证（供道二核锚号、道四核申报） ----
    n_pages = None
    if hi:
        h0 = hi[0]
        h1 = min([i for i, ln in enumerate(lines) if i > h0 and ln.startswith('## ')], default=len(lines))
        pg = [j for j in range(h0, h1) if PAGE_SET_KEY in lines[j]]
        if not pg:
            add('E-FORMAT', '来源', h0 + 1, f"头部缺「{PAGE_SET_KEY}」行（规格：解析回显共几页写「共 N 页」；取不到写「未取」并申报『{PAGE_DECL}』）")
        elif '__' in re.split(r'[:：]', lines[pg[0]], 1)[-1]:
            add('E-FORMAT', '来源', pg[0] + 1, f"「{PAGE_SET_KEY}」仍是占位（规格：「共 N 页」取自解析回显，或写「未取」并申报『{PAGE_DECL}』；机检不替你猜页集）")
        else:
            # 只核冒号后的**值面**：标签文字里本就带着「共 N 页」「页集比对跳过」两个字面，
            # 整行去比会永远命中申报——那样这道闸就是假的。
            value = re.split(r'[:：]', lines[pg[0]], 1)[-1]
            m = PAGE_N.search(value)
            if m:
                n_pages = int(m.group(1))
            elif PAGE_DECL not in value:
                add('E-COVERAGE', '页集申报', pg[0] + 1, f"页集值面既无「共 N 页」也未申报跳过（规格：取不到就写「未取」＋一句『{PAGE_DECL}』,让比对不成立这件事写在卡面上；标签文字里的这四个字不算申报）")

    def check_pages(cs, j, lane):
        """锚号 ≤ 页集：只在卡面记了「共 N 页」时核。"""
        if n_pages is None or len(cs) < 3:
            return
        for k in (int(x) for x in PNUM.findall(cs[2])):
            if k > n_pages:
                add('E-ANCHOR', '页集', j + 1, f"锚号 P{k} 超出卡面页集（共 {n_pages} 页）（规格：锚号以解析回显为准；超界即视为可疑锚,删该行或改回页集内页码）")

    secs = section_ranges(lines)
    for n, name in zip(CN_NUM, SECTIONS):
        if name not in secs:
            add('E-FORMAT', '五段', 1, f"缺「## {n}、{name}」段（规格：五段齐且按一二三四五有序）")
    if all(s in secs for s in SECTIONS):
        idx = [secs[s][0] for s in SECTIONS]
        if idx != sorted(idx):
            add('E-FORMAT', '五段', idx[0] + 1, "五段次序与契约不一致（规格：论文卡→复现清单→引用网络→综述脚手架→待核清单）")

    # ---- 道二 锚 ----
    if '论文卡' in secs:
        i0, i1 = secs['论文卡']
        for j, cs in row_items(lines, i0, i1):
            if len(cs) < 3 or blank(cs[1]):
                continue
            if blank(cs[2]) or not (ANCHOR_PAT.search(cs[2]) or MISSING_MARK.match(cs[2])):
                add('E-ANCHOR', '论文卡', j + 1, f"「{cs[0]}」行有内容无锚（锚样：P×／×页／第×节／参考文献区；取不到则内容写「缺」并锚写「不适用」）")
            check_pages(cs, j, '论文卡')
    if '引用网络' in secs:
        i0, i1 = secs['引用网络']
        for j, cs in row_items(lines, i0, i1):
            if len(cs) < 3 or blank(cs[1]):
                continue
            if blank(cs[2]) or not ANCHOR_PAT.search(cs[2]):
                add('E-ANCHOR', '引文', j + 1, "被引文献无文内定位（规格：只列参考文献区里真有的条目，逐条带页／节定位；无定位即视为可疑条目，删该行）")
            check_pages(cs, j, '引文')
    if '综述脚手架' in secs:
        i0, i1 = secs['综述脚手架']
        for j, cs in row_items(lines, i0, i1):
            if len(cs) < 4 or blank(cs[2]) or '空槽' in ''.join(cs):
                continue
            if not ANCHOR_PAT.search(cs[2]):
                add('E-ANCHOR', '槽材料', j + 1, "论点槽的材料句无页／节锚（规格：料必须可回查；没有料就写「空槽（不硬填）」）")
            check_pages(cs, j, '槽材料')

    # ---- 道三 红线 ----
    for j, ln in enumerate(lines):
        if INFER.search(ln):
            add('E-BANWORD', '推断', j + 1, "出现「应该能复现」式推断（规格：复现清单只列缺口，不判定能否复现）")
        if ghost_hit(ln):
            add('E-BANWORD', '越界', j + 1, "出现代写·降重·润色交稿类肯定话术（规格：此类请求一律婉拒并指回边界，不写进卡；「不代写」这类否定句不算违例）")
        if JUDGE.search(ln) and '[待人工]' not in ln:
            i5 = secs.get('待核清单')
            if not (i5 and i5[0] <= j < i5[1]):
                add('E-BANWORD', '学术评价', j + 1, "学术评价类语句未挂 [待人工]（规格：创新性、可靠性、是否值得引用一律挂待核清单，本卡不代答）")
    if '论文卡' in secs:
        i0, i1 = secs['论文卡']
        for j, cs in row_items(lines, i0, i1):
            if len(cs) < 3 or blank(cs[1]):
                continue
            if re.search(r'约\s?\d|近似|大概', cs[1]) and not MISSING_MARK.match(cs[1]):
                add('E-BANWORD', '改数', j + 1, "论文卡内容含约数（规格：引文与数字逐字，不改写、不四舍五入）")

    # ---- 道四 计数与申报 ----
    if '复现清单' in secs:
        i0, i1 = secs['复现清单']
        if REPRO_ERROR:
            add('E-FORMAT', '尺子来源', i0 + 1,
                REPRO_ERROR + '（规格：三类名从本包模板现取；尺子取不到就无从判「三类齐不齐」——本件宁可报错退出，不静默放行）')
        rows = row_items(lines, i0, i1)
        if len(rows) < 3:
            add('E-COVERAGE', '缺口申报', i0 + 1, f"复现清单只 {len(rows)} 行（规格：数据集／代码／参数三项逐个交代，缺也要点名）")
        # 行数够不等于三类齐：把两行项目名都写成同一个也能凑满三行。逐类名点名，名目取自本包模板现值。
        # 【只取项目列 cs[1]】——依据格／备注里出现同名串不算交代，那正是把两类挤成一类的伪装路径。
        if not REPRO_ERROR:
            named = [cs[1] for _j, cs in rows if len(cs) > 1]
            absent = [c for c in REPRO_CLASSES if not any(c in cell for cell in named)]
            if absent:
                add('E-COVERAGE', '缺口申报', i0 + 1,
                    "复现清单缺类名 %s（规格：数据集／代码／参数三类逐类交代，行数为 3 但类名重复仍算缺——项名照模板逐字写在**项目格**，不自立类别，也不许把类名挪进依据或备注格充数）" % '、'.join(absent))
        for j, cs in rows:
            if len(cs) < 4 or blank(cs[2]) or blank(cs[3]):
                add('E-COVERAGE', '缺口申报', j + 1, "该项状态或依据留空（规格：状态填在场／未见／缺／部分，依据带锚或写「不适用」）")
    if '引用网络' in secs:
        i0, i1 = secs['引用网络']
        blob = '\n'.join(lines[i0:i1])
        has_rows = any(len(cs) >= 3 and not blank(cs[1]) for _, cs in row_items(lines, i0, i1))
        declared = bool(re.search(r'(未检索到|检索面未覆盖)[^\n]*☑|☑[^\n]*(未检索到|检索面未覆盖)', blob))
        if not has_rows and not declared:
            add('E-COVERAGE', '引用', i0 + 1, "引用网络既无条目又未勾选声明（规格：列文内真有的条目，或勾选「未检索到／检索面未覆盖，待核」）")
        if REPRINT.search(blob) and '已检索并列出 ☑' not in blob and '☑ 已检索并列出' not in blob:
            add('E-COVERAGE', '被引', i0 + 1, "写了被引次数却未勾选「已检索并列出」（规格：本件不做学术数据库检索，检索面未覆盖就只写声明）")
    if '综述脚手架' in secs:
        i0, i1 = secs['综述脚手架']
        for j, cs in row_items(lines, i0, i1):
            if len(cs) < 4 or (blank(cs[1]) and blank(cs[2])) or '空槽' in ' '.join(cs):
                continue
            src = cs[3]
            chosen = [w.strip() for mk, w in re.findall(r'([☑☐])\s*([^☐☑]+)', src) if mk == '☑']
            inferred = any('推断' in w for w in chosen)
            confirmed = any('已确认' in w for w in chosen)
            if inferred and not confirmed:
                add('E-COVERAGE', '槽确认', j + 1, "推断出的论点槽未取明确确认（规格：标「推断·待用户确认」，确认后改写为「已确认：<日期>」；单字应答不算确认）")
            if '☑' not in src:
                add('E-COVERAGE', '槽来源', j + 1, "论点槽未勾选来源（规格：用户给／推断·待用户确认／已确认，三选一）")
    if '待核清单' in secs:
        i0, i1 = secs['待核清单']
        if '[待人工]' not in '\n'.join(lines[i0:i1]):
            add('E-COVERAGE', '申报', i0 + 1, "待核清单缺 [待人工] 汇总位（规格：学术评价与需读原文的判断全挂此节）")
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
    print("PASS: " + path.name + "（五段齐、头部三件套与来源版本就位、句级锚齐、推断与评价零越界、缺口与声明逐个交代）")
    print(f"       扫过 {n} 行，发条 0 条；判定与阈值全集以本脚本现值为准（--help 看四道说明）")
    return 0


# 反例档：复现清单两类项目名挤成同一种——行数仍三行、类名缺两类，其余与好样全同
def probe_isolated():
    """把本脚本单独拷进空目录（无 assets/ 模板）跑一张缺类卡：尺子来源不可读必须响亮失败。

    旧形制是 _repro_classes() 读不到模板就 return ()，absent 恒空＝这道闸静默退化成放行；
    本档就是那条退化的反证：改回静默形制，这一枚立刻红。"""
    import shutil
    import subprocess
    import tempfile
    card = HERE / 'fixtures' / 'mut-repro-one-class.md'
    if not card.is_file():
        return False, '缺反例夹具 mut-repro-one-class.md，无从跑隔离档'
    d = tempfile.mkdtemp(prefix='study-isolated-')
    try:
        scripts_dir = Path(d) / 'scripts'
        scripts_dir.mkdir(parents=True)
        dst = scripts_dir / Path(__file__).name
        shutil.copy2(str(Path(__file__).resolve()), str(dst))
        r = subprocess.run([sys.executable, '-B', str(dst), str(card)], capture_output=True, text=True)
        out = r.stdout + r.stderr
        named = '尺子的来源不可读' in out
        detail = '隔离副本（无 assets/ 模板）退码 %s，详行含「尺子的来源不可读」＝%s' % (
            r.returncode, '是' if named else '否')
        return (r.returncode != 0 and named), detail
    finally:
        shutil.rmtree(d, ignore_errors=True)


def selftest():
    good, bad = HERE / 'fixtures' / 'good-study-card.md', HERE / 'fixtures' / 'bad-study-card.md'
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
    probes = [('mut-repro-one-class.md', ('E-COVERAGE', '缺口申报'), '缺类名'),
              ('mut-class-in-evidence.md', ('E-COVERAGE', '缺口申报'), '项目格')]
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

    # 隔离档：把本脚本单独拷进空目录（无 assets/论文研读卡.md）跑同一张缺类卡——
    # 尺子来源不可读必须响亮失败（退码非 0 且详行点名来源），不许退化成「永远不缺类」。
    iso_ok, iso_detail = probe_isolated()
    print("selftest 隔离档：%s（规格 退码非 0 且详行含「尺子的来源不可读」）" % iso_detail)
    if not iso_ok:
        ok = False
    print(f"selftest: {'ALL GREEN' if ok else 'FAIL'}（好样 {len(goods)} 枚·发条 {len(gf)} 条（规格 0）· 坏样四道 {len(got)}/{len(want)} · 反例档 {len(probes)} 枚{'全发红' if allred else '有未红!'} · 隔离档 {'发红' if iso_ok else '未发红!'}）")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="校验一张论文研读卡是否合五段契约与红线（零网络）。",
        epilog="出口：FAIL 一行计数＋逐条 E-* 详行＋码表；PASS 一行＋两类计数。判定全集在本脚本现值。")
    ap.add_argument('card', nargs='?', help='待校验的卡（markdown）')
    ap.add_argument('--selftest', action='store_true', help='跑包内四件夹具（好样须过、坏样四道全发、两枚反例发红、隔离档响亮失败）')
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
