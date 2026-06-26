#!/usr/bin/env python3
"""
PDF Tool - Work with PDF files
Note: Requires pypdf (pip install pypdf). Falls back to basic operations.
"""

import argparse
import os
import sys
from pathlib import Path


def get_pdf_info(filepath):
    """Get PDF metadata and info."""
    try:
        from pypdf import PdfReader
    except ImportError:
        print("Info: pypdf not installed. Running: pip install pypdf")
        return None
    
    try:
        reader = PdfReader(filepath)
        info = {
            'pages': len(reader.pages),
            'metadata': {},
            'encrypted': reader.is_encrypted
        }
        
        if reader.metadata:
            for key, value in reader.metadata.items():
                info['metadata'][key] = str(value)
        
        return info
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None


def extract_text(filepath, output=None):
    """Extract text from PDF."""
    try:
        from pypdf import PdfReader
    except ImportError:
        print("Error: pypdf not installed. Run: pip install pypdf")
        return 1
    
    try:
        reader = PdfReader(filepath)
        text_parts = []
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                text_parts.append(f"--- Page {i+1} ---\n{text}")
        
        full_text = '\n\n'.join(text_parts)
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(full_text)
            print(f"Text extracted to: {output}")
        else:
            print(full_text)
        
        return 0
    except Exception as e:
        print(f"Error extracting text: {e}")
        return 1


def extract_page(filepath, page_num, output):
    """Extract a specific page."""
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("Error: pypdf not installed. Run: pip install pypdf")
        return 1
    
    try:
        reader = PdfReader(filepath)
        writer = PdfWriter()
        
        # Page numbers are 0-indexed
        page_idx = page_num - 1
        if page_idx < 0 or page_idx >= len(reader.pages):
            print(f"Error: Page {page_num} not found (PDF has {len(reader.pages)} pages)")
            return 1
        
        writer.add_page(reader.pages[page_idx])
        
        with open(output, 'wb') as f:
            writer.write(f)
        
        print(f"Page {page_num} extracted to: {output}")
        return 0
    except Exception as e:
        print(f"Error extracting page: {e}")
        return 1


def merge_pdfs(files, output):
    """Merge multiple PDFs."""
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("Error: pypdf not installed. Run: pip install pypdf")
        return 1
    
    try:
        writer = PdfWriter()
        
        for filepath in files:
            reader = PdfReader(filepath)
            for page in reader.pages:
                writer.add_page(page)
        
        with open(output, 'wb') as f:
            writer.write(f)
        
        print(f"Merged {len(files)} PDFs to: {output}")
        return 0
    except Exception as e:
        print(f"Error merging PDFs: {e}")
        return 1


def split_pdf(filepath, pages_per_file, output_dir):
    """Split PDF into multiple files."""
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("Error: pypdf not installed. Run: pip install pypdf")
        return 1
    
    try:
        reader = PdfReader(filepath)
        total_pages = len(reader.pages)
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        file_num = 1
        for i in range(0, total_pages, pages_per_file):
            writer = PdfWriter()
            
            end = min(i + pages_per_file, total_pages)
            for page_idx in range(i, end):
                writer.add_page(reader.pages[page_idx])
            
            output_file = output_path / f"page_{file_num}.pdf"
            with open(output_file, 'wb') as f:
                writer.write(f)
            
            print(f"Created: {output_file}")
            file_num += 1
        
        print(f"Split into {file_num - 1} files")
        return 0
    except Exception as e:
        print(f"Error splitting PDF: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description='PDF Tool')
    parser.add_argument('input', nargs='?', help='Input PDF file')
    parser.add_argument('--extract-text', action='store_true', help='Extract text')
    parser.add_argument('--extract-images', action='store_true', help='Extract images')
    parser.add_argument('--merge', nargs='+', help='Merge PDFs')
    parser.add_argument('--split', type=int, help='Split into N pages per file')
    parser.add_argument('--page', type=int, help='Extract specific page')
    parser.add_argument('--info', action='store_true', help='Show PDF info')
    parser.add_argument('--output', help='Output file/directory')
    
    args = parser.parse_args()
    
    # Merge mode
    if args.merge:
        if not args.output:
            print("Error: --output required for merge")
            return 1
        return merge_pdfs(args.merge, args.output)
    
    # Need input file for other operations
    if not args.input:
        parser.print_help()
        return 1
    
    # Extract text
    if args.extract_text:
        output = args.output or args.input.replace('.pdf', '.txt')
        return extract_text(args.input, output)
    
    # Extract page
    if args.page:
        if not args.output:
            print("Error: --output required for page extraction")
            return 1
        return extract_page(args.input, args.page, args.output)
    
    # Split
    if args.split:
        output_dir = args.output or 'split'
        return split_pdf(args.input, args.split, output_dir)
    
    # Info
    if args.info:
        info = get_pdf_info(args.input)
        if info:
            print("\n=== PDF Info ===")
            print(f"Pages: {info['pages']}")
            print(f"Encrypted: {info['encrypted']}")
            if info['metadata']:
                print("\nMetadata:")
                for key, val in info['metadata'].items():
                    print(f"  {key}: {val}")
        return 0
    
    # Default: show help
    parser.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
