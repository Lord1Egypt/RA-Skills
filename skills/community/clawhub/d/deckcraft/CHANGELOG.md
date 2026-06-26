# DeckCraft Changelog

## [6.0.0] - 2026-06-11 — PPT Master Integration (Icon Library / Source Auto-Fetch / CRAP Optimizer / Multi-Role Workflow / 9 New Charts / Industry Colors)

> **Major release** — borrows select capabilities from PPT Master (@lzfxxx, ClawHub score 3.69) while preserving DeckCraft's core philosophy: **python-pptx native (PPTX is editable, not a SVG image dump) + machine-readable gates + 5-stage discipline**.

### Tier 1 (Must-Have)

- **Icon Library (`engine/icons.py`)** — 37 hand-built icons rendered as `python-pptx` native freeform shapes
  - No SVG embedding — every icon is editable in PowerPoint
  - `from engine import icon, ICON_NAMES` — 37 icons: `arrow-right`, `arrow-up`, `arrow-up-right`, `bell`, `bookmark`, `calendar`, `chart-bar`, `check`, `circle-checkmark`, `clock`, `cog`, `download`, `edit`, `file`, `filter`, `mail`, `map-pin`, `phone`, `rocket`, `search`, `settings`, `shield`, `star`, `target`, `trending-up`, `user`, `users`, `video`, `zap`, etc.
  - New example: `examples/05_icons.py`

- **URL → Markdown importer (`importers/url.py`)** — fetch any URL and convert HTML → MD
  - CLI: `python3 scripts/import_source.py url https://example.com -o out.md`

- **WeChat Article → Markdown importer (`importers/wechat.py`)** — bypass WeChat anti-scraping with custom UA + Referer
  - CLI: `python3 scripts/import_source.py wechat https://mp.weixin.qq.com/s/xxx -o out.md`

- **CRAP Design Optimizer (`scripts/optimize_crap.py`)** — optional Stage 4.5 diagnostic
  - Four-dimension analysis: **C**ontrast / **R**epetition / **A**lignment / **P**roximity
  - Reads PPTX shapes via python-pptx, outputs MD report (does NOT modify the deck)
  - Use the report to drive a follow-up LLM-driven optimization pass

- **Speaker Notes Module (`scripts/add_notes.py` + `generate_ppt.py --notes-file`)**
  - Input: `notes.json` (format: `{"1": "page 1 notes", "2": "page 2 notes"}`)
  - Writes to `slide.notes_slide.notes_text_frame.text` for every slide
  - Integrated as post-processing step in `generate_ppt.py`

### Tier 2 (Recommended)

- **9 New Chart Types (`engine/chart_engine.py`)** — all python-pptx native, no SVG fallback
  - `chart_funnel(title, stages, values)` — horizontal funnel, 5-7 stages
  - `chart_gantt(title, tasks, start_date, end_date)` — timeline + task bars
  - `chart_swot(title, strengths, weaknesses, opportunities, threats)` — 2x2 SWOT matrix
  - `chart_porter(title, forces)` — Porter's Five Forces (5 circles around center)
  - `chart_sankey(title, nodes, links)` — simplified flow diagram (rectangles + trapezoid connectors)
  - `chart_heatmap(title, rows, cols, values)` — color-mapped grid (green→yellow→red)
  - `chart_radar(title, axes, series_data, series_names)` — polygon-based radar
  - `chart_treemap(title, items)` — squarified single-level treemap
  - `chart_waterfall(title, categories, values, is_total)` — waterfall (start/+/-/end + connector line)
  - New test file: `tests/test_charts_extended.py` (23 tests, all pass)

- **Multi-Role Workflow (Optional) — `role_mode="multi"`**
  - `DeckEngine(theme_name="business", role_mode="multi")` enables a Strategist → Executor two-phase flow
  - `eng.strategist_plan(brief)` returns a plan schema for LLM to fill
  - `eng.execute_plan(plan)` consumes LLM-filled plan and generates slides
  - **Default is `role_mode="single"`** — single-pass LLM flow unchanged from v5.3
  - New example: `examples/06_role_mode.py` (12 tests in `tests/test_role_mode.py`)

