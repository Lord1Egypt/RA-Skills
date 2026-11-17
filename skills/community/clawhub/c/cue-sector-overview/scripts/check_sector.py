#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_sector.py —— sector-overview 行业景气全景机检(spec §3 四道 + M46 题单验收协议)。

纯 stdlib、零网络、零崩溃(任何输入异常→FAIL 清单+exit 1,traceback=事故)。
CLI(合同 §3 命令式,--sources/--window 必传):
  check_sector.py <report.md> --sources <sources.jsonl> --window YYYY-MM-DD~YYYY-MM-DD [--evidence <dir>]

四道(题单 §0.3 道号定义;诊断行以 [①]..[④] 前缀标注):
  ① 声明行:「AI 初稿」等价式 + asof: 日期 + 通道用量…次,缺任一即 FAIL;
     标题声明「窗口 A~B」与 --window 不一致=申报漂移(同 [①])。
  ② 判断词-锚同行(本件命门):整词表 升|降|回暖|承压|走弱|拐点|高景气|低谷 出现在正文
     ⇒ 同句含 [S<n>],或该句逐字为「无可比序列,不做景气判定」(态二白名单,逐字不得改写——
     改写探测含「无可比序列/不做景气判定/不判断景气/暂不判」形近句);《》不豁免;跨句不豁免;
     整词铁律:「上升/升幅/下降/降幅」不触发单字 升/降(误杀=实现缺陷,good 族回归)。
  ③ 禁词零容忍:BANNED 全族 + 利好|利空|买入|增持|减持|持有|目标价|建议|推荐|看好;
     豁免区=无(《》/引用位/围栏不豁免);扫描面=正文+sources.claim/ref。
     页眉合同基线句「不构成…投资建议/买卖推荐」逐字属声明本体,先摘短语再扫——
     非豁免区,否则 good 基线自灭(题单 §1 页眉基线在场此文;此裁随对账表入账)。
  ④ 形制闸:六节语义定位(画像→量价→供需→格局→政策→复核,不绑字面标题;缺节/降序 FAIL);
     数字/序列行有锚(表格数字行含 [S<n>];散文数字行同规——纯日期形与「L3」级序号不算数字);
     「据估计/市场预期」无源句归 ④(题单 B05 合同指定);正文↔sources 双向;
     政策锚三件齐(statute:《法名》第N条（要点） 或 函件号〔YYYY〕N号)+ evidence fail-closed:
     kind=statute 行有 --evidence 须整词命中原文,无 --evidence 一律「不可核」不放行;
     代表公司 ≥3 且格局段零点评(非表行散文即点评);行契约六字段+枚举+日期有效。
