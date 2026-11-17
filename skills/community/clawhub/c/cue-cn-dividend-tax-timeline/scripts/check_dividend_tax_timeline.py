#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_dividend_tax_timeline.py — 分红到账与扣税时间轴的机检（零网络、只读传入文件）。

五道码（缺一即不叫过闸）：
  DT-STRUCT 形制：五段齐（头部申报／时间轴／分类型税负／未取到清单／待人工）；
             三日期节点**行级在场**（股权登记日／除权除息日／现金红利发放日，各占一行）；
             五类股东**行级在场**（个人股东／证券投资基金／合格境外机构投资者／香港投资者／其他法人股东）；
             三节点日期**须有序**（登记日 ≤ 除权除息日 ≤ 发放日）——顺序错了就是钱到账的时点错了；
             非「未取到」的股东行**三要素齐**：适用税率（百分比）·计税基数（每股派息类名词）·扣税后实得
             （税后／实得／扣税后／净额类名词），缺一即发；
  DT-QUOTE  原句与锚：每行的书名号（「」『』«»）内原句不得为空或只剩单字；「锚：」标签在而锚值为空同样发；
  DT-LINE   红线三道：①定式禁词——择时建议（建议持有到登记日·建议登记日前买入·抢权·填权行情·除权前买入·
             建议在股权登记日买入·持有至登记日·登记日前加仓）、评级目标价（目标价·评级·买入评级·增持评级·
             强烈推荐·建议买入·建议卖出）、收益承诺（稳赚·零风险·保证收益·必涨·必跌·包赚）、
             代办（代拟·代算·代申报·代客）；②主题词×判断语气同段（主题词＝税率·税负·扣税·到账·登记日·
             除权除息·红利·股息·股东·实得·净额·分红，判断语气＝应当·应予·将·会·必·有望·可期·可能·
             足以·构成·属于·意味着·高于·低于·划算·合理·偏高·偏低·充分·不足·无疑·显然·肯定）；
             ③自裁效力层（裁定前缀 结论／综上／因此／本件认为／判定／认定 与 效力判断 有效／无效／成立／
             不成立／违法／违规／合规／属实／构成承诺 同现即发）。`[待人工]` 标记与免责句都**只登记自己那一分句**
             （按分号·句号·逗号 cut 后逐段判），同一行后半写的肯定预测照发；机构名「X 会」与「会 X」里的「会」
             先按形态从语气域洗掉（董事会·股东大会·监事会·审计委员会都不误红）；
  DT-GAP    未取到两向点名 + 税率不得套默认：
             ①头部「共五类股东·未取到 N 类」只准出现一处（两处并存即发），且 N 必须等于分类型税负段里
             写「未取到」的行数——**两向**：申报多了是虚报，申报少了是漏报，两个方向都发；
             ②把「未取到」写成「无此项／不适用／无需扣税」一律发（那是替公告下结论，不是登记）；
             ③**本域最要紧的一格：税率数字必须在该行自己的书名号原句里出现**。公告没写某类股东的税率时，
             卡面若凭常识填 20%／10%，那个数字在原句里找不到 ⇒ 发「套用默认税率」。这条是本域与
             「分红方案速读」的分水岭：税率是**公告说的**，不是**税法默认的**；
  DT-BOUND  边界：本件只做「钱什么时候到、扣多少」。卡面若出现 `- 分红方案与每股派息：`／
             `- 分红总额与分红率：`／`- 回购方案与回购规模：` 这类**分红方案速读**的项行，
             说明写错了件 ⇒ 点名改走 `cn-shareholder-return`（那一枚做八项逐字登记，本件不重复登记方案本身）。

用法：
  python3 -B scripts/check_dividend_tax_timeline.py <待检文件>      # 逐条发红，全过则 PASS
  python3 -B scripts/check_dividend_tax_timeline.py --selftest      # 好样须过、坏样五道齐发、对照样不误伤
  python3 -B scripts/check_dividend_tax_timeline.py --help