- **Design Spec Template (`templates/design_spec.md` + `templates/design_spec_demo.md`)**
  - Standardized 9-section design spec: canvas / page count / audience / style / colors / icons / images / typography / speaker notes
  - Bridges brief.md → design spec → content.json
  - Borrowed from PPT Master `design_spec_reference.md`, trimmed to DeckCraft essentials

### Tier 3 (Nice-to-Have)

- **8 New Canvas Aliases** — `xiaohongshu`, `moments`, `weibo`, `story`, `reels`, `ppt`, `mobile`, `square`
  - `xiaohongshu` / `story` / `reels` / `mobile` → 9:16
  - `moments` / `weibo` / `square` → 1:1
  - `ppt` → 16:9
  - Total 15 canvas names (7 presets + 8 aliases), accessible via `list_canvases()`

- **14 Industry Color Palettes (`INDUSTRY_COLORS` + `get_industry_theme()`)**
  - `finance`, `tech`, `healthcare`, `government`, `education`, `retail`, `manufacturing`, `energy`, `media`, `real_estate`, `fashion`, `food`, `travel`, `consulting`
  - Each: `primary` (60%) + `secondary` (30%) + `accent` (10%) + `label`
  - 60-30-10 color rule baked in

- **Image Resource Manifest (`engine/importers/__init__.py: extract_image_manifest`)**
  - Extracts `![](...)` references from MD sources, generates PPT Master-style manifest
  - Output: list of `{filename, size, aspect_ratio, layout_hint, usage, type, status}` dicts
  - Integrated into `import_source.py` output as `<content>.images.json`

### What we DID NOT borrow from PPT Master (and why)

