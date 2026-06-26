#!/usr/bin/env python3
"""
Large Document Reader with Progress Tracking

This script reads large documents (PDF, text files) and supports:
- Chunked reading to avoid memory issues
- Progress tracking (chapter/page bookmarking)
- Resume from last position
- Knowledge extraction for long-term memory

Usage:
  python read_large_document.py <document_path> [options]

Options:
  --resume       Resume from last saved position
  --position N   Jump to specific page/chapter N
  --output FILE  Output extracted text to file
  --chunk_size N Chunk size for reading (default: 5000)
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Optional, Dict, Any

# Try to import pdfplumber, fall back to basic text reader
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

PROGRESS_FILE = ".document_learning_progress.json"


def load_progress(doc_path: str) -> Optional[Dict[str, Any]]:
    """Load progress from last session."""
    doc_dir = os.path.dirname(doc_path) or "."
    progress_file = os.path.join(doc_dir, PROGRESS_FILE)
    
    if not os.path.exists(progress_file):
        return None
    
    try:
        with open(progress_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verify this is for the same document
        if data.get('document_path') == doc_path:
            return data
    except Exception:
        pass
    
    return None


def save_progress(doc_path: str, position: int, title: str, total_pages: int = 0) -> None:
    """Save learning progress."""
    doc_dir = os.path.dirname(doc_path) or "."
    progress_file = os.path.join(doc_dir, PROGRESS_FILE)
    
    data = {
        'document_path': doc_path,
        'title': title,
        'last_position': position,
        'total_pages': total_pages,
        'last_updated': str(Path.now()) if hasattr(Path, 'now') else None
    }
    
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def read_text_document(path: str, position: int = 0, chunk_size: int = 5000) -> tuple[str, int]:
    """Read a text-based document with progress tracking."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # If resuming from position, start from that point
        if position > 0 and position < len(content):
            remaining_text = content[position:]
            return remaining_text, len(content)
        
        return content, len(content)
    
    except UnicodeDecodeError:
        # Try different encodings
        for encoding in ['utf-8', 'gbk', 'latin-1']:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    content = f.read()
                
                if position > 0 and position < len(content):
                    return content[position:], len(content)
                
                return content, len(content)
            
            except Exception:
                continue
    
    raise IOError(f"Cannot read document: {path}")


def read_pdf_document(path: str, position: int = 0, chunk_size: int = 5000) -> tuple[str, int]:
    """Read a PDF document with progress tracking."""
    if not HAS_PDFPLUMBER:
        raise ImportError("pdfplumber is required for PDF reading. Install with: pip install pdfplumber")
    
    full_text = []
    total_pages = 0
    
    try:
        with pdfplumber.open(path) as pdf:
            total_pages = len(pdf.pages)
            
            # Start from position if resuming
            start_page = max(0, position)
            
            for i in range(start_page, total_pages):
                page = pdf.pages[i]
                text = page.extract_text()
                
                if text:
                    full_text.append(f"\n--- Page {i + 1} ---\n{text}")
            
            return '\n'.join(full_text), total_pages
    
    except Exception as e:
        raise IOError(f"Error reading PDF: {e}")


def detect_file_type(path: str) -> str:
    """Detect document type based on extension."""
    ext = Path(path).suffix.lower()
    
    if ext == '.pdf':
        return 'pdf'
    elif ext in ['.txt', '.md', '.markdown', '.log', '.json', '.yaml', '.yml']:
        return 'text'
    else:
        # Try to detect by content
        try:
            with open(path, 'rb') as f:
                header = f.read(100)
                if b'%PDF' in header:
                    return 'pdf'
        except Exception:
            pass
        
        return 'text'  # Default to text reader


def extract_key_points(text: str, max_points: int = 20) -> list[str]:
    """Extract key points from document content."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Look for numbered/bulleted lists and section headers
    key_points = []
    patterns = [
        r'^\d+\.\s+(.+)',  # Numbered list
        r'^[-*•]\s+(.+)',   # Bullet points
        r'^#{1,6}\s+(.+)',  # Headers
    ]
    
    for line in lines:
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                point = match.group(1).strip()
                if len(point) < 200 and point not in key_points:
                    key_points.append(point)
                    if len(key_points) >= max_points:
                        return key_points
    
    # Fallback: take first few sentences from each major section
    sections = re.split(r'\n{3,}', text)[:5]
    for section in sections:
        sentences = [s.strip() for s in section.split('.') if len(s.strip()) > 20]
        key_points.extend(sentences[:2])
        if len(key_points) >= max_points:
            return key_points[:max_points]
    
    # If no structured content, take first paragraph
    paragraphs = text.split('\n\n')[:3]
    for para in paragraphs:
        sentences = [s.strip() for s in re.split(r'[.!?]+', para) if len(s.strip()) > 30]
        key_points.extend(sentences[:2])
    
    return key_points[:max_points]


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Read large documents with progress tracking')
    parser.add_argument('document_path', help='Path to the document file')
    parser.add_argument('--resume', action='store_true', help='Resume from last position')
    parser.add_argument('--position', type=int, default=0, help='Start at specific page/chapter (default: 0)')
    parser.add_argument('--output', '-o', help='Output file for extracted text')
    parser.add_argument('--chunk_size', type=int, default=5000, help='Chunk size for reading')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.document_path):
        print(f"Error: Document not found: {args.document_path}")
        sys.exit(1)
    
    # Load progress if resuming
    position = 0
    title = os.path.basename(args.document_path)
    total_pages = 0
    
    if args.resume:
        progress = load_progress(args.document_path)
        if progress:
            position = progress.get('last_position', 0)
            title = progress.get('title', title)
            print(f"Resuming from position {position} in '{title}'")
    
    # Detect file type and read
    doc_type = detect_file_type(args.document_path)
    print(f"Reading {doc_type} document: {title}")
    
    try:
        if doc_type == 'pdf':
            text, total_pages = read_pdf_document(args.document_path, position, args.chunk_size)
        else:
            text, char_count = read_text_document(args.document_path, position, args.chunk_size)
        
        # Save progress after reading
        if doc_type == 'pdf' and total_pages > 0:
            save_progress(args.document_path, position + len(text.split('\n')), title, total_pages)
        else:
            save_progress(args.document_path, char_count, title)
        
        # Extract key points
        key_points = extract_key_points(text)
        
        # Output results
        result = {
            'title': title,
            'type': doc_type,
            'position_from': position,
            'total_pages': total_pages if doc_type == 'pdf' else char_count,
            'content': text[:5000],  # Limit content for initial processing
            'key_points': key_points
        }
        
        print(f"\n📄 Document: {title}")
        print(f"🔍 Type: {doc_type}")
        if doc_type == 'pdf':
            print(f"📑 Pages: {total_pages} (position {position}/{total_pages})")
        else:
            print(f"📝 Characters: {char_count} (position {position}/{char_count})")
        
        print("\n🔑 Key Points:")
        for i, point in enumerate(key_points[:10], 1):
            print(f"  {i}. {point}")
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Output saved to: {args.output}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
