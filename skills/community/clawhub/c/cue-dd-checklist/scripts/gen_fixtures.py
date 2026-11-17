#!/usr/bin/env python3
"""gen_fixtures.py — 重建本包 `fixtures/` 全套样（幂等生成器；stdlib only；零网络；输出不含时间戳与随机量）。

**派生纪律（不可反向）**：**改样必须先改题单**（评审方出的坏样题单，即本包验收合同），**不得反向用本脚本产出题单**。
「审方出题先于写方交卷」这条不因为存在一个生成器而翻掉：本脚本只把题单的基线与逐题差异铺成目录，
它**没有判卷权、也不产生新缺陷**。加题流程 = 评审方写题 → 写方在此加一个 `build("bad-…")` 调用 → 出门时按题单重建逐题对账表。

**复现性以 `scripts/fixtures/run_fixtures.sh` 为准**：包内自带成品样与 runner，正常评审、判卷、外部使用者跑的都是成品样。
题单在评审方仓库、不随本包发布；**没有题单就不需要跑本脚本**——要重铺（加题或回归）时把题单路径作为必填参数传进来：

    python3 scripts/gen_fixtures.py --badspec <题单.md 路径>

脚本会按题单 §4 覆盖矩阵做**题号↔样号双向断言**（缺题或多样即报错不出货），并对控制样做**题单点名→盘上在场**的单向断言
（题单以行内代码点名的每一枚控制都必须在盘上，缺席即报错不出货；盘上历史控制可多于点名，计数如实分开报出），并保证跑一次字节级复现当前成品（幂等）。
"""
import argparse
import hashlib
import io
import json
import pathlib
import re
import shutil
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent / "fixtures"
MATRIX_ROW = re.compile(r"^\|\s*(DD-[BX]\d{1,2}[a-c]?)\s*\|")
CTL_ID = re.compile(r"`(ctl-[a-z][a-z0-9-]*)`")


def matrix_ids(badspec: pathlib.Path) -> set:
    """从题单 §4 覆盖矩阵反读题号集合（双向断言用）。"""
    return {m.group(1) for ln in badspec.read_text(encoding="utf-8").splitlines()
            if (m := MATRIX_ROW.match(ln))}


def matrix_ctl_names(badspec: pathlib.Path) -> set:
    """从题单反读**带反引号**的控制样号（控制缺席不背书用）。

    题单只在「控制」题面里以行内代码写出样号，散文提法（如裸 `ctl-` 前缀）不算一名。
    """
    return {m.group(1) for ln in badspec.read_text(encoding="utf-8").splitlines() for m in CTL_ID.finditer(ln)}
SUBJECT = "北辰股份有限公司（600001.SH）"
SUBJ_FULL, SUBJ_CODE = "北辰股份有限公司", "600001.SH"
ASOF = "2026-09-21"
START = "2023-09-21"
ANCHOR = "AN202605100000000001"
FACT = "交易所出具监管函，披露所载为问询事项"
# SKILL §3 钉死的权威句式（机检核「在场 + 位于标题后前 5 行内 + 两类语义」，语义抽读归人工）
CALLS = "calls.jsonl"
DECL = "> 本页为 AI 初稿，依据公开披露与法定原文整理，不构成投资建议，也不构成法律意见；判断位 [待人工]。"

HDR = "| 日期 | 类目 | 事实(≤40字,只写披露所载) | 影响档位 | 状态 | 窗外余档 | 来源锚 |"
SEP = "|---|---|---|---|---|---|---|"
# 五列覆盖账的固定文法（§v2-15②/§v2-16①）：与上面七列风险表是两张表，不得互相顶名
LEDGER_HDR = "| 类目 | 所需域/工具 | 本次实际调用 | 结果 | 注记 |"
LEDGER_SEP = "|---|---|---|---|---|"
LEDGER_ROW_EQ = "| 股权与控制权 | entity_data | entity_data | 检到 0 | 无新增带锚事项 |"
D = "2026-05-10"


def row(date, category, fact, impact, status, carry, anchor):
    return f"| {date} | {category} | {fact} | {impact} | {status} | {carry} | {anchor} |"


BASE_ROW = row(D, "合规与处罚", FACT, "关注", "已披露", "—", ANCHOR)


def age_decl(start, end, cap="365d", beyond="未按类目互校"):
    """§v2-11 账龄申报行（6.1 判词第 4 条：宽窗基线一律带；删它=DD-X19 唯一缺陷，改 beyond=ctl 洗白样）。"""
    return f"类目账龄申报: requested={start}~{end} | disclosure_cn={cap} | beyond={beyond}"


def report(rows=(BASE_ROW,), title_start=START, title_end=ASOF, title_subject=SUBJECT, extra="",
           domain_line="regulatory_cn 1 域 / 无工具项: 0", asof=ASOF, subject_line=SUBJECT, cond_line=None,
           no_decl=False, decl_late=False, decl_split=None, lookback="36m",
           age_start=None, age_beyond="未按类目互校", age_cap="365d", no_age=False, age_extra=None, title_mid=""):
    if domain_line and not domain_line.startswith("本节检索域"):
        domain_line = "本节检索域: " + domain_line
    age = [] if no_age else ["", age_decl(age_start or title_start, title_end, cap=age_cap, beyond=age_beyond)]
    if age_extra:
        age.append(age_extra)
    if decl_split:
        head = [f"# {title_subject}公开信息预尽调清单{title_mid} · 窗口 {title_start}~{title_end}", ""] + decl_split
        if not no_decl:
            head += ["", DECL]
        head += ["", f"- subject: {subject_line}", f"- asof: {asof}", f"- lookback: {lookback}", "- purpose: investment", "", HDR, SEP]
        return "\n".join(head + [*(rows or [BASE_ROW]), "", domain_line, *age]) + "\n"
    lines = [
        f"# {title_subject}公开信息预尽调清单{title_mid} · 窗口 {title_start}~{title_end}",
        "",
        *([] if (no_decl or decl_late) else [DECL, ""]),
        f"- subject: {subject_line}",
        f"- asof: {asof}",
        f"- lookback: {lookback}",
        "- purpose: investment",
        "",
        HDR,
        SEP,
        *rows,
        "",
        domain_line,
        *age,
    ]
    if cond_line:
        lines += ["", cond_line]
    if extra:
        lines += ["", extra]
    return "\n".join(lines) + "\n"


def src(sid="S1", domain="regulatory_cn", ref=ANCHOR, claim="北辰股份有限公司收到监管函，事项见公告原文", conf="L1", asof=D, extra=None):
    obj = {"id": sid, "kind": domain, "ref": ref, "claim": claim, "confidence": conf, "asof": asof}
    if extra:
        obj.update(extra)
    return json.dumps(obj, ensure_ascii=False)


def evid(domain="regulatory_cn", date=D, anchor=ANCHOR, fact=FACT, subjects=(SUBJECT,), category="合规与处罚", extra=None):
    payload = {
        "domain": domain,
        "category": category,
        "asof": date,
        "records": [{"公告索引号": anchor, "出具日期": date, "对象": list(subjects), "披露所载": fact}],
    }
    if extra:
        payload.update(extra)
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


COV_ROWS = [
    ("股权与控制权", "entity_data", "entity_data", "检到 0", "无新增带锚事项"),
    ("合规与处罚", "regulatory_cn", "regulatory_cn", "检到 1", ANCHOR),
    ("诉讼与仲裁", "disclosure_cn", "disclosure_cn", "检到 0", "公开披露检到零条"),
    ("财务与披露质量", "fr_fact_index", "fr_fact_index", "检到 0", "公开披露检到零条"),
    ("关联交易与资金占用", "disclosure_cn", "disclosure_cn", "检到 0", "公开披露检到零条"),
    ("业务资质与许可", "disclosure_cn", "disclosure_cn", "检到 0", "公开披露检到零条"),
    ("人力与社保", "—", "—", "无工具", "域面外，需人工/商用库"),
    ("上市与在审状态", "ipo", "ipo", "检到 0", "公开披露检到零条"),
    ("其他已披露重大事项", "disclosure_cn", "disclosure_cn", "检到 0", "公开披露检到零条"),
]


ZERO_CALLS = {
    "股权与控制权": "entity_data",
    "诉讼与仲裁": "disclosure_cn",
    "财务与披露质量": "fr_fact_index",
    "关联交易与资金占用": "disclosure_cn",
    "业务资质与许可": "disclosure_cn",
    "上市与在审状态": "ipo",
    "其他已披露重大事项": "disclosure_cn",
}


def zero_snapshots(queried=(), asof=ASOF, start=START):
    """§v2-2②：每个「检到 0/零条」的已调用域都要有一份原始零结果快照（件内标出类目与窗口）。"""
    out = {}
    for cat, dom in ZERO_CALLS.items():
        if cat in queried:
            continue
        out[f"{dom}-Z-{cat}.json"] = json.dumps({
            "domain": dom,
            "category": cat,
            "asof": asof,
            "window": f"{start}~{asof}",
            "query": f"{SUBJECT} {cat}",
            "records": [],
            "结果": "检到 0",
        }, ensure_ascii=False, indent=2) + "\n"
    return out


def cov(rows=COV_ROWS):
    lines = [LEDGER_HDR, LEDGER_SEP]
    lines += [f"| {a} | {b} | {c} | {d} | {e} |" for a, b, c, d, e in rows]
    return "\n".join(lines) + "\n"


def cov_set(updates):
    """updates: {类目: (结果, 注记) | (结果, 注记, 所需域, 实际调用)}"""
    out = []
    for a, b, c, d, e in COV_ROWS:
        if a in updates:
            v = updates[a]
            if len(v) == 2:
                out.append((a, b, c, v[0], v[1]))
            else:
                out.append((a, v[2], v[3], v[0], v[1]))
        else:
            out.append((a, b, c, d, e))
    return out


def cmd(asof=ASOF, lookback="36m", purpose="investment", subject=SUBJECT, drop=()):
    parts = ["python3 ../../check_dd.py report.md"]
    if "subject" not in drop:
        parts.append(f"--subject '{subject}'")
    if "asof" not in drop:
        parts.append(f"--asof {asof}")
    if "lookback" not in drop:
        parts.append(f"--lookback {lookback}")
    if "purpose" not in drop:
        parts.append(f"--purpose {purpose}")
    if "sources" not in drop:
        parts.append("--sources sources.jsonl")
    if "evidence" not in drop:
        parts.append("--evidence evidence")
    return " ".join(parts) + "\n"


def cell_tokens(called):
    """§v2-16② 生成器侧镜像：把「本次实际调用」格解析成域记号序列（单记号或顿号连记号）。

    与门内 `parse_called()` 同形制；非集合拼接（逗号/空格/斜杠）留在原串里，由门判非法域。
    """
    toks = [t.strip() for t in called.split("、")] if "、" in called else [called.strip()]
    return [t for i, t in enumerate(toks) if t in KINDS and t not in toks[:i]]


