#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_scan_card.py — 校验一张「风险扫描卡」是否合 `SKILL.md` §2 五段契约与 §3 红线。

用法：
    python3 check_scan_card.py <卡.md>       校验一张卡（默认零网络，不发任何请求）
    python3 check_scan_card.py --selftest    跑包内守护样：好样、坏样与单点反例各档，档名与枚数由末行自报
    python3 check_scan_card.py --help        本说明

出口形制（与套件姊妹件同族）：
    失败 = 一行 "FAIL: <文件>（N 条）"，其下每条详行**先打错误码前缀**（四枚 `E-*` 之一），
           道名后是行号与该道规格；末行 "码表:" 只列本次真正用到的码与含义。
    全过 = 一行 "PASS: <文件>（…）"，并印「扫过行数」与「发条数」两类计数。
    行数口径：「扫过 N 行」按 `split('\\n')` 计，等于 `wc -l` 现值 +1（行尾换行占一格）。

四道是什么（判定全集在本脚本，本文只指路，不复述细节）：
    道一 形制：头部自标三件套＋时点三件（数据日／窗口／运行时刻，缺一无效）就位＋五段齐且有序＋主体行两名在位
    道二 锚：处罚表逐条要日期与官方出处；担保要点逐条要 as_of 与出处；制裁条目要 document_number 或 URL 锚
    道三 红线：禁综合判断类输出（整体风险／等级／评级／违约概率／评分一类）；禁「无风险」「没被查过」一类整句；
               禁「统一 ID」一类措辞（跨域统一主体 ID 不通，主键＝六位代码）；否定式免责句不算违例
    道四 计数与申报：三面未达逐面点名；零条须勾声明并带窗口；担保 0 行须标「真无 vs 抽取缺 未辨」；
               制裁面状态须恰勾一个，跑过的那两形还须勾名形双查；待核段须有 [待人工] 汇总

本件能力面：三源可达（处罚与监管措施／对外担保代理面／全球制裁执法），三面不做（涉诉／股权链／供应链传染）。
**做不到的三面不建能力闸**——本脚本只核「有没有如实写明做不到」，
不校验那三面的数据是否存在；域面以 catalog 现值为准，现值变了才重判。
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

SECTIONS = ['主体行', '处罚与监管措施表', '对外担保要点', '制裁执法面', '未达与待核清单']
CN_NUM = ['一', '二', '三', '四', '五']
HEAD_MARKS = ('AI 整理初稿', '请回官方原文核对', '不构成投资建议')
TIME_KEYS = (('数据日', '数据日须是日期形（YYYY-MM-DD 或返货原形），不许留空'),
             ('窗口', '窗口须给出起止两个日期'),
             ('运行时刻', '运行时刻须是日期形（本卡跑成的时刻）'))
DATE_PAT = re.compile(r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}|^\d{4}-\d{2}-\d{2}$')
DATE_TOKEN = re.compile(r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}日?')   # 窗口单端点用：整段就得是一个日期
SRC_PAT = re.compile(r'https?://|doi\.org|\.gov\.cn|csrc|szse|sse\.org|gov\.cn')
DOCNO_PAT = re.compile(r'document_number|文书号|决定书|编号|〔\d{4}〕\d+|第\d+号')
RATING = re.compile(r'整体风险|风险等级|风险评级|信用等级|违约概率|评分模型|风险评分|风险打分|打个?分')
SAFEWORD = re.compile(r'无风险|没有风险|没被查过|未被查过|从未被查|零风险|肯定干净|一定是干净的')
UNIFIED = re.compile(r'统一\s*ID|统一主体\s*ID|唯一主体\s*ID|统一识别码|统一主体识别')
NEG_WORDS = ('不', '未', '禁', '勿', '拒', '非', '没')
CLAUSE_SPLIT = re.compile(r'[。；;！!？?：:，,、]')
FACES = ('司法涉诉', '股权链', '供应链传染')
ZERO_DECL = re.compile(r'窗口内未检索到|未检索到条目')
GUA_ZERO = re.compile(r'返货\s*0\s*行|0\s*行')
UNRESOLVED = re.compile(r'未辨|待核')


