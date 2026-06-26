#!/usr/bin/env python3
"""
AI Job Hunter Pro — Job Scraper
Scrapes real job listings from LinkedIn and Indeed (no login required for search).
Feeds results into the RAG matching engine.

Usage:
  python3 scripts/job_scraper.py --platforms linkedin,indeed --output jobs_found.json
  python3 scripts/job_scraper.py --platforms linkedin --keywords "AI Product Manager" --location "Shanghai"
"""

import argparse
import json
import os
import sys
import time
import hashlib
import re
from datetime import datetime
from urllib.parse import quote_plus

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("[ERROR] playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_KEYWORDS = ["AI Product Manager", "Product Manager", "Technical Product Manager"]
DEFAULT_LOCATIONS = ["Shanghai", "Hangzhou", "Suzhou"]
OUTPUT_DIR = os.path.expanduser("~/.ai-job-hunter-pro")
MAX_JOBS_PER_SEARCH = 25


# ---------------------------------------------------------------------------
# LinkedIn Scraper (no login required for job search)
# ---------------------------------------------------------------------------
class LinkedInScraper:
    """Scrape LinkedIn job listings from public search pages."""

    SEARCH_URL = "https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}&f_TPR=r604800"
    # f_TPR=r604800 = past week

    def __init__(self, page):
        self.page = page

    def search(self, keywords: str, location: str, max_results: int = MAX_JOBS_PER_SEARCH) -> list:
        """Search LinkedIn jobs and extract listings."""
        url = self.SEARCH_URL.format(
            keywords=quote_plus(keywords),
            location=quote_plus(location)
        )
        print(f"  [LinkedIn] Searching: {keywords} in {location}")

        try:
            self.page.goto(url, timeout=30000, wait_until="domcontentloaded")
            time.sleep(3)

            # Scroll to load more results
            for _ in range(3):
                self.page.evaluate("window.scrollBy(0, 800)")
                time.sleep(1)

            # Extract job cards
            jobs = []
            cards = self.page.query_selector_all(".base-card, .job-search-card, [data-entity-urn]")

            if not cards:
                # Try alternative selectors
                cards = self.page.query_selector_all("li .base-search-card, ul.jobs-search__results-list > li")

            print(f"  [LinkedIn] Found {len(cards)} cards")

            for card in cards[:max_results]:
                try:
                    job = self._parse_card(card)
                    if job and job.get("title"):
                        jobs.append(job)
                except Exception as e:
                    continue

            return jobs

        except Exception as e:
            print(f"  [LinkedIn] Error: {e}")
            return []

    def _parse_card(self, card) -> dict:
        """Parse a single LinkedIn job card."""
        title_el = card.query_selector(".base-search-card__title, h3, .sr-only")
        company_el = card.query_selector(".base-search-card__subtitle, h4, .hidden-nested-link")
        location_el = card.query_selector(".job-search-card__location, .base-search-card__metadata span")
        link_el = card.query_selector("a.base-card__full-link, a[href*='/jobs/view/']")
        time_el = card.query_selector("time, .job-search-card__listdate")

        title = title_el.inner_text().strip() if title_el else ""
        company = company_el.inner_text().strip() if company_el else ""
        location = location_el.inner_text().strip() if location_el else ""
        url = link_el.get_attribute("href") if link_el else ""
        posted = time_el.inner_text().strip() if time_el else ""

        if not title:
            return None

        job_id = hashlib.md5(f"linkedin_{title}_{company}".encode()).hexdigest()[:12]

        return {
            "id": f"li_{job_id}",
            "title": title,
            "company": company,
            "location": location,
            "url": url.split("?")[0] if url else "",
            "posted": posted,
            "platform": "linkedin",
            "description": "",  # Will be filled by detail page scrape
            "scraped_at": datetime.now().isoformat()
        }

    def get_job_detail(self, job: dict) -> dict:
        """Visit job detail page to get full description."""
        if not job.get("url"):
            return job

        try:
            self.page.goto(job["url"], timeout=20000, wait_until="domcontentloaded")
            time.sleep(2)

            # Click "Show more" if present
            show_more = self.page.query_selector("button.show-more-less-html__button, .description__see-more-btn")
            if show_more:
                try:
                    show_more.click()
                    time.sleep(1)
                except:
                    pass

            # Extract description
            desc_el = self.page.query_selector(".show-more-less-html__markup, .description__text, .decorated-job-posting__details")
            if desc_el:
                job["description"] = desc_el.inner_text().strip()[:3000]

        except Exception as e:
            print(f"    [LinkedIn] Detail error for {job['title']}: {e}")

        return job


# ---------------------------------------------------------------------------
# Indeed Scraper
# ---------------------------------------------------------------------------
class IndeedScraper:
    """Scrape Indeed job listings."""

    SEARCH_URL = "https://www.indeed.com/jobs?q={keywords}&l={location}&fromage=7&sort=date"

    def __init__(self, page):
        self.page = page

    def search(self, keywords: str, location: str, max_results: int = MAX_JOBS_PER_SEARCH) -> list:
        """Search Indeed jobs."""
        url = self.SEARCH_URL.format(
            keywords=quote_plus(keywords),
            location=quote_plus(location)
        )
        print(f"  [Indeed] Searching: {keywords} in {location}")

        try:
            self.page.goto(url, timeout=30000, wait_until="domcontentloaded")
            time.sleep(3)

            jobs = []
            cards = self.page.query_selector_all(".job_seen_beacon, .resultContent, .jobsearch-ResultsList > li")

            print(f"  [Indeed] Found {len(cards)} cards")

            for card in cards[:max_results]:
                try:
                    job = self._parse_card(card)
                    if job and job.get("title"):
                        jobs.append(job)
                except:
                    continue

            return jobs

        except Exception as e:
            print(f"  [Indeed] Error: {e}")
            return []

    def _parse_card(self, card) -> dict:
        """Parse a single Indeed job card."""
        title_el = card.query_selector("h2.jobTitle a, .jobTitle span, h2 a")
        company_el = card.query_selector("[data-testid='company-name'], .companyName, .company")
        location_el = card.query_selector("[data-testid='text-location'], .companyLocation, .location")
        link_el = card.query_selector("h2.jobTitle a, h2 a[href]")
        salary_el = card.query_selector(".salary-snippet-container, .estimated-salary, [data-testid='attribute_snippet_testid']")
        snippet_el = card.query_selector(".job-snippet, .underShelfFooter, .heading6")

        title = title_el.inner_text().strip() if title_el else ""
        company = company_el.inner_text().strip() if company_el else ""
        location = location_el.inner_text().strip() if location_el else ""
        salary = salary_el.inner_text().strip() if salary_el else ""
        snippet = snippet_el.inner_text().strip() if snippet_el else ""

        href = ""
        if link_el:
            href = link_el.get_attribute("href") or ""
            if href and not href.startswith("http"):
                href = "https://www.indeed.com" + href

        if not title:
            return None

        job_id = hashlib.md5(f"indeed_{title}_{company}".encode()).hexdigest()[:12]

        return {
            "id": f"in_{job_id}",
            "title": title,
            "company": company,
            "location": location,
            "salary": salary,
            "url": href.split("&")[0] if href else "",
            "platform": "indeed",
            "description": snippet,
            "scraped_at": datetime.now().isoformat()
        }


# ---------------------------------------------------------------------------
# Main Scraper Orchestrator
# ---------------------------------------------------------------------------
class JobScraper:
    """Orchestrates scraping across multiple platforms."""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.all_jobs = []

    def scrape(self, keywords: list, locations: list, platforms: list,
               max_per_search: int = MAX_JOBS_PER_SEARCH, fetch_details: bool = True) -> list:
        """Run full scraping pipeline."""
        print(f"\n{'='*60}")
        print(f"AI Job Hunter Pro — Job Scraper")
        print(f"{'='*60}")
        print(f"Keywords: {keywords}")
        print(f"Locations: {locations}")
        print(f"Platforms: {platforms}")
        print(f"Headless: {self.headless}")
        print(f"{'='*60}\n")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
                locale="en-US"
            )
            page = context.new_page()

            # Initialize scrapers
            scrapers = {}
            if "linkedin" in platforms:
                scrapers["linkedin"] = LinkedInScraper(page)
            if "indeed" in platforms:
                scrapers["indeed"] = IndeedScraper(page)

            # Search each keyword + location combo
            for kw in keywords:
                for loc in locations:
                    for platform_name, scraper in scrapers.items():
                        print(f"\n--- {platform_name}: '{kw}' in '{loc}' ---")
                        jobs = scraper.search(kw, loc, max_per_search)

                        # Fetch details for LinkedIn (Indeed already has snippets)
                        if fetch_details and platform_name == "linkedin" and jobs:
                            print(f"  Fetching details for top {min(10, len(jobs))} jobs...")
                            for i, job in enumerate(jobs[:10]):
                                job = scraper.get_job_detail(job)
                                time.sleep(1)  # Be polite
                                if (i + 1) % 5 == 0:
                                    print(f"    ...{i+1} done")

                        self.all_jobs.extend(jobs)
                        time.sleep(2)  # Pause between searches

            browser.close()

        # Deduplicate by title + company
        self.all_jobs = self._deduplicate(self.all_jobs)
        print(f"\n{'='*60}")
        print(f"Total unique jobs found: {len(self.all_jobs)}")
        print(f"{'='*60}")

        return self.all_jobs

    def _deduplicate(self, jobs: list) -> list:
        """Remove duplicate jobs based on title + company."""
        seen = set()
        unique = []
        for job in jobs:
            key = f"{job['title'].lower()}_{job['company'].lower()}"
            if key not in seen:
                seen.add(key)
                unique.append(job)
        return unique

    def save(self, output_path: str):
        """Save scraped jobs to JSON file."""
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.all_jobs, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.all_jobs)} jobs to {output_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="AI Job Hunter Pro — Job Scraper")
    parser.add_argument("--keywords", type=str,
                        default=",".join(DEFAULT_KEYWORDS),
                        help="Comma-separated search keywords")
    parser.add_argument("--locations", type=str,
                        default=",".join(DEFAULT_LOCATIONS),
                        help="Comma-separated locations")
    parser.add_argument("--platforms", type=str, default="linkedin,indeed",
                        help="Comma-separated platforms (linkedin, indeed)")
    parser.add_argument("--output", type=str,
                        default=os.path.join(OUTPUT_DIR, "jobs_scraped.json"),
                        help="Output JSON file path")
    parser.add_argument("--max-per-search", type=int, default=MAX_JOBS_PER_SEARCH,
                        help="Max jobs per keyword+location combo")
    parser.add_argument("--no-details", action="store_true",
                        help="Skip fetching job detail pages (faster)")
    parser.add_argument("--visible", action="store_true",
                        help="Show browser window (not headless)")
    parser.add_argument("--match", action="store_true",
                        help="After scraping, run RAG matching")
    parser.add_argument("--min-score", type=float, default=0.4,
                        help="Minimum RAG match score (with --match)")

    args = parser.parse_args()

    keywords = [k.strip() for k in args.keywords.split(",")]
    locations = [l.strip() for l in args.locations.split(",")]
    platforms = [p.strip() for p in args.platforms.split(",")]

    # Scrape
    scraper = JobScraper(headless=not args.visible)
    jobs = scraper.scrape(
        keywords=keywords,
        locations=locations,
        platforms=platforms,
        max_per_search=args.max_per_search,
        fetch_details=not args.no_details
    )
    scraper.save(args.output)

    # Optional: run RAG matching
    if args.match and jobs:
        print(f"\n{'='*60}")
        print("Running RAG matching...")
        print(f"{'='*60}")
        try:
            from rag_engine import RAGEngine
            engine = RAGEngine()
            if engine.resume_collection.count() == 0:
                print("[WARN] No resume imported. Run --import-resume first.")
            else:
                matched = engine.match_jobs(jobs, min_score=args.min_score)
                print(f"\nMatched {len(matched)} jobs above {args.min_score} threshold:\n")
                for i, job in enumerate(matched[:20], 1):
                    score = job["match_score"]
                    bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
                    print(f"  {i:2d}. [{bar}] {score:.3f}  {job['title']}")
                    print(f"      {job['company']} | {job.get('location', '')} | {job['platform']}")
                    if job.get("url"):
                        print(f"      {job['url'][:80]}")
                    print()

                # Save matched results
                match_path = args.output.replace(".json", "_matched.json")
                with open(match_path, "w", encoding="utf-8") as f:
                    json.dump(matched, f, ensure_ascii=False, indent=2)
                print(f"Matched results saved to {match_path}")
        except ImportError:
            print("[ERROR] Could not import rag_engine. Make sure you're in the skill directory.")


if __name__ == "__main__":
    main()
