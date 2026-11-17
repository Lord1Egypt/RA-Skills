#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_revenue.py — 收入确认稿五道机检（零网络、零外发、不读环境变量）

用法：
    python3 scripts/check_revenue.py <收入稿>.md
    python3 scripts/check_revenue.py --selftest
    python3 scripts/check_revenue.py --demo     打印一份完整合规样例（零输入可跑）

道一 RR-STRUCT 形制
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]；
  `主体：` 行在场且非空；`报告期：` 行在场且非空；
  七节齐且按序：合同识别与合同组合／单项履约义务／交易价格／分摊至各履约义务／时点与时段确认／口径与未取到／来源；
  前五节各至少一条 `- ` 发现行，节内只许 `- ` 发现行、`### ` 子标题与空行。

道二 RR-QUOTE 原句与锚
  每条数字行必须以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；原句与锚不得为空；
  例外只有三形：「未取到」行（缺的就是那份材料）、[待人工] 行（判断位）与〔自算〕行（本件自己算的）；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址，检索日缺一不可；
  正文引用的每个 [S#] 必须在来源节有对应行。

道三 RR-NOSELF 不得自推自算（本件承重格）
  一、拆分只认原句：写「拆分」「单项履约义务」「不构成单项」「合并为单项」的，同一行「」原句里必须也写得到——
      拆不拆、拆几项是披露做的判断，不是本件按合同类型类推的。
  二、时点/时段只认原句：写「时点确认」「时段确认」「时段内确认」「按履约进度确认」的，原句同理；
      「设备通常验收即交付」这类推定不是原句。
  三、百分数：行内出现 `40.00%` 一类数值，必须能在同一行的「」原句里逐字找到；
      找不到的须标〔自算〕，且同一行同时给出 `分子…[S#]` 与 `分母…[S#]`。
  四、可变对价自算：同一行标了〔自算〕又谈可变对价的，必须写明**估计方法**（期望值／最可能金额）与
      **计入上限或区间**各取哪一句；缺一项即发。
  五、分摊自算：同一行标了〔自算〕又谈分摊的，必须写明**分摊基础取哪一句**（单独售价），
      并给出分子与分母各自的来源。

道四 RR-GAP 未取到两向点名
  正文（一至五节）写「未取到 X」⇒ 第六节必须点名 X；第六节点名了 X 而正文没有 ⇒ 同样发；两向都判。
  零缺口时，第六节须显式写 `未取到：无`；
  出现 `不适用`／`无此项`／`无需披露` 一律发——那是把没查当成没有。

道五 RR-LINE 红线
  造假／舞弊／虚构收入／虚增收入／提前确认／调节利润／收入确认无虞／评级与目标价／建议买入一类断言零命中；
  **只判本件自己写的句子**：同一行「」里的引文先洗掉再判——引文是证据，不是本件的断言；
  含 [待人工] 的分句豁免，且只豁免它自己那一句（按 ；;。，,｜ 切分）；
  「合同负债」与「收入」在同一分句被写成相等（＝／等于／即／相同／一致）一律发——
  合同负债是已收或应收对价而尚未履约的义务，与已确认收入不是同一个数。

退码：0 全过 / 1 有发条 / 2 用法错（缺参数） / 3 读不到文件或空稿。
"""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-revenue-recognition-cn"

CODES = ("RR-STRUCT", "RR-QUOTE", "RR-NOSELF", "RR-GAP", "RR-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("合同识别与合同组合", "单项履约义务", "交易价格", "分摊至各履约义务",
            "时点与时段确认", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"

HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")

SUBJECT = re.compile(r"^主体：\s*(\S.*)$")
PERIOD = re.compile(r"^报告期：\s*(\S.*)$")

TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
ANCHOR_REF = re.compile(r"\[(S\d+)\]")

SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)"
    r"\|\s*(?P<url>https?://\S+)\s*\|"
    r"\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$"
)

PCT = re.compile(r"\d+(?:\.\d+)?\s*[%％]")

# 金额单位换算：正文常写万元、原句常写元，同一个数要有同一个判法
UNIT_SCALE = {"元": 1.0, "万元": 1e4, "亿元": 1e8}

# 承重格的两个词族：写在本件句子里就必须在原句里也写得到
POB_WORDS = ("拆分", "单项履约义务", "不构成单项", "合并为单项")
TIMING_WORDS = ("时点确认", "时段确认", "时段内确认", "按履约进度确认")

# 可变对价自算的两项口径：估计方法 / 计入上限或区间，缺一即发
VC_METHOD = ("期望值", "最可能金额")
VC_LIMIT = ("上限", "区间", "不超过")
# 分摊自算须写明分摊基础取哪一句
SPREAD_BASE = ("单独售价",)

GAP_EXCUSE = ("不适用", "无此项", "无需披露")

EQUAL_WORDS = ("＝", "=", "等于", "即", "相同", "一致")
NEG_EQUAL = re.compile(r"(?:不|非)(?:等于|同于|一致|相同)")
CONTRACT_LIAB = ("合同负债",)
REVENUE_WORDS = ("收入",)

HARD_BAN = ("虚构收入", "虚增收入", "虚减收入", "财务造假", "造假", "舞弊",
            "提前确认收入", "跨期确认", "调节利润", "利润调节", "盈余管理", "洗大澡",
            "确认无虞", "确认无误", "无风险",
            "目标价", "目标市值", "买入评级", "增持评级", "中性评级",
            "建议买入", "建议增持", "强烈推荐", "跑赢大盘", "必涨", "必跌")

PRED_WORDS = ("收入将增长", "收入将下滑", "预计收入增长", "预计收入下滑",
              "将实现收入", "预计实现收入", "将保持增长", "预计增长")

CLAUSE_SPLIT = re.compile(r"[；;。，,｜|]")

SCOPE_RULES = (
    (("存货跌价准备", "应收账款账龄", "合同资产减值", "账龄分析表"),
     "改走 cn-working-capital-quality：存货、应收账款与合同资产的余额与账龄是那一件"),
    (("经营活动现金流", "筹资活动现金流", "净现比", "收现比", "自由现金流"),
     "改走 cn-cash-flow-quality：三张现金流的逐条登记是那一件，本件只在收现口径处给一句指向"),
    (("合同违约责任条款", "不可抗力条款", "保密条款审查"),
     "改走 cn-contract-clauses：合同条款本身的审查是那一件，本件只登记会计层面的确认口径"),
    (("四期差异点评", "科目勾稽点评"),
     "改走 cn-earnings-note：财报四期差异与科目勾稽的点评是那一件"),
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
      正文 `- 项名 未取到：原因`      → 项名在「未取到」**前**
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


def _equal_hit(clause):
    """分句里有没有把合同负债与收入写成相等的连接词（否定形不算：「不等于」不是相等）。"""
    c = NEG_EQUAL.sub("", clause)
    return [w for w in EQUAL_WORDS if w in c]


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
    # 逐句洗就洗不干净——「公司否认存在虚构收入，未发生舞弊」这类照抄原文会被误判成本件断言。
    own_line = _strip_quotes(line)
    for clause in _clauses(own_line):
        if "[待人工]" in clause:
            continue
        own = clause
        hit = [w for w in HARD_BAN if w in own]
        pred = [w for w in PRED_WORDS if w in own]
        if pred:
            hit.extend(pred)
        # 合同负债 ≠ 已确认收入
        if (any(w in own for w in CONTRACT_LIAB)
                and any(w in own for w in REVENUE_WORDS)
                and _equal_hit(own)):
            hit.append("合同负债＝收入")
        if hit:
            add("RR-LINE", lineno, "红线词：%s（%s）" % ("、".join(sorted(set(hit))), clause.strip()[:40]))
            return


def _amounts(text):
    """把一段文字里的金额按单位换成元，便于跨「万元／元」比对同一个数。"""
    out = set()
    for m in re.finditer(r"(\d[\d,]*(?:\.\d+)?)\s*(亿元|万元|元)", text):
        try:
            v = float(m.group(1).replace(",", "")) * UNIT_SCALE[m.group(2)]
        except ValueError:
            continue
        out.add(round(v, 2))
    return out


def _num_in_quote(value, unit, quote_amounts, quote_text):
    """正文写的数值是否落在原句里（百分数按字面，金额按换算后的元）。"""
    v = value.replace(",", "")
    if unit in ("%", "％"):
        return (v + "%") in quote_text.replace(" ", "").replace("％", "%")
    try:
        want = round(float(v) * UNIT_SCALE.get(unit, 1.0), 2)
    except ValueError:
        return False
    return want in quote_amounts


def _quotes(line):
    return "".join(m.group(1) for m in QUOTE.finditer(line))


def _check_vocab(lineno, line, add, words, what):
    """词族只认原句：本件句子里写了，同一行原句也必须写到。

    判域＝去掉**项名**之后的余下部分。项名本身就是「履约义务·设备销售」这种写法，
    它是在标这一行的登记对象，不是在替披露拆分；把它当自推判会冤枉正确写法。
    「未取到」行整行豁免——那正是「原句没写所以照实写未取到」的正确形态。
    """
    if "未取到" in line:
        return
    body = line
    m = re.match(r"^-\s*([^「：:]*)[：:]\s*(.*)$", line)
    if m:
        body = m.group(2)
    q = _quotes(line)
    outside = [w for w in words if w in body and w not in q]
    if outside:
        add("RR-NOSELF", lineno,
            "%s须取原句：本件句子里写了「%s」，原句里没有——没披露就写未取到，不按惯例自推：%s"
            % (what, "、".join(outside), line.strip()[:40]))


def _check_mol_den(lineno, line, add, what):
    mol = re.search(r"分子[^｜|〕」；。]*\[S\d+\]", line)
    den = re.search(r"分母[^｜|〕」；。]*\[S\d+\]", line)
    why = []
    if not mol:
        why.append("缺分子来源")
    if not den:
        why.append("缺分母来源")
    if why:
        add("RR-NOSELF", lineno, "%s自算未交代%s" % (what, "／".join(why)))


def _check_vc(lineno, line, add):
    """可变对价自算：估计方法与计入上限／区间两项口径缺一即发。"""
    why = []
    if not any(w in line for w in VC_METHOD):
        why.append("未写明估计方法取哪一句（期望值／最可能金额）")
    if not any(w in line for w in VC_LIMIT):
        why.append("未写明计入上限或区间取哪一句")
    if why:
        add("RR-NOSELF", lineno, "可变对价自算未交代%s" % "／".join(why))


def _check_noself(lineno, line, add):
    q = _quotes(line).replace(" ", "")
    # 一、二、词族：拆分与时点／时段只认原句
    _check_vocab(lineno, line, add, POB_WORDS, "履约义务拆分")
    _check_vocab(lineno, line, add, TIMING_WORDS, "时点或时段判断")
    # 三、百分数：原句里没有同一数值，就必须自算并交代分子分母
    missing = [t for t in PCT.findall(line) if _norm_pct(t) not in q]
    if missing:
        if "〔自算〕" not in line:
            add("RR-NOSELF", lineno, "比例 %s 在原句里找不到，也没标〔自算〕：%s"
                % ("、".join(missing), line.strip()[:40]))
        else:
            _check_mol_den(lineno, line, add, "比例")
    # 四、可变对价自算的两项口径
    if "〔自算〕" in line and "可变对价" in line:
        _check_vc(lineno, line, add)
    # 五、分摊自算须写明分摊基础
    if "〔自算〕" in line and "分摊" in line:
        if not any(w in line for w in SPREAD_BASE):
            add("RR-NOSELF", lineno,
                "分摊自算未写明分摊基础取哪一句（单独售价）：%s" % line.strip()[:40])
        else:
            _check_mol_den(lineno, line, add, "分摊")


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
            add("RR-STRUCT", 1, "头部缺自标「%s」" % mark)
    if not any(SUBJECT.match(s) for _i, s in header):
        add("RR-STRUCT", 1, "头部缺 `主体：` 行")
    if not any(PERIOD.match(s) for _i, s in header):
        add("RR-STRUCT", 1, "头部缺 `报告期：` 行")

    # ---- 道一 节齐与序
    names = [n for n, _l, _b in sections]
    for name in SECTIONS:
        if name not in names:
            add("RR-STRUCT", 1, "缺节「%s」" % name)
    pos = [SECTIONS.index(n) for n in names]
    if pos != sorted(pos):
        add("RR-STRUCT", 1, "节序不对：现序 %s，应序 %s" % ("／".join(names), "／".join(SECTIONS)))
    for lineno, raw in stray:
        add("RR-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw)

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
                    add("RR-STRUCT", lineno, "节内只许 `- ` 发现行：%s" % s.strip()[:40])
                    continue
                n_find += 1
                stats["finding_lines"] += 1
                referenced.extend(ANCHOR_REF.findall(s))
                if "未取到" in s:
                    body_gaps.append((lineno, s))
                if not TRIPLE.search(s):
                    if "未取到" in s or "[待人工]" in s or "〔自算〕" in s:
                        pass
                    else:
                        add("RR-QUOTE", lineno, "发现行缺「」原句 + 〔锚：…〕 + [S#] 三元组：%s"
                            % s.strip()[:40])
                else:
                    for m in TRIPLE.finditer(s):
                        if not m.group("q").strip():
                            add("RR-QUOTE", lineno, "原句为空")
                        if not m.group("a").strip():
                            add("RR-QUOTE", lineno, "锚为空")
                    if not re.search(r"\[S\d+\]\s*$", s.strip()):
                        add("RR-QUOTE", lineno, "发现行未以 [S#] 收尾（三元组须在行末）")
                _check_line(lineno, s, add)
                if PCT.findall(s):
                    stats["ratio_lines"] += 1
                _check_noself(lineno, s, add)
            section_found[name] = n_find
            if n_find == 0:
                add("RR-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name)

        elif name == GAP_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not _is_finding_line(s):
                    add("RR-STRUCT", lineno, "第六节只许 `- ` 行：%s" % s.strip()[:40])
                    continue
                section_found.setdefault(name, 0)
                section_found[name] += 1
                for w in GAP_EXCUSE:
                    if w in s:
                        add("RR-GAP", lineno, "禁用「%s」把没查当成没有：%s" % (w, s.strip()[:40]))
                _check_line(lineno, s, add)

        elif name == SOURCE_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not s.lstrip().startswith("- ["):
                    add("RR-STRUCT", lineno, "来源节只许 `- [S#] …` 行：%s" % s.strip()[:40])
                    continue
                m = SOURCE_LINE.match(s.strip())
                if not m:
                    add("RR-QUOTE", lineno, "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:50])
                    continue
                stats["sources"] += 1

    # ---- 道四 未取到两向点名
    gap_body = [s for _ln, s in body_gaps]
    gap_sec = []
    for name, _h, body in sections:
        if name != GAP_SECTION:
            continue
        for _ln, s in body:
            if "未取到" in s and "未取到：无" not in s and "未取到:无" not in s:
                gap_sec.append(s)
    for s in gap_body:
        if "未取到：无" in s:
            continue
        key = _gap_key(s)
        if key and not any(key in g for g in gap_sec):
            add("RR-GAP", 1, "正文写了未取到「%s」，第六节没点名" % key)
    for g in gap_sec:
        key = _gap_key(g)
        if key and not any(key in s for s in gap_body):
            add("RR-GAP", 1, "第六节点名了「%s」，正文没有这条表述" % key)

    # 零缺口须显式写「未取到：无」
    if not gap_body and not gap_sec:
        gap_text = "\n".join(s for name, _h, body in sections if name == GAP_SECTION
                             for _ln, s in body)
        if "未取到：无" not in gap_text and "未取到:无" not in gap_text:
            add("RR-GAP", 1, "零缺口未显式写「未取到：无」")

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
            add("RR-QUOTE", 1, "正文引用 [%s]，来源节没有对应登记行" % ref)

    # ---- 边界
    # 只判前五节（登记正文）。第六节「口径与未取到」正是写明与另几枚件分界的地方，
    # 在那里点名 cn-cash-flow-quality／cn-working-capital-quality 是本件要求的动作，不是越界。
    body_lines = [(ln, s) for name, _h, body in sections
                  if name in CONTENT_SECTIONS for ln, s in body]
    for words, tip in SCOPE_RULES:
        for ln, s in body_lines:
            if any(w in s for w in words):
                add("RR-STRUCT", ln, "越界：%s" % tip)
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


GOOD = r"""# 示例材料（600000.SH）收入确认登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议 ｜ 判断位 [待人工]
主体：示例材料（600000.SH）
报告期：2025 年年度报告

## 合同识别与合同组合

- 合同识别 已订立并具有商业实质「本集团在客户取得商品控制权时，该合同具有商业实质且对价很可能收回」〔锚：2025 年年报·第 88 页·附注三·收入〕[S1]
- 合同组合 按组合方式处理「对具有类似特征的合同，本集团采用组合方式确认收入」〔锚：2025 年年报·第 88 页·附注三·收入〕[S1]
- 合同期限 18 个月「本集团与客户订立的设备销售合同期限为 18 个月」〔锚：2025 年年报·第 88 页·附注三·收入〕[S1]
- 合同变更 未取到：附注未披露本期合同变更情形

## 单项履约义务

- 履约义务·设备销售 单项履约义务「设备销售构成单项履约义务」〔锚：2025 年年报·第 89 页·附注三·收入〕[S1]
- 履约义务·安装服务 单项履约义务「安装服务构成单项履约义务」〔锚：2025 年年报·第 89 页·附注三·收入〕[S1]
- 拆分结论 拆分 2 项「本集团将合同拆分为设备销售与安装服务两项履约义务」〔锚：2025 年年报·第 89 页·附注三·收入〕[S1]
- 不可明确区分的商品 未取到：附注未列示不可明确区分的商品与服务

## 交易价格

- 交易价格 12,000.00 万元「合同交易价格为 120,000,000.00 元」〔锚：2025 年年报·第 90 页·附注三·收入〕[S1]
- 可变对价 600.00 万元「合同约定按验收合格率浮动，可变对价估计为 6,000,000.00 元」〔锚：2025 年年报·第 90 页·附注三·收入〕[S1]
- 可变对价计入上限 600.00 万元「计入交易价格的可变对价金额不超过 6,000,000.00 元」〔锚：2025 年年报·第 90 页·附注三·收入〕[S1]
- 重大融资成分 未取到：附注未披露重大融资成分
- 非现金对价 0.00 万元「本期不存在非现金对价」〔锚：2025 年年报·第 90 页·附注三·收入〕[S1]
- 应付客户对价 120.00 万元「应付客户对价 1,200,000.00 元，冲减交易价格」〔锚：2025 年年报·第 90 页·附注三·收入〕[S1]

## 分摊至各履约义务

- 分摊·设备销售 9,000.00 万元「设备销售分摊交易价格 90,000,000.00 元」〔锚：2025 年年报·第 91 页·附注三·收入〕[S1]
- 分摊·安装服务 3,000.00 万元「安装服务分摊交易价格 30,000,000.00 元」〔锚：2025 年年报·第 91 页·附注三·收入〕[S1]
- 分摊基础 按单独售价相对比例「本集团按各单项履约义务单独售价的相对比例分摊交易价格」〔锚：2025 年年报·第 91 页·附注三·收入〕[S1]
- 设备销售占比 75.00%〔自算〕分子＝设备销售单独售价 90,000,000.00 元 [S1]｜分母＝各履约义务单独售价合计 120,000,000.00 元 [S1]

## 时点与时段确认

- 设备销售 时点确认「本集团在客户取得相关商品控制权时点确认收入」〔锚：2025 年年报·第 92 页·附注三·收入〕[S1]
- 安装服务 按履约进度确认「安装服务属于在某一时段内履行的履约义务，本集团按履约进度确认收入」〔锚：2025 年年报·第 92 页·附注三·收入〕[S1]
- 履约进度确定方法 投入法「本集团采用投入法确定履约进度」〔锚：2025 年年报·第 92 页·附注三·收入〕[S1]
- 本期安装进度 40.00%〔自算〕分子＝累计已发生成本 4,000,000.00 元 [S1]｜分母＝预计总成本 10,000,000.00 元 [S1]
- 时段确认的计量基础 未取到：附注未列示产出法下的计量单位

## 口径与未取到

- 未取到：合同变更
- 未取到：不可明确区分的商品
- 未取到：重大融资成分
- 未取到：时段确认的计量基础
- 口径：拆不拆、时点还是时段，一律照抄附注原句，不由本件按行业惯例推断。
- 口径：分摊比例与履约进度自算的，分子分母各挂各的来源。
- 口径：合同负债是已收对价而尚未履约的义务，与已确认收入不是同一个数，两者不得互相印证；收现口径见 cn-cash-flow-quality。
- 口径：应收账款与合同资产的余额与账龄见 cn-working-capital-quality，本件不碰。
- 口径：合同条款审查见 cn-contract-clauses，本件只登记会计层面的确认口径。

## 来源

- [S1] 示例材料 2025 年年度报告·附注三·收入 | https://example.com/ann/S1 | 检索日 2026-11-13 | 类型：公告
- [S2] 示例材料 2025 年年度报告·附注三·收入（续） | https://example.com/ann/S2 | 检索日 2026-11-13 | 类型：公告
"""

# ---- 坏样：各只发自己那道码
# 形制坏样插的是**多出一节同名标题**，不是改节点名：改名会让整节变 stray、节内发现行一并丢，
# 连带「重大融资成分 未取到」那条正文也没了，第六节就多出一条假 RR-GAP——测出来的红分不清是哪道判的。
BAD_STRUCT = GOOD.replace(
    "## 时点与时段确认",
    "## 分摊至各履约义务\n\n## 时点与时段确认")

BAD_QUOTE = GOOD.replace(
    "「设备销售分摊交易价格 90,000,000.00 元」〔锚：2025 年年报·第 91 页·附注三·收入〕[S1]",
    "90,000,000.00 元 [S1]")

BAD_NOSELF = GOOD.replace(
    "分子＝设备销售单独售价 90,000,000.00 元 [S1]｜分母＝各履约义务单独售价合计 120,000,000.00 元 [S1]",
    "分子＝设备销售单独售价 90,000,000.00 元 [S1]")

BAD_GAP = GOOD.replace(
    "- 未取到：合同变更",
    "- 未取到：不适用")

BAD_LINE = GOOD.replace(
    "- 履约进度确定方法 投入法",
    "- 收入确认无虞，目标价 15 元；履约进度确定方法 投入法")

# ---- 反证样：不该发的必须不发
OK_HUMAN = GOOD.replace(
    "- 未取到：合同变更",
    "- 未取到：合同变更\n- 收入是否真实、有无虚构，交由人工判断 [待人工]")

BAD_HUMAN_HALF = GOOD.replace(
    "- 未取到：合同变更",
    "- 未取到：合同变更\n- 收入是否真实 [待人工]，建议买入")

# 引文反证样换的是「合同组合」那一行的引文，不动任何「未取到」行——
# 动未取到行会同时删掉正文点名，第六节立刻多一条 RR-GAP，测出来的红就不是红线那道了。
OK_QUOTED_REDLINE = GOOD.replace(
    "「对具有类似特征的合同，本集团采用组合方式确认收入」",
    "「公司否认存在虚构收入，未发生舞弊」")

BAD_LIAB_EQUALS_REV = GOOD.replace(
    "- 口径：合同负债是已收对价而尚未履约的义务，与已确认收入不是同一个数，两者不得互相印证；收现口径见 cn-cash-flow-quality。",
    "- 口径：合同负债即已确认收入，两者互相印证。")

OK_VC_DECLARED = GOOD.replace(
    "- 可变对价 600.00 万元「合同约定按验收合格率浮动，可变对价估计为 6,000,000.00 元」〔锚：2025 年年报·第 90 页·附注三·收入〕[S1]",
    "- 可变对价 600.00 万元〔自算〕按合同条款分档测算，估计方法取附注「按期望值确定」〔锚：2025 年年报·第 90 页·附注三·收入〕[S1]｜计入上限取附注「不超过 6,000,000.00 元」[S1]")

BAD_VC_NOLIMIT = GOOD.replace(
    "- 可变对价 600.00 万元「合同约定按验收合格率浮动，可变对价估计为 6,000,000.00 元」〔锚：2025 年年报·第 90 页·附注三·收入〕[S1]",
    "- 可变对价 600.00 万元〔自算〕按合同条款分档测算，估计方法取附注「按期望值确定」〔锚：2025 年年报·第 90 页·附注三·收入〕[S1]")

BAD_TIMING_GUESS = GOOD.replace(
    "- 设备销售 时点确认「本集团在客户取得相关商品控制权时点确认收入」〔锚：2025 年年报·第 92 页·附注三·收入〕[S1]",
    "- 设备销售 时段确认「设备销售于合同签订后交付并验收」〔锚：2025 年年报·第 92 页·附注三·收入〕[S1]")

# 零输入样例：直接由 GOOD 派生，不另抄一份——两份会各自漂移，
# 而用户看到的「成品长什么样」必须永远等于自测里那个「好样」。
DEMO = GOOD


def _codes(text):
    findings, _stats = check_text(text)
    return findings, set(c for c, _l, _m in findings)


def selftest():
    cases = (
        ("好样应零发条", GOOD, set()),
        ("形制：节标题写错（交易定价）", BAD_STRUCT, {"RR-STRUCT"}),
        ("锚：数字行没挂原句与锚", BAD_QUOTE, {"RR-QUOTE"}),
        ("自算：分摊比例自算只给分子没给分母", BAD_NOSELF, {"RR-NOSELF"}),
        ("点名：第六节用「不适用」搪塞", BAD_GAP, {"RR-GAP"}),
        ("红线：写收入确认无虞、目标价", BAD_LINE, {"RR-LINE"}),
        ("反证：[待人工] 整句成立 → 不发", OK_HUMAN, set()),
        ("反证：[待人工] 只豁免自己那句，后半句建议买入照样发", BAD_HUMAN_HALF, {"RR-LINE"}),
        ("反证：引文里的「虚构收入」不是本件断言 → 不发", OK_QUOTED_REDLINE, set()),
        ("红线：合同负债即已确认收入", BAD_LIAB_EQUALS_REV, {"RR-LINE"}),
        ("反证：可变对价自算写全方法与上限 → 不发", OK_VC_DECLARED, set()),
        ("自算：可变对价自算缺计入上限", BAD_VC_NOLIMIT, {"RR-NOSELF"}),
        ("自推：原句没写时点时段却自标时段确认", BAD_TIMING_GUESS, {"RR-NOSELF"}),
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
    ap = argparse.ArgumentParser(description="收入确认稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="收入稿 .md 路径")
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
        print("缺入参：给一份收入稿路径，或用 --demo / --selftest", file=sys.stderr)
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
