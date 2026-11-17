#!/usr/bin/env python3
"""check_dd.py — dd-checklist-cn 0.1.0 门禁（八道，诊断码分层）。

用法（六个参数全部必传，缺任一 = DD-INPUT，退出码 1；不设默认窗口）：

    python3 check_dd.py <report.md> \
      --subject '北辰股份有限公司（600001.SH）' \
      --asof 2026-09-21 --lookback 36m --purpose investment \
      --sources sources.jsonl --evidence evidence

诊断前缀（题单 R0-I §0.3 钉死，不得改名）：
  DD-INPUT / DD-TABLE / DD-ROW / DD-REDLINE / DD-COVERAGE / DD-EVIDENCE / DD-STATUTE / DD-OMISSION

退出码：0=PASS；1=FAIL（含任何一道）。本脚本不抛 traceback——内部异常一律折算成
DD-INPUT 诊断后 exit 1（题单 §0.1：崩溃不算命中）。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

CATEGORIES = (
    "股权与控制权",
    "合规与处罚",
    "诉讼与仲裁",
    "财务与披露质量",
    "关联交易与资金占用",
    "业务资质与许可",
    "人力与社保",
    "上市与在审状态",
    "其他已披露重大事项",
)
IMPACTS = ("重大", "关注", "背景")
# §v2-16①：覆盖率账的固定文法——恰五列、顺序精确；集合包含不证明顺序，也不证明宽度
LEDGER_HEADER = ("类目", "所需域/工具", "本次实际调用", "结果", "注记")
PURPOSES = ("investment", "credit", "mna")
KINDS = (
    "entity_data",
    "disclosure_cn",
    "regulatory_cn",
    "statute",
    "ipo",
    "fr_fact_index",
    "fr_footnote",
    "buyback",
    "esop",
    "research",
    "omni",
    "user_supplied",
)
CONFIDENCES = ("L1", "L2", "L3")

# §v2-16②（契约 spec 第 16 条②钉定）：「本次实际调用」格=单记号、或以中文顿号紧连的记号集
LEDGER_SET_SEP = "、"


def parse_called(cell: str) -> tuple[set, str]:
    """把「本次实际调用」格解析成域记号集合。返回 (集合, 缺陷说明)，缺陷说明为空即形制合法。

    只判形制与集合相等，不判来源真假（§7.8）。逗号/空格/斜杠拼接、或把两域写成一个新域名，
    都不算连记号，按非法域计——合法的多域只有一种写法。
    """
    raw = (cell or "").strip()
    if not raw:
        return set(), "为空"
    if LEDGER_SET_SEP in raw:
        toks = raw.split(LEDGER_SET_SEP)
        if any(t != t.strip() or not t for t in toks):
            return set(), f"连记号内含空格或空项（须以中文顿号「{LEDGER_SET_SEP}」紧连、不空格）：{cell!r}"
        if len(set(toks)) != len(toks):
            return set(), f"连记号内有重复域：{cell!r}"
        bad = [t for t in toks if t not in KINDS]
        if bad:
            return set(), f"含不在本件域枚举内的记号 {('、'.join(bad))}：{cell!r}"
        return set(toks), ""
    if raw in KINDS:
        return {raw}, ""
    return set(), f"不在本件域枚举内（多域只认中文顿号「{LEDGER_SET_SEP}」相连，逗号/空格/斜杠拼接按非法域计）：{cell!r}"


HEADER_COLS = ("日期", "类目", "事实(≤40字,只写披露所载)", "影响档位", "状态", "窗外余档", "来源锚")

FACT_MAX = 40

# 自白词（§2：不得以推测补条目）
CONFESSION = ("惯例", "通常", "预计", "大概率")
# 红线（§4.1/§4.2/§4.3）——全交付物零豁免：表格、脚注、标题、引用块、代码围栏、sources 可交付字段
REDLINE_INVEST = (
    "可投",
    "不建议投",
    "建议回避",
    "减持建议",
    "建议减持",
    "买入",
    "目标价",
    "估值",
    "否决",
    "尽调通过",
    "筛查通过",
)
# §4.1 的「通过」是**结论位**禁语；「审议通过/表决通过/股东大会通过」属披露原文转述，
# 用否定回溯排除这一类状语前缀，其余一律命中（细化，不放宽）。
REDLINE_PASS = re.compile(r"(?<!审议)(?<!表决)(?<!批准)(?<!通过审议)(?<!会)(?<!局)(?<!委)(?<!组)通过")
REDLINE_LEGAL = ("构成违法", "违规成立", "应被处罚", "无需披露", "不触及重大违法")
REDLINE_COMPLETE = ("已覆盖全部", "无风险", "未发现异常", "尽调完成", "干净")
# §4.4：域面外/零条不得偷换成主体否定断言
NO_TOOL_ASSERT = ("无诉讼", "不存在诉讼", "没有诉讼", "无社保", "无违规", "无处罚记录", "无异常")

# §v2-1：一次运行的交付面=这四件，红线扫这四件的全部文字。
# 包级 README/SKILL 不属交付面（说明文档会解释禁词，不做全文硬扫），且明令不得把单次运行结论写进包级 README。
DELIVERABLES = ("report.md", "sources.jsonl", "references/coverage-map.md", "progress.md")

# §v2-5：已知「来源→类目」一对一映射机检（至少一对一，闭 M1）。
# 触发词只在事实列出现时才绑类目，避免把别处的中性披露误判（细化，不放宽第一闸）。
CATEGORY_BY_KIND = {
    "regulatory_cn": ("合规与处罚", ("监管函", "问询函", "警示", "处罚")),
    "ipo": ("上市与在审状态", None),
    "fr_fact_index": ("财务与披露质量", None),
    "fr_footnote": ("财务与披露质量", None),
}

ANCHOR_AN = re.compile(r"^AN\d{12,20}$")
ANCHOR_URL = re.compile(r"^https?://\S+$")
ANCHOR_LETTER = re.compile(r"^[\u4e00-\u9fa5A-Za-z0-9]{2,20}〔\d{4}〕\d{1,6}号$")
ANCHOR_COURT = re.compile(r"^（\d{4}）[\u4e00-\u9fa5A-Za-z0-9]{1,16}号$")
ANCHOR_CONV = re.compile(r"^(conv_id[:：]?|conv_)[0-9A-Za-z_-]{4,}$")
ANCHOR_STATUTE = re.compile(r"^statute[:：]《[^》]{2,40}》第[0-9一二三四五六七八九十百]{1,6}条（[^）]{2,40}）$")

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CODE_ONLY_SUBJECT = re.compile(r"^\d{6}\.(SH|SZ|BJ)$")
# §v2-3(c)：法定推导行的「条件可判」必须有主体侧锚——形制=一行 `推导条件: <ref>`（ref 须在 sources 可解析且有 evidence 原始件）
DERIVE_CONDITION_LINE = re.compile(r"推导条件[:：]\s*([^\s（）()、，,；;]+)")
SUBJECT_TOKEN = re.compile(r"([\u4e00-\u9fa5A-Za-z0-9]{2,24}股份有限公司|[\u4e00-\u9fa5A-Za-z0-9]{2,24}有限公司)[（(](\d{6}\.[A-Z]{2})[）)]")
TITLE_WINDOW = re.compile(r"窗口\s*(\d{4}-\d{2}-\d{2})\s*[~～]\s*(\d{4}-\d{2}-\d{2})")
SECTION_DOMAIN_LINE = re.compile(r"本节检索域[:：]\s*(.*?)\s*(\d+)\s*域\s*/\s*无工具项[:：]\s*(\d+)")
PARAM_LINE = re.compile(r"^-\s*(subject|asof|lookback|purpose)\s*[:：]\s*(\S.*?)\s*$")

# §v2-11（M89 裁定①，M91 落机器核）：长窗的类目账龄可达面不得静默冒充标题窗。
# 触发=窗口跨度 > 类目检索面已知上限 且 本次实调 disclosure_cn 类目账；发码 DD-COVERAGE。
AGE_CAP_DAYS = 365
AGE_REQUIRED_BEYOND = "未按类目互校"
AGE_LAUNDER = ("已覆盖", "全覆盖", "零条", "不存在", "无异常", "无风险")
AGE_DECL_LINE = re.compile(
    r"^\s*(?:[-*>]\s*)?类目账龄申报\s*[:：]\s*requested=(\d{4}-\d{2}-\d{2})\s*[~～]\s*(\d{4}-\d{2}-\d{2})"
    r"\s*\|\s*disclosure_cn=(\d{1,4})d\s*\|\s*beyond=(.+?)\s*$"
)
# §v2-14（M98 复审）：一把识别器判级别——H1=文档标题、H2–H4=节、H5/H6=节内附注。
# 覆盖率节因此只在 H2–H4 层级认（H1 标题里带「未检到」不算节、不参与计数）。
COVERAGE_HEADING = re.compile(r"^ {0,3}#{2,4}(?:\s|$).*(?:覆盖率|未检到)")
# ATX 标题允许 0–3 个前导空格（CommonMark 合法）；只认 startswith("#") 会让缩进标题隐身，
# 节定位失败后若回退全文，就等于把别节当本节（§v2-12）。
ATX_HEADING = re.compile(r"^ {0,3}#{1,6}(?:\s|$)")
HEADING_LEVEL = re.compile(r"^ {0,3}(#{1,6})(?:\s|$)")
# §v2-15④：代码围栏起始行（``` 或 ~~~，允许 0–3 前导空格）——围栏内一切按示例文本处理
FENCE_OPEN = re.compile(r"^(`{3,}|~{3,})")
SECTION_HEADING = re.compile(r"^ {0,3}#{2,4}(?:\s|$)")


def heading_level(line: str) -> int:
    """0=不是标题；1=文档标题；2-4=节；5-6=节内附注（不结束节、不另起节）。"""
    m = HEADING_LEVEL.match(line)
    return len(m.group(1)) if m else 0


def ends_section(line: str) -> bool:
    """节到哪结束：只有 H2–H4 才结束当前节；H5/H6 属节内附注，H1 是文档标题。"""
    return bool(SECTION_HEADING.match(line))


def is_heading(line: str) -> bool:
    return bool(ATX_HEADING.match(line))
# 「先收后判」用：凡带权威前缀的原始行都先收进来（伪行单位写成「日」、beyond 被改写也要收），再核数量与语法
DECL_PREFIX_LOOSE = re.compile(r"^\s*(?:[-*>]\s*)?类目账龄申报\s*[:：]")


DECL_TOKENS = ("本页为AI初稿", "依据公开披露与法定原文整理", "不构成投资建议", "不构成法律意见", "判断位[待人工]")


def _norm(text: str) -> str:
    out = norm_cell(text)
    for ch in (" ", "\t", "　", "\u3000"):
        out = out.replace(ch, "")
    return out


def is_authoritative(line: str) -> bool:
    """§3 权威句式：单行完整承载五要件（标点/空格归一后逐件包含）。"""
    n = _norm(line)
    return all(tok in n for tok in DECL_TOKENS)


def records_of(body: str) -> list:
    """把 evidence 快照拆成逐条记录（一条一袋）；解析不了就整件一袋。"""
    try:
        obj = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return [body]
    recs = obj.get("records") if isinstance(obj, dict) else None
    if isinstance(recs, list) and recs:
        return [json.dumps(r, ensure_ascii=False) for r in recs]
    return [json.dumps(obj, ensure_ascii=False)]


class Findings:
    def __init__(self) -> None:
        self.items: list[str] = []

    def add(self, code: str, msg: str) -> None:
        line = f"{code}: {msg}"
        if line not in self.items:
            self.items.append(line)

    @property
    def codes(self) -> set[str]:
        return {i.split(":", 1)[0] for i in self.items}

    def has_code(self, code: str) -> bool:
        return any(i.startswith(code + ": ") for i in self.items)


# ---------------------------------------------------------------- 错误码表(M166)
# 五类码表 E_LEGEND 全族逐字一致(各件出口同源);E_RULES 把本件 8 枚 DD-* 码归入五类
# ——DD-* 是规则号(保留于消息原位),[E-XXX] 是分类号(详行行首)。
# 详行前缀 `[E-XXX] `,原消息一字不动;runner 抽码 sed 已同步兼容行首前缀。
E_LEGEND = {
    "E-FORMAT":   "形制/输入/表序不合式→按该行括号内规格改形制后复跑",
    "E-ANCHOR":   "锚/证据链缺失或断链→补合式锚或删除该条,禁虚构",
    "E-BANWORD":  "禁词/评级/幻觉/待人工域命中→改中性陈述或删除,零豁免区",
    "E-COVERAGE": "计数/覆盖/申报对不上→逐类补账或如实标未检索到",
    "E-LEDGER":   "账本状态机/互链断→按账本契约重建链接,禁改写历史",
}
E_RULES = (
    ("E-BANWORD", r"^DD-REDLINE"),
    ("E-ANCHOR", r"^DD-(STATUTE|EVIDENCE)"),
    ("E-COVERAGE", r"^DD-(COVERAGE|OMISSION)"),
    ("E-FORMAT", r"^DD-(INPUT|TABLE|ROW)"),
)


def ecode(msg: str) -> str:
    for code, pat in E_RULES:
        if re.search(pat, msg):
            return code
    return "E-FORMAT"


def norm_cell(text: str) -> str:
    out = text.strip()
    for full, half in (("（", "("), ("）", ")"), ("，", ","), ("：", ":")):
        out = out.replace(full, half)
    return out


def split_pipe(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in body.split("|")]


def is_sep_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells)


def months_back(d: date, months: int) -> date:
    total = d.year * 12 + (d.month - 1) - months
    year, month = divmod(total, 12)
    month += 1
    day = d.day
    while day > 28:
        try:
            return date(year, month, day)
        except ValueError:
            day -= 1
    return date(year, month, day)


def days_back(d: date, days: int) -> date:
    from datetime import timedelta

    return d - timedelta(days=days)


def window_start(asof: date, lookback: str) -> date | None:
    m = re.fullmatch(r"(\d+)([mdy])", lookback.strip())
    if not m:
        return None
    n, unit = int(m.group(1)), m.group(2)
    if unit == "m":
        return months_back(asof, n)
    if unit == "y":
        return months_back(asof, n * 12)
    return days_back(asof, n)


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def fence_mask(lines: list[str]) -> list[bool]:
    """§v2-15④ / §v2-16：按 CommonMark 词法标记"落在代码围栏内"的行。
    开栏：至多 3 个前导空格 + 连续 ≥3 个 ` 或 ~；四空格缩进的 ``` 是缩进代码行，不开栏。
    闭栏：至多 3 个前导空格 + 同种字符、长度 ≥ 开栏、行内无其它内容。
    围栏内 ## 是示例文本、申报是示例、管道行不是账；红线扫描不用本掩码（全篇照扫）。"""
    mask: list[bool] = []
    open_char = ""
    open_len = 0
    for ln in lines:
        lead = len(ln) - len(ln.lstrip(" "))
        stripped = ln.strip()
        if not open_char:
            m = FENCE_OPEN.match(stripped)
            if m and lead <= 3:
                run = m.group(1)
                info = stripped[len(run):].strip()
                if run[0] != "`" or "`" not in info:   # 反引号围栏的信息串不得再含反引号
                    open_char, open_len = run[0], len(run)
                    mask.append(True)
                    continue
            mask.append(False)
            continue
        if lead <= 3 and stripped and set(stripped) == {open_char} and len(stripped) >= open_len:
            mask.append(True)
            open_char, open_len = "", 0
            continue
        mask.append(True)
    return mask


