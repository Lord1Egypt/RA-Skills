---
name: deckcraft
description: >
  AI PPT creation skill with structured 5-stage generation, machine-readable QA gates,
  checkpoint recovery, and experience accumulation. 20 layout methods, native charts,
  visual QA pipeline, automated gate checks, and multi-canvas output (16:9/9:16/1:1/4:3/A4).
---

# DeckCraft v6 — Harness Engineering

> **Version**: 6.0.0 · **Engine**: DeckEngine (python-pptx native charts) + ChartEngine (native)
>
> **Required tools**: Read, Write, Bash
> **Requires**: `pip install python-pptx lxml Pillow`
> **Render QA**: LibreOffice Impress (soffice --headless) + poppler-utils (pdftoppm)

---

## Anti-Patterns (Read Before Every Generation)

### Anti-Pattern 1: Declaring "Gate Passed" Verbally

**Wrong**: "QA found 5 errors but all are minor, gate passed."
**Correct**: Run `gate_check.py`, read the JSON, only `"passed": true` means pass.

### Anti-Pattern 2: "I Checked In My Head"

Format errors in content JSON are invisible to mental review.
**Correct**: Run `gate_check_content.py`, read the JSON output.

### Anti-Pattern 3: Skipping the Process for "Simple" Decks

Even simple decks can have overflow, font issues, or broken layouts.
**Correct**: Use Fast Track (see below), but **never skip the QA gate**.

---

## HARD RULES

1. **Every generation must follow the 5-stage flow**
2. **Gates must be machine-readable** — run the script, read the JSON
3. **Experience accumulation is recommended** — note pattern-level fixes for future improvement
4. **All positioning values must use `int()` wrapping** for python-pptx
5. **Clear paragraphs before adding runs** — never assume `p.runs[0]` exists

---

## 5-Stage Generation Flow

```
S1 Brief → S2 Structure → S3 Content → S4 Render+QA → S5 Deliver
                          ⭐ gate        ⭐⭐ gate
```

### Stage 1: Brief

Collect: audience, goal, duration, key messages, style preference.
**Output**: `<project>/brief.md`

**Design Spec Template (v6.0+)**: Use `templates/design_spec.md` to capture structured design decisions (canvas, page count, audience, color scheme, typography, speaker notes). A filled example is at `templates/design_spec_demo.md`. Recommended for any deck ≥ 8 pages.

### Stage 2: Structure

Assign page types, write key points (full insight sentences).
**Output**: `<project>/outline.json`

### Stage 3: Content

Fill copy, numbers, chart data. Respect char budgets in `designs/layout_matrix.yaml`.
**Output**: `<project>/content.json`

**⭐ Gate S3**:

```bash
python3 scripts/gate_check_content.py <project>/content.json <project>
```

Read `gate_content.json` — only `"passed": true` allows proceeding.

### Stage 4: Render + QA

Generate PPTX from content.json, then run QA.

```bash
python3 scripts/gate_check.py <pptx_path> <project>
```

Read `gate_result.json` — only `"passed": true` allows proceeding.

**Visual QA (render preview)**:

```bash
# Render PPT → PDF → PNG for visual inspection
soffice --headless --convert-to pdf <pptx_path> --outdir <project>/
pdftoppm -png -r 200 <pdf_path> <project>/preview/slide
```

Inspect the PNG images to verify layout, fonts, colors, and chart rendering.
Fix any visual issues found, regenerate, and re-run gate.

### Stage 5: Deliver + Self-Refinement

Deliver the PPTX.

---

## Fast Track (Simple Requests)

When **all** conditions are met, skip S2/S3 gates:
- Total pages ≤ 5
- No data charts
- User says "quick" / "fast" / "simple"

**Still required**: S1 + S4 QA gate + S5 delivery.

---

## Checkpoint Recovery

When resuming a deck project, check which files exist:

- No `brief.md` → Stage 1
- No `outline.json` → Stage 2
- No `content.json` → Stage 3
- No `gate_content.json` → Stage 3-gate
- No `.pptx` → Stage 4
- No `gate_result.json` → Stage 4-gate
- All present → Stage 5

Resume from the identified stage. Do not restart from S1.

---

## DeckEngine API

