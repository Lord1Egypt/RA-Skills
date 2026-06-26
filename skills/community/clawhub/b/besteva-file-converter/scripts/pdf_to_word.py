#!/usr/bin/env python3
"""
PDF to Word (.docx) Converter
Converts PDF files to editable Microsoft Word documents.

Dependencies:
    pip install pdf2docx

Usage:
    python pdf_to_word.py <input.pdf> [output.docx]
    python pdf_to_word.py --batch <input_dir> [--output-dir <dir>]
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from pdf2docx import Converter, parse
except ImportError:
    print("Error: pdf2docx is required. Install with: pip install pdf2docx")
    sys.exit(1)


def convert_single_pdf(input_path: str, output_path: str = None) -> str:
    """Convert a single PDF file to Word format."""
    input_file = Path(input_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if input_file.suffix.lower() != ".pdf":
        raise ValueError(f"Input file must be a .pdf file: {input_path}")
    
    # Determine output path
    if output_path is None:
        output_path = input_file.with_suffix(".docx")
    else:
        output_path = Path(output_path)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Converting: {input_file.name} -> {output_path.name}")
    
    try:
        cv = Converter(str(input_file))
        cv.convert(str(output_path), start=0, end=None)
        cv.close()
        
        print(f"✓ Successfully converted: {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"✗ Error converting {input_file.name}: {e}")
        raise


def batch_convert_pdf(input_dir: str, output_dir: str = None) -> list[str]:
    """Convert all PDF files in a directory."""
    input_path = Path(input_dir)
    
    if not input_path.is_dir():
        raise NotADirectoryError(f"Input directory not found: {input_dir}")
    
    if output_dir is None:
        output_dir = input_dir
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    pdf_files = list(input_path.glob("*.pdf"))
    pdf_files.extend(input_path.glob("*.PDF"))
    
    if not pdf_files:
        print(f"No PDF files found in: {input_dir}")
        return []
    
    print(f"Found {len(pdf_files)} PDF file(s)")
    
    results = []
    for pdf_file in sorted(pdf_files):
        out_file = output_path / pdf_file.with_suffix(".docx").name
        try:
            result = convert_single_pdf(str(pdf_file), str(out_file))
            results.append(result)
        except Exception as e:
            print(f"  Skipped {pdf_file.name}: {e}")
    
    summary = f"\nConverted {len(results)}/{len(pdf_files)} files successfully"
    print(summary)
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF files to Word (.docx) format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf_to_word.py document.pdf
  python pdf_to_word.py document.pdf output.docx
  python pdf_to_word.py --batch ./pdf_folder --output-dir ./word_folder
        """
    )
    
    parser.add_argument(
        "input",
        help="Input PDF file or directory (with --batch)"
    )
    
    parser.add_argument(
        "output", 
        nargs="?",
        help="Output Word file (optional)"
    )
    
    parser.add_argument(
        "--batch", "-b",
        action="store_true",
        help="Batch mode: convert all PDFs in a directory"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        help="Output directory for batch mode"
    )
    
    parser.add_argument(
        "--start", type=int, default=0,
        help="Start page number (default: 0)"
    )
    
    parser.add_argument(
        "--end", type=int, default=None,
        help="End page number (default: all pages)"
    )
    
    args = parser.parse_args()
    
    try:
        if args.batch:
            batch_convert_pdf(args.input, args.output_dir or args.output)
        else:
            convert_single_pdf(args.input, args.output)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