def body_indices(lines: list[str]) -> list[int]:
    return [i for i, inside in enumerate(fence_mask(lines)) if not inside]


def section_range(lines: list[str], idx: int) -> tuple[int, int]:
    """含第 idx 行的那一节：以 H1–H4 为界（§v2-14 一把尺），围栏内标题不算界（§v2-15④）。"""
    mask = fence_mask(lines)
    def is_bound(i: int) -> bool:
        return not mask[i] and 1 <= heading_level(lines[i]) <= 4
    lo = 0
    for i in range(idx - 1, -1, -1):
        if is_bound(i):
            lo = i + 1
            break
    hi = len(lines)
    for i in range(idx + 1, len(lines)):
        if is_bound(i):
            hi = i
            break
    return lo, hi


def _date_or_none(text: str) -> date | None:
    """把 YYYY-MM-DD 真解析成日历日；不存在的日子（2026-02-30）返回 None（§v2-15⑦）。"""
    try:
        return date.fromisoformat(text.strip())
    except ValueError:
        return None


# ---------------------------------------------------------------- main checks
def check_inputs(ns, report: Path, finds: Findings) -> dict:
    missing = [f for f in ("subject", "asof", "lookback", "purpose", "sources", "evidence") if getattr(ns, f, None) in (None, "")]
    if missing:
        for f in missing:
            finds.add("DD-INPUT", f"参数 --{f} 缺失（六参数全必传，不设默认值/默认目录）")
        return {}
    if not report.is_file():
        finds.add("DD-INPUT", f"交付物不存在：{report}")
        return {}

    try:
        asof = date.fromisoformat(ns.asof)
    except ValueError:
        finds.add("DD-INPUT", f"--asof 非 YYYY-MM-DD：{ns.asof!r}")
        return {}
    if not ns.lookback or not re.fullmatch(r"\d+[myd]", ns.lookback.strip()):
        finds.add("DD-INPUT", f"--lookback 非法（须如 36m/24y/180d，禁 wall clock 默认窗）：{ns.lookback!r}")
        return {}
    start = window_start(asof, ns.lookback)
    if start is None:
        finds.add("DD-INPUT", f"--lookback 无法解析：{ns.lookback!r}")
        return {}
    if ns.purpose not in PURPOSES:
        finds.add("DD-INPUT", f"--purpose 非封闭三值 investment|credit|mna：{ns.purpose!r}")
        return {}

    text = read_text(report)
    if text is None:
        finds.add("DD-INPUT", f"交付物无法读取：{report}")
        return {}

    lines = text.splitlines()
    fence = fence_mask(lines)  # §v2-15④：正文语境一次算好，标题/节/回显/表提取共用
    subject_raw = (ns.subject or "").strip()
    subject_full = subject_code = None
    m = SUBJECT_TOKEN.fullmatch(subject_raw)  # §v2-15⑤：完整匹配，不再 search() 抓首个主体
    if m:
        subject_full, subject_code = m.group(1), m.group(2)
    elif CODE_ONLY_SUBJECT.fullmatch(subject_raw):
        # §v2-4：纯「6 位代码+上市地」是合法输入形态；归属改由正文/证据内「全称+代码」双标完成（见 check_anchor_chain）
        subject_code = subject_raw.upper()
    else:
        finds.add("DD-INPUT", f"--subject 不是单一合法形制（二选一：「全称（6位代码.SH|.SZ|.BJ）」或纯「6位代码.SH|.SZ|.BJ」；含两个主体的串不取首个，§v2-15⑤）：{ns.subject!r}")

    # 铁律 1 机器面（M71，M73 按 DD-X15 收严）：权威句式须由**标题后前 5 行内的同一行**完整承载，跨行拼凑不算
    h1s = [i for i, ln in enumerate(lines) if not fence[i] and heading_level(ln) == 1]
    if len(h1s) > 1:
        finds.add("DD-INPUT", f"文档 H1 标题有 {len(h1s)} 个（第 {h1s[0] + 1}、{h1s[1] + 1} 行…）——输入权威元数据须单值，不取首个也不取末个（§v2-15⑤）")
    ti = h1s[0] if h1s else None
    if ti is None:
        finds.add("DD-INPUT", "交付物无 H1 标题行——声明行窗口无处可核（§1 铁律 1）")
    else:
        # §v2-16③：窗口与兜底都只认「可交付正文行」——围栏内的示例声明不满足在场，也不满足位置
        after = [i for i in range(ti + 1, len(lines)) if not fence[i]]
        win = [lines[i] for i in after[:5]]
        body = [lines[i] for i in after[5:]]
        deliverable = [ln for i, ln in enumerate(lines) if not fence[i]]
        if not any(is_authoritative(l) for l in win):
            if any(is_authoritative(l) for l in body):
                finds.add("DD-INPUT", "AI 初稿权威声明行不在标题后前 5 行内（§1 铁律 1；越界即不认）")
            elif not any("AI 初稿" in _norm(l) for l in deliverable):
                finds.add("DD-INPUT", "缺 AI 初稿声明行（§1 铁律 1；权威句式见 §3）")
            else:
                finds.add("DD-INPUT", "标题后前 5 行内的声明不是权威句式单行——须同一行完整承载「本页为 AI 初稿 / 依据公开披露与法定原文整理 / 不构成投资建议 / 不构成法律意见 / 判断位 [待人工]」，跨行拼凑与笼统免责不认")

    # 标题窗口复算（§1）
    title_line = lines[ti] if ti is not None else ""
    tw = TITLE_WINDOW.search(title_line)
    if not tw:
        finds.add("DD-INPUT", "标题未载明「窗口 YYYY-MM-DD~YYYY-MM-DD」")
    else:
        t_start, t_end = tw.group(1), tw.group(2)
        want = f"{start.isoformat()}~{asof.isoformat()}"
        if f"{t_start}~{t_end}" != want:
            finds.add("DD-INPUT", f"标题窗口与参数不一致：应为 {want}（--asof {ns.asof} --lookback {ns.lookback}），实为 {t_start}~{t_end}")

    # 参数回显行一致性（§v2-15⑤：四条回显各须恰一个，围栏内不算，也不许 first/last-wins）
    echo_all: dict[str, list[str]] = {}
    for i, ln in enumerate(lines):
        if fence[i]:
            continue
        pm = PARAM_LINE.match(ln)
        if pm:
            echo_all.setdefault(pm.group(1), []).append(pm.group(2))
    for key in ("subject", "asof", "lookback", "purpose"):
        vals = echo_all.get(key, [])
        if len(vals) > 1:
            finds.add("DD-INPUT", f"正文参数回显 `- {key}:` 有 {len(vals)} 行（{'、'.join(vals)}）——回显须单值，矛盾的两行不取首个也不取末个（§v2-15⑤）")
    echo = {k: v[0] for k, v in echo_all.items()}
    for key, want in (("subject", ns.subject), ("asof", ns.asof), ("lookback", ns.lookback), ("purpose", ns.purpose)):
        got = echo.get(key)
        if got is None:
            finds.add("DD-INPUT", f"正文参数行 `- {key}:` 缺失")
        elif key == "subject" and subject_full is None and subject_code:
            tok = SUBJECT_TOKEN.search(got)
            if got.strip() == want.strip():
                pass  # 回显同形制（纯代码）；全称+代码双标由证据侧完成（§v2-4）
            elif not tok or tok.group(2) != subject_code:
                finds.add("DD-INPUT", f"正文 `- subject: {got}` 与命令行 --subject {want} 的代码不一致（§v2-4 双标归属）")
        elif got != want:
            finds.add("DD-INPUT", f"正文 `- {key}: {got}` 与命令行 --{key} {want} 不一致")

    # 一单一主体（§1）：不采信命令行，须从正文标题面识别
    heads = [ln for i, ln in enumerate(lines) if not fence[i] and 1 <= heading_level(ln) <= 4]  # §v2-14 一把尺 + §v2-15④ 围栏内不作数
    subjects: list[str] = []
    for ln in heads:
        for tok in SUBJECT_TOKEN.finditer(ln):
            key = f"{tok.group(1)}（{tok.group(2)}）"
            if key not in subjects:
                subjects.append(key)
    if len(subjects) > 1:
        finds.add("DD-INPUT", f"主体数 {len(subjects)} > 1（本件一单一主体，批量必然逐条锚失守）：" + "、".join(subjects))
    elif subjects and subject_code:
        tok = SUBJECT_TOKEN.search(subjects[0])
        want_full = f"{subject_full}（{subject_code}）" if subject_full else None
        if (want_full and subjects[0] != want_full) or (want_full is None and (not tok or tok.group(2) != subject_code)):
            finds.add("DD-INPUT", f"标题主体 {subjects[0]} 与 --subject {ns.subject} 不一致")

    return {
        "text": text,
        "lines": lines,
        "fence": fence_mask(lines),  # §v2-15④：可交付正文语境，一次算给标题/节/申报/表四处共用
        "asof": asof,
        "start": start,
        "subject_full": subject_full,
        "subject_code": subject_code,
        "purpose": ns.purpose,
    }


