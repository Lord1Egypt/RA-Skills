#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_morning.py — 晨会纪要（数据槽与覆盖率申报）的机检（零网络、只读传入文件）。

五道码（缺一即不叫过闸）：
  MB-STRUCT 形制：八段齐且五段有序（头部申报／市场综述／标的动态／政策行业／催化剂／风险提示／
             未取到清单／待人工；其中市场综述→标的动态→政策行业→催化剂→风险提示 须按此序）；
             槽表八槽**不重不漏**（隔夜外盘·汇率与商品·利率与流动性·指数与成交·两融余额·
             标的隔夜公告标题·标的今日事件·今日披露与解禁），槽名即契约名，改名即不合；
             每行状态只准 `已填`／`未取到`，层级只准 `市场层`／`标的层`；
  MB-COVER  覆盖率申报：`已填槽/总槽 = N/M（xx%）` 只准出现一处，且**三个数各自都能回到槽表**——
             N＝槽表里 `已填` 的行数，M＝八槽契约数，xx＝N/M 四舍五入（.5 进位）取整；
             任一处对不上即发。**报出来的数必须能回到槽表，不能自己拼**（本域最要紧的一格，
             与「比例不得自算」同族：数不是拍出来的，是数出来的）；
  MB-ANCHOR 锚：槽表每个 `已填` 行的 `值或原句`／`来源`／`检索日` 三格都不许空（`—` 视同空）；
             市场综述／标的动态／催化剂 的每条事实行（非 `[待人工]` 行）须同时有 `锚：` 与检索日；
             判断段（市场综述／政策行业／催化剂／风险提示）各须至少一处 `[待人工]`——缺即发，
             本件一字不代填。`[待人工]` 只豁免它**自己那一分句**，同一行后半照判；
  MB-GAP    未取到两向点名 + 禁「不适用」：`未取到槽：` 只准出现一处，其所列槽名集合必须**等于**
             槽表里 `未取到` 的行集合——多报是虚报，少报是漏报，两个方向都发（零缺口写「无」）；
             把「未取到」写成「无此项／不适用／无需披露」一律发（那是替数据源下结论，不是登记）；
  MB-LINE   红线三道：①定式禁词——涨跌预测（预计上涨·预计下跌·有望上涨·看多·看空·高开·低开·冲高·
             走强·走弱）、买卖建议（建议买入·建议卖出·加仓·减仓·建仓·清仓·推荐买入·逢低吸纳）、
             评级目标价（目标价·评级·买入评级·增持评级·强烈推荐）、收益承诺（稳赚·必涨·必跌·
             零风险·包赚·保证收益）；
             ②主题词×判断语气同段（主题词＝市场·大盘·指数·板块·行业·政策·催化剂·风险·汇率·利率·
             两融·标的，语气＝有望·可期·必然·无疑·显然·意味着·足以·构成·偏强·偏弱·承压·受益·
             利好·利空·应当·应予·可能）——**语气词刻意不收「将／会／必」**：本域大量事实句写
             「将于今日披露」「今日将有 2 只解禁」，把这三个字收进来，事实句会成片假红（有意收窄，不是缺陷）；
             ③越界精读（公告称·公告显示·主要内容为·解读为·意即·实质是·影响为）——本件只到标题级，
             正文精读归 `event-brief-cn`。
             判据域：①②③ 在**剥掉书名号内引文与「锚：」值之后**的行上判（引文是原文、锚值是定位词，
             不是本件自己的话）；`[待人工]` 与免责句按分句各自豁免。

用法：
  python3 -B scripts/check_morning.py <待检文件>      # 逐条发红，全过则 PASS
  python3 -B scripts/check_morning.py --selftest      # 好样须过、坏样五枚各发其码
  python3 -B scripts/check_morning.py --help
退码：0＝过（或自测全合）；1＝发红／自测不合；2＝用法错。
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