def queried_ledger_rows(coverage):
    """账表里「本次实际调用」是合法域的行（即声称查过）——这些行都要有流水；多域格逐域各一行。"""
    out = []
    for ln in coverage.splitlines():
        if not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 5 or cells[0] == "类目" or set(cells[3]) <= {"-"}:
            continue
        if re.fullmatch(r"检到\s*\d+|零条", cells[3]):
            out += [(cells[0], dom) for dom in cell_tokens(cells[2])]
    return out


def ledger_zero_rows(coverage):
    """读账表本身：凡 结果=检到 0/零条 且「本次实际调用」是合法域 的行，都要有对应零结果快照（多域格逐域各一份）。"""
    out = []
    for ln in coverage.splitlines():
        if not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 5 or cells[0] in ("类目", "") or set(cells[3]) <= {"-"}:
            continue
        if re.fullmatch(r"检到\s*0", cells[3]):
            out += [(cells[0], dom) for dom in cell_tokens(cells[2])]
    return out


def build(case, rep, sources, evidence, coverage, command, expect, need, empty_evidence=False, progress=None, flow=None,
          flow_from=None, flow_drop_field=None, flow_set_domain=None, flow_extra=()):
    # §v2-15③ 用：真实查过的账（flow_from）与被洗过的账（coverage）可以是两份——流水照真实那份生成，快照齐备
    truth = flow_from or coverage
    missing = [(cat, dom) for cat, dom in ledger_zero_rows(truth)
               if not any(re.sub(r"\.json$", "", n).startswith(dom + "-") and cat in b for n, b in evidence.items())]
    evidence = {**zero_snapshots(tuple(cat for cat, _ in ledger_zero_rows(truth))), **evidence,
                **{f"{dom}-Z-{cat}.json": json.dumps({"domain": dom, "category": cat, "asof": ASOF, "window": f"{START}~{ASOF}",
                                                      "query": f"{SUBJECT} {cat}", "records": [], "结果": "检到 0"}, ensure_ascii=False, indent=2) + "\n"
                   for cat, dom in missing}}
    d = ROOT / case
    if d.exists():
        shutil.rmtree(d)
    (d / "evidence").mkdir(parents=True)
    (d / "references").mkdir(parents=True)
    (d / "report.md").write_text(rep, encoding="utf-8")
    (d / "sources.jsonl").write_text("\n".join(sources) + "\n", encoding="utf-8")
    ledger = []
    for name, body in evidence.items():
        p = d / "evidence" / name
        p.write_text(body, encoding="utf-8")
        ledger.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {name}")
    if empty_evidence:
        for p in (d / "evidence").glob("*.json"):
            p.unlink()
        (d / "evidence" / ".gitkeep").write_text("", encoding="utf-8")
    elif ledger:
        (d / "evidence" / "LEDGER.sha256").write_text("\n".join(ledger) + "\n", encoding="utf-8")
    if not empty_evidence:
        # §v2-10 调用流水：每类目每次查询一行，承载原始命中 M 与快照真哈希
        calls = []
        rows_by_cat = {}
        for ln in rep.splitlines():
            cells = [c.strip() for c in ln.strip().strip("|").split("|")] if ln.strip().startswith("|") else []
            if len(cells) == 7 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells[0]):
                rows_by_cat[cells[1]] = rows_by_cat.get(cells[1], 0) + 1
        for cat, dom in queried_ledger_rows(truth):
            hits = (flow or {}).get(cat, rows_by_cat.get(cat, 0))
            snap = next((n for n, b in evidence.items()
                         if n.startswith(dom + "-") and json.loads(b).get("category") == cat), next(iter(evidence), ""))
            calls.append({
                "category": cat, "domain": dom, "query": f"{SUBJECT} {cat} {START}~{ASOF}",
                "hits": hits, "snapshot": snap,
                "snapshot_sha256": hashlib.sha256(evidence[snap].encode("utf-8")).hexdigest() if snap in evidence else "",
            })
        for extra in flow_extra:      # §v2-16② 双域正路：账格合法但 truth 账只记单域时，多出的那次真实调用手动补在链尾
            dom, cat = extra["domain"], extra["category"]
            snap = extra.get("snapshot") or next((n for n, b in evidence.items()
                                                  if n.startswith(dom + "-") and json.loads(b).get("category") == cat), "")
            calls.append({"category": cat, "domain": dom, "query": extra.get("query", f"{SUBJECT} {cat} {START}~{ASOF}"),
                          "hits": extra.get("hits", 0), "snapshot": snap,
                          "snapshot_sha256": hashlib.sha256(evidence[snap].encode("utf-8")).hexdigest() if snap in evidence else ""})
        if calls:
            chained, prev = [], "0" * 64
            for i, c in enumerate(calls, start=1):
                row = dict(c)
                row["seq"] = i
                row["prev_sha256"] = prev
                if flow_drop_field and row.get("category") == flow_drop_field[1]:
                    row.pop(flow_drop_field[0], None)      # 例：("hits", "合规与处罚") 删正命中流水的 M 再重算链
                if flow_set_domain and i == len(calls):
                    row["domain"] = flow_set_domain        # 末条改域、快照不动 → 域↔快照前缀失配
                raw = json.dumps(row, ensure_ascii=False, sort_keys=True)
                chained.append(raw)
                prev = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            (d / "evidence" / CALLS).write_text("\n".join(chained) + "\n", encoding="utf-8")
    if progress is not None:
        (d / "progress.md").write_text(progress, encoding="utf-8")
    (d / "references" / "coverage-map.md").write_text(coverage, encoding="utf-8")
    (d / "cmd.txt").write_text(command, encoding="utf-8")
    (d / "expect.txt").write_text(f"exit={expect}\n" + "".join(f"need={n}\n" for n in need), encoding="utf-8")


KINDS = ("entity_data", "disclosure_cn", "regulatory_cn", "statute", "ipo", "fr_fact_index",
         "fr_footnote", "buyback", "esop", "research", "omni", "user_supplied")

BASE_EVID = {"regulatory_cn-S1.json": evid()}
COND_ANCHOR = "AN202603310000000009"
LAW = "《合成示例披露规则（守护样专用）》"
STAT_AN = f"statute:{LAW}第三条（报告期后30日）"

# ---------------------------------------------------------------- 正路守护样 ×5
# 【M250】参数解析必须在**任何写盘之前**——本文件下方的 build() 全是模块级语句，
# 原先 argparse 块排在第一枚 build() 之后，于是 `--help` 也会先铺 103 枚散件再打印帮助。
# 现在把解析（含题单可读性检查）挪到第一枚 build() 之前：`--help`／无参调用**一个字节都不写盘**。
# 生成路径与产物 sha 未变（产生与复算同源那套形制照旧，见文件头派生纪律）。
ap = argparse.ArgumentParser(description="重铺 fixtures（需题单路径，无默认值）")
ap.add_argument("--badspec", required=True, help="评审方题单（本包验收合同）的 Markdown 路径")
ap.add_argument("--keep-loose", action="store_true",
                help="审计形：铺完散件就停（不封档、不删散件）。交付形不带这个——渠道条数闸要的是档案")
_args = ap.parse_args()
_badspec = pathlib.Path(_args.badspec)
if not _badspec.is_file():
    print(f"题单不可读：{_badspec}——本脚本不做默认路径，也不产出题单", file=sys.stderr)
    sys.exit(2)

build("good-baseline", report(), [src()], BASE_EVID, cov(), cmd(), 0, ())

GAW = [
    ("2024-03-15", "诉讼与仲裁", "披露所载一起民事诉讼立案，案号见原文", "关注", "已披露", "（2024）京0108民初12345号", "disclosure_cn", "S1"),
    ("2025-06-20", "股权与控制权", "公告所载控股股东持股比例变动", "背景", "已披露", "https://disclosure.invalid/2025-06-20-001", "entity_data", "S2"),
    ("2026-02-10", "合规与处罚", "交易所出具监管函，披露所载为问询事项", "关注", "已披露", "上证监管函〔2026〕12号", "regulatory_cn", "S3"),
    ("2026-05-10", "合规与处罚", "交易所出具监管函，披露所载为问询事项", "关注", "已披露", ANCHOR, "regulatory_cn", "S4"),
    ("2026-07-01", "上市与在审状态", "研究件转述在审状态，原文见会话记录", "背景", "已披露", "conv_id:op_synthetic0001", "research", "S5"),
    ("2026-08-05", "关联交易与资金占用", "董事会审议通过关联交易议案，所载为金额与对手方", "关注", "已披露", "AN202608050000000003", "disclosure_cn", "S6"),
]
gaw_srcs, gaw_ev = [], {}
for d, c, f, imp, st, an, kind, sid in GAW:
    extra = {"conv_id": "op_synthetic0001"} if kind == "research" else None
    gaw_srcs.append(src(sid, domain=kind, ref=an, claim=f"北辰股份有限公司{c}事项：{f}", asof=d, extra=extra))
    gaw_ev[f"{kind}-{sid}.json"] = evid(domain=kind, date=d, anchor=an, fact=f, category=c)
build("good-anchors-wide",
      report(rows=tuple(row(d, c, f, imp, st, "—", an) for d, c, f, imp, st, an, _k, _s in GAW),
             domain_line="disclosure_cn、regulatory_cn、entity_data、research 4 域 / 无工具项: 0"),
      gaw_srcs, gaw_ev,
      cov(cov_set({"股权与控制权": ("检到 1", "https://disclosure.invalid/2025-06-20-001"),
                   "合规与处罚": ("检到 2", "两条带锚监管函"),
                   "诉讼与仲裁": ("检到 1", "（2024）京0108民初12345号"),
                   "关联交易与资金占用": ("检到 1", "AN202608050000000003"),
                   "上市与在审状态": ("检到 1", "conv_id:op_synthetic0001", "research", "research")})),
      cmd(), 0, ())

GSD_ROWS = (row("2026-04-30", "财务与披露质量", "依披露规则第三条推得报告期后30日应披露日", "关注", "推导", "—", STAT_AN), BASE_ROW)
gsd_srcs = [src(), src("S2", domain="statute", ref=STAT_AN, claim="合成示例披露规则第三条载明报告期后30日", asof="2026-04-30"),
            src("S3", domain="disclosure_cn", ref=COND_ANCHOR, claim="北辰股份有限公司 2026 年第一季度报告期截止 2026-03-31", asof="2026-03-31")]
gsd_ev = {**BASE_EVID,
          "statute-S2.json": json.dumps({"domain": "statute", "category": "财务与披露质量", "note": "合成样例，非真实法条原文；P-10：statute 域不含部门规章与交易所规则，真实跑此路径预期零锚",
                                         "records": [{"法名": LAW, "条号": "第三条", "原文": "信息披露义务人应当在报告期后30日内披露定期报告。"}]}, ensure_ascii=False, indent=2) + "\n",
          "disclosure_cn-S3.json": evid(domain="disclosure_cn", date="2026-03-31", anchor=COND_ANCHOR, fact="一季报报告期截止日 2026-03-31", category="财务与披露质量")}
