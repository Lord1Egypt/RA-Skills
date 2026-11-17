#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_esop_card.py — A股员工持股计划条款卡的机检（零网络、只读传入文件）。

五道码（缺一即不叫过闸）：
  ES-STRUCT 五段齐：头部申报／八项逐字速读／口径对照／缺数清单／待人工，任一节缺失即发；
             八项名目另须在「逐字速读」段内**行级在场**——每枚名目一行以「- 名目：」起头，只在散文里提到不算占行；
  ES-QUOTE  每项原句与锚：项行的书名号（「」『』«»）内原句不得为空或只剩单字；「锚：」标签在而锚值为空同样发；
  ES-LINE   红线断言三道：①定式禁词，含三支**按词族收**的断言——方案类评价（方案·受让价格·购买价格·转让价格·
             认购价格·折价·折扣·力度·覆盖·持股计划·员工持股 × 合理·公允·偏低·偏高·充分·不足·优惠，插语
             「很·较为·基本·大体·相当」不构成豁免；名词后缀「性·度·论」是说明对象不是断言）、解锁类预测
             （解锁·行权·达标·考核·获批·通过·实施·过户 × 概率·可能性 × 大·高·小·低）与税务判断
             （应缴·需缴·免征·可递延·适用 × 个人所得税·个税·纳税；税负为·节税·避税·税务筹划·税收筹划·
             个税测算），另加是否划算／值得参与／建议参与／建议认购／稳赚／零风险／保证收益／利好／必涨／套利／
             代拟／代算／代客／内幕信息／绕开审议／规避披露／损害员工利益／损害股东利益；
             ②判断式规则——项行拆字段后，红线判据域只取本件自己写的话（剥掉书名号内的公告原句与锚），主题词
             （员工持股·持股计划·受让价格·购买价格·资金来源·股票来源·存续期·锁定期·解锁·考核·持有人·
             管理委员会·份额·规模·方案·员工·股东·股价·收益·税·过户·回购）与判断语气同段出现即发；
             ③自裁效力层：裁定前缀（结论／综上／因此／本件认为／判定／认定…）与效力判断（无效／有效／成立／
             不成立／违法／违规／属实…）同现即发。`[待人工]` 标记与免责句都**只登记自己那一分句**（按分号·句号·
             逗号 cut 后逐段判），同一行后半写的肯定预测照发；机构名「X 会」与「会 X」名词里的「会」先按形态从
             语气域洗掉（持有人会议·管理委员会·董事会·股东会·薪酬与考核委员会都不误红）；
  ES-COUNT  齐缺申报恰一枚：头部「共八项·缺 N 项」只准出现一处（两处并存即发），且 N 必须等于速读段里「未检索到」的
             项行数；把「未检索到」写成「无该项／没有此项」一律发；
  ES-VALUE  两格数字归属（资金来源／受让价格与规模）**以短语结构体为主**判，不按词表也不按位置：
             ①项行拆字段，判据域只取该项自己的原句；②先剥日期（草案公布日、过户日、公告日这类一律剔除，
             「2026 年 11 月 6 日」不是价格）；③取数域按「SEG_SPLIT 标点 ∪ NUM 数字边界」切成短语表，每短语带
             内本格名词（含元素序号）·内参照数名词·内候选三列偏移，一枚候选只在本短语内定档——数左跳过单位与
             连接词后最近的实义名词属本元素名词族才算合格，属参照数族（交易均价·收盘价·面值·每股净资产·股本总额·
             总股本·每份份额·份额面值·授予价格·行权价格…）且更靠数即剔，**哪怕同一短语别处写了本格名词**；
             数左什么都不剩时看本短语数右；两头都没有名词＝孤立数才继承前序最近一次的本格名词，**前序最近的若是
             参照数则不继承**；④每格两元素各自要有落点——「X 与 Y」是两组同时给，一枚合格候选只算它那一个要素
             到位、不替整组放行；**本域不设共指补判**：两格的元素量纲都不同（受让价格是元/股、标的股票数量是股；
             资金来源是安排用词、资金总额是金额），一枚数在结构上不可能同时满足两个元素，所以姊妹尺里那条
             「肯定系词共指」的分支在本域没有适用面，不搬过来；⑤kind="term" 的元素
             （资金来源）认它自己的安排用词、不要求金额，但与 num 元素一样判空泛语：用词与「待定·另行确定·届时·
             协商确定」同在一句时不算读到；⑥比率（占比·比例·上浮）与期限（N 个月）**不参与名词归属**，只在原句里
             逐字登记，缺了走「未检索到」。
             射程如实写（首版就写、不等被问）：判的是同一短语内的相邻关系加一次跨短语继承与共指补判，
             **不声称覆盖所有自然语言的归属表达**；同位式共指（系词在两个名词之后，如「受让价格与标的股票数量
             均为 17.35 元/股」）与「价格待定但数量已定」的同段共存式都在已知覆盖不到之列，按严格式发红，
             请人工回原句核对；短语内定档吃结构体三列偏移，孤立数继承与空泛语扫描那两步读的是剥日期后的原串
             对应段，不是结构体本身。发红句把被剥的日期、落空候选、缺的要素与取数域首段一并点名当证据。

用法：
  python3 -B scripts/check_esop_card.py <待检文件>      # 逐条发红，全过则 PASS
  python3 -B scripts/check_esop_card.py --selftest      # 好样须过、坏样五道齐发、钉阈按整族各钉一档、对照样不误伤、临时件自清
  python3 -B scripts/check_esop_card.py --help
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

ITEMS = ("计划名称与期次", "参加对象与确定标准", "资金来源", "股票来源", "受让价格与规模",
         "存续期与锁定期", "管理模式与持有人会议", "变更终止与权益处置")

# 参照数族（外族）：本域里能冒充「受让价格」与「标的股票数量」的数——行情与股本类、份额与面值类、别套计划的价。
# 这一族是本域最要紧的一格：员工持股的受让价常写成「不低于交易均价的 50%」，均价与 50% 都在同一句里，
# 不按短语结构体判就会把均价当受让价、把比例当价格。
REF_ESOP = (r"交易均价|成交均价|收盘价|开盘价|最高价|最低价|股票面值|面值|每股净资产|净资产|"
            r"股本总额|总股本|已发行股份|注册资本|市值|总市值|流通市值|"
            r"每份份额|份额面值|份额净值|单位份额|授予价格|行权价格|限制性股票|股票期权")
REF_PRICE = (r"前\s*\d{1,3}\s*个?交易日[^，。；]{0,8}(?:均价|价格)|"
             r"\d{1,3}\s*个?交易日的?[^，。；]{0,6}(?:均价|价格)|"
             r"草案公布前[^，。；]{0,10}(?:均价|价格)|定价基准日[^，。；]{0,8}(?:均价|价格)|"
             r"占[^，。；]{0,12}(?:比例|比重)")
REF_QTY = (r"占[^，。；]{0,12}(?:比例|比重)|累计不超过[^，。；]{0,10}股本总额|"
           r"全部在有效期内的?员工持股计划[^，。；]{0,12}(?:总数|累计)")

