---
name: document-handler
description: Read, extract, and convert document files (PDF, DOCX, XLSX, PPTX, EPUB, RTF, ODT, ODS, ODP). Use when working with any document format: extracting text, metadata, converting formats, or processing content. Triggers on mentions of document files, file paths with document extensions, or requests to read/convert documents.
---

# Document Handler

Extract text, metadata, and content from any document format.

## Supported Formats

| Format | Extensions | Text Extract | Metadata | Convert |
|--------|------------|--------------|----------|---------|
| PDF | .pdf | ✅ pdftotext | ✅ pdfinfo | ✅ pdftoppm |
| Word | .docx | ✅ unzip + xml | ✅ | ✅ |
| Excel | .xlsx | ✅ unzip + xml | ✅ | ✅ |
| PowerPoint | .pptx | ✅ unzip + xml | ✅ | ✅ |
| EPUB | .epub | ✅ unzip + html | ✅ | ✅ |
| RTF | .rtf | ✅ textutil | ✅ | ✅ |
| OpenDocument | .odt, .ods, .odp | ✅ unzip + xml | ✅ | ✅ |

## Quick Commands

### PDF

```bash
# Extract text
pdftotext -layout input.pdf output.txt

# Get metadata
pdfinfo input.pdf

# Convert to images (for OCR or viewing)
pdftoppm -png input.pdf output_prefix

# Extract specific pages
pdftotext -f 5 -l 10 -layout input.pdf output.txt
```

### DOCX/XLSX/PPTX (Office Open XML)

```bash
# Extract text from DOCX
unzip -p input.docx word/document.xml | sed 's/<[^>]*>//g' | tr -s ' \n'

# Extract text from XLSX (all sheets)
unzip -p input.xlsx xl/sharedStrings.xml | sed 's/<[^>]*>//g' | tr -s '\n'

# Extract text from PPTX
unzip -p input.pptx ppt/slides/*.xml | sed 's/<[^>]*>//g' | tr -s ' \n'

# Get metadata
unzip -p input.docx docProps/core.xml
```

### RTF (macOS)

```bash
# Convert RTF to plain text
textutil -convert txt input.rtf -output output.txt

# Convert RTF to HTML
textutil -convert html input.rtf -output output.html
```

### EPUB

```bash
# Extract and read EPUB content
unzip -l input.epub                    # List contents
unzip -p input.epub "*.html" | lynx -stdin -dump  # Text via lynx
unzip -p input.epub "*.xhtml" | sed 's/<[^>]*>//g'  # Raw text
```

### OpenDocument (ODT/ODS/ODP)

```bash
# Extract text from ODT
unzip -p input.odt content.xml | sed 's/<[^>]*>//g' | tr -s ' \n'

# Extract from ODS
unzip -p input.ods content.xml | sed 's/<[^>]*>//g'

# Get metadata
unzip -p input.odt meta.xml
```

## Scripts

### extract_document.sh

Extracts text and metadata from any supported document format.

```bash
~/Dropbox/jarvis/skills/document-handler/scripts/extract_document.sh <file>
```

Output:
- Text content to stdout
- Metadata as JSON comments

### pdf_to_images.sh

Converts PDF pages to images for OCR or visual processing.

```bash
~/Dropbox/jarvis/skills/document-handler/scripts/pdf_to_images.sh <pdf> <output_dir> [dpi]
```

## Workflow

1. **Identify format** — Check file extension
2. **Extract text** — Use appropriate tool
3. **Get metadata** — Author, date, pages, etc.
4. **Process content** — Summarize, search, transform

## Notes

- PDFs with scanned images need OCR (pdftoppm + tesseract)
- Encrypted PDFs require password
- Complex formatting may be lost in text extraction
- For tables in PDFs, consider tabula or camelot