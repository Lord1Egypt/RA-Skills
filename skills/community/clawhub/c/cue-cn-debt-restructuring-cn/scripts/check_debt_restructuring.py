#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cn-debt-restructuring-cn —— 债务重组逐条挂源的五道机检（零网络）。

五道（全部实装）：
  DR-STRUCT  形制     头部四件自标、主体／报告期、七节齐且有序、前五节各有发现行、
                      六七节不得留白
  DR-QUOTE   原句与锚 每条发现行以「原句」〔锚：…〕[S#] 收尾；来源行带 URL 与检索日；
                      引用的 [S#] 须已在来源节登记
  DR-MODE    重组方式 四条路（以资产清偿／债转股／修改其他条款／组合）须明写；两条路混在
                      一行而未标组合即发；方式一条都没登记也发
  DR-GAP     两向点名 正文与第六节互相对账；零缺口须显式写「未取到：无」；禁搪塞词
  DR-LINE    红线     处置与偿债建议、重组损益预测、评级与目标价、确定性断言零命中

退码：0 五道全过 / 1 有发条 / 2 用法错 / 3 读不到文件或空稿。

UNIMPLEMENTED 现为空元组：五道全部实装。往后若再加判据，尚未实装的道登记在那里，
自测逐条报「不可判」并按 3 收场——**不提前宣布它们实装了**。
"""

from __future__ import annotations

import datetime
import os
import re
import sys

SLUG = "cue-cn-debt-restructuring-cn"
CODES = ("DR-STRUCT", "DR-QUOTE", "DR-MODE", "DR-GAP", "DR-LINE")
UNIMPLEMENTED = ()

SECTIONS = (
    "债务重组概况",
    "重组方式",
    "以资产清偿债务",
    "债转股",
    "修改其他条款",
)
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"
ALL_SECTIONS = SECTIONS + (GAP_SECTION, SOURCE_SECTION)
CONTENT_COUNT = len(SECTIONS)

USAGE = """usage: check_debt_restructuring.py <稿.md>
       check_debt_restructuring.py --selftest
       check_debt_restructuring.py --demo

债务重组逐条挂源的五道机检（零网络）：
  DR-STRUCT 形制 / DR-QUOTE 原句与锚 / DR-MODE 重组方式口径 /
  DR-GAP 未取到两向点名 / DR-LINE 红线
退码：0 五道全过 / 1 有发条 / 2 用法错 / 3 读不到文件或空稿
"""

MARK_TEXTS = ("〔AI 整理初稿〕", "〔请回原文核对〕", "〔不构成投资建议〕", "[待人工]")

HEADING = re.compile(r"^##\s+(\S.*?)\s*$")
NUMBERING = re.compile(r"^[一二三四五六七八九十]+、\s*")
SUBJECT = re.compile(r"^-\s*主体[：:]\s*\S")
PERIOD = re.compile(r"^-\s*报告期[：:]\s*\S")

QUOTE = re.compile(r"「[^」]*」")
ANCHOR_BLOCK = re.compile(r"〔\s*锚\s*[:：][^〕]*〕")
TRIPLE = re.compile(r"「[^」]*」\s*〔\s*锚\s*[:：][^〕]*〕\s*\[S\d+\]\s*$")
ANCHOR_ANY = re.compile(r"〔\s*锚\s*[:：][^〕]*〕")
REF_TAIL = re.compile(r"\[(S\d+)\]\s*$")
REF_ANY = re.compile(r"\[S\d+\]")
SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)\|\s*(?P<url>https?://\S+)\s*"
    r"\|\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$"
)


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
    """项名与正文的界：`：`／`:`／空白里最早出现的那个（空格式项名不许整段当正文）。"""
    s = line.strip()
    if s.startswith("- "):
        s = s[2:].strip()
    cuts = [m.start() for m in re.finditer(r"[：:\s]", s)]
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


# ---------------------------------------------------------------- DR-STRUCT

def _check_struct(header, sections, add):
    htext = "\n".join(s for _ln, s in header)
    for mark in MARK_TEXTS:
        if mark not in htext:
            add("DR-STRUCT", 1, "头部缺自标「%s」：起草稿须自报身份、边界与判断位" % mark)
    if not any(SUBJECT.match(s.strip()) for _ln, s in header):
        add("DR-STRUCT", 1, "头部缺 `- 主体：…` 一行：主体不定，重组损益落不到人头上")
    if not any(PERIOD.match(s.strip()) for _ln, s in header):
        add("DR-STRUCT", 1, "头部缺 `- 报告期：…` 一行")

    seen = set()
    for name, lineno, _body in sections:
        if name in seen:
            add("DR-STRUCT", lineno,
                "节「%s」重复出现：七节各占一节，多出的同名节会让节内发现行归属不清" % name)
        seen.add(name)
        if name not in ALL_SECTIONS:
            add("DR-STRUCT", lineno,
                "不认识的节名「%s」：本件只认七个节，多出的节里的发现行不被判" % name[:20])

    names = [n for n, _l, _b in sections]
    if names != list(ALL_SECTIONS):
        missing = [s for s in ALL_SECTIONS if s not in names]
        if missing:
            add("DR-STRUCT", 1, "缺节：%s —— 七节须齐（五块内容 + %s + %s）"
                % ("、".join("「%s」" % s for s in missing), GAP_SECTION, SOURCE_SECTION))
        else:
            add("DR-STRUCT", 1, "七节顺序不对：应为 %s，实为 %s"
                % ("／".join(ALL_SECTIONS), "／".join(names)))

    for name in SECTIONS:
        body = next((b for n, _l, b in sections if n == name), None)
        if body is None:
            continue
        if not any(_is_finding_line(s) for _ln, s in body):
            lineno = next((l for n, l, _b in sections if n == name), 1)
            add("DR-STRUCT", lineno, "「%s」节只有小标题、没有发现行：这一块要逐条登记" % name)

    for name in (GAP_SECTION, SOURCE_SECTION):
        body = next((b for n, _l, b in sections if n == name), None)
        if body is None:
            continue
        if not any(s.strip() for _ln, s in body):
            lineno = next((l for n, l, _b in sections if n == name), 1)
            add("DR-STRUCT", lineno,
                "「%s」节是空的：这一节要么登记缺口、要么登记来源，不能留白" % name)


# ---------------------------------------------------------------- DR-QUOTE

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
                add("DR-QUOTE", lineno,
                    "来源行格式不对：须写 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD | 类型：…`，"
                    "URL 须 http 开头、检索日须 YYYY-MM-DD：%s" % s[:44])

    for name, _l, body in sections:
        if name not in SECTIONS:
            continue
        for lineno, raw in body:
            s = raw.strip()
            if not _is_finding_line(s):
                continue
            if _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s:
                continue
            if TRIPLE.search(s):
                m = REF_TAIL.search(s)
                if m and has_source_section and m.group(1) not in registered:
                    add("DR-QUOTE", lineno,
                        "引用了未登记的 [%s]：来源节里没有这一号" % m.group(1))
                continue
            miss = []
            if not QUOTE.search(s):
                miss.append("「」原句")
            if not ANCHOR_ANY.search(s):
                miss.append("〔锚：…〕")
            if not REF_ANY.search(s):
                miss.append("[S#]")
            add("DR-QUOTE", lineno,
                "发现行缺 %s：每条发现行须以「原句」〔锚：…〕[S#] 收尾——%s"
                % ("、".join(miss) if miss else "三元组", s[:44]))

    if has_source_section and not registered:
        add("DR-QUOTE", 1, "来源节一条合规来源行都没有：每个 [S#] 都要有可点 URL 与检索日")


# 债务重组四条路，四种账务处理完全不同，混着写就是错账。
PATH_ASSET = ("以资产清偿", "以资产抵偿", "以非现金资产清偿")
PATH_EQUITY = ("债转股", "转为权益工具", "转为股权", "转增股本")
PATH_TERMS = ("修改其他条款", "修改债务条款", "延期", "降息", "减免本金", "豁免部分本金")
PATH_MIXED = ("组合",)


# ---------------------------------------------------------------- DR-MODE

def _paths_in(s):
    """这一行点了哪几条路（返回路径名集合）。"""
    hit = set()
    if any(w in s for w in PATH_ASSET):
        hit.add("以资产清偿债务")
    if any(w in s for w in PATH_EQUITY):
        hit.add("债转股")
    if any(w in s for w in PATH_TERMS):
        hit.add("修改其他条款")
    return hit


def _check_mode(sections, add):
    mode_name = SECTIONS[1]                       # 重组方式
    doc_paths = set()
    mode_lines = []

    for name, _l, body in sections:
        if name not in SECTIONS:
            continue
        for lineno, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_gap_line(s):
                continue
            label, _rest = _split_label(s)
            own = _strip_quotes(s)
            # 判域只看「项名 + 洗掉引文后的正文」：引文里出现「债转股」是披露在说
            # 「本次不涉及债转股」，不是本件在登记这条路。
            hit = _paths_in(label + own)
            doc_paths |= hit
            if name == mode_name:
                mode_lines.append((lineno, label, hit, own))

            # 乙：两条互斥路径混在同一行，且没标组合
            if len(hit) >= 2 and not any(w in (label + own) for w in PATH_MIXED):
                add("DR-MODE", lineno,
                    "「%s」把「%s」两种重组方式混在一行且未标组合：组合方式须明写「组合」，"
                    "否则两条路各自的账务处理分不清"
                    % (label[:16], "＋".join(sorted(hit))))

    # 甲：整份稿前五节一条路都没登记（四条路名一个没有、也没明示组合）
    # 「是否组合方式：否」这类否定行不算明示组合——它恰恰是在说「不是组合」。
    declared_mixed = any(
        any(w in own for w in PATH_MIXED) and not label.startswith("是否")
        for _ln, label, _h, own in mode_lines
    )
    if mode_lines and not doc_paths and not declared_mixed:
        lineno = mode_lines[0][0]
        add("DR-MODE", lineno,
            "重组方式未登记：四条路（以资产清偿债务／债转股／修改其他条款／组合方式）"
            "一条都没写，四种账务处理各不相同，不许含混")


# ---------------------------------------------------------------- DR-GAP

# 缺口搪塞词：把「没查到」写成「没有」。
GAP_EXCUSE = ("不适用", "无此项", "无需披露")


def _is_zero_gap(s):
    """零缺口登记行：`未取到：无`。它不是一条缺口，别算进两向对账。"""
    return "未取到：无" in s or "未取到:无" in s


def _gap_key(line):
    """从一条「未取到」里取出被点名的那一项，两向对账用同一个取法。

    本件两种合法写法，取法要对两种都成立：
      正文 `- 项名：未取到：原因`  → 项名在「未取到」**前**
      第六节 `- 未取到：项名`      → 项名在「未取到」**后**
    先看前面有没有项名（剥掉行首 `- `、去掉尾随冒号），有就用它；没有才取冒号之后那一段。
    """
    head = re.sub(r"^-\s*", "", line.split("未取到", 1)[0]).strip().rstrip("：:，,。；; ")
    if head:
        return head[:12]
    rest = line.split("未取到", 1)[1].lstrip()
    m = re.match(r"^[：:]\s*(.+)$", rest)
    if m:
        rest = m.group(1)
    return re.split(r"[：:，,。；;｜——]", rest.strip())[0].strip()[:12]


def _check_gap(sections, add):
    body_gaps = []      # 正文五节里的「未取到」登记行
    gap_sec = []        # 第六节的缺口点名行
    gap_text = []       # 第六节全文，零缺口判据要看它

    for name, _l, body in sections:
        for lineno, raw in body:
            s = raw.strip()
            if not s:
                continue
            # 丁：搪塞词（引文里不算本件在说）
            own = _strip_quotes(s)
            for w in GAP_EXCUSE:
                if w in own:
                    add("DR-GAP", lineno,
                        "「%s」用了「%s」搪塞：缺口要写未取到并说明缺什么，"
                        "这三句都是免责话术" % (_split_label(s)[0][:16], w))
                    break
            if not _is_gap_line(s) or _is_zero_gap(s):
                if name == GAP_SECTION:
                    gap_text.append(s)
                continue
            if name in SECTIONS:
                body_gaps.append((lineno, s))
            elif name == GAP_SECTION:
                gap_sec.append((lineno, s))
        if name == GAP_SECTION:
            gap_text.extend(s for _ln, s in body)

    # 甲：正文写了未取到，第六节没点名
    for lineno, s in body_gaps:
        key = _gap_key(s)
        if key and not any(key in g for _ln, g in gap_sec):
            add("DR-GAP", lineno,
                "正文写了未取到「%s」，第六节没点名：两向对账，缺一头就发" % key)
    # 乙：第六节点名的一项，正文找不到落点
    for lineno, g in gap_sec:
        key = _gap_key(g)
        if key and not any(key in s for _ln, s in body_gaps):
            add("DR-GAP", lineno,
                "第六节点名了「%s」，正文没有这条表述：要么补正文，要么撤掉登记" % key)
    # 丙：零缺口须显式写「未取到：无」
    if not body_gaps and not gap_sec and not gap_text:
        add("DR-GAP", 1, "零缺口未显式写「未取到：无」：缺口为零也要在第六节写明，不能留白")
    elif not body_gaps and not gap_sec and not any(_is_zero_gap(x) for x in gap_text):
        add("DR-GAP", 1, "零缺口未显式写「未取到：无」：缺口为零也要在第六节写明，不能留白")


# ---------------------------------------------------------------- DR-LINE

# 红线四族。甲处置与偿债建议／乙重组损益预测／丙评级与目标价／丁确定性断言。
# 「债务重组」「重组损益」「债转股」这类正常术语不在表内——那是本件的登记对象。
HARD_BAN = (
    # 甲 处置与偿债建议
    "建议处置", "应当处置", "建议出售", "建议清偿", "宜尽早", "建议豁免",
    # 乙 重组损益预测
    "预计重组收益", "预计重组损益", "预计增厚", "将增厚利润", "预计扭亏",
    # 丙 评级与目标价（只收评级语言，不收裸动词——裸「买入／卖出／增持／减持」当普通
    #     动词用时是合法登记语言：「本期以出售设备清偿债务」是披露原文，不是评级意见）
    "评级", "目标价", "目标市值", "值得投资", "低估", "高估",
    "买入评级", "卖出评级", "增持评级", "减持评级", "给予买入", "给予卖出",
    "强烈推荐", "跑赢大盘",
    # 丁 确定性断言（收断言收益，不收裸「必然」——「必然导致…」可以是准则叙述）
    "稳赚", "零风险", "保证收益", "必然盈利", "必然上涨", "必然受益", "包赚",
)
# 这两节本来就在说该禁什么，判它等于自伤
LINE_EXEMPT_SECTION = ("合规红线", "数据通道")


def _check_line(sections, add):
    for name, _l, body in sections:
        if any(w in name for w in LINE_EXEMPT_SECTION):
            continue
        for lineno, raw in body:
            s = raw.strip()
            if not s.startswith("- "):
                continue
            own = _strip_quotes(s)
            for w in HARD_BAN:
                if w in own:
                    add("DR-LINE", lineno,
                        "「%s」踩了红线词「%s」：该不该重组、重组能带来多少损益、"
                        "评级与目标价都不是本件的判项——%s"
                        % (_split_label(s)[0][:16], w, s[:40]))
                    break


# ---------------------------------------------------------------- 总装

def check_text(text):
    """返回 [(码, 行号, 说明), ...]。本拍跑 DR-STRUCT 与 DR-QUOTE。"""
    findings = []
    header, sections = split_doc(text)

    def add(code, lineno, msg):
        findings.append((code, lineno, msg))

    _check_struct(header, sections, add)
    _check_quote(sections, add)
    _check_mode(sections, add)
    _check_gap(sections, add)
    _check_line(sections, add)
    return findings


# ---------------------------------------------------------------- 内置夹具

GOOD = """# 债务重组·逐条挂源（样例）

- 主体：示例实业股份有限公司
- 报告期：2025 年度
- 〔AI 整理初稿〕〔请回原文核对〕〔不构成投资建议〕判断位 [待人工]

## 一、债务重组概况

- 重组债务账面价值：12,000.00 万元「本公司应付某资产管理公司借款本金及利息合计 120,000,000.00 元」〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]
- 债权人：某资产管理公司「债权人系某资产管理股份有限公司」〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]
- 协议签署日：2025 年 6 月 20 日「双方于 2025 年 6 月 20 日签署债务重组协议」〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]
- 重组完成日：2025 年 9 月 30 日「重组事项于 2025 年 9 月 30 日实施完毕」〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]

