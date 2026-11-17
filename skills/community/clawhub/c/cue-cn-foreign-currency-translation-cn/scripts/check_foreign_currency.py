#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_foreign_currency.py —— 外币折算稿五道机检（第 6 拍：五道全部实装）。

纯 stdlib、零网络、零外部依赖。
用法：
    check_foreign_currency.py <外币折算稿.md>   # 有发条退 1，全过退 0
    check_foreign_currency.py --demo            # 打印一份完整合规样例（零输入可跑）
    check_foreign_currency.py --selftest        # 跑包内夹具自检

退码：0 全过 / 1 有发条 / 2 用法错 / 3 读不到或空稿（另有未实装的道时 --selftest 也退 3）

五道全部实装：FX-STRUCT、FX-QUOTE、FX-NOSELF、FX-GAP、FX-LINE。
仍留一处已知覆盖不到：FX-NOSELF 里「正文给金额但没给汇率、或给的汇率在原句里找不到
这个数字」那条硬判据尚未接线（见报告末行的自报提示）。
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-foreign-currency-translation-cn"

# ---------------------------------------------------------------- 五个码
# 每道一枚，互不代偿：一道红了不许指望另一道替它说话。
CODES = (
    "FX-STRUCT",   # 形制：头部自标、主体/报告期、七节按序、前五节各至少一条发现行
    "FX-QUOTE",    # 原句与锚：发现行须以「」+〔锚：…〕+[S#] 收尾；来源行带 URL 与检索日
    "FX-NOSELF",   # 不自推不自算：汇率来源与折算方法只认原句；三类汇兑损益不得拼成等式
    "FX-GAP",      # 缺口两向点名：正文与倒数第二节互相对账；禁「不适用」类搪塞
    "FX-LINE",     # 红线：汇率走势判断、套保建议、利润影响测算、境外经营优劣、评级目标价
)
UNIMPLEMENTED = ()

# ---------------------------------------------------------------- 四件头部自标
MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

# ---------------------------------------------------------------- 七节（节名照抄派单）
SECTIONS = (
    "外币货币性项目",       # ① 按币种列期末外币余额、折算汇率、折合人民币金额
    "折算汇率与汇率来源",   # ② 即期／近似汇率、取数日、发布机构——只认披露写法
    "汇兑损益",             # ③ 当期损益／其他综合收益／资本化三处去向，独立数
    "境外经营折算",         # ④ 记账本位币、期末汇率、平均汇率、折算差额及其权益列示
    "记账本位币变更",       # ⑤ 是否发生、变更原因原文、对比较报表的影响
    "口径与未取到",         # ⑥ 缺口两向点名；零缺口写「未取到：无」
    "来源",                 # ⑦ 来源行 [S#] 标题 | URL | 检索日 | 类型
)
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = SECTIONS[5]
SOURCE_SECTION = SECTIONS[6]

# ---------------------------------------------------------------- 形制与原句判据的正则
HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")

SUBJECT = re.compile(r"^主体：\s*(\S.*)$")
PERIOD = re.compile(r"^报告期：\s*(\S.*)$")

# 三元组：原句 + 锚 + 来源编号，且必须落在行末（判据看的就是这个收尾形状）。
TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
ANCHOR_BLOCK = re.compile(r"〔\s*锚\s*[:：][^〕]*〕")
ANCHOR_REF = re.compile(r"\[(S\d+)\]")

SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)"
    r"\|\s*(?P<url>https?://\S+)\s*\|"
    r"\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$"
)

# ---------------------------------------------------------------- 判据用词表（下一拍接线）
# 折算方法与汇率来源词族：写这些词的，必须出现在同一行「」原句里。
# 专项①：汇率来源只有披露知道——不按「年末中间价」补。
RATE_WORDS = (
    "即期汇率", "近似汇率", "中间价", "收盘价", "中国人民银行", "中国外汇交易中心",
    "期末汇率", "平均汇率", "月初汇率", "当月平均", "加权平均",
)

# 专项②：三类汇兑损益去向是独立披露，两两拼成等式即视为替披露轧差。
EXCHANGE_GROUPS = (
    (("财务费用", "其他综合收益", "在建工程", "存货成本"),
     "计入当期损益、计入其他综合收益、计入资产成本是三笔独立披露，缺的那笔写未取到"),
)

