#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_deferred_tax.py — 递延所得税稿五道机检（零网络、零外发、不读环境变量）

用法：
    python3 scripts/check_deferred_tax.py <递延所得税稿>.md
    python3 scripts/check_deferred_tax.py --selftest
    python3 scripts/check_deferred_tax.py --demo     打印一份完整合规样例（零输入可跑）

道一 DT-STRUCT 形制
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]；
  `主体：` 行在场且非空；`报告期：` 行在场且非空；
  七节齐且按序：递延所得税资产与负债明细／未经抵销的递延所得税资产与负债／
  未确认递延所得税资产的可抵扣亏损／所得税费用与会计利润的调节表／税率与主体口径／
  口径与未取到／来源；
  前五节各至少一条 `- ` 发现行，节内只许 `- ` 发现行、`### ` 子标题与空行。

道二 DT-QUOTE 原句与锚
  每条数字行必须以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；原句与锚不得为空；
  例外只有三形：「未取到」行（缺的就是那份材料）、[待人工] 行（判断位）与〔自算〕行（本件自己算的）；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址，检索日缺一不可；
  正文引用的每个 [S#] 必须在来源节有对应行。

道三 DT-NOSELF 不得自推自算（本件承重格）
  一、互抵只认原句：写「互抵」「抵销」「轧差」的，同一行「」原句里必须也写得到——
      互抵是披露给的列报选择与金额，不是本件做减法；「资产减负债」不是抵销额。
  二、未确认只认原句：写「未确认递延所得税资产」「未予确认」的，原句同理。
  三、百分数：行内出现 `25%` 一类数值，必须能在同一行的「」原句里逐字找到；
      找不到的须标〔自算〕，且同一行同时给出 `分子…[S#]` 与 `分母…[S#]`。
  四、税率不许落默认值：行内谈税率（法定／优惠／适用税率）而该百分比在同一行原句里找不到的，
      属「按 25% 默认值补」——即使标了〔自算〕也不放过，税率只认披露写法。
  五、未取到行整行豁免比值判定：那一行的百分比与数字是在标「没取到的是哪一项」，不是本件算的。

道四 DT-GAP 未取到两向点名
  正文（一至五节）写「未取到 X」⇒ 第六节必须点名 X；第六节点名了 X 而正文没有 ⇒ 同样发；两向都判。
  零缺口时，第六节须显式写 `未取到：无`；
  出现 `不适用`／`无此项`／`无需披露` 一律发——那是把没查当成没有。

道五 DT-LINE 红线
  能否转回／税务风险／税负优化／税率变动方向／EPS 影响／评级与目标价一类断言零命中；
  **只判本件自己写的句子**：同一行「」里的引文先洗掉再判——引文是证据，不是本件的断言；
  含 [待人工] 的分句豁免，且只豁免它自己那一句（按 ；;。，,｜ 切分）；
  「未经抵销」与「抵销后净额」在同一分句被写成相等（＝／等于／即／视同）一律发——
  那四个数是披露给的四行账，写成相等就是把抵销这一层抹掉了。

退码：0 全过 / 1 有发条 / 2 用法错（缺参数） / 3 读不到文件或空稿。
"""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-deferred-tax-cn"

CODES = ("DT-STRUCT", "DT-QUOTE", "DT-NOSELF", "DT-GAP", "DT-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("递延所得税资产与负债明细", "未经抵销的递延所得税资产与负债",
            "未确认递延所得税资产的可抵扣亏损", "所得税费用与会计利润的调节表",
            "税率与主体口径", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"

HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")

SUBJECT = re.compile(r"^主体：\s*(\S.*)$")
PERIOD = re.compile(r"^报告期：\s*(\S.*)$")

TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
# 锚块是定位指针，不是本件在判断。只洗「〔锚：…〕」，不碰〔自算〕——
# 后者恰恰是本件自己算的标记，洗掉它就等于把自算伪装成披露值。
ANCHOR_BLOCK = re.compile(r"〔\s*锚\s*[:：][^〕]*〕")
ANCHOR_REF = re.compile(r"\[(S\d+)\]")

SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)"
    r"\|\s*(?P<url>https?://\S+)\s*\|"
    r"\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$"
)

PCT = re.compile(r"\d+(?:\.\d+)?\s*[%％]")

# 承重格的词族：写在本件句子里就必须在原句里也写得到
OFFSET_WORDS = ("互抵", "抵销", "轧差")
UNRECOG_WORDS = ("未确认递延所得税资产", "未予确认")
RATE_WORDS = ("税率",)

GAP_EXCUSE = ("不适用", "无此项", "无需披露")

EQUAL_WORDS = ("＝", "=", "等于", "即", "相同", "视同")
NEG_EQUAL = re.compile(r"(?:不|非)(?:等于|同于|一致|相同|视同|即)")
OFFSET_RAW = ("未经抵销",)
OFFSET_NET = ("抵销后净额", "互抵后净额", "抵销后")

HARD_BAN = ("能够转回", "可以转回", "可全额转回", "将全额转回", "预计转回",
            "税务风险低", "税务风险可控", "无税务风险", "不存在税务风险",
            "税负优化", "税负可控", "降低税负",
            "税率将下降", "税率将上升", "预计税率变动", "税率下调",
            "增厚 EPS", "增厚每股收益", "影响 EPS", "影响每股收益",
            "目标价", "目标市值", "买入评级", "增持评级", "中性评级",
            "建议买入", "建议增持", "强烈推荐", "跑赢大盘", "必涨", "必跌")

CLAUSE_SPLIT = re.compile(r"[；;。，,｜|]")

SCOPE_RULES = (
    (("四期差异点评", "科目勾稽点评"),
     "改走 cn-earnings-note：四期差异与科目勾稽的点评是那一件，本件只登记递延所得税这一张表"),
    (("税收优惠适用条件", "优惠目录", "税收政策适用"),
     "改走 tax-policy-card-cn：税收优惠政策本身能不能用、适用条件是那一件，本件只登记税率口径"),
    (("会计政策变更", "会计估计变更", "前期差错更正"),
     "改走 cn-accounting-error-correction-cn：政策变更与差错更正是那一件"),
    (("净利润预测", "盈利预测", "业绩预告"),
     "改走 cn-earnings-forecast-cn：预测是那一件，本件不评估未来盈利能否覆盖可抵扣亏损"),
)


def mark_first_run() -> None:
    """首次运行埋点：往 ~/.cue-usage/<slug>-<日期> 落一个空文件。

    平台两个下载计数器都不可信（新 listing 首 48h 一次性播种 50~60），
    本地这枚文件是本件唯一能证明「真有人装上并跑过」的证据。
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


def _norm_pct(tok):
    return tok.replace(" ", "").replace("％", "%")


def _clauses(line):
    return CLAUSE_SPLIT.split(line)


def _gap_key(line):
    """从一条「未取到」里取出被点名的那一项，两向对账用同一个取法。

    本件有两种合法写法，取法要对两种都成立：
      正文 `- 项名：未取到：原因`      → 项名在「未取到」**前**
      第六节 `- 未取到：项名`          → 项名在「未取到」**后**
    所以先看前面有没有项名（剥掉行首 `- `、去掉冒号），有就用它；没有才取冒号／标点之后那一段。
    旧写法一律取「未取到」后面那段，于是正文标准形会取到**原因**而不是项名，两向必然对不上——
    判出来的是假红，不是真缺。
    """
    head = re.sub(r"^-\s*", "", line.split("未取到", 1)[0]).strip().rstrip("：:，,。；; ")
    if head:
        return head[:12]
    rest = line.split("未取到", 1)[1].lstrip()
    m = re.match(r"^[：:]\s*(.+)$", rest)
    if m:
        rest = m.group(1)
    return re.split(r"[：:，,。；;｜]", rest.strip())[0].strip()[:12]


def _strip_quotes(text):
    """洗掉引文：引文是证据，红线只判本件自己写的句子。"""
    return QUOTE.sub("", text)


def _is_gap_line(s):
    """这条算不算「未取到」登记行。

    第六节的 `口径：…` 行里也会出现「未取到」三个字（「披露没写就写未取到」），
    若按「行内含未取到」收，口径行会被当成一条缺口点名，两向对账立刻多出假红。
    只认两种登记形：行首就是「未取到」，或 `项名：未取到…`（项名在前、冒号分隔）。
    """
    t = re.sub(r"^-\s*", "", s.strip())
    if t.startswith("未取到"):
        return True
    return bool(re.match(r"^[^：:]{1,12}[：:]\s*未取到", t))


# 互抵四数：项名指哪一号，原句就必须有那一号的写法。
# 「抵销」是「未经抵销」的子串，所以互抵金额不能只认「抵销」二字——
# 那样拿「未经抵销的资产/负债」两句当互抵额也过得去，恰恰是自行轧差最想蒙混的写法。
OFFSET_AMOUNT_QUOTE = ("相互抵销", "互抵", "抵销金额", "抵销的金额", "予以抵销", "抵销后")
OFFSET_NET_QUOTE = ("抵销后", "净额")
OFFSET_RAW_QUOTE = ("未经抵销",)
# 第二节必须四号齐全：少披露哪一个，就用它自己的「未取到」占一行，不许省掉。
OFFSET_FAMILIES = (("未经抵销的递延所得税资产",),
                   ("未经抵销的递延所得税负债",),
                   ("互抵金额", "抵销金额"),
                   ("抵销后净额", "抵销后列示"))


def _check_offset_pair(lineno, line, add):
    """互抵四数各占一行：项名是哪一号，原句就得给那一号。"""
    if "未取到" in line:
        return
    label, _body = _split_label(line)
    if not label:
        return
    q = _quotes(line)
    if "未经抵销" in label:
        if not any(w in q for w in OFFSET_RAW_QUOTE):
            add("DT-NOSELF", lineno,
                "「%s」的原句里没有「未经抵销」：四个数是披露给的四行账，不拿另一号的数顶上" % label[:16])
    elif "净额" in label or "抵销后" in label:
        if not any(w in q for w in OFFSET_NET_QUOTE):
            add("DT-NOSELF", lineno,
                "「%s」的原句里没有「抵销后／净额」写法：净额取自披露，不由本件做减法" % label[:16])
    elif "互抵" in label or "抵销金额" in label:
        if not any(w in q for w in OFFSET_AMOUNT_QUOTE):
            add("DT-NOSELF", lineno,
                "「%s」的原句里没有抵销额写法：互抵金额取自披露，不由本件轧差" % label[:16])


def _equal_hit(clause):
    """分句里有没有把「未经抵销」与「抵销后净额」写成相等的连接词（否定形不算）。"""
    c = NEG_EQUAL.sub("", clause)
    return [w for w in EQUAL_WORDS if w in c]


def _split_label(line):
    """把一条发现行拆成「项名」与「余下部分」。

    本件两种写法都要认：
      `- 项名：值「原句」…`   → 项名到第一个冒号
      `- 项名 值「原句」…`    → 项名到第一个空白
    取「冒号」与「空白」里更早出现的那个做界。项名是标签、不是断言，
    这一步只服务自推判据的判域；拆不开（行首就是值）时整行算正文，宁严不松。

    本件的项名天生带词族（「未经抵销的递延所得税资产」「互抵金额」「抵销后净额」
    「未确认的可抵扣亏损」），不剥就会把每一条正确写法都判成自推。
    """
    m = re.match(r"^-\s*(.+)$", line)
    if not m:
        return "", line
    rest = m.group(1)
    cut = len(rest)
    for tok in ("：", ":", " ", "\t"):
        i = rest.find(tok)
        if i != -1:
            cut = min(cut, i)
    label = rest[:cut].strip()
    body = rest[cut:].lstrip("：: \t")
    return label, body


def _section_of(heading):
    h = heading.strip()
    for _ in range(2):
        h2 = NUMBERING.sub("", h)
        if h2 == h:
            break
        h = h2
    h = h.strip()
    for name in SECTIONS:
        if h == name:
            return name
        if h.startswith(name) and not h[len(name):len(name) + 1].isalnum():
            return name
    return None


def split_doc(text):
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


def _check_line(lineno, line, add):
    # 先洗引文、再切分句：引文里的逗号会在切分处断成两截，
    # 逐句洗就洗不干净——「附注称该资产能够转回，税负可控」这类照抄原文会被误判成本件断言。
    own_line = _strip_quotes(line)
    for clause in _clauses(own_line):
        if "[待人工]" in clause:
            continue
        own = clause
        hit = [w for w in HARD_BAN if w in own]
        # 未经抵销 ＝ 抵销后净额：同句出现两类词又被写成相等，就是把抵销这一层抹掉
        if (any(w in own for w in OFFSET_RAW)
                and any(w in own for w in OFFSET_NET)
                and _equal_hit(own)):
            hit.append("未经抵销＝抵销后净额")
        if hit:
            add("DT-LINE", lineno, "红线词：%s（%s）" % ("、".join(sorted(set(hit))), clause.strip()[:40]))
            return


def _quotes(line):
    return "".join(m.group(1) for m in QUOTE.finditer(line))


def _check_vocab(lineno, line, add, words, what):
    """词族只认原句：本件句子里写了，同一行原句也必须写到。

    判域＝去掉**项名**与**锚标签**之后的余下部分。两处都是标签、不是断言：
    项名是「互抵金额」「未经抵销的递延所得税资产」这种登记对象，锚标签是
    「〔锚：…附注三·递延所得税〕」这种定位指针——把它们算进自推会冤枉正确写法。
    「未取到」行整行豁免——那正是「原句没写所以照实写未取到」的正确形态。
    """
    if _is_gap_line(line):
        return
    _label, body = _split_label(line)
    body = ANCHOR_BLOCK.sub("", body)       # 锚是定位指针，不是本件在判断
    q = _quotes(line)
    outside = [w for w in words if w in body and w not in q]
    if outside:
        add("DT-NOSELF", lineno,
            "%s须取原句：本件句子里写了「%s」，原句里没有——没披露就写未取到，不按惯例自推：%s"
            % (what, "、".join(outside), line.strip()[:40]))


def _check_mol_den(lineno, line, add, what):
    mol = re.search(r"分子[^｜|〕」；。]*\[S\d+\]", line)
    den = re.search(r"分母[^｜|〕】」；。]*\[S\d+\]", line)
    why = []
    if not mol:
        why.append("缺分子来源")
    if not den:
        why.append("缺分母来源")
    if why:
        add("DT-NOSELF", lineno, "%s自算未交代%s" % (what, "／".join(why)))


def _check_pct(lineno, line, add):
    """百分数：原句里没有同一数值，就必须自算并交代分子分母；谈税率的另加一条口径。"""
    if _is_gap_line(line):
        return                      # 未取到行里的数字是在标「没取到哪一项」，不是本件算的
    q = _quotes(line).replace(" ", "")
    label, body = _split_label(line)
    missing = [t for t in PCT.findall(line) if _norm_pct(t) not in q]
    if not missing:
        return
    # 判「这一行是不是在谈税率」时把项名算进来、把引文剔出去：
    # `- 法定税率：25%「…」` 的「税率」在项名上；而引文里恰好出现「税率」二字
    # 不该把一条谈别的数的行拉进税率判据。
    rate_line = any(w in (label + _strip_quotes(body)) for w in RATE_WORDS)
    if "〔自算〕" not in line:
        if rate_line:
            add("DT-NOSELF", lineno,
                "税率 %s 在原句里找不到：税率只认披露写法，不按 25% 默认值补——%s"
                % ("、".join(missing), line.strip()[:40]))
        else:
            add("DT-NOSELF", lineno, "比例 %s 在原句里找不到，也没标〔自算〕：%s"
                % ("、".join(missing), line.strip()[:40]))
        return
    if rate_line:
        add("DT-NOSELF", lineno,
            "税率 %s 标了〔自算〕也不放过：税率只认披露写法，不按默认值自算——%s"
            % ("、".join(missing), line.strip()[:40]))
        return
    _check_mol_den(lineno, line, add, "比例")


def _check_noself(lineno, line, add):
    # 词族：互抵与未确认只认原句
    _check_vocab(lineno, line, add, OFFSET_WORDS, "互抵与抵销判断")
    _check_vocab(lineno, line, add, UNRECOG_WORDS, "未确认递延所得税资产判断")
    # 互抵四数：项名是哪一号，原句就得给哪一号
    _check_offset_pair(lineno, line, add)
    # 百分数与税率
    _check_pct(lineno, line, add)


def check_text(text):
    findings = []
    stats = {"finding_lines": 0, "sources": 0, "ratio_lines": 0}

    def add(code, lineno, msg):
        findings.append((code, lineno, msg))

    header, sections, stray = split_doc(text)

    # ---- 道一 头部
    htext = "\n".join(s for _i, s in header)
    for mark in MARK_TEXTS:
        if mark not in htext:
            add("DT-STRUCT", 1, "头部缺自标「%s」" % mark)
    if not any(SUBJECT.match(s) for _i, s in header):
        add("DT-STRUCT", 1, "头部缺 `主体：` 行")
    if not any(PERIOD.match(s) for _i, s in header):
        add("DT-STRUCT", 1, "头部缺 `报告期：` 行")

    # ---- 道一 节齐与序
    names = [n for n, _l, _b in sections]
    for name in SECTIONS:
        if name not in names:
            add("DT-STRUCT", 1, "缺节「%s」" % name)
    pos = [SECTIONS.index(n) for n in names]
    if pos != sorted(pos):
        add("DT-STRUCT", 1, "节序不对：现序 %s，应序 %s" % ("／".join(names), "／".join(SECTIONS)))
    for lineno, raw in stray:
        add("DT-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw)

    referenced = []
    body_gaps = []      # 正文点名未取到的条目
    section_found = {}

    for name, hline, body in sections:
        if name in CONTENT_SECTIONS:
            n_find = 0
            for lineno, s in body:
                if not s.strip() or s.lstrip().startswith("###"):
                    continue
                if not _is_finding_line(s):
                    add("DT-STRUCT", lineno, "节内只许 `- ` 发现行：%s" % s.strip()[:40])
                    continue
                n_find += 1
                stats["finding_lines"] += 1
                referenced.extend(ANCHOR_REF.findall(s))
                if _is_gap_line(s):
                    body_gaps.append((lineno, s))
                if not TRIPLE.search(s):
                    if "未取到" in s or "[待人工]" in s or "〔自算〕" in s:
                        pass
                    else:
                        add("DT-QUOTE", lineno, "发现行缺「」原句 + 〔锚：…〕 + [S#] 三元组：%s"
                            % s.strip()[:40])
                else:
                    for m in TRIPLE.finditer(s):
                        if not m.group("q").strip():
                            add("DT-QUOTE", lineno, "原句为空")
                        if not m.group("a").strip():
                            add("DT-QUOTE", lineno, "锚为空")
                    if not re.search(r"\[S\d+\]\s*$", s.strip()):
                        add("DT-QUOTE", lineno, "发现行未以 [S#] 收尾（三元组须在行末）")
                _check_line(lineno, s, add)
                if PCT.findall(s):
                    stats["ratio_lines"] += 1
                _check_noself(lineno, s, add)
            section_found[name] = n_find
            if n_find == 0:
                add("DT-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name)

        elif name == GAP_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not _is_finding_line(s):
                    add("DT-STRUCT", lineno, "第六节只许 `- ` 行：%s" % s.strip()[:40])
                    continue
                section_found.setdefault(name, 0)
                section_found[name] += 1
                for w in GAP_EXCUSE:
                    if w in s:
                        add("DT-GAP", lineno, "禁用「%s」把没查当成没有：%s" % (w, s.strip()[:40]))
                _check_line(lineno, s, add)

        elif name == SOURCE_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not s.lstrip().startswith("- ["):
                    add("DT-STRUCT", lineno, "来源节只许 `- [S#] …` 行：%s" % s.strip()[:40])
                    continue
                m = SOURCE_LINE.match(s.strip())
                if not m:
                    add("DT-QUOTE", lineno, "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:50])
                    continue
                stats["sources"] += 1

    # ---- 道四 未取到两向点名
    gap_body = [s for _ln, s in body_gaps]

    # ---- 道一 互抵四数各占一行：少披露哪一个，就用它自己的「未取到」占一行
    sec2 = []
    for name, _h, body in sections:
        if name == SECTIONS[1]:
            sec2 = [s for _ln, s in body if _is_finding_line(s)]
    if sec2:
        for fam in OFFSET_FAMILIES:
            if not any(any(w in s for w in fam) for s in sec2):
                add("DT-STRUCT", 1,
                    "第二节缺「%s」这一行：四个数各占一行，没披露就写它的未取到" % fam[0])
    gap_sec = []
    for name, _h, body in sections:
        if name != GAP_SECTION:
            continue
        for _ln, s in body:
            if _is_gap_line(s) and "未取到：无" not in s and "未取到:无" not in s:
                gap_sec.append(s)
    for s in gap_body:
        if "未取到：无" in s:
            continue
        key = _gap_key(s)
        if key and not any(key in g for g in gap_sec):
            add("DT-GAP", 1, "正文写了未取到「%s」，第六节没点名" % key)
    for g in gap_sec:
        key = _gap_key(g)
        if key and not any(key in s for s in gap_body):
            add("DT-GAP", 1, "第六节点名了「%s」，正文没有这条表述" % key)

    # 零缺口须显式写「未取到：无」
    if not gap_body and not gap_sec:
        gap_text = "\n".join(s for name, _h, body in sections if name == GAP_SECTION
                             for _ln, s in body)
        if "未取到：无" not in gap_text and "未取到:无" not in gap_text:
            add("DT-GAP", 1, "零缺口未显式写「未取到：无」")

    # ---- 道二 引用与登记
    defined = set()
    for name, _h, body in sections:
        if name != SOURCE_SECTION:
            continue
        for _ln, s in body:
            m = SOURCE_LINE.match(s.strip())
            if m:
                defined.add(m.group("s"))
    for ref in sorted(set(referenced)):
        if ref not in defined:
            add("DT-QUOTE", 1, "正文引用 [%s]，来源节没有对应登记行" % ref)

    # ---- 边界
    # 只判前五节（登记正文）。第六节「口径与未取到」正是写明与另几枚件分界的地方，
    # 在那里点名 cn-earnings-note／tax-policy-card-cn 是本件要求的动作，不是越界。
    body_lines = [(ln, s) for name, _h, body in sections
                  if name in CONTENT_SECTIONS for ln, s in body]
    for words, tip in SCOPE_RULES:
        for ln, s in body_lines:
            if any(w in s for w in words):
                add("DT-STRUCT", ln, "越界：%s" % tip)
                break

    findings.sort(key=lambda x: (x[1], CODES.index(x[0])))
    return findings, stats


def report(path, findings, stats):
    print("稿：%s" % path)
    print("统计：发现行 %d ｜ 来源 %d ｜ 涉比率行 %d"
          % (stats["finding_lines"], stats["sources"], stats["ratio_lines"]))
    if not findings:
        print("结论：五道全过（零发条）")
        return
    print("结论：发条 %d" % len(findings))
    for code, lineno, msg in findings:
        print("  %s L%-4d %s" % (code, lineno, msg))
    hit = sorted(set(c for c, _l, _m in findings))
    print("发条码：%s" % "、".join(hit))


GOOD = r"""# 示例材料（600000.SH）递延所得税登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议 ｜ 判断位 [待人工]
主体：示例材料（600000.SH）
报告期：2025 年年度报告

## 递延所得税资产与负债明细

- 资产减值准备：期初 120.00 万元「资产减值准备形成可抵扣暂时性差异，期初递延所得税资产 1,200,000.00 元」〔锚：2025 年年报·第 140 页·附注三·递延所得税〕[S1]
- 资产减值准备本期增减：计入损益 30.00 万元「本期计入当期损益的递延所得税资产增加 300,000.00 元」〔锚：2025 年年报·第 140 页·附注三·递延所得税〕[S1]
- 资产减值准备期末：150.00 万元「期末递延所得税资产余额 1,500,000.00 元」〔锚：2025 年年报·第 140 页·附注三·递延所得税〕[S1]
- 可抵扣亏损：期末 200.00 万元「可抵扣亏损形成递延所得税资产 2,000,000.00 元」〔锚：2025 年年报·第 140 页·附注三·递延所得税〕[S1]
- 公允价值变动：计入其他综合收益 40.00 万元「计入其他综合收益的递延所得税负债 400,000.00 元」〔锚：2025 年年报·第 141 页·附注三·递延所得税〕[S1]
- 职工薪酬：未取到：附注未单列职工薪酬形成的递延所得税

## 未经抵销的递延所得税资产与负债

- 未经抵销的递延所得税资产：1,900.00 万元「未经抵销的递延所得税资产 19,000,000.00 元」〔锚：2025 年年报·第 141 页·附注三·递延所得税〕[S1]
- 未经抵销的递延所得税负债：300.00 万元「未经抵销的递延所得税负债 3,000,000.00 元」〔锚：2025 年年报·第 141 页·附注三·递延所得税〕[S1]
- 互抵金额：200.00 万元「上述递延所得税资产与负债以 2,000,000.00 元为限相互抵销」〔锚：2025 年年报·第 141 页·附注三·递延所得税〕[S1]
- 抵销后净额·资产：1,700.00 万元「抵销后列示的递延所得税资产净额 17,000,000.00 元」〔锚：2025 年年报·第 141 页·附注三·递延所得税〕[S1]
- 抵销后净额·负债：100.00 万元「抵销后列示的递延所得税负债净额 1,000,000.00 元」〔锚：2025 年年报·第 141 页·附注三·递延所得税〕[S1]

## 未确认递延所得税资产的可抵扣亏损

- 未确认的可抵扣亏损：800.00 万元「未确认递延所得税资产的可抵扣亏损 8,000,000.00 元」〔锚：2025 年年报·第 142 页·附注三·递延所得税〕[S1]
- 可抵扣亏损到期年份：2029 年至 2031 年「上述可抵扣亏损将于 2029 年至 2031 年陆续到期」〔锚：2025 年年报·第 142 页·附注三·递延所得税〕[S1]
- 未确认理由：存在不确定性「本公司预计未来期间可能无法取得足够的应纳税所得额」〔锚：2025 年年报·第 142 页·附注三·递延所得税〕[S1]
- 未确认亏损占比：40.00%〔自算〕分子＝未确认的可抵扣亏损 8,000,000.00 元 [S1]｜分母＝可抵扣亏损总额 20,000,000.00 元 [S1]
- 未确认暂时性差异：未取到：附注未列示未确认的可抵扣暂时性差异

## 所得税费用与会计利润的调节表

- 按法定税率计算的所得税费用：2,500.00 万元「按法定税率 25% 计算的所得税费用 25,000,000.00 元」〔锚：2025 年年报·第 143 页·附注三·所得税费用〕[S1]
- 不可抵扣费用影响：120.00 万元「不可抵扣费用的所得税影响 1,200,000.00 元」〔锚：2025 年年报·第 143 页·附注三·所得税费用〕[S1]
- 免税收入影响：80.00 万元「免税收入的所得税影响减少 800,000.00 元」〔锚：2025 年年报·第 143 页·附注三·所得税费用〕[S1]
- 未确认亏损影响：160.00 万元「本期未确认可抵扣亏损的所得税影响 1,600,000.00 元」〔锚：2025 年年报·第 143 页·附注三·所得税费用〕[S1]
- 实际所得税费用：2,700.00 万元「本期所得税费用 27,000,000.00 元」〔锚：2025 年年报·第 143 页·附注三·所得税费用〕[S1]
- 调节表差异项：未取到：附注未单列税率变动的影响

## 税率与主体口径

- 法定税率：25%「本公司适用的企业所得税法定税率为 25%」〔锚：2025 年年报·第 144 页·附注三·所得税费用〕[S1]
- 优惠税率：15%「子公司享受高新技术企业优惠税率 15%」〔锚：2025 年年报·第 144 页·附注三·所得税费用〕[S2]
- 多主体合并口径：按各主体适用税率分别计算「合并报表按各纳税主体适用税率分别计算后合并」〔锚：2025 年年报·第 144 页·附注三·所得税费用〕[S1]
- 税率变动影响：未取到：附注未披露税率变动对递延所得税的影响

## 口径与未取到

- 未取到：职工薪酬
- 未取到：未确认暂时性差异
- 未取到：调节表差异项
- 未取到：税率变动影响
- 口径：递延所得税资产与负债逐项照抄期初、本期增减、期末，未列的项目不补。
- 口径：未经抵销的资产、未经抵销的负债、互抵金额、抵销后净额是四个独立数，各占一行；抵销额取自披露，不由本件做减法。
- 口径：税率只认披露写法，披露没写就写未取到，不按 25% 默认值补。
- 口径：四期差异与科目勾稽的点评见 cn-earnings-note，本件只登记递延所得税这一张表。
- 口径：税收优惠的适用条件见 tax-policy-card-cn；政策变更与差错更正见 cn-accounting-error-correction-cn。

## 来源

- [S1] 示例材料 2025 年年度报告·附注三·递延所得税与所得税费用 | https://example.com/ann/S1 | 检索日 2026-11-13 | 类型：公告
- [S2] 示例材料 2025 年年度报告·附注三·税收优惠 | https://example.com/ann/S2 | 检索日 2026-11-13 | 类型：公告
"""

# ---- 坏样：各只发自己那道码
# 形制坏样插的是**多出一节同名标题**，不是改节标题名：改名会让整节变 stray、节内发现行一并丢，
# 连带节内那条「未取到」也没了，第六节就多出一条假 DT-GAP——测出来的红分不清是哪道判的。
BAD_STRUCT = GOOD.replace(
    "## 未经抵销的递延所得税资产与负债",
    "## 递延所得税资产与负债明细\n\n## 未经抵销的递延所得税资产与负债")

BAD_QUOTE = GOOD.replace(
    "「期末递延所得税资产余额 1,500,000.00 元」〔锚：2025 年年报·第 140 页·附注三·递延所得税〕[S1]",
    "1,500,000.00 元 [S1]")

BAD_NOSELF = GOOD.replace(
    "｜分母＝可抵扣亏损总额 20,000,000.00 元 [S1]",
    "")

BAD_GAP = GOOD.replace(
    "- 未取到：调节表差异项",
    "- 未取到：不适用")

BAD_LINE = GOOD.replace(
    "- 实际所得税费用：",
    "- 递延所得税资产能够转回，税务风险可控；实际所得税费用：")

# ---- 反证样：不该发的必须不发
OK_HUMAN = GOOD.replace(
    "- 口径：税率只认披露写法，披露没写就写未取到，不按 25% 默认值补。",
    "- 递延所得税资产能否转回 [待人工]，税务风险高低 [待人工]，对 EPS 的影响 [待人工]\n"
    "- 口径：税率只认披露写法，披露没写就写未取到，不按 25% 默认值补。")

BAD_HUMAN_HALF = GOOD.replace(
    "- 口径：税率只认披露写法，披露没写就写未取到，不按 25% 默认值补。",
    "- 递延所得税资产能否转回 [待人工]，税务风险可控\n"
    "- 口径：税率只认披露写法，披露没写就写未取到，不按 25% 默认值补。")

# 引文反证样换的是「多主体合并口径」那一行的引文，不动任何「未取到」行——
# 动未取到行会同时删掉正文点名，第六节立刻多一条假 DT-GAP，测出来的红就不是红线那道了。
OK_QUOTED_REDLINE = GOOD.replace(
    "「合并报表按各纳税主体适用税率分别计算后合并」",
    "「公司称该递延所得税资产能够转回，税务风险可控」")

BAD_OFFSET_MIX = GOOD.replace(
    "- 口径：未经抵销的资产、未经抵销的负债、互抵金额、抵销后净额是四个独立数，各占一行；抵销额取自披露，不由本件做减法。",
    "- 口径：抵销后净额即未经抵销的递延所得税资产，两者相等。")

# 项名里带词族不算自推：项名是在标登记对象，不是在替披露判断。
# 本件项名天生带「互抵」「未经抵销」「未确认」这些词，剥项名要认冒号式与空格式两种。
OK_ITEMNAME = GOOD.replace(
    "- 互抵金额：200.00 万元「上述递延所得税资产与负债以 2,000,000.00 元为限相互抵销」〔锚：2025 年年报·第 141 页·附注三·递延所得税〕[S1]",
    "- 互抵·抵销金额 200.00 万元「上述递延所得税资产与负债以 2,000,000.00 元为限相互抵销」〔锚：2025 年年报·第 141 页·附注三·递延所得税〕[S1]")

# 反证：原句给了税率就照抄，不误伤
OK_RATE_QUOTED = GOOD.replace(
    "- 法定税率：25%「本公司适用的企业所得税法定税率为 25%」",
    "- 法定税率：25%「本公司适用的企业所得税法定税率为 25%」")

# 反证：未取到行里的百分比是在标「没取到哪一项」，整行豁免比值判定
OK_GAP_PCT = GOOD.replace(
    "- 未确认暂时性差异：未取到：附注未列示未确认的可抵扣暂时性差异",
    "- 未确认暂时性差异：未取到：附注未按 25% 分解列示未确认的可抵扣暂时性差异")

# 专项反证：正文写「按 25%」而原句没有 25%，即便标〔自算〕也照样红（税率不落默认值）
BAD_RATE_DEFAULT = GOOD.replace(
    "- 法定税率：25%「本公司适用的企业所得税法定税率为 25%」〔锚：2025 年年报·第 144 页·附注三·所得税费用〕[S1]",
    "- 法定税率：按 25% 计算〔自算〕「本公司适用的企业所得税税率见附注三」〔锚：2025 年年报·第 144 页·附注三·所得税费用〕[S1]｜分子＝1 [S1]｜分母＝1 [S1]")

# 自推：原句没写抵销，本件自称互抵金额
BAD_OFFSET_GUESS = GOOD.replace(
    "- 互抵金额：200.00 万元「上述递延所得税资产与负债以 2,000,000.00 元为限相互抵销」〔锚：2025 年年报·第 141 页·附注三·递延所得税〕[S1]",
    "- 互抵金额：200.00 万元「未经抵销的递延所得税资产 19,000,000.00 元，未经抵销的递延所得税负债 3,000,000.00 元」〔锚：2025 年年报·第 141 页·附注三·递延所得税〕[S1]")

# 零输入样例：直接由 GOOD 派生，不另抄一份——两份会各自漂移，
# 而用户看到的「成品长什么样」必须永远等于自测里那个「好样」。
DEMO = GOOD


# 互抵四数少一行：不是省一句，是把「没披露」和「披露了」混成一句
BAD_OFFSET_MISSING = GOOD.replace(
    "- 互抵金额：200.00 万元「上述递延所得税资产与负债以 2,000,000.00 元为限相互抵销」"
    "〔锚：2025 年年报·第 141 页·附注三·递延所得税〕[S1]\n", "")

# 拿「未经抵销」那句顶「抵销后净额」：净额是做减法的产物，披露没给就只能写未取到
BAD_NET_GUESS = GOOD.replace(
    "- 抵销后净额·资产：1,700.00 万元「抵销后列示的递延所得税资产净额 17,000,000.00 元」",
    "- 抵销后净额·资产：1,700.00 万元「未经抵销的递延所得税资产 19,000,000.00 元」")


def _codes(text):
    findings, _stats = check_text(text)
    return findings, set(c for c, _l, _m in findings)


def selftest():
    cases = (
        ("好样应零发条", GOOD, set()),
        ("形制：多出一节同名节（递延所得税资产与负债明细）", BAD_STRUCT, {"DT-STRUCT"}),
        ("锚：数字行没挂原句与锚", BAD_QUOTE, {"DT-QUOTE"}),
        ("自算：未确认亏损占比自算只给分子没给分母", BAD_NOSELF, {"DT-NOSELF"}),
        ("点名：第六节用「不适用」搪塞", BAD_GAP, {"DT-GAP"}),
        ("红线：写能够转回、税务风险可控", BAD_LINE, {"DT-LINE"}),
        ("反证：[待人工] 整句成立 → 不发", OK_HUMAN, set()),
        ("反证：[待人工] 只豁免自己那句，后半句照样发", BAD_HUMAN_HALF, {"DT-LINE"}),
        ("反证：引文里的「能够转回」不是本件断言 → 不发", OK_QUOTED_REDLINE, set()),
        ("红线：抵销后净额即未经抵销金额", BAD_OFFSET_MIX, {"DT-LINE"}),
        ("反证：项名里带「互抵·抵销」不算自推 → 不发", OK_ITEMNAME, set()),
        ("反证：原句给了税率就照抄 → 不发", OK_RATE_QUOTED, set()),
        ("反证：未取到行里的百分比整行豁免 → 不发", OK_GAP_PCT, set()),
        ("自算：正文写「按 25%」而原句没有，税率不许落默认值", BAD_RATE_DEFAULT, {"DT-NOSELF"}),
        ("自推：原句没写抵销却自标互抵金额", BAD_OFFSET_GUESS, {"DT-NOSELF"}),
        ("形制：第二节少了「互抵金额」这一行", BAD_OFFSET_MISSING, {"DT-STRUCT"}),
        ("自推：拿「未经抵销」那句顶「抵销后净额」", BAD_NET_GUESS, {"DT-NOSELF"}),
    )
    bad = 0
    for label, text, want in cases:
        findings, got = _codes(text)
        if got == want:
            print("过   %s（发条 %d 条：%s）" % (label, len(findings),
                                                "、".join(sorted(got)) or "无"))
        else:
            bad += 1
            detail = "；".join("%s L%d %s" % (c, l, m) for c, l, m in findings[:4])
            print("不合 %s：期望 %s 实得 %s ｜ %s"
                  % (label, sorted(want) or "无", sorted(got) or "无", detail))
    print("——")
    print("自测档数=%d｜不合=%d｜不可判=0" % (len(cases), bad))
    return 0 if bad == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="递延所得税稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="递延所得税稿 .md 路径")
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
        print("缺入参：给一份递延所得税稿路径，或用 --demo / --selftest", file=sys.stderr)
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

    findings, stats = check_text(text)
    report(args.path, findings, stats)
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
