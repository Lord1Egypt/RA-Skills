#!/usr/bin/env python3
"""report.py - Report export / 报告产出 (Markdown + optional JSON/PNG)."""
import argparse
import json
import os
import sys

# Shared ct-base source_guard is resolved from this skill's own scripts/ dir.
# IMPORTANT (2026-08-11): ct-base is NEVER published. Every ct- skill must carry
# its own complete copy. We ONLY resolve from this skill's own `scripts/` dir —
# never fall back to a ct-base sibling.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

try:
    from source_guard import require_source  # BASE.md §17.1 溯源红线
except Exception:  # noqa: BLE001  (vendored copy guaranteed in publish package)
    require_source = None


# ---- Report UI language (v0.14.4) ------------------------------------------
# A Markdown deliverable must not silently switch to English just because the
# runtime container has an en_US locale. The workbench injects
# CT_REGISTRY_LANG from the current UI language; prompt-driven CLI calls default
# to Chinese (this skill's primary audience). Only the interface chrome is
# localized — registry titles / status enums / sponsor names keep their source
# spelling on purpose (data fidelity, same rule as export_xlsx.py).
_TXT = {
    "zh": {
        "title": "## 📊 临床试验注册库检索报告\n",
        "total": "试验总数",
        "phase": "### 分期分布",
        "status": "\n### 试验状态分布",
        "sponsors": "\n### 主要申办方",
        "timeline": "\n### 时间线（起始年份）",
        "competitor": "\n### 竞品格局（适应症 → 申办方数）",
        "sponsors_unit": "家申办方",
        "dedup": "\n### 跨库去重（自建桥接：UTN/TRN 注册号归一 + 模糊匹配）",
        "raw": "- 原始记录",
        "unique": "- 去重后唯一试验",
        "removed": "- 移除重复",
        "groups": "- 跨库重复组",
        "merge": "- 合并依据分布",
        "fuzzy": "  - ⚠️ 其中 {n} 条为模糊匹配合并（标题+单一佐证），"
                 "误并风险最高，建议抽查各条 dedup_reason",
        "source_note": "\n> 数据来源：公开注册库（CT.gov / CDE / ChiCTR / EU CTR / "
                       "ISRCTN / DRKS / WHO ICTRP）。输出仅供参考，非监管提交文件。",
        "unverified": "\n> ⚠️ {n} 条记录缺少可溯源的首页链接，已标记「待核实」，"
                      "请人工复核其来源后再引用。",
        "records": "\n### 逐条记录（含首页链接与可下载文档）",
        "records_note": "- 共 {n} 条 primary 记录；下表给出每条的注册库首页链接，"
                        "以及可下载的详细文档（PDF 等）链接。",
        "homepage": "首页",
        "no_homepage": "首页: (无)",
        "download": "；下载: ",
        "cde_attachment": "；附件: CDE 公示平台详情页可手动下载"
                          "（自动化受 WAF 限制，无直链）",
        "verify": " ⚠️ 待核实",
        "docs_summary": "\n> 可下载文档来源：{n} 条记录含下载链接"
                        "（主要来自 EU-CTR）。用 `--download-docs` 确认后批量下载。",
        "docs_none": "\n> 本次结果无可自动下载的文档直链（CDE 工作流不返回附件 URL；"
                     "CT.gov/WHO 亦无协议 PDF API）。如需 CDE 原文，请到其公示平台手动下载。",
        "png_title": "分期分布",
    },
    "en": {
        "title": "## 📊 Clinical Trial Registry Report\n",
        "total": "Total trials",
        "phase": "### Phase distribution",
        "status": "\n### Status distribution",
        "sponsors": "\n### Top sponsors",
        "timeline": "\n### Timeline (start year)",
        "competitor": "\n### Competitor landscape (indication → sponsor count)",
        "sponsors_unit": "sponsors",
        "dedup": "\n### De-duplication (in-house bridge: UTN/TRN "
                 "registration-number normalization + fuzzy matching)",
        "raw": "- Raw records",
        "unique": "- Unique trials after de-duplication",
        "removed": "- Removed duplicates",
        "groups": "- Cross-source duplicate groups",
        "merge": "- Merge-evidence breakdown",
        "fuzzy": "  - ⚠️ {n} of these were merged by fuzzy matching "
                 "(title + a single corroborator) — highest over-merge risk; "
                 "spot-check the dedup_reason field",
        "source_note": "\n> Sources: public registries (CT.gov / CDE / ChiCTR / "
                       "EU CTR / ISRCTN / DRKS / WHO ICTRP). Reference only, "
                       "not a regulatory submission.",
        "unverified": "\n> ⚠️ {n} records lack a traceable registry homepage and "
                      "are marked 'to be verified'; check their source before citing.",
        "records": "\n### Records (with homepage links and downloadable documents)",
        "records_note": "- {n} primary records; registry homepage links and "
                        "downloadable document links (PDF etc.) are listed below.",
        "homepage": "Homepage",
        "no_homepage": "Homepage: (none)",
        "download": "; Downloads: ",
        "cde_attachment": "; Attachments: download manually from the CDE "
                          "disclosure platform (automation blocked by WAF, no direct URL)",
        "verify": " ⚠️ to be verified",
        "docs_summary": "\n> Downloadable documents: {n} records carry download "
                        "links (mostly EU-CTR). Confirm with `--download-docs` "
                        "to fetch in bulk.",
        "docs_none": "\n> No automatically downloadable document links in this run "
                     "(the CDE workflow returns no attachment URLs; CT.gov/WHO "
                     "have no protocol-PDF API either). Fetch CDE originals "
                     "manually from its disclosure platform.",
        "png_title": "Phase distribution",
    },
}


