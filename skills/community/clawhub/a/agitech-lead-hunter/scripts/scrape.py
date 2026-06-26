#!/usr/bin/env python3
"""
Lead Hunter - Stealth scraper fallback.
Uses Crawl4AI for sites that block simple HTTP requests.

Usage:
    python3 scrape.py <url> [--output markdown|json]
    python3 scrape.py --check  (verify crawl4ai is installed)

Returns clean markdown or JSON to stdout.
"""

import sys
import os
import json
import asyncio

VENV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv")

def ensure_venv():
    """Ensure venv exists and return the python path inside it."""
    venv_python = os.path.join(VENV_DIR, "bin", "python3")
    if os.path.exists(venv_python):
        return venv_python
    
    import subprocess
    print("Creating virtual environment...", file=sys.stderr)
    subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)
    return venv_python


def check_install():
    """Check if crawl4ai is installed in venv, install if not."""
    import subprocess
    venv_python = ensure_venv()
    
    # Check if crawl4ai is importable in venv
    check = subprocess.run(
        [venv_python, "-c", "import crawl4ai; print(crawl4ai.__version__)"],
        capture_output=True, text=True
    )
    
    if check.returncode == 0:
        print(json.dumps({"installed": True, "version": check.stdout.strip(), "venv": VENV_DIR}))
        return
    
    print("Installing crawl4ai...", file=sys.stderr)
    pip = os.path.join(VENV_DIR, "bin", "pip")
    result = subprocess.run(
        [pip, "install", "crawl4ai", "-q"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        # Install playwright chromium
        pw = os.path.join(VENV_DIR, "bin", "playwright")
        subprocess.run([pw, "install", "chromium"], capture_output=True, text=True)
        print(json.dumps({"installed": True, "fresh_install": True, "venv": VENV_DIR}))
    else:
        print(json.dumps({"installed": False, "error": result.stderr}))
        sys.exit(1)


async def scrape_url(url, output_format="markdown"):
    """Scrape a URL using Crawl4AI with stealth mode."""
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
    
    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
    )
    
    crawler_config = CrawlerRunConfig(
        wait_until="networkidle",
        page_timeout=30000,
    )
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url=url,
            config=crawler_config,
        )
        
        if not result.success:
            return {"success": False, "error": result.error_message or "Unknown error", "url": url}
        
        if output_format == "json":
            links_raw = result.links if isinstance(result.links, list) else list(result.links.values()) if isinstance(result.links, dict) else []
            return {
                "success": True,
                "url": url,
                "title": result.metadata.get("title", "") if result.metadata else "",
                "markdown": result.markdown[:50000] if result.markdown else "",
                "links": links_raw[:100] if links_raw else [],
            }
        else:
            return {
                "success": True,
                "url": url,
                "markdown": result.markdown[:50000],
            }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scrape.py <url> [--output markdown|json]")
        print("       python3 scrape.py --check")
        sys.exit(1)
    
    if sys.argv[1] == "--check":
        check_install()
        return
    
    # If we're not running inside the venv, re-exec inside it
    venv_python = os.path.join(VENV_DIR, "bin", "python3")
    if os.path.exists(venv_python) and sys.executable != venv_python:
        import subprocess
        result = subprocess.run([venv_python] + sys.argv, capture_output=True, text=True)
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
        sys.exit(result.returncode)
    
    url = sys.argv[1]
    output_format = "markdown"
    
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_format = sys.argv[idx + 1]
    
    result = asyncio.run(scrape_url(url, output_format))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
