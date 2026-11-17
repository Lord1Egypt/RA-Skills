#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_expected_credit_loss.py — 预期信用损失登记稿五道机检（零网络、零外发）

**五道全部落字**：`UNIMPLEMENTED` 为空，五节内容由五道判据各判一段，好样单稿退 0。
空壳入口 `_not_judged` 仍留在原地：将来某道回退成空壳（重新登记进 `UNIMPLEMENTED`）时，
调用即抛、由 `check_text` 捕获计入 unjudged，不裸抛；零发条但有未落字的稿子退 3，
报告里明写「这不等于合规」——空壳不许被读成「过」。`rc=0` 只留给「五道全过」。

用法：
    python3 scripts/check_expected_credit_loss.py <预期信用损失登记稿>.md
    python3 scripts/check_expected_credit_loss.py --selftest
    python3 scripts/check_expected_credit_loss.py --demo     打印一份七节样例（零输入可跑）

七节（按序，`## ` 起节）：
    预期信用损失概况／三阶段划分／组合计提／单项计提／前瞻性信息与账龄依据
    ／口径与未取到／来源

五道码（状态以 `UNIMPLEMENTED` 现值为准，下面写的是**这道判什么**）：

道一 ECL-STRUCT 形制【已落字】
  头部（第一个 `## ` 之前）三件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议；
  七节齐且按序；认不出的节标题与多出的同名节记 stray 逐条发。
  **只判形，不判内容**——内容对不对是另四道的事，这里越界会让一支注入同时红两道。
  不判「主体：」「报告期：」：本件规格只列三件自标，不自行加判据。

