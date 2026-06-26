# Everything2Markdown

Convert almost anything to Markdown using Microsoft MarkItDown. Optimized for AGENT and LLM workflows.

## Features

- 📝 PDF, DOCX, PPTX, XLSX, HTML, EPUB support
- 🖼️ Image OCR
- 🎵 Audio transcription  
- 📺 YouTube subtitle extraction
- 🔧 AGENT-optimized output

## Installation

```bash
pip3 install 'markitdown[all]'
```

## Usage

```bash
# Single file
markitdown document.pdf -o output.md

# Python API
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("doc.pdf")
print(result.text_content)
```

## Documentation

See [SKILL.md](SKILL.md) for complete documentation.