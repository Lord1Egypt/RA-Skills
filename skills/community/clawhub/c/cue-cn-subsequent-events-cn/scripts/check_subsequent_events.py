#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cn-subsequent-events-cn —— 资产负债表日后事项逐条挂源的五道机检（零网络）。

五道：
  SE-STRUCT  形制        头部四件自标、主体／报告期、七节齐且有序、前五节各有发现行、
                         六七节不得留白
  SE-QUOTE   原句与锚    每条发现行以「原句」〔锚：…〕[S#] 收尾；来源行带 URL 与检索日；
                         引用的 [S#] 须已在来源节登记
  SE-KIND    调整／非调整 调整事项与非调整事项的划分只认披露原句，不由本件按事项性质推定
  SE-ADJUST  调整分录    调整分录与对报表的影响只认披露原句，不由本件自行补算
  SE-LINE    红线        投资建议、损益预测、评级与目标价、确定性断言零命中

退码：0 五道全过 / 1 有发条 / 2 用法错 / 3 读不到文件或空稿，或尚有判据未实装。

SE-STRUCT／SE-QUOTE／SE-KIND／SE-ADJUST／SE-LINE **五道全部实装**，UNIMPLEMENTED 为空元组。
`_not_judged` 保留为兜底：只给「声明已实装却仍抛未实装」用，由调用方按不合计处理。
check_text 返回 (findings, unjudged) 二元组；unjudged 恒空时退码不再退回 3。
"""

from __future__ import annotations

import datetime
import os
import re
import sys

SLUG = "cue-cn-subsequent-events-cn"
CODES = ("SE-STRUCT", "SE-QUOTE", "SE-KIND", "SE-ADJUST", "SE-LINE")
UNIMPLEMENTED = ()

SECTIONS = (
    "日后事项概况",
    "调整事项",
    "非调整事项",
    "对财务报表的影响",
    "持续经营与审计意见",
)
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"
ALL_SECTIONS = SECTIONS + (GAP_SECTION, SOURCE_SECTION)
CONTENT_COUNT = len(SECTIONS)

USAGE = """usage: check_subsequent_events.py <稿.md>
       check_subsequent_events.py --selftest
       check_subsequent_events.py --demo

资产负债表日后事项逐条挂源的五道机检（零网络）：
  SE-STRUCT 形制 / SE-QUOTE 原句与锚 / SE-KIND 调整与非调整口径 /
  SE-ADJUST 调整分录与披露影响 / SE-LINE 红线
退码：0 五道全过 / 1 有发条 / 2 用法错 / 3 读不到文件或空稿，或尚有判据未实装
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


# ---------------------------------------------------------------- SE-STRUCT

def _check_struct(header, sections, add):
    htext = "\n".join(s for _ln, s in header)
    for mark in MARK_TEXTS:
        if mark not in htext:
            add("SE-STRUCT", 1, "头部缺自标「%s」：起草稿须自报身份、边界与判断位" % mark)
    if not any(SUBJECT.match(s.strip()) for _ln, s in header):
        add("SE-STRUCT", 1, "头部缺 `- 主体：…` 一行：主体不定，日后事项落不到人头上")
    if not any(PERIOD.match(s.strip()) for _ln, s in header):
        add("SE-STRUCT", 1, "头部缺 `- 报告期：…` 一行")

    seen = set()
    for name, lineno, _body in sections:
        if name in seen:
            add("SE-STRUCT", lineno,
                "节「%s」重复出现：七节各占一节，多出的同名节会让节内发现行归属不清" % name)
        seen.add(name)
        if name not in ALL_SECTIONS:
            add("SE-STRUCT", lineno,
                "不认识的节名「%s」：本件只认七个节，多出的节里的发现行不被判" % name[:20])

    names = [n for n, _l, _b in sections]
    if names != list(ALL_SECTIONS):
        missing = [s for s in ALL_SECTIONS if s not in names]
        if missing:
            add("SE-STRUCT", 1, "缺节：%s —— 七节须齐（五块内容 + %s + %s）"
                % ("、".join("「%s」" % s for s in missing), GAP_SECTION, SOURCE_SECTION))
        else:
            add("SE-STRUCT", 1, "七节顺序不对：应为 %s，实为 %s"
                % ("／".join(ALL_SECTIONS), "／".join(names)))

    for name in SECTIONS:
        body = next((b for n, _l, b in sections if n == name), None)
        if body is None:
            continue
        if not any(_is_finding_line(s) for _ln, s in body):
            lineno = next((l for n, l, _b in sections if n == name), 1)
            add("SE-STRUCT", lineno, "「%s」节只有小标题、没有发现行：这一块要逐条登记" % name)

    for name in (GAP_SECTION, SOURCE_SECTION):
        body = next((b for n, _l, b in sections if n == name), None)
        if body is None:
            continue
        if not any(s.strip() for _ln, s in body):
            lineno = next((l for n, l, _b in sections if n == name), 1)
            add("SE-STRUCT", lineno,
                "「%s」节是空的：这一节要么登记缺口、要么登记来源，不能留白" % name)


# ---------------------------------------------------------------- SE-QUOTE

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
                add("SE-QUOTE", lineno,
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
                    add("SE-QUOTE", lineno,
                        "引用了未登记的 [%s]：来源节里没有这一号" % m.group(1))
                continue
            miss = []
            if not QUOTE.search(s):
                miss.append("「」原句")
            if not ANCHOR_ANY.search(s):
                miss.append("〔锚：…〕")
            if not REF_ANY.search(s):
                miss.append("[S#]")
            add("SE-QUOTE", lineno,
                "发现行缺 %s：每条发现行须以「原句」〔锚：…〕[S#] 收尾——%s"
                % ("、".join(miss) if miss else "三元组", s[:44]))

    if has_source_section and not registered:
        add("SE-QUOTE", 1, "来源节一条合规来源行都没有：每个 [S#] 都要有可点 URL 与检索日")


# ---------------------------------------------------------------- SE-KIND

# 两类事项的会计处理完全相反，所以归类是件「只能照抄」的事：
#   调整事项   = 对资产负债表日已存在的情况提供了新证据 → 调账
#   非调整事项 = 资产负债表日后新发生的情况             → 不调账，只披露
KIND_ADJ = "调整事项"
KIND_NON = "非调整事项"

# 等价表述归一：长的排前面，扫描时吃掉的跨度不再参与匹配
# （否则「非调整事项」会被「调整事项」二次命中，反证样当场变假红）。
KIND_VARIANTS = tuple(sorted((
    ("不属于调整事项", KIND_NON),
    ("不构成调整事项", KIND_NON),
    ("非调整事项", KIND_NON),
    ("调整事项", KIND_ADJ),
    ("不需调整", KIND_NON),
    ("仅需披露", KIND_NON),
    ("不调账", KIND_NON),
    ("只披露", KIND_NON),
    ("需调整", KIND_ADJ),
    ("调账", KIND_ADJ),
), key=lambda kv: len(kv[0]), reverse=True))

# 类别位：项名写着这些词，就是「这一格要填类别」的意思。
KIND_SLOT_WORDS = ("类别", "性质", "类型", "划分", "归类", "归属")

# 事件名：只出现事件名而没写类别，不等于归了类——同一个事件名两种归类都可能。
EVENT_WORDS = (
    "销售退回", "火灾", "诉讼判决", "判决", "仲裁", "诉讼", "自然灾害", "地震",
    "水灾", "风灾", "汇率变动", "股权转让", "资产减值", "破产", "事故", "合并",
    "收购", "增发", "回购", "股利", "利润分配", "债务重组", "重大合同",
)


def _kinds_in(text):
    """→ 文本里出现的类别集合（等价表述归一到两类）。最长匹配优先、匹配跨度不重叠。"""
    hit = set()
    i = 0
    while i < len(text):
        for variant, canon in KIND_VARIANTS:
            if text.startswith(variant, i):
                hit.add(canon)
                i += len(variant)
                break
        else:
            i += 1
    return hit


def _events_in(text):
    return {w for w in EVENT_WORDS if w in text}


def check_kind(sections, add):
    """SE-KIND：调整／非调整事项的划分只认原句。

    甲 登记值写了类别，同一行「」原句里没有该类别（含等价表述）→ 发；
    乙 登记的类别与原句写的相反（原句写非调整、登记写调整，或反之）→ 发，并点明两者
       会计处理相反；甲与乙同一行冲突时按乙报，别把「写反了」说成「没写到」；
    丙 类别位（项名含 类别／性质／类型／划分／归类／归属）填了事件名却没填类别 → 发：
       事件名推不出类别，同一个事件名在不同情况下可能是调整也可能不是；
    丁 前五节一条类别都没登记 → 在首条发现行发一次。
    「未取到」行与 [待人工] 行不参与本道判定：缺口不等于归了类，判断位也不是归了类。
    """
    first_line = None
    seen_any = False

    for name, _l, body in sections:
        if name not in SECTIONS:
            continue
        for lineno, raw in body:
            s = raw.strip()
            if not _is_finding_line(s):
                continue
            if first_line is None:
                first_line = lineno
            # 丁的在场：非缺口行里出现类别（登记值与引文都算）——「未取到 X」是缺席不是登记。
            if not _is_gap_line(s) and _kinds_in(s):
                seen_any = True
            if _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s:
                continue                     # 缺口与判断位不归这道

            label, _rest = _split_label(s)
            reg_text = _strip_quotes(s)
            said_text = _quotes(s)
            reg = _kinds_in(reg_text)
            said = _kinds_in(said_text)

            missing = reg - said
            if missing:
                if said and not (reg & said):
                    # 乙：写反了——两者会计处理相反，是最该拦的一型
                    add("SE-KIND", lineno,
                        "「%s」登记为「%s」，原句写的却是「%s」：两者会计处理相反——"
                        "调整事项调账，非调整事项只披露，写反就是把账调错了"
                        % (label[:16], "、".join(sorted(reg)), "、".join(sorted(said))))
                else:
                    add("SE-KIND", lineno,
                        "「%s」登记为「%s」，同行原句没有该类别表述：归类只认披露原句，"
                        "本件不按事项性质推定" % (label[:16], "、".join(sorted(missing))))
                continue

            # 丙：类别位填了事件名。同行原句已给出类别的不算「事件名代替类别」——
            # 那一行归类有披露原句撑着，事件名只是项名，不是本件自己推出来的类别。
            if not reg and not said and any(w in label for w in KIND_SLOT_WORDS):
                ev = _events_in(reg_text)
                if ev:
                    add("SE-KIND", lineno,
                        "「%s」拿事件名（%s）代替类别：事件名推不出类别，同一个事件名在不同"
                        "情况下可能是调整也可能是非调整" % (label[:16], "、".join(sorted(ev))))

    if not seen_any:
        add("SE-KIND", first_line or 1,
            "前五节一条类别都没登记（调整事项／非调整事项）：两类会计处理相反，不许留空")


# ---------------------------------------------------------------- SE-ADJUST

# 只判「对财务报表的影响」这一节。
ADJUST_SECTION = SECTIONS[3]

# 金额：必须带单位才算数——不带单位的四位数（年份、页码、编号）不是金额。
AMOUNT = re.compile(r"(?P<num>\d[\d,]*(?:\.\d+)?)\s*(?P<unit>亿元|万元|千元|元)")
UNIT_SCALE = {"亿元": 1e8, "万元": 1e4, "千元": 1e3, "元": 1.0}
REL_TOL = 1e-6

# 取数前先剥干净：〔…〕锚与 [S#] 里都带数字（「第 132 页」的 132、[S1] 的 1），
# 不剥会把它们当金额去比，判出假红。
BRACKET = re.compile(r"〔[^〕]*〕")


def _clean_for_amount(s):
    """去掉〔…〕锚与 [S#]，只留本件自己写的登记值与「」原句，供取数用。"""
    return REF_ANY.sub("", BRACKET.sub("", s))


def _amounts(text):
    """→ [(原样串, 折算成元的值)]。万元×1e4／亿元×1e8／千元×1e3／元×1。"""
    out = []
    for m in AMOUNT.finditer(text):
        raw = m.group("num").replace(",", "")
        try:
            val = float(raw) * UNIT_SCALE[m.group("unit")]
        except ValueError:
            continue
        out.append((m.group(0).strip(), val))
    return out


def _same_amount(a, b):
    if a == b:
        return True
    return abs(a - b) <= REL_TOL * max(abs(a), abs(b))


def _says_no_adjust(text):
    return "不调整" in text


def check_adjust(sections, add):
    """SE-ADJUST：调整分录与对报表的影响只认披露原句，本件不许自算。

    甲 金额对不上：登记值里有金额（元／万元／亿元／千元），同行「」原句里没有可折算相等的数
       ⇒ 发。折算口径：万元×1e4、亿元×1e8、千元×1e3、元×1，相对容差 1e-6；取数前剥掉
       〔…〕锚与 [S#]（它们带数字，不剥就是假红）。
    乙 调整／不调整写反：登记值写「调整」而原句只写「不调整」，或登记值写「不调整」而原句
       写「调整」（未带「不」）⇒ 发。只判本件自己写的那半句，引文只作对照。
    只判「对财务报表的影响」这一节；「未取到」行与 [待人工] 行不参与。
    """
    for name, _l, body in sections:
        if name != ADJUST_SECTION:
            continue
        for lineno, raw in body:
            s = raw.strip()
            if not _is_finding_line(s):
                continue
            if _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s:
                continue
            label, _rest = _split_label(s)
            reg = _clean_for_amount(_strip_quotes(s))
            said = _clean_for_amount(_quotes(s))

            # 甲：登记值的每个金额，原句里都要能找到一个折算相等的数
            said_amts = [v for _r, v in _amounts(said)]
            for raw_amt, val in _amounts(reg):
                if said_amts and any(_same_amount(val, v) for v in said_amts):
                    continue
                if not said_amts:
                    add("SE-ADJUST", lineno,
                        "「%s」登记了金额「%s」，同行原句没有任何金额：影响金额只认披露原句，"
                        "本件不许自算" % (label[:16], raw_amt))
                else:
                    add("SE-ADJUST", lineno,
                        "登记「%s」，原句找不到该数（原句金额：%s）：影响金额只认披露原句，"
                        "本件不许自算" % (raw_amt, "、".join(r for r, _v in _amounts(said))))

            # 乙：调整／不调整写反。「不调整」里含「调整」，先判否定形，别互相咬。
            reg_no = _says_no_adjust(reg)
            said_no = _says_no_adjust(said)
            reg_yes = ("调整" in reg) and not reg_no
            said_yes = ("调整" in said) and not said_no
            if (reg_no and said_yes) or (reg_yes and said_no):
                add("SE-ADJUST", lineno,
                    "「%s」登记为「%s」，原句写的却是「%s」：调整与不调整方向相反，"
                    "写反就是把账调错了"
                    % (label[:16], "不调整" if reg_no else "调整",
                       "不调整" if said_no else "调整"))


# ---------------------------------------------------------------- SE-LINE

# 红线四族。只收「评级语言」，不收裸动词「增持」「减持」——那两个词单独出现时是普通
# 登记语言（「股东减持计划」是披露原文），收进来会把它判红。
HARD_BAN = (
    # 甲 处置与投资建议（本件只登记披露，不替读者决定买不买、卖不卖）
    "建议买入", "建议卖出", "建议增持", "建议减持", "建议建仓", "建议止损",
    # 乙 损益预测（日后事项的利润影响只能照抄披露，本件不许替披露往前推一期）
    "预计影响", "预计增厚", "将增厚利润", "预计扭亏", "预计提升业绩", "预计增利",
    # 丙 评级与目标价（一律 [待人工]，本件不给）
    "评级", "目标价", "目标市值", "值得投资", "低估", "高估",
    "买入评级", "卖出评级", "增持评级", "减持评级", "给予买入", "给予卖出",
    "强烈推荐", "跑赢大盘",
    # 丁 确定性断言（收断言收益，不收裸「必然」——「必然导致」可以是准则叙述）
    "稳赚", "零风险", "保证收益", "必然盈利", "必然上涨", "必然受益", "包赚",
)

# 这两节本来就在说该禁什么，判它等于自伤。节名含这些词即整节跳过。
LINE_EXEMPT_SECTION = ("合规红线", "数据通道")

# 否定语境：紧挨在红线词前面的这几串，说明这一行是在**划本件的边界**（「本件不给评级」），
# 不是在给评级。收口到「紧邻」为止——不做整句否定解析，深度否定不豁免。
# 长串必须排在前面：`text[:i]` 以「不给」结尾时也要认出来，而「给」不在其列。
NEG_BEFORE = ("不给", "不予", "不作", "不出具", "不写", "不做", "不含", "不提",
              "不预测", "不提供", "不推荐", "不给出", "不得", "严禁", "禁止", "不")


def _negated(text, idx):
    """判 idx 处的红线词是不是被紧邻的否定词罩着。"""
    head = text[max(0, idx - 4):idx]
    return any(head.endswith(neg) for neg in NEG_BEFORE)


def check_line(sections, add):
    """SE-LINE：投资建议、损益预测、评级与目标价、确定性断言零命中。

    只判本件自己写的字：`_strip_quotes` 先洗掉「」原句与〔锚〕——引文里出现这些词是
    披露在说话（「审计机构未出具评级意见」），不是本件在判断。
    节名含「合规红线」「数据通道」的整节跳过，否则一把尺量到写尺子的那一页上。
    紧邻否定词的不算违规：「本件不给评级、不给目标价」是边界声明，不是评级意见。
    """
    for name, _l, body in sections:
        if any(w in name for w in LINE_EXEMPT_SECTION):
            continue
        for lineno, raw in body:
            s = raw.strip()
            if not _is_finding_line(s):
                continue
            own = _strip_quotes(s)
            hit = None
            for w in HARD_BAN:
                if any(not _negated(own, m.start())
                       for m in re.finditer(re.escape(w), own)):
                    hit = w
                    break
            if hit:
                label, _rest = _split_label(s)
                add("SE-LINE", lineno,
                    "「%s」踩了红线词「%s」：买卖建议、损益预测、评级与目标价、"
                    "确定性断言都不是本件的判项——%s" % (label[:16], hit, s[:40]))


# ---------------------------------------------------------------- 总装

def check_text(text):
    """返回 (findings, unjudged)。

    五道全部实装，unjudged 恒为空；保留二元组是为了让调用方不必改判「有没有没跑的道」——
    零发条的语义从此就是五道全过，不再是「跑过的那些道过了」。
    """
    findings = []
    unjudged = []
    header, sections = split_doc(text)

    def add(code, lineno, msg):
        findings.append((code, lineno, msg))

    _check_struct(header, sections, add)
    _check_quote(sections, add)
    check_kind(sections, add)
    check_adjust(sections, add)
    check_line(sections, add)

    findings.sort(key=lambda x: (x[1], CODES.index(x[0])))
    return findings, unjudged


# ---------------------------------------------------------------- 内置夹具

GOOD = """# 资产负债表日后事项·逐条挂源（样例）

- 主体：示例制造股份有限公司
- 报告期：2025 年度
- 〔AI 整理初稿〕〔请回原文核对〕〔不构成投资建议〕判断位 [待人工]

## 一、日后事项概况

- 事项性质：资产负债表日后事项「本附注披露自资产负债表日至财务报告批准报出日之间发生的重大事项」〔锚：2025 年年报·第 178 页·附注十一·资产负债表日后事项〕[S1]
- 资产负债表日：2025 年 12 月 31 日「本公司资产负债表日为 2025 年 12 月 31 日」〔锚：2025 年年报·第 178 页·附注十一·资产负债表日后事项〕[S1]
- 财务报告批准报出日：2026 年 3 月 20 日「本财务报表于 2026 年 3 月 20 日经董事会批准报出」〔锚：2025 年年报·第 178 页·附注十一·资产负债表日后事项〕[S1]
- 事项数量：2 项「本报告期后事项共两项」〔锚：2025 年年报·第 178 页·附注十一·资产负债表日后事项〕[S1]

## 二、调整事项

- 事项一：已决诉讼判决确定「2026 年 2 月 10 日，法院就本公司作为被告的合同纠纷案作出终审判决，判令本公司赔偿 8,000,000.00 元」〔锚：2025 年年报·第 179 页·附注十一·资产负债表日后事项〕[S1]
- 事项一性质：调整事项「本公司将上述判决认定为资产负债表日后调整事项」〔锚：2025 年年报·第 179 页·附注十一·资产负债表日后事项〕[S1]

## 三、非调整事项

- 事项二：重要子公司股权转让「2026 年 1 月 15 日，本公司与第三方签署股权转让协议，转让所持某子公司 60% 股权」〔锚：2025 年年报·第 179 页·附注十一·资产负债表日后事项〕[S1]
- 事项二性质：非调整事项「本公司将上述股权转让认定为资产负债表日后非调整事项」〔锚：2025 年年报·第 179 页·附注十一·资产负债表日后事项〕[S1]

## 四、对财务报表的影响

- 事项一影响：调增营业外支出 8,000,000.00 元「上述判决使本公司 2025 年度营业外支出增加 8,000,000.00 元」〔锚：2025 年年报·第 179 页·附注十一·资产负债表日后事项〕[S1]
- 事项二影响：不调整 2025 年度财务报表「上述股权转让不调整 2025 年度财务报表」〔锚：2025 年年报·第 179 页·附注十一·资产负债表日后事项〕[S1]

## 五、持续经营与审计意见

- 持续经营能力：未取到：附注未就持续经营能力作出专项说明
- 审计意见类型：标准无保留意见「审计机构对本公司 2025 年度财务报表出具了标准无保留意见的审计报告」〔锚：2025 年年报·第 96 页·审计报告〕[S1]

## 六、口径与未取到

- 口径：调整事项与非调整事项的划分只认披露原文，不由本件按事项性质推定
- 口径：对报表的影响金额照抄披露原句，不由本件自行轧差或补算
- 未取到：持续经营能力——附注未就持续经营能力作出专项说明

## 七、来源

- [S1] 示例制造股份有限公司 2025 年年度报告 | https://example.com/annual-2025.pdf | 检索日 2026-11-14 | 类型：年报
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


# 缺节：整节删掉「非调整事项」——该只红 SE-STRUCT，来源节的 [S1] 登记行还在，别道不跟着红。
BAD_STRUCT = _without_section(GOOD, "非调整事项")

# 发现行丢了三元组（只留登记值）。
# 摘的是「事项一」这条不带类别词的行：摘在「事项二性质」上会同时踩 SE-KIND 甲
# （登记值写了类别、原句里没了），一条坏样红两道，分不清归属。
BAD_QUOTE = GOOD.replace(
    "- 事项一：已决诉讼判决确定「2026 年 2 月 10 日，法院就本公司作为被告的合同纠纷案"
    "作出终审判决，判令本公司赔偿 8,000,000.00 元」"
    "〔锚：2025 年年报·第 179 页·附注十一·资产负债表日后事项〕[S1]",
    "- 事项一：已决诉讼判决确定",
)

# 归类写反：原句写「非调整事项」，登记值写「调整事项」——该只红 SE-KIND。
# 引文与锚原样留着，SE-QUOTE 与 SE-STRUCT 都不该跟着红。
BAD_KIND = GOOD.replace(
    "- 事项二性质：非调整事项「本公司将上述股权转让认定为资产负债表日后非调整事项」",
    "- 事项二性质：调整事项「本公司将上述股权转让认定为资产负债表日后非调整事项」",
)

# 反证：类别词只在「」引文里，登记值写事件名、不写类别——判的是本件自己的话，
# 引文里的归类不构成本件登记，不该发；另一行（事项一性质）已登记类别，丁也不该发。
OK_KIND_QUOTE_ONLY = GOOD.replace(
    "- 事项二性质：非调整事项「本公司将上述股权转让认定为资产负债表日后非调整事项」",
    "- 事项二类型：股权转让及出售「本公司将上述股权转让认定为资产负债表日后非调整事项」",
)

# 甲：登记值金额与原句对不上（8,000,000.00 → 9,000,000.00），原句一字未动。
# 只动「事项一影响」的登记值，引文与锚原样——该只红 SE-ADJUST。
BAD_ADJUST_AMOUNT = GOOD.replace(
    "- 事项一影响：调增营业外支出 8,000,000.00 元「",
    "- 事项一影响：调增营业外支出 9,000,000.00 元「",
)

# 反证：写法定量不同、折算相等（登记 800.00 万元 ∥ 原句 8,000,000.00 元），
# 万元×1e4 后同为 8e6，不该发。
OK_ADJUST_UNIT = GOOD.replace(
    "- 事项一影响：调增营业外支出 8,000,000.00 元「",
    "- 事项一影响：调增营业外支出 800.00 万元「",
)

# 乙：调整／不调整写反——原句仍是「不调整」，登记值改成「调整」。该只红 SE-ADJUST。
BAD_ADJUST_FLIP = GOOD.replace(
    "- 事项二影响：不调整 2025 年度财务报表「",
    "- 事项二影响：调整 2025 年度财务报表「",
)

# 乙的反向：登记值写「不调整」而原句写「调整」（未带「不」）。乙是两向的，
# 只测一向等于没测出「方向」这件事。
BAD_ADJUST_FLIP_REV = GOOD.replace(
    "- 事项二影响：不调整 2025 年度财务报表「上述股权转让不调整 2025 年度财务报表」",
    "- 事项二影响：不调整 2025 年度财务报表「上述股权转让调整 2025 年度财务报表」",
)

# 红线：在「持续经营与审计意见」插一条损益预测，三元组照挂（不挂会先撞 SE-QUOTE）。
# 落点在第五节而不是「对财务报表的影响」：那一节归 SE-ADJUST，落在那里会一条红两码。
BAD_LINE = GOOD.replace(
    "- 持续经营能力：未取到：附注未就持续经营能力作出专项说明\n",
    "- 观点：预计影响 2026 年利润 3,000 万元「上述判决对以后年度的影响尚待观察」"
    "〔锚：2025 年年报·第 179 页·附注十一·资产负债表日后事项〕[S1]\n"
    "- 持续经营能力：未取到：附注未就持续经营能力作出专项说明\n",
)

# 反证：红线词只出现在「」引文里（摘的是别人说的），登记值不写——判的是本件自己的话。
OK_LINE_QUOTED = GOOD.replace(
    "- 持续经营能力：未取到：附注未就持续经营能力作出专项说明\n",
    "- 观点：某券商研究观点「预计影响 2026 年利润 3,000 万元」"
    "〔锚：2025 年年报·第 179 页·附注十一·资产负债表日后事项〕[S1]\n"
    "- 持续经营能力：未取到：附注未就持续经营能力作出专项说明\n",
)

# 红线甲组：处置与投资建议。上面那档只测到乙组（损益预测），甲组一整组没被测过——
# 六条词里最容易被顺手写下的就是「建议买入」。落点在第三节的非调整事项行：
# 该行登记值无类别词（不撞 SE-KIND）、不在第四节（不撞 SE-ADJUST）、三元组原样保留。
BAD_LINE_ADVICE = GOOD.replace(
    "- 事项二：重要子公司股权转让「",
    "- 事项二：重要子公司股权转让，建议买入「",
)

# 反证：边界声明——「本件不给评级、不给目标价」写的是本件不做什么，不是它在评级。
# 这一句放在「口径与未取到」节，仍落在 SE-LINE 的判域内（该节不豁免），所以它测的是
# 否定语境识别本身。节名不出现「合规红线」「数据通道」，避免借豁免蒙过。
OK_LINE_SCOPE = GOOD.replace(
    "- 口径：对报表的影响金额照抄披露原句，不由本件自行轧差或补算\n",
    "- 口径：对报表的影响金额照抄披露原句，不由本件自行轧差或补算\n"
    "- 口径：本件不给评级、不给目标价\n",
)

DEMO = GOOD


def _codes(findings):
    return sorted({c for c, _l, _m in findings})


# ---------------------------------------------------------------- 自测

CASES = (
    ("好样零发条", GOOD, ()),
    ("缺一节（坏样）", BAD_STRUCT, ("SE-STRUCT",)),
    ("发现行丢三元组（坏样）", BAD_QUOTE, ("SE-QUOTE",)),
    ("归类写反（坏样）", BAD_KIND, ("SE-KIND",)),
    ("类别词只在原句里（反证）", OK_KIND_QUOTE_ONLY, ()),
    ("影响金额与原句对不上（坏样）", BAD_ADJUST_AMOUNT, ("SE-ADJUST",)),
    ("换了单位但折算相等（反证）", OK_ADJUST_UNIT, ()),
    ("调整／不调整写反（坏样）", BAD_ADJUST_FLIP, ("SE-ADJUST",)),
    ("写反的反向（坏样）", BAD_ADJUST_FLIP_REV, ("SE-ADJUST",)),
    ("正文写了损益预测（坏样）", BAD_LINE, ("SE-LINE",)),
    ("红线词只在原句里（反证）", OK_LINE_QUOTED, ()),
    ("正文写了买卖建议（坏样）", BAD_LINE_ADVICE, ("SE-LINE",)),
    ("边界声明不算评级（反证）", OK_LINE_SCOPE, ()),
)


def selftest():
    bad = 0
    unknown = 0
    print("── 自测 ──")
    for name, text, expect in CASES:
        try:
            findings, unjudged = check_text(text)
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
    findings, unjudged = check_text(text)
    for code, lineno, msg in findings:
        print("  %s L%d %s" % (code, lineno, msg))
    if findings:
        print("%s 结论：有发条 %d 条" % (arg, len(findings)))
    else:
        print("%s 结论：五道全过（零发条）" % arg)
    if unjudged:
        for code in unjudged:
            print("不可判 %s：判据未实装" % code)
        print("注：以上 %d 道未判，**这不等于合规**；本稿不能按「零发条」读。" % len(unjudged))
        return 3
    if findings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
