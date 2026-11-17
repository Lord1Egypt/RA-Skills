#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_control_change.py — 实控人变更与要约收购卡的机检（零网络、只读传入文件）。

五道码（缺一即不叫过闸）：
  CC-STRUCT 形制：六段齐（头部申报／变更要素明细／要约收购专段／未取到清单／待人工／来源索引）；
             变更要素明细段**八项行级在场**（`- 变更方式：` 等八枚固定项名，只在散文里提到不算）；
             头部「共 N 项要素·未取到 M 项」只准一处，且 N、M 分别等于明细段行数与「未取到」行数
             （**两向**：多报虚报、少报漏报，两向都发）；
  CC-QUOTE  原句与锚：每项行的书名号（「」『』«»）内原句不得为空或只剩单字；「锚：」须在场且锚值非空；
             每项行须挂来源编号 `[S#]`，且该编号须在「来源索引」段里有对应行（索引行须带 URL 与检索日）；
  CC-CALC   **不得自算**（本域最要紧的一格，与「比例不得自算」同族）：
             ①**变动比例的百分比必须在该行自己的书名号原句里出现**——公告只写股数不写比例时，
             卡面若拿变动股数除以总股本自己算，那个百分比在原句里找不到 ⇒ 发「自算比例」；分母可能是
             总股本、可能是剔除回购专户后的股本、可能是表决权口径，算错一个分母，控制权读数就全错；
             ②**交易对价金额必须在该行自己的书名号原句里出现**——公告常写「转让价格以协议为准」
             「另行约定」，拿变动股数乘每股价格自己算总价 ⇒ 发「自算对价」；
             ③要约收购专段：**要约价与溢价率必须分列两行**（同一行写「要约价 12.00 元，溢价率 21.4%」
              ⇒ 发）；溢价率的百分比必须在该行原句里出现，且该行原句须同时出现基准口径
             （前 30 日均价／前 1 日均价／停牌前 价 等）——披露没写基准就不许自己减，两处缺任一即发；
  CC-LINE   红线三道：①定式禁词——利空利好判断（利好·利空·重大利好·中性偏多·提振股价·压制股价）、
             推断后续动作（后续将·预计将·或将·意在·旨在·计划注入·借壳）、股价预测（股价将·股价会·
             有望上涨·看多·看空）、评级目标价（目标价·评级·买入评级·增持评级·强烈推荐·建议买入·建议卖出）、
             收益承诺（稳赚·必涨·必跌·零风险·包赚）；
             ②主题词×判断语气同段（主题词＝控股权·控制权·实控人·实际控制人·要约·转让·受让·表决权·
             变动比例·交易对价·溢价率，语气＝将·会·必·有望·可期·可能·足以·构成·意味着·属于·显然·
             无疑·肯定·利好·利空·支持·支撑）；
             ③自裁效力层（裁定前缀 结论／综上／因此／本件认为／判定／认定 与 效力判断 有效／无效／
             成立／不成立／违法／违规／合规／属实／构成控制权变更 同现即发）。
             `[待人工]` 标记与免责句都**只登记自己那一分句**（按分号·句号·逗号 cut 后逐段判）。
             判据域：先剥掉书名号内引文（原文不是本件的话）与「锚：」之后的分句，再在剩下的字上判；
  CC-BOUND  边界：本件只做「控制权怎么变」。卡面若出现 `- 分红方案与每股派息：`／`- 回购方案与回购规模：`／
             `- 减持计划与减持主体：` 这类**股东回报速读**的项行 ⇒ 点名改走 `cn-shareholder-return`；
             出现 `- 重组阶段：`／`- 停牌与复牌进度：` 这类**重组进度**的项行 ⇒ 点名改走 `cn-restructuring-tracker`；
             出现 `- 质押明细：`／`- 累计质押：` 这类**质押明细**的项行 ⇒ 点名改走 `cn-share-pledge-tracker`。

用法：
  python3 -B scripts/check_control_change.py <待检文件>      # 逐条发红，全过则 PASS
  python3 -B scripts/check_control_change.py --selftest      # 好样须过、坏样五枚各发其码
  python3 -B scripts/check_control_change.py --help
