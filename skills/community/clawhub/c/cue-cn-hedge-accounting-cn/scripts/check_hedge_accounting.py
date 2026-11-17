#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_hedge_accounting.py — 套期保值会计处理判断稿五道机检（零网络、零外发、不读环境变量）

**五道判据全部落字**：七节常量、五道码常量、形制与三元组道具、`--demo`、`--selftest`
与读入/退码形制之外，五道函数体都已实装（形制／原句与锚／三类型只认原句／有效性评价与
无效部分只认原句／红线）；`_not_judged` 保留为兜底——只给「声明已落字却仍抛未落字」用，
由调用方按不合计处理，不会被读成「不可判」而放行。

用法：
    python3 scripts/check_hedge_accounting.py <套期保值稿>.md
    python3 scripts/check_hedge_accounting.py --selftest
    python3 scripts/check_hedge_accounting.py --demo     打印一份完整合规样例（零输入可跑）

七节（按序，`## ` 起节）：
    套期保值概况／套期关系与指定／套期工具与被套期项目／有效性评价与无效部分／现金流量套期储备
    ／口径与未取到／来源

五道码（五道均已落字，下面写的是**这道判什么**；判据与实现不符时按不合计处理，不放行）：

道一 HA-STRUCT 形制
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]；
  `主体：` 行、`报告期：` 行在场且非空；七节齐且按序；前五节各至少一条 `- ` 发现行，
  节内只许 `- ` 发现行、`### ` 子标题与空行。