退码：0＝过（或自测全合）；1＝发红／自测不合；2＝用法错。
"""
from __future__ import annotations

import argparse
import atexit
import os
import pathlib
import re
import shutil
import sys
import tempfile

TMP_ROOTS: list[pathlib.Path] = []

# 三日期节点：钱到账的时点链。顺序错了就是时点错了，所以 DT-STRUCT 要判有序。
TIMELINE = ("股权登记日", "除权除息日", "现金红利发放日")

# 五类股东：公告的扣税说明通常按这五类分列。缺哪类就写「未取到」，不补常识。
SHAREHOLDERS = ("个人股东", "证券投资基金", "合格境外机构投资者", "香港投资者", "其他法人股东")

# 股东类型别名：真实公告里同一类有不同叫法，命中任一别名即归到同一枚 canonical 类。
SH_ALIASES = {
    "个人股东": ("个人股东", "自然人股东", "个人投资者", "境内个人股东"),
    "证券投资基金": ("证券投资基金", "公募基金", "证券投资基金股东", "基金股东"),
    "合格境外机构投资者": ("合格境外机构投资者", "QFII", "RQFII", "合格境外机构投资者（QFII）",
                          "合格境外机构投资者(QFII)"),
    "香港投资者": ("香港投资者", "沪股通投资者", "深股通投资者", "港股通投资者", "香港中央结算"),
    "其他法人股东": ("其他法人股东", "法人股东", "机构投资者", "其他机构投资者", "居民企业股东"),
}
_ALIAS_PAIRS = sorted(((a, c) for c, al in SH_ALIASES.items() for a in al), key=lambda p: -len(p[0]))
_ALIAS_TO_CANON = dict(_ALIAS_PAIRS)
SH_ITEM = re.compile(r"^\s*[-*]\s*(" + "|".join(map(re.escape, [a for a, _ in _ALIAS_PAIRS])) + r")[：:]")
TL_ITEM = re.compile(r"^\s*[-*]\s*(" + "|".join(TIMELINE) + r")[：:]")

QUOTES = re.compile(r"[「『«]([^」』»]*)[」』»]")
ANCHOR_SPLIT = re.compile(r"锚[:：]")
ANCHOR_VAL = re.compile(r"锚[:：]\s*(\S.*)$")
DECL = re.compile(r"共\s*(?:五|5)\s*类\s*股东\s*[·：:|｜、]\s*未取到\s*(\d+)\s*类")
EMPTY_LIE = re.compile(r"(?:^|[\s：:])无(?:此项|该类)|不适用|无需扣税|无须扣税|不涉及扣税")
CORE_STRIP = re.compile(r"[\s　「」『»«“”（）()《》【】，,。.；;：:、！!？~\-—_·/％%*#]+")
SECTIONS = (("头部申报", r"头部申报"), ("时间轴", r"时间轴"),
            ("分类型税负", r"分类型税负|分类型扣税|税负"), ("未取到清单", r"未取到清单|缺数清单"),
            ("待人工", r"待人工"))
TL_HEAD = re.compile(r"^#{1,4}\s*(?:[一二三四五六七八九十\d]+\s*[、.．]\s*)?时间轴")
SH_HEAD = re.compile(r"^#{1,4}\s*(?:[一二三四五六七八九十\d]+\s*[、.．]\s*)?(?:分类型税负|分类型扣税|税负)")
ANY_HEAD = re.compile(r"^#{1,4}\s")

# 税率：百分比。本域只认百分比形，不认「按 20 个点」这类口语。
RATE = re.compile(r"\d+(?:\.\d+)?\s*[%％]")
# 计税基数：公告里税基通常写成「每股派发现金红利 X 元」这类，不是分红总额。
BASE_NOUN = re.compile(r"计税基数|税基|每股派发现金红利|每股派发|每股现金红利|每股红利|每股股利|"
                       r"每股派息|派发现金红利|现金红利金额|红利金额|股息金额")
# 扣税后实得：公告写「每股实际派发现金红利」「税后」「实得」「扣税后」「净额」。
NET_NOUN = re.compile(r"实际派发|税后|实得|扣税后|扣除后|净额|实际到手|实际发放")
# 日期：三种常见写法。
DATE = re.compile(r"(\d{4})\s*(?:年|[-/.])\s*(\d{1,2})\s*(?:月|[-/.])?\s*(\d{1,2})\s*日?")
MISSING = re.compile(r"未取到|未检索到")

# 分红方案速读的项行：出现即说明写错了件（DT-BOUND）。
FOREIGN_ITEMS = re.compile(r"^\s*[-*]\s*(?:分红方案与每股派息|分红总额与分红率|股权登记日与除权除息日|"
                           r"回购方案与回购规模|回购价格区间与资金来源|回购用途与注销安排|"
                           r"减持计划与减持主体|质押与解押情况)[：:]")

# ── 红线词族（DT-LINE ①）────────────────────────────────────────────────
NOUN_FORM = r"(?![性度论])"
VALUER_WORDS = "|".join(w + NOUN_FORM for w in (
    "划算", "合理", "偏高", "偏低", "充分", "不足", "优惠", "有吸引力"))
DEGREE_WORDS = r"很|较为|比较|基本|大体|显然|明显|相当"
TIMING_ASSERT = (r"建议持有到登记日|建议持有至登记日|持有到登记日|持有至登记日|"
                 r"建议(?:在)?(?:股权)?登记日前(?:买入|加仓|增持)|"
                 r"建议(?:在)?除权(?:除息)?前(?:买入|加仓|增持)|"
                 r"登记日前(?:买入|加仓|增持)|除权前(?:买入|加仓|增持)|"
                 r"抢权|填权行情|抢权行情|除权前布局")
RATING_ASSERT = (r"目标价|评级|买入评级|增持评级|强烈推荐|建议买入|建议卖出|建议增持|建议减持|建议持有")
PROMISE_ASSERT = r"稳赚|零风险|保证收益|必涨|必跌|包赚|无风险套利"
AGENT_ASSERT = r"代拟|代算|代申报|代客|代办申报"
TAX_VALUER = (r"(?:税率|税负|扣税|实得|净额|到手)(?:的)?(?:" + DEGREE_WORDS + r")?(?:" + VALUER_WORDS + r")")
BANNED = re.compile(TIMING_ASSERT + r"|" + RATING_ASSERT + r"|" + PROMISE_ASSERT + r"|" +
                    AGENT_ASSERT + r"|" + TAX_VALUER)
SUBJECT = re.compile(r"税率|税负|扣税|到账|登记日|除权除息|红利|股息|股东|实得|净额|分红|发放日")
TONE = re.compile(r"应当|应予|予以|将|会|必|有望|可期|可能|足以|构成|属于|意味着|高于|低于|"
                  r"无疑|显然|肯定|应(?!急)|" + VALUER_WORDS)
VERDICT = re.compile(r"结论|综上|因此|可见|据此|本院认为|本件认为|本卡认为|本件判断|判定|认定|断言")
EFFECT = re.compile(r"无效|有效|作废|不成立|成立|撤销|违法|违规|合规|属实|构成承诺|应当披露|"
                    r"应予支持|予以支持|应支持|支持|必然")
CITE_LABEL = re.compile(
    r"原文|摘录|引用|节选|摘自|引自|转引|照录|载明|列明|记载|披露|约定|规定|显示|表明|称|据|见|详见|"
    r"公告|报告书|说明书|决议|预案|合同|章程|公示|办法|指引|指导意见|通知|"
    r"第[一二三四五六七八九十百零\d]+[节条章项款页行段]|页|行|段")
LABEL_PUNCT = re.compile(r"[\s　（）()【】\[\]：:，,。.、·\-—_/｜|]+")
INNER_LABEL = re.compile(r"^\s*([^，。；：:]{1,12})[：:]")
SELF_REF_LEAD = "据经由按依对向在被将把以因故但而且并或若如虽即则从自于给替为跟同和与及照就"
SELF_REF = re.compile(r"(?:(?<![一-龥])|(?<=[" + SELF_REF_LEAD + r"]))(?:本件|本卡|本速读|笔者)")
DISCLAIM = re.compile(r"不接|不出|不提供|不作|不判|不碰|不做|不代|禁止|未证|无法|不承诺|不给")
PENDING = re.compile(r"\[待人工\]")
CLAUSE = re.compile(r"[；;。，,]")
NOUN_WASH = re.compile(r"[员委事大东议工学协商年例常布明谈论聚汇组独立]会|会[计议场话晤所馆堂员]")


# ── 基础工具 ────────────────────────────────────────────────────────────

def canon(name: str) -> str:
    return _ALIAS_TO_CANON.get(name, name)


def core_len(s: str) -> int:
    return len(CORE_STRIP.sub("", s or ""))


def parse_sh_line(line: str):
    """`- 个人股东：正文` → (canonical 类, 正文)；不是股东行返回 (None, None)。"""
    m = SH_ITEM.match(line)
    if not m:
        return None, None
    return canon(m.group(1)), line[m.end():]


def parse_tl_line(line: str):
    """`- 股权登记日：正文` → (节点名, 正文)；不是时间轴行返回 (None, None)。"""
    m = TL_ITEM.match(line)
    if not m:
        return None, None
    return m.group(1), line[m.end():]


def quote_field(body: str) -> str:
    return " ".join(QUOTES.findall(body))


def is_cite_label(s: str) -> bool:
    return bool(CITE_LABEL.search(LABEL_PUNCT.sub("", s or "")))


def inner_ok(q: str) -> bool:
    m = INNER_LABEL.match(q)
    return True if not m else is_cite_label(m.group(1))


def no_self_ref(q: str) -> bool:
    return not SELF_REF.search(q)


def own_field(body: str) -> str:
    """DT-LINE 的判据域：剥掉锚**值**，剥掉**纯引注**的书名号；非纯引注的留在域内照扫。

    ⚠ 只剥锚值本身（`锚：公告 五` 里的「公告 五」是定位词），**锚值之后的分句照扫**。
    锚是行尾标签，不是判据域的终点——在锚后写断言必须照样发红。
    """
    parts = ANCHOR_SPLIT.split(body)
    head = parts[0]
    for tail in parts[1:]:
        pieces = CLAUSE.split(tail, maxsplit=1)
        if len(pieces) > 1:
            head += " " + pieces[1]
    out, pos = [], 0
    for m in QUOTES.finditer(head):
        out.append(head[pos:m.start()])
        q = m.group(1)
        if not (no_self_ref(q) and inner_ok(q)):
            out.append(q)
        pos = m.end()
    out.append(head[pos:])
    return " ".join(out)


def dates_in(text: str):
    """抽出文本里的日期，返回 [(y,m,d)]。"""
    return [(int(a), int(b), int(c)) for a, b, c in DATE.findall(text)]


def zone_of(lines, head_rx):
    """返回某段的 (起, 止) 行号；没有该段返回 None。"""
    start = None
    for i, ln in enumerate(lines):
        if head_rx.match(ln):
            start = i + 1
            continue
        if start is not None and ANY_HEAD.match(ln):
            return start, i
    return (start, len(lines)) if start is not None else None


# ── 五道码 ──────────────────────────────────────────────────────────────

def check_text(text: str):
    """返回 (findings, stats)。findings = [(码, 行号, 说明)]。"""
    findings = []
    lines = text.splitlines()

    # ── DT-STRUCT ──
    heads = "\n".join(ln for ln in lines if ANY_HEAD.match(ln))
    for label, rx in SECTIONS:
        if not re.search(rx, heads):
            findings.append(("DT-STRUCT", 0, "缺段：" + label))

    tl_zone = zone_of(lines, TL_HEAD)
    if tl_zone is None:
        findings.append(("DT-STRUCT", 0, "缺「时间轴」段，三日期节点无处占行"))
        tl_zone = (0, 0)
    tl_seen = {}
    for i in range(tl_zone[0], tl_zone[1]):
        name, body = parse_tl_line(lines[i])
        if name is None:
            continue
        if name in tl_seen:
            findings.append(("DT-STRUCT", i + 1, "日期节点重复占行：" + name))
        tl_seen[name] = (i, body)
    for name in TIMELINE:
        if name not in tl_seen:
            findings.append(("DT-STRUCT", 0, "时间轴段内缺节点行：" + name))

    # 三节点有序：登记日 ≤ 除权除息日 ≤ 发放日。顺序错了就是钱到账的时点错了。
    seq = []
    for name in TIMELINE:
        if name not in tl_seen:
            continue
        i, body = tl_seen[name]
        ds = dates_in(quote_field(body) or body)
        if not ds:
            findings.append(("DT-STRUCT", i + 1, name + "：行内无日期"))
            continue
        seq.append((name, ds[0], i))
    for a, b in zip(seq, seq[1:]):
        if a[1] > b[1]:
            findings.append(("DT-STRUCT", b[2] + 1,
                             "日期节点次序错：%s(%04d-%02d-%02d) 晚于 %s(%04d-%02d-%02d)"
                             % (a[0], *a[1], b[0], *b[1])))

    sh_zone = zone_of(lines, SH_HEAD)
    if sh_zone is None:
        findings.append(("DT-STRUCT", 0, "缺「分类型税负」段，五类股东无处占行"))
        sh_zone = (0, 0)
    sh_seen = {}
    for i in range(sh_zone[0], sh_zone[1]):
        name, body = parse_sh_line(lines[i])
        if name is None:
            continue
        if name in sh_seen:
            findings.append(("DT-STRUCT", i + 1, "股东类型重复占行：" + name))
        sh_seen[name] = (i, body)
    for name in SHAREHOLDERS:
        if name not in sh_seen:
            findings.append(("DT-STRUCT", 0, "分类型税负段内缺股东行：" + name))

    # 非「未取到」的股东行三要素齐：税率·计税基数·扣税后实得
    for name, (i, body) in sh_seen.items():
        if MISSING.search(body):
            continue
        q = quote_field(body)
        if not RATE.search(q):
            findings.append(("DT-STRUCT", i + 1, name + "：原句里没有适用税率（百分比）"))
        if not BASE_NOUN.search(q):
            findings.append(("DT-STRUCT", i + 1, name + "：原句里没有计税基数名词"))
        if not NET_NOUN.search(q):
            findings.append(("DT-STRUCT", i + 1, name + "：原句里没有扣税后实得名词"))

    # ── DT-QUOTE ──
    for name, (i, body) in list(tl_seen.items()) + list(sh_seen.items()):
        qs = QUOTES.findall(body)
        if not qs:
            if not MISSING.search(body):
                findings.append(("DT-QUOTE", i + 1, name + "：无书名号原句"))
            continue
        for q in qs:
            if core_len(q) <= 1:
                findings.append(("DT-QUOTE", i + 1, name + "：书名号内原句为空或只剩单字"))
        m = ANCHOR_VAL.search(body)
        if not m:
            findings.append(("DT-QUOTE", i + 1, name + "：缺「锚：」"))
        elif not m.group(1).strip():
            findings.append(("DT-QUOTE", i + 1, name + "：锚值为空"))

    # ── DT-LINE ──
    for i, ln in enumerate(lines):
        if not ln.strip():
            continue
        name, body = parse_sh_line(ln)
        if name is None:
            name, body = parse_tl_line(ln)
        dom = own_field(body) if body is not None else ln
        for cl in CLAUSE.split(dom):
            if PENDING.search(cl) or DISCLAIM.search(cl):
                continue
            tone_dom = NOUN_WASH.sub("", cl)
            for m in BANNED.finditer(cl):
                findings.append(("DT-LINE", i + 1, "定式禁词：" + m.group(0)))
            if body is not None and SUBJECT.search(cl) and TONE.search(tone_dom):
                findings.append(("DT-LINE", i + 1, "主题词×判断语气同段：" + cl.strip()[:40]))
            if VERDICT.search(cl) and EFFECT.search(cl):
                findings.append(("DT-LINE", i + 1, "自裁效力层：" + cl.strip()[:40]))

    # ── DT-GAP ──
    decls = []
    for i, ln in enumerate(lines):
        for m in DECL.finditer(ln):
            decls.append((i + 1, int(m.group(1))))
    if len(decls) != 1:
        findings.append(("DT-GAP", 0, "未取到申报须恰一枚，实有 %d 枚" % len(decls)))
    missing = 0
    for i in range(sh_zone[0], sh_zone[1]):
        name, body = parse_sh_line(lines[i])
        if name is not None and MISSING.search(body):
            missing += 1
    if len(decls) == 1 and decls[0][1] != missing:
        findings.append(("DT-GAP", decls[0][0],
                         "申报未取到 %d 类，分类型税负段实有「未取到」%d 行（两向都发）"
                         % (decls[0][1], missing)))
    for i, ln in enumerate(lines):
        if EMPTY_LIE.search(ln):
            findings.append(("DT-GAP", i + 1, "把「未取到」写成「无此项／不适用／无需扣税」"))

    # 税率数字必须在该行自己的书名号原句里出现——公告没写就不能凭常识填。
    for name, (i, body) in sh_seen.items():
        if MISSING.search(body):
            continue
        q = quote_field(body)
        for m in RATE.finditer(body):
            if m.group(0) not in q:
                findings.append(("DT-GAP", i + 1,
                                 name + "：税率 %s 不在本行原句里（套用默认税率）" % m.group(0)))

    # ── DT-BOUND ──
    for i, ln in enumerate(lines):
        if FOREIGN_ITEMS.match(ln):
            findings.append(("DT-BOUND", i + 1,
                             "出现分红方案速读的项行，本件不登记方案本身——改走 cn-shareholder-return"))

    stats = {"tl": len(tl_seen), "sh": len(sh_seen), "missing": missing, "decls": len(decls)}
    return findings, stats


# ── 临时件与自测 ────────────────────────────────────────────────────────

def make_tmp(suffix: str = ".md") -> pathlib.Path:
    root = pathlib.Path(tempfile.mkdtemp(prefix="div-tax.", dir=os.environ.get("TMPDIR") or None))
    TMP_ROOTS.append(root)
    return root / ("case" + suffix)


def _cleanup():
    for r in TMP_ROOTS:
        shutil.rmtree(r, ignore_errors=True)
    TMP_ROOTS.clear()


GOOD = """# 分红到账与扣税时间轴（样例·好样）

