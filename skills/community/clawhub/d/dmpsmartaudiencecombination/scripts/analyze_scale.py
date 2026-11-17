#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""analyze_scale.py - 扩缩量分析报告（Step 11）

基于Overlap数据输出独立的分析报告，不直接生成方案。
回答以下决策问题：
1. 哪些标签AND后收窄微弱（r>70%，几乎不缩量）？
2. 哪些标签AND后收窄强烈（r<15%，人群过小）？
3. 哪些标签AND后收窄适中（r 15%-50%，适合综合型）？
4. 哪些标签高度重合（冗余）？
5. 同维度OR扩量能带来多少增量？（如果有exact pair数据）
6. 哪些标签可以带来新增？

输入：overlap分析结果（analyze_overlap.py输出）
输出：可读的分析报告JSON，供Step 12生成方案使用。
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def _name_lookup(tid, tag_pool, overrides=None):
    nm = None
    if overrides:
        nm = overrides.get(int(tid))
    if nm:
        return nm
    if tag_pool:
        tm = {int(t["tagId"]): t for t in tag_pool if t.get("isDirectory") == 1}
        return tm.get(int(tid), {}).get("tagName", str(tid))
    return str(tid)


def analyze(overlap_data: Dict, tag_pool: List[Dict] = None, m_amt: int = 0) -> Dict:
    mvo = overlap_data.get("must_vs_optional", [])
    rels = overlap_data.get("tag_relations", {})
    opt_names = {}
    for r in mvo:
        if r.get("tagName"):
            opt_names[r["tagId"]] = r["tagName"]

    # 分类AND收窄效果
    narrow_weak = []    # r > 0.7，收窄微弱
    narrow_moderate = [] # r 0.15-0.5，收窄适中
    narrow_strong = []  # r < 0.15，收窄强
    narrow_errors = []
    for r in mvo:
        tid = r.get("tagId")
        rv = r.get("r")
        entry = {
            "tagId": tid,
            "tagName": _name_lookup(tid, tag_pool, opt_names),
            "r": rv,
            "amount_int": r.get("amount_int"),
            "precision": r.get("precision", "exact"),
        }
        if rv is None:
            if r.get("error"):
                narrow_errors.append({**entry, "error": r["error"]})
            continue
        if rv > 0.7:
            narrow_weak.append(entry)
        elif rv < 0.15:
            narrow_strong.append(entry)
        else:
            narrow_moderate.append(entry)

    # 按r排序
    narrow_weak.sort(key=lambda x: -x["r"])
    narrow_moderate.sort(key=lambda x: abs(x["r"] - 0.3))
    narrow_strong.sort(key=lambda x: x["r"])

    # 同维度OR扩量增量分析
    or_expansion = []
    for p in rels.get("same_dim_exact", []):
        ta = p.get("tagId_a")
        tb = p.get("tagId_b")
        amt_int = p.get("amount_int")
        if amt_int is not None and m_amt > 0:
            # 需要|A|和|B|独立量级才能精确算并集，这里只有交集
            # 但可以提供交集量级供判断
            intersection = amt_int
            # 如果A是MUST中已有的标签，B是OR追加的标签：
            # |M ∪ B| ≈ |M| + |B\M| = |M| + (|B| - |M∩B|) → 但|B|未知
            # 能精确告诉用户的是交集有多少（帮助判断重叠程度）
            na = _name_lookup(ta, tag_pool, opt_names)
            nb = _name_lookup(tb, tag_pool, opt_names)
            or_expansion.append({
                "tagId_a": ta, "tagId_b": tb,
                "tagName_a": na, "tagName_b": nb,
                "dimension": p.get("dimension"),
                "amount_intersection": intersection,
                "intersection_pct_of_m": round(intersection / m_amt * 100, 1) if m_amt else None,
                "note": f"{na}∩{nb}交集{intersection:,}人，重叠率{round(intersection/m_amt*100,1)}%（占M比例）。OR并集精确增量需标签独立量级|x|数据。"
            })

    # 互斥/父子总结
    mutex_summary = []
    for m in rels.get("mutex", []):
        mutex_summary.append(f"{m.get('tagName_a')} ∩ {m.get('tagName_b')}: 互斥(r=0)")
    ancestor_summary = []
    for a in rels.get("ancestor", []):
        ancestor_summary.append(f"{a.get('tagName_a')} 覆盖 {a.get('tagName_b')}(r=100%)")

    # 生成建议
    suggestions = {
        "and_recommended": [e["tagName"] for e in narrow_moderate[:3]],
        "and_too_weak": [e["tagName"] for e in narrow_weak],
        "and_too_strong": [e["tagName"] for e in narrow_strong[:3]],
        "expand_note": "扩量主要通过减AND条件（去掉PREFERRED限制）或同维度OR追加标签实现。",
    }

    report = {
        "m_amount": m_amt,
        "narrow_weak": narrow_weak,
        "narrow_moderate": narrow_moderate,
        "narrow_strong": narrow_strong,
        "narrow_errors": narrow_errors,
        "mutex_summary": mutex_summary,
        "ancestor_summary": ancestor_summary,
        "or_expansion": or_expansion,
        "suggestions": suggestions,
    }
    return report


