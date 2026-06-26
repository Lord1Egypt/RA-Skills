---
name: everything2markdown
description: Convert almost anything (PDF, DOCX, PPTX, XLSX, images, audio, YouTube, etc.) to Markdown using Microsoft MarkItDown. Optimized for AGENT and LLM workflows.
homepage: https://github.com/microsoft/markitdown
metadata:
  emoji: 📝
  author: OpenClaw
  version: "1.0.0"
  category: document-processing
  tags: [markdown, conversion, pdf, docx, ocr, llm, agent]
  requires:
    bins: [python3, pip3]
    python_packages: [markitdown]
    env: []
  install:
    - id: install-markitdown
      kind: exec
      command: pip3 install 'markitdown[all]'
      label: Install MarkItDown with all dependencies
---

# Everything2Markdown - Convert Anything to Markdown

A powerful document conversion tool based on Microsoft MarkItDown, specifically optimized for AGENT and LLM workflows.

## Core Features

- ✅ **Universal Support**: PDF, DOCX, PPTX, XLSX, EPUB, HTML, CSV, JSON, XML
- ✅ **Rich Media**: Image OCR, audio transcription, YouTube subtitle extraction
- ✅ **Structure Preservation**: Headings, tables, lists, links maintained
- ✅ **Metadata Extraction**: Author, creation date, page count, etc.
- ✅ **AGENT Optimized**: Clean Markdown output perfect for LLM processing

## Supported Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | .pdf | Full text extraction with structure |
| Word | .docx, .doc | Preserves headings and tables |
| PowerPoint | .pptx, .ppt | Slide-by-slide conversion |
| Excel | .xlsx, .xls | Sheet-to-table conversion |
| EPUB | .epub | E-book format |
| HTML | .html, .htm | Web page conversion |
| Images | .png, .jpg, .gif | OCR text extraction |
| Audio | .mp3, .wav, .m4a | Speech-to-text |
| Archives | .zip | Iterates contents |
| YouTube | URL | Subtitle and metadata |

## Quick Start

### Single File Conversion

```bash
markitdown document.pdf -o output.md
```

### Batch Conversion

```bash
# Convert all PDFs in directory
for f in *.pdf; do
  markitdown "$f" -o "${f%.pdf}.md"
done

# Or with find
find . -name "*.pdf" -o -name "*.docx" | while read f; do
  out="${f%.*}.md"
  markitdown "$f" -o "$out"
  echo "✓ Converted: $f → $out"
done
```

### Advanced Options

```bash
# Verbose output
markitdown document.pdf -o output.md --verbose

# Keep intermediate files
markitdown document.pdf -o output.md --keep-temp

# Specify encoding
markitdown document.pdf -o output.md --encoding utf-8
```

## Python API

### Basic Usage

```python
from markitdown import MarkItDown

# Initialize
md = MarkItDown()

# Convert file
result = md.convert("document.pdf")

# Access content
print(result.text_content)  # Markdown text
print(result.metadata)      # Document metadata
```

### Advanced API

```python
from markitdown import MarkItDown
from markitdown.converters import DocumentConverter

# Custom configuration
md = MarkItDown(
    enable_plugins=True,
    custom_converters=[MyCustomConverter()]
)

# Convert with options
result = md.convert(
    "document.pdf",
    keep_formatting=True,
    extract_images=True
)

# Access structured data
print(f"Title: {result.metadata.get('title')}")
print(f"Author: {result.metadata.get('author')}")
print(f"Pages: {result.metadata.get('pages')}")
print(f"Word count: {len(result.text_content.split())}")
```

## AGENT Workflow Best Practices

### 1. Document Preprocessing Pipeline

```python
import re
from markitdown import MarkItDown

def preprocess_for_llm(file_path):
    """
    Preprocess document for optimal LLM consumption.
    Cleans noise, normalizes formatting, extracts structure.
    """
    # Convert to markdown
    md = MarkItDown()
    result = md.convert(file_path)
    
    text = result.text_content
    
    # Clean excessive formatting
    text = re.sub(r'\*{4,}', '***', text)  # Limit asterisks
    text = re.sub(r'\-{4,}', '---', text)  # Normalize horizontal rules
    text = re.sub(r'\n{4,}', '\n\n\n', text)  # Limit blank lines
    
    # Normalize headings
    text = re.sub(r'^#{7,}', '######', text, flags=re.MULTILINE)
    
    return {
        'content': text,
        'metadata': result.metadata,
        'original_length': len(result.text_content),
        'processed_length': len(text)
    }
```

### 2. Structured Section Extraction

```python
import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Section:
    level: int
    title: str
    content: str
    start_line: int
    end_line: int

def extract_sections(md_text: str) -> List[Section]:
    """
    Extract hierarchical sections from Markdown.
    Preserves document structure for AGENT processing.
    """
    lines = md_text.split('\n')
    sections = []
    
    # Find all headers
    header_pattern = re.compile(r'^(#{1,6})\s+(.+)$')
    headers = []
    
    for i, line in enumerate(lines):
        match = header_pattern.match(line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            headers.append({'level': level, 'title': title, 'line': i})
    
    # Extract sections
    for i, header in enumerate(headers):
        start_line = header['line']
        end_line = headers[i + 1]['line'] if i + 1 < len(headers) else len(lines)
        
        content = '\n'.join(lines[start_line + 1:end_line]).strip()
        
        sections.append(Section(
            level=header['level'],
            title=header['title'],
            content=content,
            start_line=start_line,
            end_line=end_line
        ))
    
    return sections
```

### 3. RAG-Optimized Chunking

