# SMSF Document Generator (Word & Excel)

Creator: R.J.

This OpenClaw skill generates Word and Excel documents from structured input. It is intended for practical business use, especially repeatable drafting and working-paper workflows where users want a real file output rather than a text-only answer.

## Primary use cases

- SMSF report drafts
- trustee summaries and checklists
- internal compliance notes
- budget workbooks
- invoice layouts
- spreadsheet outputs from simple JSON data

## Included files

- `SKILL.md`
- `create_docx.py`
- `create_xlsx.py`
- `requirements.txt`
- `templates/example_doc.json`
- `templates/example_sheet.json`

## Installation

```bash
pip install -r requirements.txt
```

## Example commands

### Word document

```bash
python3 create_docx.py --title "SMSF Annual Review" --content "Draft review summary." --output review.docx
```

### Word document from JSON

```bash
python3 create_docx.py --config templates/example_doc.json --output report.docx
```

### Excel workbook from template

```bash
python3 create_xlsx.py --template budget --output budget.xlsx
```

### Excel workbook from JSON

```bash
python3 create_xlsx.py --data templates/example_sheet.json --output quarterly-data.xlsx
```

## Notes

The generated documents are intended as drafts, templates, and working files. They should be reviewed before client or regulatory use.
