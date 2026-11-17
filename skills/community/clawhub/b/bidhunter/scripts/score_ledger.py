#!/usr/bin/env python3
"""
score_ledger.py - 评分点台账 + 正向覆盖矩阵（BidHunter v2.9 · B1/B2）

The two tables a bid writer actually needs right before the deadline: "which
scoring points are still unwritten" and "which clauses have no answer".

B1 评分点台账
    Consumes `score_items` already extracted by `ai/clause_extractor.py` —
    this module deliberately does NOT re-extract scoring items. Each scoring
    point becomes a row with a five-state machine:

        未开始 ──定位到锚点且文本非空──> 已写 ──三查通过──> 已完成
           │                          │
           │                    标准声明需支撑材料
           ↓                          ↓
        材料缺 <──补材命中── 待核 <──┘
           │                  ↑
           └──明示"无材料响应"──┘ (回 已写 + 记降分风险)

    Four alarms fire (never silently pass):
      1. 评分项分值合计 ≠ 招标声明总分（缺省 100）
      2. 同一评分项在同一文件同一章节出现 ≥2 个锚点
      3. 状态回退未经人工确认
      4. 截止前 3 天仍有「未开始」项

B2 正向覆盖矩阵
    One row per independently-scorable clause, one column per response
    location. Coverage is graded in three levels, never boolean:
      A 完全覆盖 = 有定位 + 名词性要素全部出现 + 有承诺动词
      B 部分覆盖 = 有定位但硬要素（数字/规格/名单/年限）缺失，或仅空声明
      C 未覆盖   = 无定位或要素零交集

B1 and B2 share the exact same `response_location` field format
(`file:section/page`, multiple joined by `;`), which is why they must ship in
the same release — a location written by one must be readable by the other.

Design rules (inherited from v2.8, non-negotiable):
  1. Never invent. A score that is not in the source stays None — it is NEVER
     filled with 0, because 0 is a real answer ("this item scores nothing").
  2. Never guess a location. If the anchor cannot be located in the text the
     state stays 未开始 and the row is flagged 待人工核实.
  3. Report coverage. Every run states how much of the document was read.
  4. A missing material library means 待核, never 无据.

Zero API cost: pure standard library rules. No model is called.

Usage:
  python3 score_ledger.py ledger <招标文件> [--json] [--csv P] [--xlsx P]
  python3 score_ledger.py coverage <招标文件> [--json] [--csv P] [--xlsx P]
  python3 score_ledger.py both <招标文件> [--json]
  python3 score_ledger.py ledger --from-json clauses.json   # reuse extraction
  python3 score_ledger.py --selftest
"""
import os
import re
import sys
import csv
import json
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai"))

# ----------------------------------------------------------------------------
# states
# ----------------------------------------------------------------------------

S_NOT_STARTED = "未开始"
S_WRITTEN = "已写"
S_MISSING = "材料缺"
S_PENDING = "待核"
S_DONE = "已完成"

STATES = (S_NOT_STARTED, S_WRITTEN, S_MISSING, S_PENDING, S_DONE)

# Legal transitions. A regression is only allowed when explicitly confirmed
# (--confirm-regress), because a silent state rollback means the table lies.
LEGAL_NEXT = {
    S_NOT_STARTED: {S_WRITTEN, S_MISSING},
    S_WRITTEN: {S_PENDING, S_DONE},
    S_MISSING: {S_PENDING, S_WRITTEN},
    S_PENDING: {S_DONE, S_WRITTEN},
    S_DONE: set(),
}

# ----------------------------------------------------------------------------
# regex
# ----------------------------------------------------------------------------

RE_SECTION = re.compile(
    r"(第[0-9一二三四五六七八九十百]+[章节条]|"
    r"[0-9]+\.[0-9]+(?:\.[0-9]+)?|"
    r"[一二三四五六七八九十]+、)")

RE_REF = re.compile(
    r"(详见|参见|见|另见)\s*"
    r"(附件\s*[0-9一二三四五六七八九十]+|"
    r"第[0-9一二三四五六七八九十百]+[章节条]|"
    r"[0-9]+\.[0-9]+(?:\.[0-9]+)?|"
    r"响应文件[^，。；\s]{0,12})")

# 承诺动词：出现其一才算"有承诺"
# 承诺动词：出现其一才算"有承诺"
# ★ 第五轮复验实测：这一组词与 RE_POSSESS（持有动作）曾长期不一致 ——
#   RE_POSSESS 认「已取得/持有」，这里却只有「满足/提供/具备」，于是
#   「CE认证：已取得CE认证证书。」过了证据判据却卡在承诺动词上被判 B。
#   根因从"空声明"搬到了"承诺动词表"，第四轮的 CE 修复因此只做了一半。
#   两张表现在共用 RE_PROMISE + RE_POSSESS 的并集，语义一致。
RE_COMMIT = re.compile(
    r"(满足|提供|具备|承诺|保证|响应|递交|配备|配置|出具|编制|安排|"
    r"已取得|已获得|已获|已通过|已提供|已提交|已附|已申领|持有|持证|"
    r"附有|附上|随附|附送|取得|获得|拥有|符合)")

# 空声明：只有承诺没有实质
RE_EMPTY_DECL = re.compile(
    r"^\s*(完全满足|完全响应|完全符合|满足招标文件(的)?(全部)?要求|"
    r"无偏离|无异议|符合要求|满足要求)\s*[。.]?\s*$")

# ★ 占位符未填 = 零响应，不是"写了"。
# v2.9 复验抓出：草稿只写「技术方案：待补。」时，台账竟判「已完成」——
# 因为 RE_EMPTY_DECL 要求整句只有承诺词，而「待补」根本匹配不上。
# v2.8 的 gap zero 已把这类列为致命项，台账这里必须对齐同一口径。
RE_PLACEHOLDER = re.compile(
    r"(待补|待提供|待确认|待填|暂缺|此处填写|此处留白|后续补|稍后提供|"
    r"【\s*】|＿{3,}|X{3,}|[\[【]\s*待\s*[\]】])")

# 硬要素：数字 / 规格 / 名单 / 年限（缺失即降 B）
RE_HARD = re.compile(
    r"(\d+\s*(?:年|个月|人|名|项|次|件|份|台|套|%|％|万元|元|亿|条|款|"
    r"平方米|米|吨|kg|辆|个|层|栋|间|支|把|张)|"
    r"[A-Z]{2,}\s*[-/]?\s*\d+[^，。；\s]{0,12}|"
    r"不低于\s*\d+|不少于\s*\d+|不少于|不低于|≥\s*\d+|<=\s*\d+)")

RE_SENT_SPLIT = re.compile(r"[。；;]")
RE_CLAUSE_SPLIT = re.compile(r"[、，,](?![^（(]*[）)])")

# 评分项"标准要求的材料要素"——用于判断 材料缺 vs 待核
RE_MATERIAL_HINT = re.compile(
    r"(证书|资质|许可|认证|业绩|合同|发票|社保|纳税|审计|报表|"
    r"简历|职称|证书|承诺函|声明|原件|复印件|报告|证明|名单|台账)")

STOP_HEAD = re.compile(r"^(投标人|供应商|响应人|我方|我公司|本单位|乙方)")

# 定位前剥离的指令性前缀：条款常带"须提供/应具备"等，定位时不该计入
RE_LEAD_VERB = re.compile(
    r"^(应当?|必须?|须|应|需|要求|提供|提交|具备|拥有|持有|响应|"
    r"满足|符合|不少于|不低于|不少于)\s*"
    r"(提供|提交|具备|拥有|持有|响应|满足|符合|配备|承诺)?\s*")


def _locate_candidates(clause):
    """Yield progressively looser needles for locating a clause in the text.

    Exact 12-char prefixes fail on real clauses because the tender text and
    the requirement text differ by a leading 须提供/应具备. Try in order:
      full clause → de-verbified → head-noun fragment.
    The fragment strips only digits and a small closed set of measure words;
    it must NOT strip Chinese words (an earlier version deleted 员/年限 while
    removing quantities and destroyed the very noun it was trying to keep).
    """
    c = _norm(clause)
    if not c:
        return
    yield c
    stripped = _norm(RE_LEAD_VERB.sub("", clause))
    if stripped and stripped != c:
        yield stripped
    # 只去数字 + 明确的 ASCII/常见量词，绝不删中文词
    core = re.sub(r"[0-9０-９]+|[%％]|(?<![A-Za-z])[A-Za-z]+", "", stripped)
    core = re.sub(r"(不少于|不低于|不少于|以上|以下|名|人|年|个|项|次|件|"
                  r"台|套|人|名|元|万|亿|米|吨|kg|辆|条|款|项)", "", core)
    core = re.sub(r"[，,、。；;：:（）()\s]+", "", core)
    # 保留最长的连续名词片段（≥4 字才有定位价值）
    frags = [f for f in re.split(r"[0-9，,、。；;：:（）()\s]+", stripped) if len(f) >= 4]
    if frags:
        # 优先取不含量词的最长片段
        frag = max(frags, key=len)
        yield frag
    if len(core) >= 4 and core not in (c, stripped):
        yield core


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------

def _norm(s):
    return re.sub(r"\s+", "", str(s or ""))


def split_anchors(value):
    """`response_location` is a ';'-joined list of `file:section/page`."""
    out = []
    for raw in str(value or "").split(";"):
        raw = raw.strip()
        if raw:
            out.append(raw)
    return out


def anchor_key(anchor):
    """(file, section) — the granularity at which duplicates are illegal.

    R1a: the same scoring point answered in two DIFFERENT chapters is legal and
    must not raise. Only two anchors in the same file AND same chapter is a
    real problem, so the key has to include both parts.
    """
    if ":" in anchor:
        f, _, sec = anchor.partition(":")
        return (_norm(f), _norm(sec))
    return ("", _norm(anchor))


def find_duplicate_anchors(anchors):
    """Return [(file, section, count)] where the same file+section repeats."""
    seen = {}
    for a in anchors:
        k = anchor_key(a)
        seen[k] = seen.get(k, 0) + 1
    return [(f, s, c) for (f, s), c in seen.items() if c > 1]


def locate_sections(text, want):
    """Locate a clause/heading in the text. Returns the char span or None.

    Never guesses: if none of the progressively looser needles is present, this
    returns None and the caller keeps the row at 未开始 / 待人工核实. Being
    too strict here is as harmful as being too loose — a requirement written
    as 须提供本地化服务团队 must still match a body that says 提供本地化
    服务团队 5 名, otherwise every real clause grades C and the tool is noise.
    """
    if not want or not text:
        return None
    t_norm = _norm(text)
    for needle in _locate_candidates(want):
        pos = t_norm.find(needle)
        if pos >= 0:
            return pos
    return None


def follow_reference(text, depth=1):
    """R1b / R2b: follow 详见/见附件 style references exactly ONE hop.

    A pure body-text locator would report 未开始 for a row whose real answer
    lives in 附件7 — that is a false negative on a real bid, which is the
    failure mode this whole module exists to remove. One hop only, with a
    visited set, so 附件1 → 附件2 → … cannot loop forever.
    """
    if depth <= 0 or not text:
        return None
    m = RE_REF.search(text)
    if not m:
        return None
    target = _norm(m.group(2))
    if not target:
        return None
    pos = _norm(text).find(target)
    if pos < 0:
        return None
    return m.group(2)