- ❌ **SVG-only rendering pipeline** — would lose PowerPoint editability (DeckCraft's core value)
- ❌ **Forced multi-role reading** — default is still single-pass LLM (faster, cheaper); `role_mode="multi"` is opt-in
- ❌ **PPT-incompatible SVG features** (filter, mask, clipPath) — DeckCraft remains PPTX-pure
- ❌ **Heavy project_manager / image analysis pipeline** — DeckCraft stays lightweight

### Test coverage

- 95 smoke + 20 validation + 23 charts_extended + 12 role_mode = **150 tests, all passing**
- 6 examples work end-to-end (cover→closing, multi-canvas, outline JSON, source import, icons, role_mode)

### Compatibility

- ✅ **Default `role_mode="single"` and default `canvas="16:9"` are 100% backward-compatible with v5.3**
- ✅ All v5.3 examples (`01-04`) work unchanged
- ✅ All v5.3 importer APIs (`detect_and_import`, `pdf_to_outline`, `docx_to_outline`, `text_to_outline`) work unchanged
- 🆕 New optional `role_mode` parameter, new optional `xiaohongshu` etc. canvas names
- See [MIGRATION.md](MIGRATION.md) for full upgrade guide

---

## [5.3.0] - 2026-06-03 — Source Importers

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [5.3.0] - 2026-06-03 — Source Importers

### Added

- **New `engine.importers` package** for converting documents to outline JSON:
  - `pdf_to_outline()` — PDF → outline via PyMuPDF
  - `docx_to_outline()` — Word .docx → outline via python-docx
  - `text_to_outline()` — .txt / .md → outline (built-in)
  - `detect_and_import()` — auto-detect format by extension
- **New `scripts/import_source.py` CLI**:
  - `python3 scripts/import_source.py <file.pdf|docx|txt|md> -o outline.json`
  - Options: `--theme`, `--canvas`, `--page-types`, `--max-pages`, `--print`
  - Supports PDF, DOCX, TXT, MD
- **Heuristic page-type classification**:
  - First page → `cover`
  - "Agenda"/"目录" headings + numbered lists → `toc`
  - "Part N"/"Section N" → `section`
  - Pipe-delimited tables → `table`
  - "99% Uptime" / "$2M Revenue" patterns → `stat_cards`
  - Default → `content`
- New example: `examples/04_from_source.py` (end-to-end PDF → PPTX)
- New test: `tests/test_importers.py` (34 tests covering heuristics + 3 importers)
- New dependencies: `PyMuPDF>=1.23.0`, `python-docx>=1.0.0`

### Test coverage

- 95 smoke + 20 validation + 34 importers = **149 tests, all passing**
- End-to-end: PDF/DOCX → outline → PPTX → gate_check 100/100

### Notes

- Importers are heuristic — review the generated outline and adjust before publishing
- Manual page-type override: pass `--page-types "cover,toc,content,..."` to skip heuristic
- See [README.md#importing-from-existing-documents](README.md) for the full workflow

---

## [5.2.0] - 2026-06-03 — Multi-Canvas Support

### Added

- **New `canvas` parameter** for `DeckEngine.__init__()`
- **6 canvas presets** with **4 aliases**:
  - `16:9` (default) — 10.0" × 5.625" — widescreen (alias: `ppt`, `ppt-16x9`)
  - `9:16` — 5.625" × 10.0" — vertical mobile (TikTok/Reels/Stories) (alias: `mobile`)
  - `1:1` — 7.5" × 7.5" — square (Instagram) (alias: `square`)
  - `4:3` — 10.0" × 7.5" — classic projector
  - `A4` — 11.69" × 8.27" — print landscape
  - `A4-portrait` — 8.27" × 11.69" — print portrait
- New helper API: `from engine.constants import list_canvases`
- New tests: `tests/test_smoke.py` (95 layout × canvas tests) + `tests/test_validation.py` (20 input validation tests)
- New CLI options: `--theme`, `--canvas`, `--list-themes`, `--list-canvases` in `generate_ppt.py`
- New documentation: `README.md`, `MIGRATION.md`, `LICENSE`
- New examples: `examples/01_basic_cover_to_closing.py`, `examples/02_multi_canvas.py`, `examples/03_from_outline_json.py`

### Changed

- **Refactored** `deck_engine.py` geometry calculations:
  - Module-level constants `SLIDE_WIDTH/SLIDE_HEIGHT/MARGIN_*/CONTENT_*` replaced with instance attributes `self.cw/self.ch/self.ml/...` (74 references updated)
  - All 20 layout methods now use canvas-aware calculations instead of hardcoded `Inches()` values
- **Input validation** on `__init__`, `cover`, `closing`, `content`, `summary`, `save`:
  - Invalid theme/canvas raises `ValueError` with helpful list of valid options
  - Empty/None text raises `ValueError`
  - Non-string text raises `TypeError`
  - Out-of-bounds lists raise `ValueError`
  - Non-`.pptx` path raises `UserWarning`
  - Missing image file raises `UserWarning` (slide is still created)
- **Type hints** added to `__init__`, `cover`, `closing`, `content`, `summary`, `save`, plus helpers `_validate_text/_validate_list/_validate_int/_validate_image_path`
- **Improved CLI** (`generate_ppt.py`): full argparse, `--help`, error handling, exit codes
- 4 layout methods (cover/content/closing/summary) had a bug where each call added 2 slides instead of 1. **Fixed.**

### Compatibility

- ✅ **16:9 default behavior is 100% backward-compatible** with v5.1
- ❌ Direct imports of `SLIDE_WIDTH`/`SLIDE_HEIGHT`/`MARGIN_*`/`CONTENT_*` from `engine.constants` are removed (use `DeckEngine` instance attributes or `get_canvas()`)
- See [MIGRATION.md](MIGRATION.md) for upgrade guide

### Testing

- 95 layout × canvas smoke tests pass (5 canvases × 19 layouts)
- 20 input validation tests pass
- 4 layouts × 19 layouts gate check: all 100/100

---

## [5.1.1] - 2026-05 (ClawHub release)

Initial ClawHub release. 5-stage workflow, gate mechanisms, 20+ layout methods.

### Highlights

- 5-stage generation flow: Brief → Structure → Content → Render+QA → Deliver
- 20+ high-level layout methods
- 10 built-in color themes
- 2 QA gates (S3 content + S4 render)
- Checkpoint recovery
- Anti-patterns documentation

---

## [5.0.0] - 2026-04 (Initial release)

Major rewrite from v4. New high-level API, structured workflow, native chart support.

### Highlights

- Replaced v4's low-level `create_slide()`/`add_text()` with high-level layout methods
- Native chart support via python-pptx (bar, pie, line, gauge)
- 10 built-in themes
- CJK font support