def report_lang(lang=None):
    """Resolve the Markdown UI language (zh default, never OS-locale-only)."""
    code = str(lang or os.environ.get("CT_REGISTRY_LANG") or "").strip().lower()
    if code.startswith("en"):
        return "en"
    return "zh"


def md(agg, lang=None):
    t = _TXT[report_lang(lang)]
    L = []
    L.append(t["title"])
    L.append(f"- **{t['total']}**: {agg['total']}\n")
    L.append(t["phase"])
    for k, v in agg["phase_dist"].items():
        L.append(f"- {k}: {v}")
    L.append(t["status"])
    for k, v in agg["status_dist"].items():
        L.append(f"- {k}: {v}")
    L.append(t["sponsors"])
    for k, v in agg["top_sponsors"].items():
        L.append(f"- {k}: {v}")
    L.append(t["timeline"])
    for k, v in agg["timeline"].items():
        L.append(f"- {k}: {v}")
    L.append(t["competitor"])
    for k, v in agg["competitor_map"].items():
        L.append(f"- {k}: {v} {t['sponsors_unit']}")
    # De-duplication summary (跨库去重)
    ds = agg.get("dedup_summary")
    if ds:
        L.append(t["dedup"])
        L.append(f"{t['raw']}: {ds['raw_total']}")
        L.append(f"{t['unique']}: {ds['deduped_total']}")
        L.append(f"{t['removed']}: {ds['removed']}")
        L.append(f"{t['groups']}: {ds['cross_source_groups']}")
        # P1-F: expose the merge-evidence breakdown so an over-merge is visible.
        # tier2_fuzzy merges on "title + one corroborator" only -> highest
        # false-positive risk, so it is called out explicitly for review.
        tb = ds.get("dedup_tier_breakdown")
        if tb:
            parts = ", ".join(f"{k}={v}" for k, v in tb.items())
            L.append(f"{t['merge']}: {parts}")
            if tb.get("tier2_fuzzy"):
                L.append(t["fuzzy"].format(n=tb["tier2_fuzzy"]))
    L.append(t["source_note"])
    # --- Per-record section: homepage links + downloadable documents ---
    recs = agg.get("records") or []
    # Anti-hallucination (BASE.md §17.1): every emitted record must carry a
    # traceable source. The canonical registry homepage `url` is mapped to
    # `source_quote` so registry-origin records auto-verify; only records with
    # NO url are flagged "⚠️ 待核实". We deliberately use require_source ONLY
    # (not guard_records' assert_no_fabrication): retrieval legitimately returns
    # drugs/targets outside the input whitelist (e.g. search NSCLC -> Osimertinib),
    # so the fabrication hard-gate would false-kill valid results.
    if recs and require_source is not None:
        for r in recs:
            if not r.get("source_quote") and r.get("url"):
                r["source_quote"] = r["url"]
        recs, n_unverified = require_source(recs, quote_key="source_quote",
                                            status_key="verification")
        if n_unverified:
            L.append(t["unverified"].format(n=n_unverified))
    if recs:
        L.append(t["records"])
        L.append(t["records_note"].format(n=len(recs)))
        for r in recs:
            rid = r.get("registry_id") or r.get("title") or "?"
            src = r.get("source") or "?"
            title = (r.get("title") or "")[:80]
            status = r.get("status") or ""
            phase = r.get("phase") or ""
            url = r.get("url")
            link = f"[{t['homepage']}]({url})" if url else t["no_homepage"]
            docs = r.get("documents") or []
            doc_line = ""
            if docs:
                doc_line = t["download"] + ", ".join(
                    f"[{d.get('title') or 'doc'}]({d.get('url')})" for d in docs)
            else:
                if src == "CDE":
                    doc_line = t["cde_attachment"]
            flag = t["verify"] if r.get("needs_verification") else ""
            L.append(f"- **{rid}** [{src}] {title} — {status}/{phase} — {link}{doc_line}{flag}")
        # Document manifest summary (where downloadable links exist)
        with_docs = [r for r in recs if r.get("documents")]
        if with_docs:
            L.append(t["docs_summary"].format(n=len(with_docs)))
        else:
            L.append(t["docs_none"])
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", default="report.md")
    ap.add_argument("--json-out")
    ap.add_argument("--png")
    ap.add_argument("--lang", choices=["auto", "zh", "en"], default="auto",
                    help="报告界面语言(auto=CT_REGISTRY_LANG/默认中文, zh, en)")
    args = ap.parse_args()
    lang = report_lang(None if args.lang == "auto" else args.lang)
    with open(args.inp, encoding="utf-8") as f:
        agg = json.load(f)
    text = md(agg, lang)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[report] wrote {args.out}")
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(agg, f, ensure_ascii=False, indent=2)
    if args.png:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            keys = list(agg["phase_dist"].keys())
            vals = list(agg["phase_dist"].values())
            plt.figure(figsize=(6, 4))
            plt.bar([str(k) for k in keys], vals)
            plt.title(_TXT[lang]["png_title"])
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig(args.png, dpi=120)
            print(f"[report] wrote {args.png}")
        except Exception as e:
            print(f"[report] PNG skipped: {e}")


if __name__ == "__main__":
    main()
