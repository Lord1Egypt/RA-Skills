#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
report_xlsx.py / 信号分析数据工作簿

Build the FAERS signal-analysis .xlsx companion workbook (xlsxwriter).

This is one of the TWO core deliverables (alongside faers_report.html):
it holds ALL raw information — FAERS counts, the 2x2 table, the four
disproportionality measures, supporting sources (FDA Label / CN-PV) and the
composite score — so every number can be audited. Pure local; no network.

Layout (modeled on ct-literature/export_xlsx.py):
  - README  : banner + logo (top-right) + KPI cards + guide (2-col layout)
  - Summary : meta block + 2×2 table + disproportionality table
  - Raw_Counts : fetch metadata + raw 2×2 + disproportionality input + top events
  - FDA_Label / CN_PV / Score : conditional sheets

Bilingual: all UI chrome goes through ``i18n.t()`` (keys ``xlsx.signal.*``).
On a Chinese OS the workbook renders in Chinese; on an English OS, English.
Raw data values (drug names, PT terms, counts) are NEVER translated.

Usage (inside ct_safety.py):
    import report_xlsx
    report_xlsx.build_signal_xlsx(out_path, drug=drug, event=event,
                                  fetch_data=data, disp_res=res,
                                  cn_pv=cn_pv, label_data=label_data,
                                  label_status=label_status, score_res=score_res)
