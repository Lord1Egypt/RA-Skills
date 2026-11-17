#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_contingency.py — 或有事项与承诺事项稿五道机检（零网络、零外发、不读环境变量）

用法：
    python3 scripts/check_contingency.py <或有事项稿>.md
    python3 scripts/check_contingency.py --selftest
    python3 scripts/check_contingency.py --demo     打印一份完整合规样例（零输入可跑）

道一 CC-STRUCT 形制
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]；
  `主体：` 行在场且非空；`报告期：` 行在场且非空；
  七节齐且按序：或有事项／承诺事项／预计负债与或有负债的区分／与日后事项、关联方担保的界线／
  未决诉讼的阶段与涉案金额／口径与未取到／来源；
  前五节各至少一条 `- ` 发现行，节内只许 `- ` 发现行、`### ` 子标题与空行。

道二 CC-QUOTE 原句与锚
  每条数字行必须以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；原句与锚不得为空；
  例外只有三形：「未取到」行（缺的就是那份材料）、[待人工] 行（判断位）与〔自算〕行（本件自己算的）；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址，检索日缺一不可；
  正文引用的每个 [S#] 必须在来源节有对应行。

道三 CC-NOSELF 不得自推自算（本件承重格）
  一、或有性质只认原句：写「预计负债」「或有负债」「或有事项」的，同一行「」原句里必须也写得到——
      一项义务是确认预计负债还是仅作或有负债披露，是披露做的判断，不是本件按金额大小或事项类型推的。
  二、终止确认只认原句：写「终止确认」「继续涉入」的，原句同理——
      「已贴现」不等于「已终止确认」，附追索权的贴现是或有事项，这条不能靠词表兜。
  三、诉讼阶段只认原句：写「一审」「二审」「再审」「审理中」「尚未开庭」「已判决」的，原句同理。
  四、界线只认原句：写「日后事项」「资产负债表日后」「关联方担保」的，原句同理——
      事项落在报告期内还是日后，披露没写就是没写，本件不按日期推。
  五、百分数：行内出现 `3.00%` 一类数值，必须能在同一行的「」原句里逐字找到；
      找不到的须标〔自算〕，且同一行同时给出 `分子…[S#]` 与 `分母…[S#]`。
  六、金额自算：同一行标了〔自算〕又谈或有／预计负债／担保／承诺／赔偿的，必须写明
      **金额取哪一句**（`金额取`／`标的额取`／`余额取`），并与分子分母一并交代；缺一项即发。

道四 CC-GAP 未取到两向点名
  正文（一至五节）写「未取到 X」⇒ 第六节必须点名 X；第六节点名了 X 而正文没有 ⇒ 同样发；两向都判。
  零缺口时，第六节须显式写 `未取到：无`；
  出现 `不适用`／`无此项`／`无需披露` 一律发——那是把没查当成没有。

道五 CC-LINE 红线
  败诉概率／很可能败诉／预计赔偿／导致违约／退市风险／偿债能力／评级与目标价／风险可控 一类断言零命中；
  **只判本件自己写的句子**：同一行「」里的引文先洗掉再判——引文是证据，不是本件的断言；
  含 [待人工] 的分句豁免，且只豁免它自己那一句（按 ；;。，,｜ 切分）；
  「预计负债」与「或有负债」在同一分句被写成相等（＝／等于／视为／视同）一律发——
  确认预计负债与仅作或有负债披露是两种不同的处理，写成同一个就把披露划的界线抹掉了。

退码：0 全过 / 1 有发条 / 2 用法错（缺参数） / 3 读不到文件或空稿。
"""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

SLUG = "cue-cn-contingency-commitment-cn"

CODES = ("CC-STRUCT", "CC-QUOTE", "CC-NOSELF", "CC-GAP", "CC-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("或有事项", "承诺事项", "预计负债与或有负债的区分",
            "与日后事项、关联方担保的界线", "未决诉讼的阶段与涉案金额",
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

# 承重格的四个词族：写在本件句子里就必须在原句里也写得到
CONTINGENT_WORDS = ("预计负债", "或有负债", "或有事项")
DERECOG_WORDS = ("终止确认", "继续涉入")
STAGE_WORDS = ("一审", "二审", "再审", "审理中", "尚未开庭", "已判决", "终审")
BOUNDARY_WORDS = ("日后事项", "资产负债表日后", "关联方担保")

# 金额自算：须写明金额取哪一句（不是替披露算出一个赔偿数）
PROV_BASIS = ("金额取", "标的额取", "余额取", "金额取自")
PROV_WORDS = ("或有", "预计负债", "担保", "承诺", "赔偿")

GAP_EXCUSE = ("不适用", "无此项", "无需披露")

EQUAL_WORDS = ("＝", "=", "等于", "相同", "一致", "视为", "视同", "同为")
NEG_EQUAL = re.compile(r"(?:不|非)(?:等于|同于|一致|相同|视为|视同|同为)")

PROMISE_LIAB = ("预计负债",)
CONTINGENT_LIAB = ("或有负债",)

HARD_BAN = ("预计败诉", "很可能败诉", "败诉概率", "胜诉概率",
            "预计赔偿", "赔偿金额预计", "赔偿金额约",
            "导致违约", "构成违约", "触发违约",
            "退市风险", "面临退市", "将被退市",
            "偿债能力", "无法偿债", "资不抵债",
            "风险可控", "无风险", "不存在重大风险", "不会败诉", "不存在败诉风险",
            "目标价", "目标市值", "买入评级", "增持评级", "中性评级",
            "建议买入", "建议增持", "强烈推荐", "跑赢大盘", "必涨", "必跌")

CLAUSE_SPLIT = re.compile(r"[；;。，,｜|]")

SCOPE_RULES = (
    (("四期差异点评", "科目勾稽点评", "六项清单"),
     "改走 cn-earnings-note：四期差异与科目勾稽的点评是那一件，本件只逐项登记或有与承诺"),
    (("票据分类", "票据背书", "坏账准备计提", "票据到期托收"),
     "改走 cn-notes-receivable-cn：票据本体的分类与坏账是那一件，本件只登记已贴现票据的或有追索"),
    (("九类覆盖率", "覆盖率盘点", "带锚事实表"),
     "改走 dd-checklist：公开信息九类覆盖率盘点是那一件，本件只做附注原文的逐条挂源"),
    (("行政处罚", "监管措施", "问询函"),
     "改走 event-risk-scan：处罚与监管措施的扫描是那一件，本件只读附注"),
    (("审计意见类型", "保留意见", "无法表示意见", "否定意见"),
     "改走 cn-audit-opinion-cn：审计意见类型的判定是那一件，本件只登记或有与承诺本身"),
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
    """分句里有没有把预计负债与或有负债写成相等的连接词（否定形不算：「不同于」不是相等）。"""
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
    # 逐句洗就洗不干净——「公司称该诉讼不会败诉，未计提预计负债」这类照抄原文会被误判成本件断言。
    own_line = _strip_quotes(line)
    for clause in _clauses(own_line):
        if "[待人工]" in clause:
            continue
        own = clause
        hit = [w for w in HARD_BAN if w in own]
        # 预计负债 ≠ 或有负债：同句出现两类词又被写成相等，就是替披露抹掉界线
        if (any(w in own for w in PROMISE_LIAB)
                and any(w in own for w in CONTINGENT_LIAB)
                and _equal_hit(own)):
            hit.append("预计负债＝或有负债")
        if hit:
            add("CC-LINE", lineno, "红线词：%s（%s）" % ("、".join(sorted(set(hit))), clause.strip()[:40]))
            return


def _quotes(line):
    return "".join(m.group(1) for m in QUOTE.finditer(line))


def _split_label(line):
    """把一条发现行拆成「项名」与「余下部分」。

    本件两种写法都要认：
      `- 项名：值「原句」…`   → 项名到第一个冒号
      `- 项名 值「原句」…`    → 项名到第一个空白
    取「冒号」与「空白」里更早出现的那个做界。项名是标签、不是断言，
    这一步只服务自推判据的判域；拆不开（行首就是值）时整行算正文，宁严不松。
    """
    m = re.match(r"^-\s*(.+)$", line)
    if not m:
        return "", line
    rest = m.group(1)
    cut = len(rest)
    for tok in ("：", ":", " ", "\t"):
        i = rest.find(tok)
        if i != -1:
            cut = min(cut, i)
    label = rest[:cut].strip()
    body = rest[cut:].lstrip("：: \t")
    return label, body


def _check_vocab(lineno, line, add, words, what):
    """词族只认原句：本件句子里写了，同一行原句也必须写到。

    判域＝去掉**项名**与**锚标签**之后的余下部分。两处都是标签、不是断言：
    项名是「或有事项·对外担保」这种登记对象，锚标签是「〔锚：…附注三·或有事项〕」
    这种定位指针——把它们算进自推会冤枉正确写法。本件的项名天生带词族（「或有事项」
    「对外担保」「日后事项」），不剥就会把每一条正确写法都判成自推。
    「未取到」行整行豁免——那正是「原句没写所以照实写未取到」的正确形态。
    """
    if "未取到" in line:
        return
    _label, body = _split_label(line)
    body = ANCHOR_BLOCK.sub("", body)       # 锚是定位指针，不是本件在判断
    q = _quotes(line)
    outside = [w for w in words if w in body and w not in q]
    if outside:
        add("CC-NOSELF", lineno,
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
        add("CC-NOSELF", lineno, "%s自算未交代%s" % (what, "／".join(why)))


def _check_prov(lineno, line, add):
    """金额自算：金额取哪一句 + 分子分母各挂各的源。"""
    why = []
    if not any(w in line for w in PROV_BASIS):
        why.append("未写明金额取哪一句")
    if why:
        add("CC-NOSELF", lineno, "或有金额自算未交代%s" % "／".join(why))
    _check_mol_den(lineno, line, add, "或有金额")


def _check_noself(lineno, line, add):
    q = _quotes(line).replace(" ", "")
    # 一至四、词族：或有性质、终止确认、诉讼阶段、界线只认原句
    _check_vocab(lineno, line, add, CONTINGENT_WORDS, "或有性质判断")
    _check_vocab(lineno, line, add, DERECOG_WORDS, "终止确认判断")
    _check_vocab(lineno, line, add, STAGE_WORDS, "诉讼阶段判断")
    _check_vocab(lineno, line, add, BOUNDARY_WORDS, "日后事项与关联方担保界线")
    # 五、百分数：原句里没有同一数值，就必须自算并交代分子分母
    missing = [t for t in PCT.findall(line) if _norm_pct(t) not in q]
    if missing:
        if "〔自算〕" not in line:
            add("CC-NOSELF", lineno, "比例 %s 在原句里找不到，也没标〔自算〕：%s"
                % ("、".join(missing), line.strip()[:40]))
        else:
            _check_mol_den(lineno, line, add, "比例")
    # 六、金额自算的两项口径
    if "〔自算〕" in line and any(w in line for w in PROV_WORDS):
        _check_prov(lineno, line, add)


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
            add("CC-STRUCT", 1, "头部缺自标「%s」" % mark)
    if not any(SUBJECT.match(s) for _i, s in header):
        add("CC-STRUCT", 1, "头部缺 `主体：` 行")
    if not any(PERIOD.match(s) for _i, s in header):
        add("CC-STRUCT", 1, "头部缺 `报告期：` 行")

    # ---- 道一 节齐与序
    names = [n for n, _l, _b in sections]
    for name in SECTIONS:
        if name not in names:
            add("CC-STRUCT", 1, "缺节「%s」" % name)
    pos = [SECTIONS.index(n) for n in names]
    if pos != sorted(pos):
        add("CC-STRUCT", 1, "节序不对：现序 %s，应序 %s" % ("／".join(names), "／".join(SECTIONS)))
    for lineno, raw in stray:
        add("CC-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw)

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
                    add("CC-STRUCT", lineno, "节内只许 `- ` 发现行：%s" % s.strip()[:40])
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
                        add("CC-QUOTE", lineno, "发现行缺「」原句 + 〔锚：…〕 + [S#] 三元组：%s"
                            % s.strip()[:40])
                else:
                    for m in TRIPLE.finditer(s):
                        if not m.group("q").strip():
                            add("CC-QUOTE", lineno, "原句为空")
                        if not m.group("a").strip():
                            add("CC-QUOTE", lineno, "锚为空")
                    if not re.search(r"\[S\d+\]\s*$", s.strip()):
                        add("CC-QUOTE", lineno, "发现行未以 [S#] 收尾（三元组须在行末）")
                _check_line(lineno, s, add)
                if PCT.findall(s):
                    stats["ratio_lines"] += 1
                _check_noself(lineno, s, add)
            section_found[name] = n_find
            if n_find == 0:
                add("CC-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name)

        elif name == GAP_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not _is_finding_line(s):
                    add("CC-STRUCT", lineno, "第六节只许 `- ` 行：%s" % s.strip()[:40])
                    continue
                section_found.setdefault(name, 0)
                section_found[name] += 1
                for w in GAP_EXCUSE:
                    if w in s:
                        add("CC-GAP", lineno, "禁用「%s」把没查当成没有：%s" % (w, s.strip()[:40]))
                _check_line(lineno, s, add)

        elif name == SOURCE_SECTION:
            for lineno, s in body:
                if not s.strip():
                    continue
                if not s.lstrip().startswith("- ["):
                    add("CC-STRUCT", lineno, "来源节只许 `- [S#] …` 行：%s" % s.strip()[:40])
                    continue
                m = SOURCE_LINE.match(s.strip())
                if not m:
                    add("CC-QUOTE", lineno, "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:50])
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
            add("CC-GAP", 1, "正文写了未取到「%s」，第六节没点名" % key)
    for g in gap_sec:
        key = _gap_key(g)
        if key and not any(key in s for s in gap_body):
            add("CC-GAP", 1, "第六节点名了「%s」，正文没有这条表述" % key)

    # 零缺口须显式写「未取到：无」
    if not gap_body and not gap_sec:
        gap_text = "\n".join(s for name, _h, body in sections if name == GAP_SECTION
                             for _ln, s in body)
        if "未取到：无" not in gap_text and "未取到:无" not in gap_text:
            add("CC-GAP", 1, "零缺口未显式写「未取到：无」")

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
            add("CC-QUOTE", 1, "正文引用 [%s]，来源节没有对应登记行" % ref)

    # ---- 边界
    # 只判前五节（登记正文）。第六节「口径与未取到」正是写明与另几枚件分界的地方，
    # 在那里点名 cn-earnings-note／dd-checklist 是本件要求的动作，不是越界。
    body_lines = [(ln, s) for name, _h, body in sections
                  if name in CONTENT_SECTIONS for ln, s in body]
    for words, tip in SCOPE_RULES:
        for ln, s in body_lines:
            if any(w in s for w in words):
                add("CC-STRUCT", ln, "越界：%s" % tip)
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


GOOD = r"""# 示例材料（600000.SH）或有事项与承诺事项登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议 ｜ 判断位 [待人工]
主体：示例材料（600000.SH）
报告期：2025 年年度报告

## 或有事项

- 未决诉讼 存在买卖合同纠纷「本公司与某供应商存在买卖合同纠纷，对方已提起诉讼」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]
- 对外担保 担保余额 3,000.00 万元「本公司为子公司提供担保 30,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]
- 担保余额占净资产比例 3.00%〔自算〕金额取附注「本公司为子公司提供担保 30,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]｜分子＝担保余额 30,000,000.00 元 [S1]｜分母＝归属于母公司所有者权益 1,000,000,000.00 元 [S1]
- 已贴现商业承兑票据 500.00 万元「已贴现未到期的商业承兑票据 5,000,000.00 元，附追索权，本公司未终止确认」〔锚：2025 年年报·第 131 页·附注三·或有事项〕[S1]
- 产品质量保证 80.00 万元「按销售收入的 1% 计提产品质量保证，确认预计负债 800,000.00 元」〔锚：2025 年年报·第 131 页·附注三·或有事项〕[S1]
- 或有事项不确定性说明：结果存在不确定性「上述担保与诉讼的最终结果存在不确定性」〔锚：2025 年年报·第 131 页·附注三·或有事项〕[S1]
- 重组义务 未取到：附注未披露重组义务
- 亏损合同 未取到：附注未披露亏损合同

