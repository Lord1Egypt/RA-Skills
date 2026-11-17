# Web API Reference

**App name:** `web`
**Base URL:** `https://api.superagnt.com/v1/data/web`
**Endpoints:** 3

Scrape any page as clean markdown or structured JSON, search the web and get full page content in one call, and map a site's URLs. Designed for LLMs and automation.

## Authentication

All requests require the superagnt API key:

```
Authorization: Bearer $SUPERAGNT_API_KEY
```

---

## Available Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `POST` | `/scrape` | Scrape a web page |
| `POST` | `/search` | Search the web |
| `POST` | `/map` | Map a website's URLs |

## Tool Schemas

The following JSON defines all available tools with their parameters. Each tool maps to an API endpoint.

```json
[
  {
    "name": "superagnt_web_scrape",
    "description": "Scrape a web page",
    "method": "POST",
    "path": "/scrape",
    "parameters": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "description": "The URL to scrape (must be a publicly reachable http(s) URL)."
        },
        "formats": {
          "type": "array",
          "description": "Output formats to return. Each entry is either a string preset or an object form. String presets: 'markdown' (default), 'summary', 'html', 'rawHtml', 'links', 'images'. Object forms include { type: 'json', schema, prompt } for structured extraction, { type: 'screenshot', fullPage, quality } for an image, and { type: 'changeTracking', modes } for diffs. Defaults to ['markdown'] when omitted."
        },
        "onlyMainContent": {
          "type": "boolean",
          "description": "Return only the main content of the page, excluding navs, headers, and footers."
        },
        "includeTags": {
          "type": "array",
          "description": "Only include content within these HTML tags / CSS selectors."
        },
        "excludeTags": {
          "type": "array",
          "description": "Exclude content within these HTML tags / CSS selectors."
        },
        "maxAge": {
          "type": "integer",
          "description": "Return cached content up to this age in milliseconds (faster, cheaper). Default 172800000 (2 days)."
        },
        "waitFor": {
          "type": "integer",
          "description": "Milliseconds to wait for the page to render before scraping."
        },
        "mobile": {
          "type": "boolean",
          "description": "Emulate a mobile device."
        },
        "timeout": {
          "type": "integer",
          "description": "Request timeout in milliseconds (1000-300000). Default 60000."
        },
        "parsers": {
          "type": "array",
          "description": "PDF parsing configuration."
        },
        "proxy": {
          "type": "string",
          "description": "Proxy / anti-bot mode. 'auto' (default) escalates only on failure; 'enhanced' forces advanced anti-bot handling and costs more."
        },
        "location": {
          "type": "object",
          "description": "Geographic proxy location and language settings."
        }
      },
      "required": [
        "url"
      ]
    }
  },
  {
    "name": "superagnt_web_search",
    "description": "Search the web",
    "method": "POST",
    "path": "/search",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "The search query."
        },
        "limit": {
          "type": "integer",
          "description": "Number of results per source. Default 10."
        },
        "sources": {
          "type": "array",
          "description": "Which result sources to query. Defaults to ['web']. Each entry is a preset string or an object with a `type`."
        },
        "categories": {
          "type": "array",
          "description": "Restrict results to these categories."
        },
        "tbs": {
          "type": "string",
          "description": "Time-based search filter (e.g. 'qdr:d' for past day)."
        },
        "location": {
          "type": "string",
          "description": "Geo-target for the search (e.g. 'San Francisco, California, United States')."
        },
        "country": {
          "type": "string",
          "description": "ISO country code. Default 'US'."
        },
        "includeDomains": {
          "type": "array",
          "description": "Only return results from these hostnames (mutually exclusive with excludeDomains)."
        },
        "excludeDomains": {
          "type": "array",
          "description": "Exclude results from these hostnames (mutually exclusive with includeDomains)."
        },
        "timeout": {
          "type": "integer",
          "description": "Request timeout in milliseconds. Default 60000."
        },
        "scrapeOptions": {
          "type": "object",
          "description": "When provided, each result is also scraped and its content returned. Accepts the same content options as /scrape (e.g. `formats`, `onlyMainContent`). Increases cost because every result is fetched."
        }
      },
      "required": [
        "query"
      ]
    }
  },
  {
    "name": "superagnt_web_map",
    "description": "Map a website's URLs",
    "method": "POST",
    "path": "/map",
    "parameters": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "description": "The base URL of the site to map."
        },
        "search": {
          "type": "string",
          "description": "Order returned URLs by relevance to this query."
        },
        "sitemap": {
          "type": "string",
          "description": "How to use the site's sitemap. Default 'include'."
        },
        "includeSubdomains": {
          "type": "boolean",
          "description": "Include URLs on subdomains."
        },
        "ignoreQueryParameters": {
          "type": "boolean",
          "description": "Treat URLs that differ only by query string as the same URL."
        },
        "limit": {
          "type": "integer",
          "description": "Maximum number of URLs to return. Default 5000, max 100000."
        },
        "timeout": {
          "type": "integer",
          "description": "Request timeout in milliseconds."
        },
        "location": {
          "type": "object",
          "description": "Geographic proxy location and language settings."
        }
      },
      "required": [
        "url"
      ]
    }
  }
]
```

## Example

```bash
curl -X POST "https://api.superagnt.com/v1/data/web/scrape" \
  -H "Authorization: Bearer $SUPERAGNT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

## Links

- [Documentation](https://superagnt.com/docs)
- [API Reference](https://superagnt.com/docs/apis/web)
- [superagnt app](https://app.superagnt.com/dashboard)