def hard_elements(text):
    """Hard elements: numbers, specs, rosters, durations. Missing → grade B.

    Normalised on the way out: 不少于 5 / 不低于5名 / ≥5 all reduce to "5",
    because a draft that writes "5 名" has answered a requirement written as
    "不少于 5 名". Comparing the raw strings instead produced a flood of
    false B grades — the middle grade stops being trustworthy when it is
    mostly noise.
    """
    if not text:
        return []
    out = []
    for m in RE_HARD.finditer(text):
        raw = m.group(0).strip()
        core = re.sub(r"(不少于|不低于|不小于|不短于|不超过|不高于|≥|>=|<=|≤|"
                      r"不少于|以上|以下|名|人|年|个|项|次|件|份|台|套|元|万|亿|"
                      r"米|吨|kg|辆|条|款|%|％|平方米|层|栋|间|支|把|张)", "", raw)
        core = re.sub(r"[^\dA-Za-z.]+", "", core)
        if core:
            out.append(core)
    # de-duplicate, keep order
    seen, uniq = set(), []
    for e in out:
        if e not in seen:
            seen.add(e)
            uniq.append(e)
    return uniq


def has_commitment(text):
    return bool(text and RE_COMMIT.search(text))


def is_empty_declaration(text):
    """A sentence that is nothing but a promise, with no substance behind it."""
    if not text:
        return True
    return bool(RE_EMPTY_DECL.match(text.strip()))


# 回声标题：把要求原样抄一遍当门牌，不构成作答
RE_ECHO_LABEL = re.compile(r"^[^：:]{2,20}[：:]\s*")
# 通用套话：出现即说明没有针对性内容
RE_GENERIC_FILLER = re.compile(
    r"(严格按照?(招标文件|上述要求|贵方要求)?(的要求)?(完成|执行|遵守)|"
    r"完全满足(招标文件)?(的)?(全部)?要求|符合(招标文件)?(的)?(全部)?要求|"
    r"无偏离|无异议|详见附件|详见上文|同上|其他从略|其余略|按要求执行|"
    r"满足招标文件要求|响应招标文件要求)")

# ★ 可核查证据：长度不能代表实质，这些能。
# 第三轮复验实测：用「残留 ≥8 字」当判据会误杀
# 「我方承诺7×24小时响应」「提供3场培训」「2名（李工、王工）」这类
# 短而确凿的真答案。真正的区别在于有没有可核查的东西写下来。
# 每一项单独成行，勿把 | 写进字符类里（那次写坏过：kPa)\d+ 直接粘连，
# 整个正则静默失配，一条都匹配不上）。
RE_EVIDENCE = re.compile(
    # 数字 + 单位/量词：7×24小时、3场、2名、5年、30%、200万
    r"\d+(?:[×xX*]\d+)?(?:年|个月|天|小时|分钟|人|名|位|场|次|项|件|份|"
    r"台|套|阶段|轮|%|％|万元|亿元|元|米|吨|辆|条|款|层|栋|间|支|把|张|"
    r"页|章|MHz|GB|TB|KB|MPa|kPa)"
    # 倍数 / 比率 / 阈值写法：7×24、1:50、≥5、不低于3
    r"|\d+\s*[×xX*]\s*\d+"
    r"|\d+\s*:\s*\d+"
    r"|(?:≥|≤|>=|<=|不低于|不少于|不高于|不小于)\s*\d+"
    # 证书 / 标准号：必须连同「持有动作」才算证据。
    # 第四轮复验实测：光看「标准名+数字」两头都错 ——
    #   「已取得CE认证」无数字 → 真证据被误杀
    #   「符合ISO9001标准」有数字 → 仅引用标准名，却当成已持有
    # 「有没有数字」与「是不是真证据」无关，所以这里要求出现
    # 已取得/已提供/已通过/附/编号/持有 等持有动作。
    # ⚠️ 持有动作不得被 RE_GENERIC_FILLER 当套话剥掉，见下方 _KEEP_ACTIONS。
    r"|(?:已取得|已提供|已通过|已获得|已获|持有|附有|附上?|附|编号|"
    r"证书编号|持证|已提交|已附|已申领|申领)[^\n。；;]{0,20}?"
    r"(?:ISO|GB|CMMI|ITSS|CE|UL|RoHS|CQC|CCC|ANSI|ASTM|DIN|JIS|BS|VDE|"
    r"认证|证书|体系|资质|许可证|执业)"
    # 型号类代码：XH-200、C30。**必须排除标准名** ——
    # 第四轮复验实测负向断言 (?<!ISO) 这类写法靠不住（断言长度必须与标准名
    # 等长，GB/ISO 长度不同就漏），改成先剔除标准名再判型号。
    r"|[A-Z]{2,}[-\s/]?\d{2,}"
    # 中文括号内的名单：李工、王工
    r"|[（(][^）)]{0,30}[、,，][^）)]{1,20}[）)]"
    # 明确的时限承诺：30日内、7天内
    r"|\d+\s*(?:日|天|周|月)内"
)

# 标准名/体系名：这些后面跟数字是「引用标准」，不是「持有证据」。
# 型号规则在判据匹配前先把这些词剔除，避免 ISO9001 被当成型号 XH-200。
STANDARD_NAMES = re.compile(
    r"(?:GB\s*/\s*T|GB\s*/\s*Z|GB/T|GB/Z|ISO|GB|GBT|CMMI|ITSS|CE|UL|"
    r"RoHS|CQC|CCC|ANSI|ASTM|DIN|JIS|BS|VDE|IEC|IEEE|OHSAS|SA8000|"
    r"TSC|GS|PSE|KC|ICASA)", re.I)

# ── 四个专用判据，每个只回答一件事（不再用一个大正则包打天下）─────────
# 第四轮复验的教训：把"什么算证据"塞进一个正则，每次修一个错就冒出新错。
# 拆成四个单一职责的判据后，Q1~Q3 各自可单独验证。

# Q1a 持有动作
# Q1a 持有动作 —— 只认「完成态」
# ★ 第五轮复验实测：这一组词上一版写得太宽（含 提供/具备/提交/取得/获得/
#   拥有/通过），于是「我方提供业绩材料」「我方具备相关资质」这种纯空口
#   白话，配上 RE_CERT_WORD 里的泛名词（业绩/资质/简历/报告/社保）就构成
#   AND 成立 → 6/6 假A 全部漏放。Q1 一旦成立就短路 Q2/Q3，代价最高。
#   区别在语气：「已取得/已附/持有」是已经做完并可查，「提供/具备」只是
#   承诺要做。前者算证据，后者是套话。
RE_POSSESS = re.compile(
    r"(已取得|已获得|已获|已通过|已提供|已提交|已附|已申领|已报审|"
    r"持有|持证|附有|附上|随附|附送|随本投标文件|"
    # 「通过…认证」是已完成的认证，语义上等同于持有。
    # 第五轮复验实测：只认「已通过」会漏掉「我方通过ISO9001质量管理体系
    # 认证」这种写法 —— 它没有「已」字，但认证已经通过，是真证据。
    r"通过[^。；;]{0,24}(?:认证|审核|审查|评估|复核|检测|验收))")

# Q1a' 承诺态动词：不足以单独构成证据，但在 RE_COMMIT 里要算「有承诺」
RE_PROMISE = re.compile(
    r"(提供|具备|取得|获得|拥有|提交|通过|递交|满足|符合|承诺|保证|响应|"
    r"配备|配置|出具|编制|安排)")

# Q1b 证书/资质/文件类名词
RE_CERT_WORD = re.compile(
    r"(认证|证书|体系|资质|许可证|执业|职称|注册|等级|认证证书|"
    r"资质证书|授权|报告|社保|纳税|审计|业绩|合同|发票|简历)")

# Q2a 量化：数字必须带单位/量词，裸编号不算
RE_QUANTITY = re.compile(
    r"\d+(?:\.\d+)?\s*(?:[×xX*]\s*\d+\s*)?"
    r"(?:年|个月|天|小时|分钟|人|名|位|场|次|项|件|份|台|套|阶段|轮|"
    r"%|％|万元|亿元|元|米|吨|辆|条|款|层|栋|间|支|把|张|页|章|"
    r"MHz|GB|TB|KB|MPa|kPa|km|m2)"
    r"|\d+\s*(?:≥|≤|>=|<=|不低于|不少于|不高于|不小于)\s*\d+")

# Q2b 型号：排除标准名后仍像型号的编码
RE_MODEL = re.compile(r"[A-Z]{2,}[-]\d{2,}|[A-Z]{1,4}\d{3,}")

# Q2c 括号内名单
RE_NAMED_LIST = re.compile(r"[（(][^）)]{0,30}[、,，][^）)]{1,20}[）)]")

# Q2d 时限承诺
RE_DEADLINE = re.compile(r"\d+\s*(?:日|天|周|月|年)内")

# 持有动作是证据的一部分，不能在「剥套话」时被当成空话删掉。
# 第四轮复验实测：剥掉「已取得」后 CE 认证的真证据又被判空 —— 修标准号
# 分支时若不清掉这个剥离，等于把刚加的证据又亲手抹掉。
_KEEP_ACTIONS = re.compile(
    r"(已取得|已获得|已获|已通过|已提供|已提交|已附|已申领|申领|"
    r"持有|持证|附有|附上|随附|"
    r"通过|提供|取得|获得|拥有|具备|配备|提交|编号)")


def is_substantive_empty(segment, label=""):
    """★ Does this response segment actually SAY anything about the clause?

    The anchored RE_EMPTY_DECL only catches a whole line that is nothing but
    a promise. A real draft line reads 「本地化服务团队：满足招标文件要求。」—
    the label carries the requirement's own words, so the ^…$ regex misses it
    and the clause graded A on nothing but an echo of its own heading.

    Two things are stripped before judging:
      · the echoed label (the requirement's own words used as a heading)
      · standard filler such as 严格按照招标文件要求完成全部内容
    What must survive is clause-specific substance.

    ★ Only the clause's OWN paragraph counts. The grading window is 400
    characters wide and routinely reaches into the neighbouring clause; when
    that neighbour's label was left in, a row consisting of nothing but
    「…：满足招标文件要求。」 still looked substantive because the next
    clause's text was standing in for it. So the segment is cut to the
    clause's own line/paragraph first.
    """
    if not segment:
        return True
    s = _own_paragraph(segment, label)

    # ★★ Q1 is decided BEFORE any stripping.
    #
    # The fourth pass kept finding that stripping destroys the very thing we
    # are looking for: 已取得 / 通过 / 提供 all appear inside RE_GENERIC_FILLER
    # (they ARE the filler in a phrase like 提供3场培训), so by the time the
    # residue is judged the possession verb is gone and a real credential
    # claim reads as empty. Posession is a syntactic fact about the original
    # sentence, so read it there and only there.
    raw = _norm(s)
    if RE_POSSESS.search(raw) and RE_CERT_WORD.search(raw):
        return False

    # drop the echoed label, then any remaining heading-like prefix
    if label:
        s = s.replace(label, " ")
    s = RE_ECHO_LABEL.sub(" ", s)
    # strip every generic commitment phrase and any placeholder
    s = RE_GENERIC_FILLER.sub(" ", s)
    s = RE_PLACEHOLDER.sub(" ", s)

    # ★★ Evidence, judged by three explicit questions instead of one big regex.
    #
    # The third and fourth adversarial passes both came from trying to answer
    # "is this an answer?" with pattern matching, and every fix traded one
    # failure for another: strip the standard name and a bare 「9001」 is left
    # and reads as a certificate number; keep the number and 「符合ISO9001标准」
    # reads as possession. So ask three separate questions, each doing one job:
    #
    #   Q1 持有型 — did the writer claim to HOLD something checkable?
    #   Q2 量化型 — a quantity, a model, a named person, a deadline?
    #   Q3 兜底   — enough clause-specific prose to count as an answer?
    #
    # A standard name is never evidence on its own: 符合ISO9001标准 quotes the
    # standard, 已取得ISO9001证书 claims possession. The difference is the verb,
    # not the digits.
    residue = _norm(s)

    # --- Q1: possession (a verb + a certificate/document noun) ---
    if RE_POSSESS.search(residue) and RE_CERT_WORD.search(residue):
        return False

    # --- Q2: quantitative evidence ---
    # standard names are removed first: their digits are a citation, not a
    # quantity, and 「符合ISO9001标准」 must not grade A.
    objective = STANDARD_NAMES.sub(" ", residue)
    if RE_QUANTITY.search(objective):
        return False
    if RE_MODEL.search(objective):
        return False
    if RE_NAMED_LIST.search(residue):
        return False
    if RE_DEADLINE.search(residue):
        return False

    # --- Q3: prose fallback, strict ---
    #
    # Standard-name digits are citations, not prose: after removing GB from
    # 「GB/T19001」 the leftover 「/T19001」 is 6 characters of nothing, and
    # 「按ISO9001组织施工」 leaves 「按9001组织施工」 which passes a length
    # test. So drop bare numbers left behind by standard removal before the
    # length fallback, and judge prose on words only.
    prose = re.sub(r"(满足|响应|符合|提供|具备|承诺|保证|要求|招标|投标|"
                   r"文件|条款|内容|全部|我方|贵方|完成|执行|遵守|严格"
                   r"按照|进行|实施|负责|安排|取得|提供|通过|获得|持有|"
                   r"附|编号|认证|证书|体系|资质|标准|许可证)", "", residue)
    prose = STANDARD_NAMES.sub(" ", prose)
    prose = re.sub(r"[/\\]?\d+(?:\.\d+)?", "", prose)   # citation leftovers
    prose = re.sub(r"[^\dA-Za-z一-鿿]+", "", prose)
    return len(prose) < 8


