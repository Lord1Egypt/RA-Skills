#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_key_financial_data.py — 主要会计数据与财务指标登记稿五道机检（零网络、零外发）

**五道已全部落字**（`UNIMPLEMENTED = ()`）：KF-STRUCT 判形制，KF-QUOTE 判引号，KF-CALC 判增减
与勾稽，KF-LINK 判行首与引文是否同一个数，KF-LINE 判该有的项与单位口径。
空壳机制仍留着当护栏：某道若回退成壳，只调 `_not_judged(code, why)`（NotImplementedError），
**不返回空表**——返回 [] 会被读成「这道跑过了、零发条」，而我们根本没跑。未落字由 `check_text`
捕获、计入 `unjudged`，不裸抛；零发条但有未落字的稿子退 3，报告里明写「这不等于合规」。

用法：
    python3 scripts/check_key_financial_data.py <主要会计数据登记稿>.md
    python3 scripts/check_key_financial_data.py --selftest
    python3 scripts/check_key_financial_data.py --demo     打印一份七节样例（零输入可跑）

七节（按序，`## ` 起节）：
    主要会计数据／主要财务指标／非经常性损益明细／扣非净利润勾稽／分季度主要会计数据
    ／口径与未取到／来源

五道码（状态以 `UNIMPLEMENTED` 现值为准，下面写的是**这道判什么**）：

道一 KF-STRUCT 形制【已落字】
  头部（第一个 `## ` 之前）三件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议；
  七节齐且按序；认不出的节标题与多出的同名节记 stray 逐条发。
  **只判形，不判内容**——内容对不对是另四道的事，这里越界会让一支注入同时红两道。
  不判「主体：」「报告期：」：本件规格只列三件自标，不自行加判据。

道二 KF-QUOTE 数要有原文引号【已落字】
  只判「主要会计数据」「主要财务指标」两节：每一条带数字的发现行必须有一对 `「…」`，
  引号内是本节的原文摘句（去空白后 ≥ 8 字，且不能只有数字没有字）。
  缺引号／引号空／引号内只有数字 ⇒ 逐行发条，一行只发一条。
  **只认形**：不核对引号里的数跟行首的数是否一致——那是 KF-LINK 的事，两处都判会让一支注入红两道。
  「未取到：」缺口行豁免（缺口本来就没有原句可摘）。

道三 KF-CALC 增减幅度与勾稽要能对上【已落字】
  ① 同一行里既有「本期」又有「上年同期」两个金额、且带一个 `增减／同比／变动` 百分数时，
    按 `(本期−上年)/|上年|` 重算，与披露值差 > 0.05 个百分点 ⇒ 发条（`重算=X 披露=Y`）。
    上年为 0、缺一个金额、或一行里有多个互不相同的百分数 ⇒ **不判、不猜**；缺口行直接跳过。
  ② 扣非净利润勾稽：`归母净利润 − 归属于母公司股东的非经常性损益净额 = 扣非净利润`，
    差 > 0.01 万元 ⇒ 发条。三数缺一即不判，不拿「小计」顶替净额（小计未扣税、未扣少数股东，
    拿它去减恒不等，那是自己造出来的假发条）。优先读「扣非净利润勾稽」节，该节三数不齐再全稿找。

道四 KF-LINK 引号里的数要与行首的数一致【已落字】
  有引号的发现行：行首的数（含单位）必须在引文里找得到；找不到 ⇒ 发条（`行首=… 引文=…`）。
  数字归一：去千分位逗号、全角转半角、统一折成万元再比；百分数单独比。
  单位不同但等值（`12.34 亿元` vs `123,400.00 万元`）⇒ 过，不是发条。
  没有引号的行不归这道管（那是 KF-QUOTE 的事）；缺口行跳过。
  行首有多个数时逐个数查（一个多数的行只要有一个数不在引文里就发一条）。

道五 KF-LINE 该有的项必须在，且单位口径不许串【已落字】
  「主要会计数据」必须含七项（少一项一条）：营业收入／归属于上市公司股东的净利润／
  扣除非经常性损益的净利润／经营活动产生的现金流量净额／总资产／归属于上市公司股东的净资产／
  基本每股收益；「主要财务指标」必须含：加权平均净资产收益率／每股净资产。
  节本身不在稿里时这一节整节跳过（缺节是 KF-STRUCT 的事，不在这里重报一遍）。
  同一行里同时出现独立的「元」与「万元」两套单位、又没写「换算／折合」⇒ 发条（单位串了）。
  全文出现「扣非净利润」而从未出现「非经常性损益」⇒ 发条（勾稽断了）。

退码：0 五道全过 / 1 有发条 / 2 用法错（缺参数或未知参数）
      / 3 读不到文件或空稿，或零发条但仍有未落字判据（`UNIMPLEMENTED` 非空时）。
      本拍五道已全部落字，好样单稿退 0；退 3 那一条留着，是给「某道回退成空壳」时的护栏——
      没跑的道不许被读成「过」。

边界（不是这几枚件，别互相代填）：
    不是 `cn-earnings-note`（那枚做业绩点评，本件只登记表内数）；
    不是 `cn-eps-cn`（那枚做每股收益的计算口径，本件只照抄表里的 EPS 与每股净资产）；
    不是 `cn-debt-restructuring-cn`（非经常性损益明细里的重组损益那几行本件照抄，不判性质）；
    不是 `tear-sheet`（那是五段一页纸，本件是这张表的逐行登记）。
