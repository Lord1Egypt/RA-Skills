#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_correction.py — 前期会计差错更正稿五道机检（零网络、零外发、不读环境变量）

用法：
    python3 scripts/check_correction.py <更正稿>.md
    python3 scripts/check_correction.py --selftest
    python3 scripts/check_correction.py --demo     打印一份完整合规样例（零输入可跑）

道一 EC-STRUCT 形制
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]；
  `主体：` 行在场且非空；`报告期：` 行在场且非空；
  七节齐且按序：差错的性质与发现时点／更正方法与判据／受影响的报表科目与各期重述金额／
  对期初未分配利润与比较报表的影响／与政策变更、估计变更的界线／口径与未取到／来源；
  前五节各至少一条 `- ` 发现行，节内只许 `- ` 发现行、`### ` 子标题与空行。

道二 EC-QUOTE 原句与锚
  每条数字行必须以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；原句与锚不得为空；
  例外只有三形：「未取到」行（缺的就是那份材料）、[待人工] 行（判断位）与〔自算〕行（本件自己算的）；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址，检索日缺一不可；
  正文引用的每个 [S#] 必须在来源节有对应行。

道三 EC-NOSELF 不得自推自算（本件承重格）
  一、差错性质只认原句：写「前期差错」「会计差错」「重大差错」「差错更正」的，同一行「」原句里必须也写得到——
      一项错报到底是差错、是政策变更还是估计变更，是披露做的判断，不是本件按金额大小或科目类型推的。
  二、更正方法只认原句：写「追溯重述」「追溯调整」「未来适用」的，原句同理；
      「金额重大所以理应追溯重述」这类推定不是原句。
  三、三类界线只认原句：写「会计政策变更」「会计估计变更」的，原句同理——披露里这三者常混写，
      界线必须由披露自己划，本件不替它划。
  四、百分数：行内出现 `40.00%` 一类数值，必须能在同一行的「」原句里逐字找到；
      找不到的须标〔自算〕，且同一行同时给出 `分子…[S#]` 与 `分母…[S#]`。
  五、重述金额自算：同一行标了〔自算〕又谈重述／累积影响／期初未分配利润／比较报表的，
      必须写明**累积影响或期初余额取哪一句**，并给出分子与分母各自的来源；缺一项即发。

道四 EC-GAP 未取到两向点名
  正文（一至五节）写「未取到 X」⇒ 第六节必须点名 X；第六节点名了 X 而正文没有 ⇒ 同样发；两向都判。
  零缺口时，第六节须显式写 `未取到：无`；
  出现 `不适用`／`无此项`／`无需披露` 一律发——那是把没查当成没有。

道五 EC-LINE 红线
  造假／舞弊／管理层故意／粉饰／虚构／虚增／利润调节／更正后报表可信／退市风险／股价影响／评级与目标价
  一类断言零命中；
  **只判本件自己写的句子**：同一行「」里的引文先洗掉再判——引文是证据，不是本件的断言；
  含 [待人工] 的分句豁免，且只豁免它自己那一句（按 ；;。，,｜ 切分）；
  「会计政策变更／会计估计变更」与「前期差错」在同一分句被写成相等（＝／等于／视为／视同）一律发——
  三者是不同的东西，写成同一个就是替披露抹掉了界线。

退码：0 全过 / 1 有发条 / 2 用法错（缺参数） / 3 读不到文件或空稿。
"""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-accounting-error-correction-cn"

CODES = ("EC-STRUCT", "EC-QUOTE", "EC-NOSELF", "EC-GAP", "EC-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("差错的性质与发现时点", "更正方法与判据", "受影响的报表科目与各期重述金额",
            "对期初未分配利润与比较报表的影响", "与政策变更、估计变更的界线",
            "口径与未取到", "来源")
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

# 承重格的三个词族：写在本件句子里就必须在原句里也写得到
ERROR_WORDS = ("前期差错", "会计差错", "重大差错", "差错更正")
METHOD_WORDS = ("追溯重述", "追溯调整", "未来适用")
CHANGE_WORDS = ("会计政策变更", "会计估计变更", "政策变更", "估计变更")

# 重述金额自算：须写明累积影响或期初余额取哪一句
RESTATE_BASIS = ("累积影响", "期初余额")
RESTATE_WORDS = ("重述", "累积影响", "期初未分配利润", "比较报表")

GAP_EXCUSE = ("不适用", "无此项", "无需披露")

EQUAL_WORDS = ("＝", "=", "等于", "相同", "一致", "视为", "视同")
NEG_EQUAL = re.compile(r"(?:不|非)(?:等于|同于|一致|相同|视为|视同)")

HARD_BAN = ("财务造假", "造假", "舞弊", "管理层故意", "故意隐瞒", "人为调节", "利润调节",
            "盈余管理", "洗大澡", "粉饰",
            "虚构", "虚增", "虚减",
            "更正后报表可信", "报表可信", "更正无虞", "更正无误", "不存在重大错报", "无风险",
            "目标价", "目标市值", "买入评级", "增持评级", "中性评级",
            "建议买入", "建议增持", "强烈推荐", "跑赢大盘", "必涨", "必跌",
            "退市风险", "面临退市", "将被退市", "影响股价", "股价将", "预计股价")

CLAUSE_SPLIT = re.compile(r"[；;。，,｜|]")

SCOPE_RULES = (
    (("四期差异点评", "科目勾稽点评"),
     "改走 cn-earnings-note：财报四期差异与科目勾稽的点评是那一件，本件只登记更正本身"),
    (("五步法", "单项履约义务", "可变对价"),
     "改走 cn-revenue-recognition-cn：收入确认五步法是那一件，本件只登记差错更正"),
    (("经营活动现金流", "净现比", "收现比", "自由现金流"),
     "改走 cn-cash-flow-quality：三张现金流的逐条登记是那一件"),
    (("审计意见类型", "保留意见", "无法表示意见", "否定意见"),
     "改走 cn-audit-opinion-cn：审计意见类型的判定是那一件，本件只登记差错本身"),
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
    """分句里有没有把三类变更写成相等的连接词（否定形不算：「不属于」不是相等）。"""
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
    # 逐句洗就洗不干净——「公司否认存在舞弊，未发生人为调节」这类照抄原文会被误判成本件断言。
    own_line = _strip_quotes(line)
    for clause in _clauses(own_line):
        if "[待人工]" in clause:
            continue
        own = clause
        hit = [w for w in HARD_BAN if w in own]
        # 三类变更 ≠ 前期差错：同句出现两类词又被写成相等，就是替披露抹掉界线
        if (any(w in own for w in CHANGE_WORDS)
                and any(w in own for w in ERROR_WORDS)
                and _equal_hit(own)):
            hit.append("政策／估计变更＝前期差错")
        if hit:
            add("EC-LINE", lineno, "红线词：%s（%s）" % ("、".join(sorted(set(hit))), clause.strip()[:40]))
            return


def _quotes(line):
    return "".join(m.group(1) for m in QUOTE.finditer(line))


def _check_vocab(lineno, line, add, words, what):
    """词族只认原句：本件句子里写了，同一行原句也必须写到。

    判域＝去掉**项名**与**锚标签**之后的余下部分。两处都是标签、不是断言：
    项名是「更正方法·追溯重述法」这种登记对象，锚标签是「〔锚：…附注二·前期差错更正〕」
    这种定位指针——把它们算进自推会冤枉正确写法。
    「未取到」行整行豁免——那正是「原句没写所以照实写未取到」的正确形态。
    """
    if "未取到" in line:
        return
    body = line
    m = re.match(r"^-\s*([^「：:]*)[：:]\s*(.*)$", line)
    if m:
        body = m.group(2)
    body = ANCHOR_BLOCK.sub("", body)       # 锚是定位指针，不是本件在判断
    q = _quotes(line)
    outside = [w for w in words if w in body and w not in q]
    if outside:
        add("EC-NOSELF", lineno,
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
        add("EC-NOSELF", lineno, "%s自算未交代%s" % (what, "／".join(why)))


def _check_restate(lineno, line, add):
    """重述金额自算：累积影响／期初余额取哪一句 + 分子分母各挂各的源。"""
    why = []
    if not any(w in line for w in RESTATE_BASIS):
        why.append("未写明累积影响或期初余额取哪一句")
    if why:
        add("EC-NOSELF", lineno, "重述金额自算未交代%s" % "／".join(why))
    _check_mol_den(lineno, line, add, "重述金额")


def _check_noself(lineno, line, add):
    q = _quotes(line).replace(" ", "")
    # 一、二、三、词族：差错性质、更正方法、三类界线只认原句
    _check_vocab(lineno, line, add, ERROR_WORDS, "差错性质判断")
    _check_vocab(lineno, line, add, METHOD_WORDS, "更正方法判断")
    _check_vocab(lineno, line, add, CHANGE_WORDS, "三类变更界线")
    # 四、百分数：原句里没有同一数值，就必须自算并交代分子分母
    missing = [t for t in PCT.findall(line) if _norm_pct(t) not in q]
    if missing:
        if "〔自算〕" not in line:
            add("EC-NOSELF", lineno, "比例 %s 在原句里找不到，也没标〔自算〕：%s"
                % ("、".join(missing), line.strip()[:40]))
        else:
            _check_mol_den(lineno, line, add, "比例")
    # 五、重述金额自算的两项口径
    if "〔自算〕" in line and any(w in line for w in RESTATE_WORDS):
        _check_restate(lineno, line, add)


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
            add("EC-STRUCT", 1, "头部缺自标「%s」" % mark)
    if not any(SUBJECT.match(s) for _i, s in header):
        add("EC-STRUCT", 1, "头部缺 `主体：` 行")
    if not any(PERIOD.match(s) for _i, s in header):
        add("EC-STRUCT", 1, "头部缺 `报告期：` 行")

    # ---- 道一 节齐与序
    names = [n for n, _l, _b in sections]
    for name in SECTIONS:
        if name not in names:
            add("EC-STRUCT", 1, "缺节「%s」" % name)
    pos = [SECTIONS.index(n) for n in names]
    if pos != sorted(pos):
        add("EC-STRUCT", 1, "节序不对：现序 %s，应序 %s" % ("／".join(names), "／".join(SECTIONS)))
    for lineno, raw in stray:
        add("EC-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw)

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
                    add("EC-STRUCT", lineno, "节内只许 `- ` 发现行：%s" % s.strip()[:40])
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
                        add("EC-QUOTE", lineno, "发现行缺「」原句 + 〔锚：…〕 + [S#] 三元组：%s"
                            % s.strip()[:40])
                else:
                    for m in TRIPLE.finditer(s):
                        if not m.group("q").strip():
                            add("EC-QUOTE", lineno, "原句为空")
                        if not m.group("a").strip():
                            add("EC-QUOTE", lineno, "锚为空")
                    if not re.search(r"\[S\d+\]\s*$", s.strip()):
                        add("EC-QUOTE", lineno, "发现行未以 [S#] 收尾（三元组须在行末）")
                _check_line(lineno, s, add)
                if PCT.findall(s):
                    stats["ratio_lines"] += 1
                _check_noself(lineno, s, add)
            section_found[name] = n_find
            if n_find == 0:
                add("EC-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name)

        elif name == GAP_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not _is_finding_line(s):
                    add("EC-STRUCT", lineno, "第六节只许 `- ` 行：%s" % s.strip()[:40])
                    continue
                section_found.setdefault(name, 0)
                section_found[name] += 1
                for w in GAP_EXCUSE:
                    if w in s:
                        add("EC-GAP", lineno, "禁用「%s」把没查当成没有：%s" % (w, s.strip()[:40]))
                _check_line(lineno, s, add)

        elif name == SOURCE_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not s.lstrip().startswith("- ["):
                    add("EC-STRUCT", lineno, "来源节只许 `- [S#] …` 行：%s" % s.strip()[:40])
                    continue
                m = SOURCE_LINE.match(s.strip())
                if not m:
                    add("EC-QUOTE", lineno, "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:50])
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
            add("EC-GAP", 1, "正文写了未取到「%s」，第六节没点名" % key)
    for g in gap_sec:
        key = _gap_key(g)
        if key and not any(key in s for s in gap_body):
            add("EC-GAP", 1, "第六节点名了「%s」，正文没有这条表述" % key)

    # 零缺口须显式写「未取到：无」
    if not gap_body and not gap_sec:
        gap_text = "\n".join(s for name, _h, body in sections if name == GAP_SECTION
                             for _ln, s in body)
        if "未取到：无" not in gap_text and "未取到:无" not in gap_text:
            add("EC-GAP", 1, "零缺口未显式写「未取到：无」")

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
            add("EC-QUOTE", 1, "正文引用 [%s]，来源节没有对应登记行" % ref)

    # ---- 边界
    # 只判前五节（登记正文）。第六节「口径与未取到」正是写明与另几枚件分界的地方，
    # 在那里点名 cn-earnings-note／cn-cash-flow-quality 是本件要求的动作，不是越界。
    body_lines = [(ln, s) for name, _h, body in sections
                  if name in CONTENT_SECTIONS for ln, s in body]
    for words, tip in SCOPE_RULES:
        for ln, s in body_lines:
            if any(w in s for w in words):
                add("EC-STRUCT", ln, "越界：%s" % tip)
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


GOOD = r"""# 示例材料（600000.SH）前期会计差错更正登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议 ｜ 判断位 [待人工]
主体：示例材料（600000.SH）
报告期：2025 年年度报告（含 2024 年度重述数）

## 差错的性质与发现时点

- 差错性质 前期差错「本公司在 2024 年度对某项目收入确认时点判断有误，构成前期差错」〔锚：2025 年年报·第 120 页·附注二·前期差错更正〕[S1]
- 重大性判断 重大前期差错「该差错影响金额较大，属于重大前期差错」〔锚：2025 年年报·第 120 页·附注二·前期差错更正〕[S1]
- 发现时点 2024 年度审计过程中发现「本公司于 2024 年度财务报表审计过程中发现上述差错」〔锚：差错更正公告·第 2 页·一、差错概述〕[S2]
- 发现时点的判断依据 未取到：附注未说明发现时点的判断依据

## 更正方法与判据

- 更正方法 追溯重述法「本公司采用追溯重述法对该项前期差错进行更正」〔锚：2025 年年报·第 120 页·附注二·前期差错更正〕[S1]
- 更正方法判据 重要性「根据《企业会计准则第 28 号》，重大前期差错采用追溯重述法」〔锚：2025 年年报·第 120 页·附注二·前期差错更正〕[S1]
- 累积影响数 320.00 万元「上述差错累积影响数为 3,200,000.00 元，调减期初未分配利润」〔锚：2025 年年报·第 120 页·附注二·前期差错更正〕[S1]
- 是否适用未来适用法 不适用「本次更正不涉及未来适用法」〔锚：差错更正公告·第 3 页·二、更正方法〕[S2]

## 受影响的报表科目与各期重述金额

- 营业收入·2024 年度 调减 1,200.00 万元「调减 2024 年度营业收入 12,000,000.00 元」〔锚：2025 年年报·第 121 页·附注二·前期差错更正〕[S1]
- 营业成本·2024 年度 调减 800.00 万元「调减 2024 年度营业成本 8,000,000.00 元」〔锚：2025 年年报·第 121 页·附注二·前期差错更正〕[S1]
- 应收账款·2024 年末 调减 400.00 万元「调减 2024 年 12 月 31 日应收账款 4,000,000.00 元」〔锚：2025 年年报·第 121 页·附注二·前期差错更正〕[S1]
- 重述金额较原披露数变动 3.00%〔自算〕累积影响取附注「上述差错累积影响数为 3,200,000.00 元」〔锚：2025 年年报·第 120 页·附注二·前期差错更正〕[S1]｜分子＝2024 年度营业收入调减 12,000,000.00 元 [S1]｜分母＝2024 年度原披露营业收入 400,000,000.00 元 [S1]
- 每股收益重述金额 未取到：更正公告未列示每股收益重述数

## 对期初未分配利润与比较报表的影响

- 期初未分配利润 调减 320.00 万元「调减 2024 年 1 月 1 日未分配利润 3,200,000.00 元」〔锚：2025 年年报·第 121 页·附注二·前期差错更正〕[S1]
- 比较报表 已重述「本财务报表已对 2024 年度比较数据进行了重述」〔锚：2025 年年报·第 121 页·附注二·前期差错更正〕[S1]
- 少数股东权益影响 0.00 万元「本次更正不影响少数股东权益」〔锚：2025 年年报·第 121 页·附注二·前期差错更正〕[S1]
- 比较报表列示格式 未取到：更正公告未披露重述后比较报表的列示格式

## 与政策变更、估计变更的界线

- 三类界线 本次属前期差错更正「本公司认为该事项属于前期差错更正，不属于会计政策变更，也不属于会计估计变更」〔锚：2025 年年报·第 122 页·附注二·前期差错更正〕[S1]
- 政策变更判据 未取到：附注未列示会计政策变更的判据
- 估计变更判据 未取到：附注未列示会计估计变更的判据

## 口径与未取到

- 未取到：发现时点的判断依据
- 未取到：每股收益重述金额
- 未取到：比较报表列示格式
- 未取到：政策变更判据
- 未取到：估计变更判据
- 口径：差错性质与更正方法一律照抄更正公告与附注原句，不由本件按金额大小或科目类型推断。
- 口径：重述金额逐字抄录；重述比例自算的，累积影响出处与分子分母各挂各的来源。
- 口径：会计政策变更、会计估计变更、前期差错更正三者是不同的东西，界线只照抄披露自己的表述。
- 口径：四期差异与科目勾稽的点评见 cn-earnings-note，本件只登记更正本身。
- 口径：三张现金流见 cn-cash-flow-quality；审计意见类型见 cn-audit-opinion-cn，本件不判意见。

## 来源

- [S1] 示例材料 2025 年年度报告·附注二·前期差错更正 | https://example.com/ann/S1 | 检索日 2026-11-13 | 类型：公告
- [S2] 示例材料 关于前期会计差错更正的公告 | https://example.com/ann/S2 | 检索日 2026-11-13 | 类型：公告
"""

# ---- 坏样：各只发自己那道码
# 形制坏样插的是**多出一节同名标题**，不是改节标题名：改名会让整节变 stray、节内发现行一并丢，
# 连带节内那条「未取到」也没了，第六节就多出一条假 EC-GAP——测出来的红分不清是哪道判的。
BAD_STRUCT = GOOD.replace(
    "## 受影响的报表科目与各期重述金额",
    "## 更正方法与判据\n\n## 受影响的报表科目与各期重述金额")

BAD_QUOTE = GOOD.replace(
    "「调减 2024 年度营业收入 12,000,000.00 元」〔锚：2025 年年报·第 121 页·附注二·前期差错更正〕[S1]",
    "12,000,000.00 元 [S1]")

BAD_NOSELF = GOOD.replace(
    "｜分母＝2024 年度原披露营业收入 400,000,000.00 元 [S1]",
    "")

BAD_GAP = GOOD.replace(
    "- 未取到：政策变更判据",
    "- 未取到：不适用")

BAD_LINE = GOOD.replace(
    "- 更正方法 追溯重述法",
    "- 本次更正不存在舞弊，更正后报表可信；更正方法 追溯重述法")

# ---- 反证样：不该发的必须不发
OK_HUMAN = GOOD.replace(
    "- 口径：差错性质与更正方法一律照抄更正公告与附注原句，不由本件按金额大小或科目类型推断。",
    "- 差错是否属于舞弊 [待人工]，是否管理层故意 [待人工]，更正后报表是否可信 [待人工]\n"
    "- 口径：差错性质与更正方法一律照抄更正公告与附注原句，不由本件按金额大小或科目类型推断。")

BAD_HUMAN_HALF = GOOD.replace(
    "- 口径：差错性质与更正方法一律照抄更正公告与附注原句，不由本件按金额大小或科目类型推断。",
    "- 差错是否属于舞弊 [待人工]，更正后报表可信\n"
    "- 口径：差错性质与更正方法一律照抄更正公告与附注原句，不由本件按金额大小或科目类型推断。")

# 引文反证样换的是「比较报表」那一行的引文，不动任何「未取到」行——
# 动未取到行会同时删掉正文点名，第六节立刻多一条假 EC-GAP，测出来的红就不是红线那道了。
# 这一行也不含任何词族（重述不在三个词族里），换掉引文不会连带 EC-NOSELF。
OK_QUOTED_REDLINE = GOOD.replace(
    "「本财务报表已对 2024 年度比较数据进行了重述」",
    "「公司否认存在舞弊，未发生人为调节」")

BAD_CHANGE_MIX = GOOD.replace(
    "- 口径：会计政策变更、会计估计变更、前期差错更正三者是不同的东西，界线只照抄披露自己的表述。",
    "- 口径：会计政策变更视同前期差错更正，两者按同一方法处理。")

# 未取到行的**项名**里带词族不算自推：那是在标「没取到的是哪一项」，不是在替披露判断。
# 正文与第六节两处同时改——只改一处会断掉两向对账，测出来的就不是自推那道码了。
OK_GAP_ITEMNAME = GOOD.replace(
    "- 政策变更判据 未取到：附注未列示会计政策变更的判据",
    "- 会计政策变更判据 未取到：附注未列示会计政策变更的判据").replace(
    "- 未取到：政策变更判据",
    "- 未取到：会计政策变更判据")

BAD_METHOD_GUESS = GOOD.replace(
    "- 更正方法 追溯重述法「本公司采用追溯重述法对该项前期差错进行更正」〔锚：2025 年年报·第 120 页·附注二·前期差错更正〕[S1]",
    "- 更正方法 追溯重述法「该差错影响金额较大，属于重大前期差错」〔锚：2025 年年报·第 120 页·附注二·前期差错更正〕[S1]")

BAD_RESTATE_NOBASIS = GOOD.replace(
    "累积影响取附注「上述差错累积影响数为 3,200,000.00 元」〔锚：2025 年年报·第 120 页·附注二·前期差错更正〕[S1]｜",
    "")

# 零输入样例：直接由 GOOD 派生，不另抄一份——两份会各自漂移，
# 而用户看到的「成品长什么样」必须永远等于自测里那个「好样」。
DEMO = GOOD


def _codes(text):
    findings, _stats = check_text(text)
    return findings, set(c for c, _l, _m in findings)


def selftest():
    cases = (
        ("好样应零发条", GOOD, set()),
        ("形制：多出一节同名节（更正方法与判据）", BAD_STRUCT, {"EC-STRUCT"}),
        ("锚：数字行没挂原句与锚", BAD_QUOTE, {"EC-QUOTE"}),
        ("自算：重述比例自算只给分子没给分母", BAD_NOSELF, {"EC-NOSELF"}),
        ("点名：第六节用「不适用」搪塞", BAD_GAP, {"EC-GAP"}),
        ("红线：写不存在舞弊、更正后报表可信", BAD_LINE, {"EC-LINE"}),
        ("反证：[待人工] 整句成立 → 不发", OK_HUMAN, set()),
        ("反证：[待人工] 只豁免自己那句，后半句照样发", BAD_HUMAN_HALF, {"EC-LINE"}),
        ("反证：引文里的「舞弊」不是本件断言 → 不发", OK_QUOTED_REDLINE, set()),
        ("红线：会计政策变更视同前期差错更正", BAD_CHANGE_MIX, {"EC-LINE"}),
        ("反证：未取到行的项名里带词族不算自推 → 不发", OK_GAP_ITEMNAME, set()),
        ("自推：原句没写更正方法却自标追溯重述法", BAD_METHOD_GUESS, {"EC-NOSELF"}),
        ("自算：重述金额自算缺累积影响出处", BAD_RESTATE_NOBASIS, {"EC-NOSELF"}),
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
    ap = argparse.ArgumentParser(description="前期会计差错更正稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="更正稿 .md 路径")
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
        print("缺入参：给一份更正稿路径，或用 --demo / --selftest", file=sys.stderr)
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