"""
import os
import sys
import json

import xlsxwriter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import disproportionality
from excel_style import (make_formats, banner, page_decor, kpi_card, cover_logo,
                        PALETTES, HEADER_H, BANNER_H)
from i18n import t, set_lang

# 阶段 2：交付语言解析统一走 ct-base 共享件（单一真源，publish_inject 注入本目录）。
from xlsx_delivery import resolve_report_lang
from xlsx_sheets import build_case_details as _build_case_details  # noqa: E402

PAL = PALETTES["safety"]
_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOGO = os.path.join(_SKILL_DIR, "assets", "icon_4x.png")

# Column grid: 10 columns (0–9), col 0 = label, cols 1–9 = content
_NCOL = 10
_LOGO_COL = _NCOL - 1   # column 9 — rightmost


def _soc(event):
    try:
        return disproportionality.map_soc(event) if event else "—"
    except Exception:
        return "—"


def _section(ws, r, c1, c2, text, fmts):
    """A full-width navy block title for a sub-section."""
    ws.merge_range(r, c1, r, c2, text, fmts["block_title"])
    return r + 1


def _table(ws, r, fmts, headers, rows, c0=0, zebra=True, first_is_key=True,
           stretch=None):
    """Write a themed header (HEADER_H) + zebra data rows.

    When ``first_is_key`` the first column is rendered as a bold key cell.
    ``stretch`` stretches the table to the full 10-col page width:
      - "last":  the last column is merged out to col 9
      - "first": the first column is merged c0..8 and the last col sits at col 9
    Skips autofilter when stretched (merged cells break filtering).
    Returns (next_row, header_row, data_first, data_last) so the caller can
    attach an autofilter.
    """
    ncol = len(headers)
    c_end = _NCOL - 1
    ws.set_row(r, HEADER_H)
    if stretch == "first" and ncol == 2:
        ws.merge_range(r, c0, r, c_end - 1, headers[0], fmts["header"])
        ws.write(r, c_end, headers[1], fmts["header"])
    elif stretch == "last":
        for ci, h in enumerate(headers[:-1]):
            ws.write(r, c0 + ci, h, fmts["header"])
        ws.merge_range(r, c0 + ncol - 1, r, c_end, headers[-1], fmts["header"])
    else:
        for ci, h in enumerate(headers):
            ws.write(r, c0 + ci, h, fmts["header"])
    hdr = r
    r += 1
    first = r
    for ri, row in enumerate(rows):
        z = zebra and (ri % 2 == 1)
        fmts_row = []
        for ci, val in enumerate(row):
            if ci == 0 and first_is_key:
                fmt = fmts["fkey_z"] if z else fmts["fkey"]
            elif isinstance(val, (int, float)):
                fmt = fmts["right"]
            else:
                fmt = fmts["zebra"] if z else fmts["plain"]
            fmts_row.append(fmt)
        if stretch == "first" and ncol == 2:
            ws.merge_range(r, c0, r, c_end - 1, str(row[0]), fmts_row[0])
            v = row[1]
            if isinstance(v, (int, float)):
                ws.write_number(r, c_end, v, fmts_row[1])
            else:
                ws.write(r, c_end, v, fmts_row[1])
        elif stretch == "last":
            for ci, val in enumerate(row[:-1]):
                if isinstance(val, (int, float)):
                    ws.write_number(r, c0 + ci, val, fmts_row[ci])
                else:
                    ws.write(r, c0 + ci, val, fmts_row[ci])
            v = row[-1]
            if isinstance(v, (int, float)):
                ws.write_number(r, c0 + ncol - 1, v, fmts_row[-1])
                ws.merge_range(r, c0 + ncol - 1, r, c_end, v, fmts_row[-1])
            else:
                ws.merge_range(r, c0 + ncol - 1, r, c_end, str(v), fmts_row[-1])
        else:
            for ci, val in enumerate(row):
                col = c0 + ci
                if isinstance(val, (int, float)):
                    ws.write_number(r, col, val, fmts_row[ci])
                else:
                    ws.write(r, col, val, fmts_row[ci])
        r += 1
    last = r - 1
    return r, hdr, first, last


def _set_grid(ws, label_w=18, body_w=12):
    """Apply the standard 10-col grid: col 0 = label, cols 1–9 = body."""
    ws.set_column(0, 0, label_w)
    for c in range(1, _NCOL):
        ws.set_column(c, c, body_w)


# ════════════════════════════════════════════════════════════════════
# README (cover)
# ════════════════════════════════════════════════════════════════════
def _build_readme(wb, fmts, drug, event, disp_res):
    ws = wb.add_worksheet(t("xlsx.signal.sheet.readme"))
    _set_grid(ws, label_w=18, body_w=12)
    page_decor(ws, t("xlsx.signal.banner"), fmts)

    # Row 0: banner (full width)
    banner(ws, 0, 0, _NCOL - 1,
           "%s · %s" % (t("xlsx.signal.banner"), t("xlsx.signal.banner.data_workbook")),
           fmts, height=BANNER_H)

    # Logo right-flush inside column J (col 9):
    # J width 13 units = 13*7+5 = 96px; image 416*0.16 = 66.5px
    # x_offset = 96 - 66.5 - 4(padding) ≈ 25px → right edge aligns with J's right border
    ws.set_column(_LOGO_COL, _LOGO_COL, 13)
    cover_logo(ws, _LOGO, col=_LOGO_COL, scale=0.16, x_offset=25, y_offset=2)

    # Row 1: KPI cards (3 cards × 3 cols each = 9 cols, starting at col 0)
    verdict = t("xlsx.signal.verdict.positive") if (disp_res or {}).get("signal_overall") \
        else t("xlsx.signal.verdict.negative")
    kpi_card(ws, 2, 0, t("xlsx.signal.kpi.drug"), drug or "?", None, fmts)
    kpi_card(ws, 2, 3, t("xlsx.signal.kpi.event"), event or "?", None, fmts)
    kpi_card(ws, 2, 6, t("xlsx.signal.kpi.verdict"), verdict, None, fmts)
    ws.set_row(2, 18)   # label
    ws.set_row(3, 32)   # value
    ws.set_row(4, 14)   # sub

    # Row 6: guide title
    r = 6
    ws.merge_range(r, 0, r, _NCOL - 1, t("xlsx.signal.guide.title"), fmts["sub"])
    r += 1

    # Guide items: 2-col layout (label | value), matching ct-literature style
    guide_items = [
        ("html", t("xlsx.signal.guide.html")),
        ("xlsx", t("xlsx.signal.guide.xlsx")),
    ]
    for i, (key, text) in enumerate(guide_items):
        zebra = (i % 2 == 1)
        ws.merge_range(r, 0, r, 2, "①" if i == 0 else "②",
                       fmts["fkey_z"] if zebra else fmts["fkey"])
        ws.merge_range(r, 3, r, _NCOL - 1, text,
                       fmts["zebra"] if zebra else fmts["plain"])
        ws.set_row(r, 16)
        r += 1

    # Sheets description
    r += 1
    ws.merge_range(r, 0, r, _NCOL - 1, t("xlsx.signal.guide.sheets"), fmts["sub"])
    r += 1
    sheets = [
        t("xlsx.signal.guide.summary"),
        t("xlsx.signal.guide.raw"),
        t("xlsx.signal.guide.cases"),
        t("xlsx.signal.guide.label"),
        t("xlsx.signal.guide.cnpv"),
        t("xlsx.signal.guide.score"),
    ]
    for i, s in enumerate(sheets):
        zebra = (i % 2 == 1)
        ws.merge_range(r, 0, r, _NCOL - 1, "  • " + s,
                       fmts["zebra"] if zebra else fmts["plain"])
        ws.set_row(r, 14)
        r += 1

    # Source caveat
    r += 1
    ws.merge_range(r, 0, r + 1, _NCOL - 1, t("xlsx.signal.guide.source"), fmts["note"])
    ws.set_row(r, 14)
    ws.set_row(r + 1, 14)

    ws.freeze_panes(1, 0)
    return ws


# ════════════════════════════════════════════════════════════════════
# Summary
# ════════════════════════════════════════════════════════════════════
def _build_summary(wb, fmts, drug, event, fetch_data, disp_res):
    ws = wb.add_worksheet(t("xlsx.signal.sheet.summary"))
    _set_grid(ws, label_w=18, body_w=12)  # total 126 units — same as README
    page_decor(ws, t("xlsx.signal.banner"), fmts)

    banner(ws, 0, 0, _NCOL - 1, t("xlsx.signal.sheet.summary"), fmts, height=BANNER_H)
    r = 2

    # ── Meta block ──
    meta = [
        (t("xlsx.signal.meta.drug"), drug),
        (t("xlsx.signal.meta.event"), event),
        (t("xlsx.signal.meta.soc"), _soc(event)),
        (t("xlsx.signal.meta.source"), t("xlsx.signal.source.faers")),
        (t("xlsx.signal.meta.continuity"),
         t("xlsx.signal.meta.enabled") if (disp_res or {}).get("continuity") else t("xlsx.signal.meta.no")),
        (t("xlsx.signal.meta.overall"),
         t("xlsx.signal.verdict.short.positive") if (disp_res or {}).get("signal_overall")
         else t("xlsx.signal.verdict.short.negative")),
    ]
    for i, (k, v) in enumerate(meta):
        zebra = (i % 2 == 1)
        ws.write(r, 0, k, fmts["fkey_z"] if zebra else fmts["fkey"])
        ws.merge_range(r, 1, r, _NCOL - 1, v, fmts["zebra"] if zebra else fmts["plain"])
        ws.set_row(r, 16)
        r += 1

    r += 1
    r = _section(ws, r, 0, _NCOL - 1, t("xlsx.signal.section.2x2"), fmts)
    r += 1

    # ── 2×2 table ──
    cnt = (fetch_data or {}).get("counts") or {}
    a, b, c, d = cnt.get("a"), cnt.get("b"), cnt.get("c"), cnt.get("d")
    if a is not None:
        rows_2x2 = [
            [t("xlsx.signal.col.drug"), a, b, (a or 0) + (b or 0)],
            [t("xlsx.signal.col.no_drug"), c, d, (c or 0) + (d or 0)],
            [t("xlsx.signal.col.total"),
             (a or 0) + (c or 0), (b or 0) + (d or 0),
             (a or 0) + (b or 0) + (c or 0) + (d or 0)],
        ]
        nr, hdr, first, last = _table(
            ws, r, fmts,
            ["", t("xlsx.signal.col.event_yes"), t("xlsx.signal.col.event_no"), t("xlsx.signal.col.total")],
            rows_2x2, c0=0, zebra=True, first_is_key=True, stretch="last")
        r = nr

    r += 1
    r = _section(ws, r, 0, _NCOL - 1, t("xlsx.signal.section.measures"), fmts)
    r += 1

    # ── Disproportionality table (stretched to full page width) ──
    ws.set_row(r, HEADER_H)
    for ci, h in enumerate([t("xlsx.signal.col.method"), t("xlsx.signal.col.estimate"),
                            t("xlsx.signal.col.ci")]):
        ws.write(r, ci, h, fmts["header"])
    ws.merge_range(r, 3, r, _NCOL - 1, t("xlsx.signal.col.signal"), fmts["header"])
    hdr = r
    r += 1
    first = r
    if disp_res:
        for name, key in (("ROR", "ROR"), ("PRR", "PRR"), ("IC", "IC"), ("EBGM (MGPS)", "EBGM")):
            m = disp_res.get(key) or {}
            lo, hi = m.get("ci_low"), m.get("ci_high")
            ci_str = "%.3f – %.3f" % (lo, hi) if lo is not None else "—"
            sig = "✅" if m.get("signal") else "—"
            if name == "PRR" and m.get("chi2") is not None:
                sig += " (χ²=%.2f)" % m["chi2"]
            pos = bool(m.get("signal"))
            z = False
            ws.write(r, 0, name, fmts["fkey"])
            ws.write_number(r, 1, float(m["value"]), fmts["right"])
            ws.write(r, 2, ci_str, fmts["right"])
            ws.merge_range(r, 3, r, _NCOL - 1, sig,
                           fmts["block_title"] if pos else fmts["center"])
            r += 1
        last = r - 1
    # Grid already totals 126 units — same page width as README

    r += 1
    ws.merge_range(r, 0, r, _NCOL - 1, t("xlsx.signal.criteria"), fmts["note"])
    ws.set_row(r, 14)

    ws.freeze_panes(1, 0)
    return ws


# ════════════════════════════════════════════════════════════════════
# Raw_Counts
# ════════════════════════════════════════════════════════════════════
def _build_raw_counts(wb, fmts, fetch_data, disp_res):
    ws = wb.add_worksheet(t("xlsx.signal.sheet.raw"))
    _set_grid(ws, label_w=18, body_w=12)  # total 126 units — same as README
    page_decor(ws, t("xlsx.signal.banner"), fmts)

    banner(ws, 0, 0, _NCOL - 1, t("xlsx.signal.sheet.raw"), fmts, height=BANNER_H)
    r = 2

    # ── Fetch metadata ──
    fd = fetch_data or {}
    meta_rows = [
        ("source", fd.get("source")),
        ("api", fd.get("api")),
        ("drug", fd.get("drug")),
        ("field", fd.get("field")),
        ("date_from", fd.get("date_from")),
        ("date_to", fd.get("date_to")),
        ("drug_total", fd.get("drug_total")),
        ("event_total", fd.get("event_total")),
        ("grand_total", fd.get("grand_total")),
    ]
    for i, (k, v) in enumerate(meta_rows):
        zebra = (i % 2 == 1)
        ws.write(r, 0, k, fmts["fkey_z"] if zebra else fmts["fkey"])
        ws.merge_range(r, 1, r, _NCOL - 1,
                       "" if v is None else (v if isinstance(v, (int, float)) else str(v)),
                       fmts["zebra"] if zebra else fmts["plain"])
        ws.set_row(r, 16)
        r += 1

    r += 1
    r = _section(ws, r, 0, _NCOL - 1, t("xlsx.signal.section.raw2x2"), fmts)
    r += 1

    # ── Raw 2×2 (uncorrected) — stretched to full page width ──
    cnt = (fetch_data or {}).get("counts") or {}
    nr, hdr, first, last = _table(
        ws, r, fmts,
        [t("xlsx.signal.col.cell"), t("xlsx.signal.col.value")],
        [["a", cnt.get("a")], ["b", cnt.get("b")],
         ["c", cnt.get("c")], ["d", cnt.get("d")]],
        c0=0, zebra=True, first_is_key=True, stretch="last")
    r = nr

    # ── Raw counts (disproportionality input) ──
    rc = (disp_res or {}).get("raw_counts")
    if rc:
        r += 1
        r = _section(ws, r, 0, _NCOL - 1, t("xlsx.signal.section.raw_counts_input"), fmts)
        r += 1
        nr, hdr, first, last = _table(
            ws, r, fmts,
            [t("xlsx.signal.col.cell"), t("xlsx.signal.col.value")],
            [["a", rc.get("a")], ["b", rc.get("b")],
             ["c", rc.get("c")], ["d", rc.get("d")]],
            c0=0, zebra=True, first_is_key=True, stretch="last")
        r = nr

    # ── Top adverse events ──
    te = fd.get("top_events")
    if te:
        r += 1
        r = _section(ws, r, 0, _NCOL - 1, t("xlsx.signal.section.top_events"), fmts)
        r += 1
        rows = []
        if isinstance(te, list):
            for it in te:
                if isinstance(it, dict):
                    # {"term": "...", "count": N}
                    rows.append([str(it.get("term", "")), it.get("count", "")])
                elif isinstance(it, (list, tuple)) and len(it) == 2:
                    rows.append([str(it[0]), it[1]])
                else:
                    rows.append([str(it), ""])
        elif isinstance(te, dict):
            for kk, vv in te.items():
                rows.append([str(kk), vv])
        if rows:
            # Term column stretches to col 8, count sits at col 9 (full page width)
            nr, hdr, first, last = _table(
                ws, r, fmts,
                [t("xlsx.signal.col.event"), t("xlsx.signal.col.count")],
                rows, c0=0, zebra=True, first_is_key=True, stretch="first")
            r = nr

    ws.freeze_panes(1, 0)
    return ws
# ════════════════════════════════════════════════════════════════════
# FDA_Label
# ════════════════════════════════════════════════════════════════════
def _build_fda_label(wb, fmts, label_data, label_status, event):
    ws = wb.add_worksheet(t("xlsx.signal.sheet.label"))
    # 2-col layout: col 0 = label, cols 1-9 = content (B-J merged)
    # Total 126 units — same page width as README (30 + 9×10.67)
    ws.set_column(0, 0, 30)
    ws.set_column(1, _NCOL - 1, 10.67)
    page_decor(ws, t("xlsx.signal.banner"), fmts)

    banner(ws, 0, 0, _NCOL - 1, t("xlsx.signal.sheet.label"), fmts, height=BANNER_H)
    r = 2

    # Status row: label in A, value merged B-J
    ws.merge_range(r, 0, r, 1, t("xlsx.signal.label.status"), fmts["fkey"])
    ws.merge_range(r, 2, r, _NCOL - 1, label_status or "—", fmts["plain"])
    ws.set_row(r, 16)
    r += 2

    matched = label_data.get("matched_drug_terms")
    if matched:
        ws.merge_range(r, 0, r, 1, t("xlsx.signal.label.matched"), fmts["fkey"])
        ws.merge_range(r, 2, r, _NCOL - 1, ", ".join(matched), fmts["plain"])
        ws.set_row(r, 16)
        r += 2

    ev = (event or "").upper()

    def _sheet_block(title, items):
        nonlocal r
        r = _section(ws, r, 0, _NCOL - 1, title, fmts)
        r += 1
        # Write header (2 cols: # | Content merged B-J)
        ws.set_row(r, HEADER_H)
        ws.write(r, 0, t("xlsx.signal.col.n"), fmts["header"])
        ws.merge_range(r, 1, r, _NCOL - 1, t("xlsx.signal.col.content"), fmts["header"])
        hdr = r
        r += 1
        items = items or []
        if ev:
            hit = [x for x in items if ev in str(x).upper()]
            if hit:
                items = hit
        rr = r
        for i, it in enumerate(items[:50], 1):
            zebra = (i % 2 == 0)
            text = str(it)
            ws.write(rr, 0, i, fmts["zebra"] if zebra else fmts["plain"])
            ws.merge_range(rr, 1, rr, _NCOL - 1, text,
                           fmts["zebra"] if zebra else fmts["plain"])
            # Row height estimate for merged B-J (~96 units ≈ 675px).
            # Empirically calibrated: ~150 chars/line for 10-11pt Calibri English text.
            chars_per_line = 150
            lines = max(1, (len(text) + chars_per_line - 1) // chars_per_line)
            ws.set_row(rr, max(16, min(lines * 13.5, 900)))
            rr += 1
        if items:
            ws.autofilter(hdr, 0, rr - 1, _NCOL - 1)
        r = rr + 1

    _sheet_block(t("xlsx.signal.section.label_warnings"), label_data.get("warnings"))
    _sheet_block(t("xlsx.signal.section.label_reactions"), label_data.get("adverse_reactions"))
    ws.freeze_panes(1, 0)
    return ws


# ════════════════════════════════════════════════════════════════════
# CN_PV
# ════════════════════════════════════════════════════════════════════
def _build_cn_pv(wb, fmts, cn_pv):
    ws = wb.add_worksheet(t("xlsx.signal.sheet.cnpv"))
    widths = [11, 9, 14, 47, 14, 31]  # total 126 units — same as README
    for i, w in enumerate(widths):
        ws.set_column(i, i, w)
    page_decor(ws, t("xlsx.signal.banner"), fmts)

    banner(ws, 0, 0, 5, t("xlsx.signal.sheet.cnpv"), fmts, height=BANNER_H)
    r = 2

    ws.set_row(r, HEADER_H)
    for ci, h in enumerate([t("xlsx.signal.col.tier"), t("xlsx.signal.col.date"),
                            t("xlsx.signal.col.column"), t("xlsx.signal.col.title"),
                            t("xlsx.signal.col.kw"), t("xlsx.signal.col.link")]):
        ws.write(r, ci, h, fmts["header"])
    hdr = r
    r += 1
    first = r

    for h in cn_pv["hits"]:
        ws.write(r, 0, h.get("tier") or "-", fmts["plain"])
        ws.write(r, 1, h.get("date") or "-", fmts["plain"])
        ws.write(r, 2, h.get("column", "-"), fmts["plain"])
        ws.write(r, 3, h.get("title", "").replace("|", "/"), fmts["plain"])
        ws.write(r, 4, ", ".join(h.get("matched_keywords", [])), fmts["plain"])
        link = h.get("url", "")
        if link:
            ws.write_url(r, 5, link, fmts["link"], link)
        else:
            ws.write(r, 5, "", fmts["plain"])
        r += 1

    last = r - 1
    ws.autofilter(hdr, 0, last, 5)
    ws.freeze_panes(1, 0)
    return ws


# ════════════════════════════════════════════════════════════════════
# Score
# ════════════════════════════════════════════════════════════════════
def _build_score(wb, fmts, score_res):
    ws = wb.add_worksheet(t("xlsx.signal.sheet.score"))
    _set_grid(ws, label_w=40, body_w=18)
    page_decor(ws, t("xlsx.signal.banner"), fmts)

    banner(ws, 0, 0, _NCOL - 1, t("xlsx.signal.score.title"), fmts, height=BANNER_H)
    r = 2

    ws.write(r, 0, t("xlsx.signal.score.total"), fmts["fkey"])
    ws.merge_range(r, 1, r, _NCOL - 1, score_res.get("score"), fmts["right"])
    ws.set_row(r, 18)
    r += 1

    tier = score_res.get("tier") or score_res.get("evidence_tier")
    ws.write(r, 0, t("xlsx.signal.score.tier"), fmts["fkey_z"])
    ws.merge_range(r, 1, r, _NCOL - 1, tier, fmts["zebra"])
    ws.set_row(r, 16)
    r += 1

    comp = score_res.get("components") or score_res.get("breakdown")
    if comp:
        r += 1
        r = _section(ws, r, 0, _NCOL - 1, t("xlsx.signal.section.components"), fmts)
        r += 1
        rows = [[str(kk), vv] for kk, vv in comp.items()]
        nr, hdr, first, last = _table(
            ws, r, fmts,
            [t("xlsx.signal.col.component"), t("xlsx.signal.col.points")],
            rows, c0=0, zebra=True, first_is_key=True)
        ws.set_column(0, 0, 40)
        ws.set_column(1, 1, 18)
        r = nr

    rationale = score_res.get("rationale")
    if rationale:
        r += 1
        ws.write(r, 0, t("xlsx.signal.score.rationale"), fmts["fkey"])
        ws.merge_range(r, 1, r, _NCOL - 1, rationale, fmts["plain"])
        ws.set_row(r, 16)

    ws.freeze_panes(1, 0)
    return ws


# ════════════════════════════════════════════════════════════════════
# Entry point
# ════════════════════════════════════════════════════════════════════
def build_signal_xlsx(out_path, *, drug, event, fetch_data, cases_data=None,
                      disp_res=None,
                      cn_pv=None, label_data=None, label_status=None,
                      score_res=None, lang=None):
    # Workbook language must not depend on the server OS: the old
    # ``"zh" if win32 else None`` branch reset i18n to auto-detect on the
    # published (Linux/en_US) workbench and silently emitted an English report.
    set_lang(resolve_report_lang(lang, skill="safety"))

    wb = xlsxwriter.Workbook(out_path, {"in_memory": True})
    fmts = make_formats(wb, PAL)

    _build_readme(wb, fmts, drug, event, disp_res)
    _build_summary(wb, fmts, drug, event, fetch_data, disp_res)
    _build_raw_counts(wb, fmts, fetch_data, disp_res)
    if cases_data:
        _build_case_details(wb, fmts, cases_data, lang)

    if label_data is not None:
        _build_fda_label(wb, fmts, label_data, label_status, event)

    if cn_pv and cn_pv.get("hit_count"):
        _build_cn_pv(wb, fmts, cn_pv)

    if score_res is not None:
        _build_score(wb, fmts, score_res)

    wb.close()
    return out_path


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Build FAERS signal-analysis .xlsx from cached JSON.")
    ap.add_argument("--fetch", required=True, help="faers_fetch.json")
    ap.add_argument("--disp", help="disproportionality.json")
    ap.add_argument("--label", help="fda_label.json")
    ap.add_argument("--cn-pv", help="cn_pv.json")
    ap.add_argument("--score", help="score json (optional)")
    ap.add_argument("--drug", default="?")
    ap.add_argument("--event", default="?")
    ap.add_argument("--out", required=True)
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"],
                    help="Language: auto (CT_SAFETY_LANG / default zh), zh, or en")
    args = ap.parse_args()

    set_lang(resolve_report_lang(args.lang, skill="safety"))

    data = json.load(open(args.fetch, encoding="utf-8")) if args.fetch else {}
    disp = json.load(open(args.disp, encoding="utf-8")) if args.disp else None
    label = json.load(open(args.label, encoding="utf-8")) if args.label else None
    cn = json.load(open(args.cn_pv, encoding="utf-8")) if args.cn_pv else None
    score = json.load(open(args.score, encoding="utf-8")) if args.score else None

    build_signal_xlsx(args.out, drug=args.drug, event=args.event,
                      fetch_data=data, disp_res=disp, cn_pv=cn,
                      label_data=label, label_status=None, score_res=score,
                      lang=args.lang)
    print("[OK] wrote", args.out)
