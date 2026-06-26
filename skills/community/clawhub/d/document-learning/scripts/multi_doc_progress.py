#!/usr/bin/env python3
"""
Multi-Document Progress Manager

This script manages learning progress across multiple documents, allowing you to:
- Track progress for several PDFs simultaneously
- Switch between documents and resume from last position
- Query overall learning status
- Export/import progress data

Usage:
  python multi_doc_progress.py <command> [options]

Commands:
  init <doc_path>              Initialize tracking for a document
  read <doc_path> [--resume]   Read document (optionally resume)
  status                       Show all document statuses
  switch <doc_name>            Switch to specific document
  progress <doc_name>          Show detailed progress for one document
  export <file>                Export all progress to JSON file
  import <file>                Import progress from JSON file
  reset <doc_name>             Reset progress for a specific document
  
Options:
  --position N                 Start at page/chapter N
  --output FILE                Output results to file
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Optional, Any

# Try to import pdfplumber for PDF reading
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

# Global progress store file
PROGRESS_STORE_FILE = ".multi_doc_learning_progress.json"


def load_progress_store() -> Dict[str, Any]:
    """Load the global progress store."""
    current_dir = os.getcwd()
    store_file = os.path.join(current_dir, PROGRESS_STORE_FILE)
    
    if not os.path.exists(store_file):
        return {'documents': {}, 'created': str(date.today())}
    
    try:
        with open(store_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Ensure structure is valid
        if 'documents' not in data:
            return {'documents': {}, 'created': str(date.today())}
        
        return data
    
    except Exception:
        return {'documents': {}, 'created': str(date.today())}


def save_progress_store(data: Dict[str, Any]) -> None:
    """Save the global progress store."""
    current_dir = os.getcwd()
    store_file = os.path.join(current_dir, PROGRESS_STORE_FILE)
    
    data['last_updated'] = str(datetime.now())
    
    with open(store_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_doc_key(doc_path: str) -> str:
    """Generate a unique key for a document."""
    return os.path.basename(doc_path)


def init_document(doc_path: str, title: Optional[str] = None) -> Dict[str, Any]:
    """Initialize tracking for a new document."""
    if not os.path.exists(doc_path):
        raise FileNotFoundError(f"Document not found: {doc_path}")
    
    store = load_progress_store()
    doc_key = get_doc_key(doc_path)
    
    # Get title from filename if not provided
    display_title = title or Path(doc_path).stem
    
    # Detect document type
    ext = Path(doc_path).suffix.lower()
    doc_type = 'pdf' if ext == '.pdf' else 'text'
    
    # Initialize progress entry
    store['documents'][doc_key] = {
        'path': os.path.abspath(doc_path),
        'title': display_title,
        'type': doc_type,
        'status': 'not_started',  # not_started, in_progress, completed
        'last_position': 0,
        'total_pages': 0,
        'pages_read': [],  # List of (page_num, read_date) tuples
        'notes': '',
        'created': str(date.today()),
        'started': None,
        'last_updated': str(date.today())
    }
    
    save_progress_store(store)
    
    return store['documents'][doc_key]


def load_document_progress(doc_path: str) -> Dict[str, Any]:
    """Load progress for a specific document."""
    store = load_progress_store()
    doc_key = get_doc_key(doc_path)
    
    if doc_key not in store.get('documents', {}):
        return None
    
    return store['documents'][doc_key]


def save_document_progress(doc_path: str, position: int, 
                          total_pages: int = 0, 
                          pages_read: Optional[List[int]] = None) -> Dict[str, Any]:
    """Save progress for a document."""
    store = load_progress_store()
    doc_key = get_doc_key(doc_path)
    
    if doc_key not in store['documents']:
        raise ValueError(f"Document {doc_key} not found. Initialize first with 'init' command.")
    
    doc_data = store['documents'][doc_key]
    
    # Update progress
    doc_data['last_position'] = position
    doc_data['total_pages'] = total_pages
    
    if pages_read:
        doc_data['pages_read'].extend([(p, str(date.today())) for p in pages_read])
    
    # Update status based on completion
    if total_pages > 0 and position >= total_pages:
        doc_data['status'] = 'completed'
    elif position > 0:
        doc_data['status'] = 'in_progress'
    
    doc_data['last_updated'] = str(date.today())
    
    save_progress_store(store)
    
    return store['documents'][doc_key]


def read_pdf_document(path: str, start_page: int = 0, max_pages: int = 50) -> tuple[str, int]:
    """Read a PDF document starting from specific page."""
    if not HAS_PDFPLUMBER:
        raise ImportError("pdfplumber is required for PDF reading. Install with: pip install pdfplumber")
    
    full_text = []
    total_pages = 0
    
    try:
        with pdfplumber.open(path) as pdf:
            total_pages = len(pdf.pages)
            
            # Start from specified page, limit to max_pages
            start_page = min(start_page, total_pages - 1) if total_pages > 0 else 0
            end_page = min(start_page + max_pages, total_pages)
            
            for i in range(start_page, end_page):
                page = pdf.pages[i]
                text = page.extract_text()
                
                if text:
                    full_text.append(f"\n--- Page {i + 1} ---\n{text}")
        
        return '\n'.join(full_text), total_pages
    
    except Exception as e:
        raise IOError(f"Error reading PDF {path}: {e}")


def read_text_document(path: str, start_pos: int = 0) -> tuple[str, int]:
    """Read a text document starting from character position."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if start_pos > 0 and start_pos < len(content):
            remaining_text = content[start_pos:]
            return remaining_text, len(content)
        
        return content, len(content)
    
    except UnicodeDecodeError:
        # Try different encodings
        for encoding in ['utf-8', 'gbk', 'latin-1']:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    content = f.read()
                
                if start_pos > 0 and start_pos < len(content):
                    return content[start_pos:], len(content)
                
                return content, len(content)
            
            except Exception:
                continue
    
    raise IOError(f"Cannot read document {path}")


