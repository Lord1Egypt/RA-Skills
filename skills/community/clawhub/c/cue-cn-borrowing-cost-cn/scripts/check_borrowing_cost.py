#!/usr/bin/env python3
"""借款费用资本化登记稿·五道机检（续拍 D：五道已全部落字）。

用法:
    python3 check_borrowing_cost.py 我的登记稿.md   # rc=0 全过｜1 有发条｜2 用法错｜3 读不到/空稿/仍有判据未落字
    python3 check_borrowing_cost.py --demo          # 打印一份六节齐的好样
    python3 check_borrowing_cost.py --selftest      # 逐档自测

退码 3 明确不等于合规：输出里会写「这不等于合规」。
"""
import re
import sys
from decimal import Decimal

SLUG = "cue-cn-borrowing-cost-cn"
CODES = ("BC-STRUCT", "BC-QUOTE", "BC-CAP", "BC-SPLIT", "BC-LINE")
MARK_TEXTS = ("AI 整理初稿", "请回原文核对", "不构成投资建议")
SECTIONS = (
    "借款费用概况",
    "专门借款",
    "一般借款",
    "资本化期间与暂停",
    "口径与未取到",
    "来源",
)
CONTENT_SECTIONS = SECTIONS[:4]

REDLINES = (
    ("投资建议", ("买入", "卖出", "增持", "减持", "目标价", "推荐", "建议持有")),
    ("前瞻预测", ("预计", "预测", "有望", "将会", "看好", "预期增长", "预判")),
    ("主观评价", ("合理", "不合理", "偏高", "偏低", "高估", "低估", "显著偏低", "显著偏高")),
    ("越界口径", ("利润调节", "盈余管理", "调节利润", "税务筹划", "避税",
                  "融资成本高", "财务风险", "资本结构优化", "杠杆空间")),
)

# 续拍 D：五道全落字，rc=3 只留给读不到与空稿。
UNIMPLEMENTED = ()

NUM_LINE = re.compile(r"^\s*-\s*(?P<name>[^〔「]+?)\s*〔")