build("good-statute-derive", report(rows=GSD_ROWS, domain_line="regulatory_cn、statute、disclosure_cn 3 域 / 无工具项: 0", cond_line=f"推导条件: {COND_ANCHOR}（报告期 2026-03-31 在场披露）"),
      gsd_srcs, gsd_ev, cov(cov_set({"合规与处罚": ("检到 1", ANCHOR), "财务与披露质量": ("检到 1", STAT_AN, "statute", "statute")})),
      cmd(), 0, ())

build("good-zero-entries-evidence-backed",
      report(rows=(), domain_line="regulatory_cn、entity_data、disclosure_cn、fr_fact_index、ipo 5 域 / 无工具项: 0"),
      [], BASE_EVID,
      cov([("股权与控制权", "entity_data", "entity_data", "检到 0", "零结果快照见 evidence"),
           ("合规与处罚", "regulatory_cn", "regulatory_cn", "检到 0", "零结果快照见 evidence"),
           ("诉讼与仲裁", "disclosure_cn", "disclosure_cn", "检到 0", "零结果快照见 evidence"),
           ("财务与披露质量", "fr_fact_index", "fr_fact_index", "检到 0", "零结果快照见 evidence"),
           ("关联交易与资金占用", "disclosure_cn", "disclosure_cn", "检到 0", "零结果快照见 evidence"),
           ("业务资质与许可", "disclosure_cn", "disclosure_cn", "检到 0", "零结果快照见 evidence"),
           ("人力与社保", "—", "—", "无工具", "域面外，需人工/商用库"),
           ("上市与在审状态", "ipo", "ipo", "检到 0", "零结果快照见 evidence"),
           ("其他已披露重大事项", "disclosure_cn", "disclosure_cn", "检到 0", "零结果快照见 evidence")]),
      cmd(), 0, ())

build("good-subject-code-only",
      report(subject_line="600001.SH", rows=(row(D, "合规与处罚", "北辰股份收到监管函，事项见公告", "关注", "已披露", "—", ANCHOR),)),
      [src(claim="北辰收到监管函，事项见公告")],
      {"regulatory_cn-S1.json": evid(fact="北辰股份有限公司（600001.SH）收到监管函，披露所载为问询事项")},
      cov(), cmd(subject="600001.SH"), 0, ())

# ---------------------------------------------------------------- 18 族（DD-B01…B24）
B03_COV = cov_set({"合规与处罚": ("检到 0", "无新增带锚事项"), "财务与披露质量": ("检到 1", ANCHOR)})
B10_EXTRA = ("## 海岳股份有限公司（600002.SH）\n\n" + HDR + "\n" + SEP + "\n"
             + row(D, "合规与处罚", FACT, "关注", "已披露", "—", "AN202605100000000002")
             + "\n\n本节检索域: regulatory_cn 1 域 / 无工具项: 0")
B12_ROWS = (row("2026-05-10", "合规与处罚", FACT, "关注", "已披露", "—", ANCHOR),
            row("2025-05-10", "合规与处罚", "披露所载一项历史问询事项", "背景", "已披露", "—", "AN202505100000000001"))
B21_ROW = row("2026-10-20", "财务与披露质量", "按报告期后30日推得应披露日", "关注", "推导", "—", "AN202610010000000001")
B22_ROW = row("2026-04-30", "财务与披露质量", "按一季报后30日推得应披露日", "关注", "推导", "—", STAT_AN)
LONG_FACT = "交易所出具监管函，披露所载为关于收入确认、合同履约、内部控制与关联交易多项连续问询事项"

build("bad-B01-anchor-missing", report(rows=[row(D, "合规与处罚", FACT, "关注", "已披露", "—", "—")]), [src()], BASE_EVID, cov(), cmd(), 1, ("DD-ROW",))
build("bad-B02-amount-as-anchor", report(rows=[row(D, "合规与处罚", "披露所载处罚金额为120000000元", "关注", "已披露", "—", "—")]), [src()], BASE_EVID, cov(), cmd(), 1, ("DD-ROW",))
B03_EVID = {"regulatory_cn-S1.json": evid(category="财务与披露质量")}
build("bad-B03-confession-words", report(rows=[row(D, "财务与披露质量", "通常预计该主体大概率存在披露延迟", "关注", "推测", "—", ANCHOR)]),
      [src()], B03_EVID, cov(B03_COV), cmd(), 1, ("DD-ROW",))
build("bad-B04-category-outside", report(rows=[row(D, "供应链风险", FACT, "关注", "已披露", "—", ANCHOR)]), [src()], BASE_EVID, cov(), cmd(), 1, ("DD-TABLE",))
build("bad-B05-impact-carries-advice", report(rows=[row(D, "合规与处罚", FACT, "建议回避", "已披露", "—", ANCHOR)]), [src()], BASE_EVID, cov(), cmd(), 1, ("DD-TABLE", "DD-REDLINE"))
build("bad-B06-investment-words", report(rows=[row(D, "合规与处罚", "据此可投，目标价应下调", "关注", "已披露", "—", ANCHOR)]), [src()], BASE_EVID, cov(), cmd(), 1, ("DD-REDLINE",))
build("bad-B07-legal-opinion", report(rows=[row(D, "合规与处罚", "该事项构成违法，应被处罚", "关注", "已披露", "—", ANCHOR)]), [src()], BASE_EVID, cov(), cmd(), 1, ("DD-REDLINE",))
build("bad-B08-completeness-claim", report(extra="以上已覆盖全部风险，尽调完成。"), [src()], BASE_EVID, cov(), cmd(), 1, ("DD-REDLINE",))
build("bad-B09-notool-to-nothing", report(extra="人力与社保和诉讼域面无工具，因此北辰股份无诉讼。"), [src()], BASE_EVID, cov(), cmd(), 1, ("DD-COVERAGE",))
build("bad-B10-multi-subject", report(extra=B10_EXTRA),
      [src(), src("S2", ref="AN202605100000000002", claim="海岳股份有限公司收到监管函，事项见公告原文")],
      {**BASE_EVID, "regulatory_cn-S2.json": evid(anchor="AN202605100000000002", subjects=("海岳股份有限公司（600002.SH）",))},
      cov(cov_set({"合规与处罚": ("检到 2", "两主体各一条带锚事项")})), cmd(), 1, ("DD-INPUT",))
build("bad-B11-naked-row", "\n".join([f"# {SUBJECT}公开信息预尽调清单 · 窗口 {START}~{ASOF}", "", DECL, "", f"- subject: {SUBJECT}", f"- asof: {ASOF}",
                                      "- lookback: 36m", "- purpose: investment", "", BASE_ROW, "", "本节检索域: regulatory_cn 1 域 / 无工具项: 0", "", age_decl(START, ASOF)]) + "\n",
      [src()], BASE_EVID, cov(), cmd(), 1, ("DD-TABLE",))
build("bad-B12-date-order", report(rows=B12_ROWS),
      [src(), src("S2", ref="AN202505100000000001", claim="北辰股份有限公司历史问询事项，见公告原文", asof="2025-05-10")],
      {**BASE_EVID, "regulatory_cn-S2.json": evid(date="2025-05-10", anchor="AN202505100000000001", fact="披露所载一项历史问询事项")},
      cov(cov_set({"合规与处罚": ("检到 2", "两条带锚事项")})), cmd(), 1, ("DD-TABLE",))
build("bad-B13-evidence-empty", report(), [src()], BASE_EVID, cov(), cmd(), 1, ("DD-EVIDENCE",), empty_evidence=True)
build("bad-B14-sha-mismatch", report(), [src()], BASE_EVID, cov(), cmd(), 1, ("DD-EVIDENCE",))
(ROOT / "bad-B14-sha-mismatch" / "evidence" / "LEDGER.sha256").write_text(
    "0000000000000000000000000000000000000000000000000000000000000000  regulatory_cn-S1.json\n", encoding="utf-8")
build("bad-B15-kind-illegal", report(), [src(domain="论坛传闻")], BASE_EVID, cov(), cmd(), 1, ("DD-EVIDENCE",))
build("bad-B16-confidence-illegal", report(), [src(conf="L9")], BASE_EVID, cov(), cmd(), 1, ("DD-EVIDENCE",))
build("bad-B17-asof-illegal", report(), [src(asof="2026/05/10")], BASE_EVID, cov(), cmd(), 1, ("DD-EVIDENCE",))
build("bad-B18-title-window-drift", report(title_start="2023-09-01"), [src()], BASE_EVID, cov(), cmd(), 1, ("DD-INPUT",))
build("bad-B19-missing-purpose", report(), [src()], BASE_EVID, cov(), cmd(drop=("purpose",)), 1, ("DD-INPUT",))
build("bad-B20-missing-evidence", report(), [src()], BASE_EVID, cov(), cmd(drop=("evidence",)), 1, ("DD-INPUT",))
build("bad-B21-derive-no-statute", report(rows=(B21_ROW,), title_end="2026-10-31", title_start="2023-10-31", asof="2026-10-31",
                                          domain_line="disclosure_cn 1 域 / 无工具项: 0"),
      [src("S1", domain="disclosure_cn", ref="AN202610010000000001", claim="北辰股份有限公司披露一期定期报告安排", asof="2026-10-20")],
      {"disclosure_cn-S1.json": evid(domain="disclosure_cn", date="2026-10-20", anchor="AN202610010000000001", fact="按报告期后30日推得应披露日", category="财务与披露质量")},
      cov(cov_set({"合规与处罚": ("检到 0", "无新增带锚事项"), "财务与披露质量": ("检到 1", "AN202610010000000001", "disclosure_cn", "disclosure_cn")})),
      cmd(asof="2026-10-31"), 1, ("DD-STATUTE",))
build("bad-B22-statute-fake", report(rows=(B22_ROW,), domain_line="statute 1 域 / 无工具项: 0", cond_line=f"推导条件: {COND_ANCHOR}（报告期 2026-03-31 在场披露）"),
      [src("S2", domain="statute", ref=STAT_AN, claim="合成示例披露规则第三条载明报告期后30日", asof="2026-04-30"),
       src("S3", domain="disclosure_cn", ref=COND_ANCHOR, claim="北辰股份有限公司一季报报告期截止 2026-03-31", asof="2026-03-31")],
      {"statute-S2.json": evid(domain="disclosure_cn", date="2026-04-30", anchor=ANCHOR, fact="公司披露一季报安排公告", category="财务与披露质量"),
       "disclosure_cn-S3.json": evid(domain="disclosure_cn", date="2026-03-31", anchor=COND_ANCHOR, fact="报告期截止日", category="财务与披露质量")},
      cov(cov_set({"合规与处罚": ("检到 0", "无新增带锚事项"), "财务与披露质量": ("检到 1", STAT_AN, "statute", "statute")})),
      cmd(), 1, ("DD-STATUTE",))
