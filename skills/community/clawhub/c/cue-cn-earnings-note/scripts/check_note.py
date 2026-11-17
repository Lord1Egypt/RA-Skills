#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_note.py —— cn-earnings-note 交付前门禁（SKILL.md §3.6，不过不交付）。

纯 stdlib、零网络。exit 0=过闸；exit 1=FAIL（逐条列因，含行号）。

四道检查：
  1. 声明在场      —— 首个标题行之后前 5 行内须同时出现「AI 初稿」与「不构成…投资建议」。
  2. [待人工] 就位 —— 含「评级」/「目标价」的行不得给出具体评级词或目标价值，且须带
                      [待人工]；--allow-pending 关闭本项。
  3. 禁用词        —— 合规最小集黑名单（内置），命中即 FAIL。
                      与 references/data-channels.md §合规最小集 冲突时以先 VERIFIED 者对齐。
  4. 数字可回查    —— 含「数字+集内单位」的正文行须带 [L1]/[L2]/[L3]；集内单位=%/percent/
                      个百分点/亿元/万元/千元/百万/万股/亿股/亿/元(负向预查防「元年」)/倍/股；
                      汉字形=确数(一二三四五六七八九十百两)+量级(千万|百万|万|亿|千)+尾(元[防年]/股)或
                      确数+倍——不定数(数亿/十几亿)、裸万+量词(五万份)、口语「三个百分点」、
                      二〇二六纪年形、无量级裸尾(三元的「三元」、五股的「五股」)在机器视野外,
                      归人工与文案纪律(清单见 M139 设计句 v1+M143 修正;裸尾不收=收它须拆量级闸,
                      「三元组/一元化」会连带被闸,过拦成本>漏拦收益,lead 可改判)。
                      标题行、列表引导行（以 - * 或数字序号引导且自身不含数字单位）、
                      「来源索引」节内豁免；覆盖率 < --min-coverage（默认 95%）FAIL。
                      给了 --sources 时另验 JSONL 契约（id/kind/ref/claim/confidence/asof
                      齐全、confidence 与标注同级、asof 为 YYYY-MM-DD）且正文引用的
                      [S<n>] id 均可解析。

用法：
  python3 check_note.py <note.md> [--sources sources.jsonl] [--allow-pending]
