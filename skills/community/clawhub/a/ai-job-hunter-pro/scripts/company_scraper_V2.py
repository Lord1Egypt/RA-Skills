#!/usr/bin/env python3
"""
AI Job Hunter Pro — Company Career Page Scraper
Scrapes job listings directly from target company career websites.

Usage:
  python3 scripts/company_scraper.py --companies google,microsoft,amazon
  python3 scripts/company_scraper.py --all --keywords "product manager"
"""

import argparse
import json
import os
import sys
import time
import hashlib
from datetime import datetime
from urllib.parse import quote_plus

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("[ERROR] playwright not installed.")
    sys.exit(1)

OUTPUT_DIR = os.path.expanduser("~/.ai-job-hunter-pro")

# ---------------------------------------------------------------------------
# Company Career Page Configs
# ---------------------------------------------------------------------------
COMPANY_CONFIGS = {
    "google": {
        "name": "Google",
        "url": "https://www.google.com/about/careers/applications/jobs/results/?location=Shanghai&location=Beijing&location=Hangzhou&q={keywords}",
        "selectors": {
            "cards": "[class*='lLd2De'], .sMn82b, li.lLd2De",
            "title": "h3, [class*='QJPWVe']",
            "location": "[class*='r0wTof'], [class*='location']",
            "link": "a[href*='/jobs/results/']",
        }
    },
    "microsoft": {
        "name": "Microsoft",
        "url": "https://jobs.careers.microsoft.com/global/en/search?q={keywords}&l=Shanghai&l=Beijing&exp=Experienced&rb=Experienced",
        "selectors": {
            "cards": "[class*='ms-List-cell'], .card-content, [data-automation-id]",
            "title": "h2, [class*='job-title'], a[aria-label]",
            "location": "[class*='location'], [class*='subText']",
            "link": "a[href*='/job/']",
        }
    },
    "amazon": {
        "name": "Amazon",
        "url": "https://www.amazon.jobs/en/search?base_query={keywords}&loc_query=Shanghai%2C+China&loc_query=Beijing%2C+China",
        "selectors": {
            "cards": ".job-tile, [class*='job-card'], .result",
            "title": "h3 a, .job-title a, h3",
            "location": ".location-and-id, [class*='location']",
            "link": "a[href*='/jobs/']",
        }
    },
    "apple": {
        "name": "Apple",
        "url": "https://jobs.apple.com/en-us/search?search={keywords}&location=shanghai-APSH+beijing-APBJ",
        "selectors": {
            "cards": ".table-row, [class*='results'] tr, tbody tr",
            "title": "a.table--advanced-search__title, td:first-child a",
            "location": ".table--advanced-search__location, td:nth-child(2)",
            "link": "a[href*='/details/']",
        }
    },
    "booking": {
        "name": "Booking.com",
        "url": "https://jobs.booking.com/careers?query={keywords}&location=Shanghai",
        "selectors": {
            "cards": ".js-job-tile, [class*='job-card'], .card",
            "title": "h3, .job-title, a[class*='title']",
            "location": ".location, [class*='location']",
            "link": "a[href*='/job/'], a[href*='careers']",
        }
    },
    "bytedance": {
        "name": "ByteDance",
        "url": "https://jobs.bytedance.com/en/position?keywords={keywords}&location=CT_51&category=",
        "selectors": {
            "cards": ".position-item, [class*='job-card'], .list-item",
            "title": ".position-name, h3, [class*='title']",
            "location": ".position-address, [class*='location']",
            "link": "a[href*='/position/']",
        }
    },
    "alibaba": {
        "name": "Alibaba",
        "url": "https://talent.alibaba.com/off-campus/position-list?lang=en&keyword={keywords}&location=330100,310100",
        "selectors": {
            "cards": ".position-item, [class*='job-item'], .list-item",
            "title": ".position-name, h4, [class*='title']",
            "location": ".position-city, [class*='location']",
            "link": "a[href*='/position/']",
        }
    },
    "tencent": {
        "name": "Tencent",
        "url": "https://careers.tencent.com/en-us/search.html?keyword={keywords}&pcity=Shanghai,Hangzhou",
        "selectors": {
            "cards": ".recruit-list-item, .post-item, [class*='job-item']",
            "title": ".recruit-title, h4, [class*='title']",
            "location": ".recruit-tips span, [class*='location']",
            "link": "a[href*='position']",
        }
    },
}