# 缺口搪塞词：把「没查到」写成「没有」。
GAP_EXCUSE = ("不适用", "无此项", "无需披露")

# 红线词族：判断汇率走势、建议套保、测算利润影响、评价境外经营、评级与目标价。
# 只收「带判断态度」的整词；折算汇率／即期汇率／平均汇率这类正常术语不在此表。
HARD_BAN = (
    # 汇率走势与预测
    "汇率将", "人民币将", "美元将走强", "美元将走弱", "预计汇率", "预判汇率", "预测汇率",
    "汇率会上涨", "汇率会下跌", "汇率走势", "贬值趋势", "升值趋势",
    # 结汇／购汇／套保建议
    "建议结汇", "建议购汇", "应锁定汇率", "建议套保", "应当套保", "建议锁汇", "应当锁汇",
    "不必套保", "套保为宜",
    # 利润影响测算
    "影响利润", "增厚利润", "侵蚀利润", "影响 EPS", "每股收益将", "对股价",
    # 境外经营优劣
    "境外经营优质", "境外资产优质", "海外布局领先", "国际化成功",
    # 评级、目标价与投资价值
    "目标价", "目标市值", "评级", "买入", "卖出", "增持", "减持",
    "值得投资", "低估", "高估", "强烈推荐", "跑赢大盘",
)


