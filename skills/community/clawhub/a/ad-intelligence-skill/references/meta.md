# Meta (Facebook / Instagram) Ad Intelligence

## Phase 1 — Web Scraping (No API Key Required)

### Tool Options
- **Playwright / Requests-HTML**: Headless browser scraping of facebook.com/ads/library
- **Apify actor**: `apify/facebook-ads-scraper` (free tier available)
- **ScrapeCreators**: Unofficial API, 100 free calls to start

### What Phase 1 Scraping Returns
- Page name, page ID, page profile picture URL
- Ad copy (body text)
- Creative image/video URL
- Ad format (image, video, carousel, none)
- CTA button text
- Landing page URL
- Platforms served (Facebook, Instagram, Messenger, Audience Network)
- Active/inactive status
- Ad start date (delivery_start_time)

### Phase 1 Python Code (Requests + Meta's internal endpoint)

```python
import requests
import time

def search_meta_ads_phase1(search_term: str, country: str = "ALL", 
                            media_type: str = "ALL", active_only: bool = True,
                            limit: int = 50) -> list[dict]:
    """
    Phase 1: Scrape Meta Ad Library using their internal search endpoint.
    No API key required. Works globally for all ad types.
    """
    base_url = "https://www.facebook.com/ads/library/async/search_ads/"
    
    params = {
        "q": search_term,
        "count": limit,
        "active_status": "active" if active_only else "all",
        "ad_type": "all",
        "country": country,
        "media_type": media_type.lower(),
        "content_languages[]": "",
        "search_type": "keyword_unordered",
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.facebook.com/ads/library/",
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Meta returns JSON with a "payload" field
        data = response.json()
        ads = data.get("payload", {}).get("results", [])
        
        normalized = []
        for ad in ads:
            snapshot = ad.get("snapshot", {})
            normalized.append({
                "platform": "meta",
                "ad_id": ad.get("adArchiveID"),
                "advertiser_name": snapshot.get("page_name"),
                "advertiser_page_url": snapshot.get("page_profile_uri"),
                "status": "active" if ad.get("isActive") else "inactive",
                "format": ad.get("snapshot", {}).get("videos") and "video" or
                          ad.get("snapshot", {}).get("images") and "image" or "unknown",
                "headline": snapshot.get("title"),
                "body_text": snapshot.get("body", {}).get("text"),
                "cta_text": snapshot.get("cta_text"),
                "destination_url": snapshot.get("link_url"),
                "creative_url": (snapshot.get("images") or [{}])[0].get("original_image_url"),
                "platforms_served": ad.get("publisherPlatform", []),
                "date_first_shown": ad.get("startDate"),
                "date_last_shown": ad.get("endDate"),
                "country": country,
                "source_phase": 1,
            })
        
        return normalized
    
    except Exception as e:
        print(f"Phase 1 Meta scrape failed: {e}")
        return []


# Usage example:
# ads = search_meta_ads_phase1("Nike", country="US", active_only=True)
```

### Phase 1 via ScrapeCreators (Unofficial API — 100 free calls)

```python
import requests

def meta_ads_scrapecreators(page_id_or_keyword: str, api_key: str, 
                             search_by: str = "keyword") -> list[dict]:
    """
    Phase 1 alternative using ScrapeCreators unofficial API.
    signup at scrapecreators.com — 100 free API calls.
    search_by: 'keyword' or 'page_id'
    """
    if search_by == "keyword":
        url = "https://api.scrapecreators.com/v1/facebookadlibrary/search"
        params = {"query": page_id_or_keyword}
    else:
        url = "https://api.scrapecreators.com/v1/facebookadlibrary/ads"
        params = {"page_id": page_id_or_keyword}
    
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers, params=params)
    return response.json().get("data", {}).get("ads", [])
```

---

## Phase 2a — Official Meta Ad Library API (Free, but limited)

### Setup Requirements
1. Facebook account (personal or business)
2. Verify identity at facebook.com/ID
3. Create a Meta Developer app at developers.facebook.com
4. Generate a User Access Token with `ads_read` permission
5. Token expires — refresh periodically (use long-lived tokens for automation)

### Key Limitation ⚠️
The official API only reliably returns data for:
- **EU-delivered ads** (all types)
- **Political/social issue ads** globally
- General ecommerce ads in non-EU countries are often missing

### API Endpoint

```
GET https://graph.facebook.com/v23.0/ads_archive
```

### Phase 2a Python Code

