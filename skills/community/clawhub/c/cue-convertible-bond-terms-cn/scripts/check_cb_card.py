#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_cb_card.py — 可转债条款卡的机检（零网络、只读本包外传入的文件）。

五道码（缺一即不叫过闸）：
  CB-STRUCT 五段齐：头部申报／八项逐字速读／口径对照／缺数清单／待人工，任一节缺失即发；
            八项名目另须在「逐字速读」段内**行级在场**——每枚名目一行以「- 名目：」起头，只在散文里提到不算占行；
  CB-QUOTE  每项原句与锚：项行的书名号（「」『』«»）内原句不得为空或只剩单字；「锚：」标签在而锚值为空同样发；
  CB-LINE   红线断言三道：①定式禁词转股收益／转股价值／套利空间／一定能转／必被赎回／会被强制赎回／建议申购／
            代客申购／代客转股／稳赚／零风险／保证收益／必涨／目标价／评级上调／评级下调；②判断式规则——把项行拆成
            字段（名目／书名号原句／锚／句体）后，凡非 [待人工]、非「不接／不出／不判」类免责行、非书名号内的公告原句，
            只要「主题词（收益·价值·评级·目标价·赎回·回售·下修·风险·概率·利好）」与「判断语气（应·将·会·必·有望·
            可能·足以·构成·属于·支持·成立·上调·下调…）」同段出现即发，不靠枚举结论短语；
            语气域先洗掉机构名 token（委员会／董事会／监事会／股东大会后缀的「会」是名词后缀不是判断语气），
            所以「赎回价格由董事会拟定」不误红，「回售应予否决」照发；
            ③自裁效力层：裁定前缀（结论／综上／因此／本院认为／判定…）与效力判断（无效／有效／作废／成立／
            撤销…）同现即发；
  CB-COUNT  齐缺申报恰一枚：头部「共八项·缺 N 项」只准出现一处（两处并存即发），且 N 必须等于速读段里
            「未检索到」的项行数；把「未检索到」写成「无该项／没有此项」一律发；
  CB-TRIG   修正、赎回、回售三项按**规则**判、不按词表判：先把项行拆成字段（名目／书名号原句／锚／句体），
            取该项自己的原句作判据域，
            ①先剥日期（YYYY年M月D日／YYYY年／M月D日一律从取数域剔除，日期凑不出触发数）；
            ②剩下的句段必须有一段**同时**给出触发量纲（N%／N 个百分点／N 个交易日／N 个计息年度／N 日／N 天／N 股）
            与触发语境（连续·低于·转股价格·收盘价·计息年度·回售线／赎回线／修正线这类词）——项名自己不算语境，
            ③归属核验（sem 真进判定）：合格段附近（±24 字窗口）必须出现**本项**触发语（修正·下修／赎回·强赎／回售），
            且窗口内不得出现**别项**触发语——完整的下修触发句塞进回售项照样发，三组触发各归各的数；
            「回售价格为面值的 100%」那种价钱不是触发线；
            别项的数、同段无关的数都不顶账；③反向判：剥日期后没有任何合格段、又没写「未检索到」，即发——
            空泛语（满足…条件／按约定执行／详见公告／视股价而定／另行公告／另定／另行约定／尚未明确／待定）
            只决定发红那句话的措辞，有没有数、数在哪一段才决定过不过闸，换同义词换不掉这一判。

用法：
  python3 -B scripts/check_cb_card.py <待检文件>      # 逐条发红，全过则 PASS
  python3 -B scripts/check_cb_card.py --selftest      # 好样须过、坏样五道齐发、钉阈各钉一档且每档整族钉、临时件自清
  python3 -B scripts/check_cb_card.py --help
