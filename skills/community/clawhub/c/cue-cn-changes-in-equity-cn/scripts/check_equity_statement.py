#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_equity_statement.py — 所有者权益变动表登记稿五道机检（零网络、零外发、不读环境变量）

**五道全部落字**：EQ-STRUCT（形制）、EQ-QUOTE（原句与锚）、EQ-FOOT（行列轧平）、
EQ-LINK（勾稽）、EQ-LINE（红线＋缺口两向对账）。
`--selftest` 末行「自测档数=N｜不合=0｜不可判=0」，退码 0。
空壳机制保留但 `UNIMPLEMENTED` 已清空：若某道将来回退成空壳（重新登记进 `UNIMPLEMENTED`
并改成调用即抛），`--selftest` 会照实报「不可判=N 道」、单稿退 3——
**零发条不等于合规**：没跑的道不能算过，rc=0 只留给「五道全过」。

用法：
    python3 scripts/check_equity_statement.py <所有者权益变动表登记稿>.md
    python3 scripts/check_equity_statement.py --selftest      跑包内夹具自检
    python3 scripts/check_equity_statement.py --demo          打印一份七节样例（零输入可跑）

七节（按序，`## ` 起节）：
    权益变动总览／本期增减变动／利润分配与所有者投入／期末余额与勾稽
    ／归属于母公司与少数股东／口径与未取到／来源

五道码（**全部已落字**，下表写的是每道判什么）：

道一 EQ-STRUCT 形制（已落字）
  头部（第一个 `## ` 之前）三件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议；
  七节齐且按序；认不出的节标题与多出的同名节逐条发。
  主体／报告期两行不在本道判据内——本件规格只列三件自标，不自行加。