BRACKET = re.compile(r"〔[^〕]*〕")
QUOTE = re.compile(r"「[^」]*」")
ANCHOR = re.compile(r"〔\s*锚\s*[:：]")
CITE = re.compile(r"\[(S\d+)\]")
SOURCE_LINE = re.compile(
    r"^-\s*\[(?P<s>S\d+)\]\s*(?P<title>.+?)\s*\|\s*(?P<url>https?://\S+)\s*\|\s*"
    r"检索日\s*(?P<d>\d{4}-\d{2}-\d{2})\s*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _gap_names(text):
    """→ 「口径与未取到」节里**真声明**的缺项名清单。

    口径节里常见 `- 未取到：无`——意思是「什么都不缺」。所以不能只判 '未取到' 在不在，
    必须看冒号后那一段：非空且不是 无/無/None/none/—/-/– 才算真声明了缺项。
    """
    m = re.search(r"##\s*口径与未取到\s*\n(.*?)(?:\n##\s|\Z)", text, re.S)
    if not m:
        return []
    names = []
    for line in m.group(1).splitlines():
        s = line.strip()
        if not s.startswith("-"):
            continue
        s = s.lstrip("-").strip()
        names.extend(_gap_names_in_line(s))
    return names


def _gap_names_in_line(s):
    """从一行取出「未取到」之后声明的缺口名清单。

    「未取到」可在行首，也可在项名/金额之后（SKILL.md 第 77 行的合法写法）。
    取它出现位置冒号后那一段，按分隔符拆；没有「未取到」返回 []。
    裸「未取到」（无冒号无名）退回用行首项名（第一个 〔/[ 之前那段）。
    """
    _T, _EMPTY = "未取到", ("无", "無", "None", "none", "—", "-", "–")
    pos = s.find(_T)
    if pos < 0:
        return []
    tail = s[pos + len(_T):]
    stripped = tail.lstrip("：: 　 ")
    if stripped != tail:
        seg = stripped
    else:
        name = re.split(r"[〔\[「]", s.lstrip("-").strip(), 1)[0].strip()
        return [name] if name and name not in _EMPTY else []
    seg = seg.split("〔")[0].split("[")[0].split("「")[0].strip().rstrip("。，,；;")
    if not seg or seg in _EMPTY:
        return []
    return [t.strip() for t in re.split(r"[、，,／/；;]", seg) if t.strip()]


def _gap_declared(text, name):
    """判「口径与未取到」节是否已声明缺 name（子串语义，供后续两分／恒等两道复用）。"""
    return any(name in n for n in _gap_names(text))


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
    out = []
    lines = text.splitlines()
    head = "\n".join(lines[:12])
    for mark in MARK_TEXTS:
        if mark not in head:
            out.append(f"BC-STRUCT L1 头部缺自标「{mark}」")
    secs, stray = section_map(text)
    # 取序的来源是**文档里的实际出现顺序**（secs 是 dict，3.7+ 保插入序），不是 SECTIONS。
    # 写成 `[s for s in SECTIONS if s in secs]` 会让 order 恒等于规范序——六节齐时那一判永远为假，
    # 「节序错」结构上不可能发条（原型里就是这么死的，实测挪「来源」节零发条）。
    order = [s for s in secs if s in SECTIONS]
    if order != list(SECTIONS):
        missing = [s for s in SECTIONS if s not in secs]
        if missing:
            out.append("BC-STRUCT L1 缺节：" + "、".join(missing))
        else:
            out.append("BC-STRUCT L1 节序错：" + " → ".join(order))
    for s in stray:
        out.append(f"BC-STRUCT L1 认不出的节标题／重复节：{s}")
    return out


def _is_finding_line(s):
    return s.startswith("- ") or s == "-"


def _is_exempt_line(s):
    """按设计不带三元组的三形：`未取到：`／`[待人工]`／`〔自算〕`。"""
    return "未取到" in s or "[待人工]" in s or "〔自算〕" in s


def _own_part(s):
    """行内「原句」之前的那一段（行首标签＋口径＋金额）。"""
    i = s.find("「")
    return s if i < 0 else s[:i]


def check_quote(text):
    """道二 BC-QUOTE：带数字的行须挂齐「」原句＋〔锚〕＋[S#]；来源与正文两向对上。

    只认形，不核对引号里的数与行首的数是否同一——那是 BC-CAP／BC-SPLIT 的活。
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
                out.append("BC-QUOTE L%d 带数字的行缺 %s：%s"
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
            out.append("BC-QUOTE L%d 来源行没有 [S#] 编号：%s" % (lineno, s[:48]))
            continue
        # 先登记编号、再验形态：否则「检索日格式错」会让这条 [S#] 被判成「没登记」，
        # 于是一条缺陷冒充两条，第二条「正文引用了来源里没有的 [S#]」还是不实的。
        declared.setdefault(sm.group(1), lineno)
        if SOURCE_LINE.match(s):
            continue
        d = re.search(r"检索日\s*(\S+)", s)
        if d and not DATE.match(d.group(1)):
            out.append("BC-QUOTE L%d [%s] 检索日不是 YYYY-MM-DD：%s"
                       % (lineno, sm.group(1), d.group(1)))
        else:
            out.append("BC-QUOTE L%d 来源行不合「- [S#] 标题 | URL | 检索日 YYYY-MM-DD」：%s"
                       % (lineno, s[:48]))

    for s_id in sorted(cited - set(declared)):
        out.append("BC-QUOTE L1 正文引用了来源里没有的 [%s]" % s_id)
    for s_id, lineno in sorted(declared.items(), key=lambda kv: kv[1]):
        if s_id not in cited:
            out.append("BC-QUOTE L%d 来源登记了 [%s] 但正文未引用" % (lineno, s_id))
    return out


def check_gap(text):
    """BC-QUOTE 的第二半：正文「未取到：X」与口径节的声明两向对账。

    `- 未取到：无` 是「什么都不缺」，不算声明了任何缺项——这一条由 `_gap_names` 保证。
    这里复用同一份解析，不另写一套（同一事实两处真值＝迟早对不上）。
    """
    out = []
    secs, _stray = section_map(text)
    declared = _gap_names(text)

    mentioned = []
    for name in CONTENT_SECTIONS:
        for lineno, raw in secs.get(name, []):
            s = raw.strip()
            if not s.startswith("-") or "未取到" not in s:
                continue
            for tok in _gap_names_in_line(s):
                mentioned.append((lineno, tok))

    for lineno, tok in mentioned:
        if not _gap_declared(text, tok):
            out.append("BC-QUOTE L%d 正文写了「未取到：%s」但口径与未取到节没声明"
                       % (lineno, tok))
    for n in declared:
        if not any(n in tok or tok in n for _ln, tok in mentioned):
            out.append("BC-QUOTE L1 口径与未取到节声明了「%s」但正文没有这处缺口" % n)
    return out


def check_bc_quote(text):
    """BC-QUOTE 整道：三元组＋来源形制＋正反两向，外加缺口两向对账。"""
    return check_quote(text) + check_gap(text)


BC_SPLIT_TOL = Decimal("0.01")
BC_NUM_RE = re.compile(r"([-+]?\d[\d,]*\.?\d*)\s*(万元|%)")
MISSING = object()   # 该行已写「未取到」⇒ 已声明的缺口：不报缺失、静默跳过


def _num_in_section(text, section, label):
    """在该节里找含 label 的项行，取行内第一个「万元／%」数。

    只取原句（「」）之前那一段——原句里的数字是原文引用，不是登记值。
    返回 Decimal；行不存在返回 None；该行已写「未取到」返回 MISSING。
    """
    secs, _ = section_map(text)
    for _ln, raw in secs.get(section, []):
        s = raw.strip()
        if not s.startswith("-") or label not in s:
            continue
        head = s.split("「")[0]
        if "未取到" in head:
            return MISSING
        m = BC_NUM_RE.search(head)
        if m:
            raw_num, unit = m.group(1), m.group(2)
            return Decimal(raw_num) if unit == "%" else Decimal(raw_num.replace(",", ""))
    return None


def check_split(text):
    out = []
    total = _num_in_section(text, "借款费用概况", "利息支出合计")
    cap = _num_in_section(text, "借款费用概况", "其中资本化")
    exp = _num_in_section(text, "借款费用概况", "其中费用化")
    if any(v is MISSING for v in (total, cap, exp)):
        return out
    if cap is None or exp is None:
        out.append("BC-SPLIT 概况节需「其中资本化」与「其中费用化」两侧都登记，缺一侧不算")
        return out
    if total is None:
        out.append("BC-SPLIT 概况节缺「利息支出合计」，两分无从复核")
        return out
    if (cap + exp - total).copy_abs() > BC_SPLIT_TOL:
        out.append("BC-SPLIT 其中资本化 %.2f + 其中费用化 %.2f = %.2f ≠ 利息支出合计 %.2f（差 %.2f）"
                   % (cap, exp, cap + exp, total, cap + exp - total))
    return out


def check_cap(text):
    out = []
    disclosed = _num_in_section(text, "借款费用概况", "其中资本化")
    if disclosed is MISSING:
        return out
    if disclosed is None:
        out.append("BC-CAP 概况节缺「其中资本化」，恒等无对照")
        return out
    sp_int = _num_in_section(text, "专门借款", "专门借款利息")
    sp_idle = _num_in_section(text, "专门借款", "闲置资金收益")
    gb_occ = _num_in_section(text, "一般借款", "加权平均占用额")
    gb_rate = _num_in_section(text, "一般借款", "资本化率")
    if any(v is MISSING for v in (sp_int, sp_idle, gb_occ, gb_rate)):
        return out
    missing = [n for n, v in (("专门借款利息", sp_int), ("闲置资金收益", sp_idle),
                              ("加权平均占用额", gb_occ), ("资本化率", gb_rate)) if v is None]
    if missing:
        out.append("BC-CAP 任一侧缺失 ⇒ 整条跳过（缺：%s），不猜、不按 0 算" % "、".join(missing))
        return out
    sp = sp_int - sp_idle
    gb = gb_occ * gb_rate / Decimal(100)
    calc = sp + gb
    if (calc - disclosed).copy_abs() > BC_SPLIT_TOL:
        out.append("BC-CAP 专门(%.2f−%.2f=%.2f) + 一般(%.2f×%.2f%%=%.2f) = %.2f ≠ 披露资本化 %.2f（差 %.2f）"
                   % (sp_int, sp_idle, sp, gb_occ, gb_rate, gb, calc, disclosed, calc - disclosed))
    return out


LINE_CLAUSE = re.compile(r"[；;。，,｜|]")


def check_line(text):
    """道五 BC-LINE：四组越界词，只扫四个内容节（口径与未取到／来源两节整节豁免）。

    「」引文与〔…〕标签槽（口径／锚／自算）都不是本件断言——先洗掉再判：照抄附注的
    「预计」、锚指向的「预计负债」那个科目名，都是出处与标签，不是本件下的判断。
    再按 ；。，｜ 分句，含 [待人工] 或 未取到 的那一句跳过（判断位与缺口声明不是断言），
    同句后半段照样判。同组命中只报不被别的命中词包含的那些（「不合理」在，「合理」就不再报）。
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
                hits = []
                for group, words in REDLINES:
                    got = [w for w in words if w in clause]
                    if not got:
                        continue
                    kept = [w for w in got if not any(w != o and w in o for o in got)]
                    hits.append((group, kept))
                for group, kept in hits:
                    out.append("BC-LINE L%d 红线〔%s〕命中「%s」：%s"
                               % (lineno, group, "、".join(kept), clause.strip()[:44]))
    return out


CHECKS = {
    "BC-STRUCT": check_struct,
    "BC-QUOTE": check_bc_quote,
    "BC-CAP": check_cap,
    "BC-SPLIT": check_split,
    "BC-LINE": check_line,
}

DEMO = """# 示例材料（600000.SH）借款费用资本化登记稿

AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议
主体：示例材料（600000.SH）
报告期：2025 年年度报告·附注·借款费用资本化

## 借款费用概况

- 利息支出合计〔口径：本期发生额〕356.00 万元「本集团本期借款费用利息支出合计为人民币 356.00 万元」〔锚：2025 年年报·第 231 页·借款费用〕[S1]
- 其中资本化〔口径：本期发生额〕302.50 万元「其中予以资本化的金额为人民币 302.50 万元」〔锚：2025 年年报·第 231 页·借款费用〕[S1]
- 其中费用化〔口径：本期发生额〕53.50 万元「其中计入当期损益的金额为人民币 53.50 万元」〔锚：2025 年年报·第 231 页·借款费用〕[S1]

## 专门借款

- 专门借款本金〔口径：本期末〕5,000.00 万元「专门借款本金余额为人民币 5,000.00 万元」〔锚：2025 年年报·第 231 页·借款费用〕[S1]
- 专门借款年利率〔口径：本期〕4.35%「专门借款年利率为 4.35%」〔锚：2025 年年报·第 231 页·借款费用〕[S1]
- 专门借款利息〔口径：本期发生额〕217.50 万元「专门借款本期发生利息人民币 217.50 万元」〔锚：2025 年年报·第 231 页·借款费用〕[S1]
- 闲置资金收益〔口径：本期发生额〕12.50 万元「尚未动用的专门借款取得的利息收入为人民币 12.50 万元」〔锚：2025 年年报·第 231 页·借款费用〕[S1]
- 专门借款资本化金额〔口径：本期发生额〕205.00 万元「专门借款本期资本化金额为人民币 205.00 万元」〔锚：2025 年年报·第 231 页·借款费用〕[S1]

## 一般借款

- 一般借款加权平均占用额〔口径：本期〕1,950.00 万元「一般借款累计资产支出加权平均数为人民币 1,950.00 万元」〔锚：2025 年年报·第 231 页·借款费用〕[S1]
- 一般借款资本化率〔口径：本期〕5.00%「一般借款资本化率为 5.00%」〔锚：2025 年年报·第 231 页·借款费用〕[S1]
- 一般借款资本化金额〔口径：本期发生额〕97.50 万元「一般借款本期资本化金额为人民币 97.50 万元」〔锚：2025 年年报·第 231 页·借款费用〕[S1]

## 资本化期间与暂停

- 开始资本化时点〔口径：本期〕[待人工]
- 暂停资本化期间〔口径：本期〕[待人工]
- 终止资本化时点〔口径：本期〕[待人工]

## 口径与未取到

- 未取到：无
- 口径：借款费用的两侧（资本化／费用化）与两类借款的资本化金额一律照抄附注原句并挂锚；
  本件不判断融资成本高低、不预测以后期间利息，也不评价资本结构。

## 来源

- [S1] 示例材料 2025 年年度报告·附注·借款费用资本化 | https://example.invalid/600000_2025_notes.pdf | 检索日 2025-04-20
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
        print("用法: check_borrowing_cost.py <稿.md> | --demo | --selftest")
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
    ("好样应零发条（BC-STRUCT 与 BC-QUOTE 落字，其余计不可判）", DEMO, 0),
    ("头部删掉「不构成投资建议」", DEMO.replace(" ｜ 不构成投资建议", "", 1), 1),
    ("删掉「一般借款」整节", re.sub(r"## 一般借款\n(.*?)(?=\n## )", "", DEMO, flags=re.S), 1),
    ("把「来源」节改名成「参考资料」",
     DEMO.replace("## 来源", "## 参考资料", 1), 1),
    # 乱序回归档：六节都在、只把「来源」挪到「一般借款」之前。旧实现
    # `order = [s for s in SECTIONS if s in secs]` 让 order 恒等于规范序，这一档永远不红——
    # 本档就是那条死判据的护栏，不许删。分两步：先摘掉原「来源」节，再插到「一般借款」前
    # （一步链式 replace 会把刚插进去的那份又摘掉，因为第一次删除命中的是它）。
    ("把「来源」整节挪到「一般借款」之前（六节齐，只错序）",
     _NO_SOURCE.replace(
         "## 一般借款\n",
         "## 来源\n\n- [S1] 示例材料 2025 年年度报告·附注·借款费用资本化 | "
         "https://example.invalid/600000_2025_notes.pdf | 检索日 2025-04-20\n\n## 一般借款\n", 1,
     ), 1),
    # 以下三档是 BC-QUOTE 的反例（本拍新增）。
    ("溯源：概况某数字行删掉 [S#]（三元组缺一件）",
     DEMO.replace(
         "〔锚：2025 年年报·第 231 页·借款费用〕[S1]\n- 其中资本化",
         "〔锚：2025 年年报·第 231 页·借款费用〕\n- 其中资本化", 1),
     1),
    ("溯源：来源行检索日写成 2025/04/20（斜杠式）",
     DEMO.replace("检索日 2025-04-20", "检索日 2025/04/20", 1), 1),
    ("溯源：正文引了 [S2] 但来源节只有 [S1]",
     DEMO.replace("〔锚：2025 年年报·第 231 页·借款费用〕[S1]\n- 其中资本化",
                  "〔锚：2025 年年报·第 231 页·借款费用〕[S2]\n- 其中资本化", 1), 1),
    # 缺口两向：正文写了「未取到：X」而口径节只写「未取到：无」⇒ 发条。
    ("缺口：正文写「未取到：一般借款资本化率」但口径节说「未取到：无」",
     DEMO.replace(
         "- 一般借款资本化率〔口径：本期〕5.00%「一般借款资本化率为 5.00%」"
         "〔锚：2025 年年报·第 231 页·借款费用〕[S1]",
         "- 未取到：一般借款资本化率", 1),
     1),
    # 反证：正文与口径节两边都声明同一缺口 ⇒ 零发条（证明上面那条不是恒红）。
    ("缺口反证：正文与口径节两边都声明同一缺口 ⇒ 零发条",
     DEMO.replace(
         "- 一般借款资本化率〔口径：本期〕5.00%「一般借款资本化率为 5.00%」"
         "〔锚：2025 年年报·第 231 页·借款费用〕[S1]",
         "- 未取到：一般借款资本化率", 1).replace(
         "- 未取到：无", "- 未取到：一般借款资本化率", 1),
     0),
    # 项名在前、「未取到」在数值位（SKILL.md 第 77 行的合法写法）：缺口名须从「未取到」之后取，
    # 不许按位置切片（旧实现从第 len("未取到") 个字切，缺口名成了「本化时点…」的垃圾）。
    ("缺口：正文「终止资本化时点〔口径：本期〕未取到：终止时点」，口径节只声明「终止资本化时点」",
     DEMO.replace(
         "- 终止资本化时点〔口径：本期〕[待人工]",
         "- 终止资本化时点〔口径：本期〕未取到：终止时点", 1).replace(
         "- 未取到：无", "- 未取到：终止资本化时点", 1),
     1),
    # 反证：同上写法，但「未取到」后的名字与口径节同名 ⇒ 零发条（切片垃圾的回归护栏）。
    ("缺口反证：正文「终止资本化时点〔口径：本期〕未取到：终止资本化时点」与口径节同名 ⇒ 零发条",
     DEMO.replace(
         "- 终止资本化时点〔口径：本期〕[待人工]",
         "- 终止资本化时点〔口径：本期〕未取到：终止资本化时点", 1).replace(
         "- 未取到：无", "- 未取到：终止资本化时点", 1),
     0),
    # 续拍 C：两分与恒等。数字取自 DEMO（356.00 = 302.50 + 53.50；205.00 = 217.50 − 12.50；
    # 97.50 = 1950.00 × 5.00%），改任一侧都该被抓。
    ("C1 两分：其中资本化 302.50 → 300.00（两分加不回合计，恒等也对不上）",
     DEMO.replace(
         "- 其中资本化〔口径：本期发生额〕302.50 万元「其中予以资本化的金额为人民币 302.50 万元」",
         "- 其中资本化〔口径：本期发生额〕300.00 万元「其中予以资本化的金额为人民币 300.00 万元」", 1),
     1),
    ("C2 恒等：一般借款资本化率 5.00% → 6.00%（行内登记值与原句两处同改）",
     DEMO.replace(
         "- 一般借款资本化率〔口径：本期〕5.00%「一般借款资本化率为 5.00%」",
         "- 一般借款资本化率〔口径：本期〕6.00%「一般借款资本化率为 6.00%」", 1),
     1),
    ("C3 恒等：删掉「闲置资金收益」整行 ⇒ 整条跳过并点名缺项，不按 0 算",
     re.sub(r"- 闲置资金收益[^\n]*\n", "", DEMO),
     1),
    # 续拍 D：红线。四组词只扫四个内容节；引文与〔…〕标签槽先洗掉（照抄附注不算本件断言）；
    # [待人工] 与 未取到 只豁免自己那一句。这几档缺了，BC-LINE 就等于没被尺子量过。
    ("D1 红线：概况行里写「融资成本偏高」",
     DEMO.replace(
         "- 一般借款资本化金额〔口径：本期发生额〕97.50 万元",
         "- 一般借款资本化金额 融资成本偏高〔口径：本期发生额〕97.50 万元", 1),
     1),
    ("D2 红线：原句里抄了「预计」不算本件断言 ⇒ 零发条",
     DEMO.replace(
         "「其中计入当期损益的金额为人民币 53.50 万元」",
         "「公司预计其中计入当期损益的金额为人民币 53.50 万元」", 1),
     0),
    ("D3 红线：[待人工] 只豁免自己那一句，同句后半段照样发",
     DEMO.replace(
         "- 开始资本化时点〔口径：本期〕[待人工]",
         "- 开始资本化时点 [待人工]；融资成本偏高", 1),
     1),
    ("D4 红线：口径与未取到整节豁免（该节写「目标价」也不发）",
     DEMO.replace(
         "  本件不判断融资成本高低、不预测以后期间利息，也不评价资本结构。",
         "  本件不判断融资成本高低；这里提一句目标价也只是说明口径边界。", 1),
     0),
    # 标签槽误报的回归护栏：〔锚：…预计负债…〕指的是附注科目名，〔口径：…〕是标签，
    # 两者都不是本件断言。不洗掉标签槽，照抄一个叫「预计负债」的科目就会被判红。
    ("D5 红线：锚指向「预计负债」科目名不算断言 ⇒ 零发条",
     DEMO.replace("第 231 页·借款费用", "第 231 页·预计负债", 1),
     0),
    ("D6 红线：口径槽里写「预计」是标签不是断言 ⇒ 零发条",
     DEMO.replace("〔口径：本期发生额〕97.50", "〔口径：预计下年〕97.50", 1),
     0),
)


def selftest():
    bad = 0
    for name, text, want in CASES:
        findings, unjudged = run(text)
        if want == 0:
            ok = (not findings)
            got = "发条 %d 条：%s" % (len(findings), "；".join(findings) or "无")
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
