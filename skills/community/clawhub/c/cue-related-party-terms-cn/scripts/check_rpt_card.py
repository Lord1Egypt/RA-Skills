#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_rpt_card.py — A股关联交易条款卡的机检（零网络、只读传入文件）。

五道码（缺一即不叫过闸）：
  RP-STRUCT 五段齐：头部申报／八项逐字速读／口径对照／缺数清单／待人工，任一节缺失即发；
             八项名目另须在「逐字速读」段内**行级在场**——每枚名目一行以「- 名目：」起头，只在散文里提到不算占行；
  RP-QUOTE  每项原句与锚：项行的书名号（「」『』«»）内原句不得为空或只剩单字；「锚：」标签在而锚值为空同样发；
  RP-LINE   红线断言三道：①定式禁词，含两支**按词族收**的断言——定价类评价（定价·价格·交易价格·交易条件·费率·
             租金·关联交易·本次交易× 合理·公允·偏低·偏高·充分·审慎，插语「很·较为·基本·大体·相当」不构成豁免；
             名词后缀「性·度·论」是说明对象不是断言，两支共用同一份排除式）与审批类预测（获批·过会·通过·豁免获准·
             股东大会通过 × 概率·可能性 × 大·高·很小·极低），另加是否划算／必能过会／稳赚／零风险／保证收益／利好／
             建议参与／建议投反对票／建议弃权／套利／内幕信息／绕开审议／规避披露／代客投票／利益输送／损害中小股东／
             侵占上市公司利益／资金占用构成违规；②判断式规则——项行拆字段后，红线判据域只取本件自己写的话
             （剥掉书名号内的公告原句与锚），主题词（关联交易·关联·交易·定价·价格·金额·额度·结算·账期·占用·回避·
             表决·独立董事·披露·豁免·审议·股东大会·董事会·中小股东·公允·股价·风险·收益·损失）与判断语气同段出现即发；
             ③自裁效力层：裁定前缀（结论／综上／因此／本件认为／判定／认定…）与效力判断（无效／有效／成立／不成立／
             违法／违规／属实…）同现即发。`[待人工]` 标记与免责句都**只登记自己那一分句**（按分号·句号·逗号 cut 后
             逐段判），同一行后半写的肯定预测照发；机构名「X 会」与「会 X」名词里的「会」先按形态从语气域洗掉；
  RP-COUNT  齐缺申报恰一枚：头部「共八项·缺 N 项」只准出现一处（两处并存即发），且 N 必须等于速读段里「未检索到」的
             项行数；把「未检索到」写成「无该项／没有此项」一律发；
  RP-VALUE  两格数字归属（定价政策与交易价格／交易金额与年度额度）**以短语结构体为主**判，不按词表也不按位置：
             ①项行拆字段，判据域只取该项自己的原句；②先剥日期（定价基准日、审计基准日、结算日这类一律剔除，
             「2025 年 12 月 31 日」不是价格）；③取数域按「SEG_SPLIT 标点 ∪ NUM 数字边界」切成短语表，每短语带
             内本格名词（含元素序号）·内参照数名词·内候选三列偏移，一枚候选（金额·倍数·百分比）只在本短语内定档——
             数左跳过单位与连接词后最近的实义名词属本元素名词族（定价依据·交易价格·交易金额·年度额度…）才算合格，
             属参照数族（账面价值·净资产·审计值·评估值·上年同期价·历史交易价·市场均价·第三方报价·已使用额度…）
             且更靠数即剔，**哪怕同一短语别处写了本格名词**；数左什么都不剩时看本短语数右；两头都没有名词＝孤立数才继承
             前序最近一次的本格名词，前序只出现过参照数时不继承；④每格两元素各自要有落点——「X 与 Y」是两组同时给，
             一枚合格候选只算它那一个要素到位、不替整组放行；唯一例外是同短语内两名词夹**肯定系词**（即为·即·为·是·
             等于·均为·都是）、中间不带否定形（不是·并非·不视为·不等同）而只一枚数时，该数同时满足两元素；
             ⑤kind="term" 的元素（定价依据）认它自己的安排用词、不要求金额，但与 num 元素一样判空泛语：用词与
             「待定·另行约定·届时·协商确定」同在一句时不算读到；⑥比率（占比·比重）与期限（按月·按季·N 个月内）
             **不参与名词归属**，只在原句里逐字登记，缺了走「未检索到」。
             射程如实写（首版就写、不等被问）：判的是同一短语内的相邻关系加一次跨短语继承与共指补判，
             **不声称覆盖所有自然语言的归属表达**；同位式共指（系词在两个名词之后，如「交易金额与预计年度额度均为 8,600 万元」）
             与「金额待定但方式已定」的同段共存式都在已知覆盖不到之列，按严格式发红，请人工回原句核对；
             短语内定档吃结构体三列偏移，孤立数继承与空泛语扫描那两步读的是剥日期后的原串对应段，不是结构体本身。
             发红句把被剥的日期、落空候选、缺的要素与取数域首段一并点名当证据。

用法：
  python3 -B scripts/check_rpt_card.py <待检文件>      # 逐条发红，全过则 PASS
  python3 -B scripts/check_rpt_card.py --selftest      # 好样须过、坏样五道齐发、钉阈按整族各钉一档、对照样不误伤、临时件自清
  python3 -B scripts/check_rpt_card.py --help
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

ITEMS = ("交易对方与关联方身份", "标的与服务内容", "定价政策与交易价格", "交易金额与年度额度",
         "结算安排与资金往来", "审议程序与回避表决", "独立董事审议安排", "披露与豁免安排")

# 参照数族（外族）：本域里能冒充「交易价格」与「年度额度」的数——账面与审计类、历史与同期价、同类与询价类。
REF_RPT = (r"账面(?:价值|净值|原值|金额)|净资产|总资产|营业收入|净利润|注册资本|担保总额|募集资金|"
           r"审计(?:值|价|数|结果)|审计(?:后)?(?:的)?(?:净)?资产|评估值|评估结果")
REF_PRICE = (r"历史交易价|上年同期(?:价|交易价)|过去十二个月(?:的)?交易价|近三年平均价|同类交易(?:的)?价|市场均价|"
             r"第三方报价|询价结果|挂牌价|指导价|占\s*[^，。；]{0,10}(?:比例|比重)")
REF_AMOUNT = (r"已使用额度|已发生金额|上年同期(?:发生额|交易金额)|累计已发生|占最近一期经审计[^，。；]{0,12}")

