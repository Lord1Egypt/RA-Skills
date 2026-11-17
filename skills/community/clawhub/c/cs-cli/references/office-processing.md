# Office Document Processing Reference

> **Saving**: These are parameter examples. `-s` alone saves only to the cloud; `-o` specifies local output. Apply the save policy in `SKILL.md` to the actual task; final artifacts without a save preference require both destinations and a context-based `--save-title`.

## office convert - Office Document Format Conversion

Convert Word, Excel, or PPT documents to PDF, or upgrade legacy formats (DOC/XLS/PPT) to modern formats (DOCX/XLSX/PPTX). The CLI automatically detects the source file type from the file extension.

### Supported Conversions

| Input Format | `--format` Value | Output Extension | Description |
|-------------|------------------|------------------|-------------|
| DOC/DOCX | `pdf` (default) | .pdf | Word to PDF |
| DOC | `docx` | .docx | Legacy Word format upgrade |
| XLS/XLSX | `pdf` (default) | .pdf | Excel to PDF |
| XLS | `xlsx` | .xlsx | Legacy Excel format upgrade |
| PPT/PPTX | `pdf` (default) | .pdf | PPT to PDF |
| PPT | `pptx` | .pptx | Legacy PPT format upgrade |

> Files already in modern format (DOCX/XLSX/PPTX) cannot be converted to the same format (e.g., DOCX to DOCX). They can only be converted to PDF.

### Parameters

| Parameter/Flag | Description |
|----------------|-------------|
| `file` (positional) | Input file path (required) |
| `--format` | Target format: `pdf` (default), `docx`, `xlsx`, `pptx` |
| `-o, --output` | Output file path (auto-derived if omitted) |
| `-s, --save` | Save to cloud documents |
| `--save-title` | Cloud document title |
| `--save-dir` | Save to a specific folder (by name) |
| `--save-dir-id` | Save to a specific folder (by ID) |

### Usage Examples

```bash
# Word to PDF (default)
camscanner-cli office convert report.docx -o "report.pdf" -s --save-title "Report PDF"

# Excel to PDF
camscanner-cli office convert data.xlsx -o "data.pdf" -s --save-title "Data table PDF"

# PPT to PDF
camscanner-cli office convert slides.pptx -o "slides.pdf" -s --save-title "Presentation PDF"

# Legacy format upgrade: DOC to DOCX
camscanner-cli office convert old.doc --format docx -o "old_upgraded.docx" -s

# Legacy format upgrade: XLS to XLSX
camscanner-cli office convert legacy.xls --format xlsx -o "legacy_upgraded.xlsx" -s

# Legacy format upgrade: PPT to PPTX
camscanner-cli office convert presentation.ppt --format pptx -o "presentation_upgraded.pptx" -s
```

## Limits and Notes

- **File size**: upload limit is 40 MB.
- **Encrypted documents**: password-protected Office documents are not supported.
- **Format detection**: the CLI determines the file type from the extension; ensure the extension is correct.
- **Unsupported conversions**: DOCX to DOCX, XLSX to XLSX, PPTX to PPTX (same-format conversion is unnecessary).
