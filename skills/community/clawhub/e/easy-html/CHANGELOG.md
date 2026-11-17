# Changelog

All notable changes to `easy-html` are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/); versions follow [SemVer](https://semver.org/).

## v1.0.1

Documentation only — no code change.

- Added a **Website** link to the top of `SKILL.md` and the README, pointing at the new
  landing page: <https://songhonglei.github.io/html-tool-suite/easy-html/> — it lists all
  19 themes and recolours itself when you click one, so the page doubles as a live demo.

## v1.0.0 (open-source first release)

First public release of `easy-html` — a content-to-polished-webpage pipeline for AI agents.

- **Two-path design**: automatically decides between *rebuild* (loose content → semantic
  skeleton → theme) and *layout inheritance* (already-elegant HTML/image → keep the layout,
  swap only the colour theme via 7 `--eh-*` semantic variables).
- **Input normalisation** (`ingest.py`): Markdown, plain text, `.xlsx` (openpyxl),
  `.docx` (zero-dependency parser), pasted tables, stdin → structured JSON blocks.
  Legacy `.xls`/`.doc` produce an explicit downgrade hint.
- **Visualisation-first skeleton generation**: a mandatory scan step turns key numbers,
  ratios, rankings, trends, flows and timelines into visual components or real charts
  instead of dumping them as plain tables.
- **Three-layer asset injection** (`apply_layout.py`): responsive layout base,
  a CSS visualisation component library (KPI cards, progress bars, donuts, bars,
  flow, timeline, tag cloud, VS blocks), and a Chart.js renderer with multi-CDN fallback.
- **19 built-in themes** (`apply_style.py`) reusing the CSS engine from the sibling project
  [html-golive](https://github.com/Songhonglei/html-golive) — themes carry colour only,
  layout stays with the skill, so the two layers never conflict.
- **Title / FavIcon** (`set_meta.py`, `make_favicon.py`): idempotent `<title>` replacement
  and zero-dependency emoji/glyph → SVG data-URI favicons.
- **Pluggable CSS engine resolution** (`_engine.py`): `EASY_HTML_CSS_ENGINE` →
  installed `golive` package → local `html-golive` source tree. Fails loudly with install
  guidance; never downloads anything silently.
- Configurable output directory via `EASY_HTML_OUT`; custom Chart.js sources via
  `window.EH_CHART_CDN` for offline/private networks.
