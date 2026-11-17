#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_bid_card.py — 招投标披露全景卡的机检（零网络、只读本包外传入的文件）。

五道码（缺一即不叫过闸）：
  BP-STRUCT 五段齐：头部申报／八项逐字速读／口径对照／缺数清单／待人工，任一节缺失即发；
            八项名目另须在「逐字速读」段内**行级在场**——每枚名目一行以「- 名目：」起头，只在散文里提到不算占行；
  BP-QUOTE  每项原句与锚：项行的书名号（「」『』«»）内原句不得为空或只剩单字；「锚：」标签在而锚值为空同样发；
  BP-LINE   红线断言三道：①定式禁词中标概率／必中标／稳赚／零风险／保证收益／利好／建议投标／代客投标／陪标／
            围标／串通报价／利益输送，以及异议…成立／目标价／评级上调下调／收入（营收）增减；
            ②判断式规则——项行先拆成字段（名目／书名号原句／锚／句体），红线判据域只取本件自己写的话：
            非 [待人工]、非「不接／不出／不判」类免责行、剥掉公告原句（书名号内）与锚之后，只要主题词
            （异议·质疑·评级·目标价·收入·营收·利润·概率·利好·收益·风险·废标·围标·串标·回款·工期）
            与判断语气（应·应予·予以·将·会·必·有望·可能·足以·构成·属于·支持·成立·上调·下调·增加·减少·无疑…）
            同段出现即发——不靠枚举结论短语，「应予支持／予以支持／应被支持」都算同一族；
            语气域先洗掉机构名 token（委员会／董事会／监事会／股东大会／理事会／工会／发布会后缀的「会」
            是名词后缀不是判断语气），所以「异议需提交股东大会处理」「名单由评标委员会核实」不误红；
            ③自裁效力层：本件自己写的话里出现裁定前缀（结论／综上／因此／据此／本院认为／判定／认定…）
            与效力判断（无效／有效／作废／成立／不成立／撤销／违法／违规／支持…）即发——
            「结论：该中标无效」这种自裁断语不靠把「中标」塞进主题词表来逮（那才会误红正常说明行）；
  BP-COUNT  齐缺申报恰一枚：头部「共八项·缺 N 项」只准出现一处（两处并存即发），且 N 必须等于速读段里
            「未检索到」的项行数；把「未检索到」写成「无该项／没有此项」一律发；
  BP-AMT    中标金额按**规则**判、不按词表判：先把项行拆成字段，取该项自己的原句作判据域，
            ①先剥日期（YYYY年M月D日／YYYY年／M月D日一律从取数域剔除）；
            ②剩下的句段必须有一段**同时**带金额量纲（N 元／万元／亿元）与中标口径词
            （中标·决标·定标·成交·候选人·投标·报价·合同价），且**口径词与数字之间**不带上限·控制价·预算·概算·估算·
            限价·最高·最低·保证金·意向·参考——「投标报价上限 2 亿元」「项目预算 2 亿元」都不顶中标实额；
            数字自己就被说成上限（「中标金额 2 亿元为最高投标限价」「中标金额为 2 亿元，即招标上限」）照剔；
            但实额之后的**括注约束**（「8,600 万元（不高于最高投标限价）」）放行——那是同一笔实额的上限说明，不是另报上限数；
            ③反向判：剥日期与剔掉不合格口径后一段合格段都没有、又没写「未检索到」，即发——
            空泛语（详见…／以…为准／另行确定／另行约定／另定／尚未披露／未披露／届时／待定）只决定那句话怎么措辞，
            换同义词换不掉这一判；发红时把被剔的段与剥掉的日期一并点名。

用法：
  python3 -B scripts/check_bid_card.py <待检文件>      # 逐条发红，全过则 PASS
  python3 -B scripts/check_bid_card.py --selftest      # 好样须过、坏样五道齐发、钉阈按整族各钉一档、对照样不误伤、临时件自清
  python3 -B scripts/check_bid_card.py --help
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

ITEMS = ("项目名称与编号", "招标人与代理机构", "开标时间与方式", "评标标准与方法",
         "中标候选人及金额", "中标公示与日期", "合同履约与期限", "异议与质疑渠道")
