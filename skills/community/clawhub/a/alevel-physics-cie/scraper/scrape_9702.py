#!/usr/bin/env python3
"""
Scrape CIE 9702 physics past papers from a configurable base URL.

Usage:
  python -m scraper.scrape_9702

For cie.fraft.org (FRANK CIE), this entry point delegates to
the dedicated API-based scraper.

Configure base_url in config.yaml.
"""

import json
import os
import re
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup
from tqdm import tqdm

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent


def load_config() -> dict:
    cfg_path = PROJECT_ROOT / "config.yaml"
    if not cfg_path.exists():
        return {}
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_scraper_config() -> dict:
    cfg = load_config()
    scraper = cfg.get("scraper", {})
    return {
        "base_url": scraper.get("base_url", "https://cie.fraft.org"),
        "subject_code": scraper.get("subject_code", "9702"),
        "output_dir": PROJECT_ROOT / scraper.get("output_dir", "data/raw"),
        "request_delay_sec": scraper.get("request_delay_sec", 1.5),
        "user_agent": scraper.get(
            "user_agent",
            "Mozilla/5.0 (compatible; Physics9702Scraper/1.0)",
        ),
    }


def fetch_page(url: str, session: requests.Session, config: dict) -> Optional[str]:
    try:
        r = session.get(
            url,
            timeout=30,
            headers={"User-Agent": config["user_agent"]},
            allow_redirects=True,
        )
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        print(f"  [WARN] Failed to fetch {url}: {e}")
        return None


def extract_links_from_html(html: str, base_url: str) -> list[tuple[str, str]]:
    """Extract links to papers (PDF or question pages). Returns [(href, text), ...]."""
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        text = (a.get_text() or "").strip()
        if not href or href.startswith("#") or href.startswith("javascript:"):
            continue
        full_url = urljoin(base_url, href)
        # Prefer PDFs and pages that look like papers
        if href.lower().endswith(".pdf"):
            links.append((full_url, text or "paper"))
        elif re.search(r"(paper|9702|past|question|exam)", href + " " + text, re.I):
            links.append((full_url, text or "page"))
    return links


def extract_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)


def save_raw(url: str, content: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    parsed = urlparse(url)
    name = re.sub(r"[^\w\-.]", "_", Path(parsed.path).name or "page")[:80]
    if not name.endswith(".html") and not name.endswith(".pdf"):
        name += ".html"
    out_path = output_dir / name
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    return out_path


def scrape_index(base_url: str, config: dict) -> list[dict]:
    """Scrape the main index and discover paper links."""
    session = requests.Session()
    index_url = base_url.rstrip("/")
    if not index_url.startswith("http"):
        index_url = "https://" + index_url

    print(f"Fetching index: {index_url}")
    html = fetch_page(index_url, session, config)
    if not html:
        print("  Could not fetch index. Trying common CIE paths...")
        for path in ["/physics-9702", "/9702", "/alevels/physics-9702"]:
            url = urljoin(index_url, path)
            html = fetch_page(url, session, config)
            if html:
                index_url = url
                break
        if not html:
            print("  No index content. Create data/raw manually or fix base_url.")
            return []

    out_dir = config["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    save_raw(index_url, html, out_dir)

    links = extract_links_from_html(html, index_url)
    seen = set()
    results = []
    for url, text in tqdm(links, desc="Discovering links"):
        if url in seen:
            continue
        seen.add(url)
        time.sleep(config["request_delay_sec"])
        if url.lower().endswith(".pdf"):
            try:
                r = session.get(url, timeout=60, headers={"User-Agent": config["user_agent"]})
                r.raise_for_status()
                name = re.sub(r"[^\w\-.]", "_", Path(urlparse(url).path).name or "paper")[:80]
                if not name.endswith(".pdf"):
                    name += ".pdf"
                pdf_path = out_dir / name
                out_dir.mkdir(parents=True, exist_ok=True)
                with open(pdf_path, "wb") as f:
                    f.write(r.content)
                results.append({"url": url, "type": "pdf", "title": text, "local_path": str(pdf_path)})
            except Exception as e:
                print(f"  [WARN] PDF download failed {url}: {e}")
                results.append({"url": url, "type": "pdf", "title": text})
            continue
        page_html = fetch_page(url, session, config)
        if page_html:
            save_raw(url, page_html, out_dir)
            results.append({"url": url, "type": "html", "title": text})
    return results


def main():
    config = get_scraper_config()
    base_url = config["base_url"]
    if "cie.fraft.org" in base_url or "fraft.org" in base_url:
        from scraper.scrape_fraft import main as fraft_main
        fraft_main()
        return

    print(f"Base URL: {base_url}")
    print(f"Output: {config['output_dir']}")

    results = scrape_index(base_url, config)
    manifest_path = config["output_dir"] / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({"base_url": base_url, "items": results}, f, indent=2)
    print(f"Saved manifest: {manifest_path} ({len(results)} items)")


if __name__ == "__main__":
    main()