退码：0＝过（或自测全合）；1＝发红／自测不合；2＝用法错。
"""
from __future__ import annotations

import argparse
import atexit
import pathlib
import re
import shutil
import sys
import tempfile

TMP_ROOTS: list[pathlib.Path] = []

ITEMS = ("发行规模与期限", "票面利率与计息", "转股价格与初始转股价格", "转股期与转股条件",
         "向下修正条款", "有条件赎回条款", "回售条款", "担保与评级")
TRIG_ITEMS = ("向下修正条款", "有条件赎回条款", "回售条款")
TRIG_SEM = {"向下修正条款": r"修正|下修", "有条件赎回条款": r"赎回|强赎", "回售条款": r"回售"}
TRIG_SEM_LABEL = {"向下修正条款": "修正·下修", "有条件赎回条款": "赎回·强赎", "回售条款": "回售"}
TRIG_FOREIGN = {"向下修正条款": r"赎回|强赎|回售", "有条件赎回条款": r"修正|下修|回售", "回售条款": r"修正|下修|赎回|强赎"}
ATTRIB_WINDOW = 24
ITEM = re.compile(r"^\s*[-*]\s*(" + "|".join(map(re.escape, ITEMS)) + r")[：:]")
TITLE = re.compile(r"[「『«][^」』»]+[」』»]")
QUOTES = re.compile(r"[「『«]([^」』»]*)[」』»]")
ANCHOR_SPLIT = re.compile(r"锚[:：]")
ANCHOR_VAL = re.compile(r"锚[:：]\s*(\S.*)$")
BANNED = re.compile(r"转股收益|转股价值|套利空间|一定能转|必被赎回|会被强制赎回|建议申购|代客申购|代客转股|稳赚|零风险|保证收益|必涨|目标价|评级上调|评级下调")
SUBJECT = re.compile(r"收益|价值|评级|目标价|赎回|回售|下修|修正|风险|概率|利好|套利|转股")
TONE = re.compile(r"应当|应予|予以|将|会|必|有望|可期|可能|足以|构成|属于|意味着|支持|成立|推翻|无效|有效|上调|下调|提升|下滑|增加|减少|回升|破发|高于|低于|稳赚|赚|亏|无疑|显然|肯定|应(?!急)")
VERDICT = re.compile(r"结论|综上|因此|可见|据此|本院认为|本件认为|本卡认为|本件判断|判定|认定|断言")
EFFECT = re.compile(r"无效|有效|作废|不成立|成立|撤销|违法|违规|应予支持|予以支持|应支持|支持|必然|属实")
NOUN_WASH = re.compile(r"[员委事大东议工学协商年例常布明谈论聚汇组]会|会[计议场话晤所馆堂员]")   # 「X 会」机构名后缀与「会 X」名词（会计·会议·会场·会员·会话）两头的「会」都是名词性成分，不是判断语气——两头按形态一起洗，不枚举个案
DISCLAIM = re.compile(r"不接|不出|不提供|不作|不判|禁止|未证|无法|不承诺")
PENDING = re.compile(r"\[待人工\]")
DECL = re.compile(r"共\s*(?:八|8)\s*项\s*[·：:|｜、]\s*缺\s*(\d+)\s*项")
EMPTY_LIE = re.compile(r"(?:^|[\s：:])无(?:该项|此项)|没有(?:该项|此项)")
DATE_SPAN = re.compile(r"\d{4}\s*(?:年|[-/.])\s*\d{1,2}\s*(?:月|[-/.])?\s*\d{1,2}\s*日?"
                       r"|\d{4}\s*年(?:\s*\d{1,2}\s*月)?(?:\s*\d{1,2}\s*日)?"
                       r"|\d{1,2}\s*月\s*\d{1,2}\s*日"
                       r"|\d{4}[-/.]\d{1,2}[-/.]\d{1,2}")
SEG_SPLIT = re.compile(r"[，。；、！？；]+|[,!](?!\s*\d)")   # 千分位逗号不断段（8,600 是一枚数）
TRIG_NUM = re.compile(r"\d[\d,\.]*\s*(?:%|个百分点|个交易日|个计息年度|个月|日|天|股)")
TRIG_CTX = re.compile(r"连续|低于|高于|不低于|不高于|转股价格|收盘价|均价|触发|计息年度|期满|届满|回售线|赎回线|修正线|调整幅度")
TRIG_VAGUE = re.compile(r"满足[^，。、；」』]{0,4}条件|按约定执行|按约定|详见公告|视股价而定|另行公告|另行约定|另行确定|另定|尚未明确|尚未披露|未披露|届时|待定|以合同为准|以[^，。]{0,6}为准")
CORE_STRIP = re.compile(r"[\s\u3000「」『』«»“”（）()《》【】，,。.；;：:、！!？~\-—_·/％%*#]+")
SECTIONS = (("头部申报", r"头部申报"), ("八项逐字速读", r"逐字速读|八项速读"),
            ("口径对照", r"口径对照"), ("缺数清单", r"缺数清单"), ("待人工", r"待人工"))
SPEED_HEAD = re.compile(r"^#{1,4}.*(?:逐字速读|八项速读)")
ANY_HEAD = re.compile(r"^#{1,4}\s")


def core_len(s: str) -> int:
    return len(CORE_STRIP.sub("", s))


def parse_item_line(ln: str):
    """项行拆成字段：名目／书名号原句／锚／原句外句体——判定按字段来，不按整行。"""
    m = ITEM.match(ln)
    if not m:
        return None
    name = m.group(1)
    body = ln[m.end():]
    anchor = ""
    ma = ANCHOR_SPLIT.search(body)
    if ma:
        anchor = body[ma.end():].strip()
        body = body[:ma.start()]
    quotes = QUOTES.findall(body)
    spoken = QUOTES.sub(" ", body).strip()
    return {"name": name, "quotes": quotes, "anchor": anchor, "spoken": spoken, "body": body.strip()}


def trigger_field(item: dict) -> str:
    """触发判据域＝该项自己的原句；没有书名号时退化为去掉锚段与名目前缀后的句体。"""
    if item["quotes"]:
        return " ".join(item["quotes"])
    return item["spoken"] or item["body"]


def trigger_gap(clause: str, sem: str, foreign: str = "", label: str = ""):
    """按规则找合格触发段：剥日期 → 分段 → 该段须同时有触发量纲与触发语境（项名不算语境），
    再核归属：该段附近必须出现**本项**触发语，且不得落在**别项**触发语里。
    返回（被剥日期，合格段，空泛语，落空候选，窗口内命中的别项语，本项语是否缺席）。"""
    dates = [d.strip() for d in DATE_SPAN.findall(clause) if d.strip()]
    naked = DATE_SPAN.sub(" ", clause)
    vague = TRIG_VAGUE.search(naked)
    candidates = []
    foreign_hit = None
    own_absent = False
    pos = 0
    for seg in SEG_SPLIT.split(naked):
        if not seg.strip():
            pos += len(seg)
            continue
        start = naked.find(seg, pos)
        pos = start + len(seg)
        if TRIG_NUM.search(seg) and TRIG_CTX.search(seg):
            window = naked[max(0, start - ATTRIB_WINDOW): pos + ATTRIB_WINDOW]
            if sem and not re.search(sem, window):
                own_absent = True
            elif foreign and re.search(foreign, window):
                foreign_hit = re.search(foreign, window).group(0)
            else:
                return dates, seg.strip(), vague, candidates, foreign_hit, own_absent
            candidates.append(seg.strip())
    return dates, None, vague, candidates, foreign_hit, own_absent


def judge_field(ln: str) -> str:
    """红线判据域＝本件自己写的话：拆字段后剥掉书名号内的公告原句与锚段，项名前缀也不进域。"""
    item = parse_item_line(ln)
    body = item["body"] if item else ln
    body = QUOTES.sub(" ", body)
    ma = ANCHOR_SPLIT.search(body)
    if ma:
        body = body[:ma.start()]
    return body.strip()


def speed_zone(lines: list[str]) -> range:
    start = None
    for i, ln in enumerate(lines):
        if SPEED_HEAD.match(ln):
            start = i + 1
            break
    if start is None:
        return range(0, len(lines))
    end = len(lines)
    for j in range(start, len(lines)):
        if ANY_HEAD.match(lines[j]):
            end = j
            break
    return range(start, end)


def check_text(text: str) -> list[tuple[str, int, str]]:
    """返回 [(码, 行号, 说明)]；行号 0＝整档级判据。"""
    hits: list[tuple[str, int, str]] = []
    lines = text.splitlines()
    for name, pat in SECTIONS:
        if not re.search(pat, text):
            hits.append(("CB-STRUCT", 0, f"缺段：{name}"))
    zone = speed_zone(lines)
    seen = {}
    for i in zone:
        ln = lines[i]
        item = parse_item_line(ln)
        if not item:
            continue
        name = item["name"]
        seen.setdefault(name, i + 1)
        if "未检索到" in ln:
            continue
        if not item["quotes"]:
            hits.append(("CB-QUOTE", i + 1, f"缺项原句：{name} 那一行没有书名号内的原文"))
        elif any(core_len(q) <= 1 for q in item["quotes"]):
            hits.append(("CB-QUOTE", i + 1, f"原句占位：{name} 那一行的书名号内为空或只剩单字"))
        mv = ANCHOR_VAL.search(ln)
        if not mv or core_len(mv.group(1)) == 0:
            hits.append(("CB-QUOTE", i + 1, f"锚值为空：{name} 那一行的「锚：」后面没有来源定位"))
        if name in TRIG_ITEMS:
            clause = trigger_field(item)
            dates, ok_seg, vague, cands, fhit, own_absent = trigger_gap(
                clause, TRIG_SEM[name], TRIG_FOREIGN[name], TRIG_SEM_LABEL[name])
            if ok_seg is None and cands:
                why = f"落在别项触发语境「{fhit}」里" if fhit else f"本项触发语（{TRIG_SEM_LABEL[name]}）在数附近不出现"
                hits.append(("CB-TRIG", i + 1, f"触发条款的数不属本项：{name} 原句里的「{cands[0]}」{why}——别项的触发数不替本项凑数，三组触发各归各的"))
            elif ok_seg is None:
                ev = "｜剥掉的日期：" + "∥".join(dates) if dates else ""
                if vague:
                    hits.append(("CB-TRIG", i + 1, f"触发条款以空泛语顶替：{name} 原句剥掉日期后没有任何一段同时给出触发量纲与触发语境，只剩「{vague.group(0)}」这类空泛说法{ev}——空泛语不因同段另有数字而过闸，别项的数与日期都不顶账"))
                else:
                    hits.append(("CB-TRIG", i + 1, f"触发条款缺该项触发量纲：{name} 原句剥掉日期后，没有一段既带「N%／N 个交易日／N 个计息年度／N 日」又落到本条款的触发语境（连续·低于·转股价格·计息年度·{TRIG_SEM_LABEL[name]}线这类词——项名不算语境）{ev}——日期与别项的数不顶触发账"))
    for name in ITEMS:
        if name not in seen:
            hits.append(("CB-STRUCT", 0, f"缺项行：{name} 在逐字速读段里没有以「- 名目：」起头的行"))
    pending_items = sum(1 for i in zone if ITEM.match(lines[i]) and "未检索到" in lines[i])
    decls = DECL.findall(text)
    if len(decls) > 1:
        hits.append(("CB-COUNT", 0, f"齐缺申报出现 {len(decls)} 处：只准一枚，两处并存即口径不唯一"))
    elif len(decls) == 1 and int(decls[0]) != pending_items:
        hits.append(("CB-COUNT", 0, f"齐缺申报与清单不对账：申报缺 {decls[0]} 项∥速读段实有 {pending_items} 行「未检索到」"))
    elif not decls:
        hits.append(("CB-COUNT", 0, "头部缺「共八项·缺 N 项」申报，无从对账"))
    for i, ln in enumerate(lines, 1):
        if PENDING.search(ln):
            pass   # 行首 [待人工] 标记管全行：这些判断的登记位就在这一行里
        else:
            dom = judge_field(ln)
            flagged = False
            for seg in SEG_SPLIT.split(dom):
                if DISCLAIM.search(seg):
                    continue   # 免责按分句算，不跨句把后半句的真判断一起免掉
                seg = NOUN_WASH.sub("", seg)
                mb = BANNED.search(seg)
                if mb:
                    hits.append(("CB-LINE", i, f"红线断言词出现在没有 [待人工] 的行：本件自己写的话里有「{mb.group(0)}」——同一行前半写了免责句也不顶，豁免只到分句为止"))
                    flagged = True
                    break
                ms, mt = SUBJECT.search(seg), TONE.search(seg)
                if ms and mt:
                    hits.append(("CB-LINE", i, f"判断式结论落在非待人工行：本件自己写的话里「{ms.group(0)}」与判断语气「{mt.group(0)}」同段出现——收益·价值·评级·目标价·赎回·回售这类判断一律留 [待人工]，公告原句（书名号内）与锚不在此列"))
                    flagged = True
                    break
            if not flagged:
                mv2, me = VERDICT.search(dom), EFFECT.search(NOUN_WASH.sub("", dom))
                if mv2 and me:
                    hits.append(("CB-LINE", i, f"自裁效力判断落在非待人工行：本件自己写的话里裁定前缀「{mv2.group(0)}」＋效力判断「{me.group(0)}」——本次发行是否有效·条款是否成立这类裁定本件一律不自判，留 [待人工]；公告原句（书名号内）与锚不在此列"))
        if EMPTY_LIE.search(ln):
            hits.append(("CB-COUNT", i, "把「未检索到」写成「无／没有」"))
    return hits


def make_tmp(prefix: str) -> pathlib.Path:
    d = pathlib.Path(tempfile.mkdtemp(prefix=prefix, dir=str(pathlib.Path(tempfile.gettempdir()))))
    TMP_ROOTS.append(d)
    return d


@atexit.register
def _cleanup() -> None:
    for d in TMP_ROOTS:
        shutil.rmtree(d, ignore_errors=True)


def selftest() -> int:
    here = pathlib.Path(__file__).resolve().parent
    good = here / "fixtures" / "good-cb-card.md"
    bad = here / "fixtures" / "bad-cb-card.md"
    rows = []
    gt = good.read_text(encoding="utf-8")
    gh = check_text(gt)
    rows.append(("好样须过（发条 0）", not gh, f"实发 {len(gh)} 条"))
    bt = bad.read_text(encoding="utf-8")
    bh = check_text(bt)
    codes = {c for c, _, _ in bh}
    rows.append(("坏样五道齐发", {"CB-STRUCT", "CB-QUOTE", "CB-LINE", "CB-COUNT", "CB-TRIG"} <= codes,
                 "实发码 " + "∥".join(sorted(codes))))
    tmp = make_tmp("check-cb-")
    stripped = tmp / "no-anchor.md"
    stripped.write_text(re.sub(r"锚[:：][^\n]*", "锚：", gt), encoding="utf-8")
    sh = check_text(stripped.read_text(encoding="utf-8"))
    rows.append(("反证·剥锚必发 CB-QUOTE", any(c == "CB-QUOTE" for c, _, _ in sh), f"实发 {len(sh)} 条"))
    nproof = 1
    pin = make_tmp("check-cb-pin-")
    ROW_HUI = "「最后两个计息年度，股票收盘价连续三十个交易日低于当期转股价格的 70% 时，持有人可回售」"
    ROW_SHU = "「可转债转股日起二十个交易日后，若公司股票收盘价格不低于当期转股价格的 130%，发行人有权赎回」"
    tiers = (
        ("钉阈·名目只剩散文必发 CB-STRUCT",
         gt.replace("- 担保与评级：", "担保与评级在募集说明书另有说明，", 1),
         "缺项行：担保与评级"),
        ("钉阈·书名号内单字必发 CB-QUOTE",
         gt.replace("「本次发行的可转债自发行结束之日起满六个月后的第一个交易日起至可转债到期日止可转股」", "「转」", 1),
         "原句占位"),
        ("钉阈·齐缺申报改数必发 CB-COUNT",
         gt.replace("共八项·缺 1 项", "共八项·缺 0 项", 1),
         "齐缺申报与清单不对账"),
        ("钉阈·赎回原句整段没数必发 CB-TRIG",
         gt.replace(ROW_SHU, "「发行人有权决定是否办理赎回事宜」", 1),
         "缺该项触发量纲：有条件赎回条款"),
        ("钉阈·别项数字顶触发账（空泛同段带数）必发 CB-TRIG",
         gt.replace(ROW_SHU, "「票面利率 1.5%，满足约定条件时发行人有权赎回」", 1),
         "以空泛语顶替：有条件赎回条款"),
        ("钉阈·裸年份混入回售原句必发 CB-TRIG",
         gt.replace(ROW_HUI, "「发行日期为 2026 年，满足回售条件时可回售」", 1),
         "只剩「满足回售条件」"),
        ("钉阈·全日期冒充回售触发必发 CB-TRIG",
         gt.replace(ROW_HUI, "「公告日期为 2026 年 4 月 1 日，回售条件另定」", 1),
         "只剩「另定」"),
        ("钉阈·全日期无数无空泛必发 CB-TRIG",
         gt.replace(ROW_HUI, "「公告日期为 2026 年 4 月 1 日，持有人可回售」", 1),
         "缺该项触发量纲：回售条款"),
        ("钉阈·另行约定族顶回售触发必发 CB-TRIG",
         gt.replace(ROW_HUI, "「回售条件另行约定」", 1),
         "只剩「另行约定」"),
        ("钉阈·届时公告族顶赎回触发必发 CB-TRIG",
         gt.replace(ROW_SHU, "「赎回触发条件届时公告」", 1),
         "只剩「届时」"),
        ("钉阈·别项触发句占本项（下修句占回售）必发 CB-TRIG",
         gt.replace(ROW_HUI, "「股票收盘价连续三十个交易日低于转股价格的 85% 时，董事会可下修转股价格」", 1),
         "不属本项：回售条款 原句里的"),
        ("钉阈·本项词与别项数混排必发 CB-TRIG",
         gt.replace(ROW_HUI, "「回售条件另定，股票收盘价连续三十个交易日低于转股价格的 85% 时，董事会可下修」", 1),
         "落在别项触发语境「下修」里"),
        ("钉阈·免责句后半的真判断必发 CB-LINE",
         gt.replace("## 二、八项逐字速读", "- 说明：本件不接申购；转股收益一定能兑现。\n\n## 二、八项逐字速读", 1),
         "本件自己写的话里有「转股收益」"),
        ("钉阈·自裁效力族一必发 CB-LINE",
         gt.replace("## 二、八项逐字速读", "- 结论：本次发行无效。\n\n## 二、八项逐字速读", 1),
         "裁定前缀「结论」＋效力判断「无效」"),
        ("钉阈·自裁效力族二必发 CB-LINE",
         gt.replace("## 二、八项逐字速读", "- 综上，该赎回条款作废。\n\n## 二、八项逐字速读", 1),
         "裁定前缀「综上」＋效力判断「作废」"),
        ("钉阈·否决式判断句必发 CB-LINE",
         gt.replace("## 二、八项逐字速读", "- 结论：回售应予否决。\n\n## 二、八项逐字速读", 1),
         "「回售」与判断语气「应予」"),
        ("钉阈·红线定式词落在非待人工行必发 CB-LINE",
         gt.replace("## 二、八项逐字速读", "- 结论：本单建议申购，稳赚。\n\n## 二、八项逐字速读", 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·判断式家族一（主题＋语气）必发 CB-LINE",
         gt.replace("## 二、八项逐字速读", "- 结论：回售收益可期。\n\n## 二、八项逐字速读", 1),
         "「回售」与判断语气「可期」"),
        ("钉阈·判断式家族二（主题＋语气）必发 CB-LINE",
         gt.replace("## 二、八项逐字速读", "- 结论：评级将上调。\n\n## 二、八项逐字速读", 1),
         "「评级」与判断语气「将」"),
    )
    for n, (name, text, needle) in enumerate(tiers, 1):
        nproof += 1
        p = pin / f"pin-{n}.md"
        p.write_text(text, encoding="utf-8")
        ph = check_text(p.read_text(encoding="utf-8"))
        fired = [m for c, _, m in ph if needle in m]
        injected = text != gt
        rows.append((name, injected and bool(fired),
                     f"注入{'生效' if injected else '作废'}·实发 {len(ph)} 条·命中句 "
                     + ("∥".join(fired) if fired else "无")))
    control = pin / "control-date-plus-value.md"
    ctl_text = gt.replace(ROW_HUI, "「公告日期为 2026 年 4 月 1 日，最后两个计息年度内股票收盘价连续三十个交易日低于当期转股价格的 70% 时，持有人可回售」", 1)
    control.write_text(ctl_text, encoding="utf-8")
    ch = check_text(control.read_text(encoding="utf-8"))
    nproof += 1
    rows.append(("对照·夹带日期的合格触发句不误伤（CB-TRIG 零发）",
                 ctl_text != gt and not [m for c, _, m in ch if c == "CB-TRIG"],
                 f"注入生效＝{ctl_text != gt}·CB-TRIG 实发 {len([m for c, _, m in ch if c == 'CB-TRIG'])} 条"))
    ctrls_cb = (
        ("对照·会计处理说明不误伤（CB-LINE 零发）",
         gt.replace("## 二、八项逐字速读", "- 说明：赎回的会计处理以募集说明书为准。\n\n## 二、八项逐字速读", 1), "CB-LINE"),
        ("对照·会议记录陈述不误伤（CB-LINE 零发）",
         gt.replace("## 二、八项逐字速读", "- 说明：会议记录载明票面利率梯度。\n\n## 二、八项逐字速读", 1), "CB-LINE"),
    )
    for n, (name, text, code) in enumerate(ctrls_cb, 1):
        nproof += 1
        cz = pin / f"control-cb-{n}.md"
        cz.write_text(text, encoding="utf-8")
        th = check_text(cz.read_text(encoding="utf-8"))
        fired = [m for cd, _, m in th if cd == code]
        rows.append((name, text != gt and not fired, f"注入{'生效' if text != gt else '作废'}·{code} 实发 {len(fired)} 条"))
    control2 = pin / "control-revision-dated.md"
    ctl2 = gt.replace("「前二十个交易日中至少十个交易日收盘价低于当期转股价格的 85% 时，董事会有权提出修正方案」",
                      "「公告日期为 2026 年 3 月 1 日，前二十个交易日中至少十个交易日收盘价低于当期转股价格的 85% 时，董事会有权提出修正方案」", 1)
    control2.write_text(ctl2, encoding="utf-8")
    ch2 = check_text(control2.read_text(encoding="utf-8"))
    nproof += 1
    rows.append(("对照·修正项夹带日期不误伤（CB-TRIG 零发）",
                 ctl2 != gt and not [m for c, _, m in ch2 if c == "CB-TRIG"],
                 f"注入生效＝{ctl2 != gt}·CB-TRIG 实发 {len([m for c, _, m in ch2 if c == 'CB-TRIG'])} 条"))
    ctrl_hui = pin / "control-institution-name.md"
    text_hui = gt.replace("## 二、八项逐字速读", "- 说明：回售价格调整由董事会与薪酬委员会核实。\n\n## 二、八项逐字速读", 1)
    ctrl_hui.write_text(text_hui, encoding="utf-8")
    hh = check_text(ctrl_hui.read_text(encoding="utf-8"))
    nproof += 1
    fired_hui = [m for cd, _, m in hh if cd == "CB-LINE"]
    rows.append(("对照·机构名陈述句不误伤（CB-LINE 零发）", text_hui != gt and not fired_hui,
                 f"注入{'生效' if text_hui != gt else '作废'}·CB-LINE 实发 {len(fired_hui)} 条"))
    made = [p.name for p in TMP_ROOTS]
    root = pathlib.Path(tempfile.gettempdir())
    for p in TMP_ROOTS:
        shutil.rmtree(p, ignore_errors=True)
    leftover = sorted(q.name for q in root.iterdir() if q.name.startswith("check-cb-")) if root.is_dir() else []
    rows.append(("临时根自清（跑后不增）", not leftover,
                 f"本次建 {len(made)} 枚·跑后残留 {len(leftover)} 枚"))
    bad_rows = [r for r in rows if not r[1]]
    for name, ok, detail in rows:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}｜{detail}")
    print(f"selftest: {'ALL GREEN' if not bad_rows else 'FAIL'}（好样 1 枚·坏样五道·反例 {nproof} 枚·临时根 {len(TMP_ROOTS)} 枚自清）")
    return 0 if not bad_rows else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="可转债条款卡五道机检（零网络）")
    ap.add_argument("target", nargs="?", help="待检文件（本件不读网络、不读目录）")
    ap.add_argument("--selftest", action="store_true", help="好样须过、坏样五道齐发、钉阈按整族各钉一档、对照样不误伤、临时件自清")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.target:
        print("用法：check_cb_card.py <待检文件> | --selftest", file=sys.stderr)
        return 2
    p = pathlib.Path(a.target)
    if not p.is_file():
        print(f"FAIL 文件不在场：{p}", file=sys.stderr)
        return 2
    text = p.read_text(encoding="utf-8", errors="replace")
    hits = check_text(text)
    for code, ln, msg in hits:
        print(f"FAIL [{code}] {p.name}" + (f":{ln}" if ln else "") + f" {msg}")
    print(("PASS" if not hits else "FAIL") + f"（扫过 {len(text.splitlines())} 行，发条 {len(hits)} 条）")
    return 0 if not hits else 1


if __name__ == "__main__":
    sys.exit(main())