---
name: word-to-pdf
description: Convert Word documents (.docx) to PDF format while preserving embedded images, formatting, and document structure. Use when user needs to convert Word files to PDF, batch convert documents, or maintain visual fidelity when converting DOCX files with images, tables, and complex formatting.
---

# Word to PDF Converter

## Quick Start

This skill converts Word documents (.docx) to PDF format, preserving embedded images, formatting, tables, and document structure.

## When to Use This Skill

Use this skill when you need to:
- Convert Word documents to PDF with images intact
- Batch convert multiple .docx files to PDF
- Preserve document formatting during conversion
- Handle Word files with embedded images, charts, or complex layouts
- Generate PDFs from Word templates or reports

## Conversion Methods

### Method 1: LibreOffice (Recommended)
**Best for:** Complex documents, highest fidelity, cross-platform
**Requirements:** LibreOffice installed
**Pros:** Free, handles complex formatting well, excellent image support
**Cons:** Requires LibreOffice installation

### Method 2: Python (python-docx + reportlab)
**Best for:** Programmatic conversion, custom formatting
**Requirements:** Python with specific libraries
**Pros:** Highly customizable, no external dependencies
**Cons:** More complex setup, may miss some formatting

### Method 3: Pandoc
**Best for:** Text-heavy documents, simple conversion
**Requirements:** Pandoc installed
**Pros:** Fast, widely available
**Cons:** Limited image support, basic formatting

### Method 4: docx2pdf (Python)
**Best for:** Quick conversions, good image support
**Requirements:** Python with docx2pdf library
**Pros:** Easy setup, good for most documents
**Cons:** May struggle with very complex layouts

## Usage

### Basic Conversion
```
Convert document.docx to PDF
```

### Batch Conversion
```
Convert all .docx files in current directory to PDF
```

### Custom Output
```
Convert report.docx to PDF and name it monthly-report.pdf
```

## Installation & Setup

### LibreOffice Method
```bash
# Install LibreOffice
sudo apt-get install libreoffice

# Or on macOS
brew install --cask libreoffice

# Or on Windows
# Download from libreoffice.org
```

### Python Method
```bash
# Install required libraries
pip install python-docx reportlab pillow

# Or use docx2pdf
pip install docx2pdf
```

### Pandoc Method
```bash
# Install pandoc
sudo apt-get install pandoc

# Or on macOS
brew install pandoc
```

## Conversion Commands

### LibreOffice (Recommended)
```bash
# Single file conversion
libreoffice --headless --convert-to pdf document.docx

# Specify output directory
libreoffice --headless --convert-to pdf --outdir ./pdfs document.docx

# Batch convert
for file in *.docx; do
    libreoffice --headless --convert-to pdf "$file"
done
```

### Python Method
```python
from docx import Document
from docx2pdf import convert

# Convert with images preserved
convert("document.docx", "output.pdf")
```

### Pandoc Method
```bash
# Basic conversion (limited image support)
pandoc document.docx -o output.pdf

# With better formatting
pandoc document.docx -o output.pdf --pdf-engine=xelatex
```

## Features & Capabilities

### What Gets Preserved
- Embedded images and screenshots
- Tables and cell formatting
- Headers, footers, and page numbers
- Font styles (bold, italic, underline)
- Document structure and headings
- Bullet points and numbered lists
- Page layout and margins

### Known Limitations
- Very complex macros may not convert perfectly
- Some advanced Word features may have PDF equivalents
- Custom fonts may need to be installed
- Extremely large documents may need memory tuning

## Troubleshooting

### Images Not Appearing
1. Check that images are embedded, not linked
2. Verify LibreOffice can open the source .docx
3. Try LibreOffice method (best image support)
4. Check disk space for large files

### Formatting Issues
1. LibreOffice method provides best results
2. Verify document isn't corrupted
3. Try opening in Word first to fix issues
4. Use headless mode to avoid UI conflicts

### Memory Issues with Large Files
```bash
# Increase LibreOffice memory (Linux)
soffice --headless -accept="socketsocket,host=localhost,port=2002;urp;" -nologo -nodefault -nofirststartwizard -nolockcheck -norestore -nocrashreport -nocrashreport -headless -invisible -convert-to pdf -nocrashreport -outdir /output /input

# Or split large document into parts before conversion
```

### Font Issues
- Install required system fonts
- Use common fonts (Arial, Times, Helvetica) for better compatibility
- Check LibreOffice font folder

## Advanced Usage

### Custom PDF Settings (LibreOffice)
```bash
# Export with specific settings
libreoffice --headless --convert-to pdf:writer_pdf_Export --infilter="writer_pdf_Export" document.docx
```

### Python Script for Batch Processing
```python
import os
from docx2pdf import convert

def convert_folder(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if file.endswith('.docx'):
            input_path = os.path.join(input_dir, file)
            output_path = os.path.join(output_dir, file.replace('.docx', '.pdf'))
            convert(input_path, output_path)
            print(f"Converted: {file}")

convert_folder('./docs', './pdfs')
```

## Quality Checklist

Before final conversion:
- [ ] Source .docx opens without errors
- [ ] Images are embedded (not external links)
- [ ] Required fonts are installed
- [ ] Sufficient disk space available
- [ ] Test conversion with similar document first
- [ ] Verify output PDF matches expected formatting

## Output Quality Tips

1. **Test First:** Always convert a sample document first
2. **Use LibreOffice:** Best method for fidelity
3. **Check Images:** Verify images appear correctly in output
4. **Batch Test:** Test one file before batch conversion
5. **Keep Originals:** Never delete source .docx files until PDF verified

## Getting Help

For detailed conversion options and troubleshooting:
- [LibreOffice Command Reference](references/libreoffice-reference.md)
- [Python docx2pdf Documentation](references/python-docx2pdf.md)
- [Common Conversion Issues](references/troubleshooting.md)
