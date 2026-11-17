#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""export_xlsx.py - Export downloaded FAERS case reports to a multi-sheet Excel workbook.

Designed for pharmacovigilance users: ONE .xlsx file, opened by double-click, with
filterable/sortable case table, a cover-style README with KPI cards, and a Summary
sheet that auto-aggregates 9 distributions (each: LEFT data table + RIGHT native
chart). All charts are native .xlsx (no web page).

i18n: all UI frame labels are localized via vendored ``i18n.t()``
(copy of ct-base/scripts/i18n.py, keys ``xlsx.*`` / ``xlsx.safety.*``).
``--lang {auto,zh,en}`` (default ``auto``) is resolved by
:func:`resolve_report_lang` — explicit value > CT_SAFETY_LANG > config >
default zh — instead of blindly following the server OS locale (the published
workbench runs in an en_US container). RAW DATA VALUES (reaction PTs, country
codes, drug names, indication text) are NEVER translated — data fidelity is
preserved; only the interface chrome switches language.

Sheets (names also localized):
  1. 说明 / README            - cover banner + 8 KPI cards + scope + data caveat
  2. 检索结果概要 / Summary   - 9 distribution bands (LEFT table + RIGHT chart):
                                 seriousness / sex / report type / country / age /
                                 annual trend / top reactions / top indications / drug role
  3. 个案明细 / Cases         - one row per downloaded case (unified 12-column template)

Implementation: xlsxwriter (>=3.0), write-only. Charts float at adaptive pixel height.

