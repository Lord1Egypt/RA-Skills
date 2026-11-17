#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_pledge_tracker.py — 股权质押与解押跟踪的机检（零网络、只读传入文件）。

五道码（缺一即不叫过闸）：
  SP-STRUCT 形制：五段齐（头部申报／本次变动明细／累计与剩余／未取到清单／待人工）；
             变动明细段每笔**行级在场**（`- 质押：` / `- 解押：`，只在散文里提到不算）；
             质押行**六要素齐**（出质人·质权人·质押股数·占所持比例·占总股本比例·质押期间），
             解押行**三要素齐**（出质人·解押股数·解押日期），缺一即发；
             累计与剩余段每行须是**两处之间的差**（`前值 → 后值`），只有一处不构成变化；
  SP-QUOTE  原句与锚：每行的书名号（「」『』«»）内原句不得为空或只剩单字；「锚：」标签在而锚值为空同样发；
  SP-LINE   红线三道：①定式禁词——平仓风险判断（有平仓风险·面临平仓·爆仓风险·触及预警线·触及平仓线·
             风险可控·风险不大·质押安全）、评级目标价（目标价·评级·买入评级·增持评级·强烈推荐·
             建议买入·建议卖出·建议增持·建议减持·建议持有）、股价预测（股价将·股价会·利空·利好·
             压制股价·提振股价）、收益承诺（稳赚·零风险·保证收益·必涨·必跌）、代办（代拟·代算·代申报·代客）、
             比例高低评价（质押比例偏高·偏低·合理·过高·充分·不足）；
             ②主题词×判断语气同段（主题词＝质押·解押·出质·质权·平仓·预警线·平仓线·履约保障·
             累计质押·质押比例·占总股本·占所持，判断语气＝应当·应予·将·会·必·有望·可期·可能·
             足以·构成·属于·意味着·高于·低于·划算·合理·偏高·偏低·充分·不足·无疑·显然·肯定）；
             ③自裁效力层（裁定前缀 结论／综上／因此／本件认为／判定／认定 与 效力判断 有效／无效／
             成立／不成立／违法／违规／合规／属实 同现即发）。`[待人工]` 标记与免责句都**只登记自己那一分句**
             （按分号·句号·逗号 cut 后逐段判），同一行后半写的断言照发；机构名「X 会」与「会 X」里的「会」
             先按形态从语气域洗掉（董事会·股东大会·监事会·审计委员会都不误红）；
  SP-GAP    未取到两向点名 + **比例不得自算**：
             ①头部「共 N 笔质押变动·未取到 M 笔」只准出现一处（两处并存即发），且 M 必须等于变动明细段里
             写「未取到」的行数——**两向**：申报多了是虚报，申报少了是漏报，两个方向都发；
             ②把「未取到」写成「无此项／不适用／无需披露」一律发（那是替公告下结论，不是登记）；
             ③**本域最要紧的一格：比例数字必须在该行自己的书名号原句里出现**。公告没写「占其所持股份比例」
             或「占公司总股本比例」时，卡面若拿质押股数除以持股数或总股本自己算，那个百分比在原句里找不到
             ⇒ 发「自算比例」。这条是本域与「股东回报速读」的分水岭：比例是**公告说的**，不是**卡面算的**——
             分母可能是持股数、可能是总股本、可能是剔除回购专户后的股本，算错一个分母，风险读数就全错；
  SP-BOUND  边界：本件只做「质押余额怎么变」。卡面若出现 `- 分红方案与每股派息：`／`- 回购方案与回购规模：`
             这类**股东回报速读**的项行，说明写错了件 ⇒ 点名改走 `cn-shareholder-return`；
             若出现 `事件类型：` 这类**单份公告速读**的单选行 ⇒ 点名改走 `event-brief-cn`。

用法：
  python3 -B scripts/check_pledge_tracker.py <待检文件>      # 逐条发红，全过则 PASS
  python3 -B scripts/check_pledge_tracker.py --selftest      # 好样须过、坏样六枚各发其码、对照样不误伤
  python3 -B scripts/check_pledge_tracker.py --help
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