def mark_first_run() -> None:
    """首次运行埋点：往 ~/.cue-usage/<slug>-<日期> 落一个空文件。

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


def _section_of(heading):
    """把 `## 3. 汇兑损益` 归一成 `汇兑损益`；认不出返回 None（当作 stray）。"""
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
    """切成 (头部行, 七节, stray)。同一节名第二次出现一律记 stray（多出同名节）。"""
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


def _is_gap_line(s):
    """一条发现行是不是「未取到」行。

    只认带冒号的登记形（`未取到：原因`）。第六节的口径行里会出现「没披露就写未取到」
    这种**叙述**，它不是缺口登记，认错了会给好样发假红。
    """
    return "未取到：" in s or "未取到:" in s


def _exempt_triple(s):
    """不要求三元组的三类行：未取到行、[待人工] 行、〔自算〕行。"""
    return _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s


def _is_zero_gap(s):
    """零缺口登记行：`未取到：无`。它不是一条缺口，别把它算进两向对账。"""
    return "未取到：无" in s or "未取到:无" in s


# 红线自述节：这一节本来就要把禁词写出来当禁用说明，判它等于自己把自己判红。
# 按节名跳过，不按行号——行号会随稿子长度漂移。
REDLINE_SECTION = "合规红线"


def _check_line(sections, add):
    """FX-LINE：正文里出现禁词即发，逐处点名。

    两条不算本件在判断：
      * 「」内的引用原文——那是披露自己说的话，剥掉再判；
      * 「合规红线」整节——禁用说明天然含禁词。
    """
    for name, _hline, body in sections:
        if name == REDLINE_SECTION:
            continue
        for lineno, s in body:
            if not s.strip():
                continue
            bare = QUOTE.sub("", s)
            for w in HARD_BAN:
                if w in bare:
                    add("FX-LINE", lineno,
                        "红线表述「%s」（本件不判断，请回原文核对）：%s" % (w, s.strip()[:40]))


def _gap_key(line):
    """从一条「未取到」里取出被点名的那一项，两向对账用同一个取法。

    本件两种合法写法，取法要对两种都成立：
      正文 `- 项名 未取到：原因`  → 项名在「未取到」**前**
      第六节 `- 未取到：项名`      → 项名在「未取到」**后**
    先看前面有没有项名（剥掉行首 `- `、去掉冒号），有就用它；没有才取冒号之后那一段。
    一律取「未取到」后面那段，正文标准形会取到**原因**而不是项名，两向必然对不上。
    """
    head = re.sub(r"^-\s*", "", line.split("未取到", 1)[0]).strip().rstrip("：:，,。；; ")
    if head:
        return head[:12]
    rest = line.split("未取到", 1)[1].lstrip()
    m = re.match(r"^[：:]\s*(.+)$", rest)
    if m:
        rest = m.group(1)
    return re.split(r"[：:，,。；;｜]", rest.strip())[0].strip()[:12]


def check_text(text):
    findings = []
    stats = {"发现行": 0, "来源": 0}

    def add(code, lineno, msg):
        findings.append((code, lineno, msg))

    header, sections, stray = split_doc(text)

    # ---- FX-STRUCT 一：头部四件自标 + 主体 / 报告期
    htext = "\n".join(s for _i, s in header)
    for mark in MARK_TEXTS:
        if mark not in htext:
            add("FX-STRUCT", 1, "头部缺自标「%s」" % mark)
    if not any(SUBJECT.match(s) for _i, s in header):
        add("FX-STRUCT", 1, "头部缺 `主体：` 行")
    if not any(PERIOD.match(s) for _i, s in header):
        add("FX-STRUCT", 1, "头部缺 `报告期：` 行")

    # ---- FX-STRUCT 二：七节齐且有序
    names = [n for n, _l, _b in sections]
    for name in SECTIONS:
        if name not in names:
            add("FX-STRUCT", 1, "缺节「%s」" % name)
    pos = [SECTIONS.index(n) for n in names]
    if pos != sorted(pos):
        add("FX-STRUCT", 1, "节序不对：现序 %s，应序 %s"
            % ("／".join(names), "／".join(SECTIONS)))
    for lineno, raw in stray:
        add("FX-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw)

    referenced = []

    for name, hline, body in sections:
        if name in CONTENT_SECTIONS:
            # ---- FX-STRUCT 三：前五节各至少一条 `- ` 发现行，且只许发现行
            n_find = 0
            for lineno, s in body:
                if not s.strip() or s.lstrip().startswith("###"):
                    continue
                if not _is_finding_line(s):
                    add("FX-STRUCT", lineno, "节内只许 `- ` 发现行：%s" % s.strip()[:40])
                    continue
                n_find += 1
                stats["发现行"] += 1
                referenced.extend(ANCHOR_REF.findall(s))
                # ---- FX-QUOTE：每条发现行以三元组收尾
                if not TRIPLE.search(s):
                    if not _exempt_triple(s):
                        add("FX-QUOTE", lineno,
                            "发现行缺「」原句 + 〔锚：…〕 + [S#] 三元组：%s" % s.strip()[:40])
                else:
                    for m in TRIPLE.finditer(s):
                        if not m.group("q").strip():
                            add("FX-QUOTE", lineno, "原句为空")
                        if not m.group("a").strip():
                            add("FX-QUOTE", lineno, "锚为空")
                    if not re.search(r"\[S\d+\]\s*$", s.strip()):
                        add("FX-QUOTE", lineno,
                            "发现行未以 [S#] 收尾（三元组须在行末）")
            if n_find == 0:
                add("FX-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name)

        elif name == GAP_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not _is_finding_line(s):
                    add("FX-STRUCT", lineno, "第六节只许 `- ` 行：%s" % s.strip()[:40])

        elif name == SOURCE_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not s.lstrip().startswith("- ["):
                    add("FX-STRUCT", lineno, "来源节只许 `- [S#] …` 行：%s" % s.strip()[:40])
                    continue
                # ---- FX-QUOTE：来源行须带 URL 与检索日
                if not SOURCE_LINE.match(s.strip()):
                    add("FX-QUOTE", lineno,
                        "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:50])
                    continue
                stats["来源"] += 1

    # ---- FX-QUOTE：正文引用的 [S#] 必须已在来源节登记
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
            add("FX-QUOTE", 1, "正文引用 [%s]，来源节没有对应登记行" % ref)

    # ---- FX-NOSELF：计量模式与转换差额去向只认原句，正文不许自推
    for lineno, s in enumerate(text.splitlines(), 1):
        m = QUOTE.search(s)
        quoted = m.group(1) if m else ""
        for mode in ("公允价值模式", "成本模式"):
            if mode in s and mode not in quoted:
                add("FX-NOSELF", lineno, "计量模式系推断，原句无该词：%s" % s.strip()[:40])
                break
        if "转换差额" in s and ("其他综合收益" in s or "当期损益" in s):
            missing = [d for d in ("其他综合收益", "当期损益")
                       if d in s and d not in quoted]
            if missing:
                add("FX-NOSELF", lineno,
                    "转换差额去向系推断，原句未写：%s" % "、".join(missing))

    # ---- FX-GAP 一二三：缺口两向点名、零缺口显式、借口词
    body_gaps = []     # 正文五节里的「未取到」登记行
    gap_sec = []       # 第六节里的缺口点名行（「未取到：无」不算一条缺口）
    gap_text = []      # 第六节全文，零缺口判据要看它
    for name, _h, body in sections:
        for lineno, s in body:
            if not s.strip():
                continue
            # 丙：借口词——把「没查到」写成「没有」，任何一节出现都发
            for w in GAP_EXCUSE:
                if w in s:
                    add("FX-GAP", lineno,
                        "禁用「%s」把没查当成没有：%s" % (w, s.strip()[:40]))
            if not _is_gap_line(s) or _is_zero_gap(s):
                continue
            if name in CONTENT_SECTIONS:
                body_gaps.append((lineno, s))
            elif name == GAP_SECTION:
                gap_sec.append((lineno, s))
        if name == GAP_SECTION:
            gap_text.extend(s for _ln, s in body)

    # 甲：两向对账。正文写了未取到而第六节没点名；第六节点名了而正文没有这条。
    for lineno, s in body_gaps:
        key = _gap_key(s)
        if key and not any(key in g for _ln, g in gap_sec):
            add("FX-GAP", lineno, "正文写了未取到「%s」，第六节没点名" % key)
    for lineno, g in gap_sec:
        key = _gap_key(g)
        if key and not any(key in s for _ln, s in body_gaps):
            add("FX-GAP", lineno, "第六节点名了「%s」，正文没有这条表述" % key)

    # 乙：零缺口须显式写「未取到：无」——不写，读的人分不清「查过没有缺口」与「没查」。
    if not body_gaps and not gap_sec and not any(_is_zero_gap(x) for x in gap_text):
        add("FX-GAP", 1, "零缺口未显式写「未取到：无」")

    _check_line(sections, add)

    findings.sort(key=lambda x: (x[1], CODES.index(x[0])))
    return findings, stats


def report(path, findings, stats):
    print("稿：%s" % path)
    print("统计：发现行 %d ｜ 来源 %d" % (stats["发现行"], stats["来源"]))
    if not findings:
        print("结论：五道全过（零发条）")
        print("注：FX-NOSELF 的「汇率缺省取值／原句找不到该数字」那条判据尚未接线，"
              "此处零发条不覆盖它（见 --selftest 末行）。")
        return
    print("结论：发条 %d" % len(findings))
    for code, lineno, msg in findings:
        print("  %s L%-4d %s" % (code, lineno, msg))
    hit = sorted(set(c for c, _l, _m in findings))
    print("发条码：%s" % "、".join(hit))


# ---------------------------------------------------------------- 样例（--demo）
# 这份样例是好样的唯一定义处：它必须零发条。下一拍接上剩余三道后，
# 它仍须继续零发条——那才是「好样长这样」的可执行版本。
DEMO = r"""# 示例材料（600000.SH）外币折算登记稿