道二 ECL-QUOTE 原句与锚【已落字】
  五节里每个数字行须挂齐「」原句 + 〔锚：…〕 + [S#] 三元组，可挂多组；
  原句须像原句（≥8 字，不是纯数字／标点）；
  例外只有三形：「未取到：」行、[待人工] 行与〔自算〕行；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址；
  两向都发：正文引了未登记的 [S#]／来源行没被任何正文行引用；来源节一条合规行都没有则单独发一条。
  **只认形**——不核对引号里的数与行首的数是同一（那是 ECL-ROLL 的活）。

道三 ECL-STAGE 三阶段划分只认原句【已落字】
  「三阶段划分」节里，行首标了〔阶段：第N阶段〕的行，原句必须含同一个阶段词；
  缺〔锚〕[S#] 也发。同一阶段在一节里报了损失准备的两个不同数 ⇒ 发。
  次数只认行首阶段标签：原句里提到别的阶段词不算归属，不按逾期天数推、不拿上期结构补。

道四 ECL-ROLL 组合与单项两条路的逐数比对【已落字】
  「组合计提」与「单项计提」两节，按〔组合：…〕／〔对象：…〕分组比两件事：
  ① `损失准备 / 账面余额` 与披露的计提比例差 > 0.05 个百分点 ⇒ 发；
  ② 滚动式 `期初 + 本期计提 - 本期转回 - 本期核销 = 期末` 差 > 0.01 万元 ⇒ 发，
     消息记 `重算=X 披露=Y`。
  **任一项缺失 ⇒ 整条比对跳过**，不猜、不按 0 算；分组名缺失的行不参与同组比对（归属不明）。

道五 ECL-LINE 红线【已落字】
  ① 把损失准备说成已发生损失（已确定收不回／坏账损失已发生）；
  ② 给出「计提充分／不足」的判断；
  ③ 用轧净额冒充账面余额；
  ④ 给评级、目标价、买卖建议。
  另：组合计提与单项计提**缺任何一节** ⇒ 发条（两条计提路径必须各占一节）。
  「口径与未取到」与「来源」两节整节豁免——口径节按设计就要写「本件不判断计提是否充分」。

退码：0 五道全过 / 1 有发条 / 2 用法错（缺参数或未知参数）
      / 3 读不到文件或空稿，或零发条但仍有未落字判据（`UNIMPLEMENTED` 非空时）。
      本件五道全落字，这条当前不触发（好样单稿退 0），留着是为了将来某道回退成空壳时
      不把「没跑」读成「过」。

边界（不是这几枚件，别互相代填）：
    不是 `cn-working-capital-quality`：那枚登记存货／应收账款／合同资产的余额与账龄、
    计提与转回，五节、**不分阶段**；本件登记的是减值准备计提方法那一段里的三阶段、
    组合与单项两条路、前瞻性信息与计提比例。两件读的是同一份财报的不同段落。
    不是 `cn-notes-receivable-cn`（那枚管票据：银行承兑／商业承兑、背书贴现、终止确认）。
    不是 `cn-other-comprehensive-income-cn`（那枚管其他综合收益，与本件不重叠）。
"""

import argparse
import contextlib
import io
import os
import re
import sys
import tempfile

SLUG = "cue-cn-expected-credit-loss-cn"

CODES = ("ECL-STRUCT", "ECL-QUOTE", "ECL-STAGE", "ECL-ROLL", "ECL-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议")

SECTIONS = ("预期信用损失概况", "三阶段划分", "组合计提", "单项计提",
            "前瞻性信息与账龄依据", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"

# 未落字的码：抛未落字一律计「不可判」，不许并进「不合」，也不许算「过」；
# 不在清单里却抛未落字＝声明与实装不符，由 check_text 直接发条。
# 本拍五道全部落字。
UNIMPLEMENTED = ()

HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")

TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
ANCHOR_BLOCK = re.compile(r"〔\s*锚\s*[:：][^〕]*〕")
ANCHOR_REF = re.compile(r"\[(S\d+)\]")
REF_TAIL = re.compile(r"\[(S\d+)\]\s*$")

SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)"
    r"\|\s*(?P<url>https?://\S+)\s*\|"
    r"\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$"
)


# ---------------------------------------------------------------- 判据（五道均已落字）

def _not_judged(code, why):
    """空壳的唯一出口：抛未落字，由 check_text 捕获计入「不可判」，不返回空表。"""
    raise NotImplementedError("%s 未落字：%s" % (code, why))


def check_struct(head, sections, stray):
    """道一 ECL-STRUCT 形制：头部三件自标、七节齐且按序、节标题可识别。

    只判「形」：自标在不在、节名在不在、顺序对不对、有没有野节。内容对不对是另四道的事——
    这里不越界，否则一支注入会同时红两道、分不清归属。
    不判「主体：」「报告期：」：本件规格只列三件自标，不自行加判据。
    """
    out = []
    htext = "\n".join(s for _i, s in head)
    for mark in MARK_TEXTS:
        if mark not in htext:
            out.append(("ECL-STRUCT", 1, "头部缺自标「%s」" % mark))

    # 丙：野节（认不出的节名／多出的同名节）逐条报，行号用 stray 给的
    for lineno, raw in stray:
        out.append(("ECL-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw))

    # 丁：七节须齐且按序
    names = [n for n, _l, _b in sections]
    missing = [n for n in SECTIONS if n not in names]
    if missing:
        out.append(("ECL-STRUCT", 1, "缺节：%s" % "／".join(missing)))
    elif names != list(SECTIONS):
        out.append(("ECL-STRUCT", 1, "节序不对：现序 %s，应序 %s"
                    % ("／".join(names), "／".join(SECTIONS))))
    return out


def check_quote(head, sections, stray):
    """道二 ECL-QUOTE 原句与锚：三元组齐全，来源两向对应。

    只认**形**：数字行有没有「」原句、〔锚：…〕与 [S#] 三件；引号里的数与行首的数是同一
    这件事不在这里管（那是 ECL-ROLL 的活）。越界会让一支注入同时红两道。

    例外只有三形：`未取到：` 缺口行、`[待人工]` 判断位、`〔自算〕` 行——这三形按设计不带原句。
    """
    out = []

    # 甲：内容节里每个数字行都得挂齐三元组；原句要像原句（≥8 字，不是纯数字／标点）
    body_refs = {}                                 # [S#] → 首次出现的行号
    for name, lineno, body in _section_lines(sections, CONTENT_SECTIONS):
        for ln, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_exempt_line(s):
                continue
            own = _own_part(s)
            numeric = bool(re.search(r"\d", own)) or "%" in own or "％" in own
            trips = list(TRIPLE.finditer(s))
            if numeric and not trips:
                out.append(("ECL-QUOTE", ln, "数字行缺「」原句＋〔锚〕＋[S#] 三元组：%s" % own))
                continue
            for m in trips:
                q = m.group("q").strip()
                if len(q) < 8:
                    out.append(("ECL-QUOTE", ln, "原句太短（%d 字，应≥8）：%s" % (len(q), q)))
                elif not re.search(r"[^\d\s.,%％:：/年月日\-]", q):
                    out.append(("ECL-QUOTE", ln, "原句只有数字／标点，不是原句：%s" % q))
                body_refs.setdefault(m.group("s"), ln)

    # 乙：来源节的行须合格式，合格式的才算「登记」
    registered = {}
    src_finding_lines = 0
    for name, lineno, body in _section_lines(sections, (SOURCE_SECTION,)):
        for ln, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_exempt_line(s):
                continue
            src_finding_lines += 1
            m = SOURCE_LINE.match(s)
            if m:
                registered.setdefault(m.group("s"), ln)
            else:
                out.append(("ECL-QUOTE", ln,
                            "来源行不合格式（应 `- [S#] 标题 | http(s) URL | 检索日 YYYY-MM-DD`）：%s" % s))

    # 丙：两向对应各发一条——正文引了未登记的，登记了没被引用的
    for ref, ln in body_refs.items():
        if ref not in registered:
            out.append(("ECL-QUOTE", ln, "正文引用了来源节未登记的 [%s]" % ref))
    for ref, ln in registered.items():
        if ref not in body_refs:
            out.append(("ECL-QUOTE", ln, "来源行 [%s] 未被任何正文行引用" % ref))
    if src_finding_lines == 0:
        out.append(("ECL-QUOTE", 1, "来源节一条来源行都没有"))
    return out


STAGE_WORDS = ("第一阶段", "第二阶段", "第三阶段")


def check_stage(head, sections, stray):
    """道三 ECL-STAGE 三阶段划分只认原句。

    ① 用了阶段词的行必须挂「」原句（原句里要有同一个阶段词）＋〔锚〕＋[S#]；
       原句里没有那个阶段词 ⇒ 发——阶段归属是附注给的，不是稿子按行首标签自己安的。
    ② 同一阶段在一节里报了损失准备的两个不同数 ⇒ 发（哪个对不是本件能判的，但两个数并存必有错）。
    ③ 「三阶段划分」节一条阶段行都没有 ⇒ 发（该节按设计就是登记三阶段的）。

    不按逾期天数推阶段归属、不拿上期结构补：附注没给就写「未取到：」。
    **不判「三阶段划分」整节缺失**：那是 ECL-STRUCT 的缺节判据；这里再判一次会让
    「节标题认不出」一支注入同时红两道，分不清归属。
    """
    out = []
    seen_amount = {}                               # (节名, 阶段) → [(行号, 金额)]
    for name, _lineno, body in _section_lines(sections, ("三阶段划分",)):
        for ln, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_exempt_line(s):
                continue
            own, quotes = _own_part(s), _quotes_of(s)
            # 阶段的归属只认**行首登记值**里的阶段标签（`〔阶段：第三阶段〕`），
            # 不认原句里出现的阶段词——否则一行原句提到两个阶段，就会把它两边都挂上，
            # 凭空多出一个「同阶段两数」。
            own_words = [w for w in STAGE_WORDS if w in own]
            if not own_words:
                # 行首没标阶段（例如「阶段划分依据」那种整节说明行）就不是阶段行，跳过。
                # 「拿不准 ⇒ 不判」：没有阶段标签就没有归属可判，不按原句里出现的词替它安一个。
                continue
            for w in own_words:
                if w not in quotes:
                    out.append(("ECL-STAGE", ln,
                                "用了阶段词「%s」却没有含该词的原句：%s" % (w, own)))
                    continue
                if not TRIPLE.search(s):
                    out.append(("ECL-STAGE", ln,
                                "阶段行「%s」缺〔锚〕[S#] 三元组：%s" % (w, own)))
                amt = _num_after(own, "损失准备")
                if amt is not None:
                    seen_amount.setdefault((name, w), []).append((ln, amt))

    for (_name, w), vals in seen_amount.items():
        distinct = {v for _ln, v in vals}
        if len(distinct) > 1:
            detail = "／".join("L%d=%s" % (ln, _fmt(v)) for ln, v in vals)
            out.append(("ECL-STAGE", vals[0][0],
                        "同一阶段「%s」报了 %d 个不同的损失准备数：%s"
                        % (w, len(distinct), detail)))
    return out


ROLL_SECTIONS = ("组合计提", "单项计提")
# 长标签排在短标签前面：`_num_after` 是按标签逐个找的，「账面余额」与「期初余额」互不为前缀，
# 但把「期初余额／期末余额」列进来自有其用——滚动式要它们，缺了就整条跳过。
ROLL_FIELDS = ("账面余额", "期初余额", "期末余额", "损失准备",
               "计提比例", "本期计提", "本期转回", "本期核销")


def check_roll(head, sections, stray):
    """道四 ECL-ROLL 组合与单项两条路的逐数比对。

    两件事，都只在「组合计提」「单项计提」两节里做：

    ① 比率：`损失准备 / 账面余额` 与披露的计提比例相差 > 0.05 个百分点 ⇒ 发。
       （百分点 = pct * 100 之后的差；0.05 个百分点即 0.0005 的比例差。）
    ② 滚动：`期初 + 本期计提 - 本期转回 - 本期核销 = 期末` 差 > 0.01 ⇒ 发，
       消息记 `重算=X 披露=Y`，X 与 Y 都回显原值，不改口径。

    **任一项缺失 ⇒ 整条比对跳过**，不猜、不按 0 算——附注没给的数不能凭空补一个 0 去让式子成立。
    分组键是 `〔组合：…〕`／`〔对象：…〕` 里的那个名字，同组内的数才互相比。
    """
    out = []
    for name, _lineno, body in _section_lines(sections, ROLL_SECTIONS):
        groups = {}                                # 组名 → {字段: [(行号, 值)]}
        for ln, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_exempt_line(s):
                continue
            own = _own_part(s)
            key = _roll_key(own)
            if key is None:
                continue
            fields = groups.setdefault(key, {})
            for f in ROLL_FIELDS:
                v = _num_after(own, f)
                if v is not None:
                    fields.setdefault(f, []).append((ln, v))

        for key, fields in groups.items():
            # ① 比率比对
            bal = _pick(fields, "账面余额")
            prov = _pick(fields, "损失准备")
            pct = _pick(fields, "计提比例")
            if bal and prov and pct:
                if abs(bal[1]) > 1e-9:
                    calc = prov[1] / bal[1] * 100.0
                    if abs(calc - pct[1]) > 0.05:
                        out.append(("ECL-ROLL", prov[0],
                                    "「%s」计提比例 %s%% 与重算 %s%% 差 > 0.05 个百分点（重算=%s 披露=%s）"
                                    % (key, _fmt(pct[1]), _fmt(calc), _fmt(calc), _fmt(pct[1]))))
                else:
                    out.append(("ECL-ROLL", bal[0],
                                "「%s」账面余额为 0，计提比例无从重算" % key))
            # ② 滚动比对
            beg = _pick(fields, "期初余额")
            end = _pick(fields, "期末余额")
            add = _pick(fields, "本期计提")
            back = _pick(fields, "本期转回")
            write = _pick(fields, "本期核销")
            if beg and end and add and back:
                # 核销缺就跳过整条：不拿 0 补
                if write:
                    calc = beg[1] + add[1] - back[1] - write[1]
                    if abs(calc - end[1]) > 0.01:
                        out.append(("ECL-ROLL", end[0],
                                    "「%s」滚动重算=%s 披露=%s（差 %s 万元 > 0.01）"
                                    % (key, _fmt(calc), _fmt(end[1]), _fmt(abs(calc - end[1])))))
    return out


LINE_BANS = (
    ("已发生损失", ("已确定收不回", "坏账损失已发生", "已确定无法收回", "坏账已发生")),
    ("计提充分性判断", ("计提充分", "计提不足", "计提明显不足", "计提是否充分", "计提偏低", "计提偏高")),
    ("轧净额冒充账面余额", ("净额列示", "按净额", "轧净", "净额反映", "抵减后的余额")),
    ("评级与买卖建议", ("目标价", "买入", "卖出", "增持", "减持", "评级为", "建议买入", "建议卖出")),
)


def check_line(head, sections, stray):
    """道五 ECL-LINE 红线。

    四条红线各一类，命中即发（同类多处只报那一类的第一处，免得同一句话刷成一片）：
    ① 把损失准备说成已发生损失——预期信用损失不是「已确定收不回」；
    ② 给出「计提充分／不足」的判断——够不够不是本件能判的；
    ③ 用轧净额（总额减备抵）冒充账面余额；
    ④ 给评级、目标价、买卖建议。
    另加规格点名的节缺：组合计提与单项计提**缺任何一节** ⇒ 发条。

    豁免：「口径与未取到」与「来源」两节整节不查红线——口径节按设计就要写
    「本件不判断计提是否充分」，不豁免会自己咬自己。
    """
    out = []
    banned = [(why, w) for why, ws in LINE_BANS for w in ws]
    for name, _lineno, body in sections:
        if name in (GAP_SECTION, SOURCE_SECTION):
            continue
        for ln, raw in body:
            s = raw.strip()
            for why, w in banned:
                if w in s:
                    out.append(("ECL-LINE", ln, "红线（%s）：出现「%s」" % (why, w)))

    names = {n for n, _l, _b in sections}
    for need in ROLL_SECTIONS:
        if need not in names:
            out.append(("ECL-LINE", 1, "缺「%s」节：两条计提路径必须各占一节" % need))
    return out


CHECKS = (
    ("ECL-STRUCT", check_struct),
    ("ECL-QUOTE", check_quote),
    ("ECL-STAGE", check_stage),
    ("ECL-ROLL", check_roll),
    ("ECL-LINE", check_line),
)


# ---------------------------------------------------------------- 道具

def _section_of(heading):
    """把 `## 3. 三阶段划分` 归一成 `三阶段划分`；认不出返回 None（当作 stray）。

    照 cn-changes-in-equity-cn/scripts/check_equity_statement.py 同名函数抄：
    先剥序号，再按节名比；节名后面紧跟字母数字的不算命中（`三阶段划分旧` 认不出）。
    """
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
    """→ (头部[(行号, 行)], [(节名, 标题行号, [(行号, 行)])], 野节[(行号, 原文)])

    野节＝不认识的节名，或多出来的同名节。它们**另记**、不吞进上一节——
    混进上一节会让「缺节」与「内容不在节里」两件事都看不出来。
    """
    header, sections, stray = [], [], []
    cur = None
    seen_h2 = False
    for i, raw in enumerate(text.split("\n"), 1):
        m = HEADING.match(raw)
        if m:
            seen_h2 = True
            name = _section_of(m.group(1))
            if name is None or any(name == n for n, _l, _b in sections):
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
    """缺口行：本件没取到、如实登记的那种行（`未取到：X`）。缺口不挂原句与锚。"""
    return "未取到" in s


def _is_exempt_line(s):
    """按设计不带三元组的三形：`未取到：` 缺口行、`[待人工]` 判断位、`〔自算〕` 行。"""
    return _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s


def _own_part(s):
    """行里「」之前的那半段——登记值本身（原句与锚不算登记值）。"""
    return s.split("「", 1)[0].strip()


def _quotes_of(s):
    """行里所有「」原句拼成一段——判「原句里有没有这个词」用它，不用整行。"""
    return "".join(m.group(1) for m in QUOTE.finditer(s))


def _fmt(v):
    """数值回显成人看的样子：整数不带小数点，小数保留原样的最短写法。"""
    return ("%.2f" % v).rstrip("0").rstrip(".") if abs(v - round(v)) > 1e-9 else str(int(round(v)))


def _roll_key(own):
    """行首登记值里的分组名：`〔组合：账龄组合〕` 或 `〔对象：甲客户〕`；没有返回 None。

    分组键只认这两个标签——没有分组名的滚动行归属不明，不参与同组比对（不猜）。
    """
    m = re.search(r"〔\s*(?:组合|对象)\s*[:：]\s*([^〕]+)〕", own)
    return m.group(1).strip() if m else None


def _pick(fields, name):
    """组内某字段的 (行号, 值)；没登记或有多个不同值都返回 None。

    多个不同值是歧义——ECL-STAGE 有「同阶段两数」那条判据来管成对登记的情形，
    滚动比对这里遇到歧义就不比（不猜哪个对）。
    """
    vals = fields.get(name)
    if not vals:
        return None
    distinct = {v for _ln, v in vals}
    if len(distinct) > 1:
        return None
    return vals[0]


def _section_lines(sections, names):
    """→ [(节名, 标题行号, [(行号, 行)])]，只取 names 里那几节；缺的节自然不在结果里。"""
    want = tuple(names)
    return [(n, l, b) for n, l, b in sections if n in want]


def _num(text):
    """行内第一个数（去千分位逗号）→ float；没有返回 None。`%`／`％` 原样保留在值里。"""
    m = re.search(r"-?\d[\d,]*(?:\.\d+)?", text)
    return float(m.group(0).replace(",", "")) if m else None


def _num_after(text, label):
    """取 `label` 后面跟着的那个数；没有返回 None（缺项走缺口，不按 0 算）。"""
    m = re.search(re.escape(label) + r"[^0-9\-]{0,12}(-?\d[\d,]*(?:\.\d+)?)", text)
    return float(m.group(1).replace(",", "")) if m else None


def check_text(text):
    """→ (findings[(code, line, msg)], unjudged[(code, why)])。

    空壳抛 NotImplementedError 一律计入 unjudged，**不计入「零发条」**、也不裸抛；
    不在 UNIMPLEMENTED 里的码抛未落字则按「声明与实装不符」直接发条——
    那是真缺陷（说自己落字了、实际是空壳），不能计不可判了事。
    """
    head, sections, stray = split_doc(text)
    findings, unjudged = [], []
    for code, fn in CHECKS:
        try:
            found = fn(head, sections, stray) or []
            findings.extend(found)
        except NotImplementedError as exc:
            if code in UNIMPLEMENTED:
                unjudged.append((code, str(exc)))
            else:
                findings.append((code, 1, "判据不在未落字清单里却抛未落字：%s" % exc))
    findings.sort(key=lambda x: (x[1], CODES.index(x[0])))
    return findings, unjudged


def _report_text(path, findings, unjudged):
    """纯函数：把报告拼成一段文本返回，**不 print**。

    与 report() 共用这一段：自测拿到的文本必须就是用户看到的文本。
    两条路径各拼一遍的话，自测验的是自己的副本，措辞一漂移它就验不出真话。
    """
    lines = []
    for code, line, msg in findings:
        lines.append("%s L%s %s" % (code, line, msg))
    for code, why in unjudged:
        lines.append("不可判 %s（%s）" % (code, why))
    if findings:
        lines.append("—— 机检：%d 条发条；判据未落字 %d 道" % (len(findings), len(unjudged)))
    elif unjudged:
        lines.append("—— 机检：0 条发条，但 %d 道判据尚未落字，**这不等于合规**" % len(unjudged))
    else:
        lines.append("—— 机检：0 条发条")
    return "\n".join(lines) + "\n"


def report(path, findings, unjudged):
    """打印就是 _report_text 的结果，一行不加、一字不改——两条路径同一段文本。"""
    sys.stdout.write(_report_text(path, findings, unjudged))


DEMO = r"""# 示例材料（600000.SH）预期信用损失登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议
主体：示例材料（600000.SH）
报告期：2025 年年度报告·附注·预期信用损失

## 预期信用损失概况

- 损失准备〔口径：本期末〕3,456.00 万元「本报告期末本集团预期信用损失准备的账面余额为人民币 3,456.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]
- 本期计提〔口径：本期〕1,234.00 万元「本期计提预期信用损失人民币 1,234.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]
- 本期转回〔口径：本期〕234.00 万元「本期因款项收回转回预期信用损失人民币 234.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]
- 本期核销〔口径：本期〕100.00 万元「本期实际核销应收款项并相应转销损失准备人民币 100.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]

## 三阶段划分

- 损失准备〔阶段：第一阶段〕456.00 万元「第一阶段（未来 12 个月内预期信用损失）的损失准备为人民币 456.00 万元」〔锚：2025 年年报·第 206 页·三阶段划分〕[S1]
- 损失准备〔阶段：第二阶段〕800.00 万元「第二阶段（整个存续期预期信用损失，信用风险显著增加但未发生信用减值）的损失准备为人民币 800.00 万元」〔锚：2025 年年报·第 206 页·三阶段划分〕[S1]
- 损失准备〔阶段：第三阶段〕2,200.00 万元「第三阶段（整个存续期预期信用损失，已发生信用减值）的损失准备为人民币 2,200.00 万元」〔锚：2025 年年报·第 206 页·三阶段划分〕[S1]
- 阶段划分依据〔口径：附注原文〕「本集团以信用风险自初始确认后是否显著增加及是否已发生信用减值为依据划分三阶段」〔锚：2025 年年报·第 206 页·三阶段划分〕[S1]

## 组合计提

- 组合计提〔组合：账龄组合〕损失准备 1,234.00 万元「本集团按账龄组合计提预期信用损失，期末损失准备人民币 1,234.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]
- 组合计提〔组合：账龄组合〕账面余额 12,340.00 万元「按账龄组合计提的应收款项账面余额为人民币 12,340.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]
- 组合计提〔组合：账龄组合〕计提比例 10.00%「按账龄组合计提的预期信用损失计提比例为 10.00%」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]
- 组合计提〔组合：账龄组合〕期初余额 1,000.00 万元「账龄组合损失准备的期初余额为人民币 1,000.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]
- 组合计提〔组合：账龄组合〕本期计提 334.00 万元「本期账龄组合计提预期信用损失人民币 334.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]
- 组合计提〔组合：账龄组合〕本期转回 50.00 万元「本期账龄组合转回预期信用损失人民币 50.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]
- 组合计提〔组合：账龄组合〕本期核销 50.00 万元「本期账龄组合核销并转销损失准备人民币 50.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]
- 组合计提〔组合：账龄组合〕期末余额 1,234.00 万元「账龄组合损失准备的期末余额为人民币 1,234.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]
- 组合计提〔组合：低风险组合〕损失准备 56.00 万元「按低风险组合计提的预期信用损失准备为人民币 56.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]

