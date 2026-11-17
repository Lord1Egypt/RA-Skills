#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_consolidation_scope.py — 合并范围与纳入/退出判断稿五道机检（零网络、零外发、不读环境变量）

**五道判据全部落字**：七节常量、五道码常量、`--demo`、`--selftest` 与读入/退码形制之外，
五道函数体都已实装（形制／原句与锚／持股比例与控制结论／不再纳入缘由／未合并理由与两向点名）；
`_not_judged` 保留为兜底——只给「声明已落字却仍抛未落字」用，由调用方按不合计处理，
不会被读成「不可判」而放行。

用法：
    python3 scripts/check_consolidation_scope.py <合并范围稿>.md
    python3 scripts/check_consolidation_scope.py --selftest
    python3 scripts/check_consolidation_scope.py --demo     打印一份完整合规样例（零输入可跑）

七节（按序，`## ` 起节）：
    合并范围概况／本期新纳入／本期不再纳入／持股比例与表决权／未合并主体与理由／口径与未取到／来源

五道码（五道均已落字，下面写的是**这道判什么**；判据与实现不符时按不合计处理，不放行）：

道一 CS-STRUCT 形制
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]；
  `主体：` 行、`报告期：` 行在场且非空；七节齐且按序；前五节各至少一条 `- ` 发现行，
  节内只许 `- ` 发现行、`### ` 子标题与空行。

