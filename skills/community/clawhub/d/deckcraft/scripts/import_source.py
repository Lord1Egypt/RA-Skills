#!/usr/bin/env python3
"""
DeckCraft v6 — Source Importer CLI

Convert a document (PDF, DOCX, TXT, MD) into a DeckCraft outline JSON file,
or fetch content from a URL / WeChat article.

Usage:
    # File-based import
    python3 import_source.py <source_file> -o outline.json
    python3 import_source.py report.pdf -o outline.json --theme tech --canvas 16:9

    # URL import
    python3 import_source.py url https://example.com -o output.md

    # WeChat import
    python3 import_source.py wechat https://mp.weixin.qq.com/s/xxx -o output.md

After importing, render the outline to PPTX:
  python3 scripts/generate_ppt.py -i outline.json -o deck.pptx
"""
import sys, os, json, argparse

# Add engine to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine.importers import detect_and_import
from engine.constants import THEMES, CANVAS_PRESETS


SUPPORTED_EXTS = {
    ".pdf": "PDF (via PyMuPDF)",
    ".docx": "Word document (via python-docx)",
    ".txt": "Plain text",
    ".md": "Markdown",
}


def _handle_url(args):
    """Handle 'url' subcommand."""
    parser = argparse.ArgumentParser(description="Import URL → Markdown")
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument("-o", "--output", default=None, help="Output file path")
    parsed = parser.parse_args(args)

    from importers.url import url_to_markdown
    try:
        md = url_to_markdown(parsed.url, parsed.output)
        if not parsed.output:
            print(md)
        return 0
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def _handle_wechat(args):
    """Handle 'wechat' subcommand."""
    parser = argparse.ArgumentParser(description="Import WeChat article → Markdown")
    parser.add_argument("url", help="WeChat article URL (mp.weixin.qq.com)")
    parser.add_argument("-o", "--output", default=None, help="Output file path")
    parsed = parser.parse_args(args)

    from importers.wechat import wechat_to_markdown
    try:
        md = wechat_to_markdown(parsed.url, parsed.output)
        if not parsed.output:
            print(md)
        return 0
    except (ValueError, RuntimeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def _handle_file():
    """Handle original file-based import."""
    parser = argparse.ArgumentParser(
        description="DeckCraft v6 — Import a document into an outline JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported formats:
  .pdf  — PDF (via PyMuPDF, requires `pip install pymupdf`)
  .docx — Word document (via python-docx, requires `pip install python-docx`)
  .txt  — Plain text
  .md   — Markdown (headings split sections)

Subcommands:
  url <URL> [-o output.md]          — Import from URL → Markdown
  wechat <URL> [-o output.md]       — Import WeChat article → Markdown

After import, render the outline to PPTX:
  python3 scripts/generate_ppt.py -i outline.json -o deck.pptx
        """,
    )
    parser.add_argument("source", help="Source file path (PDF, DOCX, TXT, MD)")
    parser.add_argument("-o", "--output", default=None,
                        help="Output outline JSON path (default: <source_basename>.json)")
    parser.add_argument("-t", "--theme", default="business",
                        help="Theme to embed in outline (default: business)")
    parser.add_argument("-c", "--canvas", default="16:9",
                        help="Canvas preset (default: 16:9)")
    parser.add_argument("--page-types", default=None,
                        help="Comma-separated explicit page types, e.g. 'cover,toc,content'")
    parser.add_argument("--max-pages", type=int, default=200,
                        help="Max slides to generate (default: 200)")
    parser.add_argument("--print", action="store_true",
                        help="Print the outline to stdout instead of writing a file")

    args = parser.parse_args()

    # Validate theme/canvas
    if args.theme not in THEMES:
        print(f"ERROR: Unknown theme: {args.theme!r}. "
              f"Available: {list(THEMES.keys())}", file=sys.stderr)
        return 1
    if args.canvas not in CANVAS_PRESETS:
        print(f"ERROR: Unknown canvas: {args.canvas!r}. "
              f"Available: {list(CANVAS_PRESETS.keys())}", file=sys.stderr)
        return 1

    # Validate source file
    if not os.path.isfile(args.source):
        print(f"ERROR: Source file not found: {args.source}", file=sys.stderr)
        return 2
    ext = os.path.splitext(args.source)[1].lower()
    if ext not in SUPPORTED_EXTS:
        print(f"ERROR: Unsupported file format: {ext!r}. Supported: {list(SUPPORTED_EXTS.keys())}",
              file=sys.stderr)
        return 2

    # Parse page types if provided
    page_types = None
    if args.page_types:
        page_types = [p.strip() for p in args.page_types.split(",") if p.strip()]
        if not page_types:
            print("ERROR: --page-types is empty", file=sys.stderr)
            return 1

    # Import
    try:
        outline = detect_and_import(
            args.source,
            page_types=page_types,
            theme=args.theme,
            canvas=args.canvas,
            max_pages=args.max_pages,
        )
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except ImportError as e:
        print(f"ERROR: Missing dependency: {e}. "
              f"Try: pip install pymupdf python-docx", file=sys.stderr)
        return 1

    # Output
    if args.print:
        print(json.dumps(outline, indent=2, ensure_ascii=False))
        return 0

    output_path = args.output
    if output_path is None:
        base = os.path.splitext(os.path.basename(args.source))[0]
        output_path = f"{base}_outline.json"

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
                exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(outline, f, indent=2, ensure_ascii=False)

    page_count = len(outline.get("pages", []))
    type_counts = {}
    for p in outline.get("pages", []):
        t = p.get("type", "?")
        type_counts[t] = type_counts.get(t, 0) + 1
    types_str = ", ".join(f"{k}×{v}" for k, v in sorted(type_counts.items()))

    print(f"✓ Imported {args.source} → {output_path}")
    print(f"  {page_count} slides: {types_str}")
    print(f"  theme={args.theme}, canvas={args.canvas}")
    print()
    print(f"Next: review/edit the outline, then run:")
    print(f"  python3 scripts/generate_ppt.py -i {output_path} -o deck.pptx")
    return 0


def main():
    # Check for subcommands
    if len(sys.argv) >= 2 and sys.argv[1] == "url":
        return _handle_url(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "wechat":
        return _handle_wechat(sys.argv[2:])
    return _handle_file()


if __name__ == "__main__":
    sys.exit(main())