# 两格数字归属（面文里那两个「与」各自的名字）：每格两元素，共用同一台结构体机器。
# kind="num" 的元素要有属于自己的合格候选；kind="term" 的元素要原句里有它自己的安排用词、且同句不带空泛语。
# 一元素判档时，外族＝本格参照数 ∪ 别格元素的名词；同格两元素之间不互为参照数。
NUM_CELLS = {
    "资金来源": {
        "foreign": re.compile(REF_ESOP),
        "elements": (
            ("资金来源", "term", re.compile(r"资金来源|自筹资金|合法薪酬|员工薪酬|奖励基金|专项奖励基金|"
                                            r"员工借款|股东借款|向第三方借款|法律法规允许的其他方式|"
                                            r"公司提取的|持股计划专项资金")),
            ("资金总额", "num", re.compile(r"资金总额|筹集资金总额|认购资金总额|资金规模|总额上限|"
                                           r"拟筹集资金|募集资金总额|资金总额上限")),
        ),
    },
    "受让价格与规模": {
        "foreign": re.compile(REF_ESOP + "|" + REF_PRICE + "|" + REF_QTY),
        "elements": (
            ("受让价格", "num", re.compile(r"受让价格|购买价格|转让价格|认购价格|购买股票的价格|受让股份的价格|"
                                           r"每股价格|每股受让价格|每股购买价格|受让单价|购买单价|"
                                           # 真实公告会在名词中间插括注（恒铭达「购买股票（含预留部分）的价格」）：
                                           # 括注是限定语不是断句，名词族要跨得过去，否则真实原句整格判缺
                                           r"购买股票(?:（[^）]{0,12}）|\([^)]{0,12}\))的?价格|"
                                           r"受让股份(?:（[^）]{0,12}）|\([^)]{0,12}\))的?价格|"
                                           r"受让价格(?:（[^）]{0,12}）|\([^)]{0,12}\))|"
                                           r"购买价格(?:（[^）]{0,12}）|\([^)]{0,12}\))")),
            ("标的股票数量", "num", re.compile(r"标的股票数量|标的股份数量|持股数量|股票数量|股份数量|"
                                               r"受让股份数量|购买股份数量|计划规模|持股规模|标的股票总数|"
                                               # 真实公告的写法（工业富联「标的股票上限」、宁德时代「标的股票规模」、
                                               # 金达威「认购的股数上限」）：数量那一格不只有「数量」一种叫法
                                               r"标的股票上限|标的股份上限|标的股票规模|标的股份规模|"
                                               r"股票上限|股份上限|股数上限|认购的股数|受让的股数")),
        ),
    },
}
# 候选形制：金额（元·万元·亿元）∪ 股数（股·万股·亿股）∪ 倍数（倍）∪ 百分比（%·％）。
# 只有带金额或股数量纲的候选才能结算元素；倍·%·％＝比率，只逐字登记（「不低于均价的 50%」里的 50% 不是价格）。
NUM = re.compile(r"\d[\d,\.]*\s*(?:万股|亿股|万元|亿元|元|股|倍|％|%)")
SETTLE_UNIT = re.compile(r"(?:万股|亿股|万元|亿元|元|股)\s*$")
RATIO_MARK = re.compile(r"(?:占比|比例|上浮|增幅|降幅|下降|增长|比重|折扣|折价|溢价)\s*[^，。；\d]{0,6}$")
DATE_SPAN = re.compile(r"\d{4}\s*(?:年|[-/.])\s*\d{1,2}\s*(?:月|[-/.])?\s*\d{1,2}\s*日?"
                       r"|\d{4}\s*年(?:\s*\d{1,2}\s*月)?(?:\s*\d{1,2}\s*日)?"
                       r"|\d{1,2}\s*月\s*\d{1,2}\s*日"
                       r"|\d{4}[-/.]\d{1,2}[-/.]\d{1,2}")
VAGUE = re.compile(r"另行确定|另行约定|另行协商|另行签订|另定|届时公告|届时披露|届时确定|届时|待定|尚未确定|未确定|未定|"
                   r"由[^，。；]{0,8}协商|协商确定|以[^，。；]{0,12}为准|尚需|有待|待[^，。]{0,6}出具|"
                   r"按有关规定执行|按规定执行|详见[^，。]{0,8}公告|视[^，。]{0,8}而定|"
                   r"以最终签[^，。；]{0,8}为准|按实际[^，。；]{0,6}确定|据实确定|以[^，。；]{0,8}结果为准")
UNIT_SKIP = re.compile(r"(?:每股|每份|每一元|人民币|约|为|是|即|按|暂定|最终|合计|总计|分别|不低于|不超过|不高于|"
                       r"高于|低于|占|比例|占比|其中|含|部分|等|的|后|前|则|并|至|以及|万股|亿股|万元|亿元|股|元|万|亿)+"
                       r"\s*$")
COPA_REF = re.compile(r"即为|均为|都是|等于|即|为|是")
SEG_SPLIT = re.compile(r"[，。；：！？]+|[,;](?!\s*\d)")   # 千分位逗号不断段；顿号算枚举不算归属边界
NOUN_WASH = re.compile(r"[员委事大东议工学协商年例常布明谈论聚汇组独立]会|会[计议场话晤所馆堂员]")
# 八项名目按「任一表述命中即算在场」认（lead 批单第二条限度）：真实公告里同一项有不同叫法——
# 恒铭达那份把「参加对象」写成「持有人」，工业富联那份把「受让价格」写成「购买价格」。
# 所以名目不是一枚死字符串，是一族别名；命中任一别名即归到同一枚 canonical 名目上，
# 行级在场、齐缺对账、缺项点名三处都按 canonical 名走，卡面写哪个别名都认。
ITEM_ALIASES = {
    "计划名称与期次": ("计划名称与期次", "计划名称及期次", "计划名称", "计划期次", "名称与期次", "计划全称"),
    "参加对象与确定标准": ("参加对象与确定标准", "参加对象及确定标准", "参加对象", "持有人范围与确定标准",
                          "持有人与确定标准", "持有人范围", "参加对象范围",
                          # 真实草案的章节标题写法（第三章）：写卡人照抄标题时也得认
                          "持有人的确定依据与范围", "持有人的确定依据及范围", "持有人确定依据及范围",
                          "持有人的确定依据、范围及份额分配情况"),
    "资金来源": ("资金来源", "认购资金来源"),
    "股票来源": ("股票来源", "股份来源", "标的股票来源"),
    "受让价格与规模": ("受让价格与规模", "购买价格与规模", "受让价格及规模", "购买价格及规模",
                       "受让价格和规模", "价格和规模", "规模和购买价格",
                       "受让价格", "购买价格", "受让价格与持股规模"),
    "存续期与锁定期": ("存续期与锁定期", "存续期、锁定期", "存续期、锁定期和业绩考核",
                       "存续期、锁定期、考核设置", "存续期与锁定期及考核",
                       "存续期", "锁定期", "存续期与解锁安排"),
    "管理模式与持有人会议": ("管理模式与持有人会议", "管理机构及管理模式", "管理模式及管理机构",
                             "持有人会议与管理模式", "管理模式", "持有人会议"),
    "变更终止与权益处置": ("变更终止与权益处置", "变更、终止及持有人权益的处置", "变更、终止及权益处置",
                           "变更、终止及持有人权益的处置办法", "变更终止及权益处置", "变更、终止与权益处置",
                           "变更与终止", "权益处置", "变更终止"),
}
_ALIAS_PAIRS = sorted(((a, c) for c, al in ITEM_ALIASES.items() for a in al),
                      key=lambda p: -len(p[0]))
_ALIAS_TO_CANON = dict(_ALIAS_PAIRS)
ITEM = re.compile(r"^\s*[-*]\s*(" + "|".join(map(re.escape, [a for a, _ in _ALIAS_PAIRS])) + r")[：:]")
QUOTES = re.compile(r"[「『«]([^」』»]*)[」』»]")
ANCHOR_SPLIT = re.compile(r"锚[:：]")
ANCHOR_VAL = re.compile(r"锚[:：]\s*(\S.*)$")
DECL = re.compile(r"共\s*(?:八|8)\s*项\s*[·：:|｜、]\s*缺\s*(\d+)\s*项")
EMPTY_LIE = re.compile(r"(?:^|[\s：:])无(?:该项|此项)|没有(?:该项|此项)")
CORE_STRIP = re.compile(r"[\s　「」『』«»“”（）()《》【】，,。.；;：:、！!？~\-—_·/％%*#]+")
SECTIONS = (("头部申报", r"头部申报"), ("八项逐字速读", r"逐字速读|八项速读"),
            ("口径对照", r"口径对照"), ("缺数清单", r"缺数清单"), ("待人工", r"待人工"))
SPEED_HEAD = re.compile(r"^#{1,4}.*(?:逐字速读|八项速读)")
ANY_HEAD = re.compile(r"^#{1,4}\s")


def canon(name: str) -> str:
    """别名归一到 canonical 名目——卡面写「购买价格与规模」与写「受让价格与规模」是同一项。"""
    return _ALIAS_TO_CANON.get(name, name)


def core_len(s: str) -> int:
    return len(CORE_STRIP.sub("", s))