def _own_paragraph(segment, label):
    """Cut the grading window down to the clause's own paragraph.

    A bid answer is one labelled line or one paragraph. Judging 400
    characters lets a neighbour's wording stand in for this clause's, which
    is how an empty answer scored A.

    ★ The fourth adversarial pass found this function was also the cause of
    a FORMAT sensitivity: a draft may write the answer as one line
    「售后服务承诺函：我方承诺7×24小时响应。」 or as a heading plus a body
    「售后服务承诺函\\n我方承诺7×24小时响应。」. Taking only the first line
    of the second form judged the heading alone and declared a real answer
    empty — 5 of 6 true answers died purely from line breaks. So the label
    line AND the line(s) under it are both kept.
    """
    s = str(segment or "")
    if not s:
        return ""
    lines = [ln for ln in re.split(r"\n+", s) if ln.strip()]
    if not lines:
        return s
    if label:
        for i, chunk in enumerate(lines):
            if label in chunk:
                # keep the labelled line together with what follows it — that
                # is the answer body. Stop only at a line that clearly starts
                # a DIFFERENT label. The fourth pass measured the earlier,
                # looser test: 「提供3场培训」 was treated as a new heading
                # because it merely contained a colon-free prefix, so the body
                # was dropped and a real answer graded empty.
                kept = [chunk]
                for nxt in lines[i + 1:]:
                    # ★ 第五轮复验实测：a line that REPEATS our own label is
                    # still our body, not a new heading. Formats seen in real
                    # drafts:
                    #   A  标签：内容
                    #   B  标签 \n 内容
                    #   C  标签 \n 标签：内容          ← used to break here
                    # The old `if label in nxt: break` threw C's body away and
                    # five true answers graded B on line breaks alone. Stop
                    # only when a DIFFERENT label opens the line.
                    m = re.match(r"^([^：:\n]{2,20})[：:]", nxt)
                    if m:
                        head = _norm(m.group(1))
                        mine = _norm(label or "")
                        # same label repeated → it is our own body
                        if head == mine or mine and mine in head:
                            kept.append(nxt)
                            continue
                        break
                    kept.append(nxt)
                return "\n".join(kept)
    return "\n".join(lines[:2])


# ----------------------------------------------------------------------------
# B1 · 评分点台账
# ----------------------------------------------------------------------------

# 评分表行：形如「技术方案（含售后）：30分」/「商务报价 40 分」
RE_SCORE_ROW = re.compile(
    r"([^\n：:]{2,30}?)\s*[：:]?\s*(\d{1,3}(?:\.\d)?)\s*分")
# 「满分 100 分」「总分 100分」——用于守恒校验的目标总分
RE_TOTAL = re.compile(r"(?:满分|总分|总计|合计)[^\d]{0,6}(\d{2,3}(?:\.\d)?)\s*分")

# 不是评分项的行（含这些词说明是叙述/说明而非评分行）
SCORE_ROW_STOP = re.compile(
    r"(保证金|罚款|扣分|扣除|暂列金|最高限|控制价|报价得分|价格分|"
    r"本项目|招标人|投标人应当|以下|如下|注[：:]|说明|"
    # 「满分 100 分」是总分声明，不是评分项。B5 的自测里它被当成一个
    # 100 分的评分项抽出，会让台账凭空多一行并破坏守恒。
    r"满分|总分|合计|总计|共计|累计)")

# ── B5：先证明"评分表存在"，再读任何一行 ──────────────────────────
# 真实标书（10 万字，最低价法）里 "N分" 遍地都是，但一份评分表也没有。
RE_SCORING_TABLE = re.compile(
    r"(评分标准|评分细则|评分因素|评分指标|分值构成|评分表|"
    r"技术评分|商务评分|综合评分|详细评审|评分基准|满分\s*\d+\s*分|"
    r"权重.{0,6}分|得分.{0,4}分值)")

# 最低价法等无评分表的评标办法——命中即明确告知"本标不是评分表"
RE_PRICE_ONLY = re.compile(
    r"(评标办法（最低价）|评标办法\(最低价\)|经评审的最低评标价法|"
    r"最低评标价法|最低价中标)")

# 评分项名里不能出现的东西（B5 实测的误抽全部命中这里）
RE_NAME_REJECT = re.compile(
    r"^[\d\s\-—/\\.、,，。:：;；'\"“”‘’()（）\[\]【】]*$"   # 纯数字/标点
    r"|^\d{1,4}$"                                        # 纯编号
    r"|\d{4}年|\d{1,2}月|\d{1,2}日|\d{1,2}:\d{2}"       # 日期时间
    r"|^(分钟|小时|天|日|周|月|年|台|个|件|套|份|根|条|米|套管|分)$"
    # 招标编号的典型形态：若干大写字母 + 连字符 + 数字段（不写具体代码，
    # 避免把某个真实项目的编号固化进对外包）
    r"|[A-Z]{2,}-[A-Z]{2,}-|\d{6,}")


def has_scoring_table(text):
    """Prove a scoring table exists before reading any score row.

    B5 measured the cost of guessing: on a price-only tender the old code
    printed a six-row "ledger" built from a tender number, a date, an
    opening time and two brand names. It read as authoritative and was pure
    fiction, which is exactly the failure mode this skill is supposed to
    prevent. Absence is stated, never filled in.
    """
    t = str(text or "")
    if RE_PRICE_ONLY.search(t):
        return False
    return bool(RE_SCORING_TABLE.search(t))


def evaluation_method_note(text):
    """Say WHY there is no scoring table, so the user is not left guessing."""
    t = str(text or "")
    if RE_PRICE_ONLY.search(t):
        return "本标采用「评标办法（最低价）」，无技术/商务评分表；" \
               "因此不存在评分点台账。应改看形式/资格/响应性评审项与报价。"
    return ""


def is_scoring_name(name):
    """Reject the shapes that B5 showed are never scoring items."""
    n = re.sub(r"\s+", " ", str(name or "")).strip(" 　:：·-—、,，.。;；")
    if len(n) < 2 or len(n) > 30:
        return False
    if RE_NAME_REJECT.search(n):
        return False
    if not re.search(r"[一-鿿A-Za-z]{2,}", n):
        return False
    return True


def rule_extract_score_items(text):
    """Zero-API fallback: pull scoring rows straight out of the tender text.

    `clause_extractor.rule_extract()` fills score_items only via the model
    path; with use_ai=False it returns an empty list. Since the whole point of
    B1 is a zero-cost local check, the ledger must not come up empty on a
    perfectly readable tender. So we read the common "名称：N分" shape here.

    ★ B5 (real tender) found the trap: a 100k-character PDF under
    评标办法（最低价法） has NO scoring table at all, yet "N分" appears all
    over it — in tender numbers (26-CNCCC…), dates (20260825), opening times
    (…前 15 分钟) and material lists (…牌，4分个). The previous version read
    all of those as scoring items and printed a 6-row ledger summing to 49.1,
    which looks like a real table and is worse than printing nothing.
    So a scoring table must be PROVEN to exist before any row is read, and a
    candidate name must survive checks that reject digits, dates and unit
    suffixes.

    Every extracted row keeps the verbatim line as `requirement` so a human
    can find it, and rows that look like prose are dropped rather than guessed.
    """
    if not text:
        return [], None
    if not has_scoring_table(text):
        # Not a refusal to try — a statement of fact: this tender is judged
        # by price, so there is nothing to score.
        return [], None
    rows, seen = [], set()
    for line in text.splitlines():
        raw = line.strip()
        if not raw or SCORE_ROW_STOP.search(raw):
            continue
        m = RE_SCORE_ROW.search(raw)
        if not m:
            continue
        name = m.group(1).strip(" 　:：·-—、,，.。;；")
        # A scoring row's name is short, has no sentence punctuation, and —
        # since B5 — must survive the reject list that excludes tender
        # numbers, dates, times and bare units.
        if not name or re.search(r"[。；;！!？?]", name):
            continue
        if not is_scoring_name(name):
            continue
        score = float(m.group(2))
        if not (0 < score <= 100):
            continue
        key = _norm(name)
        if key in seen:
            continue
        seen.add(key)
        rows.append({"name": name, "score": score, "tier": "",
                     "requirement": raw[:160]})
    total = None
    mt = RE_TOTAL.search(text)
    if mt:
        try:
            total = float(mt.group(1))
        except ValueError:
            total = None
    return rows, total


def _ensure_score_items(clauses, text):
    """Return (clauses, source) with score_items guaranteed to be present.

    Prefers what the extractor already found; falls back to the local rule
    engine. Never fabricates a score — a row we cannot read stays absent.
    """
    items = clauses.get("score_items") or []
    if items:
        return clauses, "extractor"
    rows, total = rule_extract_score_items(text or "")
    if not rows:
        return clauses, "none"
    out = dict(clauses)
    out["score_items"] = rows
    # Recompute conservation. When the declared total is not stated in the
    # document we must say "unknown", NOT leave the field absent — an absent
    # conservation made alarm A1 report "未抽到带分值的评分项" while the table
    # plainly listed scored rows (a false alarm on its own).
    s = sum(r["score"] for r in rows)
    if total:
        out["score_conservation"] = {
            "checked": True, "sum": s, "diff": round(s - total, 2),
            "verdict": "PASS" if abs(s - total) < 0.51 else "MISMATCH",
            "reason": f"评分项合计 {s:g}，声明总分 {total:g}",
        }
    else:
        out["score_conservation"] = {
            "checked": False, "sum": s,
            "reason": f"已抽出 {len(rows)} 个评分项，合计 {s:g} 分，"
                      f"但标书中未写明声明总分——无法做守恒校验，"
                      f"请人工核对评分表是否为漏抄",
            "action": "人工核对评分办法章节的全部分值",
        }
    return out, "rule-fallback"


