#!/usr/bin/env python3
"""deadlinks — Fast broken link checker for Markdown files and websites.

Usage:
    deadlinks check FILE_OR_DIR [--recursive] [--timeout SECS] [--format json|text] [--external] [--verbose]
    deadlinks url URL [--depth N] [--timeout SECS] [--format json|text] [--verbose]

Examples:
    deadlinks check README.md
    deadlinks check docs/ --recursive --external
    deadlinks url https://example.com --depth 2
"""

import argparse
import concurrent.futures
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class LinkResult:
    source: str
    url: str
    line: int = 0
    status: str = "unknown"  # ok, broken, timeout, error, skipped
    status_code: int = 0
    error: str = ""
    response_time_ms: float = 0


@dataclass
class CheckResult:
    total: int = 0
    ok: int = 0
    broken: int = 0
    timeout: int = 0
    error: int = 0
    skipped: int = 0
    results: list = field(default_factory=list)


# Common patterns
MD_LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
MD_REF_RE = re.compile(r'^\[([^\]]+)\]:\s+(\S+)', re.MULTILINE)
HTML_HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
HTML_SRC_RE = re.compile(r'src=["\']([^"\']+)["\']', re.IGNORECASE)

SKIP_SCHEMES = {'mailto:', 'tel:', 'javascript:', 'data:', '#'}
USER_AGENT = 'deadlinks/1.0 (broken-link-checker)'


def extract_md_links(content: str, source: str) -> list[tuple[str, int]]:
    """Extract links from markdown content with line numbers."""
    links = []
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        for match in MD_LINK_RE.finditer(line):
            url = match.group(2).split(' ')[0]  # Strip title
            links.append((url, i))
        for match in MD_REF_RE.finditer(line):
            links.append((match.group(2), i))
    return links


def extract_html_links(content: str, source: str) -> list[tuple[str, int]]:
    """Extract links from HTML content."""
    links = []
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        for match in HTML_HREF_RE.finditer(line):
            links.append((match.group(1), i))
        for match in HTML_SRC_RE.finditer(line):
            links.append((match.group(1), i))
    return links


def should_skip(url: str) -> bool:
    """Check if URL should be skipped."""
    for scheme in SKIP_SCHEMES:
        if url.startswith(scheme):
            return True
    return False


def is_external(url: str) -> bool:
    """Check if URL is external (http/https)."""
    return url.startswith('http://') or url.startswith('https://')


def check_local_link(url: str, source_path: Path) -> LinkResult:
    """Check if a local file/anchor link exists."""
    result = LinkResult(source=str(source_path), url=url)

    # Strip anchor
    path_part = url.split('#')[0]
    if not path_part:
        result.status = "ok"  # Pure anchor
        return result

    # Resolve relative to source file's directory
    target = source_path.parent / path_part
    if target.exists():
        result.status = "ok"
    else:
        result.status = "broken"
        result.error = "File not found"
    return result


def check_url(url: str, source: str, line: int, timeout: float = 10) -> LinkResult:
    """Check if a URL is reachable."""
    result = LinkResult(source=source, url=url, line=line)

    if should_skip(url):
        result.status = "skipped"
        return result

    if not is_external(url):
        local = check_local_link(url, Path(source))
        local.line = line
        return local

    start = time.time()
    try:
        req = urllib.request.Request(
            url,
            method='HEAD',
            headers={'User-Agent': USER_AGENT}
        )
        resp = urllib.request.urlopen(req, timeout=timeout)
        result.status_code = resp.getcode()
        result.status = "ok" if result.status_code < 400 else "broken"
    except urllib.error.HTTPError as e:
        result.status_code = e.code
        # Some sites block HEAD, try GET for 405/403
        if e.code in (405, 403, 406):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
                resp = urllib.request.urlopen(req, timeout=timeout)
                result.status_code = resp.getcode()
                result.status = "ok" if result.status_code < 400 else "broken"
            except urllib.error.HTTPError as e2:
                result.status_code = e2.code
                result.status = "broken"
                result.error = str(e2)
            except Exception as e2:
                result.status = "error"
                result.error = str(e2)
        else:
            result.status = "broken"
            result.error = f"HTTP {e.code}"
    except TimeoutError:
        result.status = "timeout"
        result.error = f"Timeout after {timeout}s"
    except Exception as e:
        result.status = "error"
        result.error = str(e)

    result.response_time_ms = (time.time() - start) * 1000
    return result