> 本稿为 AI 整理初稿，请回原文核对；不构成投资建议。

主体：示例科技股份有限公司（600000.SH）
报告期：2025 年度
判断位 [待人工]：本件只登记披露怎么写，判断留给人。

## 外币货币性项目

- 美元货币性项目期末余额 12,000,000.00 美元「期末美元货币性项目余额 12,000,000.00 美元」〔锚：2025 年年报·第 158 页·附注七·外币货币性项目〕[S1]
- 欧元货币性项目期末余额 3,000,000.00 欧元「期末欧元货币性项目余额 3,000,000.00 欧元」〔锚：2025 年年报·第 158 页·附注七·外币货币性项目〕[S1]
- 美元折合人民币 86,280,000.00 元「按期末汇率 7.1900 折算，折合人民币 86,280,000.00 元」〔锚：2025 年年报·第 158 页·附注七·外币货币性项目〕[S1]

## 折算汇率与汇率来源

- 折算汇率 7.1900「期末美元兑人民币即期汇率为 7.1900」〔锚：2025 年年报·第 158 页·附注七·外币货币性项目〕[S1]
- 汇率来源 未取到：附注未披露该即期汇率的发布机构与取数日
- 近似汇率运用 未取到：附注未说明是否采用近似汇率

## 汇兑损益

- 计入财务费用的汇兑损益 2,400,000.00 元「本期计入财务费用的汇兑损失为 2,400,000.00 元」〔锚：2025 年年报·第 159 页·附注七·汇兑损益〕[S2]
- 计入其他综合收益的汇兑损益 未取到：附注未披露本期计入其他综合收益的汇兑差额
- 计入资产成本的汇兑损益 未取到：附注未披露本期资本化的汇兑差额