道二 EQ-QUOTE 原句与锚（已落字）
  每条发现行以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；缺哪件点名哪件；
  例外只有三形：「未取到：」行、[待人工] 行与〔自算〕行；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址；
  两向对账：正文引的 [S#] 须在来源节登记，来源节登记的 [S#] 也须被正文引用过；
  来源节一条合规来源行都没有则单独发一条。

道三 EQ-FOOT 行列轧平（已落字）
  两条断言，都只在参与运算的数**全部**披露时才判：
  ① 列内纵向：同一列里 期末余额 ＝ 期初余额 ＋ 本期增减变动；
  ② 行内横向：同一行里 合计 ＝ 各列之和。
  数按「行（项目名）＋列（列名）」对齐，不按行序／列序；认不出表形（解析不出项目名或列名）
  ⇒ 记未取到、不判，宁可漏判不误判。金额归一（去千分位、去单位词后按分比），
  容差只许半分（0.01）以内的四舍五入差。任一参与数缺 ⇒ 不判，不许拿 0 补。

道四 EQ-LINK 勾稽（已落字）
  本期「综合收益总额」须等于「净利润」＋「其他综合收益税后净额」两数之和。
  两数都在稿里才判；缺一数即不判，不猜、不推。

道五 EQ-LINE 红线＋缺口两向对账（已落字）
  甲 不得自己下判断（股东回报丰厚／高送转预期／管理层意图／分红慷慨／大股东看好／
     值得买入／建议关注／后市可期——与同族件逐字同表，不另造）；
  乙 同一行里出现「未分配利润」时，不得并写「可分现金／可分配现金／现金分红能力」；
  丙 缺口两向对账：正文 `未取到：X` ⇔ 「口径与未取到」节点名 X，两向各发一条；
     零缺口时该节写 `未取到：无`。`[待人工]` 行不算缺口（那是判断位，不是缺材料）。
  甲、乙扫全文但「口径与未取到」「来源」两节整节豁免：口径节按设计就要讲
  「不把未分配利润改写成可分现金」这类口径，不豁免会自己咬自己。

退码：0 五道全过 / 1 有发条 / 2 用法错（缺参数或未知参数）
      / 3 读不到文件或空稿，或零发条但仍有未落字判据（`UNIMPLEMENTED` 非空时）。
      本件五道全落字，好样单稿退 0；上面那条留着，是某道回退成空壳时的护栏。
"""

import argparse
import contextlib
import io
import os
import re
import sys
import tempfile

SLUG = "cue-cn-changes-in-equity-cn"

CODES = ("EQ-STRUCT", "EQ-QUOTE", "EQ-FOOT", "EQ-LINK", "EQ-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议")

SECTIONS = ("权益变动总览", "本期增减变动", "利润分配与所有者投入", "期末余额与勾稽",
            "归属于母公司与少数股东", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"

# 本拍落形制、锚、行列轧平、勾稽四道。下面一个码在自测里算一档「不可判」，不得并进「不合」。
# 落一道、从本元组里摘一道；摘空的当天 rc=0 才有资格出现。
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

# 道三的行列标记：列名必须显式写出，不靠位置序号——位置一改序就整片误红。
COL_TAG = re.compile(r"〔\s*列\s*[:：]\s*([^〕]+?)〕")
OPEN_ITEM = "期初余额"
MOVE_ITEM = "本期增减变动"
CLOSE_ITEM = "期末余额"
TOTAL_COL = "合计"

# 金额：可带千分位与小数。单位词在数之后单独取，换算归披露口径，本件只比同单位。
AMOUNT = re.compile(r"(?P<num>-?\d+(?:,\d{3})*(?:\.\d+)?)\s*(?P<unit>亿|万|千|百)?\s*元")
UNIT_WORD = re.compile(r"单位\s*[:：]\s*(?P<u>人民币)?\s*(?P<scale>亿|万|千|百)?\s*元")

# 只允许登记值最后一位的四舍五入差。表登记到 0.01（无论单位是元还是亿元），
# 半个末位是 0.005，两侧各舍一次最多差 0.01——所以容差是 **0.011 个登记单位**，
# 不是 0.011 元。绝不放宽到「1 元」或「0.1%」那种量级：那会把真不平吞掉。
TOL = 0.011

# 道三的现场读数：每次 check_text 开头清零，由 check_foot 填。
# 「判了几项」必须露到报告里——判 0 项与判 12 项全平若印出同一行，
# 读者会把「一行都没查」读成「这表平了」，那正是本族的老病：读不到当成 0。
_FOOT = {"col": 0, "row": 0, "cell_skipped": 0, "group_skipped": 0}


# ---------------------------------------------------------------- 判据

def _not_judged(code, why):
    """空壳的唯一出口：抛未落字，由 check_text 捕获计入「不可判」，不返回空表。

    不返回 [] 是立件判据：空表会被读成「这道跑过了、零发条」，而它根本没跑。
    """
    raise NotImplementedError("%s 未落字：%s" % (code, why))


def check_struct(head, sections, stray):
    """道一 EQ-STRUCT 形制：头部三件自标、七节齐且按序、节标题可识别。

    只判「形」：自标在不在、节名在不在、顺序对不对。内容对不对是另四道的事——
    这里不越界，否则一支注入会同时红两道、分不清归属。
    不判「主体：」「报告期：」：本件规格只列三件自标，不自行加判据。
    """
    out = []
    htext = "\n".join(s for _i, s in head)
    for mark in MARK_TEXTS:
        if mark not in htext:
            out.append(("EQ-STRUCT", 1, "头部缺自标「%s」" % mark))

    # 丙：野节（认不出的节名／多出的同名节）逐条报，行号用 stray 给的
    for lineno, raw in stray:
        out.append(("EQ-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw))

    # 丁：七节须齐且按序
    names = [n for n, _l, _b in sections]
    missing = [n for n in SECTIONS if n not in names]
    if missing:
        out.append(("EQ-STRUCT", 1, "缺节：%s" % "／".join(missing)))
    elif names != list(SECTIONS):
        out.append(("EQ-STRUCT", 1, "节序不对：现序 %s，应序 %s"
                    % ("／".join(names), "／".join(SECTIONS))))
    return out


def check_quote(head, sections, stray):
    """道二 EQ-QUOTE 原句与锚：来源行格式、发现行三元组、[S#] 两向对账。

    例外只有三形：「未取到：」行、[待人工] 行、〔自算〕行——前两者是缺口与判断位，
    后者已经必须交代算法与口径，要求它再挂原句等于把自算伪装成披露值。
    空来源节／没有来源节不在这里报（那是道一的事），这里只判格式与对应，不许崩。
    """
    out = []
    registered, reported_missing = set(), set()
    cited = set()

    # 甲：来源行格式，只扫来源节；不合规的行照样报，但不进 registered。
    # 非 `- ` 行也报：道一尚未管来源节空不空之外的行形制，若不在这里收，就两头都没人管。
    for name, _hline, body in sections:
        if name != SOURCE_SECTION:
            continue
        for lineno, s in body:
            if not s.strip():
                continue
            if not _is_finding_line(s):
                out.append(("EQ-QUOTE", lineno,
                            "来源节只许 `- [S#] 标题 | URL | 检索日` 行：%s" % s.strip()[:44]))
                continue
            m = SOURCE_LINE.match(s.strip())
            if not m:
                out.append(("EQ-QUOTE", lineno,
                            "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:44]))
                continue
            registered.add(m.group("s"))

    # 乙：发现行三元组，只扫五个内容节
    has_source = any(name == SOURCE_SECTION for name, _l, _b in sections)
    for name, _hline, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue                     # 形制那道会发，这里不重复
            cited |= set(ANCHOR_REF.findall(s))
            if _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s:
                continue                     # 缺口登记、人工位、自算行本来就不挂三元组
            if not TRIPLE.search(s):
                miss = []
                if not QUOTE.search(s):
                    miss.append("「」原句")
                if not ANCHOR_BLOCK.search(s):
                    miss.append("〔锚：…〕")
                if not ANCHOR_REF.search(s):
                    miss.append("[S#]")
                out.append(("EQ-QUOTE", lineno,
                            "发现行缺 %s（三元组须在行末）"
                            % "、".join(miss or ["「」原句 + 〔锚〕 + [S#] 的次序"])))
                continue
            m = REF_TAIL.search(s.strip())
            if not m:
                out.append(("EQ-QUOTE", lineno,
                            "发现行未以 [S#] 收尾（三元组须在行末）"))
                continue
            # 没有来源节、或来源节里一条合规行都没有时，同一个根因会在每一行重复铺开，
            # 把「哪一行真有问题」淹掉：根因由道一（缺节）或本道丙（零合规来源行）点一次。
            if not has_source or not registered:
                continue
            ref = m.group(1)
            if ref in registered or ref in reported_missing:
                continue                     # 同一个未登记 S 号只报一次，行号取首次引用处
            reported_missing.add(ref)
            out.append(("EQ-QUOTE", lineno,
                        "引用了未登记的 [%s]：来源节没有该 S 号的合规来源行" % ref))

    # 丙：来源节存在但一条合规来源行都没有——只在节在场时报，缺节归道一
    if has_source and not registered:
        out.append(("EQ-QUOTE", 1,
                    "来源节没有一条合规来源行：每个 [S#] 都要有可点 http(s) URL 与检索日"))

    # 丁：反向对账——来源节登记了、正文一次都没引用。挂着没人用的出处是死链的一种：
    # 要么正文该引没引，要么来源节多登记了一条读者找不到落点的来源。
    # 只在来源节有合规行时判（零合规行时根因已由丙点过一次，逐号铺开只会淹掉那条）。
    if registered:
        for name, _hline, body in sections:
            if name != SOURCE_SECTION:
                continue
            for lineno, s in body:
                m = SOURCE_LINE.match(s.strip())
                if not m:
                    continue
                sid = m.group("s")
                if sid in cited:
                    continue
                out.append(("EQ-QUOTE", lineno,
                            "来源登记了 [%s]，正文一次都没引用：出处没有落点" % sid))
    return out


def check_foot(head, sections, stray):
    """道三 EQ-FOOT 行列轧平：列内 期末＝期初＋增减，行内 合计＝各列之和。

    只判**认得出表形**的行：行里的列名必须由显式 `〔列：X〕` 标记给出，数额取该标记与
    第一个「」之间的那个数。认不出（没有列标记、没有数、单位不同）⇒ 记未取到、不判。
    **不按行序／列序定位**：位置序号一改序就整片误红，本族栽过这个坑。

    两条断言各自的「数不全就不判」是分开的：
    ① 列内纵向：某列里期初／增减／期末三项都在才判，缺一项即该列不判；
    ② 行内横向：某行里「合计」与**全部**已知成分列都在才判，缺一列即该行不判。
    成分列＝全稿出现过的列名去掉「合计」；某行少一列时，用剩下的列求和会算出错的合计，
    所以宁可整行不判，也不拿缺数去补 0——补 0 就是凭空造数。
    """
    out = []
    cells, units, columns = {}, {}, set()
    seen_tag = 0        # 认出列标记的行数
    seen_row = 0        # 内容节里的发现行数（判「本稿根本没有可比结构」用）

    for name, _hline, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue
            seen_row += 1
            m = COL_TAG.search(s)
            if not m:
                _FOOT["cell_skipped"] += 1
                continue                     # 没有列标记 ⇒ 认不出表形，不判
            seen_tag += 1
            item = s.strip()[2:m.start()].strip()
            col = m.group(1).strip()
            if not item or not col:
                _FOOT["cell_skipped"] += 1
                continue
            # 只在**登记值**里取数：第一个「」之后是照抄的原文，那里也有数，
            # 越过去取会把引文里的数当成本件登记的数额（登记值没数时尤其危险）。
            tail = s[m.end():]
            cut = tail.find("「")
            amount = _amount_of(tail if cut < 0 else tail[:cut])
            if amount is None:
                _FOOT["cell_skipped"] += 1
                continue                     # 没有数（或单位认不出）⇒ 未取到，不判
            value, unit = amount
            key = (item, col)
            # 同一行同一列重复登记：本件该合并成一条，这里不判（记未取到），
            # 免得按「后一条覆盖前一条」悄悄挑一个数去算。
            if key in cells:
                cells.pop(key)
                units.pop(key)
                continue
            cells[key] = value
            units[key] = unit
            if col != TOTAL_COL:
                columns.add(col)

    def amount_at(item, col):
        key = (item, col)
        if key not in cells:
            return None
        return cells[key]

    # 单位必须同族才比：1 亿元 与 10000 万元 是同一个数，但按字面比会判成差 9999。
    # 本件不替披露做换算（换算是猜口径），单位不一致就记未取到、不判。
    def same_unit(keys):
        us = {units[k] for k in keys}
        return len(us) == 1

    # ① 列内纵向：期末 ＝ 期初 ＋ 增减
    for col in sorted({c for _i, c in cells}):
        keys = [(OPEN_ITEM, col), (MOVE_ITEM, col), (CLOSE_ITEM, col)]
        vals = [amount_at(i, c) for i, c in keys]
        if any(v is None for v in vals):
            _FOOT["group_skipped"] += 1
            continue                         # 三数不齐 ⇒ 该列不判
        if not same_unit(keys):
            _FOOT["group_skipped"] += 1
            continue
        opening, moving, closing = vals
        _FOOT["col"] += 1                    # 这一列真的比过了
        if abs(closing - (opening + moving)) > TOL:
            lineno = _line_of(sections, CLOSE_ITEM, col)
            out.append(("EQ-FOOT", lineno,
                        "列内不平：列「%s」期末 %s ≠ 期初 %s ＋ 本期增减变动 %s（差 %s）"
                        % (col, _fmt(closing), _fmt(opening), _fmt(moving),
                           _fmt(closing - opening - moving))))

    # ② 行内横向：合计 ＝ 各成分列之和
    components = sorted(columns)
    if components:
        for item in sorted({i for i, _c in cells}):
            if amount_at(item, TOTAL_COL) is None:
                continue                     # 没有合计列 ⇒ 无可判
            parts = [amount_at(item, c) for c in components]
            if any(v is None for v in parts):
                _FOOT["group_skipped"] += 1
                continue                     # 成分列不齐 ⇒ 该行不判（不许拿缺数补 0）
            keys = [(item, c) for c in components] + [(item, TOTAL_COL)]
            if not same_unit(keys):
                _FOOT["group_skipped"] += 1
                continue
            total = amount_at(item, TOTAL_COL)
            _FOOT["row"] += 1                # 这一行真的比过了
            if abs(total - sum(parts)) > TOL:
                out.append(("EQ-FOOT", _line_of(sections, item, TOTAL_COL),
                            "行内不平：行「%s」合计 %s ≠ 各列之和 %s（各列 %s）"
                            % (item, _fmt(total), _fmt(sum(parts)),
                               "＋".join(_fmt(v) for v in parts))))

    # ③ 判了 0 项而稿里确有发现行 ⇒ 必须说出来。
    # 这一条是**发条**：零发条意味着「查过了、没问题」，而这里根本没查，
    # 印成同一行会让读者把「一行都没查」读成「这表平了」——本族的老病。
    checked = _FOOT["col"] + _FOOT["row"]
    if checked == 0 and seen_row > 0:
        out.append(("EQ-FOOT", 1,
                    "未判任何一项：本稿没有一行可解析出列标记（`〔列：X〕`），整表零校验——"
                    "**这不等于合规**。列标签常需按表头补回，或把表格按行重贴"))
    return out


def check_link(head, sections, stray):
    """道四 EQ-LINK 勾稽：本期增减变动内部的构成与总括，以及跨节合计对账。

    三条断言，各自独立地「数不齐就不判」：
    ① 综合收益总额 ＝ 净利润 ＋ 其他综合收益税后净额
    ② 本期增减变动合计 ＝ 综合收益总额 ＋ 所有者投入和减少资本 － 利润分配
       **符号约定：本表里「利润分配」是减少项**，所以减号；不靠「分配记成负数」那套约定，
       因为披露里分配额是正数，靠命名取符号比靠数据取符号稳。
    ③ 本期增减变动合计 ＝ 「权益变动总览」节里「本期增减变动〔列：合计〕」那一格

    取数一律用 `_amount_of`（与 EQ-FOOT 同一套口径，不另写）：千分位归一同一个函数、
    单位不一致同上返回 None、缺单位同上返回 None。容差沿用全局 TOL。
    项目名认不出就不判——「差不多的项目」硬配会把两张不同口径的表当成一张。

    净利润只认**合并口径**：行里的引文若写「归属于母公司所有者的净利润」，那是母公司口径，
    不能顶替合并净利润（合并数＝归母＋少数股东，两者本就不等）。宁可记未取到。
    """
    out = []
    # 本项目名 → (数, 单位)；项目名在全稿内容节里按行首项目名精确匹配。
    found = {}
    for name, _hline, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue
            item, value, unit, quote, lineno = _link_cell(s, lineno)
            if item is None or value is None:
                continue
            # 同一个项目名在多个节里出现（「净利润」在总览与勾稽节都可能登记）：
            # 只在不冲突时采用；两处数不同 → 记未取到，不挑一个。
            prev = found.get(item)
            if prev is not None and (abs(prev[0] - value) > TOL or prev[1] != unit):
                found[item] = None           # 冲突 ⇒ 作废
                continue
            found[item] = (value, unit, lineno, quote)

    def get(item):
        v = found.get(item)
        return v if v else None

    def same_unit(*keys):
        us = {found[k][1] for k in keys if found.get(k)}
        return len(us) == 1

    # ① 综合收益总额 ＝ 净利润 ＋ 其他综合收益税后净额
    k = (CMP_SECTION_ITEM["综合收益总额"], CMP_SECTION_ITEM["净利润"],
         CMP_SECTION_ITEM["其他综合收益税后净额"])
    if all(get(x) for x in k) and same_unit(*k):
        ni = get(CMP_SECTION_ITEM["净利润"])
        # 母公司口径的净利润不得顶替：引文里有「归属于母公司」且没有「合并」就作废。
        if _is_parent_only(ni[3]):
            ni = None
        if ni is not None:
            tci = get(CMP_SECTION_ITEM["综合收益总额"])[0]
            oci = get(CMP_SECTION_ITEM["其他综合收益税后净额"])[0]
            if abs(tci - (ni[0] + oci)) > TOL:
                out.append(("EQ-LINK", get(CMP_SECTION_ITEM["综合收益总额"])[2],
                            "综合收益总额 %s ≠ 净利润 %s ＋ 其他综合收益税后净额 %s（差 %s）"
                            % (_fmt(tci), _fmt(ni[0]), _fmt(oci), _fmt(tci - ni[0] - oci))))

    # ② 本期增减变动合计 ＝ 综合收益总额 ＋ 所有者投入和减少资本 － 利润分配
    k2 = (CMP_SECTION_ITEM["本期增减变动合计"], CMP_SECTION_ITEM["综合收益总额"],
          CMP_SECTION_ITEM["所有者投入和减少资本"], CMP_SECTION_ITEM["利润分配"])
    if all(get(x) for x in k2) and same_unit(*k2):
        total = get(CMP_SECTION_ITEM["本期增减变动合计"])
        tci = get(CMP_SECTION_ITEM["综合收益总额"])[0]
        put = get(CMP_SECTION_ITEM["所有者投入和减少资本"])[0]
        dist = get(CMP_SECTION_ITEM["利润分配"])[0]
        if abs(total[0] - (tci + put - dist)) > TOL:
            out.append(("EQ-LINK", total[2],
                        "本期增减变动合计 %s ≠ 综合收益总额 %s ＋ 所有者投入和减少资本 %s － 利润分配 %s（差 %s）"
                        % (_fmt(total[0]), _fmt(tci), _fmt(put), _fmt(dist),
                           _fmt(total[0] - tci - put + dist))))

    # ③ 跨节对账：本节合计 ＝ 「权益变动总览」里「本期增减变动〔列：合计〕」那一格
    here = get(CMP_SECTION_ITEM["本期增减变动合计"])
    there = _overview_total(sections)
    if here is not None and there is not None:
        v_there, u_there, l_there = there
        if here[1] == u_there and abs(here[0] - v_there) > TOL:
            out.append(("EQ-LINK", l_there,
                        "跨节不符：「权益变动总览」本期增减变动〔列：合计〕%s ≠ "
                        "「本期增减变动」节合计 %s（差 %s）"
                        % (_fmt(v_there), _fmt(here[0]), _fmt(v_there - here[0]))))
    return out


# 红线词族甲：自下判断。与同族件（CF-LINE／SG-LINE 等）逐字同表，不另造一套——
# 本件产出的是登记表，不是「回报厚不厚、要不要买」的结论。
# 只收确形：「关注」单字、「看好」单字都不收，收的是「值得买入」「建议关注」这类推荐动作。
JUDGE_BAN = ("股东回报丰厚", "高送转预期", "管理层意图", "分红慷慨", "大股东看好",
             "值得买入", "建议关注", "后市可期")

# 红线词族乙：把账面数说成真金白银。「未分配利润」是权益科目余额，不等于可分派的现金；
# 同一行里并写就等于把两个不同口径的东西画上了等号。
CASH_REWRITE = ("可分现金", "可分配现金", "现金分红能力")

# 缺口点名：`未取到：X`。X 取到第一个分隔符为止（不猜跨词的东西）。
# 「无」是特例：它表示「本件零缺口」，不是一个缺口名，两向对账里要单独放行。
GAP_MARK = re.compile(r"未取到\s*[：:]\s*([^\s，。；、｜」〕\[]+)")


def check_line(head, sections, stray):
    """道五 EQ-LINE 红线 ＋ 缺口两向对账。

    甲 自下判断零命中、乙 不得把「未分配利润」改写成「可分现金」：
    扫全文，但「口径与未取到」与「来源」两节整节豁免——口径节按设计就要写
    「不把未分配利润改写成可分现金」这类说明，不豁免会自己咬自己；来源节只有来源行。
    丙 缺口两向对账：正文点名 `未取到：X` ⇔ 口径节点名 X；零缺口时口径节写 `未取到：无`。
    只查一向等于没对账，所以两向各发一条。

    `[待人工]` 行不算缺口：那是判断位，不是本件没取到的材料。把它算进缺口，
    会让「判断位」与「缺材料」两件事混成一件，缺口表从此不可信。
    """
    out = []

    # 正文＝头部 + 除「口径与未取到」「来源」之外的各节
    body_lines = list(head)
    for name, _hline, body in sections:
        if name in (GAP_SECTION, SOURCE_SECTION):
            continue
        body_lines.extend(body)

    # 甲、乙：红线
    for lineno, s in body_lines:
        if not s.strip():
            continue
        hit = next((w for w in JUDGE_BAN if w in s), None)
        if hit:
            out.append(("EQ-LINE", lineno,
                        "自下判断红线词「%s」：%s" % (hit, s.strip()[:44])))
        if "未分配利润" in s:
            cash = next((w for w in CASH_REWRITE if w in s), None)
            if cash:
                out.append(("EQ-LINE", lineno,
                            "把「未分配利润」改写成「%s」（账面余额不等于可派现金）：%s"
                            % (cash, s.strip()[:44])))

    # 丙：缺口两向对账
    body_gaps, gap_named = [], []
    for lineno, s in body_lines:
        if not s.strip() or "[待人工]" in s:
            continue                           # 判断位不是缺口
        for m in GAP_MARK.finditer(s):
            body_gaps.append((lineno, m.group(1)))
    for name, _hline, body in sections:
        if name != GAP_SECTION:
            continue
        for lineno, s in body:
            if not s.strip():
                continue
            for m in GAP_MARK.finditer(s):
                gap_named.append((lineno, m.group(1)))

    named = {n for _l, n in gap_named}
    in_body = {n for _l, n in body_gaps}
    for lineno, n in body_gaps:
        if n == "无":
            continue                           # 「未取到：无」＝该处无缺口，不在口径节点名
        if n not in named:
            out.append(("EQ-LINE", lineno,
                        "正文点名缺口「%s」，但「%s」节没有点名它（缺口只对了一向）"
                        % (n, GAP_SECTION)))
    for lineno, n in gap_named:
        if n == "无":
            continue
        if n not in in_body:
            out.append(("EQ-LINE", lineno,
                        "「%s」节点名缺口「%s」，但正文没有 `未取到：%s` 这一行（缺口只对了一向）"
                        % (GAP_SECTION, n, n)))
    real = {n for n in (in_body | named) if n != "无"}
    if not real and "无" not in named:
        out.append(("EQ-LINE", 1,
                    "零缺口时「%s」节须写 `未取到：无`，现两处都没有缺口点名" % GAP_SECTION))
    return out


CHECKS = (
    ("EQ-STRUCT", check_struct),
    ("EQ-QUOTE", check_quote),
    ("EQ-FOOT", check_foot),
    ("EQ-LINK", check_link),
    ("EQ-LINE", check_line),
)


# ---------------------------------------------------------------- 道具

def _section_of(heading):
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


def _amount_of(text):
    """→ (数, 单位) 或 None。

    取第一个金额；千分位去掉后按 float 比。没有数、或数的单位与行内声明不一致，
    一律返回 None 让调用方记未取到——**不猜**。单位缺失也返回 None：
    缺单位时「112.00」可能是元也可能是亿元，替它假定一个就是凭空定口径。
    """
    m = AMOUNT.search(text)
    if not m:
        return None
    unit = m.group("unit") or ""
    if not unit:
        # 行里若另有「单位：万元」这类声明，就照它；没有就不猜。
        w = UNIT_WORD.search(text)
        if not w or not w.group("scale"):
            return None
        unit = w.group("scale")
    try:
        return float(m.group("num").replace(",", "")), unit
    except ValueError:
        return None


def _fmt(v):
    """回显用：不留浮点尾巴，也不把 12.0 写成 12.00 之外的样子。"""
    return ("%.2f" % v).rstrip("0").rstrip(".") if v != int(v) else "%d" % int(v)


# 道四的项目名映射：左边是稿里的写法（精确匹配行首项目名），右边是内部键。
# 不在表里的项目名一律不认——「差不多的项目」硬配会把不同口径的数当同一个数。
CMP_SECTION_ITEM = {
    "综合收益总额": "综合收益总额",
    "净利润": "净利润",
    "其他综合收益税后净额": "其他综合收益税后净额",
    "本期增减变动合计": "本期增减变动合计",
    "所有者投入和减少资本": "所有者投入和减少资本",
    "利润分配": "利润分配",
}

# 母公司口径的措辞：引文里出现它、且没有任何合并口径字样时，这个数不能顶替合并数。
PARENT_ONLY = re.compile(r"归属于母公司|母公司所有者")
CONSOLIDATED = re.compile(r"合并")


def _is_parent_only(quote):
    """这一格的引文是不是母公司口径。合并口径的措辞里有「合并」二字，据此排除。"""
    return bool(PARENT_ONLY.search(quote)) and not CONSOLIDATED.search(quote)


def _link_cell(s, lineno):
    """→ (项目名, 数, 单位, 引文, 行号)；认不出项目名或取不到数时前三项为 None。

    项目名＝`- ` 之后到〔列/「/空格分隔的数额〕之前那段（去掉 `〔列：…〕` 标记）。
    数额只在**登记值**里取（第一个「」之前），与 EQ-FOOT 同一条边界：
    越过「」去取会把引文里的数当成本件登记的数额。
    """
    line = s.strip()
    if not line.startswith("- "):
        return None, None, None, "", lineno
    line = line[2:]
    # 项目名到此为止：列标记、原句、或像数字开始的地方
    stops = []
    m = COL_TAG.search(line)
    if m:
        stops.append(m.start())
    q = line.find("「")
    if q >= 0:
        stops.append(q)
    num = re.search(r"[-−]?\d", line)
    if num:
        stops.append(num.start())
    if not stops:
        return None, None, None, "", lineno
    item = line[:min(stops)].strip()
    if item not in CMP_SECTION_ITEM:
        return None, None, None, "", lineno

    tail = line[min(stops):]
    cut = tail.find("「")
    quote = QUOTE.search(tail)
    amount = _amount_of(tail if cut < 0 else tail[:cut])
    if amount is None:
        return item, None, None, quote.group(1) if quote else "", lineno
    return item, amount[0], amount[1], quote.group(1) if quote else "", lineno


def _overview_total(sections):
    """「权益变动总览」里「本期增减变动〔列：合计〕」那一格 → (数, 单位, 行号) 或 None。

    找不到就是 None（不判），不拿别的格替代——本题只有这一格是「总览口径的本期增减」。
    """
    for name, _hline, body in sections:
        if name != SECTIONS[0]:                 # 「权益变动总览」
            continue
        for lineno, s in body:
            if not s.strip() or not _is_finding_line(s):
                continue
            m = COL_TAG.search(s)
            if not m:
                continue
            if s.strip()[2:m.start()].strip() != MOVE_ITEM:
                continue
            if m.group(1).strip() != TOTAL_COL:
                continue
            tail = s[m.end():]
            cut = tail.find("「")
            amount = _amount_of(tail if cut < 0 else tail[:cut])
            if amount is None:
                return None
            return amount[0], amount[1], lineno
    return None

    """把一份稿子跑一遍 main()，返回它印出的全文（自测的文本级断言用）。

    走 main() 而不是 check_text()：读数那行是在 report() 里印的，
    只调 check_text 看不到它。临时文件用完即删。
    """
    tmp = None
    buf = io.StringIO()
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8",
                                         delete=False) as fh:
            fh.write(text)
            tmp = fh.name
        with contextlib.redirect_stdout(buf):
            main([tmp])
    finally:
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass
    return buf.getvalue()


def _run_text(text):
    """把一份稿子跑一遍 main()，原样返回它印出来的全部文本（自测的文本级断言用）。

    走 main() 而不是直接调 _report_text()：这样验的就是用户跑脚本时看到的那段字节，
    包括 exit 分支、包括所有 print。临时文件用完即删。
    """
    tmp = None
    buf = io.StringIO()
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8",
                                         delete=False) as fh:
            fh.write(text)
            tmp = fh.name
        with contextlib.redirect_stdout(buf):
            main([tmp])
    finally:
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass
    return buf.getvalue()


def _line_of(sections, item, col):
    """找回 (项目名, 列名) 那一行的行号，供发条定位；找不到退回 1（不猜别的行）。"""
    for name, _hline, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            m = COL_TAG.search(s)
            if not m:
                continue
            if s.strip()[2:m.start()].strip() == item and m.group(1).strip() == col:
                return lineno
    return 1


def check_text(text):
    """→ (findings[(code, line, msg)], unjudged[(code, why)])。

    空壳抛 NotImplementedError 一律计入 unjudged，**不计入「零发条」**、也不裸抛；
    不在 UNIMPLEMENTED 里的码抛未落字则按「声明与实装不符」直接发条——
    那是真缺陷（说自己落字了、实际是空壳），不能计不可判了事。
    """
    head, sections, stray = split_doc(text)
    findings, unjudged = [], []
    for _k in _FOOT:                       # 每次判都从零起算，别把上一次的读数带过来
        _FOOT[_k] = 0
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
    # EQ-FOOT 的现场读数：判了几项必须露出来。判 0 项与判 12 项全平若印成同一行，
    # 读者会把「一行都没查」读成「这表平了」——所以这一行不能省，判 0 项时尤其不能省。
    # 只在该道已落字时印：还是空壳时印「已判 0 项」会被读成「查了、没问题」。
    if "EQ-FOOT" not in UNIMPLEMENTED:
        checked = _FOOT["col"] + _FOOT["row"]
        skipped = _FOOT["cell_skipped"] + _FOOT["group_skipped"]
        # 过半句只说「比过的那些平不平」，不说整表平不平——只查了 1 项时
        # 「整表已验」会是假话，而这句话正是读者最容易顺手带走的那句。
        verdict = ("整表零校验，这不等于合规" if checked == 0
                   else "只对这 %d 项负责，其余未判项不在本道结论里" % checked)
        lines.append("EQ-FOOT 已判：列内 %d 项、行内 %d 项；未判（认不出表形或数不齐）%d 项——%s"
                     % (_FOOT["col"], _FOOT["row"], skipped, verdict))
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


DEMO = r"""# 示例材料（600000.SH）所有者权益变动表登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议
主体：示例材料（600000.SH）
报告期：2025 年年度报告·合并所有者权益变动表

## 权益变动总览

- 期初余额〔列：实收资本〕30.00 亿元「本集团本年期初实收资本为人民币 30.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 期初余额〔列：资本公积〕20.00 亿元「本集团本年期初资本公积为人民币 20.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 期初余额〔列：未分配利润〕50.00 亿元「本集团本年期初未分配利润为人民币 50.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 期初余额〔列：合计〕100.00 亿元「本集团本年期初所有者权益合计人民币 100.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 本期增减变动〔列：实收资本〕3.00 亿元「本期实收资本增加人民币 3.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 本期增减变动〔列：资本公积〕0.00 亿元「本期资本公积无增减变动」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 本期增减变动〔列：未分配利润〕9.00 亿元「本期未分配利润增加人民币 9.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 本期增减变动〔列：合计〕12.00 亿元「本期所有者权益增减变动合计人民币 12.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 期末余额〔列：实收资本〕33.00 亿元「本年年末实收资本为人民币 33.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 期末余额〔列：资本公积〕20.00 亿元「本年年末资本公积为人民币 20.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 期末余额〔列：未分配利润〕59.00 亿元「本年年末未分配利润为人民币 59.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 期末余额〔列：合计〕112.00 亿元「本集团本年年末所有者权益合计人民币 112.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]

## 本期增减变动

- 综合收益总额 10.00 亿元「本期综合收益总额人民币 10.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 所有者投入和减少资本 3.00 亿元「本期所有者投入和减少资本合计人民币 3.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 利润分配 1.00 亿元「本期利润分配合计人民币 1.00 亿元，为对所有者（或股东）的分配」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 本期增减变动合计 12.00 亿元「以上各项合计使所有者权益增加人民币 12.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]

