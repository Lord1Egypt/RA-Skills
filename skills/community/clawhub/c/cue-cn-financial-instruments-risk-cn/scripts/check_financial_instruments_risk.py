#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""金融工具风险敞口登记稿五道机检（已落字：FR-STRUCT／FR-SENS／FR-LINE）。

本件读的是年报附注「金融工具及其风险」那一段登记的：
资产负债表日金融资产／金融负债的账面余额、按剩余到期期限分档的未折现现金流
（流动性风险）、利率风险的浮动利率敞口与敏感性影响、汇率风险的外币货币性项目
与敏感性影响、以及信用风险集中度（单一客户／交易对手最大敞口）。

它不判断流动性是否充裕、不判断偿债能力强弱，也不把敞口金额当已发生损失——
那些正是 FR-LINE 要拦的写法。

七节（逐字、按序）：
风险敞口概况／流动性风险／市场风险—利率／市场风险—汇率／信用风险集中度／
口径与未取到／来源

五道码：
FR-STRUCT 形制（已落字）｜FR-QUOTE 原句与锚｜FR-BUCKET 期限分档与合计｜
FR-SENS 敏感性重算（已落字）｜FR-LINE 红线（已落字）

零网络、纯标准库、单文件。
"""

import argparse
import contextlib
import io
import os
import re
import sys
import tempfile

SLUG = "cue-cn-financial-instruments-risk-cn"

CODES = ("FR-STRUCT", "FR-QUOTE", "FR-BUCKET", "FR-SENS", "FR-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议")

SECTIONS = ("风险敞口概况", "流动性风险", "市场风险—利率", "市场风险—汇率",
            "信用风险集中度", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"

# 五道全部落字；清单保持空。`want_rc` 与自证都从它现算，别手写死。
UNIMPLEMENTED = ()

HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")
TRIPLE = re.compile(
    r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)\|"
    r"\s*(?P<url>https?://\S+)\s*\|"
    r"\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$")

# FR-SENS 三件：`敞口 48,000.00 万元`／`变动 50 个基点` 或 `变动 5%`／`影响 240.00 万元`
_NUM = r"(?P<n>%s)" % r"\d[\d,]*(?:\.\d+)?"
SENS_EXPOSURE = re.compile(r"敞口\s*" + _NUM + r"\s*万元")
SENS_DELTA = re.compile(r"变动\s*" + _NUM + r"\s*(?P<u>个基点|%|％)")
SENS_IMPACT = re.compile(r"影响\s*" + _NUM + r"\s*万元")

# FR-QUOTE：金额形状（判定「数字行」用）与含数字判据
AMOUNT = re.compile(r"\d[\d,]*(?:\.\d+)?\s*(?:万元|元|亿元|%|％)")
NON_QUOTE = re.compile(r"[^\d\s.,%％:：/年月日\-]")
CITE = re.compile(r"\[(S\d+)\]")
AMOUNT_WAN = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*万元")

# FR-BUCKET：四个合法档名（中间是全角连接号 U+2013，与节名里的 U+2014 不同）
BUCKETS = ("1 年以内", "1–2 年", "2–5 年", "5 年以上")
BUCKET_TOL = 0.01
TOTAL_MARK = "合计"

# FR-LINE 四类红线词（每行每类只报第一处）
RED_LINES = (
    ("流动性／偿债判断", ("流动性充裕", "流动性紧张", "偿债能力充足",
                          "偿债能力不足", "短期偿债压力大")),
    ("把敞口说成已发生损失", ("已损失", "已减值", "已违约")),
    ("把敞口当实际还款额或可用资金", ("实际需偿还", "可动用", "实际可用")),
    ("评级或买卖建议", ("目标价", "买入", "卖出", "增持", "减持",
                        "评级为", "建议买入", "建议卖出")),
)


def _not_judged(code, why):
    """空壳的唯一出口：抛未落字，由 check_text 捕获计入「不可判」，**不返回空表**。"""
    raise NotImplementedError("%s 未落字：%s" % (code, why))


def check_struct(head, sections, stray):
    """道一 FR-STRUCT 形制：头部三件自标、七节齐且按序、野节逐条发。只判形。"""
    out = []
    htext = "\n".join(s for _i, s in head)
    for mark in MARK_TEXTS:
        if mark not in htext:
            out.append(("FR-STRUCT", 1, "头部缺自标「%s」" % mark))
    for lineno, raw in stray:
        out.append(("FR-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw))
    names = [n for n, _l, _b in sections]
    missing = [n for n in SECTIONS if n not in names]
    if missing:
        out.append(("FR-STRUCT", 1, "缺节：%s" % "／".join(missing)))
    elif names != list(SECTIONS):
        out.append(("FR-STRUCT", 1, "节序不对：现序 %s，应序 %s"
                    % ("／".join(names), "／".join(SECTIONS))))
    return out


def check_quote(head, sections, stray):
    """道二 FR-QUOTE：数字行须挂齐「」原句＋〔锚〕＋[S#]；来源与正文两向对上。

    **只认形、不核对数**——引号里的数与行首的数是否同一，是 FR-BUCKET／FR-SENS 的活；
    越界会让一支注入同时红两道。
    """
    out = []
    for _name, _lineno, body in _section_lines(sections, CONTENT_SECTIONS):
        for lineno, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_exempt_line(s):
                continue
            triples = list(TRIPLE.finditer(s))
            if not triples:
                if AMOUNT.search(s):
                    out.append(("FR-QUOTE", lineno,
                                "数字行未挂「」原句＋〔锚〕＋[S#] 三元组：%s" % s[:40]))
                continue
            for m in triples:
                q = m.group("q").strip()
                if len(q) < 8 or not NON_QUOTE.search(q):
                    out.append(("FR-QUOTE", lineno,
                                "原句不成句（不足 8 字或只有数字标点）：「%s」" % q))

    registered, src_lineno = set(), 1
    for _name, hline, body in _section_lines(sections, (SOURCE_SECTION,)):
        src_lineno = hline
        for lineno, raw in body:
            s = raw.strip()
            if not _is_finding_line(s):
                continue
            m = SOURCE_LINE.match(s)
            if not m:
                out.append(("FR-QUOTE", lineno,
                            "来源行不合格式，不算登记：%s" % s[:40]))
                continue
            registered.add(m.group("s"))
    if not registered:
        out.append(("FR-QUOTE", src_lineno, "来源节一条合规登记行都没有"))

    cited = set()
    for name, _lineno, body in sections:
        if name == SOURCE_SECTION:
            continue
        for _ln, raw in body:
            cited.update(CITE.findall(raw))
    for s_id in sorted(cited - registered):
        out.append(("FR-QUOTE", 1, "正文引了未登记的 [%s]" % s_id))
    for s_id in sorted(registered - cited):
        out.append(("FR-QUOTE", 1, "登记的 [%s] 未被任何正文行引用" % s_id))
    return out


def check_bucket(head, sections, stray):
    """道三 FR-BUCKET：期限分档之和 vs 该节披露的合计；档名须认得出。

    节缺**不归这道管**（那是 FR-LINE 的结构判据）；合计缺或一个合法档名都没认出
    时整条跳过，不猜、不按 0 算、不借别节的数。合计行本身不算分档行。
    """
    out = []
    body = None
    for name, _lineno, b in sections:
        if name == "流动性风险":
            body = b
            break
    if body is None:
        return out

    total, buckets = None, []
    for lineno, raw in body:
        s = raw.strip()
        if not _is_finding_line(s) or _is_exempt_line(s):
            continue
        amount = _own_amount(s)
        if amount is None:
            continue
        label = _own_label(s)
        if TOTAL_MARK in label:
            if total is None:
                total = amount
            continue
        buckets.append((lineno, label, amount))

    for lineno, label, _amount in buckets:
        if label not in BUCKETS:
            out.append(("FR-BUCKET", lineno, "认不出的档名：%s" % label))

    known = [a for _ln, label, a in buckets if label in BUCKETS]
    if total is None or not known:
        return out                          # 任一侧缺失：整条跳过
    s_sum = sum(known)
    if abs(s_sum - total) > BUCKET_TOL:
        out.append(("FR-BUCKET", 1, "分档和=%s 披露合计=%s"
                    % (_fmt(s_sum), _fmt(total))))
    return out


def check_sens(head, sections, stray):
    """道四 FR-SENS：行内同现三件时按 影响=敞口×幅度 重算，相对差 > 0.05% 即发。

    三件缺一即跳过，不从别处借数；敞口、幅度或披露影响为 0 时如实发「无从重算」，
    绝不静默除零。只认「」原句之前的自有部分，免得原句里的数被认进来。
    """
    out = []
    for name, _lineno, body in _section_lines(sections, CONTENT_SECTIONS):
        for lineno, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_exempt_line(s):
                continue
            own = _own_part(s)
            m_e = SENS_EXPOSURE.search(own)
            m_d = SENS_DELTA.search(own)
            m_i = SENS_IMPACT.search(own)
            if not (m_e and m_d and m_i):
                continue                       # 三件缺一：整条跳过
            exposure = _num(m_e.group("n"))
            delta = _num(m_d.group("n"))
            disclosed = _num(m_i.group("n"))
            if exposure == 0 or delta == 0 or disclosed == 0:
                out.append(("FR-SENS", lineno,
                            "此项无从重算（敞口=%s 变动=%s 披露影响=%s，有零值）"
                            % (_fmt(exposure), _fmt(delta), _fmt(disclosed))))
                continue
            if m_d.group("u") == "个基点":
                recomputed = exposure * delta / 10000.0
            else:
                recomputed = exposure * delta / 100.0
            if abs(recomputed - disclosed) / abs(disclosed) > 0.0005:
                out.append(("FR-SENS", lineno, "重算=%s 披露=%s（%s×%s%s）"
                            % (_fmt(recomputed), _fmt(disclosed),
                               _fmt(exposure), m_d.group("n"), m_d.group("u"))))
    return out


def check_line(head, sections, stray):
    """道五 FR-LINE：四类红线词＋「流动性风险」节缺。

    同一行同类只报第一处；口径节与来源节整节豁免（口径节按设计就要写
    「不判断流动性是否充裕」，不豁免会自己咬自己）。

    与 FR-SENS 不同，这里**判整行（含「」引号内的原句）**：红线是硬闸，
    一句「本集团流动性充裕」不论写成自家结论还是挂着锚的引文，都该被人看见一次；
    漏报比误报贵。只报第一处已足以避免同一句话刷屏。
    """
    out = []
    if not any(n == "流动性风险" for n, _l, _b in sections):
        out.append(("FR-LINE", 1, "缺「流动性风险」节——这一节是本件存在的理由"))
    exempt = (GAP_SECTION, SOURCE_SECTION)
    for name, _lineno, body in sections:
        if name in exempt:
            continue
        for lineno, raw in body:
            s = raw.strip()
            if not _is_finding_line(s):
                continue
            for label, words in RED_LINES:
                for w in words:
                    if w in s:
                        out.append(("FR-LINE", lineno,
                                    "%s：%s" % (label, w)))
                        break                      # 同一行同类只报第一处
    return out


CHECKS = (
    ("FR-STRUCT", check_struct),
    ("FR-QUOTE", check_quote),
    ("FR-BUCKET", check_bucket),
    ("FR-SENS", check_sens),
    ("FR-LINE", check_line),
)


# ---------------------------------------------------------------- 道具

def _section_of(heading):
    """`## 3. 流动性风险` → `流动性风险`；认不出返回 None（当 stray）。"""
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


def _own_amount(s):
    """→ 行首自有部分（「」之前、去掉〔口径〕括注）里第一个万元的金额；没有返回 None。"""
    own = _BRACKET.sub("", _own_part(s))
    m = AMOUNT_WAN.search(own)
    return _num(m.group(1)) if m else None


def _own_label(s):
    """→ 行首自有部分去掉〔口径〕括注与列表破折号、截到金额之前，得到档名／标签。"""
    label = _BRACKET.sub("", _own_part(s))
    m = AMOUNT_WAN.search(label)
    if m:
        label = label[:m.start()]
    label = label.strip()
    return label[2:].strip() if label.startswith("- ") else label.lstrip("-").strip()


def _section_lines(sections, names):
    want = tuple(names)
    return [(n, l, b) for n, l, b in sections if n in want]


def _num(s):
    """`48,000.00` → 48000.0；去千分位逗号。"""
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


DEMO = r"""# 示例材料（600000.SH）金融工具风险敞口登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议
主体：示例材料（600000.SH）
报告期：2025 年年度报告·附注·金融工具及其风险

## 风险敞口概况

- 金融资产合计〔口径：本期末账面余额〕182,400.00 万元「本集团金融资产账面余额合计为人民币 182,400.00 万元」〔锚：2025 年年报·第 232 页·金融工具及风险〕[S1]
- 金融负债合计〔口径：本期末账面余额〕121,600.00 万元「本集团金融负债账面余额合计为人民币 121,600.00 万元」〔锚：2025 年年报·第 232 页·金融工具及风险〕[S1]
- 金融资产占总资产比例〔自算〕67.5%（金融资产合计 ÷ 总资产合计 270,200.00 万元）

## 流动性风险

- 1 年以内〔口径：合同未折现现金流〕71,800.00 万元「本集团一年以内到期的金融负债按合同未折现现金流列示为人民币 71,800.00 万元」〔锚：2025 年年报·第 233 页·流动性风险〕[S1]
- 1–2 年〔口径：合同未折现现金流〕18,300.00 万元「本集团一至二年到期的金融负债按合同未折现现金流列示为人民币 18,300.00 万元」〔锚：2025 年年报·第 233 页·流动性风险〕[S1]
- 2–5 年〔口径：合同未折现现金流〕22,900.00 万元「本集团二至五年到期的金融负债按合同未折现现金流列示为人民币 22,900.00 万元」〔锚：2025 年年报·第 233 页·流动性风险〕[S1]
- 5 年以上〔口径：合同未折现现金流〕12,400.00 万元「本集团五年以上到期的金融负债按合同未折现现金流列示为人民币 12,400.00 万元」〔锚：2025 年年报·第 233 页·流动性风险〕[S1]
- 流动性风险合计〔口径：合同未折现现金流〕125,400.00 万元「本集团金融负债按合同未折现现金流的到期期限分析合计为人民币 125,400.00 万元」〔锚：2025 年年报·第 233 页·流动性风险〕[S1]

## 市场风险—利率

- 浮动利率借款〔口径：本期末〕48,000.00 万元「本集团浮动利率借款余额为人民币 48,000.00 万元」〔锚：2025 年年报·第 234 页·利率风险〕[S1]
- 利率敏感性〔口径：本期末敞口静态测算〕敞口 48,000.00 万元 变动 50 个基点 影响 240.00 万元「假设浮动利率上升 50 个基点，本集团税前利润将减少人民币 240.00 万元」〔锚：2025 年年报·第 234 页·利率风险〕[S1]

## 市场风险—汇率

- 外币货币性项目净额〔口径：本期末折合人民币〕9,600.00 万元「本集团外币货币性项目净额为人民币 9,600.00 万元」〔锚：2025 年年报·第 235 页·汇率风险〕[S1]
- 汇率敏感性〔口径：本期末敞口静态测算〕敞口 9,600.00 万元 变动 5% 影响 480.00 万元「假设人民币对美元贬值 5%，本集团税前利润将增加人民币 480.00 万元」〔锚：2025 年年报·第 235 页·汇率风险〕[S1]

## 信用风险集中度

- 单一客户最大信用敞口〔口径：本期末〕未取到：前五名客户逐户敞口金额

## 口径与未取到

- 未取到：前五名客户逐户敞口金额
- 口径：敞口金额、期限分档与敏感性影响一律照抄附注原文并挂原句与锚；本件不判断流动性是否充裕、不判断偿债能力强弱，也不把敞口金额当作已发生损失或可用资金。

## 来源

- [S1] 示例材料 2025 年年度报告·附注·金融工具及其风险 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026-03-20
"""


_CUT_FROM, _CUT_TO = "## 流动性风险\n", "## 市场风险—利率\n"
_i = DEMO.index(_CUT_FROM); _j = DEMO.index(_CUT_TO)
BAD_SECTION = DEMO[:_i] + DEMO[_j:]
assert BAD_SECTION != DEMO, "删节型注入没落地"


def _swap(text, old, new, why):
    """注入型夹具的唯一入口：替换必须真的落地，否则这一档自己就不成立。"""
    out = text.replace(old, new, 1)
    assert out != text, "注入没落地：%s" % why
    return out


# 注入位置＝节标题＋其后空行，行才落进**该节**（只锚标题会落进上一节）。
_HEAD_PROFILE = "## 风险敞口概况\n\n"
_HEAD_RATE = "## 市场风险—利率\n\n"


def selftest():
    """逐档现报；档数 = 逐档比对的档数 + UNIMPLEMENTED 的码数，**两段都从现场值算**。"""
    cases = (
        ("好样应零发条（五道全部落字）", DEMO, frozenset()),
        ("形制：头部删掉「不构成投资建议」",
         DEMO.replace("不构成投资建议", "", 1), frozenset({"FR-STRUCT"})),
        ("形制：节标题写成认不出的样子（进 stray＋缺节，红两道）",
         DEMO.replace("## 流动性风险\n", "## 流动性风险旧\n", 1),
         frozenset({"FR-STRUCT", "FR-LINE"})),
        ("形制：整节删掉「流动性风险」（红两道：缺节＋结构判据）",
         BAD_SECTION, frozenset({"FR-STRUCT", "FR-LINE"})),
        ("红线①：写上「流动性充裕」",
         _swap(DEMO, _HEAD_PROFILE, _HEAD_PROFILE +
               "- 流动性评价〔口径：本期末〕「本集团流动性充裕，可覆盖短期到期债务」"
               "〔锚：2025 年年报·第 232 页·金融工具及风险〕[S1]\n", "红线①"), frozenset({"FR-LINE"})),
        ("红线②：把敞口说成已减值",
         _swap(DEMO, _HEAD_PROFILE, _HEAD_PROFILE +
               "- 应收款项〔口径：本期末〕「上述金融资产已减值，预计无法收回」"
               "〔锚：2025 年年报·第 232 页·金融工具及风险〕[S1]\n", "红线②"), frozenset({"FR-LINE"})),
        ("红线③：把敞口金额当可用资金",
         _swap(DEMO, _HEAD_PROFILE, _HEAD_PROFILE +
               "- 授信额度〔口径：本期末〕「上述额度可动用，用于补充流动资金」"
               "〔锚：2025 年年报·第 232 页·金融工具及风险〕[S1]\n", "红线③"), frozenset({"FR-LINE"})),
        ("红线④：给目标价",
         _swap(DEMO, _HEAD_PROFILE, _HEAD_PROFILE +
               "- 估值观点〔口径：本期末〕「综合考虑后给予目标价 12.80 元」"
               "〔锚：2025 年年报·第 232 页·金融工具及风险〕[S1]\n", "红线④"), frozenset({"FR-LINE"})),
        ("敏感性：影响金额改 300.00（48,000×50/10000=240.00 对不上）",
         DEMO.replace("影响 240.00 万元", "影响 300.00 万元", 1), frozenset({"FR-SENS"})),
        ("敏感性：敞口写 0.00（应记「无从重算」而非崩）",
         _swap(DEMO, _HEAD_RATE, _HEAD_RATE +
               "- 利率敏感性二〔口径：本期末敞口静态测算〕敞口 0.00 万元 变动 50 个基点 "
               "影响 0.00 万元「假设浮动利率上升 50 个基点，本集团税前利润不受影响」"
               "〔锚：2025 年年报·第 234 页·利率风险〕[S1]\n", "敏感性零值"),
         frozenset({"FR-SENS"})),
        ("锚：拆掉原句与〔锚〕只留 [S1]",
         _swap(DEMO,
               "182,400.00 万元「本集团金融资产账面余额合计为人民币 182,400.00 万元」"
               "〔锚：2025 年年报·第 232 页·金融工具及风险〕[S1]",
               "182,400.00 万元 [S1]", "锚三元组"), frozenset({"FR-QUOTE"})),
        ("锚：来源行检索日写成斜杠式（不合格式、不算登记）",
         _swap(DEMO, "检索日 2026-03-20", "检索日 2026/03/20", "来源行日期"),
         frozenset({"FR-QUOTE"})),
        ("分档：合计改 130,000.00（分档和 125,400.00 对不上）",
         _swap(DEMO, "125,400.00", "130,000.00", "合计"), frozenset({"FR-BUCKET"})),
        ("分档：档名写成「一年以内」（认不出）",
         _swap(DEMO, "- 1 年以内〔口径", "- 一年以内〔口径", "档名"),
         frozenset({"FR-BUCKET"})),
    )
    bad = 0
    last_unjudged = ()
    for label, text, want in cases:
        findings, unjudged = check_text(text)
        last_unjudged = unjudged
        got = frozenset(c for c, _l, _m in findings)
        if got == want:
            print("过   %s（发条 %d 条：%s）" % (label, len(findings), "、".join(sorted(got)) or "无"))
        else:
            bad += 1
            print("不合 %s：期望 %s 实得 %s" % (label, sorted(want) or "无", sorted(got) or "无"))

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
                 "，输出含「不可判」与「这不等于合规」" if want_rc == 3 else "，输出无「这不等于合规」"))

    unk = len({c for c, _w in last_unjudged})
    print("——")
    print("自测档数=%d｜不合=%d｜不可判=%d" % (len(cases) + len(UNIMPLEMENTED), bad, unk))
    if bad:
        return 1
    return 3 if unk else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="金融工具风险敞口登记稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="金融工具风险敞口登记稿 .md 路径")
    ap.add_argument("--selftest", action="store_true", help="跑包内夹具自检")
    ap.add_argument("--demo", action="store_true", help="打印一份七节样例（零输入可跑）")
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
        print("缺入参：给一份金融工具风险敞口登记稿路径，或用 --demo / --selftest", file=sys.stderr)
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