# 两类变动：质押（余额增加）与解押（余额减少）。本件只登记这两类，别的股东行为不接。
KINDS = ("质押", "解押")

# 质押行六要素：公告的质押公告通常按这六格写。缺哪格就写「未取到」，不补常识。
PLEDGE_CELLS = (
    ("出质人", re.compile(r"出质人|质押人|质押股东|出质股东|股东名称|控股股东|大股东")),
    ("质权人", re.compile(r"质权人|质权方|受托人|质权代理人|银行|信托|证券|资产管理")),
    ("质押股数", re.compile(r"质押(?:的)?(?:股份|股票)?(?:数量|股数)|质押(?:了)?[\d,，.]+\s*(?:万)?股|"
                            r"本次质押(?:股份)?(?:数量)?")),
    ("占所持比例", re.compile(r"占(?:其)?(?:所)?持(?:有)?(?:公司)?股份(?:总数)?(?:的)?(?:比例)?|"
                              r"占其持股|占所持股份")),
    ("占总股本比例", re.compile(r"占(?:公司)?(?:总)?股本(?:总数)?(?:的)?(?:比例)?|占总股本")),
    ("质押期间", re.compile(r"质押(?:期限|期间|起止)|起始日|到期日|质押登记日|解除日|购回日|"
                            r"自\s*\d{4}|至\s*\d{4}")),
)
# 解押行三要素。
RELEASE_CELLS = (
    ("出质人", re.compile(r"出质人|质押人|质押股东|出质股东|股东名称|控股股东|大股东")),
    ("解押股数", re.compile(r"解除质押(?:的)?(?:股份|股票)?(?:数量|股数)|解押(?:的)?(?:股份|股票)?(?:数量|股数)|"
                            r"本次解除质押|解除质押[\d,，.]+\s*(?:万)?股")),
    ("解押日期", re.compile(r"解除(?:质押)?(?:登记)?日|解押日|解除日|购回日|"
                            r"\d{4}\s*(?:年|[-/.])\s*\d{1,2}\s*(?:月|[-/.])?\s*\d{1,2}\s*日?")),
)

QUOTES = re.compile(r"[「『«]([^」』»]*)[」』»]")
ANCHOR_SPLIT = re.compile(r"锚[:：]")
ANCHOR_VAL = re.compile(r"锚[:：]\s*(\S.*)$")
DECL = re.compile(r"共\s*(\d+)\s*笔\s*质押变动\s*[·：:|｜、]\s*未取到\s*(\d+)\s*笔")
EMPTY_LIE = re.compile(r"(?:^|[\s：:])无(?:此项|该笔)|不适用|无需披露|无须披露|不涉及质押")
CORE_STRIP = re.compile(r"[\s　「」『』«»“”（）()《》【】，,。.；;：:、！!？~\-—_·/％%*#]+")
SECTIONS = (("头部申报", r"头部申报"), ("本次变动明细", r"本次变动明细|变动明细|质押明细"),
            ("累计与剩余", r"累计与剩余|累计质押|累计与余额"),
            ("未取到清单", r"未取到清单|缺数清单"), ("待人工", r"待人工"))
DETAIL_HEAD = re.compile(r"^#{1,4}\s*(?:[一二三四五六七八九十\d]+\s*[、.．]\s*)?(?:本次变动明细|变动明细|质押明细)")
CUM_HEAD = re.compile(r"^#{1,4}\s*(?:[一二三四五六七八九十\d]+\s*[、.．]\s*)?(?:累计与剩余|累计质押|累计与余额)")
ANY_HEAD = re.compile(r"^#{1,4}\s")

# 变动明细的项行：`- 质押：…` / `- 解押：…`。
KIND_ITEM = re.compile(r"^\s*[-*]\s*(质押|解押)[：:]")
# 累计与剩余的行：`- <出质人>：前值 → 后值`。变化必须两处。
ARROW = re.compile(r"→|->|—>|⇒")
NUM = re.compile(r"\d[\d,，.]*")
# 比例：百分比。本域只认百分比形。
PCT = re.compile(r"\d+(?:\.\d+)?\s*[%％]")
MISSING = re.compile(r"未取到|未检索到")

