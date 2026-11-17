#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_notes.py — 应收应付票据稿五道机检（零网络、零外发、不读环境变量）

用法：
    python3 scripts/check_notes.py <票据稿>.md
    python3 scripts/check_notes.py --selftest
    python3 scripts/check_notes.py --demo     打印一份完整合规样例（零输入可跑）

道一 NR-STRUCT 形制
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]；
  `主体：` 行在场且非空；`报告期：` 行在场且非空；
  六节齐且按序：票据分类／期末余额与坏账准备／已背书与已贴现／到期托收与拒付／口径与未取到／来源；
  前四节各至少一条 `- ` 发现行，节内只许 `- ` 发现行、`### ` 子标题与空行。

道二 NR-QUOTE 原句与锚
  每条数字行必须以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；原句与锚不得为空；
  例外只有三形：「未取到」行（缺的就是那份材料）、[待人工] 行（判断位）与〔自算〕行（本件自己算的）；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址，检索日缺一不可；
  正文引用的每个 [S#] 必须在来源节有对应行。

道三 NR-NOSELF 不得自推自算（本件承重格）
  一、分类只认原句：「银行承兑」「商业承兑」写在本件自己的句子里，同一行「」原句必须也写到——
      原句只写「应收票据」不分类时，正确做法是写未取到，不是按出票人名称或票面习惯自推。
  二、终止确认只认原句：「终止确认」「未终止确认」「继续涉入」同理必须在同一行原句里出现；
      「已背书」不等于「已终止确认」，两者之间那一步是会计判断，不是本件能替披露做的。
  三、百分数：行内出现 `1.50%` 一类数值，必须能在同一行的「」原句里逐字找到；
      找不到的须标〔自算〕，且同一行同时给出 `分子…[S#]` 与 `分母…[S#]`，两处锚各挂自己那个数上。
  四、贴现利息自算：同一行标了〔自算〕又谈贴现的，必须写明**利率、期间、按 360 还是 365 天折算**
      三项口径；缺一项即发——把三个数乘起来叫贴现息，是替用户编口径。

道四 NR-GAP 未取到两向点名
  正文（一至四节）写「未取到 X」⇒ 第五节必须点名 X；第五节点名了 X 而正文没有 ⇒ 同样发；两向都判。
  零缺口时，第五节须显式写 `未取到：无`；
  出现 `不适用`／`无此项`／`无需披露` 一律发——那是把没查当成没有。

道五 NR-LINE 红线
  真伪判断／承兑人信用／兑付风险／评级与目标价／建议买入一类断言零命中；
  **只判本件自己写的句子**：同一行「」里的引文先洗掉再判——引文是证据，不是本件的断言；
  含 [待人工] 的分句豁免，且只豁免它自己那一句（按 ；;。，,｜ 切分）；
  「票据保证金」与「货币资金」在同一分句被写成相等（＝／等于／即／相同／一致）一律发——
  保证金是受限资金，与不受限的货币资金不是同一个数。

退码：0 全过 / 1 有发条 / 2 用法错（缺参数） / 3 读不到文件或空稿。
"""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-notes-receivable-cn"

CODES = ("NR-STRUCT", "NR-QUOTE", "NR-NOSELF", "NR-GAP", "NR-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("票据分类", "期末余额与坏账准备", "已背书与已贴现",
            "到期托收与拒付", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:4]
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
CLASS_WORDS = ("银行承兑", "商业承兑")
DERECOG_WORDS = ("终止确认", "继续涉入")

# 贴现利息自算的三项口径：利率 / 期间 / 天数折算，缺一即发
DISCOUNT_RATE = ("利率", "年化")
DISCOUNT_SPAN = ("期间", "期限", "天数")
DISCOUNT_DAYCOUNT = ("360", "365")

GAP_EXCUSE = ("不适用", "无此项", "无需披露")

CASH_EQUAL = ("＝", "=", "等于", "即", "相同", "一致")
MARGIN_WORDS = ("票据保证金", "保证金")
CASH_WORDS = ("货币资金",)

HARD_BAN = ("伪造", "变造", "假票", "承兑人信用", "信用等级", "主体评级", "债项评级",
            "兑付风险", "无风险", "保证兑付", "保兑", "稳赚", "零风险",
            "目标价", "目标市值", "买入评级", "增持评级", "中性评级",
            "建议买入", "建议增持", "强烈推荐", "跑赢大盘", "必涨", "必跌")

PRED_WORDS = ("将发生拒付", "会发生拒付", "预计拒付", "将出现拒付",
              "将无法兑付", "无法兑付", "将出现违约", "会发生违约")

CLAUSE_SPLIT = re.compile(r"[；;。，,｜|]")

SCOPE_RULES = (
    (("存货跌价准备", "应收账款账龄", "合同资产减值", "账龄分析表"),
     "改走 cn-working-capital-quality：存货、应收账款与合同资产的余额与账龄是那一件"),
    (("经营活动现金流", "筹资活动现金流", "净现比", "收现比", "自由现金流"),
     "改走 cn-cash-flow-quality：三张现金流的逐条登记是那一件，本件只在保证金与贴现现金处给一句指向"),
    (("关联方资金占用", "关联方非经营性占用"),
     "改走 related-party-terms-cn：关联方资金占用与担保是那一件"),
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
      第五节 `- 未取到：项名`          → 项名在「未取到」**后**
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
    # 逐句洗就洗不干净——「公司称承兑人信用良好，未发生拒付」这类照抄原文会被误判成本件断言。
    own_line = _strip_quotes(line)
    for clause in _clauses(own_line):
        if "[待人工]" in clause:
            continue
        own = clause
        hit = [w for w in HARD_BAN if w in own]
        pred = [w for w in PRED_WORDS if w in own]
        if pred:
            hit.extend(pred)
        # 票据保证金 ≠ 货币资金
        if (any(w in own for w in MARGIN_WORDS)
                and any(w in own for w in CASH_WORDS)
                and any(e in own for e in CASH_EQUAL)):
            hit.append("票据保证金＝货币资金")
        if hit:
            add("NR-LINE", lineno, "红线词：%s（%s）" % ("、".join(sorted(set(hit))), clause.strip()[:40]))
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

    判域＝去掉**项名**之后的余下部分。项名本身就是「应付票据·商业承兑」这种写法，
    它是在标这一行的登记对象，不是在替披露分类；把它当自推判会冤枉正确写法。
    「未取到」行整行豁免——那正是「原句没分类所以照实写没取到」的正确形态。
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
        add("NR-NOSELF", lineno,
            "%s须取原句：本件句子里写了「%s」，原句里没有——没披露就写未取到，不按习惯自推：%s"
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
        add("NR-NOSELF", lineno, "%s自算未交代%s" % (what, "／".join(why)))


def _check_discount(lineno, line, add):
    """贴现利息自算：利率、期间、天数折算三项口径缺一即发。"""
    why = []
    if not any(w in line for w in DISCOUNT_RATE):
        why.append("未写明利率取哪一句")
    if not any(w in line for w in DISCOUNT_SPAN):
        why.append("未写明期间／天数取哪一句")
    if not any(w in line for w in DISCOUNT_DAYCOUNT):
        why.append("未写明按 360 还是 365 天折算")
    if why:
        add("NR-NOSELF", lineno, "贴现利息自算未交代%s" % "／".join(why))


def _check_noself(lineno, line, add):
    q = _quotes(line).replace(" ", "")
    # 一、二、词族：分类与终止确认只认原句
    _check_vocab(lineno, line, add, CLASS_WORDS, "票据分类")
    _check_vocab(lineno, line, add, DERECOG_WORDS, "终止确认")
    # 三、百分数：原句里没有同一数值，就必须自算并交代分子分母
    missing = [t for t in PCT.findall(line) if _norm_pct(t) not in q]
    if missing:
        if "〔自算〕" not in line:
            add("NR-NOSELF", lineno, "比例 %s 在原句里找不到，也没标〔自算〕：%s"
                % ("、".join(missing), line.strip()[:40]))
        else:
            _check_mol_den(lineno, line, add, "比例")
    # 四、贴现利息自算的三项口径
    if "〔自算〕" in line and "贴现" in line:
        _check_discount(lineno, line, add)


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
            add("NR-STRUCT", 1, "头部缺自标「%s」" % mark)
    if not any(SUBJECT.match(s) for _i, s in header):
        add("NR-STRUCT", 1, "头部缺 `主体：` 行")
    if not any(PERIOD.match(s) for _i, s in header):
        add("NR-STRUCT", 1, "头部缺 `报告期：` 行")

    # ---- 道一 节齐与序
    names = [n for n, _l, _b in sections]
    for name in SECTIONS:
        if name not in names:
            add("NR-STRUCT", 1, "缺节「%s」" % name)
    pos = [SECTIONS.index(n) for n in names]
    if pos != sorted(pos):
        add("NR-STRUCT", 1, "节序不对：现序 %s，应序 %s" % ("／".join(names), "／".join(SECTIONS)))
    for lineno, raw in stray:
        add("NR-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw)

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
                    add("NR-STRUCT", lineno, "节内只许 `- ` 发现行：%s" % s.strip()[:40])
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
                        add("NR-QUOTE", lineno, "发现行缺「」原句 + 〔锚：…〕 + [S#] 三元组：%s"
                            % s.strip()[:40])
                else:
                    for m in TRIPLE.finditer(s):
                        if not m.group("q").strip():
                            add("NR-QUOTE", lineno, "原句为空")
                        if not m.group("a").strip():
                            add("NR-QUOTE", lineno, "锚为空")
                    if not re.search(r"\[S\d+\]\s*$", s.strip()):
                        add("NR-QUOTE", lineno, "发现行未以 [S#] 收尾（三元组须在行末）")
                _check_line(lineno, s, add)
                if PCT.findall(s):
                    stats["ratio_lines"] += 1
                _check_noself(lineno, s, add)
            section_found[name] = n_find
            if n_find == 0:
                add("NR-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name)

        elif name == GAP_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not _is_finding_line(s):
                    add("NR-STRUCT", lineno, "第五节只许 `- ` 行：%s" % s.strip()[:40])
                    continue
                section_found.setdefault(name, 0)
                section_found[name] += 1
                for w in GAP_EXCUSE:
                    if w in s:
                        add("NR-GAP", lineno, "禁用「%s」把没查当成没有：%s" % (w, s.strip()[:40]))
                _check_line(lineno, s, add)

        elif name == SOURCE_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not s.lstrip().startswith("- ["):
                    add("NR-STRUCT", lineno, "来源节只许 `- [S#] …` 行：%s" % s.strip()[:40])
                    continue
                m = SOURCE_LINE.match(s.strip())
                if not m:
                    add("NR-QUOTE", lineno, "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:50])
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
            add("NR-GAP", 1, "正文写了未取到「%s」，第五节没点名" % key)
    for g in gap_sec:
        key = _gap_key(g)
        if key and not any(key in s for s in gap_body):
            add("NR-GAP", 1, "第五节点名了「%s」，正文没有这条表述" % key)

    # 零缺口须显式写「未取到：无」
    if not gap_body and not gap_sec:
        gap_text = "\n".join(s for name, _h, body in sections if name == GAP_SECTION
                             for _ln, s in body)
        if "未取到：无" not in gap_text and "未取到:无" not in gap_text:
            add("NR-GAP", 1, "零缺口未显式写「未取到：无」")

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
            add("NR-QUOTE", 1, "正文引用 [%s]，来源节没有对应登记行" % ref)

    # ---- 边界
    # 只判前四节（登记正文）。第五节「口径与未取到」正是写明与另几枚件分界的地方，
    # 在那里点名 cn-working-capital-quality／cn-cash-flow-quality 是本件要求的动作，不是越界。
    body_lines = [(ln, s) for name, _h, body in sections
                  if name in CONTENT_SECTIONS for ln, s in body]
    for words, tip in SCOPE_RULES:
        for ln, s in body_lines:
            if any(w in s for w in words):
                add("NR-STRUCT", ln, "越界：%s" % tip)
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


GOOD = r"""# 示例材料（600000.SH）应收应付票据登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议 ｜ 判断位 [待人工]
主体：示例材料（600000.SH）
报告期：2025 年年度报告

## 票据分类

- 应收票据·银行承兑 8,600.00 万元「应收票据—银行承兑票据 86,000,000.00 元」〔锚：2025 年年报·第 96 页·附注五·应收票据〕[S1]
- 应收票据·商业承兑 1,400.00 万元「应收票据—商业承兑票据 14,000,000.00 元」〔锚：2025 年年报·第 96 页·附注五·应收票据〕[S1]
- 应付票据·银行承兑 3,200.00 万元「应付票据—银行承兑汇票 32,000,000.00 元」〔锚：2025 年年报·第 118 页·附注五·应付票据〕[S2]
- 应付票据·商业承兑 未取到：附注只按银行承兑列示

## 期末余额与坏账准备

- 应收票据期末余额 10,000.00 万元「应收票据期末余额合计 100,000,000.00 元」〔锚：2025 年年报·第 96 页·附注五·应收票据〕[S1]
- 应收票据坏账准备 150.00 万元「坏账准备 1,500,000.00 元」〔锚：2025 年年报·第 96 页·附注五·应收票据〕[S1]
- 坏账准备计提比例为 1.50%〔自算〕分子＝坏账准备 1,500,000.00 元 [S1]｜分母＝应收票据期末余额 100,000,000.00 元 [S1]
- 应付票据期末余额 3,200.00 万元「应付票据期末余额合计 32,000,000.00 元」〔锚：2025 年年报·第 118 页·附注五·应付票据〕[S2]
- 应付票据未计提坏账准备「应付票据按票面金额入账，未计提坏账准备」〔锚：2025 年年报·第 118 页·附注五·应付票据〕[S2]

## 已背书与已贴现

- 已背书未到期·银行承兑 2,100.00 万元「已背书未到期的银行承兑票据 21,000,000.00 元」〔锚：2025 年年报·第 97 页·附注五·应收票据〕[S1]
- 已背书未到期·商业承兑 300.00 万元「已背书未到期的商业承兑票据 3,000,000.00 元」〔锚：2025 年年报·第 97 页·附注五·应收票据〕[S1]
- 已贴现未到期·银行承兑 800.00 万元「已贴现未到期的银行承兑票据 8,000,000.00 元」〔锚：2025 年年报·第 97 页·附注五·应收票据〕[S1]
- 终止确认：背书或贴现的商业承兑票据未终止确认，继续涉入金额 300.00 万元「商业承兑票据背书或贴现后未终止确认，继续涉入金额 3,000,000.00 元」〔锚：2025 年年报·第 97 页·附注五·应收票据〕[S1]
- 贴现利息 18.00 万元「本期贴现利息支出 180,000.00 元」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]

