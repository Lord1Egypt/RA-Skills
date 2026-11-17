#!/usr/bin/env python3
"""
compliance_scanner.py - Statutory bid-rejection redline scanner (BidHunter v3.5, C1).

Scans tender documents (招标文件) or bid documents (投标文件) against a curated
machine-readable redline library (redlines.json) distilled from:
  - 招标投标法 / 招标投标法实施条例
  - 评标委员会和评标方法暂行规定 (12号令)

Design notes (aligned with risk_scanner.py):
  1. Rule layer: pure regex on redlines.json — ZERO API cost, ZERO network.
  2. LLM layer (optional, --llm): asks the model to catch redlines that regex
     cannot reach (e.g. 实质性要求 buried in prose). Uses the user's own
     MiniMax key; skipped gracefully when unconfigured.

Usage:
  python3 compliance_scanner.py <file.pdf|docx|txt|md> [--mode tender|bid|both]
  python3 compliance_scanner.py --list                 # dump all redlines
  python3 compliance_scanner.py --checklist            # pre-submission checklist
  python3 compliance_scanner.py <file> --json          # machine-readable output
  python3 compliance_scanner.py <file> --llm           # add LLM second pass
"""
import os
import sys
import json
import re
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
REDLINES_PATH = os.path.join(HERE, "redlines.json")
SCRIPT_DIR = os.path.dirname(HERE)          # scripts/
AI_DIR = os.path.join(SCRIPT_DIR, "ai")

SEV_ORDER = {"致命": 0, "风险": 1, "提示": 2}
# v2.8: the old single MAX_CHARS=9000 window meant a 200-page tender was 95%
# unread. Kept only as the per-request LLM budget; the rule layer now runs on
# the full text and the LLM layer is segmented (see llm_scan).
MAX_CHARS = 8000
SEG_OVERLAP = 300