def parse_item_line(ln: str):
    """项行拆成字段：名目（已归一）／书名号原句／锚／原句外句体——判定按字段来，不按整行。"""
    m = ITEM.match(ln)
    if not m:
        return None
    name = canon(m.group(1))
    body = ln[m.end():]
    anchor = ""
    ma = ANCHOR_SPLIT.search(body)
    if ma:
        anchor = body[ma.end():].strip()
        body = body[:ma.start()]
    quotes = QUOTES.findall(body)
    spoken = QUOTES.sub(" ", body).strip()
    return {"name": name, "quotes": quotes, "anchor": anchor, "spoken": spoken, "body": body.strip()}


def value_field(item: dict) -> str:
    """数字归属判据域＝该项自己的原句；没有书名号时退化为去掉锚段与名目前缀后的句体。"""
    if item["quotes"]:
        return " ".join(item["quotes"])
    return item["spoken"] or item["body"]


def segments_of(domain: str) -> list[tuple[int, str]]:
    """按 SEG_SPLIT 把取数域切成〔起点，句段〕表——term 元素要判的是「同一个句段里有没有空泛语」。"""
    out, cur = [], 0
    for m in SEG_SPLIT.finditer(domain):
        out.append((cur, domain[cur:m.start()]))
        cur = m.end()
    out.append((cur, domain[cur:]))
    return out


def seg_of(bounds: list[tuple[int, str]], pos: int) -> tuple[int, str]:
    """给定域内位置，返回它所在的句段（term 命中点用它定位）。"""
    last = bounds[-1] if bounds else (0, "")
    for start, text in bounds:
        if pos <= start + len(text):
            return start, text
    return last


def trim_units(pre: str):
    """数左那一段先跳过单位与连接词（每股·合计·约·为·即·按·不低于·占·比例·元·股…），
    返回剩余左文与途中是否见过谓语词——「每股」是单位不是所有者，「确定为」才是谓语。"""
    rest, copula = pre, False
    while True:
        stripped = UNIT_SKIP.sub("", rest)
        if stripped == rest:
            break
        if COPA_REF.search(rest[len(stripped):]):
            copula = True
        rest = stripped
    return rest, copula


def build_phrases(domain: str, own_list: list, foreign: re.Pattern) -> list[dict]:
    """显式结构体：把取数域按「SEG_SPLIT 标点 ∪ NUM 数字边界」切成短语表。
    每短语＝〔数左｜本短语收的那枚候选｜数右〕，三列偏移＝内本格名词（带元素序号）·内参照数名词·内候选，各自带偏移位；
    候选形制＝金额（元·万元·亿元）∪股数（股·万股·亿股）∪倍数（倍）∪百分比（%·％），但 settle 列把后两支标成比率：
             比率（%·倍·占比·上浮一类的说法）只逐字登记、不结算任何元素。
    own_all 是整条短语里（数左＋数＋数右）所有本格名词的偏移与元素序号——共指判据要看整条短语，不只看数左。"""
    nums = list(NUM.finditer(domain))
    phrases: list[dict] = []
    floor = 0
    for k, m in enumerate(nums):
        start = floor
        for punct in SEG_SPLIT.finditer(domain[floor:m.start()]):
            start = max(start, floor + punct.end())
        nxt_punct = len(domain)
        for punct in SEG_SPLIT.finditer(domain[m.end():]):
            nxt_punct = m.end() + punct.start()
            break
        nxt_num = nums[k + 1].start() if k + 1 < len(nums) else len(domain)
        end = min(nxt_punct, nxt_num)
        pre, post = domain[start:m.start()], domain[m.end():end]
        text = domain[start:end]
        own_pre, own_post, own_all = [], [], []
        for idx, rx in enumerate(own_list):
            for h in rx.finditer(pre):
                own_pre.append((h.start(), h.end(), idx, h.group(0)))
            for h in rx.finditer(post):
                own_post.append((h.start(), h.end(), idx, h.group(0)))
            for h in rx.finditer(text):
                own_all.append((h.start(), h.end(), idx, h.group(0)))
        phrases.append({
            "num": m.group(0), "pre": pre, "post": post, "left_at": start, "text": text,
            "seg": (pre + m.group(0)).strip(), "settle": bool(SETTLE_UNIT.search(m.group(0))),
            "own_pre": own_pre, "own_post": own_post, "own_all": own_all,
            "for_pre": [(r.start(), r.end(), r.group(0)) for r in foreign.finditer(pre)],
            "for_post": [(r.start(), r.end(), r.group(0)) for r in foreign.finditer(post)],
            "won": None,
        })
        floor = m.end()
    return phrases


def value_gap(clause: str, spec: dict):
    """给一格的两个元素定档（**以短语结构体为主**，射程写在顶条，不自称覆盖所有归属表达）：
    ①剥日期；②build_phrases 切短语表，每短语一枚候选、三列偏移里本格名词带元素序号；③候选归谁按这个次序判一次：
      （甲）本短语数左——跳过单位与连接词后最近的实义名词：参照数与本格名词比位置，参照更靠数（或与本格同位）即剔，
            否则本格名词属哪个元素，这枚候选就满足哪个元素；
      （乙）数左什么都没有：看本短语数右最近的名词（参照更近即剔，本格更近则满足该元素）；
      （丙）两头都空＝孤立数（主语省略）：从前序取最近的一个本格名词继承，**但前序最近的若是参照数则不继承**
            （这一条比姊妹尺严：本域里「不低于交易均价的 50%，为 16.24 元/股」这类句子，前序最近的名词是均价，
             继承过去就把均价当成了受让价）；
      （丁）谓语（确定为·即·按…）领出而没踩到参照数时，按（丙）走继承，不单独放行；
    ④**本域不设共指补判**：两格的元素量纲都不同（受让价格是元/股、标的股票数量是股；资金来源是安排用词、
      资金总额是金额），一枚数在结构上不可能同时满足两个元素，所以姊妹尺里那条「肯定系词共指」的分支在本域
      没有适用面，不搬过来——「受让价格与标的股票数量均为 17.35 元/股」照发，属已知覆盖不到；
    ⑤kind="term" 的元素（资金来源）认它自己的安排用词、不要求金额，但与 num 元素一样判空泛语：用词与「待定·另行确定·
      届时·协商确定」同在一句时只说还没定，不算该元素读到，落进落空清单；
    ⑥逐元素判：每个元素各自要有落点，缺任一元素又没写「未检索到」才发。返回（被剥日期，缺的要素列表，空泛语，落空候选与理由）。"""
    dates = [d.strip() for d in DATE_SPAN.findall(clause) if d.strip()]
    naked = DATE_SPAN.sub(" ", clause)
    vague = VAGUE.search(naked)
    candidates: list[tuple[str, str]] = []
    elems = list(spec["elements"])
    own_list = [rx for (_, _, rx) in elems]
    foreign = spec["foreign"]
    satisfied: dict[int, str] = {}
    seg_bounds = segments_of(naked)
    for i, (ename, kind, rx) in enumerate(elems):
        if kind != "term":
            continue
        got = None
        for mm in rx.finditer(naked):
            _, seg_text = seg_of(seg_bounds, mm.start())
            v = VAGUE.search(seg_text)
            if v:
                candidates.append((seg_text.strip()[:44], "安排用词「" + mm.group(0) + "」与空泛语「" + v.group(0)
                                   + "」在同一句里——那句只说资金来源还没定，不算安排读到"))
                continue
            got = mm.group(0)
            break
        if got:
            satisfied[i] = ename + "（安排用词「" + got + "」在场、同句无空泛语）"
    phrases = build_phrases(naked, own_list, foreign)
    for ph in phrases:
        seg = ph["seg"]
        if not ph["settle"]:
            candidates.append((seg, "「" + ph["num"].strip() + "」是比率或倍数（%·％·倍一类的量纲），不是金额也不是股数——"
                                    "面文写的「比率与期限不参与归属」在这一条：比率只逐字登记，不结算任何元素"))
            continue
        rmark = RATIO_MARK.search(ph["pre"])
        if rmark:
            candidates.append((seg, "数前紧挨着比率词「" + rmark.group(0).strip() + "」——那句给的是占比·上浮·不低于一类的"
                                    "比率说法，不是本元素的原值；比率只逐字登记，不结算任何元素"))
            continue
        rest, copula = trim_units(ph["pre"])
        hits = []
        for idx, rx in enumerate(own_list):
            last = None
            for mm in rx.finditer(rest):
                last = mm
            if last:
                hits.append((last.start(), last.end(), idx, last.group(0)))
        near = max(hits, key=lambda x: (x[0], x[1])) if hits else None
        fr = None
        for rr in foreign.finditer(rest):     # 与本格名词同坐标系：都在跳过单位后的左文里量
            if fr is None or rr.start() >= fr[0]:
                fr = (rr.start(), rr.group(0))
        if fr and (near is None or fr[0] >= near[1]):
            candidates.append((seg, "数紧挨着参照数「" + fr[1] + "」（在本短语数左），那是交易均价·收盘价·面值·"
                                    "每股净资产·股本总额·每份份额一类的参照数，或同格别元素自己的数，不是本元素要的原值"))
            continue
        if near:
            satisfied[near[2]] = near[3]
            ph["won"] = near[2]
            continue
        own_r = min(ph["own_post"], key=lambda x: x[0]) if ph["own_post"] else None
        fr_r = min(ph["for_post"], key=lambda x: x[0]) if ph["for_post"] else None
        if fr_r and (own_r is None or fr_r[0] <= own_r[0]):
            candidates.append((seg, "数紧挨着参照数「" + fr_r[2] + "」（在本短语数右），不是本元素原值"))
            continue
        if own_r:
            satisfied[own_r[2]] = own_r[3]
            ph["won"] = own_r[2]
            continue
        before = naked[:ph["left_at"]]
        inh = None
        for idx, rx in enumerate(own_list):
            last = None
            for mm in rx.finditer(before):
                last = mm
            if last and (inh is None or last.start() >= inh[0]):
                inh = (last.start(), last.group(0), idx)
        frb = None
        for rr in foreign.finditer(before):
            if frb is None or rr.start() >= frb[0]:
                frb = (rr.start(), rr.group(0))
        if inh and (frb is None or inh[0] > frb[0]):
            satisfied[inh[2]] = inh[1] + "（孤立数继承前序）"
            ph["won"] = inh[2]
            continue
        if frb:
            candidates.append((seg, "本短语两头都没有本格名词，前序最近的是参照数「" + frb[1] + "」，孤立数不越界继承"))
            continue
        candidates.append((seg, "数前后与本短语都没有本格名词（受让价格·标的股票数量·资金总额一类的），"
                                "也没有「确定为每股 N 元」这类谓语，前序同样没有所有者可继承"))
    missing = [(ename, ("安排用词要么没出现、要么与空泛语同句（待定·另行确定·届时·协商确定一类），不算这一元素读到"
                        if kind == "term" else "没有属于本元素的合格候选（参照数与别元素的数都不顶账）"))
               for i, (ename, kind, rx) in enumerate(elems) if i not in satisfied]
    return dates, missing, vague, candidates