# 股东回报速读的项行：出现即说明写错了件（SP-BOUND）。
FOREIGN_ITEMS = re.compile(r"^\s*[-*]\s*(?:分红方案与每股派息|分红总额与分红率|股权登记日与除权除息日|"
                           r"回购方案与回购规模|回购价格区间与资金来源|回购用途与注销安排|"
                           r"减持计划与减持主体)[：:]")
# 单份公告速读的单选行：出现即说明写错了件（SP-BOUND）。
EVENT_PICK = re.compile(r"事件类型\s*[：:]")

# ── 红线词族（SP-LINE ①）────────────────────────────────────────────────
NOUN_FORM = r"(?![性度论])"
VALUER_WORDS = "|".join(w + NOUN_FORM for w in (
    "合理", "偏高", "偏低", "过高", "充分", "不足", "安全", "稳健", "可控", "划算"))
DEGREE_WORDS = r"很|较为|比较|基本|大体|显然|明显|相当"
RISK_ASSERT = (r"有(?:平仓|爆仓)风险|面临(?:平仓|爆仓)|(?:平仓|爆仓)风险|触及(?:预警线|平仓线)|"
               r"跌破(?:预警线|平仓线)|(?:预警线|平仓线)(?:已|将)?(?:被)?(?:触及|跌破)|"
               r"风险(?:可控|不大|较小|很高|很大|极高)|质押(?:很|较为|比较)?安全")
RATING_ASSERT = (r"目标价|评级|买入评级|增持评级|强烈推荐|建议买入|建议卖出|建议增持|建议减持|建议持有")
PRICE_ASSERT = (r"股价(?:将|会|必|有望|可能)|利空|利好|压制股价|提振股价|拖累股价|股价承压")
PROMISE_ASSERT = r"稳赚|零风险|保证收益|必涨|必跌|包赚|无风险套利"
AGENT_ASSERT = r"代拟|代算|代申报|代客|代办申报"
PCT_VALUER = (r"(?:质押比例|质押率|累计质押比例|占总股本比例|占所持比例)(?:的)?(?:" +
              DEGREE_WORDS + r")?(?:" + VALUER_WORDS + r")")
BANNED = re.compile(RISK_ASSERT + r"|" + RATING_ASSERT + r"|" + PRICE_ASSERT + r"|" +
                    PROMISE_ASSERT + r"|" + AGENT_ASSERT + r"|" + PCT_VALUER)
SUBJECT = re.compile(r"质押|解押|出质|质权|平仓|预警线|平仓线|履约保障|累计质押|质押比例|占总股本|占所持")
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

def core_len(s: str) -> int:
    return len(CORE_STRIP.sub("", s or ""))


