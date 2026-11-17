#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_forecast.py — 业绩预告／快报稿五道机检（零网络、零外发、不读环境变量）

用法：
    python3 scripts/check_forecast.py <预告稿>.md
    python3 scripts/check_forecast.py --selftest

道一 FC-STRUCT 形制
  头部四件自标（AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]）写在第一个 `## ` 之前；
  `基准日：YYYY-MM-DD` 行在场且值可认；
  `数据口径：` 行在场（内容归道五判）；
  六节齐且按序：一、一句话结论／二、预告要素／三、修正沿革／四、未决事项／五、未取到与口径／六、来源；
  二节六项齐：预告类型／区间下限／区间上限／同比变动幅度／变动原因／披露日，
  预告类型在册（预增／预减／扭亏／首亏／续盈／续亏／略增／略减／不确定）；披露日写成 YYYY-MM-DD；
  区间下限不得大于区间上限（只做大小比对，不产出任何新数）；
  已修正的（正文自称修正过）必须修正前、修正后两值并列，缺一即发；
  未修正的必须明写未修正，含糊（既不写修正也不写未修正）同样发。

道二 FC-QUOTE 原句与锚
  二节每一项都必须挂非空「」原句与 [S#] 锚——空引号 `「」` 与 `「 」` 都发；
  任何小节的事实行要么挂 [S#]，要么挂 [待人工]；
  六节来源每行齐 `[S#]`＋URL＋`检索日 YYYY-MM-DD`。

道三 FC-LINE 红线
  「超预期／不及预期」一类评价、评级与目标价、买卖建议、股价涨跌预测、推断正式财报数、
  改数词（约·大约·大概·左右）一律零命中；含 [待人工] 的分句豁免，且只豁免它自己那一句
  （按 ；;。，,｜ 切分）。

道四 FC-CALC 不得自算
  ① 区间中值不许自己取——「中值／中枢／均值」出现在引号外即发；
  ② 同比与修正幅度只认原句——引号外出现百分比即发；
  ③ 修正幅度不许拿前后相减——引号外出现算式（括号加减除、`/2`、除以、相减、相加）即发；
  ④ 引号外的「同比／环比／增幅／降幅／修正幅度」后面紧跟数字，同样发。
  自算的数是卡面造出来的，它在原文里找不到；不交代出处就等于冒充原句。

道五 FC-BOUND 边界
  `数据口径` 须以「业绩预告」或「业绩快报」起头；
  正文出现「已出财报／财报点评／完整财报」而不点名 cn-earnings-note → 点名；
  正文出现「公告清单／当日全部公告」而不点名 announcement-daily-cn → 点名；
  正文出现「隔夜／盘前全景」一类而不点名 cn-morning-brief → 点名。

退码：0 全过 / 1 有发条 / 3 读不到文件或空稿。
"""

import argparse
import re
import sys
from datetime import date

CODES = ("FC-STRUCT", "FC-QUOTE", "FC-LINE", "FC-CALC", "FC-BOUND")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

CN_NUM = ("一", "二", "三", "四", "五", "六")

SECTIONS = (
    ("一句话结论", r"一句话结论"),
    ("预告要素", r"预告要素|预告六项|要素表"),
    ("修正沿革", r"修正沿革|修正情况|是否修正"),
    ("未决事项", r"未决事项"),
    ("未取到与口径", r"未取到与口径|未取到清单"),
    ("来源", r"来源"),
)

ELEMENTS = ("预告类型", "区间下限", "区间上限", "同比变动幅度", "变动原因", "披露日")

TYPES = ("预增", "预减", "扭亏", "首亏", "续盈", "续亏", "略增", "略减", "不确定")

ANCHOR = re.compile(r"\[(S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
BASE = re.compile(r"^基准日：\s*(\d{4}-\d{2}-\d{2})\s*$")
BASE_LOOSE = re.compile(r"^基准日：")
CALIBER = re.compile(r"^数据口径：\s*(.*)$")
ISODATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ELEM_ROW = re.compile(r"^-\s*(%s)\s*[：:]\s*(.*)$" % "|".join(ELEMENTS))
URL = re.compile(r"https?://\S+")
RETRIEVED = re.compile(r"检索日\s*(\d{4}-\d{2}-\d{2})")
NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")
PCT = re.compile(r"\d[\d,]*(?:\.\d+)?\s*[%％]")

MIDDLE = re.compile(r"中值|中枢|均值|平均值")
ARITH = re.compile(r"[(（][^」」]*[+＋\-—/／*＊][^」」]*[)）]|[/／]\s*2(?!\d)|除以|相减|相加|求和后")
CALC_LABEL = re.compile(r"(?:同比|环比|增幅|降幅|修正幅度|变动幅度|增减幅度)\s*[：:为是]?\s*$")

UPDATED_DONE = re.compile(r"修正过|已修正|系对前次|本次修正|调整后")
UPDATED_NONE = re.compile(r"未修正|未发生修正|首次披露|无修正|未做修正")
UPDATED_PRE = re.compile(r"修正前")
UPDATED_POST = re.compile(r"修正后")

LINE_RULES = (
    ("超预期评价",
     re.compile(r"超(?:出|过)?预期|不及预期|低于预期|好于预期|高于预期|市场预期|胜预期")),
    ("评级与目标价",
     re.compile(r"(?:买入|增持|中性|减持|卖出)评级|目标价|目标位|合理估值|估值区间|强烈推荐|投资评级")),
    ("买卖建议",
     re.compile(r"(?:建议|应当|应该|可以|宜)(?:买入|卖出|减持|增持|加仓|减仓|持有|清仓|抄底|离场)"
                r"|逢高(?:减持|卖出)|逢低(?:买入|吸纳)")),
    ("股价预测",
     re.compile(r"股价(?:将|会|有望|可能|必然)|将(?:上涨|下跌|走高|走低)|有望(?:上涨|走强)"
                r"|翻倍|腰斩|创新高|创新低|涨停|跌停")),
    ("推断正式数",
     re.compile(r"正式(?:财报|年报|中报)(?:将|会|应为|预计)|据此推算|可推断|推算正式|正式数应为")),
    ("改数词",
     re.compile(r"(?:约|大约|大概|接近)\s*[\d０-９]|[\d０-９]\s*(?:倍|成|余)?\s*(?:左右|上下)"
                r"|[\d０-９]\s*左右")),
)

BOUND_NOTE = re.compile(r"cn-earnings-note")
BOUND_DAILY = re.compile(r"announcement-daily-cn")
BOUND_BRIEF = re.compile(r"cn-morning-brief")
WANT_NOTE = re.compile(r"已出财报|财报点评|完整财报|年报点评|季报点评")
WANT_DAILY = re.compile(r"公告清单|当日全部公告|全部公告一览")
WANT_BRIEF = re.compile(r"隔夜全景|盘前全景|晨会")


NEGATION = re.compile(r"[未不无没非]")


def _outside_quotes(line):
    """把一行里所有「…」段摘掉，返回剩下的散文部分。"""
    return QUOTE.sub(" ", line)


def _negated(text, start, window=6):
    """匹配点往前 window 字内有否定词 ⇒ 这一处是在声明「没做」，不是在做。

    「口径：…未取中值，未做前后相减」这类句子是第四节要求的口径声明本身，
    若按命中就发，声明反而成了唯一的红——判据要拦的是「写了中值」，不是「声明没取中值」。
    """
    return bool(NEGATION.search(text[max(0, start - window):start]))


def _parse_doc(text):
    lines = text.splitlines()
    first = len(lines)
    for i, ln in enumerate(lines):
        if ln.startswith("## "):
            first = i
            break
    head = lines[:first]
    heads = []
    body = {}
    cur = None
    for i in range(first, len(lines)):
        ln = lines[i]
        if ln.startswith("## "):
            title = ln[3:].strip()
            cur = None
            for name, pat in SECTIONS:
                if re.search(pat, title):
                    cur = name
                    heads.append((name, i + 1))
                    body.setdefault(name, [])
                    break
            continue
        if cur:
            body[cur].append((i + 1, ln))
    return head, heads, body


def check_text(text):
    """返回 (findings, stats)。findings 为 [(码, 行号, 说明), ...]，行号 0 表示全稿级。"""
    findings = []

    def add(code, lineno, msg):
        findings.append((code, lineno, msg))

    if not text.strip():
        add("FC-STRUCT", 0, "空稿")
        return findings, {}

    head, heads, body = _parse_doc(text)
    names = [n for n, _ in heads]

    # ---------------- 道一 形制 ----------------
    headtext = "\n".join(head)
    for mk in MARK_TEXTS:
        if mk not in headtext:
            add("FC-STRUCT", 1, "头部缺自标「%s」" % mk)

    base = None
    base_seen = False
    for i, ln in enumerate(head):
        s = ln.strip()
        m = BASE.match(s)
        if m:
            base_seen = True
            try:
                base = date.fromisoformat(m.group(1))
            except ValueError:
                add("FC-STRUCT", i + 1, "基准日不是合法日期：%s" % m.group(1))
            break
        if BASE_LOOSE.match(s):
            base_seen = True
            add("FC-STRUCT", i + 1, "基准日行不是 `基准日：YYYY-MM-DD` 形制")
            break
    if not base_seen:
        add("FC-STRUCT", 1, "缺「基准日：YYYY-MM-DD」行")

    if not any(CALIBER.match(ln.strip()) for ln in head):
        add("FC-STRUCT", 1, "缺「数据口径：」行")

    for idx, (name, _pat) in enumerate(SECTIONS):
        if name not in names:
            add("FC-STRUCT", 0, "缺第%s节「%s」" % (CN_NUM[idx], name))

    order = [pos for name, pos in heads if name in dict(SECTIONS)]
    if order != sorted(order):
        add("FC-STRUCT", 0, "六节次序乱了：%s" % " / ".join(n for n, _ in heads))

    elem = {}
    for lineno, ln in body.get("预告要素", []):
        s = ln.strip()
        m = ELEM_ROW.match(s)
        if m:
            elem.setdefault(m.group(1), (lineno, m.group(2), s))
    for name in ELEMENTS:
        if name not in elem:
            add("FC-STRUCT", 0, "二节缺「- %s：「原句」[S#]」一行" % name)

    if "预告类型" in elem:
        lineno, val, s = elem["预告类型"]
        q = QUOTE.findall(val)
        got = (q[0].strip() if q else val).strip()
        if got and got not in TYPES:
            add("FC-STRUCT", lineno, "预告类型不在册：%s（在册：%s）" % (got, "／".join(TYPES)))

    if "披露日" in elem:
        lineno, val, s = elem["披露日"]
        q = QUOTE.findall(val)
        got = (q[0].strip() if q else val).strip()
        if got and not ISODATE.match(got):
            add("FC-STRUCT", lineno, "披露日不是 YYYY-MM-DD：%s" % got)

    lo = hi = None
    for key, setter in (("区间下限", "lo"), ("区间上限", "hi")):
        if key not in elem:
            continue
        lineno, val, s = elem[key]
        nums = NUM.findall(val.replace(",", ""))
        if not nums:
            add("FC-STRUCT", lineno, "%s 行里没有数字：%s" % (key, val[:40]))
            continue
        try:
            v = float(nums[0])
        except ValueError:
            continue
        if setter == "lo":
            lo = v
        else:
            hi = v
    if lo is not None and hi is not None and lo > hi:
        add("FC-STRUCT", elem["区间下限"][0],
            "区间下限 %.2f 大于区间上限 %.2f——上下限写反了" % (lo, hi))

    fix_text = "\n".join(ln for _l, ln in body.get("修正沿革", []))
    done = bool(UPDATED_DONE.search(fix_text))
    none = bool(UPDATED_NONE.search(fix_text))
    if not fix_text.strip():
        add("FC-STRUCT", 0, "三、修正沿革是空节——是否修正过必须明写")
    elif done and none:
        add("FC-STRUCT", body.get("修正沿革", [(0, "")])[0][0] if body.get("修正沿革") else 0,
            "修正沿革自相矛盾：同时写了「修正过」与「未修正」")
    elif not done and not none:
        add("FC-STRUCT", body.get("修正沿革", [(0, "")])[0][0] if body.get("修正沿革") else 0,
            "修正沿革没明写修正过还是未修正（含糊即发）")
    if done:
        if not UPDATED_PRE.search(fix_text):
            add("FC-STRUCT", 0, "自称修正过，但没有「修正前」那一值")
        if not UPDATED_POST.search(fix_text):
            add("FC-STRUCT", 0, "自称修正过，但没有「修正后」那一值")

    if not [1 for _l, ln in body.get("未决事项", []) if ln.strip().startswith("-")]:
        add("FC-STRUCT", 0, "四、未决事项是空节——预告到正式财报之间一定留下未决事项")

    # ---------------- 道二 原句与锚 ----------------
    for name, _pat in SECTIONS:
        for lineno, ln in body.get(name, []):
            s = ln.strip()
            if not s.startswith("-"):
                continue
            if not ANCHOR.search(s) and "[待人工]" not in s:
                add("FC-QUOTE", lineno, "本行既无 [S#] 锚也无 [待人工]，事实无出处")

    for name in ELEMENTS:
        if name not in elem:
            continue
        lineno, val, s = elem[name]
        if not QUOTE.search(val):
            add("FC-QUOTE", lineno, "%s 行没挂「原句」——每一项都要引原文" % name)
            continue
        q = QUOTE.findall(val)[0]
        if not q.strip():
            add("FC-QUOTE", lineno, "%s 行的引号是空的（「」/「 」）" % name)

    src_rows = [(l, ln) for l, ln in body.get("来源", []) if ln.strip().startswith("-")]
    if not src_rows:
        add("FC-QUOTE", 0, "六、来源是空节——一个 [S#] 都没落下，正文的锚无处可核")
    for lineno, ln in body.get("来源", []):
        s = ln.strip()
        if not s.startswith("-"):
            continue
        if not ANCHOR.search(s):
            add("FC-QUOTE", lineno, "来源行缺 [S#] 编号")
        if not URL.search(s):
            add("FC-QUOTE", lineno, "来源行缺公告 URL")
        if not RETRIEVED.search(s):
            add("FC-QUOTE", lineno, "来源行缺「检索日 YYYY-MM-DD」")

    # ---------------- 道三 红线 ----------------
    for i, ln in enumerate(text.splitlines()):
        for label, pat in LINE_RULES:
            for clause in re.split(r"[；;。，,｜|]", ln):
                if "[待人工]" in clause:
                    continue
                m = pat.search(clause)
                if m:
                    add("FC-LINE", i + 1, "%s 命中「%s」" % (label, m.group(0)))

    # ---------------- 道四 不得自算 ----------------
    for name, _pat in SECTIONS:
        if name == "来源":
            continue
        for lineno, ln in body.get(name, []):
            s = ln.strip()
            if not s.startswith("-"):
                continue
            outside = _outside_quotes(s)
            m = MIDDLE.search(outside)
            if m and not _negated(outside, m.start()):
                add("FC-CALC", lineno,
                    "引号外出现「%s」——区间中值不许自己取，披露没写就不许写" % m.group(0))
            m = PCT.search(outside)
            if m:
                add("FC-CALC", lineno,
                    "引号外出现百分比「%s」——同比与修正幅度只认原句" % m.group(0))
            m = ARITH.search(outside)
            if m and not _negated(outside, m.start()):
                add("FC-CALC", lineno,
                    "引号外出现算式「%s」——修正幅度不许自己拿前后相减" % m.group(0))
            m = CALC_LABEL.search(outside)
            if m and NUM.search(outside[outside.index(m.group(0)) + len(m.group(0)):] or ""):
                add("FC-CALC", lineno,
                    "引号外「%s」后面直接跟数字——幅度数字必须来自原句" % m.group(0))

    # ---------------- 道五 边界 ----------------
    caliber = None
    for i, ln in enumerate(head):
        m = CALIBER.match(ln.strip())
        if m:
            caliber = (i + 1, m.group(1).strip())
            break
    if caliber:
        lineno, val = caliber
        if not (val.startswith("业绩预告") or val.startswith("业绩快报")):
            add("FC-BOUND", lineno,
                "数据口径未以「业绩预告」或「业绩快报」起头——本件只登记预告与快报本身")

    bodytext = "\n".join(ln for name, _p in SECTIONS if name != "来源"
                         for _l, ln in body.get(name, []))
    if WANT_NOTE.search(bodytext) and not BOUND_NOTE.search(text):
        add("FC-BOUND", 0,
            "正文写了已出财报／财报点评，但没点名 cn-earnings-note——完整财报点评走那一件")
    if WANT_DAILY.search(bodytext) and not BOUND_DAILY.search(text):
        add("FC-BOUND", 0,
            "正文写了公告清单，但没点名 announcement-daily-cn——当日全部公告清单走那一件")
    if WANT_BRIEF.search(bodytext) and not BOUND_BRIEF.search(text):
        add("FC-BOUND", 0,
            "正文写了晨会／隔夜全景，但没点名 cn-morning-brief——一篮子标的的隔夜全景走那一件")

    counts = {}
    for code, _l, _m in findings:
        counts[code] = counts.get(code, 0) + 1
    stats = {
        "lines": len(text.splitlines()),
        "sections": len([n for n in names if n in dict(SECTIONS)]),
        "elements": len(elem),
        "counts": counts,
    }
    return findings, stats


def report(path, findings, stats):
    for code, lineno, msg in findings:
        where = "全稿" if not lineno else "L%d" % lineno
        print("%s %s  %s" % (code, where, msg))
    print("——")
    print("道一 形制 FC-STRUCT 发条 %d" % stats.get("counts", {}).get("FC-STRUCT", 0))
    print("道二 原句 FC-QUOTE  发条 %d" % stats.get("counts", {}).get("FC-QUOTE", 0))
    print("道三 红线 FC-LINE   发条 %d" % stats.get("counts", {}).get("FC-LINE", 0))
    print("道四 自算 FC-CALC   发条 %d" % stats.get("counts", {}).get("FC-CALC", 0))
    print("道五 边界 FC-BOUND  发条 %d" % stats.get("counts", {}).get("FC-BOUND", 0))
    print("稿=%s 行=%d 节=%d 六项=%d ｜ 发条合计=%d"
          % (path, stats.get("lines", 0), stats.get("sections", 0),
             stats.get("elements", 0), len(findings)))


GOOD = """AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]

基准日：2026-11-09
数据口径：业绩预告（单份预告文件逐项登记，不评已出财报，不推断正式数）

## 一、一句话结论

示例科技于披露日「2026-11-09」发布 2026 年年度业绩预告，预告类型为「预增」，归属于上市公司股东的净利润「预计 32,000 万元至 38,000 万元」[S1]。

## 二、预告要素

- 预告类型：「预增」[S1]
- 区间下限：「32,000 万元」[S1]
- 区间上限：「38,000 万元」[S1]
- 同比变动幅度：「比上年同期增长 45.12% 至 72.35%」[S1]
- 变动原因：「主要产品销量增长及毛利率提升」[S1]
- 披露日：「2026-11-09」[S1]

## 三、修正沿革

- 修正情况：「本次业绩预告为首次披露，未发生修正」[S1]

## 四、未决事项

- 正式年度报告尚未披露，最终数据以经审计年报为准 [待人工]

## 五、未取到与口径

- 未取到 分季度拆分：预告文件只给全年区间，未披露季度分布 [S1]
- 口径：区间与同比幅度均直接引原文，未取中值，未做前后相减 [S1]

## 六、来源

- [S1] 示例科技 2026 年年度业绩预告 https://example.com/ann/S1 检索日 2026-11-09
"""

# 各坏样只发它自己那道码
BAD_STRUCT = GOOD.replace(
    "- 变动原因：「主要产品销量增长及毛利率提升」[S1]\n", "")
BAD_QUOTE = GOOD.replace(
    "- 变动原因：「主要产品销量增长及毛利率提升」[S1]",
    "- 变动原因：「」[S1]")
BAD_REDLINE = GOOD.replace(
    "- 正式年度报告尚未披露，最终数据以经审计年报为准 [待人工]",
    "- 正式年度报告尚未披露 [待人工]，本次预告超预期，股价将上涨，建议增持 [S1]")
BAD_CALC = GOOD.replace(
    "- 同比变动幅度：「比上年同期增长 45.12% 至 72.35%」[S1]",
    "- 同比变动幅度：「比上年同期增长 45.12% 至 72.35%」，中值 35,000 万元，同比增幅 58.74% [S1]")
BAD_BOUND = GOOD.replace(
    "数据口径：业绩预告（单份预告文件逐项登记，不评已出财报，不推断正式数）",
    "数据口径：已出财报的点评（收入与利润率怎么变、为什么变）")

# 反证样：不该发的必须不发
OK_FIXED = GOOD.replace(
    "- 修正情况：「本次业绩预告为首次披露，未发生修正」[S1]",
    "- 修正前：「预计 20,000 万元至 24,000 万元」[S1]\n"
    "- 修正后：「预计 32,000 万元至 38,000 万元」[S1]\n"
    "- 修正说明：「本次业绩预告系对前次预告的更正」[S1]")
BAD_FIXED_HALF = GOOD.replace(
    "- 修正情况：「本次业绩预告为首次披露，未发生修正」[S1]",
    "- 修正后：「预计 32,000 万元至 38,000 万元」[S1]\n"
    "- 修正说明：「本次业绩预告系对前次预告的更正」[S1]")
OK_HEDGE_EXEMPT = GOOD.replace(
    "- 正式年度报告尚未披露，最终数据以经审计年报为准 [待人工]",
    "- 正式年度报告尚未披露，最终数据以经审计年报为准 [待人工]\n"
    "- 是否超预期交由人工判断 [待人工]")
BAD_HEDGE_HALF = GOOD.replace(
    "- 正式年度报告尚未披露，最终数据以经审计年报为准 [待人工]",
    "- 正式年度报告尚未披露 [待人工]，本次预告超预期 [S1]")
BAD_MID = GOOD.replace(
    "- 修正情况：「本次业绩预告为首次披露，未发生修正」[S1]",
    "- 修正情况：「本次业绩预告为首次披露，未发生修正」[S1]\n"
    "- 区间中值：35,000 万元 [S1]")


def _codes(text):
    findings, _stats = check_text(text)
    return findings, set(c for c, _l, _m in findings)


def selftest():
    cases = (
        ("好样应零发条", GOOD, set()),
        ("形制：二节缺变动原因一项", BAD_STRUCT, {"FC-STRUCT"}),
        ("原句：引号是空的", BAD_QUOTE, {"FC-QUOTE"}),
        ("红线：超预期＋股价将涨＋建议增持", BAD_REDLINE, {"FC-LINE"}),
        ("自算：中值与同比增幅写在引号外", BAD_CALC, {"FC-CALC"}),
        ("边界：数据口径写成已出财报点评", BAD_BOUND, {"FC-BOUND"}),
        ("反证：修正过且前后两值并列 → 不发", OK_FIXED, set()),
        ("形制：自称修正过但缺修正前", BAD_FIXED_HALF, {"FC-STRUCT"}),
        ("反证：[待人工] 独立成立 → 不发", OK_HEDGE_EXEMPT, set()),
        ("反证：[待人工] 只豁免自己那句", BAD_HEDGE_HALF, {"FC-LINE"}),
        ("自算：中值单列一行也发", BAD_MID, {"FC-CALC"}),
    )
    bad = 0
    for label, text, want in cases:
        findings, got = _codes(text)
        ok = got == want
        if not ok:
            bad += 1
            detail = "；".join("%s L%d %s" % (c, l, m) for c, l, m in findings[:4])
            print("不合 %s：期望 %s 实得 %s ｜ %s"
                  % (label, sorted(want) or "无", sorted(got) or "无", detail))
        else:
            print("过   %s（发条 %d 道：%s）" % (label, len(findings),
                                                "、".join(sorted(got)) or "无"))
    print("——")
    print("自测档数=%d｜不合=%d｜不可判=0" % (len(cases), bad))
    return 0 if bad == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="业绩预告／快报稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="预告稿 .md 路径")
    ap.add_argument("--selftest", action="store_true", help="跑包内夹具自检")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.path:
        ap.print_help()
        return 3
    try:
        with open(args.path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except (IOError, OSError) as exc:
        print("读不到文件：%s（%s）" % (args.path, exc))
        return 3
    if not text.strip():
        print("空稿：%s" % args.path)
        return 3

    findings, stats = check_text(text)
    report(args.path, findings, stats)
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