def find_md_files(path: Path, recursive: bool = False) -> list[Path]:
    """Find markdown files in a directory."""
    if path.is_file():
        return [path]
    pattern = '**/*.md' if recursive else '*.md'
    files = list(path.glob(pattern))
    # Also check .mdx
    pattern2 = '**/*.mdx' if recursive else '*.mdx'
    files.extend(path.glob(pattern2))
    return sorted(files)


def check_files(paths: list[Path], external: bool = True, timeout: float = 10,
                verbose: bool = False, workers: int = 10) -> CheckResult:
    """Check all links in given files."""
    result = CheckResult()
    all_checks = []

    for path in paths:
        content = path.read_text(errors='replace')
        links = extract_md_links(content, str(path))

        for url, line in links:
            if not external and is_external(url):
                continue
            all_checks.append((url, str(path), line, timeout))

    result.total = len(all_checks)

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(check_url, url, src, ln, to): (url, src, ln)
            for url, src, ln, to in all_checks
        }
        for future in concurrent.futures.as_completed(futures):
            lr = future.result()
            result.results.append(lr)
            if lr.status == "ok":
                result.ok += 1
            elif lr.status == "broken":
                result.broken += 1
                if verbose or True:  # Always show broken
                    print(f"  ✗ {lr.source}:{lr.line} → {lr.url} ({lr.error or lr.status_code})", file=sys.stderr)
            elif lr.status == "timeout":
                result.timeout += 1
            elif lr.status == "error":
                result.error += 1
            elif lr.status == "skipped":
                result.skipped += 1

    return result


def crawl_url(start_url: str, depth: int = 1, timeout: float = 10,
              verbose: bool = False, workers: int = 10) -> CheckResult:
    """Crawl a website and check all links."""
    from html.parser import HTMLParser

    parsed_start = urllib.parse.urlparse(start_url)
    base_domain = parsed_start.netloc
    result = CheckResult()
    visited = set()
    to_visit = [(start_url, 0)]

    while to_visit:
        url, current_depth = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        if verbose:
            print(f"  Crawling: {url} (depth {current_depth})", file=sys.stderr)

        try:
            req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
            resp = urllib.request.urlopen(req, timeout=timeout)
            content = resp.read().decode('utf-8', errors='replace')
        except Exception as e:
            lr = LinkResult(source=url, url=url, status="error", error=str(e))
            result.results.append(lr)
            result.error += 1
            result.total += 1
            continue

        links = extract_html_links(content, url)
        md_links = extract_md_links(content, url)
        all_links = links + md_links

        checks = []
        for link_url, line in all_links:
            if should_skip(link_url):
                continue
            # Resolve relative URLs
            full_url = urllib.parse.urljoin(url, link_url)
            checks.append((full_url, url, line, timeout))

            # Queue same-domain links for crawling
            if current_depth < depth:
                parsed = urllib.parse.urlparse(full_url)
                if parsed.netloc == base_domain and full_url not in visited:
                    to_visit.append((full_url, current_depth + 1))

        result.total += len(checks)
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {
                pool.submit(check_url, u, s, ln, to): (u, s, ln)
                for u, s, ln, to in checks
            }
            for future in concurrent.futures.as_completed(futures):
                lr = future.result()
                result.results.append(lr)
                if lr.status == "ok":
                    result.ok += 1
                elif lr.status == "broken":
                    result.broken += 1
                    print(f"  ✗ {lr.source} → {lr.url} ({lr.error or lr.status_code})", file=sys.stderr)
                elif lr.status == "timeout":
                    result.timeout += 1
                elif lr.status == "error":
                    result.error += 1
                elif lr.status == "skipped":
                    result.skipped += 1

    return result