def parse_tables(lines: list[str], finds: Findings) -> list[dict]:
    """返回 [{rows:[{...}], subject, start}]；表头状态机=固定七列名+分隔行（§3，B1 教训）。"""
    tables = []
    mask = fence_mask(lines)  # §v2-15④：围栏内的管道行是示例表格，不作七列表提取
    i = 0
    while i < len(lines):
        ln = lines[i]
        if mask[i] or not ln.strip().startswith("|"):
            i += 1
            continue
        block_start = i
        block = []
        while i < len(lines) and not mask[i] and lines[i].strip().startswith("|"):
            block.append((i + 1, lines[i]))
            i += 1
        head_subject = None
        for prev_i in range(block_start - 1, -1, -1):
            if mask[prev_i]:
                continue  # §v2-15④：围栏内标题是示例文本，不参与节归属
            prev = lines[prev_i]
            lvl = heading_level(prev)
            if lvl >= 5:
                continue  # §v2-14：H5/H6 是节内附注，不改变归属，继续向上找真正的节标题
            if lvl >= 1:
                # 缩进 1–3 空格的标题同样是合法标题，漏认会一路回溯到上层标题、取错节主体
                tok = SUBJECT_TOKEN.search(prev)
                head_subject = f"{tok.group(1)}（{tok.group(2)}）" if tok else None
                break
        cells0 = split_pipe(block[0][1])
        if is_sep_row(cells0):
            finds.add("DD-TABLE", f"第 {block_start + 1} 行：分隔行出现在表首之前，缺固定七列表头")
            continue
        got = [norm_cell(c) for c in cells0]
        want = [norm_cell(c) for c in HEADER_COLS]
        if got != want:
            if DATE_RE.match(cells0[0]):
                finds.add("DD-TABLE", f"第 {block_start + 1} 行：裸数据行无固定七列表头——段落首个管道行不自动当表头（B1）")
                continue
            detail = "列名与固定七列不符"
            if len(got) == len(want):
                diffs = [f"第{k + 1}列应为「{w}」实为「{g}」" for k, (g, w) in enumerate(zip(got, want)) if g != w]
                if diffs:
                    detail = "；".join(diffs)
            finds.add("DD-TABLE", f"第 {block_start + 1} 行：{detail}（不得因列数为七放行）")
            continue
        if len(block) < 2 or not is_sep_row(split_pipe(block[1][1])):
            finds.add("DD-TABLE", f"第 {block_start + 1} 行：固定七列表头后缺分隔行（|---|…|）")
            continue
        rows = []
        for lineno, row in block[2:]:
            rc = split_pipe(row)
            if len(rc) != len(want):
                finds.add("DD-TABLE", f"第 {lineno} 行：列数 {len(rc)} ≠ 7")
                continue
            rows.append({"lineno": lineno, **dict(zip(("date", "category", "fact", "impact", "status", "carry", "anchor"), [c.strip() for c in rc]))})
        tables.append({"rows": rows, "start": block_start, "subject": head_subject})
    return tables


