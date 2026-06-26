#!/usr/bin/env python3
"""build_outline_deck_v2.py — render a banker PPT from a structured
slides-outline.md (YAML-style blocks per slide).

v2 vs v1: v1 emitted generic "title + text block" slides for every layout.
v2 emits real pptxgenjs primitives per layout type:

  stat-cards      → 2/4 gold-bordered cards with big numbers + colour highlight
  table           → real addTable() with header row + banded body
  bar-chart       → real addChart(pres.charts.BAR) with X-axis + Y-series
  line-chart      → real addChart(pres.charts.LINE) with quarterly trend
  risk-heatmap    → 3×3 matrix with colour-coded cells and risk labels placed
  scenario-table  → 3-col scenario grid with red/amber/green tinted cells
  callout-box     → full-width gold-bordered verdict box
  divider         → big Chinese + English subtitle section divider
  cover           → Rule-3 compliant cover (English 44pt hero + Chinese ≤28pt)
  bullets         → title + bullet list (fallback)

Outline block format: each slide starts with `## Slide N — Title` then has
`Layout: <type>` and type-specific YAML-like fields. Parser is YAML-ish but
hand-written (no PyYAML dep) to keep the skill light.
"""
from __future__ import annotations
import json, pathlib, re, subprocess, sys


SLIDE_HEADER = re.compile(r"^##\s*Slide\s+(\d+)\s*[—\-–]\s*(.+)$", re.MULTILINE)
LIST_ITEM = re.compile(r"^-\s+(.+)$")


# ============================================================================
# Outline parser — parse YAML-like blocks without a YAML library
# ============================================================================

def parse_value(raw: str):
    """Parse a scalar value: JSON array / string (quoted or unquoted) / number."""
    raw = raw.strip()
    if not raw:
        return None
    # JSON array or object
    if raw.startswith("[") or raw.startswith("{"):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw
    # Quoted string
    if (raw.startswith('"') and raw.endswith('"')) or \
       (raw.startswith("'") and raw.endswith("'")):
        return raw[1:-1]
    # Try number
    try:
        if "." in raw:
            return float(raw)
        return int(raw)
    except ValueError:
        pass
    return raw


def parse_slide_block(body: str) -> dict:
    """Parse one slide's body (everything after `## Slide N — Title`).

    Supports:
      Key: value                 # scalar
      Key: [a, b, c]             # JSON array
      Cards:                     # nested list of dicts
      - label: foo
        value: "1"
      Y-series:                  # nested list of dicts with numeric arrays
      - name: 营收
        values: [1,2,3]
        color: "C9A84C"
    """
    result: dict = {}
    lines = body.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()
        if not stripped or stripped.startswith("<!--"):
            i += 1
            continue
        # Top-level key
        m = re.match(r"^([A-Za-z][\w\- ]*?)\s*:\s*(.*)$", stripped)
        if m:
            key = m.group(1).strip()
            val_raw = m.group(2).rstrip()
            if val_raw:
                # Scalar on same line
                result[key] = parse_value(val_raw)
                i += 1
                continue
            # Multi-line nested list
            nested: list = []
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if not nxt.strip():
                    i += 1
                    continue
                # End of this list when we hit a new top-level key
                if re.match(r"^([A-Za-z][\w\- ]*?)\s*:\s*", nxt) and \
                        not nxt.lstrip().startswith("-") and \
                        not nxt.startswith(" "):
                    break
                m_item = re.match(r"^-\s+(.*)$", nxt)
                if m_item:
                    item_dict: dict = {}
                    rest = m_item.group(1)
                    if rest.strip():
                        # Parse "key: value" starting the item
                        m_kv = re.match(r"^([A-Za-z][\w\- ]*?)\s*:\s*(.+)$", rest)
                        if m_kv:
                            item_dict[m_kv.group(1).strip()] = \
                                parse_value(m_kv.group(2))
                        else:
                            item_dict["_scalar"] = parse_value(rest)
                    i += 1
                    # Continuation lines indented under this item
                    while i < len(lines):
                        cont = lines[i]
                        if cont.startswith("  ") and not cont.lstrip().startswith("-"):
                            m_kv = re.match(r"^\s+([A-Za-z][\w\- ]*?)\s*:\s*(.+)$",
                                            cont)
                            if m_kv:
                                item_dict[m_kv.group(1).strip()] = \
                                    parse_value(m_kv.group(2))
                                i += 1
                                continue
                        break
                    nested.append(item_dict)
                    continue
                break
            result[key] = nested
            continue
        i += 1
    return result


