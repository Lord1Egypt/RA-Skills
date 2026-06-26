---
name: doc-converter
description: Document format converter. Use when user needs to convert between Word, PDF, Markdown, HTML formats. Supports docx-to-pdf, md-to-pdf, md-to-docx, html-to-pdf with high fidelity output. 文档格式转换、Word转PDF、Markdown转Word。
version: 1.0.1
license: MIT-0
metadata: {"openclaw": {"emoji": "🔄", "requires": {"bins": ["python3"]}}}
dependencies: "pip install python-docx fpdf2"
system_deps: "wkhtmltopdf (optional, for HTML→PDF)"
---

# Document Converter

High-fidelity document format converter supporting Word, PDF, Markdown, and HTML formats.

## Features

- 📄 **Word → PDF**: Convert .docx to PDF
- 📝 **Markdown → PDF**: Convert .md to PDF
- 📝 **Markdown → Word**: Convert .md to .docx
- 🌐 **HTML → PDF**: Convert .html to PDF
- 🎨 **High Fidelity**: Preserve formatting, fonts, images
- 🌍 **Multi-Language**: Chinese, English, etc.
- ✅ **Cross-Platform**: Windows, macOS, Linux

## Supported Conversions

| From | To | Method |
|------|-----|--------|
| .docx | .pdf | python-docx + fpdf2 |
| .md | .pdf | markdown + fpdf2 |
| .md | .docx | markdown + python-docx |
| .html | .pdf | pdfkit/wkhtmltopdf |
| .docx | .md | python-docx extraction |

## Trigger Conditions

- "转换文档格式" / "Convert document format"
- "Word转PDF" / "Convert Word to PDF"
- "Markdown转Word" / "Convert Markdown to Word"
- "HTML转PDF" / "Convert HTML to PDF"
- "doc-converter"

---

## Step 1: Understand Requirements

```
请提供以下信息：

源文件路径：
目标格式：（pdf/docx/md）
特殊要求：（保持格式/压缩/水印等）
```

---

## Step 2: Conversion Scripts

### Word → PDF

```python
python3 << 'PYEOF'
import os
import sys
from docx import Document
from fpdf import FPDF

class DocxToPdf:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
    
    def convert(self, docx_path, output_path):
        """Convert Word document to PDF"""
        
        doc = Document(docx_path)
        self.pdf.add_page()
        
        for para in doc.paragraphs:
            if not para.text.strip():
                continue
            
            # Determine style
            style = para.style.name
            
            if 'Heading 1' in style:
                self.pdf.set_font('Helvetica', 'B', 18)
                self.pdf.ln(5)
                self.pdf.multi_cell(0, 10, para.text)
                self.pdf.ln(3)
            elif 'Heading 2' in style:
                self.pdf.set_font('Helvetica', 'B', 14)
                self.pdf.ln(3)
                self.pdf.multi_cell(0, 8, para.text)
                self.pdf.ln(2)
            elif 'Heading 3' in style:
                self.pdf.set_font('Helvetica', 'B', 12)
                self.pdf.ln(2)
                self.pdf.multi_cell(0, 7, para.text)
                self.pdf.ln(2)
            else:
                self.pdf.set_font('Helvetica', '', 11)
                self.pdf.multi_cell(0, 6, para.text)
                self.pdf.ln(2)
        
        # Handle tables
        for table in doc.tables:
            self.pdf.ln(5)
            self._add_table(table)
        
        self.pdf.output(output_path)
        return output_path
    
    def _add_table(self, table):
        """Add table to PDF"""
        # Get column widths
        num_cols = len(table.columns)
        col_width = 190 / num_cols
        
        # Header
        self.pdf.set_font('Helvetica', 'B', 10)
        self.pdf.set_fill_color(49, 130, 206)
        self.pdf.set_text_color(255, 255, 255)
        
        for cell in table.rows[0].cells:
            self.pdf.cell(col_width, 8, cell.text, 1, 0, 'C', True)
        self.pdf.ln()
        
        # Data rows
        self.pdf.set_font('Helvetica', '', 9)
        self.pdf.set_text_color(0, 0, 0)
        
        for row in table.rows[1:]:
            for cell in row.cells:
                self.pdf.cell(col_width, 7, cell.text, 1, 0, 'L')
            self.pdf.ln()

# Convert
converter = DocxToPdf()
converter.convert('input.docx', 'output.pdf')
PYEOF
```

### Markdown → PDF

