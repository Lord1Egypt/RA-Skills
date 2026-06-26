---
name: AutoDimensionReport
description: "Process PDF, DOCX, XLSX from supply chain document packages — conversion, image extraction, OCR, dimension verification, and review report generation. Invoked when users mention part dimension inspection, dimension report review, supplier document review, seal/signature check, or image extraction."
---

# Part Dimension Inspection

> A general-purpose Agent Skill for supply chain document review, dimension inspection report verification, and seal/signature checks.
> Core pipeline: **Document sorting -> Image extraction -> OCR recognition -> Verification -> Review report output**

---

## TL;DR

Quickly select execution path based on user goal:

| User wants | Minimum steps | Main outputs |
|---|---|---|
| Sort document package, extract images | Step 1 | `output/`, `image/`, `_ImageIndex.xlsx` |
| Check seals, signatures, scanned text | Step 1 -> Step 2 | `imagetomd/`, OCR keyword clues |
| Verify dimension correctness | Step 1 -> Step 3 | Judgement consistency check results |
| Generate full review conclusion | Step 1, optionally Step 2/3, then Step 4 | `ReviewReport.md` |

Quick judgment:

- Seeing `PDF / DOCX / XLSX` document package -> prioritize Step 1
- Seeing `seal / signature / scanned document / OCR` -> add Step 2
- Seeing `OK / NG / Pass / Fail / tolerance` -> add Step 3
- Seeing `summary report / final review conclusion` -> execute Step 4 last

---

## What Problem Does This Skill Solve

When a user provides a document package containing PDF, DOCX, XLSX files, this skill organizes the scattered files into a reviewable structure and provides directly usable intermediate results and reports for manual review.

Common suitable tasks:

- Supplier document review, quality document review, supply chain file verification
- Dimension inspection reports, full dimension reports, measurement reports, APQP inspection checklist review
- Consistency check between actual measured values and judgement in Excel/Word/PDF
- Image extraction, scanned document OCR, seal/stamp/signature keyword check
- Convert raw material into a three-layer structure (`output/`, `image/`, `imagetomd/`) for traceability

---

## When to Invoke

Use this skill when the user shows the following intent:

- Explicitly mentions "part dimension inspection", "dimension inspection report", "full dimension report", "measurement report"
- Wants to review a supplier-submitted PDF/Word/Excel document package
- Wants to batch extract images, seal pages, or scanned pages from documents
- Wants to run OCR on images or scanned documents
- Wants to check if "OK / NG / Pass / Fail" judgements are consistent with actual measurements
- Wants to generate a summary review report

Typical trigger phrases:

- `dimension inspection report`
- `part dimension inspection`
- `supply chain review`
- `supplier document review`
- `quality document review`
- `table data review`
- `judgement consistency check`
- `seal review`
- `stamp review`
- `signature review`
- `PDF to DOCX`
- `extract images`

---

## Quick Decision

If unsure how to start, follow this order:

1. Does the user provide a task folder or document package directory?
2. Does the package contain `.pdf`, `.docx`, `.xlsx`, `.xlsm` files?
3. Is the user's goal more toward "document sorting", "OCR recognition", "judgement verification", or "report generation"?
4. Does the current environment have Python dependencies and usable OCR capability?

Decision rules:

- Has document package directory but user's goal is unclear -> first ask if OCR, judgement verification, and final report are needed
- Single document only -> can still process, but warn user that completeness may be limited
- No directory path -> ask user for a valid path first; do not fabricate execution results
- No OCR environment -> can still execute Step 1; when seal/scanned document review is involved, clearly note capability limitations

---

## Cases Not Suitable for Direct Processing

Do not promise completion in these cases; explain boundaries first:

- User wants CAD / 3D model geometry analysis — this skill does not handle CAD native structures
- User only provides screenshot fragments but expects full cross-file traceability — need the original document package first
- Current environment has no Python dependencies or OCR capability — can only do document sorting, not full OCR review
- User wants to fully replace manual seal authenticity verification — this skill can only assist with text clues and position, not legal authenticity determination

---

## Input & Output

### Input

- A task folder
- Folder may contain `.pdf`, `.docx`, `.xlsx`, `.xlsm`
- For OCR, the environment needs an accessible Herdsman OCR capability

### Output

After task completion, the following structure is typically created:

```text
Task Folder/
├── Original files
├── output/
│   ├── *.pdf.docx
│   ├── *.docx
│   ├── *.xlsx
│   └── _ImageIndex.xlsx
├── image/
│   └── Extracted images saved in subdirectories by source file
├── imagetomd/
│   └── OCR Markdown generated per image
└── ReviewReport.md
```

