#!/usr/bin/env python3
"""
Word (.docx) to PDF Converter
Converts Microsoft Word documents to PDF format.

Dependencies:
    pip install docx2pdf

Note: On Windows, docx2pdf uses Microsoft Word (must be installed).
      For headless conversion, consider using libreoffice or other alternatives.

Usage:
    python word_to_pdf.py <input.docx> [output.pdf]
    python word_to_pdf.py --batch <input_dir> [--output-dir <dir>]
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from docx2pdf import convert
except ImportError:
    print("Error: docx2pdf is required. Install with: pip install docx2pdf")
    print("Note: Microsoft Word must be installed on Windows for this library to work.")
    sys.exit(1)


def convert_single_word(input_path: str, output_path: str = None) -> str:
    """Convert a single Word file to PDF format."""
    
    input_file = Path(input_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Support both .doc and .docx
    valid_extensions = {".doc", ".docx", ".DOC", ".DOCX"}
    if input_file.suffix not in valid_extensions:
        raise ValueError(f"Input file must be a .doc or .docx file: {input_path}")
    
    # Determine output path
    if output_path is None:
        output_path = input_file.with_suffix(".pdf")
    else:
        output_path = Path(output_path)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Converting: {input_file.name} -> {output_path.name}")
    
    try:
        convert(str(input_file), str(output_path))
        
        # Verify output
        if output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            print(f"✓ Successfully converted: {output_path} ({size_kb:.1f}KB)")
            return str(output_path)
        else:
            raise RuntimeError("Conversion completed but output file was not created")
            
    except Exception as e:
        print(f"✗ Error converting {input_file.name}: {e}")
        raise


def batch_convert_word(input_dir: str, output_dir: str = None) -> list[str]:
    """Convert all Word files in a directory."""
    
    input_path = Path(input_dir)
    
    if not input_path.is_dir():
        raise NotADirectoryError(f"Input directory not found: {input_dir}")
    
    if output_dir is None:
        output_dir = input_dir
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all .doc and .docx files
    word_files = []
    for ext in ["*.docx", "*.doc"]:
        word_files.extend(input_path.glob(ext))
        word_files.extend(input_path.glob(ext.upper()))
    
    # Deduplicate (case-insensitive)
    seen_lower = set()
    unique_files = []
    for f in sorted(word_files):
        f_lower = str(f).lower()
        if f_lower not in seen_lower:
            seen_lower.add(f_lower)
            unique_files.append(f)
    
    if not unique_files:
        print(f"No Word files (.doc/.docx) found in: {input_dir}")
        return []
    
    print(f"Found {len(unique_files)} Word document(s)")
    
    results = []
    errors = []
    
    for word_file in unique_files:
        out_file = output_path / f"{word_file.stem}.pdf"
        try:
            result = convert_single_word(str(word_file), str(out_file))
            results.append(result)
        except Exception as e:
            errors.append((word_file.name, str(e)))
            continue
    
    summary = f"\nConverted {len(results)}/{len(unique_files)} files successfully"
    if errors:
        summary += f"\nErrors ({len(errors)}):"
        for fname, err in errors[:5]:
            summary += f"\n  - {fname}: {err}"
        if len(errors) > 5:
            summary += f"\n  ... and {len(errors)-5} more"
    print(summary)
    
    return results


def check_requirements() -> dict:
    """Check if system requirements are met."""
    info = {
        "python": True,
        "docx2pdf": True,
        "word_installed": False,
        "platform": os.name,
    }
    
    try:
        import platform
        info["platform_detail"] = platform.system()
        
        if platform.system() == "Windows":
            # Try to detect if MS Word is installed via registry or common paths
            word_paths = [
                Path(r"C:\Program Files\Microsoft Office\Office\WINWORD.EXE"),
                Path(r"C:\Program Files (x86)\Microsoft Office\Office\WINWORD.EXE"),
                Path(r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"),
                Path(r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE"),
            ]
            info["word_installed"] = any(p.exists() for p in word_paths)
        
    except ImportError:
        pass
    
    return info


def main():
    parser = argparse.ArgumentParser(
        description="Convert Word documents (.doc/.docx) to PDF format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python word_to_pdf.py document.docx
  python word_to_pdf.py report.docx report.pdf
  python word_to_pdf.py --batch ./documents --output-dir ./pdfs
  python word_to_pdf.py --check
  
Requirements (Windows):
  - Python 3.6+
  - pip install docx2pdf
  - Microsoft Word installed
        """
    )
    
    parser.add_argument("input", nargs="?", help="Input Word file or directory (with --batch)")
    parser.add_argument("output", nargs="?", help="Output PDF file/directory (optional)")
    parser.add_argument("--batch", "-b", action="store_true", help="Batch mode: convert all Word docs in directory")
    parser.add_argument("--output-dir", "-o", help="Output directory for batch mode")
    parser.add_argument("--check", action="store_true", help="Check system requirements only")
    
    args = parser.parse_args()
    
    if args.check:
        info = check_requirements()
        print("\n=== System Requirements Check ===\n")
        print(f"Platform: {info.get('platform_detail', 'Unknown')}")
        print(f"docx2pdf installed: {'✓' if info['docx2pdf'] else '✗'}")
        
        if info["platform"] == "nt":
            print(f"MS Word detected: {'✓' if info['word_installed'] else '✗ (required)'}")
        
        all_ok = info["docx2pdf"]
        if info["platform"] == "nt":
            all_ok = all_ok and info["word_installed"]
        
        print(f"\n{'Ready to use!' if all_ok else 'Some requirements are missing.'}")
        return
    
    if not args.input:
        parser.error("Input file is required. Use --help for usage information.")
    
    try:
        if args.batch:
            batch_convert_word(args.input, args.output_dir or args.output)
        else:
            convert_single_word(args.input, args.output)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