```python
from typing import List, Dict
import hashlib

def chunk_for_rag(
    md_text: str,
    max_chunk_size: int = 1500,
    overlap: int = 200,
    preserve_headers: bool = True
) -> List[Dict]:
    """
    Chunk Markdown for optimal RAG retrieval.
    Preserves semantic boundaries and provides rich metadata.
    """
    chunks = []
    current_chunk = []
    current_size = 0
    chunk_index = 0
    
    # Split by natural boundaries
    paragraphs = md_text.split('\n\n')
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        para_size = len(para)
        
        # Check if adding this paragraph exceeds limit
        if current_size + para_size > max_chunk_size and current_chunk:
            # Save current chunk
            chunk_text = '\n\n'.join(current_chunk)
            chunks.append(create_chunk_dict(
                chunk_text, chunk_index, md_text
            ))
            
            # Start new chunk with overlap
            if overlap > 0:
                overlap_text = '\n\n'.join(current_chunk[-2:]) if len(current_chunk) >= 2 else chunk_text[-overlap:]
                current_chunk = [overlap_text, para]
                current_size = len(overlap_text) + para_size
            else:
                current_chunk = [para]
                current_size = para_size
            
            chunk_index += 1
        else:
            current_chunk.append(para)
            current_size += para_size + 2  # +2 for newlines
    
    # Don't forget the last chunk
    if current_chunk:
        chunk_text = '\n\n'.join(current_chunk)
        chunks.append(create_chunk_dict(
            chunk_text, chunk_index, md_text
        ))
    
    return chunks

def create_chunk_dict(text: str, index: int, source: str) -> Dict:
    """Create a chunk dictionary with metadata."""
    return {
        'index': index,
        'text': text,
        'length': len(text),
        'hash': hashlib.md5(text.encode()).hexdigest()[:8],
        'source_length': len(source),
        'percent_start': 0 if index == 0 else round((sum(len(c) for c in source[:text]) / len(source)) * 100, 1)
    }
```

### 4. Document Analysis Pipeline

```python
from typing import Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class DocumentAnalysis:
    """Complete document analysis for AGENT consumption."""
    file_path: str
    file_type: str
    word_count: int
    char_count: int
    section_count: int
    heading_levels: Dict[int, int]  # level -> count
    has_tables: bool
    has_images: bool
    has_links: bool
    estimated_reading_time: int  # minutes
    summary: str
    keywords: list
    metadata: Dict[str, Any]

class DocumentAnalyzer:
    """Analyze documents for AGENT workflows."""
    
    def __init__(self):
        self.md = MarkItDown()
    
    def analyze(self, file_path: str) -> DocumentAnalysis:
        """Complete document analysis."""
        # Convert to markdown
        result = self.md.convert(file_path)
        text = result.text_content
        
        # Basic stats
        word_count = len(text.split())
        char_count = len(text)
        
        # Section analysis
        sections = extract_sections(text)
        section_count = len(sections)
        
        # Heading levels
        heading_levels = {}
        for s in sections:
            heading_levels[s.level] = heading_levels.get(s.level, 0) + 1
        
        # Features detection
        has_tables = '|' in text and '---' in text
        has_images = '![' in text
        has_links = 'http' in text or '[' in text
        
        # Reading time (average 200 wpm)
        reading_time = max(1, word_count // 200)
        
        # Extract keywords (simple approach)
        words = re.findall(r'\b[A-Za-z][a-z]{4,}\b', text)
        word_freq = {}
        for w in words:
            w = w.lower()
            if w not in ['would', 'could', 'should', 'there', 'their', 'about']:
                word_freq[w] = word_freq.get(w, 0) + 1
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Generate summary
        summary = self._generate_summary(text, sections)
        
        return DocumentAnalysis(
            file_path=file_path,
            file_type=file_path.split('.')[-1].lower(),
            word_count=word_count,
            char_count=char_count,
            section_count=section_count,
            heading_levels=heading_levels,
            has_tables=has_tables,
            has_images=has_images,
            has_links=has_links,
            estimated_reading_time=reading_time,
            summary=summary,
            keywords=[k[0] for k in keywords],
            metadata=result.metadata
        )
    
    def _generate_summary(self, text: str, sections: List[Section]) -> str:
        """Generate a brief document summary."""
        if not sections:
            return text[:500] + "..." if len(text) > 500 else text
        
        # Get main sections
        main_sections = [s for s in sections if s.level <= 2]
        if main_sections:
            section_list = ", ".join([s.title for s in main_sections[:5]])
            return f"Document covers: {section_list}"
        
        return text[:300] + "..." if len(text) > 300 else text
```

## Integration with OpenClaw

### Skill Definition

```yaml
# SKILL.md
name: doc2markdown
metadata:
  emoji: 📝
  requires:
    python_packages: [markitdown]
  install:
    - command: pip3 install 'markitdown[all]'
```

### Tool Usage

```python
# In OpenClaw agent
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("/path/to/document.pdf")

# Use in RAG pipeline
chunks = chunk_for_rag(result.text_content)
store_in_vector_db(chunks)
```

## Performance Tips

1. **Batch Processing**: Process multiple files in parallel
2. **Memory Management**: For large documents, use streaming
3. **Caching**: Cache converted documents to avoid reprocessing
4. **Selective Conversion**: Only convert needed sections

## Security Considerations

- Sanitize file paths before processing
- Validate file types to prevent injection
- Handle sensitive content appropriately
- Consider file size limits to prevent DoS

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ImportError | Ensure `pip install 'markitdown[all]'` |
| OCR fails | Install Tesseract: `apt install tesseract-ocr` |
| Audio fails | Install ffmpeg: `apt install ffmpeg` |
| Memory error | Process in smaller chunks |

## License

MIT License - See LICENSE file for details.
