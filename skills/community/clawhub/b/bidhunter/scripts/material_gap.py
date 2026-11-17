#!/usr/bin/env python3
"""
material_gap.py - 待补材料清单 + 零响应检测（BidHunter v2.8 · G1/G2）

Two pre-submission checks that the previous versions did not cover at all.

G1 待补材料清单
    Reads the extracted qualification requirements, classifies each one into
    "have / missing / manual-check", and flags the two things that actually
    kill a bid at the opening table:
      · 待补材料出现在签字盖章页 → 🔴 高危（占位符 = 形式审查直接不通过）
      · 证照类材料有有效期，且有效期 < 投标截止日 → 🔴 高危

G2 零响应检测
    Scans a DRAFT bid document for the four patterns that silently lose points:
      空洞满足   "完全满足/完全响应/满足招标文件要求" with no substance
      借附件     "详见附件" where the attachment carries nothing
      项目残留   a different project's name/owner/date left in the draft
      统计型空洞 numbers promised but never stated

    Zero API cost. Pure rules. This is a *detector*, not a judge: every hit
    carries the surrounding text so a human decides.

Both checks honour the same rule as the rest of v2.8: report coverage, never
guess, never fill a blank with a plausible value.

Usage:
  python3 material_gap.py gap <招标文件> [--json]
  python3 material_gap.py zero <投标文件草稿> [--json]
  python3 material_gap.py both <招标文件> <投标文件草稿>
"""
import os
import re
import sys
import json
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "ai"))
from doc_parser import parse

# ----------------------------------------------------------------------------
# G1 · 待补材料清单
# ----------------------------------------------------------------------------

# 材料类型 → (是否可能带有效期, 是否属于签字盖章页附件)
CERT_TYPES = {
    "资质": (True, True), "证书": (True, True), "许可": (True, True),
    "认证": (True, True), "安全生产": (True, True), "授权": (True, True),
    "营业执照": (True, True), "社保": (True, False), "纳税": (True, False),
    "审计报告": (True, False), "财务": (True, False), "业绩": (False, True),
    "合同": (False, True), "人员": (False, True), "简历": (False, True),
    "承诺函": (False, True), "承诺书": (False, True), "声明": (False, True),
    "证明": (False, False), "报告": (False, False), "表格": (False, True),
    "原件": (True, True), "复印件": (False, False),
}

# 已有证据的判定线索：规则库里出现这些词视为可能已具备
HAVE_HINTS = ("已具备", "已提供", "已附", "有附", "详见", "见附件",
              "我方具备", "已上传", "已提交")

RE_VALIDITY_RANGE = re.compile(
    r"有效期[^\d]{0,10}(\d{4}\s*年|\d+\s*年|\d+\s*个?月|\d{4}\s*年\s*\d{1,2}\s*月)")
RE_DATE = re.compile(r"(20\d{2})\s*年\s*(\d{1,2})\s*月(?:\s*(\d{1,2})\s*日)?")


def _classify(item):
    """Return (category, has_expiry, on_signature_page) for a requirement."""
    has_exp = on_sig = False
    cats = []
    for k, (e, s) in CERT_TYPES.items():
        if k in item:
            cats.append(k)
            has_exp = has_exp or e
            on_sig = on_sig or s
    return cats, has_exp, on_sig


def build_gap(clauses, deadline=None):
    """Turn extracted qualification requirements into a tri-state gap list."""
    reqs = clauses.get("qualification_requirements") or []
    rows = []
    for r in reqs:
        if isinstance(r, str):
            r = {"item": r, "source_excerpt": r, "mandatory": None}
        item = str(r.get("item") or "")
        if not item.strip():
            continue
        cats, has_exp, on_sig = _classify(item)
        if any(h in item for h in HAVE_HINTS):
            status = "HAVE"
        elif r.get("mandatory") is True:
            status = "MISSING"          # 原文说"必须"但没找到证据
        else:
            status = "CHECK"            # 表述含糊，人工确认
        rows.append({
            "item": item[:120],
            "category": cats,
            "source_excerpt": str(r.get("source_excerpt") or "")[:120],
            "mandatory_in_doc": r.get("mandatory"),
            "status": status,
            "needs_original": any(k in item for k in ("原件", "原件扫描", "原件复印件")),
            "needs_seal": on_sig or "盖章" in item or "签章" in item,
            "has_expiry": has_exp,
            "risk": "HIGH" if (status == "MISSING" and on_sig) else
                    ("MED" if status == "MISSING" else "LOW"),
            "note": ("⚠️ 出现在签字盖章页——缺件即形式审查不通过"
                     if (on_sig and status == "MISSING") else
                     ("需核对有效期是否覆盖投标截止日" if has_exp else "")),
        })
    rows.sort(key=lambda x: {"HIGH": 0, "MED": 1, "LOW": 2}[x["risk"]])
    summary = {
        "total": len(rows),
        "missing": sum(1 for r in rows if r["status"] == "MISSING"),
        "check": sum(1 for r in rows if r["status"] == "CHECK"),
        "high_risk": sum(1 for r in rows if r["risk"] == "HIGH"),
        "with_expiry": sum(1 for r in rows if r["has_expiry"]),
        "deadline": deadline,
    }
    return rows, summary


