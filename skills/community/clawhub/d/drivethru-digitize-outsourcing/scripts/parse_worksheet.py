#!/usr/bin/env python3
"""Parse a Wilcom-style embroidery **Production Worksheet** PDF.

Every digitized job comes back with a worksheet PDF. This pulls the numbers the
shop needs onto the decoration:

* ``stitch_count`` — total stitches
* ``height_in`` / ``width_in`` — the sewn size, in inches
* ``colors`` — the **Stop Sequence** thread list, in stitch order, each with its
  ``sequence``, ``code`` (the field the decoration matches on), ``name``,
  ``chart``, and per-colour ``stitches``.

Its output feeds ``digitize_demand_apply_worksheet`` directly:
``{stitch_count, height_in, width_in, colors:[{code, name, sequence}, …]}``.

**Why positional, not text order.** ``get_text()`` linearises a two-column
worksheet into a misleading label/value stream, and the Stop-Sequence table has
a right-aligned stitch column and an empty colour-swatch column that shift a
naive split. So this reads each labelled scalar from the label word's *own line*
(the value words to its right), and assigns every table word to the header
column it physically **overlaps** (falling back to the nearest column centre) —
which is stable regardless of alignment or the blank swatch column. Scans all
pages, so a long colour list that spills onto page 2 is still captured.

Usage:
    python3 parse_worksheet.py <worksheet.pdf>            # prints one JSON object
    python3 parse_worksheet.py <worksheet.pdf> --pretty   # indented

Exit code is non-zero on a hard failure (missing file / unreadable PDF); a
parseable PDF that is merely missing a field returns JSON with that field null
and a note in ``warnings`` (so the caller can decide, not crash).
"""

import json
import re
import sys

# Header labels as they appear in the Stop-Sequence table, mapped to the output
# key each column feeds. "Color" is the swatch column (no text) and is ignored.
_COLUMN_KEYS = {
    "#": "row",
    "N#": "n_number",
    "Color": "_swatch",   # a colour swatch, no text — kept only for column geometry
    "St.": "stitches",
    "Code": "code",
    "Name": "name",
    "Chart": "chart",
}
# The text headers that reliably identify the Stop-Sequence header row.
_HEADER_ANCHORS = ("Code", "Name", "Chart")
# A "#"-column row marker: "1", "1.", "12." …
_ROW_MARKER = re.compile(r"^\d+\.?$")
_Y_TOL = 3.0  # words within this many points of y are on the same line


def _first_number(text):
    """First signed decimal in ``text`` as a float, or None ("2.08 in" → 2.08)."""
    if not text:
        return None
    m = re.search(r"[-+]?\d*\.?\d+", text.replace(",", ""))
    return float(m.group()) if m else None


def _first_int(text):
    """First integer in ``text``, commas stripped ("5,455" → 5455), or None."""
    if not text:
        return None
    m = re.search(r"[-+]?\d+", text.replace(",", ""))
    return int(m.group()) if m else None


def _lines(words):
    """Group PyMuPDF word tuples into lines by y, each sorted left→right.

    ``words`` are (x0, y0, x1, y1, text, block, line, wordno). Returns a list of
    (y, [word, …]) sorted top→bottom."""
    rows = []
    for w in sorted(words, key=lambda w: (round(w[1], 1), w[0])):
        y = w[1]
        for row in rows:
            if abs(row[0] - y) <= _Y_TOL:
                row[1].append(w)
                break
        else:
            rows.append((y, [w]))
    return [(y, sorted(ws, key=lambda w: w[0])) for y, ws in rows]


def _label_value(lines, label):
    """Value string for a ``label`` word — the words on its own line that sit to
    its right, joined. None when the label isn't found."""
    for _y, ws in lines:
        labword = next((w for w in ws if w[4] == label), None)
        if labword is None:
            continue
        right = [w[4] for w in ws if w[0] > labword[0] + 0.1 and w is not labword]
        return " ".join(right).strip() or None
    return None


def _assign_column(word, headers):
    """The header column ``word`` belongs to: the header it overlaps most, or —
    when it overlaps none (a value that sits between columns) — the nearest by
    centre. ``headers`` is [(key, x0, x1), …]."""
    wx0, wx1 = word[0], word[2]
    best_key, best_overlap = None, 0.0
    for key, hx0, hx1 in headers:
        overlap = min(wx1, hx1) - max(wx0, hx0)
        if overlap > best_overlap:
            best_overlap, best_key = overlap, key
    if best_key is not None:
        return best_key
    wc = (wx0 + wx1) / 2.0
    return min(headers, key=lambda h: abs((h[1] + h[2]) / 2.0 - wc))[0]


