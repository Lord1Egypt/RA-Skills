#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_lockup.py — 限售解禁压力稿五道机检（零网络、零外发、不读环境变量）

用法：
    python3 scripts/check_lockup.py <解禁稿>.md
    python3 scripts/check_lockup.py --selftest

道一 LK-STRUCT 形制
  头部四件自标（AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]）写在第一个 `## ` 之前；
  `基准日：YYYY-MM-DD` 行在场且值可认；
  `跟踪口径：` 行在场（内容归道五判）；
  七节齐且按序：一、一句话结论／二、解禁总览／三、解禁日历／四、压力测算／五、未决事项／
  六、未取到与口径／七、来源；
  二节必须有 `- 总股本：N 股 [S#]` 一行——它是四节所有占比的分母；
  三节每行 `- YYYY-MM-DD｜解禁方类型｜一句话事实 [S#]`，类型在册，日期非降序，且每行晚于基准日；
  四节每行 `- 第 N 轮 YYYY-MM-DD｜解禁 N 股／占总股本 X.XX%（分母总股本 N 股）｜占比出处：… [S#][S#]`。

道二 LK-QUOTE 原句与锚
  事实行不得空锚：每一行要么挂 [S#]，要么挂 [待人工]；
  七节来源每行 `- [S#] 标题 URL 检索日 YYYY-MM-DD`，锚、URL、检索日缺一不可；
  正文引用的每一个 [S#] 都必须在来源节有对应登记行（该行须带可点 http(s) URL 与检索日）——
  引用了根本不存在的 S 号即发：那等于凭空造出处，比挂错来源更重；
  四节每行至少两枚**不同号**锚——分子（解禁股数）与分母（总股本）各来自一处；
  二节总股本行必须自己挂锚——分母单独挂源，不许从分子那枚锚借光。

道三 LK-LINE 红线
  股价预测／涨跌承诺／买卖与减持建议／评级与目标价／解禁压力档位评价／改数词（约·大约·大概·左右）
  一律零命中；含 [待人工] 的分句豁免，且只豁免它自己那一句（按 ；;。，,｜ 切分）。

道四 LK-GAP 未取到两向点名 + 占比不得自算
  正文（一至五节）写「未取到 X」⇒ 六节必须点名 X；六节点名了 X 而正文没有 ⇒ 同样发；两向都判。
  四节每行必须自报「占比出处」：`公告原文` 或 `自算`；
  报 `自算` 的，六节必须有一条 `口径：` 行写明是自算／折算／除以——公告只写解禁股数没写占比时，
  卡面自己拿股数除总股本得出的那个百分比，在原句里找不到，不交代口径就是冒充原句。
  四节的分母总股本必须与本稿二节总股本行同一个数——不同时点的总股本不一样，分母拿错了，
  这一整节的占比全错。

道五 LK-BOUND 边界
  跟踪口径须以「解禁」起头；写成已发生／减持／分红／回购／股东回报 → 点名改走 cn-shareholder-return；
  写成质押／解押 → 点名改走 cn-share-pledge-tracker；
  日历不足两行 → 点名改走 cn-shareholder-return（本件排未来时间表，不是已发生行为清单）；
  日历行里出现分红／回购／减持／质押／解押／股东回报 → 按上述点名。

退码：0 全过 / 1 有发条 / 3 读不到文件或空稿。
"""

import argparse
import re
import sys
from datetime import date

CODES = ("LK-STRUCT", "LK-QUOTE", "LK-LINE", "LK-GAP", "LK-BOUND")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

CN_NUM = ("一", "二", "三", "四", "五", "六", "七")

SECTIONS = (
    ("一句话结论", r"一句话结论"),
    ("解禁总览", r"解禁总览"),
    ("解禁日历", r"解禁日历"),
    ("压力测算", r"压力测算"),
    ("未决事项", r"未决事项"),
    ("未取到与口径", r"未取到与口径"),
    ("来源", r"来源"),
)

TYPES = ("控股股东", "实际控制人", "董监高", "定增对象", "股权激励对象",
         "首发原股东", "战略投资者", "其他")

ANCHOR = re.compile(r"\[(S\d+)\]")
SOURCE_ID = re.compile(r"^-\s*\[(S\d+)\]")
BASE = re.compile(r"^基准日：\s*(\d{4}-\d{2}-\d{2})\s*$")
BASE_LOOSE = re.compile(r"^基准日：")
TRACK = re.compile(r"^跟踪口径：\s*(.*)$")
ISODATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TOTAL_ROW = re.compile(r"^-\s*总股本：\s*([\d,]+(?:\.\d+)?)\s*(亿|万)?股")
PRESSURE_SHAPE = re.compile(
    r"^-\s*第\s*\d+\s*轮\s*\d{4}-\d{2}-\d{2}"
    r"\s*｜\s*解禁\s*[\d,]+(?:\.\d+)?\s*(?:亿|万)?股"
    r"\s*／\s*占总股本\s*\d+(?:\.\d+)?\s*[%％]"
    r"\s*（\s*分母总股本\s*[\d,]+(?:\.\d+)?\s*(?:亿|万)?股\s*）"
)
DENOM = re.compile(r"（\s*分母总股本\s*([\d,]+(?:\.\d+)?)\s*(亿|万)?股\s*）")
PCT_SRC = re.compile(r"占比出处[：:]\s*([^\[\s｜|]+)")
URL = re.compile(r"https?://\S+")
RETRIEVED = re.compile(r"检索日\s*(\d{4}-\d{2}-\d{2})")

MISS_BODY = re.compile(r"未取到\s*([^\s：:，,。；;｜\[（(]{2,40})")
MISS_SIX = re.compile(r"^-\s*未取到\s*([^：:]{2,40})[：:]")
KOUJING = re.compile(r"口径[：:]")
SELF_CALC_WORDS = re.compile(r"自算|折算|除以|相除|以股数计算")

LINE_RULES = (
    ("股价预测",
     re.compile(r"股价(?:将|会|有望|可能|必然)|将(?:上涨|下跌|走高|走低)|有望(?:上涨|走强)"
                r"|翻倍|腰斩|创新高|创新低|后续走势|未来走势")),
    ("涨跌承诺",
     re.compile(r"必(?:涨|跌)|必然(?:上涨|下跌|套现)|一定(?:会)?(?:涨|跌)|解禁必跌|解禁即抛"
                r"|抛压|抛售压力|冲击成本|资金压力")),
    ("买卖与减持建议",
     re.compile(r"(?:建议|应当|应该|可以|宜)(?:买入|卖出|减持|增持|加仓|减仓|持有|清仓|抄底|离场)"
                r"|逢高(?:减持|卖出)|逢低(?:买入|吸纳)")),
    ("评级与目标价",
     re.compile(r"(?:买入|增持|中性|减持|卖出)评级|目标价|目标位|合理估值|估值区间|强烈推荐")),
    ("解禁压力档位评价",
     re.compile(r"解禁压力(?:大|小|较大|较小|很大|不大|适中)|压力(?:较大|很大|较小|不大|适中)"
                r"|压力大|压力小")),
    ("改数词",
     re.compile(r"(?:约|大约|大概|接近)\s*[\d０-９]|[\d０-９]\s*(?:倍|成|余)?\s*(?:左右|上下)"
                r"|[\d０-９]\s*左右")),
)

BOUND_WORDS = re.compile(r"分红|回购|减持|质押|解押|股东回报")
PLEDGE_WORDS = re.compile(r"质押|解押|解质")
DONE_WORDS = re.compile(r"已发生|减持|分红|回购|股东回报")


def _num(s, unit):
    v = float(s.replace(",", ""))
    if unit == "亿":
        v *= 1e8
    elif unit == "万":
        v *= 1e4
    return v


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


def _same_name(a, b):
    a = a.strip()
    b = b.strip()
    if not a or not b:
        return False
    if a == b or a in b or b in a:
        return True
    sa, sb = set(a), set(b)
    if len(sa) < 2 or len(sb) < 2:
        return False
    return len(sa & sb) / float(min(len(sa), len(sb))) >= 0.6


def _cal_rows(rows):
    out = []
    for lineno, ln in rows:
        s = ln.strip()
        if not s.startswith("-"):
            continue
        parts = [p.strip() for p in s[1:].split("｜")]
        if len(parts) != 3:
            out.append((lineno, None, None, None))
            continue
        d, typ, fact = parts
        out.append((lineno, d, typ, fact))
    return out


def check_text(text):
    """返回 (findings, stats)。findings 为 [(码, 行号, 说明), ...]，行号 0 表示全稿级。"""
    findings = []

    def add(code, lineno, msg):
        findings.append((code, lineno, msg))

    if not text.strip():
        add("LK-STRUCT", 0, "空稿")
        return findings, {}

    head, heads, body = _parse_doc(text)
    names = [n for n, _ in heads]

    # ---------------- 道一 形制 ----------------
    headtext = "\n".join(head)
    for mk in MARK_TEXTS:
        if mk not in headtext:
            add("LK-STRUCT", 1, "头部缺自标「%s」" % mk)

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
                add("LK-STRUCT", i + 1, "基准日不是合法日期：%s" % m.group(1))
            break
        if BASE_LOOSE.match(s):
            base_seen = True
            add("LK-STRUCT", i + 1, "基准日行不是 `基准日：YYYY-MM-DD` 形制")
            break
    if not base_seen:
        add("LK-STRUCT", 1, "缺「基准日：YYYY-MM-DD」行")

    if not any(TRACK.match(ln.strip()) for ln in head):
        add("LK-STRUCT", 1, "缺「跟踪口径：」行")

    for idx, (name, _pat) in enumerate(SECTIONS):
        if name not in names:
            add("LK-STRUCT", 0, "缺第%s节「%s」" % (CN_NUM[idx], name))

    order = [pos for name, pos in heads if name in dict(SECTIONS)]
    if order != sorted(order):
        add("LK-STRUCT", 0, "七节次序乱了：%s" % " / ".join(n for n, _ in heads))

    total_num = None
    total_line = None
    for lineno, ln in body.get("解禁总览", []):
        s = ln.strip()
        if not s.startswith("-"):
            continue
        m = TOTAL_ROW.match(s)
        if m:
            total_num = _num(m.group(1), m.group(2))
            total_line = (lineno, s)
            break
    if total_num is None:
        add("LK-STRUCT", 0, "二节缺「- 总股本：N 股 [S#]」行（四节占比的分母）")

    cal = _cal_rows(body.get("解禁日历", []))
    if not cal:
        add("LK-STRUCT", 0, "三节没有日历行")
    prev = None
    for lineno, d, typ, fact in cal:
        if d is None:
            add("LK-STRUCT", lineno, "日历行不是 `- 日期｜解禁方类型｜一句话事实 [S#]` 三格")
            continue
        if not ISODATE.match(d):
            add("LK-STRUCT", lineno, "解禁日不是 YYYY-MM-DD：%s" % d)
            continue
        if typ not in TYPES:
            add("LK-STRUCT", lineno, "解禁方类型不在册：%s" % typ)
        if not fact:
            add("LK-STRUCT", lineno, "日历行缺一句话事实")
        try:
            cur = date.fromisoformat(d)
        except ValueError:
            add("LK-STRUCT", lineno, "解禁日不是合法日期：%s" % d)
            continue
        if base is not None and cur <= base:
            add("LK-STRUCT", lineno, "解禁日 %s 不晚于基准日 %s——已发生的解禁不进本件日历"
                % (d, base.isoformat()))
        if prev is not None and cur < prev:
            add("LK-STRUCT", lineno, "日历倒序：%s 早于上一行 %s" % (d, prev.isoformat()))
        prev = cur

    pressure = []
    for lineno, ln in body.get("压力测算", []):
        s = ln.strip()
        if not s.startswith("-"):
            continue
        pressure.append((lineno, s))
        if not PRESSURE_SHAPE.match(s):
            add("LK-STRUCT", lineno,
                "压力行形制不符：应写成 `- 第 N 轮 YYYY-MM-DD｜解禁 N 股／占总股本 X.XX%（分母总股本 N 股）｜占比出处：… [S#][S#]`")
    if not pressure:
        add("LK-STRUCT", 0, "四节没有压力测算行")

    if not [1 for _l, ln in body.get("未决事项", []) if ln.strip().startswith("-")]:
        add("LK-STRUCT", 0, "五、未决事项是空节——没走完的轮次一定留下未决事项")

    # ---------------- 道二 锚 ----------------
    for name, _pat in SECTIONS:
        for lineno, ln in body.get(name, []):
            s = ln.strip()
            if not s.startswith("-"):
                continue
            if not ANCHOR.search(s) and "[待人工]" not in s:
                add("LK-QUOTE", lineno, "本行既无 [S#] 锚也无 [待人工]，事实无出处")

    for lineno, s in pressure:
        ids = ANCHOR.findall(s)
        if len(set(ids)) < 2:
            add("LK-QUOTE", lineno,
                "压力行只有 %d 枚不同号锚（%s）——分子与分母必须各挂一处"
                % (len(set(ids)), "、".join(sorted(set(ids))) or "无"))

    if total_line is not None and not ANCHOR.search(total_line[1]):
        add("LK-QUOTE", total_line[0], "总股本行没挂锚——分母必须单独挂源")

    registered = set()
    for lineno, ln in body.get("来源", []):
        s = ln.strip()
        if not s.startswith("-"):
            continue
        m = SOURCE_ID.match(s)
        if not ANCHOR.search(s):
            add("LK-QUOTE", lineno, "来源行缺 [S#] 编号")
        else:
            has_url = bool(URL.search(s))
            has_day = bool(RETRIEVED.search(s))
            if not has_url:
                add("LK-QUOTE", lineno, "来源行缺公告 URL")
            if not has_day:
                add("LK-QUOTE", lineno, "来源行缺「检索日 YYYY-MM-DD」")
            # 只有「编号 + 可点 URL + 检索日」三件齐的行才算登记；缺任何一件，
            # 这枚 S 号就不存在可用出处，正文引用它的地方由下面那道判。
            if m and has_url and has_day:
                registered.add(m.group(1))

    # 正文引用的每一个 [S#] 都必须在来源节有对应登记行；引用了根本不存在的号
    # 等于凭空造出处——比挂错来源更重（挂错至少还挂在真来源上）。
    # 来源节一条合规行都没有时不逐行铺开：根因是来源节整节不合规（上面已逐行报），
    # 这里再按引用铺一遍只会把「哪一行真有问题」淹掉。
    if registered:
        reported_missing = set()
        for name, _pat in SECTIONS:
            if name == "来源":
                continue
            for lineno, ln in body.get(name, []):
                s = ln.strip()
                if not s.startswith("-"):
                    continue
                for ref in sorted(set(ANCHOR.findall(s))):
                    if ref in registered or ref in reported_missing:
                        continue
                    reported_missing.add(ref)
                    add("LK-QUOTE", lineno,
                        "引用了未登记的 [%s]：来源节没有该 S 号的合规来源行"
                        "（须带可点 http(s) URL 与检索日）" % ref)

    # ---------------- 道三 红线 ----------------
    for i, ln in enumerate(text.splitlines()):
        for label, pat in LINE_RULES:
            for clause in re.split(r"[；;。，,｜|]", ln):
                if "[待人工]" in clause:
                    continue
                m = pat.search(clause)
                if m:
                    add("LK-LINE", i + 1, "%s 命中「%s」" % (label, m.group(0)))

    # ---------------- 道四 未取到两向 + 占比不得自算 ----------------
    body_miss = []
    for name in ("一句话结论", "解禁总览", "解禁日历", "压力测算", "未决事项"):
        for lineno, ln in body.get(name, []):
            for m in MISS_BODY.finditer(ln):
                body_miss.append((lineno, m.group(1).strip()))
    six_miss = []
    for lineno, ln in body.get("未取到与口径", []):
        m = MISS_SIX.match(ln.strip())
        if m:
            six_miss.append((lineno, m.group(1).strip()))

    for lineno, item in body_miss:
        if not any(_same_name(item, nm) for _l, nm in six_miss):
            add("LK-GAP", lineno, "正文写「未取到 %s」，六节没有点名它" % item)
    for lineno, item in six_miss:
        if not any(_same_name(item, nm) for _l, nm in body_miss):
            add("LK-GAP", lineno, "六节点名「%s」，正文没有这条未取到" % item)

    koujing_self = any(
        KOUJING.search(ln) and SELF_CALC_WORDS.search(ln)
        for _l, ln in body.get("未取到与口径", [])
    )
    for lineno, s in pressure:
        m = PCT_SRC.search(s)
        if not m:
            add("LK-GAP", lineno,
                "压力行没自报「占比出处」——占比是公告原句里的，还是自己拿股数除的，必须写明")
            continue
        src = m.group(1)
        if "自算" in src and not koujing_self:
            add("LK-GAP", lineno,
                "本行标「自算」，但六节没有写明自算口径——公告没写占比时自算出来的百分比不在原句里，不交代口径等于冒充原句")
        dm = DENOM.search(s)
        if dm and total_num is not None:
            dv = _num(dm.group(1), dm.group(2))
            if abs(dv - total_num) > 1e-6:
                add("LK-GAP", lineno,
                    "分母总股本 %s 股与本稿总股本行 %.0f 股不是同一个数——不同时点总股本不一样，分母拿错整节占比全错"
                    % (dm.group(1), total_num))

    # ---------------- 道五 边界 ----------------
    track = None
    for i, ln in enumerate(head):
        m = TRACK.match(ln.strip())
        if m:
            track = (i + 1, m.group(1).strip())
            break
    if track:
        lineno, val = track
        if PLEDGE_WORDS.search(val):
            add("LK-BOUND", lineno,
                "跟踪口径写成股权质押／解押——质押余额变化走 cn-share-pledge-tracker，本件不登记")
        elif not val.startswith("解禁"):
            add("LK-BOUND", lineno,
                "跟踪口径未以「解禁」起头——未来解禁时间表与已发生的股东行为分属两件")
        if DONE_WORDS.search(val):
            add("LK-BOUND", lineno,
                "跟踪口径混入已发生的股东行为（减持／分红／回购／股东回报）——那一类走 cn-shareholder-return")

    if len(cal) < 2:
        add("LK-BOUND", 0,
            "日历不足两行——本件排的是未来多轮解禁的时间表；只有一轮或已发生的股东行为请走 cn-shareholder-return")

    for lineno, _d_, _typ, fact in cal:
        if not fact:
            continue
        m = BOUND_WORDS.search(fact)
        if not m:
            continue
        if PLEDGE_WORDS.search(fact):
            add("LK-BOUND", lineno,
                "日历行写的是质押／解押（「%s」）——走 cn-share-pledge-tracker" % m.group(0))
        else:
            add("LK-BOUND", lineno,
                "日历行写的是已发生的股东行为（「%s」）——走 cn-shareholder-return" % m.group(0))

    counts = {}
    for code, _l, _m in findings:
        counts[code] = counts.get(code, 0) + 1
    stats = {
        "lines": len(text.splitlines()),
        "sections": len([n for n in names if n in dict(SECTIONS)]),
        "calendar": len(cal),
        "pressure": len(pressure),
        "counts": counts,
    }
    return findings, stats


def report(path, findings, stats):
    for code, lineno, msg in findings:
        where = "全稿" if not lineno else "L%d" % lineno
        print("%s %s  %s" % (code, where, msg))
    print("——")
    print("道一 形制 LK-STRUCT 发条 %d" % stats.get("counts", {}).get("LK-STRUCT", 0))
    print("道二 锚   LK-QUOTE  发条 %d" % stats.get("counts", {}).get("LK-QUOTE", 0))
    print("道三 红线 LK-LINE   发条 %d" % stats.get("counts", {}).get("LK-LINE", 0))
    print("道四 点名 LK-GAP    发条 %d" % stats.get("counts", {}).get("LK-GAP", 0))
    print("道五 边界 LK-BOUND  发条 %d" % stats.get("counts", {}).get("LK-BOUND", 0))
    print("稿=%s 行=%d 节=%d 日历=%d 轮 压力=%d 轮 ｜ 发条合计=%d"
          % (path, stats.get("lines", 0), stats.get("sections", 0),
             stats.get("calendar", 0), stats.get("pressure", 0), len(findings)))


GODD = None  # 占位，真正的样例在下方 GOOD

GOOD = """AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]

基准日：2026-11-09
跟踪口径：解禁（未来解禁的时间表与可算的压力比值，同一只股票的限售股逐轮串起来）

## 一、一句话结论

示例科技未来两轮限售解禁分别在 2026-12-20 与 2027-06-18，两轮解禁股数各 180,000,000 股，占总股本比均取自公告原句 [S1][S2]；分母总股本取 2026 年三季报同一时点 [S3]。

## 二、解禁总览

- 总股本：4,000,000,000 股 [S3]
- 限售股来源：非公开发行（定增）与股权激励 [S1][S2]
- 第 1 轮成本区间：发行价 6.80 元／股 [S1]
- 第 2 轮成本区间：授予价 4.20 元／股 [S2]
- 基准日前已解禁轮次：0 轮 [S3]

## 三、解禁日历

- 2026-12-20｜定增对象｜非公开发行限售股上市流通 180,000,000 股，未取到 具体解禁股东名单 [S1]
- 2027-06-18｜股权激励对象｜限制性股票第一期解锁 180,000,000 股 [S2]

## 四、压力测算

- 第 1 轮 2026-12-20｜解禁 180,000,000 股／占总股本 4.50%（分母总股本 4,000,000,000 股）｜占比出处：公告原文 [S1][S3]
- 第 2 轮 2027-06-18｜解禁 180,000,000 股／占总股本 4.50%（分母总股本 4,000,000,000 股）｜占比出处：公告原文 [S2][S3]

## 五、未决事项

- 第 2 轮解锁条件是否全部达成，以公司后续公告为准 [待人工]
- 两轮解禁股东是否已作相关承诺，在已取到的两份公告中均未披露 [S2]

## 六、未取到与口径

- 未取到 具体解禁股东名单：公告只列发行对象家数，未逐名列示，需回定增发行结果公告核对 [S1]
- 口径：占比取自解禁公告原句，分母总股本取自 2026 年三季报同一时点 [S3]

## 七、来源

- [S1] 示例科技非公开发行限售股上市流通公告 https://example.com/ann/S1 检索日 2026-11-09
- [S2] 示例科技限制性股票激励计划第一期解锁公告 https://example.com/ann/S2 检索日 2026-11-09
- [S3] 示例科技 2026 年第三季度报告 https://example.com/ann/S3 检索日 2026-11-09
"""

# 各坏样只发自己那道码
BAD_STRUCT = GOOD.replace(
    "- 2026-12-20｜定增对象｜", "- 2026-10-01｜定增对象｜")
BAD_QUOTE = GOOD.replace(
    "https://example.com/ann/S3 检索日", "关联网页 检索日")
BAD_LINE = GOOD.replace(
    "- 两轮解禁股东是否已作相关承诺",
    "- 解禁必跌，抛压较大，建议减持；两轮解禁股东是否已作相关承诺")
BAD_GAP = GOOD.replace(
    "- 未取到 具体解禁股东名单：", "- 未取到 第 3 轮成本区间：")
BAD_SELFPCT = GOOD.replace(
    "｜占比出处：公告原文 [S1][S3]", "｜占比出处：自算 [S1][S3]")
BAD_BOUND = GOOD.replace(
    "跟踪口径：解禁（未来解禁的时间表与可算的压力比值，同一只股票的限售股逐轮串起来）",
    "跟踪口径：已发生的减持、分红与回购登记（同一只股票的股东行为逐条串起来）")

# 反证样：不该发的必须不发
OK_SELFPCT = BAD_SELFPCT.replace(
    "- 口径：占比取自解禁公告原句，分母总股本取自 2026 年三季报同一时点 [S3]",
    "- 口径：本轮占比为自算（解禁股数除以同锚总股本），分母总股本取自 2026 年三季报同一时点 [S3]")
BAD_DENOM = GOOD.replace(
    "占总股本 4.50%（分母总股本 4,000,000,000 股）｜占比出处：公告原文 [S1]",
    "占总股本 4.50%（分母总股本 3,800,000,000 股）｜占比出处：公告原文 [S1]")
BAD_ONEANCHOR = GOOD.replace(
    "｜占比出处：公告原文 [S1][S3]", "｜占比出处：公告原文 [S1][S1]")
BAD_PLEDGE = GOOD.replace(
    "跟踪口径：解禁（未来解禁的时间表与可算的压力比值，同一只股票的限售股逐轮串起来）",
    "跟踪口径：质押与解押的余额变化（同一只股票的质押比例逐期串起来）")
OK_HEDGE_EXEMPT = GOOD.replace(
    "- 第 2 轮解锁条件是否全部达成，以公司后续公告为准 [待人工]",
    "- 第 2 轮解锁条件是否全部达成，以公司后续公告为准 [待人工]\n- 本轮占比是否算高，交由人工判断 [待人工]")
BAD_HEDGE_HALF = GOOD.replace(
    "- 第 2 轮解锁条件是否全部达成，以公司后续公告为准 [待人工]",
    "- 第 2 轮解锁条件是否全部达成 [待人工]，建议减持")


def _must_replace(text, old, new):
    """注入坏样前先断言落点唯一：替换目标对不上就 raise，不许静默产出没被注入的样本。"""
    n = text.count(old)
    if n != 1:
        raise AssertionError("夹具注入点出现 %d 次（应唯一）：%r" % (n, old))
    return text.replace(old, new)


# 坏样：引用一枚来源节根本不存在的锚号（S999）。压力行仍有两枚不同号锚，
# 所以「不同号」那条不响；响的只有「引用了未登记的 [S#]」。
BAD_UNKNOWN_ANCHOR = _must_replace(
    GOOD,
    "｜占比出处：公告原文 [S1][S3]",
    "｜占比出处：公告原文 [S1][S999]")

# 反证：来源行在册但缺 URL ⇒ 该号不算登记，正文引用它照样发（同一根因不重复铺开）。
BAD_UNREG_SOURCE = _must_replace(
    GOOD,
    "https://example.com/ann/S2 检索日",
    "关联网页 检索日")

# 反证：[S1][S2] 两枚都在册，只是分母挂在 S3 而非 S2 —— 现状**不发**，
# 因为本件只判「锚号存在且合规」；「分母必须单独挂源」由总股本行那道管。
OK_ANCHOR_EXISTS_DENOM_ELSEWHERE = _must_replace(
    GOOD,
    "｜占比出处：公告原文 [S1][S3]",
    "｜占比出处：公告原文 [S1][S2]")


def _codes(text):
    findings, _stats = check_text(text)
    return findings, set(c for c, _l, _m in findings)


def selftest():
    cases = (
        ("好样应零发条", GOOD, set()),
        ("形制：解禁日早于基准日", BAD_STRUCT, {"LK-STRUCT"}),
        ("锚：来源行缺 URL", BAD_QUOTE, {"LK-QUOTE"}),
        ("红线：必跌＋抛压＋建议减持", BAD_LINE, {"LK-LINE"}),
        ("点名：六节与正文两向不符", BAD_GAP, {"LK-GAP"}),
        ("自算：标了自算但六节无口径", BAD_SELFPCT, {"LK-GAP"}),
        ("边界：跟踪口径写成已发生股东行为", BAD_BOUND, {"LK-BOUND"}),
        ("边界：跟踪口径写成质押解押", BAD_PLEDGE, {"LK-BOUND"}),
        ("反证：自算并写了口径 → 不发", OK_SELFPCT, set()),
        ("反证：[待人工] 只豁免自己那句", BAD_HEDGE_HALF, {"LK-LINE"}),
        ("反证：待人工行独立成立 → 不发", OK_HEDGE_EXEMPT, set()),
        ("分母：压力行分母与总股本行不同数", BAD_DENOM, {"LK-GAP"}),
        ("锚：压力行两枚同号锚", BAD_ONEANCHOR, {"LK-QUOTE"}),
        ("锚：引用来源节不存在的 [S999]", BAD_UNKNOWN_ANCHOR, {"LK-QUOTE"}),
        ("锚：来源行缺 URL ⇒ 该号未登记，引用即发", BAD_UNREG_SOURCE, {"LK-QUOTE"}),
        ("反证：[S1][S2] 均在册、分母挂在别处 → 只验存在性，不发",
         OK_ANCHOR_EXISTS_DENOM_ELSEWHERE, set()),
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
    ap = argparse.ArgumentParser(description="限售解禁压力稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="解禁稿 .md 路径")
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
