# Google Ads Transparency Center — Ad Intelligence

## What Data Is Available

Google's Ads Transparency Center (adstransparency.google.com) publicly exposes ads across:
- Google Search
- YouTube
- Display (websites in the Google Display Network)
- Gmail
- Google Maps
- Google Play

There is **no official public API** from Google. All data access is via scraping or
third-party wrappers (SerpAPI, SearchAPI.io, Apify).

### Fields Available (Both Phases)
- Advertiser name and advertiser ID
- Ad creative (image URL, video URL, ad text)
- Ad format (text, image, video)
- Date first shown / date last shown
- Total days shown
- Geographic region(s) where ad was shown
- Target domain (the advertiser's website)
- Link to ad preview on Google's site

### Fields NOT Available
- Spend / budget
- Impressions / clicks
- CTR or conversion data
- Exact targeting parameters

---

## Phase 1 — Web Scraping (No API Key Required)

### Option 1: Google Ads Transparency Scraper (PyPI)

A reverse-engineered open-source Python library.

```bash
pip install Google-Ads-Transparency-Scraper
```

```python
from GoogleAdsTransparencyScraper import GoogleAds

def search_google_ads_phase1(keyword: str, count: int = 50) -> list[dict]:
    """
    Phase 1: Scrape Google Ads Transparency Center using open-source library.
    No API key needed. Reverse-engineered internal API.
    """
    g = GoogleAds()
    
    # Get advertiser ID and creative IDs by keyword
    result = g.get_creative_Ids(keyword, count)
    
    if not result.get("Ad Count"):
        return []
    
    advertiser_id = result["Advertisor Id"]
    creative_ids = result["Creative_Ids"]
    
    ads = []
    for creative_id in creative_ids:
        try:
            ad_detail = g.get_detailed_ad(advertiser_id, creative_id)
            ads.append({
                "platform": "google",
                "ad_id": creative_id,
                "advertiser_id": advertiser_id,
                "advertiser_name": result.get("Advertisor Name"),
                "format": ad_detail.get("Ad Format", "unknown").lower(),
                "headline": ad_detail.get("Headline"),
                "body_text": ad_detail.get("Description"),
                "destination_url": ad_detail.get("Ad Link"),
                "creative_url": ad_detail.get("Image URL") or ad_detail.get("Video URL"),
                "date_first_shown": ad_detail.get("First Shown"),
                "date_last_shown": ad_detail.get("Last Shown"),
                "total_days_shown": ad_detail.get("Total Days Shown"),
                "country": None,
                "source_phase": 1,
            })
        except Exception as e:
            print(f"Error fetching ad {creative_id}: {e}")
            continue
    
    return ads


# Search by domain instead of keyword:
def search_google_ads_by_domain_phase1(domain: str, count: int = 50) -> list[dict]:
    """Search Google Ads Transparency by domain (e.g. 'nike.com')"""
    g = GoogleAds()
    
    # First, resolve domain to advertiser ID
    result = g.get_advertiser_by_domain(domain)
    if not result:
        return []
    
    advertiser_id = result["Advertisor Id"]
    creatives = g.get_creative_Ids(result["Name"], count)
    
    ads = []
    for creative_id in creatives.get("Creative_Ids", []):
        try:
            detail = g.get_detailed_ad(advertiser_id, creative_id)
            ads.append({
                "platform": "google",
                "ad_id": creative_id,
                "advertiser_id": advertiser_id,
                "advertiser_name": result["Name"],
                "format": detail.get("Ad Format", "").lower(),
                "body_text": detail.get("Description"),
                "destination_url": detail.get("Ad Link"),
                "creative_url": detail.get("Image URL") or detail.get("Video URL"),
                "date_first_shown": detail.get("First Shown"),
                "date_last_shown": detail.get("Last Shown"),
                "source_phase": 1,
            })
        except Exception:
            continue
    
    return ads
```

### Option 2: Direct Requests to Google's Internal API

Google Transparency Center uses an internal protobuf-based API that has been
reverse engineered. Use with caution — this may break if Google updates their internals.

```python
import requests
import json

def google_ads_raw_scrape(advertiser_id: str, region: int = 0) -> list[dict]:
    """
    Direct scrape of Google Transparency Center's internal API.
    region: 0 = all regions, 2840 = US, 2356 = India, 2276 = Germany, etc.
    """
    url = "https://adstransparency.google.com/api/v1/ads"
    
    params = {
        "advertiser_id": advertiser_id,
        "region": region,
        "format": "json",
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": f"https://adstransparency.google.com/advertiser/{advertiser_id}",
        "Accept": "application/json",
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        return []
    
    data = response.json()
    ads = []
    
    for ad in data.get("ads", []):
        ads.append({
            "platform": "google",
            "ad_id": ad.get("creativeId"),
            "advertiser_id": ad.get("advertiserId"),
            "advertiser_name": ad.get("advertiserName"),
            "format": ad.get("format", "").lower(),
            "creative_url": ad.get("imageUrl") or ad.get("videoUrl"),
            "date_first_shown": ad.get("firstShownDatetime"),
            "date_last_shown": ad.get("lastShownDatetime"),
            "total_days_shown": ad.get("totalDaysShown"),
            "source_phase": 1,
        })
    
    return ads
```

---

## Phase 2 — Third-Party APIs (More Reliable, Richer Data)

### Option 1: SerpAPI — Google Ads Transparency Center Engine

Reliable wrapper. Handles pagination, proxy rotation, anti-bot measures.
Pricing: starts at ~$50/mo, 100 free searches trial.

```python
from serpapi import GoogleSearch
import os

def google_ads_serpapi(domain: str = None, advertiser_id: str = None,
                        api_key: str = None, region: str = "2840",
                        creative_format: str = None,
                        start_date: str = None, end_date: str = None,
                        limit: int = 100) -> list[dict]:
    """
    Phase 2: SerpAPI Google Ads Transparency Center wrapper.
    Pass either domain (e.g. 'nike.com') or advertiser_id.
    region: SerpAPI region code. 2840=US, 2356=IN, 2276=DE, 2826=UK
    creative_format: 'text', 'image', or 'video'
    date format: 'YYYYMMDD'
    """
    params = {
        "engine": "google_ads_transparency_center",
        "api_key": api_key or os.environ["SERPAPI_KEY"],
        "region": region,
        "num": min(limit, 100),
    }
    
    if domain:
        params["text"] = domain  # domain-based search
    elif advertiser_id:
        params["advertiser_id"] = advertiser_id
    
    if creative_format:
        params["creative_format"] = creative_format  # text, image, video
    
    if start_date:
        params["start_date"] = start_date  # YYYYMMDD
    if end_date:
        params["end_date"] = end_date
    
    all_ads = []
    
    while True:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        ad_creatives = results.get("ad_creatives", [])
        all_ads.extend(ad_creatives)
        
        # Pagination
        next_page_token = results.get("serpapi_pagination", {}).get("next_page_token")
        if not next_page_token or len(all_ads) >= limit:
            break
        params["next_page_token"] = next_page_token
    
    # Normalize to standard schema
    normalized = []
    for ad in all_ads[:limit]:
        advertiser = ad.get("advertiser", {})
        normalized.append({
            "platform": "google",
            "ad_id": ad.get("id"),
            "advertiser_id": advertiser.get("id"),
            "advertiser_name": advertiser.get("name"),
            "advertiser_page_url": f"https://adstransparency.google.com/advertiser/{advertiser.get('id')}",
            "status": None,  # Google doesn't expose active/inactive
            "format": ad.get("format", "").lower(),
            "headline": ad.get("headline"),
            "body_text": ad.get("description"),
            "destination_url": ad.get("target_url"),
            "creative_url": ad.get("image_url") or ad.get("video_url"),
            "date_first_shown": ad.get("first_shown_datetime"),
            "date_last_shown": ad.get("last_shown_datetime"),
            "total_days_shown": ad.get("total_days_shown"),
            "platforms_served": ["google"],
            "country": region,
            "source_phase": 2,
        })
    
    return normalized


# Get the advertiser ID from a domain or company name first:
def find_google_advertiser_id(query: str, api_key: str) -> dict:
    """
    Find a Google advertiser's ID by searching their name or domain.
    Returns advertiser name and ID.
    """
    params = {
        "engine": "google_ads_transparency_center",
        "text": query,
        "api_key": api_key,
        "num": 5,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    # First result's advertiser is usually the target
    ads = results.get("ad_creatives", [])
    if ads:
        advertiser = ads[0].get("advertiser", {})
        return {"id": advertiser.get("id"), "name": advertiser.get("name")}
    return {}
```

### Option 2: SearchAPI.io — Google Ads Transparency Engine

```python
import requests

def google_ads_searchapi(domain: str, api_key: str, region: str = "US",
                          time_period: str = None) -> list[dict]:
    """
    SearchAPI.io Google Ads Transparency Center.
    time_period options: 'last_7_days', 'last_30_days', 'last_90_days', 'last_year'
    """
    url = "https://www.searchapi.io/api/v1/search"
    params = {
        "engine": "google_ads_transparency_center",
        "domain": domain,
        "region": region,
        "api_key": api_key,
    }
    if time_period:
        params["time_period"] = time_period
    
    response = requests.get(url, params=params)
    data = response.json()
    
    ads = []
    for ad in data.get("ad_creatives", []):
        advertiser = ad.get("advertiser", {})
        ads.append({
            "platform": "google",
            "ad_id": ad.get("id"),
            "advertiser_id": advertiser.get("id"),
            "advertiser_name": advertiser.get("name"),
            "format": ad.get("format", "").lower(),
            "creative_url": ad.get("image") or ad.get("video"),
            "date_first_shown": ad.get("first_shown_datetime"),
            "date_last_shown": ad.get("last_shown_datetime"),
            "total_days_shown": ad.get("total_days_shown"),
            "country": region,
            "source_phase": 2,
        })
    
    return ads
```

---

## Region Codes (for SerpAPI)

| Region | Code |
|---|---|
| United States | 2840 |
| India | 2356 |
| United Kingdom | 2826 |
| Germany | 2276 |
| France | 2250 |
| Brazil | 2076 |
| Canada | 2124 |
| Australia | 2036 |
| Anywhere (global) | 0 |

---

## Sample Normalized Output

```json
{
  "platform": "google",
  "ad_id": "CR06172042294124871681",
  "advertiser_id": "AR17828074650563772417",
  "advertiser_name": "Nike",
  "format": "image",
  "headline": "Shop New Arrivals",
  "body_text": "New Running Gear — Free Shipping on Orders Over $50",
  "destination_url": "https://nike.com/running",
  "creative_url": "https://displayads-formats.googleusercontent.com/ads/preview/...",
  "date_first_shown": "2025-01-15T00:00:00Z",
  "date_last_shown": "2025-03-04T19:41:49Z",
  "total_days_shown": 48,
  "country": "2840",
  "source_phase": 2
}
```

---

## Important Notes

- **Ad copy in images**: Many Google Display ads are image-only. Text extraction requires OCR
  (use pytesseract or a vision model on the `creative_url` image).
- **Advertiser ID lookup**: Before fetching ads, you typically need the advertiser's Google ID
  (format: `AR` + 18 digits). Use the search/text endpoint first to discover it.
- **Rate limiting**: SerpAPI allows 100 results per request; paginate using `next_page_token`.
- **Creative redirects**: Google returns redirect URLs for creatives like
  `https://displayads-formats.googleusercontent.com/ads/preview/...` — follow the redirect
  to get the actual image URL if needed.