---

## Core Capabilities

### 1. Document Conversion & Sorting

- Convert PDF to reviewable DOCX
- Preserve text, tables, images and their relative order
- Copy DOCX / XLSX / XLSM directly to `output/` for traceability

### 2. Dual Image Indexing

When converting PDF to DOCX, image positions retain two types of information:

| Method | Purpose |
|---|---|
| Embedded image | For manual review directly in DOCX |
| Path reference `[Image Reference] image/...` | For agent or manual backtracking to original image |

### 3. Image Extraction

Extract embedded images from PDF, DOCX, XLSX/XLSM and save to `image/{source file name}/`.

| File Type | Image Naming Convention |
|---|---|
| PDF | `source.pdf-p{page}-img{seq}.{ext}` |
| DOCX | `source.docx-{seq}.{ext}` |
| XLSX/XLSM | `source.xlsx-{seq}.{ext}` |

### 4. OCR Text Recognition

- Iterate through images in `image/`
- Default: use Herdsman HTTP API for recognition; fall back to OCR script on failure
- Write results to corresponding Markdown files under `imagetomd/`
- Supports specifying OCR skill directory via `HERDSMAN_SKILL_DIR` or `scripts/config.json`
- Supports batch processing, resume capability, per-image timing & ETA output

### 5. Judgement Consistency Verification

For common dimension inspection tables, the script checks:

- Whether measured values fall within tolerance range
- Whether the judgement column uses standard terminology
- High-risk cases where values are out-of-tolerance but marked as `OK` / `Pass`

### 6. Review Report Generation

Aggregate data from `output/`, `image/`, `imagetomd/` to generate a report for manual review, with additional OCR text scanning for:

- `seal` / `stamp`
- `signature`

---

## Standard Workflow

Execute in the following order by default. Do not skip steps unless the user explicitly requests only partial results.

### Step 0: Confirm Task Scope

First confirm the following:

1. Task folder path
2. Does the user want "document sorting only" or "full review"
3. Is OCR needed?
4. Is judgement consistency check needed?
5. Is a final review report needed?

If the user has not been clear, ask at least once — do not make assumptions.

### Step 1: Execute Document Sorting & Image Extraction

Main entry script:

```powershell
uv run python "<skill-dir>/scripts/task_convert_extract.py" --dir "<task-folder>"
```

This step will:

- Process PDF -> DOCX
- Extract images to `image/`
- Copy preservable DOCX / XLSX / XLSM to `output/`
- Generate `output/_ImageIndex.xlsx`

### Step 2: If OCR is needed, process image recognition

```powershell
python "<skill-dir>/scripts/image_to_markdown.py" --dir "<task-folder>"
```

Optional parameters:

```powershell
python "<skill-dir>/scripts/image_to_markdown.py" --dir "<task-folder>" --force
python "<skill-dir>/scripts/image_to_markdown.py" --dir "<task-folder>" --model "paddleocr-ppocrv5-server"
python "<skill-dir>/scripts/image_to_markdown.py" --dir "<task-folder>" --batch-size 20
```

This step is mandatory only in these scenarios:

- Scanned document review
- Seal / stamp / signature check
- Need to extract text clues from images

### Step 3: If table judgement verification is needed, extract and validate data

```powershell
python "<skill-dir>/scripts/extract_verify_data.py" --dir "<task-folder>"
```

When template column positions vary, supplement with these parameters:

```powershell
python "<skill-dir>/scripts/extract_verify_data.py" --dir "<task-folder>" --seq-col 2 --item-col 3 --std-col 5 --method-col 7 --data-start 9 --data-cols 5 --judge-col 14 --data-start-row 24
```

Enhancements:

- Auto-detect column positions from headers
- Auto-identify number of data columns
- Support `√`, `○` as pass judgement
- Support tolerance formats like `43°±5°`, `Φ6-0.05`, `≥5.4MPa`, `13（+0.2/0）`

Applicable to:

- XLSX inspection tables
- DOCX measurement reports with dimension tables
- Tasks requiring tolerance vs judgement consistency checks

### Step 4: Generate Review Report

```powershell
python "<skill-dir>/scripts/generate_report.py" --dir "<task-folder>"
```

Optional output formats:

```powershell
python "<skill-dir>/scripts/generate_report.py" --dir "<task-folder>" --format md
python "<skill-dir>/scripts/generate_report.py" --dir "<task-folder>" --format json
python "<skill-dir>/scripts/generate_report.py" --dir "<task-folder>" --format summary
```