build("bad-B23-evidence-other-subject", report(rows=[row(D, "合规与处罚", "北辰收到监管函，事项见公告", "关注", "已披露", "—", ANCHOR)]),
      [src(claim="北辰收到监管函，事项见公告")],
      {"regulatory_cn-S1.json": evid(subjects=("北辰控股有限公司（600100.SH）",), fact="北辰控股有限公司收到监管函")},
      cov(), cmd(), 1, ("DD-ROW",))
build("bad-B24-shortname-collision", report(rows=[row(D, "合规与处罚", "北辰收到监管函，事项见公告", "关注", "已披露", "—", ANCHOR)]),
      [src(claim="北辰收到监管函，事项见公告")],
      {"regulatory_cn-S1.json": evid(subjects=("北辰科技股份有限公司（600100.SH）", "北辰新材股份有限公司（600101.SH）"), fact="两家含「北辰」字号的主体同日收到监管函")},
      cov(), cmd(), 1, ("DD-ROW",))

# ---------------------------------------------------------------- 6.1 加题（X01…X14）
build("bad-X01-date-outside-window", report(rows=[row("2023-09-20", "合规与处罚", FACT, "关注", "已披露", "—", ANCHOR)]),
      [src(asof="2023-09-20")], {"regulatory_cn-S1.json": evid(date="2023-09-20")}, cov(), cmd(), 1, ("DD-ROW",))
build("bad-X02-anchor-in-fact-only", report(rows=[row(D, "合规与处罚", "公告AN202605100000000001载明问询事项", "关注", "已披露", "—", "—")]),
      [src()], BASE_EVID, cov(), cmd(), 1, ("DD-ROW",))
build("bad-X03-anchor-multi-parse", report(), [src(), src("S2", domain="disclosure_cn", claim="同一公告的第二条冲突记录")], BASE_EVID, cov(), cmd(), 1, ("DD-EVIDENCE",))
build("bad-X04-evidence-wrong-anchor", report(), [src()],
      {"regulatory_cn-S1.json": evid(anchor="AN202605110000000002", fact="另一事项的公告原文")}, cov(), cmd(), 1, ("DD-EVIDENCE",))
build("bad-X05-header-renamed", report().replace(HDR, HDR.replace("来源锚", "来源")), [src()], BASE_EVID, cov(), cmd(), 1, ("DD-TABLE",))
build("bad-X06-fact-too-long", report(rows=[row(D, "合规与处罚", LONG_FACT, "关注", "已披露", "—", ANCHOR)]),
      [src()], {"regulatory_cn-S1.json": evid(fact=LONG_FACT)}, cov(), cmd(), 1, ("DD-TABLE",))
build("bad-X07-coverage-missing-row", report(), [src()], BASE_EVID,
      cov([r for r in COV_ROWS if r[0] != "人力与社保"]), cmd(), 1, ("DD-COVERAGE",))
build("bad-X08-fake-zero-entries", report(rows=(), domain_line="entity_data、disclosure_cn、regulatory_cn、ipo、fr_fact_index 5 域 / 无工具项: 0"),
      [src()], BASE_EVID,
      cov([("股权与控制权", "entity_data", "—", "检到 0", "伪零条"),
           ("合规与处罚", "regulatory_cn", "—", "检到 0", "伪零条"),
           ("诉讼与仲裁", "disclosure_cn", "—", "检到 0", "伪零条"),
           ("财务与披露质量", "fr_fact_index", "—", "检到 0", "伪零条"),
           ("关联交易与资金占用", "disclosure_cn", "—", "检到 0", "伪零条"),
           ("业务资质与许可", "disclosure_cn", "—", "检到 0", "伪零条"),
           ("人力与社保", "—", "—", "无工具", "域面外，需人工/商用库"),
           ("上市与在审状态", "ipo", "—", "检到 0", "伪零条"),
           ("其他已披露重大事项", "disclosure_cn", "—", "检到 0", "伪零条")]),
      cmd(), 1, ("DD-COVERAGE",))
X09_EVID = {"regulatory_cn-S1.json": evid(category="其他已披露重大事项")}
build("bad-X09-refile-to-other", report(rows=[row(D, "其他已披露重大事项", FACT, "背景", "已披露", "—", ANCHOR)]),
      [src()], X09_EVID, cov(cov_set({"合规与处罚": ("检到 0", "无新增带锚事项"), "其他已披露重大事项": ("检到 1", ANCHOR)})),
      cmd(), 1, ("DD-TABLE",))
build("bad-X10-redline-in-ledger", report(), [src()], BASE_EVID,
      cov([r if r[0] != "合规与处罚" else ("合规与处罚", "regulatory_cn", "regulatory_cn", "检到 1", "监管函在场，建议回避") for r in COV_ROWS]),
      cmd(), 1, ("DD-REDLINE",))
X11_SRC = [src(), src("S2", domain="disclosure_cn", ref=STAT_AN, claim="合成示例披露规则第三条载明报告期后30日", asof="2026-04-30"),
           src("S3", domain="disclosure_cn", ref=COND_ANCHOR, claim="北辰股份有限公司一季报报告期截止 2026-03-31", asof="2026-03-31")]
X11_EV = {**BASE_EVID,
          "statute-S2.json": json.dumps({"domain": "statute", "category": "财务与披露质量", "note": "合成样例，非真实法条原文",
                                         "records": [{"法名": LAW, "条号": "第三条", "原文": "信息披露义务人应当在报告期后30日内披露定期报告。"}]}, ensure_ascii=False, indent=2) + "\n",
          "disclosure_cn-S3.json": evid(domain="disclosure_cn", date="2026-03-31", anchor=COND_ANCHOR, fact="报告期截止日", category="财务与披露质量")}
X11_REP = report(rows=GSD_ROWS, domain_line="regulatory_cn、statute、disclosure_cn 3 域 / 无工具项: 0", cond_line=f"推导条件: {COND_ANCHOR}（报告期 2026-03-31 在场披露）")
X11_COV = cov(cov_set({"合规与处罚": ("检到 1", ANCHOR), "财务与披露质量": ("检到 1", STAT_AN, "statute", "statute")}))
build("bad-X11-statute-wrong-kind", X11_REP, X11_SRC, X11_EV, X11_COV, cmd(), 1, ("DD-STATUTE",))
build("bad-X12-statute-cross-file", X11_REP, [src(), src("S2", domain="statute", ref=STAT_AN, claim="合成示例披露规则第三条", asof="2026-04-30"), src("S3", domain="disclosure_cn", ref=COND_ANCHOR, claim="北辰股份有限公司一季报报告期截止 2026-03-31", asof="2026-03-31")],
      {**BASE_EVID,
       "statute-S2.json": json.dumps({"domain": "statute", "category": "财务与披露质量", "records": [{"法名": LAW, "条号": "第三条"}]}, ensure_ascii=False, indent=2) + "\n",
       "statute-S3.json": json.dumps({"domain": "statute", "category": "财务与披露质量", "records": [{"法名": "《另一部合成规则》", "条号": "第七条", "原文": "信息披露义务人应当在报告期后30日内披露。"}]}, ensure_ascii=False, indent=2) + "\n",
       "disclosure_cn-S3.json": evid(domain="disclosure_cn", date="2026-03-31", anchor=COND_ANCHOR, fact="报告期截止日", category="财务与披露质量")},
      X11_COV, cmd(), 1, ("DD-STATUTE",))
build("bad-X13-no-subject-condition", X11_REP, [src(), src("S2", domain="statute", ref=STAT_AN, claim="合成示例披露规则第三条载明报告期后30日", asof="2026-04-30")],
      {**BASE_EVID, "statute-S2.json": X11_EV["statute-S2.json"]}, X11_COV, cmd(), 1, ("DD-STATUTE",))
build("bad-X14-user-supplied-no-evidence", report(), [src(domain="user_supplied", extra={"path": "materials/监管函.pdf"})],
      BASE_EVID, cov(), cmd(), 1, ("DD-EVIDENCE",), empty_evidence=True)

# ---------------------------------------------------------------- runner 控制样（不占 43 合同样数）
build("ctl-runner-expect-extra-code", report(rows=[row(D, "供应链风险", "据此可投，目标价应下调", "建议回避", "已披露", "—", "—")]),
      [src()], BASE_EVID, cov(), cmd(), 1, ("DD-TABLE",))
(ROOT / "ctl-runner-expect-extra-code" / "expect.txt").write_text(
    "exit=1\nneed=DD-TABLE\nmust-not=DD-REDLINE DD-ROW\nverdict=must-fail\nnote=故意含多缺陷：runner 须因未声明的额外码判 FAIL（M63-M2 负控）\n", encoding="utf-8")

# §v2-7 边界控制样：39/40 必过、41 必拦，CJK 与中英混排各测一次
B39_CJK, B40_CJK, B41_CJK = "甲" * 39, "甲" * 40, "甲" * 41
_PRE = "监管函AN202605100000000001号事项说明"     # 中英混排：ASCII 与 CJK 各计 1 码


def _mix(target):
    body = _PRE + "字" * max(0, target - len(_PRE))
    return body[:target]


B39_MIX, B40_MIX, B41_MIX = _mix(39), _mix(40), _mix(41)
assert (len(B39_CJK), len(B40_CJK), len(B41_CJK)) == (39, 40, 41)
assert (len(B39_MIX), len(B40_MIX), len(B41_MIX)) == (39, 40, 41)
build("ctl-boundary-40-pass", report(rows=(row(D, "合规与处罚", B39_CJK, "关注", "已披露", "—", ANCHOR),
                                           row("2026-05-11", "合规与处罚", B40_CJK, "关注", "已披露", "—", "AN202605110000000003"),
                                           row("2026-05-12", "合规与处罚", B39_MIX, "关注", "已披露", "—", "AN202605120000000004"),
                                           row("2026-05-13", "合规与处罚", B40_MIX, "关注", "已披露", "—", "AN202605130000000005"))),
      [src(), src("S2", ref="AN202605110000000003", asof="2026-05-11"), src("S3", ref="AN202605120000000004", asof="2026-05-12"),
       src("S4", ref="AN202605130000000005", asof="2026-05-13")],
      {**BASE_EVID,
       "regulatory_cn-S2.json": evid(date="2026-05-11", anchor="AN202605110000000003", fact=B40_CJK),
       "regulatory_cn-S3.json": evid(date="2026-05-12", anchor="AN202605120000000004", fact=B39_MIX),
       "regulatory_cn-S4.json": evid(date="2026-05-13", anchor="AN202605130000000005", fact=B40_MIX)},
      cov(cov_set({"合规与处罚": ("检到 4", "四条长度边界样")})), cmd(), 0, ())