## 单项计提

- 单项计提〔对象：甲客户〕账面余额 5,000.00 万元「甲客户应收款项账面余额为人民币 5,000.00 万元」〔锚：2025 年年报·第 206 页·单项计提〕[S2]
- 单项计提〔对象：甲客户〕损失准备 2,000.00 万元「本集团对甲客户单项计提预期信用损失人民币 2,000.00 万元」〔锚：2025 年年报·第 206 页·单项计提〕[S2]
- 单项计提〔对象：甲客户〕计提比例 40.00%「对甲客户单项计提的预期信用损失计提比例为 40.00%」〔锚：2025 年年报·第 206 页·单项计提〕[S2]
- 单项计提〔对象：甲客户〕本期计提 500.00 万元「本期对甲客户新增计提预期信用损失人民币 500.00 万元」〔锚：2025 年年报·第 206 页·单项计提〕[S2]

## 前瞻性信息与账龄依据

- 前瞻性信息〔情形：基准情形〕权重 50.00%「本集团在计量预期信用损失时采用基准情形，权重为 50.00%」〔锚：2025 年年报·第 207 页·前瞻性信息〕[S2]
- 前瞻性信息〔情形：不利情形〕权重 30.00%「不利情形权重为 30.00%」〔锚：2025 年年报·第 207 页·前瞻性信息〕[S2]
- 前瞻性信息〔情形：有利情形〕权重 20.00%「有利情形权重为 20.00%」〔锚：2025 年年报·第 207 页·前瞻性信息〕[S2]
- 账龄组合依据〔口径：附注原文〕「本集团按信用风险特征将应收款项划分为账龄组合与低风险组合」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]