def extract_key_points(text: str, max_points: int = 20) -> list[str]:
    """Extract key points from text."""
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


def show_all_status(store: Dict[str, Any]) -> str:
    """Show status of all tracked documents."""
    docs = store.get('documents', {})
    
    if not docs:
        return "No documents being tracked. Use 'init <doc_path>' to start tracking."
    
    lines = ["📚 Document Learning Status", "=" * 50, ""]
    
    for doc_key in sorted(docs.keys()):
        doc = docs[doc_key]
        
        # Calculate progress percentage
        if doc['total_pages'] > 0:
            progress_pct = min(100, int((doc['last_position'] / doc['total_pages']) * 100))
            status_icon = "✅" if doc['status'] == 'completed' else "🔄" if doc['status'] == 'in_progress' else "⏳"
        else:
            progress_pct = "?"
            status_icon = "⏳"
        
        lines.append(f"{status_icon} {doc['title']}")
        lines.append(f"   📁 Path: {os.path.basename(doc['path'])}")
        if doc['total_pages'] > 0:
            lines.append(f"   📑 Progress: {doc['last_position']}/{doc['total_pages']} pages ({progress_pct}%)")
        else:
            lines.append(f"   📝 Status: {doc['status'].replace('_', ' ').title()}")
        
        if doc.get('started'):
            lines.append(f"   🕐 Started: {doc['started']}")
        
        lines.append(f"   🔄 Last updated: {doc['last_updated']}")
        lines.append("")
    
    return '\n'.join(lines)


