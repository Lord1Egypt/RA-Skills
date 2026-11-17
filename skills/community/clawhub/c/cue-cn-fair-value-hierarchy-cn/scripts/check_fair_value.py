#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_fair_value.py — 公允价值层次登记稿五道机检（零网络、零外发、不读环境变量）

**五道全已落字**：FV-STRUCT（形制）、FV-QUOTE（原句与锚）、FV-LEVEL（三层次归类）、
FV-TECH（估值技术与输入值）、FV-LINE（红线）。`UNIMPLEMENTED` 已清空，
单稿零发条退 0——rc=0 就是「五道全过」，不再有「零发条但有道没跑」的中间态。

用法：
    python3 scripts/check_fair_value.py <公允价值层次登记稿>.md
    python3 scripts/check_fair_value.py --selftest      跑包内夹具自检
    python3 scripts/check_fair_value.py --demo          打印一份合规样例（零输入可跑）

七节（按序，`## ` 起节）：
    公允价值计量概况／公允价值层次归属／估值技术与输入值／层次间转换
    ／第三层次变动／口径与未取到／来源

五道码：

道一 FV-STRUCT 形制（已落字）
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／
  判断位 [待人工]；`主体：` 行、`报告期：` 行在场且非空；七节齐且按序；前五节各至少一条
  `- ` 发现行；「口径与未取到」与「来源」两节不得为空；认不出的节标题与多出的同名节逐条发。

