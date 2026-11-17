#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_eps.py — 每股收益逐条挂源稿五道机检（零网络、零外发、不读环境变量）

**五道全部实装**：形制／原句与锚／基本分子分母／稀释调整项／红线逐道落字。
`UNIMPLEMENTED` 现为空元组；往后若再加判据，尚未实装的道登记在那里，`--selftest` 逐条报「不可判」
并按 3 收场——**不提前宣布它们实装了**。

用法：
    python3 scripts/check_eps.py <每股收益稿>.md
    python3 scripts/check_eps.py --selftest
    python3 scripts/check_eps.py --demo     打印一份完整合规样例（零输入可跑）

七节（按序，`## ` 起节）：
    每股收益概况／基本每股收益／稀释每股收益／股数与调整／列报与追溯调整／口径与未取到／来源

五道码（带「已落字」的两道是本拍实现的行为，其余三道写的是**这道要判什么**）：

道一 EP-STRUCT 形制（已落字）
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]；
  `- 主体：` 行、`- 报告期：` 行在场且非空；七节齐且按序；前五节各至少一条 `- ` 发现行，
  节内只许 `- ` 发现行、`### ` 子标题与空行；六七节不得留白。

道二 EP-QUOTE 原句与锚（已落字）
  每条发现行以「」原句 + 〔锚：…〕 + [S#] 收尾，可挂多组；原句与锚不得为空；
  例外只有三形：「未取到」行、[待人工] 行与〔自算〕行；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址；
  正文引用的每个 [S#] 必须在来源节有对应行；来源节一条来源行都没有也发。

道三 EP-CALC 基本每股收益的分子分母只认原句（已落字）
  归属于普通股股东的净利润、扣非后净利润、加权平均普通股股数、基本每股收益金额——
  每一族的登记数都必须在同一行「」原句里找得到（跨单位按量纲折算后比，`17,200.00 万元`
  与 `172,000,000.00 元` 是同一个数）；找不到就是没照抄，一律发。
  行内出现「据此计算」「＝」「数字／数字」这类本件自算的痕迹而原句没给结果的，同样发——
  本件只登记披露数，不自行计算每股收益。

道四 EP-DILUTE 稀释每股收益的调整项只认原句（已落字）
  甲 登记了「调整后净利润／调整后股数」的数，同一行「」原句里找不到 → 发（跨单位折算后比）
  乙 登记了潜在普通股类型词（可转换公司债券／认股权证／股份期权／可转换优先股…），
     该类型词必须也在同一行原句里 → 否则发
  丙 登记了「具有反稀释性／不计入稀释每股收益」，原句没有该说法 → 发
  丁 行内写「假定转换／假设转换」，原句没有该说法 → 发
  反稀释与是否计入是披露的判断，本件不代下；调整项不按假定的转换价格自行补算。

道五 EP-LINE 红线（已落字）
  每股收益预测、估值结论与目标价、评级语言、确定性断言零命中；引文先洗掉再判。

退码：0 全过 / 1 有发条 / 2 用法错（缺参数） / 3 读不到文件或空稿
      （判据空壳期间，`--selftest` 有「不可判」档时退 3，不并入「不合」）。
"""

import argparse
import re
import sys

SLUG = "cue-cn-eps-cn"

CODES = ("EP-STRUCT", "EP-QUOTE", "EP-CALC", "EP-DILUTE", "EP-LINE")
UNIMPLEMENTED = ()

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("每股收益概况", "基本每股收益", "稀释每股收益", "股数与调整",
            "列报与追溯调整", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"

HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")
SUBJECT = re.compile(r"^-\s*主体[：:]\s*\S")
PERIOD = re.compile(r"^-\s*报告期[：:]\s*\S")

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
    """判据尚未落字：抛出去让调用方计「不可判」。绝不返回空清单冒充零发条。"""
    raise NotImplementedError("%s 未落字：%s" % (code, why))


def check_struct(head, sections, stray):
    """道一 EP-STRUCT 形制：头部四件自标与两行、七节齐且按序、节内行形制。

    只判「形」：节名在不在、顺序对不对、节内是不是清一色 `- ` 发现行。
    判断内容对不对是另四道的事——这里不越界，否则一支注入会同时红两道、分不清归属。
    """
    out = []
    htext = "\n".join(s for _i, s in head)
    for mark in MARK_TEXTS:
        if mark not in htext:
            out.append(("EP-STRUCT", head[0][0] if head else 1, "头部缺自标「%s」" % mark))
    if not any(SUBJECT.match(s.strip()) for _i, s in head):
        out.append(("EP-STRUCT", head[0][0] if head else 1, "头部缺 `- 主体：` 行"))
    if not any(PERIOD.match(s.strip()) for _i, s in head):
        out.append(("EP-STRUCT", head[0][0] if head else 1, "头部缺 `- 报告期：` 行"))

    names = [n for n, _l, _b in sections]
    for name in SECTIONS:
        if name not in names:
            out.append(("EP-STRUCT", 1, "缺节「%s」" % name))
    pos = [SECTIONS.index(n) for n in names]
    if pos != sorted(pos):
        out.append(("EP-STRUCT", 1, "节序不对：现序 %s，应序 %s"
                    % ("／".join(names), "／".join(SECTIONS))))
    for lineno, raw in stray:
        out.append(("EP-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw))

    for name, hline, body in sections:
        if name not in CONTENT_SECTIONS:
            if name == GAP_SECTION:
                if not any(s.strip() for _ln, s in body):
                    out.append(("EP-STRUCT", hline, "「%s」节留白：这一节要么登记缺口、要么写 `未取到：无`" % name))
                for lineno, s in body:
                    if s.strip() and not _is_finding_line(s):
                        out.append(("EP-STRUCT", lineno, "「%s」只许 `- ` 行：%s"
                                    % (name, s.strip()[:40])))
            elif name == SOURCE_SECTION:
                if not any(s.strip() for _ln, s in body):
                    out.append(("EP-STRUCT", hline, "「%s」节留白：每条 [S#] 都要有一条来源行" % name))
                for lineno, s in body:
                    if s.strip() and not s.lstrip().startswith("- ["):
                        out.append(("EP-STRUCT", lineno, "来源节只许 `- [S#] …` 行：%s"
                                    % s.strip()[:40]))
            continue
        n_find = 0
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                out.append(("EP-STRUCT", lineno, "节内只许 `- ` 发现行：%s" % s.strip()[:40]))
                continue
            n_find += 1
        if n_find == 0:
            out.append(("EP-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name))
    return out


def check_quote(head, sections, stray):
    """道二 EP-QUOTE 原句与锚：三元组、来源行、[S#] 两向对应。

    例外只有三形：「未取到」行、[待人工] 行、〔自算〕行——前两者是缺口与判断位，
    后者已经必须在同一行交代取数口径，要求它再挂原句等于把自算伪装成披露值。
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
                if "未取到" in s or "[待人工]" in s or "〔自算〕" in s:
                    continue
                out.append(("EP-QUOTE", lineno,
                            "发现行缺「」原句 + 〔锚：…〕 + [S#] 三元组：%s" % s.strip()[:40]))
                continue
            for m in TRIPLE.finditer(s):
                if not m.group("q").strip():
                    out.append(("EP-QUOTE", lineno, "原句为空"))
                if not m.group("a").strip():
                    out.append(("EP-QUOTE", lineno, "锚为空"))
            if not re.search(r"\[S\d+\]\s*$", s.strip()):
                out.append(("EP-QUOTE", lineno, "发现行未以 [S#] 收尾（三元组须在行末）"))

    defined = set()
    for name, _hline, body in sections:
        if name != SOURCE_SECTION:
            continue
        for lineno, s in body:
            if not s.strip():
                continue
            m = SOURCE_LINE.match(s.strip())
            if not m:
                out.append(("EP-QUOTE", lineno,
                            "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:50]))
                continue
            defined.add(m.group("s"))
    for ref in sorted(set(referenced)):
        if ref not in defined:
            out.append(("EP-QUOTE", 1, "正文引用 [%s]，来源节没有对应登记行" % ref))
    return out


# ---------------------------------------------------------------- EP-CALC

# 三族登记值：每一族的数字都必须能在同一行「」原句里找到，找不到就是没照抄。
CALC_EPS_BASIC = "基本每股收益"
CALC_NET_PROFIT = ("净利润", "归属于")
CALC_SHARES = ("股数", "加权平均")

# 本件自己算的痕迹。**不收裸「／」**：`元/股` 是单位不是算式，收进来会把每一条
# 正常登记的每股收益行都判红。要求斜杠两侧都是数字才算算式痕迹。
SELF_CALC_TRACES = ("据此计算", "据此测算", "据此推算", "自行计算", "计算得出", "÷", "＝", "=")
SELF_CALC_DIVIDE = re.compile(r"\d\s*[／/]\s*\d")

# 单位换算表：(单位串, 量纲, 倍率)。长的写在前面——「元/股」必须先于「元」匹配，
# 否则 `0.86 元/股` 会被拆成 0.86 元再剩下「/股」，跟原句对不上。
UNITS = (
    ("元/股", "per_share", 1.0),
    ("亿股", "share", 1e8),
    ("亿元", "money", 1e8),
    ("万股", "share", 1e4),
    ("万元", "money", 1e4),
    ("元", "money", 1.0),
    ("股", "share", 1.0),
    ("％", "ratio", 1.0),
    ("%", "ratio", 1.0),
)
NUM_UNIT = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(%s)?" % "|".join(re.escape(u) for u, _d, _m in UNITS))
_UNIT_MAP = {u: (d, m) for u, d, m in UNITS}


# 取数前必须先剥掉的三类非数据字符。**引用编号 [S#] 也含数字**：不剥的话
# `「…0.86 元/股」[S1]` 会取出一个 bare 1.0，于是每一条正常登记行都恒多一个
# 「原句里找不到的数」——那是假红，不是判据错。锚段同理（页码、日期都在里面）。
CITE = re.compile(r"\[S\d+\]")
ANCHOR = re.compile(r"〔[^〕]*〕")


def _nums(s):
    """→ [(量纲, 基准值)]。无单位数的量纲记 `bare`，比对时与任意量纲都算。

    入口统一剥掉锚段与引用编号，再取数——这条清洗是所有调用点的共同前提，
    放在这里而不是各调用点各写一遍，免得漏一处又长出一支假红。
    """
    s = ANCHOR.sub("", CITE.sub("", s))
    out = []
    for m in NUM_UNIT.finditer(s):
        raw = m.group(1).replace(",", "")
        try:
            v = float(raw)
        except ValueError:
            continue
        unit = m.group(2)
        if unit:
            dim, mul = _UNIT_MAP[unit]
            out.append((dim, v * mul))
        else:
            out.append(("bare", v))
    return out


def _num_in(value, pool):
    """这个数在 pool 里找得到吗（同量纲或任一方是 bare，相对容差 1e-6）。"""
    dim, v = value
    for pdim, pv in pool:
        if dim != "bare" and pdim != "bare" and dim != pdim:
            continue
        if pv == v:
            return True
        if pv and abs(v - pv) / max(abs(pv), abs(v)) < 1e-6:
            return True
    return False


def check_calc(head, sections, stray):
    """道三 EP-CALC 基本每股收益的分子分母只认原句：登记的数必须能在同一行原句里找到。

    甲 登记了净利润数字（含扣非后），同一行「」原句里没有该数字 → 发
    乙 登记了加权平均普通股股数，同一行原句里没有该数字 → 发
    丙 登记了基本每股收益金额，同一行原句里没有该金额 → 发
    丁 行里出现本件自己算的痕迹（据此计算／＝／数字／数字 这类），而原句没给该结果 → 发

    单位不算没照抄：`17,200.00 万元` 与原句 `172,000,000.00 元` 是同一个数，按量纲折算后比对。
    「未取到」行不参与判定——缺口行本来就没有数可对。
    """
    out = []
    for name, _hline, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            s = s.strip()
            if not s or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s) or _is_gap_line(s):
                continue
            quotes = QUOTE.findall(s)
            if not quotes:
                continue                     # 没有原句：EP-QUOTE 那道管，这里不越界
            label, own = _split_label(_strip_quotes(s))
            pool = _nums("".join(quotes))

            if CALC_EPS_BASIC in label:
                kind = "基本每股收益"
            elif any(w in label for w in CALC_NET_PROFIT):
                kind = "净利润"
            elif any(w in label for w in CALC_SHARES):
                kind = "股数"
            else:
                continue                     # 不是这三族登记行，不归这道

            # 丁：有自算痕迹，且原句里根本没有这一族的结果数 → 先按「本件不许算」发。
            traced = any(t in own for t in SELF_CALC_TRACES) or bool(SELF_CALC_DIVIDE.search(own))
            if traced and not pool:
                out.append(("EP-CALC", lineno,
                            "「%s」写了自算痕迹而原句未给结果：本件只登记披露数，"
                            "不自行计算每股收益" % label[:16]))
                continue

            missing = [n for n in _nums(own) if not _num_in(n, pool)]
            if not missing:
                continue
            out.append(("EP-CALC", lineno,
                        "「%s」的登记数 %s 在同一行原句里找不到：分子分母与每股收益金额一律照抄披露，"
                        "不按净利润÷股数反算%s"
                        % (label[:16], _fmt_nums(missing),
                           "（行内有自算痕迹）" if traced else "")))
    return out


def _fmt_nums(ns):
    shown = []
    for dim, v in ns[:3]:
        if v == int(v) and abs(v) >= 1000:
            shown.append("%s%.0f" % (_DIM_UNIT.get(dim, ""), v))
        else:
            shown.append("%s%g" % (_DIM_UNIT.get(dim, ""), v))
    return "、".join(shown)


_DIM_UNIT = {"money": "¥", "share": "股/份额 ", "per_share": "¥/股 ", "ratio": "", "bare": ""}


# ---------------------------------------------------------------- EP-DILUTE

# 潜在普通股的四类。只收**名词形**，不收裸「稀释」——「稀释每股收益」是节名与指标名，
# 收进来会把每一条正常行都判红。这些词出现即须在同一行原句里也出现该类型词。
POTENTIAL_KINDS = ("可转换公司债券", "可转换债券", "可转债", "认股权证", "股份期权",
                   "可转换优先股", "限制性股票")

# 本件不得代披露下的两个判断。
DILUTE_JUDGE = ("具有反稀释性", "反稀释", "不计入稀释每股收益", "不纳入稀释每股收益")
DILUTE_ASSUME = ("假定转换", "假设转换", "假定行权", "假设行权")

# 调整项两族（登记值关键字 → 说明用）。
DILUTE_ADJ = ("调整后净利润", "调整后股数", "调整后普通股股数")


def check_dilute(head, sections, stray):
    """道四 EP-DILUTE 稀释每股收益的调整项只认原句。

    甲 登记了「调整后净利润／调整后股数」的数字，同一行「」原句里没有该数字 → 发
    乙 登记了潜在普通股类型词，该词必须也在同一行原句里 → 发
    丙 登记了「具有反稀释性／不计入稀释每股收益」，原句里没有该说法 → 发
        （反稀释是披露的判断，不是本件的）
    丁 行内写了「假定转换／假设转换」，原句里没有该说法 → 发

    「未取到」行不参与判定；〔自算〕行同样跳过——那类行的契约是交代取数口径，不是照抄。
    数比对走 `_nums`，入口已剥 `[S#]` 与〔锚〕，并做跨单位折算：
    `21,000.00 万股` 与 `210,000,000 股` 是同一个数，不算没照抄。
    """
    out = []
    for name, _hline, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, raw in body:
            s = raw.strip()
            if not s or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s) or _is_gap_line(s):
                continue
            quotes = QUOTE.findall(s)
            if not quotes:
                continue                     # 没有原句：EP-QUOTE 那道管，这里不越界
            if "〔自算〕" in s:
                continue                     # 自算行另有交代口径的义务，不归这道
            label, own = _split_label(_strip_quotes(s))
            qtext = "".join(quotes)
            pool = _nums(qtext)

            # 甲：调整项数字对不上原句
            if any(w in label for w in DILUTE_ADJ):
                missing = [n for n in _nums(own) if not _num_in(n, pool)]
                if missing:
                    out.append(("EP-DILUTE", lineno,
                                "「%s」的调整项 %s 在同一行原句里找不到：稀释的调整项一律照抄披露，"
                                "不按假定的转换价格自行补算" % (label[:16], _fmt_nums(missing))))
                    continue

            # 乙：潜在普通股类型词只出现在登记值里
            said = [k for k in POTENTIAL_KINDS if k in (label + own)]
            if said:
                absent = [k for k in said if k not in qtext]
                if absent:
                    out.append(("EP-DILUTE", lineno,
                                "「%s」写了潜在普通股「%s」而原句没有该表述：潜在普通股的类别"
                                "只有披露说了算" % (label[:16], absent[0])))
                    continue

            # 丙：反稀释／不计入，是披露的判断
            judge = [w for w in DILUTE_JUDGE if w in (label + own)]
            if judge and not any(w in qtext for w in DILUTE_JUDGE):
                out.append(("EP-DILUTE", lineno,
                            "「%s」写了「%s」而原句没有该判断：反稀释与是否计入稀释每股收益"
                            "是披露做的判断，不由本件下" % (label[:16], judge[0])))
                continue

            # 丁：假定转换的说法须与原句一致
            assume = [w for w in DILUTE_ASSUME if w in (label + own)]
            if assume and not any(w in qtext for w in DILUTE_ASSUME):
                out.append(("EP-DILUTE", lineno,
                            "「%s」写了「%s」而原句没有该说法：假定的转换／行权条件照抄披露"
                            % (label[:16], assume[0])))
                continue
    return out


# ---------------------------------------------------------------- EP-LINE

# 红线四族。甲投资建议／乙损益预测／丙评级与目标价／丁确定性断言。
# 「每股收益」「基本每股收益」「稀释每股收益」这类正常术语不在表内——那是本件的登记对象。
HARD_BAN = (
    # 甲 处置与投资建议
    "建议买入", "建议卖出", "建议增持", "建议减持", "建议建仓",
    # 乙 损益预测
    "预计每股收益", "预计增厚", "将增厚每股收益", "预计扭亏", "预计提升每股收益",
    # 丙 评级与目标价（只收评级语言，不收裸动词——裸「增持／减持」当普通词用时是
    #     合法登记语言：「本期减持库存股」是披露原文，不是评级意见）
    "评级", "目标价", "目标市值", "值得投资", "低估", "高估",
    "买入评级", "卖出评级", "增持评级", "减持评级", "给予买入", "给予卖出",
    "强烈推荐", "跑赢大盘",
    # 丁 确定性断言（收断言收益，不收裸「必然」——「必然导致…」可以是准则叙述）
    "稳赚", "零风险", "保证收益", "必然盈利", "必然上涨", "包赚",
)
# 这两节本来就在说该禁什么，判它等于自伤
LINE_EXEMPT_SECTION = ("合规红线", "数据通道")

# 紧邻红线词前面的否定词：边界声明（「本件不给评级、不给目标价」）不是评级意见。
# 只认紧贴着的那个词，不跨句、不跨逗号——「本件不给预测，但机构目标价 12.50 元」
# 里的「目标价」前面是空格不是否定词，照样发。
NEG_BEFORE = ("不给", "不予", "不作", "不出具", "不写", "不做", "不含", "不提",
              "不预测", "不提供", "不推荐", "不给出", "不得", "严禁", "禁止", "不")


def _negated(text, idx):
    """判 idx 处的红线词是不是被紧邻的否定词罩着（边界声明不是评级意见）。"""
    head = text[max(0, idx - 4):idx]
    return any(head.endswith(n) for n in NEG_BEFORE)


def check_line(head, sections, stray):
    """道五 EP-LINE 红线：投资建议、损益预测、评级与目标价、确定性断言零命中。

    只判本件自己写的句子：先 `_strip_quotes` 洗掉「」引文与〔锚〕，
    引文里出现禁用词不算（那是披露原文，本件只是照抄）。
    紧邻否定词罩着的命中不算——「本件不给评级、不给目标价」是边界声明，
    不是本件在下评级意见；罩不住的（「给出买入评级」「机构观点：目标价 12.50 元」）照发。
    节名含「合规红线」「数据通道」的整节跳过——那两节本来就要写这些词来说明自己不做什么。
    """
    out = []
    for name, _hline, body in sections:
        if any(w in name for w in LINE_EXEMPT_SECTION):
            continue
        for lineno, raw in body:
            s = raw.strip()
            if not s.startswith("- "):
                continue
            own = _strip_quotes(s)
            for w in HARD_BAN:
                if any(not _negated(own, m.start()) for m in re.finditer(re.escape(w), own)):
                    out.append(("EP-LINE", lineno,
                                "「%s」踩了红线词「%s」：投资建议、每股收益预测、"
                                "评级与目标价都不是本件的判项——%s"
                                % (_split_label(s)[0][:16], w, s[:40])))
                    break
    return out


CHECKS = (
    ("EP-STRUCT", check_struct),
    ("EP-QUOTE", check_quote),
    ("EP-CALC", check_calc),
    ("EP-DILUTE", check_dilute),
    ("EP-LINE", check_line),
)


# ---------------------------------------------------------------- 形制道具

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
    吞进去会让「多出一节」既不发 EP-STRUCT、又把下一节的发现行算到这一节头上。
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
    """只认两种登记形：行首 `未取到`，或 `项名：未取到…`。口径行不在其列。"""
    s = s.strip()
    if s.startswith("- "):
        s = s[2:].strip()
    if s.startswith("未取到"):
        return True
    return re.match(r"^[^：:]{1,16}[：:]\s*未取到", s) is not None


def _split_label(line):
    """项名与正文的界：`：`／`:`／空白里**最早出现**的那个。"""
    s = line.strip()
    if s.startswith("- "):
        s = s[2:].strip()
    cuts = [m.start() for m in re.finditer(r"[：:\s]", s)]
    if not cuts:
        return s, ""
    i = min(cuts)
    return s[:i].strip(), s[i + 1:].strip()


def _quotes(line):
    return QUOTE.findall(line)


def _strip_quotes(line):
    return ANCHOR_BLOCK.sub("", QUOTE.sub("", line))


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
                # 声明已落字的判据却仍抛未落字：按不合计，不装成「不可判」
                findings.append((code, 1, "判据声明已落字却抛未落字：%s" % exc))
    findings.sort(key=lambda x: (x[1], CODES.index(x[0])))
    return findings, unjudged


def report(path, findings, unjudged):
    for code, line, msg in findings:
        print("%s L%s %s" % (code, line, msg))
    for code, why in unjudged:
        print("不可判 %s（%s）" % (code, why))
    if findings:
        print("—— 机检：%d 条发条；判据未落字 %d 道，**这不等于合规**" % (len(findings), len(unjudged)))
    elif unjudged:
        print("—— 机检：0 条发条，但 %d 道判据尚未落字，**这不等于合规**" % len(unjudged))
    else:
        print("—— 机检：0 条发条")


DEMO = r"""# 示例科技股份有限公司 每股收益登记稿

- 〔AI 整理初稿〕〔请回原文核对〕〔不构成投资建议〕判断位 [待人工]
- 主体：示例科技股份有限公司
- 报告期：2025 年年度报告

## 每股收益概况

- 基本每股收益：0.86 元/股「本报告期基本每股收益为 0.86 元/股」〔锚：2025 年年报·第 78 页·附注九·每股收益〕[S1]
- 稀释每股收益：0.83 元/股「本报告期稀释每股收益为 0.83 元/股」〔锚：2025 年年报·第 78 页·附注九·每股收益〕[S1]

## 基本每股收益

- 归属于普通股股东的净利润：17,200.00 万元「归属于母公司普通股股东的净利润为 172,000,000.00 元」〔锚：2025 年年报·第 78 页·附注九·每股收益〕[S1]
- 扣除非经常性损益后净利润：15,600.00 万元「扣除非经常性损益后归属于普通股股东的净利润 156,000,000.00 元」〔锚：2025 年年报·第 78 页·附注九·每股收益〕[S1]
- 加权平均普通股股数：200,000,000 股「发行在外普通股的加权平均数为 200,000,000 股」〔锚：2025 年年报·第 78 页·附注九·每股收益〕[S1]

## 稀释每股收益

- 潜在普通股：可转换公司债券「本公司发行的可转换公司债券在转换前属于潜在普通股」〔锚：2025 年年报·第 79 页·附注九·每股收益〕[S1]
- 调整后净利润：17,500.00 万元「假定可转换公司债券当期期初转换为普通股，归属于普通股股东的净利润调整为 175,000,000.00 元」〔锚：2025 年年报·第 79 页·附注九·每股收益〕[S1]
- 调整后股数：210,000,000 股「假定转换后发行在外普通股加权平均数调整为 210,000,000 股」〔锚：2025 年年报·第 79 页·附注九·每股收益〕[S1]

## 股数与调整

- 报告期内股本变动：资本公积转增股本「本期以资本公积向全体股东每 10 股转增 2 股」〔锚：2025 年年报·第 79 页·附注九·每股收益〕[S1]
- 限制性股票：未取到：附注未披露限制性股票对每股收益的影响
- 库存股：未取到：附注未披露库存股对加权平均股数的影响

## 列报与追溯调整

- 列报位置：利润表「每股收益在利润表内单独列示」〔锚：2025 年年报·第 78 页·附注九·每股收益〕[S1]
- 追溯调整：按调整后股数重述上年可比数「因资本公积转增股本，按调整后的股数重新计算上年可比期间的每股收益」〔锚：2025 年年报·第 79 页·附注九·每股收益〕[S1]

## 口径与未取到

- 口径：基本每股收益的分子分母、稀释每股收益的全部调整项一律照抄披露，不由本件套公式补算
- 未取到：限制性股票对每股收益的影响
- 未取到：库存股对加权平均股数的影响

## 来源

- [S1] 示例科技股份有限公司 2025 年年度报告 | https://example.invalid/000000_2025_annual.pdf | 检索日 2026-11-14 | 类型：年报
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


BAD_STRUCT = _without_section(DEMO, "稀释每股收益")

BAD_QUOTE = DEMO.replace(
    "「本报告期基本每股收益为 0.86 元/股」〔锚：2025 年年报·第 78 页·附注九·每股收益〕[S1]",
    "0.86 元/股", 1)

# EP-CALC 坏样：把登记数改一个，原句还是原来那个数——登记数与原句对不上。
# 三元组一字不动，所以 EP-QUOTE 不该跟着红；只动一个数字，EP-STRUCT 也不该红。
BAD_CALC = DEMO.replace(
    "- 归属于普通股股东的净利润：17,200.00 万元「",
    "- 归属于普通股股东的净利润：17,300.00 万元「", 1)

# EP-CALC 反证：数字只在「」引文里，登记值不写数字（写「见原句」）。
# 这条必须零发条——它证明判据咬的是「登记数与原句对不上」，不是「没写数字就发」。
OK_CALC_QUOTED = DEMO.replace(
    "- 归属于普通股股东的净利润：17,200.00 万元「",
    "- 归属于普通股股东的净利润：见原句「", 1)

# ---- EP-DILUTE ----

# 乙 坏样：潜在普通股类型词只在登记值里，原句说的是另一种。
# 这条**只该发 EP-DILUTE**：EP-CALC 认的族是「净利润／归属于」「股数／加权平均」，
# 「潜在普通股」三字一个都不沾；三元组完整，EP-QUOTE 不红；行形制没动，EP-STRUCT 不红。
BAD_DILUTE_KIND = DEMO.replace(
    "- 潜在普通股：可转换公司债券「本公司发行的可转换公司债券在转换前属于潜在普通股」",
    "- 潜在普通股：认股权证「本公司发行的可转换公司债券在转换前属于潜在普通股」", 1)

# 乙 反证：类型词只在「」引文里，登记值写「无潜在普通股」——须零发条。
# 它证明判据咬的是「登记值里的类型词在原句里找不到」，不是「出现类型词就发」。
OK_DILUTE_QUOTED = DEMO.replace(
    "- 潜在普通股：可转换公司债券「本公司发行的可转换公司债券在转换前属于潜在普通股」",
    "- 潜在普通股：无潜在普通股「本公司发行的可转换公司债券在转换前属于潜在普通股」", 1)

# 甲 坏样：调整后股数与原句真正不相等（原句 210,000,000 股）。
# 注意这条会**同时**发 EP-CALC：`调整后股数` 这个标签里含「股数」，落在 EP-CALC 的股数族里，
# 两道都在判同一行的数。这是两把尺射程重叠，不是注入没放对——所以本档的期望码集是两枚，
# 不写成一枚冒充「只红一道」。
BAD_DILUTE_ADJ = DEMO.replace(
    "- 调整后股数：210,000,000 股「",
    "- 调整后股数：220,000,000 股「", 1)

# 甲 反证：跨单位折算后相等（21,000.00 万股 == 210,000,000 股）——须零发条。
# 这条钉的是「单位不同不算没照抄」，防止把量纲折算这一层写坏后整片误红。
OK_DILUTE_UNIT = DEMO.replace(
    "- 调整后股数：210,000,000 股「",
    "- 调整后股数：21,000.00 万股「", 1)

# ---- EP-LINE ----

# 坏样：在「股数与调整」节里插一条带完整三元组的目标价行。
# 三元组齐全，EP-QUOTE 不红；行形制没动，EP-STRUCT 不红；标签不带净利润／股数／调整项，
# EP-CALC 与 EP-DILUTE 都不认这一行——只该发 EP-LINE。
BAD_LINE = DEMO.replace(
    "- 报告期内股本变动：",
    "- 目标价：12.50 元「机构给出目标价 12.50 元」〔锚：2025 年年报·第 80 页〕[S1]\n"
    "- 报告期内股本变动：", 1)

# 反证一：同一个禁用词只出现在「」引文里、登记值写「未取到」——须零发条。
# 它钉的是「只判本件自己写的句子」：引文里出现目标价是披露原话，不是本件在下结论。
OK_LINE_QUOTED = DEMO.replace(
    "- 报告期内股本变动：",
    "- 机构观点：未取到「有机构给出目标价 12.50 元」〔锚：2025 年年报·第 80 页〕[S1]\n"
    "- 报告期内股本变动：", 1)

# 反证二：在已有的「口径与未取到」节里写边界声明——这一行不许发 EP-LINE，期望零发条。
# 放在真实存在的节里，就不必为这一档插第八节：八节契约本来就不收，插进去必撞 EP-STRUCT，
# 那会让本档只证明「结构那道会红」，红线豁免根本没测到。本档同时验两件事：
# 边界声明不误伤，且它落在真节里不撞结构。
OK_LINE_EXEMPT = DEMO.replace(
    "- 口径：基本每股收益的分子分母",
    "- 口径：本件不给评级、不给目标价。\n- 口径：基本每股收益的分子分母", 1)


def selftest():
    """逐档现报：好样须零发条，坏样须发出该道码；空壳道如实计「不可判」，不冒充绿。"""
    cases = (
        ("好样应零发条", DEMO, None),
        ("形制：删掉「稀释每股收益」整节", BAD_STRUCT, "EP-STRUCT"),
        ("锚：一条发现行拆掉三元组", BAD_QUOTE, "EP-QUOTE"),
        ("分子分母：登记数与原句对不上", BAD_CALC, "EP-CALC"),
        ("反证：数字只在原句里（不误伤）", OK_CALC_QUOTED, None),
        ("稀释：类型词只在登记值里", BAD_DILUTE_KIND, "EP-DILUTE"),
        ("反证：类型词只在原句里（不误伤）", OK_DILUTE_QUOTED, None),
        ("稀释：调整项与原句对不上（两尺射程重叠）", BAD_DILUTE_ADJ,
         ("EP-CALC", "EP-DILUTE")),
        ("反证：21,000.00 万股与 210,000,000 股折算相等", OK_DILUTE_UNIT, None),
        ("红线：正文写目标价", BAD_LINE, "EP-LINE"),
        ("反证：目标价只在引文里（不误伤）", OK_LINE_QUOTED, None),
        # 边界声明的反证：写在已有的「口径与未取到」节里，落字真节不撞结构，
        # 「不给」罩住「评级」「目标价」，故零发条。期望集为空——EP-LINE 或 EP-STRUCT
        # 任一枚冒出来都判不合。
        ("反证：边界声明「不给评级」不误伤", OK_LINE_EXEMPT, None),
    )
    bad = unk = 0
    print("── 自测 ──")
    for label, text, want in cases:
        findings, unjudged = check_text(text)
        pending = {code for code, _why in unjudged}
        got = set(c for c, _l, _m in findings)
        if isinstance(want, str):
            wantset = {want}
        elif want is None:
            wantset = set()
        else:
            wantset = set(want)
        # 「不可判」只对得上单码档有意义；多码档里只要有一枚未落字，整档都不可判。
        if wantset & pending:
            unk += 1
            print("  %-26s 不可判：%s 未落字，本档不作为绿也不作为红"
                  % (label, "／".join(sorted(wantset & pending))))
            continue
        ok = (got & wantset) == wantset and not (got - wantset - pending)
        if ok:
            print("  %-26s 码=%s 条数=%d OK（另有 %d 道未落字）"
                  % (label, ",".join(sorted(got)) or "无", len(findings), len(pending)))
        else:
            bad += 1
            print("  %-26s 期望 %s 实得 %s 不符" % (label, sorted(wantset) or "无", sorted(got) or "无"))
    for code in UNIMPLEMENTED:
        print("  %-26s 不可判：本拍未落字（不读成「零违例」）" % code)
    unk += len(UNIMPLEMENTED)
    print("——")
    print("自测档数=%d｜不合=%d｜不可判=%d" % (len(cases) + len(UNIMPLEMENTED), bad, unk))
    if bad:
        return 1
    return 3 if unk else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="每股收益逐条挂源稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="每股收益稿 .md 路径")
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
        print("缺入参：给一份每股收益稿路径，或用 --demo / --selftest", file=sys.stderr)
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
