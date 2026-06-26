---
name: ghost-closer-web-scraper
description: Scrape complete business intelligence from Google Maps, Facebook, and Instagram for any local business. Returns structured JSON with ratings, contact info, services, and media.
version: 1.0.0
tags: [scraping, business-intelligence, local-business, lead-generation]
---

# Ghost Closer Web Scraper

## Purpose
Automates the research phase of the Ghost Closer workflow. Given a business name and location, this skill scrapes Google Maps, Facebook, and Instagram to build a complete business intelligence profile in structured JSON.

## Requirements
- Python 3.10+
- Playwright (`pip install playwright`)
- Chrome running with remote debugging on port 9222
- `.env` file at `/Users/edwin/.openclaw/workspace/dreams-arts/.env`

## Usage

### From Command Line
```bash
python scraper.py "Business Name" "City, State"
```

### From Python
```python
from scraper import GhostCloserScraper

scraper = GhostCloserScraper()
result = await scraper.run("La Taza Coffee", "Caguas, PR")
print(result)
```

### Output Format
```json
{
  "business_name": "La Taza Coffee",
  "location_query": "Caguas, PR",
  "google_maps": {
    "name": "La Taza Coffee Shop",
    "rating": 4.7,
    "review_count": 312,
    "address": "123 Calle Comercio, Caguas, PR 00725",
    "phone": "+1-787-555-1234",
    "website": "https://latazacoffee.com",
    "hours": {"Mon": "7AM-9PM", "Tue": "7AM-9PM"},
    "categories": ["Coffee shop", "Cafe"],
    "photo_urls": ["https://..."]
  },
  "facebook": {
    "page_url": "https://facebook.com/latazacoffee",
    "followers": 2450,
    "likes": 2300,
    "logo_url": "https://...",
    "recent_posts": [
      {"text": "New seasonal blend!", "date": "2026-04-05", "likes": 45}
    ]
  },
  "instagram": {
    "handle": "@latazacoffee",
    "profile_url": "https://instagram.com/latazacoffee"
  },
  "services_or_menu": ["Espresso $3.50", "Latte $4.75"],
  "scraped_at": "2026-04-09T14:30:00Z"
}
```

## How Claude Should Use This Skill

1. **Identify the business**: Extract the business name and location from the user's request.
2. **Run the scraper**: Execute `python scraper.py "Business Name" "City, State"` via Bash.
3. **Parse the JSON output**: The script prints valid JSON to stdout.
4. **Use the data**: Feed into Ghost Closer page builder, lead generation, or competitive analysis.

## Error Handling
- If Google Maps returns no results, the `google_maps` field will be `null`.
- If Facebook page is not found, `facebook` will be `null`.
- Network errors are retried up to 3 times with exponential backoff.
- All errors are logged to stderr; stdout always contains valid JSON.

## Notes
- Connects to existing Chrome on port 9222 (never launches a new browser).
- Respects rate limits with built-in delays between requests.
- Photos are returned as URLs only (not downloaded).
