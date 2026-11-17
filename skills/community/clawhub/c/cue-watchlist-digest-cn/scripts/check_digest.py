#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_digest.py — 校验一份自选清单增量日报是否合 `SKILL.md` §3 五段契约与 §4/§6 红线（零网络）。

用法：
    python3 check_digest.py <digest.md> [--run <run.json>] [--sources <sources.jsonl>]
                                                            校验一份日报（两缺省都取日报同目录同名件）
    python3 check_digest.py --selftest                          七档自证：好样／零新增样须过、坏样四道全发、反证矩阵逐枚自报、
                                                                跨日重放链须逐字节同、来源对账好形须过且坏形必红、
                                                                生成器坏输入须出一句人话且不得抛 Traceback
    python3 check_digest.py --help                              本说明

第四档＝反证矩阵（长在包里，不靠外部脚本）：对好样做单点破坏，每枚必须发出预期的码与道名；
另附一枚正向不误拦（合法形必须零发条）。锚点是「好样里唯一命中的那行」——锚失配即判该枚 FAIL，
所以守护样一旦漂移，矩阵会先叫，不会静默恒真。

出口形制（与姊妹件同族）：失败＝一行 "FAIL: <文件>（N 条）" ＋逐条先打 `E-*` 码的详行 ＋末行「码表:」；
全过＝一行 "PASS: <文件>（…）" 并印「扫过行数」「发条数」两类计数。
行数口径：`扫过 N 行` 按 `split('\\n')` 计＝`wc -l` 现值 +1。

五道（判定全集在本脚本；SKILL §5 是验收合同）：
    道一 E-FORMAT   五段齐且有序＋头部三件套＋时点七项就位且落成日期形（asof／窗口缺一不可）
    道二 E-ANCHOR   今日新增每行要日期＋出处锚；近端变更要「前值 → 现值」两侧或明写取不到；来源索引逐条给出处
    道三 E-BANWORD  评级／目标价／走势／买卖建议／行情与资金流承诺／「无风险」类断言落在非「需人工」节且未挂 [待人工]
    道四 E-COVERAGE 日报声明的主体数／实跑域数／返货腿数／新增数／清单外返货数与 run.json 实况对不上；零新增未勾声明或未带窗口；
                    有腿未取到却未点名；待核段缺 [待人工] 汇总
    道五 E-SOURCE   日报第五段来源索引与同目录 sources.jsonl 双向对账：索引里每条出处都要在件中有对应行，件里每条出处也要在索引里见得到；
                    件缺、件行坏了、两处单向缺都算断链（本码是本包自有第五枚，不属姊妹件逐字同源的四枚家族）

**它是形制闸，不是事实闸**：`exit 0` 只证明形制合式与自证一致，不证明数字为真——事实层由逐条回官方原文承担。
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

# 与姊妹件逐字同源的四枚码（第五枚 E-LEDGER 属账本状态机面，本件无账本，故不启用）
FAMILY = ('E-FORMAT', 'E-ANCHOR', 'E-BANWORD', 'E-COVERAGE')
E_LEGEND = {
    "E-FORMAT":   "形制/输入/表序不合式→按该行括号内规格改形制后复跑",
    "E-ANCHOR":   "锚/证据链缺失或断链→补合式锚或删除该条,禁虚构",
    "E-BANWORD":  "禁词/评级/幻觉/待人工域命中→改中性陈述或删除,零豁免区",
    "E-COVERAGE": "计数/覆盖/申报对不上→逐类补账或如实标未检索到",
    # 本包自有第五枚：不属上面那枚家族同源的四个，改动不需要同步姊妹件
    "E-SOURCE":   "来源索引与 sources.jsonl 双向对不上→重跑 digest.py 让两处同批写出,禁手工补行或删行",
}

SECTIONS = ['时点与范围', '今日新增', '近端变更', '需人工', '来源索引']
CN_NUM = ['一', '二', '三', '四', '五']
HEAD_MARKS = ('AI 整理初稿', '请回官方原文核对', '不构成投资建议')
TIME_KEYS = (('asof 时刻', 'YYYY-MM-DD 或 YYYY-MM-DD HH:MM'),
             ('清单规模', 'N 家，须与 run.json 的 subjects 一致'),
             ('本次实跑域数', '取自返货回显，不外推'),
             ('本次返货腿数', '返货实际覆盖的腿数'),
             ('上次快照日期', 'YYYY-MM-DD 或「无（首次运行）」'),
             ('检索窗口', 'YYYY-MM-DD~YYYY-MM-DD'),
             ('清单外返货（未并入本清单）', 'N 条，与 run.json 的 offlist_skipped 一致；零条也写 0，不删行'))
DATE = re.compile(r'\d{4}-\d{2}-\d{2}')
ASOF = re.compile(r'^\d{4}-\d{2}-\d{2}([ T]\d{2}:\d{2}(:\d{2})?)?$')
URL = re.compile(r'https?://|www\.|\.cn|\.com|\.gov|巨潮|交易所')
BANNED = re.compile(r'风险等级|风险评级|信用评级|违约概率|评分模型|目标价|评级为|建议买入|建议卖出|'
                    r'看涨|看跌|走势|涨停|抄底|资金流向|北向资金|持续监控|自动提醒|每天推给你|'
                    r'无风险|没有风险|没被查过|从未被查')
NEG_WORDS = ('不', '未', '禁', '勿', '拒', '非', '没')
CLAUSE_SPLIT = re.compile(r'[。；;！!？?：:，,、〕）」』]')
NUM = re.compile(r'(\d+)')


def clause_before(line, start):
    idx = 0
    for m in CLAUSE_SPLIT.finditer(line[:start]):
        idx = m.end()
    return line[idx:start]


def guarded(line, m):
    """否定式免责句不算违例：只看命中点所在小句内有无否定词。"""
    return any(n in clause_before(line, m.start()) for n in NEG_WORDS)


def blank(s: str) -> bool:
    s = s.strip()
    return (not s) or set(s) <= {'-', '—'} or '__' in s or s in {'☐', '－', '—'}


def cells(line: str):
    return [c.strip() for c in line.strip().strip('|').split('|')]


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