AMT_ITEM = "中标候选人及金额"
ITEM = re.compile(r"^\s*[-*]\s*(" + "|".join(map(re.escape, ITEMS)) + r")[：:]")
TITLE = re.compile(r"[「『«][^」』»]+[」』»]")
QUOTES = re.compile(r"[「『«]([^」』»]*)[」』»]")
ANCHOR_SPLIT = re.compile(r"锚[:：]")
ANCHOR_VAL = re.compile(r"锚[:：]\s*(\S.*)$")
BANNED = re.compile(r"中标概率|必中标|稳赚|零风险|保证收益|利好|建议投标|代客投标|陪标|围标|串通报价|利益输送"
                    r"|异议[^，。；、」』]{0,6}成立|目标价|评级上调|评级下调|(?:收入|营收)[^，。；、」』]{0,8}?(?:增加|上升|提升|减少|下滑)")
PENDING = re.compile(r"\[待人工\]")
DECL = re.compile(r"共\s*(?:八|8)\s*项\s*[·：:|｜、]\s*缺\s*(\d+)\s*项")
EMPTY_LIE = re.compile(r"(?:^|[\s：:])无(?:该项|此项)|没有(?:该项|此项)")
DATE_SPAN = re.compile(r"\d{4}\s*(?:年|[-/.])\s*\d{1,2}\s*(?:月|[-/.])?\s*\d{1,2}\s*日?"
                       r"|\d{4}\s*年(?:\s*\d{1,2}\s*月)?(?:\s*\d{1,2}\s*日)?"
                       r"|\d{1,2}\s*月\s*\d{1,2}\s*日"
                       r"|\d{4}[-/.]\d{1,2}[-/.]\d{1,2}")
SEG_SPLIT = re.compile(r"[，。；、！？；]+|[,!](?!\s*\d)")   # 千分位逗号不断段（8,600 是一枚数）
AMT_SEM = re.compile(r"中标|决标|定标|成交|候选人|投标|报价|合同价|发包价|签约价")
AMT_BRACKET = re.compile(r"^[（(]")
ATTRIB_WINDOW = 24
AMT_REF_NOUN = r"上限|控制价|最高限价|限价|预算|概算|估算|基准价|评标基准|账面净资产|账面值|净值|评估价|参考价|市场价|市价|面值|保证金|意向价"
AMT_DISQUAL = re.compile(AMT_REF_NOUN + r"|最高|最低|不高于|不低于|参考|意向")   # 参照价词族：数挂在这些词上就不是中标实额（与「实额后的括注约束」两分）
AMT_UNIT = re.compile(r"\d[\d,\.]*\s*(?:亿元|万元|元)")
AMT_VAGUE = re.compile(r"详见[^，。]*|以合同为准|以[^，。]{0,6}为准|另行确定|另行约定|另行公告|另定|金额待定|待定|尚未披露|未披露|尚未公布|未公布|届时|尚未明确")
SUBJECT = re.compile(r"异议|质疑|评级|目标价|收入|营收|利润|概率|利好|收益|风险|废标|围标|串标|中标可能|回款|工期")
TONE = re.compile(r"应当|应予|予以|将|会|必|有望|可期|可能|足以|构成|属于|意味着|支持|成立|推翻|无效|有效|上调|下调|提升|下滑|增加|减少|高于|低于|稳赚|赚|亏|无疑|显然|肯定|应(?!急)")
VERDICT = re.compile(r"结论|综上|因此|可见|据此|本院认为|本件认为|本卡认为|本件判断|判定|认定|断言")
EFFECT = re.compile(r"无效|有效|作废|不成立|成立|撤销|违法|违规|应予支持|予以支持|应支持|支持|必然|属实")
NOUN_WASH = re.compile(r"[员委事大东议工学协商年例常布明谈论聚汇组]会|会[计议场话晤所馆堂员]")   # 「X 会」机构名后缀与「会 X」名词（会计·会议·会场·会员·会话）两头的「会」都是名词性成分，不是判断语气——两头按形态一起洗，不枚举个案
DISCLAIM = re.compile(r"不接|不出|不提供|不作|不判|禁止|未证|无法|不承诺")
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


def amount_field(item: dict) -> str:
    """金额判据域＝该项自己的原句；没有书名号时退化为去掉锚段与名目前缀后的句体。"""
    if item["quotes"]:
        return " ".join(item["quotes"])
    return item["spoken"] or item["body"]