# 评价断言族与预测断言族按词族收：被评价的名词 × 插语（可有可无）× 评价词；预测动作 × 概率名词 × 程度词。
# 插语不构成豁免——「方案很合理」「方案基本公允」与「方案合理」同判；「解锁可能性极低」与「解锁概率大」同判。
NOUN_FORM = r"(?![性度论])"   # 名词形豁免只写这一处：性·度·论三种后缀都是被说明的对象，不是本件自己下的评价断言
VALUER_WORDS = "|".join(w + NOUN_FORM for w in ("合理", "公允", "偏低", "偏高", "充分", "不足", "优惠", "划算"))
DEGREE_WORDS = r"很|较为|比较|基本|大体|显然|明显|相当"
VALUER_ASSERT = (r"(?:方案|受让价格|购买价格|转让价格|认购价格|折价|折扣|力度|覆盖|持股计划|员工持股|"
                 r"考核指标|业绩目标|解锁条件)(?:的)?(?:" + DEGREE_WORDS + r")?(?:" + VALUER_WORDS + r")")
PREDICT_ASSERT = (r"(?:解锁|行权|达标|考核|获批|通过审核|审核通过|过会|通过|实施|过户|认购)(?:的)?"
                  r"(?:概率|可能性|几率)(?:很|非常|比|较|极)?(?:大|高|小|低|不大|不高|极低)")
# 税务判断是本域**独有**的一支红线（lead 批单第三条）：员工持股的税务处理（个税、递延纳税、税负）属人工与税务位，
# 本件只登记公告里写了什么，不判该缴多少、能不能递延、怎么筹划。
TAX_ASSERT = (r"(?:应缴|需缴|须缴|免征|可递延|适用)[^，。；]{0,8}(?:个人所得税|个税|纳税)|"
              r"税负(?:为|约|是)|节税|避税|税务筹划|税收筹划|个税测算|递延纳税(?:可以|可行|成立)")
BANNED = re.compile(r"是否划算|值得参与|建议参与|建议认购|建议买入|建议卖出|稳赚|零风险|保证收益|利好|必涨|套利|"
                    r"内幕信息|绕开审议|绕开审批|规避披露|代客申报|代客投票|代拟|代算|代客|"
                    r"损害员工利益|损害股东利益|侵占公司利益|"
                    + VALUER_ASSERT + r"|" + PREDICT_ASSERT + r"|" + TAX_ASSERT)
SUBJECT = re.compile(r"员工持股|持股计划|受让价格|购买价格|资金来源|股票来源|存续期|锁定期|解锁|考核|持有人|"
                     r"管理委员会|份额|规模|方案|员工|股东|股价|收益|税|过户|回购|业绩")
# 同一份词族喂给两支：BANNED 认整句断言，主题×语气这一支认「名词与评价词被别的话隔开」的写法——排除式只写一次
TONE = re.compile(r"应当|应予|予以|将|会|必|有望|可期|可能|足以|构成|属于|意味着|支持|成立|推翻|无效|有效|上调|下调|"
                  r"提升|下滑|增加|减少|回升|高于|低于|稳赚|赚|亏|无疑|显然|肯定|应(?!急)|"
                  + VALUER_WORDS + r"|" + PREDICT_ASSERT)
VERDICT = re.compile(r"结论|综上|因此|可见|据此|本院认为|本件认为|本卡认为|本件判断|判定|认定|断言")
# 书名号豁免＝**白名单准入**，不是黑名单排除（作者口吻是开放集，黑名单补不完）。准入条件四条，缺一不给豁免：
#   ①该行有锚（「原句逐字＋锚」是豁免的入场券）；
#   ②书名号之外只剩**引用标签**——源名词（公告·草案·计划·决议…）／报道动词（载明·披露·约定·称·据·见…）／
#     定位词（第 N 节·页·行）／引述标记（原文·摘录·引用·节选·摘自…），或干脆是空的。剥完还剩任何字＝本件自己写的，
#     书名号里的字照进判据域。**说明·注不在白名单**：它们是本件自述标签，不是引用标签；
#   ③书名号内以「短标签：」起头时，那个标签同样得是引用标签——「我们判断：…」「本件结论：…」塞进书名号照发，
#     「发行人：某股份有限公司」这类原文登记照旧豁免；
#   ④书名号内**任意位置**不得出现本件自称（本件·本卡·本速读·笔者）——公告原文里不可能出现写卡人对自己这份卡的
#     称呼，所以这一形不是「引文不可核验」的取舍面，是结构上必然是本件自己写的字。③管「带冒号的标签」，
#     ④管「不带冒号的自称」，两者是并集不是替代。**「本公司」「本计划」「本员工持股计划」不在表内**——
#     它们是公告主体与计划自身的自称，原文里真会出现（「本员工持股计划由公司自行管理」），收进来就误伤一片。
CITE_LABEL = re.compile(
    r"原文|摘录|引用|节选|摘自|引自|转引|照录|"
    r"载明|列明|记载|披露|约定|规定|显示|表明|称|据|见|详见|"
    r"草案|计划|公告|报告书|说明书|决议|预案|合同|章程|公示|办法|指引|指导意见|"
    r"核查意见|督导意见|审计报告|评估报告|董事会决议|股东大会决议|股东会决议|"
    r"第[一二三四五六七八九十百零\d]+[节条章项款页行段]|页|行|段")
