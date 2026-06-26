# Claw Search Skill

🦞 **Free Search API for OpenClaw Agents**

## What This Does

Provides web search, image search, news search, and suggestions - all without requiring an API key.

## When to Use

When your agent needs to search the web, find images, or get latest news. Replace paid APIs like Brave Search with this free alternative.

## How to Use

```javascript
// Web search
const results = await fetch('https://www.claw-search.com/api/search?q=your query');
const data = await results.json();

// Image search  
const images = await fetch('https://www.claw-search.com/api/images?q=cats');
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/search` | Web search results |
| GET | `/api/images` | Image search |
| GET | `/api/news` | News search |
| GET | `/api/suggest` | Autocomplete suggestions |

## Parameters

- `q` (required): Search query
- `count`: Number of results (default: 10)
- `offset`: Pagination offset

## Example

```json
{
  "query": "OpenClaw AI",
  "web": {
    "results": [
      {
        "title": "OpenClaw - AI Assistant",
        "url": "https://openclaw.ai",
        "description": "Powerful AI assistant..."
      }
    ]
  }
}
```

## Notes

- No API key needed
- 100 requests/minute
- Powered by DuckDuckGo (fallback)
- Works with all OpenClaw agents