Reuses the rendering pattern proven in ct-registry/export_xlsx.py, but with a
medical-red theme and FAERS-specific distributions; chart value ranges are FIXED to
start at the first DATA row (hdr+1) — correcting the off-by-one in the upstream
reference where values started at the header row.
"""

import argparse
import json
import os
import re
import statistics
import sys
from collections import Counter
from datetime import datetime

import xlsxwriter


# ═══════════════════════════════════════════════════════════════════════════
# i18n — vendored copy of ct-base's shared i18n
# IMPORTANT (2026-08-11): ct-base is NEVER published. Every ct- skill must carry
# its own complete copy. We ONLY import from this skill's own `scripts/` dir.
# ═══════════════════════════════════════════════════════════════════════════
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


# ---- report UI language resolution (阶段 2：上移 ct-base 共享件) ------------
# 单一真源 ct-base/scripts/xlsx_delivery.py（publish_inject 注入本目录）。
# 交付物语言禁止回退到服务器 OS locale；契约见 references/xlsx_delivery.md。
from xlsx_delivery import resolve_report_lang  # noqa: E402
from xlsx_sheets import build_case_details  # noqa: E402


# ---- shared Excel visual standard (vendored from ct-base) ------
# All palette / format / layout / chart logic lives in scripts/excel_style.py
# (vendored from ct-base/scripts/excel_style.py).
try:
    from excel_style import (
        make_formats, banner as _banner, page_decor as _page_decor,
        kpi_card as _kpi_card, cover_logo, PALETTES, FONT,
        add_chart as _add_chart, chart_h as _chart_h, chart_w as _chart_w,
        ROW_PX, MIN_CHART_ROWS, MIN_CHART_H, BAND_GAP, HEADER_H,
    )
except Exception as _e:
    raise RuntimeError("ct-safety export_xlsx: cannot import vendored "
                       "excel_style: " + str(_e))
P = PALETTES["safety"]
RED, DARKRED, LIGHTRED = P["blue"], P["navy"], P["light"]
BANNER = P["banner"]
GRID, GREYTX = P["grid"], P["greytx"]
CARDHEAD, CARDBODY = P["cardhead"], P["cardbody"]
WARNBG, WARNBD = P["warn_bg"], P["warn_bd"]
CHART_COL = "G"   # safety anchors charts one column further right (title band is wider)
# safety-specific chart theming (medical-red) is kept local:
#   _style_series(chart_type, labels)  — red bars/lines
#   _pie_points(key)                   — serious/sex semantic slices

# kind: "dist" -> category distribution (label / count / share + chart)
SAFETY_BLOCKS = [
    # key, chart_type, chart_max_rows, kind
    ("serious",     "pie",  None, "dist"),
    ("sex",         "pie",  None, "dist"),
    ("report_type", "barh", None, "dist"),
    ("country",     "barh", 12,   "dist"),
    ("age",         "col",  None, "dist"),
    ("year",        "line", None, "dist"),
    ("reaction",    "barh", 15,   "dist"),
    ("indication",  "barh", 12,   "dist"),
    ("drug_role",   "barh", None, "dist"),
]
NOTE_KEYS = {
    "country": "top12", "reaction": "top15", "indication": "top12",
    "age": "age", "year": "year", "drug_role": "role",
}

# fixed age-bin order (years, normalized)
AGE_BINS = ["0-17", "18-44", "45-64", "65-74", "75+"]


def SHEET_SUMMARY():
    return t("xlsx.sheet.summary")


def _block_label(key):
    """First-column / x-axis category label for a distribution key."""
    return t("xlsx.safety.label." + key)


# ═══════════════════════════════════════════════════════════════════════════
# Format factory
# ═══════════════════════════════════════════════════════════════════════════
def _make_formats(wb):
    f = {}
    f["title"] = wb.add_format({"bold": True, "font_size": 16, "font_color": "white",
                                "bg_color": BANNER, "align": "center", "valign": "vcenter",
                                "font_name": FONT})
    f["cover"] = wb.add_format({"bold": True, "font_size": 18, "font_color": "white",
                                "bg_color": BANNER, "align": "center", "valign": "vcenter",
                                "font_name": FONT})
    f["sub"] = wb.add_format({"bold": True, "font_size": 11, "font_color": DARKRED,
                              "font_name": FONT, "align": "left", "valign": "vcenter"})
    f["body"] = wb.add_format({"font_size": 10, "font_name": FONT, "valign": "top",
                               "text_wrap": True})
    f["body_c"] = wb.add_format({"font_size": 10, "font_name": FONT, "align": "center",
                                 "valign": "vcenter", "text_wrap": True})
    f["note"] = wb.add_format({"italic": True, "font_size": 9, "font_color": GREYTX,
                               "font_name": FONT, "valign": "vcenter"})
    f["header"] = wb.add_format({"bold": True, "font_color": "white", "bg_color": DARKRED,
                                 "align": "center", "valign": "vcenter", "border": 1,
                                 "border_color": GRID, "font_name": FONT, "text_wrap": True})
    f["zebra"] = wb.add_format({"bg_color": LIGHTRED, "border": 1, "border_color": GRID,
                                "font_name": FONT, "font_size": 10, "valign": "top",
                                "text_wrap": True})
    f["plain"] = wb.add_format({"border": 1, "border_color": GRID, "font_name": FONT,
                                "font_size": 10, "valign": "top", "text_wrap": True})
    f["sumrow"] = wb.add_format({"bold": True, "font_color": DARKRED, "bg_color": "#F5B7B1",
                                 "border": 1, "border_color": GRID, "font_name": FONT,
                                 "font_size": 10, "align": "right", "valign": "vcenter"})
    f["left"] = wb.add_format({"align": "left", "valign": "top", "text_wrap": True,
                               "border": 1, "border_color": GRID, "font_name": FONT,
                               "font_size": 10})
    f["right"] = wb.add_format({"align": "right", "valign": "vcenter", "border": 1,
                                "border_color": GRID, "font_name": FONT, "font_size": 10})
    f["center"] = wb.add_format({"align": "center", "valign": "vcenter", "border": 1,
                                 "border_color": GRID, "font_name": FONT, "font_size": 10})
    f["pct"] = wb.add_format({"align": "right", "valign": "vcenter", "border": 1,
                              "border_color": GRID, "font_name": FONT, "font_size": 10,
                              "num_format": "0.0%"})
    f["kpi_label"] = wb.add_format({"bold": True, "font_color": "white", "bg_color": CARDHEAD,
                                    "align": "center", "valign": "vcenter", "font_name": FONT,
                                    "font_size": 10, "text_wrap": False})
    f["kpi_value"] = wb.add_format({"bold": True, "font_color": DARKRED, "bg_color": CARDBODY,
                                    "align": "center", "valign": "vcenter", "font_name": FONT,
                                    "font_size": 22})
    f["kpi_sub"] = wb.add_format({"italic": True, "font_color": GREYTX, "bg_color": CARDBODY,
                                  "align": "center", "valign": "vcenter", "font_name": FONT,
                                  "font_size": 9})
    f["warn"] = wb.add_format({"bg_color": WARNBG, "border": 2, "border_color": WARNBD,
                               "font_size": 10, "font_color": "#7F6000", "text_wrap": True,
                               "valign": "vcenter", "font_name": FONT})
    f["block_title"] = wb.add_format({"bold": True, "font_color": "white", "bg_color": DARKRED,
                                      "align": "center", "valign": "vcenter", "border": 1,
                                      "border_color": GRID, "font_name": FONT, "font_size": 11})
    f["note_r"] = wb.add_format({"italic": True, "font_size": 9, "font_color": GREYTX,
                                 "font_name": FONT, "align": "right", "valign": "vcenter"})
    f["divider"] = wb.add_format({"bg_color": LIGHTRED})  # thin section separator band
    # README provenance line: explicit left-align, NO wrap → overflows into empty cells
    f["prov"] = wb.add_format({"font_size": 10, "font_name": FONT, "font_color": GREYTX,
                                "align": "left", "valign": "vcenter"})
    # README scope value: explicit LEFT align (Excel right-aligns bare numbers otherwise)
    f["body_l"] = wb.add_format({"font_size": 10, "font_name": FONT, "valign": "top",
                                  "align": "left", "text_wrap": True})
    # raw-sheet: right-aligned numeric column + monospace ID column
    f["raw_num"] = wb.add_format({"align": "right", "valign": "top", "font_name": FONT,
                                  "font_size": 10})
    f["raw_mono"] = wb.add_format({"align": "left", "valign": "top", "font_name": "Consolas",
                                    "font_size": 10})
    return f


# ---- low-level styling helpers ---------------------------------------------
# _banner / _page_decor / _kpi_card are imported from vendored excel_style.


# ---- chart factory ----------------------------------------------------------
# _add_chart is imported from vendored excel_style (_style_series / _pie_points
# stay local — they carry the medical-red chart theming).


def _style_series(chart_type, labels):
    lbl_font = {"size": 9, "font_name": FONT, "color": "#7B241C", "bold": False}
    opts = {"data_labels": {"value": True, "font": lbl_font}}
    if chart_type == "pie":
        opts = {"data_labels": {"percentage": True, "category": True,
                                "num_format": "0.0%", "font": lbl_font}, "gap": 55}
    if chart_type in ("col", "barh"):
        opts["gap"] = 55
        opts["fill"] = {"color": RED}   # unify bar/column charts to medical-red theme
    if chart_type == "line":
        opts["line"] = {"color": RED, "width": 2.25}
        opts["marker"] = {"type": "circle", "size": 6,
                          "fill": {"color": RED}, "border": {"color": DARKRED}}
    return opts


def _pie_points(key):
    """Semantic per-slice colors for pie charts (None = Excel default)."""
    if key == "serious":
        # order from prepare_dists: serious(1) first, then non-serious
        return [{"fill": {"color": RED}}, {"fill": {"color": "#27AE60"}}]
    if key == "sex":
        # order: male, female, unknown
        return [{"fill": {"color": "#2E86C1"}},
                {"fill": {"color": "#E74C8E"}},
                {"fill": {"color": "#BFC9CA"}}]
    return None


# _chart_h / _chart_w are imported from vendored excel_style.


# ═══════════════════════════════════════════════════════════════════════════
# Distribution block: LEFT data table + RIGHT native chart
# ═══════════════════════════════════════════════════════════════════════════
def _render_dist_block(ws, row0, key, title, chart_type, cmax, note_key, dists, fmts, wb):
    items = dists.get(key, [])
    if not items:
        return row0
    total = sum(c for _, c in items) or 1

    ws.merge_range(row0, 0, row0, 6, title, fmts["block_title"])  # extend title across table+chart band
    hdr = row0 + 1
    ws.write(hdr, 0, _block_label(key), fmts["header"])
    ws.write(hdr, 1, t("xlsx.safety.col.count"), fmts["header"])
    ws.write(hdr, 2, t("xlsx.col.share"), fmts["header"])

    r = hdr + 1
    for label, cnt in items:
        zebra = ((r - hdr) % 2 == 1)
        ws.write(r, 0, label if label else t("xlsx.unknown"),
                 fmts["zebra"] if zebra else fmts["plain"])
        ws.write(r, 1, cnt, fmts["right"])
        ws.write(r, 2, cnt / total, fmts["pct"])
        r += 1
    last = r - 1

    ws.write(last + 1, 0, t("xlsx.total"), fmts["sumrow"])
    ws.write(last + 1, 1, total, fmts["sumrow"])
    ws.write(last + 1, 2, 1.0, fmts["pct"])
    sum_row = last + 1

    if last >= hdr + 1:
        ws.conditional_format(hdr + 1, 2, last, 2,
                              {"type": "data_bar", "bar_color": RED})

    # native chart on the right (column E). Height ADAPTS to the table height.
    # FIX: value range starts at FIRST DATA row (hdr+1), not the header row.
    last_ch = last if not cmax else min(last, hdr + cmax)
    n_rows = last - hdr
    h = _chart_h(n_rows)
    w = h if chart_type == "pie" else _chart_w(h)
    ch = _add_chart(wb, chart_type, title, w, h)
    cats = [SHEET_SUMMARY(), hdr + 1, 0, last_ch, 0]
    vals = [SHEET_SUMMARY(), hdr + 1, 1, last_ch, 1]
    pts = _pie_points(key) if chart_type == "pie" else None
    ch.add_series({"categories": cats, "values": vals,
                   "points": pts or [], **_style_series(chart_type, True)})
    if chart_type == "line":
        ch.set_x_axis({"name": _block_label(key), "name_font": {"font_name": FONT}})
        ch.set_y_axis({"name": t("xlsx.safety.col.count"), "name_font": {"font_name": FONT}})
    ws.insert_chart(f"{CHART_COL}{hdr + 1}", ch)

    if note_key:
        ws.write(sum_row + 2, 0, "· " + t("xlsx.safety.note." + note_key), fmts["note"])

    note_row = sum_row + 2 if note_key else last
    table_bottom = max(last, note_row)
    chart_bottom = row0 + (h // ROW_PX)
    return max(table_bottom, chart_bottom) + BAND_GAP


# ═══════════════════════════════════════════════════════════════════════════
# Data aggregation (pure step, no IO)
# ═══════════════════════════════════════════════════════════════════════════
def _split(text):
    return [p.strip() for p in (text or "").split(";") if p.strip()]


def _age_to_years(age, unit):
    try:
        a = float(age)
    except (TypeError, ValueError):
        return None
    u = (unit or "").strip().upper()
    factor = {"YR": 1.0, "Y": 1.0, "MON": 1 / 12.0, "M": 1 / 12.0,
              "WK": 7 / 365.0, "W": 7 / 365.0, "DY": 1 / 365.0, "D": 1 / 365.0,
              "HR": 1 / 8760.0, "H": 1 / 8760.0, "DEC": 10.0}.get(u)
    return a * factor if factor is not None else None


def _age_bin(y):
    if y is None:
        return None
    if y < 18:
        return "0-17"
    if y < 45:
        return "18-44"
    if y < 65:
        return "45-64"
    if y < 75:
        return "65-74"
    return "75+"


def _sex_label(code):
    return {"1": t("xlsx.safety.sex_m"), "2": t("xlsx.safety.sex_f")}.get(
        str(code).strip(), t("xlsx.safety.sex_unknown"))


def _serious_label(val):
    return t("xlsx.safety.serious_yes") if str(val).strip() == "1" \
        else t("xlsx.safety.serious_no")


def _rt_label(code):
    return {"1": t("xlsx.safety.rt_initial"), "2": t("xlsx.safety.rt_followup")}.get(
        str(code).strip(), t("xlsx.safety.rt_unknown"))


def _role_label(code):
    return {"1": t("xlsx.safety.role_suspect"), "2": t("xlsx.safety.role_concomitant"),
            "3": t("xlsx.safety.role_interaction")}.get(
        str(code).strip(), t("xlsx.safety.rt_unknown"))


def prepare_dists(rows):
    """Compute all FAERS summary distributions from a flattened case list."""
    serious = Counter()
    sex = Counter()
    rtype = Counter()
    country = Counter()
    age_counter = Counter()
    year = Counter()
    reaction = Counter()
    indication = Counter()
    role = Counter()
    ages = []

    for r in rows:
        serious[_serious_label(r.get("serious"))] += 1
        sex[_sex_label(r.get("patientsex"))] += 1
        rtype[_rt_label(r.get("reporttype"))] += 1
        cc = (r.get("primarysourcecountry") or "").strip()
        if cc:
            country[cc] += 1
        y = _age_to_years(r.get("patientage"), r.get("patientageunit"))
        if y is not None:
            ages.append(y)
            b = _age_bin(y)
            if b:
                age_counter[b] += 1
        rd = (r.get("receivedate") or "").strip()
        if len(rd) >= 4 and rd[:4].isdigit():
            year[rd[:4]] += 1
        for p in _split(r.get("reaction_pts")):
            reaction[p] += 1
        for p in _split(r.get("drug_indications")):
            indication[p] += 1
        for c in _split(r.get("drug_characterizations")):
            role[_role_label(c)] += 1

    age_items = [(b, age_counter.get(b, 0)) for b in AGE_BINS]
    year_items = sorted(year.items())
    country_items = country.most_common(12)
    reaction_items = reaction.most_common(15)
    indication_items = indication.most_common(12)

    median_age = round(statistics.median(ages), 1) if ages else None
    year_span = "%s–%s" % (year_items[0][0], year_items[-1][0]) if year_items else "—"

    # KPI helpers
    total = len(rows) or 1
    n_serious = sum(1 for r in rows if str(r.get("serious", "")).strip() == "1")
    n_male = sex.get(t("xlsx.safety.sex_m"), 0)
    n_female = sex.get(t("xlsx.safety.sex_f"), 0)

    kpis = {
        "n_serious": n_serious,
        "median_age": median_age,
        "year_span": year_span,
        "serious_rate": (n_serious / total) if total else 0.0,
        "male_pct": (n_male / total) if total else 0.0,
        "female_pct": (n_female / total) if total else 0.0,
    }

    return {
        "serious": serious.most_common(),
        "sex": sex.most_common(),
        "report_type": rtype.most_common(),
        "country": country_items,
        "age": age_items,
        "year": year_items,
        "reaction": reaction_items,
        "indication": indication_items,
        "drug_role": role.most_common(),
        "kpis": kpis,
    }


def prepare_dists_from_facets(facets, total_matching=0):
    """Build the SAME `dists` shape as prepare_dists, but from openFDA count
    facets (fast mode). `facets` = {key: [{"term","count"}, ...]}.
    Age is NOT count-able via the API → omitted (empty list)."""
    s_yes = s_no = 0
    for x in facets.get("serious", []):
        if str(x.get("term", "")).strip() == "1":
            s_yes += int(x.get("count", 0) or 0)
        else:
            s_no += int(x.get("count", 0) or 0)
    serious = [(_serious_label("1"), s_yes), (_serious_label("2"), s_no)]

    sex = [(_sex_label(x.get("term")), int(x.get("count", 0) or 0))
           for x in facets.get("sex", [])]
    rtype = [(_rt_label(x.get("term")), int(x.get("count", 0) or 0))
             for x in facets.get("report_type", [])]
    country = [(x.get("term"), int(x.get("count", 0) or 0))
               for x in facets.get("country", [])][:12]

    yr = Counter()
    for x in facets.get("year", []):
        # openFDA returns receivedate counts under the `time` key (not `term`)
        term = x.get("term") or x.get("time") or ""
        if len(term) >= 4 and term[:4].isdigit():
            yr[term[:4]] += int(x.get("count", 0) or 0)
    year = sorted(yr.items())

    reaction = [(x.get("term"), int(x.get("count", 0) or 0))
                for x in facets.get("reaction", [])][:15]
    indication = [(x.get("term"), int(x.get("count", 0) or 0))
                  for x in facets.get("indication", [])][:12]
    role = [(_role_label(x.get("term")), int(x.get("count", 0) or 0))
            for x in facets.get("drug_role", [])]

    total = total_matching or 1
    n_serious = s_yes
    sex_map = dict(sex)
    n_male = sex_map.get(t("xlsx.safety.sex_m"), 0)
    n_female = sex_map.get(t("xlsx.safety.sex_f"), 0)
    kpis = {
        "n_serious": n_serious,
        "median_age": None,  # count mode can't recover age (unit ambiguity) → "—"
        "year_span": "%s–%s" % (year[0][0], year[-1][0]) if year else "—",
        "serious_rate": (n_serious / total) if total else 0.0,
        "male_pct": (n_male / total) if total else 0.0,
        "female_pct": (n_female / total) if total else 0.0,
    }
    return {
        "serious": serious,
        "sex": sex,
        "report_type": rtype,
        "country": country,
        "age": [],            # unavailable in count mode
        "year": year,
        "reaction": reaction,
        "indication": indication,
        "drug_role": role,
        "kpis": kpis,
    }


# ═══════════════════════════════════════════════════════════════════════════
# Sheet builders
# ═══════════════════════════════════════════════════════════════════════════
def build_readme(wb, rows, dists, meta, fmts):
    ws = wb.add_worksheet(t("xlsx.sheet.readme"))
    # uniform 15-col grid (11px each) → KPI cards (3 cols) are equal width;
    # scope labels use a 3-col merge, value uses the remaining 12 cols.
    ws.set_column(0, 14, 11)
    _page_decor(ws, t("xlsx.safety.doc_title"), fmts)
    _banner(ws, 0, 0, 14, t("xlsx.safety.banner"), fmts)
    # top-right brand mark (shared standard; image is optional, skipped if absent)
    _logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                         "assets", "ct-safety_4x.png")
    cover_logo(ws, _logo, col=14, scale=0.16, x_offset=20, y_offset=2)
    # provenance + timestamp: anchored at the LEFTMOST cell (col 0), left-aligned,
    # no wrap → overflows into the empty cells to its right (full sentence visible).
    ws.write(1, 0,
             "%s: %s" % (t("xlsx.safety.cover.generated"),
                         datetime.now().strftime("%Y-%m-%d %H:%M")),
             fmts["prov"])

    k = dists["kpis"]
    total = len(rows)
    fast = meta.get("mode") == "fast"
    # KPI cards — row 3 (×4) and row 7 (×4); set row heights so big value fits
    for rr in (3, 7):
        ws.set_row(rr, 18)      # label
    for rr in (4, 8):
        ws.set_row(rr, 34)      # value (22pt)
    for rr in (5, 9):
        ws.set_row(rr, 14)      # sub
    # first card: in fast/count mode it's the FULL analyzed population, not a download count
    if fast:
        _kpi_card(ws, 3, 0, t("xlsx.safety.kpi.population"), meta.get("total_matching", 0),
                  t("xlsx.safety.kpi.population_sub"), fmts)
    else:
        _kpi_card(ws, 3, 0, t("xlsx.safety.kpi.downloaded"), total,
                  t("xlsx.safety.kpi.downloaded_sub"), fmts)
    _kpi_card(ws, 3, 4, t("xlsx.safety.kpi.total"), meta.get("total_matching", 0),
              t("xlsx.safety.kpi.total_sub"), fmts)
    _kpi_card(ws, 3, 8, t("xlsx.safety.kpi.serious"),
              k.get("n_serious", dists["serious"][0][1] if dists["serious"] else 0),
              t("xlsx.safety.kpi.serious_sub"), fmts)
    _kpi_card(ws, 3, 12, t("xlsx.safety.kpi.serious_rate"),
              "%.1f%%" % (k["serious_rate"] * 100),
              t("xlsx.safety.kpi.serious_rate_sub"), fmts)
    _kpi_card(ws, 7, 0, t("xlsx.safety.kpi.male"),
              "%.0f%%" % (k["male_pct"] * 100), t("xlsx.safety.sex_m"), fmts)
    _kpi_card(ws, 7, 4, t("xlsx.safety.kpi.female"),
              "%.0f%%" % (k["female_pct"] * 100), t("xlsx.safety.sex_f"), fmts)
    _kpi_card(ws, 7, 8, t("xlsx.safety.kpi.median_age"),
              k["median_age"] if k["median_age"] is not None else "—",
              t("xlsx.safety.kpi.median_age_sub"), fmts)
    _kpi_card(ws, 7, 12, t("xlsx.safety.kpi.year_span"),
              k["year_span"], t("xlsx.safety.kpi.year_span_sub"), fmts)

    # thin section separator band between KPI area and scope
    ws.set_row(11, 6)
    ws.merge_range(11, 0, 11, 14, "", fmts["divider"])

    # scope info cards
    r = 12
    ws.write(r, 0, t("xlsx.readme.scope_title"), fmts["sub"])
    r += 1
    info = [
        (t("xlsx.safety.scope.drug"), meta.get("drug", "—")),
        (t("xlsx.safety.scope.field"), meta.get("field", "—")),
        (t("xlsx.safety.scope.date"),
         "%s ~ %s" % (meta.get("date_from") or "—", meta.get("date_to") or "—")),
        (t("xlsx.safety.scope.source"), t("xlsx.safety.scope.source_val")),
        (t("xlsx.safety.scope.total"), meta.get("total_matching", 0)),
        (t("xlsx.safety.scope.downloaded"),
         t("xlsx.safety.scope.downloaded_fast") if fast
         else "%s / cap %s" % (total, meta.get("hard_cap", 10000))),
    ]
    if fast:
        info.append((t("xlsx.safety.scope.mode"), t("xlsx.safety.mode_fast")))
    for kk, vv in info:
        ws.merge_range(r, 0, r, 2, kk, fmts["kpi_label"])   # 3-col label cell
        ws.merge_range(r, 3, r, 14, vv, fmts["body_l"])     # value spans remaining 12 cols (left-aligned)
        r += 1

    # data caveat callout
    r += 1
    ws.merge_range(r, 0, r + 3, 14, t("xlsx.safety.caveat"), fmts["warn"])

    # subtle brand watermark in the lower empty area (offline-safe: textbox, no image)
    ws.insert_textbox(24, 0, t("xlsx.safety.watermark"),
                      {"width": 760, "height": 90,
                       "font": {"color": "#F2F2F2", "size": 44, "bold": True,
                                "font_name": FONT},
                       "fill": {"none": True}, "line": {"none": True}})


def build_summary(wb, dists, fmts, fast=False):
    ws = wb.add_worksheet(SHEET_SUMMARY())
    # 分布表列宽：类别列加宽（表单不再过窄），计数/占比列适中
    ws.set_column(0, 0, 24)
    ws.set_column(1, 1, 12)
    ws.set_column(2, 2, 10)
    _page_decor(ws, t("xlsx.safety.doc_title"), fmts)
    _banner(ws, 0, 0, 12, t("xlsx.safety.banner"), fmts)
    intro = t("xlsx.safety.summary_intro_fast") if fast else t("xlsx.safety.summary_intro")
    ws.merge_range(1, 0, 1, 12, intro, fmts["note"])

    row = 3
    for key, ctype, cmax, _kind in SAFETY_BLOCKS:
        # count mode can't produce age → note instead of an empty block
        if key == "age" and not dists.get("age"):
            ws.merge_range(row, 0, row, 12,
                           "· " + t("xlsx.safety.note.age_skip_fast"), fmts["note"])
            row += 2
            continue
        note = NOTE_KEYS.get(key)
        row = _render_dist_block(
            ws, row, key, t("xlsx.safety.block." + key), ctype, cmax, note, dists, fmts, wb)

    # bottom caveat
    ws.merge_range(row + 1, 0, row + 4, 12, t("xlsx.safety.caveat"), fmts["warn"])


def export_workbook(rows, out_path, meta=None, lang="auto", dists=None):
    """Render the 3-sheet FAERS workbook and save to ``out_path``.
    `dists` may be pre-supplied (fast/count mode); otherwise computed from rows."""
    if xlsxwriter is None:
        raise RuntimeError("xlsxwriter not installed: pip install xlsxwriter")
    # Always resolve explicitly — never leave "auto" to the server OS locale.
    set_lang(resolve_report_lang(lang, skill="safety"))
    meta = meta or {}
    if dists is None:
        dists = prepare_dists(rows)
    fast = meta.get("mode") == "fast"

    wb = xlsxwriter.Workbook(out_path)
    fmts = _make_formats(wb)
    build_readme(wb, rows, dists, meta, fmts)
    build_summary(wb, dists, fmts, fast=fast)
    build_case_details(wb, fmts, rows)  # unified per-case sheet (mirrors report_xlsx)
    wb.close()
    return dists


def main():
    ap = argparse.ArgumentParser(description="Export FAERS cases to .xlsx (README+Summary+Raw).")
    ap.add_argument("--in-csv", required=True, help="flattened CSV of cases (one row per report)")
    ap.add_argument("--out", required=True, help="output .xlsx path")
    ap.add_argument("--drug", default="")
    ap.add_argument("--field", default="patient.drug.medicinalproduct")
    ap.add_argument("--date-from")
    ap.add_argument("--date-to")
    ap.add_argument("--total", type=int, default=0, help="total matching reports in FAERS")
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"],
                    help="report UI language (auto = CT_SAFETY_LANG / config / "
                         "default zh, NEVER the server OS locale; en forces English)")
    args = ap.parse_args()

    import csv
    rows = []
    with open(args.in_csv, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            rows.append(dict(r))
    meta = {"drug": args.drug, "field": args.field, "date_from": args.date_from,
            "date_to": args.date_to, "total_matching": args.total, "hard_cap": 10000}
    export_workbook(rows, args.out, meta=meta, lang=args.lang)
    print("[OK] wrote", args.out, "(%d cases)" % len(rows))


if __name__ == "__main__":
    main()
