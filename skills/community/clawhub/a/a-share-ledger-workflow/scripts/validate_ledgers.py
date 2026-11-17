#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A股台账校验器（配合 ashare-ledger-standard 技能）

检查项：
  1. cron ID 真实性  —— 台账里写的 cron ID 是否真实存在于 jobs.json
  2. Markdown 格式   —— 四星号、表格列数不一致等
  3. 必填项缺失      —— 按 0.1 全景表 36 项清单核对
  4. 相对基准完整性  —— 第5步必须有同方向排名表
  5. 隐私边界        —— 候选台账不得含真实持仓数字
  6. 状态表一致性    —— 台账 ↔ 流程状态表 双向（全步骤 第2–8步）
                         A 跨行重复 / B 有台账未登记 / C 第5-7步登记但无台账
  7. 台账 ↔ 门槛数据 —— 正文「相对中位」与 bench.json 的 bench_pt 是否一致
  8. 代码 ↔ 名称     —— 防「张冠李戴」，与行情接口比对
  9. 旧口径残留      —— 台账不得留「成本＋2×ATR」/旧「两阶段各卖50%」/
                        「仓位上限未设定」（与 0.1 全景表自相矛盾）— **全台账**
 10. 权威模板自检    —— 模板是建档唯一权威，模板错 = 之后每条新台账都错
 11. 台账 ↔ 模板     —— 全景表「第7步」组项目名必须与模板一致
                        （防模板改了、台账没跟）