## 二、重组方式

- 重组方式：以资产清偿债务「本次重组以本公司持有的厂房及土地使用权清偿上述债务」〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]
- 是否组合方式：否「本次重组不涉及债转股及修改其他条款」〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]
- 是否关联方交易：否「债权人与本公司不存在关联关系」〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]

## 三、以资产清偿债务

- 用于清偿的资产类别：厂房及土地使用权「用于清偿的资产为厂房及土地使用权」〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]
- 资产账面价值：9,800.00 万元「上述资产的账面价值合计 98,000,000.00 元」〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]
- 资产公允价值：11,500.00 万元「上述资产的公允价值合计 115,000,000.00 元」〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]
- 清偿债务账面价值：12,000.00 万元「上述资产用于清偿的债务账面价值为 120,000,000.00 元」〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]
- 债务重组损益：500.00 万元「本次债务重组确认其他收益 5,000,000.00 元」〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]

## 四、债转股

- 转股数量：未取到：本报告期债务重组不涉及债转股
- 确认的债务重组损益：未取到：同上

## 五、修改其他条款

- 修改后条款要点：未取到：本报告期债务重组不涉及修改其他条款
- 修改前后现金流差异：未取到：同上

## 六、口径与未取到

- 口径：重组方式只认披露写法，不由本件按「清偿比例」或「对价形式」推定
- 口径：债务重组损益以披露确认的金额为准，不由本件用账面价值与公允价值轧差倒算
- 未取到：转股数量——本报告期债务重组不涉及债转股
- 未取到：确认的债务重组损益——同上（本报告期无债转股）
- 未取到：修改后条款要点——本报告期债务重组不涉及修改其他条款
- 未取到：修改前后现金流差异——同上（本报告期无条款修改）

