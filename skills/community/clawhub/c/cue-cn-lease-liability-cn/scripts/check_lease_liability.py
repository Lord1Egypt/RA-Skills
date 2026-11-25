#!/usr/bin/env python3
"""租赁负债与使用权资产登记稿·五道机检（续拍 C：五道已全部落字）。

用法:
    python3 check_lease_liability.py 我的租赁稿.md   # rc=0 全过｜1 有发条｜2 用法错｜3 读不到/空稿/仍有判据未落字
    python3 check_lease_liability.py --demo          # 打印一份六节齐的好样
    python3 check_lease_liability.py --selftest      # 逐档自测

退码 3 明确不等于合规：输出里会写「这不等于合规」。
"""
import re
import sys
from decimal import Decimal

SLUG = "cue-cn-lease-liability-cn"
CODES = ("LL-STRUCT", "LL-QUOTE", "LL-SPLIT", "LL-ASSET", "LL-LINE")
MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议")
SECTIONS = (
    "租赁负债",
    "使用权资产",
    "租赁期与折现率",
    "租赁变更与重估",
    "口径与未取到",
    "来源",
)
CONTENT_SECTIONS = SECTIONS[:4]

# 续拍 C：五道全落字，rc=3 只留给读不到、空稿与（万一的）未落字。
UNIMPLEMENTED = ()

REDLINES = (
    ("投资建议", ("买入", "卖出", "增持", "减持", "目标价", "推荐", "建议持有")),
    ("前瞻预测", ("预计", "预测", "有望", "将会", "看好", "预期增长", "预判")),
    ("主观评价", ("合理", "不合理", "偏高", "偏低", "高估", "低估", "显著偏低", "显著偏高")),
    ("越界口径", ("租赁融资成本高", "融资成本高", "财务风险", "资本结构优化", "杠杆空间",
                  "融资租赁更划算", "经营租赁优于")),
)

LINE_CLAUSE = re.compile(r"[；;。，,｜|]")

