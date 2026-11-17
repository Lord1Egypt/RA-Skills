#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ma_extractor.py — 路线 C：公开文献 MA 效应量候选抽取器（ct-samplesize）。

流水线：PubMed esearch → efetch 摘要 → 荟萃分析甄别（复用 ct-literature
doc_type_filter）→ 正则效应量抽取（HR/OR/RR/MD/SMD + 95%CI）→ 候选 JSON
（与 effect_ref.py / --effect-ref 入库格式互认）+ markdown 人工确认对照表。

纪律（与 ct-samplesize 评估文档一致）：
- 纯 Python 标准库（urllib/regex/xml.etree），零新依赖，不算样本量；
- 产出的是「候选」（candidates），绝不直接写入 references/effect_size_benchmarks/；
  人工逐条核实（对照 excerpt 原文句）确认后，方可用 --confirm 拷入基准库；
- 每条候选带 pmid/source/excerpt/as_of，全程可溯源；
- 摘要级抽取命中率有限（约 5–7 成），确认时人工补录全文值即可。

用法：
  python ma_extractor.py --query "depression AND exercise AND meta-analysis" \
      --ta "抑郁症" --endpoint "HAMD-17 均值差" \
      --out candidates.json [--retmax 20] [--sheet candidates.md]

确认入库：
  人工编辑 candidates.json（删除/修正条目，确认 verify 字段）后：
  python ma_extractor.py --confirm candidates.json \
      --into "C:/Users/Wintone/.workbuddy/skills/ct-samplesize/references/effect_size_benchmarks/抑郁症__HAMD-17.json"
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
UA = {"User-Agent": "ct-samplesize-ma_extractor/1.0 (workflow: curated benchmark ingest)"}
DISCLAIMER = ("Benchmarks are user-supplied from PUBLIC published meta-analyses only "
              "(e.g. Cochrane/PubMed). NOT derived from any commercial curated database.")
_CANDIDATE_NOTE = "CANDIDATE — NOT VERIFIED. 人工核实（对照 excerpt/原文全文）并确认后方可入库。"


# ---------------------------------------------------------------- eutils ---
def _http_get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def search_pmids(query, retmax=20, use_proxy_env=True):
    """esearch → pmid 列表。默认遵循环境代理（WorkBuddy 注入即可用）。"""
    q = urllib.parse.urlencode({
        "db": "pubmed", "term": query, "retmax": str(retmax),
        "retmode": "json", "sort": "relevance",
        "tool": "ct-samplesize-ma_extractor", "email": "user@example.org",
    })
    data = json.loads(_http_get(f"{EUTILS}/esearch.fcgi?{q}"))
    return data.get("esearchresult", {}).get("idlist", [])


def fetch_records(pmids):
    """efetch → 记录列表（pmid/title/abstract/journal/year/pub_types）。"""
    if not pmids:
        return []
    q = urllib.parse.urlencode({
        "db": "pubmed", "id": ",".join(pmids),
        "rettype": "abstract", "retmode": "xml",
        "tool": "ct-samplesize-ma_extractor", "email": "user@example.org",
    })
    root = ET.fromstring(_http_get(f"{EUTILS}/efetch.fcgi?{q}"))
    records = []
    for art in root.findall(".//PubmedArticle"):
        pmid = (art.findtext(".//PMID") or "").strip()
        title = (art.findtext(".//ArticleTitle") or "").strip()
        # AbstractText 可能分节（BACKGROUND/OBJECTIVE/...）
        abstract = "\n".join(
            (t.text or "") + "".join((s.text or "") for s in t.findall("i")) + ""
            for t in art.findall(".//Abstract/AbstractText")).strip()
        journal = (art.findtext(".//Journal/Title") or "").strip()
        year = (art.findtext(".//JournalIssue/PubDate/Year")
                or art.findtext(".//JournalIssue/PubDate/MedlineDate") or "").strip()
        pub_types = [pt.text for pt in art.findall(".//PublicationTypeList/PublicationType")
                     if pt.text]
        records.append({"pmid": pmid, "title": title, "abstract": abstract,
                        "journal": journal, "year": year, "pub_types": pub_types})
    return records


# ------------------------------------------------------------- MA 甄别 ----
_MA_TITLE = re.compile(
    r"systematic review|meta-?analy|\bnetwork meta\b|meta-regression|pooled analysis",
    re.I)
_MA_PUBTYPE = re.compile(r"systematic review|meta-?analysis", re.I)


