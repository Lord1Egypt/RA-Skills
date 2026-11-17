#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_page.py —— tear-sheet 公司一页纸机检(spec-tear-sheet-0.1.0 §4 四道 + badspec 验收协议)。

纯 stdlib、零网络、零崩溃(任何输入异常→FAIL 清单+exit 1)。
CLI: check_page.py <page.md> --sources sources.jsonl --subjects <n>
     题单纪律:badspec 各题带 --sources;不传 sources 时 ②道仅做列级锚形制检查,双向账跳过。
     --sources/--subjects 按 SKILL §4 正式命令式在场;缺 --subjects=[参数] FAIL(M43 双向对齐:
     阈值不随申报走——spec §4「主体数 >5 FAIL」为硬闸,--subjects 只作申报↔机检对账项)。

四道(spec §4 道号定义,诊断行以 [①][②][③][④] 前缀标注道号):
  ①身份/声明:页头区(文首至首个主体块前)须含 本页为AI初稿 / asof:日期 / 数据截止日:日期 /
    通道用量声明(research…次|omni…次)——逐字段点名缺失。
  ②数字行:速览表按内容识别(期间列 \\d{4}(H1|Q\\d|A) 或 basis 列);每条数字行须合式来源锚
    ([S<n]> 或 AN/URL/conv/函件号;纯数字不是锚);basis ∈ {cumulative,qtr};
    正文↔sources 双向:[S<n] 引用须有 sources 行、sources 行须被正文 [S<n] 引用(附录散文不算)。
  ③禁词:整份交付物全文扫(书名号/引用位/围栏不豁免)+ sources claim/ref:
    BANNED 全集+利好|利空|买入|增持|目标价|建议;评级概念本页不适用=零容忍无豁免。
  ④形制:主体块=非保留词的 H2 节(标题含「主体」与否无关),≤5;块内子段按内容语义分类
    (身份/速览/事件/风险/观点),五段顺序=身份→速览→事件→风险→观点,风险先于事件即乱序;
    每主体非空物理行 ≤40;事件行(含围栏内)>4 FAIL;事件第一闸:日期列须全格式 YYYY-MM-DD
    且事件文字不含估算/自白词、法定类锚须 statute:《法名》第N条（要点）形制+sources kind=statute
    同串(只验形状与承载,编造法名可复核性声明义务=statute 行 ref 须为可访问 URL 或 AN 承载原文);
    观点段(占位行特征识别,任意节名)有非 [待人工] 内容即 FAIL;风险段无命中行时须逐字含
    「直查面内未命中≠无敞口」。
