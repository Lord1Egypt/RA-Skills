# LinkedIn Ad Library — Ad Intelligence

## What Data Is Available

LinkedIn's Ad Library (linkedin.com/ad-library) is primarily useful for **B2B competitor research**.
It shows publicly running ads from any company's LinkedIn page.

### Fields Available (Both Phases)
- Advertiser name and LinkedIn page URL
- Ad copy (body text / description)
- Headline
- CTA button text
- Ad format type (Single Image, Video, Carousel, Document, Text, Spotlight)
- Image URL / Video URL / Carousel images
- Destination URL / landing page
- Ad start date / end date
- Active / inactive status
- Impression range (e.g. "< 1k", "1k–10k") — available in some scrapers

### Fields Available in Phase 2 Only
- Targeting summary (partial: language, location, sometimes exclusion info)
- Total ad count for a company
- Continuation token for pagination through full ad history
- Advertiser LinkedIn company ID

### Fields NOT Available
- Exact spend or budget
- CTR or conversion rates
- Job title / seniority / company size targeting specifics
- Engagement metrics (likes, comments, shares)

---

## Phase 1 — Web Scraping (No API Key Required)

### Approach: Scrape linkedin.com/ad-library Directly

LinkedIn's Ad Library doesn't require login to browse. It uses a paginated infinite-scroll
interface. Playwright or Selenium can automate this.

```python
# Requirements: pip install playwright
# Run: playwright install chromium

from playwright.sync_api import sync_playwright
import json
import time

def scrape_linkedin_ads_phase1(company_name: str, max_ads: int = 30) -> list[dict]:
    """
    Phase 1: Scrape LinkedIn Ad Library for a company's ads.
    No API key needed. Uses Playwright headless browser.
    """
    base_url = f"https://www.linkedin.com/ad-library/search?q={company_name.replace(' ', '%20')}"
    
    ads = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()
        
        # Intercept network requests to capture API responses
        captured_ads = []
        
        def handle_response(response):
            if "ad-library/search" in response.url and response.status == 200:
                try:
                    body = response.json()
                    elements = body.get("elements", [])
                    captured_ads.extend(elements)
                except Exception:
                    pass
        
        page.on("response", handle_response)
        page.goto(base_url, wait_until="networkidle", timeout=30000)
        
        # Scroll to load more ads
        scroll_count = max(1, max_ads // 10)
        for _ in range(scroll_count):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
        
        browser.close()
        
        # Normalize captured ads
        for raw_ad in captured_ads[:max_ads]:
            content = raw_ad.get("content", {})
            ads.append({
                "platform": "linkedin",
                "ad_id": raw_ad.get("id"),
                "advertiser_name": raw_ad.get("advertiserName"),
                "advertiser_page_url": raw_ad.get("advertiserLinkedinPage"),
                "status": "active" if raw_ad.get("isActive") else "inactive",
                "format": raw_ad.get("adType", "").replace("_", " ").title(),
                "headline": content.get("headline"),
                "body_text": content.get("description"),
                "cta_text": raw_ad.get("cta"),
                "destination_url": raw_ad.get("destinationUrl"),
                "creative_url": content.get("image") or content.get("video"),
                "date_first_shown": raw_ad.get("startDate"),
                "date_last_shown": raw_ad.get("endDate"),
                "impression_range": raw_ad.get("totalImpressions"),
                "source_phase": 1,
            })
    
    return ads


# Alternative: simpler requests-based approach (may require session cookies)
import requests

def scrape_linkedin_ads_requests(company_name: str, api_key: str = None) -> list[dict]:
    """
    Phase 1 alt: ScrapeCreators LinkedIn Ad Library API.
    100 free calls. signup at scrapecreators.com.
    """
    url = "https://api.scrapecreators.com/v1/linkedinadlibrary/search"
    headers = {"x-api-key": api_key}
    params = {"company": company_name}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    ads = []
    for ad in data.get("data", {}).get("ads", []):
        ads.append({
            "platform": "linkedin",
            "ad_id": ad.get("id"),
            "advertiser_name": ad.get("advertiser"),
            "advertiser_page_url": ad.get("advertiserLinkedinPage"),
            "status": "active" if ad.get("isActive") else "inactive",
            "format": ad.get("adType"),
            "headline": ad.get("headline"),
            "body_text": ad.get("des"),
            "cta_text": ad.get("cta"),
            "destination_url": ad.get("destinationUrl"),
            "creative_url": ad.get("image") or ad.get("video"),
            "date_first_shown": ad.get("startDate"),
            "date_last_shown": ad.get("endDate"),
            "impression_range": ad.get("totalImpressions"),
            "source_phase": 1,
        })
    
    return ads
```