LABEL_PUNCT = re.compile(r"[\s　（）()【】\[\]：:，,。.、·\-—_/｜|]+")
INNER_LABEL = re.compile(r"^\s*([^，。；：:]{1,12})[：:]")
# 本件自称：写卡人对自己这份卡的称呼，公告原文里不可能出现。**不含「本公司」「本计划」「本员工持股计划」**。
# **按位置认，不按子串认**：`样本件`／`基本件`／`成本件`／`副本件` 是公告原文里真会出现的词（采购标的、成本构成），
# 「本件」只是它们的尾巴——负向后顾要求「本件」前不得紧邻汉字，尾巴不再命中，而「本件认为」／「，本件认为」／
# 「『本件认为』」前接标点或引号照命中。负向后顾放行两类前邻：①非汉字（句首／标点／引号／数字）；
# ②**虚词**——「据本件判断」「经本件核对」「对本件而言」里「本件」是独立词不是尾巴。实词前邻一律不放行。
# **该表是有限白名单、不覆盖自然语言全部虚词**——「通过本件判断」「围绕本件」「经过本件」「仍本件认为」这类
# 前邻不在表内的形机检认不出、照绿，属**已知覆盖不到**，请人工回原句核对。
SELF_REF_LEAD = "据经由按依对向在被将把以因故但而且并或若如虽即则从自于给替为跟同和与及照就"
SELF_REF = re.compile(r"(?:(?<![一-龥])|(?<=[" + SELF_REF_LEAD + r"]))(?:本件|本卡|本速读|笔者)")
EFFECT = re.compile(r"无效|有效|作废|不成立|成立|撤销|违法|违规|应予支持|予以支持|应支持|支持|必然|属实")
DISCLAIM = re.compile(r"不接|不出|不提供|不作|不判|不碰|不做|不代|禁止|未证|无法|不承诺")
PENDING = re.compile(r"\[待人工\]")


def is_cite_label(s: str) -> bool:
    """书名号外（或书名号内冒号前）那截字是不是**引用标签**：剥掉标点与括号后只剩空＝是；
    否则把引用标签成分（源名词·报道动词·定位词·引述标记）逐个剥掉，剥完还剩字＝本件自己写的，不是引用标签。"""
    t = LABEL_PUNCT.sub("", s)
    return t == "" or CITE_LABEL.sub("", t) == ""


def inner_ok(q: str) -> bool:
    """书名号内以「短标签：」起头时，那个标签也必须是引用标签——「发行人：某股份有限公司」是原文登记，
    「我们判断：本次受让价格公允」是本件自裁（作者口吻的第三种入口在书名号内，不在书名号外）。"""
    m = INNER_LABEL.match(q)
    return True if not m else is_cite_label(m.group(1))


def no_self_ref(q: str) -> bool:
    """书名号内**任意位置**不得出现本件自称——「本件·本卡·本速读·笔者」是写卡人对自己这份卡的称呼，
    公告原文里不可能出现，所以这一形不是「引文不可核验」的取舍面，是结构上必然是本件自己写的字。
    ③（inner_ok）管「带冒号的标签」，这一条管「不带冒号的自称」，两者是并集不是替代。
    **只挡书名号豁免，不当红线词整行扫**：好样卡里「- 本卡以公告原文为准…」「…本件不接代办…」都在书名号外，
    是正当自述，照旧绿；命中后只是这一行的书名号不给豁免，书名号里的字照进判据域，之后照常由 ES-LINE 判。
    **边界两条**：①按前邻词性认不按子串认——前邻非汉字或虚词才算自称，`样本件`／`基本件`／`成本件`／`副本件`
    的尾巴（前邻实词）不算；②先做空白归一（`\\s+` 全删）再扫——`本 件`／`本　件`／`本\\t件` 这类断字公告原文里
    不可能出现，与「本件」同类。"""
    return not SELF_REF.search(re.sub(r"\s+", "", q))