🔴 只报告不修改（--fix-format 仅修格式类：四星号）
🔴 退出码：0 = 全清；1 = 有台账问题 / 有校验项降级未跑 / 模板自检不过
"""
import json
import os
import pathlib
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_guard import FetchResult
# ── 数据根目录（环境变量；未设置即报错，不回落任何具体路径）──────────────
_D = os.environ.get("STOCK_DATA_DIR", "").rstrip("/")
if not _D:
    raise SystemExit(
        "🔴 未设置环境变量 STOCK_DATA_DIR（你的股票数据根目录）。\n"
        '   例：export STOCK_DATA_DIR="$HOME/stock_data"\n'
        "   目录结构见 README「数据目录约定」。"
    )

# ── Hermes 主目录（可选；未设置时依赖它的功能跳过，不报错）──────────────
_H = os.environ.get("HERMES_HOME", "").rstrip("/")


ROOT = pathlib.Path(_D + "/股票台账")
STATUS = ROOT / "流程状态表.md"
CAND = ROOT / "候选"
HOLD = ROOT / "持仓中"
JOBS = pathlib.Path(
    _H + "/cron/jobs.json"
)

# 🔴 降级记录：本应执行的校验因取数失败而没跑上的项。
#    「没校验」≠「校验通过」—— 必须由 main 显式报出。
DEGRADED = []

# ⚪ 跳过记录：因「环境里没配置」而跳过的项（≠ DEGRADED）。
#    没装 Hermes / 没建 cron 的使用者不该被判失败，但**必须看得见被跳过了**，
#    否则「跳过」与「通过」长得一样。
SKIPPED = []

# cron 是否可用（main 按 jobs.json 是否存在设定）。不可用时 cron 相关项整体跳过。
CRON_AVAILABLE = True

# 0.1 全景表：阶段 → 必填项关键词
REQUIRED = {
    "base": ["股票名称", "当前阶段", "档案类型", "建档"],
    "step3": ["产业链环节定位", "入池依据", "移出条件"],
    "step4": ["筛选结论", "横向比较位置"],
    "step5": [
        "原始理由", "核心假设", "传导链", "可观察指标", "失效条件",
        "估值分位", "财务基线", "门槛状态", "用户最担心点", "Q3",
    ],
    # 🔴 三模块：持仓台账必须有这三个模块的全部参数字段，
    # 否则 profit_guard 只能报 NEED_DATA，等于监控失效。
    "step7_modules": [
        "持仓期最高价", "盈利保护一档回撤", "盈利保护二档回撤",
        "亏损保护预警回撤", "亏损保护止跌回撤", "单股仓位上限",
    ],
}

# 🔴 只「字段在」不够 —— 值必须真是用户设定过的数字。
#    代价控制原则：字段缺失→报缺字段；字段在但值是「待商定/待补充」→报未设定。
# 🔴 峰值已从这份清单移除 —— 它由脚本从日K自算（流程规定），
#    不再是「用户需要设定」的东西。要求它手填等于逼用户填客观行情数据。
HOLDING_SET_VALUES = [
    "盈利保护一档回撤", "盈利保护二档回撤",
    "亏损保护预警回撤", "亏损保护止跌回撤", "单股仓位上限",
]

# 🔴 第 9 项：持仓台账「旧口径」黑名单。
#    三模块已取代「成本＋2×ATR」与旧「两阶段各卖 50%」。残留会让台账自相矛盾。
#    合法追溯须同行标「废弃」或「不属于当前流程」。
LEGACY_PATTERNS = [
    (r"2\s*[×xX*]\s*(20\s*日)?\s*ATR", "旧盈利保护公式「成本＋2×ATR」"),
    (r"成本\s*[＋+]\s*2", "旧盈利保护公式「成本＋2×ATR」"),
    (r"两阶段(保护线|卖出|各\s*50%)", "旧「两阶段各卖 50%」结构"),
    (r"第[一二](?:\s*[/／]\s*[一二])?\s*阶段(?:线|保护线)",
     "旧「两阶段」结构（新：一档 −12% 减 1/3、二档 −20% 再减 1/3）"),
    (r"单股(最大)?仓位上限[^。\n]{0,24}(尚未设定|仍未设|未设|待商定)",
     "仓位上限写「未设定」（与全景表冲突）"),
    (r"(尚未设定|仍未设)[^。\n]{0,24}单股(最大)?仓位上限",
     "仓位上限写「未设定」（与全景表冲突）"),
]

# 🔴 实测台账有三种标题风格，必须都认：
#    ① 阿拉伯数字  "## 0. 档案信息"（多数）
#    ② 中文数字    "## 一、方向与逻辑"（如中文数字编号）
#    ③ 无编号      "## Sources" / "## 建档后同步状态"（附属章节）
#    规范只认 ①；②③ 视为「未按标准结构」，但不算数据错误。
SECTION_RE = re.compile(r"^##\s*([0-8])[.、]\s*\S", re.M)
CN_NUM = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
          "六": 6, "七": 7, "八": 8, "九": 9}
CN_RE = re.compile(r"^##\s*([一二三四五六七八九])[、.]\s*\S", re.M)


def detect_structure(text):
    """返回 (数字编号节集合, 是否中文编号, 是否有全景表)"""
    digits = set(SECTION_RE.findall(text))
    cn = CN_RE.findall(text)
    has_panorama = "全景信息表" in text
    return digits, bool(cn), has_panorama


def load_schedule():
    """任务名 → 人类可读时点（用于校验台账时点是否与 cron 一致）

    🔴 原来读不到 jobs.json 就返回 {}，下游 `if not full: continue` 静默跳过
    全部时点校验 —— 看似「无问题」，实际是**校验根本没跑**。
    现在记进 DEGRADED，由 main 明确报出。
    （未配置 cron 的使用者：跳过，由 load_job_ids 记入 SKIPPED，不算失败。）
    """
    if not JOBS.exists():
        return {}
    try:
        data = json.loads(JOBS.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        DEGRADED.append(f"jobs.json 不可读（{type(exc).__name__}: {exc}）"
                        f"→ **时点校验与 cron 引用校验本次未执行**")
        return {}
    jobs = data.get("jobs", data if isinstance(data, list) else [])
    out = {}
    for j in jobs:
        if not isinstance(j, dict) or not j.get("name"):
            continue
        if not j.get("enabled", True):
            continue
        sch = j.get("schedule", {})
        expr = sch.get("expr") or sch.get("at") or ""
        out[j["name"]] = describe_schedule(expr)
    return out


CRON_DESC = {
    "20 8 * * 2,5": "周二/周五 08:20",
    "31 8 * * 1": "周一 08:31",
    "30 20 * * 1-5": "每交易日 20:30",
    "5 20 * * 5": "周五 20:05",
    "12 8 * * 1": "周一 08:12",
    "5 19 * * *": "每交易日 19:05",
    "20 11 * * 1-5": "每交易日 11:20",
    "40 14 * * 1-5": "每交易日 14:40",
}


def describe_schedule(expr):
    if expr in CRON_DESC:
        return CRON_DESC[expr]
    return expr


def check_schedule(text, sched):
    """台账写的时点必须与 cron 实际调度一致"""
    issues = []
    for m in re.finditer(r"^\|[^\n]*cron\s*`([^`\n]+)`[^\n]*$", text, re.M):
        row, ref = m.group(0), m.group(1)
        # 唯一前缀解析
        full = None
        for n in sched:
            if n == ref or n.startswith(ref) or ref in n:
                full = n
                break
        if not full:
            continue
        want = sched[full]
        # 从该行里抽出时点格（第3列）
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        got = cells[2].replace("*", "").strip()
        if not re.search(r"\d{2}:\d{2}", got):
            continue
        # 只在两者都写得出具体时点时比对
        if want in CRON_DESC.values() and want not in got and got not in want:
            issues.append(f"时点不符：台账『{got}』vs cron『{want}』（{ref}）")
    return issues


def load_job_ids():
    """返回 (ids, enabled_ids, names, enabled_names)"""
    if not JOBS.exists():
        # 未配置 cron 的新用户走这里：**跳过**，不是降级、不是失败。
        SKIPPED.append("未配置 cron（找不到 jobs.json）"
                       " → 第1项 cron ID/任务名校验 与 时点校验 已跳过")
        return set(), set(), set(), set()
    try:
        data = json.loads(JOBS.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        # 🔴 原来返回四个空 set，下游「找不到匹配」= 全部 cron 引用静默通过
        DEGRADED.append(f"jobs.json 不可读（{type(exc).__name__}: {exc}）"
                        f"→ **cron ID/任务名校验本次未执行**")
        return set(), set(), set(), set()
    jobs = data.get("jobs", data if isinstance(data, list) else [])
    ids = {j.get("id") for j in jobs if isinstance(j, dict)}
    enabled = {j.get("id") for j in jobs
               if isinstance(j, dict) and j.get("enabled", True)}
    names = {j.get("name") for j in jobs
             if isinstance(j, dict) and j.get("name")}
    enames = {j.get("name") for j in jobs
              if isinstance(j, dict) and j.get("name")
              and j.get("enabled", True)}
    return ids, enabled, names, enames


def check_cron_refs(text, valid, enabled, names, enames):
    """🔴 台账只应写 cron 任务名，不写 ID。
    返回 (写成ID的, 停用的ID, 无效的任务名, 已停用的任务名)"""
    id_refs = set(re.findall(r"cron\s*`([0-9a-f]{12,})`", text))
    bad_ids = sorted(i for i in id_refs if i not in valid)
    off_ids = sorted(i for i in id_refs if i in valid and i not in enabled)
    name_refs = set(re.findall(r"cron\s*`([^`\n]{2,30})`", text))
    name_refs = {n for n in name_refs if not re.fullmatch(r"[0-9a-f]{12,}", n)}

    # ⭐ 允许「唯一前缀」简写：如 `候选监控｜15只候选门槛复查`
    #    是 `候选监控｜15只候选门槛复查（A1+A2必过…）` 的唯一前缀。
    #    简写更易读且不会像 ID 那样失效；歧义（匹配多个）才报错。
    def resolve(n):
        if n in names:
            return n
        cands = [x for x in names if x.startswith(n) or n in x]
        return cands[0] if len(cands) == 1 else None

    bad_names, off_names = [], []
    for n in sorted(name_refs):
        full = resolve(n)
        if full is None:
            bad_names.append(n)
        elif full not in enames:
            off_names.append(f"{n} → {full}（已停用）")
    return bad_ids, off_ids, bad_names, off_names


def check_format(text):
    issues = []
    for m in re.finditer(r"\*{4,}([^*\n]{1,40})\*{4,}", text):
        issues.append(f"四星号强调: {m.group(1)[:24]}")
    # 表格列数不一致（同一表内）
    for block in re.findall(r"((?:^\|.*\|\s*$\n)+)", text, re.M):
        rows = [r for r in block.strip().split("\n")
                if not re.match(r"^\|[\s:|-]+\|$", r.strip())]
        counts = {r.count("|") for r in rows}
        if len(counts) > 1:
            issues.append(f"表格列数不一致: {sorted(counts)}")
    return issues


def check_holding_values(text):
    """🔴 持仓台账的三模块参数：字段在 ≠ 值已设定。

    两种坏状态要分开报：
      - 字段整行缺失        → check_required 已经报了「缺字段」
      - 字段在但值是占位符  → 这里报「未设定」（这才是真正卡住监控的）
    """
    issues = []
    for k in HOLDING_SET_VALUES:
        # 🔴 别锚定到第一格：台账行首格是「第7步」，字段名在第二格。
        #   （旧写法 ^\|[^|]*KEY 把 key 限定在首格，永远匹配不到 → 检查恒真）
        #   另：只认「字段名整格相等」，否则「持仓期最高价」会匹配到
        #   「盈利保护启动条件」行里那段提到它的描述文字。
        row = None
        for ln in text.splitlines():
            if not ln.strip().startswith("|"):
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 2 and cells[1].replace("**", "").replace("*", "").strip() == k:
                row = ln
                break
        if row is None:
            continue                           # 缺字段，交给 check_required
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        val = cells[-1].replace("**", "").replace("*", "").strip()
        if any(b in val for b in ("待商定", "待补充", "待确认", "未设", "—", "⬜")) \
           or not re.match(r"^[¥￥]?\s*\d", val):
            issues.append(f"{k} 未设定（值：{val[:40]}）")
    return issues


def check_required(text, holding_only=False):
    """必填字段检查。

    🔴 step7_modules 只对**持仓台账**生效。
    候选台账还没建仓，不该被要求填峰值/仓位上限 —— 否则全库恒红。
    """
    missing = []
    groups = REQUIRED if holding_only else {
        k: v for k, v in REQUIRED.items() if k != "step7_modules"
    }
    for group, keys in groups.items():
        for k in keys:
            # 找全景表里对应的行
            pat = rf"\|\s*\*?\*?[^|]*{re.escape(k)}[^|]*\*?\*?\s*\|[^\n]*"
            if not re.search(pat, text):
                missing.append(f"{group}:{k}")
    return missing


def check_evidence_source(text):
    """🔴 第4节（可核验数据与证据）必须带来源，否则数值不可追溯。

    起因：多份台账第4节曾是裸数值表，无日期/无 art 编号/无接口名，
    而 validate_ledgers 当时报「全部通过」—— 它只验必填项在不在，不验内容出处。

    判定：第4节内须出现下列任一
      ① ISO 日期 2026-09-30          ② 巨潮 art 编号 AN2026...
      ③ 明写「来源」/「数据来源与口径」  ④ 具体接口名（RPT_/腾讯/东财/前复权…）
    ⚠️ 只看第4节本身，不看全文 —— 免得第8节的日期把无来源的第4节蒙混过关。
    """
    m = re.search(r"^## 4\..*?(?=^## 5\.)", text, re.M | re.S)
    if not m:
        return ["缺第4节 可核验数据与证据"]
    body = m.group(0)
    marks = {
        "日期": re.search(r"20\d\d-\d\d-\d\d", body),
        "art编号": re.search(r"AN\d{15,}", body),
        "来源声明": ("来源" in body),
        "接口名": re.search(r"RPT_[A-Z_]+|腾讯|东财|前复权|qfq|巨潮|新浪", body),
    }
    hit = [k for k, v in marks.items() if v]
    if not hit:
        return ["第4节无任何来源标注（无日期/art编号/来源声明/接口名）→ 数值不可追溯"]
    return []


def check_relative_baseline(text):
    """第5步候选台账必须有同方向排名表（本标的 + 其他标的）

    ⭐ 例外：方向内仅 1 只标的时，可裁定「不做横向对比」，
       台账须写明裁定结论，此时不算缺项。
    🔴 修：豁免原为**全文子串匹配** —— 台账任何位置出现
       「暂不适用」就整份放行（例：§5 写「分红送转口径：暂不适用」
       → 起点基准这一节被静默跳过）。现在豁免必须**自证**：
       该行同时提到「横向对比」。
    """
    if "方向起点基准" not in text and "起点回溯" not in text:
        # 无起点基准章节：只有写明「横向对比」裁定行才放行
        if any(_is_exempt_line(l) for l in text.splitlines()):
            return []
        return ["缺方向起点基准章节"]
    issues = []
    # 🔴 必须用正则找『下一个二级标题』：用 text.find("\n## ") 会在
    #    标题后紧跟空行时立刻命中，导致段长为 1（实测误报）。
    m = re.search(r"方向起点基准|起点回溯", text)
    seg = ""
    if m:
        nxt = re.search(r"^## ", text[m.end():], re.M)
        seg = text[m.start(): m.end() + nxt.start()] if nxt else text[m.start():]
    # 🔴 豁免只在**起点基准章节内**生效
    if any(_is_exempt_line(l) for l in seg.splitlines()):
        return []
    rows = re.findall(r"^\|\s*\d+\s*\|", seg, re.M)
    if len(rows) < 2:
        issues.append("基准表只有本标的，缺同方向其他标的涨幅")
    if "相对中位" not in seg:
        issues.append("缺『相对中位』对比行")
    return issues


def _is_exempt_line(line):
    """豁免必须自证：该行**同时**提到「横向对比」。

    只写「暂不适用」不算 —— 否则台账里任何一处无关的「暂不适用」
    都会把起点基准这一节静默豁免掉（实测到的静默失效）。
    """
    return ("暂不适用" in line or "不做横向对比" in line) and "横向对比" in line


def check_privacy(text, is_holding):
    issues = []
    if is_holding:
        return issues  # 持仓台账本就该有数字
    # 候选台账不得出现真实持仓数字
    for pat, desc in [
        (r"\d{3,6}\s*股(?!\s*（\s*0\s*）)", "疑似真实持股数"),
        (r"加权成本\s*\|\s*\d", "加权成本有真实数值"),
        (r"(已实现|未实现)盈亏\s*\|\s*[-\d]", "盈亏有真实数值"),
    ]:
        if re.search(pat, text):
            issues.append(desc)
    return issues


def parse_status_table():
    """解析流程状态表「在流程中」表格 → [(阶段名, {代码: 名称})]。
    只取 ## 在流程中 到下一个 ## 之间；行必须是 markdown 表格行。"""
    if not STATUS.exists():
        return None
    t = STATUS.read_text(encoding="utf-8")
    i = t.find("## 在流程中")
    if i < 0:
        return None
    j = t.find("\n## ", i + 5)
    block = t[i: j if j > 0 else len(t)]
    rows = []
    for l in block.split("\n"):
        if not l.startswith("|") or l.startswith("| 阶段") or set(l) <= set("|-: "):
            continue
        cells = [c.strip() for c in l.strip("|").split("|")]
        if len(cells) < 2:
            continue
        stage = cells[0]
        # 代码 → 就近取前面的名称
        pairs = {}
        for m in re.finditer(r"([\u4e00-\u9fa5A-Za-z0-9*]+)\s*\((\d{6})\)", cells[1]):
            pairs[m.group(2)] = m.group(1).lstrip("*")
        rows.append((stage, pairs))
    return rows