## 利润分配与所有者投入

- 提取盈余公积 1.00 亿元「本期提取法定盈余公积人民币 1.00 亿元，为未分配利润与盈余公积之间的内部结转」〔锚：2025 年年报·第 181 页·合并所有者权益变动表〕[S1]
- 对所有者的分配 1.00 亿元「本期对所有者（或股东）的分配人民币 1.00 亿元」〔锚：2025 年年报·第 181 页·合并所有者权益变动表〕[S1]
- 所有者投入资本 3.00 亿元「本期所有者投入资本人民币 3.00 亿元」〔锚：2025 年年报·第 181 页·合并所有者权益变动表〕[S1]

## 期末余额与勾稽

- 期末余额 112.00 亿元「期末所有者权益合计人民币 112.00 亿元，等于期初余额 100.00 亿元加本期增减变动 12.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 其他综合收益税后净额 2.00 亿元「本期其他综合收益税后净额人民币 2.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 净利润 8.00 亿元「本期合并净利润人民币 8.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]

## 归属于母公司与少数股东

- 归属于母公司所有者权益 105.00 亿元「归属于母公司所有者权益合计人民币 105.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 少数股东权益 7.00 亿元「少数股东权益合计人民币 7.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]
- 两项合计 112.00 亿元「母公司所有者权益与少数股东权益合计人民币 112.00 亿元」〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]