def ticks(cell: str):
    return re.findall(r'([☑☐])\s*([^☐☑]+)', cell)


def read_sources(sp: Path):
    """件是 jsonl：一行一事件。返回 (逐行 (行号, url), 坏行 (行号, 病灶语))；空行跳过，坏行不静默吞。

    坏行两种：不是合法 JSON；或是合法 JSON 但不是对象（数组／字符串／数字／布尔／null）——
    后者按实收类型点名，不在这里抛 AttributeError（闸自己被坏件崩掉，就等于把门交给坏件）。"""
    pairs, bad = [], []
    for i, ln in enumerate(sp.read_text(encoding='utf-8').split('\n'), 1):
        if not ln.strip():
            continue
        try:
            obj = json.loads(ln)
        except json.JSONDecodeError:
            bad.append((i, '不是合法 JSON'))
            continue
        if not isinstance(obj, dict):
            bad.append((i, '是 JSON %s，本件每行只收对象（实收类型 %s）' % (type(obj).__name__, type(obj).__name__)))
            continue
        pairs.append((i, str(obj.get('url', '')).strip()))
    return pairs, bad


def section_ranges(lines):
    heads = {}
    for i, ln in enumerate(lines):
        m = re.match(r'^##\s+([一二三四五六七八九])、(.+?)\s*$', ln)
        if m:
            heads.setdefault(m.group(2).strip(), i)
    order = sorted(heads.values())
    return {name: (idx, min([o for o in order if o > idx], default=len(lines)))
            for name, idx in heads.items()}


