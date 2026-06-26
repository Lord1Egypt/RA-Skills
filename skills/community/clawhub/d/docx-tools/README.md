# docx-tools

Python-based Word document (.docx) processing tools for OpenClaw.

## Description

Read, write, and convert Word documents using Python's python-docx library.

## Installation

```bash
pip install python-docx
```

## Usage

### Read Word Document
```python
from docx import Document

doc = Document('input.docx')
for para in doc.paragraphs:
    print(para.text)
```

### Write Word Document
```python
from docx import Document

doc = Document()
doc.add_heading('Title', 0)
doc.add_paragraph('Content here')
doc.save('output.docx')
```

## Tools

- `read_docx`: Read content from .docx files
- `write_docx`: Create and write .docx files
- `docx_to_md`: Convert .docx to Markdown
- `md_to_docx`: Convert Markdown to .docx

## Author

SuperMike for 豹老大