def parse_kind_line(line: str):
    """`- 质押：正文` → (类别, 正文)；不是变动行返回 (None, None)。"""
    m = KIND_ITEM.match(line)
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
    """SP-LINE 的判据域：剥掉锚**值**，剥掉**纯引注**的书名号；非纯引注的留在域内照扫。

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

    # ── SP-STRUCT ──
    heads = "\n".join(ln for ln in lines if ANY_HEAD.match(ln))
    for label, rx in SECTIONS:
        if not re.search(rx, heads):
            findings.append(("SP-STRUCT", 0, "缺段：" + label))

    det_zone = zone_of(lines, DETAIL_HEAD)
    if det_zone is None:
        findings.append(("SP-STRUCT", 0, "缺「本次变动明细」段，质押/解押行无处占行"))
        det_zone = (0, 0)
    det_seen = []
    for i in range(det_zone[0], det_zone[1]):
        kind, body = parse_kind_line(lines[i])
        if kind is None:
            continue
        det_seen.append((kind, i, body))
        cells = PLEDGE_CELLS if kind == "质押" else RELEASE_CELLS
        if MISSING.search(body):
            continue
        q = quote_field(body)
        for cell_name, rx in cells:
            if not rx.search(q):
                findings.append(("SP-STRUCT", i + 1, kind + "行缺要素：" + cell_name))
    if not det_seen:
        findings.append(("SP-STRUCT", 0, "本次变动明细段内无质押/解押行"))

    # 累计与剩余：每行须是两处之间的差（前值 → 后值）。只有一处不构成变化。
    cum_zone = zone_of(lines, CUM_HEAD)
    if cum_zone is None:
        findings.append(("SP-STRUCT", 0, "缺「累计与剩余」段，余额变化无处登记"))
        cum_zone = (0, 0)
    cum_rows = 0
    for i in range(cum_zone[0], cum_zone[1]):
        ln = lines[i]
        if not re.match(r"^\s*[-*]\s*\S", ln):
            continue
        cum_rows += 1
        if MISSING.search(ln):
            continue
        if not ARROW.search(ln):
            findings.append(("SP-STRUCT", i + 1, "累计与剩余行不是「前值 → 后值」两处之差"))
            continue
        left, right = ARROW.split(ln, maxsplit=1)
        if not NUM.search(left) or not NUM.search(right):
            findings.append(("SP-STRUCT", i + 1, "累计与剩余行两侧须各有数字（前值 → 后值）"))
    if cum_rows == 0:
        findings.append(("SP-STRUCT", 0, "累计与剩余段内无行"))

    # ── SP-QUOTE ──
    for kind, i, body in det_seen:
        qs = QUOTES.findall(body)
        if not qs:
            if not MISSING.search(body):
                findings.append(("SP-QUOTE", i + 1, kind + "行：无书名号原句"))
            continue
        for q in qs:
            if core_len(q) <= 1:
                findings.append(("SP-QUOTE", i + 1, kind + "行：书名号内原句为空或只剩单字"))
        m = ANCHOR_VAL.search(body)
        if not m:
            findings.append(("SP-QUOTE", i + 1, kind + "行：缺「锚：」"))
        elif not m.group(1).strip():
            findings.append(("SP-QUOTE", i + 1, kind + "行：锚值为空"))

    # ── SP-LINE ──
    for i, ln in enumerate(lines):
        if not ln.strip():
            continue
        kind, body = parse_kind_line(ln)
        dom = own_field(body) if body is not None else ln
        for cl in CLAUSE.split(dom):
            if PENDING.search(cl) or DISCLAIM.search(cl):
                continue
            tone_dom = NOUN_WASH.sub("", cl)
            for m in BANNED.finditer(cl):
                findings.append(("SP-LINE", i + 1, "定式禁词：" + m.group(0)))
            if body is not None and SUBJECT.search(cl) and TONE.search(tone_dom):
                findings.append(("SP-LINE", i + 1, "主题词×判断语气同段：" + cl.strip()[:40]))
            if VERDICT.search(cl) and EFFECT.search(cl):
                findings.append(("SP-LINE", i + 1, "自裁效力层：" + cl.strip()[:40]))

    # ── SP-GAP ──
    decls = []
    for i, ln in enumerate(lines):
        for m in DECL.finditer(ln):
            decls.append((i + 1, int(m.group(1)), int(m.group(2))))
    if len(decls) != 1:
        findings.append(("SP-GAP", 0, "未取到申报须恰一枚，实有 %d 枚" % len(decls)))
    missing = sum(1 for _k, _i, b in det_seen if MISSING.search(b))
    if len(decls) == 1:
        if decls[0][1] != len(det_seen):
            findings.append(("SP-GAP", decls[0][0],
                             "申报共 %d 笔质押变动，变动明细段实有 %d 行（两向都发）"
                             % (decls[0][1], len(det_seen))))
        if decls[0][2] != missing:
            findings.append(("SP-GAP", decls[0][0],
                             "申报未取到 %d 笔，变动明细段实有「未取到」%d 行（两向都发）"
                             % (decls[0][2], missing)))
    for i, ln in enumerate(lines):
        if EMPTY_LIE.search(ln):
            findings.append(("SP-GAP", i + 1, "把「未取到」写成「无此项／不适用／无需披露」"))

    # 比例数字必须在该行自己的书名号原句里出现——公告没写就不能自己拿股数除。
    for kind, i, body in det_seen:
        if MISSING.search(body):
            continue
        q = quote_field(body)
        for m in PCT.finditer(body):
            if m.group(0) not in q:
                findings.append(("SP-GAP", i + 1,
                                 kind + "行：比例 %s 不在本行原句里（自算比例）" % m.group(0)))

    # ── SP-BOUND ──
    for i, ln in enumerate(lines):
        if FOREIGN_ITEMS.match(ln):
            findings.append(("SP-BOUND", i + 1,
                             "出现股东回报速读的项行，本件不登记分红回购减持——改走 cn-shareholder-return"))
        if EVENT_PICK.search(ln):
            findings.append(("SP-BOUND", i + 1,
                             "出现单份公告速读的单选行，本件做跨期质押跟踪——改走 event-brief-cn"))

    stats = {"det": len(det_seen), "missing": missing, "decls": len(decls), "cum": cum_rows}
    return findings, stats


# ── 临时件与自测 ────────────────────────────────────────────────────────

def make_tmp(suffix: str = ".md") -> pathlib.Path:
    root = pathlib.Path(tempfile.mkdtemp(prefix="pledge.", dir=os.environ.get("TMPDIR") or None))
    TMP_ROOTS.append(root)
    return root / ("case" + suffix)


def _cleanup():
    for r in TMP_ROOTS:
        shutil.rmtree(r, ignore_errors=True)
    TMP_ROOTS.clear()


GOOD = """# 股权质押与解押跟踪（样例·好样）

