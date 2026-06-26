# Exa API & SDK Reference Cheat Sheet
**Author**: Simon-Pierre Boucher

## 1. Quick API Endpoints

* **Base URL**: `https://api.exa.ai`
* **Authentication**: Header `x-api-key: <KEY>` or `Authorization: Bearer <KEY>`

### 1.1 `/search` (POST)
```json
{
  "query": "string (required)",
  "type": "auto | instant | fast | deep-lite | deep | deep-reasoning",
  "numResults": 10,
  "contents": {
    "text": true,
    "highlights": true,
    "summary": true
  },
  "includeDomains": ["string"],
  "excludeDomains": ["string"],
  "startPublishedDate": "ISO-8601-Date",
  "endPublishedDate": "ISO-8601-Date"
}
```

### 1.2 `/contents` (POST)
```json
{
  "urls": ["string"],
  "text": true,
  "highlights": { "query": "string" },
  "summary": true,
  "maxAgeHours": 0,
  "livecrawlTimeout": 10000,
  "subpages": 0
}
```

### 1.3 `/findSimilar` (POST)
```json
{
  "url": "string (required)",
  "numResults": 10,
  "includeDomains": ["string"]
}
```

---

## 2. SDK Reference

### Python (`exa-py`)
```python
from exa_py import Exa
exa = Exa(api_key="YOUR_KEY")

# Search
res = exa.search("query", type="auto", num_results=5)

# Extract Contents
contents = exa.get_contents(["url1", "url2"], text=True, max_age_hours=0)

# Similar
similar = exa.find_similar("url", num_results=5)
```

### TypeScript (`exa-js`)
```typescript
import Exa from "exa-js";
const exa = new Exa("YOUR_KEY");

const res = await exa.search("query", { type: "auto", numResults: 5 });
const contents = await exa.getContents(["url1"], { text: true, maxAgeHours: 0 });
```
