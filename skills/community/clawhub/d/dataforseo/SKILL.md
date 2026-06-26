---
name: dataforseo
description: Search Google and gather SEO data using the DataForSEO API. Supports SERP results, keyword data, backlinks, and on-page analysis. Use when you need high-volume Google searches (bulk lead generation), keyword research, rank tracking, or detailed SERP data at scale. Pay-as-you-go pricing with no monthly commitment. Requires DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD.
metadata:
  requires:
    env: [DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD]
  primaryEnv: DATAFORSEO_LOGIN
---

# DataForSEO Skill

Pay-as-you-go Google SERP + SEO data API. Best for high-volume lead generation at low cost. No monthly commitment — only pay for what you use.

## Credentials

```env
DATAFORSEO_LOGIN=your_email@example.com
DATAFORSEO_PASSWORD=your_password
```

Sign up at dataforseo.com. Minimum deposit: $50. Cost per SERP task: ~$0.0006 (very cheap for bulk).

## Quick Usage — SERP Search

```python
import requests, os, json
from base64 import b64encode

def dfs_auth():
    creds = f"{os.environ['DATAFORSEO_LOGIN']}:{os.environ['DATAFORSEO_PASSWORD']}"
    return b64encode(creds.encode()).decode()

def dfs_search(keyword: str, location: str = "United States", language: str = "en") -> list[dict]:
    """
    Search Google via DataForSEO Live SERP endpoint.
    Returns organic results: {url, title, description, rank_absolute, domain}
    """
    headers = {
        "Authorization": f"Basic {dfs_auth()}",
        "Content-Type": "application/json"
    }
    payload = [{
        "keyword": keyword,
        "location_name": location,
        "language_name": language,
        "device": "desktop",
        "os": "windows",
        "depth": 10
    }]
    
    url = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
    
    data = r.json()
    tasks = data.get("tasks", [])
    if not tasks or tasks[0]["status_code"] != 20000:
        return []
    
    items = tasks[0]["result"][0].get("items", [])
    organic = [i for i in items if i.get("type") == "organic"]
    
    return [{
        "title": i.get("title"),
        "url": i.get("url"),
        "description": i.get("description"),
        "rank": i.get("rank_absolute"),
        "domain": i.get("domain")
    } for i in organic]
```

## Lead Generation — Batch Mode (Most Efficient)

```python
def dfs_batch_search(queries: list[str], location: str = "United States") -> dict[str, list]:
    """
    Submit multiple queries in one API call (up to 100).
    Much more efficient — one round trip for many queries.
    Returns dict: {query: [results]}
    """
    headers = {
        "Authorization": f"Basic {dfs_auth()}",
        "Content-Type": "application/json"
    }
    
    # Build task list
    tasks = [{
        "keyword": q,
        "location_name": location,
        "language_name": "en",
        "device": "desktop",
        "depth": 10,
        "tag": q  # use query as tag for matching results
    } for q in queries]
    
    # Submit tasks
    url = "https://api.dataforseo.com/v3/serp/google/organic/task_post"
    r = requests.post(url, headers=headers, json=tasks)
    task_ids = [t["id"] for t in r.json()["tasks"] if t["status_code"] == 20100]
    
    # Poll for results (tasks complete in ~10–60 seconds)
    import time
    time.sleep(15)
    
    results = {}
    for task_id in task_ids:
        result_url = f"https://api.dataforseo.com/v3/serp/google/organic/task_get/advanced/{task_id}"
        res = requests.get(result_url, headers=headers)
        items = res.json()["tasks"][0]["result"][0].get("items", [])
        organic = [i for i in items if i.get("type") == "organic"]
        tag = res.json()["tasks"][0].get("tag", task_id)
        results[tag] = [{"title": i["title"], "url": i["url"], "domain": i.get("domain")} for i in organic]
    
    return results
```

## Available API Endpoints

| Category | Endpoint | Use Case |
|---|---|---|
| SERP (live) | `/serp/google/organic/live/advanced` | Single query, instant result |
| SERP (async) | `/serp/google/organic/task_post` | Bulk queries, cheaper |
| SERP (local) | `/serp/google/organic/live/advanced` + location_code | City-specific results |
| Maps | `/serp/google/maps/live/advanced` | Local business + phone + website |
| Keywords | `/keywords_data/google_ads/search_volume/live` | Search volume data |
| On-Page | `/on_page/task_post` | Full site audit |
| Backlinks | `/backlinks/summary/live` | Link profile |

## Maps Search (Best for Local Lead Gen)

```python
def dfs_maps_search(query: str, location_code: int = 1023191) -> list[dict]:
    """
    Search Google Maps for local businesses.
    Returns: {title, url, phone, address, rating, reviews_count}
    location_code 1023191 = Portland, OR. Find codes at:
    https://api.dataforseo.com/v3/serp/google/locations
    """
    headers = {"Authorization": f"Basic {dfs_auth()}", "Content-Type": "application/json"}
    payload = [{
        "keyword": query,
        "location_code": location_code,
        "language_code": "en",
        "device": "desktop"
    }]
    url = "https://api.dataforseo.com/v3/serp/google/maps/live/advanced"
    r = requests.post(url, headers=headers, json=payload)
    items = r.json()["tasks"][0]["result"][0].get("items", [])
    return [{
        "title": i.get("title"),
        "url": i.get("url"),
        "phone": i.get("phone"),
        "address": i.get("address"),
        "rating": i.get("rating", {}).get("value"),
        "reviews": i.get("rating", {}).get("votes_count"),
        "category": i.get("category")
    } for i in items if i.get("type") == "maps_search"]
```

## Location Codes (Common US Cities)

```python
LOCATION_CODES = {
    "Portland, OR": 1023191,
    "Seattle, WA": 1027744,
    "Dallas, TX": 1026339,
    "Chicago, IL": 1016367,
    "Los Angeles, CA": 1013962,
    "New York, NY": 1023191,
    "Denver, CO": 1016143,
    "Phoenix, AZ": 1023725,
    "Atlanta, GA": 1013971,
    "Miami, FL": 1017862,
}
# Full list: GET https://api.dataforseo.com/v3/serp/google/locations
```

## Pricing Reference

| Task Type | Cost Per 1K |
|---|---|
| SERP Live | ~$1.50 |
| SERP Async (batch) | ~$0.60 |
| Maps Live | ~$2.00 |
| Keywords (search vol) | ~$0.50 |

For lead gen at 50 queries/day: ~$0.03–$0.08/day.

## When to Use DataForSEO vs Serper

| Scenario | Use |
|---|---|
| Quick test / low volume | Serper.dev (free tier) |
| High volume (500+ queries/day) | DataForSEO (cheaper at scale) |
| Need Google Maps data (phone+website) | DataForSEO Maps endpoint |
| Need keyword volume data | DataForSEO Keywords |
| Need backlink data | DataForSEO Backlinks |
| Just need organic results fast | Serper.dev |