## 一、头部申报
- 文件：示例股份有限公司 关于控股股东股份质押的公告｜来路：官方原文｜附件腿：未发起
- 共 4 笔质押变动·未取到 1 笔

## 二、本次变动明细
- 质押：「出质人示例控股集团有限公司，质权人中国工商银行股份有限公司，本次质押股份数量 1,200 万股，占其所持公司股份的 8.00%，占公司总股本的 2.40%，质押期限自 2026 年 6 月 12 日至 2027 年 6 月 11 日」 锚：公告 二、本次质押情况
- 质押：「出质人示例控股集团有限公司，质权人中国建设银行股份有限公司，本次质押股份数量 800 万股，占其所持公司股份的 5.33%，占公司总股本的 1.60%，质押期限自 2026 年 7 月 3 日至 2027 年 7 月 2 日」 锚：公告 二、本次质押情况
- 解押：「出质人示例控股集团有限公司，本次解除质押股份数量 500 万股，解除质押登记日为 2026 年 8 月 20 日」 锚：公告 三、本次解除质押情况
- 质押：未取到（未取到清单已点名）

## 三、累计与剩余
- 示例控股集团有限公司：累计质押 4,500 万股 → 累计质押 6,000 万股
- 示例控股集团有限公司：占其所持股份 30.00% → 占其所持股份 40.00%
- 示例控股集团有限公司：占公司总股本 9.00% → 占公司总股本 12.00%

## 四、未取到清单
- 未取到 1 笔：第三笔质押的质权人与质押期间——本次取得的公告未列该笔明细，需回完整公告核对。