def format_output(result: CheckResult, fmt: str = "text") -> str:
    if fmt == "json":
        return json.dumps({
            "summary": {
                "total": result.total,
                "ok": result.ok,
                "broken": result.broken,
                "timeout": result.timeout,
                "error": result.error,
                "skipped": result.skipped,
            },
            "broken_links": [
                {"source": r.source, "line": r.line, "url": r.url,
                 "status_code": r.status_code, "error": r.error}
                for r in result.results if r.status in ("broken", "timeout", "error")
            ]
        }, indent=2)

    lines = []
    broken = [r for r in result.results if r.status in ("broken", "timeout", "error")]
    if broken:
        lines.append(f"\n{'='*60}")
        lines.append(f"BROKEN LINKS ({len(broken)})")
        lines.append(f"{'='*60}")
        for r in sorted(broken, key=lambda x: (x.source, x.line)):
            loc = f"{r.source}:{r.line}" if r.line else r.source
            code = f" [{r.status_code}]" if r.status_code else ""
            err = f" - {r.error}" if r.error else ""
            lines.append(f"  {loc}")
            lines.append(f"    → {r.url}{code}{err}")
        lines.append("")

    lines.append(f"Total: {result.total} | ✓ {result.ok} | ✗ {result.broken} | ⏱ {result.timeout} | ⚠ {result.error} | ⊘ {result.skipped}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        prog='deadlinks',
        description='Fast broken link checker for Markdown files and websites'
    )
    sub = parser.add_subparsers(dest='command')

    # check command
    check_p = sub.add_parser('check', help='Check links in markdown files')
    check_p.add_argument('path', help='File or directory to check')
    check_p.add_argument('--recursive', '-r', action='store_true', help='Recurse into directories')
    check_p.add_argument('--external', '-e', action='store_true', help='Also check external URLs')
    check_p.add_argument('--timeout', '-t', type=float, default=10, help='Request timeout in seconds')
    check_p.add_argument('--format', '-f', choices=['text', 'json'], default='text')
    check_p.add_argument('--verbose', '-v', action='store_true')
    check_p.add_argument('--workers', '-w', type=int, default=10, help='Concurrent workers')

    # url command
    url_p = sub.add_parser('url', help='Crawl and check a website')
    url_p.add_argument('url', help='Starting URL')
    url_p.add_argument('--depth', '-d', type=int, default=1, help='Crawl depth')
    url_p.add_argument('--timeout', '-t', type=float, default=10)
    url_p.add_argument('--format', '-f', choices=['text', 'json'], default='text')
    url_p.add_argument('--verbose', '-v', action='store_true')
    url_p.add_argument('--workers', '-w', type=int, default=10)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'check':
        path = Path(args.path)
        if not path.exists():
            print(f"Error: {path} does not exist", file=sys.stderr)
            sys.exit(1)

        files = find_md_files(path, args.recursive)
        if not files:
            print(f"No markdown files found in {path}", file=sys.stderr)
            sys.exit(1)

        print(f"Checking {len(files)} file(s)...", file=sys.stderr)
        result = check_files(files, external=args.external, timeout=args.timeout,
                            verbose=args.verbose, workers=args.workers)
        print(format_output(result, args.format))
        sys.exit(1 if result.broken > 0 else 0)

    elif args.command == 'url':
        print(f"Crawling {args.url} (depth {args.depth})...", file=sys.stderr)
        result = crawl_url(args.url, depth=args.depth, timeout=args.timeout,
                          verbose=args.verbose, workers=args.workers)
        print(format_output(result, args.format))
        sys.exit(1 if result.broken > 0 else 0)


if __name__ == '__main__':
    main()
