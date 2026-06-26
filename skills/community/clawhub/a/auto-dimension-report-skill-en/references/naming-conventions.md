# Naming & Directory Conventions

This document defines the input directory requirements, output naming rules, and scan exclusion rules for the `AutoDimensionReport` Skill.

The single goal: ensure that original documents, processed results, and OCR text can always be traced back to each other.

---

## Input Directory Requirements

It is recommended to place original documents directly in the task folder root:

```text
{TaskFolder}/
├── report1.pdf
├── report2.xlsx
├── report3.docx
└── ...
```

After script execution, the following will be auto-generated:

```text
{TaskFolder}/
├── output/
├── image/
└── imagetomd/
```

Notes:

- Do not mix original documents into `output/`, `image/`, or `imagetomd/`
- These directories are treated as script output directories — do not manually backfill original files

---

## Output File Rules

During document sorting, results corresponding to each original file are generated in `output/`:

| Source File | Output File | Description |
|---|---|---|
| `*.pdf` | `source.pdf.docx` | PDF converted to reviewable DOCX |
| `*.xlsx` | `source.xlsx` | Copied as-is |
| `*.xlsm` | `source.xlsm` | Copied as-is |
| `*.docx` | `source.docx` | Copied as-is |

Naming principles:

- Preserve original file names where possible
- Use extensions to distinguish processing types
- Ensure output files can be directly traced back to source files

---

## Image Naming Rules

All extracted images are placed in:

```text
image/{source file name}/
```

Specific naming conventions:

| Source | Naming Format | Example |
|---|---|---|
| PDF embedded image | `source.pdf-p{page}-img{seq}.{ext}` | `ReportA.pdf-p4-img1.jpeg` |
| PDF full page render | `source.pdf-p{page}.png` | `ReportA.pdf-p1.png` |
| DOCX embedded image | `source.docx-{seq}.{ext}` | `ReportB.docx-1.png` |
| XLSX/XLSM embedded image | `source.xlsx-{seq}.{ext}` | `ReportC.xlsx-1.png` |

Corresponding OCR results are saved to:

```text
imagetomd/{source file name}/
```

Maintaining the same relative directory relationship.

---

## Index File Rules

The script generates `_ImageIndex.xlsx` in `output/`. Typical columns include:

- Source file
- Image relative path
- Image absolute path

Its purpose:

- Enable quick manual image location
- Allow agents to trace back to source documents via relative paths
- Establish a stable association between OCR text and image paths

---

## Directory Exclusion Rules

When recursively scanning source files, directories containing the following fragments are excluded by default:

- `副本` (copy)
- `复制` (copy)
- `Copy`
- `output`
- `image`

During OCR stage, additionally exclude:

- `imagetomd`

This prevents already-generated files from being re-processed as input.

---

## PDF Classification Rules

During document sorting, PDFs are classified into two types:

- Text-based PDF: contains extractable text that passes garbage text detection
- Scanned PDF: too little extractable text, or text is clearly garbled/fragmented

Significance:

- Text-based PDF: prioritize preserving text and table structure
- Scanned PDF: prioritize preserving page images for OCR and manual review

---

## Relationship to Business Review

This naming and directory convention directly supports the following tasks:

- Table data review: quickly locate source tables, output tables, and verification results
- Seal review: quickly navigate from image path to OCR text
- Signature review: quickly compare signature images with recognized text
- Supply chain document review: establish unified traceability across multiple files

---

## Not Recommended

- Do not manually rename result files in `output/`, `image/`, or `imagetomd/`
- Do not mix external images into `image/` — this breaks source tracking
- Do not place script output back into the task root disguised as original documents
