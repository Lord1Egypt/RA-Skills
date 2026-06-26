#!/usr/bin/env python3
"""Download a paper PDF to a themed folder."""

import argparse
import json
import os
import re
import sys
import urllib.request


def sanitize_filename(name: str, max_length: int = 150) -> str:
    """Sanitize and truncate filename."""
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = re.sub(r'[_\s]+', "_", name).strip("_. ")
    name = (name[:max_length] + "...") if len(name) > max_length else name
    return name + ".pdf" if not name.lower().endswith(".pdf") else name


def download_pdf(url: str, filepath: str, timeout: int = 120) -> bool:
    """Download PDF with progress indication."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as response, open(filepath, 'wb') as f:
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            for chunk in iter(lambda: response.read(8192), b''):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0 and downloaded % (1024 * 1024) < 8192:
                    print(f"Downloading: {downloaded/total_size*100:.1f}% ({downloaded/1024/1024:.1f}MB / {total_size/1024/1024:.1f}MB)", file=sys.stderr)
        print(f"✓ Downloaded: {filepath}", file=sys.stderr)
        return True
    except Exception as e:
        print(f"✗ Download failed: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Download a paper PDF")
    parser.add_argument("--url", help="Direct PDF URL")
    parser.add_argument("--theme", help="Theme folder name")
    parser.add_argument("--filename", help="Output filename")
    parser.add_argument("--papers_dir", default=r"C:\Users\Lenovo\Desktop\papers", help="Base directory")
    parser.add_argument("--json_input", help="JSON from search_papers. Use '-' for stdin")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout seconds")
    args = parser.parse_args()

    # Parse input
    paper = None
    if args.json_input == "-":
        paper = json.loads(sys.stdin.read().strip())
    elif args.json_input:
        paper = json.loads(args.json_input)
    
    if paper:
        if isinstance(paper, list) and paper:
            paper = paper[0]
        url = paper.get("pdf_url") or paper.get("openAccessPdf", {}).get("url", "")
        title = paper.get("title", "paper")
        year = paper.get("year", "")
        venue = paper.get("venue", "")
        theme = args.theme or venue or "papers"
        
        # Fallback: construct arXiv PDF URL if we have arXiv URL
        if not url and "arxiv.org/abs/" in paper.get("url", ""):
            arxiv_id = paper["url"].split("/abs/")[-1]
            url = f"https://arxiv.org/pdf/{arxiv_id}"
        
        filename = args.filename or f"{title}_{year}.pdf" if year else f"{title}.pdf"
    elif args.url:
        url, theme, filename = args.url, args.theme or "papers", args.filename or "paper.pdf"
    else:
        print("✗ Must provide --url or --json_input", file=sys.stderr)
        sys.exit(1)

    if not url:
        print("✗ No PDF URL found", file=sys.stderr)
        sys.exit(1)

    filepath = os.path.join(args.papers_dir, theme, sanitize_filename(filename))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    if download_pdf(url, filepath, args.timeout):
        print(json.dumps({"status": "success", "path": filepath, "size_mb": round(os.path.getsize(filepath)/1024/1024, 2), "url": url}, indent=2))
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