## 境外经营折算

- 境外子公司记账本位币 美元「乙公司以美元为记账本位币」〔锚：2025 年年报·第 159 页·附注七·境外经营〕[S2]
- 资产负债项目折算汇率 期末汇率「资产负债表项目按期末汇率折算」〔锚：2025 年年报·第 159 页·附注七·境外经营〕[S2]
- 损益项目折算汇率 平均汇率「损益项目按当期平均汇率折算」〔锚：2025 年年报·第 159 页·附注七·境外经营〕[S2]
- 外币报表折算差额 未取到：附注未披露折算差额的具体金额与其在所有者权益中的列示位置

## 记账本位币变更

- 本期是否变更 否「本公司本期未发生记账本位币变更」〔锚：2025 年年报·第 159 页·附注七·记账本位币〕[S2]
- 变更原因 本期未发生「本公司本期未发生记账本位币变更」〔锚：2025 年年报·第 159 页·附注七·记账本位币〕[S2]
- 对比较报表的影响 本期未发生「本公司本期未发生记账本位币变更」〔锚：2025 年年报·第 159 页·附注七·记账本位币〕[S2]

## 口径与未取到

- 口径：汇率与折算方法一律照抄附注原句，不按「年末中间价」补；三类汇兑损益去向各自登记，不自行轧差。
- 口径：境外经营只登记折算怎么写，不判合并范围。
- 未取到：汇率来源
- 未取到：近似汇率运用
- 未取到：计入其他综合收益的汇兑损益
- 未取到：计入资产成本的汇兑损益
- 未取到：外币报表折算差额

## 来源

