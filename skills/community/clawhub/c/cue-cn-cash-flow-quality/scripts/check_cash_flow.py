#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_cash_flow.py — 现金流质量稿五道机检（零网络、零外发、不读环境变量）

用法：
    python3 scripts/check_cash_flow.py <现金流稿>.md
    python3 scripts/check_cash_flow.py --selftest
    python3 scripts/check_cash_flow.py --demo     打印一份完整合规样例（零输入可跑）

道一 CF-STRUCT 形制
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]；
  `主体：` 行在场且非空；`报告期：` 行在场且非空；
  七节齐且按序：经营活动现金流／投资活动现金流／筹资活动现金流／净现比与收现比／
  净利润调节表／口径与未取到／来源；
  前五节各至少一条 `- ` 发现行，节内只许 `- ` 发现行、`### ` 子标题与空行。

道二 CF-QUOTE 原句与锚
  每条数字行必须以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；原句与锚不得为空；
  例外只有两形：「未取到」行（缺的就是那份材料）与 [待人工] 行（判断位）；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址，检索日缺一不可；
  正文引用的每个 [S#] 必须在来源节有对应行。

道三 CF-NOSELF 不得自算（本件承重格）
  一、百分数与倍数：行内出现 `12.3%` 一类数值，必须能在同一行的「」原句里逐字找到；
      找不到的须标〔自算〕，且同一行同时给出 `分子…[S#]` 与 `分母…[S#]`，两处锚各挂自己那个数上。
  二、净现比／收现比：同一条，且必须分别给出分子与分母的来源。
  三、自由现金流：原句没有同一数值时须标〔自算〕，且同行给出至少两枚**不同号**锚，
      并写明资本开支取哪个科目（`资本开支` 或 `购建固定资产` 二者之一）。
  四、间接法调节表（第五节）：逐项照抄，不许合并、不许取绝对值——行内出现
      `绝对值`／`合并为`／`合并成`／`小计`／`合计` 一律发。

道四 CF-GAP 未取到两向点名
  正文（一至五节）写「未取到 X」⇒ 第六节必须点名 X；第六节点名了 X 而正文没有 ⇒ 同样发；两向都判。
  零缺口时，第六节须显式写 `未取到：无`；
  出现 `不适用`／`无此项`／`无需披露` 一律发——那是把没查当成没有。

道五 CF-LINE 红线
  造假／暴雷／资金链断裂／财务舞弊／财务洗澡／下期现金流预测／评级与目标价／建议关注一类断言零命中；
  含 [待人工] 的分句豁免，且只豁免它自己那一句（按 ；;。，,｜ 切分）；
  「期末现金及现金等价物余额」与「货币资金」在同一行被写成相等（＝／等于／即／相同／一致）一律发——
  两者不是同一个数，受限资金与等价物范围都不同。

退码：0 全过 / 1 有发条 / 2 用法错（缺参数） / 3 读不到文件或空稿。
"""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-cash-flow-quality"

CODES = ("CF-STRUCT", "CF-QUOTE", "CF-NOSELF", "CF-GAP", "CF-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("经营活动现金流", "投资活动现金流", "筹资活动现金流",
            "净现比与收现比", "净利润调节表", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"
INDIRECT_SECTION = "净利润调节表"

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
NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")
# 承重格里「被陈述的那个比率值」：倍数或百分数；自由现金流另按金额取
RATIO_VAL = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(倍|[%％])")
FCF_VAL = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(万元|亿元|元)")

# 金额单位换算：正文常写万元、原句常写元，同一个数要有同一个判法
UNIT_SCALE = {"元": 1.0, "万元": 1e4, "亿元": 1e8}

RATIO_KEYS = ("净现比", "收现比", "自由现金流")

MERGE_WORDS = ("绝对值", "合并为", "合并成", "小计", "合计")

GAP_EXCUSE = ("不适用", "无此项", "无需披露")

CASH_EQUAL = ("＝", "=", "等于", "即", "相同", "一致")

HARD_BAN = ("造假", "暴雷", "爆雷", "资金链断裂", "财务舞弊", "财务洗澡",
            "资金占用", "掏空", "目标价", "目标市值", "买入评级", "增持评级",
            "建议关注", "建议买入", "建议增持", "强烈推荐", "跑赢大盘",
            "必涨", "必跌", "稳赚", "零风险")

PRED_WORDS = ("下期现金流", "下季度现金流", "明年现金流", "将改善", "将恶化",
              "将持续为正", "转正", "将继续下降", "将继续上升")

CLAUSE_SPLIT = re.compile(r"[；;。，,｜|]")

SCOPE_RULES = (
    (("四期差异", "科目勾稽", "利润表点评", "毛利率拆解"),
     "改走 cn-earnings-note：那一件从利润表出发做逐数点评，本件只做现金流量表"),
    (("存货周转", "应收账款账龄", "合同资产", "存货跌价准备", "坏账准备"),
     "改走 cn-working-capital-quality：存货与应收的质量登记是那一件"),
    (("商誉减值", "商誉减值测试"),
     "改走 cn-goodwill-impairment-risk：商誉减值风险是那一件"),
    (("分红方案", "回购计划"),
     "改走 cn-shareholder-return：分红与回购登记是那一件"),
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
    for clause in _clauses(line):
        if "[待人工]" in clause:
            continue
        hit = [w for w in HARD_BAN if w in clause]
        if any(w in clause for w in PRED_WORDS):
            hit.append(next(w for w in PRED_WORDS if w in clause))
        # 期末现金余额 ≠ 货币资金
        if ("期末现金" in clause and "货币资金" in clause
                and any(e in clause for e in CASH_EQUAL)):
            hit.append("期末现金余额＝货币资金")
        if hit:
            add("CF-LINE", lineno, "红线词：%s（%s）" % ("、".join(sorted(set(hit))), clause.strip()[:40]))
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
    """正文写的数值是否落在原句里（百分数／倍数按字面，金额按换算后的元）。"""
    v = value.replace(",", "")
    if unit in ("%", "％"):
        return (v + "%") in quote_text.replace(" ", "").replace("％", "%")
    if unit == "倍":
        return (v + "倍") in quote_text.replace(" ", "")
    try:
        want = round(float(v) * UNIT_SCALE.get(unit, 1.0), 2)
    except ValueError:
        return False
    return want in quote_amounts


def _quotes(line):
    return "".join(m.group(1) for m in QUOTE.finditer(line))


def _check_fcf(lineno, line, add):
    """自由现金流自算：须交代经营现金流取哪个科目、资本开支取哪个科目。"""
    why = []
    if "资本开支" not in line and "购建固定资产" not in line:
        why.append("未写明资本开支取哪个科目")
    if "经营现金流" not in line and "经营活动产生的现金流量净额" not in line:
        why.append("未写明经营现金流取哪个科目")
    if why:
        add("CF-NOSELF", lineno, "自由现金流自算未交代%s" % "／".join(why))


def _check_mol_den(lineno, line, add, what):
    mol = re.search(r"分子[^｜|〕」；。]*\[S\d+\]", line)
    den = re.search(r"分母[^｜|〕」；。]*\[S\d+\]", line)
    why = []
    if not mol:
        why.append("缺分子来源")
    if not den:
        why.append("缺分母来源")
    if why:
        add("CF-NOSELF", lineno, "%s自算未交代%s" % (what, "／".join(why)))


def _check_noself(lineno, line, add, section=None):
    q = _quotes(line).replace(" ", "")
    q_amounts = _amounts(_quotes(line))
    # 一、百分数与倍数：原句里没有同一数值，就必须自算并交代分子分母
    toks = PCT.findall(line)
    missing = [t for t in toks if _norm_pct(t) not in q]
    if missing:
        if "〔自算〕" not in line:
            add("CF-NOSELF", lineno, "比率 %s 在原句里找不到，也没标〔自算〕：%s"
                % ("、".join(missing), line.strip()[:40]))
        elif "自由现金流" in line:
            _check_fcf(lineno, line, add)
        else:
            _check_mol_den(lineno, line, add, "比率")
    # 二、承重格：净现比／收现比／自由现金流——被陈述的比率值原句没写就必须自算
    if any(k in line for k in RATIO_KEYS):
        absent = []
        for m in RATIO_VAL.finditer(line):
            if not _num_in_quote(m.group(1), m.group(2), q_amounts, q):
                absent.append(m.group(0))
        if "自由现金流" in line:
            for m in FCF_VAL.finditer(line):
                if not _num_in_quote(m.group(1), m.group(2), q_amounts, q):
                    absent.append(m.group(0))
                    break
        if absent:
            if "〔自算〕" not in line:
                add("CF-NOSELF", lineno,
                    "承重格：%s 原句没写，须标〔自算〕并写明分子分母出处：%s"
                    % ("、".join(absent[:3]), line.strip()[:40]))
            elif "自由现金流" in line:
                _check_fcf(lineno, line, add)
            else:
                _check_mol_den(lineno, line, add, "比率")
    # 四、间接法调节表：逐项照抄
    if section == INDIRECT_SECTION:
        hit = [w for w in MERGE_WORDS if w in line]
        if hit:
            add("CF-NOSELF", lineno,
                "间接法调节表须逐项照抄，不许合并或取绝对值：命中「%s」" % "、".join(hit))


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
            add("CF-STRUCT", 1, "头部缺自标「%s」" % mark)
    if not any(SUBJECT.match(s) for _i, s in header):
        add("CF-STRUCT", 1, "头部缺 `主体：` 行")
    if not any(PERIOD.match(s) for _i, s in header):
        add("CF-STRUCT", 1, "头部缺 `报告期：` 行")

    # ---- 道一 节齐与序
    names = [n for n, _l, _b in sections]
    for name in SECTIONS:
        if name not in names:
            add("CF-STRUCT", 1, "缺节「%s」" % name)
    pos = [SECTIONS.index(n) for n in names]
    if pos != sorted(pos):
        add("CF-STRUCT", 1, "节序不对：现序 %s，应序 %s" % ("／".join(names), "／".join(SECTIONS)))
    for lineno, raw in stray:
        add("CF-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw)

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
                    add("CF-STRUCT", lineno, "节内只许 `- ` 发现行：%s" % s.strip()[:40])
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
                        add("CF-QUOTE", lineno, "发现行缺「」原句 + 〔锚：…〕 + [S#] 三元组：%s"
                            % s.strip()[:40])
                else:
                    for m in TRIPLE.finditer(s):
                        if not m.group("q").strip():
                            add("CF-QUOTE", lineno, "原句为空")
                        if not m.group("a").strip():
                            add("CF-QUOTE", lineno, "锚为空")
                    if not re.search(r"\[S\d+\]\s*$", s.strip()):
                        add("CF-QUOTE", lineno, "发现行未以 [S#] 收尾（三元组须在行末）")
                if "〔自算〕" in s:
                    if not (re.search(r"分子[^｜|〕」；。]*\[S\d+\]", s)
                            and re.search(r"分母[^｜|〕」；。]*\[S\d+\]", s)):
                        if "自由现金流" not in s:
                            add("CF-NOSELF", lineno, "自算行未分别给出分子与分母的 [S#]：%s"
                                % s.strip()[:40])
                _check_line(lineno, s, add)
                if PCT.findall(s) or any(k in s for k in RATIO_KEYS):
                    stats["ratio_lines"] += 1
                _check_noself(lineno, s, add, section=name)
            section_found[name] = n_find
            if n_find == 0:
                add("CF-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name)

        elif name == GAP_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not _is_finding_line(s):
                    add("CF-STRUCT", lineno, "第六节只许 `- ` 行：%s" % s.strip()[:40])
                    continue
                section_found.setdefault(name, 0)
                section_found[name] += 1
                for w in GAP_EXCUSE:
                    if w in s:
                        add("CF-GAP", lineno, "禁用「%s」把没查当成没有：%s" % (w, s.strip()[:40]))
                _check_line(lineno, s, add)
                if "未取到" in s:
                    continue

        elif name == SOURCE_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not s.lstrip().startswith("- ["):
                    add("CF-STRUCT", lineno, "来源节只许 `- [S#] …` 行：%s" % s.strip()[:40])
                    continue
                m = SOURCE_LINE.match(s.strip())
                if not m:
                    add("CF-QUOTE", lineno, "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:50])
                    continue
                stats["sources"] += 1

    for name in SECTIONS[:-1]:
        if name in names and section_found.get(name, 0) == 0 and name != GAP_SECTION:
            pass  # 前五节的空节已在上面报过

    # ---- 道四 未取到两向点名
    gap_body = [s for _ln, s in body_gaps]
    gap_sec = []
    for name, _h, body in sections:
        if name != GAP_SECTION:
            continue
        for _ln, s in body:
            if "未取到" in s and "未取到：无" not in s:
                gap_sec.append(s)
    for s in gap_body:
        if "未取到：无" in s:
            continue
        key = s.split("未取到", 1)[1]
        key = re.split(r"[：:，,。；;｜]", key.strip())[0].strip()
        key = key[:12]
        if key and not any(key in g or g.strip().startswith("- 未取到") and key in g for g in gap_sec):
            add("CF-GAP", 1, "正文写了未取到「%s」，第六节没点名" % key)
    for g in gap_sec:
        key = g.split("未取到", 1)[1]
        key = re.split(r"[：:，,。；;｜]", key.strip())[0].strip()[:12]
        if key and not any(key in s for s in gap_body):
            add("CF-GAP", 1, "第六节点名了「%s」，正文没有这条表述" % key)

    # 零缺口须显式写「未取到：无」
    if not gap_body and not gap_sec:
        gap_text = "\n".join(s for name, _h, body in sections if name == GAP_SECTION
                             for _ln, s in body)
        if "未取到：无" not in gap_text and "未取到:无" not in gap_text:
            add("CF-GAP", 1, "零缺口未显式写「未取到：无」")

    # ---- 道三 引用与登记
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
            add("CF-QUOTE", 1, "正文引用 [%s]，来源节没有对应登记行" % ref)

    # ---- 边界
    body_lines = [(ln, s) for name, _h, body in sections
                  if name != SOURCE_SECTION for ln, s in body]
    for words, tip in SCOPE_RULES:
        for ln, s in body_lines:
            if any(w in s for w in words):
                add("CF-STRUCT", ln, "越界：%s" % tip)
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


GOOD = r"""# 示例科技（600000.SH）现金流质量稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议 ｜ 判断位 [待人工]
主体：示例科技（600000.SH）
报告期：2025 年年度报告

## 经营活动现金流

- 经营活动产生的现金流量净额 12,340.00 万元「经营活动产生的现金流量净额 123,400,000.00 元」〔锚：2025 年年报·第 58 页·合并现金流量表〕[S1]
- 销售商品、提供劳务收到的现金 48,200.00 万元「销售商品、提供劳务收到的现金 482,000,000.00 元」〔锚：2025 年年报·第 58 页·合并现金流量表〕[S1]
- 购买商品、接受劳务支付的现金 26,500.00 万元「购买商品、接受劳务支付的现金 265,000,000.00 元」〔锚：2025 年年报·第 58 页·合并现金流量表〕[S1]
- 支付的各项税费 3,100.00 万元「支付的各项税费 31,000,000.00 元」〔锚：2025 年年报·第 58 页·合并现金流量表〕[S1]

## 投资活动现金流

- 投资活动产生的现金流量净额 -8,600.00 万元「投资活动产生的现金流量净额 -86,000,000.00 元」〔锚：2025 年年报·第 59 页·合并现金流量表〕[S1]
- 购建固定资产、无形资产和其他长期资产支付的现金 9,200.00 万元「购建固定资产、无形资产和其他长期资产支付的现金 92,000,000.00 元」〔锚：2025 年年报·第 59 页·合并现金流量表〕[S1]

## 筹资活动现金流

- 筹资活动产生的现金流量净额 1,500.00 万元「筹资活动产生的现金流量净额 15,000,000.00 元」〔锚：2025 年年报·第 59 页·合并现金流量表〕[S1]
- 分配股利、利润或偿付利息支付的现金 2,300.00 万元「分配股利、利润或偿付利息支付的现金 23,000,000.00 元」〔锚：2025 年年报·第 59 页·合并现金流量表〕[S1]

## 净现比与收现比

- 净利润 10,200.00 万元「归属于母公司所有者的净利润 102,000,000.00 元」〔锚：2025 年年报·第 46 页·合并利润表〕[S2]
- 营业收入 41,800.00 万元「营业收入 418,000,000.00 元」〔锚：2025 年年报·第 46 页·合并利润表〕[S2]
- 净现比为 1.21 倍〔自算〕分子＝经营活动产生的现金流量净额 123,400,000.00 元 [S1]｜分母＝归属于母公司所有者的净利润 102,000,000.00 元 [S2]
- 收现比为 115.31%〔自算〕分子＝销售商品、提供劳务收到的现金 482,000,000.00 元 [S1]｜分母＝营业收入 418,000,000.00 元 [S2]
- 自由现金流为 3,140.00 万元〔自算〕经营现金流取经营活动产生的现金流量净额 123,400,000.00 元 [S1]｜减项取购建固定资产、无形资产和其他长期资产支付的现金 92,000,000.00 元 [S1]，资本开支即该科目

## 净利润调节表

- 净利润 10,200.00 万元「净利润 102,000,000.00 元」〔锚：2025 年年报·第 60 页·现金流量表补充资料〕[S3]
- 加：资产减值准备 1,800.00 万元「加：资产减值准备 18,000,000.00 元」〔锚：2025 年年报·第 60 页·现金流量表补充资料〕[S3]
- 加：固定资产折旧 2,600.00 万元「加：固定资产折旧、油气资产折耗、生产性生物资产折旧 26,000,000.00 元」〔锚：2025 年年报·第 60 页·现金流量表补充资料〕[S3]
- 减：存货的减少 -1,200.00 万元「存货的减少 -12,000,000.00 元」〔锚：2025 年年报·第 60 页·现金流量表补充资料〕[S3]

## 口径与未取到

- 未取到：无
- 口径：比率均为自算并在同一行注明分子分母；自由现金流的资本开支口径取「购建固定资产、无形资产和其他长期资产支付的现金」。
- 口径：期末现金及现金等价物余额取自现金流量表，与资产负债表的货币资金不以相等处理。

## 来源

- [S1] 示例科技 2025 年年度报告·合并现金流量表 | https://example.com/ann/S1 | 检索日 2026-11-09 | 类型：公告
- [S2] 示例科技 2025 年年度报告·合并利润表 | https://example.com/ann/S2 | 检索日 2026-11-09 | 类型：公告
- [S3] 示例科技 2025 年年度报告·现金流量表补充资料 | https://example.com/ann/S3 | 检索日 2026-11-09 | 类型：公告
"""

# ---- 坏样：各只发自己那道码
BAD_STRUCT = GOOD.replace("## 筹资活动现金流", "## 筹资活动现金流量")

BAD_QUOTE = GOOD.replace(
    "「经营活动产生的现金流量净额 123,400,000.00 元」〔锚：2025 年年报·第 58 页·合并现金流量表〕[S1]",
    "经营活动产生的现金流量净额 123,400,000.00 元 [S1]")

BAD_NOSELF = GOOD.replace(
    "- 净现比为 1.21 倍〔自算〕分子＝经营活动产生的现金流量净额 123,400,000.00 元 [S1]｜分母＝归属于母公司所有者的净利润 102,000,000.00 元 [S2]",
    "- 净现比为 1.21 倍「经营活动产生的现金流量净额 123,400,000.00 元」〔锚：2025 年年报·第 58 页·合并现金流量表〕[S1]")

BAD_GAP = GOOD.replace(
    "- 未取到：无",
    "- 未取到 资本开支的明细构成：年报未按项目拆分")

BAD_LINE = GOOD.replace(
    "- 支付的各项税费 3,100.00 万元",
    "- 经营现金流为正说明不存在财务造假；支付的各项税费 3,100.00 万元")

# ---- 反证样：不该发的必须不发
OK_INDIRECT_FULL = GOOD.replace(
    "- 减：存货的减少 -1,200.00 万元「存货的减少 -12,000,000.00 元」〔锚：2025 年年报·第 60 页·现金流量表补充资料〕[S3]",
    "- 减：存货的减少 -1,200.00 万元「存货的减少 -12,000,000.00 元」〔锚：2025 年年报·第 60 页·现金流量表补充资料〕[S3]\n"
    "- 经营性应收项目的减少 -3,400.00 万元「经营性应收项目的减少 -34,000,000.00 元」〔锚：2025 年年报·第 60 页·现金流量表补充资料〕[S3]")

BAD_INDIRECT_MERGE = GOOD.replace(
    "- 减：存货的减少 -1,200.00 万元「存货的减少 -12,000,000.00 元」〔锚：2025 年年报·第 60 页·现金流量表补充资料〕[S3]",
    "- 减：存货与经营性应收合计 -4,600.00 万元「存货的减少 -12,000,000.00 元」〔锚：2025 年年报·第 60 页·现金流量表补充资料〕[S3]")

BAD_CASH_EQUAL = GOOD.replace(
    "- 口径：期末现金及现金等价物余额取自现金流量表，与资产负债表的货币资金不以相等处理。",
    "- 口径：期末现金及现金等价物余额等于货币资金，两者互相印证。")

OK_HUMAN = GOOD.replace(
    "- 未取到：无",
    "- 未取到：无\n- 现金流质量是否优良，交由人工判断 [待人工]")

BAD_HUMAN_HALF = GOOD.replace(
    "- 未取到：无",
    "- 未取到：无\n- 现金流质量交由人工判断 [待人工]，建议关注")

OK_FCF_DECLARED = GOOD.replace(
    "- 自由现金流为 3,140.00 万元〔自算〕经营现金流取经营活动产生的现金流量净额 123,400,000.00 元 [S1]｜减项取购建固定资产、无形资产和其他长期资产支付的现金 92,000,000.00 元 [S1]，资本开支即该科目",
    "- 自由现金流为 3,140.00 万元「自由现金流量 31,400,000.00 元」〔锚：2025 年年报·第 61 页·非财务信息披露〕[S3]")

# 零输入样例：直接由 GOOD 派生，不另抄一份——两份会各自漂移，
# 而用户看到的「成品长什么样」必须永远等于自测里那个「好样」。
DEMO = GOOD


def _codes(text):
    findings, _stats = check_text(text)
    return findings, set(c for c, _l, _m in findings)


def selftest():
    cases = (
        ("好样应零发条", GOOD, set()),
        ("形制：节标题写错（筹资活动现金流量）", BAD_STRUCT, {"CF-STRUCT"}),
        ("锚：数字行没挂原句与锚", BAD_QUOTE, {"CF-QUOTE"}),
        ("承重格：净现比自算充披露值", BAD_NOSELF, {"CF-NOSELF"}),
        ("点名：正文未取到而第六节没列", BAD_GAP, {"CF-GAP"}),
        ("红线：写不存在财务造假", BAD_LINE, {"CF-LINE"}),
        ("反证：调节表逐项照抄 → 不发", OK_INDIRECT_FULL, set()),
        ("自算：调节表合并项目（合计）", BAD_INDIRECT_MERGE, {"CF-NOSELF"}),
        ("红线：期末现金＝货币资金", BAD_CASH_EQUAL, {"CF-LINE"}),
        ("反证：[待人工] 整句成立 → 不发", OK_HUMAN, set()),
        ("反证：[待人工] 只豁免自己那句，后半句建议关注照样发", BAD_HUMAN_HALF, {"CF-LINE"}),
        ("反证：自由现金流照抄披露值 → 不发", OK_FCF_DECLARED, set()),
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
    ap = argparse.ArgumentParser(description="现金流质量稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="现金流稿 .md 路径")
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
        print("缺入参：给一份现金流稿路径，或用 --demo / --selftest", file=sys.stderr)
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