def field_value(line, key, peers):
    """从「键 值　键 值」一行里只切出**该键自己的值面**——整行去比会把邻键的缺陷算到本键头上。"""
    idx = line.find(key)
    if idx < 0:
        return ''
    rest = line[idx + len(key):].lstrip('：:　 ')
    ends = [rest.find(p) for p in peers if p != key and rest.find(p) >= 0]
    return (rest[:min(ends)] if ends else rest).strip()


def clause_before(line, start):
    """命中点所在**小句**的头部：从最近一个句读符到命中处。跨句的否定词不算豁免，同句的否定词才管用。"""
    idx = 0
    for m in CLAUSE_SPLIT.finditer(line[:start]):
        idx = m.end()
    return line[idx:start]


def guarded(line, m):
    """否定式免责句不算违例（如「不评整体风险」「不算违约概率」）；
       断言式违规（「无风险。统一主体 ID 已解析」）不因上一句里的否定字而漏放——故按小句判，不按字数窗口判。"""
    return any(n in clause_before(line, m.start()) for n in NEG_WORDS)


def blank(s: str) -> bool:
    s = s.strip()
    return (not s) or set(s) <= {'-', '—'} or '__' in s or s in {'☐', '－'}


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
        if not cs or set(cs[0]) <= {'-'} or cs[0] in {'#', '项', '面'}:
            continue
        out.append((j, cs))
    return out


def ticks(cell: str):
    """逐格解析勾选：返回 [(标记, 选项文字), …]，兼容「☑ 甲　☐ 乙」与「甲 ☑」两形。"""
    return re.findall(r'([☑☐])\s*([^☐☑]+)', cell)


