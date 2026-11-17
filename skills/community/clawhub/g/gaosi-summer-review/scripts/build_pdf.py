#!/usr/bin/env python3
"""Render an HTML file to PDF via a Chromium-family headless browser.

Usage:
    python build_pdf.py <input.html> <output.pdf>

Auto-detects Microsoft Edge / Google Chrome / Chromium on Windows, macOS and Linux.
Falls back to the CHROME / EDGE environment variable if set.
"""
import os
import shutil
import subprocess
import sys

CANDIDATES = [
    # Windows
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    # macOS
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    # Linux / generic
    "msedge", "google-chrome", "chrome", "chromium", "chromium-browser",
]


def find_browser():
    for env in ("EDGE", "CHROME", "CHROMIUM"):
        p = os.environ.get(env)
        if p and os.path.exists(p):
            return p
    for c in CANDIDATES:
        if os.path.exists(c):
            return c
        found = shutil.which(c)
        if found:
            return found
    return None


def main():
    if len(sys.argv) != 3:
        print("Usage: python build_pdf.py <input.html> <output.pdf>", file=sys.stderr)
        sys.exit(2)
    html_path = os.path.abspath(sys.argv[1])
    pdf_path = os.path.abspath(sys.argv[2])
    if not os.path.exists(html_path):
        print(f"ERROR: input not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    browser = find_browser()
    if not browser:
        print("ERROR: no Chromium-family browser found. Install Edge/Chrome or set EDGE/CHROME env var.",
              file=sys.stderr)
        sys.exit(1)

    url = "file:///" + html_path if os.name == "nt" else "file://" + html_path
    cmd = [
        browser, "--headless", "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        url,
    ]
    print(f"Rendering with: {browser}")
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("ERROR: browser exited with code", e.returncode, file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(pdf_path):
        print("ERROR: PDF was not created.", file=sys.stderr)
        sys.exit(1)
    size = os.path.getsize(pdf_path)
    print(f"OK: {pdf_path} ({size} bytes)")


if __name__ == "__main__":
    main()
