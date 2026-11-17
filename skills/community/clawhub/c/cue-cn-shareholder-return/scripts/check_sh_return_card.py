#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_sh_return_card.py — A股股东回报全景卡的机检（零网络、只读传入文件）。

五道码（缺一即不叫过闸）：
  SR-STRUCT 五段齐：头部申报／八项逐字速读／口径对照／缺数清单／待人工，任一节缺失即发；
             八项名目另须在「逐字速读」段内**行级在场**——每枚名目一行以「- 名目：」起头，只在散文里提到不算占行；
  SR-QUOTE  每项原句与锚：项行的书名号（「」『』«»）内原句不得为空或只剩单字；「锚：」标签在而锚值为空同样发；
  SR-LINE   红线断言三道：①定式禁词，含三支**按词族收**的断言——回报类评价（分红率·股息率·分红比例·派息率·
             回购力度·回购规模·减持规模·质押比例·分红方案·回购方案·减持计划·质押 × 合理·公允·偏高·偏低·
             充分·不足·慷慨·大方·优厚·有诚意·划算，插语「很·较为·基本·大体·相当」不构成豁免；名词后缀
             「性·度·论」是说明对象不是断言）、实施类预测（回购·增持·减持·解禁·分红·派息·注销·实施 ×
             概率·可能性·几率 × 大·高·小·低）与**股价影响断言**（股价·市值·估值·每股收益·市盈率 ×
             将·会·有望·必然·势必·可能·预计 × 上涨·下跌·走高·走低·提振·承压·反弹·回升·回落·提升·下滑·修复），
             另加是否划算／值得买入／值得卖出／建议买入／建议卖出／建议增持／建议减持／建议持有／稳赚／零风险／
             保证收益／利好／利空／必涨／必跌／抄底／套利／代拟／代算／代客／内幕信息／绕开审议／规避披露／
             损害中小股东利益／损害股东利益／侵占公司利益；
             ②判断式规则——项行拆字段后，红线判据域只取本件自己写的话（剥掉书名号内的公告原句与锚），主题词
             （分红·派息·送股·转增·回购·注销·减持·增持·质押·解押·解禁·股权登记·除权除息·股息率·分红率·
             股价·市值·股东·股本·方案·计划·回报）与判断语气同段出现即发；
             ③自裁效力层：裁定前缀（结论／综上／因此／本件认为／判定／认定…）与效力判断（无效／有效／成立／
             不成立／违法／违规／合规／属实／构成承诺／应当披露…）同现即发。`[待人工]` 标记与免责句都**只登记
             自己那一分句**（按分号·句号·逗号 cut 后逐段判），同一行后半写的肯定预测照发；机构名「X 会」与
             「会 X」名词里的「会」先按形态从语气域洗掉（董事会·股东大会·监事会·审计委员会·薪酬与考核委员会
             都不误红）；
  SR-COUNT  齐缺申报恰一枚：头部「共八项·缺 N 项」只准出现一处（两处并存即发），且 N 必须等于速读段里「未检索到」的
             项行数；把「未检索到」写成「无该项／没有此项」一律发；
  SR-VALUE  两格数字归属（分红方案与每股派息／回购方案与回购规模）**以短语结构体为主**判，不按词表也不按位置：
             ①项行拆字段，判据域只取该项自己的原句；②先剥日期（公告日、股权登记日、除权除息日这类一律剔除，
             「2026 年 6 月 12 日」不是派息值）；③**本域独有的预处理：`每 N 股` 里的 N 是分母不是值**——
             `每 10 股派 3.50 元` 的 10 是「每十股」这个单位的分母，先把它掩成 `每N股` 再切短语，否则机器会把
             10 当成派息值、把 3.50 当成每股值；简写形 `10派3.5元` 同样掩成 `每N股派 3.5 元`。被掩的分母进证据串，
             不静默吞掉；④取数域按「SEG_SPLIT 标点 ∪ NUM 数字边界」切成短语表，每短语带内本格名词（含元素序号）·
             内参照数名词·内候选三列偏移，一枚候选只在本短语内定档——数左跳过单位与连接词后最近的实义名词属本格族
             才算合格，属参照数族（总股本·股本总额·总市值·收盘价·前收盘价·交易均价·每股净资产·净利润·归母净利润·
             营业收入·每股收益·已回购数量·已回购金额·成交均价…）且更靠数即剔，**哪怕同一短语别处写了本格名词**；
             数左什么都不剩时看本短语数右；两头都没有名词＝孤立数才继承前序最近一次的本格名词，**前序最近的若是
             参照数则不继承**；⑤每格两元素各自要有落点——「分红方案与每股派息」是派息标准与分红总额两组同时给，
             一枚合格候选只算它那一个要素到位、不替整组放行；**本域不设共指补判**：两格的元素量纲都不同
             （派息标准是元/股、分红总额是元；回购规模是股或元、回购价格上限是元/股），一枚数在结构上不可能同时
             满足两个元素，所以姊妹尺里那条「肯定系词共指」的分支在本域没有适用面，不搬过来；⑥比率（占比·比例·
             上浮·增幅·降幅·折扣·折价·溢价）与转增送股（转增·送股·送红股）**不参与名词归属**，只在原句里逐字登记，
             缺了走「未检索到」。
             射程如实写（首版就写、不等被问）：判的是同一短语内的相邻关系加一次跨短语继承，
             **不声称覆盖所有自然语言的归属表达**；同位式共指（系词在两个名词之后）与「价格待定但数量已定」的
             同段共存式都在已知覆盖不到之列，按严格式发红，请人工回原句核对；短语内定档吃结构体三列偏移，
             孤立数继承与空泛语扫描那两步读的是剥日期与掩分母后的原串对应段，不是结构体本身。
             发红句把被剥的日期、被掩的分母、落空候选、缺的要素与取数域首段一并点名当证据。