def check_status_consistency(ledger_codes):
    """流程状态表 ↔ 台账 全步骤一致性（新增，覆盖第2–8步）。

    A. 跨行重复 —— 同一代码出现在多个阶段行
    B. 有台账未登记 —— 候选/持仓台账的代码必须出现在状态表
    C. 登记了但无台账 —— 标「第5步/第6步/第7步」的代码必须有对应台账
    """
    rows = parse_status_table()
    if rows is None:
        return ["流程状态表缺失或无法解析"]
    errs = []
    seen = {}
    for stage, pairs in rows:
        for c in pairs:
            seen.setdefault(c, []).append(stage)
    # A. 跨行重复
    for c, sts in seen.items():
        if len(sts) > 1:
            errs.append(f"🔴 跨行重复登记：{c} 同时出现在 {' ／ '.join(sts)}")
    # B. 有台账未登记
    for c, nm in sorted(ledger_codes.items()):
        if c not in seen:
            errs.append(f"🔴 有台账但流程状态表未登记：{nm}({c})")
    # C. 第5/6/7步登记的代码必须有台账
    for stage, pairs in rows:
        if not re.match(r"^(第[567]步)", stage):
            continue
        for c, nm in pairs.items():
            if c not in ledger_codes:
                errs.append(f"🔴 {stage[:6]} 登记了 {nm}({c})，但无对应台账文件")
    return errs