"""

import argparse
import json
import re
import sys
from pathlib import Path

# 合规最小集（铁律 6）。与 A 单 data-channels.md §合规最小集 若冲突，以先 VERIFIED 者对齐。
BANNED_WORDS = ["必涨", "稳赚", "零风险", "保证收益", "内幕", "无风险套利", "历史最佳"]
BANNED_RE = re.compile("|".join(BANNED_WORDS))

# ---------------------------------------------------------------- 错误码表(M166)
# 五类全族统一(各件出口同源);发码只在详行前缀 `[E-XXX] `,原消息一字不动——
# run_fixtures.sh 按子串断言,向后兼容零退化;图例行只列本次出现过的码。
E_LEGEND = {
    "E-FORMAT":   "形制/输入/表序不合式→按该行括号内规格改形制后复跑",
    "E-ANCHOR":   "锚/证据链缺失或断链→补合式锚或删除该条,禁虚构",
    "E-BANWORD":  "禁词/评级/幻觉/待人工域命中→改中性陈述或删除,零豁免区",
    "E-COVERAGE": "计数/覆盖/申报对不上→逐类补账或如实标未检索到",
    "E-LEDGER":   "账本状态机/互链断→按账本契约重建链接,禁改写历史",
}
E_RULES = (
    ("E-LEDGER", r"ledger|账本|互链|期初|fulfilled|amendment"),
    ("E-ANCHOR", r"^\[来源\]|^\[脚手架\][^\n]*(锚|来源)|锚行|双向"),
    ("E-BANWORD", r"^\[(禁用词|待人工)\]|^\[脚手架\][^\n]*(判断|观点)|评级|目标价"),
    ("E-COVERAGE", r"^\[数字\]|覆盖率|可回查|未检索"),
    ("E-FORMAT", r"^\[(声明|脚手架|参数)\]"),
)


def ecode(msg: str) -> str:
    for code, pat in E_RULES:
        if re.search(pat, msg):
            return code
    return "E-FORMAT"

NUM_UNIT_RE = re.compile(r"\d(?:[.,]\d+)?\s*(?:%|percent|个百分点|亿元|万元|千元|百万|万股|亿股|亿|元(?!年)|倍|股)", re.IGNORECASE)
CN_NUM_UNIT_RE = re.compile(r"[一二三四五六七八九十百两]+(?:千万|百万|万|亿|千)(?:元(?!年)|股)|[一二三四五六七八九十百两]+倍")
LEVEL_RE = re.compile(r"\[L[123]\]")
SRC_REF_RE = re.compile(r"\[S(\d+)\]")
HEADING_RE = re.compile(r"^#{1,6}\s")
INDEX_HEADING_RE = re.compile(r"^#{1,6}\s.*来源索引")
LIST_LEAD_RE = re.compile(r"^\s*(?:[-*]|\d+[.)、])\s+")
RATING_WORD_RE = re.compile(
    r"买入|增持|减持|卖出|中性|持有|推荐|强烈推荐|强烈买入|审慎增持|跑赢|跑输|逢低|高沽"
)
TARGET_VALUE_RE = re.compile(r"目标价[^。\n]*?\d+(?:\.\d+)?\s*(?:元|港元|美元|RMB|HKD|USD)", re.IGNORECASE)
PENDING_RE = re.compile(r"\[待人工\]")
# 白名单评级词以斜杠枚举并列且同行带 [待人工] 时,是 data-channels.md §4.3 允许的
# 「模板占位句式」(封面声明/§7 评级行),不构成「给出具体评级」——豁免条件:行内每个
# 白名单词都邻接斜杠;任一裸出现的词(如「倾向买入」)即破豁免照常 FAIL。
# 邻接前先把词典叠词(买卖/购买)归一,防「证券买卖推荐」这类通用词误判为评级词。
RATING_ENUM_RE = re.compile(r"(?:买入|增持|中性|减持|卖出)/(?:买入|增持|中性|减持|卖出)")
ANY_RATING_RE = re.compile(r"买入|增持|中性|减持|卖出")
SLASH = "/"


def _all_ratings_slash_adjacent(line):
    probe = line.replace("买卖", "XX").replace("购买", "XX")
    for m in ANY_RATING_RE.finditer(probe):
        before = probe[m.start() - 1] if m.start() > 0 else ""
        after = probe[m.end()] if m.end() < len(probe) else ""
        if SLASH not in (before, after):
            return False
    return True
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SOURCE_REQUIRED_FIELDS = ("id", "kind", "ref", "claim", "confidence", "asof")

# ---- ledger 模式(spec-0.2.0 F1;实现即 M2,缺陷编号见 verify/f1-deskcheck.md)----
LEDGER_STATUSES = {"fulfilled", "unfulfilled", "partial",
                   "carried_forward", "superseded", "unverifiable"}
LEDGER_DIRECTIONS = {"improving", "worsening", "flat"}
LEDGER_RESULTS = {"HIT", "MISS", "NO_TOOL", "EXTRACT_FAILED", "NO_RESPONSE"}
LEDGER_REF_RE = re.compile(r"^[A-Za-z0-9._\-]+:S\d+$")
LEDGER_CARRY_RE = re.compile(r"^(?:[A-Za-z0-9._\-]+:P\d{1,2}|new)$")
LEDGER_HEAD_FIELDS = ("schema", "run", "period")
LEDGER_OF_RE = re.compile(r"^([A-Za-z0-9._\-]+):([\w.\-]+\.json)$")
LEDGER_KNOWN_TOP = {"schema", "run", "period", "ledger_of", "anchors",
                    "risk_scan", "pending", "linkage_checks"}


def classify_lines(lines):
    """返回与 lines 等长的布尔表：该行是否属于「来源索引」豁免区（标题起，至下一任意标题止）。"""
    exempt = [False] * len(lines)
    in_index = False
    for i, line in enumerate(lines):
        if INDEX_HEADING_RE.match(line):
            in_index = True
        elif in_index and HEADING_RE.match(line):
            in_index = False
        exempt[i] = in_index
    return exempt


def check_declaration(lines):
    fails = []
    title_idx = next((i for i, l in enumerate(lines) if HEADING_RE.match(l)), None)
    if title_idx is None:
        return ["[声明] 未找到标题行（# 开头），AI 初稿声明无从挂靠"]
    window = "".join(lines[title_idx + 1: title_idx + 6])
    if "AI 初稿" not in window:
        fails.append(f"[声明] 标题后前 5 行内未出现「AI 初稿」（实际扫描行 {title_idx + 2}–{title_idx + 6}）")
    if not re.search(r"不构成.{0,12}投资建议", window):
        fails.append("[声明] 标题后前 5 行内未出现「不构成…投资建议」免责句")
    return fails


def check_pending(lines, index_exempt):
    fails = []
    for i, line in enumerate(lines):
        if index_exempt[i] or not line.strip():
            continue
        has_kw = ("评级" in line) or ("目标价" in line)
        if not has_kw:
            continue
        if has_kw and PENDING_RE.search(line) and RATING_ENUM_RE.search(line) \
                and _all_ratings_slash_adjacent(line):
            continue  # §4.3 模板占位句式:白名单词全部斜杠邻接且同行 [待人工];裸出现一词即破豁免
        if RATING_WORD_RE.search(line) or TARGET_VALUE_RE.search(line):
            fails.append(f"[待人工] 第 {i + 1} 行给出了具体评级/目标价：{line.strip()[:60]}")
        elif not PENDING_RE.search(line):
            fails.append(f"[待人工] 第 {i + 1} 行涉及评级/目标价但未见 [待人工]：{line.strip()[:60]}")
    return fails


def check_banned(lines):
    fails = []
    for i, line in enumerate(lines):
        m = BANNED_RE.search(line)
        if m:
            fails.append(f"[禁用词] 第 {i + 1} 行命中「{m.group(0)}」：{line.strip()[:60]}")
    return fails


def check_numbers(lines, index_exempt, sources_path, min_coverage):
    fails = []
    stat_rows = []
    refs = set()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        for rid in SRC_REF_RE.findall(line):
            if not index_exempt[i]:
                refs.add(int(rid))
        if index_exempt[i] or HEADING_RE.match(line):
            continue
        has_num = bool(NUM_UNIT_RE.search(line) or CN_NUM_UNIT_RE.search(line))
        if not has_num:
            continue
        if LIST_LEAD_RE.match(line) and not LEVEL_RE.search(line) and SRC_REF_RE.search(line):
            continue  # 列表引导行自带 [S<n>] 来源指向,视为可回查
        stat_rows.append((i, line))
        if not LEVEL_RE.search(line):
            fails.append(f"[数字] 第 {i + 1} 行含数字结论但无 [L1]/[L2]/[L3]：{stripped[:60]}")

    total = len(stat_rows)
    tagged = total - sum(1 for f in fails if f.startswith("[数字]"))
    coverage = 1.0 if total == 0 else tagged / total
    pct = coverage * 100
    if coverage * 100 + 1e-9 < min_coverage:
        fails.insert(0, f"[数字] 可回查覆盖率 {pct:.1f}% < 阈值 {min_coverage:.0f}%（{tagged}/{total}）")

    if sources_path:
        fails.extend(check_sources_jsonl(sources_path, refs, lines))
    return fails, total, tagged


def check_sources_jsonl(path, refs_in_note, lines):
    fails = []
    ids = set()
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except OSError as e:
        return [f"[来源] --sources 无法读取：{e}"]
    for ln, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as e:
            fails.append(f"[来源] sources.jsonl 第 {ln} 行非法 JSON：{e}")
            continue
        if not isinstance(rec, dict):
            fails.append(f"[来源] sources.jsonl 第 {ln} 行不是对象")
            continue
        for f in SOURCE_REQUIRED_FIELDS:
            v = rec.get(f)
            if not isinstance(v, str) or not v.strip():
                fails.append(f"[来源] sources.jsonl 第 {ln} 行字段 {f} 缺失或为空")
        m = re.fullmatch(r"S(\d+)", str(rec.get("id", "")))
        if m:
            ids.add(int(m.group(1)))
        elif rec.get("id"):
            fails.append(f"[来源] sources.jsonl 第 {ln} 行 id 不符合 S<n>：{rec['id']}")
        if rec.get("asof") and not DATE_RE.match(rec["asof"]):
            fails.append(f"[来源] sources.jsonl 第 {ln} 行 asof 非 YYYY-MM-DD：{rec['asof']}")

    missing = sorted(refs_in_note - ids)
    if missing:
        fails.append("[来源] 正文引用的 [S<n>] 在 sources.jsonl 中无法解析：" + ", ".join(f"S{n}" for n in missing))
    return fails


def _walk_value_dicts(node, path):
    """yield (path, dict) for every dict containing a numeric-ish "value" key (D6)."""
    if isinstance(node, dict):
        if "value" in node:
            yield path, node
        for k, v in node.items():
            yield from _walk_value_dicts(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _walk_value_dicts(v, f"{path}[{i}]")


def _check_ledger_of(led, ledger_path, prev_led, tag, fails):
    """B2(spec-0.2.0 §F1 修 D2):ledger_of 互链的上季文件存在且 period 匹配,机检断言化。"""
    lo = led.get("ledger_of")
    if lo is None:
        return  # 首季建账合法缺省
    m = LEDGER_OF_RE.match(str(lo))
    if not m:
        fails.append(f"[{tag}] ledger_of 格式须为 <run_dir>:<file>.json,实为 {lo!r}")
        return
    run_name, fname = m.group(1), m.group(2)
    here = Path(ledger_path).resolve().parent
    for cand in (here / run_name / fname, Path.cwd() / run_name / fname):
        if cand.is_file():
            try:
                data = json.loads(cand.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as e:
                fails.append(f"[{tag}] ledger_of 命中文件不可读/解析：{cand}（{e}）")
                return
            if data.get("period") == led.get("period"):
                fails.append(f"[{tag}] ledger_of 互链 period 与本季相同（{led.get('period')}）")
            return
    if isinstance(prev_led, dict) and prev_led.get("run") == run_name:
        if prev_led.get("period") == led.get("period"):
            fails.append(f"[{tag}] ledger_of={lo} 经 --prev-ledger 承载,但其 period 与本季相同")
        return
    fails.append(f"[{tag}] ledger_of 断链：{run_name}/{fname} 不可达,且 --prev-ledger 的 run 不匹配")


def check_ledger(path, is_prev=False, prev_led=None):
    fails = []
    tag = "prev-ledger" if is_prev else "ledger"
    try:
        led = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [f"[{tag}] 无法读取/解析：{e}"]
    if not isinstance(led, dict):
        return [f"[{tag}] 顶层不是对象"]
    for f in LEDGER_HEAD_FIELDS:  # D2/D9:文件头三件,缺一即断链
        if not str(led.get(f, "")).strip():
            fails.append(f"[{tag}] 头部字段 {f} 缺失或为空")
    _check_ledger_of(led, path, prev_led, tag, fails)  # B2
    unknown = set(led) - LEDGER_KNOWN_TOP
    if unknown:  # 6.1 B1 防呆补位:未识别顶层键提示(不 FAIL,前瞻兼容)
        print(f"[{tag}] ⚠ 未识别顶层键(机检不覆盖,确认拼写): {sorted(unknown)}")
    if "risk_checks" in led:  # 旧名残留=分家复发,直接 FAIL
        fails.append(f"[{tag}] 顶层出现旧名 risk_checks——已统一为 risk_scan(spec-0.2.0)")

    for a in led.get("anchors", []):
        aid = a.get("id", "?")
        status = a.get("status")
        if status not in LEDGER_STATUSES:  # ① D3 六态
            fails.append(f"[{tag}] 锚 {aid} status 非法：{status!r}(六态枚举)")
        if "direction" in a:
            if not a.get("trend"):
                fails.append(f"[{tag}] 锚 {aid} 非趋势锚(trend≠true)不得带 direction(D3)")  # ①
            elif a["direction"] not in LEDGER_DIRECTIONS:
                fails.append(f"[{tag}] 锚 {aid} direction 非法：{a['direction']!r}")
        src = a.get("source")
        if src is not None and not LEDGER_REF_RE.match(str(src)):  # ⑧ D9
            fails.append(f"[{tag}] 锚 {aid} source 引用须为 <run>:S##,实为 {src!r}")
        amended = False
        for ev in a.get("events", []):
            if not ev.get("type") or not ev.get("date"):
                fails.append(f"[{tag}] 锚 {aid} event 缺 type/date(D4)")
            if ev.get("type") == "amendment":
                amended = True
        if amended and status == "fulfilled":  # ② D4
            fails.append(f"[{tag}] 锚 {aid} 有 amendment 事件却判 fulfilled(D4)")

    for key, rc in (led.get("risk_scan") or {}).items():
        result = rc.get("result") if isinstance(rc, dict) else None
        if result not in LEDGER_RESULTS:  # ④ D8 五枚举
            fails.append(f"[{tag}] 风险项 {key} result 非法：{result!r}(HIT/MISS/NO_TOOL/EXTRACT_FAILED/NO_RESPONSE)")
        ev = rc.get("evidence") if isinstance(rc, dict) else None
        if isinstance(ev, str) and ev and not LEDGER_REF_RE.match(ev):  # ⑧
            fails.append(f"[{tag}] 风险项 {key} evidence 引用须为 <run>:S##,实为 {ev!r}")

    for vp, vd in _walk_value_dicts(led, tag):  # ③ D6:一切数值对象带 basis
        b = vd.get("basis")
        if not isinstance(b, dict) or not b:
            fails.append(f"[{tag}] {vp} 带 value 但缺 basis 对象(D6)")

    pend = led.get("pending", [])
    filled = gate_total = 0
    for p in pend:
        pid = p.get("id", "?")
        cf = p.get("carry_from")
        if not LEDGER_CARRY_RE.match(str(cf or "")):  # ⑤ D7
            fails.append(f"[{tag}] pending {pid} carry_from 须为 <run>:P## 或 new,实为 {cf!r}")
        ex = p.get("exempt_from_gate", False)
        if not isinstance(ex, bool):  # ⑥ D11
            fails.append(f"[{tag}] pending {pid} exempt_from_gate 须为布尔(D11)")
            ex = False
        if not ex:
            gate_total += 1
            if p.get("verdict") is not None:
                filled += 1
    print(f"[{tag}] 裁决回填率(除豁免行): {filled}/{gate_total}")  # ⑥:豁免行不入统计

    for i, lc in enumerate(led.get("linkage_checks", []), 1):  # ⑦ D5 核心
        pe, tb = lc.get("prev_period_end"), lc.get("this_period_begin")
        refs = lc.get("both_ref")
        if pe != tb:
            fails.append(
                f"[{tag}] linkage#{i} {lc.get('metric','?')} 跨期衔接不等: "
                f"上季末={pe!r} vs 本季初={tb!r} (refs={refs})")
        if not (isinstance(refs, list) and len(refs) == 2
                and all(LEDGER_REF_RE.match(str(r)) for r in refs)):  # ⑧
            fails.append(f"[{tag}] linkage#{i} both_ref 须为两条 <run>:S##,实为 {refs!r}")
    return fails


GAP_RE = re.compile(r"未检索到|未披露|未获取|域面无项|缺数")


def build_audit_report(args, lines, index_exempt, banned_fails, pending_note_fails,
                       ledger_paths, ledger_data):
    """送审就绪度附录(spec-0.2.0 F3)。五节恒在,无内容也显式写结论行。"""
    import datetime
    d = Path(args.note).resolve().parent
    out = [f"# 送审就绪度附录 — {Path(args.note).name}",
           f"生成：check_note.py --audit-report · {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} · 不构成合规意见，仅供送审前自检。", ""]
    out.append("## 1. 禁止词命中表")
    out.append("| 行号 | 命中词 | 原文截断 |")
    out.append("| --- | --- | --- |")
    if banned_fails:
        for f in banned_fails:
            m = re.match(r"\[禁用词\] 第 (\d+) 行命中「(.+?)」：(.*)", f)
            out.append(f"| {m.group(1)} | {m.group(2)} | {m.group(3)[:40]} |" if m else f"| ? | ? | {f[:60]} |")
        out.append(f"\n结论：**{len(banned_fails)} 处命中，送审前必须清零**。")
    else:
        out.append("| — | 零命中 | 全文黑名单未触发 |")
        out.append("\n结论：**零命中**（黑名单 7 词逐行扫描，无例外区）。")
    out.append("\n## 2. [待人工] 计数")
    pend_lines = [i + 1 for i, l in enumerate(lines) if not index_exempt[i] and PENDING_RE.search(l)]
    out.append(f"- note 内 [待人工] 标注行：{len(pend_lines)} 处（行号 {pend_lines[:12]}）")
    out.append(f"- 第 2 道门禁违规（给出具体评级/目标价或缺 [待人工]）：{len(pending_note_fails)} 条")
    for led, lp in zip(ledger_data, ledger_paths):
        if isinstance(led, dict):
            pend = led.get("pending", [])
            ex = sum(1 for p in pend if p.get("exempt_from_gate"))
            filled = sum(1 for p in pend if p.get("verdict") is not None and not p.get("exempt_from_gate"))
            out.append(f"- ledger `{Path(lp).name}`：pending {len(pend)} 行，豁免 {ex} 行（D11 剥离），非豁免回填 {filled}/{len(pend)-ex}")
    out.append("\n## 3. 缺数未回补清单")
    gaps = [(i + 1, re.sub(r"\s+", " ", l.strip())[:56]) for i, l in enumerate(lines) if not index_exempt[i] and GAP_RE.search(l)]
    out.append("| 行号 | 处所摘录 |")
    out.append("| --- | --- |")
    for ln, s in gaps:
        out.append(f"| {ln} | {s} |")
    out.append(f"\n结论：**{len(gaps)} 处**缺数/降级表述在场（送审时应随附回补计划或人工核对说明；无缺数则此计数为 0）。" if gaps else "\n结论：**0 处**——本期无缺数表述（若全量取到属实，可随附声明；缺数若有未写占位，门禁不兜，人工确认）。")
    out.append("\n## 4. AI 声明与免责核验")
    decl = check_declaration(lines)
    out.append(f"- 标题后前 5 行「AI 初稿」+「不构成…投资建议」核验：{'✅ 通过' if not decl else '❌ ' + '；'.join(decl)}")
    out.append(f"- 评级/目标价代填核验：{'✅ 无违规' if not pending_note_fails else '❌ 见第 2 节'}")
    out.append("\n## 5. 送审包文件清单")
    checks = [("note.md", Path(args.note)), ("sources.jsonl", Path(args.sources) if args.sources else None),
              ("ledger(当期)", Path(args.ledger) if args.ledger else None),
              ("ledger(上季)", Path(args.prev_ledger) if args.prev_ledger else None)]
    for name, pth in checks:
        out.append(f"- {name}: {'✅ ' + str(pth) if pth and pth.is_file() else ('未提供' if pth is None else '❌ 缺失 ' + str(pth))}")
    bl = d / "baseline.json"
    out.append(f"- baseline.json(同级): {'✅ 在场' if bl.is_file() else '— 同级无（首季或未启用基线则合法）'}")
    return "\n".join(out) + "\n"


SCAFFOLD_HEADING_RE = re.compile(r"^#{1,6}\s*预测脚手架")
SCAFFOLD_ANCHOR_PREFIX = "对照锚（非本方观点）"
SCAFFOLD_BORDER_PHRASE = "本 skill 不产前瞻值"
SCAFFOLD_ROW3 = ("归母净利润", "每股收益（EPS）", "营业收入")
SCAFFOLD_CELL_OK = re.compile(
    r"^(?:\[待人工\]|约?\s*-?\d{1,3}(?:,\d{3})*(?:\.\d+)?(?:\s*[-–~至]\s*约?\d{1,3}(?:,\d{3})*(?:\.\d+)?)?(?:\s*(?:亿|万)?元?)|—|-)$")
SCAFFOLD_OPINION_WORDS = ("预计", "上调", "下调", "看好", "乐观", "谨慎", "维持", "给予")
YEAR_COL_RE = re.compile(r"^(?:<?Y\d?>?|\d{4})E$")


def check_scaffold(lines):
    """spec-0.3.3 §B 第⑤形制检查:标记触发,无标记不校验。"""
    head = next((i for i, l in enumerate(lines) if SCAFFOLD_HEADING_RE.match(l)), None)
    if head is None:
        return []
    end = next((i for i in range(head + 1, len(lines)) if HEADING_RE.match(lines[i])), len(lines))
    sec = lines[head + 1:end]
    body = "\n".join(sec)
    fails = []

    if SCAFFOLD_BORDER_PHRASE not in body:  # B4
        fails.append("[脚手架] 缺边框注固定句「" + SCAFFOLD_BORDER_PHRASE + "」(N1 条件②机检化)")

    anchor_rows = [l for l in sec if l.strip().startswith(SCAFFOLD_ANCHOR_PREFIX)]
    if not anchor_rows:  # A1 固定形状:锚行必须在场
        fails.append("[脚手架] 缺「对照锚（非本方观点）」行(固定形状;态二须写未检索到句)")
    for l in anchor_rows:  # B3:非「未检索到」锚行须同行含 S<n>
        if "未检索到" not in l and not re.search(r"S\d+", l):
            fails.append(f"[脚手架] 锚行缺 S<n> 引用：{l.strip()[:60]}")

    rows_seen = {r: False for r in SCAFFOLD_ROW3}
    col_idx = None
    for l in sec:
        if not l.strip().startswith("|"):
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if not cells:
            continue
        if col_idx is None and any(YEAR_COL_RE.match(c) for c in cells):
            col_idx = [j for j, c in enumerate(cells) if YEAR_COL_RE.match(c)][:3]
            continue
        first = cells[0]
        if first in rows_seen and col_idx:
            rows_seen[first] = True
            for j in col_idx:  # B2:三格形态+禁判断词(词表复用门禁②精神)
                if j >= len(cells):
                    fails.append(f"[脚手架] 「{first}」行预测列缺格")
                    continue
                cell = cells[j]
                if any(w in cell for w in SCAFFOLD_OPINION_WORDS):
                    fails.append(f"[脚手架] 「{first}」格含判断词(观点归人,B2)：{cell[:24]}")
                elif not SCAFFOLD_CELL_OK.match(cell):
                    fails.append(f"[脚手架] 「{first}」单元格形态非法：{cell[:24]}(只许 [待人工]/数值/区间/约值)")
    for r, seen in rows_seen.items():
        if not seen:
            fails.append(f"[脚手架] 三行固定指标缺「{r}」行(A1 形状)")
    return fails


def main(argv=None):
    p = argparse.ArgumentParser(
        description="cn-earnings-note 交付前四道门禁：声明在场 / [待人工] 就位 / 禁用词 / 数字可回查。",
        epilog="exit 0=过闸；exit 1=FAIL。纯 stdlib、零网络。",
    )
    p.add_argument("note", help="待检查的 note.md")
    p.add_argument("--sources", default=None, help="sources.jsonl；给了则逐条验证契约字段与 [S<n>] 引用可解析")
    p.add_argument("--allow-pending", action="store_true", help="关闭「[待人工] 就位」检查（第 2 道）")
    p.add_argument("--min-coverage", type=float, default=95.0, help="数字可回查覆盖率阈值（默认 95）")
    p.add_argument("--ledger", default=None, help="覆盖账本当期 JSON（spec-0.2.0 F1 八项校验，见 references/ledger-schema.md）")
    p.add_argument("--prev-ledger", default=None, help="上一期账本 JSON（同样过结构校验；linkage 断言在当期文件内自含）")
    p.add_argument("--audit-report", default=None, help="输出「送审就绪度」五节附录到该 md 文件（F3；FAIL 时也照样产出）")
    args = p.parse_args(argv)

    try:
        lines = Path(args.note).read_text(encoding="utf-8").splitlines()
    except OSError as e:
        print(f"FAIL: 无法读取 {args.note}: {e}")
        return 1

    index_exempt = classify_lines(lines)
    fails = []
    fails += check_declaration(lines)
    pending_fails = [] if args.allow_pending else check_pending(lines, index_exempt)
    fails += pending_fails
    banned_fails = check_banned(lines)
    fails += banned_fails
    num_fails, total, tagged = check_numbers(lines, index_exempt, args.sources, args.min_coverage)
    fails += num_fails
    fails += check_scaffold(lines)  # spec-0.3.3 §B 第⑤形制(标记触发)
    ledger_paths, ledger_data = [], []
    if args.ledger:
        prev_data = None
        if args.prev_ledger:
            try:
                prev_data = json.loads(Path(args.prev_ledger).read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                pass  # 失败由 prev 校验路径自行报
        ledger_paths = [args.ledger, args.prev_ledger]
        try:
            cur_data = json.loads(Path(args.ledger).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            cur_data = None
        ledger_data = [cur_data, prev_data]
        fails += check_ledger(args.ledger, prev_led=prev_data)
    if args.prev_ledger:
        fails += check_ledger(args.prev_ledger, is_prev=True)

    if args.audit_report:
        report = build_audit_report(args, lines, index_exempt, banned_fails,
                                    pending_fails, ledger_paths, ledger_data)
        try:
            Path(args.audit_report).write_text(report, encoding="utf-8")
            print(f"送审就绪度附录 → {args.audit_report}")
        except OSError as e:
            print(f"FAIL: --audit-report 无法写出 {args.audit_report}: {e}")
            return 1

    if fails:
        print(f"FAIL: {args.note}（{len(fails)} 条）")
        codes = []
        for f in fails:
            c = ecode(f)
            if c not in codes:
                codes.append(c)
            print(f"  - [{c}] {f}")
        print("  码表: " + "; ".join(f"{c}→{E_LEGEND[c]}" for c in codes))
        return 1
    print(f"PASS: {args.note}（数字行 {tagged}/{total} 已标注，四道门禁全过）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