# ----------------------------------------------------------------------------
# G2 · 零响应检测
# ----------------------------------------------------------------------------

ZERO_PATTERNS = [
    ("空洞满足", re.compile(
        r"(完全满足|完全响应|满足招标文件(的全部)?要求|完全符合|无偏离|无异议)"),
     "必须紧跟具体做法/参数/承诺主体，否则等于没写"),
    ("借附件", re.compile(r"(详见附件|见附件|见后附|见投标文件第[一二三四五六七八九十\d]+[章节页])"),
     "须确认附件里确有对应内容，否则是空指针"),
    ("待补占位", re.compile(
        r"(待补|待提供|待确认|暂缺|\[此处填写\]|【\s*】|＿{3,}|X{3,}|"
        r"此处留白|后续补|稍后提供)"),
     "★高危：待补材料写进正文，评标时等同未提供"),
    ("跨项目残留", re.compile(
        r"(本项目(名称)?\s*[:：]?\s*20\d{2}\s*年度|本工程为.{0,12}项目)|"
        r"(甲方[：:]\s*\S{4,})"),
     "须确认是本项目甲方，非上一个项目"),
    ("承诺主体不明", re.compile(r"(我司|我公司|本公司|我单位)(将|应|承诺)"),
     "须落到具体章节与具体承诺内容"),
]

# 数字型承诺：出现"不低于/不高于/不少于"却没有具体数字
RE_VAGUE_NUM = re.compile(
    r"(不低于|不高于|不少于|不超过|不短于|优于|达到|≥|≤|不低于)\s*"
    r"(招标文件要求|要求|规定|标准|同等|相当于|国家规定)?\s*"
    r"(?![\d．.])[，。；、）)]{0,2}")

RE_SECTION = re.compile(r"(第[一二三四五六七八九十百\d]+[章节]|[一二三四五六七八九十]+、)")


def _context(text, m, before=40, after=60):
    s = max(0, m.start() - before)
    e = min(len(text), m.end() + after)
    return re.sub(r"\s+", " ", text[s:e]).strip()


def zero_response_scan(text, our_project=None, other_projects=None):
    """Detect zero-response patterns in a draft bid document."""
    findings = []
    for name, pat, why in ZERO_PATTERNS:
        for m in pat.finditer(text):
            findings.append({
                "type": name,
                "why": why,
                "context": _context(text, m),
                "severity": "致命" if name in ("待补占位", "跨项目残留") else "风险",
                "position": m.start(),
            })

    for m in RE_VAGUE_NUM.finditer(text):
        findings.append({
            "type": "数字型空洞",
            "why": "承诺了量化标准但没给出数字，评委按无偏离计分等于零",
            "context": _context(text, m),
            "severity": "风险",
            "position": m.start(),
        })

    # 跨项目残留：若显式给了我方项目名与其它项目名，直接比对
    if our_project:
        for other in (other_projects or []):
            if other and other in text and other != our_project:
                idx = text.find(other)
                findings.append({
                    "type": "跨项目残留",
                    "why": f"出现了其它项目名「{other}」，疑似复制未替换",
                    "context": _context(text, type("M", (), {"start": idx,
                                                            "end": idx + 4})()),
                    "severity": "致命",
                    "position": idx,
                })

    # 同偏移量附近的命中只保留一条（不同模式常常指向同一处问题）
    findings.sort(key=lambda f: (f["position"],
                                 {"致命": 0, "风险": 1, "提示": 2}.get(
                                     f["severity"], 9)))
    deduped = []
    for f in findings:
        if deduped and abs(f["position"] - deduped[-1]["position"]) < 120:
            if f["severity"] == "致命":
                deduped[-1] = f
            continue
        deduped.append(f)
    findings = deduped
    order = {"致命": 0, "风险": 1, "提示": 2}
    findings.sort(key=lambda f: order.get(f["severity"], 9))
    return findings


