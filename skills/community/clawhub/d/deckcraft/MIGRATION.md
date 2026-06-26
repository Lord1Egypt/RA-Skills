# DeckCraft — Migration Guides

How to upgrade between major versions without breaking your existing code.

---

## v5.3 → v6.0 (PPT Master Integration)

### What changed

- **New `role_mode` parameter** on `DeckEngine.__init__` (default `"single"` — backward-compatible)
- **New canvas aliases** recognized by `DeckEngine` (8 new names: `xiaohongshu`, `moments`, `weibo`, `story`, `reels`, `ppt`, `mobile`, `square`)
- **New chart methods** on `chart_engine`: `chart_funnel`, `chart_gantt`, `chart_swot`, `chart_porter`, `chart_sankey`, `chart_heatmap`, `chart_radar`, `chart_treemap`, `chart_waterfall`
- **New icon API**: `from engine import icon, ICON_NAMES`
- **New industry color API**: `from engine import INDUSTRY_COLORS, get_industry_theme`
- **New source importers**: URL and WeChat article → MD (extends `scripts/import_source.py`)
- **New tools**: `scripts/optimize_crap.py` (CRAP design diagnostic), `scripts/add_notes.py` (speaker notes injection)
- **New templates**: `templates/design_spec.md` and `templates/design_spec_demo.md`
- **New test files**: `tests/test_charts_extended.py` (23 tests), `tests/test_role_mode.py` (12 tests)
- **New examples**: `examples/05_icons.py`, `examples/06_role_mode.py`

### Migration steps

#### If you used `DeckEngine()` with no args

**No changes needed.** Default `theme_name="business"`, `canvas="16:9"`, `role_mode="single"` preserves exact v5.3 behavior.

```python
# v5.3 and v6.0 — same code, same output
eng = DeckEngine(theme_name="business")
eng.cover(title="Hello")
eng.save("out.pptx")
```

#### If you specified `canvas="16:9"` (or any existing preset)

**No changes needed.** All v5.3 canvas names (`16:9`, `9:16`, `1:1`, `4:3`, `A4`, `A4-portrait`, `ppt-16x9`, `mobile`, `square`, `ppt`) still work.

#### If you want to try a new alias

```python
# v6.0: new alias names map to existing canvases
eng = DeckEngine(canvas="xiaohongshu")  # → 9:16
eng = DeckEngine(canvas="moments")      # → 1:1
eng = DeckEngine(canvas="story")        # → 9:16
```

#### If you want to try multi-role workflow (optional)

```python
# v6.0: opt-in multi-role mode
eng = DeckEngine(theme_name="business", canvas="16:9", role_mode="multi")
plan = eng.strategist_plan(brief={...})  # LLM fills this
eng.execute_plan(plan)                   # LLM-driven generation
```

Default `role_mode="single"` keeps the v5.3 single-pass behavior.

#### If you want new chart types

```python
eng.chart_funnel(title="Funnel", stages=["A","B","C","D"], values=[100, 80, 40, 20])
eng.chart_swot(title="SWOT", strengths=[...], weaknesses=[...], opportunities=[...], threats=[...])
eng.chart_heatmap(title="Heatmap", rows=[...], cols=[...], values=[[...]])
# ... and 6 more
```

#### If you want icons

```python
from engine import icon
icon(slide=eng._current_slide, name="rocket", x=100, y=100, size=48, color="FF6B35")
```

#### If you want industry colors

```python
from engine import get_industry_theme
theme = get_industry_theme("tech")  # {"primary": "#1565C0", "secondary": "#42A5F5", "accent": "#FF6B35", ...}
```

### What we did NOT do (and why)

- ❌ **No SVG-embed rendering pipeline** — DeckCraft remains python-pptx native (PPTX is editable in PowerPoint)
- ❌ **No forced multi-role workflow** — default is `role_mode="single"` (fast, single LLM pass)
- ❌ **No PPT-incompatible SVG features** (filter, mask, clipPath) — DeckCraft is PPTX-pure

### Testing the upgrade

```bash
# All v5.3 tests still pass
python3 tests/test_smoke.py            # 95 tests
python3 tests/test_validation.py       # 20 tests
python3 tests/test_importers.py        # 34 tests

# New v6.0 tests
python3 -m pytest tests/test_charts_extended.py  # 23 tests
python3 -m pytest tests/test_role_mode.py        # 12 tests

# All v5.3 examples still work
python3 examples/01_basic_cover_to_closing.py
python3 examples/02_multi_canvas.py
python3 examples/03_from_outline_json.py
python3 examples/04_from_source.py

# New v6.0 examples
python3 examples/05_icons.py
python3 examples/06_role_mode.py
```

All 150 tests + 6 examples should pass.

---

## v5.2 → v5.3 (Source Importers)

### What changed

- **New `engine.importers` package** for PDF/DOCX/MD → outline conversion
- **New `scripts/import_source.py` CLI** for batch import
- **New example**: `examples/04_from_source.py`
- **New test**: `tests/test_importers.py` (34 tests)
- **New dependencies**: `PyMuPDF>=1.23.0`, `python-docx>=1.0.0`

### Migration steps

#### No code changes needed

The v5.3 release is purely **additive**. All v5.2 code continues to work unchanged.