build("ctl-boundary-41-fail", report(rows=(row(D, "合规与处罚", B41_CJK, "关注", "已披露", "—", ANCHOR),
                                           row("2026-05-11", "合规与处罚", B41_MIX, "关注", "已披露", "—", "AN202605110000000003"))),
      [src(), src("S2", ref="AN202605110000000003", asof="2026-05-11")],
      {**BASE_EVID, "regulatory_cn-S2.json": evid(date="2026-05-11", anchor="AN202605110000000003", fact=B41_MIX)},
      cov(cov_set({"合规与处罚": ("检到 2", "两条越界样")})), cmd(), 1, ("DD-TABLE",))




# ---------------------------------------------------------------- M72 反沉默漏报控制样（ctl，不占 43 题号）
UNDER_COV = cov([r if r[0] != "合规与处罚" else ("合规与处罚", "regulatory_cn", "regulatory_cn", "检到 0", "行被删、账被改零") for r in COV_ROWS])
build("ctl-underreport-drop-row", report(rows=()), [src()], BASE_EVID, UNDER_COV, cmd(), 1, ("DD-OMISSION",), flow={"合规与处罚": 1})
build("ctl-underreport-drop-source", report(rows=()), [], BASE_EVID, UNDER_COV, cmd(), 1, ("DD-OMISSION",), flow={"合规与处罚": 1})
build("ctl-underreport-with-reason", report(rows=()), [src()], BASE_EVID, UNDER_COV, cmd(), 0, (), flow={"合规与处罚": 1},
      progress="# 台账\n\n- 降级: 合规与处罚 | AN202605100000000001 | 归属不判：原文对象为同名非本主体，已移入待核\n")




# ---------------------------------------------------------------- M73（X15–X18 题面落地）
# X15 声明三形
build("bad-X15a-declaration-missing", report(no_decl=True), [src()], BASE_EVID, cov(), cmd(), 1, ("DD-INPUT",))
build("bad-X15b-declaration-late", report(decl_late=True), [src()], BASE_EVID, cov(), cmd(), 1, ("DD-INPUT",))
build("bad-X15c-declaration-bag",
      report(decl_split=["> AI 初稿，仅供内部讨论。", "> 本段不构成投资建议。"], no_decl=True),
      [src()], BASE_EVID, cov(), cmd(), 1, ("DD-INPUT",))

# X16 反沉默漏报三形（流水仍记 M，且流水带 seq/prev_sha256 链）
X16_EV = {"regulatory_cn-S1.json": BASE_EVID["regulatory_cn-S1.json"],
          "regulatory_cn-S2.json": evid(anchor="AN202605110000000002", date="2026-05-11", fact="交易所出具问询函，披露所载为收入确认事项")}
X16_SRC = [src(), src("S2", ref="AN202605110000000002", claim="北辰股份有限公司收到问询函，事项见公告原文", asof="2026-05-11")]
X16_COV = cov([r if r[0] != "合规与处罚" else ("合规与处罚", "regulatory_cn", "regulatory_cn", "检到 0", "行被删、账被改零") for r in COV_ROWS])
build("bad-X16a-zero-without-reason", report(rows=()), X16_SRC, X16_EV, X16_COV, cmd(), 1, ("DD-OMISSION",), flow={"合规与处罚": 2})
build("bad-X16b-delete-source-and-evidence", report(rows=()), [src("S2", ref="AN202605110000000002", claim="北辰股份有限公司收到问询函", asof="2026-05-11")],
      {"regulatory_cn-S2.json": X16_EV["regulatory_cn-S2.json"]}, X16_COV, cmd(), 1, ("DD-OMISSION",), flow={"合规与处罚": 2, "诉讼与仲裁": 0})
build("bad-X16c-vague-progress-claim", report(rows=()), X16_SRC, X16_EV, X16_COV, cmd(), 1, ("DD-OMISSION",), flow={"合规与处罚": 2},
      progress="# 台账\n\n合规与处罚本次均不适用，已降级。\n")
build("good-X16-downgrade-accounted", report(rows=(row(D, "合规与处罚", FACT, "关注", "已披露", "—", ANCHOR),)),
      X16_SRC, {**BASE_EVID, "regulatory_cn-S2.json": evid(anchor="AN202605110000000002", date="2026-05-11",
                                                           subjects=("海岳股份有限公司（600002.SH）",), fact="海岳股份收到问询函，与本主体无关")},
      cov([r if r[0] != "合规与处罚" else ("合规与处罚", "regulatory_cn", "regulatory_cn", "检到 1", ANCHOR) for r in COV_ROWS]),
      cmd(), 0, (), flow={"合规与处罚": 2},
      progress="# 台账\n\n- 降级: 合规与处罚 | AN202605110000000002 | 归属不判：原文对象为海岳股份有限公司（600002.SH），非本主体\n")

# X17 / X18：statute 同件不同法条、条件锚属他主体
X17_EV = {**BASE_EVID,
          "statute-S2.json": json.dumps({"domain": "statute", "category": "财务与披露质量", "note": "合成样例，非真实法条原文",
                                         "records": [{"法名": "《甲规则》", "条号": "第三条", "原文": "信息披露义务人应披露定期报告。"},
                                                     {"法名": "《乙规则》", "条号": "第七条", "原文": "信息披露义务人应当在报告期后30日内披露定期报告。"}]},
                                        ensure_ascii=False, indent=2) + "\n",
          "disclosure_cn-S3.json": evid(domain="disclosure_cn", date="2026-03-31", anchor=COND_ANCHOR, fact="一季报报告期截止日", category="财务与披露质量")}
X17_AN = "statute:《甲规则》第三条（报告期后30日）"
X17_ROWS = (row("2026-04-30", "财务与披露质量", "依甲规则第三条推得报告期后30日应披露日", "关注", "推导", "—", X17_AN), BASE_ROW)
X17_SRC = [src(), src("S2", domain="statute", ref=X17_AN, claim="甲规则第三条载明报告期后30日", asof="2026-04-30"),
           src("S3", domain="disclosure_cn", ref=COND_ANCHOR, claim="北辰股份有限公司 2026 年第一季度报告期截止 2026-03-31", asof="2026-03-31")]
X17_COV = cov(cov_set({"财务与披露质量": ("检到 1", X17_AN, "statute", "statute")}))
X17_REP = report(rows=X17_ROWS, domain_line="regulatory_cn、statute、disclosure_cn 3 域 / 无工具项: 0", cond_line=f"推导条件: {COND_ANCHOR}（报告期 2026-03-31 在场披露）")
build("bad-X17-statute-other-article", X17_REP, X17_SRC, X17_EV, X17_COV, cmd(), 1, ("DD-STATUTE",))

X18_EV = {**BASE_EVID,
          "statute-S2.json": json.dumps({"domain": "statute", "category": "财务与披露质量", "note": "合成样例，非真实法条原文",
                                         "records": [{"法名": LAW, "条号": "第三条", "原文": "信息披露义务人应当在报告期后30日内披露定期报告。"}]},
                                        ensure_ascii=False, indent=2) + "\n",
          "disclosure_cn-S3.json": json.dumps({"domain": "disclosure_cn", "category": "财务与披露质量", "asof": "2026-03-31",
                                               "records": [{"公告索引号": "AN202604010000000007", "出具日期": "2026-04-01",
                                                            "对象": [SUBJECT], "披露所载": "北辰股份有限公司董事会决议公告"},
                                                           {"公告索引号": COND_ANCHOR, "出具日期": "2026-03-31",
                                                            "对象": ["海岳股份有限公司（600002.SH）"], "披露所载": "海岳股份 2026 年第一季度报告期截止 2026-03-31"}]},
                                              ensure_ascii=False, indent=2) + "\n"}
X18_ROWS = (row("2026-04-30", "财务与披露质量", "依披露规则第三条推得报告期后30日应披露日", "关注", "推导", "—", STAT_AN), BASE_ROW)
X18_REP = report(rows=X18_ROWS, domain_line="regulatory_cn、statute、disclosure_cn 3 域 / 无工具项: 0",
                 cond_line=f"推导条件: {COND_ANCHOR}（报告期 2026-03-31 在场披露）")
build("bad-X18-condition-other-subject", X18_REP,
      [src(), src("S2", domain="statute", ref=STAT_AN, claim="合成示例披露规则第三条载明报告期后30日", asof="2026-04-30"),
       src("S3", domain="disclosure_cn", ref=COND_ANCHOR, claim="2026 年第一季度报告期截止 2026-03-31", asof="2026-03-31")],
      X18_EV, cov(cov_set({"财务与披露质量": ("检到 1", STAT_AN, "statute", "statute")})), cmd(), 1, ("DD-STATUTE",))

# ---- M91（§v2-11；题单 X19）：长窗的类目账龄可达面不得静默冒充标题窗 ----
X19_START = "2024-09-21"
X19_CMD = cmd(lookback="24m")
X21_PSEUDO = "类目账龄申报: requested=2024-09-21~2026-09-21 | disclosure_cn=730日 | beyond=已覆盖"
build("bad-X19-long-window-undeclared", report(title_start=X19_START, lookback="24m", no_age=True),
      [src()], BASE_EVID, cov(), X19_CMD, 1, ("DD-COVERAGE",))
build("good-X19-long-window-declared", report(title_start=X19_START, lookback="24m"),
      [src()], BASE_EVID, cov(), X19_CMD, 0, ())
build("bad-X20-beyond-laundered", report(title_start=X19_START, lookback="24m", age_beyond="零条"),
      [src()], BASE_EVID, cov(), X19_CMD, 1, ("DD-COVERAGE",))
build("bad-X21-double-declared-variant", report(title_start=X19_START, lookback="24m", age_extra=X21_PSEUDO),
      [src()], BASE_EVID, cov(), X19_CMD, 1, ("DD-COVERAGE",))
# 控制样（题单未给题号的同族等价攻击，不占主集）：beyond 的另一形「不存在」、申报窗≠复算窗
build("ctl-age-beyond-nonexistent", report(title_start=X19_START, lookback="24m", age_beyond="不存在"),
      [src()], BASE_EVID, cov(), X19_CMD, 1, ("DD-COVERAGE",))
build("ctl-age-requested-mismatch", report(title_start=X19_START, lookback="24m", age_start=START),
      [src()], BASE_EVID, cov(), X19_CMD, 1, ("DD-COVERAGE",))
# 单行形制不合法（只有伪行、无合法行）：走「唯一申报行不可解析」分支，防死码
build("ctl-age-single-malformed", report(title_start=X19_START, lookback="24m", age_cap="730日"),
      [src()], BASE_EVID, cov(), X19_CMD, 1, ("DD-COVERAGE",))

# ---- M95（§v2-12；题单 X22）：三空格 ATX 标题让节定位隐身、申报串到别节，禁止回退全文 ----
X22_TAIL = ("\n## 其他说明\n"
            + age_decl(X19_START, ASOF)
            + "\n\n   ## 覆盖率与未检到\n本节无账龄申报行（合法申报在上一节里）。\n")
build("bad-X22-section-lookup-bypass",
      report(title_start=X19_START, lookback="24m", no_age=True) + X22_TAIL,
      [src()], BASE_EVID, cov(), X19_CMD, 1, ("DD-COVERAGE",))

