---
name: smsf-document-creator
description: >
  Generates Word (.docx) reports and Excel (.xlsx) workbooks as real downloadable files.
  Use when the user wants a file output — not a text answer — for SMSF, accounting, compliance,
  or business document workflows. Triggers include: "create a Word doc", "make an Excel spreadsheet",
  "generate a report", "draft a trustee summary", "build a budget workbook", "I need a .docx / .xlsx file".
  Do NOT trigger for plain-text answers, inline tables, or when no file is requested.
user-invocable: true
---

# SMSF Document Creator

Generates Microsoft Word and Excel files from structured input. Designed for repeatable SMSF, accounting,
and compliance workflows where the user needs a real file — not just a formatted text response.

---

## When to use this skill

**Trigger this skill when the user asks for a file**, such as:

- "Draft a Word document for the trustee review"
- "Create an Excel budget workbook"
- "Generate a .docx / .xlsx file"
- "Make a checklist I can send to the client"
- "Produce a working paper in Excel"
- "I need a spreadsheet with this data"

**Do not trigger this skill when:**

- The user only wants a text response or inline table
- No file output is requested
- The document requires heavy formatting, macros, or branding this skill cannot produce (see Limitations)

---

## What this skill produces

### Word documents (`.docx`)

| Element | Supported |
|---|---|
| Document title | ✅ |
| Headings (levels 1–2) | ✅ |
| Paragraphs | ✅ |
| Bullet lists | ✅ |
| Numbered lists | ✅ |
| Basic tables | ✅ |
| Images / branding | ❌ |
| Advanced styles | ❌ |

**Typical uses:** trustee resolution drafts, client checklists, engagement summaries, compliance review notes, internal workpaper notes, business letters.

### Excel workbooks (`.xlsx`)

| Mode | How to invoke |
|---|---|
| Budget template | `--template budget` |
| Invoice template | `--template invoice` |
| Custom data (JSON) | `--data your-file.json` |

Features: styled header rows, auto-sized columns, simple SUM/difference formulas, bar chart (budget template only).

**Typical uses:** budget sheets, invoice layouts, cashflow working papers, financial review tables, data exports.

---

## Usage

Use `{baseDir}` to refer to the skill directory.

### Word — simple

```bash
python3 "{baseDir}/create_docx.py" \
  --title "SMSF Trustee Review Summary" \
  --content "This draft summarises matters identified during the annual compliance review." \
  --output "./trustee-review-summary.docx"
```

### Word — from JSON config

```bash
python3 "{baseDir}/create_docx.py" \
  --config "{baseDir}/templates/example_doc.json" \
  --output "./smsf-report.docx"
```

### Excel — budget template

```bash
python3 "{baseDir}/create_xlsx.py" \
  --template budget \
  --output "./budget.xlsx"
```

### Excel — invoice template

```bash
python3 "{baseDir}/create_xlsx.py" \
  --template invoice \
  --output "./invoice.xlsx"
```

### Excel — from JSON data

```bash
python3 "{baseDir}/create_xlsx.py" \
  --data "{baseDir}/templates/example_sheet.json" \
  --output "./quarterly-data.xlsx"
```

Use `--force` on any command to overwrite an existing output file.

---

## JSON input formats

### Word document

```json
{
  "title": "Document Title",
  "sections": [
    {
      "heading": "Section Heading",
      "level": 1,
      "paragraphs": ["Paragraph one.", "Paragraph two."],
      "bullets": ["Point A", "Point B"],
      "numbered": ["Step 1", "Step 2"],
      "table": [
        ["Header 1", "Header 2"],
        ["Value 1",  "Value 2"]
      ]
    }
  ]
}
```

- `title` and all section keys are optional
- `level` should be 1 or 2
- All rows in a `table` must have the same column count

### Excel workbook — single sheet

```json
{
  "title": "Quarterly Data",
  "headers": ["Month", "Revenue", "Expenses", "Profit"],
  "rows": [
    ["January",  120000, 80000, 40000],
    ["February", 140000, 85000, 55000]
  ]
}
```

### Excel workbook — multiple sheets

```json
{
  "sheets": [
    {
      "title": "Income",
      "headers": ["Month", "Amount"],
      "rows": [["January", 1000], ["February", 1200]]
    },
    {
      "title": "Expenses",
      "headers": ["Month", "Amount"],
      "rows": [["January", 700], ["February", 650]]
    }
  ]
}
```

---

## Safety rules

1. **Only write files to locations the user has explicitly approved.** Do not write to shared, client, or regulated folders without confirmation.
2. **Do not overwrite existing files** unless the user has clearly asked for that (use `--force` only when authorised).
3. **All output is a draft.** Never present generated documents as final, signed, or legally compliant without separate professional review.
4. **SMSF and compliance documents must be reviewed** by a qualified accountant, auditor, or adviser before use with a client or regulator.
5. **Do not interpolate free-form user input directly into shell commands.** Use structured JSON input instead.
6. **Do not execute arbitrary code** supplied by the user as part of document content or config.

---

## Limitations

This skill does **not**:

- Apply business branding, logos, or letterheads
- Produce advanced Word styles beyond the built-in Normal/Heading/List set
- Create complex Excel formulas, pivot tables, or VBA macros
- Validate legal or regulatory wording
- Replace professional review for any client-facing or lodgement document
- Produce macro-enabled `.xlsm` or `.dotm` files

---

## Requirements

```bash
pip install python-docx openpyxl
```

---

## Files

| File | Purpose |
|---|---|
| `create_docx.py` | Generates Word documents |
| `create_xlsx.py` | Generates Excel workbooks |
| `templates/example_doc.json` | Sample Word config |
| `templates/example_sheet.json` | Sample Excel data |

---

*Author: R.J. — MySMSF. Generated documents are drafts and working files only.*
