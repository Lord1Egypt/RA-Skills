#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_policy_change.py —— 会计政策变更稿五道机检（PC-STRUCT／PC-QUOTE／PC-CHANGE／PC-RETRO／PC-LINE 五道全实装）。

纯 stdlib、零网络、零外部依赖。
用法：
    check_policy_change.py <会计政策变更稿.md>   # 有发条退 1，全过退 0
    check_policy_change.py --demo               # 打印一份完整合规样例（零输入可跑）
    check_policy_change.py --selftest           # 跑包内夹具自检

退码：0 全过 / 1 有发条 / 2 用法错 / 3 读不到或空稿，或零发条但尚有判据未实装
      （rc=0 的含义是「五道全过」——没跑的道不能算过，与 --selftest 同一条语义）

本件五道全实装：PC-STRUCT、PC-QUOTE、PC-CHANGE、PC-RETRO、PC-LINE。没有空壳、
没有未判道——零发条即 rc=0；--selftest 同一条语义，全部夹具过即退 0。
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-accounting-policy-change-cn"

# ---------------------------------------------------------------- 五个码
# 每道一枚，互不代偿：一道红了不许指望另一道替它说话。
CODES = (
    "PC-STRUCT",   # 形制：头部自标、主体/报告期、七节按序、前五节各至少一条发现行
    "PC-QUOTE",    # 原句与锚：发现行须以「」+〔锚：…〕+[S#] 收尾；来源行带 URL 与检索日
    "PC-CHANGE",   # 变更性质与依据只认原句：法定/自主、依据文号、变更前后处理，不得自补
    "PC-RETRO",    # 追溯调整与不切实可行：金额可追（全部内容节）、追溯／未来适用、替代处理方法
    "PC-LINE",     # 红线：变更合理性评价、盈余管理判断、利润影响测算、评级目标价
)

# ---------------------------------------------------------------- 七节（节名照抄派单）
SECTIONS = (
    "会计政策变更概况",     # ① 变更事项、生效日、是否属于政策变更
    "变更性质与依据",       # ② 法定变更／自主变更、依据文号——只认披露写法
    "变更前后会计处理",     # ③ 变更前怎么算、变更后怎么算，各自一句
    "追溯调整与累积影响",   # ④ 累积影响数、比较报表调整、调整科目
    "不切实可行的处理",     # ⑤ 是否不切实可行、替代处理方法
)
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"
ALL_SECTIONS = SECTIONS + (GAP_SECTION, SOURCE_SECTION)
CONTENT_SECTIONS = SECTIONS

# ---------------------------------------------------------------- 四件头部自标
MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

# ---------------------------------------------------------------- 形制与原句判据的正则
HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")

SUBJECT = re.compile(r"^主体：\s*(\S.*)$")
PERIOD = re.compile(r"^报告期：\s*(\S.*)$")

# 三元组：原句 + 锚 + 来源编号，且必须落在行末（判据看的就是这个收尾形状）。
TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
ANCHOR_BLOCK = re.compile(r"〔\s*锚\s*[:：][^〕]*〕")
ANCHOR_REF = re.compile(r"\[(S\d+)\]")

SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)"
    r"\|\s*(?P<url>https?://\S+)\s*\|"
    r"\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$"
)

# ---------------------------------------------------------------- 判据用词表
# 缺口搪塞词：把「没查到」写成「没有」。
GAP_EXCUSE = ("不适用", "无此项", "无需披露")

# 变更性质三类（PC-CHANGE）。顺序有意义：长词在前，避免「会计政策变更」先吃掉
# 「会计政策变更与会计估计变更难以区分」的前缀而漏掉第三类。
CHANGE_KINDS = (
    "会计政策变更与会计估计变更难以区分",
    "会计估计变更",
    "会计政策变更",
)

# 性质断言词（PC-CHANGE 甲／丙）。只有「变更的**性质类别**」这三个词才算断言；
# 法定变更／自愿变更／强制变更这类是**变更方式**，与性质是不同维度——方式词不判性质。
KIND_CLAIMS = ("会计政策变更", "会计估计变更", "会计政策变更与会计估计变更难以区分")

# 依据行的项名（PC-CHANGE 戊）：登记了依据，原句里必须能找到准则号／解释号／文件名。
BASIS_LABELS = ("变更依据", "依据", "审批依据", "准则依据")

# 依据原句里该出现的东西：解释第 N 号、准则第 N 号、财会〔YYYY〕N 号、或《…》文件名。
BASIS_CUE = re.compile(r"解释第\s*\d+\s*号|准则第\s*\d+\s*号|财会\s*〔\d{4}〕\s*\d+\s*号|《[^》]+》")

# ---------------------------------------------------------------- PC-RETRO 用词与数
# 甲（金额可追）扫全部内容节：金额写在哪一节都得有出处。
# 乙（追溯／未来适用写反）只判这两节；别的节里谈法不归 PC-RETRO 管。
RETRO_SECTIONS = ("追溯调整与累积影响", "不切实可行的处理")
FEASIBLE_SECTION = "不切实可行的处理"

# 金额：数字（可带千分位与小数）+ 单位。长单位在前，否则「万元」会被「元」吃掉后面的字。
AMOUNT = re.compile(
    r"(?P<num>\d[\d,]*(?:\.\d+)?)\s*(?P<unit>亿元|万元|千元|元)")
AMOUNT_SCALE = {"亿元": 1e8, "万元": 1e4, "千元": 1e3, "元": 1.0}
AMOUNT_REL_TOL = 1e-6

# ---------------------------------------------------------------- PC-LINE 红线词
# 红线四族。只收「评级语言」，不收裸动词「增持」「减持」——那两个词单独出现时是
# 普通登记语言（「股东增持计划」是披露原文），收进来会把它判红。
# 甲族按件内惯例按词收（不做「评价语境」识别）：这些词在本件里除了自评没有别的用途。
HARD_BAN = (
    # 甲 变更合理性评价（本件只登记披露怎么写，不替披露判断变更合不合理）
    "变更合理", "有利于", "有助于提升", "旨在优化", "恰当反映", "更真实公允",
    # 乙 盈余管理判断（动机判断是人的事，[待人工]）
    "盈余管理", "调节利润", "利润平滑", "操纵利润", "粉饰报表",
    # 丙 利润影响测算（影响数只能照抄披露，不许本件往前推一期）
    # 裸「预计影响」必收：漏了它，「本件预计影响 2026 年净利润 …」这种往前推一期的
    # 自算句会零发条过关（控制稿 A／B 实测漏判）。
    "预计影响", "增厚利润", "预计增利", "将增厚", "预计减少利润", "预计提升净利润",
    # 丁 评级与目标价（一律 [待人工]，本件不给）
    "评级", "目标价", "目标市值", "值得投资", "低估", "高估",
    "买入评级", "卖出评级", "增持评级", "减持评级", "给予买入", "给予卖出",
    "强烈推荐", "跑赢大盘",
)

