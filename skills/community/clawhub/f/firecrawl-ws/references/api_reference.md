# Firecrawl API Reference & SDK Guides

This reference guide is designed to provide quick lookup schemas and parameters for Firecrawl endpoints and SDK methods.

## 1. Endpoints & Schemas

### `/scrape` (POST)
Synchronously scrapes a single URL.
*   **Endpoint:** `https://api.firecrawl.dev/v2/scrape`
*   **Request Schema:**
    ```json
    {
      "url": "string (required)",
      "formats": ["markdown", "html", "rawHtml", "links", "images", "screenshot", "json"],
      "onlyMainContent": "boolean (default: true)",
      "includeTags": ["string"],
      "excludeTags": ["string"],
      "mobile": "boolean (default: false)",
      "waitFor": "integer (milliseconds)",
      "timeout": "integer (milliseconds, default: 60000)",
      "actions": [
        {
          "type": "wait|click|write|press|scroll|screenshot",
          "selector": "string",
          "text": "string",
          "key": "string",
          "milliseconds": "integer",
          "direction": "string"
        }
      ]
    }
    ```

### `/crawl` (POST)
Asynchronously crawls a domain starting from a base URL.
*   **Endpoint:** `https://api.firecrawl.dev/v2/crawl`
*   **Request Schema:**
    ```json
    {
      "url": "string (required)",
      "exclude": ["string (glob patterns)"],
      "includes": ["string (glob patterns)"],
      "limit": "integer (default: 10000)",
      "maxDepth": "integer (default: 10)",
      "mode": "default|fast",
      "scrapeOptions": {
        "formats": ["markdown"],
        "onlyMainContent": true
      }
    }
    ```

### `/map` (POST)
Discovers all URLs belonging to a domain.
*   **Endpoint:** `https://api.firecrawl.dev/v2/map`
*   **Request Schema:**
    ```json
    {
      "url": "string (required)",
      "search": "string (filter pattern)",
      "ignoreSitemap": "boolean (default: false)",
      "includeSubdomains": "boolean (default: false)",
      "limit": "integer (default: 5000)"
    }
    ```

### `/extract` (POST)
Asynchronously extracts structured data matching a schema.
*   **Endpoint:** `https://api.firecrawl.dev/v2/extract`
*   **Request Schema:**
    ```json
    {
      "urls": ["string"],
      "prompt": "string",
      "schema": "object (JSON Schema)"
    }
    ```

---

## 2. Python SDK Snippets

### Advanced Scrape
```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

scrape_result = app.scrape_url(
    "https://example.com",
    params={
        "formats": ["markdown", "screenshot"],
        "onlyMainContent": True,
        "actions": [
            {"type": "click", "selector": "button#load-more"},
            {"type": "wait", "milliseconds": 1000}
        ]
    }
)
```

### Async Crawl
```python
import time
from firecrawl import FirecrawlApp

app = FirecrawlApp()
crawl_job = app.crawl_url(
    "https://example.com",
    params={"limit": 50, "scrapeOptions": {"formats": ["markdown"]}},
    wait_until_done=False
)

while True:
    status = app.check_crawl_status(crawl_job["id"])
    if status["status"] in ["completed", "failed"]:
        break
    time.sleep(5)
```

---

## 3. TypeScript SDK Snippets

### Map Domain
```typescript
import FirecrawlApp from '@mendable/firecrawl-js';

const app = new FirecrawlApp({ apiKey: process.env.FIRECRAWL_API_KEY });

const result = await app.mapUrl('https://stripe.com', {
  search: 'pricing'
});
```

### Structured Extraction (Zod)
```typescript
import FirecrawlApp from '@mendable/firecrawl-js';
import { z } from 'zod';

const app = new FirecrawlApp();
const CompanySchema = z.object({
  name: z.string(),
  hq: z.string()
});

const extraction = await app.extract({
  urls: ['https://example.com/about'],
  prompt: 'Extract company details',
  schema: CompanySchema
});
```