"""

import argparse
import contextlib
import io
import os
import re
import sys
import tempfile

SLUG = "cue-cn-key-financial-data-cn"

CODES = ("KF-STRUCT", "KF-QUOTE", "KF-CALC", "KF-LINK", "KF-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议")

SECTIONS = ("主要会计数据", "主要财务指标", "非经常性损益明细",
            "扣非净利润勾稽", "分季度主要会计数据", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"

# 未落字的码：抛未落字一律计「不可判」，不许并进「不合」，也不许算「过」；
# 不在清单里却抛未落字＝声明与实装不符，由 check_text 直接发条。
# 本件五道已全部落字，清单为空。留着这个机制是为了某道回退成壳时不把「没跑」读成「过」。
UNIMPLEMENTED = ()

HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")

TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
ANCHOR_BLOCK = re.compile(r"〔\s*锚\s*[:：][^〕]*〕")
ANCHOR_REF = re.compile(r"\[(S\d+)\]")
REF_TAIL = re.compile(r"\[(S\d+)\]\s*$")

SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)"
    r"\|\s*(?P<url>https?://\S+)\s*\|"
    r"\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$"
)


# ---------------------------------------------------------------- 判据（道一已落字，道二至五空壳）

def _not_judged(code, why):
    """空壳的唯一出口：抛未落字，由 check_text 捕获计入「不可判」，不返回空表。"""
    raise NotImplementedError("%s 未落字：%s" % (code, why))


def check_struct(head, sections, stray):
    """道一 KF-STRUCT 形制：头部三件自标、七节齐且按序、节标题可识别。

    只判「形」：自标在不在、节名在不在、顺序对不对、有没有野节。内容对不对是另四道的事——
    这里不越界，否则一支注入会同时红两道、分不清归属。
    不判「主体：」「报告期：」：本件规格只列三件自标，不自行加判据。
    """
    out = []
    htext = "\n".join(s for _i, s in head)
    for mark in MARK_TEXTS:
        if mark not in htext:
            out.append(("KF-STRUCT", 1, "头部缺自标「%s」" % mark))

    # 丙：野节（认不出的节名／多出的同名节）逐条报，行号用 stray 给的
    for lineno, raw in stray:
        out.append(("KF-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw))

    # 丁：七节须齐且按序
    names = [n for n, _l, _b in sections]
    missing = [n for n in SECTIONS if n not in names]
    if missing:
        out.append(("KF-STRUCT", 1, "缺节：%s" % "／".join(missing)))
    elif names != list(SECTIONS):
        out.append(("KF-STRUCT", 1, "节序不对：现序 %s，应序 %s"
                    % ("／".join(names), "／".join(SECTIONS))))
    return out


def check_quote(head, sections, stray):
    """道二 KF-QUOTE：主要会计数据／主要财务指标两节的数字行必须带「」原文摘句。

    只认形：引号在不在、里面有没有字、够不够 8 字。**不核对引文里的数与行首的数是否一致**
    ——那是 KF-LINK 的事；两处都判的话一支注入会红两道，分不清是谁的问题。
    缺口行豁免：`未取到：X` 本来就没有原句可摘，硬要引号就是逼人编。
    """
    out = []
    for name, _ln, body in sections:
        if name not in ("主要会计数据", "主要财务指标"):
            continue
        for lineno, s in body:
            if not _is_finding_line(s) or _is_gap_line(s):
                continue
            if not NUM_RE.search(s):
                continue
            quotes = QUOTE.findall(s)
            if not quotes:
                out.append(("KF-QUOTE", lineno, "数字行没有「」原文引号"))
            elif not any(_quote_ok(q) for q in quotes):
                out.append(("KF-QUOTE", lineno,
                            "「」引文不足 %d 字或只有数字没有字：%s"
                            % (QUOTE_MIN_CHARS, quotes[0])))
    return out


def check_calc(head, sections, stray):
    """道三 KF-CALC：增减幅度能重算对上，扣非净利润能勾稽上。

    ① 只在一段「」引文内部算：同一段引文里同时给出本期金额、上年同期金额与一个
      增减／同比／变动百分数，才按 `(本期−上年)/|上年|` 重算，差 > 0.05 个百分点发条。
      三项缺一、上年为 0、或行首登记值与引文不一致（那是 KF-LINK）都不归这道——
      拿 0 去补、拿行首的数去顶，都是自己造发条。
    ② 扣非净利润勾稽：归母净利润 − 归属于母公司股东的非经常性损益净额 = 扣非净利润，
      差 > 0.01 万元发条。三数缺一即不判；**不拿「非经常性损益小计」顶替净额**——
      小计未扣所得税影响、未扣少数股东，拿它去减恒不等，那是假发条。
    """
    out = []
    for _name, _ln, body in sections:
        for lineno, s in body:
            if not _is_finding_line(s) or _is_gap_line(s):
                continue
            for quote in QUOTE.findall(s):
                this = _clause_amount(quote, ("本期",), skip=("上年", "上年同期"))
                prev = _clause_amount(quote, ("上年同期", "上年", "上期"))
                disc = _clause_pct(quote)
                if not (this and prev) or disc is None:
                    continue
                tv = _to_wan(*this)
                pv = _to_wan(*prev)
                if pv == 0:
                    break              # 上年为 0：披露口径得不出比率，不判、不猜
                calc = (tv - pv) / abs(pv) * 100
                if abs(calc - disc) > GROWTH_TOL:
                    out.append(("KF-CALC", lineno,
                                "重算=%s%% 披露=%s%%（本期 %s 万元／上年 %s 万元）"
                                % (_fmt(calc), _fmt(disc), _fmt(tv), _fmt(pv))))
                break                  # 一条发现行只算它第一段带齐三件的引文

    picked = _deduct_numbers(sections)
    if all(k in picked for k in ("net", "nre", "ded")):
        net = _to_wan(*picked["net"][:2])
        nre = _to_wan(*picked["nre"][:2])
        ded = _to_wan(*picked["ded"][:2])
        gap = net - nre - ded
        if abs(gap) > WAN_TOL:
            out.append(("KF-CALC", picked["ded"][2],
                        "归母净利润−非经常性损益净额=%s 万元，扣非=%s 万元，差 %s 万元"
                        % (_fmt(net - nre), _fmt(ded), _fmt(gap))))
    return out


def check_link(head, sections, stray):
    """道四 KF-LINK：行首登记的每个数，都必须能在同一行引文里找到等值的那一个。

    数字归一：去千分位逗号、全角转半角、折成万元再比；单位不同但等值（`12.34 亿元`
    vs `123,400.00 万元`）算过，不算发条——那正是「照抄时换了单位」的合法写法。
    没有引号的行不归这道管（缺引号是 KF-QUOTE 的事）；缺口行跳过。
    """
    out = []
    for _name, _ln, body in sections:
        for lineno, s in body:
            if not _is_finding_line(s) or _is_gap_line(s):
                continue
            qi = s.find("「")
            if qi < 0:
                continue
            lead = _amounts(s[:qi])
            if not lead:
                continue
            quoted = _amounts("".join(QUOTE.findall(s)))
            miss = []
            for val, unit, _pos in lead:
                if unit == "%":
                    ok = any(u == "%" and abs(v - val) <= PCT_TOL for v, u, _q in quoted)
                else:
                    want = _to_wan(val, unit)
                    ok = any(u != "%" and abs(_to_wan(v, u) - want) <= WAN_TOL
                             for v, u, _q in quoted)
                if not ok:
                    miss.append("%s%s" % (val, unit))
            if miss:
                out.append(("KF-LINK", lineno, "行首=%s 引文里找不到等值数"
                            % "、".join(miss)))
    return out


def check_line(head, sections, stray):
    """道五 KF-LINE：该有的项必须在，单位口径不许串，勾稽不许断。

    项缺了按节报、行号用该节的标题行；节本身不在稿里就整节跳过——缺节是 KF-STRUCT 的事，
    在这里重报一遍只会让一支删节的注入红两道。
    """
    out = []
    for name, items in REQUIRED_ITEMS:
        body = _body(sections, name)
        if body is None:
            continue
        joined = "\n".join(s for _l, s in body)
        head_line = _section_line(sections, name)
        for item in items:
            if item not in joined:
                out.append(("KF-LINE", head_line, "「%s」节缺「%s」" % (name, item)))

    for _name, _ln, body in sections:
        for lineno, s in body:
            units = {u for _v, u, _p in _amounts(s)}
            if "元" in units and "万元" in units and not any(
                    w in s for w in ("换算", "折合", "即")):
                out.append(("KF-LINE", lineno, "同一行混用「元」与「万元」两套单位，未注明换算"))

    text = _all_text(head, sections, stray)
    if "扣非净利润" in text and "非经常性损益" not in text:
        out.append(("KF-LINE", 1, "出现了「扣非净利润」但全文无「非经常性损益」，勾稽断了"))
    return out


CHECKS = (
    ("KF-STRUCT", check_struct),
    ("KF-QUOTE", check_quote),
    ("KF-CALC", check_calc),
    ("KF-LINK", check_link),
    ("KF-LINE", check_line),
)


# ---------------------------------------------------------------- 道具

def _section_of(heading):
    """把 `## 3. 主要财务指标` 归一成 `主要财务指标`；认不出返回 None（当作 stray）。

    照 cn-changes-in-equity-cn/scripts/check_equity_statement.py 同名函数抄：
    先剥序号，再按节名比；节名后面紧跟字母数字的不算命中（`主要财务指标旧` 认不出）。
    """
    h = heading.strip()
    for _ in range(2):
        h2 = NUMBERING.sub("", h)
        if h2 == h:
            break
        h = h2
    h = h.strip()
    for name in SECTIONS:
        if h == name:
            return name
        if h.startswith(name) and not h[len(name):len(name) + 1].isalnum():
            return name
    return None


def split_doc(text):
    """→ (头部[(行号, 行)], [(节名, 标题行号, [(行号, 行)])], 野节[(行号, 原文)])

    野节＝不认识的节名，或多出来的同名节。它们**另记**、不吞进上一节——
    混进上一节会让「缺节」与「内容不在节里」两件事都看不出来。
    """
    header, sections, stray = [], [], []
    cur = None
    seen_h2 = False
    for i, raw in enumerate(text.split("\n"), 1):
        m = HEADING.match(raw)
        if m:
            seen_h2 = True
            name = _section_of(m.group(1))
            if name is None or any(name == n for n, _l, _b in sections):
                stray.append((i, raw.strip()))
                cur = None
                continue
            cur = (name, i, [])
            sections.append(cur)
            continue
        if not seen_h2:
            header.append((i, raw))
        elif cur is not None:
            cur[2].append((i, raw))
    return header, sections, stray


def _is_finding_line(s):
    return s.startswith("- ") or s == "-"


def _is_gap_line(s):
    """缺口行：本件没取到、如实登记的那种行（`未取到：X`）。缺口不挂原句与锚。"""
    return "未取到" in s


# ---------------------------------------------------------------- 数字道具

QUOTE_MIN_CHARS = 8        # 引文去空白后至少这么长，太短的是标签不是原句
GROWTH_TOL = 0.05          # 增减率重算容差，单位：百分点
WAN_TOL = 0.01             # 金额比对容差，单位：万元
PCT_TOL = 0.001            # 百分数比对容差

NUM_RE = re.compile(r"[0-9０-９]")
AMOUNT_RE = re.compile(
    r"(?P<v>[0-9０-９][0-9０-９,，]*(?:\.[0-9０-９]+)?)\s*"
    r"(?P<u>亿元|万元|千元|百万元|元|[%％])")
CJK_RE = re.compile(r"[一-鿿]")
# 切句：中文标点随便切；半角逗号只在两侧不是数字时才切——`1,234.00` 里那个逗号是千分位，
# 切开就把一个金额劈成两半（`本集团…1` ／ `234.00 亿元`），数的判据全都认不出来。
CLAUSE_SPLIT = re.compile(r"[。；、，]|(?<![0-9])[,](?![0-9])")

_FW = str.maketrans("０１２３４５６７８９．，", "0123456789.,")


def _dec(s):
    """全角转半角、去千分位后转 float；转不了返回 0.0（调用方的那一项本就不判）。"""
    try:
        return float(s.translate(_FW).replace(",", ""))
    except (TypeError, ValueError):
        return 0.0


def _to_wan(v, unit):
    """折成万元再比：单位不同但等值（12.34 亿元 vs 123,400.00 万元）必须算过。"""
    if unit == "亿元":
        return v * 10000.0
    if unit == "万元":
        return v
    if unit == "千元":
        return v / 10.0
    if unit == "百万元":
        return v * 100.0
    if unit == "元":
        return v / 10000.0
    return v


def _fmt(x):
    s = "%.4f" % x
    return s.rstrip("0").rstrip(".") or "0"


def _amounts(text):
    """→ [(数值, 单位, 位置)]。单位取 亿元／万元／千元／百万元／元／%；没单位的不算数。"""
    out = []
    for m in AMOUNT_RE.finditer(text):
        unit = m.group("u")
        out.append((_dec(m.group("v")), "%" if unit in "%％" else unit, m.start()))
    return out


def _quote_ok(q):
    """引文够不够长、里面有没有字：只有数字的引文不是原句，是数字抄了第二遍。"""
    compact = re.sub(r"\s+", "", q)
    return len(compact) >= QUOTE_MIN_CHARS and bool(CJK_RE.search(compact))


def _clause_amount(quote, keys, skip=()):
    """按 ，。；、 切句，取第一个含 keys 且不含 skip 的句子里第一个**金额**（% 不算）。"""
    for part in CLAUSE_SPLIT.split(quote):
        if any(k in part for k in keys) and not any(k in part for k in skip):
            for val, unit, _pos in _amounts(part):
                if unit != "%":
                    return val, unit
    return None


def _clause_pct(quote):
    """取带 增减／同比／变动／增长／下降 的句子里那一个百分数；「下降」记作负。"""
    for part in CLAUSE_SPLIT.split(quote):
        if not any(k in part for k in ("增减", "同比", "变动", "增长", "下降")):
            continue
        for val, unit, _pos in _amounts(part):
            if unit == "%":
                return -val if "下降" in part else val
    return None


def _label_of(s):
    """发现行「」之前那一段（登记值所在处）。"""
    qi = s.find("「")
    return s if qi < 0 else s[:qi]


def _body(sections, name):
    for n, _ln, body in sections:
        if n == name:
            return body
    return None


def _section_line(sections, name):
    for n, ln, _body_ in sections:
        if n == name:
            return ln
    return 1


def _all_text(head, sections, stray):
    parts = [s for _i, s in head]
    for _n, _l, body in sections:
        parts.extend(s for _i, s in body)
    parts.extend(raw for _i, raw in stray)
    return "\n".join(parts)


REQUIRED_ITEMS = (
    ("主要会计数据", ("营业收入", "归属于上市公司股东的净利润",
                      "扣除非经常性损益的净利润", "经营活动产生的现金流量净额",
                      "总资产", "归属于上市公司股东的净资产", "基本每股收益")),
    ("主要财务指标", ("加权平均净资产收益率", "每股净资产")),
)


def _deduct_numbers(sections):
    """找齐 归母净利润／非经常性损益净额／扣非净利润 三个数：优先「扣非净利润勾稽」节，再全稿。

    **不拿「非经常性损益小计」顶替净额**：小计未扣所得税影响、未扣少数股东权益，
    拿它去减恒不等，那是自己造出来的假发条。缺哪个就少哪个键，调用方判不了即不判。
    """
    pools = []
    body = _body(sections, "扣非净利润勾稽")
    if body is not None:
        pools.append(body)
    pools.append([ln for _n, _l, b in sections for ln in b])
    got = {}
    for pool in pools:
        for lineno, s in pool:
            if _is_gap_line(s):
                continue
            lab = _label_of(s)
            amt = [a for a in _amounts(lab) if a[1] != "%"]
            if not amt:
                continue
            val, unit, _pos = amt[0]
            if "非经常性损益" in lab and "净额" in lab:
                got.setdefault("nre", (val, unit, lineno))
            elif "扣除" in lab and "净利润" in lab:
                got.setdefault("ded", (val, unit, lineno))
            elif "净利润" in lab and "归属于" in lab:
                got.setdefault("net", (val, unit, lineno))
        if all(k in got for k in ("net", "nre", "ded")):
            return got
    return got


def check_text(text):
    """→ (findings[(code, line, msg)], unjudged[(code, why)])。

    空壳抛 NotImplementedError 一律计入 unjudged，**不计入「零发条」**、也不裸抛；
    不在 UNIMPLEMENTED 里的码抛未落字则按「声明与实装不符」直接发条——
    那是真缺陷（说自己落字了、实际是空壳），不能计不可判了事。
    """
    head, sections, stray = split_doc(text)
    findings, unjudged = [], []
    for code, fn in CHECKS:
        try:
            found = fn(head, sections, stray) or []
            findings.extend(found)
        except NotImplementedError as exc:
            if code in UNIMPLEMENTED:
                unjudged.append((code, str(exc)))
            else:
                findings.append((code, 1, "判据不在未落字清单里却抛未落字：%s" % exc))
    findings.sort(key=lambda x: (x[1], CODES.index(x[0])))
    return findings, unjudged


def _report_text(path, findings, unjudged):
    """纯函数：把报告拼成一段文本返回，**不 print**。

    与 report() 共用这一段：自测拿到的文本必须就是用户看到的文本。
    两条路径各拼一遍的话，自测验的是自己的副本，措辞一漂移它就验不出真话。
    """
    lines = []
    for code, line, msg in findings:
        lines.append("%s L%s %s" % (code, line, msg))
    for code, why in unjudged:
        lines.append("不可判 %s（%s）" % (code, why))
    if findings:
        lines.append("—— 机检：%d 条发条；判据未落字 %d 道" % (len(findings), len(unjudged)))
    elif unjudged:
        lines.append("—— 机检：0 条发条，但 %d 道判据尚未落字，**这不等于合规**" % len(unjudged))
    else:
        lines.append("—— 机检：0 条发条")
    return "\n".join(lines) + "\n"


def report(path, findings, unjudged):
    """打印就是 _report_text 的结果，一行不加、一字不改——两条路径同一段文本。"""
    sys.stdout.write(_report_text(path, findings, unjudged))


DEMO = r"""# 示例材料（600000.SH）主要会计数据与财务指标登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议
主体：示例材料（600000.SH）
报告期：2025 年年度报告·第一节·主要会计数据和财务指标

