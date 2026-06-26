#!/usr/bin/env python3
"""
Batch download Chinese ebooks from online sources via file hosting service.
Usage: python batch_download.py --book-list books.json --output-dir ~/Books/
Supports resume via _progress.json.
"""
import sys
import os
import json
import asyncio
import time
import re
import subprocess
from pathlib import Path

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from search_secondary_source import search_yabook as search_secondary_source, decrypt_ctfile as decrypt_file_host, get_download_url
from search_source_c import search_annas_archive as search_source_c, download_book_from_annas_archive as download_from_source_c

def _import_download_book():
    from download_book import download_book as download_from_primary, download_with_curl, verify_file, sanitize_filename, extract_zip
    return download_from_primary, download_with_curl, verify_file, sanitize_filename, extract_zip


def sanitize_filename(name: str) -> str:
    """Clean filename for filesystem."""
    name = re.sub(r'[\[\]【】（）()《》]', '', name)
    name = re.sub(r'[：:]', ' -', name)
    name = re.sub(r'[\\/:*?"<>|]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name[:200]


def detect_format_from_files(files: list) -> str:
    """Detect the format(s) of extracted ebook files. Returns 'pdf', 'epub', etc. or 'unknown'."""
    formats = set()
    for f in files:
        ext = Path(f).suffix.lower().lstrip('.')
        if ext in ('pdf', 'epub', 'mobi', 'azw3'):
            formats.add(ext.upper())
    return ', '.join(sorted(formats)) if formats else 'unknown'


def sanitize_filename(name: str) -> str:
    """Clean filename for filesystem."""
    name = re.sub(r'[\[\]【】（）()《》]', '', name)
    name = re.sub(r'[：:]', ' -', name)
    name = re.sub(r'[\\/:*?"<>|]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name[:200]


def load_progress(output_dir: str) -> dict:
    """Load progress file."""
    progress_file = os.path.join(output_dir, '_progress.json')
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return json.load(f)
    return {}


def save_progress(output_dir: str, progress: dict):
    """Save progress file."""
    progress_file = os.path.join(output_dir, '_progress.json')
    with open(progress_file, 'w') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def download_with_curl(url: str, output_path: str) -> bool:
    """Download file with curl."""
    cmd = [
        'curl', '-L', '-o', output_path, url,
        '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        '-H', 'Referer: https://placeholder.example.com/',
        '--max-time', '600',
        '--connect-timeout', '30'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def verify_file(filepath: str) -> bool:
    """Verify downloaded file is valid."""
    if not os.path.exists(filepath):
        return False
    size = os.path.getsize(filepath)
    if size < 1024:  # Too small, probably an error page
        return False
    
    result = subprocess.run(['file', filepath], capture_output=True, text=True)
    output = result.stdout.lower()
    
    # Check for valid document types
    valid_types = ['pdf document', 'epub', 'mobi', 'zip archive']
    return any(t in output for t in valid_types) or size > 1024 * 1024  # >1MB is likely valid


async def download_from_secondary(title: str, author: str, output_dir: str, preferred_format: str = "pdf", browser=None) -> dict:
    """Try secondary book source. Returns {"status": "done"|"failed", ...}"""
    try:
        search_fn = search_secondary_source
    except ImportError:
        return {"status": "failed", "error": "Secondary source module not available"}

    results = await search_fn(title, author, browser=browser)
    if not results:
        return {"status": "failed", "error": "No results on secondary source"}

    best = results[0]
    file_url = best.get('ctfile_url', best.get('file_url', ''))
    password = best.get('password', '')
    if not file_url:
        return {"status": "failed", "error": "No download link found"}

    api_vars = await decrypt_file_host(file_url, password, browser=browser)
    if not api_vars:
        return {"status": "failed", "error": "Could not decrypt file link (secondary)"}

    downurl = await get_download_url(api_vars, browser=browser)
    if not downurl:
        return {"status": "failed", "error": "Could not get download URL (secondary)"}

    print(f"  ⬇️  Downloading from secondary source...")
    clean = sanitize_filename(f"{title} - {author}")
    output_path = os.path.join(output_dir, f"{clean}.zip")
    success = download_with_curl(downurl, output_path)
    if not success:
        return {"status": "failed", "error": "curl download failed (secondary)"}

    # Try to extract ZIP with format filter
    try:
        extracted = extract_zip(output_path, output_dir, preferred_ext=preferred_format)
        os.remove(output_path)
        ebook_exts = ('.pdf', '.epub', '.mobi', '.azw3')
        if preferred_format != 'any':
            ebook_exts = (f'.{preferred_format}',)
        ebook_files = [f for f in extracted if f.lower().endswith(ebook_exts)]
        if ebook_files:
            return {"status": "done", "files": ebook_files, "source": "secondary"}
        # Files extracted but none match preferred format
        fmt = detect_format_from_files(extracted)
        return {"status": "format_mismatch", "available_formats": fmt, "source": "secondary", "files": extracted}
    except Exception:
        os.remove(output_path) if os.path.exists(output_path) else None
        return {"status": "failed", "error": "ZIP extraction failed (secondary)"}


async def download_from_tertiary(title: str, author: str, output_dir: str, preferred_format: str = "pdf", browser=None) -> dict:
    """Source C: Anna's Archive (search works, download may be blocked by DDoS-Guard)."""
    try:
        return await download_from_source_c(
            title=title, author=author, output_dir=output_dir,
            preferred_format=preferred_format, browser=browser,
        )
    except Exception as e:
        return {"status": "failed", "error": f"Source C error: {e}"}


async def download_book(title: str, author: str, output_dir: str, preferred_format: str = "pdf", browser=None) -> dict:
    """Download a single book with multi-source fallback and format awareness."""
    clean_title = sanitize_filename(f"{title} - {author}" if author else title)

    # Check if already downloaded (only for the preferred format)
    if preferred_format != 'any':
        p = os.path.join(output_dir, f"{clean_title}.{preferred_format}")
        if os.path.exists(p) and os.path.getsize(p) > 1024:
            return {"status": "done", "message": "Already exists", "source": "cache"}
    else:
        for ext in ('.pdf', '.epub', '.mobi', '.azw3'):
            p = os.path.join(output_dir, f"{clean_title}{ext}")
            if os.path.exists(p) and os.path.getsize(p) > 1024:
                return {"status": "done", "message": "Already exists", "source": "cache"}

    print(f"\n{'='*60}")
    print(f"📚 {title} - {author}")
    print(f"{'='*60}")

    available_formats = []  # Track what formats each source has

    # Source 1: Primary online library
    try:
        _dl = _import_download_book
        download_from_primary = _dl()[0]
        print(f"  🔍 Trying primary source (preferred: {preferred_format})...")
        result = await download_from_primary(title=title, author=author, output_dir=output_dir, preferred_format=preferred_format, browser=browser)
        if result.get('status') == 'done':
            result["source"] = "primary"
            return result
        if result.get('status') == 'format_mismatch':
            fmt = result.get('available_formats', 'unknown')
            available_formats.append(f"{fmt} (primary)")
            print(f"  ⚠️  Primary has wrong format: {fmt}")
        else:
            print(f"  ❌ Primary failed: {result.get('error', '?')}")
    except Exception as e:
        print(f"  ❌ Primary source error: {e}")

    # Source 2: Secondary source
    print(f"  🔍 Trying secondary source (preferred: {preferred_format})...")
    result = await download_from_secondary(title, author, output_dir, preferred_format=preferred_format, browser=browser)
    if result.get('status') == 'done':
        return result
    if result.get('status') == 'format_mismatch':
        fmt = result.get('available_formats', 'unknown')
        available_formats.append(f"{fmt} (secondary)")
        print(f"  ⚠️  Secondary has wrong format: {fmt}")
    else:
        print(f"  ❌ Secondary failed: {result.get('error', '?')}")

    # Source 3: Tertiary source
    result = await download_from_tertiary(title, author, output_dir, preferred_format=preferred_format, browser=browser)
    if result.get('status') == 'done':
        return result

    # Build failure message
    if available_formats and preferred_format != 'any':
        msg = f"No {preferred_format.upper()} available for this book. Sources returned: {', '.join(available_formats)}"
    elif result.get('error'):
        msg = result['error']
    else:
        msg = "All sources failed"
    return {"status": "failed", "error": msg}


async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch download Chinese ebooks")
    parser.add_argument('--book-list', required=True, help='JSON file with book list')
    parser.add_argument('--output-dir', required=True, help='Output directory')
    parser.add_argument('--start', type=int, default=0, help='Start index (0-based)')
    parser.add_argument('--limit', type=int, default=0, help='Max books to download (0=all)')
    parser.add_argument('--format', default='pdf', choices=['pdf', 'epub', 'mobi', 'azw3', 'any'],
                        help='Preferred format (default: pdf)')
    args = parser.parse_args()
    
    # Load book list
    with open(args.book_list, 'r') as f:
        books = json.load(f)
    
    os.makedirs(args.output_dir, exist_ok=True)
    progress = load_progress(args.output_dir)
    
    # Apply start/limit
    books = books[args.start:]
    if args.limit > 0:
        books = books[:args.limit]
    
    stats = {"done": 0, "failed": 0, "skipped": 0}

    from playwright.async_api import async_playwright
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=True)

    try:
        for i, book in enumerate(books):
            title = book.get('title', '')
            author = book.get('author', '')
            key = f"{title}|{author}"
            
            # Skip already done
            if progress.get(key) == 'done':
                print(f"⏭️  Skipping (already done): {title}")
                stats['skipped'] += 1
                continue
            
            # Skip previously failed (will retry)
            # Allow retry for 'failed' and 'retry' status
            
            result = await download_book(title, author, args.output_dir, preferred_format=args.format, browser=browser)
            
            # Save progress
            progress[key] = result['status']
            save_progress(args.output_dir, progress)
            
            if result['status'] == 'done':
                stats['done'] += 1
            else:
                stats['failed'] += 1
                print(f"❌ Failed: {result.get('error', 'Unknown')}")
            
            # Rate limiting - wait between books
            if i < len(books) - 1:
                wait = 5
                print(f"⏳ Waiting {wait}s before next book...")
                await asyncio.sleep(wait)
            
            # Report every 5 books
            if (i + 1) % 5 == 0:
                print(f"\n📊 Progress: {stats['done']} done, {stats['failed']} failed, {stats['skipped']} skipped ({i+1}/{len(books)})")
    finally:
        await browser.close()
        await pw.stop()
    
    # Final summary
    print(f"\n{'='*60}")
    print(f"📊 FINAL SUMMARY")
    print(f"  ✅ Downloaded: {stats['done']}")
    print(f"  ❌ Failed:     {stats['failed']}")
    print(f"  ⏭️  Skipped:    {stats['skipped']}")
    print(f"  📁 Output:     {args.output_dir}")
    print(f"{'='*60}")


if __name__ == '__main__':
    asyncio.run(main())