def check_rows(tables, ctx, finds: Findings, src=None) -> None:
    start, asof = ctx["start"], ctx["asof"]
    kinds_by_ref = (src or {}).get("kind_by_ref", {})
    for t in tables:
        prev = None
        for r in t["rows"]:
            ln = r["lineno"]
            d = r["date"]
            if not DATE_RE.match(d):
                finds.add("DD-ROW", f"第 {ln} 行：日期非 YYYY-MM-DD 全格式：{d!r}")
            else:
                try:
                    dd = date.fromisoformat(d)
                    if dd < start or dd > asof:
                        finds.add("DD-ROW", f"第 {ln} 行：日期 {d} 在窗口 [{start.isoformat()}, {asof.isoformat()}] 外（早于 {start.isoformat()}）" if dd < start else f"第 {ln} 行：日期 {d} 在窗口 [{start.isoformat()}, {asof.isoformat()}] 外（晚于 {asof.isoformat()}）")
                except ValueError:
                    finds.add("DD-ROW", f"第 {ln} 行：日期不可解析：{d!r}")
            if r["category"] not in CATEGORIES:
                finds.add("DD-TABLE", f"第 {ln} 行：类目「{r['category']}」不在九项封闭枚举内，不入表")
            if r["impact"] not in IMPACTS:
                finds.add("DD-TABLE", f"第 {ln} 行：影响档位「{r['impact']}」不在封闭枚举 重大|关注|背景 内")
            fact_len = len(re.sub(r"\s", "", r["fact"]))
            if fact_len > FACT_MAX:
                finds.add("DD-TABLE", f"第 {ln} 行：事实列 {fact_len} 字 > {FACT_MAX} 字上限（只写披露所载，不得借有锚放宽形制）")
            for w in CONFESSION:
                if w in r["fact"]:
                    finds.add("DD-ROW", f"第 {ln} 行：事实列含自白词「{w}」——入类第一闸不接受推测，无在场披露即不入表")
            anchor = r["anchor"]
            if anchor in ("", "—", "-", "－", "无", "N/A", "n/a", "见下", "待补"):
                smuggled = re.search(r"\d{6,}", " ".join([r["fact"], r["carry"], r["status"]]))
                hint = f"；事实列出现的 {smuggled.group(0)} 属金额/股数，不认作公告号或函件号" if smuggled else ""
                finds.add("DD-ROW", f"第 {ln} 行：完整来源锚缺失（锚只认最后一列，其他列的公告号/数字不补位{hint}）")
            else:
                if any(rx.match(anchor) for rx in (ANCHOR_AN, ANCHOR_URL, ANCHOR_LETTER, ANCHOR_COURT, ANCHOR_CONV, ANCHOR_STATUTE)):
                    ctx.setdefault("row_anchors", []).append({"lineno": ln, "anchor": anchor, "status": r["status"], "fact": r["fact"], "category": r["category"], "section_subject": t.get("subject")})
                else:
                    finds.add("DD-ROW", f"第 {ln} 行：锚型不在白名单（URL/公告 AN 号/函件号/裁判文书号/conv_id/statute 原文锚）：{anchor!r}——金额、股数、纯数字不认作锚")
            derived = r["status"] == "推导" or any(k in r["fact"] for k in ("推得", "应披露", "法定期限", "截止日推"))
            if derived:
                ctx.setdefault("derived_rows", []).append({"lineno": ln, "anchor": anchor, "fact": r["fact"]})
            if prev is not None and DATE_RE.match(prev) and DATE_RE.match(d) and date.fromisoformat(prev) > date.fromisoformat(d):
                finds.add("DD-TABLE", f"第 {ln} 行：日期倒序 {prev} → {d}（同一主体节内须按日期非降序排列）")
            # §v2-5：已知「来源→类目」一对一映射不得降档（闭 M1：全塞「其他」+「背景」=形式化假门）
            kind = kinds_by_ref.get(anchor) if anchor else None
            bound = CATEGORY_BY_KIND.get(kind or "")
            if bound:
                want_cat, trigger = bound
                if trigger is None or any(w in r["fact"] for w in trigger):
                    if r["category"] != want_cat:
                        finds.add("DD-TABLE", f"第 {ln} 行：来源域 {kind} 的「{r['fact'][:14]}…」按 channel-map §2 属「{want_cat}」，不得记作「{r['category']}」（类目不是任意枚举桶）")
                    if want_cat == "合规与处罚" and r["impact"] == "背景":
                        finds.add("DD-TABLE", f"第 {ln} 行：{kind} 监管函/问询类事实档位不得降为「背景」（三档描述披露事实量级，不是降档通道）")
            prev = d


def check_redlines(files, finds: Findings) -> None:
    scanned = [(name, blob) for name, blob in files if blob]
    for fname, blob in scanned:
        for lineno, ln in enumerate(blob.splitlines(), start=1):
            for w in REDLINE_INVEST:
                if w in ln:
                    finds.add("DD-REDLINE", f"{fname}:{lineno} 命中投资建议词「{w}」——判断位=空壳 [待人工]，本件无豁免区")
            if REDLINE_PASS.search(ln):
                finds.add("DD-REDLINE", f"{fname}:{lineno} 结论位「通过」类投资建议——本件只列带锚事实，通过/否决判断归人（审议/表决/批转型转述不在此列）")
            for w in REDLINE_LEGAL:
                if w in ln:
                    finds.add("DD-REDLINE", f"{fname}:{lineno} 命中法律意见句「{w}」——只转述披露所载事实")
            for w in REDLINE_COMPLETE:
                if w in ln:
                    finds.add("DD-REDLINE", f"{fname}:{lineno} 命中完备性禁语「{w}」——诚实形=本次所查域与窗口内检到 N 条带锚事项")
            for w in NO_TOOL_ASSERT:
                if w in ln:
                    finds.add("DD-COVERAGE", f"{fname}:{lineno} 把「域面无工具/检到零条」写成主体否定断言「{w}」——无工具不等于不存在，无工具项只进 §5 对账表")


def check_sources(path: Path, finds: Findings) -> dict:
    out = {"refs": {}, "kind_by_ref": {}, "records": {}, "ids": {}}
    raw = read_text(path)
    if raw is None:
        finds.add("DD-EVIDENCE", f"sources 不可读或不存在：{path}")
        return out
    for lineno, ln in enumerate(raw.splitlines(), start=1):
        if not ln.strip():
            continue
        try:
            obj = json.loads(ln)
        except json.JSONDecodeError as e:
            finds.add("DD-EVIDENCE", f"sources:{lineno} 非合法 JSON 行：{e}")
            continue
        if not isinstance(obj, dict):
            finds.add("DD-EVIDENCE", f"sources:{lineno} 非对象形状")
            continue
        sid = obj.get("id")
        if not isinstance(sid, str) or not re.fullmatch(r"S\d+", sid):
            finds.add("DD-EVIDENCE", f"sources:{lineno} id 非法（须 S<n>）：{sid!r}")
            continue
        if sid in out.setdefault("ids", {}):
            finds.add("DD-EVIDENCE", f"sources:{lineno} id 重复：{sid}")
            continue
        out["ids"][sid] = True
        kind = obj.get("kind")
        if kind not in KINDS:
            finds.add("DD-EVIDENCE", f"sources:{lineno}({sid}) kind 非封闭枚举：{kind!r}——ref 像公告号也不放行")
        ref = obj.get("ref")
        if not isinstance(ref, str) or not ref.strip():
            finds.add("DD-EVIDENCE", f"sources:{lineno}({sid}) 缺 ref（须外部可核锚）")
        else:
            ref = ref.strip()
            out["refs"].setdefault(ref, []).append(sid)
            out["kind_by_ref"].setdefault(ref, kind)
            out["records"].setdefault(ref, []).append({"id": sid, "kind": kind, "claim": obj.get("claim")})
        conf = obj.get("confidence")
        if conf not in CONFIDENCES:
            finds.add("DD-EVIDENCE", f"sources:{lineno}({sid}) confidence 非封闭枚举 L1|L2|L3：{conf!r}")
        asof = obj.get("asof")
        if not isinstance(asof, str) or not DATE_RE.match(asof):
            finds.add("DD-EVIDENCE", f"sources:{lineno}({sid}) asof 非 YYYY-MM-DD：{asof!r}")
        elif _date_or_none(asof) is None:
            # §v2-15⑦：十个字符的"数字形状"不证明这一天存在（2026-02-30 过词法、不过日历）
            finds.add("DD-EVIDENCE", f"sources:{lineno}({sid}) asof={asof!r} 不是真实存在的日历日（词法形制已过、日历校验不过，§v2-15⑦）——只判形制有效，不判披露事件本身真伪")
        if not isinstance(obj.get("claim"), str) or not obj.get("claim").strip():
            finds.add("DD-EVIDENCE", f"sources:{lineno}({sid}) 缺 claim")
        if kind == "research" and not obj.get("conv_id"):
            finds.add("DD-EVIDENCE", f"sources:{lineno}({sid}) kind=research 须带 conv_id")
        if kind == "user_supplied" and not obj.get("path"):
            finds.add("DD-EVIDENCE", f"sources:{lineno}({sid}) kind=user_supplied 须带 path")
    for ref, ids in out["refs"].items():
        if len(ids) > 1:
            finds.add("DD-EVIDENCE", f"来源锚多重解析：{ref} 同时挂在 {', '.join(ids)}，§2① 要求唯一解析")
    return out


def load_calls(ev_dir: Path, finds: Findings, sink=None):
    """读 <evidence>/calls.jsonl；文件不存在返回空表（由 omission 门按「声称已查却无流水」判）。"""
    raw = read_text(ev_dir / CALLS_NAME)
    if raw is None:
        return []
    if sink is not None:
        sink.extend([ln for ln in raw.splitlines() if ln.strip()])
    out = []
    for lineno, ln in enumerate(raw.splitlines(), start=1):
        if not ln.strip():
            continue
        try:
            obj = json.loads(ln)
        except json.JSONDecodeError as e:
            finds.add("DD-OMISSION", f"{CALLS_NAME}:{lineno} 非合法 JSON 行：{e}——流水不可解析即无法反证漏报")
            continue
        if not isinstance(obj, dict):
            finds.add("DD-OMISSION", f"{CALLS_NAME}:{lineno} 非对象形状")
            continue
        if obj.get("category") not in CATEGORIES:
            finds.add("DD-OMISSION", f"{CALLS_NAME}:{lineno} category {obj.get('category')!r} 不在九类枚举内")
        out.append(obj)
    return out


def load_reasons(report_dir: Path) -> list:
    """progress.md 里的降级理由行：`降级: <类目> | <锚或查询串> | <理由>`。"""
    raw = read_text(report_dir / "progress.md")
    if raw is None:
        return []
    out = []
    for ln in raw.splitlines():
        m = REASON_LINE.match(ln.strip())
        if m:
            out.append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip()))
    return out


