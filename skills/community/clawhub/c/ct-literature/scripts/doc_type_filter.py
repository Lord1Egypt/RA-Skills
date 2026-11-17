#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc_type_filter.py — 文献类型甄别（review / guideline / protocol / original）。

移植自 meta-analysis 技能 pdf_extractor.classify_pdf 的实证规则（v2，33 篇
真实 PDF 全量回归 33/33 正确、无一误判）。用于用户检索时明确「只要论文
（original research），不要综述 / 指南·共识 / 研究方案」的场景。

双层甄别（按成本从低到高）：
  A. 元数据级 classify_record(title, abstract, pub_types)
     — 检索阶段即可用（OpenAlex / Europe PMC 记录），零额外网络；
       Europe PMC 的 pubType 元数据是最强通道（权威文章类型）。
  B. PDF 级 classify_pdf(pdf_path)
     — 下载后兜底（需要 PyMuPDF/fitz）；四级信号：独立成行 article-type
       标签(权重 100) > 声明短语(head 4/命中) > 标题词(2/命中) >
       自指信号(全文 2/命中, 封顶 6)。全文裸关键词不参与（双向误判实证）。

规律 R3（来自 meta-analysis 实证）：信号分层次、强信号压倒弱信号；
探测失败绝不阻断正常流程——classify 异常时一律返回 unknown 并放行。

用法（独立 CLI，作用于 .merged.json）：
  python doc_type_filter.py --in .merged.json            # 标注 doc_type
  python doc_type_filter.py --in m.json --exclude-non-original
                                                         # 排除 review/guideline/protocol
也可作为库：
  from doc_type_filter import classify_record, classify_pdf, filter_records
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---- 类型甄别信号（对齐 meta-analysis/adapters/pdf_extractor.py v2 实证规则）----

# PDF 独立成行的 article-type 标签（期刊把 "Review" / "Article" 单独成行印在
# 刊名下方，如 enm-2026-3080 的 "Review\nArticle"；标题里的 "Guidelines" 不算）
_STANDALONE_TYPE = [
    (r"(?m)^\s*(systematic\s+)?review\s*$", "review"),
    (r"(?m)^\s*meta[- ]?analysis\s*$", "review"),
    (r"(?m)^\s*guideline\s*$", "guideline"),
    (r"(?m)^\s*consensus\s+statement\s*$", "guideline"),
    (r"(?m)^\s*(study|trial)\s+protocol\s*$", "protocol"),
    (r"(?m)^\s*protocol\s*$", "protocol"),
    (r"(?m)^\s*original\s+(article|research)\s*$", "original"),
    (r"(?m)^\s*research\s+article\s*$", "original"),
]
# 声明短语（head 区：标题 + 摘要开头）
_DECLARED_TYPE = [
    (r"review article|literature review|systematic review|meta[- ]?analysis|"
     r"umbrella review|scoping review|narrative review", "review"),
    (r"clinical practice guideline|practice guideline|"
     r"consensus (statement|conference|report)|position statement|"
     r"presidential advisory|expert (consensus|panel)|focus on \w+ (guidelines|guidance)",
     "guideline"),
    (r"study protocol|trial protocol|protocol (for a|of the|paper)|"
     r"protocol article|rationale and (design|protocol)|"
     r"design and rationale( of| for)", "protocol"),
    (r"original article|original research|research article|target trial emulation|"
     r"randomized(,? double[- ]blind)?[, ]*(controlled )?trial\b", "original"),
]
# 自指信号（全文/摘要：论文「本身就是」该类型的强证据，非引用）
_REVIEW_SELF = [
    r"our (systematic )?review", r"this (systematic |narrative )?review",
    r"in this review", r"we (systematically )?(searched|reviewed|screened)",
    r"\bprisma\b", r"we included \d+ (studies|trials|articles)",
    r"prospectively registered", r"(studies|trials) (were )?(included|eligible)",
    r"search strategy", r"(medline|pubmed|embase)[^.]{0,60}(searched|queried)",
]
_GUIDELINE_SELF = [
    r"we recommend", r"the (task force|panel|committee|writing group|work group) recommend",
    r"these (guidelines|recommendations)", r"we suggest",
    r"class (i{1,3}|iv)\b.{0,40}level of evidence",
    r"level of evidence|grade of recommendation",
    r"recommendations? (for|are|were|on)\b",
]
_ORIG_SELF = [
    r"we (enrolled|randomly assigned|prospectively (enrolled|assigned)|conducted)",
    r"we (designed|performed|carried out) (a|an|this) (study|trial|analysis)",
    r"patients? (were )?randomly assigned", r"inclusion criteria",
    r"baseline characteristics", r"we analyzed", r"intention[- ]to[- ]treat",
    r"primary (outcome|endpoint) (was|were)",
]
_REVIEW_HEAD = [r"\breview\b", r"systematic review", r"meta[- ]?analysis",
                r"\bsummary\b", r"advances? in", r"progress in", r"update on"]