# 八槽契约：槽名即契约名。市场层五槽、标的层三槽。
SLOTS = (
    ("隔夜外盘", "市场层"),
    ("汇率与商品", "市场层"),
    ("利率与流动性", "市场层"),
    ("指数与成交", "市场层"),
    ("两融余额", "市场层"),
    ("标的隔夜公告标题", "标的层"),
    ("标的今日事件", "标的层"),
    ("今日披露与解禁", "标的层"),
)
SLOT_NAME = {n for n, _ in SLOTS}
SLOT_LAYER = dict(SLOTS)
LAYERS = {"市场层", "标的层"}
STATUS = {"已填", "未取到"}

# 段：八段齐；五段有序（CORE 按下标递增）。
SECTIONS = (
    ("头部申报", r"头部申报"),
    ("市场综述", r"市场综述|市场回顾|市场层"),
    ("标的动态", r"标的动态|标的层|个股动态"),
    ("政策行业", r"政策行业|政策与行业|政策"),
    ("催化剂", r"催化剂|事件日历"),
    ("风险提示", r"风险提示|风险因素"),
    ("未取到清单", r"未取到清单|缺数清单"),
    ("待人工", r"待人工"),
)
CORE = ("市场综述", "标的动态", "政策行业", "催化剂", "风险提示")
JUDGE_SECTIONS = ("市场综述", "政策行业", "催化剂", "风险提示")
ANCHOR_SECTIONS = ("市场综述", "标的动态", "催化剂")
ANY_HEAD = re.compile(r"^#{1,4}\s")

COVER = re.compile(r"已填槽\s*/\s*总槽\s*=\s*(\d+)\s*/\s*(\d+)\s*"
                   r"(?:（\s*(\d+)\s*%\s*）|\(\s*(\d+)\s*%\s*\))")
COVER_LOOSE = re.compile(r"已填槽\s*/\s*总槽")
GAP = re.compile(r"未取到槽\s*[：:]\s*(.+)")
GAP_NAME = re.compile(r"[、，,；;/／\s]+")
EMPTY_LIE = re.compile(r"无(?:此项|该槽)|不适用|无需披露|无须披露|不作申报")
EMPTY_CELL = re.compile(r"^[—\-－–\s]*$")
ANCHOR_VAL = re.compile(r"锚[:：]\s*(\S.*)$")
DATE = re.compile(r"\d{4}\s*-\s*\d{2}\s*-\s*\d{2}|\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日")
PENDING = re.compile(r"\[待人工\]")
DISCLAIM = re.compile(r"不接|不出|不提供|不作|不判|不碰|不做|不代|禁止|未证|无法|不承诺|不给|留人工")
CLAUSE = re.compile(r"[；;。，,]")
QUOTES = re.compile(r"[「『«]([^」』»]*)[」』»]")
ANCHOR_SPLIT = re.compile(r"锚[:：]")

# ── 红线词族（MB-LINE ①）──────────────────────────────────────────────
DIRECTION = r"预计(?:上涨|下跌|上行|下行)|有望(?:上涨|下跌|上行|下行|走强|走弱)|看多|看空|高开|低开|冲高|走强|走弱|大幅上涨|大幅下跌"
TRADE = r"建议买入|建议卖出|建议增持|建议减持|加仓|减仓|建仓|清仓|推荐买入|逢低吸纳|逢高减持"
RATING = r"目标价|买入评级|增持评级|强烈推荐|(?:给予|维持|上调|下调)[^，。；\n]{0,8}评级"
PROMISE = r"稳赚|必涨|必跌|零风险|包赚|保证收益|无风险套利"
BANNED = re.compile(DIRECTION + r"|" + TRADE + r"|" + RATING + r"|" + PROMISE)
SUBJECT = re.compile(r"市场|大盘|指数|板块|行业|政策|催化剂|风险|汇率|利率|两融|标的")
TONE = re.compile(r"有望|可期|必然|无疑|显然|意味着|足以|构成|偏强|偏弱|承压|受益|利好|利空|应当|应予|可能")
DEEP_READ = re.compile(r"公告称|公告显示|主要内容为|解读为|意即|实质是|影响为|正文显示")


