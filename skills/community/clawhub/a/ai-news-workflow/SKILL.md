# AI News Workflow

This skill collects AI industry news (RSS + web pages), filters/deduplicates/classifies them, optionally generates Chinese titles & ~80-char summaries(recommended 60-100,hard cap ~110) via Doubao (Volcengine Ark), and exports Excel tables + a Word briefing.

## How to run
- Entry: `skill_entry.py`
- Init (optional): `python skill_entry.py --init`
- Run: `python skill_entry.py`

## Inputs
Put these files under `./input/`:
- 企业名单.xlsx
- source_config.xlsx
- web_source_config.xlsx (optional)

## Outputs
Generated under `./output/`:
- Excel: `./output/excel/`
- Word: `./output/word/`

## Optional: Ark API
Provide API key via environment variable:
- `ARK_API_KEY`

Model can be selected at runtime:
- `python skill_entry.py --model <MODEL_NAME>`