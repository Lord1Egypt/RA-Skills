#!/usr/bin/env python3
"""Fetch arxiv paper metadata and PDF.

Usage:
  python fetch_arxiv.py <arxiv_id_or_url> [output_dir]

Outputs JSON with title, authors, abstract, pdf_path.
"""
import sys
import os
import re
import json
import requests

def parse_arxiv_id(s: str) -> str:
    """Extract arxiv ID from URL or raw ID."""
    # https://arxiv.org/abs/2301.12345 or https://arxiv.org/pdf/2301.12345
    m = re.search(r'arxiv\.org/(?:abs|pdf)/([^\s?#]+)', s)
    if m:
        return m.group(1).rstrip('.pdf')
    # raw id like 2301.12345 or 2301.12345v2
    m = re.match(r'^(\d{4}\.\d{4,5}(?:v\d+)?)$', s.strip())
    if m:
        return m.group(1)
    return s.strip()

def fetch_metadata(arxiv_id: str) -> dict:
    """Fetch metadata via arxiv API."""
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    text = r.text
    # Simple XML parsing
    def tag(name):
        m = re.search(rf'<{name}[^>]*>(.*?)</{name}>', text, re.DOTALL)
        return m.group(1).strip() if m else ""
    title = tag("title")
    # skip the first <title> which is the feed title
    titles = re.findall(r'<title[^>]*>(.*?)</title>', text, re.DOTALL)
    title = titles[-1].strip() if len(titles) > 1 else title
    summary = tag("summary")
    authors = re.findall(r'<name>(.*?)</name>', text)
    published = tag("published")
    return {
        "arxiv_id": arxiv_id,
        "title": re.sub(r'\s+', ' ', title),
        "authors": authors,
        "abstract": re.sub(r'\s+', ' ', summary),
        "published": published,
        "abs_url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
    }

def download_pdf(arxiv_id: str, output_dir: str = ".") -> str:
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{arxiv_id.replace('/', '_')}.pdf")
    if os.path.exists(path):
        return path
    r = requests.get(url, timeout=120, stream=True)
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    return path

if __name__ == "__main__":
    raw = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "/tmp/arxiv_papers"
    arxiv_id = parse_arxiv_id(raw)
    meta = fetch_metadata(arxiv_id)
    pdf_path = download_pdf(arxiv_id, out_dir)
    meta["pdf_path"] = pdf_path
    print(json.dumps(meta, ensure_ascii=False))