---

## Phase 2a — Adyntel API (Domain-Based, No LinkedIn Auth Required)

Adyntel is the most developer-friendly LinkedIn ad intelligence API.
Input: company domain → Output: paginated JSON of all their LinkedIn ads.
No Apify account, no LinkedIn cookies, no session management.

Pricing: check adyntel.com (paid API)

```python
import requests

def linkedin_ads_adyntel(domain: str, api_key: str, 
                          continuation_token: str = None,
                          limit: int = 25) -> dict:
    """
    Phase 2a: Adyntel LinkedIn Ads API.
    Pass a company domain (e.g. 'salesforce.com') and get all their LinkedIn ads.
    Returns ads + continuation_token for pagination + total_count.
    """
    url = "https://api.adyntel.com/v1/linkedin/ads"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"domain": domain}
    
    if continuation_token:
        params["continuation_token"] = continuation_token
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    ads = []
    for ad in data.get("ads", []):
        ads.append({
            "platform": "linkedin",
            "ad_id": ad.get("id"),
            "advertiser_name": ad.get("advertiser"),
            "advertiser_page_url": ad.get("advertiserLinkedinPage"),
            "status": "active" if ad.get("isActive") else "inactive",
            "format": ad.get("adType"),
            "headline": ad.get("headline"),
            "body_text": ad.get("des"),
            "cta_text": ad.get("cta"),
            "destination_url": ad.get("destinationUrl"),
            "creative_url": ad.get("image") or ad.get("video"),
            "carousel_images": ad.get("carouselImages", []),
            "date_first_shown": ad.get("startDate"),
            "date_last_shown": ad.get("endDate"),
            "impression_range": ad.get("totalImpressions"),
            "targeting_summary": _format_targeting(ad.get("targeting", {})),
            "source_phase": 2,
        })
    
    return {
        "total_ads": data.get("total_count"),
        "continuation_token": data.get("continuation_token"),
        "ads": ads,
    }


def _format_targeting(targeting: dict) -> str:
    """Format partial targeting info into readable string."""
    parts = []
    if targeting.get("language"):
        parts.append(targeting["language"])
    if targeting.get("location"):
        parts.append(targeting["location"])
    if targeting.get("company"):
        parts.append(targeting["company"])
    return " | ".join(parts) if parts else None


def linkedin_ads_adyntel_full(domain: str, api_key: str) -> list[dict]:
    """Fetch ALL ads for a domain by paginating through continuation tokens."""
    all_ads = []
    token = None
    
    while True:
        result = linkedin_ads_adyntel(domain, api_key, continuation_token=token)
        all_ads.extend(result["ads"])
        token = result.get("continuation_token")
        if not token:
            break
    
    return all_ads
```

---

## Phase 2b — Apify LinkedIn Ad Library Scrapers

Multiple community-maintained actors are available. Best ones:
- `silentflow/linkedin-ads-scraper` — stable, handles infinite scroll
- `operatorultra/linkedin-ad-library-scraper` — ultra-fast, proxy-free
- `silva95gustavo/linkedin-ad-library-scraper` — supports EU targeting data

