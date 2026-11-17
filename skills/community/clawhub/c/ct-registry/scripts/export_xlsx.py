#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""export_xlsx.py - Export normalized trial records to a multi-sheet Excel workbook.

Designed for clinical users: ONE .xlsx file, opened by double-click, with
filterable/sortable tables, clickable homepage links, embedded charts, a
    cover-style README with KPI cards, status colour-coding, share-column data
    bars, and a rich-text cover -- a dashboard-like workbook, all produced
natively inside the .xlsx (no web page).

Implementation note (v0.3.20): rendering is done exclusively with **xlsxwriter**
(>=3.0). xlsxwriter is write-only (cannot reopen/edit an existing file) which is
fine here because the workbook is generated from scratch each run. It gives us,
vs openpyxl: native icon sets, richer chart data labels, single-cell rich-text
(covers with mixed formats), proper header/footer codes, and faster writes.

i18n (v0.3.25 / v0.14.4): all UI frame labels are localized via ct-base's shared
``i18n.t()`` (single source of truth in ct-base/scripts/i18n.py, keys ``xlsx.*``).
Pass ``--lang {auto,zh,en}``. ``auto`` is resolved by :func:`resolve_report_lang`
(workbench UI language > config > cover-title language > OS locale > zh) instead
of blindly following the server OS locale -- the published workbench runs in an
en_US container, which used to make every Chinese user's workbook all-English.
RAW DATA VALUES (e.g. CDE Chinese status "进行中", Chinese conditions) are NEVER
translated -- data fidelity is preserved; only the interface chrome switches
language.

Sheets (names are also localized):
  1. 说明 / README            - cover banner + KPI cards + scope + field dictionary
  2. 检索结果概要 / Summary   - 9 distribution / summary bands (LEFT data table + RIGHT
                                 native chart): 分期 / 状态 / 数据来源 / 适应症 / 国家地区 /
                                 逐年趋势 / 申办方 / 样本量统计+直方图 / 分期×状态交叉矩阵。
                                 each category block has a "合计" row and a data bar on the
                                 share column (no icon set; arrows were removed for clarity).
  3. 试验总表 / Master        - one row per trial; clickable homepage; status colour-coded;
                                 frozen header + autofilter
  4. 原始明细 / Raw           - flattened key columns for traceability

