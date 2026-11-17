#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_concentration.py — 校一份「客户集中度与依赖风险台账」是否合 `SKILL.md` §1 六节契约与 §4 红线。

用法：
    python3 check_concentration.py <台账.md>      校一份台账（纯标准库、零网络、不发任何请求）
    python3 check_concentration.py --selftest     跑包内夹具：好样必须过，七枚坏样必须各发它该发的那一道
    python3 check_concentration.py --help         本说明

出口形制（与套件姊妹件同族）：
    失败 = 一行 "FAIL: <文件>（N 条）"，其下每条详行先打错误码前缀（五枚 E-* 之一），道名后是行号与该道规格；
           末行 "码表:" 只列本次真正用到的码与含义。
    全过 = 一行 "PASS: <文件>（…）"，并印「扫过 N 行」与五道计数——计数说看到多少，不说猜多少。

五道是什么（判定全集在本脚本，本文只指路，不复述细节）：
    道一 形制：头部四件自标逐字在位＋「集中度口径：」行在场且值为客户依赖口径＋六节齐且按一至六有序
                ＋集中度一句话非空非占位＋第二节至少一行合计行＋第三节至少一行单客户行
                ＋**每行数据行必须是四字段形制**「- 期间：<期间>｜前五大客户合计：<N>%｜口径：<口径> [S#]」
                  或「- 期间：<期间>｜客户：<客户名>｜占比：<N>%｜口径：<口径> [S#]」——
                  占比不带期间是孤数，不带口径是不可比数，两者各发一条
                ＋**匿名客户不得具名**：客户名写成「客户一／客户二／第 N 名客户」时，其括号注只能是
                  「未具名／匿名／未披露／未点名」这一类；括号里出现公司名即发红——披露没点名，你就不能替它点名
                ＋**占比自洽**：同一期间的单客户占比之和不得大于该期前五大客户合计（差在四舍五入以内不算）
    道二 锚：数据行行末带 [S#]，且该编号在第六节有对应行；第六节每行必须同时带 URL 与 YYYY-MM-DD 检索日
    道三 红线：评级／目标价／买卖与走势类断言零命中；**另加本域独有的判断词族**——风险可控／风险不大／
                无风险／严重依赖／过度依赖／高度依赖／优质客户／标杆客户／大客户背书／客户质量高／深度绑定／
                绑定龙头／护城河／粘性强／订单饱满／业绩确定性，一律零命中（本件出的是集中度事实，不是
                客户质量与风险大小的结论）；要写只能同行挂 [待人工]
    道四 未取到与计数：正文写了「未取到／未检索到」的，第五节必须逐条点名它；第五节列了而正文没有这条表述的同样发
    道五 边界：集中度口径写成「招股书／首发／IPO」＝这一问该走 prospectus-digest-cn 的招股书速览；
                写成「产业链／上下游／环节」＝该走 cn-supply-chain-map 的链条结构；本件的客户依赖台账不适用

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
    d = Path(tempfile.mkdtemp(prefix='check-conc-', dir=tempfile.gettempdir()))
    TMP_ROOTS.append(d)
    f = d / 'probe.md'
    f.write_text(text, encoding='utf-8')
    return f


SECTIONS = ('集中度一句话', '分期集中度', '单客户明细', '关联与依赖事实', '未取到与口径', '来源')
CN_NUM = ('一', '二', '三', '四', '五', '六')
MARKS = ('AI 整理初稿', '请回原文核对', '不构成投资建议', '判断位 [待人工]')
URL_RE = re.compile(r'https?://|www\.[A-Za-z0-9.-]+')
DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')
PLACEHOLDER_RE = re.compile(r'^\s*(（[^）]*）)?[—\-–]\s*$|待定|待填|TBD|<[^>]*>$')
SCOPE_RE = re.compile(r'^集中度口径[：:]\s*(.+?)\s*$')
MISS_WORD = re.compile(r"未取到|未检索到|没取到|没检索到")

# 数据行两形。占比必须与期间、口径同处一行——这是本域的要害：
# 「前五大客户占比 62%」不带期间是孤数（哪一期？），不带口径是不可比数（合并还是母公司？含税还是不含税？）。
# 占比前的改数词（约／大约／大概）与占比后的「左右」在正则里留了位：这类词是**要报的红线**，
# 不是**认不出的形制**。若让它们在 \d+ 前把整行卡成失配，形制分支会先命中并 continue，
# 改数词那条判据就永远够不着（2026-11-09 runner 档⑤ 实发即此：只报形制、不报改数词）；
# 同时该行会被悄悄排除在合计自洽之外，占比之和的检查少算一行。
_HEDGE_PRE = r'(?:(?:约|大约|大概)\s*)?'
_HEDGE_POST = r'(?:左右)?'
TOTAL_RE = re.compile(
    r'^\s*[-*]\s*期间[：:]\s*(?P<period>[^｜|]+?)\s*[｜|]\s*前(?:[三五]大|十大)客户合计[：:]\s*'
    + _HEDGE_PRE + r'(?P<pct>\d+(?:\.\d+)?)\s*%\s*' + _HEDGE_POST
    + r'\s*[｜|]\s*口径[：:]\s*(?P<cal>[^｜|\[]+?)\s*\[S(?P<n>\d+)\]\s*$')
CUST_RE = re.compile(
    r'^\s*[-*]\s*期间[：:]\s*(?P<period>[^｜|]+?)\s*[｜|]\s*客户[：:]\s*(?P<co>[^｜|]+?)\s*[｜|]\s*'
    r'占比[：:]\s*' + _HEDGE_PRE + r'(?P<pct>\d+(?:\.\d+)?)\s*%\s*' + _HEDGE_POST
    + r'\s*[｜|]\s*口径[：:]\s*(?P<cal>[^｜|\[]+?)\s*\[S(?P<n>\d+)\]\s*$')
# 匿名客户的三种披露写法。披露没点名，台账就不能替它点名——这是本件与「公司名单」的分界。
ANON_RE = re.compile(r'^客户[一二三四五六七八九十\d]+$|^第[一二三四五六七八九十\d]+名客户$|^客户[A-Z]$')
ANON_NOTE_RE = re.compile(r'未具名|匿名|未披露|未点名')
NAME_NOTE_RE = re.compile(r'^(?P<name>[^（(]+?)\s*(?:[（(](?P<note>[^）)]*)[）)])?$')
# 红线词族甲：评级／目标价／买卖与走势承诺（与套件同族，逐字同表——这是全仓共用的红线词，不是本域新造）。
BANNED = re.compile(r'买入|卖出|建仓|清仓|加仓|目标价|止盈|止损|必涨|必跌|稳赚|无风险'
                    r'|强烈建议|建议持有|建议买入|建议增持|建议减持|翻倍|跑赢大盘'
                    r'|严重低估|严重高估|值得买入|可以买入')
# 红线词族乙：**本域独有**的判断词。客户集中度台账出的是事实，不是「客户好不好、风险大不大」的结论。
# 收窄写在这里防后人放宽：裸「依赖」不收（「对前五大客户存在一定依赖」是披露原话），
# 只收「严重依赖／过度依赖／高度依赖」这种加程度的判断；裸「集中」不收，只收「风险可控／风险不大」这种下结论的形。
CONC_BANNED = re.compile(r'风险可控|风险不大|风险较小|风险极低|风险很高|风险极大'
                         r'|严重依赖|过度依赖|高度依赖'
                         r'|优质客户|标杆客户|大客户背书|客户质量高|深度绑定|绑定龙头'
                         r'|护城河|粘性强|订单饱满|业绩确定性')
HEDGE = re.compile(r'约\s*[\d０-９]|左右|大概|大约')
CODES = {'E-FORMAT': '道一 形制', 'E-ANCHOR': '道二 锚', 'E-BANWORD': '道三 红线',
         'E-COVERAGE': '道四 未取到与计数', 'E-SCOPE': '道五 边界'}
SUM_TOL = 0.5   # 单客户之和与合计的容差（个百分点）：只吸收四舍五入，不吸收真错


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

    # ---- 道一／道五 集中度口径 ----
    sc = None
    for i in range(first_h2):
        m = SCOPE_RE.match(lines[i].strip())
        if m:
            sc = (i, m.group(1))
            break
    if sc is None:
        add('E-FORMAT', '集中度口径', 1,
            '头部缺「集中度口径：」行（规格：本件只出集中度事实，这一格是它与招股书速览、产业链图谱的分界，必须自报）')
    else:
        i, v = sc
        # 只看括号前的口径头，不看括号里的说明——「客户依赖（…；不判客户质量、不判风险大小）」里的
        # 「风险」是**否定式**的边界声明，按整串 contains 判会误伤。
        head_v = re.split(r'[（(]', v, 1)[0].strip()
        if re.search(r'招股书|首发|IPO|上市申报', head_v):
            add('E-SCOPE', '边界', i + 1,
                f'集中度口径写的是「{v}」——读一份招股书、把八项逐字摘成速览卡走 prospectus-digest-cn；'
                '本件做的是跨期客户依赖台账（多期、多份披露、占比怎么变），不读单份招股书')
        elif re.search(r'产业链|上下游|环节|供应链', head_v):
            add('E-SCOPE', '边界', i + 1,
                f'集中度口径写的是「{v}」——谁在哪个环节、上下游关系走 cn-supply-chain-map；'
                '本件问的是「这家公司的收入来自哪些客户、占比多少、跨期怎么变」，不画链条结构')
        elif not head_v.startswith('客户依赖'):
            add('E-FORMAT', '集中度口径', i + 1,
                f'集中度口径「{v}」认不出（规格：以「客户依赖」起头，'
                '如「客户依赖（收入来自哪些客户、占比多少、跨期怎么变；不判客户质量、不判风险大小）」）')

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

    # ---- 道一 集中度一句话非空非占位 ----
    if 1 in bounds:
        i0, i1 = bounds[1]
        body = [ln for ln in lines[i0 + 1:i1] if ln.strip() and not ln.startswith('#')]
        if not body:
            add('E-FORMAT', '集中度一句话', i0 + 1, '集中度一句话留空（规格：至少一行实句，不留占位）')
        else:
            bad = next((ln for ln in body if PLACEHOLDER_RE.search(ln)), None)
            if bad is not None:
                add('E-FORMAT', '集中度一句话', i0 + 1 + body.index(bad),
                    '集中度一句话仍是占位（规格：写成可核的实句；判断走 [待人工]，不靠占位）')

    # ---- 道一／道二 数据行 ----
    anchors_used = []
    totals = {}   # 期间 -> (占比, 行号)
    custs = {}    # 期间 -> [(占比, 行号), ...]

    def rows_of(n):
        if n not in bounds:
            return []
        i0, i1 = bounds[n]
        return [(i, lines[i]) for i in range(i0 + 1, i1) if lines[i].strip().startswith(('-', '*'))]

    for i, ln in rows_of(2):
        if MISS_WORD.search(ln):
            continue          # 缺口行：形制不要求，由道四两向点名管
        # 红线先于形制：形制不合时下面会 continue，若把改数词判据放在其后，
        # 一个形制错就能把这行的红线一并吞掉（只报形制、不报改数词）。
        if HEDGE.search(ln):
            add('E-BANWORD', '改数', i + 1,
                f"命中改数词「{HEDGE.search(ln).group(0)}」（规格：占比照来源写，不用约／左右打底）")
        m = TOTAL_RE.match(ln)
        if not m:
            add('E-FORMAT', '合计行', i + 1,
                '合计行形制不合（规格：- 期间：<期间>｜前五大客户合计：<N>%｜口径：<口径> [S#]；'
                '占比不带期间是孤数，不带口径是不可比数）')
            continue
        anchors_used.append((int(m.group('n')), i + 1))
        totals[m.group('period').strip()] = (float(m.group('pct')), i + 1)

    for i, ln in rows_of(3):
        if MISS_WORD.search(ln):
            continue
        if HEDGE.search(ln):
            add('E-BANWORD', '改数', i + 1,
                f"命中改数词「{HEDGE.search(ln).group(0)}」（规格：占比照来源写，不用约／左右打底）")
        m = CUST_RE.match(ln)
        if not m:
            add('E-FORMAT', '单客户行', i + 1,
                '单客户行形制不合（规格：- 期间：<期间>｜客户：<客户名>｜占比：<N>%｜口径：<口径> [S#]）')
            continue
        anchors_used.append((int(m.group('n')), i + 1))
        co = m.group('co').strip()
        nm = NAME_NOTE_RE.match(co)
        if nm and ANON_RE.match(nm.group('name').strip()):
            note = (nm.group('note') or '').strip()
            if note and not ANON_NOTE_RE.search(note):
                add('E-FORMAT', '匿名客户', i + 1,
                    f'匿名客户「{nm.group("name").strip()}」的括号注写成了「{note}」——'
                    '披露没点名，台账就不能替它点名（规格：括号注只能是「未具名／匿名／未披露／未点名」这一类；'
                    '要写公司名，得有一处披露原文点了名并挂锚）')
        custs.setdefault(m.group('period').strip(), []).append((float(m.group('pct')), i + 1))

    if 2 in bounds and not rows_of(2):
        add('E-FORMAT', '分期集中度', bounds[2][0] + 1,
            '「分期集中度」一行都没有（规格：至少一行——没有合计就没有集中度；'
            '取不到就写「前五大客户合计：未取到」并进第五节点名，不省行）')
    if 3 in bounds and not rows_of(3):
        add('E-FORMAT', '单客户明细', bounds[3][0] + 1,
            '「单客户明细」一行都没有（规格：至少一行；只给合计不给明细，等于没拆开看；'
            '取不到就写「客户：未取到」并进第五节点名，不省行）')
    if 4 in bounds:
        i0, i1 = bounds[4]
        if not [ln for ln in lines[i0 + 1:i1] if ln.strip() and not ln.startswith('#')]:
            add('E-FORMAT', '关联与依赖事实', i0 + 1,
                '「关联与依赖事实」整节为空（规格：至少一行——关联关系、重大合同、客户变动都是依赖事实；'
                '一条都没有就写「未取到」并进第五节）')

    # ---- 道一 占比自洽 ----
    for period, (tp, tline) in totals.items():
        if period not in custs:
            continue
        s = sum(p for p, _ in custs[period])
        if s > tp + SUM_TOL:
            add('E-FORMAT', '占比自洽', custs[period][0][1],
                f'「{period}」单客户占比之和 {s:.2f}% 大于同期前五大客户合计 {tp:.2f}%（规格：明细不得大于合计；'
                f'差在四舍五入以内（≤{SUM_TOL} 个百分点）不算）')

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
                    f'来源 [S{m.group(1) if m else k}] 缺检索日 YYYY-MM-DD（规格：集中度的时效以检索日为凭）')
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
        m = CONC_BANNED.search(ln)
        if m:
            add('E-BANWORD', '判断词', i,
                f"命中「{m.group(0)}」（规格：本件出的是集中度事实，不是客户质量与风险大小的结论——"
                '风险可控／严重依赖／优质客户／护城河这类判断本件不产出；要写就同行挂 [待人工]，或改写成占比与期间）')

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
            # 数据行里的「<字段>：未取到」：名目是**那个字段名**（前五大客户合计／客户），
            # 不是整行。这一形必须先认出来并跳过下面的通用抽取——通用式的排除字符集里有
            # 「：」与「｜」，正好把字段名与「未取到」隔开，于是这一形会被整条漏掉，
            # 骨架的第五节就被判成「多列一项」。
            dm = re.match(r'^\s*[-*]\s*期间[：:]', ln)
            if dm:
                fm = re.search(r'[｜|]\s*([^｜|：:\[\]]{2,24}?)\s*[：:]\s*(?:未取到|未检索到|没取到|没检索到)', ln)
                if fm:
                    tok = fm.group(1).strip()
                    if tok and tok not in STOP_TOK:
                        out.append((tok, off))
                    continue
            # 括号注是注解，不是名目：先剥掉再抽。
            # 「- 未取到：X（该年度年报只披露合计数）」里括号内是原因从句，不剥就会把原因抽成一条名目。
            body = re.sub(r'[（(][^）)]*[）)]', '', ln)
            # 后置形只认「未取到：X」与「未取到X」两种——**逗号不算分隔符**：
            # 「X未取到，年报只披露了合计数」里逗号后面是原因从句，不是名目；
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
    print('PASS: ' + path.name + '（六节齐、自标在位、集中度口径为客户依赖、数据行四字段齐、'
          '匿名客户未具名、占比自洽、每条数据带可回锚、来源行齐 URL 与检索日、判断词零命中、未取到逐条点名）')
    print(f'       扫过 {len(lines)} 行，发条 0 条；判定与阈值全集以本脚本现值为准（--help 看五道说明）')
    return 0, 0, {}


def selftest():
    fx = Path(__file__).resolve().parent / 'fixtures'
    cases = [('good-concentration.md', 0, None),
             ('bad-no-anchor.md', 1, 'E-ANCHOR'),
             ('bad-missing-section.md', 1, 'E-FORMAT'),
             ('bad-rating-word.md', 1, 'E-BANWORD'),
             ('bad-gap-unlisted.md', 1, 'E-COVERAGE'),
             ('bad-scope-prospectus.md', 1, 'E-SCOPE'),
             ('bad-anon-named.md', 1, 'E-FORMAT'),
             ('bad-sum-exceeds.md', 1, 'E-FORMAT')]
    bad = 0
    gt = (fx / 'good-concentration.md').read_text(encoding='utf-8')
    body_gap_line = '- 2023年度单客户占比明细未取到，该年度年报只披露合计数 [S1]'
    sec5_line = '- 未取到：2023年度单客户占比明细（该年度年报只披露合计数，未列单客户）'
    assert gt.count(body_gap_line) == 1 and gt.count(sec5_line) == 1, '夹具形制变了，反证档要跟着改'
    probes = []
    # 阈值三形钉死：字面全等与同指异词都算点到，真无关才算多列
    p0a = gt.replace(sec5_line, '- 未取到：2023年度单客户占比明细（该年度年报只披露合计数）')
    probes.append(('钉阈·字面全等（两侧都写「2023年度单客户占比明细」）不得报多列', p0a, '第五节多列一项', False))
    p0b = gt.replace(sec5_line, '- 未取到：2023年度单客户占比明细表（该年度年报只披露合计数）')
    probes.append(('钉阈·同指异词（正文「2023年度单客户占比明细」∥第五节「…明细表」）不得报多列', p0b, '第五节多列一项', False))
    p0c = gt.replace(sec5_line, '- 未取到：2023年度前五大客户名单')
    probes.append(('钉阈·真无关（第五节只列「2023年度前五大客户名单」）必须报多列', p0c, '第五节多列一项', True))
    p1 = gt.replace(body_gap_line, body_gap_line + '\n- 2024年度客户流失原因未取到 [S2]')
    probes.append(('反证·正文多写一条未取到而第五节不列｜独有句「第五节的点名缺一项」', p1, '第五节的点名缺一项', True))
    p2 = gt.replace(sec5_line, sec5_line + '；2023年度前五大客户名单未取到')
    probes.append(('反证·第五节多列一条而正文无｜独有句「第五节多列一项」', p2, '第五节多列一项', True))
    p3 = gt.replace('\n' + body_gap_line, '').replace(
        sec5_line, '- 口径：2023 年度为追溯调整前口径，2024 年度起为追溯调整后口径，两者不直接可比')
    probes.append(('反证·两处都无这一项时本支不发｜独有句反向断言', p3, '第五节的点名缺一项', False))
    probes.append(('反证·两处都有时本支不发（好样原样）', gt, '第五节多列一项', False))
    # 本域独有的两形：匿名客户不得具名、占比不得大于合计，两向各钉一枚
    p4 = gt.replace('客户一（披露未具名）', '客户一（华为技术有限公司）')
    probes.append(('本域·匿名客户被具名必发｜独有句「披露没点名」', p4, '披露没点名', True))
    p5 = gt.replace('客户一（披露未具名）', '客户一（匿名）')
    probes.append(('本域·匿名客户括号注合规（「匿名」）不得发｜独有句反向断言', p5, '披露没点名', False))
    p6 = gt.replace('｜占比：27.85%', '｜占比：77.85%')
    probes.append(('本域·单客户占比大于合计必发｜独有句「明细不得大于合计」', p6, '明细不得大于合计', True))
    p7 = gt.replace('｜占比：27.85%', '｜占比：28.20%')
    probes.append(('本域·差在四舍五入以内（+0.35pp）不得发｜独有句反向断言', p7, '明细不得大于合计', False))
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
    leftover = sorted(q.name for q in root.iterdir() if q.name.startswith('check-conc-')) if root.is_dir() else []
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
    print('selftest: ' + ('ALL GREEN（好样 1 枚·坏样七道 7/7）' if bad == 0 else f'{bad} 条不合期望'))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(prog='check_concentration.py', add_help=False,
                                 description='校一份客户集中度与依赖风险台账（五道，见 --help 正文）')
    ap.add_argument('target', nargs='?')
    ap.add_argument('--selftest', action='store_true', help='跑包内夹具（好样须过、七枚坏样须各发红）')
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
        print(f'取值域故障：读不到台账文件 {p}（不当「零违例」读）')
        return 3
    rc, _, _ = run_one(p, quiet=a.quiet)
    return rc


if __name__ == '__main__':
    sys.exit(main())
