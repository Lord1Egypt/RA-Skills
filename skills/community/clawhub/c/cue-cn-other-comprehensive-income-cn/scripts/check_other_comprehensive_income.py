#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_other_comprehensive_income.py — 其他综合收益判断稿五道机检（零网络、零外发）

**五道已全部落字**：OCI-STRUCT（形制）、OCI-QUOTE（原句与锚）、OCI-TAX（税后净额逐数回原句）、
OCI-RECLASS（重分类金额／去向／范围回原句）、OCI-LINE（红线词）。
空壳机制保留但 `UNIMPLEMENTED` 已清空：若某道将来回退成空壳（重新登记进 `UNIMPLEMENTED`
并调 `_not_judged`），`check_text` 会把它计入 `unjudged`、报告里明写「这不等于合规」、单稿退 3——
空壳不许被读成「过」。

用法：
    python3 scripts/check_other_comprehensive_income.py <其他综合收益稿>.md
    python3 scripts/check_other_comprehensive_income.py --selftest
    python3 scripts/check_other_comprehensive_income.py --demo     打印一份完整合规样例（零输入可跑）

七节（按序，`## ` 起节）：
    其他综合收益概况／税后净额明细／重分类调整／归属于母公司与少数股东／现金流量套期与折算差额
    ／口径与未取到／来源

五道码（状态以 `UNIMPLEMENTED` 现值为准，下面写的是**这道判什么**）：

道一 OCI-STRUCT 形制【已落字】
  头部（第一个 `## ` 之前）四件自标逐字在位：AI 整理初稿／请回原文核对／不构成投资建议／判断位 [待人工]；
  `主体：` 行、`报告期：` 行在场且非空；七节齐且按序；前五节各至少一条 `- ` 发现行；
  「口径与未取到」与「来源」两节不得为空；认不出的节标题与多出的同名节逐条发。