# 两格数字归属（面文里那两个「与」各自的名字）：每格两元素，共用同一台结构体机器。
# kind="num" 的元素要有属于自己的合格候选；kind="term" 的元素要原句里有它自己的安排用词、且同句不带空泛语。
# 一元素判档时，外族＝本格参照数 ∪ 别格元素的名词；同格两元素之间不互为参照数。
NUM_CELLS = {
    "定价政策与交易价格": {
        "foreign": re.compile(REF_RPT + "|" + REF_PRICE),
        "elements": (
            ("定价依据", "term", re.compile(r"定价依据|定价政策|市场价|协议价|成本加成|政府指导价|招标投标|竞价|"
                                            r"市场价格为基础|评估结果为基础|参考.{0,6}价")),
            ("交易价格", "num", re.compile(r"交易价格|成交价格|单价|每股(?:转让)?价格|合同价|每公斤价|每吨价|"
                                           r"租金(?:标准)?|服务费率|费率")),
        ),
    },
    "交易金额与年度额度": {
        "foreign": re.compile(REF_RPT + "|" + REF_AMOUNT),
        "elements": (
            ("交易金额", "num", re.compile(r"交易金额|成交金额|合同(?:总)?金额|本次(?:交易)?金额|金额合计|合同款")),
            ("年度额度", "num", re.compile(r"年度预计[^，。；\d]{0,6}(?:金额|总额|额度|交易)|预计[^，。；\d]{0,6}额度|"
                                            r"额度上限|年度上限|全年预计|可用额度|授权额度")),
        ),
    },
}
NUM = re.compile(r"\d[\d,\.]*\s*(?:万元|亿元|元|倍|％|%)")
MONEY_UNIT = re.compile(r"(?:万元|亿元|元)\s*$")   # 只有带金额量纲的候选才能结算元素；倍·%·％＝比率，只逐字登记
RATIO_MARK = re.compile(r"(?:占比|比例|上浮|增幅|降幅|下降|增长|比重|折扣|折价|溢价)\s*[^，。；\d]{0,4}$")
DATE_SPAN = re.compile(r"\d{4}\s*(?:年|[-/.])\s*\d{1,2}\s*(?:月|[-/.])?\s*\d{1,2}\s*日?"
                       r"|\d{4}\s*年(?:\s*\d{1,2}\s*月)?(?:\s*\d{1,2}\s*日)?"
                       r"|\d{1,2}\s*月\s*\d{1,2}\s*日"
                       r"|\d{4}[-/.]\d{1,2}[-/.]\d{1,2}")
VAGUE = re.compile(r"另行确定|另行约定|另行协商|另行签订|另定|届时公告|届时披露|届时确定|届时|待定|尚未确定|未确定|未定|"
                   r"由交易双方协商|由双方协商|协商确定|以[^，。；]{0,12}为准|尚需|有待|待[^，。]{0,6}出具|"
                   r"按有关规定执行|按规定执行|详见[^，。]{0,8}公告|视[^，。]{0,8}而定|"
                   r"以最终签[^，。；]{0,8}为准|按实际发生额?[^，。；]{0,6}结算|据实结算|以审计结果为准|以评估结果为准")
UNIT_SKIP = re.compile(r"(?:每股|每份|每一元|人民币|约|为|是|即|按|暂定|最终|合计|总计|分别|不低于|不超过|不高于|"
                       r"高于|低于|占|比例|占比|其中|含|部分|等|的|后|前|则|并|至|以及|万股|亿股|万元|亿元|股|元|万|亿)+"
                       r"\s*$")
COPA_REF = re.compile(r"即为|均为|都是|等于|即|为|是")
NEG_COPA = re.compile(r"不|非|未|无|别|勿|毋")   # 否定形在场＝两名词不共指，各回各的落点（不是·并非·不视为·不等同·不等值）
COPA = re.compile(r"为|定为|即|按|暂定|是|确定|达|至")
SEG_SPLIT = re.compile(r"[，。；：！？]+|[,;](?!\s*\d)")   # 千分位逗号不断段；顿号算枚举不算归属边界（分年度枚举别把所有者切开）
NOUN_WASH = re.compile(r"[员委事大东议工学协商年例常布明谈论聚汇组独立]会|会[计议场话晤所馆堂员]")
ITEM = re.compile(r"^\s*[-*]\s*(" + "|".join(map(re.escape, ITEMS)) + r")[：:]")
QUOTES = re.compile(r"[「『«]([^」』»]*)[」』»]")
ANCHOR_SPLIT = re.compile(r"锚[:：]")
ANCHOR_VAL = re.compile(r"锚[:：]\s*(\S.*)$")
# 评价断言族与预测断言族按词族收：被评价的名词 × 插语（可有可无）× 评价词；预测动作 × 概率名词 × 程度词。
# 插语不构成豁免——「估值很合理」「估值基本公允」与「估值合理」同判；「获批可能性极低」与「获批概率大」同判。
NOUN_FORM = r"(?![性度论])"   # 名词形豁免只写这一处：性·度·论三种后缀都是被说明的对象，不是本件自己下的评价断言
VALUER_WORDS = "|".join(w + NOUN_FORM for w in ("合理", "公允", "偏低", "偏高", "充分", "审慎"))
DEGREE_WORDS = r"很|较为|比较|基本|大体|显然|明显|相当"
VALUER_ASSERT = r"(?:定价|价格|交易价格|交易条件|费率|租金|关联交易|本次交易|对价)(?:的)?(?:" + DEGREE_WORDS + r")?(?:" + VALUER_WORDS + r")"
PREDICT_ASSERT = (r"(?:获批|通过审核|审核通过|过会|通过|豁免获准|股东大会通过|取得注册|核准)(?:的)?"
                  r"(?:概率|可能性|几率)(?:很|非常|比|较|极)?(?:大|高|小|低|不大|不高|极低)")
BANNED = re.compile(r"是否划算|必能过会|一定能过会|稳赚|零风险|保证收益|利好|建议参与|建议申购|建议买入|建议卖出|"
                    r"建议投反对票|建议弃权|套利|内幕信息|绕开审议|绕开审批|规避披露|规避关联交易审议|代客申报|代客投票|"
                    r"利益输送|必然获批|损害中小股东|侵占上市公司利益|资金占用构成违规"
                    r"|" + VALUER_ASSERT + r"|" + PREDICT_ASSERT)
