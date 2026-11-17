#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_other_equity_instruments.py — 其他权益工具判断稿五道机检（零网络、零外发、不读环境变量）

**五道判据全部落字**：节常量、码常量、形制道具、`--demo`、`--selftest`
与读入/退码形制之外，五道函数体都已实装（形制／原句与锚／条款只认原句／分类只认原句／红线；
缺口两向点名并入道五）；`_not_judged` 保留为兜底——只给「声明已落字却仍抛未落字」用，
由调用方按不合计处理，不会被读成「不可判」而放行。`UNIMPLEMENTED = ()`，正常读数不可判=0、好样单稿退 0。

用法：
    python3 scripts/check_other_equity_instruments.py <其他权益工具稿>.md
    python3 scripts/check_other_equity_instruments.py --selftest
    python3 scripts/check_other_equity_instruments.py --demo     打印一份完整合规样例（零输入可跑）

七节（按序，`## ` 起节）：
    其他权益工具概况／永续债条款／优先股条款／利息与股利处理／会计分类依据
    ／口径与未取到／来源

五道码（五道均已落字，下面写的是**这道判什么**；判据与实现不符时按不合计处理，不放行）：

道一 OEI-STRUCT 形制（已落字）
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]；
  `主体：` 行、`报告期：` 行在场且非空；七节齐且按序；前五节各至少一条 `- ` 发现行；
  「口径与未取到」与「来源」两节不得为空；认不出的节标题与多出的同名节逐条发。