退码：0＝过（或自测全合）；1＝发红／自测不合；2＝用法错；3＝读不到文件或空稿（不可判，不作「0 违例」读）。
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

# 八项要素：项名即契约名。变更前后拆两格（常常是两个人名，合成一格读不出前后）。
ITEMS = (
    "变更方式", "出让方", "受让方", "变动股数", "变动比例",
    "交易对价", "变更前控制权归属", "变更后控制权归属",
)
ITEM_SET = set(ITEMS)
# 八项里哪几项带「钱数/比例」，要判「必须在本行原句里」（CC-CALC）。
PCT_ITEMS = {"变动比例"}
MONEY_ITEMS = {"交易对价"}

SECTIONS = (
    ("头部申报", r"头部申报"),
    ("变更要素明细", r"变更要素明细|要素明细|变更明细"),
    ("要约收购专段", r"要约收购专段|要约收购|要约专段"),
    ("未取到清单", r"未取到清单|缺数清单"),
    ("待人工", r"待人工"),
    ("来源索引", r"来源索引|来源清单"),
)
ANY_HEAD = re.compile(r"^#{1,4}\s")
ITEM_LINE = re.compile(r"^\s*[-*]\s*(" + "|".join(ITEMS) + r")[：:]")
QUOTES = re.compile(r"[「『«]([^」』»]*)[」』»]")
ANCHOR_SPLIT = re.compile(r"锚[:：]")
ANCHOR_VAL = re.compile(r"锚[:：]\s*(\S.*)$")
CORE_STRIP = re.compile(r"[\s　「」『』«»“”（）()《》【】，,。.；;：:、！!？~\-—_·/％%*#]+")
DECL = re.compile(r"共\s*(\d+)\s*项\s*要素\s*[·：:|｜ 、]+\s*未取到\s*(\d+)\s*项")
MISSING = re.compile(r"未取到|未检索到")
EMPTY_LIE = re.compile(r"(?:^|[\s：:])无(?:此项|该项)|不适用|无需披露|无须披露|不涉及变更")
SREF = re.compile(r"\[S(\d+)\]")
SREF_HEAD = re.compile(r"^\s*[-*]\s*\[(S\d+)\]")
URL = re.compile(r"https?://\S+")
DATE = re.compile(r"\d{4}\s*-\s*\d{2}\s*-\d{2}|\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日")
PCT = re.compile(r"\d+(?:\.\d+)?\s*[%％]")
MONEY = re.compile(r"\d[\d,，.]*\s*(?:万元|亿元|元|万|亿)")
OFFER_PRICE = re.compile(r"要约价")
OFFER_PREM = re.compile(r"溢价率")
BASIS = re.compile(r"前\s*(?:30|二十|30个|三十)\s*(?:个)?交易日|前\s*(?:1|一)\s*(?:个)?交易日|"
                   r"停牌前(?:一交易日)?|基准价|均价|收盘价")

# ── 红线词族（CC-LINE ①）──────────────────────────────────────────────
DIRECTION = r"重大利好|重大利空|利好|利空|中性偏多|提振股价|压制股价|拖累股价"
FOLLOWUP = r"后续将|预计将|或将|意在|旨在|计划注入|拟注入|借壳|后续注入"
PRICE = r"股价(?:将|会|必|有望|可能)|有望上涨|有望下跌|看多|看空|大幅上涨|大幅下跌"
RATING = r"目标价|买入评级|增持评级|强烈推荐|建议买入|建议卖出|建议增持|建议减持"
PROMISE = r"稳赚|必涨|必跌|零风险|包赚|保证收益|无风险套利"
BANNED = re.compile(DIRECTION + r"|" + FOLLOWUP + r"|" + PRICE + r"|" + RATING + r"|" + PROMISE)
SUBJECT = re.compile(r"控股权|控制权|实控人|实际控制人|要约|转让|受让|表决权|变动比例|交易对价|溢价率")
TONE = re.compile(r"将|会|必|有望|可期|可能|足以|构成|意味着|属于|显然|无疑|肯定|利好|利空|支持|支撑")
VERDICT = re.compile(r"结论|综上|因此|可见|据此|本件认为|本卡认为|本件判断|判定|认定|断言")
EFFECT = re.compile(r"无效|有效|作废|不成立|成立|违法|违规|合规|属实|构成控制权变更")
DISCLAIM = re.compile(r"不接|不出|不提供|不作|不判|不碰|不做|不代|禁止|未证|无法|不承诺|不给|留人工")
PENDING = re.compile(r"\[待人工\]")
CLAUSE = re.compile(r"[；;。，,]")