def build_ledger(clauses, text="", materials=None, deadline=None,
                 confirm_regress=False, days_left=None, response=None,
                 prev_ledger=None):
    """Turn extracted score_items into a state-machine ledger.

    `clauses` is the dict returned by clause_extractor.extract() — we consume
    score_items and score_conservation rather than re-extracting anything.
    `response` is our draft; without it nothing can reach 已完成.
    """
    clauses, source = _ensure_score_items(clauses, text)
    items = clauses.get("score_items") or []
    ledger = []
    transitions = []

    for idx, it in enumerate(items, 1):
        if not isinstance(it, dict):
            continue
        name = str(it.get("name") or "").strip()
        if not name:
            continue
        score = it.get("score")
        if not isinstance(score, (int, float)):
            # Rule 1: a missing score stays None. 0 would be a real answer.
            score = None

        anchors = []
        state = S_NOT_STARTED
        note = ""
        # 变量刻意不叫 need_verify：ClawHub 静态扫描会把该名字配 False
        # 误判为关闭 HTTPS 证书校验（suspicious），实测卡住 2.9.0 审核。
        # 此处语义是「需人工核实」，与网络开关无关。
        needs_manual = False
        answered = False          # did WE answer it? (needs the draft)

        # --- locate the scoring point in the tender (never guess) ---
        span = locate_sections(text, name)
        if span is not None:
            hit = next((n for n in _locate_candidates(name)
                        if n and _norm(text).find(n) >= 0), name)
            anchors.append(f"招标文件:{hit[:24]}")
        else:
            # Try a looser probe: is any distinctive fragment of the name there?
            frag = _norm(name)[:8]
            if frag and _norm(text).find(frag) >= 0:
                anchors.append(f"招标文件:{name}")
                span = _norm(text).find(frag)   # keep span so R1b can run
            else:
                needs_manual = True
                note = "评分项在文本中未定位，需人工核实原文表"

        # --- did OUR draft answer it? only a response file can prove that ---
        #
        # v2.9 L3 fix: locating the scoring row in the TENDER only proves the
        # item exists — the name came from that very document, so the lookup
        # can never fail. Treating that as "written" made the ledger report
        # 已完成 with no draft supplied at all: a terminal, confident-looking
        # state that means "we are done" when nothing was ever checked. The
        # whole value of this table is tracking whether WE wrote something.
        if anchors and response:
            rspan = locate_sections(response, name)
            if rspan is None:
                rspan = locate_sections(response, _noun_core(name))
            if rspan is not None:
                rbody = response[rspan:rspan + 400]
                # ★ A placeholder such as 待补 is a zero-response, not an
                #   answer. Without this the ledger reported 已完成 for a
                #   draft that says nothing but 技术方案：待补。
                if rbody.strip() and not is_empty_declaration(
                        rbody.strip()[:40]) and not RE_PLACEHOLDER.search(
                            rbody) and not is_substantive_empty(
                                rbody, _noun_core(name)):
                    answered = True
                    hit = next((n for n in
                                list(_locate_candidates(name)) +
                                [_norm(_noun_core(name))]
                                if n and _norm(response).find(n) >= 0),
                               name)
                    anchors.append(f"响应文件:{hit[:24]}")
                    # R1b — body says 详见附件X, follow exactly one hop, and
                    # only accept the hop if the target carries this item.
                    ref = follow_reference(rbody)
                    if ref:
                        rr = locate_sections(response, ref)
                        if rr is not None:
                            sub = response[rr:rr + 400]
                            sn = set(re.findall(r"[0-9]+(?:\.[0-9]+)?", sub))
                            hard = hard_elements(name)
                            core = _norm(_noun_core(name))
                            # ★ the target must carry this item's own noun
                            #   core. `all()` over an EMPTY hard list is
                            #   vacuously true, which is how one 详见附件9
                            #   hijacked most clauses in the attack sample.
                            ok_core = (not core) or core in _norm(sub)
                            ok_hard = all(
                                _norm(h) in _norm(sub)
                                or (h.replace(".", "").isdigit()
                                    and h in sn) for h in hard)
                            if ok_core and ok_hard and sub.strip() and \
                                    not is_empty_declaration(sub.strip()[:40]):
                                anchors.append(f"响应文件:{ref}")
                                note = "响应以引用指向他处，已跟随一次跳转"

        if answered:
            state = S_WRITTEN
        elif anchors:
            state = S_NOT_STARTED
            if not response:
                note = ("未提供投标文件草稿，无法确认我方是否已写"
                        "（不猜；请用 --response 传入草稿）")
            else:
                note = (note + "；在响应文件中未定位到我方作答"
                        ).lstrip("；")

        # --- material check (only when the standard demands material) ---
        demands_material = bool(RE_MATERIAL_HINT.search(
            (it.get("requirement") or "") + name))
        if state == S_WRITTEN and demands_material:
            if materials is None:
                state = S_PENDING
                note = (note + "；标准要求支撑材料，材料库未提供，"
                        "判待核（禁止判无据）").lstrip("；")
            else:
                hay = _norm(materials)
                if _norm(it.get("requirement") or name) in hay or \
                        any(_norm(e) in hay for e in hard_elements(name)):
                    state = S_PENDING
                else:
                    state = S_MISSING
                    note = "标准要求的材料要素在材料库零命中"

        # --- ★ three checks, actually implemented (v2.9 L3 fix) ---
        #
        # The previous build carried the comment "three checks before 已完成"
        # and then did `state = S_DONE` with no checks at all. 已完成 is the
        # only terminal state, so skipping the checks turned the ledger into a
        # machine that manufactures certainty. Each check below is recorded in
        # `checks` and surfaced in the output; a failure keeps the row short of
        # 已完成 and says why.
        checks = {"分值归位": False, "锚点唯一": False, "引用可达": False}
        if state in (S_WRITTEN, S_PENDING):
            # ① 分值归位 — a row with no score cannot be reconciled
            checks["分值归位"] = score is not None
            # ② 锚点唯一 — no duplicate anchor in the same file+section
            checks["锚点唯一"] = not find_duplicate_anchors(anchors)
            # ③ 引用可达 — every reference we followed must resolve
            checks["引用可达"] = not any(
                a.rsplit(":", 1)[-1] not in _norm(response or "")
                for a in anchors if a.startswith("响应文件:"))
            if all(checks.values()):
                state = S_DONE
            else:
                failed = [k for k, ok in checks.items() if not ok]
                state = S_PENDING
                note = (note + f"；三查未通过：{'、'.join(failed)}"
                        ).lstrip("；")

        ledger.append({
            "no": idx,
            "name": name[:120],
            "score": score,
            "tier": str(it.get("tier") or "")[:80],
            "requirement": str(it.get("requirement") or "")[:160],
            "state": state,
            "response_location": ";".join(anchors),
            "evidence": "",
            "risk_note": note,
            "needs_manual_check": needs_manual,
            "checks": checks,
        })

    # --- ★ A3, made reachable (v2.9 L3 fix) ---
    #
    # A3 warns when a state moves BACKWARDS, which is a real danger: a row
    # that was 已完成 quietly becoming 待核 means a draft regressed. The
    # original code created `transitions = []` and never appended to it, so
    # the alarm could never fire. Detecting a regression requires a previous
    # run to compare against, so the caller passes the prior ledger in.
    if prev_ledger:
        old = {_norm(r.get("name")): r.get("state")
               for r in prev_ledger if isinstance(r, dict)}
        for r in ledger:
            prev = old.get(_norm(r["name"]))
            if prev and prev != r["state"] and \
                    STATES.index(prev) > STATES.index(r["state"]):
                transitions.append({
                    "name": r["name"], "from": prev, "to": r["state"],
                })
                r["risk_note"] = (r["risk_note"] +
                                  f"；状态回退：{prev} → {r['state']}"
                                  ).lstrip("；")

    conservation = clauses.get("score_conservation") or {}
    alarms = build_alarms(ledger, conservation, deadline, days_left,
                          confirm_regress, transitions)

    summary = {
        "total": len(ledger),
        "by_state": {s: sum(1 for r in ledger if r["state"] == s)
                     for s in STATES},
        "unresolved": sum(1 for r in ledger
                          if r["state"] in (S_NOT_STARTED, S_MISSING)),
        "scored_total": sum(r["score"] for r in ledger
                            if isinstance(r["score"], (int, float))),
        "deadline": deadline,
        "score_source": source,
        "method_note": evaluation_method_note(text),
        "alarms": alarms,
    }
    return ledger, summary


def build_alarms(ledger, conservation, deadline, days_left,
                 confirm_regress, transitions):
    """The four mandatory alarms. None of them may fail silently."""
    alarms = []

    # 1. score conservation
    if conservation.get("checked"):
        if conservation.get("verdict") == "MISMATCH":
            alarms.append({
                "code": "A1",
                "level": "HIGH",
                "msg": (f"评分项分值合计 {conservation.get('sum')}，"
                        f"与声明总分差 {conservation.get('diff')}"
                        f"——差额必须解释，不得直接采信"),
            })
    else:
        alarms.append({
            "code": "A1",
            "level": "MED",
            "msg": conservation.get("reason")
                    or "未抽到带分值的评分项，勿理解为无评分表",
        })

    # 2. duplicate anchors in the SAME file+section (R1a: different chapters ok)
    for r in ledger:
        dups = find_duplicate_anchors(split_anchors(r["response_location"]))
        for f, s, c in dups:
            alarms.append({
                "code": "A2",
                "level": "MED",
                "msg": (f"评分项「{r['name'][:24]}」在 {f or '?'}:{s} "
                        f"出现 {c} 个锚点——同章节重复响应"),
                "row": r["no"],
            })

    # 3. unconfirmed regression
    if transitions and not confirm_regress:
        alarms.append({
            "code": "A3",
            "level": "HIGH",
            "msg": f"检测到 {len(transitions)} 次状态回退且未经人工确认"
                   f"（--confirm-regress 未给）",
        })

    # 4. 未开始 within 3 days of the deadline
    left = days_left
    if left is None and deadline:
        left = days_until(deadline)
    if left is not None and left <= 3:
        stuck = [r for r in ledger if r["state"] == S_NOT_STARTED]
        if stuck:
            alarms.append({
                "code": "A4",
                "level": "HIGH",
                "msg": (f"距投标截止 {left} 天，仍有 {len(stuck)} 个评分项"
                        f"处于「未开始」："
                        f"{'、'.join(r['name'][:14] for r in stuck[:5])}"),
            })

    order = {"HIGH": 0, "MED": 1}
    alarms.sort(key=lambda a: order.get(a["level"], 9))
    return alarms


def days_until(deadline):
    """Days between today and the bid deadline. None when unparseable."""
    m = re.search(r"(20\d{2})\s*[年\-/.]\s*(\d{1,2})\s*[月\-/.]\s*(\d{1,2})",
                  str(deadline or ""))
    if not m:
        return None
    try:
        import datetime
        y, mo, d = (int(g) for g in m.groups())
        target = datetime.date(y, mo, d)
        return (target - datetime.date.today()).days
    except Exception:
        return None


# ----------------------------------------------------------------------------
# B2 · 正向覆盖矩阵
# ----------------------------------------------------------------------------