## 七、来源

- [S1] 示例实业股份有限公司 2025 年年度报告 | https://example.com/annual-2025.pdf | 检索日 2026-11-14 | 类型：年报
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


BAD_STRUCT = _without_section(GOOD, "债转股").replace(
    "- 未取到：转股数量——本报告期债务重组不涉及债转股\n"
    "- 未取到：确认的债务重组损益——同上（本报告期无债转股）\n", "")

# 发现行丢了三元组（只留登记值）
BAD_QUOTE = GOOD.replace(
    "- 债权人：某资产管理公司「债权人系某资产管理股份有限公司」",
    "- 债权人：某资产管理公司",
)

# 引了来源节没登记的编号
BAD_REF = GOOD.replace(
    "- 协议签署日：2025 年 6 月 20 日「双方于 2025 年 6 月 20 日签署债务重组协议」"
    "〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]",
    "- 协议签署日：2025 年 6 月 20 日「双方于 2025 年 6 月 20 日签署债务重组协议」"
    "〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S9]",
)

# 甲：改组方式行点了「重组」，但四条路一条没写
BAD_MODE_VAGUE = GOOD.replace(
    "- 重组方式：以资产清偿债务「本次重组以本公司持有的厂房及土地使用权清偿上述债务」",
    "- 重组方式：本次重组已实施完成「本次重组以本公司持有的厂房及土地使用权清偿上述债务，"
    "并已办理资产过户手续」",
)