# 股东回报速读 / 重组进度 / 质押明细的项行：出现即说明写错了件（CC-BOUND）。
FOREIGN_RETURN = re.compile(r"^\s*[-*]\s*(?:分红方案与每股派息|分红总额与分红率|股权登记日与除权除息日|"
                            r"回购方案与回购规模|回购价格区间与资金来源|减持计划与减持主体)[：:]")
FOREIGN_RESTR = re.compile(r"^\s*[-*]\s*(?:重组阶段|停牌与复牌进度|预案与过会进度|审核与注册进度)[：:]")
FOREIGN_PLEDGE = re.compile(r"^\s*[-*]\s*(?:质押明细|累计质押|解押明细|质押比例明细)[：:]")


# ── 基础工具 ────────────────────────────────────────────────────────────

def core_len(s: str) -> int:
    return len(CORE_STRIP.sub("", s or ""))


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


def parse_item(line: str):
    """`- 变动比例：正文` → (项名, 正文)；不是要素行返回 (None, None)。"""
    m = ITEM_LINE.match(line)
    if not m:
        return None, None
    return m.group(1), line[m.end():]


def quote_field(body: str) -> str:
    return " ".join(QUOTES.findall(body))


def own_field(body: str) -> str:
    """CC-LINE 的判据域：剥掉书名号内引文与「锚：」之后的分句；锚后分句照扫。"""
    parts = ANCHOR_SPLIT.split(body)
    head = parts[0]
    for tail in parts[1:]:
        pieces = CLAUSE.split(tail, maxsplit=1)
        if len(pieces) > 1:
            head += " " + pieces[1]
    out, pos = [], 0
    for m in QUOTES.finditer(head):
        out.append(head[pos:m.start()])
        pos = m.end()
    out.append(head[pos:])
    return " ".join(out)


# ── 五道码 ──────────────────────────────────────────────────────────────

