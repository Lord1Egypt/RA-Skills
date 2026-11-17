#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""终止经营登记稿五道机检（骨架／形状参考，不是成品）。

形状参考：本文件是给派单对象的「照着写」样本，**自己先跑通再派**。
现状 `UNIMPLEMENTED` 登记四道，只有 TO-STRUCT 落字；`--selftest` 末行应为
「自测档数=6｜不合=0｜不可判=4」。

零网络、纯标准库、单文件；输入就是用户直供的附注文本。
"""
import argparse
import contextlib
import io
import os
import re
import sys
import tempfile

SLUG = "cue-cn-terminated-operations-cn"

CODES = ("TO-STRUCT", "TO-QUOTE", "TO-PL", "TO-CASH", "TO-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议")

SECTIONS = ("终止经营概况", "终止经营损益", "终止经营现金流量",
            "持有待售资产与负债", "处置损益与对价", "口径与未取到", "来源")
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
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)\|\s*(?P<url>https?://\S+)\s*\|\s*"
    r"检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$")
CITE = re.compile(r"\[(S\d+)\]")
AMOUNT_WAN = re.compile(r"([0-9][0-9,]*(?:\.[0-9]+)?)\s*万元")
AMOUNT = AMOUNT_WAN
NON_QUOTE = re.compile(r"[^\d\s,，.。、；;：:()（）\[\]〔〕「」%％\-—–/]")

TOTAL_MARK = "合计"

# TO-PL：损益分项里金额可能带负号（成本、费用），金额比对容差 0.01 万元。
PL_TOL = 0.01
PL_AMOUNT = re.compile(
    r"(?P<sign>[-+−])?\s*(?P<n>[0-9][0-9,]*(?:\.[0-9]+)?)\s*万元")

# TO-CASH：经营／投资活动两项之和与同节合计比对，容差同 PL。
CASH_TOL = 0.01
CASH_OP_MARK = "经营活动"
CASH_INV_MARK = "投资活动"

# TO-LINE 四类红线词（每行每类只报第一处）。词表照派单原样，未自行扩展：
# 扩词要有语料校准才敢动，这里没有可校准的东西，拿不准就不写。
RED_LINES = (
    ("判断处置是否划算／好坏", ("处置划算", "处置不划算", "卖亏了",
                              "一卖了之", "甩包袱")),
    ("把处置损益当可持续利润", ("可持续利润", "经常性损益", "主业改善",
                              "盈利能力提升")),
    ("预测处置对以后期间的影响", ("预计明年", "将增厚业绩", "未来业绩将",
                                "可增厚利润")),
    ("评级或买卖建议", ("目标价", "买入", "卖出", "增持", "减持",
                        "评级为", "建议买入", "建议卖出")),
)


def _not_judged(code, why):
    """空壳的唯一出口：抛未落字，由 check_text 捕获计入「不可判」，**不返回空表**。"""
    raise NotImplementedError("%s 未落字：%s" % (code, why))


def check_struct(head, sections, stray):
    """道一 TO-STRUCT 形制：头部三件自标、七节齐且按序、野节逐条发。只判形。"""
    out = []
    htext = "\n".join(s for _i, s in head)
    for mark in MARK_TEXTS:
        if mark not in htext:
            out.append(("TO-STRUCT", 1, "头部缺自标「%s」" % mark))
    for lineno, raw in stray:
        out.append(("TO-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw))
    names = [n for n, _l, _b in sections]
    missing = [n for n in SECTIONS if n not in names]
    if missing:
        out.append(("TO-STRUCT", 1, "缺节：%s" % "／".join(missing)))
    elif names != list(SECTIONS):
        out.append(("TO-STRUCT", 1, "节序不对：现序 %s，应序 %s"
                    % ("／".join(names), "／".join(SECTIONS))))
    return out


def check_quote(head, sections, stray):
    """道二 TO-QUOTE：数字行须挂齐「」原句＋〔锚〕＋[S#]；来源与正文两向对上。

    **只认形、不核对引号里的数与行首的数是否同一**——那是 TO-PL／TO-CASH 的活；
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
                    out.append(("TO-QUOTE", lineno,
                                "数字行未挂「」原句＋〔锚〕＋[S#] 三元组：%s" % s[:40]))
                continue
            for m in triples:
                q = m.group("q").strip()
                if len(q) < 8 or not NON_QUOTE.search(q):
                    out.append(("TO-QUOTE", lineno,
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
                out.append(("TO-QUOTE", lineno,
                            "来源行不合格式，不算登记：%s" % s[:40]))
                continue
            registered.add(m.group("s"))
    if not registered:
        out.append(("TO-QUOTE", src_lineno, "来源节一条合规登记行都没有"))

    cited = set()
    for name, _lineno, body in sections:
        if name == SOURCE_SECTION:
            continue
        for _ln, raw in body:
            cited.update(CITE.findall(raw))
    for s_id in sorted(cited - registered):
        out.append(("TO-QUOTE", 1, "正文引了未登记的 [%s]" % s_id))
    for s_id in sorted(registered - cited):
        out.append(("TO-QUOTE", 1, "登记的 [%s] 未被任何正文行引用" % s_id))
    return out


def check_pl(head, sections, stray):
    """道三 TO-PL：「终止经营损益」节分项之和 vs「终止经营概况」节披露的净利润。

    负号在这里自己解析（`PL_AMOUNT` 认 `-`／`+`／全角负号），不动共享的 `_own_amount`——
    那条路径 TO-QUOTE 也在走，改它容易带坏别的判据。任一侧缺失 ⇒ 整条跳过。
    """
    out = []
    parts, net_profit = [], None
    for name, _lineno, body in sections:
        if name == "终止经营损益":
            for lineno, raw in body:
                s = raw.strip()
                if not _is_finding_line(s) or _is_exempt_line(s):
                    continue
                amt = _pl_amount(s)
                if amt is not None:
                    parts.append((lineno, amt))
        elif name == "终止经营概况":
            for lineno, raw in body:
                s = raw.strip()
                if not _is_finding_line(s) or _is_exempt_line(s):
                    continue
                if "净利润" not in _own_label(s):
                    continue
                amt = _pl_amount(s)
                if amt is not None and net_profit is None:
                    net_profit = (lineno, amt)
    if net_profit is None or not parts:
        return out                          # 任一侧缺失：整条跳过
    p_sum = sum(a for _ln, a in parts)
    if abs(p_sum - net_profit[1]) > PL_TOL:
        out.append(("TO-PL", net_profit[0], "分项和=%s 披露净利润=%s"
                    % (_fmt(p_sum), _fmt(net_profit[1]))))
    return out


def check_cash(head, sections, stray):
    """道四 TO-CASH：「终止经营现金流量」节 经营＋投资 两项之和 vs 同节合计。

    与 TO-PL 共用同一套本地符号解析（`_pl_amount`：认 `-`／`+`／全角负号），
    投资活动为净流出时符号不会丢。任一侧缺失 ⇒ 整条跳过。
    """
    out = []
    body = None
    for name, _lineno, b in sections:
        if name == "终止经营现金流量":
            body = b
            break
    if body is None:
        return out

    op = inv = total = None
    total_lineno = 1
    for lineno, raw in body:
        s = raw.strip()
        if not _is_finding_line(s) or _is_exempt_line(s):
            continue
        label = _own_label(s)
        amt = _pl_amount(s)
        if amt is None:
            continue
        if TOTAL_MARK in label:
            if total is None:
                total, total_lineno = amt, lineno
            continue
        if CASH_OP_MARK in label and op is None:
            op = amt
        elif CASH_INV_MARK in label and inv is None:
            inv = amt
    if total is None or op is None or inv is None:
        return out                          # 任一侧缺失：整条跳过
    s_sum = op + inv
    if abs(s_sum - total) > CASH_TOL:
        out.append(("TO-CASH", total_lineno, "经营+投资=%s 披露净额=%s"
                    % (_fmt(s_sum), _fmt(total))))
    return out


def check_line(head, sections, stray):
    """道五 TO-LINE：四类红线词＋「终止经营概况」节缺。

    同一行同类只报第一处；`口径与未取到` 与 `来源` 两节整节豁免
    （口径节按设计就要写「不判断处置是否划算」，不豁免会自己咬自己）。

    判**整行（含「」引号内的原句）**：红线是硬闸，一句「本次处置划算」不论写在
    自家结论还是挂着锚的引文里都该被看见一次；漏报比误报贵。
    """
    out = []
    if not any(n == "终止经营概况" for n, _l, _b in sections):
        out.append(("TO-LINE", 1, "缺「终止经营概况」节——这一节是本件存在的理由"))
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
                        out.append(("TO-LINE", lineno, "%s：%s" % (label, w)))
                        break                      # 同一行同类只报第一处
    return out


CHECKS = (
    ("TO-STRUCT", check_struct),
    ("TO-QUOTE", check_quote),
    ("TO-PL", check_pl),
    ("TO-CASH", check_cash),
    ("TO-LINE", check_line),
)


# ---------------------------------------------------------------- 道具

def _section_of(heading):
    """`## 3. 终止经营概况` → `终止经营概况`；认不出返回 None（当 stray）。"""
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
    """→ 行首自有部分去掉〔口径〕括注与列表破折号、截到金额之前，得到标签。"""
    label = _BRACKET.sub("", _own_part(s))
    m = AMOUNT_WAN.search(label)
    if m:
        label = label[:m.start()]
    label = label.strip()
    return label[2:].strip() if label.startswith("- ") else label.lstrip("-").strip()


def _pl_amount(s):
    """TO-PL 专用：行首自有部分里第一个带符号的万元金额；负号保号，没有返回 None。

    只认行首（「」原句之前、去掉〔口径〕括注），免得原句里的数被算进分项和。
    列表破折号 `- ` 必须先剥掉，否则 `- 88,000.00 万元` 会被读成负 88,000。
    """
    own = _BRACKET.sub("", _own_part(s)).strip()
    if own.startswith("- "):
        own = own[2:].strip()
    elif own.startswith("-"):
        own = own[1:].strip()
    m = PL_AMOUNT.search(own)
    if not m:
        return None
    val = _num(m.group("n"))
    return -val if m.group("sign") in ("-", "−") else val


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
    """→ (findings[(code, line, msg)], unjudged[(code, why)])。"""
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


DEMO = r"""# 示例材料（600000.SH）终止经营登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议
主体：示例材料（600000.SH）
报告期：2025 年年度报告·附注·终止经营

## 终止经营概况

- 终止经营业务〔口径：本期末〕处置子公司甲公司的全部股权，已于本年 6 月完成交割「本集团于 2025 年 6 月完成对甲公司全部股权的处置，甲公司不再纳入合并范围」〔锚：2025 年年报·第 251 页·终止经营〕[S1]
- 终止经营净利润〔口径：本期发生额〕34,600.00 万元「终止经营净利润为人民币 34,600.00 万元」〔锚：2025 年年报·第 251 页·终止经营〕[S1]

## 终止经营损益

- 营业收入〔口径：本期发生额〕88,000.00 万元「终止经营营业收入为人民币 88,000.00 万元」〔锚：2025 年年报·第 251 页·终止经营〕[S1]
- 营业成本〔口径：本期发生额〕-61,000.00 万元「终止经营营业成本为人民币 61,000.00 万元」〔锚：2025 年年报·第 251 页·终止经营〕[S1]
- 资产处置损益〔口径：本期发生额〕12,400.00 万元「处置甲公司产生的资产处置损益为人民币 12,400.00 万元」〔锚：2025 年年报·第 251 页·终止经营〕[S1]
- 所得税费用〔口径：本期发生额〕-4,800.00 万元「终止经营所得税费用为人民币 4,800.00 万元」〔锚：2025 年年报·第 251 页·终止经营〕[S1]

## 终止经营现金流量

- 经营活动现金流量净额〔口径：本期发生额〕15,200.00 万元「终止经营经营活动产生的现金流量净额为人民币 15,200.00 万元」〔锚：2025 年年报·第 252 页·终止经营〕[S1]
- 投资活动现金流量净额〔口径：本期发生额〕21,800.00 万元「终止经营投资活动产生的现金流量净额为人民币 21,800.00 万元」〔锚：2025 年年报·第 252 页·终止经营〕[S1]
- 现金流量净额合计〔口径：本期发生额〕37,000.00 万元「终止经营现金及现金等价物净增加额为人民币 37,000.00 万元」〔锚：2025 年年报·第 252 页·终止经营〕[S1]

## 持有待售资产与负债

- 持有待售资产〔口径：本期末账面价值〕9,800.00 万元「划分为持有待售的资产账面价值为人民币 9,800.00 万元」〔锚：2025 年年报·第 252 页·终止经营〕[S1]
- 持有待售负债〔口径：本期末账面价值〕3,600.00 万元「划分为持有待售的负债账面价值为人民币 3,600.00 万元」〔锚：2025 年年报·第 252 页·终止经营〕[S1]

## 处置损益与对价

- 处置对价〔口径：交易对价〕46,000.00 万元「本次股权转让对价为人民币 46,000.00 万元」〔锚：2025 年年报·第 253 页·终止经营〕[S1]
- 处置进度〔口径：本期末〕已完成交割，剩余 10% 尾款待收「截至本报告期末已完成股权交割，剩余 10% 价款尚未收到」〔锚：2025 年年报·第 253 页·终止经营〕[S1]

## 口径与未取到

- 未取到：无
- 口径：终止经营损益、现金流量与持有待售项目一律照抄附注原文并挂原句与锚；本件不判断处置是否划算、不预测处置对以后期间的影响，也不把处置损益当作可持续利润。

## 来源

- [S1] 示例材料 2025 年年度报告·附注·终止经营 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026-03-20
"""


def _swap(text, old, new, why):
    """注入型夹具的唯一入口：替换必须真的落地，否则这一档自己就不成立。"""
    out = text.replace(old, new, 1)
    assert out != text, "注入没落地：%s" % why
    return out


def _reorder(text):
    """把「终止经营现金流量」整段挪到「终止经营损益」之前，造一个真的节序错。"""
    i = text.index("## 终止经营损益")
    j = text.index("## 终止经营现金流量")
    k = text.index("## 持有待售资产与负债")
    out = text[:i] + text[j:k] + text[i:j] + text[k:]
    assert out != text, "注入没落地：节序颠倒"
    return out


def selftest():
    """逐档现报；档数 = 逐档比对的档数 + UNIMPLEMENTED 的码数，**两段都从现场值算**。"""
    _i = DEMO.index("## 终止经营概况")
    _j = DEMO.index("## 终止经营损益")
    bad_section = DEMO[:_i] + DEMO[_j:]
    cases = (
        ("好样应零发条（五道全部落字）", DEMO, frozenset()),
        ("形制：头部删掉「不构成投资建议」",
         DEMO.replace("不构成投资建议", "", 1), frozenset({"TO-STRUCT"})),
        ("形制：节标题写成认不出的样子（进 stray＋缺节）",
         DEMO.replace("## 终止经营损益\n", "## 终止经营损益表\n", 1),
         frozenset({"TO-STRUCT"})),
        ("形制：整节删掉「终止经营概况」（红两道：缺节＋结构判据）",
         bad_section, frozenset({"TO-STRUCT", "TO-LINE"})),
        ("形制：节序颠倒（把现金流量节整段挪到损益节之前）",
         _reorder(DEMO), frozenset({"TO-STRUCT"})),
        ("形制：末尾多出一个同名节「来源」",
         _swap(DEMO, "## 来源\n\n",
               "## 来源\n\n- [S1] 重复登记 | https://example.invalid/x.pdf | 检索日 2026-03-20\n\n## 来源\n\n",
               "同名节"),
         frozenset({"TO-STRUCT"})),
        ("原句与锚：拆掉原句与〔锚〕只留 [S1]",
         _swap(DEMO,
               "34,600.00 万元「终止经营净利润为人民币 34,600.00 万元」"
               "〔锚：2025 年年报·第 251 页·终止经营〕[S1]",
               "34,600.00 万元 [S1]", "锚三元组"), frozenset({"TO-QUOTE"})),
        ("损益：净利润改 40,000.00（分项和 34,600.00 对不上）",
         _swap(DEMO, "34,600.00 万元「终止经营净利润", "40,000.00 万元「终止经营净利润", "净利润"),
         frozenset({"TO-PL"})),
        ("锚：来源行检索日写成斜杠式（不合格式、不算登记）",
         _swap(DEMO, "检索日 2026-03-20", "检索日 2026/03/20", "来源行日期"),
         frozenset({"TO-QUOTE"})),
        ("锚：正文引了未登记的 [S2]",
         _swap(DEMO, "## 处置损益与对价\n\n",
               "## 处置损益与对价\n\n"
               "- 处置税费〔口径：交易对价〕1,200.00 万元「本次股权转让相关税费为人民币 1,200.00 万元」"
               "〔锚：2025 年年报·第 253 页·终止经营〕[S2]\n", "引用未登记来源"),
         frozenset({"TO-QUOTE"})),
        ("现金流量：合计改 40,000.00（经营 15,200＋投资 21,800 对不上）",
         _swap(DEMO, "37,000.00 万元「终止经营现金及现金等价物",
               "40,000.00 万元「终止经营现金及现金等价物", "现金合计"),
         frozenset({"TO-CASH"})),
        ("红线：写上「本次处置划算，预计将增厚业绩」",
         _swap(DEMO, "## 处置损益与对价\n\n",
               "## 处置损益与对价\n\n"
               "- 处置评价〔口径：本期末〕「本次处置划算，预计将增厚业绩」"
               "〔锚：2025 年年报·第 253 页·终止经营〕[S1]\n", "红线处置评价"),
         frozenset({"TO-LINE"})),
        ("现金流量：投资活动改 -21,800.00（净流出，符号须保住；合计对不上）",
         _swap(DEMO, "本期发生额〕21,800.00 万元",
               "本期发生额〕-21,800.00 万元", "投资净流出"),
         frozenset({"TO-CASH"})),
        ("反证：把口径节的「可持续利润」再写一次 → 仍零发条（整节豁免）",
         _swap(DEMO, "也不把处置损益当作可持续利润。",
               "也不把处置损益当作可持续利润，更不当作可持续利润来源。", "口径豁免"),
         frozenset()),
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
    ap = argparse.ArgumentParser(description="终止经营登记稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="终止经营登记稿 .md 路径")
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
        print("缺入参：给一份终止经营登记稿路径，或用 --demo / --selftest", file=sys.stderr)
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