# ────────────────────────────────────────────────────────────────
# 第 7 项：台账正文 ↔ bench.json 门槛数据 一致性
#   背景：曾实测发现——字典 BENCH 先填 0.0，台账正文却写 −6.93，
#        两者不一致且无任何机制拦截。字典是门槛计算的唯一输入，必须与台账对齐。
#   策略（fail-closed）：
#     · bench.json 里有的标的，台账**必须**能解析出「相对中位」数值 —— 提不到 = 报错，
#       不再静默跳过（旧版 `if not hits: continue` 会让 32 只里只有 2 只被真正校验）；
#     · bench_pt 为 null（方向内无对照）= 台账也不得写数值；
#     · 台账写了基准起止时，必须与 bench.json 的 bench_base 一致，否则报「基准日不符」
#       （口径不同 vs 填错，处置方式完全不同）；
#     · 每次运行回报「实际校验 X / 应有 Y」，跳过必须列名单。
# ────────────────────────────────────────────────────────────────
SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent

# 相对中位数值：容忍表格竖线、加粗、全角负号、加号、pt 前后空格
BENCH_PAT = re.compile(
    r"相对(?:方向)?中位[^|\n]*?\|?\s*\**\s*([\u2212\u2013\u2014\-\uff0d+]?\s*[\d.]+)\s*pt")
BASE_START_RE = re.compile(r"(?:基准起点|起点日)\**\s*[：:]?\s*(\d{4}-\d{2}-\d{2})")
BASE_END_RE = re.compile(r"(?:基准终点|终点日)\**\s*[：:]?\s*(\d{4}-\d{2}-\d{2})")
# （脚本可放在仓库目录、数据放 $STOCK_DATA_DIR，两者不必同处；用脚本自身目录最稳）


def load_gate_dicts():
    """读 $STOCK_DATA_DIR/bench.json 取门槛字典。

    🔴 原先用 ast 解析 candidate_gate.py 里的硬编码字典。数据外抽到 bench.json 后
       （见 README / 打包说明书 §3.2），代码里已没有这些字典 —— 继续 ast 解析只会
       读到空字典，静默跳过一致性校验。「数据在哪」必须与「读哪」同时改。
    """
    f = pathlib.Path(_D + "/bench.json")
    if not f.exists():
        SKIPPED.append(f"未找到门槛数据文件 {f}"
                       f" → 第7项 台账↔字典一致性校验 已跳过"
                       f"（cp templates/bench.example.json 后按你的标的填写）")
        return {}
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        DEGRADED.append(f"bench.json 解析失败（行 {exc.lineno}：{exc.msg}）"
                        f"→ **台账↔字典一致性校验未执行，且门槛脚本已无法运行**")
        return {}
    stock = data.get("stock") or {}
    if not stock:
        DEGRADED.append("bench.json 的 stock 为空 → **台账↔字典一致性校验未执行**"
                        "（所有台账会报 NEED_DATA，等于监控失效）")
        return {}
    return {
        "BENCH":      {c: (v.get("direction"), v.get("bench_pt")) for c, v in stock.items()},
        "BENCH_BASE": data.get("bench_base") or {},
        "PB_PCTL":    {c: v.get("pb_pctl") for c, v in stock.items()},
        "PE_PCTL_3Y": {c: v.get("pe_pctl_3y") for c, v in stock.items()},
        "KF_RATIO":   {c: v.get("kf_ratio") for c, v in stock.items()},
        "A1_BASE":    {c: tuple(v.get("a1") or []) for c, v in stock.items()},
    }


def nums_near(text, kw, window=45):
    """提取 text 中 kw 之后 window 字符内的所有百分比数字（宽松：命中任一即可）。
    ⚠️ 排除门槛定义式（如「扣非占归母≥90%」），只取台账正文的实际值。"""
    out = []
    for m in re.finditer(re.escape(kw), text):
        head = text[max(0, m.start() - 6): m.end()]
        if "\u2265" in head or ">=" in head:      # ≥ / >= 是口径定义，不是实际值
            continue
        seg = text[m.end(): m.end() + window]
        for x in re.finditer(r"([\d.]+)%", seg):
            out.append(float(x.group(1)))
    return out