_GUIDELINE_HEAD = [r"\bguideline", r"recommendation", r"consensus", r"advisory"]
_ORIG_HEAD = [r"effect of", r"efficacy (and safety )?of", r"association of",
              r"trial\b", r"original (article|research)", r"target trial"]

# Europe PMC / PubMed-style pubType → 类型（权威文章类型，最强元数据通道）
_PUBTYPE_MAP = [
    (r"systematic review|meta[- ]?analysis|review\b(?!ed)|scoping review|"
     r"bibliography|comparative study\b.*review", "review"),
    (r"practice guideline|guideline|consensus development conference|"
     r"position statement|practice advisory", "guideline"),
    (r"clinical trial protocol|protocol\b", "protocol"),
    (r"randomized controlled trial|controlled clinical trial|clinical trial\b|"
     r"multicenter study|observational study|comparative study|"
     r"journal article\b", "original"),
]
_NON_ORIGINAL = {"review", "guideline", "protocol"}


def _hits(pats, s):
    return sum(1 for p in pats if re.search(p, s))


def _pubtype_signal(pub_types):
    """pubType 列表 → (declared_type, signal)；冲突时非 original 优先（保守排除）。

    容忍 CamelCase 标签（S2/Coze 端返回 "JournalArticle"/"SystematicReview"）：
    先在小写→大写边界插空格再匹配（与 fetch_semantic_scholar._camel_to_words 同理）。
    """
    found = []
    for pt in (pub_types or []):
        low = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", str(pt)).lower()
        for pat, t in _PUBTYPE_MAP:
            if re.search(pat, low):
                found.append(t)
                break
    if not found:
        return "", ""
    if any(t in _NON_ORIGINAL for t in found):
        # 优先返回排除类（e.g. ["Journal Article", "Review"] → review）
        for t in ("guideline", "protocol", "review"):
            if t in found:
                return t, "pubtype:" + ";".join(str(p) for p in pub_types)
    if "original" in found:
        return "original", "pubtype:" + ";".join(str(p) for p in pub_types)
    return "", ""


def classify_record(title, abstract, pub_types=None, head_chars=3500):
    """元数据级甄别（检索阶段，零额外网络）。

    返回 {"type": original|review|guideline|protocol|unknown,
          "confidence": float, "declared": str, "signals": [...]}。
    head 区 = 标题 + 摘要开头；pubType 元数据是独立强通道（±100）。
    """
    head = ((title or "") + "\n" + (abstract or "")[:2000]).strip()
    signals, declared = [], ""
    # ① pubType 元数据（最强，±100）
    pt_type, pt_sig = _pubtype_signal(pub_types)
    # ② 声明短语
    head_low = head.lower()
    for pat, t in _DECLARED_TYPE:
        if re.search(pat, head_low):
            declared = t
            signals.append("declared: " + pat[:40])
            break

    def score():
        s_rev = _hits(_REVIEW_HEAD, head_low) * 2 + min(_hits(_REVIEW_SELF, head_low), 3) * 2
        s_gdl = _hits(_GUIDELINE_HEAD, head_low) * 2 + min(_hits(_GUIDELINE_SELF, head_low), 3) * 2
        s_org = _hits(_ORIG_HEAD, head_low) * 2 + min(_hits(_ORIG_SELF, head_low), 3) * 2
        s_prt = 0
        if re.search(r"study protocol|trial protocol|protocol (for a|of the)|"
                     r"this protocol|will be (recruited|enrolled|randomised|randomized|"
                     r"reported|estimated|compared|analysed|analyzed)|"
                     r"ethics (approval|and dissemination)", head_low):
            s_prt = 4 if re.search(r"protocol", head_low) else 2
        if declared == "review":
            s_rev += 100
        elif declared == "guideline":
            s_gdl += 100
        elif declared == "protocol":
            s_prt += 100
        elif declared == "original":
            s_org += 100
        if pt_type:
            if pt_type == "original":
                s_org += 100
            else:
                s_rev += 100 if pt_type == "review" else 0
                s_gdl += 100 if pt_type == "guideline" else 0
                s_prt += 100 if pt_type == "protocol" else 0
        return {"review": s_rev, "guideline": s_gdl, "original": s_org, "protocol": s_prt}

    scores = score()
    total = sum(scores.values())
    if total == 0:
        return {"type": "unknown", "confidence": 0.0, "declared": declared,
                "signals": signals or ["no-signal"]}
    if pt_sig:
        signals.append(pt_sig)
    best = max(scores, key=scores.get)
    conf = scores[best] / total
    # 平票防误判（实证：protocol 被平票误判 guideline）——分差不足 20% 时降为 unknown
    other = max(v for k, v in scores.items() if k != best) if any(
        k != best for k in scores) else 0
    if scores[best] - other < 0.2 * total:
        return {"type": "unknown", "confidence": conf, "declared": declared,
                "signals": signals + ["near-tie"]}
    return {"type": best, "confidence": conf, "declared": declared, "signals": signals}


