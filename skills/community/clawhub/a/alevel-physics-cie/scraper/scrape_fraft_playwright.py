#!/usr/bin/env python3
"""
Scrape ALL 9702 physics papers from cie.fraft.org using Playwright (handles JS).

The site loads results via JavaScript when selecting subject/year/season.
This script iterates through all years and seasons, collects PDF links, and downloads them.

Usage:
  playwright install chromium   # first time only
  python -m scraper.scrape_fraft_playwright
"""

import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import yaml
from tqdm import tqdm

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

# CIE 9702 paper variants: qp_11..13 (P1), qp_21..23 (P2), qp_31..35 (P3), qp_41..45 (P4), qp_51..53 (P5)
QP_VARIANTS = [
    "11", "12", "13", "21", "22", "23",
    "31", "32", "33", "34", "35",
    "41", "42", "43", "44", "45",
    "51", "52", "53",
]
SEASONS = [("s", "夏季"), ("w", "冬季")]


def load_config() -> dict:
    cfg_path = PROJECT_ROOT / "config.yaml"
    if not cfg_path.exists():
        return {}
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_config() -> dict:
    cfg = load_config()
    scraper = cfg.get("scraper", {})
    return {
        "base_url": scraper.get("base_url", "https://cie.fraft.org").rstrip("/"),
        "subject_code": scraper.get("subject_code", "9702"),
        "output_dir": PROJECT_ROOT / scraper.get("output_dir", "data/raw"),
        "request_delay_sec": scraper.get("request_delay_sec", 1.0),
        "years": scraper.get("years", list(range(2015, 2026))),
    }


def scrape_with_playwright(config: dict) -> list[tuple[str, str]]:
    """Use Playwright to load page, iterate year/season, collect PDF links."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Install: pip install playwright && playwright install chromium")
        return []

    base = config["base_url"]
    if not base.startswith("http"):
        base = "https://" + base

    all_links = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_default_timeout(30000)

        for year in tqdm(config["years"], desc="Years"):
            for season_code, season_cn in SEASONS:
                try:
                    page.goto(base, wait_until="networkidle", timeout=60000)
                    time.sleep(1.5)

                    # Select subject 9702 (may already be default)
                    try:
                        page.select_option('select[name="subject"], select[id*="subject"], [data-subject]', "9702", timeout=3000)
                    except Exception:
                        pass

                    # Select year
                    year_str = str(year)
                    try:
                        for sel in ['select[name="year"]', 'select[id*="year"]', '[data-year]', 'select']:
                            opts = page.query_selector_all(f'{sel} option')
                            for opt in opts:
                                if year_str in (opt.get_attribute("value") or "") or year_str in (opt.inner_text() or ""):
                                    page.select_option(sel, opt.get_attribute("value") or opt.inner_text(), timeout=2000)
                                    break
                            else:
                                continue
                            break
                    except Exception:
                        pass

                    # Select season
                    try:
                        page.select_option('select[name="season"], select[id*="season"]', season_cn, timeout=2000)
                    except Exception:
                        try:
                            page.click(f'text="{season_cn}"', timeout=2000)
                        except Exception:
                            pass

                    time.sleep(2)
                    html = page.content()
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(html, "lxml")
                    for a in soup.find_all("a", href=True):
                        href = a["href"].strip()
                        if ".pdf" in href.lower() and "9702" in href:
                            full = urljoin(base, href)
                            name = Path(urlparse(href).path).name or "paper.pdf"
                            if (full, name) not in [(u, n) for u, n in all_links]:
                                all_links.append((full, name))

                except Exception as e:
                    print(f"  [WARN] {year} {season_code}: {e}")
                time.sleep(config["request_delay_sec"])

        browser.close()

    return all_links


def try_predictable_urls(config: dict) -> list[tuple[str, str]]:
    """Try known CIE URL patterns (e.g. from PapaCambridge, FRANK CIE)."""
    import requests
    base = config["base_url"].rstrip("/")
    if not base.startswith("http"):
        base = "https://" + base
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (compatible; Physics9702Scraper/1.0)"
    links = []
    for year in config["years"]:
        sy = str(year)[-2:]
        for sc, _ in SEASONS:
            for var in QP_VARIANTS:
                fname = f"9702_{sc}{sy}_qp_{var}.pdf"
                for prefix in ["/", "/files/", "/pdf/", "/9702/"]:
                    url = urljoin(base, prefix + fname)
                    try:
                        r = session.head(url, timeout=10, allow_redirects=True)
                        if r.status_code == 200:
                            links.append((r.url if r.history else url, fname))
                            break
                        r = session.get(url, timeout=15, stream=True)
                        if r.status_code == 200 and len(r.content) > 500:
                            links.append((url, fname))
                            break
                    except Exception:
                        pass
                    time.sleep(0.3)
    return links


def download_pdfs(links: list[tuple[str, str]], config: dict) -> list[dict]:
    """Download PDFs and return manifest items."""
    import requests
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (compatible; Physics9702Scraper/1.0)"
    out_dir = config["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for url, name in tqdm(links, desc="Downloading PDFs"):
        try:
            r = session.get(url, timeout=60, stream=True)
            r.raise_for_status()
            if len(r.content) < 500:
                continue
            path = out_dir / name
            with open(path, "wb") as f:
                f.write(r.content)
            results.append({"url": url, "type": "pdf", "title": name, "local_path": str(path)})
        except Exception as e:
            print(f"  [WARN] {name}: {e}")
        time.sleep(config["request_delay_sec"])
    return results


def main():
    config = get_config()
    print("Scraping cie.fraft.org for ALL 9702 physics papers...")
    links = scrape_with_playwright(config)
    if not links:
        print("Playwright found no links. Trying predictable URLs...")
        links = try_predictable_urls(config)
    if not links:
        print("No papers found. Check site structure or run with browser visible.")
        return
    seen = set()
    unique = [(u, n) for u, n in links if (u, n) not in seen and not seen.add((u, n))]
    print(f"Found {len(unique)} unique PDFs")
    results = download_pdfs(unique, config)
    manifest_path = config["output_dir"] / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({"base_url": config["base_url"], "source": "cie.fraft.org", "items": results}, f, indent=2)
    print(f"Saved {len(results)} PDFs to {config['output_dir']}")


if __name__ == "__main__":
    main()
