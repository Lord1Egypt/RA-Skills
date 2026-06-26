# client-report-generator — Status

**Status:** Ready
**Price:** $79
**Created:** 2026-03-27

## What It Does
Generates professional client-facing reports from CSV, JSON, or raw data. Includes data parsing, metric detection, trend analysis, and HTML export with multiple themes.

## Components
- `SKILL.md` — Main skill instructions with workflow
- `scripts/parse_data.py` — Data parser (CSV/TSV/JSON → normalized metrics)
- `scripts/report_to_html.py` — Markdown → styled HTML converter (3 themes)
- `references/report-templates.md` — 4 detailed report templates

## Testing
- [x] parse_data.py tested with CSV data (currency, percentage, count detection works)
- [x] parse_data.py tested with JSON array data
- [x] report_to_html.py tested with sample report (default theme)
- [x] report_to_html.py tested with branded theme
- [x] All scripts executable

## Next Steps
- Package to .skill file
- Publish to ClawHub