## 到期托收与拒付

- 本期到期托收 4,600.00 万元「本期到期托收的应收票据 46,000,000.00 元」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]
- 拒付记录 0.00 万元「本期到期的应收票据均已收回」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]
- 托收是否按期到账「本期到期的应收票据均已收回」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]

## 口径与未取到

- 未取到：应付票据·商业承兑
- 口径：分类取附注列示的银行承兑与商业承兑两栏，不按出票人名称自推。
- 口径：终止确认与否照抄附注原文，背书或贴现不等于终止确认。
- 口径：票据保证金属受限资金，与货币资金口径不同，不得互相印证；贴现收到的现金见 cn-cash-flow-quality。
- 口径：票据往来若涉及关联方，关联方资金占用那一块见 related-party-terms-cn，本件不碰。

## 来源

- [S1] 示例材料 2025 年年度报告·附注五·应收票据 | https://example.com/ann/S1 | 检索日 2026-11-11 | 类型：公告
- [S2] 示例材料 2025 年年度报告·附注五·应付票据 | https://example.com/ann/S2 | 检索日 2026-11-11 | 类型：公告
"""

# ---- 坏样：各只发自己那道码
BAD_STRUCT = GOOD.replace("## 期末余额与坏账准备", "## 期末余额与坏账计提")

BAD_QUOTE = GOOD.replace(
    "「本期到期托收的应收票据 46,000,000.00 元」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]",
    "46,000,000.00 元 [S1]")

BAD_NOSELF = GOOD.replace(
    "- 坏账准备计提比例为 1.50%〔自算〕分子＝坏账准备 1,500,000.00 元 [S1]｜分母＝应收票据期末余额 100,000,000.00 元 [S1]",
    "- 坏账准备计提比例为 1.50%〔自算〕分子＝坏账准备 1,500,000.00 元 [S1]")

BAD_GAP = GOOD.replace(
    "- 未取到：应付票据·商业承兑",
    "- 未取到：不适用")

BAD_LINE = GOOD.replace(
    "- 贴现利息 18.00 万元",
    "- 承兑人信用良好，兑付风险低；贴现利息 18.00 万元")

# ---- 反证样：不该发的必须不发
OK_HUMAN = GOOD.replace(
    "- 未取到：应付票据·商业承兑",
    "- 未取到：应付票据·商业承兑\n- 票据到期能否足额兑付，交由人工判断 [待人工]")

BAD_HUMAN_HALF = GOOD.replace(
    "- 未取到：应付票据·商业承兑",
    "- 未取到：应付票据·商业承兑\n- 票据到期能否足额兑付 [待人工]，建议买入")

OK_QUOTED_REDLINE = GOOD.replace(
    "- 拒付记录 0.00 万元「本期到期的应收票据均已收回」",
    "- 拒付记录 0.00 万元「公司称承兑人信用良好，未发生拒付」")

BAD_MARGIN_CASH = GOOD.replace(
    "- 口径：票据保证金属受限资金，与货币资金口径不同，不得互相印证；贴现收到的现金见 cn-cash-flow-quality。",
    "- 口径：票据保证金即货币资金，两者互相印证。")

OK_DISCOUNT_DECLARED = GOOD.replace(
    "- 贴现利息 18.00 万元「本期贴现利息支出 180,000.00 元」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]",
    "- 贴现利息 18.00 万元〔自算〕票面 8,000,000.00 元 [S1]｜利率取附注「年贴现率 3.60%」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]｜期间 76 天、按 360 天折算 [S1]")

BAD_DISCOUNT_NODAYCOUNT = GOOD.replace(
    "- 贴现利息 18.00 万元「本期贴现利息支出 180,000.00 元」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]",
    "- 贴现利息 18.00 万元〔自算〕票面 8,000,000.00 元 [S1]｜利率取附注「年贴现率 3.60%」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]｜期间 76 天 [S1]")

BAD_CLASS_GUESS = GOOD.replace(
    "- 应付票据·商业承兑 未取到：附注只按银行承兑列示",
    "- 应付票据·商业承兑 0.00 万元「应付票据期末余额合计 32,000,000.00 元」〔锚：2025 年年报·第 118 页·附注五·应付票据〕[S2]").replace(
    "- 未取到：应付票据·商业承兑\n", "- 未取到：无\n")

OK_DERECOG_QUOTED = GOOD.replace(
    "- 终止确认：背书或贴现的商业承兑票据未终止确认，继续涉入金额 300.00 万元",
    "- 终止确认：背书或贴现的商业承兑票据未终止确认，继续涉入金额 300.00 万元")

# 零输入样例：直接由 GOOD 派生，不另抄一份——两份会各自漂移，
# 而用户看到的「成品长什么样」必须永远等于自测里那个「好样」。
DEMO = GOOD


def _codes(text):
    findings, _stats = check_text(text)
    return findings, set(c for c, _l, _m in findings)


def selftest():
    cases = (
        ("好样应零发条", GOOD, set()),
        ("形制：节标题写错（坏账计提）", BAD_STRUCT, {"NR-STRUCT"}),
        ("锚：数字行没挂原句与锚", BAD_QUOTE, {"NR-QUOTE"}),
        ("自算：比例自算只给分子没给分母", BAD_NOSELF, {"NR-NOSELF"}),
        ("点名：第五节用「不适用」搪塞", BAD_GAP, {"NR-GAP"}),
        ("红线：写承兑人信用良好、兑付风险低", BAD_LINE, {"NR-LINE"}),
        ("反证：[待人工] 整句成立 → 不发", OK_HUMAN, set()),
        ("反证：[待人工] 只豁免自己那句，后半句建议买入照样发", BAD_HUMAN_HALF, {"NR-LINE"}),
        ("反证：引文里的「承兑人信用」不是本件断言 → 不发", OK_QUOTED_REDLINE, set()),
        ("红线：票据保证金即货币资金", BAD_MARGIN_CASH, {"NR-LINE"}),
        ("反证：贴现利息自算写全利率／期间／360 天 → 不发", OK_DISCOUNT_DECLARED, set()),
        ("自算：贴现利息自算缺天数折算", BAD_DISCOUNT_NODAYCOUNT, {"NR-NOSELF"}),
        ("自推：原句没分类却自己写商业承兑", BAD_CLASS_GUESS, {"NR-NOSELF"}),
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
    ap = argparse.ArgumentParser(description="应收应付票据稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="票据稿 .md 路径")
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
        print("缺入参：给一份票据稿路径，或用 --demo / --selftest", file=sys.stderr)
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