# ---- M97（§v2-13；题单 X23）：同名覆盖率节须恰为 1 个，≥2 直接判不可唯一（不做首节歧义解决）----
X23_AGE = age_decl(X19_START, ASOF)
build("bad-X23-duplicate-coverage-sections",
      report(title_start=X19_START, lookback="24m", no_age=True)
      + f"\n## 覆盖率与未检到\n{X23_AGE}\n\n## 覆盖率与未检到\n{X23_AGE}\n",
      [src()], BASE_EVID, cov(), X19_CMD, 1, ("DD-COVERAGE",))
build("good-X23-compact-h5-note",
      report(title_start=X19_START, lookback="24m")
      + "\n##### 附注\n本附注是节内级说明，不构成 H2-H4 分节（§v2-12 的 compact 合法形）。\n",
      [src()], BASE_EVID, cov(), X19_CMD, 0, ())
# 两枚控制样（审方 M96-A 判）：分节且申报在被识别节内（正路形，防新门恒红）；上限写高 730d（M94 欠的持久样）
build("ctl-age-sectioned-declared",
      report(title_start=X19_START, lookback="24m", no_age=True) + f"\n## 覆盖率与未检到\n{X23_AGE}\n",
      [src()], BASE_EVID, cov(), X19_CMD, 0, ())
build("ctl-age-cap-overclaim", report(title_start=X19_START, lookback="24m", age_cap="730d"),
      [src()], BASE_EVID, cov(), X19_CMD, 1, ("DD-COVERAGE",))

# ---- M99（§v2-14；题单 X24/X25）：一把识别器判级别——H1 永不作覆盖率节，H5/H6 不结束当前节 ----
X24_HEAD = "\n## 覆盖率与未检到\n"
build("bad-X24-h5-insection-duplicate",
      report(title_start=X19_START, lookback="24m", no_age=True)
      + f"{X24_HEAD}{X23_AGE}\n##### 补充说明\n{X23_AGE}\n",
      [src()], BASE_EVID, cov(), X19_CMD, 1, ("DD-COVERAGE",))
build("good-X24-sectioned-h5-before-declaration",
      report(title_start=X19_START, lookback="24m", no_age=True)
      + X24_HEAD + "##### 补充说明\n本节按类目逐条留账，说明不改变节的归属与范围。\n" + X23_AGE + "\n",
      [src()], BASE_EVID, cov(), X19_CMD, 0, ())
build("bad-X25-h1-title-masquerade",
      report(title_start=X19_START, lookback="24m", title_mid="（未检到项说明见后）")
      + "\n## 其他说明\n本件不设覆盖率说明节（申报行仍在标题后的紧凑正文里）。\n",
      [src()], BASE_EVID, cov(), X19_CMD, 1, ("DD-COVERAGE",))

# ---- M100（§v2-15；题单 X26–X32）：七条结构根因一单合治，一题一形 ----
GOOD_COV = cov()                      # 真实查过的九类账（流水与快照按它生成）
WASHED = ("诉讼与仲裁", "关联交易与资金占用", "业务资质与许可", "其他已披露重大事项")


def cov_wash(cats):
    """把若干 disclosure_cn 账行改写成「本次实际调用=—、结果=无工具」，流水与快照保持真实调用。"""
    return cov(cov_set({c: ("无工具", "域面外，需人工", "disclosure_cn", "—") for c in cats}))


# ①X26 账龄三段须核等值：写低 1d 与写高 730d 同罪（既有 ctl-age-cap-overclaim 只挡写高）
build("bad-X26-age-cap-underclaim", report(title_start=X19_START, lookback="24m", age_cap="1d"),
      [src()], BASE_EVID, cov(), X19_CMD, 1, ("DD-COVERAGE",))

# ②X27 九类账必须是一封闭集表：第十类行、以及"没先认表"的无表头形（同根控制）
build("bad-X27-ledger-tenth-category", report(title_start=X19_START, lookback="24m"),
      [src()], BASE_EVID, cov(COV_ROWS + [("虚构第十类", "—", "—", "无工具", "域面外，需人工")]), X19_CMD, 1, ("DD-COVERAGE",))
build("ctl-ledger-no-header", report(title_start=X19_START, lookback="24m"),
      [src()], BASE_EVID, "\n".join(GOOD_COV.split("\n")[2:]) + "\n", X19_CMD, 1, ("DD-COVERAGE",))

# ③X28 流水↔账↔三角闭合（主样 + 三枚同根控制，代码集按题面精确）
# flow_from=GOOD_COV：真实查过的九类照样进流水与快照，只有交付的账被改写——这才是"事后抹成无工具"的形状
build("bad-X28-called-washed-to-no-tool", report(title_start=X19_START, lookback="24m"),
      [src()], BASE_EVID, cov_wash(("诉讼与仲裁",)), X19_CMD, 1, ("DD-OMISSION",), flow_from=GOOD_COV)
build("ctl-flow-missing-hits", report(title_start=X19_START, lookback="24m"),
      [src()], BASE_EVID, GOOD_COV, X19_CMD, 1, ("DD-OMISSION",), flow_from=GOOD_COV, flow_drop_field=("hits", "合规与处罚"))
build("ctl-flow-domain-snapshot-mismatch", report(title_start=X19_START, lookback="24m"),
      [src()], BASE_EVID, GOOD_COV, X19_CMD, 1, ("DD-OMISSION",), flow_from=GOOD_COV, flow_set_domain="entity_data")
build("ctl-flow-age-trigger-launder", report(title_start=X19_START, lookback="24m", no_age=True),
      [src()], BASE_EVID, cov_wash(WASHED), X19_CMD, 1, ("DD-OMISSION", "DD-COVERAGE"), flow_from=GOOD_COV)

# ④X29 围栏内一切按示例文本：节定位、申报计数都不从围栏借；红线仍全篇扫
build("bad-X29-fenced-fake-section", report(title_start=X19_START, lookback="24m", no_age=True)
      + "\n```md\n## 覆盖率与未检到\n" + X23_AGE + "\n```\n\n## 其他说明\n本节与覆盖率账无关。\n",
      [src()], BASE_EVID, GOOD_COV, X19_CMD, 1, ("DD-COVERAGE",))
build("good-X29-fenced-heading-example", report(title_start=X19_START, lookback="24m", no_age=True)
      + X24_HEAD + X23_AGE + "\n\n```md\n## 覆盖率与未检到\n（示例标题，非交付节，也不含第二条申报）\n```\n",
      [src()], BASE_EVID, GOOD_COV, X19_CMD, 0, ())

# ⑤X30 输入权威单值：主体串不得抓首个；两行回显、两个 H1 各为一枚同根控制
DUAL = "北辰股份有限公司（600001.SH）；海岳股份有限公司（600002.SH）"
build("bad-X30-dual-subject-in-param", report(title_start=X19_START, lookback="24m", subject_line=DUAL),
      [src()], BASE_EVID, GOOD_COV, cmd(lookback="24m", subject=DUAL), 1, ("DD-INPUT",))
build("ctl-input-double-echo", report(title_start=X19_START, lookback="24m")
      .replace("- lookback: 24m", "- lookback: 12m\n- lookback: 24m", 1),
      [src()], BASE_EVID, GOOD_COV, X19_CMD, 1, ("DD-INPUT",))
build("ctl-input-double-h1", report(title_start=X19_START, lookback="24m")
      + f"\n# {SUBJECT}公开信息预尽调清单 · 窗口 2025-09-21~2026-09-21\n",
      [src()], BASE_EVID, GOOD_COV, X19_CMD, 1, ("DD-INPUT",))

# ⑥X31 足行按表节唯一：同节复制一行即竞争（合法紧凑一表一行不受影响）
build("bad-X31-duplicate-domain-line", report(title_start=X19_START, lookback="24m")
      .replace("本节检索域: regulatory_cn 1 域 / 无工具项: 0", "本节检索域: regulatory_cn 1 域 / 无工具项: 0\n本节检索域: regulatory_cn 1 域 / 无工具项: 0", 1),
      [src()], BASE_EVID, GOOD_COV, X19_CMD, 1, ("DD-COVERAGE",))

# ⑦X32 sources 的 asof 须是真实日历日（B17 管词法，本题管日历）
build("bad-X32-asof-not-a-calendar-day", report(title_start=X19_START, lookback="24m"),
      [src(asof="2026-02-30")], BASE_EVID, GOOD_COV, X19_CMD, 1, ("DD-EVIDENCE",))

# ---- M102（§v2-16；题单 M101 节十二枚控制）：X27/X28/X29 三格按审方闭包补全 ----
def sub_once(text, old, new, tag):
    assert text.count(old) >= 1, f"控制样改造锚点丢失：{tag}"
    return text.replace(old, new, 1)

GOOD_REP24 = report(title_start=X19_START, lookback="24m")
LEDGER24 = cov()

# ①X27 五列账固定文法（五枚，均只动账表一处，预期单码 DD-COVERAGE）
build("ctl-ledger-header-order", GOOD_REP24, [src()], BASE_EVID,
      sub_once(LEDGER24, LEDGER_HDR, "| 类目 | 本次实际调用 | 所需域/工具 | 结果 | 注记 |", "header-order"),
      X19_CMD, 1, ("DD-COVERAGE",), flow_from=LEDGER24)
build("ctl-ledger-header-width", GOOD_REP24, [src()], BASE_EVID,
      sub_once(LEDGER24, LEDGER_HDR, LEDGER_HDR + " 额外列 |", "header-width"),
      X19_CMD, 1, ("DD-COVERAGE",), flow_from=LEDGER24)
build("ctl-ledger-separator-width", GOOD_REP24, [src()], BASE_EVID,
      sub_once(LEDGER24, LEDGER_SEP, "|---|---|", "separator-width"),
      X19_CMD, 1, ("DD-COVERAGE",), flow_from=LEDGER24)
build("ctl-ledger-row-width", GOOD_REP24, [src()], BASE_EVID,
      sub_once(LEDGER24, LEDGER_ROW_EQ, LEDGER_ROW_EQ + " 隐形备注 |", "row-width"),
      X19_CMD, 1, ("DD-COVERAGE",), flow_from=LEDGER24)
build("ctl-ledger-second-header", GOOD_REP24, [src()], BASE_EVID,
      sub_once(LEDGER24, LEDGER_HDR, LEDGER_HDR + "\n" + LEDGER_SEP + "\n" + LEDGER_HDR, "second-header"),
      X19_CMD, 1, ("DD-COVERAGE",), flow_from=LEDGER24)

# ②X28 域相等（账内域 ≠ 该类流水域，两者都属合法枚举；足行同步改，避免借 §v2-2③ 代打）
LEDGER_DOMAIN_SWAP = sub_once(LEDGER24, "| 合规与处罚 | regulatory_cn | regulatory_cn |",
                              "| 合规与处罚 | regulatory_cn | entity_data |", "ledger-domain")