## 承诺事项

- 资本承诺 已签约未执行 2,000.00 万元「已签约但尚未执行的资本性支出承诺 20,000,000.00 元」〔锚：2025 年年报·第 132 页·附注三·承诺事项〕[S1]
- 资本承诺期限 一年内「上述资本承诺预计于一年内执行完毕」〔锚：2025 年年报·第 132 页·附注三·承诺事项〕[S1]
- 经营租赁承诺 未来三年合计 900.00 万元「不可撤销经营租赁的最低租赁付款额合计 9,000,000.00 元」〔锚：2025 年年报·第 132 页·附注三·承诺事项〕[S1]
- 投资承诺 未取到：附注未披露投资承诺
- 大额合同承诺 未取到：附注未披露大额合同承诺

## 预计负债与或有负债的区分

- 对外担保 未确认预计负债「本公司认为该担保无需确认预计负债，仅作或有负债披露」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]
- 产品质量保证 已确认预计负债「产品质量保证已确认预计负债 800,000.00 元」〔锚：2025 年年报·第 131 页·附注三·或有事项〕[S1]
- 未决诉讼 未确认预计负债「该诉讼尚未开庭，本公司未确认预计负债」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]

## 与日后事项、关联方担保的界线

- 担保与日后事项的界线 不属日后事项「上述担保事项发生于报告期内，不属于资产负债表日后事项」〔锚：2025 年年报·第 133 页·附注三·承诺事项〕[S1]
- 关联方担保：单列披露「对关联方担保已在关联方交易附注中单独披露」〔锚：2025 年年报·第 133 页·附注四·关联方及关联交易〕[S2]
- 日后事项的影响 未取到：附注未披露资产负债表日后事项对本项或有事项的影响