# 这两节本来就在说该禁什么，判它等于自伤。节名含这些词即整节跳过。
LINE_EXEMPT_SECTION = ("合规红线", "数据通道")

# 否定语境：紧挨在红线词前面的这几串，说明这一行是在**划本件的边界**（「本件不给评级」），
# 不是在给评级。收口到「紧邻」为止——不做整句否定解析，深度否定不豁免。
# 长串必须排在前面：`text[:i]` 以「不给」结尾时也要认出来，而「给」不在其列。
NEG_BEFORE = ("不给", "不予", "不作", "不出具", "不写", "不做", "不含", "不提",
              "不预测", "不提供", "不推荐", "不给出", "不得", "严禁", "禁止", "不")

# 名词术语豁免：这些词紧接「数／额／金额／数额」时是附注里的金额**名称**
# （「预计影响数」「预计影响金额」与「累积影响数／累积影响金额」同形），是照抄披露，
# 不是本件在预测。只收真能名词化的词——「增厚利润」「预计增利」这类没有同形名词，
# 收了反而放过自推句。
# 后缀只收完整的量名词：不扩到「范围」「区间」（后面常接自推句，收了会放过真红）。
TERM_SUFFIX = ("数", "额", "金额", "数额")
TERM_NOUN_OK = ("预计影响",)


def _negated(text, idx):
    """判 idx 处的红线词是不是被紧邻的否定词罩着。"""
    head = text[max(0, idx - 4):idx]
    return any(head.endswith(neg) for neg in NEG_BEFORE)


def _at_value_head(text, idx):
    """判 idx 处的命中是不是就落在登记值开头（前面只有冒号与空白）。

    照抄型名词（「项名：预计影响数 3,000 万元」）里，术语就是登记值的第一个词；
    在它前面加主语或状语（「管理层预计影响额…」「本件据此测算，预计影响额…」），
    是「谁在预测」——那是本件在说，不是照抄，不豁免。

    这是**白名单**：只认「术语打头」这一种形状，不靠枚举主语。主语与状语永远列不全
    （管理层／本报告／经测算／根据以上…），黑名单补一个漏一个。
    """
    try:
        colon = text.index("：")
    except ValueError:
        return False
    return text[colon + 1:idx].strip() == ""


def _term_after(text, idx, word):
    """判 idx 处的命中是不是名词术语（「预计影响**数**」「预计影响**金额**」＝照抄披露的金额名），
    不是本件在预测。

    紧邻生效，不收远：只看命中词紧跟的两字。术语是行内登记值的一部分，
    和当年 PC-CHANGE 把项名当断言是同一类坑——判据读整行，术语本身也在行内。
    只豁免本次命中：同一行后面再出现的命中要各自判定（「预计影响数 …，本件据此
    预计影响 2027 年净利润」里第二次命中不带后缀，照旧判红）。
    本函数只管后缀形状；命中是否落在登记值开头，由 `_at_value_head` 另行判定。
    """
    tail = text[idx + len(word):idx + len(word) + 2]
    return tail.startswith(TERM_SUFFIX)


def mark_first_run() -> None:
    """首次运行埋点：往 ~/.cue-usage/<slug>-<日期> 落一个空文件。

    解析参数成功后、干正事之前调用；任何失败静默跳过，绝不报错、不改进程退码。
    """
    try:
        root = Path(os.path.expanduser("~")) / ".cue-usage"
        root.mkdir(parents=True, exist_ok=True)
        target = root / f"{SLUG}-{date.today().isoformat()}"
        if not target.exists():
            target.touch()
    except Exception:                                    # noqa: BLE001
        pass


def _section_of(heading):
    """把 `## 3. 变更性质与依据` 归一成 `变更性质与依据`；认不出返回 None（当作 stray）。"""
    h = heading.strip()
    for _ in range(2):
        h2 = NUMBERING.sub("", h)
        if h2 == h:
            break
        h = h2
    h = h.strip()
    for name in ALL_SECTIONS:
        if h == name:
            return name
        if h.startswith(name) and not h[len(name):len(name) + 1].isalnum():
            return name
    return None


def split_doc(text):
    """切成 (头部行, 七节, stray)。同一节名第二次出现一律记 stray（多出同名节）。"""
    lines = text.splitlines()
    header = []
    sections = []
    cur = None
    seen_h2 = False
    stray = []
    for i, raw in enumerate(lines, 1):
        m = HEADING.match(raw)
        if m:
            seen_h2 = True
            name = _section_of(m.group(1))
            if name is None:
                stray.append((i, raw.strip()))
                cur = None
                continue
            if any(name == n for n, _ln, _b in sections):
                stray.append((i, raw.strip()))
                cur = None
                continue
            cur = (name, i, [])
            sections.append(cur)
            continue
        if not seen_h2:
            header.append((i, raw))
        elif cur is not None:
            cur[2].append((i, raw))
    return header, sections, stray


def _is_finding_line(s):
    return s.startswith("- ") or s == "-"


def _is_gap_line(s):
    """一条发现行是不是「未取到」行。

    只认带冒号的登记形（`未取到：原因`）。口径行里会出现「没披露就写未取到」这种**叙述**，
    它不是缺口登记，认错了会给好样发假红。
    """
    return "未取到：" in s or "未取到:" in s


def _is_zero_gap(s):
    """零缺口登记行：`未取到：无`。它不是一条缺口。"""
    return "未取到：无" in s or "未取到:无" in s


def _split_label(s):
    """把发现行切成 (项名, 其余)。项名取第一个全角冒号之前；没有冒号就退回行首词组。"""
    body = re.sub(r"^-\s*", "", s.strip())
    if "：" in body:
        label, rest = body.split("：", 1)
        return label.strip(), rest.strip()
    return body.split("「", 1)[0].strip(), ""