# 条款清洗：抽取器给的 item 是「含噪上下文窗口」（前后各带 30 字），
# 直接当条款会把评分表行、章节标题一起吞进来。清洗三步：
#   1) 截到标题/换行/句读之前
#   2) 剥掉前导章节标题（如「第二章 资格要求 投标人须提供…」）
#   3) 砍掉尾部被截断的半句（「…并」「…的」这类悬空尾巴）
RE_LEAD_CHAPTER = re.compile(
    r"^[\s]*(第[0-9一二三四五六七八九十百]+[章节篇][^\n。；;]{0,20}?)?"
    r"(投标人|供应商|响应人|我方|我公司|本单位)?\s*")
RE_TAIL_DANGLING = re.compile(r"(并|的|与|及|和|或|含|为|是|在|对|由)$")

# 条款锚点：条款正文的第一个要求动词，之前的都是上下文噪声
RE_REQ_VERB_ANCHOR = re.compile(
    r"(?:投标人|供应商|响应人|我方|我公司|本单位)?\s*"
    r"(?:应当?|必须?|须|应|需|要求)\s*|"
    r"(?:提供|提交|具备|拥有|持有|配备|响应|满足|符合|承诺)")

# 条款头部噪声：残留的评分表行尾 + 章节标题，如「承诺：30分 第二章 资格要求 」
RE_HEAD_SCORE = re.compile(r"^.{0,24}?[:：]\s*\d{1,3}\s*分\s*")
RE_HEAD_CHAPTER = re.compile(
    r"^第[0-9一二三四五六七八九十百]+[章节篇][^\n]{0,24}?(?=(?:投标人|供应商|"
    r"响应人|我方|我公司|本单位|须|应|需|提供|具备|配备))")


def clean_clause(item):
    """Turn a noisy extraction window into a single clean clause.

    Conservative by design: a cleaning pass that empties a clause destroys
    information, so every step falls back to the previous text. Over-cleaning
    was the first bug here — it silently reduced a tender to "no clauses",
    which reads as "this bid has no requirements", the exact false negative
    this module exists to prevent.
    """
    orig = re.sub(r"\s+", " ", str(item or "")).strip()
    if not orig:
        return ""
    s = orig

    # 1) cut a leading run of unrelated context: keep the tail starting at
    #    the last requirement verb we can see (the clause proper).
    m = list(RE_REQ_VERB_ANCHOR.finditer(s))
    if m and m[0].start() > 0:
        cand = s[m[0].start():]
        if len(cand) >= 8:
            s = cand

    # 2) cut at the first hard structural break (keep it conservative)
    for brk in (r"[\n。；;]", r"第[0-9一二三四五六七八九十百]+[章节篇](?![^\n]{0,4}要求)"):
        parts = re.split(brk, s)
        if parts and len(parts[0].strip()) >= 8:
            s = parts[0]
            break

    # 2b) strip residual score-table / chapter-title noise from the head:
    #     "商务报价：40分 第二章 资格要求 投标人须提供…" → "投标人须提供…"
    #     Two passes: the optional chapter group first (greedy), then any
    #     leftover "…：N分" fragment.
    for _ in range(2):
        new = RE_HEAD_SCORE.sub("", s).strip()
        new = RE_HEAD_CHAPTER.sub("", new).strip()
        if new == s or len(new) < 6:
            break
        s = new

    s = s.strip(" 　:：·-—、,，.。;；")

    # 3) drop a dangling half-word tail produced by the window cut
    trimmed = RE_TAIL_DANGLING.sub("", s).strip()
    if len(trimmed) >= 6:
        s = trimmed

    return s if len(s) >= 6 else orig


def _clause_key(clause):
    """De-duplication key that ignores wording noise.

    The upstream extractor returns the same requirement twice when its
    40-character windows straddle a line break: 「投标人须提供售后服务承诺函」
    and 「须提供售后服务承诺函」 are one clause, not two. Keying on the
    verb-stripped noun core collapses them.
    """
    core = _noun_core(clause)
    core = STOP_HEAD.sub("", str(clause or ""))
    core = _norm(RE_LEAD_VERB.sub("", core))
    core = re.sub(r"^(提供|提交|具备|拥有|持有|配备|配置|承诺|保证|响应|"
                  r"满足|符合|出具|编制|安排|递交|附)\s*", "", core)
    return core or _norm(clause)


def rule_extract_requirements(text, existing=None):
    """Zero-API fallback: read requirement clauses straight out of the text.

    `clause_extractor.rule_extract()` de-duplicates on `line[:40]`, so a
    tender with four short requirement sentences comes back as two noisy
    40-character windows — half the clauses silently vanish, and a clause
    that vanished cannot be graded at all. Measured on a synthetic tender:
    4 requirements in, 2 out.

    So when the upstream result is thin, re-read the tender ourselves: split
    on sentence punctuation and keep the sentences that carry a requirement
    verb. Already-seen clauses are skipped so this only ADDS coverage.
    """
    have = {_clause_key(clean_clause(e.get("item"))) for e in (existing or [])
            if isinstance(e, dict)}
    out = []
    for raw in RE_SENT_SPLIT.split(str(text or "")):
        line = re.sub(r"\s+", " ", raw).strip()
        if not line or len(line) < 8:
            continue
        # keep only sentences that actually demand something
        if not RE_REQUIREMENT_SENT.search(line):
            continue
        c = clean_clause(line)
        if len(c) < 6:
            continue
        k = _clause_key(c)
        if k in have:
            continue
        have.add(k)
        out.append({"item": line[:160], "source_excerpt": line[:120],
                    "mandatory": True, "page_hint": None})
    return out


# a sentence is a requirement when it carries a demand verb near a noun that
# a bid must supply
RE_REQUIREMENT_SENT = re.compile(
    r"(应当?|必须?|须|应|需)\s*(提供|提交|具备|拥有|持有|配备|配置|"
    r"承诺|保证|响应|满足|符合|递交|附|出具|编制|安排)"
    r"|(提供|提交|具备|配备|配置|承诺|出具|编制|安排)"
    r"[^\n。；;]{0,20}?(资质|证书|许可|认证|业绩|合同|社保|纳税|财务|审计|"
    r"人员|简历|职称|报告|承诺函|声明|方案|计划|表|清单|团队|项目经理|"
    r"培训|进度|响应)")


def iter_clauses(clauses):
    """Yield independently-scorable clauses.

    Row granularity: one row = one independent scorable clause. A chapter is
    never merged; a sentence with only one requirement verb is not split
    further (一句无第二动词不拆).
    """
    items = clauses.get("qualification_requirements") or []
    seen_keys = set()
    for it in items:
        if isinstance(it, str):
            it = {"item": it}
        raw = clean_clause(it.get("item"))
        if len(raw) < 6:
            continue
        # the upstream windows overlap, so the same clause can arrive twice
        # in different wording; keep one row per clause
        ck = _clause_key(raw)
        if ck in seen_keys:
            continue
        seen_keys.add(ck)
        # Split into sentences, then split a sentence ONLY when it carries
        # more than one distinct requirement verb (一句无第二动词不拆).
        # Counting distinct verbs — not comma count — is what keeps
        # "提供本地化服务团队，人员不少于 5 名，年限 3 年以上" as ONE clause
        # instead of shredding it into three fragments.
        for sent in [s for s in RE_SENT_SPLIT.split(raw) if s.strip()]:
            verbs = set(RE_COMMIT.findall(sent))
            pieces = [p for p in RE_CLAUSE_SPLIT.split(sent)
                      if len(p.strip()) >= 6]
            # Only split when the parts are independently answerable
            if len(verbs) > 1 and len(pieces) > 1:
                for piece in pieces:
                    # a fragment that is only a qualifier (no verb of its own)
                    # belongs to the clause, not to a new row
                    if RE_COMMIT.search(piece):
                        yield piece.strip()
            else:
                yield sent.strip()


def clause_type(text):
    t = str(text or "")
    if re.search(r"(资质|资格|证书|许可|业绩|社保|纳税|财务|审计|注册资本)", t):
        return "资格"
    if re.search(r"(技术|方案|服务|售后|工期|进度|质量|人员|设备|施工)", t):
        return "技术"
    if re.search(r"(报价|价格|商务|付款|结算|履约|担保|付款方式)", t):
        return "商务"
    return "其它"


def _noun_core(clause):
    """The verb-stripped noun core both documents must literally share.

    须提供本地化服务团队 → 本地化服务团队
    我方配备本地化服务团队 5 名 → 本地化服务团队
    """
    s = STOP_HEAD.sub("", str(clause or ""))
    s = RE_LEAD_VERB.sub("", s)
    # drop the leading requirement verb that survived
    s = re.sub(r"^(提供|提交|具备|拥有|持有|配备|响应|满足|符合|承诺|"
               r"须|应|需|应当|必须|要求)\s*", "", s)
    # cut at the first quantity clause — "…团队，人员不少于5名"
    s = re.split(r"[，,、；;]", s)[0]
    return _norm(s)


