---
name: getpost-scrape
description: "Scrape any web page with a headless browser. Extract text or screenshots."
version: "1.0.0"
---

# GetPost Web Scrape API

Scrape any web page using a headless browser. Extract text, take screenshots, wait for elements.

## Quick Start
```bash
# Sign up (no verification needed)
curl -X POST https://getpost.dev/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name": "YOUR_NAME", "bio": "What your agent does"}'
# Save the api_key from the response
```

## Authentication
```
Authorization: Bearer gp_live_YOUR_KEY
```

## Scrape a Page
```bash
curl -X POST https://getpost.dev/api/scrape \
  -H "Authorization: Bearer gp_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "extract_text": true}'
```
Cost: 5 credits per scrape.

## Options
- `url` (required) — the page to scrape
- `extract_text` — return extracted text content
- `screenshot` — return a screenshot
- `wait_for` — CSS selector to wait for before extracting

## Full Docs
https://getpost.dev/docs/api-reference#scrape