class CompanyCareerScraper:
    """Scrape jobs from company career pages."""

    def __init__(self, page):
        self.page = page

    def scrape_company(self, company_key: str, keywords: str, max_results: int = 15) -> list:
        """Scrape a single company's career page."""
        config = COMPANY_CONFIGS.get(company_key)
        if not config:
            print(f"  [WARN] Unknown company: {company_key}")
            return []

        name = config["name"]
        url = config["url"].format(keywords=quote_plus(keywords))
        sel = config["selectors"]

        print(f"  [{name}] Searching: {keywords}")
        print(f"  [{name}] URL: {url[:80]}...")

        try:
            self.page.goto(url, timeout=20000, wait_until="domcontentloaded")
            time.sleep(4)  # Wait for dynamic content

            # Scroll to load more
            for _ in range(2):
                self.page.evaluate("window.scrollBy(0, 600)")
                time.sleep(1)

            # Try to find job cards
            cards = self.page.query_selector_all(sel["cards"])
            print(f"  [{name}] Found {len(cards)} cards")

            jobs = []
            for card in cards[:max_results]:
                try:
                    job = self._parse_card(card, sel, name, company_key)
                    if job and job.get("title"):
                        jobs.append(job)
                except Exception as e:
                    continue

            # If no cards found via selectors, try generic approach
            if not jobs:
                jobs = self._fallback_scrape(name, company_key, keywords)

            return jobs

        except Exception as e:
            print(f"  [{name}] Error: {e}")
            return []

    def _parse_card(self, card, sel: dict, company_name: str, company_key: str) -> dict:
        """Parse a job card using company-specific selectors."""
        title_el = card.query_selector(sel["title"])
        location_el = card.query_selector(sel["location"])
        link_el = card.query_selector(sel["link"])

        title = title_el.inner_text().strip() if title_el else ""
        location = location_el.inner_text().strip() if location_el else ""
        href = ""
        if link_el:
            href = link_el.get_attribute("href") or ""

        if not title or len(title) < 3:
            return None

        job_id = hashlib.md5(f"{company_key}_{title}".encode()).hexdigest()[:12]

        return {
            "id": f"co_{job_id}",
            "title": title,
            "company": company_name,
            "location": location,
            "url": href if href.startswith("http") else "",
            "platform": f"career_{company_key}",
            "description": "",
            "scraped_at": datetime.now().isoformat()
        }

    def _fallback_scrape(self, company_name: str, company_key: str, keywords: str) -> list:
        """Fallback: extract all links that look like job postings."""
        print(f"  [{company_name}] Trying fallback scrape...")
        jobs = []

        # Find all links on the page that might be job listings
        links = self.page.query_selector_all("a")
        kw_lower = keywords.lower().split()

        for link in links:
            try:
                text = link.inner_text().strip()
                href = link.get_attribute("href") or ""

                # Check if the link text contains our keywords
                text_lower = text.lower()
                if any(kw in text_lower for kw in ["product", "manager", "pm", "产品"]):
                    if len(text) > 5 and len(text) < 120:
                        job_id = hashlib.md5(f"{company_key}_{text}".encode()).hexdigest()[:12]
                        jobs.append({
                            "id": f"co_{job_id}",
                            "title": text,
                            "company": company_name,
                            "location": "",
                            "url": href if href.startswith("http") else "",
                            "platform": f"career_{company_key}",
                            "description": "",
                            "scraped_at": datetime.now().isoformat()
                        })
            except:
                continue

        # Deduplicate
        seen = set()
        unique = []
        for j in jobs:
            if j["title"] not in seen:
                seen.add(j["title"])
                unique.append(j)

        print(f"  [{company_name}] Fallback found {len(unique)} jobs")
        return unique[:15]


