---
name: exa
description: |
  Exa API integration with managed API key authentication. Perform neural web search, retrieve page contents, find similar pages, get AI-generated answers, and run async research tasks.
  Use this skill when users want to search the web, extract content from URLs, find similar websites, get research answers with citations, or run deep research tasks.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Exa

Access the Exa API with managed API key authentication. Perform neural web searches, retrieve page contents, find similar pages, get AI-generated answers with citations, and run async research tasks.

## Quick Start

```bash
# Search the web
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"query": "latest AI research", "numResults": 5}).encode()
req = urllib.request.Request('https://gateway.maton.ai/exa/search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/exa/{endpoint}
```

Replace `{endpoint}` with the Exa API endpoint (`search`, `contents`, `findSimilar`, `answer`, `research/v1`). The gateway proxies requests to `api.exa.ai` and automatically injects your API key.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Exa API key connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=exa&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'exa', 'method': 'API_KEY'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

Open the returned `url` in a browser to enter your Exa API key.

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Exa connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"query": "AI news"}).encode()
req = urllib.request.Request('https://gateway.maton.ai/exa/search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### Search

Perform a neural web search with optional content extraction.

```bash
POST /exa/search
Content-Type: application/json

{
  "query": "latest AI research papers",
  "numResults": 10
}
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Search query string |
| numResults | integer | No | Number of results (max 100, default 10) |
| type | string | No | Search type: `neural`, `auto` (default), `keyword` |
| category | string | No | Filter by category: `company`, `research paper`, `news`, `tweet`, `personal site`, `financial report`, `people` |
| includeDomains | array | No | Only include these domains |
| excludeDomains | array | No | Exclude these domains |
| startPublishedDate | string | No | ISO 8601 date filter (after) |
| endPublishedDate | string | No | ISO 8601 date filter (before) |
| contents | object | No | Content extraction options (see below) |

**Contents Options:**

```json
{
  "contents": {
    "text": true,
    "highlights": true,
    "summary": true
  }
}
```

| Option | Type | Description |
|--------|------|-------------|
| text | boolean/object | Extract full page text |
| highlights | boolean/object | Extract relevant snippets |
| summary | boolean/object | Generate AI summary |

**Response:**

```json
{
  "requestId": "abc123",
  "resolvedSearchType": "neural",
  "results": [
    {
      "id": "https://example.com/article",
      "title": "Article Title",
      "url": "https://example.com/article",
      "publishedDate": "2024-01-15T00:00:00.000Z",
      "author": "Author Name",
      "text": "Full page content...",
      "highlights": ["Relevant snippet 1", "Relevant snippet 2"],
      "summary": "AI-generated summary..."
    }
  ],
  "costDollars": {
    "total": 0.005
  }
}
```

### Get Contents

Retrieve full page contents for specific URLs.

```bash
POST /exa/contents
Content-Type: application/json

{
  "ids": ["https://example.com/page1", "https://example.com/page2"],
  "text": true
}
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ids | array | Yes | List of URLs to fetch content from |
| text | boolean | No | Include full page text |
| highlights | boolean/object | No | Include relevant snippets |
| summary | boolean/object | No | Generate AI summary |

**Response:**

```json
{
  "requestId": "abc123",
  "results": [
    {
      "id": "https://example.com/page1",
      "url": "https://example.com/page1",
      "title": "Page Title",
      "text": "Full page content..."
    }
  ]
}
```

### Find Similar

Find pages similar to a given URL.

```bash
POST /exa/findSimilar
Content-Type: application/json

{
  "url": "https://example.com",
  "numResults": 10
}
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | URL to find similar pages for |
| numResults | integer | No | Number of results (max 100, default 10) |
| includeDomains | array | No | Only include these domains |
| excludeDomains | array | No | Exclude these domains |
| contents | object | No | Content extraction options |

**Response:**

```json
{
  "requestId": "abc123",
  "results": [
    {
      "id": "https://similar-site.com",
      "title": "Similar Site",
      "url": "https://similar-site.com",
      "score": 0.95
    }
  ],
  "costDollars": {
    "total": 0.005
  }
}
```

### Answer

Get an AI-generated answer to a question with citations.

```bash
POST /exa/answer
Content-Type: application/json

{
  "query": "What is machine learning?",
  "text": true
}
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Question to answer |
| text | boolean | No | Include source text in response |

**Response:**

```json
{
  "requestId": "abc123",
  "answer": "Machine learning is a subset of artificial intelligence...",
  "citations": [
    {
      "id": "https://example.com/ml-guide",
      "url": "https://example.com/ml-guide",
      "title": "Machine Learning Guide"
    }
  ]
}
```

### Research Tasks

Run asynchronous research tasks that explore the web, gather sources, and synthesize findings with citations.

#### Create Research Task

```bash
POST /exa/research/v1
Content-Type: application/json

{
  "instructions": "What are the top AI companies and their main products?",
  "model": "exa-research"
}
```

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| instructions | string | Yes | What to research (max 4096 chars) |
| model | string | No | Model to use: `exa-research-fast`, `exa-research` (default), `exa-research-pro` |
| outputSchema | object | No | JSON Schema for structured output |

**Response:**

```json
{
  "researchId": "r_01abc123",
  "createdAt": 1772969504083,
  "model": "exa-research",
  "instructions": "What are the top AI companies...",
  "status": "running"
}
```

#### Get Research Task

```bash
GET /exa/research/v1/{researchId}
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| events | string | Set to `true` to include event log |
| stream | string | Set to `true` for SSE streaming |

**Response (completed):**

```json
{
  "researchId": "r_01abc123",
  "status": "completed",
  "createdAt": 1772969504083,
  "finishedAt": 1772969520000,
  "model": "exa-research",
  "instructions": "What are the top AI companies...",
  "output": {
    "content": "Based on my research, the top AI companies are..."
  },
  "costDollars": {
    "total": 0.15,
    "numSearches": 5,
    "numPages": 20,
    "reasoningTokens": 1500
  }
}
```

**Status values:** `pending`, `running`, `completed`, `canceled`, `failed`

#### List Research Tasks

```bash
GET /exa/research/v1?limit=10
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| limit | integer | Results per page (1-50, default 10) |
| cursor | string | Pagination cursor |

**Response:**

```json
{
  "data": [
    {
      "researchId": "r_01abc123",
      "status": "completed",
      "model": "exa-research",
      "instructions": "What are the top AI companies..."
    }
  ],
  "hasMore": false,
  "nextCursor": null
}
```

## Code Examples

### JavaScript

```javascript
// Search with content extraction
const response = await fetch('https://gateway.maton.ai/exa/search', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'latest AI news',
    numResults: 5,
    contents: { text: true, highlights: true }
  })
});
const data = await response.json();
```

### Python

```python
import os
import requests

# Search with content extraction
response = requests.post(
    'https://gateway.maton.ai/exa/search',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'query': 'latest AI news',
        'numResults': 5,
        'contents': {'text': True, 'highlights': True}
    }
)
data = response.json()
```

## Notes

- Search types: `neural` (semantic), `auto` (hybrid), `keyword` (traditional)
- Maximum 100 results per search request
- Content extraction (text, highlights, summary) incurs additional costs
- Categories like `people` and `company` have restricted filter support
- Timestamps are in ISO 8601 format
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Exa connection or invalid request |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Exa API |

## Resources

- [Exa API Documentation](https://exa.ai/docs)
- [Exa API Reference](https://exa.ai/docs/reference/search)
- [Exa Dashboard](https://dashboard.exa.ai)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
