#!/usr/bin/env python3
"""
AI Job Hunter Pro — Company Career Page Scraper v2
Uses real career page URLs provided by user. Supports Feishu/Mokahr job platforms.

Usage:
  python3 scripts/company_scraper.py --all --keywords "产品经理,Product Manager" --visible
  python3 scripts/company_scraper.py --companies google,bytedance,deepseek --merge --match
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
    print("[ERROR] playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)

OUTPUT_DIR = os.path.expanduser("~/.ai-job-hunter-pro")

# ---------------------------------------------------------------------------
# Company Career Page Configs — using real URLs
# ---------------------------------------------------------------------------
COMPANY_CONFIGS = {
    # === Big Tech (International) ===
    "google": {
        "name": "Google",
        "url": "https://www.google.com/about/careers/applications/jobs/results/?location=Shanghai&location=Beijing&location=Hangzhou&q={keywords}",
        "wait": 4,
        "selectors": {
            "cards": "[class*='lLd2De'], .sMn82b, li.lLd2De",
            "title": "h3, [class*='QJPWVe']",
            "location": "[class*='r0wTof'], [class*='location']",
            "link": "a[href*='/jobs/results/']",
        }
    },
    "microsoft": {
        "name": "Microsoft",
        "url": "https://apply.careers.microsoft.com/careers?start=0&sort_by=timestamp&keyword={keywords}&country=China",
        "wait": 8,
        "selectors": {
            "cards": "[class*='job-card'], [class*='card'], [class*='result'], tr[class*='row'], li[class*='item']",
            "title": "a[class*='title'], h2, h3, [class*='job-title']",
            "location": "[class*='location'], [class*='city']",
            "link": "a[href*='careers'], a[href*='job']",
        }
    },
    "amazon": {
        "name": "Amazon",
        "url": "https://www.amazon.jobs/en/search?base_query={keywords}&loc_query=China",
        "wait": 4,
        "selectors": {
            "cards": ".job-tile, [class*='job-card'], .result",
            "title": "h3 a, .job-title a, h3",
            "location": ".location-and-id, [class*='location']",
            "link": "a[href*='/jobs/']",
        }
    },
    "apple": {
        "name": "Apple",
        "url": "https://jobs.apple.com/zh-cn/search?search={keywords}&location=china-CHNC",
        "wait": 10,
        "selectors": {
            "cards": "[class*='table-row'], tbody tr, [class*='results'] tr, [class*='search-result']",
            "title": "a[class*='table--advanced-search__title'], td:first-child a, [class*='title'] a",
            "location": "[class*='table--advanced-search__location'], td:nth-child(2), [class*='location']",
            "link": "a[href*='/details/']",
        }
    },
    "nvidia": {
        "name": "NVIDIA",
        "url": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?q={keywords}&locationCountry=f2e609fe253a4b19a58c305ebabad23d",
        "wait": 6,
        "selectors": {
            "cards": "[data-automation-id='compositeContainer'], li[class*='css']",
            "title": "a[data-automation-id='jobTitle'], h3 a",
            "location": "[data-automation-id='locations'], dd[class*='css']",
            "link": "a[data-automation-id='jobTitle'], a[href*='/job/']",
        }
    },
    "tesla": {
        "name": "Tesla",
        "url": "https://app.mokahr.com/social-recruitment/tesla/46129#/jobs?keyword={keywords}&page=1&anchorName=jobsList",
        "wait": 6, "type": "mokahr",
        "selectors": {
            "cards": "[class*='job-list-item'], [class*='ant-list-item'], [class*='position-item']",
            "title": "[class*='job-name'], [class*='position-name'], h4",
            "location": "[class*='job-location'], [class*='city']",
            "link": "a[href*='job']",
        }
    },
    "booking": {
        "name": "Booking.com",
        "url": "https://jobs.booking.com/careers?query={keywords}&location=Shanghai",
        "wait": 5,
        "selectors": {
            "cards": "[class*='job-tile'], [class*='job-card'], [class*='card']",
            "title": "h3, [class*='job-title'], a[class*='title']",
            "location": "[class*='location']",
            "link": "a[href*='/job/'], a[href*='careers']",
        }
    },
    "shopee": {
        "name": "Shopee",
        "url": "https://careers.shopee.cn/jobs?keyword={keywords}",
        "wait": 6,
        "selectors": {
            "cards": "[class*='job-card'], [class*='position'], [class*='list-item']",
            "title": "[class*='job-title'], h3, [class*='name']",
            "location": "[class*='location'], [class*='city']",
            "link": "a[href*='job']",
        }
    },

    # === Chinese Tech Giants ===
    "bytedance": {
        "name": "ByteDance",
        "url": "https://jobs.bytedance.com/experienced/position?keywords={keywords}&location=CT_51&project=&type=&job_hot_flag=&current=1&limit=20",
        "wait": 6,
        "selectors": {
            "cards": "[class*='JobCard'], [class*='position-item'], [class*='list__item'], a[href*='/position/']",
            "title": "[class*='name'], [class*='title'], h3",
            "location": "[class*='city'], [class*='location'], [class*='address']",
            "link": "a[href*='/position/']",
        }
    },
    "alibaba": {
        "name": "Alibaba Group",
        "url": "https://talent-holding.alibaba.com/off-campus/position-list?lang=zh&keyword={keywords}",
        "wait": 6,
        "selectors": {
            "cards": "[class*='position-item'], [class*='job-item'], [class*='list-item'], [class*='card']",
            "title": "[class*='position-name'], h4, [class*='title'], [class*='name']",
            "location": "[class*='position-city'], [class*='location'], [class*='city']",
            "link": "a[href*='/position/'], a[href*='positionDetail']",
        }
    },
    "taotian": {
        "name": "Taobao/Tmall",
        "url": "https://talent.taotian.com/off-campus/position-list?lang=zh&search={keywords}",
        "wait": 6,
        "selectors": {
            "cards": "[class*='position-item'], [class*='job-item'], [class*='list-item'], [class*='card']",
            "title": "[class*='position-name'], h4, [class*='title'], [class*='name']",
            "location": "[class*='position-city'], [class*='location'], [class*='city']",
            "link": "a[href*='/position/'], a[href*='positionDetail']",
        }
    },
    "aliyun": {
        "name": "Alibaba Cloud",
        "url": "https://careers.aliyun.com/off-campus/position-list?lang=zh&keyword={keywords}",
        "wait": 6,
        "selectors": {
            "cards": "[class*='position-item'], [class*='job-item'], [class*='list-item'], [class*='card']",
            "title": "[class*='position-name'], h4, [class*='title'], [class*='name']",
            "location": "[class*='position-city'], [class*='location'], [class*='city']",
            "link": "a[href*='/position/'], a[href*='positionDetail']",
        }
    },
    "tencent": {
        "name": "Tencent",
        "url": "https://careers.tencent.com/search.html?keyword={keywords}&query=at_1",
        "wait": 6,
        "selectors": {
            "cards": "[class*='recruit-list-item'], [class*='post-item'], [class*='recruit-wrap']",
            "title": "[class*='recruit-title'], h4, [class*='title']",
            "location": "[class*='recruit-tips'] span, [class*='location']",
            "link": "a[href*='position']",
        }
    },

    # === AI Startups ===
    "deepseek": {
        "name": "DeepSeek",
        "url": "https://app.mokahr.com/social-recruitment/high-flyer/140576#/jobs?keyword={keywords}",
        "wait": 6, "type": "mokahr",
        "selectors": {
            "cards": "[class*='job-list-item'], [class*='ant-list-item'], [class*='position-item']",
            "title": "[class*='job-name'], [class*='position-name'], h4",
            "location": "[class*='job-location'], [class*='city']",
            "link": "a[href*='job']",
        }
    },
    "zhipu": {
        "name": "Zhipu AI (智谱)",
        "url": "https://zhipu-ai.jobs.feishu.cn/index/?keywords={keywords}&category=6791702736615409933&location=CT_125",
        "wait": 6, "type": "feishu",
        "selectors": {
            "cards": "[class*='JobCard'], [class*='position-item'], [class*='list__item'], a[href*='/position/']",
            "title": "[class*='name'], [class*='title'], h3",
            "location": "[class*='city'], [class*='location']",
            "link": "a[href*='/position/']",
        }
    },
    "minimax": {
        "name": "MiniMax",
        "url": "https://vrfi1sk8a0.jobs.feishu.cn/index/?keywords={keywords}",
        "wait": 6, "type": "feishu",
        "selectors": {
            "cards": "[class*='JobCard'], [class*='position-item'], [class*='list__item'], a[href*='/position/']",
            "title": "[class*='name'], [class*='title'], h3",
            "location": "[class*='city'], [class*='location']",
            "link": "a[href*='/position/']",
        }
    },
    "stepfun": {
        "name": "StepFun (阶跃星辰)",
        "url": "https://app.mokahr.com/social-recruitment/step/94904#/jobs?keyword={keywords}",
        "wait": 6, "type": "mokahr",
        "selectors": {
            "cards": "[class*='job-list-item'], [class*='ant-list-item'], [class*='position-item']",
            "title": "[class*='job-name'], [class*='position-name'], h4",
            "location": "[class*='job-location'], [class*='city']",
            "link": "a[href*='job']",
        }
    },
}

# Company groups for easy selection
COMPANY_GROUPS = {
    "bigtech": ["google", "microsoft", "amazon", "apple", "nvidia", "tesla"],
    "china": ["bytedance", "alibaba", "taotian", "aliyun", "tencent", "shopee"],
    "ai": ["deepseek", "zhipu", "minimax", "stepfun"],
    "travel": ["booking"],
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
        wait = config.get("wait", 5)

        print(f"  [{name}] Searching: {keywords}")

        try:
            self.page.goto(url, timeout=30000, wait_until="domcontentloaded")
            time.sleep(wait)

            # Scroll to load more
            for _ in range(3):
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
                except:
                    continue

            # Fallback: scan all links for job-related text
            if not jobs:
                jobs = self._fallback_scrape(name, company_key, keywords)

            return jobs

        except Exception as e:
            print(f"  [{name}] Error: {e}")
            return []

    def _parse_card(self, card, sel: dict, company_name: str, company_key: str) -> dict:
        title_el = card.query_selector(sel["title"])
        location_el = card.query_selector(sel["location"])
        link_el = card.query_selector(sel["link"])

        title = title_el.inner_text().strip() if title_el else ""
        location = location_el.inner_text().strip() if location_el else ""
        href = ""
        if link_el:
            href = link_el.get_attribute("href") or ""

        # If card itself is a link
        if not href:
            href = card.get_attribute("href") or ""

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
        print(f"  [{company_name}] Trying fallback scrape...")
        jobs = []
        kw_list = ["product", "manager", "pm", "产品", "经理"]

        links = self.page.query_selector_all("a")
        for link in links:
            try:
                text = link.inner_text().strip()
                href = link.get_attribute("href") or ""
                text_lower = text.lower()
                if any(kw in text_lower for kw in kw_list):
                    if 5 < len(text) < 120:
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

        seen = set()
        unique = []
        for j in jobs:
            if j["title"] not in seen:
                seen.add(j["title"])
                unique.append(j)

        print(f"  [{company_name}] Fallback found {len(unique)} jobs")
        return unique[:15]


def main():
    parser = argparse.ArgumentParser(description="AI Job Hunter Pro — Company Career Scraper v2")
    parser.add_argument("--companies", type=str, default="google,amazon,bytedance",
                        help="Comma-separated company keys, or group names: bigtech, china, ai, travel")
    parser.add_argument("--all", action="store_true", help="Scrape ALL configured companies")
    parser.add_argument("--keywords", type=str, default="Product Manager,产品经理",
                        help="Comma-separated search keywords")
    parser.add_argument("--output", type=str,
                        default=os.path.join(OUTPUT_DIR, "jobs_company.json"))
    parser.add_argument("--visible", action="store_true", help="Show browser")
    parser.add_argument("--match", action="store_true", help="Run RAG matching")
    parser.add_argument("--min-score", type=float, default=0.0)
    parser.add_argument("--merge", action="store_true", help="Merge with LinkedIn data")

    args = parser.parse_args()

    # Resolve company list
    if args.all:
        companies = list(COMPANY_CONFIGS.keys())
    else:
        companies = []
        for c in args.companies.split(","):
            c = c.strip().lower()
            if c in COMPANY_GROUPS:
                companies.extend(COMPANY_GROUPS[c])
            else:
                companies.append(c)
        companies = list(dict.fromkeys(companies))  # dedupe preserving order

    keywords_list = [k.strip() for k in args.keywords.split(",")]

    print(f"\n{'='*60}")
    print(f"AI Job Hunter Pro — Company Career Scraper v2")
    print(f"{'='*60}")
    print(f"Companies ({len(companies)}): {', '.join(companies)}")
    print(f"Keywords: {keywords_list}")
    print(f"{'='*60}\n")

    all_jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.visible)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="zh-CN"
        )
        page = context.new_page()
        scraper = CompanyCareerScraper(page)

        for company in companies:
            for kw in keywords_list:
                print(f"\n--- {company}: '{kw}' ---")
                jobs = scraper.scrape_company(company, kw)
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

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)
    print(f"Saved to {args.output}")

    # Merge
    if args.merge:
        linkedin_path = os.path.join(OUTPUT_DIR, "jobs_scraped.json")
        if os.path.exists(linkedin_path):
            with open(linkedin_path) as f:
                linkedin_jobs = json.load(f)
            merged = linkedin_jobs + unique
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
            print(f"Merged {len(merged_unique)} total jobs -> {merged_path}")

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
                if args.merge:
                    all_path = os.path.join(OUTPUT_DIR, "jobs_all.json")
                    if os.path.exists(all_path):
                        with open(all_path) as f:
                            match_source = json.load(f)

                matched = engine.match_jobs(match_source, min_score=args.min_score)
                print(f"\nMatched {len(matched)} jobs:\n")
                for i, job in enumerate(matched[:25], 1):
                    s = job["match_score"]
                    bar = chr(9608) * int(s * 20) + chr(9617) * (20 - int(s * 20))
                    print(f"  {i:2d}. [{bar}] {s:.3f}  {job['title'][:50]}")
                    print(f"      {job['company']} | {job.get('location','')} | {job.get('platform','')}")
                    print()

                match_path = os.path.join(OUTPUT_DIR, "jobs_scraped_matched.json")
                with open(match_path, "w", encoding="utf-8") as f:
                    json.dump(matched, f, ensure_ascii=False, indent=2)
                print(f"Matched results saved to {match_path}")
        except ImportError as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