## 口径与未取到

- 未取到：无
- 口径：七个节一律照抄合并所有者权益变动表原文；本件不做轧账、不把未分配利润改写成可分现金、不评价利润分配方案是否合理。

## 来源

- [S1] 示例材料 2025 年年度报告 | https://example.invalid/600000_2025_annual.pdf | 检索日 2026-03-20
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
# 道一（a）头部少一件自标。
BAD_MARK = _must_replace(DEMO, " ｜ 不构成投资建议", "", 1)
# 道一（b）节标题写成认不出的样子：该节进不了 sections（算缺节），标题本身也进 stray。
BAD_HEADING = _must_replace(DEMO, "## 期末余额与勾稽\n", "## 期末余额与勾稽表\n", 1)
# 道二（a）摘掉整段「」+〔锚〕、只留收尾 [S1]（原句与锚都没了，行形制仍合规）。
NO_TRIPLE = _must_replace(
    DEMO,
    "「本集团本年年末所有者权益合计人民币 112.00 亿元」"
    "〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕",
    "", 1)
# 道二（b）来源行检索日写成斜杠式：该行不合格式，S1 不再算登记。
BAD_SOURCE_FMT = _must_replace(
    DEMO,
    "https://example.invalid/600000_2025_annual.pdf | 检索日 2026-03-20",
    "https://example.invalid/600000_2025_annual.pdf | 检索日 2026/03/20", 1)