def fmt_report_text(report: Dict) -> str:
    """格式化为可读文本。"""
    lines = []
    M = report.get("m_amount", 0)
    lines.append(f"📊 MUST基准量级：{M:,}")
    lines.append("")

    def _fmt_entry(e):
        rv = e.get('r')
        amt = e.get('amount_int')
        r_str = f"r={rv:.1%}" if rv is not None else "r=?"
        amt_str = f"剩余≈{amt:,}" if amt is not None else ""
        return f"  {e['tagName']}: {r_str}{', '+amt_str if amt_str else ''}"

    lines.append("━━━ AND收窄分析 ━━━")
    if report["narrow_weak"]:
        lines.append("🟢 收窄微弱（r>70%，加了几乎不缩量，冗余度高）：")
        for e in report["narrow_weak"]:
            lines.append(_fmt_entry(e))
    if report["narrow_moderate"]:
        lines.append("🟡 收窄适中（r 15%-50%，适合精准定向）：")
        for e in report["narrow_moderate"]:
            lines.append(_fmt_entry(e))
    if report["narrow_strong"]:
        lines.append("🔴 收窄强烈（r<15%，人群过小需谨慎）：")
        for e in report["narrow_strong"]:
            lines.append(_fmt_entry(e))
    lines.append("")

    if report["mutex_summary"]:
        lines.append("━━━ 互斥标签（交集=0）━━━")
        for s in report["mutex_summary"]:
            lines.append(f"  {s}")
        lines.append("")
    if report["ancestor_summary"]:
        lines.append("━━━ 父子标签（交集=子类）━━━")
        for s in report["ancestor_summary"]:
            lines.append(f"  {s}")
        lines.append("")

    if report["or_expansion"]:
        lines.append("━━━ 同维度OR扩量分析 ━━━")
        for e in report["or_expansion"]:
            lines.append(f"  {e['tagName_a']} OR {e['tagName_b']}: {e['note']}")
        lines.append("")

    lines.append("━━━ 建议 ━━━")
    if report["suggestions"]["and_recommended"]:
        lines.append(f"  ✅ 适合AND收窄：{', '.join(report['suggestions']['and_recommended'])}")
    if report["suggestions"]["and_too_weak"]:
        lines.append(f"  ⚠️ AND效果微弱（可省略）：{', '.join(report['suggestions']['and_too_weak'])}")
    if report["suggestions"]["and_too_strong"]:
        lines.append(f"  ⚠️ AND后人群过小（谨慎使用）：{', '.join(report['suggestions']['and_too_strong'])}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--overlap", required=True, help="analyze_overlap.py输出的JSON")
    ap.add_argument("--tag-pool", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--text", default=None, help="同时输出可读文本报告到文件")
    args = ap.parse_args()

    with open(args.overlap, "r", encoding="utf-8") as f:
        overlap_data = json.load(f)

    skill_dir = Path(__file__).parent.parent
    pool_path = Path(args.tag_pool) if args.tag_pool else skill_dir / "tag_pool.json"
    tag_pool = []
    if pool_path.exists():
        with open(pool_path, "r", encoding="utf-8") as f:
            tag_pool = json.load(f)

    m_amt = overlap_data.get("meta", {}).get("must_amount", 0)
    report = analyze(overlap_data, tag_pool, m_amt)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    text = fmt_report_text(report)
    if args.text:
        with open(args.text, "w", encoding="utf-8") as f:
            f.write(text)
    print(text)
    print(json.dumps({"ok": True, "out": args.out}, ensure_ascii=False))


if __name__ == "__main__":
    main()