def check_evidence_dir(ev_dir: Path, finds: Findings) -> dict:
    info = {"files": {}, "texts": {}, "calls": [], "calls_raw": [], "reasons": []}
    if not ev_dir.is_dir():
        finds.add("DD-EVIDENCE", f"evidence 目录不存在：{ev_dir}（fail-closed，不放行先交付后补证）")
        return info
    info["calls"] = load_calls(ev_dir, finds, info.setdefault("calls_raw", []))
    info["reasons"] = load_reasons(ev_dir.parent)
    snap = sorted(p for p in ev_dir.iterdir() if p.is_file() and p.suffix == ".json")
    if not snap:
        finds.add("DD-EVIDENCE", f"evidence 目录为空：{ev_dir}——表行锚无原始件即不得交付")
        return info
    ledger = ev_dir / "LEDGER.sha256"
    ltext = read_text(ledger)
    if ltext is None:
        finds.add("DD-EVIDENCE", "evidence/LEDGER.sha256 缺失或不可读")
        return info
    listed = {}
    for lineno, ln in enumerate(ltext.splitlines(), start=1):
        if not ln.strip():
            continue
        m = re.match(r"^([0-9a-fA-F]{64})\s+\*?(.+?)\s*$", ln.strip())
        if not m:
            finds.add("DD-EVIDENCE", f"LEDGER.sha256:{lineno} 行形状非法（sha256 + 两空格 + 文件名）")
            continue
        listed[m.group(2)] = m.group(1).lower()
    for p in snap:
        try:
            digest = hashlib.sha256(p.read_bytes()).hexdigest()
        except OSError:
            finds.add("DD-EVIDENCE", f"{p.name} 读取失败")
            continue
        want = listed.get(p.name)
        if want is None:
            finds.add("DD-EVIDENCE", f"{p.name} 未登记在 LEDGER.sha256（台账不全即哈希不可信）")
        elif want != digest:
            finds.add("DD-EVIDENCE", f"hash mismatch：{p.name} 台账记 {want}，实算 {digest}")
        body = read_text(p) or ""
        info["texts"][p.name] = body
        info["files"][p.name] = digest
    for name in listed:
        if name not in info["files"]:
            finds.add("DD-EVIDENCE", f"LEDGER 登记了 {name}，但 evidence 目录内无该件")
    for name in info["texts"]:
        stem = re.sub(r"\.json$", "", name)
        domain = stem.split("-", 1)[0]
        if domain not in KINDS:
            finds.add("DD-EVIDENCE", f"evidence/{name} 前缀域 {domain!r} 不在通道枚举内（命名须 <域>-<slug>.json）")
    return info


def check_anchor_chain(ctx, src, ev, finds: Findings) -> None:
    subj_full = ctx.get("subject_full")
    subj_code = ctx.get("subject_code")
    refs = src.get("refs", {})
    texts = ev.get("texts", {})
    for r in ctx.get("row_anchors", []):
        ln, anchor = r["lineno"], r["anchor"]
        if r["anchor"] in ("", "—", "-", "－", "无", "N/A", "n/a"):
            continue
        if ANCHOR_STATUTE.match(anchor):
            continue  # 法定推导行由 DD-STATUTE 逐字验原文，不套「锚串逐字出现在快照」这条
        if anchor not in refs:
            finds.add("DD-EVIDENCE", f"第 {ln} 行：锚 {anchor} 在 sources.jsonl 不可解析（无对应记录）")
        hit_files = [name for name, body in texts.items() if anchor in body]
        if not hit_files:
            finds.add("DD-EVIDENCE", f"第 {ln} 行：表行锚 {anchor} 缺对应 evidence 原始件（目录非空不等于证据闭环）")
            continue
        bodies = "\n".join(texts[n] for n in hit_files)
        subjects_named = {f"{m.group(1)}（{m.group(2)}）" for m in SUBJECT_TOKEN.finditer(bodies)}
        sec_full, sec_code = subj_full, subj_code
        if r.get("section_subject"):
            tok = SUBJECT_TOKEN.search(r["section_subject"])
            if tok:
                sec_full, sec_code = tok.group(1), tok.group(2)
        ok = bool(sec_full and sec_full in bodies) or bool(sec_code and sec_code in bodies)
        if not ok and sec_full is None:
            # §v2-4：纯代码形制的 subject——归属只能由证据内「同一代码的全称+代码双标」完成
            dual = {f"{m.group(1)}（{m.group(2)}）" for m in SUBJECT_TOKEN.finditer(bodies) if m.group(2) == sec_code}
            if not dual:
                finds.add("DD-ROW", f"第 {ln} 行：--subject 为纯代码形制 {sec_code}，证据内无同代码的「全称+代码」双标（实见 {'、'.join(sorted(subjects_named)) or '无'}）——归属不明")
                continue
            ok = True
        if not ok:
            near = [s for s in subjects_named if sec_full and (s[:2] == sec_full[:2] or sec_full[:3] in s)]
            if len(subjects_named) >= 2 and near:
                finds.add("DD-ROW", f"第 {ln} 行：主体归属不唯一/简称撞号——evidence 内命中 {len(subjects_named)} 个近似全称（{('、'.join(sorted(near)))}），不得取第一个模糊命中")
            elif subjects_named:
                finds.add("DD-ROW", f"第 {ln} 行：evidence 主体与 subject（{sec_full or sec_code}）不一致（实为 {'、'.join(sorted(subjects_named))}）——命令行 subject 不覆盖证据全称")
            else:
                finds.add("DD-ROW", f"第 {ln} 行：evidence 未出现主体全称或代码 {sec_full or sec_code}，归属不可判")


def check_statute(ctx, ev, src, finds: Findings) -> None:
    """§v2-3 法定推导三元绑定：(a) 锚对应唯一 kind=statute 记录；(b) 三件逐字共现在该记录对应的同一 evidence 件；(c) 另有主体侧条件锚及其证据。缺任一=拒推不落行。"""
    texts = ev.get("texts", {})
    derived = ctx.get("derived_rows", [])
    if not derived:
        return
    cond_refs = [m.group(1) for m in DERIVE_CONDITION_LINE.finditer(ctx["text"])]
    subj_full, subj_code = ctx.get("subject_full"), ctx.get("subject_code")
    for idx, r in enumerate(derived):
        ln, anchor = r["lineno"], r["anchor"]
        if not ANCHOR_STATUTE.match(anchor or ""):
            finds.add("DD-STATUTE", f"第 {ln} 行：法定期限推导行未挂 statute 原文锚（锚={anchor!r}）——按 §2 拒推不落行，progress 记理由与探针清单")
            continue
        m = re.match(r"^statute[:：]《([^》]{2,40})》(第[0-9一二三四五六七八九十百]{1,6}条)（([^）]{2,40})）$", anchor)
        law, article, quote = m.group(1), m.group(2), m.group(3)
        recs = src.get("records", {}).get(anchor, [])
        statute_recs = [x for x in recs if x.get("kind") == "statute"]
        if not recs:
            finds.add("DD-STATUTE", f"第 {ln} 行：statute 锚在 sources 无记录，原文不可核——拒推不落行")
            continue
        if len(statute_recs) != 1:
            finds.add("DD-STATUTE", f"第 {ln} 行：推导锚对应的 sources 记录须唯一且 kind=statute（实得 {len(statute_recs)} 条，kind 集 {sorted({str(x.get('kind')) for x in recs})}）——登记在别的域上不构成法定原文锚")
            continue
        sid = statute_recs[0]["id"]
        bound = [n for n in texts if re.sub(r"\.json$", "", n).split("-", 1)[0] == "statute" and re.sub(r"\.json$", "", n).split("-", 1)[-1] == sid]
        if not bound:
            finds.add("DD-STATUTE", f"第 {ln} 行：statute 记录 {sid} 无对应 evidence 件（命名须 statute-{sid}.json）——原文不可逐字取回即拒推")
            continue
        hit = None
        for n in bound:
            for rec in records_of(texts[n]):
                r = _norm(rec)
                missing = [tok for tok in (f"《{law}》", article, quote) if _norm(tok) not in r]
                if not missing:
                    hit = (n, None)
                    break
            if hit:
                break
        if not hit:
            # 报最接近的那件缺了什么，便于回改
            for n in bound:
                recs = [records_of(texts[n])[i] if i < len(records_of(texts[n])) else "" for i in range(len(records_of(texts[n])))]
                best = min((([t for t in (f"《{law}》", article, quote) if _norm(t) not in _norm(rc)], rc) for rc in recs),
                           key=lambda x: len(x[0]))
                finds.add("DD-STATUTE", f"第 {ln} 行：法名/条号/短引三件未落在**同一条法条记录**内（{n} 内最近一条仍缺 {('、'.join(best[0]) or '（无）')}）"
                                        "——整份 JSON 当词袋、或从另一部法的记录里借字，都不算原文在场（§v2-3(b)）")
                break
            continue
        if idx >= len(cond_refs):
            finds.add("DD-STATUTE", f"第 {ln} 行：缺「推导条件: <锚>」行——法条在场不等于本主体本次条件可判（§v2-3(c)：须另有报告期/成立日/方案日等触发事实锚）")
            continue
        cond = cond_refs[idx]
        crecs = src.get("records", {}).get(cond, [])
        if not crecs:
            finds.add("DD-STATUTE", f"第 {ln} 行：推导条件锚 {cond} 在 sources 不可解析——条件不可判即不落行")
            continue
        csid = crecs[0]["id"]
        cfiles = [n for n in texts if re.sub(r"\.json$", "", n).split("-", 1)[-1] == csid]
        if not cfiles:
            finds.add("DD-STATUTE", f"第 {ln} 行：推导条件锚 {cond} 无对应 evidence 原始件")
            continue
        # 先按条件锚定位到那条记录，再在该记录内核主体双标与在场日期（同文件他主体的记录不借光）
        located = [rc for n in cfiles for rc in records_of(texts[n]) if cond in rc]
        if not located:
            finds.add("DD-STATUTE", f"第 {ln} 行：推导条件锚 {cond} 在其 evidence 件内定位不到对应记录——条件不可核即不落行（§v2-3(c)）")
            continue
        ok_rec = any(((subj_full and subj_full in rc) or (subj_code and subj_code in rc)) and re.search(r"\d{4}-\d{2}-\d{2}", rc) for rc in located)
        if not ok_rec:
            named = sorted({f"{m.group(1)}（{m.group(2)}）" for rc in located for m in SUBJECT_TOKEN.finditer(rc)})
            finds.add("DD-STATUTE", f"第 {ln} 行：条件锚 {cond} 对应记录的主体不是 {subj_full or subj_code}（记录内实见 {'、'.join(named) or '无全称'}）"
                                    "——同文件里别处出现本主体字样不算条件可判")