道二 HA-QUOTE 原句与锚
  每条发现行以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；原句与锚不得为空；
  例外只有三形：「未取到」行、[待人工] 行与〔自算〕行；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址；
  正文引用的每个 [S#] 必须在来源节有对应行。

道三 HA-TYPE 套期关系三类型只认原句
  公允价值套期／现金流量套期／境外经营净投资套期，三类只能照抄披露原文；
  正文写某一类而同一行「」原句里没有该类别表述，一律发——类型是披露指定的，不是本件判断的。

道四 HA-EFFECT 有效性评价与无效部分只认原句
  有效性评价方法与结论、无效部分金额与去向，都只能照抄原句；
  正文写「高度有效」「无效部分计入当期损益」，同行原句里找不到该表述，一律发。

道五 HA-LINE 红线
  套期储备（其他综合收益腿）不得与套期损益（当期损益腿）轧成净额／合计／相抵；
  无效部分不得以暂挂／待摊／递延确认挂账不确认；
  正文与「口径与未取到」节两向点名（正文「未取到 X」须在节里点名，反之亦然），
  零缺口须显式写 `未取到：无`；节名含「红线」「机检」的节不作判域，「」引文不算本件在说。

退码：0 全过 / 1 有发条 / 2 用法错（缺参数） / 3 读不到文件或空稿
      （`UNIMPLEMENTED` 非空且某道抛未落字时，`--selftest` 把该档计「不可判」并退 3，
      不并入「不合」；当前五道全落字，`UNIMPLEMENTED = ()`，正常读数不可判=0、退 0）。
"""

import argparse
import re
import sys

SLUG = "cue-cn-hedge-accounting-cn"

CODES = ("HA-STRUCT", "HA-QUOTE", "HA-TYPE", "HA-EFFECT", "HA-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("套期保值概况", "套期关系与指定", "套期工具与被套期项目",
            "有效性评价与无效部分", "现金流量套期储备", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"

# 五道已全部落字，此处留空；码抛未落字时才计「不可判」——
# 且只限列表里的码：声明已落字的判据再抛未落字，即声明与实装不符，按不合计处理，不装成「不可判」。
UNIMPLEMENTED = ()

# HA-EFFECT 用的四串词：结论／方法名／去向，外加金额形制。
EFFECT_CONCLUSIONS = ("高度有效", "基本有效", "有效", "无效")
EFFECT_METHODS = ("定量评价", "回归分析", "美元偏移法")
EFFECT_DESTINATIONS = ("当期损益", "其他综合收益")
AMOUNT = re.compile(r"\d+(?:\.\d+)?\s*(?:万元|亿元|元)")

# HA-LINE 用的四串词：储备腿／损益腿／轧账字样／挂账字样，外加红线节与缺口项名。
RESERVE_WORDS = ("套期储备", "其他综合收益")
PNL_WORDS = ("套期损益", "当期损益")
NET_WORDS = ("净额", "合计", "轧差", "相抵", "抵减")
HANG_WORDS = ("暂挂", "待摊", "递延确认")
EXCUSE_WORDS = ("不适用", "无此项", "无需披露")
_REDLINE_SECTION = re.compile(r"红线|机检")
GAP_ITEM = re.compile(r"^-\s*未取到\s*[:：]\s*(?P<item>.+)$")

# 套期关系三类型：变体归一到同一类，比对时按类算，不按字面算。
TYPE_VARIANTS = (
    ("境外经营净投资套期", "境外经营净投资套期"),
    ("对境外经营净投资的套期", "境外经营净投资套期"),
    ("境外经营套期", "境外经营净投资套期"),
    ("公允价值套期", "公允价值套期"),
    ("现金流量套期", "现金流量套期"),
)

HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")
SUBJECT = re.compile(r"^主体：\s*(\S.*)$")
PERIOD = re.compile(r"^报告期：\s*(\S.*)$")

TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
ANCHOR_REF = re.compile(r"\[(S\d+)\]")
ANCHOR_BLOCK = re.compile(r"〔\s*锚\s*[:：][^〕]*〕")

SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)"
    r"\|\s*(?P<url>https?://\S+)\s*\|"
    r"\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$"
)


# ---------------------------------------------------------------- 判据

def _not_judged(code, why):
    """兜底：声明已落字却抛未落字时由调用方按不合计处理（当前无判据走到这里）。"""
    raise NotImplementedError("%s 未落字：%s" % (code, why))


def check_struct(head, sections, stray):
    """道一 HA-STRUCT 形制：头部四件自标与两行、七节齐且按序、节内行形制。

    只判「形」：节名在不在、顺序对不对、节内是不是清一色 `- ` 发现行。
    判断内容对不对是另四道的事——这里不越界，否则一支注入会同时红两道、分不清归属。
    """
    out = []
    htext = "\n".join(s for _i, s in head)
    for mark in MARK_TEXTS:
        if mark not in htext:
            out.append(("HA-STRUCT", head[0][0] if head else 1, "头部缺自标「%s」" % mark))
    if not any(SUBJECT.match(s) for _i, s in head):
        out.append(("HA-STRUCT", head[0][0] if head else 1, "头部缺 `主体：` 行"))
    if not any(PERIOD.match(s) for _i, s in head):
        out.append(("HA-STRUCT", head[0][0] if head else 1, "头部缺 `报告期：` 行"))

    names = [n for n, _l, _b in sections]
    for name in SECTIONS:
        if name not in names:
            out.append(("HA-STRUCT", 1, "缺节「%s」" % name))
    pos = [SECTIONS.index(n) for n in names]
    if pos != sorted(pos):
        out.append(("HA-STRUCT", 1, "节序不对：现序 %s，应序 %s"
                    % ("／".join(names), "／".join(SECTIONS))))
    for lineno, raw in stray:
        out.append(("HA-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw))

    for name, hline, body in sections:
        if name not in CONTENT_SECTIONS:
            if name == GAP_SECTION:
                for lineno, s in body:
                    if s.strip() and not _is_finding_line(s):
                        out.append(("HA-STRUCT", lineno, "「%s」只许 `- ` 行：%s"
                                    % (name, s.strip()[:40])))
            elif name == SOURCE_SECTION:
                for lineno, s in body:
                    if s.strip() and not s.lstrip().startswith("- ["):
                        out.append(("HA-STRUCT", lineno, "来源节只许 `- [S#] …` 行：%s"
                                    % s.strip()[:40]))
            continue
        n_find = 0
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                out.append(("HA-STRUCT", lineno, "节内只许 `- ` 发现行：%s" % s.strip()[:40]))
                continue
            n_find += 1
        if n_find == 0:
            out.append(("HA-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name))
    return out


def check_quote(head, sections, stray):
    """道二 HA-QUOTE 原句与锚：三元组、来源行、[S#] 两向对应。

    例外只有三形：「未取到」行、[待人工] 行、〔自算〕行——前两者是缺口与判断位，
    后者已经必须在同一行交代算法与口径，要求它再挂原句等于把自算伪装成披露值。
    """
    out = []
    referenced = []
    for name, _hline, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue                     # 形制那道已经发过，这里不重复发
            referenced.extend(ANCHOR_REF.findall(s))
            if not TRIPLE.search(s):
                if _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s:
                    continue
                label, _rest = _split_label(s)
                out.append(("HA-QUOTE", lineno,
                            "发现行缺「」原句 + 〔锚：…〕 + [S#] 三元组：%s"
                            % (label or s.strip()[:40])))
                continue
            for m in TRIPLE.finditer(s):
                if not m.group("q").strip():
                    out.append(("HA-QUOTE", lineno, "原句为空"))
                if not m.group("a").strip():
                    out.append(("HA-QUOTE", lineno, "锚为空"))
            if not re.search(r"\[S\d+\]\s*$", s.strip()):
                out.append(("HA-QUOTE", lineno, "发现行未以 [S#] 收尾（三元组须在行末）"))

    defined = set()
    for name, _hline, body in sections:
        if name != SOURCE_SECTION:
            continue
        for lineno, s in body:
            if not s.strip():
                continue
            m = SOURCE_LINE.match(s.strip())
            if not m:
                out.append(("HA-QUOTE", lineno,
                            "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:50]))
                continue
            defined.add(m.group("s"))
    for ref in sorted(set(referenced)):
        if ref not in defined:
            out.append(("HA-QUOTE", 1, "正文引用 [%s]，来源节没有对应登记行" % ref))
    return out


def check_type(head, sections, stray):
    """道三 HA-TYPE 套期关系三类型只认原句：类型是披露指定的，不是本件判断的。

    甲 登记值写了某类型，同一行「」原句里没有该类型词 → 发（本件替披露定了类型）。
    乙 同一行登记了两个类型而原句只写一个 → 发（至少一个类型没有原句支撑）。
    丙 前五节一条类型都没登记（连引文里也没有）→ 在首条发现行发一次，不逐行发。
    「未取到」与 [待人工] 行不归这道：缺口不等于登记。
    """
    out = []
    first_line = None
    seen_any = False
    for name, _hline, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue
            if first_line is None:
                first_line = lineno
            # 丙的在场：非缺口行里出现类型词（登记值或引文都算）。「未取到 X」是缺席不是登记，
            # 拿它当在场会让「一条类型都没登记」的稿子蒙混过关。
            if not _is_gap_line(s) and _types_in(s):
                seen_any = True
            if _is_gap_line(s) or "[待人工]" in s:
                continue                     # 缺口与判断位不归这道
            reg = _types_in(_strip_quotes(s))
            said = _types_in("".join(_quotes(s)))
            missing = sorted(reg - said)
            if not missing:
                continue
            if len(reg) >= 2 and said:
                out.append(("HA-TYPE", lineno,
                            "同一行登记了%s个类型（%s）而原句只写一个（%s）"
                            % (len(reg), "／".join(sorted(reg)), "／".join(sorted(said)))))
            else:
                out.append(("HA-TYPE", lineno,
                            "登记值写「%s」，同行原句没有该类型表述" % missing[0]))
    if not seen_any:
        out.append(("HA-TYPE", first_line or 1,
                    "前五节一条套期类型都没登记（公允价值／现金流量／境外经营净投资）"))
    return out


def check_effect(head, sections, stray):
    """道四 HA-EFFECT 有效性评价与无效部分只认原句：结论、金额、去向、方法名都不是本件能推的。

    甲 登记值写了有效性结论（高度有效／基本有效／有效／无效），同行原句没有该结论词 → 发。
    乙 登记了无效部分金额，同行原句没有该数（或原句只说「存在无效部分」没给数）→ 发。
    丙 登记了无效部分去向（当期损益／其他综合收益），同行原句没有该去向 → 发。
    丁 登记值写评价方法名（定量评价／回归分析／美元偏移法），同行原句没有该方法名 → 发。
    「未取到」与 [待人工] 行不参与：那是缺口与判断位，不是断言。
    """
    out = []
    for name, _hline, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue
            if _is_gap_line(s) or "[待人工]" in s:
                continue                     # 缺口不等于断言，这四条都不判它
            plain = _strip_quotes(s)
            quote_text = "".join(_quotes(s))
            for w in _longest_in(plain, EFFECT_CONCLUSIONS):
                if w not in quote_text:
                    out.append(("HA-EFFECT", lineno,
                                "登记值写有效性结论「%s」，同行原句没有该结论" % w))
            for w in _longest_in(plain, EFFECT_METHODS):
                if w not in quote_text:
                    out.append(("HA-EFFECT", lineno,
                                "登记值写评价方法「%s」，同行原句没有该方法名" % w))
            if "无效" not in s:
                continue                     # 乙丙只判无效部分那几行
            for amt in AMOUNT.findall(plain):
                if _squeeze(amt) not in _squeeze(quote_text):
                    out.append(("HA-EFFECT", lineno,
                                "登记了无效部分金额「%s」，同行原句没有该数" % amt.strip()))
            for w in EFFECT_DESTINATIONS:
                if w in plain and w not in quote_text:
                    out.append(("HA-EFFECT", lineno,
                                "登记了无效部分去向「%s」，同行原句没有该去向" % w))
    return out


def check_line(head, sections, stray):
    """道五 HA-LINE 红线：储备与损益两条腿不许轧、无效部分不许挂账、缺口两向点名。

    甲 一行里储备腿（本行登记值或所在节名含「套期储备」／其他综合收益）与损益腿
       （套期损益／当期损益）同时在场，行内又出现净额／合计／轧差／相抵／抵减 → 发。
    乙 登记了「无效部分」金额而行内写暂挂／待摊／递延确认 → 发。
    丙 正文「未取到 X」与「口径与未取到」节点名两向对账，各缺一向都发；零缺口须写
       `未取到：无`；搪塞词「不适用」「无此项」「无需披露」出现即发。
    丁 节名含「红线」或「机检」的节整体跳过；「」引文不算本件在说，只判本件自己写的字。
    """
    out = []
    body_items, gap_items = {}, {}
    gap_hline = 1
    all_lines, judged_lines = [], []
    for name, hline, body in sections:
        if _REDLINE_SECTION.search(name or ""):
            continue                         # 丁：红线／机检节不作判域
        if name == GAP_SECTION:
            gap_hline = hline
        all_lines.extend(body)
        if name == GAP_SECTION:
            for lineno, s in body:
                m = GAP_ITEM.match(s.strip())
                if not m:
                    continue
                item = _clean_item(m.group("item"))
                if item and item != "无":    # `未取到：无` 是零缺口的显式写法，不入对账
                    gap_items[item] = lineno
            continue
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue
            judged_lines.append((lineno, s, name))
            plain = _strip_quotes(s)
            if "未取到" in plain:
                item = _gap_item_in(plain)
                if item:
                    body_items[item] = lineno

    for lineno, s, name in judged_lines:
        if _is_gap_line(s) or "[待人工]" in s:
            continue                         # 缺口不等于断言
        plain = _strip_quotes(s)
        reserve_leg = any(w in plain for w in RESERVE_WORDS) or any(
            w in (name or "") for w in RESERVE_WORDS)
        pnl_leg = any(w in plain for w in PNL_WORDS)
        net_word = [w for w in NET_WORDS if w in plain]
        if reserve_leg and pnl_leg and net_word:
            out.append(("HA-LINE", lineno,
                        "套期储备与套期损益轧成「%s」：两条腿不得互抵" % net_word[0]))
        if "无效" in s and any(w in plain for w in HANG_WORDS):
            hit = [w for w in HANG_WORDS if w in plain]
            out.append(("HA-LINE", lineno,
                        "无效部分「%s」，不得挂账不确认" % hit[0]))

    for item, lineno in body_items.items():
        if item not in gap_items:
            out.append(("HA-LINE", lineno,
                        "正文写了「未取到：%s」，「%s」节没有点名" % (item, GAP_SECTION)))
    for item, lineno in gap_items.items():
        if item not in body_items:
            out.append(("HA-LINE", lineno,
                        "「%s」节点名「%s」，正文没有对应的「未取到」" % (GAP_SECTION, item)))

    if "未取到" not in "\n".join(s for _i, s in all_lines):
        out.append(("HA-LINE", gap_hline,
                    "全文无缺口，但「%s」节未显式写 `未取到：无`" % GAP_SECTION))

    for lineno, s in all_lines:
        hit = [w for w in EXCUSE_WORDS if w in s]
        if hit:
            out.append(("HA-LINE", lineno,
                        "搪塞词「%s」：未取到与不适用是两件事" % hit[0]))
    return out


CHECKS = (
    ("HA-STRUCT", check_struct),
    ("HA-QUOTE", check_quote),
    ("HA-TYPE", check_type),
    ("HA-EFFECT", check_effect),
    ("HA-LINE", check_line),
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

    野节＝不认识的节名，或多出来的同名节。它们**另记**、不吞进上一节：
    吞进去会让「多出一节」既不发 HA-STRUCT、又把下一节的发现行算到这一节头上。
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
    """缺口行：本件没取到、按 `未取到` 如实登记的那种行。"""
    return "未取到" in s


def _split_label(s):
    """→ (标签, 其余)。标签是 `- ` 之后第一段，用于发条时点名是哪一行，不改原文。"""
    t = s.strip()
    if t.startswith("- "):
        t = t[2:]
    parts = t.split(None, 1)
    if not parts:
        return "", ""
    return parts[0], (parts[1] if len(parts) > 1 else "")


def _quotes(s):
    """→ 该行所有「」原句（按出现顺序）。"""
    return QUOTE.findall(s)


def _strip_quotes(s):
    """去掉「」原句、〔锚：…〕与 [S#]，只留本件自己写的登记值。"""
    t = ANCHOR_REF.sub("", s)
    t = ANCHOR_BLOCK.sub("", t)
    return QUOTE.sub("", t)


def _types_in(text):
    """→ 文本里出现的套期类型集合（归一后的类别名）。变体按类算，不按字面算。"""
    return set(canon for variant, canon in TYPE_VARIANTS if variant in text)


def _longest_in(text, words):
    """→ text 里命中的词，且去掉被更长命中词包含的短词（「有效」不再单报于「高度有效」下）。"""
    hit = [w for w in words if w in text]
    return [w for w in hit if not any(w != o and w in o for o in hit)]


def _squeeze(s):
    """比对金额时抹掉空白：`12.30 万元` 与 `12.30万元` 是同一个数。"""
    return re.sub(r"\s+", "", s)


def _gap_item_in(plain):
    """→ 正文行里「未取到」后面那个项名（`未取到：X` 取 X；只写「未取到」无项名则返回空）。"""
    m = re.search(r"未取到\s*[:：]\s*(.+)$", plain)
    if not m:
        return ""
    return _clean_item(m.group(1))


def _clean_item(s):
    """项名归一：去掉 `- `、空白与收尾标点，好让两向对账真的对得上。"""
    t = s.strip()
    if t.startswith("- "):
        t = t[2:]
    return t.strip().strip("：: 　，,。.;；")


def check_text(text):
    """→ (findings[(code, line, msg)], unjudged[(code, why)])。

    发条按 (行号, 码序) 排；判据抛 NotImplementedError 的计入 unjudged，**不计入「零发条」**。
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
                # 不在 UNIMPLEMENTED 里却抛未落字：声明与实装不符，按不合计处理
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


DEMO = r"""# 示例材料（600000.SH）套期保值会计处理登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议 ｜ 判断位 [待人工]
主体：示例材料（600000.SH）
报告期：2025 年年度报告·附注七·套期会计

## 套期保值概况

- 套期类型 现金流量套期「本公司子公司甲以浮动利率借款，并签订利率互换合约，将其指定为现金流量套期」〔锚：2025 年年报·第 165 页·附注七·套期会计〕[S1]
- 净投资套期 未取到：境外经营净投资套期

## 套期关系与指定

- 甲借款利率互换 指定日为 2025-01-01「本公司将利率互换合约指定为对甲借款浮动利息现金流量的套期工具，套期关系自 2025 年 1 月 1 日起生效」〔锚：2025 年年报·第 165 页·附注七·套期会计〕[S1]

## 套期工具与被套期项目

- 套期工具 利率互换合约 名义本金 5,000 万元「利率互换合约名义本金为人民币 5,000 万元，到期日为 2027 年 12 月 31 日」〔锚：2025 年年报·第 166 页·附注七·套期会计〕[S1]
- 被套期项目 甲借款浮动利息「被套期项目为甲借款按季重定价的浮动利息现金流量」〔锚：2025 年年报·第 166 页·附注七·套期会计〕[S1]

## 有效性评价与无效部分

- 有效性评价 按季定性评价「本集团按季度以定性方式评价套期有效性，套期工具与被套期项目的关键条款一致」〔锚：2025 年年报·第 166 页·附注七·套期会计〕[S1]
- 无效部分 计入当期损益 12.30 万元「本期套期无效部分金额为人民币 12.30 万元，已计入当期损益」〔锚：2025 年年报·第 167 页·附注七·套期会计〕[S1]

## 现金流量套期储备

- 本期变动 -85.60 万元「本期计入其他综合收益的现金流量套期储备金额为人民币 -85.60 万元」〔锚：2025 年年报·第 167 页·附注七·套期会计〕[S1]

## 口径与未取到

- 未取到：境外经营净投资套期
- 口径：套期类型、有效性评价与无效部分一律照抄披露原文，本件不按比例或经验反推；套期储备与套期损益不互抵。

## 来源

- [S1] 示例材料 2025 年年度报告 | https://example.invalid/600000_2025_annual.pdf | 检索日 2026-03-20
"""


# 坏样都由好样单向替换而来：只动该道真正看的那一处，别处一行不改。
# 形制：整节删掉「现金流量套期储备」——七节不再齐，而来源节的 [S1] 登记行仍在，
# 所以只有 HA-STRUCT（缺节）会红，HA-QUOTE 不该跟着红。
_CASHFLOW_BLOCK = ("## 现金流量套期储备\n"
                   "\n"
                   "- 本期变动 -85.60 万元「本期计入其他综合收益的现金流量套期储备金额为"
                   "人民币 -85.60 万元」〔锚：2025 年年报·第 167 页·附注七·套期会计〕[S1]\n"
                   "\n")
BAD_STRUCT = DEMO.replace(_CASHFLOW_BLOCK, "")

# 锚：一条发现行拆掉三元组（原句与锚都没了，只剩登记值）——该只红 HA-QUOTE。
BAD_QUOTE = DEMO.replace(
    "「本公司将利率互换合约指定为对甲借款浮动利息现金流量的套期工具，"
    "套期关系自 2025 年 1 月 1 日起生效」〔锚：2025 年年报·第 165 页·附注七·套期会计〕[S1]",
    "", 1)

# 类型自判：登记值写「公允价值套期」，原句写的是「现金流量套期」——该只红 HA-TYPE。
BAD_TYPE = DEMO.replace(
    "- 套期类型 现金流量套期「",
    "- 套期类型 公允价值套期「", 1)

# 反证：类型词只出现在「」引文里，登记值写别的（不写类型词）——判的是本件自己的话，
# 引文里的类型不构成登记，不该发。
GOOD_TYPE_QUOTE_ONLY = DEMO.replace(
    "- 套期类型 现金流量套期「",
    "- 套期安排 利率互换「", 1)

# 有效性自判：登记值写「高度有效」，原句只写「按季度以定性方式评价」——该只红 HA-EFFECT。
BAD_EFFECT = DEMO.replace(
    "- 有效性评价 按季定性评价「",
    "- 有效性评价 高度有效「", 1)

# 反证：结论词与方法名只出现在「」引文里，登记值一个不写——判的是本件自己的话，
# 引文里的「高度有效」「定性评价」不构成登记，不该发。
GOOD_EFFECT_QUOTE_ONLY = DEMO.replace(
    "- 有效性评价 按季定性评价「",
    "- 评价方式 「", 1)

# 红线：把套期储备与套期损益互抵成净额——该只红 HA-LINE。
BAD_LINE = DEMO.replace(
    "- 本期变动 -85.60 万元「",
    "- 本期变动 与套期损益互抵后净额 0.00 万元「", 1)

# 反证：互抵／挂账字样只出现在「」引文里，登记值一个不写——引文是披露在说，不是本件在说。
GOOD_LINE_QUOTE_ONLY = DEMO.replace(
    "「本期计入其他综合收益的现金流量套期储备金额为人民币 -85.60 万元」",
    "「本期计入其他综合收益的现金流量套期储备金额为人民币 -85.60 万元，"
    "与套期损益相抵后净额列示」", 1).replace(
    "「本期套期无效部分金额为人民币 12.30 万元，已计入当期损益」",
    "「本期套期无效部分金额为人民币 12.30 万元，已计入当期损益，本期暂挂待摊」", 1)

# 反证：零缺口——正文与节里都不再有「未取到：X」，节里显式写 `未取到：无`，不该发。
GOOD_LINE_NO_GAP = DEMO.replace(
    "- 净投资套期 未取到：境外经营净投资套期",
    "- 净投资套期 0 笔「本报告期未发生境外经营净投资套期」"
    "〔锚：2025 年年报·第 167 页·附注七·套期会计〕[S1]", 1).replace(
    "- 未取到：境外经营净投资套期", "- 未取到：无", 1)


def selftest():
    """逐档现报：好样须零发条，坏样须只发出该道码；判据声明未落字的档才计「不可判」（当前为零）。"""
    cases = (
        ("好样应零发条", DEMO, None),
        ("形制：整节删掉「现金流量套期储备」（七节不齐）", BAD_STRUCT, "HA-STRUCT"),
        ("锚：一条发现行拆掉「」原句与〔锚〕，只剩登记值", BAD_QUOTE, "HA-QUOTE"),
        ("类型：登记值写「公允价值套期」，原句写的是「现金流量套期」", BAD_TYPE, "HA-TYPE"),
        ("反证：类型词只在「」引文里，登记值不写类型", GOOD_TYPE_QUOTE_ONLY, None),
        ("有效性：登记值写「高度有效」，原句只写按季定性评价", BAD_EFFECT, "HA-EFFECT"),
        ("反证：结论词与方法名只在「」引文里，登记值不写", GOOD_EFFECT_QUOTE_ONLY, None),
        ("红线：套期储备与套期损益互抵成净额", BAD_LINE, "HA-LINE"),
        ("反证：互抵／挂账字样只在「」引文里，登记值不写", GOOD_LINE_QUOTE_ONLY, None),
        ("反证：零缺口显式写「未取到：无」", GOOD_LINE_NO_GAP, None),
    )
    bad = unk = 0
    for label, text, want in cases:
        findings, unjudged = check_text(text)
        by_code = {code: why for code, why in unjudged}
        if want is not None and want in by_code:
            print("不可判 %s（%s 判据未落字，本档不作为绿也不作为红）" % (label, want))
            unk += 1
            continue
        got = set(c for c, _l, _m in findings)
        wantset = set() if want is None else {want}
        if got == wantset:
            print("过   %s（发条 %d 条：%s）"
                  % (label, len(findings), "、".join(sorted(got)) or "无"))
        else:
            bad += 1
            detail = "；".join("%s L%s %s" % (c, l, m) for c, l, m in findings[:4])
            print("不合 %s：期望 %s 实得 %s ｜ %s"
                  % (label, sorted(wantset) or "无", sorted(got) or "无", detail))
    print("——")
    print("自测档数=%d｜不合=%d｜不可判=%d" % (len(cases), bad, unk))
    if bad:
        return 1
    return 3 if unk else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="套期保值会计处理判断稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="套期保值稿 .md 路径")
    ap.add_argument("--selftest", action="store_true", help="跑包内夹具自检")
    ap.add_argument("--demo", action="store_true", help="打印一份完整合规样例（零输入可跑）")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.demo:
        sys.stdout.write(DEMO)
        return 0
    if not args.path:
        ap.print_usage(sys.stderr)
        print("缺入参：给一份套期保值稿路径，或用 --demo / --selftest", file=sys.stderr)
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
