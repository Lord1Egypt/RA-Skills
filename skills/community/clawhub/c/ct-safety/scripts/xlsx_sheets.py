#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""xlsx_sheets.py — shared, composable FAERS workbook sheet builders.

Single source of truth for the per-case detail sheet used by BOTH Excel
generators in ct-safety:

  * ``report_xlsx.build_signal_xlsx``  (workbench interactive search → faers_report.xlsx)
  * ``export_xlsx.export_workbook``    (fetch_reports.py batch download)

The two upstream generators keep their own analytical sections (signal 2×2 /
disproportionality vs demographic distributions + charts) because their inputs
differ, but the *template* — chrome, sheet naming and especially the
individual-case sheet — is unified here so both workbooks read as one product.

Unification contract (per references/xlsx_delivery.md: "统一契约，不统一实现"):
  - The individual-case sheet is ALWAYS named via ``t("xlsx.signal.sheet.cases")``
    (个案明细) and renders the SAME 12 columns, regardless of which path built it.
  - ``build_case_details`` tolerates BOTH field schemas in the wild:
      - report path : adapters/fetch_faers.fetch_case_reports case dict
      - batch  path : fetch_reports._extract flattened dict
    via ``_norm_case``, so neither caller has to pre-normalise.

Pure local; no network. Reuses vendored ``excel_style`` / ``i18n``.
"""

import os
import sys

import xlsxwriter

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from excel_style import (  # noqa: E402
    make_formats, banner, page_decor, BANNER_H, PALETTES, HEADER_H,
)
from i18n import t, set_lang  # noqa: E402
from xlsx_delivery import resolve_report_lang  # noqa: E402

PAL = PALETTES["safety"]


# ── column definition (single source of truth) ────────────────────────────
_CASE_COLS = [
    ("xlsx.signal.case.id", 16),
    ("xlsx.signal.case.version", 9),
    ("xlsx.signal.case.received", 13),
    ("xlsx.signal.case.serious", 11),
    ("xlsx.signal.case.outcome", 11),
    ("xlsx.signal.case.reaction", 42),
    ("xlsx.signal.case.drug", 32),
    ("xlsx.signal.case.sex", 9),
    ("xlsx.signal.case.age", 11),
    ("xlsx.signal.case.ageunit", 11),
    ("xlsx.signal.case.country", 13),
    ("xlsx.signal.case.reporter", 13),
]


def _norm_case(c):
    """Map either field schema onto the canonical 12-column case dict."""
    rp = c.get("reaction_pt")
    if rp is None:
        rp = c.get("reaction_pts")  # batch path stores a joined string
    if isinstance(rp, (list, tuple)):
        reaction = "; ".join(str(x) for x in rp if x is not None)
    else:
        reaction = "" if rp is None else str(rp)

    dg = c.get("drug")
    if dg is None:
        dg = c.get("drug_indications") or c.get("drug_characterizations")
    if isinstance(dg, (list, tuple)):
        drug = "; ".join(str(x) for x in dg if x is not None)
    else:
        drug = "" if dg is None else str(dg)

    sev = c.get("seriousness")
    if sev is None:
        sev = c.get("serious")
    # Outcome is genuinely absent from the openFDA case schema (only seriousness
    # flags exist). Do NOT fall back to reporttype — that would mislabel an
    # initial/follow-up code under the 结局/Outcome column. Interactive and batch
    # paths both leave it blank when unavailable, keeping the template honest.
    outc = c.get("outcome")
    occ = c.get("occurcountry") or c.get("primarysourcecountry")
    rep = c.get("reportercountry") or c.get("primarysourcecountry") or occ
    age = c.get("patientonsetage") or c.get("patientage")
    ageu = c.get("patientonsetageunit") or c.get("patientageunit")
    return {
        "safetyreportid": c.get("safetyreportid"),
        "safetyreportversion": c.get("safetyreportversion"),
        "receivedate": c.get("receivedate"),
        "seriousness": sev,
        "outcome": outc,
        "reaction": reaction,
        "drug": drug,
        "patientsex": c.get("patientsex"),
        "patientonsetage": age,
        "patientonsetageunit": ageu,
        "occurcountry": occ,
        "reportercountry": rep,
    }


def _serious(v):
    if v in ("1", 1, "Y", "y"):
        return t("xlsx.safety.serious_yes")
    if v in ("2", 2, "N", "n"):
        return t("xlsx.safety.serious_no")
    return "" if v is None else str(v)


def _sex(v):
    if v in ("1", 1):
        return t("xlsx.safety.sex_m")
    if v in ("2", 2):
        return t("xlsx.safety.sex_f")
    return "" if v is None else str(v)


def build_case_details(wb, fmts, cases, lang=None):
    """Render the unified per-case FAERS sheet (filterable, frozen header).

    Used by BOTH report_xlsx and export_xlsx, so the individual-case template
    is identical across the interactive and batch deliverables.
    """
    ws = wb.add_worksheet(t("xlsx.signal.sheet.cases"))
    page_decor(ws, t("xlsx.signal.banner"), fmts)

    headers = [t(k) for k, _ in _CASE_COLS]
    ncols = len(headers)
    for ci, (_, w) in enumerate(_CASE_COLS):
        ws.set_column(ci, ci, w)
    banner(ws, 0, 0, ncols - 1, t("xlsx.signal.sheet.cases"), fmts, height=BANNER_H)

    hdr_row = 2
    for ci, h in enumerate(headers):
        ws.write(hdr_row, ci, h, fmts["header"])
    ws.set_row(hdr_row, 18)

    r = hdr_row + 1
    for raw in (cases or []):
        c = _norm_case(raw)
        row = [
            c["safetyreportid"],
            c["safetyreportversion"],
            c["receivedate"],
            _serious(c["seriousness"]),
            c["outcome"],
            c["reaction"],
            c["drug"],
            _sex(c["patientsex"]),
            c["patientonsetage"],
            c["patientonsetageunit"],
            c["occurcountry"],
            c["reportercountry"],
        ]
        base = fmts["zebra"] if ((r - hdr_row) % 2 == 0) else fmts["plain"]
        for ci, val in enumerate(row):
            ws.write(r, ci, "" if val is None else val, base)
        r += 1

    if r > hdr_row + 1:
        ws.autofilter(hdr_row, 0, r - 1, ncols - 1)
    ws.freeze_panes(hdr_row + 1, 0)

    note = t("xlsx.signal.case.note").format(n=len(cases or []))
    ws.merge_range(r + 1, 0, r + 1, ncols - 1, note, fmts["note"])
    return ws