def check_dict_consistency(files):
    """台账 ↔ bench.json 门槛数据 一致性（fail-closed）。

    🔴 只校验 BENCH（方向内相对中位）一项，原因：
       · PB分位 / PE分位 / 扣非占比 在台账里常「全样本」与「剔首年」并列，
         口径差异会被正则误判为不一致（曾实测十余项误报）；
       · bench_pt 是唯一「单一数值、无口径歧义」的项，也正是实际踩过的坑
         （数据先填 0.0，台账正文写 −6.93，两者不一致却无机制拦截）。

    🔴 提不到数值 = 报错，**不是跳过**。旧版 `if not hits: continue` 会让格式一变
       就整批静默失效 —— 实测 32 只里只有 2 只被真正校验，却照样输出「✅ 通过」。
    返回 (errs, cov)：cov 供 main 打印覆盖率，使「实际校验了几只」永远可见。
    """
    dicts = load_gate_dicts()
    bench = dicts.get("BENCH", {})
    bench_base = dicts.get("BENCH_BASE", {})
    if not bench:
        return [], {}
    errs, skipped = [], []
    checked = 0
    required = sum(1 for v in bench.values() if v[1] is not None)
    for f in files:
        m = re.match(r"(.+?)_(\d{6})_", f.name)
        if not m:
            continue
        name, code = m.group(1), m.group(2)
        if code not in bench:
            continue
        label, want = bench[code]
        t = f.read_text(encoding="utf-8")

        # ── 基准日核对：口径不同 ≠ 填错，分开报 ──
        wb = bench_base.get(label)
        if wb:
            bs, be = BASE_START_RE.search(t), BASE_END_RE.search(t)
            if bs and be:
                if (bs.group(1), be.group(1)) != tuple(wb):
                    errs.append(f"{name}({code}) 基准日不符：台账 "
                                f"{bs.group(1)}→{be.group(1)}，bench.json {wb[0]}→{wb[1]}"
                                f"（口径不同，需重算后统一）")
                    continue
            else:
                skipped.append(f"{name}({code})：台账未写基准起止，无法核对基准日"
                               f"（bench.json 为 {wb[0]}→{wb[1]}）")

        hits = []
        for mm in BENCH_PAT.finditer(t):
            try:
                hits.append(float(mm.group(1).replace("\u2212", "-")
                                  .replace("\u2013", "-").replace("\u2014", "-")
                                  .replace("\uff0d", "-").replace(" ", "")))
            except ValueError:
                pass

        # ── bench_pt 为 null：无对照，台账不得写数值 ──
        if want is None:
            if hits:
                errs.append(f"{name}({code}) 相对中位：bench.json 标「无对照」(null)，"
                            f"台账却写有数值 {hits} —— 请把该行改为「不适用」")
            else:
                skipped.append(f"{name}({code})：方向内无对照，bench_pt = null")
            continue

        try:
            wv = float(want)
        except (TypeError, ValueError):
            continue

        if not hits:
            errs.append(f"{name}({code}) 相对中位：**台账提不到数值**"
                        f"（缺该行或格式不合规；确属无对照请把 bench_pt 写成 null）")
            continue
        checked += 1
        if any(abs(h - wv) <= 0.15 for h in hits):
            continue
        if wv != 0 and all(abs(h) <= 0.15 for h in hits):
            errs.append(f"{name}({code}) 相对中位：台账为**占位 {hits}**，"
                        f"bench_pt={wv:+.2f} → 该行未填")
        else:
            errs.append(f"{name}({code}) 相对中位：台账 {hits} 中无 {wv:+.2f}"
                        f"（bench_pt）→ **数值冲突**")
    cov = {"checked": checked, "required": required, "skipped": skipped}
    return errs, cov


# ────────────────────────────────────────────────────────────────
# 第 8 项：代码 ↔ 名称 绑定（防「张冠李戴」）
#   背景：实测发现——某方向记录整篇用的是另一主体的数据
#        （涨幅 / PB分位 / 半年报披露日 三项独立数据全部与另一主体吻合），
#        错误一路穿透到「排除」结论层面，此前**没有任何机制**拦得住。
#   策略：台账文件名 + 台账/方向记录/流程状态表 正文里的「名称（6位代码）」
#        一律与行情接口比对；取数失败 → DEGRADED（不误报）。
#   ⚠️ 与已有「跨行重复/未登记」校验互补：那项查「有没有登记」，
#      本项查「登记的主体对不对」。
# ────────────────────────────────────────────────────────────────
PROJECT = ROOT.parent
NAME_CACHE = PROJECT / "方向记录" / "数据" / "代码名称映射.json"
NAME_CODE_RE = re.compile(
    r"([\u4e00-\u9fa5][\u4e00-\u9fa5A-Za-z0-9]{1,7})\s*[（(]\s*(\d{6})\s*[）)]")


def _norm_name(s):
    """去掉交易所状态前缀（ST/*ST/XD/XR/DR/N/C/U/W）再比对。"""
    s = (s or "").strip()
    s = re.sub(r"^\*?ST", "", s)
    s = re.sub(r"^(XD|XR|DR|N|C|U|W)", "", s)
    return s.strip()


def _mk_secid(code):
    if not code:
        return None
    if code[0] in "56":
        return "sh" + code
    if code[0] in "03":
        return "sz" + code
    if code[0] in "48":
        return "bj" + code
    return None


def _fetch_names(codes):
    """腾讯行情批量取 代码→名称。任何异常吞掉，返回已取到的部分。"""
    import ssl as _ssl
    import urllib.request
    ctx = _ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = _ssl.CERT_NONE
    got = {}
    codes = [c for c in codes if _mk_secid(c)]
    for i in range(0, len(codes), 40):
        q = ",".join(_mk_secid(c) for c in codes[i:i + 40])
        try:
            req = urllib.request.Request(
                "https://qt.gtimg.cn/q=" + q,
                headers={"User-Agent": "Mozilla/5.0",
                         "Referer": "https://gu.qq.com/"})
            raw = urllib.request.urlopen(
                req, timeout=12, context=ctx).read().decode("gbk", "replace")
        except Exception:
            continue
        for seg in raw.split(";"):
            if "=" not in seg:
                continue
            parts = seg.split("=", 1)[1].strip().strip('"').split("~")
            if len(parts) > 3 and len(parts[2]) == 6 and parts[1]:
                got[parts[2]] = parts[1]
    return got


def check_code_name_binding(files, extra_files=()):
    """返回 (errs, notes)。errs=真不符；notes=行情查不到（仅提示，不计错）。"""
    pairs = []
    for f in files:
        m = re.match(r"(.+?)_(\d{6})_", f.name)
        if m:
            pairs.append((m.group(2), m.group(1), f"台账文件名 {f.name}"))
    for xf in extra_files:
        try:
            t = xf.read_text(encoding="utf-8")
        except Exception:
            continue
        for mm in NAME_CODE_RE.finditer(t):
            pairs.append((mm.group(2), mm.group(1), f"{xf.name} 正文"))
    if not pairs:
        return [], []

    cache = {}
    if NAME_CACHE.exists():
        try:
            cache = json.loads(NAME_CACHE.read_text(encoding="utf-8"))
        except Exception:
            cache = {}
    need = sorted({c for c, _, _ in pairs if c not in cache})
    if need:
        got = _fetch_names(need)
        if not got:
            DEGRADED.append(
                "行情接口取名称失败 → **代码↔名称绑定校验未执行**"
                f"（待核 {len(need)} 个代码：{'、'.join(need[:6])}…）")
            return [], []
        cache.update(got)
        try:
            NAME_CACHE.parent.mkdir(parents=True, exist_ok=True)
            NAME_CACHE.write_text(
                json.dumps(cache, ensure_ascii=False, indent=1, sort_keys=True),
                encoding="utf-8")
        except Exception as exc:
            DEGRADED.append(
                f"名称缓存写入失败（{type(exc).__name__}: {exc}）→ 下次仍会联网")

    errs, notes, seen = [], [], set()
    for code, name, where in pairs:
        cn = cache.get(code)
        if not cn:
            notes.append(f"{name}({code}) ← {where}")
            continue
        a, b = _norm_name(name), _norm_name(cn)
        # a = 文中捕获的名字（可能带前面的连接词）
        # b = 行情接口的官方名。只认三种相符：
        #   ①完全相同 ②官方名以文中名开头 ③官方名是文中名的子串
        #   ⚠️ 不用「文中名是官方名子串」——那会让同名前缀的另一主体误过。
        if a == b or b.startswith(a) or (len(b) >= 2 and b in a):
            continue
        if (code, name) in seen:
            continue
        seen.add((code, name))
        errs.append(f"🔴 张冠李戴：{where} 写「{name}({code})」，"
                    f"但 {code} 实为「{cn}」")
    return errs, notes


