#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""应付职工薪酬登记稿五道机检（EB-STRUCT／EB-QUOTE／EB-ROLL／EB-PLAN／EB-LINE 均已落字）。

本件读的是年报附注「应付职工薪酬」那一段：短期薪酬、离职后福利（设定提存／
设定受益两类计划）、辞退福利与其他长期福利，以及薪酬总额的四数滚动。

五道均已落字，没有空壳：UNIMPLEMENTED 为空，任一码都不抛未落字。

五道判据如下（均已落字）：
  EB-STRUCT 形制：头部三件自标（AI 整理初稿／请回原文核对／不构成投资建议）要齐；
            六节齐且按序；不认识的节标题与多出的同名节逐条发。
  EB-QUOTE 溯源：四个内容节里每个带数字的行须挂齐「原句＋〔锚：…〕＋[S#]」三元组；
            正文引了没登记、登记了没被引用，两向都要发。
  EB-ROLL  恒等：概况四数恒等 期初 ＋ 本期增加 − 本期减少 ＝ 期末（万元，容差 0.01）。
            任一侧缺失 ⇒「口径与未取到」已写明未取到则跳过，否则发「缺数」，
            **不猜、不按 0 算**。
  EB-PLAN  分列：只扫「离职后福利」节；「设定提存计划」与「设定受益计划」两行必须分列
            （不能合成一行），缺哪行就发哪行；设定受益计划那几行里，折现率与精算
            利得／损失各至少要有一行。节缺失或节内无可判行时这一道不出声（缺节归
            EB-STRUCT 管），发条行号落在设定受益那行、缺行则落节标题行。
  EB-LINE  红线：四组越界词只在四个内容节扫，口径与未取到／来源 两节整节豁免。
            四组是 投资建议（买入／卖出／增持／减持／目标价／推荐／建议持有）、
            前瞻预测（预计／预测／有望／将会／看好／预期增长／预判）、
            主观评价（合理／不合理／偏高／偏低／高估／低估／显著偏低／显著偏高）、
            越界口径（人工成本率／人均创收／薪酬竞争力／裁员／降薪／优化人员／
            对标薪酬／行业均值／效率提升空间）。判整行（含「」引号内的原句），
            同一行内被更长词包含的短词不再重复报（「不合理」含「合理」⇒ 只报前者）。

退出码：0=五道都判过且零发条；1=有发条；2=用法错；3=读不了／空稿／仍有判据未落字。
**只有 rc=0 才等于「查过且干净」**——不可判一律落在 3，不混进 0。
末行档数由 `len(cases) + len(UNIMPLEMENTED)` 现算，不写死。

零网络、纯标准库、单文件；输入就是用户直供的附注文本。
"""
import argparse
import contextlib
import io
import os
import re
import sys
import tempfile

SLUG = "cue-cn-employee-benefits-cn"

CODES = ("EB-STRUCT", "EB-QUOTE", "EB-ROLL", "EB-PLAN", "EB-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议")

SECTIONS = ("应付职工薪酬概况", "短期薪酬", "离职后福利",
            "辞退福利与其他长期福利", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:4]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"

# 五道全部落字，清单为空。某道若回退成空壳就登记回这里：它会调用即抛、
# 被 check_text 收进「不可判」、单稿退 3——既不判也不放行，rc=0 只留给「五道全过」。
UNIMPLEMENTED = ()

HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")
TRIPLE = re.compile(
    r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)\|\s*(?P<url>https?://\S+)\s*\|\s*"
    r"检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$")
CITE = re.compile(r"\[(S\d+)\]")
AMOUNT_WAN = re.compile(r"([0-9][0-9,]*(?:\.[0-9]+)?)\s*万元")
AMOUNT = AMOUNT_WAN
NON_QUOTE = re.compile(r"[^\d\s,，.。、；;：:()（）\[\]〔〕「」%％\-—–/]")

# EB-LINE 四组越界词（薪酬题面专用；不是股份支付那套投资建议语境的词表）
REDLINES = (
    ("投资建议", ("买入", "卖出", "增持", "减持", "目标价", "推荐", "建议持有")),
    ("前瞻预测", ("预计", "预测", "有望", "将会", "看好", "预期增长", "预判")),
    ("主观评价", ("合理", "不合理", "偏高", "偏低", "高估", "低估",
                  "显著偏低", "显著偏高")),
    ("越界口径", ("人工成本率", "人均创收", "薪酬竞争力", "裁员", "降薪", "优化人员",
                  "对标薪酬", "行业均值", "效率提升空间")),
)


def _not_judged(code, why):
    """空壳的唯一出口：抛未落字，由 check_text 捕获计入「不可判」，**不返回空表**。"""
    raise NotImplementedError("%s 未落字：%s" % (code, why))


def check_struct(head, sections, stray):
    """道一 EB-STRUCT 形制：头部三件自标、六节齐且按序、野节逐条发。只判形。"""
    out = []
    htext = "\n".join(s for _i, s in head)
    for mark in MARK_TEXTS:
        if mark not in htext:
            out.append(("EB-STRUCT", 1, "头部缺自标「%s」" % mark))
    for lineno, raw in stray:
        out.append(("EB-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw))
    names = [n for n, _l, _b in sections]
    missing = [n for n in SECTIONS if n not in names]
    if missing:
        out.append(("EB-STRUCT", 1, "缺节：%s" % "／".join(missing)))
    elif names != list(SECTIONS):
        out.append(("EB-STRUCT", 1, "节序不对：现序 %s，应序 %s"
                    % ("／".join(names), "／".join(SECTIONS))))
    return out


def check_quote(head, sections, stray):
    """道二 EB-QUOTE：带数字的行须挂齐「」原句＋〔锚〕＋[S#]；来源与正文两向对上。

    只认形，不核对引号里的数与行首的数是否同一——那是 EB-ROLL 的活。
    """
    out = []
    for _name, _lineno, body in _section_lines(sections, CONTENT_SECTIONS):
        for lineno, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_exempt_line(s):
                continue
            own = _BRACKET.sub("", _own_part(s))
            if not re.search(r"[0-9]", own):
                continue
            if not TRIPLE.search(s):
                out.append(("EB-QUOTE", lineno, "带数字的行没挂齐「原句＋锚＋[S#]」"))

    cited = set()
    for _name, _lineno, body in _section_lines(sections, CONTENT_SECTIONS):
        for _ln, raw in body:
            cited |= set(CITE.findall(raw))

    declared = {}
    for _name, _lineno, body in _section_lines(sections, (SOURCE_SECTION,)):
        for lineno, raw in body:
            s = raw.strip()
            m = SOURCE_LINE.match(s)
            if m:
                declared.setdefault(m.group("s"), lineno)
    for s_id in sorted(cited - set(declared)):
        out.append(("EB-QUOTE", 1, "正文引用了来源里没有的 [%s]" % s_id))
    for s_id, lineno in sorted(declared.items(), key=lambda kv: kv[1]):
        if s_id not in cited:
            out.append(("EB-QUOTE", lineno,
                        "来源登记了 [%s] 但正文未引用" % s_id))
    return out


def check_roll(head, sections, stray):
    """道三 EB-ROLL：概况四数恒等 期初＋本期增加−本期减少＝期末（万元，容差 0.01）。

    缺数时不按 0 算：先看口径节是否**真的**声明了未取到——`未取到：无` 不算声明
    （那行字面也含「未取到」，只判关键字会把「什么都没缺」误读成「已声明缺数」，
    于是删掉一行的反例就永远不红）。必须解析冒号后的尾巴。同一标签匹配到多行时
    发「多义」并跳过比较，不瞎取第一条。
    """
    out = []
    body = None
    for name, _lineno, b in sections:
        if name == "应付职工薪酬概况":
            body = b
            break
    if body is None:
        return out

    wanted = ("期初余额", "本期增加", "本期减少", "期末余额")
    hits = {k: [] for k in wanted}
    for lineno, raw in body:
        s = raw.strip()
        if not _is_finding_line(s) or _is_exempt_line(s):
            continue
        label = _BRACKET.sub("", _own_part(s))
        m = AMOUNT_WAN.search(label)
        if not m:
            continue
        for key in wanted:
            if key in label:
                hits[key].append((lineno, _num(m.group(1))))
                break

    ambiguous = []
    for key in wanted:
        if len(hits[key]) > 1:
            ambiguous.append(("EB-ROLL", hits[key][1][0],
                              "多义：%s 匹配到 %d 行，不敢比"
                              % (key, len(hits[key]))))
    if ambiguous:
        return out + ambiguous

    missing = [k for k in wanted if not hits[k]]
    if missing:
        if _gap_declared(sections):
            return out                     # 口径节真声明了缺数 ⇒ 跳过本道
        out.append(("EB-ROLL", 1, "缺数：%s" % "／".join(missing)))
        return out

    open_bal = hits["期初余额"][0][1]
    add = hits["本期增加"][0][1]
    less = hits["本期减少"][0][1]
    close_lineno, close = hits["期末余额"][0]
    calc = open_bal + add - less
    # 先归到分位再比：浮点下 |13,800.00 - 13,800.01| 会算成 0.010000000002，
    # 直接 > 0.01 会把正好差一分的稿子误红。round 到两位是在做十进制定点比较，
    # 不是放宽容差——差 0.02 照样红。
    diff = round(calc - close, 2)
    if abs(diff) > 0.01:
        out.append(("EB-ROLL", close_lineno,
                    "期初 %s ＋ 增加 %s − 减少 %s ＝ %s ≠ 期末 %s（差 %s）"
                    % (_fmt(open_bal), _fmt(add), _fmt(less),
                       _fmt(calc), _fmt(close), _fmt(diff))))
    return out


def check_plan(head, sections, stray):
    """道四 EB-PLAN：只扫「离职后福利」节——两计划分列、受益计划的两项要件。

    该节没有 `- ` 行时返回空表不报：缺节归 EB-STRUCT。「折现率」「精算利得／损失」
    只在有设定受益计划时才要求，行号用设定受益那一行。
    """
    out = []
    body = first_lineno = None
    for name, hline, b in sections:
        if name == "离职后福利":
            body, first_lineno = b, hline
            break
    if body is None:
        return out

    rows = [(ln, raw.strip()) for ln, raw in body if _is_finding_line(raw.strip())]
    if not rows:
        return out                          # 空节不报，形制那道管缺节
    heading_lineno = first_lineno

    have_ti, have_bi = None, None
    for ln, s in rows:
        label = _BRACKET.sub("", _own_part(s))
        if "设定提存" in s and "设定受益" in s:
            out.append(("EB-PLAN", ln, "设定提存与设定受益被合成一行，必须分列"))
        if "设定提存" in label and have_ti is None:
            have_ti = (ln, s)
        if "设定受益" in label and have_bi is None:
            have_bi = (ln, s)

    if have_ti is None:
        out.append(("EB-PLAN", heading_lineno, "离职后福利节缺「设定提存计划」一行"))
    if have_bi is None:
        out.append(("EB-PLAN", heading_lineno, "离职后福利节缺「设定受益计划」一行"))
        return out

    bi_lineno = have_bi[0]
    has_rate = any("折现率" in _BRACKET.sub("", _own_part(s)) for _ln, s in rows)
    has_act = any(("精算利得" in _BRACKET.sub("", _own_part(s))
                   or "精算损失" in _BRACKET.sub("", _own_part(s)))
                  for _ln, s in rows)
    if not has_rate:
        out.append(("EB-PLAN", bi_lineno, "设定受益计划缺折现率一行"))
    if not has_act:
        out.append(("EB-PLAN", bi_lineno, "设定受益计划缺精算利得／损失一行"))
    return out


def check_line(head, sections, stray):
    """道五 EB-LINE：四组越界词只扫四个内容节，口径节与来源节整节豁免。

    同一行同一组命中多个词时，只留不被别的命中词包含的那些（「不合理」含「合理」、
    「显著偏低」含「偏低」）；互不包含的照样各报一条。
    """
    out = []
    for _name, _lineno, body in _section_lines(sections, CONTENT_SECTIONS):
        for lineno, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_exempt_line(s):
                continue
            for group, words in REDLINES:
                hit = [w for w in words if w in s]
                keep = [w for w in hit
                        if not any(w != o and w in o for o in hit)]
                for w in keep:
                    out.append(("EB-LINE", lineno, "红线词：%s（%s）" % (w, group)))
    return out


CHECKS = (
    ("EB-STRUCT", check_struct),
    ("EB-QUOTE", check_quote),
    ("EB-ROLL", check_roll),
    ("EB-PLAN", check_plan),
    ("EB-LINE", check_line),
)


# ---------------------------------------------------------------- 道具

def _section_of(heading):
    """`## 3. 短期薪酬` → `短期薪酬`；认不出返回 None（当 stray）。"""
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
    """→ (头部, [(节名, 标题行号, [(行号, 行)])], 野节)。野节另记、不吞进上一节。"""
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
    return "未取到" in s


def _is_exempt_line(s):
    """按设计不带三元组的三形：`未取到：`／`[待人工]`／`〔自算〕`。"""
    return _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s


def _own_part(s):
    return s.split("「", 1)[0].strip()


_BRACKET = re.compile(r"〔[^〕]*〕")


def _section_lines(sections, names):
    want = tuple(names)
    return [(n, l, b) for n, l, b in sections if n in want]


_EMPTY_TAILS = ("无", "無", "None", "none", "—", "-", "–")


def _gap_declared(sections):
    """口径节是否**真的**声明了未取到：解析冒号后的尾巴，非空且非空值词才算。

    `- 未取到：无` 字面含「未取到」，但它说的是「没缺」——只判关键字会把
    这份稿子误读成「已声明缺数」，于是删掉一行的反例就永远不红。
    """
    for _name, _lineno, body in _section_lines(sections, (GAP_SECTION,)):
        for _ln, raw in body:
            s = raw.strip()
            if "未取到" not in s:
                continue
            tail = s.split("未取到", 1)[1].lstrip("：:").strip()
            if tail and tail not in _EMPTY_TAILS:
                return True
    return False


def _num(s):
    """`12,400.00` → 12400.0；去千分位逗号。"""
    return float(s.replace(",", ""))


def _fmt(x):
    """金额统一留两位小数。"""
    return "%.2f" % x


def check_text(text):
    """→ (findings[(code, line, msg)], unjudged[(code, why)])。

    空壳抛 NotImplementedError 一律计 unjudged，**不计入「零发条」**、也不裸抛；
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


def _report_text(path, findings, unjudged):
    """纯函数：拼报告文本返回，**不 print**。打印走的也是这一段，两条路径同一段字节。"""
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
    sys.stdout.write(_report_text(path, findings, unjudged))


# 好样的四数（万元）先在这里自洽：12,400.00 ＋ 8,600.00 − 7,200.00 ＝ 13,800.00。
DEMO = r"""# 示例材料（600000.SH）应付职工薪酬登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议
主体：示例材料（600000.SH）
报告期：2025 年年度报告·附注·应付职工薪酬

## 应付职工薪酬概况

- 期初余额〔口径：本期末〕12,400.00 万元「本集团应付职工薪酬年初余额为人民币 12,400.00 万元」〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]
- 本期增加〔口径：本期发生额〕8,600.00 万元「本集团本期应付职工薪酬增加额为人民币 8,600.00 万元」〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]
- 本期减少〔口径：本期发生额〕7,200.00 万元「本集团本期应付职工薪酬减少额为人民币 7,200.00 万元」〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]
- 期末余额〔口径：本期末〕13,800.00 万元「本集团应付职工薪酬期末余额为人民币 13,800.00 万元」〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]

## 短期薪酬

- 工资、奖金、津贴和补贴〔口径：本期发生额〕6,900.00 万元「短期薪酬中工资、奖金、津贴和补贴本期发生额为人民币 6,900.00 万元」〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]
- 职工福利费〔口径：本期发生额〕420.00 万元「短期薪酬中职工福利费本期发生额为人民币 420.00 万元」〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]

## 离职后福利

- 设定提存计划〔口径：本期发生额〕960.00 万元「本集团按既定比例向基本养老保险及企业年金缴存，设定提存计划本期缴费金额为人民币 960.00 万元」〔锚：2025 年年报·第 259 页·离职后福利〕[S1]
- 设定受益计划〔口径：本期末〕320.00 万元「本集团设定受益计划净负债现值为人民币 320.00 万元」〔锚：2025 年年报·第 259 页·离职后福利〕[S1]
- 折现率〔口径：本期末〕3.25%「设定受益计划义务现值按 3.25% 的折现率计算」〔锚：2025 年年报·第 259 页·离职后福利〕[S1]
- 精算损失〔口径：本期发生额〕18.00 万元「设定受益计划本期确认精算损失人民币 18.00 万元」〔锚：2025 年年报·第 259 页·离职后福利〕[S1]

## 辞退福利与其他长期福利

- 辞退福利〔口径：本期发生额〕150.00 万元「本集团本期确认辞退福利人民币 150.00 万元」〔锚：2025 年年报·第 260 页·应付职工薪酬〕[S1]

## 口径与未取到

- 未取到：无
- 口径：薪酬总额、各明细项目与两类离职后福利计划一律照抄附注原文并挂原句与锚；本件不判断薪酬水平高低、不预测以后期间的人工成本，也不把应付职工薪酬当作可支配资金。

## 来源

- [S1] 示例材料 2025 年年度报告·附注·应付职工薪酬 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026-03-20
"""


def _swap(text, old, new, why):
    """注入型夹具的唯一入口：替换必须真的落地，否则这一档自己就不成立。"""
    out = text.replace(old, new, 1)
    assert out != text, "注入没落地：%s" % why
    return out


def selftest():
    """逐档现报；档数 = 逐档比对的档数 + UNIMPLEMENTED 的码数，**两段都从现场值算**。"""
    _i = DEMO.index("## 短期薪酬")
    _j = DEMO.index("## 离职后福利")
    bad_section = DEMO[:_i] + DEMO[_j:]
    assert bad_section != DEMO, "删节型注入没落地"
    cases = (
        ("好样应零发条（EB-STRUCT／EB-QUOTE／EB-ROLL 已落字，其余计不可判）", DEMO, frozenset()),
        ("形制：头部删掉「不构成投资建议」",
         _swap(DEMO, "不构成投资建议", "", "头部自标"), frozenset({"EB-STRUCT"})),
        ("形制：节标题写成认不出的样子（进 stray＋缺节）",
         _swap(DEMO, "## 短期薪酬\n", "## 短期薪酬明细\n", "节标题"),
         frozenset({"EB-STRUCT"})),
        ("形制：整节删掉「短期薪酬」", bad_section, frozenset({"EB-STRUCT"})),
        ("形制：节序颠倒（把「离职后福利」挪到「短期薪酬」之前；红两道："
         "节序错＋两计划都不在该节里）",
         _swap(DEMO, "## 短期薪酬\n", "## 离职后福利\n", "节序"),
         frozenset({"EB-STRUCT", "EB-PLAN"})),
        ("形制：末尾多出一个同名节「来源」",
         _swap(DEMO, "## 来源\n\n",
               "## 来源\n\n- [S1] 重复登记 | https://example.invalid/x.pdf | 检索日 2026-03-20\n\n## 来源\n\n",
               "同名节"),
         frozenset({"EB-STRUCT"})),
        ("溯源：删掉某数字行的〔锚：…〕（整数行没挂齐三元组）",
         _swap(DEMO, "〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]\n- 本期增加",
               "[S1]\n- 本期增加", "锚缺"),
         frozenset({"EB-QUOTE"})),
        ("溯源：来源节多登记一条正文没引用的 [S2]",
         _swap(DEMO, "## 来源\n\n",
               "## 来源\n\n- [S2] 未引用登记 | https://example.invalid/y.pdf | 检索日 2026-03-20\n",
               "多登记"),
         frozenset({"EB-QUOTE"})),
        ("溯源：正文某处 [S1] 改成来源里没有的 [S9]",
         _swap(DEMO, "〔锚：2025 年年报·第 259 页·离职后福利〕[S1]",
               "〔锚：2025 年年报·第 259 页·离职后福利〕[S9]", "未登记引用"),
         frozenset({"EB-QUOTE"})),
        ("滚动：期末余额改 13,900.00（12,400＋8,600−7,200=13,800 对不上）",
         _swap(DEMO, "13,800.00 万元「本集团应付职工薪酬期末余额",
               "13,900.00 万元「本集团应付职工薪酬期末余额", "期末余额"),
         frozenset({"EB-ROLL"})),
        ("滚动：删掉「本期减少」行（口径节仍是「未取到：无」⇒ 未被豁免）",
         _swap(DEMO, "- 本期减少〔口径：本期发生额〕7,200.00 万元「本集团本期应付职工薪酬减少额为人民币 7,200.00 万元」〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]\n", "", "删本期减少"),
         frozenset({"EB-ROLL"})),
        ("滚动：删掉「本期减少」且口径节改成「未取到：本期减少额」⇒ 零发条（豁免生效）",
         _swap(_swap(DEMO, "- 本期减少〔口径：本期发生额〕7,200.00 万元「本集团本期应付职工薪酬减少额为人民币 7,200.00 万元」〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]\n", "", "删本期减少"),
               "- 未取到：无", "- 未取到：本期减少额", "声明缺数"),
         frozenset()),
        ("计划：删掉「设定提存计划」一行",
         _swap(DEMO, "- 设定提存计划〔口径：本期发生额〕960.00 万元「本集团按既定比例向基本养老保险及企业年金缴存，设定提存计划本期缴费金额为人民币 960.00 万元」〔锚：2025 年年报·第 259 页·离职后福利〕[S1]\n", "", "删设定提存"),
         frozenset({"EB-PLAN"})),
        ("计划：删掉「设定受益计划」一行",
         _swap(DEMO, "- 设定受益计划〔口径：本期末〕320.00 万元「本集团设定受益计划净负债现值为人民币 320.00 万元」〔锚：2025 年年报·第 259 页·离职后福利〕[S1]\n", "", "删设定受益"),
         frozenset({"EB-PLAN"})),
        ("计划：两计划合成一行",
         _swap(DEMO, "- 设定提存计划〔口径：本期发生额〕960.00 万元",
               "- 设定提存计划与设定受益计划〔口径：本期发生额〕960.00 万元", "合行"),
         frozenset({"EB-PLAN"})),
        ("计划：删掉「折现率」一行",
         _swap(DEMO, "- 折现率〔口径：本期末〕3.25%「设定受益计划义务现值按 3.25% 的折现率计算」〔锚：2025 年年报·第 259 页·离职后福利〕[S1]\n", "", "删折现率"),
         frozenset({"EB-PLAN"})),
        ("计划：删掉「精算损失」一行",
         _swap(DEMO, "- 精算损失〔口径：本期发生额〕18.00 万元「设定受益计划本期确认精算损失人民币 18.00 万元」〔锚：2025 年年报·第 259 页·离职后福利〕[S1]\n", "", "删精算损失"),
         frozenset({"EB-PLAN"})),
        ("红线：内容节插一行含「预计」（三元组挂齐，不惊动 EB-QUOTE）",
         _swap(DEMO, "## 短期薪酬\n\n",
               "## 短期薪酬\n\n"
               "- 薪酬展望〔口径：本期末〕「预计明年人工成本将保持稳定」"
               "〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]\n", "前瞻预测"),
         frozenset({"EB-LINE"})),
        ("红线：内容节插一行含「降薪」（三元组挂齐）",
         _swap(DEMO, "## 短期薪酬\n\n",
               "## 短期薪酬\n\n"
               "- 人员政策〔口径：本期末〕「本集团本年度未实施降薪」"
               "〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]\n", "越界口径"),
         frozenset({"EB-LINE"})),
        ("红线：往口径节再写一句含「预计」⇒ 零发条（整节豁免）",
         _swap(DEMO, "也不把应付职工薪酬当作可支配资金。",
               "也不把应付职工薪酬当作可支配资金，本件不预计以后期间的薪酬水平。",
               "口径豁免"),
         frozenset()),
    )
    # 「恰好 2 条」这一档必须数条数，不是数码集合：不能并入上面的 want 比较。
    _dedup_text = _swap(DEMO, "## 短期薪酬\n\n",
                        "## 短期薪酬\n\n"
                        "- 水平评价〔口径：本期末〕「管理层认为该水平不合理且显著偏低」"
                        "〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]\n", "去重")
    # 单列档（只数条数、不比较码集合）的枚数：自己数，别手写进档数表达式。
    extra_cases = 1
    bad = 0
    last_unjudged = ()
    for label, text, want in cases:
        findings, unjudged = check_text(text)
        last_unjudged = unjudged
        got = frozenset(c for c, _l, _m in findings)
        if got == want:
            print("过   %s（发条 %d 条：%s）" % (label, len(findings),
                                              "、".join(sorted(got)) or "无"))
        else:
            bad += 1
            print("不合 %s：期望 %s 实得 %s"
                  % (label, sorted(want) or "无", sorted(got) or "无"))

    # 单列一档：这一档判的是**条数**而不是码集合（去重后应恰好 2 条，合并成 1 条即错）。
    # 它同样进档数，所以 cases 的长度要把它算上——见下方档数表达式。
    _df, _du = check_text(_dedup_text)
    last_unjudged = _du
    _dl = [m for c, _l, m in _df if c == "EB-LINE"]
    if len(_dl) == 2:
        print("过   红线去重：一行含「不合理」与「显著偏低」⇒ 恰好 2 条（%s）"
              % "；".join(_dl))
    else:
        bad += 1
        print("不合 红线去重：期望恰好 2 条，实得 %d 条（%s）"
              % (len(_dl), "；".join(_dl) or "无"))

    implemented = [c for c in CODES if c not in UNIMPLEMENTED]
    covered = set()
    for _label, text, want in cases:
        if text is not None:
            covered |= set(want)
    uncovered = [c for c in implemented if c not in covered]
    print("%s 覆盖自证：已落字码 %d 道，有反例的 %d 道，缺反例：%s"
          % ("不合" if uncovered else "过  ", len(implemented),
             len(implemented) - len(uncovered), "／".join(uncovered) if uncovered else "无"))
    if uncovered:
        bad += 1

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
        print("过   空壳自证（未落字清单为空：五道均不抛未落字、均返回列表，无空壳可留）")

    crash = []
    for label, text in (("空稿", ""), ("乱头", "x\n"), ("只头无节", DEMO.split("## ")[0])):
        try:
            _f2, u2 = check_text(text)
        except Exception as exc:                       # noqa: BLE001
            crash.append("%s 抛出 %s: %s" % (label, type(exc).__name__, exc))
            continue
        got_codes = {c for c, _w in u2}
        if got_codes != set(UNIMPLEMENTED):
            crash.append("%s 不可判 %s，应为 %s"
                         % (label, sorted(got_codes) or "无", sorted(UNIMPLEMENTED) or "无"))
    if crash:
        bad += 1
        print("不合 不崩自证：%s" % "；".join(crash))
    else:
        print("过   不崩自证（空稿／乱头／只头无节均返回二元组，未落字 %d 道计不可判）"
              % len(UNIMPLEMENTED))

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
                 "，输出含「不可判」与「这不等于合规」" if want_rc == 3
                 else "，输出无「这不等于合规」"))

    unk = len({c for c, _w in last_unjudged})
    print("——")
    print("自测档数=%d｜不合=%d｜不可判=%d"
          % (len(cases) + extra_cases + len(UNIMPLEMENTED), bad, unk))
    if bad:
        return 1
    return 3 if unk else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="应付职工薪酬登记稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="应付职工薪酬登记稿 .md 路径")
    ap.add_argument("--selftest", action="store_true", help="跑包内夹具自检")
    ap.add_argument("--demo", action="store_true", help="打印一份六节样例（零输入可跑）")
    try:
        args = ap.parse_args(argv)
    except SystemExit:                                 # 用法错统一退 2
        return 2

    if args.selftest:
        return selftest()
    if args.demo:
        sys.stdout.write(DEMO)
        return 0
    if not args.path:
        ap.print_usage(sys.stderr)
        print("缺入参：给一份应付职工薪酬登记稿路径，或用 --demo / --selftest",
              file=sys.stderr)
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