def is_meta_analysis(rec):
    """三层信号：pubType 强通道 > 标题 > 摘要声明短语。返回 (bool, signal)。"""
    pts = ";".join(rec.get("pub_types") or [])
    if pts and _MA_PUBTYPE.search(pts):
        return True, "pubtype:" + pts
    if _MA_TITLE.search(rec.get("title") or ""):
        return True, "title"
    head_low = ((rec.get("title") or "") + "\n"
                + (rec.get("abstract") or "")[:1500]).lower()
    if re.search(r"we (conducted|performed) (a|this) (systematic review|meta-?analysis)"
                 r"|this (systematic review|meta-?analysis|network meta-?analysis)"
                 r"|(systematic review|meta-?analysis) (and|was) "
                 r"|(pooled|pooling) (the|data|results|estimates)", head_low):
        return True, "abstract-declaration"
    return False, "no-signal"


# ------------------------------------------------------- 效应量抽取 -------
# 数值：0.72 / .85 / 1.30；CI 分隔符：- – — to ,
_NUM = r"(\d*\.?\d+)"
_SEP = r"\s*(?:-|–|—|to|,)\s*"
_CI = re.compile(
    r"95\s*%?\s*(?:CI|confidence interval)\s*[:=]?\s*"
    + _NUM + _SEP + _NUM, re.I)
# ES 表述与数值相邻的三种典型排布：
#   A: "HR 0.72 (95% CI 0.61-0.85)" / "HR=0.72; 95% CI: 0.61 to 0.85"
#   B: "0.72 (95% CI 0.61-0.85)"（带前缀词距离 <=20 字符内找 scale 词）
#   C: "95% CI 0.61-0.85"（无 scale 上下文 → scale=unknown，供人工判）
_SCALE_WORDS = {
    # 短语允许任意大小写（(?i:...)），缩写词严格大写 + 双词边界（防 "f|or" 误匹配）
    "HR": re.compile(r"(?i:hazard\s*ratio)|\bHR\b"),
    "OR": re.compile(r"(?i:odds\s*ratio)|\bOR\b"),
    "RR": re.compile(r"(?i:risk\s*ratio|relative\s*risk)|\bRR\b"),
    "SMD": re.compile(r"(?i:standardi[sz]ed\s*mean)|\bSMD\b"),
    "MD": re.compile(r"(?i:(?:weighted\s+)?mean\s*difference)"),
}
_EXCERPT_WIN = 160  # excerpt 上下文窗口（前后各 80 字符）


def _excerpt(text, start, end):
    lo, hi = max(0, start - 80), min(len(text), end + 80)
    return re.sub(r"\s+", " ", text[lo:hi]).strip()


# 负向守卫：这些统计量的 CI 不是效应量（NNT/异质性 I²/tau/k 等），宁缺勿滥。
# 注意不挡 "publication bias"——"SMD adjusted for publication bias" 是真效应量。
_NOT_EFFECT = re.compile(
    r"NNT\b|number needed to treat|\bI\s*2\b|I²|heterogeneity|between-study (variance|heterogeneity)|\bk\s*=|"
    r"tau\b|fail-safe", re.I)


def _window_scale(text, pos):
    """在 CI 括号前 <=40 字符窗口内识别效应量类型。"""
    w = text[max(0, pos - 60):pos]
    if _NOT_EFFECT.search(w):
        return "SKIP"          # 负向上下文 → 非效应量，直接丢弃
    for scale, pat in _SCALE_WORDS.items():
        if pat.search(w):
            return scale
    return None


def extract_effects(text, rec=None):
    """从文本（标题+摘要）抽取效应量候选。返回 list[dict]（effect_ref 条目形状）。"""
    src = f"PubMed {rec['pmid']} ({rec.get('year','')}) {rec.get('journal','')}" if rec else ""
    out = []
    for m in _CI.finditer(text):
        lo_ci, hi_ci = float(m.group(1)), float(m.group(2))
        if lo_ci > hi_ci:            # CI 必须低<=高
            continue
        est = None
        scale = _window_scale(text, m.start())
        if scale == "SKIP":          # NNT/I²/k 等非效应量上下文 → 丢弃
            continue
        # 生存率/缓解率等百分比 CI（如 "OS was 82% (95% CI 79-85)"）不是效应量：
        # unknown 且量级超界 → 丢弃（效应量 HR/OR/RR≈0-10，SMD/MD 也很少 >30）
        if scale is None and max(lo_ci, hi_ci) > 30:
            continue
        # A 排布：CI 前紧邻 "<NUM> (95% CI ...)" —— 向前找最近的数值
        before = text[max(0, m.start() - 30):m.start()]
        m_est = re.search(_NUM + r"\s*[(;:，,]?\s*$", before)
        if m_est:
            est = float(m_est.group(1))
        param = {"HR": "hazard_ratio", "OR": "odds_ratio", "RR": "risk_ratio",
                 "SMD": "effect", "MD": "effect", "WMD": "effect"}.get(scale, "effect")
        item = {
            "param": param, "scale": scale or "unknown",
            "estimate": est, "ci_low": lo_ci, "ci_high": hi_ci,
            "n": None, "source": src,
            "pmid": rec["pmid"] if rec else None,
            "excerpt": _excerpt(text, m.start(), m.end()),
            "verify": "pending",     # pending → human 逐条改 ok/reject
        }
        # estimate 缺失时置 None（人工填），但 CI 外无点估计的条目仍保留
        out.append(item)
    # 总样本量（粗通道，仅摘要级提示，人工核实）
    m_n = re.search(r"(\d{3,6})\s+(?:patients|participants|subjects|individuals)", text, re.I)
    if m_n and out:
        out[0]["n"] = int(m_n.group(1))
        out[0]["excerpt"] += " [n≈" + m_n.group(1) + " — 粗通道，人工核实]"
    return out