def judge_field(ln: str) -> str:
    """红线判据域＝本件自己写的话：拆字段后剥掉书名号内的公告原句与锚段，项名前缀也不进域。
    书名号豁免改成**白名单准入**（作者口吻是开放集，黑名单补不完）。四条准入条件缺一不给豁免：
      ①该行有锚——「原句逐字＋锚」是豁免的入场券，没锚就不是原文登记；
      ②书名号之外只剩引用标签（源名词·报道动词·定位词·引述标记）或干脆是空的；剥完还剩任何字＝本件自己写的。
        **说明·注不在白名单**：它们是本件自述标签，不是引用标签，挂这两个标签的引文照进内容判据；
      ③书名号内以「短标签：」起头时，那个标签同样得是引用标签；
      ④书名号内任意位置不得出现本件自称。「本公司」「本计划」「本员工持股计划」不在表内，照旧豁免。
    四条都过才剥书名号；公告原句里有裁定措辞不误伤。"""
    item = parse_item_line(ln)
    if item is None:
        body = ln
        ma = ANCHOR_SPLIT.search(body)
        head = body[:ma.start()] if ma else body
        anchored = bool(ANCHOR_VAL.search(ln))
        label = QUOTES.sub(" ", head).strip()
        quotes = QUOTES.findall(head)
    else:
        body = item["body"]
        anchored = bool(item["anchor"].strip())
        label = item["spoken"]
        quotes = item["quotes"]
    if (anchored and is_cite_label(label)
            and all(inner_ok(q) and no_self_ref(q) for q in quotes)):
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
            hits.append(("ES-STRUCT", 0, f"缺段：{name}"))
    zone = speed_zone(lines)
    seen: dict[str, int] = {}
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
            hits.append(("ES-QUOTE", i + 1, f"缺项原句：{name} 那一行没有书名号内的原文"))
        elif any(core_len(q) <= 1 for q in item["quotes"]):
            hits.append(("ES-QUOTE", i + 1, f"原句占位：{name} 那一行的书名号内为空或只剩单字"))
        mv = ANCHOR_VAL.search(ln)
        if not mv or core_len(mv.group(1)) == 0:
            hits.append(("ES-QUOTE", i + 1, f"锚值为空：{name} 那一行的「锚：」后面没有来源定位"))
        if name in NUM_CELLS:
            dates, missing, vague, cands = value_gap(value_field(item), NUM_CELLS[name])
            ev = ""
            if cands:
                ev = "｜有数但不合格的段：" + "∥".join(f"「{s}」＝{why}" for s, why in cands)
            if dates:
                ev += "｜剥掉的日期：" + "∥".join(dates)
            if missing:
                miss = "、".join(e + "（" + why + "）" for e, why in missing)
                both = "∥".join(e for e, _ in missing)
                if vague:
                    hits.append(("ES-VALUE", i + 1, f"{name} 以空泛语顶替原值：这一格的两个要素「{both}」没有各自拿到合格候选，"
                                                   f"句里只剩「{vague.group(0)}」这类说法；缺的要素：{miss}{ev}——面文写的「X 与 Y」"
                                                   "是两组同时给，一枚合格数只算它那一个要素到位，不替整组放行；别格的数、参照数与"
                                                   "日期都不顶账，没取到就写「未检索到」"))
                else:
                    hits.append(("ES-VALUE", i + 1, f"{name} 缺本格原值：两要素里没有各自给出属于本元素的合格候选；缺的要素："
                                                    f"{miss}{ev}——本元素的原值要与本元素的名词同短语相邻，参照数与别元素的数不顶账，"
                                                    "没取到就写「未检索到」"))
    for name in ITEMS:
        if name not in seen:
            hits.append(("ES-STRUCT", 0, f"缺项行：{name} 在逐字速读段里没有以「- 名目：」起头的行"
                                         "（名目按任一表述命中即算在场，别名表见 ITEM_ALIASES）"))
    pending_items = sum(1 for i in zone if ITEM.match(lines[i]) and "未检索到" in lines[i])
    decls = DECL.findall(text)
    if len(decls) > 1:
        hits.append(("ES-COUNT", 0, f"齐缺申报出现 {len(decls)} 处：只准一枚，两处并存即口径不唯一"))
    elif len(decls) == 1 and int(decls[0]) != pending_items:
        hits.append(("ES-COUNT", 0, f"齐缺申报与清单不对账：申报缺 {decls[0]} 项∥速读段实有 {pending_items} 行「未检索到」"))
    elif not decls:
        hits.append(("ES-COUNT", 0, "头部缺「共八项·缺 N 项」申报，无从对账"))
    for i, ln in enumerate(lines, 1):
        dom = judge_field(ln)
        flagged = False
        for seg in SEG_SPLIT.split(dom):
            # marker 只登记它所在那一分句（「[待人工] 方案是否合理留人工」），分号与句号之后的分句照走红线；
            # 免责句同样按分句算——两样豁免都不跨句。
            if PENDING.search(seg) or DISCLAIM.search(seg):
                continue
            seg = NOUN_WASH.sub("", seg)
            mb = BANNED.search(seg)
            if mb:
                hits.append(("ES-LINE", i, f"红线断言词出现在没有 [待人工] 的行：本件自己写的话里有「{mb.group(0)}」——"
                                            "同一行前半写了免责句也不顶，豁免只到分句为止"))
                flagged = True
                break
            ms, mt = SUBJECT.search(seg), TONE.search(seg)
            if ms and mt:
                hits.append(("ES-LINE", i, f"判断式结论落在非待人工行：本件自己写的话里「{ms.group(0)}」与判断语气"
                                           f"「{mt.group(0)}」同段出现——方案好坏·能否解锁·税怎么缴·股价反应这类判断一律留 "
                                           "[待人工]，公告原句（书名号内）与锚不在此列"))
                flagged = True
                break
        if not flagged:
            mv2, me = VERDICT.search(dom), EFFECT.search(NOUN_WASH.sub("", dom))
            if mv2 and me:
                hits.append(("ES-LINE", i, f"自裁效力判断落在非待人工行：本件自己写的话里裁定前缀「{mv2.group(0)}」"
                                            f"＋效力判断「{me.group(0)}」——计划是否有效·程序是否违规这类裁定本件一律不自判，"
                                            "留 [待人工]；公告原句（书名号内）与锚不在此列"))
        if EMPTY_LIE.search(ln):
            hits.append(("ES-COUNT", i, "把「未检索到」写成「无／没有」"))
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
    good = here / "fixtures" / "good-esop-card.md"
    bad = here / "fixtures" / "bad-esop-card.md"
    rows = []
    gt = good.read_text(encoding="utf-8")
    gh = check_text(gt)
    rows.append(("好样须过（发条 0）", not gh, f"实发 {len(gh)} 条"))
    bt = bad.read_text(encoding="utf-8")
    bh = check_text(bt)
    codes = {c for c, _, _ in bh}
    rows.append(("坏样五道齐发", {"ES-STRUCT", "ES-QUOTE", "ES-LINE", "ES-COUNT", "ES-VALUE"} <= codes,
                 "实发码 " + "∥".join(sorted(codes))))
    tmp = make_tmp("check-esop-")
    stripped = tmp / "no-anchor.md"
    stripped.write_text(re.sub(r"锚[:：][^\n]*", "锚：", gt), encoding="utf-8")
    sh = check_text(stripped.read_text(encoding="utf-8"))
    rows.append(("反证·剥锚必发 ES-QUOTE", any(c == "ES-QUOTE" for c, _, _ in sh), f"实发 {len(sh)} 条"))
    nproof = 1
    pin = make_tmp("check-esop-pin-")
    ROW_PRICE = ("「本员工持股计划购买股票的价格为 17.35 元/股」"
                 "「本员工持股计划拟持有的标的股票数量不超过 217.3984 万股」")
    ROW_FUND = ("「本员工持股计划的资金来源为员工合法薪酬、自筹资金以及法律法规允许的其他方式」"
                "「本员工持股计划拟筹集资金总额上限为 3,771.86224 万元」")
    ROW_OBJ = ("「参加本员工持股计划的对象范围为公司（含子公司）核心技术/业务/管理人员（以下简称“持有人”），"
               "不包括公司独立董事、单独或合计持有上市公司 5%以上股份的股东、实际控制人及其配偶、父母、子女，"
               "初始设立时总人数不超过 380 人」")
    ROW_CHANGE = ("- 变更终止与权益处置：「本员工持股计划的变更须经出席持有人会议的持有人所持 2/3（含）以上份额同意，"
                  "并提交公司董事会审议通过后方可实施」 锚：草案 第十章 二")
    ROW_SOURCE = "「本员工持股计划股票来源为公司回购专用账户回购的晶盛机电 A 股普通股股票」"
    HEAD = "## 二、八项逐字速读"
    PENDING_LINE = ("- [待人工] 这份方案值不值得参与、受让价格是否公允、考核目标能否达成、解锁能否实现、"
                    "个人所得税与递延纳税如何处理，全部留人工；本件不接代办，也不碰内幕信息与规避披露的做法。")
    tiers = (
        ("钉阈·名目只剩散文必发 ES-STRUCT",
         gt.replace("- 股票来源：", "股票来源在草案另有说明，", 1),
         "缺项行：股票来源"),
        ("钉阈·整行名目缺席必发 ES-STRUCT",
         gt.replace(ROW_CHANGE + "\n", "", 1),
         "缺项行：变更终止与权益处置"),
        ("钉阈·书名号内单字必发 ES-QUOTE",
         gt.replace(ROW_SOURCE, "「股」", 1),
         "原句占位"),
        ("钉阈·齐缺申报改数必发 ES-COUNT",
         gt.replace("共八项·缺 1 项", "共八项·缺 0 项", 1),
         "齐缺申报与清单不对账"),
        ("钉阈·把未检索到写成无该项必发 ES-COUNT",
         gt.replace("- 管理模式与持有人会议：未检索到（缺数清单已点名）", "- 管理模式与持有人会议：无该项", 1),
         "把「未检索到」写成「无／没有」"),
        ("钉阈·交易均价冒充受让价格必发 ES-VALUE",
         gt.replace(ROW_PRICE, "「受让价格参照草案公布前 20 个交易日交易均价 34.70 元/股，受让价格另行确定」", 1),
         "数紧挨着参照数"),
        ("钉阈·均价五折按比率量纲剔必发 ES-VALUE",
         gt.replace(ROW_PRICE, "「受让价格不低于交易均价的 50%，受让价格另行确定」", 1),
         "是比率或倍数"),
        ("钉阈·占比顶股数账必发 ES-VALUE",
         gt.replace("「本员工持股计划拟持有的标的股票数量不超过 217.3984 万股」",
                    "「标的股票数量占比 0.17%，标的股票数量另行确定」", 1),
         "是比率或倍数"),
        ("钉阈·股本总额冒充标的股票数量必发 ES-VALUE",
         gt.replace("「本员工持股计划拟持有的标的股票数量不超过 217.3984 万股」",
                    "「标的股票数量参照公司股本总额 130,953.3797 万股，标的股票数量另行确定」", 1),
         "数紧挨着参照数"),
        ("钉阈·受让价格整格缺席必发 ES-VALUE",
         gt.replace(ROW_PRICE, "「受让价格按草案约定执行，具体以过户时为准」", 1),
         "缺的要素：受让价格"),
        ("钉阈·资金来源与空泛语同句必发 ES-VALUE",
         gt.replace(ROW_FUND, "「拟筹集资金总额上限为 3,771.86 万元，资金来源另行确定」", 1),
         "不算这一元素读到"),
        ("钉阈·资金总额待定必发 ES-VALUE",
         gt.replace(ROW_FUND, "「本员工持股计划的资金来源为员工合法薪酬、自筹资金，资金总额待定」", 1),
         "缺的要素：资金总额"),
        ("钉阈·草案公布日不顶价格账必发 ES-VALUE",
         gt.replace(ROW_PRICE, "「草案公布日为 2026 年 11 月 6 日，受让价格届时公告」", 1),
         "以空泛语顶替原值"),
        ("钉阈·孤立数无前序本格名词不洗绿必发 ES-VALUE",
         gt.replace("「本员工持股计划拟持有的标的股票数量不超过 217.3984 万股」",
                    "「公司股本总额为 130,953.3797 万股，另需受让 217.3984 万股」", 1),
         "孤立数不越界继承"),
        ("钉阈·否定关系不认共指必发 ES-VALUE",
         gt.replace("「本员工持股计划拟持有的标的股票数量不超过 217.3984 万股」",
                    "「标的股票数量不是受让价格 17.35 元/股」", 1),
         "缺的要素"),
        ("钉阈·同位式共指属已知覆盖不到仍发红必发 ES-VALUE",
         gt.replace(ROW_PRICE, "「受让价格与标的股票数量均为 17.35 元/股」", 1),
         "缺的要素"),
        ("钉阈·方案评价断言带插语必发 ES-LINE",
         gt.replace(HEAD, "- 这份员工持股方案很合理。\n\n" + HEAD, 1),
         "「方案很合理」"),
        ("钉阈·受让价格评价另一支必发 ES-LINE",
         gt.replace(HEAD, "- 受让价格基本公允。\n\n" + HEAD, 1),
         "受让价格基本公允"),
        ("钉阈·解锁预测族必发 ES-LINE",
         gt.replace(HEAD, "- 本次解锁概率大。\n\n" + HEAD, 1),
         "「解锁概率大」"),
        ("钉阈·税务判断必发 ES-LINE（本域独有）",
         gt.replace(HEAD, "- 持有人应缴个人所得税按工资薪金所得计算。\n\n" + HEAD, 1),
         "应缴个人所得税"),
        ("钉阈·递延纳税判断必发 ES-LINE（本域独有）",
         gt.replace(HEAD, "- 本计划可递延纳税。\n\n" + HEAD, 1),
         "可递延纳税"),
        ("钉阈·税务筹划必发 ES-LINE（本域独有）",
         gt.replace(HEAD, "- 建议做税务筹划以降低税负。\n\n" + HEAD, 1),
         "税务筹划"),
        ("钉阈·参与建议必发 ES-LINE",
         gt.replace(HEAD, "- 建议参与本次员工持股计划。\n\n" + HEAD, 1),
         "「建议参与」"),
        ("钉阈·判断式家族（主题＋语气）必发 ES-LINE",
         gt.replace(HEAD, "- 另：本次员工持股会提升收益。\n\n" + HEAD, 1),
         "与判断语气"),
        ("钉阈·自裁效力族必发 ES-LINE",
         gt.replace(HEAD, "- 结论：本次转让行为有效。\n\n" + HEAD, 1),
         "裁定前缀「结论」"),
        ("钉阈·免责句后半的真判断必发 ES-LINE",
         gt.replace(HEAD, "- 说明：本件不判方案好坏；本次解锁一定会实现。\n\n" + HEAD, 1),
         "与判断语气"),
        ("钉阈·书名号包作者自裁必发 ES-LINE",
         gt.replace(HEAD, "- 本件结论：「本次受让价格公允」。\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·作者自裁包书名号又挂锚仍必发 ES-LINE",
         gt.replace(HEAD, "- 本件结论：「本次解锁概率大」 锚：草案 第五章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·整句塞进书名号必发 ES-LINE",
         gt.replace(HEAD, "- 「本件结论：本次受让价格公允」。\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·第一人称判断语包书名号必发 ES-LINE",
         gt.replace(HEAD, "- 我们判断：「本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·未进任何词表的作者口吻包书名号必发 ES-LINE",
         gt.replace(HEAD, "- 本报告研判：「本员工持股计划有效」 锚：草案 第四章\n\n" + HEAD, 1),
         "与判断语气"),
        ("钉阈·注标签藏作者口吻必发 ES-LINE",
         gt.replace(HEAD, "- 注：「本件认为本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·说明标签藏作者口吻必发 ES-LINE",
         gt.replace(HEAD, "- 说明：「本件认为本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·整句进书名号又挂锚必发 ES-LINE",
         gt.replace(HEAD, "- 「我们判断：本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·书名号内本件自称必发 ES-LINE",
         gt.replace(HEAD, "- 草案原文：「本件认为本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·书名号内本卡自称必发 ES-LINE",
         gt.replace(HEAD, "- 草案原文：「本卡认为本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·书名号内本速读自称必发 ES-LINE",
         gt.replace(HEAD, "- 草案原文：「本速读判断本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·书名号内笔者自称必发 ES-LINE",
         gt.replace(HEAD, "- 草案原文：「笔者判断本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·项行书名号内本件自称必发 ES-LINE",
         gt.replace(ROW_OBJ, "「本件认为本次受让价格公允」", 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·书名号内空白断字的本件自称必发 ES-LINE",
         gt.replace(HEAD, "- 草案原文：「本 件认为本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·书名号内全角空白断字的本件自称必发 ES-LINE",
         gt.replace(HEAD, "- 草案原文：「本　件认为本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·书名号内制表符断字的本件自称必发 ES-LINE",
         gt.replace(HEAD, "- 草案原文：「本\t件认为本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·虚词前邻的本件自称必发 ES-LINE",
         gt.replace(HEAD, "- 草案原文：「据本件判断，本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·虚词前邻的本件自称（经）必发 ES-LINE",
         gt.replace(HEAD, "- 草案原文：「经本件核对，本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·虚词前邻的本件自称（对）必发 ES-LINE",
         gt.replace(HEAD, "- 草案原文：「对本件而言，本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·虚词前邻的本件自称（按）必发 ES-LINE",
         gt.replace(HEAD, "- 草案原文：「按本件结论，本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
    )
    for n, (name, text, needle) in enumerate(tiers, 1):
        nproof += 1
        f = pin / f"pin-{n}.md"
        f.write_text(text, encoding="utf-8")
        th = check_text(f.read_text(encoding="utf-8"))
        ok = (text != gt) and any(needle in m for _, _, m in th)
        rows.append((name, ok, f"注入{'生效' if text != gt else '作废'}·命中句 {'有' if ok else '无'}"))
    ctrls = (
        ("对照·受让价格与标的股票数量齐备不误伤（ES-VALUE 零发）",
         gt.replace(ROW_PRICE, "「受让价格为 17.35 元/股，标的股票数量不超过 217.3984 万股」", 1), "ES-VALUE"),
        ("对照·均价五折与受让价格分列不误伤（ES-VALUE 零发）",
         gt.replace(ROW_PRICE, "「受让价格为 17.35 元/股，不低于草案公布前 20 个交易日交易均价的 50%，"
                               "标的股票数量不超过 217.3984 万股」", 1), "ES-VALUE"),
        ("对照·资金来源与资金总额齐备不误伤（ES-VALUE 零发）",
         gt.replace(ROW_FUND, "「资金来源为员工合法薪酬与自筹资金，拟筹集资金总额上限为 3,771.86 万元」", 1), "ES-VALUE"),
        ("对照·受让价格带每股单位不误伤（ES-VALUE 零发）",
         gt.replace(ROW_PRICE, "「受让价格即为每股 17.35 元，标的股票数量不超过 217.3984 万股」", 1), "ES-VALUE"),
        ("对照·股数带占比不误伤（ES-VALUE 零发）",
         gt.replace(ROW_PRICE, "「受让价格为 17.35 元/股，标的股票数量不超过 217.3984 万股，"
                               "占公司股本总额的 0.17%」", 1), "ES-VALUE"),
        ("对照·存续期与锁定期月数不参与名词归属（ES-VALUE 零发）",
         gt.replace(ROW_PRICE, "「受让价格为 17.35 元/股，标的股票数量不超过 217.3984 万股，"
                               "存续期不超过 36 个月，锁定期 12 个月」", 1), "ES-VALUE"),
        # 真实公告的数量格不只有「数量」一种叫法（四份语料实测）：工业富联写「标的股票上限」、
        # 宁德时代写「标的股票规模」、金达威写「认购的股数上限」——名词族收窄了真实原句就整格判缺
        ("对照·真实写法「标的股票上限」按数量格认（ES-VALUE 零发）",
         gt.replace(ROW_PRICE, "「受让价格为 6.49 元/股，本员工持股计划所能购买和持有的标的股票上限为 4,422.82 万股」", 1),
         "ES-VALUE"),
        ("对照·真实写法「标的股票规模」按数量格认（ES-VALUE 零发）",
         gt.replace(ROW_PRICE, "「受让价格为 158.42 元/股，本持股计划拟持有的标的股票规模不超过 808.1586 万股」", 1),
         "ES-VALUE"),
        ("对照·真实写法「认购的股数上限」按数量格认（ES-VALUE 零发）",
         gt.replace(ROW_PRICE, "「受让价格为 8.60 元/股，员工认购的股数上限为 58.13 万股」", 1), "ES-VALUE"),
        # 真实公告会在名词中间插括注（恒铭达「购买股票（含预留部分）的价格」）：括注是限定语不是断句
        ("对照·名词中间插括注「购买股票（含预留部分）的价格」仍按价格格认（ES-VALUE 零发）",
         gt.replace(ROW_PRICE, "「本员工持股计划购买股票（含预留部分）的价格为 24.05 元/股，"
                               "标的股票数量不超过 130.00 万股」", 1), "ES-VALUE"),
        ("对照·名词中间插括注「受让价格（含预留）」仍按价格格认（ES-VALUE 零发）",
         gt.replace(ROW_PRICE, "「本持股计划受让价格（含预留）为 158.42 元/股，"
                               "标的股票规模不超过 808.1586 万股」", 1), "ES-VALUE"),
        ("对照·名词形评价不误伤（ES-LINE 零发）",
         gt.replace(HEAD, "- 本次方案需说明受让价格的公允性。\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·度后缀名词形不误伤（ES-LINE 零发）",
         gt.replace(HEAD, "- 方案合理度讨论见附件。\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·论后缀名词形不误伤（ES-LINE 零发）",
         gt.replace(HEAD, "- 受让价格公允性论证由独立财务顾问出具。\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·持有人会议机构名不误伤（ES-LINE 零发）",
         gt.replace(HEAD, "- 说明：本员工持股计划经持有人会议审议通过。\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·管理委员会机构名不误伤（ES-LINE 零发）",
         gt.replace(HEAD, "- 说明：管理委员会负责本员工持股计划的日常管理。\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·薪酬与考核委员会机构名不误伤（ES-LINE 零发）",
         gt.replace(HEAD, "- 说明：董事会薪酬与考核委员会核实了参加对象名单。\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·会计处理陈述不误伤（ES-LINE 零发）",
         gt.replace(HEAD, "- 说明：本员工持股计划的会计处理按公告列示。\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·有锚公告原句里的裁定措辞不误伤（ES-LINE 零发）",
         gt.replace(ROW_CHANGE,
                    "- 变更终止与权益处置：「未经管理委员会同意擅自转让的，该转让行为无效」 锚：草案 第十章 四", 1),
         "ES-LINE"),
        ("对照·纯待人工登记行不误伤（ES-LINE 零发）",
         gt.replace(PENDING_LINE, "- [待人工] 这份方案值不值得参与留人工。", 1), "ES-LINE"),
        ("对照·免责分句陈述不误伤（ES-LINE 零发）",
         gt.replace(HEAD, "- 说明：本件不出税务意见，也不接代办。\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·书名号内源名词标签不误伤（ES-LINE 零发）",
         gt.replace(HEAD, "- 发行人：「某股份有限公司」 锚：草案 第一章\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·项行引用标签「草案原文」不误伤（ES-LINE 零发）",
         gt.replace(ROW_PRICE, "草案原文「本员工持股计划购买股票的价格为 17.35 元/股」"
                               "「本员工持股计划拟持有的标的股票数量不超过 217.3984 万股」", 1), "ES-LINE"),
        ("对照·书名号内「本公司」是公告主体不误伤（ES-LINE 零发）",
         gt.replace(HEAD, "- 草案原文：「本公司认为本次受让价格遵循公允原则」 锚：草案 第四章\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·书名号内「本员工持股计划」是计划自称不误伤（ES-LINE 零发）",
         gt.replace(HEAD, "- 草案原文：「本员工持股计划由公司自行管理」 锚：草案 第七章\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·书名号内「本计划」是计划自称不误伤（ES-LINE 零发）",
         gt.replace(HEAD, "- 草案原文：「本计划的存续期不超过 36 个月」 锚：草案 第五章\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·书名号外本件自称是正当自述不误伤（ES-LINE 零发）",
         gt.replace(HEAD, "- 本件不接代办，也不碰内幕信息。\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·书名号内「样本件」复合词不误伤（ES-LINE 零发）",
         gt.replace(HEAD, "- 草案原文：「本次受让标的为样本件，受让价格按市场公允价格确定」 锚：草案 第四章\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·书名号内「成本件」复合词不误伤（ES-LINE 零发）",
         gt.replace(HEAD, "- 草案原文：「成本件与标准件的受让价格均为市场公允价格」 锚：草案 第四章\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·前邻不在虚词表内的自称属已知覆盖不到（ES-LINE 零发）",
         gt.replace(HEAD, "- 草案原文：「通过本件判断本次受让价格公允」 锚：草案 第四章\n\n" + HEAD, 1), "ES-LINE"),
        ("对照·别名名目「购买价格与规模」按同一项认（ES-STRUCT 零发）",
         gt.replace("- 受让价格与规模：", "- 购买价格与规模：", 1), "ES-STRUCT"),
        ("对照·别名名目「持有人范围与确定标准」按同一项认（ES-STRUCT 零发）",
         gt.replace("- 参加对象与确定标准：", "- 持有人范围与确定标准：", 1), "ES-STRUCT"),
        # 真实草案章节标题的写法（四份语料实测）：写卡人照抄标题时也得认，否则真实公告会漏
        ("对照·真实标题「持有人的确定依据、范围及份额分配情况」按同一项认（ES-STRUCT 零发）",
         gt.replace("- 参加对象与确定标准：", "- 持有人的确定依据、范围及份额分配情况：", 1), "ES-STRUCT"),
        ("对照·真实标题「变更、终止及持有人权益的处置」按同一项认（ES-STRUCT 零发）",
         gt.replace("- 变更终止与权益处置：", "- 变更、终止及持有人权益的处置：", 1), "ES-STRUCT"),
        ("对照·真实标题「存续期、锁定期和业绩考核」按同一项认（ES-STRUCT 零发）",
         gt.replace("- 存续期与锁定期：", "- 存续期、锁定期和业绩考核：", 1), "ES-STRUCT"),
        ("对照·真实标题「管理机构及管理模式」按同一项认（ES-STRUCT 零发）",
         gt.replace("- 管理模式与持有人会议：", "- 管理机构及管理模式：", 1), "ES-STRUCT"),
        ("对照·真实标题「价格和规模」按同一项认（ES-STRUCT 零发）",
         gt.replace("- 受让价格与规模：", "- 价格和规模：", 1), "ES-STRUCT"),
    )
    for n, (name, text, code) in enumerate(ctrls, 1):
        nproof += 1
        c = pin / f"control-{n}.md"
        c.write_text(text, encoding="utf-8")
        th = check_text(c.read_text(encoding="utf-8"))
        fired = [m for cd, _, m in th if cd == code]
        rows.append((name, text != gt and not fired, f"注入{'生效' if text != gt else '作废'}·{code} 实发 {len(fired)} 条"))
    made = [p.name for p in TMP_ROOTS]
    root = pathlib.Path(tempfile.gettempdir())
    for p in TMP_ROOTS:
        shutil.rmtree(p, ignore_errors=True)
    leftover = sorted(q.name for q in root.iterdir() if q.name.startswith("check-esop-")) if root.is_dir() else []
    rows.append(("临时根自清（跑后不增）", not leftover, f"本次建 {len(made)} 枚·跑后残留 {len(leftover)} 枚"))
    bad_rows = [r for r in rows if not r[1]]
    for name, ok, detail in rows:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}｜{detail}")
    print(f"selftest: {'ALL GREEN' if not bad_rows else 'FAIL'}（好样 1 枚·坏样五道·反例 {nproof} 枚·临时根 {len(TMP_ROOTS)} 枚自清）")
    return 0 if not bad_rows else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="A股员工持股计划条款卡五道机检（零网络）")
    ap.add_argument("target", nargs="?", help="待检的条款卡文件（Markdown）")
    ap.add_argument("--selftest", action="store_true",
                    help="好样须过、坏样五道齐发、钉阈按整族各钉一档、对照样不误伤、临时件自清")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.target:
        ap.error("缺参数：给一个待检文件，或用 --selftest")
    path = pathlib.Path(args.target)
    if not path.is_file():
        print(f"FAIL 读不到文件：{path}")
        return 2
    hits = check_text(path.read_text(encoding="utf-8"))
    if not hits:
        print(f"PASS（扫过 {len(path.read_text(encoding='utf-8').splitlines())} 行，五道全过）")
        return 0
    for code, ln, msg in hits:
        print(f"FAIL [{code}] {path.name}:{ln or '整档'} {msg}")
    print(f"FAIL（扫过 {len(path.read_text(encoding='utf-8').splitlines())} 行，发条 {len(hits)} 条）")
    return 1


if __name__ == "__main__":
    sys.exit(main())

