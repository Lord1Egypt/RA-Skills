#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_eip_card.py — A股股权激励计划条款卡的机检（零网络、只读传入文件）。

五道码（缺一即不叫过闸）：
  EIP-STRUCT 五段齐：头部申报／八项逐字速读／口径对照／缺数清单／待人工，任一节缺失即发；
             八项名目另须在「逐字速读」段内**行级在场**——每枚名目一行以「- 名目：」起头，只在散文里提到不算占行；
  EIP-QUOTE  每项原句与锚：项行的书名号（「」『』«»）内原句不得为空或只剩单字；「锚：」标签在而锚值为空同样发；
  EIP-LINE   红线断言三道：①定式禁词行权盈亏／摊销测算／稀释比例结论／一定能行权／稳赚／零风险／保证收益／利好／
             建议参与／代客行权／内幕信息利用／绕开审议；②判断式规则——项行拆字段后，红线判据域只取本件自己写的话
             （剥掉书名号内的草案原句与锚，非 [待人工]、非明写「不接／不出／不判」的免责行，
             并把机构名 token——委员会／董事会／监事会／股东大会／理事会／工会／发布会——后缀的「会」先从语气域洗掉），主题词
             （解锁·限售·行权·授予·摊销·摊薄·稀释·业绩考核·激励对象·股价·收入·利润·评级·目标价·利好·收益·风险）
             与判断语气（应·应予·予以·将·会·必·有望·可期·可能·足以·构成·属于·意味着·支持·成立·上调·下调·增加·减少·
             高于·低于·稳赚·赚·亏·无疑·显然·肯定…）同段出现即发；③自裁效力层：裁定前缀（结论／综上／因此／本件认为／
             判定／认定…）与效力判断（无效／有效／作废／不成立／成立／撤销／违法／违规／属实…）同现即发；
  EIP-COUNT  齐缺申报恰一枚：头部「共八项·缺 N 项」只准出现一处（两处并存即发），且 N 必须等于速读段里
             「未检索到」的项行数；把「未检索到」写成「无该项／没有此项」一律发；
  EIP-PRICE  授予价格与定价方法一项**以短语结构体为主**判、不按词表也不按位置判：①先把项行拆成字段（名目／书名号原句／锚／句体），
             判据域只取该项自己的原句；②先剥日期（YYYY年M月D日／YYYY年／M月D日／ISO 形一律从取数域剔除，
             公告日的「1 日」不是价格）；③**先建结构体、判定以它为主**（不在原文上挪窗、也不靠补词）：取数域按「SEG_SPLIT 标点 ∪ PRICE_ABS 金额边界」
             切成短语表，每短语＝〔数左｜内金额｜数右〕，内领价·内参照·内金额三列偏移各自算好；一枚候选归谁所有只在本短语内判一次——
             数左跳过单位（每股·每份·人民币·元·约·为·即·按·暂定·最终·后·前…）后最近的实义名词是领价族（授予价格·行权价格·定价·折扣）
             才算本项实额，是参照族（市价·市场价·面值·均价·收盘价·开盘价·净值·账面值·账面净资产·评估价·参考价·基准价）且比领价更靠数
             即剔，**哪怕同一短语别处写了「授予价格」**；「每股」是单位不是所有者，「面值每股 1 元」仍归面值；数左什么都不剩时看本短语数右
             （「每股 12.60 元的授予价格」合格、「每股 1 元的股票面值」即剔）；短语内两头都没名词＝**孤立数**（主语省略，
             「最终每股 12.60 元」里「最终」是状语不是所有者）：继承前序最近一次的领价名词，**前序从头到尾只出现过参照价时不继承、
             本数仍归参照**（防把参照洗成合格）；④反向判兜底：剥日期后没有一段合格、又没写「未检索到」即发，
             空泛语（另行确定·另行约定·届时公告·待定·由董事会确定·按有关规定执行·以…为准）只决定发红那句话的措辞，
             换同义词换不掉判据。发红句把被剥的日期、落空的候选段与取数域首段一并点名当证据。

用法：
  python3 -B scripts/check_eip_card.py <待检文件>      # 逐条发红，全过则 PASS
  python3 -B scripts/check_eip_card.py --selftest      # 好样须过、坏样五道齐发、钉阈按整族各钉一档、对照样不误伤、临时件自清
  python3 -B scripts/check_eip_card.py --help
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