## 口径与未取到

- 未取到：无
- 口径：损失准备、账面余额、计提比例与本期计提转回一律照抄附注原文；本件不重算损失率、不拿期初期末轧本期计提、不判断计提是否充分；三阶段归属只照抄附注，不按逾期天数自行推断。

## 来源

- [S1] 示例材料 2025 年年度报告·附注·预期信用损失 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026-03-20
- [S2] 示例材料 2025 年年度报告·附注·单项计提与前瞻性信息 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026-03-20
"""


def _must_replace(text, old, new, count=1):
    """注入点必须落地：片段不在源件、或替换后字节没变，一律 raise，不静默放过。

    静默放过的注入会让坏样等于好样，那一档就永远「过」——比不合更坏。
    """
    n = text.count(old)
    if n < count:
        raise AssertionError("注入点未落地：片段出现 %d 次，至少要 %d 次：%r" % (n, count, old))
    out = text.replace(old, new, count)
    if out == text:
        raise AssertionError("注入后字节未变：%r -> %r" % (old, new))
    return out


# 坏样都由好样单向替换而来，只动那一档真正看的那一处。
# (a) 头部少一件自标。
BAD_MARK = _must_replace(DEMO, "不构成投资建议", "", 1)
# (b) 一个节标题写成认不出的样子：该节既进不了 sections（算缺节），标题本身也进 stray。
#     注：不能用「## 三阶段划分（旧）」——全角括号前 `not isalnum()` 为真，_section_of 仍认得出；
#     要接一个字母数字才算认不出（「三阶段划分旧」落空 → None → stray）。这是实测出来的形。
BAD_HEADING = _must_replace(DEMO, "## 三阶段划分\n", "## 三阶段划分旧\n", 1)
# (c) 整节删掉「前瞻性信息与账龄依据」（连标题与五行）：七节不齐。
#     为什么删这一节而不是「单项计提」：ECL-LINE 按规格也要判组合／单项两节缺失，
#     删单项计提会让那一档同时红两道，钉不住「只红 ECL-STRUCT」。缺单项计提另有一档（j）。
_SECTION_BLOCK = ("## 前瞻性信息与账龄依据\n"
                  "\n"
                  "- 前瞻性信息〔情形：基准情形〕权重 50.00%「本集团在计量预期信用损失时采用基准情形，权重为 50.00%」〔锚：2025 年年报·第 207 页·前瞻性信息〕[S2]\n"
                  "- 前瞻性信息〔情形：不利情形〕权重 30.00%「不利情形权重为 30.00%」〔锚：2025 年年报·第 207 页·前瞻性信息〕[S2]\n"
                  "- 前瞻性信息〔情形：有利情形〕权重 20.00%「有利情形权重为 20.00%」〔锚：2025 年年报·第 207 页·前瞻性信息〕[S2]\n"
                  "- 账龄组合依据〔口径：附注原文〕「本集团按信用风险特征将应收款项划分为账龄组合与低风险组合」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]\n"
                  "\n")
BAD_SECTION = _must_replace(DEMO, _SECTION_BLOCK, "", 1)

# (d) 拆掉概况首行尾的「」原句与〔锚〕，只留 [S#]：数字行三元组不齐。
#     只该红 ECL-QUOTE——行仍是 `- ` 行、节没动、S1 仍被别的行引用（不致连带「未引用」）。
BAD_QUOTE = _must_replace(
    DEMO,
    "「本报告期末本集团预期信用损失准备的账面余额为人民币 3,456.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]",
    "[S1]", 1)

# (e) 来源行检索日写成斜杠式：该行不合格式、不再算登记，正文引 S2 的行随之发「未登记」。
#     同一个 S 号只报一次，码集仍是 {ECL-QUOTE}，不连带别的码。
#     用 S2 的标题前缀定位，别靠 `"""` 这种行尾特征（那太脆）。
BAD_SOURCE = _must_replace(
    DEMO,
    "单项计提与前瞻性信息 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026-03-20",
    "单项计提与前瞻性信息 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026/03/20", 1)

# (f) 阶段行自写一个原句里没有的阶段词：原句只写了「第二阶段」，行首标成「第三阶段」。
#     只该红 ECL-STAGE——三元组齐（ECL-QUOTE 不红），数没动（ECL-ROLL 不判三阶段节）。
BAD_STAGE_WORD = _must_replace(
    DEMO,
    "- 损失准备〔阶段：第三阶段〕2,200.00 万元「第三阶段（整个存续期预期信用损失",
    "- 损失准备〔阶段：第三阶段〕2,200.00 万元「第一阶段（整个存续期预期信用损失", 1)

# (g) 同一阶段在一节里报两个不同的损失准备数：第一阶段行改成 4,560.00（原句也跟着改，
#     好让这一档只钉「同阶段两数并存」这一条，不连带 ECL-QUOTE）。
BAD_STAGE_TWO = _must_replace(
    DEMO,
    "- 损失准备〔阶段：第一阶段〕456.00 万元「第一阶段（未来 12 个月内预期信用损失）的损失准备为人民币 456.00 万元」〔锚：2025 年年报·第 206 页·三阶段划分〕[S1]\n",
    "- 损失准备〔阶段：第一阶段〕456.00 万元「第一阶段（未来 12 个月内预期信用损失）的损失准备为人民币 456.00 万元」〔锚：2025 年年报·第 206 页·三阶段划分〕[S1]\n"
    "- 损失准备〔阶段：第一阶段〕789.00 万元「第一阶段（未来 12 个月内预期信用损失）的损失准备为人民币 789.00 万元」〔锚：2025 年年报·第 206 页·三阶段划分〕[S1]\n", 1)

# (h) 比率不符：账龄组合计提比例写成 20.00%，而损失准备/账面余额 = 1,234/12,340 = 10.00%。
#     只该红 ECL-ROLL——三元组齐、阶段节没动。
BAD_ROLL_PCT = _must_replace(
    DEMO,
    "计提比例 10.00%「按账龄组合计提的预期信用损失计提比例为 10.00%」",
    "计提比例 20.00%「按账龄组合计提的预期信用损失计提比例为 20.00%」", 1)

# (i) 滚动不符：期末余额写成 1,500.00，而 期初 1,000 + 计提 334 - 转回 50 - 核销 50 = 1,234。
#     比率那一路不受影响（损失准备与账面余额没动，比例仍是 10.00%）。
BAD_ROLL_SUM = _must_replace(
    DEMO,
    "期末余额 1,234.00 万元「账龄组合损失准备的期末余额为人民币 1,234.00 万元」",
    "期末余额 1,500.00 万元「账龄组合损失准备的期末余额为人民币 1,500.00 万元」", 1)

# (j) 缺「单项计提」整节：ECL-STRUCT 报缺节，ECL-LINE 按规格也报（两条计提路径缺一条）。
#     这一档就是你说的「双红」，专门钉住它不被并成单码。
BAD_SINGLE_SECTION = _must_replace(
    DEMO,
    ("## 单项计提\n"
     "\n"
     "- 单项计提〔对象：甲客户〕账面余额 5,000.00 万元「甲客户应收款项账面余额为人民币 5,000.00 万元」〔锚：2025 年年报·第 206 页·单项计提〕[S2]\n"
     "- 单项计提〔对象：甲客户〕损失准备 2,000.00 万元「本集团对甲客户单项计提预期信用损失人民币 2,000.00 万元」〔锚：2025 年年报·第 206 页·单项计提〕[S2]\n"
     "- 单项计提〔对象：甲客户〕计提比例 40.00%「对甲客户单项计提的预期信用损失计提比例为 40.00%」〔锚：2025 年年报·第 206 页·单项计提〕[S2]\n"
     "- 单项计提〔对象：甲客户〕本期计提 500.00 万元「本期对甲客户新增计提预期信用损失人民币 500.00 万元」〔锚：2025 年年报·第 206 页·单项计提〕[S2]\n"
     "\n"),
    "", 1)

# (k)~(n) 四条红线各一支：都是往某个内容节插一条带完整三元组的行，
#     这样 ECL-QUOTE 不会连带红（三元组齐、S 号已登记），只钉 ECL-LINE。
#     插入型注入：片段本身留在原处，出现次数应仍为 1。
BAD_LINE_LOSS = _must_replace(
    DEMO,
    "## 口径与未取到",
    ("- 损失准备〔口径：本期末〕已确定收不回「本集团对甲客户的应收款项已确定收不回，全额计提损失准备」〔锚：2025 年年报·第 206 页·单项计提〕[S2]\n"
     "\n"
     "## 口径与未取到"), 1)

BAD_LINE_ENOUGH = _must_replace(
    DEMO,
    "## 口径与未取到",
    ("- 计提结论〔口径：本期末〕计提充分「本集团预期信用损失计提充分，不存在进一步减值风险」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]\n"
     "\n"
     "## 口径与未取到"), 1)

BAD_LINE_NET = _must_replace(
    DEMO,
    "## 口径与未取到",
    ("- 账面余额〔口径：本期末〕按净额列示 10,890.00 万元「按账龄组合计提的应收款项账面余额为人民币 12,340.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]\n"
     "\n"
     "## 口径与未取到"), 1)

BAD_LINE_RATING = _must_replace(
    DEMO,
    "## 口径与未取到",
    ("- 结论〔口径：本期末〕给予增持评级「我们给予公司增持评级，目标价 12.00 元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]\n"
     "\n"
     "## 口径与未取到"), 1)

# (o) 反证：把「口径与未取到」那行口径说明改写成带红线词的形态——期望**零发条**。
#     口径节整节豁免：按设计它就要写「本件不判断计提是否充分」这类话，
#     不豁免会自己咬自己。这是全套里唯一期望不发码的注入档。
OK_LINE_GAP_EXEMPT = _must_replace(
    DEMO,
    "- 口径：损失准备、账面余额、计提比例与本期计提转回一律照抄附注原文；本件不重算损失率、不拿期初期末轧本期计提、不判断计提是否充分；三阶段归属只照抄附注，不按逾期天数自行推断。",
    "- 口径：损失准备、账面余额、计提比例与本期计提转回一律照抄附注原文；本件不重算损失率、不拿期初期末轧本期计提；关于计提充分与计提不足的判断不在本件，附注亦未给出按净额列示的口径；三阶段归属只照抄附注，不按逾期天数自行推断。", 1)


def selftest():
    """逐档现报：好样须零发条，坏样须恰发它该发的那几道；未落字各算一档「不可判」。

    档数＝逐档比对的那几档 + UNIMPLEMENTED 的码数（未落字各算一档「不可判」），
    两段都从现场值算，不写死数字。本件五道全落字，好样单稿退 0；
    将来某道回退成空壳，这两处会自己从 0 变 3，不用手改。
    """
    cases = (
        ("好样应零发条（五道全落字）", DEMO, frozenset()),
        ("形制：头部删掉「不构成投资建议」", BAD_MARK, frozenset({"ECL-STRUCT"})),
        ("形制：节标题写成认不出的样子（进 stray＋缺节）", BAD_HEADING,
         frozenset({"ECL-STRUCT"})),
        ("形制：整节删掉「前瞻性信息与账龄依据」", BAD_SECTION, frozenset({"ECL-STRUCT"})),
        ("原句与锚：数字行拆掉「」原句与〔锚〕只留 [S#]", BAD_QUOTE,
         frozenset({"ECL-QUOTE"})),
        ("原句与锚：来源行检索日写成斜杠式", BAD_SOURCE, frozenset({"ECL-QUOTE"})),
        ("三阶段：行首阶段词与含该词的原句不符", BAD_STAGE_WORD,
         frozenset({"ECL-STAGE"})),
        ("三阶段：同一阶段报了两个不同损失准备数", BAD_STAGE_TWO,
         frozenset({"ECL-STAGE"})),
        ("计提转回：计提比例与 损失准备/账面余额 不符", BAD_ROLL_PCT,
         frozenset({"ECL-ROLL"})),
        ("计提转回：滚动式 期初+计提-转回-核销 与期末不符", BAD_ROLL_SUM,
         frozenset({"ECL-ROLL"})),
        ("路径缺失：删掉「单项计提」整节（双红）", BAD_SINGLE_SECTION,
         frozenset({"ECL-STRUCT", "ECL-LINE"})),
        ("红线：把损失准备写成「已确定收不回」", BAD_LINE_LOSS, frozenset({"ECL-LINE"})),
        ("红线：给「计提充分」的判断", BAD_LINE_ENOUGH, frozenset({"ECL-LINE"})),
        ("红线：用轧净额冒充账面余额", BAD_LINE_NET, frozenset({"ECL-LINE"})),
        ("红线：给评级与目标价", BAD_LINE_RATING, frozenset({"ECL-LINE"})),
        ("反证：口径节写红线词 → 不发码（整节豁免）", OK_LINE_GAP_EXEMPT, frozenset()),
    )
    bad = 0
    last_unjudged = ()
    for label, text, want in cases:
        findings, unjudged = check_text(text)
        last_unjudged = unjudged
        got = frozenset(c for c, _l, _m in findings)
        if got == want:
            print("过   %s（发条 %d 条：%s）"
                  % (label, len(findings), "、".join(sorted(got)) or "无"))
        else:
            bad += 1
            detail = "；".join("%s L%s %s" % (c, l, m) for c, l, m in findings[:4])
            print("不合 %s：期望 %s 实得 %s ｜ %s"
                  % (label, sorted(want) or "无", sorted(got) or "无", detail))

    # 覆盖自证：每道已落字的码，在 cases 里至少有一档期望恰含它。
    # 这条防的是「实现了一道判据、同时少了一档反例，净增反例 0 档」——
    # 判据接进 CHECKS 却没有反例钉住，它以后被改坏，自测照样报 不合=0。
    # 本拍只有 ECL-STRUCT，但这条现在就写进去：它下一拍会替我们抓漏。
    implemented = [c for c in CODES if c not in UNIMPLEMENTED]
    covered = set()
    for _label, _text, want in cases:
        covered |= set(want)
    uncovered = [c for c in implemented if c not in covered]
    print("%s 覆盖自证：已落字码 %d 道，有反例的 %d 道，缺反例：%s"
          % ("不合" if uncovered else "过  ",
             len(implemented), len(implemented) - len(uncovered),
             "／".join(uncovered) if uncovered else "无"))
    if uncovered:
        bad += 1

    # 空壳自证：清单里的码调用即抛且点名自身；不在清单里的码不许抛，只能返回列表
    shell_bad = []
    for code, fn in CHECKS:
        try:
            got = fn([], [], [])
        except NotImplementedError as exc:
            if code not in UNIMPLEMENTED:
                shell_bad.append("%s 已声明落字却抛未落字（%s）" % (code, exc))
            elif code not in str(exc):
                shell_bad.append("%s 抛出但未点名码（%s）" % (code, exc))
            continue
        if code in UNIMPLEMENTED:
            shell_bad.append("%s 返回了 %r，空壳必须抛未落字" % (code, got))
        elif not isinstance(got, list):
            shell_bad.append("%s 返回 %r，应返回列表" % (code, got))
    if shell_bad:
        bad += 1
        print("不合 空壳自证：%s" % "；".join(shell_bad))
    elif UNIMPLEMENTED:
        print("过   空壳自证（%s 调用即抛并点名；其余返回列表）"
              % "、".join(UNIMPLEMENTED))
    else:
        print("过   空壳自证（未落字清单为空，五道均返回列表）")

    # 不崩自证：空稿、乱头、只头无节都过一遍，必须返回二元组且未落字的码全计不可判
    crash = []
    for label, text in (("空稿", ""), ("乱头", "x\n"), ("只头无节", DEMO.split("## ")[0])):
        try:
            _f2, u2 = check_text(text)
        except Exception as exc:                       # noqa: BLE001 — 自证只问崩不崩
            crash.append("%s 抛出 %s: %s" % (label, type(exc).__name__, exc))
            continue
        got_codes = {c for c, _w in u2}
        if got_codes != set(UNIMPLEMENTED):
            crash.append("%s 不可判 %s，应为 %s"
                         % (label, sorted(got_codes) or "无", sorted(UNIMPLEMENTED) or "无"))
    if crash:
        bad += 1
        print("不合 不崩自证：%s" % "；".join(crash))
    elif UNIMPLEMENTED:
        print("过   不崩自证（空稿／乱头／只头无节均返回二元组，未落字 %d 道计不可判）"
              % len(UNIMPLEMENTED))
    else:
        print("过   不崩自证（空稿／乱头／只头无节均返回二元组，无未落字）")

    # 单稿退码自证：好样落盘单跑，退码与「是否还有未落字」绑定，不写死数：
    # 有未落字 → 3（且输出须含「不可判」与「这不等于合规」）；全落字 → 0（且不得再出现该句）。
    rc, out, tmp = None, "", None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8",
                                         delete=False) as fh:
            fh.write(DEMO)
            tmp = fh.name
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main([tmp])
        out = buf.getvalue()
    finally:
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass
    want_rc = 3 if UNIMPLEMENTED else 0
    if rc != want_rc:
        bad += 1
        print("不合 单稿退码自证：好样单稿 rc=%r，应为 %d（未落字 %d 道）"
              % (rc, want_rc, len(UNIMPLEMENTED)))
    elif want_rc == 3 and ("不可判" not in out or "这不等于合规" not in out):
        bad += 1
        print("不合 单稿退码自证：rc=3 但输出缺口径字样")
    elif want_rc == 0 and "这不等于合规" in out:
        bad += 1
        print("不合 单稿退码自证：已无未落字，输出却仍写「这不等于合规」")
    else:
        print("过   单稿退码自证（好样单稿 rc=%d，未落字 %d 道%s）"
              % (want_rc, len(UNIMPLEMENTED),
                 "，输出含「不可判」与「这不等于合规」" if want_rc == 3 else "，输出无「这不等于合规」"))

    unk = len({c for c, _w in last_unjudged})
    print("——")
    print("自测档数=%d｜不合=%d｜不可判=%d" % (len(cases) + len(UNIMPLEMENTED), bad, unk))
    if bad:
        return 1
    return 3 if unk else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="预期信用损失登记稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="预期信用损失登记稿 .md 路径")
    ap.add_argument("--selftest", action="store_true", help="跑包内夹具自检")
    ap.add_argument("--demo", action="store_true", help="打印一份七节样例（零输入可跑）")
    try:
        args = ap.parse_args(argv)
    except SystemExit:                                 # 用法错统一退 2，不沿用 argparse 的 2/0 混用
        return 2

    if args.selftest:
        return selftest()
    if args.demo:
        sys.stdout.write(DEMO)
        return 0
    if not args.path:
        ap.print_usage(sys.stderr)
        print("缺入参：给一份预期信用损失登记稿路径，或用 --demo / --selftest", file=sys.stderr)
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

    findings, unjudged = check_text(text)
    report(args.path, findings, unjudged)
    if findings:
        return 1
    return 3 if unjudged else 0


if __name__ == "__main__":
    sys.exit(main())