def check(path: Path, run_path: Path | None, sources_path: Path | None = None):
    lines = path.read_text(encoding='utf-8').split('\n')
    finds = []

    def add(code, lane, lineno, detail):
        finds.append(f"[{code}] [{lane}] 第 {lineno} 行：{detail}")

    run = None
    if run_path and run_path.is_file():
        try:
            run = json.loads(run_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            add('E-FORMAT', '实况', 1, f"{run_path.name} 不是合法 JSON（规格：计数比对以 run.json 实况为唯一凭据，坏了就重跑 digest.py）")
    elif run_path:
        add('E-FORMAT', '实况', 1, f"缺 {run_path.name}（规格：日报必须与本次 run.json 同目录成对交付，计数比对无从进行）")

    # ---- 道一 形制 ----
    hi = [i for i, ln in enumerate(lines) if ln.strip() == '## 头部自标']
    if not hi:
        add('E-FORMAT', '头部', 1, "缺「## 头部自标」段（规格：含『AI 整理初稿』『请回官方原文核对』『不构成投资建议』三件套）")
    else:
        i0 = hi[0]
        i1 = min([i for i, ln in enumerate(lines) if i > i0 and ln.startswith('## ')], default=len(lines))
        blob = '\n'.join(lines[i0:i1])
        for need in HEAD_MARKS:
            if need not in blob:
                add('E-FORMAT', '头部', i0 + 1, f"头部自标缺『{need}』（规格：三件套逐字齐）")
    secs = section_ranges(lines)
    for n, name in zip(CN_NUM, SECTIONS):
        if name not in secs:
            add('E-FORMAT', '五段', 1, f"缺「## {n}、{name}」段（规格：五段齐且按一二三四五有序）")
    if all(s in secs for s in SECTIONS):
        idx = [secs[s][0] for s in SECTIONS]
        if idx != sorted(idx):
            add('E-FORMAT', '五段', idx[0] + 1, "五段次序与契约不一致（规格：时点与范围→今日新增→近端变更→需人工→来源索引）")
    if '时点与范围' in secs:
        i0, i1 = secs['时点与范围']
        for key, spec in TIME_KEYS:
            hit = [j for j in range(i0, i1) if key in lines[j] and lines[j].strip().startswith('|')]
            if not hit:
                add('E-FORMAT', '时点', i0 + 1, f"时点段缺「{key}」一行（规格：{spec}）")
                continue
            j = hit[0]
            cs = cells(lines[j])
            val = cs[1] if len(cs) > 1 else ''
            if blank(val):
                add('E-FORMAT', '时点', j + 1, f"「{key}」未填（规格：{spec}）")
            elif key == 'asof 时刻' and not ASOF.match(val):
                add('E-FORMAT', '时点', j + 1, f"「asof 时刻」不是日期形（规格：{spec}）")
            elif key == '检索窗口' and not (val.count('~') == 1 and all(DATE.fullmatch(x.strip()) for x in val.split('~'))):
                add('E-FORMAT', '时点', j + 1, f"「检索窗口」没给起止两个日期（规格：{spec}）")
    if '来源索引' in secs:
        i0, i1 = secs['来源索引']
        if 'sources.jsonl' not in '\n'.join(lines[i0:i1]):
            add('E-FORMAT', '来源', i0 + 1, "来源索引段没点名 sources.jsonl（规格：日报与逐条来源索引件一一对应，缺对应物即无从回查）")

    # ---- 道二 锚 ----
    if '今日新增' in secs:
        i0, i1 = secs['今日新增']
        for j, cs in row_items(lines, i0, i1):
            if len(cs) < 6 or all(blank(c) for c in cs[1:]):
                continue
            if not DATE.search(cs[4]):
                add('E-ANCHOR', '新增日期', j + 1, "该行缺事件日期（规格：照返货逐字填 YYYY-MM-DD）")
            if not URL.search(cs[5]):
                add('E-ANCHOR', '新增出处', j + 1, "该行出处锚不合规（规格：官方链接或公告编号；取不到就删该行，不补猜）")
    if '近端变更' in secs:
        i0, i1 = secs['近端变更']
        for j, cs in row_items(lines, i0, i1):
            if len(cs) < 5 or all(blank(c) for c in cs[1:]):
                continue
            if '不适用' in ' '.join(cs) or '取不到' in ' '.join(cs):
                continue
            if '→' not in cs[3] or any(blank(x) for x in cs[3].split('→')):
                add('E-ANCHOR', '变更两值', j + 1, "前值／现值不成对（规格：要「前值 → 现值」两侧齐；取不到前值就明写取不到，不编造）")
            if not URL.search(cs[4]):
                add('E-ANCHOR', '变更出处', j + 1, "该行依据锚不合规（规格：同上，须能回查）")
    if '来源索引' in secs:
        i0, i1 = secs['来源索引']
        for j, cs in row_items(lines, i0, i1):
            if len(cs) < 3 or all(blank(c) for c in cs[1:]) or '不适用' in ' '.join(cs):
                continue
            if not URL.search(cs[1]):
                add('E-ANCHOR', '来源锚', j + 1, "来源索引行缺出处（规格：与 sources.jsonl 逐条对应的出处链接或公告编号）")

    # ---- 道三 红线 ----
    judge0, judge1 = secs.get('需人工', (-1, -1))
    for j, ln in enumerate(lines):
        if judge0 <= j < judge1:
            continue
        for m in BANNED.finditer(ln):
            if guarded(ln, m) or '[待人工]' in ln:
                continue
            add('E-BANWORD', '评级行情', j + 1, f"命中「{m.group(0)}」——评级／目标价／走势／行情资金流承诺与「无风险」类断言只许挂在第四段（规格：SKILL §4；其余段落要写就同行挂 [待人工]，或改中性陈述）")
            break

    # ---- 道四 计数与申报 ----
    if run:
        want = [('清单规模', run.get('subjects'), '家'),
                ('本次实跑域数', run.get('legs_called'), ''),
                ('本次返货腿数', run.get('legs_returned'), ''),
                ('清单外返货（未并入本清单）', run.get('offlist_skipped'), '条')]
        i0, i1 = secs.get('时点与范围', (0, len(lines)))
        for key, val, unit in want:
            if val is None:
                continue
            hit = [j for j in range(i0, i1) if key in lines[j]]
            if not hit:
                continue
            got = NUM.search(cells(lines[hit[0]])[1] if len(cells(lines[hit[0]])) > 1 else '')
            if not got or int(got.group(1)) != int(val):
                add('E-COVERAGE', '计数比对', hit[0] + 1, f"「{key}」与 run.json 实况（{val}{unit}）对不上（规格：计数一律取本次返货回显，不凭记忆、不外推）")
        i0, i1 = secs['今日新增'] if '今日新增' in secs else (0, len(lines))
        listed = [cs for _, cs in row_items(lines, i0, i1) if len(cs) >= 6 and not all(blank(c) for c in cs[1:])]
        new_count = run.get('new_count')
        if new_count is not None and len(listed) != int(new_count):
            add('E-COVERAGE', '新增数', i0 + 1, f"今日新增列出 {len(listed)} 行，run.json 记 {new_count} 条（规格：两者必须相等，多写少写都是虚报）")
        decl = [ln for ln in lines[i0:i1] if '零新增声明' in ln]
        if new_count == 0:
            picked = [w for ln in decl for mk, w in ticks(ln) if mk == '☑']
            if not any('未检索到' in w for w in picked):
                add('E-COVERAGE', '零新增申报', i0 + 1, "零新增却没勾「窗口内未检索到新增」（规格：没检索到 ≠ 没有发生，必须勾声明并带窗口日期）")
            elif not any(DATE.search(w) for w in picked):
                add('E-COVERAGE', '零新增申报', i0 + 1, "零新增声明没带窗口起止日期（规格：要能核对到检索参数，否则与「没跑」无从区分）")
        elif decl and any('未检索到' in w for ln in decl for mk, w in ticks(ln) if mk == '☑'):
            add('E-COVERAGE', '零新增申报', i0 + 1, "run.json 记有新增却勾了「未检索到新增」（规格：申报与实况互斥，二者必居其一）")
        miss = [ln for ln in lines if '本腿未取到' in ln]
        called, got_legs = run.get('legs_called'), run.get('legs_returned')
        if isinstance(called, int) and isinstance(got_legs, int) and called > got_legs and not miss:
            add('E-COVERAGE', '缺腿点名', 1, f"实跑 {called} 域而返货只覆盖 {got_legs} 腿，日报未点名「本腿未取到」（规格：一腿挂不挡全篇，但必须点名挂第四段待人工）")
    if '需人工' in secs:
        i0, i1 = secs['需人工']
        if '[待人工]' not in '\n'.join(lines[i0:i1]):
            add('E-COVERAGE', '汇总', i0 + 1, "需人工段缺 [待人工] 汇总位（规格：评级／目标价／走势与资金面解读全挂此节）")

    # ---- 道五 来源对账（第五段索引 ⇄ sources.jsonl 双向） ----
    idx_rows = []
    if '来源索引' in secs:
        i0, i1 = secs['来源索引']
        for j, cs in row_items(lines, i0, i1):
            if len(cs) < 2 or all(blank(c) for c in cs[1:]) or '不适用' in ' '.join(cs) or '未检索到' in ' '.join(cs):
                continue
            idx_rows.append((j + 1, cs[1]))
    sp = sources_path or (path.parent / 'sources.jsonl')
    head_line = secs['来源索引'][0] + 1 if '来源索引' in secs else 1
    if idx_rows and not sp.is_file():
        add('E-SOURCE', '来源对账', idx_rows[0][0],
            f"来源索引列了 {len(idx_rows)} 条出处，同目录却没有 {sp.name}（规格：两处由 digest.py 同批写出，缺件即索引全部无从回查）")
    elif sp.is_file():
        pairs, bad = read_sources(sp)
        for i, why in bad:
            add('E-SOURCE', '来源对账', i, f"{sp.name} 第 {i} 行{why}（规格：逐行一事件的对象，坏行等同断链——重跑 digest.py 整件重出，不手补这一行）")
        src_urls = {u for _n, u in pairs if u}
        idx_urls = {u for _n, u in idx_rows if u}
        for n, u in idx_rows:
            if u and u not in src_urls:
                add('E-SOURCE', '来源对账', n,
                    f"来源索引第 {n} 行的出处「{u}」在 {sp.name} 里没有对应行（规格：索引里每条都要能回查到件里的一行；补行请重跑 digest.py，不手写）")
        for n, u in pairs:
            if u and u not in idx_urls:
                add('E-SOURCE', '来源对账', head_line,
                    f"{sp.name} 第 {n} 行的出处「{u}」未见于日报来源索引（规格：双向都要见得到，单向多写同样是断链）")
    return finds, len(lines)


def report(path, finds, n):
    if finds:
        print(f"FAIL: {path.name}（{len(finds)} 条）")
        for f in finds:
            print('  - ' + f)
        codes = sorted({re.match(r'\[(E-[A-Z]+)\]', f).group(1) for f in finds})
        print('  码表: ' + '; '.join(f'{c}→{E_LEGEND[c]}' for c in codes))
        return 1
    print("PASS: " + path.name + "（五段齐、时点七项落成日期形、每行有锚、评级与行情承诺零命中、五类计数与 run.json 对上、来源索引与 sources.jsonl 双向对上）")
    print(f"       扫过 {n} 行，发条 0 条；判定与阈值全集以本脚本现值为准（--help 看五道说明）")
    return 0


def _lane(finding):
    m = re.match(r'\[(E-[A-Z]+)\] \[([^\]]+)\]', finding)
    return (m.group(1), m.group(2)) if m else ('?', '?')


def probe_matrix(md, run, tmp: Path, sources: str):
    """第四档：单点破坏每枚必须发出预期的码与道名；一枚正向不误拦（合法形须零发条）。

    锚点从好样文本里现场取（要求唯一命中）；锚失配＝该枚判 FAIL 并说明锚在文本里出现几处——
    这样守护样漂移会先叫出来，而不是让破坏样悄悄"通过"（防恒真）。"""
    out = []

    def one(name, expect, md2, run2, anchor_n=1, drop_run=False, src2=None):
        exp = expect if isinstance(expect, str) else '%s／%s' % expect
        if anchor_n != 1:
            out.append((name, exp, '锚失配（好样里命中 %d 处）' % anchor_n, False, []))
            return
        d = tmp / name
        d.mkdir(parents=True, exist_ok=True)
        f = d / 'digest.md'
        f.write_text(md2, encoding='utf-8')
        rp = d / 'run.json'
        if drop_run:
            rp = d / 'run.absent.json'
        else:
            rp.write_text(json.dumps(run2, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        sp = d / 'sources.jsonl'
        sp.write_text(sources if src2 is None else src2, encoding='utf-8')
        finds, _n = check(f, rp, sp)
        lanes = [_lane(x) for x in finds]
        if expect == '零发条':
            got = '零发条' if not lanes else '误拦：%s／%s（共 %d 条）' % (lanes[0][0], lanes[0][1], len(lanes))
            out.append((name, exp, got, not lanes, finds))
        else:
            hit = next((i for i, l in enumerate(lanes, 1) if l == expect), 0)
            got = ('%s／%s（第 %d／共 %d 条）' % (expect[0], expect[1], hit, len(lanes)) if hit else
                   ('未命中：零发条' if not lanes else
                    '未命中：首条 %s／%s（共 %d 条）' % (lanes[0][0], lanes[0][1], len(lanes))))
            out.append((name, exp, got, bool(hit), finds))

    def only(prefix):
        hits = [ln for ln in md.split('\n') if ln.startswith(prefix)]
        return (hits[0] if len(hits) == 1 else None, len(hits))

    asof_row, n1 = only('| asof 时刻 |')
    size_row, n2 = only('| 清单规模 |')
    called_row, n3 = only('| 本次实跑域数 |')
    off_row, n4 = only('| 清单外返货')
    leg_rows = [ln for ln in md.split('\n') if '本腿未取到' in ln]
    add_rows = [ln for ln in md.split('\n') if re.match(r'^\| \d+ \| .+（\d{6}） \|', ln)]
    decl_rows = [ln for ln in md.split('\n') if '零新增声明' in ln]
    blank = '| 1 | | | | | |'

    one('PB1-缺第五段', ('E-FORMAT', '五段'), re.sub(r'\n## 五、来源索引[\s\S]*', '\n', md), run)
    one('PB2-时点占位', ('E-FORMAT', '时点'), md.replace(asof_row, '| asof 时刻 | ____ |', 1) if n1 == 1 else md, run, n1)
    one('PB3-出处删空', ('E-ANCHOR', '新增出处'),
        md.replace(add_rows[0], add_rows[0].rsplit('|', 2)[0] + '| | |', 1) if add_rows else md, run,
        1 if add_rows else 0)
    one('PB4-评级入正文', ('E-BANWORD', '评级行情'),
        md.replace(add_rows[0], add_rows[0] + '\n> 机构给予买入评级，目标价 30 元。\n', 1) if add_rows else md,
        run, 1 if add_rows else 0)
    one('PB5-规模虚报', ('E-COVERAGE', '计数比对'),
        md.replace(size_row, '| 清单规模 | 9 家 |', 1) if n2 == 1 else md, run, n2)
    one('PB6-缺腿未点名', ('E-COVERAGE', '缺腿点名'),
        md.replace(leg_rows[0], '| 2 | 其他事项 | `[待人工]` |', 1) if len(leg_rows) == 1 else md, run, len(leg_rows))
    one('PB9-清单外数虚报', ('E-COVERAGE', '计数比对'),
        md.replace(off_row, re.sub(r'\d+', '9999', off_row, count=1), 1) if n4 == 1 else md, run, n4)
    one('PB10-清单外行删掉', ('E-FORMAT', '时点'),
        md.replace('\n' + off_row, '', 1) if n4 == 1 else md, run, n4)
    # PB11／PB12：来源对账的兩個方向各一枚——索引有、件里缺该行；件里有、索引没该行
    src_lines = [ln for ln in sources.split('\n') if ln.strip()]
    idx_url_rows = [ln for ln in md.split('\n') if re.match(r'^\| \d+ \| https?://', ln)]

    def url_of(line):
        try:
            return str(json.loads(line).get('url', '')).strip()
        except json.JSONDecodeError:
            return ''

    if len(src_lines) >= 2 and len(idx_url_rows) >= 2:
        second = cells(idx_url_rows[1])[1]
        kept = [ln for ln in src_lines if url_of(ln) != second]
        if len(kept) < len(src_lines):
            one('PB11-索引有件里缺', ('E-SOURCE', '来源对账'), md, run, 1,
                src2=''.join(ln + '\n' for ln in kept))
        else:
            out.append(('PB11-索引有件里缺', 'E-SOURCE／来源对账',
                        '锚失配（索引第二行 %s 在件里无同 URL 行可删）' % second, False, []))
        one('PB12-件里有索引缺', ('E-SOURCE', '来源对账'), md.replace(idx_url_rows[1] + '\n', '', 1), run, 1)
    else:
        detail = '锚失配（件行 %d／索引 URL 行 %d）' % (len(src_lines), len(idx_url_rows))
        out.append(('PB11-索引有件里缺', 'E-SOURCE／来源对账', detail, False, []))
        out.append(('PB12-件里有索引缺', 'E-SOURCE／来源对账', detail, False, []))
    # PB7：实况记零新增、表里空行、两条声明都没勾 → 必须发「零新增未申报」
    if len(decl_rows) == 1 and len(add_rows) >= 1:
        md7 = md.replace(decl_rows[0], decl_rows[0].replace('☑', '☐'), 1)
        for r in add_rows:
            md7 = md7.replace(r, blank, 1)
        r7 = dict(run)
        r7['new_count'] = 0
        one('PB7-零新增未勾', ('E-COVERAGE', '零新增申报'), md7, r7, 1)
    else:
        out.append(('PB7-零新增未勾', 'E-COVERAGE／零新增申报',
                    '锚失配（声明行 %d 处／新增行 %d 处）' % (len(decl_rows), len(add_rows)), False, []))
    one('PB8-无run成对', ('E-FORMAT', '实况'), md, run, 1, drop_run=True)
    # 正向一枚：把「实跑 5 域／返货 3 域＋缺腿点名」改成两数相等且删掉点名行——合法形，不许误拦
    if n3 == 1 and len(leg_rows) == 1:
        md3 = md.replace(called_row, re.sub(r'\d+', '3', called_row, count=1), 1)
        md3 = md3.replace(leg_rows[0], '', 1)
        md3 = re.sub(r'\n{3,}', '\n\n', md3)
        r3 = dict(run)
        r3.update({'legs_called': 3, 'legs_returned': 3, 'missing_legs': []})
        one('POS-无缺腿合法形', '零发条', md3, r3, 1)
    else:
        out.append(('POS-无缺腿合法形', '零发条',
                    '锚失配（实跑域数行 %d 处／点名行 %d 处）' % (n3, len(leg_rows)), False, []))
    return out


def replay_chain(tmp: Path):
    """五档 跨日重放：包内夹具走 init → day1 → day2 → day2 重放，全链现场跑。

    断言：①重放产物与当日首跑逐字节同；②new_count 不变（当日 1 条）；③run.json 至多差
    idempotent_replay 一键；④首跑与重放两态都过五道闸（零发条）；⑤窗口存量（3 条）大于当日增量（1 条）——
    这一条使「把重放退回窗口存量」的旧态必红：旧态会呈 3≠1，本档即判不符；⑥重放态的来源索引行数＝
    sources.jsonl 行数且件非空（两处不同批写出时这一条必红）。"""
    fx, dig, init = HERE / 'fixtures', HERE / 'digest.py', HERE / 'init_watchlist.py'
    for n in ('replay-return.jsonl', 'replay-day1.jsonl', 'replay-day2.jsonl'):
        if not (fx / n).is_file():
            print(f'selftest 五档跨日重放：缺件 fixtures/{n}（规格：链上三件输入必须随包）')
            return False
    d = tmp / 'chain'
    d.mkdir(parents=True, exist_ok=True)

    def run(*args):
        r = subprocess.run([sys.executable, '-B'] + [str(a) for a in args], capture_output=True, text=True)
        return r.returncode, (r.stdout + r.stderr).strip()

    rc_init, _o_init = run(init, '--run-dir', d, '--subject', '999901', '--subject', '999902',
                          '--from-return', fx / 'replay-return.jsonl', '--quiet')
    rc1, o1 = run(dig, '--run-dir', d, '--events', fx / 'replay-day1.jsonl', '--asof', '2026-10-11 07:30',
                  '--window', '2026-09-11~2026-10-11', '--legs-called', '2', '--quiet')
    day1_run = json.loads((d / 'run.json').read_text(encoding='utf-8')) if (d / 'run.json').is_file() else {}
    rc2, o2 = run(dig, '--run-dir', d, '--events', fx / 'replay-day2.jsonl', '--asof', '2026-10-12 07:45',
                  '--window', '2026-09-12~2026-10-12', '--legs-called', '3', '--quiet')
    day_md = d / 'digest-2026-10-12.md'
    first_md = day_md.read_bytes() if day_md.is_file() else b''
    first_run = json.loads((d / 'run.json').read_text(encoding='utf-8')) if (d / 'run.json').is_file() else {}
    rc3, o3 = run(dig, '--run-dir', d, '--events', fx / 'replay-day2.jsonl', '--asof', '2026-10-12 07:45',
                  '--window', '2026-09-12~2026-10-12', '--legs-called', '3', '--quiet')
    replay_md = day_md.read_bytes() if day_md.is_file() else b''
    replay_run = json.loads((d / 'run.json').read_text(encoding='utf-8')) if (d / 'run.json').is_file() else {}
    f_first, n_first = check(day_md, d / 'run.json') if day_md.is_file() else ([], 0)
    src_f = d / 'sources.jsonl'
    src_lines = [ln for ln in (src_f.read_text(encoding='utf-8').split('\n') if src_f.is_file() else []) if ln.strip()]
    idx_rows = [ln for ln in (replay_md.decode('utf-8', 'ignore').split('\n') if replay_md else [])
                if re.match(r'^\| \d+ \| https?://', ln)]
    diff_keys = sorted(set(first_run) ^ set(replay_run)) or         sorted(k for k in set(first_run) & set(replay_run) if first_run[k] != replay_run[k])
    checks = [
        ('init 退码', rc_init, 0),
        ('day1 退码', rc1, 10),
        ('day2 首跑退码', rc2, 10),
        ('day2 重放退码', rc3, 10),
        ('day1 当日增量', day1_run.get('new_count'), 2),
        ('day1 窗口存量', day1_run.get('window_new_rows'), 2),
        ('重放产物与当日首跑逐字节同', first_md == replay_md and bool(first_md), True),
        ('new_count 不变', (first_run.get('new_count'), replay_run.get('new_count')), (1, 1)),
        ('窗口存量大于增量（旧态在此必红）', replay_run.get('window_new_rows'), 3),
        ('当日增量指纹集枚数', len(replay_run.get('new_fps') or []), 1),
        ('run.json 至多差 idempotent_replay', diff_keys, ['idempotent_replay']),
        ('重放态过闸零发条', len(f_first), 0),
        ('重放态 sources.jsonl 有行', bool(src_lines), True),
        ('索引行数与来源件行数同批', len(idx_rows), len(src_lines)),
    ]
    bad = [(n, got, want) for n, got, want in checks if got != want]
    print('selftest 五档跨日重放：init→day1→day2→day2 重放 现场跑｜断言 %d 条，不符 %d 条｜重放产物逐字节同＝%s，new_count 首跑/重放=%s/%s，窗口存量=%s，索引行/来源件行=%s/%s' % (
        len(checks), len(bad), '是' if first_md == replay_md and first_md else '否',
        first_run.get('new_count'), replay_run.get('new_count'), replay_run.get('window_new_rows'),
        len(idx_rows), len(src_lines)))
    for n, got, want in bad:
        print('   不符 → %s：实得 %s（规格 %s）' % (n, got, want))
    for x in f_first[:3]:
        print('   闸发条 → ' + x)
    return not bad


def source_pair(tmp: Path):
    """六档 来源对账：现场造「只变更、无新增」的输入跑生成器，断言两处同批写出；再把件里那一行删掉，断言 E-SOURCE 必红。

    这一档是「造出 PASS 的断链件」那类缺陷的直接反证：变更前生成器把变更腿的 URL 写进日报索引、
    却不写进 sources.jsonl，闸不读那个文件，于是一份索引可点、逐条回查却无的件照样 PASS。
    断言三件：①好形（索引行＝件行、且过闸零发条）；②坏形（件里删掉那一行必发 E-SOURCE，
    详行要点名缺的那条 URL 与所在行号）；③变更腿的字段齐（件里那行带 before／now）。"""
    d = tmp / 'src'
    d.mkdir(parents=True, exist_ok=True)
    url = 'http://www.cninfo.example/disc/600001-m245probe'

    def run(*args):
        r = subprocess.run([sys.executable, '-B'] + [str(a) for a in args], capture_output=True, text=True)
        return r.returncode, (r.stdout + r.stderr).strip()

    rc_init, _oi = run(HERE / 'init_watchlist.py', '--run-dir', d, '--subject', '600001', '--quiet')
    (d / 'events.jsonl').write_text(json.dumps({
        'code': '600001', 'name': '样本股份', 'type': '回购进展', 'date': '2026-10-16',
        'title': '关于回购进展情况的公告', 'url': url, 'kind': 'changed', 'leg': '回购',
        'item': '回购进展', 'before': '已回购 1.0%', 'now': '已回购 2.0%'}, ensure_ascii=False) + '\n',
        encoding='utf-8')
    rc_dig, _od = run(HERE / 'digest.py', '--run-dir', d, '--events', d / 'events.jsonl',
                      '--asof', '2026-10-17 09:00', '--window', '2026-09-17~2026-10-17',
                      '--legs-called', '1', '--quiet')
    md_f = d / 'digest-2026-10-17.md'
    src_f = d / 'sources.jsonl'
    good_lines = [ln for ln in (src_f.read_text(encoding='utf-8').split('\n') if src_f.is_file() else []) if ln.strip()]
    idx_rows = [ln for ln in (md_f.read_text(encoding='utf-8').split('\n') if md_f.is_file() else [])
                if re.match(r'^\| \d+ \| https?://', ln)]
    f_good, _ng = check(md_f, d / 'run.json', src_f) if md_f.is_file() else (['件未生成'], 0)
    rec = {}
    if good_lines:
        try:
            rec = json.loads(good_lines[0])
        except json.JSONDecodeError:
            rec = {}
    # 坏形：同一份日报，只把件里那一行删掉——索引有、件里无，必发 E-SOURCE
    d2 = tmp / 'src-bad'
    d2.mkdir(parents=True, exist_ok=True)
    shutil.copy(md_f, d2 / md_f.name) if md_f.is_file() else None
    (d2 / 'run.json').write_text((d / 'run.json').read_text(encoding='utf-8'), encoding='utf-8')
    (d2 / 'sources.jsonl').write_text('', encoding='utf-8')
    bad_md = d2 / md_f.name
    f_bad, _nb = check(bad_md, d2 / 'run.json', d2 / 'sources.jsonl') if bad_md.is_file() else (['件未生成'], 0)
    e_src = [x for x in f_bad if x.startswith('[E-SOURCE]')]
    names_url = any(url in x for x in e_src)
    has_lineno = any(re.match(r'^\[E-SOURCE\] \[来源对账\] 第 \d+ 行：', x) for x in e_src)
    # 同批的第三种坏形：件里某行是合法 JSON 但不是对象——闸必须发红，且自己不被坏件崩掉
    arr_src = HERE / 'fixtures' / 'bad-sources-array.jsonl'
    f_arr, _na = check(md_f, d / 'run.json', arr_src) if arr_src.is_file() and md_f.is_file() else (['缺件 bad-sources-array.jsonl'], 0)
    arr_esrc = [x for x in f_arr if x.startswith('[E-SOURCE]')]
    arr_tb = 'Traceback' in ' '.join(f_arr)
    checks = [
        ('init 退码', rc_init, 0),
        ('只变更无新增 生成退码', rc_dig, 0),
        ('日报已生成', md_f.is_file(), True),
        ('sources.jsonl 有行（变更前为 0）', len(good_lines) >= 1, True),
        ('索引行数＝件行数', len(idx_rows), len(good_lines)),
        ('索引那条 URL 在件里', bool(idx_rows) and cells(idx_rows[0])[1] == rec.get('url'), True),
        ('件里变更腿字段齐', ('before' in rec and 'now' in rec), True),
        ('好形过闸零发条', len(f_good), 0),
        ('坏形必发 E-SOURCE', len(e_src) >= 1, True),
        ('坏形详行点名缺的那条 URL', names_url, True),
        ('坏形详行带行号', has_lineno, True),
        ('件内非对象行也必发 E-SOURCE', len(arr_esrc) >= 1, True),
        ('闸自己不被非对象行崩（无 Traceback）', arr_tb, False),
        ('详行点出实收类型 list', any('list' in x for x in arr_esrc), True),
    ]
    bad_items = [(n, got, want) for n, got, want in checks if got != want]
    print('selftest 六档来源对账：现场跑生成器（只变更无新增）＋单变量反证＋件内非对象行 现场跑｜断言 %d 条，不符 %d 条｜索引行/件行=%s/%s，坏形发条=%s 条（%s），非对象行发条=%s 条' % (
        len(checks), len(bad_items), len(idx_rows), len(good_lines), len(e_src),
        ('点名 URL' if names_url else '未点名 URL'), len(arr_esrc)))
    for n, got, want in bad_items:
        print('   不符 → %s：实得 %s（规格 %s）' % (n, got, want))
    for x in e_src[:2]:
        print('   坏形实发详行 → ' + x[:150])
    return not bad_items


def bad_input_exit(tmp: Path):
    """七档 生成器坏输入出口：一行合法 JSON 但不是对象，须出一句人话、退码 1、且不抛 Traceback、不留半件。

    这一档钉的是 README 操作列里的承诺「写坏的行仍按取数错误报错」：曾经数组行能让 digest.py 直接
    AttributeError 崩在 load_events 里——退码巧合也是 1，但用户看到的是一坨 Traceback。
    五形各跑一次（数组／字符串／数字／null／布尔），夹具件跑数组形，其余四形在临时目录现造——
    夹具只随包一枚，不把五种写法都塞进包里。断言含「Traceback 计数＝0」与「未产出 digest／sources／run」。"""
    fx = HERE / 'fixtures' / 'bad-array-events.jsonl'
    if not fx.is_file():
        print('selftest 七档生成器坏输入：缺件 fixtures/bad-array-events.jsonl（规格：坏形夹具必须随包）')
        return False
    d = tmp / 'badexit'
    d.mkdir(parents=True, exist_ok=True)

    def run(*args):
        r = subprocess.run([sys.executable, '-B'] + [str(a) for a in args], capture_output=True, text=True)
        return r.returncode, r.stdout, r.stderr

    rc_init, _oi, _oe = run(HERE / 'init_watchlist.py', '--run-dir', d, '--subject', '600001', '--quiet')
    shapes = {'夹具-数组行': fx,
              '数组行': None, '字符串行': None, '数字行': None, '布尔行': None}
    inline = d / 'inline.jsonl'
    for key, body in (('数组行', '[{"code":"600001"}]'), ('字符串行', '"just a string"'),
                      ('数字行', '42'), ('布尔行', 'true')):
        inline.write_text(body + '\n', encoding='utf-8')
        shapes[key] = inline
    tb_total, msgs, leaks = 0, [], []
    codes = {}
    for name, ev in shapes.items():
        rc, out, err = run(HERE / 'digest.py', '--run-dir', d, '--events', ev, '--asof', '2026-10-17 09:00',
                           '--window', '2026-09-17~2026-10-17', '--legs-called', '1')
        codes[name] = rc
        tb_total += err.count('Traceback')
        msgs.append(err.strip().split('\n')[0] if err.strip() else '(空)')
        left = [p.name for p in d.glob('digest-*.md')] + [n for n in ('sources.jsonl', 'run.json')
                                                          if (d / n).is_file()]
        if left:
            leaks.append(f'{name}:{left}')
    # 同族第二枚：init_watchlist 的 --from-return 返货件，旧态下数字／布尔／null 三形抛 Traceback、
    # 数组与字符串形虽有人话但不点实收类型——两处一并跟正，五形各跑一次
    iw_codes, iw_tb, iw_typed = {}, 0, 0
    for body, want in (('数组行', 'list'), ('字符串行', 'str'), ('数字行', 'int'), ('布尔行', 'bool'), ('null 行', 'NoneType')):
        if body == '数组行':
            ev = HERE / 'fixtures' / 'bad-return-array.jsonl'
        else:
            ev = d / ('iw-%s.jsonl' % body)
            ev.write_text({'字符串行': '"样本股份"', '数字行': '42', '布尔行': 'true', 'null 行': 'null'}[body] + '\n',
                          encoding='utf-8')
        rc_iw, oi, oe = run(HERE / 'init_watchlist.py', '--run-dir', d / ('iw' + body), '--subject', '600001',
                            '--from-return', ev, '--quiet')
        iw_codes[body] = rc_iw
        iw_tb += ('Traceback' in oi + oe)
        iw_typed += ('第 1 行是 JSON %s' % want) in (oi + oe)
    checks = [
        ('init 退码', rc_init, 0),
        ('五形退码全为 1', sorted({v for v in codes.values()}), [1]),
        ('清单器五形退码全为 1', sorted({v for v in iw_codes.values()}), [1]),
        ('清单器五形 Traceback 命中 0', iw_tb, 0),
        ('清单器每形句里点实收类型', iw_typed, 5),
        ('Traceback 计数＝0（本档主断言）', tb_total, 0),
        ('每形都有一句可读出口', sum(1 for m in msgs if m.startswith('digest: --events 第 1 行是 JSON')), 5),
        ('句里点名行号与实际收到的类型', sum(1 for m in msgs if '第 1 行是 JSON' in m and '本件只收对象' in m), 5),
        ('句里给出零条的正确写法', sum(1 for m in msgs if '_kind' in m and 'header' in m), 5),
        ('未留半件（digest／sources／run 一件都不产）', leaks, []),
    ]
    bad = [(n, got, want) for n, got, want in checks if got != want]
    print('selftest 七档生成器坏输入：digest.py 五形＋init_watchlist 五形 现场跑｜断言 %d 条，不符 %d 条｜Traceback 命中=%s（日报器 %s／清单器 %s），退码集 日报器=%s 清单器=%s，可读句=%s/5、点名类型=%s/5' % (
        len(checks), len(bad), tb_total + iw_tb, tb_total, iw_tb,
        sorted({v for v in codes.values()}), sorted({v for v in iw_codes.values()}),
        sum(1 for m in msgs if m.startswith('digest: --events 第 1 行是 JSON')), iw_typed))
    for n, got, want in bad:
        print('   不符 → %s：实得 %s（规格 %s）' % (n, got, want))
    print('   可读出口首句 → ' + msgs[0][:150])
    return not bad


def selftest():
    gd = HERE / 'fixtures' / 'good-digest.md'
    gr = HERE / 'fixtures' / 'good-run.json'
    zd = HERE / 'fixtures' / 'zero-digest.md'
    zr = HERE / 'fixtures' / 'zero-run.json'
    bd = HERE / 'fixtures' / 'bad-digest.md'
    br = HERE / 'fixtures' / 'bad-run.json'
    gs = HERE / 'fixtures' / 'good-sources.jsonl'
    for f in (gd, gr, zd, zr, bd, br, gs):
        if not f.is_file():
            print(f"SELFTEST FAIL: 守护样缺失 {f}")
            return 1
    goods = [(gd, gr, gs)]  # 一档好样夹具集（日报＋记账件＋来源件为一枚）：末行枚数由它现算，不写字面量
    gf, gnl = [], 0
    for d, r, s in goods:
        fx, nl = check(d, r, s)
        gf += fx
        gnl += nl
    zeros = [(zd, zr)]  # 二档零新增样夹具集：同上，枚数由夹具集现算
    zf, znl = [], 0
    for d, r in zeros:
        fx, nl = check(d, r)
        zf += fx
        znl += nl
    bf, bnl = check(bd, br)
    got = {re.match(r'\[(E-[A-Z]+)\]', x).group(1) for x in bf}
    want = set(FAMILY)
    ok = True
    print(f"selftest 一档好样：{'、'.join(d.name for d, _r, _s in goods)} 扫过 {gnl} 行，发条 {len(gf)} 条（规格 0）")
    for x in gf:
        print('   意外发条 → ' + x)
        ok = False
    print(f"selftest 二档零新增样：{'、'.join(d.name for d, _r in zeros)} 扫过 {znl} 行，发条 {len(zf)} 条（规格 0，形制＝第二段勾「未检索到新增」带窗口）")
    for x in zf:
        print('   意外发条 → ' + x)
        ok = False
    zrun = json.loads(zr.read_text(encoding='utf-8'))
    zdecl = [ln for ln in zd.read_text(encoding='utf-8').split('\n') if '零新增声明' in ln]
    zticked = [w for ln in zdecl for mk, w in ticks(ln) if mk == '☑']
    if zrun.get('new_count') != 0 or not any('未检索到' in w and DATE.search(w) for w in zticked):
        print('   零新增样自身不合式 → new_count=%s，勾选项=%s' % (zrun.get('new_count'), zticked))
        ok = False
    print(f"selftest 三档坏样：{bd.name} 扫过 {bnl} 行，发条 {len(bf)} 条（规格 ≥1 且四道全发）")
    missing = sorted(want - got)
    if missing:
        print('   未发出的码 → ' + ', '.join(missing))
        ok = False
    tmp = Path(tempfile.mkdtemp(prefix='check-digest-selftest-'))
    try:
        res = probe_matrix(gd.read_text(encoding='utf-8'), json.loads(gr.read_text(encoding='utf-8')), tmp,
                           gs.read_text(encoding='utf-8'))
        chain_ok = replay_chain(tmp)
        src_ok = source_pair(tmp)
        badin_ok = bad_input_exit(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if not chain_ok or not src_ok or not badin_ok:
        ok = False
    bad = [x for x in res if not x[3]]
    print(f"selftest 四档反证矩阵：{len(res)} 枚（单点破坏 {len(res) - 1} ＋正向不误拦 1），未达预期 {len(bad)} 枚")
    for name, exp, gotv, passed, finds in res:
        print('   %-18s 期望 %-24s 实得 %-28s %s' % (name, exp, gotv, '符合' if passed else '不符'))
        if not passed and finds:
            for x in finds[:2]:
                print('      实发详行 → ' + x[:120])
    if bad:
        ok = False
    print(f"selftest: {'ALL GREEN' if ok else 'FAIL'}（一档 {len(goods)} 枚·发条 {len(gf)} 条（规格 0）· 二档 {len(zeros)} 枚·发条 {len(zf)} 条（规格 0）· 三档四道 {len(got)}/{len(want)} · 四档 {len(res) - len(bad)}/{len(res)} · 五档跨日重放 {'通' if chain_ok else '不通'} · 六档来源对账 {'通' if src_ok else '不通'} · 七档生成器坏输入 {'通' if badin_ok else '不通'}）")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description='校验一份增量日报是否合五段契约与红线（零网络）。',
                                 epilog='出口：FAIL 一行计数＋逐条 E-* 详行＋码表；PASS 一行＋两类计数。判定全集在本脚本现值。')
    ap.add_argument('digest', nargs='?', help='待校验的日报（markdown）')
    ap.add_argument('--run', help='同次运行的 run.json（缺省取日报同目录）')
    ap.add_argument('--sources', help='同次运行的 sources.jsonl（缺省取日报同目录 sources.jsonl；道五用它双向对账）')
    ap.add_argument('--selftest', action='store_true', help='跑包内守护样（七档：好样与零新增样须过、坏样四道全发、反证矩阵逐枚自报、跨日重放链须逐字节同、来源对账好形须过且坏形必红、生成器坏输入须出一句人话不抛 Traceback）')
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.digest:
        ap.error('缺参数：给一份日报，或用 --selftest')
    p = Path(args.digest)
    if not p.is_file():
        print(f"[出错] 文件不存在：{p}")
        return 1
    rp = Path(args.run) if args.run else p.parent / 'run.json'
    sp = Path(args.sources) if args.sources else p.parent / 'sources.jsonl'
    finds, n = check(p, rp, sp)
    return report(p, finds, n)


if __name__ == '__main__':
    sys.exit(main())