def check_legacy_wording(text):
    """🔴 第 9 项：持仓台账「旧口径」黑名单。

    背景：三模块取代了旧「盈利保护＝成本＋2×ATR」与旧「两阶段各卖 50%」。
    实测残留：§0.1 全景表已写新口径，而 §3 价格线／§5 风险／§8 待办仍写旧口径，
    并在同一份文件里既写「仓位上限 10,000 股」又写「尚未设定」—— **同一文件自相矛盾**。
    原有校验只查「字段在不在」，看不见「两处说法打架」，多份台账全绿也照样漏。

    做法：黑名单直接命中即报错 —— 比语义检测便宜且够用。
    ⚠️ 合法提及旧口径必须同行标注「废弃/不属于当前流程」，否则按残留报出。
    """
    errs = []
    for i, line in enumerate(text.splitlines(), 1):
        if "废弃" in line or "不属于当前流程" in line:
            continue                      # 合法追溯说明，放行
        for pat, why in LEGACY_PATTERNS:
            if re.search(pat, line):
                errs.append(f"第{i}行 仍写{why} → {line.strip()[:80]}")
                break
    return errs


# ── 第 10 项：权威模板自检 ───────────────────────────────────────
# 起因：本脚本只扫 候选/ + 持仓中/，**模板从来没被校验过**，
# 于是模板里潜伏了 3 个缺陷：缺 §8 整节、缺「方向起点基准」章节、
# 示例写真实量级股数会触发候选台账隐私拦截（须用 10,000 股等示例值）。而技能写着「只从模板建档」
# —— 模板错 = 之后每条新台账都错，且要到建档时才发现。
TEMPLATE = ROOT / "模板" / "单股跟踪台账_模板.md"

# 把模板占位符换成假值，使其成为一份可比对的「假台账」
TMPL_FILL = [
    ("{股票名称}", "模板自检股"), ("{名称}", "模板自检股"), ("{代码}", "600000"),
    ("{候选跟踪 / 持仓中 / 已清仓}", "候选跟踪"), ("{候选跟踪}", "候选跟踪"),
    ("{1}", "5"), ("{阶段名称}", "跟踪"), ("{YYYY-MM-DD}", "2026-01-01"),
    ("{方向研究启动日}", "2026-01-01"), ("{最近交易日}", "2026-01-02"),
    ("{起点日}", "2026-01-01"), ("{终点日}", "2026-01-02"),
    ("{+X%}", "+1.00%"), ("¥{价}", "¥10.00"),
    ("{名称 代码}", "模板自检股 600000"),
]


def check_template():
    """对权威模板本身做结构与格式自检。

    🔴 **不跑 check_relative_baseline**：模板的示例表只有 1 行（本标的），
       必然触发「基准表只有本标的」。改为**直接断言章节标题存在** ——
       这比那一项更严：check_relative_baseline 的豁免是**全文子串匹配**，
       模板说明文字里出现「暂不适用」就会让整份台账自我豁免（实测踩过，
       已把模板措辞改掉）。
    """
    if not TEMPLATE.exists():
        return [f"找不到权威模板：{TEMPLATE}"]
    raw = TEMPLATE.read_text(encoding="utf-8")
    errs = []

    digits, is_cn, pano = detect_structure(raw)
    if is_cn and not digits:
        errs.append("中文数字编号，未按 0–8 标准结构")
    elif len(digits) < 9:
        errs.append("仅 %d/9 节，缺第 %s 节"
                    % (len(digits), "/".join(sorted(set("012345678") - digits))))
    if not pano:
        errs.append("缺 0.1 全景信息表")
    if "方向起点基准" not in raw and "起点回溯" not in raw:
        errs.append("缺「方向起点基准（方向内相对强弱）」章节"
                    "（校验器对候选台账强制要求）")

    filled = raw
    for a, b in TMPL_FILL:
        filled = filled.replace(a, b)
    errs += [f"格式：{x}" for x in check_format(filled)]
    errs += [f"必填项：{x}" for x in check_required(filled, holding_only=False)]
    errs += [f"隐私：{x}" for x in check_privacy(filled, is_holding=False)]
    errs += [f"证据来源：{x}" for x in check_evidence_source(filled)]
    return errs


# ── 第 11 项：台账 ↔ 模板 结构一致性 ─────────────────────────────
# 全景表「第7步」组项目名的格式（模板与台账同一格式）
P7_ROW_RE = re.compile(
    r"^\|\s*(?:\*\*第7步\*\*)?\s*\|\s*([^|]+?)\s*\|\s*第7步\s*\|", re.M)


def _p7_names(text):
    """取全景表「第7步」组的项目名。"""
    return [m.strip() for m in P7_ROW_RE.findall(text)]


def check_template_conformance(text):
    """台账全景表「第7步」组的项目名必须与权威模板一致。

    起因：模板第7组 7→11 项（三模块）后，**多份候选台账没跟**，
    仍挂着旧口径项目名「盈利保护启动条件」「盈利保护两阶段线」——
    没有任何检查会发现：第9项黑名单只查持仓，且从不比对项目名。
    """
    if not TEMPLATE.exists():
        return []
    tnames = _p7_names(TEMPLATE.read_text(encoding="utf-8"))
    if not tnames:
        return ["模板全景表第7组解析为空（模板结构可能已变）→ 本项未生效"]
    cur = _p7_names(text)
    out = []
    miss = [n for n in tnames if n not in cur]
    extra = [n for n in cur if n not in tnames]
    if miss:
        out.append("全景表第7组缺项：" + "、".join(miss))
    if extra:
        out.append("全景表第7组多出旧项：" + "、".join(extra))
    out += check_section3_cats(text)
    return out


# §3 价格线与计划必须含这 4 类（与模板 §3.2 一致）
S3_CATS = [
    ("买入计划/批次", r"买入计划|批次|第\s*\d\s*批"),
    ("盈利保护", r"盈利保护"),
    ("亏损保护", r"亏损保护"),
    ("加仓建议", r"加仓建议"),
]