def show_document_progress(doc_path: str) -> Optional[str]:
    """Show detailed progress for a specific document."""
    doc_data = load_document_progress(doc_path)
    
    if not doc_data:
        return f"❌ No progress found for {os.path.basename(doc_path)}"
    
    lines = [f"📊 Progress for: {doc_data['title']}", "-" * 50, ""]
    
    # Basic info
    lines.append(f"📁 Path: {doc_data['path']}")
    lines.append(f"🔍 Type: {doc_data['type'].upper()}")
    lines.append(f"📑 Status: {doc_data['status'].replace('_', ' ').title()}")
    
    # Progress details
    if doc_data['total_pages'] > 0:
        progress_pct = min(100, int((doc_data['last_position'] / doc_data['total_pages']) * 100))
        lines.append(f"📖 Position: {doc_data['last_position']}/{doc_data['total_pages']} pages ({progress_pct}%)")
        
        # Visual progress bar
        bar_width = 30
        filled = int(bar_width * progress_pct / 100)
        bar = "█" * filled + "░" * (bar_width - filled)
        lines.append(f"   [{bar}]")
    else:
        lines.append("📖 Position: Not tracked yet")
    
    # History
    if doc_data.get('pages_read'):
        lines.append("")
        lines.append("📅 Reading history:")
        for page, read_date in doc_data['pages_read'][-5:]:  # Last 5 entries
            lines.append(f"   • Page {page} - {read_date}")
    
    if doc_data.get('started'):
        lines.append(f"\n🕐 Started: {doc_data['started']}")
    
    lines.append(f"🔄 Last updated: {doc_data['last_updated']}")
    
    return '\n'.join(lines)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Multi-Document Learning Progress Manager')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # init command
    init_parser = subparsers.add_parser('init', help='Initialize tracking for a document')
    init_parser.add_argument('doc_path', help='Path to the document file')
    init_parser.add_argument('--title', '-t', help='Display title for the document (optional)')
    
    # read command
    read_parser = subparsers.add_parser('read', help='Read a document (optionally resume)')
    read_parser.add_argument('doc_path', help='Path to the document file')
    read_parser.add_argument('--resume', action='store_true', help='Resume from last position')
    read_parser.add_argument('--position', '-p', type=int, default=0, 
                            help='Start at specific page/chapter (default: 0)')
    read_parser.add_argument('--max_pages', type=int, default=50, 
                            help='Maximum pages to read in one session (default: 50)')
    
    # status command
    subparsers.add_parser('status', help='Show status of all tracked documents')
    
    # progress command
    progress_parser = subparsers.add_parser('progress', help='Show detailed progress for a document')
    progress_parser.add_argument('doc_path', help='Path to the document file')
    
    # switch command
    switch_parser = subparsers.add_parser('switch', help='Switch to specific document context')
    switch_parser.add_argument('doc_name', help='Document name or path')
    
    # export command
    export_parser = subparsers.add_parser('export', help='Export progress to JSON file')
    export_parser.add_argument('output_file', help='Output JSON file path')
    
    # import command
    import_parser = subparsers.add_parser('import', help='Import progress from JSON file')
    import_parser.add_argument('input_file', help='Input JSON file path')
    
    # reset command
    reset_parser = subparsers.add_parser('reset', help='Reset progress for a document')
    reset_parser.add_argument('doc_path', help='Path to the document file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Initialize command
        if args.command == 'init':
            doc_data = init_document(args.doc_path, args.title)
            print(f"✅ Initialized tracking for: {doc_data['title']}")
            print(f"   Path: {os.path.basename(doc_data['path'])}")
            print(f"   Type: {doc_data['type'].upper()}")
            print(f"\nYou can now start learning with 'read' command.")
        
        # Read command
        elif args.command == 'read':
            store = load_progress_store()
            doc_key = get_doc_key(args.doc_path)
            
            if doc_key not in store['documents']:
                print(f"⚠️  Document {doc_key} not found. Initializing...")
                init_document(args.doc_path)
                store = load_progress_store()
            
            doc_data = store['documents'][doc_key]
            
            # Load progress if resuming
            position = args.position
            title = doc_data.get('title', os.path.basename(args.doc_path))
            total_pages = 0
            
            if args.resume:
                position = doc_data.get('last_position', 0)
                print(f"🔄 Resuming from page {position} in '{title}'")
            
            # Detect type and read
            doc_type = doc_data['type']
            print(f"\n📖 Reading {doc_type.upper()} document: {title}")
            
            if doc_type == 'pdf':
                text, total_pages = read_pdf_document(args.doc_path, position, args.max_pages)
                
                # Save progress (new position = start + pages read)
                new_position = min(position + len(text.split('\n')), 
                                 total_pages if total_pages > 0 else position + args.max_pages)
                save_document_progress(args.doc_path, int(new_position), total_pages)
                
                print(f"\n✅ Read {len(text.split(chr(10)))} pages (pages {position+1}-{min(position+50, total_pages)})")
                print(f"📊 New position: {int(new_position)}/{total_pages}")
            
            else:  # text document
                text, char_count = read_text_document(args.doc_path, position)
                save_document_progress(args.doc_path, char_count, char_count)
                
                print(f"\n✅ Read {len(text)} characters")
                print(f"📊 New position: {char_count}/{char_count}")
            
            # Extract and display key points
            if text.strip():
                key_points = extract_key_points(text)
                print("\n🔑 Key Points:")
                for i, point in enumerate(key_points[:10], 1):
                    print(f"   {i}. {point}")
            
        # Status command
        elif args.command == 'status':
            store = load_progress_store()
            print(show_all_status(store))
        
        # Progress command
        elif args.command == 'progress':
            result = show_document_progress(args.doc_path)
            if result:
                print(result)
            else:
                print(f"❌ No progress found for {os.path.basename(args.doc_path)}")
        
        # Switch command
        elif args.command == 'switch':
            store = load_progress_store()
            doc_key = get_doc_key(args.doc_name)
            
            if doc_key not in store['documents']:
                print(f"❌ Document '{args.doc_name}' not found.")
                return
            
            doc_data = store['documents'][doc_key]
            print(f"🔄 Switched to context: {doc_data['title']}")
            print(f"   Path: {os.path.basename(doc_data['path'])}")
            if doc_data['last_position'] > 0:
                print(f"   Resume from page/chapter {doc_data['last_position']}")
        
        # Export command
        elif args.command == 'export':
            store = load_progress_store()
            with open(args.output_file, 'w', encoding='utf-8') as f:
                json.dump(store, f, indent=2, ensure_ascii=False)
            print(f"✅ Progress exported to {args.output_file}")
        
        # Import command
        elif args.command == 'import':
            if not os.path.exists(args.input_file):
                raise FileNotFoundError(f"Import file not found: {args.input_file}")
            
            with open(args.input_file, 'r', encoding='utf-8') as f:
                store = json.load(f)
            
            save_progress_store(store)
            print(f"✅ Progress imported from {args.input_file}")
        
        # Reset command
        elif args.command == 'reset':
            store = load_progress_store()
            doc_key = get_doc_key(args.doc_path)
            
            if doc_key not in store['documents']:
                print(f"❌ Document '{args.doc_path}' not found.")
                return
            
            # Reset progress
            store['documents'][doc_key].update({
                'last_position': 0,
                'status': 'not_started',
                'pages_read': [],
                'last_updated': str(date.today())
            })
            
            save_progress_store(store)
            print(f"✅ Progress reset for: {store['documents'][doc_key]['title']}")
    
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
