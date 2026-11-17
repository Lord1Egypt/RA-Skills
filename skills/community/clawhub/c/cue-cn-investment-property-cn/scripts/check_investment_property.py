#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cn-investment-property-cn —— 投资性房地产逐条挂源的五道机检（零网络）。

五道：
  IP-STRUCT  形制     头部四件自标、主体／报告期、七节齐且有序、前五节各有发现行
  IP-QUOTE   原句与锚 每条发现行以「原句」〔锚：…〕[S#] 收尾；来源行带 URL 与检索日；
                      引用的 [S#] 必须已在来源节登记
  IP-NOSELF  不得自推 计量模式只认披露写法；转换差额的去向与金额须与原句一致（第 3 拍）
  IP-GAP     两向点名 正文与第六节互相对账；零缺口须显式写「未取到：无」（第 3 拍）
  IP-LINE    红线     处置建议、公允价值预测、评估结论点评、评级与目标价零命中（第 3 拍）

退码：0 五道全过 / 1 有发条 / 2 用法错 / 3 读不到文件或空稿。

本拍（第 2 拍）只填 IP-STRUCT 与 IP-QUOTE，其余三道留空。
"""

from __future__ import annotations

import datetime
import os
import re
import sys

SLUG = "cue-cn-investment-property-cn"
CODES = ("IP-STRUCT", "IP-QUOTE", "IP-NOSELF", "IP-GAP", "IP-LINE")

SECTIONS = (
    "投资性房地产概况",
    "计量模式",
    "成本模式明细",
    "公允价值模式明细",
    "转换与处置",
)
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"
ALL_SECTIONS = SECTIONS + (GAP_SECTION, SOURCE_SECTION)

USAGE = """usage: check_investment_property.py <稿.md>
       check_investment_property.py --selftest
       check_investment_property.py --demo

投资性房地产逐条挂源的五道机检（零网络）：
  IP-STRUCT 形制 / IP-QUOTE 原句与锚 / IP-NOSELF 不得自推自算 /
  IP-GAP 未取到两向点名 / IP-LINE 红线
退码：0 五道全过 / 1 有发条 / 2 用法错 / 3 读不到文件或空稿
"""

MARK_TEXTS = ("〔AI 起草〕", "〔须与原句核对〕", "〔非投资建议〕", "〔待人工〕")

HEADING = re.compile(r"^##\s+(\S.*?)\s*$")
NUMBERING = re.compile(r"^[一二三四五六七八九十]+、\s*")
SUBJECT = re.compile(r"^-\s*主体[：:]\s*\S")
PERIOD = re.compile(r"^-\s*报告期[：:]\s*\S")

TRIPLE = re.compile(r"「[^」]*」\s*〔\s*锚\s*[:：][^〕]*〕\s*\[S\d+\]\s*$")
REF_TAIL = re.compile(r"\[(S\d+)\]\s*$")
SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)\|\s*(?P<url>https?://\S+)\s*"
    r"\|\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$"
)

GAP_EXCUSE = ("不适用", "无此项", "无需披露")

# 计量模式：只有披露说了算。活跃市场是公允价值模式的一个条件，不是它本身。
MODE_WORDS = ("成本模式", "公允价值模式")
MODE_EQUIV = {
    "成本模式": ("成本模式", "成本计量", "成本法"),
    "公允价值模式": ("公允价值模式", "公允价值计量", "以公允价值"),
}
ACTIVE_MARKET = ("活跃市场", "活跃交易")

# 转换差额的去向：准则定方向，金额与去向只有披露知道。
DEST_OCI = ("其他综合收益",)
DEST_PL = ("当期损益",)

QUOTE = re.compile(r"「[^」]*」")
ANCHOR_BLOCK = re.compile(r"〔\s*锚\s*[:：][^〕]*〕")
NUM = re.compile(r"\d[\d,]*\.?\d*\s*(?:万元|亿元|元|%)")
LABEL_CUT = re.compile(r"[：:\s]")


# ---------------------------------------------------------------- 埋点

def mark_first_run():
    """首次运行埋点：落一枚空文件，任何失败都静默，不改退码。"""
    try:
        day = datetime.date.today().isoformat()
        d = os.path.join(os.path.expanduser("~"), ".cue-usage")
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "%s-%s" % (SLUG, day)), "a").close()
    except Exception:
        pass


# ---------------------------------------------------------------- 行判别

def _split_label(line):
    """项名与正文的界：`：`／`:`／空白里**最早出现**的那个。

    只按冒号切会把空格式项名整段当正文，好样里几条就红几条。
    """
    s = line.strip()
    if s.startswith("- "):
        s = s[2:].strip()
    cuts = [m.start() for m in LABEL_CUT.finditer(s)]
    if not cuts:
        return s, ""
    i = min(cuts)
    return s[:i].strip(), s[i + 1:].strip()


def _quotes(line):
    return "".join(QUOTE.findall(line))


def _strip_quotes(line):
    return ANCHOR_BLOCK.sub("", QUOTE.sub("", line))


def _is_gap_line(s):
    """只认两种登记形：行首 `未取到`，或 `项名：未取到…`。口径行不在其列。"""
    s = s.strip()
    if s.startswith("- "):
        s = s[2:].strip()
    if s.startswith("未取到"):
        return True
    return re.match(r"^[^：:]{1,16}[：:]\s*未取到", s) is not None


def _is_finding_line(s):
    """发现行 = 以 `- ` 开头、不是主体／报告期、也不是纯自标行。"""
    s = s.strip()
    if not s.startswith("- "):
        return False
    if SUBJECT.match(s) or PERIOD.match(s):
        return False
    body = s[2:].strip()
    if not body:
        return False
    rest = body
    for mark in MARK_TEXTS:
        rest = rest.replace(mark, "")
    return bool(rest.strip())


def split_doc(text):
    """→ (头部行, [(节名, 标题行号, [(行号, 行文本)])])"""
    header = []
    sections = []
    cur = None
    for lineno, raw in enumerate(text.splitlines(), 1):
        m = HEADING.match(raw)
        if m:
            name = NUMBERING.sub("", m.group(1)).strip()
            cur = [name, lineno, []]
            sections.append(cur)
        elif cur is None:
            header.append((lineno, raw))
        else:
            cur[2].append((lineno, raw))
    return header, sections


# ---------------------------------------------------------------- IP-STRUCT

def _check_struct(header, sections, add):
    htext = "\n".join(s for _ln, s in header)
    for mark in MARK_TEXTS:
        if mark not in htext:
            add("IP-STRUCT", 1, "头部缺自标「%s」：起草稿须自报身份与边界" % mark)
    if not any(SUBJECT.match(s.strip()) for _ln, s in header):
        add("IP-STRUCT", 1, "头部缺 `- 主体：…` 一行：主体不定，后面每个数都落不到人头上")
    if not any(PERIOD.match(s.strip()) for _ln, s in header):
        add("IP-STRUCT", 1, "头部缺 `- 报告期：…` 一行")

    seen = set()
    for name, lineno, _body in sections:
        if name in seen:
            add("IP-STRUCT", lineno, "节「%s」重复出现：七节各占一节，多出的同名节会让节内发现行归属不清" % name)
        seen.add(name)
        if name not in ALL_SECTIONS:
            add("IP-STRUCT", lineno, "不认识的节名「%s」：本件只认七个节，多出的节里的发现行不被判" % name[:20])

    names = [n for n, _l, _b in sections]
    if names != list(ALL_SECTIONS):
        missing = [s for s in ALL_SECTIONS if s not in names]
        if missing:
            add("IP-STRUCT", 1, "缺节：%s —— 七节须齐（五块内容 + %s + %s）"
                % ("、".join("「%s」" % s for s in missing), GAP_SECTION, SOURCE_SECTION))
        else:
            add("IP-STRUCT", 1, "七节顺序不对：应为 %s，实为 %s"
                % ("／".join(ALL_SECTIONS), "／".join(names)))

    for name in SECTIONS:
        body = next((b for n, _l, b in sections if n == name), None)
        if body is None:
            continue
        if not any(_is_finding_line(s) for _ln, s in body):
            lineno = next((l for n, l, _b in sections if n == name), 1)
            add("IP-STRUCT", lineno, "「%s」节只有小标题、没有发现行：这一块要逐条登记" % name)

    for name in (GAP_SECTION, SOURCE_SECTION):
        if not any(s.strip() for _ln, s in next((b for n, _l, b in sections if n == name), [])):
            lineno = next((l for n, l, _b in sections if n == name), 1)
            add("IP-STRUCT", lineno, "「%s」节是空的：这一节要么登记缺口、要么登记来源，不能留白" % name)


# ---------------------------------------------------------------- IP-QUOTE

def _check_quote(sections, add):
    registered = set()
    has_source_section = any(n == SOURCE_SECTION for n, _l, _b in sections)
    for name, _l, body in sections:
        if name != SOURCE_SECTION:
            continue
        for lineno, raw in body:
            s = raw.strip()
            if not s.startswith("- "):
                continue
            m = SOURCE_LINE.match(s)
            if m:
                registered.add(m.group("s"))
            else:
                add("IP-QUOTE", lineno,
                    "来源行格式不对：须写 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD | 类型：…`：%s"
                    % s[:40])

    for name, _l, body in sections:
        if name not in SECTIONS:
            continue
        for lineno, raw in body:
            s = raw.strip()
            if not _is_finding_line(s):
                continue
            if _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s:
                continue
            if not TRIPLE.search(s):
                add("IP-QUOTE", lineno,
                    "发现行没有以「原句」〔锚：…〕[S#] 收尾：%s" % s[:44])
                continue
            m = REF_TAIL.search(s)
            if m and has_source_section and m.group(1) not in registered:
                add("IP-QUOTE", lineno,
                    "引用了未登记的 [%s]：来源节里没有这一号" % m.group(1))

    if has_source_section and not registered:
        add("IP-QUOTE", 1, "来源节一条来源行都没有：每个 [S#] 都要有可点 URL 与检索日")


# ---------------------------------------------------------------- IP-NOSELF

def _check_mode(lineno, line, add):
    """计量模式只认披露写法：原句里没有这个词、也没有等价表述，就发。"""
    label, body = _split_label(line)
    own = _strip_quotes(body)
    q = _quotes(line)
    for word in MODE_WORDS:
        if word in q:
            continue                      # 原句自己写了，最硬的一档
        if not (word in own or word in label):
            continue
        if any(eq in q for eq in MODE_EQUIV[word]):
            continue                      # 原句用了等价表述
        if word == "公允价值模式" and any(w in (label + own) for w in ACTIVE_MARKET) \
                and not any(w in q for w in ACTIVE_MARKET):
            add("IP-NOSELF", lineno,
                "「%s」推断自「存在活跃市场」：活跃市场只是公允价值模式的一个条件，"
                "不等于披露已采用该模式——原句里没有「公允价值模式」或其等价表述" % label[:16])
        else:
            add("IP-NOSELF", lineno,
                "「%s」的原句里没有「%s」或其等价表述：计量模式只有披露说了算，"
                "不按常识或同业惯例补" % (label[:16], word))


def _check_transfer_dest(lineno, line, add):
    """转换差额的去向与金额必须与本行原句一致。"""
    label, body = _split_label(line)
    own = _strip_quotes(body)
    if not own.strip():
        return
    is_transfer = "转换" in (label + own) or "转入" in (label + own) or "转出" in (label + own)
    has_diff = "差额" in (label + own) or NUM.search(own)
    if not is_transfer or not has_diff:
        return
    q = _quotes(line)
    said_oci = any(w in own for w in DEST_OCI)
    said_pl = any(w in own for w in DEST_PL)
    if not (said_oci or said_pl):
        if NUM.search(own) and "差额" in own:
            add("IP-NOSELF", lineno,
                "「%s」写了转换差额金额却没写去向：差额进其他综合收益还是当期损益，"
                "只有披露知道，不许默认其一" % label[:16])
        return
    for dest, words in (("其他综合收益", DEST_OCI), ("当期损益", DEST_PL)):
        if not any(w in own for w in words):
            continue
        if not any(w in q for w in words):
            add("IP-NOSELF", lineno,
                "「%s」的去向写作「%s」，原句里没有这个去向：去向照抄披露，不由本件按准则方向补"
                % (label[:16], dest))


def _check_noself(sections, add):
    for name, _l, body in sections:
        if name not in SECTIONS:
            continue
        for lineno, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_gap_line(s):
                continue
            _check_mode(lineno, s, add)
            _check_transfer_dest(lineno, s, add)


# ---------------------------------------------------------------- IP-GAP

NO_GAP = re.compile(r"^-\s*未取到\s*[：:]\s*无\s*$")


def _gap_key(s):
    """缺口点名的键：`项名：未取到…` 取项名；`未取到：项名——说明` 取冒号后到破折号前。"""
    s = s.strip()
    if s.startswith("- "):
        s = s[2:].strip()
    i = s.find("未取到")
    if i < 0:
        return ""
    head = s[:i].strip().rstrip("：: ").strip()
    if head:
        return head[:12]
    tail = re.sub(r"^[：:\s]+", "", s[i + 3:]).strip()
    for mark in ("——", "—", "｜", "|", "：", ":"):
        j = tail.find(mark)
        if j > 0:
            tail = tail[:j].strip()
            break
    return tail[:12]


def _check_gap(sections, add):
    body_keys = []
    for name, _l, body in sections:
        if name not in SECTIONS:
            continue
        for lineno, raw in body:
            s = raw.strip()
            if _is_gap_line(s) and not NO_GAP.match(s):
                body_keys.append((lineno, _gap_key(s)))

    gap_keys = []
    no_gap_decl = False
    for name, _l, body in sections:
        if name != GAP_SECTION:
            continue
        for lineno, raw in body:
            s = raw.strip()
            if not s.startswith("- "):
                continue
            if NO_GAP.match(s):
                no_gap_decl = True
            elif _is_gap_line(s):
                gap_keys.append((lineno, _gap_key(s)))

    a = {k for _ln, k in body_keys}
    b = {k for _ln, k in gap_keys}
    for lineno, k in body_keys:
        if k and k not in b:
            add("IP-GAP", lineno,
                "正文点名了「%s」的未取到，第六节没有登记：两向对账，缺一头就发" % k)
    for lineno, k in gap_keys:
        if k and k not in a:
            add("IP-GAP", lineno,
                "第六节登记了「%s」的未取到，正文里没有这一条：要么补正文，要么撤掉登记" % k)
    if not body_keys and not gap_keys and not no_gap_decl:
        add("IP-GAP", 1,
            "全文没有一条未取到，第六节也没写「未取到：无」：零缺口须显式声明，不能留白")

    for name, _l, body in sections:
        for lineno, raw in body:
            s = raw.strip()
            if not s.startswith("- ") or _is_gap_line(s):
                continue
            for w in GAP_EXCUSE:
                if w in _strip_quotes(s):
                    add("IP-GAP", lineno,
                        "「%s」用了「%s」搪塞：缺口要写未取到并说明缺什么，这三句都是免责话术"
                        % (_split_label(s)[0][:16], w))
                    break


# ---------------------------------------------------------------- IP-LINE

# 红线词表：裸「卖出」「买入」不收——投资性房地产的处置登记本来就写「本期出售办公楼
# 取得价款」，那是披露原文式的正常登记语言，当禁词会把该绿的行判红。收的是**评级语言**
# 的整段写法（卖出评级／给予买入…）。「增持」「减持」留着：财报登记语境里几乎不自然出现。
HARD_BAN = (
    "处置建议", "建议处置", "建议出售", "目标价", "评级", "增持",
    "减持", "估值结论", "评估结论", "公允价值将上涨", "预计升值", "值得投资",
    "低估", "高估",
    "卖出评级", "买入评级", "增持评级", "减持评级",
    "给予买入", "给予卖出", "强烈推荐", "跑赢大盘",
)
# 说明性小节的节名里会正当地写出这些词，整节跳过
BAN_EXEMPT_SECTION = ("红线", "机检")


def _check_line(sections, add):
    for name, _l, body in sections:
        if any(w in name for w in BAN_EXEMPT_SECTION):
            continue
        for lineno, raw in body:
            s = raw.strip()
            if not s.startswith("- "):
                continue
            own = _strip_quotes(s)
            for w in HARD_BAN:
                if w in own:
                    add("IP-LINE", lineno,
                        "「%s」踩了红线词「%s」：处置与否、公允价值涨跌、评估机构好坏、"
                        "评级与目标价都不是本件的判项——%s" % (_split_label(s)[0][:16], w, s[:40]))
                    break


# ---------------------------------------------------------------- 总装

def check_text(text):
    """返回 [(码, 行号, 说明), ...]。"""
    findings = []
    header, sections = split_doc(text)

    def add(code, lineno, msg):
        findings.append((code, lineno, msg))

    _check_struct(header, sections, add)
    _check_quote(sections, add)
    _check_noself(sections, add)
    _check_gap(sections, add)
    _check_line(sections, add)
    return findings


# ---------------------------------------------------------------- 内置夹具

GOOD = """# 投资性房地产·逐条挂源（样例）

- 主体：示例股份有限公司
- 报告期：2025 年度
- 〔AI 起草〕〔须与原句核对〕〔非投资建议〕〔待人工〕

## 一、投资性房地产概况

- 期末账面价值：8,600.00 万元「投资性房地产期末账面价值 86,000,000.00 元」〔锚：2025 年年报·第 96 页·附注五·投资性房地产〕[S1]
- 期初账面价值：7,900.00 万元「投资性房地产期初账面价值 79,000,000.00 元」〔锚：2025 年年报·第 96 页·附注五·投资性房地产〕[S1]

## 二、计量模式

- 计量模式：成本模式「本公司投资性房地产采用成本模式进行后续计量」〔锚：2025 年年报·第 96 页·附注五·投资性房地产〕[S1]
- 模式是否变更：否「本报告期投资性房地产的计量模式未发生变更」〔锚：2025 年年报·第 96 页·附注五·投资性房地产〕[S1]

## 三、成本模式明细

- 原值：11,200.00 万元「投资性房地产原值 112,000,000.00 元」〔锚：2025 年年报·第 96 页·附注五·投资性房地产〕[S1]
- 累计折旧：2,600.00 万元「累计折旧 26,000,000.00 元」〔锚：2025 年年报·第 96 页·附注五·投资性房地产〕[S1]

## 四、公允价值模式明细

- 期初公允价值：未取到：本报告期采用成本模式，附注未披露公允价值
- 期末公允价值：未取到：本报告期采用成本模式，附注未披露公允价值

## 五、转换与处置

- 自用转投资性房地产：未取到：本报告期无自用房地产转入投资性房地产
- 本期处置损益：未取到：本报告期未处置投资性房地产

## 六、口径与未取到

- 口径：计量模式只认披露写法，不按「有活跃市场」推定
- 口径：转换差额的去向照抄披露，不二选一猜
- 未取到：期初公允价值——成本模式下附注未披露公允价值
- 未取到：期末公允价值——同上
- 未取到：自用转投资性房地产——本报告期无转入
- 未取到：本期处置损益——本报告期未处置

## 七、来源

- [S1] 示例股份有限公司 2025 年年度报告 | https://example.com/annual-2025.pdf | 检索日 2026-11-13 | 类型：年报
"""


def _without_section(text, name):
    keep = []
    skip = False
    for line in text.splitlines():
        if line.startswith("## "):
            skip = NUMBERING.sub("", line[3:]).strip() == name
        if not skip:
            keep.append(line)
    return "\n".join(keep) + "\n"


BAD_STRUCT = _without_section(GOOD, "成本模式明细")

BAD_QUOTE = GOOD.replace(
    "- 原值：11,200.00 万元「投资性房地产原值 112,000,000.00 元」"
    "〔锚：2025 年年报·第 96 页·附注五·投资性房地产〕[S1]",
    "- 原值：11,200.00 万元",
)

# 反证一：因「存在活跃市场」推成公允价值模式，原句里没有「公允价值模式」
BAD_MODE_GUESS = GOOD.replace(
    "- 计量模式：成本模式「本公司投资性房地产采用成本模式进行后续计量」"
    "〔锚：2025 年年报·第 96 页·附注五·投资性房地产〕[S1]",
    "- 计量模式：公允价值模式「本公司所在地已存在活跃市场」"
    "〔锚：2025 年年报·第 96 页·附注五·投资性房地产〕[S1]",
)

UNREGISTER_TRANSFER = "- 未取到：自用转投资性房地产——本报告期无转入\n"

# 反证二：写了转换差额金额，却没写去向
BAD_DIFF_NO_DEST = GOOD.replace(
    "- 自用转投资性房地产：未取到：本报告期无自用房地产转入投资性房地产",
    "- 自用转投资性房地产：转换差额 320.00 万元「自用房地产于转换日转为本公司投资性房地产」"
    "〔锚：2025 年年报·第 97 页·附注五·投资性房地产〕[S1]",
).replace(UNREGISTER_TRANSFER, "")

# 反证三：去向写了，原句里没有这个去向
BAD_DEST_GUESS = GOOD.replace(
    "- 自用转投资性房地产：未取到：本报告期无自用房地产转入投资性房地产",
    "- 自用转投资性房地产：转换差额 320.00 万元计入当期损益"
    "「自用房地产于转换日转为本公司投资性房地产，转换日公允价值大于账面价值的差额"
    "计入其他综合收益」〔锚：2025 年年报·第 97 页·附注五·投资性房地产〕[S1]",
).replace(UNREGISTER_TRANSFER, "")

# 反证四：原句自己的去向写对了，不误伤
OK_DEST_QUOTED = GOOD.replace(
    "- 自用转投资性房地产：未取到：本报告期无自用房地产转入投资性房地产",
    "- 自用转投资性房地产：转换差额 320.00 万元计入其他综合收益"
    "「自用房地产于转换日转为本公司投资性房地产，转换日公允价值大于账面价值的差额"
    "计入其他综合收益」〔锚：2025 年年报·第 97 页·附注五·投资性房地产〕[S1]",
).replace(UNREGISTER_TRANSFER, "")

# 缺口两向不对账：正文多了一条没在第六节登记
BAD_GAP_ONE_WAY = GOOD.replace(
    "- 累计折旧：2,600.00 万元「累计折旧 26,000,000.00 元」"
    "〔锚：2025 年年报·第 96 页·附注五·投资性房地产〕[S1]",
    "- 累计折旧：2,600.00 万元「累计折旧 26,000,000.00 元」"
    "〔锚：2025 年年报·第 96 页·附注五·投资性房地产〕[S1]\n"
    "- 减值准备：未取到：附注未单列投资性房地产减值准备",
)

# 零缺口反证：全文没有未取到，第六节显式写「未取到：无」
ZERO_GAP = GOOD.replace(
    "- 期初公允价值：未取到：本报告期采用成本模式，附注未披露公允价值",
    "- 期初公允价值：成本模式下不披露「本公司投资性房地产采用成本模式进行后续计量」"
    "〔锚：2025 年年报·第 96 页·附注五·投资性房地产〕[S1]",
).replace(
    "- 期末公允价值：未取到：本报告期采用成本模式，附注未披露公允价值",
    "- 期末公允价值：成本模式下不披露「本公司投资性房地产采用成本模式进行后续计量」"
    "〔锚：2025 年年报·第 96 页·附注五·投资性房地产〕[S1]",
).replace(
    "- 自用转投资性房地产：未取到：本报告期无自用房地产转入投资性房地产",
    "- 自用转投资性房地产：无「本报告期无自用房地产转入投资性房地产」"
    "〔锚：2025 年年报·第 97 页·附注五·投资性房地产〕[S1]",
).replace(
    "- 本期处置损益：未取到：本报告期未处置投资性房地产",
    "- 本期处置损益：无「本报告期未处置投资性房地产」"
    "〔锚：2025 年年报·第 97 页·附注五·投资性房地产〕[S1]",
).replace(
    "- 未取到：期初公允价值——成本模式下附注未披露公允价值\n"
    "- 未取到：期末公允价值——同上\n"
    "- 未取到：自用转投资性房地产——本报告期无转入\n"
    "- 未取到：本期处置损益——本报告期未处置",
    "- 未取到：无",
)

# 红线：正文里写了处置建议
BAD_REDLINE = GOOD.replace(
    "- 原值：11,200.00 万元「投资性房地产原值 112,000,000.00 元」",
    "- 原值：11,200.00 万元，建议处置该物业「投资性房地产原值 112,000,000.00 元」",
)

# 红线反证：禁词只出现在「」原句里，不是本件在判断
OK_REDLINE_QUOTED = GOOD.replace(
    "- 原值：11,200.00 万元「投资性房地产原值 112,000,000.00 元」",
    "- 原值：11,200.00 万元「投资性房地产原值 112,000,000.00 元，"
    "评估机构给出的目标价为 130,000,000.00 元」",
)

DEMO = GOOD


def _codes(findings):
    return sorted({c for c, _l, _m in findings})


# ---------------------------------------------------------------- 自测

CASES = (
    ("好样零发条", GOOD, ()),
    ("缺一节（坏样）", BAD_STRUCT, ("IP-STRUCT",)),
    ("发现行没挂原句（坏样）", BAD_QUOTE, ("IP-QUOTE",)),
    ("活跃市场推成公允价值（坏样）", BAD_MODE_GUESS, ("IP-NOSELF",)),
    ("差额写了没写去向（坏样）", BAD_DIFF_NO_DEST, ("IP-NOSELF",)),
    ("去向与原句相反（坏样）", BAD_DEST_GUESS, ("IP-NOSELF",)),
    ("去向照抄原句（反证）", OK_DEST_QUOTED, ()),
    ("缺口两向不对账（坏样）", BAD_GAP_ONE_WAY, ("IP-GAP",)),
    ("零缺口显式声明（反证）", ZERO_GAP, ()),
    ("正文写了处置建议（坏样）", BAD_REDLINE, ("IP-LINE",)),
    ("禁词只在原句里（反证）", OK_REDLINE_QUOTED, ()),
)


def selftest():
    bad = 0
    unknown = 0
    print("── 自测 ──")
    for name, text, expect in CASES:
        try:
            findings = check_text(text)
        except Exception as exc:
            unknown += 1
            print("  %-22s 不可判：%s" % (name, exc))
            continue
        got = tuple(_codes(findings))
        ok = set(got) == set(expect)
        if not ok:
            bad += 1
        print("  %-22s 码=%s 条数=%d %s"
              % (name, ",".join(got) or "无", len(findings), "OK" if ok else "不合"))
    print("自测档数=%d｜不合=%d｜不可判=%d" % (len(CASES), bad, unknown))
    return 0 if (bad == 0 and unknown == 0) else 1


# ---------------------------------------------------------------- 主入口

def main(argv):
    if len(argv) != 2:
        sys.stderr.write(USAGE)
        return 2
    arg = argv[1]
    if arg in ("-h", "--help"):
        sys.stdout.write(USAGE)
        return 0
    mark_first_run()
    if arg == "--demo":
        sys.stdout.write(DEMO)
        return 0
    if arg == "--selftest":
        return selftest()
    try:
        text = open(arg, encoding="utf-8").read()
    except OSError as exc:
        sys.stderr.write("读不到文件：%s\n" % exc)
        return 3
    if not text.strip():
        sys.stderr.write("空稿：%s\n" % arg)
        return 3
    findings = check_text(text)
    if not findings:
        print("%s 结论：五道全过（零发条）" % arg)
        return 0
    for code, lineno, msg in sorted(findings, key=lambda x: (x[1], x[0])):
        print("  %s L%d %s" % (code, lineno, msg))
    print("%s 结论：有发条 %d 条" % (arg, len(findings)))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