```python
import sys, os
sys.path.insert(0, '<skill-path>')
from engine import DeckEngine

# v5.2+: canvas parameter (16:9 / 9:16 / 1:1 / 4:3 / A4)
eng = DeckEngine(theme_name="business", canvas="16:9")  # default
eng = DeckEngine(theme_name="business", canvas="9:16")   # vertical mobile (TikTok, Reels, Stories)
eng = DeckEngine(theme_name="business", canvas="1:1")    # square (Instagram)
eng = DeckEngine(theme_name="business", canvas="4:3")    # classic projector
eng = DeckEngine(theme_name="business", canvas="A4")     # print landscape

# v6.0+: Multi-role mode (optional strategist → executor workflow)
eng = DeckEngine(theme_name="business", canvas="16:9", role_mode="multi")
plan = eng.strategist_plan({"title": "My Brief"})  # get plan template
# ... fill plan with your LLM ...
eng.execute_plan(filled_plan)                       # generate from plan
eng.cover(title="Title", subtitle="Sub", author="Author", date="2026")
eng.toc(items=[("1", "Chapter", "Description")])
eng.section_divider("Section Title", section_number=1)
eng.content(title="Slide", bullets=["Point 1", "Point 2"], key_point="Insight")
eng.content_with_icon(title="Slide", items=[("01", "Head", "Desc")])
eng.two_col(title="Compare", left_title="A", left_items=[], right_title="B", right_items=[])
eng.vs_compare(title="VS", left_title="Before", right_title="After", rows=[("Dim", "Val1", "Val2")])
eng.table(title="Data", headers=["H1", "H2"], rows=[["a", "b"]], insights=["Key takeaway"])
eng.stat_cards(title="KPIs", stats=[("99%", "Uptime"), ("$2M", "Revenue")])
eng.chart_bar(title="Revenue", data=[[4.2, 3.8]], labels=["A", "B"], series_names=["S1"])
eng.chart_pie(title="Mix", data=[45, 30, 25], labels=["X", "Y", "Z"], donut=True)
eng.chart_line(title="Trend", data=[[1, 2, 3]], labels=["Q1", "Q2", "Q3"])
eng.chart_gauge(title="Score", value=87, max_value=100, label="NPS")
eng.timeline(title="Roadmap", milestones=[("Q1", "Launch"), ("Q2", "Scale")])
eng.process_flow(title="Steps", steps=["Research", "Build", "Launch"])
eng.matrix_2x2(title="Priority", quadrants=[("TL", "desc"), ("TR", "desc"), ("BL", "desc"), ("BR", "desc")])
eng.quote(title="Insight", quote_text="Words matter.", attribution="Author")
eng.image_full(title="Visual", image_path="photo.jpg", caption="Detail")
eng.image_split(title="Split", image_path="photo.jpg", bullets=["Point"])
eng.kpi_dashboard(title="Dashboard", kpis=[("Revenue", 12.4, 15, "M")])
eng.team_grid(title="Team", members=[("Name", "Role")])
eng.checklist(title="Tasks", items=["Task 1", "Task 2"], checked=[True, False])
eng.summary(title="Takeaways", key_points=["Point 1"], conclusion="Next step")
eng.closing(title="Thank You", message="Questions?")  # no page_num (closing slide)
eng.save("output.pptx")
```

**10 themes**: business, business_dark, tech, tech_gradient, minimal, elegant, creative, green, red, ocean

**Canvas presets (v5.2+)**: `16:9` (default, widescreen), `9:16` (vertical mobile, TikTok/Reels/Stories), `1:1` (square, Instagram), `4:3` (classic projector), `A4` (print landscape), `A4-portrait`. Aliases: `mobile`=9:16, `square`=1:1, `ppt`=16:9.

List available canvases: `from engine.constants import list_canvases; print(list_canvases())`

---

## Design Guide

### Color

Extract from user's original PPT first. Pick a bold palette matching the topic.
One dominant color (60-70%), 1-2 supporting, one sharp accent.

### Typography

| Element | Size | Notes |
|---------|------|-------|
| Slide title | 26-36pt bold | Must stand out |
| Body text | 14-16pt | Never below 10pt |
| Captions | 10-12pt | Muted color |

CJK: Noto Sans CJK SC / Latin: Arial / Calibri

### Spacing

- Minimum margin: 0.5"
- Between blocks: 0.3-0.5"
- Leave breathing room

### Avoid

- Repeating the same layout on every slide
- Text-only slides — add visual elements
- Center-aligned body text
- Low-contrast text (light on light, dark on dark)

---

## Dependencies

| Tool | Install |
|------|---------|
| python-pptx | `pip install python-pptx` |
| lxml | `pip install lxml` |
| Pillow | `pip install Pillow` |

**Render QA (optional but recommended)**:

| Tool | Install |
|------|----------|
| LibreOffice Impress | `apt install libreoffice-impress` |
| poppler-utils | `apt install poppler-utils` |
| Noto Sans CJK | `apt install fonts-noto-cjk` |

---

## Skill File Structure

```
deckcraft/
├── SKILL.md                     # This file
├── engine/
│   ├── __init__.py
│   ├── constants.py             # 10 theme color palettes, typography, grid
│   ├── core.py                  # Drawing primitives, XML cleanup, CJK font
│   ├── chart_engine.py          # Native bar/pie/line/gauge charts (python-pptx)
│   ├── deck_engine.py           # 20 layout methods, 40+ high-level API
│   └── importers/               # v5.3+ source importers
│       ├── __init__.py
│       ├── base.py              # Shared heuristics
│       ├── pdf.py               # PDF → outline (PyMuPDF)
│       ├── docx.py              # DOCX → outline (python-docx)
│       └── text.py              # TXT/MD → outline
├── scripts/
│   ├── generate_ppt.py          # CLI: outline JSON → PPTX
│   ├── import_source.py         # v5.3+ CLI: PDF/DOCX/MD → outline
│   ├── gate_check.py            # S4 QA gate → gate_result.json
│   └── gate_check_content.py   # S3 content gate → gate_content.json
├── designs/
│   └── layout_matrix.yaml       # 23 layout definitions with char budgets
├── examples/                    # Working code samples
│   ├── 01_basic_cover_to_closing.py
│   ├── 02_multi_canvas.py
│   ├── 03_from_outline_json.py
│   └── 04_from_source.py        # v5.3+
└── tests/
    ├── test_smoke.py            # 95 layout × canvas tests
    ├── test_validation.py       # 20 input validation tests
    └── test_importers.py        # v5.3+ 34 importer tests
```
