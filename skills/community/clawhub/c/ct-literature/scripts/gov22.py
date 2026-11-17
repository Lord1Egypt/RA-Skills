#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gov22.py — ct-base §22 governance sections for ct-literature.

Implements the two RAG / synthesis governance obligations that ct-literature
must satisfy (ct-base/BASE.md §22, split doc docs/13-ai-generation-governance.md):

  §22.16 P1·h  RAG 三列待核对清单 (问题 / 原文位置 / 依据) + 显式「未覆盖项」
  §22.17 P2·a  确定性工具层 vs LLM 依赖输出 分层验收声明

Design constraints (ct-base AGENTS §2.1 function-first, §22 anti-hallucination):
  * PURE, deterministic, stdlib-only — same inputs always yield same output.
  * Takes explicit inputs (never reaches into global state) so the Markdown
    renderer (report.py) and the HTML renderer (export_html.py) stay in lock-step
    and never drift.
  * Derives every figure from the real run payload (evidence_log / config / works)
    — no fabricated counts. "漏项" (uncovered items) is the DEFAULT failure mode
    and is surfaced explicitly, never assumed complete (§22.16 + §17.1).

Skill version stamp (§22.5 processDefinitionVersion) lives here as the single
source and MUST be kept in sync with SKILL.md `version:`.
"""
# ── §22.5 processDefinitionVersion: single source of truth ──────────────────
# Keep in lock-step with SKILL.md `version:`; bump together on every release.
SKILL_VERSION = "1.4.12"

# Optional / opt-in / reserved sources and how they are enabled, used to derive
# 「未覆盖项」 when they were not part of this run.
_OPTIONAL_SOURCES = (
    ("Semantic Scholar", "opt-in via --with-semantic-scholar"),
    ("arXiv", "opt-in via --with-arxiv"),
    ("Cochrane CDSR", "opt-in via --cochrane (Europe PMC journal filter)"),
    ("PROSPERO", "reserved / dormant — no token, never claimed functional"),
)


def _lang(lang):
    if lang in ("zh", "zh-CN", "zh-cn"):
        return "zh"
    if lang in ("en", "auto"):
        return "en"
    return "zh" if (lang or "").lower().startswith("zh") else "en"


def _source_status(evidence_log):
    sources = (evidence_log or {}).get("sources") or []
    return [s for s in sources if isinstance(s, dict)]


def _coverage(evidence_log):
    return (evidence_log or {}).get("coverage") or "n/a"


def _concept_stats(evidence_log):
    cons = (evidence_log or {}).get("concepts") or []
    exact = sum(1 for c in cons if c.get("mapping_status") == "exact_label")
    syn = sum(1 for c in cons if c.get("mapping_status") == "synonym")
    unmapped = sum(1 for c in cons if c.get("mapping_status") == "unmapped_literal")
    return {"total": len(cons), "exact": exact, "synonym": syn, "unmapped": unmapped}


def build_uncovered(works, evidence_log, meta, lang="auto"):
    """§22.16 + §22.17 — explicit 「未覆盖项」 (uncovered items).

    Default failure mode per Waikar et al. 2026: a RAG answer that silently
    assumes completeness. We enumerate the gaps this run left open.
    Returns a list of {item, reason} (bilingual via lang).
    """
    L = _lang(lang)
    meta = meta or {}
    ev = evidence_log or {}
    srcs = _source_status(ev)
    attempted = {s.get("source") for s in srcs if s.get("status") in ("ok", "empty", "error")}
    skipped = [s for s in srcs if s.get("status") == "skipped"]
    errors = [s for s in srcs if s.get("status") == "error"]
    empties = [s for s in srcs if s.get("status") == "empty"]
    items = []

    T = {
        "zh": {
            "disabled": "已显式关闭（flag off，not_run）——该源未被检索",
            "optin_off": "未启用（%s）——本运行未检索该源",
            "error": "检索失败 / 降级（error）——该源证据缺口，结论不得外推至该源",
            "empty": "已检索但零命中（empty）——该源范围内未检出相关文献",
            "lang": "默认以英文为主书目 API（OpenAlex / Europe PMC / 预印本），非英文（尤其中文）文献覆盖有限；如需中文覆盖请明确说明",
            "year": "仅检索 %s–%s 范围；范围外文献未覆盖",
            "year_full": "未设年份窗口——全时段已检索，但更早/更晚的待刊文献可能未入库",
            "critical": "⚠️ 主源 OpenAlex 失败（critical_gap）——证据存在结构性缺口，任何结论均不得外推",
            "prospero": "PROSPERO 为保留源（token 门控，opt-in）——勾选 --with-prospero 时经 coze 端点检索系统综述注册库；未勾选则如实声明未检索",
        },
        "en": {
            "disabled": "explicitly turned OFF (flag off, not_run) — source not searched",
            "optin_off": "not enabled (%s) — source not searched in this run",
            "error": "fetch failed / degraded (error) — evidence gap for this source; do NOT extrapolate",
            "empty": "searched but zero hits (empty) — no relevant records within this source's scope",
            "lang": "defaults to English-first bibliographic APIs (OpenAlex / Europe PMC / preprints); non-English (esp. Chinese) coverage is limited — state explicitly if Chinese coverage is required",
            "year": "only the %s–%s window was searched; records outside this window are NOT covered",
            "year_full": "no year window set — full timeline searched, but not-yet-indexed forthcoming records may be missing",
            "critical": "⚠️ primary source OpenAlex failed (critical_gap) — structural evidence gap; no conclusion may be extrapolated",
            "prospero": "PROSPERO is a reserved (token-gated, opt-in) source — searched via the coze endpoint when --with-prospero is set; stated honestly when not selected",
        },
    }[L]

    # 1) explicitly disabled sources (status == skipped)
    for s in skipped:
        items.append({"item": s.get("source") or "—", "reason": T["disabled"]})
    # 2) optional / opt-in sources that were neither attempted nor skipped
    for name, how in _OPTIONAL_SOURCES:
        if name in attempted or any(s.get("source") == name for s in skipped):
            continue
        items.append({"item": name, "reason": T["optin_off"] % how})
    # 3) failed sources (error) — real gap, never zeroed
    for s in errors:
        items.append({"item": s.get("source") or "—", "reason": T["error"]})
    # 4) empty sources (searched, zero hits)
    for s in empties:
        items.append({"item": s.get("source") or "—", "reason": T["empty"]})
    # 5) language scope limitation (always a standing caveat for this skill)
    items.append({"item": "语种 / Language", "reason": T["lang"]})
    # 6) year window limitation
    yf = meta.get("year_from")
    yt = meta.get("year_to")
    if yf or yt:
        items.append({"item": "年份窗口 / Year window",
                      "reason": T["year"] % ("%s" % yf if yf else "…", "%s" % yt if yt else "…")})
    else:
        items.append({"item": "年份窗口 / Year window", "reason": T["year_full"]})
    # 7) critical gap — escalate the primary-source failure
    if _coverage(ev) == "critical_gap":
        items.append({"item": "主源缺口 / Primary-source gap", "reason": T["critical"]})
    return items


def build_rag_checklist(works, evidence_log, meta, lang="auto"):
    """§22.16 — three-column review checklist (问题 / 原文位置 / 依据).

    A RAG / synthesis answer MUST NOT be delivered as bare conclusions; the
    professional must be able to trace every point back to source. We build:
      * synthesis questions (landscape / study-type / safety / top-cited) mapped
        to the report section that answers them (原文位置) and the evidence basis
        (依据).
      * per-source coverage questions derived from the real source ledger.

    Returns a list of dicts: {q, location, basis, covered(bool), note}.
    """
    L = _lang(lang)
    meta = meta or {}
    ev = evidence_log or {}
    works = [w for w in (works or []) if isinstance(w, dict)]
    n = len(works)
    srcs = _source_status(ev)
    safety = [w for w in works if w.get("is_safety")]
    top_cited = max((w.get("cited_by_count") or 0) for w in works) if works else 0
    coverage = _coverage(ev)
    topic = meta.get("topic") or (ev.get("topic") or "—")

    if L == "zh":
        synth = [
            ("该主题的发表证据整体规模与年度趋势？",
             "概览 KPI + 「年度趋势」分布表",
             "六源合并 + 去重结果（coverage=%s）；共 %d 篇唯一文献" % (coverage, n),
             n > 0),
            ("研究类型分布如何（RCT / 系统评价 / 观察性 / 病例报告）？",
             "「研究类型分布」表",
             "study_type 归一化字段逐篇归类",
             n > 0),
            ("安全性 / CSM 定性证据有哪些？",
             "「安全性 / CSM 子集」（仅 --safety 或 is_safety 标记命中）",
             "is_safety 标记（AE / 毒性 / 病例报告 / PV）",
             len(safety) > 0),
            ("高影响力关键文献（被引最高）是哪些？",
             "「按被引排序的 Top 文献」表",
             "cited_by_count 降序；最高 %d 次" % top_cited,
             top_cited > 0),
        ]
    else:
        synth = [
            ("Overall publication volume and yearly trend for this topic?",
             "Overview KPIs + 'Yearly trend' distribution",
             "six-source merge + de-duplication (coverage=%s); %d unique works" % (coverage, n),
             n > 0),
            ("What is the study-type distribution (RCT / systematic review / observational / case report)?",
             "'Study-type distribution' table",
             "per-work study_type normalisation",
             n > 0),
            ("What qualitative safety / CSM evidence exists?",
             "'Safety / CSM subset' (only under --safety or is_safety hits)",
             "is_safety flag (AE / toxicity / case report / PV)",
             len(safety) > 0),
            ("Which are the high-impact key works (most cited)?",
             "'Top works by citations' table",
             "cited_by_count desc; top = %d" % top_cited,
             top_cited > 0),
        ]

    rows = []
    for q, loc, basis, covered in synth:
        rows.append({"q": q, "location": loc, "basis": basis,
                     "covered": covered, "note": "" if covered else "未覆盖 / NOT covered"})

    # per-source coverage questions (only attempted / skipped / errored sources)
    for s in srcs:
        name = s.get("source") or "—"
        status = s.get("status")
        q = ("是否从 %s 检索到「%s」相关文献？" % (name, topic)) if L == "zh" \
            else ("Were '%s'-related records retrieved from %s?" % (topic, name))
        cnt = s.get("count", 0) or 0
        qy = (s.get("query") or "")[:90]
        if status == "ok" and cnt > 0:
            # 原文位置 = first work whose source matches (best-effort DOI)
            doi = "—"
            for w in works:
                if name in (w.get("sources") or [w.get("source")]):
                    doi = w.get("doi") or w.get("url") or "—"
                    break
            loc = ("见来源=%s 的 %d 篇（示例 %s）" % (name, cnt, doi)) if L == "zh" \
                  else ("see %d works under source=%s (e.g. %s)" % (cnt, name, doi))
            covered = True
            note = ""
        elif status == "skipped":
            loc = "—"
            covered = False
            note = "未检索（关闭）/ not_run" if L == "zh" else "not searched (off) / not_run"
        elif status == "error":
            loc = "—"
            covered = False
            note = "检索失败 / fetch error"
        else:  # empty
            loc = "—"
            covered = False
            note = "已检索零命中 / searched, zero hits"
        rows.append({"q": q, "location": loc,
                     "basis": ("检索式: %s" % qy) if L == "zh" else ("query: %s" % qy),
                     "covered": covered, "note": note})
    return rows


def build_layer_acceptance(works, evidence_log, meta, lang="auto"):
    """§22.17 — stratified acceptance: deterministic tool layer vs LLM-dependent output.

    Two layers are reported SEPARATELY (never merged into one 'overall accuracy').
    Returns a dict with both layer blocks + their metrics.
    """
    L = _lang(lang)
    meta = meta or {}
    ev = evidence_log or {}
    works = [w for w in (works or []) if isinstance(w, dict)]
    srcs = _source_status(ev)
    attempted = [s for s in srcs if s.get("status") in ("ok", "empty", "error")]
    ok_n = sum(1 for s in attempted if s.get("status") == "ok")
    err_n = sum(1 for s in attempted if s.get("status") == "error")
    skip_n = sum(1 for s in srcs if s.get("status") == "skipped")
    raw_total = sum((s.get("count") or 0) for s in attempted)
    unique = len(works)
    dedup = max(0, raw_total - unique)
    cov = _coverage(ev)
    cstat = _concept_stats(ev)
    yf = meta.get("year_from")
    yt = meta.get("year_to")
    date_applied = bool(yf or yt)
    safety = bool(meta.get("safety"))

    if L == "zh":
        deterministic = {
            "title": "确定性工具层（可独立验收 · 可入 CM0）",
            "components": [
                "六源检索（OpenAlex / Europe PMC / 预印本 / 可选 arXiv·S2·Cochrane）",
                "日期窗口过滤（%s）" % ("已原生下推 + 客户端裁剪" if date_applied else "未设年份窗口"),
                "合并 + 跨源去重（去重 %d 条，raw=%d → unique=%d）" % (dedup, raw_total, unique),
            ],
            "metrics": "数据源：attempted=%d · 成功(ok)=%d · 失败(error)=%d · 跳过(skipped)=%d；"
                       "覆盖判定 coverage=%s。上述为确定性执行结果，可逐字节复现。" % (
                           len(attempted), ok_n, err_n, skip_n, cov),
            "accept": "确定性层可独立验收、可入 CM0；本运行 coverage=%s，去重 %d 条。" % (cov, dedup),
        }
        # LLM layer — ct-literature's LLM touchpoints are bounded (normalisation /
        # translation / tagging), it NEVER authors evidence conclusions.
        llm_components = [
            "主题中英翻译（topic_translator）",
            "MeSH / 概念归一化（mesh_mapper / kw_localize）",
            "安全性标记（is_safety 启发式标注）",
            "摘要片段处理（abstract_snippet 截断/段落还原）",
        ]
        llm = {
            "title": "LLM 依赖输出层（禁入 CM4 · 复杂域须人工复核）",
            "components": llm_components,
            "metrics": "概念归一化准确率（按映射状态分层，不混报）：total=%d · exact_label=%d · "
                       "synonym=%d · unmapped_literal=%d。未覆盖/未映射概念须人工复核，不得静默通过。" % (
                           cstat["total"], cstat["exact"], cstat["synonym"], cstat["unmapped"]),
            "accept": "LLM 层仅在归一化/翻译/标注环节介入，不生成证据结论、不撰写综述正文；"
                      "安全性定性归类属复杂域，建议人工复核。两层准确率分开声明，"
                      "严禁用「总体 X% 准」掩盖「复杂域 <55%」。"
                      + ("（本运行含 --safety，安全性子集为定性输出，仅佐证 ct-safety，不得喂入 FAERS）"
                         if safety else ""),
        }
    else:
        deterministic = {
            "title": "Deterministic tool layer (independently verifiable · CM0-eligible)",
            "components": [
                "six-source fetch (OpenAlex / Europe PMC / preprints / optional arXiv·S2·Cochrane)",
                "date-window filter (%s)" % ("native push-down + client clip" if date_applied else "no year window set"),
                "merge + cross-source de-duplication (dedup %d, raw=%d → unique=%d)" % (dedup, raw_total, unique),
            ],
            "metrics": "sources: attempted=%d · ok=%d · error=%d · skipped=%d; "
                       "coverage verdict=%s. Deterministic, byte-for-byte reproducible." % (
                           len(attempted), ok_n, err_n, skip_n, cov),
            "accept": "Deterministic layer is independently verifiable and CM0-eligible; "
                      "this run coverage=%s, dedup %d." % (cov, dedup),
        }
        llm_components = [
            "topic EN↔ZH translation (topic_translator)",
            "MeSH / concept normalisation (mesh_mapper / kw_localize)",
            "safety flagging (is_safety heuristic)",
            "abstract-snippet processing (truncation / paragraph restore)",
        ]
        llm = {
            "title": "LLM-dependent output layer (CM4-forbidden · complex domains need human review)",
            "components": llm_components,
            "metrics": "concept-normalisation accuracy (stratified by mapping status, not merged): "
                       "total=%d · exact_label=%d · synonym=%d · unmapped_literal=%d. "
                       "Unmapped concepts require human review; silent pass is forbidden." % (
                           cstat["total"], cstat["exact"], cstat["synonym"], cstat["unmapped"]),
            "accept": "The LLM layer only intervenes in normalisation / translation / tagging — "
                      "it does NOT author evidence conclusions or write review prose; safety "
                      "qualitative tagging is a complex domain and warrants human review. The two "
                      "layers are reported separately; a single 'overall X% accurate' figure that "
                      "hides '<55% in complex domains' is explicitly forbidden."
                      + (" (this run used --safety: the safety subset is qualitative only and "
                         "corroborates ct-safety, never feed it into FAERS)"
                         if safety else ""),
        }
    return {"deterministic": deterministic, "llm": llm,
            "metrics": {"attempted": len(attempted), "ok": ok_n, "error": err_n,
                        "skipped": skip_n, "raw_total": raw_total, "unique": unique,
                        "dedup": dedup, "coverage": cov, "concepts": cstat}}


def build_gov22(works, evidence_log, meta, lang="auto"):
    """Single entry point used by both renderers."""
    return {
        "version": SKILL_VERSION,
        "uncovered": build_uncovered(works, evidence_log, meta, lang),
        "checklist": build_rag_checklist(works, evidence_log, meta, lang),
        "layers": build_layer_acceptance(works, evidence_log, meta, lang),
        "coverage": _coverage(evidence_log),
        "has_run": bool(evidence_log),
    }