def chosen(cell: str):
    return [w.strip() for mk, w in ticks(cell) if mk == '☑']


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
        add('E-FORMAT', '头部', 1, "缺「## 头部自标」段（规格：该段存在，且含『AI 整理初稿』『请回官方原文核对』『不构成投资建议』三件套）")
    else:
        i0 = hi[0]
        i1 = min([i for i, ln in enumerate(lines) if i > i0 and ln.startswith('## ')], default=len(lines))
        blob = '\n'.join(lines[i0:i1])
        for need in HEAD_MARKS:
            if need not in blob:
                add('E-FORMAT', '头部', i0 + 1, f"头部自标缺『{need}』（规格：三件套逐字齐）")
        for key, spec in TIME_KEYS:
            hit = [j for j in range(i0, i1) if key in lines[j]]
            if not hit:
                add('E-FORMAT', '时点', i0 + 1, f"头部缺「{key}」（规格：时点三件缺一无效——{spec}）")
                continue
            j = hit[0]
            value = field_value(lines[j], key, [k for k, _ in TIME_KEYS])
            if '__' in value:
                add('E-FORMAT', '时点', j + 1, f"「{key}」仍是占位（规格：{spec}）")
            elif key == '窗口':
                # 窗口是一段区间：整串里搜到任一日期不算合式——起止两端要各自核，
                # 否则「2024-10-09~待定」这类终点没落的形状会被起点带过去。
                parts = [x.strip() for x in re.split(r'[~～]', value) if x.strip()]
                if len(parts) != 2:
                    add('E-FORMAT', '时点', j + 1,
                        f"「窗口」没给出起止两端（现值「{value}」实得 {len(parts)} 段；规格：{spec}，形如 起~止）")
                else:
                    for which, token in zip(('起点', '终点'), parts):
                        if not DATE_TOKEN.fullmatch(token):
                            add('E-FORMAT', '时点', j + 1,
                                f"「窗口」{which}没落成日期形（现值「{token}」；规格：{spec}——两端各自都须是日期形，一端待定则整段无效）")
            elif not DATE_PAT.search(value):
                add('E-FORMAT', '时点', j + 1, f"「{key}」没落成日期形（规格：{spec}）")
    secs = section_ranges(lines)
    if '主体行' in secs:
        i0, i1 = secs['主体行']
        seg = '\n'.join(lines[i0:i1])
        for need in ('公司名', '代码'):
            if need not in seg:
                add('E-FORMAT', '主体', i0 + 1, f"主体行缺「{need}」一行（规格：两名都取自本次返货内字符串，取不到写「未检索到」并进第五段）")
    for n, name in zip(CN_NUM, SECTIONS):
        if name not in secs:
            add('E-FORMAT', '五段', 1, f"缺「## {n}、{name}」段（规格：五段齐且按一二三四五有序）")
    if all(s in secs for s in SECTIONS):
        idx = [secs[s][0] for s in SECTIONS]
        if idx != sorted(idx):
            add('E-FORMAT', '五段', idx[0] + 1, "五段次序与契约不一致（规格：主体行→处罚与监管措施表→对外担保要点→制裁执法面→未达与待核清单）")

    # ---- 道二 锚 ----
    if '主体行' in secs:
        i0, i1 = secs['主体行']
        for j, cs in row_items(lines, i0, i1):
            if not cs or ('候选' in cs[0]):
                continue
            if len(cs) < 3 or blank(cs[1]):
                continue
            if blank(cs[2]):
                add('E-ANCHOR', '主体出处', j + 1, f"「{cs[0]}」有值无出处（规格：主体名与代码也要指回本次返货——域内字段名、链接或解析步皆可；取不到就写「未检索到」并进第五段）")
    if '处罚与监管措施表' in secs:
        i0, i1 = secs['处罚与监管措施表']
        for j, cs in row_items(lines, i0, i1):
            if all(blank(c) for c in cs[1:]):
                continue
            if not DATE_PAT.search(' '.join(cs[2:4])):
                add('E-ANCHOR', '处罚日期', j + 1, "该行缺日期（规格：日期格照返货逐字填，跨源须各自截日对齐）")
            if not (SRC_PAT.search(cs[-1]) or DOCNO_PAT.search(cs[-1])):
                add('E-ANCHOR', '处罚出处', j + 1, "出处格里既无链接也无文书号类锚（规格：最后一格放本次返货里的链接，或写 document_number／决定书号；只写在别格不算——标题里那句「决定书」顶不了出处）")
    if '对外担保要点' in secs:
        i0, i1 = secs['对外担保要点']
        for j, cs in row_items(lines, i0, i1):
            if all(blank(c) for c in cs[1:]):
                continue
            if not DATE_PAT.search(cs[3] if len(cs) > 3 else ''):
                add('E-ANCHOR', '担保时点', j + 1, "该行缺 as_of／数据日（规格：代理面每条都要快照时点，取不到则整行改挂未取到声明）")
            if len(cs) < 5 or (not SRC_PAT.search(cs[4]) and blank(cs[2])):
                add('E-ANCHOR', '担保出处', j + 1, "该行无出处且内容留空（规格：内容格照返货字段值逐字填，出处格放链接或字段定位；两者皆无则删该行）")
    if '制裁执法面' in secs:
        i0, i1 = secs['制裁执法面']
        for j, cs in row_items(lines, i0, i1):
            if all(blank(c) for c in cs[1:]):
                continue
            if not DATE_PAT.search(cs[2]):
                add('E-ANCHOR', '制裁日期', j + 1, "该行缺日期（规格：动作日期照返货逐字填）")
            if not (SRC_PAT.search(cs[3]) or DOCNO_PAT.search(cs[3])):
                add('E-ANCHOR', '制裁锚', j + 1, "该行缺 document_number／URL 锚（规格：实测正例双锚在案，取不到锚就不列该行）")

    # ---- 道三 红线 ----
    for j, ln in enumerate(lines):
        for pat, spec in ((RATING, '本件不产出整体风险／等级／评级／违约概率／评分一类输出（规格：SKILL §3 红线；要写就写「不评、不算」这类否定句或删句）'),
                          (SAFEWORD, '出现「无风险／没被查过」一类整句（规格：扫不到条目只写「窗口内未检索到」＋窗口，不等于没有）'),
                          (UNIFIED, '出现「统一 ID」一类措辞（规格：跨域统一主体 ID 不通；主键＝六位代码＋各域自立消歧）')):
            for m in pat.finditer(ln):
                if not guarded(ln, m):
                    add('E-BANWORD', '红线', j + 1, f"{spec}｜命中「{m.group(0)}」")
                    break
    if '未达与待核清单' in secs:
        i0, i1 = secs['未达与待核清单']
        for j, cs in row_items(lines, i0, i1):
            if not cs or not any(f in cs[0] for f in FACES):
                continue
            if any('已有腿' in w for w in chosen(cs[1])):
                if not (SRC_PAT.search(cs[2]) or DATE_PAT.search(cs[2])):
                    add('E-BANWORD', '装腿', j + 1, f"「{cs[0]}」勾了「已有腿」却拿不出本次出处（规格：本件无该腿；确有新依据就附本次链接或日期，否则改勾「通道当前未达」）")

    # ---- 道四 计数与申报 ----
    if '主体行' in secs:
        i0, i1 = secs['主体行']
        cand = [ln for ln in lines[i0:i1] if '候选' in ln]
        if not cand:
            add('E-COVERAGE', '候选处理', i0 + 1, "主体行缺「候选处理」勾选行（规格：单一命中／多候选·已列出待用户点／不适用，恰勾一个——多候选不代选）")
        elif len(chosen(cand[0])) != 1:
            add('E-COVERAGE', '候选处理', i0 + 1, f"候选处理勾了 {len(chosen(cand[0]))} 个（规格：恰勾一个）")
    if '处罚与监管措施表' in secs:
        i0, i1 = secs['处罚与监管措施表']
        has_rows = any(not all(blank(c) for c in cs[1:]) for _, cs in row_items(lines, i0, i1))
        if not has_rows:
            dl = [ln for ln in lines[i0:i1] if ZERO_DECL.search(ln)]
            picked = [w for ln in dl for mk, w in ticks(ln) if mk == '☑' and ZERO_DECL.search(w)]
            if not picked:
                add('E-COVERAGE', '零条声明', i0 + 1, "处罚表零条目且零命中声明**没勾上**（规格：勾「窗口内未检索到」并把窗口起止写进被勾那句；光留着未勾的选项文字不算声明）")
            elif not DATE_PAT.search(picked[0]):
                add('E-COVERAGE', '零条声明', i0 + 1, "零命中声明没带窗口起止日期（规格：被勾那句里要出现「窗口 YYYY-MM-DD~YYYY-MM-DD」）")
    if '对外担保要点' in secs:
        i0, i1 = secs['对外担保要点']
        has_rows = any(not all(blank(c) for c in cs[1:]) for _, cs in row_items(lines, i0, i1))
        if not has_rows:
            picked = [w for ln in lines[i0:i1] for mk, w in ticks(ln) if mk == '☑' and GUA_ZERO.search(w)]
            if not picked:
                add('E-COVERAGE', '担保零行', i0 + 1, "担保面零条目且「返货 0 行」申报没勾上（规格：0 行也要点名，选项里带上 as_of；未勾的选项文字不算声明）")
            elif '__' in picked[0] or not DATE_PAT.search(picked[0]):
                add('E-COVERAGE', '担保零行', i0 + 1, "0 行申报里的 as_of 仍是占位或没落成日期形（规格：快照时点照返货逐字填）")
            elif not UNRESOLVED.search(picked[0]):
                add('E-COVERAGE', '担保零行', i0 + 1, "0 行申报未辨「真无」与「抽取缺」（规格：envelope 无该自证位，须在句内写未辨并挂第五段待核）")
    if '制裁执法面' in secs:
        i0, i1 = secs['制裁执法面']
        blob = '\n'.join(lines[i0:i1])
        state = [ln for ln in lines[i0:i1] if '本面状态' in ln]
        if not state:
            add('E-COVERAGE', '制裁状态', i0 + 1, "缺「本面状态」勾选行（规格：已跑列出／已跑未命中／未跑不涉跨境／未跑原因待核，恰勾一个）")
        else:
            picked = chosen(state[0])
            if len(picked) != 1:
                add('E-COVERAGE', '制裁状态', i0 + 1, f"本面状态勾了 {len(picked)} 个（规格：恰勾一个；不适用也要点名，不留空顶替）")
            elif any('已跑' in w for w in picked) and ('未命中' in picked[0]) and not DATE_PAT.search(picked[0]):
                add('E-COVERAGE', '制裁窗口', i0 + 1, "「已跑未命中」没带窗口起止（规格：未命中要写窗口与库面申报，否则与「没跑」无从区分）")
        if any('已跑' in w for w in (chosen(state[0]) if state else [])):
            nm = [ln for ln in lines[i0:i1] if '名形双查' in ln]
            if not nm:
                add('E-COVERAGE', '名形双查', i0 + 1, "制裁面跑过却无「名形双查声明」行（规格：机构全称可致零命中是实测教训，简称与全称各查才算跑完）")
            elif len(chosen(nm[0])) != 1:
                add('E-COVERAGE', '名形双查', i0 + 1, "名形双查声明未恰勾一个（规格：各查过一次／只查了一种／不适用，三选一）")
    if '未达与待核清单' in secs:
        i0, i1 = secs['未达与待核清单']
        rows = {cs[0]: cs for _, cs in row_items(lines, i0, i1) if cs and any(f in cs[0] for f in FACES)}
        for f in FACES:
            hit = [k for k in rows if f in k]
            if not hit:
                add('E-COVERAGE', '三面点名', i0 + 1, f"未达清单缺「{f}」一行（规格：三面逐面点名，缺面等于把没腿的说成扫过了）")
            elif len(chosen(rows[hit[0]][1])) != 1:
                add('E-COVERAGE', '三面点名', i0 + 1, f"「{f}」状态未恰勾一个（规格：通道当前未达／声称已有腿，二选一并附依据）")
        if '[待人工]' not in '\n'.join(lines[i0:i1]):
            add('E-COVERAGE', '申报', i0 + 1, "待核清单缺 [待人工] 汇总位（规格：整体性判断与需人看的项全挂此节）")

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
    print("PASS: " + path.name + "（五段齐、时点三件就位、逐条挂出处与日期、综合判断类输出零命中、三面未达逐个点名）")
    print(f"       扫过 {n} 行，发条 0 条；判定与阈值全集以本脚本现值为准（--help 看四道说明）")
    return 0