ITEMS = ("激励形式与股票来源", "授予数量与占比", "激励对象与范围", "授予价格与定价方法",
         "有效期与等待期安排", "解除限售与行权条件", "特殊情形与离职处理", "审议程序与披露义务")
PRICE_ITEM = "授予价格与定价方法"
PRICE_OWN = re.compile(r"授予价格|授予价|行权价格|行权价|定价|均价|每股")
PRICE_ABS = re.compile(r"每股\s*\d[\d,\.]*\s*元|\d[\d,\.]*\s*元(?:\/股)?")
PRICE_RATIO = re.compile(r"\d[\d,\.]*\s*(?:%|％|折)")
PRICE_RATIO_CTX = re.compile(r"不低于|高于|低于|均价|折扣|定价")   # 泛用的「比例」不算定价语境——「解除限售比例 40%」会冒充定价
PRICE_FOREIGN = re.compile(r"增长率|净利润|营业收入|解除限售|占比|股本总额|有效期|激励对象共?|人数")
PRICE_IMPOSTOR = re.compile(r"市价|市场价|面值|收盘价|开盘价|均价|账面净资产|账面值|净值|评估价|参考价|基准价|评标基准")   # 参照价不是授予价：数挂在这些词上就不算本项实额
PRICE_HEAD = re.compile(r"授予价格|授予价|行权价格|行权价|定价|折扣")   # 能领出一个真价的实义名词（「每股」是单位，不是所有者）
UNIT_SKIP = re.compile(r"(?:每股|每份|每一元|一元|人民币|约|为|是|即|按|暂定|最终|等|的|后|前|则|并|至|元)+\s*$")
COPULA_SEEN = re.compile(r"为|定为|即|按|暂定|是")
PRICE_VAGUE = re.compile(r"另行确定|另行约定|另行公告|另定|届时公告|届时确定|届时|由董事会确定|由股东大会确定|"
                        r"按有关规定执行|按规定执行|待定|以[^，。]{0,8}为准|尚未确定|未确定|协商确定")
DATE_SPAN = re.compile(r"\d{4}\s*(?:年|[-/.])\s*\d{1,2}\s*(?:月|[-/.])?\s*\d{1,2}\s*日?"
                       r"|\d{4}\s*年(?:\s*\d{1,2}\s*月)?(?:\s*\d{1,2}\s*日)?"
                       r"|\d{1,2}\s*月\s*\d{1,2}\s*日"
                       r"|\d{4}[-/.]\d{1,2}[-/.]\d{1,2}")
SEG_SPLIT = re.compile(r"[，。；、！？；]+|[,!](?!\s*\d)")   # 千分位逗号不断段
NOUN_WASH = re.compile(r"[员委事大东议工学协商年例常布明谈论聚汇组]会|会[计议场话晤所馆堂员]")   # 「X 会」机构名后缀（委员会·董事会·股东大会…）与「会 X」名词（会计·会议·会场·会员…）里的「会」都是名词性成分，不是判断语气——两头都按形态洗，不枚举个案
ITEM = re.compile(r"^\s*[-*]\s*(" + "|".join(map(re.escape, ITEMS)) + r")[：:]")
QUOTES = re.compile(r"[「『«]([^」』»]*)[」』»]")
ANCHOR_SPLIT = re.compile(r"锚[:：]")
ANCHOR_VAL = re.compile(r"锚[:：]\s*(\S.*)$")
BANNED = re.compile(r"行权盈亏|摊销测算|稀释比例结论|一定能行权|必能行权|稳赚|零风险|保证收益|利好|建议参与|"
                    r"代客行权|代客认购|内幕信息|绕开审议|规避审议|利益输送")
SUBJECT = re.compile(r"解锁|限售|行权|授予|摊销|摊薄|稀释|业绩考核|激励对象|股价|收入|利润|评级|目标价|利好|收益|风险|归属")
TONE = re.compile(r"应当|应予|予以|将|会|必|有望|可期|可能|足以|构成|属于|意味着|支持|成立|推翻|无效|有效|上调|下调|"
                  r"提升|下滑|增加|减少|回升|高于|低于|稳赚|赚|亏|无疑|显然|肯定|应(?!急)")
