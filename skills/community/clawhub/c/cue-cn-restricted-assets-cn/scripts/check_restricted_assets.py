#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_restricted_assets.py — 受限资产登记稿五道机检（零网络、零外发）

**五道均已落字**（`UNIMPLEMENTED` 现值为空）：形制、原句与锚、合计与分项、比例重算、红线。
没有 `_not_judged` 调用残留（该入口仍留在原地备用，见其 docstring）——判据缺失**不许**用返回空表糊过去：返回 [] 会被读成
「这道跑过了、零发条」，而我们根本没跑。若将来再把某道退回空壳，把码登记进
`UNIMPLEMENTED` 并让它抛 NotImplementedError：由 `check_text` 捕获计入 `unjudged`、不裸抛，
零发条但有未落字的稿子退 3，报告里明写「这不等于合规」。

用法：
    python3 scripts/check_restricted_assets.py <受限资产登记稿>.md
    python3 scripts/check_restricted_assets.py --selftest
    python3 scripts/check_restricted_assets.py --demo     打印一份七节样例（零输入可跑）

七节（按序，`## ` 起节）：
    受限资产概况／货币资金受限／非货币资产受限／受限原因与期限／与负债的对应
    ／口径与未取到／来源

五道码（状态以 `UNIMPLEMENTED` 现值为准，下面写的是**这道判什么**）：

道一 RA-STRUCT 形制【已落字】
  头部（第一个 `## ` 之前）三件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议；
  七节齐且按序；认不出的节标题与多出的同名节记 stray 逐条发。
  **只判形，不判内容**——内容对不对是另四道的事，这里越界会让一支注入同时红两道。
  不判「主体：」「报告期：」：本件规格只列三件自标，不自行加判据。

道二 RA-QUOTE 原句与锚【已落字】
  五个内容节的数字行须挂齐「」原句（≥8 字、非纯数字标点）＋〔锚：…〕＋`[S#]` 三元组，可挂多组；
  例外只有三形：`未取到：` 行、`[待人工]` 行、`〔自算〕` 行；
  来源行须合 `- [S#] 标题 | http(s) URL | 检索日 YYYY-MM-DD`；
  正文引用与来源登记**两向**都要对得上；来源节一条合规行都没有则单独发一条。
  **不核对引号里的数与行首是否同一**（那是 RA-SUM／RA-RATIO 的活）。

道三 RA-SUM 合计与分项【已落字】
  ① 「受限资产概况」里的合计数与各节分项之和比对，差 > 0.01 万元即发（记 `分项和=X 披露合计=Y`）；
  ② 某类资产的受限金额大于该类资产账面总额（附注给了总额才判）⇒ 发。
  **任一侧缺失整条跳过**，不按 0 算。

道四 RA-RATIO 比例重算【已落字】
  行内同现受限金额与资产总额（或占总资产比例）时，按 `受限金额 / 总额` 重算，
  与披露比例差 > 0.05 个百分点 ⇒ 发；受限比例 > 100% ⇒ 单独发一条。
  只照抄分子分母重算，不替附注改口径。

道五 RA-LINE 红线【已落字】
  ① 给「资产质量好／差」「偿债能力充足／不足」的判断；
  ② 把受限资产说成「已损失」或「已减值」；
  ③ 拿受限金额当可动用金额（「可动用货币资金」写成受限口径）；
  ④ 给评级、目标价、买卖建议。
  另加：「货币资金受限」节缺 ⇒ 发条（这一节是本件存在的理由）。
  「口径与未取到」与「来源」两节整节豁免。

退码：0 五道全过 / 1 有发条 / 2 用法错（缺参数或未知参数）
      / 3 读不到文件或空稿，或零发条但仍有未落字判据（`UNIMPLEMENTED` 非空时）。
      五道全落字，好样单稿现退 0；若哪天退回空壳，退码自己跟着变，不用手改。

边界（不是这几枚件，别互相代填）：
    不是 `cn-share-pledge-tracker`：那枚跟踪股东所持股份的质押与解押，标的是「股东手里的股票」；
    本件标的是「公司账上的资产」。
    不是 `cn-contingency-commitment-cn`：那枚管或有事项与承诺，含对外担保但只登记担保本身；
    本件登记的是被担保／被抵押的资产那一侧。
    不是 `cn-working-capital-quality`：那枚管存货与应收的余额与账龄，不问受限。