"""

import argparse
import datetime as dt
import json
import re
import sys
import traceback
from pathlib import Path

STATE2 = "无可比序列，不做景气判定"
STATE2_HINT_RE = re.compile(r"无可比序列|不做景气判定|不判断景气|暂不判")
JUDGE_PHRASE = ("回暖", "承压", "走弱", "拐点", "高景气", "低谷")
JUDGE_SINGLE = (
    (re.compile(r"(?<![上下提跌跳])升(?![降幅级温])"), "升"),
    (re.compile(r"(?<![上回低])降(?![降幅级温])"), "降"),
)
BANNED_RE = re.compile(
    r"必涨|稳赚|零风险|保证收益|内幕|无风险套利|历史最佳|暴涨|会涨|抄底|逃顶"
    r"|利好|利空|买入|增持|减持|持有|目标价|建议|推荐|看好")
NOT_INVEST_RE = re.compile(r"不构成[^。；;]{0,16}(投资建议|买卖推荐)")
GUESS_RE = re.compile(r"据估计|市场预期")
ASOF_RE = re.compile(r"asof[:：]\s*(\d{4}-\d{2}-\d{2})", re.I)
USAGE_RE = re.compile(r"(通道用量|channel usage).{0,24}(次|times)", re.I)
TITLE_HEAD = re.compile(r"窗口\s*(\d{4}-\d{2}-\d{2})\s*[~至]\s*(\d{4}-\d{2}-\d{2})")
DATE_RE = re.compile(r"\d{4}-\d{2}(?:-\d{2})?")
SREF_RE = re.compile(r"\[S(\d+)\]")
NUM_CELL_RE = re.compile(r"^-?[\d,]+(?:\.\d+)?%?$")
NUM_PROSE_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:万吨|亿吨|亿|万|%|个百分点|台|吨)|\d+\.\d+|\d{2,}")
STATUTE_SPEC_RE = re.compile(
    r"^statute[:：]《[^《》]+》第[0-9一二三四五六七八九十百零]+条（[^（）]{2,}）$")
LETTER_RE = re.compile(r"^\S*〔\d{4}〕\d+号$")
KIND_ENUM = {"macro", "disclosure_cn", "statute", "regulatory_cn", "research",
             "omni", "pool", "user", "fr_fact_index", "buyback", "esop",
             "fr_footnote", "disclosure", "institutional"}  # M49 冒烟修:家族真 kind 面(fr_fact_index 等)入枚举

# ---------------------------------------------------------------- 错误码表(M166)
# 五类码表 E_LEGEND 全族逐字一致(各件出口同源);E_RULES 是按本件标签的分类表。
# 发码只在详行前缀 `[E-XXX] `,原消息一字不动,runner 子串断言向后兼容。
E_LEGEND = {
    "E-FORMAT":   "形制/输入/表序不合式→按该行括号内规格改形制后复跑",
    "E-ANCHOR":   "锚/证据链缺失或断链→补合式锚或删除该条,禁虚构",
    "E-BANWORD":  "禁词/评级/幻觉/待人工域命中→改中性陈述或删除,零豁免区",
    "E-COVERAGE": "计数/覆盖/申报对不上→逐类补账或如实标未检索到",
    "E-LEDGER":   "账本状态机/互链断→按账本契约重建链接,禁改写历史",
}
E_RULES = (
    ("E-BANWORD", r"\[③\]"),
    ("E-COVERAGE", r"\[④\][^\n]*(缺数|未检索|覆盖)"),
    ("E-ANCHOR", r"\[②\]|\[④\][^\n]*(锚|双向|来源|statute|证据)"),
    ("E-FORMAT", r"\[①\]|\[参数\]|^\[④\]"),
)


def ecode(msg: str) -> str:
    for code, pat in E_RULES:
        if re.search(pat, msg):
            return code
    return "E-FORMAT"

RANK = {"portrait": 1, "series": 2, "supply": 3, "companies": 4, "policy": 5, "review": 6}
KIND_CN = {"portrait": "画像", "series": "量价", "supply": "供需",
           "companies": "格局", "policy": "政策", "review": "复核"}
RESERVED_H2 = ("附录", "来源索引")
SENDER_MARK_RE = re.compile(r"conv_id=\S+")


def judge_hits(s):
    hits = [w for w in JUDGE_PHRASE if w in s]
    for pat, w in JUDGE_SINGLE:
        if pat.search(s):
            hits.append(w)
    return hits


def evidence_hit(text, probe):
    return re.search(r"(?<![0-9A-Za-z])" + re.escape(probe) + r"(?![0-9A-Za-z])", text) is not None


def scan_sources(recs):
    fails = []
    seen = set()
    for ln, rec in recs:
        rid = str(rec.get("id", ""))
        if not re.fullmatch(r"S\d+", rid):
            fails.append(f"[④] sources 第 {ln} 行 id 非 S<n>:{rid!r}")
        elif rid in seen:
            fails.append(f"[④] sources id 重复:{rid}")
        seen.add(rid)
        for f in ("id", "kind", "ref", "claim", "confidence", "asof"):
            v = rec.get(f)
            if not isinstance(v, str) or not v.strip():
                fails.append(f"[④] sources 第 {ln} 行字段 {f} 缺失或为空")
        if rec.get("kind") and rec["kind"] not in KIND_ENUM:
            fails.append(f"[④] sources 第 {ln} 行 kind 非枚举:{rec['kind']!r}")
        if rec.get("confidence") and rec["confidence"] not in {"L1", "L2", "L3"}:
            fails.append(f"[④] sources 第 {ln} 行 confidence 非枚举:{rec['confidence']!r}")
        a = str(rec.get("asof", ""))
        if a:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", a):
                fails.append(f"[④] sources 第 {ln} 行 asof 非 YYYY-MM-DD:{a!r}")
            else:
                try:
                    dt.date.fromisoformat(a)
                except ValueError:
                    fails.append(f"[④] sources 第 {ln} 行 asof 日期不存在:{a}")
        ref = str(rec.get("ref", ""))
        if rec.get("kind") == "research" and not (SENDER_MARK_RE.search(ref) and re.search(r"(\.md|\.log|reports/)", ref)):
            fails.append(f"[④] sources 第 {ln} 行 research 件缺 conv_id+落盘路径:{ref[:60]}")
        if rec.get("kind") == "statute" and not STATUTE_SPEC_RE.match(ref.strip()):
            fails.append(f"[④] 法定锚不可核:statute 锚不符《法名》第N条（要点）三件齐:{ref[:60]!r}")
        if rec.get("kind") == "regulatory_cn" and not (LETTER_RE.match(ref.strip()) or re.match(r"^AN\d{8,}$", ref.strip())):
            fails.append(f"[④] 政策锚三件齐:regulatory 行 ref 须函件号或 AN:{ref[:60]!r}")
        bad = BANNED_RE.search(NOT_INVEST_RE.sub("", ref)) or BANNED_RE.search(NOT_INVEST_RE.sub("", str(rec.get("claim", ""))))
        if bad:
            fails.append(f"[③] sources 第 {ln} 行 claim/ref 命中禁词「{bad.group(0)}」(③扫描面)")
    return fails


def classify(title, body_text):
    if re.search(r"复核|把关", title) or re.search(r"^- L3|^- \[?\s*L3", body_text, re.M):
        return "review"
    cells = set()
    for l in body_text.splitlines():
        if l.strip().startswith("|"):
            cells.update(c.strip() for c in l.strip().strip("|").split("|"))
    joined = "|".join(cells)
    if "basis" in joined:
        return "series"
    if re.search(r"公司", joined):
        return "companies"
    if re.search(r"文件", joined) or re.search(r"政策|时间线|文件链", title):
        return "policy"
    if re.search(r"量价", title):
        return "series"  # M49 冒烟修:量价节只带缺数句(无 basis 表)时曾被 缺数→supply 抢走——薄简报合法形制
    if re.search(r"供需|供给|产能|缺数|断更", title + "\n" + body_text):
        return "supply"
    return "portrait"


def run(args):
    fails = []
    if not args.sources:
        fails.append("[参数] 缺 --sources(合同 §3 命令式必传)")
    if not args.window:
        fails.append("[参数] 缺 --window(合同 §3 命令式必传,反 wall-clock)")
    if fails:
        return fails
    m = re.match(r"^(\d{4}-\d{2}-\d{2})[~至](\d{4}-\d{2}-\d{2})$", args.window.strip())
    if not m:
        return [f"[参数] --window 形制应为 YYYY-MM-DD~YYYY-MM-DD,实为 {args.window!r}"]
    lo, hi = dt.date.fromisoformat(m.group(1)), dt.date.fromisoformat(m.group(2))
    if lo > hi:
        return ["[参数] --window 起点晚于终点"]
    try:
        lines = Path(args.report).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as e:
        return [f"无法读取 {args.report}:{e}"]

    recs = []
    try:
        raw = Path(args.sources).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return [f"无法读取 sources:{e}"]
    for ln, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
            recs.append((ln, rec if isinstance(rec, dict) else {}))
        except json.JSONDecodeError:
            recs.append((ln, {}))
            fails.append(f"[④] sources 第 {ln} 行非法 JSON")
    fails += scan_sources(recs)

    evidence_text = None
    if args.evidence:
        ed = Path(args.evidence)
        if ed.is_dir():
            eps = [p for p in ed.resolve().iterdir() if p.is_file()]
            if eps:
                evidence_text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in eps)

    # —— 道① 声明 + 窗口申报 ——
    title_i = next((i for i, l in enumerate(lines) if l.startswith("# ")), None)
    if title_i is None:
        fails.append("[①] 未找到标题行")
    else:
        w5 = "\n".join(lines[title_i:title_i + 6])
        if not re.search(r"AI ?初稿", w5):
            fails.append("[①] 页头缺声明字段「AI 初稿」(或契约等价)")
        if not ASOF_RE.search(w5):
            fails.append("[①] 页头缺声明字段「asof: 日期」")
        if not USAGE_RE.search(w5):
            fails.append("[①] 页头缺声明字段「通道用量」")
    tw = TITLE_HEAD.search("\n".join(lines[:3]))
    if tw and (tw.group(1) != lo.isoformat() or tw.group(2) != hi.isoformat()):
        fails.append(f"[①] 标题声明窗口 {tw.group(1)}~{tw.group(2)} 与 --window 不一致(申报漂移)")

    # —— 六节切块(语义定位,协议 4 字面形状零依赖) ——
    marks = [i for i, l in enumerate(lines) if l.startswith("## ")]
    sections = []
    for j, s in enumerate(marks):
        e = marks[j + 1] if j + 1 < len(marks) else len(lines)
        title = lines[s][3:].strip()
        if any(title.startswith(r) for r in RESERVED_H2):
            continue
        sections.append((title, s, e))
    kinds = []
    for title, s, e in sections:
        body = "\n".join(lines[s + 1:e])
        kinds.append(classify(title, body))
    missing = [KIND_CN[k] for k in ("portrait", "series", "supply", "companies", "policy", "review") if k not in kinds]
    if missing:
        fails.append(f"[④] 六节不完整:缺「{'、'.join(missing)}」节(语义定位,改名不豁免)")
    for i in range(len(kinds) - 1):
        if RANK[kinds[i + 1]] < RANK[kinds[i]]:
            fails.append(f"[④] 「{KIND_CN[kinds[i]]}」段出现在「{KIND_CN[kinds[i + 1]]}」段之前(六节语义顺序 1→6)")
            break

    # —— 道② 判断词-锚同句(命门) ——
    for i, l in enumerate(lines):
        if not l.strip() or l.lstrip().startswith("#"):
            continue
        for sent in re.split(r"[。；;！!？?]", l):
            s = sent.strip()
            if not s:
                continue
            if s == STATE2 or s.rstrip("。") == STATE2:
                continue
            if STATE2_HINT_RE.search(s):
                fails.append(f"[②] 第 {i + 1} 行态二句被改写(合同逐字:「{STATE2}」):{s[:30]!r}")
                continue
            hits = judge_hits(s)
            if hits and not SREF_RE.search(s):
                fails.append(f"[②] 第 {i + 1} 行判断词「{hits[0]}」无锚——同句须挂 [S<n>] 或整句走态二逐字(《》与跨句不豁免)")

    # —— 道③ 禁词(正文;豁免区=无;声明本体短语先摘) ——
    for i, l in enumerate(lines):
        mb = BANNED_RE.search(NOT_INVEST_RE.sub("", l))
        if mb:
            fails.append(f"[③] 第 {i + 1} 行命中禁词「{mb.group(0)}」(零容忍无豁免)")

    # —— 道④ 数字锚/双向/政策锚/格局点评 ——
    page_text = "\n".join(lines)
    for key in sorted(set(SREF_RE.findall(page_text))):
        if not any(str(rec.get("id", "")) == f"S{key}" for _, rec in recs):
            fails.append(f"[④] 正文孤儿锚:S{key} 在 sources 不存在(④双向账)")
    for ln, rec in recs:
        rid = str(rec.get("id", ""))
        if rid and f"[{rid}]" not in page_text:
            fails.append(f"[④] sources 孤儿记录未被正文引用:{rid}")
        if rec.get("kind") == "statute":
            core = re.sub(r"^statute[:：]", "", str(rec.get("ref", "")).strip())
            if evidence_text is None:
                fails.append(f"[④] 法定锚不可核:statute 行 {rid} 未提供 --evidence,fail-closed 不放行(伪满/豁免条文机器层无从分辨,题单 B09 括号合同)")
            elif core and not evidence_hit(evidence_text, core):
                fails.append(f"[④] 法定锚不可核:statute 伪满/断链——{core[:30]!r} 不在 evidence 当场取回清单")
    head_end = marks[0] if marks else len(lines)
    for title, s, e in sections:
        kind = classify(title, "\n".join(lines[s + 1:e]))
        company_rows = 0
        for i in range(s + 1, e):
            l = lines[i]
            st = l.strip()
            if not st:
                continue
            if st.startswith("|"):
                if set(st) <= set("|-: "):
                    continue
                cs = [c.strip() for c in st.strip("|").split("|")]
                numeric = any(NUM_CELL_RE.match(c) for c in cs)
                if numeric and not SREF_RE.search(l):
                    fails.append(f"[④] 第 {i + 1} 行数字/序列行未锚:含数值而本行无 [S<n>](缺数须申报)")
                if kind == "companies":
                    company_rows += 1
            elif not st.startswith("#"):
                if kind == "companies":
                    fails.append(f"[④] 第 {i + 1} 行格局段出现点评句(只聚合不点评):{st[:24]!r}")
                residue = DATE_RE.sub("", st)
                if GUESS_RE.search(st):
                    fails.append(f"[④] 第 {i + 1} 行「{GUESS_RE.search(st).group(0)}」无源句——禁补,缺数即申报(题单 B05 合同归④)")
                elif NUM_PROSE_RE.search(residue) and not SREF_RE.search(st):
                    fails.append(f"[④] 第 {i + 1} 行数字行未锚:散文含数值而同句无 [S<n>](缺数须申报)")
        if kind == "companies":
            n = max(company_rows - 1, 0)  # 表头行不算数据行(分隔行已剔)
            if n < 3:
                fails.append(f"[④] 代表公司 {n} < 3(聚合下限,格局表数据行计数)")
    return fails


def main(argv=None):
    p = argparse.ArgumentParser(description="sector-overview 四道机检(spec §3+M46 题单)。--sources/--window 必传。")
    p.add_argument("report", help="report.md")
    p.add_argument("--sources", default=None, help="sources.jsonl(合同 §3 必传)")
    p.add_argument("--window", default=None, help="YYYY-MM-DD~YYYY-MM-DD(合同 §3 必传)")
    p.add_argument("--evidence", default=None, help="evidence/ 目录(statute 行 fail-closed:无证据即不可核)")
    args = p.parse_args(argv)
    try:
        fails = run(args)
    except Exception:
        print("FAIL: 内部异常兜底(报缺陷,勿 traceback 出院):")
        print("  - " + traceback.format_exc(limit=1).strip().splitlines()[-1])
        return 1
    if fails:
        print(f"FAIL: {args.report}（{len(fails)} 条）")
        codes = []
        for f in fails:
            c = ecode(f)
            if c not in codes:
                codes.append(c)
            print(f"  - [{c}] {f}")
        print("  码表: " + "; ".join(f"{c}→{E_LEGEND[c]}" for c in codes))
        return 1
    print(f"PASS: {args.report}（四道全过:声明/命门/禁词/形制）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