VERDICT = re.compile(r"结论|综上|因此|可见|据此|本院认为|本件认为|本卡认为|本件判断|判定|认定|断言")
EFFECT = re.compile(r"无效|有效|作废|不成立|成立|撤销|违法|违规|应予支持|予以支持|应支持|支持|必然|属实")
DISCLAIM = re.compile(r"不接|不出|不提供|不作|不判|禁止|未证|无法|不承诺")
PENDING = re.compile(r"\[待人工\]")
DECL = re.compile(r"共\s*(?:八|8)\s*项\s*[·：:|｜、]\s*缺\s*(\d+)\s*项")
EMPTY_LIE = re.compile(r"(?:^|[\s：:])无(?:该项|此项)|没有(?:该项|此项)")
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


def price_field(item: dict) -> str:
    """定价判据域＝该项自己的原句；没有书名号时退化为去掉锚段与名目前缀后的句体。"""
    if item["quotes"]:
        return " ".join(item["quotes"])
    return item["spoken"] or item["body"]


def trim_units(pre: str):
    """数左那一段先跳过单位与连接词（每股·每份·人民币·元·约·为·是·即·按·暂定·最终·后·前·的·等…），
    返回剩余左文与被跳过段里是否出现过系词——「每股」是单位不是所有者，「定为」才是谓语。"""
    rest, copula = pre, False
    while True:
        stripped = UNIT_SKIP.sub("", rest)
        if stripped == rest:
            break
        if COPULA_SEEN.search(rest[len(stripped):]):
            copula = True
        rest = stripped
    if rest.rstrip().endswith("股"):
        rest = rest.rstrip()[:-1]
    return rest, copula


def build_phrases(domain: str) -> list[dict]:
    """显式结构体：把取数域按「SEG_SPLIT 标点 ∪ PRICE_ABS 金额边界」切成**短语表**，判定只吃这张表。
    每短语＝〔数左 pre｜内金额｜数右 post〕，三列偏移各自算好：
    heads_pre∥refs_pre＝本短语内的领价名词与参照价名词（带偏移），heads_post∥refs_post＝数右那两段同理，
    left_at＝本短语起点（在它之前的全部文本是「前序」，供孤立数继承），text＝本短语全文（发红句要引它）。"""
    money = list(PRICE_ABS.finditer(domain))
    phrases: list[dict] = []
    floor = 0
    for k, m in enumerate(money):
        start = floor
        for punct in SEG_SPLIT.finditer(domain[floor:m.start()]):
            start = max(start, floor + punct.end())
        nxt_punct = len(domain)
        for punct in SEG_SPLIT.finditer(domain[m.end():]):
            nxt_punct = m.end() + punct.start()
            break
        nxt_money = money[k + 1].start() if k + 1 < len(money) else len(domain)
        end = min(nxt_punct, nxt_money)
        pre, post = domain[start:m.start()], domain[m.end():end]
        phrases.append({
            "money": m.group(0), "pre": pre, "post": post, "left_at": start,
            "text": domain[start:end].strip(), "seg": (pre + m.group(0)).strip(),
            "heads_pre": [(h.start(), h.group(0)) for h in PRICE_HEAD.finditer(pre)],
            "refs_pre": [(r.start(), r.group(0)) for r in PRICE_IMPOSTOR.finditer(pre)],
            "heads_post": [(h.start(), h.group(0)) for h in PRICE_HEAD.finditer(post)],
            "refs_post": [(r.start(), r.group(0)) for r in PRICE_IMPOSTOR.finditer(post)],
        })
        floor = m.end()
    return phrases