def parse_outline(outline_md: str) -> list[dict]:
    """Return ordered list of parsed slide dicts."""
    slides = []
    parts = re.split(r"(?=^##\s*Slide\s+\d+\s*[—\-–])",
                     outline_md, flags=re.MULTILINE)
    for part in parts:
        m = SLIDE_HEADER.match(part)
        if not m:
            continue
        num = int(m.group(1))
        heading = m.group(2).strip()
        body = part[m.end():]
        parsed = parse_slide_block(body)
        parsed["_num"] = num
        parsed["_heading"] = heading
        parsed["_layout"] = str(parsed.get("Layout", "bullets")).strip().lower()
        slides.append(parsed)
    slides.sort(key=lambda s: s["_num"])
    return slides


# ============================================================================
# pptxgenjs code emission — one function per layout type
# ============================================================================

THEME = {
    "bg": "0D1829",
    "primary": "0D1829",
    "secondary": "C9A84C",
    "accent": "D4AF37",
    "light": "2A3A5C",
    "white": "FFFFFF",
    "grey": "AAAAAA",
    "red": "C0392B",
    "amber": "E67E22",
    "green": "27AE60",
}


def js_str(s) -> str:
    """JSON-dump for safe embedding in JS source."""
    return json.dumps("" if s is None else str(s), ensure_ascii=False)


def head_bar() -> str:
    """Top gold accent bar present on every non-cover slide."""
    return f"""  slide.addShape(pres.ShapeType.rect, {{
    x: 0, y: 0, w: 10, h: 0.08,
    fill: {{ color: '{THEME['secondary']}' }}, line: {{ color: '{THEME['secondary']}', width: 0 }},
  }});
"""


def slide_title(title: str) -> str:
    return f"""  slide.addText({js_str(title)}, {{
    x: 0.5, y: 0.25, w: 9, h: 0.65,
    fontSize: 24, bold: true, color: '{THEME['secondary']}',
    fontFace: 'Microsoft YaHei',
  }});
"""


def render_cover(s: dict) -> str:
    en = s.get("English-title") or s.get("english-title") or s.get("_heading")
    cn = s.get("Chinese-subtitle") or s.get("chinese-subtitle") or ""
    ticker = s.get("Ticker") or s.get("ticker") or ""
    date = s.get("Date") or s.get("date") or "2026-04"
    return f"""  // Rule 3: English hero 44pt + Chinese subtitle ≤28pt
  slide.addText({js_str(en)}, {{
    x: 0.7, y: 1.7, w: 8.5, h: 1.2,
    fontSize: 44, bold: true, color: '{THEME['secondary']}', fontFace: 'Arial',
  }});
  slide.addText({js_str(cn)}, {{
    x: 0.7, y: 2.9, w: 8.5, h: 0.8,
    fontSize: 24, color: '{THEME['white']}', fontFace: 'Microsoft YaHei',
  }});
  slide.addText({js_str(ticker)}, {{
    x: 0.7, y: 3.7, w: 8.5, h: 0.5,
    fontSize: 18, color: '{THEME['secondary']}', fontFace: 'Arial',
  }});
  slide.addText({js_str('投行深度研究 · ' + str(date))}, {{
    x: 0.7, y: 4.4, w: 8.5, h: 0.4,
    fontSize: 14, color: '{THEME['grey']}', fontFace: 'Arial',
  }});
  slide.addShape(pres.ShapeType.rect, {{
    x: 0, y: 5.4, w: 10, h: 0.06,
    fill: {{ color: '{THEME['secondary']}' }}, line: {{ color: '{THEME['secondary']}', width: 0 }},
  }});
"""