AMT_AS_CAP = re.compile(r"^[为是即报]?\s*(?:不高于|不低于)?[^，。；、）)]{0,10}?(" + AMT_REF_NOUN + ")")
AMT_CAP_AFTER = re.compile(r"^[，、]?\s*(?:即|为|系|是|属于?)\s*[^，。]{0,12}(" + AMT_REF_NOUN + ")")


def amount_gap(clause: str):
    """按规则找合格金额段：剥日期 → 分段 → 金额自己须紧跟中标口径，且**口径与数之间**不带上限／预算／控制价；
    数后面的括注约束（如「（不高于最高投标限价）」）放行——那是实额的上限说明，不是另报一个上限数；
    但数后面直陈「即／为……上限」的，等于本数自己就是限价，照剔（剔除面跨到下一段的前 24 字）。"""
    dates = [d.strip() for d in DATE_SPAN.findall(clause) if d.strip()]
    naked = DATE_SPAN.sub(" ", clause)
    vague = AMT_VAGUE.search(naked)
    bounds, start = [], 0
    for m in SEG_SPLIT.finditer(naked):
        bounds.append((start, m.start())); start = m.end()
    bounds.append((start, len(naked)))
    rejected = []
    for s, e in bounds:
        seg = naked[s:e].strip()
        if not seg:
            continue
        for m in AMT_UNIT.finditer(naked, s, e):
            prefix = naked[s:m.start()]
            tail = naked[m.end():min(len(naked), e + ATTRIB_WINDOW)]
            sems = list(AMT_SEM.finditer(prefix))
            if not sems:
                why = AMT_DISQUAL.search(prefix) or AMT_DISQUAL.search(naked[s:e])
                rejected.append((seg, why.group(0) if why else "无中标口径词"))
                continue
            dq = AMT_DISQUAL.search(prefix[sems[-1].end():])
            if dq:
                rejected.append((seg, dq.group(0)))
                continue
            cap = None if AMT_BRACKET.match(tail.lstrip()) else (AMT_AS_CAP.match(tail) or AMT_CAP_AFTER.match(tail))
            if cap:
                rejected.append((seg, cap.group(cap.lastindex or 1)))
                continue
            return dates, seg, None, vague
    return dates, None, rejected, vague


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
            hits.append(("BP-STRUCT", 0, f"缺段：{name}"))
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
            hits.append(("BP-QUOTE", i + 1, f"缺项原句：{name} 那一行没有书名号内的原文"))
        elif any(core_len(q) <= 1 for q in item["quotes"]):
            hits.append(("BP-QUOTE", i + 1, f"原句占位：{name} 那一行的书名号内为空或只剩单字"))
        mv = ANCHOR_VAL.search(ln)
        if not mv or core_len(mv.group(1)) == 0:
            hits.append(("BP-QUOTE", i + 1, f"锚值为空：{name} 那一行的「锚：」后面没有来源定位"))
        if name == AMT_ITEM:
            dates, ok_seg, rejected, vague = amount_gap(amount_field(item))
            ev = ""
            if rejected:
                ev = "｜有数但被剔的段：" + "∥".join(f"「{s}」＝{why}" for s, why in rejected)
            if dates:
                ev += "｜剥掉的日期：" + "∥".join(dates)
            if ok_seg is None:
                if vague:
                    hits.append(("BP-AMT", i + 1, f"中标金额以空泛语顶替：{name} 原句剥掉日期后没有任何一段给出中标／成交口径的实额，只剩「{vague.group(0)}」这类说法{ev}——上限·预算·控制价的数与日期都不顶中标账，换同义词也换不掉这一判"))
                else:
                    hits.append(("BP-AMT", i + 1, f"中标金额缺实额原值：{name} 原句剥掉日期后没有一段既带「N 元／万元／亿元」又落在中标口径（中标·决标·成交·候选人实投标报价）{ev}——干扰口径与别项的数不顶账，没取到就写「未检索到」"))
    for name in ITEMS:
        if name not in seen:
            hits.append(("BP-STRUCT", 0, f"缺项行：{name} 在逐字速读段里没有以「- 名目：」起头的行"))
    pending_items = sum(1 for i in zone if ITEM.match(lines[i]) and "未检索到" in lines[i])
    decls = DECL.findall(text)
    if len(decls) > 1:
        hits.append(("BP-COUNT", 0, f"齐缺申报出现 {len(decls)} 处：只准一枚，两处并存即口径不唯一"))
    elif len(decls) == 1 and int(decls[0]) != pending_items:
        hits.append(("BP-COUNT", 0, f"齐缺申报与清单不对账：申报缺 {decls[0]} 项∥速读段实有 {pending_items} 行「未检索到」"))
    elif not decls:
        hits.append(("BP-COUNT", 0, "头部缺「共八项·缺 N 项」申报，无从对账"))
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
                    hits.append(("BP-LINE", i, f"红线断言词出现在没有 [待人工] 的行：本件自己写的话里有「{mb.group(0)}」——同一行前半写了免责句也不顶，豁免只到分句为止"))
                    flagged = True
                    break
                ms, mt = SUBJECT.search(seg), TONE.search(seg)
                if ms and mt:
                    hits.append(("BP-LINE", i, f"判断式结论落在非待人工行：本件自己写的话里「{ms.group(0)}」与判断语气「{mt.group(0)}」同段出现——异议·评级·目标价·收入这类判断一律留 [待人工]，公告原句（书名号内）与锚不在此列"))
                    flagged = True
                    break
            if not flagged:
                mv2, me = VERDICT.search(dom), EFFECT.search(NOUN_WASH.sub("", dom))
                if mv2 and me:
                    hits.append(("BP-LINE", i, f"自裁效力判断落在非待人工行：本件自己写的话里裁定前缀「{mv2.group(0)}」＋效力判断「{me.group(0)}」——中标效力·异议是否成立这类裁定本件一律不自判，留 [待人工]；公告原句（书名号内）与锚不在此列"))
        if EMPTY_LIE.search(ln):
            hits.append(("BP-COUNT", i, "把「未检索到」写成「无／没有」"))
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
    good = here / "fixtures" / "good-bid-card.md"
    bad = here / "fixtures" / "bad-bid-card.md"
    rows = []
    gt = good.read_text(encoding="utf-8")
    gh = check_text(gt)
    rows.append(("好样须过（发条 0）", not gh, f"实发 {len(gh)} 条"))
    bt = bad.read_text(encoding="utf-8")
    bh = check_text(bt)
    codes = {c for c, _, _ in bh}
    rows.append(("坏样五道齐发", {"BP-STRUCT", "BP-QUOTE", "BP-LINE", "BP-COUNT", "BP-AMT"} <= codes,
                 "实发码 " + "∥".join(sorted(codes))))
    tmp = make_tmp("check-bid-")
    stripped = tmp / "no-anchor.md"
    stripped.write_text(re.sub(r"锚[:：][^\n]*", "锚：", gt), encoding="utf-8")
    sh = check_text(stripped.read_text(encoding="utf-8"))
    rows.append(("反证·剥锚必发 BP-QUOTE", any(c == "BP-QUOTE" for c, _, _ in sh), f"实发 {len(sh)} 条"))
    nproof = 1
    pin = make_tmp("check-bid-pin-")
    ROW_AMT = "「第一中标候选人某建设集团，投标报价 8,600 万元」"
    tiers = (
        ("钉阈·名目只剩散文必发 BP-STRUCT",
         gt.replace("- 异议与质疑渠道：", "异议与质疑渠道在公告另有说明，", 1),
         "缺项行：异议与质疑渠道"),
        ("钉阈·书名号内单字必发 BP-QUOTE",
         gt.replace("「市政道路改造工程（招标编号：ZB-2026-0312）」", "「项」", 1),
         "原句占位"),
        ("钉阈·齐缺申报改数必发 BP-COUNT",
         gt.replace("共八项·缺 1 项", "共八项·缺 0 项", 1),
         "齐缺申报与清单不对账"),
        ("钉阈·中标金额写成详见公告必发 BP-AMT",
         gt.replace(ROW_AMT, "「中标金额详见公告」", 1),
         "只剩「详见公告」"),
        ("钉阈·预算金额洗中标额必发 BP-AMT",
         gt.replace(ROW_AMT, "「项目预算 2 亿元，中标金额以合同为准」", 1),
         "「项目预算 2 亿元」＝预算"),
        ("钉阈·预算金额无空泛语也不放行必发 BP-AMT",
         gt.replace(ROW_AMT, "「项目预算 2 亿元，最终数额在合同阶段明确」", 1),
         "中标金额缺实额原值"),
        ("钉阈·报价上限洗中标额必发 BP-AMT",
         gt.replace(ROW_AMT, "「投标报价上限 2 亿元，中标金额尚未披露」", 1),
         "「投标报价上限 2 亿元」＝上限"),
        ("钉阈·招标控制价洗中标额必发 BP-AMT",
         gt.replace(ROW_AMT, "「招标控制价 1.2 亿元，中标金额另行公告」", 1),
         "「招标控制价 1.2 亿元」＝控制价"),
        ("钉阈·保证金洗中标额必发 BP-AMT",
         gt.replace(ROW_AMT, "「投标保证金 80 万元，中标金额未披露」", 1),
         "「投标保证金 80 万元」＝保证金"),
        ("钉阈·数字自己就是限价必发 BP-AMT",
         gt.replace(ROW_AMT, "「中标金额 2 亿元为最高投标限价」", 1),
         "「中标金额 2 亿元为最高投标限价」＝限价"),
        ("钉阈·跨段直陈上限必发 BP-AMT",
         gt.replace(ROW_AMT, "「中标金额为 2 亿元，即招标上限」", 1),
         "「中标金额为 2 亿元」＝上限"),
        ("钉阈·红线定式词落在非待人工行必发 BP-LINE",
         gt.replace("｜来路：官方原文", "｜来路：官方原文｜中标概率高", 1),
         "话里有「中标概率」"),
        ("钉阈·上轮判断式原句仍红必发 BP-LINE",
         gt.replace("## 二、八项逐字速读",
                    "- 结论：异议必然成立，目标价上调，项目收入将增加。\n\n## 二、八项逐字速读", 1),
         "话里有「异议必然成立」"),
        ("钉阈·异议应予支持族必发 BP-LINE",
         gt.replace("## 二、八项逐字速读", "- 结论：异议应予支持。\n\n## 二、八项逐字速读", 1),
         "「异议」与判断语气「应予」"),
        ("钉阈·异议予以支持族必发 BP-LINE",
         gt.replace("## 二、八项逐字速读", "- 结论：该异议予以支持。\n\n## 二、八项逐字速读", 1),
         "「异议」与判断语气「予以」"),
        ("钉阈·评级目标价族必发 BP-LINE",
         gt.replace("## 二、八项逐字速读", "- 结论：评级将上调。\n\n## 二、八项逐字速读", 1),
         "「评级」与判断语气「将」"),
        ("钉阈·收入影响族必发 BP-LINE",
         gt.replace("## 二、八项逐字速读", "- 结论：项目收入可能翻倍。\n\n## 二、八项逐字速读", 1),
         "「收入」与判断语气「可能」"),
        ("钉阈·免责句后半的真判断必发 BP-LINE",
         gt.replace("## 二、八项逐字速读", "- 说明：本件不判异议是否成立；项目收入一定能增加。\n\n## 二、八项逐字速读", 1),
         "本件自己写的话里有「收入一定能增加」"),
        ("钉阈·评标基准价冒充中标额必发 BP-AMT",
         gt.replace(ROW_AMT, "「投标报价为评标基准价 8,600 万元」", 1),
         "＝评标基准"),
        ("钉阈·账面值冒充中标额必发 BP-AMT",
         gt.replace(ROW_AMT, "「中标金额为账面值 8,600 万元」", 1),
         "＝账面值"),
        ("钉阈·否决式判断句必发 BP-LINE",
         gt.replace("## 二、八项逐字速读", "- 结论：异议应予否决。\n\n## 二、八项逐字速读", 1),
         "「异议」与判断语气「应予」"),
        ("钉阈·自裁效力族一必发 BP-LINE",
         gt.replace("## 二、八项逐字速读", "- 结论：该中标无效。\n\n## 二、八项逐字速读", 1),
         "裁定前缀「结论」＋效力判断「无效」"),
        ("钉阈·自裁效力族二必发 BP-LINE",
         gt.replace("## 二、八项逐字速读", "- 综上，本次评标作废。\n\n## 二、八项逐字速读", 1),
         "裁定前缀「综上」＋效力判断「作废」"),
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
    control = pin / "control-date-plus-amount.md"
    ctl_text = gt.replace(ROW_AMT, "「公示日期为 2026 年 4 月 26 日，第一中标候选人某建设集团，投标报价 8,600 万元」", 1)
    control.write_text(ctl_text, encoding="utf-8")
    ch = check_text(control.read_text(encoding="utf-8"))
    nproof += 1
    rows.append(("对照·夹带日期的合格金额句不误伤（BP-AMT 零发）",
                 ctl_text != gt and not [m for c, _, m in ch if c == "BP-AMT"],
                 f"注入生效＝{ctl_text != gt}·BP-AMT 实发 {len([m for c, _, m in ch if c == 'BP-AMT'])} 条"))
    ctrls = (
        ("对照·实额后括注限价约束不误伤（BP-AMT 零发）",
         gt.replace(ROW_AMT, "「第一中标候选人为甲，投标报价为人民币 8,600 万元（不高于最高投标限价）」", 1), "BP-AMT"),
        ("对照·拟中标实额按边界放行（BP-AMT 零发）",
         gt.replace(ROW_AMT, "「第一候选人甲，拟中标金额 8,600 万元」", 1), "BP-AMT"),
        ("对照·会议记录陈述不误伤（BP-LINE 零发）",
         gt.replace("## 二、八项逐字速读", "- 说明：会议记录载明异议渠道见第六节。\n\n## 二、八项逐字速读", 1), "BP-LINE"),
        ("对照·评标委员会组建句不误伤（BP-LINE 零发）",
         gt.replace("## 二、八项逐字速读", "- 说明：评标委员会由招标人依法组建。\n\n## 二、八项逐字速读", 1), "BP-LINE"),
        ("对照·实额后不跟参照价不误伤（BP-AMT 零发）",
         gt.replace(ROW_AMT, "「第一中标候选人某建设集团，中标金额为人民币 8,600 万元」", 1), "BP-AMT"),
        ("对照·机构名陈述句不误伤（BP-LINE 零发）",
         gt.replace("## 二、八项逐字速读", "- 说明：异议需提交股东大会处理。\n\n## 二、八项逐字速读", 1), "BP-LINE"),
        ("对照·委员会核实句不误伤（BP-LINE 零发）",
         gt.replace("## 二、八项逐字速读", "- 说明：中标候选人名单由评标委员会核实。\n\n## 二、八项逐字速读", 1), "BP-LINE"),
        ("对照·正常说明行不误伤（BP-LINE 零发）",
         gt.replace("## 二、八项逐字速读", "- 说明：中标公示载明异议渠道，原句见第六节。\n\n## 二、八项逐字速读", 1), "BP-LINE"),
    )
    for n, (name, text, code) in enumerate(ctrls, 1):
        nproof += 1
        c = pin / f"control-{n}.md"
        c.write_text(text, encoding="utf-8")
        th = check_text(c.read_text(encoding="utf-8"))
        fired = [m for cd, _, m in th if cd == code]
        rows.append((name, text != gt and not fired,
                     f"注入{'生效' if text != gt else '作废'}·{code} 实发 {len(fired)} 条"))
    made = [p.name for p in TMP_ROOTS]
    root = pathlib.Path(tempfile.gettempdir())
    for p in TMP_ROOTS:
        shutil.rmtree(p, ignore_errors=True)
    leftover = sorted(q.name for q in root.iterdir() if q.name.startswith("check-bid-")) if root.is_dir() else []
    rows.append(("临时根自清（跑后不增）", not leftover,
                 f"本次建 {len(made)} 枚·跑后残留 {len(leftover)} 枚"))
    bad_rows = [r for r in rows if not r[1]]
    for name, ok, detail in rows:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}｜{detail}")
    print(f"selftest: {'ALL GREEN' if not bad_rows else 'FAIL'}（好样 1 枚·坏样五道·反例 {nproof} 枚·临时根 {len(TMP_ROOTS)} 枚自清）")
    return 0 if not bad_rows else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="招投标披露全景卡五道机检（零网络）")
    ap.add_argument("target", nargs="?", help="待检文件（本件不读网络、不读目录）")
    ap.add_argument("--selftest", action="store_true", help="好样须过、坏样五道齐发、钉阈按整族各钉一档、对照样不误伤、临时件自清")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.target:
        print("用法：check_bid_card.py <待检文件> | --selftest", file=sys.stderr)
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