# 道二（c）正文引 [S9]，来源节只有 S1（顺带让 S1 成为「登记了没人引」，
# 但那一条只在 registered 非空时判——这里 S1 合规、S9 未登记，两条都会发，
# 所以坏样要**只**红这个方向：把 S1 换成 S9 而不是新增一行。
BAD_REF = _must_replace(
    DEMO,
    "〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]",
    "〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S9]", 1)

# 道三（a）列内破：未分配利润的期末 59.00 改成 61.00（50＋9 应 59）。
# 注意：好样是一张**闭合**的表，一格错必然同时踩到「列内」与「行内」两条断言
# （期末合计 112 也跟着不等于 33＋61＋20）。这不是判据串味，是表本身两处都不平；
# 两档夹具的区别在**注入点不同**（这一档动未分配利润格，下一档动合计格），
# 断言的是码集恰为 {EQ-FOOT}——第二道码一个都不许跟着红。
BAD_FOOT_COL = _must_replace(
    DEMO, "- 期末余额〔列：未分配利润〕59.00 亿元",
    "- 期末余额〔列：未分配利润〕61.00 亿元", 1)
# 道三（b）行内破：期初余额的合计 100.00 改成 103.00（30＋20＋50 应 100）。
BAD_FOOT_ROW = _must_replace(
    DEMO, "- 期初余额〔列：合计〕100.00 亿元",
    "- 期初余额〔列：合计〕103.00 亿元", 1)