def classify_pdf(pdf_path, head_chars=3500):
    """PDF 级甄别（下载后兜底，需 fitz；失败一律 unknown 不阻断流程）。"""
    try:
        import fitz
    except ImportError:
        return {"type": "unknown", "confidence": 0.0, "declared": "",
                "signals": ["fitz-unavailable"]}
    try:
        with fitz.open(pdf_path) as doc:
            n_pages = len(doc)
            text = "\n".join(doc[i].get_text() or "" for i in range(min(3, n_pages)))
            if n_pages > 3:
                text += "\n" + "\n".join(
                    doc[i].get_text() or "" for i in range(3, min(n_pages, 40)))
    except Exception as e:  # noqa: BLE001
        return {"type": "unknown", "confidence": 0.0, "declared": "",
                "signals": ["open-fail: %s" % e]}
    head = text[:head_chars]
    head_low, text_low = head.lower(), text.lower()
    signals, declared = [], ""

    # 1) 独立成行 article-type 标签（最强）
    for pat, t in _STANDALONE_TYPE:
        if re.search(pat, head_low):
            declared = t
            signals.append("standalone-label: " + pat)
            break
    # 2) 声明短语
    if not declared:
        for pat, t in _DECLARED_TYPE:
            if re.search(pat, head_low):
                declared = t
                signals.append("declared: " + pat[:40])
                break
    # 3) 计分（同 meta-analysis 实证权重）
    s_rev = _hits(_REVIEW_HEAD, head_low) * 2 + min(_hits(_REVIEW_SELF, text_low), 3) * 2
    s_gdl = _hits(_GUIDELINE_HEAD, head_low) * 2 + min(_hits(_GUIDELINE_SELF, text_low), 3) * 2
    s_org = _hits(_ORIG_HEAD, head_low) * 2 + min(_hits(_ORIG_SELF, text_low), 3) * 2
    s_prt = 0
    if re.search(r"study protocol|trial protocol|protocol (for a|of the)|"
                 r"this protocol|will be (recruited|enrolled|randomised|randomized|"
                 r"reported|estimated|compared|analysed|analyzed)|"
                 r"ethics (approval|and dissemination)", text_low):
        s_prt = 4 if re.search(r"protocol", head_low) else 2
    if declared == "review":
        s_rev += 100
    elif declared == "guideline":
        s_gdl += 100
    elif declared == "protocol":
        s_prt += 100
    elif declared == "original":
        s_org += 100
    scores = {"review": s_rev, "guideline": s_gdl, "original": s_org, "protocol": s_prt}
    total = sum(scores.values())
    if total == 0:
        return {"type": "unknown", "confidence": 0.0, "declared": declared,
                "signals": signals or ["no-signal"]}
    best = max(scores, key=scores.get)
    return {"type": best, "confidence": scores[best] / total,
            "declared": declared, "signals": signals}