# ── 基础工具 ────────────────────────────────────────────────────────────

def zone_of(lines, head_rx):
    """返回某段的 (起, 止) 行下标；没有该段返回 None。"""
    start = None
    for i, ln in enumerate(lines):
        if head_rx.match(ln):
            start = i + 1
            continue
        if start is not None and ANY_HEAD.match(ln):
            return start, i
    return (start, len(lines)) if start is not None else None


def own_voice(line: str) -> str:
    """判据域：剥掉书名号内引文（原文不是本件的话）与「锚：」到行尾的定位词。"""
    head = ANCHOR_SPLIT.split(line)[0]
    return QUOTES.sub(" ", head)


def round_pct(n: int, m: int) -> int:
    """四舍五入（.5 进位），整数算，不碰浮点。"""
    return (n * 200 + m) // (2 * m) if m else 0


def cells_of(line: str):
    s = line.strip()
    if not s.startswith("|"):
        return None
    return [c.strip() for c in s.strip("|").split("|")]


# ── 五道码 ──────────────────────────────────────────────────────────────

def check_text(text: str):
    findings = []
    lines = text.splitlines()
    heads = [(i, ln) for i, ln in enumerate(lines) if ANY_HEAD.match(ln)]

    # ── MB-STRUCT ──
    zones = {}
    for label, rx in SECTIONS:
        z = zone_of(lines, re.compile(r"^#{1,4}\s*.*(?:" + rx + r")"))
        if z is None:
            findings.append(("MB-STRUCT", 0, "缺段：" + label))
        else:
            zones[label] = z
    idx = []
    for label in CORE:
        hit = next((i for i, ln in heads if re.search(dict(SECTIONS)[label], ln)), None)
        idx.append((label, hit))
    if all(h is not None for _l, h in idx):
        seq = [h for _l, h in idx]
        if seq != sorted(seq):
            findings.append(("MB-STRUCT", 0,
                             "五段次序不合（须 市场综述→标的动态→政策行业→催化剂→风险提示）"))

    # 槽表：在头部申报段内解析。八槽不重不漏。
    rows = []
    hz = zones.get("头部申报")
    if hz is not None:
        for i in range(hz[0], hz[1]):
            cs = cells_of(lines[i])
            if not cs or len(cs) < 7:
                continue
            if cs[1] in ("槽", "") or set(cs[1]) <= set("-: "):
                continue
            if cs[2] not in LAYERS and cs[1] not in SLOT_NAME:
                continue
            rows.append((i + 1, cs))
    seen = {}
    for lineno, cs in rows:
        name, layer, status = cs[1], cs[2], cs[3]
        if name not in SLOT_NAME:
            findings.append(("MB-STRUCT", lineno, "槽表出现契约外槽名：" + name))
            continue
        if name in seen:
            findings.append(("MB-STRUCT", lineno, "槽重复占行：" + name))
        seen[name] = lineno
        if layer not in LAYERS:
            findings.append(("MB-STRUCT", lineno, "槽「%s」层级不是 市场层／标的层：%s" % (name, layer)))
        elif SLOT_LAYER[name] != layer:
            findings.append(("MB-STRUCT", lineno,
                             "槽「%s」应属 %s，槽表写在 %s" % (name, SLOT_LAYER[name], layer)))
        if status not in STATUS:
            findings.append(("MB-STRUCT", lineno,
                             "槽「%s」状态只准 已填／未取到：%s" % (name, status)))
    for name, _layer in SLOTS:
        if name not in seen:
            findings.append(("MB-STRUCT", 0, "槽表缺槽：" + name))

    filled = [cs for _l, cs in rows if cs[3] == "已填"]
    missing = [cs for _l, cs in rows if cs[3] == "未取到"]

    # ── MB-COVER ──
    decls = []
    loose = 0
    for i, ln in enumerate(lines):
        if COVER_LOOSE.search(ln):
            loose += 1
        for m in COVER.finditer(ln):
            pct = m.group(3) or m.group(4)
            decls.append((i + 1, int(m.group(1)), int(m.group(2)),
                          int(pct) if pct is not None else None))
    if len(decls) != 1:
        findings.append(("MB-COVER", 0,
                         "覆盖率申报须恰一处「已填槽/总槽 = N/M（xx%）」，实有 %d 处" % len(decls)))
    else:
        lineno, n, m, pct = decls[0]
        if n != len(filled):
            findings.append(("MB-COVER", lineno,
                             "申报已填 %d 槽，槽表实有「已填」%d 行（两向都发）" % (n, len(filled))))
        if m != len(SLOTS):
            findings.append(("MB-COVER", lineno,
                             "申报总槽 %d，八槽契约数 %d（槽名即契约，不许自己改总数）"
                             % (m, len(SLOTS))))
        if pct is None:
            findings.append(("MB-COVER", lineno, "覆盖率未报百分比：须显式写（xx%）"))
        else:
            want = round_pct(n, m)
            if pct != want:
                findings.append(("MB-COVER", lineno,
                                 "百分比 %d%% 与 %d/%d 不符（应为 %d%%，四舍五入）——数要能回到槽表，不能自己拼"
                                 % (pct, n, m, want)))

    # ── MB-ANCHOR ──
    for lineno, cs in rows:
        if cs[3] != "已填":
            continue
        name = cs[1]
        for col, label in ((4, "值或原句"), (5, "来源"), (6, "检索日")):
            if col >= len(cs) or EMPTY_CELL.match(cs[col]):
                findings.append(("MB-ANCHOR", lineno, "槽「%s」已填但缺%s" % (name, label)))
        if len(cs) > 6 and cs[6] and not EMPTY_CELL.match(cs[6]) and not DATE.search(cs[6]):
            findings.append(("MB-ANCHOR", lineno, "槽「%s」检索日不是日期形：%s" % (name, cs[6])))
    for label in ANCHOR_SECTIONS:
        z = zones.get(label)
        if z is None:
            continue
        for i in range(z[0], z[1]):
            ln = lines[i]
            if not re.match(r"^\s*[-*]\s*\S", ln):
                continue
            if PENDING.search(ln):
                continue
            if not ANCHOR_VAL.search(ln):
                findings.append(("MB-ANCHOR", i + 1, label + "事实行缺「锚：」"))
            elif not DATE.search(ln):
                findings.append(("MB-ANCHOR", i + 1, label + "事实行缺检索日"))
    for label in JUDGE_SECTIONS:
        z = zones.get(label)
        if z is None:
            continue
        if not any(PENDING.search(lines[i]) for i in range(z[0], z[1])):
            findings.append(("MB-ANCHOR", z[0], label + "段缺 [待人工]（判断位一字不代填）"))

    # ── MB-GAP ──
    gdecls = []
    for i, ln in enumerate(lines):
        m = GAP.search(ln)
        if m:
            gdecls.append((i + 1, m.group(1).strip()))
    if len(gdecls) != 1:
        findings.append(("MB-GAP", 0,
                         "「未取到槽：」申报须恰一处（零缺口写「无」），实有 %d 处" % len(gdecls)))
    else:
        lineno, body = gdecls[0]
        declared = set()
        if body.strip().strip("。.") not in ("无", "0", "无缺槽", "无缺口"):
            for tok in GAP_NAME.split(body):
                tok = tok.strip("。（）()·：:。\"'")
                if not tok:
                    continue
                if tok not in SLOT_NAME:
                    findings.append(("MB-GAP", lineno, "申报的缺槽名不在八槽契约内：" + tok))
                    continue
                declared.add(tok)
        marked = {cs[1] for cs in missing}
        over = declared - marked
        under = marked - declared
        if over:
            findings.append(("MB-GAP", lineno, "虚报：申报未取到 %s，槽表标的是「已填」"
                             % "、".join(sorted(over))))
        if under:
            findings.append(("MB-GAP", lineno, "漏报：槽表标了「未取到」而申报未列 %s"
                             % "、".join(sorted(under))))
    for i, ln in enumerate(lines):
        if EMPTY_LIE.search(ln):
            findings.append(("MB-GAP", i + 1, "把「未取到」写成「无此项／不适用／无需披露」"))

    # ── MB-LINE ──
    for i, ln in enumerate(lines):
        if not ln.strip() or ANY_HEAD.match(ln):
            continue
        dom = own_voice(ln)
        for cl in CLAUSE.split(dom):
            if PENDING.search(cl) or DISCLAIM.search(cl):
                continue
            for m in BANNED.finditer(cl):
                findings.append(("MB-LINE", i + 1, "定式禁词：" + m.group(0)))
            if SUBJECT.search(cl) and TONE.search(cl):
                findings.append(("MB-LINE", i + 1, "主题词×判断语气同段：" + cl.strip()[:40]))
        for m in DEEP_READ.finditer(dom):
            findings.append(("MB-LINE", i + 1, "越界精读（本件只到标题级）：" + m.group(0)))

    stats = {"filled": len(filled), "missing": len(missing),
             "decls": len(decls), "gaps": len(gdecls), "slots": len(seen)}
    return findings, stats