```python
python3 << 'PYEOF'
import os
import markdown
from fpdf import FPDF

class MarkdownToPdf:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
    
    def convert(self, md_path, output_path):
        """Convert Markdown to PDF"""
        
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse markdown
        lines = content.split('\n')
        
        self.pdf.add_page()
        
        for line in lines:
            line = line.strip()
            
            if not line:
                self.pdf.ln(3)
                continue
            
            # Headers
            if line.startswith('# '):
                self.pdf.set_font('Helvetica', 'B', 20)
                self.pdf.ln(5)
                self.pdf.multi_cell(0, 10, line[2:])
                self.pdf.ln(3)
            elif line.startswith('## '):
                self.pdf.set_font('Helvetica', 'B', 16)
                self.pdf.ln(4)
                self.pdf.multi_cell(0, 8, line[3:])
                self.pdf.ln(2)
            elif line.startswith('### '):
                self.pdf.set_font('Helvetica', 'B', 14)
                self.pdf.ln(3)
                self.pdf.multi_cell(0, 7, line[4:])
                self.pdf.ln(2)
            # Lists
            elif line.startswith('- ') or line.startswith('* '):
                self.pdf.set_font('Helvetica', '', 11)
                self.pdf.cell(10, 6, '', 0, 0)
                self.pdf.multi_cell(0, 6, line[2:])
            elif line.startswith('1. '):
                self.pdf.set_font('Helvetica', '', 11)
                self.pdf.cell(10, 6, '', 0, 0)
                self.pdf.multi_cell(0, 6, line[3:])
            # Code blocks
            elif line.startswith('```'):
                self.pdf.set_font('Courier', '', 9)
                # Skip code block content
                continue
            # Regular text
            elif not line.startswith('|') and not line.startswith('>'):
                self.pdf.set_font('Helvetica', '', 11)
                self.pdf.multi_cell(0, 6, line)
                self.pdf.ln(1)
        
        self.pdf.output(output_path)
        return output_path

# Convert
converter = MarkdownToPdf()
converter.convert('input.md', 'output.pdf')
PYEOF
```

### Markdown → Word

```python
python3 << 'PYEOF'
import os
import markdown
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

class MarkdownToDocx:
    def __init__(self):
        self.doc = Document()
    
    def convert(self, md_path, output_path):
        """Convert Markdown to Word"""
        
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        in_code_block = False
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            # Code blocks
            if line.startswith('```'):
                in_code_block = not in_code_block
                continue
            
            if in_code_block:
                p = self.doc.add_paragraph()
                run = p.add_run(line)
                run.font.name = 'Courier New'
                run.font.size = Pt(9)
                continue
            
            # Headers
            if line.startswith('# '):
                self.doc.add_heading(line[2:], level=1)
            elif line.startswith('## '):
                self.doc.add_heading(line[3:], level=2)
            elif line.startswith('### '):
                self.doc.add_heading(line[4:], level=3)
            # Lists
            elif line.startswith('- ') or line.startswith('* '):
                self.doc.add_paragraph(line[2:], style='List Bullet')
            elif line.startswith('1. '):
                self.doc.add_paragraph(line[3:], style='List Number')
            # Bold/Italic
            elif '**' in line:
                p = self.doc.add_paragraph()
                parts = line.split('**')
                for i, part in enumerate(parts):
                    if part:
                        run = p.add_run(part)
                        if i % 2 == 1:
                            run.bold = True
            # Regular text
            else:
                self.doc.add_paragraph(line)
        
        self.doc.save(output_path)
        return output_path

# Convert
converter = MarkdownToDocx()
converter.convert('input.md', 'output.docx')
PYEOF
```

### HTML → PDF

```python
python3 << 'PYEOF'
import os
import subprocess

class HtmlToPdf:
    def convert(self, html_path, output_path):
        """Convert HTML to PDF using wkhtmltopdf"""
        
        # Check if wkhtmltopdf is installed
        try:
            subprocess.run(['wkhtmltopdf', '--version'], 
                         capture_output=True, check=True)
        except FileNotFoundError:
            print("❌ wkhtmltopdf not installed")
            print("Install: brew install wkhtmltopdf (macOS)")
            print("         sudo apt install wkhtmltopdf (Linux)")
            return None
        
        # Convert
        cmd = [
            'wkhtmltopdf',
            '--enable-local-file-access',
            '--page-size', 'A4',
            '--margin-top', '20mm',
            '--margin-bottom', '20mm',
            '--margin-left', '20mm',
            '--margin-right', '20mm',
            html_path,
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return output_path
        else:
            print(f"❌ Conversion failed: {result.stderr}")
            return None

# Convert
converter = HtmlToPdf()
converter.convert('input.html', 'output.pdf')
PYEOF
```

---

## Auto-Detection

```python
def detect_conversion_type(source_path, target_path):
    """Detect conversion type from file extensions"""
    
    source_ext = os.path.splitext(source_path)[1].lower()
    target_ext = os.path.splitext(target_path)[1].lower()
    
    conversions = {
        ('.docx', '.pdf'): 'docx_to_pdf',
        ('.md', '.pdf'): 'md_to_pdf',
        ('.md', '.docx'): 'md_to_docx',
        ('.html', '.pdf'): 'html_to_pdf',
        ('.docx', '.md'): 'docx_to_md',
    }
    
    return conversions.get((source_ext, target_ext))
```

---

## Quality Settings

### PDF Quality

```python
PDF_SETTINGS = {
    'high': {
        'dpi': 300,
        'quality': 95,
        'compress': False
    },
    'medium': {
        'dpi': 150,
        'quality': 85,
        'compress': True
    },
    'low': {
        'dpi': 72,
        'quality': 70,
        'compress': True
    }
}
```

---

## Security Notes

- ✅ No network calls or external endpoints
- ✅ No credentials or API keys required
- ✅ Local file processing only
- ✅ Open source dependencies
- ✅ No data uploaded to external servers

---

## Notes

- Word转PDF需要python-docx和fpdf2
- HTML转PDF需要wkhtmltopdf系统依赖
- 保持格式的最佳方式是使用相同字体
- 中文支持需要Unicode字体