def filter_records(works, exclude=("review", "guideline", "protocol"),
                   require=None, annotate=True, use_pdfs=False, pdf_dir=None):
    """批量过滤 .merged.json 的 works 列表。

    两种模式（同时给出时 require 优先）：
    - exclude 集合内的类型被排除（默认排除 review/guideline/protocol，即只要 original）；
      unknown 一律放行（宁缺勿误）。
    - require 非空时反向：只保留 require 集合内的类型；unknown 也被排除
      （用户点名要某类时，无信号记录不应混入）。

    - use_pdfs=True 时对已有本地 PDF（pdf_dir 或 work["pdf_path"]）追加 PDF 级
      兜底甄别（仅对 metadata=original 或 unknown 的记录，节省开销）。
    - annotate=True 时写入 doc_type / doc_type_confidence / doc_type_signals /
      doc_type_excluded 字段。
    返回 (works, stats)。
    """
    exclude = set(exclude)
    require = set(require) if require else None
    stats = {"total": 0, "excluded": 0, "by_type": {}}
    out = []
    for w in works:
        if not isinstance(w, dict):
            out.append(w)
            continue
        stats["total"] += 1
        rec = dict(w)
        cls = classify_record(w.get("title") or "", w.get("abstract_snippet") or "",
                              w.get("pub_types"))
        # PDF 兜底：仅当元数据不是明确 original 时
        if use_pdfs and cls["type"] in ("unknown", "original"):
            pp = (w.get("pdf_path")
                  or (os.path.join(pdf_dir, w.get("doi_filename") or "") if pdf_dir else ""))
            if pp and os.path.isfile(pp):
                cls_pdf = classify_pdf(pp)
                if cls_pdf["type"] != "unknown" or cls["type"] == "unknown":
                    cls = cls_pdf
        if require is not None:
            excluded = cls["type"] not in require
        else:
            excluded = cls["type"] in exclude
        if excluded:
            stats["excluded"] += 1
            stats["by_type"][cls["type"]] = stats["by_type"].get(cls["type"], 0) + 1
        if annotate:
            rec["doc_type"] = cls["type"]
            rec["doc_type_confidence"] = cls["confidence"]
            rec["doc_type_signals"] = cls["signals"]
            rec["doc_type_excluded"] = excluded
        out.append(rec)
    return out, stats


def main():
    ap = argparse.ArgumentParser(
        description="Doc-type filter (review/guideline/protocol vs original).")
    ap.add_argument("--in", default=".merged.json", dest="inp")
    ap.add_argument("--out", help="output path (default: overwrite --in)")
    ap.add_argument("--exclude-non-original", action="store_true",
                    help="exclude review/guideline/protocol records")
    ap.add_argument("--only", dest="only", default=None,
                    metavar="TYPES",
                    help="只保留指定类型，逗号分隔：original/review/guideline/protocol"
                         "（反向模式：unknown 也被排除）。"
                         "例：--only review 或 --only guideline,protocol")
    ap.add_argument("--use-pdfs", action="store_true",
                    help="run PDF-level screening as fallback for local PDFs")
    ap.add_argument("--pdf-dir", default=None)
    args = ap.parse_args()

    data = json.load(open(args.inp, encoding="utf-8"))
    works = data.get("works", [])
    if args.only:
        require = [t.strip().lower() for t in args.only.split(",") if t.strip()]
        bad = [t for t in require if t not in ("original", "review", "guideline", "protocol")]
        if bad:
            ap.error("unknown type(s): %s (valid: original, review, guideline, protocol)" % bad)
        works, stats = filter_records(works, require=require, use_pdfs=args.use_pdfs,
                                      pdf_dir=args.pdf_dir)
        data["works"] = works
        if "count" in data:
            data["count"] = len(works)
        print("[OK] require-only %s: total=%d kept=%d excluded=%d by_type=%s" % (
            require, stats["total"], stats["total"] - stats["excluded"],
            stats["excluded"], stats["by_type"]))
    elif args.exclude_non_original:
        works, stats = filter_records(works, use_pdfs=args.use_pdfs,
                                      pdf_dir=args.pdf_dir)
        data["works"] = works
        if "count" in data:
            data["count"] = len(works)
        print("[OK] doc-type filter: total=%d excluded=%d by_type=%s" % (
            stats["total"], stats["excluded"], stats["by_type"]))
    else:
        works, stats = filter_records(works, exclude=(), use_pdfs=args.use_pdfs,
                                      pdf_dir=args.pdf_dir)
        data["works"] = works
        print("[OK] annotated doc_type only: total=%d by_type=%s" % (
            stats["total"], {w.get("doc_type", "?") for w in works if isinstance(w, dict)}))

    out_path = args.out or args.inp
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("-> %s" % out_path)


if __name__ == "__main__":
    main()
