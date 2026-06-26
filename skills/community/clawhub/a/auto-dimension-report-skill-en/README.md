# Part Dimension Inspection Skill

A document processing Skill for supply chain document review, dimension inspection report verification, image OCR recognition, and seal/signature clue checking.

It organizes a mixed document package into a reviewable structure with 4 core outputs:

- `output/` — Processed document results
- `image/` — Extracted images from documents
- `imagetomd/` — OCR recognition results from images
- `ReviewReport.md` — Summary report for manual review

## Capability Overview

### 1. Document Sorting

- PDF to DOCX conversion
- Preserves text, tables, and image order
- Archive copies of DOCX / XLSX / XLSM

### 2. Image Extraction & Indexing

- Extract images from PDF, DOCX, XLSX/XLSM
- Auto-generate `output/_ImageIndex.xlsx`
- Supports tracing back to original documents via relative image paths

### 3. OCR & Seal/Signature Clue Check

- Invoke Herdsman OCR for image text recognition
- Output to `imagetomd/`
- Search for keywords: `seal`, `stamp`, `signature` in reports

### 4. Judgement Consistency Verification

- Check if measured values fall within tolerance range
- Check if judgement column uses standard terminology
- Flag "out-of-tolerance but written OK/Pass" as high-risk items

## Applicable Scenarios

- Supplier document review
- Supply chain quality file verification
- Dimension inspection report / full dimension report review
- Excel judgement consistency check
- OCR-assisted check of scanned pages, seal pages, signature pages
- Standardized document package sorting

## Quick Start

Copy the entire skill folder to the `skills/` directory of any Agent runtime that supports Skill directories.

Recommended directory structure:

```text
skills/
└── AutoDimensionReport/
    ├── SKILL.md
    ├── README.md
    ├── references/
    │   ├── setup-guide.md
    │   └── naming-conventions.md
    └── scripts/
        ├── config.json
        ├── task_convert_extract.py
        ├── image_to_markdown.py
        ├── extract_verify_data.py
        └── generate_report.py
```

## Dependencies

- Python 3.8+
- `uv` or `pip`
- A usable Herdsman OCR environment is recommended

Install Python dependencies:

```powershell
uv pip install PyMuPDF python-docx openpyxl Pillow pdf2image pdfplumber
```

## Recommended Execution Flow

### Step 1. Document Sorting & Image Extraction

```powershell
uv run python "<skill-dir>/scripts/task_convert_extract.py" --dir "E:\TaskFolder"
```

### Step 2. Image OCR

```powershell
python "<skill-dir>/scripts/image_to_markdown.py" --dir "E:\TaskFolder"
```

Force re-run:

```powershell
python "<skill-dir>/scripts/image_to_markdown.py" --dir "E:\TaskFolder" --force
```

Batch processing:

```powershell
python "<skill-dir>/scripts/image_to_markdown.py" --dir "E:\TaskFolder" --batch-size 20
```

Switch OCR model:

```powershell
python "<skill-dir>/scripts/image_to_markdown.py" --dir "E:\TaskFolder" --model "paddleocr-ppocrv5-server"
```

Notes:

- Default: HTTP direct call `POST /v1/ocr`
- Falls back to external `scripts/ocr.py` if HTTP call fails (if exists)
- Automatically skips existing `imagetomd/*.md` — ideal for resume
- Output includes per-image time, average time, and ETA

### Step 3. Data Extraction & Judgement Verification

```powershell
python "<skill-dir>/scripts/extract_verify_data.py" --dir "E:\TaskFolder"
```

If template column positions differ, specify manually:

```powershell
python "<skill-dir>/scripts/extract_verify_data.py" --dir "E:\TaskFolder" --seq-col 2 --item-col 3 --std-col 5 --method-col 7 --data-start 9 --data-cols 5 --judge-col 14 --data-start-row 24
```

Currently supported:

- Auto-detect headers
- `√`, `○` recognized as pass
- Tolerance formats: `43°±5°`, `Φ6-0.05`, `≥5.4MPa`, `13（+0.2/0）`
- Data column count: 1 / 3 / 5 auto-adaptive

### Step 4. Generate Review Report

```powershell
python "<skill-dir>/scripts/generate_report.py" --dir "E:\TaskFolder"
```

Output summary or JSON:

```powershell
python "<skill-dir>/scripts/generate_report.py" --dir "E:\TaskFolder" --format summary
python "<skill-dir>/scripts/generate_report.py" --dir "E:\TaskFolder" --format json
```

Additional checks included by default:

- Tight tolerance boundary
- Precision inconsistency
- All-positive / all-negative bias
- Numeric tolerance but only OK/√ filled
- Missing required fields: part number, responsible person, full supplier name, vehicle model

## Output Structure

```text
TaskFolder/
├── Original files
├── output/
│   ├── *.pdf.docx
│   ├── *.docx
│   ├── *.xlsx
│   └── _ImageIndex.xlsx
├── image/
│   └── Extracted images sorted by source file directory
├── imagetomd/
│   └── OCR Markdown generated per image
└── ReviewReport.md
```

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

Can be overridden via:

- Environment variable `HERDSMAN_BASE_URL`
- Environment variable `HERDSMAN_SKILL_DIR`
- Environment variable `HERDSMAN_OCR_TRANSPORT`
- CLI argument `--model`

Default OCR skill search directories:

- `skills/headsman-skill/`
- `skills/herdsman-skill/`
- `~/.openclaw/skills/headsman-skill/`
- `~/.openclaw/skills/herdsman-skill/`

If OCR skill is not in default directories, specify manually:

```powershell
$env:HERDSMAN_SKILL_DIR = "E:\skills\herdsman-skill"
```

## Review Rules

Standard pass terms:

- `OK`
- `Pass`
- `√`
- `○`

Standard fail terms:

- `NOK`
- `Fail`
- `NG`

The following are flagged as non-standard (not treated as standard pass):

- `PASS`
- `Pass (in Chinese)`
- `Correct`

High-risk rule:

- Measured value outside tolerance range but judgement column is `OK` or `Pass`

OCR keyword check provides clue indication only — does not equal authenticity conclusion.

## File Reference

| Path | Purpose |
|---|---|
| `SKILL.md` | Main skill definition — trigger conditions, workflow, boundaries, and rules |
| `README.md` | Distribution documentation and quick-start guide |
| `references/setup-guide.md` | Environment setup instructions |
| `references/naming-conventions.md` | Naming and directory conventions |
| `scripts/task_convert_extract.py` | Main entry point: document sorting, image extraction, index generation |
| `scripts/image_to_markdown.py` | Image OCR recognition |
| `scripts/extract_verify_data.py` | Judgement consistency verification |
| `scripts/generate_report.py` | Review report generation |

## Limitations

- Without OCR environment, cannot fully execute seal/signature related checks
- Does not handle CAD / 3D model level analysis
- Does not directly determine seal or signature authenticity — provides OCR text clues only
- Reports are for assisted review, not a replacement for final manual judgment
