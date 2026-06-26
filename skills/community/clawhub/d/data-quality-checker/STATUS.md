# data-quality-checker — Status

**Status:** Ready
**Price:** $59
**Created:** 2026-03-30

## What It Does
Validates CSV/JSON/JSONL data for quality issues: missing values, duplicates, type inconsistencies, outliers, format violations, whitespace, empty columns, schema drift. Quality score 0-100. Schema validation and auto-generation. Pure Python, no deps.

## Components
- `scripts/check_data_quality.py` — main checker (8 checks, 3 output formats)
- Tested with CSV and JSON sample data

## Next Steps
- [x] Published to ClawHub (after April 11)
- [ ] Add JSONL streaming for large files
- [ ] Add --fix mode for auto-corrections