def check_text(text: str):
    """返回 (findings, stats)。findings = [(码, 行号, 说明)]。"""
    findings = []
    lines = text.splitlines()

    # ── CC-STRUCT ──
    zones = {}
    for label, rx in SECTIONS:
        # 段头只认 `##`～`####`：`#` 是件名行（「实控人变更与要约收购卡」也含「要约收购」四个字），
        # 收进来会把件名当段头、整段判成空段。这条是实测踩出来的，不是洁癖。
        z = zone_of(lines, re.compile(r"^#{2,4}\s*.*(?:" + rx + r")"))
        if z is None:
            findings.append(("CC-STRUCT", 0, "缺段：" + label))
        else:
            zones[label] = z

    det = zones.get("变更要素明细")
    seen_rows = []
    if det is None:
        findings.append(("CC-STRUCT", 0, "缺「变更要素明细」段，八项要素无处占行"))
        det = (0, 0)
    for i in range(det[0], det[1]):
        name, body = parse_item(lines[i])
        if name is None:
            continue
        seen_rows.append((name, i, body))
    present = {n for n, _i, _b in seen_rows}
    for name in ITEMS:
        if name not in present:
            findings.append(("CC-STRUCT", 0, "要素明细缺项：" + name))
    seen_names = [n for n, _i, _b in seen_rows]
    for name in ITEMS:
        if seen_names.count(name) > 1:
            findings.append(("CC-STRUCT", 0, "要素行重复占行：" + name))

    # 头部申报：只准一处，N／M 两向对齐。
    decls = []
    hz = zones.get("头部申报")
    if hz is not None:
        for i in range(hz[0], hz[1]):
            for m in DECL.finditer(lines[i]):
                decls.append((i + 1, int(m.group(1)), int(m.group(2))))
    else:
        findings.append(("CC-STRUCT", 0, "缺「头部申报」段，申报数无处登记"))
    if len(decls) != 1:
        findings.append(("CC-STRUCT", 0, "「共 N 项要素·未取到 M 项」须恰一处，实有 %d 处" % len(decls)))
    else:
        lineno, n, m = decls[0]
        if n != len(seen_rows):
            findings.append(("CC-STRUCT", lineno,
                             "申报共 %d 项要素，明细段实有 %d 行（两向都发）" % (n, len(seen_rows))))
        miss = sum(1 for _n, _i, b in seen_rows if MISSING.search(b))
        if m != miss:
            findings.append(("CC-STRUCT", lineno,
                             "申报未取到 %d 项，明细段实有「未取到」%d 行（两向都发）" % (m, miss)))

    # ── CC-QUOTE ──
    src_idx = {}
    sz = zones.get("来源索引")
    if sz is not None:
        for i in range(sz[0], sz[1]):
            m = SREF_HEAD.match(lines[i])
            if not m:
                continue
            tag = m.group(1)
            if tag in src_idx:
                findings.append(("CC-QUOTE", i + 1, "来源编号重复登记：" + tag))
            src_idx[tag] = i + 1
            row = lines[i]
            if not URL.search(row):
                findings.append(("CC-QUOTE", i + 1, "来源索引行缺 URL：" + tag))
            if not DATE.search(row):
                findings.append(("CC-QUOTE", i + 1, "来源索引行缺检索日：" + tag))
    for name, i, body in seen_rows:
        if MISSING.search(body):
            continue
        qs = QUOTES.findall(body)
        if not qs:
            findings.append(("CC-QUOTE", i + 1, name + "行：无书名号原句"))
        else:
            for q in qs:
                if core_len(q) <= 1:
                    findings.append(("CC-QUOTE", i + 1, name + "行：书名号内原句为空或只剩单字"))
        m = ANCHOR_VAL.search(body)
        if not m:
            findings.append(("CC-QUOTE", i + 1, name + "行：缺「锚：」"))
        elif not SREF.sub("", m.group(1)).strip():
            # 锚值判的是「定位词在不在」：`锚：  [S1]` 只有来源编号、没有定位（节/页/段），视同锚值为空。
            findings.append(("CC-QUOTE", i + 1, name + "行：锚值为空（只剩来源编号，缺定位）"))
        refs = SREF.findall(body)
        if not refs:
            findings.append(("CC-QUOTE", i + 1, name + "行：缺来源编号 [S#]"))
        elif sz is not None:
            for r in refs:
                if "S" + r not in src_idx:
                    findings.append(("CC-QUOTE", i + 1,
                                     name + "行：来源编号 [S%s] 在来源索引里找不到" % r))

    # ── CC-CALC ──
    # ① 比例、② 对价：数字必须在本行自己的书名号原句里。
    for name, i, body in seen_rows:
        if MISSING.search(body):
            continue
        q = quote_field(body)
        if name in PCT_ITEMS:
            for mm in PCT.finditer(body):
                if mm.group(0) not in q:
                    findings.append(("CC-CALC", i + 1,
                                     name + "行：比例 %s 不在本行原句里（自算比例）" % mm.group(0)))
        if name in MONEY_ITEMS:
            for mm in MONEY.finditer(body):
                if mm.group(0) not in q:
                    findings.append(("CC-CALC", i + 1,
                                     name + "行：金额 %s 不在本行原句里（自算对价）" % mm.group(0)))
    # ③ 要约专段：要约价与溢价率分列两行；溢价率百分比在原句里，且原句带基准口径。
    oz = zones.get("要约收购专段")
    if oz is not None:
        rows = [(i + 1, lines[i]) for i in range(oz[0], oz[1])
                if re.match(r"^\s*[-*]\s*\S", lines[i])]
        not_offering = any("不涉及要约收购" in ln for _i, ln in rows)
        if not not_offering:
            price_rows = [(i, ln) for i, ln in rows if OFFER_PRICE.search(ln)]
            prem_rows = [(i, ln) for i, ln in rows if OFFER_PREM.search(ln)]
            for i, ln in rows:
                if OFFER_PRICE.search(ln) and OFFER_PREM.search(ln):
                    findings.append(("CC-CALC", i,
                                     "要约价与溢价率须分列两行，同一行写两样即发"))
            if not prem_rows:
                findings.append(("CC-CALC", 0, "要约收购专段缺「溢价率」行（披露没写就写「未取到」）"))
            for i, ln in prem_rows:
                if MISSING.search(ln):
                    continue
                q = quote_field(ln)
                if not q:
                    findings.append(("CC-CALC", i, "溢价率行：无书名号原句"))
                    continue
                for mm in PCT.finditer(ln):
                    if mm.group(0) not in q:
                        findings.append(("CC-CALC", i,
                                         "溢价率 %s 不在本行原句里（自算溢价率）" % mm.group(0)))
                if DECL.search(q) is None and not BASIS.search(q):
                    findings.append(("CC-CALC", i,
                                     "溢价率行原句未写基准口径（前 30 日均价／前 1 日均价／停牌前价等）"
                                     "——基准不在场就不许自己减"))

    # ── CC-LINE ──
    for i, ln in enumerate(lines):
        if not ln.strip() or ANY_HEAD.match(ln):
            continue
        name, body = parse_item(ln)
        dom = own_field(body) if body is not None else ln
        for cl in CLAUSE.split(dom):
            if PENDING.search(cl) or DISCLAIM.search(cl):
                continue
            for m in BANNED.finditer(cl):
                findings.append(("CC-LINE", i + 1, "定式禁词：" + m.group(0)))
            if SUBJECT.search(cl) and TONE.search(cl):
                findings.append(("CC-LINE", i + 1, "主题词×判断语气同段：" + cl.strip()[:40]))
            if VERDICT.search(cl) and EFFECT.search(cl):
                findings.append(("CC-LINE", i + 1, "自裁效力层：" + cl.strip()[:40]))

    # ── CC-BOUND ──
    for i, ln in enumerate(lines):
        if FOREIGN_RETURN.match(ln):
            findings.append(("CC-BOUND", i + 1,
                             "出现股东回报速读的项行，本件不登记分红回购减持——改走 cn-shareholder-return"))
        elif FOREIGN_RESTR.match(ln):
            findings.append(("CC-BOUND", i + 1,
                             "出现重组进度的项行，本件不登记停牌/预案/过会进度——改走 cn-restructuring-tracker"))
        elif FOREIGN_PLEDGE.match(ln):
            findings.append(("CC-BOUND", i + 1,
                             "出现质押明细的项行，本件不重登质押——改走 cn-share-pledge-tracker"))

    stats = {"rows": len(seen_rows),
             "missing": sum(1 for _n, _i, b in seen_rows if MISSING.search(b)),
             "decls": len(decls), "src": len(src_idx)}
    return findings, stats


