#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""股份支付登记稿五道机检（五道全部落字）。

本件读的是年报附注「股份支付」那一段：两类计量（权益结算／现金结算）、
等待期内费用摊销、以及可行权数量的变动。

五道判据：
  SP-STRUCT 形制：头部三件自标、七节齐且按序、野节逐条发。
  SP-QUOTE  溯源：带数字的行须挂齐「原句＋〔锚〕＋[S#]」；正文与来源节两向对上。
  SP-SUM    加总：两类本期费用之和 ＝ 两处披露合计；两处合计互不相等本身即发条。
  SP-VEST   恒等：期初 ＋ 新增 − 行权 ＝ 期末（万股）。
  SP-LINE   红线：四组越界词（投资建议／前瞻预测／主观评价／越界口径）。

退出码：0=五道都判过且零发条；1=有发条；3=读不了／空稿／仍有判据未落字。
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

SLUG = "cue-cn-share-based-payment-cn"

CODES = ("SP-STRUCT", "SP-QUOTE", "SP-SUM", "SP-VEST", "SP-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议")

SECTIONS = ("股份支付概况", "权益结算的股份支付", "现金结算的股份支付",
            "等待期费用摊销", "数量变动", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"

# 五道全部落字，清单为空。某道若回退成空壳，就登记回这里：它会调用即抛、
# 被 check_text 收进「不可判」，单稿退 3——既不判也不放行，rc=0 只留给「五道全过」。
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


def _not_judged(code, why):
    """空壳的唯一出口：抛未落字，由 check_text 捕获计入「不可判」，**不返回空表**。"""
    raise NotImplementedError("%s 未落字：%s" % (code, why))


def check_struct(head, sections, stray):
    """道一 SP-STRUCT 形制：头部三件自标、七节齐且按序、野节逐条发。只判形。"""
    out = []
    htext = "\n".join(s for _i, s in head)
    for mark in MARK_TEXTS:
        if mark not in htext:
            out.append(("SP-STRUCT", 1, "头部缺自标「%s」" % mark))
    for lineno, raw in stray:
        out.append(("SP-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw))
    names = [n for n, _l, _b in sections]
    missing = [n for n in SECTIONS if n not in names]
    if missing:
        out.append(("SP-STRUCT", 1, "缺节：%s" % "／".join(missing)))
    elif names != list(SECTIONS):
        out.append(("SP-STRUCT", 1, "节序不对：现序 %s，应序 %s"
                    % ("／".join(names), "／".join(SECTIONS))))
    return out


def check_quote(head, sections, stray):
    """道二 SP-QUOTE：数字行须挂齐「」原句＋〔锚〕＋[S#]；来源与正文两向对上。"""
    out = []
    for name, _l, body in sections:
        if name in (GAP_SECTION, SOURCE_SECTION):
            continue
        for l, row in body:
            if not row.startswith("- ") or _is_exempt_line(row):
                continue
            own = _BRACKET.sub("", _own_part(row))
            if not re.search(r"[0-9]", own):
                continue
            if not TRIPLE.search(row):
                out.append(("SP-QUOTE", l, "带数字的行没挂齐「原句＋锚＋[S#]」"))
    cited = set()
    for name, _l, body in sections:
        if name in (GAP_SECTION, SOURCE_SECTION):
            continue
        for _l2, row in body:
            cited |= set(CITE.findall(row))
    declared = {}
    for name, _l, body in sections:
        if name != SOURCE_SECTION:
            continue
        for l, row in body:
            m = SOURCE_LINE.match(row.strip())
            if m:
                declared.setdefault(m.group("s"), l)
    for s in sorted(cited - set(declared)):
        out.append(("SP-QUOTE", 1, "正文引用了来源里没有的 [%s]" % s))
    for s, l in sorted(declared.items(), key=lambda kv: kv[1]):
        if s not in cited:
            out.append(("SP-QUOTE", l, "来源登记了 [%s] 但正文未引用" % s))
    return out


def check_sum(head, sections, stray):
    """道三 SP-SUM：本期费用 权益结算＋现金结算 vs 披露的合计。"""
    out = []
    a = _pick(sections, "权益结算的股份支付", "本期确认的费用")
    b = _pick(sections, "现金结算的股份支付", "本期确认的费用")
    t_gen = _pick(sections, "股份支付概况", "总额") or _pick(sections, "股份支付概况", "合计")
    t_cash = _pick(sections, "现金结算的股份支付", "合计")
    totals = t_gen + [r for r in t_cash if r not in t_gen]
    if not (a and b and totals):
        if _gap_declared(sections):
            return out
        miss = [nm for nm, g in (("权益结算本期确认的费用", a),
                                 ("现金结算本期确认的费用", b),
                                 ("披露合计", totals)) if not g]
        return [("SP-SUM", 1, "缺数：%s" % "／".join(miss))]
    hit = _one("SP-SUM", out, (a, b), ("权益结算费用", "现金结算费用"))
    if hit is not None:
        return hit
    x, y = a[0][1], b[0][1]
    if len(totals) > 1 and abs(totals[0][1] - totals[1][1]) > 0.01:
        out.append(("SP-SUM", totals[1][0],
                    "两处披露合计互不相等：概况 %.2f vs 现金结算节 %.2f"
                    % (totals[0][1], totals[1][1])))
    for l, z, label in totals:
        if abs(x + y - z) > 0.01:
            out.append(("SP-SUM", l,
                        "两类之和 %.2f ≠ 「%s」%.2f（差 %.2f）" % (x + y, label, z, x + y - z)))
    return out




def check_vest(head, sections, stray):
    """道四 SP-VEST：数量变动恒等式 期初+本期可行权−本期行权=期末。"""
    out = []
    allr = [(l, _own_qty(s), _own_label(s))
            for l, s in _body(sections, "数量变动") if s.startswith("- ")]
    allr = [r for r in allr if r[1] is not None]
    b = [r for r in allr if "期初" in r[2]]
    n = [r for r in allr if "新增" in r[2]]
    e = [r for r in allr if "行权" in r[2] and "可行权" not in r[2]]
    c = [r for r in allr if "期末" in r[2]]
    if not (b and n and e and c):
        if _gap_declared(sections):
            return out
        miss = [nm for nm, g in (("期初", b), ("新增", n), ("行权", e), ("期末", c)) if not g]
        return [("SP-VEST", 1, "缺数：%s" % "／".join(miss))]
    hit = _one("SP-VEST", out, (b, n, e, c), ("期初", "新增", "行权", "期末"))
    if hit is not None:
        return hit
    B, N, E, C = b[0][1], n[0][1], e[0][1], c[0][1]
    if abs((B + N - E) - C) > 0.01:
        return [("SP-VEST", c[0][0],
                 "四数恒等不成立：%.2f ＋ %.2f − %.2f ＝ %.2f，稿写 %.2f"
                 % (B, N, E, B + N - E, C))]
    return out




def check_line(head, sections, stray):
    """道五 SP-LINE：四组红线词，只在内容节扫。"""
    out = []
    for name, _l, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        for l, row in body:
            if _is_exempt_line(row):
                continue
            for gname, words in REDLINES:
                hit = [w for w in words if w in row]
                if not hit:
                    continue
                # 子串会叠：「不合理」里含「合理」，「显著低估」里含「低估」。
                # 同一行同一组只报最长的那个，避免一句话被记成两三条。
                keep = [w for w in hit if not any(w != o and w in o for o in hit)]
                for w in keep:
                    out.append(("SP-LINE", l, "红线词：%s（%s）" % (w, gname)))
    return out


REDLINES = (
    ("投资建议", ("买入", "卖出", "增持", "减持", "目标价", "推荐", "建议持有")),
    ("前瞻预测", ("预计", "预测", "有望", "将会", "看好", "预期增长")),
    ("主观评价", ("合理", "不合理", "偏高", "偏低", "显著低估", "高估")),
    ("越界口径", ("经常性损益", "扣非", "估值", "市盈率", "市值")),
)


CHECKS = (
    ("SP-STRUCT", check_struct),
    ("SP-QUOTE", check_quote),
    ("SP-SUM", check_sum),
    ("SP-VEST", check_vest),
    ("SP-LINE", check_line),
)


# ---------------------------------------------------------------- 道具

def _section_of(heading):
    """`## 3. 股份支付概况` → `股份支付概况`；认不出返回 None（当 stray）。"""
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


def _section_lines(sections, names):
    want = tuple(names)
    return [(n, l, b) for n, l, b in sections if n in want]


def _num(s):
    """`48,000.00` → 48000.0；去千分位逗号。"""
    return float(s.replace(",", ""))


def _fmt(x):
    """金额统一留两位小数。"""
    return "%.2f" % x


QTY_WAN_GU = re.compile(r"([0-9][0-9,]*(?:\.[0-9]+)?)\s*万股")


def _own_qty(s):
    """→ 行首自有部分（「」之前、去掉〔口径〕括注）里第一个「万股」的数量；没有返回 None。"""
    own = _BRACKET.sub("", _own_part(s))
    m = QTY_WAN_GU.search(own)
    return _num(m.group(1)) if m else None


def _body(sections, name):
    for n, _l, b in sections:
        if n == name:
            return b
    return []


def _gap_declared(sections):
    """→ 「口径与未取到」节里「未取到：」后面写了真东西（不是「无」）时为 True。"""
    for _l, s in _body(sections, GAP_SECTION):
        if "未取到" in s:
            tail = s.split("未取到", 1)[1].lstrip("：: ").strip()
            if tail and tail not in ("无", "無", "None", "none", "—", "-", "–"):
                return True
    return False


def _pick(sections, name, kw, amt=None):
    """→ [(行号, 数值, 标签)]；kw 是标签子串，amt 缺省取万元。"""
    out = []
    for l, s in _body(sections, name):
        if not s.startswith("- "):
            continue
        label = _own_label(s)
        if kw not in label:
            continue
        v = (amt or _own_amount)(s)
        if v is None:
            continue
        out.append((l, v, label))
    return out


def _one(code, out, groups, names):
    """四组数任一不唯一即发条；返回 None 表示可以继续比。"""
    for g, nm in zip(groups, names):
        if len(g) > 1:
            out.append((code, g[1][0], "多义：%s 匹配到 %d 行，不敢比" % (nm, len(g))))
            return out
    return None


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


DEMO = r"""# 示例材料（600000.SH）股份支付登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议
主体：示例材料（600000.SH）
报告期：2025 年年度报告·附注·股份支付

## 股份支付概况

- 股份支付类型〔口径：本期〕权益结算的股份支付与现金结算的股份支付并行「本公司股份支付包括以权益结算的股份支付和以现金结算的股份支付」〔锚：2025 年年报·第 268 页·股份支付〕[S1]
- 本期确认的费用总额〔口径：本期发生额〕18,400.00 万元「本期因股份支付确认的费用总额为人民币 18,400.00 万元」〔锚：2025 年年报·第 268 页·股份支付〕[S1]

## 权益结算的股份支付

- 授予日权益工具公允价值的确定方法〔口径：本期〕按授予日收盘价扣除行权价确定「限制性股票的公允价值按授予日股票收盘价扣除授予价格确定」〔锚：2025 年年报·第 268 页·股份支付〕[S1]
- 本期确认的费用〔口径：本期发生额〕15,600.00 万元「以权益结算的股份支付本期确认费用人民币 15,600.00 万元」〔锚：2025 年年报·第 268 页·股份支付〕[S1]
- 累计确认的费用〔口径：截至本期末〕32,800.00 万元「截至本报告期末累计确认费用人民币 32,800.00 万元」〔锚：2025 年年报·第 268 页·股份支付〕[S1]

## 现金结算的股份支付

- 负债的期末账面价值〔口径：本期末〕2,800.00 万元「以现金结算的股份支付形成的负债期末账面价值为人民币 2,800.00 万元」〔锚：2025 年年报·第 269 页·股份支付〕[S1]
- 本期确认的费用〔口径：本期发生额〕2,800.00 万元「以现金结算的股份支付本期确认费用人民币 2,800.00 万元」〔锚：2025 年年报·第 269 页·股份支付〕[S1]
- 本期费用合计〔口径：本期发生额〕18,400.00 万元「两类股份支付本期确认费用合计人民币 18,400.00 万元」〔锚：2025 年年报·第 269 页·股份支付〕[S1]

## 等待期费用摊销

- 本期摊销额〔口径：本期发生额〕15,600.00 万元「本期摊销计入相关成本费用人民币 15,600.00 万元」〔锚：2025 年年报·第 269 页·股份支付〕[S1]
- 剩余等待期将确认的费用〔口径：本期末〕21,600.00 万元「剩余等待期内拟确认的费用为人民币 21,600.00 万元」〔锚：2025 年年报·第 269 页·股份支付〕[S1]

## 数量变动

- 期初可行权数量〔口径：本期末（股）〕1,200.00 万股「期初尚未行权的限制性股票为 1,200.00 万股」〔锚：2025 年年报·第 270 页·股份支付〕[S1]
- 本期新增可行权数量〔口径：本期（股）〕400.00 万股「本期新增可解除限售的限制性股票 400.00 万股」〔锚：2025 年年报·第 270 页·股份支付〕[S1]
- 本期行权数量〔口径：本期（股）〕300.00 万股「本期实际解除限售 300.00 万股」〔锚：2025 年年报·第 270 页·股份支付〕[S1]
- 期末可行权数量〔口径：本期末（股）〕1,300.00 万股「期末尚未解除限售的限制性股票为 1,300.00 万股」〔锚：2025 年年报·第 270 页·股份支付〕[S1]

## 口径与未取到

- 未取到：无
- 口径：股份支付的类型、授予日公允价值方法、各期费用与数量变动一律照抄附注原文并挂原句与锚；本件不判断激励方案是否合理、不预测对以后期间业绩的影响，也不把股份支付费用当作可比的经常性损益。

## 来源

- [S1] 示例材料 2025 年年度报告·附注·股份支付 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026-03-20
"""


def _swap(text, old, new, why):
    """注入型夹具的唯一入口：替换必须真的落地，否则这一档自己就不成立。"""
    out = text.replace(old, new, 1)
    assert out != text, "注入没落地：%s" % why
    return out


def _reorder(text):
    """把「现金结算的股份支付」整段挪到「权益结算的股份支付」之前，造一个真的节序错。"""
    i = text.index("## 权益结算的股份支付")
    j = text.index("## 现金结算的股份支付")
    k = text.index("## 等待期费用摊销")
    out = text[:i] + text[j:k] + text[i:j] + text[k:]
    assert out != text, "注入没落地：节序颠倒"
    return out



CASH_FEE_LINE = ("- 本期确认的费用〔口径：本期发生额〕2,800.00 万元"
                 "「以现金结算的股份支付本期确认费用人民币 2,800.00 万元」"
                 "〔锚：2025 年年报·第 269 页·股份支付〕[S1]")


def selftest():
    """逐档现报；档数 = 逐档比对的档数 + UNIMPLEMENTED 的码数，**两段都从现场值算**。"""
    _i = DEMO.index("## 股份支付概况")
    _j = DEMO.index("## 权益结算的股份支付")
    bad_section = DEMO[:_i] + DEMO[_j:]
    cases = (
        ("好样应零发条（五道全落字，好样一个闹钟都不该响）", DEMO, frozenset()),
        ("形制：头部删掉「不构成投资建议」",
         DEMO.replace("不构成投资建议", "", 1), frozenset({"SP-STRUCT"})),
        ("形制：节标题写成认不出的样子（进 stray＋缺节）",
         DEMO.replace("## 权益结算的股份支付\n", "## 权益结算的股份支付明细\n", 1),
         frozenset({"SP-STRUCT", "SP-SUM"})),
        ("形制：整节删掉「股份支付概况」",
         bad_section, frozenset({"SP-STRUCT"})),
        ("形制：节序颠倒（把现金结算节整段挪到权益结算节之前）",
         _reorder(DEMO), frozenset({"SP-STRUCT"})),
        ("形制：末尾多出一个同名节「来源」",
         _swap(DEMO, "## 来源\n\n",
               "## 来源\n\n- [S1] 重复登记 | https://example.invalid/x.pdf | 检索日 2026-03-20\n\n## 来源\n\n",
               "同名节"),
         frozenset({"SP-STRUCT"})),
        ("合计：把「股份支付概况」的费用总额改大 1000（两类之和不再等于披露合计）",
         _swap(DEMO, "本期确认的费用总额〔口径：本期发生额〕18,400.00",
               "本期确认的费用总额〔口径：本期发生额〕19,400.00", "合计改大"),
         frozenset({"SP-SUM"})),
        ("合计：把现金结算节的「本期费用合计」改小 1000", 
         _swap(DEMO, "本期费用合计〔口径：本期发生额〕18,400.00",
               "本期费用合计〔口径：本期发生额〕17,400.00", "合计改小"),
         frozenset({"SP-SUM"})),
        ("缺数：现金结算的「本期确认的费用」那一行整行删掉，且未声明未取到",
         _swap(DEMO, CASH_FEE_LINE + "\n", "", "现金费用行"),
         frozenset({"SP-SUM"})),
        ("数量：期末可行权 1,300 改成 1,400（四数恒等不再成立）",
         _swap(DEMO, "1,300.00 万股", "1,400.00 万股", "期末数量"),
         frozenset({"SP-VEST"})),
        ("数量：期初可行权 1,200 改成 1,100（四数恒等不再成立）",
         _swap(DEMO, "1,200.00 万股", "1,100.00 万股", "期初数量"),
         frozenset({"SP-VEST"})),
        ("跳过：删掉现金费用行但「口径与未取到」写明未取到 ⇒ SP-SUM 不发条",
         _swap(_swap(DEMO, CASH_FEE_LINE + "\n", "", "现金费用行"),
               "- 未取到：无", "- 未取到：现金结算的股份支付本期费用附注未单列", "未取到声明"),
         frozenset()),
        ("缺数：整节删掉「数量变动」且未声明未取到 ⇒ SP-VEST 报缺数（同时 SP-STRUCT 报缺节）",
         DEMO.replace(DEMO[DEMO.index("## 数量变动"):DEMO.index("## 口径与未取到")], "", 1),
         frozenset({"SP-STRUCT", "SP-VEST"})),
        ("溯源：把「权益结算本期确认的费用」那行的〔锚〕删掉 ⇒ 三重标记不齐",
         _swap(DEMO,
               "15,600.00 万元「以权益结算的股份支付本期确认费用人民币 15,600.00 万元」"
               "〔锚：2025 年年报·第 268 页·股份支付〕[S1]",
               "15,600.00 万元「以权益结算的股份支付本期确认费用人民币 15,600.00 万元」[S1]",
               "删锚"),
         frozenset({"SP-QUOTE"})),
        ("溯源：把某行的 [S1] 改成 [S9]（正文引用来源里没有的号）",
         _swap(DEMO, "〔锚：2025 年年报·第 270 页·股份支付〕[S1]",
               "〔锚：2025 年年报·第 270 页·股份支付〕[S9]", "改引用号"),
         frozenset({"SP-QUOTE"})),
        ("溯源：来源节多登记一条 [S2] 但正文从不引用",
         _swap(DEMO, "## 来源\n\n",
               "## 来源\n\n- [S2] 未被引用的来源 | https://example.invalid/y.pdf | 检索日 2026-03-20\n",
               "多登记来源"),
         frozenset({"SP-QUOTE"})),
        ("红线：内容节里插一行含「预计」（三重标记齐全，不惊动 SP-QUOTE）",
         _swap(DEMO, "- 本期摊销额",
               "- 预计下期摊销额〔口径：本期发生额〕15,600.00 万元"
               "「本期摊销计入相关成本费用人民币 15,600.00 万元」"
               "〔锚：2025 年年报·第 269 页·股份支付〕[S1]",
               "插预计行"),
         frozenset({"SP-LINE"})),
        ("红线：内容节里插一行含「目标价」",
         _swap(DEMO, "- 本期摊销额",
               "- 目标价〔口径：本期〕15,600.00 万元"
               "「本期摊销计入相关成本费用人民币 15,600.00 万元」"
               "〔锚：2025 年年报·第 269 页·股份支付〕[S1]",
               "插目标价行"),
         frozenset({"SP-LINE"})),
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
    ap = argparse.ArgumentParser(description="股份支付登记稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="股份支付登记稿 .md 路径")
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
        print("缺入参：给一份股份支付登记稿路径，或用 --demo / --selftest", file=sys.stderr)
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