All styling is applied with xlsxwriter only -- the deliverable stays a single .xlsx.
"""

import argparse
import json
import os
import platform
import re
import statistics
import sys
from collections import Counter

import xlsxwriter


# ═══════════════════════════════════════════════════════════════════════════
# i18n — ct-base's shared i18n (vendored into this skill directory)
# ═══════════════════════════════════════════════════════════════════════════
# IMPORTANT (2026-08-11): ct-base is NEVER published. Every ct- skill must carry
# its own complete copy. We ONLY import from this skill's own `scripts/` dir.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
try:
    from i18n import t, set_lang   # noqa: E402
except Exception:  # defensive fallback — vendored copy must be present
    def t(key, **kw):
        return key
    def set_lang(code):
        pass


# ---- shared Excel visual standard (vendored into this skill) ------
# All palette / format / layout / chart / status logic lives in
# scripts/excel_style.py (vendored from ct-base/scripts/excel_style.py).
try:
    from excel_style import (
        make_formats, banner as _banner, page_decor as _page_decor,
        kpi_card as _kpi_card, cover_logo, status_fill_hex as _status_hex,
        PALETTES, FONT, add_chart as _add_chart, style_series as _style_series,
        chart_h as _chart_h, chart_w as _chart_w, dist_pie_points,
        autofit_widths as _autofit_widths, join as _join, safe as _safe,
        year_of as _year, HEADER_H, STATUS_LEGEND as STATUS_LEGEND_KEYS,
        STATUS_LEGEND_COLOR as _LEGEND_COLOR,
    )
except Exception as _e:  # vendored copy must be present
    raise RuntimeError("ct-registry export_xlsx: cannot import vendored "
                       "excel_style: " + str(_e))
P = PALETTES["registry"]
NAVY, BLUE, LIGHT, BANNER = P["navy"], P["blue"], P["light"], P["banner"]
GRID, GREYTX = P["grid"], P["greytx"]
CARDHEAD, CARDBODY = P["cardhead"], P["cardbody"]
WARNBG, WARNBD = P["warn_bg"], P["warn_bd"]
# source slice colours for distribution pies (kept here: registry-specific CDE hue)
_SOURCE_COLOR = {"ICTRP": NAVY, "CDE": "#ED7D31"}

# ---- CTIS / EUCTR numeric status code → human label -------------------------
# The EU Clinical Trials Information System (CTIS) public API returns trial status
# as a NUMERIC code, not text. The mapping below is the *verified* decode (derived
# by probing the live API: each code's retrieve endpoint returns the label shown).
# Codes 2-5 all resolve to "Authorised" at the verified level; the portal's finer
# sub-labels (not started / recruiting / …) are NOT reliably code-mappable, so we
# deliberately do NOT invent them. Codes 13-18 are per-member-state sub-states
# (kept coarse here). Raw numeric codes are preserved (see _status_display); only a
# parenthetical label is added — the export rule "RAW DATA VALUES are NEVER
# normalized" is respected (rec dict is never mutated).
_CTIS_STATUS = {
    1:  ("Under evaluation", "评估中"),
    2:  ("Authorised", "已授权"),
    3:  ("Authorised", "已授权"),
    4:  ("Authorised", "已授权"),
    5:  ("Authorised", "已授权"),
    6:  ("Halted", "已暂停"),
    7:  ("Suspended", "已中止"),
    8:  ("Ended", "已结束"),
    9:  ("Expired", "已过期"),
    10: ("Revoked", "已撤销"),
    11: ("Not authorised", "未获授权"),
    12: ("Cancelled", "已取消"),
}
# Mirrors the i18n global set by set_lang(); updated in build() so the decode
# follows the report language.
_LANG = "zh"

def _ctis_status_label(val):
    """Return the (en, zh) label for a CTIS numeric status code, else None."""
    try:
        code = int(_safe(val))
    except (TypeError, ValueError):
        return None
    return _CTIS_STATUS.get(code)

def _status_display(rec):
    """Master/Raw cell text: keep the raw code, append a decoded label if it is a
    numeric CTIS status code; otherwise return the value unchanged."""
    raw = _safe(rec.get("status"))
    pair = _ctis_status_label(raw)
    if pair:
        return "%s (%s)" % (raw, pair[1] if _LANG == "zh" else pair[0])
    return raw

def _status_category(val):
    """Summary aggregation key: decode CTIS codes so 2-5 merge into 'Authorised'
    (collapsing three indistinguishable sub-states into one honest bucket)."""
    pair = _ctis_status_label(val)
    if pair:
        return pair[1] if _LANG == "zh" else pair[0]
    return _safe(val)


# ---- unified summary sheet -------------------------------------------------
# Charts float over the grid at a fixed pixel height. We anchor each chart to
# the first data row and let its height ADAPT to the table, with a hard floor of
# 20 rows (MIN_CHART_ROWS) so small distributions still get a readable chart.
# Blocks are stepped by their *actual* height (table vs chart, whichever is
# taller) plus a small BAND_GAP, so we no longer over-reserve blank rows.
ROW_PX         = 20    # xlsxwriter anchors at ~20px per Excel row (verified empirically)
MIN_CHART_ROWS = 20    # user floor: charts never shorter than 20 rows
MIN_CHART_H    = MIN_CHART_ROWS * ROW_PX   # 400 px == 20 rows
BAND_GAP       = 2     # blank rows between consecutive blocks
CHART_COL      = "E"   # column letter where dist/charts are anchored (right side)
# kind: "dist"    -> category distribution (label / count / share + chart)
#       "stats"   -> numeric summary (KPI table + histogram)
#       "crosstab"-> 2-D matrix (rows x cols) with colour scale only (table-only, no chart)
# Title and note are resolved per-call via t("xlsx.block.*") / t("xlsx.note.*").
SUMMARY_BLOCKS = [
    # key, chart_type, chart_max_rows, kind
    ("phase",       "col",  None, "dist"),
    ("status",      "pie",  None, "dist"),
    ("source",      "pie",  None, "dist"),
    ("ind",         "barh", 12,   "dist"),
    ("countries",   "barh", 12,   "dist"),
    ("timeline",    "line", None, "dist"),
    ("sponsor",     "barh", 15,   "dist"),
    ("enrollment",  "col",  None, "stats"),
    ("phase_status","none", None, "crosstab"),
]
NOTE_KEYS = {
    "status": "status_color", "source": "source", "ind": "top12",
    "countries": "top12_cde", "sponsor": "top15", "enrollment": "enroll",
    "phase_status": "crosstab",
}


def SHEET_SUMMARY():
    """Summary sheet name (resolved at call time, not import time, so it honors --lang)."""
    return t("xlsx.sheet.summary")


def _block_label(key):
    """First-column / x-axis category label for a summary block (call-time resolved)."""
    return t(f"xlsx.label.{key}") if key in (
        "phase", "status", "source", "ind", "countries", "timeline", "sponsor",
        "enrollment", "phase_status") else t("xlsx.col.category")


# ---- master table columns --------------------------------------------------
# Kept as field keys; headers are localized via t("xlsx.field.<key>").
MASTER_KEYS = [
    "registry_id", "title", "conditions", "study_type", "phase",
    "enrollment", "status", "sponsor", "countries", "start_date",
    "primary_outcome", "url",
]
STATUS_COL = MASTER_KEYS.index("status")  # 0-based


def _master_header(k):
    return t(f"xlsx.field.{k}")


# ---- report UI language resolution (阶段 2：上移 ct-base 共享件) ------------
# 单一真源：ct-base/scripts/xlsx_delivery.py（publish_inject 注入本目录）。
# 交付物语言禁止回退到服务器 OS locale；契约见 references/xlsx_delivery.md。
from xlsx_delivery import resolve_report_lang  # noqa: E402

_CJK_RE = re.compile(r"[\u3400-\u9fff\uf900-\ufaff]")  # 封面标题中英切分用


def _title_for_lang(title, lang):
    """英文交付物的封面标题优先使用英文检索词片段。

    检索词常为中英并列（"Orebatinib / 奥雷巴替尼"）；英文界面下原样保留会让
    封面出现中文字符。按 "/" 切片保留不含 CJK 的片段；全中文时保持原值（宁可
    保留数据，也不写空标题）。明细表内的中文数据值不受影响（数据保真红线）。
    """
    if lang != "en" or not title or not _CJK_RE.search(str(title)):
        return title
    parts = [p.strip() for p in str(title).split("/") if p.strip()]
    en_parts = [p for p in parts if not _CJK_RE.search(p)]
    return " / ".join(en_parts) if en_parts else title


# ---- helpers (data logic, library-agnostic) --------------------------------
# _year is imported from excel_style (as _year)


# _join is imported from excel_style (as _join)


# _safe is imported from excel_style (as _safe)


# _cjk_width is internal to excel_style.autofit_widths (imported)


# _autofit_widths is imported from excel_style (as _autofit_widths)


# _status_hex is imported from excel_style (as _status_hex)


# ---- numeric enrollment summary + histogram bins --------------------------
def _enroll_to_num(v):
    """Best-effort numeric parse for a possibly string-typed enrollment value."""
    if v is None:
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    m = re.search(r"\d[\d,]*", str(v))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def _enroll_summary(enrolls):
    """Return (stats_dict, bins_list). bins_list = [(label, count), ...]."""
    if not enrolls:
        st = {"n": 0, "total": 0, "mean": 0, "median": 0, "min": 0, "max": 0}
        return st, [(t("xlsx.no_data"), 0)]
    n = len(enrolls)
    total = sum(enrolls)
    mean = total / n
    median = statistics.median(enrolls)
    mn, mx = min(enrolls), max(enrolls)
    st = {"n": n, "total": int(total), "mean": mean,
          "median": median, "min": int(mn), "max": int(mx)}
    # Clinical size bands (fixed, meaningful for trials; covers Phase I/II small
    # studies through large Phase III pivotal trials; avoids sparse equal-width bins
    # when data is right-skewed: most early-phase trials are small with rare large ones).
    bands = [("≤20",     lambda x: x <= 20),
             ("21–50",   lambda x: 21 <= x <= 50),
             ("51–100",  lambda x: 51 <= x <= 100),
             ("101–200", lambda x: 101 <= x <= 200),
             ("201–500", lambda x: 201 <= x <= 500),
             (">500",    lambda x: x > 500)]
    bins = [(label, sum(1 for x in enrolls if pred(x))) for label, pred in bands]
    return st, bins


def _phase_status_matrix(recs):
    """Return (phases, statuses, matrix) ordered by frequency (unknown last)."""
    def order(c):
        items = c.most_common()
        items.sort(key=lambda kv: (kv[0] == t("xlsx.unknown"), -kv[1]))
        return [k for k, _ in items]
    pc = Counter(_safe(r.get("phase")) or t("xlsx.unknown") for r in recs)
    sc = Counter(_status_category(r.get("status")) or t("xlsx.unknown") for r in recs)
    phases, statuses = order(pc), order(sc)
    matrix = {}
    for r in recs:
        ph = _safe(r.get("phase")) or t("xlsx.unknown")
        st = _status_category(r.get("status")) or t("xlsx.unknown")
        matrix.setdefault(ph, {}).setdefault(st, 0)
        matrix[ph][st] += 1
    return (phases, statuses, matrix)


# ---- format factory (delegates to the shared ct-base standard) -------------
def _make_formats(wb):
    """All formats are produced by ct-base/scripts/excel_style.make_formats using
    the registry palette, so the visual system stays in sync across ct- skills."""
    return make_formats(wb, PALETTES["registry"])


# ---- low-level styling helpers (operate on a worksheet + formats) ----------
# _banner / _page_decor / _kpi_card are imported from vendored excel_style.
def _merge_box(ws, r1, c1, r2, c2, value, fmt):
    ws.merge_range(r1, c1, r2, c2, value, fmt)


# ---- chart factory: _add_chart / _style_series / _chart_h / _chart_w /
#     dist_pie_points are all imported from vendored excel_style. --------------


# ---- master table columns --------------------------------------------------
def build_readme(wb, recs, title, meta, fmts):
    ws = wb.add_worksheet(t("xlsx.sheet.readme"))
    _page_decor(ws, title or t("xlsx.doc.title"), fmts)
    ws.set_tab_color("#1F4E78")  # navy — cover sheet

    # ---- cover banner (row 0): navy bar, centered title ----
    _banner(ws, 0, 0, 14, t("xlsx.banner.title"), fmts)
    # brand logo pinned to the TOP-RIGHT, column O (last col), row 0 — sized to
    # span the first TWO rows (banner 30pt + subtitle 20pt = 50pt ≈ 66.5px) so it
    # reads as a tall brand mark aligned with the headline block. The mark is a
    # light (near-white) transparent PNG, clearly legible on the dark navy.
    # xlsxwriter ignores `width`/`height` for this anchor, so scale the 416px
    # source (416 * 0.16 ≈ 66.5px ≈ 2 rows).
    ws.set_row(0, 30)
    _logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                         "assets", "ct-registry_4x.png")
    cover_logo(ws, _logo, col=14, scale=0.16, x_offset=20, y_offset=2)
    # rich-text subtitle (row 1)
    ws.write_rich_string(1, 0,
                         fmts["sub"], t("xlsx.cover.topic"),
                         fmts["body"], (title or t("xlsx.unknown")) or "",
                         fmts["note"], "   " + t("xlsx.cover.generated"))
    ws.set_row(1, 20)

    # ---- KPI cards (row 3) ----
    total = len(recs)
    who = sum(1 for r in recs if r.get("source") == "ICTRP")
    cde = sum(1 for r in recs if r.get("source") == "CDE")
    yrs = sorted(y for y in (_year(r.get("start_date")) for r in recs) if y)
    span = f"{yrs[0]}–{yrs[-1]}" if yrs else "—"
    _kpi_card(ws, 3, 0, t("xlsx.kpi.total"), total, t("xlsx.kpi.total_sub"), fmts)
    _kpi_card(ws, 3, 4, t("xlsx.kpi.who"), who, t("xlsx.kpi.who_sub"), fmts)
    _kpi_card(ws, 3, 8, t("xlsx.kpi.cde"), cde, t("xlsx.kpi.cde_sub"), fmts)
    _kpi_card(ws, 3, 12, t("xlsx.kpi.span"), span, t("xlsx.kpi.span_sub"), fmts)
    # explicit KPI row heights so the 22pt value fits at any zoom (no clip)
    ws.set_row(3, 18)   # label
    ws.set_row(4, 32)   # value (22pt)
    ws.set_row(5, 14)   # sub

    # ---- info cards (scope) ----
    r = 8
    # thin separator band between KPI area and scope (visual grouping)
    ws.set_row(7, 6)
    ws.merge_range(7, 0, 7, 14, "", fmts["divider"])
    ws.write(r, 0, t("xlsx.readme.scope_title"), fmts["sub"])
    r += 1
    info = [
        (t("xlsx.scope.topic"), title or t("xlsx.unknown")),
        (t("xlsx.scope.range"), t("xlsx.scope.range_val")),
        (t("xlsx.scope.source"), t("xlsx.scope.source_val")),
        (t("xlsx.scope.quota"), t("xlsx.scope.quota_val")),
    ]
    for k, v in info:
        ws.write(r, 0, k, fmts["kpi_label"])
        ws.merge_range(r, 1, r, 14, v, fmts["body"])
        r += 1

    # ---- field dictionary ----
    r += 1
    ws.write(r, 0, t("xlsx.readme.field_title"), fmts["sub"])
    r += 1
    fields = [
        (t("xlsx.field.registry_id"), t("xlsx.field.registry_id_desc")),
        (t("xlsx.field.conditions"), t("xlsx.field.conditions_desc")),
        (t("xlsx.field.study_type"), t("xlsx.field.study_type_desc")),
        (t("xlsx.field.phase"), t("xlsx.field.phase_desc")),
        (t("xlsx.field.enrollment"), t("xlsx.field.enrollment_desc")),
        (t("xlsx.field.status"), t("xlsx.field.status_desc")),
        (t("xlsx.field.sponsor"), t("xlsx.field.sponsor_desc")),
        (t("xlsx.field.countries"), t("xlsx.field.countries_desc")),
        (t("xlsx.field.start_date"), t("xlsx.field.start_date_desc")),
        (t("xlsx.field.primary_outcome"), t("xlsx.field.primary_outcome_desc")),
        (t("xlsx.field.url"), t("xlsx.field.url_desc")),
    ]
    ws.write(r, 0, t("xlsx.field.col"), fmts["header"])
    ws.merge_range(r, 1, r, 14, t("xlsx.field.meaning"), fmts["header"])
    r += 1
    for i, (k, v) in enumerate(fields):
        zebra = (i % 2 == 1)
        # key (field name) and value (description) share the same row background
        # -> uniform zebra striping; key is bolded for hierarchy only.
        key_fmt = fmts["fkey_z"] if zebra else fmts["fkey"]
        val_fmt = fmts["zebra"] if zebra else fmts["plain"]
        ws.write(r, 0, k, key_fmt)
        ws.merge_range(r, 1, r, 14, v, val_fmt)
        r += 1

    # ---- status colour legend (so the master-table coding is self-explanatory) ----
    r += 1
    ws.write(r, 0, t("xlsx.legend.title"), fmts["sub"])
    r += 1
    for lk in STATUS_LEGEND_KEYS:
        sw = wb.add_format({"bg_color": _LEGEND_COLOR[lk], "border": 1,
                            "border_color": GRID})
        ws.write(r, 0, "", sw)
        ws.merge_range(r, 1, r, 14, t(f"xlsx.legend.{lk}"), fmts["body"])
        r += 1

    # ---- caveat callout ----
    r += 1
    ws.merge_range(r, 0, r + 2, 14, t("xlsx.caveat.text"), fmts["warn"])
    ws.set_row(r, 18)
    ws.set_row(r + 1, 18)
    ws.set_row(r + 2, 18)

    # column widths
    ws.set_column(0, 14, 13)
    ws.set_column(0, 0, 16)
    return ws


def build_master(wb, recs, fmts):
    ws = wb.add_worksheet(t("xlsx.sheet.master"))
    _page_decor(ws, t("xlsx.sheet.master"), fmts)
    ws.set_tab_color("#70AD47")  # green — data detail sheet
    ncol = len(MASTER_KEYS)
    headers = [_master_header(k) for k in MASTER_KEYS]

    # header on row 0 (native table object below applies the filter + header look)
    ws.set_row(0, 24)  # matched header height with the 原始明细 sheet
    for ci, h in enumerate(headers):
        ws.write(0, ci, h, fmts["header"])

    row = 1
    col_cells = [[] for _ in MASTER_KEYS]
    for rec in recs:
        vals = [_join(rec.get(key)) for key in MASTER_KEYS]
        for ci, v in enumerate(vals):
            # decode CTIS numeric status to "code (label)" only at display time
            col_cells[ci].append(_status_display(rec) if ci == STATUS_COL else v)
        zebra = ((row - 1) % 2 == 1)
        for ci, v in enumerate(vals):
            if ci == STATUS_COL:
                raw = rec.get("status")
                sf = _status_hex(raw)
                disp = _status_display(rec)
                if sf:
                    ws.write(row, ci, disp, fmts["status"][sf])
                else:
                    ws.write(row, ci, disp, fmts["center"] if zebra else fmts["plain"])
            elif ci == 5:  # 样本量 right-aligned
                ws.write(row, ci, v, fmts["right"])
            else:
                ws.write(row, ci, v, fmts["zebra"] if zebra else fmts["plain"])
        # homepage hyperlink
        url = _safe(rec.get("url"))
        if url and str(url).lower().startswith(("http://", "https://")):
            ws.write_url(row, ncol - 1, url, fmts["link"], string=str(vals[-1]))
        row += 1

    # content-aware column widths (CJK-aware) — long titles/sponsors no longer
    # overflow or get over-padded; the table "responds" to its data.
    for i, w in enumerate(_autofit_widths(col_cells, headers, min_w=10, max_w=60)):
        ws.set_column(i, i, w)
    ws.freeze_panes(1, 0)
    # NOTE: we deliberately do NOT use a native Excel table here. A native table
    # carries its own built-in style (e.g. TableStyleMedium2) that RE-PAINTS the
    # header row with a different colour, breaking visual consistency with the
    # 原始明细 sheet (which uses the shared navy fmts["header"]). Autofilter +
    # the manual per-cell zebra below give the same UX without the style clash.
    ws.autofilter(0, 0, row - 1, ncol - 1)
    if row > 1:
        ws.repeat_rows(0, 0)  # repeat header row on every printed page
    return ws


def build_raw(wb, recs, fmts):
    ws = wb.add_worksheet(t("xlsx.sheet.raw"))
    _page_decor(ws, t("xlsx.sheet.raw"), fmts)
    ws.set_tab_color("#BFBFBF")  # grey — raw/traceability sheet
    raw_cols = ["source", "registry_id", "title", "status", "phase", "study_type",
                "conditions", "interventions", "sponsor", "countries", "enrollment",
                "start_date", "primary_outcome", "secondary_outcome", "inclusion",
                "exclusion", "comparator", "age_min", "age_max", "gender", "url"]
    ncol = len(raw_cols)
    STATUS_COL_RAW = raw_cols.index("status")  # 0-based
    headers = [t(f"xlsx.field.{k}") for k in raw_cols]
    ws.set_row(0, 24)  # taller header row (matched to master sheet)
    for ci, h in enumerate(headers):
        ws.write(0, ci, h, fmts["header"])
    # numeric columns sit flush-right for scanning (ported from ct-safety).
    num_cols = {raw_cols.index(c) for c in ("enrollment", "age_min", "age_max")
                if c in raw_cols}
    row = 1
    col_cells = [[] for _ in raw_cols]
    for rec in recs:
        vals = [_join(rec.get(k)) for k in raw_cols]
        for ci, v in enumerate(vals):
            # decode CTIS numeric status to "code (label)" only at display time
            col_cells[ci].append(_status_display(rec) if ci == STATUS_COL_RAW else v)
        # Per-cell zebra striping — IDENTICAL scheme to the master sheet
        # (LIGHT fill + grey border on odd rows; plain white on even rows) so the
        # two detail sheets read as one visual system. A native-table band was
        # avoided for the same reason as master: it would re-paint the header.
        zebra = ((row - 1) % 2 == 1)
        for ci, v in enumerate(vals):
            if ci == STATUS_COL_RAW:
                raw = rec.get("status")
                sf = _status_hex(raw)
                disp = _status_display(rec)
                if sf:
                    ws.write(row, ci, disp, fmts["status"][sf])
                else:
                    ws.write(row, ci, disp, fmts["center"] if zebra else fmts["plain"])
            elif ci in num_cols:
                ws.write(row, ci, v, fmts["right"])
            else:
                ws.write(row, ci, v, fmts["zebra"] if zebra else fmts["plain"])
        row += 1
    # content-aware widths (CJK-aware) replace the old uniform 22px columns.
    for i, w in enumerate(_autofit_widths(col_cells, headers, min_w=10, max_w=60)):
        ws.set_column(i, i, w)
    ws.freeze_panes(1, 0)
    ws.autofilter(0, 0, row - 1, ncol - 1)
    if row > 1:
        ws.repeat_rows(0, 0)  # repeat header row on every printed page
    return ws


def build_summary(wb, dists, fmts):
    ws = wb.add_worksheet(SHEET_SUMMARY())
    _page_decor(ws, SHEET_SUMMARY(), fmts)
    ws.set_tab_color("#2E75B6")  # blue — summary/analytics sheet
    _banner(ws, 0, 0, 12, t("xlsx.banner.summary"), fmts)
    ws.merge_range(1, 0, 1, 12, t("xlsx.summary.intro"), fmts["note"])

    row0 = 3  # 0-based band start (first band)
    for key, chart_type, cmax, kind in SUMMARY_BLOCKS:
        title = t(f"xlsx.block.{key}")
        note = t(f"xlsx.note.{NOTE_KEYS[key]}") if key in NOTE_KEYS else ""
        if kind == "dist":
            end = _render_dist_block(ws, row0, key, title, chart_type, cmax, note, dists, fmts, wb)
        elif kind == "stats":
            end = _render_stats_block(ws, row0, title, note, dists, fmts, wb)
        elif kind == "crosstab":
            end = _render_crosstab_block(ws, row0, title, note, dists["phase_status"], fmts)
        # step to next band by actual height + a small gap (no over-reservation)
        row0 = end + 1 + BAND_GAP

    ws.set_column(0, 0, 42)
    for col in range(1, 7):
        ws.set_column(col, col, 13)
    for col in range(7, 13):
        ws.set_column(col, col, 3)
    return ws


# ---- block renderers -------------------------------------------------------
def _render_dist_block(ws, row0, key, title, chart_type, cmax, note, dists, fmts, wb):
    items = dists[key]
    total = sum(c for _, c in items) or 1

    ws.merge_range(row0, 0, row0, 2, title, fmts["block_title"])
    hdr = row0 + 1  # 0-based header row
    ws.write(hdr, 0, _block_label(key), fmts["header"])
    ws.write(hdr, 1, t("xlsx.col.count"), fmts["header"])
    ws.write(hdr, 2, t("xlsx.col.share"), fmts["header"])

    r = hdr + 1
    for label, cnt in items:
        zebra = ((r - hdr) % 2 == 1)
        ws.write(r, 0, label if label else t("xlsx.unknown"), fmts["zebra"] if zebra else fmts["plain"])
        ws.write(r, 1, cnt, fmts["right"])
        ws.write(r, 2, cnt / total, fmts["pct"])
        r += 1
    last = r - 1  # 0-based last data row

    # 合计 row
    ws.write(last + 1, 0, t("xlsx.total"), fmts["sumrow"])
    ws.write(last + 1, 1, total, fmts["sumrow"])
    ws.write(last + 1, 2, 1.0, fmts["pct"])
    sum_row = last + 1
    r = sum_row + 1

    # conditional formatting: data bar on share col only (icon set / 小箭头 removed)
    if last >= hdr + 1:
        ws.conditional_format(hdr + 1, 2, last, 2,
                              {"type": "data_bar", "bar_color": BLUE})

    # native chart on the right (column E). Height ADAPTS to the table height so the
    # chart and table read as one balanced unit (small tables -> short charts, large
    # tables -> tall charts). Anchored at the FIRST DATA row (not the blue header) so
    # the chart top aligns with the data, not the title bar.
    if items:
        last_ch = last if not cmax else min(last, hdr + cmax)
        n_rows = last - hdr  # data rows (excl. 合计)
        h = _chart_h(n_rows)
        if chart_type == "pie":
            # pie stays square; floor = 20 rows, gentle cap for very large pies
            w = h
        else:
            # landscape width (~1.2:1) so column/bar charts don't look thin
            w = _chart_w(h)
        ch = _add_chart(wb, chart_type, title, w, h)
        cats = [SHEET_SUMMARY(), hdr + 1, 0, last_ch, 0]
        vals = [SHEET_SUMMARY(), hdr, 1, last_ch, 1]
        pts = dist_pie_points(key, items, _SOURCE_COLOR) if chart_type == "pie" else None
        ch.add_series({
            "categories": cats,
            "values": vals,
            "points": pts or [],
            **_style_series(ch, chart_type),
        })
        if chart_type == "line":
            ch.set_x_axis({"name": _block_label(key), "name_font": {"font_name": FONT}})
            ch.set_y_axis({"name": t("xlsx.col.count"), "name_font": {"font_name": FONT}})
        # anchor at the BLOCK TITLE row (2 rows above the first data row) so the
        # chart top is flush with the section title, not the data header.
        ws.insert_chart(f"{CHART_COL}{hdr}", ch)

    if note:
        ws.write(sum_row + 2, 0, "· " + note, fmts["note"])

    # block extent (0-based) = max(table bottom, floating chart bottom) so the
    # caller can step to the next band without over-reserving blank rows.
    note_row = sum_row + 2 if note else last
    table_bottom = max(last, note_row)
    chart_bottom = row0 + (h // ROW_PX) if items else 0
    return max(table_bottom, chart_bottom)


def _render_stats_block(ws, row0, title, note, dists, fmts, wb):
    st = dists["enrollment"]
    bins = dists["enroll_bins"]

    # title spans A:B only -- matches the 2-column tables below.
    ws.merge_range(row0, 0, row0, 1, title, fmts["block_title"])
    # --- KPI-style stats table (left, A:B) ---
    hdr = row0 + 1
    ws.write(hdr, 0, t("xlsx.col.metric"), fmts["header"])
    ws.write(hdr, 1, t("xlsx.col.value"), fmts["header"])
    stats_rows = [
        (t("xlsx.stat.n"), st["n"]),
        (t("xlsx.stat.total"), st["total"]),
        (t("xlsx.stat.median"), st["median"]),
        (t("xlsx.stat.mean"), round(st["mean"], 1)),
        (t("xlsx.stat.min"), st["min"]),
        (t("xlsx.stat.max"), st["max"]),
    ]
    r = hdr + 1
    for i, (k, v) in enumerate(stats_rows):
        zebra = (i % 2 == 1)
        ws.write(r, 0, k, fmts["zebra"] if zebra else fmts["plain"])
        ws.write(r, 1, v, fmts["right"])
        r += 1

    # --- histogram table (left, BELOW KPI table, with extra gap rows so the
    #     right-side chart never crowds the KPI rows) ---
    hhdr = r + 2  # 2 blank rows between KPI table and histogram table
    ws.write(hhdr, 0, t("xlsx.col.enroll_band"), fmts["header"])
    ws.write(hhdr, 1, t("xlsx.col.count"), fmts["header"])
    r2 = hhdr + 1
    for label, cnt in bins:
        zebra = ((r2 - hhdr) % 2 == 1)
        ws.write(r2, 0, label, fmts["zebra"] if zebra else fmts["plain"])
        ws.write(r2, 1, cnt, fmts["right"])
        r2 += 1
    last2 = r2 - 1

    # histogram chart anchored at COLUMN E (same column as the other distribution
    # charts) and top-aligned with the BLOCK TITLE row (2 rows up from the histogram
    # data row) -- so it reads as one visual system with blocks 1-7 instead of sitting
    # off to the left at column C. Height adapts to the band count (20-row floor).
    if bins:
        n_bins = last2 - hhdr
        h = _chart_h(n_bins)
        ch = _add_chart(wb, "col", t("xlsx.chart.enroll_hist"), _chart_w(h), h)
        cats = [SHEET_SUMMARY(), hhdr + 1, 0, last2, 0]
        vals = [SHEET_SUMMARY(), hhdr, 1, last2, 1]
        ch.add_series({"categories": cats, "values": vals,
                       **_style_series(ch, "col")})
        ws.insert_chart(f"E{row0 + 1}", ch)  # align with block title, column E

    if note:
        ws.write(last2 + 2, 0, "· " + note, fmts["note"])

    # block extent (0-based): table bottom vs floating histogram bottom
    note_row = last2 + 2 if note else last2
    table_bottom = max(last2, note_row)
    chart_bottom = row0 + (h // ROW_PX) if bins else 0
    return max(table_bottom, chart_bottom)


def _render_crosstab_block(ws, row0, title, note, cross, fmts):
    phases, statuses, matrix = cross
    ncol = 1 + len(statuses) + 1  # +1 for the 合计 column

    ws.merge_range(row0, 0, row0, ncol - 1, title, fmts["block_title"])
    hdr = row0 + 1
    ws.write(hdr, 0, _block_label("phase_status"), fmts["header"])
    for j, st in enumerate(statuses, start=1):
        ws.write(hdr, j, st, fmts["header"])
    ws.write(hdr, ncol - 1, t("xlsx.total"), fmts["header"])

    r = hdr + 1
    for ph in phases:
        zebra = ((r - hdr) % 2 == 1)
        ws.write(r, 0, ph if ph else t("xlsx.unknown"), fmts["zebra"] if zebra else fmts["plain"])
        tot = 0
        for j, st in enumerate(statuses, start=1):
            c = matrix.get(ph, {}).get(st, 0)
            tot += c
            ws.write(r, j, c, fmts["right"])
        ws.write(r, ncol - 1, tot, fmts["sumrow"])
        r += 1
    last = r - 1

    # column totals row
    ws.write(r, 0, t("xlsx.total"), fmts["sumrow"])
    grand = 0
    for j, st in enumerate(statuses, start=1):
        c = sum(matrix.get(ph, {}).get(st, 0) for ph in phases)
        grand += c
        ws.write(r, j, c, fmts["sumrow"])
    ws.write(r, ncol - 1, grand, fmts["sumrow"])
    r += 1

    # colour scale over the count area (exclude 合计 col & total row)
    if last >= hdr + 1 and statuses:
        ws.conditional_format(hdr + 1, 1, last, len(statuses),
                              {"type": "3_color_scale",
                               "min_color": "#FFFFFF",
                               "mid_color": "#9DC3E6",
                               "max_color": BLUE})

    if note:
        ws.write(r + 1, 0, "· " + note, fmts["note"])

    # block extent (0-based): crosstab has no chart, just table + note
    return (r + 1) if note else r


def prepare_dists(recs):
    """Compute all summary distributions from a normalized record list.

    Pure data step (no IO) — returns the ``dists`` dict consumed by
    :func:`build_summary`. Callers may invoke this directly to inspect or
    pre-compute aggregations without touching the rendering layer.
    """
    phase_items = Counter(_safe(r.get("phase")) or t("xlsx.unknown") for r in recs).most_common()
    status_items = Counter(_status_category(r.get("status")) or t("xlsx.unknown") for r in recs).most_common()
    ind_counter = Counter()
    for r in recs:
        vals = r.get("conditions") or []
        if isinstance(vals, list):
            for v in vals:
                if v:
                    ind_counter[v.strip()] += 1
        elif vals:
            ind_counter[str(vals).strip()] += 1
    ind_items = ind_counter.most_common(12)
    tl_items = sorted(Counter(_year(r.get("start_date")) or t("xlsx.unknown") for r in recs).items())
    sp_items = Counter(_safe(r.get("sponsor")) or t("xlsx.unknown") for r in recs).most_common(15)

    # ---- extended dimensions (v0.3.17) ----
    source_items = Counter(_safe(r.get("source")) or t("xlsx.unknown") for r in recs).most_common()
    cc = Counter()
    for r in recs:
        vals = r.get("countries") or []
        if isinstance(vals, list):
            for v in vals:
                if v:
                    cc[v.strip()] += 1
        elif vals:
            cc[str(vals).strip()] += 1
    if not cc:
        cc[t("xlsx.unknown")] = 0
    country_items = cc.most_common(12)
    # R7: coerce defensively. Records may arrive from an older run (or be
    # hand-assembled) where enrollment is still a string such as "1,200";
    # the old isinstance() filter dropped those from the stats silently.
    enrolls = []
    for r in recs:
        v = r.get("enrollment")
        if isinstance(v, bool):
            continue
        if isinstance(v, (int, float)):
            enrolls.append(float(v))
            continue
        n = _enroll_to_num(v)
        if n is not None:
            enrolls.append(n)
    enroll_stats, enroll_bins = _enroll_summary(enrolls)
    phase_status = _phase_status_matrix(recs)

    return {"phase": phase_items, "status": status_items, "ind": ind_items,
            "timeline": tl_items, "sponsor": sp_items,
            "source": source_items, "countries": country_items,
            "enrollment": enroll_stats, "enroll_bins": enroll_bins,
            "phase_status": phase_status}


def build(recs, title, meta, out, lang="auto"):
    """Render the 4-sheet workbook from a normalized record list and save to ``out``.

    This is the internal builder. Prefer :func:`export_workbook` for direct calls;
    ``build`` is kept for backward compatibility (same signature as earlier versions,
    plus the optional ``lang`` keyword).
    """
    # Always resolve explicitly. Leaving "auto" to i18n's OS-locale default made
    # the published (en_US container) workbench emit an all-English workbook.
    resolved = resolve_report_lang(lang, skill="registry", title=title)
    set_lang(resolved)
    global _LANG
    _LANG = resolved
    title = _title_for_lang(title, resolved)
    wb = xlsxwriter.Workbook(out)
    wb.set_properties({"title": title or t("xlsx.doc.title"),
                       "author": "ct-registry · export_xlsx.py"})
    fmts = _make_formats(wb)

    dists = prepare_dists(recs)

    # Sheet 1: README (cover) -> Sheet 2: Summary -> Sheet 3: Master -> Sheet 4: Raw
    build_readme(wb, recs, title, meta, fmts)
    build_summary(wb, dists, fmts)
    build_master(wb, recs, fmts)
    build_raw(wb, recs, fmts)

    wb.close()
    return len(wb.worksheets())


def export_workbook(recs, out_path, *, title="", meta=None, lang="auto"):
    """Public high-level API — the one call you need to (re)generate a report.

    Args:
        recs: list of normalized trial dicts, OR a dict with a ``"records"`` key
            (the shape produced by the normalizer / aggregation steps).
        out_path: destination ``.xlsx`` path.
        title: report title shown on the cover and sheet banners (optional).
        meta: reserved for future use (currently unused).
        lang: language for the report UI — ``"auto"`` (default; resolved by
            :func:`resolve_report_lang`: workbench UI language > config >
            cover-title language > OS locale > zh), ``"zh"`` or ``"en"``.
            Raw DATA values are never translated (data fidelity).

    Returns:
        int — number of worksheets written.

    Example (no code edits required to regenerate a file)::

        from export_xlsx import export_workbook
        import json

        recs = json.load(open("normalized.json", encoding="utf-8"))
        export_workbook(recs, "report.xlsx",
                        title="奥雷巴替尼 I/II 期 (2020 至今)", lang="zh")

    The heavy lifting (distribution math, styling, charts) is all encapsulated,
    so callers never rewrite layout code — just pass data + path + title (+ lang).
    """
    if isinstance(recs, dict):
        recs = recs.get("records") or recs.get("records_all") or []
    return build(recs, title, meta, out_path, lang=lang)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="normalized detail JSON")
    ap.add_argument("--out", required=True, help="output .xlsx path")
    ap.add_argument("--title", default="")
    ap.add_argument("--meta", default="")
    ap.add_argument("--lang", choices=["auto", "zh", "en"], default="auto",
                    help="report UI language (auto=workbench UI / config / title "
                         "language / OS locale, zh, en)")
    args = ap.parse_args()
    recs = json.load(open(args.inp, encoding="utf-8"))
    if isinstance(recs, dict):
        recs = recs.get("records") or recs.get("records_all") or []
    n = build(recs, args.title, args.meta, args.out, lang=args.lang)
    print(f"[export_xlsx] {len(recs)} records -> {args.out} ({n} sheets)")


if __name__ == "__main__":
    main()
