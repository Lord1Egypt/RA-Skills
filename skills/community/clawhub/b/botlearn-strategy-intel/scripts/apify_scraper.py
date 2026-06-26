"""
botlearn/strategy-intel — Apify Scraper
Scrapes public company data for strategic analysis
"""

import os
import requests
import json

APIFY_API_KEY = os.environ.get("APIFY_API_KEY")
BASE_URL = "https://api.apify.com/v2"


def scrape_company(company_name: str, depth: str = "quick") -> dict:
    """
    Scrape public data about a company using Apify actors.
    Returns structured raw data for analysis.
    """
    results = {}

    # 1. Google Search scrape — fastest signal
    results["search"] = run_google_search(company_name)

    if depth == "deep":
        results["crunchbase"] = run_crunchbase_scrape(company_name)

    return results


def run_google_search(company_name: str) -> list:
    """Use Apify Google Search Scraper actor"""
    actor_id = "apify~google-search-scraper"
    
    payload = {
        "queries": "\n".join([
            f"{company_name} strategy business model funding",
            f"{company_name} product competitors market positioning",
        ]),
        "maxPagesPerQuery": 1,
        "languageCode": "en",
    }

    run_url = f"{BASE_URL}/acts/{actor_id}/run-sync-get-dataset-items"
    
    response = requests.post(
        run_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {APIFY_API_KEY}"
        },
        json=payload,
        timeout=120
    )

    if response.status_code in (200, 201):
        return response.json()
    else:
        print(f"[Apify] Search scrape failed: {response.status_code}")
        print(f"[Apify] Error: {response.text[:500]}")
        return []


def run_crunchbase_scrape(company_name: str) -> dict:
    """Use Apify Crunchbase scraper for funding/investor data"""
    actor_id = "apify~crunchbase-scraper"
    
    payload = {
        "companyName": company_name,
        "maxItems": 1
    }

    run_url = f"{BASE_URL}/acts/{actor_id}/run-sync-get-dataset-items"
    
    response = requests.post(
        run_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {APIFY_API_KEY}"
        },
        json=payload,
        timeout=120
    )

    if response.status_code == 200:
        data = response.json()
        return data[0] if data else {}
    else:
        print(f"[Apify] Crunchbase scrape failed: {response.status_code}")
        return {}


if __name__ == "__main__":
    # Quick test
    import sys
    company = sys.argv[1] if len(sys.argv) > 1 else "Notion"
    print(f"Scraping: {company}")
    data = scrape_company(company)
    print(json.dumps(data, indent=2)[:2000])  # preview first 2000 chars