## 主要会计数据

- 营业收入〔口径：本期〕1,234.00 亿元「本集团本期实现营业收入人民币 1,234.00 亿元」〔锚：2025 年年报·第 12 页·主要会计数据和财务指标〕[S1]
- 营业收入〔口径：上期〕1,150.00 亿元「上年同期实现营业收入人民币 1,150.00 亿元」〔锚：2025 年年报·第 12 页·主要会计数据和财务指标〕[S1]
- 归属于上市公司股东的净利润〔口径：本期〕123.00 亿元「本期归属于上市公司股东的净利润为人民币 123.00 亿元」〔锚：2025 年年报·第 12 页·主要会计数据和财务指标〕[S1]
- 扣除非经常性损益的净利润〔口径：本期〕110.00 亿元「本期归属于上市公司股东的扣除非经常性损益的净利润为人民币 110.00 亿元」〔锚：2025 年年报·第 12 页·主要会计数据和财务指标〕[S1]
- 经营活动产生的现金流量净额〔口径：本期〕200.00 亿元「本期经营活动产生的现金流量净额为人民币 200.00 亿元」〔锚：2025 年年报·第 12 页·主要会计数据和财务指标〕[S1]
- 总资产〔口径：本期末〕5,000.00 亿元「本报告期末总资产为人民币 5,000.00 亿元」〔锚：2025 年年报·第 12 页·主要会计数据和财务指标〕[S1]
- 归属于上市公司股东的净资产〔口径：本期末〕2,000.00 亿元「本报告期末归属于上市公司股东的净资产为人民币 2,000.00 亿元」〔锚：2025 年年报·第 12 页·主要会计数据和财务指标〕[S1]
- 基本每股收益〔口径：本期〕1.23 元「本期基本每股收益为人民币 1.23 元」〔锚：2025 年年报·第 12 页·主要会计数据和财务指标〕[S1]