# 道三（c）反证：整格删掉「本期增减变动〔列：资本公积〕」——参与运算的数缺一个。
# 缺数时该列不判、该行也不判，**不得**拿 0 补位（补 0 就是凭空造数）：期望零发条。
OK_FOOT_GAP = _must_replace(
    DEMO,
    "- 本期增减变动〔列：资本公积〕0.00 亿元"
    "「本期资本公积无增减变动」"
    "〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]\n",
    "", 1)
# 读数档：把所有 〔列：X〕 标签摘干净。EQ-FOOT 一格都认不出 ⇒ 它一项都没判，
# 这时必须发「未判任何一项」，**不许**印成和好样一样的零发条——
# 零发条意思是「查过了、没问题」，而这里根本没查。真年报表格贴成纯文本时就是这个样子。
NO_COL_TAG = re.sub(r"〔\s*列\s*[:：][^〕]*〕", "", DEMO)
if NO_COL_TAG == DEMO:
    raise AssertionError("读数档注入未落地：摘掉列标签后字节未变")

# 道四（a）断言1破：综合收益总额 10.00 改 11.00（净利润 8 ＋ 其他综合收益 2 应 10）。
# 顺带会破断言2（本节合计 12 ＝ 11＋3－1 也差 1），但两处都是 EQ-LINK，
# 断言的是**码集**恰为 {EQ-LINK}——另两道码一个都不许跟着红。
BAD_LINK_1 = _must_replace(DEMO, "- 综合收益总额 10.00 亿元", "- 综合收益总额 11.00 亿元", 1)