def render_divider(s: dict) -> str:
    ct = s.get("Chinese-title") or s.get("chinese-title") or s.get("_heading")
    es = s.get("English-subtitle") or s.get("english-subtitle") or ""
    return f"""  slide.addShape(pres.ShapeType.rect, {{
    x: 0, y: 2.3, w: 10, h: 1.5,
    fill: {{ color: '{THEME['light']}' }}, line: {{ color: '{THEME['light']}', width: 0 }},
  }});
  slide.addText({js_str(ct)}, {{
    x: 0.7, y: 2.45, w: 8.5, h: 0.9,
    fontSize: 36, bold: true, color: '{THEME['secondary']}', fontFace: 'Microsoft YaHei',
  }});
  slide.addText({js_str(es)}, {{
    x: 0.7, y: 3.25, w: 8.5, h: 0.5,
    fontSize: 14, italic: true, color: '{THEME['grey']}', fontFace: 'Arial',
  }});
"""


def render_stat_cards(s: dict) -> str:
    cards = s.get("Cards") or s.get("cards") or []
    n = len(cards)
    if n == 0:
        return render_bullets({**s, "Points": ["(no cards provided)"]})
    # 1-3 cards in one row, 4 cards in a 2x2 grid
    card_w = min(2.9, 9.0 / max(1, n))
    if n == 4:
        card_w = 4.5
    out = [slide_title(s["_heading"])]
    for idx, c in enumerate(cards):
        if n == 4:
            x = 0.5 + (idx % 2) * (card_w + 0.1)
            y = 1.2 + (idx // 2) * 1.9
            w, h = card_w, 1.7
        else:
            x = 0.5 + idx * (card_w + 0.1)
            y = 1.5
            w, h = card_w, 2.8
        label = c.get("label", "")
        value = c.get("value", "")
        unit = c.get("unit", "")
        highlight = (c.get("highlight") or "none").lower()
        color_map = {"red": THEME["red"], "amber": THEME["amber"],
                     "green": THEME["green"], "none": THEME["white"]}
        val_color = color_map.get(highlight, THEME["white"])
        out.append(f"""  slide.addShape(pres.ShapeType.rect, {{
    x: {x}, y: {y}, w: {w}, h: {h},
    fill: {{ color: '{THEME['light']}' }},
    line: {{ color: '{THEME['secondary']}', width: 1 }},
  }});
  slide.addText({js_str(label)}, {{
    x: {x + 0.15}, y: {y + 0.15}, w: {w - 0.3}, h: 0.5,
    fontSize: 14, color: '{THEME['secondary']}', fontFace: 'Microsoft YaHei',
  }});
  slide.addText({js_str(value)}, {{
    x: {x + 0.15}, y: {y + 0.6}, w: {w - 0.3}, h: {h - 1.1},
    fontSize: 36, bold: true, color: '{val_color}', fontFace: 'Arial',
  }});
  slide.addText({js_str(unit)}, {{
    x: {x + 0.15}, y: {y + h - 0.5}, w: {w - 0.3}, h: 0.4,
    fontSize: 14, color: '{THEME['grey']}', fontFace: 'Microsoft YaHei',
  }});
""")
    return "".join(out)


def render_table(s: dict) -> str:
    headers = s.get("Headers") or s.get("headers") or []
    rows = s.get("Rows") or s.get("rows") or []
    note = s.get("Note") or s.get("note") or ""
    if not headers or not rows:
        return slide_title(s["_heading"]) + \
               "  slide.addText('(table data missing)', {x: 0.5, y: 1.2, w: 9, h: 4, fontSize: 12, color: '#FFFFFF'});"
    # Build rows array as JS
    js_rows = []
    # Header row with gold fill + dark text
    hdr_cells = [
        f"{{text: {js_str(h)}, options: {{bold: true, color: '{THEME['primary']}', fill: '{THEME['secondary']}', align: 'center'}}}}"
        for h in headers
    ]
    js_rows.append(f"[{', '.join(hdr_cells)}]")
    for row in rows:
        if not isinstance(row, list):
            row = [row]
        cells = []
        for i, cell in enumerate(row):
            align = "'left'" if i == 0 else "'right'"
            color = THEME["white"]
            # Highlight negative numbers red, green for positive gains
            if isinstance(cell, str) and (cell.startswith("-") or "N/M" in cell):
                color = THEME["red"]
            cells.append(
                f"{{text: {js_str(cell)}, options: {{color: '{color}', align: {align}}}}}"
            )
        js_rows.append(f"[{', '.join(cells)}]")
    rows_js = ",\n    ".join(js_rows)
    col_count = len(headers)
    # Column widths: first col wider, others equal
    first_w = 2.5 if col_count >= 3 else 3.0
    rest_w = round((9.0 - first_w) / max(1, col_count - 1), 2)
    col_w = [first_w] + [rest_w] * (col_count - 1)
    out = [slide_title(s["_heading"])]
    out.append(f"""  slide.addTable([
    {rows_js}
  ], {{
    x: 0.5, y: 1.15, w: 9, h: {min(3.8, 0.4 * (len(rows) + 1))},
    fontSize: 12, fontFace: 'Microsoft YaHei',
    border: {{ type: 'solid', pt: 0.5, color: '{THEME['light']}' }},
    fill: {{ color: '{THEME['primary']}' }},
    colW: {json.dumps(col_w)},
  }});
""")
    if note:
        out.append(f"""  slide.addText({js_str('注: ' + str(note))}, {{
    x: 0.5, y: 5.15, w: 9, h: 0.35,
    fontSize: 11, italic: true, color: '{THEME['grey']}', fontFace: 'Microsoft YaHei',
  }});
""")
    return "".join(out)


def _chart(s: dict, chart_kind: str) -> str:
    x_axis = s.get("X-axis") or s.get("x-axis") or []
    series = s.get("Y-series") or s.get("y-series") or []
    note = s.get("Note") or s.get("note") or ""
    if not x_axis or not series:
        return slide_title(s["_heading"]) + "  slide.addText('(chart data missing)', {x: 0.5, y: 1.2, w: 9, h: 4, fontSize: 12, color: '#FFFFFF'});"
    # Build chart data array
    data_entries = []
    chart_colors = []
    for sr in series:
        name = sr.get("name", "")
        values = sr.get("values", [])
        color = sr.get("color", THEME["secondary"]).lstrip("#")
        chart_colors.append(f"'{color}'")
        values_js = json.dumps(values)
        data_entries.append(
            f"{{name: {js_str(name)}, labels: {json.dumps(x_axis)}, values: {values_js}}}"
        )
    data_js = ",\n    ".join(data_entries)
    chart_type_js = "pres.charts.BAR" if chart_kind == "bar" else "pres.charts.LINE"
    out = [slide_title(s["_heading"])]
    out.append(f"""  slide.addChart({chart_type_js}, [
    {data_js}
  ], {{
    x: 0.5, y: 1.15, w: 9, h: 3.9,
    chartColors: [{', '.join(chart_colors)}],
    catAxisLabelColor: '{THEME['white']}',
    catAxisLabelFontFace: 'Arial',
    valAxisLabelColor: '{THEME['white']}',
    valAxisLabelFontFace: 'Arial',
    showLegend: true,
    legendPos: 'b',
    legendColor: '{THEME['white']}',
    legendFontFace: 'Microsoft YaHei',
    plotArea: {{ fill: {{ color: '{THEME['primary']}' }} }},
  }});
""")
    if note:
        out.append(f"""  slide.addText({js_str('Takeaway: ' + str(note))}, {{
    x: 0.5, y: 5.1, w: 9, h: 0.4,
    fontSize: 11, italic: true, color: '{THEME['grey']}', fontFace: 'Microsoft YaHei',
  }});
""")
    return "".join(out)


def render_bar_chart(s: dict) -> str:
    return _chart(s, "bar")


def render_line_chart(s: dict) -> str:
    return _chart(s, "line")


def render_risk_heatmap(s: dict) -> str:
    risks = s.get("Risks") or s.get("risks") or []
    # 3x3 grid: likelihood on X, severity on Y; top-right (高, 高) = red, bottom-left (低, 低) = green
    sev_map = {"高": 2, "中": 1, "低": 0}
    lik_map = {"高": 2, "中": 1, "低": 0}
    # Color grid (bottom-left green, top-right red)
    grid_colors = [
        [THEME["green"], THEME["amber"], THEME["red"]],
        [THEME["green"], THEME["amber"], THEME["red"]],
        [THEME["amber"], THEME["red"], THEME["red"]],
    ]
    # Cells indexed [sev_row][lik_col]
    cells: dict = {}  # (sev, lik) -> list of risk names
    for r in risks:
        sev = sev_map.get(str(r.get("severity", "")).strip(), 1)
        lik = lik_map.get(str(r.get("likelihood", "")).strip(), 1)
        cells.setdefault((sev, lik), []).append(r.get("name", "?"))
    out = [slide_title(s["_heading"])]
    # Grid dimensions
    grid_x0, grid_y0 = 1.5, 1.3
    cell_w, cell_h = 2.5, 1.2
    # Y axis label (severity)
    out.append(f"""  slide.addText('严重程度 →', {{
    x: 0.15, y: 2.6, w: 1.3, h: 0.4, fontSize: 11, color: '{THEME['grey']}',
    fontFace: 'Microsoft YaHei', rotate: -90,
  }});
  slide.addText('发生概率 →', {{
    x: {grid_x0}, y: {grid_y0 + 3 * cell_h + 0.1}, w: 3 * {cell_w}, h: 0.35,
    fontSize: 11, color: '{THEME['grey']}', fontFace: 'Microsoft YaHei', align: 'center',
  }});
""")
    severity_labels = ["高", "中", "低"]  # top → bottom
    likelihood_labels = ["低", "中", "高"]  # left → right
    for row_idx in range(3):  # sev axis (top is 高=2)
        for col_idx in range(3):  # lik axis (right is 高=2)
            sev_rank = 2 - row_idx
            lik_rank = col_idx
            x = grid_x0 + col_idx * cell_w
            y = grid_y0 + row_idx * cell_h
            color = grid_colors[sev_rank][lik_rank]
            risk_names = cells.get((sev_rank, lik_rank), [])
            # Cell background
            out.append(f"""  slide.addShape(pres.ShapeType.rect, {{
    x: {x}, y: {y}, w: {cell_w}, h: {cell_h},
    fill: {{ color: '{color}', transparency: 40 }},
    line: {{ color: '{THEME['secondary']}', width: 0.5 }},
  }});
""")
            if risk_names:
                txt = "\n".join("• " + n for n in risk_names)
                out.append(f"""  slide.addText({js_str(txt)}, {{
    x: {x + 0.1}, y: {y + 0.1}, w: {cell_w - 0.2}, h: {cell_h - 0.2},
    fontSize: 10, color: '{THEME['white']}', fontFace: 'Microsoft YaHei', valign: 'top',
  }});
""")
    # Axis tick labels
    for i, lab in enumerate(severity_labels):
        out.append(f"""  slide.addText({js_str(lab)}, {{
    x: {grid_x0 - 0.6}, y: {grid_y0 + i * cell_h + cell_h / 2 - 0.15}, w: 0.5, h: 0.3,
    fontSize: 11, color: '{THEME['secondary']}', fontFace: 'Microsoft YaHei', align: 'right',
  }});
""")
    for i, lab in enumerate(likelihood_labels):
        out.append(f"""  slide.addText({js_str(lab)}, {{
    x: {grid_x0 + i * cell_w}, y: {grid_y0 - 0.35}, w: {cell_w}, h: 0.3,
    fontSize: 11, color: '{THEME['secondary']}', fontFace: 'Microsoft YaHei', align: 'center',
  }});
""")
    return "".join(out)


def render_scenario_table(s: dict) -> str:
    scenarios = s.get("Scenarios") or s.get("scenarios") or []
    out = [slide_title(s["_heading"])]
    col_w = 3.0
    row_y = 1.3
    # Header row
    for idx, name in enumerate(["情景", "核心假设", "目标价", "空间"]):
        out.append(f"""  slide.addShape(pres.ShapeType.rect, {{
    x: {0.5 + idx * 2.25}, y: {row_y}, w: 2.25, h: 0.5,
    fill: {{ color: '{THEME['secondary']}' }}, line: {{ width: 0 }},
  }});
  slide.addText({js_str(name)}, {{
    x: {0.5 + idx * 2.25}, y: {row_y}, w: 2.25, h: 0.5,
    fontSize: 14, bold: true, color: '{THEME['primary']}',
    fontFace: 'Microsoft YaHei', align: 'center', valign: 'middle',
  }});
""")
    # Data rows with colored left indicator
    color_map = {"red": THEME["red"], "amber": THEME["amber"], "green": THEME["green"]}
    for s_idx, sc in enumerate(scenarios):
        ry = row_y + 0.6 + s_idx * 1.0
        color = color_map.get(str(sc.get("color", "amber")).lower(), THEME["amber"])
        cells_vals = [
            sc.get("name", ""),
            sc.get("assumption", ""),
            sc.get("target", ""),
            sc.get("upside", ""),
        ]
        for idx, val in enumerate(cells_vals):
            x = 0.5 + idx * 2.25
            out.append(f"""  slide.addShape(pres.ShapeType.rect, {{
    x: {x}, y: {ry}, w: 2.25, h: 0.9,
    fill: {{ color: '{THEME['light']}' }}, line: {{ color: '{THEME['secondary']}', width: 0.3 }},
  }});
""")
            if idx == 0:  # Scenario name column gets colored bar
                out.append(f"""  slide.addShape(pres.ShapeType.rect, {{
    x: {x}, y: {ry}, w: 0.12, h: 0.9, fill: {{ color: '{color}' }}, line: {{ width: 0 }},
  }});
""")
            align = "'left'" if idx == 1 else "'center'"
            font_size = 11 if idx == 1 else 14
            bold = "false" if idx == 1 else "true"
            out.append(f"""  slide.addText({js_str(val)}, {{
    x: {x + 0.2}, y: {ry + 0.1}, w: 2.05, h: 0.7,
    fontSize: {font_size}, bold: {bold}, color: '{THEME['white']}',
    fontFace: 'Microsoft YaHei', align: {align}, valign: 'middle',
  }});
""")
    return "".join(out)


def render_callout_box(s: dict) -> str:
    title = s.get("Title") or s.get("title") or s["_heading"]
    tags = s.get("Tags") or s.get("tags") or []
    message = s.get("Message") or s.get("message") or ""
    out = [slide_title(s["_heading"])]
    # Large gold-bordered box
    out.append(f"""  slide.addShape(pres.ShapeType.rect, {{
    x: 0.5, y: 1.2, w: 9, h: 4,
    fill: {{ color: '{THEME['light']}' }},
    line: {{ color: '{THEME['secondary']}', width: 2 }},
  }});
  slide.addText({js_str(title)}, {{
    x: 0.8, y: 1.4, w: 8.4, h: 0.6,
    fontSize: 22, bold: true, color: '{THEME['secondary']}',
    fontFace: 'Microsoft YaHei',
  }});
""")
    # Tag badges
    if tags:
        for t_idx, tag in enumerate(tags):
            tx = 0.8 + t_idx * 2.3
            out.append(f"""  slide.addShape(pres.ShapeType.roundRect, {{
    x: {tx}, y: 2.1, w: 2.1, h: 0.5, rectRadius: 0.1,
    fill: {{ color: '{THEME['secondary']}' }}, line: {{ width: 0 }},
  }});
  slide.addText({js_str(tag)}, {{
    x: {tx}, y: 2.1, w: 2.1, h: 0.5,
    fontSize: 13, bold: true, color: '{THEME['primary']}',
    fontFace: 'Microsoft YaHei', align: 'center', valign: 'middle',
  }});
""")
    out.append(f"""  slide.addText({js_str(message)}, {{
    x: 0.8, y: 2.8, w: 8.4, h: 2.3,
    fontSize: 14, color: '{THEME['white']}', fontFace: 'Microsoft YaHei',
    valign: 'top', lineSpacingMultiple: 1.3,
  }});
""")
    return "".join(out)


def render_bullets(s: dict) -> str:
    points = s.get("Points") or s.get("points") or []
    out = [slide_title(s["_heading"])]
    text = "\n".join("• " + str(p) for p in points)
    out.append(f"""  slide.addText({js_str(text)}, {{
    x: 0.8, y: 1.2, w: 8.4, h: 4,
    fontSize: 14, color: '{THEME['white']}', fontFace: 'Microsoft YaHei',
    valign: 'top', lineSpacingMultiple: 1.4,
  }});
""")
    return "".join(out)


RENDERERS = {
    "cover": render_cover,
    "divider": render_divider,
    "stat-cards": render_stat_cards,
    "table": render_table,
    "bar-chart": render_bar_chart,
    "line-chart": render_line_chart,
    "risk-heatmap": render_risk_heatmap,
    "scenario-table": render_scenario_table,
    "callout-box": render_callout_box,
    "bullets": render_bullets,
}


def emit_slide_file(s: dict) -> str:
    layout = s["_layout"]
    renderer = RENDERERS.get(layout, render_bullets)
    body = renderer(s)
    # Cover gets its own background; everything else gets the standard chrome
    if layout == "cover":
        chrome = f"  slide.background = {{ color: '{THEME['bg']}' }};\n"
    else:
        chrome = f"  slide.background = {{ color: '{THEME['bg']}' }};\n" + head_bar()
    heading = s.get("_heading", "")
    return f"""// slide-{s['_num']:02d}.js — {layout} — {heading[:40]}
const createSlide = (pres, theme) => {{
  const slide = pres.addSlide();
{chrome}{body}
}};

const slideConfig = {{ notes: "", title: {js_str(heading)} }};

module.exports = {{ createSlide, slideConfig }};
"""


# ============================================================================
# Main: parse outline, write slides/, compile
# ============================================================================

def main() -> int:
    if len(sys.argv) < 5:
        sys.exit("usage: build_outline_deck_v2.py <dir> <ts_code> <name_cn> <name_en>")
    d = pathlib.Path(sys.argv[1]).resolve()
    ts_code, name_cn, name_en = sys.argv[2], sys.argv[3], sys.argv[4]

    outline_path = d / "slides-outline.md"
    if not outline_path.exists():
        sys.exit(f"{outline_path} missing — run banker-slides-pptx first")
    slides = parse_outline(outline_path.read_text(encoding="utf-8"))
    if not slides:
        sys.exit("no slide blocks parsed")
    layout_counts: dict = {}
    for sl in slides:
        layout_counts[sl["_layout"]] = layout_counts.get(sl["_layout"], 0) + 1
    print(f"parsed {len(slides)} slides; layouts: {layout_counts}")

    slides_dir = d / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)
    for old in slides_dir.glob("slide-*.js"):
        old.unlink()
    for s in slides:
        (slides_dir / f"slide-{s['_num']:02d}.js").write_text(
            emit_slide_file(s), encoding="utf-8")

    template_path = (pathlib.Path.home() /
                     ".openclaw/extensions/aigroup-financial-services-openclaw"
                     "/skills/cn-client-investigation/references"
                     "/compile_with_typo_gate.template.js.txt")
    if not template_path.exists():
        template_path = (pathlib.Path(__file__).resolve().parents[3] /
                         "cn-client-investigation/references"
                         "/compile_with_typo_gate.template.js.txt")
    template = template_path.read_text(encoding="utf-8")
    output_pptx = f"{ts_code.replace('.', '_').lower()}_banker_deck.pptx"
    template = (template
        .replace("const SLIDE_COUNT = 20;", f"const SLIDE_COUNT = {len(slides)};")
        .replace("'presentation.pptx'", f"'{output_pptx}'")
        .replace("'2B2D42'", f"'{THEME['primary']}'")
        .replace("'8D99AE'", f"'{THEME['secondary']}'")
        .replace("'EF233C'", f"'{THEME['accent']}'")
        .replace("'EDF2F4'", f"'{THEME['light']}'")
        .replace("'FFFFFF'", f"'{THEME['bg']}'"))
    (slides_dir / "compile.js").write_text(template, encoding="utf-8")
    (slides_dir / "package.json").write_text(json.dumps({
        "name": f"{ts_code.lower().replace('.', '-')}-banker-deck-v2",
        "version": "0.0.1", "private": True,
        "dependencies": {"pptxgenjs": "^3.12.0"},
    }, indent=2))

    if not (slides_dir / "node_modules" / "pptxgenjs").exists():
        r = subprocess.run(["npm", "install", "--omit=dev", "--silent"],
                           cwd=str(slides_dir), capture_output=True,
                           text=True, timeout=180)
        if r.returncode != 0:
            sys.exit(f"npm install failed: {r.stderr[:500]}")

    r = subprocess.run(["node", "compile.js"], cwd=str(slides_dir),
                       capture_output=True, text=True, timeout=300)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    if r.returncode != 0:
        sys.exit(f"compile failed rc={r.returncode}")
    pptx = d / output_pptx
    print(f"OK: {pptx} ({pptx.stat().st_size} bytes, {len(slides)} slides; "
          f"{layout_counts})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