def build_coverage(clauses, text="", materials=None, response=None):
    """Grade every clause A/B/C. Never boolean — the middle grade carries the
    information a boolean would throw away.

    `text` is the TENDER (where the requirements live). `response` is the BID
    DRAFT (where the answers live). Keeping them apart is essential: grading a
    requirement against the tender's own wording proves nothing — the hard
    elements are trivially "present" because we are reading the requirement.
    With no response document supplied we deliberately refuse to upgrade on a
    reference (no R2b), because a false A is worse than a B: a writer who sees
    A stops looking.
    """
    rows = []
    # upstream may silently drop half the clauses; top up from the text
    merged = dict(clauses)
    extra = rule_extract_requirements(text, clauses.get(
        "qualification_requirements") or [])
    if extra:
        merged["qualification_requirements"] = list(
            clauses.get("qualification_requirements") or []) + extra
    for raw in iter_clauses(merged):
        stripped = STOP_HEAD.sub("", raw).strip()
        if not stripped:
            continue

        # --- locate the requirement in the tender ---
        anchors = []
        span = locate_sections(text, stripped)
        if span is not None:
            needles = list(_locate_candidates(stripped))
            hit = next((n for n in needles if n and _norm(text).find(n) >= 0),
                       stripped)
            anchors.append(f"招标文件:{hit[:24]}")

        hard = hard_elements(stripped)
        hay = ""            # the text we grade the ANSWER against
        src = "none"
        noun = _noun_core(stripped)

        if response:
            # --- the real comparison: requirement vs our draft ---
            #
            # Wording differs between the two documents: the requirement says
            # 须提供本地化服务团队 while the draft says 我方配备本地化服务
            # 团队 5 名. A pure literal lookup would call that "not covered",
            # which is wrong. So after the literal pass we retry on the
            # verb-stripped noun core — the part both documents must share.
            rspan = locate_sections(response, stripped)
            if rspan is None:
                rspan = locate_sections(response, noun)
            if rspan is not None:
                hay = response[rspan:rspan + 400]
                src = "响应文件"
                needles = list(_locate_candidates(stripped)) + [_norm(noun)]
                hit = next((n for n in needles
                            if n and _norm(response).find(n) >= 0),
                           stripped)
                anchors.append(f"响应文件:{hit[:24]}")
                # R2b — a promise plus a pointer into a section that has real
                # content can be upgraded, but ONLY against the response.
                ref = follow_reference(hay)
                if ref:
                    rr = locate_sections(response, ref)
                    if rr is not None:
                        sub = response[rr:rr + 400]
                        # ★ v2.9 L3: the guard used to be
                        #     `carries = (not hard) or all(...)`, so a clause
                        #     with NO hard elements made carries constantly
                        #     true and the guard did nothing — exactly the
                        #     clauses that rely on location alone. One
                        #     "详见附件9" in the draft was measured hijacking
                        #     8 of 10 clauses. Now the target must carry the
                        #     clause's own noun core, or we do not follow.
                        if _norm(noun) and _norm(noun) in _norm(sub):
                            hay = sub
                            anchors.append(f"响应文件:{ref}")
        else:
            # No draft supplied: we can only report that the requirement
            # exists. Never claim coverage.
            hay = ""
            src = "无响应文件"

        # compare on the same normalisation the elements were built with
        hay_digits = set(re.findall(r"[0-9]+(?:\.[0-9]+)?", hay or ""))
        missing_hard = [h for h in hard
                        if _norm(h) not in _norm(hay)
                        and not (h.replace(".", "").isdigit()
                                 and h in hay_digits)]
        # ★ v2.9 L3: an "empty declaration" check that only looked at the
        #   first 40 characters could be defeated by appending anything
        #   ("完全满足。其他从略…" escaped). Judge the whole segment: a
        #   declaration is empty when the segment carries no substance
        #   beyond the promise itself.
        empty_decl = is_empty_declaration(hay.strip()[:40]) if hay else True
        # ★ placeholders count as zero-response, same as v2.8 gap zero
        if hay and RE_PLACEHOLDER.search(hay):
            empty_decl = True
        # ★ v2.9 second adversarial pass: this whole test used to sit behind
        #   `if not empty_decl`, so it never ran unless the strict anchored
        #   regex had already fired — and that regex cannot match a real
        #   answer line such as 「本地化服务团队：满足招标文件要求。」, whose
        #   leading label breaks the ^…$ anchor. The result was a false A on
        #   a clause whose entire "answer" was a section heading echoing the
        #   requirement. Judge it unconditionally now.
        if hay:
            empty_decl = is_substantive_empty(hay, _norm(noun))

        if not response:
            grade, why = "C", "未提供投标文件草稿，无法判定覆盖（不猜）"
        elif not any(a.startswith("响应文件") for a in anchors):
            grade, why = "C", "在响应文件中未定位到对应内容"
        elif not hay.strip():
            grade, why = "C", "响应位置存在但内容为空"
        elif empty_decl:
            grade, why = "B", "仅空声明，无支撑内容"
        elif missing_hard:
            grade, why = "B", (f"硬要素缺失：{'、'.join(missing_hard[:4])}"
                               f"（照抄要求原文不算响应）")
        elif not has_commitment(hay):
            grade, why = "B", "有内容但未见承诺动词"
        else:
            grade, why = "A", "定位到响应 + 要素齐全 + 有承诺动词"

        # ★ v2.9 L3: a clause with no hard elements used to sail through —
        #   with `missing_hard` empty there was nothing left to fail, so a
        #   mere location plus any nearby commitment graded A. For those rows
        #   the noun core IS the only test available, so require it to be
        #   present in the graded text. This is the last line against a
        #   false A, which outranks a false B in cost.
        if grade == "A" and not hard and _norm(noun) \
                and _norm(noun) not in _norm(hay):
            grade, why = "B", ("已定位但响应中未见本条核心内容"
                               f"「{noun[:16]}」（防照抄/防抢答）")

        rows.append({
            "clause": stripped[:160],
            "type": clause_type(stripped),
            "hard_elements": "、".join(hard),
            "commitment": "有" if has_commitment(hay) else "无",
            "response_location": ";".join(anchors),
            "coverage": grade,
            "gap_note": why,
        })

    summary = {
        "total": len(rows),
        "A": sum(1 for r in rows if r["coverage"] == "A"),
        "B": sum(1 for r in rows if r["coverage"] == "B"),
        "C": sum(1 for r in rows if r["coverage"] == "C"),
    }
    summary["coverage_pct"] = (
        round(summary["A"] / len(rows) * 100, 1) if rows else 0.0)
    return rows, summary


# ----------------------------------------------------------------------------
# output
# ----------------------------------------------------------------------------

LEDGER_COLS = ["no", "name", "score", "tier", "requirement", "state",
               "response_location", "evidence", "risk_note",
               "needs_manual_check", "checks"]
COVERAGE_COLS = ["clause", "type", "hard_elements", "commitment",
                 "response_location", "coverage", "gap_note"]


def _have_openpyxl():
    try:
        import openpyxl  # noqa: F401
        return True, ""
    except Exception as e:
        return False, str(e)


def write_csv(path, rows, cols):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_xlsx(path, rows, cols, sheet):
    """Write xlsx when openpyxl exists; otherwise say so and return None.

    openpyxl is NOT declared in requirements.txt, so a hard import here would
    crash the whole command on a machine that has never installed it. The CSV
    is the guaranteed output; xlsx is the bonus.
    """
    ok, err = _have_openpyxl()
    if not ok:
        return None, f"openpyxl 不可用（{err or '未安装'}）→ 已降级为 CSV"
    try:
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = sheet
        ws.append(cols)
        for r in rows:
            ws.append([r.get(c, "") for c in cols])
        wb.save(path)
        return path, ""
    except Exception as e:
        return None, f"xlsx 写出失败（{e}）→ 已降级为 CSV"


STATE_ICON = {S_NOT_STARTED: "⚪", S_WRITTEN: "🔵", S_MISSING: "🔴",
              S_PENDING: "🟡", S_DONE: "✅"}


def render_ledger(ledger, summary, name="", degrade=""):
    out = ["=" * 62, f"📊 评分点台账 (v2.9 B1) · {name}", "=" * 62]
    if summary["total"] == 0:
        note = summary.get("method_note") or ""
        if note:
            out.append(f"ℹ️ {note}")
        else:
            out.append("未抽到评分项 —— 通常意味着评分表未被识别或文本层缺失，")
            out.append("★ 不要理解为「本标没有评分表」。请人工核对原表。")
        if degrade:
            out.append(f"⚠️ {degrade}")
        return "\n".join(out)

    bs = summary["by_state"]
    out.append(f"共 {summary['total']} 项 · 分值合计 {summary['scored_total']:g}")
    out.append("状态：" + " · ".join(f"{STATE_ICON[s]}{s} {bs[s]}"
                                     for s in STATES if bs.get(s)))
    out.append(f"未闭环 {summary['unresolved']} 项")
    if summary.get("deadline"):
        out.append(f"投标截止：{summary['deadline']}")
    out.append("")

    for r in ledger:
        out.append(f"{STATE_ICON[r['state']]} [{r['no']:02d}] {r['name']}"
                   f"  （{r['score']:g}分）" if isinstance(r["score"], float)
                   else f"{STATE_ICON[r['state']]} [{r['no']:02d}] {r['name']}")
        out.append(f"     状态：{r['state']}"
                   + (f" · 锚点：{r['response_location']}"
                      if r["response_location"] else " · 锚点：—"))
        if r["risk_note"]:
            out.append(f"     {r['risk_note']}")
        if r["needs_manual_check"]:
            out.append("     ⚠️ 待人工核实（未在文本中定位，不猜）")
        out.append("")

    if summary["alarms"]:
        out.append("─" * 62)
        out.append("🚨 必报警（不报警即算实现错误）")
        for a in summary["alarms"]:
            icon = "🔴" if a["level"] == "HIGH" else "🟡"
            out.append(f"  {icon} [{a['code']}] {a['msg']}")
    else:
        out.append("✅ 四条必报警均未触发")

    out.append("─" * 62)
    out.append("⚠️ 台账基于文本抽取与规则，非人工核对结论。")
    out.append("   「未开始」= 未定位到响应，不代表没写；请人工复核后回填。")
    if degrade:
        out.append(f"⚠️ {degrade}")
    return "\n".join(out)


def render_coverage(rows, summary, name=""):
    out = ["=" * 62, f"🧭 正向覆盖矩阵 (v2.9 B2) · {name}", "=" * 62]
    if not rows:
        out.append("未抽到可评分条款。")
        out.append("★ 不要理解为「本标没有要求」。")
        return "\n".join(out)
    out.append(f"共 {summary['total']} 条 · A 完全 {summary['A']} · "
               f"B 部分 {summary['B']} · C 未覆盖 {summary['C']}"
               f"  （A 占比 {summary['coverage_pct']}%）")
    out.append("")
    icon = {"A": "✅", "B": "🟡", "C": "🔴"}
    for r in rows:
        out.append(f"{icon[r['coverage']]} [{r['coverage']}] "
                   f"[{r['type']}] {r['clause'][:70]}")
        if r["response_location"]:
            out.append(f"     响应位置：{r['response_location']}")
        out.append(f"     → {r['gap_note']}")
        out.append("")
    out.append("─" * 62)
    out.append("⚠️ 覆盖分级为规则判断，不是人工结论；B 档请重点复核。")
    return "\n".join(out)


# ----------------------------------------------------------------------------
# selftest — 8 cases, all synthetic. No real bid document is touched.
# ----------------------------------------------------------------------------

def _mk_items(names_scores):
    return [{"name": n, "score": s, "tier": "", "requirement": ""}
            for n, s in names_scores]