BRACKET = re.compile(r"〔[^〕]*〕")
QUOTE = re.compile(r"「[^」]*」")
ANCHOR = re.compile(r"〔\s*锚\s*[:：]")
CITE = re.compile(r"\[(S\d+)\]")
SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<title>.+?)\s*\|\s*(?P<url>https?://\S+)\s*\|\s*"
    r"检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _is_finding_line(s):
    return s.startswith("- ") or s == "-"


def _is_exempt_line(s):
    return "未取到" in s or "[待人工]" in s or "〔自算〕" in s


def _own_part(s):
    i = s.find("「")
    return s if i < 0 else s[:i]


def section_map(text):
    """→ ({节名: [(行号, 行)]}（dict 保文档出现序）, [野节／重复节说明])。

    重复节与认不出的节标题一样进 stray，且**其后正文不并入前一节**（cur = None）。
    不这么做的话，第二个同名节的正文会被偷偷并进第一次那个节，节序与缺口两向都看不出来。
    """
    out, stray, cur = {}, [], None
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            name = line[3:].strip()
            if name in SECTIONS:
                if name in out:
                    stray.append(f"重复节：{name}（第 {lineno} 行）")
                    cur = None
                else:
                    out[name] = []
                    cur = name
            else:
                stray.append(f"认不出的节标题：{name}（第 {lineno} 行）")
                cur = None
            continue
        if cur is not None:
            out[cur].append((lineno, line))
    return out, stray


def check_struct(text):
    """道一 LL-STRUCT：头部三件自标、六节齐且按序、野节／重复节。只判形，不判内容。"""
    out = []
    lines = text.splitlines()
    head = "\n".join(lines[:12])
    for mark in MARK_TEXTS:
        if mark not in head:
            out.append(f"LL-STRUCT L1 头部缺自标「{mark}」")
    secs, stray = section_map(text)
    # 取序的来源是**文档里的实际出现顺序**（secs 是 dict，3.7+ 保插入序），不是 SECTIONS。
    # 写成 `[s for s in SECTIONS if s in secs]` 会让 order 恒等于规范序，节序判据永远为假。
    order = [s for s in secs if s in SECTIONS]
    if order != list(SECTIONS):
        missing = [s for s in SECTIONS if s not in secs]
        if missing:
            out.append("LL-STRUCT L1 缺节：" + "、".join(missing))
        else:
            out.append("LL-STRUCT L1 节序错：" + " → ".join(order))
    for s in stray:
        out.append(f"LL-STRUCT L1 认不出的节标题／重复节：{s}")
    return out


def check_quote(text):
    """道二 LL-QUOTE：带数字的行须挂齐「」原句＋〔锚〕＋[S#]；来源与正文两向对上。

    只认形，不核对引号里的数与行首的数是否同一——那是 LL-SPLIT／LL-ASSET 的活。
    """
    out = []
    secs, _stray = section_map(text)

    for name in CONTENT_SECTIONS:
        for lineno, raw in secs.get(name, []):
            s = raw.strip()
            if not _is_finding_line(s) or _is_exempt_line(s):
                continue
            own = BRACKET.sub("", _own_part(s))
            if not re.search(r"[0-9]", own):
                continue
            lacks = []
            if not QUOTE.search(s):
                lacks.append("「原句」")
            if not ANCHOR.search(s):
                lacks.append("〔锚：…〕")
            if not CITE.search(s):
                lacks.append("[S#]")
            if lacks:
                out.append("LL-QUOTE L%d 带数字的行缺 %s：%s"
                           % (lineno, "＋".join(lacks), s[:48]))

    cited = set()
    for name in CONTENT_SECTIONS:
        for _ln, raw in secs.get(name, []):
            cited |= set(CITE.findall(raw))

    declared = {}
    for lineno, raw in secs.get("来源", []):
        s = raw.strip()
        if not s.startswith("-"):
            continue
        sm = re.search(r"\[(S\d+)\]", s)
        if not sm:
            out.append("LL-QUOTE L%d 来源行没有 [S#] 编号：%s" % (lineno, s[:48]))
            continue
        # 先登记编号、再验形态：否则「检索日格式错」会让这条 [S#] 被判成「没登记」，
        # 一条缺陷冒充两条。
        declared.setdefault(sm.group(1), lineno)
        if SOURCE_LINE.match(s):
            continue
        d = re.search(r"检索日\s*(\S+)", s)
        if d and not DATE.match(d.group(1)):
            out.append("LL-QUOTE L%d [%s] 检索日不是 YYYY-MM-DD：%s"
                       % (lineno, sm.group(1), d.group(1)))
        else:
            out.append("LL-QUOTE L%d 来源行不合「- [S#] 标题 | URL | 检索日 YYYY-MM-DD」：%s"
                       % (lineno, s[:48]))

    for s_id in sorted(cited - set(declared)):
        out.append("LL-QUOTE L1 正文引用了来源里没有的 [%s]" % s_id)
    for s_id, lineno in sorted(declared.items(), key=lambda kv: kv[1]):
        if s_id not in cited:
            out.append("LL-QUOTE L%d 来源登记了 [%s] 但正文未引用" % (lineno, s_id))
    return out


TOL = Decimal("0.01")
NUM_RE = re.compile(r"([0-9][0-9,]*(?:\.[0-9]+)?)\s*(万元|%)")
MISSING = object()   # 该行已写「未取到」⇒ 已声明的缺口：不报缺失、整条静默跳过
NO_NUM = object()    # 行在、但行首那段取不到「万元」数（如单位写成「元」）：不是「缺项」，是取不到数


def _num_in_section(text, section, label):
    """在该节里找含 label 的项行，取行内第一个「万元／%」数（登记值）。

    只取原句（「」）之前那一段——原句里的数字是原文引用，不是登记值。
    返回 Decimal；该行已写「未取到」→ MISSING（缺口已在口径节声明，静默跳过、不重复计缺陷）；
    行在但取不到「万元」数 → NO_NUM（与「行不存在」分开，措辞不能混成「缺项」）；
    找不到该行 → None。
    """
    secs, _ = section_map(text)
    saw_line = False
    for _ln, raw in secs.get(section, []):
        s = raw.strip()
        if not s.startswith("-") or label not in s:
            continue
        head = s.split("「")[0]
        if "未取到" in head:
            return MISSING
        saw_line = True
        m = NUM_RE.search(head)
        if m:
            return Decimal(m.group(1).replace(",", ""))
    return NO_NUM if saw_line else None


def _missing_msgs(code, section, names, vals, role):
    """把「行不存在」与「行在但取不到万元金额」两类分开成消息。"""
    out = []
    for n, v in zip(names, vals):
        if v is None:
            out.append("%s %s节缺「%s」，%s（整条跳过，不按 0 算）" % (code, section, n, role.get(n, "无从复核")))
        elif v is NO_NUM:
            out.append("%s %s节「%s」行取不到万元金额（数没写成「N 万元」，整条跳过，不按 0 算）"
                       % (code, section, n))
    return out


def check_split(text):
    """道三 LL-SPLIT：三个到期分档之和 vs 未折现租赁付款额合计。已声明缺口整条跳过。"""
    out = []
    names = ("一年内到期", "一到三年到期", "三年以上到期", "未折现租赁付款额合计")
    vals = [_num_in_section(text, "租赁负债", n) for n in names]
    if any(v is MISSING for v in vals):
        return out
    bad = _missing_msgs("LL-SPLIT", "租赁负债", names, vals, {
        "未折现租赁付款额合计": "无对照",
    })
    if bad:
        return out + bad
    tiers, total = vals[:3], vals[3]
    s = tiers[0] + tiers[1] + tiers[2]
    if (s - total).copy_abs() > TOL:
        out.append("LL-SPLIT 一年内到期 %.2f + 一到三年到期 %.2f + 三年以上到期 %.2f = %.2f "
                   "≠ 未折现租赁付款额合计 %.2f（差 %.2f）"
                   % (tiers[0], tiers[1], tiers[2], s, total, s - total))
    return out


def check_asset(text):
    """道四 LL-ASSET：原值 − 累计折旧 − 减值准备 vs 账面价值。已声明缺口整条跳过。"""
    out = []
    names = ("使用权资产原值", "使用权资产累计折旧", "使用权资产减值准备", "使用权资产账面价值")
    vals = [_num_in_section(text, "使用权资产", n) for n in names]
    if any(v is MISSING for v in vals):
        return out
    bad = _missing_msgs("LL-ASSET", "使用权资产", names, vals, {
        "使用权资产原值": "减法那一层无从复核",
        "使用权资产累计折旧": "减法那一层无从复核",
        "使用权资产减值准备": "减法那一层无从复核",
        "使用权资产账面价值": "勾稽无对照",
    })
    if bad:
        return out + bad
    orig, dep, imp, book = vals
    calc = orig - dep - imp
    if (calc - book).copy_abs() > TOL:
        out.append("LL-ASSET 原值 %.2f − 累计折旧 %.2f − 减值准备 %.2f = %.2f "
                   "≠ 账面价值 %.2f（差 %.2f）"
                   % (orig, dep, imp, calc, book, calc - book))
    return out


def check_line(text):
    """道五 LL-LINE：四组越界词，只扫四个内容节（口径与未取到／来源两节整节豁免）。

    「」引文与〔…〕标签槽（口径／锚／自算）都不是本件断言——先洗掉再判：照抄附注的
    「预计」、锚指向的「预计负债」那个科目名，都是出处与标签，不是本件下的判断。
    再按分句判，含 [待人工] 或 未取到 的那一句跳过，同句后半段照样判。
    同组命中只报不被别的命中词包含的那些。
    """
    out = []
    secs, _stray = section_map(text)
    for name in CONTENT_SECTIONS:
        for lineno, raw in secs.get(name, []):
            s = raw.strip()
            if not _is_finding_line(s):
                continue
            own = BRACKET.sub("", QUOTE.sub("", s))   # 洗掉引文与标签槽
            for clause in LINE_CLAUSE.split(own):
                if "[待人工]" in clause or "未取到" in clause:
                    continue
                for group, words in REDLINES:
                    got = [w for w in words if w in clause]
                    if not got:
                        continue
                    kept = [w for w in got if not any(w != o and w in o for o in got)]
                    out.append("LL-LINE L%d 红线〔%s〕命中「%s」：%s"
                               % (lineno, group, "、".join(kept), clause.strip()[:44]))
    return out


CHECKS = {
    "LL-STRUCT": check_struct,
    "LL-QUOTE": check_quote,
    "LL-SPLIT": check_split,
    "LL-ASSET": check_asset,
    "LL-LINE": check_line,
}

DEMO = """# 示例材料（600000.SH）租赁登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议
主体：示例材料（600000.SH）
报告期：2025 年年度报告·附注·租赁

## 租赁负债

- 租赁负债一年内到期〔口径：本期末〕1,200.00 万元「一年内到期的租赁负债为人民币 1,200.00 万元」〔锚：2025 年年报·第 213 页·租赁〕[S1]
- 租赁负债一到三年到期〔口径：本期末〕2,400.00 万元「一到三年内到期的租赁负债为人民币 2,400.00 万元」〔锚：2025 年年报·第 213 页·租赁〕[S1]
- 租赁负债三年以上到期〔口径：本期末〕3,600.00 万元「三年以上到期的租赁负债为人民币 3,600.00 万元」〔锚：2025 年年报·第 213 页·租赁〕[S1]
- 未折现租赁付款额合计〔口径：本期末〕7,200.00 万元「未折现的租赁付款额合计为人民币 7,200.00 万元」〔锚：2025 年年报·第 213 页·租赁〕[S1]
- 租赁负债账面余额〔口径：本期末〕6,900.00 万元「租赁负债账面余额为人民币 6,900.00 万元」〔锚：2025 年年报·第 213 页·租赁〕[S1]

## 使用权资产

- 使用权资产原值〔口径：本期末〕8,000.00 万元「使用权资产原值为人民币 8,000.00 万元」〔锚：2025 年年报·第 213 页·租赁〕[S1]
- 使用权资产累计折旧〔口径：本期末〕2,400.00 万元「使用权资产累计折旧为人民币 2,400.00 万元」〔锚：2025 年年报·第 213 页·租赁〕[S1]
- 使用权资产减值准备〔口径：本期末〕0.00 万元「使用权资产减值准备为零」〔锚：2025 年年报·第 213 页·租赁〕[S1]
- 使用权资产账面价值〔口径：本期末〕5,600.00 万元「使用权资产账面价值为人民币 5,600.00 万元」〔锚：2025 年年报·第 213 页·租赁〕[S1]

## 租赁期与折现率

- 租赁期〔口径：本期〕5 年「本集团租入资产的租赁期主要为 5 年」〔锚：2025 年年报·第 213 页·租赁〕[S1]
- 增量借款利率〔口径：本期〕4.75%「折现采用的增量借款利率为 4.75%」〔锚：2025 年年报·第 213 页·租赁〕[S1]
- 短期租赁与低价值资产租赁简化处理〔口径：本期〕[待人工]
- 租赁付款额〔口径：本期发生额〕1,440.00 万元「本期租赁付款额为人民币 1,440.00 万元」〔锚：2025 年年报·第 213 页·租赁〕[S1]

## 租赁变更与重估

- 本期新增使用权资产〔口径：本期发生额〕900.00 万元「本期新增使用权资产人民币 900.00 万元」〔锚：2025 年年报·第 213 页·租赁〕[S1]
- 租赁变更影响〔口径：本期发生额〕150.00 万元「因租赁变更调增使用权资产人民币 150.00 万元」〔锚：2025 年年报·第 213 页·租赁〕[S1]
- 租赁期重估影响〔口径：本期发生额〕[待人工]

## 口径与未取到

- 未取到：无
- 口径：租赁负债按到期日分档逐行登记，分档一律取未折现的租赁付款额；使用权资产按原值、累计折旧、减值准备、账面价值四行登记。
  本件不评价租赁融资安排是否划算，也不预测以后期间租金。

## 来源

- [S1] 示例材料 2025 年年度报告·附注·租赁 | https://example.invalid/600000_2025_notes.pdf | 检索日 2025-04-20
"""


def run(text):
    findings = []
    unjudged = []
    for code in CODES:
        fn = CHECKS[code]
        if fn is None or code in UNIMPLEMENTED:
            unjudged.append(code)
            continue
        findings.extend(fn(text))
    return findings, unjudged


def main(argv):
    if len(argv) < 2:
        print("用法: check_lease_liability.py <稿.md> | --demo | --selftest")
        return 2
    arg = argv[1]
    if arg == "--demo":
        sys.stdout.write(DEMO)
        return 0
    if arg == "--selftest":
        return selftest()
    if arg.startswith("--"):
        print(f"未知参数：{arg}")
        return 2
    try:
        text = open(arg, encoding="utf-8").read()
    except OSError as e:
        print(f"读不到文件：{arg}（{e}）")
        return 3
    if not text.strip():
        print("空稿：不判，也不等于合规")
        return 3
    findings, unjudged = run(text)
    for f in findings:
        print(f)
    if findings:
        print(f"—— 机检：{len(findings)} 条发条｜不可判 {len(unjudged)} 道")
        return 1
    if unjudged:
        print(f"—— 机检：0 条发条，但 {len(unjudged)} 道判据未落字（{'、'.join(unjudged)}）"
              f"——这不等于合规")
        return 3
    print("—— 机检：五道全过，0 条发条")
    return 0


# 乱序回归档用的底稿：从好样里**摘掉整个「来源」节**（该节跑在文末，是最后一段）。
_NO_SOURCE = DEMO[:DEMO.index("## 来源")]
assert _NO_SOURCE != DEMO and "## 来源" not in _NO_SOURCE, "乱序档底稿没摘掉来源节"

CASES = (
    ("好样应零发条（五道全落字）", DEMO, 0),
    ("头部删掉「不构成投资建议」", DEMO.replace(" ｜ 不构成投资建议", "", 1), 1),
    ("删掉「使用权资产」整节", re.sub(r"## 使用权资产\n(.*?)(?=\n## )", "", DEMO, flags=re.S), 1),
    ("「来源」节写了两次（重复节记 stray）", DEMO + "\n## 来源\n\n- [S2] 重复登记的一份\n", 1),
    # 乱序回归档：六节都在、只把「来源」挪到「租赁变更与重估」之前。旧实现
    # `order = [s for s in SECTIONS if s in secs]` 让 order 恒等于规范序，这一档永远不红——
    # 本档就是那条死判据的护栏，不许删。分两步：先摘掉原「来源」节，再插到「租赁变更与重估」前。
    ("把「来源」整节挪到「租赁变更与重估」之前（六节齐，只错序）",
     _NO_SOURCE.replace(
         "## 租赁变更与重估\n",
         "## 来源\n\n- [S1] 示例材料 2025 年年度报告·附注·租赁 | "
         "https://example.invalid/600000_2025_notes.pdf | 检索日 2025-04-20\n\n## 租赁变更与重估\n", 1,
     ), 1),
    # 以下四档是 LL-QUOTE 的正反例（本拍新增）。
    ("LL-QUOTE：数字行丢了原句与锚（三元组缺两件）",
     DEMO.replace(
         "- 租赁负债一年内到期〔口径：本期末〕1,200.00 万元「一年内到期的租赁负债为人民币 1,200.00 万元」"
         "〔锚：2025 年年报·第 213 页·租赁〕[S1]",
         "- 租赁负债一年内到期〔口径：本期末〕1,200.00 万元", 1),
     1),
    ("LL-QUOTE：来源行检索日写成 2025/04/20（斜杠式）",
     DEMO.replace("检索日 2025-04-20", "检索日 2025/04/20", 1), 1),
    ("LL-QUOTE：正文引了未登记的 [S9]",
     DEMO.replace("[S1]", "[S9]", 1), 1),
    # 护栏：[待人工] 行整体豁免，引文里的数字不触发三元组要求。
    # 不许为了上面三档变红而把 [待人工] 的豁免写死——那会让本该豁免的行重被判红。
    ("LL-QUOTE 反证：引文里带数字不算本件断言（[待人工] 行豁免）⇒ 零发条",
     DEMO.replace(
         "- 短期租赁与低价值资产租赁简化处理〔口径：本期〕[待人工]",
         "- 短期租赁与低价值资产租赁简化处理〔口径：本期〕[待人工]（原文写「低于 5 万元的按简化处理」）", 1),
     0),
    # 续拍 B：两道勾稽。DEMO 的数字本来就自洽（1,200+2,400+3,600=7,200；8,000−2,400−0=5,600），
    # 接上判据后好样仍须零发条——若变红，说明取数取错了。
    ("B2 分档：三年以上到期 3,600.00 → 3,900.00 ⇒ 只发 LL-SPLIT",
     DEMO.replace("3,600.00 万元", "3,900.00 万元", 1), 1),
    ("B3 勾稽：累计折旧 2,400.00 → 2,000.00 ⇒ 只发 LL-ASSET",
     DEMO.replace(
         "- 使用权资产累计折旧〔口径：本期末〕2,400.00 万元",
         "- 使用权资产累计折旧〔口径：本期末〕2,000.00 万元", 1),
     1),
    # 缺口反证（护栏）：某格写成「未取到」且口径节已声明 ⇒ 整条静默跳过、零发条。
    # 不许为了让 B2／B3 变红而把「已声明缺口」也报成缺失——那会把合规稿判红。
    ("B4 缺口反证：三年以上到期写「未取到」且口径节已声明 ⇒ 零发条（静默跳过）",
     DEMO.replace(
         "- 租赁负债三年以上到期〔口径：本期末〕3,600.00 万元「三年以上到期的租赁负债为人民币 3,600.00 万元」"
         "〔锚：2025 年年报·第 213 页·租赁〕[S1]",
         "- 未取到：三年以上到期", 1).replace(
         "- 未取到：无", "- 未取到：三年以上到期", 1),
     0),
    ("B5 勾稽：删掉「使用权资产减值准备」整行 ⇒ 发 LL-ASSET 并点名缺项",
     re.sub(r"- 使用权资产减值准备[^\n]*\n", "", DEMO),
     1),
    # 续拍 C：红线。四组词只扫四个内容节；引文与〔…〕标签槽先洗掉（照抄附注不算本件断言）；
    # [待人工] 与 未取到 只豁免自己那一句。这几档缺了，LL-LINE 等于没被尺子量过。
    ("C1 红线：正文写「租赁融资成本偏高」⇒ 发 LL-LINE（两道勾稽的数没动，不该跟着红）",
     DEMO.replace(
         "- 增量借款利率〔口径：本期〕4.75%",
         "- 增量借款利率 租赁融资成本偏高〔口径：本期〕4.75%", 1),
     1),
    # 反证档：引文里照抄附注的「预计」不是本件断言。
    ("C2 红线反证：引文里照抄的「预计」⇒ 零发条",
     DEMO.replace(
         "「本期新增使用权资产人民币 900.00 万元」",
         "「公司预计本期新增使用权资产人民币 900.00 万元」", 1),
     0),
    # 反证档：〔锚：…预计负债…〕指向的是附注科目名，不是本件判断。
    ("C3 红线反证：锚指向「预计负债」科目名 ⇒ 零发条",
     DEMO.replace("第 213 页·租赁", "第 213 页·预计负债", 1),
     0),
    # 反证档：[待人工] 那一句整体豁免（判断位不是断言），同句后半段仍照样判。
    ("C4 红线反证：[待人工] 行里写评价词 ⇒ 零发条",
     DEMO.replace(
         "- 租赁期重估影响〔口径：本期发生额〕[待人工]",
         "- 租赁期重估影响 是否偏高〔口径：本期发生额〕[待人工]", 1),
     0),
    # 反证档：「口径与未取到」整节豁免（口径声明不是断言）。
    ("C5 红线反证：口径与未取到节里写「预计」⇒ 零发条（整节豁免）",
     DEMO.replace(
         "  本件不评价租赁融资安排是否划算，也不预测以后期间租金。",
         "  本件不评价租赁融资安排是否划算，也不预测以后期间租金；下年预计无新增。", 1),
     0),
)


def selftest():
    bad = 0
    for name, text, want in CASES:
        findings, unjudged = run(text)
        if want == 0:
            ok = (not findings)
        else:
            ok = bool(findings)
        got = "发条 %d 条：%s" % (len(findings), "；".join(findings) or "无")
        print(("过   " if ok else "不合 ") + name + f"（{got}）")
        if not ok:
            bad += 1
    # 单稿退码自证：好样在仍有未落字时应 rc=3
    findings, unjudged = run(DEMO)
    import tempfile, os
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
        f.write(DEMO)
        p = f.name
    try:
        rc = main(["x", p])
    finally:
        os.unlink(p)
    want_rc = 3 if unjudged else 0
    ok = (rc == want_rc)
    print(("过   " if ok else "不合 ") + f"单稿退码自证（好样 rc={rc}，期望 {want_rc}，未落字 {len(unjudged)} 道）")
    if not ok:
        bad += 1
    print("——")
    print(f"自测档数={len(CASES) + 1}｜不合={bad}｜不可判={len(unjudged)}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