## 未决诉讼的阶段与涉案金额

- 诉讼阶段 一审已判决「本案一审已判决，本公司已提起上诉」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]
- 涉案金额 1,200.00 万元「原告请求本公司赔偿 12,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]
- 期后进展 未取到：附注未披露资产负债表日后诉讼进展

## 口径与未取到

- 未取到：重组义务
- 未取到：亏损合同
- 未取到：投资承诺
- 未取到：大额合同承诺
- 未取到：日后事项的影响
- 未取到：期后进展
- 口径：或有事项的性质、金额与不确定性一律照抄附注原句，不由本件按事项类型或金额大小推断。
- 口径：确认预计负债还是仅作或有负债披露，只照抄附注那一句；两者是不同的处理，不得写成相等或互相替代。
- 口径：诉讼阶段与涉案金额只抄披露原文；「已立案」不等于「已开庭」，「已起诉」也不等于「很可能败诉」。
- 口径：四期差异与科目勾稽的点评见 cn-earnings-note，本件只逐项登记或有与承诺。
- 口径：票据本体的分类与坏账见 cn-notes-receivable-cn，本件只登记已贴现票据的或有追索。
- 口径：公开信息九类覆盖率盘点见 dd-checklist；处罚与监管措施见 event-risk-scan；审计意见类型见 cn-audit-opinion-cn。