## 五、待人工
- [待人工] 质押比例是否偏高、是否存在平仓风险、对股价的影响，全部留人工；本件不接代办，也不给风险判断。
"""

BAD_STRUCT = GOOD.replace("## 四、未取到清单", "## 四、缺项清单").replace(
    "- 示例控股集团有限公司：累计质押 4,500 万股 → 累计质押 6,000 万股",
    "- 示例控股集团有限公司：累计质押 6,000 万股")
BAD_QUOTE = GOOD.replace(
    "- 解押：「出质人示例控股集团有限公司，本次解除质押股份数量 500 万股，解除质押登记日为 2026 年 8 月 20 日」 锚：公告 三、本次解除质押情况",
    "- 解押：「」 锚：")
BAD_LINE = GOOD.replace(
    "- [待人工] 质押比例是否偏高、是否存在平仓风险、对股价的影响，全部留人工；本件不接代办，也不给风险判断。",
    "- [待人工] 质押比例留人工；该股质押比例偏高，存在平仓风险，目标价 15 元，稳赚。")
BAD_GAP = GOOD.replace("- 共 4 笔质押变动·未取到 1 笔", "- 共 4 笔质押变动·未取到 0 笔")
# 自算比例：公告原句只写股数不写比例，卡面自己拿股数除出 8.00%——那个数字在本行原句里找不到。
# 这是本域最要紧的一格：比例是**公告说的**，不是**卡面算的**。
BAD_PCT = GOOD.replace(
    "- 质押：「出质人示例控股集团有限公司，质权人中国工商银行股份有限公司，本次质押股份数量 1,200 万股，占其所持公司股份的 8.00%，占公司总股本的 2.40%，质押期限自 2026 年 6 月 12 日至 2027 年 6 月 11 日」 锚：公告 二、本次质押情况",
    "- 质押：「出质人示例控股集团有限公司，质权人中国工商银行股份有限公司，本次质押股份数量 1,200 万股，质押期限自 2026 年 6 月 12 日至 2027 年 6 月 11 日」 占其所持公司股份的 8.00%，占公司总股本的 2.40% 锚：公告 二、本次质押情况")
BAD_BOUND = GOOD.replace(
    "- 质押：「出质人示例控股集团有限公司，质权人中国工商银行股份有限公司，本次质押股份数量 1,200 万股，占其所持公司股份的 8.00%，占公司总股本的 2.40%，质押期限自 2026 年 6 月 12 日至 2027 年 6 月 11 日」 锚：公告 二、本次质押情况",
    "- 分红方案与每股派息：「每 10 股派发现金红利 3.50 元（含税）」 锚：公告 一")
# 边界第二支：写成了单份公告速读的单选行（不是股东回报速读那一支）。
BAD_EVENT = GOOD.replace("- 质押：未取到（未取到清单已点名）", "- 事件类型：股份质押公告").replace(
    "- 共 4 笔质押变动·未取到 1 笔", "- 共 3 笔质押变动·未取到 0 笔")


def selftest() -> int:
    bad = 0
    f, _ = check_text(GOOD)
    if f:
        bad += 1
        print("✗ 好样不该发红：", f[:3])
    else:
        print("✓ 好样全过")
    cases = (("SP-STRUCT", BAD_STRUCT), ("SP-QUOTE", BAD_QUOTE), ("SP-LINE", BAD_LINE),
             ("SP-GAP", BAD_GAP), ("SP-GAP", BAD_PCT), ("SP-BOUND", BAD_BOUND),
             ("SP-BOUND", BAD_EVENT))
    for want, txt in cases:
        f, _ = check_text(txt)
        codes = sorted({c for c, _i, _m in f})
        if want in codes:
            print("✓ 坏样发红 %s（共 %d 条）" % (want, len(f)))
        else:
            bad += 1
            print("✗ 坏样未发 %s，实发 %s" % (want, codes))
    f, _ = check_text(GOOD)
    if any(c == "SP-LINE" for c, _i, _m in f):
        bad += 1
        print("✗ 对照样误伤 SP-LINE")
    else:
        print("✓ 对照样不误伤")
    _cleanup()
    print("自测：%s" % ("全合" if bad == 0 else "不合 %d 档" % bad))
    return 0 if bad == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="股权质押与解押跟踪机检（零网络）")
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
        print("不合 %d 条｜变动 %d 笔｜未取到 %d 笔｜申报 %d 枚｜累计行 %d"
              % (len(findings), stats["det"], stats["missing"], stats["decls"], stats["cum"]))
        return 1
    print("PASS｜变动 %d 笔｜未取到 %d 笔｜申报 %d 枚｜累计行 %d"
          % (stats["det"], stats["missing"], stats["decls"], stats["cum"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