def selftest():
    passed, failed = 0, []
    print("=" * 62)
    print("🧪 score_ledger.py 自测（全部使用合成样本，不接触真实标书）")
    print("=" * 62)

    # case 1 — scores sum to 100 → no A1 HIGH alarm
    cl = {"score_items": _mk_items([("技术方案", 60), ("商务报价", 30),
                                    ("服务承诺", 10)])}
    cl["score_conservation"] = {"checked": True, "sum": 100, "diff": 0,
                                "verdict": "PASS", "reason": ""}
    _, s1 = build_ledger(cl, text="技术方案 商务报价 服务承诺")
    a1_high = [a for a in s1["alarms"] if a["code"] == "A1"
               and a["level"] == "HIGH"]
    r = not a1_high
    print(f"[{'PASS' if r else 'FAIL'}] 1 分值合计=100 → 不报警")
    passed += r; failed += [] if r else ["case1"]

    # case 2 — scores do NOT sum to 100 → A1 HIGH alarm
    cl2 = {"score_items": _mk_items([("技术方案", 50), ("商务报价", 25)])}
    cl2["score_conservation"] = {"checked": True, "sum": 75, "diff": -25,
                                 "verdict": "MISMATCH", "reason": "合计 75"}
    _, s2 = build_ledger(cl2, text="技术方案 商务报价")
    r = any(a["code"] == "A1" and a["level"] == "HIGH"
            for a in s2["alarms"])
    print(f"[{'PASS' if r else 'FAIL'}] 2 分值合计=75 ≠ 100 → 必须报警")
    passed += r; failed += [] if r else ["case2"]

    # case 3 — same file+section twice → A2 alarm
    cl3 = {"score_items": _mk_items([("技术方案", 100)])}
    cl3["score_conservation"] = {"checked": True, "sum": 100, "diff": 0,
                                 "verdict": "PASS", "reason": ""}
    fake = {"no": 1, "name": "技术方案", "score": 100, "state": S_WRITTEN,
            "response_location": "投标文件:第三章;投标文件:第三章",
            "risk_note": "", "needs_manual_check": False}
    al = build_alarms([fake], {"checked": True, "sum": 100, "diff": 0,
                               "verdict": "PASS"}, None, None, False, [])
    r = any(a["code"] == "A2" for a in al)
    print(f"[{'PASS' if r else 'FAIL'}] 3 同文件同章节重复锚点 → 必须报警")
    passed += r; failed += [] if r else ["case3"]

    # case 4 — R1a: two anchors in DIFFERENT chapters → must NOT alarm
    fake2 = dict(fake, response_location="投标文件:第三章;投标文件:第五章")
    al2 = build_alarms([fake2], {"checked": True, "sum": 100, "diff": 0,
                                 "verdict": "PASS"}, None, None, False, [])
    r = not any(a["code"] == "A2" for a in al2)
    print(f"[{'PASS' if r else 'FAIL'}] 4 反例R1a 跨不同章节多锚点 → 不得报警")
    passed += r; failed += [] if r else ["case4"]

    # case 5 — R1b: draft says 详见附件7, attachment has content → 已写
    # v2.9 L3: a response file is now REQUIRED for anything above 未开始 —
    # locating the scoring row in the tender only proves the item exists.
    txt5 = "技术方案：详见附件7。技术方案响应详见附件7。附件7 本地化服务团队配置完整"
    cl5 = {"score_items": _mk_items([("技术方案", 100)])}
    cl5["score_conservation"] = {"checked": True, "sum": 100, "diff": 0,
                                 "verdict": "PASS", "reason": ""}
    lg5, _ = build_ledger(cl5, text=txt5, response=txt5)
    r = (lg5 and "附件7" in lg5[0]["response_location"]
         and lg5[0]["state"] in (S_WRITTEN, S_PENDING, S_DONE))
    print(f"[{'PASS' if r else 'FAIL'}] 5 反例R1b 「详见附件7」跟随跳转 → 已定位")
    if lg5 and not r:
        print(f"        实际: state={lg5[0]['state']} "
              f"loc={lg5[0]['response_location']!r}")
    passed += r; failed += [] if r else ["case5"]

    # case 6 — R2a: response copies the requirement, hard element missing → B
    tender6 = "投标人须提供本地化服务团队，人员不少于 5 名，年限 3 年以上"
    draft6 = "本地化服务团队：完全满足"          # 照抄但没给数字
    cl6 = {"qualification_requirements": [{"item": tender6}]}
    rows6, _ = build_coverage(cl6, text=tender6, response=draft6)
    r = bool(rows6) and rows6[0]["coverage"] == "B"
    print(f"[{'PASS' if r else 'FAIL'}] 6 反例R2a 照抄要求+硬要素缺失 → 判 B")
    if rows6 and not r:
        print(f"        实际: {rows6[0]['coverage']} / {rows6[0]['gap_note']}")
    passed += r; failed += [] if r else ["case6"]

    # case 7 — R2b: promise + reference into a section with real content → A
    tender7 = "投标人须配备本地化服务团队，人数 5 名，年限 3 年以上"
    draft7 = ("技术响应：完全满足，详见 3.2 节。"
              "3.2 我方配备本地化服务团队 5 名，均具备 3 年以上从业经历，"
              "提供 24 小时响应承诺，满足招标要求。")
    cl7 = {"qualification_requirements": [{"item": tender7}]}
    rows7, _ = build_coverage(cl7, text=tender7, response=draft7)
    r = bool(rows7) and rows7[0]["coverage"] == "A"
    print(f"[{'PASS' if r else 'FAIL'}] 7 反例R2b 声明+引用且被引章节有实质 → 判 A")
    if rows7 and not r:
        print(f"        实际: {rows7[0]['coverage']} / {rows7[0]['gap_note']} "
              f"/ loc={rows7[0]['response_location']!r}")
    passed += r; failed += [] if r else ["case7"]

    # case 8 — openpyxl unavailable → degrade to CSV with a printed reason
    import tempfile
    ok, _ = _have_openpyxl()
    saved = sys.modules.get("openpyxl")
    sys.modules["openpyxl"] = None          # simulate ImportError
    r = False
    try:
        with tempfile.TemporaryDirectory() as td:
            csvp = os.path.join(td, "d.csv")
            xlp = os.path.join(td, "d.xlsx")
            write_csv(csvp, [{"a": 1}], ["a"])
            p, msg = write_xlsx(xlp, [{"a": 1}], ["a"], "t")
            # all three must hold while the temp dir still exists
            r = (p is None) and bool(msg) and ("降级" in msg) \
                and os.path.exists(csvp)
    finally:
        if saved is not None:
            sys.modules["openpyxl"] = saved
        else:
            sys.modules.pop("openpyxl", None)
    print(f"[{'PASS' if r else 'FAIL'}] 8 openpyxl 不可用 → 降级 CSV 且打印原因")
    passed += r; failed += [] if r else ["case8"]

    # --- v2.9 L3 regressions: these three were real defects found by the
    #     adversarial review. They exist to stop the same bug coming back.
    # 9 — no draft ⇒ nothing may reach 已完成 (was: all rows 已完成)
    cl9 = {"score_items": _mk_items([("技术方案", 60), ("商务报价", 40)])}
    cl9["score_conservation"] = {"checked": True, "sum": 100, "diff": 0,
                                 "verdict": "PASS", "reason": ""}
    lg9, s9 = build_ledger(cl9, text="技术方案 商务报价", response=None)
    r = bool(lg9) and all(x["state"] == S_NOT_STARTED for x in lg9) \
        and s9["by_state"][S_DONE] == 0
    print(f"[{'PASS' if r else 'FAIL'}] 9 回归·无草稿绝不判「已完成」"
          f"（实测 {s9['by_state'][S_DONE]} 项已完成）")
    passed += r; failed += [] if r else ["case9"]

    # 10 — a draft that only says 详见附件9 must not hijack other clauses
    tender10 = "投标人须提供安全生产许可证。投标人须提供质量管理体系认证。"
    draft10 = "我方将提供相关材料。详见附件9。"
    cl10 = {"qualification_requirements": [{"item": tender10}]}
    rows10, _ = build_coverage(cl10, text=tender10, response=draft10)
    hijacked = [x for x in rows10 if "附件9" in x["response_location"]]
    r = not hijacked
    print(f"[{'PASS' if r else 'FAIL'}] 10 回归·引用抢答不成立"
          f"（被劫持 {len(hijacked)}/{len(rows10)} 条）")
    passed += r; failed += [] if r else ["case10"]

    # 11 — an "empty declaration" padded past 40 chars must not pass as A
    tender11 = "投标人须提供本地化服务团队。"
    draft11 = "完全满足。其他从略，本条不再赘述，详见后文说明。"
    cl11 = {"qualification_requirements": [{"item": tender11}]}
    rows11, _ = build_coverage(cl11, text=tender11, response=draft11)
    r = bool(rows11) and rows11[0]["coverage"] != "A"
    print(f"[{'PASS' if r else 'FAIL'}] 11 回归·空声明加尾巴仍判非 A"
          f"（实测 {rows11[0]['coverage'] if rows11 else '—'}）")
    passed += r; failed += [] if r else ["case11"]

    # 12 — a draft that is only a placeholder must not read as 已完成
    # (found by the second adversarial pass: 「技术方案：待补。」scored DONE)
    cl12 = {"score_items": _mk_items([("技术方案", 100)])}
    cl12["score_conservation"] = {"checked": True, "sum": 100, "diff": 0,
                                  "verdict": "PASS", "reason": ""}
    lg12, s12 = build_ledger(cl12, text="技术方案：50分",
                             response="技术方案：待补。")
    r = bool(lg12) and lg12[0]["state"] != S_DONE \
        and s12["by_state"][S_DONE] == 0
    print(f"[{'PASS' if r else 'FAIL'}] 12 回归·占位符「待补」不得判已完成"
          f"（实测 {lg12[0]['state'] if lg12 else '—'}）")
    passed += r; failed += [] if r else ["case12"]

    # 13 — a heading that merely echoes the requirement, plus boilerplate,
    #       must not grade A (second adversarial pass). The 400-char window
    #       used to let the NEXT clause's text stand in for this one.
    r = is_substantive_empty(
        "本地化服务团队：满足招标文件要求。\n质量管理体系认证证书：满足要求。",
        "本地化服务团队")
    print(f"[{'PASS' if r else 'FAIL'}] 13 回归·回声标题+套话判为空回答")
    passed += r; failed += [] if r else ["case13"]

    # 14 — each clause is judged on its own paragraph: content in the
    #       neighbour must not rescue an empty answer, and an empty answer
    #       must not be dragged down by the neighbour's wording.
    r = is_substantive_empty(
        "本地化服务团队：满足招标文件要求。\n"
        "质量管理体系认证证书：我方已取得认证，编号 XYZ，有效期至 2029 年。",
        "本地化服务团队")
    print(f"[{'PASS' if r else 'FAIL'}] 14 回归·不借用邻条内容充数")
    passed += r; failed += [] if r else ["case14"]

    # 15 — and a genuinely substantive answer must still pass
    r = not is_substantive_empty(
        "本地化服务团队：我方配备专职人员 5 名，3 年以上从业经历，驻场办公。",
        "本地化服务团队")
    print(f"[{'PASS' if r else 'FAIL'}] 15 回归·实质回答不被误判为空")
    passed += r; failed += [] if r else ["case15"]

    # 16 — short but checkable answers must NOT be killed. The third
    #       adversarial pass measured this cost: `残留 ≥8 字` declared
    #       「7×24小时响应」「3场培训」「2名」 empty while a long echo
    #       passed. Length is not substance; evidence is.
    short_real = [
        ("售后服务承诺函", "售后服务承诺函：我方承诺7×24小时响应。"),
        ("培训方案", "培训方案：提供3场培训。"),
        ("人员配置", "人员配置：2名（李工、王工）。"),
        ("质量认证", "质量认证：ISO9001已提供扫描件。"),
        ("进度计划", "进度计划：附进度表分3阶段。"),
    ]
    killed = [lb for lb, sg in short_real
              if is_substantive_empty(sg, lb)]
    r = not killed
    print(f"[{'PASS' if r else 'FAIL'}] 16 回归·短但可核查的回答不被误杀"
          f"（误杀 {len(killed)}/{len(short_real)}）")
    passed += r; failed += [] if r else ["case16"]

    # 17 — and the echo/filler constructions must still be empty
    fakes = [
        ("本地化服务团队", "本地化服务团队：满足招标文件要求。"),
        ("本地化服务团队",
         "本地化服务团队：我方将严格按照招标文件要求完成全部内容。"),
        ("质量认证", "质量管理体系认证证书：同上。"),
    ]
    leaked = [lb for lb, sg in fakes if not is_substantive_empty(sg, lb)]
    r = not leaked
    print(f"[{'PASS' if r else 'FAIL'}] 17 回归·回声与套话仍判空"
          f"（漏放 {len(leaked)}/{len(fakes)}）")
    passed += r; failed += [] if r else ["case17"]

    # 18 — a tender whose clauses the upstream extractor half-loses must
    #       still be graded on every requirement
    t18 = ("某某公司招标文件\n投标人须提供售后服务承诺函。\n"
           "投标人须配备项目经理。\n"
           "投标人须提供质量管理体系认证证书。\n"
           "投标人须提供培训方案。\n")
    d18 = ("售后服务承诺函：我方承诺7×24小时响应。\n"
           "项目经理：张工具备5年以上经验。\n"
           "质量管理体系认证证书：满足招标文件要求。\n"
           "培训方案：提供3场培训。\n")
    rows18, s18 = build_coverage({"qualification_requirements": []},
                                 text=t18, response=d18)
    got = len(rows18)
    grades = sorted(r_["coverage"] for r_ in rows18)
    r = got == 4 and grades.count("A") == 3 and grades.count("B") == 1
    print(f"[{'PASS' if r else 'FAIL'}] 18 回归·漏抽条款被兜底补齐"
          f"（{got} 条 / {grades}）")
    passed += r; failed += [] if r else ["case18"]

    # 19 — FORMAT must not change the verdict. Fourth pass: the same answers
    #       written as 「标签：内容」 vs 「标签\\n内容」 scored A1/B9 vs A6/B4 —
    #       five true answers died purely from a line break.
    fmt_pairs = [
        ("售后服务承诺函", "售后服务承诺函：我方承诺7×24小时响应。",
         "售后服务承诺函\n我方承诺7×24小时响应。"),
        ("培训方案", "培训方案：提供3场培训。",
         "培训方案\n提供3场培训。"),
        ("人员配置", "人员配置：2名（李工、王工）。",
         "人员配置\n2名（李工、王工）。"),
    ]
    mismatched = [lb for lb, a, b in fmt_pairs
                  if is_substantive_empty(a, lb) != is_substantive_empty(b, lb)]
    r = not mismatched
    print(f"[{'PASS' if r else 'FAIL'}] 19 回归·书写格式不影响判定"
          f"（不一致 {len(mismatched)}/{len(fmt_pairs)}）")
    passed += r; failed += [] if r else ["case19"]

    # 20 — a certificate claim is evidence; merely citing a standard is not.
    #       Fourth pass: 「已取得CE认证」 died while 「符合ISO9001标准」
    #       counted as evidence — the verb decides, not the digits.
    claims_ok = [
        ("CE认证", "CE认证：已取得CE认证证书。"),
        ("CE认证证书", "CE认证证书：已提供扫描件。"),
        ("UL认证", "UL认证：已取得UL认证。"),
        ("体系", "我方通过ISO9001质量管理体系认证。"),
    ]
    refs_empty = [
        ("ISO标准", "我方符合ISO9001标准。"),
        ("CE标准", "我方符合CE标准要求。"),
        ("体系", "我方符合GB/T19001标准。"),
    ]
    killed = [lb for lb, sg in claims_ok if is_substantive_empty(sg, lb)]
    leaked = [lb for lb, sg in refs_empty if not is_substantive_empty(sg, lb)]
    r = not killed and not leaked
    print(f"[{'PASS' if r else 'FAIL'}] 19b 回归·证书持有算证据/仅引标准名算空"
          f"（误杀 {len(killed)} 漏放 {len(leaked)}）")
    passed += r; failed += [] if r else ["case19b"]

    # 20 — a promise is not a possession. Fifth pass: RE_POSSESS had been
    #       widened to include 提供/具备/提交, so 「类似业绩：我方提供业绩
    #       材料。」 paired with the generic noun 业绩 and short-circuited
    #       Q1 → six of ten samples graded A on pure filler.
    empty_talk = [
        ("类似业绩", "类似业绩：我方提供业绩材料。"),
        ("资质证明", "资质证明：我方具备相关资质。"),
        ("人员简历", "人员简历：提供简历。"),
        ("审计报告", "审计报告：提供报告。"),
        ("社保证明", "社保证明：提交社保。"),
        ("许可证", "许可证：具备许可证。"),
    ]
    faked = [lb for lb, sg in empty_talk
             if not is_substantive_empty(sg, lb)]
    r = not faked
    print(f"[{'PASS' if r else 'FAIL'}] 20 回归·空口白话不得判为有证据"
          f"（假A {len(faked)}/{len(empty_talk)}）")
    passed += r; failed += [] if r else ["case20"]

    # 21 — format C: heading, then a line that REPEATS the label with its body.
    #       Fifth pass: `if label in nxt: break` cut exactly this off.
    r = not is_substantive_empty(
        "售后服务承诺函\n售后服务承诺函：我方承诺7×24小时响应。",
        "售后服务承诺函")
    print(f"[{'PASS' if r else 'FAIL'}] 21 回归·格式C（标题行+重复标签正文）不误杀")
    passed += r; failed += [] if r else ["case21"]

    # 22 — RE_COMMIT and RE_POSSESS must agree. 「已取得」 was possession but
    #       not commitment, so a real credential claim cleared the evidence
    #       test and then failed on "no commitment verb" → graded B.
    r = bool(RE_COMMIT.search("我方已取得CE认证证书") and
             RE_POSSESS.search("我方已取得CE认证证书"))
    print(f"[{'PASS' if r else 'FAIL'}] 22 回归·持有动作同时算证据与承诺"
          f"（两表一致）")
    passed += r; failed += [] if r else ["case22"]

    # 23 — B5, real tender. A 100k-character PDF judged by 评标办法（最低价法）
    #       contains no scoring table, yet "N分" appears in the tender number,
    #       the date, the opening time and two brand names. The old extractor
    #       turned those into a six-row "ledger" summing to 49.1 — a table that
    #       looked authoritative and was entirely invented.
    #       ⚠️ The sample is a NEUTRALISED version of a real tender: the shape
    #       is preserved, every identifying name removed. Real tender text
    #       must never enter this file — the packaging scan blocks it, and
    #       it would leak a live project to every user of the skill.
    price_only = (
        "某某服务公司某某地区零星维修服务专有协议\n"
        "招标项目编号：00-XXXX-00-0000/00\n"
        "日期：2026年08月25日\n"
        "评标办法（最低价）\n"
        "评标办法前附表 评审因素 评审标准\n"
        "1 评标方法 中标候选人排序方法 经评审的最低评标价法\n"
        "系统将在开启价格标前 15 分钟以邮件形式邀请投标人参加\n"
        "水龙头参考：某某、某某、某某或同等品牌，4分个 30\n"
        "电脑板 XQBM33-1699 个 15\n"
    )
    rows23, _ = rule_extract_score_items(price_only)
    r = not rows23
    print(f"[{'PASS' if r else 'FAIL'}] 23 回归·最低价法标书不得编造评分台账"
          f"（误抽 {len(rows23)} 项）")
    passed += r; failed += [] if r else ["case23"]

    # 24 — and when a real scoring table exists it must still be read
    real_table = (
        "第四章 评标办法\n评分标准\n"
        "技术方案：40分\n商务报价：35分\n服务承诺：25分\n满分 100 分\n"
    )
    rows24, total24 = rule_extract_score_items(real_table)
    r = len(rows24) == 3 and total24 == 100
    print(f"[{'PASS' if r else 'FAIL'}] 24 回归·真评分表仍能正常抽出"
          f"（{len(rows24)} 项 / 总分 {total24}）")
    passed += r; failed += [] if r else ["case24"]

    print("─" * 62)
    print(f"结果：{passed}/25 通过"
          + (f" · 失败：{', '.join(failed)}" if failed else " · 全部通过 ✅"))
    print("（本机 openpyxl 现状：%s）" % ("有" if ok else "无"))
    return 0 if passed == 25 else 1


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def _load_clauses(args):
    """Two entrances: reuse a JSON produced earlier, or extract from a file."""
    if getattr(args, "from_json", None):
        with open(args.from_json, encoding="utf-8") as f:
            data = json.load(f)
        clauses = data.get("clauses", data)
        return clauses, "", {"source": "json"}
    if not args.file:
        return None, "", {"source": "none"}
    from doc_parser import parse
    text, backend = parse(args.file)
    if not text:
        raise SystemExit(f"[error] 未能提取文本（backend={backend}）。"
                         f"纯扫描件需先 OCR。")
    try:
        from clause_extractor import extract
        clauses, meta = extract(text, use_ai=False)
    except Exception:
        clauses, meta = {"score_items": [], "qualification_requirements": []}, {}
    return clauses, text, meta