## 主要财务指标

- 基本每股收益〔口径：本期〕1.23 元「本期基本每股收益为人民币 1.23 元」〔锚：2025 年年报·第 12 页·主要会计数据和财务指标〕[S1]
- 加权平均净资产收益率〔口径：本期〕6.20%「本期加权平均净资产收益率为 6.20%，比上年减少 0.30 个百分点」〔锚：2025 年年报·第 12 页·主要会计数据和财务指标〕[S1]
- 每股净资产〔口径：本期末〕20.00 元「本报告期末归属于上市公司股东的每股净资产为人民币 20.00 元」〔锚：2025 年年报·第 12 页·主要会计数据和财务指标〕[S1]
- 营业收入比上年增减〔口径：本期对上年〕7.30%「本集团本期实现营业收入人民币 1,234.00 亿元，上年同期为人民币 1,150.00 亿元，同比增长 7.30%」〔锚：2025 年年报·第 12 页·主要会计数据和财务指标〕[S1]

## 非经常性损益明细

- 非流动资产处置损益 2.00 亿元「本期非流动资产处置损益为人民币 2.00 亿元」〔锚：2025 年年报·第 13 页·非经常性损益项目及金额〕[S2]
- 计入当期损益的政府补助 8.00 亿元「本期计入当期损益的政府补助为人民币 8.00 亿元」〔锚：2025 年年报·第 13 页·非经常性损益项目及金额〕[S2]
- 委托他人投资或管理资产的损益 5.00 亿元「本期委托他人投资或管理资产的损益为人民币 5.00 亿元」〔锚：2025 年年报·第 13 页·非经常性损益项目及金额〕[S2]
- 除上述各项之外的其他营业外收入和支出 1.00 亿元「本期除上述各项之外的其他营业外收入和支出为人民币 1.00 亿元」〔锚：2025 年年报·第 13 页·非经常性损益项目及金额〕[S2]
- 非经常性损益小计 16.00 亿元「本期非经常性损益项目小计人民币 16.00 亿元」〔锚：2025 年年报·第 13 页·非经常性损益项目及金额〕[S2]
- 减：所得税影响额 2.50 亿元「减：本期所得税影响额为人民币 2.50 亿元」〔锚：2025 年年报·第 13 页·非经常性损益项目及金额〕[S2]
- 减：少数股东权益影响额 0.50 亿元「减：本期少数股东权益影响额为人民币 0.50 亿元」〔锚：2025 年年报·第 13 页·非经常性损益项目及金额〕[S2]
- 归属于母公司股东的非经常性损益净额 13.00 亿元「本期归属于母公司股东的非经常性损益净额为人民币 13.00 亿元」〔锚：2025 年年报·第 13 页·非经常性损益项目及金额〕[S2]