def _registered_value(s):
    """这一行**本件自己登记的**那个值：冒号之后、第一个「」之前那段。

    不能拿整行去数性质词：`〔锚：…附注三·重要会计政策变更〕` 里带「会计政策变更」，
    那是锚点地址不是断言；行首「是否属于会计政策变更」是**项名**不是登记值。
    拿整行数会给出两个方向的假红（好样被判自推、合法登记被判两类）。
    """
    _label, rest = _split_label(s)
    return rest.split("「", 1)[0].strip()


def _quotes(s):
    """取出这一行里所有「」原句。"""
    return QUOTE.findall(s)


def _strip_quotes(text):
    """洗掉引文与锚：引文是证据、锚是地址，红线只判本件自己写的句子。"""
    return ANCHOR_BLOCK.sub("", QUOTE.sub("", text))


def _exempt_triple(s):
    """不要求三元组的三类行：未取到行、[待人工] 行、〔自算〕行。"""
    return _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s


def _not_judged(code):
    """未接线的判据一律从这里抛，绝不返回空表冒充「查过且没问题」。"""
    raise NotImplementedError("%s 判据未实装（骨架期：调用即抛，不产出零发条）" % code)


# ---------------------------------------------------------------- 五道判据
def check_struct(header, sections, stray, add):
    """PC-STRUCT：头部四件自标、主体／报告期、七节齐且有序、前五节各至少一条发现行。"""
    htext = "\n".join(s for _i, s in header)
    for mark in MARK_TEXTS:
        if mark not in htext:
            add("PC-STRUCT", 1, "头部缺自标「%s」" % mark)
    if not any(SUBJECT.match(s) for _i, s in header):
        add("PC-STRUCT", 1, "头部缺 `主体：` 行")
    if not any(PERIOD.match(s) for _i, s in header):
        add("PC-STRUCT", 1, "头部缺 `报告期：` 行")

    names = [n for n, _l, _b in sections]
    for name in ALL_SECTIONS:
        if name not in names:
            add("PC-STRUCT", 1, "缺节「%s」" % name)
    pos = [ALL_SECTIONS.index(n) for n in names]
    if pos != sorted(pos):
        add("PC-STRUCT", 1, "节序不对：现序 %s，应序 %s"
            % ("／".join(names), "／".join(ALL_SECTIONS)))
    for lineno, raw in stray:
        add("PC-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw)

    for name, hline, body in sections:
        if name in CONTENT_SECTIONS:
            n_find = 0
            for lineno, s in body:
                if not s.strip() or s.lstrip().startswith("###"):
                    continue
                if not _is_finding_line(s):
                    add("PC-STRUCT", lineno, "节内只许 `- ` 发现行：%s" % s.strip()[:40])
                    continue
                n_find += 1
            if n_find == 0:
                add("PC-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name)
        elif name == GAP_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not _is_finding_line(s):
                    add("PC-STRUCT", lineno, "第六节只许 `- ` 行：%s" % s.strip()[:40])
        elif name == SOURCE_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not s.lstrip().startswith("- ["):
                    add("PC-STRUCT", lineno, "来源节只许 `- [S#] …` 行：%s" % s.strip()[:40])


def check_quote(sections, add):
    """PC-QUOTE：发现行三元组收尾、来源行带 URL 与检索日、引用编号须已登记。"""
    referenced = []
    defined = set()
    for name, _hline, body in sections:
        if name in CONTENT_SECTIONS:
            for lineno, s in body:
                if not s.strip() or not _is_finding_line(s):
                    continue
                referenced.extend(ANCHOR_REF.findall(s))
                if not TRIPLE.search(s):
                    if not _exempt_triple(s):
                        add("PC-QUOTE", lineno,
                            "发现行缺「」原句 + 〔锚：…〕 + [S#] 三元组：%s" % s.strip()[:40])
                    continue
                for m in TRIPLE.finditer(s):
                    if not m.group("q").strip():
                        add("PC-QUOTE", lineno, "原句为空")
                    if not m.group("a").strip():
                        add("PC-QUOTE", lineno, "锚为空")
                if not re.search(r"\[S\d+\]\s*$", s.strip()):
                    add("PC-QUOTE", lineno, "发现行未以 [S#] 收尾（三元组须在行末）")
        elif name == SOURCE_SECTION:
            for lineno, s in body:
                if not s.strip() or not s.lstrip().startswith("- ["):
                    continue
                m = SOURCE_LINE.match(s.strip())
                if not m:
                    add("PC-QUOTE", lineno,
                        "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:50])
                    continue
                defined.add(m.group("s"))
    for ref in sorted(set(referenced)):
        if ref not in defined:
            add("PC-QUOTE", 1, "正文引用 [%s]，来源节没有对应登记行" % ref)


def _label_of(s):
    """这一行登记的项名（行首到冒号）；没有冒号返回空串。"""
    return _split_label(s)[0]


def _kinds_in(text):
    """从一段文本里取出出现的变更性质类别，按 CHANGE_KINDS 顺序，去重。

    长词优先且取出后从文本里剔掉，避免「会计政策变更与会计估计变更难以区分」被
    同时数成「会计政策变更」与「会计估计变更」两类（那会把一次合法登记判成乙）。
    """
    found = []
    rest = text
    for kind in CHANGE_KINDS:
        if kind in rest:
            found.append(kind)
            rest = rest.replace(kind, "\u0000")
    return found


def check_change(sections, add):
    """PC-CHANGE：变更性质与依据只认原句。

    甲 登记值写了某性质，同一行「」原句里没有该性质词
    乙 同一行登记了两类而原句只写一类
    丙 把「会计估计变更」写成「会计政策变更」（两者追溯处理完全不同）
    丁 整份稿一条性质都没登记时，在第一条发现行发一次（不逐条发）
    戊 登记了依据却原句里没有准则号／解释号／文件名
    """
    any_kind = False
    first_finding_line = None

    for name, _hline, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            if not s.strip() or not _is_finding_line(s):
                continue
            if first_finding_line is None:
                first_finding_line = lineno
            if _is_gap_line(s):
                continue                      # 未取到行是缺口登记，不是性质断言

            label = _label_of(s)
            quoted = "".join(_quotes(s))

            # 取数面＝本件自己登记的那个值（冒号后、第一个「」之前）。
            # 项名里的理念词不是断言；〔锚：…附注三·重要会计政策变更〕是地址不是断言。
            reg_kinds = _kinds_in(_registered_value(s))
            q_kinds = _kinds_in(quoted)         # 原句里有的

            # 丁的取数面：登记值或原句出现过性质词就算登记过。锚点地址里的类别词不算。
            if reg_kinds or q_kinds:
                any_kind = True

            # ---- 性质登记行：只有登记值里真写了类别才判性质，其余行走过去不判
            if reg_kinds:
                # 丙：本行登记「会计政策变更」，原句写的却是「会计估计变更」
                if "会计政策变更" in reg_kinds and "会计估计变更" in q_kinds \
                        and "会计政策变更" not in q_kinds:
                    add("PC-CHANGE", lineno,
                        "登记为「会计政策变更」，原句写的是「会计估计变更」——"
                        "会计估计变更适用未来适用法，会计政策变更原则追溯调整，两者不能混：%s"
                        % s.strip()[:40])
                    continue
                # 甲：登记了某类，原句里一类都没有
                if reg_kinds and not q_kinds:
                    add("PC-CHANGE", lineno,
                        "变更性质系推断，原句无该类词：%s" % s.strip()[:40])
                    continue
                # 乙：登记两类，原句只有一类
                if len(reg_kinds) > 1 and len(q_kinds) == 1:
                    add("PC-CHANGE", lineno,
                        "同期登记两类性质，原句只写一类（%s）：%s"
                        % ("、".join(q_kinds), s.strip()[:40]))
                    continue
                # 原句写了而本件登记值不在原句（比如原句「难以区分」、登记只写「政策变更」）
                missing = [k for k in reg_kinds if k not in q_kinds]
                if missing and q_kinds:
                    add("PC-CHANGE", lineno,
                        "登记「%s」，原句未写该类别：%s"
                        % ("、".join(missing), s.strip()[:40]))

            # ---- 依据行（戊）
            if any(label.startswith(k) for k in BASIS_LABELS):
                if not BASIS_CUE.search(quoted):
                    add("PC-CHANGE", lineno,
                        "变更依据只认原句：登记了「%s」，原句里没有准则号／解释号／文件名：%s"
                        % (label, s.strip()[:40]))

    # 丁：整份稿一条性质都没登记，发一次
    if not any_kind and first_finding_line is not None:
        add("PC-CHANGE", first_finding_line,
            "全稿未登记变更性质（会计政策变更／会计估计变更／难以区分），无法确定追溯与否")


def _amounts_in(text):
    """从一段文本里取金额，折算成元。

    取数前必先剥掉 [S#] 引用与〔…〕锚：锚里常见「第 132 页」「第 18 号」，
    不剥会把引用编号的 1 当成金额（EP 那件踩过的坑）。
    """
    text = ANCHOR_REF.sub(" ", text)
    text = ANCHOR_BLOCK.sub(" ", text)
    out = []
    for m in AMOUNT.finditer(text):
        try:
            num = float(m.group("num").replace(",", ""))
        except ValueError:
            continue
        out.append(num * AMOUNT_SCALE[m.group("unit")])
    return out


def _amount_close(a, b):
    """相对容差比金额：折算后相等（含 1,200.00 万元 ↔ 12,000,000.00 元）。"""
    if a == b:
        return True
    denom = max(abs(a), abs(b))
    if denom == 0:
        return True
    return abs(a - b) / denom <= AMOUNT_REL_TOL


def _fmt_amount(v):
    return ("%d" % v) if float(v).is_integer() else ("%.2f" % v)


def _check_amounts_backed(lineno, s, add, where=""):
    """登记值里的每个金额，同行「」引文里必须找得到可折算相等的数。

    影响数只能照抄披露：本件自己算出来的数，无论写在哪个内容节，都不可追。
    返回 True 表示已发条（调用方据此跳过本行后续判项，避免一条行叠几条同因发条）。
    """
    reg_amts = _amounts_in(_registered_value(s))
    if not reg_amts:
        return False
    q_amts = _amounts_in("".join(_quotes(s)))
    unmatched = [a for a in reg_amts
                 if not any(_amount_close(a, q) for q in q_amts)]
    if not unmatched:
        return False
    add("PC-RETRO", lineno,
        "登记金额 %s 在引文里找不到对应数（原句金额：%s）%s：%s"
        % ("、".join(_fmt_amount(a) for a in unmatched),
           "、".join(_fmt_amount(a) for a in q_amts) or "无", where,
           s.strip()[:40]))
    return True


def check_retro(sections, add):
    """PC-RETRO：登记的数与法是照抄披露，还是本件自己算的。

    甲（**全部五个内容节**）登记值有金额（元／万元／亿元／千元），同行原句里没有
       可折算相等的数。金额不可追的句子写在哪一节都不行——原先只判追溯两节，
       结果「变更前后会计处理」里登记 9,999 万元、引文说 3,000 万元照样零发条。
    乙（追溯两节）登记值写「追溯调整」而原句写「未来适用法」，或反过来
    丙（不切实可行节）＝否却登记了替代处理方法；＝是却没有（非未取到的）替代处理方法

    跳过「未取到：」行、含 [待人工] 的行、含〔自算〕的行——前两类是缺口登记或
    判断留人，〔自算〕行本来就是本件算的，不拿引文核对。

    本拍**不判**年份（引文 2026、登记 2027 这种推期）：年份写法太多
    （2027／二〇二七／下一年度），要单独设计，别顺手加。
    """
    for name, _hline, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        in_retro = name in RETRO_SECTIONS

        if name == FEASIBLE_SECTION:
            _check_feasible(body, add)

        for lineno, s in body:
            if not s.strip() or not _is_finding_line(s):
                continue
            if _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s:
                continue
            reg = _registered_value(s)
            quoted = "".join(_quotes(s))

            # 甲：金额对不上（全部内容节）
            if _check_amounts_backed(lineno, s, add,
                                     "" if in_retro else "（非追溯节）"):
                continue

            if not in_retro:
                continue                      # 乙只在追溯两节判

            # 乙：追溯／未来适用写反
            if ("追溯调整" in reg and "未来适用法" in quoted
                    and "追溯调整" not in quoted):
                add("PC-RETRO", lineno,
                    "登记「追溯调整」，原句写的是「未来适用法」——两者适用前提不同：%s"
                    % s.strip()[:40])
                continue
            if ("未来适用法" in reg and "追溯调整" in quoted
                    and "未来适用法" not in quoted):
                add("PC-RETRO", lineno,
                    "登记「未来适用法」，原句写的是「追溯调整」——两者适用前提不同：%s"
                    % s.strip()[:40])


def _check_feasible(body, add):
    """丙：不切实可行的是／否与替代处理方法要自洽（只在「不切实可行的处理」节判）。"""
    verdicts = []            # (lineno, 「是」／「否」)
    alt_lines = []           # (lineno, 是否未取到行)
    for lineno, s in body:
        if not s.strip() or not _is_finding_line(s):
            continue
        label = _label_of(s)
        reg = _registered_value(s)
        if label.startswith("是否不切实可行"):
            # 是／否只按登记值判，不看引文
            if reg.startswith("是"):
                verdicts.append((lineno, "是"))
            elif reg.startswith("否"):
                verdicts.append((lineno, "否"))
        elif label.startswith("替代处理方法"):
            alt_lines.append((lineno, _is_gap_line(s)))

    real_alt = [ln for ln, is_gap in alt_lines if not is_gap]
    for lineno, verdict in verdicts:
        if verdict == "否" and real_alt:
            add("PC-RETRO", real_alt[0],
                "登记「不切实可行：否」（L%d），却登记了替代处理方法——"
                "不切实可行才需要替代处理" % lineno)
        elif verdict == "是" and not real_alt:
            add("PC-RETRO", lineno,
                "登记「不切实可行：是」，但替代处理方法%s"
                % ("只登记为未取到" if alt_lines else "没有登记"))


def check_line(sections, add):
    """PC-LINE：变更合理性评价、盈余管理判断、利润影响测算、评级与目标价零命中。

    只判本件自己写的字：`_strip_quotes` 先洗掉「」原句与〔锚〕——披露原文里提到
    「利润影响」「评级」是在说话，不是本件在判断。
    节名含「合规红线」「数据通道」的整节跳过，否则一把尺量到写尺子的那一页上。
    紧邻否定词的不算违规：「本件不作盈余管理判断、不给评级」是边界声明。
    """
    for name, _l, body in sections:
        if any(w in name for w in LINE_EXEMPT_SECTION):
            continue
        for lineno, raw in body:
            s = raw.strip()
            if not _is_finding_line(s):
                continue
            own = _strip_quotes(s)
            hit = None
            for w in HARD_BAN:
                if any(not _negated(own, m.start())
                       and not (w in TERM_NOUN_OK and _term_after(own, m.start(), w)
                                and _at_value_head(own, m.start()))
                       for m in re.finditer(re.escape(w), own)):
                    hit = w
                    break
            if hit:
                label, _rest = _split_label(s)
                add("PC-LINE", lineno,
                    "「%s」踩了红线词「%s」：变更合理性评价、盈余管理判断、利润影响测算、"
                    "评级与目标价都不是本件的判项——%s" % (label[:16], hit, s[:40]))


# 五道全部实装。
IMPLEMENTED = ("PC-STRUCT", "PC-QUOTE", "PC-CHANGE", "PC-RETRO", "PC-LINE")
UNIMPLEMENTED = ()

# 空壳函数自证用：调用即抛 NotImplementedError 才算「没装成零发条」。
SHELLS = ()


def check_text(text):
    """返回 (findings, unjudged)。

    空壳判据调用即抛 NotImplementedError；这里捕获后计进 unjudged，**不让整份稿崩**——
    一份稿子是否合规不该因为尺子没接线就报 Traceback，但没接线的道也不能算「查过」。
    """
    findings = []
    unjudged = []
    stats = {"发现行": 0, "来源": 0}

    def add(code, lineno, msg):
        findings.append((code, lineno, msg))

    header, sections, stray = split_doc(text)

    check_struct(header, sections, stray, add)
    check_quote(sections, add)

    for code, fn in (("PC-CHANGE", check_change), ("PC-RETRO", check_retro),
                     ("PC-LINE", check_line)):
        try:
            fn(sections, add)
        except NotImplementedError:
            unjudged.append(code)

    for name, _hline, body in sections:
        for _lineno, s in body:
            if s.strip() and _is_finding_line(s):
                stats["发现行"] += 1
    for name, _hline, body in sections:
        if name != SOURCE_SECTION:
            continue
        for _lineno, s in body:
            if SOURCE_LINE.match(s.strip()):
                stats["来源"] += 1

    findings.sort(key=lambda x: (x[1], CODES.index(x[0])))
    return findings, unjudged, stats


def report(path, findings, unjudged, stats):
    print("稿：%s" % path)
    print("统计：发现行 %d ｜ 来源 %d" % (stats["发现行"], stats["来源"]))
    if not findings:
        print("结论：五道全过（零发条）")
    else:
        print("结论：发条 %d" % len(findings))
        for code, lineno, msg in findings:
            print("  %s L%-4d %s" % (code, lineno, msg))
        hit = sorted(set(c for c, _l, _m in findings))
        print("发条码：%s" % "、".join(hit))
    if unjudged:
        # rc=0 的含义是「五道全过」。有没跑的道，就不许说全过——退码由调用方按这里判定。
        for code in unjudged:
            print("不可判 %s：判据未实装" % code)
        print("注：以上 %d 道未判，**这不等于合规**；本稿不能按「零发条」读。" % len(unjudged))


# ---------------------------------------------------------------- 样例（--demo）
# 这份样例是好样的唯一定义处：它必须零发条。接上剩余一道后它仍须零发条。
DEMO = r"""# 示例材料（600000.SH）会计政策变更登记稿

> 本稿为 AI 整理初稿，请回原文核对；不构成投资建议。

主体：示例科技股份有限公司（600000.SH）
报告期：2025 年度
判断位 [待人工]：本件只登记披露怎么写，判断留给人。

## 会计政策变更概况

- 变更事项：执行企业会计准则解释第 18 号「本公司自 2025 年 1 月 1 日起执行财政部发布的企业会计准则解释第 18 号」〔锚：2025 年年报·第 132 页·附注三·重要会计政策变更〕[S1]
- 生效日：2025 年 1 月 1 日「上述会计政策变更自 2025 年 1 月 1 日起施行」〔锚：2025 年年报·第 132 页·附注三·重要会计政策变更〕[S1]
- 是否属于会计政策变更：是「本次变更属于会计政策变更」〔锚：2025 年年报·第 132 页·附注三·重要会计政策变更〕[S1]

## 变更性质与依据

- 变更依据：企业会计准则解释第 18 号「本次变更系依据财政部《企业会计准则解释第 18 号》的要求进行」〔锚：2025 年年报·第 132 页·附注三·重要会计政策变更〕[S1]
- 变更性质：法定变更「本次变更属于法律、行政法规或国家统一的会计制度要求进行的变更」〔锚：2025 年年报·第 132 页·附注三·重要会计政策变更〕[S1]

## 变更前后会计处理

- 变更前处理：按已收或应收对价的公允价值计量「变更前，本公司按已收或应收对价的公允价值确认收入」〔锚：2025 年年报·第 133 页·附注三·重要会计政策变更〕[S1]
- 变更后处理：按履约进度确认收入「变更后，本公司按履约进度确认收入」〔锚：2025 年年报·第 133 页·附注三·重要会计政策变更〕[S1]

## 追溯调整与累积影响

- 累积影响数：调减期初留存收益 12,000,000.00 元「本次会计政策变更的累积影响数为调减期初留存收益 12,000,000.00 元」〔锚：2025 年年报·第 133 页·附注三·重要会计政策变更〕[S1]
- 比较报表调整：调减上年营业收入 30,000,000.00 元「相应调减比较报表上年营业收入 30,000,000.00 元」〔锚：2025 年年报·第 133 页·附注三·重要会计政策变更〕[S1]

## 不切实可行的处理

- 是否不切实可行：否「本公司不存在不切实可行的情况」〔锚：2025 年年报·第 133 页·附注三·重要会计政策变更〕[S1]
- 替代处理方法：未取到：附注未披露替代处理方法

## 口径与未取到

- 口径：变更性质、依据与变更前后处理一律照抄附注原句，不按准则条文自补。
- 口径：累积影响数与比较报表调整各自登记，不把两个数互相印证。
- 未取到：替代处理方法

## 来源

- [S1] 示例科技股份有限公司 2025 年年度报告 | https://example.invalid/600000-2025.pdf | 检索日 2026-11-14 | 类型：年报
"""


def _must_replace(text, old, new):
    """注入必须真落地：对不上就抛，别静默产出原文（否则「该红没红」会被读成机检漏判）。"""
    if old not in text:
        raise RuntimeError("夹具注入点对不上：%r" % old[:60])
    return text.replace(old, new, 1)


def _struct_bad_sample():
    """坏样（PC-STRUCT）：把一个节标题改成认不出的写法 ⇒ 该节缺、且整节变 stray。"""
    return _must_replace(DEMO, "## 变更性质与依据", "## 变更依" + "据（旧标题）")


def _quote_bad_sample():
    """坏样（PC-QUOTE）：挑一条有完整三元组、又不是「未取到」的发现行，只摘掉三元组。

    摘三元组不能摘在未取到行上：那行本来豁免，摘了什么都不发。
    """
    return _must_replace(
        DEMO,
        "「本次变更属于会计政策变更」〔锚：2025 年年报·第 132 页·附注三·重要会计政策变更〕[S1]",
        "[S1]")


def _change_two_kinds_sample():
    """坏样（PC-CHANGE 乙）：登记值写两类、原句只写一类 ⇒ 恰发 PC-CHANGE。"""
    return _must_replace(
        DEMO,
        "- 是否属于会计政策变更：是「本次变更属于会计政策变更」",
        "- 是否属于会计政策变更：会计政策变更与会计估计变更「本次变更属于会计政策变更」")


def _change_label_kind_sample():
    """反证（缺陷甲回归）：项名带类别词、登记值只写变更方式 ⇒ 不发 PC-CHANGE。

    「法定变更」是变更**方式**不是类别断言；项名「会计政策变更性质」也不是登记值。
    """
    return _must_replace(
        DEMO,
        "- 变更性质：法定变更",
        "- 会计政策变更性质：法定变更")


def _change_quote_only_sample():
    """反证：类别词只在「」引文里、登记值不写 ⇒ 不发 PC-CHANGE。"""
    return _must_replace(
        DEMO,
        "- 变更事项：执行企业会计准则解释第 18 号"
        "「本公司自 2025 年 1 月 1 日起执行财政部发布的企业会计准则解释第 18 号」",
        "- 变更事项：执行解释第 18 号「本次会计政策变更自 2025 年 1 月 1 日起执行」")


def _retro_amount_bad_sample():
    """坏样（PC-RETRO 甲）：登记值金额与原句金额对不上 ⇒ 只发 PC-RETRO。"""
    return _must_replace(
        DEMO,
        "- 累积影响数：调减期初留存收益 12,000,000.00 元",
        "- 累积影响数：调减期初留存收益 13,000,000.00 元")


def _retro_amount_scaled_sample():
    """反证：登记值写万元、原句写元，折算相等 ⇒ 不发 PC-RETRO。"""
    return _must_replace(
        DEMO,
        "- 累积影响数：调减期初留存收益 12,000,000.00 元",
        "- 累积影响数：调减期初留存收益 1,200.00 万元")


def _retro_feasible_bad_sample():
    """坏样（PC-RETRO 丙）：登记「不切实可行：是」而原句写「不存在」，替代处理仍是未取到。"""
    return _must_replace(
        DEMO,
        "- 是否不切实可行：否「本公司不存在不切实可行的情况」",
        "- 是否不切实可行：是「本公司不存在不切实可行的情况」")


def _line_forecast_bad_sample():
    """坏样（PC-LINE 丙）：本件自己往前推一期，登记「预计影响 2026 年净利润」⇒ 恰发 PC-LINE。

    影响数只能照抄披露；登记值却是本件自算的数。行里三元组齐全，所以 PC-QUOTE 不该跟着红。
    引文里刻意带上同一个金额，是为了让金额可追（PC-RETRO 甲不发）——这一档单锁红线丙组，
    否则会同时踩中「登记金额在引文里找不到」而分不清是哪道判出来的。
    """
    return _must_replace(
        DEMO,
        "## 变更前后会计处理\n\n",
        "## 变更前后会计处理\n\n"
        "- 影响测算：本件预计影响 2026 年净利润 3,000 万元"
        "「本次会计政策变更预计影响 2026 年净利润 3,000 万元」"
        "〔锚：2025 年年报·第 138 页·附注三·重要会计政策变更〕[S1]\n\n")


def _line_forecast_term_sample():
    """反证（名词术语不红）：登记「预计影响数 3,000.00 万元」＋照抄原句 ⇒ 零发条。

    「预计影响**数**」是附注里的金额名称（与「累积影响数」同形），是照抄披露，
    不是本件往前推一期。这一档与上一档必须一绿一红同时在场：证明判据分得开
    名词与动词，而不是碰巧都红或都绿。

    注意术语必须落在**引文外**（登记值里）才测得到 `_term_after`：写成
    「- 净利润影响数：3,000.00 万元「…预计影响…」」时「预计影响」只在引文里，
    引文先被洗掉，那一版夹具不接 `_term_after` 也照样绿，锁不住这个形状。
    """
    return _must_replace(
        DEMO,
        "## 追溯调整与累积影响\n\n",
        "## 追溯调整与累积影响\n\n"
        "- 影响测算：预计影响数 3,000.00 万元"
        "「本次会计政策变更预计影响 2026 年净利润 3,000 万元」"
        "〔锚：2025 年年报·第 140 页·附注三·重要会计政策变更〕[S1]\n\n")


def _line_forecast_amount_term_sample():
    """反证（名词术语不红·「金额」后缀）：登记「预计影响金额 3,000.00 万元」＋照抄原句 ⇒ 零发条。

    「预计影响**金额**」与「累积影响金额」同形，是附注里的标准列名，照抄不是自推。
    后缀首字是「金」，只写「数／额」收不到——这一档专锁这一点。
    """
    return _must_replace(
        DEMO,
        "## 追溯调整与累积影响\n\n",
        "## 追溯调整与累积影响\n\n"
        "- 净利润影响数：预计影响金额 3,000.00 万元"
        "「本次会计政策变更预计影响 2026 年净利润 3,000 万元」"
        "〔锚：2025 年年报·第 140 页·附注三·重要会计政策变更〕[S1]\n\n")


def _line_forecast_selfnoun_sample():
    """坏样（主语 + 名词后缀）：登记值写「本件预计影响额（2027 年）3,000.00 万元」⇒ 恰发 PC-LINE。

    这句同时满足旧夹具的所有「绿」条件：带「额」后缀（像照抄列名）、金额在原句里找得到、
    结构三元组齐全——但它把引文的 2026 推成 2027，且术语前面有主语。术语豁免只认
    「术语打头」（`_at_value_head`），前面加了字就不算照抄。
    """
    return _must_replace(
        DEMO,
        "## 追溯调整与累积影响\n\n",
        "## 追溯调整与累积影响\n\n"
        "- 净利润影响数：本件预计影响额（2027 年）3,000.00 万元"
        "「本次会计政策变更预计影响 2026 年净利润 3,000 万元」"
        "〔锚：2025 年年报·第 140 页·附注三·重要会计政策变更〕[S1]\n\n")


def _line_forecast_mgmt_sample():
    """坏样（非自指主语 + 名词后缀）：登记值写「管理层预计影响额 3,000.00 万元」⇒ 恰发 PC-LINE。

    「管理层」不在任何自指主语词表里——黑名单式豁免补一个漏一个。白名单只看
    术语是否打头：前面有「管理层」，就不是照抄列名。
    """
    return _must_replace(
        DEMO,
        "## 追溯调整与累积影响\n\n",
        "## 追溯调整与累积影响\n\n"
        "- 净利润影响数：管理层预计影响额 3,000.00 万元"
        "「本次会计政策变更预计影响 2026 年净利润 3,000 万元」"
        "〔锚：2025 年年报·第 140 页·附注三·重要会计政策变更〕[S1]\n\n")


def _line_forecast_report_sample():
    """坏样（「本报告」主语 + 名词后缀）：登记值写「本报告预计影响额 3,000.00 万元」⇒ 恰发 PC-LINE。"""
    return _must_replace(
        DEMO,
        "## 追溯调整与累积影响\n\n",
        "## 追溯调整与累积影响\n\n"
        "- 净利润影响数：本报告预计影响额 3,000.00 万元"
        "「本次会计政策变更预计影响 2026 年净利润 3,000 万元」"
        "〔锚：2025 年年报·第 140 页·附注三·重要会计政策变更〕[S1]\n\n")


def _line_forecast_adverbial_sample():
    """坏样（主语 + 状语，拉开距离）：登记值写「本件据此测算，预计影响额 3,000.00 万元」⇒ 恰发 PC-LINE。

    最能体现绕过的一档：命中词前面既有主语又有状语、离得很远。紧邻窗口式的
    主语判定（只看前 3 字）在这里必漏；白名单只看「术语是否登记值第一个词」，不受距离影响。
    """
    return _must_replace(
        DEMO,
        "## 追溯调整与累积影响\n\n",
        "## 追溯调整与累积影响\n\n"
        "- 净利润影响数：本件据此测算，预计影响额 3,000.00 万元"
        "「本次会计政策变更预计影响 2026 年净利润 3,000 万元」"
        "〔锚：2025 年年报·第 140 页·附注三·重要会计政策变更〕[S1]\n\n")


def _line_forecast_pure_term_sample():
    """反证（纯术语打头）：登记值写「预计影响数额 3,000.00 万元」，前面只有冒号空白 ⇒ 零发条。

    与上一档互为对照：同样的词、同样的后缀，唯一的区别是术语前面有没有主语／状语。
    """
    return _must_replace(
        DEMO,
        "## 追溯调整与累积影响\n\n",
        "## 追溯调整与累积影响\n\n"
        "- 净利润影响数：预计影响数额 3,000.00 万元"
        "「本次会计政策变更预计影响 2026 年净利润 3,000 万元」"
        "〔锚：2025 年年报·第 140 页·附注三·重要会计政策变更〕[S1]\n\n")


def _amount_unbacked_nonretro_sample():
    """坏样（PC-RETRO 甲·非追溯节）：在「变更前后会计处理」登记 9,999.00 万元，引文说 3,000 万元。

    金额不可追的句子写在哪一节都不行。原先甲只扫追溯两节，于是这一行全绿——
    术语打头、结构齐全、PC-LINE 不认这个词，唯一异常就是那个数凭空来的。
    """
    return _must_replace(
        DEMO,
        "## 变更前后会计处理\n\n",
        "## 变更前后会计处理\n\n"
        "- 净利润影响数：预计影响数额 9,999.00 万元"
        "「本次会计政策变更预计影响 2026 年净利润 3,000 万元」"
        "〔锚：2025 年年报·第 140 页·附注三·重要会计政策变更〕[S1]\n\n")


def _codes(text):
    findings, unjudged, _stats = check_text(text)
    return findings, unjudged, set(c for c, _l, _m in findings)


def selftest():
    cases = (
        ("好样应零发条（五道）", DEMO, set()),
        ("坏样：一节标题认不出（缺节 + stray）", _struct_bad_sample(), {"PC-STRUCT"}),
        ("坏样：一条发现行丢三元组", _quote_bad_sample(), {"PC-QUOTE"}),
        ("坏样：登记值写两类、原句只写一类", _change_two_kinds_sample(), {"PC-CHANGE"}),
        ("反证：项名带类别词、登记值只写方式", _change_label_kind_sample(), set()),
        ("反证：类别词只在引文里、登记值不写", _change_quote_only_sample(), set()),
        ("坏样：登记金额与原句金额对不上", _retro_amount_bad_sample(), {"PC-RETRO"}),
        ("反证：万元与原句元折算相等", _retro_amount_scaled_sample(), set()),
        ("坏样：登记「是」却没有替代处理方法", _retro_feasible_bad_sample(), {"PC-RETRO"}),
        ("坏样：本件自推一期利润影响（预计影响）", _line_forecast_bad_sample(), {"PC-LINE"}),
        ("反证：照抄术语「预计影响数」不算自推", _line_forecast_term_sample(), set()),
        ("反证：照抄术语「预计影响金额」不算自推", _line_forecast_amount_term_sample(), set()),
        ("坏样：自指主语套名词后缀（本件预计影响额）", _line_forecast_selfnoun_sample(), {"PC-LINE"}),
        ("坏样：非自指主语套名词后缀（管理层预计影响额）", _line_forecast_mgmt_sample(), {"PC-LINE"}),
        ("坏样：本报告主语套名词后缀", _line_forecast_report_sample(), {"PC-LINE"}),
        ("坏样：主语＋状语拉开距离（本件据此测算，预计影响额）", _line_forecast_adverbial_sample(), {"PC-LINE"}),
        ("反证：纯术语打头「预计影响数额」不算自推", _line_forecast_pure_term_sample(), set()),
        ("坏样：非追溯节登记金额在引文里找不到", _amount_unbacked_nonretro_sample(), {"PC-RETRO"}),
    )
    bad = 0
    for label, text, want in cases:
        findings, _unjudged, got = _codes(text)
        if got == want:
            print("过   %s（发条 %d 条：%s）"
                  % (label, len(findings), "、".join(sorted(got)) or "无"))
        else:
            bad += 1
            detail = "；".join("%s L%d %s" % (c, l, m) for c, l, m in findings[:4])
            print("不合 %s：期望 %s 实得 %s ｜ %s"
                  % (label, sorted(want) or "无", sorted(got) or "无", detail))

    # 全实装自证：五道都接线之后，不许再有空壳，也不许 check_text 报不可判。
    shells_n = len(SHELLS)
    unimpl_n = len(UNIMPLEMENTED)
    _f0, unj0, _s0 = check_text(DEMO)
    all_wired = (shells_n == 0 and unimpl_n == 0 and list(unj0) == [])
    print("全实装自证：空壳 %d 道｜UNIMPLEMENTED %d 道｜check_text 不可判 %d 条 %s"
          % (shells_n, unimpl_n, len(unj0), "（五道全接线）" if all_wired else "（失败：仍有未接线道）"))
    if not all_wired:
        bad += 1

    # 不崩自证：整份稿遇上未接线的空壳，仍须走完 check_text 并返回，不裸抛。
    try:
        _f, unj, _s = check_text(DEMO)
        survived = unj == list(UNIMPLEMENTED)
    except NotImplementedError:
        survived = False
    print("不崩自证：check_text 捕获空壳并计不可判 %s"
          % ("（未裸抛）" if survived else "（失败：裸抛或不可判清单不符）"))
    if not survived:
        bad += 1

    # 单稿退码自证：喂一份**好样单稿**走 main()，必须 rc=0 且输出说五道全过、不出现不可判。
    # 零发条但仍有道未判，退回 0 就等于替五道签了字。
    import contextlib
    import io
    import tempfile
    rc_single, out_single, tmp = None, "", None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8",
                                         delete=False) as fh:
            fh.write(DEMO)
            tmp = fh.name
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_single = main([tmp])
        out_single = buf.getvalue()
    except Exception:                                     # noqa: BLE001
        rc_single = None
    finally:
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass
    single_ok = (rc_single == 0 and "不可判" not in out_single
                 and ("五道全过" in out_single or "零发条" in out_single))
    print("单稿退码自证：好样单稿 rc=%s（期望 0）｜输出含「全过」=%s｜含「不可判」=%s"
          % (rc_single, ("五道全过" in out_single or "零发条" in out_single),
             "不可判" in out_single))
    if not single_ok:
        bad += 1

    print("——")
    what = {"PC-CHANGE": "变更性质与依据", "PC-RETRO": "追溯调整与不切实可行",
            "PC-LINE": "红线"}
    for code in UNIMPLEMENTED:
        print("不可判 %s %s：判据未实装" % (code, what[code]))
    # 档数 = 用例档 + 未实装档（2.1 定、lead 认的口径），按公式算不按口头数字。
    print("自测档数=%d｜不合=%d｜不可判=%d"
          % (len(cases) + len(UNIMPLEMENTED), bad, len(UNIMPLEMENTED)))
    if bad:
        return 1
    return 3 if UNIMPLEMENTED else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="会计政策变更稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="会计政策变更稿 .md 路径")
    ap.add_argument("--selftest", action="store_true", help="跑包内夹具自检")
    ap.add_argument("--demo", action="store_true", help="打印一份完整合规样例（零输入可跑）")
    args = ap.parse_args(argv)

    mark_first_run()                                     # ← 解析成功之后、干正事之前

    if args.selftest:
        return selftest()
    if args.demo:
        sys.stdout.write(DEMO)
        return 0
    if not args.path:
        ap.print_usage(sys.stderr)
        print("缺入参：给一份会计政策变更稿路径，或用 --demo / --selftest", file=sys.stderr)
        return 2
    try:
        with open(args.path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except (IOError, OSError) as exc:
        print("读不到文件：%s（%s）" % (args.path, exc))
        return 3
    if not text.strip():
        print("空稿：%s" % args.path)
        return 3

    findings, unjudged, stats = check_text(text)
    report(args.path, findings, unjudged, stats)
    # 退码语义与 --selftest 同一条：有发条退 1；零发条但有未判道退 3。
    # rc=0 只留给「五道全过」——有没跑的就没资格说全过。
    if findings:
        return 1
    if unjudged:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
