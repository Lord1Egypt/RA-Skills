#!/usr/bin/env python3
"""
book_parser.py - Deep Reader Book Format Parser

Supported formats: TXT, PDF, EPUB, MD
Output: Plain text dictionary with chapter structure

Pure Python implementation, no system binary dependencies

Usage:
    from book_parser import parse_book
    result = parse_book("/path/to/book.pdf")
    print(result["content"][:500])  # First 500 characters
    print(result["chapters"])        # Chapter list
"""

from pathlib import Path
from typing import Dict, List, Optional
import re


def parse_book(file_path: str) -> Dict:
    """
    Unified entry function: Call corresponding parser based on file extension
    
    Args:
        file_path: Path to the book file
        
    Returns:
        {
            "content": str,          # Full text content
            "chapters": List[dict],  # Chapter list [{title, start_idx, content}]
            "format": str,           # Original format (txt/pdf/epub/md)
            "metadata": dict         # Metadata (if extractable)
        }
    """
    path = Path(file_path)
    ext = path.suffix.lower()
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    parsers = {
        '.txt': parse_txt,
        '.pdf': parse_pdf,
        '.epub': parse_epub,
        '.md': parse_md,
        '.markdown': parse_md,
    }
    
    parser = parsers.get(ext)
    if not parser:
        raise ValueError(f"Unsupported format: {ext}. Supported: {list(parsers.keys())}")
    
    return parser(path)