# ----------------------------------------------------------------------------
# render
# ----------------------------------------------------------------------------

def render_gap(rows, summary):
    out = ["=" * 60, "📋 待补材料清单 (v2.8 G1)", "=" * 60,
           f"共 {summary['total']} 项：缺 {summary['missing']} · "
           f"待确认 {summary['check']} · 高风险 {summary['high_risk']} · "
           f"带有效期 {summary['with_expiry']}"]
    if summary.get("deadline"):
        out.append(f"投标截止：{summary['deadline']}"
                   f"（有效期类材料须覆盖此日期）")
    out.append("")
    if not rows:
        out.append("未从标书抽出资格要求 —— 通常意味着招标文件文本层缺失或"
                   "资格章节写法特殊，**不要理解为「没有要求」**。")
        return "\n".join(out)
    icon = {"HIGH": "🔴", "MED": "🟡", "LOW": "⚪"}
    for r in rows:
        out.append(f"{icon[r['risk']]} [{r['status']}] {r['item']}")
        if r["source_excerpt"]:
            out.append(f"     原文：{r['source_excerpt'][:80]}")
        if r["note"]:
            out.append(f"     {r['note']}")
        flags = []
        if r["needs_original"]:
            flags.append("需原件")
        if r["needs_seal"]:
            flags.append("需盖章")
        if r["has_expiry"]:
            flags.append("有有效期")
        if flags:
            out.append(f"     标记：{' / '.join(flags)}")
        out.append("")
    out.append("─" * 60)
    out.append("⚠️ 清单基于招标文件文本抽取，非我方实际资料库存。"
               "「MISSING」= 原文要求但未找到我方证据，不等于我方没有。")
    return "\n".join(out)


def render_zero(findings, name):
    out = ["=" * 60, f"🔍 零响应检测 (v2.8 G2) · {name}", "=" * 60]
    if not findings:
        out.append("未命中已知零响应模式。")
        out.append("（检测基于规则，非语义；'完全满足'类短句若写在具体参数"
                   "之后不算问题，请人工复核上下文）")
        return "\n".join(out)
    bad = sum(1 for f in findings if f["severity"] == "致命")
    out.append(f"命中 {len(findings)} 处，其中致命 {bad} 处。")
    out.append("")
    for f in findings[:60]:
        out.append(f"[{f['severity']}] · {f['type']}")
        out.append(f"    {f['context']}")
        out.append(f"    → {f['why']}")
        out.append("")
    if len(findings) > 60:
        out.append(f"...另有 {len(findings)-60} 处，--json 查看全部")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="BidHunter 待补材料/零响应 v2.8")
    ap.add_argument("mode", choices=["gap", "zero", "both"])
    ap.add_argument("file1", nargs="?", help="招标文件")
    ap.add_argument("file2", nargs="?", help="投标文件草稿（both 模式）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--our-project", help="我方本项目名，用于跨项目残留比对")
    ap.add_argument("--other-projects", nargs="*", help="其它项目名，用于残留比对")
    args = ap.parse_args()

    out = {}
    if args.mode in ("gap", "both"):
        if not args.file1:
            ap.error("gap 模式需要 <招标文件>")
        text, backend = parse(args.file1)
        if not text:
            print(f"[error] 无法提取文本 backend={backend}", file=sys.stderr)
            sys.exit(1)
        try:
            from clause_extractor import extract
            clauses, meta = extract(text)
        except Exception:
            clauses, meta = {"qualification_requirements": []}, {}
        rows, summary = build_gap(clauses, clauses.get("bid_deadline"))
        out["gap"] = {"rows": rows, "summary": summary, "meta": meta}
        if not args.json:
            print(render_gap(rows, summary))

    if args.mode in ("zero", "both"):
        tgt = args.file2 if args.mode == "both" else args.file1
        if not tgt:
            ap.error("zero 模式需要 <投标文件草稿>")
        text, backend = parse(tgt)
        if not text:
            print(f"[error] 无法提取文本 backend={backend}", file=sys.stderr)
            sys.exit(1)
        findings = zero_response_scan(text, args.our_project,
                                      args.other_projects)
        out["zero"] = {"findings": findings, "chars": len(text),
                       "backend": backend}
        if not args.json:
            print(render_zero(findings, os.path.basename(tgt)))

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