用法：
  python3 -B scripts/check_sh_return_card.py <待检文件>      # 逐条发红，全过则 PASS
  python3 -B scripts/check_sh_return_card.py --selftest      # 好样须过、坏样五道齐发、钉阈按整族各钉一档、对照样不误伤、临时件自清
  python3 -B scripts/check_sh_return_card.py --help
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

ITEMS = ("分红方案与每股派息", "分红总额与分红率", "股权登记日与除权除息日", "回购方案与回购规模",
         "回购价格区间与资金来源", "回购用途与注销安排", "减持计划与减持主体", "质押与解押情况")

# 参照数族（外族）：本域里能冒充「派息标准」「分红总额」「回购股份数量」「回购资金总额」的数——
# 股本与市值类、行情类、业绩类、已回购类。这一族是本域最要紧的一格：分红率常写成「占归母净利润的 25%」，
# 净利润与 25% 都在同一句里，不按短语结构体判就会把净利润当分红总额、把比例当派息。
REF_SH = (r"总股本|股本总额|已发行股份|已发行股本|注册资本|总市值|流通市值|市值|"
          r"收盘价|前收盘价|开盘价|最高价|最低价|交易均价|成交均价|每股净资产|净资产|"
          r"归属于上市公司股东的净利润|归母净利润|净利润|合并报表|母公司报表|营业收入|营业总收入|"
          r"基本每股收益|每股收益|母公司未分配利润|可供分配利润|累计未分配利润|未分配利润|"
          r"货币资金|现金储备|资产负债率|已回购数量|已回购金额")
REF_RATIO = (r"占[^，。；]{0,12}(?:比例|比重)|"
             r"前\s*\d{1,3}\s*个?交易日[^，。；]{0,8}(?:均价|价格)|"
             r"\d{1,3}\s*个?交易日[^，。；]{0,8}(?:均价|价格)")