SUBJECT = re.compile(r"关联交易|关联|交易|定价|价格|金额|额度|结算|账期|占用|回避|表决|独董|独立董事|披露|豁免|"
                     r"审议|股东大会|董事会|中小股东|公允|股价|风险|收益|损失|补偿")
# 同一份词族喂给两支：BANNED 认整句断言，主题×语气这一支认「名词与评价词被别的话隔开」的写法——排除式只写一次
TONE = re.compile(r"应当|应予|予以|将|会|必|有望|可期|可能|足以|构成|属于|意味着|支持|成立|推翻|无效|有效|上调|下调|"
                  r"提升|下滑|增加|减少|回升|高于|低于|稳赚|赚|亏|无疑|显然|肯定|应(?!急)|"
                  + VALUER_WORDS + r"|" + PREDICT_ASSERT)
VERDICT = re.compile(r"结论|综上|因此|可见|据此|本院认为|本件认为|本卡认为|本件判断|判定|认定|断言")
# 书名号豁免＝**白名单准入**，不是黑名单排除（M581：作者口吻是开放集，黑名单补不完——「我们判断」「本报告研判」
# 「我们看」换个说法就洗绿）。准入条件三条，缺一不给豁免：
#   ①该行有锚（「原句逐字＋锚」是豁免的入场券）；
#   ②书名号之外只剩**引用标签**——源名词（公告·报告书·协议·决议…）／报道动词（载明·披露·约定·称·据·见…）／
#     定位词（第 N 节·页·行）／引述标记（原文·摘录·引用·节选·摘自…），或干脆是空的。剥完还剩任何字＝本件自己写的，
#     书名号里的字照进判据域。**说明·注不在白名单**：它们是本件自述标签，不是引用标签（M582 定）；
#   ③书名号内以「短标签：」起头时，那个标签同样得是引用标签（M583）——「我们判断：…」「本件结论：…」塞进书名号
#     照发，「发行人：某股份有限公司」这类原文登记照旧豁免。整句塞进书名号＋挂锚这一形靠这条堵住，不靠词表；
#   ④书名号内**任意位置**不得出现本件自称（M584）——「本件·本卡·本速读·笔者」是写卡人对自己这份卡的称呼，
#     公告原文里不可能出现，所以这一形不是「引文不可核验」的取舍面，是结构上必然是本件自己写的字。③管「带冒号
#     的标签」，④管「不带冒号的自称」，两者是并集不是替代（M583 交卷时把 SELF_REF 当「已无引用」删掉，是漏搬）。
#     **「本公司」「本行」「本集团」不在表内**：它们是公告主体／银行的自称，原文里真会出现，必须照旧豁免。
CITE_LABEL = re.compile(
    r"原文|摘录|引用|节选|摘自|引自|转引|照录|"
    r"载明|列明|记载|披露|约定|规定|显示|表明|称|据|见|详见|"
    r"募集说明书|说明书|报告书|公告|协议|决议|预案|合同|章程|公示|招标文件|草案|摘要|"
    r"核查意见|督导意见|审计报告|评估报告|董事会决议|股东大会决议|"
    r"第[一二三四五六七八九十百零\d]+[节条章项款页行段]|页|行|段")
LABEL_PUNCT = re.compile(r"[\s　（）()【】\[\]：:，,。.、·\-—_/｜|]+")
INNER_LABEL = re.compile(r"^\s*([^，。；：:]{1,12})[：:]")
# 本件自称（M584）：写卡人对自己这份卡的称呼，公告原文里不可能出现。**不含「本公司」「本行」「本集团」**——
# 那是公告主体／银行的自称，原文里真会出现，收进来就误伤一片。
# **按位置认，不按子串认**（M585）：`样本件`／`基本件`／`成本件`／`副本件` 是公告原文里真会出现的词（采购标的、
# 成本构成），「本件」只是它们的尾巴——负向后顾要求「本件」前不得紧邻汉字，尾巴不再命中，而「本件认为」／
# 「，本件认为」／「『本件认为』」前接标点或引号照命中。加词表补不完（补了样本件还有成品件／标准件），所以是位置约束。
# 负向后顾放行两类前邻：①非汉字（句首／标点／引号／数字）；②**虚词**——「据本件判断」「经本件核对」「对本件而言」
# 里「本件」是独立词不是尾巴，只放行非汉字会把这一族漏掉（M585 gate 出的洞）。实词前邻一律不放行，
# 所以「样本件」「基本件」「成本件」「副本件」这类复合词的尾巴照旧不命中。
# 位置约束两条，取并集（M585）：
#   ①前邻**不是汉字**（句首／标点／引号／数字）——「本件认为」「，本件认为」「『本件认为』」照命中；
#   ②前邻是**虚词**——「据本件判断」「由本件出具」「按本件结论」「经本件核对」「对本件而言」「以本件为准」
#     里「本件」是独立词不是尾巴。实词前邻一律不放行，所以「样本件」「基本件」「成本件」「副本件」这类复合词
#     的尾巴照旧不命中（「成本件认定」也不命中——前邻「成」是实词）。
#   只做①会漏「据本件判断」这一族（前接汉字）；只做「后跟判断动词」的前瞻会漏「由本件出具」「经本件核对」
#   （后接非判断动词），且会把「成本件认定」误红。所以按**前邻词性**收，不按后接词收。
SELF_REF_LEAD = "据经由按依对向在被将把以因故但而且并或若如虽即则从自于给替为跟同和与及照就"
SELF_REF = re.compile(r"(?:(?<![一-龥])|(?<=[" + SELF_REF_LEAD + r"]))(?:本件|本卡|本速读|笔者)")
EFFECT = re.compile(r"无效|有效|作废|不成立|成立|撤销|违法|违规|应予支持|予以支持|应支持|支持|必然|属实")
DISCLAIM = re.compile(r"不接|不出|不提供|不作|不判|不碰|不做|不代|禁止|未证|无法|不承诺")
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
        if COPA.search(rest[len(stripped):]):
            copula = True
        rest = stripped
    return rest, copula


