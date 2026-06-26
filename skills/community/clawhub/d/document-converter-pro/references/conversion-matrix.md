# Conversion Matrix

## Supported Conversions

| Source | Target | Quality | Method |
|--------|--------|---------|--------|
| .docx | .pdf | ⭐⭐⭐⭐⭐ | python-docx + fpdf2 |
| .docx | .md | ⭐⭐⭐⭐ | python-docx extraction |
| .md | .pdf | ⭐⭐⭐⭐⭐ | markdown + fpdf2 |
| .md | .docx | ⭐⭐⭐⭐ | markdown + python-docx |
| .html | .pdf | ⭐⭐⭐⭐⭐ | wkhtmltopdf |
| .txt | .pdf | ⭐⭐⭐⭐ | fpdf2 |
| .txt | .docx | ⭐⭐⭐⭐ | python-docx |

## Dependencies

### Required
- python3
- pip

### Python Packages
- python-docx (Word processing)
- fpdf2 (PDF generation)
- markdown (Markdown parsing)

### System Tools
- wkhtmltopdf (HTML to PDF, optional)

## Font Handling

### Chinese Fonts
- Noto Sans SC (recommended)
- Noto Serif SC (recommended)
- SimSun (Windows)
- STSong (macOS)

### English Fonts
- Times New Roman
- Arial
- Liberation Serif

## Quality Considerations

### Formatting Preservation
- Headers and styles
- Tables and lists
- Images and figures
- Fonts and colors
- Page breaks

### Limitations
- Complex layouts may lose fidelity
- Embedded objects may not convert
- Custom fonts may fallback
- Macros are not preserved