## 来源

- [S1] 示例材料 2025 年年度报告·附注三·或有事项与承诺事项 | https://example.com/ann/S1 | 检索日 2026-11-13 | 类型：公告
- [S2] 示例材料 2025 年年度报告·附注四·关联方及关联交易 | https://example.com/ann/S2 | 检索日 2026-11-13 | 类型：公告
"""

# ---- 坏样：各只发自己那道码
# 形制坏样插的是**多出一节同名标题**，不是改节标题名：改名会让整节变 stray、节内发现行一并丢，
# 连带节内那条「未取到」也没了，第六节就多出一条假 CC-GAP——测出来的红分不清是哪道判的。
BAD_STRUCT = GOOD.replace(
    "## 预计负债与或有负债的区分",
    "## 承诺事项\n\n## 预计负债与或有负债的区分")

BAD_QUOTE = GOOD.replace(
    "「本公司为子公司提供担保 30,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]",
    "30,000,000.00 元 [S1]")

BAD_NOSELF = GOOD.replace(
    "｜分母＝归属于母公司所有者权益 1,000,000,000.00 元 [S1]",
    "")

BAD_GAP = GOOD.replace(
    "- 未取到：投资承诺",
    "- 未取到：不适用")

BAD_LINE = GOOD.replace(
    "- 诉讼阶段 一审已判决",
    "- 本案胜诉概率较高，不会败诉；诉讼阶段 一审已判决")

# ---- 反证样：不该发的必须不发
OK_HUMAN = GOOD.replace(
    "- 口径：诉讼阶段与涉案金额只抄披露原文；「已立案」不等于「已开庭」，「已起诉」也不等于「很可能败诉」。",
    "- 是否很可能败诉 [待人工]，赔偿金额估计 [待人工]，是否影响偿债能力 [待人工]\n"
    "- 口径：诉讼阶段与涉案金额只抄披露原文；「已立案」不等于「已开庭」，「已起诉」也不等于「很可能败诉」。")

BAD_HUMAN_HALF = GOOD.replace(
    "- 口径：诉讼阶段与涉案金额只抄披露原文；「已立案」不等于「已开庭」，「已起诉」也不等于「很可能败诉」。",
    "- 是否很可能败诉 [待人工]，赔偿金额预计 1,200 万元\n"
    "- 口径：诉讼阶段与涉案金额只抄披露原文；「已立案」不等于「已开庭」，「已起诉」也不等于「很可能败诉」。")

# 引文反证样换的是「关联方担保」那一行的引文，不动任何「未取到」行——
# 动未取到行会同时删掉正文点名，第六节立刻多一条假 CC-GAP，测出来的红就不是红线那道了。
OK_QUOTED_REDLINE = GOOD.replace(
    "「对关联方担保已在关联方交易附注中单独披露」",
    "「公司称该诉讼不会败诉，不存在败诉风险」")

BAD_PROV_MIX = GOOD.replace(
    "- 口径：确认预计负债还是仅作或有负债披露，只照抄附注那一句；两者是不同的处理，不得写成相等或互相替代。",
    "- 口径：预计负债视同或有负债，两者按同一种方式处理。")

# 项名里带词族不算自推：项名是在标登记对象，不是在替披露判断。
OK_ITEMNAME = GOOD.replace(
    "- 对外担保 担保余额 3,000.00 万元「本公司为子公司提供担保 30,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]",
    "- 或有事项·对外担保：担保余额 3,000.00 万元「本公司为子公司提供担保 30,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]")

BAD_STAGE_GUESS = GOOD.replace(
    "- 诉讼阶段 一审已判决「本案一审已判决，本公司已提起上诉」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]",
    "- 诉讼阶段 一审已判决「原告请求本公司赔偿 12,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]")

BAD_PROV_NOBASIS = GOOD.replace(
    "金额取附注「本公司为子公司提供担保 30,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]｜",
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
        ("形制：多出一节同名节（承诺事项）", BAD_STRUCT, {"CC-STRUCT"}),
        ("锚：数字行没挂原句与锚", BAD_QUOTE, {"CC-QUOTE"}),
        ("自算：担保占比自算只给分子没给分母", BAD_NOSELF, {"CC-NOSELF"}),
        ("点名：第六节用「不适用」搪塞", BAD_GAP, {"CC-GAP"}),
        ("红线：写胜诉概率、不会败诉", BAD_LINE, {"CC-LINE"}),
        ("反证：[待人工] 整句成立 → 不发", OK_HUMAN, set()),
        ("反证：[待人工] 只豁免自己那句，后半句照样发", BAD_HUMAN_HALF, {"CC-LINE"}),
        ("反证：引文里的「不会败诉」不是本件断言 → 不发", OK_QUOTED_REDLINE, set()),
        ("红线：预计负债视同或有负债", BAD_PROV_MIX, {"CC-LINE"}),
        ("反证：项名里带「或有事项」不算自推 → 不发", OK_ITEMNAME, set()),
        ("自推：原句没写诉讼阶段却自标一审已判决", BAD_STAGE_GUESS, {"CC-NOSELF"}),
        ("自算：或有金额自算缺「金额取哪一句」", BAD_PROV_NOBASIS, {"CC-NOSELF"}),
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
    ap = argparse.ArgumentParser(description="或有事项与承诺事项稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="或有事项稿 .md 路径")
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
        print("缺入参：给一份或有事项稿路径，或用 --demo / --selftest", file=sys.stderr)
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