build("ctl-flow-ledger-domain-mismatch",
      sub_once(GOOD_REP24, "本节检索域: regulatory_cn 1 域", "本节检索域: entity_data 1 域", "footer-domain"),
      [src()], BASE_EVID, LEDGER_DOMAIN_SWAP, X19_CMD, 1, ("DD-OMISSION",), flow_from=LEDGER24)

# ③X29 围栏词法与掩码作用面（六枚；两枚是"现 1→应 0"的反向形状）
build("ctl-fence-longer-close-good",
      report(title_start=X19_START, lookback="24m", no_age=True)
      + "\n```md\n## 覆盖率与未检到\n（示例块：四反引号收尾才是合法闭栏）\n````\n"
      + X24_HEAD + X23_AGE + "\n",
      [src()], BASE_EVID, LEDGER24, X19_CMD, 0, ())
build("ctl-fence-four-space-not-open",
      report(title_start=X19_START, lookback="24m", no_age=True)
      + X24_HEAD + X23_AGE + "\n    ```md\n" + X23_AGE + "\n",
      [src()], BASE_EVID, LEDGER24, X19_CMD, 1, ("DD-COVERAGE",))
build("ctl-ledger-entirely-fenced", GOOD_REP24, [src()], BASE_EVID,
      "```md\n" + LEDGER24 + "```\n", X19_CMD, 1, ("DD-COVERAGE",), flow_from=LEDGER24)
build("ctl-fence-domain-footer-example-good",
      GOOD_REP24 + "\n```md\n本节检索域: bogus 1 域 / 无工具项: 0\n```\n",
      [src()], BASE_EVID, LEDGER24, X19_CMD, 0, ())
build("ctl-fence-authority-only",
      sub_once(report(title_start=X19_START, lookback="24m", no_decl=True),
               f"# {SUBJECT}公开信息预尽调清单 · 窗口 {X19_START}~{ASOF}",
               f"# {SUBJECT}公开信息预尽调清单 · 窗口 {X19_START}~{ASOF}\n\n```md\n{DECL}\n```",
               "authority-in-fence"),
      [src()], BASE_EVID, LEDGER24, X19_CMD, 1, ("DD-INPUT",))
build("ctl-fence-redline-still-scanned", GOOD_REP24 + "\n~~~\n可投\n~~~\n",
      [src()], BASE_EVID, LEDGER24, X19_CMD, 1, ("DD-REDLINE",))

# ---- M104-a（题单 :681/:682）：§v2-16② 多域集合的正反配对，唯一差别=账格写不写全两个域 ----
X28_FOOT = "regulatory_cn、disclosure_cn 2 域 / 无工具项: 0"
X28_REP = report(title_start=X19_START, lookback="24m", domain_line=X28_FOOT)
X28_COV_TWO = cov(cov_set({"合规与处罚": ("检到 1", ANCHOR, "regulatory_cn", "regulatory_cn、disclosure_cn")}))
X28_ZERO = json.dumps({"domain": "disclosure_cn", "category": "合规与处罚", "asof": ASOF,
                       "window": f"{X19_START}~{ASOF}", "query": f"{SUBJECT} 合规与处罚 {X19_START}~{ASOF}",
                       "records": [], "结果": "检到 0"}, ensure_ascii=False, indent=2) + "\n"
X28_EVID = {**BASE_EVID, "disclosure_cn-Z-合规与处罚.json": X28_ZERO}
X28_FLOW = ({"category": "合规与处罚", "domain": "disclosure_cn", "hits": 0,
             "snapshot": "disclosure_cn-Z-合规与处罚.json"},)
build("good-X28-two-domains-booked", X28_REP, [src()], X28_EVID, X28_COV_TWO, X19_CMD, 0, (),
      flow_from=GOOD_COV, flow_extra=X28_FLOW)
build("ctl-flow-two-domains-one-omitted", X28_REP, [src()], X28_EVID, GOOD_COV, X19_CMD, 1, ("DD-OMISSION",),
      flow_from=GOOD_COV, flow_extra=X28_FLOW)

# 反向计数控制样：账写「检到 1」而正文零行
build("ctl-overclaim-row-missing", report(rows=()), [src()], BASE_EVID,
      cov([r if r[0] != "合规与处罚" else ("合规与处罚", "regulatory_cn", "regulatory_cn", "检到 1", ANCHOR) for r in COV_ROWS]),
      cmd(), 1, ("DD-COVERAGE",), flow={"合规与处罚": 1})

# 参数解析已挪到第一枚 build() 之前（M250 零副作用），此处只留一句指路：见 `# 【M250】` 那段。

build("ctl-declaration-missing", report(no_decl=True), [src()], BASE_EVID, cov(), cmd(), 1, ("DD-INPUT",))

# ─────────────────────────────────────────────────────────────────────────────
# M217：共享语料上收（病灶是「同一套语料被抄了 N 份」，不是「哪几枚没人用」）
# 形制：被 ≥2 枚样**逐字节同**共用的文件留一份进 _shared/；每样只留 cmd.txt／expect.txt、
#   一份 shared.txt（该样要点名铺哪些公共件）、以及它**真正改动过**的那份（挪进 local/）。
# 两道防缩面：
#   ①证据目录必须为空的样（测「空证据即 fail-closed」那几道）**整体不参与上收**；
#   ②**按样清单铺设**（不是把 _shared 整个并进去）——上一版把公共池当并集铺，
#     给每样注入了它原本没有的原始件，check_dd 立刻报「未登记在 LEDGER」＝覆盖面被改变。
# ctl- 32 枚一枚不删：负控自证就是「自测不恒真」的证据。cmd.txt 走 bash -c（见 run_fixtures.sh）。
KEEP_LOCAL = ("cmd.txt", "expect.txt")


def _sample_dirs():
    return [d for d in sorted(ROOT.iterdir()) if d.is_dir()
            and d.name.startswith(("good-", "bad-", "ctl-"))]


def _files(d: pathlib.Path):
    return {f.relative_to(d).as_posix(): f for f in sorted(d.rglob("*")) if f.is_file()}


def _empty_evidence(fs) -> bool:
    ev = [p for p in fs if p.startswith("evidence/")]
    return bool(ev) and all(p == "evidence/.gitkeep" for p in ev)


REJECTED_EXT = (".sha256",)     # K-23 实测拒收族（第四拒原文点名 `_shared/variants/evidence__LEDGER__….sha256`）


def _shared_name(rel: str) -> str:
    """公共位**落盘名**：末段后缀属实测拒收族时，在后面并一层允许后缀（`LEDGER.sha256` →
       `LEDGER.sha256.txt`），内容与目的地名都不变——runner 按 `shared.txt` 的目的地铺回临时目录，
       `check_dd` 看到的仍是 `evidence/LEDGER.sha256`，换的只是仓内那枚文件的后缀。"""
    base = rel.rsplit("/", 1)[-1]
    stem, dot, ext = base.rpartition(".")
    return rel + ".txt" if dot and ("." + ext).lower() in REJECTED_EXT else rel


def _variant_name(rel: str, h: str) -> str:
    """变体落成**扁平名且保留原扩展名**：`variants/report__<sha16>.md`。
       旧形制是 `variants/<rel>/<sha16>`——末段无扩展名，落在渠道扩展名白名单的问号区（K-22 刚咬过
       压缩包，不拿「大概没事」赌第四次 400）；顺带少五枚目录条目。"""
    base, ext = rel.rsplit(".", 1) if "." in rel.rsplit("/", 1)[-1] else (rel, "")
    stem = base.replace("/", "__")
    return _shared_name(f"{stem}__{h[:16]}{('.' + ext) if ext else ''}")