# ── 自测样（改一处只改一行：每枚坏样只发它自己那道码）────────────────────

GOOD = """# 晨会纪要·2026-11-09 隔夜

## 一、头部申报与槽表

- 文件：2026-11-09 隔夜｜覆盖标的：2 只｜来路：用户直供
- 已填槽/总槽 = 6/8（75%）
- 未取到槽：利率与流动性、两融余额

| # | 槽 | 层 | 状态 | 值或原句 | 来源 | 检索日 |
|---|---|---|---|---|---|---|
| ① | 隔夜外盘 | 市场层 | 已填 | 道琼斯 -0.42%、纳斯达克 +0.31% | 交易所收盘页 | 2026-11-09 |
| ② | 汇率与商品 | 市场层 | 已填 | 美元兑人民币 7.1180；布伦特 68.40 美元／桶 | 官方中间价与结算页 | 2026-11-09 |
| ③ | 利率与流动性 | 市场层 | 未取到 | — | — | 2026-11-09 |
| ④ | 指数与成交 | 市场层 | 已填 | 上证 3,120.45 -0.35%；两市成交 8,120 亿元 | 交易所行情页 | 2026-11-09 |
| ⑤ | 两融余额 | 市场层 | 未取到 | — | — | 2026-11-09 |
| ⑥ | 标的隔夜公告标题 | 标的层 | 已填 | 「关于以集中竞价交易方式回购股份进展公告」等 3 条 | 披露平台标题列表 | 2026-11-09 |
| ⑦ | 标的今日事件 | 标的层 | 已填 | 2 只标的今日召开股东大会 | 交易所日历 | 2026-11-09 |
| ⑧ | 今日披露与解禁 | 标的层 | 已填 | 1 只标的披露三季报；无解禁 | 交易所日历 | 2026-11-09 |

## 二、市场综述
- 隔夜外盘：「道琼斯 -0.42%、纳斯达克 +0.31%」 锚：交易所收盘页｜检索日 2026-11-09
- 汇率与商品：「美元兑人民币 7.1180」 锚：官方中间价｜检索日 2026-11-09
- [待人工] 隔夜外盘与汇率对今日开盘的强弱，本件不判，一字不代填。

## 三、标的动态
- 示例股份（600001）｜「关于以集中竞价交易方式回购股份进展公告」 锚：披露平台标题列表｜检索日 2026-11-09
- 示例科技（300002）｜「2026 年第三季度报告」 锚：披露平台标题列表｜检索日 2026-11-09

## 四、政策行业
- [待人工] 隔夜政策与行业消息的取向与影响，本件不判。

## 五、催化剂
- 示例股份（600001）｜股东大会 锚：交易所日历｜检索日 2026-11-09
- [待人工] 催化剂能否兑现，本件不判。

## 六、风险提示
- [待人工] 风险大小、是否需回避，本件不判、不给方向。

## 七、未取到清单
- 未取到 2 槽：利率与流动性（缺当日资金价格）、两融余额（缺上一交易日余额），需回官方披露页核对。

## 八、待人工
- [待人工] 涨跌方向、买卖建议、评级目标价，全部留人工。
"""

