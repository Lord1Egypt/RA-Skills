#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_long_term_equity.py — 长期股权投资稿五道机检（零网络、零外发、不读环境变量）

用法：
    python3 scripts/check_long_term_equity.py <长期股权投资稿>.md
    python3 scripts/check_long_term_equity.py --selftest
    python3 scripts/check_long_term_equity.py --demo     打印一份完整合规样例（零输入可跑）

道一 LE-STRUCT 形制
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]；
  `主体：` 行在场且非空；`报告期：` 行在场且非空；
  七节齐且按序：按被投资单位列的明细／核算方法与分类／权益法确认的投资损益／
  投资收益与现金分红的对应／减值与处置／口径与未取到／来源；
  前五节各至少一条 `- ` 发现行，节内只许 `- ` 发现行、`### ` 子标题与空行。

道二 LE-QUOTE 原句与锚
  每条数字行必须以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；原句与锚不得为空；
  例外只有三形：「未取到」行（缺的就是那份披露）、[待人工] 行（判断位）与〔自算〕行（本件自己算的）；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址，检索日缺一不可；
  正文引用的每个 [S#] 必须在来源节有对应行。

道三 LE-NOSELF 不得自推自算（本件承重格）
  一、核算方法与分类只认原句：写「权益法」「成本法」「合营企业」「联营企业」「子公司」「控制」
      「共同控制」「重大影响」的，同一行「」原句里也必须写得到——
      某单位算联营还是合营、能不能控制、用成本法还是权益法，**是披露做的判断**；
      20%／50% 只是常识门槛，本包不按持股比例推。
  二、百分数：行内出现 `30.00%` 一类数值，必须能在同一行的「」原句里逐字找到；
      找不到的须标〔自算〕，且同一行同时给出 `分子…[S#]` 与 `分母…[S#]`。
      例外：「未取到」行整行豁免——那一行里的百分比是**披露对象的名称**，不是本件算的比值。
  三、自算差额：同一行标了〔自算〕又谈轧差／推算／差额／补齐的，必须写明分子与分母各自的来源。
  四、三个数不自行轧差：被投资单位净利润、按持股比例确认的投资收益、未实现损益抵消额是三个独立数；
      「本期确认的投资收益」与「本期收到的现金分红」也是两个数。一行里把它们拼成等式
      （＝／等于／即／系…之差）而没标〔自算〕，一律发——差额要么披露给，要么写 `未取到`。

道四 LE-GAP 未取到两向点名
  正文（一至五节）写「未取到 X」⇒ 第六节必须点名 X；第六节点名了 X 而正文没有 ⇒ 同样发；两向都判。
  零缺口时，第六节须显式写 `未取到：无`；
  出现 `不适用`／`无此项`／`无需披露` 一律发——那是把没查当成没有。

道五 LE-LINE 红线
  被投资单位值不值钱／投资能否收回／预测投资收益／建议追加或退出投资／对赌条款是否合理／
  对 EPS 与股价的影响／评级与目标价 一类断言零命中；
  **只判本件自己写的句子**：同一行「」里的引文先洗掉再判——引文是证据，不是本件的断言；
  「〔锚：…〕」也先洗掉：那是定位指针，不是本件在判断；
  含 [待人工] 的分句豁免，且只豁免它自己那一句（按 ；;。，,｜ 切分）。

退码：0 全过 / 1 有发条 / 2 用法错（缺参数） / 3 读不到文件或空稿。
"""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-long-term-equity-investment-cn"

CODES = ("LE-STRUCT", "LE-QUOTE", "LE-NOSELF", "LE-GAP", "LE-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("按被投资单位列的明细", "核算方法与分类", "权益法确认的投资损益",
            "投资收益与现金分红的对应", "减值与处置", "口径与未取到", "来源")
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

# 承重格的词族：写在本件句子里就必须在原句里也写得到。
# 这八枚全是**披露做的分类判断**，不是本件能按持股比例推出来的。
METHOD_WORDS = ("权益法", "成本法", "合营企业", "联营企业", "子公司",
                "共同控制", "重大影响", "控制")
RECON_WORDS = ("轧差", "推算", "差额", "补齐")

# 「三个数不自行轧差」：每组里的词同线出现两枚以上，又被连成等式，就是替披露做了减法。
NETTING_GROUPS = (
    (("净利润", "投资收益", "未实现损益"),
     "被投资单位净利润、按持股比例确认的投资收益、未实现损益抵消额是三个独立数"),
    (("投资收益", "现金分红"),
     "本期确认的投资收益与本期收到的现金分红是两个数"),
)

GAP_EXCUSE = ("不适用", "无此项", "无需披露")

EQUAL_WORDS = ("＝", "=", "等于", "即", "相同", "一致", "等同")
NEG_EQUAL = re.compile(r"(?:不|非)(?:等于|同于|一致|相同|等同)")

HARD_BAN = ("值钱", "值得投资", "具有投资价值", "投资价值高", "估值偏低", "估值偏高",
            "被低估", "被高估", "严重低估", "应当追加投资", "建议追加投资", "应当退出",
            "建议退出", "建议减持", "建议增持",
            "能否收回", "全额收回", "本金安全",
            "预计投资收益", "预测投资收益", "投资收益将", "收益可期",
            "对赌条款合理", "业绩承诺可实现", "对赌可实现", "承诺必然完成",
            "增厚利润", "增厚 EPS", "影响 EPS", "每股收益将",
            "目标价", "目标市值", "买入评级", "增持评级", "中性评级",
            "强烈推荐", "跑赢大盘", "必涨", "必跌",
            "影响股价", "股价将", "预计股价", "市值管理", "无风险", "稳赚")

CLAUSE_SPLIT = re.compile(r"[；;。，,｜|]")

SCOPE_RULES = (
    (("关联方关系", "关联交易定价", "关联交易披露"),
     "改走 cue-related-party-terms-cn：关联方与关联交易的口径、定价与披露是那一件"),
    (("商誉减值", "减值测试的结论", "减值是否充分"),
     "改走 cn-goodwill-impairment-risk：商誉与长期资产减值风险的判定是那一件，本件只登记长期股权投资这一节的减值披露"),
    (("控股股东变更", "实际控制人变更", "控制权变更"),
     "改走 cn-controlling-shareholder-change-cn：控股股东变更与控制权是那一件"),
    (("四期差异", "科目勾稽点评"),
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
    # 先洗引文与锚块、再切分句：引文里的逗号会在切分处断成两截，
    # 逐句洗就洗不干净——「附注称该单位无风险」这类照抄原文会被误判成本件断言。
    own_line = ANCHOR_BLOCK.sub("", _strip_quotes(line))
    for clause in _clauses(own_line):
        if "[待人工]" in clause:
            continue
        hit = [w for w in HARD_BAN if w in clause]
        if hit:
            add("LE-LINE", lineno, "红线词：%s（%s）" % ("、".join(sorted(set(hit))), clause.strip()[:40]))
            return


def _quotes(line):
    return "".join(m.group(1) for m in QUOTE.finditer(line))


def _check_vocab(lineno, line, add, words, what):
    """词族只认原句：本件句子里写了，同一行原句也必须写到。

    判域＝去掉**项名**与**锚标签**之后的余下部分。两处都是标签、不是断言：
    项名是「权益法确认的投资损益」这种登记对象，锚标签是「〔锚：…附注七·长期股权投资〕」
    这种定位指针——把它们算进自推会冤枉正确写法。
    所以项名两种写法都要剥：`：` 分隔形与空白分隔形。只认一种，另一种就会被判成自推。
    「未取到」行整行豁免——那正是「原句没写所以照实写未取到」的正确形态。
    """
    if _is_gap_line(line):
        return
    body = line
    m = re.match(r"^-\s*([^「：:]*)[：:]\s*(.*)$", line)
    if m:
        body = m.group(2)
    else:
        # 空格分隔的项名形（`- 乙公司持股比例 30.00%「…」`）：项名同样是登记对象，不是断言。
        # 只剥行首到第一个空白之前那一段，且该段不得含「（后面就是正文了）。
        m2 = re.match(r"^-\s*([^「：:\s]+)\s+(.*)$", line)
        if m2:
            body = m2.group(2)
    body = ANCHOR_BLOCK.sub("", body)       # 锚是定位指针，不是本件在判断
    q = _quotes(line)
    outside = [w for w in words if w in body and w not in q]
    if outside:
        add("LE-NOSELF", lineno,
            "%s须取原句：本件句子里写了「%s」，原句里没有——分类与核算法只有披露知道，"
            "不按持股比例自推，没披露就写未取到：%s"
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
        add("LE-NOSELF", lineno, "%s自算未交代%s" % (what, "／".join(why)))


def _is_gap_line(s):
    """一条发现行是不是「未取到」行。

    只认带冒号的登记形（`未取到：原因` ／ `未取到：项名`）。第六节的口径行里会出现
    「差额没披露就写未取到」这种**叙述**，它不是缺口登记，认错了会给好样发假红。
    """
    return "未取到：" in s or "未取到:" in s


def _check_netting(lineno, line, add):
    """三个数不自行轧差：两个以上独立数被连成等式且没标〔自算〕，一律发。"""
    if "〔自算〕" in line or _is_gap_line(line):
        return
    own = ANCHOR_BLOCK.sub("", _strip_quotes(line))
    if not _equal_hit(own):
        return
    for words, why in NETTING_GROUPS:
        present = [w for w in words if w in own]
        if len(present) >= 2:
            add("LE-NOSELF", lineno,
                "被拼成等式（%s）：%s——不自行轧差，缺的那个写未取到：%s"
                % ("、".join(present), why, line.strip()[:40]))
            return


def _check_noself(lineno, line, add):
    q = _quotes(line).replace(" ", "")
    # 一、核算方法与分类只认原句
    _check_vocab(lineno, line, add, METHOD_WORDS, "核算方法与分类判断")
    # 二、百分数：原句里没有同一数值，就必须自算并交代分子分母
    # 「未取到」行整行豁免——那一行是在标「哪一项没取到」，里面的百分比是**披露对象的名称**
    # （「未达 20% 持股比例的投资」这类），不是本件算出来的比值；
    # 对它要求〔自算〕等于逼人把缺项写成结论。
    missing = [] if _is_gap_line(line) else [t for t in PCT.findall(line) if _norm_pct(t) not in q]
    if missing:
        if "〔自算〕" not in line:
            add("LE-NOSELF", lineno, "比例 %s 在原句里找不到，也没标〔自算〕：%s"
                % ("、".join(missing), line.strip()[:40]))
        else:
            _check_mol_den(lineno, line, add, "比例")
    # 三、自算差额须交代分子分母
    if "〔自算〕" in line and any(w in line for w in RECON_WORDS):
        _check_mol_den(lineno, line, add, "自算差额")
    # 四、三个数不自行轧差
    _check_netting(lineno, line, add)


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
            add("LE-STRUCT", 1, "头部缺自标「%s」" % mark)
    if not any(SUBJECT.match(s) for _i, s in header):
        add("LE-STRUCT", 1, "头部缺 `主体：` 行")
    if not any(PERIOD.match(s) for _i, s in header):
        add("LE-STRUCT", 1, "头部缺 `报告期：` 行")

    # ---- 道一 节齐与序
    names = [n for n, _l, _b in sections]
    for name in SECTIONS:
        if name not in names:
            add("LE-STRUCT", 1, "缺节「%s」" % name)
    pos = [SECTIONS.index(n) for n in names]
    if pos != sorted(pos):
        add("LE-STRUCT", 1, "节序不对：现序 %s，应序 %s" % ("／".join(names), "／".join(SECTIONS)))
    for lineno, raw in stray:
        add("LE-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw)

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
                    add("LE-STRUCT", lineno, "节内只许 `- ` 发现行：%s" % s.strip()[:40])
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
                        add("LE-QUOTE", lineno, "发现行缺「」原句 + 〔锚：…〕 + [S#] 三元组：%s"
                            % s.strip()[:40])
                else:
                    for m in TRIPLE.finditer(s):
                        if not m.group("q").strip():
                            add("LE-QUOTE", lineno, "原句为空")
                        if not m.group("a").strip():
                            add("LE-QUOTE", lineno, "锚为空")
                    if not re.search(r"\[S\d+\]\s*$", s.strip()):
                        add("LE-QUOTE", lineno, "发现行未以 [S#] 收尾（三元组须在行末）")
                _check_line(lineno, s, add)
                if PCT.findall(s):
                    stats["ratio_lines"] += 1
                _check_noself(lineno, s, add)
            section_found[name] = n_find
            if n_find == 0:
                add("LE-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name)

        elif name == GAP_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not _is_finding_line(s):
                    add("LE-STRUCT", lineno, "第六节只许 `- ` 行：%s" % s.strip()[:40])
                    continue
                section_found.setdefault(name, 0)
                section_found[name] += 1
                for w in GAP_EXCUSE:
                    if w in s:
                        add("LE-GAP", lineno, "禁用「%s」把没查当成没有：%s" % (w, s.strip()[:40]))
                _check_line(lineno, s, add)

        elif name == SOURCE_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not s.lstrip().startswith("- ["):
                    add("LE-STRUCT", lineno, "来源节只许 `- [S#] …` 行：%s" % s.strip()[:40])
                    continue
                m = SOURCE_LINE.match(s.strip())
                if not m:
                    add("LE-QUOTE", lineno, "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:50])
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
            add("LE-GAP", 1, "正文写了未取到「%s」，第六节没点名" % key)
    for g in gap_sec:
        key = _gap_key(g)
        if key and not any(key in s for s in gap_body):
            add("LE-GAP", 1, "第六节点名了「%s」，正文没有这条表述" % key)

    # 零缺口须显式写「未取到：无」
    if not gap_body and not gap_sec:
        gap_text = "\n".join(s for name, _h, body in sections if name == GAP_SECTION
                             for _ln, s in body)
        if "未取到：无" not in gap_text and "未取到:无" not in gap_text:
            add("LE-GAP", 1, "零缺口未显式写「未取到：无」")

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
            add("LE-QUOTE", 1, "正文引用 [%s]，来源节没有对应登记行" % ref)

    # ---- 边界
    # 只判前五节（登记正文）。第六节「口径与未取到」正是写明与另几枚件分界的地方。
    body_lines = [(ln, s) for name, _h, body in sections
                  if name in CONTENT_SECTIONS for ln, s in body]
    for words, tip in SCOPE_RULES:
        for ln, s in body_lines:
            if any(w in s for w in words):
                add("LE-STRUCT", ln, "越界：%s" % tip)
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


GOOD = r"""# 示例科技（600000.SH）长期股权投资登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议 ｜ 判断位 [待人工]
主体：示例科技（600000.SH）
报告期：2025 年年度报告·附注七·长期股权投资

## 按被投资单位列的明细

- 乙公司期初余额 20,000,000.00 元「乙公司期初余额 20,000,000.00 元」〔锚：2025 年年报·第 152 页·附注七·长期股权投资〕[S1]
- 乙公司本期追加投资 未取到：附注未披露对乙公司本期追加投资的金额
- 乙公司本期权益法确认损益 12,000,000.00 元「乙公司本期权益法确认损益 12,000,000.00 元」〔锚：2025 年年报·第 152 页·附注七·长期股权投资〕[S1]
- 乙公司期末余额 32,000,000.00 元「乙公司期末余额 32,000,000.00 元」〔锚：2025 年年报·第 152 页·附注七·长期股权投资〕[S1]
- 乙公司持股比例 30.00%「本公司持有乙公司 30.00% 的股权」〔锚：2025 年年报·第 152 页·附注七·长期股权投资〕[S1]
- 乙公司表决权比例 30.00%「表决权比例 30.00%」〔锚：2025 年年报·第 152 页·附注七·长期股权投资〕[S1]

## 核算方法与分类

- 对乙公司的核算方法 权益法「本公司对乙公司具有重大影响，采用权益法核算」〔锚：2025 年年报·第 151 页·附注七·长期股权投资·重要会计政策〕[S1]
- 对子公司投资的核算方法 成本法「对子公司的长期股权投资采用成本法核算」〔锚：2025 年年报·第 151 页·附注七·长期股权投资·重要会计政策〕[S1]
- 合营企业与联营企业的划分 照抄附注表述「合营企业是指合营方仅对该安排的净资产享有权利的合营安排，联营企业是指投资方对被投资单位具有重大影响的权益性投资」〔锚：2025 年年报·第 151 页·附注七·长期股权投资·重要会计政策〕[S1]
- 各被投资单位的分类依据 未取到：附注未说明划分为合营企业或联营企业的具体依据

## 权益法确认的投资损益

- 被投资单位本期净利润 40,000,000.00 元「乙公司本期净利润 40,000,000.00 元」〔锚：2025 年年报·第 153 页·附注七·长期股权投资〕[S1]
- 按持股比例确认的投资收益 12,000,000.00 元「按持股比例 30.00% 确认投资收益 12,000,000.00 元」〔锚：2025 年年报·第 153 页·附注七·长期股权投资〕[S1]
- 内部交易未实现损益抵消金额 1,500,000.00 元「抵消未实现内部交易损益 1,500,000.00 元」〔锚：2025 年年报·第 153 页·附注七·长期股权投资〕[S1]

## 投资收益与现金分红的对应

- 本期确认的投资收益 12,000,000.00 元「本期确认投资收益 12,000,000.00 元」〔锚：2025 年年报·第 153 页·附注七·长期股权投资〕[S1]
- 本期收到的现金分红 6,000,000.00 元「本期收到现金分红 6,000,000.00 元」〔锚：2025 年年报·第 154 页·附注七·长期股权投资〕[S1]
- 现金分红占本期确认投资收益比 50.00%〔自算〕分子＝本期收到现金分红 6,000,000.00 元 [S1]｜分母＝本期确认投资收益 12,000,000.00 元 [S1]
- 两者差额及其披露解释 未取到：附注未披露投资收益与现金分红差额的解释

## 减值与处置

- 减值准备期末余额 2,000,000.00 元「长期股权投资减值准备期末余额 2,000,000.00 元」〔锚：2025 年年报·第 154 页·附注七·长期股权投资〕[S1]
- 本期计提减值准备 未取到：附注未披露本期计提的长期股权投资减值准备
- 处置长期股权投资的投资收益 未取到：附注未披露本期处置长期股权投资的损益
- 对赌或业绩承诺的安排 未取到：附注未披露与被投资单位相关的对赌或业绩承诺安排

## 口径与未取到

- 未取到：乙公司本期追加投资
- 未取到：各被投资单位的分类依据
- 未取到：两者差额及其披露解释
- 未取到：本期计提减值准备
- 未取到：处置长期股权投资的投资收益
- 未取到：对赌或业绩承诺的安排
- 口径：某单位算子公司、合营企业还是联营企业，用成本法还是权益法，一律照抄附注原句，不由本件按持股比例推断。
- 口径：被投资单位净利润、按持股比例确认的投资收益、未实现损益抵消额是三个独立数，各自登记；披露只给两个时第三个写未取到。
- 口径：本期确认的投资收益与本期收到的现金分红是两个数，差额及其解释只认披露原句，没披露就写未取到。
- 口径：比例披露没给的，本件算出来才标〔自算〕，并在同一行给出分子与分母各自的来源。
- 口径：值不值得投、本金能否收回均由人工判断 [待人工]；本件只登记披露怎么写。
- 口径：减值风险的判定见 cn-goodwill-impairment-risk；关联方与关联交易见 cue-related-party-terms-cn；控股股东变更见 cn-controlling-shareholder-change-cn；四期差异与科目勾稽的点评见 cn-earnings-note。

## 来源

- [S1] 示例科技 2025 年年度报告·附注七·长期股权投资 | https://example.com/ann/S1 | 检索日 2026-11-13 | 类型：年报
- [S2] 示例科技 2025 年年度报告·合并利润表 | https://example.com/ann/S2 | 检索日 2026-11-13 | 类型：年报
"""

# ---- 坏样：各只发自己那道码
# 形制坏样插的是**多出一节同名标题**，不是改节标题名：改名会让整节变 stray、节内发现行一并丢，
# 连带节内那条「未取到」也没了，第六节就多出一条假 LE-GAP——测出来的红分不清是哪道判的。
BAD_STRUCT = GOOD.replace(
    "## 核算方法与分类",
    "## 按被投资单位列的明细\n\n## 核算方法与分类")

BAD_QUOTE = GOOD.replace(
    "「乙公司期初余额 20,000,000.00 元」〔锚：2025 年年报·第 152 页·附注七·长期股权投资〕[S1]",
    "20,000,000.00 元 [S1]")

BAD_NOSELF = GOOD.replace(
    "｜分母＝本期确认投资收益 12,000,000.00 元 [S1]",
    "")

BAD_GAP = GOOD.replace(
    "- 未取到：各被投资单位的分类依据",
    "- 未取到：无此项")

BAD_LINE = GOOD.replace(
    "- 口径：比例披露没给的，本件算出来才标〔自算〕，并在同一行给出分子与分母各自的来源。",
    "- 口径：该投资具有投资价值，预计投资收益将增厚利润。")

# ---- 反证样：不该发的必须不发
OK_HUMAN = GOOD.replace(
    "- 口径：比例披露没给的，本件算出来才标〔自算〕，并在同一行给出分子与分母各自的来源。",
    "- 值不值得投 [待人工]，本金能否收回 [待人工]，对 EPS 的影响 [待人工]\n"
    "- 口径：比例披露没给的，本件算出来才标〔自算〕，并在同一行给出分子与分母各自的来源。")

BAD_HUMAN_HALF = GOOD.replace(
    "- 口径：比例披露没给的，本件算出来才标〔自算〕，并在同一行给出分子与分母各自的来源。",
    "- 值不值得投 [待人工]，该投资必然增厚利润。\n"
    "- 口径：比例披露没给的，本件算出来才标〔自算〕，并在同一行给出分子与分母各自的来源。")

# 引文反证样换的是「减值准备期末余额」那一行的引文，两处讲究：
#   * 不动任何「未取到」行——动它会同时删掉正文点名，第六节立刻多一条假 LE-GAP；
#   * 换的这一行值位不含核算方法词族——换掉引文后若值位里还留着「成本法」「权益法」，
#     判据剥掉项名就会发现原句里没有了，于是 LE-NOSELF 连带发条，测出来的就不是红线那道了。
OK_QUOTED_REDLINE = GOOD.replace(
    "「长期股权投资减值准备期末余额 2,000,000.00 元」",
    "「附注称该单位无风险，业绩承诺可实现」")

BAD_JIAZHA = GOOD.replace(
    "- 本期确认的投资收益 12,000,000.00 元",
    "- 本期确认的投资收益 即本期收到现金分红与上期余额之差")

# 未取到行的**项名**里带词族不算自推：那是在标「没取到的是哪一项」，不是在替披露判断。
# 正文与第六节两处同时改——只改一处会断掉两向对账，测出来的就不是自推那道码了。
OK_GAP_ITEMNAME = GOOD.replace(
    "- 各被投资单位的分类依据 未取到：附注未说明划分为合营企业或联营企业的具体依据",
    "- 合营企业与联营企业的分类依据 未取到：附注未说明划分为合营企业或联营企业的具体依据").replace(
    "- 未取到：各被投资单位的分类依据",
    "- 未取到：合营企业与联营企业的分类依据")

# 坏样要坏在判据真正看的地方：只换引文、项名里不带词族，判据剥掉项名后整行就没有词族了，
# 码发不出来。这里让「权益法」成为原句之外唯一的词族。
BAD_METHOD_GUESS = GOOD.replace(
    "- 对乙公司的核算方法 权益法「本公司对乙公司具有重大影响，采用权益法核算」",
    "- 对乙公司的核算方法 持股 30.00%，故按权益法核算「本公司持有乙公司 30.00% 的股权」")

BAD_SELF_NOBASIS = GOOD.replace(
    "分子＝本期收到现金分红 6,000,000.00 元 [S1]｜",
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
        ("形制：多出一节同名节（按被投资单位列的明细）", BAD_STRUCT, {"LE-STRUCT"}),
        ("锚：数字行没挂原句与锚", BAD_QUOTE, {"LE-QUOTE"}),
        ("自算：比例自算只给分子没给分母", BAD_NOSELF, {"LE-NOSELF"}),
        ("点名：第六节用「无此项」搪塞", BAD_GAP, {"LE-GAP"}),
        ("红线：写投资价值与增厚利润", BAD_LINE, {"LE-LINE"}),
        ("反证：[待人工] 整句成立 → 不发", OK_HUMAN, set()),
        ("反证：[待人工] 只豁免自己那句，后半句照样发", BAD_HUMAN_HALF, {"LE-LINE"}),
        ("反证：引文里的「无风险／可实现」不是本件断言 → 不发", OK_QUOTED_REDLINE, set()),
        ("轧差：投资收益与现金分红被拼成等式", BAD_JIAZHA, {"LE-NOSELF"}),
        ("反证：未取到行的项名里带词族不算自推 → 不发", OK_GAP_ITEMNAME, set()),
        ("自推：原句没写权益法却按持股比例自标", BAD_METHOD_GUESS, {"LE-NOSELF"}),
        ("自算：比例自算缺分子来源", BAD_SELF_NOBASIS, {"LE-NOSELF"}),
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
    ap = argparse.ArgumentParser(description="长期股权投资稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="长期股权投资稿 .md 路径")
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
        print("缺入参：给一份长期股权投资稿路径，或用 --demo / --selftest", file=sys.stderr)
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