def build_phrases(domain: str, own_list: list, foreign: re.Pattern) -> list[dict]:
    """显式结构体：把取数域按「SEG_SPLIT 标点 ∪ NUM 数字边界」切成短语表。
    每短语＝〔数左｜本短语收的那枚候选｜数右〕，三列偏移＝内本格名词（带元素序号）·内参照数名词·内候选，各自带偏移位；
    候选形制＝金额（元·万元·亿元）∪股数（股·万股·亿股）∪倍数（倍）∪百分比（%·％），但 money 列把后两支标成比率：
             比率（%·倍·占比·上浮一类的说法）只逐字登记、不结算任何元素，M576-1 就是这条从面文落进实现。
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
            "seg": (pre + m.group(0)).strip(), "money": bool(MONEY_UNIT.search(m.group(0))),
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
      （丙）两头都空＝孤立数（主语省略）：从前序取最近的一个本格名词继承；前序只出现过参照数则不继承、仍归参照；
      （丁）谓语（确定为·即·按…）领出而没踩到参照数时，按（丙）走继承，不单独放行；
    ④**共指**：某元素在①〜③里没有自己的候选时，若同一短语内另一元素赢下一枚候选、而本元素的本格名词也在同一条短语里、
      两者之间夹着**肯定**共指系词（即为·均为·都是·等于·即·为·是）且中间不带否定形（不是·并非·不视为·不等同·未·无），      则该枚候选同时满足两元素——否定形在场时那枚数只归最近的名词，另一元素仍要自己的落点；系词必须落在两名词之间，同位式（系词在两名词之后）不在覆盖之内；
      「交易金额即为预计年度额度上限 8,600 万元」是同值句，两个名词共指一枚数；共指系词不在场时严格式不动，
      「交易金额 8,600 万元，预计年度额度待定」仍发；
    ⑤kind="term" 的元素（定价依据）认它自己的安排用词、不要求金额，但与 num 元素一样判空泛语：用词与「待定·另行约定·届时·协商确定」同在一句时只说还没定，不算该元素读到，落进落空清单；「金额待定但方式已定」这种同段共存式也按未定判（已知覆盖不到，分号或句号切开才读得到方式）；
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
                                   + "」在同一句里——那句只说定价依据还没定，不算安排读到"))
                continue
            got = mm.group(0)
            break
        if got:
            satisfied[i] = ename + "（安排用词「" + got + "」在场、同句无空泛语）"
    phrases = build_phrases(naked, own_list, foreign)
    for ph in phrases:
        seg = ph["seg"]
        if not ph["money"]:
            candidates.append((seg, "「" + ph["num"].strip() + "」是比率或倍数（%·％·倍一类的量纲），不是金额——"
                                    "面文写的「比率与期限不参与归属」在这一条：比率只逐字登记，不结算任何元素"))
            continue
        rmark = RATIO_MARK.search(ph["pre"])
        if rmark:
            candidates.append((seg, "数前紧挨着比率词「" + rmark.group(0).strip() + "」——那句给的是占比·上浮·降幅一类的"
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
            candidates.append((seg, "数紧挨着参照数「" + fr[1] + "」（在本短语数左），那是账面价值·净资产·审计值·"
                                    "上年同期价·市场均价·累计已发生额一类的参照数，或同格别元素自己的数，不是本元素要的原值"))
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
        if inh:
            satisfied[inh[2]] = inh[1] + "（孤立数继承前序）"
            ph["won"] = inh[2]
            continue
        if frb:
            candidates.append((seg, "本短语两头都没有本格名词，前序也只出现过参照数「" + frb[1] + "」，孤立数不越界继承"))
            continue
        candidates.append((seg, "数前后与本短语都没有本格名词（交易价格·交易金额·预计年度额度·定价依据一类的），"
                                "也没有「确定为每公斤 N 元」这类谓语，前序同样没有所有者可继承"))
    for i, (ename, kind, rx) in enumerate(elems):
        if i in satisfied or kind == "term":
            continue
        for ph in phrases:
            if ph["won"] is None or ph["won"] == i:
                continue
            mine = [(s, e) for (s, e, idx, _) in ph["own_all"] if idx == i]
            theirs = [(s, e) for (s, e, idx, _) in ph["own_all"] if idx == ph["won"]]
            if not mine or not theirs:
                continue
            a, b = mine[0], theirs[0]
            mid_lo, mid_hi = min(a[1], b[1]), max(a[0], b[0])
            mid = ph["text"][mid_lo:mid_hi] if mid_hi > mid_lo else ""
            cop = COPA_REF.search(mid)
            if cop and not NEG_COPA.search(mid):
                satisfied[i] = "共指（同短语内肯定系词「" + cop.group(0) + "」共指同一枚数）"
                break
    missing = [(ename, ("安排用词要么没出现、要么与空泛语同句（待定·另行约定·届时·协商确定一类），不算这一元素读到"
                        if kind == "term" else "没有属于本元素的合格候选（参照数与别元素的数都不顶账；肯定系词的共指也不在场）"))
               for i, (ename, kind, rx) in enumerate(elems) if i not in satisfied]
    return dates, missing, vague, candidates


def is_cite_label(s: str) -> bool:
    """书名号外（或书名号内冒号前）那截字是不是**引用标签**：剥掉标点与括号后只剩空＝是；
    否则把引用标签成分（源名词·报道动词·定位词·引述标记）逐个剥掉，剥完还剩字＝本件自己写的，不是引用标签。"""
    t = LABEL_PUNCT.sub("", s)
    return t == "" or CITE_LABEL.sub("", t) == ""


def inner_ok(q: str) -> bool:
    """书名号内以「短标签：」起头时，那个标签也必须是引用标签——「发行人：某股份有限公司」是原文登记，
    「我们判断：本次交易定价公允」是本件自裁（M583：作者口吻的第三种入口在书名号内，不在书名号外）。"""
    m = INNER_LABEL.match(q)
    return True if not m else is_cite_label(m.group(1))


def no_self_ref(q: str) -> bool:
    """书名号内**任意位置**不得出现本件自称（M584）——「本件·本卡·本速读·笔者」是写卡人对自己这份卡的称呼，
    公告原文里不可能出现，所以这一形不是「引文不可核验」的取舍面，是结构上必然是本件自己写的字。
    ③（inner_ok）管「带冒号的标签」，这一条管「不带冒号的自称」，两者是并集不是替代。
    **只挡书名号豁免，不当红线词整行扫**：好样卡里「- 本卡以公告原文为准…」「…本件不接代办…」都在书名号外，
    是正当自述，照旧绿；命中后只是这一行的书名号不给豁免，书名号里的字照进判据域，之后照常由 RP-LINE 判。
    **边界两条（M585）**：①按前邻词性认不按子串认——前邻非汉字或虚词才算自称，`样本件`／`基本件`／`成本件`／`副本件` 的尾巴（前邻实词）不算；
    ②先做空白归一（`\\s+` 全删）再扫——`本 件`／`本　件`／`本\\t件` 这类断字公告原文里不可能出现，与「本件」同类。"""
    return not SELF_REF.search(re.sub(r"\s+", "", q))


def judge_field(ln: str) -> str:
    """红线判据域＝本件自己写的话：拆字段后剥掉书名号内的报告书原句与锚段，项名前缀也不进域。
    书名号豁免改成**白名单准入**（M581：作者口吻是开放集，黑名单补不完——「我们判断」「本报告研判」「我们看」
    换个说法就洗绿）。四条准入条件缺一不给豁免：
      ①该行有锚——「原句逐字＋锚」是豁免的入场券，没锚就不是原文登记；
      ②书名号之外只剩引用标签（源名词·报道动词·定位词·引述标记）或干脆是空的；剥完还剩任何字＝本件自己写的。
        **说明·注不在白名单**：它们是本件自述标签，不是引用标签（M582 定），挂这两个标签的引文照进内容判据；
      ③书名号内以「短标签：」起头时，那个标签同样得是引用标签（M583）——「我们判断：…」塞进书名号照发，
        「发行人：某股份有限公司」这类原文登记照旧豁免；
      ④书名号内任意位置不得出现本件自称（M584）——「本件·本卡·本速读·笔者」公告原文里不可能出现，
        ③管带冒号的标签、④管不带冒号的自称，并集不是替代。「本公司」「本行」「本集团」不在表内，照旧豁免。
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
            hits.append(("RP-STRUCT", 0, f"缺段：{name}"))
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
            hits.append(("RP-QUOTE", i + 1, f"缺项原句：{name} 那一行没有书名号内的原文"))
        elif any(core_len(q) <= 1 for q in item["quotes"]):
            hits.append(("RP-QUOTE", i + 1, f"原句占位：{name} 那一行的书名号内为空或只剩单字"))
        mv = ANCHOR_VAL.search(ln)
        if not mv or core_len(mv.group(1)) == 0:
            hits.append(("RP-QUOTE", i + 1, f"锚值为空：{name} 那一行的「锚：」后面没有来源定位"))
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
                    hits.append(("RP-VALUE", i + 1, f"{name} 以空泛语顶替原值：这一格的两个要素「{both}」没有各自拿到合格候选，"
                                                   f"句里只剩「{vague.group(0)}」这类说法；缺的要素：{miss}{ev}——面文写的「X 与 Y」"
                                                   "是两组同时给，一枚合格数只算它那一个要素到位，不替整组放行；别格的数、参照数与"
                                                   "日期都不顶账，没取到就写「未检索到」"))
                else:
                    hits.append(("RP-VALUE", i + 1, f"{name} 缺本格原值：两要素里没有各自给出属于本元素的合格候选；缺的要素："
                                                    f"{miss}{ev}——本元素的原值要与本元素的名词同短语相邻，参照数与别元素的数不顶账，"
                                                    "没取到就写「未检索到」"))
    for name in ITEMS:
        if name not in seen:
            hits.append(("RP-STRUCT", 0, f"缺项行：{name} 在逐字速读段里没有以「- 名目：」起头的行"))
    pending_items = sum(1 for i in zone if ITEM.match(lines[i]) and "未检索到" in lines[i])
    decls = DECL.findall(text)
    if len(decls) > 1:
        hits.append(("RP-COUNT", 0, f"齐缺申报出现 {len(decls)} 处：只准一枚，两处并存即口径不唯一"))
    elif len(decls) == 1 and int(decls[0]) != pending_items:
        hits.append(("RP-COUNT", 0, f"齐缺申报与清单不对账：申报缺 {decls[0]} 项∥速读段实有 {pending_items} 行「未检索到」"))
    elif not decls:
        hits.append(("RP-COUNT", 0, "头部缺「共八项·缺 N 项」申报，无从对账"))
    for i, ln in enumerate(lines, 1):
        dom = judge_field(ln)
        flagged = False
        for seg in SEG_SPLIT.split(dom):
            # marker 只登记它所在那一分句（「[待人工] 估值是否合理留人工」），分号与句号之后的分句照走红线；
            # 免责句同样按分句算——两样豁免都不跨句。
            if PENDING.search(seg) or DISCLAIM.search(seg):
                continue
            seg = NOUN_WASH.sub("", seg)
            mb = BANNED.search(seg)
            if mb:
                hits.append(("RP-LINE", i, f"红线断言词出现在没有 [待人工] 的行：本件自己写的话里有「{mb.group(0)}」——"
                                            "同一行前半写了免责句也不顶，豁免只到分句为止"))
                flagged = True
                break
            ms, mt = SUBJECT.search(seg), TONE.search(seg)
            if ms and mt:
                hits.append(("RP-LINE", i, f"判断式结论落在非待人工行：本件自己写的话里「{ms.group(0)}」与判断语气"
                                           f"「{mt.group(0)}」同段出现——交易能否过会·估值高低·股价反应这类判断一律留 "
                                           "[待人工]，报告书原句（书名号内）与锚不在此列"))
                flagged = True
                break
        if not flagged:
            mv2, me = VERDICT.search(dom), EFFECT.search(NOUN_WASH.sub("", dom))
            if mv2 and me:
                hits.append(("RP-LINE", i, f"自裁效力判断落在非待人工行：本件自己写的话里裁定前缀「{mv2.group(0)}」"
                                            f"＋效力判断「{me.group(0)}」——本次交易是否有效·程序是否违规这类裁定本件一律不自判，"
                                            "留 [待人工]；报告书原句（书名号内）与锚不在此列"))
        if EMPTY_LIE.search(ln):
            hits.append(("RP-COUNT", i, "把「未检索到」写成「无／没有」"))
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
    good = here / "fixtures" / "good-rpt-card.md"
    bad = here / "fixtures" / "bad-rpt-card.md"
    rows = []
    gt = good.read_text(encoding="utf-8")
    gh = check_text(gt)
    rows.append(("好样须过（发条 0）", not gh, f"实发 {len(gh)} 条"))
    bt = bad.read_text(encoding="utf-8")
    bh = check_text(bt)
    codes = {c for c, _, _ in bh}
    rows.append(("坏样五道齐发", {"RP-STRUCT", "RP-QUOTE", "RP-LINE", "RP-COUNT", "RP-VALUE"} <= codes,
                 "实发码 " + "∥".join(sorted(codes))))
    tmp = make_tmp("check-rpt-")
    stripped = tmp / "no-anchor.md"
    stripped.write_text(re.sub(r"锚[:：][^\n]*", "锚：", gt), encoding="utf-8")
    sh = check_text(stripped.read_text(encoding="utf-8"))
    rows.append(("反证·剥锚必发 RP-QUOTE", any(c == "RP-QUOTE" for c, _, _ in sh), f"实发 {len(sh)} 条"))
    nproof = 1
    pin = make_tmp("check-rpt-pin-")
    ROW_PRICE = "「本次交易以市场公开价格为定价依据，经双方协商确定交易价格为每公斤 12.60 元」"
    ROW_AMOUNT = "「本次交易金额合计 8,600 万元，列入 2026 年度预计总额度不超过 12,000 万元」"
    ROW_PARTY = "「本次关联交易对方为公司控股股东的全资子公司，公司与其构成关联关系」"
    HEAD = "## 二、八项逐字速读"
    PENDING_LINE = ("- [待人工] 关联交易定价是否公允、是否损害中小股东利益、是否构成利益输送、股东大会能否通过、"
                    "对当期业绩的影响，全部留人工；本件不接代办，也不碰内幕信息与规避披露的做法。")
    tiers = (
        ("钉阈·名目只剩散文必发 RP-STRUCT",
         gt.replace("- 标的与服务内容：", "标的与服务内容在公告另有说明，", 1),
         "缺项行：标的与服务内容"),
        ("钉阈·整行名目缺席必发 RP-STRUCT",
         gt.replace("- 披露与豁免安排：「本次关联交易达到披露标准，可在年度预计额度内免于逐项提交股东大会审议」 锚：公告 第七节 披露与豁免\n", "", 1),
         "缺项行：披露与豁免安排"),
        ("钉阈·书名号内单字必发 RP-QUOTE",
         gt.replace("「本次关联交易标的为原材料采购，并由关联方向公司提供仓储服务」", "「购」", 1),
         "原句占位"),
        ("钉阈·齐缺申报改数必发 RP-COUNT",
         gt.replace("共八项·缺 1 项", "共八项·缺 0 项", 1),
         "齐缺申报与清单不对账"),
        ("钉阈·把未检索到写成无该项必发 RP-COUNT",
         gt.replace("- 独立董事审议安排：未检索到（缺数清单已点名）", "- 独立董事审议安排：无该项", 1),
         "把「未检索到」写成「无／没有」"),
        ("钉阈·上年同期价冒充交易价格必发 RP-VALUE",
         gt.replace(ROW_PRICE, "「交易价格参照上年同期价格 12.00 元，定价依据为市场公开价格」", 1),
         "数紧挨着参照数「上年同期价」"),
        ("钉阈·均价倍数按比率量纲剔必发 RP-VALUE",
         gt.replace(ROW_PRICE, "「定价依据为市场均价的 1.2 倍，交易价格另行确定」", 1),
         "是比率或倍数"),
        ("钉阈·比率顶金额账必发 RP-VALUE（M576-1）",
         gt.replace(ROW_AMOUNT, "「本次交易金额占比 10%，列入年度预计总额度不超过 12,000 万元」", 1),
         "是比率或倍数"),
        ("钉阈·比率词顶着金额数必发 RP-VALUE（M576-1 另一支）",
         gt.replace(ROW_AMOUNT, "「本次交易金额较上年上浮 1,200 万元，预计年度额度 12,000 万元」", 1),
         "紧挨着比率词"),
        ("钉阈·格内两数全是比率必发 RP-VALUE（M576-1 整格）",
         gt.replace(ROW_AMOUNT, "「本次交易金额占比 10%，年度预计总额度占比 8%」", 1),
         "是比率或倍数"),
        ("钉阈·书名号包作者自裁必发 RP-LINE（M576-2）",
         gt.replace(HEAD, "- 本件结论：「本次关联交易定价公允」。\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·作者自裁包书名号又挂锚仍必发 RP-LINE（M576-2 另一支）",
         gt.replace(HEAD, "- 本件结论：「本次交易一定能过会」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·整句塞进书名号必发 RP-LINE（M576-2 无锚支）",
         gt.replace(HEAD, "- 「本件结论：本次关联交易定价公允」。\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·第一人称判断语包书名号必发 RP-LINE（M581）",
         gt.replace(HEAD, "- 我们判断：「本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·本报告判断包书名号必发 RP-LINE（M581）",
         gt.replace(HEAD, "- 本报告判断：「本次交易有效」 锚：公告 第二节\n\n" + HEAD, 1),
         "与判断语气"),
        ("钉阈·未进任何词表的作者口吻包书名号必发 RP-LINE（M581 结构性）",
         gt.replace(HEAD, "- 本报告研判：「本次交易有效」 锚：公告 第二节\n\n" + HEAD, 1),
         "与判断语气"),
        ("钉阈·我们看包书名号必发 RP-LINE（M581 结构性）",
         gt.replace(HEAD, "- 我们看：「本次交易一定能过会」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·注标签藏作者口吻必发 RP-LINE（M582）",
         gt.replace(HEAD, "- 注：「本件认为本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·说明标签藏作者口吻必发 RP-LINE（M582）",
         gt.replace(HEAD, "- 说明：「本件认为本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·整句进书名号又挂锚必发 RP-LINE（M583）",
         gt.replace(HEAD, "- 「我们判断：本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·书名号内本件自称必发 RP-LINE（M584）",
         gt.replace(HEAD, "- 公告原文：「本件认为本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·书名号内本卡自称必发 RP-LINE（M584）",
         gt.replace(HEAD, "- 公告原文：「本卡认为本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·书名号内本速读自称必发 RP-LINE（M584）",
         gt.replace(HEAD, "- 公告原文：「本速读判断本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·书名号内笔者自称必发 RP-LINE（M584）",
         gt.replace(HEAD, "- 公告原文：「笔者判断本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·项行书名号内本件自称必发 RP-LINE（M584）",
         gt.replace(ROW_PARTY, "「本件认为公司与其构成关联关系」", 1),
         "与判断语气"),
        ("钉阈·书名号内空白断字的本件自称必发 RP-LINE（M585）",
         gt.replace(HEAD, "- 公告原文：「本 件认为本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·书名号内全角空白断字的本件自称必发 RP-LINE（M585）",
         gt.replace(HEAD, "- 公告原文：「本　件认为本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·书名号内制表符断字的本件自称必发 RP-LINE（M585）",
         gt.replace(HEAD, "- 公告原文：「本\t件认为本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·书名号内空白断字的本卡自称必发 RP-LINE（M585）",
         gt.replace(HEAD, "- 公告原文：「本 卡认为本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·书名号内空白断字的笔者自称必发 RP-LINE（M585）",
         gt.replace(HEAD, "- 公告原文：「笔 者判断本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·虚词前邻的本件自称必发 RP-LINE（M585）",
         gt.replace(HEAD, "- 公告原文：「据本件判断，本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·虚词前邻的本件自称（经）必发 RP-LINE（M585）",
         gt.replace(HEAD, "- 公告原文：「经本件核对，本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·虚词前邻的本件自称（对）必发 RP-LINE（M585）",
         gt.replace(HEAD, "- 公告原文：「对本件而言，本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·虚词前邻的本件自称（以）必发 RP-LINE（M585）",
         gt.replace(HEAD, "- 公告原文：「以本件为准，本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·虚词前邻的本件自称（由）必发 RP-LINE（M585）",
         gt.replace(HEAD, "- 公告原文：「由本件判断，本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·虚词前邻的本件自称（按）必发 RP-LINE（M585）",
         gt.replace(HEAD, "- 公告原文：「按本件结论，本次关联交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1),
         "红线断言词出现在没有 [待人工] 的行"),
        ("钉阈·账面值冒充年度额度必发 RP-VALUE",
         gt.replace(ROW_AMOUNT, "「本次交易金额合计 8,600 万元，年度额度参照账面价值 30,000 万元」", 1),
         "数紧挨着参照数「账面价值」"),
        ("钉阈·已发生额冒充额度必发 RP-VALUE",
         gt.replace(ROW_AMOUNT, "「本次交易金额合计 8,600 万元，年度额度以累计已发生 30,000 万元为准」", 1),
         "数紧挨着参照数「累计已发生」"),
        ("钉阈·年度额度待定必发 RP-VALUE",
         gt.replace(ROW_AMOUNT, "「本次交易金额合计 8,600 万元，年度额度待定」", 1),
         "缺的要素：年度额度"),
        ("钉阈·定价依据与空泛语同句必发 RP-VALUE",
         gt.replace(ROW_PRICE, "「交易价格为每公斤 12.60 元，定价依据另行确定」", 1),
         "不算这一元素读到"),
        ("钉阈·交易价格整格缺席必发 RP-VALUE",
         gt.replace(ROW_PRICE, "「本次交易以市场公开价格为定价依据，金额按实际发生结算」", 1),
         "缺的要素：交易价格"),
        ("钉阈·定价基准日不顶价格账必发 RP-VALUE",
         gt.replace(ROW_PRICE, "「定价基准日为 2025 年 12 月 31 日，交易价格届时公告」", 1),
         "以空泛语顶替原值"),
        ("钉阈·孤立数无前序本格名词不洗绿必发 RP-VALUE",
         gt.replace(ROW_AMOUNT, "「经审计净资产为 41,000 万元，标的另需支付 8,000 万元」", 1),
         "孤立数不越界继承"),
        ("钉阈·否定关系不认共指必发 RP-VALUE",
         gt.replace(ROW_AMOUNT, "「预计年度额度不是交易金额 8,600 万元」", 1),
         "缺的要素：年度额度"),
        ("钉阈·同位式共指属已知覆盖不到仍发红必发 RP-VALUE",
         gt.replace(ROW_AMOUNT, "「交易金额与预计年度额度均为 8,600 万元」", 1),
         "缺的要素"),
        ("钉阈·红线定式词利益输送必发 RP-LINE",
         gt.replace(HEAD, "- 本次交易的定价明显有利于关联方，构成利益输送。\n\n" + HEAD, 1),
         "「利益输送」"),
        ("钉阈·投票建议必发 RP-LINE",
         gt.replace(HEAD, "- 建议投反对票。\n\n" + HEAD, 1),
         "「建议投反对票」"),
        ("钉阈·判断式家族（主题＋语气）必发 RP-LINE",
         gt.replace(HEAD, "- 另：本次关联交易会提升收益。\n\n" + HEAD, 1),
         "与判断语气"),
        ("钉阈·自裁效力族必发 RP-LINE",
         gt.replace(HEAD, "- 结论：本次授权文件有效。\n\n" + HEAD, 1),
         "裁定前缀「结论」"),
        ("钉阈·免责句后半的真判断必发 RP-LINE",
         gt.replace(HEAD, "- 说明：本件不判定价是否公允；本次交易一定能过会。\n\n" + HEAD, 1),
         "「一定能过会」"),
        ("钉阈·评价断言带插语必发 RP-LINE",
         gt.replace(HEAD, "- 本次交易定价很合理。\n\n" + HEAD, 1),
         "「定价很合理」"),
        ("钉阈·评价断言另一支必发 RP-LINE",
         gt.replace(HEAD, "- 关联交易价格基本公允。\n\n" + HEAD, 1),
         "价格基本公允"),
        ("钉阈·审批预测族必发 RP-LINE",
         gt.replace(HEAD, "- 本次关联交易获批概率大。\n\n" + HEAD, 1),
         "「获批概率大」"),
        ("钉阈·损害中小股东断言必发 RP-LINE",
         gt.replace(HEAD, "- 本次交易损害中小股东利益。\n\n" + HEAD, 1),
         "「损害中小股东」"),
    )
    for n, (name, text, needle) in enumerate(tiers, 1):
        nproof += 1
        f = pin / f"pin-{n}.md"
        f.write_text(text, encoding="utf-8")
        th = check_text(f.read_text(encoding="utf-8"))
        ok = (text != gt) and any(needle in m for _, _, m in th)
        rows.append((name, ok, f"注入{'生效' if text != gt else '作废'}·命中句 {'有' if ok else '无'}"))
    ctrls = (
        ("对照·定价依据与交易价格齐备不误伤（RP-VALUE 零发）",
         gt.replace(ROW_PRICE, "「定价依据为市场公开价格，交易价格为每公斤 12.60 元」", 1), "RP-VALUE"),
        ("对照·额度与金额分列不误伤（RP-VALUE 零发）",
         gt.replace(ROW_AMOUNT, "「预计年度额度不超过 12,000 万元，本次交易金额 8,600 万元」", 1), "RP-VALUE"),
        ("对照·肯定系词共指不误伤（RP-VALUE 零发）",
         gt.replace(ROW_AMOUNT, "「本次交易金额即为预计年度额度 12,000 万元」", 1), "RP-VALUE"),
        ("对照·额度按年计与期限不参与名词归属（RP-VALUE 零发）",
         gt.replace(ROW_AMOUNT, "「本次交易金额合计 8,600 万元，预计年度额度不超过 12,000 万元，协议有效期 3 年」", 1),
         "RP-VALUE"),
        ("对照·价格带括注下限不误伤（RP-VALUE 零发）",
         gt.replace(ROW_PRICE, "「定价依据为协议价，交易价格为每公斤 12.60 元（不低于成本加成价）」", 1), "RP-VALUE"),
        ("对照·结算周期与占用陈述不误伤（RP-VALUE 零发）",
         gt.replace(ROW_AMOUNT, "「本次交易金额合计 8,600 万元，预计年度额度 12,000 万元，款项按季度结算」", 1), "RP-VALUE"),
        ("对照·名词形评价不误伤（RP-LINE 零发）",
         gt.replace(HEAD, "- 本次交易需说明定价的公允性。\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·度后缀名词形不误伤（RP-LINE 零发）",
         gt.replace(HEAD, "- 关联交易合理度讨论见附件。\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·论后缀名词形不误伤（RP-LINE 零发）",
         gt.replace(HEAD, "- 定价公允性论证由独立财务顾问出具。\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·机构名里的「会」不误伤（RP-LINE 零发）",
         gt.replace(HEAD, "- 说明：本次交易经董事会审议通过。\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·审计委员会核实不误伤（RP-LINE 零发）",
         gt.replace(HEAD, "- 说明：审计委员会核实了关联方身份。\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·会计处理陈述不误伤（RP-LINE 零发）",
         gt.replace(HEAD, "- 说明：关联交易的会计处理按公告列示。\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·比率在场而两元素金额齐备不误伤（RP-VALUE 零发）（M576-1 对照）",
         gt.replace(ROW_AMOUNT,
                    "「本次交易金额合计 8,600 万元，占年度预计总额度的比例 71%，年度预计总额度 12,000 万元」", 1),
         "RP-VALUE"),
        ("对照·有锚公告原句里的裁定措辞不误伤（RP-LINE 零发）",
         gt.replace("- 披露与豁免安排：「本次关联交易达到披露标准，可在年度预计额度内免于逐项提交股东大会审议」 锚：公告 第七节 披露与豁免",
                    "- 披露与豁免安排：「本次交易的效力以股东大会审议结果为准，关联股东回避表决的认定见公告」 锚：公告 第七节", 1), "RP-LINE"),
        ("对照·纯待人工登记行不误伤（RP-LINE 零发）",
         gt.replace(PENDING_LINE, "- [待人工] 关联交易定价是否公允留人工。", 1), "RP-LINE"),
        ("对照·免责分句陈述不误伤（RP-LINE 零发）",
         gt.replace(HEAD, "- 说明：本件不出公允性意见，也不接代办。\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·书名号内源名词标签不误伤（RP-LINE 零发）（M583）",
         gt.replace(HEAD, "- 发行人：「某股份有限公司」 锚：公告 第一节\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·项行引用标签「公告原文」不误伤（RP-LINE 零发）（M583）",
         gt.replace(ROW_PRICE, "公告原文「本次交易以市场公开价格为定价依据，经双方协商确定交易价格为每公斤 12.60 元」", 1),
         "RP-LINE"),
        ("对照·书名号内「本公司」是公告主体不误伤（RP-LINE 零发）（M584）",
         gt.replace(HEAD, "- 公告原文：「本公司认为本次交易定价遵循公允原则」 锚：公告 第三节\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·书名号内「本行」是银行自称不误伤（RP-LINE 零发）（M584）",
         gt.replace(HEAD, "- 公告原文：「本次交易定价遵循公允原则，本行已履行审批程序」 锚：公告 第三节\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·书名号内中性引文不误伤（RP-LINE 零发）（M584）",
         gt.replace(HEAD, "- 公告原文：「本次交易定价遵循公允原则」 锚：公告 第三节\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·书名号外本件自称是正当自述不误伤（RP-LINE 零发）（M584）",
         gt.replace(HEAD, "- 本件不接代办，也不碰内幕信息。\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·书名号内「样本件」复合词不误伤（RP-LINE 零发）（M585）",
         gt.replace(HEAD, "- 公告原文：「本次交易标的为样本件，交易价格按市场公允价格确定」 锚：公告 第三节\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·书名号内「基本件」复合词不误伤（RP-LINE 零发）（M585）",
         gt.replace(HEAD, "- 公告原文：「基本件采购价格按市场公允价格确定」 锚：公告 第三节\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·书名号内「成本件」复合词不误伤（RP-LINE 零发）（M585）",
         gt.replace(HEAD, "- 公告原文：「成本件与标准件的定价依据均为市场公允价格」 锚：公告 第三节\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·书名号内「副本件」复合词不误伤（RP-LINE 零发）（M585）",
         gt.replace(HEAD, "- 公告原文：「副本件与正本件内容一致，交易价格按市场公允价格确定」 锚：公告 第三节\n\n" + HEAD, 1), "RP-LINE"),
        ("对照·前邻不在虚词表内的自称属已知覆盖不到（RP-LINE 零发）（M587）",
         gt.replace(HEAD, "- 公告原文：「通过本件判断本次交易定价公允」 锚：公告 第二节\n\n" + HEAD, 1), "RP-LINE"),
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
    leftover = sorted(q.name for q in root.iterdir() if q.name.startswith("check-rpt-")) if root.is_dir() else []
    rows.append(("临时根自清（跑后不增）", not leftover, f"本次建 {len(made)} 枚·跑后残留 {len(leftover)} 枚"))
    bad_rows = [r for r in rows if not r[1]]
    for name, ok, detail in rows:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}｜{detail}")
    print(f"selftest: {'ALL GREEN' if not bad_rows else 'FAIL'}（好样 1 枚·坏样五道·反例 {nproof} 枚·临时根 {len(TMP_ROOTS)} 枚自清）")
    return 0 if not bad_rows else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="A股并购重组条款卡五道机检（零网络）")
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