# ------------------------------------------------------------ 主流程 ------
def run_pipeline(query, ta, endpoint, retmax=20, offline_json=None):
    """检索 → 甄别 → 抽取。返回 (candidate_doc, records_kept, records_dropped)。"""
    if offline_json:
        with open(offline_json, encoding="utf-8") as f:
            records = json.load(f)
    else:
        pmids = search_pmids(query, retmax=retmax)
        if not pmids:
            return {"references": [], "_error": "esearch 无结果"}, [], []
        records = fetch_records(pmids)
    kept, dropped = [], []
    refs = []
    for rec in records:
        ok, sig = is_meta_analysis(rec)
        if not ok:
            dropped.append({"pmid": rec["pmid"], "title": rec["title"][:80], "signal": sig})
            continue
        rec["_ma_signal"] = sig
        kept.append(rec)
        text = (rec["title"] or "") + "\n" + (rec["abstract"] or "")
        refs.extend(extract_effects(text, rec))
    doc = {
        "_comment": _CANDIDATE_NOTE,
        "ta": ta, "endpoint": endpoint,
        "query": query, "as_of": date.today().isoformat(),
        "disclaimer": DISCLAIMER,
        "records_screened": len(records),
        "records_kept": len(kept),
        "references": refs,
    }
    return doc, kept, dropped


def render_sheet(doc, kept, dropped):
    """markdown 人工确认对照表。"""
    lines = ["# MA 效应量候选确认表", "",
             f"- 适应症 (ta): **{doc.get('ta') or '（未填）'}**",
             f"- 终点 (endpoint): **{doc.get('endpoint') or '（未填）'}**",
             f"- 检索式: `{doc.get('query')}` | as_of: {doc.get('as_of')}",
             f"- 筛选: {doc.get('records_screened')} 条 → MA 保留 {doc.get('records_kept')} 条",
             "", "> 人工核对每条候选（对照 excerpt；摘要没有的数值拉全文补录），",
             "> 将 candidates.json 中对应条目的 `verify` 改为 `ok`（或删除错误条目），",
             "> 再用 `--confirm` 入库。`scale=unknown` 条目必须人工补判类型。", ""]
    if kept:
        lines += ["## 保留的 MA 文献", ""]
        for rec in kept:
            lines.append(f"- **PMID {rec['pmid']}** ({rec.get('year','')}) {rec['title']} "
                         f"[signal: {rec.get('_ma_signal')}]")
        lines.append("")
    if dropped:
        lines += ["## 排除（非 MA）", ""]
        for d in dropped[:15]:
            lines.append(f"- {d['pmid']} {d['title']}… ({d['signal']})")
        lines.append("")
    lines += ["## 效应量候选", "",
              "| # | scale | est | 95%CI | n | verify | excerpt | source |",
              "|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(doc.get("references", []), 1):
        est = r.get("estimate")
        lines.append(
            f"| {i} | {r.get('scale')} | {est if est is not None else '—'} "
            f"| [{r.get('ci_low')}, {r.get('ci_high')}] "
            f"| {r.get('n') or '—'} | {r.get('verify')} "
            f"| {r.get('excerpt','')[:120]} | {r.get('source','')} |")
    return "\n".join(lines) + "\n"


def confirm(doc_path, into_path):
    """人工确认后的入库：仅收 verify=ok 的条目；目标文件存在则合并（按 pmid+scale+CI 去重）。

    入库闸门（2026-10-16）：ok 条目整体过 effect_ref.validate——param/scale 白名单、
    数值完整性、CI 与 estimate 关系、source 必填。任一条款不合格即拒绝写入
    （防止 estimate=None 的半成品或尺度笔误流入基准库）。
    """
    with open(doc_path, encoding="utf-8") as f:
        doc = json.load(f)
    ok_refs = [r for r in doc.get("references", []) if r.get("verify") == "ok"]
    unknown = [r for r in ok_refs if r.get("scale") == "unknown"]
    if unknown:
        print(f"[confirm] ✗ 存在 {len(unknown)} 条 scale=unknown 的 ok 条目，须先人工补判类型。",
              file=sys.stderr)
        sys.exit(1)
    if not ok_refs:
        print("[confirm] ✗ 没有 verify=ok 的条目，无事可入库。", file=sys.stderr)
        sys.exit(1)
    # 入库闸门：与 effect_ref 入库格式互认（param/scale/数值/source 全校验）
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        import effect_ref as _er
    except ImportError:
        import scripts.effect_ref as _er  # type: ignore
    _, gate_errors, _ = _er.validate({"references": ok_refs, "as_of": doc.get("as_of")})
    if gate_errors:
        print("[confirm] ✗ %d 条 ok 条目未通过 effect_ref 校验，拒绝入库：" % len(gate_errors),
              file=sys.stderr)
        for e in gate_errors:
            print("  ✗ " + e, file=sys.stderr)
        print("[confirm] 提示：补全 estimate/CI/source、核对 scale 与 param 对应后重试。",
              file=sys.stderr)
        sys.exit(1)
    for r in ok_refs:
        r.pop("excerpt", None)
        r.pop("verify", None)
    merged = {
        "ta": doc.get("ta"), "endpoint": doc.get("endpoint"),
        "as_of": doc.get("as_of"), "disclaimer": DISCLAIMER,
        "references": ok_refs,
    }
    if os.path.exists(into_path):
        with open(into_path, encoding="utf-8") as f:
            old = json.load(f)
        seen = {(r.get("pmid"), r.get("scale"), r.get("ci_low"), r.get("ci_high"))
                for r in old.get("references", [])}
        for r in ok_refs:
            key = (r.get("pmid"), r.get("scale"), r.get("ci_low"), r.get("ci_high"))
            if key not in seen:
                old["references"].append(r)
                seen.add(key)
        old["as_of"] = max(old.get("as_of") or "", doc.get("as_of") or "")
        merged = old
    with open(into_path, "w", encoding="utf-8", newline="") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"[confirm] 已入库 {len(merged['references'])} 条 -> {into_path}")
    print("[confirm] 提示：入库前请确保 ta/endpoint 与文件名一致；数值已经人工核实。")


