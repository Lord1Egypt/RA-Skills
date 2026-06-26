---
name: feishu-knowledge-ingest
description: batch ingest feishu folders and single attachments into report-first knowledge artifacts. use when chatgpt needs to read a feishu directory or a single shared file, classify files, extract text from supported attachments, and produce ingest-report.md, kb-items.jsonl, failed-items.jsonl, and memory.candidate.md without directly writing memory.md. best for feishu knowledge training, directory learning, policy/manual ingestion, and controlled docx/pdf parsing workflows.
---

# Feishu Knowledge Ingest

Use this skill to turn a Feishu folder or a single shared attachment into structured, reviewable knowledge outputs.

## What this skill does
- Accept a Feishu folder link/token or a single shared attachment.
- Classify files into direct-read, download-and-parse, manual-review, or permission-blocked.
- Parse `.docx` and `.pdf` in v0.1.
- Produce report-first outputs instead of writing `MEMORY.md` directly.
- Preserve failures and uncertainty instead of guessing content.

## Supported v0.1 scope
### Inputs
- Feishu folder link or `folder_token`
- Single shared attachment link or token

### Parsing
- `.docx`
- `.pdf`

### Outputs
- `ingest-report.md`
- `kb-items.jsonl`
- `failed-items.jsonl`
- `MEMORY.candidate.md`

## Required behavior
1. Distinguish Feishu native docs from uploaded attachments.
   - Native docs: `doc`, `sheet`, `wiki`, `bitable`
   - Uploaded attachments: `.docx`, `.pdf`, `.pptx`, other files
2. Do not claim attachment content was learned unless text was actually extracted.
3. Default to report-first. Do not write `MEMORY.md` in v0.1.
4. Record every failed file with a concrete reason.
5. Prefer plain-text summaries over complex Feishu cards when reporting progress.

## File routing rules
### Direct-read
Treat these as direct-read only when the runtime has a reliable native-reader path:
- `doc`
- `sheet`
- `wiki`
- `bitable`

### Download-and-parse
Treat these as download-and-parse:
- `.docx`
- `.pdf`

### Manual-review
Route here when the file is out of scope or low-confidence in v0.1:
- `.pptx`
- images
- scans with no extractable text
- archives
- unusual file types

### Permission-blocked
Route here when listing is possible but the file cannot be downloaded or read.

## Standard workflow
1. Resolve input type.
   - Folder link/token -> enumerate files.
   - Single file link/token -> build a one-file manifest.
2. Create a batch record.
   - Generate `batch_id`.
   - Record `started_at`.
3. Build a manifest.
   - File name
   - File token/link
   - file type
   - route decision
4. Attempt extraction.
   - `.docx` -> use `parsers/parse_docx.py`
   - `.pdf` -> use `parsers/parse_pdf.py`
5. Produce structured outputs.
   - success -> append to `kb-items.jsonl`
   - failure -> append to `failed-items.jsonl`
6. Summarize the batch.
   - Write `ingest-report.md`
   - Write `MEMORY.candidate.md`
7. Finish the batch.
   - Record `finished_at`
   - Never auto-write `MEMORY.md`

## Output contracts
### kb-items.jsonl
Write one JSON object per successfully extracted knowledge item with at least:
- `batch_id`
- `source_file`
- `source_token`
- `file_type`
- `topic`
- `content_type`
- `summary`
- `extracted_at`
- `confidence`

### failed-items.jsonl
Write one JSON object per failed or blocked file with at least:
- `batch_id`
- `source_file`
- `source_token`
- `file_type`
- `failure_reason`
- `error_detail`
- `suggested_action`
- `failed_at`

### MEMORY.candidate.md
Include:
- batch header (`batch_id`, `started_at`, `finished_at`, `source_directory` or `source_file`)
- grouped knowledge summaries
- source references
- confidence notes
- items needing review

### ingest-report.md
Include:
1. Batch summary
2. Input scope
3. File counts and routing counts
4. Successful extraction summary
5. Failures and risks
6. Recommended next actions

## Safety rules
- Never invent text that was not extracted.
- If parsing fails, say so plainly and log it.
- Treat filenames as hints only, never as proof of document contents.
- Keep sensitive data out of `MEMORY.candidate.md` unless the workflow explicitly allows it.

## Included files
- `run.py`: minimal batch runner for local testing
- `parsers/parse_docx.py`: docx text extraction helper
- `parsers/parse_pdf.py`: pdf text extraction helper
- `references/output_examples.md`: sample output shapes and field guidance
- `README.md`: setup and usage notes