# 乙：两种路径混在一行、未标组合
BAD_MODE_MIXED = GOOD.replace(
    "- 重组方式：以资产清偿债务「本次重组以本公司持有的厂房及土地使用权清偿上述债务」",
    "- 重组方式：以资产清偿债务及债转股「本次重组以本公司持有的厂房及土地使用权清偿"
    "部分债务」",
)

# 丙（反证）：明写「组合」，两条路并存不误伤
OK_MODE_COMBO = GOOD.replace(
    "- 重组方式：以资产清偿债务「本次重组以本公司持有的厂房及土地使用权清偿上述债务」",
    "- 重组方式：组合方式（以资产清偿债务＋债转股）「本次重组以本公司持有的厂房及土地"
    "使用权清偿部分债务，其余部分转为对本公司的股权投资」",
)

# 甲：正文写了未取到，第六节没点名（把第六节那条登记删掉）
BAD_GAP_ONE_WAY = GOOD.replace(
    "- 未取到：转股数量——本报告期债务重组不涉及债转股\n", "")

# 丙反证：全文零缺口，第六节显式写「未取到：无」——须零发条
ZERO_GAP = GOOD.replace(
    "- 转股数量：未取到：本报告期债务重组不涉及债转股",
    "- 转股数量：0 股「本次债务重组不涉及债转股」"
    "〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]",
).replace(
    "- 确认的债务重组损益：未取到：同上",
    "- 确认的债务重组损益：0.00 元「本次债务重组不涉及债转股」"
    "〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]",
).replace(
    "- 修改后条款要点：未取到：本报告期债务重组不涉及修改其他条款",
    "- 修改后条款要点：无修改「本次债务重组不涉及修改其他条款」"
    "〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]",
).replace(
    "- 修改前后现金流差异：未取到：同上",
    "- 修改前后现金流差异：0.00 元「本次债务重组不涉及修改其他条款」"
    "〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]",
).replace(
    "- 未取到：转股数量——本报告期债务重组不涉及债转股\n"
    "- 未取到：确认的债务重组损益——同上（本报告期无债转股）\n"
    "- 未取到：修改后条款要点——本报告期债务重组不涉及修改其他条款\n"
    "- 未取到：修改前后现金流差异——同上（本报告期无条款修改）",
    "- 未取到：无",
)

