#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_rd_capitalization.py — 研发支出资本化稿五道机检（零网络、零外发、不读环境变量）

用法：
    python3 scripts/check_rd_capitalization.py <研发稿>.md
    python3 scripts/check_rd_capitalization.py --selftest
    python3 scripts/check_rd_capitalization.py --demo     打印一份完整合规样例（零输入可跑）

道一 RD-STRUCT 形制
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]；
  `主体：` 行在场且非空；`报告期：` 行在场且非空；
  七节齐且按序：研发投入与资本化概况／开发支出明细／资本化与费用化的划分／
  资本化条件的满足情况／无形资产摊销与减值／口径与未取到／来源；
  前五节各至少一条 `- ` 发现行，节内只许 `- ` 发现行、`### ` 子标题与空行。

道二 RD-QUOTE 原句与锚
  每条数字行必须以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；原句与锚不得为空；
  例外只有三形：「未取到」行（缺的就是那份披露）、[待人工] 行（判断位）与〔自算〕行（本件自己算的）；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址，检索日缺一不可；
  正文引用的每个 [S#] 必须在来源节有对应行。

道三 RD-NOSELF 不得自推自算（本件承重格）
  一、研究阶段与开发阶段的划分只认原句：写「研究阶段」「开发阶段」的，同一行「」原句里必须也写得到——
      某个项目处在哪个阶段、哪些支出在开发阶段，是披露做的判断。
  二、「满足资本化条件」只认原句：写「满足资本化条件」「符合资本化条件」的，原句同理。
      准则列了五个条件，但**哪个项目满足了、怎么判定的只有披露知道**——本件不替它判。
  三、百分数：行内出现 `25.00%` 一类数值，必须能在同一行的「」原句里逐字找到；
      找不到的须标〔自算〕，且同一行同时给出 `分子…[S#]` 与 `分母…[S#]`。
  四、自算差额：同一行标了〔自算〕又谈轧差／推算／差额／补齐的，必须写明分子与分母各自的来源。
  五、三个数不自行轧差：研发投入合计、资本化金额、费用化金额是三个独立数。
      一行里把它们拼成等式（＝／等于／即／系…之差）而没标〔自算〕，一律发——
      披露只给两个数时，第三个的正确答案是「未取到」，不是减法。

道四 RD-GAP 未取到两向点名
  正文（一至五节）写「未取到 X」⇒ 第六节必须点名 X；第六节点名了 X 而正文没有 ⇒ 同样发；两向都判。
  零缺口时，第六节须显式写 `未取到：无`；
  出现 `不适用`／`无此项`／`无需披露` 一律发——那是把没查当成没有。

道五 RD-LINE 红线
  研发值不值钱／技术是否领先／是不是核心竞争力／该不该全部费用化或继续资本化／
  对利润与股价的影响／目标价与评级 一类断言零命中；
  **只判本件自己写的句子**：同一行「」里的引文先洗掉再判——引文是证据，不是本件的断言；
  含 [待人工] 的分句豁免，且只豁免它自己那一句（按 ；;。，,｜ 切分）。

退码：0 全过 / 1 有发条 / 2 用法错（缺参数） / 3 读不到文件或空稿。
"""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-rd-capitalization-cn"

CODES = ("RD-STRUCT", "RD-QUOTE", "RD-NOSELF", "RD-GAP", "RD-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("研发投入与资本化概况", "开发支出明细", "资本化与费用化的划分",
            "资本化条件的满足情况", "无形资产摊销与减值", "口径与未取到", "来源")
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
STAGE_WORDS = ("研究阶段", "开发阶段")
COND_WORDS = ("满足资本化条件", "符合资本化条件")
RECON_WORDS = ("轧差", "推算", "差额", "补齐")

# 三个独立数的名字——把它们拼成等式就是自动替披露做减法
IDEN_WORDS = ("研发投入", "开发支出")
CAPFEI_WORDS = ("资本化", "费用化")

GAP_EXCUSE = ("不适用", "无此项", "无需披露")

EQUAL_WORDS = ("＝", "=", "等于", "即", "相同", "一致", "等同")
NEG_EQUAL = re.compile(r"(?:不|非)(?:等于|同于|一致|相同|等同)")

HARD_BAN = ("最有价值", "更值钱", "技术领先", "行业领先", "核心竞争力", "护城河",
            "研发实力最强", "创新能力最强", "未来之星",
            "应当全部费用化", "应当费用化", "不应当继续资本化", "应当资本化",
            "建议资本化", "建议费用化",
            "增厚利润", "美化利润", "调节利润", "平滑利润", "利润将增厚",
            "目标价", "目标市值", "买入评级", "增持评级", "中性评级",
            "建议买入", "建议增持", "强烈推荐", "跑赢大盘", "必涨", "必跌",
            "影响股价", "股价将", "预计股价", "市值管理",
            "无风险", "研发必然成功", "项目前景确定", "研发成果可期")

CLAUSE_SPLIT = re.compile(r"[；;。，,｜|]")

SCOPE_RULES = (
    (("无形资产减值测试", "商誉减值", "减值准备计提是否充分"),
     "改走 cn-goodwill-impairment-risk：无形资产与商誉减值风险的判定是那一件，本件只登记摊销与减值披露怎么写"),
    (("研发费用加计扣除", "加计扣除", "税收优惠适用"),
     "改走 tax-policy-card-cn：税收优惠政策的口径与适用条件是那一件"),
    (("四期差异点评", "科目勾稽点评"),
     "改走 cn-earnings-note：财报四期差异与科目勾稽的点评是那一件，本件只登记研发这一节"),
    (("政府补助", "研发补助", "财政补贴"),
     "改走 cn-gov-grant-quality：政府补助与研发补助的台账是那一件"),
    (("审计意见类型", "保留意见", "无法表示意见"),
     "改走 cn-audit-opinion-cn：审计意见类型的判定是那一件"),
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
    """分句里有没有把两个口径写成相等的连接词（否定形不算）。"""
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
    # 逐句洗就洗不干净——「公司称该项目无风险，研发成果可期」这类照抄原文会被误判成本件断言。
    own_line = _strip_quotes(line)
    for clause in _clauses(own_line):
        if "[待人工]" in clause:
            continue
        hit = [w for w in HARD_BAN if w in clause]
        if hit:
            add("RD-LINE", lineno, "红线词：%s（%s）" % ("、".join(sorted(set(hit))), clause.strip()[:40]))
            return


def _quotes(line):
    return "".join(m.group(1) for m in QUOTE.finditer(line))


def _check_vocab(lineno, line, add, words, what):
    """词族只认原句：本件句子里写了，同一行原句也必须写到。

    判域＝去掉**项名**与**锚标签**之后的余下部分。两处都是标签、不是断言：
    项名是「开发阶段支出」这种登记对象，锚标签是「〔锚：…附注五·开发支出〕」
    这种定位指针——把它们算进自推会冤枉正确写法。
    「未取到」行整行豁免——那正是「原句没写所以照实写未取到」的正确形态。
    """
    if _is_gap_line(line):
        return
    body = line
    m = re.match(r"^-\s*([^「：:]*)[：:]\s*(.*)$", line)
    if m:
        body = m.group(2)
    else:
        # 空格分隔的项名形（`- 开发阶段支出 8,000.00 万元「…」`）：项名同样是登记对象，不是断言。
        # 只剥行首到第一个空白之前那一段，且该段不得含「（后面就是正文了）。
        m2 = re.match(r"^-\s*([^「：:\s]+)\s+(.*)$", line)
        if m2:
            body = m2.group(2)
    body = ANCHOR_BLOCK.sub("", body)       # 锚是定位指针，不是本件在判断
    q = _quotes(line)
    outside = [w for w in words if w in body and w not in q]
    if outside:
        add("RD-NOSELF", lineno,
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
        add("RD-NOSELF", lineno, "%s自算未交代%s" % (what, "／".join(why)))


def _is_gap_line(s):
    """一条发现行是不是「未取到」行。

    只认带冒号的登记形（`未取到：原因` ／ `未取到：项名`）。第六节的口径行里会出现
    「披露只给两个时第三个写未取到」这种**叙述**，它不是缺口登记，认错了会给好样发假红。
    """
    return "未取到：" in s or "未取到:" in s


def _check_noself(lineno, line, add):
    q = _quotes(line).replace(" ", "")
    # 一、二、词族：阶段划分与资本化条件只认原句
    _check_vocab(lineno, line, add, STAGE_WORDS, "阶段划分判断")
    _check_vocab(lineno, line, add, COND_WORDS, "资本化条件判断")
    # 三、百分数：原句里没有同一数值，就必须自算并交代分子分母
    # 「未取到」行整行豁免——那一行是在标「哪一项没取到」，里面的百分比是**披露对象的名称**，
    # 不是本件算出来的比值；对它要求〔自算〕等于逼人把缺项写成结论。
    missing = [] if _is_gap_line(line) else [t for t in PCT.findall(line) if _norm_pct(t) not in q]
    if missing:
        if "〔自算〕" not in line:
            add("RD-NOSELF", lineno, "比例 %s 在原句里找不到，也没标〔自算〕：%s"
                % ("、".join(missing), line.strip()[:40]))
        else:
            _check_mol_den(lineno, line, add, "比例")
    # 四、自算差额须交代分子分母
    if "〔自算〕" in line and any(w in line for w in RECON_WORDS):
        _check_mol_den(lineno, line, add, "自算差额")
    # 五、三个数不自行轧差
    #    研发投入合计、资本化金额、费用化金额各有披露值；把它们拼成等式＝本件替披露做了减法。
    #    〔自算〕行豁免——那一行正是「本件自己算了一个比例」，它已经必须交代分子分母。
    own = _strip_quotes(line)
    if "〔自算〕" not in line and not _is_gap_line(line):
        if any(w in own for w in IDEN_WORDS) and any(w in own for w in CAPFEI_WORDS) and _equal_hit(own):
            add("RD-NOSELF", lineno,
                "研发投入／开发支出与资本化／费用化被拼成等式：三个数各有披露值，不自行轧差，缺的那个写未取到：%s"
                % line.strip()[:40])


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
            add("RD-STRUCT", 1, "头部缺自标「%s」" % mark)
    if not any(SUBJECT.match(s) for _i, s in header):
        add("RD-STRUCT", 1, "头部缺 `主体：` 行")
    if not any(PERIOD.match(s) for _i, s in header):
        add("RD-STRUCT", 1, "头部缺 `报告期：` 行")

    # ---- 道一 节齐与序
    names = [n for n, _l, _b in sections]
    for name in SECTIONS:
        if name not in names:
            add("RD-STRUCT", 1, "缺节「%s」" % name)
    pos = [SECTIONS.index(n) for n in names]
    if pos != sorted(pos):
        add("RD-STRUCT", 1, "节序不对：现序 %s，应序 %s" % ("／".join(names), "／".join(SECTIONS)))
    for lineno, raw in stray:
        add("RD-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw)

    referenced = []
    body_gaps = []
    section_found = {}

    for name, hline, body in sections:
        if name in CONTENT_SECTIONS:
            n_find = 0
            for lineno, s in body:
                if not s.strip() or s.lstrip().startswith("###"):
                    continue
                if not _is_finding_line(s):
                    add("RD-STRUCT", lineno, "节内只许 `- ` 发现行：%s" % s.strip()[:40])
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
                        add("RD-QUOTE", lineno, "发现行缺「」原句 + 〔锚：…〕 + [S#] 三元组：%s"
                            % s.strip()[:40])
                else:
                    for m in TRIPLE.finditer(s):
                        if not m.group("q").strip():
                            add("RD-QUOTE", lineno, "原句为空")
                        if not m.group("a").strip():
                            add("RD-QUOTE", lineno, "锚为空")
                    if not re.search(r"\[S\d+\]\s*$", s.strip()):
                        add("RD-QUOTE", lineno, "发现行未以 [S#] 收尾（三元组须在行末）")
                _check_line(lineno, s, add)
                if PCT.findall(s):
                    stats["ratio_lines"] += 1
                _check_noself(lineno, s, add)
            section_found[name] = n_find
            if n_find == 0:
                add("RD-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name)

        elif name == GAP_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not _is_finding_line(s):
                    add("RD-STRUCT", lineno, "第六节只许 `- ` 行：%s" % s.strip()[:40])
                    continue
                section_found.setdefault(name, 0)
                section_found[name] += 1
                for w in GAP_EXCUSE:
                    if w in s:
                        add("RD-GAP", lineno, "禁用「%s」把没查当成没有：%s" % (w, s.strip()[:40]))
                _check_line(lineno, s, add)

        elif name == SOURCE_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not s.lstrip().startswith("- ["):
                    add("RD-STRUCT", lineno, "来源节只许 `- [S#] …` 行：%s" % s.strip()[:40])
                    continue
                m = SOURCE_LINE.match(s.strip())
                if not m:
                    add("RD-QUOTE", lineno, "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:50])
                    continue
                stats["sources"] += 1

    # ---- 道四 未取到两向点名
    gap_body = [s for _ln, s in body_gaps]
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
            add("RD-GAP", 1, "正文写了未取到「%s」，第六节没点名" % key)
    for g in gap_sec:
        key = _gap_key(g)
        if key and not any(key in s for s in gap_body):
            add("RD-GAP", 1, "第六节点名了「%s」，正文没有这条表述" % key)

    # 零缺口须显式写「未取到：无」
    if not gap_body and not gap_sec:
        gap_text = "\n".join(s for name, _h, body in sections if name == GAP_SECTION
                             for _ln, s in body)
        if "未取到：无" not in gap_text and "未取到:无" not in gap_text:
            add("RD-GAP", 1, "零缺口未显式写「未取到：无」")

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
            add("RD-QUOTE", 1, "正文引用 [%s]，来源节没有对应登记行" % ref)

    # ---- 边界
    # 只判前五节（登记正文）。第六节「口径与未取到」正是写明与另几枚件分界的地方。
    body_lines = [(ln, s) for name, _h, body in sections
                  if name in CONTENT_SECTIONS for ln, s in body]
    for words, tip in SCOPE_RULES:
        for ln, s in body_lines:
            if any(w in s for w in words):
                add("RD-STRUCT", ln, "越界：%s" % tip)
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


GOOD = r"""# 示例材料（600000.SH）研发支出资本化登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议 ｜ 判断位 [待人工]
主体：示例材料（600000.SH）
报告期：2025 年年度报告·附注五·开发支出与无形资产

## 研发投入与资本化概况

- 研发投入合计 32,000.00 万元「本期研发投入合计 320,000,000.00 元」〔锚：2025 年年报·第 128 页·附注五·研发投入〕[S1]
- 其中费用化 24,000.00 万元「本期费用化研发投入 240,000,000.00 元」〔锚：2025 年年报·第 128 页·附注五·研发投入〕[S1]
- 资本化金额 8,000.00 万元「本期资本化研发投入 80,000,000.00 元」〔锚：2025 年年报·第 128 页·附注五·研发投入〕[S1]
- 资本化率 25.00%〔自算〕分子＝本期资本化研发投入 80,000,000.00 元 [S1]｜分母＝本期研发投入合计 320,000,000.00 元 [S1]
- 占营业收入比 未取到：附注未披露研发投入占营业收入的比例

## 开发支出明细

- 期初余额 6,500.00 万元「开发支出期初余额 65,000,000.00 元」〔锚：2025 年年报·第 129 页·附注五·开发支出〕[S1]
- 本期增加 8,000.00 万元「本期开发支出增加额 80,000,000.00 元」〔锚：2025 年年报·第 129 页·附注五·开发支出〕[S1]
- 本期转入无形资产 5,000.00 万元「本期开发支出转入无形资产 50,000,000.00 元」〔锚：2025 年年报·第 129 页·附注五·开发支出〕[S1]
- 本期转入当期损益 未取到：附注未披露开发支出转入当期损益的金额
- 期末余额 9,500.00 万元「开发支出期末余额 95,000,000.00 元」〔锚：2025 年年报·第 129 页·附注五·开发支出〕[S1]
- 开发支出本期增加占研发投入比 25.00%〔自算〕分子＝开发支出本期增加额 80,000,000.00 元 [S1]｜分母＝本期研发投入合计 320,000,000.00 元 [S1]

## 资本化与费用化的划分

- 划分标准 照抄附注表述「研究阶段的支出于发生时计入当期损益，开发阶段的支出同时满足下列条件的予以资本化」〔锚：2025 年年报·第 130 页·附注五·开发支出〕[S1]
- 研究阶段支出 24,000.00 万元「本期研究阶段支出 240,000,000.00 元，全部计入当期损益」〔锚：2025 年年报·第 130 页·附注五·开发支出〕[S1]
- 开发阶段支出 8,000.00 万元「本期开发阶段支出 80,000,000.00 元」〔锚：2025 年年报·第 130 页·附注五·开发支出〕[S1]
- 资本化起始时点 未取到：附注未披露各项目开始资本化的具体时点
- 在研项目名称与所处阶段 未取到：附注未逐项目列示在研项目名称与所处阶段

## 资本化条件的满足情况

- 五项条件原文 照抄附注表述「①完成该无形资产以使其能够使用或出售在技术上具有可行性；②具有完成该无形资产并使用或出售的意图；③无形资产产生经济利益的方式；④有足够的技术、财务资源和其他资源支持；⑤归属于该无形资产开发阶段的支出能够可靠地计量」〔锚：2025 年年报·第 130 页·附注五·开发支出〕[S1]
- 本期满足条件的项目数 未取到：附注未披露本期满足资本化条件的项目数量
- 条件判断依据 未取到：附注未说明各项目如何判定满足上述条件
- 资本化金额占开发支出增加额比 100.00%〔自算〕分子＝本期资本化研发投入 80,000,000.00 元 [S1]｜分母＝开发支出本期增加额 80,000,000.00 元 [S1]

## 无形资产摊销与减值

- 资本化形成无形资产原值 5,000.00 万元「本期开发支出转入无形资产 50,000,000.00 元」〔锚：2025 年年报·第 131 页·附注五·无形资产〕[S1]
- 摊销年限 5 年「该项无形资产按 5 年、采用直线法摊销」〔锚：2025 年年报·第 131 页·附注五·无形资产〕[S1]
- 本期摊销额 500.00 万元「本期无形资产摊销额 5,000,000.00 元」〔锚：2025 年年报·第 131 页·附注五·无形资产〕[S1]
- 摊销政策 直线法「无形资产采用直线法按预计使用寿命摊销」〔锚：2025 年年报·第 131 页·附注五·无形资产〕[S1]
- 资本化形成无形资产的减值准备 未取到：附注未披露该等无形资产的减值准备金额

## 口径与未取到

- 未取到：占营业收入比
- 未取到：本期转入当期损益
- 未取到：资本化起始时点
- 未取到：在研项目名称与所处阶段
- 未取到：本期满足条件的项目数
- 未取到：条件判断依据
- 未取到：资本化形成无形资产的减值准备
- 口径：研究阶段与开发阶段的划分、各项目所处阶段一律照抄附注原句，不由本件按项目进度推断。
- 口径：研发投入合计、资本化金额、费用化金额是三个独立数，披露只给两个时第三个写未取到，不自行轧差补齐。
- 口径：资本化率披露没给的，本件算出来才标〔自算〕，并在同一行给出分子与分母各自的来源。
- 口径：摊销年限与减值照抄原值；项目是否满足资本化条件只登记披露说法，本件不替披露判定。
- 口径：无形资产减值测试的结论见 cn-goodwill-impairment-risk；加计扣除等税收口径见 tax-policy-card-cn；四期差异与科目勾稽的点评见 cn-earnings-note。

## 来源

- [S1] 示例材料 2025 年年度报告·附注五·开发支出与无形资产 | https://example.com/ann/S1 | 检索日 2026-11-13 | 类型：年报
- [S2] 示例材料 2025 年年度报告·合并利润表 | https://example.com/ann/S2 | 检索日 2026-11-13 | 类型：年报
"""

# ---- 坏样：各只发自己那道码
# 形制坏样插的是**多出一节同名标题**，不是改节标题名：改名会让整节变 stray、节内发现行一并丢，
# 连带节内那条「未取到」也没了，第六节就多出一条假 RD-GAP——测出来的红分不清是哪道判的。
BAD_STRUCT = GOOD.replace(
    "## 开发支出明细",
    "## 研发投入与资本化概况\n\n## 开发支出明细")

BAD_QUOTE = GOOD.replace(
    "「本期研发投入合计 320,000,000.00 元」〔锚：2025 年年报·第 128 页·附注五·研发投入〕[S1]",
    "320,000,000.00 元 [S1]")

BAD_NOSELF = GOOD.replace(
    "｜分母＝本期研发投入合计 320,000,000.00 元 [S1]",
    "")

BAD_GAP = GOOD.replace(
    "- 未取到：资本化起始时点",
    "- 未取到：无此项")

BAD_LINE = GOOD.replace(
    "- 本期摊销额 500.00 万元",
    "- 该研发项目是公司的核心竞争力；本期摊销额 500.00 万元")

# ---- 反证样：不该发的必须不发
OK_HUMAN = GOOD.replace(
    "- 口径：摊销年限与减值照抄原值；项目是否满足资本化条件只登记披露说法，本件不替披露判定。",
    "- 该研发项目值不值钱 [待人工]，是否建议继续资本化 [待人工]，对利润的影响 [待人工]\n"
    "- 口径：摊销年限与减值照抄原值；项目是否满足资本化条件只登记披露说法，本件不替披露判定。")

BAD_HUMAN_HALF = GOOD.replace(
    "- 口径：摊销年限与减值照抄原值；项目是否满足资本化条件只登记披露说法，本件不替披露判定。",
    "- 该研发项目值不值钱 [待人工]，该项目的技术领先于同行业\n"
    "- 口径：摊销年限与减值照抄原值；项目是否满足资本化条件只登记披露说法，本件不替披露判定。")

# 引文反证样换的是「摊销政策」那一行的引文，不动任何「未取到」行——
# 动未取到行会同时删掉正文点名，第六节立刻多一条假 RD-GAP，测出来的红就不是红线那道了。
# 这一行也不含两个词族，换掉引文不会连带 RD-NOSELF。
OK_QUOTED_REDLINE = GOOD.replace(
    "「无形资产采用直线法按预计使用寿命摊销」",
    "「公司称该项目无风险，研发成果可期」")

BAD_JIAZHA = GOOD.replace(
    "- 资本化金额 8,000.00 万元",
    "- 资本化金额 即研发投入合计与费用化金额之差")

# 未取到行的**项名**里带词族不算自推：那是在标「没取到的是哪一项」，不是在替披露判断。
# 正文与第六节两处同时改——只改一处会断掉两向对账，测出来的就不是自推那道码了。
OK_GAP_ITEMNAME = GOOD.replace(
    "- 本期满足条件的项目数 未取到：附注未披露本期满足资本化条件的项目数量",
    "- 本期满足资本化条件的项目数 未取到：附注未披露本期满足资本化条件的项目数量").replace(
    "- 未取到：本期满足条件的项目数",
    "- 未取到：本期满足资本化条件的项目数")

# 坏样要坏在判据真正看的地方：只换引文、项名里不带词族，判据剥掉项名后整行就没有词族了，
# 码发不出来（上一枚踩过这个坑）。这里让「开发阶段」成为原句之外唯一的词族。
BAD_STAGE_GUESS = GOOD.replace(
    "- 划分标准 照抄附注表述「研究阶段的支出于发生时计入当期损益，开发阶段的支出同时满足下列条件的予以资本化」",
    "- 划分标准 开发阶段支出全部资本化「本公司的研发活动按项目立项管理，各项支出按项目归集」")

BAD_SELF_NOBASIS = GOOD.replace(
    "分子＝本期资本化研发投入 80,000,000.00 元 [S1]｜",
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
        ("形制：多出一节同名节（研发投入与资本化概况）", BAD_STRUCT, {"RD-STRUCT"}),
        ("锚：数字行没挂原句与锚", BAD_QUOTE, {"RD-QUOTE"}),
        ("自算：比例自算只给分子没给分母", BAD_NOSELF, {"RD-NOSELF"}),
        ("点名：第六节用「无此项」搪塞", BAD_GAP, {"RD-GAP"}),
        ("红线：写核心竞争力", BAD_LINE, {"RD-LINE"}),
        ("反证：[待人工] 整句成立 → 不发", OK_HUMAN, set()),
        ("反证：[待人工] 只豁免自己那句，后半句照样发", BAD_HUMAN_HALF, {"RD-LINE"}),
        ("反证：引文里的「无风险」不是本件断言 → 不发", OK_QUOTED_REDLINE, set()),
        ("自算：研发投入与资本化费用化被拼成等式", BAD_JIAZHA, {"RD-NOSELF"}),
        ("反证：未取到行的项名里带词族不算自推 → 不发", OK_GAP_ITEMNAME, set()),
        ("自推：原句没写阶段划分却自标", BAD_STAGE_GUESS, {"RD-NOSELF"}),
        ("自算：比例自算缺分子来源", BAD_SELF_NOBASIS, {"RD-NOSELF"}),
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
    ap = argparse.ArgumentParser(description="研发支出资本化稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="研发稿 .md 路径")
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
        print("缺入参：给一份研发稿路径，或用 --demo / --selftest", file=sys.stderr)
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