## 一、头部申报
- 文件：示例股份有限公司 2025 年年度权益分派实施公告｜来路：官方原文｜附件腿：未发起
- 共五类股东·未取到 1 类

## 二、时间轴
- 股权登记日：「股权登记日为 2026 年 6 月 12 日」 锚：公告 二、本次权益分派方案
- 除权除息日：「除权除息日为 2026 年 6 月 15 日」 锚：公告 二、本次权益分派方案
- 现金红利发放日：「现金红利发放日为 2026 年 6 月 19 日」 锚：公告 二、本次权益分派方案

## 三、分类型税负
- 个人股东：「对个人股东每股实际派发现金红利 0.28 元，按 20% 的税率代扣个人所得税，计税基数为每股派发现金红利 0.35 元」 锚：公告 四、扣税说明
- 证券投资基金：「对证券投资基金每股实际派发现金红利 0.28 元，按 20% 的税率代扣个人所得税」 锚：公告 四、扣税说明
- 合格境外机构投资者：「对合格境外机构投资者按 10% 的税率代扣企业所得税，每股实际派发现金红利 0.315 元」 锚：公告 四、扣税说明
- 香港投资者：「对香港投资者按 10% 的税率代扣所得税，每股实际派发现金红利 0.315 元」 锚：公告 四、扣税说明
- 其他法人股东：未取到（未取到清单已点名）