道二 OCI-QUOTE 原句与锚【已落字】
  每条发现行以「」原句 + 〔锚：…〕 + [S#] 三元组收尾，可挂多组；
  例外只有三形：「未取到：」行、[待人工] 行与〔自算〕行；
  来源行 `- [S#] 标题 | URL | 检索日 YYYY-MM-DD`，URL 须为可点 http(s) 地址；
  发现行收尾的 [S#] 必须在来源节有对应登记行。

道三 OCI-TAX 税后净额与所得税影响只认原句【已落字】
  只判「税后净额明细」节：登记值形如「税前 X 万元／所得税影响 Y 万元／税后净额 Z 万元」，
  三个数逐个去掉千分位逗号后，须在该行「」原句里找到同一字面串，缺哪个数点名哪个；
  「无所得税影响」是合法登记值，此时只核税前与税后净额两个数，但**原句若给了具体所得税金额**
  即发（登记值把附注的一个数吃掉了）；「合计」行照同一条判，不特殊放行。
  **不做算术校验**（不验 税前−所得税影响＝税后净额）：附注里有些项目本就不满足该恒等式，验算会误伤。

道四 OCI-RECLASS 重分类调整只认原句【已落字】
  只判「重分类调整」节：登记值里的金额须在该行「」原句里找到同一字面串；
  登记值写了去向词（投资收益／营业成本／营业外收入／资产处置收益／其他业务成本）时，
  原句须出现同一个去向词；「不能重分类项目 … 无重分类」这类行属**范围判据**——
  原句须含「不能重分类」且含「无重分类」或「无…金额」，缺一则发。

道五 OCI-LINE 红线【已落字】
  扫全文，但「口径与未取到」「来源」两节整节豁免（前者按设计就要写「与净利润不轧账」，
  不豁免会自己咬自己）。命中即发：轧账类「与净利润合计／轧成／相抵／净影响／合计影响所有者权益」；
  已实现类「已实现收益／已实现利得」；评级类「目标价／买入／增持／减持／评级为」。
  **不拿单字「净额」当红线**（「税后净额」是本件核心合法词）；
  **不拿「投资建议」当红线**（头部自标「不构成投资建议」必须含它，一定误伤）。

退码：0 全过 / 1 有发条 / 2 用法错（缺参数或未知参数）
      / 3 读不到文件或空稿，或零发条但有未实装判据（`UNIMPLEMENTED` 非空时）。
      本拍仍有三个空壳，好样单稿必退 3，不得读成合规。
"""

import argparse
import io
import os
import re
import sys
import tempfile
import contextlib
from datetime import date
from pathlib import Path

SLUG = "cue-cn-other-comprehensive-income-cn"

CODES = ("OCI-STRUCT", "OCI-QUOTE", "OCI-TAX", "OCI-RECLASS", "OCI-LINE")

MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议", "判断位 [待人工]")

SECTIONS = ("其他综合收益概况", "税后净额明细", "重分类调整",
            "归属于母公司与少数股东", "现金流量套期与折算差额",
            "口径与未取到", "来源")
CONTENT_SECTIONS = SECTIONS[:5]
GAP_SECTION = "口径与未取到"
SOURCE_SECTION = "来源"
TAX_SECTION = "税后净额明细"
RECLASS_SECTION = "重分类调整"

# 未落字的码：抛未落字一律计「不可判」，不许并进「不合」，也不许算「过」；
# 不在清单里却抛未落字＝声明与实装不符，由 check_text 直接发条。
# 本拍五道全部落字，清单清空。清空不是因为「闸松一点好过」，而是因为空壳已经没了；
# 将来某道回退成空壳时，把它的码登记回这里，才不会让空壳被当成「过」。
UNIMPLEMENTED = ()

HEADING = re.compile(r"^##(?!#)\s*(.+?)\s*$")
NUMBERING = re.compile(r"^(?:[0-9]+[.、)]|[一二三四五六七八九十]+[、.])\s*")
SUBJECT = re.compile(r"^主体：\s*(\S.*)$")
PERIOD = re.compile(r"^报告期：\s*(\S.*)$")

TRIPLE = re.compile(r"「(?P<q>[^」]*)」\s*〔\s*锚\s*[:：]\s*(?P<a>[^〕]*)〕\s*\[(?P<s>S\d+)\]")
QUOTE = re.compile(r"「([^」]*)」")
ANCHOR_REF = re.compile(r"\[(S\d+)\]")
ANCHOR_BLOCK = re.compile(r"〔\s*锚\s*[:：][^〕]*〕")
REF_TAIL = re.compile(r"\[(S\d+)\]\s*$")

SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<rest>.+?)"
    r"\|\s*(?P<url>https?://\S+)\s*\|"
    r"\s*检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*(?:\|.*)?$"
)


# ---------------------------------------------------------------- 判据

def _not_judged(code, why):
    """空壳的唯一出口：抛未落字，由 check_text 捕获计入「不可判」，不返回空表。

    本拍五道全部落字，这里没有调用方；留着是因为 `UNIMPLEMENTED` 机制还在——
    将来某道回退成空壳时，重新登记 + 调这里即可，不必再造一套。
    """
    raise NotImplementedError("%s 未落字：%s" % (code, why))


def check_struct(head, sections, stray):
    """道一 OCI-STRUCT 形制：头部四件自标与两行、七节齐且按序、节内是否有发现行。

    只判「形」：节名在不在、顺序对不对、内容节里有没有发现行、两节尾部有没有内容。
    判断内容对不对是另四道的事——这里不越界，否则一支注入会同时红两道、分不清归属。
    """
    out = []
    htext = "\n".join(s for _i, s in head)
    for mark in MARK_TEXTS:
        if mark not in htext:
            out.append(("OCI-STRUCT", 1, "头部缺自标「%s」" % mark))
    if not any(SUBJECT.match(s.strip()) for _i, s in head):
        out.append(("OCI-STRUCT", 1, "头部缺 `主体：` 行"))
    if not any(PERIOD.match(s.strip()) for _i, s in head):
        out.append(("OCI-STRUCT", 1, "头部缺 `报告期：` 行"))

    # 丙：野节（认不出的节名／多出的同名节）逐条报，行号用 stray 给的
    for lineno, raw in stray:
        out.append(("OCI-STRUCT", lineno, "不认识的节标题或多出同名节：%s" % raw))

    # 丁：七节须齐且按序
    names = [n for n, _l, _b in sections]
    missing = [n for n in SECTIONS if n not in names]
    if missing:
        out.append(("OCI-STRUCT", 1, "缺节：%s" % "／".join(missing)))
    elif names != list(SECTIONS):
        out.append(("OCI-STRUCT", 1, "节序不对：现序 %s，应序 %s"
                    % ("／".join(names), "／".join(SECTIONS))))

    # 戊：五个内容节各至少一条发现行；己：两节尾部不得为空
    for name, hline, body in sections:
        if name in CONTENT_SECTIONS:
            if not any(_is_finding_line(s) for _i, s in body):
                out.append(("OCI-STRUCT", hline, "节「%s」没有一条发现行（空节）" % name))
        elif name in (GAP_SECTION, SOURCE_SECTION):
            if not any(s.strip() for _i, s in body):
                out.append(("OCI-STRUCT", hline, "节「%s」为空" % name))
    return out


def check_quote(head, sections, stray):
    """道二 OCI-QUOTE 原句与锚：来源行格式、发现行三元组、[S#] 两向对应。

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
                out.append(("OCI-QUOTE", lineno,
                            "来源节只许 `- [S#] 标题 | URL | 检索日` 行：%s" % s.strip()[:44]))
                continue
            m = SOURCE_LINE.match(s.strip())
            if not m:
                out.append(("OCI-QUOTE", lineno,
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
                continue                     # 缺口登记与人工位、自算行本来就不挂三元组
            if not TRIPLE.search(s):
                miss = []
                if not QUOTE.search(s):
                    miss.append("「」原句")
                if not ANCHOR_BLOCK.search(s):
                    miss.append("〔锚：…〕")
                if not ANCHOR_REF.search(s):
                    miss.append("[S#]")
                out.append(("OCI-QUOTE", lineno,
                            "发现行缺 %s（三元组须在行末）"
                            % "、".join(miss or ["「」原句 + 〔锚〕 + [S#] 的次序"])))
                continue
            m = REF_TAIL.search(s.strip())
            if not m:
                out.append(("OCI-QUOTE", lineno,
                            "发现行未以 [S#] 收尾（三元组须在行末）"))
                continue
            # 没有来源节、或来源节里一条合规行都没有时，同一个根因会在每一行重复铺开，
            # 把「哪一行真有问题」淹掉：根因由道一（缺节）或本道丙（零合规来源行）点一次，
            # 这里只在来源节确有登记行时，才逐行判「引用的是不是登记过的 S 号」。
            if not has_source or not registered:
                continue
            ref = m.group(1)
            if ref in registered or ref in reported_missing:
                continue                     # 同一个未登记 S 号只报一次，行号取首次引用处
            reported_missing.add(ref)
            out.append(("OCI-QUOTE", lineno,
                        "引用了未登记的 [%s]：来源节没有该 S 号的合规来源行" % ref))

    # 丙：来源节存在但一条合规来源行都没有——只在节在场时报，缺节归道一
    if has_source and not registered:
        out.append(("OCI-QUOTE", 1,
                    "来源节没有一条合规来源行：每个 [S#] 都要有可点 http(s) URL 与检索日"))
    return out


def _quotes_of(line):
    """该行全部「」原句拼成一串；没有原句返回空串。"""
    return "".join(m.group(1) for m in QUOTE.finditer(line))


def _own_value(line):
    """登记值＝行内第一个「」之前的文字；没有原句返回整行之外的空串（由调用方先判）。"""
    return line.split("「", 1)[0]


def _num_in_value(own, label):
    """从登记值里取 `label` 后面紧跟的那个数（如 `税前 1,200.00 万元` → `1,200.00`）。

    只认「标签＋空白＋数」紧邻的形态：`无所得税影响` 后面没有数，返回 None——
    这是合法登记值，不是缺数。
    """
    m = re.search(re.escape(label) + r"\s*(-?\d[\d,]*(?:\.\d+)?)", own)
    return m.group(1) if m else None


def _squash(num):
    """去掉千分位逗号：`1,200.00` → `1200.00`。比对两侧都这样归一。"""
    return num.replace(",", "")


# 原句里「所得税影响」后面跟了一个具体金额（允许「为」「人民币」「：」这些桥接词）。
# 要求数字**紧邻**标签，是为了不把「该项不产生所得税影响，税后净额为人民币 850.00 万元」
# 这种合法句子误判成「原句给了所得税金额」——那里的 850.00 属于税后净额，中间隔着逗号与文字。
_TAX_AMOUNT_IN_QUOTE = re.compile(
    r"所得税影响\s*(?:金额)?\s*(?:合计)?\s*(?:为|是|：|:)?\s*(?:人民币)?\s*(-?\d[\d,]*(?:\.\d+)?)")


def check_tax(head, sections, stray):
    """道三 OCI-TAX 税后净额与所得税影响只认原句。

    只判「税后净额明细」节：登记值里取「税前／所得税影响／税后净额」三个数，逐个去千分位逗号后，
    须在同一行「」原句里找到同一字面串。缺哪个点名哪个。
    `无所得税影响` 是合法登记值（外币折算那类），此时只核税前与税后净额；但原句若紧邻给了
    具体所得税金额，说明登记值把附注的一个数吃掉了，发。
    **不做算术校验**：不验 税前−所得税影响＝税后净额。附注里有些项目本就不满足该恒等式，验算会误伤。
    """
    out = []
    for name, _hline, body in sections:
        if name != TAX_SECTION:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue
            if _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s:
                continue                       # 缺口／人工位／自算行不是「照抄三个数」的登记行
            if "「" not in s:
                continue                       # 没有原句＝无可比对，缺原句由 OCI-QUOTE 点名
            own, q = _own_value(s), _quotes_of(s)
            nq = _squash(q)

            pre = _num_in_value(own, "税前")
            inc = _num_in_value(own, "所得税影响")
            net = _num_in_value(own, "税后净额")
            if pre is None and net is None:
                continue                       # 不是「税前…／税后净额…」形态的行，本道不管

            fields = [("税前", pre), ("税后净额", net)]
            if "无所得税影响" in own:
                # 合法登记值：不核所得税那个数，只判原句有没有「吃掉」附注给的金额
                if ("不产生所得税影响" not in q and "无所得税影响" not in q
                        and _TAX_AMOUNT_IN_QUOTE.search(q)):
                    out.append(("OCI-TAX", lineno,
                                "登记值写「无所得税影响」，原句却给了具体所得税金额"
                                "（登记值把附注的一个数吃掉了）"))
            else:
                fields.append(("所得税影响", inc))

            for label, num in fields:
                if num is None:
                    continue                   # 登记值没写这个数：没什么可比，不发
                if _squash(num) not in nq:
                    out.append(("OCI-TAX", lineno,
                                "登记值「%s %s」在同行原句里找不到该数字面串（缺：%s）"
                                % (label, num, label)))
    return out


# 重分类去向词。只判这几个，不扩表：扩表等于替附注认定「哪些科目算重分类去向」。
DEST_WORDS = ("投资收益", "营业成本", "营业外收入", "资产处置收益", "其他业务成本")
# 范围判据的第二半：「无…金额」这种把范围说清楚的形态（中间不许跨句号／逗号／分号）。
_NO_AMOUNT = re.compile(r"无[^。，；]{0,20}金额")


def check_reclass(head, sections, stray):
    """道四 OCI-RECLASS 重分类调整只认原句。

    只判「重分类调整」节：①登记值里的金额须在同句原句里找到同一字面串；
    ②登记值写了去向词，原句须出现同一个去向词；③`不能重分类` 这类范围行，
    原句须含「不能重分类」且含「无重分类」或「无…金额」——只写「本期无重分类金额」
    而丢掉范围表述的，发（那是范围判据，不是金额判据）。
    """
    out = []
    for name, _hline, body in sections:
        if name != RECLASS_SECTION:
            continue
        for lineno, s in body:
            if not s.strip() or s.lstrip().startswith("###"):
                continue
            if not _is_finding_line(s):
                continue
            if _is_gap_line(s) or "[待人工]" in s or "〔自算〕" in s:
                continue
            if "「" not in s:
                continue                       # 没有原句＝无可比对，缺原句由 OCI-QUOTE 点名
            own, q = _own_value(s), _quotes_of(s)
            nq = _squash(q)

            # ① 金额逐字回原句
            for m in re.finditer(r"-?\d[\d,]*(?:\.\d+)?", own):
                num = m.group(0)
                if _squash(num) not in nq:
                    out.append(("OCI-RECLASS", lineno,
                                "登记值里的金额 %s 在同行原句里找不到该数字面串" % num))

            # ② 去向词须原句也有同词
            for w in DEST_WORDS:
                if w in own and w not in q:
                    out.append(("OCI-RECLASS", lineno,
                                "登记值写「%s」，同行原句里没有该去向词" % w))

            # ③ 范围行：不能重分类 的范围表述不能只写「无重分类金额」
            if "不能重分类" in own:
                if "不能重分类" not in q:
                    out.append(("OCI-RECLASS", lineno,
                                "登记值写「不能重分类」，原句里没有该范围表述"))
                elif "无重分类" not in q and not _NO_AMOUNT.search(q):
                    out.append(("OCI-RECLASS", lineno,
                                "登记值写「无重分类」，原句既没有「无重分类」也没有「无…金额」"))
    return out


# 红线词分组。三处刻意的「不加」：
#   ① 不拿单字「净额」当红线——「税后净额」是本件核心合法词，收了会全篇发红；
#   ② 不拿「投资建议」当红线——头部四件自标必须含「不构成投资建议」，收了必然误伤；
#   ③ 不拿「合计」单字——「以上各项合计」是附注原话，轧账要看「与净利润合计」这个组合。
LINE_BANS = (
    ("轧账", ("与净利润合计", "轧成", "相抵", "净影响", "合计影响所有者权益")),
    ("已实现", ("已实现收益", "已实现利得")),
    ("评级", ("目标价", "买入", "增持", "减持", "评级为")),
)


def check_line(head, sections, stray):
    """道五 OCI-LINE 红线。

    扫全文，但「口径与未取到」「来源」两节整节豁免：前者按设计就要写
    「其他综合收益与净利润不轧账」这类口径说明，后者是来源行，不豁免会自己咬自己。
    命中即发，行号取命中行；同一行命中多个词只报一次（点第一个命中词）。
    """
    out = []
    lines = list(head)
    for name, _hline, body in sections:
        if name in (GAP_SECTION, SOURCE_SECTION):
            continue                           # 口径节与来源节整节豁免
        lines.extend(body)
    for lineno, s in lines:
        if not s.strip():
            continue
        for group, words in LINE_BANS:
            hit = next((w for w in words if w in s), None)
            if hit:
                out.append(("OCI-LINE", lineno,
                            "%s红线词「%s」：%s" % (group, hit, s.strip()[:44])))
                break
    return out


CHECKS = (
    ("OCI-STRUCT", check_struct),
    ("OCI-QUOTE", check_quote),
    ("OCI-TAX", check_tax),
    ("OCI-RECLASS", check_reclass),
    ("OCI-LINE", check_line),
)


# ---------------------------------------------------------------- 道具

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
    """把 `## 3. 税后净额明细` 归一成 `税后净额明细`；认不出返回 None（当作 stray）。"""
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


DEMO = r"""# 示例材料（600000.SH）其他综合收益登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议 ｜ 判断位 [待人工]
主体：示例材料（600000.SH）
报告期：2025 年年度报告·附注七·其他综合收益

## 其他综合收益概况

- 期初余额 3,050.00 万元「截至 2025 年 1 月 1 日，本集团其他综合收益余额为人民币 3,050.00 万元」〔锚：2025 年年报·第 188 页·合并所有者权益变动表〕[S1]
- 本期税后净额 1,397.50 万元「本期计入其他综合收益的税后净额（不含重分类转出）为人民币 1,397.50 万元」〔锚：2025 年年报·第 188 页·合并所有者权益变动表〕[S1]
- 本期重分类转出 380.00 万元「本期由其他综合收益重分类转入损益的税后金额为人民币 380.00 万元」〔锚：2025 年年报·第 191 页·附注七·其他综合收益〕[S2]
- 期末余额 4,067.50 万元「截至 2025 年 12 月 31 日，本集团其他综合收益余额为人民币 4,067.50 万元」〔锚：2025 年年报·第 188 页·合并所有者权益变动表〕[S1]

## 税后净额明细

- 其他债权投资公允价值变动 税前 1,200.00 万元／所得税影响 300.00 万元／税后净额 900.00 万元「本期其他债权投资公允价值变动形成的其他综合收益税前金额为人民币 1,200.00 万元，所得税影响为人民币 300.00 万元，税后净额为人民币 900.00 万元」〔锚：2025 年年报·第 189 页·附注七·其他综合收益〕[S2]
- 现金流量套期储备 税前 -640.00 万元／所得税影响 -160.00 万元／税后净额 -480.00 万元「本期现金流量套期储备税前发生额为人民币 -640.00 万元，所得税影响为人民币 -160.00 万元，税后净额为人民币 -480.00 万元」〔锚：2025 年年报·第 189 页·附注七·其他综合收益〕[S2]
- 外币财务报表折算差额 税前 850.00 万元／无所得税影响／税后净额 850.00 万元「本期外币财务报表折算差额为人民币 850.00 万元，该项不产生所得税影响」〔锚：2025 年年报·第 189 页·附注七·其他综合收益〕[S2]
- 其他权益工具投资公允价值变动 税前 320.00 万元／所得税影响 80.00 万元／税后净额 240.00 万元「本期其他权益工具投资公允价值变动税前金额为人民币 320.00 万元，所得税影响为人民币 80.00 万元，税后净额为人民币 240.00 万元」〔锚：2025 年年报·第 190 页·附注七·其他综合收益〕[S2]
- 重新计量设定受益计划变动额 税前 -150.00 万元／所得税影响 -37.50 万元／税后净额 -112.50 万元「本期重新计量设定受益计划变动额为人民币 -150.00 万元，所得税影响为人民币 -37.50 万元，税后净额为人民币 -112.50 万元」〔锚：2025 年年报·第 190 页·附注七·其他综合收益〕[S2]
- 合计 税前 1,580.00 万元／所得税影响 182.50 万元／税后净额 1,397.50 万元「以上各项合计税前金额为人民币 1,580.00 万元，所得税影响合计为人民币 182.50 万元，税后净额合计为人民币 1,397.50 万元」〔锚：2025 年年报·第 190 页·附注七·其他综合收益〕[S2]

## 重分类调整

- 其他债权投资 本期重分类进损益 260.00 万元「本期处置其他债权投资，原计入其他综合收益的公允价值变动人民币 260.00 万元（税后）转入投资收益」〔锚：2025 年年报·第 191 页·附注七·其他综合收益〕[S2]
- 现金流量套期储备 本期重分类进损益 120.00 万元「本期原计入现金流量套期储备的税后金额人民币 120.00 万元转入营业成本」〔锚：2025 年年报·第 191 页·附注七·其他综合收益〕[S2]
- 不能重分类项目 本期无重分类「重新计量设定受益计划变动额与其他权益工具投资公允价值变动属于不能重分类进损益的项目，本期无重分类金额」〔锚：2025 年年报·第 191 页·附注七·其他综合收益〕[S2]

## 归属于母公司与少数股东

- 归属于母公司 1,180.00 万元「本期其他综合收益税后净额中，归属于母公司股东的部分为人民币 1,180.00 万元」〔锚：2025 年年报·第 188 页·合并所有者权益变动表〕[S1]
- 归属于少数股东 217.50 万元「本期其他综合收益税后净额中，归属于少数股东的部分为人民币 217.50 万元」〔锚：2025 年年报·第 188 页·合并所有者权益变动表〕[S1]

## 现金流量套期与折算差额

- 现金流量套期储备 期末 -280.00 万元「本期现金流量套期储备期初余额为人民币 320.00 万元，本期计入其他综合收益的税后金额为人民币 -480.00 万元，本期重分类转入营业成本的税后金额为人民币 120.00 万元，期末余额为人民币 -280.00 万元」〔锚：2025 年年报·第 192 页·附注七·其他综合收益〕[S2]
- 外币报表折算差额 期末 1,900.00 万元「本期外币财务报表折算差额期初余额为人民币 1,050.00 万元，本期增加人民币 850.00 万元，期末余额为人民币 1,900.00 万元」〔锚：2025 年年报·第 192 页·附注七·其他综合收益〕[S2]
- 处置境外经营 本期无转出「本期无处置境外经营的情形，外币财务报表折算差额未转入当期损益」〔锚：2025 年年报·第 192 页·附注七·其他综合收益〕[S2]

## 口径与未取到

- 未取到：无
- 口径：税前金额、所得税影响、税后净额与重分类金额一律照抄附注原文，本件不按 25% 税率或上期比例反算；其他综合收益与净利润不轧账。

## 来源

- [S1] 示例材料 2025 年年度报告·合并所有者权益变动表 | https://example.invalid/600000_2025_annual.pdf | 检索日 2026-03-20
- [S2] 示例材料 2025 年年度报告·附注七·其他综合收益 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026-03-20
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
# 形制坏样 (a) 头部少一件自标。
BAD_MARK = _must_replace(DEMO, "不构成投资建议", "", 1)
# 形制坏样 (b) 一个节标题写成认不出的样子：该节既进不了 sections（算缺节），标题本身也进 stray。
# 注：不能用「## 税后净额明细（旧）」——全角括号前 `not isalnum()` 为真，_section_of 仍认得出；
# 要接一个字母数字才算认不出（「明细旧」落空 → None → stray）。这是实测出来的形，不是猜的。
BAD_HEADING = _must_replace(DEMO, "## 税后净额明细\n", "## 税后净额明细旧\n", 1)
# 形制坏样 (c) 整节删掉「来源」（连标题与两条来源行）：七节不齐、来源节为空。
_SOURCE_BLOCK = ("## 来源\n"
                 "\n"
                 "- [S1] 示例材料 2025 年年度报告·合并所有者权益变动表 | "
                 "https://example.invalid/600000_2025_annual.pdf | 检索日 2026-03-20\n"
                 "- [S2] 示例材料 2025 年年度报告·附注七·其他综合收益 | "
                 "https://example.invalid/600000_2025_notes.pdf | 检索日 2026-03-20\n")
BAD_SOURCE = _must_replace(DEMO, _SOURCE_BLOCK, "", 1)

# 原句与锚坏样 (a) 整段「」+〔锚〕摘掉、只留收尾 [S1]（原句与锚都没了，行形制仍合规）。
_QUOTE_SNIP = ("「本期计入其他综合收益的税后净额（不含重分类转出）为人民币 1,397.50 万元」"
               "〔锚：2025 年年报·第 188 页·合并所有者权益变动表〕")
NO_TRIPLE = _must_replace(DEMO, _QUOTE_SNIP, "", 1)
# 原句与锚坏样 (b) S2 的检索日写成斜杠式：该行不合格式、S2 不再算登记（只坏 S2，S1 仍登记）。
# 写成斜杠后，正文里引用 [S2] 的那几行会各发一条「引用了未登记的 S2」——同一 S 号只报一处，
# 所以整张稿的码集仍是 {OCI-QUOTE}，不会连带别的码。
BAD_SOURCE_FMT = _must_replace(
    DEMO,
    "https://example.invalid/600000_2025_notes.pdf | 检索日 2026-03-20",
    "https://example.invalid/600000_2025_notes.pdf | 检索日 2026/03/20", 1)
# 原句与锚坏样 (c) 正文引 [S9]，来源节只有 S1／S2。
BAD_REF = _must_replace(
    DEMO,
    "本集团其他综合收益余额为人民币 4,067.50 万元」〔锚：2025 年年报·第 188 页·合并所有者权益变动表〕[S1]",
    "本集团其他综合收益余额为人民币 4,067.50 万元」〔锚：2025 年年报·第 188 页·合并所有者权益变动表〕[S9]",
    1)

# 税后净额坏样：登记值把税后净额 900.00 改成 975.00，同行原句一字不动（原句仍是 900.00）。
# 只该红 OCI-TAX：三个数里前两个（1,200.00／300.00）仍能在原句里找到，缺的只有税后净额。
# 三元组完整，OCI-QUOTE 不红；该行在「税后净额明细」节，OCI-RECLASS 只判重分类节、OCI-LINE 无红线词。
# `税后净额 900.00 万元「` 只在那一行的登记值里出现（合计行是 1,397.50），替换唯一。
BAD_TAX = _must_replace(DEMO, "税后净额 900.00 万元「", "税后净额 975.00 万元「", 1)

# 重分类坏样（a）去向不符：登记值里写「转入营业成本」，同行原句写的是「转入投资收益」。
# 只该红 OCI-RECLASS：金额 260.00 原句仍有，登记值也没多出别的数；缺的是去向词对得上。
# 三元组完整，OCI-QUOTE 不红；该行在「重分类调整」节，另两道不认这一行。
BAD_RECLASS = _must_replace(
    DEMO,
    "本期重分类进损益 260.00 万元「",
    "本期重分类进损益 260.00 万元 转入营业成本「", 1)

# 重分类坏样（b）范围判据：把「不能重分类项目」那行的原句换成只剩「本期无重分类金额」，
# 丢掉了「不能重分类」这个范围表述。只该红 OCI-RECLASS（范围语句另一赋缺）。
BAD_RECLASS_SCOPE = _must_replace(
    DEMO,
    "「重新计量设定受益计划变动额与其他权益工具投资公允价值变动属于不能重分类进损益的项目，本期无重分类金额」",
    "「本期无重分类金额」", 1)

# 红线坏样（a）轧账：在第二个内容节插一条带完整三元组的行，登记值写「与净利润合计影响所有者权益」。
# 必须挂完整三元组——否则 OCI-QUOTE 会一起红，那一档就钉不住「只红 OCI-LINE」。
# 引用的 4,067.50 与同行原句一致，本道不判「归属」节的金额，只有红线词命中。
_SUB_LINE = ("- 归属于少数股东 217.50 万元「本期其他综合收益税后净额中，归属于少数股东的部分为人民币 217.50 万元」"
             "〔锚：2025 年年报·第 188 页·合并所有者权益变动表〕[S1]\n")
BAD_LINE = _must_replace(
    DEMO, _SUB_LINE,
    _SUB_LINE +
    "- 合计影响 其他综合收益与净利润合计影响所有者权益 4,067.50 万元"
    "「截至 2025 年 12 月 31 日，本集团其他综合收益余额为人民币 4,067.50 万元」"
    "〔锚：2025 年年报·第 188 页·合并所有者权益变动表〕[S1]\n", 1)

# 红线坏样（b）已实现：插一条把未实现变动写成「已实现收益」的行，三元组同样完整。
_OPEN_LINE = ("- 期末余额 4,067.50 万元「截至 2025 年 12 月 31 日，本集团其他综合收益余额为人民币 4,067.50 万元」"
              "〔锚：2025 年年报·第 188 页·合并所有者权益变动表〕[S1]\n")
BAD_LINE_REALIZED = _must_replace(
    DEMO, _OPEN_LINE,
    _OPEN_LINE +
    "- 已实现 本期其他综合收益变动确认为已实现收益 1,397.50 万元"
    "「本期计入其他综合收益的税后净额（不含重分类转出）为人民币 1,397.50 万元」"
    "〔锚：2025 年年报·第 188 页·合并所有者权益变动表〕[S1]\n", 1)

# 口径节豁免的反例：把口径行写成带两个红线词（「与净利润合计」「合计影响所有者权益」）的形态。
# 期望零发条——这一档防的是「红线词把口径说明也判了」。口径节按设计就要讲轧账口径，
# 不整节豁免就会自己咬自己；这一档是把那条豁免钉住，而不是放宽判据。
GAP_BAN_OK = _must_replace(
    DEMO,
    "- 口径：税前金额、所得税影响、税后净额与重分类金额一律照抄附注原文，"
    "本件不按 25% 税率或上期比例反算；其他综合收益与净利润不轧账。",
    "- 口径：税前金额、所得税影响、税后净额与重分类金额一律照抄附注原文，"
    "本件不按 25% 税率或上期比例反算；附注亦未列示「与净利润合计」或「合计影响所有者权益」的口径，"
    "本件同样不轧账。", 1)


def selftest():
    """逐档现报：好样须零发条，坏样须恰发该道码；未落字一道计「不可判」，不并进「不合」。

    档数＝逐档比对的那几档 + UNIMPLEMENTED 的码数（未落字各算一档「不可判」）。
    本拍只落形制与原句与锚两道：好样单稿仍退 3（还有三道未落字），不得读成合规。
    """
    cases = (
        ("好样应零发条", DEMO, frozenset()),
        ("形制：头部删掉「不构成投资建议」", BAD_MARK, frozenset({"OCI-STRUCT"})),
        ("形制：节标题写成认不出的样子（进 stray＋缺节）", BAD_HEADING,
         frozenset({"OCI-STRUCT"})),
        ("形制：整节删掉「来源」", BAD_SOURCE, frozenset({"OCI-STRUCT"})),
        ("原句与锚：摘掉整段「」+〔锚〕，只留 [S1]", NO_TRIPLE,
         frozenset({"OCI-QUOTE"})),
        ("来源行：S2 检索日写成 2026/03/20", BAD_SOURCE_FMT, frozenset({"OCI-QUOTE"})),
        ("对应：正文引 [S9] 而来源节只有 S1／S2", BAD_REF, frozenset({"OCI-QUOTE"})),
        ("税后净额：登记值一个数在原句里找不到", BAD_TAX, frozenset({"OCI-TAX"})),
        ("重分类：登记值写了原句没有的去向", BAD_RECLASS, frozenset({"OCI-RECLASS"})),
        ("重分类：范围行原句丢掉「不能重分类」", BAD_RECLASS_SCOPE,
         frozenset({"OCI-RECLASS"})),
        ("红线：发现行把自己写进「与净利润合计」", BAD_LINE, frozenset({"OCI-LINE"})),
        ("红线：把未实现变动写成「已实现收益」", BAD_LINE_REALIZED, frozenset({"OCI-LINE"})),
        ("反证：口径节写轧账口径不该发（整节豁免）", GAP_BAN_OK, frozenset()),
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
    # 反面也报：cases 里出现未落字的码＝钉了一个还没接线的靶，那份期望本身是假的。
    implemented = [c for c in CODES if c not in UNIMPLEMENTED]
    covered = set()
    for _label, _text, want in cases:
        covered |= set(want)
    uncovered = [c for c in implemented if c not in covered]
    ghosts = sorted(covered - set(implemented))
    if uncovered or ghosts:
        bad += 1
        print("不合 覆盖自证：已落字码 %d 道，有反例的 %d 道，缺反例：%s%s"
              % (len(implemented), len(implemented) - len(uncovered),
                 "／".join(uncovered) or "无",
                 ("；反例里出现未落字的码：%s" % "／".join(ghosts)) if ghosts else ""))
    else:
        print("过   覆盖自证（已落字码 %d 道，有反例的 %d 道，缺反例：无；"
              "未落字 %d 道以「不可判」计：%s）"
              % (len(implemented), len(implemented), len(UNIMPLEMENTED),
                 "／".join(UNIMPLEMENTED) or "无"))

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
        print("过   空壳自证（%s 调用即抛并点名；其余已落字段返回列表）"
              % "、".join(UNIMPLEMENTED))
    else:
        print("过   空壳自证（无空壳；五道调用均返回列表）")

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
                         % (label, sorted(got_codes) or "无", sorted(UNIMPLEMENTED)))
    if crash:
        bad += 1
        print("不合 不崩自证：%s" % "；".join(crash))
    else:
        print("过   不崩自证（空稿／乱头／只头无节均返回二元组，未落字 %d 道计不可判）"
              % len(UNIMPLEMENTED))

    # 单稿退码自证：好样落盘单跑，退码与「是否还有未落字」绑定，不写死数：
    # 有未落字 → 3（且输出须含「不可判」与「这不等于合规」）；五道全落字 → 0（且不得再出现该句）。
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
    ap = argparse.ArgumentParser(description="其他综合收益判断稿五道机检（零网络）")
    ap.add_argument("path", nargs="?", help="其他综合收益稿 .md 路径")
    ap.add_argument("--selftest", action="store_true", help="跑包内自检")
    ap.add_argument("--demo", action="store_true", help="打印一份完整合规样例（零输入可跑）")
    try:
        args = ap.parse_args(argv)
    except SystemExit:                                 # 用法错统一退 2，不沿用 argparse 的 0/2 混用
        return 2

    mark_first_run()                                   # ← 解析成功之后、干正事之前

    if args.selftest:
        return selftest()
    if args.demo:
        sys.stdout.write(DEMO)
        return 0
    if not args.path:
        ap.print_usage(sys.stderr)
        print("缺入参：给一份其他综合收益稿路径，或用 --demo / --selftest", file=sys.stderr)
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