def price_gap(clause: str):
    """给本项定价定性：**先建短语结构体，判定以它为主**（不再在原文上挪窗、也不再补词）——
    数据源如实写在面上：短语内的名词归属吃结构体三列偏移，而孤立数继承那一步扫的是剥日期后的原串对应段
    （naked 里本短语起点之前的全部文本），比率支路同样按原串切段、不进结构体——不说「只吃结构体」这种超实话。
    ①该项原句剥日期（DATE_SPAN：公告日·发行日这类一律从取数域剔除）后交 build_phrases 切成短语表，
    每短语收一枚金额候选，带内领价·内参照·内金额三列偏移；②一枚候选归谁所有按这个次序判，只判一次：
      （甲）**本短语数左**有名词：跳过单位后最近的实义名词是领价族（授予价格·行权价格·定价·折扣）＝本项实额，合格；
            是参照族（市价·市场价·面值·均价·收盘价·开盘价·净值·账面值·账面净资产·评估价·参考价·基准价）
            且比内领价更靠数＝参照价，即剔，**哪怕同一短语别处写了「授予价格」**（「面值每股 1 元」仍归面值）；
            左文跳过单位后什么都不剩、但途中见过系词（定为·即·按·暂定…）＝谓语领出的实价，合格；
      （乙）数左什么都没有：看**本短语数右**最近的名词（「每股 12.60 元的授予价格」合格、「每股 1 元的股票面值」即剔）；
      （丙）短语内两头都没有名词＝**孤立数**（主语省略，如「最终每股 12.60 元」——「最终」是状语不是所有者）：
            **继承前序最近一次的领价名词**（跨逗号的所有权传递）；前序从头到尾只出现过参照价、一次领价都没有时
            **不继承、本数仍归参照**（防把参照洗成合格）；前序连名词都没有＝落空；
    ③比率（N%／N折）另走定价语境那条，不参与上面的名词归属：不低于·均价·折扣·定价在同段或紧邻前段收束才算，
      泛用的「比例」不算，别项语境（增长率·净利润·解除限售·占比·股本总额·有效期）同段出现即剔。
    **存在一个合格候选即过；一个都没有、又没写「未检索到」才发**——不取首数即返回，也不看逗号在哪。
    返回（被剥日期，合格段或 None，空泛语，落空候选与各自的剔除理由）。"""
    dates = [d.strip() for d in DATE_SPAN.findall(clause) if d.strip()]
    naked = DATE_SPAN.sub(" ", clause)
    vague = PRICE_VAGUE.search(naked)
    candidates: list[tuple[str, str]] = []
    for ph in build_phrases(naked):
        seg = ph["seg"]
        rest, copula = trim_units(ph["pre"])
        mh = mr = None
        for h in PRICE_HEAD.finditer(rest):
            mh = h
        for r in PRICE_IMPOSTOR.finditer(rest):
            if mr is None or r.start() > mr.start():
                mr = r
        if mr and (not mh or mr.start() > mh.end()):
            candidates.append((seg, f"数紧挨着参照价「{mr.group(0)}」（在本短语数左），那是市价·面值·均价一类的参照数，不是授予价或行权价"))
            continue
        if mh:
            return dates, seg, vague, candidates
        if copula and not mr:
            return dates, seg, vague, candidates
        r0 = ph["refs_post"][0] if ph["refs_post"] else None
        h_last = ph["heads_post"][-1] if ph["heads_post"] else None
        if r0 and (h_last is None or r0[0] < h_last[0]):
            candidates.append((seg, "数紧挨着参照价「" + r0[1] + "」（在本短语数右），不是授予价或行权价"))
            continue
        if ph["heads_post"]:
            return dates, seg, vague, candidates
        before = naked[:ph["left_at"]]
        bh = None
        for h in PRICE_HEAD.finditer(before):
            bh = h
        br = None
        for r in PRICE_IMPOSTOR.finditer(before):
            br = r
        if bh:
            return dates, seg, vague, candidates
        if br:
            candidates.append((seg, f"本短语两头都没有领价名词，前序也只出现过参照价「{br.group(0)}」，孤立数不越界继承"))
            continue
        candidates.append((seg, "数前后与本短语都没有领价的实义名词（授予价格·行权价格·定价·折扣），也没有「定为每股 N 元」这类谓语，前序同样没有所有者可继承"))
    segs = [s.strip() for s in SEG_SPLIT.split(naked)]
    for idx, s in enumerate(segs):
        if not s or not PRICE_RATIO.search(s):
            continue
        prev_ok = idx > 0 and bool(PRICE_RATIO_CTX.search(segs[idx - 1] or ""))
        if not (PRICE_RATIO_CTX.search(s) or prev_ok):
            candidates.append((s, "百分比没落在不低于·均价·折扣·定价的定价语境"))
            continue
        if not PRICE_OWN.search(s) and not PRICE_OWN.search(naked):
            candidates.append((s, "本项定价语（授予价格·行权价格·均价·定价·每股）在取数域里不出现"))
            continue
        foreign = PRICE_FOREIGN.search(s)
        if foreign:
            candidates.append((s, f"数同段出现别项语境「{foreign.group(0)}」"))
            continue
        return dates, s, vague, candidates
    return dates, None, vague, candidates