## 扣非净利润勾稽

- 归属于上市公司股东的净利润 123.00 亿元「本期归属于上市公司股东的净利润为人民币 123.00 亿元」〔锚：2025 年年报·第 12 页·主要会计数据和财务指标〕[S1]
- 归属于母公司股东的非经常性损益净额 13.00 亿元「本期归属于母公司股东的非经常性损益净额为人民币 13.00 亿元」〔锚：2025 年年报·第 13 页·非经常性损益项目及金额〕[S2]
- 扣除非经常性损益的净利润 110.00 亿元「本期归属于上市公司股东的扣除非经常性损益的净利润为人民币 110.00 亿元」〔锚：2025 年年报·第 12 页·主要会计数据和财务指标〕[S1]

## 分季度主要会计数据

- 营业收入〔季度：第一季度〕280.00 亿元「第一季度实现营业收入人民币 280.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]
- 营业收入〔季度：第二季度〕300.00 亿元「第二季度实现营业收入人民币 300.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]
- 营业收入〔季度：第三季度〕310.00 亿元「第三季度实现营业收入人民币 310.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]
- 营业收入〔季度：第四季度〕344.00 亿元「第四季度实现营业收入人民币 344.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]
- 归属于上市公司股东的净利润〔季度：第一季度〕25.00 亿元「第一季度归属于上市公司股东的净利润为人民币 25.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]
- 归属于上市公司股东的净利润〔季度：第二季度〕30.00 亿元「第二季度归属于上市公司股东的净利润为人民币 30.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]
- 归属于上市公司股东的净利润〔季度：第三季度〕31.00 亿元「第三季度归属于上市公司股东的净利润为人民币 31.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]
- 归属于上市公司股东的净利润〔季度：第四季度〕37.00 亿元「第四季度归属于上市公司股东的净利润为人民币 37.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]