# ── 自测样 ──────────────────────────────────────────────────────────────

GOOD = """# 实控人变更与要约收购卡（样例·好样）

## 一、头部申报
- 文件：示例股份有限公司 详式权益变动报告书｜来路：官方原文｜附件腿：已发起
- 共 8 项要素·未取到 1 项

## 二、变更要素明细
- 变更方式：「本次权益变动方式为协议转让」 锚：报告书 第二节 一  [S1]
- 出让方：「出让方示例控股集团有限公司，持有公司股份 180,000,000 股」 锚：报告书 第二节 二  [S1]
- 受让方：「受让方示例产业发展有限公司」 锚：报告书 第二节 二  [S1]
- 变动股数：「本次转让股份数量 120,000,000 股」 锚：报告书 第二节 三  [S1]
- 变动比例：「占公司总股本的 15.00%」 锚：报告书 第二节 三  [S1]
- 交易对价：未取到（未取到清单已点名）
- 变更前控制权归属：「本次权益变动前，公司实际控制人为示例控股集团有限公司」 锚：报告书 第三节 一  [S1]
- 变更后控制权归属：「本次权益变动后，公司实际控制人变更为示例产业发展有限公司」 锚：报告书 第三节 二  [S1]

## 三、要约收购专段
- 本笔不涉及要约收购，无要约价与溢价率。

## 四、未取到清单
- 未取到 1 项：交易对价——报告书写「转让价格由双方另行协商确定」，需回补充协议核对。

## 五、待人工
- [待人工] 对控制权稳定性、新实控人后续动作、股价影响的判断，全部留人工；本件不接代办，也不给方向。

## 六、来源索引
- [S1] 示例股份有限公司详式权益变动报告书｜http://www.cninfo.example/disc/2026-11-09-1｜检索日 2026-11-09
"""

