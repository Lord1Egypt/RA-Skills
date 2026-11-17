#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""export_xlsx.py - Export a ct-literature ``.merged.json`` to a multi-sheet Excel
workbook (green theme, ct-base ``excel_style`` shared standard).

Sheets (names localized):
  1. README             - cover banner + KPI cards (count / safety / top-cited / span)
                          + search scope + field dictionary + data caveats
  2. Overview           - distribution blocks (year col chart; source/type/study_type
                          pies) + top-cited list; charts floated right (col E), no overlap
  3. Works              - unified literature table; title hyperlinked to DOI
                          (url fallback; the standalone Link column was removed
                          2026-09-04); safety-relevant rows highlighted amber
  4. Safety-Related     - filtered subset where is_safety is true

Rendering standard: scripts/excel_style.py (vendored from ct-base/scripts/excel_style.py)
  - header row height 24px (HEADER_H)
  - per-cell zebra striping (light green + grey grid border)
  - safety-relevant rows highlighted with warn_bg
  - cover logo pinned top-right (icon_4x.png, scale 0.16)
  - native .xlsx charts (no web page)
"""

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime

import xlsxwriter

# ═══════════════════════════════════════════════════════════════════════════
# import the shared excel rendering standard (vendored from ct-base)
# IMPORTANT (2026-08-11): ct-base is NEVER published. Every ct- skill must carry
# its own complete copy. We ONLY import from this skill's own `scripts/` dir.
# ═══════════════════════════════════════════════════════════════════════════
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
try:
    from excel_style import (
        make_formats, banner as _banner, page_decor as _page_decor,
        kpi_card as _kpi_card, cover_logo, PALETTES, FONT, HEADER_H,
        add_chart as _add_chart, chart_h as _chart_h, chart_w as _chart_w,
        dist_pie_points as _dist_pie_points, ROW_PX, BAND_GAP,
    )
except Exception as _e:  # pragma: no cover — vendored copy must be present
    raise RuntimeError("ct-literature export_xlsx: cannot import vendored "
                       "excel_style: " + str(_e))

P = PALETTES["literature"]
NAVY, BLUE, LIGHT = P["navy"], P["blue"], P["light"]
GRID, GREYTX = P["grid"], P["greytx"]
BANNER = P["banner"]

# distinct but on-brand fills for the source pie (so slices read clearly)
_SOURCE_COLOR = {
    "OpenAlex": "#2E7D4F",        # literature navy-green
    "EuropePMC": "#2E75B6",       # registry blue (clearly distinct)
    "SemanticScholar": "#BF9000", # amber (clearly distinct)
}
CHART_COL = "E"  # right-side anchor column for all overview charts (no overlap)


# ═══════════════════════════════════════════════════════════════════════════
# i18n — reuse vendored i18n; skill-specific labels live in _LOCAL.
# ═══════════════════════════════════════════════════════════════════════════
try:
    from i18n import (t as _base_t, set_lang as _base_set_lang,
                     is_chinese_os as _base_is_chinese_os)
except Exception:  # pragma: no cover
    _base_t = lambda k, **kw: k
    def _base_set_lang(c):
        pass
    def _base_is_chinese_os():
        return False

_LANG = "en"
_LOCAL = {
    "sheet.readme":    {"en": "README", "zh": "说明"},
    "sheet.works":     {"en": "Works", "zh": "文献总表"},
    "sheet.overview":  {"en": "Overview", "zh": "概览"},
    "sheet.safety":    {"en": "Safety-Related", "zh": "安全性相关"},
    "doc.title":       {"en": "Literature Evidence Base", "zh": "文献证据库"},
    "banner.title":    {"en": "Systematic Literature Review", "zh": "系统文献综述"},
    "kpi.count":       {"en": "Publications", "zh": "文献总数"},
    "kpi.count_sub":   {"en": "deduplicated", "zh": "已去重"},
    "kpi.safety":      {"en": "Safety-related", "zh": "安全性相关"},
    "kpi.safety_sub":  {"en": "is_safety flag", "zh": "安全性标记"},
    "kpi.cited":       {"en": "Top cited", "zh": "最高被引"},
    "kpi.cited_sub":   {"en": "citations", "zh": "次引用"},
    "kpi.span":        {"en": "Year span", "zh": "年份跨度"},
    "kpi.span_sub":    {"en": "publication years", "zh": "发表年份范围"},
    "prov.generated":  {"en": "Generated", "zh": "生成时间"},
    "prov.source":     {"en": "Sources", "zh": "数据来源"},
    "col.source":      {"en": "Source", "zh": "来源"},
    "col.doi":         {"en": "DOI", "zh": "DOI"},
    "col.oa_flag":     {"en": "OA", "zh": "开放获取"},
    "col.year":        {"en": "Year", "zh": "年份"},
    "col.title":       {"en": "Title", "zh": "标题"},
    "col.authors":     {"en": "Authors", "zh": "作者"},
    "col.publication": {"en": "Journal", "zh": "期刊"},
    "col.type":        {"en": "Type", "zh": "类型"},
    "col.study_type":  {"en": "Study type", "zh": "研究类型"},
    "col.cited":       {"en": "Cited by", "zh": "被引"},
    "col.relevance":       {"en": "Relevance", "zh": "相关性"},
    "col.relevance_basis": {"en": "Relevance basis", "zh": "相关性依据"},
    "col.is_safety":   {"en": "Safety", "zh": "安全性"},
    "col.decision":    {"en": "Decision", "zh": "裁决"},
    "col.reason":      {"en": "Reason", "zh": "理由"},
    # 附加决策列（decision_extra）：人工确认的文献类型，下游只读不再判定。
    # 与 col.type（元数据原始类型，只读）分列，避免"确认值"与"库方标注"混为一谈。
    "col.doc_type_confirmed": {"en": "Confirmed type", "zh": "文献类型确认"},
    "col.oa":          {"en": "OA link", "zh": "OA链接"},
    "col.abstract":    {"en": "Abstract", "zh": "摘要"},
    "col.pdf_path":    {"en": "PDF Path", "zh": "PDF 本地路径"},
    "col.pdf_size_kb": {"en": "Size (KB)", "zh": "大小KB"},
    "col.pdf_pages":   {"en": "Pages", "zh": "页数"},
    "col.mesh":        {"en": "MeSH", "zh": "MeSH"},
    "col.funders":     {"en": "Funders", "zh": "资助方"},
    "col.count":       {"en": "Count", "zh": "数量"},
    "col.share":       {"en": "Share", "zh": "占比"},
    "col.unknown":     {"en": "(unknown)", "zh": "(未知)"},
    "col.topic":       {"en": "Topic", "zh": "主题"},
    "ov.year":         {"en": "Publications by year", "zh": "逐年文献分布"},
    "ov.source":       {"en": "By source", "zh": "按来源分布"},
    "ov.type":         {"en": "By type", "zh": "按类型分布"},
    "ov.stype":        {"en": "By study type", "zh": "按研究类型分布"},
    "ov.top":          {"en": "Most cited", "zh": "高被引文献"},
    "ov.total":        {"en": "Total", "zh": "合计"},
    "ov.banner":       {"en": "Literature Search Summary", "zh": "文献检索结果概要"},
    "ov.intro":        {"en": "Distribution tables and charts below are auto-summarised from the search results: each block shows the data table on the left and the corresponding chart on the right.",
                       "zh": "下列数据表与图表由检索结果自动汇总生成：每个区块左侧为分布数据表、右侧为对应统计图。"},
    # ---- README scope (search overview) ----
    "scope.title":     {"en": "Search scope", "zh": "检索概览"},
    "scope.topic":     {"en": "Topic", "zh": "检索主题"},
    "scope.keywords":  {"en": "Generated keywords", "zh": "生成关键字"},
    "scope.filter":    {"en": "Filter", "zh": "检索范围"},
    "scope.source":    {"en": "Sources", "zh": "数据来源"},
    "scope.year":      {"en": "Year range", "zh": "时间范围"},
    # ---- field dictionary (field meanings) ----
    "field.title":     {"en": "Field dictionary", "zh": "字段说明"},
    "field.col":       {"en": "Field", "zh": "字段"},
    "field.mean":      {"en": "Meaning", "zh": "含义"},
    "f.source":        {"en": "Source repository (OpenAlex / Europe PMC / Semantic Scholar)",
                       "zh": "文献来源库（OpenAlex / Europe PMC / Semantic Scholar）"},
    "f.title":         {"en": "Work title (hyperlinked to its DOI — click to open)",
                        "zh": "文献标题（已超链接至 DOI，点击可访问）"},
    "f.authors":       {"en": "Author list (first 6)", "zh": "作者列表（前 6 位）"},
    "f.year":          {"en": "Publication year", "zh": "发表年份"},
    "f.publication":   {"en": "Journal / venue", "zh": "发表期刊 / 会议"},
    "f.type":          {"en": "Work type (article, etc.)", "zh": "文献类型（article 等）"},
    "f.study_type":    {"en": "Study type (RCT / review / case-report …)", "zh": "研究类型（RCT / 综述 / 病例报告 等）"},
    "f.cited":         {"en": "Citation count", "zh": "被引次数"},
    "f.is_safety":     {"en": "Safety-related flag (Y / —, amber-highlighted in the table)",
                       "zh": "是否安全性相关（Y / —，表中琥珀色高亮）"},
    "f.oa_flag":       {"en": "Open-access flag: Y = OA full text available (verified via "
                             "OpenAlex open_access.is_oa + OA locations, NOT inferred from links); "
                             "bioRxiv/medRxiv/arXiv = preprint candidate (author-verified, "
                             "default-ON); — = no OA and no preprint.",
                       "zh": "是否开放获取：Y = 有 OA 全文（经 OpenAlex open_access.is_oa + OA "
                             "location 校验，非由链接有无推断）；bioRxiv/medRxiv/arXiv = 预印本候选"
                             "（经作者姓氏同篇校验，默认开启）；— = 无 OA 且无预印本。"},
    "f.abstract":      {"en": "Abstract snippet (for judging relevance before download)",
                       "zh": "摘要片段（用于下载前判断相关性）"},
    "f.pdf_size_kb":   {"en": "Downloaded PDF file size in KB (blank = not downloaded / not re-scanned)",
                        "zh": "已下载 PDF 的文件大小（KB）（空白 = 未下载 / 未重扫）"},
    "f.pdf_pages":     {"en": "Downloaded PDF page count (deep-verified: parser-openable and "
                             ">= 1 page; blank = not downloaded / parser unavailable)",
                        "zh": "已下载 PDF 的页数（经深度校验：可被解析器打开且 ≥1 页；"
                             "空白 = 未下载 / 无可用解析器）"},
    "f.mesh":          {"en": "MeSH terms (Europe PMC)", "zh": "医学主题词（Europe PMC）"},
    "f.funders":       {"en": "Funding organisations (OpenAlex)", "zh": "资助机构（OpenAlex）"},
    # ---- source attribution banner (R1: provenance of the retrieval engine) ----
    "src.banner":       {"en": "Retrieval engine: ct-literature (local + Coze dual-engine; OpenAlex primary)",
                        "zh": "检索引擎：ct-literature（本地 + Coze 双引擎；OpenAlex 为主源）"},
    # ---- caveat callout (data caveats) ----
    "caveat.title":    {"en": "Data caveats", "zh": "数据局限"},
    "caveat.text":     {"en": "① OpenAlex is the primary source; Europe PMC / Semantic Scholar are optional enrichments. ② Abstract availability depends on the source (Europe PMC ≈100%, OpenAlex partial). ③ Deduplicated by DOI / title; multi-source works keep provenance. ④ This is published-literature evidence, NOT trial-registry metadata (see ct-registry); the safety subset is qualitative, not FAERS quantitative signal. ⑤ Citation count reflects impact, NOT evidence quality — clinical evidence grade follows study design (RCT / systematic review).",
                       "zh": "① OpenAlex 为主源，Europe PMC / Semantic Scholar 为可选增强；② 摘要可用性取决于来源（Europe PMC ≈100%，OpenAlex 部分缺失）；③ 按 DOI / 标题去重，多源文献保留来源溯源；④ 本表为已发表文献证据，非试验注册信息（见 ct-registry）；安全性子集为定性证据，非 FAERS 定量信号；⑤ 被引次数仅反映影响力，非证据质量——临床证据等级以研究设计（RCT / 系统评价）为准。"},
    # ---- evidence log (P0: provenance + citation verification, ct-base §17.1) ----
    "sheet.evidence":   {"en": "Evidence Log", "zh": "证据溯源"},
    "ev.title":        {"en": "Evidence Provenance & Citation Verification", "zh": "证据溯源与引文验证"},
    "ev.generated":    {"en": "Generated", "zh": "生成时间"},
    "ev.verify":       {"en": "Citation verification", "zh": "引文验证"},
    "ev.verified":     {"en": "Verified", "zh": "已验证"},
    "ev.unresolved":   {"en": "Unresolved", "zh": "未解析"},
    "ev.no_id":        {"en": "No identifier", "zh": "无标识"},
    "ev.suspicious":   {"en": "Suspicious", "zh": "可疑"},
    "ev.mismatch":     {"en": "Mismatch", "zh": "不一致"},
    "ev.mismatch.note": {"en": "identifier resolved to a LIVE resource but title/author do NOT match — possible hallucinated/incorrect id",
                         "zh": "标识符解析到存活资源，但标题/作者不一致 —— 可能为幻觉或错误 id"},
    "ev.preview":      {"en": "preview — verification skipped", "zh": "预览，已跳过验证"},
    "ev.verify.top":   {"en": "top-%s verified; remaining works not checked (--verify all for full)",
                       "zh": "仅验证 top-%s；其余未核验（--verify all 全量）"},
    "ev.verify.none":  {"en": "verification disabled (--verify none)",
                       "zh": "已通过 --verify none 关闭核验"},
    "ev.sampled":      {"en": "Sampled out", "zh": "抽样跳过"},
    "ev.bot_blocked":  {"en": "Bot-blocked", "zh": "出版社拦爬"},
    "ev.bot_blocked.note": {"en": "publisher returned 403 to automated access — DOI is real, not a broken link",
                            "zh": "出版社对自动化访问回 403 —— DOI 真实有效、非断链"},
    "ev.src":          {"en": "Source", "zh": "来源"},
    "ev.run_config":   {"en": "Run config", "zh": "运行配置"},
    "ev.src_provenance": {"en": "Source provenance", "zh": "来源溯源"},
    "ev.query":        {"en": "Query", "zh": "检索式"},
    "ev.type":         {"en": "Type", "zh": "类型"},
    "ev.year":         {"en": "Year", "zh": "年份"},
    "ev.safety":       {"en": "Safety", "zh": "安全性"},
    "ev.count":        {"en": "Count", "zh": "数量"},
    "ev.retrieved":    {"en": "Retrieved", "zh": "检索时间"},
    "ev.status":       {"en": "Status", "zh": "状态"},
    "ev.note":         {"en": "Provenance audit trail (ct-base §17.1): every evidence item is traceable to its source query and retrieval time. Verification status is advisory, not a substitute for human review.",
                       "zh": "证据溯源审计（ct-base §17.1）：每条证据可回溯至来源检索式与检索时间；验证状态仅供参考，不替代人工核查。"},
    "cfg.degraded":     {"en": "Degraded sources", "zh": "降级数据源"},
}


def set_lang(code):
    global _LANG
    _LANG = "zh" if code in ("zh", "zh-CN", "zh-cn") else "en"
    _base_set_lang(code)


# ---- report UI language resolution (v1.6.3) --------------------------------
# The published workbench runs in an en_US container. The old
# 阶段 2（2026-11-06）：交付语言解析上移到 ct-base 共享件，消除三技能三份副本。
# 单一真源 ct-base/scripts/xlsx_delivery.py（publish_inject 注入本目录）；
# 契约与红线见 ct-base/references/xlsx_delivery.md。
from xlsx_delivery import resolve_report_lang  # noqa: E402


def t(key, **kw):
    if key in _LOCAL:
        return _LOCAL[key][_LANG].format(**kw)
    return _base_t(key, **kw)


def _style_series(chart_type, labels=None):
    lbl_font = {"size": 9, "font_name": FONT, "color": NAVY, "bold": False}
    opts = {"data_labels": {"value": True, "font": lbl_font}}
    if chart_type == "pie":
        opts = {"data_labels": {"percentage": True, "category": True,
                                "num_format": "0.0%", "font": lbl_font}, "gap": 55}
    if chart_type in ("col", "barh"):
        opts["gap"] = 55
        opts["fill"] = {"color": BLUE}
    if chart_type == "line":
        opts["line"] = {"color": NAVY, "width": 2.25}
        opts["marker"] = {"type": "circle", "size": 6,
                           "fill": {"color": BLUE}, "border": {"color": NAVY}}
    return opts


def _qref(name, cell):
    return "'%s'!%s" % (name, cell)


def _normalize_link(u):
    """Return a hyperlink-safe URL, or '' if `u` is not linkable.

    xlsxwriter.write_url raises 'Unknown URL type' for anything without a known
    scheme (http/https/ftp/mailto…). Real sources sometimes yield a bare DOI —
    e.g. Semantic Scholar ``externalIds.DOI`` or Europe PMC ``doi`` when no
    fullTextUrl is present — so normalise those to ``https://doi.org/<doi>`` and
    drop the rest (write as plain text instead of crashing the whole workbook).
    """
    if not u:
        return ""
    u = str(u).strip()
    if u.startswith(("http://", "https://", "ftp://", "ftps://", "mailto:")):
        return u
    if u.startswith("10."):
        return "https://doi.org/" + u
    return ""


# ═══════════════════════════════════════════════════════════════════════════
# sheet builders
# ═══════════════════════════════════════════════════════════════════════════
def build_readme(wb, data, fmts):
    ws = wb.add_worksheet(t("sheet.readme"))
    _page_decor(ws, t("doc.title"), fmts)
    ws.set_tab_color(NAVY)
    _banner(ws, 0, 0, 14, t("banner.title"), fmts)
    ws.set_row(0, 30)

    works = data.get("works") or []
    n = data.get("count") or len(works)
    n_safety = sum(1 for w in works if w.get("is_safety"))
    top = max((w.get("cited_by_count") or 0) for w in works) if works else 0
    yrs = sorted(y for y in (w.get("year") for w in works) if y)
    span = "%d–%d" % (yrs[0], yrs[-1]) if yrs else "—"
    meta = data.get("meta") or {}

    _logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                         "assets", "icon_4x.png")
    cover_logo(ws, _logo, col=14, scale=0.16, x_offset=20, y_offset=2)

    # rich-text subtitle (row 1): topic + generated time
    topic = meta.get("topic") or t("doc.title")
    topic_en = meta.get("topic_en")
    if topic_en and topic_en != topic:
        topic_disp = "%s → %s" % (topic, topic_en)  # 中文检索词 → 翻译英文
    else:
        topic_disp = topic
    ws.write_rich_string(1, 0,
                         fmts["sub"], t("scope.topic") + "：",
                         fmts["body"], (topic_disp or t("col.unknown"))[:60],
                         fmts["note"], "   " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    ws.set_row(1, 20)

    # ---- KPI cards (row 3): 4 cards ----
    _kpi_card(ws, 3, 0, t("kpi.count"), n, t("kpi.count_sub"), fmts)
    _kpi_card(ws, 3, 4, t("kpi.safety"), n_safety, t("kpi.safety_sub"), fmts)
    _kpi_card(ws, 3, 8, t("kpi.cited"), top, t("kpi.cited_sub"), fmts)
    _kpi_card(ws, 3, 12, t("kpi.span"), span, t("kpi.span_sub"), fmts)
    ws.set_row(3, 18)   # label
    ws.set_row(4, 32)   # value (22pt)
    ws.set_row(5, 14)   # sub

    # ---- scope (search overview) ----
    r = 8
    ws.set_row(7, 6)
    ws.merge_range(7, 0, 7, 14, "", fmts["divider"])
    ws.write(r, 0, t("scope.title"), fmts["sub"])
    r += 1
    src = ", ".join(sorted(set(w.get("source", "") for w in works))) or "—"
    yf = meta.get("year_from")
    yt = meta.get("year_to")
    yr_range = ("%s–%s" % (yf, yt)) if (yf or yt) else "—"
    rt = meta.get("review_type") or "all"
    kw = meta.get("keywords")
    kw_str = kw if isinstance(kw, str) else (", ".join(str(x) for x in kw) if kw else "—")
    # R1: standalone retrieval-engine provenance banner in README scope
    ws.merge_range(r, 0, r, 14, t("src.banner"), fmts["note"])
    ws.set_row(r, 16)
    r += 1

    scope = [
        (t("scope.topic"), topic_disp or t("col.unknown")),
        (t("scope.filter"), rt),
        (t("scope.source"), src),
        (t("scope.year"), yr_range),
        (t("scope.keywords"), kw_str),
    ]
    for k, v in scope:
        ws.write(r, 0, k, fmts["kpi_label"])
        ws.merge_range(r, 1, r, 14, v, fmts["body"])
        r += 1

    # ---- field dictionary (field meanings) ----
    r += 1
    ws.write(r, 0, t("field.title"), fmts["sub"])
    r += 1
    ws.write(r, 0, t("field.col"), fmts["header"])
    ws.merge_range(r, 1, r, 14, t("field.mean"), fmts["header"])
    r += 1
    fields = [
        ("col.source", "f.source"), ("col.title", "f.title"),
        ("col.authors", "f.authors"), ("col.year", "f.year"),
        ("col.publication", "f.publication"), ("col.type", "f.type"),
        ("col.study_type", "f.study_type"), ("col.cited", "f.cited"),
        ("col.is_safety", "f.is_safety"),
        ("col.oa_flag", "f.oa_flag"),
        ("col.abstract", "f.abstract"),
        ("col.pdf_size_kb", "f.pdf_size_kb"),
        ("col.pdf_pages", "f.pdf_pages"),
        ("col.mesh", "f.mesh"), ("col.funders", "f.funders"),
    ]
    for i, (ck, mk) in enumerate(fields):
        zebra = (i % 2 == 1)
        key_fmt = fmts["fkey_z"] if zebra else fmts["fkey"]
        val_fmt = fmts["zebra"] if zebra else fmts["plain"]
        ws.write(r, 0, t(ck), key_fmt)
        ws.merge_range(r, 1, r, 14, t(mk), val_fmt)
        r += 1

    # ---- caveat callout (data caveats) ----
    r += 1
    ws.write(r, 0, t("caveat.title"), fmts["sub"])
    r += 1
    ws.merge_range(r, 0, r + 2, 14, t("caveat.text"), fmts["warn"])
    ws.set_row(r, 18)
    ws.set_row(r + 1, 18)
    ws.set_row(r + 2, 18)

    ws.set_column(0, 0, 16)
    ws.set_column(1, 14, 13)
    return ws


# Shared works-table column definition — used by BOTH the Works sheet and the
# Safety-Related sheet so headers, widths (incl. the OA column) and autofilter
# never drift apart (2026-08-15: Safety sheet was missing autofilter and the
# OA column width, causing header-wrap).

_ABS_SECTION_RE = None  # lazy import re


def restore_abstract_paragraphs(text):
    """Structured abstracts arrive as a single flat string from Europe PMC /
    OpenAlex (verified: source abstractText contains NO line breaks). Restore
    paragraph breaks heuristically at the classic section labels that medical
    abstracts begin paragraphs with — BACKGROUND / OBJECTIVE / METHODS /
    RESULTS / CONCLUSIONS: etc. Free-form narrative abstracts (no labels) are
    returned unchanged. Paragraph text itself is never modified.
    Placeholder abstracts (e.g. "How to cite", too short) return "—".
    """
    s = (text or "").strip()
    if not s:
        return "—"
    if len(s) < 20:
        return "—"
    # Check for known placeholder patterns
    import re as _re
    # Normalize: lowercase, strip punctuation, check against known placeholders
    normalized = _re.sub(r"[\s\[\]\(\)\{\}]+", " ", s.lower()).strip()
    placeholders = {
        "how to cite", "how to cite.", "[abstract unavailable]",
        "abstract not available", "no abstract available", "[no abstract]",
        "abstract:", "summary:", "abstract available", "unavailable",
        "abstract not provided", "not available", "n/a", "abstract not avail"
    }
    if normalized in placeholders:
        return "—"
    # Check if it looks like a placeholder (very short, starts with "[abstract" or "abstract")
    if len(s) < 30 and normalized.startswith(("abstract", "[abstract", "no abstract", "abstract not")):
        return "—"
    import re as _re
    global _ABS_SECTION_RE
    if _ABS_SECTION_RE is None:
        _ABS_SECTION_RE = _re.compile(
            r"(?i)(?<![A-Za-z0-9])(?:BACKGROUND AND OBJECTIVE|BACKGROUND|OBJECTIVE|"
            r"PURPOSE|INTRODUCTION|AIM|METHODS|MATERIALS AND METHODS|PATIENTS AND "
            r"METHODS|METHODOLOGY|RESULTS|FINDINGS|CONCLUSIONS?|DISCUSSION|TRIAL "
            r"REGISTRATION)\s*:")
    matches = list(_ABS_SECTION_RE.finditer(s))
    if len(matches) < 2:
        return s  # nothing to section-ise
    out = []
    prev = 0
    for m in matches:
        if m.start() <= 2:
            continue  # label at the very start — already a paragraph head
        seg = s[prev:m.start()].rstrip()
        if seg:
            out.append(seg)
            out.append("\n\n")
        prev = m.start()
    out.append(s[prev:].lstrip())
    return "".join(out)


# 2026-09-04 reorder (v2, per user): Type → Study type → Year → Journal →
# Authors → Title (hyperlinked to https://doi.org/<doi>, fallback url) →
# Abstract → DOI → Cited by → Safety → OA PDF. The standalone "Link" (url)
# column was removed — the title itself carries the DOI link now.
# 2026-09-06 (v3, per user): DOI column removed (title already hyperlinks to
# it); the standalone "OA" flag column removed as redundant with the link
# column, which is renamed "OA链接 / OA link". Column widths re-tuned.
# NOTE: meta-analysis A3 upload parsing (parse_screening_xlsx) locates columns
# BY HEADER NAME, not position, so this reorder is safe for the round-trip.
# IMPORTANT: headers are resolved via t() at WRITE time, not import time —
# resolving at import froze them to English because set_lang() runs later
# (this was the root cause of "bilingual headers never switch").
_WORKS_COLS = [("type", "col.type", 12),
               ("study_type", "col.study_type", 18),
               ("year", "col.year", 7),
               ("publication", "col.publication", 22),
               # DOI 是记录的第一标识列，必须落表（2026-09-10 补）：
               # 裁决表回传按 DOI 匹配远比标题稳健——人工在 Excel 里改一个标点、
               # 多一个换行，归一化标题就不再相交，匹配会静默降为 0 且不报错。
               # 纯文本写入（不加超链接）：① 便于人工复制/核对；② 回传端按文本读，
               # 不受超链接结构影响。标题单元格仍有 doi.org 超链可点。
               ("doi", "col.doi", 30),
               ("authors", "col.authors", 30),
               ("title", "col.title", 50),
               ("abstract_snippet", "col.abstract", 62),
               ("cited_by_count", "col.cited", 9),
               ("relevance_score", "col.relevance", 10),
               ("relevance_basis", "col.relevance_basis", 36),
               ("is_safety", "col.is_safety", 9),
               ("open_access_url", "col.oa", 24),
               ("local_pdf_path", "col.pdf_path", 36),
               # 下载质量佐证列（2026-10-25 PDF 下载增强）：大小KB + 页数。
               # 页数由深度校验（pypdf/fitz 解析）产出——残篇即使混过浅层校验，
               # 也会在页数上暴露；无解析器时为空白而非 0（不造假）。
               ("pdf_size_kb", "col.pdf_size_kb", 10),
               ("pdf_pages", "col.pdf_pages", 8)]


def _works_header(key_label):
    return t(key_label)


def _norm_doi(doi):
    """归一化 DOI 作为匹配键（works ↔ decisions）。"""
    if not doi:
        return ""
    return str(doi).strip().lower()


def _norm_title(title):
    """归一化标题作为匹配键（DOI 缺失时回退）。"""
    if not title:
        return ""
    return " ".join(str(title).strip().lower().split())


def _col_label(hkey):
    """列头标签解析：i18n key（"col.*"）经 t() 本地化；其余按字面量原样输出。

    让调用方（如 meta-analysis）可以自带列名而不必改共享模块的 i18n 表。
    """
    if isinstance(hkey, str) and hkey.startswith("col."):
        return t(hkey)
    return hkey


def _build_decision_map(decisions, extra_keys=()):
    """把 [{doi,title,decision,reason,...}, ...] 建成 {匹配键: 行记录}。

    匹配键优先 DOI（更稳），DOI 缺失/重复时回退归一化标题。
    extra_keys：随裁决一并携带的附加列键（如 "doc_type"），值原样透传。
    返回 dict：键为 _norm_doi 或 _norm_title 的结果，值为 {
        "decision":…, "reason":…, <extra_key>:… }。
    """
    mp = {}
    if not decisions:
        return mp
    extra_keys = tuple(extra_keys or ())
    for d in decisions:
        if not isinstance(d, dict):
            continue
        rec = {"decision": d.get("decision"), "reason": d.get("reason") or ""}
        for k in extra_keys:
            rec[k] = d.get(k)
        key = _norm_doi(d.get("doi")) or _norm_title(d.get("title"))
        if key:
            mp[key] = rec
    return mp


def _write_works_table(ws, works, fmts, safety_hl, start_row=0, decision_map=None,
                       decision_options=None, decision_extra=None):
    cols = _WORKS_COLS
    has_dec = bool(decision_map)
    # 决策列（可选）：仅在传入 decisions 时出现，避免影响普通检索导出
    extra = [("decision", "col.decision", 12), ("reason", "col.reason", 40)] if has_dec else []
    # 附加列（可选）：附加决策列，仅在同时存在决策列时有意义（值随裁决行携带）
    if has_dec:
        extra += [(s["key"], s.get("label") or s["key"], s.get("width", 16))
                  for s in (decision_extra or []) if isinstance(s, dict) and s.get("key")]
    all_cols = cols + extra
    ws.set_row(start_row, HEADER_H)
    for ci, (_, hkey, _) in enumerate(all_cols):
        ws.write(start_row, ci, _col_label(hkey), fmts["header"])
    for ri, w in enumerate(works, start=start_row + 1):
        zebra = ((ri - start_row - 1) % 2 == 1)
        base = fmts["zebra"] if zebra else fmts["plain"]
        # safety-relevant rows get an amber highlight (wins over zebra)
        row_fmt = safety_hl if w.get("is_safety") else base
        for ci, (key, _, _) in enumerate(cols):
            v = w.get(key)
            if key == "authors":
                av = v if isinstance(v, list) else [str(v)]
                ws.write(ri, ci, ", ".join(av)[:120], row_fmt)
            elif key == "title":
                tstr = (v or "")[:240]
                # 2026-09-04: title cell itself becomes the hyperlink —
                # DOI link first (https://doi.org/<doi>), fallback to url.
                link = _normalize_link(w.get("doi")) or _normalize_link(w.get("url"))
                if link and tstr:
                    ws.write_url(ri, ci, link, fmts["link"], string=tstr)
                else:
                    ws.write(ri, ci, tstr, row_fmt)
            elif key == "is_safety":
                ws.write(ri, ci, "Y" if v else "—",
                         fmts["center"] if not w.get("is_safety") else safety_hl)

            elif key == "is_oa":
                pp = w.get("preprint") if isinstance(w.get("preprint"), dict) else None
                if v:
                    ws.write(ri, ci, "Y", fmts["oa_yes"])
                elif pp:
                    venue = str(pp.get("venue") or "preprint")
                    label = {"biorxiv": "bioRxiv", "medrxiv": "medRxiv",
                             "biorxiv_medrxiv": "bioRxiv/medRxiv",
                             "arxiv": "arXiv"}.get(venue, venue)
                    ws.write(ri, ci, label, fmts["preprint_tag"])
                else:
                    ws.write(ri, ci, "—", fmts["center"])
            elif key == "open_access_url":
                oa = _normalize_link(v)
                # 开放获取链接：OA URL 优先；无 OA 但有预印本候选时降级到预印本链接
                # （venue 标签如 "OA PDF / medRxiv" 区分发表版与预印本）
                pp = w.get("preprint") if isinstance(w.get("preprint"), dict) else None
                if oa:
                    ws.write_url(ri, ci, oa, fmts["link"], string="OA PDF")
                elif pp:
                    pp_url = _normalize_link(pp.get("url") or (
                        ("https://doi.org/" + pp["doi"]) if pp.get("doi") else ""))
                    venue = str(pp.get("venue") or "preprint")
                    label = {"biorxiv": "bioRxiv", "medrxiv": "medRxiv",
                             "biorxiv_medrxiv": "bioRxiv/medRxiv",
                             "arxiv": "arXiv"}.get(venue, venue)
                    if pp_url:
                        ws.write_url(ri, ci, pp_url, fmts["link"], string=label)
                    else:
                        ws.write(ri, ci, label, row_fmt)
                else:
                    ws.write(ri, ci, "—", row_fmt)
            elif key == "abstract_snippet":
                # 完整摘要（text_wrap 由 zebra/plain 格式承载；行高在行尾自适应）；
                # 按医学摘要段首标签恢复分段（源为单段文本）
                ws.write(ri, ci, restore_abstract_paragraphs(v or ""), row_fmt)
            elif key == "local_pdf_path":
                # PDF 本地路径：本地脚本产物（pipeline / PdfDownloader / update_xlsx_pdf_paths），
                # 由用户在本地打开 → 必须写**绝对路径**，便于复制到资源管理器直接定位。
                # 网页端不渲染该列（网页只提供下载，不存在本地路径概念）；若要在网页里展示，
                # 由前端自行取 os.path.basename。
                from pathlib import Path
                if v and Path(str(v)).is_file():
                    ws.write(ri, ci, os.path.normpath(str(v)), row_fmt)
                elif w.get("pdf_download_note"):
                    ws.write(ri, ci, "失败", fmts["center"])
                else:
                    ws.write(ri, ci, "—", fmts["center"])
            elif key in ("pdf_size_kb", "pdf_pages"):
                # 下载质量佐证（2026-10-25）：空白 = 未下载/无解析器，写 — 占位
                # （不写 0——0 页是「校验失败」语义，不能与「未知」混淆）。
                if v is None or v == "":
                    ws.write(ri, ci, "—", fmts["center"])
                else:
                    ws.write(ri, ci, v, fmts["right"])
            elif key == "cited_by_count":
                ws.write(ri, ci, v if v is not None else 0, fmts["right"])
            else:
                ws.write(ri, ci, v, row_fmt)
        if has_dec:
            # 按 DOI（优先）/ 标题匹配本行对应的裁决/理由（+ 附加列）
            key = _norm_doi(w.get("doi")) or _norm_title(w.get("title"))
            rec = decision_map.get(key) or {}
            ci0 = len(cols)
            ws.write(ri, ci0, rec.get("decision") or "", base)
            ws.write(ri, ci0 + 1, rec.get("reason") or "", base)
            for j, spec in enumerate(decision_extra or [], start=2):
                if not isinstance(spec, dict) or not spec.get("key"):
                    continue
                ws.write(ri, ci0 + j, rec.get(spec["key"]) or "", base)
        # 行高自适应：按摘要（主）与标题（次）的估算折行数设置行高，默认展开约 5 行
        # —— 摘要文本始终完整写入（text_wrap），更长内容在 Excel 中双击该行头
        # 下边界（自动适应行高）或手动拖高即可查看全文，避免每行撑满半屏。
        est = 1
        alen = len((w.get("abstract_snippet") or "").strip())
        if alen:
            est = max(est, (alen + 55) // 56)
        tlen = len((w.get("title") or "").strip())
        if tlen:
            est = max(est, (tlen + 42) // 43)
        ws.set_row(ri, min(13.5 * est, 68))
    # 裁决列加下拉列表（仅当调用方显式传入选项时）：人工在 Excel 里逐条选
    # 纳入/排除/低置信，避免手打错字；空单元格（未裁决）放行。
    # 双标签（中文 + 英文 internal）兼容预填的英文 internal 值，不触发校验红标。
    # decision_options 由 meta-analysis 传入（与其 _DECISION_ALIAS 口径一致），
    # 共享模块本身不持有裁决语义。
    if has_dec and works and decision_options:
        col = len(cols)  # 裁决列索引
        ws.data_validation(start_row + 1, col, start_row + len(works), col, {
            "validate": "list",
            "source": list(decision_options),
            "ignore_blank": True,
            "show_error": True,
            "error_title": "裁决取值",
            "error_message": "请从下拉选择：纳入 / 排除 / 低置信",
        })
    # 附加列下拉：由调用方给选项（如「文献类型确认」的原始/综述/指南/方案），
    # 保证人工只能选合法值，回传端无需猜写错的形式。
    if has_dec and works:
        for j, spec in enumerate(decision_extra or [], start=2):
            if not isinstance(spec, dict) or not spec.get("options"):
                continue
            col = len(cols) + j
            ws.data_validation(start_row + 1, col, start_row + len(works), col, {
                "validate": "list",
                "source": list(spec["options"]),
                "ignore_blank": True,
                "show_error": True,
                "error_title": (spec.get("label") or spec["key"]),
                "error_message": spec.get("error_message") or "请从下拉选择",
            })
    return len(works)


def build_works(wb, data, fmts, safety_hl, decisions=None, decision_options=None,
                decision_extra=None):
    ws = wb.add_worksheet(t("sheet.works"))
    _page_decor(ws, t("sheet.works"), fmts)
    ws.set_tab_color(BLUE)
    works = data.get("works") or []
    extra_specs = [s for s in (decision_extra or [])
                   if isinstance(s, dict) and s.get("key")]
    dmap = (_build_decision_map(decisions, [s["key"] for s in extra_specs])
            if decisions else None)
    n = _write_works_table(ws, works, fmts, safety_hl, decision_map=dmap,
                           decision_options=decision_options,
                           decision_extra=extra_specs)
    ws.freeze_panes(1, 0)
    ncols = len(_WORKS_COLS) + (2 if dmap else 0) + (len(extra_specs) if dmap else 0)
    if works:
        ws.autofilter(0, 0, n, ncols - 1)
    for ci, (_, _, w) in enumerate(_WORKS_COLS):
        ws.set_column(ci, ci, w)
    if dmap:
        ws.set_column(len(_WORKS_COLS), len(_WORKS_COLS), 12)       # 裁决
        ws.set_column(len(_WORKS_COLS) + 1, len(_WORKS_COLS) + 1, 40)  # 理由
        for j, spec in enumerate(extra_specs, start=2):
            c = len(_WORKS_COLS) + j
            ws.set_column(c, c, spec.get("width", 16))
    return ws


def _render_dist_block(ws, row0, title, label_header, chart_type, items, fmts, wb, sheet_name, color_map=None):
    """A distribution block: block title + (label/count/share) table + total row +
    data bar + right-side chart. Returns the 0-based bottom row so the caller can
    step to the next band without over-reserving blank rows (prevents overlap)."""
    total = sum(c for _, c in items) or 1
    ws.merge_range(row0, 0, row0, 2, title, fmts["block_title"])
    hdr = row0 + 1
    ws.write(hdr, 0, label_header, fmts["header"])
    ws.write(hdr, 1, t("col.count"), fmts["header"])
    ws.write(hdr, 2, t("col.share"), fmts["header"])
    r = hdr + 1
    for label, cnt in items:
        zebra = ((r - hdr) % 2 == 1)
        ws.write(r, 0, label if label else t("col.unknown"),
                 fmts["zebra"] if zebra else fmts["plain"])
        ws.write(r, 1, cnt, fmts["right"])
        ws.write(r, 2, cnt / total, fmts["pct"])
        r += 1
    last = r - 1
    # total row
    ws.write(last + 1, 0, t("ov.total"), fmts["sumrow"])
    ws.write(last + 1, 1, total, fmts["sumrow"])
    ws.write(last + 1, 2, 1.0, fmts["pct"])
    sum_row = last + 1
    r = sum_row + 1
    # data bar on the share column only
    if last >= hdr + 1:
        ws.conditional_format(hdr + 1, 2, last, 2,
                              {"type": "data_bar", "bar_color": BLUE})
    # native chart on the RIGHT (column E), top-aligned with the data header row.
    if items:
        last_ch = last
        n_rows = last - hdr
        h = _chart_h(n_rows)
        w = h if chart_type == "pie" else _chart_w(h)
        ch = _add_chart(wb, chart_type, title, w, h)
        cats = [sheet_name, hdr + 1, 0, last_ch, 0]
        vals = [sheet_name, hdr, 1, last_ch, 1]
        pts = None
        if chart_type == "pie":
            pts = _dist_pie_points("source", items, color_map) if color_map \
                  else _dist_pie_points("type", items)
        ch.add_series({
            "categories": cats,
            "values": vals,
            "points": pts or [],
            **_style_series(chart_type),
        })
        ws.insert_chart("%s%d" % (CHART_COL, hdr), ch)
    # block extent = max(table bottom, chart bottom) so the next band never overlaps
    table_bottom = last
    chart_bottom = row0 + (h // ROW_PX) if items else 0
    return max(table_bottom, chart_bottom)


def _render_top_block(ws, row0, fmts, works):
    """Top-cited list block (no chart)."""
    ws.merge_range(row0, 0, row0, 2, t("ov.top"), fmts["block_title"])
    hdr = row0 + 1
    ws.write(hdr, 0, t("col.title"), fmts["header"])
    ws.write(hdr, 1, t("col.cited"), fmts["header"])
    r = hdr + 1
    for i, w in enumerate(sorted(works, key=lambda x: -(x.get("cited_by_count") or 0))[:10]):
        zebra = ((r - hdr) % 2 == 1)
        ws.write(r, 0, (w.get("title") or "")[:90],
                 fmts["zebra"] if zebra else fmts["plain"])
        ws.write(r, 1, w.get("cited_by_count") or 0, fmts["right"])
        r += 1
    return r - 1


def build_overview(wb, data, fmts):
    ws = wb.add_worksheet(t("sheet.overview"))
    _page_decor(ws, t("sheet.overview"), fmts)
    ws.set_tab_color(BLUE)
    works = data.get("works") or []
    name = t("sheet.overview")

    _banner(ws, 0, 0, 12, t("ov.banner"), fmts)
    ws.merge_range(1, 0, 1, 12, t("ov.intro"), fmts["note"])

    row0 = 3
    # 1) year distribution (column chart)
    yr = Counter(w.get("year") for w in works if w.get("year"))
    yitems = sorted(yr.items())
    if yitems:
        row0 = _render_dist_block(ws, row0, t("ov.year"), t("col.year"),
                                  "col", yitems, fmts, wb, name) + 1 + BAND_GAP
    # 2) source distribution (pie, branded colours)
    src = Counter(w.get("source", "—") for w in works)
    sitems = sorted(src.items(), key=lambda x: -x[1])
    if sitems:
        row0 = _render_dist_block(ws, row0, t("ov.source"), t("col.source"),
                                  "pie", sitems, fmts, wb, name, _SOURCE_COLOR) + 1 + BAND_GAP
    # 3) type distribution (pie)
    typ = Counter(w.get("type", "—") for w in works)
    titems = sorted(typ.items(), key=lambda x: -x[1])
    if titems:
        row0 = _render_dist_block(ws, row0, t("ov.type"), t("col.type"),
                                  "pie", titems, fmts, wb, name) + 1 + BAND_GAP
    # 4) study_type distribution (pie)
    st = Counter((w.get("study_type") or "—") for w in works)
    stitems = sorted(st.items(), key=lambda x: -x[1])
    if stitems:
        row0 = _render_dist_block(ws, row0, t("ov.stype"), t("col.study_type"),
                                  "pie", stitems, fmts, wb, name) + 1 + BAND_GAP
    # 5) top-cited list
    row0 = _render_top_block(ws, row0, fmts, works) + 1 + BAND_GAP

    ws.set_column(0, 0, 40)
    for col in range(1, 3):
        ws.set_column(col, col, 12)
    for col in range(3, 12):   # narrow gutter so right-side charts never crowd tables
        ws.set_column(col, col, 3)
    return ws


def build_safety(wb, data, fmts, safety_hl, safety=False):
    """Safety-Related sheet (opt-in).

    Only emitted when the run was requested with `--safety` (the CSM /
    safety-literature subset). In a plain literature search this sheet is
    intentionally NOT created — the safety/CSM qualitative subset is the
    domain of an explicit safety-oriented call (or a ct-safety chained
    invocation), not a default deliverable of every search.
    """
    if not safety:
        return None
    ws = wb.add_worksheet(t("sheet.safety"))
    _page_decor(ws, t("sheet.safety"), fmts)
    ws.set_tab_color(BLUE)
    works = [w for w in (data.get("works") or []) if w.get("is_safety")]
    n = _write_works_table(ws, works, fmts, safety_hl)
    ws.freeze_panes(1, 0)
    # same header filter + column widths as the Works sheet (incl. OA col 28)
    if works:
        ws.autofilter(0, 0, n, len(_WORKS_COLS) - 1)
    for ci, (_, _, w) in enumerate(_WORKS_COLS):
        ws.set_column(ci, ci, w)
    return ws


# ═══════════════════════════════════════════════════════════════════════════
# entry point
# ═══════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════
# evidence log (P0: provenance + citation verification, ct-base §17.1)
# ═══════════════════════════════════════════════════════════════
def build_evidence(wb, data, fmts):
    ws = wb.add_worksheet(t("sheet.evidence"))
    _page_decor(ws, t("sheet.evidence"), fmts)
    ws.set_tab_color(NAVY)
    _banner(ws, 0, 0, 12, t("ev.title"), fmts)
    ws.set_row(0, 30)
    evidence = data.get("evidence_log") or {}
    verification = data.get("verification") or {}
    r = 2

    # generated time
    if evidence.get("generated_at"):
        ws.write(r, 0, t("ev.generated"), fmts["kpi_label"])
        ws.merge_range(r, 1, r, 12, evidence["generated_at"], fmts["body"])
        r += 1

    # run-time config audit block (key status — avoids silently taking the wrong path)
    cfg = evidence.get("config") or {}
    if cfg:
        ws.write(r, 0, t("ev.run_config"), fmts["sub"])
        r += 1
        _cstat = lambda s: ("configured ✓" if s == "configured"
                            else ("missing — keyless" if s == "missing" else str(s)))
        for label, key in (("OpenAlex key", "openalex_key"),
                           ("Semantic Scholar key", "semantic_scholar_key"),
                           ("PROSPERO token", "prospero_token")):
            val = cfg.get(key)
            if val is None:
                continue
            ws.write(r, 0, label, fmts["fkey"])
            ws.merge_range(r, 1, r, 12, _cstat(val), fmts["body"])
            r += 1
        # actionable follow-up: when the OpenAlex key is absent, show HOW to get one
        # (status alone is not actionable for the user)
        if cfg.get("openalex_key") == "missing":
            _u = cfg.get("openalex_key_url") or "https://docs.openalex.org/about-openalex/api-key"
            _m = ("⚠️ 未配置 OpenAlex key：本次为 keyless 模式（限 100 次/天，易 429）。"
                  "免费申请后写入技能 `.env`（OPENALEX_API_KEY=<key>）：%s" % _u
                  if _LANG == "zh" else
                  "⚠️ OpenAlex key missing: this run used the keyless pool (100 credits/day, "
                  "easily rate-limited). Apply for a FREE key and write it to the skill `.env` "
                  "(OPENALEX_API_KEY=<key>): %s" % _u)
            ws.merge_range(r, 0, r, 12, _m, fmts["body"])
            r += 1
        r += 1

    # degraded sources (rate-limit / fetch failure) — friendly, actionable note
    degraded = evidence.get("degraded") or []
    if degraded:
        ws.write(r, 0, t("cfg.degraded"), fmts["sub"])
        r += 1
        for _d in degraded:
            _msg = _d.get("message_%s" % _LANG)  # xlsx auto-switches locale like the report
            ws.write(r, 0, "⚠️ %s (%s)" % (_d.get("source"), _d.get("status")), fmts["fkey"])
            ws.merge_range(r, 1, r, 12, _msg or "", fmts["body"])
            r += 1
        r += 1

    # citation verification summary block
    if verification:
        ws.write(r, 0, t("ev.verify"), fmts["sub"])
        r += 1
        if verification.get("skipped_preview"):
            skip = " " + t("ev.preview")
        elif verification.get("mode") == "top":
            skip = " " + (t("ev.verify.top") % verification.get("top_n", 15))
        elif verification.get("mode") == "none":
            skip = " " + t("ev.verify.none")
        else:
            skip = ""
        vrows = [
            (t("ev.verified"), verification.get("verified", 0)),
            (t("ev.bot_blocked"), verification.get("bot_blocked", 0)),
            (t("ev.mismatch"), verification.get("mismatch", 0)),
            (t("ev.unresolved"), verification.get("unresolved", 0)),
            (t("ev.no_id"), verification.get("no_identifier", 0)),
            (t("ev.suspicious"), verification.get("suspicious", 0)),
            (t("ev.sampled"), verification.get("unverified_sampled", 0)),
        ]
        ws.write(r, 0, "total", fmts["fkey"])
        ws.merge_range(r, 1, r, 2, verification.get("total", 0), fmts["right"])
        r += 1
        for label, cnt in vrows:
            ws.write(r, 0, label, fmts["fkey"])
            ws.merge_range(r, 1, r, 2, cnt, fmts["right"])
            r += 1
        _bb = verification.get("bot_blocked", 0)
        _bb_note = (" — %s" % t("ev.bot_blocked.note")) if _bb else ""
        _mm = verification.get("mismatch", 0)
        _mm_note = (" — %s" % t("ev.mismatch.note")) if _mm else ""
        ws.merge_range(r, 0, r, 12, ("verified=%s · bot-blocked=%s · mismatch=%s · "
                                     "unresolved=%s · no_identifier=%s · suspicious=%s · "
                                     "sampled=%s%s%s%s" % (
                                         verification.get("verified", 0),
                                         _bb,
                                         _mm,
                                         verification.get("unresolved", 0),
                                         verification.get("no_identifier", 0),
                                         verification.get("suspicious", 0),
                                         verification.get("unverified_sampled", 0),
                                         _bb_note, _mm_note, skip)), fmts["note"])
        r += 2

    # source provenance table
    srcs = evidence.get("sources") or []
    if srcs:
        ws.write(r, 0, t("ev.src_provenance"), fmts["sub"])
        r += 1
        headers = [t("ev.src"), t("ev.query"), t("ev.type"), t("ev.year"),
                   t("ev.safety"), t("ev.count"), t("ev.retrieved"), t("ev.status")]
        for ci, h in enumerate(headers):
            ws.write(r, ci, h, fmts["header"])
        r += 1
        for s in srcs:
            yf = s.get("year_from") or ""
            yt_ = s.get("year_to") or ""
            yr = ("%s–%s" % (yf, yt_)) if (yf or yt_) else "—"
            row = [s.get("source"), (s.get("query") or "")[:120],
                   s.get("review_type") or "all", yr,
                   "Y" if s.get("safety") else "—", s.get("count", 0),
                   (s.get("retrieved_at") or "")[:19], s.get("status", "")]
            for ci, v in enumerate(row):
                ws.write(r, ci, v, fmts["plain"])
            r += 1
        r += 1

    # caveat callout
    ws.merge_range(r, 0, r + 2, 12, t("ev.note"), fmts["warn"])
    ws.set_row(r, 18)
    ws.set_row(r + 1, 18)
    ws.set_row(r + 2, 18)

    ws.set_column(0, 0, 16)
    ws.set_column(1, 1, 50)
    for col in range(2, 8):
        ws.set_column(col, col, 14)
    return ws


def _coerce_int(v):
    """Coerce a possibly string/None numeric field to int, else None."""
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        return int(v)
    if isinstance(v, str) and v.strip().lstrip("-").isdigit():
        return int(v.strip())
    return None


def sanitize(data):
    """Normalise a merged payload so mixed / missing types cannot crash sheets.

    Real-world .merged.json may carry year as str, cited_by_count as None,
    sources as None, or list fields holding None elements. Sorting or joining
    those raises TypeError deep inside a sheet builder and aborts the whole
    workbook, so we coerce once at the entry point.
    """
    if not isinstance(data, dict):
        data = {"works": data if isinstance(data, list) else []}
    works = [w for w in (data.get("works") or []) if isinstance(w, dict)]
    clean = []
    for w in works:
        w = dict(w)
        w["year"] = _coerce_int(w.get("year"))
        w["cited_by_count"] = _coerce_int(w.get("cited_by_count")) or 0
        w["is_oa"] = bool(w.get("is_oa"))
        srcs = w.get("sources")
        if not isinstance(srcs, (list, tuple)) or not srcs:
            srcs = [w.get("source")]
        w["sources"] = [str(s) for s in srcs if s]
        w["source"] = str(w.get("source") or (w["sources"][0] if w["sources"] else "—"))
        for k in ("authors", "mesh", "concepts", "keywords", "funders"):
            v = w.get(k)
            w[k] = [str(x) for x in v if x] if isinstance(v, (list, tuple)) else []
        for k in ("title", "abstract_snippet"):
            if w.get(k) is not None and not isinstance(w[k], str):
                w[k] = str(w[k])
        clean.append(w)
    data = dict(data)
    data["works"] = clean
    data["count"] = data.get("count") if isinstance(data.get("count"), int) else len(clean)
    return data


def export_workbook(data, out_path, lang="auto", safety=False, decisions=None,
                    decision_options=None, decision_extra=None):
    data = sanitize(data)
    # Promote provenance / verification blocks from `meta` when the caller passed
    # them nested (the pipeline passes {count, works, meta}); the standalone CLI
    # passes .merged.json which already has them at top level. Without this, the
    # Evidence Log sheet renders EMPTY — verification stats, source provenance and
    # run-config are all dropped (regression introduced at v0.6.8).
    _meta = data.get("meta") or {}
    for _k in ("evidence_log", "verification"):
        if _k not in data and _meta.get(_k) is not None:
            data[_k] = _meta[_k]
    # Always resolve explicitly — never fall back to the server OS locale.
    set_lang(resolve_report_lang(lang, skill="literature"))
    wb = xlsxwriter.Workbook(out_path)
    fmts = make_formats(wb, PALETTES["literature"])
    # safety-row highlight (amber) — local extension of the shared format set
    fmts["safety_hl"] = wb.add_format({"bg_color": P["warn_bg"], "border": 1,
                                       "border_color": GRID, "font_name": FONT,
                                       "font_size": 10, "valign": "top",
                                       "text_wrap": True})
    # OA=Y cell (green tint, same family as the zebra light but readable as "yes")
    fmts["oa_yes"] = wb.add_format({"bg_color": "#CDEBD6", "border": 1,
                                    "border_color": GRID, "font_name": FONT,
                                    "font_size": 10, "align": "center",
                                    "valign": "vcenter"})
    # Preprint tag in the OA column (amber, distinct from the green Y)
    fmts["preprint_tag"] = wb.add_format({"bg_color": "#FFF2CC", "border": 1,
                                          "border_color": GRID, "font_name": FONT,
                                          "font_size": 10, "align": "center",
                                          "valign": "vcenter", "bold": True,
                                          "font_color": "#BF9000"})
    build_readme(wb, data, fmts)
    build_overview(wb, data, fmts)
    build_works(wb, data, fmts, fmts["safety_hl"], decisions=decisions,
                decision_options=decision_options, decision_extra=decision_extra)
    # Safety-Related sheet is opt-in: only when --safety (CSM subset) is requested.
    # A plain literature search keeps the workbook to 3 sheets (README / Overview /
    # Works / Evidence Log) — the safety subset is NOT a default deliverable.
    build_safety(wb, data, fmts, fmts["safety_hl"], safety=safety)
    build_evidence(wb, data, fmts)
    wb.close()


def main():
    ap = argparse.ArgumentParser(description="Export ct-literature .merged.json to .xlsx")
    ap.add_argument("--in-json", default=".merged.json", help=".merged.json (hidden intermediate)")
    ap.add_argument("--out", required=True, help="output .xlsx path")
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"],
                    help="report UI language (auto = CT_LITERATURE_LANG / config / "
                         "default zh, NEVER the server OS locale; en forces English)")
    ap.add_argument("--topic", default=None, help="search topic (for README scope)")
    ap.add_argument("--review-type", default=None, help="review type filter")
    ap.add_argument("--year-from", default=None, help="year from")
    ap.add_argument("--year-to", default=None, help="year to")
    ap.add_argument("--safety", action="store_true",
                    help="emit the Safety-Related sheet (CSM subset); "
                         "otherwise the workbook keeps only 3 data sheets")
    args = ap.parse_args()
    with open(args.in_json, encoding="utf-8") as f:
        data = json.load(f)
    if "meta" not in data:
        data["meta"] = {
            "topic": args.topic,
            "review_type": args.review_type,
            "year_from": args.year_from,
            "year_to": args.year_to,
        }
    export_workbook(data, args.out, lang=args.lang, safety=args.safety)
    print("[OK] wrote", args.out)


if __name__ == "__main__":
    main()