def judge_field(ln: str) -> str:
    """红线判据域＝本件自己写的话：拆字段后剥掉书名号内的草案原句与锚段，项名前缀也不进域。"""
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
            hits.append(("EIP-STRUCT", 0, f"缺段：{name}"))
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
            hits.append(("EIP-QUOTE", i + 1, f"缺项原句：{name} 那一行没有书名号内的原文"))
        elif any(core_len(q) <= 1 for q in item["quotes"]):
            hits.append(("EIP-QUOTE", i + 1, f"原句占位：{name} 那一行的书名号内为空或只剩单字"))
        mv = ANCHOR_VAL.search(ln)
        if not mv or core_len(mv.group(1)) == 0:
            hits.append(("EIP-QUOTE", i + 1, f"锚值为空：{name} 那一行的「锚：」后面没有来源定位"))
        if name == PRICE_ITEM:
            dates, ok_seg, vague, cands = price_gap(price_field(item))
            ev = ""
            if cands:
                ev = "｜有数但不合格的段：" + "∥".join(f"「{s}」＝{why}" for s, why in cands)
            if dates:
                ev += "｜剥掉的日期：" + "∥".join(dates)
            if not cands and ok_seg is None:
                ev += "｜取数域（剥日期后）首段：「" + price_field(item).strip()[:28] + "」"
            if ok_seg is None:
                if vague:
                    hits.append(("EIP-PRICE", i + 1, f"授予价格以空泛语顶替：{name} 原句剥掉日期后没有任何一段给出价格原值或定价比例，只剩「{vague.group(0)}」这类说法{ev}——别项的数与日期都不顶定价账，换同义词换不掉这一判"))
                else:
                    hits.append(("EIP-PRICE", i + 1, f"授予价格缺价格原值：{name} 原句剥掉日期后没有一段既给出「每股 N 元／N 元」或落在定价语境的「N%·N 折」，又带本项定价语（授予价格·行权价格·均价·定价·每股）{ev}——百分比要配上不低于·均价·折扣才是定价，别项的数不顶账，没取到就写「未检索到」"))
    for name in ITEMS:
        if name not in seen:
            hits.append(("EIP-STRUCT", 0, f"缺项行：{name} 在逐字速读段里没有以「- 名目：」起头的行"))
    pending_items = sum(1 for i in zone if ITEM.match(lines[i]) and "未检索到" in lines[i])
    decls = DECL.findall(text)
    if len(decls) > 1:
        hits.append(("EIP-COUNT", 0, f"齐缺申报出现 {len(decls)} 处：只准一枚，两处并存即口径不唯一"))
    elif len(decls) == 1 and int(decls[0]) != pending_items:
        hits.append(("EIP-COUNT", 0, f"齐缺申报与清单不对账：申报缺 {decls[0]} 项∥速读段实有 {pending_items} 行「未检索到」"))
    elif not decls:
        hits.append(("EIP-COUNT", 0, "头部缺「共八项·缺 N 项」申报，无从对账"))
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
                    hits.append(("EIP-LINE", i, f"红线断言词出现在没有 [待人工] 的行：本件自己写的话里有「{mb.group(0)}」——同一行前半写了免责句也不顶，豁免只到分句为止"))
                    flagged = True
                    break
                ms, mt = SUBJECT.search(seg), TONE.search(seg)
                if ms and mt:
                    hits.append(("EIP-LINE", i, f"判断式结论落在非待人工行：本件自己写的话里「{ms.group(0)}」与判断语气「{mt.group(0)}」同段出现——解锁·行权·摊销·摊薄·业绩这类判断一律留 [待人工]，草案原句（书名号内）与锚不在此列"))
                    flagged = True
                    break
            if not flagged:
                mv2, me = VERDICT.search(dom), EFFECT.search(NOUN_WASH.sub("", dom))
                if mv2 and me:
                    hits.append(("EIP-LINE", i, f"自裁效力判断落在非待人工行：本件自己写的话里裁定前缀「{mv2.group(0)}」＋效力判断「{me.group(0)}」——本次计划是否有效·程序是否违法这类裁定本件一律不自判，留 [待人工]；草案原句（书名号内）与锚不在此列"))
        if EMPTY_LIE.search(ln):
            hits.append(("EIP-COUNT", i, "把「未检索到」写成「无／没有」"))
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
    good = here / "fixtures" / "good-eip-card.md"
    bad = here / "fixtures" / "bad-eip-card.md"
    rows = []
    gt = good.read_text(encoding="utf-8")
    gh = check_text(gt)
    rows.append(("好样须过（发条 0）", not gh, f"实发 {len(gh)} 条"))
    bt = bad.read_text(encoding="utf-8")
    bh = check_text(bt)
    codes = {c for c, _, _ in bh}
    rows.append(("坏样五道齐发", {"EIP-STRUCT", "EIP-QUOTE", "EIP-LINE", "EIP-COUNT", "EIP-PRICE"} <= codes,
                 "实发码 " + "∥".join(sorted(codes))))
    tmp = make_tmp("check-eip-")
    stripped = tmp / "no-anchor.md"
    stripped.write_text(re.sub(r"锚[:：][^\n]*", "锚：", gt), encoding="utf-8")
    sh = check_text(stripped.read_text(encoding="utf-8"))
    rows.append(("反证·剥锚必发 EIP-QUOTE", any(c == "EIP-QUOTE" for c, _, _ in sh), f"实发 {len(sh)} 条"))
    nproof = 1
    pin = make_tmp("check-eip-pin-")
    ROW_PRICE = "「限制性股票授予价格为每股 12.60 元，不低于草案公告前 1 个交易日公司股票均价 25.20 元的 50%」"
    tiers = (
        ("钉阈·名目只剩散文必发 EIP-STRUCT",
         gt.replace("- 审议程序与披露义务：未检索到", "审议程序与披露义务在草案末章另有说明，未检索到", 1),
         "缺项行：审议程序与披露义务"),
        ("钉阈·书名号内单字必发 EIP-QUOTE",
         gt.replace("「本计划采取限制性股票与股票期权两种形式，标的股票来源为公司向激励对象定向发行的 A 股普通股」", "「股」", 1),
         "原句占位"),
        ("钉阈·齐缺申报改数必发 EIP-COUNT",
         gt.replace("共八项·缺 1 项", "共八项·缺 0 项", 1),
         "齐缺申报与清单不对账"),
        ("钉阈·把未检索到写成无该项必发 EIP-COUNT",
         gt.replace("- 审议程序与披露义务：未检索到（缺数清单已点名）", "- 审议程序与披露义务：无该项内容。", 1),
         "把「未检索到」写成「无／没有」"),
        ("钉阈·整段无价格原值必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「限制性股票授予价格由董事会按有关规定确定」", 1),
         "取数域（剥日期后）首段：「限制性股票授予价格由董事会"),
        ("钉阈·市价数不顶授予价必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「授予价格另行确定，市场价 30 元」", 1),
         "「市场价 30 元」＝数紧挨着参照价「市场价」"),
        ("钉阈·别项百分比顶定价账必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「授予价格为 1.20%」", 1),
         "「授予价格为 1.20%」＝百分比没落在"),
        ("钉阈·公告日期冒充价格必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「公告日期为 2026 年 4 月 1 日，授予价格另定」", 1),
         "只剩「另定」"),
        ("钉阈·届时公告族必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「授予价格届时公告」", 1),
         "只剩「届时公告」"),
        ("钉阈·协商确定族必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「授予价格由公司与激励对象协商确定」", 1),
         "只剩「协商确定」"),
        ("钉阈·别项数字搬进定价段必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「解除限售比例 40%、30%、30%，授予价格为均价」", 1),
         "「解除限售比例 40%」＝百分比没落在"),
        ("钉阈·红线定式词落在非待人工行必发 EIP-LINE",
         gt.replace("## 二、八项逐字速读", "- 结论：本计划建议参与，稳赚。\n\n## 二、八项逐字速读", 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·判断式家族一（主题＋语气）必发 EIP-LINE",
         gt.replace("## 二、八项逐字速读", "- 另：摊薄将影响每股收益。\n\n## 二、八项逐字速读", 1),
         "「摊薄」与判断语气「将」"),
        ("钉阈·判断式家族二（主题＋语气）必发 EIP-LINE",
         gt.replace("## 二、八项逐字速读", "- 另：解锁收益可期。\n\n## 二、八项逐字速读", 1),
         "「解锁」与判断语气「可期」"),
        ("钉阈·自裁效力族一必发 EIP-LINE",
         gt.replace("## 二、八项逐字速读", "- 结论：本次激励计划无效。\n\n## 二、八项逐字速读", 1),
         "裁定前缀「结论」＋效力判断「无效」"),
        ("钉阈·真判断语气（会）必发 EIP-LINE",
         gt.replace("## 二、八项逐字速读", "- 本次解锁条件会达成。\n\n## 二、八项逐字速读", 1),
         "「解锁」与判断语气「会」"),
        ("钉阈·继承不越界：本短语自归参照必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「授予价格参考股票面值 1 元，市价 5 元」", 1),
         "「市价 5 元」＝数紧挨着参照价「市价」（在本短语数左）"),
        ("钉阈·孤立数无前序领价不洗绿必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「参考市价 30 元，每股 12.60 元」", 1),
         "「每股 12.60 元」＝本短语两头都没有领价名词，前序也只出现过参照价「市价」，孤立数不越界继承"),
        ("钉阈·数后紧跟参照价必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「每股 1 元面值的股票另行确定价格」", 1),
         "＝数紧挨着参照价「面值」（在本短语数右）"),
        ("钉阈·参照价在前授予价在后仍须发必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「参考市价 30 元后授予价格另行确定」", 1),
         "「参考市价 30 元」＝数紧挨着参照价「市价」"),
        ("钉阈·单位词遮眼：面值每股 N 元必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「授予价格参考股票面值每股 1 元，最终由董事会决定」", 1),
         "「授予价格参考股票面值每股 1 元」＝数紧挨着参照价「面值」"),
        ("钉阈·单位词遮眼：市价每股 N 元必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「参考市价每股 30 元，授予价格另行确定」", 1),
         "「参考市价每股 30 元」＝数紧挨着参照价「市价」"),
        ("钉阈·市价冒充授予价必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「授予价格参考市价 30 元，最终由董事会决定」", 1),
         "「授予价格参考市价 30 元」＝数紧挨着参照价「市价」"),
        ("钉阈·面值冒充授予价必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「授予价格以股票面值 1 元为基准，实际价格待定」", 1),
         "「授予价格以股票面值 1 元」＝数紧挨着参照价「面值」"),
        ("钉阈·账面值冒充必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「授予价格按每股账面净资产 8.50 元确定」", 1),
         "「授予价格按每股账面净资产 8.50 元」＝数紧挨着参照价「账面净资产」"),
        ("钉阈·均价是参照价不是授予价必发 EIP-PRICE",
         gt.replace(ROW_PRICE, "「授予价格即前 20 个交易日均价 25.20 元」", 1),
         "＝数紧挨着参照价「均价」"),
        ("钉阈·否决式判断句必发 EIP-LINE",
         gt.replace("## 二、八项逐字速读", "- 结论：授予应予否决。\n\n## 二、八项逐字速读", 1),
         "「授予」与判断语气「应予」"),
        ("钉阈·免责句后半的真判断必发 EIP-LINE",
         gt.replace("## 二、八项逐字速读", "- 说明：本件不判名单真伪；授予一定能行权。\n\n## 二、八项逐字速读", 1),
         "本件自己写的话里有「一定能行权」"),
        ("钉阈·免责句后半的判断式必发 EIP-LINE",
         gt.replace("## 二、八项逐字速读", "- 本件不接代办；摊销会逐年上升。\n\n## 二、八项逐字速读", 1),
         "「摊销」与判断语气「会」"),
        ("钉阈·裸判断语气（会）家族必发 EIP-LINE",
         gt.replace("## 二、八项逐字速读", "- 结论：股权激励会带来收益。\n\n## 二、八项逐字速读", 1),
         "「收益」与判断语气「会」"),
        ("钉阈·自裁效力族二必发 EIP-LINE",
         gt.replace("## 二、八项逐字速读", "- 综上，本次审议程序违规。\n\n## 二、八项逐字速读", 1),
         "裁定前缀「综上」＋效力判断「违规」"),
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
    ctrls = (
        ("对照·带公告日期与括注约束的合格定价句不误伤（EIP-PRICE 零发）",
         gt.replace(ROW_PRICE, "「草案公告日期为 2026 年 4 月 1 日，限制性股票授予价格为每股 12.60 元（不低于授予价格法定下限）」", 1), "EIP-PRICE"),
        ("对照·正常说明行不误伤（EIP-LINE 零发）",
         gt.replace("## 二、八项逐字速读", "- 说明：草案另载有回购注销安排，原句见第八章。\n\n## 二、八项逐字速读", 1), "EIP-LINE"),
        ("对照·机构名里的「会」不误伤（EIP-LINE 零发）",
         gt.replace("## 二、八项逐字速读", "- 说明：激励对象名单以股东大会批准为准。\n\n## 二、八项逐字速读", 1), "EIP-LINE"),
        ("对照·会计处理说明不误伤（EIP-LINE 零发）",
         gt.replace("## 二、八项逐字速读", "- 说明：行权会计处理按草案列示。\n\n## 二、八项逐字速读", 1), "EIP-LINE"),
        ("对照·会议记录陈述不误伤（EIP-LINE 零发）",
         gt.replace("## 二、八项逐字速读", "- 说明：会议记录载明考核条款见第六章。\n\n## 二、八项逐字速读", 1), "EIP-LINE"),
        ("对照·面值每股在前、合格价在后不误伤（EIP-PRICE 零发）",
         gt.replace(ROW_PRICE, "「授予价格参考股票面值每股 1 元，最终定为每股 12.60 元」", 1), "EIP-PRICE"),
        ("对照·主语省略的授予价不误伤（EIP-PRICE 零发·R4-1）",
         gt.replace(ROW_PRICE, "「授予价格参考面值 1 元，最终每股 12.60 元」", 1), "EIP-PRICE"),
        ("对照·状语非系词跨逗号不误伤（EIP-PRICE 零发·R4-1 同族）",
         gt.replace(ROW_PRICE, "「授予价格参考股票面值 1 元，最终由董事会决定每股 12.60 元」", 1), "EIP-PRICE"),
        ("对照·均价在前而领价在场不误伤（EIP-PRICE 零发）",
         gt.replace(ROW_PRICE, "「授予价格不低于草案公告前 20 个交易日均价，最终每股 12.60 元」", 1), "EIP-PRICE"),
        ("对照·数右有领价名词不误伤（EIP-PRICE 零发）",
         gt.replace(ROW_PRICE, "「每股 12.60 元的授予价格」", 1), "EIP-PRICE"),
        ("对照·参照价之后另有合格授予价不误伤（EIP-PRICE 零发）",
         gt.replace(ROW_PRICE, "「授予价格参考面值 1 元后最终定为每股 12.60 元」", 1), "EIP-PRICE"),
        ("对照·同上形加逗号也不误伤（EIP-PRICE 零发）",
         gt.replace(ROW_PRICE, "「授予价格参考面值 1 元，后最终定为每股 12.60 元」", 1), "EIP-PRICE"),
        ("对照·合格价在前参照价在后不误伤（EIP-PRICE 零发）",
         gt.replace(ROW_PRICE, "「授予价格为每股 12.60 元，参考面值 1 元」", 1), "EIP-PRICE"),
        ("对照·每股金额带下限括注不误伤（EIP-PRICE 零发）",
         gt.replace(ROW_PRICE, "「授予价格为每股 12.60 元（不低于法定下限）」", 1), "EIP-PRICE"),
        ("对照·考核委员会陈述句不误伤（EIP-LINE 零发）",
         gt.replace("## 二、八项逐字速读", "- 说明：本次授予由薪酬与考核委员会核实。\n\n## 二、八项逐字速读", 1), "EIP-LINE"),
        ("对照·委员会拟定行权价不误伤（EIP-LINE 零发）",
         gt.replace("## 二、八项逐字速读", "- 说明：行权价格调整方案由委员会拟定。\n\n## 二、八项逐字速读", 1), "EIP-LINE"),
        ("对照·草案原句里的判断措辞不误伤（EIP-LINE 零发）",
         gt.replace("「以 2025 年净利润为基数，2026 年、2027 年、2028 年净利润增长率分别不低于 30%、60%、100%；个人绩效考核结果为 B 及以上方可解除限售」",
                    "「公司层面业绩考核不达标的，当期股份不得解锁，由公司按授予价格回购注销」", 1), "EIP-LINE"),
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
    leftover = sorted(q.name for q in root.iterdir() if q.name.startswith("check-eip-")) if root.is_dir() else []
    rows.append(("临时根自清（跑后不增）", not leftover,
                 f"本次建 {len(made)} 枚·跑后残留 {len(leftover)} 枚"))
    bad_rows = [r for r in rows if not r[1]]
    for name, ok, detail in rows:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}｜{detail}")
    print(f"selftest: {'ALL GREEN' if not bad_rows else 'FAIL'}（好样 1 枚·坏样五道·反例 {nproof} 枚·临时根 {len(TMP_ROOTS)} 枚自清）")
    return 0 if not bad_rows else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="A股股权激励计划条款卡五道机检（零网络）")
    ap.add_argument("target", nargs="?", help="待检文件（本件不读网络、不读目录）")
    ap.add_argument("--selftest", action="store_true", help="好样须过、坏样五道齐发、钉阈按整族各钉一档、对照样不误伤、临时件自清")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.target:
        print("用法：check_eip_card.py <待检文件> | --selftest", file=sys.stderr)
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