## 四、未取到清单
- 未取到 1 类：其他法人股东——本次取得的公告未列该类股东的扣税口径，需回完整公告与税务说明核对。

## 五、待人工
- [待人工] 各类股东的实际到手金额、是否值得持有到登记日，全部留人工；本件不接代办，也不给择时建议。
"""

BAD_STRUCT = GOOD.replace("## 四、未取到清单", "## 四、缺项清单").replace(
    "- 除权除息日：「除权除息日为 2026 年 6 月 15 日」 锚：公告 二、本次权益分派方案",
    "- 除权除息日：「除权除息日为 2026 年 6 月 10 日」 锚：公告 二、本次权益分派方案")
BAD_QUOTE = GOOD.replace(
    "- 香港投资者：「对香港投资者按 10% 的税率代扣所得税，每股实际派发现金红利 0.315 元」 锚：公告 四、扣税说明",
    "- 香港投资者：「」 锚：")
BAD_LINE = GOOD.replace(
    "- [待人工] 各类股东的实际到手金额、是否值得持有到登记日，全部留人工；本件不接代办，也不给择时建议。",
    "- [待人工] 各类股东的实际到手金额留人工；建议持有到登记日，目标价 15 元，稳赚。")
BAD_GAP = GOOD.replace("- 共五类股东·未取到 1 类", "- 共五类股东·未取到 0 类")
# 套用默认税率：公告原句只写「按适用税率代扣」，卡面自己补 20%——那个数字在本行原句里找不到。
# 这是本域最要紧的一格：税率是**公告说的**，不是**税法默认的**。
BAD_RATE = GOOD.replace(
    "- 其他法人股东：未取到（未取到清单已点名）",
    "- 其他法人股东：「对其他法人股东按适用税率代扣企业所得税」 按 25% 的税率，每股实际派发现金红利 0.2625 元 锚：公告 四、扣税说明").replace(
    "- 共五类股东·未取到 1 类", "- 共五类股东·未取到 0 类").replace(
    "- 未取到 1 类：其他法人股东——本次取得的公告未列该类股东的扣税口径，需回完整公告与税务说明核对。",
    "- 本次五类股东扣税口径均已取到。")
BAD_BOUND = GOOD.replace(
    "- 股权登记日：「股权登记日为 2026 年 6 月 12 日」 锚：公告 二、本次权益分派方案",
    "- 分红方案与每股派息：「每 10 股派发现金红利 3.50 元（含税）」 锚：公告 一")


def selftest() -> int:
    bad = 0
    f, _ = check_text(GOOD)
    if f:
        bad += 1
        print("✗ 好样不该发红：", f[:3])
    else:
        print("✓ 好样全过")
    cases = (("DT-STRUCT", BAD_STRUCT), ("DT-QUOTE", BAD_QUOTE), ("DT-LINE", BAD_LINE),
             ("DT-GAP", BAD_GAP), ("DT-GAP", BAD_RATE), ("DT-BOUND", BAD_BOUND))
    for want, txt in cases:
        f, _ = check_text(txt)
        codes = sorted({c for c, _i, _m in f})
        if want in codes:
            print("✓ 坏样发红 %s（共 %d 条）" % (want, len(f)))
        else:
            bad += 1
            print("✗ 坏样未发 %s，实发 %s" % (want, codes))
    f, _ = check_text(GOOD)
    if any(c == "DT-LINE" for c, _i, _m in f):
        bad += 1
        print("✗ 对照样误伤 DT-LINE")
    else:
        print("✓ 对照样不误伤")
    _cleanup()
    print("自测：%s" % ("全合" if bad == 0 else "不合 %d 档" % bad))
    return 0 if bad == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="分红到账与扣税时间轴机检（零网络）")
    ap.add_argument("path", nargs="?", help="待检 Markdown 文件")
    ap.add_argument("--selftest", action="store_true", help="跑内置好样/坏样自测")
    args = ap.parse_args()
    atexit.register(_cleanup)
    if args.selftest:
        return selftest()
    if not args.path:
        ap.print_help()
        return 2
    p = pathlib.Path(args.path)
    if not p.is_file():
        print("用法错：文件不存在 %s" % p, file=sys.stderr)
        return 2
    findings, stats = check_text(p.read_text(encoding="utf-8"))
    for code, ln, msg in findings:
        print("%s 第%d行 %s" % (code, ln, msg))
    if findings:
        print("不合 %d 条｜节点 %d 枚｜股东 %d 类｜未取到 %d 类｜申报 %d 枚"
              % (len(findings), stats["tl"], stats["sh"], stats["missing"], stats["decls"]))
        return 1
    print("PASS｜节点 %d 枚｜股东 %d 类｜未取到 %d 类｜申报 %d 枚"
          % (stats["tl"], stats["sh"], stats["missing"], stats["decls"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