def load_redlines(path=REDLINES_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_text(path):
    """Read plain text; try doc_parser for pdf/docx with graceful fallback.

    v2.8 fix: previously called doc_parser.parse_document(), which does not
    exist. The ImportError was swallowed by the bare `except`, so every PDF or
    DOCX scan silently scanned an empty string and reported zero findings
    while still printing a confident checklist. Now uses the real `parse()`
    and reports the backend so a silent failure is visible.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext in (".txt", ".md"):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read(), "text"
        except Exception as e:
            print(f"[warn] 无法读取 {path}: {e}", file=sys.stderr)
            return "", "none"
    # pdf/docx -> v2.0 doc_parser
    sys.path.insert(0, AI_DIR)
    try:
        from doc_parser import parse
        text, backend = parse(path)
        if not text:
            print(f"[warn] 未能从 {os.path.basename(path)} 提取文本"
                  f"（backend={backend}）。纯扫描件需先 OCR；"
                  f"建议 pip install PyPDF2 或安装 poppler 的 pdftotext。",
                  file=sys.stderr)
        return text, backend
    except Exception as e:
        print(f"[warn] doc_parser 调用失败: {e}", file=sys.stderr)
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read(), "text"
        except Exception as e2:
            print(f"[warn] 无法读取 {path}: {e2}", file=sys.stderr)
            return "", "none"


def _excluded(rl, text):
    """Return the matched exclude pattern (or None) for a redline."""
    for pat in rl.get("exclude_patterns", []):
        try:
            if re.search(pat, text):
                return pat
        except re.error:
            continue
    return None


def rule_scan(text, redlines, mode="both"):
    """Regex scan. mode: tender (招标文件) / bid (投标文件) / both."""
    findings = []
    excluded = []
    for rl in redlines.get("redlines", []):
        pats = []
        if mode in ("tender", "both"):
            pats += [("tender", p) for p in rl.get("tender_patterns", [])]
        if mode in ("bid", "both"):
            pats += [("bid", p) for p in rl.get("bid_patterns", [])]

        for scope, pat in pats:
            try:
                m = re.search(pat, text)
            except re.error:
                continue
            if not m:
                continue

            # 反向排除：命中 exclude_patterns 则该红线在本文件中不适用
            ex = _excluded(rl, text)
            if ex:
                excluded.append({
                    "id": rl["id"],
                    "name": rl["name"],
                    "reason": rl.get("exclude_note", f"命中排除模式: {ex}"),
                    "matched_pattern": ex,
                    "layer": "rule",
                })
                break

            s, e = max(0, m.start() - 30), min(len(text), m.end() + 30)
            findings.append({
                "id": rl["id"],
                "category": rl["category"],
                "category_name": redlines["categories"][rl["category"]]["name"],
                "name": rl["name"],
                "legal_basis": rl["legal_basis"],
                "severity": rl.get("severity", "提示"),
                "scope": scope,
                "snippet": text[s:e].replace("\n", " "),
                "check": rl.get("check", ""),
                "remedy": rl.get("remedy", ""),
                "layer": "rule",
            })
            break  # one hit per redline to avoid noise

    # manual-only redlines: always surface as checklist items, never as text hits
    manual_items = [
        {
            "id": rl["id"],
            "category": rl["category"],
            "category_name": redlines["categories"][rl["category"]]["name"],
            "name": rl["name"],
            "legal_basis": rl["legal_basis"],
            "severity": rl.get("severity", "提示"),
            "scope": "manual",
            "snippet": "",
            "check": rl.get("check", ""),
            "remedy": rl.get("remedy", ""),
            "layer": "checklist",
        }
        for rl in redlines.get("redlines", [])
        if rl.get("manual")
    ]
    return findings, manual_items, excluded


def llm_scan(text, redlines):
    """Optional second pass: LLM catches redlines regex cannot reach.

    v2.8: was a single MAX_CHARS=9000 window. Now segmented so a long tender
    is scanned in full. Findings from every segment are concatenated and
    deduplicated by (name, snippet).
    """
    sys.path.insert(0, AI_DIR)
    try:
        from doc_parser import segment
    except Exception:
        segment = None
    try:
        from minimax_client import MiniMaxClient, ConfigError
        client = MiniMaxClient.from_config()
    except Exception as e:
        return [{"severity": "提示", "name": "LLM 未配置，跳过智能补充扫描",
                 "legal_basis": "-", "snippet": str(e), "layer": "llm",
                 "category": "-", "category_name": "LLM", "check": "", "remedy": "",
                 "id": "LLM", "scope": "llm"}]

    segs = segment(text, budget=MAX_CHARS, overlap=SEG_OVERLAP) or [(0, text[:MAX_CHARS])]
    cats = "；".join(f"{k}={v['name']}" for k, v in redlines["categories"].items())
    system = (
        "你是招投标合规审查专家。依据《招标投标法》《招标投标法实施条例》《评标委员会和"
        "评标方法暂行规定》(12号令)，从文本中找出可能导致投标被拒收/否决/无效的风险点，"
        "特别是『实质性要求』类条款（用必须/应/不得表述、要求提供特定承诺函、关键参数带★）。"
        "只输出 JSON 数组，每项含 id(自拟如 X01)、category(A/B/C/D/E 之一或 '-')、"
        "name(风险名)、legal_basis(法条，不确定填'待核')、severity(致命/风险/提示)、"
        "snippet(原文片段,≤40字)、check(自检动作)。无则输出空数组 []。分类：" + cats
    )

    collected = []
    seen = set()
    for i, (_idx, piece) in enumerate(segs):
        prompt = (f"待审文本片段（第 {i+1}/{len(segs)} 段）：\n'''{piece}'''\n"
                  f"只找本片段中的风险点。")
        try:
            raw = client.chat(prompt, system=system, json_mode=True).strip()
            if raw.startswith("```"):
                raw = raw[raw.find("["): raw.rfind("]") + 1]
            for it in json.loads(raw):
                if not isinstance(it, dict):
                    continue
                it.setdefault("category", "-")
                it.setdefault("category_name", "LLM")
                it.setdefault("remedy", "")
                it.setdefault("scope", "llm")
                it["layer"] = "llm"
                key = (str(it.get("name", "")), str(it.get("snippet", ""))[:30])
                if key in seen:
                    continue
                seen.add(key)
                collected.append(it)
        except Exception:
            # a failed segment must not discard the segments that succeeded
            continue

    if not collected:
        collected = [{"severity": "提示",
                      "name": f"LLM 扫描完成 {len(segs)} 段，未识别到风险点"
                              f"（空数组）",
                      "legal_basis": "-", "snippet": "", "layer": "llm",
                      "category": "-", "category_name": "LLM", "check": "",
                      "remedy": "", "id": "LLM", "scope": "llm"}]
    return collected


def render_text(findings, manual_items, redlines, mode, excluded=None):
    excluded = excluded or []
    meta = redlines
    out = []
    out.append("=" * 60)
    out.append("⚖️  BidHunter 合规红线扫描 (v3.5)")
    out.append("=" * 60)
    out.append(f"扫描模式: {mode}  规则库: {len(meta.get('redlines', []))} 条")
    out.append("")

    hits = sorted(findings, key=lambda x: SEV_ORDER.get(x.get("severity"), 9))
    fatal = [f for f in hits if f.get("severity") == "致命"]
    warn = [f for f in hits if f.get("severity") == "风险"]
    info = [f for f in hits if f.get("severity") == "提示"]

    for label, group, mark in (("🔴 致命", fatal, "🔴"), ("🟠 风险", warn, "🟠"),
                               ("🟡 提示/保护", info, "🟡")):
        if not group:
            continue
        out.append(f"--- {label}（{len(group)}）---")
        for f in group:
            out.append(f"{mark} [{f['id']}] {f['name']}")
            out.append(f"    依据: {f['legal_basis']}")
            if f.get("snippet"):
                out.append(f"    命中: …{f['snippet']}…")
            if f.get("check"):
                out.append(f"    自检: {f['check']}")
            if f.get("remedy"):
                out.append(f"    补救: {f['remedy']}")
            out.append("")

    if excluded:
        out.append(f"--- ⚪ 已排除（{len(excluded)} 项，本文件不适用）---")
        for x in excluded:
            out.append(f"⚪ [{x['id']}] {x['name']} — {x['reason']}")
        out.append("")

    if manual_items:
        out.append(f"--- ✅ 人工核对清单（{len(manual_items)} 项，正则不可达，必须逐条人工确认）---")
        for m in sorted(manual_items, key=lambda x: SEV_ORDER.get(x.get("severity"), 9)):
            out.append(f"☐ [{m['id']}] {m['name']}（{m['legal_basis']}）")
            if m.get("check"):
                out.append(f"    → {m['check']}")
        out.append("")

    out.append("=" * 60)
    out.append("⚠️  本扫描为法规条文索引的本地提示，不构成法律意见；")
    out.append("   最终判定以招标文件、评标委员会认定及有权机关解释为准。")
    out.append("   深度审查请联动姊妹 skill：bid-rejection-guard / bid-price-redline /")
    out.append("   multi-entity-bid-isolation（多主体投标必先查实施条例第34条）。")
    out.append("=" * 60)
    return "\n".join(out)


def render_checklist(redlines):
    out = ["📋 交标前合规自查清单（BidHunter v3.5 · 共 %d 条）" % len(redlines["redlines"])]
    out.append("")
    for cat_key, cat in redlines["categories"].items():
        items = [r for r in redlines["redlines"] if r["category"] == cat_key]
        if not items:
            continue
        out.append(f"【{cat_key}·{cat['name']}】{cat['consequence']}（决定方：{cat['decider']}）")
        for r in items:
            mark = "★" if r.get("severity") == "致命" else "·"
            out.append(f"  {mark} [{r['id']}] {r['name']} — {r['legal_basis']}")
            if r.get("check"):
                out.append(f"      → {r['check']}")
        out.append("")
    out.append("⚠️ 多主体（≥2个主体投同一标段）必先查 [C02] 实施条例第34条资格红线。")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="BidHunter 合规红线扫描器 v3.5")
    ap.add_argument("file", nargs="?", help="待扫描文件 (pdf/docx/txt/md)")
    ap.add_argument("--mode", default="both", choices=["tender", "bid", "both"],
                    help="tender=扫招标文件找埋雷; bid=扫投标文件找致命项; both=都扫")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--llm", action="store_true", help="附加 LLM 智能补充扫描（需 MiniMax Key）")
    ap.add_argument("--list", action="store_true", help="列出全部红线")
    ap.add_argument("--checklist", action="store_true", help="输出交标前自查清单")
    args = ap.parse_args()

    redlines = load_redlines()

    if args.list:
        print(json.dumps(redlines, ensure_ascii=False, indent=2))
        return
    if args.checklist:
        print(render_checklist(redlines))
        return
    if not args.file:
        ap.error("需要 <file>，或用 --list / --checklist")

    text, backend = read_text(args.file)
    if not text.strip():
        print(f"[error] 文件为空或无法解析: {args.file}", file=sys.stderr)
        sys.exit(1)

    findings, manual_items, excluded = rule_scan(text, redlines, args.mode)
    if args.llm:
        findings += llm_scan(text, redlines)

    if args.json:
        print(json.dumps({
            "file": args.file, "mode": args.mode, "backend": backend,
            "chars_read": len(text),
            "rule_hits": len(findings), "manual_items": len(manual_items),
            "excluded": len(excluded),
            "findings": findings, "checklist": manual_items,
            "excluded_items": excluded,
        }, ensure_ascii=False, indent=2))
    else:
        print(render_text(findings, manual_items, redlines, args.mode, excluded))


if __name__ == "__main__":
    main()