# 道四（b）断言2破：本节「本期增减变动合计」12.00 改 13.00
# （综收 10 ＋ 投入 3 － 分配 1 应 12）。同时破断言3（两处合计不再一致），同样都是 EQ-LINK。
BAD_LINK_2 = _must_replace(
    DEMO, "- 本期增减变动合计 12.00 亿元", "- 本期增减变动合计 13.00 亿元", 1)

# 道四（c）断言3破：**只动「权益变动总览」那张表**，本节合计原封不动。
# 这里必须动四格而不是一格：总览表是闭合的（期末 112 － 期初 100 锁死了增减合计 12），
# 单独改合计恒等于同时破 EQ-FOOT 的列内。所以把未分配利润这一列的数和两个合计
# **自洽地**一起挪（期初 50→49、增减 9→10，期末 59 不变；两处合计随之 100→99、12→13），
# 使总览表自身仍然轧平、只有「与本节合计不一致」这一条成立。
_BAD_LINK_3 = DEMO
for _old, _new in (
        ("- 期初余额〔列：未分配利润〕50.00 亿元", "- 期初余额〔列：未分配利润〕49.00 亿元"),
        ("- 期初余额〔列：合计〕100.00 亿元", "- 期初余额〔列：合计〕99.00 亿元"),
        ("- 本期增减变动〔列：未分配利润〕9.00 亿元", "- 本期增减变动〔列：未分配利润〕10.00 亿元"),
        ("- 本期增减变动〔列：合计〕12.00 亿元", "- 本期增减变动〔列：合计〕13.00 亿元"),
):
    _BAD_LINK_3 = _must_replace(_BAD_LINK_3, _old, _new, 1)
BAD_LINK_3 = _BAD_LINK_3

# 道四（d）断言3的**更严一档**：总览表自身完全轧平（各列之和、列内纵向都成立），
# 唯一不成立的是「与本节合计不一致」。上一档挪了 4 格，会不会是靠 EQ-FOOT 顺带逮住的
# 说不清；这一档把未分配利润列的期初／增减／期末与两个合计**单调同步**地各挪 1，
# 使总览表在自己的账上无懈可击，只有跨节那一条成立 ⇒ 期望码集恰为 {EQ-LINK}。
_BAD_LINK_4 = DEMO
for _old, _new in (
        ("- 本期增减变动〔列：未分配利润〕9.00 亿元", "- 本期增减变动〔列：未分配利润〕8.00 亿元"),
        ("- 本期增减变动〔列：合计〕12.00 亿元", "- 本期增减变动〔列：合计〕11.00 亿元"),
        ("- 期末余额〔列：未分配利润〕59.00 亿元", "- 期末余额〔列：未分配利润〕58.00 亿元"),
        ("- 期末余额〔列：合计〕112.00 亿元", "- 期末余额〔列：合计〕111.00 亿元"),
):
    _BAD_LINK_4 = _must_replace(_BAD_LINK_4, _old, _new, 1)
BAD_LINK_4 = _BAD_LINK_4

# 道四反证一：删掉「其他综合收益税后净额」整行 ⇒ 断言1 三数不齐，不判。
# 只删这一行、不动任何数，免得顺手把断言2／3 也弄红。
OK_LINK_NO_OCI = _must_replace(
    DEMO,
    "- 其他综合收益税后净额 2.00 亿元"
    "「本期其他综合收益税后净额人民币 2.00 亿元」"
    "〔锚：2025 年年报·第 180 页·合并所有者权益变动表〕[S1]\n",
    "", 1)
# 道四反证二：净利润的引文改成**只有**母公司口径 ⇒ 不许顶替合并数，断言1 不判。
# 数一个都不动：这一档钉的是「口径认不认」，不是「算术对不对」。
OK_LINK_PARENT_ONLY = _must_replace(
    DEMO,
    "「本期合并净利润人民币 8.00 亿元」",
    "「本期归属于母公司所有者的净利润人民币 8.00 亿元」", 1)


# ── 道五 EQ-LINE 的坏样与反证 ────────────────────────────────────────────────
# 五道全落字之后，覆盖自证会逐道查「已落字的码有没有反例钉住」。EQ-LINE 落字时
# 只落了判据、没补反例档，所以覆盖自证当场报「缺反例：EQ-LINE」——这正是它该干的事。
# 下面六档都从 DEMO 派生，一处只坏一件事，免得逐档比对分不清是谁发的。
# （此块曾出现过两组同名定义并存：后定义静默遮蔽前定义，前一组成了永远跑不到的死代码。
#  合并时只保留一组，名字与 cases 里的引用一一对上。）

# 甲、自下判断红线：在内容节里加一句替读者下结论的话。
BAD_LINE_JUDGE = _must_replace(
    DEMO,
    "- 综合收益总额 10.00 亿元",
    "- 公司本期股东回报丰厚，综合收益总额 10.00 亿元", 1)

# 乙、把「未分配利润」改写成可分现金：同一行里两个词都出现即发。
BAD_LINE_CASH = _must_replace(
    DEMO,
    "- 期末余额〔列：未分配利润〕59.00 亿元",
    "- 期末余额〔列：未分配利润〕59.00 亿元，为大额可分现金", 1)

# 丙、缺口单向（正文→口径）：正文点名一个缺口，口径节却仍写「未取到：无」。
BAD_LINE_GAP = _must_replace(
    DEMO,
    "- 净利润 8.00 亿元",
    "- 未取到：商誉减值\n- 净利润 8.00 亿元", 1)

# 丁、缺口反向（口径→正文）：口径节点名一个缺口，正文一个字没写。
# 这一档钉的是「只查一向等于没对账」——丙只证了正文→口径，反向不钉住，
# 判据里那一半以后被删掉，自测照样报零不合。
BAD_LINE_GAP_REVERSE = _must_replace(
    DEMO,
    "- 未取到：无",
    "- 未取到：外币报表折算差额", 1)