# §v2-10：调用流水与降级理由行的形制
CALLS_NAME = "calls.jsonl"
CALL_FIELDS = ("seq", "category", "domain", "query", "hits", "snapshot", "snapshot_sha256", "prev_sha256")  # §v2-15③
REASON_LINE = re.compile(r"^-?\s*降级[:：]\s*([^|，,]+?)\s*[|，,]\s*([^|，,]+?)\s*[|，,]\s*(\S.*)$")


def check_omission(ledger_rows, ev, finds: Findings) -> None:
    """§v2-10 反沉默漏报（题单 §0.3 明写此码**不得折回 DD-COVERAGE**）：
    `DD-COVERAGE` 管账的形制、枚举与账↔正文计数；本函数管「原始流水 → 交付」的因果断链——
    每类「检到 N/零条」不得低于流水原始命中 M，N<M 须逐条降级理由行（窗外/归属不判/非本主体）进 progress.md。"""
    calls = ev.get("calls", [])
    reasons = ev.get("reasons", [])
    # §v2-15③：三角闭合的结构面——流水八字段齐、hits 为非负整数、domain↔快照文件名域前缀互证。
    # 边界照 §7.8：这里只证结构与哈希自洽，不宣称能挡"整链重写"（外部锚是服务端回执与人工抽 3 对原文）。
    for i, c in enumerate(calls, start=1):
        lack = [k for k in CALL_FIELDS if k not in c or c.get(k) in (None, "")]
        if lack:
            finds.add("DD-OMISSION", f"流水第 {i} 行缺字段 {('、'.join(lack))}——八字段缺一即三角不可核（§v2-15③）")
        h = c.get("hits")
        if not isinstance(h, int) or isinstance(h, bool) or h < 0:
            finds.add("DD-OMISSION", f"流水第 {i} 行 hits={h!r} 非非负整数——原始命中 M 缺失或被改写成文本，M↔N 无从互校（§v2-15③）")
        dom, snap = str(c.get("domain") or ""), str(c.get("snapshot") or "")
        if dom and snap and not re.sub(r"\.json$", "", snap).startswith(dom + "-"):
            finds.add("DD-OMISSION", f"流水第 {i} 行 domain={dom} 与快照 {snap} 的域前缀不互证——调用与被称的原始件对不上（§v2-15③）")
    flow_cats = {str(c.get("category") or "") for c in calls}
    flow_domains: dict[str, set[str]] = {}
    for c in calls:
        flow_domains.setdefault(str(c.get("category") or ""), set()).add(str(c.get("domain") or ""))
    for cat, v in ledger_rows.items():
        domains, _defect = parse_called(v["called"])
        if cat in flow_cats and not domains:
            finds.add("DD-OMISSION", f"「{cat}」流水内有该类原始调用，账却写「本次实际调用={v['called']}、结果={v['result']}」——真实调用不能事后抹成无工具/未发起（§v2-15③）")
            continue
        # §v2-16②：三角最后一条边——账内域集合须**等于**该类流水的 domain 集；"属合法枚举"不等于"就是它调的那个域"
        if domains and cat in flow_domains and domains != flow_domains[cat]:
            finds.add("DD-OMISSION", f"「{cat}」账记本次实际调用={('、'.join(sorted(domains)))}，而该类流水的 domain 集是 {('、'.join(sorted(flow_domains[cat])))}——域集合必须相等，合法域之间的错配与漏记都是断链（§v2-16②，只判结构相等，不判来源真假）")
    for cat, v in ledger_rows.items():
        res = v["result"]
        m = re.fullmatch(r"检到\s*(\d+)", res)
        if not m and res != "零条":
            continue                       # 「无工具」与非法写法各有别的门
        if v["called"] not in KINDS and not parse_called(v["called"])[0]:
            # 未发起/无工具：进门归 §v2-2，不在这里重复发码。合法连记号集合同样放行——
            # 否则「写两个域」反而绕过 §v2-10 的 M↔N 反证，多域登记就成了漏报的后门
            continue
        n = int(m.group(1)) if m else 0
        mine_calls = [c for c in calls if c.get("category") == cat]
        if not mine_calls:
            finds.add("DD-OMISSION", f"「{cat}」账上记 {res}（本次实际调用={v['called']}），但 {CALLS_NAME} 内无该类目的查询流水"
                                     "——声称查过却无流水即不可反证（§v2-10）")
            continue
        hits = sum(int(c.get("hits", 0) or 0) for c in mine_calls)
        if hits > n:
            need = hits - n
            mine = [r for r in reasons if r[0] == cat]
            if len(mine) < need:
                finds.add("DD-OMISSION", f"「{cat}」账记 {res}，而调用流水的原始命中 M={hits}：差的 {need} 条须逐条写降级理由行"
                                          "（窗外 / 归属不判 / 非本主体）进 progress.md——无理由归零=「多查少写」出门（§v2-10）")
                continue
            for k, (_rcat, _ref, why) in enumerate(mine[:need], start=1):
                if not any(w in why for w in ("窗外", "归属", "非本主体", "不判")):
                    finds.add("DD-OMISSION", f"「{cat}」第 {k} 条降级理由 {why!r} 不属三类合法理由（窗外/归属不判/非本主体）")


def check_calls_chain(ev, finds: Findings) -> None:
    """流水链：`seq` 连续 + 每行 `prev_sha256` 等于上一行原文摘要。断链/改序/回写前缀都在这道露形。
    边界（§7.8）：链只证同一次交付内自洽，**不防整链重写**——整链伪造的外部锚是服务端回执与人工抽 3 对原文。"""
    raw = ev.get("calls_raw", [])
    prev = "0" * 64
    for i, line in enumerate(raw, start=1):
        c = ev["calls"][i - 1] if i - 1 < len(ev["calls"]) else {}
        if int(c.get("seq") or 0) != i:
            finds.add("DD-OMISSION", f"流水第 {i} 行 seq={c.get('seq')!r} 不连续——流水被增删或改序（§v2-10）")
        if str(c.get("prev_sha256") or "").lower() != prev:
            finds.add("DD-OMISSION", f"流水第 {i} 行的 prev_sha256 与上一行摘要不符——历史行被回写（链只证同次自洽，见 §7.8）")
        prev = hashlib.sha256(line.encode("utf-8")).hexdigest()


def check_calls_ledger(ev, finds: Findings) -> None:
    """流水自身须可反证：每条记录的快照真在场且哈希相符——「删 source/evidence 不消除流水」。"""
    texts = ev.get("texts", {})
    for i, c in enumerate(ev.get("calls", []), start=1):
        snap = str(c.get("snapshot") or "")
        want = str(c.get("snapshot_sha256") or "").lower()
        if not snap or not re.fullmatch(r"[0-9a-f]{64}", want or ""):
            finds.add("DD-OMISSION", f"流水第 {i} 行缺 snapshot 或 snapshot_sha256（无快照可反证即原始命中数不可信）")
            continue
        body = texts.get(snap)
        if body is None:
            finds.add("DD-OMISSION", f"流水第 {i} 行指向 {snap}，evidence 目录内已无该件——删证据不消除流水（§v2-10）")
        elif hashlib.sha256(body.encode("utf-8")).hexdigest() != want:
            finds.add("DD-OMISSION", f"流水第 {i} 行的快照哈希与 {snap} 现值不符——流水与证据被分开改过即不可信")


def coverage_head_count(lines: list[str]) -> int:
    """§v2-13：全文同名覆盖率节计数（0 / 1 / ≥2）——升级成计数，不再"取第一个"。
    §v2-15④：围栏内的同名标题是示例文本，不参与计数。"""
    mask = fence_mask(lines)
    return sum(1 for i, ln in enumerate(lines) if not mask[i] and COVERAGE_HEADING.match(ln))


def coverage_section_lines(lines: list[str]) -> tuple[list[str], str]:
    """定位覆盖率说明节，返回 (节内正文行, 形态)。
    形态四值：section=唯一该节已定位 / compact=整篇无 H2-H4 的紧凑交付（可全文扫）/
    missing=有 H2-H4 分节却无覆盖率节（§v2-12 禁止回退全文）/
    duplicate=同名覆盖率节 ≥2（§v2-13 不做首节歧义解决，直接判不可唯一）。"""
    if coverage_head_count(lines) > 1:
        return [], "duplicate"
    mask = fence_mask(lines)
    # 只有 H2-H4 算"分节"；H5/H6 属节内附注——误把 H5/H6 当分节会打死紧凑正路（good-X23 guard）
    sectioned = any(not mask[i] and SECTION_HEADING.match(ln) for i, ln in enumerate(lines))
    out: list[str] = []
    seen = False
    for i, ln in enumerate(lines):
        if mask[i]:
            # §v2-15④：围栏内文本既不作节边界、也不作本节交付行——示例里的申报不是交付申报
            continue
        if ends_section(ln):
            # §v2-14：只有 H2–H4 结束本节；H5/H6 是节内附注，其后的申报仍属本节
            if seen:
                break
            seen = bool(COVERAGE_HEADING.match(ln))
            continue
        if seen:
            out.append(ln)
    if seen:
        return out, "section"
    return out, ("compact" if not sectioned else "missing")