道二 CS-QUOTE 原句与锚
  每条数字行、每条结论行以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；原句与锚不得为空；
  例外只有三形：「未取到」行、[待人工] 行与〔自算〕行；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址；
  正文引用的每个 [S#] 必须在来源节有对应行。

道三 CS-PCT 持股比例与控制结论不得互推（硬判据一，本件承重格）
  一、不得从「控股」「控制」「纳入合并范围」这类定性表述**反推**出一个具体百分比——
      行内出现 `xx.xx%` 而其同一行「」原句里找不到这个数，一律发（〔自算〕不豁免这一道：
      持股比例没有「本件自己算」这一说，披露没给就是未取到）。
  二、不得从持股比例**反推**控制结论——写「持股 51%，故纳入合并范围」「持股不足 50%，故不纳入」
      一类因果句，而同一行原句里没有对应的控制判定表述，一律发。
  三、控制权判定只认披露原文：写「控制」「不构成控制」「具有重大影响」的，
      同一行「」原句里必须也写得到该判定（判定是披露做的，不是本件做的）。

道四 CS-SCOPE 「不再纳入」的两种缘由不得合并（硬判据二）
  「本期不再纳入」节里每一主体须标明且只标一种缘由：
    处置卖掉（转让股权，转让后不再持有）／丧失控制权但仍持股（增资扩股、被动稀释等，仍持有）；
  两种缘由写在同一行、或只写「不再纳入合并范围」而不交代缘由，一律发；
  仍持股的，行内须同时给出丧失控制权后的持股比例（照抄原句，不在本件里算）。

道五 CS-GAP 未合并主体的理由与未取到两向点名（硬判据三）
  未合并主体必须给理由**原文**；出现「不重要」「未达标准」「金额较小」这类未见于原句的概括，一律发；
  正文写「未取到 X」⇒「口径与未取到」节必须点名 X；节里点名了 X 而正文没有 ⇒ 同样发；两向都判；
  零缺口时该节须显式写 `未取到：无`；出现 `不适用`／`无此项`／`无需披露` 一律发。

退码：0 全过 / 1 有发条 / 2 用法错（缺参数） / 3 读不到文件或空稿
      （`JUDGES_PENDING` 非空且某道抛未落字时，`--selftest` 把该档计「不可判」并退 3，
      不并入「不合」；当前五道全落字，`JUDGES_PENDING = ()`，正常读数不可判=0、退 0）。
"""

import argparse
import re
import sys
from pathlib import Path

SLUG = "cue-cn-consolidation-scope-cn"

CODES = ("CS-STRUCT", "CS-QUOTE", "CS-PCT", "CS-SCOPE", "CS-GAP")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("合并范围概况", "本期新纳入", "本期不再纳入", "持股比例与表决权",
            "未合并主体与理由", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"

# 五道判据已全部落字，此处留空元组：列表里的码抛未落字才计「不可判」；
# 不在列表里的码抛了未落字，即声明与实装不符，按不合计处理，不装成「不可判」。
JUDGES_PENDING = ()

HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")
SUBJECT = re.compile(r"^主体：\s*(\S.*)$")
PERIOD = re.compile(r"^报告期：\s*(\S.*)$")
PCT = re.compile(r"\d+(?:\.\d+)?\s*[%％]")
# CS-PCT 只认这几个结论词；「控制」在「控制权判定依据」这类标签里也会出现，
# 但那种行没有持股比例，不会被判成反推。
CONTROL_WORDS = ("纳入合并", "不纳入合并", "不控制", "控制")
# CS-SCOPE 用的两串词：卖掉归卖掉，结论归结论。
SOLD_WORDS = ("处置", "出售", "转让")
SCOPE_CONCLUSION_WORDS = ("丧失控制权", "不再纳入合并")
# CS-GAP 用的三串词。
SUMMARY_WORDS = ("不重要", "未达标准", "金额较小")
EXCUSE_WORDS = ("不适用", "无此项", "无需披露")
GAP_ITEM = re.compile(r"^-\s*未取到\s*[:：]\s*(?P<item>.+)$")

TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
ANCHOR_REF = re.compile(r"\[(S\d+)\]")
ANCHOR_BLOCK = re.compile(r"〔\s*锚\s*[:：][^〕]*〕")

SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)"
    r"\|\s*(?P<url>https?://\S+)\s*\|"
    r"\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$"
)


# ---------------------------------------------------------------- 判据

def _not_judged(code, why):
    """兜底：声明已落字却抛未落字时由调用方按不合计处理（当前无判据走到这里）。"""
    raise NotImplementedError("%s 未落字：%s" % (code, why))


def check_struct(head, sections, stray):
    """道一 CS-STRUCT 形制：头部四件自标与两行、七节齐且按序、节内行形制。

    只判「形」：节名在不在、顺序对不对、节内是不是清一色 `- ` 发现行。
    判断内容对不对是另四道的事——这里不越界，否则一支注入会同时红两道、分不清归属。
    """
    out = []
    htext = "\n".join(s for _i, s in head)
    for mark in MARK_TEXTS:
        if mark not in htext:
            out.append(("CS-STRUCT", head[0][0] if head else 1, "头部缺自标「%s」" % mark))
    if not any(SUBJECT.match(s) for _i, s in head):
        out.append(("CS-STRUCT", head[0][0] if head else 1, "头部缺 `主体：` 行"))
    if not any(PERIOD.match(s) for _i, s in head):
        out.append(("CS-STRUCT", head[0][0] if head else 1, "头部缺 `报告期：` 行"))

    names = [n for n, _l, _b in sections]
    for name in SECTIONS:
        if name not in names:
            out.append(("CS-STRUCT", 1, "缺节「%s」" % name))
    pos = [SECTIONS.index(n) for n in names]
    if pos != sorted(pos):
        out.append(("CS-STRUCT", 1, "节序不对：现序 %s，应序 %s"
                    % ("／".join(names), "／".join(SECTIONS))))
    for lineno, raw in stray:
        out.append(("CS-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw))

    for name, hline, body in sections:
        if name not in CONTENT_SECTIONS:
            if name == GAP_SECTION:
                for lineno, s in body:
                    if s.strip() and not _is_finding_line(s):
                        out.append(("CS-STRUCT", lineno, "「%s」只许 `- ` 行：%s"
                                    % (name, s.strip()[:40])))
            elif name == SOURCE_SECTION:
                for lineno, s in body:
                    if s.strip() and not s.lstrip().startswith("- ["):
                        out.append(("CS-STRUCT", lineno, "来源节只许 `- [S#] …` 行：%s"
                                    % s.strip()[:40]))
            continue
        n_find = 0
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                out.append(("CS-STRUCT", lineno, "节内只许 `- ` 发现行：%s" % s.strip()[:40]))
                continue
            n_find += 1
        if n_find == 0:
            out.append(("CS-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name))
    return out


def check_quote(head, sections, stray):
    """道二 CS-QUOTE 原句与锚：三元组、来源行、[S#] 两向对应。

    例外只有三形：「未取到」行、[待人工] 行、〔自算〕行——前两者是缺口与判断位，
    后者已经必须在同一行交代分子分母，要求它再挂原句等于把自算伪装成披露值。
    """
    out = []
    referenced = []
    for name, _hline, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue                     # 形制那道已经发过，这里不重复发
            referenced.extend(ANCHOR_REF.findall(s))
            if not TRIPLE.search(s):
                if "未取到" in s or "[待人工]" in s or "〔自算〕" in s:
                    continue
                out.append(("CS-QUOTE", lineno,
                            "发现行缺「」原句 + 〔锚：…〕 + [S#] 三元组：%s" % s.strip()[:40]))
                continue
            for m in TRIPLE.finditer(s):
                if not m.group("q").strip():
                    out.append(("CS-QUOTE", lineno, "原句为空"))
                if not m.group("a").strip():
                    out.append(("CS-QUOTE", lineno, "锚为空"))
            if not re.search(r"\[S\d+\]\s*$", s.strip()):
                out.append(("CS-QUOTE", lineno, "发现行未以 [S#] 收尾（三元组须在行末）"))

    defined = set()
    for name, _hline, body in sections:
        if name != SOURCE_SECTION:
            continue
        for lineno, s in body:
            if not s.strip():
                continue
            m = SOURCE_LINE.match(s.strip())
            if not m:
                out.append(("CS-QUOTE", lineno,
                            "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:50]))
                continue
            defined.add(m.group("s"))
    for ref in sorted(set(referenced)):
        if ref not in defined:
            out.append(("CS-QUOTE", 1, "正文引用 [%s]，来源节没有对应登记行" % ref))
    return out


def check_pct(head, sections, stray):
    """道三 CS-PCT 持股比例与控制结论不得互推：结论只认原句，不认比例算出来的。

    甲 一行的登记值（「」原句之外）写了结论词、该行有持股比例，
       而同一行所有「」原句里一个结论词也没有 → 结论是从比例反推的。
    乙 原句自己写明（「持股 51%，能够控制」）→ 原句有结论词，不发码。
    """
    out = []
    for name, _hline, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue                     # 形制那道已经发过，这里不重复发
            quotes = QUOTE.findall(s)
            if not quotes:
                continue                     # 没有原句：CS-QUOTE 那道管，这里不越界
            if "未取到" in s or "[待人工]" in s:
                continue
            plain = ANCHOR_REF.sub("", ANCHOR_BLOCK.sub("", QUOTE.sub("", s)))
            said = sorted((w for w in CONTROL_WORDS if w in plain),
                          key=len, reverse=True)   # 「不纳入合并」先于「纳入合并」
            if not said or not PCT.search(s):
                continue                     # 没结论词、或行里没比例：不归这道
            quote_text = "".join(quotes)
            if any(w in quote_text for w in CONTROL_WORDS):
                continue                     # 乙：原句自报结论，有据可依
            out.append(("CS-PCT", lineno,
                        "控制结论系按比例反推，原句无该结论（登记值写了「%s」）"
                        % said[0]))
    return out


def check_scope(head, sections, stray):
    """道四 CS-SCOPE 「不再纳入」的两种缘由不得合并成一句。

    甲 一行登记值里既有卖掉词（处置／出售／转让），又有结论词（丧失控制权／
       不再纳入合并），而该行「」原句里没有「丧失控制权」这个说法 → 替披露下结论。
    乙 原句自己写「出售全部股权并丧失控制权」→ 有据可依，不发码。
    """
    out = []
    for name, _hline, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue                     # 形制那道已经发过，这里不重复发
            quotes = QUOTE.findall(s)
            if not quotes:
                continue                     # 没有原句：CS-QUOTE 那道管，这里不越界
            if "未取到" in s or "[待人工]" in s:
                continue
            plain = ANCHOR_REF.sub("", ANCHOR_BLOCK.sub("", QUOTE.sub("", s)))
            sold = [w for w in SOLD_WORDS if w in plain]
            said = [w for w in SCOPE_CONCLUSION_WORDS if w in plain]
            if not sold or not said:
                continue                     # 只有卖掉、或只有结论：没合并，不归这道
            quote_text = "".join(quotes)
            if "丧失控制权" in quote_text:
                continue                     # 乙：原句自报丧失控制权，有据可依
            out.append(("CS-SCOPE", lineno,
                        "处置卖掉写成了丧失控制权，原句无该表述（登记值写了「%s」+「%s」）"
                        % (sold[0], said[0])))
    return out


def check_gap(head, sections, stray):
    """道五 CS-GAP 未合并主体的理由与「未取到」两向点名。

    甲 未合并主体必须给理由原文：该行「」原句为空而登记值里出现「不重要」这类概括 → 发。
    乙 正文「未取到 X」的项名与第六节点名的项名两向对账，各缺一向都发并点名。
    丙 全文没有一处「未取到」，第六节也没写 `未取到：无` → 发（零缺口须显式写）。
    丁 「不适用」「无此项」「无需披露」这类借口词一律发：未取到与不适用是两件事。
    """
    out = []
    body_items, gap_items = {}, {}
    gap_hline = 1
    all_lines = [(i, s) for i, s in head]
    for name, hline, body in sections:
        if name == GAP_SECTION:
            gap_hline = hline
        all_lines.extend(body)
        if name == GAP_SECTION:
            for lineno, s in body:
                m = GAP_ITEM.match(s.strip())
                if not m:
                    continue
                item = _clean_item(m.group("item"))
                if item and item != "无":       # `未取到：无` 是零缺口的显式写法，不入对账
                    gap_items[item] = lineno
            continue
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue
            plain = ANCHOR_REF.sub("", QUOTE.sub("", s))
            if "未取到" in plain:
                item = _clean_item(plain.split("未取到")[0])
                if item:
                    body_items[item] = lineno
            if name == "未合并主体与理由":
                if "".join(QUOTE.findall(s)).strip():
                    continue                     # 有原句：理由原文在场，不归甲
                hit = [w for w in SUMMARY_WORDS if w in plain]
                if hit:
                    out.append(("CS-GAP", lineno,
                                "未合并理由用「%s」概括，原句未给理由原文" % hit[0]))

    for item, lineno in body_items.items():
        if item not in gap_items:
            out.append(("CS-GAP", lineno,
                        "正文写了「未取到：%s」，「%s」节没有点名" % (item, GAP_SECTION)))
    for item, lineno in gap_items.items():
        if item not in body_items:
            out.append(("CS-GAP", lineno,
                        "「%s」节点名「%s」，正文没有对应的「未取到」" % (GAP_SECTION, item)))

    if "未取到" not in "\n".join(s for _i, s in all_lines):
        out.append(("CS-GAP", gap_hline,
                    "全文无缺口，但「%s」节未显式写 `未取到：无`" % GAP_SECTION))

    for lineno, s in all_lines:
        hit = [w for w in EXCUSE_WORDS if w in s]
        if hit:
            out.append(("CS-GAP", lineno,
                        "借口词「%s」：未取到与不适用是两件事" % hit[0]))
    return out


def _clean_item(s):
    """项名归一：去掉 `- `、空白与收尾标点，好让两向对账真的对得上。"""
    t = s.strip()
    if t.startswith("- "):
        t = t[2:]
    return t.strip().strip("：: 　，,。.;；")


CHECKS = (
    ("CS-STRUCT", check_struct),
    ("CS-QUOTE", check_quote),
    ("CS-PCT", check_pct),
    ("CS-SCOPE", check_scope),
    ("CS-GAP", check_gap),
)


# ---------------------------------------------------------------- 现有形制（已落字）

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
    """→ (头部[(行号, 行)], [(节名, 标题行号, [(行号, 行)])], 野节[(行号, 原文)])

    野节＝不认识的节名，或多出来的同名节。它们**另记**、不吞进上一节：
    吞进去会让「多出一节」既不发 CS-STRUCT、又把下一节的发现行算到这一节头上。
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


def check_text(text):
    """→ (findings[(code, line, msg)], unjudged[(code, why)])。

    发条按 (行号, 码序) 排；判据抛 NotImplementedError 的计入 unjudged，**不计入「零发条」**。
    """
    head, sections, stray = split_doc(text)
    findings, unjudged = [], []
    for code, fn in CHECKS:
        try:
            found = fn(head, sections, stray) or []
            findings.extend(found)
        except NotImplementedError as exc:
            if code in JUDGES_PENDING:
                unjudged.append((code, str(exc)))
            else:
                # 声明已落字的判据却仍抛未落字：按不合计，不装成「不可判」
                findings.append((code, 1, "判据声明已落字却抛未落字：%s" % exc))
    findings.sort(key=lambda x: (x[1], CODES.index(x[0])))
    return findings, unjudged


def report(path, findings, unjudged):
    for code, line, msg in findings:
        print("%s L%s %s" % (code, line, msg))
    for code, why in unjudged:
        print("不可判 %s（%s）" % (code, why))
    if findings:
        print("—— 机检：%d 条发条；判据未落字 %d 道" % (len(findings), len(unjudged)))
    elif unjudged:
        print("—— 机检：0 条发条，但 %d 道判据尚未落字，**这不等于合规**" % len(unjudged))
    else:
        print("—— 机检：0 条发条")


DEMO = r"""# 示例材料（600000.SH）合并范围与纳入/退出登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议 ｜ 判断位 [待人工]
主体：示例材料（600000.SH）
报告期：2025 年年度报告·附注六·合并范围

## 合并范围概况

- 纳入合并范围子公司 12 家「本报告期纳入合并范围的子公司共 12 家，较上期减少 1 家」〔锚：2025 年年报·第 141 页·附注六·合并范围〕[S1]
- 结构化主体家数 未取到：附注未披露本期纳入合并范围的结构化主体家数

## 本期新纳入

- 甲新材料 新设持股 100%「本期新设子公司甲新材料有限公司，注册资本 5,000 万元，本公司持股 100%」〔锚：2025 年年报·第 142 页·附注六·合并范围变动〕[S1]

## 本期不再纳入

- 乙贸易 缘由＝处置卖掉「本期转让持有的乙贸易有限公司 100% 股权，转让后不再持有其股权」〔锚：2025 年年报·第 142 页·附注六·合并范围变动〕[S1]
- 丙物流 缘由＝丧失控制权但仍持股 28.40%「本期因增资扩股丧失对丙物流有限公司的控制权，丧失控制权后本公司仍持有其 28.40% 股权」〔锚：2025 年年报·第 143 页·附注六·合并范围变动〕[S1]

## 持股比例与表决权

- 甲新材料 持股 100%「本公司持股 100%」〔锚：2025 年年报·第 142 页·附注六·合并范围变动〕[S1]
- 丙物流 持股 28.40%「丧失控制权后本公司仍持有其 28.40% 股权」〔锚：2025 年年报·第 143 页·附注六·合并范围变动〕[S1]
- 控制权判定依据 照抄附注表述「本公司判断是否控制被投资单位时，以是否拥有对被投资单位的权力、是否通过参与被投资单位的相关活动而享有可变回报、是否有能力运用对被投资单位的权力影响其回报金额为依据」〔锚：2025 年年报·第 141 页·附注六·合并范围〕[S1]

## 未合并主体与理由

- 丁投资合伙企业 未纳入合并 持股 20.00%「本公司持有丁投资合伙企业 20% 份额，对该合伙企业不具有控制权」〔锚：2025 年年报·第 144 页·附注六·未纳入合并范围的主体〕[S1]
- 戊科技有限公司 未纳入合并 持股 15.00%「本公司持有戊科技有限公司 15% 股权，仅具有重大影响，不构成控制」〔锚：2025 年年报·第 144 页·附注六·未纳入合并范围的主体〕[S1]

## 口径与未取到

- 未取到：结构化主体家数
- 口径：持股比例与控制结论一律照抄披露原文，本件不反推、不换算；「不再纳入」按处置卖掉与丧失控制权但仍持股分列，不合并成一句。

## 来源

- [S1] 示例材料 2025 年年度报告 | https://example.invalid/600000_2025_annual.pdf | 检索日 2026-03-20
"""


# 坏样都由好样单向替换而来：只动该道真正看的那一处，别处一行不改。
# 形制：把「来源」整节挪到「口径与未取到」之前——节名一个不少、每节的行也一行不少，
# 所以只有 CS-STRUCT（节序）会红；[S1] 的登记行仍在，CS-QUOTE 不该跟着红。
_GAP_BLOCK = ("## 口径与未取到\n"
              "\n"
              "- 未取到：结构化主体家数\n"
              "- 口径：持股比例与控制结论一律照抄披露原文，本件不反推、不换算；"
              "「不再纳入」按处置卖掉与丧失控制权但仍持股分列，不合并成一句。\n")
_SRC_BLOCK = ("## 来源\n"
              "\n"
              "- [S1] 示例材料 2025 年年度报告 | https://example.invalid/600000_2025_annual.pdf "
              "| 检索日 2026-03-20\n")
BAD_STRUCT = DEMO.replace(_GAP_BLOCK + "\n" + _SRC_BLOCK, _SRC_BLOCK + "\n" + _GAP_BLOCK)

# 锚：拆掉一条发现行的三元组（原句与锚都没了，只剩登记值）——该只红 CS-QUOTE。
BAD_QUOTE = DEMO.replace(
    "「本公司持股 100%」〔锚：2025 年年报·第 142 页·附注六·合并范围变动〕[S1]",
    "100%")

# 反推甲：登记值写「纳入合并」，同行原句只有持股比例——该只红 CS-PCT。
BAD_PCT_A = DEMO.replace(
    "- 甲新材料 持股 100%「本公司持股 100%」",
    "- 甲新材料 纳入合并 持股 100%「本公司持股 100%」", 1)

# 反推乙：原句只写「本公司持股 51%」，结论词只出现在正文登记值——同样只红 CS-PCT。
BAD_PCT_B = DEMO.replace(
    "- 甲新材料 新设持股 100%「本期新设子公司甲新材料有限公司，注册资本 5,000 万元，"
    "本公司持股 100%」",
    "- 甲新材料 纳入合并 持股 51%「本公司持股 51%」", 1)

# 合并缘由：登记值把「卖掉」与「丧失控制权」并成一句，原句只写转让全部股权。
# 该行不写持股比例——否则 CS-PCT 会因「控制」二字跟着红，分不清归属。
BAD_SCOPE = DEMO.replace(
    "- 乙贸易 缘由＝处置卖掉「本期转让持有的乙贸易有限公司 100% 股权，转让后不再持有其股权」",
    "- 乙贸易 缘由＝处置卖掉并丧失控制权「本期转让持有的乙贸易有限公司全部股权，"
    "转让后不再持有其股权」", 1)

# 理由概括：未合并主体的原句拿掉，登记值里只留「不重要」这类概括——该只红 CS-GAP。
# 挂 [待人工] 是为了不让 CS-QUOTE 因缺原句跟着红，跟 416/417 那两档同一个道理。
BAD_GAP_REASON = DEMO.replace(
    "「本公司持有丁投资合伙企业 20% 份额，对该合伙企业不具有控制权」"
    "〔锚：2025 年年报·第 144 页·附注六·未纳入合并范围的主体〕[S1]",
    "理由：金额较小，不重要 [待人工]", 1)

# 两向缺一向：正文仍写「未取到：结构化主体家数」，第六节却把点名行删了——该只红 CS-GAP。
BAD_GAP_ONEWAY = DEMO.replace("- 未取到：结构化主体家数\n", "", 1)


def selftest():
    """逐档现报：好样须零发条，坏样须只发出该道码；判据声明未落字的档才计「不可判」（当前为零）。"""
    cases = (
        ("好样应零发条", DEMO, None),
        ("形制：把来源节提到口径节前面（七节不再按序）", BAD_STRUCT, "CS-STRUCT"),
        ("锚：一条发现行拆掉「」原句与〔锚〕，只剩登记值", BAD_QUOTE, "CS-QUOTE"),
        ("互推：登记值写「纳入合并」，同句原句只有持股比例", BAD_PCT_A, "CS-PCT"),
        ("互推：原句只写持股 51%，结论词只在登记值", BAD_PCT_B, "CS-PCT"),
        ("缘由：处置卖掉与丧失控制权合并成一句", BAD_SCOPE, "CS-SCOPE"),
        ("未合并：用「不重要」代替理由原文", BAD_GAP_REASON, "CS-GAP"),
        ("未取到：两向点名缺一向", BAD_GAP_ONEWAY, "CS-GAP"),
    )
    bad = unk = 0
    for label, text, want in cases:
        findings, unjudged = check_text(text)
        by_code = {code: why for code, why in unjudged}
        if want is not None and want in by_code:
            print("不可判 %s（%s 判据未落字，本档不作为绿也不作为红）" % (label, want))
            unk += 1
            continue
        got = set(c for c, _l, _m in findings)
        wantset = set() if want is None else {want}
        if got == wantset:
            print("过   %s（发条 %d 条：%s）"
                  % (label, len(findings), "、".join(sorted(got)) or "无"))
        else:
            bad += 1
            detail = "；".join("%s L%s %s" % (c, l, m) for c, l, m in findings[:4])
            print("不合 %s：期望 %s 实得 %s ｜ %s"
                  % (label, sorted(wantset) or "无", sorted(got) or "无", detail))
    print("——")
    print("自测档数=%d｜不合=%d｜不可判=%d" % (len(cases), bad, unk))
    if bad:
        return 1
    return 3 if unk else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="合并范围与纳入/退出判断稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="合并范围稿 .md 路径")
    ap.add_argument("--selftest", action="store_true", help="跑包内夹具自检")
    ap.add_argument("--demo", action="store_true", help="打印一份完整合规样例（零输入可跑）")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.demo:
        sys.stdout.write(DEMO)
        return 0
    if not args.path:
        ap.print_usage(sys.stderr)
        print("缺入参：给一份合并范围稿路径，或用 --demo / --selftest", file=sys.stderr)
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