# 反证一：口径节按设计要写「不评价股东回报是否丰厚」这类说明，
# 该节整节豁免红线。这一档把红线词**搬进口径节**，期望零发条——
# 证明豁免是真生效，而不是靠「没测到」蒙过去的。
OK_LINE_GAP_EXEMPT = _must_replace(
    DEMO,
    "- 口径：七个节一律照抄合并所有者权益变动表原文；",
    "- 口径：本件不评价股东回报是否丰厚，七个节一律照抄合并所有者权益变动表原文；", 1)

# 反证二：`[待人工]` 行不算缺口 ⇒ 正文写「未取到：… [待人工]」不该发。
# 这条钉的是「判断位 ≠ 缺口」：判断位是本件已交代清楚的位置，缺口是材料没到手。
# 把判断位算进缺口，缺口表从此不可信——所以它必须有反例钉住。
OK_LINE_HUMAN_NOT_GAP = _must_replace(
    DEMO,
    "- 两项合计 112.00 亿元",
    "- 分红方案 未取到：现金分红方案 [待人工]\n"
    "- 两项合计 112.00 亿元", 1)


def selftest():
    """逐档现报：好样须零发条，坏样须恰发该道码；未落字各算一档「不可判」，不并进「不合」。

    档数＝逐档比对的那几档 + UNIMPLEMENTED 的码数（未落字各算一档「不可判」），
    两段都从现场值算，不写死数字。本件五道全落字，好样单稿退 0；若某道回退成空壳，
    这两处会自己从 0 变 3，不用手改。
    """
    cases = (
        ("好样应零发条（五道全落字）", DEMO, frozenset()),
        ("形制：头部删掉「不构成投资建议」", BAD_MARK, frozenset({"EQ-STRUCT"})),
        ("形制：节标题写成认不出的样子（进 stray＋缺节）", BAD_HEADING,
         frozenset({"EQ-STRUCT"})),
        ("原句与锚：摘掉整段「」+〔锚〕，只留 [S1]", NO_TRIPLE, frozenset({"EQ-QUOTE"})),
        ("来源行：检索日写成 2026/03/20", BAD_SOURCE_FMT, frozenset({"EQ-QUOTE"})),
        ("对应：正文引 [S9] 而来源节只有 S1", BAD_REF, frozenset({"EQ-QUOTE"})),
        ("行列轧平：未分配利润期末 59→61（列内破）", BAD_FOOT_COL,
         frozenset({"EQ-FOOT"})),
        ("行列轧平：期初合计 100→103（行内破）", BAD_FOOT_ROW,
         frozenset({"EQ-FOOT"})),
        ("反证：删掉一格「本期增减变动〔列：资本公积〕」（缺数不判）", OK_FOOT_GAP,
         frozenset()),
        ("读数：整稿摘掉列标签（一项都判不了，必须发条明说）", NO_COL_TAG,
         frozenset({"EQ-FOOT"})),
        ("勾稽①：综合收益总额 10→11（≠净利润 8＋其他综合收益 2）", BAD_LINK_1,
         frozenset({"EQ-LINK"})),
        ("勾稽②：本节增减合计 12→13（≠综收 10＋投入 3－分配 1）", BAD_LINK_2,
         frozenset({"EQ-LINK"})),
        ("勾稽③：只挪总览表合计（表自身仍平，仅与本节合计不符）", BAD_LINK_3,
         frozenset({"EQ-LINK"})),
        ("勾稽③b：总览表自洽同步挪 1（表无懈可击，只跨节那一条成立）", BAD_LINK_4,
         frozenset({"EQ-LINK"})),
        ("反证：删掉「其他综合收益税后净额」整行（三数不齐不判）", OK_LINK_NO_OCI,
         frozenset()),
        ("反证：净利润只有母公司口径（不许顶替合并数）", OK_LINK_PARENT_ONLY,
         frozenset()),
        ("红线：内容节里自下判断「股东回报丰厚」", BAD_LINE_JUDGE,
         frozenset({"EQ-LINE"})),
        ("改写：把「未分配利润」说成「可分现金」", BAD_LINE_CASH,
         frozenset({"EQ-LINE"})),
        ("缺口单向：正文点名未取到，口径节仍写「未取到：无」", BAD_LINE_GAP,
         frozenset({"EQ-LINE"})),
        ("缺口反向：口径节点名未取到，正文一个字没写", BAD_LINE_GAP_REVERSE,
         frozenset({"EQ-LINE"})),
        ("反证：红线词写进「口径与未取到」节（该节整节豁免）", OK_LINE_GAP_EXEMPT,
         frozenset()),
        ("反证：[待人工] 行不算缺口（判断位 ≠ 缺材料）", OK_LINE_HUMAN_NOT_GAP,
         frozenset()),
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

    # 读数自证：EQ-FOOT 必须报出「判了几项」，且判 0 项时不许和好样印成同一行。
    # 逐档比对只看码集，查不出这一层——判 0 项与判 12 项全平都是零发条（或都带别的码），
    # 码集一样。这条专门钉住「读不到当成 0」那个老病。
    read_bad = []
    if "EQ-FOOT" not in UNIMPLEMENTED:
        good = _run_text(DEMO)
        nocol = _run_text(NO_COL_TAG)
        m_good = re.search(r"EQ-FOOT 已判：列内 (\d+) 项、行内 (\d+) 项", good)
        if not m_good:
            read_bad.append("好样输出里没有「EQ-FOOT 已判：…」这一行")
        elif int(m_good.group(1)) + int(m_good.group(2)) == 0:
            read_bad.append("好样已判项数为 0：好样明明有可轧平的格子，判 0 项说明表形没认出来")
        if "未判任何一项" not in nocol:
            read_bad.append("摘掉列标签后输出里没有「未判任何一项」：判 0 项被印成了零发条")
        if "不平" in nocol:
            read_bad.append("摘掉列标签后发了「不平」：认不出表形时不许发不平")
        if good == nocol:
            read_bad.append("好样与摘标签稿输出逐字节相同：判了几项没有露出来")
    if read_bad:
        bad += 1
        print("不合 读数自证：%s" % "；".join(read_bad))
    elif "EQ-FOOT" in UNIMPLEMENTED:
        print("过   读数自证（EQ-FOOT 仍未落字，无需报项数）")
    else:
        print("过   读数自证（好样报出非 0 已判项数；摘标签稿发「未判任何一项」且不发不平；两稿输出不同）")

    # 覆盖自证：每道已落字的码，在 cases 里至少有一档期望恰含它。
    # 这条防的是「实现了一道判据、同时少了一档反例，净增反例 0 档」——
    # 判据接进 CHECKS 却没有反例钉住，它以后被改坏，自测照样报 不合=0。
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
    ap = argparse.ArgumentParser(description="所有者权益变动表登记稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="所有者权益变动表登记稿 .md 路径")
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
        print("缺入参：给一份所有者权益变动表登记稿路径，或用 --demo / --selftest", file=sys.stderr)
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