def main():
    parser = argparse.ArgumentParser(description="AI Job Hunter Pro — Company Career Scraper")
    parser.add_argument("--companies", type=str, default="google,microsoft,amazon,bytedance",
                        help="Comma-separated company keys")
    parser.add_argument("--all", action="store_true", help="Scrape all configured companies")
    parser.add_argument("--keywords", type=str, default="Product Manager",
                        help="Search keywords")
    parser.add_argument("--output", type=str,
                        default=os.path.join(OUTPUT_DIR, "jobs_company.json"))
    parser.add_argument("--visible", action="store_true", help="Show browser")
    parser.add_argument("--match", action="store_true", help="Run RAG matching after scrape")
    parser.add_argument("--min-score", type=float, default=0.0)
    parser.add_argument("--merge", action="store_true",
                        help="Merge with existing jobs_scraped.json")

    args = parser.parse_args()

    if args.all:
        companies = list(COMPANY_CONFIGS.keys())
    else:
        companies = [c.strip().lower() for c in args.companies.split(",")]

    print(f"\n{'='*60}")
    print(f"AI Job Hunter Pro — Company Career Scraper")
    print(f"{'='*60}")
    print(f"Companies: {', '.join(companies)}")
    print(f"Keywords: {args.keywords}")
    print(f"{'='*60}\n")

    all_jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.visible)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="en-US"
        )
        page = context.new_page()
        scraper = CompanyCareerScraper(page)

        for company in companies:
            print(f"\n--- {company} ---")
            jobs = scraper.scrape_company(company, args.keywords)
            all_jobs.extend(jobs)
            time.sleep(2)

        browser.close()

    # Deduplicate
    seen = set()
    unique = []
    for j in all_jobs:
        key = f"{j['title'].lower()}_{j['company'].lower()}"
        if key not in seen:
            seen.add(key)
            unique.append(j)

    print(f"\n{'='*60}")
    print(f"Total unique jobs from company sites: {len(unique)}")
    print(f"{'='*60}")

    # Save
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)
    print(f"Saved to {args.output}")

    # Merge with LinkedIn/Indeed data if requested
    if args.merge:
        linkedin_path = os.path.join(OUTPUT_DIR, "jobs_scraped.json")
        if os.path.exists(linkedin_path):
            with open(linkedin_path) as f:
                linkedin_jobs = json.load(f)
            merged = linkedin_jobs + unique
            # Deduplicate merged
            seen2 = set()
            merged_unique = []
            for j in merged:
                key = f"{j['title'].lower()}_{j['company'].lower()}"
                if key not in seen2:
                    seen2.add(key)
                    merged_unique.append(j)
            merged_path = os.path.join(OUTPUT_DIR, "jobs_all.json")
            with open(merged_path, "w", encoding="utf-8") as f:
                json.dump(merged_unique, f, ensure_ascii=False, indent=2)
            print(f"Merged {len(merged_unique)} total jobs → {merged_path}")

    # RAG matching
    if args.match:
        print(f"\n{'='*60}")
        print("Running RAG matching...")
        print(f"{'='*60}")
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
            from rag_engine import RAGEngine
            engine = RAGEngine()
            if engine.resume_collection.count() == 0:
                print("[WARN] No resume imported.")
            else:
                match_source = unique
                if args.merge and os.path.exists(os.path.join(OUTPUT_DIR, "jobs_all.json")):
                    with open(os.path.join(OUTPUT_DIR, "jobs_all.json")) as f:
                        match_source = json.load(f)

                matched = engine.match_jobs(match_source, min_score=args.min_score)
                print(f"\nMatched {len(matched)} jobs:\n")
                for i, job in enumerate(matched[:20], 1):
                    s = job["match_score"]
                    src = job.get("platform", "?")
                    bar = chr(9608) * int(s * 20) + chr(9617) * (20 - int(s * 20))
                    print(f"  {i:2d}. [{bar}] {s:.3f}  {job['title']}")
                    print(f"      {job['company']} | {job.get('location','')} | {src}")
                    print()

                match_path = os.path.join(OUTPUT_DIR, "jobs_scraped_matched.json")
                with open(match_path, "w", encoding="utf-8") as f:
                    json.dump(matched, f, ensure_ascii=False, indent=2)
                print(f"Matched results saved to {match_path}")
        except ImportError as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
