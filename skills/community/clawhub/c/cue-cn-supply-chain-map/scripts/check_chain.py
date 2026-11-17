#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_chain.py — 校一份「产业链上下游图谱」是否合 `SKILL.md` §3 六节契约与 §5 红线。

用法：
    python3 check_chain.py <图谱.md>         校一份图谱（纯标准库、零网络、不发任何请求）
    python3 check_chain.py --selftest        跑包内夹具：好样必须过，五枚坏样必须各发它该发的那一道
    python3 check_chain.py --help            本说明

出口形制（与套件姊妹件同族）：
    失败 = 一行 "FAIL: <文件>（N 条）"，其下每条详行先打错误码前缀（五枚 E-* 之一），道名后是行号与该道规格；
           末行 "码表:" 只列本次真正用到的码与含义。
    全过 = 一行 "PASS: <文件>（…）"，并印「扫过 N 行」与五道计数——计数说看到多少，不说猜多少。

五道是什么（判定全集在本脚本，本文只指路，不复述细节）：
    道一 形制：头部四件自标逐字在位＋「链条口径：」行在场且值为结构口径＋六节齐且按一至六有序
                ＋链条一句话非空非占位＋上游／中游／下游三层各至少一行环节行
                ＋**每行环节行必须是三字段形制**「- 环节：<环节名>｜代表公司：<公司名>（<在链条里的位置>）[S#]」，
                  缺环节名／缺代表公司／缺位置括号／位置括号为空，四形各发一条——只列环节不点公司是环节表不是图谱，
                  点了公司不写位置是名单不是图谱；**没查到的环节写「- 环节：<环节名>｜代表公司：未取到 [S#]」**，
                  这一形不要求位置括号（没有公司就没有位置），但它必须同时出现在第五节——两向点名照旧
    道二 锚：环节行行末带 [S#]，且该编号在第六节有对应行；第六节每行必须同时带 URL 与 YYYY-MM-DD 检索日
    道三 红线：评级／目标价／买卖与走势类断言零命中；**另加本域独有的推荐词族**——受益标的／受益股／核心标的／
                弹性标的／首选标的／龙头／潜力股／值得关注／建议关注／重点推荐／推荐关注／布局良机／上车，
                一律零命中（产业链图谱是「谁在哪个环节」的事实图，不是选股清单）；要写只能同行挂 [待人工]
    道四 未取到与计数：正文写了「未取到／未检索到」的，第五节必须逐条点名它；第五节列了而正文没有这条表述的同样发
    道五 边界：链条口径写成「景气」＝这一问该走 sector-overview 的行业景气全景，本件的链条结构框架不适用

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
    d = Path(tempfile.mkdtemp(prefix='check-chain-', dir=tempfile.gettempdir()))
    TMP_ROOTS.append(d)
    f = d / 'probe.md'
    f.write_text(text, encoding='utf-8')
    return f


SECTIONS = ('链条一句话', '上游', '中游', '下游', '未取到与口径', '来源')
CN_NUM = ('一', '二', '三', '四', '五', '六')
LAYER_IDX = (2, 3, 4)               # 三层：各至少一行环节行，空层＝这条链没画完
MARKS = ('AI 整理初稿', '请回原文核对', '不构成投资建议', '判断位 [待人工]')
URL_RE = re.compile(r'https?://|www\.[A-Za-z0-9.-]+')
DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')
PLACEHOLDER_RE = re.compile(r'^\s*(（[^）]*）)?[—\-–]\s*$|待定|待填|TBD|<[^>]*>$')
SCOPE_RE = re.compile(r'^链条口径[：:]\s*(.+?)\s*$')
# 环节行三字段形制：环节名 ｜ 代表公司（位置） [S#]。位置括号是本域的要害——
# 「谁在哪个环节」里的「哪个环节」由位置括号承载；没有它，一行就只是公司名单。
ROW_RE = re.compile(r'^\s*[-*]\s*环节[：:]\s*(?P<seg>[^｜|]+?)\s*[｜|]\s*代表公司[：:]\s*(?P<co>.+?)\s*\[S(?P<n>\d+)\]\s*$')
POS_RE = re.compile(r'^(?P<name>[^（(]+?)\s*[（(](?P<pos>[^）)]*)[）)]\s*$')
# 红线词族甲：评级／目标价／买卖与走势承诺（与套件同族，逐字同表——这是全仓共用的红线词，不是本域新造）。
BANNED = re.compile(r'买入|卖出|建仓|清仓|加仓|目标价|止盈|止损|必涨|必跌|稳赚|无风险'
                    r'|强烈建议|建议持有|建议买入|建议增持|建议减持|翻倍|跑赢大盘'
                    r'|严重低估|严重高估|值得买入|可以买入')
# 红线词族乙：**本域独有**的推荐词。产业链图谱是这类词最密集的落点——
# 「受益标的」「龙头」「潜力股」把一张事实图变成选股清单，而本件不判好坏、不选股。
# 收窄写在这里防后人放宽：裸「受益」不收（「受益于硅料降价」是因果陈述，不是推荐），
# 只收「受益标的／受益股」这种把公司当推荐对象的形；裸「关注」不收，只收「值得关注／建议关注／推荐关注」。
CHAIN_BANNED = re.compile(r'受益标的|受益股|核心标的|弹性标的|首选标的|龙头|潜力股'
                          r'|值得关注|建议关注|重点推荐|推荐关注|布局良机|上车')
HEDGE = re.compile(r'约\s*[\d０-９]|左右|大概|大约')
MISS_WORD = re.compile(r"未取到|未检索到|没取到|没检索到")
CODES = {'E-FORMAT': '道一 形制', 'E-ANCHOR': '道二 锚', 'E-BANWORD': '道三 红线',
         'E-COVERAGE': '道四 未取到与计数', 'E-SCOPE': '道五 边界'}


def scan(path: Path):
    issues = []
    seen = set()

    def add(code, lane, line_no, msg):
        key = (code, line_no, msg)
        if key not in seen:
            seen.add(key)
            issues.append((code, lane, line_no, msg))

    lines = path.read_text(encoding='utf-8', errors='replace').split('\n')
    first_h2 = next((i for i, ln in enumerate(lines) if ln.startswith('## ')), len(lines))

    # ---- 道一 头部自标 ----
    head = '\n'.join(lines[:first_h2])
    for need in MARKS:
        if need not in head:
            add('E-FORMAT', '头部', 1, f"头部自标缺『{need}』（规格：四件逐字齐，写在第一个「## 」之前）")

    # ---- 道一／道五 链条口径 ----
    sc = None
    for i in range(first_h2):
        m = SCOPE_RE.match(lines[i].strip())
        if m:
            sc = (i, m.group(1))
            break
    if sc is None:
        add('E-FORMAT', '链条口径', 1,
            '头部缺「链条口径：」行（规格：本件只画链条结构，这一格是它与行业景气全景的分界，必须自报）')
    else:
        i, v = sc
        # 只看括号前的口径头，不看括号里的说明——「结构（…；不判景气、不判好坏）」里的「景气」
        # 是**否定式**的边界声明，按整串 contains 判会把它读成「这一问是景气」，好样当场误红。
        head_v = re.split(r'[（(]', v, 1)[0].strip()
        if '景气' in head_v:
            add('E-SCOPE', '边界', i + 1,
                f'链条口径写的是「{v}」——行业景气全景（一个行业的量价与格局）走 sector-overview，'
                '本件只画链条结构（谁在哪个环节、上下游关系），不判景气、不判好坏；'
                '要么改走那一件，要么把问题收窄成「这条链上有哪些环节、各环节有谁」')
        elif not head_v.startswith('结构'):
            add('E-FORMAT', '链条口径', i + 1,
                f'链条口径「{v}」认不出（规格：以「结构」起头，如「结构（谁在哪个环节、上下游关系；不判景气、不判好坏）」）')

    # ---- 道一 六节齐且有序 ----
    idxs = []
    for n, name in enumerate(SECTIONS, 1):
        hit = [i for i, ln in enumerate(lines)
               if re.match(rf'^##\s*{CN_NUM[n - 1]}、{re.escape(name)}\s*$', ln)]
        if not hit:
            add('E-FORMAT', '六节', 1, f"缺「## {CN_NUM[n - 1]}、{name}」段（规格：六节齐且按一至六有序）")
        else:
            idxs.append((n, hit[0]))
    if len(idxs) > 1 and [n for n, _ in idxs] != sorted(n for n, _ in idxs):
        add('E-FORMAT', '六节', idxs[0][1] + 1, '六节次序与契约不一致（规格：一至六有序）')
    bounds = {}
    for pos, (n, i0) in enumerate(idxs):
        i1 = idxs[pos + 1][1] if pos + 1 < len(idxs) else len(lines)
        bounds[n] = (i0, i1)

    # ---- 道一 链条一句话非空非占位 ----
    if 1 in bounds:
        i0, i1 = bounds[1]
        body = [ln for ln in lines[i0 + 1:i1] if ln.strip() and not ln.startswith('#')]
        if not body:
            add('E-FORMAT', '链条一句话', i0 + 1, '链条一句话留空（规格：至少一行实句，不留占位）')
        else:
            bad = next((ln for ln in body if PLACEHOLDER_RE.search(ln)), None)
            if bad is not None:
                add('E-FORMAT', '链条一句话', i0 + 1 + body.index(bad),
                    '链条一句话仍是占位（规格：写成可核的实句；判断走 [待人工]，不靠占位）')

    # ---- 道一／道二 三层环节行 ----
    anchors_used = []
    for n in LAYER_IDX:
        if n not in bounds:
            continue
        i0, i1 = bounds[n]
        rows = [(i, lines[i]) for i in range(i0 + 1, i1)
                if lines[i].strip().startswith(('-', '*'))]
        if not rows:
            add('E-FORMAT', '层', i0 + 1,
                f'「{SECTIONS[n - 1]}」整层为空（规格：三层各至少一行环节行——空层＝这条链没画完）')
            continue
        for i, ln in rows:
            m = ROW_RE.match(ln)
            if not m:
                add('E-FORMAT', '环节行', i + 1,
                    '环节行形制不合（规格：- 环节：<环节名>｜代表公司：<公司名>（<在链条里的位置>）[S#]；'
                    '只列环节不点公司是环节表不是图谱）')
                continue
            seg = m.group('seg').strip()
            co = m.group('co').strip()
            if not seg:
                add('E-FORMAT', '环节行', i + 1, '环节名为空（规格：每个环节要有名字，空名等于没画这一环）')
            anchors_used.append((int(m.group('n')), i + 1))
            if HEDGE.search(ln):
                add('E-BANWORD', '改数', i + 1,
                    f"命中改数词「{HEDGE.search(ln).group(0)}」（规格：数值要么照来源写，要么落第五节写未取到，不用约／左右打底）")
            if MISS_WORD.search(co):
                # 「代表公司：未取到」是合法形：没查到公司就没有位置可写，位置括号不要求；
                # 但这一形必须同时出现在第五节（道四两向点名照旧），否则就是「正文说没查到、缺口清单不认」。
                continue
            pm = POS_RE.match(co)
            if not pm:
                add('E-FORMAT', '位置', i + 1,
                    f'代表公司「{co}」没写位置括号（规格：公司名后必须跟（<在链条里的位置>）——'
                    '点了公司不写位置是名单不是图谱）')
            else:
                if not pm.group('name').strip():
                    add('E-FORMAT', '环节行', i + 1, '代表公司名为空（规格：位置括号前要有公司名）')
                if not pm.group('pos').strip():
                    add('E-FORMAT', '位置', i + 1,
                        f'代表公司「{pm.group("name").strip()}」的位置括号是空的（规格：括号里要写它在链条里的位置，'
                        '空括号等于没写）')

    # ---- 道二 来源行 ----
    listed = set()
    if 6 in bounds:
        i0, i1 = bounds[6]
        rows = [(i, lines[i]) for i in range(i0 + 1, i1) if lines[i].strip().startswith(('-', '*'))]
        if not rows:
            add('E-COVERAGE', '来源', i0 + 1, '第六节一行来源都没有（规格：逐条挂源的价值就在这一节，空节等于没有出处）')
        for k, (i, ln) in enumerate(rows, 1):
            m = re.match(r'^[-*]\s*\[S(\d+)\]', ln.strip())
            if not m:
                add('E-ANCHOR', '来源', i + 1, f'来源第 {k} 行不以 [S#] 开头（规格：编号与正文锚一一对应）')
            else:
                listed.add(int(m.group(1)))
            if not URL_RE.search(ln):
                add('E-ANCHOR', '来源', i + 1,
                    f'来源 [S{m.group(1) if m else k}] 缺 URL（规格：逐条可回查——域名或链接原样写进同一行）')
            if not DATE_RE.search(ln):
                add('E-ANCHOR', '来源', i + 1,
                    f'来源 [S{m.group(1) if m else k}] 缺检索日 YYYY-MM-DD（规格：链条结构的时效以检索日为凭）')
    for num, ln_no in anchors_used:
        if num not in listed:
            add('E-ANCHOR', '锚', ln_no, f'锚 [S{num}] 在第六节没有对应行（规格：正文用的每个编号都要能回到来源行）')

    # ---- 道三 红线（两族分开报，命中哪族说哪族） ----
    for i, ln in enumerate(lines, 1):
        if '[待人工]' in ln:
            continue
        m = BANNED.search(ln)
        if m:
            add('E-BANWORD', '判断词', i,
                f"命中「{m.group(0)}」（规格：评级／目标价／买卖与走势类断言本件不产出；要写就同行挂 [待人工]，或改中性陈述）")
            continue
        m = CHAIN_BANNED.search(ln)
        if m:
            add('E-BANWORD', '推荐词', i,
                f"命中「{m.group(0)}」（规格：产业链图谱是「谁在哪个环节」的事实图，不是选股清单——"
                '受益标的／龙头／潜力股这类推荐词本件不产出；要写就同行挂 [待人工]，或改写成它在链条里的位置）')

    # ---- 道四 未取到两向点名 ----
    STOP_TOK = {"它", "这", "该", "其", "本节", "来源", "渠道", "本条", "该项", "本次"}
    # 名目「同指」判：先剥括号注与标点，再按核心名词短语判——字面全等算同指；一方含另一方且短的一方 ≥4 字算同指；
    # 否则取汉字集合的 Jaccard ≥ SAME_REF_MIN 算同指。阈值写在这里、由自测的三形钉死，不按文体特例放宽。
    SAME_REF_MIN = 0.6
    PUNCT_STRIP = re.compile(r"[^一-龥A-Za-z0-9]")

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
            # 环节行里的「代表公司：未取到」：名目是**环节名**，不是「代表公司」四个字。
            # 这一形必须先认出来并跳过下面的通用抽取——否则通用式会把「代表公司」抓成名目，
            # 于是好样被判「第五节多列一项」。
            rm = ROW_RE.match(ln)
            if rm and MISS_WORD.search(rm.group('co')):
                seg = rm.group('seg').strip()
                if seg and seg not in STOP_TOK:
                    out.append((seg, off))
                continue
            # 括号注是注解，不是名目：先剥掉再抽。
            # 「- 未取到：X（骨架未取到链条结构，只排了材料清单）」里括号内的「未取到链条结构」
            # 是原因从句，不剥就会把「链条结构」抽成一条名目，于是骨架凭空多出三条「多列一项」。
            body = re.sub(r'[（(][^）)]*[）)]', '', ln)
            # 后置形只认「未取到：X」与「未取到X」两种——**逗号不算分隔符**：
            # 「银浆环节未取到，公告只披露了组件环节」里逗号后面是原因从句，不是名目；
            # 把逗号当分隔符会把整句原因抓成名目，于是好样被判「第五节多列一项」。
            for m in re.finditer(r"(?:未取到|未检索到|没取到|没检索到)[：:\s]*([^\s，。；、：:｜\[\]（）()「」【】\n]{3,24})", body):
                tok = m.group(1)
                if tok not in STOP_TOK:
                    out.append((tok, off))
            for m in re.finditer(r"([^\s，。；、：:｜\[\]（）()「」【】\n]{3,24}?)(?:未取到|未检索到|没取到|没检索到)", body):
                tok = m.group(1)
                if tok not in STOP_TOK:
                    out.append((tok, off))
        return out

    body_seg = [(i, lines[i]) for n, (a, b) in bounds.items() if n != 5 for i in range(a + 1, b)]
    sec5_seg = [(i, lines[i]) for i in range(bounds[5][0] + 1, bounds[5][1])] if 5 in bounds else []
    body_toks = [tok for tok, _ in miss_tokens(body_seg)]
    sec5_toks = [tok for tok, _ in miss_tokens(sec5_seg)]
    for tok, no in miss_tokens(body_seg):
        if not refs(tok, sec5_toks):
            add("E-COVERAGE", "未取到点名", no + 1,
                f"第五节的点名缺一项：正文写了「{tok}」未取到，第五节没有同指的名目"
                "（规格：没列就是没说——逐条点名按名目同指对，不认整节出现过一个「未取到」）")
    for tok, no in miss_tokens(sec5_seg):
        if not refs(tok, body_toks):
            add("E-COVERAGE", "未取到点名", no + 1,
                f"第五节多列一项：「{tok}」在第五节点名为未取到，正文没有同指的这条表述"
                "（规格：反向同判——多列与少列都不许）")
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
    print('PASS: ' + path.name + '（六节齐、自标在位、链条口径为结构、三层环节行三字段齐、'
          '每条环节带可回锚、来源行齐 URL 与检索日、判断词与推荐词零命中、未取到逐条点名）')
    print(f'       扫过 {len(lines)} 行，发条 0 条；判定与阈值全集以本脚本现值为准（--help 看五道说明）')
    return 0, 0, {}


def selftest():
    fx = Path(__file__).resolve().parent / 'fixtures'
    cases = [('good-chain.md', 0, None),
             ('bad-no-anchor.md', 1, 'E-ANCHOR'),
             ('bad-missing-section.md', 1, 'E-FORMAT'),
             ('bad-rating-word.md', 1, 'E-BANWORD'),
             ('bad-gap-unlisted.md', 1, 'E-COVERAGE'),
             ('bad-industry-boom.md', 1, 'E-SCOPE'),
             ('bad-no-position.md', 1, 'E-FORMAT')]
    bad = 0
    gt = (fx / 'good-chain.md').read_text(encoding='utf-8')
    body_gap_line = '- 环节：光伏银浆｜代表公司：未取到 [S1]'
    sec5_line = '- 未取到：光伏银浆环节的代表公司（公告与年报只披露组件与电池片环节，未点名银浆供应商）'
    assert gt.count(body_gap_line) == 1 and gt.count(sec5_line) == 1, '夹具形制变了，反证档要跟着改'
    probes = []
    # 阈值三形钉死：字面全等与同指异词都算点到，真无关才算多列
    p0a = gt.replace(sec5_line, '- 未取到：光伏银浆环节的代表公司（公告只披露组件与电池片环节）')
    probes.append(('钉阈·字面全等（两侧都写「光伏银浆环节的代表公司」）不得报多列', p0a, '第五节多列一项', False))
    p0b = gt.replace(sec5_line, '- 未取到：光伏银浆环节代表公司名单（公告只披露组件与电池片环节）')
    probes.append(('钉阈·同指异词（正文「光伏银浆」∥第五节「光伏银浆环节代表公司名单」）不得报多列', p0b, '第五节多列一项', False))
    p0c = gt.replace(sec5_line, '- 未取到：光伏玻璃窑炉产能')
    probes.append(('钉阈·真无关（第五节只列「光伏玻璃窑炉产能」）必须报多列', p0c, '第五节多列一项', True))
    p1 = gt.replace(body_gap_line, body_gap_line + '\n- 环节：银浆国产化率｜代表公司：未取到 [S2]')
    probes.append(('反证·正文多写一条未取到而第五节不列｜独有句「第五节的点名缺一项」', p1, '第五节的点名缺一项', True))
    p2 = gt.replace(sec5_line, sec5_line + '；光伏玻璃窑炉产能未取到')
    probes.append(('反证·第五节多列一条而正文无｜独有句「第五节多列一项」', p2, '第五节多列一项', True))
    p3 = gt.replace('\n' + body_gap_line, '').replace(
        sec5_line, '- 口径：份额数据来自第三方汇总层，与公司自述口径不同，两者不互校')
    probes.append(('反证·两处都无这一项时本支不发｜独有句反向断言', p3, '第五节的点名缺一项', False))
    probes.append(('反证·两处都有时本支不发（好样原样）', gt, '第五节多列一项', False))
    # 本域独有的两形：位置括号是图谱与名单的分界，两向各钉一枚
    p4 = gt.replace('（硅料产能位于链首，向下自供硅片）', '')
    probes.append(('本域·代表公司缺位置括号必发｜独有句「没写位置括号」', p4, '没写位置括号', True))
    p5 = gt.replace('（硅料产能位于链首，向下自供硅片）', '（）')
    probes.append(('本域·位置括号为空必发｜独有句「位置括号是空的」', p5, '位置括号是空的', True))
    for name, txt, needle, want in probes:
        assert txt != gt or not want, '注入自证：反证档必须真改过文本（除好样档）'
        pf = _probe_copy(txt)
        iss_p, _ls_p = scan(pf)
        detail_p = "\n".join(f'[{c}] 第 {no} 行：{msg}' for c, lane, no, msg in iss_p)
        rc_p = 1 if iss_p else 0
        hit = needle in detail_p
        okp = (hit if want else not hit)
        print(f"  {'ok  ' if okp else 'FAIL'} {name}｜实发{'含' if hit else '不含'}独有句、退码 {rc_p}")
        if not okp:
            bad += 1
    root = Path(tempfile.gettempdir())
    for d in TMP_ROOTS:
        shutil.rmtree(d, ignore_errors=True)
    leftover = sorted(q.name for q in root.iterdir() if q.name.startswith('check-chain-')) if root.is_dir() else []
    print(f"  {'ok  ' if not leftover else 'FAIL'} 临时根自清（跑后不增）｜本次建 {len(TMP_ROOTS)} 枚·跑后残留 {len(leftover)} 枚")
    if leftover:
        bad += 1
    for name, want_rc, want_code in cases:
        p = fx / name
        if not p.is_file():
            print(f'  selftest 取值域故障：夹具不在场 {name}')
            return 3
        import contextlib
        import io
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
        if want_code is None and rc == 0:
            print(f'  ok   {name}（退码 {rc}·发条 {n}）')
        elif want_code:
            print(f'  ok   {name}（退码 {rc}·发条 {n}·实发 {want_code}）')
    print('selftest: ' + ('ALL GREEN（好样 1 枚·坏样六道 6/6）' if bad == 0 else f'{bad} 条不合期望'))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(prog='check_chain.py', add_help=False,
                                 description='校一份产业链上下游图谱（五道，见 --help 正文）')
    ap.add_argument('target', nargs='?')
    ap.add_argument('--selftest', action='store_true', help='跑包内夹具（好样须过、六枚坏样须各发红）')
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
        print(f'取值域故障：读不到图谱文件 {p}（不当「零违例」读）')
        return 3
    rc, _, _ = run_one(p, quiet=a.quiet)
    return rc


if __name__ == '__main__':
    sys.exit(main())