Key output includes:

- File inventory overview
- Table and document content summary
- Image index availability
- OCR hit keyword locations
- Deep checks: tight-limit, precision inconsistency, bias analysis, OK-only filling
- Missing field warnings: part number, responsible person, full supplier name, vehicle model
- Anomaly items requiring manual re-check

### Step 5: Summarize Results to User

The final response should at least cover:

1. Which source files were processed
2. Which output directories and files were generated
3. Whether OCR was executed
4. Whether high-risk judgement inconsistencies were found
5. Whether seal/signature keywords were hit
6. Suggestions for what to manually review next

---

## Typical User Requests

The following phrases should typically trigger this skill:

```text
"Review this supplier document package for dimension judgement issues."
"Convert all PDFs in this task folder to reviewable versions and extract images."
"Check this batch of reports for stamp or signature clues."
"Check if the OK/NG judgements in the Excel match the measured values."
"Once done, produce a review report."
```

Recommended response strategy:

- First confirm the task directory
- Clarify whether OCR is needed
- Clarify whether judgement consistency check is needed
- Explain which directories and files will be output

---

## Review Rules

### Rule 1: Judgement Terminology Must Be Strictly Consistent

Standard pass terms:

- `OK`
- `合格` (Pass)
- `√`
- `○`

Standard fail terms:

- `NOK`
- `不合格` (Fail)
- `NG`

The following are considered non-standard pass terms and require user notification:

- `PASS`
- `正确` (Correct)
- `通过` (Pass)

### Rule 2: Out-of-Tolerance but Judged Pass — High Risk

If measured values are outside tolerance range but the judgement column still reads:

- `OK`
- `合格` (Pass)

It must be marked as a high-risk item with explicit warning in the summary.

### Rule 3: Seal/Signature — Clue Only

When OCR hits the following keywords, only indicate "relevant text clues found" — do not draw conclusions:

- `印章` (seal)
- `公章` (official stamp)
- `签名` (signature)

### Rule 4: Keep Original Files Traceable

Do not overwrite original files. All output should be placed in:

- `output/`
- `image/`
- `imagetomd/`

---

## OCR Configuration

Configuration file: `scripts/config.json`

```json
{
  "base_url": "http://127.0.0.1:8080",
  "ocr_model": "paddleocr-ppocrv5-server",
  "ocr_transport": "auto",
  "request_timeout": 120,
  "retry_count": 2,
  "retry_delay": 5,
  "ocr_script_dir": ""
}
```

Priority (high to low):

1. CLI argument `--model`
2. Environment variables
3. `config.json`
4. Script defaults

Relevant environment variables:

- `HERDSMAN_BASE_URL`: Override OCR service address
- `HERDSMAN_SKILL_DIR`: Explicitly specify OCR skill root directory
- `HERDSMAN_OCR_TRANSPORT`: Override OCR transport method (`auto` / `http` / `script`)

---

## Failure & Fallback Handling

### `image/` not found

- Means the user has not executed Step 1 yet
- Run `task_convert_extract.py` first

### OCR script not found

- Notify user that the current environment lacks Herdsman OCR capability
- List searched directories
- Have user set `HERDSMAN_SKILL_DIR` or update `scripts/config.json`

### Task directory does not exist

- Stop immediately
- Ask user to provide a valid path

### Partial functionality only

Execute on demand, no forced full workflow:

- Extract images only -> Step 1
- OCR only -> Step 1, then Step 2
- Judgement verification only -> at least Step 1, then Step 3
- Review report only -> usually recommend completing Step 1 first, optionally Step 2/3

---

## Resource Quick Reference

| Path | Purpose |
|---|---|
| `scripts/task_convert_extract.py` | Document sorting, PDF to DOCX, image extraction, index generation entry point |
| `scripts/image_to_markdown.py` | Image OCR recognition and Markdown output |
| `scripts/extract_verify_data.py` | Dimension data extraction and judgement consistency verification |
| `scripts/generate_report.py` | Aggregate and generate review report |
| `scripts/config.json` | OCR model and service configuration |
| `references/setup-guide.md` | Environment installation and setup instructions |
| `references/naming-conventions.md` | Directory structure and naming conventions |

---

## Constraints

1. Do not modify original file content
2. Do not treat OCR hit results as factual conclusions
3. Do not treat non-standard judgement terms as standard pass
4. Without OCR environment, do not fabricate OCR results
5. When responding, prioritize giving the user "directory location + risk items + next steps"
