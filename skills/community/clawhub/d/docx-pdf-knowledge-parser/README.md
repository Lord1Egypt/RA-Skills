# feishu-knowledge-ingest

Minimal v0.1 skill skeleton for report-first ingestion of Feishu folders and single attachments.

## v0.1 decisions
- Inputs: Feishu folder or single attachment
- Parsers: `.docx`, `.pdf`
- Outputs:
  - `ingest-report.md`
  - `kb-items.jsonl`
  - `failed-items.jsonl`
  - `MEMORY.candidate.md`
- No direct write to `MEMORY.md`

## Current boundary
This skeleton does not include live Feishu API credentials or connector code. It focuses on the processing contract and local parsing layer so the agent can plug in listing/downloading later.

## Local test flow
1. Put sample `.docx` or `.pdf` files in a folder.
2. Run `python3 run.py --input-dir <folder> --output-dir outputs`.
3. Review the four output files.

## Next recommended upgrades
1. Add Feishu folder listing and download adapters.
2. Add `.pptx` parser in v0.2.
3. Add better policy/manual extraction heuristics.