```python
from apify_client import ApifyClient

def linkedin_ads_apify(company_name: str, apify_token: str, 
                        actor_id: str = "silentflow/linkedin-ads-scraper",
                        max_items: int = 100) -> list[dict]:
    """
    Phase 2b: Apify LinkedIn Ad Library Scraper.
    Requires Apify account (free tier available).
    actor_id: use 'silentflow/linkedin-ads-scraper' or 'operatorultra/linkedin-ad-library-scraper'
    """
    client = ApifyClient(apify_token)
    
    run_input = {
        "searchQuery": company_name,
        "maxItems": max_items,
        "proxyConfiguration": {"useApifyProxy": True},
    }
    
    run = client.actor(actor_id).call(run_input=run_input)
    
    ads = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        ads.append({
            "platform": "linkedin",
            "ad_id": item.get("id"),
            "advertiser_name": item.get("advertiser") or item.get("advertiserName"),
            "advertiser_page_url": item.get("advertiserLinkedinPage"),
            "status": "active" if item.get("isActive") else "inactive",
            "format": item.get("adType") or item.get("format"),
            "headline": item.get("headline"),
            "body_text": item.get("des") or item.get("description"),
            "cta_text": item.get("cta"),
            "destination_url": item.get("destinationUrl"),
            "creative_url": item.get("image") or item.get("video"),
            "date_first_shown": item.get("startDate") or item.get("adDuration"),
            "date_last_shown": item.get("endDate"),
            "impression_range": item.get("totalImpressions"),
            "targeting_summary": str(item.get("targeting", {})),
            "source_phase": 2,
        })
    
    return ads
```

---

## Phase 2c — SociaVault API

Domain or company-name based, simple REST endpoint.

```python
import requests

def linkedin_ads_sociavault(company_name: str, api_key: str) -> list[dict]:
    """Phase 2c: SociaVault LinkedIn Ad Library API."""
    url = "https://api.sociavault.com/v1/scrape/linkedin-ad-library/search"
    headers = {"x-api-key": api_key}
    params = {"company": company_name}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if not data.get("success"):
        return []
    
    ads = []
    for ad in data["data"].get("ads", []):
        ads.append({
            "platform": "linkedin",
            "ad_id": ad.get("id"),
            "advertiser_name": company_name,
            "format": ad.get("format"),
            "body_text": ad.get("text"),
            "headline": ad.get("headline"),
            "creative_url": ad.get("mediaUrl"),
            "date_first_shown": ad.get("startDate"),
            "source_phase": 2,
        })
    
    return ads
```

---

## Sample Normalized Output

```json
{
  "platform": "linkedin",
  "ad_id": "756473943",
  "advertiser_name": "Microsoft",
  "advertiser_page_url": "https://www.linkedin.com/company/1035",
  "status": "inactive",
  "format": "Single Image Ad",
  "headline": null,
  "body_text": "Register today and be part of the future of innovation...",
  "cta_text": null,
  "destination_url": "http://msft.it/6043sMFt3",
  "creative_url": "https://media.licdn.com/dms/image/v2/D5610AQH8f...",
  "date_first_shown": "2025-08-10T05:00:00.000Z",
  "date_last_shown": "2025-08-10T05:00:00.000Z",
  "impression_range": "< 1k",
  "targeting_summary": "Targeting includes English | Targeting includes Netherlands | Exclusion targeting applied",
  "source_phase": 2
}
```

---

## LinkedIn API Provider Comparison

| Provider | Input Method | Auth Required | Free Tier | Best For |
|---|---|---|---|---|
| Playwright (DIY) | Company name | None | Yes (free) | One-off scrapes |
| ScrapeCreators | Company name | API key | 100 calls | Quick lookups |
| Adyntel | Domain | API key | No | Production pipelines |
| Apify | Company name | Apify token | $5 credit | Bulk scraping |
| SociaVault | Company name | API key | Limited | Simple integrations |

---

## Finding a LinkedIn Company's Page Handle

LinkedIn Ad Library URLs follow this pattern:
`https://www.linkedin.com/ad-library/search?q=COMPANY_NAME`

To find the numeric company ID (needed for some APIs):
1. Go to the company's LinkedIn page
2. The URL will be: `linkedin.com/company/HANDLE` or `linkedin.com/company/ID`
3. View page source and search for `"companyId"` or inspect network requests