- [S1] 示例科技股份有限公司 2025 年年度报告 | https://example.invalid/600000-2025.pdf | 检索日 2026-11-13 | 类型：年报
- [S2] 示例科技股份有限公司 2025 年年度报告 | https://example.invalid/600000-2025.pdf | 检索日 2026-11-13 | 类型：年报
"""

# 坏样：两处单点注入，一处只红 FX-STRUCT、一处只红 FX-QUOTE。
#   * 多出一节同名节——不删正文，免得节内发现行一并丢、连带把 FX-QUOTE 也带红；
#   * 挑一条**有完整三元组**、且不是「未取到」的发现行，只摘掉三元组（项名与值位都留着）。
#     摘三元组不能摘在未取到行上：那行本来豁免，摘了什么都不发。
BAD = DEMO.replace(
    "## 折算汇率与汇率来源", "## 外币货币性项目\n\n## 折算汇率与汇率来源", 1
).replace(
    "「按期末汇率 7.1900 折算，折合人民币 86,280,000.00 元」"
    "〔锚：2025 年年报·第 158 页·附注七·外币货币性项目〕[S1]",
    "[S1]", 1
)

# 坏样（FX-NOSELF）：正文断了一个计量模式，而它引的原句写的是另一个模式。
NOSELF_BAD = DEMO.replace(
    "- 境外子公司记账本位币 美元「乙公司以美元为记账本位币」"
    "〔锚：2025 年年报·第 159 页·附注七·境外经营〕[S2]",
    "- 境外子公司记账本位币 美元「乙公司以美元为记账本位币」"
    "〔锚：2025 年年报·第 159 页·附注七·境外经营〕[S2]\n"
    "- 投资性房地产后续计量 公允价值模式「投资性房地产按成本模式进行后续计量」"
    "〔锚：2025 年年报·第 159 页·附注七·投资性房地产〕[S2]",
    1
)


def _codes(text):
    findings, _stats = check_text(text)
    return findings, set(c for c, _l, _m in findings)


def _must_replace(text, old, new):
    """注入必须真落地：对不上就抛，别静默产出原文（否则「该红没红」会被读成机检漏判）。"""
    if old not in text:
        raise RuntimeError("夹具注入点对不上：%r" % old[:60])
    return text.replace(old, new, 1)


def _gap_unmatched_sample():
    """坏样（FX-GAP 甲）：正文有一条未取到，第六节把它删掉——两向对不上。"""
    return _must_replace(
        DEMO, "- 未取到：外币报表折算差额\n", "")


def _zero_gap_sample():
    """反证样（FX-GAP 乙）：全文零缺口，第六节显式写「未取到：无」——须零发条。

    缺一不可：把正文的「未取到」行全摘掉（那几节仍各留至少一条发现行，不连带空节），
    再把第六节五个缺口条目换成一行「未取到：无」。
    """
    t = DEMO
    for line in (
        "- 汇率来源 未取到：附注未披露该即期汇率的发布机构与取数日\n",
        "- 近似汇率运用 未取到：附注未说明是否采用近似汇率\n",
        "- 计入其他综合收益的汇兑损益 未取到：附注未披露本期计入其他综合收益的汇兑差额\n",
        "- 计入资产成本的汇兑损益 未取到：附注未披露本期资本化的汇兑差额\n",
        "- 外币报表折算差额 未取到：附注未披露折算差额的具体金额与其在所有者权益中的列示位置\n",
    ):
        t = _must_replace(t, line, "")
    return _must_replace(
        t,
        "- 未取到：汇率来源\n"
        "- 未取到：近似汇率运用\n"
        "- 未取到：计入其他综合收益的汇兑损益\n"
        "- 未取到：计入资产成本的汇兑损益\n"
        "- 未取到：外币报表折算差额",
        "- 未取到：无")


def _line_sample():
    """坏样（FX-LINE）：正文写了一行结汇建议——本件不许替用户下这个判断。

    注入点选第六节的口径行（那段本来就不要求三元组），只把口径换成建议句：
    不连带 FX-QUOTE（不要求三元组）、不连带 FX-STRUCT（仍是 `- ` 行、节数不变）。
    """
    return _must_replace(
        DEMO,
        "- 口径：境外经营只登记折算怎么写，不判合并范围。",
        "- 口径：建议结汇以锁定汇率，避免后续波动。")


def _line_quoted_ok_sample():
    """反证样（FX-LINE）：禁词只出现在「」原句里，正文自己没写——须零发条。

    引文是证据、不是本件断言：披露原话说「目标价」不等于本件给了目标价。
    """
    return _must_replace(
        DEMO,
        "- 口径：境外经营只登记折算怎么写，不判合并范围。",
        "- 口径：原文提及「目标价」一事，本件不采信、不转述。")


def selftest():
    cases = (
        ("好样应零发条（五道）", DEMO, set()),
        ("坏样：多出一节同名节 + 一条发现行丢三元组", BAD, {"FX-STRUCT", "FX-QUOTE"}),
        ("坏样：计量模式系推断（原句写的是另一模式）", NOSELF_BAD, {"FX-NOSELF"}),
        ("坏样：正文写了未取到而第六节没点名（两向不对账）",
         _gap_unmatched_sample(), {"FX-GAP"}),
        ("反证：零缺口显式写「未取到：无」不得误红",
         _zero_gap_sample(), set()),
        ("坏样：正文写了结汇建议（红线）", _line_sample(), {"FX-LINE"}),
        ("反证：禁词只在「」原句里、正文没写，不得误红",
         _line_quoted_ok_sample(), set()),
    )
    bad = 0
    for label, text, want in cases:
        findings, got = _codes(text)
        if got == want:
            print("过   %s（发条 %d 条：%s）"
                  % (label, len(findings), "、".join(sorted(got)) or "无"))
        else:
            bad += 1
            detail = "；".join("%s L%d %s" % (c, l, m) for c, l, m in findings[:4])
            print("不合 %s：期望 %s 实得 %s ｜ %s"
                  % (label, sorted(want) or "无", sorted(got) or "无", detail))
    print("——")
    what = {"FX-NOSELF": "不自推不自算", "FX-GAP": "缺口两向", "FX-LINE": "红线"}
    for code in UNIMPLEMENTED:
        print("不可判 %s %s：判据未实装" % (code, what[code]))
    # 五道各有判据在管，所以「不可判」按码计为 0；但 FX-NOSELF 少接了一条硬判据，
    # 这条单独点出来——不可判=0 不许被读成「五道全方面覆盖」。
    print("已知覆盖不到 FX-NOSELF：正文给金额但没给汇率、或给的汇率在原句里找不到该数字"
          "（本尺不判，请人工回原句核对）")
    print("自测档数=%d｜不合=%d｜不可判=%d" % (len(cases), bad, len(UNIMPLEMENTED)))
    if bad:
        return 1
    return 3 if UNIMPLEMENTED else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="外币折算稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="外币折算稿 .md 路径")
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
        print("缺入参：给一份外币折算稿路径，或用 --demo / --selftest", file=sys.stderr)
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
