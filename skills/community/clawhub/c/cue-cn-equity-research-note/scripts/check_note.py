#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_note.py — 个股深度研究稿五道机检（零网络、零外发、不读环境变量）

用法：
    python3 scripts/check_note.py <研究稿>.md
    python3 scripts/check_note.py --selftest

道一 ER-FORM 形制
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]；
  `主体：` 行在场且非空；`截至日：YYYY-MM-DD` 行在场且值可认；
  六节齐且按序：业务拆解／竞争位／驱动因子／风险清单／关键数字表／来源；
  业务拆解至风险清单四节各至少一条 `- ` 发现行（空节＝不是一份研究稿），且节内只许出现
  `- ` 发现行、`### ` 子标题与空行——散文段落无处挂锚，按非发现行发；
  关键数字表须有表头行与至少一条数据行，表头含「原句」「锚」「来源」三列；
  来源节至少一条来源行。

道二 ER-ANCHOR 原句与锚
  四节每条 `- ` 发现行必须以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；
  原句不得为空，锚不得为空；
  关键数字表每条数据行须同时出现「」原句、(S#) 编号与「锚」列；
  来源行形制 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 与检索日缺一不可，且须是可点的 http(s) 地址；
  正文引用的每个 [S#] 必须在来源节有对应行；引用了没登记的，发。

道三 ER-REDLINE 红线（评级／目标价／股价预测／看好看空）
  硬词零命中：目标价、目标市值、买入评级、增持评级、中性评级、跑赢大盘、跑输大盘、强烈推荐、
  首次覆盖、上调评级、下调评级、严重低估、严重高估、看好、看空、看多、看淡、必涨、必跌、
  稳赚、零风险、保证收益；
  情境词：`股价／市值／估值` 与 `翻倍／上涨空间／见底／见顶／创新高／再创新低` 相距 10 字以内视为预测；
  `(评级|给予|维持|首次覆盖|上调|下调)` 与 `买入／增持／中性／减持／推荐` 相距 8 字以内视为评级。
  含 [待人工] 的分句豁免，且只豁免它自己那一句（按 ；;。，,｜ 切分），同行后半句照样发。

道四 ER-NOSELF 不得自算
  发现行里出现百分数（`12.3%` 或 `12.3％`）时，该数值必须能在同一行的「」原句里逐字找到；
  找不到的，该行须标 `〔自算〕`，且同一行同时给出 `分子…[S#]` 与 `分母…[S#]`——分子分母各自挂源；
  标了 〔自算〕 却缺分子或缺分母的来源，同样发。
  毛利率、市占率、增速、渗透率、占比、周转率、负债率、复合增长率这些比率词出现在发现行里，
  也按同一条走：只认原句，披露没写就不许自己除。关键数字表的数据行同验。
  非百分数的自算（如「约为 X 倍」）不强制 〔自算〕，但行里真标了就照上面查分子分母。

道五 ER-SCOPE 边界
  正文出现「已出财报」「财报点评」「四期差异」「科目勾稽」「覆盖账本」→ 点名改走 cn-earnings-note；
  正文出现「问题清单」「逐问作答」「问题驱动」「多源速览」→ 点名改走 cn-research-brief；
  正文出现「研报摘要」「研报结论」「研报原文摘录」→ 点名：本件只认能回到句子的原句，不搬研报结论。

退码：0 全过 / 1 有发条 / 3 读不到文件、缺参数或空稿。
"""

import argparse
import re
import sys

CODES = ("ER-FORM", "ER-ANCHOR", "ER-REDLINE", "ER-NOSELF", "ER-SCOPE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("业务拆解", "竞争位", "驱动因子", "风险清单", "关键数字表", "来源")
CONTENT_SECTIONS = SECTIONS[:4]
TABLE_SECTION = "关键数字表"
SOURCE_SECTION = "来源"

HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")

SUBJECT = re.compile(r"^主体：\s*(\S.*)$")
ASOF = re.compile(r"^截至日：\s*(\d{4}-\d{2}-\d{2})\s*$")

TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
ANCHOR_REF = re.compile(r"\[(S\d+)\]")

SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)"
    r"\|\s*(?P<url>https?://\S+)\s*\|"
    r"\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$"
)

PCT = re.compile(r"\d+(?:\.\d+)?\s*[%％]")
RATIO_KW = ("毛利率", "净利率", "市占率", "市场份额", "增速", "增长率", "渗透率",
            "占比", "周转率", "负债率", "复合增长", "集中度")

HARD_BAN = ("目标价", "目标市值", "买入评级", "增持评级", "中性评级", "跑赢大盘", "跑输大盘",
            "强烈推荐", "首次覆盖", "上调评级", "下调评级", "严重低估", "严重高估",
            "看好", "看空", "看多", "看淡", "必涨", "必跌", "稳赚", "零风险", "保证收益")

PRICE_WORDS = ("股价", "市值", "估值")
PRED_WORDS = ("翻倍", "上涨空间", "见底", "见顶", "创新高", "再创新低", "下行空间")

RATING_VERB = ("评级", "给予", "维持", "首次覆盖", "上调", "下调", "建议")
RATING_WORD = ("买入", "增持", "中性", "减持", "推荐")

CLAUSE_SPLIT = re.compile(r"[；;。，,｜|]")

SCOPE_RULES = (
    (("已出财报", "财报点评", "四期差异", "科目勾稽", "覆盖账本"),
     "改走 cn-earnings-note：那一件做已出财报的逐数点评，本件只做未出财报期的个股研究"),
    (("问题清单", "逐问作答", "问题驱动", "多源速览"),
     "改走 cn-research-brief：那一件是问题驱动的多源速览，本件是标的主键驱动"),
    (("研报摘要", "研报结论", "研报原文摘录"),
     "本件只认能回到句子的原句，不搬研报结论；要抓研报原文另走研报原文类工具"),
)


def _norm_pct(tok):
    return tok.replace(" ", "").replace("％", "%")


def _clauses(line):
    return [c for c in CLAUSE_SPLIT.split(line)]


def _section_of(heading):
    h = heading.strip()
    for _ in range(2):
        h2 = NUMBERING.sub("", h)
        if h2 == h:
            break
        h = h2
    h = h.strip()
    for name in SECTIONS:
        if h.startswith(name):
            return name
    return None


def split_doc(text):
    """→ (header_lines, [(name, heading_lineno, [(lineno, line)])], stray_headings)"""
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


def _check_redline(lineno, line, add):
    for clause in _clauses(line):
        if "[待人工]" in clause:
            continue
        hit = [w for w in HARD_BAN if w in clause]
        for pw in PRICE_WORDS:
            for idx in [m.start() for m in re.finditer(pw, clause)]:
                window = clause[idx: idx + len(pw) + 10]
                if any(w in window for w in PRED_WORDS):
                    hit.append("%s+%s" % (pw, next(w for w in PRED_WORDS if w in window)))
        m = re.search(r"(%s)[^，。；｜]{0,8}(%s)" % ("|".join(RATING_VERB), "|".join(RATING_WORD)), clause)
        if m:
            hit.append(m.group(0))
        if hit:
            add("ER-REDLINE", lineno, "红线词：%s（%s）" % ("、".join(sorted(set(hit))), clause.strip()[:40]))
            return


def _check_selfcalc(lineno, line, add, kind="行"):
    toks = PCT.findall(line)
    if not toks:
        return
    quotes = "".join(m.group(1) for m in QUOTE.finditer(line))
    missing = [t for t in toks if _norm_pct(t) not in quotes.replace(" ", "")]
    if not missing:
        return
    if "〔自算〕" in line:
        # 分子／分母的 [S#] 必须挂在自己那个数上：不许跨过 ｜、引号或锚的收尾去借下一处来源
        mol = re.search(r"分子[^｜|〕」；。]*\[S\d+\]", line)
        den = re.search(r"分母[^｜|〕」；。]*\[S\d+\]", line)
        if mol and den:
            return
        why = []
        if not mol:
            why.append("缺分子来源")
        if not den:
            why.append("缺分母来源")
        add("ER-NOSELF", lineno, "自算未交代%s：%s" % ("／".join(why), "、".join(missing)))
        return
    add("ER-NOSELF", lineno, "比率 %s 在原句里找不到，也没标〔自算〕：%s"
        % ("、".join(missing), line.strip()[:40]))


def _check_table_row(lineno, s, add):
    if not (s.startswith("|") and s.endswith("|")):
        add("ER-FORM", lineno, "关键数字表里出现非表格行：%s" % s.strip()[:40])
        return
    cells = [c.strip() for c in s.strip().strip("|").split("|")]
    if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
        return
    body = s
    if "「" not in body or "」" not in body:
        add("ER-ANCHOR", lineno, "关键数字表数据行缺「」原句：%s" % s.strip()[:40])
    if not ANCHOR_REF.search(body):
        add("ER-ANCHOR", lineno, "关键数字表数据行缺 [S#]：%s" % s.strip()[:40])
    _check_selfcalc(lineno, body, add, kind="表行")


def check_text(text):
    findings = []
    stats = {"finding_lines": 0, "sources": 0, "ratios": 0}

    def add(code, lineno, msg):
        findings.append((code, lineno, msg))

    header, sections, stray = split_doc(text)

    # ---- 道一 头部
    htext = "\n".join(s for _i, s in header)
    for mark in MARK_TEXTS:
        if mark not in htext:
            add("ER-FORM", 1, "头部缺自标「%s」" % mark)
    if not any(SUBJECT.match(s) for _i, s in header):
        add("ER-FORM", 1, "头部缺 `主体：` 行")
    if not any(ASOF.match(s) for _i, s in header):
        add("ER-FORM", 1, "头部缺 `截至日：YYYY-MM-DD` 行或日期不合形")

    # ---- 道一 节齐与序
    names = [n for n, _l, _b in sections]
    for name in SECTIONS:
        if name not in names:
            add("ER-FORM", 1, "缺节「%s」" % name)
    pos = [SECTIONS.index(n) for n in names]
    if pos != sorted(pos):
        add("ER-FORM", 1, "节序不对：现序 %s，应序 %s" % ("／".join(names), "／".join(SECTIONS)))
    for lineno, raw in stray:
        add("ER-FORM", lineno, "不认识的节标题或多出同名节：%s" % raw)

    # ---- 正文引用收集
    referenced = []

    for name, hline, body in sections:
        if name in CONTENT_SECTIONS:
            n_find = 0
            for lineno, s in body:
                if not s.strip() or s.lstrip().startswith("###"):
                    continue
                if not _is_finding_line(s):
                    add("ER-FORM", lineno, "四节内只许 `- ` 发现行：%s" % s.strip()[:40])
                    continue
                n_find += 1
                stats["finding_lines"] += 1
                referenced.extend(ANCHOR_REF.findall(s))
                if not TRIPLE.search(s):
                    if "未取到" in s or "【未取到】" in s:
                        pass  # 缺料行本来就无原句可挂；道二只要求它挂 [S#] 指向查过的那一处
                    elif "[待人工]" in s:
                        pass  # 判断位待人工，无原句可挂
                    elif "〔自算〕" in s:
                        pass  # 自算值本来就没有原句；分子／分母各自挂源另在下面统一验
                    else:
                        add("ER-ANCHOR", lineno, "发现行缺「」原句 + 〔锚：…〕 + [S#] 三元组：%s"
                            % s.strip()[:40])
                else:
                    for m in TRIPLE.finditer(s):
                        if not m.group("q").strip():
                            add("ER-ANCHOR", lineno, "原句为空")
                        if not m.group("a").strip():
                            add("ER-ANCHOR", lineno, "锚为空")
                    if not re.search(r"\[S\d+\]\s*$", s.strip()):
                        add("ER-ANCHOR", lineno, "发现行未以 [S#] 收尾（三元组须在行末）")
                if "〔自算〕" in s:
                    # 自算行无论挂不挂原句，分子与分母都必须各自挂源，不许借同一处
                    if not (re.search(r"分子[^｜|〕」；。]*\[S\d+\]", s)
                            and re.search(r"分母[^｜|〕」；。]*\[S\d+\]", s)):
                        add("ER-ANCHOR", lineno, "自算行未分别给出分子与分母的 [S#]：%s"
                            % s.strip()[:40])
                _check_redline(lineno, s, add)
                if PCT.findall(s) or any(k in s for k in RATIO_KW):
                    stats["ratios"] += 1
                _check_selfcalc(lineno, s, add)
            if n_find == 0:
                add("ER-FORM", hline, "节「%s」没有一条发现行（空节）" % name)

        elif name == TABLE_SECTION:
            rows = 0
            header_row = None
            for lineno, s in body:
                if not s.strip():
                    continue
                if s.lstrip().startswith("###"):
                    continue
                if not s.lstrip().startswith("|"):
                    add("ER-FORM", lineno, "关键数字表里出现非表格行：%s" % s.strip()[:40])
                    continue
                s = s.strip()
                if header_row is None:
                    header_row = (lineno, s)
                    continue
                _check_table_row(lineno, s, add)
                cells = [c.strip() for c in s.strip("|").split("|")]
                if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    continue
                rows += 1
                referenced.extend(ANCHOR_REF.findall(s))
            if header_row is None:
                add("ER-FORM", hline, "关键数字表缺表头行")
            else:
                for col in ("原句", "锚", "来源"):
                    if col not in header_row[1]:
                        add("ER-FORM", header_row[0], "关键数字表表头缺列「%s」" % col)
            if rows == 0:
                add("ER-FORM", hline, "关键数字表没有数据行")

        elif name == SOURCE_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not s.lstrip().startswith("- ["):
                    add("ER-FORM", lineno, "来源节只许 `- [S#] …` 行：%s" % s.strip()[:40])
                    continue
                m = SOURCE_LINE.match(s.strip())
                if not m:
                    add("ER-ANCHOR", lineno, "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:50])
                    continue
                stats["sources"] += 1

    # ---- 道二 引用与登记一一对应
    defined = set()
    for name, _hline, body in sections:
        if name != SOURCE_SECTION:
            continue
        for _lineno, s in body:
            m = SOURCE_LINE.match(s.strip())
            if m:
                defined.add(m.group("s"))
    for ref in sorted(set(referenced)):
        if ref not in defined:
            add("ER-ANCHOR", 1, "正文引用 [%s]，来源节没有对应登记行" % ref)

    # ---- 道五 边界
    body_lines = [(ln, s) for name, _h, body in sections
                  if name != SOURCE_SECTION for ln, s in body]
    for words, tip in SCOPE_RULES:
        for ln, s in body_lines:
            if any(w in s for w in words):
                add("ER-SCOPE", ln, "越界：%s" % tip)
                break

    findings.sort(key=lambda x: (x[1], CODES.index(x[0])))
    return findings, stats


def report(path, findings, stats):
    print("稿：%s" % path)
    print("统计：发现行 %d ｜ 来源 %d ｜ 涉比率行 %d"
          % (stats["finding_lines"], stats["sources"], stats["ratios"]))
    if not findings:
        print("结论：五道全过（零发条）")
        return
    print("结论：发条 %d" % len(findings))
    for code, lineno, msg in findings:
        print("  %s L%-4d %s" % (code, lineno, msg))
    hit = sorted(set(c for c, _l, _m in findings))
    print("发条码：%s" % "、".join(hit))


GOOD = r"""# 示例科技（600000.SH）个股深度研究初稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议 ｜ 判断位 [待人工]
主体：示例科技（600000.SH）
截至日：2026-11-09

## 业务拆解

- 收入按产品线分为数控机床与功能部件两块，数控机床是主要来源「公司主营业务收入主要来自数控机床及功能部件两大板块」〔锚：2025 年年报·第 46 页·营业收入构成表〕[S1]
- 数控机床 2025 年实现营业收入 42.6 亿元，占主营业务收入 68.30%「数控机床产品实现营业收入 426,000.00 万元，占主营业务收入的 68.30%」〔锚：2025 年年报·第 46 页·营业收入构成表〕[S1]
- 功能部件 2025 年实现营业收入 19.8 亿元「功能部件业务实现营业收入 198,000.00 万元」〔锚：2025 年年报·第 46 页·营业收入构成表〕[S1]
- 机床业务收入约为功能部件的 2.15 倍〔自算〕分子＝数控机床 426,000.00 万元 [S1]｜分母＝功能部件 198,000.00 万元 [S1]

## 竞争位

- 国内数控机床行业 2025 年前五名企业合计市场份额为 31.20%「2025 年国内数控机床行业前五名企业合计市场份额为 31.20%」〔锚：行业研究·第 3 节·竞争格局〕[S2]
- 已披露的同行业可比公司名单见招股说明书「同行业可比公司包括华中数控、海天精工等」〔锚：招股说明书·第 88 页·同行业可比公司〕[S3]
- 未取到 公司在细分型号上的份额：行业资料只给前五名合计，未按型号拆分 [S2]

## 驱动因子

- 驱动变量为募投项目产能释放，投产进度直接影响 2027 年收入上限「募投项目预计于 2027 年三季度达到预定可使用状态」〔锚：2026-06-30 募集资金存放与使用情况公告·第二节〕[S4]
- 可观测指标为在建工程转固金额，可在定期报告里逐期取得「在建工程本期转入固定资产 12,300.00 万元」〔锚：2026 年半年度报告·第 31 页·在建工程〕[S5]

## 风险清单

- 风险为原材料价格上行，触发条件为原材料价格出现大幅上涨「若原材料价格出现大幅上涨，公司毛利率存在下降风险」〔锚：2025 年年报·第 22 页·风险因素〕[S1]
- 已披露的应对为集中采购与长期协议锁价「公司通过集中采购与长期协议锁定部分原材料成本」〔锚：2025 年年报·第 22 页·风险因素〕[S1]
- 未取到 客户集中度的具体数值：公告未披露前五大客户占比 [S1]

## 关键数字表

| 指标 | 数值 | 口径与期间 | 原句 | 锚 | 来源 |
|---|---|---|---|---|---|
| 数控机床收入 | 42.6 亿元 | 2025 年度·合并口径 | 「数控机床产品实现营业收入 426,000.00 万元」 | 2025 年年报·第 46 页 | [S1] |
| 数控机床收入占比 | 68.30% | 2025 年度·占主营业务收入 | 「占主营业务收入的 68.30%」 | 2025 年年报·第 46 页 | [S1] |
| 前五名企业合计份额 | 31.20% | 2025 年度·行业口径 | 「前五名企业合计市场份额为 31.20%」 | 行业研究·第 3 节 | [S2] |

## 来源

- [S1] 示例科技 2025 年年度报告 | https://example.com/ann/S1 | 检索日 2026-11-09 | 类型：公告
- [S2] 数控机床行业竞争格局研究 | https://example.com/res/S2 | 检索日 2026-11-09 | 类型：研报
- [S3] 示例科技首次公开发行招股说明书 | https://example.com/ann/S3 | 检索日 2026-11-09 | 类型：公告
- [S4] 示例科技 2026 年半年度募集资金存放与实际使用情况专项报告 | https://example.com/ann/S4 | 检索日 2026-11-09 | 类型：公告
- [S5] 示例科技 2026 年半年度报告 | https://example.com/ann/S5 | 检索日 2026-11-09 | 类型：公告
"""

# ---- 各坏样：只发自己那道码
BAD_FORM = GOOD.replace("## 驱动因子", "## 驱动因素")
BAD_EMPTY = GOOD.replace(
    "- 风险为原材料价格上行，触发条件为原材料价格出现大幅上涨「若原材料价格出现大幅上涨，公司毛利率存在下降风险」〔锚：2025 年年报·第 22 页·风险因素〕[S1]\n"
    "- 已披露的应对为集中采购与长期协议锁价「公司通过集中采购与长期协议锁定部分原材料成本」〔锚：2025 年年报·第 22 页·风险因素〕[S1]\n"
    "- 未取到 客户集中度的具体数值：公告未披露前五大客户占比 [S1]\n", "")
BAD_ANCHOR = GOOD.replace(
    "「募投项目预计于 2027 年三季度达到预定可使用状态」〔锚：2026-06-30 募集资金存放与使用情况公告·第二节〕[S4]",
    "募投项目预计于 2027 年三季度达到预定可使用状态 [S4]")
BAD_REDLINE = GOOD.replace(
    "- 已披露的应对为集中采购与长期协议锁价",
    "- 我们给予公司买入评级，目标价 58 元；已披露的应对为集中采购与长期协议锁价")
BAD_NOSELF = GOOD.replace(
    "| 数控机床收入占比 | 68.30% |", "| 数控机床收入占比 | 71.50% |")
BAD_SCOPE = GOOD.replace(
    "- 可观测指标为在建工程转固金额",
    "- 本稿同时覆盖已出财报的四期差异与科目勾稽；可观测指标为在建工程转固金额")

# ---- 反证样：不该发的必须不发
OK_SELF_DECLARED = GOOD.replace(
    "| 数控机床收入占比 | 68.30% |",
    "| 机床与功能部件收入之比 | 2.15 倍 |")
OK_HUMAN = GOOD.replace(
    "- 未取到 客户集中度的具体数值：公告未披露前五大客户占比 [S1]",
    "- 未取到 客户集中度的具体数值：公告未披露前五大客户占比 [S1]\n"
    "- 公司是否属于行业龙头，交由人工判断 [待人工]")

BAD_HUMAN_HALF = GOOD.replace(
    "- 未取到 客户集中度的具体数值：公告未披露前五大客户占比 [S1]",
    "- 未取到 客户集中度的具体数值 [待人工]，建议买入 [S1]")

# 自算行里分母跨过引号去借下一处来源的锚——分母没自己的出处
BAD_SELF_BORROW = GOOD.replace(
    "- 机床业务收入约为功能部件的 2.15 倍〔自算〕分子＝数控机床 426,000.00 万元 [S1]｜分母＝功能部件 198,000.00 万元 [S1]",
    "- 机床业务收入约为功能部件的 2.15 倍〔自算〕分子＝数控机床 426,000.00 万元 [S1]｜分母＝功能部件 198,000.00 万元"
    "「功能部件业务实现营业收入 198,000.00 万元」〔锚：2025 年年报·第 46 页〕[S1]")


def _codes(text):
    findings, _stats = check_text(text)
    return findings, set(c for c, _l, _m in findings)


def selftest():
    cases = (
        ("好样应零发条", GOOD, set()),
        ("形制：节标题写错（驱动因素）", BAD_FORM, {"ER-FORM"}),
        ("形制：风险清单空节", BAD_EMPTY, {"ER-FORM"}),
        ("锚：发现行没挂原句与锚", BAD_ANCHOR, {"ER-ANCHOR"}),
        ("红线：买入评级＋目标价", BAD_REDLINE, {"ER-REDLINE"}),
        ("自算：表内比率原句里找不到", BAD_NOSELF, {"ER-NOSELF"}),
        ("边界：写成已出财报的四期差异", BAD_SCOPE, {"ER-SCOPE"}),
        ("反证：非百分数自算未标〔自算〕→ 不发", OK_SELF_DECLARED, set()),
        ("反证：[待人工] 整句成立 → 不发", OK_HUMAN, set()),
        ("反证：[待人工] 只豁免自己那句，后半句照样发", BAD_HUMAN_HALF, {"ER-REDLINE"}),
        ("自算：分母跨过引号借下一处锚", BAD_SELF_BORROW, {"ER-ANCHOR"}),
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
    ap = argparse.ArgumentParser(description="个股深度研究稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="研究稿 .md 路径")
    ap.add_argument("--selftest", action="store_true", help="跑包内夹具自检")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.path:
        ap.print_help()
        return 3
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