def harvest_shared():
    import hashlib
    def sha(b):
        return hashlib.sha256(b).hexdigest()

    samples = _sample_dirs()
    # 公共位先清再写：形制换过一次（嵌套变体目录→扁平带扩展名），留着旧文件就成了「第二副面孔」，
    # 而且渠道按条目数计——陈旧件不是难看，是占额度（本次实测多出 18 份无扩展名残件）。
    if (ROOT / "_shared").is_dir():
        shutil.rmtree(ROOT / "_shared")
    users, size, staged, originals, ev_locked = {}, {}, [], {}, set()
    for s in samples:
        fs = _files(s)
        originals[s.name] = {rel: sha(f.read_bytes()) for rel, f in fs.items()}
        if _empty_evidence(fs):
            ev_locked.add(s.name)          # 空证据样：证据目录整体不上收（否则公共件被注进去＝缩面）
        staged.append(s)
        for rel, f in fs.items():
            if rel in KEEP_LOCAL or (s.name in ev_locked and rel.startswith("evidence/")):
                continue
            h = sha(f.read_bytes())
            users.setdefault(rel, {}).setdefault(h, []).append(s.name)
            size[h] = len(f.read_bytes())
    modal, variants = {}, {}
    for rel, byhash in users.items():
        if sum(len(v) for v in byhash.values()) < 2:
            continue
        ordered = sorted(byhash.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        modal[rel] = ordered[0]
        for h, owners in ordered[1:]:
            if len(owners) < 2:
                continue
            variants[(rel, h)] = owners[0]
    for rel, (h, owners) in sorted(modal.items()):
        dst = ROOT / "_shared" / _shared_name(rel)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((ROOT / owners[0] / rel).read_bytes())
    for (rel, h), owner in sorted(variants.items()):
        dst = ROOT / "_shared" / "variants" / _variant_name(rel, h)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((ROOT / owner / rel).read_bytes())
    hoisted = diffs = 0
    for s in staged:
        want, keep = [], []
        for rel, f in sorted(_files(s).items(), key=lambda kv: -len(kv[0])):
            if rel in KEEP_LOCAL or rel == "shared.txt" or rel.startswith("local/"):
                continue
            if s.name in ev_locked and rel.startswith("evidence/"):
                continue
            h = sha(f.read_bytes())
            if rel in modal and h == modal[rel][0]:
                f.unlink()
                src = _shared_name(rel)
                want.append(rel if src == rel else f"{rel}\t{src}")
                hoisted += 1
            elif (rel, h) in variants:
                f.unlink()
                want.append(f"{rel}\tvariants/{_variant_name(rel, h)}")
                hoisted += 1
            elif rel in modal:
                dst = s / "local" / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(f.read_bytes())
                f.unlink()
                keep.append(rel)
                diffs += 1
        (s / "shared.txt").write_text("".join(r + "\n" for r in sorted(want)), encoding="utf-8")
    for s in staged:
        cp = s / "cmd.txt"
        if not cp.is_file():
            continue
        m = re.match(r"^(python3?)\s+(\S+)\s+(.*)$", cp.read_text(encoding="utf-8").strip())
        if not m:
            continue
        interp, script, args = m.groups()
        TAB = chr(9)
        new = ('T="$(mktemp -d)"; while IFS="' + TAB + '" read -r d s; do src="${s:-$d}"; '
               'mkdir -p "$T/$(dirname "$d")"; cp "../_shared/$src" "$T/$d"; done < shared.txt; '
               'cp -R . "$T"/ 2>/dev/null; [ -d local ] && cp -R local/. "$T"/ 2>/dev/null; '
f'cd "$T" && {interp} "$OLDPWD/{script}" {args}; rc=$?; exit $rc')
        cp.write_text(new + "\n", encoding="utf-8")
    print(f"上收：_shared 装模态 {len(modal)} 类＋变体 {len(variants)} 份"
          f"（公共版 {sum(size[h] for h, _ in modal.values()) + sum(size[h] for (_, h) in variants):,} B）；"
          f"样内删公共副本 {hoisted} 份、挪差异位 {diffs} 份；参与 {len(staged)} 样、"
          f"证据目录整体不上收（空证据样）{len(ev_locked)} 样")
    return originals


ORIGINALS = harvest_shared()


def verify_materialization(originals):
    """等价自证（①的防缩面）：按 shared.txt＋样内原位件＋local/ 覆盖，在 python 里复算一遍
       「bash 铺出来会给 check_dd 看到什么」，与**上收前逐枚同文件同 sha** 才算过。
       不过就 sys.exit(2)——覆盖面被悄悄改动，比体积不过闸更严重。"""
    import hashlib
    def sha(b):
        return hashlib.sha256(b).hexdigest()
    bad = []
    for s in _sample_dirs():
        if not (s / "shared.txt").is_file():
            eff = {rel: sha(f.read_bytes()) for rel, f in _files(s).items() if rel not in ("shared.txt",)}
            base = dict(originals.get(s.name, {}))
            if {k: v for k, v in base.items() if k not in KEEP_LOCAL} != {k: v for k, v in eff.items() if k not in KEEP_LOCAL}:
                bad.append((s.name, "未参与上收但文件集变了"))
            continue
        want = [l.rstrip("\n") for l in (s / "shared.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
        eff = {}
        for line in want:
            parts = line.split("\t")
            rel, src = parts[0], (parts[1] if len(parts) > 1 else parts[0])
            eff[rel] = sha((ROOT / "_shared" / src).read_bytes())
        for rel, f in _files(s).items():
            if rel in KEEP_LOCAL or rel == "shared.txt" or rel.startswith("local/"):
                continue   # 样内原位件（含证据目录里的本地件）由 cp -R . 铺回，必须计入等价面
            eff[rel] = sha(f.read_bytes())
        for rel, f in _files(s).items():
            if rel.startswith("local/"):
                eff[rel[len("local/"):]] = sha(f.read_bytes())
        base = {k: v for k, v in originals.get(s.name, {}).items() if k not in KEEP_LOCAL}
        if base != eff:
            miss = sorted(set(base) - set(eff))
            extra = sorted(set(eff) - set(base))
            diff = sorted(k for k in set(base) & set(eff) if base[k] != eff[k])
            bad.append((s.name, f"缺 {miss[:3]} 多 {extra[:3]} 变 {diff[:3]}"))
    if bad:
        for n, why in bad[:8]:
            print(f"等价自证失败：{n} — {why}", file=sys.stderr)
        sys.exit(2)
    print(f"等价自证通过：{len(originals)} 样铺回后与上收前逐枚同文件同 sha（覆盖面零变化）。")


verify_materialization(ORIGINALS)

names = sorted(x.name for x in ROOT.iterdir() if x.is_dir())
bad = [n for n in names if n.startswith("bad-")]
good = [n for n in names if n.startswith("good-")]
ctl = [n for n in names if n.startswith("ctl-")]

print(f"fixtures 重铺完成：{len(bad)} bad + {len(good)} good + {len(ctl)} ctl = {len(names)} 目录")
want = matrix_ids(_badspec)
have = {"DD-" + re.match(r"^bad-([BX]\d{1,2}[a-c]?)-", n).group(1) for n in bad}
if want != have:
    print(f"题号↔样号双向断言失败：缺题 {sorted(want - have)}；多样 {sorted(have - want)}", file=sys.stderr)
    sys.exit(2)
print(f"题单 {len(want)} 题 ↔ 主集样 {len(have)} 个（bad 族），双向断言通过。")

# 控制样：题单只以行内代码点名它出过题的控制；盘上另有历史控制不写进题单（不做缺席背书也不做全覆盖宣称）。
cw = matrix_ctl_names(_badspec)
ch = set(ctl)
if cw - ch:
    print(f"题单控制名↔盘上控制样断言失败：题单点名而盘上缺席 {sorted(cw - ch)}", file=sys.stderr)
    sys.exit(2)
print(f"控制样：题单点名 {len(cw)} 枚全数在盘；盘上控制共 {len(ch)} 枚"
      f"（其中 {len(ch - cw)} 枚为历史控制、题单未点名，只随 runner 复跑）。")
print("提醒：判卷与复现以 run_fixtures.sh 为准；本脚本幂等，跑完应无差异（见文件头派生纪律）。")# ─────────────────────────────────────────────────────────────────────────────
# M225（收口形制）：并样内文件——渠道对**包内条目数（≤200，目录条目照计）**与**扩展名白名单**
#   各有一道硬限：散件态 1,000 条目被 400 拒（K-20），改封 `corpus.tar.gz` 后又被 400
#   「不允许的文件类型」拒（压缩包与 *.png 同族，K-22）。故语料**不封二进制档**：
#   每枚样的 cmd/expect/差异件并进一枚 `samples/<名>.json`（ASCII-only 文本容器），
#   共享语料留在 `_shared/` 以 .json/.md 散放（40 份）。题数、码集、负控一枚不减。
#   铺法只有一处实现——runner 与本自证都调 `unpack.materialize()`，容器与散件两副面孔不许多分家。
#   档案必须保「空目录」这条事实照旧成立：`dirs` 逐枚记，202 枚空目录是 fail-closed 题的形制。


def emit_samples(sample_names):
    sys.path.insert(0, str(ROOT))
    import unpack                                    # 与 runner 同一枚铺法，不另写一遍
    sdir = ROOT / "samples"
    if sdir.is_dir():
        shutil.rmtree(sdir)
    sdir.mkdir(parents=True)
    for stale in ("corpus.tar.gz", "corpus.manifest.txt"):
        f = ROOT / stale
        if f.is_file():
            f.unlink()                              # 换形制：旧档案不留在包里当「第二副面孔」

    snap = {}                                       # 铺回对平的参照＝删除前的散件原样
    for n in sample_names:
        s = ROOT / n
        fs = {f.relative_to(s).as_posix(): f for f in sorted(s.rglob("*")) if f.is_file()}
        empty_dirs = sorted(d.relative_to(s).as_posix() for d in sorted(s.rglob("*"))
                            if d.is_dir() and not any(f.startswith(d.relative_to(s).as_posix() + "/") for f in fs))
        obj = {"name": n}
        for key, field in unpack.FIELDS:
            src = s / key
            if src.is_file():
                obj[field] = src.read_text(encoding="utf-8")
        files = {}
        for rel, f in fs.items():
            if rel in ("cmd.txt", "expect.txt", "shared.txt"):
                continue
            try:
                files[rel] = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                print(f"容器是纯文本形制，装不下非 UTF-8 件：{n}/{rel}——改判卷面或改容器，不自加 base64", file=sys.stderr)
                sys.exit(2)
        obj["files"] = files
        obj["dirs"] = empty_dirs
        (sdir / f"{n}.json").write_text(json.dumps(obj, ensure_ascii=True, sort_keys=True,
                                                  separators=(",", ":")) + "\n", encoding="utf-8")
        snap[n] = ({rel: hashlib.sha256(f.read_bytes()).hexdigest() for rel, f in fs.items()},
                   set(empty_dirs))

    # 复算自证（fail-closed）：容器铺回 == 删除前散件，逐枚同文件同 sha、同空目录集
    work = pathlib.Path(tempfile.mkdtemp(prefix="dd-emit-"))
    bad = []
    for sp in sorted(sdir.glob("*.json")):
        d = unpack.materialize(sp, work)
        got = {f.relative_to(d).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(d.rglob("*")) if f.is_file()}
        gdirs = sorted(x.relative_to(d).as_posix() for x in sorted(d.rglob("*"))
                       if x.is_dir() and not any(f.startswith(x.relative_to(d).as_posix() + "/") for f in got))
        want_files, want_dirs = snap[d.name]
        if got != want_files or set(gdirs) != want_dirs:
            bad.append((d.name, sorted(set(want_files) ^ set(got))[:3], sorted(want_dirs ^ set(gdirs))[:3]))
    if bad:
        shutil.rmtree(work, ignore_errors=True)
        for n, df, dd in bad[:8]:
            print(f"容器复算失败：{n} 文件差 {df} 空目录差 {dd}——散件未删，不交付", file=sys.stderr)
        sys.exit(2)

    total_files = sum(len(v[0]) for v in snap.values())
    loose_bytes = sum(f.stat().st_size for n in sample_names for f in (ROOT / n).rglob("*") if f.is_file())
    n_containers = len(list(sdir.glob("*.json")))
    n_shared = len([f for f in (ROOT / "_shared").rglob("*") if f.is_file()])
    man = ["# 样容器清单（gen_fixtures.py 产出；铺法唯一实现＝scripts/fixtures/unpack.py::materialize）",
           f"# 样 {len(sample_names)} 枚＝容器 {n_containers} 份；铺回后文件 {total_files} 份／散件态 {loose_bytes:,} B；"
           f"共享语料留散件于 _shared/（{n_shared} 份）",
           "样目录名\t铺回件数\t铺回字节\tcmd.txt sha8"]
    for n in sample_names:
        d = work / n
        fs = [f for f in sorted(d.rglob("*")) if f.is_file()]
        c8 = hashlib.sha256((d / "cmd.txt").read_bytes()).hexdigest()[:8] if (d / "cmd.txt").is_file() else "-"
        man.append(f"{n}\t{len(fs)}\t{sum(f.stat().st_size for f in fs)}\t{c8}")
    (ROOT / "samples.manifest.txt").write_text("\n".join(man) + "\n", encoding="utf-8")
    cb = sum(f.stat().st_size for f in sdir.glob("*.json"))
    for n in sample_names:
        shutil.rmtree(ROOT / n)
    print(f"并样：容器 {n_containers} 份／{cb:,} B（散件态 {len(sample_names)} 目录／{loose_bytes:,} B，样内件已并、散件已删）；"
          f"共享留散件 {len([f for f in (ROOT / '_shared').rglob('*') if f.is_file()])} 份；"
          f"铺回复算逐枚同文件同 sha、同空目录集通过（{total_files} 份）；清单落 samples.manifest.txt。")
    shutil.rmtree(work, ignore_errors=True)


sample_names = sorted(x.name for x in ROOT.iterdir() if x.is_dir() and not x.name.startswith(("_", "samples")))
if _args.keep_loose:
    print(f"--keep-loose：散件态保留（审计形，不交付）——样目录 {len(sample_names)} 枚在盘，未并容器。")
else:
    emit_samples(sample_names)
