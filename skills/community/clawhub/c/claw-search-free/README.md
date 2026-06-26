# Claw Search - OpenClaw Skill

Free search API skill for OpenClaw agents. Similar to Brave Search API.

## Features

- **Web Search** - Search the web for any topic
- **Image Search** - Find images related to your query  
- **News Search** - Get latest news articles
- **Suggestions** - Autocomplete/suggestions endpoint
- **No API Key Required** - Free for all OpenClaw agents

## Usage

```javascript
// Using fetch directly
const response = await fetch('https://www.claw-search.com/api/search?q=your query');
const data = await response.json();

// Or use the web_search tool with custom URL
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/search` | Web search |
| `/api/images` | Image search |
| `/api/news` | News search |
| `/api/suggest` | Autocomplete |

## Parameters

- `q` - Search query (required)
- `count` - Number of results (default: 10)
- `offset` - Pagination offset (default: 0)

## Example Response

```json
{
  "query": "OpenClaw",
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

## Integration

To use with OpenClaw's web_search, configure your agent:

```json
{
  "web_search": {
    "url": "https://www.claw-search.com/api/search"
  }
}
```

Or use environment variable:
```
CLAW_SEARCH_URL=https://www.claw-search.com
```

## Rate Limits

- 100 requests per minute (default tier)
- Contact for higher limits

## License

MIT