道二 FV-QUOTE 原句与锚（已落字）
  每条发现行以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；缺哪件点名哪件；
  例外只有三形：「未取到：」行、[待人工] 行与〔自算〕行；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址；
  发现行收尾的 [S#] 必须在来源节有对应登记行；来源节一条合规来源行都没有则单独发一条。

道三 FV-LEVEL 三层次归类只认原句（已落字）
  只判「公允价值层次归属」节：登记值写了第几层次（汉字或阿拉伯数字写法），同行「」原句
  必须出现同一个层次词，否则发。漏登记（原句有层次、登记值没写）不判。

道四 FV-TECH 估值技术与输入值只认原句（已落字）
  只判「估值技术与输入值」节：登记值里的市场法／收益法／成本法、可观察／不可观察输入值
  须逐个在同行「」原句找到同词；「不可观察输入值」含「可观察输入值」子串，按整词前缀判。

道五 FV-LINE 红线（已落字）
  轧账词（净额／轧差／相抵／合计影响）只在发现行正文里判；「口径与未取到」整节豁免。
  估值意见（估值偏高／偏低／合理、应该用、建议采用）与评级目标价（目标价、买入、增持、
  减持、评级为）全文命中即发。

退码：0 五道全过 / 1 有发条 / 2 用法错（缺参数或未知参数） / 3 读不到文件或空稿。
"""

import argparse
import contextlib
import io
import os
import re
import sys
import tempfile

SLUG = "cue-cn-fair-value-hierarchy-cn"

CODES = ("FV-STRUCT", "FV-QUOTE", "FV-LEVEL", "FV-TECH", "FV-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("公允价值计量概况", "公允价值层次归属", "估值技术与输入值", "层次间转换",
            "第三层次变动", "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"
LEVEL_SECTION = "公允价值层次归属"
TECH_SECTION = "估值技术与输入值"

# 五道全已落字：清单清空是「零发条即合规」的前提。只要还留着一个码在这里，
# 单稿零发条也只能退 3（不可判），不许读成过。
UNIMPLEMENTED = ()

HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")
SUBJECT = re.compile(r"^主体：\s*(\S.*)$")
PERIOD = re.compile(r"^报告期：\s*(\S.*)$")

TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
ANCHOR_BLOCK = re.compile(r"〔\s*锚\s*[:：][^〕]*〕")
ANCHOR_REF = re.compile(r"\[(S\d+)\]")
REF_TAIL = re.compile(r"\[(S\d+)\]\s*$")

SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)"
    r"\|\s*(?P<url>https?://\S+)\s*\|"
    r"\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$"
)

# 第 X 层次：汉字与阿拉伯写法归一（「第 1 层次」≡「第一层次」），只认这三个层次名。
LEVEL_WORD = re.compile(r"第\s*([一二三1-3])\s*层次")
LEVEL_CN = {"1": "一", "2": "二", "3": "三"}

TECH_WORDS = ("市场法", "收益法", "成本法")
# 「不可观察输入值」包含「可观察输入值」这串子串，裸 in 会把前者误判成后者的命中；
# 顺序上先判长词，短词另由 _has_input_word 按「前面是否带『不』」整词判。
INPUT_WORDS = ("不可观察输入值", "可观察输入值")

CASH_WORDS = ("净额", "轧差", "相抵", "合计影响")
OPINION_WORDS = ("估值偏高", "估值偏低", "估值合理", "应该用", "建议采用")
RATING_WORDS = ("目标价", "买入", "增持", "减持", "评级为")


# ---------------------------------------------------------------- 判据

def _not_judged(code, why):
    """空壳的唯一出口：抛未落字，由 check_text 捕获计入「不可判」，不返回空表。"""
    raise NotImplementedError("%s 未落字：%s" % (code, why))


def check_struct(head, sections, stray):
    """道一 FV-STRUCT 形制：头部四件自标与两行、七节齐且按序、节内是否有发现行。

    只判「形」：节名在不在、顺序对不对、内容节里有没有发现行、两节尾部有没有内容。
    判内容对不对是另四道的事——这里不越界，否则一支注入会同时红两道、分不清归属。
    """
    out = []
    htext = "\n".join(s for _i, s in head)
    for mark in MARK_TEXTS:
        if mark not in htext:
            out.append(("FV-STRUCT", 1, "头部缺自标「%s」" % mark))
    if not any(SUBJECT.match(s.strip()) for _i, s in head):
        out.append(("FV-STRUCT", 1, "头部缺 `主体：` 行"))
    if not any(PERIOD.match(s.strip()) for _i, s in head):
        out.append(("FV-STRUCT", 1, "头部缺 `报告期：` 行"))

    # 丙：野节（认不出的节名／多出的同名节）逐条报，行号用 stray 给的
    for lineno, raw in stray:
        out.append(("FV-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw))

    # 丁：七节须齐且按序
    names = [n for n, _l, _b in sections]
    missing = [n for n in SECTIONS if n not in names]
    if missing:
        out.append(("FV-STRUCT", 1, "缺节：%s" % "／".join(missing)))
    elif names != list(SECTIONS):
        out.append(("FV-STRUCT", 1, "节序不对：现序 %s，应序 %s"
                    % ("／".join(names), "／".join(SECTIONS))))

    # 戊：五个内容节各至少一条发现行；己：两节尾部不得为空
    for name, hline, body in sections:
        if name in CONTENT_SECTIONS:
            if not any(_is_finding_line(s) for _i, s in body):
                out.append(("FV-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name))
        elif name in (GAP_SECTION, SOURCE_SECTION):
            if not any(s.strip() for _i, s in body):
                out.append(("FV-STRUCT", hline, "节「%s」为空" % name))
    return out


def check_quote(head, sections, stray):
    """道二 FV-QUOTE 原句与锚：来源行格式、发现行三元组、[S#] 两向对应。

    例外只有三形：「未取到：」行、[待人工] 行、〔自算〕行——前两者是缺口与判断位，
    后者已经必须交代算法与口径，要求它再挂原句等于把自算伪装成披露值。
    空来源节／没有来源节不在这里报（那是道一的事），这里只判格式与对应，不许崩。
    """
    out = []
    registered, reported_missing = set(), set()

    # 甲：来源行格式，只扫来源节；不合规的行照样报，但不进 registered。
    # 非 `- ` 行也报：道一只管来源节空不空，行形制若不在这里收，就会两头都没人管。
    for name, _hline, body in sections:
        if name != SOURCE_SECTION:
            continue
        for lineno, s in body:
            if not s.strip():
                continue
            if not _is_finding_line(s):
                out.append(("FV-QUOTE", lineno,
                            "来源节只许 `- [S#] 标题 | URL | 检索日` 行：%s" % s.strip()[:44]))
                continue
            m = SOURCE_LINE.match(s.strip())
            if not m:
                out.append(("FV-QUOTE", lineno,
                            "来源行缺 URL 或检索日 YYYY-MM-DD：%s" % s.strip()[:44]))
                continue
            registered.add(m.group("s"))

    # 乙：发现行三元组，只扫五个内容节
    has_source = any(name == SOURCE_SECTION for name, _l, _b in sections)
    for name, _hline, body in sections:
        if name not in CONTENT_SECTIONS:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue                     # 形制那道会发，这里不重复
            if _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s:
                continue                     # 缺口登记、人工位、自算行本来就不挂三元组
            if not TRIPLE.search(s):
                miss = []
                if not QUOTE.search(s):
                    miss.append("「」原句")
                if not ANCHOR_BLOCK.search(s):
                    miss.append("〔锚：…〕")
                if not ANCHOR_REF.search(s):
                    miss.append("[S#]")
                out.append(("FV-QUOTE", lineno,
                            "发现行缺 %s（三元组须在行末）"
                            % "、".join(miss or ["「」原句 + 〔锚〕 + [S#] 的次序"])))
                continue
            m = REF_TAIL.search(s.strip())
            if not m:
                out.append(("FV-QUOTE", lineno,
                            "发现行未以 [S#] 收尾（三元组须在行末）"))
                continue
            # 没有来源节、或来源节里一条合规行都没有时，同一个根因会在每一行重复铺开，
            # 把「哪一行真有问题」淹掉：根因由道一（缺节）或本道丙（零合规来源行）点一次。
            if not has_source or not registered:
                continue
            ref = m.group(1)
            if ref in registered or ref in reported_missing:
                continue                     # 同一个未登记 S 号只报一次，行号取首次引用处
            reported_missing.add(ref)
            out.append(("FV-QUOTE", lineno,
                        "引用了未登记的 [%s]：来源节没有该 S 号的合规来源行" % ref))

    # 丙：来源节存在但一条合规来源行都没有——只在节在场时报，缺节归道一
    if has_source and not registered:
        out.append(("FV-QUOTE", 1,
                    "来源节没有一条合规来源行：每个 [S#] 都要有可点 http(s) URL 与检索日"))
    return out


def check_level(head, sections, stray):
    """道三 FV-LEVEL 三层次归类只认原句。

    只判「公允价值层次归属」节：登记值里写了第几层次，同行「」原句里就得有同一个词。
    漏登记（原句写了层次、登记值没写）**不判**——那是本件没抄全，不是凭空归层，越界会误伤。
    没有「」原句的行也跳过：缺原句归 FV-QUOTE，同一行发两道会分不清归属。
    """
    out = []
    for lineno, s in _section_lines(sections, LEVEL_SECTION):
        if not _is_finding_line(s):
            continue
        reg, quote = _reg_and_quote(s)
        if reg is None or quote is None:
            continue
        reg_words = _level_words(reg)
        if not reg_words:
            continue
        quote_words = _level_words(quote)
        for w in sorted(reg_words - quote_words):
            out.append(("FV-LEVEL", lineno,
                        "登记值写了第%s层次、原句没有：%s" % (w, s.strip()[:44])))
    return out


def check_tech(head, sections, stray):
    """道四 FV-TECH 估值技术与输入值只认原句。

    只判「估值技术与输入值」节：登记值里的技术词（市场法／收益法／成本法）与输入值词
    （可观察／不可观察输入值）必须逐个在同行「」原句里找到。
    输入值词按整词判：「不可观察输入值」包含「可观察输入值」这串子串，用裸 in 会把
    原句的「不可观察」误判成登记「可观察」的命中；所以「可观察」前面带「不」的那一处不算。
    两边都没有技术词的行不判；没有「」原句的行跳过（缺原句归 FV-QUOTE）。
    """
    out = []
    for lineno, s in _section_lines(sections, TECH_SECTION):
        if not _is_finding_line(s):
            continue
        reg, quote = _reg_and_quote(s)
        if reg is None or quote is None:
            continue
        for w in TECH_WORDS:
            if w in reg and w not in quote:
                out.append(("FV-TECH", lineno,
                            "登记值写了「%s」、原句没有：%s" % (w, s.strip()[:44])))
        for w in INPUT_WORDS:
            if not _has_input_word(reg, w):
                continue
            if not _has_input_word(quote, w):
                out.append(("FV-TECH", lineno,
                            "登记值写了「%s」、原句没有同词（不可观察≠可观察）：%s"
                            % (w, s.strip()[:44])))
    return out


def check_line(head, sections, stray):
    """道五 FV-LINE 红线：轧账、估值意见、评级目标价。

    轧账词只在发现行正文里判（节名与散文里出现「合计影响」这类词不算本件在轧账）；
    「口径与未取到」整节豁免——那节本来就要写「不轧净额」交代口径，判它等于判自己。
    估值意见与评级目标价是全稿红线，头部、各节散文都算。
    """
    out = []
    sec_of = {}
    for name, _hline, body in sections:
        for lineno, _s in body:
            sec_of[lineno] = name
    for lineno, s in _all_lines(head, sections, stray):
        if sec_of.get(lineno) == GAP_SECTION:
            continue
        hit = [w for w in OPINION_WORDS + RATING_WORDS if w in s]
        if _is_finding_line(s.strip()) or s.startswith("-"):
            hit = [w for w in CASH_WORDS if w in s] + hit
        if hit:
            seen = []
            for w in hit:
                if w not in seen:
                    seen.append(w)
            out.append(("FV-LINE", lineno,
                        "红线词「%s」：%s" % ("、".join(seen), s.strip()[:44])))
    return out


CHECKS = (
    ("FV-STRUCT", check_struct),
    ("FV-QUOTE", check_quote),
    ("FV-LEVEL", check_level),
    ("FV-TECH", check_tech),
    ("FV-LINE", check_line),
)


# ---------------------------------------------------------------- 道具

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

    野节＝不认识的节名，或多出来的同名节。它们**另记**、不吞进上一节。
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


def _is_gap_line(s):
    """缺口行：本件没取到、如实登记的那种行（`未取到：X`）。缺口不挂原句与锚。"""
    return "未取到" in s


def _section_lines(sections, name):
    """某一节的全部行；节不在场就是空——缺节归 FV-STRUCT，这里不重复报。"""
    for sname, _hline, body in sections:
        if sname == name:
            return list(body)
    return []


def _reg_and_quote(s):
    """→ (登记值, 该行第一段「」原句)；没有「」原句时原句为 None，整行认不出时登记值为 None。

    登记值＝第一个「」原句之前的部分再剥掉行首 `- `。原句缺不缺归 FV-QUOTE：
    没有原句的行在道三道四里整行跳过，免得同一处缺件被两道各发一次、分不清归属。
    """
    line = s.lstrip()
    if line.startswith("- "):
        line = line[2:]
    elif line == "-":
        return None, None
    m = QUOTE.search(line)
    if not m:
        return line.strip(), None
    return line[:m.start()].strip(), m.group(1)


def _level_words(text):
    """文本里出现的层次名（归一成汉字「一／二／三」），用于两端同词比对。"""
    return {LEVEL_CN.get(g, g) for g in LEVEL_WORD.findall(text)}


def _has_input_word(text, word):
    """整词判输入值词：判「可观察输入值」时要排除「不可观察输入值」里的那一处。"""
    start = 0
    while True:
        i = text.find(word, start)
        if i < 0:
            return False
        if word == "可观察输入值" and i > 0 and text[i - 1] == "不":
            start = i + len(word)
            continue
        return True


def _all_lines(head, sections, stray):
    """全稿逐行：头部＋各节＋野节，行号全局唯一，供全文红线扫描用。"""
    out = list(head)
    for _name, _hline, body in sections:
        out.extend(body)
    return out


def check_text(text):
    """→ (findings[(code, line, msg)], unjudged[(code, why)])。

    空壳抛 NotImplementedError 一律计入 unjudged，**不计入「零发条」**、也不裸抛；
    不在 UNIMPLEMENTED 里的码抛未落字则按「声明与实装不符」直接发条。
    """
    head, sections, stray = split_doc(text)
    findings, unjudged = [], []
    for code, fn in CHECKS:
        try:
            found = fn(head, sections, stray) or []
            findings.extend(found)
        except NotImplementedError as exc:
            if code in UNIMPLEMENTED:
                unjudged.append((code, str(exc)))
            else:
                findings.append((code, 1, "判据不在未落字清单里却抛未落字：%s" % exc))
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


DEMO = r"""# 示例材料（600000.SH）公允价值层次登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议 ｜ 判断位 [待人工]
主体：示例材料（600000.SH）
报告期：2025 年年度报告·附注十·公允价值的披露

## 公允价值计量概况

- 持续计量 合计 32.00 亿元「截至 2025 年 12 月 31 日，本集团以公允价值持续计量的资产合计人民币 32.00 亿元」〔锚：2025 年年报·第 240 页·附注十·公允价值的披露〕[S1]
- 非持续计量 合计 4.50 亿元「本集团以公允价值非持续计量的资产合计人民币 4.50 亿元，为持有待售的处置组」〔锚：2025 年年报·第 240 页·附注十·公允价值的披露〕[S1]

## 公允价值层次归属

- 上市公司股票 第一层次 12.00 亿元「上市公司股票按活跃市场报价计量，期末公允价值 12.00 亿元，归属于第一层次」〔锚：2025 年年报·第 241 页·附注十·公允价值的披露〕[S1]
- 理财产品 第二层次 15.00 亿元「理财产品按同类产品可观察报价与收益率曲线计量，期末公允价值 15.00 亿元，归属于第二层次」〔锚：2025 年年报·第 241 页·附注十·公允价值的披露〕[S1]
- 非上市股权 第三层次 5.00 亿元「非上市股权投资采用不可观察输入值计量，期末公允价值 5.00 亿元，归属于第三层次」〔锚：2025 年年报·第 241 页·附注十·公允价值的披露〕[S1]

## 估值技术与输入值

- 上市公司股票 市场法「上市公司股票采用市场法估值，以活跃市场报价作为输入值」〔锚：2025 年年报·第 242 页·附注十·公允价值的披露〕[S1]
- 理财产品 收益法「理财产品采用收益法估值，输入值为同类产品报价与国债收益率曲线，均属可观察输入值」〔锚：2025 年年报·第 242 页·附注十·公允价值的披露〕[S1]
- 非上市股权 市场法「非上市股权投资采用市场法估值，输入值为可比公司市盈率与流动性折扣，均属不可观察输入值」〔锚：2025 年年报·第 242 页·附注十·公允价值的披露〕[S1]

## 层次间转换

- 转入第二层次 2.00 亿元「本期有 2.00 亿元理财产品由第一层次转入第二层次，原因为该产品市场报价不再活跃」〔锚：2025 年年报·第 243 页·附注十·公允价值的披露〕[S1]
- 转出第三层次 0.00 亿元「本期无自第三层次转出的金额」〔锚：2025 年年报·第 243 页·附注十·公允价值的披露〕[S1]

## 第三层次变动

- 期初余额 6.00 亿元「第三层次公允价值计量项目的期初余额为人民币 6.00 亿元」〔锚：2025 年年报·第 244 页·附注十·公允价值的披露〕[S1]
- 当期损益 0.50 亿元「本期计入当期损益的第三层次公允价值变动为人民币 0.50 亿元」〔锚：2025 年年报·第 244 页·附注十·公允价值的披露〕[S1]
- 期末余额 5.00 亿元「第三层次公允价值计量项目的期末余额为人民币 5.00 亿元」〔锚：2025 年年报·第 244 页·附注十·公允价值的披露〕[S1]

## 口径与未取到

- 未取到：无
- 口径：三个层次的归属、估值技术与输入值、层次间转换、第三层次变动一律照抄附注原文；本件不按资产类别自行归层、不按比率反推公允价值、不评价层次划分是否恰当。

## 来源

- [S1] 示例材料 2025 年年度报告 | https://example.invalid/600000_2025_annual.pdf | 检索日 2026-03-20
"""


def _must_replace(text, old, new, count=1):
    """注入点必须落地：片段不在源件、或替换后字节没变，一律 raise，不静默放过。

    静默放过的注入会让坏样等于好样，那一档就永远「过」——比不合更坏。
    """
    n = text.count(old)
    if n < count:
        raise AssertionError("注入点未落地：片段出现 %d 次，至少要 %d 次：%r" % (n, count, old))
    out = text.replace(old, new, count)
    if out == text:
        raise AssertionError("注入后字节未变：%r -> %r" % (old, new))
    return out


# 坏样都由好样单向替换而来，只动那一档真正看的那一处。
# 道一（a）头部少一件自标。
BAD_MARK = _must_replace(DEMO, " ｜ 不构成投资建议", "", 1)
# 道一（b）一个节标题写成认不出的样子：该节既进不了 sections（算缺节），标题本身也进 stray。
BAD_HEADING = _must_replace(DEMO, "## 层次间转换\n", "## 层次间转换表\n", 1)
# 道一（c）整节删掉「来源」（连标题与来源行）：七节不齐、来源节为空。
BAD_SOURCE = _must_replace(
    DEMO,
    "## 来源\n"
    "\n"
    "- [S1] 示例材料 2025 年年度报告 | "
    "https://example.invalid/600000_2025_annual.pdf | 检索日 2026-03-20\n",
    "", 1)

# 道二（a）整段「」+〔锚〕摘掉、只留收尾 [S1]（原句与锚都没了，行形制仍合规）。
NO_TRIPLE = _must_replace(
    DEMO,
    "「上市公司股票采用市场法估值，以活跃市场报价作为输入值」"
    "〔锚：2025 年年报·第 242 页·附注十·公允价值的披露〕",
    "", 1)
# 道二（b）来源行检索日写成斜杠式，该行不合格式、S1 不再算登记（只坏来源行，不动正文）。
BAD_SOURCE_FMT = _must_replace(
    DEMO,
    "https://example.invalid/600000_2025_annual.pdf | 检索日 2026-03-20",
    "https://example.invalid/600000_2025_annual.pdf | 检索日 2026/03/20", 1)
# 道二（c）正文引 [S9]，来源节只有 S1。
BAD_REF = _must_replace(
    DEMO,
    "均属不可观察输入值」〔锚：2025 年年报·第 242 页·附注十·公允价值的披露〕[S1]",
    "均属不可观察输入值」〔锚：2025 年年报·第 242 页·附注十·公允价值的披露〕[S9]", 1)

# 道三（a）登记值写了第三层次，原句里把「归属于第三层次」删净：层次是自行归的。
BAD_LEVEL = _must_replace(
    DEMO,
    "非上市股权投资采用不可观察输入值计量，期末公允价值 5.00 亿元，归属于第三层次",
    "非上市股权投资采用不可观察输入值计量，期末公允价值 5.00 亿元", 1)

# 道四（a）登记值写「收益法」，原句仍写「市场法」：技术是替发行人挑的。
BAD_TECH = _must_replace(
    DEMO,
    "非上市股权 市场法「非上市股权投资采用市场法估值",
    "非上市股权 收益法「非上市股权投资采用市场法估值", 1)
# 道四（b）原句「均属不可观察输入值」，登记值写「可观察输入值」：前缀整词判，不许被子串蒙过去。
BAD_TECH_INPUT = _must_replace(
    DEMO,
    "- 非上市股权 市场法「非上市股权投资",
    "- 非上市股权 市场法 可观察输入值「非上市股权投资", 1)

# 道五（a）第三层次变动节自己下估值判断：红线里的「估值偏高」。
BAD_LINE = _must_replace(
    DEMO,
    "- 期末余额 5.00 亿元「第三层次公允价值计量项目的期末余额",
    "- 期末余额 5.00 亿元 估值偏高「第三层次公允价值计量项目的期末余额", 1)

# 反证一：原句写了层次、登记值没写——漏登记不是自行归层，这道不判（规则 2）。
OK_LEVEL_QUOTE_ONLY = _must_replace(
    DEMO, "非上市股权 第三层次 5.00 亿元「", "非上市股权 5.00 亿元「", 1)
# 反证二：口径节里写「不轧净额」「不相抵」交代口径，整节豁免，不得反过来判本件在轧账。
OK_GAP_EXEMPT = _must_replace(
    DEMO,
    "不评价层次划分是否恰当。",
    "不评价层次划分是否恰当；利息与股息不轧净额、不相抵，各占各行。", 1)


def selftest():
    """逐档现报：好样须零发条，坏样须恰发该道码；反证档专验不该发的不发。

    档数＝逐档比对的那几档 + UNIMPLEMENTED 的码数（未落字各算一档「不可判」）。
    五道全落字后，好样单稿退 0，rc=0 才叫「五道全过」。
    """
    cases = (
        ("好样应零发条（五道全过）", DEMO, frozenset()),
        ("形制：头部删掉「不构成投资建议」", BAD_MARK, frozenset({"FV-STRUCT"})),
        ("形制：节标题写成认不出的样子（进 stray＋缺节）", BAD_HEADING,
         frozenset({"FV-STRUCT"})),
        ("形制：整节删掉「来源」", BAD_SOURCE, frozenset({"FV-STRUCT"})),
        ("原句与锚：摘掉整段「」+〔锚〕，只留 [S1]", NO_TRIPLE, frozenset({"FV-QUOTE"})),
        ("来源行：检索日写成 2026/03/20", BAD_SOURCE_FMT, frozenset({"FV-QUOTE"})),
        ("对应：正文引 [S9] 而来源节只有 S1", BAD_REF, frozenset({"FV-QUOTE"})),
        ("层次：登记值写第三层次、原句里没有层次词", BAD_LEVEL,
         frozenset({"FV-LEVEL"})),
        ("估值技术：登记值写收益法、原句写市场法", BAD_TECH, frozenset({"FV-TECH"})),
        ("输入值：原句「不可观察」、登记值写「可观察」（前缀整词）", BAD_TECH_INPUT,
         frozenset({"FV-TECH"})),
        ("红线：发现行自己下「估值偏高」的判断", BAD_LINE, frozenset({"FV-LINE"})),
        ("反证：原句写了层次、登记值没写（漏登记不该发）", OK_LEVEL_QUOTE_ONLY,
         frozenset()),
        ("反证：口径节写「不轧净额」「不相抵」（整节豁免）", OK_GAP_EXEMPT, frozenset()),
    )
    bad = 0
    last_unjudged = ()
    for label, text, want in cases:
        findings, unjudged = check_text(text)
        last_unjudged = unjudged
        got = frozenset(c for c, _l, _m in findings)
        if got == want:
            print("过   %s（发条 %d 条：%s）"
                  % (label, len(findings), "、".join(sorted(got)) or "无"))
        else:
            bad += 1
            detail = "；".join("%s L%s %s" % (c, l, m) for c, l, m in findings[:4])
            print("不合 %s：期望 %s 实得 %s ｜ %s"
                  % (label, sorted(want) or "无", sorted(got) or "无", detail))

    # 覆盖自证：每道已落字的码，在 cases 里至少有一档期望恰含它。
    # 这条防的是「实现了一道判据、同时少了一档不可判，净增反例 0 档」——
    # 判据接进 CHECKS 却没有反例钉住，它以后被改坏，自测照样报 不合=0。
    implemented = [c for c in CODES if c not in UNIMPLEMENTED]
    covered = set()
    for _label, _text, want in cases:
        covered |= set(want)
    uncovered = [c for c in implemented if c not in covered]
    print("%s 覆盖自证：已落字码 %d 道，有反例的 %d 道，缺反例：%s"
          % ("不合" if uncovered else "过  ",
             len(implemented), len(implemented) - len(uncovered),
             "／".join(uncovered) if uncovered else "无"))
    if uncovered:
        bad += 1

    # 空壳自证：清单里的码调用即抛且点名自身；不在清单里的码不许抛，只能返回列表
    shell_bad = []
    for code, fn in CHECKS:
        try:
            got = fn([], [], [])
        except NotImplementedError as exc:
            if code not in UNIMPLEMENTED:
                shell_bad.append("%s 已声明落字却抛未落字（%s）" % (code, exc))
            elif code not in str(exc):
                shell_bad.append("%s 抛出但未点名码（%s）" % (code, exc))
            continue
        if code in UNIMPLEMENTED:
            shell_bad.append("%s 返回了 %r，空壳必须抛未落字" % (code, got))
        elif not isinstance(got, list):
            shell_bad.append("%s 返回 %r，应返回列表" % (code, got))
    if shell_bad:
        bad += 1
        print("不合 空壳自证：%s" % "；".join(shell_bad))
    elif UNIMPLEMENTED:
        print("过   空壳自证（%s 调用即抛并点名；其余返回列表）"
              % "、".join(UNIMPLEMENTED))
    else:
        print("过   空壳自证（未落字清单为空，五道均返回列表）")

    # 不崩自证：空稿、乱头、只头无节都过一遍，必须返回二元组且未落字的码全计不可判
    crash = []
    for label, text in (("空稿", ""), ("乱头", "x\n"), ("只头无节", DEMO.split("## ")[0])):
        try:
            _f2, u2 = check_text(text)
        except Exception as exc:                       # noqa: BLE001 — 自证只问崩不崩
            crash.append("%s 抛出 %s: %s" % (label, type(exc).__name__, exc))
            continue
        got_codes = {c for c, _w in u2}
        if got_codes != set(UNIMPLEMENTED):
            crash.append("%s 不可判 %s，应为 %s"
                         % (label, sorted(got_codes) or "无", sorted(UNIMPLEMENTED) or "无"))
    if crash:
        bad += 1
        print("不合 不崩自证：%s" % "；".join(crash))
    elif UNIMPLEMENTED:
        print("过   不崩自证（空稿／乱头／只头无节均返回二元组，未落字 %d 道计不可判）"
              % len(UNIMPLEMENTED))
    else:
        print("过   不崩自证（空稿／乱头／只头无节均返回二元组，无未落字）")

    # 单稿退码自证：好样落盘单跑，退码与「是否还有未落字」绑定，不写死数：
    # 有未落字 → 3（且输出须含「不可判」与「这不等于合规」）；全落字 → 0（且不得再出现该句）。
    rc, out, tmp = None, "", None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8",
                                         delete=False) as fh:
            fh.write(DEMO)
            tmp = fh.name
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main([tmp])
        out = buf.getvalue()
    finally:
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass
    want_rc = 3 if UNIMPLEMENTED else 0
    if rc != want_rc:
        bad += 1
        print("不合 单稿退码自证：好样单稿 rc=%r，应为 %d（未落字 %d 道）"
              % (rc, want_rc, len(UNIMPLEMENTED)))
    elif want_rc == 3 and ("不可判" not in out or "这不等于合规" not in out):
        bad += 1
        print("不合 单稿退码自证：rc=3 但输出缺口径字样")
    elif want_rc == 0 and "这不等于合规" in out:
        bad += 1
        print("不合 单稿退码自证：已无未落字，输出却仍写「这不等于合规」")
    else:
        print("过   单稿退码自证（好样单稿 rc=%d，未落字 %d 道%s）"
              % (want_rc, len(UNIMPLEMENTED),
                 "，输出含「不可判」与「这不等于合规」" if want_rc == 3 else "，输出无「这不等于合规」"))

    unk = len({c for c, _w in last_unjudged})
    print("——")
    print("自测档数=%d｜不合=%d｜不可判=%d" % (len(cases) + len(UNIMPLEMENTED), bad, unk))
    if bad:
        return 1
    return 3 if unk else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="公允价值层次登记稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="公允价值层次登记稿 .md 路径")
    ap.add_argument("--selftest", action="store_true", help="跑包内夹具自检")
    ap.add_argument("--demo", action="store_true", help="打印一份合规样例（零输入可跑）")
    try:
        args = ap.parse_args(argv)
    except SystemExit:                                 # 用法错统一退 2，不沿用 argparse 的 2/0 混用
        return 2

    if args.selftest:
        return selftest()
    if args.demo:
        sys.stdout.write(DEMO)
        return 0
    if not args.path:
        ap.print_usage(sys.stderr)
        print("缺入参：给一份公允价值层次登记稿路径，或用 --demo / --selftest", file=sys.stderr)
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