def check_age_declaration(ctx, calls, report: Path, finds: Findings) -> None:
    """§v2-11：窗口跨度超过类目检索面已知上限、且本次实调 disclosure_cn 类目账时，
    覆盖率说明节必须带且只带一行可复算的账龄申报；缺行、窗错写或 beyond 被洗成否定=DD-COVERAGE。"""
    span = (ctx["asof"] - ctx["start"]).days
    if span <= AGE_CAP_DAYS or "disclosure_cn" not in calls:
        return
    if finds.has_code("DD-INPUT"):
        # 参数/形制门优先：标题窗与参数本就不一致时，requested 无从两头对齐，不在此重复发码（同 §v2-2 对 DD-EVIDENCE 的静音规矩）
        return
    want = f"{ctx['start'].isoformat()}~{ctx['asof'].isoformat()}"
    body, kind = coverage_section_lines(ctx["lines"])
    if kind == "duplicate":
        return  # 同名节 ≥2 由 check_coverage() 统一发码（§v2-13），此处不重复出码
    if kind == "missing":
        # §v2-12（M94 blocker）：有分节却没定位到覆盖率节 → 禁止回退全文；申报写在别节＝本节缺失
        finds.add("DD-COVERAGE", f"交付物有分节却未定位到「覆盖率与未检到」节（0–3 前导空格的 ATX 标题已按 CommonMark 识别），且窗口实跨 {span} 天 > 类目检索面 {AGE_CAP_DAYS} 天——不回退全文扫申报行：申报放在别的节里等于本节缺失（§v2-12）")
        return
    if kind == "compact":
        # 紧凑件全文扫，但围栏内仍是示例文本，不算交付申报（§v2-15④）
        body = [ctx["lines"][i] for i in body_indices(ctx["lines"])]
    # 先收：按归一前缀收集**本节内全部**原始申报行（伪行也要被收进来），再判数量，最后才解析唯一一行
    raw = [ln.strip() for ln in body if DECL_PREFIX_LOOSE.match(ln) or _norm(ln).startswith("类目账龄申报:")]
    template = f"类目账龄申报: requested={want} | disclosure_cn={AGE_CAP_DAYS}d | beyond={AGE_REQUIRED_BEYOND}"
    if not raw:
        finds.add("DD-COVERAGE", f"窗口实跨 {span} 天 > 本件已知类目检索面 {AGE_CAP_DAYS} 天，且本次实调 disclosure_cn 类目账，但覆盖率节无账龄申报行——短类目账不得静默冒充标题长窗账（§v2-11）；应带：{template}")
        return
    if len(raw) > 1:
        unparsed = [ln for ln in raw if not AGE_DECL_LINE.match(ln)]
        dirty = [ln for ln in raw if any(w in ln for w in AGE_LAUNDER)]
        note = ""
        if unparsed:
            note += f"；形制不合法的一行：{unparsed[0][:64]}"
        if dirty:
            note += f"；带否定/积极措辞的一行：{dirty[0][:64]}"
        finds.add("DD-COVERAGE", f"覆盖率节出现 {len(raw)} 行账龄申报，§v2-11 要求带且只带一行——伪行不得借「解析失败所以不算」出门（先收后判：按归一前缀收原始行，行数须恰为 1）{note}")
        return
    m = AGE_DECL_LINE.match(raw[0])
    if not m:
        finds.add("DD-COVERAGE", f"唯一申报行形制不合法：{raw[0][:70]}——须逐字承载 requested=<复算窗>、disclosure_cn=<数字>d、beyond=<措辞> 三段，单位只认数字+d 形制（写成「日」等变体不认，§v2-11）；应带：{template}")
        return
    req = f"{m.group(1)}~{m.group(2)}"
    if req != want:
        finds.add("DD-COVERAGE", f"账龄申报 requested={req} 与参数复算窗 {want} 不一致（§v2-11：标题窗是用户请求窗，申报行不得改写过窗）")
    cap = int(m.group(3))
    if cap != AGE_CAP_DAYS:
        # §v2-15①：三段一律核**等值**，「不高于」不能替代「等于」——写低到 1d 与写高到 730d 同罪
        finds.add("DD-COVERAGE", f"账龄申报写 disclosure_cn={cap}d，本件契约常量为恰好 {AGE_CAP_DAYS}d——写高是凭据不足，写低是把已知上限伪装成更小事实（§v2-15①）；应逐字为 disclosure_cn={AGE_CAP_DAYS}d")
    beyond = norm_cell(m.group(4))
    laundered = [w for w in AGE_LAUNDER if w in beyond]
    if laundered:
        finds.add("DD-COVERAGE", f"账龄申报 beyond={beyond!r} 命中否定/积极措辞（{('、'.join(laundered))}）——把「机器尚不能互校」写成结论即洗白（§v2-11）")
    elif beyond != AGE_REQUIRED_BEYOND:
        finds.add("DD-COVERAGE", f"账龄申报 beyond={beyond!r} 偏离权威式样（须逐字 {AGE_REQUIRED_BEYOND!r}，§v2-11）")