## 口径与未取到

- 未取到：无
- 口径：主要会计数据与财务指标一律照抄年报第一节表格原文；本期比上年增减只照抄表里那一格，本件不自己四舍五入、不自己换单位；非经常性损益明细照抄，本件不判其性质。

## 来源

- [S1] 示例材料 2025 年年度报告·第一节·主要会计数据和财务指标 | https://example.invalid/600000_2025_annual.pdf | 检索日 2026-03-20
- [S2] 示例材料 2025 年年度报告·非经常性损益项目及金额 | https://example.invalid/600000_2025_annual.pdf | 检索日 2026-03-20
- [S3] 示例材料 2025 年年度报告·分季度主要财务数据 | https://example.invalid/600000_2025_annual.pdf | 检索日 2026-03-20
"""


def _must_replace(text, old, new, count=1):
    """注入点必须落地：片段不在源件、或替换后字节没变，一律 raise，不静默放过。

    静默放过的注入会让坏样等于好样，那一档就永远「过」——比不合更坏。
    """
    n = text.count(old)
    if n < count:
        raise AssertionError("注入点未落地：片段出现 %d 次，至少要 %d 次：%r" % (n, count, old))
    out = text.replace(old, new, count)
    if out == text:
        raise AssertionError("注入后字节未变：%r -> %r" % (old, new))
    return out


# 坏样都由好样单向替换而来，只动那一档真正看的那一处。
# (a) 头部少一件自标。
BAD_MARK = _must_replace(DEMO, "不构成投资建议", "", 1)
# (b) 一个节标题写成认不出的样子：该节既进不了 sections（算缺节），标题本身也进 stray。
#     注：不能用「## 主要财务指标（旧）」——全角括号前 `not isalnum()` 为真，_section_of 仍认得出；
#     要接一个字母数字才算认不出（「指标旧」落空 → None → stray）。这是实测出来的形。
BAD_HEADING = _must_replace(DEMO, "## 主要财务指标\n", "## 主要财务指标旧\n", 1)
# (c) 整节删掉「分季度主要会计数据」（连标题与八行）：七节不齐。
_SECTION_BLOCK = ("## 分季度主要会计数据\n"
                  "\n"
                  "- 营业收入〔季度：第一季度〕280.00 亿元「第一季度实现营业收入人民币 280.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]\n"
                  "- 营业收入〔季度：第二季度〕300.00 亿元「第二季度实现营业收入人民币 300.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]\n"
                  "- 营业收入〔季度：第三季度〕310.00 亿元「第三季度实现营业收入人民币 310.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]\n"
                  "- 营业收入〔季度：第四季度〕344.00 亿元「第四季度实现营业收入人民币 344.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]\n"
                  "- 归属于上市公司股东的净利润〔季度：第一季度〕25.00 亿元「第一季度归属于上市公司股东的净利润为人民币 25.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]\n"
                  "- 归属于上市公司股东的净利润〔季度：第二季度〕30.00 亿元「第二季度归属于上市公司股东的净利润为人民币 30.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]\n"
                  "- 归属于上市公司股东的净利润〔季度：第三季度〕31.00 亿元「第三季度归属于上市公司股东的净利润为人民币 31.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]\n"
                  "- 归属于上市公司股东的净利润〔季度：第四季度〕37.00 亿元「第四季度归属于上市公司股东的净利润为人民币 37.00 亿元」〔锚：2025 年年报·第 14 页·分季度主要财务数据〕[S3]\n"
                  "\n")
BAD_SECTION = _must_replace(DEMO, _SECTION_BLOCK, "", 1)
# (d) 数字行摘掉「」原文引号：只该红 KF-QUOTE（KF-LINK 见无引号即跳过，不跟着红）。
BAD_NO_QUOTE = _must_replace(
    DEMO,
    "「本集团本期实现营业收入人民币 1,234.00 亿元」",
    "", 1)
# (e) 登记值与披露值一起改成 9.30%：两处一致（KF-LINK 过），但与本期／上年两个数重算不出 9.30%
#     （重算 7.3043%），只该红 KF-CALC。两处都改是必要的——只改一处会把 KF-LINK 一起拉红。
BAD_CALC = _must_replace(DEMO, "7.30%", "9.30%", 2)
# (f) 只改引文里的收入数：行首 1,234.00 亿元 与引文 1,243.00 亿元 对不上，只该红 KF-LINK。
BAD_LINK = _must_replace(
    DEMO,
    "「本集团本期实现营业收入人民币 1,234.00 亿元」",
    "「本集团本期实现营业收入人民币 1,243.00 亿元」", 1)
# (g) 删掉「经营活动产生的现金流量净额」那一行：只该红 KF-LINE（该有的项少了）。
BAD_ITEM = _must_replace(
    DEMO,
    "- 经营活动产生的现金流量净额〔口径：本期〕200.00 亿元"
    "「本期经营活动产生的现金流量净额为人民币 200.00 亿元」"
    "〔锚：2025 年年报·第 12 页·主要会计数据和财务指标〕[S1]\n",
    "", 1)


def selftest():
    """逐档现报：好样须零发条，坏样须恰发 KF-STRUCT；未落字各算一档「不可判」。

    档数＝逐档比对的那几档 + UNIMPLEMENTED 的码数（未落字各算一档「不可判」），
    两段都从现场值算，不写死数字。本拍四道空壳，好样单稿退 3；
    落字一道，这两处自己从 3 变 0，不用手改。
    """
    cases = (
        ("好样应零发条（五道均落字）", DEMO, frozenset()),
        ("形制：头部删掉「不构成投资建议」", BAD_MARK, frozenset({"KF-STRUCT"})),
        ("形制：节标题写成认不出的样子（进 stray＋缺节）", BAD_HEADING,
         frozenset({"KF-STRUCT"})),
        ("形制：整节删掉「分季度主要会计数据」", BAD_SECTION, frozenset({"KF-STRUCT"})),
        ("引号：数字行摘掉「」原句", BAD_NO_QUOTE, frozenset({"KF-QUOTE"})),
        ("增减：登记值与披露值同改成 9.30%（重算 7.3043%）", BAD_CALC,
         frozenset({"KF-CALC"})),
        ("数字：引文里的收入数与行首对不上", BAD_LINK, frozenset({"KF-LINK"})),
        ("项：删掉「经营活动产生的现金流量净额」一行", BAD_ITEM, frozenset({"KF-LINE"})),
    )
    bad = 0
    last_unjudged = ()
    for label, text, want in cases:
        findings, unjudged = check_text(text)
        last_unjudged = unjudged
        got = frozenset(c for c, _l, _m in findings)
        if got == want:
            print("过   %s（发条 %d 条：%s）"
                  % (label, len(findings), "、".join(sorted(got)) or "无"))
        else:
            bad += 1
            detail = "；".join("%s L%s %s" % (c, l, m) for c, l, m in findings[:4])
            print("不合 %s：期望 %s 实得 %s ｜ %s"
                  % (label, sorted(want) or "无", sorted(got) or "无", detail))

    # 覆盖自证：每道已落字的码，在 cases 里至少有一档期望恰含它。
    # 这条防的是「实现了一道判据、同时少了一档反例，净增反例 0 档」——
    # 判据接进 CHECKS 却没有反例钉住，它以后被改坏，自测照样报 不合=0。
    # 本拍只有 KF-STRUCT，但这条现在就写进去：它下一拍会替我们抓漏。
    implemented = [c for c in CODES if c not in UNIMPLEMENTED]
    covered = set()
    for _label, _text, want in cases:
        covered |= set(want)
    uncovered = [c for c in implemented if c not in covered]
    print("%s 覆盖自证：已落字码 %d 道，有反例的 %d 道，缺反例：%s"
          % ("不合" if uncovered else "过  ",
             len(implemented), len(implemented) - len(uncovered),
             "／".join(uncovered) if uncovered else "无"))
    if uncovered:
        bad += 1

    # 空壳自证：清单里的码调用即抛且点名自身；不在清单里的码不许抛，只能返回列表
    shell_bad = []
    for code, fn in CHECKS:
        try:
            got = fn([], [], [])
        except NotImplementedError as exc:
            if code not in UNIMPLEMENTED:
                shell_bad.append("%s 已声明落字却抛未落字（%s）" % (code, exc))
            elif code not in str(exc):
                shell_bad.append("%s 抛出但未点名码（%s）" % (code, exc))
            continue
        if code in UNIMPLEMENTED:
            shell_bad.append("%s 返回了 %r，空壳必须抛未落字" % (code, got))
        elif not isinstance(got, list):
            shell_bad.append("%s 返回 %r，应返回列表" % (code, got))
    if shell_bad:
        bad += 1
        print("不合 空壳自证：%s" % "；".join(shell_bad))
    elif UNIMPLEMENTED:
        print("过   空壳自证（%s 调用即抛并点名；其余返回列表）"
              % "、".join(UNIMPLEMENTED))
    else:
        print("过   空壳自证（未落字清单为空，五道均返回列表）")

    # 不崩自证：空稿、乱头、只头无节都过一遍，必须返回二元组且未落字的码全计不可判
    crash = []
    for label, text in (("空稿", ""), ("乱头", "x\n"), ("只头无节", DEMO.split("## ")[0])):
        try:
            _f2, u2 = check_text(text)
        except Exception as exc:                       # noqa: BLE001 — 自证只问崩不崩
            crash.append("%s 抛出 %s: %s" % (label, type(exc).__name__, exc))
            continue
        got_codes = {c for c, _w in u2}
        if got_codes != set(UNIMPLEMENTED):
            crash.append("%s 不可判 %s，应为 %s"
                         % (label, sorted(got_codes) or "无", sorted(UNIMPLEMENTED) or "无"))
    if crash:
        bad += 1
        print("不合 不崩自证：%s" % "；".join(crash))
    elif UNIMPLEMENTED:
        print("过   不崩自证（空稿／乱头／只头无节均返回二元组，未落字 %d 道计不可判）"
              % len(UNIMPLEMENTED))
    else:
        print("过   不崩自证（空稿／乱头／只头无节均返回二元组，无未落字）")

    # 单稿退码自证：好样落盘单跑，退码与「是否还有未落字」绑定，不写死数：
    # 有未落字 → 3（且输出须含「不可判」与「这不等于合规」）；全落字 → 0（且不得再出现该句）。
    rc, out, tmp = None, "", None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8",
                                         delete=False) as fh:
            fh.write(DEMO)
            tmp = fh.name
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main([tmp])
        out = buf.getvalue()
    finally:
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass
    want_rc = 3 if UNIMPLEMENTED else 0
    if rc != want_rc:
        bad += 1
        print("不合 单稿退码自证：好样单稿 rc=%r，应为 %d（未落字 %d 道）"
              % (rc, want_rc, len(UNIMPLEMENTED)))
    elif want_rc == 3 and ("不可判" not in out or "这不等于合规" not in out):
        bad += 1
        print("不合 单稿退码自证：rc=3 但输出缺口径字样")
    elif want_rc == 0 and "这不等于合规" in out:
        bad += 1
        print("不合 单稿退码自证：已无未落字，输出却仍写「这不等于合规」")
    else:
        print("过   单稿退码自证（好样单稿 rc=%d，未落字 %d 道%s）"
              % (want_rc, len(UNIMPLEMENTED),
                 "，输出含「不可判」与「这不等于合规」" if want_rc == 3 else "，输出无「这不等于合规」"))

    unk = len({c for c, _w in last_unjudged})
    print("——")
    print("自测档数=%d｜不合=%d｜不可判=%d" % (len(cases) + len(UNIMPLEMENTED), bad, unk))
    if bad:
        return 1
    return 3 if unk else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="主要会计数据与财务指标登记稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="主要会计数据登记稿 .md 路径")
    ap.add_argument("--selftest", action="store_true", help="跑包内夹具自检")
    ap.add_argument("--demo", action="store_true", help="打印一份七节样例（零输入可跑）")
    try:
        args = ap.parse_args(argv)
    except SystemExit:                                 # 用法错统一退 2，不沿用 argparse 的 2/0 混用
        return 2

    if args.selftest:
        return selftest()
    if args.demo:
        sys.stdout.write(DEMO)
        return 0
    if not args.path:
        ap.print_usage(sys.stderr)
        print("缺入参：给一份主要会计数据登记稿路径，或用 --demo / --selftest", file=sys.stderr)
        return 2
    try:
        with open(args.path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except (IOError, OSError) as exc:
        print("读不到文件：%s（%s）" % (args.path, exc))
        return 3
    if not text.strip():
        print("空稿：%s" % args.path)
        return 3

    findings, unjudged = check_text(text)
    report(args.path, findings, unjudged)
    if findings:
        return 1
    return 3 if unjudged else 0


if __name__ == "__main__":
    sys.exit(main())