def check_section3_cats(text):
    """§3 必须含 4 类价格线条目。

    起因：候选台账里 **多份根本没有 §3.2 小节**，
    只有一张「批次」占位表 —— 没有盈利保护/亏损保护/加仓建议行。
    照模板建档本该有；缺了会让「模块二到底配了没」在台账里看不出来。
    """
    m = re.search(r"^##\s*3[.、].*$", text, re.M)
    if not m:
        return []          # 缺 §3 由结构检查报，本项不重复报
    nxt = re.search(r"^##\s*\d+[.、]", text[m.end():], re.M)
    seg = text[m.start(): m.end() + nxt.start()] if nxt else text[m.start():]
    miss = [name for name, pat in S3_CATS if not re.search(pat, seg)]
    return ["§3 缺条目类别：" + "、".join(miss)] if miss else []


# ────────────────────────────────────────────────────────────────
# 第 12 项：cron 脚本漂移（工作区源 ↔ profile 运行副本）
#   背景：曾实测 —— cron 的 `script` 是相对名，只解析到
#        HERMES_HOME/scripts/（=`<profile>/scripts/`），与 `workdir` 无关。
#        工作区改完不 cp，cron 照跑旧版，而且**每次都记 last_status=ok**
#        → 静默失效。实测过一次：profile 副本精确等于数天前的基线提交，
#        其间落地的整组三模块从未生效。
#   策略：对「两边都存在的同名 .py」逐个比 sha256，不一致即报错。
#        若该文件被某个 no_agent 任务的 script 字段引用、或被其 import，
#        则计为**错误**；否则只提示（避免与 cron 无关的文件制造噪音）。
#        profile 独有的文件只提示（多为废弃包装/孤儿脚本）。
# ────────────────────────────────────────────────────────────────
PROFILE_SCRIPTS = JOBS.parent.parent / "scripts"   # cron/jobs.json → <profile>/scripts


def _load_jobs_raw():
    if not JOBS.exists():
        return None
    try:
        data = json.loads(JOBS.read_text(encoding="utf-8"))
    except Exception:
        return None
    jobs = data if isinstance(data, list) else data.get("jobs", data)
    return list(jobs.values()) if isinstance(jobs, dict) else list(jobs)


def _used_by_cron(name, jobs):
    """该文件名是否被某个 no_agent 任务直接引用，或被其脚本 import。"""
    mod = name[:-3]
    for j in jobs:
        if j.get("script") == name:
            return True
        other = PROFILE_SCRIPTS / str(j.get("script") or "")
        if not other.is_file():
            continue
        try:
            text = other.read_text(encoding="utf-8")
        except Exception:
            continue
        if re.search(rf"^\s*(from\s+{re.escape(mod)}\s+import|import\s+{re.escape(mod)}\b)",
                     text, re.M):
            return True
    return False


def check_script_drift():
    """返回 (errors, notes)。errors 非空 = 存在会让 cron 静默跑旧版的漂移。"""
    import hashlib

    errs, notes = [], []
    if not _H:
        SKIPPED.append("未配置 HERMES_HOME（无 profile 目录）"
                       " → 第12项 脚本漂移校验 已跳过")
        return errs, notes
    if not PROFILE_SCRIPTS.is_dir():
        DEGRADED.append(f"profile scripts 目录不存在：{PROFILE_SCRIPTS}"
                        f" → **第12项 脚本漂移校验未执行**")
        return errs, notes
    jobs = _load_jobs_raw()
    if jobs is None:
        DEGRADED.append(f"读不到 cron/jobs.json（{JOBS}）"
                        f" → **第12项 无法判断哪些文件被 cron 使用，降级为仅提示**")
        jobs = []

    def h(p):
        return hashlib.sha256(p.read_bytes()).hexdigest()

    prof = {p.name: p for p in PROFILE_SCRIPTS.glob("*.py")}
    ws = {p.name: p for p in SCRIPTS_DIR.glob("*.py")}

    for name in sorted(set(prof) & set(ws)):
        if h(prof[name]) != h(ws[name]):
            msg = (f"{name}：profile 副本 {prof[name].stat().st_size}B "
                   f"≠ 工作区源 {ws[name].stat().st_size}B")
            if _used_by_cron(name, jobs):
                errs.append(f"🔴 {msg} —— cron 跑的是 profile 那份，"
                            f"修复：cp {ws[name]} {prof[name]}")
            else:
                notes.append(f"{name} 与工作区不一致，但无 cron 引用（仅提示）")
    for name in sorted(set(prof) - set(ws)):
        notes.append(f"{name} 仅存于 profile（工作区无同名源，多为残留）")
    return errs, notes