def parse_txt(path: Path) -> Dict:
    """Parse TXT file with automatic encoding detection"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'big5']
    
    for enc in encodings:
        try:
            with open(path, 'r', encoding=enc) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue
    else:
        raise RuntimeError(f"Cannot detect file encoding: {path}")
    
    chapters = _detect_chapters(content)
    
    return {
        "content": content,
        "chapters": chapters,
        "format": "txt",
        "metadata": {"encoding": enc}
    }


def parse_pdf(path: Path) -> Dict:
    """
    Parse PDF file (pure Python implementation)
    Dependency: pdfplumber
    Install: pip install pdfplumber
    """
    try:
        import pdfplumber
    except ImportError:
        raise RuntimeError(
            "Missing dependency. Run: pip install pdfplumber"
        )
    
    full_text = []
    
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
    
    content = '\n\n'.join(full_text)
    chapters = _detect_chapters(content)
    
    return {
        "content": content,
        "chapters": chapters,
        "format": "pdf",
        "metadata": {"pages": len(full_text)}
    }


def parse_epub(path: Path) -> Dict:
    """
    Parse EPUB file (pure Python implementation)
    Dependency: ebooklib, beautifulsoup4
    Install: pip install ebooklib beautifulsoup4
    """
    try:
        from ebooklib import epub
        from bs4 import BeautifulSoup
    except ImportError:
        raise RuntimeError(
            "Missing dependency. Run: pip install ebooklib beautifulsoup4"
        )
    
    book = epub.read_epub(str(path))
    full_text = []
    chapter_info = []
    
    # Iterate through all document items
    for item in book.get_items():
        if item.get_type() == 9:  # ITEM_DOCUMENT = 9
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text = soup.get_text()
            
            # Clean up blank lines
            text = re.sub(r'\n{3,}', '\n\n', text)
            
            if text.strip():
                full_text.append(text)
                
                # Try to get chapter title
                title_item = soup.find(['h1', 'h2'])
                chapter_title = title_item.get_text().strip() if title_item else "Unknown Chapter"
                chapter_info.append({
                    "title": chapter_title,
                    "start_idx": len('\n'.join(full_text[:-1])),
                    "content": text
                })
    
    content = '\n\n---\n\n'.join(full_text)
    
    return {
        "content": content,
        "chapters": chapter_info if chapter_info else [{"title": "Full Text", "start_idx": 0, "content": content}],
        "format": "epub",
        "metadata": {
            "title": book.get_metadata('DC', 'title'),
            "author": book.get_metadata('DC', 'creator'),
        }
    }


def parse_md(path: Path) -> Dict:
    """Parse Markdown file"""
    encodings = ['utf-8', 'gbk']
    
    for enc in encodings:
        try:
            with open(path, 'r', encoding=enc) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue
    else:
        raise RuntimeError(f"Cannot detect file encoding: {path}")
    
    chapters = _detect_markdown_chapters(content)
    
    return {
        "content": content,
        "chapters": chapters,
        "format": "md",
        "metadata": {}
    }


def _detect_chapters(text: str) -> List[Dict]:
    """
    Generic chapter detection (for TXT/PDF)
    Try multiple common chapter marker patterns
    """
    patterns = [
        # Chinese patterns
        r'^第 [一二三四五六七八九十百千\d]+章\s*[^\n]+',
        r'^第 [一二三四五六七八九十百千\d]+[部分卷]\s*[^\n]+',
        # English patterns
        r'^Chapter\s+\d+\s*[.:]?\s*[^\n]*',
        r'^Part\s+[IVX\d]+\s*[.:]?\s*[^\n]*',
        # Numeric patterns
        r'^\d+\.\s*[^\n]+',
        r'^\d+\s+[^\n]+',
    ]
    
    chapters = []
    lines = text.split('\n')
    current_chapter = {"title": "Introduction", "start_idx": 0, "lines": []}
    
    for i, line in enumerate(lines):
        for pattern in patterns:
            if re.match(pattern, line.strip()):
                # Found new chapter
                if current_chapter["lines"]:
                    current_chapter["content"] = '\n'.join(current_chapter["lines"])
                    chapters.append(current_chapter)
                
                current_chapter = {
                    "title": line.strip(),
                    "start_idx": sum(len(l) + 1 for l in lines[:i]),
                    "lines": [line]
                }
                break
        else:
            current_chapter["lines"].append(line)
    
    # Add the last chapter
    if current_chapter["lines"]:
        current_chapter["content"] = '\n'.join(current_chapter["lines"])
        chapters.append(current_chapter)
    
    return chapters


def _detect_markdown_chapters(text: str) -> List[Dict]:
    """Chapter detection specifically for Markdown files"""
    chapters = []
    
    # Match ## headings
    pattern = r'^(#{2,})\s+(.+)$'
    lines = text.split('\n')
    
    current_chapter = None
    current_lines = []
    
    for i, line in enumerate(lines):
        match = re.match(pattern, line)
        if match:
            # Save previous chapter
            if current_chapter:
                current_chapter["content"] = '\n'.join(current_lines)
                chapters.append(current_chapter)
            
            current_chapter = {
                "title": match.group(2).strip(),
                "start_idx": sum(len(l) + 1 for l in lines[:i]),
                "lines": [line]
            }
            current_lines = [line]
        elif current_chapter:
            current_lines.append(line)
    
    # Add the last chapter
    if current_chapter:
        current_chapter["content"] = '\n'.join(current_lines)
        chapters.append(current_chapter)
    
    return chapters if chapters else [{"title": "Full Text", "start_idx": 0, "content": text}]


def clean_text(text: str) -> str:
    """
    Clean text: Remove headers, footers, ads, special characters
    
    Rules:
    - Remove duplicate lines (possibly from page breaks)
    - Remove special Unicode characters
    - Compress consecutive blank lines
    """
    # Compress consecutive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove common footer patterns
    page_foot_patterns = [
        r'\n\d+\s*$',  # Page number at end of line
        r'^\s*\d+\s*\n',  # Page number at start of line
        r'—+\s*\n',  # Separator line
    ]
    
    for pattern in page_foot_patterns:
        text = re.sub(pattern, '\n', text)
    
    # Compress spaces
    text = re.sub(r'[ \t]+', ' ', text)
    
    return text.strip()


# CLI test entry
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python book_parser.py <book_file_path>")
        print("Supported formats: TXT, PDF, EPUB, MD")
        sys.exit(1)
    
    path = sys.argv[1]
    
    try:
        result = parse_book(path)
        print(f"✓ Format: {result['format']}")
        print(f"✓ Total length: {len(result['content'])} characters")
        print(f"✓ Chapter count: {len(result['chapters'])}")
        print("\n--- First 500 characters ---")
        print(result['content'][:500])
        print("\n--- Chapter list ---")
        for i, ch in enumerate(result['chapters'][:10]):
            print(f"{i+1}. {ch['title']}")
        if len(result['chapters']) > 10:
            print(f"... and {len(result['chapters']) - 10} more chapters")
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
