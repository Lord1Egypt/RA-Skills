#!/usr/bin/env python3
"""Extract text from resume files (PDF, DOCX, TXT, MD)"""
import sys
import argparse
from pathlib import Path

def extract_pdf(file_path):
    """Extract text from PDF"""
    try:
        import pypdf
        with open(file_path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            text = '\n\n'.join(page.extract_text() for page in reader.pages)
        return text
    except ImportError:
        print("Error: pypdf not installed. Run: pip install pypdf", file=sys.stderr)
        sys.exit(1)

def extract_docx(file_path):
    """Extract text from DOCX"""
    try:
        import docx
        doc = docx.Document(file_path)
        text = '\n\n'.join(para.text for para in doc.paragraphs if para.text.strip())
        return text
    except ImportError:
        print("Error: python-docx not installed. Run: pip install python-docx", file=sys.stderr)
        sys.exit(1)

def extract_text(file_path):
    """Extract text from TXT/MD"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser(description='Extract text from resume files')
    parser.add_argument('input', help='Input file path')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout)')
    args = parser.parse_args()

    file_path = Path(args.input)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    ext = file_path.suffix.lower()

    if ext == '.pdf':
        text = extract_pdf(file_path)
    elif ext in ['.docx', '.doc']:
        text = extract_docx(file_path)
    elif ext in ['.txt', '.md']:
        text = extract_text(file_path)
    else:
        print(f"Error: Unsupported file type: {ext}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Extracted to: {args.output}")
    else:
        print(text)

if __name__ == '__main__':
    main()
