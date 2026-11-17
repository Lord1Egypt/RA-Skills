# PDF Processing Reference

> **Saving**: These are parameter examples. `-s` alone saves only to the cloud; `-o`/`-d` specify local output. Apply the save policy in `SKILL.md` to the actual task; final artifacts without a save preference require both destinations and a context-based `--save-title`.

> **Capability boundary**: There is no command to merge existing PDFs. Process multiple PDFs individually only when separate results are requested. Rendering pages to images does not preserve the original PDF text layer or structure; do not combine it with image assembly to promise PDF merging.

## pdf convert - PDF Format Conversion

Convert a PDF document to another editable format.

| Target Format | `--format` Value | Output Extension | Description |
|---------------|------------------|------------------|-------------|
| Word | `word` | .docx | Preserves layout. Default. |
| Excel | `excel` | .xlsx | Good for table-heavy PDFs |
| Markdown | `md` | .md | Plain text with structure |
| TXT | `txt` | .txt | Plain text, does not support `-s` |

```bash
camscanner-cli pdf convert report.pdf --format word -s
camscanner-cli pdf convert invoice.pdf --format excel -s
camscanner-cli pdf convert paper.pdf --format md -s
camscanner-cli pdf convert doc.pdf --format txt -o plain.txt
```

## pdf to-images - Convert PDF Pages to Images

Render each PDF page as a JPEG image.

```bash
# Output individual pages to a directory.
camscanner-cli pdf to-images report.pdf -d ./pages
# Output: pages/page_1.jpg, pages/page_2.jpg, ...

# Cloud only, when explicitly requested: a multi-page image document.
camscanner-cli pdf to-images report.pdf -s --save-title "Report pages"

# No save preference: both a local directory and cloud; no -o flag.
camscanner-cli pdf to-images report.pdf -d ./report_pages -s --save-title "Report pages"
```

| Parameter | Description |
|-----------|-------------|
| `-d, --dir` | Output directory. Default: `<filename>_pages/`. |
| `-s` | Cloud only; combine with `-d dir` to save both. |

## pdf to-images-zip - Convert PDF Pages to an Image ZIP

Same function as `to-images`, but the server packages the images as a single ZIP file.

```bash
camscanner-cli pdf to-images-zip report.pdf -o report_images.zip
```

> Note: `to-images-zip` does not support `-s` because ZIP is not a supported cloud document type.

## pdf watermark - Add Watermark

| Parameter | Description |
|-----------|-------------|
| `--text` | Watermark text. **Required**. |
| `--color` | Color, such as `#FF0000`. |
| `--opacity` | Opacity from 0 to 1. |
| `--size` | Font size. |

```bash
camscanner-cli pdf watermark contract.pdf --text "INTERNAL USE ONLY" -s
camscanner-cli pdf watermark doc.pdf --text "DRAFT" --color "#999999" --opacity 0.2 -s
```

## pdf remove-watermark - Remove Watermark

Remove existing watermarks from a PDF.

```bash
camscanner-cli pdf remove-watermark document.pdf -s
camscanner-cli pdf remove-watermark doc.pdf -o clean.pdf
```

## Limits and Notes

- **File size**: upload limit is 40 MB.
- **Page count**: watermark operations support at most 100 pages.
- **PDF type**: text PDFs and scanned PDFs are supported.
- **Encrypted PDFs**: password-protected PDFs are not supported.