def main():
    ap = argparse.ArgumentParser(description="MA 效应量候选抽取器（路线 C）")
    ap.add_argument("--query", help="PubMed 检索式（建议含 systematic review OR meta-analysis）")
    ap.add_argument("--ta", help="适应症（写入候选文档）")
    ap.add_argument("--endpoint", help="终点（写入候选文档）")
    ap.add_argument("--retmax", type=int, default=20, help="esearch retmax（默认 20）")
    ap.add_argument("--out", default="ma_candidates.json", help="候选 JSON 输出路径")
    ap.add_argument("--sheet", default=None, help="markdown 确认表输出路径（默认与 out 同名 .md）")
    ap.add_argument("--offline-records", default=None,
                    help="调试用：跳过网络，从 JSON 记录文件读（fetch_records 输出形状）")
    ap.add_argument("--confirm", metavar="CANDIDATES_JSON",
                    help="人工确认后的入库模式：读候选 JSON（verify=ok 条目）并入基准库")
    ap.add_argument("--into", default=None,
                    help="--confirm 目标基准库路径 references/effect_size_benchmarks/<ta>__<endpoint>.json")
    a = ap.parse_args()

    if a.confirm:
        if not a.into:
            print("[confirm] 必须同时给 --into <基准库文件路径>", file=sys.stderr)
            sys.exit(1)
        confirm(a.confirm, a.into)
        return

    if not a.query and not a.offline_records:
        ap.error("--query 必填（或 --offline-records 调试模式 / --confirm 入库模式）")
    doc, kept, dropped = run_pipeline(a.query, a.ta, a.endpoint,
                                      retmax=a.retmax, offline_json=a.offline_records)
    if doc.get("_error"):
        print("[extract] " + doc["_error"], file=sys.stderr)
        sys.exit(1)
    sheet_path = a.sheet or os.path.splitext(a.out)[0] + ".md"
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    with open(sheet_path, "w", encoding="utf-8", newline="") as f:
        f.write(render_sheet(doc, kept, dropped))
    print(f"[extract] 筛选 {doc['records_screened']} 条，MA 保留 {doc['records_kept']} 条，"
          f"候选效应量 {len(doc['references'])} 条")
    print(f"[extract] 候选 JSON -> {a.out}")
    print(f"[extract] 确认表   -> {sheet_path}")
    print("[extract] ⚠ 候选未经核实，绝不直接入库；人工对照 excerpt 核实后 --confirm。")


if __name__ == "__main__":
    main()