#### To use the new import feature

```bash
# 1. Install new dependencies
pip install -r requirements.txt

# 2. Import a document
python3 scripts/import_source.py brief.pdf -o outline.json

# 3. Render (use existing CLI)
python3 scripts/generate_ppt.py -i outline.json -o deck.pptx
```

Or use the Python API:

```python
from engine.importers import detect_and_import
outline = detect_and_import("brief.pdf", theme="business", canvas="16:9")
```

### Limitations (v5.3 first cut)

- Importers use heuristics for page-type classification — always review the output
- Image extraction from PDF/DOCX is not supported in v5.3 (text-only)
- Complex tables may not be detected — use `--page-types` to override

### Testing the upgrade

```bash
pip install pymupdf python-docx
python3 tests/test_smoke.py        # 95 tests
python3 tests/test_validation.py   # 20 tests
python3 tests/test_importers.py    # 34 tests (new)
```

All 149 tests should pass.

---

## v5.1 → v5.2 (Multi-Canvas)

### What changed

- `DeckEngine.__init__()` accepts a new `canvas` parameter (default: `"16:9"`)
- Module-level constants (`SLIDE_WIDTH`, `SLIDE_HEIGHT`, `MARGIN_LEFT`, etc.) are now instance attributes (`self.cw`, `self.ch`, `self.ml`, etc.) on `DeckEngine`. **Direct imports of these constants are no longer supported.**
- New: 6 canvas presets + 4 aliases

### Migration steps

#### If you used `DeckEngine()` with no args

**No changes needed.** Default `canvas="16:9"` preserves exact v5.1 behavior.

```python
# v5.1 and v5.2 — same code, same output
eng = DeckEngine(theme_name="business")
eng.cover(title="Hello")
eng.save("out.pptx")
```

#### If you imported constants directly from `engine.constants`

**BREAKING:** Module-level constants are removed. Use `get_canvas()` or the `DeckEngine` instance attributes.

```python
# ❌ v5.1 (no longer works)
from engine.constants import SLIDE_WIDTH, SLIDE_HEIGHT
x = SLIDE_WIDTH / 2  # crashes in v5.2

# ✅ v5.2: use DeckEngine instance attributes
eng = DeckEngine(canvas="16:9")
x = eng.cw / 2

# ✅ v5.2: use get_canvas() for canvas-agnostic access
from engine.constants import get_canvas
canvas = get_canvas("16:9")
x = canvas["width"]
```

#### If you need a non-16:9 canvas

**New in v5.2.** Add the `canvas` parameter:

```python
# 9:16 for mobile/social (TikTok, Reels, Stories)
eng = DeckEngine(canvas="9:16")

# 1:1 for Instagram square
eng = DeckEngine(canvas="1:1")

# A4 for print
eng = DeckEngine(canvas="A4")
```

See [README.md](README.md#canvas-presets) for the full list of presets and aliases.

#### If you customized layout internals via Inches()

**Most layout positions are now canvas-aware.** If you monkey-patched `deck_engine.py` to use specific `Inches()` values, you may need to recompute for the new canvas dimensions. The 16:9 default still works identically.

### Behavior change: input validation

**v5.2 raises** for invalid inputs that v5.1 silently accepted:

```python
# v5.1: silently created a slide with empty content
eng.cover(title="")

# v5.2: raises ValueError
# ValueError: title is required (got empty string)
```

If your code generates titles dynamically, add a default or guard:

```python
title = user_input.get("title", "Untitled") or "Untitled"
eng.cover(title=title)
```

### Behavior change: slide counts

v5.2 fixes a bug where `cover()`, `content()`, `closing()`, and `summary()` each added **2 slides** per call. They now correctly add **1 slide** per call.

If you depended on this bug, add an explicit no-op call to compensate (not recommended).

### New CLI options

```bash
# v5.1
python3 generate_ppt.py --outline out.json --output out.pptx --style business

# v5.2: --style renamed to --theme, plus new --canvas
python3 generate_ppt.py -i out.json -o out.pptx --theme business --canvas 16:9

# New: list available themes/canvases
python3 generate_ppt.py --list-themes
python3 generate_ppt.py --list-canvases
```

### Testing the migration

After upgrading, run:

```bash
python3 tests/test_smoke.py        # 95 layout × canvas tests
python3 tests/test_validation.py   # 20 input validation tests
```

Both should pass. If your existing code uses canvas="16:9" (default), it should work unchanged.

---

## v5.0 → v5.1 (Gate Refinements)

v5.1 was a refinement release. The 5-stage workflow and core API are unchanged from v5.0. The main additions were:

- `gate_check_content.py` for S3 content gate (was implicit before)
- `Checkpoint Recovery` section in SKILL.md
- `Anti-Patterns` section in SKILL.md
- Stronger error messages in `gate_check.py`

No code changes required for v5.0 → v5.1.

---

## v4 → v5 (Major Rewrite)

v5 introduced the 5-stage structured workflow. The v4 API (`create_slide()`, `add_text()`, etc.) was replaced by high-level layout methods (`cover()`, `content()`, `two_col()`, etc.).

If you have v4 code, you'll need to rewrite. The new API is significantly higher-level and produces better output. See [SKILL.md](SKILL.md#deckengine-api) for the full v5 API.