# 形制：政策行业段标题被改名（段缺即发）。此处不连带 MB-ANCHOR——缺段处不做「缺 [待人工]」判。
BAD_STRUCT = GOOD.replace("## 四、政策行业", "## 四、宏观跟踪")
# 覆盖率：已填 6 行、百分比却写 80%，数回不到槽表。
BAD_COVER = GOOD.replace("- 已填槽/总槽 = 6/8（75%）", "- 已填槽/总槽 = 6/8（80%）")
# 锚：已填槽行缺来源。
BAD_ANCHOR = GOOD.replace(
    "| ① | 隔夜外盘 | 市场层 | 已填 | 道琼斯 -0.42%、纳斯达克 +0.31% | 交易所收盘页 | 2026-11-09 |",
    "| ① | 隔夜外盘 | 市场层 | 已填 | 道琼斯 -0.42%、纳斯达克 +0.31% | — | 2026-11-09 |")
# 缺口：槽表标了 2 槽未取到，申报只列 1 槽（漏报）。
BAD_GAP = GOOD.replace("- 未取到槽：利率与流动性、两融余额", "- 未取到槽：利率与流动性")
# 红线：同一行后半越出 [待人工] 的分句之外写了方向与建议。
BAD_LINE = GOOD.replace(
    "- [待人工] 涨跌方向、买卖建议、评级目标价，全部留人工。",
    "- [待人工] 涨跌方向留人工；今日大盘有望走强，建议买入示例股份，目标价 20 元。")