# 两格数字归属（面文里那两个「与」各自的名字）：每格一枚 num 元素，共用同一台结构体机器。
# 一元素判档时，外族＝本格参照数 ∪ 别格元素的名词；同格两元素之间不互为参照数。
# 为什么每格只钉一枚：项名里的「与」两侧常常是**同一个数的两种写法**（每 10 股派 3.5 元 ＝ 每股 0.35 元），
# 或是一组**或**关系（回购规模可写股数也可写金额）。钉两枚会逼着卡面把同一件事写两遍，
# 反而让「只给了一个要素就放行」的漏洞变成「两个要素必须都出现」的假严格。
NUM_CELLS = {
    "分红方案与每股派息": {
        "foreign": re.compile(REF_SH + "|" + REF_RATIO),
        "elements": (
            ("派息标准", "num", re.compile(
                r"每股派发现金红利|每股派发|每股派息|每股派|每股现金红利|每股红利|每股股利|每股分红|"
                r"派息标准|每股税前|每股税后|每十股派")),
        ),
    },
    "分红总额与分红率": {
        "foreign": re.compile(REF_SH + "|" + REF_RATIO),
        "elements": (
            ("分红总额", "num", re.compile(
                r"分红总额|现金分红总额|派发现金红利总额|派发现金红利合计|合计派发现金红利|"
                r"合计派发|合计派息|共派发|合计分红|利润分配总额|现金红利总额|分红金额|派息总额|"
                r"本次分红总额|拟派发现金红利")),
        ),
    },
    "回购方案与回购规模": {
        "foreign": re.compile(REF_SH + "|" + REF_RATIO),
        "elements": (
            ("回购规模", "num", re.compile(
                r"回购股份数量|回购股份总数|回购数量|回购股数|拟回购股份数量|回购规模|"
                r"回购资金总额|回购资金|回购金额|回购总金额|拟回购金额|"
                r"回购上限|回购下限|回购股份的下限|回购股份的上限")),
        ),
    },
    "回购价格区间与资金来源": {
        "foreign": re.compile(REF_SH + "|" + REF_RATIO),
        "elements": (
            ("回购价格上限", "num", re.compile(
                r"回购价格上限|回购价格区间|回购价格|回购价|价格上限|每股回购价|每股价格")),
        ),
    },
}
# 候选形制：金额（元·万元·亿元）∪ 股数（股·万股·亿股）∪ 倍数（倍）∪ 百分比（%·％）。
# 只有带金额或股数量纲的候选才能结算元素；倍·%·％＝比率，只逐字登记（「占归母净利润的 25%」里的 25% 不是分红总额）。
NUM = re.compile(r"\d[\d,\.]*\s*(?:万股|亿股|万元|亿元|元|股|倍|％|%)")
SETTLE_UNIT = re.compile(r"(?:万股|亿股|万元|亿元|元|股)\s*$")
# 比率词与转增送股词：数左紧挨着它们时，那个数给的是占比或股本变动，不是本元素的原值。
RATIO_MARK = re.compile(r"(?:占比|比例|上浮|增幅|降幅|下降|增长|比重|折扣|折价|溢价|"
                        r"转增|送股|送红股|转增股本|送转)\s*[^，。；\d]{0,6}$")
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
# ⚠ COPA_REF 声明但**不接线**：本域不设共指补判（见模块 docstring ⑤）。
# 留着是为了让「为什么没有这条分支」在代码里可查，不是漏用。
SEG_SPLIT = re.compile(r"[，。；：！？]+|[,;](?!\s*\d)")   # 千分位逗号不断段；顿号算枚举不算归属边界
NOUN_WASH = re.compile(r"[员委事大东议工学协商年例常布明谈论聚汇组独立]会|会[计议场话晤所馆堂员]")
# 本域独有的预处理：`每 N 股` 里的 N 是**分母**不是值。
# `每 10 股派 3.50 元` 的 10 是「每十股」这个单位的分母，不掩掉机器会把 10 当成派息值、把 3.50 当成每股值；
# 简写形 `10 派 3.5 元` 同理（`10` 后面没有量纲词，NUM 本来就不收，但 `派` 前没有本格名词，3.5 会成孤立数）。
# 掩成 `每股` / `每股派 ` 之后，本格名词族里的「每股派发」「每股派」就能接住后面的数；被掩的分母进证据串，不静默吞掉。
PER_N = re.compile(r"每\s*(\d{1,4})\s*股")
PER_N_SHORT = re.compile(r"(?<![\d.])(\d{1,4})\s*派\s*(?=\d)")
# 八项名目按「任一表述命中即算在场」认：真实公告里同一项有不同叫法——
# 分红有的写「利润分配」「权益分派」，回购有的写「股份回购」，减持有的写「股份减持」。
# 所以名目不是一枚死字符串，是一族别名；命中任一别名即归到同一枚 canonical 名目上，
# 行级在场、齐缺对账、缺项点名三处都按 canonical 名走，卡面写哪个别名都认。
ITEM_ALIASES = {
    "分红方案与每股派息": ("分红方案与每股派息", "分红方案及每股派息", "利润分配方案与每股派息",
                          "权益分派方案与每股派息", "分红方案与每股股利", "分红派息方案",
                          "利润分配及资本公积金转增股本方案", "年度权益分派方案"),
    "分红总额与分红率": ("分红总额与分红率", "分红总额及分红率", "现金分红总额与分红率",
                        "分红金额与分红比例", "派息总额与派息率"),
    "股权登记日与除权除息日": ("股权登记日与除权除息日", "股权登记日及除权除息日", "股权登记日、除权除息日",
                              "股权登记日与除息日", "登记日与除权除息日"),
    "回购方案与回购规模": ("回购方案与回购规模", "回购方案及回购规模", "股份回购方案与回购规模",
                          "回购方案与回购数量", "回购股份方案与回购规模", "回购方案与回购金额"),
    "回购价格区间与资金来源": ("回购价格区间与资金来源", "回购价格区间及资金来源", "回购价格与资金来源",
                              "回购价格区间与回购资金来源", "回购价格上限与资金来源"),
    "回购用途与注销安排": ("回购用途与注销安排", "回购用途及注销安排", "回购股份用途与注销安排",
                          "回购用途与注销", "回购股份的处置与注销安排"),
    "减持计划与减持主体": ("减持计划与减持主体", "减持计划及减持主体", "股东减持计划与减持主体",
                          "股份减持计划与减持主体", "减持主体与减持计划"),
    "质押与解押情况": ("质押与解押情况", "质押及解押情况", "股权质押与解押情况", "股份质押与解除质押情况",
                      "质押、解押与解除质押情况"),
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

# ── 红线词族（SR-LINE ①）────────────────────────────────────────────────
NOUN_FORM = r"(?![性度论])"
VALUER_WORDS = "|".join(w + NOUN_FORM for w in (
    "合理", "公允", "偏高", "偏低", "充分", "不足", "慷慨", "大方", "优厚", "有诚意", "划算"))
DEGREE_WORDS = r"很|较为|比较|基本|大体|显然|明显|相当"
RETURN_SUBJ = (r"分红率|股息率|分红比例|派息率|回购力度|回购规模|减持规模|质押比例|"
               r"分红方案|回购方案|减持计划|质押")
VALUER_ASSERT = (r"(?:" + RETURN_SUBJ + r")(?:的)?(?:" + DEGREE_WORDS + r")?(?:" + VALUER_WORDS + r")")
IMPL_SUBJ = r"回购|增持|减持|解禁|解锁|分红|派息|注销|实施"
PREDICT_ASSERT = (r"(?:" + IMPL_SUBJ + r")(?:的)?(?:概率|可能性|几率)"
                  r"(?:很|非常|比|较|极)?(?:大|高|小|低|不大|不高|极低)")
PRICE_SUBJ = r"股价|市值|估值|每股收益|市盈率"
PRICE_VERB = r"将|会|有望|必然|势必|可能|预计"
PRICE_DIR = r"上涨|下跌|走高|走低|提振|承压|反弹|回升|回落|提升|下滑|修复"
# 两种语序都收：`股价将上涨` 与 `有望提振股价`。只收前一种会漏掉公告解读里最常见的后一种写法。
PRICE_IMPACT_ASSERT = (r"(?:(?:" + PRICE_SUBJ + r")(?:的)?(?:" + PRICE_VERB + r")"
                       r"[^，。；]{0,6}(?:" + PRICE_DIR + r")"
                       r"|(?:" + PRICE_VERB + r")[^，。；]{0,6}(?:" + PRICE_DIR + r")"
                       r"[^，。；]{0,4}(?:" + PRICE_SUBJ + r"))")
BANNED = re.compile(
    r"是否划算|值得买入|值得卖出|建议买入|建议卖出|建议增持|建议减持|建议持有|"
    r"稳赚|零风险|保证收益|利好|利空|必涨|必跌|抄底|套利|代拟|代算|代客|"
    r"内幕信息|绕开审议|规避披露|损害中小股东利益|损害股东利益|侵占公司利益|"
    + VALUER_ASSERT + r"|" + PREDICT_ASSERT + r"|" + PRICE_IMPACT_ASSERT)
SUBJECT = re.compile(r"分红|派息|送股|转增|回购|注销|减持|增持|质押|解押|解禁|解锁|"
                     r"股权登记|除权除息|股息率|分红率|股价|市值|股东|股本|方案|计划|回报")
TONE = re.compile(r"应当|应予|予以|将|会|必|有望|可期|可能|足以|构成|属于|意味着|支持|成立|推翻|"
                  r"无效|有效|上调|下调|提升|下滑|增加|减少|回升|高于|低于|稳赚|赚|亏|无疑|显然|肯定|"
                  r"应(?!急)|" + VALUER_WORDS + r"|" + PREDICT_ASSERT)
VERDICT = re.compile(r"结论|综上|因此|可见|据此|本院认为|本件认为|本卡认为|本件判断|判定|认定|断言")
EFFECT = re.compile(r"无效|有效|作废|不成立|成立|撤销|违法|违规|合规|属实|构成承诺|应当披露|"
                    r"应予支持|予以支持|应支持|支持|必然")
CITE_LABEL = re.compile(
    r"原文|摘录|引用|节选|摘自|引自|转引|照录|载明|列明|记载|披露|约定|规定|显示|表明|称|据|见|详见|"
    r"草案|计划|公告|报告书|说明书|决议|预案|合同|章程|公示|办法|指引|指导意见|"
    r"核查意见|督导意见|审计报告|评估报告|董事会决议|股东大会决议|股东会决议|"
    r"第[一二三四五六七八九十百零\d]+[节条章项款页行段]|页|行|段")
LABEL_PUNCT = re.compile(r"[\s　（）()【】\[\]：:，,。.、·\-—_/｜|]+")
INNER_LABEL = re.compile(r"^\s*([^，。；：:]{1,12})[：:]")
SELF_REF_LEAD = "据经由按依对向在被将把以因故但而且并或若如虽即则从自于给替为跟同和与及照就"
SELF_REF = re.compile(r"(?:(?<![一-龥])|(?<=[" + SELF_REF_LEAD + r"]))(?:本件|本卡|本速读|笔者)")
DISCLAIM = re.compile(r"不接|不出|不提供|不作|不判|不碰|不做|不代|禁止|未证|无法|不承诺")
PENDING = re.compile(r"\[待人工\]")
CLAUSE = re.compile(r"[；;。，,]")
REF_PRICE = r"回购价格|回购价|价格上限|价格区间|每股价格|每股回购价"
# ⚠ REF_PRICE 声明但**不接线**：回购价格是「回购价格区间与资金来源」这一格的**本格**名词，
# 不是参照数；它出现在 REF_SH 之外是刻意的。留着备下一版做跨格互斥时用。


# ── 基础工具 ────────────────────────────────────────────────────────────

def canon(name: str) -> str:
    """别名 → canonical 名目。"""
    return _ALIAS_TO_CANON.get(name, name)


def core_len(s: str) -> int:
    """书名号内原句的实义字数（剥标点与空白）。"""
    return len(CORE_STRIP.sub("", s or ""))


def parse_item_line(line: str):
    """`- 名目：正文` → (canonical 名目, 正文)；不是项行返回 (None, None)。"""
    m = ITEM.match(line)
    if not m:
        return None, None
    return canon(m.group(1)), line[m.end():]


def quote_field(body: str) -> str:
    """项行里所有书名号内的原句（SR-VALUE 的判据域）。"""
    return " ".join(QUOTES.findall(body))


def is_cite_label(s: str) -> bool:
    return bool(CITE_LABEL.search(LABEL_PUNCT.sub("", s or "")))


def inner_ok(q: str) -> bool:
    """书名号内的 `短标签：` 必须自己也是引注标签，否则不算纯引注。"""
    m = INNER_LABEL.match(q)
    if not m:
        return True
    return is_cite_label(m.group(1))


def no_self_ref(q: str) -> bool:
    """书名号内不得出现本件自指（本件／本卡／本速读／笔者）。"""
    return not SELF_REF.search(q)


def own_field(body: str) -> str:
    """SR-LINE 的判据域：剥掉锚**值**，剥掉**纯引注**的书名号；非纯引注的留在域内照扫。

    ⚠ 只剥锚值本身（`锚：公告 五` 里的「公告 五」是定位词），**锚值之后的分句照扫**。
    早先整段 `锚：` 之后一律丢弃，于是「… 锚：公告 五；建议增持，稳赚」能整句绕过红线——
    锚是行尾标签，不是判据域的终点。
    """
    parts = ANCHOR_SPLIT.split(body)
    head = parts[0]
    for tail in parts[1:]:
        # 锚值＝到第一个分句分隔符为止的定位词；其后的分句是卡面自己写的话，留在域内。
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


def segments_of(text: str):
    out, pos = [], 0
    for m in SEG_SPLIT.finditer(text):
        if m.start() > pos:
            out.append(text[pos:m.start()])
        pos = m.end()
    if pos < len(text):
        out.append(text[pos:])
    return out


def trim_units(s: str) -> str:
    prev = None
    while prev != s:
        prev = s
        s = UNIT_SKIP.sub("", s)
    return s


# ── 短语结构体（SR-VALUE 的机器）────────────────────────────────────────

def build_phrases(text: str, cell: dict):
    """把判据域切成短语表；每短语带本格名词·外族名词·候选三列偏移。

    本域独有的预处理：`每 N 股` 的 N 是分母不是值，先掩成 `每股` 再切短语；
    被掩的分母进证据串，不静默吞掉。
    """
    masked = []
    work = text
    for m in DATE_SPAN.finditer(work):
        masked.append(("日期", m.group(0)))
    work = DATE_SPAN.sub(lambda m: " " * len(m.group(0)), work)
    for m in PER_N.finditer(work):
        masked.append(("分母", m.group(0)))
    work = PER_N.sub("每股", work)
    for m in PER_N_SHORT.finditer(work):
        masked.append(("分母", m.group(0)))
    work = PER_N_SHORT.sub("每股派 ", work)

    phrases = []
    for seg in segments_of(work):
        if not seg.strip():
            continue
        own = []
        for name, _kind, rx in cell["elements"]:
            for m in rx.finditer(seg):
                own.append((m.start(), m.end(), name))
        foreign = [(m.start(), m.end()) for m in cell["foreign"].finditer(seg)]
        cands = []
        for m in NUM.finditer(seg):
            if SETTLE_UNIT.search(m.group(0)):
                cands.append((m.start(), m.end(), m.group(0)))
        phrases.append({"seg": seg, "own": own, "foreign": foreign, "cands": cands})
    return phrases, masked


def _nearest(ph: dict, lo: int, hi: int):
    """在 [lo,hi) 内找最近的实义名词；返回 (kind, name) 或 None。"""
    best = None
    for s, e, name in ph["own"]:
        if s >= lo and e <= hi and (best is None or s > best[2]):
            best = ("own", name, s)
    for s, e in ph["foreign"]:
        if s >= lo and e <= hi and (best is None or s > best[2]):
            best = ("foreign", None, s)
    return None if best is None else (best[0], best[1])


def value_gap(item: str, text: str):
    """两格数字归属。返回 (缺的要素, 已到位的要素→候选, 证据串, 被掩串)。"""
    cell = NUM_CELLS[item]
    phrases, masked = build_phrases(text, cell)
    got = {name: [] for name, _k, _rx in cell["elements"]}
    evidence = []
    last_noun = None          # 前序最近一次实义名词（跨短语继承用）
    for ph in phrases:
        seg, cands = ph["seg"], ph["cands"]
        # 先按偏移顺序更新 last_noun（整短语扫一遍，不只候选附近）
        marks = [(s, "own", n) for s, _e, n in ph["own"]] + \
                [(s, "foreign", None) for s, _e in ph["foreign"]]
        for _s, kind, name in sorted(marks):
            last_noun = (kind, name)
        # 空泛语：本短语写了「另行确定／届时公告／以实际…为准」这类，本短语的数一律不结算——
        # 那是估计值或上限，不是公告承诺的本项数值。不结算不等于静默：进证据串。
        vague = VAGUE.search(seg)
        for i, (cs, ce, ctext) in enumerate(cands):
            if vague:
                evidence.append("空泛语不结算：" + ctext + "（" + vague.group(0) + "）")
                continue
            lo = cands[i - 1][1] if i else 0
            left = seg[lo:cs]
            if RATIO_MARK.search(left):
                evidence.append("比率/送转不结算：" + ctext)
                continue
            hit = _nearest(ph, lo, cs)
            if hit is None:
                hit = _nearest(ph, ce, len(seg))
            if hit is None:
                if last_noun and last_noun[0] == "own":
                    got[last_noun[1]].append(ctext)
                    evidence.append("孤立数继承前序本格名词：" + ctext + "→" + last_noun[1])
                else:
                    evidence.append("孤立数不结算：" + ctext)
                continue
            kind, name = hit
            if kind == "own":
                got[name].append(ctext)
            else:
                evidence.append("参照数更近，不结算：" + ctext)
    gaps = [name for name, kind, _rx in cell["elements"] if kind == "num" and not got[name]]
    return gaps, got, evidence, masked


# ── 五道码 ──────────────────────────────────────────────────────────────

def speed_zone(lines):
    """返回「逐字速读」段的 (起, 止) 行号；没有该段返回 None。"""
    start = None
    for i, ln in enumerate(lines):
        if SPEED_HEAD.match(ln):
            start = i + 1
            continue
        if start is not None and ANY_HEAD.match(ln):
            return start, i
    return (start, len(lines)) if start is not None else None


def check_text(text: str):
    """返回 (findings, stats)。findings = [(码, 行号, 说明)]。"""
    findings = []
    lines = text.splitlines()

    # ── SR-STRUCT ──
    heads = "\n".join(ln for ln in lines if ANY_HEAD.match(ln))
    for label, rx in SECTIONS:
        if not re.search(rx, heads):
            findings.append(("SR-STRUCT", 0, "缺段：" + label))
    zone = speed_zone(lines)
    if zone is None:
        findings.append(("SR-STRUCT", 0, "缺「八项逐字速读」段，八项名目无处占行"))
        zone = (0, 0)
    seen = {}
    for i in range(zone[0], zone[1]):
        name, body = parse_item_line(lines[i])
        if name is None:
            continue
        if name in seen:
            findings.append(("SR-STRUCT", i + 1, "名目重复占行：" + name))
        seen[name] = (i, body)
    for name in ITEMS:
        if name not in seen:
            findings.append(("SR-STRUCT", 0, "速读段内缺名目行：" + name))

    # ── SR-QUOTE ──
    for name, (i, body) in seen.items():
        qs = QUOTES.findall(body)
        if not qs:
            if "未检索到" not in body:
                findings.append(("SR-QUOTE", i + 1, name + "：无书名号原句"))
            continue
        for q in qs:
            if core_len(q) <= 1:
                findings.append(("SR-QUOTE", i + 1, name + "：书名号内原句为空或只剩单字"))
        m = ANCHOR_VAL.search(body)
        if not m:
            findings.append(("SR-QUOTE", i + 1, name + "：缺「锚：」"))
        elif not m.group(1).strip():
            findings.append(("SR-QUOTE", i + 1, name + "：锚值为空"))

    # ── SR-LINE ──
    # 三道判据都按**分句**判：`[待人工]` 与免责句只登记自己那一分句，
    # 同一行后半写的肯定预测照发（不因整行有免责就整行放行）。
    for i, ln in enumerate(lines):
        if not ln.strip():
            continue
        name, body = parse_item_line(ln)
        dom = own_field(body) if name is not None else ln
        for cl in CLAUSE.split(dom):
            if PENDING.search(cl) or DISCLAIM.search(cl):
                continue
            # 机构名里的「会」先按形态洗掉再判语气：董事会／股东大会／监事会／审计委员会／
            # 薪酬与考核委员会都不该因为一个「会」字被当成判断语气（docstring 承诺的那条）。
            tone_dom = NOUN_WASH.sub("", cl)
            for m in BANNED.finditer(cl):
                findings.append(("SR-LINE", i + 1, "定式禁词：" + m.group(0)))
            if name is not None and SUBJECT.search(cl) and TONE.search(tone_dom):
                findings.append(("SR-LINE", i + 1, "主题词×判断语气同段：" + cl.strip()[:40]))
            if VERDICT.search(cl) and EFFECT.search(cl):
                findings.append(("SR-LINE", i + 1, "自裁效力层：" + cl.strip()[:40]))

    # ── SR-COUNT ──
    decls = []
    for i, ln in enumerate(lines):
        for m in DECL.finditer(ln):
            decls.append((i + 1, int(m.group(1))))
    if len(decls) != 1:
        findings.append(("SR-COUNT", 0, "齐缺申报须恰一枚，实有 %d 枚" % len(decls)))
    missing = 0
    for i in range(zone[0], zone[1]):
        name, body = parse_item_line(lines[i])
        if name is not None and "未检索到" in body:
            missing += 1
    if len(decls) == 1 and decls[0][1] != missing:
        findings.append(("SR-COUNT", decls[0][0],
                         "齐缺申报缺 %d 项，速读段实有「未检索到」%d 项" % (decls[0][1], missing)))
    for i, ln in enumerate(lines):
        if EMPTY_LIE.search(ln):
            findings.append(("SR-COUNT", i + 1, "把「未检索到」写成「无该项／没有此项」"))

    # ── SR-VALUE ──
    for item in NUM_CELLS:
        if item not in seen:
            continue
        i, body = seen[item]
        qtext = quote_field(body)
        if not qtext.strip():
            continue
        gaps, got, evidence, masked = value_gap(item, qtext)
        if gaps:
            ev = "；".join(evidence[:4]) or "无候选"
            mk = "；".join("%s=%s" % (k, v) for k, v in masked[:4]) or "无"
            findings.append(("SR-VALUE", i + 1,
                             "%s：缺要素 %s｜已到位 %s｜被掩 %s｜证据 %s"
                             % (item, "、".join(gaps),
                                "、".join("%s=%s" % (k, "/".join(v)) for k, v in got.items() if v) or "无",
                                mk, ev)))

    stats = {"items": len(seen), "missing": missing, "decls": len(decls)}
    return findings, stats


# ── 临时件与自测 ────────────────────────────────────────────────────────

def make_tmp(suffix: str = ".md") -> pathlib.Path:
    root = pathlib.Path(tempfile.mkdtemp(prefix="sh-return-card.", dir=os.environ.get("TMPDIR") or None))
    TMP_ROOTS.append(root)
    return root / ("case" + suffix)


def _cleanup():
    for r in TMP_ROOTS:
        shutil.rmtree(r, ignore_errors=True)
    TMP_ROOTS.clear()


GOOD = """# 股东回报全景卡（样例·好样）

## 一、头部申报
- 文件：示例股份有限公司 2025 年年度权益分派实施公告｜来路：官方原文｜附件腿：未发起
- 共八项·缺 1 项

## 二、八项逐字速读
- 分红方案与每股派息：「每 10 股派发现金红利 3.50 元（含税）」 锚：公告 一、重要内容提示
- 分红总额与分红率：「合计派发现金红利 1.75 亿元」 锚：公告 一、重要内容提示
- 股权登记日与除权除息日：「股权登记日为 2026 年 6 月 12 日」 锚：公告 二、本次权益分派方案
- 回购方案与回购规模：「拟回购股份数量为 500 万股」 锚：公告 三、回购方案
- 回购价格区间与资金来源：「回购价格不超过 12.00 元/股，资金来源为自有资金」 锚：公告 三、回购方案
- 回购用途与注销安排：「回购股份将全部予以注销并减少注册资本」 锚：公告 三、回购方案
- 减持计划与减持主体：未检索到（缺数清单已点名）
- 质押与解押情况：「控股股东本次解除质押 1,200 万股」 锚：公告 五、股东质押情况

## 三、口径对照
- 本卡以公告原文为准；本次未取到第二处披露（董事会决议或法律意见书），两份未齐，口径不判。

## 四、缺数清单
- 缺 1 项：减持计划与减持主体——本次取得的公告未含减持计划，需回减持预披露公告核对。

## 五、待人工
- [待人工] 这份方案对股东的实际回报水平、后续股价走向，全部留人工；本件不接代办，也不碰内幕信息与规避披露的做法。
"""

BAD_STRUCT = GOOD.replace("## 四、缺数清单", "## 四、缺项清单")
BAD_QUOTE = GOOD.replace(
    "- 分红总额与分红率：「合计派发现金红利 1.75 亿元」 锚：公告 一、重要内容提示",
    "- 分红总额与分红率：「」 锚：")
BAD_LINE = GOOD.replace(
    "- [待人工] 这份方案对股东的实际回报水平、后续股价走向，全部留人工；本件不接代办，也不碰内幕信息与规避披露的做法。",
    "- [待人工] 这份方案对股东的实际回报水平留人工；分红方案很合理，回购有望提振股价，建议增持，稳赚。")
BAD_COUNT = GOOD.replace("- 共八项·缺 1 项", "- 共八项·缺 0 项").replace(
    "- 减持计划与减持主体：未检索到（缺数清单已点名）",
    "- 减持计划与减持主体：无该项")
BAD_VALUE = GOOD.replace(
    "- 分红方案与每股派息：「每 10 股派发现金红利 3.50 元（含税）」 锚：公告 一、重要内容提示",
    "- 分红方案与每股派息：「公司总股本 5.00 亿股，2025 年归属于上市公司股东的净利润 7.00 亿元」 锚：公告 一、重要内容提示")


def selftest() -> int:
    bad = 0
    f, _ = check_text(GOOD)
    if f:
        bad += 1
        print("✗ 好样不该发红：", f[:3])
    else:
        print("✓ 好样全过")
    cases = (("SR-STRUCT", BAD_STRUCT), ("SR-QUOTE", BAD_QUOTE), ("SR-LINE", BAD_LINE),
             ("SR-COUNT", BAD_COUNT), ("SR-VALUE", BAD_VALUE))
    for want, txt in cases:
        f, _ = check_text(txt)
        codes = sorted({c for c, _i, _m in f})
        if want in codes:
            print("✓ 坏样发红 %s（共 %d 条）" % (want, len(f)))
        else:
            bad += 1
            print("✗ 坏样未发 %s，实发 %s" % (want, codes))
    # 对照样：好样里那两句免责与 [待人工] 不得误伤
    f, _ = check_text(GOOD)
    if any(c == "SR-LINE" for c, _i, _m in f):
        bad += 1
        print("✗ 对照样误伤 SR-LINE")
    else:
        print("✓ 对照样不误伤")
    _cleanup()
    print("自测：%s" % ("全合" if bad == 0 else "不合 %d 档" % bad))
    return 0 if bad == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="A股股东回报全景卡机检（零网络）")
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
        print("不合 %d 条｜名目 %d 枚｜未检索到 %d 项｜齐缺申报 %d 枚"
              % (len(findings), stats["items"], stats["missing"], stats["decls"]))
        return 1
    print("PASS｜名目 %d 枚｜未检索到 %d 项｜齐缺申报 %d 枚"
          % (stats["items"], stats["missing"], stats["decls"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