# 反例档：窗口终点写成「待定」——时点三件里只坏一个端点，好样其余不动
def selftest():
    good, bad = HERE / 'fixtures' / 'good-scan-card.md', HERE / 'fixtures' / 'bad-scan-card.md'
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
    mu = HERE / 'fixtures' / 'mut-window-tbd-card.md'
    if not mu.is_file():
        print(f"SELFTEST FAIL: 反例夹具缺失 {mu}")
        return 1
    mf, mnl = check(mu)
    mcode = [(m.group(1), m.group(2)) for m in (re.match(r'\[(E-[A-Z]+)\] \[([^\]]+)\]', x) for x in mf) if m]
    mhit = ('E-FORMAT', '时点') in mcode
    mnamed = any('终点没落成日期形' in x for x in mf)
    print(f"selftest 反例档：{mu.name} 扫过 {mnl} 行，发条 {len(mf)} 条（规格 ≥1、须发 E-FORMAT／时点、详行点名病灶）")
    for x in mf[:3]:
        print('   实发详行 → ' + x[:130])
    if not mf:
        print('   意外：单点反例过了闸（缺陷——本档治的正是「判据只查其一」把门过宽）')
        ok = False
    elif not mhit:
        print('   未命中预期码与道名 → 期望 E-FORMAT／时点，实发 %s' % ('、'.join(a + '／' + b for a, b in mcode) or '无'))
        ok = False
    elif not mnamed:
        print("   发条未点名病灶 → 详行里找不到「终点没落成日期形」")
        ok = False
    print(f"selftest: {'ALL GREEN' if ok else 'FAIL'}（好样 {len(goods)} 枚·发条 {len(gf)} 条（规格 0）· 坏样四道 {len(got)}/{len(want)} · 反例档 {'发红' if (mf and mhit and mnamed) else '未发红!'}）")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="校验一张风险扫描卡是否合五段契约与红线（零网络）。",
        epilog="出口：FAIL 一行计数＋逐条 E-* 详行＋码表；PASS 一行＋两类计数。判定全集在本脚本现值。")
    ap.add_argument('card', nargs='?', help='待校验的卡（markdown）')
    ap.add_argument('--selftest', action='store_true', help='跑包内守护样（好样、坏样与单点反例各档，档名与枚数由末行自报）')
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