def selftest() -> int:
    bad = 0
    f, _ = check_text(GOOD)
    if f:
        bad += 1
        print("✗ 好样不该发红：", f[:3])
    else:
        print("✓ 好样全过")
    cases = (("MB-STRUCT", BAD_STRUCT), ("MB-COVER", BAD_COVER), ("MB-ANCHOR", BAD_ANCHOR),
             ("MB-GAP", BAD_GAP), ("MB-LINE", BAD_LINE))
    for want, txt in cases:
        f, _ = check_text(txt)
        codes = sorted({c for c, _i, _m in f})
        if want in codes and codes == [want]:
            print("✓ 坏样只发 %s（共 %d 条）" % (want, len(f)))
        else:
            bad += 1
            print("✗ 坏样应只发 %s，实发 %s" % (want, codes))
    print("自测：%s" % ("全合" if bad == 0 else "不合 %d 档" % bad))
    return 0 if bad == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="晨会纪要机检（零网络）")
    ap.add_argument("path", nargs="?", help="待检 Markdown 文件")
    ap.add_argument("--selftest", action="store_true", help="跑内置好样/坏样自测")
    args = ap.parse_args()
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
        print("不合 %d 条｜已填槽 %d｜未取到槽 %d｜槽 %d｜覆盖率申报 %d｜缺口申报 %d"
              % (len(findings), stats["filled"], stats["missing"], stats["slots"],
                 stats["decls"], stats["gaps"]))
        return 1
    print("PASS｜已填槽 %d｜未取到槽 %d｜槽 %d｜覆盖率申报 %d｜缺口申报 %d"
          % (stats["filled"], stats["missing"], stats["slots"],
             stats["decls"], stats["gaps"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