"""

import argparse
import json
import re
import sys
from pathlib import Path

PERIOD_RE = re.compile(r"^\d{4}(H1|H2|Q[1-4]|A|AR)$")
BASIS_ENUM = {"cumulative", "qtr"}
SREF_RE = re.compile(r"\[S(\d+)\]")
FULL_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ESTIMATE_RE = re.compile(r"估算|大约|约于|或将|预计|惯例|通常|非承诺|中旬|下旬|月初|月底")
STATUTE_SPEC_RE = re.compile(r"^statute[:：]《[^《》]+》第[0-9一二三四五六七八九十百零]+条（[^（）]{2,}）$")
BANNED_RE = re.compile(
    r"必涨|稳赚|零风险|保证收益|内幕|无风险套利|历史最佳|利好|利空|暴涨|会涨|抄底|逃顶"
    r"|买入|增持|减持|持有|推荐|目标价|建议")
RISK_FIXED = "直查面内未命中≠无敞口"
HEDGE_USAGE_RE = re.compile(r"(research|Research|深研)\s*\d*\s*次.{0,4}(omni|Omni|解析)?[^。\n]*")

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
    ("E-BANWORD", r"\[③\]|禁词|评级|目标价|买入|推荐"),
    ("E-COVERAGE", r"\[④\][^\n]*(申报|对账|覆盖|未登记|漏报)"),
    ("E-ANCHOR", r"\[②\]|\[④\][^\n]*(锚|双向|sources|statute)|\[来源\]"),
    ("E-FORMAT", r"\[①\]|\[参数\]|^\[④\]"),
)


def ecode(msg: str) -> str:
    for code, pat in E_RULES:
        if re.search(pat, msg):
            return code
    return "E-FORMAT"
RESERVED_H2 = ("附录", "来源索引")
NUM_CELL_RE = re.compile(r"^-?[\d,]+(?:\.\d+)?$")
ANCHOR_OK_RE = re.compile(r"^(\[S\d+\]|AN\d{8,}|(?<!\d)\d{6,}|https?://\S+|conv_id=\S+.*|\S*〔\d{4}〕\d+号|statute[:：].+)$", re.I)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def scan_body(page_lines, src_recs, declared=None):
    fails = []
    text = "\n".join(page_lines)

    # —— 道①:页头声明四字段(至首个 H2 前) ——
    head_end = next((i for i, l in enumerate(page_lines) if l.startswith("## ")), len(page_lines))
    head = "\n".join(page_lines[:head_end])
    for pat, name in ((r"本页为 ?AI ?初稿", "本页为 AI 初稿"),
                      (r"asof[:：]\s*\d{4}-\d{2}-\d{2}", "asof 日期"),
                      (r"数据截止日[:：]\s*\d{4}-\d{2}-\d{2}", "数据截止日"),
                      (r"(通道用量|channel usage).{0,24}(次|times)", "通道用量声明")):
        if not re.search(pat, head, re.I):
            fails.append(f"[①] 页头缺声明字段「{name}」")

    # —— 结构:H2 主体块 + 子段语义分类 ——
    blocks = []  # (title, start, end)
    marks = [i for i, l in enumerate(page_lines) if l.startswith("## ")]
    for j, s in enumerate(marks):
        e = marks[j + 1] if j + 1 < len(marks) else len(page_lines)
        title = page_lines[s][3:].strip()
        if not any(title.startswith(r) for r in RESERVED_H2):
            blocks.append((title, s, e))
    if len(blocks) > 5:
        fails.append(f"[④] 主体数 {len(blocks)} > 5")
    if declared is None:
        fails.append("[参数] 缺 --subjects(声明主体数;SKILL §4 正式命令式,M43 双向对齐)")
    elif declared != len(blocks):
        fails.append(f"[④] --subjects 声明 {declared} ≠ 机检主体数 {len(blocks)}(少报多搭/顶替申报)")

    order_names = ["identity", "facts", "events", "risk", "view"]
    for bi, (bt, bs, be) in enumerate(blocks):
        blines = page_lines[bs:be]
        span = page_lines if len(blocks) == 1 else blines   # 计数约定:单主体页=整页非空行(badspec B08),多主体=逐块
        body_nl = [l for l in span if l.strip()]
        if len(body_nl) > 40:
            fails.append(f"[④] 主体块/主体页 {len(body_nl)} 行 > 40")
        sub_idx = [i for i, l in enumerate(blines) if l.startswith("### ")] + [len(blines)]
        segs = []
        for k in range(len(sub_idx) - 1):
            seg = blines[sub_idx[k]:sub_idx[k + 1]]
            if not seg:
                continue
            seg_text = "\n".join(seg)
            rows = [cells(l) for l in seg if l.strip().startswith("|")]
            data_rows = [r for r in rows if r and (
                PERIOD_RE.match(r[0]) or (len(r) > 1 and r[1] in BASIS_ENUM))]
            ev_rows = [r for r in rows if r and FULL_DATE_RE.match(r[0])]
            if any(l.startswith("- 全称") or "代码" in seg for l in seg) and not rows and "身份" in seg[0]:
                kind = "identity"
            elif any(l.startswith("- 全称") for l in seg) and not rows:
                kind = "identity"
            elif data_rows:
                kind = "facts"
            elif ev_rows:
                kind = "events"
            elif sum(l.strip().startswith("- [待人工]") for l in seg) >= 2 and not rows:
                kind = "view"
            elif "风险" in seg[0] or "风险" in seg_text or RISK_FIXED in seg_text:
                kind = "risk"
            else:
                kind = None
            if kind:
                segs.append((kind, seg))
        seen_order = [s[0] for s in segs]
        for need in order_names:
            if need not in seen_order and bi == 0 and need in ("identity", "facts", "view"):
                pass
        pos = {n: seen_order.index(n) for n in order_names if n in seen_order}
        if "risk" in pos and "events" in pos and pos["risk"] < pos["events"]:
            fails.append(f"[④] 主体块「{bt[:16]}」风险段出现在事件段之前(五段顺序破坏)")

        # 事件第一闸 + 计数(含围栏内行)
        ev_all = [cells(l) for l in blines if l.strip().startswith("|")
                  and l.strip().split("|")[1].strip() and FULL_DATE_RE.match(l.strip().split("|")[1].strip())]
        if len(ev_all) > 4:
            fails.append(f"[④] 在场事件 {len(ev_all)} > 4(含围栏内)")
        for r in ev_all:
            d, ev = r[0], r[1] if len(r) > 1 else ""
            typ = r[2] if len(r) > 2 else ""
            anchor = r[3] if len(r) > 3 else ""
            if ESTIMATE_RE.search(ev + anchor):
                fails.append(f"[④] 事件「{ev[:24]}」日期为估算/非披露明确日期(第一闸)")
            if typ == "法定":  # 承载两形制:字面 statute 串,或 [S<n]> 引用且对应 sources 行为 kind=statute
                ms = re.fullmatch(r"\[S(\d+)\]", anchor)
                def statute_ref_ok(ref):
                    ref = str(ref).strip()
                    core = re.sub(r"^statute[:：]", "", ref)
                    spec = bool(re.match(r"^《[^《》]+》第[0-9一二三四五六七八九十百零]+条（[^（）]{2,}）", core))
                    verifiable = bool(re.search(r"https?://|gov\.cn|AN\d{8,}", ref))
                    return spec and verifiable
                if ms:
                    hit = any(str(rec.get("id")) == "S" + ms.group(1) and rec.get("kind") == "statute"
                              and statute_ref_ok(rec.get("ref", "")) for _, rec in src_recs)
                else:
                    hit = bool(STATUTE_SPEC_RE.match(anchor)) and statute_ref_ok(anchor)
                if not hit:
                    fails.append(f"[④] 法定锚不可核/适用条件不可判:{anchor[:36]}(statute 形制+可复核承载)")

        # 速览表数字行(跨段收集,含无表头形态)
        for l in blines:
            s = l.strip()
            if not s.startswith("|"):
                continue
            cs = cells(l)
            if not cs or not PERIOD_RE.match(cs[0]):
                continue
            anchor_v = cs[-1]
            if not ANCHOR_OK_RE.match(anchor_v):
                fails.append(f"[②] {cs[0]} 行来源锚为空/不在白名单:{anchor_v[:16]!r}")
            basis_v = cs[1] if len(cs) > 1 else ""
            if basis_v not in BASIS_ENUM:
                fails.append(f"[②] {cs[0]} 行 basis 缺失/不在枚举:{basis_v!r}")

        # 观点占位硬账(spec §2.5:每主体 3 行 [待人工] 恒在场,代填=占位不足 3 或段内混入他行)
        ph = sum(1 for l in blines if re.match(r"^-\s*\[待人工\]", l.strip()))
        if ph < 3:
            fails.append(f"[④] 主体块「{bt[:16]}」观点区存在非 `[待人工]` 内容(占位 {ph}/3,缺位即代填)")
        for kind, seg in segs:
            if kind == "view":
                others = [l for l in seg[1:] if l.strip() and not re.match(r"^-\s*\[待人工\]", l.strip())]
                if others:
                    fails.append(f"[④] 观点区存在非 `[待人工]` 内容:{others[0].strip()[:30]}")
        # 风险段固定句:该块无风险命中行而有风险段 → 逐字检查
        for kind, seg in segs:
            if kind == "risk":
                has_hit = any(re.search(r"\[S\d+\]|命中", l) and RISK_FIXED not in l for l in seg)
                if not has_hit and RISK_FIXED not in "\n".join(seg):
                    fails.append(f"[④] 风险无命中固定句缺失(须逐字含「{RISK_FIXED}」)")

    # —— 道③:全文禁词(含围栏/书名号)+ sources claim/ref ——
    for i, l in enumerate(page_lines):
        m = BANNED_RE.search(l)
        if m:
            fails.append(f"[③] 第 {i + 1} 行命中禁词「{m.group(0)}」")
    for ln, rec in src_recs:
        for f in ("claim", "ref"):
            v = str(rec.get(f, ""))
            m = BANNED_RE.search(v)
            if m:
                fails.append(f"[③] sources 第 {ln} 行 {f} 命中禁词「{m.group(0)}」")

    # —— 道②双向:正文 [S<n] ↔ sources id ——
    if src_recs:
        body_ids = {int(x) for x in SREF_RE.findall(text)}
        src_ids = {int(m.group(1)) for _, rec in src_recs if re.fullmatch(r"S\d+", str(rec.get("id", ""))) for m in [re.match(r"S(\d+)", str(rec["id"]))]}
        orphan_body = sorted(body_ids - src_ids)
        if orphan_body:
            fails.append("[②] 正文孤儿锚:" + ",".join(f"S{i}" for i in orphan_body) + " 在 sources 不存在")
        refs_ids = set()
        for _, rec in src_recs:
            m = re.fullmatch(r"S(\d+)", str(rec.get("id", "")))
            if m:
                refs_ids.add(int(m.group(1)))
        orphan_src = []
        for rid, rec_id in sorted((int(m.group(1)), str(rec.get("id"))) for _, rec in src_recs
                                   if (m := re.fullmatch(r"S(\d+)", str(rec.get("id", ""))))):
            if rid in body_ids:
                continue
            # 例外:sources 的锚串本身出现在正文表格锚列(法定字面承载形)也算引用
            ref = str(rec.get("ref", "")).strip()
            in_table_anchor = any(ref == c.strip() for l in page_lines if l.strip().startswith("|")
                                  for c in l.strip().strip("|").split("|"))
            if not in_table_anchor:
                orphan_src.append(rec_id)
        if orphan_src:
            fails.append("[②] sources 孤儿记录未被正文引用(附录散文不算):" + ",".join(orphan_src))
    return fails


def _view_only(seg):
    body = [l for l in seg[1:] if l.strip()]
    return bool(body) and all(re.match(r"^-\s*\[待人工\]", l.strip()) for l in body)


def main(argv=None):
    p = argparse.ArgumentParser(description="tear-sheet 四道机检(spec §4)。")
    p.add_argument("page", help="page.md")
    p.add_argument("--sources", default=None, help="sources.jsonl(题单必传;不传则双向账跳过)")
    p.add_argument("--subjects", type=int, default=None,
                   help="申报主体数(SKILL §4 正式命令式;与机检数不符=FAIL,阈值 >5 不随申报走)")
    args = p.parse_args(argv)
    try:
        lines = Path(args.page).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as e:
        print(f"FAIL: 无法读取 {args.page}: {e}")
        return 1
    recs = []
    if args.sources:
        try:
            raw = Path(args.sources).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            print(f"FAIL: [②] 无法读取 sources:{e}")
            return 1
        for ln, line in enumerate(raw.splitlines(), 1):
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
                if isinstance(rec, dict):
                    recs.append((ln, rec))
            except json.JSONDecodeError:
                recs.append((ln, {}))
    fails = scan_body(lines, recs, args.subjects)
    if fails:
        print(f"FAIL: {args.page}（{len(fails)} 条）")
        codes = []
        for f in fails:
            c = ecode(f)
            if c not in codes:
                codes.append(c)
            print(f"  - [{c}] {f}")
        print("  码表: " + "; ".join(f"{c}→{E_LEGEND[c]}" for c in codes))
        return 1
    print(f"PASS: {args.page}（四道全过,主体块扫描正常）")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:
        print(f"FAIL: 内部异常兜底(报 bug):{type(e).__name__}: {e}")
        sys.exit(1)