# 红线：正文里写了处置建议
BAD_REDLINE = GOOD.replace(
    "- 是否关联方交易：否「债权人与本公司不存在关联关系」"
    "〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]",
    "- 是否关联方交易：否，建议出售该资产后清偿剩余债务「债权人与本公司不存在关联关系」"
    "〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]",
)

# 红线反证：禁词只出现在「」原句里，不是本件在判断
OK_REDLINE_QUOTED = GOOD.replace(
    "- 是否关联方交易：否「债权人与本公司不存在关联关系」"
    "〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]",
    "- 是否关联方交易：否「债权人称本次重组不存在关联关系，亦未对标的资产出具评级意见」"
    "〔锚：2025 年年报·第 132 页·附注八·债务重组〕[S1]",
)

DEMO = GOOD


def _codes(findings):
    return sorted({c for c, _l, _m in findings})


# ---------------------------------------------------------------- 自测

CASES = (
    ("好样零发条", GOOD, ()),
    ("缺一节（坏样）", BAD_STRUCT, ("DR-STRUCT",)),
    ("发现行丢三元组（坏样）", BAD_QUOTE, ("DR-QUOTE",)),
    ("引用未登记编号（坏样）", BAD_REF, ("DR-QUOTE",)),
    ("重组方式未登记（坏样）", BAD_MODE_VAGUE, ("DR-MODE",)),
    ("两条路径混一行（坏样）", BAD_MODE_MIXED, ("DR-MODE",)),
    ("明写组合方式（反证）", OK_MODE_COMBO, ()),
    ("缺口两向不对账（坏样）", BAD_GAP_ONE_WAY, ("DR-GAP",)),
    ("零缺口显式声明（反证）", ZERO_GAP, ()),
    ("正文写了处置建议（坏样）", BAD_REDLINE, ("DR-LINE",)),
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
    for code in UNIMPLEMENTED:
        unknown += 1
        print("  %-22s 不可判：本拍未实装（不读成「零违例」）" % code)
    print("自测档数=%d｜不合=%d｜不可判=%d" % (len(CASES) + len(UNIMPLEMENTED), bad, unknown))
    if unknown > 0:
        return 3
    return 0 if bad == 0 else 1


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
        print("%s 结论：已实装的道全过（零发条）；未实装：%s"
              % (arg, "、".join(UNIMPLEMENTED)))
        return 0
    for code, lineno, msg in sorted(findings, key=lambda x: (x[1], x[0])):
        print("  %s L%d %s" % (code, lineno, msg))
    print("%s 结论：有发条 %d 条；未实装：%s" % (arg, len(findings), "、".join(UNIMPLEMENTED)))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