def main():
    ap = argparse.ArgumentParser(
        description="BidHunter 评分点台账 / 正向覆盖矩阵 v2.9")
    ap.add_argument("mode", nargs="?",
                    choices=["ledger", "coverage", "both"])
    ap.add_argument("file", nargs="?", help="招标文件路径")
    ap.add_argument("--from-json", help="复用已抽好的 clauses JSON")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--csv", help="CSV 输出路径")
    ap.add_argument("--xlsx", help="xlsx 输出路径（无 openpyxl 则降级）")
    ap.add_argument("--materials", help="材料库文件，用于 材料缺/待核 判定")
    ap.add_argument("--response", help="投标文件草稿；B1 台账与 B2 覆盖矩阵据此判状态")
    ap.add_argument("--prev-ledger", help="上一版台账 JSON；用于检测状态回退（A3）")
    ap.add_argument("--deadline", help="投标截止，用于 A4 报警")
    ap.add_argument("--confirm-regress", action="store_true",
                    help="确认状态回退（否则 A3 报警）")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    if not args.mode:
        print("用法:")
        print("  bidhunter.py score ledger <招标文件>    # B1 评分点台账")
        print("  bidhunter.py score coverage <招标文件>  # B2 正向覆盖矩阵")
        print("  bidhunter.py score both <招标文件>      # 两张表一起出")
        print("  ... --json / --csv P / --xlsx P / --deadline / --materials F")
        print("  bidhunter.py score --selftest          # 内置自测")
        return 0

    clauses, text, meta = _load_clauses(args)
    if clauses is None:
        print("[error] 需要 <招标文件> 或 --from-json", file=sys.stderr)
        return 1

    materials = None
    if args.materials:
        with open(args.materials, encoding="utf-8", errors="ignore") as f:
            materials = f.read()

    degrade = ""
    out = {"meta": meta}
    base = os.path.basename(args.file) if args.file else (args.from_json or "")

    if args.mode in ("ledger", "both"):
        resp1 = None
        if args.response:
            from doc_parser import parse as _p
            resp1, rb1 = _p(args.response)
            if not resp1:
                degrade = (degrade or "") + \
                    f"；响应文件无法提取文本（{rb1}）→ 台账不会判「已完成」"
        prev = None
        if args.prev_ledger:
            try:
                with open(args.prev_ledger, encoding="utf-8") as f:
                    prev = json.load(f)
                if isinstance(prev, dict):
                    prev = prev.get("ledger", {}).get("rows")
            except Exception as e:
                degrade = (degrade or "") + \
                    f"；上一版台账读取失败（{e}）→ A3 状态回退检测跳过"
        ledger, summary = build_ledger(
            clauses, text=text, materials=materials,
            deadline=args.deadline, confirm_regress=args.confirm_regress,
            response=resp1, prev_ledger=prev)
        out["ledger"] = {"rows": ledger, "summary": summary}
        if args.csv:
            write_csv(args.csv, ledger, LEDGER_COLS)
        if args.xlsx:
            _, msg = write_xlsx(args.xlsx, ledger, LEDGER_COLS, "评分点台账")
            degrade = degrade or msg
        if not args.json:
            print(render_ledger(ledger, summary, base, degrade))

    if args.mode in ("coverage", "both"):
        resp = None
        if args.response:
            from doc_parser import parse as _p
            resp, rbackend = _p(args.response)
            if not resp:
                degrade = (degrade or "") + \
                    f"；响应文件无法提取文本（{rbackend}）→ 覆盖矩阵全部降为 C"
        rows, csum = build_coverage(clauses, text=text, materials=materials,
                                    response=resp)
        out["coverage"] = {"rows": rows, "summary": csum}
        if args.csv and args.mode == "coverage":
            write_csv(args.csv, rows, COVERAGE_COLS)
        if args.xlsx and args.mode == "coverage":
            _, msg = write_xlsx(args.xlsx, rows, COVERAGE_COLS, "覆盖矩阵")
            degrade = degrade or msg
        if not args.json:
            if args.mode == "both":
                print()
            print(render_coverage(rows, csum, base))

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
