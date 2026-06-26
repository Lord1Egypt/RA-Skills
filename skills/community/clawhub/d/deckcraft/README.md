# DeckCraft

> **AI-native PPTX generation with structured workflow, machine-readable QA gates, and multi-canvas output.**

Generate professional, **natively-editable** PowerPoint files (`.pptx`) with a 5-stage structured workflow. Every shape is a real DrawingML object — not an image — so users can click and edit any element in PowerPoint.

[![Version](https://img.shields.io/badge/version-5.2.0-blue)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## ✨ Features

- 🎨 **20+ high-level layout methods** — cover, TOC, content, comparison, table, chart, timeline, matrix, quote, summary, closing, and more
- 📐 **6 canvas presets** — `16:9`, `9:16`, `1:1`, `4:3`, `A4`, `A4-portrait` (mobile, square, classic, print)
- 🎨 **10 built-in themes** — business, tech, elegant, creative, green, red, ocean, etc.
- 📊 **Native charts** — bar, pie, line, gauge (using python-pptx's chart engine, not images)
- ✅ **5-stage structured workflow** — Brief → Structure → Content → Render+QA → Deliver
- 🚦 **Machine-readable QA gates** — `gate_check.py` + `gate_check_content.py` produce JSON verdict
- 🔄 **Checkpoint recovery** — resume mid-project without restarting
- 🌏 **CJK font support** — Noto Sans CJK SC built-in
- 🛠️ **3 interfaces** — Python API, CLI (`generate_ppt.py`), and outline-JSON mode

---

## 📦 Installation

```bash
pip install python-pptx lxml Pillow
```

Optional (for visual QA preview):

```bash
apt install libreoffice-impress poppler-utils fonts-noto-cjk
```

From source (after cloning):

```bash
git clone <repo> deckcraft
cd deckcraft
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### Python API

```python
import sys
sys.path.insert(0, "path/to/deckcraft")
from engine import DeckEngine

# 16:9 widescreen (default)
eng = DeckEngine(theme_name="business")
eng.cover(title="Q3 Marketing Plan", subtitle="Strategic Roadmap", author="Marketing Team", date="2026-06-03")
eng.toc(items=[("01", "Market Analysis", "Industry trends & competitor landscape")])
eng.content(title="Key Insights", bullets=["Gen-Z prefers short-form video", "ROI 2.3x on creator partnerships"], key_point="Lean into TikTok + Xiaohongshu")
eng.summary(title="Takeaways", key_points=["Lead with creative, not media"], conclusion="Approve 60% budget shift by June 15")
eng.closing(message="Questions?")
eng.save("q3_plan.pptx")
```

### CLI

```bash
python3 scripts/generate_ppt.py outline.json -o output.pptx --theme business --canvas 16:9
```

### Multi-canvas

```python
# 9:16 for social media (mobile, TikTok, Instagram Reels)
eng = DeckEngine(canvas="9:16")
eng.cover(title="Product Launch")
eng.content(title="Features", bullets=["Fast", "Beautiful", "Affordable"])
eng.save("launch_vertical.pptx")

# 1:1 for Instagram square
eng = DeckEngine(canvas="1:1")
# ... 

# A4 for printing
eng = DeckEngine(canvas="A4")
# ...
```

### Importing from existing documents (v5.3+)

Turn a PDF, DOCX, or Markdown file into a deck outline, then render:

```bash
# 1. Import → outline JSON
python3 scripts/import_source.py brief.pdf -o outline.json

# 2. Edit outline.json (optional) to fine-tune page types and content

# 3. Render → PPTX
python3 scripts/generate_ppt.py -i outline.json -o deck.pptx
```

Supported formats: **PDF** (via PyMuPDF), **DOCX** (via python-docx), **TXT**, **MD**.

The importer auto-classifies each section as `cover`, `toc`, `content`, `table`, or `stat_cards` using heuristics. You can override with `--page-types "cover,toc,content,..."`.

See [examples/](examples/) for full working samples.

---

## 🎨 Canvas Presets

| Preset | Dimensions | Aliases | Use Case |
|--------|------------|---------|----------|
| `16:9` (default) | 10.0" × 5.625" | `ppt`, `ppt-16x9` | Standard widescreen |
| `9:16` | 5.625" × 10.0" | `mobile` | Vertical/mobile (TikTok, Reels) |
| `1:1` | 7.5" × 7.5" | `square` | Square (Instagram) |
| `4:3` | 10.0" × 7.5" | — | Classic projector |
| `A4` | 11.69" × 8.27" | — | Print landscape |
| `A4-portrait` | 8.27" × 11.69" | — | Print portrait |

List all: `python3 -c "from engine.constants import list_canvases; print(list_canvases())"`

---

## 🏗️ The 5-Stage Workflow

```
S1 Brief → S2 Structure → S3 Content → S4 Render+QA → S5 Deliver
                          ⭐ gate        ⭐⭐ gate
```

### Stage 1: Brief
Collect audience, goal, duration, key messages, style. Output: `brief.md`

### Stage 2: Structure
Assign page types, write key points. Output: `outline.json`

### Stage 3: Content
Fill copy, numbers, chart data. Output: `content.json`

**⭐ Gate S3**: `python3 scripts/gate_check_content.py content.json <project>`

### Stage 4: Render + QA
Generate PPTX, then run QA. Output: `output.pptx`

**⭐⭐ Gate S4**: `python3 scripts/gate_check.py output.pptx <project>`

### Stage 5: Deliver
Hand off the PPTX.

**Fast Track** (≤5 pages, no charts, user says "quick"): skip S2/S3 gates, but **never skip S4 QA gate**.

---

## 📚 API Reference

### DeckEngine (20+ methods)

| Method | Purpose |
|--------|---------|
| `cover(title, subtitle, author, date, image_path)` | Title slide |
| `toc(items)` | Table of contents |
| `section_divider(title, section_number, subtitle)` | Section break |
| `content(title, bullets, key_point, image_path)` | Bullets + optional image |
| `content_with_icon(title, items)` | Icon-style content |
| `two_col(left_title, left_items, right_title, right_items)` | Side-by-side |
| `vs_compare(left_title, right_title, rows)` | Comparison table |
| `table(headers, rows, insights)` | Data table |
| `stat_cards(stats)` | KPI cards |
| `chart_bar/pie/line/gauge(...)` | Native charts |
| `timeline(milestones)` | Roadmap timeline |
| `process_flow(steps)` | Step-by-step flow |
| `matrix_2x2(quadrants)` | 2×2 grid |
| `quote(text, attribution)` | Quote slide |
| `image_full(image_path, caption)` | Full-width image |
| `image_split(image_path, bullets, image_side)` | Image + text |
| `kpi_dashboard(kpis)` | KPI dashboard |
| `team_grid(members)` | Team grid |
| `checklist(items, checked)` | Checklist |
| `summary(key_points, conclusion)` | Summary slide |
| `closing(title, message, contact)` | Thank you |
| `save(path)` | Save PPTX |

### Themes (10)

`business`, `business_dark`, `tech`, `tech_gradient`, `minimal`, `elegant`, `creative`, `green`, `red`, `ocean`

---

## 🧪 QA Gates

### S3 Content Gate

```bash
python3 scripts/gate_check_content.py content.json <project_dir>
```

Validates content JSON format. Catches:
- Unsupported page types
- Missing required fields
- Char budget overflow
- Element count exceeded

### S4 Render Gate

```bash
python3 scripts/gate_check.py output.pptx <project_dir>
```

Validates rendered PPTX. Catches:
- Text/shape overflow (off-slide)
- Image positioning issues
- Aspect ratio mismatches
- Font issues (rough check)

Both gates output machine-readable JSON. **AI must read the JSON verdict; verbal declaration is not accepted.**

---

## 🎯 Design Principles

1. **Native > Image** — Every shape is real DrawingML. Users can edit, recolor, reposition in PowerPoint.
2. **Canvas-aware** — Layouts adapt to aspect ratio. No content overflow.
3. **Theme-driven** — One `theme_name` swap changes entire deck's color/typography.
4. **Predictable** — Same API + same theme = same output. Easy to iterate.
5. **Composable** — Mix `content()`, `table()`, `chart_*()` in any order.

---

## 📁 Project Structure

```
deckcraft/
├── SKILL.md                     # Detailed skill spec
├── README.md                    # This file
├── CHANGELOG.md                 # Version history
├── LICENSE                      # MIT
├── requirements.txt             # Python dependencies
├── MIGRATION.md                 # Migration guides
├── engine/
│   ├── __init__.py
│   ├── constants.py             # 10 themes + 6 canvas presets
│   ├── core.py                  # Drawing primitives
│   ├── chart_engine.py          # Native bar/pie/line/gauge
│   └── deck_engine.py           # 20+ layout methods
├── scripts/
│   ├── generate_ppt.py          # CLI entry point
│   ├── gate_check.py            # S4 QA gate
│   └── gate_check_content.py   # S3 content gate
├── designs/
│   └── layout_matrix.yaml       # Layout constraints
├── examples/                    # Working code samples
│   ├── 01_basic_cover_to_closing.py
│   ├── 02_multi_canvas.py
│   └── 03_from_outline_json.py
└── tests/
    └── test_smoke.py            # Smoke test (all layouts × all canvases)
```

---

## 🤝 Contributing

Bug reports and PRs welcome. For major changes, please open an issue first.

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

## 🔗 Links

- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Migration**: [MIGRATION.md](MIGRATION.md)
- **Skill spec**: [SKILL.md](SKILL.md)
- **Examples**: [examples/](examples/)