道二 OEI-QUOTE 原句与锚（已落字）
  每条发现行以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；缺哪件点名哪件；
  例外只有三形：「未取到：」行、[待人工] 行与〔自算〕行；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址；
  发现行收尾的 [S#] 必须在来源节有对应登记行；来源节一条合规来源行都没有则单独发一条。

道三 OEI-TERMS 永续债／优先股条款只认原句（已落字）
  票面利率／股息率、利率重置与跳升幅度、付息日与递延权利、赎回权与赎回价、
  清偿顺序与转股安排，都只能照抄募集说明书或附注原文；只判「永续债条款」「优先股条款」两节：
  登记值不得为空；登记值里的每个数须在同行「」原句出现；
  登记值含递延／跳升／赎回／清偿顺序／转股／重置六词之一时，同行原句须有同词（不扩表）。

道四 OEI-CLASS 会计分类依据只认原句（已落字）
  权益工具／金融负债的最终分类及理由（不可避免的交付现金义务、可回售条款、自主决定权），
  只能照抄附注原文；只判「会计分类依据」节：登记的分类结论词须在同行原句里逐个找到；
  登记值里的推理链词（因为／故／因此／属于…）与准则编号引用，原句没有即发——
  分类是发行方按合同条款作的判断，本件不得自己接因果链或搬条文。

道五 OEI-LINE 红线（已落字）
  永续债利息与优先股股息不得与债务利息费用轧成净额／轧差／冲减／抵扣／抵销／互抵；
  递延支付不得记成费用（递延与计入费用／确认为费用／转回损益同现即发），
  登记值写「递延」而原句没有也发；只判「利息与股利处理」节的**登记值**，不判引文；
  缺口两向点名：①缺口节点了名的项，正文不得有它的全三元组登记行；
  ②正文「未取到：X」须在缺口节点名；③缺口节点名了而正文没有对应也发；
  零缺口须显式写 `未取到：无`（不触发丙）。

退码：0 全过 / 1 有发条 / 2 用法错（缺参数或未知参数）
      / 3 读不到文件或空稿，或零发条但有未实装判据（`UNIMPLEMENTED` 非空时）。
      五道全落字后 `UNIMPLEMENTED = ()`，好样单稿退 0、不可判=0；若将来某道退回空壳，
      置回清单即自动回到退 3、并重新打印「这不等于合规」。
"""

import argparse
import io
import os
import re
import sys
import tempfile
import contextlib

SLUG = "cue-cn-other-equity-instruments-cn"

CODES = ("OEI-STRUCT", "OEI-QUOTE", "OEI-TERMS", "OEI-CLASS", "OEI-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("其他权益工具概况", "永续债条款", "优先股条款", "利息与股利处理",
            "会计分类依据", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"

# 五道已全部落字，此处留空。码抛未落字时才计「不可判」——
# 且只限列表里的码：声明已落字的判据再抛未落字，即声明与实装不符，按不合计处理，不装成「不可判」。
UNIMPLEMENTED = ()

HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")
SUBJECT = re.compile(r"^主体：\s*(\S.*)$")
PERIOD = re.compile(r"^报告期：\s*(\S.*)$")

TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
ANCHOR_REF = re.compile(r"\[(S\d+)\]")
ANCHOR_BLOCK = re.compile(r"〔\s*锚\s*[:：][^〕]*〕")
REF_TAIL = re.compile(r"\[(S\d+)\]\s*$")

# 道三只判「永续债条款」「优先股条款」两节，且只判这六个条款词（不扩表：其余词形太多，扩了造假红）。
TERM_SECTIONS = ("永续债条款", "优先股条款")
TERM_WORDS = ("递延", "跳升", "赎回", "清偿顺序", "转股", "重置")

# 道四只判「会计分类依据」节，且只判这三组：分类结论词、推理链词、准则编号引用。
CLASS_SECTION = "会计分类依据"
CLASS_TERMS = ("权益工具", "金融负债", "复合金融工具")
# 推理链词：本件自己接因果链时用的连接词。宁可组小一点——目的不是抓所有连接词，
# 是抓「本件替发行人下结论」。DEMO 三行登记值里一个都不含，好样不会误红。
REASON_WORDS = ("因为", "由于", "因此", "故", "所以", "据此",
                "表明", "说明", "意味着", "符合", "满足", "属于")
# 准则编号引用：「第 N 号」，且同处 12 字内要有「准则」或「CAS」；纯页码「第 12 页」不算。
CAS_NO = re.compile(r"第\s*(\d+)\s*号")
CAS_NEAR = re.compile(r"准则|CAS|cas")

# 道五只判「利息与股利处理」节的登记值（不判引文），外加缺口两向对账。
LINE_SECTION = "利息与股利处理"
# 合并／互抵词：本件自己把永续债利息、优先股股息与债务利息费用对冲时用的词。
NET_WORDS = ("净额", "轧差", "轧账", "冲减", "抵扣", "抵销", "互抵", "净影响")
# 费用化词：与「递延」同现在登记值里，就是把未付的递延利息转成了费用。
FEE_WORDS = ("计入费用", "确认为费用", "转回损益", "计入当期费用")
GAP_ITEM = re.compile(r"^-\s*未取到\s*[:：]\s*(?P<item>.+)$")

# 登记值里的数：整数、千分位、小数；百分号与单位不算进数里（引文里常写成「3.85%」或「3.85 %」）。
NUMBER = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?")

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
    """道一 OEI-STRUCT 形制：头部四件自标与两行、七节齐且按序、节内是否有发现行。

    只判「形」：节名在不在、顺序对不对、内容节里有没有发现行、两节尾部有没有内容。
    判断内容对不对是另四道的事——这里不越界，否则一支注入会同时红两道、分不清归属。
    """
    out = []
    htext = "\n".join(s for _i, s in head)
    for mark in MARK_TEXTS:
        if mark not in htext:
            out.append(("OEI-STRUCT", 1, "头部缺自标「%s」" % mark))
    if not any(SUBJECT.match(s.strip()) for _i, s in head):
        out.append(("OEI-STRUCT", 1, "头部缺 `主体：` 行"))
    if not any(PERIOD.match(s.strip()) for _i, s in head):
        out.append(("OEI-STRUCT", 1, "头部缺 `报告期：` 行"))

    # 丙：野节（认不出的节名／多出的同名节）逐条报，行号用 stray 给的
    for lineno, raw in stray:
        out.append(("OEI-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw))

    # 丁：七节须齐且按序
    names = [n for n, _l, _b in sections]
    missing = [n for n in SECTIONS if n not in names]
    if missing:
        out.append(("OEI-STRUCT", 1, "缺节：%s" % "／".join(missing)))
    elif names != list(SECTIONS):
        out.append(("OEI-STRUCT", 1, "节序不对：现序 %s，应序 %s"
                    % ("／".join(names), "／".join(SECTIONS))))

    # 戊：五个内容节各至少一条发现行；己：两节尾部不得为空
    for name, hline, body in sections:
        if name in CONTENT_SECTIONS:
            if not any(_is_finding_line(s) for _i, s in body):
                out.append(("OEI-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name))
        elif name in (GAP_SECTION, SOURCE_SECTION):
            if not any(s.strip() for _i, s in body):
                out.append(("OEI-STRUCT", hline, "节「%s」为空" % name))
    return out


def check_quote(head, sections, stray):
    """道二 OEI-QUOTE 原句与锚：来源行格式、发现行三元组、[S#] 两向对应。

    例外只有三形：「未取到：」行、[待人工] 行、〔自算〕行——前两者是缺口与判断位，
    后者已经必须交代算法与口径，要求它再挂原句等于把自算伪装成披露值。
    空来源节／没有来源节不在这里报（那是道一的事），这里只判格式与对应，不许崩。
    """
    out = []
    registered, reported_missing = set(), set()

    # 甲：来源行格式，只扫来源节；不合规的行照样报，但不进 registered。
    # 非 `- ` 行也报：道一只管来源节空不空，行形制若不在这里收，就会两头都没人管。
    for name, _hline, body in sections:
        if name != SOURCE_SECTION:
            continue
        for lineno, s in body:
            if not s.strip():
                continue
            if not _is_finding_line(s):
                out.append(("OEI-QUOTE", lineno,
                            "来源节只许 `- [S#] 标题 | URL | 检索日` 行：%s" % s.strip()[:44]))
                continue
            m = SOURCE_LINE.match(s.strip())
            if not m:
                out.append(("OEI-QUOTE", lineno,
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
            if _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s:
                continue                     # 缺口登记与人工位、自算行本来就不挂三元组
            if not TRIPLE.search(s):
                miss = []
                if not QUOTE.search(s):
                    miss.append("「」原句")
                if not ANCHOR_BLOCK.search(s):
                    miss.append("〔锚：…〕")
                if not ANCHOR_REF.search(s):
                    miss.append("[S#]")
                out.append(("OEI-QUOTE", lineno,
                            "发现行缺 %s（三元组须在行末）"
                            % "、".join(miss or ["「」原句 + 〔锚〕 + [S#] 的次序"])))
                continue
            m = REF_TAIL.search(s.strip())
            if not m:
                out.append(("OEI-QUOTE", lineno,
                            "发现行未以 [S#] 收尾（三元组须在行末）"))
                continue
            # 没有来源节、或来源节里一条合规行都没有时，同一个根因会在每一行重复铺开，
            # 把「哪一行真有问题」淹掉：根因由道一（缺节）或本道丙（零合规来源行）点一次，
            # 这里只在来源节确有登记行时，才逐行判「引用的是不是登记过的 S 号」。
            if not has_source or not registered:
                continue
            ref = m.group(1)
            if ref in registered or ref in reported_missing:
                continue                     # 同一个未登记 S 号只报一次，行号取首次引用处
            reported_missing.add(ref)
            out.append(("OEI-QUOTE", lineno,
                        "引用了未登记的 [%s]：来源节没有该 S 号的合规来源行" % ref))

    # 丙：来源节存在但一条合规来源行都没有——只在节在场时报，缺节归道一
    if has_source and not registered:
        out.append(("OEI-QUOTE", 1,
                    "来源节没有一条合规来源行：每个 [S#] 都要有可点 http(s) URL 与检索日"))
    return out


def check_terms(head, sections, stray):
    """道三 OEI-TERMS 永续债／优先股条款只认原句：条款是文件写定的，不是本件能推的。

    只扫「永续债条款」「优先股条款」两节。
    甲 条款项只有项名没有登记值（登记值为空）→ 发：空值无从回溯。
    乙 登记值里的每个数都必须在同行「」原句里出现→ 找不到即发：数是对出来的，不是推出来的。
    丙 登记值里出现 TERM_WORDS 六词之一，同行原句须有同词→ 缺即发：
       挡「可无限次递延」对「有权推延支付」这类改写。**只判这六词，不扩表**——
       其余条款词形式太多（赎回价／赎回权、面值／票面），扩了会造一堆假红。
    「未取到：」与 [待人工]、〔自算〕行不归这道：缺口与判断位不是条款登记。
    """
    out = []
    for name, _hline, body in sections:
        if name not in TERM_SECTIONS:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue
            if _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s:
                continue
            reg = _registered_value(s)
            if not reg:
                out.append(("OEI-TERMS", lineno, "条款项只有项名没有登记值"))
                continue
            quote_text = "".join(QUOTE.findall(s))
            reported = set()
            for num in _numbers_in(reg):
                if num in reported or not _num_missing(num, quote_text):
                    continue
                reported.add(num)
                out.append(("OEI-TERMS", lineno,
                            "登记值里的数「%s」在同行原句里找不到" % num))
            for w in TERM_WORDS:
                if w in reg and w not in quote_text:
                    out.append(("OEI-TERMS", lineno,
                                "登记值写「%s」，同行原句里没有该条款词" % w))
    return out


def check_class(head, sections, stray):
    """道四 OEI-CLASS 会计分类依据只认原句：分类是发行方按合同条款作的判断。

    本件只能照抄「发行方说它归哪一类、据此说了什么理由」，不能自己拿准则条文去归。
    只扫「会计分类依据」节。
    甲 登记值里出现分类结论词（CLASS_TERMS）之一，同行原句须有**同一个词**——逐个判，
       不拿包含关系糊：原句只说「权益工具」而登记写「权益工具／金融负债复合」，后者照样发。
    乙 登记值里出现推理链词（REASON_WORDS）之一，同行原句须有同词——缺即发：
       挡本件自己接一根「因为…所以归类为权益工具」的因果链。只在「会计分类依据」节判，
       别的节里「由于」是正常行文。
    丙 登记值给准则编号引用（「第 N 号」前后 12 字内有「准则」或「CAS」），同行原句没有→ 发：
       挡本件搬条文下结论。「第 12 页」这类页码不算编号引用（前面没有准则／CAS）。
    「未取到：」与 [待人工]、〔自算〕行不归这道。
    """
    out = []
    for name, _hline, body in sections:
        if name != CLASS_SECTION:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue
            if _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s:
                continue
            reg = _registered_value(s)
            if not reg:
                continue                     # 空值归道三那样点；这里不重复发
            quote_text = "".join(QUOTE.findall(s))
            for term in CLASS_TERMS:
                if term in reg and term not in quote_text:
                    out.append(("OEI-CLASS", lineno,
                                "登记分类结论「%s」，同行原句里没有该表述" % term))
            for w in REASON_WORDS:
                if w in reg and w not in quote_text:
                    out.append(("OEI-CLASS", lineno,
                                "登记值写「%s」，同行原句里没有该词：分类理由不得由本件接因果链" % w))
            for ref in _cas_refs(reg):
                if ref not in quote_text:
                    out.append(("OEI-CLASS", lineno,
                                "登记值引准则编号「%s」，同行原句里没有该引用" % ref))
    return out


def check_line(head, sections, stray):
    """道五 OEI-LINE 红线：利息股息不轧账、递延不得冲销、缺口两向点名。

    甲 不轧账（只扫「利息与股利处理」）：登记值里出现合并／互抵词（NET_WORDS）之一，
       同行原句没有同词 → 发。只判**登记值**，不判引文——披露原文里写「不涉及所得税抵扣」
       是本件在照抄，不是本件在对冲（好样那行就靠这条不红）。
    乙 递延不得冲销（同节）：登记值写「递延」而原句没有 → 发；
       登记值里「递延」与费用化词（FEE_WORDS）同现 → 发（未付的递延利息不因未付就转成费用）。
    丙 缺口两向点名（「口径与未取到」↔ 全稿）：
       ① 缺口节点了名 X，而正文有一条**已挂全三元组**的 X 登记行 → 发：写了又说不算数。
       ② 正文一条「未取到：X」行的 X 没进缺口节 → 发：缺口未在两向同时登记。
       ③ 缺口节点了名 X，而正文里 X 一次都没出现 → 发：节点名了正文却没有对应。
       **不判「缺三元组」**：那一件事归 OEI-QUOTE，本条判的是缺口台账，
       不抢那条发条（否则同一行会同时红两道，分不清是缺件还是台账漏记）。
    「未取到：无」是显式的零缺口登记，不触发丙。
    """
    out = []
    gap_items = {}
    body_lines = []
    for name, _hline, body in sections:
        if name == GAP_SECTION:
            for lineno, s in body:
                m = GAP_ITEM.match(s.strip())
                if not m:
                    continue
                item = _clean_item(m.group("item"))
                if item and item != "无":
                    gap_items[item] = lineno
            continue
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue
            body_lines.append((lineno, s, name))

    # 甲、乙：只扫「利息与股利处理」的登记值
    for lineno, s, name in body_lines:
        if name != LINE_SECTION:
            continue
        if _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s:
            continue
        reg = _registered_value(s)
        if not reg:
            continue
        quote_text = "".join(QUOTE.findall(s))
        for w in NET_WORDS:
            if w in reg and w not in quote_text:
                out.append(("OEI-LINE", lineno,
                            "登记值写「%s」：利息与股息不得与费用轧账互抵" % w))
                break
        if "递延" in reg:
            if "递延" not in quote_text:
                out.append(("OEI-LINE", lineno,
                            "登记值写「递延」，同行原句里没有该表述"))
            for w in FEE_WORDS:
                if w in reg:
                    out.append(("OEI-LINE", lineno,
                                "登记值把递延与「%s」写在一处：递延利息不得转成费用" % w))
                    break

    # 丙①：缺口节点了名，正文却有它的全三元组登记行
    for item in gap_items:
        for lineno, s, _name in body_lines:
            if _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s:
                continue
            if not TRIPLE.search(s):
                continue                     # 缺三元组的行归 OEI-QUOTE
            if _names_item(s, item):
                out.append(("OEI-LINE", lineno,
                            "「%s」节点了「%s」，正文却有它的登记行" % (GAP_SECTION, item)))
                break

    # 丙②：正文的「未取到：X」没有进缺口节
    for lineno, s, _name in body_lines:
        if not _is_gap_line(s):
            continue
        m = re.search(r"未取到\s*[:：]\s*(.+)$", _strip_quotes(s))
        if not m:
            continue
        item = _clean_item(m.group(1))
        if item and item != "无" and item not in gap_items:
            out.append(("OEI-LINE", lineno,
                        "正文「未取到：%s」，「%s」节没有点名" % (item, GAP_SECTION)))

    # 丙③：缺口节点了名，正文里一次都没出现
    for item, gline in gap_items.items():
        if not any(item in s for _l, s, _n in body_lines):
            out.append(("OEI-LINE", gline,
                        "「%s」节点名「%s」，正文里没有对应" % (GAP_SECTION, item)))
    return out


CHECKS = (
    ("OEI-STRUCT", check_struct),
    ("OEI-QUOTE", check_quote),
    ("OEI-TERMS", check_terms),
    ("OEI-CLASS", check_class),
    ("OEI-LINE", check_line),
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

    野节＝不认识的节名，或多出来的同名节。它们**另记**、不吞进上一节。
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


def _registered_value(s):
    """这一行**本件自己登记的**那个值：项名之后、第一个「」之前那段。

    不能拿整行去判：`〔锚：…·发行条款〕` 里带「条款」二字、又带年份与页码，那是锚点地址
    不是断言；项名「利息递延」里的「递延」是**项名**不是登记值。拿整行判两个方向都会假红。
    也必须先截到第一个「」再切项名：锚块里有全角冒号，先按冒号切会把锚文本当成登记值。
    """
    head = re.sub(r"^-\s*", "", s.strip()).split("「", 1)[0].strip()
    if "：" in head:
        return head.split("：", 1)[1].strip()
    parts = head.split(None, 1)
    return (parts[1].strip() if len(parts) > 1 else "")


def _clean_item(s):
    """项名归一：去掉 `- `、空白与收尾标点，好让缺口两向对账真的对得上。"""
    t = s.strip()
    if t.startswith("- "):
        t = t[2:]
    return t.strip().strip("：: 　，,。.;；")


def _line_label(s):
    """→ 发现行的项名（`- ` 之后第一个词，或冒号之前那段），供缺口两向对账用。"""
    body = re.sub(r"^-\s*", "", s.strip())
    head = body.split("「", 1)[0]
    if "：" in head:
        return head.split("：", 1)[0].strip()
    parts = head.split(None, 1)
    return parts[0].strip() if parts else ""


def _names_item(s, item):
    """这一行是不是在登记 `item`：项名与 item 互相包含即算（项名写法常有长有短）。"""
    label = _line_label(s)
    return bool(label) and (item in label or label in item)


def _numbers_in(text):
    """→ 文本里的数（按出现顺序，去重前）。千分位原样保留，好让 `5,000` 与 `5000` 各自比对。"""
    return NUMBER.findall(text)


def _num_missing(num, quote_text):
    """登记值里的数在引文里找不到吗？带边界比对，免得 `5` 被 `15.00` 里的数字蒙混过。

    另试一次去掉千分位的写法：`5,000` 与 `5000` 是同一个数。
    """
    for cand in (num, num.replace(",", "")):
        pat = r"(?<![\d.])" + re.escape(cand) + r"(?![\d])"
        if re.search(pat, quote_text) or re.search(pat, quote_text.replace(",", "")):
            return False
    return True


def _cas_refs(text):
    """→ 文本里的准则编号引用（`第 37 号` 这种），只认「准则／CAS」前后 12 字内出现的。

    纯页码 `第 12 页` 不算：它前面没有「准则」也没有「CAS」，是锚点页不是条文号。
    """
    refs = []
    for m in CAS_NO.finditer(text):
        lo, hi = max(0, m.start() - 12), min(len(text), m.end() + 12)
        if CAS_NEAR.search(text[lo:hi]):
            refs.append(m.group(0))
    return refs


def check_text(text):
    """→ (findings[(code, line, msg)], unjudged[(code, why)])。

    空壳抛 NotImplementedError 一律计入 unjudged，**不计入「零发条」**、也不裸抛；
    不在 UNIMPLEMENTED 里的码抛未落字则按「声明与实装不符」直接发条。
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


def report(path, findings, unjudged):
    for code, line, msg in findings:
        print("%s L%s %s" % (code, line, msg))
    for code, why in unjudged:
        print("不可判 %s（%s）" % (code, why))
    if findings:
        print("—— 机检：%d 条发条；判据未落字 %d 道" % (len(findings), len(unjudged)))
    elif unjudged:
        print("—— 机检：0 条发条，但 %d 道判据尚未落字，**这不等于合规**" % len(unjudged))
    else:
        print("—— 机检：0 条发条")


DEMO = r"""# 示例材料（600000.SH）其他权益工具登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议 ｜ 判断位 [待人工]
主体：示例材料（600000.SH）
报告期：2025 年年度报告·附注七·其他权益工具

## 其他权益工具概况

- 期末余额 其他权益工具合计 20.00 亿元「截至 2025 年 12 月 31 日，本集团其他权益工具账面价值合计人民币 20.00 亿元，其中永续债 15.00 亿元、优先股 5.00 亿元」〔锚：2025 年年报·第 210 页·附注七·其他权益工具〕[S1]
- 本期变动 净增加 15.00 亿元「本期新增永续债人民币 15.00 亿元，优先股余额本期无变动」〔锚：2025 年年报·第 210 页·附注七·其他权益工具〕[S1]

## 永续债条款

- 发行规模 15.00 亿元「本公司于 2025 年 3 月发行 2025 年度第一期中期票据（永续债），发行金额人民币 15.00 亿元，无固定到期日」〔锚：2025 年永续债募集说明书·第 12 页·发行条款〕[S2]
- 票面利率 3.85%「本期永续债初始票面利率为 3.85%，以 5 年为一个利率重置周期」〔锚：2025 年永续债募集说明书·第 13 页·发行条款〕[S2]
- 利息递延 可无限次递延「本公司有权在付息日将当期利息及已递延利息推延至下一付息日支付，且不受递延次数限制」〔锚：2025 年永续债募集说明书·第 14 页·发行条款〕[S2]
- 利率跳升 每 5 年跳升 300BP「若本公司在任一 5 年利率重置周期届满时未行使赎回权，则自该重置日起票面利率在当期基础上跳升 300 个基点，累计跳升幅度不超过 600 个基点」〔锚：2025 年永续债募集说明书·第 14 页·发行条款〕[S2]
- 赎回权 发行人选择权「本公司有权于每个付息日选择赎回本期永续债，赎回价格为面值加当期应计利息」〔锚：2025 年永续债募集说明书·第 15 页·发行条款〕[S2]
- 清偿顺序 劣后于普通债务「本期永续债在清算时的清偿顺序劣后于本公司普通债务，与本公司其他权益工具同顺位」〔锚：2025 年永续债募集说明书·第 15 页·发行条款〕[S2]

## 优先股条款

- 发行规模 5.00 亿元「本公司于 2024 年 12 月非公开发行优先股 5,000 万股，募集资金总额人民币 5.00 亿元」〔锚：2025 年年报·第 211 页·附注七·其他权益工具〕[S1]
- 股息率 5.20%「本次优先股采用固定股息率，票面股息率为 5.20%，以现金方式每年支付一次」〔锚：2025 年年报·第 211 页·附注七·其他权益工具〕[S1]
- 股息递延 可累积「本公司有权在股东大会决议后取消或递延支付优先股股息，未足额支付的股息可累积至下一年度」〔锚：2025 年年报·第 211 页·附注七·其他权益工具〕[S1]
- 赎回权 满 5 年后可赎回「自发行之日起满 5 年后，本公司有权按面值加当期已宣告未支付股息赎回全部或部分优先股」〔锚：2025 年年报·第 211 页·附注七·其他权益工具〕[S1]
- 转股安排 不设转股条款「本次优先股不设转股条款，不参与剩余利润分配」〔锚：2025 年年报·第 211 页·附注七·其他权益工具〕[S1]

## 利息与股利处理

- 永续债利息 作为利润分配「本期永续债利息作为利润分配处理，在所有者权益中列示，不确认为利息费用」〔锚：2025 年年报·第 212 页·附注七·其他权益工具〕[S1]
- 永续债付息 5,775.00 万元「报告期内本公司未发生永续债利息递延，已按期支付当期利息人民币 5,775.00 万元」〔锚：2025 年年报·第 212 页·附注七·其他权益工具〕[S1]
- 优先股股息 2,600.00 万元「本期宣告并支付优先股股息人民币 2,600.00 万元，按 5.20% 的票面股息率计算」〔锚：2025 年年报·第 212 页·附注七·其他权益工具〕[S1]
- 所得税处理 税后利润分配「永续债利息及优先股股息均以税后利润分配，不涉及所得税抵扣」〔锚：2025 年年报·第 212 页·附注七·其他权益工具〕[S1]

## 会计分类依据

- 永续债分类 权益工具「本公司将本期永续债分类为权益工具，理由为合同未约定交付现金或其他金融资产的不可避免义务，且不含可回售条款」〔锚：2025 年年报·第 213 页·附注七·其他权益工具〕[S1]
- 优先股分类 权益工具「本公司将本次优先股分类为权益工具，理由为本公司可自主决定是否支付股息且不承担交付现金的合同义务」〔锚：2025 年年报·第 213 页·附注七·其他权益工具〕[S1]
- 每股收益影响 已扣除「计算每股收益时，已扣除归属于其他权益工具持有者的当期利息及股息」〔锚：2025 年年报·第 213 页·附注七·其他权益工具〕[S1]

## 口径与未取到

- 未取到：无
- 口径：票息／股息率、递延与跳升条款、赎回权与分类理由一律照抄募集说明书与附注原文，本件不按利率或经验反推；永续债利息、优先股股息与债务利息费用不互抵。

## 来源

- [S1] 示例材料 2025 年年度报告 | https://example.invalid/600000_2025_annual.pdf | 检索日 2026-03-20
- [S2] 示例材料 2025 年度第一期中期票据（永续债）募集说明书 | https://example.invalid/600000_perpetual_2025.pdf | 检索日 2026-03-20
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
BAD_HEADING = _must_replace(DEMO, "## 优先股条款\n", "## 优先股条款旧\n", 1)
# (c) 整节删掉「来源」（连标题与两条来源行）：七节不齐、来源节为空。
_SOURCE_BLOCK = ("## 来源\n"
                 "\n"
                 "- [S1] 示例材料 2025 年年度报告 | "
                 "https://example.invalid/600000_2025_annual.pdf | 检索日 2026-03-20\n"
                 "- [S2] 示例材料 2025 年度第一期中期票据（永续债）募集说明书 | "
                 "https://example.invalid/600000_perpetual_2025.pdf | 检索日 2026-03-20\n")
BAD_SOURCE = _must_replace(DEMO, _SOURCE_BLOCK, "", 1)

# 道二坏样：整段「」+〔锚〕摘掉、只留收尾 [S1]（原句与锚都没了，行形制仍合规）。
_QUOTE_SNIP = ("「本期宣告并支付优先股股息人民币 2,600.00 万元，"
               "按 5.20% 的票面股息率计算」〔锚：2025 年年报·第 212 页·附注七·其他权益工具〕")
NO_TRIPLE = _must_replace(DEMO, _QUOTE_SNIP, "", 1)
# 道二坏样：S2 的检索日写成斜杠式，该行不合格式、S2 不再算登记（只坏 S2，S1 仍登记）。
BAD_SOURCE_FMT = _must_replace(
    DEMO,
    "https://example.invalid/600000_perpetual_2025.pdf | 检索日 2026-03-20",
    "https://example.invalid/600000_perpetual_2025.pdf | 检索日 2026/03/20", 1)
# 道二坏样：正文引 [S9]，来源节只有 S1／S2。
BAD_REF = _must_replace(
    DEMO,
    "已按期支付当期利息人民币 5,775.00 万元」〔锚：2025 年年报·第 212 页·附注七·其他权益工具〕[S1]",
    "已按期支付当期利息人民币 5,775.00 万元」〔锚：2025 年年报·第 212 页·附注七·其他权益工具〕[S9]",
    1)

# 道三坏样（甲）：条款项清空登记值，只留项名。
BAD_TERM_EMPTY = _must_replace(DEMO, "- 票面利率 3.85%「", "- 票面利率「", 1)
# 道三坏样（乙）：登记值仍写 3.85%，原句里的数被改成 4.15%。
BAD_TERM_NUM = _must_replace(DEMO, "初始票面利率为 3.85%", "初始票面利率为 4.15%", 1)
# 道三坏样（丙）：登记值仍写「可无限次递延」，原句里两处「递延」都删掉，
# 删完该行引文里彻底没有「递延」二字（删净才触发）。
BAD_TERM_WORD = _must_replace(
    _must_replace(DEMO, "当期利息及已递延利息推延", "当期利息推延", 1),
    "下一付息日支付，且不受递延次数限制", "下一付息日支付", 1)
# 反证（丁）：登记值多带一个说法（把原句的首句抄进来），数仍对得上、条款词也在原句里——不该发。
GOOD_TERM_REPHRASED = _must_replace(
    DEMO, "- 票面利率 3.85%「", "- 票面利率 初始票面利率为 3.85%「", 1)

# 道四坏样（甲）：永续债分类登记值改成「金融负债」，同行原句仍说「权益工具」。
BAD_CLASS_TERM = _must_replace(DEMO, "- 永续债分类 权益工具「", "- 永续债分类 金融负债「", 1)
# 道四坏样（乙）：优先股分类登记值自己接一根因果链（「故」），原句里没有该词。
BAD_CLASS_REASON = _must_replace(
    DEMO, "- 优先股分类 权益工具「",
    "- 优先股分类 权益工具，因其可自主决定股息故不构成交付义务「", 1)
# 道四坏样（丙）：每股收益影响登记值搬准则编号，原句里没有该引用。
BAD_CLASS_CAS = _must_replace(
    DEMO, "- 每股收益影响 已扣除「",
    "- 每股收益影响 按照《企业会计准则第 34 号》已扣除「", 1)
# 反证（丁）：登记值原样保留「权益工具」、不带因果也不带条文，只多一段中性括注——不该发。
GOOD_CLASS_ANNOTATED = _must_replace(
    DEMO, "- 永续债分类 权益工具「", "- 永续债分类 权益工具（发行方自评）「", 1)

# 道五坏样（甲）：利息登记值里自己写互抵（「净额」），同行原句没有该词。
BAD_LINE_NET = _must_replace(
    DEMO, "- 永续债付息 5,775.00 万元「",
    "- 永续债付息 5,775.00 万元，与债务利息费用轧差后净额列示「", 1)
# 道五坏样（乙）：登记值把「递延」与费用化写在一处，原句里没有「递延」也没有费用化。
BAD_LINE_FEE = _must_replace(
    DEMO, "- 优先股股息 2,600.00 万元「",
    "- 优先股股息 递延利息计入当期费用 2,600.00 万元「", 1)
# 道五坏样（丙①）：缺口节点名了一个正文里确有全三元组登记行的项。
BAD_LINE_GAP = _must_replace(DEMO, "- 未取到：无", "- 未取到：永续债付息", 1)
# 反证（丁）：互抵与「净额」字样只出现在「」引文里，登记值一个不写——
# 引文是披露在说，不是本件在对冲，不该发。
GOOD_LINE_QUOTE_ONLY = _must_replace(
    DEMO, "不涉及所得税抵扣」",
    "不涉及所得税抵扣，与债务利息费用互抵后净额列示」", 1)


def selftest():
    """逐档现报：好样须零发条，坏样须恰发该道码；空壳一道计「不可判」，不并进「不合」。

    档数＝逐档比对的那几档 + UNIMPLEMENTED 的码数（未落字各算一档「不可判」）。
    本拍五道全落字，好样单稿退 0，不得读成「五道全方面覆盖」。
    """
    cases = (
        ("好样应零发条", DEMO, frozenset()),
        ("形制：头部删掉「不构成投资建议」", BAD_MARK, frozenset({"OEI-STRUCT"})),
        ("形制：节标题写成认不出的样子（进 stray＋缺节）", BAD_HEADING,
         frozenset({"OEI-STRUCT"})),
        ("形制：整节删掉「来源」", BAD_SOURCE, frozenset({"OEI-STRUCT"})),
        ("原句与锚：摘掉整段「」+〔锚〕，只留 [S1]", NO_TRIPLE,
         frozenset({"OEI-QUOTE"})),
        ("来源行：S2 检索日写成 2026/03/20", BAD_SOURCE_FMT, frozenset({"OEI-QUOTE"})),
        ("对应：正文引 [S9] 而来源节只有 S1／S2", BAD_REF, frozenset({"OEI-QUOTE"})),
        ("条款：只留项名、登记值为空", BAD_TERM_EMPTY, frozenset({"OEI-TERMS"})),
        ("条款：登记值 3.85%，原句写成 4.15%", BAD_TERM_NUM, frozenset({"OEI-TERMS"})),
        ("条款：登记写「递延」，原句里两处递延都删净", BAD_TERM_WORD,
         frozenset({"OEI-TERMS"})),
        ("反证：登记值多带说法（数在、条款词在），不该发", GOOD_TERM_REPHRASED,
         frozenset()),
        ("分类：登记值写「金融负债」，原句仍是「权益工具」", BAD_CLASS_TERM,
         frozenset({"OEI-CLASS"})),
        ("分类：登记值自己接因果链（「故」），原句没有", BAD_CLASS_REASON,
         frozenset({"OEI-CLASS"})),
        ("分类：登记值搬准则编号「第 34 号」，原句没有", BAD_CLASS_CAS,
         frozenset({"OEI-CLASS"})),
        ("反证：登记值多带中性括注，不带因果不带条文，不该发", GOOD_CLASS_ANNOTATED,
         frozenset()),
        ("红线：利息登记值自己写「轧差后净额」", BAD_LINE_NET, frozenset({"OEI-LINE"})),
        ("红线：登记值把「递延」与「计入当期费用」写在一处", BAD_LINE_FEE,
         frozenset({"OEI-LINE"})),
        ("缺口：节点名了「永续债付息」，正文却有它的登记行", BAD_LINE_GAP,
         frozenset({"OEI-LINE"})),
        ("反证：互抵字样只在「」引文里，登记值不写，不该发", GOOD_LINE_QUOTE_ONLY,
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

    # 覆盖自证：每道已落字的码，在 cases 里至少有一档期望恰含它。
    # 这条防的是「实现了一道判据、同时少了一档不可判，净增反例 0 档」——
    # 判据接进 CHECKS 却没有反例钉住，它以后被改坏，自测照样报 不合=0。
    implemented = [c for c in CODES if c not in UNIMPLEMENTED]
    covered = set()
    for _label, _text, want in cases:
        covered |= set(want)
    uncovered = [c for c in implemented if c not in covered]
    if uncovered:
        bad += 1
        print("不合 覆盖自证：已落字码 %d 道，有反例的 %d 道，缺反例：%s"
              % (len(implemented), len(implemented) - len(uncovered),
                 "／".join(uncovered)))
    else:
        print("过   覆盖自证（已落字码 %d 道，有反例的 %d 道，缺反例：无）"
              % (len(implemented), len(implemented)))

    # 空壳自证：清单里的码调用即抛且点名自身；不在清单里的码（当前五道全落字）不许抛，只能返回列表
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
        print("过   空壳自证（%s 调用即抛并点名；其余返回列表）" % "、".join(UNIMPLEMENTED))
    else:
        print("过   空壳自证（无空壳；五道调用均返回列表）")

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
                         % (label, sorted(got_codes) or "无", sorted(UNIMPLEMENTED)))
    if crash:
        bad += 1
        print("不合 不崩自证：%s" % "；".join(crash))
    else:
        print("过   不崩自证（空稿／乱头／只头无节均返回二元组，未落字 %d 道计不可判）"
              % len(UNIMPLEMENTED))

    # 单稿退码自证：好样落盘单跑，退码与「是否还有未落字」绑定，不写死数：
    # 有未落字 → 3（且输出须含「不可判」与「这不等于合规」）；五道全落字 → 0（且不得再出现该句）。
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
    ap = argparse.ArgumentParser(description="其他权益工具判断稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="其他权益工具稿 .md 路径")
    ap.add_argument("--selftest", action="store_true", help="跑包内自检")
    ap.add_argument("--demo", action="store_true", help="打印一份完整合规样例（零输入可跑）")
    try:
        args = ap.parse_args(argv)
    except SystemExit as exc:                          # 用法错统一退 2，不沿用 argparse 的 2/0 混用
        return 2

    if args.selftest:
        return selftest()
    if args.demo:
        sys.stdout.write(DEMO)
        return 0
    if not args.path:
        ap.print_usage(sys.stderr)
        print("缺入参：给一份其他权益工具稿路径，或用 --demo / --selftest", file=sys.stderr)
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