包面（下一拍写 SKILL.md 时用，这一拍只登记）：
    SLUG = "cue-cn-restricted-assets-cn"
    consumes: [structured-note]／produces: [structured-note]
    inputs: [announcement-doc, disclosure-file]
    topics: 受限资产／所有权受限／抵押质押／担保物／资产冻结
"""

import argparse
import contextlib
import io
import os
import re
import sys
import tempfile

SLUG = "cue-cn-restricted-assets-cn"

CODES = ("RA-STRUCT", "RA-QUOTE", "RA-SUM", "RA-RATIO", "RA-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议")

SECTIONS = ("受限资产概况", "货币资金受限", "非货币资产受限",
            "受限原因与期限", "与负债的对应", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"

# 未落字的码：抛未落字一律计「不可判」，不许并进「不合」，也不许算「过」；
# 不在清单里却抛未落字＝声明与实装不符，由 check_text 直接发条。
# 五道全部落字，清单为空——别为了让自测有东西可测而硬留一个返回空表的空壳。
UNIMPLEMENTED = ()

HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")

TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
ANCHOR_BLOCK = re.compile(r"〔\s*锚\s*[:：][^〕]*〕")
ANCHOR_REF = re.compile(r"\[(S\d+)\]")

SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)"
    r"\|\s*(?P<url>https?://\S+)\s*\|"
    r"\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$"
)


# ---------------------------------------------------------------- 判据（五道全落字）

def _not_judged(code, why):
    """空壳的唯一出口：抛未落字，由 check_text 捕获计入「不可判」，不返回空表。

    五道全落字后本函数没有调用方，仍留在原地——与 `cn-expected-credit-loss-cn` 同一形制：
    将来某道若回退成空壳（重新登记进 `UNIMPLEMENTED`），它得有这条唯一出口，
    而不是顺手 `return []`（那会被读成「跑过了、零发条」）。
    """
    raise NotImplementedError("%s 未落字：%s" % (code, why))


def check_struct(head, sections, stray):
    """道一 RA-STRUCT 形制：头部三件自标、七节齐且按序、节标题可识别。

    只判「形」：自标在不在、节名在不在、顺序对不对、有没有野节。内容对不对是另四道的事——
    这里不越界，否则一支注入会同时红两道、分不清归属。
    不判「主体：」「报告期：」：本件规格只列三件自标，不自行加判据。
    「货币资金受限」整节缺失归 RA-LINE 判（那一节是本件存在的理由），这里按常规算缺节，
    两道各说各的：一支注入同时红两道是规格写明的，不是越界。
    """
    out = []
    htext = "\n".join(s for _i, s in head)
    for mark in MARK_TEXTS:
        if mark not in htext:
            out.append(("RA-STRUCT", 1, "头部缺自标「%s」" % mark))

    # 丙：野节（认不出的节名／多出的同名节）逐条报，行号用 stray 给的
    for lineno, raw in stray:
        out.append(("RA-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw))

    # 丁：七节须齐且按序
    names = [n for n, _l, _b in sections]
    missing = [n for n in SECTIONS if n not in names]
    if missing:
        out.append(("RA-STRUCT", 1, "缺节：%s" % "／".join(missing)))
    elif names != list(SECTIONS):
        out.append(("RA-STRUCT", 1, "节序不对：现序 %s，应序 %s"
                    % ("／".join(names), "／".join(SECTIONS))))
    return out


def check_quote(head, sections, stray):
    """道二 RA-QUOTE 原句与锚：三元组齐全，来源两向对应。

    只认**形**：数字行有没有「」原句、〔锚：…〕与 [S#] 三件；引号里的数与行首的数是同一
    这件事不在这里管（那是 RA-SUM／RA-RATIO 的活）。越界会让一支注入同时红两道。

    例外只有三形（`_is_exempt_line`）：`未取到：` 缺口行、`[待人工]` 判断位、`〔自算〕` 行——
    这三形按设计不带原句。
    """
    out = []

    # 甲：五个内容节里每个数字行都得挂齐三元组；原句要像原句
    body_refs = {}                                 # [S#] → 首次出现的行号
    for _name, _lineno, body in _section_lines(sections, CONTENT_SECTIONS):
        for ln, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_exempt_line(s):
                continue
            own = _own_part(s)
            numeric = bool(re.search(r"\d", own)) or "%" in own or "％" in own
            trips = list(TRIPLE.finditer(s))
            if numeric and not trips:
                out.append(("RA-QUOTE", ln, "数字行缺「」原句＋〔锚〕＋[S#] 三元组：%s" % own))
                continue
            for m in trips:
                q = m.group("q").strip()
                if len(q) < 8:
                    out.append(("RA-QUOTE", ln, "原句太短（%d 字，应≥8）：%s" % (len(q), q)))
                elif not re.search(r"[^\d\s.,%％:：/年月日\-]", q):
                    out.append(("RA-QUOTE", ln, "原句只有数字／标点，不是原句：%s" % q))
                body_refs.setdefault(m.group("s"), ln)

    # 乙：来源节的行须合格式，合格式的才算「登记」
    registered = {}
    src_finding_lines = 0
    for _name, _lineno, body in _section_lines(sections, (SOURCE_SECTION,)):
        for ln, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_exempt_line(s):
                continue
            src_finding_lines += 1
            m = SOURCE_LINE.match(s)
            if m:
                registered.setdefault(m.group("s"), ln)
            else:
                out.append(("RA-QUOTE", ln,
                            "来源行不合格式（应 `- [S#] 标题 | http(s) URL | 检索日 YYYY-MM-DD`）：%s"
                            % s))

    # 丙：两向对应各发一条——正文引了未登记的，登记了没被引用的
    for ref, ln in body_refs.items():
        if ref not in registered:
            out.append(("RA-QUOTE", ln, "正文引用了来源节未登记的 [%s]" % ref))
    for ref, ln in registered.items():
        if ref not in body_refs:
            out.append(("RA-QUOTE", ln, "来源行 [%s] 未被任何正文行引用" % ref))
    if src_finding_lines == 0:
        out.append(("RA-QUOTE", 1, "来源节一条来源行都没有"))
    return out


def check_sum(head, sections, stray):
    """道三 RA-SUM 合计与分项。

    ① 取「受限资产概况」节里 `受限资产合计` 后面那个数（万元），与「货币资金受限」＋
       「非货币资产受限」两节所有金额行之和比对，差 > 0.01 万元 ⇒ 发，记 `分项和=X 披露合计=Y`。
    ② 某行同时给了受限金额与「账面总额／资产总额」，且受限金额更大 ⇒ 发。
       只在同一行里有这两个数时才判，跨行不算（跨行归属不明）。

    **任一侧缺失 ⇒ 整条跳过**，不猜、不按 0 算——附注没给的数不能凭空补一个 0 去让式子成立。
    **两节缺任何一节也整条跳过**：缺节是 RA-STRUCT 与 RA-LINE 的事，这里再比一次会让
    「删掉货币资金受限」那支注入同时红三道，归属就混了。
    """
    out = []

    # ① 合计 vs 分项和
    names = {n for n, _l, _b in sections}
    if not set(("货币资金受限", "非货币资产受限")) <= names:
        return out                     # 缺节不在这里判：那是 STRUCT／LINE 的活

    total = None
    for _name, _lineno, body in _section_lines(sections, ("受限资产概况",)):
        for ln, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_exempt_line(s):
                continue
            v = _amount_after(_own_part(s), "受限资产合计")
            if v is not None:
                total = (ln, v)
                break
        if total:
            break

    parts = []
    for _name, _lineno, body in _section_lines(sections, ("货币资金受限", "非货币资产受限")):
        for ln, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_exempt_line(s):
                continue
            v = _amount_of(_own_part(s))
            if v is not None:
                parts.append((ln, v))

    if total is not None and parts:
        psum = sum(v for _ln, v in parts)
        if abs(psum - total[1]) > 0.01:
            out.append(("RA-SUM", total[0],
                        "分项和=%s 披露合计=%s（差 %s 万元 > 0.01）"
                        % (_fmt(psum), _fmt(total[1]), _fmt(abs(psum - total[1])))))

    # ② 受限金额 > 该类资产账面总额（同一行内才判）
    for _name, _lineno, body in _section_lines(sections, CONTENT_SECTIONS):
        for ln, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_exempt_line(s):
                continue
            own = _own_part(s)
            restricted = _amount_of(own)
            cap = _amount_after(own, "账面总额")
            if cap is None:
                cap = _amount_after(own, "资产总额")
            if restricted is None or cap is None:
                continue
            if restricted > cap:
                out.append(("RA-SUM", ln,
                            "受限金额 %s 万元 > 该类资产账面总额 %s 万元"
                            % (_fmt(restricted), _fmt(cap))))
    return out


def check_ratio(head, sections, stray):
    """道四 RA-RATIO 比例重算：受限金额 / 资产总额 与披露比例对不上就发。

    只在**同一行**里同时拿到「受限金额」「资产总额」与「披露比例」时才判——
    跨行拼出来的分母归属不明，宁可跳过也不猜。任一侧缺失 ⇒ 整条跳过，不按 0 算。

    比例 > 100% 另发一条：那不是四舍五入能解释的，说明分子分母取错了行。
    """
    out = []
    for _name, _lineno, body in _section_lines(sections, CONTENT_SECTIONS):
        for ln, raw in body:
            s = raw.strip()
            if not _is_finding_line(s) or _is_exempt_line(s):
                continue
            own = _own_part(s)
            restricted = _amount_after(own, "受限金额")
            if restricted is None:
                restricted = _amount_after(own, "受限资产")
            base = _amount_after(own, "资产总额")
            if base is None:
                base = _amount_after(own, "总资产")
            m = PCT.search(own)
            if restricted is None or base is None or m is None:
                continue                      # 缺一即跳过：不从别处借数、不按 0 算
            disclosed = float(m.group(1).replace(",", ""))
            if abs(base) < 1e-9:
                # 分母为 0 不是发条，是这句算式无从成立——如实记一句，不静默吞掉、也不除零崩
                out.append(("RA-RATIO", ln, "资产总额为 0，比例无从重算：%s" % own))
                continue
            calc = restricted / base * 100.0
            if calc > 100.0:
                out.append(("RA-RATIO", ln,
                            "比例重算=%s%% > 100%%，分子分母取错行：受限 %s / 总额 %s"
                            % (_fmt(calc), _fmt(restricted), _fmt(base))))
                continue
            if abs(calc - disclosed) > 0.05:
                out.append(("RA-RATIO", ln,
                            "比例重算=%s%% 披露=%s%%（差 %s 个百分点 > 0.05）"
                            % (_fmt(calc), _fmt(disclosed), _fmt(abs(calc - disclosed)))))
    return out


# 红线词表：每条 (原因, (词…))。同类多处只报第一处，免得同一句话刷成一片。
LINE_BANS = (
    ("资产质量与偿债能力判断",
     ("资产质量好", "资产质量差", "偿债能力充足", "偿债能力不足", "偿债压力大")),
    ("把受限资产说成已损失",
     ("已损失", "已减值", "无法收回")),
    ("拿受限金额当可动用金额",
     ("可动用", "可自由支配", "实际可用")),
    ("评级与买卖建议",
     ("目标价", "买入", "卖出", "增持", "减持", "评级为", "建议买入", "建议卖出")),
)


def check_line(head, sections, stray):
    """道五 RA-LINE 红线。

    四类词各一类，命中即发（同类多处只报那一类的第一处）。
    另加一条**结构判据**：「货币资金受限」节缺 ⇒ 发——这一节是本件存在的理由
    （账面货币资金里有多少动不了），缺了这一节，登记表的用途就没了。

    「口径与未取到」与「来源」两节整节豁免：口径节按设计就要写
    「本件不判断资产质量与偿债能力」，不豁免会自己咬自己。
    """
    out = []
    banned = [(why, w) for why, ws in LINE_BANS for w in ws]
    for name, _lineno, body in sections:
        if name in (GAP_SECTION, SOURCE_SECTION):
            continue
        for ln, raw in body:
            s = raw.strip()
            fired = set()                 # 本行已报过的类：同一句话里同类命中只报第一处
            for why, w in banned:
                if why in fired:
                    continue
                if w in s:
                    fired.add(why)
                    out.append(("RA-LINE", ln, "红线（%s）：出现「%s」" % (why, w)))

    names = {n for n, _l, _b in sections}
    if "货币资金受限" not in names:
        out.append(("RA-LINE", 1, "缺「货币资金受限」节：本件就是要登记动不了的那部分货币资金"))
    return out


CHECKS = (
    ("RA-STRUCT", check_struct),
    ("RA-QUOTE", check_quote),
    ("RA-SUM", check_sum),
    ("RA-RATIO", check_ratio),
    ("RA-LINE", check_line),
)


# ---------------------------------------------------------------- 道具

def _section_of(heading):
    """把 `## 3. 货币资金受限` 归一成 `货币资金受限`；认不出返回 None（当作 stray）。

    照 cn-changes-in-equity-cn/scripts/check_equity_statement.py 同名函数抄：
    先剥序号，再按节名比；节名后面紧跟字母数字的不算命中（`货币资金受限旧` 认不出）。
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


def _section_lines(sections, names):
    """→ [(节名, 标题行号, [(行号, 行)])]，只取 names 里那几节；缺的节自然不在结果里。"""
    want = tuple(names)
    return [(n, l, b) for n, l, b in sections if n in want]


_NUM = r"-?\d[\d,]*(?:\.\d+)?"
# 金额：数 + 万元。只认带「万元」的，免得把「3.20%」「4 类」当成金额取走。
AMOUNT = re.compile(r"(" + _NUM + r")\s*万元")
# 百分比：3.20% 或 3.20％——全角半角都认。只认带 % 的数，
# 否则「4 类」那种类别数会被当成比例。
PCT = re.compile(r"(" + _NUM + r")\s*[%％]")


def _amount_of(text):
    """行内第一个「…万元」金额（去千分位）→ float；没有返回 None。

    只认带「万元」的数：登记值里常有百分比（3.20%）和类别数（4 类），
    不带单位地取第一个数会把它们当金额，合计就永远对不上。
    """
    m = AMOUNT.search(text)
    return float(m.group(1).replace(",", "")) if m else None


def _amount_after(text, label):
    """取 `label` 后面跟着的那个「…万元」金额；没有返回 None（缺项跳过，不按 0 算）。"""
    m = re.search(re.escape(label) + r"[^0-9\-]{0,12}(" + _NUM + r")\s*万元", text)
    return float(m.group(1).replace(",", "")) if m else None


def _fmt(v):
    """数值回显成人看的样子：整数不带小数点，小数保留两位后去尾零。"""
    if abs(v - round(v)) <= 1e-9:
        return str(int(round(v)))
    return ("%.2f" % v).rstrip("0").rstrip(".")


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


DEMO = r"""# 示例材料（600000.SH）受限资产登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议
主体：示例材料（600000.SH）
报告期：2025 年年度报告·附注·所有权或使用权受到限制的资产

## 受限资产概况

- 受限资产合计〔口径：本期末〕6,600.00 万元「本集团所有权或使用权受到限制的资产账面价值合计为人民币 6,600.00 万元」〔锚：2025 年年报·第 210 页·受限资产〕[S1]
- 总资产〔口径：本期末〕206,250.00 万元「本报告期末本集团资产总额为人民币 206,250.00 万元」〔锚：2025 年年报·第 210 页·受限资产〕[S1]
- 占总资产比例〔口径：本期末〕受限金额 6,600.00 万元／资产总额 206,250.00 万元 → 3.20%「上述受限资产账面价值为人民币 6,600.00 万元，占本集团资产总额人民币 206,250.00 万元的比例为 3.20%」〔锚：2025 年年报·第 210 页·受限资产〕[S1]
- 受限类别数〔口径：本期末〕4 类「本集团受限资产分为货币资金、应收票据、存货与固定资产四类」〔锚：2025 年年报·第 210 页·受限资产〕[S1]

## 货币资金受限

- 货币资金受限〔形态：银行承兑汇票保证金〕1,200.00 万元「期末因开具银行承兑汇票而受限的保证金存款为人民币 1,200.00 万元」〔锚：2025 年年报·第 210 页·受限资产〕[S1]
- 货币资金受限〔形态：保函保证金〕300.00 万元「期末因开具保函而受限的保证金存款为人民币 300.00 万元」〔锚：2025 年年报·第 210 页·受限资产〕[S1]
- 货币资金受限〔形态：冻结存款〕200.00 万元「期末因诉讼保全被冻结的银行存款为人民币 200.00 万元」〔锚：2025 年年报·第 210 页·受限资产〕[S1]

## 非货币资产受限

- 应收票据受限〔类别：应收票据〕500.00 万元「期末已质押的应收票据账面价值为人民币 500.00 万元」〔锚：2025 年年报·第 210 页·受限资产〕[S1]
- 存货受限〔类别：存货〕1,000.00 万元「期末用于质押借款的存货账面价值为人民币 1,000.00 万元」〔锚：2025 年年报·第 210 页·受限资产〕[S1]
- 固定资产受限〔类别：房屋建筑物〕3,400.00 万元「期末用于借款抵押的房屋建筑物账面价值为人民币 3,400.00 万元」〔锚：2025 年年报·第 210 页·受限资产〕[S1]

## 受限原因与期限

- 受限原因〔对象：房屋建筑物〕借款抵押「该等房屋建筑物已抵押给银行以取得长期借款」〔锚：2025 年年报·第 210 页·受限资产〕[S1]
- 受限原因〔对象：银行承兑汇票保证金〕票据保证金「该等存款系为开具银行承兑汇票而存入的保证金」〔锚：2025 年年报·第 210 页·受限资产〕[S1]
- 受限期限〔对象：房屋建筑物〕至借款到期日「抵押期限至对应长期借款到期日止」〔锚：2025 年年报·第 210 页·受限资产〕[S1]

## 与负债的对应

- 未取到：与受限资产对应的借款金额

## 口径与未取到

- 未取到：与受限资产对应的借款金额
- 口径：受限资产的账面价值、受限形态、原因与期限一律照抄附注原文；本件不重算可动用资金、不判断资产质量与偿债能力，也不把受限金额当作可动用金额。

## 来源

- [S1] 示例材料 2025 年年度报告·附注·所有权或使用权受到限制的资产 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026-03-20
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
#     注：不能用「## 受限原因与期限（旧）」——全角括号前 `not isalnum()` 为真，_section_of 仍认得出；
#     要接一个字母数字才算认不出（「受限原因与期限旧」落空 → None → stray）。这是实测出来的形。
#     为什么不用「货币资金受限」做这一档：RA-LINE 按规格也判那一节缺失，会同时红两道。
BAD_HEADING = _must_replace(DEMO, "## 受限原因与期限\n", "## 受限原因与期限旧\n", 1)
# (c) 整节删掉「受限原因与期限」（连标题与三行）：七节不齐。
#     切法照派单：从该节标题到下一节标题之间整块切走。
_CUT_FROM, _CUT_TO = "## 受限原因与期限\n", "## 与负债的对应\n"
_i = DEMO.index(_CUT_FROM)
_j = DEMO.index(_CUT_TO)
BAD_SECTION = DEMO[:_i] + DEMO[_j:]
assert BAD_SECTION != DEMO, "删节型注入没落地"

# (d) 整节删掉「货币资金受限」：这一节是 RA-LINE 的结构判据点名的，
#     所以这一档刻意**双红**（RA-STRUCT 缺节 ＋ RA-LINE 结构判据），不追求单码。
_CUT_FROM2, _CUT_TO2 = "## 货币资金受限\n", "## 非货币资产受限\n"
_i2 = DEMO.index(_CUT_FROM2)
_j2 = DEMO.index(_CUT_TO2)
BAD_CASH_SECTION = DEMO[:_i2] + DEMO[_j2:]
assert BAD_CASH_SECTION != DEMO, "删节型注入没落地"
# 这一档的期望码集现算：RA-STRUCT 的缺节判据任何时候都发；
# RA-LINE 的结构判据只有它落字之后才会发。写死成两码会在过渡期假红，写死成一码会在落字后假绿。
EXPECT_CASH_SECTION = frozenset({"RA-STRUCT"}) | (
    frozenset({"RA-LINE"}) if "RA-LINE" not in UNIMPLEMENTED else frozenset())

# (e) 拆掉「受限资产合计」行尾的「」原句与〔锚〕，只留 [S#]：数字行三元组不齐。
#     只该红 RA-QUOTE——行仍是 `- ` 行、节没动、S1 仍被别的行引用（不致连带「未引用」）。
BAD_QUOTE = _must_replace(
    DEMO,
    "「本集团所有权或使用权受到限制的资产账面价值合计为人民币 6,600.00 万元」〔锚：2025 年年报·第 210 页·受限资产〕[S1]",
    "[S1]", 1)

# (f) 来源行检索日写成斜杠式：该行不合格式、不再算登记，正文引 S1 的行随之发「未登记」。
#     同一个 S 号只报一次，码集仍是 {RA-QUOTE}，不连带别的码。
BAD_SOURCE = _must_replace(
    DEMO,
    "所有权或使用权受到限制的资产 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026-03-20",
    "所有权或使用权受到限制的资产 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026/03/20",
    1)

# (g) 合计与分项和对不上：把「受限资产合计」改成 9,900（原 6,600），分项一律不动。
#     行首与引文同步改，三元组仍然齐——所以只该红 RA-SUM，不连带 RA-QUOTE。
#     9,900 / 206,250 = 4.80%，与「占总资产比例」那行的 3.20% 也不符——
#     但比例行判的是它自己行内的三个数，不是拿合计去推，所以 RA-RATIO 不受影响。
BAD_SUM = _must_replace(
    DEMO,
    "受限资产合计〔口径：本期末〕6,600.00 万元「本集团所有权或使用权受到限制的资产账面价值合计为人民币 6,600.00 万元」",
    "受限资产合计〔口径：本期末〕9,900.00 万元「本集团所有权或使用权受到限制的资产账面价值合计为人民币 9,900.00 万元」",
    1)

# (h) 比例重算对不上：把比例行的披露值 3.20% 改成 5.20%（分子分母不动，仍是 6,600/206,250=3.2%）。
#     行首与引文同步改（7.30% 那次栽过的坑：只改一处会让别的码先红），只该红 RA-RATIO。
BAD_RATIO = _must_replace(
    DEMO,
    "占本集团资产总额人民币 206,250.00 万元的比例为 3.20%",
    "占本集团资产总额人民币 206,250.00 万元的比例为 5.20%",
    1)
# 行首那一侧的 3.20% 也要同步改，否则行首写 3.20% 而引文写 5.20%，两支都对不上同一件事。
BAD_RATIO = _must_replace(
    BAD_RATIO,
    "受限金额 6,600.00 万元／资产总额 206,250.00 万元 → 3.20%",
    "受限金额 6,600.00 万元／资产总额 206,250.00 万元 → 5.20%",
    1)

# (i) RA-SUM 分支②：某类受限金额大于该类资产账面总额。
#     插在「受限原因与期限」**节内首行**（replace 的锚点带着节标题之后那行，才落进本节），
#     该节不参与分项求和 ⇒ 分支①不连带红；行内无比例 ⇒ 不惊动 RA-RATIO。
BAD_SUM_OVER = _must_replace(
    DEMO,
    "## 受限原因与期限\n\n- 受限原因〔对象：房屋建筑物〕",
    ("## 受限原因与期限\n"
     "\n"
     "- 存货受限〔类别：存货〕1,200.00 万元／账面总额 1,000.00 万元"
     "「期末用于质押借款的存货账面价值为人民币 1,200.00 万元，该类存货账面总额为人民币 1,000.00 万元」"
     "〔锚：2025 年年报·第 210 页·受限资产〕[S1]\n"
     "- 受限原因〔对象：房屋建筑物〕"), 1)

# (j) RA-RATIO 分支②：重算比例 > 100%（分子分母取错行）。
#     分母刻意写「总资产」（不是「资产总额」），避免同时点亮 RA-SUM 分支②，归属才干净。
BAD_RATIO_OVER = _must_replace(
    DEMO,
    "## 受限原因与期限\n\n- 受限原因〔对象：房屋建筑物〕",
    ("## 受限原因与期限\n"
     "\n"
     "- 受限比例〔口径：本期末〕受限金额 6,600.00 万元／总资产 5,000.00 万元 → 132.00%"
     "「上述受限资产占本集团总资产的比例为 132.00%」〔锚：2025 年年报·第 210 页·受限资产〕[S1]\n"
     "- 受限原因〔对象：房屋建筑物〕"), 1)

# (k)~(n) 四条红线各一支：往「受限原因与期限」节里插一条带完整三元组的行，
#     这样 RA-QUOTE 不会连带红（原句够长、S1 已登记），只钉 RA-LINE。
#     插入型：`## 与负债的对应` 留在原处，残留次数仍为 1。
BAD_LINE_QUALITY = _must_replace(
    DEMO,
    "## 与负债的对应",
    ("- 结论〔口径：本期末〕偿债能力充足「本集团资产质量好，偿债能力充足」〔锚：2025 年年报·第 210 页·受限资产〕[S1]\n"
     "\n"
     "## 与负债的对应"), 1)

BAD_LINE_LOSS = _must_replace(
    DEMO,
    "## 与负债的对应",
    ("- 受限资产〔口径：本期末〕已减值「上述受限资产已减值，预计无法收回」〔锚：2025 年年报·第 210 页·受限资产〕[S1]\n"
     "\n"
     "## 与负债的对应"), 1)

BAD_LINE_SPEND = _must_replace(
    DEMO,
    "## 与负债的对应",
    ("- 可动用资金〔口径：本期末〕8,600.00 万元「本集团可自由支配的货币资金为人民币 8,600.00 万元」〔锚：2025 年年报·第 210 页·受限资产〕[S1]\n"
     "\n"
     "## 与负债的对应"), 1)

BAD_LINE_RATING = _must_replace(
    DEMO,
    "## 与负债的对应",
    ("- 结论〔口径：本期末〕增持「我们给予公司增持评级，目标价 12.00 元」〔锚：2025 年年报·第 210 页·受限资产〕[S1]\n"
     "\n"
     "## 与负债的对应"), 1)

# (m) 反证：把「口径与未取到」那行口径说明改写成带红线词的形态——期望**零发条**。
#     口径节整节豁免：按设计它就要写「不判断资产质量与偿债能力」「不把受限金额当可动用金额」
#     这类话，不豁免会自己咬自己。这是全套里唯一期望不发码的注入档。
OK_GAP_EXEMPT = _must_replace(
    DEMO,
    "本件不重算可动用资金、不判断资产质量与偿债能力，也不把受限金额当作可动用金额。",
    "本件不重算可动用资金、不判断资产质量好坏与偿债能力是否充足，也不把受限金额当作可动用金额或实际可用额度。",
    1)


def selftest():
    """逐档现报：好样须零发条，坏样须恰发自己那道的码；未落字各算一档「不可判」。

    档数＝逐档比对的那几档 + UNIMPLEMENTED 的码数（未落字各算一档「不可判」），
    两段都从现场值算，不写死数字。五道全落字，故好样单稿现退 0；
    若哪天退回空壳，退码与档数自己跟着变，不用手改。
    """
    cases = (
        ("好样应零发条（五道全落字）", DEMO, frozenset()),
        ("形制：头部删掉「不构成投资建议」", BAD_MARK, frozenset({"RA-STRUCT"})),
        ("形制：节标题写成认不出的样子（进 stray＋缺节）", BAD_HEADING,
         frozenset({"RA-STRUCT"})),
        ("形制：整节删掉「受限原因与期限」", BAD_SECTION, frozenset({"RA-STRUCT"})),
        ("结构：整节删掉「货币资金受限」（RA-STRUCT 缺节 ＋ 落字后的 RA-LINE 结构判据，双红）",
         BAD_CASH_SECTION, EXPECT_CASH_SECTION),
        ("原句与锚：数字行拆掉「」原句与〔锚〕只留 [S#]", BAD_QUOTE,
         frozenset({"RA-QUOTE"})),
        ("原句与锚：来源行检索日写成斜杠式", BAD_SOURCE, frozenset({"RA-QUOTE"})),
        ("合计与分项：把合计改成 9,900（分项和仍 6,600）", BAD_SUM,
         frozenset({"RA-SUM"})),
        ("合计与分项②：某类受限金额 > 该类账面总额（受限 1,200／总额 1,000）", BAD_SUM_OVER,
         frozenset({"RA-SUM"})),
        ("比例重算：披露比例改成 5.20%（分子分母仍 6,600/206,250=3.2%）", BAD_RATIO,
         frozenset({"RA-RATIO"})),
        ("比例重算②：受限 6,600／总资产 5,000 → 132% > 100%", BAD_RATIO_OVER,
         frozenset({"RA-RATIO"})),
        ("红线①：插一条「偿债能力充足」的结论行", BAD_LINE_QUALITY,
         frozenset({"RA-LINE"})),
        ("红线②：插一条把受限资产说成「已减值」的行", BAD_LINE_LOSS,
         frozenset({"RA-LINE"})),
        ("红线③：插一条把受限金额写成「可自由支配」的行", BAD_LINE_SPEND,
         frozenset({"RA-LINE"})),
        ("红线④：插一条「增持／目标价」的行", BAD_LINE_RATING,
         frozenset({"RA-LINE"})),
        ("反证：「口径与未取到」节写满红线词仍应零发条（该节整节豁免）",
         OK_GAP_EXEMPT, frozenset()),
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
    # 五道各至少一支，缺哪支这里当场点名。
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
    ap = argparse.ArgumentParser(description="受限资产登记稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="受限资产登记稿 .md 路径")
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
        print("缺入参：给一份受限资产登记稿路径，或用 --demo / --selftest", file=sys.stderr)
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