def validate_file(path, valid_ids, enabled_ids, names, enames,
                  sched, fix_format=False):
    text = path.read_text(encoding="utf-8")
    is_holding = HOLD in path.parents
    res = {"file": path.name, "stage": "第7步持仓" if is_holding else "第5步候选"}

    if CRON_AVAILABLE:
        bad, off, badn, offn = check_cron_refs(
            text, valid_ids, enabled_ids, names, enames)
        if bad:
            res["cron_id_写法"] = f"🔴 写了 ID（应为任务名）: {bad}"
        if off:
            res["cron_id_失效"] = off
        if badn:
            res["cron_任务名无效"] = badn
        if offn:
            res["cron_已停用"] = offn

    fmt = check_format(text)
    if fmt and fix_format:
        new = re.sub(r"\*{4,}([^*\n]{1,40})\*{4,}", r"**\1**", text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            fmt = [f + "（已修）" for f in fmt]
            text = new
    if fmt:
        res["format"] = fmt

    miss = check_required(text) if is_holding else check_required(text, holding_only=False)
    if miss:
        res["missing"] = miss

    # 🔴 三模块参数必须真有值 —— 只看字段在不在，挡不住「待商定」占位。
    if is_holding:
        hv = check_holding_values(text)
        if hv:
            res["holding_params"] = hv

    # 🔴 第 9 项：旧口径残留。**全台账**跑（修：原来只在
    #    `if is_holding` 里，候选台账的「成本＋2×20日ATR」从未被扫到）。
    lw = check_legacy_wording(text)
    if lw:
        res["legacy_wording"] = lw

    # 🔴 第 11 项：台账 ↔ 模板 结构一致性（全景表第7组项目名）
    tc = check_template_conformance(text)
    if tc:
        res["template_drift"] = tc

    digits, is_cn, has_pano = detect_structure(text)
    if is_cn and not digits:
        res["structure"] = "🔴 中文数字编号，未按 0–8 标准结构"
    elif len(digits) < 9:
        missing_secs = sorted(set("012345678") - digits)
        res["sections"] = (f"仅 {len(digits)}/9 节，缺第 "
                           + "/".join(missing_secs) + " 节")
    if not has_pano and not is_holding:
        res["panorama"] = "缺 0.1 全景信息表"

    if not is_holding:
        rb = check_relative_baseline(text)
        if rb:
            res["baseline"] = rb

    ev = check_evidence_source(text)
    if ev:
        res["evidence"] = ev

    if CRON_AVAILABLE:
        sc = check_schedule(text, sched)
        if sc:
            res["schedule"] = sc

    pv = check_privacy(text, is_holding)
    if pv:
        res["privacy"] = pv

    return res


def main():
    fix = "--fix-format" in sys.argv
    global CRON_AVAILABLE
    CRON_AVAILABLE = JOBS.exists()
    valid, enabled, names, enames = load_job_ids()
    if CRON_AVAILABLE:
        print(f"cron 任务：共 {len(valid)} 个，启用 {len(enabled)} 个")
        print("📌 标准：台账只写 cron 任务名，不写 ID\n")
    else:
        print("cron：未配置（找不到 jobs.json）→ 相关校验已跳过，不计失败\n")
    if fix:
        print("模式：--fix-format（仅修四星号等格式类）\n")

    files = sorted(CAND.glob("*.md")) + sorted(HOLD.glob("*.md"))
    if not files:
        print("未找到台账文件")
        return

    sched = load_schedule()
    results = [validate_file(f, valid, enabled, names, enames, sched, fix)
               for f in files]
    clean = [r for r in results if len(r) == 2]
    dirty = [r for r in results if len(r) > 2]

    print(f"台账 {len(files)} 份：无问题 {len(clean)}，有问题 {len(dirty)}\n")

    # ── 流程状态表一致性（全步骤 第2–8步）────────────────────────
    ledger_codes = {}
    for f in files:
        m = re.match(r"(.+?)_(\d{6})_", f.name)
        if m:
            ledger_codes[m.group(2)] = m.group(1)
    serrs = check_status_consistency(ledger_codes)
    if serrs:
        print(f"🔴 流程状态表一致性：{len(serrs)} 项问题（台账 ↔ 状态表）")
        for e in serrs:
            print(f"   {e}")
        print()
    else:
        srows = parse_status_table() or []
        covered = sum(len(p) for _, p in srows)
        print(f"✅ 流程状态表一致性通过（{len(srows)} 个阶段行、共 {covered} 个代码位，"
              f"与 {len(ledger_codes)} 份台账双向匹配）\n")
    # ── 第 7 项：台账正文 ↔ 字典 一致性 ───────────────────────
    derrs, dcov = check_dict_consistency(files)
    if derrs:
        print(f"🔴 台账↔字典 一致性：{len(derrs)} 项不一致")
        for e in derrs:
            print(f"   {e}")
        print()
    else:
        print("\u2705 台账\u2194\u5b57\u5178一致性通过（BENCH \u65b9\u5411\u5185\u76f8\u5bf9\u4e2d\u4f4d\u53ef\u6bd4\u9879\u5747\u5339\u914d）\n")
    if dcov:
        print(f"   ↳ 第7项覆盖率：实际校验 {dcov.get('checked', 0)} / 应有 "
              f"{dcov.get('required', 0)} 只"
              + (f"，跳过/豁免 {len(dcov['skipped'])} 只" if dcov.get("skipped") else ""))
        for s in dcov.get("skipped", []):
            print(f"      · {s}")
        print()

    # ── 第 8 项：代码 ↔ 名称 绑定（防「张冠李戴」）──────────────
    extra = [STATUS] + sorted((PROJECT / "方向记录").glob("*.md"))
    berrs, bnotes = check_code_name_binding(files, extra)
    if berrs:
        print(f"🔴 代码↔名称 绑定：{len(berrs)} 项不符（主体写错）")
        for e in berrs:
            print(f"   {e}")
        print()
    else:
        print(f"✅ 代码↔名称 绑定通过（{len(files)} 份台账 + "
              f"{len(extra)} 份方向记录/流程状态表，均与行情接口一致）\n")
    if bnotes:
        print(f"ℹ️ 代码↔名称 有 {len(bnotes)} 项在行情接口查不到"
              f"（仅提示，不计错）：")
        for n in bnotes[:8]:
            print(f"   {n}")
        print()

    # ── 第 10 项：权威模板自检 ──────────────────────────────────
    terr = check_template()
    if terr:
        print(f"🔴 模板自检：{len(terr)} 项问题（{TEMPLATE.name}）")
        print("   （模板是建档唯一权威，模板错 = 之后每条新台账都错）")
        for e in terr:
            print(f"   · {e}")
        print()
    else:
        print("✅ 模板自检通过（结构 9/9、起点基准章节、必填项、格式、隐私）\n")

    # ── 第 12 项：cron 脚本漂移（工作区源 ↔ profile 运行副本）────────
    drift_errs, drift_notes = check_script_drift()
    if drift_errs:
        print(f"🔴 cron 脚本漂移：{len(drift_errs)} 项 "
              f"（cron 只跑 profile 副本，工作区改动不 cp 就不生效）")
        for e in drift_errs:
            print(f"   · {e}")
        print()
    else:
        if any("第12项" in s for s in SKIPPED):
            print("⚪ 脚本漂移校验已跳过（未配置 HERMES_HOME，见末尾跳过清单）\n")
        else:
            print("✅ 无脚本漂移"
                  "（profile 运行副本与工作区源逐一哈希一致）\n")
    if drift_notes:
        print(f"ℹ️ 脚本提示 {len(drift_notes)} 项（不计错）：")
        for n in drift_notes[:10]:
            print(f"   {n}")
        print()

    for r in dirty:
        print(f"🔴 {r['file']}（{r['stage']}）")
        for k, v in r.items():
            if k in ("file", "stage"):
                continue
            print(f"     {k}: {v}")
        print()
    if not dirty:
        print("✅ 全部台账通过")

    # 🔴 降级汇总：这些校验项因为取数失败**根本没跑**，
    #    不能跟着上面的「✅」一起被当成「全部通过」。
    if DEGRADED:
        print()
        print(f"🔴🔴 本次 {len(DEGRADED)} 项校验因取数失败未执行 ——")
        print("    「上面没报错」不等于「这些项合格」，须人工复核：")
        for d in DEGRADED:
            print(f"   · {d}")
    if SKIPPED:
        print()
        print(f"⚪ 本次跳过 {len(SKIPPED)} 项（环境未配置，**不计失败**）——")
        print("   但「跳过」不等于「通过」，如需这些校验请先按 README 配置：")
        for s in SKIPPED:
            print(f"   · {s}")
    if DEGRADED or terr or drift_errs:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())