# 形制：明细段少一项（变更后控制权归属被并进变更前那一行）
BAD_STRUCT = GOOD.replace(
    "- 变更后控制权归属：「本次权益变动后，公司实际控制人变更为示例产业发展有限公司」 锚：报告书 第三节 二  [S1]\n",
    "").replace("- 共 8 项要素·未取到 1 项", "- 共 7 项要素·未取到 1 项")
# 原句与锚：原句写成空书名号、锚值也空
BAD_QUOTE = GOOD.replace(
    "- 受让方：「受让方示例产业发展有限公司」 锚：报告书 第二节 二  [S1]",
    "- 受让方：「」 锚：  [S1]")
# 不得自算：公告只写股数不写比例，卡面自己除出 15.00%（百分比在书名号外）
BAD_CALC = GOOD.replace(
    "- 变动比例：「占公司总股本的 15.00%」 锚：报告书 第二节 三  [S1]",
    "- 变动比例：「本次转让股份数量 120,000,000 股」 占公司总股本的 15.00% 锚：报告书 第二节 三  [S1]")
# 红线：同一行后半越出 [待人工] 分句写了利好判断与后续动作
BAD_LINE = GOOD.replace(
    "- [待人工] 对控制权稳定性、新实控人后续动作、股价影响的判断，全部留人工；本件不接代办，也不给方向。",
    "- [待人工] 控制权稳定性留人工；本次变更属重大利好，新实控人后续将注入资产，目标价 20 元。")
# 边界：写成了股东回报速读的项行
# 边界：写成了股东回报速读的项行。**不能拿它替掉八项之一**——那样会连带发 CC-STRUCT（缺项），
# 测的就不是边界而是形制。所以挂到明细段之外（未取到清单里多一行），八项保持完整。
BAD_BOUND = GOOD.replace(
    "- 未取到 1 项：交易对价——报告书写「转让价格由双方另行协商确定」，需回补充协议核对。",
    "- 未取到 1 项：交易对价——报告书写「转让价格由双方另行协商确定」，需回补充协议核对。\n"
    "- 分红方案与每股派息：「每 10 股派发现金红利 3.50 元（含税）」 锚：报告书 第四节  [S1]")


def selftest() -> int:
    bad = 0
    f, _ = check_text(GOOD)
    if f:
        bad += 1
        print("✗ 好样不该发红：", f[:3])
    else:
        print("✓ 好样全过")
    cases = (("CC-STRUCT", BAD_STRUCT), ("CC-QUOTE", BAD_QUOTE), ("CC-CALC", BAD_CALC),
             ("CC-LINE", BAD_LINE), ("CC-BOUND", BAD_BOUND))
    for want, txt in cases:
        f, _ = check_text(txt)
        codes = sorted({c for c, _i, _m in f})
        if codes == [want]:
            print("✓ 坏样只发 %s（共 %d 条）" % (want, len(f)))
        else:
            bad += 1
            print("✗ 坏样应只发 %s，实发 %s" % (want, codes))
    print("自测：%s" % ("全合" if bad == 0 else "不合 %d 档" % bad))
    return 0 if bad == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="实控人变更与要约收购机检（零网络）")
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
        print("不可判：文件不存在 %s（读不到输入，不作「0 违例」读）" % p, file=sys.stderr)
        return 3
    text = p.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        print("不可判：空稿 %s（读不到内容，不作「0 违例」读）" % p, file=sys.stderr)
        return 3
    findings, stats = check_text(text)
    for code, ln, msg in findings:
        print("%s 第%d行 %s" % (code, ln, msg))
    if findings:
        print("不合 %d 条｜要素 %d 项｜未取到 %d 项｜申报 %d 枚｜来源 %d 条"
              % (len(findings), stats["rows"], stats["missing"], stats["decls"], stats["src"]))
        return 1
    print("PASS｜要素 %d 项｜未取到 %d 项｜申报 %d 枚｜来源 %d 条"
          % (stats["rows"], stats["missing"], stats["decls"], stats["src"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