def check_coverage(report: Path, ctx, tables, finds: Findings, ev=None) -> None:
    dup = coverage_head_count(ctx["lines"])
    if dup > 1:
        # §v2-13：同名覆盖率节须恰为 1；≥2 不做"取首节"的歧义解决，整类跨节重复/首节遮蔽一次封掉
        finds.add("DD-COVERAGE", f"交付物内有 {dup} 个同名覆盖率节（§v2-13：计数须恰为 1）——不取首节、不作歧义解决：重复节让「带且只带一行」失去唯一作用域，第二节既可藏洗白行也可逃节内计数")
    cov_path = report.parent / "references" / "coverage-map.md"
    text = read_text(cov_path)
    if text is None:
        finds.add("DD-COVERAGE", f"覆盖率对账表缺失或不可读：{cov_path}（§5 随 run 交，机器可核）")
        return
    ledger_lines = text.splitlines()
    ledger_mask = fence_mask(ledger_lines)  # §v2-16③：独立账文件同用一把尺——整表被围栏包住＝没有真账
    rows: dict[str, dict] = {}
    dupes: list[str] = []
    header_seen = sep_seen = False   # §v2-15②：先认表（五列表头+分隔行），再认九类
    header_hits: list[int] = []
    near_headers: list[str] = []
    bad_sep: list[str] = []
    bad_rows: list[str] = []
    stray: list[str] = []
    for n, ln in enumerate(ledger_lines, start=1):
        if ledger_mask[n - 1]:
            continue        # §v2-16③：围栏内的账表行是示例文本，独立账文件同此口径
        if not ln.strip().startswith("|"):
            continue
        cells = [norm_cell(c) for c in split_pipe(ln)]
        looks_like_header = "类目" in cells and "结果" in cells
        if looks_like_header and len(cells) >= 5 and cells[0] == "类目":
            header_hits.append(n)
            if cells != list(LEDGER_HEADER):
                near_headers.append(f"第 {n} 行列数 {len(cells)}、列名 {cells}")
                continue
            header_seen, sep_seen = True, False
            continue
        if looks_like_header and cells != list(LEDGER_HEADER):
            near_headers.append(f"第 {n} 行（列序或列名不符，实为 {cells}）")
            continue
        if is_sep_row(cells):
            if header_seen:
                if len(cells) != len(LEDGER_HEADER):
                    bad_sep.append(f"第 {n} 行 {len(cells)} 列")
                else:
                    sep_seen = True
            continue
        if len(cells) < 5:
            continue
        if not (header_seen and sep_seen):
            stray.append(cells[0])   # §v2-15②：没先认表就把管道行当账——不猜
            continue
        if len(cells) != len(LEDGER_HEADER):
            bad_rows.append(f"「{cells[0]}」行 {len(cells)} 列")   # §v2-16①：不静默截断第六格
            cells = cells[:len(LEDGER_HEADER)]
        if cells[0] in rows:
            dupes.append(cells[0])
            continue
        rows[cells[0]] = {"need": cells[1], "called": cells[2], "result": cells[3], "note": cells[4]}
    if len(header_hits) > 1:
        finds.add("DD-COVERAGE", f"覆盖率账出现 {len(header_hits)} 张表头（第 {'、'.join(str(h) for h in header_hits)} 行）——一交付须恰一张完整五列账表，第二表头不得重置识别状态（§v2-16①）")
    for msg in near_headers:
        finds.add("DD-COVERAGE", f"覆盖率账表头不合法：{msg}——须恰为五列且顺序精确「{' | '.join(LEDGER_HEADER)}」，集合包含不证明顺序与宽度（§v2-16①）")
    for msg in bad_sep:
        finds.add("DD-COVERAGE", f"分隔行与表头列数不等：{msg}（表头 {len(LEDGER_HEADER)} 列）——每个 cell 像分隔符不等于同列数（§v2-16①）")
    for msg in bad_rows:
        finds.add("DD-COVERAGE", f"数据行列数不等于表头：{msg}——多出的列不得被静默忽略（§v2-16①）")
    if not header_hits and not near_headers:
        finds.add("DD-COVERAGE", "覆盖率账不是合法的一张表：缺固定五列表头行（类目/所需域·工具/本次实际调用/结果/注记）——先认表再认类（§v2-15②）")
    elif header_seen and not sep_seen and not bad_sep:
        finds.add("DD-COVERAGE", "覆盖率账缺分隔行：五列表头后必须有同列数的分隔行，否则数据行不具表身份（§v2-15②）")
    if stray:
        finds.add("DD-COVERAGE", f"表身份未成立却有 {len(stray)} 行账数据行（{'、'.join(stray[:3])}）——散落管道行不猜成合法账（§v2-15②）")
    for cat in sorted(c for c in rows if c not in CATEGORIES):
        finds.add("DD-COVERAGE", f"覆盖率账出现类目集合外的「{cat}」——九类须恰为九项、每项一次，无第十项（§v2-15②）")
    for cat in sorted(set(dupes)):
        finds.add("DD-COVERAGE", f"「{cat}」在对账表里出现多行——九类须逐类唯一（§v2-2）")
    for cat in CATEGORIES:
        if cat not in rows:
            finds.add("DD-COVERAGE", f"九类覆盖账缺「{cat}」记录——未列类目不等于零条（§5 逐类留账）")
    if not [c for c, v in rows.items() if v["result"] == "无工具" or "域面外" in v["note"]]:
        finds.add("DD-COVERAGE", "对账表无任何「域面外/无工具」明示（§5 要求每类目至少一行，本件公开面必有能力边界）")
    ev_texts = (ev or {}).get("texts", {})
    calls: set[str] = set()
    for cat, v in rows.items():
        if not re.fullmatch(r"(检到\s*\d+|零条|无工具)", v["result"]):
            finds.add("DD-COVERAGE", f"「{cat}」结果列 {v['result']!r} 不在 检到 N|零条|无工具 封闭枚举内（「未发起」只许写在 progress.md，§v2-2）")
            continue
        if v["result"] == "无工具":
            if "域面外" not in v["note"] and "人工" not in v["note"]:
                finds.add("DD-COVERAGE", f"「{cat}」标无工具却未注明域面外/需人工——无工具不等于不存在")
            continue
        called = v["called"]
        if called in ("", "—", "-", "－"):
            finds.add("DD-COVERAGE", f"「{cat}」记 {v['result']} 但「本次实际调用」为空——未发起不得写成零条（§v2-2①，闭 B1 空门）")
            continue
        domains, defect = parse_called(called)
        if defect:
            finds.add("DD-COVERAGE", f"「{cat}」的本次实际调用 {defect}（§v2-16②：只认单记号或以中文顿号紧连的不重复记号集，逐记号须∈域枚举）")
            continue
        calls |= domains
        m0 = re.fullmatch(r"检到\s*(\d+)", v["result"])
        if (m0 and int(m0.group(1)) == 0) or v["result"] == "零条":
            # §v2-2②：零条目也须有对应域的原始快照；哈希类缺陷已由 DD-EVIDENCE 承担，不在此重复发码
            if not finds.has_code("DD-EVIDENCE"):
                for dom in sorted(domains):   # 多域登记=每域各须有自己的原始件，写两个域不能只交一份快照
                    bound = {n: b for n, b in ev_texts.items() if re.sub(r"\.json$", "", n).split("-", 1)[0] == dom}
                    if not bound:
                        finds.add("DD-COVERAGE", f"「{cat}」记 {v['result']} 但 evidence 内无 {dom} 域的原始结果快照——零条目亦须可核（§v2-2②）")
                    elif not any(cat in b for b in bound.values()):
                        finds.add("DD-COVERAGE", f"「{cat}」记 {v['result']} 但 {dom} 域快照内未标出该类目——调用与账目对不上（§v2-2②）")
    # §v2-15③：长窗触发源不得仅采可被改成「无工具」的账表——流水里真实调过的域并入触发集（洗成无工具也照样要求申报）
    flow_domains = {str(c.get("domain") or "") for c in (ev or {}).get("calls", [])}
    check_age_declaration(ctx, calls | flow_domains, report, finds)
    counts: dict[str, int] = {}
    for t in tables:
        for r in t["rows"]:
            counts[r["category"]] = counts.get(r["category"], 0) + 1
    # M73-B1：两侧都要比。只遍历「正文有的类目」会漏掉账写 N>0 而正文零行的反向谎报。
    if tables and not finds.has_code("DD-TABLE"):
        # 表本身被判否时不做两侧计数互校（形制门优先，同 §v2-2 对 DD-EVIDENCE 的静音规矩）
        for cat, v in rows.items():
            m = re.fullmatch(r"检到\s*(\d+)", v["result"])
            n_body = counts.get(cat, 0)
            if m and int(m.group(1)) != n_body:
                finds.add("DD-COVERAGE", f"「{cat}」对账表记「检到 {m.group(1)}」而正文实有 {n_body} 行——两侧逐类必比（§v2-10 反向计数）")
            if v["result"] in ("无工具", "零条") and n_body:
                finds.add("DD-COVERAGE", f"「{cat}」对账表记 {v['result']} 但正文有 {n_body} 行——无工具/零条项禁入正文断言")
    fence_c = ctx.get("fence") or fence_mask(ctx["lines"])
    body_rows = [i for i, inside in enumerate(fence_c) if not inside]
    # §v2-16③：足行只在可交付正文里认——围栏内的示例足行既不抵真足行，也不该被拿去做未知域诊断
    found = [m for m in (SECTION_DOMAIN_LINE.search(ctx["lines"][i]) for i in body_rows) if m]
    dom_lines = [i for i in body_rows if SECTION_DOMAIN_LINE.search(ctx["lines"][i])]
    # §v2-15⑥：足行按"表所在节"核唯一——每节恰一行，同节堆两行互相竞争、或拿他节那一行抵本节，都 FAIL
    for t in tables:
        lo, hi = section_range(ctx["lines"], max(0, t["start"] - 1))
        n = sum(1 for i in dom_lines if lo <= i < hi)
        if n > 1:
            finds.add("DD-COVERAGE", f"同一节内出现 {n} 行「本节检索域」（该节第 {lo + 1}–{hi} 行）——每节恰一行，两行竞争即本节口径不可唯一（§v2-15⑥）")
        elif n == 0:
            finds.add("DD-COVERAGE", f"第 {t['start']} 行起的七列表所在节内没有「本节检索域」行——别节的足行不能抵本节（§v2-15⑥）")
    if not found:
        finds.add("DD-COVERAGE", "正文缺「本节检索域:X 域 / 无工具项:Y」行（§3 每节末必带，与 §5 对账表互校）")
    for m in found:
        doms = [d.strip() for d in re.split(r"[、,/]", m.group(1)) if d.strip() and d.strip() != "—"]
        bad = [d for d in doms if d not in KINDS]
        if bad:
            finds.add("DD-COVERAGE", f"检索域行列出未知域 {('、'.join(bad))}（域面清单见 references/channel-map.md）")
        stated = int(m.group(2))  # 「N 域」的 N；「无工具项: K」的 K 属本节口径，归人工复核，不做机器互校
        if stated != len(doms):
            finds.add("DD-COVERAGE", f"检索域行写「{stated} 域」而实列 {len(doms)} 域（{('、'.join(doms))}）——计数与列举须一致")
        unknown = [d for d in doms if d in KINDS and calls and d not in calls]
        if unknown:
            finds.add("DD-COVERAGE", f"正文检索域行宣称查过 {('、'.join(unknown))}，但对账表「本次实际调用」集里没有——§v2-2③ 互校要求正文集为账内调用集的子集")
    return rows


def run(ns) -> int:
    finds = Findings()
    report = Path(ns.report)
    ctx = check_inputs(ns, report, finds)
    if not ctx and finds.items:
        return _finish(finds, report)
    text = ctx["text"]
    tables = parse_tables(text.splitlines(), finds)
    if not tables:
        finds.add("DD-TABLE", "交付物内未找到任何固定七列表（无表=无清单；零行表合法但须有表头与逐类零结果证据，§v2-2）")
    src_path = Path(ns.sources)
    src = check_sources(src_path, finds)
    check_rows(tables, ctx, finds, src)
    # §v2-1：红线扫交付面四件的全部文字（progress.md 存在才扫）
    cov_path = report.parent / "references" / "coverage-map.md"
    prog_path = report.parent / "progress.md"
    deliverables = [
        ("report.md", text),
        ("sources.jsonl", read_text(src_path) or ""),
        ("references/coverage-map.md", read_text(cov_path) or ""),
        ("progress.md", read_text(prog_path) or ""),
    ]
    check_redlines(deliverables, finds)
    ev = check_evidence_dir(Path(ns.evidence), finds)
    check_anchor_chain(ctx, src, ev, finds)
    check_statute(ctx, ev, src, finds)
    ledger_rows = check_coverage(report, ctx, tables, finds, ev) or {}
    if not finds.has_code("DD-EVIDENCE"):
        # 证据面本身塌了时由 DD-EVIDENCE 承担，不在此重复发码（题单逐题单码要求）
        check_calls_chain(ev, finds)
        check_calls_ledger(ev, finds)
        check_omission(ledger_rows, ev, finds)
    return _finish(finds, report)


def _finish(finds: Findings, report: Path) -> int:
    if finds.items:
        codes = []
        for item in finds.items:
            c = ecode(item)
            if c not in codes:
                codes.append(c)
            print(f"[{c}] {item}")
        print("码表: " + "; ".join(f"{c}→{E_LEGEND[c]}" for c in codes))
        print(f"RESULT: FAIL {report}（{len(finds.items)} 项；码集 {', '.join(sorted(finds.codes))}）")
        return 1
    print(f"RESULT: PASS {report}（八道门禁全过）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True, description="dd-checklist 交付物门禁")
    ap.add_argument("report", nargs="?", default=None, help="report.md 路径")
    ap.add_argument("--subject", default=None)
    ap.add_argument("--asof", default=None)
    ap.add_argument("--lookback", default=None)
    ap.add_argument("--purpose", default=None)
    ap.add_argument("--sources", default=None)
    ap.add_argument("--evidence", default=None)
    ns, extra = ap.parse_known_args()
    if extra:
        print(f"DD-INPUT: 无法识别的参数 {extra[:3]}——命令行只接受 <report.md> 与六个必传参数，不做部分解析")
        return 1
    if not ns.report:
        print("DD-INPUT: 缺交付物路径参数（report.md）——六参数全必传")
        return 1
    ns.sources = ns.sources or ""
    try:
        return run(ns)
    except Exception as e:  # noqa: BLE001 — 崩溃不算命中，折算 FAIL 诊断
        print(f"DD-INPUT: 门禁内部异常（折算为 FAIL，不以 traceback 代替判定）：{type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