```python
import requests

def search_meta_ads_api(search_terms: str, access_token: str,
                         countries: list = ["US"], 
                         active_status: str = "ACTIVE",
                         media_type: str = "ALL",
                         date_min: str = None, date_max: str = None,
                         limit: int = 100) -> list[dict]:
    """
    Phase 2a: Official Meta Ad Library API.
    Returns richer data including spend/impression ranges (EU only).
    """
    url = "https://graph.facebook.com/v23.0/ads_archive"
    
    fields = [
        "id", "ad_archive_id", "page_id", "page_name",
        "ad_snapshot_url", "publisher_platforms",
        "ad_delivery_start_time", "ad_delivery_stop_time",
        "ad_creative_link_captions", "ad_creative_link_descriptions",
        "ad_creative_link_titles", "ad_creative_bodies",
        "spend", "impressions",  # Only populated for EU/political ads
        "currency",
        "demographic_distribution",  # EU only
    ]
    
    params = {
        "search_terms": search_terms,
        "ad_reached_countries": str(countries).replace("'", '"'),
        "ad_active_status": active_status,
        "media_type": media_type,
        "fields": ",".join(fields),
        "limit": limit,
        "access_token": access_token,
    }
    
    if date_min:
        params["ad_delivery_date_min"] = date_min  # format: YYYY-MM-DD
    if date_max:
        params["ad_delivery_date_max"] = date_max
    
    all_ads = []
    
    while True:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "error" in data:
            print(f"API Error: {data['error']}")
            break
        
        ads = data.get("data", [])
        all_ads.extend(ads)
        
        # Pagination
        paging = data.get("paging", {})
        next_cursor = paging.get("cursors", {}).get("after")
        if not next_cursor or not paging.get("next"):
            break
        params["after"] = next_cursor
    
    return all_ads


# Search by Page ID (more precise than keyword):
def get_ads_by_page_id(page_id: str, access_token: str, countries: list = ["US"]) -> list[dict]:
    url = "https://graph.facebook.com/v23.0/ads_archive"
    params = {
        "search_page_ids": page_id,
        "ad_reached_countries": str(countries).replace("'", '"'),
        "fields": "id,page_name,ad_snapshot_url,spend,impressions,publisher_platforms,ad_delivery_start_time",
        "limit": 100,
        "access_token": access_token,
    }
    response = requests.get(url, params=params)
    return response.json().get("data", [])
```

---

## Phase 2b — Third-Party Paid APIs (More Reliable, Global Coverage)

### Option 1: SearchAPI.io — Meta Ad Library Engine

```python
import requests

def meta_ads_searchapi(page_id: str, api_key: str, country: str = "ALL",
                        media_type: str = "all") -> dict:
    """
    SearchAPI.io Meta Ad Library — works globally, no geographic restriction.
    Returns: total ad count, page info, individual ad creatives.
    Pricing: paid (starts ~$50/mo for 5000 searches)
    """
    url = "https://www.searchapi.io/api/v1/search"
    params = {
        "engine": "meta_ad_library",
        "page_id": page_id,
        "ad_type": "all",
        "country": country,
        "media_type": media_type,
        "api_key": api_key,
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    ads = []
    for ad in data.get("ads", []):
        snapshot = ad.get("snapshot", {})
        ads.append({
            "platform": "meta",
            "ad_id": ad.get("ad_archive_id"),
            "advertiser_name": data.get("search_information", {})
                                   .get("ad_library_page_info", {}).get("page_name"),
            "status": "active" if ad.get("is_active") else "inactive",
            "body_text": snapshot.get("body", {}).get("text"),
            "headline": (snapshot.get("cards") or [{}])[0].get("title"),
            "cta_text": (snapshot.get("cards") or [{}])[0].get("cta_text"),
            "destination_url": (snapshot.get("cards") or [{}])[0].get("link_url"),
            "creative_url": snapshot.get("images", [None])[0],
            "platforms_served": ad.get("publisher_platform", []),
            "date_first_shown": ad.get("start_date"),
            "date_last_shown": ad.get("end_date"),
            "source_phase": 2,
        })
    
    return {
        "total_ads": data.get("search_information", {}).get("ads_count"),
        "page_info": data.get("search_information", {}).get("ad_library_page_info"),
        "ads": ads,
    }
```

### Option 2: SerpAPI — Meta Ad Library

```python
from serpapi import GoogleSearch

def meta_ads_serpapi(page_id: str, api_key: str) -> list[dict]:
    params = {
        "engine": "facebook_ad_library",
        "page_id": page_id,
        "api_key": api_key,
    }
    search = GoogleSearch(params)
    return search.get_dict().get("ads", [])
```

---

## Sample Normalized Output

```json
{
  "platform": "meta",
  "ad_id": "1617728395605978",
  "advertiser_name": "Nike",
  "advertiser_page_url": "https://www.facebook.com/nike/",
  "status": "active",
  "format": "video",
  "headline": "Just Do It",
  "body_text": "New season, new gear. Shop the latest Nike Running collection.",
  "cta_text": "Shop Now",
  "destination_url": "https://www.nike.com/running",
  "creative_url": "https://scontent.xx.fbcdn.net/v/t39...",
  "platforms_served": ["facebook", "instagram"],
  "date_first_shown": "2025-01-15",
  "date_last_shown": null,
  "country": "US",
  "spend_range": null,
  "impression_range": null,
  "source_phase": 1
}
```

---

## Finding a Page ID

To use page-ID-based lookup (more reliable than keyword search):
1. Go to `facebook.com/ads/library`
2. Search for the brand name
3. Click on the advertiser — the URL will contain the Page ID
4. Or use: `https://www.facebook.com/{page_slug}` and inspect the page source for `"pageID"`