def _parse_stop_sequence(all_lines_by_page):
    """Extract the Stop-Sequence colour rows across pages, in order.

    Returns (colors, warnings). Each colour: {sequence, n_number, code, name,
    chart, stitches}; ``sequence`` is the running stitch order (1..N)."""
    colors, warnings = [], []
    seq = 0
    for page_no, lines in all_lines_by_page:
        # Find this page's header row: a line carrying the text anchors.
        header = None
        for y, ws in lines:
            texts = {w[4] for w in ws}
            if all(a in texts for a in _HEADER_ANCHORS):
                header = (y, ws)
                break
        if not header:
            continue
        y_header, header_ws = header
        # Build column ranges from the header words we recognise.
        headers = [(_COLUMN_KEYS[w[4]], w[0], w[2])
                   for w in header_ws if w[4] in _COLUMN_KEYS]
        hash_col = next((h for h in headers if h[0] == "row"), None)

        for y, ws in lines:
            if y <= y_header + _Y_TOL:
                continue
            # A data row is marked by "1." / "2." in the "#" column.
            marker = None
            for w in ws:
                if _ROW_MARKER.match(w[4]) and (
                        hash_col is None
                        or min(w[2], hash_col[2]) - max(w[0], hash_col[1]) > -2):
                    marker = w
                    break
            if marker is None:
                continue
            cells = {}
            for w in ws:
                key = _assign_column(w, headers)
                cells.setdefault(key, []).append(w[4])
            code = " ".join(cells.get("code", [])).strip()
            name = " ".join(cells.get("name", [])).strip()
            chart = " ".join(cells.get("chart", [])).strip()
            seq += 1
            row = {
                "sequence": seq,
                "n_number": _first_int(" ".join(cells.get("n_number", []))),
                "code": code or None,
                "name": name or None,
                "chart": chart or None,
                "stitches": _first_int(" ".join(cells.get("stitches", []))),
            }
            if not code:
                warnings.append("Stop-Sequence row %d has no code" % seq)
            colors.append(row)
    return colors, warnings


def parse_worksheet(path):
    """Parse ``path`` and return the worksheet dict. Raises on an unreadable PDF."""
    try:
        import pymupdf  # PyMuPDF; self-contained (no cffi/cryptography deps)
    except ImportError:  # pragma: no cover - environment guard
        try:
            import fitz as pymupdf  # legacy import name
        except ImportError:
            raise RuntimeError(
                "PyMuPDF is required (pip/uv install pymupdf) to parse worksheets")

    doc = pymupdf.open(path)
    all_lines = []
    field_lines = []  # search every page for the labelled scalars
    for i in range(doc.page_count):
        lines = _lines(doc[i].get_text("words"))
        all_lines.append((i, lines))
        field_lines.extend(lines)

    stitches_raw = _label_value(field_lines, "Stitches:")
    height_raw = _label_value(field_lines, "Height:")
    width_raw = _label_value(field_lines, "Width:")
    colors_raw = _label_value(field_lines, "Colors:")

    colors, warnings = _parse_stop_sequence(all_lines)

    result = {
        "stitch_count": _first_int(stitches_raw),
        "height_in": _first_number(height_raw),
        "width_in": _first_number(width_raw),
        "colors_declared": _first_int(colors_raw),
        "colors": colors,
        "raw": {  # what the labels actually said, for auditing a bad parse
            "stitches": stitches_raw, "height": height_raw,
            "width": width_raw, "colors": colors_raw,
        },
        "warnings": warnings,
    }

    # Cross-checks — surfaced, never fatal.
    if result["stitch_count"] is None:
        warnings.append("no Stitches value found")
    for key, raw in (("height_in", height_raw), ("width_in", width_raw)):
        if raw and "mm" in raw.lower():
            warnings.append("%s looks like millimetres (%r); the decoration "
                            "expects inches" % (key, raw))
    declared = result["colors_declared"]
    if declared is not None and declared != len(colors):
        warnings.append("Colors field says %d but %d Stop-Sequence rows parsed"
                        % (declared, len(colors)))
    if not colors:
        warnings.append("no Stop-Sequence colour rows parsed")
    return result


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("-")]
    pretty = "--pretty" in argv[1:]
    if len(args) != 1:
        sys.stderr.write("usage: parse_worksheet.py <worksheet.pdf> [--pretty]\n")
        return 2
    try:
        result = parse_worksheet(args[0])
    except FileNotFoundError:
        print(json.dumps({"error": "file not found: %s" % args[0]}))
        return 1
    except Exception as exc:  # noqa: BLE001 - report cleanly as JSON + exit code
        print(json.dumps({"error": str(exc)}))
        return 1
    print(json.dumps(result, indent=2 if pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
